# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** rabby @ 663c0e80e9f6 · Rabby Wallet (DeBank) — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-28 18:13 UTC |
| Версия отчёта | 1 |
| Запуск аудита | e5611530-27b9-4a86-bf92-59f3f7ed161f (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `cd71a6408082cfedd9f571cc9cd9d48a53b708d27b8a87e76466454bfa56cbf9` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **2**
- Высокая: **74**
- Средняя: **78**
- Низкая: **3**
- Информационная: **3**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 154
- Подтверждённая ошибка конфигурации: 1
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 2
- Рекомендация по улучшению: 2
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/RabbyHub/Rabby> @ `663c0e80e9f6139cbb87932ddea909e1e4a382f1` — ссылки в доказательствах открывают строки на этом коммите.

1694 файлов, всего 10750140 байт, редактирований: 7; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 1692 | _raw/go-rabby-link-router.js: 57 lines scanned with 16 rule patterns and 122 registry patterns; _raw/sw.js: 198 lines scanned with 16 rule patterns and 122 registry patterns; changeLogs/index.ts: 87 lines scanned with 16 rule patterns and 122 registry patterns |
| dependencies | проверено | 2 | package.json: 208 dependencies parsed (207 pinned); yarn.lock: 2477 dependencies parsed (2477 pinned) |
| secrets | проверено | 5 | scripts/manual-qa/tempo-security-cases.js: 2 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); src/constant/index.ts: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); src/constant/tempo.ts: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| tls_key_exchange_groups | Недостаточность данных | 2 | src/ui/views/DesktopPerps/modal/PositionTpSlModal/index.tsx line 459: not in the algorithm registry, not assessed: {partialGroups}; src/ui/views/DesktopPerps/modal/PositionTpSlModal/index.tsx line 506: not in the algorithm registry, not assessed: {positionGroups} |
| tls_configuration | проверено | 1 | src/ui/views/DesktopPerps/modal/PositionTpSlModal/index.tsx: openssl TLS directives parsed |
| osv_advisories | проверено | 1 | 1000 pinned packages queried at OSV.dev; 21 affected (3 of them only in development or build dependencies) |
| osv_advisories | Недостаточность данных | 6 | npm/axios@0.24.0: 23 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest; npm/axios@1.12.2: 32 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest; npm/axios@1.13.2: 35 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- tls_key_exchange_groups — Недостаточность данных: src/ui/views/DesktopPerps/modal/PositionTpSlModal/index.tsx line 459: not in the algorithm registry, not assessed: {partialGroups}
- tls_key_exchange_groups — Недостаточность данных: src/ui/views/DesktopPerps/modal/PositionTpSlModal/index.tsx line 506: not in the algorithm registry, not assessed: {positionGroups}
- osv_advisories — Недостаточность данных: npm/axios@0.24.0: 23 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories — Недостаточность данных: npm/axios@1.12.2: 32 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories — Недостаточность данных: npm/axios@1.13.2: 35 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories — Недостаточность данных: npm/axios@1.15.2: 28 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories — Недостаточность данных: npm/axios@0.21.4: 23 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories — Недостаточность данных: npm/axios@0.27.2: 24 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest

## 5. Краткое описание архитектуры

Static review of the source tree rabby at 663c0e80e9f6139cbb87932ddea909e1e4a382f1. 1694 files analysed; of 3192 files, 171 are test, fuzzing, benchmark or example code and were left out, 1325 are not read by any analyzer, 1 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **0** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 43.9%

## 7. Подробное описание находок

### QSI-2026-05639 — @openzeppelin/contracts 3.4.1-solc-0.7-2 затронут GHSA-fg47-3c2x-m2wr (CVE-2021-39167)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@3.4.1-solc-0.7-2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 40.6 / 100
- CVSS v3.1: 10.0 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-fg47-3c2x-m2wr (CVE-2021-39167) для пакета npm @openzeppelin/contracts версии 3.4.1-solc-0.7-2: TimelockController vulnerability in OpenZeppelin Contracts. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-fg47-3c2x-m2wr
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-fg47-3c2x-m2wr](https://osv.dev/vulnerability/GHSA-fg47-3c2x-m2wr) · line 4591 · SHA-256 168531d671c5f74ade60ec81cf57f2b9d061c10cf639c9076268ec0fd8f1db82_

```
{"id": "GHSA-fg47-3c2x-m2wr", "aliases": ["CVE-2021-39167"], "modified": "2026-07-08T06:29:37.864167374Z", "summary": "TimelockController vulnerability in OpenZeppelin Contracts ", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.4.2, 4.3.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05643 — @openzeppelin/contracts 3.4.2-solc-0.7 затронут GHSA-fg47-3c2x-m2wr (CVE-2021-39167)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@3.4.2-solc-0.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 40.6 / 100
- CVSS v3.1: 10.0 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-fg47-3c2x-m2wr (CVE-2021-39167) для пакета npm @openzeppelin/contracts версии 3.4.2-solc-0.7: TimelockController vulnerability in OpenZeppelin Contracts. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-fg47-3c2x-m2wr
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-fg47-3c2x-m2wr](https://osv.dev/vulnerability/GHSA-fg47-3c2x-m2wr) · line 4598 · SHA-256 168531d671c5f74ade60ec81cf57f2b9d061c10cf639c9076268ec0fd8f1db82_

```
{"id": "GHSA-fg47-3c2x-m2wr", "aliases": ["CVE-2021-39167"], "modified": "2026-07-08T06:29:37.864167374Z", "summary": "TimelockController vulnerability in OpenZeppelin Contracts ", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.4.2, 4.3.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05625 — fflate 0.8.2 затронут GHSA-px8p-9vwx-vf98 (CVE-2026-45820)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/fflate@0.8.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-px8p-9vwx-vf98 (CVE-2026-45820) для пакета npm fflate версии 0.8.2: fflate unzipSync can enter an infinite loop when parsing malformed ZIP64 archives. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-px8p-9vwx-vf98
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-px8p-9vwx-vf98](https://osv.dev/vulnerability/GHSA-px8p-9vwx-vf98) · manifest · SHA-256 6e7711718042d9137f2381f8a724c5802eb16bbcd68520d2d1ce67d9fd7cc87f_

```
{"id": "GHSA-px8p-9vwx-vf98", "aliases": ["CVE-2026-45820"], "modified": "2026-09-10T03:50:52.758792289Z", "summary": "fflate unzipSync can enter an infinite loop when parsing malformed ZIP64 archives", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:U/S:N/AU:Y/R:U/V:D/RE:M/U:Amber"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.4.9, 0.5.4, 0.6.11, 0.7.5, 0.8.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05627 — lodash 4.17.21 затронут GHSA-r5fr-rjxr-66jc (CVE-2026-4800)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/lodash@4.17.21`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: 8.1 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-r5fr-rjxr-66jc (CVE-2026-4800) для пакета npm lodash версии 4.17.21: lodash vulnerable to Code Injection via `_.template` imports key names. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-r5fr-rjxr-66jc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-r5fr-rjxr-66jc](https://osv.dev/vulnerability/GHSA-r5fr-rjxr-66jc) · manifest · SHA-256 34e248cbde009d2e62d040ca3cb170063d1f73728fde2cfb9f0e3258a5682cb1_

```
{"id": "GHSA-r5fr-rjxr-66jc", "aliases": ["CVE-2026-4800"], "modified": "2026-10-17T02:56:15.633068434Z", "summary": "lodash vulnerable to Code Injection via `_.template` imports key names", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05632 — nanoid 3.3.6 затронут GHSA-xwg4-73v4-xw9w (CVE-2026-73086)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/nanoid@3.3.6`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: 7.4 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-xwg4-73v4-xw9w (CVE-2026-73086) для пакета npm nanoid версии 3.3.6: nanoid: Integer Overflow or Wraparound. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xwg4-73v4-xw9w
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xwg4-73v4-xw9w](https://osv.dev/vulnerability/GHSA-xwg4-73v4-xw9w) · manifest · SHA-256 e5fd27a6e5674297d69b8c6ce0e804051e5f6a8eeacfadcaa5bde90cca166035_

```
{"id": "GHSA-xwg4-73v4-xw9w", "aliases": ["CVE-2026-73086"], "modified": "2026-09-01T19:30:08.615560716Z", "summary": "nanoid: Integer Overflow or Wraparound", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.3.12, 5.1.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05633 — uuid 9.0.0 затронут GHSA-w5hq-g745-h8pq (CVE-2026-41907, CVE-2026-41988)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/uuid@9.0.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-w5hq-g745-h8pq (CVE-2026-41907, CVE-2026-41988) для пакета npm uuid версии 9.0.0: uuid: Missing buffer bounds check in v3/v5/v6 when buf is provided. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w5hq-g745-h8pq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w5hq-g745-h8pq](https://osv.dev/vulnerability/GHSA-w5hq-g745-h8pq) · manifest · SHA-256 7bad665555315bb9d1a092179d7dc6dfbd531087a606bf3b7adbe68f189a1210_

```
{"id": "GHSA-w5hq-g745-h8pq", "aliases": ["CVE-2026-41907", "CVE-2026-41988"], "modified": "2026-09-10T03:51:03.663336650Z", "summary": "uuid: Missing buffer bounds check in v3/v5/v6 when buf is provided", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (11.1.1, 12.0.1, 13.0.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05634 — zod 4.4.3 затронут GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/zod@4.4.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404) для пакета npm zod версии 4.4.3: Zod can exhaust memory while validating oversized constrained collections. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mrhx-c7xc-m3w5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mrhx-c7xc-m3w5](https://osv.dev/vulnerability/GHSA-mrhx-c7xc-m3w5) · manifest · SHA-256 fbd5f5d9c08d5ea6e57797966cf6931e9dccbb3e46859554eba6ad6e73820f9d_

```
{"id": "GHSA-mrhx-c7xc-m3w5", "aliases": ["CVE-2023-54404"], "modified": "2026-10-23T18:30:09.376405885Z", "summary": "Zod can exhaust memory while validating oversized constrained collections", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.6.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05623 — Возможный секрет в коде src/utils/ga4.ts

- Серьёзность: **Высокая** · Классификация: Подтверждённая ошибка конфигурации · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `file:src/utils/ga4.ts`
- Источник данных: src/utils/ga4.ts
- Метод обнаружения: Сопоставление регулярных выражений с API конкретного языка.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 47.1 / 100
- CVSS v3.1: неприменимо

1 значений, похожих на секреты, типа generic_assignment (первое — строка 10). Значения замаскированы QSI.

**Возможные последствия.** Учётные данные в коде утекают через репозитории, сборки и журналы.

**Шаги воспроизведения.**

```
Откройте строка 10 в предоставленном файле src/utils/ga4.ts и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/utils/ga4.ts](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/utils/ga4.ts#L10) · line 10 · SHA-256 976f6122a523d26eccfd49eaf31224760000dbc5aac15980096c6a8a0fd0b28e_

```
   10 | const API_SECRET = '[REDACTED]';
```

**Ограничения проверки.** Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Перенесите секреты в менеджер секретов/окружение; замените раскрытые значения.

**Повторная проверка.** Повторно просканируйте код и проверьте места вызова из доказательства.

### QSI-2026-05636 — @babel/plugin-transform-modules-systemjs 7.29.0 затронут GHSA-fv7c-fp4j-7gwp (CVE-2026-44728)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@babel/plugin-transform-modules-systemjs@7.29.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 8.2 (`CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-fv7c-fp4j-7gwp (CVE-2026-44728) для пакета npm @babel/plugin-transform-modules-systemjs версии 7.29.0: @babel/plugin-transform-modules-systemjs generates arbitrary code when compiling malicious input. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-fv7c-fp4j-7gwp
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-fv7c-fp4j-7gwp](https://osv.dev/vulnerability/GHSA-fv7c-fp4j-7gwp) · line 963 · SHA-256 e3684d1cb03fd6fb3bd3a79d6225f3462943419778e3ab139a00af6895a3a642_

```
{"id": "GHSA-fv7c-fp4j-7gwp", "aliases": ["CVE-2026-44728"], "modified": "2026-09-10T03:51:05.541786109Z", "summary": "@babel/plugin-transform-modules-systemjs generates arbitrary code when compiling malicious input", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:C/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.29.4, 8.0.0-alpha.13).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05638 — @openzeppelin/contracts 3.4.1-solc-0.7-2 затронут GHSA-88g8-f5mf-f5rj (CVE-2021-46320, CVE-2022-39384, GHSA-9c22-pwxw-p6hx)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@3.4.1-solc-0.7-2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-88g8-f5mf-f5rj (CVE-2021-46320, CVE-2022-39384, GHSA-9c22-pwxw-p6hx) для пакета npm @openzeppelin/contracts версии 3.4.1-solc-0.7-2: Improper Initialization in OpenZeppelin. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-88g8-f5mf-f5rj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-88g8-f5mf-f5rj](https://osv.dev/vulnerability/GHSA-88g8-f5mf-f5rj) · line 4591 · SHA-256 424d83524bb180962c4ae83693152d5b7cee3ef0f57c4ddba99ac5e747ea4156_

```
{"id": "GHSA-88g8-f5mf-f5rj", "aliases": ["CVE-2021-46320", "CVE-2022-39384", "GHSA-9c22-pwxw-p6hx"], "modified": "2026-07-16T03:56:17.546633851Z", "summary": "Improper Initialization in OpenZeppelin", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.4.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05642 — @openzeppelin/contracts 3.4.2-solc-0.7 затронут GHSA-88g8-f5mf-f5rj (CVE-2021-46320, CVE-2022-39384, GHSA-9c22-pwxw-p6hx)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@3.4.2-solc-0.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-88g8-f5mf-f5rj (CVE-2021-46320, CVE-2022-39384, GHSA-9c22-pwxw-p6hx) для пакета npm @openzeppelin/contracts версии 3.4.2-solc-0.7: Improper Initialization in OpenZeppelin. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-88g8-f5mf-f5rj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-88g8-f5mf-f5rj](https://osv.dev/vulnerability/GHSA-88g8-f5mf-f5rj) · line 4598 · SHA-256 424d83524bb180962c4ae83693152d5b7cee3ef0f57c4ddba99ac5e747ea4156_

```
{"id": "GHSA-88g8-f5mf-f5rj", "aliases": ["CVE-2021-46320", "CVE-2022-39384", "GHSA-9c22-pwxw-p6hx"], "modified": "2026-07-16T03:56:17.546633851Z", "summary": "Improper Initialization in OpenZeppelin", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.4.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05645 — @openzeppelin/contracts 4.7.0 затронут GHSA-4g63-c64m-25w9 (CVE-2022-31172)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@4.7.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-4g63-c64m-25w9 (CVE-2022-31172) для пакета npm @openzeppelin/contracts версии 4.7.0: OpenZeppelin Contracts's SignatureChecker may revert on invalid EIP-1271 signers. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4g63-c64m-25w9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4g63-c64m-25w9](https://osv.dev/vulnerability/GHSA-4g63-c64m-25w9) · line 4605 · SHA-256 29aa75a196197b2f8300eb288bf2ee90136c4178c6264f63e422d0e8cb2701ce_

```
{"id": "GHSA-4g63-c64m-25w9", "aliases": ["CVE-2022-31172"], "modified": "2023-11-08T04:09:28.648312Z", "summary": "OpenZeppelin Contracts's SignatureChecker may revert on invalid EIP-1271 signers", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.7.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05646 — @openzeppelin/contracts 4.7.0 затронут GHSA-4h98-2769-gh6h (CVE-2022-35961)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@4.7.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.9 (`CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:L`)

OSV.dev сообщает GHSA-4h98-2769-gh6h (CVE-2022-35961) для пакета npm @openzeppelin/contracts версии 4.7.0: OpenZeppelin Contracts vulnerable to ECDSA signature malleability. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4h98-2769-gh6h
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4h98-2769-gh6h](https://osv.dev/vulnerability/GHSA-4h98-2769-gh6h) · line 4605 · SHA-256 80269529aa3f0ff798923e81783db6bfaf14ab8954d1d470123be7717d0cd4ca_

```
{"id": "GHSA-4h98-2769-gh6h", "aliases": ["CVE-2022-35961"], "modified": "2023-11-08T04:09:54.445546Z", "summary": "OpenZeppelin Contracts vulnerable to ECDSA signature malleability", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.7.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05649 — @openzeppelin/contracts 4.7.0 затронут GHSA-93hq-5wgc-jc82 (CVE-2023-30542)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@4.7.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 8.8 (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-93hq-5wgc-jc82 (CVE-2023-30542) для пакета npm @openzeppelin/contracts версии 4.7.0: GovernorCompatibilityBravo may trim proposal calldata. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-93hq-5wgc-jc82
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-93hq-5wgc-jc82](https://osv.dev/vulnerability/GHSA-93hq-5wgc-jc82) · line 4605 · SHA-256 dd086cfb78aaf307e9c6d54e1860cc0468e4ebcbf35efb8a93dfba83346fd779_

```
{"id": "GHSA-93hq-5wgc-jc82", "aliases": ["CVE-2023-30542"], "modified": "2023-11-08T04:12:24.945774Z", "summary": "GovernorCompatibilityBravo may trim proposal calldata", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.8.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05654 — @openzeppelin/contracts 4.7.0 затронут GHSA-qh9x-gcfh-pcrw (CVE-2022-31170)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@4.7.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-qh9x-gcfh-pcrw (CVE-2022-31170) для пакета npm @openzeppelin/contracts версии 4.7.0: OpenZeppelin Contracts's ERC165Checker may revert instead of returning false. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qh9x-gcfh-pcrw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qh9x-gcfh-pcrw](https://osv.dev/vulnerability/GHSA-qh9x-gcfh-pcrw) · line 4605 · SHA-256 7560449cfe59b3e79c113b73d85babbf102d53fa851d8a485f87da238b3bd2f1_

```
{"id": "GHSA-qh9x-gcfh-pcrw", "aliases": ["CVE-2022-31170"], "modified": "2023-11-08T04:09:28.586055Z", "summary": "OpenZeppelin Contracts's ERC165Checker may revert instead of returning false", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.7.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05656 — @openzeppelin/contracts 4.7.0 затронут GHSA-xrc4-737v-9q75 (CVE-2022-31198)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@4.7.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-xrc4-737v-9q75 (CVE-2022-31198) для пакета npm @openzeppelin/contracts версии 4.7.0: OpenZeppelin Contracts's GovernorVotesQuorumFraction updates to quorum may affect past defeated proposals. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xrc4-737v-9q75
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xrc4-737v-9q75](https://osv.dev/vulnerability/GHSA-xrc4-737v-9q75) · line 4605 · SHA-256 b299085071cdc194deb1789b3b6c665e600905c3c1a6828f5f98ae3aae807174_

```
{"id": "GHSA-xrc4-737v-9q75", "aliases": ["CVE-2022-31198"], "modified": "2023-11-08T04:09:29.869695Z", "summary": "OpenZeppelin Contracts's GovernorVotesQuorumFraction updates to quorum may affect past defeated proposals", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.7.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05659 — axios 0.24.0 затронут GHSA-3g43-6gmg-66jw (CVE-2026-44495)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.0 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L`)

OSV.dev сообщает GHSA-3g43-6gmg-66jw (CVE-2026-44495) для пакета npm axios версии 0.24.0: axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3g43-6gmg-66jw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3g43-6gmg-66jw](https://osv.dev/vulnerability/GHSA-3g43-6gmg-66jw) · line 9733 · SHA-256 a6909e3523dbd0cc52c03f153847345a88a10ad7d6f44e8f7efaa4f0aaf05860_

```
{"id": "GHSA-3g43-6gmg-66jw", "aliases": ["CVE-2026-44495"], "modified": "2026-09-10T03:51:04.440180855Z", "summary": "axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05661 — axios 0.24.0 затронут GHSA-43fc-jf86-j433 (CVE-2026-25639)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-43fc-jf86-j433 (CVE-2026-25639) для пакета npm axios версии 0.24.0: Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-43fc-jf86-j433
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-43fc-jf86-j433](https://osv.dev/vulnerability/GHSA-43fc-jf86-j433) · line 9733 · SHA-256 fc80959fa45823eca99f8a4333940fcdf72894ce183ddffe5ade2efb70c0ba9d_

```
{"id": "GHSA-43fc-jf86-j433", "aliases": ["CVE-2026-25639"], "modified": "2026-09-10T03:50:34.100599628Z", "summary": "Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.30.3, 1.13.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05663 — axios 0.24.0 затронут GHSA-62hf-57xw-28j9 (CVE-2026-42039)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-62hf-57xw-28j9 (CVE-2026-42039) для пакета npm axios версии 0.24.0: Axios: unbounded recursion in toFormData causes DoS via deeply nested request data. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-62hf-57xw-28j9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-62hf-57xw-28j9](https://osv.dev/vulnerability/GHSA-62hf-57xw-28j9) · line 9733 · SHA-256 0a1ca526f6904a47d0d7d594ef69b73f96d14b1cdd90a07422cd9e65c494e13c_

```
{"id": "GHSA-62hf-57xw-28j9", "aliases": ["CVE-2026-42039"], "modified": "2026-09-10T03:50:45.703789635Z", "summary": "Axios: unbounded recursion in toFormData causes DoS via deeply nested request data", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05664 — axios 0.24.0 затронут GHSA-6chq-wfr3-2hj9 (CVE-2026-42035)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.4 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-6chq-wfr3-2hj9 (CVE-2026-42035) для пакета npm axios версии 0.24.0: Axios: Header Injection via Prototype Pollution. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6chq-wfr3-2hj9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-6chq-wfr3-2hj9](https://osv.dev/vulnerability/GHSA-6chq-wfr3-2hj9) · line 9733 · SHA-256 3c6cd4295abd8e612bd72548494dfc1aeddbc8cf7dff12939811a557df8955a3_

```
{"id": "GHSA-6chq-wfr3-2hj9", "aliases": ["CVE-2026-42035"], "modified": "2026-09-10T03:51:04.772235088Z", "summary": "Axios: Header Injection via Prototype Pollution", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05668 — axios 0.24.0 затронут GHSA-hfxv-24rg-xrqf (CVE-2026-44496)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496) для пакета npm axios версии 0.24.0: Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hfxv-24rg-xrqf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-hfxv-24rg-xrqf](https://osv.dev/vulnerability/GHSA-hfxv-24rg-xrqf) · line 9733 · SHA-256 96da8f038734a53dff48d2f1e59ee8f0d7e3d0f5d24ffe272caeee5d0cb7fd13_

```
{"id": "GHSA-hfxv-24rg-xrqf", "aliases": ["CVE-2026-44496"], "modified": "2026-09-10T03:50:49.732285826Z", "summary": "Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05669 — axios 0.24.0 затронут GHSA-j5f8-grm9-p9fc (CVE-2026-44486)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486) для пакета npm axios версии 0.24.0: Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j5f8-grm9-p9fc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j5f8-grm9-p9fc](https://osv.dev/vulnerability/GHSA-j5f8-grm9-p9fc) · line 9733 · SHA-256 e6778ca2fd5dd3478778c3fec3f8ed21e4a0f41329fb4dded8c779d04bd21ad2_

```
{"id": "GHSA-j5f8-grm9-p9fc", "aliases": ["CVE-2026-44486"], "modified": "2026-09-10T03:50:50.017253448Z", "summary": "Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05670 — axios 0.24.0 затронут GHSA-jr5f-v2jv-69x6 (CVE-2025-27152)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-jr5f-v2jv-69x6 (CVE-2025-27152) для пакета npm axios версии 0.24.0: axios Requests Vulnerable To Possible SSRF and Credential Leakage via Absolute URL. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-jr5f-v2jv-69x6
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-jr5f-v2jv-69x6](https://osv.dev/vulnerability/GHSA-jr5f-v2jv-69x6) · line 9733 · SHA-256 fba295b3957d5028e46b79609df20a0c34611cdb91f007367b15dc49ffb3f58e_

```
{"id": "GHSA-jr5f-v2jv-69x6", "aliases": ["CVE-2025-27152"], "modified": "2026-09-10T03:50:56.787685282Z", "summary": "axios Requests Vulnerable To Possible SSRF and Credential Leakage via Absolute URL", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.30.0, 1.8.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05673 — axios 0.24.0 затронут GHSA-p92q-9vqr-4j8v (CVE-2026-44487)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-p92q-9vqr-4j8v (CVE-2026-44487) для пакета npm axios версии 0.24.0: Axios: Proxy-Authorization Credential Leak to Origin Server Across HTTP-to-HTTPS Redirect in Axios Node.js HTTP Adapter. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-p92q-9vqr-4j8v
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-p92q-9vqr-4j8v](https://osv.dev/vulnerability/GHSA-p92q-9vqr-4j8v) · line 9733 · SHA-256 91165ac13ef2fa2e8e85f80ea8801353fca1cf1d2be5b9ccfb383583c4b1aa99_

```
{"id": "GHSA-p92q-9vqr-4j8v", "aliases": ["CVE-2026-44487"], "modified": "2026-09-10T03:51:09.218790313Z", "summary": "Axios: Proxy-Authorization Credential Leak to Origin Server Across HTTP-to-HTTPS Redirect in Axios Node.js HTTP Adapter", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05674 — axios 0.24.0 затронут GHSA-pf86-5x62-jrwf (CVE-2026-42033)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.4 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-pf86-5x62-jrwf (CVE-2026-42033) для пакета npm axios версии 0.24.0: Axios: Prototype Pollution Gadgets - Response Tampering, Data Exfiltration, and Request Hijacking. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pf86-5x62-jrwf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pf86-5x62-jrwf](https://osv.dev/vulnerability/GHSA-pf86-5x62-jrwf) · line 9733 · SHA-256 a44b8a78be68716ce0a71e307c6cd2d4a7a0311de2ce7d8866a32100e79c6a5b_

```
{"id": "GHSA-pf86-5x62-jrwf", "aliases": ["CVE-2026-42033"], "modified": "2026-09-10T03:51:06.658921258Z", "summary": "Axios: Prototype Pollution Gadgets - Response Tampering, Data Exfiltration, and Request Hijacking", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05675 — axios 0.24.0 затронут GHSA-pjwm-pj3p-43mv (CVE-2026-44492)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 8.6 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-pjwm-pj3p-43mv (CVE-2026-44492) для пакета npm axios версии 0.24.0: axios's shouldBypassProxy does not recognize IPv4-mapped IPv6 addresses, allowing NO_PROXY bypass (incomplete fix for CVE-2025-62718). Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pjwm-pj3p-43mv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pjwm-pj3p-43mv](https://osv.dev/vulnerability/GHSA-pjwm-pj3p-43mv) · line 9733 · SHA-256 df84ce1e471f6ac8550004d0227794d9eaa8f2dca0bcfbc45d9594e0837fdf1f_

```
{"id": "GHSA-pjwm-pj3p-43mv", "aliases": ["CVE-2026-44492"], "modified": "2026-09-10T03:51:06.693575938Z", "summary": "axios's shouldBypassProxy does not recognize IPv4-mapped IPv6 addresses, allowing NO_PROXY bypass (incomplete fix for CVE-2025-62718)", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05676 — axios 0.24.0 затронут GHSA-pmwg-cvhr-8vh7 (CVE-2026-42043)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.2 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-pmwg-cvhr-8vh7 (CVE-2026-42043) для пакета npm axios версии 0.24.0: Axios: Incomplete Fix for CVE-2025-62718 — NO_PROXY Protection Bypassed via RFC 1122 Loopback Subnet (127.0.0.0/8) in Axios 1.15.0. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pmwg-cvhr-8vh7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pmwg-cvhr-8vh7](https://osv.dev/vulnerability/GHSA-pmwg-cvhr-8vh7) · line 9733 · SHA-256 0b8f54404d99b3a73d924c3012e6c07f7c24dc001d4f40189c4e9fe81bde3566_

```
{"id": "GHSA-pmwg-cvhr-8vh7", "aliases": ["CVE-2026-42043"], "modified": "2026-09-10T03:51:06.691311805Z", "summary": "Axios: Incomplete Fix for CVE-2025-62718 — NO_PROXY Protection Bypassed via RFC 1122 Loopback Subnet (127.0.0.0/8) in Axios 1.15.0", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05679 — axios 1.12.2 затронут GHSA-35jp-ww65-95wh (CVE-2026-44494)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 8.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-35jp-ww65-95wh (CVE-2026-44494) для пакета npm axios версии 1.12.2: axios Vulnerable to Full Man-in-the-Middle via Prototype Pollution Gadget in `config.proxy`. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-35jp-ww65-95wh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-35jp-ww65-95wh](https://osv.dev/vulnerability/GHSA-35jp-ww65-95wh) · line 9742 · SHA-256 1a291e56e0ab3baa07377ca6700ff8aa08aabd97f6707876264f601526f3306a_

```
{"id": "GHSA-35jp-ww65-95wh", "aliases": ["CVE-2026-44494"], "modified": "2026-09-10T03:51:04.268287831Z", "summary": "axios Vulnerable to Full Man-in-the-Middle via Prototype Pollution Gadget in `config.proxy`", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05680 — axios 1.12.2 затронут GHSA-3g43-6gmg-66jw (CVE-2026-44495)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.0 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L`)

OSV.dev сообщает GHSA-3g43-6gmg-66jw (CVE-2026-44495) для пакета npm axios версии 1.12.2: axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3g43-6gmg-66jw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3g43-6gmg-66jw](https://osv.dev/vulnerability/GHSA-3g43-6gmg-66jw) · line 9742 · SHA-256 a6909e3523dbd0cc52c03f153847345a88a10ad7d6f44e8f7efaa4f0aaf05860_

```
{"id": "GHSA-3g43-6gmg-66jw", "aliases": ["CVE-2026-44495"], "modified": "2026-09-10T03:51:04.440180855Z", "summary": "axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05684 — axios 1.12.2 затронут GHSA-43fc-jf86-j433 (CVE-2026-25639)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-43fc-jf86-j433 (CVE-2026-25639) для пакета npm axios версии 1.12.2: Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-43fc-jf86-j433
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-43fc-jf86-j433](https://osv.dev/vulnerability/GHSA-43fc-jf86-j433) · line 9742 · SHA-256 fc80959fa45823eca99f8a4333940fcdf72894ce183ddffe5ade2efb70c0ba9d_

```
{"id": "GHSA-43fc-jf86-j433", "aliases": ["CVE-2026-25639"], "modified": "2026-09-10T03:50:34.100599628Z", "summary": "Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.30.3, 1.13.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05688 — axios 1.12.2 затронут GHSA-62hf-57xw-28j9 (CVE-2026-42039)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-62hf-57xw-28j9 (CVE-2026-42039) для пакета npm axios версии 1.12.2: Axios: unbounded recursion in toFormData causes DoS via deeply nested request data. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-62hf-57xw-28j9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-62hf-57xw-28j9](https://osv.dev/vulnerability/GHSA-62hf-57xw-28j9) · line 9742 · SHA-256 0a1ca526f6904a47d0d7d594ef69b73f96d14b1cdd90a07422cd9e65c494e13c_

```
{"id": "GHSA-62hf-57xw-28j9", "aliases": ["CVE-2026-42039"], "modified": "2026-09-10T03:50:45.703789635Z", "summary": "Axios: unbounded recursion in toFormData causes DoS via deeply nested request data", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05689 — axios 1.12.2 затронут GHSA-6chq-wfr3-2hj9 (CVE-2026-42035)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.4 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-6chq-wfr3-2hj9 (CVE-2026-42035) для пакета npm axios версии 1.12.2: Axios: Header Injection via Prototype Pollution. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6chq-wfr3-2hj9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-6chq-wfr3-2hj9](https://osv.dev/vulnerability/GHSA-6chq-wfr3-2hj9) · line 9742 · SHA-256 3c6cd4295abd8e612bd72548494dfc1aeddbc8cf7dff12939811a557df8955a3_

```
{"id": "GHSA-6chq-wfr3-2hj9", "aliases": ["CVE-2026-42035"], "modified": "2026-09-10T03:51:04.772235088Z", "summary": "Axios: Header Injection via Prototype Pollution", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05690 — axios 1.12.2 затронут GHSA-777c-7fjr-54vf (CVE-2026-44488)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-777c-7fjr-54vf (CVE-2026-44488) для пакета npm axios версии 1.12.2: Allocation of Resources Without Limits or Throttling in Axios. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-777c-7fjr-54vf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-777c-7fjr-54vf](https://osv.dev/vulnerability/GHSA-777c-7fjr-54vf) · line 9742 · SHA-256 126ffde4e7cfe5a708f3eff82e4b76624570096a5e2709f6ea0bcb61fa3d7cfa_

```
{"id": "GHSA-777c-7fjr-54vf", "aliases": ["CVE-2026-44488"], "modified": "2026-09-10T03:50:48.738717543Z", "summary": "Allocation of Resources Without Limits or Throttling in Axios", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05695 — axios 1.12.2 затронут GHSA-hfxv-24rg-xrqf (CVE-2026-44496)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496) для пакета npm axios версии 1.12.2: Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hfxv-24rg-xrqf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-hfxv-24rg-xrqf](https://osv.dev/vulnerability/GHSA-hfxv-24rg-xrqf) · line 9742 · SHA-256 96da8f038734a53dff48d2f1e59ee8f0d7e3d0f5d24ffe272caeee5d0cb7fd13_

```
{"id": "GHSA-hfxv-24rg-xrqf", "aliases": ["CVE-2026-44496"], "modified": "2026-09-10T03:50:49.732285826Z", "summary": "Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05696 — axios 1.12.2 затронут GHSA-j5f8-grm9-p9fc (CVE-2026-44486)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486) для пакета npm axios версии 1.12.2: Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j5f8-grm9-p9fc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j5f8-grm9-p9fc](https://osv.dev/vulnerability/GHSA-j5f8-grm9-p9fc) · line 9742 · SHA-256 e6778ca2fd5dd3478778c3fec3f8ed21e4a0f41329fb4dded8c779d04bd21ad2_

```
{"id": "GHSA-j5f8-grm9-p9fc", "aliases": ["CVE-2026-44486"], "modified": "2026-09-10T03:50:50.017253448Z", "summary": "Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05699 — axios 1.13.2 затронут GHSA-35jp-ww65-95wh (CVE-2026-44494)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 8.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-35jp-ww65-95wh (CVE-2026-44494) для пакета npm axios версии 1.13.2: axios Vulnerable to Full Man-in-the-Middle via Prototype Pollution Gadget in `config.proxy`. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-35jp-ww65-95wh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-35jp-ww65-95wh](https://osv.dev/vulnerability/GHSA-35jp-ww65-95wh) · line 9753 · SHA-256 1a291e56e0ab3baa07377ca6700ff8aa08aabd97f6707876264f601526f3306a_

```
{"id": "GHSA-35jp-ww65-95wh", "aliases": ["CVE-2026-44494"], "modified": "2026-09-10T03:51:04.268287831Z", "summary": "axios Vulnerable to Full Man-in-the-Middle via Prototype Pollution Gadget in `config.proxy`", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05700 — axios 1.13.2 затронут GHSA-3g43-6gmg-66jw (CVE-2026-44495)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.0 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L`)

OSV.dev сообщает GHSA-3g43-6gmg-66jw (CVE-2026-44495) для пакета npm axios версии 1.13.2: axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3g43-6gmg-66jw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3g43-6gmg-66jw](https://osv.dev/vulnerability/GHSA-3g43-6gmg-66jw) · line 9753 · SHA-256 a6909e3523dbd0cc52c03f153847345a88a10ad7d6f44e8f7efaa4f0aaf05860_

```
{"id": "GHSA-3g43-6gmg-66jw", "aliases": ["CVE-2026-44495"], "modified": "2026-09-10T03:51:04.440180855Z", "summary": "axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05702 — axios 1.13.2 затронут GHSA-3pq3-5fj3-cg6v (CVE-2026-101898)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3pq3-5fj3-cg6v (CVE-2026-101898) для пакета npm axios версии 1.13.2: Axios: HTTP/2 adapter bypasses configured DNS lookup and proxy controls. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3pq3-5fj3-cg6v
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3pq3-5fj3-cg6v](https://osv.dev/vulnerability/GHSA-3pq3-5fj3-cg6v) · line 9753 · SHA-256 4c00ee167865398091112c9a691df4d5d62106cad9bc28ac851187d2b29538c9_

```
{"id": "GHSA-3pq3-5fj3-cg6v", "aliases": ["CVE-2026-101898"], "modified": "2026-09-30T15:15:04.067807024Z", "summary": "Axios: HTTP/2 adapter bypasses configured DNS lookup and proxy controls", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05705 — axios 1.13.2 затронут GHSA-43fc-jf86-j433 (CVE-2026-25639)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-43fc-jf86-j433 (CVE-2026-25639) для пакета npm axios версии 1.13.2: Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-43fc-jf86-j433
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-43fc-jf86-j433](https://osv.dev/vulnerability/GHSA-43fc-jf86-j433) · line 9753 · SHA-256 fc80959fa45823eca99f8a4333940fcdf72894ce183ddffe5ade2efb70c0ba9d_

```
{"id": "GHSA-43fc-jf86-j433", "aliases": ["CVE-2026-25639"], "modified": "2026-09-10T03:50:34.100599628Z", "summary": "Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.30.3, 1.13.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05708 — axios 1.13.2 затронут GHSA-542g-h47m-68v8 (CVE-2026-101901)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-542g-h47m-68v8 (CVE-2026-101901) для пакета npm axios версии 1.13.2: Axios: Denial of Service via Unhandled 'error' Event in HTTP/2 ClientHttp2Session Initialization. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-542g-h47m-68v8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-542g-h47m-68v8](https://osv.dev/vulnerability/GHSA-542g-h47m-68v8) · line 9753 · SHA-256 dbaea426f5b3d75e8930f3b5e8fd416a139536224cb1fa380dde0f4c4ae62d33_

```
{"id": "GHSA-542g-h47m-68v8", "aliases": ["CVE-2026-101901"], "modified": "2026-09-30T15:15:04.061469672Z", "summary": "Axios: Denial of Service via Unhandled 'error' Event in HTTP/2 ClientHttp2Session Initialization", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05710 — axios 1.13.2 затронут GHSA-62hf-57xw-28j9 (CVE-2026-42039)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-62hf-57xw-28j9 (CVE-2026-42039) для пакета npm axios версии 1.13.2: Axios: unbounded recursion in toFormData causes DoS via deeply nested request data. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-62hf-57xw-28j9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-62hf-57xw-28j9](https://osv.dev/vulnerability/GHSA-62hf-57xw-28j9) · line 9753 · SHA-256 0a1ca526f6904a47d0d7d594ef69b73f96d14b1cdd90a07422cd9e65c494e13c_

```
{"id": "GHSA-62hf-57xw-28j9", "aliases": ["CVE-2026-42039"], "modified": "2026-09-10T03:50:45.703789635Z", "summary": "Axios: unbounded recursion in toFormData causes DoS via deeply nested request data", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05711 — axios 1.13.2 затронут GHSA-6chq-wfr3-2hj9 (CVE-2026-42035)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.4 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-6chq-wfr3-2hj9 (CVE-2026-42035) для пакета npm axios версии 1.13.2: Axios: Header Injection via Prototype Pollution. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6chq-wfr3-2hj9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-6chq-wfr3-2hj9](https://osv.dev/vulnerability/GHSA-6chq-wfr3-2hj9) · line 9753 · SHA-256 3c6cd4295abd8e612bd72548494dfc1aeddbc8cf7dff12939811a557df8955a3_

```
{"id": "GHSA-6chq-wfr3-2hj9", "aliases": ["CVE-2026-42035"], "modified": "2026-09-10T03:51:04.772235088Z", "summary": "Axios: Header Injection via Prototype Pollution", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05712 — axios 1.13.2 затронут GHSA-777c-7fjr-54vf (CVE-2026-44488)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-777c-7fjr-54vf (CVE-2026-44488) для пакета npm axios версии 1.13.2: Allocation of Resources Without Limits or Throttling in Axios. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-777c-7fjr-54vf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-777c-7fjr-54vf](https://osv.dev/vulnerability/GHSA-777c-7fjr-54vf) · line 9753 · SHA-256 126ffde4e7cfe5a708f3eff82e4b76624570096a5e2709f6ea0bcb61fa3d7cfa_

```
{"id": "GHSA-777c-7fjr-54vf", "aliases": ["CVE-2026-44488"], "modified": "2026-09-10T03:50:48.738717543Z", "summary": "Allocation of Resources Without Limits or Throttling in Axios", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05717 — axios 1.13.2 затронут GHSA-hfxv-24rg-xrqf (CVE-2026-44496)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496) для пакета npm axios версии 1.13.2: Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hfxv-24rg-xrqf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-hfxv-24rg-xrqf](https://osv.dev/vulnerability/GHSA-hfxv-24rg-xrqf) · line 9753 · SHA-256 96da8f038734a53dff48d2f1e59ee8f0d7e3d0f5d24ffe272caeee5d0cb7fd13_

```
{"id": "GHSA-hfxv-24rg-xrqf", "aliases": ["CVE-2026-44496"], "modified": "2026-09-10T03:50:49.732285826Z", "summary": "Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05718 — axios 1.13.2 затронут GHSA-j5f8-grm9-p9fc (CVE-2026-44486)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486) для пакета npm axios версии 1.13.2: Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j5f8-grm9-p9fc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j5f8-grm9-p9fc](https://osv.dev/vulnerability/GHSA-j5f8-grm9-p9fc) · line 9753 · SHA-256 e6778ca2fd5dd3478778c3fec3f8ed21e4a0f41329fb4dded8c779d04bd21ad2_

```
{"id": "GHSA-j5f8-grm9-p9fc", "aliases": ["CVE-2026-44486"], "modified": "2026-09-10T03:50:50.017253448Z", "summary": "Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05719 — axios 1.15.2 затронут GHSA-35jp-ww65-95wh (CVE-2026-44494)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 8.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-35jp-ww65-95wh (CVE-2026-44494) для пакета npm axios версии 1.15.2: axios Vulnerable to Full Man-in-the-Middle via Prototype Pollution Gadget in `config.proxy`. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-35jp-ww65-95wh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-35jp-ww65-95wh](https://osv.dev/vulnerability/GHSA-35jp-ww65-95wh) · line 9764 · SHA-256 1a291e56e0ab3baa07377ca6700ff8aa08aabd97f6707876264f601526f3306a_

```
{"id": "GHSA-35jp-ww65-95wh", "aliases": ["CVE-2026-44494"], "modified": "2026-09-10T03:51:04.268287831Z", "summary": "axios Vulnerable to Full Man-in-the-Middle via Prototype Pollution Gadget in `config.proxy`", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05720 — axios 1.15.2 затронут GHSA-3pq3-5fj3-cg6v (CVE-2026-101898)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3pq3-5fj3-cg6v (CVE-2026-101898) для пакета npm axios версии 1.15.2: Axios: HTTP/2 adapter bypasses configured DNS lookup and proxy controls. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3pq3-5fj3-cg6v
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3pq3-5fj3-cg6v](https://osv.dev/vulnerability/GHSA-3pq3-5fj3-cg6v) · line 9764 · SHA-256 4c00ee167865398091112c9a691df4d5d62106cad9bc28ac851187d2b29538c9_

```
{"id": "GHSA-3pq3-5fj3-cg6v", "aliases": ["CVE-2026-101898"], "modified": "2026-09-30T15:15:04.067807024Z", "summary": "Axios: HTTP/2 adapter bypasses configured DNS lookup and proxy controls", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05724 — axios 1.15.2 затронут GHSA-542g-h47m-68v8 (CVE-2026-101901)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-542g-h47m-68v8 (CVE-2026-101901) для пакета npm axios версии 1.15.2: Axios: Denial of Service via Unhandled 'error' Event in HTTP/2 ClientHttp2Session Initialization. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-542g-h47m-68v8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-542g-h47m-68v8](https://osv.dev/vulnerability/GHSA-542g-h47m-68v8) · line 9764 · SHA-256 dbaea426f5b3d75e8930f3b5e8fd416a139536224cb1fa380dde0f4c4ae62d33_

```
{"id": "GHSA-542g-h47m-68v8", "aliases": ["CVE-2026-101901"], "modified": "2026-09-30T15:15:04.061469672Z", "summary": "Axios: Denial of Service via Unhandled 'error' Event in HTTP/2 ClientHttp2Session Initialization", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05726 — axios 1.15.2 затронут GHSA-777c-7fjr-54vf (CVE-2026-44488)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-777c-7fjr-54vf (CVE-2026-44488) для пакета npm axios версии 1.15.2: Allocation of Resources Without Limits or Throttling in Axios. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-777c-7fjr-54vf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-777c-7fjr-54vf](https://osv.dev/vulnerability/GHSA-777c-7fjr-54vf) · line 9764 · SHA-256 126ffde4e7cfe5a708f3eff82e4b76624570096a5e2709f6ea0bcb61fa3d7cfa_

```
{"id": "GHSA-777c-7fjr-54vf", "aliases": ["CVE-2026-44488"], "modified": "2026-09-10T03:50:48.738717543Z", "summary": "Allocation of Resources Without Limits or Throttling in Axios", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05731 — axios 1.15.2 затронут GHSA-gcfj-64vw-6mp9 (CVE-2026-67320)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-gcfj-64vw-6mp9 (CVE-2026-67320) для пакета npm axios версии 1.15.2: Axios Node HTTP adapter can use an inherited proxy after interceptor config cloning. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-gcfj-64vw-6mp9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-gcfj-64vw-6mp9](https://osv.dev/vulnerability/GHSA-gcfj-64vw-6mp9) · line 9764 · SHA-256 8d26fc7811fe887857bd374955222a4dcb208a6336606c49b6bf8e2196a333b4_

```
{"id": "GHSA-gcfj-64vw-6mp9", "aliases": ["CVE-2026-67320"], "modified": "2026-09-10T03:50:52.061533850Z", "summary": "Axios Node HTTP adapter can use an inherited proxy after interceptor config cloning", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05733 — axios 1.15.2 затронут GHSA-hfxv-24rg-xrqf (CVE-2026-44496)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496) для пакета npm axios версии 1.15.2: Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hfxv-24rg-xrqf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-hfxv-24rg-xrqf](https://osv.dev/vulnerability/GHSA-hfxv-24rg-xrqf) · line 9764 · SHA-256 96da8f038734a53dff48d2f1e59ee8f0d7e3d0f5d24ffe272caeee5d0cb7fd13_

```
{"id": "GHSA-hfxv-24rg-xrqf", "aliases": ["CVE-2026-44496"], "modified": "2026-09-10T03:50:49.732285826Z", "summary": "Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05734 — axios 1.15.2 затронут GHSA-j5f8-grm9-p9fc (CVE-2026-44486)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486) для пакета npm axios версии 1.15.2: Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j5f8-grm9-p9fc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j5f8-grm9-p9fc](https://osv.dev/vulnerability/GHSA-j5f8-grm9-p9fc) · line 9764 · SHA-256 e6778ca2fd5dd3478778c3fec3f8ed21e4a0f41329fb4dded8c779d04bd21ad2_

```
{"id": "GHSA-j5f8-grm9-p9fc", "aliases": ["CVE-2026-44486"], "modified": "2026-09-10T03:50:50.017253448Z", "summary": "Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05737 — axios 1.15.2 затронут GHSA-m8m8-qj5v-23w3 (CVE-2026-101905)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-m8m8-qj5v-23w3 (CVE-2026-101905) для пакета npm axios версии 1.15.2: Axios: Node HTTP adapter prototype-pollution gadget allows request socket hijack via inherited createConnection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-m8m8-qj5v-23w3
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-m8m8-qj5v-23w3](https://osv.dev/vulnerability/GHSA-m8m8-qj5v-23w3) · line 9764 · SHA-256 6d824e2d6a9c2d6bf6397f21f8d755ad8eaa2aa30e715cc5d35d1c8886a64c5a_

```
{"id": "GHSA-m8m8-qj5v-23w3", "aliases": ["CVE-2026-101905"], "modified": "2026-09-30T15:46:18.253717573Z", "summary": "Axios: Node HTTP adapter prototype-pollution gadget allows request socket hijack via inherited createConnection", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:L/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05738 — axios 1.15.2 затронут GHSA-mghh-pgcx-3jjj (CVE-2026-101906)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-mghh-pgcx-3jjj (CVE-2026-101906) для пакета npm axios версии 1.15.2: Axios: ReDoS (O(N²)) in shouldBypassProxy host normalization, reachable via untrusted redirect Location. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mghh-pgcx-3jjj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mghh-pgcx-3jjj](https://osv.dev/vulnerability/GHSA-mghh-pgcx-3jjj) · line 9764 · SHA-256 a5a1fb599f58ee42aec987735742bb8295fbf86e39efb50e5cf2261e48964be7_

```
{"id": "GHSA-mghh-pgcx-3jjj", "aliases": ["CVE-2026-101906"], "modified": "2026-09-30T15:15:04.048176303Z", "summary": "Axios: ReDoS (O(N²)) in shouldBypassProxy host normalization, reachable via untrusted redirect Location", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05739 — axios 0.21.4 затронут GHSA-3g43-6gmg-66jw (CVE-2026-44495)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.0 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L`)

OSV.dev сообщает GHSA-3g43-6gmg-66jw (CVE-2026-44495) для пакета npm axios версии 0.21.4: axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3g43-6gmg-66jw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3g43-6gmg-66jw](https://osv.dev/vulnerability/GHSA-3g43-6gmg-66jw) · line 9775 · SHA-256 a6909e3523dbd0cc52c03f153847345a88a10ad7d6f44e8f7efaa4f0aaf05860_

```
{"id": "GHSA-3g43-6gmg-66jw", "aliases": ["CVE-2026-44495"], "modified": "2026-09-10T03:51:04.440180855Z", "summary": "axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05741 — axios 0.21.4 затронут GHSA-43fc-jf86-j433 (CVE-2026-25639)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-43fc-jf86-j433 (CVE-2026-25639) для пакета npm axios версии 0.21.4: Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-43fc-jf86-j433
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-43fc-jf86-j433](https://osv.dev/vulnerability/GHSA-43fc-jf86-j433) · line 9775 · SHA-256 fc80959fa45823eca99f8a4333940fcdf72894ce183ddffe5ade2efb70c0ba9d_

```
{"id": "GHSA-43fc-jf86-j433", "aliases": ["CVE-2026-25639"], "modified": "2026-09-10T03:50:34.100599628Z", "summary": "Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.30.3, 1.13.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05743 — axios 0.21.4 затронут GHSA-62hf-57xw-28j9 (CVE-2026-42039)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-62hf-57xw-28j9 (CVE-2026-42039) для пакета npm axios версии 0.21.4: Axios: unbounded recursion in toFormData causes DoS via deeply nested request data. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-62hf-57xw-28j9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-62hf-57xw-28j9](https://osv.dev/vulnerability/GHSA-62hf-57xw-28j9) · line 9775 · SHA-256 0a1ca526f6904a47d0d7d594ef69b73f96d14b1cdd90a07422cd9e65c494e13c_

```
{"id": "GHSA-62hf-57xw-28j9", "aliases": ["CVE-2026-42039"], "modified": "2026-09-10T03:50:45.703789635Z", "summary": "Axios: unbounded recursion in toFormData causes DoS via deeply nested request data", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05744 — axios 0.21.4 затронут GHSA-6chq-wfr3-2hj9 (CVE-2026-42035)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.4 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-6chq-wfr3-2hj9 (CVE-2026-42035) для пакета npm axios версии 0.21.4: Axios: Header Injection via Prototype Pollution. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6chq-wfr3-2hj9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-6chq-wfr3-2hj9](https://osv.dev/vulnerability/GHSA-6chq-wfr3-2hj9) · line 9775 · SHA-256 3c6cd4295abd8e612bd72548494dfc1aeddbc8cf7dff12939811a557df8955a3_

```
{"id": "GHSA-6chq-wfr3-2hj9", "aliases": ["CVE-2026-42035"], "modified": "2026-09-10T03:51:04.772235088Z", "summary": "Axios: Header Injection via Prototype Pollution", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05748 — axios 0.21.4 затронут GHSA-hfxv-24rg-xrqf (CVE-2026-44496)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496) для пакета npm axios версии 0.21.4: Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hfxv-24rg-xrqf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-hfxv-24rg-xrqf](https://osv.dev/vulnerability/GHSA-hfxv-24rg-xrqf) · line 9775 · SHA-256 96da8f038734a53dff48d2f1e59ee8f0d7e3d0f5d24ffe272caeee5d0cb7fd13_

```
{"id": "GHSA-hfxv-24rg-xrqf", "aliases": ["CVE-2026-44496"], "modified": "2026-09-10T03:50:49.732285826Z", "summary": "Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05749 — axios 0.21.4 затронут GHSA-j5f8-grm9-p9fc (CVE-2026-44486)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486) для пакета npm axios версии 0.21.4: Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j5f8-grm9-p9fc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j5f8-grm9-p9fc](https://osv.dev/vulnerability/GHSA-j5f8-grm9-p9fc) · line 9775 · SHA-256 e6778ca2fd5dd3478778c3fec3f8ed21e4a0f41329fb4dded8c779d04bd21ad2_

```
{"id": "GHSA-j5f8-grm9-p9fc", "aliases": ["CVE-2026-44486"], "modified": "2026-09-10T03:50:50.017253448Z", "summary": "Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05750 — axios 0.21.4 затронут GHSA-jr5f-v2jv-69x6 (CVE-2025-27152)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-jr5f-v2jv-69x6 (CVE-2025-27152) для пакета npm axios версии 0.21.4: axios Requests Vulnerable To Possible SSRF and Credential Leakage via Absolute URL. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-jr5f-v2jv-69x6
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-jr5f-v2jv-69x6](https://osv.dev/vulnerability/GHSA-jr5f-v2jv-69x6) · line 9775 · SHA-256 fba295b3957d5028e46b79609df20a0c34611cdb91f007367b15dc49ffb3f58e_

```
{"id": "GHSA-jr5f-v2jv-69x6", "aliases": ["CVE-2025-27152"], "modified": "2026-09-10T03:50:56.787685282Z", "summary": "axios Requests Vulnerable To Possible SSRF and Credential Leakage via Absolute URL", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.30.0, 1.8.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05753 — axios 0.21.4 затронут GHSA-p92q-9vqr-4j8v (CVE-2026-44487)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-p92q-9vqr-4j8v (CVE-2026-44487) для пакета npm axios версии 0.21.4: Axios: Proxy-Authorization Credential Leak to Origin Server Across HTTP-to-HTTPS Redirect in Axios Node.js HTTP Adapter. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-p92q-9vqr-4j8v
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-p92q-9vqr-4j8v](https://osv.dev/vulnerability/GHSA-p92q-9vqr-4j8v) · line 9775 · SHA-256 91165ac13ef2fa2e8e85f80ea8801353fca1cf1d2be5b9ccfb383583c4b1aa99_

```
{"id": "GHSA-p92q-9vqr-4j8v", "aliases": ["CVE-2026-44487"], "modified": "2026-09-10T03:51:09.218790313Z", "summary": "Axios: Proxy-Authorization Credential Leak to Origin Server Across HTTP-to-HTTPS Redirect in Axios Node.js HTTP Adapter", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05754 — axios 0.21.4 затронут GHSA-pf86-5x62-jrwf (CVE-2026-42033)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.4 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-pf86-5x62-jrwf (CVE-2026-42033) для пакета npm axios версии 0.21.4: Axios: Prototype Pollution Gadgets - Response Tampering, Data Exfiltration, and Request Hijacking. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pf86-5x62-jrwf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pf86-5x62-jrwf](https://osv.dev/vulnerability/GHSA-pf86-5x62-jrwf) · line 9775 · SHA-256 a44b8a78be68716ce0a71e307c6cd2d4a7a0311de2ce7d8866a32100e79c6a5b_

```
{"id": "GHSA-pf86-5x62-jrwf", "aliases": ["CVE-2026-42033"], "modified": "2026-09-10T03:51:06.658921258Z", "summary": "Axios: Prototype Pollution Gadgets - Response Tampering, Data Exfiltration, and Request Hijacking", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05755 — axios 0.21.4 затронут GHSA-pjwm-pj3p-43mv (CVE-2026-44492)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 8.6 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-pjwm-pj3p-43mv (CVE-2026-44492) для пакета npm axios версии 0.21.4: axios's shouldBypassProxy does not recognize IPv4-mapped IPv6 addresses, allowing NO_PROXY bypass (incomplete fix for CVE-2025-62718). Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pjwm-pj3p-43mv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pjwm-pj3p-43mv](https://osv.dev/vulnerability/GHSA-pjwm-pj3p-43mv) · line 9775 · SHA-256 df84ce1e471f6ac8550004d0227794d9eaa8f2dca0bcfbc45d9594e0837fdf1f_

```
{"id": "GHSA-pjwm-pj3p-43mv", "aliases": ["CVE-2026-44492"], "modified": "2026-09-10T03:51:06.693575938Z", "summary": "axios's shouldBypassProxy does not recognize IPv4-mapped IPv6 addresses, allowing NO_PROXY bypass (incomplete fix for CVE-2025-62718)", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05756 — axios 0.21.4 затронут GHSA-pmwg-cvhr-8vh7 (CVE-2026-42043)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.2 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-pmwg-cvhr-8vh7 (CVE-2026-42043) для пакета npm axios версии 0.21.4: Axios: Incomplete Fix for CVE-2025-62718 — NO_PROXY Protection Bypassed via RFC 1122 Loopback Subnet (127.0.0.0/8) in Axios 1.15.0. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pmwg-cvhr-8vh7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pmwg-cvhr-8vh7](https://osv.dev/vulnerability/GHSA-pmwg-cvhr-8vh7) · line 9775 · SHA-256 0b8f54404d99b3a73d924c3012e6c07f7c24dc001d4f40189c4e9fe81bde3566_

```
{"id": "GHSA-pmwg-cvhr-8vh7", "aliases": ["CVE-2026-42043"], "modified": "2026-09-10T03:51:06.691311805Z", "summary": "Axios: Incomplete Fix for CVE-2025-62718 — NO_PROXY Protection Bypassed via RFC 1122 Loopback Subnet (127.0.0.0/8) in Axios 1.15.0", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05759 — axios 0.27.2 затронут GHSA-3g43-6gmg-66jw (CVE-2026-44495)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.0 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L`)

OSV.dev сообщает GHSA-3g43-6gmg-66jw (CVE-2026-44495) для пакета npm axios версии 0.27.2: axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3g43-6gmg-66jw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3g43-6gmg-66jw](https://osv.dev/vulnerability/GHSA-3g43-6gmg-66jw) · line 9784 · SHA-256 a6909e3523dbd0cc52c03f153847345a88a10ad7d6f44e8f7efaa4f0aaf05860_

```
{"id": "GHSA-3g43-6gmg-66jw", "aliases": ["CVE-2026-44495"], "modified": "2026-09-10T03:51:04.440180855Z", "summary": "axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05761 — axios 0.27.2 затронут GHSA-43fc-jf86-j433 (CVE-2026-25639)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-43fc-jf86-j433 (CVE-2026-25639) для пакета npm axios версии 0.27.2: Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-43fc-jf86-j433
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-43fc-jf86-j433](https://osv.dev/vulnerability/GHSA-43fc-jf86-j433) · line 9784 · SHA-256 fc80959fa45823eca99f8a4333940fcdf72894ce183ddffe5ade2efb70c0ba9d_

```
{"id": "GHSA-43fc-jf86-j433", "aliases": ["CVE-2026-25639"], "modified": "2026-09-10T03:50:34.100599628Z", "summary": "Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.30.3, 1.13.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05763 — axios 0.27.2 затронут GHSA-62hf-57xw-28j9 (CVE-2026-42039)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-62hf-57xw-28j9 (CVE-2026-42039) для пакета npm axios версии 0.27.2: Axios: unbounded recursion in toFormData causes DoS via deeply nested request data. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-62hf-57xw-28j9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-62hf-57xw-28j9](https://osv.dev/vulnerability/GHSA-62hf-57xw-28j9) · line 9784 · SHA-256 0a1ca526f6904a47d0d7d594ef69b73f96d14b1cdd90a07422cd9e65c494e13c_

```
{"id": "GHSA-62hf-57xw-28j9", "aliases": ["CVE-2026-42039"], "modified": "2026-09-10T03:50:45.703789635Z", "summary": "Axios: unbounded recursion in toFormData causes DoS via deeply nested request data", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05764 — axios 0.27.2 затронут GHSA-6chq-wfr3-2hj9 (CVE-2026-42035)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.4 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-6chq-wfr3-2hj9 (CVE-2026-42035) для пакета npm axios версии 0.27.2: Axios: Header Injection via Prototype Pollution. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6chq-wfr3-2hj9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-6chq-wfr3-2hj9](https://osv.dev/vulnerability/GHSA-6chq-wfr3-2hj9) · line 9784 · SHA-256 3c6cd4295abd8e612bd72548494dfc1aeddbc8cf7dff12939811a557df8955a3_

```
{"id": "GHSA-6chq-wfr3-2hj9", "aliases": ["CVE-2026-42035"], "modified": "2026-09-10T03:51:04.772235088Z", "summary": "Axios: Header Injection via Prototype Pollution", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05769 — axios 0.27.2 затронут GHSA-hfxv-24rg-xrqf (CVE-2026-44496)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496) для пакета npm axios версии 0.27.2: Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hfxv-24rg-xrqf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-hfxv-24rg-xrqf](https://osv.dev/vulnerability/GHSA-hfxv-24rg-xrqf) · line 9784 · SHA-256 96da8f038734a53dff48d2f1e59ee8f0d7e3d0f5d24ffe272caeee5d0cb7fd13_

```
{"id": "GHSA-hfxv-24rg-xrqf", "aliases": ["CVE-2026-44496"], "modified": "2026-09-10T03:50:49.732285826Z", "summary": "Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05770 — axios 0.27.2 затронут GHSA-j5f8-grm9-p9fc (CVE-2026-44486)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486) для пакета npm axios версии 0.27.2: Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j5f8-grm9-p9fc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j5f8-grm9-p9fc](https://osv.dev/vulnerability/GHSA-j5f8-grm9-p9fc) · line 9784 · SHA-256 e6778ca2fd5dd3478778c3fec3f8ed21e4a0f41329fb4dded8c779d04bd21ad2_

```
{"id": "GHSA-j5f8-grm9-p9fc", "aliases": ["CVE-2026-44486"], "modified": "2026-09-10T03:50:50.017253448Z", "summary": "Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05771 — axios 0.27.2 затронут GHSA-jr5f-v2jv-69x6 (CVE-2025-27152)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-jr5f-v2jv-69x6 (CVE-2025-27152) для пакета npm axios версии 0.27.2: axios Requests Vulnerable To Possible SSRF and Credential Leakage via Absolute URL. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-jr5f-v2jv-69x6
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-jr5f-v2jv-69x6](https://osv.dev/vulnerability/GHSA-jr5f-v2jv-69x6) · line 9784 · SHA-256 fba295b3957d5028e46b79609df20a0c34611cdb91f007367b15dc49ffb3f58e_

```
{"id": "GHSA-jr5f-v2jv-69x6", "aliases": ["CVE-2025-27152"], "modified": "2026-09-10T03:50:56.787685282Z", "summary": "axios Requests Vulnerable To Possible SSRF and Credential Leakage via Absolute URL", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.30.0, 1.8.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05774 — axios 0.27.2 затронут GHSA-p92q-9vqr-4j8v (CVE-2026-44487)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-p92q-9vqr-4j8v (CVE-2026-44487) для пакета npm axios версии 0.27.2: Axios: Proxy-Authorization Credential Leak to Origin Server Across HTTP-to-HTTPS Redirect in Axios Node.js HTTP Adapter. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-p92q-9vqr-4j8v
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-p92q-9vqr-4j8v](https://osv.dev/vulnerability/GHSA-p92q-9vqr-4j8v) · line 9784 · SHA-256 91165ac13ef2fa2e8e85f80ea8801353fca1cf1d2be5b9ccfb383583c4b1aa99_

```
{"id": "GHSA-p92q-9vqr-4j8v", "aliases": ["CVE-2026-44487"], "modified": "2026-09-10T03:51:09.218790313Z", "summary": "Axios: Proxy-Authorization Credential Leak to Origin Server Across HTTP-to-HTTPS Redirect in Axios Node.js HTTP Adapter", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05775 — axios 0.27.2 затронут GHSA-pf86-5x62-jrwf (CVE-2026-42033)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.4 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-pf86-5x62-jrwf (CVE-2026-42033) для пакета npm axios версии 0.27.2: Axios: Prototype Pollution Gadgets - Response Tampering, Data Exfiltration, and Request Hijacking. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pf86-5x62-jrwf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pf86-5x62-jrwf](https://osv.dev/vulnerability/GHSA-pf86-5x62-jrwf) · line 9784 · SHA-256 a44b8a78be68716ce0a71e307c6cd2d4a7a0311de2ce7d8866a32100e79c6a5b_

```
{"id": "GHSA-pf86-5x62-jrwf", "aliases": ["CVE-2026-42033"], "modified": "2026-09-10T03:51:06.658921258Z", "summary": "Axios: Prototype Pollution Gadgets - Response Tampering, Data Exfiltration, and Request Hijacking", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05776 — axios 0.27.2 затронут GHSA-pjwm-pj3p-43mv (CVE-2026-44492)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 8.6 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-pjwm-pj3p-43mv (CVE-2026-44492) для пакета npm axios версии 0.27.2: axios's shouldBypassProxy does not recognize IPv4-mapped IPv6 addresses, allowing NO_PROXY bypass (incomplete fix for CVE-2025-62718). Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pjwm-pj3p-43mv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pjwm-pj3p-43mv](https://osv.dev/vulnerability/GHSA-pjwm-pj3p-43mv) · line 9784 · SHA-256 df84ce1e471f6ac8550004d0227794d9eaa8f2dca0bcfbc45d9594e0837fdf1f_

```
{"id": "GHSA-pjwm-pj3p-43mv", "aliases": ["CVE-2026-44492"], "modified": "2026-09-10T03:51:06.693575938Z", "summary": "axios's shouldBypassProxy does not recognize IPv4-mapped IPv6 addresses, allowing NO_PROXY bypass (incomplete fix for CVE-2025-62718)", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05777 — axios 0.27.2 затронут GHSA-pmwg-cvhr-8vh7 (CVE-2026-42043)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.2 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-pmwg-cvhr-8vh7 (CVE-2026-42043) для пакета npm axios версии 0.27.2: Axios: Incomplete Fix for CVE-2025-62718 — NO_PROXY Protection Bypassed via RFC 1122 Loopback Subnet (127.0.0.0/8) in Axios 1.15.0. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pmwg-cvhr-8vh7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pmwg-cvhr-8vh7](https://osv.dev/vulnerability/GHSA-pmwg-cvhr-8vh7) · line 9784 · SHA-256 0b8f54404d99b3a73d924c3012e6c07f7c24dc001d4f40189c4e9fe81bde3566_

```
{"id": "GHSA-pmwg-cvhr-8vh7", "aliases": ["CVE-2026-42043"], "modified": "2026-09-10T03:51:06.691311805Z", "summary": "Axios: Incomplete Fix for CVE-2025-62718 — NO_PROXY Protection Bypassed via RFC 1122 Loopback Subnet (127.0.0.0/8) in Axios 1.15.0", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05626 — lodash 4.17.21 затронут GHSA-f23m-r3pf-42rh (CVE-2026-2950)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/lodash@4.17.21`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:L`)

OSV.dev сообщает GHSA-f23m-r3pf-42rh (CVE-2026-2950) для пакета npm lodash версии 4.17.21: lodash vulnerable to Prototype Pollution via array path bypass in `_.unset` and `_.omit`. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-f23m-r3pf-42rh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-f23m-r3pf-42rh](https://osv.dev/vulnerability/GHSA-f23m-r3pf-42rh) · manifest · SHA-256 851a0fffd4c796fa383d6fbc3d9561c029f63f187e945251ed48e65139a0a5ff_

```
{"id": "GHSA-f23m-r3pf-42rh", "aliases": ["CVE-2026-2950"], "modified": "2026-10-17T02:56:13.084362346Z", "summary": "lodash vulnerable to Prototype Pollution via array path bypass in `_.unset` and `_.omit`", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05628 — lodash 4.17.21 затронут GHSA-xxjr-mmjv-4gpg (CVE-2025-13465)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/lodash@4.17.21`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:L`)

OSV.dev сообщает GHSA-xxjr-mmjv-4gpg (CVE-2025-13465) для пакета npm lodash версии 4.17.21: Lodash has Prototype Pollution Vulnerability in `_.unset` and `_.omit` functions. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xxjr-mmjv-4gpg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xxjr-mmjv-4gpg](https://osv.dev/vulnerability/GHSA-xxjr-mmjv-4gpg) · manifest · SHA-256 1717142b9a59f55c7e583fcc5d11b0c944fd8022ccfa789110ec90ea07517970_

```
{"id": "GHSA-xxjr-mmjv-4gpg", "aliases": ["CVE-2025-13465"], "modified": "2026-10-17T02:55:54.229635593Z", "summary": "Lodash has Prototype Pollution Vulnerability in `_.unset` and `_.omit` functions", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:L/SC:H/SI:H/SA:H/E:P"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.17.23).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05629 — nanoid 3.3.6 затронут GHSA-28wg-ghj8-5hjv (CVE-2026-67214)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/nanoid@3.3.6`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-28wg-ghj8-5hjv (CVE-2026-67214) для пакета npm nanoid версии 3.3.6: nanoid: non-secure generators can loop indefinitely with negative size. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-28wg-ghj8-5hjv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-28wg-ghj8-5hjv](https://osv.dev/vulnerability/GHSA-28wg-ghj8-5hjv) · manifest · SHA-256 2302a67ec3b393feb2075f9bc97ea86c38cdb60e2e706cf617652b9702461650_

```
{"id": "GHSA-28wg-ghj8-5hjv", "aliases": ["CVE-2026-67214"], "modified": "2026-09-10T03:50:51.191256883Z", "summary": "nanoid: non-secure generators can loop indefinitely with negative size", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.3.16, 5.1.16).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05630 — nanoid 3.3.6 затронут GHSA-2v37-7h3g-55p8 (CVE-2026-67213)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/nanoid@3.3.6`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-2v37-7h3g-55p8 (CVE-2026-67213) для пакета npm nanoid версии 3.3.6: nanoid: custom generators can loop indefinitely when size is zero. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2v37-7h3g-55p8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2v37-7h3g-55p8](https://osv.dev/vulnerability/GHSA-2v37-7h3g-55p8) · manifest · SHA-256 a2cba23b6c0c21d7bd43925434e7664dbad02fa63c69a50f163cad94fdc2a475_

```
{"id": "GHSA-2v37-7h3g-55p8", "aliases": ["CVE-2026-67213"], "modified": "2026-09-10T03:50:51.243328986Z", "summary": "nanoid: custom generators can loop indefinitely when size is zero", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.3.18, 5.1.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05631 — nanoid 3.3.6 затронут GHSA-mwcw-c2x4-8c55 (CVE-2024-55565)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/nanoid@3.3.6`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 4.3 (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-mwcw-c2x4-8c55 (CVE-2024-55565) для пакета npm nanoid версии 3.3.6: Predictable results in nanoid generation when given non-integer values. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mwcw-c2x4-8c55
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mwcw-c2x4-8c55](https://osv.dev/vulnerability/GHSA-mwcw-c2x4-8c55) · manifest · SHA-256 c8aac9ee3413a1c4d6af59dcbcc132b7a32b8b355228b125a9c0cf63e97dadd5_

```
{"id": "GHSA-mwcw-c2x4-8c55", "aliases": ["CVE-2024-55565"], "modified": "2026-09-10T03:50:21.666094798Z", "summary": "Predictable results in nanoid generation when given non-integer values", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.3.8, 5.0.9).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05621 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (17 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: src/background/controller/wallet.ts
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

46 упоминаний ECDSA в 17 файл(ах), например src/background/controller/wallet.ts:5012. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/background/controller/wallet.ts:5012 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/background/controller/wallet.ts](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/background/controller/wallet.ts#L5012) · line 5012 · SHA-256 3310f80848dc5467d0a13ba8ac17684ee8d7ad71d58704696a3f7d770798a276_

```
 5011 | 
 5012 |   signTypedData = async (
 5013 |     type: string,
```

_file_excerpt · [src/background/controller/wallet.ts](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/background/controller/wallet.ts#L5061) · line 5061 · SHA-256 50d1ceb582d1699fbc6e8d342c105d0d140ab9b2257b78ac4c9b67276cb0d9fa_

```
 5060 |       }).then(() => {
 5061 |         return this.signTypedData(type, from, data as any, options);
 5062 |       });
```

_file_excerpt · [src/background/service/keyring/eth-bitbox02-keyring/eth-bitbox02-keyring.ts](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/background/service/keyring/eth-bitbox02-keyring/eth-bitbox02-keyring.ts#L242) · line 242 · SHA-256 55d496763bbcfdebc6909fe7452e2879e9d35ffe7cf49339d9ea1fc2cb277302_

```
  241 | 
  242 |   async signTypedData(withAccount, data, options: any = {}) {
  243 |     if (options.version !== 'V4') {
```

_file_excerpt · [src/background/service/keyring/eth-cobo-argus-keyring.ts](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/background/service/keyring/eth-cobo-argus-keyring.ts#L114) · line 114 · SHA-256 ac954394697598bf00bd8ae037d28549d50f0a71f810de1af1feb02da2341206_

```
  113 | 
  114 |   signTypedData() {
  115 |     throw new Error('not support in Cobo Safe');
```

_file_excerpt · [src/background/service/keyring/eth-gnosis-keyring.ts](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/background/service/keyring/eth-gnosis-keyring.ts#L723) · line 723 · SHA-256 430d564d2b7881e0c64de373148e05922d411365a0b858c67c68183738c5e4e6_

```
  722 | 
  723 |   signTypedData() {
  724 |     throw new Error('Gnosis address not support signTypedData');
```

_file_excerpt · [src/background/service/keyring/eth-gnosis-keyring.ts](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/background/service/keyring/eth-gnosis-keyring.ts#L724) · line 724 · SHA-256 3219e1e4c9e96e4c6b808088e3bae041ad334fa5d5817d688b90dcac439dafc5_

```
  723 |   signTypedData() {
  724 |     throw new Error('Gnosis address not support signTypedData');
  725 |   }
```

_file_excerpt · [src/background/service/keyring/eth-imkey-keyring/eth-imkey-keyring.ts](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/background/service/keyring/eth-imkey-keyring/eth-imkey-keyring.ts#L338) · line 338 · SHA-256 d2da2842ff2a54dce6bc9516e12fed984c0f8c578a50d0133f4d643fa42c8072_

```
  337 | 
  338 |   async signTypedData(address, data, opts) {
  339 |     await this.unlock();
```

_file_excerpt · [src/background/service/keyring/eth-ledger-keyring.ts](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/background/service/keyring/eth-ledger-keyring.ts#L1403) · line 1403 · SHA-256 cbea547937b4e70d550c88c49f2f3ca875381a49a6e0e70eff2bc0740f951a20_

```
 1402 | 
 1403 |   async signTypedData(
 1404 |     withAccount,
```

_file_excerpt · [src/background/service/keyring/eth-ledger-keyring.ts](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/background/service/keyring/eth-ledger-keyring.ts#L1436) · line 1436 · SHA-256 ae069a2ec00ffd3810dcc0ff90a4b3fb2f5037f9c1670fd601399369763cca88_

```
 1435 |         await runDeviceAction(
 1436 |           signer.signTypedData(this._toLedgerPath(hdPath), data, {
 1437 |             skipOpenApp: true,
```

_file_excerpt · [src/background/service/keyring/eth-onekey-keyring/eth-onekey-keyring.ts](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/background/service/keyring/eth-onekey-keyring/eth-onekey-keyring.ts#L568) · line 568 · SHA-256 50fb12c6b325aa7095bd759288b81065301d36b429e536fbd1a2adebc4bb6fdf_

```
  567 | 
  568 |   async signTypedData(address, data, opts) {
  569 |     switch (opts.version) {
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05622 — Квантово-уязвимый ECDSA: роль не определена (12 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: src/background/service/keyring/index.ts
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

31 упоминаний ECDSA в 12 файл(ах), например src/background/service/keyring/index.ts:1017. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/background/service/keyring/index.ts:1017 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/background/service/keyring/index.ts](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/background/service/keyring/index.ts#L1017) · line 1017 · SHA-256 7c2c9aaf8270758934924654f25a44ca6cebb0d5d1b6c0ab061c475911c4d290_

```
 1016 |       (attempt) =>
 1017 |         keyring.signTypedData(address, msgParams.data, opts, attempt),
 1018 |       address
```

_file_excerpt · [src/ui/utils/sendTypedData.ts](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/ui/utils/sendTypedData.ts#L115) · line 115 · SHA-256 f67d40e21d46972fe5fce7a5c7b6eae11cade0a87207173fa6c6c0087c3120fa_

```
  114 | 
  115 |     hash = await wallet.signTypedData(account?.type, from, data1, {
  116 |       brandName: currentAccount.brandName,
```

_file_excerpt · [src/ui/views/Approval/components/Actions/MultiSwap.tsx](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/ui/views/Approval/components/Actions/MultiSwap.tsx#L180) · line 180 · SHA-256 edb544df009b464a8b156a0dac593aefd6468b2f92d1c1cc95cb365fd6d15b80_

```
  179 |                     chain,
  180 |                     title: t('page.signTypedData.buyNFT.listOn'),
  181 |                   }}
```

_file_excerpt · [src/ui/views/Approval/components/Actions/SwapLimitPay.tsx](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/ui/views/Approval/components/Actions/SwapLimitPay.tsx#L170) · line 170 · SHA-256 d5371570ebb7512445b2fd0dc1029d060c98bcbd21f9ee8b9a0ab9cd42e2cd07_

```
  169 |                     chain,
  170 |                     title: t('page.signTypedData.buyNFT.listOn'),
  171 |                   }}
```

_file_excerpt · [src/ui/views/Approval/components/CommonAction.tsx](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/ui/views/Approval/components/CommonAction.tsx#L36) · line 36 · SHA-256 b74ee08fd5fe63c5766132c9c821c5d251d7c060795be25c8ab8334b9f739663_

```
   35 |   data: CommonActions;
   36 |   requireData?: ContractRequireData | ContractCallRequireData; // ContractRequireData for signTypedData, ContractCallRequireData for signTransaction
   37 |   chain?: Chain;
```

_file_excerpt · [src/ui/views/Approval/components/TypedDataActions/BatchPermit2.tsx](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/ui/views/Approval/components/TypedDataActions/BatchPermit2.tsx#L107) · line 107 · SHA-256 1b90c1a718c3ec899a8f14629f2d6f3ec5ee83e6f6c6e2f8c46a72bebfed71b4_

```
  106 |         <Col>
  107 |           <Row isTitle tip={t('page.signTypedData.permit2.sigExpireTimeTip')}>
  108 |             {t('page.signTypedData.permit2.sigExpireTime')}
```

_file_excerpt · [src/ui/views/Approval/components/TypedDataActions/BatchPermit2.tsx](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/ui/views/Approval/components/TypedDataActions/BatchPermit2.tsx#L108) · line 108 · SHA-256 79e47fe4f61796078a3179258e84f8bdf892e85cdd13e35ebb4a05c18a7d1704_

```
  107 |           <Row isTitle tip={t('page.signTypedData.permit2.sigExpireTimeTip')}>
  108 |             {t('page.signTypedData.permit2.sigExpireTime')}
  109 |           </Row>
```

_file_excerpt · [src/ui/views/Approval/components/TypedDataActions/BatchPermit2.tsx](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/ui/views/Approval/components/TypedDataActions/BatchPermit2.tsx#L123) · line 123 · SHA-256 91b122971e8bde78be868df52a83fc61ce2aaf86e67fd70690677bc088bdcc91_

```
  122 |           <Row isTitle>
  123 |             {t('page.signTypedData.permit2.approvalExpiretime')}
  124 |           </Row>
```

_file_excerpt · [src/ui/views/Approval/components/TypedDataActions/BatchSellNFT.tsx](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/ui/views/Approval/components/TypedDataActions/BatchSellNFT.tsx#L124) · line 124 · SHA-256 9bc2e49352dfc971beb494238b33a8696996b4d55c688229f85d211c24415de4_

```
  123 |         <Col>
  124 |           <Row isTitle>{t('page.signTypedData.sellNFT.listNFT')}</Row>
  125 |           <Row className="gap-y-6 flex flex-col overflow-hidden items-end">
```

_file_excerpt · [src/ui/views/Approval/components/TypedDataActions/BatchSellNFT.tsx](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/src/ui/views/Approval/components/TypedDataActions/BatchSellNFT.tsx#L141) · line 141 · SHA-256 d27cbdee3da87e8c70c3967135b201f7b7187518ede40ff8588bfdd9ea81aab5_

```
  140 |         <Col>
  141 |           <Row isTitle>{t('page.signTypedData.sellNFT.receiveToken')}</Row>
  142 |           <Row>
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05637 — @openzeppelin/contracts 3.4.1-solc-0.7-2 затронут GHSA-7grf-83vw-6f5x (CVE-2022-35915)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@3.4.1-solc-0.7-2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-7grf-83vw-6f5x (CVE-2022-35915) для пакета npm @openzeppelin/contracts версии 3.4.1-solc-0.7-2: OpenZeppelin Contracts ERC165Checker unbounded gas consumption. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7grf-83vw-6f5x
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7grf-83vw-6f5x](https://osv.dev/vulnerability/GHSA-7grf-83vw-6f5x) · line 4591 · SHA-256 e69c833c4dd67dd694a1f622237cf59f5df4edf7aebf05416ad5307115d674d6_

```
{"id": "GHSA-7grf-83vw-6f5x", "aliases": ["CVE-2022-35915"], "modified": "2023-11-08T04:09:52.370855Z", "summary": "OpenZeppelin Contracts ERC165Checker unbounded gas consumption", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.7.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05640 — @openzeppelin/contracts 3.4.1-solc-0.7-2 затронут GHSA-mx2q-35m2-x2rh (CVE-2023-30541)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@3.4.1-solc-0.7-2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-mx2q-35m2-x2rh (CVE-2023-30541) для пакета npm @openzeppelin/contracts версии 3.4.1-solc-0.7-2: OpenZeppelin Contracts TransparentUpgradeableProxy clashing selector calls may not be delegated. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mx2q-35m2-x2rh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mx2q-35m2-x2rh](https://osv.dev/vulnerability/GHSA-mx2q-35m2-x2rh) · line 4591 · SHA-256 1ba1e23e4b88be638e2f34bb89ef527c1424d3e81d1d9bd2a532f61065e63ddb_

```
{"id": "GHSA-mx2q-35m2-x2rh", "aliases": ["CVE-2023-30541"], "modified": "2026-09-10T03:50:01.099654307Z", "summary": "OpenZeppelin Contracts TransparentUpgradeableProxy clashing selector calls may not be delegated", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.8.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05641 — @openzeppelin/contracts 3.4.2-solc-0.7 затронут GHSA-7grf-83vw-6f5x (CVE-2022-35915)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@3.4.2-solc-0.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-7grf-83vw-6f5x (CVE-2022-35915) для пакета npm @openzeppelin/contracts версии 3.4.2-solc-0.7: OpenZeppelin Contracts ERC165Checker unbounded gas consumption. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7grf-83vw-6f5x
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7grf-83vw-6f5x](https://osv.dev/vulnerability/GHSA-7grf-83vw-6f5x) · line 4598 · SHA-256 e69c833c4dd67dd694a1f622237cf59f5df4edf7aebf05416ad5307115d674d6_

```
{"id": "GHSA-7grf-83vw-6f5x", "aliases": ["CVE-2022-35915"], "modified": "2023-11-08T04:09:52.370855Z", "summary": "OpenZeppelin Contracts ERC165Checker unbounded gas consumption", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.7.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05644 — @openzeppelin/contracts 3.4.2-solc-0.7 затронут GHSA-mx2q-35m2-x2rh (CVE-2023-30541)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@3.4.2-solc-0.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-mx2q-35m2-x2rh (CVE-2023-30541) для пакета npm @openzeppelin/contracts версии 3.4.2-solc-0.7: OpenZeppelin Contracts TransparentUpgradeableProxy clashing selector calls may not be delegated. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mx2q-35m2-x2rh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mx2q-35m2-x2rh](https://osv.dev/vulnerability/GHSA-mx2q-35m2-x2rh) · line 4598 · SHA-256 1ba1e23e4b88be638e2f34bb89ef527c1424d3e81d1d9bd2a532f61065e63ddb_

```
{"id": "GHSA-mx2q-35m2-x2rh", "aliases": ["CVE-2023-30541"], "modified": "2026-09-10T03:50:01.099654307Z", "summary": "OpenZeppelin Contracts TransparentUpgradeableProxy clashing selector calls may not be delegated", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.8.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05647 — @openzeppelin/contracts 4.7.0 затронут GHSA-5h3x-9wvq-w4m2 (CVE-2023-34234)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@4.7.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-5h3x-9wvq-w4m2 (CVE-2023-34234) для пакета npm @openzeppelin/contracts версии 4.7.0: OpenZeppelin Contracts's governor proposal creation may be blocked by frontrunning. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5h3x-9wvq-w4m2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-5h3x-9wvq-w4m2](https://osv.dev/vulnerability/GHSA-5h3x-9wvq-w4m2) · line 4605 · SHA-256 85fc64bf95a87e84dfc0e122e6e01d4cbd357628355bad75ec9d84ba91e43c8c_

```
{"id": "GHSA-5h3x-9wvq-w4m2", "aliases": ["CVE-2023-34234"], "modified": "2026-09-10T03:50:02.116353126Z", "summary": "OpenZeppelin Contracts's governor proposal creation may be blocked by frontrunning", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.9.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05648 — @openzeppelin/contracts 4.7.0 затронут GHSA-7grf-83vw-6f5x (CVE-2022-35915)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@4.7.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-7grf-83vw-6f5x (CVE-2022-35915) для пакета npm @openzeppelin/contracts версии 4.7.0: OpenZeppelin Contracts ERC165Checker unbounded gas consumption. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7grf-83vw-6f5x
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7grf-83vw-6f5x](https://osv.dev/vulnerability/GHSA-7grf-83vw-6f5x) · line 4605 · SHA-256 e69c833c4dd67dd694a1f622237cf59f5df4edf7aebf05416ad5307115d674d6_

```
{"id": "GHSA-7grf-83vw-6f5x", "aliases": ["CVE-2022-35915"], "modified": "2023-11-08T04:09:52.370855Z", "summary": "OpenZeppelin Contracts ERC165Checker unbounded gas consumption", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.7.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05650 — @openzeppelin/contracts 4.7.0 затронут GHSA-9j3m-g383-29qr (CVE-2022-35916)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@4.7.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-9j3m-g383-29qr (CVE-2022-35916) для пакета npm @openzeppelin/contracts версии 4.7.0: OpenZeppelin Contracts's Cross chain utilities for Arbitrum L2 see EOA calls as cross chain calls. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9j3m-g383-29qr
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9j3m-g383-29qr](https://osv.dev/vulnerability/GHSA-9j3m-g383-29qr) · line 4605 · SHA-256 1da4ae657d53eb15dcb007498f4bd1088c1104f7dc4815ded43153f67bad591d_

```
{"id": "GHSA-9j3m-g383-29qr", "aliases": ["CVE-2022-35916"], "modified": "2023-11-08T04:09:52.432466Z", "summary": "OpenZeppelin Contracts's Cross chain utilities for Arbitrum L2 see EOA calls as cross chain calls", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.7.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05651 — @openzeppelin/contracts 4.7.0 затронут GHSA-9vx6-7xxf-x967 (CVE-2024-27094)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@4.7.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H`)

OSV.dev сообщает GHSA-9vx6-7xxf-x967 (CVE-2024-27094) для пакета npm @openzeppelin/contracts версии 4.7.0: OpenZeppelin Contracts base64 encoding may read from potentially dirty memory. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9vx6-7xxf-x967
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9vx6-7xxf-x967](https://osv.dev/vulnerability/GHSA-9vx6-7xxf-x967) · line 4605 · SHA-256 b486b5d3c3bcfdae39d02964b5493b268ee7d15dbf1c28d393e95cbef256aebc_

```
{"id": "GHSA-9vx6-7xxf-x967", "aliases": ["CVE-2024-27094"], "modified": "2025-12-05T12:36:38.324850Z", "summary": "OpenZeppelin Contracts base64 encoding may read from potentially dirty memory", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.9.6, 5.0.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05652 — @openzeppelin/contracts 4.7.0 затронут GHSA-g4vp-m682-qqmp (CVE-2023-40014)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@4.7.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-g4vp-m682-qqmp (CVE-2023-40014) для пакета npm @openzeppelin/contracts версии 4.7.0: OpenZeppelin Contracts vulnerable to Improper Escaping of Output. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-g4vp-m682-qqmp
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-g4vp-m682-qqmp](https://osv.dev/vulnerability/GHSA-g4vp-m682-qqmp) · line 4605 · SHA-256 abec547c13ed6dc79d77d0ddfc5c64829e82972f58aac6d14564abf1b2bb8d4d_

```
{"id": "GHSA-g4vp-m682-qqmp", "aliases": ["CVE-2023-40014"], "modified": "2023-11-08T04:13:16.291927Z", "summary": "OpenZeppelin Contracts vulnerable to Improper Escaping of Output", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.9.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05653 — @openzeppelin/contracts 4.7.0 затронут GHSA-mx2q-35m2-x2rh (CVE-2023-30541)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@4.7.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-mx2q-35m2-x2rh (CVE-2023-30541) для пакета npm @openzeppelin/contracts версии 4.7.0: OpenZeppelin Contracts TransparentUpgradeableProxy clashing selector calls may not be delegated. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mx2q-35m2-x2rh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mx2q-35m2-x2rh](https://osv.dev/vulnerability/GHSA-mx2q-35m2-x2rh) · line 4605 · SHA-256 1ba1e23e4b88be638e2f34bb89ef527c1424d3e81d1d9bd2a532f61065e63ddb_

```
{"id": "GHSA-mx2q-35m2-x2rh", "aliases": ["CVE-2023-30541"], "modified": "2026-09-10T03:50:01.099654307Z", "summary": "OpenZeppelin Contracts TransparentUpgradeableProxy clashing selector calls may not be delegated", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.8.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05655 — @openzeppelin/contracts 4.7.0 затронут GHSA-wprv-93r4-jj2p (CVE-2023-34459)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@4.7.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-wprv-93r4-jj2p (CVE-2023-34459) для пакета npm @openzeppelin/contracts версии 4.7.0: OpenZeppelin Contracts using MerkleProof multiproofs may allow proving arbitrary leaves for specific trees. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-wprv-93r4-jj2p
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-wprv-93r4-jj2p](https://osv.dev/vulnerability/GHSA-wprv-93r4-jj2p) · line 4605 · SHA-256 44c88123acc99823e8247a38950c07a13a27f18421da5a697e6950c964f83a90_

```
{"id": "GHSA-wprv-93r4-jj2p", "aliases": ["CVE-2023-34459"], "modified": "2026-09-10T03:50:02.441943191Z", "summary": "OpenZeppelin Contracts using MerkleProof multiproofs may allow proving arbitrary leaves for specific trees", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.9.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05657 — @protobufjs/utf8 1.1.0 затронут GHSA-q6x5-8v7m-xcrf (CVE-2026-44288)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@protobufjs/utf8@1.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-q6x5-8v7m-xcrf (CVE-2026-44288) для пакета npm @protobufjs/utf8 версии 1.1.0: protobufjs has overlong UTF-8 decoding. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-q6x5-8v7m-xcrf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-q6x5-8v7m-xcrf](https://osv.dev/vulnerability/GHSA-q6x5-8v7m-xcrf) · line 4739 · SHA-256 98aac47f5c7610a83fd5292748cac1cc7328191f39d4d9af4dc28b697e37ab9d_

```
{"id": "GHSA-q6x5-8v7m-xcrf", "aliases": ["CVE-2026-44288"], "modified": "2026-09-10T03:50:55.284110621Z", "summary": "protobufjs has overlong UTF-8 decoding", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.1.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05660 — axios 0.24.0 затронут GHSA-3p68-rc4w-qgx5 (CVE-2025-62718)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-3p68-rc4w-qgx5 (CVE-2025-62718) для пакета npm axios версии 0.24.0: Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3p68-rc4w-qgx5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3p68-rc4w-qgx5](https://osv.dev/vulnerability/GHSA-3p68-rc4w-qgx5) · line 9733 · SHA-256 24de2bf2c2b0567dcca1049fb6c83e6b0a00b69cd23dafd93f0e96ed2fd8c036_

```
{"id": "GHSA-3p68-rc4w-qgx5", "aliases": ["CVE-2025-62718"], "modified": "2026-09-10T03:50:42.452672741Z", "summary": "Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.0, 1.15.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05662 — axios 0.24.0 затронут GHSA-5c9x-8gcm-mpgx (CVE-2026-42034)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-5c9x-8gcm-mpgx (CVE-2026-42034) для пакета npm axios версии 0.24.0: Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5c9x-8gcm-mpgx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-5c9x-8gcm-mpgx](https://osv.dev/vulnerability/GHSA-5c9x-8gcm-mpgx) · line 9733 · SHA-256 8507c5d19d76dd81021813965232b1bc9613e8b3f3af18c3cf0ad957330c8666_

```
{"id": "GHSA-5c9x-8gcm-mpgx", "aliases": ["CVE-2026-42034"], "modified": "2026-09-10T03:50:45.707956373Z", "summary": "Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05665 — axios 0.24.0 затронут GHSA-7q8q-rj6j-mhjq (CVE-2026-67319)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319) для пакета npm axios версии 0.24.0: Axios: Nested axios option objects can consume polluted prototype values. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7q8q-rj6j-mhjq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7q8q-rj6j-mhjq](https://osv.dev/vulnerability/GHSA-7q8q-rj6j-mhjq) · line 9733 · SHA-256 4838795094627c51e9533a33dde4f7cf82edc30c300d68055aa2a6903f16efd0_

```
{"id": "GHSA-7q8q-rj6j-mhjq", "aliases": ["CVE-2026-67319"], "modified": "2026-09-10T03:51:10.872027953Z", "summary": "Axios: Nested axios option objects can consume polluted prototype values", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05666 — axios 0.24.0 затронут GHSA-898c-q2cr-xwhg (CVE-2026-44490)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L`)

OSV.dev сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490) для пакета npm axios версии 0.24.0: axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-898c-q2cr-xwhg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-898c-q2cr-xwhg](https://osv.dev/vulnerability/GHSA-898c-q2cr-xwhg) · line 9733 · SHA-256 10ec648796606cfd08553fd8067005e7b9095f6de8f9b684ce539896ddf5b07e_

```
{"id": "GHSA-898c-q2cr-xwhg", "aliases": ["CVE-2026-44490"], "modified": "2026-09-10T03:51:04.811379218Z", "summary": "axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05667 — axios 0.24.0 затронут GHSA-fvcv-3m26-pcqx (CVE-2026-40175)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-fvcv-3m26-pcqx (CVE-2026-40175) для пакета npm axios версии 0.24.0: Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-fvcv-3m26-pcqx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-fvcv-3m26-pcqx](https://osv.dev/vulnerability/GHSA-fvcv-3m26-pcqx) · line 9733 · SHA-256 9ec17186dc46e836df05cd2a2f5682a295141a11ac2b9ae4c62e8f69be49d0f0_

```
{"id": "GHSA-fvcv-3m26-pcqx", "aliases": ["CVE-2026-40175"], "modified": "2026-09-10T03:50:44.273401032Z", "summary": "Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.0, 1.15.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05671 — axios 0.24.0 затронут GHSA-m7pr-hjqh-92cm (CVE-2026-42038)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 6.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-m7pr-hjqh-92cm (CVE-2026-42038) для пакета npm axios версии 0.24.0: Axios: no_proxy bypass via IP alias allows SSRF. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-m7pr-hjqh-92cm
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-m7pr-hjqh-92cm](https://osv.dev/vulnerability/GHSA-m7pr-hjqh-92cm) · line 9733 · SHA-256 b654783f950b13f15741db12cfb830fba8fcb5dbfa19e7d7b3124420e48cf944_

```
{"id": "GHSA-m7pr-hjqh-92cm", "aliases": ["CVE-2026-42038"], "modified": "2026-09-10T03:51:06.293033204Z", "summary": "Axios: no_proxy bypass via IP alias allows SSRF", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05672 — axios 0.24.0 затронут GHSA-mmx7-hfxf-jppx (CVE-2026-67316)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-mmx7-hfxf-jppx (CVE-2026-67316) для пакета npm axios версии 0.24.0: Axios: Prototype pollution gadgets can alter axios request construction. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mmx7-hfxf-jppx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mmx7-hfxf-jppx](https://osv.dev/vulnerability/GHSA-mmx7-hfxf-jppx) · line 9733 · SHA-256 11065eda7b7a743d0f7213a1e2b712cedbf8ad2852bb2defb3b9fb5a812f826b_

```
{"id": "GHSA-mmx7-hfxf-jppx", "aliases": ["CVE-2026-67316"], "modified": "2026-09-10T03:50:52.753640421Z", "summary": "Axios: Prototype pollution gadgets can alter axios request construction", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05677 — axios 0.24.0 затронут GHSA-vf2m-468p-8v99 (CVE-2026-42036)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-vf2m-468p-8v99 (CVE-2026-42036) для пакета npm axios версии 0.24.0: Axios: HTTP adapter streamed responses bypass maxContentLength. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vf2m-468p-8v99
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vf2m-468p-8v99](https://osv.dev/vulnerability/GHSA-vf2m-468p-8v99) · line 9733 · SHA-256 49b0b43d4fcbe7efef36b7b94f1b8d1d09fa6e5382d63877e8d445b03cb4c1e8_

```
{"id": "GHSA-vf2m-468p-8v99", "aliases": ["CVE-2026-42036"], "modified": "2026-09-10T03:50:47.671121168Z", "summary": "Axios: HTTP adapter streamed responses bypass maxContentLength", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05678 — axios 0.24.0 затронут GHSA-w9j2-pvgh-6h63 (CVE-2026-42041)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-w9j2-pvgh-6h63 (CVE-2026-42041) для пакета npm axios версии 0.24.0: Axios: Authentication Bypass via Prototype Pollution Gadget in `validateStatus` Merge Strategy. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w9j2-pvgh-6h63
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w9j2-pvgh-6h63](https://osv.dev/vulnerability/GHSA-w9j2-pvgh-6h63) · line 9733 · SHA-256 2955515615238e7c20c02272fcbc3d529c9817529be8d1ee844ec099dfe3f615_

```
{"id": "GHSA-w9j2-pvgh-6h63", "aliases": ["CVE-2026-42041"], "modified": "2026-09-10T03:50:47.772907977Z", "summary": "Axios: Authentication Bypass via Prototype Pollution Gadget in `validateStatus` Merge Strategy", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05681 — axios 1.12.2 затронут GHSA-3p68-rc4w-qgx5 (CVE-2025-62718)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-3p68-rc4w-qgx5 (CVE-2025-62718) для пакета npm axios версии 1.12.2: Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3p68-rc4w-qgx5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3p68-rc4w-qgx5](https://osv.dev/vulnerability/GHSA-3p68-rc4w-qgx5) · line 9742 · SHA-256 24de2bf2c2b0567dcca1049fb6c83e6b0a00b69cd23dafd93f0e96ed2fd8c036_

```
{"id": "GHSA-3p68-rc4w-qgx5", "aliases": ["CVE-2025-62718"], "modified": "2026-09-10T03:50:42.452672741Z", "summary": "Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.0, 1.15.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05682 — axios 1.12.2 затронут GHSA-3w6x-2g7m-8v23 (CVE-2026-42044)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:N`)

OSV.dev сообщает GHSA-3w6x-2g7m-8v23 (CVE-2026-42044) для пакета npm axios версии 1.12.2: Axios: Invisible JSON Response Tampering via Prototype Pollution Gadget in `parseReviver`. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3w6x-2g7m-8v23
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3w6x-2g7m-8v23](https://osv.dev/vulnerability/GHSA-3w6x-2g7m-8v23) · line 9742 · SHA-256 8657db9c81abe30c07929718563e5d029746c52ba88916257f44ac4d460806fb_

```
{"id": "GHSA-3w6x-2g7m-8v23", "aliases": ["CVE-2026-42044"], "modified": "2026-09-10T03:50:45.398396828Z", "summary": "Axios: Invisible JSON Response Tampering via Prototype Pollution Gadget in `parseReviver`", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.15.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05683 — axios 1.12.2 затронут GHSA-42h9-826w-cgv3 (CVE-2026-67313)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-42h9-826w-cgv3 (CVE-2026-67313) для пакета npm axios версии 1.12.2: Axios: Excessive recursion in formDataToJSON can cause denial of service. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-42h9-826w-cgv3
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-42h9-826w-cgv3](https://osv.dev/vulnerability/GHSA-42h9-826w-cgv3) · line 9742 · SHA-256 d6c3909ec10e2e019286d9bf0e7bc72e7158765a21910a2418df1af4e8370736_

```
{"id": "GHSA-42h9-826w-cgv3", "aliases": ["CVE-2026-67313"], "modified": "2026-09-10T03:51:10.187294734Z", "summary": "Axios: Excessive recursion in formDataToJSON can cause denial of service", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05685 — axios 1.12.2 затронут GHSA-445q-vr5w-6q77 (CVE-2026-42037)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-445q-vr5w-6q77 (CVE-2026-42037) для пакета npm axios версии 1.12.2: Axios: CRLF Injection in multipart/form-data body via unsanitized blob.type in formDataToStream. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-445q-vr5w-6q77
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-445q-vr5w-6q77](https://osv.dev/vulnerability/GHSA-445q-vr5w-6q77) · line 9742 · SHA-256 7de452c500b8f724747fbde990758dab52d8f2a5cde07bec02ee26fa7a26a64b_

```
{"id": "GHSA-445q-vr5w-6q77", "aliases": ["CVE-2026-42037"], "modified": "2026-09-10T03:50:45.396631689Z", "summary": "Axios: CRLF Injection in multipart/form-data body via unsanitized blob.type in formDataToStream", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05686 — axios 1.12.2 затронут GHSA-4hqw-qxg8-jxx2 (CVE-2026-101900)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-4hqw-qxg8-jxx2 (CVE-2026-101900) для пакета npm axios версии 1.12.2: Axios: Fetch Adapter Header Injection via Inherited FormData getHeaders. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4hqw-qxg8-jxx2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4hqw-qxg8-jxx2](https://osv.dev/vulnerability/GHSA-4hqw-qxg8-jxx2) · line 9742 · SHA-256 618e85b178b38ef4f912a99c0ee72dc271729a1a4e2358ae27a3bb3b6fcba132_

```
{"id": "GHSA-4hqw-qxg8-jxx2", "aliases": ["CVE-2026-101900"], "modified": "2026-09-30T15:46:17.701967512Z", "summary": "Axios: Fetch Adapter Header Injection via Inherited FormData getHeaders", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:L/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05687 — axios 1.12.2 затронут GHSA-5c9x-8gcm-mpgx (CVE-2026-42034)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-5c9x-8gcm-mpgx (CVE-2026-42034) для пакета npm axios версии 1.12.2: Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5c9x-8gcm-mpgx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-5c9x-8gcm-mpgx](https://osv.dev/vulnerability/GHSA-5c9x-8gcm-mpgx) · line 9742 · SHA-256 8507c5d19d76dd81021813965232b1bc9613e8b3f3af18c3cf0ad957330c8666_

```
{"id": "GHSA-5c9x-8gcm-mpgx", "aliases": ["CVE-2026-42034"], "modified": "2026-09-10T03:50:45.707956373Z", "summary": "Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05691 — axios 1.12.2 затронут GHSA-7q8q-rj6j-mhjq (CVE-2026-67319)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319) для пакета npm axios версии 1.12.2: Axios: Nested axios option objects can consume polluted prototype values. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7q8q-rj6j-mhjq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7q8q-rj6j-mhjq](https://osv.dev/vulnerability/GHSA-7q8q-rj6j-mhjq) · line 9742 · SHA-256 4838795094627c51e9533a33dde4f7cf82edc30c300d68055aa2a6903f16efd0_

```
{"id": "GHSA-7q8q-rj6j-mhjq", "aliases": ["CVE-2026-67319"], "modified": "2026-09-10T03:51:10.872027953Z", "summary": "Axios: Nested axios option objects can consume polluted prototype values", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05692 — axios 1.12.2 затронут GHSA-898c-q2cr-xwhg (CVE-2026-44490)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L`)

OSV.dev сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490) для пакета npm axios версии 1.12.2: axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-898c-q2cr-xwhg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-898c-q2cr-xwhg](https://osv.dev/vulnerability/GHSA-898c-q2cr-xwhg) · line 9742 · SHA-256 10ec648796606cfd08553fd8067005e7b9095f6de8f9b684ce539896ddf5b07e_

```
{"id": "GHSA-898c-q2cr-xwhg", "aliases": ["CVE-2026-44490"], "modified": "2026-09-10T03:51:04.811379218Z", "summary": "axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05693 — axios 1.12.2 затронут GHSA-9fr6-4gfg-395g (CVE-2026-101902)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-9fr6-4gfg-395g (CVE-2026-101902) для пакета npm axios версии 1.12.2: Axios: Prototype-Pollution Gadget in the Default Instance Allows Inherited Object.prototype.method to Override HTTP Method. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9fr6-4gfg-395g
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9fr6-4gfg-395g](https://osv.dev/vulnerability/GHSA-9fr6-4gfg-395g) · line 9742 · SHA-256 9348b449e55e20a681909cc3ea0b0820d360895e68214c894a0ef66b0e4fb063_

```
{"id": "GHSA-9fr6-4gfg-395g", "aliases": ["CVE-2026-101902"], "modified": "2026-09-30T15:30:03.718390401Z", "summary": "Axios: Prototype-Pollution Gadget in the Default Instance Allows Inherited Object.prototype.method to Override HTTP Method", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.34.0, 1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05694 — axios 1.12.2 затронут GHSA-fvcv-3m26-pcqx (CVE-2026-40175)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-fvcv-3m26-pcqx (CVE-2026-40175) для пакета npm axios версии 1.12.2: Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-fvcv-3m26-pcqx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-fvcv-3m26-pcqx](https://osv.dev/vulnerability/GHSA-fvcv-3m26-pcqx) · line 9742 · SHA-256 9ec17186dc46e836df05cd2a2f5682a295141a11ac2b9ae4c62e8f69be49d0f0_

```
{"id": "GHSA-fvcv-3m26-pcqx", "aliases": ["CVE-2026-40175"], "modified": "2026-09-10T03:50:44.273401032Z", "summary": "Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.0, 1.15.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05697 — axios 1.12.2 затронут GHSA-j8rh-479h-cp32 (CVE-2026-101904)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-j8rh-479h-cp32 (CVE-2026-101904) для пакета npm axios версии 1.12.2: Axios: Header Injection via Inherited headers After Minimal Interceptor. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j8rh-479h-cp32
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j8rh-479h-cp32](https://osv.dev/vulnerability/GHSA-j8rh-479h-cp32) · line 9742 · SHA-256 4b808bddc7a1ef9c83acf9d69b9cdab9901acf387489e3da172b14bad901dfb5_

```
{"id": "GHSA-j8rh-479h-cp32", "aliases": ["CVE-2026-101904"], "modified": "2026-09-30T15:46:18.108444439Z", "summary": "Axios: Header Injection via Inherited headers After Minimal Interceptor", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:L/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05698 — axios 1.12.2 затронут GHSA-jqh4-m9w3-8hp9 (CVE-2026-67317)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-jqh4-m9w3-8hp9 (CVE-2026-67317) для пакета npm axios версии 1.12.2: Axios: Fetch adapter `ReadableStream` uploads bypass `maxBodyLength`. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-jqh4-m9w3-8hp9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-jqh4-m9w3-8hp9](https://osv.dev/vulnerability/GHSA-jqh4-m9w3-8hp9) · line 9742 · SHA-256 72e1ca4cd8db16e38390918031d965c7878c8e6378a5cb82c2c4a6cac1ea5fdf_

```
{"id": "GHSA-jqh4-m9w3-8hp9", "aliases": ["CVE-2026-67317"], "modified": "2026-09-10T03:50:52.448472902Z", "summary": "Axios: Fetch adapter `ReadableStream` uploads bypass `maxBodyLength`", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05701 — axios 1.13.2 затронут GHSA-3p68-rc4w-qgx5 (CVE-2025-62718)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-3p68-rc4w-qgx5 (CVE-2025-62718) для пакета npm axios версии 1.13.2: Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3p68-rc4w-qgx5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3p68-rc4w-qgx5](https://osv.dev/vulnerability/GHSA-3p68-rc4w-qgx5) · line 9753 · SHA-256 24de2bf2c2b0567dcca1049fb6c83e6b0a00b69cd23dafd93f0e96ed2fd8c036_

```
{"id": "GHSA-3p68-rc4w-qgx5", "aliases": ["CVE-2025-62718"], "modified": "2026-09-10T03:50:42.452672741Z", "summary": "Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.0, 1.15.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05703 — axios 1.13.2 затронут GHSA-3w6x-2g7m-8v23 (CVE-2026-42044)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:N`)

OSV.dev сообщает GHSA-3w6x-2g7m-8v23 (CVE-2026-42044) для пакета npm axios версии 1.13.2: Axios: Invisible JSON Response Tampering via Prototype Pollution Gadget in `parseReviver`. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3w6x-2g7m-8v23
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3w6x-2g7m-8v23](https://osv.dev/vulnerability/GHSA-3w6x-2g7m-8v23) · line 9753 · SHA-256 8657db9c81abe30c07929718563e5d029746c52ba88916257f44ac4d460806fb_

```
{"id": "GHSA-3w6x-2g7m-8v23", "aliases": ["CVE-2026-42044"], "modified": "2026-09-10T03:50:45.398396828Z", "summary": "Axios: Invisible JSON Response Tampering via Prototype Pollution Gadget in `parseReviver`", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.15.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05704 — axios 1.13.2 затронут GHSA-42h9-826w-cgv3 (CVE-2026-67313)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-42h9-826w-cgv3 (CVE-2026-67313) для пакета npm axios версии 1.13.2: Axios: Excessive recursion in formDataToJSON can cause denial of service. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-42h9-826w-cgv3
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-42h9-826w-cgv3](https://osv.dev/vulnerability/GHSA-42h9-826w-cgv3) · line 9753 · SHA-256 d6c3909ec10e2e019286d9bf0e7bc72e7158765a21910a2418df1af4e8370736_

```
{"id": "GHSA-42h9-826w-cgv3", "aliases": ["CVE-2026-67313"], "modified": "2026-09-10T03:51:10.187294734Z", "summary": "Axios: Excessive recursion in formDataToJSON can cause denial of service", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05706 — axios 1.13.2 затронут GHSA-445q-vr5w-6q77 (CVE-2026-42037)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-445q-vr5w-6q77 (CVE-2026-42037) для пакета npm axios версии 1.13.2: Axios: CRLF Injection in multipart/form-data body via unsanitized blob.type in formDataToStream. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-445q-vr5w-6q77
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-445q-vr5w-6q77](https://osv.dev/vulnerability/GHSA-445q-vr5w-6q77) · line 9753 · SHA-256 7de452c500b8f724747fbde990758dab52d8f2a5cde07bec02ee26fa7a26a64b_

```
{"id": "GHSA-445q-vr5w-6q77", "aliases": ["CVE-2026-42037"], "modified": "2026-09-10T03:50:45.396631689Z", "summary": "Axios: CRLF Injection in multipart/form-data body via unsanitized blob.type in formDataToStream", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05707 — axios 1.13.2 затронут GHSA-4hqw-qxg8-jxx2 (CVE-2026-101900)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-4hqw-qxg8-jxx2 (CVE-2026-101900) для пакета npm axios версии 1.13.2: Axios: Fetch Adapter Header Injection via Inherited FormData getHeaders. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4hqw-qxg8-jxx2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4hqw-qxg8-jxx2](https://osv.dev/vulnerability/GHSA-4hqw-qxg8-jxx2) · line 9753 · SHA-256 618e85b178b38ef4f912a99c0ee72dc271729a1a4e2358ae27a3bb3b6fcba132_

```
{"id": "GHSA-4hqw-qxg8-jxx2", "aliases": ["CVE-2026-101900"], "modified": "2026-09-30T15:46:17.701967512Z", "summary": "Axios: Fetch Adapter Header Injection via Inherited FormData getHeaders", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:L/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05709 — axios 1.13.2 затронут GHSA-5c9x-8gcm-mpgx (CVE-2026-42034)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-5c9x-8gcm-mpgx (CVE-2026-42034) для пакета npm axios версии 1.13.2: Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5c9x-8gcm-mpgx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-5c9x-8gcm-mpgx](https://osv.dev/vulnerability/GHSA-5c9x-8gcm-mpgx) · line 9753 · SHA-256 8507c5d19d76dd81021813965232b1bc9613e8b3f3af18c3cf0ad957330c8666_

```
{"id": "GHSA-5c9x-8gcm-mpgx", "aliases": ["CVE-2026-42034"], "modified": "2026-09-10T03:50:45.707956373Z", "summary": "Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05713 — axios 1.13.2 затронут GHSA-7q8q-rj6j-mhjq (CVE-2026-67319)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319) для пакета npm axios версии 1.13.2: Axios: Nested axios option objects can consume polluted prototype values. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7q8q-rj6j-mhjq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7q8q-rj6j-mhjq](https://osv.dev/vulnerability/GHSA-7q8q-rj6j-mhjq) · line 9753 · SHA-256 4838795094627c51e9533a33dde4f7cf82edc30c300d68055aa2a6903f16efd0_

```
{"id": "GHSA-7q8q-rj6j-mhjq", "aliases": ["CVE-2026-67319"], "modified": "2026-09-10T03:51:10.872027953Z", "summary": "Axios: Nested axios option objects can consume polluted prototype values", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05714 — axios 1.13.2 затронут GHSA-898c-q2cr-xwhg (CVE-2026-44490)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L`)

OSV.dev сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490) для пакета npm axios версии 1.13.2: axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-898c-q2cr-xwhg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-898c-q2cr-xwhg](https://osv.dev/vulnerability/GHSA-898c-q2cr-xwhg) · line 9753 · SHA-256 10ec648796606cfd08553fd8067005e7b9095f6de8f9b684ce539896ddf5b07e_

```
{"id": "GHSA-898c-q2cr-xwhg", "aliases": ["CVE-2026-44490"], "modified": "2026-09-10T03:51:04.811379218Z", "summary": "axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05715 — axios 1.13.2 затронут GHSA-9fr6-4gfg-395g (CVE-2026-101902)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-9fr6-4gfg-395g (CVE-2026-101902) для пакета npm axios версии 1.13.2: Axios: Prototype-Pollution Gadget in the Default Instance Allows Inherited Object.prototype.method to Override HTTP Method. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9fr6-4gfg-395g
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9fr6-4gfg-395g](https://osv.dev/vulnerability/GHSA-9fr6-4gfg-395g) · line 9753 · SHA-256 9348b449e55e20a681909cc3ea0b0820d360895e68214c894a0ef66b0e4fb063_

```
{"id": "GHSA-9fr6-4gfg-395g", "aliases": ["CVE-2026-101902"], "modified": "2026-09-30T15:30:03.718390401Z", "summary": "Axios: Prototype-Pollution Gadget in the Default Instance Allows Inherited Object.prototype.method to Override HTTP Method", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.34.0, 1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05716 — axios 1.13.2 затронут GHSA-fvcv-3m26-pcqx (CVE-2026-40175)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.13.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-fvcv-3m26-pcqx (CVE-2026-40175) для пакета npm axios версии 1.13.2: Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-fvcv-3m26-pcqx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-fvcv-3m26-pcqx](https://osv.dev/vulnerability/GHSA-fvcv-3m26-pcqx) · line 9753 · SHA-256 9ec17186dc46e836df05cd2a2f5682a295141a11ac2b9ae4c62e8f69be49d0f0_

```
{"id": "GHSA-fvcv-3m26-pcqx", "aliases": ["CVE-2026-40175"], "modified": "2026-09-10T03:50:44.273401032Z", "summary": "Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.0, 1.15.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05721 — axios 1.15.2 затронут GHSA-42h9-826w-cgv3 (CVE-2026-67313)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-42h9-826w-cgv3 (CVE-2026-67313) для пакета npm axios версии 1.15.2: Axios: Excessive recursion in formDataToJSON can cause denial of service. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-42h9-826w-cgv3
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-42h9-826w-cgv3](https://osv.dev/vulnerability/GHSA-42h9-826w-cgv3) · line 9764 · SHA-256 d6c3909ec10e2e019286d9bf0e7bc72e7158765a21910a2418df1af4e8370736_

```
{"id": "GHSA-42h9-826w-cgv3", "aliases": ["CVE-2026-67313"], "modified": "2026-09-10T03:51:10.187294734Z", "summary": "Axios: Excessive recursion in formDataToJSON can cause denial of service", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05722 — axios 1.15.2 затронут GHSA-44g4-m2mj-wpvx (CVE-2026-101899)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-44g4-m2mj-wpvx (CVE-2026-101899) для пакета npm axios версии 1.15.2: Axios: CIDR-form NO_PROXY entries are ignored, causing proxy exclusion bypass for internal IP ranges. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-44g4-m2mj-wpvx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-44g4-m2mj-wpvx](https://osv.dev/vulnerability/GHSA-44g4-m2mj-wpvx) · line 9764 · SHA-256 39d48933660633e359f8405fc6340fd355342d0c92d0b744688c5641838f1efb_

```
{"id": "GHSA-44g4-m2mj-wpvx", "aliases": ["CVE-2026-101899"], "modified": "2026-09-30T15:45:41.069795706Z", "summary": "Axios: CIDR-form NO_PROXY entries are ignored, causing proxy exclusion bypass for internal IP ranges", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:H/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05723 — axios 1.15.2 затронут GHSA-4hqw-qxg8-jxx2 (CVE-2026-101900)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-4hqw-qxg8-jxx2 (CVE-2026-101900) для пакета npm axios версии 1.15.2: Axios: Fetch Adapter Header Injection via Inherited FormData getHeaders. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4hqw-qxg8-jxx2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4hqw-qxg8-jxx2](https://osv.dev/vulnerability/GHSA-4hqw-qxg8-jxx2) · line 9764 · SHA-256 618e85b178b38ef4f912a99c0ee72dc271729a1a4e2358ae27a3bb3b6fcba132_

```
{"id": "GHSA-4hqw-qxg8-jxx2", "aliases": ["CVE-2026-101900"], "modified": "2026-09-30T15:46:17.701967512Z", "summary": "Axios: Fetch Adapter Header Injection via Inherited FormData getHeaders", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:L/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05727 — axios 1.15.2 затронут GHSA-7q8q-rj6j-mhjq (CVE-2026-67319)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319) для пакета npm axios версии 1.15.2: Axios: Nested axios option objects can consume polluted prototype values. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7q8q-rj6j-mhjq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7q8q-rj6j-mhjq](https://osv.dev/vulnerability/GHSA-7q8q-rj6j-mhjq) · line 9764 · SHA-256 4838795094627c51e9533a33dde4f7cf82edc30c300d68055aa2a6903f16efd0_

```
{"id": "GHSA-7q8q-rj6j-mhjq", "aliases": ["CVE-2026-67319"], "modified": "2026-09-10T03:51:10.872027953Z", "summary": "Axios: Nested axios option objects can consume polluted prototype values", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05728 — axios 1.15.2 затронут GHSA-898c-q2cr-xwhg (CVE-2026-44490)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L`)

OSV.dev сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490) для пакета npm axios версии 1.15.2: axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-898c-q2cr-xwhg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-898c-q2cr-xwhg](https://osv.dev/vulnerability/GHSA-898c-q2cr-xwhg) · line 9764 · SHA-256 10ec648796606cfd08553fd8067005e7b9095f6de8f9b684ce539896ddf5b07e_

```
{"id": "GHSA-898c-q2cr-xwhg", "aliases": ["CVE-2026-44490"], "modified": "2026-09-10T03:51:04.811379218Z", "summary": "axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05729 — axios 1.15.2 затронут GHSA-9fr6-4gfg-395g (CVE-2026-101902)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-9fr6-4gfg-395g (CVE-2026-101902) для пакета npm axios версии 1.15.2: Axios: Prototype-Pollution Gadget in the Default Instance Allows Inherited Object.prototype.method to Override HTTP Method. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9fr6-4gfg-395g
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9fr6-4gfg-395g](https://osv.dev/vulnerability/GHSA-9fr6-4gfg-395g) · line 9764 · SHA-256 9348b449e55e20a681909cc3ea0b0820d360895e68214c894a0ef66b0e4fb063_

```
{"id": "GHSA-9fr6-4gfg-395g", "aliases": ["CVE-2026-101902"], "modified": "2026-09-30T15:30:03.718390401Z", "summary": "Axios: Prototype-Pollution Gadget in the Default Instance Allows Inherited Object.prototype.method to Override HTTP Method", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.34.0, 1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05730 — axios 1.15.2 затронут GHSA-f4gw-2p7v-4548 (CVE-2026-67315)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-f4gw-2p7v-4548 (CVE-2026-67315) для пакета npm axios версии 1.15.2: Axios: NO_PROXY bypass for 0.0.0.0 local addresses in axios. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-f4gw-2p7v-4548
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-f4gw-2p7v-4548](https://osv.dev/vulnerability/GHSA-f4gw-2p7v-4548) · line 9764 · SHA-256 5c83dcf006badde859766ea760226aa234dd677120ad87334cb2d2e277f9fe48_

```
{"id": "GHSA-f4gw-2p7v-4548", "aliases": ["CVE-2026-67315"], "modified": "2026-09-10T03:50:51.811859543Z", "summary": "Axios: NO_PROXY bypass for 0.0.0.0 local addresses in axios", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:N/SC:H/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05732 — axios 1.15.2 затронут GHSA-hcpx-6fm6-wx23 (CVE-2026-67321)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-hcpx-6fm6-wx23 (CVE-2026-67321) для пакета npm axios версии 1.15.2: Axios form serializer maxDepth bypass via {} metatoken. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hcpx-6fm6-wx23
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-hcpx-6fm6-wx23](https://osv.dev/vulnerability/GHSA-hcpx-6fm6-wx23) · line 9764 · SHA-256 68ef3894da56fec6420cee70944b52b3cdfbba5b7321da6b9cf321da1e95a3a1_

```
{"id": "GHSA-hcpx-6fm6-wx23", "aliases": ["CVE-2026-67321"], "modified": "2026-09-08T17:45:04.244507616Z", "summary": "Axios form serializer maxDepth bypass via {} metatoken", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05735 — axios 1.15.2 затронут GHSA-j8rh-479h-cp32 (CVE-2026-101904)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-j8rh-479h-cp32 (CVE-2026-101904) для пакета npm axios версии 1.15.2: Axios: Header Injection via Inherited headers After Minimal Interceptor. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j8rh-479h-cp32
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j8rh-479h-cp32](https://osv.dev/vulnerability/GHSA-j8rh-479h-cp32) · line 9764 · SHA-256 4b808bddc7a1ef9c83acf9d69b9cdab9901acf387489e3da172b14bad901dfb5_

```
{"id": "GHSA-j8rh-479h-cp32", "aliases": ["CVE-2026-101904"], "modified": "2026-09-30T15:46:18.108444439Z", "summary": "Axios: Header Injection via Inherited headers After Minimal Interceptor", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:L/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05736 — axios 1.15.2 затронут GHSA-jqh4-m9w3-8hp9 (CVE-2026-67317)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-jqh4-m9w3-8hp9 (CVE-2026-67317) для пакета npm axios версии 1.15.2: Axios: Fetch adapter `ReadableStream` uploads bypass `maxBodyLength`. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-jqh4-m9w3-8hp9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-jqh4-m9w3-8hp9](https://osv.dev/vulnerability/GHSA-jqh4-m9w3-8hp9) · line 9764 · SHA-256 72e1ca4cd8db16e38390918031d965c7878c8e6378a5cb82c2c4a6cac1ea5fdf_

```
{"id": "GHSA-jqh4-m9w3-8hp9", "aliases": ["CVE-2026-67317"], "modified": "2026-09-10T03:50:52.448472902Z", "summary": "Axios: Fetch adapter `ReadableStream` uploads bypass `maxBodyLength`", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05740 — axios 0.21.4 затронут GHSA-3p68-rc4w-qgx5 (CVE-2025-62718)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-3p68-rc4w-qgx5 (CVE-2025-62718) для пакета npm axios версии 0.21.4: Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3p68-rc4w-qgx5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3p68-rc4w-qgx5](https://osv.dev/vulnerability/GHSA-3p68-rc4w-qgx5) · line 9775 · SHA-256 24de2bf2c2b0567dcca1049fb6c83e6b0a00b69cd23dafd93f0e96ed2fd8c036_

```
{"id": "GHSA-3p68-rc4w-qgx5", "aliases": ["CVE-2025-62718"], "modified": "2026-09-10T03:50:42.452672741Z", "summary": "Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.0, 1.15.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05742 — axios 0.21.4 затронут GHSA-5c9x-8gcm-mpgx (CVE-2026-42034)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-5c9x-8gcm-mpgx (CVE-2026-42034) для пакета npm axios версии 0.21.4: Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5c9x-8gcm-mpgx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-5c9x-8gcm-mpgx](https://osv.dev/vulnerability/GHSA-5c9x-8gcm-mpgx) · line 9775 · SHA-256 8507c5d19d76dd81021813965232b1bc9613e8b3f3af18c3cf0ad957330c8666_

```
{"id": "GHSA-5c9x-8gcm-mpgx", "aliases": ["CVE-2026-42034"], "modified": "2026-09-10T03:50:45.707956373Z", "summary": "Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05745 — axios 0.21.4 затронут GHSA-7q8q-rj6j-mhjq (CVE-2026-67319)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319) для пакета npm axios версии 0.21.4: Axios: Nested axios option objects can consume polluted prototype values. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7q8q-rj6j-mhjq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7q8q-rj6j-mhjq](https://osv.dev/vulnerability/GHSA-7q8q-rj6j-mhjq) · line 9775 · SHA-256 4838795094627c51e9533a33dde4f7cf82edc30c300d68055aa2a6903f16efd0_

```
{"id": "GHSA-7q8q-rj6j-mhjq", "aliases": ["CVE-2026-67319"], "modified": "2026-09-10T03:51:10.872027953Z", "summary": "Axios: Nested axios option objects can consume polluted prototype values", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05746 — axios 0.21.4 затронут GHSA-898c-q2cr-xwhg (CVE-2026-44490)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L`)

OSV.dev сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490) для пакета npm axios версии 0.21.4: axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-898c-q2cr-xwhg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-898c-q2cr-xwhg](https://osv.dev/vulnerability/GHSA-898c-q2cr-xwhg) · line 9775 · SHA-256 10ec648796606cfd08553fd8067005e7b9095f6de8f9b684ce539896ddf5b07e_

```
{"id": "GHSA-898c-q2cr-xwhg", "aliases": ["CVE-2026-44490"], "modified": "2026-09-10T03:51:04.811379218Z", "summary": "axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05747 — axios 0.21.4 затронут GHSA-fvcv-3m26-pcqx (CVE-2026-40175)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-fvcv-3m26-pcqx (CVE-2026-40175) для пакета npm axios версии 0.21.4: Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-fvcv-3m26-pcqx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-fvcv-3m26-pcqx](https://osv.dev/vulnerability/GHSA-fvcv-3m26-pcqx) · line 9775 · SHA-256 9ec17186dc46e836df05cd2a2f5682a295141a11ac2b9ae4c62e8f69be49d0f0_

```
{"id": "GHSA-fvcv-3m26-pcqx", "aliases": ["CVE-2026-40175"], "modified": "2026-09-10T03:50:44.273401032Z", "summary": "Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.0, 1.15.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05751 — axios 0.21.4 затронут GHSA-m7pr-hjqh-92cm (CVE-2026-42038)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 6.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-m7pr-hjqh-92cm (CVE-2026-42038) для пакета npm axios версии 0.21.4: Axios: no_proxy bypass via IP alias allows SSRF. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-m7pr-hjqh-92cm
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-m7pr-hjqh-92cm](https://osv.dev/vulnerability/GHSA-m7pr-hjqh-92cm) · line 9775 · SHA-256 b654783f950b13f15741db12cfb830fba8fcb5dbfa19e7d7b3124420e48cf944_

```
{"id": "GHSA-m7pr-hjqh-92cm", "aliases": ["CVE-2026-42038"], "modified": "2026-09-10T03:51:06.293033204Z", "summary": "Axios: no_proxy bypass via IP alias allows SSRF", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05752 — axios 0.21.4 затронут GHSA-mmx7-hfxf-jppx (CVE-2026-67316)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-mmx7-hfxf-jppx (CVE-2026-67316) для пакета npm axios версии 0.21.4: Axios: Prototype pollution gadgets can alter axios request construction. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mmx7-hfxf-jppx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mmx7-hfxf-jppx](https://osv.dev/vulnerability/GHSA-mmx7-hfxf-jppx) · line 9775 · SHA-256 11065eda7b7a743d0f7213a1e2b712cedbf8ad2852bb2defb3b9fb5a812f826b_

```
{"id": "GHSA-mmx7-hfxf-jppx", "aliases": ["CVE-2026-67316"], "modified": "2026-09-10T03:50:52.753640421Z", "summary": "Axios: Prototype pollution gadgets can alter axios request construction", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05757 — axios 0.21.4 затронут GHSA-vf2m-468p-8v99 (CVE-2026-42036)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-vf2m-468p-8v99 (CVE-2026-42036) для пакета npm axios версии 0.21.4: Axios: HTTP adapter streamed responses bypass maxContentLength. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vf2m-468p-8v99
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vf2m-468p-8v99](https://osv.dev/vulnerability/GHSA-vf2m-468p-8v99) · line 9775 · SHA-256 49b0b43d4fcbe7efef36b7b94f1b8d1d09fa6e5382d63877e8d445b03cb4c1e8_

```
{"id": "GHSA-vf2m-468p-8v99", "aliases": ["CVE-2026-42036"], "modified": "2026-09-10T03:50:47.671121168Z", "summary": "Axios: HTTP adapter streamed responses bypass maxContentLength", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05758 — axios 0.21.4 затронут GHSA-w9j2-pvgh-6h63 (CVE-2026-42041)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.21.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-w9j2-pvgh-6h63 (CVE-2026-42041) для пакета npm axios версии 0.21.4: Axios: Authentication Bypass via Prototype Pollution Gadget in `validateStatus` Merge Strategy. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w9j2-pvgh-6h63
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w9j2-pvgh-6h63](https://osv.dev/vulnerability/GHSA-w9j2-pvgh-6h63) · line 9775 · SHA-256 2955515615238e7c20c02272fcbc3d529c9817529be8d1ee844ec099dfe3f615_

```
{"id": "GHSA-w9j2-pvgh-6h63", "aliases": ["CVE-2026-42041"], "modified": "2026-09-10T03:50:47.772907977Z", "summary": "Axios: Authentication Bypass via Prototype Pollution Gadget in `validateStatus` Merge Strategy", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05760 — axios 0.27.2 затронут GHSA-3p68-rc4w-qgx5 (CVE-2025-62718)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-3p68-rc4w-qgx5 (CVE-2025-62718) для пакета npm axios версии 0.27.2: Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3p68-rc4w-qgx5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3p68-rc4w-qgx5](https://osv.dev/vulnerability/GHSA-3p68-rc4w-qgx5) · line 9784 · SHA-256 24de2bf2c2b0567dcca1049fb6c83e6b0a00b69cd23dafd93f0e96ed2fd8c036_

```
{"id": "GHSA-3p68-rc4w-qgx5", "aliases": ["CVE-2025-62718"], "modified": "2026-09-10T03:50:42.452672741Z", "summary": "Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.0, 1.15.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05762 — axios 0.27.2 затронут GHSA-5c9x-8gcm-mpgx (CVE-2026-42034)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-5c9x-8gcm-mpgx (CVE-2026-42034) для пакета npm axios версии 0.27.2: Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5c9x-8gcm-mpgx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-5c9x-8gcm-mpgx](https://osv.dev/vulnerability/GHSA-5c9x-8gcm-mpgx) · line 9784 · SHA-256 8507c5d19d76dd81021813965232b1bc9613e8b3f3af18c3cf0ad957330c8666_

```
{"id": "GHSA-5c9x-8gcm-mpgx", "aliases": ["CVE-2026-42034"], "modified": "2026-09-10T03:50:45.707956373Z", "summary": "Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05765 — axios 0.27.2 затронут GHSA-7q8q-rj6j-mhjq (CVE-2026-67319)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319) для пакета npm axios версии 0.27.2: Axios: Nested axios option objects can consume polluted prototype values. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7q8q-rj6j-mhjq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7q8q-rj6j-mhjq](https://osv.dev/vulnerability/GHSA-7q8q-rj6j-mhjq) · line 9784 · SHA-256 4838795094627c51e9533a33dde4f7cf82edc30c300d68055aa2a6903f16efd0_

```
{"id": "GHSA-7q8q-rj6j-mhjq", "aliases": ["CVE-2026-67319"], "modified": "2026-09-10T03:51:10.872027953Z", "summary": "Axios: Nested axios option objects can consume polluted prototype values", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05766 — axios 0.27.2 затронут GHSA-898c-q2cr-xwhg (CVE-2026-44490)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L`)

OSV.dev сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490) для пакета npm axios версии 0.27.2: axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-898c-q2cr-xwhg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-898c-q2cr-xwhg](https://osv.dev/vulnerability/GHSA-898c-q2cr-xwhg) · line 9784 · SHA-256 10ec648796606cfd08553fd8067005e7b9095f6de8f9b684ce539896ddf5b07e_

```
{"id": "GHSA-898c-q2cr-xwhg", "aliases": ["CVE-2026-44490"], "modified": "2026-09-10T03:51:04.811379218Z", "summary": "axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05767 — axios 0.27.2 затронут GHSA-9fr6-4gfg-395g (CVE-2026-101902)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-9fr6-4gfg-395g (CVE-2026-101902) для пакета npm axios версии 0.27.2: Axios: Prototype-Pollution Gadget in the Default Instance Allows Inherited Object.prototype.method to Override HTTP Method. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9fr6-4gfg-395g
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9fr6-4gfg-395g](https://osv.dev/vulnerability/GHSA-9fr6-4gfg-395g) · line 9784 · SHA-256 9348b449e55e20a681909cc3ea0b0820d360895e68214c894a0ef66b0e4fb063_

```
{"id": "GHSA-9fr6-4gfg-395g", "aliases": ["CVE-2026-101902"], "modified": "2026-09-30T15:30:03.718390401Z", "summary": "Axios: Prototype-Pollution Gadget in the Default Instance Allows Inherited Object.prototype.method to Override HTTP Method", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.34.0, 1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05768 — axios 0.27.2 затронут GHSA-fvcv-3m26-pcqx (CVE-2026-40175)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-fvcv-3m26-pcqx (CVE-2026-40175) для пакета npm axios версии 0.27.2: Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-fvcv-3m26-pcqx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-fvcv-3m26-pcqx](https://osv.dev/vulnerability/GHSA-fvcv-3m26-pcqx) · line 9784 · SHA-256 9ec17186dc46e836df05cd2a2f5682a295141a11ac2b9ae4c62e8f69be49d0f0_

```
{"id": "GHSA-fvcv-3m26-pcqx", "aliases": ["CVE-2026-40175"], "modified": "2026-09-10T03:50:44.273401032Z", "summary": "Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.0, 1.15.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05772 — axios 0.27.2 затронут GHSA-m7pr-hjqh-92cm (CVE-2026-42038)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 6.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-m7pr-hjqh-92cm (CVE-2026-42038) для пакета npm axios версии 0.27.2: Axios: no_proxy bypass via IP alias allows SSRF. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-m7pr-hjqh-92cm
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-m7pr-hjqh-92cm](https://osv.dev/vulnerability/GHSA-m7pr-hjqh-92cm) · line 9784 · SHA-256 b654783f950b13f15741db12cfb830fba8fcb5dbfa19e7d7b3124420e48cf944_

```
{"id": "GHSA-m7pr-hjqh-92cm", "aliases": ["CVE-2026-42038"], "modified": "2026-09-10T03:51:06.293033204Z", "summary": "Axios: no_proxy bypass via IP alias allows SSRF", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05773 — axios 0.27.2 затронут GHSA-mmx7-hfxf-jppx (CVE-2026-67316)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-mmx7-hfxf-jppx (CVE-2026-67316) для пакета npm axios версии 0.27.2: Axios: Prototype pollution gadgets can alter axios request construction. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mmx7-hfxf-jppx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mmx7-hfxf-jppx](https://osv.dev/vulnerability/GHSA-mmx7-hfxf-jppx) · line 9784 · SHA-256 11065eda7b7a743d0f7213a1e2b712cedbf8ad2852bb2defb3b9fb5a812f826b_

```
{"id": "GHSA-mmx7-hfxf-jppx", "aliases": ["CVE-2026-67316"], "modified": "2026-09-10T03:50:52.753640421Z", "summary": "Axios: Prototype pollution gadgets can alter axios request construction", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05778 — axios 0.27.2 затронут GHSA-vf2m-468p-8v99 (CVE-2026-42036)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@0.27.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-vf2m-468p-8v99 (CVE-2026-42036) для пакета npm axios версии 0.27.2: Axios: HTTP adapter streamed responses bypass maxContentLength. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vf2m-468p-8v99
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vf2m-468p-8v99](https://osv.dev/vulnerability/GHSA-vf2m-468p-8v99) · line 9784 · SHA-256 49b0b43d4fcbe7efef36b7b94f1b8d1d09fa6e5382d63877e8d445b03cb4c1e8_

```
{"id": "GHSA-vf2m-468p-8v99", "aliases": ["CVE-2026-42036"], "modified": "2026-09-10T03:50:47.671121168Z", "summary": "Axios: HTTP adapter streamed responses bypass maxContentLength", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05635 — @babel/core 7.29.0 затронут GHSA-4x5r-pxfx-6jf8 (CVE-2026-49356)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@babel/core@7.29.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 3.2 (`CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-4x5r-pxfx-6jf8 (CVE-2026-49356) для пакета npm @babel/core версии 7.29.0: @babel/core: Arbitrary File Read via sourceMappingURL Comment. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4x5r-pxfx-6jf8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4x5r-pxfx-6jf8](https://osv.dev/vulnerability/GHSA-4x5r-pxfx-6jf8) · line 103 · SHA-256 5f71a1b5a670c67dd7f59ea74e809d2535212120b0cb536b016fe24ee52565e2_

```
{"id": "GHSA-4x5r-pxfx-6jf8", "aliases": ["CVE-2026-49356"], "modified": "2026-09-10T03:50:48.280629201Z", "summary": "@babel/core: Arbitrary File Read via sourceMappingURL Comment", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:C/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.29.6, 8.0.0-rc.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05658 — @tootallnate/once 2.0.0 затронут GHSA-vpq2-c234-7xj6 (CVE-2026-3449)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@tootallnate/once@2.0.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 3.3 (`CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-vpq2-c234-7xj6 (CVE-2026-3449) для пакета npm @tootallnate/once версии 2.0.0: @tootallnate/once vulnerable to Incorrect Control Flow Scoping. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vpq2-c234-7xj6
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vpq2-c234-7xj6](https://osv.dev/vulnerability/GHSA-vpq2-c234-7xj6) · line 6657 · SHA-256 b2c649ee2dcd1d5c214d3169987170f2dfd11f0cb5d5bee7d1a1efb551c507a9_

```
{"id": "GHSA-vpq2-c234-7xj6", "aliases": ["CVE-2026-3449"], "modified": "2026-09-10T03:51:00.790088103Z", "summary": "@tootallnate/once vulnerable to Incorrect Control Flow Scoping", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.0.1, 3.0.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05725 — axios 1.15.2 затронут GHSA-654m-c8p4-x5fp (CVE-2026-44489)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/axios@1.15.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-654m-c8p4-x5fp (CVE-2026-44489) для пакета npm axios версии 1.15.2: Axios has a Patch Bypass: Proxy-Authorization Header Injection via Prototype Pollution — Incomplete Null-Prototype Fix. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-654m-c8p4-x5fp
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-654m-c8p4-x5fp](https://osv.dev/vulnerability/GHSA-654m-c8p4-x5fp) · line 9764 · SHA-256 7d5033f294bc6c55c1be4cba4a82a2c066278bb7daee0abdce120b233497c40d_

```
{"id": "GHSA-654m-c8p4-x5fp", "aliases": ["CVE-2026-44489"], "modified": "2026-09-10T03:50:45.767891933Z", "summary": "Axios has a Patch Bypass: Proxy-Authorization Header Injection via Prototype Pollution — Incomplete Null-Prototype Fix", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05779 — 8 бюллетеней в 3 пакет(ах) npm, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:npm:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 15.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 8 бюллетеней (3 с оценкой high или critical) для 3 пакет(ов) npm, которые подтягивают только инструменты разработки или сборки (package.json): например, postcss@8.4.31 [dev]: GHSA-6g55-p6wh-862q, GHSA-fxqj-rqcc-2cmp, GHSA-qx2v-qp2m-jg93, GHSA-r28c-9q8g-f849; webpack@5.76.0 [dev]: GHSA-38r7-794h-5758, GHSA-4vvj-4cpr-p986, GHSA-8fgc-7cc6-rx7x; webpack-dev-middleware@7.4.5 [dev]: GHSA-g84c-rxfj-3j2c. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в package.json.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · package.json · SHA-256 e5a557ed8e9a3a41d1253f298d8874a395746a6721527126b3bb4e6cbc16b049_

```
postcss@8.4.31 [dev]: GHSA-6g55-p6wh-862q, GHSA-fxqj-rqcc-2cmp, GHSA-qx2v-qp2m-jg93, GHSA-r28c-9q8g-f849
webpack@5.76.0 [dev]: GHSA-38r7-794h-5758, GHSA-4vvj-4cpr-p986, GHSA-8fgc-7cc6-rx7x
webpack-dev-middleware@7.4.5 [dev]: GHSA-g84c-rxfj-3j2c
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05620 — MD5 предоставляется функциями API (1 файл(ов))

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:MD5:api`
- Источник данных: scripts/fns.js
- Метод обнаружения: Сопоставление регулярных выражений с API конкретного языка; совпадение в определении, объявлении или внутри функции с именем алгоритма считается предоставлением.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 13.8 / 100
- CVSS v3.1: неприменимо

2 определений, объявлений или тонких обёрток MD5 в 1 файл(ах), например scripts/fns.js:97. Эти файлы предоставляют алгоритм (библиотека хеширования, экспорт FFI); использования в решениях безопасности в них не найдено.

**Возможные последствия.** Само по себе — нет: риск зависит от вызывающего кода. Вызов, полагающийся на стойкость к коллизиям (подписи, сертификаты, дедупликация недоверенных данных), был бы слабым.

**Шаги воспроизведения.**

```
Откройте scripts/fns.js:97 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [scripts/fns.js](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/scripts/fns.js#L97) · line 97 · SHA-256 4d44d424b3ed18f8185e8b2732c688db519422d839b696558ae775816430dc17_

```
   96 | function get_md5(buf) {
   97 |   return require('crypto').createHash('md5').update(buf, 'utf8').digest('hex');
   98 | }
```

_file_excerpt · [scripts/fns.js](https://github.com/RabbyHub/Rabby/blob/663c0e80e9f6139cbb87932ddea909e1e4a382f1/scripts/fns.js#L102) · line 102 · SHA-256 d0a95988e40f7781c631352fe0fc654eda5feab70f33c5d97c1f1393b9686dd9_

```
  101 |   const stream = fs.createReadStream(path.resolve(__dirname, filepath));
  102 |   const hash = require('crypto').createHash('md5');
  103 |   stream.on('data', chunk => {
```

**Ограничения проверки.** Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Зафиксируйте, зачем предоставляется MD5 (протокол или устаревший формат, которому он нужен), проверьте вызывающий код и выведите алгоритм из API там, где он не нужен.

**Повторная проверка.** Повторно просканируйте код после проверки.

### QSI-2026-05624 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:13 UTC
- Балл приоритета: 13.3 / 100
- CVSS v3.1: неприменимо

В 2 манифестах зависимостей QSI нашёл криптобиблиотеки (@noble/curves, @noble/hashes, @noble/secp256k1, @solana/web3.js, crypto-js, elliptic, ethers, secp256k1, tweetnacl), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · package.json, yarn.lock · SHA-256 7d3e64d0fbedc4eca4c8a72332065b89a814164584dc630ac02983c505ac9470_

```
Crypto libraries: @noble/curves, @noble/hashes, @noble/secp256k1, @solana/web3.js, crypto-js, elliptic, ethers, secp256k1, tweetnacl
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
_Допущения планирования: x для обмена ключами, x для подписей, y — значения по умолчанию профиля риска «Криптобиржа, кастодиан или кошелёк», а не данные клиента; с фактическими сроками клиента вывод может измениться._

### Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет


**Следующий шаг:** Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **подпись транзакций и сообщений** | ECDSA (17) | QSI-2026-05621 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |
| **роль не определена** | ECDSA (12) | QSI-2026-05622 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | ECDSA (29) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | HKDF (1), HMAC (1), Keccak-256 (1), MD5 (1) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (1), MD5 (1) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |
| Алгоритм Саймона — суперпозиционные атаки на симметричные конструкции | только при суперпозиционных запросах | Q2 | GCM mode (1) | Для обычного применения AES-GCM или CBC-MAC действий не требуется — модель атаки неприменима. Зафиксируйте это как допущение модели; для конструкций типа Even–Mansour см. офлайн-вариант. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- tls_key_exchange_groups: src/ui/views/DesktopPerps/modal/PositionTpSlModal/index.tsx line 459: not in the algorithm registry, not assessed: {partialGroups}
- tls_key_exchange_groups: src/ui/views/DesktopPerps/modal/PositionTpSlModal/index.tsx line 506: not in the algorithm registry, not assessed: {positionGroups}
- osv_advisories: npm/axios@0.24.0: 23 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories: npm/axios@1.12.2: 32 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories: npm/axios@1.13.2: 35 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories: npm/axios@1.15.2: 28 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories: npm/axios@0.21.4: 23 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories: npm/axios@0.27.2: 24 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P1 | QSI-2026-05623 | Замените и удалите секреты из src/utils/ga4.ts. | устранение первопричины | Сканер секретов ничего не находит; старые значения отозваны. |
| P2 | QSI-2026-05639 | Обновите @openzeppelin/contracts до исправленной версии (3.4.2, 4.3.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fg47-3c2x-m2wr (CVE-2021-39167). |
| P2 | QSI-2026-05643 | Обновите @openzeppelin/contracts до исправленной версии (3.4.2, 4.3.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fg47-3c2x-m2wr (CVE-2021-39167). |
| P2 | QSI-2026-05625 | Обновите fflate до исправленной версии (0.4.9, 0.5.4, 0.6.11, 0.7.5, 0.8.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-px8p-9vwx-vf98 (CVE-2026-45820). |
| P2 | QSI-2026-05627 | Обновите lodash до исправленной версии (4.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-r5fr-rjxr-66jc (CVE-2026-4800). |
| P2 | QSI-2026-05632 | Обновите nanoid до исправленной версии (3.3.12, 5.1.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xwg4-73v4-xw9w (CVE-2026-73086). |
| P2 | QSI-2026-05633 | Обновите uuid до исправленной версии (11.1.1, 12.0.1, 13.0.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w5hq-g745-h8pq (CVE-2026-41907, CVE-2026-41988). |
| P2 | QSI-2026-05634 | Обновите zod до исправленной версии (4.6.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404). |
| P2 | QSI-2026-05636 | Обновите @babel/plugin-transform-modules-systemjs до исправленной версии (7.29.4, 8.0.0-alpha.13). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fv7c-fp4j-7gwp (CVE-2026-44728). |
| P2 | QSI-2026-05638 | Обновите @openzeppelin/contracts до исправленной версии (4.4.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-88g8-f5mf-f5rj (CVE-2021-46320, CVE-2022-39384, GHSA-9c22-pwxw-p6hx). |
| P2 | QSI-2026-05642 | Обновите @openzeppelin/contracts до исправленной версии (4.4.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-88g8-f5mf-f5rj (CVE-2021-46320, CVE-2022-39384, GHSA-9c22-pwxw-p6hx). |
| P2 | QSI-2026-05645 | Обновите @openzeppelin/contracts до исправленной версии (4.7.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4g63-c64m-25w9 (CVE-2022-31172). |
| P2 | QSI-2026-05646 | Обновите @openzeppelin/contracts до исправленной версии (4.7.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4h98-2769-gh6h (CVE-2022-35961). |
| P2 | QSI-2026-05649 | Обновите @openzeppelin/contracts до исправленной версии (4.8.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-93hq-5wgc-jc82 (CVE-2023-30542). |
| P2 | QSI-2026-05654 | Обновите @openzeppelin/contracts до исправленной версии (4.7.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qh9x-gcfh-pcrw (CVE-2022-31170). |
| P2 | QSI-2026-05656 | Обновите @openzeppelin/contracts до исправленной версии (4.7.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xrc4-737v-9q75 (CVE-2022-31198). |
| P2 | QSI-2026-05659 | Обновите axios до исправленной версии (0.31.1, 1.15.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3g43-6gmg-66jw (CVE-2026-44495). |
| P2 | QSI-2026-05661 | Обновите axios до исправленной версии (0.30.3, 1.13.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-43fc-jf86-j433 (CVE-2026-25639). |
| P2 | QSI-2026-05663 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-62hf-57xw-28j9 (CVE-2026-42039). |
| P2 | QSI-2026-05664 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-6chq-wfr3-2hj9 (CVE-2026-42035). |
| P2 | QSI-2026-05668 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496). |
| P2 | QSI-2026-05669 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486). |
| P2 | QSI-2026-05670 | Обновите axios до исправленной версии (0.30.0, 1.8.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-jr5f-v2jv-69x6 (CVE-2025-27152). |
| P2 | QSI-2026-05673 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-p92q-9vqr-4j8v (CVE-2026-44487). |
| P2 | QSI-2026-05674 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pf86-5x62-jrwf (CVE-2026-42033). |
| P2 | QSI-2026-05675 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pjwm-pj3p-43mv (CVE-2026-44492). |
| P2 | QSI-2026-05676 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pmwg-cvhr-8vh7 (CVE-2026-42043). |
| P2 | QSI-2026-05679 | Обновите axios до исправленной версии (1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-35jp-ww65-95wh (CVE-2026-44494). |
| P2 | QSI-2026-05680 | Обновите axios до исправленной версии (0.31.1, 1.15.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3g43-6gmg-66jw (CVE-2026-44495). |
| P2 | QSI-2026-05684 | Обновите axios до исправленной версии (0.30.3, 1.13.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-43fc-jf86-j433 (CVE-2026-25639). |
| P2 | QSI-2026-05688 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-62hf-57xw-28j9 (CVE-2026-42039). |
| P2 | QSI-2026-05689 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-6chq-wfr3-2hj9 (CVE-2026-42035). |
| P2 | QSI-2026-05690 | Обновите axios до исправленной версии (1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-777c-7fjr-54vf (CVE-2026-44488). |
| P2 | QSI-2026-05695 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496). |
| P2 | QSI-2026-05696 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486). |
| P2 | QSI-2026-05699 | Обновите axios до исправленной версии (1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-35jp-ww65-95wh (CVE-2026-44494). |
| P2 | QSI-2026-05700 | Обновите axios до исправленной версии (0.31.1, 1.15.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3g43-6gmg-66jw (CVE-2026-44495). |
| P2 | QSI-2026-05702 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3pq3-5fj3-cg6v (CVE-2026-101898). |
| P2 | QSI-2026-05705 | Обновите axios до исправленной версии (0.30.3, 1.13.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-43fc-jf86-j433 (CVE-2026-25639). |
| P2 | QSI-2026-05708 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-542g-h47m-68v8 (CVE-2026-101901). |
| P2 | QSI-2026-05710 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-62hf-57xw-28j9 (CVE-2026-42039). |
| P2 | QSI-2026-05711 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-6chq-wfr3-2hj9 (CVE-2026-42035). |
| P2 | QSI-2026-05712 | Обновите axios до исправленной версии (1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-777c-7fjr-54vf (CVE-2026-44488). |
| P2 | QSI-2026-05717 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496). |
| P2 | QSI-2026-05718 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486). |
| P2 | QSI-2026-05719 | Обновите axios до исправленной версии (1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-35jp-ww65-95wh (CVE-2026-44494). |
| P2 | QSI-2026-05720 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3pq3-5fj3-cg6v (CVE-2026-101898). |
| P2 | QSI-2026-05724 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-542g-h47m-68v8 (CVE-2026-101901). |
| P2 | QSI-2026-05726 | Обновите axios до исправленной версии (1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-777c-7fjr-54vf (CVE-2026-44488). |
| P2 | QSI-2026-05731 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-gcfj-64vw-6mp9 (CVE-2026-67320). |
| P2 | QSI-2026-05733 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496). |
| P2 | QSI-2026-05734 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486). |
| P2 | QSI-2026-05737 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-m8m8-qj5v-23w3 (CVE-2026-101905). |
| P2 | QSI-2026-05738 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mghh-pgcx-3jjj (CVE-2026-101906). |
| P2 | QSI-2026-05739 | Обновите axios до исправленной версии (0.31.1, 1.15.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3g43-6gmg-66jw (CVE-2026-44495). |
| P2 | QSI-2026-05741 | Обновите axios до исправленной версии (0.30.3, 1.13.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-43fc-jf86-j433 (CVE-2026-25639). |
| P2 | QSI-2026-05743 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-62hf-57xw-28j9 (CVE-2026-42039). |
| P2 | QSI-2026-05744 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-6chq-wfr3-2hj9 (CVE-2026-42035). |
| P2 | QSI-2026-05748 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496). |
| P2 | QSI-2026-05749 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486). |
| P2 | QSI-2026-05750 | Обновите axios до исправленной версии (0.30.0, 1.8.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-jr5f-v2jv-69x6 (CVE-2025-27152). |
| P2 | QSI-2026-05753 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-p92q-9vqr-4j8v (CVE-2026-44487). |
| P2 | QSI-2026-05754 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pf86-5x62-jrwf (CVE-2026-42033). |
| P2 | QSI-2026-05755 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pjwm-pj3p-43mv (CVE-2026-44492). |
| P2 | QSI-2026-05756 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pmwg-cvhr-8vh7 (CVE-2026-42043). |
| P2 | QSI-2026-05759 | Обновите axios до исправленной версии (0.31.1, 1.15.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3g43-6gmg-66jw (CVE-2026-44495). |
| P2 | QSI-2026-05761 | Обновите axios до исправленной версии (0.30.3, 1.13.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-43fc-jf86-j433 (CVE-2026-25639). |
| P2 | QSI-2026-05763 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-62hf-57xw-28j9 (CVE-2026-42039). |
| P2 | QSI-2026-05764 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-6chq-wfr3-2hj9 (CVE-2026-42035). |
| P2 | QSI-2026-05769 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496). |
| P2 | QSI-2026-05770 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486). |
| P2 | QSI-2026-05771 | Обновите axios до исправленной версии (0.30.0, 1.8.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-jr5f-v2jv-69x6 (CVE-2025-27152). |
| P2 | QSI-2026-05774 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-p92q-9vqr-4j8v (CVE-2026-44487). |
| P2 | QSI-2026-05775 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pf86-5x62-jrwf (CVE-2026-42033). |
| P2 | QSI-2026-05776 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pjwm-pj3p-43mv (CVE-2026-44492). |
| P2 | QSI-2026-05777 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pmwg-cvhr-8vh7 (CVE-2026-42043). |
| P2 | QSI-2026-05626 | Обновите lodash до исправленной версии (4.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-f23m-r3pf-42rh (CVE-2026-2950). |
| P2 | QSI-2026-05628 | Обновите lodash до исправленной версии (4.17.23). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xxjr-mmjv-4gpg (CVE-2025-13465). |
| P2 | QSI-2026-05629 | Обновите nanoid до исправленной версии (3.3.16, 5.1.16). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-28wg-ghj8-5hjv (CVE-2026-67214). |
| P2 | QSI-2026-05630 | Обновите nanoid до исправленной версии (3.3.18, 5.1.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2v37-7h3g-55p8 (CVE-2026-67213). |
| P2 | QSI-2026-05631 | Обновите nanoid до исправленной версии (3.3.8, 5.0.9). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mwcw-c2x4-8c55 (CVE-2024-55565). |
| P2 | QSI-2026-05637 | Обновите @openzeppelin/contracts до исправленной версии (4.7.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7grf-83vw-6f5x (CVE-2022-35915). |
| P2 | QSI-2026-05640 | Обновите @openzeppelin/contracts до исправленной версии (4.8.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mx2q-35m2-x2rh (CVE-2023-30541). |
| P2 | QSI-2026-05641 | Обновите @openzeppelin/contracts до исправленной версии (4.7.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7grf-83vw-6f5x (CVE-2022-35915). |
| P2 | QSI-2026-05644 | Обновите @openzeppelin/contracts до исправленной версии (4.8.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mx2q-35m2-x2rh (CVE-2023-30541). |
| P2 | QSI-2026-05647 | Обновите @openzeppelin/contracts до исправленной версии (4.9.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-5h3x-9wvq-w4m2 (CVE-2023-34234). |
| P2 | QSI-2026-05648 | Обновите @openzeppelin/contracts до исправленной версии (4.7.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7grf-83vw-6f5x (CVE-2022-35915). |
| P2 | QSI-2026-05650 | Обновите @openzeppelin/contracts до исправленной версии (4.7.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9j3m-g383-29qr (CVE-2022-35916). |
| P2 | QSI-2026-05651 | Обновите @openzeppelin/contracts до исправленной версии (4.9.6, 5.0.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9vx6-7xxf-x967 (CVE-2024-27094). |
| P2 | QSI-2026-05652 | Обновите @openzeppelin/contracts до исправленной версии (4.9.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-g4vp-m682-qqmp (CVE-2023-40014). |
| P2 | QSI-2026-05653 | Обновите @openzeppelin/contracts до исправленной версии (4.8.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mx2q-35m2-x2rh (CVE-2023-30541). |
| P2 | QSI-2026-05655 | Обновите @openzeppelin/contracts до исправленной версии (4.9.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-wprv-93r4-jj2p (CVE-2023-34459). |
| P2 | QSI-2026-05657 | Обновите @protobufjs/utf8 до исправленной версии (1.1.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-q6x5-8v7m-xcrf (CVE-2026-44288). |
| P2 | QSI-2026-05660 | Обновите axios до исправленной версии (0.31.0, 1.15.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3p68-rc4w-qgx5 (CVE-2025-62718). |
| P2 | QSI-2026-05662 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-5c9x-8gcm-mpgx (CVE-2026-42034). |
| P2 | QSI-2026-05665 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319). |
| P2 | QSI-2026-05666 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490). |
| P2 | QSI-2026-05667 | Обновите axios до исправленной версии (0.31.0, 1.15.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fvcv-3m26-pcqx (CVE-2026-40175). |
| P2 | QSI-2026-05671 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-m7pr-hjqh-92cm (CVE-2026-42038). |
| P2 | QSI-2026-05672 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mmx7-hfxf-jppx (CVE-2026-67316). |
| P2 | QSI-2026-05677 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vf2m-468p-8v99 (CVE-2026-42036). |
| P2 | QSI-2026-05678 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w9j2-pvgh-6h63 (CVE-2026-42041). |
| P2 | QSI-2026-05681 | Обновите axios до исправленной версии (0.31.0, 1.15.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3p68-rc4w-qgx5 (CVE-2025-62718). |
| P2 | QSI-2026-05682 | Обновите axios до исправленной версии (1.15.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3w6x-2g7m-8v23 (CVE-2026-42044). |
| P2 | QSI-2026-05683 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-42h9-826w-cgv3 (CVE-2026-67313). |
| P2 | QSI-2026-05685 | Обновите axios до исправленной версии (1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-445q-vr5w-6q77 (CVE-2026-42037). |
| P2 | QSI-2026-05686 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4hqw-qxg8-jxx2 (CVE-2026-101900). |
| P2 | QSI-2026-05687 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-5c9x-8gcm-mpgx (CVE-2026-42034). |
| P2 | QSI-2026-05691 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319). |
| P2 | QSI-2026-05692 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490). |
| P2 | QSI-2026-05693 | Обновите axios до исправленной версии (0.34.0, 1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9fr6-4gfg-395g (CVE-2026-101902). |
| P2 | QSI-2026-05694 | Обновите axios до исправленной версии (0.31.0, 1.15.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fvcv-3m26-pcqx (CVE-2026-40175). |
| P2 | QSI-2026-05697 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j8rh-479h-cp32 (CVE-2026-101904). |
| P2 | QSI-2026-05698 | Обновите axios до исправленной версии (1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-jqh4-m9w3-8hp9 (CVE-2026-67317). |
| P2 | QSI-2026-05701 | Обновите axios до исправленной версии (0.31.0, 1.15.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3p68-rc4w-qgx5 (CVE-2025-62718). |
| P2 | QSI-2026-05703 | Обновите axios до исправленной версии (1.15.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3w6x-2g7m-8v23 (CVE-2026-42044). |
| P2 | QSI-2026-05704 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-42h9-826w-cgv3 (CVE-2026-67313). |
| P2 | QSI-2026-05706 | Обновите axios до исправленной версии (1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-445q-vr5w-6q77 (CVE-2026-42037). |
| P2 | QSI-2026-05707 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4hqw-qxg8-jxx2 (CVE-2026-101900). |
| P2 | QSI-2026-05709 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-5c9x-8gcm-mpgx (CVE-2026-42034). |
| P2 | QSI-2026-05713 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319). |
| P2 | QSI-2026-05714 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490). |
| P2 | QSI-2026-05715 | Обновите axios до исправленной версии (0.34.0, 1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9fr6-4gfg-395g (CVE-2026-101902). |
| P2 | QSI-2026-05716 | Обновите axios до исправленной версии (0.31.0, 1.15.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fvcv-3m26-pcqx (CVE-2026-40175). |
| P2 | QSI-2026-05721 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-42h9-826w-cgv3 (CVE-2026-67313). |
| P2 | QSI-2026-05722 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-44g4-m2mj-wpvx (CVE-2026-101899). |
| P2 | QSI-2026-05723 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4hqw-qxg8-jxx2 (CVE-2026-101900). |
| P2 | QSI-2026-05727 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319). |
| P2 | QSI-2026-05728 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490). |
| P2 | QSI-2026-05729 | Обновите axios до исправленной версии (0.34.0, 1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9fr6-4gfg-395g (CVE-2026-101902). |
| P2 | QSI-2026-05730 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-f4gw-2p7v-4548 (CVE-2026-67315). |
| P2 | QSI-2026-05732 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-hcpx-6fm6-wx23 (CVE-2026-67321). |
| P2 | QSI-2026-05735 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j8rh-479h-cp32 (CVE-2026-101904). |
| P2 | QSI-2026-05736 | Обновите axios до исправленной версии (1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-jqh4-m9w3-8hp9 (CVE-2026-67317). |
| P2 | QSI-2026-05740 | Обновите axios до исправленной версии (0.31.0, 1.15.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3p68-rc4w-qgx5 (CVE-2025-62718). |
| P2 | QSI-2026-05742 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-5c9x-8gcm-mpgx (CVE-2026-42034). |
| P2 | QSI-2026-05745 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319). |
| P2 | QSI-2026-05746 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490). |
| P2 | QSI-2026-05747 | Обновите axios до исправленной версии (0.31.0, 1.15.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fvcv-3m26-pcqx (CVE-2026-40175). |
| P2 | QSI-2026-05751 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-m7pr-hjqh-92cm (CVE-2026-42038). |
| P2 | QSI-2026-05752 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mmx7-hfxf-jppx (CVE-2026-67316). |
| P2 | QSI-2026-05757 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vf2m-468p-8v99 (CVE-2026-42036). |
| P2 | QSI-2026-05758 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w9j2-pvgh-6h63 (CVE-2026-42041). |
| P2 | QSI-2026-05760 | Обновите axios до исправленной версии (0.31.0, 1.15.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3p68-rc4w-qgx5 (CVE-2025-62718). |
| P2 | QSI-2026-05762 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-5c9x-8gcm-mpgx (CVE-2026-42034). |
| P2 | QSI-2026-05765 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319). |
| P2 | QSI-2026-05766 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490). |
| P2 | QSI-2026-05767 | Обновите axios до исправленной версии (0.34.0, 1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9fr6-4gfg-395g (CVE-2026-101902). |
| P2 | QSI-2026-05768 | Обновите axios до исправленной версии (0.31.0, 1.15.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fvcv-3m26-pcqx (CVE-2026-40175). |
| P2 | QSI-2026-05772 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-m7pr-hjqh-92cm (CVE-2026-42038). |
| P2 | QSI-2026-05773 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mmx7-hfxf-jppx (CVE-2026-67316). |
| P2 | QSI-2026-05778 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vf2m-468p-8v99 (CVE-2026-42036). |
| P2 | QSI-2026-05635 | Обновите @babel/core до исправленной версии (7.29.6, 8.0.0-rc.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4x5r-pxfx-6jf8 (CVE-2026-49356). |
| P2 | QSI-2026-05658 | Обновите @tootallnate/once до исправленной версии (2.0.1, 3.0.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vpq2-c234-7xj6 (CVE-2026-3449). |
| P2 | QSI-2026-05725 | Обновите axios до исправленной версии (1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-654m-c8p4-x5fp (CVE-2026-44489). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-05621 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-05622 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-05621 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05622 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05779 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |
| P4 | QSI-2026-05620 | Задокументируйте, зачем предоставляется MD5, и проверьте вызывающий код. | устранение первопричины | Вызывающий код проверен; MD5 оставлен только там, где его требует протокол. |

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
3. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
4. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
5. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
6. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
7. D. R. Simon — On the Power of Quantum Computation (SIAM J. Comput. 26, 1997) — SIAM. <https://doi.org/10.1137/S0097539796298637> (peer-reviewed article)
8. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
9. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
10. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
11. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
12. H. Kuwakado, M. Morii — Quantum distinguisher between the 3-round Feistel cipher and the random permutation (IEEE ISIT 2010) — IEEE. <https://ieeexplore.ieee.org/document/5513654> (peer-reviewed conference paper)
13. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
14. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
15. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
16. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
17. M. Kaplan, G. Leurent, A. Leverrier, M. Naya-Plasencia — Breaking Symmetric Cryptosystems using Quantum Period Finding (CRYPTO 2016; arXiv:1602.05973) — Springer / arXiv. <https://arxiv.org/abs/1602.05973> (peer-reviewed article: superposition-query forgeries on CBC-MAC, PMAC, GMAC, GCM, OCB)
18. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
19. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
20. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
21. NIST SP 800-131A Rev. 2 — Transitioning the Use of Cryptographic Algorithms and Key Lengths — NIST. <https://csrc.nist.gov/pubs/sp/800/131/a/r2/final> (final (2019))
22. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
23. OSV advisory GHSA-28wg-ghj8-5hjv — OSV.dev. <https://osv.dev/vulnerability/GHSA-28wg-ghj8-5hjv> (modified 2026-09-10T03:50:51.191256883Z)
24. OSV advisory GHSA-2v37-7h3g-55p8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-2v37-7h3g-55p8> (modified 2026-09-10T03:50:51.243328986Z)
25. OSV advisory GHSA-35jp-ww65-95wh — OSV.dev. <https://osv.dev/vulnerability/GHSA-35jp-ww65-95wh> (modified 2026-09-10T03:51:04.268287831Z)
26. OSV advisory GHSA-3g43-6gmg-66jw — OSV.dev. <https://osv.dev/vulnerability/GHSA-3g43-6gmg-66jw> (modified 2026-09-10T03:51:04.440180855Z)
27. OSV advisory GHSA-3p68-rc4w-qgx5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-3p68-rc4w-qgx5> (modified 2026-09-10T03:50:42.452672741Z)
28. OSV advisory GHSA-3pq3-5fj3-cg6v — OSV.dev. <https://osv.dev/vulnerability/GHSA-3pq3-5fj3-cg6v> (modified 2026-09-30T15:15:04.067807024Z)
29. OSV advisory GHSA-3w6x-2g7m-8v23 — OSV.dev. <https://osv.dev/vulnerability/GHSA-3w6x-2g7m-8v23> (modified 2026-09-10T03:50:45.398396828Z)
30. OSV advisory GHSA-42h9-826w-cgv3 — OSV.dev. <https://osv.dev/vulnerability/GHSA-42h9-826w-cgv3> (modified 2026-09-10T03:51:10.187294734Z)
31. OSV advisory GHSA-43fc-jf86-j433 — OSV.dev. <https://osv.dev/vulnerability/GHSA-43fc-jf86-j433> (modified 2026-09-10T03:50:34.100599628Z)
32. OSV advisory GHSA-445q-vr5w-6q77 — OSV.dev. <https://osv.dev/vulnerability/GHSA-445q-vr5w-6q77> (modified 2026-09-10T03:50:45.396631689Z)
33. OSV advisory GHSA-44g4-m2mj-wpvx — OSV.dev. <https://osv.dev/vulnerability/GHSA-44g4-m2mj-wpvx> (modified 2026-09-30T15:45:41.069795706Z)
34. OSV advisory GHSA-4g63-c64m-25w9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-4g63-c64m-25w9> (modified 2023-11-08T04:09:28.648312Z)
35. OSV advisory GHSA-4h98-2769-gh6h — OSV.dev. <https://osv.dev/vulnerability/GHSA-4h98-2769-gh6h> (modified 2023-11-08T04:09:54.445546Z)
36. OSV advisory GHSA-4hqw-qxg8-jxx2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-4hqw-qxg8-jxx2> (modified 2026-09-30T15:46:17.701967512Z)
37. OSV advisory GHSA-4x5r-pxfx-6jf8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-4x5r-pxfx-6jf8> (modified 2026-09-10T03:50:48.280629201Z)
38. OSV advisory GHSA-542g-h47m-68v8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-542g-h47m-68v8> (modified 2026-09-30T15:15:04.061469672Z)
39. OSV advisory GHSA-5c9x-8gcm-mpgx — OSV.dev. <https://osv.dev/vulnerability/GHSA-5c9x-8gcm-mpgx> (modified 2026-09-10T03:50:45.707956373Z)
40. OSV advisory GHSA-5h3x-9wvq-w4m2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-5h3x-9wvq-w4m2> (modified 2026-09-10T03:50:02.116353126Z)
41. OSV advisory GHSA-62hf-57xw-28j9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-62hf-57xw-28j9> (modified 2026-09-10T03:50:45.703789635Z)
42. OSV advisory GHSA-654m-c8p4-x5fp — OSV.dev. <https://osv.dev/vulnerability/GHSA-654m-c8p4-x5fp> (modified 2026-09-10T03:50:45.767891933Z)
43. OSV advisory GHSA-6chq-wfr3-2hj9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-6chq-wfr3-2hj9> (modified 2026-09-10T03:51:04.772235088Z)
44. OSV advisory GHSA-777c-7fjr-54vf — OSV.dev. <https://osv.dev/vulnerability/GHSA-777c-7fjr-54vf> (modified 2026-09-10T03:50:48.738717543Z)
45. OSV advisory GHSA-7grf-83vw-6f5x — OSV.dev. <https://osv.dev/vulnerability/GHSA-7grf-83vw-6f5x> (modified 2023-11-08T04:09:52.370855Z)
46. OSV advisory GHSA-7q8q-rj6j-mhjq — OSV.dev. <https://osv.dev/vulnerability/GHSA-7q8q-rj6j-mhjq> (modified 2026-09-10T03:51:10.872027953Z)
47. OSV advisory GHSA-88g8-f5mf-f5rj — OSV.dev. <https://osv.dev/vulnerability/GHSA-88g8-f5mf-f5rj> (modified 2026-07-16T03:56:17.546633851Z)
48. OSV advisory GHSA-898c-q2cr-xwhg — OSV.dev. <https://osv.dev/vulnerability/GHSA-898c-q2cr-xwhg> (modified 2026-09-10T03:51:04.811379218Z)
49. OSV advisory GHSA-93hq-5wgc-jc82 — OSV.dev. <https://osv.dev/vulnerability/GHSA-93hq-5wgc-jc82> (modified 2023-11-08T04:12:24.945774Z)
50. OSV advisory GHSA-9fr6-4gfg-395g — OSV.dev. <https://osv.dev/vulnerability/GHSA-9fr6-4gfg-395g> (modified 2026-09-30T15:30:03.718390401Z)
51. OSV advisory GHSA-9j3m-g383-29qr — OSV.dev. <https://osv.dev/vulnerability/GHSA-9j3m-g383-29qr> (modified 2023-11-08T04:09:52.432466Z)
52. OSV advisory GHSA-9vx6-7xxf-x967 — OSV.dev. <https://osv.dev/vulnerability/GHSA-9vx6-7xxf-x967> (modified 2025-12-05T12:36:38.324850Z)
53. OSV advisory GHSA-f23m-r3pf-42rh — OSV.dev. <https://osv.dev/vulnerability/GHSA-f23m-r3pf-42rh> (modified 2026-10-17T02:56:13.084362346Z)
54. OSV advisory GHSA-f4gw-2p7v-4548 — OSV.dev. <https://osv.dev/vulnerability/GHSA-f4gw-2p7v-4548> (modified 2026-09-10T03:50:51.811859543Z)
55. OSV advisory GHSA-fg47-3c2x-m2wr — OSV.dev. <https://osv.dev/vulnerability/GHSA-fg47-3c2x-m2wr> (modified 2026-07-08T06:29:37.864167374Z)
56. OSV advisory GHSA-fv7c-fp4j-7gwp — OSV.dev. <https://osv.dev/vulnerability/GHSA-fv7c-fp4j-7gwp> (modified 2026-09-10T03:51:05.541786109Z)
57. OSV advisory GHSA-fvcv-3m26-pcqx — OSV.dev. <https://osv.dev/vulnerability/GHSA-fvcv-3m26-pcqx> (modified 2026-09-10T03:50:44.273401032Z)
58. OSV advisory GHSA-g4vp-m682-qqmp — OSV.dev. <https://osv.dev/vulnerability/GHSA-g4vp-m682-qqmp> (modified 2023-11-08T04:13:16.291927Z)
59. OSV advisory GHSA-gcfj-64vw-6mp9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-gcfj-64vw-6mp9> (modified 2026-09-10T03:50:52.061533850Z)
60. OSV advisory GHSA-hcpx-6fm6-wx23 — OSV.dev. <https://osv.dev/vulnerability/GHSA-hcpx-6fm6-wx23> (modified 2026-09-08T17:45:04.244507616Z)
61. OSV advisory GHSA-hfxv-24rg-xrqf — OSV.dev. <https://osv.dev/vulnerability/GHSA-hfxv-24rg-xrqf> (modified 2026-09-10T03:50:49.732285826Z)
62. OSV advisory GHSA-j5f8-grm9-p9fc — OSV.dev. <https://osv.dev/vulnerability/GHSA-j5f8-grm9-p9fc> (modified 2026-09-10T03:50:50.017253448Z)
63. OSV advisory GHSA-j8rh-479h-cp32 — OSV.dev. <https://osv.dev/vulnerability/GHSA-j8rh-479h-cp32> (modified 2026-09-30T15:46:18.108444439Z)
64. OSV advisory GHSA-jqh4-m9w3-8hp9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-jqh4-m9w3-8hp9> (modified 2026-09-10T03:50:52.448472902Z)
65. OSV advisory GHSA-jr5f-v2jv-69x6 — OSV.dev. <https://osv.dev/vulnerability/GHSA-jr5f-v2jv-69x6> (modified 2026-09-10T03:50:56.787685282Z)
66. OSV advisory GHSA-m7pr-hjqh-92cm — OSV.dev. <https://osv.dev/vulnerability/GHSA-m7pr-hjqh-92cm> (modified 2026-09-10T03:51:06.293033204Z)
67. OSV advisory GHSA-m8m8-qj5v-23w3 — OSV.dev. <https://osv.dev/vulnerability/GHSA-m8m8-qj5v-23w3> (modified 2026-09-30T15:46:18.253717573Z)
68. OSV advisory GHSA-mghh-pgcx-3jjj — OSV.dev. <https://osv.dev/vulnerability/GHSA-mghh-pgcx-3jjj> (modified 2026-09-30T15:15:04.048176303Z)
69. OSV advisory GHSA-mmx7-hfxf-jppx — OSV.dev. <https://osv.dev/vulnerability/GHSA-mmx7-hfxf-jppx> (modified 2026-09-10T03:50:52.753640421Z)
70. OSV advisory GHSA-mrhx-c7xc-m3w5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-mrhx-c7xc-m3w5> (modified 2026-10-23T18:30:09.376405885Z)
71. OSV advisory GHSA-mwcw-c2x4-8c55 — OSV.dev. <https://osv.dev/vulnerability/GHSA-mwcw-c2x4-8c55> (modified 2026-09-10T03:50:21.666094798Z)
72. OSV advisory GHSA-mx2q-35m2-x2rh — OSV.dev. <https://osv.dev/vulnerability/GHSA-mx2q-35m2-x2rh> (modified 2026-09-10T03:50:01.099654307Z)
73. OSV advisory GHSA-p92q-9vqr-4j8v — OSV.dev. <https://osv.dev/vulnerability/GHSA-p92q-9vqr-4j8v> (modified 2026-09-10T03:51:09.218790313Z)
74. OSV advisory GHSA-pf86-5x62-jrwf — OSV.dev. <https://osv.dev/vulnerability/GHSA-pf86-5x62-jrwf> (modified 2026-09-10T03:51:06.658921258Z)
75. OSV advisory GHSA-pjwm-pj3p-43mv — OSV.dev. <https://osv.dev/vulnerability/GHSA-pjwm-pj3p-43mv> (modified 2026-09-10T03:51:06.693575938Z)
76. OSV advisory GHSA-pmwg-cvhr-8vh7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-pmwg-cvhr-8vh7> (modified 2026-09-10T03:51:06.691311805Z)
77. OSV advisory GHSA-px8p-9vwx-vf98 — OSV.dev. <https://osv.dev/vulnerability/GHSA-px8p-9vwx-vf98> (modified 2026-09-10T03:50:52.758792289Z)
78. OSV advisory GHSA-q6x5-8v7m-xcrf — OSV.dev. <https://osv.dev/vulnerability/GHSA-q6x5-8v7m-xcrf> (modified 2026-09-10T03:50:55.284110621Z)
79. OSV advisory GHSA-qh9x-gcfh-pcrw — OSV.dev. <https://osv.dev/vulnerability/GHSA-qh9x-gcfh-pcrw> (modified 2023-11-08T04:09:28.586055Z)
80. OSV advisory GHSA-r5fr-rjxr-66jc — OSV.dev. <https://osv.dev/vulnerability/GHSA-r5fr-rjxr-66jc> (modified 2026-10-17T02:56:15.633068434Z)
81. OSV advisory GHSA-vf2m-468p-8v99 — OSV.dev. <https://osv.dev/vulnerability/GHSA-vf2m-468p-8v99> (modified 2026-09-10T03:50:47.671121168Z)
82. OSV advisory GHSA-vpq2-c234-7xj6 — OSV.dev. <https://osv.dev/vulnerability/GHSA-vpq2-c234-7xj6> (modified 2026-09-10T03:51:00.790088103Z)
83. OSV advisory GHSA-w5hq-g745-h8pq — OSV.dev. <https://osv.dev/vulnerability/GHSA-w5hq-g745-h8pq> (modified 2026-09-10T03:51:03.663336650Z)
84. OSV advisory GHSA-w9j2-pvgh-6h63 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w9j2-pvgh-6h63> (modified 2026-09-10T03:50:47.772907977Z)
85. OSV advisory GHSA-wprv-93r4-jj2p — OSV.dev. <https://osv.dev/vulnerability/GHSA-wprv-93r4-jj2p> (modified 2026-09-10T03:50:02.441943191Z)
86. OSV advisory GHSA-xrc4-737v-9q75 — OSV.dev. <https://osv.dev/vulnerability/GHSA-xrc4-737v-9q75> (modified 2023-11-08T04:09:29.869695Z)
87. OSV advisory GHSA-xwg4-73v4-xw9w — OSV.dev. <https://osv.dev/vulnerability/GHSA-xwg4-73v4-xw9w> (modified 2026-09-01T19:30:08.615560716Z)
88. OSV advisory GHSA-xxjr-mmjv-4gpg — OSV.dev. <https://osv.dev/vulnerability/GHSA-xxjr-mmjv-4gpg> (modified 2026-10-17T02:55:54.229635593Z)
89. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
90. OWASP Application Security Verification Standard — OWASP. <https://owasp.org/www-project-application-security-verification-standard/> (living standard — check the project page for the current version)
91. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
92. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
93. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| MD5 |  |  | слаб классически | взломан | 1 | 1 | scripts/fns.js:97 |
| HKDF |  |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/ui/utils/biometric.ts:70 |
| HMAC |  |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | scripts/notify-lark.js:12 |
| Keccak-256 | Keccak-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 1 | 1 | src/utils/nft.ts:51 |
| Crypto library | 1.8.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 2 | 2 | package.json; yarn.lock:4392 |
| Crypto library | 1.9.7 | @noble/curves (noble-curves) | н/п | допустимо | 2 | 2 | package.json; yarn.lock:4346 |
| Crypto library | 5.8.0 | ethers (ethers.js) | н/п | допустимо | 2 | 2 | package.json; yarn.lock:13568 |
| Crypto library | 4.2.0 | crypto-js (crypto-js) | н/п | допустимо | 1 | 1 | yarn.lock:11682 |
| Crypto library | 6.5.4 | elliptic (elliptic (Node)) | н/п | допустимо | 1 | 1 | yarn.lock:12610 |
| Crypto library | 6.5.7 | elliptic (elliptic (Node)) | н/п | допустимо | 1 | 1 | yarn.lock:12625 |
| Crypto library | 6.6.1 | elliptic (elliptic (Node)) | н/п | допустимо | 1 | 1 | yarn.lock:12640 |
| Crypto library | 5.5.1 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | yarn.lock:13530 |
| Crypto library | 6.13.4 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | yarn.lock:13606 |
| Crypto library | 6.14.1 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | yarn.lock:13621 |
| Crypto library | 6.16.0 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | yarn.lock:13636 |
| Crypto library | 5.0.1 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | yarn.lock:22551 |
| Crypto library | 3.8.1 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | yarn.lock:22563 |
| Crypto library | 4.0.4 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | yarn.lock:22580 |
| Crypto library | 1.0.3 | tweetnacl (TweetNaCl) | н/п | допустимо | 1 | 1 | yarn.lock:24372 |
| Crypto library | 1.2.0 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:4310 |
| Crypto library | 1.4.2 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:4319 |
| Crypto library | 1.8.0 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:4328 |
| Crypto library | 1.9.1 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:4337 |
| Crypto library | 2.2.0 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:4355 |
| Crypto library | 1.2.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:4364 |
| Crypto library | 1.3.2 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:4371 |
| Crypto library | 1.4.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:4378 |
| Crypto library | 1.7.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:4385 |
| Crypto library | 2.2.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:4399 |
| Crypto library | 1.3.3 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:4406 |
| Crypto library | 1.7.1 | @noble/secp256k1 (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:4413 |
| Crypto library | 1.7.2 | @noble/secp256k1 (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:4420 |
| Crypto library | 1.98.4 | @solana/web3.js (Solana web3.js) | н/п | допустимо | 1 | 1 | yarn.lock:6241 |
| GCM mode |  |  | н/п | допустимо | 1 | 1 | src/ui/utils/biometric.ts:64 |
| ECDSA |  |  | уязвим (Шор) | допустимо | 28 | 28 | src/background/controller/wallet.ts:5012; src/background/service/keyring/eth-bitbox02-keyring/eth-bitbox02-keyring.ts:242; src/background/service/keyring/eth-cobo-argus-keyring.ts:114 |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 1 | 1 | src/background/service/perps.ts:4 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| _raw/go-rabby-link-router.js | 1363 | `3889cf93a0e4a2ad158d3f3a7cd239b5a38dce3e7823fbd34ef263a7ca5dd31b` | 0 |
| _raw/sw.js | 5422 | `a93c2a2bcf71ed1432a36d59095b820507ee9596ffcf0435acba5ec0474bf8d7` | 0 |
| changeLogs/index.ts | 2769 | `427a7bdf5799aca6a074d16951573b5e7ce9b95a7b8616a71d037478d2b009e9` | 0 |
| jest.config.js | 2023 | `146093109ce3ad695a9a7a98ac6ce2c9e403c1b388ef06cb14421726f5d0fdc3` | 0 |
| package.json | 10442 | `e5640260b64ad0eac3b95ac8dd019160c69af98b1e7f6aeb986a611e4c917d8a` | 0 |
| postcss.config.js | 150 | `338c4d3484340a4cb4362db7c7bd057a353802fb4f0b9b72f8f0ebb2c2444d4c` | 0 |
| scripts/check-eip7702.js | 5380 | `3ba055f521758448efff391be3ba4e6b80a625edaf441658a38fc5c2efcab3fb` | 0 |
| scripts/fns.js | 3124 | `4c197d56f337205706a568d92749e5519298366b552cdc2983c25c28bd0b34bf` | 0 |
| scripts/make-theme.js | 5090 | `34fbc6af54272ab501bae2542d6bfbf8b060bda00a1707563c9a8c07fdc9ea86` | 0 |
| scripts/manual-qa/tempo-security-cases.js | 3518 | `e637403c31d7dc4a0179e51c3b5d1eb78b3c6d445edf4a6f7f3d71f07dbfb0e7` | 2 |
| scripts/notify-lark.js | 3522 | `08f781843b9594f0e53572dcb235e52af02a07054dd8a1f6e84fee73c79fab61` | 0 |
| scripts/sync-support-chain.js | 540 | `e525bed7091508eb743b9a1227b6c59669650fa480b6a4363c9ce1f10aa17fff` | 0 |
| scripts/update-eip7702-supported-chains.js | 9986 | `b5a2a9494332d5f7306f5071f06f0e710dcbf45db50c25014c9d478bbbe07ca5` | 0 |
| src/@types/i18next.d.ts | 488 | `24a6309c0b8ca11c9486b631dbe0d00598a0b21862a505624ee3b09a72cfe736` | 0 |
| src/background/controller/base.ts | 1099 | `6c82fa881846e5a055eed4a439131c353ef7dcac476f7ce0e92306c616115844` | 0 |
| src/background/controller/index.ts | 116 | `8c39357a16ca5a93e1b004196d3b0f67d2487cfbf5e54ecc5335f1781870d5d3` | 0 |
| src/background/controller/provider/controller.ts | 60427 | `7dc05ed6bd5ba8192fe93f11ceec5917836caaa3041702734d704bf56216c265` | 0 |
| src/background/controller/provider/gnosisController.ts | 937 | `6be058bfc3651756676794a6252019302a92a79622d952ba9114f0954c68036d` | 0 |
| src/background/controller/provider/index.ts | 2644 | `ede94d363facacfbc5d20635f739d2ae35bdd6d46327bce83d3ed4b16a5fb985` | 0 |
| src/background/controller/provider/internalMethod.ts | 6463 | `00312fcb1f82e550bc261d173aa5a7d37570fca80b80a4685ea9832fa658cb06` | 0 |
| src/background/controller/provider/openInDesktopPolicy.ts | 556 | `39ad2a1415b6f34eeeaa3ffbb9dc08fb79b4fcf4f1959ac12800544178e27b68` | 0 |
| src/background/controller/provider/rpcFlow.ts | 21303 | `390a1c344fbebdff8c5cc405eaed172c64585666e60989b12836ca8c4b9c7d30` | 0 |
| src/background/controller/provider/subscriptionManager.ts | 1706 | `b831f9f64ffec9b103b188529f2ee135a49cb25ac06790bbb1f48ae9aa5b530d` | 0 |
| src/background/controller/provider/type.ts | 720 | `3964be4ba0f0f1d08cf151df7501912a58c8e67ce400ec57d7e1b331c86d816a` | 0 |
| src/background/controller/utils.ts | 2743 | `03e219738ad8c98d5690292977ecff44477b09f0243eaf52f4f27eadb7f165f8` | 0 |
| src/background/controller/wallet.ts | 217714 | `29fe920a8fb2846a2d85b349770e5241e0b6828e25fe4ceab71aabb9481d3927` | 0 |
| src/background/controller/walletUtils/approvalSigning.ts | 2038 | `3452826b9cacf77031ecb0e734e95442ad062fa807e082a41f93a2799efea488` | 0 |
| src/background/controller/walletUtils/boot.ts | 738 | `7d0972933974939cedeb3bcd21ed68d46f27c647ea2039cc44918b72caf06f85` | 0 |
| src/background/controller/walletUtils/fix.ts | 846 | `04707f7664ce7064043c23cfa09d209d7b0994d7414fdcede69e202f7df680a0` | 0 |
| src/background/controller/walletUtils/sign.ts | 4139 | `ed9cb582349b1b7349dcee45c392023b206d5e169804dedea8531983472589e7` | 0 |
| src/background/index.ts | 21496 | `0cf8f5388153c088d5092bcb770d15c63bfb5467054419d7375af9af0da7d0ca` | 0 |
| src/background/service/HDKeyRingLastAddAddrTime.ts | 527 | `67909968eddbace1861efce6251b53784310e96a1b8919b0c950836f0fe1b17e` | 0 |
| src/background/service/autoLock.ts | 1613 | `1e7bfb7c54043cb8b1610d22aeb29645c8eb95e3a51974b47eba75d3bd438697` | 0 |
| src/background/service/bridge.ts | 4897 | `8284d31c845c94a3eada424264743ad10eb8e1d8e957f02e6e923570409a94bd` | 0 |
| src/background/service/contactBook.ts | 5391 | `c98573667728646e5dd403c14de136ec908afb17479a834b83bf2feef037e49e` | 0 |
| src/background/service/currency.ts | 3471 | `6ba6cc5e452e7deb43d77b292f5cf8d6284b23673c2db8ae9c5ba248c8a1ac6d` | 0 |
| src/background/service/customTestnet.ts | 38082 | `02b4dc6339cc67c92c451f4e7dd8a4de6eafef8c60f458ce877ea5d62a2a5b9e` | 0 |
| src/background/service/extensionUpdate.ts | 7521 | `af272ca60d9f7d8cb1b0d646b9aae910f9d542aa3851fe36bddbd5e21226cec0` | 0 |
| src/background/service/feedback.ts | 4485 | `6ed57e619ac5d31918cb7fa2f2807e4e846e58169b3ffbd2f9c218678f86b764` | 0 |
| src/background/service/gasAccount.ts | 7539 | `78ad1eb641fe389b279071ce986264feccc79b584559b7a1ad74d8b8f80a65cb` | 0 |
| src/background/service/gasMarket.ts | 1474 | `6ae1813ea347573bf8aad3cb25478c0a5a863a9d1e0ad2fa17ff546f29166321` | 0 |
| src/background/service/i18n.ts | 2305 | `124a71f5dc4faf0f93e719411cbf7d4b01ae918866fd04c5a711302bfe500d6f` | 0 |
| src/background/service/index.ts | 1831 | `3afa3242b7c9f8f021148a0d4071739c6f1e9fd4ee7ad01732d49a391e899de3` | 0 |
| src/background/service/keyring/bridge.ts | 1266 | `1766411e5a49c82ead863fef030e5b36f591757958c72501a94ad8e249f72a2e` | 0 |
| src/background/service/keyring/display.ts | 1021 | `6e7346b55ae2db6b22595abc3badc7acc8a49b24399e80679c3a621497f91850` | 0 |
| src/background/service/keyring/eth-bitbox02-keyring/bitbox02-bridge-interface.ts | 794 | `fb38acb3396a9a64554c8c2f5409bb46a435c35ca06202d34cf60b0a99691a2d` | 0 |
| src/background/service/keyring/eth-bitbox02-keyring/bitbox02-bridge.ts | 3361 | `3496c349f346befaf743a3a9c6bc821987a6d899bd87fefbbfbde176d47e93a6` | 0 |
| src/background/service/keyring/eth-bitbox02-keyring/bitbox02-offscreen-bridge.ts | 3276 | `195d79e3c203d6ce2dc1741ca8aedaa81651d897104951ccb4c7935316ef4e57` | 0 |
| src/background/service/keyring/eth-bitbox02-keyring/eth-bitbox02-keyring.ts | 8277 | `8c7eb897e57212f3242d72db85a3ace38a7cb22453efdfdfd604fe59d2d99dd6` | 0 |
| src/background/service/keyring/eth-cobo-argus-keyring.ts | 2757 | `52606dece69811fd5b9b143bfd7cef274d2a9197afe7af30b92d40031c2105de` | 0 |
| src/background/service/keyring/eth-gnosis-keyring.ts | 19665 | `c10d15a59677345f45b3402358f05bef84c6b7533e002fbd16b568654fac1073` | 0 |
| src/background/service/keyring/eth-imkey-keyring/eth-imkey-keyring.ts | 12968 | `7b48b44b279573625a600bd54f0fdb6b4c186242f3219c327f21bd672397523f` | 0 |
| src/background/service/keyring/eth-imkey-keyring/imkey-bridge-interface.ts | 426 | `7925d95a1712fc8a62e507cb1fd1d28e35c94852435ad628d0095b1656568319` | 0 |
| src/background/service/keyring/eth-imkey-keyring/imkey-bridge.ts | 1496 | `6e265781a8cb7cae9650470468f116f444a2c3715d8d6bf553961f718e9069d8` | 0 |
| src/background/service/keyring/eth-imkey-keyring/imkey-offscreen-bridge.ts | 1591 | `b967169349f62a63967d4e126360fe13806cecd187022a7d02daa7a3af9568d8` | 0 |
| src/background/service/keyring/eth-imkey-keyring/utils.ts | 1035 | `7fd1c40bcc3bd77af2c7313d53d6f322202cc62d74b7cdd8ff5243f0b51e9ec7` | 0 |
| src/background/service/keyring/eth-keystone-keyring/index.ts | 8745 | `14946027099254222cef82856938bc5ea4ad7628b39d6108652f597566cd2dab` | 0 |
| src/background/service/keyring/eth-keystone-keyring/utils.ts | 3730 | `53c45cec90b712d8feebdfadddb8cca0941c4c9e85e0a1a3f0988c9c5cee37f6` | 0 |
| src/background/service/keyring/eth-lattice-keyring/eth-lattice-keyring.ts | 6014 | `11c33f731e2a3c55a6706fa982711bdbc05b8f9116958a3ae26581812e865bb8` | 0 |
| src/background/service/keyring/eth-ledger-keyring.ts | 51900 | `9c656d72034ab8e31c39f12b47839e5dcde55d880163798c62e2ab26997cd326` | 0 |
| src/background/service/keyring/eth-onekey-keyring/eth-onekey-keyring.ts | 28476 | `e758244dd3e405ef9382416727e6a9b2172e062a8b408cf72086eb10fb6a8138` | 0 |
| src/background/service/keyring/eth-onekey-keyring/onekey-bridge-interface.ts | 452 | `0157e0ebf702825860634b1782d0bd18a6c4c243272ed84621f5da5c1474ab2b` | 0 |
| src/background/service/keyring/eth-onekey-keyring/onekey-bridge.ts | 1954 | `5921e76d895e3339ddf20a39121461c6928849e9f62423fb2949340a03d79e5b` | 0 |
| src/background/service/keyring/eth-onekey-keyring/onekey-offscreen-bridge.ts | 4075 | `609593f4e6a5d94534d25173e8733b1a51875542bb4716a420731db5103a88e9` | 0 |
| src/background/service/keyring/eth-trezor-keyring/trezor-offscreen-bridge.ts | 5326 | `2d304e0a6954779eae16f29b7b267436fe8a8ba24ce41f6c0bc201bf4d032491` | 0 |
| src/background/service/keyring/helper.ts | 102 | `3d2c6fb72ed0a8ba1346ab093bf2a832760c3391deacabb193aa4b2120382da5` | 0 |
| src/background/service/keyring/index.ts | 50167 | `fa0583e7807f6aa3ac24b8fff8849be8d510624e249e68b3aaa9148d97137a9c` | 0 |
| src/background/service/keyring/sanitizeUnencryptedKeyringData.ts | 578 | `074cbde0feb73017ab6ae51183af7f65386dd1843d7f46996e4a52a60d52f37f` | 0 |
| src/background/service/keyring/signing-diagnostics.ts | 12614 | `8f02dd337ceff939d9dce7ed90f048989fea05d764db8889b01d2bb846e9b5d8` | 0 |
| src/background/service/metamaskModeService.ts | 2492 | `d6b767cd12c1dc7fe5fd13a8c74a68dbf2e15841c7f256344caa1bd6c366521e` | 0 |
| src/background/service/misc.ts | 339 | `4d27f23539bddf498c9aa38246330bb11cb2964d0185f8eaf4dee3db3b060aad` | 0 |
| src/background/service/notification.ts | 18856 | `3f5bcda2a1e3faf71a65556894268ab97152e23415f556a8d28eb536d762d109` | 0 |
| src/background/service/offlineChain.ts | 691 | `fa9ac4b7db9231770658509dd1e7305bf42459452f28be374cde542206a7a0a7` | 0 |
| src/background/service/openapi.ts | 3158 | `a01e4aec09408ad32dab3b89a68a39e879fcc73a1790d22c283c911c072a3071` | 0 |
| src/background/service/pageStateCache.ts | 1345 | `e723faa130660005cc565c2f154939454ff11dd30d0ea3e211f37cad18db8e3e` | 0 |
| src/background/service/permission.ts | 7701 | `68416fb784ddb7633350db7fcc061a9d9ae1fd53f6f95a9e7875a4d64ddff801` | 0 |
| src/background/service/perps.ts | 21804 | `b15a9ff9955cc8f2c98cf6b1aa59bac03277911c3c288d4606d3c0c1ba32127e` | 0 |
| src/background/service/perpsLive.ts | 29945 | `580518df5844a5a27a3872f8bd5dbeb9957550ccfa90d51af54b273e7a473a24` | 0 |
| src/background/service/preference.ts | 30286 | `39adf576e9609a23afff53249253720249624dba2b7af1dca2e262d8b3155a8a` | 0 |
| src/background/service/rabbyPoints.ts | 1152 | `f17a0646e98f10627705f5766004719d151d186145a07e809bf6016b470681a2` | 0 |
| src/background/service/removedTokens.ts | 2023 | `6e5c63ae23b0ba2a7d3cb8ee6c255d0589030b6a34fd7c7d0bd4b31eb9c7bdba` | 0 |
| src/background/service/rpc.ts | 11132 | `7164c3aba336d4977f570cff09bf336a7d581f2263f24c439e99c2f2d303fc0b` | 0 |
| src/background/service/securityEngine.ts | 9558 | `a3afd21ac6ad32cd1af1343f630a169bdd2e0c100855c2cb0ab540104c0dbc26` | 0 |
| src/background/service/session.ts | 2495 | `ace4cd3b1158cbe5b079a59bc0c387474980056994b6a6a8e36626998ff07398` | 0 |
| src/background/service/signTextHistory.ts | 2868 | `7219d24b6697b179a9c88036523d41a079f472b08f57f4eafc62ad8a8ecf2a03` | 0 |
| src/background/service/signTxPreparation.ts | 6070 | `d800310d048473c4a842dd3ff080d8231fde70492dab887dfda4554f93841488` | 0 |
| src/background/service/swap.ts | 5674 | `66fe7eb6ce51531b091cd175d43a85635e7362c7c489be76d3933cf6d640b865` | 0 |
| src/background/service/syncChain.ts | 2685 | `0a2567bc8602b529f7a3cb6efde819e55e05cdee9c58af147ea67d7dd2b6ee72` | 0 |
| src/background/service/transactionBroadcastWatcher.ts | 4630 | `d52d856ad94c5b200906e64ed0794ea5330e6e23862af8fe28249bbab4dda036` | 0 |
| src/background/service/transactionHistory.ts | 43225 | `05de5f5d3243f5ff7ff4e2ac2bbfd4d1028841eb4c0fcbb7903c7e2880598518` | 0 |
| src/background/service/transactionWatcher.ts | 7892 | `900c0291697f1fb2c21914daa2c1ba7c0309b229a26a82efefb1cd9020bd567f` | 0 |
| src/background/service/transactions.ts | 1402 | `e533ca9f93f522991151630d9e780fcbb77a035b50dc35da36d74e1e8aaae84a` | 0 |
| src/background/service/unTriggerTxCounter.ts | 269 | `56bea423fc7b0614fafdd61282715891df5e4bb206241f1264e014c211fa48e0` | 0 |
| src/background/service/uninstalled.ts | 3010 | `2b66ffee087108a614f407ab8fe3251022df36cd1be39f1bb2107993c0be3a78` | 0 |
| src/background/service/userGuide.ts | 1488 | `c3084ad747d9be3d0a6d70dfda3335d8f68681e62ab8d5ded01ea8f8f0836902` | 0 |
| src/background/service/whitelist.ts | 4284 | `2249070d8a5a872eb6fdf9b6d46553b5dd50599af732ed62e979b6f979f72b10` | 0 |
| src/background/subscriptions/rateGuidance.ts | 1172 | `2b78f7e32ee4c4f89a19238b2fc713fc17d903e24d5c7af404177a23e6f01c2f` | 0 |
| src/background/utils/7702.ts | 624 | `e77b4a632fab40a9a61edf84471748f62e38fba1fe5f46ae58e7df0d1eef33b5` | 0 |
| src/background/utils/alarms.ts | 320 | `b7a4af9a41c75fcc6f373e781426a43a82b58121a8ffb67b0e93fa3e2db18477` | 0 |
| src/background/utils/assertProviderRequest.ts | 636 | `5dc4bbb1ada8b9435569103188f581c8a99fbafbf344c2dd4812638827775460` | 0 |
| src/background/utils/broadcastToUI.ts | 373 | `a5ebfcaa2aad1316a797018288e6b2d45be0d67cdd0d7e42126fae36ae57bd95` | 0 |
| src/background/utils/buildinProvider.ts | 5615 | `c4e91134e4a4d614a18dcc601f40e542177da182ab024eef87dcae6db4ab5a53` | 0 |
| src/background/utils/cache.ts | 1921 | `d1b57b0eba594f8acf169afa41d26bd4aa48bf45e6388a092a9480f581f04d85` | 0 |
| src/background/utils/errorTxRetry.ts | 5042 | `fc1d98f1307e20c0774957534e9a7dd1dc4ea0f10f938fe2cb9f21032cf18d57` | 0 |
| src/background/utils/gasAccountDiscovery.ts | 6152 | `ddef8256381238459cee72601f76cd045c1e3f7ce6520cd0ae8c4f71fe2875e0` | 0 |
| src/background/utils/gasAccountLogin.ts | 2692 | `50bb18aa7eb2250d3ab36bc4c5c32c5aa202c5d7d7396f1b593dec07dc0e0c39` | 0 |
| src/background/utils/http.ts | 152 | `54f7d54ee466cfafd144382c92ff6f2d17473309d1178e2e4556b6f9d50be66b` | 0 |
| src/background/utils/index.ts | 3246 | `efbacb2a567df878766145a674908c0d188577d010ab79036481e8e2b04fc995` | 0 |
| src/background/utils/ipfs.ts | 2817 | `28f02d5e5300fb95d4729e8f24e6b32fe08404ef5e4c609c703b35d324ecf55e` | 0 |
| src/background/utils/password.ts | 3887 | `0e12a9d1a7004ebdfe470f3d8feaeff9dad7d6a216d628d684a46a4dc5c62f46` | 0 |
| src/background/utils/persistStore.ts | 8180 | `b1fc71eb60848c37c8bdf7051aa7f9f4d520d8aa2873d998354742f45df3c815` | 0 |
| src/background/utils/promiseFlow.ts | 605 | `770f2df43baf6bcf0a9a0aa0abf678cb6ee939a263cee3ad9718416aa2db2c5c` | 0 |
| src/background/utils/rpcCache.ts | 4368 | `dfa33caab1df80345a70e7354b3c33e2af5a8a8d173e6ffe1b885907cbd7680d` | 0 |
| src/background/utils/safe.ts | 885 | `53c2648c0e1cb4bca6ae05f3528ed43f91328ccf4388ae2eb5ee11696859c3aa` | 0 |
| src/background/utils/tx.ts | 1758 | `a14c1bca5849ee41fd2080b9b6e356b0f5c925c5c153f0da63a5679d23ea109e` | 0 |
| src/background/utils/typedDataTypes.ts | 1263 | `509b70e01e5daf39492a37193484469de27133ce88092befb363cd4453120735` | 0 |
| src/background/utils/walletconnectTransportError.ts | 1104 | `07cab8cf326795356fb53365223afd56209f956eac2686461bbcca4b66da6ea6` | 0 |
| src/background/webapi/index.ts | 192 | `d37633d7d587c976db89577690ac8cc1bc70a685a71bcc35f3cfcf866f29cd67` | 0 |
| src/background/webapi/notification.ts | 1052 | `674753a321f1b85ca0bb9a7a3a5460eeca5c77bf575d7c0cf79b9c28f244a885` | 0 |
| src/background/webapi/storage.ts | 966 | `2cdabffe21322b563838d237797a1980c0eb0c7b6dfb3cc01fb3070685344c45` | 0 |
| src/background/webapi/tab.ts | 795 | `a6ab0bb6c2b9116ffd84293d611bb938e5362426e2a08491755b8df05492ed2e` | 0 |
| src/background/webapi/window.ts | 3348 | `2fad4c5ec37107c1c0d8b446e8e1c6b2ff27dd90349b50c352b0e4e6fc61e668` | 0 |
| src/constant/abi.ts | 83821 | `516d86fbd8dcb7ddcccea8eaad837d41ec2288abf3c91e5b5b9f63e3d751923b` | 0 |
| src/constant/bridge.ts | 5250 | `a2e371eed0c2edbca57c31b2e240eae3490ccba6c3dce67bcea8418c3e88fc2e` | 0 |
| src/constant/custom-testnet.ts | 734 | `26857b0de2e926e28e2accb09607b3daaa0f669df2d9298b8565fa68284cdc8c` | 0 |
| src/constant/dex-swap.ts | 10572 | `30872e04e8d940159039849989d8688783fc03afb1dd3e0099edec84a47228bb` | 0 |
| src/constant/download.ts | 208 | `80c4d70b72a3a0f88b7cf61921f9793df0efd3c5b52731b88a058941f3724ed8` | 0 |
| src/constant/eip7702.ts | 1722 | `ac7880f6bbd6ec3f41f2174bd2461ac701db363b80ee901daf72f845b29a99fa` | 0 |
| src/constant/gas-account.ts | 879 | `1f9e06ca35d32813bf45810275da4c7f4772618a43ccd70ab71af86f8738d727` | 0 |
| src/constant/index.ts | 49980 | `cd7eec6f3c7c6918b3024a9e8c4ca7953890e20ec735335a533fb01c409814b1` | 1 |
| src/constant/message.ts | 405 | `f6504af1d484134b407f040be5e3443a4b9cf19c34a691be03e3c51714773f76` | 0 |
| src/constant/offscreen-communication.ts | 2568 | `cad239bad72083d96c3c2b224d60bb159fef75be49b5ecfe0c8dcb768ee953d8` | 0 |
| src/constant/perps.ts | 2259 | `d585bc8e5e794d1ea5dfe7f95467e4c21e9de68aa3d370991e2f67a869c454dc` | 0 |
| src/constant/regexp.ts | 816 | `c21e3d200637e12554d7c59fce3b3224c8e487f4b8a6c543d02aa9d2fcaf24fe` | 0 |
| src/constant/scene-account.ts | 53 | `2558cc2d473448c436ec966712ee5056cfd9c7cbaa7f57ef80dda492e7b33fdc` | 0 |
| src/constant/screenshot.ts | 261 | `55eeb06e571e79f61a193bdb9994c54b1b0b8dd224602c19e29a56273853326e` | 0 |
| src/constant/tempo.ts | 275 | `5f659772c2f9bbe978d8fd37568b0f94f584671841870677020e92fd34a2e06e` | 1 |
| src/constant/theme-colors.js | 9378 | `f918c72abe8fa0ed8fbd88aba9ecdfb9599d9fdb513324c8ed393af00dc7d9e6` | 0 |
| src/constant/theme.ts | 95 | `17222edd24b3c6ee371c356e0ae21a17579568c6c7cf59cf98fcbb70d7dd8499` | 0 |
| src/constant/timeout.ts | 620 | `ccdea71e2b349608496e61d040c04034a8bea2daadc367ce1561128c48b67024` | 0 |
| src/constant/txGasLimit.ts | 950 | `d4a4714d4972bdb44b515e8fad36e2523c75e72e02f78af5360077c0652e42e2` | 0 |
| src/constant/ui.ts | 77 | `82474c6135cdd92c508b64375309eb68b99d2009693fb0af65557ba6d5922733` | 0 |
| src/content-script/index.ts | 4050 | `d26c762ae5cf3f3e9954881de533fb70de32056d8edfe8f81b4d3a22eda66893` | 0 |
| src/content-script/page-provider.ts | 38 | `4c6d5a4852d13bc89bebd49192e1d7b4472c1d6d778f4961567de01ae088451a` | 0 |
| src/content-script/perps-widget/index.ts | 3181 | `31036dbaad6c92d8f70a467bd45163c3d20707d6b3f64fbd4b6d390975509287` | 0 |
| src/content-script/perps-widget/livedataClient.ts | 4963 | `cb2d59afae5fb687137765c2931c8ee3262123f62ab8f1e5daa2c452ddab1023` | 0 |
| src/content-script/perps-widget/ui/App.tsx | 8734 | `bab3c95697465d160c987dbbb87eb4fc595a05c1fd8e700a05e4953a9bc7f9e8` | 0 |
| src/content-script/perps-widget/ui/Ball.tsx | 5295 | `7c6bebdb278aadb678cab278d52ad6e4e5a28c790bacee2e17e2e275a5e40705` | 0 |
| src/content-script/perps-widget/ui/Panel.tsx | 2943 | `f6a5fc1f33349a1fbed02a4e3c72262474d105ffa8f641dc82305daa8414bab4` | 0 |
| src/content-script/perps-widget/ui/PositionCard.tsx | 3924 | `911a0e07691f506f7e6affa25d58e3ea73244a3241223d0a21ca93167e7dab57` | 0 |
| src/content-script/perps-widget/ui/Sparkline.tsx | 3139 | `ee4386645ebf197d6696c77639eccb89a729515314c9c2ef7839f4dc55fc2639` | 0 |
| src/content-script/perps-widget/ui/format.ts | 2271 | `1ed892805d24a1dfd0139f75ea985b5a62a7412b732699697f2a2f15b3ec15a0` | 0 |
| src/content-script/perps-widget/ui/mount.tsx | 913 | `0036fab194b64a02a48152cc4c5ef5ad8023c807e35e7ae62d4033e647e743e9` | 0 |
| src/content-script/perps-widget/ui/strings.ts | 404 | `d4c79a3dd01c8a95acea873fe514cfd487924a86bb6586309642945378c4165d` | 0 |
| src/content-script/perps-widget/ui/styles.ts | 10720 | `8149bd795947b41caf74b061e3c984656bd9e776e3002eff5e57812394645d8e` | 0 |
| src/content-script/perps-widget/ui/wallet.ts | 1824 | `e59777c69778712698b52fb46f8a4767ef5b2b707831ece61b9521d791b550c9` | 0 |
| src/db/constants.ts | 734 | `921f069cb0d56fbcc91abfac2f980856dcb0d15101920c34ee7cc9b2d43a4295` | 0 |
| src/db/hooks/history.ts | 5802 | `08d33f7aa855d2020734a41427d5b598d73938c003bb0330d1b8c97a60db46a1` | 0 |
| src/db/index.ts | 9570 | `9230696f2aa5f870f2751da6aa170d6c13c320cfac0ddadac65b1bdbd8e775a8` | 0 |
| src/db/schema/appChain.ts | 427 | `5e7285b23fa5b953de563390718404417569aedb842e93e296f40af747afa0b9` | 0 |
| src/db/schema/balance.ts | 1036 | `046ac2e1efdea917b07515657c4c691bb73a39070c6f0f42a046f9908e8ac931` | 0 |
| src/db/schema/defi.ts | 446 | `9459768525049e573344742a532d60ad84ad519071c8be5893ea63388635f9d8` | 0 |
| src/db/schema/history.ts | 818 | `3c7a61456254b3c97012fbe7d9d0b754dbdce25031d166917c5e02de8652639b` | 0 |
| src/db/schema/index.ts | 916 | `5406cefe08b960a7b290d1c9b5fc968545262d3bf10283e6940280ec142d87d0` | 0 |
| src/db/schema/nft.ts | 443 | `065d562c39457529a98352a9abf52fb2fd0d8950ed3fa8b203c8c872dddbdfe0` | 0 |
| src/db/schema/sync.ts | 837 | `d70556718b5e5c7acc8b87243a10c727a4d6c41e57c4953ac4f256ef08066243` | 0 |
| src/db/schema/token.ts | 431 | `0d7232b049b7d4471c7ca52283982b1c65a52a58ac14417b7a67c02e34770004` | 0 |
| src/db/services/appChainDbService.ts | 1545 | `01b88eb728d9141020bf67a60136fe79e7257f5c6cf0d72550c4b4505902bd1b` | 0 |
| src/db/services/balanceDbService.ts | 1441 | `65ac5a9cfe7be3abb6b1a8ecff9f34a14536b7d3fb6957737c04c00e8270bdf4` | 0 |
| src/db/services/defiDbService.ts | 1750 | `71f2c2d5fe991d12a8342a6fe4a8f9669e19451ff341e9e540b474617808f9e5` | 0 |
| src/db/services/historyDbService.ts | 13740 | `c8dfcb665c56217d129827bdd04c1174f191362a08090482514cd4c5807903b7` | 0 |
| src/db/services/nftDbService.ts | 1773 | `01f4aa18a6bfc8dd8724aa2340261045c279db89a646b00dc49b7b9883284d61` | 0 |
| src/db/services/syncDbService.ts | 2205 | `00d23c5e76059437b03e9d516325e1576e6d2c2338f83891298b07e96a60d3ec` | 0 |
| src/db/services/tokenDbService.ts | 1642 | `56725c7d07f02b592451c25d6a20392fbd49067ab3304afdf4f8428c137eeb58` | 0 |
| src/db/utils/expired.ts | 364 | `8e8bb30529593c0e94598ce9178eadac0f1b482b4af66532a913f0c941ba6564` | 0 |
| src/eventBus.ts | 1152 | `7560af1592a394e430788ed3f94814e0c25d56f2736278ebe52f3f15996af792` | 0 |
| src/global.d.ts | 731 | `87d45dae7d17c974ecbefa3cc6070c399090d38f1e7ee1bd9ec2573df1aab4d2` | 0 |
| src/i18n.ts | 1346 | `f0d54c3539e8a4fde1b2a21b9f54ef7d9436296b64fd1978450e11fd3e84c568` | 0 |
| src/migrations/connectedSiteMigration.ts | 853 | `ec98822d1d2b69c784707073e578c21c8b10703af123cd9a9a070f835156da57` | 0 |
| src/migrations/contactBookMigration.ts | 1461 | `ee9667f6f4871391026650ae43b383de573903007e9d886aaa428daf1aa0746d` | 0 |
| src/migrations/customRPCMigration.ts | 656 | `d1d9b3dbe552ff58d4add9ac92e7364b36cf0cedcb96ecf0a8ba637d6b96f19e` | 0 |
| src/migrations/customTokenMigration.ts | 2064 | `9b9526df313b920a56a4c20894bdffe91c6e3d56e63898717d46b95aeff6b1d6` | 0 |
| src/migrations/customizedTokenMigration.ts | 1139 | `e2200ca1ddee745b45b5095684cbaef716a784362a16908ce087a43cfeb2f255` | 0 |
| src/migrations/daiChainMigration.ts | 791 | `59fc8e719536ea2b8b57d6395f8b167d51fe0e262b306e1e08f0acfcba3269f1` | 0 |
| src/migrations/dashboardPanelOrderMigration.ts | 984 | `d5741977a954890b04c722bb09ca3565399efdf7b8d50c9889a6f935b8942a9f` | 0 |
| src/migrations/index.ts | 1263 | `e5361968e77575e6be8a4b7c8b647e0319a5bc387135e7b27082d1cf2f4981b5` | 0 |
| src/migrations/localeMigration.ts | 683 | `08a44fda2eb32b255487a540db336ac14586f2b42ee8233b803dfcacf10ad2e0` | 0 |
| src/migrations/metamaskModeSiteMigration.ts | 588 | `53d8ca1f85c3d60546b25fc702a168a3159c2364b4b51efdbac4264b7dbd11c4` | 0 |
| src/migrations/migrations.ts | 1020 | `91995d81c087efd297e85fa0a9163a49d5f73553b392dd10f2c3dde4d9c1c9b2` | 0 |
| src/migrations/siteAccountMigration.ts | 949 | `795eef92c727bba1136f8b5202658f7a9bb8ab9a0d8660a45c3118bcd2e980a4` | 0 |
| src/migrations/siteAccountMigrationEmpty.ts | 798 | `f8b0a358886bea4a6abd302b32c98b28e4d2ce84f206b05da2772ae60f23b68b` | 0 |
| src/migrations/ukrainianLocaleMigration.ts | 410 | `73d397ec1f662cde1e53408f5eeb4effdaa87285839b64a4cd20e3b8847b8f46` | 0 |
| src/migrations/userDataTrackingOptOutMigration.ts | 419 | `858b0b9523d1304043050cab729c3f6b018d824adf3a5a37b05ab0874f23658e` | 0 |
| src/modules.ts | 398 | `ad706f35fba74efa8640684975298412175b5ae9ce1502e641a1e46a392b9132` | 0 |
| src/offscreen/scripts/bitbox02.ts | 3898 | `4643e844a77b8f9e534fb3237bc2131d9e0a45d88b702d1560af56abb6a56a50` | 0 |
| src/offscreen/scripts/imkey.ts | 1672 | `4e3e58b30046963f6e2d06d11b98ad19f4c12c8ca60b98f66fe002b2e299d824` | 0 |
| src/offscreen/scripts/lattice.ts | 3150 | `6d43c36b262858dc687a0b9d8f44425bcc86023b6eb5adeb7ce57aa5c0751a50` | 0 |
| src/offscreen/scripts/ledger.ts | 817 | `04a3d06f2ab2b964ca2a2f29b82d6b6b3036bb6f21541bde85328266cbd68077` | 0 |
| src/offscreen/scripts/offscreen.ts | 479 | `a7b08786cea57b52bea3fcd5a8bd57b61e29ca0e500b62e4c00473a00333c6fd` | 0 |
| src/offscreen/scripts/onekey.ts | 3021 | `f0b037c12bebaf5d6178eca7b38c323c2e4949e9ea90e1ce2b33bcc97d639946` | 0 |
| src/offscreen/scripts/trezor-browser-api.ts | 3635 | `5e936a44c15ac2520ec5eefc7b8b0d2a77f309023c5ad92f5b6cde6d83ef4c9c` | 0 |
| src/offscreen/scripts/trezor.ts | 3928 | `c168459fdf8f60290d14750b3143b01c8c12b3c47cd82d3038c8dc229fca37d1` | 0 |
| src/services/openapi/createOpenapiClient.ts | 1334 | `e1fe1d0194cb29346784184db0ee00fc1537baf0bbe26d6524b001f85f9b32ec` | 0 |
| src/services/openapi/createOpenapiRuntime.ts | 7408 | `35b15de9f075a50171a910056bf431bbd6458d93be201d21e0c4b11ebe61b020` | 0 |
| src/services/openapi/fetchAdapter.ts | 7148 | `772b79d7eecb41dc084a77b7eff6316d866a3f187417210e42bc0b5b36b1677a` | 0 |
| src/services/openapi/index.ts | 156 | `f4eff371f427e6a9e67c735d0d3fbe58169bc38bee2ff810b1411710a1355a9e` | 0 |
| src/services/openapi/types.ts | 1188 | `f5b352f7f9cca3b96e0b31ab5a93d092342d3b1e0fc8423c4a1c2e9958b182d9` | 0 |
| src/stats.ts | 925 | `54bc4251c8e31f08f6ec7b9f30621eb49d7e2f23d16b1f21cc5cf83bf2c800c5` | 0 |
| src/types/chain.ts | 3184 | `595616dcdeec08abf169c527f863eadc19dd2e5ac891aa78db2cd6e88ae6fe36` | 0 |
| src/types/permit2.ts | 262 | `75220a27ce95cb5c811778a1f172a42bb926f9f7f07b044b154cb6e3c02b28b2` | 0 |
| src/types/persistedStore.ts | 1292 | `4953832d08eb6e7d0f53829866ddf40c938704f97e8c2b7e859a93ff8ba7268a` | 0 |
| src/ui/app.tsx | 10607 | `eb725c856f24ccde7773c06fc981b15144cfdc3e34aa86c5d99a7ecebc97e593` | 0 |
| src/ui/assets/add-address/index.ts | 2165 | `00d89daeef39f78ebae2fce3b7930de450a541c166c3b6c0af652282dce197c9` | 0 |
| src/ui/assets/checkbox/index.tsx | 159 | `adedf3fd481cbab6f32aab3068d27c05f707288e7d3640d0b594ab7e7f6cb1d2` | 0 |
| src/ui/assets/component/IconClear.tsx | 957 | `ed618e4c53d74a2f815f1dcf958d4f352e16f317ca1b3d182f24794672780977` | 0 |
| src/ui/assets/component/IconCopyCC.tsx | 667 | `5d4fc578daded5135b3548cfc967782fa1cf0919a4ccaaa33d24e4ef54587091` | 0 |
| src/ui/assets/dashboard/JumpBoldIcon.tsx | 289 | `24cc38069e64a029fa3c171c1e0b7e747a6ccc18296b02586f680b03fcfa82a3` | 0 |
| src/ui/assets/dashboard/index.tsx | 791 | `9a402cbcac55a36af3b578257aea99d66ccea286ace98d31f8eb0042b3d9c6f7` | 0 |
| src/ui/assets/dashboard/panel/index.tsx | 1415 | `4f30fdfaf02d61f6a3d0cdbad234b912a12d75fe14c647f7861f3e4f41652e95` | 0 |
| src/ui/assets/desktop/common/index.tsx | 956 | `bce1fba32c839d3627316fb005a791903718c91edd8bacaf93c00860562abb67` | 0 |
| src/ui/assets/desktop/index.tsx | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| src/ui/assets/desktop/nav/index.tsx | 277 | `fdbb5c810fd2ebd38fa5f170fd468c738c20596490990d3456a5a5c6c783d0ac` | 0 |
| src/ui/assets/desktop/profile/index.tsx | 739 | `0ec2820f55b34a5027fa90f291a56091a508ac8de2ba2e44fd834a4219fd6467` | 0 |
| src/ui/assets/index.ts | 2923 | `5f752858e3ac5e2ec7c600bc0bf02542cfa426c455cbed37f10828f0a3a1f024` | 0 |
| src/ui/component/AccountList.tsx | 1252 | `6b490d24c7ac31a4f30ee814826f25922909c91e97929374135c09aaf9d42716` | 0 |
| src/ui/component/AccountSearchInput/AddressItem.tsx | 4111 | `db1398d42a5d6fbe92452628ecfe5df7cc000d8937e115b3e354981c279a9949` | 0 |
| src/ui/component/AccountSearchInput/index.tsx | 7538 | `b25640186ceb2de0c1c329353aae901970e2933ccccff242647e0041a0f9b7fb` | 0 |
| src/ui/component/AccountSelectDrawer/index.tsx | 7824 | `a896d6573ae5bfd029d95816d706093b33d9536941b25f4c27c81d6b2ecb9748` | 0 |
| src/ui/component/AccountSelector/AccountItem.tsx | 10511 | `78164a00b4a033ffd514934c8f9fe5d7d85a5a356bc4383d362cb8a1c4ea4e42` | 0 |
| src/ui/component/AccountSelector/AccountSelectorModal.tsx | 10645 | `27a6b5ef1c53f7b2806f68cb5311b64c26f65ea124740ec1fffe934f3ca8560f` | 0 |
| src/ui/component/AccountSelector/index.tsx | 2767 | `8c15c643aaf2ff67244b28c04215c571b8fb761bf4a80caa66d24fbe7a07ef14` | 0 |
| src/ui/component/AddAddressOptions/Field/index.tsx | 2185 | `3a57514c0244f1dc21a7148dee0c7867d30e84139a84263b29ef5e0ca4b2793a` | 0 |
| src/ui/component/AddAddressOptions/index.tsx | 7003 | `092ddb4bb9dcb3bcdefb7e7fb07503c9be99ea21860ef42ca6bdaf8f2b8a60c2` | 0 |
| src/ui/component/AddressList/AddressItem.tsx | 8335 | `f235fe14554507cb4de9d548c3831b2fc37344f64f41f8b7255fc75018a9b388` | 0 |
| src/ui/component/AddressList/index.tsx | 4946 | `8b221f0225e3723583fcafbb29a38e8344038683061ad08316720c5f673a1962` | 0 |
| src/ui/component/AddressRiskAlert/RiskRow.tsx | 518 | `b7fdb531f44dc6014f8bd9c5c52cab9da1518d8defb928d470a8aa43d21fa0ba` | 0 |
| src/ui/component/AddressRiskAlert/index.tsx | 19390 | `62b91466fef7cb6c703c3e5d32db4a649b99abea42dd0b38efad1834d778198a` | 0 |
| src/ui/component/AddressViewer/MarkedHeadTailAddress.tsx | 1155 | `d91aa990c56c47d3fb34cadc7c4de63ccd1b8deb784f499fdfa725f6d7b9192d` | 0 |
| src/ui/component/AddressViewer/index.tsx | 1169 | `a435ed70895cc2ba63efad6c0361ee18df222b4c7a492f5dd3be4006a7788ddd` | 0 |
| src/ui/component/Alert/ErrorAlert.tsx | 447 | `6df9f1615a8bc64dd19b455c091f68b5cd28321ab19954ce41397f83be341427` | 0 |
| src/ui/component/AuthenticationModal/index.tsx | 212 | `c25e6764cdfc2671bf293c94d6aa283902e2fb52062dc33a13c836e5786bc42f` | 0 |
| src/ui/component/AuthenticationModal/modal.tsx | 4147 | `ed830723e61630cc4f2d07ebfa08cab23a41e4e4c3ea3b57c72455af10eca19d` | 0 |
| src/ui/component/AuthenticationModal/popup.tsx | 8076 | `63644097911197c32f2b5b6a8f1668ffd30e0cdae0cbfbf4f081fdc83b3bc297` | 0 |
| src/ui/component/AutoSizeAmountInput/index.tsx | 1723 | `ecd8cb98dab6ad3935e1c45c6f3d787637f77b88a6b39db20f68d4c1ae25a7f9` | 0 |
| src/ui/component/CexSelect/index.tsx | 2358 | `2d121b7c5fc945a538d03892b6a74ccfe2fde9f7f6b18aa82f021449c6b88591` | 0 |
| src/ui/component/ChainCard/index.tsx | 2058 | `6f78d940d315514be72875d9941b312fbe3fdfd0ae91af342bfafb4c0c03e85a` | 0 |
| src/ui/component/ChainIcon.tsx | 5955 | `8f9cedf8261c531153939884c28ddc2fba97f76973bb88a270abe429eac821e5` | 0 |
| src/ui/component/ChainSelector/InForm.tsx | 9529 | `6488f3d27ae1f1f9a0f0ee7f1904715fd739ee206d98fc2c40d063528f348540` | 0 |
| src/ui/component/ChainSelector/LargeModal.tsx | 7286 | `0746cc510277e29f9c114c16994c5ea3e84dcb126dc14cca70afe25abd965074` | 0 |
| src/ui/component/ChainSelector/LoadingBalances.tsx | 1835 | `201bcd11cd58e09e27f823eff1cbd46eeebf6284dfad3ff08c3640941f4efd87` | 0 |
| src/ui/component/ChainSelector/Modal.tsx | 9414 | `0faab4fe9f5dedf4f042f6a559864bcdaa0c0d05fd05932c7f393c17f9e6fff8` | 0 |
| src/ui/component/ChainSelector/components/SelectChainItem.tsx | 6675 | `6e7361ff62d725a6613dfd259c993bbed356cdf4fa9f4d197ef873aeca399413` | 0 |
| src/ui/component/ChainSelector/components/SelectChainList.tsx | 4484 | `097cf4b495de86f28f82d6c91f1f7aaf5c9ef91f6cb389514f8a9b6901383605` | 0 |
| src/ui/component/ChainSelector/components/SortableSelectChainItem.tsx | 839 | `e58e02222e092ab340fe186c20001ff0def0aad367f72dc7194baf2f2e852b5e` | 0 |
| src/ui/component/ChainSelector/index.tsx | 2774 | `e45c3bcb992b2c85beade5f372f632c06d4f9821e6ab84462070cc00525b759c` | 0 |
| src/ui/component/ChainSelector/tag.tsx | 2008 | `be3fcc7ef5320e9e0dabd75779e5ee877bd9c481520141dd70796a1f8db90893` | 0 |
| src/ui/component/Checkbox/index.tsx | 2004 | `1b668e69c326d5e8eef191de767bedf02ce3026f8d1f4389841a524d3fbd02d1` | 0 |
| src/ui/component/ConnectStatus/CommonSignal.tsx | 1481 | `9f1bde977e5ccf0277450d10a17f5941f07de6bcdaa591443478454520c52fa8` | 0 |
| src/ui/component/ConnectStatus/CommonStatusBar.tsx | 927 | `b0abf31b5c622634d80cee1db17db223a9025d1b44970e6d3e123742a84cc5d3` | 0 |
| src/ui/component/ConnectStatus/GridPlusSignal.tsx | 523 | `41b5f775bd01e9c6028b98689b6412318e43eb2e650abce620d546c22c83003e` | 0 |
| src/ui/component/ConnectStatus/GridPlusStatusBar.tsx | 1136 | `1d6e40972a453dd23f1fc6b5785ba94c96277a538e1aa26ac83762193be20579` | 0 |
| src/ui/component/ConnectStatus/KeystoneSignal.tsx | 450 | `38ed956eba607d36d1be39ef4434c23c5088f994bc500dd47facf71577bf22e4` | 0 |
| src/ui/component/ConnectStatus/KeystoneStatusBar.tsx | 744 | `6346336362f4000e96a3cfc286cc4f72d533156eccf2f54e8bd45ad3afedafae` | 0 |
| src/ui/component/ConnectStatus/LedgerSignal.tsx | 515 | `51a6003a78e0a5d90010bddef7cf42e580a87172edfe3a2051169c6820e43479` | 0 |
| src/ui/component/ConnectStatus/LedgerStatusBar.tsx | 730 | `b09557e4e7885e5b31088f972cccc21950a75a713ef644bae9c46cdd91b7de3d` | 0 |
| src/ui/component/ConnectStatus/useGridPlusStatus.ts | 1483 | `7f3b79471b7b52c33b315d61189b01915e8c1d1ad743978cb9921e5912760f9d` | 0 |
| src/ui/component/ConnectStatus/useImKeyStatus.ts | 955 | `be08b6483cf38faa151b5f89dc02c82459eb118f4aa818057211479e22035f2e` | 0 |
| src/ui/component/ConnectStatus/useKeystoneStatus.ts | 941 | `bafb958b6bb100e301e8ca01c8f5b189664a5533e86623262a9b18f64d5ec373` | 0 |
| src/ui/component/ConnectStatus/useLedgerStatus.ts | 954 | `77b4cbd0b67ff6e2febb5c070a0a9cbe27fbbbafe648b74d11d0cc1f96fb3b26` | 0 |
| src/ui/component/ConnectStatus/useOneKeyStatus.ts | 1182 | `28cd80c631b72028d7ae97d92caf314421fe83a3c981d67518a795f035e9c4d1` | 0 |
| src/ui/component/Contact/AccountItem.tsx | 4730 | `3e812ac7c0d514de71eb151104fe488da5b34f84f1f2adc9fc315a20f44bbe37` | 0 |
| src/ui/component/Contact/EditModal.tsx | 3309 | `5a945409aae5790851451691c33a0a1ac8f28a8db6415b7c29962fa201ef9f60` | 0 |
| src/ui/component/Contact/EditWhitelist.tsx | 4570 | `00770ab812a63058e74af06dd40276f8e9443251190eb4df674005167c713c4f` | 0 |
| src/ui/component/Contact/ListModal.tsx | 5379 | `1453eba7a432421ee49b7f8018ad09de1ed8d28085a0b5e24d42edd02279da3e` | 0 |
| src/ui/component/Copy/index.tsx | 2141 | `822c55ccb5fe7f9142a7eb543e522327c7de3491f1b666b08cdd44b9b942fe63` | 0 |
| src/ui/component/CopyChecked.tsx | 1539 | `649804f8c6cf1e78bdd26ca8ef40e5a9564369b3de67c359882451cd858bc4b7` | 0 |
| src/ui/component/CurrentAccout/index.tsx | 2230 | `b51c1b7b714055e99c59102ff1da0f9993d486119d80330928e8a01d72e0b95a` | 0 |
| src/ui/component/DebouncedInput/index.tsx | 1287 | `d55f0d2c65dea2f6262fb75ca2fe264588469f5e0a3f9b11bd3f3db6c4b4188b` | 0 |
| src/ui/component/DesktopAccountSelector/index.tsx | 16457 | `35a83f64ded4f48bd70daadad186afb2f011935fac6bbec2b3fcf00370494870` | 0 |
| src/ui/component/DesktopNav/index.tsx | 7174 | `27b5fe44d8afb915efa4d1a94c30103c83c52aa23622efa1b11c17dd4036fb9b` | 0 |
| src/ui/component/DesktopPageWrap/index.tsx | 1355 | `98a7e47ff639b41c7ea99b731585d6fd24ded4fcba0b4ff3421d1e269eef5f4b` | 0 |
| src/ui/component/DesktopSelectAccountList/PerpsAccountList/index.tsx | 13153 | `a56f3a5dc7aab2e3563ea47ee402f1c694d9247417fa041537812a710277dc78` | 0 |
| src/ui/component/DesktopSelectAccountList/index.tsx | 9204 | `a78818c2337e7bb1fed8a447ee2c41220f5fb65f832cd9b77f835b6bb0455c03` | 0 |
| src/ui/component/DropdownWithMask/index.tsx | 1915 | `6deadd5aaca8f82f9310726d6646e89a20ba4328dddc0fcb32dea376fb2e05d4` | 0 |
| src/ui/component/Ecology/EcologyNavBar.tsx | 1796 | `a4d1c2356a24f686d0c442a05f876f279f259c4209f0d3d6adcb3623ac291843` | 0 |
| src/ui/component/Ecology/EcologyNoticeModal.tsx | 2345 | `3d412fed0aa9bcd378fd5a69667f5b9458a6f66bede06568ba7f77996edd99a6` | 0 |
| src/ui/component/Empty/index.tsx | 707 | `91577b44642798e6e95ae417b9dd761d11ca70c467917920805486b474be7a7d` | 0 |
| src/ui/component/ExternalSwapBridgeDappPopup/hooks.tsx | 2648 | `7b448f348956f0e072661212a32ee7a55f62d09c10017039d20035be1177327a` | 0 |
| src/ui/component/ExternalSwapBridgeDappPopup/index.tsx | 5200 | `2168fdcb13f02f9e470b8d7e67dacb50eeb46cc5acb79036edc2af7592487b82` | 0 |
| src/ui/component/FallbackSiteLogo/index.tsx | 2872 | `b8f01b7ae5675290ae4f2568642b358b92479402550fd2ee7b17378d00d9d321` | 0 |
| src/ui/component/Field/index.tsx | 734 | `e9e365901c03e9de61425cd3f38dbc38a1ab93debd923c450f4293ef36991ed8` | 0 |
| src/ui/component/FieldCheckbox.tsx | 2055 | `fa3b5020f064d9d7fe40c9ceb15798d17a5c3cc8abb7592c23ed69115369c7c6` | 0 |
| src/ui/component/FullscreenContainer/index.tsx | 1812 | `9660d6f7d2f0a53e0712c0b69b636667c9b11075358bb0a6489f32def375e29c` | 0 |
| src/ui/component/Item/index.tsx | 4959 | `5184b12e013e4457bd2b46faff560671d722b1133e9850be575db1117584388e` | 0 |
| src/ui/component/LangSelector/index.tsx | 2462 | `686f6c515c6265bba36cee0c20e8e3c07cf8b9f723ea612bac5fe9e84a785de3` | 0 |
| src/ui/component/Loading/index.tsx | 642 | `f98efe0dc8e0f625c24d8416d21cf050ba7e207767ac134550d3e7fcbf1e260f` | 0 |
| src/ui/component/LoadingOverlay/index.tsx | 562 | `f21efee75b5bae91171af78e3075d81395fa22556d4cadcec0819b34eb1868c8` | 0 |
| src/ui/component/MiniSignV2/components/GlobalSignerPortal.tsx | 643 | `7d1006210d7e231497fd505c754b754b775cfd80d72f736a932ad19f8a9c8d2d` | 0 |
| src/ui/component/MiniSignV2/components/GlobalTypedDataSignerPortal.tsx | 321 | `96c745a5e3962cd67679df7c5c91fe8660ea46517c7c7b2da073f01a6eab68ca` | 0 |
| src/ui/component/MiniSignV2/components/MiniSecurityHeader.tsx | 1943 | `c183e16c3aedebb2e9d87cf41dd45351d6309666071ad0fb61db1be7e67e737a` | 0 |
| src/ui/component/MiniSignV2/components/index.ts | 195 | `287f5a6cb2eebb55779e3057f7bc6fe718d7e9b01ad12d5dac3aa94bd0e3fd22` | 0 |
| src/ui/component/MiniSignV2/domain/ctx.ts | 1624 | `f06327e9c5cd0cb37eb4539a9f6c398f1410459e2b482ca98392a6e42bde6648` | 0 |
| src/ui/component/MiniSignV2/domain/gasSelection.ts | 1911 | `781cab807ef78080fffd07f4df743cf6c9242f3b07d95a3dde42303f2f4511e1` | 0 |
| src/ui/component/MiniSignV2/domain/index.ts | 80 | `e65cba0a38059b34cb10cdf7140b438b0d977ca241a73ee053ea33ccd0c4287e` | 0 |
| src/ui/component/MiniSignV2/domain/types.ts | 3695 | `a094a9dfe33461cecd00f18cbc43f1e764bde516257177c34971422c57bcc883` | 0 |
| src/ui/component/MiniSignV2/index.ts | 109 | `3565075d790404cffeb14ff089fd5420ce29f6de2d6d207ebfb75352b2e392a6` | 0 |
| src/ui/component/MiniSignV2/registry/index.ts | 1710 | `a3d0068e2e47a5cca9b1dbf12cc02573ddc688d5613311465f3aadd54f8abb4c` | 0 |
| src/ui/component/MiniSignV2/services/SignatureService.ts | 4554 | `4845c17b582cac9437a20b8fb82c4034957188e2b933153d69d09d49033660f4` | 0 |
| src/ui/component/MiniSignV2/services/SignatureSteps.ts | 37935 | `7982ccbd50c905393302d52968cafcff26536327b0fa5fa2df7cb8eb86c854cd` | 0 |
| src/ui/component/MiniSignV2/services/index.ts | 106 | `bb7e450b4ba6f1c958fb3188641e1ecee63d5b269d98431312195ff5d3f5b4c8` | 0 |
| src/ui/component/MiniSignV2/state/SignatureInstanceContext.tsx | 717 | `a0cb105d5ddcb4a404e32701e5c3a6a21d767b47cc55b17c80cb51f012eba0b6` | 0 |
| src/ui/component/MiniSignV2/state/SignatureManager.ts | 26418 | `22fccf60eec24782934da5889176c09d47f55cb9197a426b15ec53f6ed9ccbbc` | 0 |
| src/ui/component/MiniSignV2/state/TypedDataSignatureManager.ts | 7849 | `aea652e82dc029a53da6bc1d0756343f4a062f7fdb217cbda03e30cdf3b62504` | 0 |
| src/ui/component/MiniSignV2/state/index.ts | 521 | `212a3d0dd08dfc9c5a6384d6d21cc7cbe91d2c0a5d8acf9d9629c0b866fb6b63` | 0 |
| src/ui/component/MiniSignV2/state/machine.ts | 3972 | `2ef4d535767942ae0ca0d7170ff1527b64c4bdd5e9b7f8b517cc59640f586754` | 0 |
| src/ui/component/MiniSignV2/state/types.ts | 2137 | `83697fe58744bcfe55b66e0e85ff547a75f3bb8084c7740b89a21d5ff32596fd` | 0 |
| src/ui/component/MiniSignV2/state/useSignatureStore.ts | 1231 | `2b9f4ad994337b435b71c7ee1e7f6b67163cf4a036246db1575af674f5a8cdae` | 0 |
| src/ui/component/Modal/WrapPromise.tsx | 1100 | `2ac87c671d6e363e1e8b3f6f9b6b792128ebc489e42e2bb554ecf2b260b8a17a` | 0 |
| src/ui/component/Modal/index.tsx | 829 | `2b72dc46c6370b1d1be5c3036e2708e7d6d53a2e2d39efbf0f9b68d6e0751f7a` | 0 |
| src/ui/component/ModalPreviewNFTItem/index.tsx | 4255 | `68a395c87843674a72f14a42cf9f077ff038d9983426d7a4bd952cb0b0986d24` | 0 |
| src/ui/component/MultiSelectAddressList/index.tsx | 2867 | `402f16fd1d92bcd8728f8f620bcc561c413f555d0078f5c62f32e21254ee755d` | 0 |
| src/ui/component/NFTNumberInput/index.tsx | 2361 | `439615e334216fcb790d7fc612a775c276dba430b019845f2bf691191a8f772f` | 0 |
| src/ui/component/NameAndAddress/index.tsx | 4987 | `536e5e6d5c3b17bf2d26a366219548f3873a338eacbc5b277bc57116f1839d72` | 0 |
| src/ui/component/Navbar/index.tsx | 1013 | `9a873ca577fa83fbddde895cb47f7e3fd79d622bc6805d4c44977163e1b6a1ca` | 0 |
| src/ui/component/NewUserImport/index.tsx | 3447 | `bf61be5fa56af8c96446615806e46478fc98ac85e523951bbc31f21786b84361` | 0 |
| src/ui/component/PageHeader/index.tsx | 6646 | `547dea6ca5daa6c88e992dc957f3c2a9ac09e8f3b0a4cfe078e047fb5b64ac10` | 0 |
| src/ui/component/PillsSwitch/NetSwitchTabs.tsx | 3060 | `5c451214edf34559dc9f5d56c8812dffdefecc5d18e822663cb6713e55868dcb` | 0 |
| src/ui/component/PillsSwitch/index.tsx | 1332 | `30fca7d03038518790c88b575637be2185ca1e93fffccd517e4630740ba95d7b` | 0 |
| src/ui/component/Popup/index.tsx | 2164 | `af60350bcbf59b623b086fdb6d807e7f4be81dcd20c4b3438a6e25f431b30217` | 0 |
| src/ui/component/PortalHost/PortalController.tsx | 1510 | `ba8ef1049a371baf61bddd1d108c9d7c8c419a8d84d9af603cd5920a91405a9d` | 0 |
| src/ui/component/PortalHost/index.tsx | 456 | `a4be284ff47dd43cfe522df1f62b115bb6597ac788e7d53b6ca58ae1f4ae5d26` | 0 |
| src/ui/component/PortalHost/wrapPromiseOnPortalHost.tsx | 1682 | `1f3a78eaf640e212d28e318041646bace2bc8e97fbb88d6e91f1291d5de59a57` | 0 |
| src/ui/component/PrivateRoute.tsx | 1284 | `eba7541cb339b268364abb3821d57a33cefef239ed733f9f7f5214937a40e432` | 0 |
| src/ui/component/Progress/index.tsx | 413 | `cf7f44293764e0735b045c1e48e7612d1eb5d558363c45aad23738de42a32b42` | 0 |
| src/ui/component/QRCodeReader/index.tsx | 2579 | `72b77de12d9c8dacd858dea0d53ed3730a3d7339060175c075bffaf200ed9e12` | 0 |
| src/ui/component/RateModal/ClickableStar.tsx | 1405 | `cfee2e701277a92adb11ba65d60f47eaebd30930cda239a30bc58a9a585394e1` | 0 |
| src/ui/component/RateModal/RateModal.tsx | 9385 | `3a2395ee02156f649a46904a938cc7189e60fe5ae4a2ce024c13d46e654ab65e` | 0 |
| src/ui/component/RateModal/RateModalTriggerOnSettings.tsx | 3767 | `515f0441a47153f227e87b6fae22adbe278278cf19df4165d5020b5668ccdbbb` | 0 |
| src/ui/component/RateModal/hooks.ts | 9621 | `4a05f5c864f73b3071c065effa4f05b6f0c9f3d915c6a1d2803b1ae9e43302c0` | 0 |
| src/ui/component/RiskWarningTitle.tsx | 538 | `9485c69b9c4f17ab900ce79342f1722840dc879f31e91a96ab99055408e5338f` | 0 |
| src/ui/component/ScanCopyQRCode.tsx | 5516 | `1f1d5c425c8e8aaa797857ce34c6c309dbf38870551861cb29d0b9e83194f8e2` | 0 |
| src/ui/component/ScreenshotContextMenu/hooks.ts | 4388 | `b4aa9dd0f4df499ceaa8c28c382ee470c0208d6bc0aa1f3b89e21d8359e41297` | 0 |
| src/ui/component/ScreenshotContextMenu/index.tsx | 10515 | `8a95bcf555418af85834f5b8c2b5eba8961a27b1b3219bae92d491a90ddbc409` | 0 |
| src/ui/component/SeedPhraseBackupAlert.tsx | 3501 | `02cf001227a023ea9233697625a67f44cfcfca1c22956b1c7464dc1cea5df01a` | 0 |
| src/ui/component/SendLike/AddressInfoFrom.tsx | 3841 | `d591355ba8c9075d861b5bfaa6867079edb3679f17e6e7213021c45a2386f849` | 0 |
| src/ui/component/SendLike/AddressInfoTo.tsx | 9607 | `c2379ad9b22dfa5868bf724726ce66a8928bf58b44e5110411eda8a2c1a48ac3` | 0 |
| src/ui/component/SendLike/Slider.tsx | 1448 | `cd9de9a1f4abd18900cbfe1b7fdbcfb0d826cb376f12308ce64f6e512dd372a7` | 0 |
| src/ui/component/SendLike/ToAddressCard.tsx | 2769 | `9d45f7f3e70048d937b533f2443474bedf0ba3b3d7bedc6585ee4a230c9c47bb` | 0 |
| src/ui/component/SendLike/hooks/useRecentSend.ts | 7896 | `8a84f5133139c8659354836c3793a56a6898d1f4e6950c0ae9e4f522ad50595b` | 0 |
| src/ui/component/SignProcessButton.tsx | 2159 | `ec2f6dbf010852153c8c83e38f915d8a0054f528daaccf0c6f5d929276ea0eb2` | 0 |
| src/ui/component/Signal.tsx | 738 | `da9ac42f41c1fbf9daab6ea23eb12682628e0c815603c17167aa170839508fb6` | 0 |
| src/ui/component/Spin.tsx | 938 | `67b22e4746b4d506f262bf0dda62cf70cacab796723d9127f75f1d5223302664` | 0 |
| src/ui/component/StepInput.tsx | 4883 | `9bee0da150d895b7faa8b45a778855cb7924f1462f78baf6d09cfc1e5d56ff69` | 0 |
| src/ui/component/StrayFooter.tsx | 2743 | `0bf880afd3d0b4dd1073b6fe9cff7cdf2771e49fdc270a806c10fd5b4293e223` | 0 |
| src/ui/component/StrayHeader.tsx | 708 | `1b10bf72deb8e2159dd7fe34420518a4bb91f69ae811b1ac394721503172083a` | 0 |
| src/ui/component/StrayPage/index.tsx | 5559 | `eb4e4b842233f615f96012629b9f40371dd3c04d7542dfd1792e065415eff80c` | 0 |
| src/ui/component/TestnetChainLogo/index.tsx | 464 | `8608ad974a1862f0c48697807bee86e52e5dee2bb27545d610ec116ad03ff126` | 0 |
| src/ui/component/ThemeMode/ThemeIcon.tsx | 1262 | `e5bffb984d0a7b5b169ea79290fc1c99adc1de0a897be75a9e88651ba3120661` | 0 |
| src/ui/component/TiledSelect.tsx | 5514 | `944a895b88c989f273a1fa512687f3e00f4ba6513f152b238b32cac542220caa` | 0 |
| src/ui/component/ToConfirmButton/index.tsx | 10047 | `2e9ed95f1037af1699b28470fd2adeeeca0a28203f216843d1ef24ddfc274eb5` | 0 |
| src/ui/component/TokenAmountInput/index.tsx | 19561 | `2610932b66b17935193e13647637fe7c11c25056ce892b84fb1ddd405bca5b0e` | 0 |
| src/ui/component/TokenChart/TimeTab.tsx | 1667 | `239b78a240120509796d4407c62a065f73ec2d3aae915454af83fe6dfe9fa5ef` | 0 |
| src/ui/component/TokenChart/hooks.tsx | 4854 | `e309b3b3aa8124a45760b9df218399967144db9b34f84538c9cc3b8026f3bec5` | 0 |
| src/ui/component/TokenChart/index.tsx | 11532 | `e8b4289768f9a3443a1efc2c58cb2ea91df15cb2a1987b43aee29561f2a6408c` | 0 |
| src/ui/component/TokenSelect/index.tsx | 13769 | `bc4bd44d3445fd159cc7cf971adeb668a03f5755372a2be1945d5aa9b77209c0` | 0 |
| src/ui/component/TokenSelector/CexLogos.tsx | 1833 | `fe46d9533f4ab1c6f47ef022aee838e02195bf886b004100a6fe7a34270da2d7` | 0 |
| src/ui/component/TokenSelector/ChainFilterV2Line.tsx | 7601 | `8d092f63873a109fff40d3c9aa6b8e12d0111212eda123ccbeeedbc3e1d408ab` | 0 |
| src/ui/component/TokenSelector/ExternalToken.tsx | 8991 | `afa4a09c7013e8ddb844a24bdf25286f02d56a16875879266308b4a8fde20308` | 0 |
| src/ui/component/TokenSelector/context.tsx | 714 | `42456e79893f5fad761758d40774d08a37d7c159be36c1cdfeca46e1c83eb0af` | 0 |
| src/ui/component/TokenSelector/index.tsx | 27128 | `3998b7db52f6149beda4dbbe65b659f3b15a158c4cf1d77b525313e114d14f9f` | 0 |
| src/ui/component/TokenWithChain/index.tsx | 3850 | `4e1075329a39b59810780d12697a7eafcdb128aaf77fe112cd6d4471b05f07d6` | 0 |
| src/ui/component/Tooltip/TooltipV6.tsx | 6225 | `d44f673fae63002f00cb590e230f914e49ded728a9e2a016322fc5e0954638ce` | 0 |
| src/ui/component/Tooltip/TooltipWithMagnetArrow.tsx | 3015 | `a0d674be01041f424c0001f948283f02570647462216b0769445d0b544b59e36` | 0 |
| src/ui/component/TxHistory/TokenLabel.tsx | 1972 | `1ef35a3a553090448cd7b11785674fbccc017c8104047dc93b606ec26d40d839` | 0 |
| src/ui/component/TxHistory/TxAvatar.tsx | 673 | `3f0ed7b78cf247169b936d15a1903a47f9f9cae2ad62babe917189433b7f253b` | 0 |
| src/ui/component/TxHistory/TxChange.tsx | 4809 | `fe0a2fc895254c28c85214ff46f78a58a338c21a1e4bdd758eb32d77735a59d9` | 0 |
| src/ui/component/TxHistory/TxId.tsx | 1290 | `14047726672fb407a03cdac298112ae2690c818aa8ae04d001591947794d3f09` | 0 |
| src/ui/component/TxHistory/TxInterAddressExplain.tsx | 4196 | `0b93e6c830cd6ecf3470fc0f02277d1ff9f7b80723515648318730b8fa861687` | 0 |
| src/ui/component/TxHistory/index.tsx | 144 | `1eae481267e2c91a1c415bc682d1b0d3f712bd9b12681b1face5192ea90c6af4` | 0 |
| src/ui/component/UnknownTag/index.tsx | 927 | `40f2164e82f92848aa4916c76009fcce3af39d64870413d0c78aea84b32bcd8a` | 0 |
| src/ui/component/Uploader.tsx | 2280 | `0cd9e315dc18d763bcec13eea1ec935971c1a046ce2ba1f22d391548ee92c7c0` | 0 |
| src/ui/component/WalletConnect/ClockSkewWarning.tsx | 634 | `bc658407c2a620ababfa22ddf13a850596e0a5cd37f3b2b0cef638792d3a1dd3` | 0 |
| src/ui/component/WalletConnect/ConnectStatus.tsx | 3898 | `a22ffe81deba0310745fe261e121182c847c81215478b88eaa1460992afbf561` | 0 |
| src/ui/component/WalletConnect/ReconnectView.tsx | 3105 | `0df3e07bcd3c4ad1cec7131a7d38f1e62c8e732312eee7018d961faf4b00a084` | 0 |
| src/ui/component/WalletConnect/SessionSignal.tsx | 1295 | `32cb647a13d13c3e6163e8e260455167b816525e3f9c3139a8e496006235aaac` | 0 |
| src/ui/component/WalletConnect/SessionStatusBar.tsx | 3556 | `1b6678cc2ce2e22ffd784c2779bdbb14ecb839c05bce2d5bf3aa8286ab2660a0` | 0 |
| src/ui/component/WalletConnect/useBrandNameHasWallet.ts | 136 | `b795e8648fbc9cc17f5049b64a9aa94b8687adc50d0514f2b2c3d1354be7c959` | 0 |
| src/ui/component/WalletConnect/useDisplayBrandName.ts | 1113 | `5338ab94dfa5d6edad73dc0b427fb7c2c3814ea4f9851517ed7ce13c38607ce0` | 0 |
| src/ui/component/WalletConnect/useSessionChainId.ts | 1304 | `a6aef5f9f78367c2f579f0813f6d203e5f660c5e51dda97ded8c08d0ab45b5cd` | 0 |
| src/ui/component/WalletConnect/useSessionNetworkStatus.ts | 1487 | `facb1ca23ae845f90646937a143b24053dbffae347bbb5a087dc0dd6411b9dbb` | 0 |
| src/ui/component/WalletConnect/useSessionStatus.ts | 2979 | `f61cdf95f94047132c701f7be634e35eb31de6eee27a245ce69ea401cebf0e4d` | 0 |
| src/ui/component/WalletConnect/useWalletConnectClockSkew.ts | 1720 | `3db03d302b47cee7effad74b341edc09a1d939559f7a690d207d04ebf7d1fb9c` | 0 |
| src/ui/component/WalletConnect/useWalletConnectIcon.ts | 1297 | `3a9294b0a6d807fc47f58f84d16668496748cd448b1834a489f2c76b9c3c907e` | 0 |
| src/ui/component/Whitelist/Modal.tsx | 9574 | `db1b70b3be884ce39695f6f094ad1427f4faa8614c2ceeed1958f90ed004848a` | 0 |
| src/ui/component/WordsMatrix/MnemonicsInputs.tsx | 33027 | `7b67f8f5b25e918e49b85fb27c0d99aefdcd39a08cf40454a91e6de8c24a8d8d` | 0 |
| src/ui/component/WordsMatrix/index.tsx | 4259 | `71010690f9a57e2b3628b6426af48831a261de049c1fca2959103cb28770ee53` | 0 |
| src/ui/component/index.tsx | 1819 | `8b95aeb4ea073832d03bb54956adc80e01c2f0801368ecd6be8abde1b95e0755` | 0 |
| src/ui/hooks/backgroundState/useAccount.ts | 3381 | `641209b239c13179ce716de86992e185d4f6ba63851d4af4ae3887f4f95470b5` | 0 |
| src/ui/hooks/contextState.tsx | 851 | `921f27ec0668a3b8891c5a57d84755861138da50633e886eda911aa6aa78232e` | 0 |
| src/ui/hooks/miniSignGasStore.tsx | 1446 | `c5d8bd1204a2f2d4c94898b6a2cb408180ff7132b4cee755de685cef57e3c090` | 0 |
| src/ui/hooks/useAccounts.ts | 4932 | `705ac903511812744931d4e7b0edf77d0504af2d7d3164b5e08e431bf78f6da5` | 0 |
| src/ui/hooks/useAddressInfo.ts | 6592 | `9a658d1d6f639d19725b41b6fd0bc87738afc626c6469cb2e40bafdd5c5c03bf` | 0 |
| src/ui/hooks/useAddressRisk.ts | 11679 | `e7780d1d2fd162e3444d2c00ad55d6185ba746c162796134f976a737dd6f32a6` | 0 |
| src/ui/hooks/useAppChain.ts | 5789 | `a73158bc28476c1a58aa0a45008f43487ebafaf92dd62eb8090d080b910dadc5` | 0 |
| src/ui/hooks/useApprovalDangerCount.ts | 1253 | `15cd408731b263ceb91c926078368b6862ff414268fc044efa1ff55cff2f1bc7` | 0 |
| src/ui/hooks/useAutoSizeAmountInput.ts | 3531 | `a62d417b7706e8ba3c8b99d4475b28d9997bd3846b6547d084d2657a85ad80c3` | 0 |
| src/ui/hooks/useBalanceChange.ts | 1276 | `d418f8382956a849454bce1724b4dd7c85c116ed7ba063866af9180b428b448a` | 0 |
| src/ui/hooks/useBrandIcon.ts | 1931 | `f05d706c8f88861404c0d09cc43a17799de1b06dc2d56ea4756621b350574255` | 0 |
| src/ui/hooks/useChain.ts | 2924 | `366d08dbd52157936b83e0f697352a7c6f017eb247af805441bdadaf2cbf5629` | 0 |
| src/ui/hooks/useContact.ts | 1183 | `18d0ffe0050eefa1e3580d12fca8c062731c8d5688d4843b48651c0022f03391` | 0 |
| src/ui/hooks/useCurrency.ts | 1228 | `8f1a759b11d232bcdd968efbd0982f7c818f6e19beda8e4c0b8fab13b2e7d6bc` | 0 |
| src/ui/hooks/useCurrentBalance.ts | 5291 | `a65255e8de571e6d7e15e7ba1eedbe51166438c728ba764fa53582ebbbd38c71` | 0 |
| src/ui/hooks/useDebounceValue.ts | 1911 | `efef1beb9e452705aeb42e312f095bd2e8b0437f101c9b572bf71c726b45b40b` | 0 |
| src/ui/hooks/useDeleteHdOrPrivateKeyringAddress.tsx | 9426 | `549dc94e740146c36e9a623c4ccbc1585473f5356c7c912c1e207b47b5dd9f74` | 0 |
| src/ui/hooks/useEnterPassphraseModal.ts | 1605 | `23d7ce1e3be738bce103595dbfb6372cd23742feeb9f3193b2ba02140ed18c23` | 0 |
| src/ui/hooks/useEventBusListener.ts | 446 | `5b18b4f13328ab691e2cee818db1c2032fbe8aae52bb7385cc71072f8e964f55` | 0 |
| src/ui/hooks/useExtensionUpdateSettingsCard.ts | 1394 | `ca63f578486c111cd470f1f0b9768cb7bde567f3b3f5637c7e1c531f0d63e464` | 0 |
| src/ui/hooks/useExtensionVersionInfo.ts | 771 | `f51459d473032b462dd87d6e42f1f92c571b2d84c4315aa3b85f454583427411` | 0 |
| src/ui/hooks/useGnosisNetworks.ts | 566 | `a57efa7ccb6b5bfd8cd5d8ee7ac80832639a2aae9a30129064944fa9378259d4` | 0 |
| src/ui/hooks/useGnosisPendingCount.ts | 793 | `0b2df38f8aafbb0ab67b28a9844b55ee4c053f1e6d409a9d4024033afe6361cc` | 0 |
| src/ui/hooks/useGnosisPendingMessages.ts | 713 | `63ada536b4d4924c1fc70e5192969fb6dc36eb6100437b1a65fb4363f1030436` | 0 |
| src/ui/hooks/useGnosisPendingTxs.ts | 820 | `9a1e91efe484020910047acac14658321569e4f77ea95e83ef9027600f76289b` | 0 |
| src/ui/hooks/useGnosisSafeInfo.ts | 740 | `ce256ea609d3e6390d176440d7ec96baa4e2d661c60f81964bd6bd04f3a25b71` | 0 |
| src/ui/hooks/useIntervalEffect.ts | 715 | `dee9c5f7142c88316791efd563259028f71497fea4e399af3253f6a92c46cc01` | 0 |
| src/ui/hooks/useMiniApprovalDirectSign.tsx | 4164 | `c725f4d3cc2fcd300fbe7d7ada87b897d7df847d73a3c33dd1f7467a08e6ff89` | 0 |
| src/ui/hooks/useMountedRef.ts | 288 | `7af3936fe236ed37b2fd3885d80939b31e8ecde5493de99bfb63d139bd53dd3d` | 0 |
| src/ui/hooks/useNFTCollections.ts | 5669 | `32cbe2f263655ec4e937b1faf511723681eb6757817ab1449dd06c7f25dfeb5d` | 0 |
| src/ui/hooks/useNFTListingSigner.ts | 6865 | `3a8b74aea0903cea6245441c8d36e934d1f0a0cd40352ada74789a98db9a6720` | 0 |
| src/ui/hooks/useParseAddress.ts | 2839 | `d3596c1ff5b442ab74a5c0d9844e8d97ad98ffae5971669f8a37d537d50a5167` | 0 |
| src/ui/hooks/usePopupContainer.tsx | 964 | `729fe3331e2bd264eb6ee35b6a92f819c559da968ba0eb74304abd4bf52837da` | 0 |
| src/ui/hooks/usePreference.ts | 3668 | `08b4407be6e013915a7ad9026dd362b3330f166f2097d2ef17d8edd34f94123b` | 0 |
| src/ui/hooks/useRefState.ts | 506 | `c889d828f97e3e1ed4a9bb3730962af33d08da0938078115f197a54fdf065f31` | 0 |
| src/ui/hooks/useRemovedTokens.ts | 1102 | `c35957faf09fad64b56945a40fa71e30c8fb368f1757f09855cb2137fc18b334` | 0 |
| src/ui/hooks/useScreenshotContextMenuVisible.ts | 1863 | `a611149d6f200dc677031c4d9310561be29c112c451bc52532224a23d5d9996b` | 0 |
| src/ui/hooks/useSearchTestnetToken.ts | 1177 | `0c166ad669c519641910820b8d2766a0782ac0877fb760f9a8621d9501f99fd9` | 0 |
| src/ui/hooks/useSearchToken.ts | 10142 | `f7dd11f478a4013ed8f17763df6e9c9478515145fd772ed6dce839b2905d3a42` | 0 |
| src/ui/hooks/useSetReportGasLevel.tsx | 426 | `383eeb266050c264325a347b4c98af5da592d5966983ccb71de8fac4b3dca6d4` | 0 |
| src/ui/hooks/useSigner.tsx | 7237 | `e2cb4c2c221374def92fb1cdd5f315866e2bae477a6097d575dff6de71fa0fb5` | 0 |
| src/ui/hooks/useSinceTimeWithSecs.ts | 347 | `66908e2c1906e9ceb10e017da4bc24dcf70244cb627bcd2fa4455377fd1982fd` | 0 |
| src/ui/hooks/useSortTokens.ts | 2678 | `bd4e2e6f32d9417b0faac54474e2a2a5e48e8278fe89cade7726e91d0f643c12` | 0 |
| src/ui/hooks/useSticky.ts | 1687 | `8364e294c90e4a2a082a007bc788b77b220ca553d2a1e5f8ae5270bf433b3b45` | 0 |
| src/ui/hooks/useSyncGnonisNetworks.ts | 588 | `7ec576fe7f9d50154c647aa53ccc28c1691a3dd4238b370473c425e69c8c5f64` | 0 |
| src/ui/hooks/useTokenInfo.ts | 584 | `ed28e8ea6915caac2b47b9a8eaf6f1757b25affae8412094ab622c4bffcfca90` | 0 |
| src/ui/hooks/useTypedDataSigner.ts | 1157 | `b19618bbe62794849f654baf908709c0e27512fbeb6e857abd84a20c0587fd5b` | 0 |
| src/ui/hooks/useTypingMnemonics.ts | 2326 | `c7483817d131a46eaee1b7714ca626fc58e10e32ad098da0a61dea01ee096b52` | 0 |
| src/ui/index.tsx | 1220 | `ab658f4b9d8a2b5a3ff4611d82fcc54291e7d0105d3484ea0eef163a847611d2` | 0 |
| src/ui/query/index.ts | 155 | `0b5721fb76f7cbfd6870d31e1568c651f3cad4ac5141f7e0c0d8b8914ef7c3d5` | 0 |
| src/ui/query/queryClient.ts | 750 | `402b629e3461573a7b0c6b1bb4ca06baca42c5b1abcdfaf894639f8174570d55` | 0 |
| src/ui/query/queryKey.ts | 925 | `d5e00bf22b705fcf42eb5b896480dccf726666f562a20e5ba2f0caba8970460a` | 0 |
| src/ui/query/resources/gasMarket.ts | 1068 | `0ab69376646c34fcbfeb9c0191dfbf2cc36299b14cf9fd3caa61182d159b6220` | 0 |
| src/ui/query/resources/token.ts | 1070 | `cdf0ff66de96936c8d038b8a6ec3d39ee020318798ac033b92947982e43d1929` | 0 |
| src/ui/query/resources/tokenPrice.ts | 737 | `d25e96a7c5052273daa2bdd79c15825b53e57b2bb315b505634e1f5855884099` | 0 |
| src/ui/state/account.ts | 14635 | `928a97f041b1b4fe6d14613fb1363191e5a202a8062cf030a87287dd72dc1a86` | 0 |
| src/ui/state/accountToDisplay.ts | 4457 | `21a6811dd51c5a6f81cfa19e95553280599c2247200a82c62b704b6aba967b5a` | 0 |
| src/ui/state/addressManagement.ts | 2712 | `45607aaf333ffa792f8b05e9f531e1d2b0c5c6f56dd3db5b17d04daabda18f2f` | 0 |
| src/ui/state/appVersion.ts | 1755 | `b105a5f3894adc9d3cb01489c25caa419e077f9c6a2a5d77b1377d53e7f56410` | 0 |
| src/ui/state/bridge.ts | 4450 | `a7e87664e419fc64ddc8503fae0d3bc174dccef4d78616757c9b2528b1d4d27e` | 0 |
| src/ui/state/chains.ts | 3006 | `9d618b0c0a7f23f5f62760d008f69de6ded7fb3a178fdf501ce747aced877fa3` | 0 |
| src/ui/state/contactBook.ts | 2322 | `5df9c86fc65e398f992db7ee06461cd7c3ccf852b614ef700638b78a3554d53f` | 0 |
| src/ui/state/createMnemonics.ts | 1254 | `4b2df498bb20442574ead7de614b8e6a7bfdc53a7ae2e0cdf7b1197105e36f2d` | 0 |
| src/ui/state/createStore/createExtensionStoreOptions.ts | 2837 | `8ce5e75c4804588287711104fee8187676b6c82a19ca872e3742f00636e2faf3` | 0 |
| src/ui/state/createStore/createRabbyStore.ts | 8778 | `cba15af78108088757b975a04993e84728f5683474356ba1ee9bf4cc52df501a` | 0 |
| src/ui/state/createStore/createSelectorStore.ts | 481 | `25309d084d2bee0b8737c4cefaf7b668029721a60ad818530210fe5e37faef84` | 0 |
| src/ui/state/createStore/createSyncedBackgroundStorage.ts | 1721 | `b769db306336ef4360acd45d8c99b78ecd29d7826c46e9566a83822f9aad3703` | 0 |
| src/ui/state/currency.ts | 1069 | `cd3a28eda4a9418ba405e976e22d6cc6d71e99904bbdb33c358ca69834332111` | 0 |
| src/ui/state/customRPC.ts | 2554 | `c9218fb4931bcf85579e370f86f9d6d825e05d86eb2d8d4d6a75b20f8098036a` | 0 |
| src/ui/state/desktopProfile.ts | 936 | `9daec951a0a9711b02bb11ecafe42ad75e031b3a646dcd0e3bb8155daeb9b9a8` | 0 |
| src/ui/state/exchange.ts | 3407 | `4df461fcdbfdf4cdaeec382a9ebef52f0d934534d4356d5d242c28b99a229617` | 0 |
| src/ui/state/extensionUpdate.ts | 6626 | `a0339b6d496e02fdc7b5bdf924be1a46c86b061aa6578ca61cddcb659118497d` | 0 |
| src/ui/state/gasAccount.ts | 2949 | `2b2bf5eeff7f4f61bc72524f4e8c6b247b999cfdf05f7965566490aad79ad9ac` | 0 |
| src/ui/state/gift.ts | 9194 | `9bf6cdb894b9686ea926fd254b928f02f1a14a503cf24a362b201982471ce905` | 0 |
| src/ui/state/importMnemonics.ts | 11106 | `069afc1dfbc7275cf54c68f4f2948cdf306e43f5106023f6bc1799ead818ebea` | 0 |
| src/ui/state/initializeBizStores.ts | 1085 | `aac60e35bc6ff36df9d937ff6dfab0f8800ac511f2402f918a17d23069b44180` | 0 |
| src/ui/state/initializeUIStore.ts | 2060 | `025d92116a174518c13f358c3cda384e4e53f132bb733db5c438d5d33cbdbc1f` | 0 |
| src/ui/state/newUserGuide.ts | 1163 | `e02ea913bf9dd3ade9f6030eda24ed6eeb4a16b99d0db61cd68d25271785a8b7` | 0 |
| src/ui/state/openapi.ts | 786 | `0ce247af041fa266224247374afda7a2dd70c6cc7b0941be8391eb94cdc0f355` | 0 |
| src/ui/state/permission.ts | 1725 | `0a2c487f91e4ceb93e2c297353b7093023f9268de88793a760d641362ae117c4` | 0 |
| src/ui/state/perps.ts | 79818 | `cba3dbf4949ef6b9773a90ea00942e65f82b387bee67fe7bf923487d6743c675` | 0 |
| src/ui/state/preference.ts | 11940 | `eabbaada1a43f2a4e68d8073d9637c820f804aa6c05360cc421981792d8342a7` | 0 |
| src/ui/state/rateGuidance.ts | 679 | `fc0df15f9fc28b86fb9985214898aad14fa077c5f2e6f180aa7566ced2e6969b` | 0 |
| src/ui/state/removedTokens.ts | 2531 | `054ed179b3e198d5f9912eb463ca3b7f0e95c1ec4f19807e7b3b46d93621740d` | 0 |
| src/ui/state/securityEngine.ts | 5472 | `4abfee14ba6ffa0bde4d1f3be4df9b64a59a49c3709cfae28f129fa669951557` | 0 |
| src/ui/state/securityEngineScope.ts | 483 | `0f54324448dd03e55e7a5fa7cf09a13be8a0ebb6d5f56658f7b718e924c11abd` | 0 |
| src/ui/state/sign.ts | 975 | `e41a0ac6047550dc91f262a72cfc8ec4e12e4954bb50518cb38cca1690ab13c3` | 0 |
| src/ui/state/swap.ts | 4147 | `89248e8f36103b4d299cf3d4e9e2c0b8f89706663253f878854046bbecb766a4` | 0 |
| src/ui/state/transactions.ts | 758 | `d091a16e61e8288f7f1157ce22ebe4a64a3b5b679e98d58cd941975566db2207` | 0 |
| src/ui/state/walletStatus.ts | 4455 | `478c27b8e2ea9121c1924adb2699c6684cb49a16ea14b8334a68af27180bacc3` | 0 |
| src/ui/state/whitelist.ts | 1831 | `2dc461ae44882bd9cabb42f78c149f4b591ecafadd4944a4bf1a706aa14ba089` | 0 |
| src/ui/store-hooks.ts | 950 | `7b0a84d998f6bdbe528cb405ebf5d176442569a2fe82f74d820162c46f4e6df7` | 0 |
| src/ui/store.ts | 4254 | `c7c6bd97ae76a17c7c034b98a1cc6188ad9b2e5d08a6e40bb1cdf71eec33983a` | 0 |
| src/ui/style/var-defs.ts | 1600 | `b5d0056714beb07ed2bff31872204f9827ba42de7f619648a4774bba279964c1` | 0 |
| src/ui/utils/SyncToMobile/DemoPanel.tsx | 1542 | `a42032282e4e31b22b954c09a84c5ab4c375bec434a839faaa7a9237520a01ba` | 0 |
| src/ui/utils/SyncToMobile/DownloadCard.tsx | 1689 | `966a3b6ecfe70de77dfe60972f1b21c387fdbc4808faf742ae7754f34fcf823a` | 0 |
| src/ui/utils/SyncToMobile/EncodeQRCode.tsx | 2007 | `9ca45f36cb744d2d5a9f0e85fc353030c4e26bef452e05f1b08f0cf5d72c96e8` | 0 |
| src/ui/utils/SyncToMobile/QRCodePanel.tsx | 4929 | `db7c5de41e44da791417d33ac94605ce14bb3b1e7027bf72d9ab19f5c2b7a46c` | 0 |
| src/ui/utils/SyncToMobile/SelectAddressItem.tsx | 5318 | `674d99a95735239218403c8c2c1600693300a75a19d4aabaade77a8922b3f37c` | 0 |
| src/ui/utils/SyncToMobile/SelectAddressModal.tsx | 4383 | `b742e789d55f65f6c264a30a4579e7babee7f7e933bdf052ec8ac4899f2fa75b` | 0 |
| src/ui/utils/SyncToMobile/SyncToMobile.tsx | 2068 | `40487e07999b6a1c0974d2f4aa13294823dc4e4e1b86ed52b71b933cbd2f4a27` | 0 |
| src/ui/utils/WalletContext.tsx | 3463 | `0f45c0f77170e31457e93a203ee585ac7043eb25d9b3de26cda866876457134f` | 0 |
| src/ui/utils/WindowContext.tsx | 741 | `f91c4c5a9ec42721eccac56c4ee1e49d3f2b4732b44aac70e2727cde514101f8` | 0 |
| src/ui/utils/account.ts | 303 | `efafa866ce749bebaec0c1da512fc675e33d6df145185ceade136c196b8c19f8` | 0 |
| src/ui/utils/address.ts | 697 | `b63554be7939de0acf7b7ffcaaf4ea6de5284553a8f60c3145d294d0c9745647` | 0 |
| src/ui/utils/addressInput.ts | 1030 | `ea843005d7bd3298667359a836ab6945584e04408ab4fe6b57938e3f0e346794` | 0 |
| src/ui/utils/approval-popup.tsx | 407 | `31a2da1dd6d7b1d3a414441ef4764f42c75d64d642d5f9fee14a18f0dc7bf2a3` | 0 |
| src/ui/utils/biometric.ts | 6747 | `f4e9b50ca5aef70686758ed528a0190cd641b6c8096344e7f8380e1869dec75c` | 0 |
| src/ui/utils/broadcastToUI.ts | 1296 | `a48ce58c0eb2f0ce05425c26c2f4693d12f2ce0b890e251b684d422020ef1983` | 0 |
| src/ui/utils/cex.ts | 1228 | `d4eb9a79c8c702cac4ed69f471310ce1065cd334161e912da79aa4537d46f13b` | 0 |
| src/ui/utils/clipboard.tsx | 1711 | `2ae456e05ed73e5e08a62627dde0ddad4453ac826e47d41e4df909d06ce950fa` | 0 |
| src/ui/utils/concurrency.ts | 2844 | `01f445309e61613f9fb4682d1a15fb78201b363125dadd2c13646d3d10f27892` | 0 |
| src/ui/utils/currentTab.ts | 232 | `2f183d8f58241cef5c16253e304a75c47f04e58e6ebfd49dbb29b47793d45dde` | 0 |
| src/ui/utils/ens.ts | 1058 | `9eae488058578bb91291351c7e91f3878e552fce3f23934b16f0a57f21757131` | 0 |
| src/ui/utils/form.ts | 2497 | `f48e89bfd32f2bb8f002ed76ec493b89ebaff20dbd42f5488537336f2fc9c698` | 0 |
| src/ui/utils/ga-event.ts | 2256 | `b310dcc1610de66cf16e6c9ebbb9bfcc54a747bd39407f00c3e0c8ecf01964de` | 0 |
| src/ui/utils/gnosis.ts | 3372 | `4be89467f7a65917a056cdc923c42b6819c473abd60d2744235c780489d1cc22` | 0 |
| src/ui/utils/gnosisReplace.ts | 1879 | `898f0fda44047cd015f1ee73da90abb283821a09b97b7992bcb7507f9911be28` | 0 |
| src/ui/utils/hooks.ts | 13474 | `45b9dc5d532ac1c788b6bc3e2d26a85350ba588a7c2173b865d508f4d4b526bc` | 0 |
| src/ui/utils/imKey.ts | 1823 | `3a33ae07810f070bdf10ff2a7b98fb8ec5daa1951014e1956c8db21eca281825` | 0 |
| src/ui/utils/index.ts | 3661 | `21f9d65ba21951bddebcccf0679f58f8d92bfe77ec6e536a33016c5ab6f8bef2` | 0 |
| src/ui/utils/keyboard.ts | 166 | `51813062745b3c7d9d1fafdd008157cb1f6bc590279ddd0f0133d370499ef23e` | 0 |
| src/ui/utils/keystone.ts | 4161 | `c029c5739584fb6c4bc4ed96a88c31712a7022ee0ec4ebe84bce0c3885968953` | 0 |
| src/ui/utils/ledger-dmk.ts | 878 | `6a57fa1e3cf245dca421a7667712de269289ad4dfed3f9849edfcac20cc794ec` | 0 |
| src/ui/utils/ledger.ts | 2668 | `28af854f4a9b3e37b50824587e84e53d59b2c7fbe0bc0dc5c93408430491c517` | 0 |
| src/ui/utils/number.ts | 12242 | `8f13c3418326c39c77c4c72f0ea74d6e0eff6979e98b0e4b5f49ebe4096e7201` | 0 |
| src/ui/utils/onekey.ts | 753 | `3283d482e113fd81a08a42a1fd3852e6be7f281523656d1d3ab30172619651b6` | 0 |
| src/ui/utils/openapi.ts | 987 | `2b549fe4690f2efe6b93c51852d3c7bc5121e47524ceb7d6640b842514282014` | 0 |
| src/ui/utils/os.ts | 452 | `fe3e59349e8945c7187faf7ff08fb337b1604509dea128bca1912717ac82270e` | 0 |
| src/ui/utils/portfolio/assets.ts | 6745 | `5ee2e282261af8fa534d3366d3227599ad20aae675337b0c7acb04cfc5ab8f94` | 0 |
| src/ui/utils/portfolio/chains.ts | 599 | `4541a651d16db31d83c70ec34bf40d1f0380cedebfc3f8250616733293c9d358` | 0 |
| src/ui/utils/portfolio/collections.ts | 320 | `bb5bc741f7c914aa638148457cd3a9fdb1df213dde5b477a4ca377ed3325b7cd` | 0 |
| src/ui/utils/portfolio/expandList.ts | 1689 | `efa0d28074c33ea0212a8517b1f4faf84094c94bc24a0b6de6429716f97128dd` | 0 |
| src/ui/utils/portfolio/index.ts | 1574 | `e89e2323138551c22d83cf32022025c979a4fa9088afe1b84865d758d899b6ec` | 0 |
| src/ui/utils/portfolio/lpToken.ts | 1345 | `d4948b9abb2d2e98e9d0055f51008b45c2d54015e90d10288bfabcb56a3fab2a` | 0 |
| src/ui/utils/portfolio/price.ts | 714 | `284a8d88ecbe5d981dbba480bf43ce00785050eee1aee5c2d14949d620b92a12` | 0 |
| src/ui/utils/portfolio/project.ts | 12949 | `a559b7a07c799650c640a92c3c4e373398580698ccc3a3cb9c2e739d02f75602` | 0 |
| src/ui/utils/portfolio/token.ts | 10276 | `94262868481ad8a30880e4870ea54c31ba64b00a2ea64e2a19f951e19c1363de` | 0 |
| src/ui/utils/portfolio/tokenUtils.ts | 7450 | `ae09fd3244fe28917fe83640482e73fef2335264767e7169545e5cb6285c651f` | 0 |
| src/ui/utils/portfolio/types.ts | 1760 | `36b840062d7959b44cb12e3c209e8705c1cc7cc53efbf8bd90999d0504b06e18` | 0 |
| src/ui/utils/portfolio/usePortfolio.ts | 8988 | `83e1265586dab65a3b6ecd53dc3fb78e36ab93b23ee98b8e1f89f579277de0f2` | 0 |
| src/ui/utils/portfolio/useSummary.ts | 1578 | `2394a29f4b71ef87f6e79561b23bd1183b3304bfaa716efc3e3d9a894fd2c846` | 0 |
| src/ui/utils/portfolio/utils.ts | 3951 | `78e5b09df446de0e5a1a766f58fd1ac2cee25a095088aa264985c72872c0ba53` | 0 |
| src/ui/utils/quote.ts | 732 | `f86b23f7955253fb833f5424453e7ec54b832a4a62827f37062a2fe9e24f56e9` | 0 |
| src/ui/utils/safeState.ts | 827 | `d6fa6ba5eaefba08b95dabcd469e77897176ae5502255618c181cd32836b4300` | 0 |
| src/ui/utils/securityEngine.ts | 1096 | `16f9ed96a97e8c761e3feae4589e8e1d0f707b6d95f95ed7765f3b57528aea6a` | 0 |
| src/ui/utils/sendPersonalMessage.ts | 3386 | `99bddd428101cadc6e78ba3fcfacce339a0458bd01d158ce10ddecef12a49f9e` | 0 |
| src/ui/utils/sendTransaction.ts | 29129 | `c9ed303ec3f50cecbcef44e30ab28ccbe24101e8030eeb81d35de7a8d4abb768` | 0 |
| src/ui/utils/sendTypedData.ts | 3344 | `d62464bf94c4257133f1ed1172b5093de92738f9d512ac2d0e2e9145a65c9027` | 0 |
| src/ui/utils/smart-completion.ts | 1124 | `b5959095d2286d910cd5f8c0eb28e47f613fdccc30ed1294f584bd7d529e439a` | 0 |
| src/ui/utils/sound.ts | 1201 | `31b497239a1a244fabca529390f37492a4d642113c7935d20c47f7c9e970b6c7` | 0 |
| src/ui/utils/styled.ts | 1097 | `9c874bcf2b90969d24e96d34674ce10cfb5f1ca797929654aa28071e0b6ac11b` | 0 |
| src/ui/utils/switch.ts | 575 | `08fbac0ea293d9b5246d73fe1344e33b2a5c8c9964128a0fc330e81590cf385b` | 0 |
| src/ui/utils/time.ts | 4022 | `6e31624144b5edaeb015edbead90d50856ec9279a82a1ae5b5b03413cf67ef2e` | 0 |
| src/ui/utils/token.ts | 7887 | `5ff809aa051e1aac09cef1a2a5488b111a44ee0df81c8bbbc04cbafc89cb67e6` | 0 |
| src/ui/utils/trans.ts | 298 | `c524936bd41688dd03ff160b99bb0c9c10b7d1b55ad2382c5fe735dd200fa7d3` | 0 |
| src/ui/utils/transaction.ts | 7995 | `0dafce8f81cc1e33409b9330efad4601e6683cf4ba308ef54e35163ed163d11f` | 0 |
| src/ui/utils/type.ts | 73 | `23fab3ec9dac9bdbe1519eb25cdd250e17966b1561389302d5b79e3724b3477a` | 0 |
| src/ui/utils/uiType.ts | 733 | `6a44427ffdf27f28e6ef25292713eec5b646bb3f1a5acd019db38de7b09dedf3` | 0 |
| src/ui/utils/url.ts | 584 | `c3f7d744780ad91e98df652ca7420a814c1eeafcc510b171557bfc0bb24cb4b2` | 0 |
| src/ui/utils/useCheckSeedPhraseBackup.ts | 851 | `7b094879aaebea12801d0a93317ca961a34ee21373a738bb4ef69980181ae93a` | 0 |
| src/ui/utils/useDeviceConnect.ts | 2389 | `9227bc819aa2f5697808a56e98c6e2889dd5929a5890b161b1c5fb2f35fb8da1` | 0 |
| src/ui/utils/useRepeatImportConfirm.tsx | 2330 | `e02114aea004b276660c04dacfcf8a9291903417885a9bbcadeb18aa12b50233` | 0 |
| src/ui/utils/webapi.tsx | 3612 | `3fb7f0d782b73d3d5391a54a19360452f7182721d4d7dd423b64747e7a0cc0b5` | 0 |
| src/ui/utils/withAccountChange.tsx | 1469 | `33a283e0d93852ff4ab49b3caad93042506bd2aaf4c22f1a68098819a9685d71` | 0 |
| src/ui/views/Activities/index.tsx | 4239 | `e16963a4a1297f92c59dc83157eda01eb309eb57f5cca1c4b7bdb17618466f23` | 0 |
| src/ui/views/AddAddress/AddMoreAddressesFromSeedPhrase.tsx | 20046 | `543e2e9ad3999591a92e474b9dd3c7579cfab11156800b73d2b128d0a7f57b0e` | 0 |
| src/ui/views/AddAddress/AddNewAddress.tsx | 12639 | `adfb966e376cb66a209c54d5008d7b337613b95357080c0c83e8568eb16eddea` | 0 |
| src/ui/views/AddAddress/BulkImportPrivateKey.tsx | 41392 | `17073c9f0df744788331d2ed5cec60d7bc365030bf527653b263e1bf19fa84d0` | 0 |
| src/ui/views/AddAddress/CreateAddressSuccess.tsx | 7390 | `f4a2c3ef1c7e499af07a6afab64f9227991d619b0233826f5e4f01b0895bab67` | 0 |
| src/ui/views/AddAddress/HardwareWallets.tsx | 3016 | `2a9db000e371fa4e9d3ec424f640a5b845eed48cde5041ea5530e95b4daece6f` | 0 |
| src/ui/views/AddAddress/ImportAddressSuccess.tsx | 6080 | `d27d7422f6af609347519b2abae692349909fdec792e4540fc7becd259b1623a` | 0 |
| src/ui/views/AddAddress/ImportKeyOrSeed.tsx | 18034 | `7e0ac426e01ec4c7ed2a9d8d6f9c8143918024a7e36a44f28e742cdfe9627e72` | 0 |
| src/ui/views/AddAddress/InstitutionalWallets.tsx | 2575 | `f55a5818995633d2c5215bc3142cf1ed2a70e0ede9a2e303bc1403e1ac29b65d` | 0 |
| src/ui/views/AddAddress/SuccessAddressCards.tsx | 8651 | `384e2f4aa5cfb7ffdfe0173e958e3a6bdc5d00207e545365dc83841b913c7e0e` | 0 |
| src/ui/views/AddAddress/index.tsx | 828 | `cba008c992d5e490a3b5b71dd6b16ddc19c138d65539c7ed148a056dd6856d94` | 0 |
| src/ui/views/AddAddress/shared.tsx | 7832 | `9ed85390a82dd5e2bca499546fdab01b76d77731ea3599c7378bd6ce66b97696` | 0 |
| src/ui/views/AddAddress/useCreateAddress.ts | 7522 | `3c4712a04dfa0a55ded15759b69ca190906b8f43ea3dabb030fb00f0f7375137` | 0 |
| src/ui/views/AddFromCurrentSeedPhrase/hooks.ts | 2534 | `eb2b629dd160a887e2a341daf03aac69a6cf8bb874c12053d0a0a8e5e3190ed7` | 0 |
| src/ui/views/AddFromCurrentSeedPhrase/index.tsx | 4375 | `e54edb61f14309908b18c78444b6c19ad1d0c9dd71e777b2010d48d3343b4a2a` | 0 |
| src/ui/views/AddFromCurrentSeedPhrase/sort.ts | 820 | `9759c8dcc6a100bc136e2282571fd5aa8a97b90f0fa5019fd39c1b427cf5735a` | 0 |
| src/ui/views/AddressBackup/Mnemonics.tsx | 8685 | `ed6b8609bfe4ec4f6fb65d36eec6e5ee4df0ed03575fa5fe66412e8ff53336f3` | 0 |
| src/ui/views/AddressBackup/PrivateKey.tsx | 3121 | `0a5ea94f18968297345ac3816b5cc93f3f00b71eb7c7ba3d1f311e31f69c51a8` | 0 |
| src/ui/views/AddressBackup/Slip39TextAreaContainer.tsx | 729 | `b6c67eb76ffcf88ede669cfcbba5d9efa706c8fd8117398146f0e9c7e12966bc` | 0 |
| src/ui/views/AddressDetail/AddressBackup.tsx | 4583 | `1133db5f9e16cbaa9a9ef2f83c29297d271e05d4ed2687e7c89b34ca327ff277` | 0 |
| src/ui/views/AddressDetail/AddressDelete.tsx | 5060 | `f19469d5315aabc9e2d7e9c92ef80af28d2758077d24703e8325b6e04717c1f4` | 0 |
| src/ui/views/AddressDetail/AddressInfo.tsx | 9521 | `4b75b5962ac0824ba8af3fad4e6fb1fc53945c80988bdb215677f0792520cbf2` | 0 |
| src/ui/views/AddressDetail/CoboArugsInfo.tsx | 3602 | `b432491cf97fd2ea308fbd89a28868bcd8d3a2f04bbcec12b1562000f1d1b06b` | 0 |
| src/ui/views/AddressDetail/GnosisSafeInfo.tsx | 5580 | `34b6b20166fe4ed7dd04d30ff3b5bf9224a5e5a04914d9504157bdeb13302c5d` | 0 |
| src/ui/views/AddressDetail/HardwareBar.tsx | 3011 | `405dd2eebcf7864650c3540855f84f9c87c2de4d52fe0ecf6c09d208659532a3` | 0 |
| src/ui/views/AddressDetail/SeedPhraseBar.tsx | 2080 | `d804f214bcf2023a5266c2205d1717d2b345f8bf39390cfb89655a655639560a` | 0 |
| src/ui/views/AddressDetail/index.tsx | 3353 | `b909510770be1ed51c66ac10b57fb9aee018e4868d11e2e03a9f2e032070c98b` | 0 |
| src/ui/views/AddressManagement/AddressItem.tsx | 11469 | `003d78c6ca8dd0177855873ae314420c10b230e76539ab79891f9a9cbbb41543` | 0 |
| src/ui/views/AddressManagement/SortInput.tsx | 2246 | `ae3f1e292cb6000a9d52615380af980c87a709c94b13f2b6c8a5de9fe3282933` | 0 |
| src/ui/views/AddressManagement/SortPopup.tsx | 2651 | `5192fd6966537b391c4c754367c51116c529420805931face3984f5ac7fffc56` | 0 |
| src/ui/views/AddressManagement/index.tsx | 20749 | `2dce01bb1d518479a1a671e954295eb1474fe2f64532322d3b39b6cbfe19f601` | 0 |
| src/ui/views/AdvanceSettings/index.tsx | 3863 | `a6ba2810401bfec28766ea7726d2b573fd30d5921954a6fcc446647670fe36ed` | 0 |
| src/ui/views/Approval/components/AccountAlias.tsx | 1315 | `da0830751f57a3dd01c6d8ed3fe8164bc86978f7444ae8f811795e9f32a1df4a` | 0 |
| src/ui/views/Approval/components/AccountCard.tsx | 3634 | `ce7cb55efd8588b81da67cec2bb04f463b9b839af5ad4f87e0e48c1eadde3ea8` | 0 |
| src/ui/views/Approval/components/ActionWrapper.tsx | 1885 | `387f0bffef1894338b8ca05e5a89932266ede5d2b1f70fdbfcbac785c5a7842c` | 0 |
| src/ui/views/Approval/components/Actions/AddLiquidity.tsx | 7924 | `1f6069875135d25a81ca817c20c50222ff55f995b61af94ff9ef2ad3822b8a10` | 0 |
| src/ui/views/Approval/components/Actions/ApproveNFT.tsx | 5506 | `4a81b85b839ce03ec32d0ea22093496d5e4a9ab4cddaab3b1fc73b77d265d35f` | 0 |
| src/ui/views/Approval/components/Actions/ApproveNFTCollection.tsx | 5851 | `87038e2b897a8dc51ace6ed821b3cd7ff0e009110d51a67ede1a6726e15b65e2` | 0 |
| src/ui/views/Approval/components/Actions/AssetOrder.tsx | 9594 | `4bda6f71fdad4101527c4165867b444174eaf759a76c5b90ed64f5e269298acc` | 0 |
| src/ui/views/Approval/components/Actions/BatchRevokePermit2.tsx | 3605 | `479a2ecaa9ebf2727b30c637194ba5ef792db594914243264a91b56ceaf3c9c7` | 0 |
| src/ui/views/Approval/components/Actions/CancelTx.tsx | 4299 | `f94fc87f0294421a4d05cf5aded03ef40fa8799cf29178a313babe0d1a7c1e48` | 0 |
| src/ui/views/Approval/components/Actions/ContractCall.tsx | 8322 | `c6a55fe9ffd7221bc7faea8140b8b74c38bd705ac4070bca25f7eb3d0df93176` | 0 |
| src/ui/views/Approval/components/Actions/CrossSwapToken.tsx | 9955 | `07cc8a757f2a419fb74cf2da4240cac1c889e2252513f26e0961ede45f42f343` | 0 |
| src/ui/views/Approval/components/Actions/CrossToken.tsx | 9650 | `dc46141379f11ecfe42c1912d7697b6db53c1d85f29b98a2c0303f6352571658` | 0 |
| src/ui/views/Approval/components/Actions/DeployContract.tsx | 1238 | `60992169677e6d699768b6df866e9843b27fdf01c891b4c2832a6b681307e5dd` | 0 |
| src/ui/views/Approval/components/Actions/MultiSwap.tsx | 6986 | `7d681e758b25209c55337bf6958e3a07b2f70c9511c4a9761f226650b749856d` | 0 |
| src/ui/views/Approval/components/Actions/PushMultiSig.tsx | 2250 | `f70a780d18f039c8bc9fe75b8cf45b75d5b60ff59a6f3bed77dca3ff46ccd2d9` | 0 |
| src/ui/views/Approval/components/Actions/RevokeNFT.tsx | 3299 | `af43c7d972cf8d0bc27d3604d5ca02d9eac66df6e985562e70692922de81b9d6` | 0 |
| src/ui/views/Approval/components/Actions/RevokeNFTCollection.tsx | 3712 | `be34fce832b799f4ef71639c85bc05c70e396f646cf485a9594d488961445067` | 0 |
| src/ui/views/Approval/components/Actions/RevokePermit2.tsx | 2753 | `609da2a8ead2ffa070e1be89671a3a13595bef2914c75ce1672a9f2edf8b741d` | 0 |
| src/ui/views/Approval/components/Actions/RevokeTokenApprove.tsx | 3050 | `62dfc573bb245dc4b4d3aca5a3365b7168698222e2c88b57ca53558f9a49396a` | 0 |
| src/ui/views/Approval/components/Actions/Send.tsx | 8096 | `326f60b4262f4e47dcf515aad16a528fe0a20dfa6ec521c2dd47c37fd4bf557d` | 0 |
| src/ui/views/Approval/components/Actions/SendNFT.tsx | 6939 | `336a82c8287beae4c475e4675f193e8d3f67c1b54777b5b0719579af93e08663` | 0 |
| src/ui/views/Approval/components/Actions/Swap.tsx | 11763 | `74db905b2f2cc58e1c766bf33504e5cf9288349f6833c108aa8b5832c24bfac8` | 0 |
| src/ui/views/Approval/components/Actions/SwapLimitPay.tsx | 6482 | `a2490f06af7b17f2fefb7d0177d85e030058e7fcacc04a4ae328641465910a54` | 0 |
| src/ui/views/Approval/components/Actions/TokenApprove.tsx | 11836 | `252ad3e5cf1407342ae1d16aa43a86ac49f310505543e63c3eaff51c2e669d2e` | 0 |
| src/ui/views/Approval/components/Actions/TransferOwner.tsx | 3602 | `dff20abb64ae7abf436ec7a09166e28622e13390ff5ad2dad2d469f72aa2d243` | 0 |
| src/ui/views/Approval/components/Actions/UnWrapToken.tsx | 7724 | `27c93fcb0278de2ca06893249956e5c66e0566d5aa2c08859ca2f916c8d662b6` | 0 |
| src/ui/views/Approval/components/Actions/WrapToken.tsx | 7713 | `0dd9672233a668f7b9d9fee883d9387ae11d73929856301f1bfa1b0bd7325927` | 0 |
| src/ui/views/Approval/components/Actions/components/AddressMemo.tsx | 3643 | `70c9be2fcb3bfce7a5f39c281c15e7fb8dec54cbb39d7f87b5654b2a07c0ad50` | 0 |
| src/ui/views/Approval/components/Actions/components/LogoWithText.tsx | 1385 | `6f19690d38a8e52ec0f6ab18c3960bc481b27c2c550454aa4058e223fa7dafae` | 0 |
| src/ui/views/Approval/components/Actions/components/NFTWithName.tsx | 2669 | `2c836cdadbbc142b3eca8f7474cd943dac5cfdc32d9ff57051251efd06e9975f` | 0 |
| src/ui/views/Approval/components/Actions/components/ProtocolListItem.tsx | 612 | `ea11b9098992084b3c6edd7b7d10c138b54baecf57fb65fd641024ff1fd72ceb` | 0 |
| src/ui/views/Approval/components/Actions/components/SecurityListItem.tsx | 1819 | `d58167e8e097f72ec4f1c7f01e1d86844d87ba879f71e5b5639b309be4255dd6` | 0 |
| src/ui/views/Approval/components/Actions/components/SecurityListItemTag.tsx | 1410 | `1042794f014512c5bcbdf46591bace8d0576786f7a5c11580fe8d880d9ba9e20` | 0 |
| src/ui/views/Approval/components/Actions/components/SubTable.tsx | 3368 | `040a64024ea5e49565bd42198daf389826e60af953fb40fe3a99bae99fb82d82` | 0 |
| src/ui/views/Approval/components/Actions/components/Table.tsx | 3047 | `bec1d0d9a3cbd2250fa9052004bba96ea40fe1c29829df946cd4bbcb1bcc1d38` | 0 |
| src/ui/views/Approval/components/Actions/components/TokenAmountItem.tsx | 2712 | `2505bfa5eb98f8abbcf23a40d14494790f20866247db6c61ca36faadda2470ef` | 0 |
| src/ui/views/Approval/components/Actions/components/TransactionActionList.tsx | 8830 | `fae2708bd5f406ab7a26495e9c3c789de252a6519c629b933aa8c2bacda89739` | 0 |
| src/ui/views/Approval/components/Actions/components/UserListDrawer.tsx | 3719 | `3713031694a424f6a0db04c6a8e6420d2abaeca05eaf8414519b36db22bce12f` | 0 |
| src/ui/views/Approval/components/Actions/components/Values.tsx | 13771 | `52e674014f7d09429a240b2925bb0143aca7af434935dccaf11715af28367ec3` | 0 |
| src/ui/views/Approval/components/Actions/components/ViewMore.tsx | 3667 | `733a9ce8a8001cc3164e840a2477a352522a56b155a533304a55074d551101e9` | 0 |
| src/ui/views/Approval/components/Actions/components/ViewMorePopup/CollectionPopup.tsx | 1779 | `64d9371a3bab8e7a16205f08c4181f0b9069f3d8a44eb72dd89f981a67a7380d` | 0 |
| src/ui/views/Approval/components/Actions/components/ViewMorePopup/ContractPopup.tsx | 3672 | `e45a103864e4bbf5d40fb980244add26d34d988b166926eed441a33e12e654ef` | 0 |
| src/ui/views/Approval/components/Actions/components/ViewMorePopup/NFTPopup.tsx | 1701 | `c3b280214691d274722ffcd5777e91188b5b83c234f725434ae4bd050d09bd9a` | 0 |
| src/ui/views/Approval/components/Actions/components/ViewMorePopup/NFTSpenderPopup.tsx | 4067 | `7ce65f81b35774e18c1127e588bf04b20c19c7c14603d435f443fea89a981749` | 0 |
| src/ui/views/Approval/components/Actions/components/ViewMorePopup/ReceiverPopup.tsx | 6827 | `0496fa7bd246b4f05286a0098eaf35f0f68a5f4e0109f13a99588d99229cb837` | 0 |
| src/ui/views/Approval/components/Actions/components/ViewMorePopup/SpenderPopup.tsx | 4114 | `9214de3de1e1e30b642d0d733ef5c7e1c9151fff38e471204960410e8baa0180` | 0 |
| src/ui/views/Approval/components/Actions/index.tsx | 7548 | `8f977670e9d08d8c1361a86131b901804c949086f03f494835861120092ef49e` | 0 |
| src/ui/views/Approval/components/Actions/utils.tsx | 3945 | `fadd524d722c684030d4a1327cce9785452592e5370c3689765fc6cf4ad5d35c` | 0 |
| src/ui/views/Approval/components/AddAsset.tsx | 25713 | `69e5a9fb88b630147b478d3bc1fe6b399ac456f1bbb073406e22e9c2f4373d46` | 0 |
| src/ui/views/Approval/components/AddChain/AddChain.tsx | 3688 | `56674b6f94f5b462485a4849b21db39cfa6ed237bf3c61b04cf69620c441cd88` | 0 |
| src/ui/views/Approval/components/AddChain/style.ts | 1741 | `9532dae28458cf0fa1c0624786ab90c7539500da4f3e474dd8470dca369d3d20` | 0 |
| src/ui/views/Approval/components/AddChain/type.ts | 221 | `99fb2701579829494f1dd7822666378bf161dd4b241810296d7de23863d43d6d` | 0 |
| src/ui/views/Approval/components/BroadcastMode/index.tsx | 10978 | `ca9bd3bd272fc46eda71ea85c2454303e09913332f85e25bbcccfd92baac7c0b` | 0 |
| src/ui/views/Approval/components/Card.tsx | 2006 | `7c2f47b6efbba3a6f073256731b8e8b7c573da263c9d371f08d5131af52b67f9` | 0 |
| src/ui/views/Approval/components/CoinbaseWaiting/Process.tsx | 4815 | `d39b18f4e9b5a429b99e7d024a50ddaf8949d24cafbd0e00e61d84676618b613` | 0 |
| src/ui/views/Approval/components/CoinbaseWaiting/index.tsx | 7601 | `0541b5ef3ee07f65eea3d231483341875dff8dfdd0759e1dcf5899bf2e6aa6aa` | 0 |
| src/ui/views/Approval/components/CommonAction.tsx | 7476 | `c3f421ebeeaa173ef08aeef8057e3b3de74381fe8445a330aa41adbfbcfee597` | 0 |
| src/ui/views/Approval/components/CommonWaiting.tsx | 10687 | `55cd35dd43ea7984bdccccabccbf7699f47ac9ed0c39686c7ad4ef941e88c6b5` | 0 |
| src/ui/views/Approval/components/Connect/ConnectContent.tsx | 24934 | `1853a1d3419988818c4583dba6fd83414ab86989b4e286626dd13bfc51c8e7b4` | 0 |
| src/ui/views/Approval/components/Connect/PerpsInviteContent.tsx | 14247 | `658abe5526196362f290bcbb1787a46f7e4f04c8ebc8228936952721af14efa2` | 0 |
| src/ui/views/Approval/components/Connect/RuleResult.tsx | 6208 | `501a5482bacbb7e54b0e018a629aeaa6d763160561a638ad7b75319d8b2e129a` | 0 |
| src/ui/views/Approval/components/Connect/SelectWallet.tsx | 3183 | `201df47fcf07612ada030fc6abec477846e6765a85c15e4c5b785cf0d23d1979` | 0 |
| src/ui/views/Approval/components/Connect/SelectWalletApproval.tsx | 1458 | `b3ae39e6b8c859ee599bcacb5c95259a8d66bb0149edb7aa1262d476c15841b6` | 0 |
| src/ui/views/Approval/components/Connect/UserListDrawer.tsx | 4239 | `12a8a470b5f06f14eaa11799319c19830a56313245c5b5948146572acfcb3c73` | 0 |
| src/ui/views/Approval/components/Connect/index.tsx | 3299 | `b8499e1b22fd7436342ccad1cce7380236f6ed8d3ab73ca1c92893645f9371b5` | 0 |
| src/ui/views/Approval/components/Decrypt.tsx | 4548 | `ffa307033c9968648ca897b88df2c2cb836ed8c3d4181c36e0cad439bb38fd16` | 0 |
| src/ui/views/Approval/components/Divide.tsx | 278 | `5b891405b80e8e7421fd053bd8e0c77690ef5e60201b43b1be0295bc6c103aab` | 0 |
| src/ui/views/Approval/components/EIP7702Warning.tsx | 1629 | `a399a7f12e7df9d19fd5a1c346decc92dca6b8c7174c107b8208051be787f88d` | 0 |
| src/ui/views/Approval/components/ETHSign.tsx | 1512 | `7229c6744c91ea9d7189f6497f3eaec955f7b61169593f07d145ca76db42f1fe` | 0 |
| src/ui/views/Approval/components/FooterBar/AccountInfo.tsx | 3488 | `d160dea15ac7fca4a9d795a903a61946cb12ba272d33b22a7ae7ee53839f0fc2` | 0 |
| src/ui/views/Approval/components/FooterBar/ActionGroup.tsx | 1362 | `912852b350430d107358cfabe1fba6998ff92791ff56287135f8d6c3f5721ced` | 0 |
| src/ui/views/Approval/components/FooterBar/ActionsContainer.tsx | 2335 | `3ebd1ac38d0c79aa8c21e164117cbefe8f63de6e56e9825503e14614cc771c7c` | 0 |
| src/ui/views/Approval/components/FooterBar/CommonAccount.tsx | 1389 | `81d7c59b5b12856d5fb8afa44463a7a03c5a3d46642c5142c88f662e40f917ee` | 0 |
| src/ui/views/Approval/components/FooterBar/FooterBar.tsx | 12022 | `47e3b5363863770755e39b5a36e19814e13f487ac61d36a70808c99fd2469198` | 0 |
| src/ui/views/Approval/components/FooterBar/GasLessComponents.tsx | 18979 | `23888729172ba5a56a9254a071955cc15d4acd9f757800a1b397e9c47973745b` | 0 |
| src/ui/views/Approval/components/FooterBar/GridPlusProcessActions.tsx | 306 | `81aceb3679fc10d080a6d5db0c2918e7d082a5ff47972cbbce194fee730065e8` | 0 |
| src/ui/views/Approval/components/FooterBar/ImKeyProcessActions.tsx | 303 | `c1aba7a6703196a99cc677525d6368ce37f9ee5684aa67a9c5129bc17ced69ee` | 0 |
| src/ui/views/Approval/components/FooterBar/LedgerProcessActions.tsx | 304 | `c5b61edda28538f8893fdb72996b642350a32e17d4145f1cca639193da4eeb49` | 0 |
| src/ui/views/Approval/components/FooterBar/ProcessActions.tsx | 2037 | `5fba08110f651bfa99df240709e53c29a0c795b6099848e61d7d95529e99542c` | 0 |
| src/ui/views/Approval/components/FooterBar/SubmitActions.tsx | 4253 | `330b0815d4dde736a424541371421f0f4582fb6f81a139e0710b7815955fbe24` | 0 |
| src/ui/views/Approval/components/FooterBar/WalletConnectProcessActions.tsx | 311 | `a906a53ef833a11f3791dc33236673a8efaef836c7953c4329c52390c57e9274` | 0 |
| src/ui/views/Approval/components/FooterBar/gasAccountDecision.ts | 2720 | `ece0f44e996fa2e2d5f44b759bb606589253c13d9c9b798a61e0519b075deb93` | 0 |
| src/ui/views/Approval/components/FooterBar/securityGate.ts | 607 | `5594877714ed314a2c33435b6f2799bae3ea8122b2f67e5e5cfe99b0caad8a6a` | 0 |
| src/ui/views/Approval/components/GetPublicKey.tsx | 3685 | `600c2ad6e74b95e9784cd83523a31be907b0b34d594b5f950b99cc0194e08b29` | 0 |
| src/ui/views/Approval/components/ImKeyHardwareWaiting.tsx | 11501 | `d13a875bcb4d8415ce3e1e933342e23e2f365485726e29817d6151abdd4b4b11` | 0 |
| src/ui/views/Approval/components/ImportAddress.tsx | 757 | `bf851543bc65a8957db9173e6783c0ffc4cd33d14f1669c5a75e0af08f4626f5` | 0 |
| src/ui/views/Approval/components/LedgerHardwareWaiting.tsx | 13082 | `34b61dfa752f3cf995b49cbf43316009d2e4996e179f27eae059740f090ab432` | 0 |
| src/ui/views/Approval/components/MiniPersonalMessgae/MiniSignPersonalMessage.tsx | 4959 | `acef816c19a19651f2d95ed2a9f329421ce6ecaeaa7e5fbf0208c2a0e3ddc55d` | 0 |
| src/ui/views/Approval/components/MiniPersonalMessgae/hooks.tsx | 444 | `2227584065b2020c4cf2e64ba01231487a5dc59b6110acc027288f4e369183af` | 0 |
| src/ui/views/Approval/components/MiniPersonalMessgae/index.tsx | 4649 | `4513c1a9c457bc62f07543d4300cd1be8e5bbc82ed084c0b9b0bcf23a899e712` | 0 |
| src/ui/views/Approval/components/MiniPersonalMessgae/useBatchPersonalMessageTask.tsx | 4343 | `b55d625939189cd6cc35241bdaeabe920d514da65b9b63646db3b2b71894a3c2` | 0 |
| src/ui/views/Approval/components/MiniSignTx/BalanceChangeLoanding.tsx | 720 | `a29f329ee42cab0a9d79dff5bef365666cd536926ec41e3392a3ab5bc75b4f6c` | 0 |
| src/ui/views/Approval/components/MiniSignTx/MiniCommonAction.tsx | 3844 | `fe414c3e15de67c062648400bed253bee41ef3989b4eaddb6a89df837b22c099` | 0 |
| src/ui/views/Approval/components/MiniSignTx/MiniFooterBar.tsx | 15455 | `5a18572034e5109f911d5d12c37c99e08e9e71e9633671f93632f3b97ae1f2fb` | 0 |
| src/ui/views/Approval/components/MiniSignTx/MiniLedgerAction.tsx | 9833 | `a1f9c465c29fcf2844f67e1ba46d5f5256dc64e226a6708f3b3a5866dffdc8ba` | 0 |
| src/ui/views/Approval/components/MiniSignTx/MiniOneKeyAction.tsx | 8046 | `7bad9cd4679e87ffe340be73aedb73cd0e5cd3396acbeefd10e33075e8fe11e9` | 0 |
| src/ui/views/Approval/components/MiniSignTx/MiniSignTxV2.tsx | 44395 | `868a5cc90745784a53eae2d1fb2155277e9e40418b658b47c78f2470784897c4` | 0 |
| src/ui/views/Approval/components/MiniSignTx/SpeedUpCancalHeader.tsx | 1925 | `f96d47957c074e33e16e567150075d59c309551903b802515402af8f44e28cb0` | 0 |
| src/ui/views/Approval/components/MiniSignTx/useBatchSignTxTask.ts | 6582 | `b8251c8e371897af18c3ae159a13bdc56288241beb64bcc2bae0ae9da273e931` | 0 |
| src/ui/views/Approval/components/MiniSignTypedData/MiniTypeDataApproval.tsx | 5020 | `35df879a6f2978d080868c8d95d9c71102526f741e797d18ae8e1d82b245891a` | 0 |
| src/ui/views/Approval/components/MiniSignTypedData/MiniTypedDataApprovalV2.tsx | 7673 | `94e28e6310d05f2af5f9df40090e063925f41da2cd2e6908eb69b1c600898035` | 0 |
| src/ui/views/Approval/components/MiniSignTypedData/index.tsx | 4659 | `d9b2dde4336664e569e06f21aeff2afed56f4de51487dba953c189a84a8f54ae` | 0 |
| src/ui/views/Approval/components/MiniSignTypedData/useTypedDataTask.ts | 4372 | `f82f51f73fa30a98a34affb724b2031d89fe4eed8e829ad5d704b432553b9f81` | 0 |
| src/ui/views/Approval/components/NoActionAlert/NoActionAlert.tsx | 2653 | `6368a1f21bb661eb5e72e0e1e94cc770c61d09813f17573ea8a262e142ef5408` | 0 |
| src/ui/views/Approval/components/NoActionAlert/NoActionBody.tsx | 1771 | `3eb1574b971c3c7e5a5d927aab8b9a0a85cd7bef953dff0b9a205fee92e8c2bf` | 0 |
| src/ui/views/Approval/components/OriginInfo.tsx | 4590 | `782b6abba4194a440a7da17a15b79125e053faedc1f682ff1aa19c47cd9bba89` | 0 |
| src/ui/views/Approval/components/Popup/ApprovalPopupContainer.tsx | 6521 | `d2cb7bae4265f8f13b168a9bae60cc6b3afa4df7d45c781fd925534ca1b70125` | 0 |
| src/ui/views/Approval/components/Popup/Dots.tsx | 686 | `eb2a11b59e3ccacd7f6e634bede6b61628e807b468f159e353021f1f252e685f` | 0 |
| src/ui/views/Approval/components/Popup/ErrorTxRetryCommonPopup.tsx | 2621 | `1e18c8a1c96734005892d4a43424175076ca4bf71a0c7e707a905fbfe9829b10` | 0 |
| src/ui/views/Approval/components/Popup/FooterButton.tsx | 676 | `ce3e8a1dea3d5a57757b8ddd561ebc8ffd981074290e43bcc9e1569f4493a364` | 0 |
| src/ui/views/Approval/components/Popup/FooterDoneButton.tsx | 930 | `afea0176071d1ec6721c7cd43f9f0316e0d91e3904c939bc4f9bee8ba9c58a5b` | 0 |
| src/ui/views/Approval/components/Popup/FooterResend.tsx | 489 | `cd28a26be92483d8802fb3e105a19a2ad5ff53e9e1ec27301c0a05ac1c8f5d9e` | 0 |
| src/ui/views/Approval/components/Popup/FooterResendCancelGroup.tsx | 2037 | `e286edf4ab7ce919881984562cd870f93f4ab78b8758a22046ef329aa6ff1924` | 0 |
| src/ui/views/Approval/components/Popup/MiniApprovalPopupContainer.tsx | 4450 | `017eb52757f3283e7649b0c08da4ec14cc5a795720c68567e04854cc33092ff1` | 0 |
| src/ui/views/Approval/components/PrivatekeyWaiting.tsx | 10551 | `c9889e151b9f4b800a2e1d8e92f14e7d9172c9a117f7dec71941198726810743` | 0 |
| src/ui/views/Approval/components/ProcessTooltip.tsx | 260 | `2e19c605faa775a3533b66e1ec50b5d18a48c02f15440bbd0edc1831bb532b49` | 0 |
| src/ui/views/Approval/components/QRHardWareWaiting/KeystoneWaiting/KeystoneWiredWaiting.tsx | 6097 | `a2d5c152fa4131ccb983d4b5d8b653fc43824c60b2e1ee5f08209a32fda1edf9` | 0 |
| src/ui/views/Approval/components/QRHardWareWaiting/KeystoneWaiting/Styled.tsx | 362 | `57f883c47084d180295af242ce786458878dbb1cbca5bdd4a34cadbefb6fc7ee` | 0 |
| src/ui/views/Approval/components/QRHardWareWaiting/KeystoneWaiting/hooks/useCanSwitchSignature.ts | 702 | `4f7b3acc2dc4bf51c9fdcb988e437e391e441cbd108895237202b621cd5a4cf4` | 0 |
| src/ui/views/Approval/components/QRHardWareWaiting/KeystoneWaiting/index.ts | 248 | `80a713ebae234c2f4719bbfa053205259a425d09e90a166ee84ae2ffbae6291d` | 0 |
| src/ui/views/Approval/components/QRHardWareWaiting/Player.tsx | 2141 | `72a86e030e7de239219e5c6b1d55f3f87626bbf57f821aba95db898dd59fa929` | 0 |
| src/ui/views/Approval/components/QRHardWareWaiting/QRHardWareWaiting.tsx | 13013 | `81c66b99bab2a8ae1e94d6c41ca1b5969e72a14cd62e791b848150241aa52fb8` | 0 |
| src/ui/views/Approval/components/QRHardWareWaiting/Reader.tsx | 2270 | `9bc6d0f2ce1271e3de28ed981fb57e9d84a736f5dbec97973cc143179f253e97` | 0 |
| src/ui/views/Approval/components/QRHardWareWaiting/index.tsx | 88 | `aaa6752e6650e3bffa83f16d2b51fae09c080dc59b98ef0f9cd392828c953b53` | 0 |
| src/ui/views/Approval/components/SecurityEngine/RuleDrawer.tsx | 8675 | `e0c2878e344aa9c0e8825bee898808160374a7b5ae075739e317788f90fa5e4e` | 0 |
| src/ui/views/Approval/components/SecurityEngine/SecurityLevelTagNoText.tsx | 3525 | `515d50b434570bac8a3f95b01c047eb3b5980294f4abc0080e89d4da5afa513b` | 0 |
| src/ui/views/Approval/components/SecurityEngine/actionSecurity.ts | 2015 | `cfc300c9b94992ec59f5dbf5c89473376bb557d6c9f13416282758b75ee32a4d` | 0 |
| src/ui/views/Approval/components/SignAdvancedSettings.tsx | 8643 | `4cda3012811963f59b7af11daf6d2a6ff9fec7485b091e5bad9304d5c6c411c3` | 0 |
| src/ui/views/Approval/components/SignMessageAddressTag.tsx | 6109 | `9b93b7b4f2680b0baaf7cd02f5d98889437a2f370027e19666c37ab0fa4c4bf0` | 0 |
| src/ui/views/Approval/components/SignTestnetTx/Actions/UnknownAction.tsx | 731 | `7f79fce0519a0fd889ef643605df885ce80a836ae42210cab5200fb75af0fc82` | 0 |
| src/ui/views/Approval/components/SignTestnetTx/Actions/index.tsx | 5645 | `f6546c1c9b2bea5b7af7879fafa1a3830fdbe01870c605b474b0e1f837bb8669` | 0 |
| src/ui/views/Approval/components/SignTestnetTx/index.tsx | 28196 | `c00418ce4b3cf8bc8078a715b5c1be20490605fe952bda60a729f87fbddc3daf` | 0 |
| src/ui/views/Approval/components/SignText.tsx | 21656 | `37c22ff5b3dcbac292d7b48fc4ef8a9a1900a0e1923b783d91814db15098cf6d` | 0 |
| src/ui/views/Approval/components/SignTx.tsx | 98436 | `4193b578bfb9e32df2a90da9f626d76a2e549aee90e8a2d056e6600e0c119da2` | 0 |
| src/ui/views/Approval/components/SignTypedData.tsx | 39986 | `31331390581c52a6bc0eb23846e307d79d9b48ab8cf22811a68044d5d0787f25` | 0 |
| src/ui/views/Approval/components/SignTypedDataExplain/parseSignTypedDataMessage.ts | 708 | `e89dd869e7cea168de99db813335ba78d192bb611070536596c36a7001c26359` | 0 |
| src/ui/views/Approval/components/SwitchChain/SwitchChain.tsx | 5015 | `f726bb2c71dca5ece99a6f267b5b2ae153c39e96c5cf5e71b921982105a2bbf4` | 0 |
| src/ui/views/Approval/components/SwitchChain/style.ts | 1741 | `9532dae28458cf0fa1c0624786ab90c7539500da4f3e474dd8470dca369d3d20` | 0 |
| src/ui/views/Approval/components/SwitchChain/type.ts | 66 | `f1ce8643fd5fade8c81acd55c2cdd71d787cd625e4eceeb51b9f4913e5e3470d` | 0 |
| src/ui/views/Approval/components/TextActions/CreateKey.tsx | 958 | `17897a1bc10b2c2090d5facb7e223a43ae4dfccebda2a8993f4e7626faf77caa` | 0 |
| src/ui/views/Approval/components/TextActions/VerifyAddress.tsx | 975 | `1cdf0ccd6e23ea637a7255dd9fd86d59fcbf7318f7cf5ccca22dbd6fa5867172` | 0 |
| src/ui/views/Approval/components/TextActions/index.tsx | 12169 | `d492f03dcc902e5412bed05dcdc02bcd639433e873f6bb318ae9053dad054e4b` | 0 |
| src/ui/views/Approval/components/TextActions/utils.ts | 462 | `eb8320294d0879e6b943d42ffd08ce69f17efff9d94f4460bf2f1d00d6ad8b3e` | 0 |
| src/ui/views/Approval/components/TxComponents/BalanceChange.tsx | 12448 | `5d514b3eec753d238d806171f272317b10d2eafd0871524ce7d019036c20af3d` | 0 |
| src/ui/views/Approval/components/TxComponents/BalanceChangeWrapper.tsx | 1829 | `6c5f8de0c830f3bb36f2f852222e6cfa766833f1f67dbd685cdf5889c1ebb36b` | 0 |
| src/ui/views/Approval/components/TxComponents/CoboDelegatedDrawer.tsx | 4246 | `f6fbc87a71c4a28aaa30e2e508ecd79cdf38e37ad90f50e4985fa3e313212a61` | 0 |
| src/ui/views/Approval/components/TxComponents/DrawerAddressItem.tsx | 3254 | `bffe4524a5601359e04dfe40353cf7bc367b4bfb5bdd80101c7e1503b90754ff` | 0 |
| src/ui/views/Approval/components/TxComponents/GasMenuButton.tsx | 8658 | `9fcf5c132ae44005b3bfccf05b6eceab7fc4ea8e5c0fdec30de195f850a5deae` | 0 |
| src/ui/views/Approval/components/TxComponents/GasSelector/SignMainnetCustomGasSheet.tsx | 20419 | `b315759c29680f8336a1974ba8db9bf1840bf20196dd6078d1513241126bf9a1` | 0 |
| src/ui/views/Approval/components/TxComponents/GasSelector/SignMainnetGasSelectorHeader.tsx | 30252 | `249b0eccea735fc7a621b7c11582693d3c63302017d480961d82d7b6b07eb9d8` | 0 |
| src/ui/views/Approval/components/TxComponents/GasSelector/SignMainnetShowMoreGasModal.tsx | 19261 | `6a75be07655c076bc44b37626a3c7b8d8b017bea8768799df383b75a3593587b` | 0 |
| src/ui/views/Approval/components/TxComponents/GasSelector/SignMainnetSwapGasQuotePopup.tsx | 17355 | `06c95b2a4d2f8443b418fe1b4d35c768d57732dcf9cc7d357ff64053bd473c34` | 0 |
| src/ui/views/Approval/components/TxComponents/GasSelector/approvalGasDisplay.ts | 6036 | `78fd3dcf1ce4a24253e451ed5f7b123ba67ccc95235d546e09a1cca20f7784dc` | 0 |
| src/ui/views/Approval/components/TxComponents/GasSelector/directSignSummary.ts | 1005 | `2f5ca0911c17209455c4bb0eab34727bad0bffae679243dadb389fdda5371982` | 0 |
| src/ui/views/Approval/components/TxComponents/GasSelector/gasCardStyles.ts | 3220 | `1009c7992b991c34b93967d3b7400182c5aa53f870dc2483d349719c882992e5` | 0 |
| src/ui/views/Approval/components/TxComponents/GasSelector/signMainnetGasLevelPrefetch.ts | 7388 | `1b03c668d31698b8741fa0712cfb824f30e8a8fe0fa58fd4ab9150aa2b38db62` | 0 |
| src/ui/views/Approval/components/TxComponents/GasSelector/useEffectiveApprovalGasMethod.ts | 2801 | `0d7fb2d29832a4ab58c192d8825ee71abea432bef53ebe806fa1d9d1828cc507` | 0 |
| src/ui/views/Approval/components/TxComponents/GasSelectorHeader.tsx | 38775 | `eca29c326c6a248e4b74867088e41a97942318ce123a4062c988f89e06f91bc7` | 0 |
| src/ui/views/Approval/components/TxComponents/GnosisDrawer.tsx | 5214 | `81ce4f96118072962adc59237b490e5fb24db3fb2be90a9a23e39b84d3b511f6` | 0 |
| src/ui/views/Approval/components/TxComponents/Loading.tsx | 2486 | `84c74b108e2af88893375860282ec965540e04c543f48036ad040113a27e135f` | 0 |
| src/ui/views/Approval/components/TxComponents/SafeNonceSelector.tsx | 12566 | `0f9e16c979c8925cd08e06e9c859dbd67b5a06b603c6081124db0b7331a3dc29` | 0 |
| src/ui/views/Approval/components/TxComponents/ViewRawModal.tsx | 1167 | `915b0d46b2eee73851a2693b18bf65c7d0b77d68bab28fcba3568552caaaf2fd` | 0 |
| src/ui/views/Approval/components/TypedDataActions/BatchPermit2.tsx | 6774 | `99b5c86f1872282c52d3b72978d8ed15496e73518e3dcc5847a4672e2fa8a0a7` | 0 |
| src/ui/views/Approval/components/TypedDataActions/BatchSellNFT.tsx | 9103 | `84203caf21659cbfa940f47194c8c61891329ab974c7ab64c2524b8f6d4c5670` | 0 |
| src/ui/views/Approval/components/TypedDataActions/BuyNFT.tsx | 7769 | `a7a42f587b328d7fc728331555e6efff164f6058e1e5a40895bfb383d38250ad` | 0 |
| src/ui/views/Approval/components/TypedDataActions/CoboSafeCreate.tsx | 2081 | `c460d5c9e8b4f486c5cd85540b89288a63c26abc0b5defacf42cc903e8c5f121` | 0 |
| src/ui/views/Approval/components/TypedDataActions/CoboSafeModificationDelegatedAddress.tsx | 2295 | `528c8b7be045a56bd08b6209ccca07e8659d4844d1db285a9b841fbe95db79c2` | 0 |
| src/ui/views/Approval/components/TypedDataActions/CoboSafeModificationRole.tsx | 2179 | `3711a46b7125783a05e4d474fd30654e54e26149339c1e0478c68830013fcb92` | 0 |
| src/ui/views/Approval/components/TypedDataActions/CoboSafeModificationTokenApproval.tsx | 2252 | `24bd0c9ecd0c20cea2fff8207edb99e4148370fbd065c73c2d2bdf78f09622d6` | 0 |
| src/ui/views/Approval/components/TypedDataActions/ContractCall.tsx | 5459 | `a66dbc020e2449296f36ace6a4349b076f5f7b5a7ca83c3519f69324fc0baccb` | 0 |
| src/ui/views/Approval/components/TypedDataActions/Permit.tsx | 6027 | `9c30d6f32e429d76ac101793f29779e07606ce5e4141d536ddc098bc7b2ecdee` | 0 |
| src/ui/views/Approval/components/TypedDataActions/Permit2.tsx | 6409 | `cf46d614be125118af96f6c9a99be8a35e84dc1cafd9166b1ce844cfe1ec983e` | 0 |
| src/ui/views/Approval/components/TypedDataActions/SellNFT.tsx | 8776 | `10cef295726f2f4abcd9a8238013d5dd7d9d713fcd8f9a6cfc8fd45ffbe496d8` | 0 |
| src/ui/views/Approval/components/TypedDataActions/SignMultisig.tsx | 2833 | `bf7ad43aad81b5df1c51b0659e1faf17949cc607aaeedf1a08fac50ff7ff1622` | 0 |
| src/ui/views/Approval/components/TypedDataActions/SwapTokenOrder.tsx | 9272 | `750ac3ee490dd00361a5e56e47223af7cc5406cc21179778cb2ede9205179f43` | 0 |
| src/ui/views/Approval/components/TypedDataActions/index.tsx | 14116 | `2541b64123acdfa143f069470ad12004b3221eff5bdf8bf0cfdbcfebddc96a16` | 0 |
| src/ui/views/Approval/components/TypedDataActions/utils.ts | 7290 | `26244d95e71b57aeb8cca9c5dcee9b9aa14e83b546635b1bc65f3895d84d3744` | 0 |
| src/ui/views/Approval/components/WatchAddressWaiting/NetworkStatus.tsx | 1223 | `8d469f1746c2339c417dc98390f8991e0f33bb34535c5552c9c98c97ee9a39bd` | 0 |
| src/ui/views/Approval/components/WatchAddressWaiting/Process.tsx | 5105 | `8aa79e62688647e6f1e4f8bc3e4d9c1d530937d96fcb4261bd8503dea9accb23` | 0 |
| src/ui/views/Approval/components/WatchAddressWaiting/Scan.tsx | 1058 | `e1ea9d33c64e769672fc541c3ab00f68de257eaf5208953df40603f31061924b` | 0 |
| src/ui/views/Approval/components/WatchAddressWaiting/index.tsx | 12128 | `90007b241ce4dca9c78b49ae46458972afb0f4a83134a06cfc74b0a72bfb5edd` | 0 |
| src/ui/views/Approval/components/index.ts | 1033 | `a343db7d2cd100aeeb7de758b7f239af90e8338757f98f40587a88e470cfa0a8` | 0 |
| src/ui/views/Approval/components/map.ts | 1319 | `dd246baa5ec16dc36ab7f180e4670dde1eaca477f9ed7434bb4715a260a7d823` | 0 |
| src/ui/views/Approval/components/signMessageAddressData.ts | 5848 | `a988cc65d1d950a124fa27fc95e56629ab58429f5991f65eaabcbac697a3f5ae` | 0 |
| src/ui/views/Approval/components/signMessageAddressTagLayout.ts | 659 | `22b97d89b0ef6125cf7e9e2c342cf9ca0d484d8d7bf3d5686f55d085e4f065c5` | 0 |
| src/ui/views/Approval/components/signMessageHighlighter.ts | 5850 | `943a08ff1c1e224333b90b870c0fa0599f3e92b374cc01989dfb1a155bdd6054` | 0 |
| src/ui/views/Approval/components/useSignMessageAddressData.ts | 2710 | `f586185d4c6a9d25a4aa410eab40d36e4a29f7f257fab8f0d4159cc8965072ba` | 0 |
| src/ui/views/Approval/hooks/useApprovalAlias.ts | 1194 | `6f7336575588484ba039ecc559b549c0adb7ecb6b269587b58cefd4ed81e3d54` | 0 |
| src/ui/views/Approval/hooks/useApprovalUtils.tsx | 704 | `9d6a6d7ef091ca2876fcd54fa564d84d2cc8c001dfba23e972a048c134c26bde` | 0 |
| src/ui/views/Approval/hooks/useCheckCurrentSafeMessage.ts | 1677 | `57523086f1110e1600b97f73d432c972a7b1293a3b974e2b0250716255692090` | 0 |
| src/ui/views/Approval/hooks/useGetCurrentMessageHash.ts | 876 | `98007d7e04cce52f62bccbe95b1c6c9ddcd736903cdea24ba80d2626bbbf882f` | 0 |
| src/ui/views/Approval/hooks/useGetCurrentSafeInfo.ts | 1674 | `5caf5b4ac9c4806225c2fe7884ba446a528d4c5ce77d20821703e0f2d4dbb58e` | 0 |
| src/ui/views/Approval/index.tsx | 3147 | `4d4c3503c3f2f959e26b4ec8011f65a3da56a4b9c25c3997d5297d04c1b2c7e9` | 0 |
| src/ui/views/BiometricUnlockSetup/index.tsx | 6885 | `2a551bf9ae8cf433ad12a6f20ff9964cb85ff23d82b68d28574e0a7e6a19ee82` | 0 |
| src/ui/views/Bridge/Component/BridgeContent.tsx | 39843 | `08f53c6b0fd33619073d92bfc3a19df0c9fc8ded0eaf2a848ed84e81225f3137` | 0 |
| src/ui/views/Bridge/Component/BridgeHeader.tsx | 3393 | `ee9566ad9074f6779e610767b34ab83bc82225a16eb45fab86425cd6e7fb2d81` | 0 |
| src/ui/views/Bridge/Component/BridgeHistory.tsx | 17446 | `05f20da3d6377c843bd0c4d4ca107c3371c8ea5a104526568b0dda4d216594b8` | 0 |
| src/ui/views/Bridge/Component/BridgeHistoryStatus.tsx | 13146 | `8d404c87d94fffa0fc003d31afae4d4e4383e7f9a4623d1576268f1898b58784` | 0 |
| src/ui/views/Bridge/Component/BridgeProgressCard.tsx | 6833 | `1a7aaa25b93e774abe7c3e6418566279a8f16f1ff620dbe9f0af46318abbfccd` | 0 |
| src/ui/views/Bridge/Component/BridgeQuoteItem.tsx | 9376 | `6bdb5536b94ebe905cc4b2c70cf173ea1bccfbfd77bbaf6bdf722bdb14b26b70` | 0 |
| src/ui/views/Bridge/Component/BridgeQuotes.tsx | 5754 | `0849bcfcdf71cebb31376df5862fec93baa5409d3c724fbb7194b020b24928f0` | 0 |
| src/ui/views/Bridge/Component/BridgeShowMore.tsx | 41060 | `d9b6af84787115d80b07c415452dccb88307ab1f15d8ae27a53a0ef740f4848a` | 0 |
| src/ui/views/Bridge/Component/BridgeSlippage.tsx | 15588 | `0013b462308d9ce7844537c087d46eb2c03ffb3cc8da1b84977306b28789a76f` | 0 |
| src/ui/views/Bridge/Component/BridgeStatusPopup.tsx | 12510 | `fedb0b9f0616d4ecd824c123c4009c21554e28003b1a605c19e27ed614db6ab9` | 0 |
| src/ui/views/Bridge/Component/BridgeSwitchButton.tsx | 3857 | `a0f14a5437f9b2292e9a87516f4b9c3753913766d89f7b4b7a49ad0f6375e89f` | 0 |
| src/ui/views/Bridge/Component/BridgeToTokenSelect.tsx | 4206 | `0fbb6f25a97b180469a9cbaf1c429dd7f66e4588e90abcd210387503156ea8b3` | 0 |
| src/ui/views/Bridge/Component/BridgeToken.tsx | 15071 | `8cd4291a8ca69871169c456c351e04c8bfe803a0f8abbebec11efdd9dcc14994` | 0 |
| src/ui/views/Bridge/Component/IconRefresh.tsx | 1390 | `af7fb41276df58b7a3b562799f7fc8b8a33d28cea9890c7258beea5134aab2c4` | 0 |
| src/ui/views/Bridge/Component/InsufficientTip.tsx | 547 | `3c03b0a861edcdb03c3daf9b40924cc344242eb31dd4bfaa4d07a9e7d7c04bd4` | 0 |
| src/ui/views/Bridge/Component/PendingTxItem.tsx | 9052 | `6cd70b5ee3d602d4bf6984c520ae2d2cec0a0ed08dba50b92c12ed3a2b7f6794` | 0 |
| src/ui/views/Bridge/Component/QuoteLogo.tsx | 1294 | `a2f5c53a8ef095caab46cf31d0aaaf9098a37a1a031ab592a3583cb38e68241f` | 0 |
| src/ui/views/Bridge/Component/loading.tsx | 1766 | `a1ea52ca12a9048c6e89e5d700650da0beb49995b2c837bbfb1b96c053f824e2` | 0 |
| src/ui/views/Bridge/constants.ts | 416 | `5bbb7bfa7749f14883c9b5fefc392269369c3de6b1e0801d2e290f7c1022aa1e` | 0 |
| src/ui/views/Bridge/hooks/context.tsx | 640 | `b5d09104c4efdc7dd71668e592c27fbcd000eef2e12da6326869595dbb651cbf` | 0 |
| src/ui/views/Bridge/hooks/history.tsx | 3075 | `d3f8a54c5eb8bde14e1a7dc384b9bc7cd26522cb7f3275a992d7e2e481bc9a50` | 0 |
| src/ui/views/Bridge/hooks/index.tsx | 79 | `55f05ab1be9e9be9e32d6afd9c85072b661eee58953f2e0c955839098ae87122` | 0 |
| src/ui/views/Bridge/hooks/slippage.tsx | 1184 | `cfc851d415d7d41506f2261948e30c1b3a2dcda5e60614207d87a6f210ae54cf` | 0 |
| src/ui/views/Bridge/hooks/token.tsx | 29349 | `756b2a9fbdba1bac521e3c2bd9c5c222aec51c3068cd618b6b7766460498beca` | 0 |
| src/ui/views/Bridge/index.tsx | 1463 | `d7815ffba4d96efebbf9874a0af20bf1cc2f7ce41d485ce3b8c2b3606d4f42ba` | 0 |
| src/ui/views/Bridge/utils/bridgeQuote.ts | 2407 | `7a0aa9ceeb49ed49df2b3179410b25246ece11485a658ef80c7ac76a2dfeb80e` | 0 |
| src/ui/views/Bridge/utils/duration.ts | 3045 | `6b0f2377d06accaa926fed370067c1b09e94f51fc2ec5c9f5b4a5d52f347bd40` | 0 |
| src/ui/views/Bridge/utils/historyCache.ts | 1570 | `ea53911f6fef910ec323eb33949748f282d7b1f3e5d6037a597f6d919a952b93` | 0 |
| src/ui/views/Bridge/utils/historyRefresh.ts | 902 | `fb2d379b2c0aed1bbaf67f7ebc78c091c58641c276d2d383f551d6421a770e10` | 0 |
| src/ui/views/Bridge/utils/historyStatus.ts | 13980 | `f49dc70cafb25c744730313f7c9f509271281debd78bf443e3853bf9108ed1aa` | 0 |
| src/ui/views/Bridge/utils/pendingStatus.ts | 3661 | `194423b5ad45ffd5db6473019baa3cad9c465805af623fc3a70257ed9d70a92f` | 0 |
| src/ui/views/Bridge/utils/progressBar.ts | 8102 | `8d9233b967e721a7d21abdd0315d6c3f00ae94a4e139881a8e4f2e3f633ed71a` | 0 |
| src/ui/views/Bridge/utils/refundLink.ts | 317 | `6b005d23a2d857c970866a5f59414c1c41b2df33cc10fb13156f81df8f9d1dff` | 0 |
| src/ui/views/Bridge/utils/remoteFromTx.ts | 1268 | `0d464c288a861cae32b631b12705f128e15629d04b4e9470e1ccf28f2ee6b068` | 0 |
| src/ui/views/Bridge/utils/submit.ts | 4357 | `6740ba28f7ab3ba632de490656395a597f245f7ae5968c0e60b6b80a1bca3f5b` | 0 |
| src/ui/views/Bridge/utils/support.ts | 246 | `8eaa7fe9a5b1e0ced0cd80fd379bb9c11fbe869546a004cc574db3e03f36a73f` | 0 |
| src/ui/views/ChainList/index.tsx | 1470 | `8f1c42967a4e02ee310c0b352607b1ab4ee623469dc4c9a7cf0a2d8b13356878` | 0 |
| src/ui/views/CommonPopup/AssetList/AddTokenEntry.tsx | 3482 | `9c18caae50f9db89db31a70ce6cdd150e4efa22a6314605f22138fef6bf71c9d` | 0 |
| src/ui/views/CommonPopup/AssetList/AssetList.tsx | 5912 | `ec4735bc4c394c1153743b1bcbdf3cec396226bb12d3b78730e42462bd1b1fdb` | 0 |
| src/ui/views/CommonPopup/AssetList/AssetListContainer.tsx | 7780 | `0af9d425b8bc5c9221d8507a68dc9271eba03ac46e307531cb38606f866766c5` | 0 |
| src/ui/views/CommonPopup/AssetList/BlockedButton.tsx | 980 | `bc2c12843a3c06722bde8b56b858e7f796d5a2a7d2950b12963fa2f068713db0` | 0 |
| src/ui/views/CommonPopup/AssetList/ChainItem.tsx | 2792 | `49955f365ca5cd0306f3ed653fe16fddd18bbbb2ce91f349f208786102b2fd0e` | 0 |
| src/ui/views/CommonPopup/AssetList/ChainList.tsx | 4174 | `f37465ef1d19f92667d2a686ffc3205553dc471623bb46a65750b34d7c03a2b5` | 0 |
| src/ui/views/CommonPopup/AssetList/ChainToggleButton.tsx | 776 | `3b9e009238303d43bf367857210c07fd55b039d81e8422080bc1c803201b79f7` | 0 |
| src/ui/views/CommonPopup/AssetList/CustomAssetList/AddCustomTokenPopup.tsx | 12593 | `f5902002f98551ce8e60b7d1734334c8bbdd12facc60f446f2fb8e3d199180d8` | 0 |
| src/ui/views/CommonPopup/AssetList/CustomTestnetAssetList/AddCustomTestnetTokenPopup.tsx | 11627 | `c1e4245c00c6e111601ecc5a19f10e567ef509ad2ab0afee9151fdd9a72a04bd` | 0 |
| src/ui/views/CommonPopup/AssetList/CustomTestnetAssetList/CustomTestTokenList.tsx | 979 | `eb69d94769cc3931cf2bd263e8762e18d0978cdd556b65d0f6c4cfc661822990` | 0 |
| src/ui/views/CommonPopup/AssetList/CustomTestnetAssetList/CustomTestnetAssetListContainer.tsx | 7235 | `586a3677be2fe74476e39228f4ec4406b7b2e11eb32ceac316bd8e4aa9b7c31c` | 0 |
| src/ui/views/CommonPopup/AssetList/CustomTestnetAssetList/CustomTestnetTokenItem.tsx | 4905 | `bb2d12719388786008b79468fb8aefd5cebafecb4b49609b37438b6a2154b0fd` | 0 |
| src/ui/views/CommonPopup/AssetList/CustomTestnetAssetList/index.tsx | 1746 | `df6ebe3e5c9a06d7bd2adaf1e6adbc76dd584d0c5d45cac96e60bc9ec6ed4494` | 0 |
| src/ui/views/CommonPopup/AssetList/CustomTestnetTokenDetailPopup/CustomTestnetTokenDetail.tsx | 11371 | `a8394a26a5dd88870208249a49660176d68f513ed330287a75fe720273f25c2e` | 0 |
| src/ui/views/CommonPopup/AssetList/CustomTestnetTokenDetailPopup/CustomizedButton.tsx | 1531 | `1fac1434f8c4586d5180b6259a21fa6dd9f63cc8ae65cac6c194be0ccab7673f` | 0 |
| src/ui/views/CommonPopup/AssetList/CustomTestnetTokenDetailPopup/index.tsx | 1948 | `5f11b7c55b88606fc1dabc53b2e4490c3be35fe2a57f6652d15f7a09e3b8c2b0` | 0 |
| src/ui/views/CommonPopup/AssetList/CustomizedButton.tsx | 1006 | `5527eb4e3e4befa89d4641b5e0596dfd2dc413547ebc2f204945a5a33346b8ce` | 0 |
| src/ui/views/CommonPopup/AssetList/HisotryList.tsx | 561 | `397c1996008533ef310ed5b00852cc4cfaeaa959c0cb0ee3e201aa3ffe9c553a` | 0 |
| src/ui/views/CommonPopup/AssetList/HomePerpsPositionList.tsx | 9002 | `f6f7528e02554b99848ac29afb62f6a5a982dc918f5f8acbd90e4b6e5a42abd9` | 0 |
| src/ui/views/CommonPopup/AssetList/NftPreviewSection.tsx | 3832 | `e82d65cb11547ae45f13d3ac9b342d8c2fef11eb277ede94292bed4e1098ece3` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolList.tsx | 11183 | `6c2336f75a33214e027fe962ba991e85f36b6b2ef7b01919c1faed4ee5ef0ed2` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolLowValueItem.tsx | 3192 | `9669b356cfd332ec7d5897f4a9a6c1f3d582565d47ad7264b98bda4b0e8ae6d5` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/Common.tsx | 847 | `b59997a9216d70e13c04eeef262e20ebcc425c939b640693ed79179677aaee2b` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/Lending.tsx | 1230 | `dfd416ef7bfd71571ed917e3cf442f8521b02da2d3d04d702fbe9290573c2f34` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/LeveragedFarming.tsx | 1166 | `8c044cb8876d11f4e64da05c7c090a852509f56cf88cebff6634936b0c50005e` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/Locked.tsx | 1118 | `281be48adb5c2d6becd69d2fd4cb36aca557e7a9404d3c46f9b8656e1ed7b3b8` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/NftCommon.tsx | 787 | `d1aa802a274f9beff3fddc7855b6549edf73177f16b3e09cfaf1ee0f66bc2cc7` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/NftFraction.tsx | 764 | `e30c677e5d5fea4ce492af4b85ac414cfddbe199d8b1ea7cfece45ff12a09e67` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/NftLending.tsx | 1173 | `e29fa3bbc6329ccd71d3e7689a9cfe38e28cff11b28facda87e870d441dfa27e` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/NftP2PBorrower.tsx | 814 | `73266431fce1ecbb01fabe8ad678e58d2c54231f8c3fcf8c8c46488bdcc82f8a` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/NftP2PLender.tsx | 955 | `b6052f65370f8c87bfd378f758e7b283a457f09860f9e299a9bc2bbb1e9f917f` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/OptionsSeller.tsx | 1932 | `b28d149b5228e9855045a65a6be4d84928c65342bd984b5dab2c6476e7697a22` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/Perpetuals.tsx | 2029 | `d75120ab2986e9d1c53f01559102b69440da4b18dc55c11a62c74a0574dc3278` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/Prediction.tsx | 2175 | `c5a923d76e94901e454b268320503c806c40909da62046a62aa7435f759cc83a` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/Reward.tsx | 583 | `c976938e887f2247f1cdd272c1e037abc163ebeffb3fe34b57454c0f233bb360` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/Unsupported.tsx | 763 | `e285c4d4051bcdaf9bb796f9908df7abe49ed2504a906466e28d6ca37c6ca6e3` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/Vesting.tsx | 1563 | `42a61bdd4c46d853bbe3bed43d67c32848467f450e1220e52f184fb05bd30ee8` | 0 |
| src/ui/views/CommonPopup/AssetList/ProtocolTemplates/index.tsx | 1018 | `122ce9883a15e29d2de643165508fd0b45bdd016025d77fa2496781dc4e64bc0` | 0 |
| src/ui/views/CommonPopup/AssetList/SummaryItem.tsx | 4016 | `970a76209b39ee1e4bdffe79f92984e7748effb5f3f6f9157993d766b7a64a57` | 0 |
| src/ui/views/CommonPopup/AssetList/SummaryList.tsx | 2570 | `2ef9edac693220e6ba6a86fd008031b519c949e538a7958339ba8f9d30db45bc` | 0 |
| src/ui/views/CommonPopup/AssetList/TestnetChainList.tsx | 3030 | `2701f48a6d7ecd3fc07028d75a054f2fb9cf7726271ed139948cf54f67d79d69` | 0 |
| src/ui/views/CommonPopup/AssetList/TokenItem.tsx | 9189 | `1cee812f777fa8ba7ea5742e4e6fd9876a3c08061a5e0c81ba449a6479f348e6` | 0 |
| src/ui/views/CommonPopup/AssetList/TokenList.tsx | 2095 | `8cc6bf9cfb8c871c8067f605ca86769d6903a94c633c7df685bc8c0ea6534fb4` | 0 |
| src/ui/views/CommonPopup/AssetList/TokenListEmpty.tsx | 657 | `65f0fa91258d944d77d5b384eb76b8e5136b60b346efbe26066a1485a94b9b3d` | 0 |
| src/ui/views/CommonPopup/AssetList/TokenListViewSkeleton.tsx | 2225 | `8cc91a113689740a80065bb8a139f494c01c1bec68ddd3a3516116419281b158` | 0 |
| src/ui/views/CommonPopup/AssetList/TokenLowValueItem.tsx | 2744 | `39689243c2df858c438b2caf2e4d676e1d9e2166c8e564e8021b01d8a03f463b` | 0 |
| src/ui/views/CommonPopup/AssetList/TokenSearchInput.tsx | 1892 | `772e0feb63bace1272e672039fbadfd13c28c77b9a32d36a477e885ac559c2e1` | 0 |
| src/ui/views/CommonPopup/AssetList/components/Card.tsx | 359 | `17926ca7db6a195802bfe7d1d89074164f2a3bea1293efc0fdf6a1d2319d04f9` | 0 |
| src/ui/views/CommonPopup/AssetList/components/CustomTestnetTokenTable.tsx | 2230 | `8f92dc16899af11e429c1b28e89f592fbfa648f2828cd77e5d55c9bae5c8918d` | 0 |
| src/ui/views/CommonPopup/AssetList/components/DappActions/DappActionsForPopup.tsx | 9080 | `e8f94424adc428115d70828ea429982132341a6aa6b8eb08d3a7e292a654143e` | 0 |
| src/ui/views/CommonPopup/AssetList/components/DappActions/constant.ts | 267998 | `f591b9bd01168329303019b1a6c0e13468181d83f43530c3d7f10c7bf31809d0` | 0 |
| src/ui/views/CommonPopup/AssetList/components/DappActions/hook.ts | 10562 | `3404d5cc87f8903e91f40da8fef5102bf7f0dbb57dd2f9ff911f6e583be52919` | 0 |
| src/ui/views/CommonPopup/AssetList/components/DappActions/index.tsx | 8851 | `b61db1f6dc274c2f833ac68b101e47d9f20e9d8c1c2289c89cd6fbee3cb09e6a` | 0 |
| src/ui/views/CommonPopup/AssetList/components/PortfolioDetail.tsx | 7446 | `b7e5fd4474755884b49101423a5dafa3cbfca82ba18097bed8749fadd1c59bf8` | 0 |
| src/ui/views/CommonPopup/AssetList/components/PortfolioHeader.tsx | 1674 | `daf9377a3e11efd7b435ee200a66acd1107f8a8fce6ef456127f9b4a61decd84` | 0 |
| src/ui/views/CommonPopup/AssetList/components/Table.tsx | 1398 | `9e5d73a969dfe5d775f370215c189b8cf3c4ba61ccf9608eb0b561a6eb1a09b5` | 0 |
| src/ui/views/CommonPopup/AssetList/components/TokenButton.tsx | 3906 | `aa937b37f05b3a8510fd9c7785f40fa5013538fb8395f36dd67560c30ae8932e` | 0 |
| src/ui/views/CommonPopup/AssetList/components/TokenTable.tsx | 3034 | `c7aa5ed42254bf8d820ebf10d448d1843714d69a9ec9dfe9c5a778364600325e` | 0 |
| src/ui/views/CommonPopup/AssetList/useCustomizedToken.ts | 2018 | `95474492330601a36348397a98bfff27c7cba2870774bd03f3b1c32fea5b252b` | 0 |
| src/ui/views/CommonPopup/AssetList/useExpandableList.ts | 1131 | `77dd2953bf721d0b97087ff863fb8a91b6358f75487a2803e59099b488fe3025` | 0 |
| src/ui/views/CommonPopup/AssetList/useFilterProtocolList.ts | 1409 | `7a07f6d576dd1e286d53ae12820ab72a4cc3cca67c2c55541010d7fa786e87d4` | 0 |
| src/ui/views/CommonPopup/AssetList/useFilteredTokens.ts | 1079 | `b1fe684cbeec8ff609b1afb1f53aaf927642211294077d241e6442d2a7e2f8ab` | 0 |
| src/ui/views/CommonPopup/CancelApproval/CancelApproval.tsx | 1941 | `84fa8f3c177fa9b2360735d9554cb1de1a494872f293f60d87f0d211cc5e219a` | 0 |
| src/ui/views/CommonPopup/CancelApproval/CancelItem.tsx | 767 | `f04d4f9feacdf3b9135736d03b8dc8a9b9519e53687653bef23860248c35f95b` | 0 |
| src/ui/views/CommonPopup/CancelConnect/CancelConnect.tsx | 1240 | `322e949e04045fda83980eedde334e67fba58f0b0a73b672c10b67e365c753b0` | 0 |
| src/ui/views/CommonPopup/ImKeyPermission.tsx | 1903 | `29dd20c9ff34a678042d41a144a67dad8228906dbeebf7831c06e60c84637ffd` | 0 |
| src/ui/views/CommonPopup/Keystone.tsx | 1728 | `248b48d1713e2395b63bad88066c7444f05f3d377c2af0e5b4abfae1882f840f` | 0 |
| src/ui/views/CommonPopup/Ledger.tsx | 2346 | `52ead2337380405d71ddb80055839a6c2ac965c07525c91be5f21e7bf16c884c` | 0 |
| src/ui/views/CommonPopup/OneKey.tsx | 2113 | `ebb7b94a4077833b19357873875e71f6cd890ffa2e623de56759c2dbec87b27d` | 0 |
| src/ui/views/CommonPopup/SwitchAddress.tsx | 1107 | `d96308d5ed9e7dc3edacbb6060c0f5d0942ff42a4cc040949ff68684b2b63c56` | 0 |
| src/ui/views/CommonPopup/SwitchChain.tsx | 1094 | `b20d19091f22e907916faaf69265de6c9230bb5bf767a9c8b11e3cd7135e8450` | 0 |
| src/ui/views/CommonPopup/index.tsx | 3410 | `50921b7aab166e9f34a5068cf313e8a22a1f80797efcb6f58454ac02d51efc25` | 0 |
| src/ui/views/ConnectedSites/index.tsx | 2126 | `9e1238e3932bb436233c6224f2c96c7b429ffc77173a586ff2452432c6cd0652` | 0 |
| src/ui/views/CreateMnemonics/DisplayMnemonic.tsx | 4103 | `4021e439d53b1e8ae0e3fd021034aa1fd289547a455789653234327a112c6810` | 0 |
| src/ui/views/CreateMnemonics/RiskCheck.tsx | 2390 | `dcef09ce4ddc4ebeaa5b7c20f2558a8e165147a6a687f6abc970999e20420488` | 0 |
| src/ui/views/CreateMnemonics/index.tsx | 857 | `6e159e4bdab6b74c0fee1855626e71b9b7a2415778d5ce71a1bdc5aa2c9fadbc` | 0 |
| src/ui/views/CreatePassword.tsx | 9008 | `d7a6d5d975b5ab4b1554dd9c2263e8e7bde810334e12165d0091a2bf25ca52a0` | 0 |
| src/ui/views/CustomRPC/components/EditRPCModal.tsx | 5299 | `70051a8aae4fa3de105987701fc0db2f755b0a630300a9984e4ff8181a3efcb4` | 0 |
| src/ui/views/CustomRPC/index.tsx | 9400 | `939fdc2949c6f9e2598373a79dd1788142857c5cf62f1afb805c35f101c6257f` | 0 |
| src/ui/views/CustomTestnet/components/AddFromChainList.tsx | 9825 | `9ed003956118e762280af02656e70da7cc7db2c00a24fe4c11a01b9d2be78989` | 0 |
| src/ui/views/CustomTestnet/components/ConfirmModifyRpcModal.tsx | 2299 | `9be6b55b77146ed7a214ea1a5838f0798039a8ad70680d67a21f09a529ffec6a` | 0 |
| src/ui/views/CustomTestnet/components/CustomTestnetForm.tsx | 4082 | `b3bb4a5cdfc955b6b0a48cf9d229b41dceb138aaae424387161d1bee42e75c79` | 0 |
| src/ui/views/CustomTestnet/components/CustomTestnetItem.tsx | 3082 | `d356d11ec7b9c2266bf2a32b1b42d3c30780cf1d2642276c9fab4e3961ad6872` | 0 |
| src/ui/views/CustomTestnet/components/EditTestnetModal.tsx | 7025 | `9da5906e98aa3e1765f929f2ba165d5f13b021fd494c405b2a2be8c9b9f45d03` | 0 |
| src/ui/views/CustomTestnet/components/Empty.tsx | 665 | `392add2f07d35a627bdc86a906a576ba5ab787f172139bfcdba7cdfaed7f7198` | 0 |
| src/ui/views/CustomTestnet/hooks/useRPCData.ts | 1370 | `9f1cf69c04a44c0eaa8ce77b67b14beced8f89fe728d8854f5c16c56995188d2` | 0 |
| src/ui/views/CustomTestnet/index.tsx | 5632 | `7207c547ca5084e4ad6d809d7b32bd8bb3573fb673d4f95f2d719fe259c7222f` | 0 |
| src/ui/views/DappSearch/components/DappCard.tsx | 6822 | `468bfcd73206ad7afdac5ac95195381bcd48ee2a3ae730a7a185b7abcc5df6ec` | 0 |
| src/ui/views/DappSearch/components/DappCardSkeleton.tsx | 1564 | `34dca7c2625ed5d1c06aa12f8ec7eb49d8a7d360aa9f50ccb61d30f47846e03e` | 0 |
| src/ui/views/DappSearch/components/DappFavoriteList.tsx | 1578 | `db84a9f08068ea2ea84c6e2cef02adc37087b4d6d81251bfc1be20df5998cfbd` | 0 |
| src/ui/views/DappSearch/components/DappSearchEmpty.tsx | 614 | `ba56449a5a3800bfdc2be8c9ebcdb2670b893b943894640f6a86de853d76ed73` | 0 |
| src/ui/views/DappSearch/components/DappSearchResult.tsx | 1589 | `24862aed07ba93a42e30ab57a4083ffcde339ad253eae04c40520f768e2388c6` | 0 |
| src/ui/views/DappSearch/index.tsx | 10182 | `89e795317702075c1ec083f9c684c410b239421ded9ac56ac135badbcd447de7` | 0 |
| src/ui/views/Dashboard/components/AddressRow.tsx | 5273 | `7603c6a66d9f157ae864d46f83ff46f20bb4d97e2d62cc143a8f95a6cb2f8a64` | 0 |
| src/ui/views/Dashboard/components/BalanceView/BalanceLabel.tsx | 2015 | `113c0d0ddc08797fbe00ccc29ebdcf792882a758a83ddf3c334a4c79f0a7598c` | 0 |
| src/ui/views/Dashboard/components/BalanceView/BalanceView.tsx | 17375 | `25bb7c16f68d2299bfd6128dec6e94b1e12aec50f5d5f55efeda45ec79b5dc3e` | 0 |
| src/ui/views/Dashboard/components/BalanceView/ChainList.tsx | 2405 | `ad7c2fd0d1e4993c0eb6e4590f78d554b66b228ac904655b9ef84ff51a7eb8cb` | 0 |
| src/ui/views/Dashboard/components/BalanceView/CurveView.tsx | 5895 | `082443c16eaeb806c22599a2cd169fc1aa2b1aa45618f62919f2d0f6835d5d0b` | 0 |
| src/ui/views/Dashboard/components/BalanceView/ZeroAssets.tsx | 1611 | `998656b3f8a66baace7ef588c6828f786652e69aeff91a191de845838b8893dc` | 0 |
| src/ui/views/Dashboard/components/BalanceView/useCurve.ts | 5167 | `bf193a25254cc5085364d9b853b8ee3659bc8eaf654d56a533a60bef58e5894e` | 0 |
| src/ui/views/Dashboard/components/BalanceView/useHomeBalanceView.ts | 4764 | `3d70d60038d391c4f500a41e13a2d07db7f687643bdfd52778e71e93aa927d0d` | 0 |
| src/ui/views/Dashboard/components/ClaimRabbyBadgeModal/freeGasBadgeModal.tsx | 13781 | `af99611656750d1c4f19c4ff7432d2b8cbf3e6c8b41c450e1a4109c185226b50` | 0 |
| src/ui/views/Dashboard/components/ClaimRabbyBadgeModal/index.tsx | 12468 | `da2d9bd06821da10de0ffe7ee101a04cf91aef40fd044dcc7590b02de8b2d350` | 0 |
| src/ui/views/Dashboard/components/Contacts/index.tsx | 3942 | `713bf1cd3e7478507c90de8252c69c00f08b90b27fbf2e8c8b1e0f4b73696b2b` | 0 |
| src/ui/views/Dashboard/components/CurrentConnection/index.tsx | 15117 | `17f2b8c18390f948eebf55982975a8be6b95e18dd69e7e270a1eaa2f83f3043f` | 0 |
| src/ui/views/Dashboard/components/DashboardHeader/index.tsx | 16159 | `71bd0a07c5e0c11f394230e6f7f08dd6eec681e9e4d87d39aad60ffe18027f77` | 0 |
| src/ui/views/Dashboard/components/DashboardPanel/index.tsx | 31135 | `4b8e54e803c98c781d364d15349bfb6c4f2b1e0b2c449119fc2bec2c6902eb89` | 0 |
| src/ui/views/Dashboard/components/EcologyPopup/EcologyContent.tsx | 1352 | `569b03b526163f69f319861a12284ca7a4f7fe28e6ea6487ffb5e1fd9b30c47f` | 0 |
| src/ui/views/Dashboard/components/EcologyPopup/index.tsx | 550 | `4d37cc1d00bfeaff573c08c5f5f57ef6e443bcfbffc6b2888ca667a705a12c60` | 0 |
| src/ui/views/Dashboard/components/ExtensionUpdateBanner.tsx | 2069 | `352ed0e6dd17b620e5574b3a37329f581a772fa0cd4fc24e4e1714a09dfb00ee` | 0 |
| src/ui/views/Dashboard/components/Feedback/index.tsx | 2906 | `9d95c9a45ec0639cf9c672d3030f08ad603dc083460bc75ebe9803f93b40127f` | 0 |
| src/ui/views/Dashboard/components/FirstNoticeDialog.tsx | 1373 | `a2c5f4d26b115f61c0e2cce4cd313cebb21b9b21760789b5063c18b3d2b5ae58` | 0 |
| src/ui/views/Dashboard/components/GasPriceBar/index.tsx | 4161 | `1741f39759cef05894063f281306ddba6cd6b25b131fd7a51dd2f4652ebf13c7` | 0 |
| src/ui/views/Dashboard/components/GnosisWrongChainAlertBar.tsx | 603 | `0f7946be5c017162f585b9577b763a4f229e25330baf871bdeed02fb83c4a4c1` | 0 |
| src/ui/views/Dashboard/components/NFT/ChainIcon.tsx | 649 | `24749858e411beef9f12b90002253e25b1264b707342bb48081998822e734d2d` | 0 |
| src/ui/views/Dashboard/components/NFT/NFTAvatar.tsx | 3949 | `4350f4b2b1ac91f234143171d12d518499960e5afcc0010ad8881a31f6ffad93` | 0 |
| src/ui/views/Dashboard/components/NFT/NFTModal.tsx | 4587 | `74ced6fdebf0e9a99e6dbef66dbbf297a0a50fe75dce5d2ae1cc09438d37908b` | 0 |
| src/ui/views/Dashboard/components/OfflineChainNotify/index.tsx | 5004 | `a9ac5bc941bc9b5d5a3384ba2a8723e3ecc5c138fe0850722d428580b8401e22` | 0 |
| src/ui/views/Dashboard/components/PendingApproval.tsx | 2329 | `49512e5b5a6282d1a99c79197eaae5e6897d85e413d8627cc73b22ef18e46ff4` | 0 |
| src/ui/views/Dashboard/components/PendingTxs.tsx | 1511 | `f3650f0c708f55546d2e780fef4fa36bddcd3bed352dad12e66fe107a11bd677` | 0 |
| src/ui/views/Dashboard/components/Queue.tsx | 1396 | `916d92cf020434b0e891eae3a16fbb28ea1d2a0aea49ed586ba32a7b47bd79bb` | 0 |
| src/ui/views/Dashboard/components/RabbyPointsPopup/index.tsx | 2195 | `0a8a920040280e66f548b3772b04cb323026d3b221c1f5ba2ce44c97f17a4058` | 0 |
| src/ui/views/Dashboard/components/RecentConnections/ConnectionItem.tsx | 3050 | `02d418c9d481ce278e53b08e36a02ff3224d793e1e8827361b7cb1cd5f91f053` | 0 |
| src/ui/views/Dashboard/components/RecentConnections/ConnectionList.tsx | 1365 | `8e2a56be39d7e02e4ee6882627cc6ed5ca3a6caa80bc4c84deb29cd595c966d3` | 0 |
| src/ui/views/Dashboard/components/RecentConnections/index.tsx | 5928 | `c9c766eab7eea3c34a27848c38eb830ab03a690570f48975e8c0408a4c783eb1` | 0 |
| src/ui/views/Dashboard/components/Security/index.tsx | 2959 | `f58193d8d9691e15fcc9b568016841ad055bed635d4aa3624fdc7f1a3078bc1b` | 0 |
| src/ui/views/Dashboard/components/Settings/components/CurrencyModal.tsx | 5757 | `b7b90470cbea31b40b570e54d6753d2fabea1a263b2d3854fd4179c1ef9daea2` | 0 |
| src/ui/views/Dashboard/components/Settings/components/EcosystemBanner.tsx | 1029 | `4f08e3fbd9035d99e2b2ba10cdb85bc4414918ba71d0869cf38a25b7b16ac1a7` | 0 |
| src/ui/views/Dashboard/components/Settings/components/ExtensionUpdateCard.tsx | 3825 | `51d9341204567efe66baec569dd163973da8e400948c4346185b14045279dfaf` | 0 |
| src/ui/views/Dashboard/components/Settings/components/ExtensionUpdateDialog.tsx | 866 | `d530a74b50ac8643f51e124f57449a4eef048477710f177fadf49eb78c731b15` | 0 |
| src/ui/views/Dashboard/components/Settings/components/RemovedTokenPopup.tsx | 7887 | `2d9461e0cebe212721016757f3593d56cb2873d626b355760a6106262c8535bf` | 0 |
| src/ui/views/Dashboard/components/Settings/components/SwitchThemeModal.tsx | 2164 | `c65f29260131ddf2ac5c214ab2f2ebe1360b66ed3817ef5fbf2b08c107db4606` | 0 |
| src/ui/views/Dashboard/components/Settings/index.tsx | 57593 | `f2cebd1f8957b0cfc1fd8221da3026eb0d57977cb73019b5ff842e4075b97507` | 0 |
| src/ui/views/Dashboard/components/StablecoinSwapPopup/index.tsx | 5584 | `07acf0caba2040aee5c6ba729d3fb60d21d7897a4310cd85048baac46e8ba8b8` | 0 |
| src/ui/views/Dashboard/components/TokenDetailPopup/BlockedButton.tsx | 1542 | `5efe232098b9466b4c9dd6f030509e4d1466479106750dd09e740f64022085ac` | 0 |
| src/ui/views/Dashboard/components/TokenDetailPopup/BlockedTopTips.tsx | 1624 | `8f356162a9756ec892d48a8f5cf467803e1c555ad094168c6bf86779114196f8` | 0 |
| src/ui/views/Dashboard/components/TokenDetailPopup/CustomizedButton.tsx | 1535 | `e0e9766f6000a3963099b878293a24b22bb1da0d3f98283eb865525235745eba` | 0 |
| src/ui/views/Dashboard/components/TokenDetailPopup/HistoryItem.tsx | 3074 | `7fb68ad01863d7a183ca9816d2e823cc005848f208b6c807f3dec25efb80ef69` | 0 |
| src/ui/views/Dashboard/components/TokenDetailPopup/Loading.tsx | 849 | `b29f9e841017f10566d20e22d71488a2b9d173b3bd9c81754bc8935aad5732e6` | 0 |
| src/ui/views/Dashboard/components/TokenDetailPopup/RemoveTokenConfirmPopup.tsx | 2939 | `ebc9fcc1b226577ab7a0c586bcbcaeefbc890b80a126351477c49ad9de3cef30` | 0 |
| src/ui/views/Dashboard/components/TokenDetailPopup/RemovedTokenActions.tsx | 5046 | `07513c439ad793829a90e56625e825c746d323ec953932304a412c63c20e9ce6` | 0 |
| src/ui/views/Dashboard/components/TokenDetailPopup/ScamTokenTips.tsx | 1314 | `43e4a63735065a14896f89fc505cc96e71f41b90fb602b5998f14181775456b3` | 0 |
| src/ui/views/Dashboard/components/TokenDetailPopup/TokenDetail.tsx | 22641 | `2efcc2c43794edef2cd38f80280023187209094aa1af2623753ca91dd3ebc984` | 0 |
| src/ui/views/Dashboard/components/TokenDetailPopup/TokenInfo.tsx | 17408 | `2f9b5d3fc76ed5613970fa25eee8e35ea7f46953647ef374d4aedfea101bb199` | 0 |
| src/ui/views/Dashboard/components/TokenDetailPopup/index.tsx | 3330 | `d3dbba4142873e4b612e6b927bd3be6822c83850a5a9bda5d63f3cccb46415e7` | 0 |
| src/ui/views/Dashboard/components/TokenDetailPopup/utils.ts | 678 | `d59a05e2c5f614a834e444ee46ef1990767ef99f7f8696e0701d2f3decdcdbe1` | 0 |
| src/ui/views/Dashboard/components/index.tsx | 250 | `b1c6a37222cd3335c4f33a1f479034bbf55ca5ca0208fa4248701e0fd3cfc3e8` | 0 |
| src/ui/views/Dashboard/hooks/ads/useStablecoinSwapPopup.ts | 5168 | `9b5bb07f2ff10bc140383953251b47e56393a6e03b097c0471efa04c76b4cbef` | 0 |
| src/ui/views/Dashboard/index.tsx | 9256 | `0c9b351a9b3a06f5a44e3afd5d8ebb99288af67777d967e13545a30276062ae9` | 0 |
| src/ui/views/DesktopChainSelector/index.tsx | 4138 | `b1a186c6d1c1632be37e38e8193bd6106145240bb3a2e82824d2e588e425a227` | 0 |
| src/ui/views/DesktopManageApprovals/index.tsx | 1994 | `3560def30273d962dde1f080dfdda41c42745742a9c6e969130e2732152cd353` | 0 |
| src/ui/views/DesktopPerps/components/AccountActions/index.tsx | 2864 | `5072975b1ce5997cc5c34918c2d04d27a31ba0670fa3fc6eb05205a0124de103` | 0 |
| src/ui/views/DesktopPerps/components/AccountInfo/RatioGauge.tsx | 2866 | `91bdc1f4d5b3e7b5dc1a4ff7f31f4578eb49d05f5e9e866e9ce378483fce7f71` | 0 |
| src/ui/views/DesktopPerps/components/AccountInfo/index.tsx | 4238 | `05a366f149af401f334f4889287fa21847148bb20df62b72007d43cdbc7b474e` | 0 |
| src/ui/views/DesktopPerps/components/AccountInfo/usePerpsAccountSummary.ts | 6649 | `780f2ea058e20de62f1b2b214d499a9c6313ee1278d2e537b7e7464f72ce28e8` | 0 |
| src/ui/views/DesktopPerps/components/AccountInfo/utils.ts | 12059 | `5f5cc1f8e8928721be8cd5eb3c32d5bd2be5fffa0714907c9e539404c5ce53a6` | 0 |
| src/ui/views/DesktopPerps/components/ChartArea/components/ChartWrapper.tsx | 8771 | `1c09c41ba9e53b792a7c56d9ae0fa0ccd5412e1a9ca445851055179c78108de4` | 0 |
| src/ui/views/DesktopPerps/components/ChartArea/components/CoinDropdown.tsx | 20323 | `65460929653168c9e8615df8cbae904f32f8cf2d62ac089a2e6db0d93eae732a` | 0 |
| src/ui/views/DesktopPerps/components/ChartArea/components/CoinSelector.tsx | 7815 | `620d940bc98f793367c1c292adf675095945be1af37477cfbba193ed97bd1e09` | 0 |
| src/ui/views/DesktopPerps/components/ChartArea/components/FavoriteBar.tsx | 3164 | `ab1634a8a073c3b6d1c2e1d5593644ec706cd4ac87da2e90007944581c8f0b14` | 0 |
| src/ui/views/DesktopPerps/components/ChartArea/components/HorizontalScrollContainer.tsx | 3774 | `0dc873d92dee5be38c025cdd45488118646856b36a1d0a2d4bfc9ce49ea41fb8` | 0 |
| src/ui/views/DesktopPerps/components/ChartArea/index.tsx | 1039 | `0d28fa8c94f4a633fc078f32e21354e46e86f694d90066435ee87ce7f1b837b7` | 0 |
| src/ui/views/DesktopPerps/components/DashedUnderlineText/index.tsx | 1390 | `8750bf4ae211ae3c532ba885dcfc6a90d11ff278bf94750ec26ddbab319e0c59` | 0 |
| src/ui/views/DesktopPerps/components/DepositWithdrawModal/ChainSelectPopup.tsx | 2706 | `c5501ef1b656d1263fd7aef7d1a28f25a9ff4de606542ab7b158b821eee2da48` | 0 |
| src/ui/views/DesktopPerps/components/DepositWithdrawModal/DepositPending.tsx | 472 | `d4100142ddb9014ea4e9bef386962ad01796e436ddeb871e24df61e5c12773ba` | 0 |
| src/ui/views/DesktopPerps/components/DepositWithdrawModal/HistoryPopup.tsx | 5537 | `0a9398c25333a1663dec81e24732acaca2652820a0d01384b480f21c2a0c03d8` | 0 |
| src/ui/views/DesktopPerps/components/DepositWithdrawModal/TokenSelectPopup.tsx | 9394 | `399db16d1075a0132ea72cf54dd1d883ac8b83d36bc6eb01aabc13c46b0bc44e` | 0 |
| src/ui/views/DesktopPerps/components/DepositWithdrawModal/index.tsx | 24724 | `838ad0da02be70906404a2b41ae789c092586e8e74b0d1e3804754ac0a99b377` | 0 |
| src/ui/views/DesktopPerps/components/DepositWithdrawModal/useDepositWithdraw.ts | 35958 | `43ac099c82ad74f244637448f0c798026e80a96c9c29c2f59167783484e6f2fc` | 0 |
| src/ui/views/DesktopPerps/components/DesktopPerpsInput.tsx | 1368 | `dfc29a78dd57ed6fca5fc77ca4aebb0b5892a669d37c3344c1f3ace6195beb6c` | 0 |
| src/ui/views/DesktopPerps/components/DesktopPerpsInputV2.tsx | 1980 | `92b33d02cbc5333227210e748414c06084e6bc8479a54bf7014722e61e1d8336` | 0 |
| src/ui/views/DesktopPerps/components/DesktopPerpsSlider.tsx | 2152 | `abcebccef2be93433e1b93a8b4a117ddfb796e3eee1c64f7e0ae0712d2ffe54a` | 0 |
| src/ui/views/DesktopPerps/components/DesktopPerpsSliderV2.tsx | 5409 | `e5fc4c1876ee5f7e365141efb8bb8bfe4f9b1c3e207fb76a3ceed1f20151a1bf` | 0 |
| src/ui/views/DesktopPerps/components/DesktopPerpsTopBar/index.tsx | 7979 | `57b0c80689df7bb775511507e272ea96b66e9cb57c5beaa0866164bb087916dd` | 0 |
| src/ui/views/DesktopPerps/components/OrderBookTrades/components/OrderBook.tsx | 24885 | `6945112b9ec4dd2a0bd8851794c506a4c7f49459f3501f0601a294fabae2607d` | 0 |
| src/ui/views/DesktopPerps/components/OrderBookTrades/components/Trades.tsx | 3017 | `dbe4055d22b119a283725186cbe9f38eced3d44724b76960428502ad16a65160` | 0 |
| src/ui/views/DesktopPerps/components/OrderBookTrades/index.tsx | 4289 | `1f523c37225a9fcda6b16f5af759ee428a9c8eb27a3188a3c8f2d5171f60db01` | 0 |
| src/ui/views/DesktopPerps/components/PerpsPositionCard.tsx | 3135 | `fb1bc40519c0d273f28d5ca1a2cb1ef2b2e9470a1a0f8597496c17c959b7d254` | 0 |
| src/ui/views/DesktopPerps/components/PerpsSettingsDrawer/AccountTypePanel.tsx | 5282 | `a6d8c5a52d91bc61a6a693900c83a45d2c6ae2fc8adc96cb024a0a0031180f0a` | 0 |
| src/ui/views/DesktopPerps/components/PerpsSettingsDrawer/OrderConfirmationsPanel.tsx | 2039 | `d9e168e1fcce76c231804594cdef8e0c53ede6324669f2e4835499672f54a6f5` | 0 |
| src/ui/views/DesktopPerps/components/PerpsSettingsDrawer/SettingsHome.tsx | 4226 | `64d407b0553e03f07b0cc40d5eb7c38a4ace4ce632e1d094f624c8e244ae0d2a` | 0 |
| src/ui/views/DesktopPerps/components/PerpsSettingsDrawer/index.tsx | 3510 | `b346b31538923b94f3564837e74fc445606822288c5644e2ae6851461fe351a6` | 0 |
| src/ui/views/DesktopPerps/components/PerpsToast/index.tsx | 3411 | `7012879c1b1e2b0fdafe3a1e3a5d54f9227abfd3b6ae7ac8d5e6229e47cf7a99` | 0 |
| src/ui/views/DesktopPerps/components/ResizableVSplit.tsx | 5411 | `baa7ccdc3f3e879a95adc64f1d24304d9dfaeeee5fa55cf2ae7e39c0e90d20c1` | 0 |
| src/ui/views/DesktopPerps/components/StatusBar/index.tsx | 24539 | `745c6d18925ae7a24da257dbf25654aa53400c275047e15b73e0787aabb32e41` | 0 |
| src/ui/views/DesktopPerps/components/ThousandsInput.tsx | 535 | `a63960a03e5541b13987acebe89219fe18aaf96c8a3c59f8c71adf32ad581bc8` | 0 |
| src/ui/views/DesktopPerps/components/ThousandsNativeInput.tsx | 1049 | `4d5812a5b53d53941b1a4767969cc0db5d5d9e12ac0f3c1517d8194cbeb1c734` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/EditMarketSlippage.tsx | 5570 | `6e7a3eb04d3d339723cc9195155d41a6f94cfa901c39c5693cf82f401b9d6233` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/LeverageInput.tsx | 3561 | `12735381bd8364e7478bdff9e4ddc54da2b440a8df7f3a336f97a2505232855e` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/LeverageModal.tsx | 4224 | `1a30876dbf93bec3d5d3d11210fe12697f8ce1b5e377ab917dc59842002133c3` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/LimitOrderTypeSelector.tsx | 1506 | `427563062e200e50ea002d68c4e84b95da82326b48d3b2480273025b99493dc7` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/MarginModeModal.tsx | 5445 | `722576933e4df2fc6c11bc6fd8fb17d2637c8ced8e718eb977b906a73df71c65` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/OrderInfoGrid.tsx | 3868 | `b2bcbad2d724ce181ad7ff7f80be1cb028d57628c7202b16ab1756ce30452d0b` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/OrderSideAndFunds.tsx | 2236 | `9cfacf48f54120034fc332c0fb0488581997fd4adbc4171a039be90b49e12074` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/OrderSummary.tsx | 4554 | `77c8ae61ceee77ca5407207b0368cab248c431a974d089f5d36e9e99ee68b21e` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/PerpsCheckbox/index.tsx | 4572 | `7c02b0092a6bf46a1e35c3c16cbeb7cc95afbd2b9a93e102564b82078313bed3` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/PerpsDropdown.tsx | 1429 | `180a0190e0c6fa8d5511b4fe8c859c696987bd19bd5b99ae8db3dc8bca6fba72` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/PositionSizeInputAndSlider.tsx | 10935 | `e1dd5ace1b2841612e11da9c088d512413594f46473a02c78b78ddf3803f7fb3` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/PositionSizeInputAndSliderV2.tsx | 13990 | `4655a1a27272d0da1467d60448d76dd920c5d8dd229bf27ea942c6f9039d66e4` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/TPSLSettings.tsx | 14647 | `a7f30175bf8e3c9e65aef3640eda3dee7a2f7e301c8a6e3990c31029f4a16328` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/TopModeStatus.tsx | 13507 | `830c5a843e817b98457c862deea00cb23f1cf931e864dc9e9dbf1e6c7a560d6d` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/TradingButtons.tsx | 8052 | `e140eb24107d5f0b32c6bd2370bc2b6d2d2aaa5dfa4c07c4e5fe272c4b90f675` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/components/index.ts | 541 | `8acd0024b283ad006b7fbf120c3a56c6d4dc36ae56446eba6e5cb3cf611f10a0` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/containers/LimitTradingContainer.tsx | 33420 | `cb959c77c0d74cf53e977434acba59259495bf8ceeb1df4fa3a716d72ff83de8` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/containers/MarketTradingContainer.tsx | 21158 | `10187d1b1e5bd2172026fc22c20ab43b5f7b03c219913c7a496a5ba39cad72b0` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/containers/ScaleTradingContainer.tsx | 17923 | `ac3baecc53907f2464cc14983a536cae0d1fcd883438203879028b4142ead255` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/containers/TWAPTradingContainer.tsx | 18253 | `9a59484413ebecea636840cdc4e36220a94b4260dee9eb72ba1ca249f3d0c297` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/containers/TakeOrStopLimitTradingContainer.tsx | 18182 | `301e628b0b4bcb000d098bda62ee397b430c086155d7a87dec04f5fc2e08529c` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/containers/TakeOrStopMarketTradingContainer.tsx | 13367 | `f7926332a623c62efc123933bc896d1061baecb0c799f6a7bd85ab609e506744` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/containers/index.ts | 432 | `eb7e528cc5397791eb39dac29deb8641fbc8b98d660d98f5f123fa7aa360e8ea` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/containers/takeOrStopConfirmContent.ts | 3878 | `cc0dc5abf070d48a410c46d0995186af17c730690443c49fc5100eda83a74e3a` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/hooks/useDirectionMaxGate.ts | 1468 | `e994d336e00119ae4105eec907c8390583de7b2dd12504985f2b5862e85ea985` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/hooks/usePerpsTradingGate.ts | 3234 | `10ab586a043cca181d72293cebaeaf0edb8d154e96866029db515aa209130dba` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/index.tsx | 2396 | `df70ece76fc07f7783d5351a5d5cc0dde770622f3c3647ffca929e8504dca589` | 0 |
| src/ui/views/DesktopPerps/components/TradingPanel/utils.ts | 9540 | `6d64de71481eea775ce61e6bd4cc333c01436d09429d7be4166ecf335d60e276` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/About/index.tsx | 1171 | `83e7c4dc01b2b551966500deb13f3e296b32701ab66b494844fd3b13457feb03` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/Assets/index.tsx | 6397 | `0375ce8d5a1b23bd6692408b898e74eb80818c22e8045ba6cb80f16328dd0685` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/CommonTable/index.tsx | 17893 | `ca63b68eaee00b8f39f65bfbb9ddcc628098a95da079ac591cf45226ee7e44ca` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/FloatingWidgetToggle.tsx | 3936 | `96adb6f600adf59d166b625a5f224b8f0618b47ead1c8ec2f0f520a79c71e4c1` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/FundingHistory/index.tsx | 6247 | `3138753edbc21c5cbb59b69cb71a07a1fbae76f69a01f44aeed67fafef38d50e` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/OpenOrders/index.tsx | 10711 | `65a427781a3333fb4d57fa5b0a0afeb0806690a2d9a59b56b5aaeea95ee62b2c` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/OrderHistory/index.tsx | 10605 | `6c13fc4bae677e1dc260c8f3d7b9a70355172bb45abdd2f84293ef06d0f6c980` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/PositionsInfo/DistanceRiskTag.tsx | 935 | `496073362ba27b409e507d3f03a6fc2502f2502e615dced4406b9222849416c5` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/PositionsInfo/InlineLimitClose.tsx | 21671 | `df0f5d1cf31c66a39c4ff999ad20653576c7fa71c0746e93cc80fe9c08cceb0f` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/PositionsInfo/ScrollAwareTooltip.tsx | 3790 | `07a4aa1fd54fe4f8fa7c110ff2ae02c5f5b25375634c2049f9663cd498997687` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/PositionsInfo/index.tsx | 28785 | `ca2dfae3b3c5b5dfd4fb026197d59db77bfb7940d59f2ada02f44c737bd26aad` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/TradeHistory/index.tsx | 8086 | `749432502c7b27cfa84276a285d5833a4f3e779f79bf25f7707e4e5e4b8d210a` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/Twap/index.tsx | 23973 | `456c47df84bb0642719d421bbca183f64dac6492f6a11fc9ed45e6c4ecf7e027` | 0 |
| src/ui/views/DesktopPerps/components/UserInfoHistory/index.tsx | 6405 | `716ecbb249afd84552290fa6ecfed6e1e181446ef695e27ae0204d97f3326d52` | 0 |
| src/ui/views/DesktopPerps/entry.tsx | 189 | `1773640dadaeff3e31039c2111a7fcb0f0e9d0819383a542105be4aefdd6583f` | 0 |
| src/ui/views/DesktopPerps/hooks/useHourlyCountdown.ts | 1211 | `0afae7f9ce068a9ed1694f5c738be93643e7746d4d5d6e515b8ee04b20639f43` | 0 |
| src/ui/views/DesktopPerps/hooks/usePerpsPopupNav.ts | 8117 | `e1faac48904cf9ac6693bc5cd0c82e2ea752b9dee5624c7d1bc3f7f1c0bf6a9a` | 0 |
| src/ui/views/DesktopPerps/hooks/usePerpsProInit.ts | 5700 | `8f0fd95c624e81593c3842a8d081ede0a6cb5aad2c365e6b05dcf88d1882e107` | 0 |
| src/ui/views/DesktopPerps/hooks/usePerpsProPosition.ts | 33748 | `22aaa13b8315259ced01c4d8f077e2cbd8392b6158d9276da4faf0c83c2aeabb` | 0 |
| src/ui/views/DesktopPerps/hooks/usePerpsProState.ts | 22044 | `88ff53fc2aaed5ec90df3a08e1ccb8f5dd5a3e73309f518b7da453d6b934ea2a` | 0 |
| src/ui/views/DesktopPerps/hooks/usePerpsTradingState.ts | 16640 | `0b0858552b47b3ad5ad8ee42c75145e5a6b3fc6880b5235f57632df3a1778563` | 0 |
| src/ui/views/DesktopPerps/hooks/useThousandsInput.ts | 3972 | `d3030167ac14fa1190bba1b5cd137ee0c77f2c871f72ca8cfda85a81759d0c7d` | 0 |
| src/ui/views/DesktopPerps/index.tsx | 8475 | `8e3248e634dbd7d7609a0e3be718c192b5d74ae8fcdc874c09002a0270040625` | 0 |
| src/ui/views/DesktopPerps/liquidationDistance.ts | 1161 | `527a6f9c794ce05dd49fa1fad4905f6ea052c05e8ef87f7ffad94a341252a5e9` | 0 |
| src/ui/views/DesktopPerps/modal/ClosePositionModal.tsx | 27802 | `c3dd548b4964d0dc5fcc45d8edebe302abff173840dc643d1e78dd4105b0ee19` | 0 |
| src/ui/views/DesktopPerps/modal/EditMarginModal.tsx | 14075 | `473432a8073ba04e000b27e27f3ee3cd7970db07258d6ffac8d9f3d89690b9f6` | 0 |
| src/ui/views/DesktopPerps/modal/EnableUnifiedAccountModal.tsx | 2625 | `cfe43d053fa65234689b24cd0d0cea5c4418b25fed88ed86b7bc7eb5ed4e0bb8` | 0 |
| src/ui/views/DesktopPerps/modal/OrderConfirmLiveValues.tsx | 5326 | `fcb4ff6094db6be8314105e71cec5d32d0a6aefbae5f4042c2cff279ce66766a` | 0 |
| src/ui/views/DesktopPerps/modal/OrderConfirmModal.tsx | 7737 | `c782d6b36833303eee580ea280a536be5f45e2b5ce16aeb1111842868bb261ab` | 0 |
| src/ui/views/DesktopPerps/modal/OrderConfirmProvider.tsx | 6626 | `de0b5cac4b4774e177f66ac3831bb7bd4e662028631b09f609e17f413c1d4b65` | 0 |
| src/ui/views/DesktopPerps/modal/OrderConfirmScaleTable.tsx | 5953 | `5c145ee1982799d5e6f9b1c905189cf73e04c08bbe0b754fe571d097666a5463` | 0 |
| src/ui/views/DesktopPerps/modal/PositionTpSlModal/PositionTpSlHeader.tsx | 4663 | `c4901ed26aa34d69689c7a2b9c879120dbbc1da63ab77a34c6ccf993f5a070d8` | 0 |
| src/ui/views/DesktopPerps/modal/PositionTpSlModal/PositionTpSlTabs.tsx | 1815 | `301f26ba88e02423ef43f98455b796930f36ba0b6086b34774e6c978715c706b` | 0 |
| src/ui/views/DesktopPerps/modal/PositionTpSlModal/TpSlAmountInput.tsx | 4911 | `4f0a8c3fbfc163feca4340425944e0f4597a27ac9726bfe4dcea10e2254faa07` | 0 |
| src/ui/views/DesktopPerps/modal/PositionTpSlModal/TpSlConfirmPage.tsx | 5004 | `83050021b5674b926294f66d93983b781fe532001f5c96e76a21283cb346a59e` | 0 |
| src/ui/views/DesktopPerps/modal/PositionTpSlModal/TpSlForm.tsx | 15829 | `2e47986abf0bd46cccb03ef22a7462cf0ffb4520dde8aeb60b12c82f746e21e6` | 0 |
| src/ui/views/DesktopPerps/modal/PositionTpSlModal/TpSlIntroCard.tsx | 1300 | `b3d97cfcc9f50a2d7dba9d941d391a7d6f9ed194b6fab7ab700a0774c6a4f5c9` | 0 |
| src/ui/views/DesktopPerps/modal/PositionTpSlModal/TpSlOrderList.tsx | 8479 | `d2c21b6840c94207740a256f90c23c504e500d21578d4e25e6d09b7b6e7fc470` | 0 |
| src/ui/views/DesktopPerps/modal/PositionTpSlModal/TpSlSectionTitle.tsx | 1181 | `f5423bc12b1c4ff53e5f9327766cbc02244bfccb6d4f123126a11701504f410f` | 0 |
| src/ui/views/DesktopPerps/modal/PositionTpSlModal/TpSlSideInputs.tsx | 7388 | `4cde945b8655b708e8dc967495b608d1c8f34c23082c27bb2cf0a43dbdbe64aa` | 0 |
| src/ui/views/DesktopPerps/modal/PositionTpSlModal/format.ts | 889 | `0df41caecebd8a750aefad17fdf61fd24d1645a982bbb26f2ec841958edbfefa` | 0 |
| src/ui/views/DesktopPerps/modal/PositionTpSlModal/index.tsx | 20552 | `a865449cbbd08b9225797aa3077ad2c112ef364f8baebd3a4428e5943591b33f` | 0 |
| src/ui/views/DesktopPerps/modal/SpotSwapModal.tsx | 14715 | `04fe5229816110e90875c8f0c8df857e9ac76831e279667f60de806617bbb084` | 0 |
| src/ui/views/DesktopPerps/modal/TransferToPerpsModal.tsx | 11411 | `4d1173fca6d6504cd6c8b627dc3709db04885a9aaa1da82c40b15e942018c8e6` | 0 |
| src/ui/views/DesktopPerps/positionTpSl.ts | 20283 | `d871223d9cba7cb21999e869887ad8ac35913aab2ba5a96dec4af5ba82d38992` | 0 |
| src/ui/views/DesktopPerps/tpslTrigger.ts | 1711 | `148533076e3448a26e7ab9fd0b06ad5fe0c5315a7b093245c56f47bf82e5dc82` | 0 |
| src/ui/views/DesktopPerps/types.ts | 2829 | `66c740d30319acad156173e7a72ca45d6ae9bd1be7c12a9c7cb7b945340a079a` | 0 |
| src/ui/views/DesktopPerps/utils/openDeleteAgentModal.tsx | 2227 | `40ab7f68c8cb0c9dac2da244dd0cc6ef7b410777d1acc4118a98f59ddb9ee825` | 0 |
| src/ui/views/DesktopPerps/utils.ts | 20502 | `2bf3d376db83909589aa94d79aeb44e8c6f03de7b6b38ad5f61e3d0b00e5aa75` | 0 |
| src/ui/views/DesktopProfile/components/AddAddressModal/index.tsx | 6126 | `a46aa5e3e36f03eb8f57d05295e1d1e5b5fc56400c4223147baabbc81c263687` | 0 |
| src/ui/views/DesktopProfile/components/AddCustomNetworkModal/index.tsx | 1159 | `512b35ce4d76bbe0b83b10d569bfd465a0f8c7c55707ab7019b8a28e77a9811d` | 0 |
| src/ui/views/DesktopProfile/components/AddCustomTokenModal/index.tsx | 1659 | `dff71b02431592112d70cd28b12e15c953e5ed71b42d9fe0cc4e6a0e99904eec` | 0 |
| src/ui/views/DesktopProfile/components/AddressBackupModal/index.tsx | 1364 | `494899710ef63d8ef3f8144e756f9474d07acc493ba8ca2f3d0e0b1ca1c91d25` | 0 |
| src/ui/views/DesktopProfile/components/AddressDetailModal/index.tsx | 888 | `4f2f0837462559e607744a13e8966445e2d776883fd9a700069e14d566141eae` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/ApprovalContractItem.tsx | 4834 | `2d66750798eb82a9ddd27e829223f987dcec6516707f4752b0b393706fbfa7b5` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/AssetRow.tsx | 1419 | `606fcf9418e77d02b0afce7c40899ad3a4d507c48c2529b1abf6c9aa25d73322` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/Badges.tsx | 2933 | `e4e0a1db4f6a9bf4146032d917efcf3c4a0a4413358946f0242317c9f40942bd` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/BatchRevoke/GasRow.tsx | 1554 | `73a9fca2ea9d3f53d3f0803e8b1a94ba19f5122cce192bcbca73cb4474fc566b` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/BatchRevoke/HashRow.tsx | 1631 | `3e13d900b5451282b307b380beac4b7185e98c10a844bf9120368b9c86781b50` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/BatchRevoke/RevokeActionButton.tsx | 1551 | `876e103d149fc65d5115ae5a6bd7765c0268a3393e3dbf00e47d067b745aa5ea` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/BatchRevoke/RevokeActionLedgerButton.tsx | 5389 | `124a91a4e40e9392675e81de35707c20b7267dce501166563fd55124f353f416` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/BatchRevoke/RevokeModalHeader.tsx | 3068 | `0bfad2ea6f93f5d02e27287c3f9cd2c01f197abd07fe8a739d613037acaa5ec4` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/BatchRevoke/RevokeTable.tsx | 5093 | `1a7426cdf3351d4d52212acdfbec5d5ee75722488eb66e9fad7fffde1143d3fc` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/BatchRevoke/StatusRow.tsx | 3051 | `cdb4e62904d4524d33f813c45f16bbd87bd31e15cdbbe07970255c2ab20d11af` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/BatchRevoke/useBatchRevokeModal.tsx | 2554 | `c949b093788c02c9dd96406b0167993d2abe2cebb81669f0e5755455ade71df1` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/BatchRevoke/useBatchRevokeTask.ts | 8267 | `56029fee26aebe74dd77eb2d87ea9e694cb0adacd7f328ea3e32b4b2cb6aaa48` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/BatchRevoke/useConfirmRevokeModal.tsx | 2605 | `35a1345dfd415b226c5cfe5adfd8f2e7c41570809b2e750ed37ac2d8f8891011` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/ChainSelectorButton.tsx | 3786 | `9d46607f85c744bc11855f93acde865eb769c59fc479803ad4728a5669a490ca` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/CheckboxRow.tsx | 1137 | `891e7fda0c40f173856a4899524bc66abe6ffa237b9e10e1fdd05184e5efdfff` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/ModalDebugRowItem.tsx | 4818 | `882a88add65db6760b08791f90ab7c45506e0987e9af8688b59d214c5217dcc7` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/NameAndAddr.tsx | 723 | `be487264437614cd253efc8f42b4f333a47a62bc05bf239206fe72fc9aecf5a9` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/RevokeApprovalModal.tsx | 19828 | `1802df863b7683ae04a103d8388533e04b8c1870731266cc78aab7cdfbfbc5ff` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/RevokeButton.tsx | 4504 | `a989f9d89ad39ca8ac67ed38757c8cb89efa1d938d6ae862ff02b1ed0e8537f2` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/SearchInput.tsx | 847 | `b2c54072dc59d8b0e55ed208d930546f02760aec9e5c0ca5bd056b583fe03ae4` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/SpenderRow.tsx | 2807 | `649a76332ef2ebb78b994ea485a3f88aa0c11372f97476a97b87523b5d247e41` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/components/Table.tsx | 12660 | `7c03ebfca2594f9875a37e247ebb1d1ad3bcbb61eea920635a1cacb2c00ab7a8` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/constant.ts | 423 | `7bdb9eb438bb06e431508f06097b2c431ef572d9488a783693c6a433dbfec729` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/index.tsx | 54440 | `9bf8ffaebf0bafaa7afdac64c6e3cd45f3d03c72a93e2e2595bf8fefe642fc85` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/useApprovalsPage.ts | 22274 | `37ae446f830706a655989ab020f5ae69c0213b047c216905226b3ad7475d21df` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/useEIP7702Approvals.tsx | 5653 | `32d91a4480810fcbc8efcd43e7c8298eb91e30af78aafac5b995d4fd1a543996` | 0 |
| src/ui/views/DesktopProfile/components/ApprovalsTabPane/utils.ts | 13202 | `380b27c8e5df1e674d861985251dac6ea023aba0ae5c787cacb1dfd5b60c6fe4` | 0 |
| src/ui/views/DesktopProfile/components/DesktopPending/index.tsx | 2057 | `8bf8af96f33212bc98f404bd49a02e6bd5de99faac0784bd3bf68bf116e66516` | 0 |
| src/ui/views/DesktopProfile/components/GnosisQueueModal/index.tsx | 727 | `55f12a6ebaa0458992077652de727286ca6cbea7eaf41aa2ca0fb399dfb95ed8` | 0 |
| src/ui/views/DesktopProfile/components/NFTTabPane/components/AcceptOfferModal.tsx | 22148 | `de91889ac9e99364d009fa70232eee98465620aecf6578643cb03b36563622eb` | 0 |
| src/ui/views/DesktopProfile/components/NFTTabPane/components/CancelListingModal.tsx | 10068 | `3c95bd2cff27d9692f71da1811df431a11a4f3a0670ca4b3a312312500ae2c65` | 0 |
| src/ui/views/DesktopProfile/components/NFTTabPane/components/CreateListingModal.tsx | 43809 | `72b2ed5a69a35c2e03d14b90583d1261f10ec8375c788e38e7e3b2c583936260` | 0 |
| src/ui/views/DesktopProfile/components/NFTTabPane/components/EndTime.tsx | 2263 | `f9474fe5ab27afdde41d6993283a0445e5969566d1bd1b5460440f349578015b` | 0 |
| src/ui/views/DesktopProfile/components/NFTTabPane/components/NFTCardItem.tsx | 2139 | `0c34422b794f2921876362bc56c896635be3bc9436a8b525452dfac7935575bf` | 0 |
| src/ui/views/DesktopProfile/components/NFTTabPane/components/NFTDetailModal.tsx | 24138 | `a398a50fda6521d2dffd9105677839dae4b4a138f39859c31a047850647bd298` | 0 |
| src/ui/views/DesktopProfile/components/NFTTabPane/components/ResultModal.tsx | 4582 | `9e13b704b09d34adb110ab5f692bbf37e4351e1afabfaaaa64285d057f4560ae` | 0 |
| src/ui/views/DesktopProfile/components/NFTTabPane/hooks/useNFTListingOrders.ts | 989 | `0b00f0e364259df1115d4d12380c96557d9314ebdca74995dd0474eadcc94e60` | 0 |
| src/ui/views/DesktopProfile/components/NFTTabPane/hooks/useNFTTradingConfig.ts | 403 | `77b96f12191c28af8e4a3ba3eaba3dbba1928875d0a2ad42676ed7f77c49e0a5` | 0 |
| src/ui/views/DesktopProfile/components/NFTTabPane/index.tsx | 11836 | `41db6620084f2266290e503ebb9350d149d0454039f2a0ca6e330de63d31f97d` | 0 |
| src/ui/views/DesktopProfile/components/ProfileHeader/BalanceView.tsx | 8927 | `daed803caaec588729fc5a1d5c3914e49a28ee61d24caed3925abb869b88b1df` | 0 |
| src/ui/views/DesktopProfile/components/ProfileHeader/CurveModal.tsx | 5811 | `2c08bdbf51fd867568b0f1284188844919f63741637ff731355b08c773d38ce5` | 0 |
| src/ui/views/DesktopProfile/components/ProfileHeader/CurveThumbnail.tsx | 5833 | `31d3adab599ac777b0bb959f2421d831a0f006de47ae2cb6feba7c5947e03b40` | 0 |
| src/ui/views/DesktopProfile/components/ProfileHeader/index.tsx | 2785 | `07b56d538a0354baa40e589991c78aa347a1f2fa54e1f2b1c6b88cd02c29d168` | 0 |
| src/ui/views/DesktopProfile/components/ReachedEnd/index.tsx | 537 | `bcf812671edc1a263a1c1999c67a1344555b72afc3b4991e2ba0570fc62bca33` | 0 |
| src/ui/views/DesktopProfile/components/ReceiveTokenModal/index.tsx | 948 | `365e69b8267b404413ebc1ba5a49fc42a189c689486eb5369aecfbe49e3402b7` | 0 |
| src/ui/views/DesktopProfile/components/SendNftModal/index.tsx | 1301 | `52056ca45a7b07459e68d5840f25822a7d386575771963470403191ebd9697d3` | 0 |
| src/ui/views/DesktopProfile/components/SendTokenModal/index.tsx | 1803 | `41194ee8afa4694a75ab7c12066136da3080de8c58da9945ea115cfe2fe124ec` | 0 |
| src/ui/views/DesktopProfile/components/SignatureRecordModal/index.tsx | 724 | `6793f2c262e1abc698f8d4b0f5c84b5f870cb983376193ed47523de30add0c7a` | 0 |
| src/ui/views/DesktopProfile/components/SwapTokenModal/index.tsx | 2692 | `d8639b5edadce84f5cd395ef06adfc9906856b0b43d97a6bf20cb855c6a67b72` | 0 |
| src/ui/views/DesktopProfile/components/SwitchThemeBtn/index.tsx | 1685 | `29b89e5f633ef83b256c63883ffeb72c26d168e07fcb647f8975bfd29b0eddc8` | 0 |
| src/ui/views/DesktopProfile/components/TokenDetailModal/index.tsx | 2509 | `73f0a936ecc4f9e865ea2eb7903565391737d4d819c6062a0f7567ce2c304a05` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/DifiTab.tsx | 2990 | `296247dbc72efb51e3722a8ce3a9b9be658cf65230a768c73fd9382b498efeb6` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/ProjectOverview.tsx | 4901 | `b576b0f3ce3c74c81ba45c180028d4c4a8725ca426ba0ec3e7f7743c8388db26` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/ProtocolList.tsx | 12975 | `2baa22a7386770f9b3d4902ab55aad1eaea2f974385b520a74107d3072eb6138` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/components/ActionRow.tsx | 2301 | `b70c7823be5be9302d879c5c62e78b8ae19bf317b8a79b67812c0305d286676d` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/components/BookMark/index.tsx | 605 | `476617d6ef7935dfb1a89adb0da37389c9b7e723a67e22f1b7b17d032474ac26` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/components/HelperTooltip.tsx | 838 | `effc813cb3ec50fdfca222584ca1bb024a8e3b2a7665620305993e5d6d660e42` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/components/LabelWithIcons.tsx | 1125 | `67885dc002f2b0d1232a277b8675cf2265f454335657511f7eb8bbb2c92460cb` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/components/More/index.tsx | 1129 | `f9aea197ce7ee82b47016a5264ba933b14a10379b6709ebc6f383aae2b77527d` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/components/Panel/index.tsx | 954 | `6450f10050d0104e88384dc004bbefb26c2c12a78022de8fd6b7f1d99c8057fc` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/components/ProxyTag/index.tsx | 845 | `532618290512c48748d5969270f54f9b877840e9ac74e3e689f429f485529db7` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/components/Tips.tsx | 1384 | `a94247d7c0c647d0666774389156509911214f3cf55f519b890553d3f80c5a51` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/components/TokenAvatar.tsx | 953 | `c3eb769b3b7d5a4792c579690e63de5b34ef97e8e0126171f729ea96ba46d1ce` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/components/TokenIcons.tsx | 2518 | `65893b5480b484d7bcf4473a87fc50c892957a9cc101ff52cf73b99a6a4132d6` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/components/index.tsx | 210 | `b44c91f1ae07df4e83c54a743facd575f29e5ba9538b39edde8b64c4cbf3c38b` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/components/table.tsx | 3851 | `b7258229d2ef2395837ec5503dd1a6e2fa669b011e35ca6c48000d9291f8a55a` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/components/value.tsx | 7592 | `41fc0f39cb9a43a915cc78d5d9a1372be2d7abebefc17a54004dc7837e2ef38b` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/Common.tsx | 4057 | `aee4773b8da4923995bff8c17c2a8a86cdd7dd92bcdb496de1e5408a48012216` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/InsuranceBuyer.tsx | 1298 | `631969d88d45825d5586c6e0b5ee5a98dc9287ef7b65f1e6143dda753860b658` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/InsuranceSeller.tsx | 3441 | `7c760e03c25b58cb65806fb550da1a9ba6d1f0c54c63b864cc78a8d97b6e8b7e` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/Lending.tsx | 7540 | `45ab357b294c908221574257c94c4af2e80ba9a63cc6ae0fc31a949682c751c9` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/LeveragedFarming.tsx | 3079 | `dc35e9bcb3f61744ed6a8b3558b61620380b0069104ecf3a6268c210bddcec2d` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/Locked.tsx | 3634 | `6dc03a396d067b84a7513488a8098a7ab30aeee784954d3fb0df6c06ca7dace1` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/NftCommon.tsx | 4536 | `b20138cc60be3a11d816a6fc46893d2b134c8e16648ab93ff553a7c9dbb9a7b3` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/NftFraction.tsx | 3539 | `56e525ea3c1f9714fc29881acd0c35a84ef037c616f52b8ae1d7b9c74a15f31a` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/NftLending.tsx | 9799 | `697c40f1f3a15d2a7bb5951ef96b3dbcc3fd49c59c878db6433b90729b8d3057` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/NftP2PBorrower.tsx | 1863 | `0571fef5afaec23b27c8dbbae1b5c7710b440d270c5277946cb50ddff1235aae` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/NftP2PLender.tsx | 1900 | `b73ea13c33a1162758dd386178d9710eaa0f0ddd734041ab62b2f3324e9b3b68` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/OptionsSeller.tsx | 2654 | `013530e1bbc62274b147efa9a32c8ad94914233c56cc6c70bc715b73516da7a4` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/Perpetuals.tsx | 2041 | `25e6dced3cdb423d8ff08d857f561672cbde68900833ead21e2ddd0d910d1e45` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/Prediction.tsx | 1399 | `a78fde4442cce0a4ac92131743f592d15603723902053f683add120490180786` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/Reward.tsx | 2029 | `4fcac842ff1991fe6560e222cccf7a686758471b4ce3e75d4a1e4b798977b845` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/Unsupported.tsx | 1661 | `d46d4fdd952778b097d2ccf6045f3a4614b598cbc386412acb4010cc8e493c02` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/Vesting.tsx | 3335 | `0d841f0b2becd5c2ef744d6d11cefd4f8e2f79c812af3be58fb28706a6f54ec1` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/template/index.ts | 932 | `051069c0d8fe9dcdec23a8e43198e2bd396cb9b79382635c25773c7731f308f6` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/utils/index.tsx | 1110 | `4a019c4e1ae3a6f38523348028f097e2cdada9913a153dc8a326918031b7814d` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/utils/nft.ts | 518 | `76a1d5c70ebaa25eeb8cb65c6dbadf65e45e73bb8dd484d8974b523592bc280a` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/Protocols/utils/table.tsx | 4302 | `eccd96acdef82eda3396aa59788753d67e40c93c0d7ee8bd52ec8203f8d30544` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/TestTokenlist.tsx | 8434 | `1528b1cab60b6c73e1efcf29b3d725e64a166e251effe0a3da9d6216e014d299` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/TokenItem.tsx | 8933 | `e008ae0c5c2d2209ff55daba403d28ea2fa0e9e8dd0b99c2bd563caa874e81fd` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/TokenList.tsx | 7783 | `60a6957dd2f895495b46c8ce0cf0392fa857ed1a9269002b579accd1d3a490ea` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/TokenListEmpty.tsx | 1097 | `ec240fdc6463bf9009feb31d52a038478aad49d2ce5acec70714fcff12102697` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/TokenTab.tsx | 5163 | `2c48955dd6dda6eb3c8e32f0b60a3c485ee500a925a32f7ca8215a0227bfe05f` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/TokenTable.tsx | 2724 | `b378ad5db0dae3c61a9af2dc9c0ee22f77ef4df5939656f91df9ae0e73b40853` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/components/LpTokenSwitch.tsx | 1094 | `139c625225e0982f6ec99937e94ae2cb5fa64643efa2689a042c0a296f86b73a` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/components/LpTokenTag.tsx | 1590 | `144b18c4deed054a96687dc285a9d23a84cfe67da2385829ae3cea99a8964b06` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/components/TopShortCut.tsx | 7356 | `b3195e36d4c6bf4737f8e880f3c1ea1a60aead6248b8d69820734da346575a32` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/components/switchTestTab.tsx | 922 | `4fca8b3a5ea2adee102b860c26ef224b191818a1bcadc2be880f33afa728f24c` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/constant.ts | 61 | `f0f385e51c7edd7921650ad1994028e0cb09dca22d94c096939484e6a076294b` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/hook.ts | 3137 | `06d2f0579fe0c6e195d373f388d0b988885ac7e7177d2823cc6f0be0ac3aec9d` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/useExpandList.ts | 1829 | `9adde7cdf732a2dcc23cf9e4a08da023287f9031bcd99607e132d17a684800c1` | 0 |
| src/ui/views/DesktopProfile/components/TokensTabPane/utils.ts | 993 | `c6f666bcf05be49eb860669c890031efbab059d7adcaf4510212e74a4be692b0` | 0 |
| src/ui/views/DesktopProfile/components/TransactionsTabPane/DesktopHistoryItem.tsx | 4216 | `9636539ca61ada5a5227d80c0bfbb7cda06f7f31c3394d3d56100c1d34fee3df` | 0 |
| src/ui/views/DesktopProfile/components/TransactionsTabPane/DesktopLoading.tsx | 3074 | `427ddd2831dc0239d83fd91afc3a42aeb6f74001706037a6ba05f115a819be44` | 0 |
| src/ui/views/DesktopProfile/components/TransactionsTabPane/DesktopTokenChange.tsx | 4618 | `5f215eee0140571fa7a16fc9379ce3944084e1e67d0d3275c924f3374b0d0ca9` | 0 |
| src/ui/views/DesktopProfile/components/TransactionsTabPane/DesktopTokenLabel.tsx | 2113 | `428b531d8646feba75a3e47d0079509aa5ce793fe774bde8bfffb321ec9e1c15` | 0 |
| src/ui/views/DesktopProfile/components/TransactionsTabPane/DesktopTxExplain.tsx | 4859 | `bae2368894b958a6f8c7a2475a5bedb6fb4842f533d780b3718572f4b1dd33a9` | 0 |
| src/ui/views/DesktopProfile/components/TransactionsTabPane/index.tsx | 2800 | `5016608335733baba37f1dd79733dd1b1a5f4ea4b43104d66b4653e3a9cd3e28` | 0 |
| src/ui/views/DesktopProfile/hooks/useDesktopBalanceView.ts | 5140 | `6501f78a44d2d6f6111766a687c4fc70dc58ba9a973f296cca0791e89ff28636` | 0 |
| src/ui/views/DesktopProfile/hooks/useListenTxReload.ts | 1026 | `d124a4ab57ee09970f545fe7912d695d9c81913856090744ea209ca2c35ecf35` | 0 |
| src/ui/views/DesktopProfile/index.tsx | 17598 | `ab6f7f45ed8965b908896e3eb4950cf252f5aadafbca3f3992db316bf47465e4` | 0 |
| src/ui/views/DesktopRoute.tsx | 3061 | `56c357d39c8901bb0a78fc12ef88d580d32f48c8dab4f59f59b396df849cde80` | 0 |
| src/ui/views/DesktopSmallSwap/components/ChainPillList.tsx | 6644 | `c4c5809e4b0ced279e7b415cbc6589e589ba380b5bc637b1c507c8a12a875580` | 0 |
| src/ui/views/DesktopSmallSwap/components/Checkbox.tsx | 1044 | `6fef73cd9cca8c3e8ea4adbdd7e93f5ba3070e5cf2c4a00b9fd9367ef719aa8c` | 0 |
| src/ui/views/DesktopSmallSwap/components/ExchangeSettingRow.tsx | 849 | `9aa890824de37c3b678b5453fd31da9b67d457f8361343622972f083d112b41d` | 0 |
| src/ui/views/DesktopSmallSwap/components/LowValueTokenSelector.tsx | 15057 | `1f1b1a935f0aa3aa624f0fbf8f5786f98cdbd0b1a8cb46354408f148ef9f69fe` | 0 |
| src/ui/views/DesktopSmallSwap/components/ReceiveSummary.tsx | 14864 | `ce8008e236b41d10fcd98185c0bfe05d85182d0144c9ca7efcbf63d3f8b8e399` | 0 |
| src/ui/views/DesktopSmallSwap/components/SelectPopup.tsx | 2844 | `7daf06b29eab6fef95b742293f2ab1642f7bc4b783f3542bf8793fed0759e76a` | 0 |
| src/ui/views/DesktopSmallSwap/components/StopTaskModal.tsx | 2302 | `842f08a4368c1c318ed92aa33735a3404d99d0e71cda099ee6c6cbf53db97d96` | 0 |
| src/ui/views/DesktopSmallSwap/components/SwapActionButton.tsx | 2277 | `0465b49fcd2bc807c846d565447c5293d11b812cdc5df32d8fc71553b20c8421` | 0 |
| src/ui/views/DesktopSmallSwap/components/SwapActionLedgerButton.tsx | 6161 | `7ae90c76b2b4a92d4cbbd86b02fd48768b01e0fd0a891835ba7c613cf2497662` | 0 |
| src/ui/views/DesktopSmallSwap/components/SwapAnimation.tsx | 3596 | `ba638a52ad08a6e6087283da646a148b008ba2f33d4f33e122b482e970402f0b` | 0 |
| src/ui/views/DesktopSmallSwap/constant.ts | 221 | `32e54578c2b2799dbc24f1cc0c0ac0a523297fdecc6908627a0f9796164c5868` | 0 |
| src/ui/views/DesktopSmallSwap/hooks/useBatchSwapTask.ts | 22261 | `5be7773723c5d2c47de11dfb557ec0520badbab4f0681eed09820522b5453947` | 0 |
| src/ui/views/DesktopSmallSwap/index.tsx | 9297 | `211900fd797d14f4b2d59cccab5457bd115c0544c8ab5914e9d9cc36b45d4374` | 0 |
| src/ui/views/Ecology/constants.tsx | 680 | `afb679bd723fb92aed089dd148706841925f7b00ba963ee6fecf36d0b154c397` | 0 |
| src/ui/views/Ecology/dbk-chain/Entry.tsx | 675 | `127a587bb0dbc0e9e0e2ce136a92ca03cdacedc5d8958ab2fae1c506ac98d83a` | 0 |
| src/ui/views/Ecology/dbk-chain/components/DbkButton.tsx | 1644 | `569ff055a56f5b9b39c1ef46a7370fc0d25f04d0dd8b6695d3a159390a3b7d8c` | 0 |
| src/ui/views/Ecology/dbk-chain/pages/Bridge/components/ActivityPopup.tsx | 16712 | `beeb24d51c25503ec3a2ec40ea26db7f2f04602f2d6547b8ce6163086ef303cc` | 0 |
| src/ui/views/Ecology/dbk-chain/pages/Bridge/components/WithdrawConfirmPopup.tsx | 5150 | `719616279be22e27e8be22eea8fa456af70229b04ccb144083b415df93f96c86` | 0 |
| src/ui/views/Ecology/dbk-chain/pages/Bridge/hooks/useCheckBridgeStatus.ts | 1146 | `f102eccace4df97534b8e63da0645a68db7e9a7eb3eea52670656257b9dfe01c` | 0 |
| src/ui/views/Ecology/dbk-chain/pages/Bridge/hooks/useCreateViemClient.ts | 485 | `70673bab9bd508410199560f3b458281f450af8566888801c06fb2035b0a6bd9` | 0 |
| src/ui/views/Ecology/dbk-chain/pages/Bridge/hooks/useDbkChainBridge.ts | 10222 | `8223162371e0d692ec1155a7ba27943aba4777beee4f0a970f3da7efbc00413c` | 0 |
| src/ui/views/Ecology/dbk-chain/pages/Bridge/hooks/useQueryDbkBridgeHistory.ts | 1012 | `74d1ee0d6009cdd698438617cefe5601d0b62ee47f706b6b0670807ad8f0a716` | 0 |
| src/ui/views/Ecology/dbk-chain/pages/Bridge/index.tsx | 15043 | `97be872d2a07b2ad1de469fd8ff625a01a26f8d9b6a4c863d555ecc91884ad0b` | 0 |
| src/ui/views/Ecology/dbk-chain/pages/Home/index.tsx | 2177 | `ba00fbb6a0c2425d8e6a1b49e3b0808a386c173c03c4d25bc7894f236c2b2923` | 0 |
| src/ui/views/Ecology/dbk-chain/pages/MintNFT/hooks/useDBKNFT.ts | 2164 | `9b96826bc7711f72f335f093aed8b85d59dab588ff39ec3f3998c2d5f6e3f1fe` | 0 |
| src/ui/views/Ecology/dbk-chain/pages/MintNFT/index.tsx | 2500 | `d013d4cff8feecf514ec0ee43b3004bd501754d5e14404a37eb151f497780278` | 0 |
| src/ui/views/Ecology/dbk-chain/utils/index.tsx | 4138 | `ed14656f180a8aa49b24a0b2c84cb1803b8512a431ee679ce475f61ea05bd6b2` | 0 |
| src/ui/views/Ecology/index.tsx | 669 | `19f863dd403127c19f7eec87e95f6e855a1f8bf348d7a864738deac3cf6bb08b` | 0 |
| src/ui/views/Ecology/sonic/Entry.tsx | 445 | `a4e9fdd7baf99314073ee14680935e7bf70ebec16cbc8f32701e0bc7fae5fa99` | 0 |
| src/ui/views/Ecology/sonic/components/CodeAndShare.tsx | 3819 | `b01fdb0bdfb59816d02a67facadd5df8aec70cc927bc329eb8fe7547a9123bef` | 0 |
| src/ui/views/Ecology/sonic/components/Icons.tsx | 8516 | `d005d5fec6094ffbb45c655692fa8a53eff41a565aacccd5d378eca9be184fdc` | 0 |
| src/ui/views/Ecology/sonic/components/MigrationBanner.tsx | 1707 | `fae66dda2eae24c26819d5e75f1bfd2d2e502c88a0d4f3731952c10164ae3aa2` | 0 |
| src/ui/views/Ecology/sonic/components/SonicButton.tsx | 1340 | `1cd4913058193670da2ddcc0895699b153ecf75149d68f586594d2465a239968` | 0 |
| src/ui/views/Ecology/sonic/components/SonicCard.tsx | 448 | `169872c02d5bec7f4e7485456b2bfe6b30fe0d592ceffc5b0b62ea8889eac769` | 0 |
| src/ui/views/Ecology/sonic/pages/Home/index.tsx | 6768 | `547803cb0d9b3c7c0e8d280d530370fccfef6461ee85bd6f1b62221d2a5295cc` | 0 |
| src/ui/views/Ecology/sonic/pages/Points/hooks.tsx | 2888 | `a65f0836ba0d259a7d3cee6aa2c610c6c491f110cb522a6adee8dd317e988787` | 0 |
| src/ui/views/Ecology/sonic/pages/Points/index.tsx | 4573 | `2a685445a033b8512db36d999fde3ec982e5229bcd1efcf90000ad23731c4917` | 0 |
| src/ui/views/ForgotPassword/CommonConfirmCard.tsx | 1535 | `75efb05836f3f0e139ea1b6f33fddc593ac5def25b9a9a1ad0cdda5c2cd4e240` | 0 |
| src/ui/views/ForgotPassword/CommonEntry.tsx | 983 | `48df817dba012a93fd5baa8cd7bcc1ab74648f230f16051fe3c87d18b13c1bb2` | 0 |
| src/ui/views/ForgotPassword/ForgotPassword.tsx | 4471 | `e287e8dda9ebf3d59f5dc0b19b12fa668246b602114ce8761f8e97ee95d02f26` | 0 |
| src/ui/views/ForgotPassword/ResetConfirm.tsx | 4502 | `7e37bc06497d930919c678cdccfe431ca39c2021404c74683dc98b0f33740c44` | 0 |
| src/ui/views/ForgotPassword/ResetSuccess.tsx | 670 | `c383e442d523ef04f9df452160ea12933355ac109a39421ca86e50888082d02f` | 0 |
| src/ui/views/ForgotPassword/ResetTip.tsx | 976 | `cac3f8f11f18edd177c403210e647ce3e6c15e41f14e3559252cc0c3b4416b78` | 0 |
| src/ui/views/GasAccount/components/Button.tsx | 1734 | `c08792cac24b4a3dd0cfe513a26ca23fc65a5d6ac36a99670423912a992a9010` | 0 |
| src/ui/views/GasAccount/components/GasAccountBalanceCard.tsx | 1171 | `bac256d4a83d41dc5b16a4af3e3a5046094b4bc056879291dc635e7a5a59b6ed` | 0 |
| src/ui/views/GasAccount/components/GasAccountBenefitsCard.tsx | 2808 | `10c94ff96f8621c4d153b221d713743674e07c3c9339900f1472ca21372858d8` | 0 |
| src/ui/views/GasAccount/components/GasAccountBlueLogo.tsx | 559 | `f2d4f03378f5f1818dcb58b1baf186c7ac07892a30efc9a5a1c811dfc666b599` | 0 |
| src/ui/views/GasAccount/components/GasAccountDepositPopup.tsx | 1695 | `388be1aec003ef867af2cf665e6a82b873b701b3950cc8188ef4d3b6046532c5` | 0 |
| src/ui/views/GasAccount/components/GasAccountDepositTipPopup.tsx | 96 | `47573ed3bcc1e987f11708a8978e2daba0e0bb4aed0316455e3e8c29b9c8d2a5` | 0 |
| src/ui/views/GasAccount/components/GasAccountDepositTokenForm.tsx | 43479 | `d759aa9da7a931b0407d14fe83aa9fab18598575ba690bddef5a548d82ddbba3` | 0 |
| src/ui/views/GasAccount/components/GasAccountDepositTokenForm.utils.ts | 4899 | `ed679a96655b739067f5b441596dce53fecb13c1cd4583827c4a412836091c42` | 0 |
| src/ui/views/GasAccount/components/GasAccountDepositTokenPicker.tsx | 9932 | `6aec3011b1765142c5d372ff1f362eb6dd4ed794220fb7f6d494eeb505277580` | 0 |
| src/ui/views/GasAccount/components/GasAccountEmptyState.tsx | 259 | `c26155d697fe42fadad49ab6c3b85e04274080c4110b0d476722f6d4e49cf42e` | 0 |
| src/ui/views/GasAccount/components/GasAccountEmptyState.utils.ts | 369 | `d6729b5303feddfd03c2a63144f18121c9ed8dd58958fb3cd7c5f5f03bbd9943` | 0 |
| src/ui/views/GasAccount/components/GasAccountLoginPopup.tsx | 4281 | `75101e48e7b8062492af244655c40b0aa8bd6dbdfca8803f058b6c1c5bb2230d` | 0 |
| src/ui/views/GasAccount/components/GasAccountLogoutPopup.tsx | 2386 | `ed2695deb556b8a072559613ddadf43c369e074bb05eb94144f0cf34097f76f5` | 0 |
| src/ui/views/GasAccount/components/GasAccountUserState.tsx | 855 | `387e427f9ff5bcd8b1faa51e6c0c0add2545765b8dff75e330fa8b2c5b407bf7` | 0 |
| src/ui/views/GasAccount/components/GasAccountWarning.tsx | 569 | `648c8e495afa39412abfea298561b3fdae7afee2e5f2c39c01bd73156f99090a` | 0 |
| src/ui/views/GasAccount/components/HeaderRight.tsx | 2962 | `8f30b18a09cd70c7c5eeee525f891d991b677966f8c38fe16a27f0cb1e3b0c4b` | 0 |
| src/ui/views/GasAccount/components/History.tsx | 6499 | `1f20e9783f1ce7c8211d51800f9e49044ac4d6fa27e9ac9322bfa0f938e29208` | 0 |
| src/ui/views/GasAccount/components/PopupCloseIcon.tsx | 358 | `86ad112e6d2ca23435e6a72ed37702a79109588166123c219f216ad0cf1a2a49` | 0 |
| src/ui/views/GasAccount/components/SelectGasAccountList.tsx | 6003 | `ac4e58ed90b7ace508d23d1d502c9d178de31b8fa919d3760e239272e2373f82` | 0 |
| src/ui/views/GasAccount/components/WithdrawPopup.tsx | 21420 | `709b7a4ec93da65ac7111e2b18f79e9e41bf6ed01be8df11298ca5554a292d31` | 0 |
| src/ui/views/GasAccount/components/WrapperBg.tsx | 398 | `76257bb992cb3b02f1baa63fbf66dbcd79d01030bb1180b956dd4abe60584b56` | 0 |
| src/ui/views/GasAccount/components/depositUtils.ts | 7408 | `dac812dd0dcc4200cce05f648f7360d50b6d3fe00301a083a2eaa1593ed5c9c7` | 0 |
| src/ui/views/GasAccount/components/topUpContinuation.ts | 3514 | `d13b20fc393b8812f1f41537bfcce5bdbeb4cae1826c5d1c29c55c31f8e65d4c` | 0 |
| src/ui/views/GasAccount/hooks/checkTxs.ts | 5382 | `36b50f476af046816566afdb113e68c0d986a8cf329c317a48a637b6a1575863` | 0 |
| src/ui/views/GasAccount/hooks/context.ts | 341 | `4cb8cda1189461b365a5572ef40397e9c33da9a17f5467ada2d717cf82ee56e8` | 0 |
| src/ui/views/GasAccount/hooks/index.ts | 27113 | `03b344812d11f36edd89bc77acc25e996678f16a9ca25da0935178c2ece6ba94` | 0 |
| src/ui/views/GasAccount/hooks/runtime.ts | 1026 | `2fb23a114dd745f59c0e082528b888680ca2be038c3a1f1835ed50c28394e2c5` | 0 |
| src/ui/views/GasAccount/hooks/useDepositTokenAvailability.ts | 13913 | `91b7459ebcd3cec62e139660ab789e97fa4c8b73c9f259fda10e6ac8dbd12e20` | 0 |
| src/ui/views/GasAccount/index.tsx | 11489 | `87dc9e161f084d25bfbde70094801419894e4e18745509ad159e393421ff46df` | 0 |
| src/ui/views/GasAccount/utils/bridgeSupportTokens.ts | 3041 | `ef929f1245dad9b56d7458c10520e03182555bcbd716caaff892f3a34a3f86dc` | 0 |
| src/ui/views/GnosisQueue/components/GnosisMessageQueue/GnosisMessageExplain.tsx | 2390 | `28f8fd11cdc51421aea39568181acfa51930fd9ffc8ccfffa465dfac7ba1c4d5` | 0 |
| src/ui/views/GnosisQueue/components/GnosisMessageQueue/GnosisMessageQueueConfirmations.tsx | 2758 | `e18b7bd97a890788deee3ff79bc4182221dc32c75da94844c663a4a768c64ada` | 0 |
| src/ui/views/GnosisQueue/components/GnosisMessageQueue/GnosisMessageQueueItem.tsx | 3341 | `714af0a03a57655dc52e4626d331e898231a6f16731866821c356650955deb00` | 0 |
| src/ui/views/GnosisQueue/components/GnosisMessageQueue/GnosisMessageQueueList.tsx | 4992 | `1993ceea052f7dbf638c6214d94d95acbc92e9a8e484f7c5cd7f8e7357461ef3` | 0 |
| src/ui/views/GnosisQueue/components/GnosisMessageQueue/index.tsx | 3286 | `41801540f73f02d18009c5a22ef7e2cea38da5d73af0c6e7e7528ddfbe0bdd59` | 0 |
| src/ui/views/GnosisQueue/components/GnosisTransactionQueue/GnosisTransactionQueueList.tsx | 23689 | `eeff0255371205567642857c075f3b3ebf872798b8924a2493cce0f418be5a50` | 0 |
| src/ui/views/GnosisQueue/components/GnosisTransactionQueue/ReplacePopup.tsx | 2938 | `30ff52b151694ffe1f3888ec5ff473bad5e47c84b053f42be8ad1ce78e23a117` | 0 |
| src/ui/views/GnosisQueue/components/GnosisTransactionQueue/index.tsx | 3292 | `df9c5dc9330cb9e7d4188b2f4bcc5df2334a7aee004f5651b83f90f47efa9550` | 0 |
| src/ui/views/GnosisQueue/index.tsx | 3287 | `895557bda96732b9e83d6236ba8644645d2c0c7bf3a0ee4206b2d04d306ce78e` | 0 |
| src/ui/views/HDManager/AccountList.tsx | 14072 | `7ed44bb386a6e2c0af4e398f5a13cb483d900500b786183ed6fcc989434adf39` | 0 |
| src/ui/views/HDManager/AccountListSkeleton.tsx | 496 | `17f6bca522f1b3282c7e6a3d405820bbb5a8f1f3cba81984b09b57350ad795e5` | 0 |
| src/ui/views/HDManager/AddToRabby.tsx | 1157 | `8ea1eeb6de1b1396781d5dac2b200bfc99cc5c596fe91283c4627a22d7422c7f` | 0 |
| src/ui/views/HDManager/AddressesInHD.tsx | 5322 | `d6bd267c604c2bdc7b5416d31f0270cce94973899161e062ce0d19f008249a32` | 0 |
| src/ui/views/HDManager/AddressesInRabby.tsx | 329 | `2cc39f452897fe5c08b8e9d25e9d6099427ad54c02f6d600eb9cacddf22e41da` | 0 |
| src/ui/views/HDManager/AdvancedSettings.tsx | 10850 | `a7afc0215b6aacbf1c462327e233e48e7fe6653b217adeaf64c9f4ded8b2439a` | 0 |
| src/ui/views/HDManager/AliasName.tsx | 2192 | `37230de144924b8d8b5956035c003e8f543d615fbf3ed8c1cd2d58df242fd974` | 0 |
| src/ui/views/HDManager/BitBox02Manager.tsx | 3435 | `0f1169479a2ec2a917183b4cf07fc8e8a76c5a1da66b446b0f5bd6002c0a05d1` | 0 |
| src/ui/views/HDManager/ChainList.tsx | 975 | `0c48068fdcbfb545f2ff6e1e91a32ca98cf2a400c25da5d330738403feada48c` | 0 |
| src/ui/views/HDManager/GridPlusManager.tsx | 6316 | `3ab9b7be5966832c74d9696e9de9bfd3a7c714485dd91f556825b66ad434db93` | 0 |
| src/ui/views/HDManager/HDManager.tsx | 12185 | `4329ff143b393bb516d7e129d45c621bc649932d20cbbaf3be4df6e002794a42` | 0 |
| src/ui/views/HDManager/HDPathTypeButton.tsx | 751 | `6b1ffb65a7c4dd0bc5f643f64abe26d9d9133d1c6316546a7b919e157236befd` | 0 |
| src/ui/views/HDManager/ImKeyManager.tsx | 2915 | `de60d79354846f9a0fbe0e19905532500bac593ae548998ec41ef17c1ebe3e2b` | 0 |
| src/ui/views/HDManager/InViewport.tsx | 434 | `d8bcffebd4a24e0e3ea0842df39ccb0828bc774dc125f036ca75b942a6e70ca1` | 0 |
| src/ui/views/HDManager/LedgerManager.tsx | 4816 | `1a1af12fa6b9a4a93b6142b94bd4630260111261845fef594ecff1ba2ffdcc62` | 0 |
| src/ui/views/HDManager/MainContainer.tsx | 2240 | `3106d39e0607662415554ae42d1443c37add93d59397380ae17cad9de1d0c04e` | 0 |
| src/ui/views/HDManager/MnemonicManager.tsx | 3037 | `c9a3f2863ac16d7b89f5a500294e320010007153a85d7ee06bba269310171f39` | 0 |
| src/ui/views/HDManager/OnekeyManager.tsx | 4687 | `a94614088ae87096068678cc60de876489fb8727759bcced275e6b45597c4b39` | 0 |
| src/ui/views/HDManager/QRCodeManager.tsx | 6929 | `334fc8f46881e1247a28ee1cadccc800cdbf157bc80821d14c0f5002e7bb62c4` | 0 |
| src/ui/views/HDManager/TrezorManager.tsx | 4404 | `a79b9eef632dadf4030f084273396903b42a39092fa1b59cf9c2412f8378ceee` | 0 |
| src/ui/views/HDManager/hooks/useQueryAccontsInfo.ts | 3023 | `9e2f44995f9423c5f7d2954a63bd4bd8e8c7289d15a29f92a751dd2ae320bd38` | 0 |
| src/ui/views/HDManager/utils.tsx | 7733 | `7b09ae381addbb51d81b6021e14bb2bf7b3dfa14c71362ce71643e39ccd0dd5b` | 0 |
| src/ui/views/History/components/HistoryItem.tsx | 9346 | `dd2738892d734e13a119a651f4f4ceb027ed0f6c5800309ebe80d059a61ab88c` | 0 |
| src/ui/views/History/components/HistoryList.tsx | 5769 | `c4c91977e226d2cb068d42656515ec278d8c1cfd1dec51bdfa5595f6b3c13b92` | 0 |
| src/ui/views/History/components/Loading.tsx | 921 | `2fccbd9dea0fe92e69d142a5312041ef7b7b5642130a1fc4e3e80117f28cbe19` | 0 |
| src/ui/views/History/hooks/useBridgeHistoryByTxIds.ts | 4631 | `7a129a12c6521ae7a50e75ad7224cd586461e837cc88575881a115030f951a23` | 0 |
| src/ui/views/History/index.tsx | 2651 | `7a932847c56a82a537f492fb7d0ce3857046fd2ec7692f4bcc6c7813a0afcb94` | 0 |
| src/ui/views/History/utils/bridgeHistoryLookup.ts | 6438 | `c1e0ba5f783579fd810252ff3a723d2360e0decb66fafb686225af05b29022e5` | 0 |
| src/ui/views/History/utils/mergeBridgeHistory.ts | 5266 | `9d2bcd97b950a61ad560a5a567b36082c945d8f63f72d9699148fe5e7f2ecc7e` | 0 |
| src/ui/views/ImportCoboArgus/AddressInput.tsx | 1443 | `5559ae98037b490d960185033735023332d29ccb13f0dc2e17f8a3af99ca4a79` | 0 |
| src/ui/views/ImportCoboArgus/ChainItem.tsx | 1064 | `4ab8a5fcb5bcbd9cf206faa5eda08012b558382bfecc8b198b69e7b39cc3af22` | 0 |
| src/ui/views/ImportCoboArgus/ChainList.tsx | 703 | `a60802f23a2f34643ef56fc348ff91185f436e3488e05fb61fa0c6abd51be796` | 0 |
| src/ui/views/ImportCoboArgus/Header.tsx | 1361 | `f0cdc0045361011058578ece6af6cbf03b36dbba51b4a1c222ee3d4a9072db7a` | 0 |
| src/ui/views/ImportCoboArgus/ImportCoboArgus.tsx | 6919 | `1f700413bc581f88a7c91b53287f6ee9c87fbbba11583f8aaac7707f3a070373` | 0 |
| src/ui/views/ImportCoboArgus/SelectAddressPopup.tsx | 1719 | `34f2c3bece43e3bc9a0adfe5e80696e09bc10bf9ca9cd934dc5e852e76c922b6` | 0 |
| src/ui/views/ImportCoinbase/ImportCoinbase.tsx | 5011 | `1ec71ee3ea86160b540ee52ac1a80773f4b8fd71c2c5d28075ff0bbf4c0151cb` | 0 |
| src/ui/views/ImportGnosisAddress/index.tsx | 8001 | `a3511e0c8784757196da9c6cd742d98dcd1541adf0a85d2974949d5c8e7d4443` | 0 |
| src/ui/views/ImportHardware/ImKeyConnect/index.tsx | 2090 | `d50cf8fdeb9938607971f9f186a4cc746fc9550864c4d511255a9314f70aa775` | 0 |
| src/ui/views/ImportHardware/KeystoneConnect/index.tsx | 9429 | `9844e08016f89e8075c01c30c5b18b5de36bce9b85bbad021d1501e5124e15a0` | 0 |
| src/ui/views/ImportHardware/LedgerConnect/LedgerBanner.tsx | 2218 | `d2a4aa09cf55aba04efcbe9e821af2a5860bc3f65ba7aec330b6769e29bcc8b0` | 0 |
| src/ui/views/ImportHardware/LedgerConnect/index.tsx | 2878 | `1b9dd938ea73269231179325c878c45e75885e2cd584bcbb9a68179149657ff5` | 0 |
| src/ui/views/ImportHardware/OneKeyConnect/Bannder.tsx | 521 | `177936fbae211f74fae15146a9419e93609f87c5aeee8c7b66be4b327696adbc` | 0 |
| src/ui/views/ImportHardware/OneKeyConnect/ImageCarousel.tsx | 4153 | `91b834926a00235236c238aaca326538ff5fb217263c9b06bf07a76e092a30a5` | 0 |
| src/ui/views/ImportHardware/OneKeyConnect/OnekeyBanner.tsx | 1982 | `e8847718594eb173f8ead7a6bc38e07e8a550d1723438f612386faa35a9e3792` | 0 |
| src/ui/views/ImportHardware/OneKeyConnect/index.tsx | 10166 | `04abd9f62bba2ec054a2041aaa164c9957f2cb0eb0c9ab0db3cf577886fa8514` | 0 |
| src/ui/views/ImportHardware/OneKeyConnect/utils.ts | 691 | `a0947eaeff82d238d01ace19069fed10e4ec01f168ffb9bae7fead040339f156` | 0 |
| src/ui/views/ImportHardware/QRCodeConnect/index.tsx | 5862 | `df7d7c90b97799dd2ed0b7b0fc2dbad39a7caa1f72205b56dd962646bebd84f8` | 0 |
| src/ui/views/ImportHardware/TrezorConnect/Bannder.tsx | 521 | `3a9cba7c85e93d83e91e8b1149a9acabd4c5be74d7fdf5cf55d097f66abb94f3` | 0 |
| src/ui/views/ImportHardware/TrezorConnect/index.tsx | 1303 | `36fcc63da449325649d02e166852a1f715885186d898810d16402e0b85f8c6d5` | 0 |
| src/ui/views/ImportHardware/index.tsx | 1112 | `12aaa08e118b30bb42a73901faeef3a18f2cf9db3171ecdef62d8a9eefaf0a52` | 0 |
| src/ui/views/ImportJson.tsx | 3555 | `cee87f206a8d0375871c14e4f9dae02c280de6e56bceb3118e6a1f60bc24ffc0` | 0 |
| src/ui/views/ImportMnemonics/InputMnemonics.tsx | 7244 | `1c40a0aa9c8a13eee895c5515f0c4df0462f61d7c0e2ae17a35aac6dd7ac4c62` | 0 |
| src/ui/views/ImportMode.tsx | 2687 | `58f266ca98fb2454ace8653486aee0a1f76d6892cc2c5370a44236580c8fd776` | 0 |
| src/ui/views/ImportMyMetaMaskAccount/index.tsx | 6534 | `daf594f7c42db83ece52ade7668a3046ae228f026b0f306a9a3b3d3cb379c099` | 0 |
| src/ui/views/ImportPrivateKey.tsx | 7832 | `7412bd45b1b3e03b0bc7767b2476edd250697a2191109aacd806beddebffe7c8` | 0 |
| src/ui/views/ImportSuccess/index.tsx | 10812 | `bdfb7365278828e2a939f48cd9a28749fbb7e1cc5db22c99a95960e8e34259b9` | 0 |
| src/ui/views/ImportWatchAddress.tsx | 10649 | `dab1ad9104519dd5b83611d09bbbdc35cd8a1131f7cc51f5f33a9abd08da9752` | 0 |
| src/ui/views/MainRoute.tsx | 19284 | `31d42ff940561e33bfbfe2377469b1d4ec51107b85c38c9c5af55bac78545f4f` | 0 |
| src/ui/views/ManageAddress/AddressDeleteModal.tsx | 2950 | `2a2d8c2143f8aec7a4b5f0c1095a282b6500d90039640e6fc7f983b8ff974466` | 0 |
| src/ui/views/ManageAddress/GroupItem.tsx | 2038 | `86b74cee395694016830519add187250c703e3aaee3a79b4bc5fddaeb10d2aab` | 0 |
| src/ui/views/ManageAddress/List.tsx | 4927 | `87e38d0233c14f8fc104efe61c86793c1f1ca17fd74a71ab175731679528aeed` | 0 |
| src/ui/views/ManageAddress/SeedPhraseDelete.tsx | 1683 | `03cc1a31ed140b37152317c3101eb19f4ed63d15411d48dc609444829fcb6b3c` | 0 |
| src/ui/views/ManageAddress/hooks.tsx | 9783 | `7ef84dcb7f4be3bc30834b4fadd6fb573fcbdec59b5e8e790a42884890b2ce7d` | 0 |
| src/ui/views/ManageAddress/index.tsx | 15120 | `f621f81799d52f05952397cb08b2580e97dd162221d316a1b82cfb6f8ae4b6eb` | 0 |
| src/ui/views/ManageApprovals/components/ApprovalAssetPopup/ApprovalCardAsset.tsx | 3826 | `51703b7ca9b12783e3a3cb17937a7091ba214a2730efd9e022aeeb626b77f369` | 0 |
| src/ui/views/ManageApprovals/components/ApprovalAssetPopup/InModalApprovalAssetRow.tsx | 3934 | `b3985650d224b4b44afd8d513889b0f8527f4de2837928398339679f60085235` | 0 |
| src/ui/views/ManageApprovals/components/ApprovalAssetPopup/index.tsx | 4969 | `e57351684c7350e364c29c4d815507018bb5d7b7accdc8e0ab6f85d2212a828b` | 0 |
| src/ui/views/ManageApprovals/components/ApprovalAvatar.tsx | 435 | `e0bd77da5f3a0bee60cdb65400f6c9829401452b5d201957d9c094d1db289eac` | 0 |
| src/ui/views/ManageApprovals/components/ApprovalCard.tsx | 3111 | `07c3463114f59a0e5a938e015077499111b532da22545d04a47159d49d380f21` | 0 |
| src/ui/views/ManageApprovals/components/ApprovalContractPopup/ApprovalCardContract.tsx | 3505 | `38258028efb44865c44271a9c3b757c7e9b5aceeee6e80fb9cb232e45ae0a622` | 0 |
| src/ui/views/ManageApprovals/components/ApprovalContractPopup/InModalApprovalContractRow.tsx | 6866 | `07639fc20b29912f6542c02cf628277f1b149254ee5d8209cb3a32e2c36db375` | 1 |
| src/ui/views/ManageApprovals/components/ApprovalContractPopup/index.tsx | 5073 | `bd0f2121c78e2f2db58ce1f968f25c99626f465e1920c6fc3393f5378b022197` | 0 |
| src/ui/views/ManageApprovals/components/ApprovalsBottomBar.tsx | 2370 | `f98526c1ac9bac18b015e2ac091e6d9ffaf728775329849f4aa36caa87b2d87d` | 0 |
| src/ui/views/ManageApprovals/components/AssetAvatar.tsx | 2701 | `ce4fcb6fbc457fa643dd6e95d4bb8a8c6c82fc70993ff494d000dabec1cd5d65` | 0 |
| src/ui/views/ManageApprovals/components/EIP7702Panel.tsx | 8634 | `d32046de3d834221d700d1b4ead708a84a860b14ef41217a57277cc5262582e7` | 0 |
| src/ui/views/ManageApprovals/components/EIP7702RevokeList.tsx | 659 | `629d601ddcdc5f6b2f3e985834da737aefe33341013dcdc01330e3b61300f7fd` | 0 |
| src/ui/views/ManageApprovals/components/EIP7702SupportedChainsPopup.tsx | 2033 | `85c1ea41489bdf770c794895daf98500eaf7d8ee859314afa26b8f3de4dc9761` | 0 |
| src/ui/views/ManageApprovals/components/EmptyState.tsx | 857 | `72bec35984bf483cccfddf814048dd660ff2c66ed0842db4b9e2f88ea3848718` | 0 |
| src/ui/views/ManageApprovals/components/ListByAssets.tsx | 2425 | `f829e3a9d67abf27b122fe01bfa0ec5e8defea2659e83a912e27c981035b8d95` | 0 |
| src/ui/views/ManageApprovals/components/ListByContracts.tsx | 2141 | `77aca192af5f77ac006028a93d5af1700fb9c0d311ef7d42da29beeb770ee349` | 0 |
| src/ui/views/ManageApprovals/components/RiskBanner.tsx | 700 | `b5be55433b23cba9d1f1fe31191b92fa63342d9c390c6e8542bb350d24660cdc` | 0 |
| src/ui/views/ManageApprovals/components/SkeletonLoading.tsx | 731 | `4c5545387096a6f7ffdd7676ccc198166e9e13aa940888f7714106e5dd015974` | 0 |
| src/ui/views/ManageApprovals/components/index.ts | 784 | `f9c661cf741a455a692beb8ff58dfa65f44f19e2a2b6aaf47b888c09d514355c` | 0 |
| src/ui/views/ManageApprovals/hooks/useEIP7702Approvals.tsx | 10863 | `14f43da18860c8d43b8805131b097b581c1f89f08c77dfc3af2328602cbf7d15` | 0 |
| src/ui/views/ManageApprovals/hooks/useManageApprovalsPage.ts | 32821 | `6594ac0db9fd8c925764ae9bbb9aa633e469bdb4277c851aacce4e02abeb73f8` | 0 |
| src/ui/views/ManageApprovals/index.tsx | 4858 | `c6072d8cae31a7af157ecb4022260b7fcabaf69a42d90e6c5d48d77fba68e3f7` | 0 |
| src/ui/views/ManageApprovals/utils.ts | 20265 | `a3e4ea11f3595c666582bf9d5ae1ee60603951d471a06e9805d6085b51c45217` | 0 |
| src/ui/views/ManageBatchApprovals/components/Cell.tsx | 532 | `241da8f8a6e67800511359cf6fa271ae00b4e3590196ddf2c50a43aa1c0c72ea` | 0 |
| src/ui/views/ManageBatchApprovals/components/ListHeader.tsx | 970 | `2e2dc53b48efaf7f78ee6d114cb9f240c3851182be54e23bbb57d6c980d420b0` | 0 |
| src/ui/views/ManageBatchApprovals/components/ListItem.tsx | 1084 | `9ae38f94a0a6be9f675da962e0a3812d7cc340f05489f5c375a75b94142096d1` | 0 |
| src/ui/views/ManageBatchApprovals/components/ListItemAsset.tsx | 698 | `3aa482dfdc2a7f5d9a656689e06759813fc8cb6acdd9bc30a3d165d3b3d9816f` | 0 |
| src/ui/views/ManageBatchApprovals/components/ListItemSpender.tsx | 714 | `a7762e6cac34713a2acadb0d8cce683180d4235833aac3e876b19dda4acb206c` | 0 |
| src/ui/views/ManageBatchApprovals/components/ListItemStatus.tsx | 3453 | `a0ce9c040e31638fb788ef29c7479a0ce7fc0608dbf38df41b21dfab779e2929` | 0 |
| src/ui/views/ManageBatchApprovals/components/RevokeActionButton/RevokeActionCommonButton.tsx | 2005 | `8829d1492d56feff1ad496db7829fafbee4122e4d13f72304472feea48bf4206` | 0 |
| src/ui/views/ManageBatchApprovals/components/RevokeActionButton/RevokeActionLedgerButton.tsx | 6720 | `8e93cddf8ab295f8d6a92ec2b2b64a47116190e3ff68d0160b80b0d7504284b2` | 0 |
| src/ui/views/ManageBatchApprovals/components/RevokeActionButton/RevokeActionOnekeyButton.tsx | 6750 | `63ff3b2789d13b7919f45b248255918b542b05800e1aa709c5b0e40f2d6d381e` | 0 |
| src/ui/views/ManageBatchApprovals/components/RevokeActionButton/index.tsx | 958 | `b62774a51b2d27f3baee71820f72247c7eb2d145a58d8df516dea4aac830b2ca` | 0 |
| src/ui/views/ManageBatchApprovals/hooks/useBatchRevoke.ts | 2318 | `ce4767418b10c07ba2c42f4d77f23561fd96d23a26e310357d701fc6611e7051` | 0 |
| src/ui/views/ManageBatchApprovals/hooks/useBatchRevokeTask.ts | 9606 | `52a4bbc153a97ee485aa6713c4fbe460a4d6ab72dc16da02488df2621d0c048c` | 0 |
| src/ui/views/ManageBatchApprovals/hooks/useRevokeOne.ts | 1687 | `2a0bb3dc3507f625aff0ad860e40c8b07a1f1a35d6a89826d4df5af15ffea71c` | 0 |
| src/ui/views/ManageBatchApprovals/index.tsx | 6576 | `aafd4c82b4123664a4f8ab955102217b8796bcdf1b21018ad6c55b176d4f2add` | 0 |
| src/ui/views/MetamaskModeDapps/Guide.tsx | 5822 | `7f13f70d0e1d0656604dd014106465cc3bb8784640b35fa93421e640257189e0` | 0 |
| src/ui/views/MetamaskModeDapps/List.tsx | 2175 | `52f18eced0f7bbcf056c3684c14520b72ea22dd8a959f8a31620a89fc5674924` | 0 |
| src/ui/views/MetamaskModeDapps/index.tsx | 98 | `2f1746a0c358a1d488c755b30a8d144c50cf4d371f15e062e004ae0156957753` | 0 |
| src/ui/views/NFTApproval/components/Loading.tsx | 1131 | `510593ffd00f61a12fba8de99cbaa4361adcaebc7b6e68d67f43d7d0f41f73bc` | 0 |
| src/ui/views/NFTApproval/components/NFTContractList.tsx | 1465 | `0d41635544090a41ce04e9b1dedd7e21e9f430c46589681196d149fb41614fef` | 0 |
| src/ui/views/NFTApproval/components/NFTContractListItem.tsx | 2013 | `8eac38d7cdf977adca7b47ae11132f7644318f61ca6c9c347a907b756d7abf00` | 0 |
| src/ui/views/NFTApproval/components/NFTList.tsx | 2129 | `ee0ba6768cc655ffad24d9701a73fc087f72dbb5983c19bd4d952117637f265d` | 0 |
| src/ui/views/NFTApproval/components/NFTListItem.tsx | 1449 | `a414f459d8b6918a3c8685d2117fa83cbd57a354deff67825adbb0a40d250da4` | 0 |
| src/ui/views/NFTApproval/components/PopupSearch.tsx | 4330 | `a3bbfbbe6a89fe99025cda8c614bd52522ae6aa0e49d9e285967bec77b5cba7a` | 0 |
| src/ui/views/NFTApproval/index.tsx | 5951 | `d0269710d2f2a81fcca2079aba633d05585e484c2928bcfdc075a4ed0a8190af` | 0 |
| src/ui/views/NFTApproval/utils.ts | 127 | `06d24b5d1cea2ca0394a8ac5f2e2729494ab1c6c34d367c6dfb9e7b4f485fc8c` | 0 |
| src/ui/views/NFTView/ChainIcon.tsx | 863 | `3f46bb0a9a04f6541d93cd9a972d53c9486427cbaa67d483168910981d82f8b9` | 0 |
| src/ui/views/NFTView/CollectionCard.tsx | 3116 | `5ae90fc73882174845514ab316e7e8ead5fc92aec8cd0ac9640b096fcad26cc1` | 0 |
| src/ui/views/NFTView/CollectionListSkeleton.tsx | 368 | `4e37ab0733ce7df4898c208c811036758aaa93020e49b6bfa19da4fc12425116` | 0 |
| src/ui/views/NFTView/NFTEmpty.tsx | 1880 | `7f933768f72af25d2ba7a36ec16bb394b02ac67dc2ed982c154b806f24e17a77` | 0 |
| src/ui/views/NFTView/index.tsx | 5529 | `73fabfb21dea00ee98db6d7daacbadd2dc13bb1391722c5a65744e9c06ddaa22` | 0 |
| src/ui/views/NFTView/useCollection.tsx | 2472 | `baebe21647ee6411080e657bc9f065f19ffb034a0ea177e797fa31599bdaf9df` | 0 |
| src/ui/views/NewUserImport/AccountItem.tsx | 801 | `5e77dcd55430f38e3da0ef41d392cf2dad6061c6abaffad225a9f26c07e03813` | 0 |
| src/ui/views/NewUserImport/BackupSeedPhrase.tsx | 5548 | `72af1e5bc684082977ecb2f65ec4653f40af6848028f2dd325d93036a9d308ca` | 0 |
| src/ui/views/NewUserImport/CreateSeedPhrase.tsx | 2628 | `f61323cc25a26acb696cf17a98e645126e37b92724ce736af150524c23e7b2c5` | 0 |
| src/ui/views/NewUserImport/GnosisChainList.tsx | 1440 | `625b70142ae23f5bf19e6580ba3f75947708a399229ec980a6e9346877a003b3` | 0 |
| src/ui/views/NewUserImport/Guide.tsx | 2910 | `fdbbc402aa66669cec8bd3c8b1bf4f947c83667228cf97b22ef4df633cea93f1` | 0 |
| src/ui/views/NewUserImport/ImportGnosisAddress.tsx | 6105 | `4eb09cc48396f1c16dbfcaaae1eb97c62e89d36bb0d61393004fc2444c5e2d58` | 0 |
| src/ui/views/NewUserImport/ImportHardWare.tsx | 5382 | `b8c1924133bc99c668ee2ab6c81df67eea9d39ef58f557a2d2b6514fca84b71e` | 0 |
| src/ui/views/NewUserImport/ImportImKey.tsx | 2882 | `d37ac97bfd3d681e0673e2876a1972e545977eed2f1831cbeb6da28bf0fa7905` | 0 |
| src/ui/views/NewUserImport/ImportKeystone.tsx | 10635 | `a388d4c51d899362ba612d39fd6faf1e73574b66adbd480a349a07d05da70b2e` | 0 |
| src/ui/views/NewUserImport/ImportLedger.tsx | 3945 | `0daa31104bf4ec23927e354b71f6e7666b9aab0c12e6dbf69e33aca83c94b7bb` | 0 |
| src/ui/views/NewUserImport/ImportOnekey.tsx | 10436 | `1cd63bd7d90defabd680d7a9388fde689e0a5f4538060b8754ee556a2366c3a0` | 0 |
| src/ui/views/NewUserImport/ImportSeedOrKey/ImportPrivateKey.tsx | 5310 | `f8495e6013d58d1002b979d23c7c3226ed00df3321125d80ec14ff746957ed31` | 0 |
| src/ui/views/NewUserImport/ImportSeedOrKey/ImportSeedPhrase.tsx | 7653 | `1efa267280dbb9c74c4842f78ba0dcdefabf8f62bcf59b46812ae1826123ef64` | 0 |
| src/ui/views/NewUserImport/ImportSeedOrKey/index.tsx | 2011 | `46b3af2e7889dc37a374bbab9c72a89c55e2c90e37b82c709a3df180e84f3478` | 0 |
| src/ui/views/NewUserImport/ImportWalletType.tsx | 4848 | `05ae2d3f046d96edea9934345a65e3b72a7e8f5c7dc30d9312c220d28878f966` | 0 |
| src/ui/views/NewUserImport/PasswordCard.tsx | 12137 | `57d8dad464e3862ec18f7448be52a580c8c14e1bd0f05e87b56296c5fea80542` | 0 |
| src/ui/views/NewUserImport/ReadyToUse.tsx | 5280 | `719c1d72bd9f7f5529648f19a5b0f93376651296d521000efafdb7a23e32b232` | 0 |
| src/ui/views/NewUserImport/SelectAddress.tsx | 619 | `8ed0831c683fbe3520860b47bae50bdf65738bbd3c79e92b081c3f6ea7872c99` | 0 |
| src/ui/views/NewUserImport/SetPassword.tsx | 6603 | `6f4d081ac9f6bc0d736dc1951a7624a6b9d997013b441e7f257213e846892ad1` | 0 |
| src/ui/views/NewUserImport/Success.tsx | 13366 | `74c34ce75f860d10ea09b051548f0133ffa06fc33e97eb672adc848e8485ab68` | 0 |
| src/ui/views/NewUserImport/hooks/useHardWareUnlockAddress.tsx | 2091 | `0c138e0bd71e00fc687342b3e269c85658749519a781625efb811c973adf5e40` | 0 |
| src/ui/views/NewUserImport/hooks/useNewUserGuideStore.ts | 423 | `17d5fd781c2f4044cf5131f55ca31dd101054f5353296d2888181153b7cb8f94` | 0 |
| src/ui/views/NewUserImport/importHardwareList.tsx | 4756 | `1271b37bd167ec0ccbaaaaad06f1dd499e68e6b225fec558b2b26b782899f942` | 0 |
| src/ui/views/NoAddress/index.tsx | 531 | `b10e93bb4578cc42d7a725ed904e7af01f7883ce4caae86ee75bba318173df37` | 0 |
| src/ui/views/Perps/candleSubscriptions.ts | 6704 | `34525994409584205a3c980a8aa5e6556eb0de62b0b9fd6fba56618f80855bbf` | 0 |
| src/ui/views/Perps/components/AssetMetaItem.tsx | 3812 | `73926e7d1ca929855f7138a7ec8bf5cf28fc162012f1e82ed16dfc6fff8f2856` | 0 |
| src/ui/views/Perps/components/AssetPriceInfo.tsx | 1838 | `a2a1db690b638c239fa09b2d42a959ff29831ff771350e29ca06e29a7b533765` | 0 |
| src/ui/views/Perps/components/BlueBorderedButton.tsx | 1026 | `023b3f6176af43903e826d408fbd660c9a08bd901ae21d03c2099da2eb7e64e9` | 0 |
| src/ui/views/Perps/components/Chart.tsx | 24592 | `d1d10198fa6fe7a34e1856753433dc7b732c657e4ee5ebd3f39dc4a4446f3362` | 0 |
| src/ui/views/Perps/components/EditLimitPriceTag.tsx | 8220 | `2310a6cf077f87b89a7e638751e66cca6741171e607d9ee0b36372b97ae422df` | 0 |
| src/ui/views/Perps/components/EditTpSlTag.tsx | 16467 | `f9d04f3f336528a638fee233c53a41d72cbb13eacf912e0f99879b3a102984e6` | 0 |
| src/ui/views/Perps/components/HistoryContent.tsx | 5001 | `225703709b28e65a95de2bbf06d7794ffe48b1b8056480ba2290aece6a42c853` | 0 |
| src/ui/views/Perps/components/HistoryItem.tsx | 9816 | `f38f84d71048fe3ecbc091ba3ddd119eb2b80358197cfbe50ca73fa11883a3c1` | 0 |
| src/ui/views/Perps/components/LeverageInput.tsx | 3693 | `050099ba9acae60288fff45caabaa0ab97b8e4f05275d19f6122f66fca3c6097` | 0 |
| src/ui/views/Perps/components/Loading.tsx | 4549 | `fcd0a07542b6fdd5427a3258c4c01f8a64bc11d3a56ce9b5d2717b30602556f5` | 0 |
| src/ui/views/Perps/components/LoginContent.tsx | 1715 | `aa61f59c69c0d682a435a4a1372bb99cdae0dd889dc35f07f9193673505f6086` | 0 |
| src/ui/views/Perps/components/MarginEditInput.tsx | 4653 | `a0d485cc0ed6c28cdefd75431b71b937a35cbba58cf40466c55a8738f19d79f2` | 0 |
| src/ui/views/Perps/components/MarginInput.tsx | 5735 | `6ea27ed04ff36a53f0296b96b05a82902e1d3b5177ceb6ae181a9ef782916c4e` | 0 |
| src/ui/views/Perps/components/MarketSlippage.tsx | 2329 | `51580f3c535d1dbaa4fb143364ff9277586c2e7a555d3ab6482e8e795ccf8b33` | 0 |
| src/ui/views/Perps/components/Modal.tsx | 2173 | `9815694e8141c199301f5252d496177aca27f8e622f05907a84672d8ba501552` | 0 |
| src/ui/views/Perps/components/PerpsAbout.tsx | 1443 | `330fc3d6f5e4d431a17d6bd1ef0327a6b4097c749c43d9c1f907de9dfefb4691` | 0 |
| src/ui/views/Perps/components/PerpsAccountCard.tsx | 18647 | `5c5b42523445a05d046dcc7a26bd1c88bde42375ddf7b888a67268dbdda12cec` | 0 |
| src/ui/views/Perps/components/PerpsCategorySectionHeader.tsx | 1130 | `094c70e15f3182700ca2b03dd07e14b66c12a0d39bd454828aaf88193ee56c56` | 0 |
| src/ui/views/Perps/components/PerpsDisplayCoinName.tsx | 2439 | `cadda6495035201532bc41a5627aec2b02f2689fb252ad085d80107f6a5538d6` | 0 |
| src/ui/views/Perps/components/PerpsHeaderRight.tsx | 2320 | `0cee5fe053f7b7dca30120f308135788c435a8dbecaf3933c993505c441c7d11` | 0 |
| src/ui/views/Perps/components/PerpsLimitOrderItem.tsx | 4702 | `6cb86468518da866ec4dfc0a673c5b255cfe919423eb6589d095d8e71be7befb` | 0 |
| src/ui/views/Perps/components/PerpsLimitOrdersSection.tsx | 4676 | `6f1fc22a8c8665ff9557d5fd51e18870f37180dce383f6919a2dfaad56670b07` | 0 |
| src/ui/views/Perps/components/PerpsPortfolioBreakdownTips.tsx | 3405 | `ebb55eff8e2ff92b8dc30a026e678e2da0e5c7f988d2f7c73730a6d69b6b31b9` | 0 |
| src/ui/views/Perps/components/PerpsPortfolioChart.tsx | 11055 | `f1038136a4037bd12aa7324f12d17a257cc9f3d40ca95a9d02e17d3d20579bc9` | 0 |
| src/ui/views/Perps/components/PerpsSlider/index.tsx | 990 | `6a1504392f6a363157b5a6d3bc202bba69ea7758e463ea4a913e084871936b07` | 0 |
| src/ui/views/Perps/components/PositionItem.tsx | 7040 | `3dd92d92ca65df933cacd6cb3aa966b81daae7c1ff1ddd0ab179e4fd070b022f` | 0 |
| src/ui/views/Perps/components/SelectAddressList.tsx | 13164 | `46e550430873baf3bbdebf6b8706420b66088f4357237985a9c74be07048a97e` | 0 |
| src/ui/views/Perps/components/TokenImg.tsx | 1491 | `55a942253cca24cd020ad6a2efba11b5744650651bf5df514fdbd110117226fc` | 0 |
| src/ui/views/Perps/components/TopPermissionTips.tsx | 540 | `f92393047240cb5f2b7aaddaf4277eefdbe8322df81404ed58a44d6a2f893bb6` | 0 |
| src/ui/views/Perps/components/TradingViewIframeChart.tsx | 29911 | `bf21b81be8e7421d65657fa277696c58889dae8bd40915b5070cdc1404062111` | 0 |
| src/ui/views/Perps/components/quoteAssetIcons.ts | 553 | `f2108576ebfee2680beac5d1081ecaf71e09a5392254094123dcf38e3b84beea` | 0 |
| src/ui/views/Perps/constants/perpsCategories.ts | 267 | `eb84d5637866cc373c4ebcd99a245d971d9d960416145e69ef769f3fcadb433d` | 0 |
| src/ui/views/Perps/constants.ts | 9171 | `e4685dda6992def9589089422e237bbe26f6f8cb415e555d91f44a00951634f9` | 0 |
| src/ui/views/Perps/hooks/useActiveAssetDataCache.ts | 2953 | `e5201c9a06779d0ec52a21c1abc6bdfb30a612033af1c11a24ed620b5d7e4907` | 0 |
| src/ui/views/Perps/hooks/useActiveAssetSubscription.ts | 1471 | `7a5a98e016891ac4e52ff8d67ac7ebc613977cb92aac785f28950004434e53c8` | 0 |
| src/ui/views/Perps/hooks/useHypeWithdrawGasReserve.ts | 1537 | `a4e9f5d6bd583f449ea5d1ee752aa0c72fbba4dd715d0ea58a08718060e32ec4` | 0 |
| src/ui/views/Perps/hooks/useLimitOrders.ts | 2429 | `1b761528d684939c66bf6e1e6b107948c6ef98080f00a5fe5790f253fe30cdd8` | 0 |
| src/ui/views/Perps/hooks/useMarketSlippage.ts | 2193 | `0f46fb0d9ee8c2d1fc51feda31b582b0c5ac28e833801597c80173f451631370` | 0 |
| src/ui/views/Perps/hooks/usePerpsAccount.ts | 6105 | `2fb13271f9c3f1924544d3e1e2065ce94ce915da0ab59319eb23f4ecdb157150` | 0 |
| src/ui/views/Perps/hooks/usePerpsActions.ts | 7043 | `5011f557388177b6fb8bd3c208b0090b48ab7356fd42548def280166eb2fe78f` | 0 |
| src/ui/views/Perps/hooks/usePerpsClearingHouseState.ts | 573 | `6c00a7b2d24285eb2d9e1cba5d4696d078287896c3e1d6df690342fd104acce5` | 0 |
| src/ui/views/Perps/hooks/usePerpsDefaultAccount.ts | 4210 | `c0a9a8ae048c90ca34f4b86daa9979524a012d528ec821ed4a3da4e72ebedda2` | 0 |
| src/ui/views/Perps/hooks/usePerpsDeposit.ts | 12508 | `e63ba3d616566d3617e7c1a47493ba37aaad2cb867cb6ae518c03c2ddba51868` | 0 |
| src/ui/views/Perps/hooks/usePerpsGroupedMarketData.ts | 3594 | `6b63adf89e2be90805a307589b7a516bec43a5b1072c1c459d981b0ed48222ad` | 0 |
| src/ui/views/Perps/hooks/usePerpsHomePnl.ts | 1221 | `b90ea157fcd9fe7c3f7825aa9703a277c1ae103641177d4b078a33b5d9bc3717` | 0 |
| src/ui/views/Perps/hooks/usePerpsPortfolioLiveValue.ts | 1132 | `b909d501c12aeca116b244c272dfb7f4a3be4f7466e32eefd607d75f5275e997` | 0 |
| src/ui/views/Perps/hooks/usePerpsPosition.ts | 21578 | `e61e69761e24a4e5fe63bfc7bbd9567088b3dc73d0e4adee8060818bd44ed314` | 0 |
| src/ui/views/Perps/hooks/usePerpsSpotMids.ts | 1023 | `4baee9ea30253fdb9abf41df9230dc3e1a20b0d130a8fcb9c016337175541b14` | 0 |
| src/ui/views/Perps/hooks/usePerpsState.ts | 32306 | `d51b154a8bff6128d0f3c32e4655e88d85f292fdd27428b4277bf585267b351f` | 0 |
| src/ui/views/Perps/hooks/useStableCoinSwap.ts | 7523 | `84956f3e7c768d8c541767352c8cc328bac68cd524d0199261f1f51d60f550a0` | 0 |
| src/ui/views/Perps/limitOrderUtils.ts | 1630 | `e622710cd35e7f3eed9ef69eeb1f262abf59a0af0e67b002cde0c9d32f166e63` | 0 |
| src/ui/views/Perps/liquidation.ts | 10980 | `c9c61f3199e5c69de34447f3e13b2593f61d5cad83bc9aa965ed3f8b7c94cac2` | 0 |
| src/ui/views/Perps/popup/AddPositionPopup.tsx | 14329 | `a3e33223494cd967a7f1f782f8701b5861af506cb2bbdf725903bbf806c3e7bc` | 0 |
| src/ui/views/Perps/popup/ClosePositionPopup.tsx | 11930 | `befe97db4839cfe5ac497ec32296f87149c02600a9741e6dd7c5868b5851d3f4` | 0 |
| src/ui/views/Perps/popup/DepositAmountPopup.tsx | 20458 | `cd64273227099fc76681fcd4cb8923c29d10c95c56b7cd9ee6530ba2e7cdea36` | 0 |
| src/ui/views/Perps/popup/EditMarginPopup.tsx | 11921 | `2ca8e705dadf2a43a4a94e89b449f4e3b040e2d174bc4d74c69e52201a30817a` | 0 |
| src/ui/views/Perps/popup/EnableUnifiedAccountPopup.tsx | 2777 | `e3a19f47749ea2413feff0e5d4f240794c110f260a712effac68a94b83f2baa9` | 0 |
| src/ui/views/Perps/popup/HistoryDetailPopup.tsx | 15143 | `af3c26678ed14577137087eb1576a13795677c6d1de411166c17b6c05daba480` | 0 |
| src/ui/views/Perps/popup/HistoryTransferDetailPopup.tsx | 3017 | `9f580bf34be79aec9421fb9f0b2936a1152cb4f08bfe9cef30ec56b9717bd43c` | 0 |
| src/ui/views/Perps/popup/LimitOrderDetailPopup.tsx | 4330 | `9a7326b9ae293ec21b13b42bf2986a4c69f41b0d1db00c793ab7bd01edd0886f` | 0 |
| src/ui/views/Perps/popup/LoginPopup.tsx | 3119 | `351dbfab4cb0965a776c1983216e97551df16faadc614e335b5d7326da1cbfe6` | 0 |
| src/ui/views/Perps/popup/LogoutPopup.tsx | 3827 | `7ea9400c54cb86b6acf7b240cffc7d9050828f651f8e78d1a1ebf4730c43e331` | 0 |
| src/ui/views/Perps/popup/MarginModePopup.tsx | 4377 | `aa025a9044a4ee3df10b18b06190e18fcbf7b75aa986b2237df119fec2a3dabd` | 0 |
| src/ui/views/Perps/popup/NewUserProcessPopup.tsx | 6301 | `2fb165f1595c0709bf9b136cbfb8738c4b21b3bfb5cd92fb288dfa5108ea22cb` | 0 |
| src/ui/views/Perps/popup/OpenPositionPopup.tsx | 32658 | `11477635fdf256e125348bb1bd11fcd1c5efa79a4e94063a09cae46e2ff40a31` | 0 |
| src/ui/views/Perps/popup/PerpsInvitePopup.tsx | 4820 | `50de96a91f4a3836b5658aa2b3e32e93cf273013efb2a8bf86f070cca4583366` | 0 |
| src/ui/views/Perps/popup/RiskLevelPopup.tsx | 3461 | `e18d64c50fad73eb3fd23d1014c3dbe9301b42911ba45c20b782206eaeccc7b6` | 0 |
| src/ui/views/Perps/popup/SearchPerpsPopup.tsx | 10399 | `3e95969a6fb33a65005c6adde502f59dd3cb79c89c2158a1d26704cc16cb30dc` | 0 |
| src/ui/views/Perps/popup/SpotSwapPopup.tsx | 9406 | `274529757a25711fecbfdd7abb05c71cc58cac48dd2b72b748aeea79eddf461b` | 0 |
| src/ui/views/Perps/popup/TokenSelectPopup.tsx | 14390 | `d8c6c56d6faeaf14d0d6414345cf1cde9518f7091ad3631ab731a8fd510ea813` | 0 |
| src/ui/views/Perps/popup/WithdrawPopup.tsx | 21548 | `73a12b0481b3672d54c622f8a1ed43dc5e8be47116276fb17e8675b86835bd18` | 0 |
| src/ui/views/Perps/pricePrecision.ts | 4061 | `9e3cd9af25d59d1b09ca13fef958edefaa77de3d1deaddc746fe9ece458ad528` | 0 |
| src/ui/views/Perps/screen/ExploreMore.tsx | 3201 | `4456e84aa8433bc9440bf57206712a9386f9340dfd5116da1b79059a928cb544` | 0 |
| src/ui/views/Perps/screen/HistoryPage.tsx | 4291 | `b4bad6ccd867ff26f5fb8c4c5c4dbc36583051676b81f8a120a3f1dc34aeef04` | 0 |
| src/ui/views/Perps/screen/SingleCoin.tsx | 58275 | `43291ce32b8f6bbfc1d9e9ad5ea24c772ba239199fa936114f2d96ffd4391b81` | 0 |
| src/ui/views/Perps/screen/home.tsx | 24317 | `e1274449d2b8e27be889206159dd140c07dfc7656b935d49e3e2bbea2ac49f4d` | 0 |
| src/ui/views/Perps/screen/homeScrollState.ts | 997 | `78904f12acbb385b4beef607fec5551ab60a4838de0a7e01099a1f3bb6e415d2` | 0 |
| src/ui/views/Perps/sdkManager.ts | 3952 | `36f75e0e512eef5976f352b0fd1dfc88baaae09d377694b33534a4ca36d40702` | 0 |
| src/ui/views/Perps/sentry.ts | 3314 | `73f27a2c3aaee59854028e15b9eef55e768c6ab0e5ffa8556809731b9cd1b6d7` | 0 |
| src/ui/views/Perps/slippageUtils.ts | 1734 | `b51b125f3340a754a3b2072c26edb70f6c5322333cfa8f51901a620be4503aa4` | 0 |
| src/ui/views/Perps/utils/accountPricing.ts | 9565 | `26fac838a9b87ad41962b852f63448cf8055850a2fe65a001dda3b240b086f82` | 0 |
| src/ui/views/Perps/utils/perpsPortfolio.ts | 5962 | `1c48a57037154bf91794b1ec242e91b6b381dd0fb16979abc39aebff5e487f7f` | 0 |
| src/ui/views/Perps/utils.ts | 10389 | `801b3dc924eb06f4a194b8286804677934900c0ce6a8479c08f7dd0a7011fc69` | 0 |
| src/ui/views/Perps/weeklyCandles.ts | 4936 | `2282671f322fd02073efe571aa7c721909a95f80876c7065c480ef4108fd02c5` | 0 |
| src/ui/views/PreferMetamaskDapps/index.tsx | 2961 | `c86227e5dcd4477de29183895599eae8a26d553ffeb25e18532320a94aab6d77` | 0 |
| src/ui/views/QRCodeCheckerDetail.tsx | 1509 | `178c933155b3999d91f7a24fa723ac38544d748f66f3849eb243a5640ff32c0d` | 0 |
| src/ui/views/RabbyPoints/component/ClaimItem.tsx | 4459 | `53ef584ec8d766929cd2c312d23df51d421b0387dadba32f6837a745cc6cfa32` | 0 |
| src/ui/views/RabbyPoints/component/ClaimRabbyPointsModal.tsx | 11508 | `c5fe1bbfc2ebfec8ab8bba8a06c8e8ef095af55e92041f44e2c88c8354629713` | 0 |
| src/ui/views/RabbyPoints/component/ClaimUserAvatar.tsx | 417 | `97a99a4952cc1c1a06221aa10f33f8af505c52402bea7b03a17aeb743afb6dc9` | 0 |
| src/ui/views/RabbyPoints/component/CodeAndShare.tsx | 3209 | `39bcb1e513870ceb4711e9a4b9bd64ccd150edbcf961b1b9f4ba009c5755074e` | 0 |
| src/ui/views/RabbyPoints/component/ReferrralCode.tsx | 6459 | `50935bc8343e59a2a6894c4d438cc26bf5da1b1fd4582a1ec0cf75a764638a32` | 0 |
| src/ui/views/RabbyPoints/component/TopBoard.tsx | 2865 | `53b5fdddb82e5ff8358f4adac905c2990a77b42fef395dd359b97688d1bd4534` | 0 |
| src/ui/views/RabbyPoints/component/VerifyAddressModal.tsx | 2270 | `3d855d5d59b7a6c80379b4efaf12fa7e10943482f0a6504339ae718c93ba3927` | 0 |
| src/ui/views/RabbyPoints/hooks.tsx | 3385 | `3fb1324682995c1a08b8dba107c1474450e6166636a9cd27b403eed1fbd2f7a6` | 0 |
| src/ui/views/RabbyPoints/index.tsx | 16621 | `79842da66953108274877d5433820ef90665a477a97a3e171c2ceb7d1714579a` | 0 |
| src/ui/views/Receive/index.tsx | 14131 | `5fb89849abf19004bd6e01a5df5f7d73f584e91c34f2dc0b54557b3064601d60` | 0 |
| src/ui/views/RequestDeBankTestnetGasToken/Loading.tsx | 1153 | `895a01904806d6f9c005e6454d4e33658f99c20d9c3fae1fbc00189033fb0698` | 0 |
| src/ui/views/RequestDeBankTestnetGasToken/index.tsx | 9744 | `19f1a45bd4b3eebf09b5bc3ba4f834a1b549751cba3ba108607fd8b768cbe4a9` | 0 |
| src/ui/views/RequestPermission/index.tsx | 8213 | `10e12a5f8ac988a361b90ac6a350918df66e6f12039d4f0cb67a2b2cbb11a154` | 0 |
| src/ui/views/SelectAddress/components/Pagination.tsx | 766 | `1b4c9de8959fec8a3f55cd8d5ec7a27fb5b1f39394d5c6d7ad6b8d34162c13e6` | 0 |
| src/ui/views/SelectAddress/index.tsx | 2692 | `ce6e08d0cf8ffdbbb4868ccde9cb1ff7ab8e4e90d5d1e12a953a1d955129dd10` | 0 |
| src/ui/views/SelectAddress/route.ts | 799 | `b81890194c64ca0bc59f3d63ec9c3384c70e3fa3535b355ef2bc6b76e2b3118f` | 0 |
| src/ui/views/SelectToAddress/components/AccountList.tsx | 2696 | `d6bad7a7150af8518bce82572c02b0128eb2f8fb797bdbb1babcf74ee47b270c` | 0 |
| src/ui/views/SelectToAddress/components/EmptyWhitelistHolder.tsx | 1563 | `2565808d0176a2172be4c07f5e77d3bdd3b3f6d7394d73ab31c28753a9efc70e` | 0 |
| src/ui/views/SelectToAddress/components/EnterAddress.tsx | 11641 | `4741eec518af20319fc520e070930fc6b6192c9232a39430f6786fef516a3101` | 0 |
| src/ui/views/SelectToAddress/components/TabImported.tsx | 4116 | `84ed98d35bc844cac9d55a3635e2210eaf2d54617f479953eafb36ddf54036e6` | 0 |
| src/ui/views/SelectToAddress/components/TabWhitelist.tsx | 17063 | `b2bf97965d18c1089212b4698004b05e6cb8f3a36f19f5e1195b67d0fe8e5e94` | 0 |
| src/ui/views/SelectToAddress/index.tsx | 15415 | `941ee23c6a476261de32724835da6bea2924be007eb797838bbaab1c67adcdb5` | 0 |
| src/ui/views/SelectToAddress/util.ts | 470 | `2b7978a89db08db39e295b6aabdaba193dfd0e43dce142b96f29099e3f317389` | 0 |
| src/ui/views/SendNFT/BottomArea.tsx | 3785 | `7a8a44af8f0efb275a6eebd98b6037b0f837f52b3acb713ac1b160eb1a3b8817` | 0 |
| src/ui/views/SendNFT/index.tsx | 24737 | `8b8850429a74aa598c8c0229cf298a28b1530e7840aad44d351f01e7b131e9ad` | 0 |
| src/ui/views/SendToken/amountInputState.ts | 6497 | `e1184a8a6ccb31ab29cac3b399f39e2719be65136251f19b083c2cd03e13e1a5` | 0 |
| src/ui/views/SendToken/components/BottomArea.tsx | 3777 | `73d2982e4dd7023be43b9b9c985af45312f195c7539e6a2d23a221f1f783c123` | 0 |
| src/ui/views/SendToken/components/ChainSelectorInSend.tsx | 5034 | `619b612ab9e5f52c9c50d6850fbecc47e9de8ebc6cd04ddfd665505e0de9f4c5` | 0 |
| src/ui/views/SendToken/components/MaxButton.tsx | 809 | `baeb708b706702f8d63062015e47b5dfa7f6374d0c25802ef3f8023267438fab` | 0 |
| src/ui/views/SendToken/components/ModalConfirmAddToContacts.tsx | 6269 | `b73eec4cc9b29980dcc3843665fba2c8e2b60a605470fde7ec167d1d5da16817` | 0 |
| src/ui/views/SendToken/components/ModalConfirmAllowTransfer.tsx | 5219 | `83add46d33049f3fdc51efa5deffd57349c3b553a532e68ecb91e5e6180d8fc1` | 0 |
| src/ui/views/SendToken/components/PreExecTransactionExplain.tsx | 3713 | `4084a26d45ce917d90a0fad3bb8db1a70b09767923f44fcc2a9e086e4dc0a108` | 0 |
| src/ui/views/SendToken/components/SendShowMore.tsx | 2062 | `7713f801750004d2a509a6ee5d44887028353b6b095fbf6546958bdd7fae304c` | 0 |
| src/ui/views/SendToken/components/SwitchReserveGas.tsx | 1130 | `1405d4fcfdacb1c446c9d3aa791cd986e547a6de0bd4601cd58733f04a317793` | 0 |
| src/ui/views/SendToken/index.tsx | 103838 | `e9196c3a743fce30aeacd58a5e9ee0be1b3c304bddba055bac95359f49c78ddd` | 0 |
| src/ui/views/SendToken/useInitCheck.tsx | 3458 | `7a78ca30f8121d3ff6bf254bb13b71770156c623ab4ed41fab790630ad00bcb7` | 0 |
| src/ui/views/SignedTextHistory/index.tsx | 3681 | `40660eb0d6b52d13b4047c3d28ea006053e3de7b7412a99981fa53b4405665e8` | 0 |
| src/ui/views/SortHat.tsx | 3131 | `1c6e19840f3392b2d9762b13d27d328e67d967fbc7c5cff16c891eb72e8bf999` | 0 |
| src/ui/views/Staking/Detail.tsx | 18903 | `dc92be36f042f96bb4f78325811d163554142a1d69ed98c3de5be5d25e73875e` | 0 |
| src/ui/views/Staking/components/ActionModalShared.tsx | 598 | `dc6bba32b66c575a0d36ff1985955a7778437186998e70cc11e24df36510527a` | 0 |
| src/ui/views/Staking/components/DetailAboutSection.tsx | 9302 | `15516da295abf7183adb060825150bdab8ea7da2f995e6fa80cb73c83d29a033` | 0 |
| src/ui/views/Staking/components/DetailControls.tsx | 1744 | `3ae500269a9396e3757e1ca1c0a5cd45eb42dabf14c7b5601a6f5e2efc20db89` | 0 |
| src/ui/views/Staking/components/DetailPortfolioSection.tsx | 18146 | `46ab516ea397303c88c52a6b40af1deff5c42244dab3a260bbe81743dfe60df5` | 0 |
| src/ui/views/Staking/components/DetailSectionUtils.ts | 767 | `2cb8c254143daf19d0084962cdd96806a8a598306212a3c117164fcb4872a5b0` | 0 |
| src/ui/views/Staking/components/DetailSections.tsx | 428 | `f3387e78bf3d32cd1a5bf36a61555609d9559ca9918ef5a41af24ded418b6328` | 0 |
| src/ui/views/Staking/components/DetailSecuritySection.tsx | 2832 | `49a80f224e95d2cd489060ba3d21ff2415b6f272439c5b42e79cfeb375c204cd` | 0 |
| src/ui/views/Staking/components/DetailSummarySection.tsx | 8672 | `07608ab779d4870dfd215660036bb14c091fce3cbe9bba795acd12995864fd78` | 0 |
| src/ui/views/Staking/components/Erc4626ActionModal.tsx | 14976 | `7d366c190b6885e2bea55c706473328f61fffba0f354d0ae23699ea41e1c5291` | 0 |
| src/ui/views/Staking/components/Erc4626ActionModalSections.tsx | 7617 | `4bca5b9ef965c107454fd7a880629a65528edfcd3abebc996e18fa204c74bdbd` | 0 |
| src/ui/views/Staking/components/ListSections.tsx | 12310 | `b5ac433319cf7b297c1e06f6c673734c67395544ccf91fc560a841cf84706382` | 0 |
| src/ui/views/Staking/components/LpActionModal.tsx | 51213 | `c7c85244096860d99a60a41a1cb4f33690fa1d0899f62c32521f56849e350cfd` | 0 |
| src/ui/views/Staking/components/LpActionModalSections.tsx | 18508 | `97858bd6b0d537e91f36e6a3db71f53873c3eb96379b928139fb0e9470900b50` | 0 |
| src/ui/views/Staking/components/PoolVisuals.tsx | 5669 | `6988ec40a251d9b7190956b9eb7d8b18565382e59547cd2f70c28745ff7256b8` | 0 |
| src/ui/views/Staking/data/securityAudits.ts | 8895 | `01ea1bc6fd9034b7409a7a34898256f448a73718bdaff4adbf5e69386648694e` | 0 |
| src/ui/views/Staking/hooks/useStakingFilters.ts | 916 | `739052bb12b27db034af3d1b6893a62af4bb416ddc4e21e080a169326fd69620` | 0 |
| src/ui/views/Staking/hooks/useStakingMiniSign.ts | 3444 | `f6714d1d29ad6ef0837d44dd6477346ca2cabb8c99ed42ee1b1c84e612b81b0a` | 0 |
| src/ui/views/Staking/hooks/useStakingPendingActions.ts | 15598 | `b2257cbc5c87d53143635e23d7bc4073b570dea508c4ac8dee367885c57b5302` | 0 |
| src/ui/views/Staking/hooks/useStakingPoolCurve.ts | 864 | `ca17e7a56d29b6fa98797fbc977f59077ce5d577bc261078bdf06b664b9fbb68` | 0 |
| src/ui/views/Staking/hooks/useStakingPoolDetail.ts | 1041 | `69265770a2775c0247819bb8ef84db5dc240076211d9fb3c5d199a050a030620` | 0 |
| src/ui/views/Staking/hooks/useStakingPools.ts | 3827 | `7f7929b5701cfac155b56ee56545ea129639b096bad7fcd25062ee7bf076e249` | 0 |
| src/ui/views/Staking/hooks/useStakingPositionSummary.ts | 18271 | `fd2494bb6a2d6efb5f2701007ce83a33ba1251c591a25dfc25c59cb94348ca55` | 0 |
| src/ui/views/Staking/icons/index.ts | 637 | `2fbd086d6238e8901a6b5519da4198dec0ab6d2c01f35f84824d3a143702a390` | 0 |
| src/ui/views/Staking/index.tsx | 10709 | `ac5f4049f10cb2f8d9bc4f6ca6ed63976f63cad6701b63230e9def18e6051a7f` | 0 |
| src/ui/views/Staking/types.ts | 1295 | `f957bf2d41e5e02442ca20fe9854ac09ce2b54fc6f13b44a6d7c70817c2f41de` | 0 |
| src/ui/views/Staking/utils/format.ts | 3517 | `cee2243dabebccd6b50e1dcc728d23b2a727bd1087559ede680a77cfabb0ded3` | 0 |
| src/ui/views/Staking/utils/normalize.ts | 2801 | `c472fdaaa78bc07d80d59256546ed0bf28371949cebe82cd1ea83d6cca616997` | 0 |
| src/ui/views/Staking/utils/pendingResolution.ts | 5671 | `adef8863baea0700d494f37dc42e74eea281d24cdc82010fe8382aa0b90b1d3e` | 0 |
| src/ui/views/Staking/utils/poolKey.ts | 2114 | `65d154599037d62dae7f9da9e3ee8c32930ec809164d316a27a49e6d67df7d3e` | 0 |
| src/ui/views/Staking/utils/portfolioVisibility.ts | 567 | `5d9b4814ddaa1a73134aca39d8be8ba160d20d3ed89f86299fe0d83b13cfb3dc` | 0 |
| src/ui/views/Staking/utils/report.ts | 3027 | `4f7dec96e380d4b15cd5864b912f6484bb3d22ffa7e0d67a0148ca41ae957001` | 0 |
| src/ui/views/Staking/utils/tx.ts | 6638 | `5d5ef3210423b4c10b22c164b363b4fdd2a230fb43064a7c16f36601ed383088` | 0 |
| src/ui/views/Staking/utils/univ3NftReceipt.ts | 3254 | `df5e00141bdfe68b2a90ddf3dba255b86e0580a9843b035b10cf77416535d3b3` | 0 |
| src/ui/views/Staking/utils/univ3Withdraw.ts | 388 | `ad7fb2e377d8a370facf4f19f99d09a089c91a40b8d6037b28e4aa4442ae8bc2` | 0 |
| src/ui/views/Swap/Component/Header.tsx | 2945 | `37754b3ae3286b535691efbece43adda57b9672d624faf1339c3f56baed8ba6d` | 0 |
| src/ui/views/Swap/Component/History.tsx | 9831 | `39a92682c62a5b30634db037b9a8badca71f4b308e36163a7709528be058f0c9` | 0 |
| src/ui/views/Swap/Component/IconRefresh.tsx | 1390 | `af7fb41276df58b7a3b562799f7fc8b8a33d28cea9890c7258beea5134aab2c4` | 0 |
| src/ui/views/Swap/Component/LowCreditModal.tsx | 3589 | `8f0e1dec6821e98fe6c33f04d96a30dbf31200ccbef33cabb06c980f38c713e8` | 0 |
| src/ui/views/Swap/Component/Main.tsx | 47653 | `c559e187f6f58b54f3493a0daea436ebb050c902b316edf7c0214566033cee8e` | 0 |
| src/ui/views/Swap/Component/PendingTxItem.tsx | 11988 | `e8c3817bde7f0c1f587518718d5eb5a5852fd7cdc9627381d973a17206edce7a` | 0 |
| src/ui/views/Swap/Component/PendingTxStatusPopup.tsx | 4861 | `ce85701d99ad0cb5a4c704a844c39c0e4567fc5fb8cbd105af323832ccec5708` | 0 |
| src/ui/views/Swap/Component/QuoteItem.tsx | 17578 | `2f3295f04cb9b9b8aa591454872a13ad0f4357d181b7d55fc9634717dcb1dc20` | 0 |
| src/ui/views/Swap/Component/QuoteLogo.tsx | 1292 | `9a4d189addbfa80dfd2f8a2e2a41e80dff4a207cbc146e40ee067ee5493e1532` | 0 |
| src/ui/views/Swap/Component/Quotes.tsx | 9498 | `0e469cdc30afff498884bdf1ebd9ebeb9030830e913a08ead0d957f5d6352bf7` | 0 |
| src/ui/views/Swap/Component/RabbyFeePopup.tsx | 4644 | `60a84181e90e19aa09813aabfcb5a7f040e9a9b291ec6f8249bbd4226e9ceab9` | 0 |
| src/ui/views/Swap/Component/RabbyFeeTag.tsx | 5145 | `e329bfe3e209fd3bd20f20b20ec0e001d221b6fc05fe954a68590ddd86fa594d` | 0 |
| src/ui/views/Swap/Component/ReserveGasPopup.tsx | 9761 | `7916dfeac7ef45c400ba210f82c9fd60b83357c7caea0141fec2194b02ad3eab` | 0 |
| src/ui/views/Swap/Component/Slider.tsx | 1457 | `a7b991a0abc94c538c74ca8cfc893c050b6e61c3de291ecdf0f5c78262a6549c` | 0 |
| src/ui/views/Swap/Component/Token.tsx | 9515 | `7c8d1a00332a783e1ff3b5d61111242f082b8aaf948272da2d7ab7055e4fb3ec` | 0 |
| src/ui/views/Swap/Component/TokenRender.tsx | 2379 | `ccefd78b9c5074b6bc81cbb4e5057161d99d1c44f6e347fd6280145f1b98f9ab` | 0 |
| src/ui/views/Swap/Component/loading.tsx | 7251 | `41d2df83f656fcf2007c2b4880623a1c4fa0d8cb04f9e789920189c0934abf97` | 0 |
| src/ui/views/Swap/hooks/autoSlippageEffect.tsx | 462 | `514a246d10371d3b48d35b665c771329157f051bfbec203c723f7f4831fe7f47` | 0 |
| src/ui/views/Swap/hooks/context.tsx | 570 | `8bcb63c9c1ff4c9d6c0983afc8cc7a1107052c4a720fd99148d1bcedab58312b` | 0 |
| src/ui/views/Swap/hooks/fee.ts | 2157 | `0bf5421714e70f87665d4844f298116880cc61d624316342b0ea1602bc6ded89` | 0 |
| src/ui/views/Swap/hooks/history.tsx | 3588 | `89ce5212802157903ac0e9eab945f8dc7dacec345705b34e051cb15b9a9dfc50` | 0 |
| src/ui/views/Swap/hooks/index.tsx | 185 | `ff1b22d4895328e0b09d868a4a3564e8b2b264b34627f9e9aaf8897250d16bda` | 0 |
| src/ui/views/Swap/hooks/quote.tsx | 22357 | `2fa2d59e741230b205e6558b647ca25eb0751ee2de438baeba4943975914408b` | 0 |
| src/ui/views/Swap/hooks/recommentToken.ts | 5121 | `da7f6f5bdcd3dc95acb228015874d5f3121f02cc6d649fd88beacf8a4ae15637` | 0 |
| src/ui/views/Swap/hooks/render.ts | 3945 | `117a6c071b168d868e097d185e06dfe2f2989f996aa11b932db7bc987de1c193` | 0 |
| src/ui/views/Swap/hooks/settings.tsx | 403 | `7bc1fc8ef978a80dd4fe8f90ed872ec3d30366ce38062c84871eb5219e865247` | 0 |
| src/ui/views/Swap/hooks/slippage.tsx | 1994 | `5d014e3dab15a3e1a2c1c6cd3f7e8acff64557866c4fcfd7be5fdd31430457e7` | 0 |
| src/ui/views/Swap/hooks/swapReport.tsx | 2131 | `580c32879795fb58da63cc6fc0f5d03e8057b3001e9cb158bbcdc5c4e0e78121` | 0 |
| src/ui/views/Swap/hooks/token.tsx | 35604 | `dae27cd7f5156b1edf8bdf34994f5c3cb18ee0e6153c84c0054c3212cbe804fa` | 0 |
| src/ui/views/Swap/hooks/twoStepSwap.tsx | 2202 | `4d8956f6d148c47f03a0d1a10753d5c0916dc9b6806fc7caab5cb9adbda6a386` | 0 |
| src/ui/views/Swap/index.tsx | 1545 | `d98b9625b94ab8591163f1aca01a5c5cba2fc8aa1f43a918e0daebed63036f3d` | 0 |
| src/ui/views/Swap/utils.ts | 685 | `308cef9aad9e69e1bb265dfa823466bc2a9d393c2af92b873b12a5611dc7ad02` | 0 |
| src/ui/views/SwitchLang/index.tsx | 1315 | `438472c75002318feda23dc4f439713265ebdbc253a2a5e94e76b9edf33b6e9c` | 0 |
| src/ui/views/TokenApproval/components/ApprovalCard.tsx | 4459 | `4a80f06fed8e1c403d4583662c491ca6a22abe9dab1dd7f58690c92e64244e93` | 0 |
| src/ui/views/TokenApproval/components/Loading.tsx | 856 | `f31c8e07dc2bf9454f7aad591f7c16907bf000c49e1e155f21d44c743f6baf2c` | 0 |
| src/ui/views/TokenApproval/components/PopupApprovalCard.tsx | 683 | `68991d069df50538ee98c97a5868d7d142e581d1ad4090cc9641a9797256c40b` | 0 |
| src/ui/views/TokenApproval/components/PopupSearch.tsx | 2997 | `8a5a6f6cd20343a2122e6f0204f0e586374e866546c7f95b675e692870929039` | 0 |
| src/ui/views/TokenApproval/index.tsx | 6841 | `118caaf0e24ee8badee0369d974fd3168d5a5df2a1eaff2d906a056d38ece2b4` | 0 |
| src/ui/views/TransactionHistory/TestnetTranasctionHistory.tsx | 1395 | `9241a549a85cea807cbe927824d1122074a26d098b002afbac3885939db0ec91` | 0 |
| src/ui/views/TransactionHistory/components/CancelTxConfirmPopup.tsx | 2624 | `7dd917cfaa801be79ec7e452a91d7aac0785bfc578d942caf9e7ab7fd54d138d` | 0 |
| src/ui/views/TransactionHistory/components/CancelTxPopup.tsx | 4786 | `ccbad2be2f335433ae7b64627607049442eba6ef90bb34e45aa746aad8e85579` | 0 |
| src/ui/views/TransactionHistory/components/ChildrenTxText.tsx | 835 | `5a815e731c507e911842055e8d5f28af41230e3d86c6a2337399ee9cdc4d35b9` | 0 |
| src/ui/views/TransactionHistory/components/MempoolList.tsx | 5673 | `4e5c7a7e51420ddaa8a0b869d263ae59bb5f95f3b43752b87e9b66b387d18505` | 0 |
| src/ui/views/TransactionHistory/components/SkipNonceAlert.tsx | 7377 | `f8875d9ab73bbe5fe1b6a2b05f4352318dbb24e931dc47229a6fe85cc9f43c62` | 0 |
| src/ui/views/TransactionHistory/components/TransactionExplain.tsx | 11132 | `dc9e0cb34204db3ad56f41b353900524e06d3002658006ec9338cf6512a08952` | 0 |
| src/ui/views/TransactionHistory/components/TransactionItem.tsx | 18985 | `652f4a9f135c84d8d6bc3fdb441afebeca5e9fa847e6ebdc0194318655749c1b` | 0 |
| src/ui/views/TransactionHistory/components/TransactionPendingTag.tsx | 3918 | `51d4839c44783f6e1abb5273f919d3ecbcb7a03ebaa308056ec418ee45002014` | 0 |
| src/ui/views/TransactionHistory/components/TransactionWebsite.tsx | 978 | `42c192e9ef8719f92e3462257f73781d090383c5067e8707e977e43043212154` | 0 |
| src/ui/views/TransactionHistory/hooks/index.ts | 3501 | `141bd1a78de881e40c0c4124942642b05e808cbc3872728a146871217339588f` | 0 |
| src/ui/views/TransactionHistory/index.tsx | 4120 | `ea0dd103d3eb54143a28164d9249ffb65ddc98ad91d6584599484749c5723109` | 0 |
| src/ui/views/Unlock/index.tsx | 16325 | `de5b4909f848541e19c04e69404c947309d0875de9b492e0e3b39a6c70aee2a7` | 0 |
| src/ui/views/WalletConnect/index.tsx | 9014 | `b6b4d8c379c0524e13695d2db67f63e0183609fee2f73650d621d23420de134a` | 0 |
| src/ui/views/Welcome.tsx | 2332 | `d933a9f89d2459b89626659bf54fedacc455b9efcd3c7c66ddf98520854ba8b7` | 0 |
| src/ui/views/WhitelistInput/index.tsx | 16618 | `b2fa6ae1efdffe57608f726b1d68f32bb163f6f462459e51fb99ccf4da6a7160` | 0 |
| src/ui/views/index.tsx | 3905 | `33d234c40d3b7e55e6e262308a26105bbea36b2e51040ebd774b0442f51f9dbc` | 0 |
| src/ui/wallet/createWallet.ts | 4746 | `9c287679091a5c5385969097a783fc5c49e6dc6900a730e0b8b225a2c9996e62` | 0 |
| src/ui/wallet/index.ts | 1921 | `9c84c2955a0a3006af6c46fe866feee8e7462d5ba5c3c08babeff627cf2909f5` | 0 |
| src/utils/account.ts | 7443 | `0841b20699361018fe1eb9a06b38d9c6127e09fda07b19f6ebda2ff45138954b` | 0 |
| src/utils/approval.ts | 14696 | `ac1ec3199461f870134c9a2cf6ed6db6c845bd7f302a1c7f57c142af73ad36fb` | 0 |
| src/utils/approve.ts | 3019 | `6e4dd69ab3e16359f4e8d43531d0d065297d80f791f306d3e08ea7611c656ed2` | 0 |
| src/utils/broadcastToUI.ts | 900 | `14e9e3e8d970ba469d802ee50f8330fcbff86af3fe6d09cd049887efc444c064` | 0 |
| src/utils/chain.ts | 12329 | `9e3b5b9cf8691394dd8badd445f414b680184f81eb93c0b507dced1ed25715cb` | 0 |
| src/utils/cobo-agrus-sdk/cobo-agrus-sdk.ts | 4652 | `75064aae3699cb679836eeadc97674df594366eee58b3008a6f88d977c0e947b` | 0 |
| src/utils/curve.ts | 409 | `14caca130140cc00242347c7a38c72caaa65917242de06d121f902ab418c6e34` | 0 |
| src/utils/env.ts | 638 | `bec125d0515d115d0b6c566eb426f8725e0aa0ea1f154bc467702e27c079bff0` | 0 |
| src/utils/extensionVersion.ts | 1066 | `efa073dd9f3546ee2fff48eada850813c4e4eb9a4c5fbcfbed918a4349925494` | 0 |
| src/utils/ga4.ts | 4879 | `e18e5d8c0bc28ee4b12e27ea87ae03923f97a37351d09cab7a2c58ef82f8f3f5` | 1 |
| src/utils/gasAccount.ts | 898 | `7e30f6ec2cb139f4d000c7b06f415020d5c51fadea21983f5ea92ef4422f9656` | 0 |
| src/utils/history.ts | 3802 | `9da522056a2f10e0eda12d791d28f15b9bbc05f049b753fa3e50de7b91dd105f` | 0 |
| src/utils/hyperEvm.ts | 1194 | `9044667cd69f1e116bd0523d68087c0932ac329230456ace3c199cb984d92c7a` | 0 |
| src/utils/index.ts | 3753 | `e97fae567c3cb1575088f6b89d3b18c138496eeb916c805c737e2d1bf5a82378` | 0 |
| src/utils/l2.ts | 3913 | `be8d75e782e0d33fb97b7a617c0863440902bfdac70cdf7323a7bde539d0c1aa` | 0 |
| src/utils/matomo-request.ts | 2354 | `6478280516d55c08d285eec5ec9c880f521cf8adab66eb575f408fd1f1bd3b96` | 0 |
| src/utils/message/broadcastChannelMessage.ts | 1373 | `46628482ead9554ca0a7bf38736a3670da273a1b76d01cda6eb9f5055e055975` | 0 |
| src/utils/message/constants.ts | 136 | `a8fa5a4a27b6c1ba65ccd5d2530bcbb07e005747d8ce03c7155d6553a8467365` | 0 |
| src/utils/message/index.ts | 6691 | `4f5aea37b27a25e443ee14559736c589cdd2c3fd0118da1c2c661e00ec6c504b` | 0 |
| src/utils/message/perpsLive.ts | 1671 | `38ddbf48ae399a717c5f9db8be0966cef7635f1b64ae6cbaf1b92fa62ede55f7` | 0 |
| src/utils/message/portMessage.ts | 1691 | `95f7d6ff0bc045791d1249f740af2bba04550459d9a6e8059aad0533ae53982c` | 0 |
| src/utils/message.ts | 2399 | `96b680e27aa6ffc3f46872d57fade74a33ea4a5761b957a82be1f55d6258d0d8` | 0 |
| src/utils/nft.ts | 5099 | `149d3b28b1e0f863d14850d1a21840573fe97cb0354f7099c709c43fb0c42b73` | 0 |
| src/utils/nftVerify.ts | 22999 | `d3b751cef3c48bb86f65fee4cd7dee01dec3e89c3ed2722a2d9549c6d58cd781` | 0 |
| src/utils/optimism/buildUnserializedTransaction.ts | 2303 | `2382ea08e1d9b1ee8362b0a2f41e81e26f995a671175b1ef897fe6c802284520` | 0 |
| src/utils/perps/coinLogo.ts | 938 | `98a155c441789aef14d8da15fa079c3003f59cd3ac400346d4c3ff2559299c64` | 0 |
| src/utils/perps/fillFee.ts | 1283 | `6bd302b8de3d1394898ed95a5d5d2f974bb8fa4ad37b595b28c6e107198a5f47` | 0 |
| src/utils/perps/quoteAsset.ts | 640 | `49a0452de294ee6693ee5b32a8ea347eb2b2adc9d1e92a0b3dbd28a24d00ac8d` | 0 |
| src/utils/poll.ts | 1185 | `b76e0fa97fa304462ce4d8871e41849c4979c3a65ff850fad8dbbc2313decab7` | 0 |
| src/utils/rateGuidance.ts | 1574 | `7e14d83527c35c6befa8783cf2644876b6585a86e25349bbedd61b6a12ce74cd` | 0 |
| src/utils/removedTokens.ts | 197 | `8df5aa285b92147f75627a5c70512e49ef2e0d87c8de1a03db0967e1850d80c8` | 0 |
| src/utils/sentry-config.ts | 4296 | `c6a5936aa32573c2ac22c2b2f86262afe39c993c5a9e4e247e7229aeb2f94303` | 0 |
| src/utils/sentry.ts | 12573 | `771fe27dafc9f2709be73fbe347408e85460e510960033e58f6094c03ddf50ea` | 0 |
| src/utils/signEvent.ts | 489 | `d9bc455fb0918ed9b75aeb7349538a3c691002c0f60447ec16938dbabb9e430e` | 0 |
| src/utils/string.ts | 734 | `410db427681225ab71e5bc71c7e50d33513b0aac4dc3243cbc62b3a0eca35cd3` | 0 |
| src/utils/tempo.ts | 29806 | `7d739e5f47abddf98f69027044518c9a291605e4be3ce39abac093481eb91449` | 0 |
| src/utils/time.ts | 587 | `0ab133574d8d04c971d1cc4857805311ae85b8428972a8ce648c96cae7320832` | 0 |
| src/utils/transaction.ts | 28141 | `8b3e03cf50da869c295fa3d51c190627d14341fc54ab81f3c8e56d02592f2899` | 0 |
| src/utils/tx.ts | 1593 | `6914d80c64975863355d40e04582229f23f7f7fb317383ce2c248567f48822c4` | 0 |
| src/utils/type.ts | 59 | `58f253a44258b29c1691864c9ee1b2e43aef322e6087790a4471ecf018072bc1` | 0 |
| src/utils/user-data-tracking.ts | 2272 | `c7ccc44eb3aac4b829e6f4de99aa752078abac2f9b8943e262e3e8b0e1b8faa7` | 0 |
| src/utils/walletconnect-error.ts | 485 | `6b880cc033ed545f04dbe126b1a069e845222e3a077996a94a2226542ab293ce` | 0 |
| src/utils/walletconnect.ts | 646 | `e27ad5fca74da6aca9b5cc46160812924fe1c7d44911e06d7c61fe5f2ff89d70` | 0 |
| svgTransform.js | 264 | `987353d72c86f2f846381df439064b353737ff99cf969e70c9b105da9fe9c723` | 0 |
| tailwind.config.js | 3860 | `304f7d8cf11759db70537cf8b5f012bc4ff52946eb2dd3d59bd8d6be34dd4230` | 0 |
| webpack.config.js | 622 | `7ad1be35ef9799f75731e14f82f82b694f5ac1eb74cfe6a5e934af09784f6949` | 0 |
| yarn.lock | 961697 | `8e252baa79ff8948303d9e48183658b095333f2553b4e327933a7d1651ca66e4` | 1 |
