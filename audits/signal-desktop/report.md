# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** signal-desktop @ 17502b9d1a9e · Signal Messenger — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-28 18:29 UTC |
| Версия отчёта | 1 |
| Запуск аудита | f5cb1d6d-23ed-4a89-b045-61c86d6b9fea (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Разработчик ПО безопасности |
| SHA-256 содержимого | `7bc698dcb2c9734f1682d4f12713911e942d23cc39434a23f720e6817e6ba212` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **1**
- Высокая: **6**
- Средняя: **3**
- Низкая: **0**
- Информационная: **2**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 9
- Подтверждённая ошибка конфигурации: 1
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 0
- Рекомендация по улучшению: 1
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 3, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 1 из 4 — постквантовый код есть, но не подключён.** Следующий шаг: Подключите имеющийся постквантовый примитив к критичному пути (обёртка ключей или канал) в гибридной схеме и проверьте совместимость.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/signalapp/Signal-Desktop> @ `17502b9d1a9e34af689f31508c4ac4ccee5b5cb7` — ссылки в доказательствах открывают строки на этом коммите.

2202 файлов, всего 13952587 байт, редактирований: 7; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 2178 | .babelrc.mjs: 24 lines scanned with 16 rule patterns and 122 registry patterns; .oxlint/plugin.mjs: 41 lines scanned with 16 rule patterns and 122 registry patterns; .oxlint/rules/enforceArrayBuffer.mjs: 48 lines scanned with 16 rule patterns and 122 registry patterns |
| certificates | ошибка (не проверено) | 1 | config/default.json line 23: certificate could not be parsed (ValueError) |
| certificates_and_keys | проверено | 1 | config/default.json: certificates/keys parsed |
| dependencies | проверено | 9 | danger/package.json: 5 dependencies parsed (5 pinned); danger/pnpm-lock.yaml: 133 dependencies parsed (133 pinned); package.json: 224 dependencies parsed (217 pinned) |
| secrets | проверено | 2 | ts/textsecure/WebAPI.preload.ts: 5 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); ts/types/SealedSender.std.ts: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| osv_advisories | проверено | 1 | 1000 pinned packages queried at OSV.dev; 6 affected (2 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- certificates — ошибка (не проверено): config/default.json line 23: certificate could not be parsed (ValueError)

## 5. Краткое описание архитектуры

Static review of the source tree signal-desktop at 17502b9d1a9e34af689f31508c4ac4ccee5b5cb7. 2202 files analysed; of 4499 files, 1033 are test, fuzzing, benchmark or example code and were left out, 1264 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **0** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 0.0%

## 7. Подробное описание находок

### QSI-2026-05952 — @storybook/core 8.6.18 затронут GHSA-f2ph-cmg5-wxc8 (CVE-2026-114125)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@storybook/core@8.6.18`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:29 UTC
- Балл приоритета: 40.7 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-f2ph-cmg5-wxc8 (CVE-2026-114125) для пакета npm @storybook/core версии 8.6.18: Storybook: Missing origin validation in Storybook preview allows code injection from malicious websites. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-f2ph-cmg5-wxc8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-f2ph-cmg5-wxc8](https://osv.dev/vulnerability/GHSA-f2ph-cmg5-wxc8) · manifest · SHA-256 92de84a398faba971f897dfefaa92fd81e9492196c28c9310b7b387367a423ef_

```
{"id": "GHSA-f2ph-cmg5-wxc8", "aliases": ["CVE-2026-114125"], "modified": "2026-10-21T17:35:19.889160714Z", "summary": "Storybook: Missing origin validation in Storybook preview allows code injection from malicious websites", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (8.6.19).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05945 — zod 4.3.6 затронут GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/zod@4.3.6`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:29 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404) для пакета npm zod версии 4.3.6: Zod can exhaust memory while validating oversized constrained collections. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-05943 — Возможный секрет в коде ts/state/smart/fun/giphy.preload.ts

- Серьёзность: **Высокая** · Классификация: Подтверждённая ошибка конфигурации · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `file:ts/state/smart/fun/giphy.preload.ts`
- Источник данных: ts/state/smart/fun/giphy.preload.ts
- Метод обнаружения: Сопоставление регулярных выражений с API конкретного языка.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:29 UTC
- Балл приоритета: 48.5 / 100
- CVSS v3.1: неприменимо

1 значений, похожих на секреты, типа generic_assignment (первое — строка 22). Значения замаскированы QSI.

**Возможные последствия.** Учётные данные в коде утекают через репозитории, сборки и журналы.

**Шаги воспроизведения.**

```
Откройте строка 22 в предоставленном файле ts/state/smart/fun/giphy.preload.ts и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [ts/state/smart/fun/giphy.preload.ts](https://github.com/signalapp/Signal-Desktop/blob/17502b9d1a9e34af689f31508c4ac4ccee5b5cb7/ts/state/smart/fun/giphy.preload.ts#L22) · line 22 · SHA-256 1a3544c4894e717e5ff4905f6fbf51e17a24af7b9bc216e1a8ee0b98baa78272_

```
   22 | const API_KEY = '[REDACTED]';
```

**Ограничения проверки.** Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Перенесите секреты в менеджер секретов/окружение; замените раскрытые значения.

**Повторная проверка.** Повторно просканируйте код и проверьте места вызова из доказательства.

### QSI-2026-05947 — undici 6.29.0 затронут GHSA-2m5v-pch6-74hx (CVE-2026-109383)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/undici@6.29.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:29 UTC
- Балл приоритета: 37.7 / 100
- CVSS v3.1: 7.4 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-2m5v-pch6-74hx (CVE-2026-109383) для пакета npm undici версии 6.29.0: undici vulnerable to TLS certificate validation bypass via dropped tls options in Agent. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2m5v-pch6-74hx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2m5v-pch6-74hx](https://osv.dev/vulnerability/GHSA-2m5v-pch6-74hx) · manifest · SHA-256 19e2f924907f2ce4ed8291ce8090db4b0a3c4d3641b23ef551ecbdd3dbfd6d4e_

```
{"id": "GHSA-2m5v-pch6-74hx", "aliases": ["CVE-2026-109383"], "modified": "2026-10-27T19:15:22.407771210Z", "summary": "undici vulnerable to TLS certificate validation bypass via dropped tls options in Agent", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.29.1, 7.30.1, 8.12.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05950 — undici 6.29.0 затронут GHSA-qrxm-fqhp-jwvm (CVE-2026-87018)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/undici@6.29.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:29 UTC
- Балл приоритета: 37.7 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-qrxm-fqhp-jwvm (CVE-2026-87018) для пакета npm undici версии 6.29.0: undici vulnerable to Denial of Service via TLS 1.2 certificate-changing renegotiation. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qrxm-fqhp-jwvm
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qrxm-fqhp-jwvm](https://osv.dev/vulnerability/GHSA-qrxm-fqhp-jwvm) · manifest · SHA-256 9e812022c75ee0daa805570ce3c7fd7af5aa9523895bf6543828e4f354d52e36_

```
{"id": "GHSA-qrxm-fqhp-jwvm", "aliases": ["CVE-2026-87018"], "modified": "2026-10-27T19:15:22.403573595Z", "summary": "undici vulnerable to Denial of Service via TLS 1.2 certificate-changing renegotiation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.29.1, 7.30.1, 8.12.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05951 — undici 6.29.0 затронут GHSA-xjj6-f33q-929c (CVE-2026-109869)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/undici@6.29.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:29 UTC
- Балл приоритета: 37.7 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-xjj6-f33q-929c (CVE-2026-109869) для пакета npm undici версии 6.29.0: undici vulnerable to Denial of Service via unhandled error on excessive content-encodings. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xjj6-f33q-929c
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xjj6-f33q-929c](https://osv.dev/vulnerability/GHSA-xjj6-f33q-929c) · manifest · SHA-256 98da2a0ccc8faf78e8cda82e772dd00dfecd0503ce078459f6a1363e331ac198_

```
{"id": "GHSA-xjj6-f33q-929c", "aliases": ["CVE-2026-109869"], "modified": "2026-10-23T22:30:05.007687918Z", "summary": "undici vulnerable to Denial of Service via unhandled error on excessive content-encodings", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.29.1, 7.30.1, 8.12.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05953 — @storybook/core 8.6.18 затронут GHSA-px85-f4q5-jh77 (CVE-2026-114126)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@storybook/core@8.6.18`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:29 UTC
- Балл приоритета: 37.7 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-px85-f4q5-jh77 (CVE-2026-114126) для пакета npm @storybook/core версии 8.6.18: Storybook dev server vulnerable to code injection from the local network. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-px85-f4q5-jh77
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-px85-f4q5-jh77](https://osv.dev/vulnerability/GHSA-px85-f4q5-jh77) · manifest · SHA-256 ca9572e93e0a3ad41e56d349820ff80eb5e275b89e55d7b8dd80a943aca43ff7_

```
{"id": "GHSA-px85-f4q5-jh77", "aliases": ["CVE-2026-114126"], "modified": "2026-10-22T16:45:03.723842082Z", "summary": "Storybook dev server vulnerable to code injection from the local network", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (8.6.19).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05946 — qs 6.16.0 затронут GHSA-6pq8-jhm2-2vcw (CVE-2026-110816)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/qs@6.16.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:29 UTC
- Балл приоритета: 33.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-6pq8-jhm2-2vcw (CVE-2026-110816) для пакета npm qs версии 6.16.0: qs : qs.stringify with arrayFormat 'comma' throws an uncaught TypeError on array elements carrying a non-callable own toString (DoS). Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6pq8-jhm2-2vcw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-6pq8-jhm2-2vcw](https://osv.dev/vulnerability/GHSA-6pq8-jhm2-2vcw) · manifest · SHA-256 4fd7af689173b0c3abc4f3e9006070e7de778a692b621288cc277cd4bcb7ab05_

```
{"id": "GHSA-6pq8-jhm2-2vcw", "aliases": ["CVE-2026-110816"], "modified": "2026-10-27T16:15:05.324423680Z", "summary": "qs : qs.stringify with arrayFormat 'comma' throws an uncaught TypeError on array elements carrying a non-callable own toString (DoS)", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.16.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05948 — undici 6.29.0 затронут GHSA-4qv8-2p9j-2685 (CVE-2026-109924)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/undici@6.29.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:29 UTC
- Балл приоритета: 33.2 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-4qv8-2p9j-2685 (CVE-2026-109924) для пакета npm undici версии 6.29.0: undici vulnerable to Denial of Service via unbounded memory in the EventSource parser. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4qv8-2p9j-2685
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4qv8-2p9j-2685](https://osv.dev/vulnerability/GHSA-4qv8-2p9j-2685) · manifest · SHA-256 e5622217ce8fee7d0f9d0c69334e0892afdc8d1b893f742d4e2027eeec4a9894_

```
{"id": "GHSA-4qv8-2p9j-2685", "aliases": ["CVE-2026-109924"], "modified": "2026-10-23T22:30:04.104974737Z", "summary": "undici vulnerable to Denial of Service via unbounded memory in the EventSource parser", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.29.1, 7.30.1, 8.12.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05949 — undici 6.29.0 затронут GHSA-9fm3-97px-rjf6 (CVE-2026-109932)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/undici@6.29.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:29 UTC
- Балл приоритета: 33.2 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-9fm3-97px-rjf6 (CVE-2026-109932) для пакета npm undici версии 6.29.0: undici WebSocket client vulnerable to Denial of Service via unbounded automatic PONG buffering. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9fm3-97px-rjf6
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9fm3-97px-rjf6](https://osv.dev/vulnerability/GHSA-9fm3-97px-rjf6) · manifest · SHA-256 ec1f6601eb756d4048c59aceff106702f6512b7dea2377ff744bf7d42c4d4f79_

```
{"id": "GHSA-9fm3-97px-rjf6", "aliases": ["CVE-2026-109932"], "modified": "2026-10-27T19:15:22.400702743Z", "summary": "undici WebSocket client vulnerable to Denial of Service via unbounded automatic PONG buffering", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.29.1, 7.30.1, 8.12.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05954 — 4 бюллетеней в 2 пакет(ах) npm, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:npm:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:29 UTC
- Балл приоритета: 15.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 4 бюллетеней (3 с оценкой high или critical) для 2 пакет(ов) npm, которые подтягивают только инструменты разработки или сборки (package.json): например, fabric@4.6.0 [dev]: GHSA-hfvx-25r5-qc3w, GHSA-w22m-hvvm-xmwx; storybook@8.6.18 [dev]: GHSA-f2ph-cmg5-wxc8, GHSA-px85-f4q5-jh77. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в package.json.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · package.json · SHA-256 aadeefee928a68c6a9a98b0557f79317c2b91a9a070abbc504a6408a16babd6e_

```
fabric@4.6.0 [dev]: GHSA-hfvx-25r5-qc3w, GHSA-w22m-hvvm-xmwx
storybook@8.6.18 [dev]: GHSA-f2ph-cmg5-wxc8, GHSA-px85-f4q5-jh77
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05944 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:29 UTC
- Балл приоритета: 13.5 / 100
- CVSS v3.1: неприменимо

В 9 манифестах зависимостей QSI нашёл криптобиблиотеки (jsonwebtoken), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · danger/package.json, danger/pnpm-lock.yaml, package.json, packages/lame/package.json, packages/mute-state-change/package.json, packages/types/package.json, packages/windows-ucv/package.json, pnpm-lock.yaml, sticker-creator/package.json · SHA-256 727c9fa51969eaa77ba568319a2ba09bbbf416d73bddeee8bfc4b77ecb755aa0_

```
Crypto libraries: jsonwebtoken
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

### Постквантовая зрелость: Уровень 1 из 4 — постквантовый код есть, но не подключён

- Есть, но не подключено: ML-KEM — ts/sql/migrations/1470-kyber-triple.std.ts
- Есть, но не подключено: ML-KEM — ts/sql/migrations/85-add-kyber-keys.std.ts

**Следующий шаг:** Подключите имеющийся постквантовый примитив к критичному пути (обёртка ключей или канал) в гибридной схеме и проверьте совместимость.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | AES-256 (3), HKDF (1), HMAC (5), SHA-2 (8) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | SHA-2 (8) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |
| Квантовое решетчатое просеивание | учтено в стандартных параметрах | Q1 | ML-KEM (2) | Для ML-KEM и ML-DSA в стандартных наборах параметров ничего менять не нужно. Заявление 2024 года о полиномиальном квантовом алгоритме для LWE отозвано после обнаружения ошибки (см. заявления). |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- certificates: config/default.json line 23: certificate could not be parsed (ValueError)

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P1 | QSI-2026-05943 | Замените и удалите секреты из ts/state/smart/fun/giphy.preload.ts. | устранение первопричины | Сканер секретов ничего не находит; старые значения отозваны. |
| P2 | QSI-2026-05952 | Обновите @storybook/core до исправленной версии (8.6.19). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-f2ph-cmg5-wxc8 (CVE-2026-114125). |
| P2 | QSI-2026-05945 | Обновите zod до исправленной версии (4.6.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404). |
| P2 | QSI-2026-05947 | Обновите undici до исправленной версии (6.29.1, 7.30.1, 8.12.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2m5v-pch6-74hx (CVE-2026-109383). |
| P2 | QSI-2026-05950 | Обновите undici до исправленной версии (6.29.1, 7.30.1, 8.12.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qrxm-fqhp-jwvm (CVE-2026-87018). |
| P2 | QSI-2026-05951 | Обновите undici до исправленной версии (6.29.1, 7.30.1, 8.12.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xjj6-f33q-929c (CVE-2026-109869). |
| P2 | QSI-2026-05953 | Обновите @storybook/core до исправленной версии (8.6.19). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-px85-f4q5-jh77 (CVE-2026-114126). |
| P2 | QSI-2026-05946 | Обновите qs до исправленной версии (6.16.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-6pq8-jhm2-2vcw (CVE-2026-110816). |
| P2 | QSI-2026-05948 | Обновите undici до исправленной версии (6.29.1, 7.30.1, 8.12.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4qv8-2p9j-2685 (CVE-2026-109924). |
| P2 | QSI-2026-05949 | Обновите undici до исправленной версии (6.29.1, 7.30.1, 8.12.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9fm3-97px-rjf6 (CVE-2026-109932). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P4 | QSI-2026-05954 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |

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
4. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
5. CRYSTALS-Kyber — Algorithm Specifications and Supporting Documentation (round 3, 2021-08-04) — CRYSTALS team. <https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf> (NIST round-3 submission: core-SVP cost 2^{0.292β} classical, 2^{0.265β} quantum; Kyber768 166 quantum bits)
6. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
7. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
8. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
9. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
10. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
11. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
12. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
13. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
14. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
15. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
16. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
17. OSV advisory GHSA-2m5v-pch6-74hx — OSV.dev. <https://osv.dev/vulnerability/GHSA-2m5v-pch6-74hx> (modified 2026-10-27T19:15:22.407771210Z)
18. OSV advisory GHSA-4qv8-2p9j-2685 — OSV.dev. <https://osv.dev/vulnerability/GHSA-4qv8-2p9j-2685> (modified 2026-10-23T22:30:04.104974737Z)
19. OSV advisory GHSA-6pq8-jhm2-2vcw — OSV.dev. <https://osv.dev/vulnerability/GHSA-6pq8-jhm2-2vcw> (modified 2026-10-27T16:15:05.324423680Z)
20. OSV advisory GHSA-9fm3-97px-rjf6 — OSV.dev. <https://osv.dev/vulnerability/GHSA-9fm3-97px-rjf6> (modified 2026-10-27T19:15:22.400702743Z)
21. OSV advisory GHSA-f2ph-cmg5-wxc8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-f2ph-cmg5-wxc8> (modified 2026-10-21T17:35:19.889160714Z)
22. OSV advisory GHSA-mrhx-c7xc-m3w5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-mrhx-c7xc-m3w5> (modified 2026-10-23T18:30:09.376405885Z)
23. OSV advisory GHSA-px85-f4q5-jh77 — OSV.dev. <https://osv.dev/vulnerability/GHSA-px85-f4q5-jh77> (modified 2026-10-22T16:45:03.723842082Z)
24. OSV advisory GHSA-qrxm-fqhp-jwvm — OSV.dev. <https://osv.dev/vulnerability/GHSA-qrxm-fqhp-jwvm> (modified 2026-10-27T19:15:22.403573595Z)
25. OSV advisory GHSA-xjj6-f33q-929c — OSV.dev. <https://osv.dev/vulnerability/GHSA-xjj6-f33q-929c> (modified 2026-10-23T22:30:05.007687918Z)
26. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
27. OWASP Application Security Verification Standard — OWASP. <https://owasp.org/www-project-application-security-verification-standard/> (living standard — check the project page for the current version)
28. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Расположение | Квантовый статус | Классический статус |
|---|---|---|---|---|---|
| AES-256 | AES-256 |  | ts/Crypto.node.ts:437 | сниженный запас (Гровер), одобрен | допустимо |
| AES-256 | AES-256 |  | ts/context/Crypto.node.ts:46 | сниженный запас (Гровер), одобрен | допустимо |
| AES-256 | AES-256 |  | ts/types/Crypto.std.ts:12 | сниженный запас (Гровер), одобрен | допустимо |
| HKDF |  |  | sticker-creator/src/util/crypto.ts:56 | сниженный запас (Гровер), одобрен | допустимо |
| HMAC |  |  | sticker-creator/src/util/crypto.ts:90 | сниженный запас (Гровер), одобрен | допустимо |
| HMAC |  |  | ts/AttachmentCrypto.node.ts:387 | сниженный запас (Гровер), одобрен | допустимо |
| HMAC |  |  | ts/context/Crypto.node.ts:20 | сниженный запас (Гровер), одобрен | допустимо |
| HMAC |  |  | ts/services/backups/index.preload.ts:845 | сниженный запас (Гровер), одобрен | допустимо |
| HMAC |  |  | ts/util/appendMacStream.node.ts:24 | сниженный запас (Гровер), одобрен | допустимо |
| SHA-2 | SHA-512 |  | app/OptionalResourceService.main.ts:76 | сниженный запас (Гровер), одобрен | допустимо |
| SHA-2 | SHA-512 |  | scripts/artifact-build-completed.mjs:66 | сниженный запас (Гровер), одобрен | допустимо |
| SHA-2 | SHA-512 |  | scripts/generate-icu-types.mjs:281 | сниженный запас (Гровер), одобрен | допустимо |
| SHA-2 | SHA-512 |  | scripts/get-emoji-locales.mjs:56 | сниженный запас (Гровер), одобрен | допустимо |
| SHA-2 | SHA-512 |  | scripts/get-jumbomoji.mjs:54 | сниженный запас (Гровер), одобрен | допустимо |
| SHA-2 | SHA-512 |  | ts/updater/util.node.ts:28 | сниженный запас (Гровер), одобрен | допустимо |
| SHA-2 | SHA-256 |  | .storybook/test-runner.ts:89 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| SHA-2 | SHA-256 |  | ts/updater/signature.node.ts:65 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| CBC mode |  |  | sticker-creator/src/util/crypto.ts:82 | н/п | допустимо |
| Crypto library | 9.0.2 | jsonwebtoken (jsonwebtoken (Node)) | danger/pnpm-lock.yaml | н/п | допустимо |
| Crypto library | 9.0.2 | jsonwebtoken (jsonwebtoken (Node)) | pnpm-lock.yaml | н/п | допустимо |
| ML-KEM |  |  | ts/sql/migrations/1470-kyber-triple.std.ts | постквантовый | допустимо |
| ML-KEM |  |  | ts/sql/migrations/85-add-kyber-keys.std.ts | постквантовый | допустимо |

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| .babelrc.mjs | 855 | `da19b0181107660e1063a5ed7e7370ea6c6d1a3097c2c008d792ee70902c2405` | 0 |
| .oxlint/plugin.mjs | 1781 | `022c3c07e5c28d09c1779719e1cb1167c9b6a97f2d16f464ae214cdfe1d76d1b` | 0 |
| .oxlint/rules/enforceArrayBuffer.mjs | 1183 | `b097ab1e78a1ccfc8bf8029b651845cdaa6bf32c34749b1d257eabcfdb88e3be` | 0 |
| .oxlint/rules/enforceClassNameHasStyles.mjs | 14038 | `9797363bbdf5de0e8e0ee46130f2688de31befdc404403544a1ed46f6fbac85b` | 0 |
| .oxlint/rules/enforceFileSuffix.mjs | 16668 | `e23007f3ffc8a929ea523337cdf21530b7d10fec597c9a3dcdc4a2b9000f0040` | 0 |
| .oxlint/rules/enforceLicenseComments.mjs | 2221 | `58385036b672b946a2e6090e580af6007ad1d3056f45ba94b247fc22e0047be0` | 0 |
| .oxlint/rules/enforceStaticClassNames.mjs | 15428 | `4eb04e2e687ba275d78c4a35dd80f604504988fa3e0fd79e9362f8717db46463` | 0 |
| .oxlint/rules/enforceTw.mjs | 4415 | `336267c0fc5287cfe64338dd7940e4d1f2a09e7e0bf0076042d5ca8433ad3d87` | 0 |
| .oxlint/rules/enforceTw.worker.mjs | 1580 | `ac37df62be286a7b8d56e4dbe6c8b0b77fc0f71bed356c4ae36a7b7256acbb54` | 0 |
| .oxlint/rules/enforceTypeAliasReadonlyDeep.mjs | 1742 | `5271673578939862cb2048e530e6b32aaab2d878931cc56906293aecfead35f2` | 0 |
| .oxlint/rules/noDisabledTests.mjs | 1656 | `752d1f16fd1db4310a6eae7f6a88c5c8b75d7112b64f1d2d1e5e26bbf5728467` | 0 |
| .oxlint/rules/noExtraneousDependencies.mjs | 5340 | `05e4f68a835017652153d08893f4b5770a26e7778fc10f319ec5cd57fa8993a7` | 0 |
| .oxlint/rules/noFocusedTests.mjs | 1576 | `c2a8d7b574a4d14c2f728062d1e2835b5e0f06985ed8bfee91b99326aa72d03b` | 0 |
| .oxlint/rules/noForIn.mjs | 528 | `437d41f718d44d534253320b21e351fd227197de3534037212df64d3265933d9` | 0 |
| .oxlint/rules/noRestrictedPaths.mjs | 7133 | `d819a3731e83d69e4df5badd3655bf322e264ec493aed63dcf47618f5cb76984` | 0 |
| .oxlint/rules/noThen.mjs | 792 | `67891a71a8bed2f68fb53e898b42be28a7d102edc05b66eecfec690f461a2040` | 0 |
| .oxlint/rules/utils/assert.mjs | 328 | `54c75ebd549a048748a732c5c3f5bd807316789546b74bee38b8d553347a21c2` | 0 |
| .oxlint/rules/utils/astUtils.mjs | 1109 | `a8df39093e62a5854449f2ee8f71c28f8d1d45ea7142476122897c90f798169c` | 0 |
| .oxlint/rules/utils/createImportSourceVisitor.mjs | 3188 | `943e362400021481b6f09ef413e2993b4558a34c15cd815918b1fc47acef2dbf` | 0 |
| .oxlint/rules/utils/getReferenceType.mjs | 542 | `225fcf486fc5cc34a4e89974372d8171c64a04b87c8c1742ff918d6abc59d322` | 0 |
| .oxlint/test-setup.mjs | 223 | `d198444dbdb8e9dcaf59d360d3b6f0479597b93980a326ddd7675944f6650d1a` | 0 |
| .oxlint/utils/classNames.mjs | 11920 | `cdef1acf7b54292f7ea262fd64ffdb2151fd383aaa0f8303ad85a39674f9efa3` | 0 |
| .pnpmfile.mjs | 6616 | `052bab912c50d3c3ecdbbc5dad34211b08d4f4bd702c07acd1883166da491c0f` | 0 |
| .prettierrc.mjs | 407 | `d279e77498d940f45a3dc0814832a93bddc775d81f5a2db95d6d3eb5d735e289` | 0 |
| .storybook/StorybookThemeContext.std.ts | 245 | `5df92c8ab57856f3db6debf38891da1505326a8324842ff3b462d198e4ecf10e` | 0 |
| .storybook/main.ts | 3442 | `eb3610188b68bad47bdc83a74e79d15d2722a05e02c64db40b6ba2fa14ea106a` | 0 |
| .storybook/preview.tsx | 9067 | `5f77afe2826a1ed34c7ebd58db356b76517f23a905e51fd9555c03b87576e621` | 0 |
| .storybook/test-runner.ts | 2986 | `2d417a286554e79e4b652e04824b35ab4073d83106132c550065e2283594c5b7` | 0 |
| .stylelintrc.mjs | 1710 | `54fdac854cf25b8d6f0b1211a365babba545141d7fd6fccb9a6b8ffe984662fa` | 0 |
| app/AssetService.main.ts | 2950 | `1cc84514304f8c877be6757f44916d3358084100aa4b8b1fc7a4c311118e2b2c` | 0 |
| app/DevelopmentService.main.ts | 1043 | `dd2c4e34ca5744029c793611a98c078672e15a65c6ebabecb028496911b949e3` | 0 |
| app/EmojiService.main.ts | 3527 | `d888db5f1dcf872dca16d6c22dde855a74ab92cdab03e255e0518ee40b4cc5ac` | 0 |
| app/OptionalResourceService.main.ts | 5478 | `f675f9ac06fbf801e8c7c69c5c2cbee8d01d208986d03c676c22a9a5f6334e88` | 0 |
| app/PreventDisplaySleepService.std.ts | 1142 | `3eb56f81dfa4eb4587187d8871f797ee113f0b342a0aa92dea68f7796187eef7` | 0 |
| app/SystemTrayService.main.ts | 10540 | `e05ae8b8f1fb551786eb77eee80930533d07b82ece1fdbe925a72266576718c3` | 0 |
| app/SystemTraySettingCache.node.ts | 3146 | `bd4a079b0544250bcad09d6c3a35220930943a42e32c92ff98d4bb3e16bbead9` | 0 |
| app/WindowsNotifications.main.ts | 1538 | `0006080bfb462b67383195bac07b87d6fc0884a62de7f9101ca8ea8b72b81e5b` | 0 |
| app/attachment_channel.main.ts | 24042 | `212288a0bd3e7c2493a0ac78c0c8a70746ee64036c1b0cadf48176af92224777` | 0 |
| app/attachments.node.ts | 9471 | `5c863578d4a447de80df075c27e4a50e68dd1b147e76fcc73e98e44a6870f6ce` | 0 |
| app/base_config.node.ts | 3450 | `153d6f14527755ec250363f4f971bae2a0e5b52d722117b08e163a2d8f023bd2` | 0 |
| app/config.main.ts | 2679 | `d152b196ca706ef0b4e042123cb91e887c27e6bfca1f094dd8492bb80e58a070` | 0 |
| app/crashReports.main.ts | 6337 | `edda1a68fdffc7c29603b96dfe5a6f0cd51cc66d8ca8080d557dfa7b6e4f7f91` | 0 |
| app/dns-fallback.main.ts | 1131 | `75a432a6227896c0456dc7a5536b92fb4b8f1f80150ac60bffbb1e44e30c1a40` | 0 |
| app/ephemeral_config.main.ts | 608 | `a5d1957897cdf667dea7725bc7e56488b1904c47283824f2994b0766e10aea4d` | 0 |
| app/global_errors.main.ts | 2573 | `05e4bebf75328abbfbf483a0165bbc8a660fda28e35b966c419655505819358d` | 0 |
| app/locale.node.ts | 5752 | `5cee91b90128986aff1cc35feb81ae00cf3864667085b46ec70179f9ce891bab` | 0 |
| app/main.main.ts | 103162 | `1dc1d928ea06fe3fd920f407da70469f6039d0a39c53641fadd313d3d55cf477` | 0 |
| app/menu.std.ts | 9273 | `7343577cd2198e21045a9a006d1232af3513678c17f661666b7905a90ecf4c20` | 0 |
| app/permissions.std.ts | 2958 | `caaa519987389fcaba2bbf6eded2005b13abc6ae4e4bd17ac9178b78919505b0` | 0 |
| app/privacy.main.ts | 439 | `01a7a80007c245a7d222982eeb2bdc48f234f43a7cb2a91e2e49e6fe8ae853f2` | 0 |
| app/protocol_filter.node.ts | 5704 | `cdde17c0b41d01412b84534c2d0d03fad47e0ad2a004579cfeca1eba1d07a930` | 0 |
| app/renderWindowsToast.std.tsx | 3183 | `f32a4d4f34f9457f41dc3fb29780ce131f58101a0b782498ea599f72f3b434bf` | 0 |
| app/spell_check.main.ts | 8031 | `4e75b658596f14411f95e3bd9e0cc37fc602442eaee8c1d9eda64b056c1cdbb5` | 0 |
| app/sql_channel.main.ts | 2594 | `1f5769a6e52f36a0575f65eb4bc0df5e13ce34bc49c001fe8560ee341390ce48` | 0 |
| app/startup_config.main.ts | 688 | `7574d9561bf3f6a6fccae0baced19e0cc8f7907eecc436bf78f0546db63e2005` | 0 |
| app/updateDefaultSession.main.ts | 3286 | `a0f0e07e17822e172326996f992fdb076896c99a63373ac3838a29d82144b461` | 0 |
| app/user_config.main.ts | 1654 | `323735848b1c36e1c01b69f7aef7256f030b740d9c9d03f53f613d439b501204` | 0 |
| app/window_state.std.ts | 709 | `7901ca6301518cc41371378bb60e543c46d4955953e6b7990ef9ddbb0f7ee41c` | 0 |
| ci.js | 788 | `abd74e91829b9f08417f88a029866258a5b09533a909a7286c3b979f3d6785f6` | 0 |
| codemods/color-system/01-update-tailwind-classes.mjs | 15216 | `190dd8fe9cd819de30b9ec157660f94eb4412a629023f3567ef6fca7c5515dda` | 0 |
| codemods/protopiler-migration/01-remove-finish.mjs | 945 | `f018b43a1b9cc38f8cc0de4c0ec106c3963c277f2204b99e7b5afadb3093cfd2` | 0 |
| codemods/protopiler-migration/02-remove-i.mjs | 865 | `ba08b791d88ae0f83b278ea358de698d9e0b693f772e888802a6bc71778de954` | 0 |
| codemods/protopiler-migration/03-to-number.mjs | 2216 | `f6476af8337efcff6845fc3a5ae010f1c3db667c97d2291dbf9f5bb74320da44` | 0 |
| codemods/protopiler-migration/04-long-from-number.mjs | 1784 | `9b1dd45bed9be79fc53faeff66bc4ee52016c65ef92b9de1b3586bb11f3d358a` | 0 |
| codemods/react-jsx/01-namespace-to-default.mjs | 1223 | `034874fdaf814efe97dd88baa7ef1f40cbd65048757151768476fa31b8016b2f` | 0 |
| codemods/react-jsx/02-to-named-exports.mjs | 7064 | `9fac6abef83f798e0cba47b42c0ad6668ce067862f3c1d43157882af7f7c6978` | 0 |
| codemods/react-jsx/03-remove-default-react-for-jsx.mjs | 1768 | `9ed0829d6959cf70a3759376df80719390baedfe5d61109573b162c7701ed4f1` | 0 |
| codemods/react-jsx/04-fix-type-references.mjs | 6176 | `1f4c367415561c3fc7abecdb163b654c5f51fd3443a687162ca5f47d2f4b5293` | 0 |
| codemods/rolldown/01-rename-imports.mjs | 1688 | `3146c47a0e8d578f06514932822899f1b33394bdee04ade33dd4eb608e857a3b` | 0 |
| config/default.json | 4938 | `df16b59a043ac47c39b8d21cbc35cbe10459d8801dcc628df12d53491f46a869` | 0 |
| danger/.pnpmfile.mjs | 595 | `6716b096a52c10722fe126ecfe531d53a5ab62b75d9b779c508542c79974a399` | 0 |
| danger/danger-exports.mjs | 707 | `dde8ba2e6f29c279f9e9b840116f99343ed4b08844ffd31cedde4ebc8ee1b63a` | 0 |
| danger/package.json | 615 | `f9d688b5ac0598ad71fb9bb57f8a24d0b103d02d04903b41109f54399dd96a18` | 0 |
| danger/pnpm-lock.yaml | 43137 | `a170b0103cb80ca1d72b3037c81d904c27429fc5bd50fa4808807ebe2001838d` | 0 |
| danger/rules/enforcePackageJsonPinnedDeps.mjs | 1543 | `0a34560e1bdb47b4198a902deb0a77b4a35f6ba30a52f339c4945bcb6024dab8` | 0 |
| danger/rules/enforcePackageJsonPublishConfig.mjs | 1912 | `9b6a3293b522a17ed88651742014e0fea7d67a432ed13917ce9fbf28d1069766` | 0 |
| danger/rules/enforcePnpmLockfileDepsIntegrity.mjs | 974 | `17a84231ed95c83c6480bb5f05a98dfd645d7e4519db0988fe3d7f9091fae9ec` | 0 |
| danger/rules/enforceTailwindDepsMatch.mjs | 2175 | `a9a27275012778c74ad0a36dcd5b9ef4d1f04530e4aace68f403fba7ba061274` | 0 |
| danger/rules.mjs | 303 | `96c6f63438fa575d669ec93ba0efa766481e4396a691298acb9f679ab3172fad` | 0 |
| dangerfile.mjs | 125 | `f3f5f9f5703c2e0625a419e2518a04da82614517f248dc2e7a1e9b3b484f81ae` | 0 |
| knip.js | 3899 | `272277e39966a650e26f785789e5f412cca1792ec697ce9fbab758b2111351d7` | 0 |
| package.json | 25135 | `7694973e611a20ee50bfd7fd53e8b16fd4de18aa9e1a68ddbd6b1f349bd1f837` | 0 |
| packages/lame/index.mjs | 1411 | `a370853d082495514234130c94bce7465e0c7fcb4f83f5e228440ff9970c28bb` | 0 |
| packages/lame/package.json | 371 | `d162395e7d079ae092e710c88b6c71d79d7b0e5100548dda597125b513cd6805` | 0 |
| packages/lame/wrapper.c | 1172 | `9269138831a85ec54026434900f5d04ae84b31763ac1ea9e0a9a310a15910614` | 0 |
| packages/lame/wrapper.mjs | 264556 | `90a0aad263fecc5ff3a53177bfe8c036696dbafdcf00d80288d04e4c6e03768d` | 0 |
| packages/mute-state-change/index.d.ts | 369 | `a0b9299c32410540a7a2779462b5ec26c725dd1ad97981e91767a77b90c0315d` | 0 |
| packages/mute-state-change/index.mjs | 898 | `0993edd407254615f8b85af638f13a793facad4afc2c0362890a7aeadb2a4896` | 0 |
| packages/mute-state-change/package.json | 995 | `922e963a6cba70e921a4d1cf02060b63d1583213da1fb2a25a06ce27123b1050` | 0 |
| packages/types/package.json | 1193 | `e299d6e3cc841d36ba6f720171f77a46c59297d56397e847fb7c0587b30b2424` | 0 |
| packages/types/src/Result.std.ts | 1042 | `4f9bb2a015f14cf10c00ce732fc4450b580b529a83cd77425decda9c1e2c3b1c` | 0 |
| packages/types/src/_utils/address.std.ts | 1319 | `8fc5ab4d84ab9756060309dedbdb1c2470958c6504cea14aac44d22f3729558c` | 0 |
| packages/types/src/_utils/bytes.std.ts | 1567 | `fb0eeac900fcec7c593963f9107e7f9e5cdb23b2483334cac0196bbf3e8cee16` | 0 |
| packages/types/src/_utils/datetime.std.ts | 1239 | `af570e106f96660b391e50c3a8c50b77647aade2f5989c9b8f67876e0dd051fd` | 0 |
| packages/types/src/_utils/numbers.std.ts | 792 | `de9ace2d1d876102a382944122569c67d41b53c4b9fc21367b59121d51191c52` | 0 |
| packages/types/src/_utils/pni.std.ts | 347 | `268b0a5e21d3476918c6e36fd30dcfc161d43c3946260e1c42378c75e3f59ffa` | 0 |
| packages/types/src/_utils/schemas.std.ts | 511 | `c82b1f2a4c68874c0deb54d57977233f3010b5f261122700684eb871ae810eb7` | 0 |
| packages/types/src/_utils/usernames.std.ts | 3122 | `2e98d16ef667b6974dbc785899b512850d623d450c8f1f10e386149a39dae400` | 0 |
| packages/types/src/datetime/DurationDays.std.ts | 1658 | `639a2a32af30b9d63a17ae632672e328b7be1833c17081b90309952ca6e5c586` | 0 |
| packages/types/src/datetime/DurationMs.std.ts | 2145 | `27c3f888e9930b7a4abdb9403564ad437c02886a68d6f9aae89726d2329a4ea3` | 0 |
| packages/types/src/datetime/DurationSecs.std.ts | 2020 | `11eed7962db559375f2167f1494877f94545c0f97754430e94c7cfe94c453cf8` | 0 |
| packages/types/src/datetime/PlainTimeHourMin.std.ts | 1258 | `3e56506c666811af536ea35b64e1d009db62e645ba9df0e3512448ec97fbd0f8` | 0 |
| packages/types/src/datetime/TimestampMs.std.ts | 1431 | `8ccbe349ee1bcd4a68c0a92d62b69e103447c5755f8e6d9aad8ad845dfb448e0` | 0 |
| packages/types/src/datetime/TimestampSecs.std.ts | 1299 | `fd7aa9f29209e50a34613f2e8f512164f362a91f180202846fa2536bc2b49f20` | 0 |
| packages/types/src/encodings/Base64.std.ts | 1308 | `fd6512ec31f4a5cd1c45df54d1caee5cb864138f8f8bb19a2dc95645123f1fce` | 0 |
| packages/types/src/encodings/Base64Url.std.ts | 1428 | `984edc63c0542b0b02db05b13a48bf3918f6bd388c37475c360ecc6218fcf80f` | 0 |
| packages/types/src/encodings/Bytes.std.ts | 935 | `cf0758c3d045908c79369c67cbd1a5e718b2c24884c02876c58784d8f5f2f246` | 0 |
| packages/types/src/encodings/Hex.std.ts | 1251 | `3d4ba346c90609011b90af95ee51bfb4db65a5561920953d6bc27729dfcd4347` | 0 |
| packages/types/src/encodings/Json.std.ts | 3491 | `ef99585ca0a1168b980527890761ff4e967a05dd0f32760aafaf441532280e02` | 0 |
| packages/types/src/encodings/Utf8.std.ts | 640 | `e6eb018e07b8deb0c903ea1bd2a8abae2590f066de0e380cbc0ab08132b6d599` | 0 |
| packages/types/src/formats/CountryCode.std.ts | 753 | `a837b7a5375597b42487c1f4badb7ab0d31123c846090c56e3336c17f13c6195` | 0 |
| packages/types/src/formats/CurrencyCode.std.ts | 753 | `aa39a9c8c41ca3d582b80cdc49181c55ce2937157e14bbb84095af92b00c387e` | 0 |
| packages/types/src/formats/HexColor.std.ts | 716 | `84134fe4f4dc9c6fd09f83eb4b824a2b16da2e5a4084ddf15bcf567f3bf70a83` | 0 |
| packages/types/src/formats/HttpUrl.std.ts | 656 | `608f304de13e1d6dfb163bf2570324b80980d5475dae5dade7d6bdda3df9d3cc` | 0 |
| packages/types/src/formats/LanguageTag.std.ts | 878 | `b9d54f9dff5309dee10e00398e05226e4f280957fe32c666900a07868fea0407` | 0 |
| packages/types/src/formats/MimeType.std.ts | 708 | `a1da0d77cc496aa42e6c9ccd0b40ea35124c9d346abe2279852f464869b1bc29` | 0 |
| packages/types/src/formats/Semver.std.ts | 802 | `39f812a40f82f2d27de89d32f2af1c1ca7b8078950a32f2b29b4c7cd9eb3cb26` | 0 |
| packages/types/src/formats/Uuid.std.ts | 952 | `4c8c3d2ed44d708e5f3ce017e8f9a870219707a8db64d153f7127d9870e8ba8a` | 0 |
| packages/types/src/index.std.ts | 4313 | `f918c51730aa3c96eb5cf582ea7e22b12faf0069caee2c6e980b2aa86fe49433` | 0 |
| packages/types/src/numbers/BigInt128.std.ts | 947 | `be7d41e3bb794df0aa80599a386c238ebe5e7c0e7237b54c65e246766b1eab7d` | 0 |
| packages/types/src/numbers/BigInt64.std.ts | 934 | `21de9d0566d2bc28aa3d53c8e02c45a94e1caafc4e45c8be1f7a18254c60860c` | 0 |
| packages/types/src/numbers/BigUint128.std.ts | 948 | `7afb845bf3c3af84e09562deaeb72c01dc4ad226b605722e6575c5d61353c404` | 0 |
| packages/types/src/numbers/BigUint64.std.ts | 936 | `5700c40b5181fe873e9f7f209578198ef313c54e1cb3aac07e53c69f30fec914` | 0 |
| packages/types/src/numbers/Float16.std.ts | 802 | `2c976df645031bdecea175cbbdcbc7464cb97ce64ee24fe2b0f17e9a7c4a1b4b` | 0 |
| packages/types/src/numbers/Float32.std.ts | 800 | `3e6e3bb824a574634fc87685663083be8c76eb94a08f9caf8eaed591642eef1d` | 0 |
| packages/types/src/numbers/Float64.std.ts | 688 | `0f3ff0ac885074f668b2a9cc8e7b7b3fdb3b129876f1043e0d1a0bd2779c1107` | 0 |
| packages/types/src/numbers/Int16.std.ts | 975 | `f609ba81bdfe8f810360a1bbc49812b2443ce5884c02b5b0eacf08ba648af50f` | 0 |
| packages/types/src/numbers/Int32.std.ts | 975 | `00fe3e46e33b850754ea548abc429cf5f5b69a9a15f36360392d159064ae23fb` | 0 |
| packages/types/src/numbers/Int8.std.ts | 962 | `debf9f1bde104a6e55cb4bb0ec1a70838af5bcfd71c3d8164c3a9f79db600e69` | 0 |
| packages/types/src/numbers/Uint16.std.ts | 978 | `b54fd02ebede1ede86888e7c0665590c7f5d4f876508ed5d25e59c24b7fe339c` | 0 |
| packages/types/src/numbers/Uint32.std.ts | 978 | `30cd3bbe02bfc5dcf5c07eecf08af7cbdb4750a31151757db3dba05cc92e5e33` | 0 |
| packages/types/src/numbers/Uint8.std.ts | 966 | `7ad304a4021e4e404c5f68ef0bcea9c79cddbc2148549744ba8c3851982757e9` | 0 |
| packages/types/src/service/AccountEntropyPool.std.ts | 845 | `a074250e78bf63e6429060ddb1b70df0607171e4652af8afb69fd4620c58c47b` | 0 |
| packages/types/src/service/Aci.std.ts | 1274 | `58fdbbe9eeda56b4d162713ae29ac1e8c5a437790300c8f5b15a2863c4c11f1b` | 0 |
| packages/types/src/service/Address.std.ts | 1625 | `2341ba8541e65728386585d9d2511c9634d4ae51195c3477bc3bc30e755bc79d` | 0 |
| packages/types/src/service/AddressInfo.std.ts | 1405 | `93dd917598e7e540e95a5e03533bbafd790d2ddeca5a4db1728eebf2688ec45e` | 0 |
| packages/types/src/service/DeviceId.std.ts | 841 | `7ea4ed8b79478bc6aa946b308d3fb53220aad50fc116f348a8d3c807e30e742d` | 0 |
| packages/types/src/service/DistributionId.std.ts | 1366 | `d7b41aa22782903ecca2c0a0527ef91e2a2854e74934b0e7e33745381eb7a64f` | 0 |
| packages/types/src/service/DistributionListId.std.ts | 1410 | `9e509102fc890e9c4409587134a719158d190ddf8ac142637b7303d0cff41201` | 0 |
| packages/types/src/service/E164.std.ts | 1150 | `513095dbad3d41d670b9fdcf70a0ea5f57e44553f2c53f907a0ff11bb932b6c7` | 0 |
| packages/types/src/service/GroupId.std.ts | 1264 | `71021481ea151d547c57cc4e5473fcea682229b6bfe9a141e8dac96351ead595` | 0 |
| packages/types/src/service/GroupInviteLinkPassword.std.ts | 1455 | `6ed0976eb90e57474648e99d06ada6690f27042b196e15ecdf6433b4c2dd8b26` | 0 |
| packages/types/src/service/GroupMasterKey.std.ts | 1269 | `bf5c4c1e7951dba8609f2e883ca2d6db3f9867f7b85c824492eb07cfd7a57199` | 0 |
| packages/types/src/service/GroupPublicParams.std.ts | 1222 | `cf23984302b45bc728df82fa3480b4c4a7e6f89091a38440c3678169eebea8c1` | 0 |
| packages/types/src/service/GroupSecretParams.std.ts | 1222 | `de3f3957d1223e808ccb08369cd37d8a10972a1029146f764233bcf37e18e3c7` | 0 |
| packages/types/src/service/GroupVersion.std.ts | 913 | `ad9daa32991d9e73725bdcf50f9aef5fc02abdd81087b34dbd907570d97653c3` | 0 |
| packages/types/src/service/MuteExpiration.std.ts | 2499 | `6dd82573e80adbda732bd592693fa35506f5fbaf209202c5abae3eb13a891e3f` | 0 |
| packages/types/src/service/Pni.std.ts | 1660 | `95795f899829a4f74c41295de81c5e7fdd80a841255b5266326e886188202dea` | 0 |
| packages/types/src/service/ProfileKey.std.ts | 1229 | `f52f7de652138ea9f34e10fd16247f9cf3eeead4734cf97935692f9ab81483f3` | 0 |
| packages/types/src/service/ProfileKeyVersion.std.ts | 1186 | `ec0a351001dadb85865eced1689c78430533b0ca1563200c3d00a7c226375681` | 0 |
| packages/types/src/service/ReceivedTimestampMs.std.ts | 1243 | `687e3586ad8e1cef5de0fbc99ed7bfd34cadc927ae8ebed8f45ce79c5e6762cc` | 0 |
| packages/types/src/service/RegistrationId.std.ts | 910 | `e3148882f88b355e9f84ed98107d22f92dc1e6b7815a64bb89fe09c40abd0b92` | 0 |
| packages/types/src/service/ReportSpamToken.std.ts | 1287 | `b1edbd862c720ce2aa48d4eb30f5cae1cdd4f544dc379b1a8e44ef14aff4d8a9` | 0 |
| packages/types/src/service/SentTimestampMs.std.ts | 1198 | `52027610b414cb5b4d3bf97ddfe7f0fc637655851d990ff495ae803c9cb5bc70` | 0 |
| packages/types/src/service/ServerGuid.std.ts | 1281 | `67542fb72041721a2ddd4f37e4a53048daf7ed57a4eccc244f87daaf19d57cf5` | 0 |
| packages/types/src/service/ServerTimestampMs.std.ts | 1248 | `f3c5e43a000cd2e69c664749065b9a62f564540485abf2103b6c14b8813591e3` | 0 |
| packages/types/src/service/ServiceId.std.ts | 1175 | `e9e4dbf0738bb826ea1d37ffaecc761300b6815eb03e2acd9b46a00a6bb868af` | 0 |
| packages/types/src/service/StorageItemKey.std.ts | 1236 | `f8ec562c58293231c8ba5ffa2876e79b7851fb7f3ee6a13f364f34d97ddf389e` | 0 |
| packages/types/src/service/StorageManifestVersion.std.ts | 993 | `ba99ef8ec1b91c193a9b83d03e219da20ec3aabbce6049410e67b05970d744ad` | 0 |
| packages/types/src/service/UnidentifiedAccessKey.std.ts | 1385 | `72f15e252431f606fe70cc9edb331fee048bf7c75b8f22dd10ab9240a1e2f77e` | 0 |
| packages/types/src/service/UntaggedPni.std.ts | 1595 | `edce2ec8508701cd9defae27dd326224a91fd3b4da4c361163f8a0800875f4fc` | 0 |
| packages/types/src/service/Username.std.ts | 1388 | `57cfd4aa27cec208bd7ca47709e9cca4bc87f2995fedf56c770f87ecdabed82d` | 0 |
| packages/types/src/service/UsernameDiscriminator.std.ts | 971 | `2eb7ef9ed7a499385e06d7bbdab03c24ed2d441939c8d6a867b43cbbfaa47d3b` | 0 |
| packages/types/src/service/UsernameHash.std.ts | 703 | `c30a38990624d77e7fae9832144142005e6167b8268aed4911ccc1c738e6c0c4` | 0 |
| packages/types/src/service/UsernameNickname.std.ts | 915 | `e6c92aff4012dfa9ca43abef469e621ba4d4a933621b25c0da6179e3ef3e658c` | 0 |
| packages/types/src/service/UsernameProof.std.ts | 679 | `e12801631a5279d46688f13144a7cdb46c0b50dc58e79ea49449f02a416bbb35` | 0 |
| packages/types/src/units/UnitBytes.std.ts | 1390 | `ec3d7e79518a4ca12277a7c5fd827e66ef51d9515a10b5dbff4741f397e9afc5` | 0 |
| packages/types/src/units/UnitKibibytes.std.ts | 1325 | `25193deb03d2093ac3625d9350652754d6d06d86fe59b5352f7009f757bb2720` | 0 |
| packages/types/src/units/UnitKilobytes.std.ts | 1324 | `6a4ec96a4e984199fb32a4b41000d9e5ab7ccefbc2e0e709d3c96c52752fff5e` | 0 |
| packages/types/tsdown.config.mjs | 310 | `6f851d25e1ae8233bdab3620ca75e76b150044710f36ce4373cc629ccc12bdea` | 0 |
| packages/windows-ucv/addon.cpp | 4761 | `71fa92a33cf2762aff1cd48e46f19ef7bd2b12424e0bb9ae02bcaab0ea4b3bc6` | 0 |
| packages/windows-ucv/index.ts | 2449 | `e098095ea5404661c6cd0698ef233d64a4c6591fc6958f4b9391ce98457919f9` | 0 |
| packages/windows-ucv/package.json | 890 | `b19b993bcbe13b6d0085fade0f569825e114d5192c5883cb3a19eb75a495ffce` | 0 |
| pnpm-lock.yaml | 1027918 | `7f9e6e9b23be82a60f32e9f6bd143c78aecac29947f92f3e86a00f1182b2769a` | 0 |
| preload.wrapper.ts | 2291 | `1947efdd1e8e1fcaa839dac598d852cea91eef2a85a3fe46ed9ed36763b07037` | 0 |
| protos/Backups.proto | 44115 | `1d0f18c12c1aedc9b3bb0f85db18fd412ac0fb093f0ed3e903acf57f1f450ed7` | 0 |
| protos/CallQualitySurvey.proto | 4035 | `9bf306b2a7122173d17ee9e80fc67ca10041a4ecf8da971998e88d06bb98f8a9` | 0 |
| protos/DeviceMessages.proto | 1699 | `a60bc81b933cb16a6e0dbf8062ba7ad2ab57d435076c96f94c73e757ab706884` | 0 |
| protos/DeviceName.proto | 244 | `fed7cd39825bb43f1727d6a7f8c8f155d410696441b0c288ea30eeca141b75b4` | 0 |
| protos/Groups.proto | 8246 | `9e197da7e9d427131326be60b71fa00073e0db3787345f816eba28d0f3995d76` | 0 |
| protos/JumboPack.proto | 254 | `f1affb2ccf5ce30b48e155698c298153946791be539f881f118d57e1a8f2e7d5` | 0 |
| protos/KeyTransparency.proto | 323 | `6c65dbb7b5f05f76d577e255b16c851b8e9a4134361770ca3cd88a2eee4e90d9` | 0 |
| protos/LibSignal-Client.proto | 2624 | `12411766658bfb6d33103630cd8aa59c670b399e7bc2c1e3f042053f3cd1fa40` | 0 |
| protos/LocalBackup.proto | 797 | `d593361c954be9a82d8bccd784cbfbb73a67b8f5c211b473cad4a9bb90ba0747` | 0 |
| protos/Migrations.proto | 2216 | `89653245862d28d9c7c3f09a0ddbfd13b4a9f893017dce47e4b751c05087786f` | 0 |
| protos/SignalService.proto | 29795 | `3ddae8dd51ef7bbc5f93027bb4e571305ca849db544623d71b2c8342783d2635` | 0 |
| protos/SignalStorage.proto | 13173 | `1e092957a4b0bb938e8862a2d4f720f3cce19718fb9a25b35fc918d218a9f49e` | 0 |
| protos/Stickers.proto | 350 | `ec2376155798d26f94cdec20fbdfc5288505a3bce8f33bdc0d44bbd63627ae82` | 0 |
| rolldown.config.ts | 5013 | `e064947268c77e62691f7ae2719f4e5487f8802fe87a18d35c0dc2f30810d780` | 0 |
| scripts/after-all-artifact-build.mjs | 429 | `4b02d5320a8c7a6f564ff67ac932163bd3fc215c902e31fce82302e3dca8e2b3` | 0 |
| scripts/after-pack.mjs | 719 | `43f58970b8b422466e9afb4b8de7c0f46b0dd4010fc55af7fd36b9f1ebb7c1cd` | 0 |
| scripts/after-sign.mjs | 534 | `404bf3224aacfe9f29ebbc8cfe1a4a6beb92866b1568c72e46e91e3b6956e87a` | 0 |
| scripts/artifact-build-completed.mjs | 2117 | `e2c0ce4b52091342e1cd067845f789d867c29a68466ab9c91cbab11b4f9cdc8a` | 0 |
| scripts/build-localized-display-names.mjs | 4076 | `2f59f4ff07ff05eb5f795e8b9e00f7a09abff657b8be3f73902911ab0e0a7170` | 0 |
| scripts/check-min-os-version.mjs | 9745 | `3b6048e026912e00f191a8096794974e83af5cc15dc5c107afcea8a4d4bbe99e` | 0 |
| scripts/check-unused-icons.mjs | 3584 | `bdf781b416d3ee75a1b4b5bf218eec67762decae85bcb0f49e0f71364083e344` | 0 |
| scripts/check-unused-styles.mjs | 2931 | `9c9ca0a0a23ca8747cf2c1fa90897426f2c0a150cdeb304633c1d03700fc869a` | 0 |
| scripts/check-upgradeable-deps.mjs | 9330 | `b18de68f695024ed9269dc8d885f23dcf8e1bf418835cc493f6fa58468d53379` | 0 |
| scripts/clean-transpile.mjs | 959 | `0dfeeb2c450f3be56a4c79d0342faf4c5288b0c29b02b4ed939c4b97b615b2f1` | 0 |
| scripts/compile-stories-icu-lookup.mjs | 1564 | `e09f81f796c14827f247dccb1346f59860caeccbef6bbe0ed70bdb0d8b87acdf` | 0 |
| scripts/copy-language-packs.mjs | 3107 | `53001c715a301a1a6332fa38bbaead6f681eb4ac6e71e04805ea577e25e1ac18` | 0 |
| scripts/ensure-linux-file-permissions.mjs | 819 | `92e67ea4d0e87e3917b387fb1acbd6bb815bdf7248ce41154edd47a39ef67e89` | 0 |
| scripts/extract-info-plist-strings.mjs | 1217 | `93f195f63dcbca72621b421f448bf2250c8bd100ebb0696f13498b6badb90786` | 0 |
| scripts/fuse-electron.mjs | 2037 | `ef633be12f55a420837c156f30e0a6a5af24faa0fada98d7d68fba057661d2e4` | 0 |
| scripts/gen-locales-config.mjs | 1846 | `dd2cb4bc9785fcf681d1265d65035836d5716c334c7fe9341a9d0fc3e0d17ac7` | 0 |
| scripts/gen-nsis-script.mjs | 2941 | `74e244c0cd09c3d8a2563f62b52f7afcf305a746017cd1b6581b75d3b01c1cc0` | 0 |
| scripts/gen-policy-files.mjs | 3459 | `644c610c1c6bd96320077ed958b9b013a5ac0911b1cba5ddf97776855a75a05b` | 0 |
| scripts/generate-acknowledgments.mjs | 5100 | `2d70cb3d8106cd7d566beda50901d77e733ff9c4c4c86d3469a63ddf43268226` | 0 |
| scripts/generate-compact-locales.mjs | 2395 | `1628324557b5b79e1657dab64919104ea2e443ea8bf8a23be18a546bd124dafd` | 0 |
| scripts/generate-db-schema.mjs | 11436 | `50d1ad9a20d02a2f9999c2f2c4bf47c7319205fe540c2c6e1be7e5de1a2a3966` | 0 |
| scripts/generate-dns-fallback.mjs | 1520 | `98ddbc5ef80507d1aab7ba1c9b715da83aa1042c136c704b2fd324096740ca9f` | 0 |
| scripts/generate-emoji-data.mjs | 7788 | `e753446b46704cdf50aa0509feee77ebc84db0e383240f20c0bad5e9eaaf63c7` | 0 |
| scripts/generate-fixtures.mjs | 1201 | `208e43862ca9dca7878a95dba6850c44c3fa98e1c2f560d8bed7f4485c3b612f` | 0 |
| scripts/generate-icu-types.mjs | 7650 | `b32f6f25686c64fd6899019e00859473b34958013b731f80c0200fbe3792dc4a` | 0 |
| scripts/generate-preload-cache.mjs | 2247 | `d16d654982f0ace7e68197fddec4c7fbc93a0acf0d7f94a24231ddc3cbd68710` | 0 |
| scripts/generate-tray-icons.mjs | 7690 | `6e209489bc935efb148538a5433ffcaf8822fc2848056666ffb2671971b085e4` | 0 |
| scripts/get-emoji-locales.mjs | 2557 | `d7dfbd1223faa6128e54c52104ea0c4ff178325e3720dd926da2d3dca1acfd89` | 0 |
| scripts/get-expire-time.mjs | 1082 | `1b88b99b7a87d0f6aa78818b2dcc3b04d816c3de985d3ca6d4a449826c1843d3` | 0 |
| scripts/get-jumbomoji.mjs | 2724 | `d8be765ebc6f08b7fa2739b187d284925ff47191b9ce44015d910138f3d46960` | 0 |
| scripts/get-strings.mjs | 4469 | `d0e1dad77540415ffd60938ebb1d5fc13fb19b864c9f77cf38a08da4721b1616` | 0 |
| scripts/mark-unused-strings-deleted.mjs | 2256 | `d976ff389f63073e69b73d1398fcaf4ae156f3a3a6b1b3611bb83ee1819db26d` | 0 |
| scripts/mocha-separator.mjs | 938 | `bdfae2ebc5b1e1f282ea892027eba064b9e99cd70eb039250594ccde4f5db2eb` | 0 |
| scripts/notarize-universal-dmg.mjs | 2063 | `3415a3da48429c4ba281115fee833f7b836e7085ca9dde5bfe4f4ff6010b4f31` | 0 |
| scripts/notarize.mjs | 1674 | `942239b9463927948909f717013b0af456d6d30dab6736f9a6b20a5d951eca42` | 0 |
| scripts/prepare-no-delay-release.mjs | 473 | `005f3249eaf33e0a3249ffbe6a231478dfb15f9092c9d9a8ad64a7bea9193201` | 0 |
| scripts/prepare_adhoc_build.mjs | 3875 | `e21c345db30ff751626cc1646d661973a19fc62833d6df661a7b7cfc58b26a88` | 0 |
| scripts/prepare_alpha_build.mjs | 3090 | `0eb64b9318f8bd62aa58f0103ab09e7927231cbc18d3e8913900e79a0f0d0f33` | 0 |
| scripts/prepare_axolotl_build.mjs | 3133 | `4d1d7be33fba33c25cb44cf1c715af0d634b2e90b042fa2811c11fba5a3c5c7e` | 0 |
| scripts/prepare_beta_build.mjs | 3003 | `b9bb7bfdd1f60c394b17283ec47456f521eabd32cae8d45393ec93661d9403b6` | 0 |
| scripts/prepare_linux_build.mjs | 1189 | `b58e977be056d994ad4010e936ac9f133fffc29ef8a67167c5de0eacf985f41e` | 0 |
| scripts/prepare_mas_build.mjs | 2772 | `41d2090f37606653ffa5ea20a4d99a2cc3609939796efcf9ef45c7154a118f5a` | 0 |
| scripts/prepare_staging_build.mjs | 3459 | `6e63590eb1e5d9288bfe08d0716590d4aa0c492838d20c557403e6e3997f7b9d` | 0 |
| scripts/prepare_tagged_version.mjs | 1019 | `2fa205e7c2036cf19bae107de88fb80f6e1501af45c7d176a20d5fcd6dbade7e` | 0 |
| scripts/prune-macos-release.mjs | 1780 | `60a48e8c7d9724de2a0f274efafb1cca7d081abf7cba076cd83ca473610b3934` | 0 |
| scripts/publish-installer-size.mjs | 1800 | `95a7ca8481225daa53b8f0c48ab16e836b84b19d8f5f832a44479e9bad24f565` | 0 |
| scripts/push-strings.mjs | 2401 | `e46354e5c7600fb79dd0ea781262b3e18ef537d90e2f80f187d757aa9eb0a810` | 0 |
| scripts/remove-strings.mjs | 2782 | `82ea77291e789c72a00cb3769d845fb246652243c3ea71721e446e82c3006951` | 0 |
| scripts/sign-macos.mjs | 1400 | `1b429b72dd47894ed008489693e45b64d2629e2fe6fcba0bdfbf98381f766c2b` | 0 |
| scripts/sign-mas-installer.mjs | 1070 | `128ed61f5116730554f3d8527a1a368565bbae24e9629bdba5f33d98a241a9bb` | 0 |
| scripts/sign-windows.mjs | 1229 | `18ec0236e45a9f6e6eeb4d75f302b180f721a70bc4647c667558754e7f2f37c1` | 0 |
| scripts/symbolicate-crash-report.mjs | 2772 | `693fcbfd19e8bfdb43e54155cba9f7c3a9e5a77ef75895653dd6064dc94c68a7` | 0 |
| scripts/test-electron.mjs | 6539 | `f3273483778f930c260bbc6ed88aaef8eafc6ae43c7ddadba6b2b5786493ce31` | 0 |
| scripts/test-release.mjs | 2861 | `4427a2b0ab48f56996add30a7812da359f6cc2e8149fae6ebfab9117cc9fc043` | 0 |
| scripts/update-gha.mjs | 3318 | `6c761261d00131ee54ab5ff1ecb3663229ea3622a3eea55bd3bd730b417a9acc` | 0 |
| scripts/update-signal-symbols.mjs | 7386 | `64333e246909fe601d2fda3a9f90aa587da2ced7e80d7a95b58c0984165dbb3e` | 0 |
| scripts/utils/assert.mjs | 464 | `a4646cc9467d69f654220baf4ac25639059e2b121867bc5e1d05dce9d2d582d8` | 0 |
| scripts/utils/better-blockmap.d.ts | 394 | `0515d1ff4c489e01207e4830665f45cb6e21839fa6ecf1709519bf9572095c11` | 0 |
| scripts/utils/durations.mjs | 222 | `b70adb88d3e47ef75672cad2702d23d71d61eab07a340be38aa93093555ec499` | 0 |
| scripts/utils/generateTaggedVersion.mjs | 1186 | `4d053581eeac5462aef01a76b73e634f20131ad6570f5fca9e0a3fb51a2050d0` | 0 |
| scripts/utils/generateTaggedVersion_test.mjs | 2858 | `591763d8a6ce0685fe4528c241089eeba0a94269e4d1cbc7bda5647e03723d18` | 0 |
| scripts/utils/getBuildCreationTimestamp.mjs | 439 | `18d7484c437a7f3859529ff36310e0d122ee335cb42eee577766ad30f7f27113` | 0 |
| scripts/utils/getICUMessageParams.mjs | 2576 | `c153aeaef24fb7d4eb2db60cf19981276984a17bd775a335e70e774c6c2e6091` | 0 |
| scripts/utils/intlMessages.mjs | 176 | `8cf2d2c8c34533229d9117fa0c1e46c6a71685301e2fc3544bcf93502d1946a7` | 0 |
| scripts/utils/nsis.mjs | 3891 | `88e9925bb711ea1c2c382c3013689f0d3b6507e65c1186a98bcc2e1240af21d0` | 0 |
| scripts/utils/optionalResources.mjs | 495 | `faaeceb11b5ca59e410241385e60e0dd2a88aa775fd2bfcecc81d1e051d711b4` | 0 |
| scripts/utils/parseVersion.mjs | 1771 | `e71dd92a695eb5d64549c26087787b7cb63c861e4bfc8c81b0aa6ab0ed72331a` | 0 |
| scripts/utils/smartling.mjs | 951 | `e8f7267eb2bb31e0de02c53cfac56717289f7a1e6828fe56fc701ee0d6ab9e3b` | 0 |
| scripts/utils/symbolicate-mac.d.ts | 233 | `d4c4c80a120bc743b31a38230643634a83f2c66ac37de54aecb47c11ef8f996b` | 0 |
| scripts/utils/utf16ToEmoji.mjs | 423 | `5dcc9b8cf900f52d1e2518805baef42e0c6bcb02fbef9d162d9011d90dff3aae` | 0 |
| sticker-creator/.eslintrc.cjs | 6151 | `084331661b6dd0149fac7bc16747940fc46b6a2df9730af9b931fe64df104911` | 0 |
| sticker-creator/.prettierrc.cjs | 179 | `8d0af6f3fdad1aaba8b9ba54b1d80d8c22b83d44d1b9df33eb442a2a7035d47d` | 0 |
| sticker-creator/package.json | 1849 | `ea6913b1205247a3287f0133bdcd747d541a30f7dde78f2a041267851c2a1771` | 0 |
| sticker-creator/protos/Stickers.proto | 392 | `8c6963e45901d97d85a973bfb5615f6209fe05e781030e2c287203cd38960d48` | 0 |
| sticker-creator/src/components/ArtFrame.tsx | 7664 | `3c8000628e4a47cdf5653fa2ff1d7dab5d957869b8c9c79f39189332be86ca28` | 0 |
| sticker-creator/src/components/ArtGrid.tsx | 4877 | `041414d98baa9e09756ac762ae771637404b804583abe3742d126282560cf9d1` | 0 |
| sticker-creator/src/components/ArtPackPreview.tsx | 1140 | `76d84c795cf0ebfa635fc0a51b0223e21c095db173dc8f1b22066e64124b990e` | 0 |
| sticker-creator/src/components/ConfirmModal.tsx | 728 | `558d953341388655e49623b30021e6a9e6301771eabd2f78a197a5f06e8089f4` | 0 |
| sticker-creator/src/components/EmojiPicker.tsx | 1341 | `d1ac898a8ce96dbf0fd5980ffe6b96c32595a2d5692fcd4addbd30739ddd54c9` | 0 |
| sticker-creator/src/components/Intl.tsx | 3522 | `fba609bdfb40ca1a0b01797b6483ff107e6ae1d4c1736e0fa8d33f90dc270c8f` | 0 |
| sticker-creator/src/components/ShareButtons.tsx | 4106 | `56cf40494437e22646df2f1938b0747d58eb73c56cb64eb120417a409bb542e4` | 0 |
| sticker-creator/src/components/Toaster.tsx | 951 | `65f3062cedfb1e4765217d37968051d9f3bedfaf48bba6e1b20722ec5f530ee9` | 0 |
| sticker-creator/src/constants.ts | 311 | `12bc0beb39e60bddaaed88a0ebb4c7a2faafaebcef924770705afd777ac9d5a9` | 0 |
| sticker-creator/src/contexts/I18n.tsx | 3277 | `6c88eb18ca7f1ebe3f9960fc161b3e9f16e7a17f40e97576986b7bb9926d8c4f` | 0 |
| sticker-creator/src/elements/Button.tsx | 994 | `7f431afeb58e947b956a49333e697c9a8d7d6a4c63f0cd99143cefd8b07f17e0` | 0 |
| sticker-creator/src/elements/ConfirmDialog.tsx | 1150 | `01443ea0e1d670da65b52be8dc24429823e780ac49ebcb678d6a3fb5538bccba` | 0 |
| sticker-creator/src/elements/CopyText.tsx | 955 | `d91270ed056a6d01f857594931b85dd2d4ecfb559a69f59173f0256b57454c62` | 0 |
| sticker-creator/src/elements/DropZone.tsx | 1911 | `aa2119e3662ddb90c26fed61084504829d5fbe6ed171ce4879d7b4bd236e17d3` | 0 |
| sticker-creator/src/elements/LabeledCheckbox.tsx | 1211 | `cd35e3b149507675c1d438146c3e5ba2d796e32dbfd5fe9f5d706fa6a32d32e3` | 0 |
| sticker-creator/src/elements/LabeledInput.tsx | 992 | `15c9a6489fb838c80d558d644cc66558e36efe21250484ad39536669acffb15d` | 0 |
| sticker-creator/src/elements/MessageBubble.tsx | 599 | `89ec0c72ff60b50e91ccc64b255e75d4481374f517cabd1f17d4dc337900f380` | 0 |
| sticker-creator/src/elements/MessageMeta.tsx | 1949 | `e967225795031fb47eef6e578f7ab7c9bf3075af052e13c1282297f94e205ef4` | 0 |
| sticker-creator/src/elements/MessageSticker.tsx | 615 | `ea03cceac695b8f4d940ea9e1c5c93b5e25351e5e7bff2af808993fc00682f57` | 0 |
| sticker-creator/src/elements/PageHeader.tsx | 935 | `c617bc0d5f8919eec86c9ea2a0fbcdc8a0a40c6f9676e6a80665daa2b003b7a4` | 0 |
| sticker-creator/src/elements/ProgressBar.tsx | 660 | `69f52d4b141b8fcf1f2f840d137aeada133570abd75e11ce1282f67cb0753c2e` | 0 |
| sticker-creator/src/elements/Spinner.tsx | 513 | `58bc7f7d191429a32389b4fa98bd6d5cd02a1ce32d43ff017d06d16a6927fcb4` | 0 |
| sticker-creator/src/elements/StickerPreview.tsx | 2070 | `1f6659a1c7ef6349a0ee4e7e5420c087543909877371526431fe05d43558b863` | 0 |
| sticker-creator/src/elements/Toast.tsx | 568 | `fc2ef6544df273ccc73edb09a47f2c844dd8cdc34fa2666c420bde52dfce33a4` | 0 |
| sticker-creator/src/elements/Typography.tsx | 1558 | `adc85575de004ed3525fcbe8a06f601f83a1b59355182a52aea03405bea0e2e7` | 0 |
| sticker-creator/src/elements/icons/AddEmoji.tsx | 900 | `fcca80297eb9741c30dce067cd4fd6c3d59a5f79c488b50fa159f5d55abe5dbb` | 0 |
| sticker-creator/src/elements/icons/index.tsx | 122 | `a19f15744faf2bf8b7b27f2ff1ad41f4266c2480b1d884322ffa56305d16beb3` | 0 |
| sticker-creator/src/main.tsx | 892 | `ecdb1e9f77d446169437664f598f1759c22427b4710ee6ec2db1e3315c9ead16` | 0 |
| sticker-creator/src/routes/Root.tsx | 584 | `f9d3cd8d6875fa600078168fda92071dd9e38430667aaf1303396526520a8d2f` | 0 |
| sticker-creator/src/routes/art/AppStage.tsx | 3128 | `27dd2c34eb4257cc6460b0283eb566ee1d7513811ce8d409192a4f552129dc94` | 0 |
| sticker-creator/src/routes/art/DropStage.tsx | 1365 | `83d0762aac9aadee52a4e93f53bc0e517a6bef27c9ac9b47ecc1bfc4b6d2aa7b` | 0 |
| sticker-creator/src/routes/art/EmojiStage.tsx | 1007 | `684b3df1f3408628ab6484d9238483f6553f88c5607484a5447caf6d394c6893` | 0 |
| sticker-creator/src/routes/art/MetaStage.tsx | 4614 | `e4c191ba1715b81c6272e2d0ffb635cc8d11f19a3b40902421de7b7ddc7cd37c` | 0 |
| sticker-creator/src/routes/art/ShareStage.tsx | 3260 | `ab80e09e087ba608e8607ebce79087b9653337a6640c5331637260f4d0f72933` | 0 |
| sticker-creator/src/routes/art/UploadStage.tsx | 3630 | `39419e08780bd549188b637c4388902e3641a152b7efe03e46560af0700ba41a` | 0 |
| sticker-creator/src/routes/art.tsx | 1731 | `cbca45b81eb3a80b52952f451086d0518fda16a543ac8ab72dc1772171f2003f` | 0 |
| sticker-creator/src/selectors/art.ts | 3197 | `42704c151a4553164a4c96278669509c92a4bcfcd37b779233956f024369915f` | 0 |
| sticker-creator/src/slices/art.ts | 5512 | `7c05bd572aff813c1df5d3935bec64f57bbe1c1f7e55e4fca43f363c028aba58` | 0 |
| sticker-creator/src/slices/credentials.ts | 700 | `ae4bcb6498f8d31567a763664e4750b5b63231be558626f4badd36e80872aaaa` | 0 |
| sticker-creator/src/store.ts | 642 | `64b3b36e0415044118b1e61c036dde52405b7e61991f1d661864849735c5d623` | 0 |
| sticker-creator/src/types.d.ts | 1805 | `abe1ecf07ca472c14def10629dbe55c742eb8671499e530d8def062bef519899` | 0 |
| sticker-creator/src/util/api.ts | 1516 | `d50ca4350881d098aed12fe7f47d90123010a1dc072c39bc91f6d5742e720204` | 0 |
| sticker-creator/src/util/apng.ts | 2705 | `619543b03f2062ed5b7c5c330c543449a7308471ad4025b9fa03e7151588962d` | 0 |
| sticker-creator/src/util/assert.ts | 220 | `ff5b18eaac0014a5223609a254d3fb889b2b2c1af87911d8fd439d9be5a83c8b` | 0 |
| sticker-creator/src/util/crypto.ts | 4652 | `fb5930ebbd3d8d5f1eb53daef3d0f4c9dd7e1b21e95e7b150c5e00052060aea2` | 0 |
| sticker-creator/src/util/i18n.ts | 3306 | `1fb9b6560a64a49b98258f137badd02a2394571f2345c28080cba59c213af32f` | 0 |
| sticker-creator/src/util/loadImage.ts | 507 | `e5e684d84e7e318065fe3dc6d347ad56d62eb1c29411ed113f25c25c7d7aa647` | 0 |
| sticker-creator/src/util/noop.ts | 180 | `f3f2f3809f57666e31c962178875e4830a7abedcfa7aeb07bc17107357c8db84` | 0 |
| sticker-creator/src/util/processImage.ts | 4197 | `87e15dd6b577e32d039ff9768daa8b6a813d4110495cb5965efa4845a1f5d86f` | 0 |
| sticker-creator/src/util/protos.d.ts | 1289 | `26dd0d89d013515fd45783816d52d5a36944773a1671273e1db83059c6fde63d` | 0 |
| sticker-creator/src/util/protos.js | 2547 | `93fb8aec0bbdb9bfa22c764a1ad1f7a43c35637ae3fe514cb7932b13e8dc74ae` | 0 |
| sticker-creator/src/util/useStickerDropzone.ts | 539 | `76d02e9e7ff84e1e0bafd1b651d52421ca24e0c62e8b578e73fcb48881aa09a6` | 0 |
| sticker-creator/src/vite-env.d.ts | 121 | `d27e72174ebf9d7d8cc577217f5df3f2d14ea3e29273e45e8fa41c0f133e7e32` | 0 |
| sticker-creator/vite.config.ts | 660 | `9e19a4c8857434f617f8d2d55c39a844748c3587d2bd950b3f03c247b177b81b` | 0 |
| ts/AttachmentCrypto.node.ts | 21237 | `9f65def315dba51705b6ea80949b18140bbd0b28a1088a2a32880a803075ecc1` | 0 |
| ts/Bytes.std.ts | 2145 | `1fb17908453f6fb3a9309404b416a9799614479e73a22c231c40a72d1732f1cd` | 0 |
| ts/CI/benchmarkConversationOpen.preload.ts | 6986 | `4ac3b8b277acca3dd6bbca461fc312d074649891d6b6fe2ad68b49f134ecaddc` | 0 |
| ts/CI.preload.ts | 11203 | `e53525c96265117a91b2454a7a43e8f077bd6b9dc68ced89561f4f405b9cfb14` | 0 |
| ts/ConversationController.preload.ts | 64507 | `e72d4053f04db4d6adc125eb6feb3e61d4bc3402b478c7e2264b0b3a0400088c` | 0 |
| ts/Crypto.node.ts | 21480 | `14b53187ca5903557a630dc7eed9ca82882b5eec18c6881542d921ab37c89725` | 0 |
| ts/Curve.node.ts | 3685 | `bd8276dd2ae5321a3603356895a75fea2a0d4f9da5e9d32278757131b91aeefd` | 0 |
| ts/IdleDetector.preload.ts | 1526 | `f95950bb7eaa4946a517f331749947891d835518a420c93061cfcbd8ee16c2c2` | 0 |
| ts/LibSignalStores.node.ts | 10642 | `dbe1eae16b7bae7ae17c42dbc3854e4b7cc57565e16888dca749a3a13c4c5377` | 0 |
| ts/LibsignalNetRemoteConfig.preload.ts | 2196 | `8d721d202f5604657d1f37abef8edfbbdc051090cf1b13d5b4492d1bc929f26e` | 0 |
| ts/MessageSeenStatus.std.ts | 834 | `d7a90115d19ce06556c6ed2885f30e03984af44bd09c06bb6fb96c9772810d5b` | 0 |
| ts/RemoteConfig.dom.ts | 14567 | `42650f181635ad6dedec86b030274dfdae7c920f7600bb5740edef299b1e080c` | 0 |
| ts/SignalProtocolStore.preload.ts | 83667 | `f5a9321e92dc05c05942aa11a0db3486caecfe1360b73c3646747a5eef1e7bb9` | 0 |
| ts/Timers.preload.ts | 506 | `30d0ab1886cd8373f7bbfa690fbabb1d5a3c6517de190d777f66344fbdd465f8` | 0 |
| ts/axo/AriaClickable.dom.tsx | 10675 | `f94f47a7b0b01c9f523f3c1724a9152a162b77aef8aff7c884ed6f28319534bd` | 0 |
| ts/axo/AxoAlertDialog.dom.tsx | 14411 | `738fb83347c3f9ebb86f41d2064cd24e4019b2e9ba89251d41040113244102ab` | 0 |
| ts/axo/AxoAvatar.dom.tsx | 19383 | `f4f80452bfdb1517b62c8720fd02b865ee881f5b3203f1219c9920ccf17fd2fd` | 0 |
| ts/axo/AxoBadge.dom.tsx | 5310 | `7f16561cd5b84ce0af10d6c23d3e72dda90862bbf9fb66fa4cdfe6a18c4b7dc5` | 0 |
| ts/axo/AxoButton.dom.tsx | 10623 | `2c66ebb4ae63c7bbf49de7fdddc9689d8232f2b1ea6d0af2948dd6660cc60f00` | 0 |
| ts/axo/AxoCheckbox.dom.tsx | 3938 | `f4fd651f5a3e1388fa560aa7ccdd8a010a00f1d10520f4e9243b1f9ca68c436a` | 0 |
| ts/axo/AxoConfirmDialog.dom.tsx | 3579 | `957f7eb0c1d7abb4bfa2868cbf3c4f106ba9b597ea4d1860aafbd9c4bd6d2d4a` | 0 |
| ts/axo/AxoContactName.dom.tsx | 1331 | `b1f9a65fb3fabe294dc8be341aa9d08b5d6138f1576dfff9060ca6cdb81223e4` | 0 |
| ts/axo/AxoContainer.dom.tsx | 835 | `63ce9ba8110de9070c301d7e10a13aa2730935ace6cf003c98a27f3cf727aad4` | 0 |
| ts/axo/AxoContextMenu.dom.tsx | 17955 | `794ffe2e6277a2d11827bfaed39158dd3a85203baa8d320578e3a03f46b92826` | 0 |
| ts/axo/AxoDialog.dom.tsx | 26966 | `ec21aad6fce31cd5fa6fd92f102dbe4993c990c9c9857528e0c70a801c10d825` | 0 |
| ts/axo/AxoDragRegion.dom.tsx | 2658 | `6f6eabc314a629f099d88d6cdd86cd7b343657e2b968105217bd6272793f5918` | 0 |
| ts/axo/AxoDropdownMenu.dom.tsx | 19267 | `4b4828f8bf202958d80bb8d2cf3738c0ee7c75d77af9d7eff7c109b555911bf6` | 0 |
| ts/axo/AxoIconButton.dom.tsx | 12101 | `f3472a49cfe6db7cfa7460b308c6f4da0f9e4fcce9cfc81757fe031a05ed8630` | 0 |
| ts/axo/AxoMediaButton.dom.tsx | 3662 | `07151c5c3d67c11ad9b138f8f7457fe1d541389940a6116c23790473c63cbe53` | 0 |
| ts/axo/AxoMenuBuilder.dom.tsx | 12081 | `16ba030501c00d0b4c0463bd9a9f3467b1b5e19f7208286a01b24510401a05fa` | 0 |
| ts/axo/AxoPanel.dom.tsx | 3460 | `0375cb9d348f14d29b2073f39c9c7237a9d580c70d626f22e05124d79afeb3bf` | 0 |
| ts/axo/AxoProvider.dom.tsx | 1545 | `a9eff0a009b7d660781ec25c920aa1f107b94c267afb895c57eca9853693fc56` | 0 |
| ts/axo/AxoScrollArea.dom.tsx | 18598 | `1f1cda89417aa0c2a3136266460846a992e13a2e6657011701b7261963094e24` | 0 |
| ts/axo/AxoSegmentedControl.dom.tsx | 6316 | `094808288a66ab812a5ffa64bf7a27fce6d994f284a182790b355d5f51fe74b8` | 0 |
| ts/axo/AxoSelect.dom.tsx | 17325 | `7d414756b839ae9452f4b366b877b378e664f2501ffed62742720315014fb369` | 0 |
| ts/axo/AxoStackedButton.dom.tsx | 6353 | `74dc3ff942cc62a235506500c66ff44b73195c67d72e822472266800ef97d75a` | 0 |
| ts/axo/AxoSwitch.dom.tsx | 5163 | `08946ab6bada6c0af3e48f1abf4085508a06f7b4d2885a8de503af764335416d` | 0 |
| ts/axo/AxoSymbol.dom.tsx | 4591 | `04593f988d4290e15426ccbb32f5a6d3082b18ae88171837a2647ee563d69edf` | 0 |
| ts/axo/AxoTabs.dom.tsx | 3048 | `52bb847d1a69cca48f4a2bd0df2207923608c564df661fec031bc49c8fc54368` | 0 |
| ts/axo/AxoTheme.dom.tsx | 3430 | `693a5b68ac9063c44e9b85a3b3abb4326b58f8636a069cdd19d32cdccfe22132` | 0 |
| ts/axo/AxoTokens.std.ts | 13713 | `fc42a1a1cbc889c8fecf6f888306d1a304e5c8923916fef8fb3c8160b6001b82` | 0 |
| ts/axo/AxoTooltip.dom.tsx | 17957 | `dd2e2d3fea01ecb7da9b066b4063051994827430027ba620c848b59ef6d7f8ba` | 0 |
| ts/axo/_internal/AxoBaseDialog.dom.tsx | 4054 | `f6698f1050e5c04529c783d4026b730efef7eee44c7a094357e35728a1d6dda3` | 0 |
| ts/axo/_internal/AxoBaseMenu.dom.tsx | 14119 | `db90fde1ad8c5e8e9e255ed269fe397cdcbd6a10910ec40701e1e271d8ebc51a` | 0 |
| ts/axo/_internal/AxoBaseSegmentedControl.dom.tsx | 8323 | `ee90b612a7dc492bb5919ee0f90c5b57a1adde0428ab494a790351946c2f8186` | 0 |
| ts/axo/_internal/AxoIntl.dom.tsx | 4180 | `c314c7fca388a36670c152a9c1030dccd54762e4b2cb6d1cf21c7057f7dfee71` | 0 |
| ts/axo/_internal/AxoMath.dom.tsx | 934 | `47d1b6ae699f10f87f72d47095177f9c925c9935543f4deb10169766fdb0de1e` | 0 |
| ts/axo/_internal/AxoSymbolDefs.generated.std.ts | 40865 | `f9f0022dda4ab504b9858a54becf29ae292659b77bba39fe7091e28596073268` | 0 |
| ts/axo/_internal/FlexWrapDetector.dom.tsx | 1890 | `2a3c50c96f18ed997801d570c9ab6c9ba5b408a263de83d0ebdf8cf622b922bb` | 0 |
| ts/axo/_internal/StrictContext.dom.tsx | 1586 | `f65c74fdb76db177abbf0906cadb2ba4474766f7d7421695b1554912619cd3be` | 0 |
| ts/axo/_internal/ariaRoles.dom.tsx | 5317 | `1387ed58f43111d4b49f8dda2d7dbb11978cdd29efa20dbb956f82bbd2e7fee8` | 0 |
| ts/axo/_internal/assert.std.tsx | 2842 | `6543b7d95907c90186e56279f00d27a8356b04c4b9c5c82db29823b8aab5290b` | 0 |
| ts/axo/_internal/css.dom.tsx | 790 | `0dc404fead3cc029df4f33225576cb23292e6c0f6c178ab7a62b3d0e50ed98f6` | 0 |
| ts/axo/_internal/props.dom.tsx | 265 | `bfc7fe423c77e0aed54762badf72abe8205a86d3bc07d5d54f692bb37ecfcef6` | 0 |
| ts/axo/_internal/scrollbars.dom.tsx | 5512 | `7c62a571e89b7e2bfaf05b367a239492bf420caa53afecbd181e8351972deee5` | 0 |
| ts/axo/_internal/utf8.std.ts | 5030 | `04eeb83b8cef418ae25a2b0d9adc17ce845b7bee1e81600f573c878de08f18e6` | 0 |
| ts/axo/_internal/variants.dom.tsx | 1183 | `410423c30e78f98bb8f84afcaba04043f61a26b167c22cd4b2dd75d196d5444a` | 0 |
| ts/axo/_storybook-helpers/Story.dom.tsx | 2378 | `490c966e46808c1e87598becdfd2b64262a0b63fe5c518da085e8defbab153ae` | 0 |
| ts/axo/aria/AriaLabelled.dom.tsx | 4279 | `7feda19ba880ffe3729408941ede38c862ed021daa70362d985dacb46c4adaeb` | 0 |
| ts/axo/aria/AriaList.dom.tsx | 1997 | `ab80e9a1505e4eb9ace552d55a3b86e35fb44201cf78b64316c70cb7cb291207` | 0 |
| ts/axo/chat/AxoChatDateSection.dom.tsx | 2140 | `100a983a8684f8ef5ce5ba51dc524f6c8a66417d436fad2e43d8379e82514505` | 0 |
| ts/axo/chat/AxoChatEvent.dom.tsx | 6746 | `f021a5483950277142ad8786b39f8e36f907ebfde11ad753850be11606725fa3` | 0 |
| ts/axo/chat/AxoChatUnreadHeader.dom.tsx | 1173 | `0f8f3d27d4edf9fc98e6b68af2314cd3aa9f4790ae919a280e746ac8356042f5` | 0 |
| ts/axo/controls/AxoRadioGroup.dom.tsx | 4753 | `264d36e5edc3c4b5c5ff055641dab0d3c973573fb27021d77fc0fd5776b277d1` | 0 |
| ts/axo/controls/_AxoBaseRadioGroup.dom.tsx | 3221 | `fd309b595469f0b879c033fa2b67fcfe075df0463b2bd1021e19e2f48a9102da` | 0 |
| ts/axo/emoji.std.ts | 25914 | `5836be174170f9c9a9b57ce2d34c25bdc19086fa44481e6f35312cc40d224ecc` | 0 |
| ts/axo/fields/AxoFieldGroup.dom.tsx | 1461 | `d64a77d77675c4b985bdb6069ff491ec02922b653ca6548c6bbf56e39e5fca15` | 0 |
| ts/axo/fields/AxoPasswordField.dom.tsx | 3884 | `2941a2e092572b6ff9b39cb5f3fff0143cff98a07acc05edb0d2861c6711a5b8` | 0 |
| ts/axo/fields/AxoSearchField.dom.tsx | 3089 | `edc5458593312e5d5f69a55cf1f19d0ba0e966030ea03d1396efedc9a2fa6445` | 0 |
| ts/axo/fields/AxoTextField.dom.tsx | 8365 | `3b80eee4c357834f27db2e6cbec11e90a97393474d780ae010aef0f4c80fd2be` | 0 |
| ts/axo/fields/_AxoBaseField.dom.tsx | 26137 | `d8bc90c5997be88312902498ec4baf0b5abe80fc3984b0ea86ede8bbe6a2301a` | 0 |
| ts/axo/items/AxoClickableItem.dom.tsx | 2289 | `d1375b03d3fa9e79493fbb69f26faed04ffc3ebb77b6dae9b221d03aa981163a` | 0 |
| ts/axo/items/AxoContactList.dom.tsx | 6579 | `4c8a3cc61295c10053f64cef766a54b2e4470fe5911869a67a5247c5c5a5ca16` | 0 |
| ts/axo/items/AxoFieldList.dom.tsx | 1898 | `fa4df23ae23d465ad0944545b1defd9f697a13f94767773fa07b2954477978c6` | 0 |
| ts/axo/items/AxoItem.dom.tsx | 9801 | `6d3a7742a9dcc678abd66ce116450b73032ccafaaaf38e4d371246279accbc2a` | 0 |
| ts/axo/items/AxoList.dom.tsx | 4258 | `ff43cc0eb0975feb580acb5270ec41b3ba6672ff544d97fb58fdbfbc647eb9aa` | 0 |
| ts/axo/items/AxoRadioGroupList.dom.tsx | 3559 | `b681dc09661dc2573715ed6271e77646f0e1666020e505b6f6474f890a8835ac` | 0 |
| ts/axo/items/AxoSelectItem.dom.tsx | 2654 | `7b2b13bd0d995932fadb4ded2a6aabb282f0e66824bc32a4815db24f62c9f496` | 0 |
| ts/axo/items/AxoSwitchItem.dom.tsx | 2265 | `46f746f03636d85247d4e677dfabbc2b9425d6373646573b688fc2add1636465` | 0 |
| ts/axo/items/AxoTextItem.dom.tsx | 1442 | `74504e8a30b77c58169a4484478afe0336a081548138d1a788cf92efd3b2ebc6` | 0 |
| ts/axo/items/_AxoBaseItem.dom.tsx | 15450 | `82a6be80fd39f1aef71d7e133ec7f6b4e1d009e50dfcd95d927dfcd5a4986b29` | 0 |
| ts/axo/message/AxoExpireTimer.dom.tsx | 4409 | `16915711e110e768b8c3eeb7801f5921ef9b69f5e214da7ed368ce5431289573` | 0 |
| ts/axo/message/AxoMessage.dom.tsx | 9157 | `358d174a86e8b2426a5aada9a06803106a3acda8cba0789f20edf6bda02c6638` | 0 |
| ts/axo/status/AxoLoadingIndicator.dom.tsx | 1145 | `535242afb4749f67dfe082ee8a4ba2ff458c21496f502aba33eb1ee5abd3c893` | 0 |
| ts/axo/status/AxoProgressIndicator.dom.tsx | 1511 | `af8daabc345536b13dd23a581827baec3bf33461867405288b822bd888840214` | 0 |
| ts/axo/status/_AxoBaseSpinner.dom.tsx | 4569 | `3f76276be003d61c8f48556d08e62cf3af063ced846618efae0857d8166e75d9` | 0 |
| ts/axo/timers.dom.tsx | 1615 | `cad97c843ba05a9d9de680f1aa43f5087aafaad05602e46dcd848c9cf624e9a2` | 0 |
| ts/axo/tw.dom.tsx | 735 | `8308fd5ae82a7b0db4c1273b0af329db5ec5d66e23f07852fcb690a9256ccf4f` | 0 |
| ts/background.preload.ts | 135047 | `93b4423f948ff096460e9ac5f93dbbbc80f587e75b3e9e8e10beb0f99a357413` | 0 |
| ts/badges/BadgeCategory.std.ts | 369 | `b62ff8ab77cfac7c731fa9e2e578d836538ee4183092cbc495e145a4cf64804f` | 0 |
| ts/badges/BadgeImageTheme.std.ts | 342 | `e62d15236770af67fc64866c2d98d3e7ec0043721ed7eba0c0f31aa6a176ef81` | 0 |
| ts/badges/badgeImageFileDownloader.preload.ts | 3404 | `e19c5b2baac2eecad5efac689d05a18a5227b9ce2c68d50337e5d4de657725a8` | 0 |
| ts/badges/getBadgeImageFileLocalPath.std.ts | 968 | `920080d77b929c89f2082f065ac04a8327488881bb73a7ecfc89c26d30f4a869` | 0 |
| ts/badges/isBadgeImageFileUrlValid.std.ts | 370 | `8d7d21671109f7b1d218c5e0a1395026acfaea4c760f0aa08a9785123684b680` | 0 |
| ts/badges/isBadgeVisible.std.ts | 253 | `0c4ff3ee32502b8a9da8a500a5e72f169b8327c95ca3bc0973658e53a6e8dcf6` | 0 |
| ts/badges/parseBadgesFromServer.std.ts | 4649 | `f69ea58891c5ff6ea4b2b82864fa08715ee7b055986b600a1d5f381ba5f2a6a2` | 0 |
| ts/badges/types.std.ts | 721 | `f85607134c90a9829b69184229c3e576ed73e5ecaa293eafaad74e091b020f19` | 0 |
| ts/calling/VideoSupport.preload.ts | 17193 | `d6f1c968484b97a4009334077c1468baca599947781731c521e3b85e4600f718` | 0 |
| ts/calling/constants.std.ts | 1021 | `848c72d8fc7f4ddeb637890207cc095f7f7d2ce8ddf92a62b09c944fa8f11f23` | 0 |
| ts/calling/findBestMatchingDevice.std.ts | 1846 | `901c813bc82cdde03774c092003b573d3f2cb9e0623521a36198788d0ee5094b` | 0 |
| ts/calling/truncateAudioLevel.std.ts | 642 | `0d8c5e89075ee47f7ad0b54584a2d33cee16baf7928ea3fa67a3937ffb5e88b5` | 0 |
| ts/calling/useGetCallingFrameBuffer.std.ts | 831 | `7bb1b31730b9875c957b4ec754ef8a783e251fd5ba7c1c3fca1cf62053f08e79` | 0 |
| ts/challenge.dom.ts | 13597 | `312332194ed6b31ca31027cdfbe0eeeab6983707c489373539f0f8e33661c1e1` | 0 |
| ts/changedpi.d.ts | 243 | `49d521d8d3fbde81dadd388917211a155bfc4a9a1280e3f150bc3a9f8cd45950` | 0 |
| ts/components/About.dom.tsx | 1805 | `c7bef8fd309f40b48e7b56d7b23082b608d79af7f3f8fe137ae42f3a9193eb4a` | 0 |
| ts/components/AddGroupMemberErrorDialog.dom.tsx | 1432 | `27da77cbc485f6b9c840df3fcf9f4ccd2adc1a9ecd303bf744dd24aef73d5c9b` | 0 |
| ts/components/AddUserToAnotherGroupModal.dom.tsx | 7889 | `09877ff5f9235c6371c45e483797bf13925cab115b5fd7e1457d63ff55b30dd6` | 0 |
| ts/components/AnimatedEmojiGalore.dom.tsx | 2067 | `0802b09c17d85fec76f40afcc2240ea71655c6dec85c14a4321da5e4ec7bd224` | 0 |
| ts/components/AnnouncementsOnlyGroupBanner.dom.tsx | 2102 | `665b333b182dc16c18887342dad6829ee9ce39d64547e3d65bb733024598144a` | 0 |
| ts/components/AnnouncementsOnlyGroupBannerAdminsDialog.dom.tsx | 4170 | `e8a3493d757b98559ad9471d46d23208ad7d18bdfe17282ad9b36923cf9acbd3` | 0 |
| ts/components/App.dom.tsx | 3771 | `4d07dcb67ad6f81a4ba77144c78ca0fd11bac36c6a9c6fa559204d7552a2bca0` | 0 |
| ts/components/AutoSizeTextArea.dom.tsx | 2005 | `273f3f1c6cf06921a5d74cf78f4ac72f2e49f94719d561ec689c0aa23a0fb29c` | 0 |
| ts/components/Avatar.dom.tsx | 10328 | `7986667d354281493dbf17402200d85bf95e6f5dc3ca9d403aada9053eb58dbb` | 0 |
| ts/components/AvatarColorPicker.dom.tsx | 1127 | `6535e62d4224c9d0c41250f74019aae8228c7243bf4be2ae3483cad85e495093` | 0 |
| ts/components/AvatarEditor.dom.tsx | 11488 | `0c7b20d0526382781ad7bda996bf49688384eee926bc30176d8d027583ddec43` | 0 |
| ts/components/AvatarIconEditor.dom.tsx | 2612 | `27c63ca67fdbf45aca8ab2417414fe750c3ad7ce453e66e0adea71ce86c24877` | 0 |
| ts/components/AvatarLightbox.dom.tsx | 1792 | `1c4e2cf8dbf4b38c5d61d782bbe27b5badd390288eb2a53c9545812408632f11` | 0 |
| ts/components/AvatarModalButtons.dom.tsx | 2898 | `055766850c41b3269fd026ff9d90f68928c085580ca663287e7808decc5b8114` | 0 |
| ts/components/AvatarPreview.dom.tsx | 7357 | `39fdf37ebc84d39deaba4c32e7fcc59c79b59ab0d124ca9c13130ccc19f5f3c8` | 0 |
| ts/components/AvatarSpacer.dom.tsx | 343 | `b15c0d2757210bc5c7e3024749b9b544ad937ccf678a91f90167fc4905ac4096` | 0 |
| ts/components/AvatarTextEditor.dom.tsx | 5732 | `3ecbbc9b4c1ad4dfec6db0fff9f3709492db37551ff52600cbd14eadd1138182` | 0 |
| ts/components/AvatarUploadButton.dom.tsx | 2251 | `9c16101cfac45fc773e1189a51437ee950e1425d06c15a955047dfc8d0b51e0c` | 0 |
| ts/components/BackfillFailureModal.dom.tsx | 1165 | `0a5ac64092c349f620653d43b1032b148e43ea48ca8a00a7fee931bc0edb4d86` | 0 |
| ts/components/BackupMediaDownloadCancelConfirmationDialog.dom.tsx | 1598 | `6d6fc291347051df91ee428dfbd3f5c054748dc5fc3dc7cbd6cbfbf9e5f1081b` | 0 |
| ts/components/BackupMediaDownloadProgress.dom.tsx | 6941 | `6351df69a390f06530459f46c7886e9456951e0e9360ebbb2ebbd0a034c21341` | 0 |
| ts/components/BackupMediaDownloadProgressSettings.dom.tsx | 3593 | `e315bd91fb3530fc6676f1e1f72ed50c043d1c7b97ec01415be2e153b2d9b680` | 0 |
| ts/components/BadgeCarouselIndex.dom.tsx | 957 | `64fa1ebea99e231cd8c8151e684a88e9668fb2cc0dfe6ca2eda5e93f43633353` | 0 |
| ts/components/BadgeDescription.dom.tsx | 905 | `144b3da4a54b3dbf0b3ed808010ae2faab88b1449996e0364e48538028e7b29c` | 0 |
| ts/components/BadgeDialog.dom.tsx | 5020 | `f12dc30f7b3ffef1eedef1579ee36d9c7a672c54e96fb1a515b1c3d1613c11ae` | 0 |
| ts/components/BadgeImage.dom.tsx | 894 | `485d9c5ce817440ac9cf745b53bd8a5212c14894d151725115f93865b7b722e3` | 0 |
| ts/components/BetterAvatar.dom.tsx | 3201 | `88195df4e35829c86f817b7558167c440034a7ba2dddab3d266c7d0b026a9575` | 0 |
| ts/components/BetterAvatarBubble.dom.tsx | 1647 | `5b82d96515c2cc4af2516ecad3cceaa81ba7bfadc04c72e4a8bf6e680f91d8b8` | 0 |
| ts/components/BrandedQRCode.dom.tsx | 4663 | `6ccf9d1f356a0a18344434ab43f9194de4d4e91f3637091cfb8185c4787f2ba6` | 0 |
| ts/components/Button.dom.tsx | 4054 | `c91d79de55e23f8de2981798b73b9b6597ec311a1b3998ea0de0ce0f23af6f48` | 0 |
| ts/components/CallBackgroundBlur.dom.tsx | 884 | `59d3bae723687425675d57fac0ef92164a78c846ccdb827554470257ca581a97` | 0 |
| ts/components/CallDiagnosticWindow.dom.tsx | 1928 | `e21e653f690f650a0d23f157f8214a0db4d866d62860f6be0cbf6a992542fad2` | 0 |
| ts/components/CallLinkAddNameModal.dom.tsx | 3979 | `52361bdc1fc77beed1968499a617ad2c92bc65af906e1757fa8a2b97bb074a7c` | 0 |
| ts/components/CallLinkDetails.dom.tsx | 8186 | `056507700a1df7b1aea5e5f5cde03defef268a7a63e4f266e84bd7eac0f9cc5c` | 0 |
| ts/components/CallLinkEditModal.dom.tsx | 6763 | `0e2e99991ebbd0dbc1a28abdf431c8f74aee69abcaef28ba3898160608b03bac` | 0 |
| ts/components/CallLinkPendingParticipantModal.dom.tsx | 5350 | `ed49b23de2dfef64f0607bd1b45dc620de4f1146032ed18d421c2c9de3305215` | 0 |
| ts/components/CallManager.dom.tsx | 24846 | `8f7f580328de9f7bca7ed349db548e14f744789fff3e7e75f547020bfcddc76d` | 0 |
| ts/components/CallNeedPermissionScreen.dom.tsx | 2336 | `0f928e6cafaa1e386a43f2e1a8dbd7f0ba8fe2adc3ac3f652eea2218e39f5027` | 0 |
| ts/components/CallParticipantCount.dom.tsx | 1924 | `1e8360e7b16362f95f754f01f4026b5cbbafaa04ba08549ea80471aef1307f64` | 0 |
| ts/components/CallQualitySurveyDialog.dom.tsx | 19266 | `520151c964aebe3b5bf2510a77da3fc29a93ce515f9ae33592a669f63dca1b53` | 0 |
| ts/components/CallReactionBurst.dom.tsx | 4563 | `0795751c0cff5358688314a2388db8a0e4eb8c4fd977cd82dd7fc70a6c0101bb` | 0 |
| ts/components/CallReactionBurstEmoji.dom.tsx | 4362 | `4598eb9dfb38813991eaea061c7615b0d192bdee2796d885a66f04534ab13eeb` | 0 |
| ts/components/CallScreen.dom.tsx | 50740 | `580cc92fe962901664f55876b23d29a92e00f4959c736fe3c558af56a1a1a60b` | 0 |
| ts/components/CallingAdhocCallInfo.dom.tsx | 8420 | `0fefd88ed7d0597d5fac27eda6e6120c5446697d471097fc5d3d0f1b0d1c4a76` | 0 |
| ts/components/CallingAudioIndicator.dom.tsx | 3893 | `329a76ee2c3bd167b67a382726a82f4b27ddbe3ba76f8f17bcad6481f4ccf947` | 0 |
| ts/components/CallingButton.dom.tsx | 6865 | `def68cb1d300f78f4e7a99cfbf77090a15b038f136421a302f68b87dae110086` | 0 |
| ts/components/CallingDeviceSelection.dom.tsx | 5315 | `0fade252aac73aea7275af5bd7f70cc3f0fa3a85d407225891baf9d9341b9e2c` | 0 |
| ts/components/CallingHeader.dom.tsx | 4096 | `94d80637093b3695fde1429f03a17c2ccb7b1191a4d809d478e61bd4fddd3f88` | 0 |
| ts/components/CallingLobby.dom.tsx | 13269 | `086ded7b90891e64264852e893f7545deac65f98099a72e022f9e55559252858` | 0 |
| ts/components/CallingLobbyJoinButton.dom.tsx | 3789 | `ef73ffc2a56ce73904b85f9c0dbbd8380955e96874bc1a93c4b4c63b036787a9` | 0 |
| ts/components/CallingParticipantListItem.dom.tsx | 5580 | `be49aec66278088b6cfd41cd6011850b5a43779cd149abf5d13264cf4f92aba2` | 0 |
| ts/components/CallingParticipantMenu.dom.tsx | 4377 | `b339673871a84f044a73efa6db03edf489650eddfa117e8018eddb2dfeb8b0e9` | 0 |
| ts/components/CallingParticipantsList.dom.tsx | 3540 | `d5c31b0edbac1cf9a90a0acc7743bf4d252a26823f964c58009e37e6bd408328` | 0 |
| ts/components/CallingPendingParticipants.dom.tsx | 14141 | `c594afe3b516fd1df4947bd57de72019e13644596059e4ecde5366e49fbad306` | 0 |
| ts/components/CallingPip.dom.tsx | 21966 | `7da15ce3ad6bc9a67f78e61e400a804c042621cc7aee44f4b75a1e5c0e49508d` | 0 |
| ts/components/CallingPipRemoteVideo.dom.tsx | 8951 | `7285a4b8f20fcf920c2d5f13867c8e283e4a76078390ca17eb5d8010ad88681f` | 0 |
| ts/components/CallingPreCallInfo.dom.tsx | 9026 | `710db0078bce29485aa0f585db79d3b98b80dda53d516fd49d580625c7bbd8cc` | 0 |
| ts/components/CallingRaisedHandsList.dom.tsx | 10009 | `bb7c7ac1774f635fe927d8e67d2a350ff7045a1936790af207eb64893848e1b9` | 0 |
| ts/components/CallingScreenSharingController.dom.tsx | 1940 | `b12d75f40055f5d05e3c6260c57147a3352fe4fd99e0005342675668f4f87a28` | 0 |
| ts/components/CallingSelectPresentingSourcesModal.dom.tsx | 8480 | `121b1735bad87a3eba846364874ca2552f548f5ebf083d5f8f84364b3ccda13c` | 0 |
| ts/components/CallingStatusIndicatorHandRaised.dom.tsx | 1133 | `ba27626bea30ec2aeced03283ae05ee29986eb1d34f7cf3a3bad32644872230c` | 0 |
| ts/components/CallingToast.dom.tsx | 12309 | `a35c5e0a5d7d1d08107f5ada88eafc2a11e3f262676e6681f6cb2a70dbc6ba95` | 0 |
| ts/components/CallingToastManager.dom.tsx | 14653 | `06f306d946cfe444b253a9d99454d1d203cd187513838dfdf3e43617a9215276` | 0 |
| ts/components/CallsList.dom.tsx | 34263 | `7735797107dc349ad2cd1f7f5fe03c898f74d3b4c4f6d23c2c6259d2689e46e2` | 0 |
| ts/components/CallsNewCallButton.dom.tsx | 9867 | `c572d0b7b1d6ae1d620c38d90a0ba22b90ebc827ab0109cfe587ba566df28c6f` | 0 |
| ts/components/CallsTab.dom.tsx | 13114 | `5a68788ec7d9b1bf3d29baa3ebd3649ce661e9ea5c677acf365491123c140dd8` | 0 |
| ts/components/CaptchaDialog.dom.tsx | 2149 | `fdadfe2acafda0ed85f6720ccddb016f8b1a9ec5ec0fabad5678f4713cb27104` | 0 |
| ts/components/ChatColorPicker.dom.tsx | 14002 | `d56bca68dd7ca845855d8e0f825825afd26ce41871d8cd283085e73dfac9586d` | 0 |
| ts/components/ChatsTab.dom.tsx | 2734 | `baade0ae7f91797f5179a7cf09b0aa69e3537e4aebf4125345008b65f9af6045` | 0 |
| ts/components/Checkbox.dom.tsx | 1787 | `668f79741c3d7397b26b08351caf19151c98db49cf7419fe71ed5a34f91dfb83` | 0 |
| ts/components/CircleCheckbox.dom.tsx | 1483 | `5252c5e188c86fce73a6634c261ceb3d8ebd48e5e2a4cab82421653f485f8ce7` | 0 |
| ts/components/ClearingData.dom.tsx | 2143 | `43a8b4cd1f6da6514ff6153b1fa1a8d5001d15b71c75f341f4240881360eabc6` | 0 |
| ts/components/CollidingAvatars.dom.tsx | 2151 | `b47b499c8d286f533c6bb3812a23b26cc45a05dbac3bf4ff589196c64b57309c` | 0 |
| ts/components/CompositionArea.dom.tsx | 42838 | `d505ab3e584be159aee118ae49e705beb5eaa4c2dbefd825b039e33b6b6a28f2` | 0 |
| ts/components/CompositionInput.dom.tsx | 35464 | `1e091ab9c5cee1a01d994a47e9f06d600f0d56e3d4e4cc2aa0980ad686e4d9e1` | 0 |
| ts/components/CompositionRecording.dom.tsx | 4742 | `5b7b9adacd71c8bc730e6e59a8dd1985e1e2b169f4bc4a34d6d67a486e5f0b14` | 0 |
| ts/components/CompositionRecordingDraft.dom.tsx | 4744 | `3b277addccd9bcd445b9b2ece1927c54e2ab9a4e0bef15b8522366fe0ba9cbba` | 0 |
| ts/components/CompositionTextArea.dom.tsx | 6746 | `b78ddd665245d40b1675a2d977abba220446a6e1edb3fed1cf6e01926f80f56c` | 0 |
| ts/components/CompositionUpload.dom.tsx | 1912 | `82671048cecb1221fc3cfcf6c9ef2c5f2ba008870c38da241454b953a4796b7e` | 0 |
| ts/components/ConfirmDiscardDialog.dom.tsx | 1128 | `c60f15c9ca86bbed42aec2496aa29ae18b517dc0630df4d15c33dcc7298c3af4` | 0 |
| ts/components/ConfirmLeaveCallModal.dom.tsx | 1612 | `a0ff4b1dc64f5ff50135017e1274d29bd980515c0e2c08bfefe0b0b0ba1d54dd` | 0 |
| ts/components/ContactPill.dom.tsx | 1778 | `9bbe66bd32115161a67d2e04b47f94bafccb30d06ec1cba09c5c79ed854b2d44` | 0 |
| ts/components/ContactPills.dom.tsx | 1080 | `58fe54b8bcbb52686926fbc6258521aa14fddae8b906629079d76bb5481fe7d9` | 0 |
| ts/components/ContextMenu.dom.tsx | 10393 | `d617249c768a8be5376f505afef342c17aed74aeb9869dffa24e7038f0b9481b` | 0 |
| ts/components/ConversationList.dom.tsx | 23655 | `1874c620ab9bfe18d81d569c1f89e3ec61adf487dd39709d36be206afc8fab7e` | 0 |
| ts/components/CountryCodeSelect.dom.tsx | 4895 | `fc283a75d50c90cc0101511a56678190f5a11c47cab447b6afffc1bd7495d527` | 0 |
| ts/components/CrashReportDialog.dom.tsx | 1526 | `49f74b631f5b3a4c67d241062cf13c2daff571c84c5208edc9cc7bf20a7f69f0` | 0 |
| ts/components/CriticalIdlePrimaryDeviceDialog.dom.tsx | 1283 | `c39a13644699f22814a369f8f2dd1051bfa9772e8ab10f510ad3a722dd75e9b0` | 0 |
| ts/components/CriticalIdlePrimaryDeviceModal.dom.tsx | 1967 | `d52e451bb27c665825dd5d52caeb51f8be50bc775a7c20549ce8b704c6d997c6` | 0 |
| ts/components/CustomColorEditor.dom.tsx | 5954 | `9d875ba66bd00e8988b6191f9c17d93ab616a519db6b84efbf960ae33641914b` | 0 |
| ts/components/CustomizingPreferredReactionsModal.dom.tsx | 5911 | `8553d33e8b3980d84bd46869b7707c94dc8c3dd13e2e5686fc33607d39b1943e` | 0 |
| ts/components/DatePicker.dom.tsx | 7091 | `1dd9c95dcc42aaf84ce03f96c53072d4929568b1c2d2c29d92d53ab62b81aead` | 0 |
| ts/components/DebugLogErrorModal.dom.tsx | 1096 | `92a0fa9f5b8b38faa604ae824090cf2f1bbe7a5dbdf50067eabb570677905214` | 0 |
| ts/components/DebugLogWindow.dom.tsx | 7256 | `3ce52c962305f3cb5bac171e0dbf79c1efcfeb9ab686adae68e459747c4b3fb9` | 0 |
| ts/components/DeleteAttachmentConfirmationDialog.dom.tsx | 1106 | `a36c358b9e7f5ffcd672f0fef2b0090ef1ecc4b5b83c27dfea66b9a09fa0aca0` | 0 |
| ts/components/DeleteMessagesConfirmationDialog.dom.tsx | 1200 | `30d4ac1796f753bb52bbd0a297a9b46bf04d6549d9fdc9edd370e4d31d06342f` | 0 |
| ts/components/DeleteMessagesModal.dom.tsx | 7366 | `d585f2065e3b011f2109adf42edf08884b451646b7aa603c3ddf96c07a3a2c2d` | 0 |
| ts/components/DialogClockSkew.dom.tsx | 1192 | `ceacf13bb2ca9042f2d8f8d0bd8608eab8937c1966f028f25bcb54959cc4d381` | 0 |
| ts/components/DialogExpiredBuild.dom.tsx | 1175 | `bd7ad3ea7dbe9f094b3b0f7296476c99a3cd6a1abdbb61638ceb3978003b7dee` | 0 |
| ts/components/DialogNetworkStatus.dom.tsx | 2565 | `16db093d87c14fc3c4b88a8b7b3f4fdfd635492b12340577cd1008e9937e2a1f` | 0 |
| ts/components/DialogRelink.dom.tsx | 2254 | `bf069c59db46ab8094e984636890a5e0dc6a5782c1c9a438694164326621cf79` | 0 |
| ts/components/DialogUpdate.dom.tsx | 6283 | `b60ec164d6d11a95e7f18ebbdc19dae3af71accef80b5bc8f2e1dbaebb8cbcf5` | 0 |
| ts/components/DirectCallRemoteParticipant.dom.tsx | 2678 | `da89bfed28561bb13ff111efea59dfdceab6f890eefdfac11cda0f956e122577` | 0 |
| ts/components/DisappearingTimeDialog.dom.tsx | 4626 | `851954ba797448befbe6df1289b7fabdf82b8230b6e3d8178e978de031f72167` | 0 |
| ts/components/DisappearingTimerSelect.dom.tsx | 3451 | `5958f0acbe3a639a84d97dd5c034b266a2f0da41224666b3755a1bedd1af510c` | 0 |
| ts/components/DiscardDraftDialog.dom.tsx | 1443 | `8df98aa28ee6111b639ee4f3fcc2f198d4c53fd8617783b16874b60cff91f111` | 0 |
| ts/components/DonationErrorModal.dom.tsx | 2379 | `2823eed5886c256a417f94fb2aeb172a036e39b2a371b10628614a0142334d74` | 0 |
| ts/components/DonationInterruptedModal.dom.tsx | 980 | `befbc0416ab3bd525d48f2d32148110b59afdf234f25d9263055d0583f2a2902` | 0 |
| ts/components/DonationPrivacyInformationModal.dom.tsx | 3393 | `6ba9c95122efcabda554901973f5e53168da491d7f9e006d3f033b395a08bb27` | 0 |
| ts/components/DonationProgressModal.dom.tsx | 1507 | `ea33412e41e658584bb5109f620e3386a930f02a86cace2337abd9ad33e3e013` | 0 |
| ts/components/DonationStillProcessingModal.dom.tsx | 716 | `cecad8a849beb40be99d910412d58be6593aa077b8922e1ce56b2af150f4a730` | 0 |
| ts/components/DonationThanksModal.dom.tsx | 3830 | `77746c120d1f347892b995660ea69fbb6713c96fad5481b5141ee664d3991775` | 0 |
| ts/components/DonationVerificationModal.dom.tsx | 2407 | `6ceeb2050b84a547844ab85f5af7be40fdbf260d6986984069a01a0bb3244d0e` | 0 |
| ts/components/DonationsErrorBoundary.dom.tsx | 1923 | `dfa2c85d1425d63d73b62ea0a96c0e5df0472061c68ec437251b29f650884ac2` | 0 |
| ts/components/DraftGifMessageSendModal.dom.tsx | 3989 | `85e7f496537ae4b1a3ec610c6b8b884f252c863ce14ea9c673e556c79f6d1b7b` | 0 |
| ts/components/EditHistoryMessagesModal.dom.tsx | 11307 | `1738c861af3ef21c04f626dfe3757ba0c0106e3eff672e881f18653603e0f958` | 0 |
| ts/components/EditNicknameAndNoteModal.dom.tsx | 7936 | `fcdb1aac48d263de114c23ca1c05170d39af2d88bfc288b3d58fa1a8782a5c5f` | 0 |
| ts/components/ErrorBoundary.dom.tsx | 1390 | `1a86e78971b5767cf6eaed40c91e4ce858eaac9b8645303a9e5fa71818c28484` | 0 |
| ts/components/ErrorModal.dom.tsx | 649 | `6a7bd9771844b28be06e6b5d79f6db329b0794ec7b3dba3b94f84d9a04633dae` | 0 |
| ts/components/FileThumbnail.dom.tsx | 1438 | `70a405f50a12aba5793bd78337e9e8af2d1957ec0734391f5d6da8b24e900ee7` | 0 |
| ts/components/ForwardMessagesModal.dom.tsx | 15965 | `398110d04bec06163be27c17f0ae8741b1562558af3b30bd064de7e18ab7e2b8` | 0 |
| ts/components/GlobalModalContainer.dom.tsx | 18311 | `16e37834fbf65aa06c58189d6a2f8694ba97f93260e97ce8060f123d65bfd54f` | 0 |
| ts/components/GradientDial.dom.tsx | 7688 | `919f5fdf221e8a55773de78b50af2be0f925a968a05a5d82dfb64469384bbe31` | 0 |
| ts/components/GroupCallOverflowArea.dom.tsx | 7099 | `9346730a50ebb8a96d959c8cef36e8fffd831ea910be1b4dccc02b5a11f1e3e1` | 0 |
| ts/components/GroupCallRemoteParticipant.dom.tsx | 23792 | `d0e7f327a4cb2ac6166091be40725d27e5255552eb38aad39aacaa93deb200f5` | 0 |
| ts/components/GroupCallRemoteParticipants.dom.tsx | 35255 | `6fb93b62bca09358e439510686de2ea39fe5ddf3409c69894aad2bf02926c317` | 0 |
| ts/components/GroupDescriptionInput.dom.tsx | 922 | `bc2c76de06296148d857a51fc00b69102c238538c941236d72d0b0e67758873f` | 0 |
| ts/components/GroupDescriptionText.dom.tsx | 987 | `0d566b5a020db7c4b8fa1e590f25b3946d010a619bf99c4ddfffaea6bd7ac29a` | 0 |
| ts/components/GroupDialog.dom.tsx | 3705 | `8c415c684a1d22b99d270c74bc67e2e642b394e1ac48520805e70a5204d56657` | 0 |
| ts/components/GroupMemberLabelInfoModal.dom.tsx | 2634 | `859e4fdf621100f048dfaa3b3d50c33947ec9c149b78a6805b0d10a1b80ef3fe` | 0 |
| ts/components/GroupMembersNames.dom.tsx | 5717 | `18aea138e62dcef9be9d4a111a44d86c0c951dc0c62e978233895c164fbbfc0a` | 0 |
| ts/components/GroupTitleInput.dom.tsx | 801 | `fbd6c65ca39985e95bca9770b50f1272ad69b84de38c1f55e6a7e6fabbe6f2ce` | 0 |
| ts/components/GroupV1MigrationDialog.dom.tsx | 5554 | `24a04ebe32fb1e4393a66c4cadf35eb433e81253946ed29eec2744de81adcddf` | 0 |
| ts/components/GroupV2JoinDialog.dom.tsx | 3680 | `0fd625ccc12a4ba627201943c9fbc59d91911accbf047d8b25b6cf811f51bd92` | 0 |
| ts/components/I18n.dom.tsx | 1025 | `732274f18ad62cffbce1aa908b626dd3cd2aa3c54ca2eeeea4945948ae19c637` | 0 |
| ts/components/IdenticonSVG.dom.tsx | 5109 | `1c42cf0f44c1fe71401ae2543d20d7ec0b0e8b9d812385e658214d90326805cf` | 0 |
| ts/components/ImageOrBlurhash.dom.tsx | 2407 | `e0ada7912f8bf1a054802911e95cf271b881e7c541a59ce48945720e7e236254` | 0 |
| ts/components/InContactsIcon.dom.tsx | 1056 | `65e4c00edd88c5da076ea207c031286a56a066ad550fe864659dd659b6e8ca4a` | 0 |
| ts/components/Inbox.dom.tsx | 1460 | `c8e067b873b8bbfc4cfca06b31c05bd2e29a31b46ced4b6365a54e048a5e8a24` | 0 |
| ts/components/IncomingCallBar.dom.tsx | 10512 | `55284213c4896d5fc8cdc019b597e7d8cd605d383061c8eba6f5aef0723d6bc0` | 0 |
| ts/components/Input.dom.tsx | 8828 | `e793afdb663daa5a99da4348822ff61d66a76d35d2de4a9bb5c60ceda712f57f` | 0 |
| ts/components/InstallScreen.dom.tsx | 2036 | `595239655359b4c4fd33f8717d34f57e24b7e75f7cd2a78272048dc38f33a6ba` | 0 |
| ts/components/KeyTransparencyErrorDialog.dom.tsx | 3186 | `2af999554705cd8d0ce20afe9a5bd9b3487d58a494db5e4dd97aba18962c11b4` | 0 |
| ts/components/KeyTransparencyOnboardingDialog.dom.tsx | 3051 | `d3db4c31216d697768be0ff67722c49c799c258902213658b4aeab42e5cf5772` | 0 |
| ts/components/LeftPane.dom.tsx | 37575 | `c11b9a79054f020d5ad7ae15efe018e9f0599a9b958817d042214b673690bfcf` | 0 |
| ts/components/LeftPaneBanner.dom.tsx | 1006 | `65d3f5df3b6b02645a497a6eaa6dc060afc4210e0da23f909aba584f41bca4c3` | 0 |
| ts/components/LeftPaneDialog.dom.tsx | 5681 | `b950e99218a6dad6ca5c934f9351de3b3f504e4d9e152fcc9ab3c218b66678e1` | 0 |
| ts/components/LeftPaneSearchInput.dom.tsx | 6600 | `73a6a67259af885524eb1a464197db605a407bfb6eb7573cb4f537ee87dac1ff` | 0 |
| ts/components/Lightbox.dom.tsx | 27603 | `e9e190e463ed61701a99f45e81a92cb51d6cdc134fa1df02a7ce93800b236869` | 0 |
| ts/components/ListTile.dom.tsx | 5596 | `740e3540e8b64a1101ec908a490a207743cb5878a57bfd61563190d6bd64284e` | 0 |
| ts/components/ListView.dom.tsx | 1921 | `f4adc2f92a593d4866ceb00236dbe26a14c301564e71503ce80278ac815b6877` | 0 |
| ts/components/LocalBackupExportWorkflow.dom.tsx | 8690 | `2775a3b727457de12e47656d810f282bf31ad85bbdc130f06e53ab78d28aa922` | 0 |
| ts/components/LowDiskSpaceBackupImportModal.dom.tsx | 1649 | `662b594fbcafcbfdad6c1cfbb325934dfb787e03b229e6e5fe31a136c4796dbf` | 0 |
| ts/components/MaybeTransferModal.dom.tsx | 5033 | `222588884a25787f050e286ba4735756f74ae9e55ea2a03a8dd12502595feef4` | 0 |
| ts/components/MediaEditor.dom.tsx | 53079 | `3229c888a592ca256ebf28d905a2ef489b0cb44cd692616f1c119038f343efae` | 0 |
| ts/components/MediaPermissionsModal.dom.tsx | 3590 | `cf0ce7992ed36d4e692dac337d3fcfb7e5f4fc12379599031296b5de89bf55a7` | 0 |
| ts/components/MediaQualitySelector.dom.tsx | 2582 | `fa6ce145cdeaeb2bb82e2728737280853cd58729801573d2bca3973d332f0421` | 0 |
| ts/components/Megaphone.dom.tsx | 3762 | `c37219ae21a0baad3a7c8aacb5a8f2fa783fcc13346cb235df68e9eb77440c9d` | 0 |
| ts/components/MiniPlayer.dom.tsx | 3220 | `2c627aeceedb34fadd1071b0bf96da9fe7062cae6f98638bdaaa5646e6292d61` | 0 |
| ts/components/Modal.dom.tsx | 10253 | `3afd9dfbc284298060606474e112a9cca59ef6ba57f78594858db1a112664c7c` | 0 |
| ts/components/ModalContainer.dom.tsx | 1012 | `c195ca6c3a699934fa0c9b09b3635eaf8b5e11a7b81cab181688da8a0d4ecee6` | 0 |
| ts/components/ModalHost.dom.tsx | 4050 | `ba91319d22db215df29aed70f4bacecac0401f2f6abeb057786170a10a1bf2b7` | 0 |
| ts/components/MuteNotificationsMenu.dom.tsx | 6677 | `51220c20ea54ab2ff81432f366c7d94d0fbe62330ddb2170afe969a9d35bc140` | 0 |
| ts/components/MuteUntilDialog.dom.tsx | 4183 | `9d79ff35e25dac2ba9eb9b8a527f44df939f0ce30d19ba92b60f842623d338f4` | 0 |
| ts/components/MyStories.dom.tsx | 10060 | `d87f70d9f718dc9c1ac4debfa468c6dfcdff46a4a8e7131bdb7c2b0434d7d8e9` | 0 |
| ts/components/MyStoryButton.dom.tsx | 6397 | `959dceb1ecf7781105643c67cab04e4e42a259e954942ff4ec13c47e2ef52616` | 0 |
| ts/components/NavSidebar.dom.tsx | 8262 | `49edbd5981ebdb34ca7c4592b73f9e68267bf99001f77968a0f3444add796707` | 0 |
| ts/components/NavTabs.dom.tsx | 9018 | `632da940772e39b7e1519cd3f83721a5d00b1d62cdf397ddadab547a032d38d1` | 0 |
| ts/components/NeedsScreenRecordingPermissionsModal.dom.tsx | 2324 | `f6d1f0e4be50c32f9a38837057bcf04b561ccc3ffd75d99934c6d24c0986786b` | 0 |
| ts/components/NewlyCreatedGroupInvitedContactsDialog.dom.tsx | 2736 | `5bdbfe754a1605b7c1dc50047ec3dbe4de5e023ae4758a393918ae0ad1ee0ba7` | 0 |
| ts/components/NotePreviewModal.dom.tsx | 2042 | `6305a405978916f8229f00551df462e055cbb4aff1cfa7e64af0e401ca9b4740` | 0 |
| ts/components/NotificationProfilesMenu.dom.tsx | 5115 | `cfcb65b15210fe74bd50c23ec586abee28e21c77947a43b25b0a347f535ae0a0` | 0 |
| ts/components/OutgoingGiftBadgeModal.dom.tsx | 2423 | `b64816633e71b62cbc9e34782434ce150ec55b744377caab4bc743cb10438c65` | 0 |
| ts/components/Pdf.dom.tsx | 826 | `b79b982f16a1bbdfc062bb7324df6df02d130db32014e677e96fb5a5cf4ca030` | 0 |
| ts/components/PermissionsPopup.dom.tsx | 1210 | `db179a3735662745316f2001ccc6d49253a52cb53837ffb87e40d74f1dc65d4d` | 0 |
| ts/components/PinChangeModal.dom.tsx | 5405 | `4f8c919b3566a373ee511dc04212d22e4b507c17221e96683603bfdf51e95ff7` | 0 |
| ts/components/PinReminderMegaphone.dom.tsx | 1174 | `590a38d87b3c5a88b7be7e182d833745817cd76c39177c7cc1c4130d539a88a9` | 0 |
| ts/components/PinReminderModal.dom.tsx | 4298 | `2345f60bc8f1e94988c1bdafb4b414a50761ef227cf56e71e00c45ce81b7b1ba` | 0 |
| ts/components/PlaintextExportWorkflow.dom.tsx | 9691 | `8b4542e29b3725ef2406630e8c57bc2def1f6a10b2db4d3298ddf69679a26d39` | 0 |
| ts/components/PlaybackButton.dom.tsx | 4234 | `188a1be5ca4c78edf4b42708f3da259ba309eb959fb088930e526f9b9de7e1eb` | 0 |
| ts/components/PlaybackRateButton.dom.tsx | 3114 | `a5b66bb3e470262d2ece6dbd7cca60acec24d12e1ea9b84aae9a0f1bf81797f3` | 0 |
| ts/components/PollCreateModal.dom.tsx | 14801 | `2d43bda3414e2fef3fac7d47bbf0f6ec07f798c7da3090abb937600de989dd49` | 0 |
| ts/components/Preferences.dom.tsx | 108184 | `357b37acea94b98ee665f5eb5007e896c71e90beabbfb743b9e070f360a10efb` | 0 |
| ts/components/PreferencesBackupDetails.dom.tsx | 8871 | `8b0bb1e77621d05e1e9a63afc5dab64c0a5538478d1325ffae40066832250bb2` | 0 |
| ts/components/PreferencesBackups.dom.tsx | 14037 | `3614422b9c4653bb50312d2ad6ab7263afc9a9783d591fd5c90a576faa3a6385` | 0 |
| ts/components/PreferencesDonateFlow.dom.tsx | 36108 | `22a4d48d0272f7a47968ceaf549a358813204f0a56b1b1e92a5639cb80e5c63f` | 0 |
| ts/components/PreferencesDonations.dom.tsx | 27674 | `087c37953d4b0a6d1698a6398552f2853f29a6908c10714e709aff8e785b4114` | 0 |
| ts/components/PreferencesInternal.dom.tsx | 30462 | `919490dd47b71c5b729e7405d415f0d34cbf10050fbf1b81fc0fe7dc03e6c5a1` | 0 |
| ts/components/PreferencesLocalBackups.dom.tsx | 27468 | `61304c479418af53b0ec33664a3ae2e8dd6e3cdb545be68994568c65a2236b4b` | 0 |
| ts/components/PreferencesNotificationProfiles.dom.tsx | 50894 | `322ced9e78b19f332350a5dac49a261ad5a5964f226cb0be722ac215257cc74c` | 0 |
| ts/components/PreferencesUtil.dom.tsx | 3581 | `0aabf8244024a22927bb4a63a36d9dbf82268a9da9014de6db47d495e206b749` | 0 |
| ts/components/ProfileEditor.dom.tsx | 31175 | `303c9af75ac908f477d15abbe82b6fed8f66a25a0d6457d232e45342a7015d16` | 0 |
| ts/components/Profiler.dom.tsx | 842 | `ea6fb4c8527995cef2d1866ebaf6c88c6a13d2e745276959d0fa2782718bb4d0` | 0 |
| ts/components/ProgressBar.dom.tsx | 671 | `6df1c8d79b8aeddd28e4c1573c4bdfef1d8f00903467029d4dc2c382c2b6b8a0` | 0 |
| ts/components/ProgressDialog.dom.tsx | 807 | `d68f20cfadd7d5f1e15b8586060e2f9f404e39046e49acf9347af9c5736c9a3d` | 0 |
| ts/components/ProgressModal.dom.tsx | 1178 | `b1033ddd0472e0db12c8945dd4c908b3738d9a8702b93cc146f88cc5bfea7e07` | 0 |
| ts/components/QrCode.dom.tsx | 1889 | `633b7ed2dc5c02e77ecf8d8664d69d516514c498dc00c2ccb72ac4bb781fbc75` | 0 |
| ts/components/ReactionPickerPicker.dom.tsx | 2222 | `ebf769676a400e18ad25a7daec27378550c7a0a9a41cedc705bfe6765380e8dc` | 0 |
| ts/components/RecordingComposer.dom.tsx | 889 | `91a11bc47ecbedcbb975fd79c3adbcda5e42b7198a38959b780df9a74b312a6c` | 0 |
| ts/components/RecoveryKeyPasteWarning.dom.tsx | 2783 | `da574345238b610978ebab1fc88e48cc37c2a43e2c39a32b102d7c66629d8b7e` | 0 |
| ts/components/RemoteMegaphone.dom.tsx | 1641 | `d2b6d3d151a75f6ee805eb5db62954e9b1733ceed0fe8a09f9a22d0da61eedad` | 0 |
| ts/components/SafetyNumberChangeDialog.dom.tsx | 17900 | `b836d05158f0c7b2de73dc3bdd175d9ead19f524cf48415966e0c72aa63c4a6a` | 0 |
| ts/components/SafetyNumberModal.dom.tsx | 2905 | `ee743cbd43c54ae4f15b4b04c326cdfa1efc8fbce6b8467c9f27ed4351eef214` | 0 |
| ts/components/SafetyNumberViewer.dom.tsx | 10882 | `9635a9695f7898921ef6f97cfb679dd7ac7f20793fe1189a792430fb73197e65` | 0 |
| ts/components/SafetyTipsModal.dom.tsx | 9596 | `682722a9bdc719cc648c4af375fb37b1ae3bc6b5972c4e7b0d805a9ea059b24f` | 0 |
| ts/components/SampleMessageBubbles.dom.tsx | 4191 | `65ab540a4f83fa288fbaafd0d01850df48b24d97a2a5908835fddedf376a07f4` | 0 |
| ts/components/SearchInput.dom.tsx | 3222 | `bd6b963f81683811d867a1926522691b30d54423bc5f3f48f8dd8cb234658489` | 0 |
| ts/components/Select.dom.tsx | 1636 | `cd6a714ab341d25b76fe08cf1ab64628452894ed1ec8202defa12ea326e2fb19` | 0 |
| ts/components/SendStoryModal.dom.tsx | 34994 | `0bff6185f9429ada3169396406cdc4e9580908d767df013b37c903b92d515b9b` | 0 |
| ts/components/ServerAlerts.dom.tsx | 1882 | `ed8d26fac4be250efd0e3e4e5dd230824d9c1ba91778e1ea01a3492082b3eda9` | 0 |
| ts/components/SharedGroupNames.dom.tsx | 3198 | `9e7410029c87a52a6ff308197d3ff6cf85cf95899c389b7cc55e23970ecfd322` | 0 |
| ts/components/ShortcutGuide.dom.tsx | 15584 | `315405d26b1eaaff6c556765d221332e80841ea5527567e84da9d5546202221a` | 0 |
| ts/components/ShortcutGuideModal.dom.tsx | 1267 | `b2038e8dcdaa93c9d104e0d1ad1c881758473ab2dc18dcb247f3b1b7eb0732b9` | 0 |
| ts/components/SignalConnectionsModal.dom.tsx | 2608 | `1bc99c7f313064cbaf90206c379d12f97b120aee086548d227a07add4185e578` | 0 |
| ts/components/SimpleQuillWrapper.dom.tsx | 2078 | `3ffb4309d87aeef61626b26e3d7d5adf036bde438080d52b59488b2ea8e714a7` | 0 |
| ts/components/Slider.dom.tsx | 3027 | `cca95dd9aecb121036e88ef40765d0a8670ab451991c82ff00ff6d989ce7a91f` | 0 |
| ts/components/Spinner.dom.tsx | 1928 | `42f4ca56cbfc6122e553b5196c0901f728d9452c6a180ef48f9a871e27fba197` | 0 |
| ts/components/SpinnerV2.dom.tsx | 4512 | `572a2d7e110f0d383dd5e8a5c07169fa1c1a6529aff0295a4903d97e8d0f6077` | 0 |
| ts/components/StoriesAddStoryButton.dom.tsx | 3700 | `c56ca817b2a9e1994c224316abdbb8b9e87a39d1f2ad6b739bb6f9b076cd75b6` | 0 |
| ts/components/StoriesPane.dom.tsx | 6331 | `125c29b22413ec1b46020146ce71a465ed6637436de277fc542a2029513a7c67` | 0 |
| ts/components/StoriesSettingsModal.dom.tsx | 41747 | `6cd52afe24264d9b82dd42ff15568458ae79214872698a7f4067837973e8f9ae` | 0 |
| ts/components/StoriesTab.dom.tsx | 7921 | `e087a17efd5ad3d83c9f806b1f4d68d250bb66dcbef35a5a40785f4ed00e922c` | 0 |
| ts/components/StoryCreator.dom.tsx | 10489 | `e63744d6d5f61f9558ca6700fb28c4e1bb9cb42960545cc03b81f7f03e9c7f09` | 0 |
| ts/components/StoryDetailsModal.dom.tsx | 9242 | `4ff81405fd2bc8095c566a28c1bc000161a9c8a7c800c6ee4991d356d23b7d3e` | 0 |
| ts/components/StoryDistributionListName.dom.tsx | 659 | `5f12376c068ab928d06ebe26fd01f3544e51ea33cc7c48f2ba06589e17b7b4a2` | 0 |
| ts/components/StoryImage.dom.tsx | 5294 | `d84bfe735981b673d1a1f334275b1a038ac2169886287fd2ba08d9a4fe188e8c` | 0 |
| ts/components/StoryLinkPreview.dom.tsx | 2582 | `15dd88d68b1983e02c947232ff63ee009a0f99c1c383a982077525893c53aec4` | 0 |
| ts/components/StoryListItem.dom.tsx | 6799 | `853f4447d26861575182f3522a05ab8a71fdbb02e0a69870ab8d198f188490fd` | 0 |
| ts/components/StoryProgressSegment.dom.tsx | 1708 | `4fbde1f88a0475d1047643c4a93ad5650b1939c48623d3a3fd069e0d3400147c` | 0 |
| ts/components/StoryViewer.dom.tsx | 34196 | `81fae63fcd33bc1f6d2ba6fda6715e2ed311bfd598148c15e79ad778c8dade61` | 0 |
| ts/components/StoryViewsNRepliesModal.dom.tsx | 24328 | `320f2c03dbbbc7c521864e06d90f41f5c570a4a641b7a6045e54d2790b0769f9` | 0 |
| ts/components/Tabs.dom.tsx | 606 | `f1eff8a8ef74769cadd51dd0221c43653776d1d11e8c3c4500d678dd4ebc04d1` | 0 |
| ts/components/TapToViewNotAvailableModal.dom.tsx | 1227 | `5f0ca6a08208422809e543247a867a9da2289e50c199d9e964649436b2c7b5e2` | 0 |
| ts/components/TerminateGroupFailedModal.dom.tsx | 1298 | `f78269c0ca303526050c3942833d5361270942296ecc09272a5d8ea379a69ba0` | 0 |
| ts/components/TextAttachment.dom.tsx | 9961 | `91fbbdf4e5beb9d45e96e107dce5c79d4201465865d98442e5463a948b8c625f` | 0 |
| ts/components/TextStoryCreator.dom.tsx | 22014 | `46bf3738327675619577bc5177db2ec4c3b936555d72879d32a118b06cd3a62d` | 0 |
| ts/components/Time.dom.tsx | 857 | `42029cdb6e8fda978c306b85f519ff9f8e810010840bd4118ee10e8cbbd7e9f0` | 0 |
| ts/components/TimePicker.dom.tsx | 11568 | `26805f8005ee24b660e6ba2a415941b653d25346658eb736c3ca5862093ddb76` | 0 |
| ts/components/TitlebarDragArea.dom.tsx | 369 | `7ad56ef22c6ceb84f269a18e215c0b0e0b261cdce461fc86a166dcb86cd98239` | 0 |
| ts/components/Toast.dom.tsx | 2417 | `c4422cef20351fa7cce08ed3fc1f28ed23dd055b90844a3aeacedfdf89e7844c` | 0 |
| ts/components/ToastManager.dom.tsx | 29714 | `c52f60454d632db681d7c930ddbbb98e41c09b3ed35cfdf6893d79c356626d14` | 0 |
| ts/components/Tooltip.dom.tsx | 5487 | `55acdd14e13b5f72e3cfe78a9314def002e9d805bb87ad8571acbf513c669727` | 0 |
| ts/components/UnsupportedOSDialog.dom.tsx | 1759 | `118757212931edbffda2bbfeb975fcddeb059bd1abceb47ce31f6c500a70646a` | 0 |
| ts/components/UserText.dom.tsx | 738 | `c3b80f556f84611178b4dbd5ed6275a619d1ba1b867fa54b5330b1c1c2bd30f8` | 0 |
| ts/components/UsernameEditor.dom.tsx | 16631 | `fb00b1be3f75e376c5fea903a5c2495e2da4348b80a282fe34d38a63ff6fda9a` | 0 |
| ts/components/UsernameLinkEditor.dom.tsx | 21782 | `9202c46774eabb36a47df12cfa38a6d275dadca32de0feb78f30824cc2d8c436` | 0 |
| ts/components/UsernameMegaphone.dom.tsx | 1533 | `778cf5ca1f3fa73187b2dd12f2fc7fa3bc76b86c0fc115bcf3bd4ae19598d202` | 0 |
| ts/components/UsernameOnboardingModal.dom.tsx | 3474 | `c06485421d776a80939484873cc04730217fdbde165fc607c8b3314f74993ac6` | 0 |
| ts/components/VoiceNotesPlaybackContext.dom.tsx | 5201 | `7bc2fef9d0cc90247f9eb042b4f057b819aa7c9a847e3d995637ac65ae14f393` | 0 |
| ts/components/WarningIdlePrimaryDeviceDialog.dom.tsx | 1873 | `96e37fe7830841212b7f505e3a7edab23d02dbd87bbf327ab1dab67ed4d77046` | 0 |
| ts/components/WhatsNewLink.dom.tsx | 744 | `a5998b0e9eb00d01d5383573d281fd585c5517d74e3a7bbaa456088fb039d528` | 0 |
| ts/components/WhatsNewModal.dom.tsx | 2646 | `e08da5b4e17635fc0a34964c550a8a4df34bcdd1c29287e3524073f5810e861a` | 0 |
| ts/components/_util.std.ts | 436 | `19f83e46c3e07b61cdb3e73743c7ab27598b9f9c11396dca047901bbb1ba2a54` | 0 |
| ts/components/conversation/About.dom.tsx | 484 | `b9afe259735adc2f3d209bf6a01d872cc3554a1bb5ab9f258e5a8b9393ce831b` | 0 |
| ts/components/conversation/AboutContactModal.dom.tsx | 12694 | `e7760a392dd2110b15dc3267c51ba88ff5a33309d1ea690ad38747f390b50f4c` | 0 |
| ts/components/conversation/AddNewLines.dom.tsx | 1287 | `a077dc39d5b6c6eba6cd92494c616a14862c30a6a3d2bbeba507796f20ba3aa6` | 0 |
| ts/components/conversation/AtMention.dom.tsx | 1486 | `858ce01676b96b81d8b776555bf530103a81c55c5c5317a1ce3315e2b3075acc` | 0 |
| ts/components/conversation/AttachmentDetailPill.dom.tsx | 5454 | `7a55e5924e22353f2df95acc58392d4dde29bfe16c82482843d5cdb6c36d8075` | 0 |
| ts/components/conversation/AttachmentList.dom.tsx | 5182 | `06c7fc8db735d4ff796e264c328b9e1078dd9909e9ec3d72b6e97376449aba39` | 0 |
| ts/components/conversation/AttachmentStatusIcon.dom.tsx | 2668 | `8c6ca4a71b28efa9ff1358ddcd139f0e2aac94f9dc400584603f3da0d6c4e975` | 0 |
| ts/components/conversation/AudioCapture.dom.tsx | 2163 | `24d1c6797ec04531c9ab3d5f7636a93724b5c2ba9f5b60511651ac8a713983f9` | 0 |
| ts/components/conversation/CallingNotification.dom.tsx | 7542 | `bfa7155587bbe5ff1c00628338442b2422fa4943f137855a708de32b63d603cd` | 0 |
| ts/components/conversation/ChangeNumberNotification.dom.tsx | 1241 | `0fb000c1968f91ccea617c85b5f03e5f25570dbb509a8268fdddbf4bc92479be` | 0 |
| ts/components/conversation/ChatSessionRefreshedDialog.dom.tsx | 2478 | `c03f26102bfb177e4587bbccae9080b634913f7492647342d6a99d80899e9027` | 0 |
| ts/components/conversation/ChatSessionRefreshedNotification.dom.tsx | 963 | `fce59139c25d1a7bd6e6bb723c0d9e8b7bf0492d8054b91c0de6206e20e54b8b` | 0 |
| ts/components/conversation/CollapseSet.dom.tsx | 12458 | `01ca10d46b636f076211cc5ed605ae3b231f711abe43106b5e8a98b63d3d6efb` | 0 |
| ts/components/conversation/ContactDetail.dom.tsx | 9487 | `bb80c3b5b6015a04277fe114ec8789e5f2905c8f8e6240ad7a47a599f71346f6` | 0 |
| ts/components/conversation/ContactModal.dom.tsx | 24862 | `3e25278a14fd04218b23122fddd47b006ac138e1de5cbe4d2f4155e9aba2a5f5` | 0 |
| ts/components/conversation/ContactName.dom.tsx | 5428 | `138a2ffd7eed765832291edfe5b5f9c30972b80b0111ff44737966ecf16cf0db` | 0 |
| ts/components/conversation/ContactSpoofingReviewDialog.dom.tsx | 15290 | `38123017332f4a80bc41336b3fad51b487ae45d1bed3eb9a9d63d1313ac2f7a9` | 0 |
| ts/components/conversation/ContactSpoofingReviewDialogPerson.dom.tsx | 4708 | `cf2704cc6007e8786cc3a725dd64e7c044340faffb9bc6eb6d30d7f73b9c7598` | 0 |
| ts/components/conversation/ConversationHeader.dom.tsx | 44087 | `0518c8623bd66e33f13b81e7b890a6617d403aab14cb07f6589d1a84583b884e` | 0 |
| ts/components/conversation/ConversationHero.dom.tsx | 10442 | `ca6608f868bf7ab0dc302c1b29936a64f85cc91d25bf9f5179c72e1bd8bc2933` | 0 |
| ts/components/conversation/ConversationMergeNotification.dom.tsx | 3407 | `bf76f82b839f3a3a2ec819b2f5946ba61059fd985c8b9f3bb9381f5073ee2dd7` | 0 |
| ts/components/conversation/ConversationView.dom.tsx | 5181 | `edd4bedd21b71f2eb67d2eafde39ad4c332921b32208ce4cdab6ff872d69da9a` | 0 |
| ts/components/conversation/DeliveryIssueDialog.dom.tsx | 3070 | `bb336f46cdbe8aaa80ac0c97c393dcceab3d4cf09d0edb9fb989a4ae6a3a97e0` | 0 |
| ts/components/conversation/DeliveryIssueNotification.dom.tsx | 1458 | `f14968b1ca9f43ff48571e740fe3db5ad5236273d972d90e40e1a28c26c89e8a` | 0 |
| ts/components/conversation/DonationsOfflineTooltip.dom.tsx | 829 | `7aa533fb4b7a1abb8d9b9da955767aa73b1f710a754906fa38a3e8e1cce066f8` | 0 |
| ts/components/conversation/EmbeddedContact.dom.tsx | 2438 | `c6a3c8dd98636ededfa2d2d504f567c4dc0951cf1564cea9c6ca5167ebbb2121` | 0 |
| ts/components/conversation/Emojify.dom.tsx | 1650 | `2fba322bc1b7cdac00d6520ca72c4f23024f12eceafcd8b1880649f3b68e4a30` | 0 |
| ts/components/conversation/ErrorBoundary.dom.tsx | 1999 | `23c9c6cad31a04d2790e8573c49e662c3412b342ce761255bafe574e82bdcc2f` | 0 |
| ts/components/conversation/ExpireTimer.dom.tsx | 1535 | `2e4107cdd6bcbdb33f5c0e067a015880d59568a20e616e82ee680ca0c078209a` | 0 |
| ts/components/conversation/GIF.dom.tsx | 8366 | `3acd05918d772fe5a2f8c4bbc4aab7432c6b532d02bddfc7c90adbb00a82d5c1` | 0 |
| ts/components/conversation/GroupDescription.dom.tsx | 2418 | `4e9ef7e373b11efac8ce8233a922fabcdcdc566e098bc2c4dcee467d6fd11f06` | 0 |
| ts/components/conversation/GroupNotification.dom.tsx | 4911 | `9ba8e9758f31130cf0c533bc2524c779e7f5245ac1f05a558f9b94b438e91b22` | 0 |
| ts/components/conversation/GroupV1DisabledActions.dom.tsx | 1534 | `a0d665a5d92b5076197b21ea7fc41fe8e6f4e7e143c6867c0d4c189685870c94` | 0 |
| ts/components/conversation/GroupV1Migration.dom.tsx | 4554 | `ab0354bb111976337d53654451db3034abbda0a1a012dc595b1d0ad30b62ffb1` | 0 |
| ts/components/conversation/GroupV2Change.dom.tsx | 10147 | `31d29e2086b1267728473a1b3d84dc996fc22b455324bebbda48a501d09e113d` | 0 |
| ts/components/conversation/GroupV2PendingApprovalActions.dom.tsx | 1883 | `5ede9250f2b4a6d9dc69a164dc633aebd3400fb6517cf352487f750817d35920` | 0 |
| ts/components/conversation/Image.dom.tsx | 9718 | `05a408abb1d207c12c529d41b8963f3707f94ec91b94e234e6a04bc079c023e1` | 0 |
| ts/components/conversation/ImageGrid.dom.tsx | 20956 | `0ea6bf24bcaa2116e30a1c8ad7f990a3171e3198b577125041c0a34217800f19` | 0 |
| ts/components/conversation/InAnotherCallTooltip.dom.tsx | 732 | `b4cac0e751801f0017a3ecc95b56636f80ec42bcaffde9749860547251cdff07` | 0 |
| ts/components/conversation/InlineNotificationWrapper.dom.tsx | 2625 | `96f9df769ae26d20378ba4df88400eb20c0df35fac7b040839402aa66957f2cc` | 0 |
| ts/components/conversation/JoinedSignalNotification.dom.tsx | 881 | `648e162c740f13eb82b1d7748453e533d4c21f1e56de966eb5c972e6fa57a897` | 0 |
| ts/components/conversation/LastSeenIndicator.dom.tsx | 746 | `f6d69cfbb552014f9fb7ef28eb902fb51eef9834a83560087278bc5fd04cc479` | 0 |
| ts/components/conversation/LinkPreviewDate.dom.tsx | 682 | `a4cae0d8fb5423456e3190ed34601698c570efc16ffe4e5bcf131b0d0f9d64ec` | 0 |
| ts/components/conversation/Linkify.dom.tsx | 6239 | `2b2b5a2affd4d426ca23aab01c5a4bcfba3d23bcffcfa089fdb7907d5a05ea2c` | 0 |
| ts/components/conversation/MandatoryProfileSharingActions.dom.tsx | 4167 | `d3daacf9c94247854a4ed09c1de972d01466df8cde18e7df85a34f02595c649f` | 0 |
| ts/components/conversation/Message.dom.tsx | 106030 | `13dd18538970aca6f3efb19dca96df97b331d24e1d7e1e1cca109c6f3f3ac41c` | 0 |
| ts/components/conversation/MessageAudio.dom.tsx | 11575 | `d26ddd859fdf306b5378ef6a3aab0df192bf124edd14d6afe56f800847d88d33` | 0 |
| ts/components/conversation/MessageBody.dom.tsx | 5547 | `54f9dcae51ba845f4c15fb6b1e7821467efc330d4d02e2dcbeb6c5566693f1bd` | 0 |
| ts/components/conversation/MessageBodyReadMore.dom.tsx | 2257 | `d71bc7ef896a658bffcbdb30e25271fa63dd53a692a270538166bc8e25d323eb` | 0 |
| ts/components/conversation/MessageContextMenu.dom.tsx | 5892 | `6d05f5416864fe4973ce2fd10a4fb648965da037fadbfe96ab5a0c7f8a518371` | 0 |
| ts/components/conversation/MessageDetail.dom.tsx | 16986 | `93155050083effa744be353a69a19fe3ca44677eadc7c250912fcb22d566b530` | 0 |
| ts/components/conversation/MessageMetadata.dom.tsx | 11290 | `912f79eee2cdbfa34dc278e4bdceedd3bad9756083744269c11418978d03aa97` | 0 |
| ts/components/conversation/MessageRequestActions.dom.tsx | 6037 | `b7290d6d61856ba3c144c3be67c8e7a46638412cdc0948c8db215cdfec808727` | 0 |
| ts/components/conversation/MessageRequestActionsConfirmation.dom.tsx | 10529 | `0d5457ecd1dfc4f5fe0721b7235486e607ee4c3699f3a930634f67684e3b9d6b` | 0 |
| ts/components/conversation/MessageRequestResponseNotification.dom.tsx | 4081 | `47dc20b17c00b16c7b49ac89fc5a6d32cea13058db3cf7aac09f6ecc953e21b4` | 0 |
| ts/components/conversation/MessageTextMetadataSpacer.dom.tsx | 364 | `bd6348636ca0dbb7ab3d267a03b3f4add9d02dde68bda386e05ed1ffd542a32e` | 0 |
| ts/components/conversation/MessageTextRenderer.dom.tsx | 12234 | `f8372ad7178b41a70587464b92ae57223444743390364588816c357ef845de8b` | 0 |
| ts/components/conversation/MessageTimestamp.dom.tsx | 1063 | `0c1a76471fcd302275c1b4f4e7dc68bad470e17e28dcd7c8d624f9b0023d6306` | 0 |
| ts/components/conversation/OfficialChatInlineBadge.dom.tsx | 901 | `859e9717d6795dc967f4ab6103f184d8250cf5e11ad78e7846e124c431697bd8` | 0 |
| ts/components/conversation/PaymentEventNotification.dom.tsx | 1010 | `cc5d84a5d5a4c63c75dc0c524aa7e8c66017f6d0388be3ed84f073c78cb6feb6` | 0 |
| ts/components/conversation/PhoneNumberDiscoveryNotification.dom.tsx | 1340 | `2730a3114972fd3c25a4f998add0ed95e5c281c47edf723355c53755e6e1a5c9` | 0 |
| ts/components/conversation/PollTerminateNotification.dom.tsx | 2499 | `9a95df0ab886006bd05d9e7e5638e8ac4110c3467c2ebf452cd25b57e7b7eb62` | 0 |
| ts/components/conversation/ProfileChangeNotification.dom.tsx | 1721 | `1459896d95e1f8d57378462f66ea234ed69fed99b7986e7a254c0c70ce1feac2` | 0 |
| ts/components/conversation/ProfileNameWarningModal.dom.tsx | 3368 | `48eb0a2b707948556bb05ec3eab932dbac6d29b9ba6aa392ca510f2b4ad6722d` | 0 |
| ts/components/conversation/Quote.dom.tsx | 16066 | `82930becc9e64889b34db88ff5ecebc459c17b6e21f3d109652627b3bfaf5128` | 0 |
| ts/components/conversation/ReactionPicker.dom.tsx | 4072 | `c2072b9a9d41b719c62a3dd4133b1cbb73bb9825af7f16bbd0b30c5938848d0b` | 0 |
| ts/components/conversation/ReactionViewer.dom.tsx | 8502 | `7c34e819c4929a7d5aa2ef1b42a25b94f4e078575359247b329da6dfc3b5d94b` | 0 |
| ts/components/conversation/RemoveGroupMemberConfirmationDialog.dom.tsx | 1808 | `c723920f5661e9db47345a6a7e1671b69078d2f029e5df7c1e4caed6f13311d9` | 0 |
| ts/components/conversation/ResetSessionNotification.dom.tsx | 459 | `c1390f8048a279a06390481cf5e8a4f129a31be9237734d4b7a4eeb49875874b` | 0 |
| ts/components/conversation/SafetyNumberNotification.dom.tsx | 1431 | `a81c4eb04b6f75b4f0b52d165fa42f372be1fbab7d8b09d4449a272d7be0b1a9` | 0 |
| ts/components/conversation/ScrollDownButton.dom.tsx | 1764 | `03197e4ecc33809cbd3744ae0caf3657991e1673aef5306c25477490227e8f67` | 0 |
| ts/components/conversation/SelectModeActions.dom.tsx | 3015 | `f2217bf2dadd4eb2be1f3a12281c2a2c67e655f37e56fe2f1a14b69aa68e7388` | 0 |
| ts/components/conversation/SignalConversationBackground.dom.tsx | 2520 | `fc8efc54a7a6bb6d6b497427f8c7bcee21d8167136661b3f47af162cb15e5b5c` | 0 |
| ts/components/conversation/StagedGenericAttachment.dom.tsx | 1093 | `f4be6ab1b2d22729585bdf393da400416745d2d56e524870c5facec64f6ef3e4` | 0 |
| ts/components/conversation/StagedLinkPreview.dom.tsx | 5436 | `37d6bf69956e1ad9c0d5d6a29b5256cd8b641c21ca8f4e0d8ba3732ed0f43fd3` | 0 |
| ts/components/conversation/StagedPlaceholderAttachment.dom.tsx | 623 | `695b1c8179d4da5cdea754f8a61a2dc179269bbeddcd302fa48bfd85fccacbff` | 0 |
| ts/components/conversation/SystemMessage.dom.tsx | 5300 | `f884ae37c01816194b432f5e8f6505497415bedfc505f8feef5b93b242ff55e4` | 0 |
| ts/components/conversation/Timeline.dom.tsx | 46881 | `2e69df723da1b0c54e53621bb495cd7774fd2672801f35ce0ba2982426369727` | 0 |
| ts/components/conversation/TimelineDateHeader.dom.tsx | 1753 | `d1b63e58ab259c4c7944d07164817ad05252f643cd0c3c16342c738a3624346f` | 0 |
| ts/components/conversation/TimelineFloatingHeader.dom.tsx | 2587 | `3b8bfd0350af12ee949eef19a773ceabfd5c4ec93b628ab51c1274a33846938d` | 0 |
| ts/components/conversation/TimelineItem.dom.tsx | 19313 | `262ad9b10e06fbb5b52ab9d499c7d27ef2a9bfa5d0aae5fef5533a4c9a655816` | 0 |
| ts/components/conversation/TimelineMessage.dom.tsx | 18330 | `5c7bc07dc18d12f23fad4449091704cdb833ff6f1f99295f1ea1c93b157da1c1` | 0 |
| ts/components/conversation/TimelineWarning.dom.tsx | 1530 | `5feaa914b99184934b801e4019aabda26a65f894790932f12536d6ec1be7f61e` | 0 |
| ts/components/conversation/TimerNotification.dom.tsx | 2550 | `ed43f28a9ab7c4da6897200108194d5e0095f883891d4f438c096519baa72e9e` | 0 |
| ts/components/conversation/TitleTransitionNotification.dom.tsx | 874 | `e75d1e7a6e446358aa861381f109d1bdfe9ee1da7b8d4488b881c1ef78bb25b1` | 0 |
| ts/components/conversation/TypingAnimation.dom.tsx | 1254 | `e646617275c8b7c0aae864afa180b45bbfe03eb31139ff44e8cb84d04fa5d775` | 0 |
| ts/components/conversation/TypingBubble.dom.tsx | 11534 | `17d9d7a16948db88ca3f4b38d3ec66ed63836a5300a521922626154c637056c4` | 0 |
| ts/components/conversation/UniversalTimerNotification.dom.tsx | 849 | `298f7d4f050b288bbe433710934ab1b41339f49614aed75f03a39cc7e08efc40` | 0 |
| ts/components/conversation/UnsupportedMessage.dom.tsx | 2448 | `7f8f6263b7c450693a87e18728a5339bbe86c290331d0b6237cb2a7e86f83d0e` | 0 |
| ts/components/conversation/VerificationNotification.dom.tsx | 1777 | `4aaae2573553a41afe8025bb94130ebf3fdeec30700caa8b830695669776d06f` | 0 |
| ts/components/conversation/Waveform.dom.tsx | 1536 | `c9c5661a9b6ffddeb3e167ed86bd005d5c13f44d6548745ee6073b74be631321` | 0 |
| ts/components/conversation/WaveformScrubber.dom.tsx | 3429 | `9755463c3a52f2a349e31206dd3642a31f6a6762c9d7c1bfcb077ec6a40e46c5` | 0 |
| ts/components/conversation/contactUtil.dom.tsx | 2890 | `16f844c2e541f3e5bd6d14a1dfda613005e596967c700e3087c5b81a5deedc9b` | 0 |
| ts/components/conversation/conversation-details/AddGroupMembersModal/ChooseGroupMembersModal.dom.tsx | 15879 | `d65c521633dc93e9665d7ec87f170b121c085d65e1e2f8d7e8bd7b7581655778` | 0 |
| ts/components/conversation/conversation-details/AddGroupMembersModal/ConfirmAdditionsModal.dom.tsx | 2652 | `4d7a8b1b99b540d0aa2d5b5bf4a81442a0017eaf7f145bcef67c3a87cd293496` | 0 |
| ts/components/conversation/conversation-details/AddGroupMembersModal.dom.tsx | 7830 | `4cf37cf1921acfabcc8ce25c8d5be8cd770b2c57ff35b92c3a6a69c9dcadecae` | 0 |
| ts/components/conversation/conversation-details/CallHistoryGroupPanelSection.dom.tsx | 3435 | `3be7858266fcbe63eaac887366f8ffd3af7a5e93c2f73d0b6fb23eca60069b3b` | 0 |
| ts/components/conversation/conversation-details/ConversationDetails.dom.tsx | 29410 | `400c624d01ca30c9969cd387af2c7af3390bad8d85fa36aa9494466d8fe690a9` | 0 |
| ts/components/conversation/conversation-details/ConversationDetailsActions.dom.tsx | 12159 | `ea1c095acc7f306e5a01fd88b1f7640770f6d89a9832b044b635f7fddfd78a55` | 0 |
| ts/components/conversation/conversation-details/ConversationDetailsGroups.dom.tsx | 2468 | `246b43313066747ee975739468d6c4babb967a521975d735b2b74681a86db35e` | 0 |
| ts/components/conversation/conversation-details/ConversationDetailsHeader.dom.tsx | 8562 | `3eefb3b91c854a9ef783b301dfd90839d9766f18bfcaba75f3aa4a9d5c6a522c` | 0 |
| ts/components/conversation/conversation-details/ConversationDetailsMembershipList.dom.tsx | 9318 | `e743ff1cf5b13875f966676d4e4c4a0d3204a6cadcf2d51584bb0b334cc7c5e4` | 0 |
| ts/components/conversation/conversation-details/ConversationNotificationsSettings.dom.tsx | 6564 | `21d2930ab179e2affb7c1c7a13a07da04f9a152af316657b656e4b40ca3823b0` | 0 |
| ts/components/conversation/conversation-details/EditConversationAttributesModal.dom.tsx | 8568 | `419fb00d54d256c1c1b45a9d7a65ba9ea3bbe69a7919f025467ad58bd1c261ce` | 0 |
| ts/components/conversation/conversation-details/GroupLinkManagement.dom.tsx | 4855 | `472da16e3e375bc2c91d4e257d93514bca33cc9034f07d40ac65b7898d6dd63a` | 0 |
| ts/components/conversation/conversation-details/GroupMemberLabelEditor.dom.tsx | 17683 | `7a79de6601abb91043949aca7b6f66e10e76f884120162c412bf743aacda97ab` | 0 |
| ts/components/conversation/conversation-details/GroupMembersSearchDialog.dom.tsx | 14739 | `1523b45452188bd98c237163f4526818bbff1bd5b89a887c6e74372636553d8e` | 0 |
| ts/components/conversation/conversation-details/GroupV2Permissions.dom.tsx | 6774 | `91facd6e912119ebb5454ce25ef7e5924de6d6000856f7c842b73b92120660f2` | 0 |
| ts/components/conversation/conversation-details/PendingInvites.dom.tsx | 16899 | `148c52a6000dfddfe0b502df99258dd9389d1eae628bbc9621c6a12669a90b63` | 0 |
| ts/components/conversation/conversation-details/WhileMutedSettings.dom.tsx | 3671 | `9cd36d858f1eed1ee559a24544a93863e44197266ed012cd08282b132a0e59c9` | 0 |
| ts/components/conversation/conversation-details/util.std.ts | 155 | `785921b7fd8f760fb0f1098cc6f81f0e7e39634782f32216a58e0a2a5bc2bce0` | 0 |
| ts/components/conversation/media-gallery/AttachmentSection.dom.tsx | 3933 | `1d6c52156e7250c20fc3aff6fbbc1739eaeb7b66ce6481d77b1f8d4ce029bb37` | 0 |
| ts/components/conversation/media-gallery/AudioListItem.dom.tsx | 3974 | `89170fadd6245c7934524d18405d4e3796fe230f6fab8b25c6587ce5e6ac12a1` | 0 |
| ts/components/conversation/media-gallery/ContactListItem.dom.tsx | 1956 | `b98651913643a84f93d0911db392a395b26bdb165d2935439bbf8a4bb33330c7` | 0 |
| ts/components/conversation/media-gallery/DocumentListItem.dom.tsx | 2067 | `d861a4ffa4ff26d5d76bd3dc46ca3a8bed818d9687e5a5007a703d760cb1c452` | 0 |
| ts/components/conversation/media-gallery/EmptyState.dom.tsx | 1723 | `344f04c64d139f4021881ffa9399ebd0230711b7fd65a98348f2d4dacaa05912` | 0 |
| ts/components/conversation/media-gallery/LinkPreviewItem.dom.tsx | 2968 | `1b75094dfa92eacb2e68d102bd68647603591ed393eb1bd19669e77b91887549` | 0 |
| ts/components/conversation/media-gallery/ListItem.dom.tsx | 4855 | `10f04e79fb27a2094a5e5eb98c573067afbd0b5f9ad19afd06eadef13c0ba7fb` | 0 |
| ts/components/conversation/media-gallery/MediaContextMenu.dom.tsx | 2923 | `5e41fedd6724137af346fe1cd356e400d9cc517df41d51210990f139644132f0` | 0 |
| ts/components/conversation/media-gallery/MediaGallery.dom.tsx | 10150 | `a765f901c60aebe03abbbe7cb0b8e6b41facb5ed5666d456d8827ee9dbfc02a2` | 0 |
| ts/components/conversation/media-gallery/MediaGridItem.dom.tsx | 5422 | `96e1f99c1c01ec0c2c3963f2ed4e3c72ab3e1ed20c0371cd8195b2900d9ba720` | 0 |
| ts/components/conversation/media-gallery/PanelHeader.dom.tsx | 5310 | `35d88d84586bcc51df6ee7ca6c5b4c493f7e9cfcf7efb96e7d9d054bb5547b3f` | 0 |
| ts/components/conversation/media-gallery/groupMediaItemsByDate.std.ts | 4288 | `0df79eba8bf7a173f2627decdcdcf4d61c53a6e2555aa62066bd5d1c02cf753b` | 0 |
| ts/components/conversation/media-gallery/types/ItemClickEvent.std.ts | 373 | `d888b4ad37d723b778fd9c42a30f1bf05b5c5ded933433782a48be02cfba3e64` | 0 |
| ts/components/conversation/pinned-messages/PinMessageDialog.dom.tsx | 10468 | `3baa62f5a3aa974b36d7f6e418d618ca03a417b89ceed9b387a5ee35837a3ba5` | 0 |
| ts/components/conversation/pinned-messages/PinnedMessageNotification.dom.tsx | 2108 | `1291af5fdf5d00d8ad4dd894cc49e4d03e59df505fe61fe667b5f8fc2f6b43e8` | 0 |
| ts/components/conversation/pinned-messages/PinnedMessagesBar.dom.tsx | 17941 | `2319d041f6c0b3e0e819fa668825b22c82de7820154eb9e072c2640c6622d305` | 0 |
| ts/components/conversation/pinned-messages/PinnedMessagesPanel.dom.tsx | 6186 | `b2a19d200bfc9ce7384b5bdf41d1323b4592b436b7e9b9c7b3ad537b7e5abb96` | 0 |
| ts/components/conversation/poll-message/PollMessageContents.dom.tsx | 13435 | `1445ad524b6050c348b3374ee154fa72042e3fbf01f45f834835c18738568f50` | 0 |
| ts/components/conversation/poll-message/PollVotesModal.dom.tsx | 6078 | `f1171484405ee4a91f8d40c4d2116448a07ae0452e6047b6744919b2d7f52ddd` | 0 |
| ts/components/conversationList/BaseConversationListItem.dom.tsx | 12109 | `1fe05af0f5534d589bef6f1c0bf3e991029e871fe152519cc78684a951103493` | 0 |
| ts/components/conversationList/ComposeStepButton.dom.tsx | 1013 | `d8ce1a34990dfa47fa46bc2d7b86bdcb285667122bbbbd3adad7977cc41db2b6` | 0 |
| ts/components/conversationList/ContactCheckbox.dom.tsx | 3193 | `d92565630d15bd857b659b6dd42e71b29bd5461afaa41f3fddb50cd2473f3e75` | 0 |
| ts/components/conversationList/ContactListItem.dom.tsx | 8959 | `8e1633432fc95afdc847502f1813a55d962561d6d68d643da8403778c6f1c6fe` | 0 |
| ts/components/conversationList/ConversationListItem.dom.tsx | 9119 | `a91cfd16bf1ba6bd3d4a4e9b012a408076ce95e6ad9bc747bdf901fcb5c5b34d` | 0 |
| ts/components/conversationList/GroupListItem.dom.tsx | 2167 | `9b04b5e6cc6e1fcf72045df9be7f3b3bed6783c44da9abb42ccd56470e3e1188` | 0 |
| ts/components/conversationList/MessageSearchResult.dom.tsx | 5271 | `52e2e55b1d162869239e48a6e78fc5dc5f24938f9e21e7950f07333a160977c8` | 0 |
| ts/components/conversationList/PhoneNumberCheckbox.dom.tsx | 3723 | `537e30ce86fb028e57a66d27724b99ab60124b0a652366fd1177bb9b4fc1f439` | 0 |
| ts/components/conversationList/SearchResultsLoadingFakeHeader.dom.tsx | 305 | `21da9ccc1a6af7bc929cf68c5d7382838daaf4964e10edb3d5505b640bc89eb1` | 0 |
| ts/components/conversationList/SearchResultsLoadingFakeRow.dom.tsx | 702 | `1563c8217d7956b19fb6fe88c3724e872c8ede2e7836c01c287ef8b9f3151301` | 0 |
| ts/components/conversationList/StartNewConversation.dom.tsx | 3287 | `0e91f9746277b5f77992dcd7d97989e4cc6a61739e9e9b22b92309042c8d5fe3` | 0 |
| ts/components/conversationList/UsernameCheckbox.dom.tsx | 2473 | `6b376759b10955f5809ce8a80074f0885e3ed1f51639ffb9abe6ab160b55cd44` | 0 |
| ts/components/conversationList/UsernameSearchResultListItem.dom.tsx | 2051 | `d1899c0db581a9c1f51b4fe713c0e68891002d74715501e6e50dbbd27cdddaec` | 0 |
| ts/components/fun/FunButton.dom.tsx | 2132 | `772a60cc9e08d27575f0650d6cce66d29e2fc872f9ce080c15a0b48f7ef6b055` | 0 |
| ts/components/fun/FunEmoji.dom.tsx | 6243 | `1880965e86b36b534c827eb4c28c9e4037a9a9b01faf1e0d090e8a7315fe8c33` | 0 |
| ts/components/fun/FunEmojiPicker.dom.tsx | 2167 | `a18558f15e8002b22001fdea278f93412545de7833da1f53f656e9ccadd03f1c` | 0 |
| ts/components/fun/FunGif.dom.tsx | 5271 | `93673815e9b3b3e2dbfb1eb39b682e2889f38ba3bac5ef72e0207bcb1c8d08e8` | 0 |
| ts/components/fun/FunPicker.dom.tsx | 8452 | `3c36f069b19797ab32b141a50787e8f2c1e81b64246b99b31247b08710685ff0` | 0 |
| ts/components/fun/FunProvider.dom.tsx | 6085 | `1ddeec5c948914b364ccac078a5e7f2d7d3c85db6492ffeeb710a5f46826ab53` | 0 |
| ts/components/fun/FunSkinTones.dom.tsx | 3125 | `49cea21a0fbe79e24564b3522ed365ccb9ea74e2db1e32950c75cd3cb5b820d2` | 0 |
| ts/components/fun/FunSticker.dom.tsx | 692 | `6c5662bea01f13cf304c2c2725e26fd889d79a8bfb72944a8c67e1a51fe24ab0` | 0 |
| ts/components/fun/FunStickerPicker.dom.tsx | 2121 | `d5a06294c55097dbe932cd9972efa921df7afb2b9c2d02a58a495b5e49ff9663` | 0 |
| ts/components/fun/base/FunErrorBoundary.dom.tsx | 1943 | `fc6428865bf42a7b61893e12d9f03f1c716656d8dbb1618e0fbf295a364aac32` | 0 |
| ts/components/fun/base/FunGrid.dom.tsx | 5607 | `30729bb15aa3fa4a1501224ac4ac458e83d62a69b8e722b78da3f27cbae21d68` | 0 |
| ts/components/fun/base/FunImage.dom.tsx | 5716 | `522540d59e8450617374895de2bb23451639a2c7c8b0d264a8e2219c99e1a776` | 0 |
| ts/components/fun/base/FunItem.dom.tsx | 3444 | `d7e6d1e2c9ec57a62c15de1173a07217e15404f349a56943f8275a6f7b00e751` | 0 |
| ts/components/fun/base/FunLightbox.dom.tsx | 3988 | `972d8e8efd1bb8451f6cb4bd79d58e15f2a16a0fb2366cd5bb3c5e0ee49a006c` | 0 |
| ts/components/fun/base/FunPanel.dom.tsx | 961 | `cd930b7a8346019ff35b4e8ebc2f711bccc6e7741e3f6e359d188cebb299971c` | 0 |
| ts/components/fun/base/FunPopover.dom.tsx | 1568 | `9b9bd54d27fd6771fb746cdb3a89f09e84e63d59852aa99dd4bb92310e2bb2ef` | 0 |
| ts/components/fun/base/FunResults.dom.tsx | 1363 | `60709b8687d57e5a13e500c62cb1486b9d391f91a3d1ac71d60db9b7ea5e95bf` | 0 |
| ts/components/fun/base/FunScroller.dom.tsx | 5177 | `0ba372b4291ce5bf08d848bfa2c0c2bf532524631b954788efba6fac23a125ec` | 0 |
| ts/components/fun/base/FunSearch.dom.tsx | 1756 | `125111d18041a43519ae0024bb38a669b07829ef3ac6a2a467d5c724e7c430bd` | 0 |
| ts/components/fun/base/FunSubNav.dom.tsx | 9180 | `e95f7c00acf4adece4d2cfa7bb8dc6a93dde55cd3e334037d965b53e35729cbf` | 0 |
| ts/components/fun/base/FunTabs.dom.tsx | 2808 | `b43ee04c33f123757618e2f297140f90cd3ee73f150becdde4b12e4d427020a2` | 0 |
| ts/components/fun/base/FunTooltip.dom.tsx | 1730 | `d9a582516424e2424432d0ad426ca08500401e231dd6420e7e5b3172c398c5a8` | 0 |
| ts/components/fun/base/FunWaterfall.dom.tsx | 1300 | `b7e764ea4bd1a91ce111dc73a89deed1cc49a36619ebcbd74f5f66083d4bc33c` | 0 |
| ts/components/fun/constants.dom.tsx | 1910 | `e586831eb6c513f7044f5402e66cd525b1fbcd2251d8fc9b58d7d00410b57454` | 0 |
| ts/components/fun/data/infinite.std.ts | 5437 | `f4e4c4ebe0eea82ab9dfc5474ab6b30210d9af8920344dc66c16897b9275343a` | 0 |
| ts/components/fun/data/segments.std.ts | 4440 | `a8afdacd51a219edd553f4e7e12b97742767a57edf06817e6ddc0899bde22fce` | 0 |
| ts/components/fun/keyboard/FunKeyboard.dom.tsx | 5583 | `23e1be3791fb36e8fca02960987085852d40257cf13a2174e5f57375518f79e8` | 0 |
| ts/components/fun/keyboard/GridKeyboardDelegate.dom.tsx | 9017 | `a5ab54409d256301ea340a64c15586c6c9de90bc26ce478bcaaded3bdf258275` | 0 |
| ts/components/fun/keyboard/WaterfallKeyboardDelegate.dom.tsx | 10195 | `a99148de942766c48db90d52da786173796931751fe9d7a33f91695aa995530b` | 0 |
| ts/components/fun/panels/FunPanelEmojis.dom.tsx | 25976 | `a83b983080f1265d2cde79725a6e532754f1d14e874827f81030af7e3449744b` | 0 |
| ts/components/fun/panels/FunPanelGifs.dom.tsx | 24255 | `e5648517a970fe2c1e6c424421b649805838050a81d67ab539baadd53edd0730` | 0 |
| ts/components/fun/panels/FunPanelStickers.dom.tsx | 24434 | `69efa0feafa0292e79b75fe148ceaeb8ef4144b10e117e38db0ef0391895adfd` | 0 |
| ts/components/fun/types.dom.tsx | 229 | `2dd13a8b5b09bc384e10c8a0ce96de8538a656a367e1727c9b5dd9059313b652` | 0 |
| ts/components/fun/virtual/useFunVirtualGrid.dom.tsx | 11839 | `919202d1e00d613c0d16d826b5a26ea22cc93f7f0b487597ab53d316c636cf75` | 0 |
| ts/components/installScreen/InstallScreenBackupImportStep.dom.tsx | 8979 | `46853b35161ad6df55a5750aa542be3fd33cfef8f92a6073fc89aceaa2c171ed` | 0 |
| ts/components/installScreen/InstallScreenErrorStep.dom.tsx | 2506 | `2bc6918b4b837d7406441754a911f71646fa3dbaff70b8779dbd889d6b418fb8` | 0 |
| ts/components/installScreen/InstallScreenLinkInProgressStep.dom.tsx | 835 | `8d1246481ec52574fca756e9a105602acde10135c6ce313dac972a66a78c8be4` | 0 |
| ts/components/installScreen/InstallScreenQrCodeNotScannedStep.dom.tsx | 11175 | `a080ac96e1a3ffd2f3b58688b60f97d034312718e35f1fadd70f6204f3027b74` | 0 |
| ts/components/installScreen/InstallScreenSignalLogo.dom.tsx | 241 | `baf81558911df060f4fd19f2cccc650a0dc781e6939c4d8977f012641d186eca` | 0 |
| ts/components/installScreen/InstallScreenUpdateDialog.dom.tsx | 10726 | `0e685d3a11bed87f99849bddde28d0ee7d81b4ce7bdffaa7519f5e9608a38edf` | 0 |
| ts/components/leftPane/LeftPaneArchiveHelper.dom.tsx | 8168 | `430b4c5df8662fecd6c36bca47de2433785be338118d8e6091956769d9483538` | 0 |
| ts/components/leftPane/LeftPaneChatFolders.dom.tsx | 12492 | `261ca52f339e63ef7d1618d39a18accbcc287848641887bbc394de2e88e5cf2a` | 0 |
| ts/components/leftPane/LeftPaneChooseGroupMembersHelper.dom.tsx | 12132 | `41fa0591f03a7d7a91f4f4d5a641e2edd4d6529431c1cb791d961e62564b3d62` | 0 |
| ts/components/leftPane/LeftPaneComposeHelper.dom.tsx | 9754 | `aa0915f338a75ba8b061218e75c27b3368e8eef01112bbe3ee84c28d2ec52405` | 0 |
| ts/components/leftPane/LeftPaneConversationListItemContextMenu.dom.tsx | 13770 | `33ffd507b2b3bf3ef889a5bf3de72a723568ea9dd69343baf704d0097bc51f0f` | 0 |
| ts/components/leftPane/LeftPaneFindByPhoneNumberHelper.dom.tsx | 6947 | `05c852fb21c60a7f0bac091638108d8589a4323a8b440fa1340854619f017a31` | 0 |
| ts/components/leftPane/LeftPaneFindByUsernameHelper.dom.tsx | 5806 | `f51111edaac6a4a209e03cb36be7f6b272f23d44d1049e1efb2f3745b53b452c` | 0 |
| ts/components/leftPane/LeftPaneHelper.dom.tsx | 4403 | `c68bc611d9ad8d60959aa694f0a2349224f9ac527bcad14aeee00b8f6a1e066a` | 0 |
| ts/components/leftPane/LeftPaneInboxHelper.dom.tsx | 11441 | `112a1224f14d86aab68ed37d29de17688a12c83b414fd92e56765d3912965e91` | 0 |
| ts/components/leftPane/LeftPaneSearchHelper.dom.tsx | 14726 | `627e792beb9f081690a3c05b1f69f53d7a5e3a8b1cdc4e0e00cdafa56bd9dc26` | 0 |
| ts/components/leftPane/LeftPaneSetGroupMetadataHelper.dom.tsx | 9584 | `6f207347106189d8e01566426c7359f4edf256181a6e8f9479b4f75c01e3cea4` | 0 |
| ts/components/leftPane/getConversationInDirection.dom.ts | 2338 | `8b1cd50e1fc7acfe9c1ac1f6508f375f074e0d554ac5a70acf1f5909fa1b57e4` | 0 |
| ts/components/leftPane/handleKeydownForSearch.dom.ts | 1025 | `3b99bd0876259643fd95e72080d28ad5594a786cef4acd80ae0c7af12c5bb900` | 0 |
| ts/components/preferences/LinkedDevicesOnboardingDialog.dom.tsx | 2164 | `2c1060450e15d693e2fce54e31f7aa368b357302c41735ea3a8f61afe850d794` | 0 |
| ts/components/preferences/OSAuthErrorDialog.dom.tsx | 1135 | `ec8f851cc2a871145e582500891b92548a71e0bdbd44f628427c21d9d37c094b` | 0 |
| ts/components/preferences/PreferencesBlockChooserDialog.dom.tsx | 7439 | `8072bb491c5055c1031159ed223626bc8a4e1477becc545d0603d84255685ffd` | 0 |
| ts/components/preferences/PreferencesBlocked.dom.tsx | 6316 | `97a27ad19ec6fb203be24568fed4f2bd39bb37f6f5a47a89a10fcdb08f44ec56` | 0 |
| ts/components/preferences/PreferencesList.dom.tsx | 1034 | `832ad092ca1e9223411fd4ecae859d7ad551c9c714b0e83d71f9b6ff1b69ff79` | 0 |
| ts/components/preferences/PreferencesSelectChatsDialog.dom.tsx | 10023 | `5db071c28c2d543627bcb2abfba9d163c3adc73d6644a7e4d055c04a5f55c90b` | 0 |
| ts/components/preferences/SignalAccountKeys.dom.tsx | 4655 | `e852283e038c738854c84c72f235d988777a11422262c0922489759bab0edd0c` | 0 |
| ts/components/preferences/SignalAccountKeysButton.dom.tsx | 2871 | `730bd5bb5130ad7f91d557a05fadab38075d11302f840d60cbc326ce00479597` | 0 |
| ts/components/preferences/chatFolders/DeleteChatFolderDialog.dom.tsx | 957 | `d51b4a555c91af74525209811f24bcfafa820797123b0c3b1caed3d13083cfe7` | 0 |
| ts/components/preferences/chatFolders/PreferencesChatFolderItems.dom.tsx | 3014 | `59f8a10af198085a6c188349841018dba28a8fe8d7f773933e44176a933cb44b` | 0 |
| ts/components/preferences/chatFolders/PreferencesChatFoldersPage.dom.tsx | 16232 | `f9328a229c043d58f6ccadeee4f76efb40af37a7a389850dd3cfcedf748b8208` | 0 |
| ts/components/preferences/chatFolders/PreferencesEditChatFoldersPage.dom.tsx | 21441 | `0dbff282190083c9629ed4533697ca0981fa68fa02c94051ec3dfd522465ecba` | 0 |
| ts/components/preferences/donations/DonateInputAmount.dom.tsx | 8088 | `0dc1450c44612d44a600f7b9b19b41ae720bb4200d003f455a1f1b8779fdfe13` | 0 |
| ts/components/preferences/donations/DonateInputCardCvc.dom.tsx | 2085 | `05ff0de02314e420ca73a811d3b458ee7e47ed997490b3520c1d9c54ab699f03` | 0 |
| ts/components/preferences/donations/DonateInputCardExp.dom.tsx | 2727 | `bc64639566c87bdb2aa8ef8f31860229a891d7ad3ff5ee20fc3f42b965603b94` | 0 |
| ts/components/preferences/donations/DonateInputCardNumber.dom.tsx | 2060 | `7e966cc94e78932ecdca3f9ec8f657fe6d66d610c2804bbae33e4e8abeff5dde` | 0 |
| ts/components/preferences/notificationProfiles/NotificationProfilesOnboardingDialog.dom.tsx | 1781 | `58376d0284eda5b13df6aa5469daaf83bad43e76e7205d56cbcac602b9fca001` | 0 |
| ts/components/standaloneRegistration/StandaloneRegistration.dom.tsx | 12916 | `2fb26fb79d2e82102cb14b2151c576b3ed9ad591e660d005db9828267f6cbd77` | 0 |
| ts/components/standaloneRegistration/stages/AccountLocked.dom.tsx | 2051 | `c63b0c49c09a0fe5c1d1eb428ada518de1fbc6671998ec112918b6f1cf712d6b` | 0 |
| ts/components/standaloneRegistration/stages/Captcha.dom.tsx | 9639 | `47078a44aba2c4cf0f34185823d16e200817b5c12ffa16bf9ec8fdce27518334` | 0 |
| ts/components/standaloneRegistration/stages/CreatePIN.dom.tsx | 8941 | `0977338aa597d62df7c427ed1af814481a6ca9f5759478d759dc933342e18d4e` | 0 |
| ts/components/standaloneRegistration/stages/CreatePINConfirm.dom.tsx | 3202 | `55ebb95acbe48e9fa8883274a8291a92df30f2b37f7f4cf636aec7db81da0991` | 0 |
| ts/components/standaloneRegistration/stages/PhoneNumber.dom.tsx | 7381 | `6ac5ef649c878212178ad1ce179b4d339f7f421e29f50e5b5d4fda27a0f4e13d` | 0 |
| ts/components/standaloneRegistration/stages/ProfileEntry.dom.tsx | 12874 | `10a2784c0d1763d0fad114454911cc569c381afb2b4d392b103eea90bba9a6c5` | 0 |
| ts/components/standaloneRegistration/stages/VerificationCode.dom.tsx | 26723 | `fcc2b228f991b2034ba9a59fb2fcf842bf26dc04c8e016ee5a584b32f118ec13` | 0 |
| ts/components/standaloneRegistration/stages/VerifyPIN.dom.tsx | 18309 | `243e9db81734a3eab2f89debfa65938f7d84e42c5b648ec81ef57eec464ffb34` | 0 |
| ts/components/standaloneRegistration/util/ConfirmPhoneNumberDialog.dom.tsx | 1401 | `2d0f9ce09b867e8f0b202b0368cae4180457087522d5bb9722f01c84a1658807` | 0 |
| ts/components/standaloneRegistration/util/StepComponents.dom.tsx | 2889 | `e60d4cf0e341eca19813b7eec43403e4485ca9fa7809a693ed51a5ad89df61ae` | 0 |
| ts/components/standaloneRegistration/util/timeIsPast.std.ts | 259 | `d196a5537c93af69e41552dbcf51e46c59aeb89efbdbc61a721d4c11a290986c` | 0 |
| ts/components/standaloneRegistration/util/useCountdownDuration.std.ts | 1300 | `e8bb0872fad6a2e67d50bd4576b41e724e77642205349cba23d1dd69d9349b0d` | 0 |
| ts/components/stickers/StickerManager.dom.tsx | 10070 | `27f5edcf74070b41aadae5a73783c60caaeec1d06f6118007af588d814f07df9` | 0 |
| ts/components/stickers/StickerManagerHeader.dom.tsx | 3185 | `99b1b14abefe16152514b1f83766c724124b50f13b934c2adc72b27aaed73c99` | 0 |
| ts/components/stickers/StickerManagerPackRow.dom.tsx | 7293 | `d867f2fa43f60627009b80cbe2ea798cc1fa02cc82a5872e4addbaa51cf632f7` | 0 |
| ts/components/stickers/StickerPreviewModal.dom.tsx | 9020 | `92ec11ae844d834f2738a15bed0b5c9f02fce85f31c65fee5c4ac2eca7b302e9` | 0 |
| ts/context/Bytes.std.ts | 2370 | `414e94c00e419a3c6ddb584d73f7e5cc9c385a6f97020051eea16569f7ff37be` | 0 |
| ts/context/Crypto.node.ts | 3507 | `1943ba3b9d2f7e7c093aa4fbbcb6bee9ff5cb846ab01a567c66b47890910a0c1` | 0 |
| ts/context/Timers.node.ts | 972 | `ce840f6ebf6cb967b31d302ee9a87b285c00d692d93185124f01fc2098a55e78` | 0 |
| ts/context/activeWindowService.preload.ts | 326 | `2fa00cb07d5b54dde3b802167692ce43e9b75dbabf2e42dca5e909866c5144e3` | 0 |
| ts/context/config.preload.ts | 290 | `42e2953d7904675869b70bf5cae11edcb926c7f01fb8e221abc358d0afce067f` | 0 |
| ts/context/createNativeThemeListener.std.ts | 2119 | `3aa7ac1442bb04ff0b981c728caf7f645614ff15f4ad86f1b6e4f93b9f61f757` | 0 |
| ts/context/environment.preload.ts | 381 | `51d060789371c70425e94f27b53e2adceae100f64b43c58cf362dcd76f1112b7` | 0 |
| ts/context/i18n.preload.ts | 619 | `70e01960eb5b8790212acbfbeb27edfb1aa9c97cb40694f31837299485965891` | 0 |
| ts/context/localeMessages.preload.ts | 357 | `51901bd6e3b11c6b7b417c1de35da5c25b72881cd874b09f14060c82bfd5e77a` | 0 |
| ts/context/waitForSettingsChange.preload.ts | 620 | `981f7091c29bb7da6b660a976bf6b834119674381d6b71d22f252d8a77237415` | 0 |
| ts/conversations/isConversationTooBigToRing.dom.ts | 610 | `f7e6adb15a838be4f756c1b8d86f001302bf15a0b6655355de7dd3a2792ec430` | 0 |
| ts/environment.std.ts | 1807 | `96573d376ed4d57e16592f488cb2f629a91e96242c9f19761866b591d0f1c41b` | 0 |
| ts/firstline.d.ts | 305 | `ea8718502f0e79bae822759ce0ef0de485b0c7ab7b524e6bead4cc483e18060d` | 0 |
| ts/groupChange.std.ts | 27618 | `6924177ca0a4a5cc8c9b785e8295ed63f54843fdc42e058de569637a300e2ea2` | 0 |
| ts/groups/joinViaLink.preload.ts | 15287 | `dcbb19019453af0e897c0209d7da877071c300a8ca58a7acc254bcd3ef438787` | 0 |
| ts/groups/limits.dom.ts | 854 | `542a6b92a6defd85dc888fb351e41bb876167e12d1778a75f693260ceb09a16d` | 0 |
| ts/groups/toggleSelectedContactForGroupAddition.std.ts | 2001 | `dc0e7977a9192374a48d8f775e76de24a7eb7e8d0dd7c97abdb188677a39cfba` | 0 |
| ts/groups/util.std.ts | 518 | `f05342a4626efbe3112bd6604f58f4097a29804f462e9265af7fce0afe22bb4b` | 0 |
| ts/groups.preload.ts | 226625 | `706bdc5068e65d42e9d3ddc6e34ad6e189e2ab070f0b0d897252f99a06b8ecee` | 0 |
| ts/growing-file.d.ts | 386 | `ce8a143eee6beaf51ee30f6392e9695a0989624e04fb8c3606d032fd78f520e4` | 0 |
| ts/heic-convert.d.ts | 280 | `a43ef85fe765f423566adfaa7667207b58ddb013391807631f9f598cf7be7f78` | 0 |
| ts/hooks/useActivateSpeakerViewOnPresenting.std.ts | 1358 | `770ce6f03867106cb6727af3fa334c669689901156cc86034a56b49b4702f9ed` | 0 |
| ts/hooks/useAnimated.dom.tsx | 2290 | `b6b255e239cf9023e3fed76b877d1d63995dc883b2ab1f9629297957dc53b885` | 0 |
| ts/hooks/useAttachmentStatus.std.ts | 2781 | `536df0c57cc2880bef6816e944745b39e7b6c7bab201269ea6f985a045925e14` | 0 |
| ts/hooks/useBoundActions.std.ts | 714 | `6e4cafac497529712f5d81be1d15f0e6f5654f56037125376322ce2e25a54609` | 0 |
| ts/hooks/useComputePeaks.dom.ts | 3193 | `4c9c0b4a8548dc0588448b4f9ab59ee5bb2547d663b1e6fa4e30a43c3723ddfc` | 0 |
| ts/hooks/useConfirmDiscard.dom.tsx | 2846 | `a7c3ac82b4f260f7dbdda8ebf11ffed2b807df912153710216bf38b232f48492` | 0 |
| ts/hooks/useDelayedValue.std.ts | 1302 | `caa349132fc9c0cfb085e2d8890f0e352f16d4546566cd56973ffae488953832` | 0 |
| ts/hooks/useDevicePixelRatio.dom.ts | 621 | `9b840dfc6cd3337c6ae2a7c23b25422bb96d24c87e2241ad711298e6b263fc0f` | 0 |
| ts/hooks/useEscapeHandling.dom.ts | 604 | `8afa11104724165356c7af566b589270293a41ed664d441146b48113d9cec8b8` | 0 |
| ts/hooks/useHasWrapped.std.ts | 1542 | `2d98ccd73f193dc4a0562a2c7c4676624f33e12526d3bc2b028644430591ceb1` | 0 |
| ts/hooks/useInputMask.dom.tsx | 1870 | `72a5f37a8561db21c0b4a58974cd9afbc6ffcedfe9a9f0f4403a4b1b15242f67` | 0 |
| ts/hooks/useIntersectionObserver.std.ts | 1749 | `3ab053d4f4b2cc47a22ab7cda4994a25d20bf3233b8070f822fc4a3748b9c69d` | 0 |
| ts/hooks/useIsMounted.std.ts | 807 | `4dae64d44b02f91c213acf7fce7967f0de650f7304dba20bec5229368385b70f` | 0 |
| ts/hooks/useIsWindowActive.dom.ts | 606 | `98a08df0ac16e7d292c0c907b65529797059ada723e499145365f19442107a28` | 0 |
| ts/hooks/useKeyboardShortcuts.dom.tsx | 1256 | `6851224270cc908cd26708018888e43d59fc963f0a24b2d18ba7af037d4bfd4d` | 0 |
| ts/hooks/useMinimalConversation.std.ts | 3071 | `2cffd083eca03c2a4c80e80e3ab3d97816e8974945c36fb8539d6c3e0213d403` | 0 |
| ts/hooks/useNavBlocker.std.ts | 2284 | `a4556aeeb6e3e2e3fbeedaa324ce4bc8989e6b32d73ab254a3bdc205d63182a8` | 0 |
| ts/hooks/useNowThatUpdatesEveryMinute.std.ts | 924 | `a2d4975ce6dd80ddff2d5eb22f23791e7e374db7a4d30f5b8cfa189d40eb2c32` | 0 |
| ts/hooks/usePageVisibility.dom.ts | 622 | `40c2f9ef4ec9dbf65fa010d046c4ea8b7d5aff450100e3837bc099831db46e29` | 0 |
| ts/hooks/usePortal.dom.ts | 541 | `524cea8975e089f3e05de2df7da1d57c43d6b87d7bc64d57203c9760910b15eb` | 0 |
| ts/hooks/usePrevious.std.ts | 1666 | `23fc545cc6239d62fbf14dd63ec505e005a500441c9437a95af4a0de9b70f3a3` | 0 |
| ts/hooks/useProxySelector.std.ts | 712 | `2abbba63cad2e962d400b63fb1b0a7ff6f08bfa914f2268bc5f2b5d2f0528057` | 0 |
| ts/hooks/useReducedMotion.dom.ts | 756 | `6f2e6b18ba48652cfae4dc93cc6eb57fb330988ff5d6a1dbd3591ab1421cfebf` | 0 |
| ts/hooks/useRefMerger.std.ts | 313 | `258e5260469de17dcdbc91906bdf03a6f7e1c35c1a94445f42ce0dc37ac3421d` | 0 |
| ts/hooks/useRestoreFocus.dom.ts | 2919 | `b79925c02c6f9a19bf148572938358dce73d836834e2a4448c64154190d480cb` | 0 |
| ts/hooks/useRetryStorySend.dom.tsx | 1820 | `f072de4b4860939bb06773e57d23c3fe3432e084dbbabc7ea524e1f0408f186f` | 0 |
| ts/hooks/useScrollLock.dom.tsx | 2255 | `3728caf9a6d270ec90b95f76d2bb55d9033ddf613c2dcdff9aaf1044a8aa33e4` | 0 |
| ts/hooks/useSizeObserver.dom.tsx | 7217 | `3ec310bb95cb66b5e7681fde03ba6e938ba0963d801557c27686dcf837afd768` | 0 |
| ts/hooks/useTabs.dom.tsx | 2524 | `6b7163f198cab67c74e00c1a9038dd23d5233f28f3792e3e4a8a2dfc19cd1173` | 0 |
| ts/hooks/useTheme.dom.ts | 1564 | `9037ee1406c9ad3add9f420abc2e070374c68747861f694bc9670c7ccf153a2a` | 0 |
| ts/hooks/useUndownloadableMediaHandler.dom.tsx | 542 | `297e1f2540723612ca1d5425a2e5b6e4d08a11a3494680e408a2e678f238e232` | 0 |
| ts/hooks/useValueAtFixedRate.std.ts | 462 | `44a575681babd3da08f8ad8459f88f46ab020883c6eef0a8e8a1b8cddbbc0087` | 0 |
| ts/indexeddb.dom.ts | 1741 | `e8d8677b66da242e7860150804575bd601617cea5426c4ee5060ca77a5c689d3` | 0 |
| ts/jobs/AttachmentBackupManager.preload.ts | 18399 | `d0f7ef6a1431585d42bf253c408bad9d38ada8c8ae4faa529a6dc572ec0fa711` | 0 |
| ts/jobs/AttachmentDownloadManager.preload.ts | 34005 | `9d0fb3839b00e76bd4c3fc90deabe422d67402a9e8ec8cfbcbb397e7806a353e` | 0 |
| ts/jobs/AttachmentLocalBackupManager.preload.ts | 5202 | `6dd2df834d2988101d2af9098860e37af8106e5491e9058b847bf3450c2aa9fb` | 0 |
| ts/jobs/Job.std.ts | 718 | `1ff358d4721dbe16eb9329f930c243f56514b299653e16d143ffb2f93d231679` | 0 |
| ts/jobs/JobError.std.ts | 677 | `ea9b0d8a51507aed075c08a37aa06e6d01a2ec05940c2a9a4d41391d741919c5` | 0 |
| ts/jobs/JobLogger.std.ts | 1439 | `db46ecc3de841e45863f770fcd4b44e1ce44d14b01418789518012bcc89dcab0` | 0 |
| ts/jobs/JobManager.std.ts | 14884 | `2d87bd1c0237a1fe97b4af7d2eb3dc1352fe198a4c532bcc94c56cdfc9786293` | 0 |
| ts/jobs/JobQueue.std.ts | 11152 | `5d23aedafd6abd50bf03392972ed354c1dbc437f0dc18e83189f4d277d6e9afc` | 0 |
| ts/jobs/JobQueueDatabaseStore.preload.ts | 3486 | `0d93203f850e1045dbecdf6185ff30bc81cf3229b8bda4f8d901a44faef7a76c` | 0 |
| ts/jobs/callLinkRefreshJobQueue.preload.ts | 10083 | `832d7d04be96f87b96c0dc12f2ee50701529f05d3fd606cc525a21be735f9ede` | 0 |
| ts/jobs/conversationJobQueue.preload.ts | 38822 | `3be38d85713c1eb8a4c8170d0648039b13d690abc59cb6d3e69997fb8030c546` | 0 |
| ts/jobs/deleteDownloadsJobQueue.preload.ts | 3709 | `ea68713789f86b7f51e2f5c10b3fd358f5bcf22bc6c4b2415448dd0b7b9944c4` | 0 |
| ts/jobs/formatJobForInsert.std.ts | 552 | `1f1a20ebb2d896f2c75dc1eb8cb89d93aedc10370d0f049ff86925bd6dd66802` | 0 |
| ts/jobs/groupAvatarJobQueue.preload.ts | 2409 | `41364f296e7cbcd6bae2e4db8164c63bc371ad3ba721fa4cd6ba5d36437aa035` | 0 |
| ts/jobs/helpers/InMemoryQueues.std.ts | 612 | `cf315fbf394cdbbb49b9eea2d98f1f677e0f5fe2b99ba570cb45a261a83d6599` | 0 |
| ts/jobs/helpers/addReportSpamJob.dom.ts | 2343 | `87e80b0a21adfbe8fbb843c8a768e895f3084589290eaec3e19d984d4cb17c73` | 0 |
| ts/jobs/helpers/areAllErrorsUnregistered.dom.ts | 636 | `de7dcc15e382df9ddae6bf7366c6e974d48cc04fa04122144107b851620cdda4` | 0 |
| ts/jobs/helpers/attachmentBackfill.preload.ts | 14720 | `d130e394f860987060c0bd626d7111c6b66dc5c67a9a94d15404ce1e269f69d8` | 0 |
| ts/jobs/helpers/commonShouldJobContinue.preload.ts | 1776 | `97742b7e48f5ccd18b42f99604780a6bb63be068b2ea9f6143ae8b36d6da2c9e` | 0 |
| ts/jobs/helpers/createSendMessageJob.preload.ts | 7628 | `53d1163e3a306de77a88eb010d9db0a75336aa93a8da7943f8df2a5487edfc66` | 0 |
| ts/jobs/helpers/findRetryAfterTimeFromError.std.ts | 813 | `86913482128a834d8e85751b3013090373aa7d2a0567171eed936af1f94d50d3` | 0 |
| ts/jobs/helpers/getHttpErrorCode.std.ts | 846 | `da99c3975ce787cea1902b5743c5480ce96b5504d36041fbbdcdce82a72f43be` | 0 |
| ts/jobs/helpers/getSendRecipientLists.dom.ts | 3000 | `896afd729a246a863dad54922ab30f18732b7ab7633e87efd0b9266f7cd310c0` | 0 |
| ts/jobs/helpers/getUntrustedConversationServiceIds.dom.ts | 979 | `fda20478b8454c83233ab23162f09d606504cf30da2810a22dcb6dee1da40e07` | 0 |
| ts/jobs/helpers/getValidRecipients.dom.ts | 1047 | `634aaa2cbf934f47f627a86a6f29bac8b39ad79bf1b00a92a91efa4926429abf` | 0 |
| ts/jobs/helpers/handleCommonJobRequestError.std.ts | 761 | `4ac922ff4366c6c7ba8ba5f71d6c2c44271b6a9716c4b8799c3141a8d91635d3` | 0 |
| ts/jobs/helpers/handleMultipleSendErrors.std.ts | 2458 | `a0a346a8878efebed2409a2ad95d4e2609d0ad7b31f45896ca184e3635f33157` | 0 |
| ts/jobs/helpers/sendCallingMessage.preload.ts | 4606 | `f810f42705abe8285778b7bcce092fd8fd220eb101f8db426a83d35282de87c0` | 0 |
| ts/jobs/helpers/sendDeleteForEveryone.preload.ts | 11133 | `0c8f20bbb4dc60b7ac1f1fa5c3eaec680d1b954bc6d9b5472c73d9dd5a948d30` | 0 |
| ts/jobs/helpers/sendDeleteStoryForEveryone.preload.ts | 9997 | `8b5406f1c0a3215f1af18732d769b089a6fafc2b75d9c8ccf519b23d9be41abc` | 0 |
| ts/jobs/helpers/sendDirectExpirationTimerUpdate.preload.ts | 5120 | `ea0c9a79b27733e9998699792143648ed99cac807573fccdfbd6f970cc575fbc` | 0 |
| ts/jobs/helpers/sendGroupCallUpdate.preload.ts | 3319 | `65700d5ac49a37e9c88dece3c45854442ea4148ccbc1759e3ad8929dc9301853` | 0 |
| ts/jobs/helpers/sendGroupUpdate.preload.ts | 4348 | `de8a8b7288d36439396ce06ef7969d490ea700de0b30b9878fd05f6b4753b7db` | 0 |
| ts/jobs/helpers/sendNormalMessage.preload.ts | 36151 | `58e61b915a6b29ab3e74897a11f073d93ba521e89ee9ad3f3205b5e8dbfe1cf2` | 0 |
| ts/jobs/helpers/sendNullMessage.preload.ts | 5308 | `c9f79a755c7287ed2380d757d79d28bfe76882c3c3c7c7f89794171565879b8a` | 0 |
| ts/jobs/helpers/sendPinMessage.preload.ts | 805 | `d4c0f470733dfa463ba13656deb62cfbe00d26d325127cb7ed7d6837d62af233` | 0 |
| ts/jobs/helpers/sendPollTerminate.preload.ts | 10828 | `ce8262bafcd9adb1eaab4de17c489a36d518791cff76f966377b5378a94c8d32` | 0 |
| ts/jobs/helpers/sendPollVote.preload.ts | 13311 | `da4064f9bbf2dde6222e479f84de753869e6fed77f51c05089cc347f0b2fc757` | 0 |
| ts/jobs/helpers/sendProfileKey.preload.ts | 6725 | `363cb3e260df7fa95e6e32794e9ef7dd3369aca5f15bfc305e1a7a6f09f548df` | 0 |
| ts/jobs/helpers/sendReaction.preload.ts | 13721 | `a8886668b289387a35b707657049dad7ae357bcf9572b1072541e4a895170ecc` | 0 |
| ts/jobs/helpers/sendReceipts.preload.ts | 831 | `9448692c8ecb1a72c2d7788947c57043f80a16b6af230b88e9c7a0c15c8252c8` | 0 |
| ts/jobs/helpers/sendResendRequest.preload.ts | 5860 | `26711ed9f13914e9c39a96a1413ae8d1d9dc4d8d09ddc033257b222f3c5c73aa` | 0 |
| ts/jobs/helpers/sendSavedProto.preload.ts | 3335 | `ebeb892e9e6444c7732d17d1fbc17723ba0067ad77547ea7862941d2b4c00445` | 0 |
| ts/jobs/helpers/sendSenderKeyDistribution.preload.ts | 3638 | `6bbedcb2d66157fb73616aeff63a50f16e669ccdd49c466d264393f32c543ea8` | 0 |
| ts/jobs/helpers/sendStory.preload.ts | 23380 | `b559ba4febfce00c23dd9a2bacf2475a9e1f5d5a5dc042d096ac881c13fade1d` | 0 |
| ts/jobs/helpers/sendUnpinMessage.preload.ts | 783 | `1f1f49e9e62de7b24e29807ad24632115d5a24236b0f774db4f07c8b14622494` | 0 |
| ts/jobs/helpers/shouldSendToConversation.preload.ts | 3286 | `9d33d612018275ea49869fb29e0a55819742d8d11b1cab539b61162b77606ddc` | 0 |
| ts/jobs/helpers/sleepForRateLimitRetryAfterTime.std.ts | 853 | `3624dbbf8f4ab0e2660d8168ad618c183f1b9141149c357cb03cb69e659c8d87` | 0 |
| ts/jobs/helpers/syncHelpers.preload.ts | 5143 | `583b85920b09987fa28905f8c1d4a999c5fdf158d3942e31b6746a473d2c414e` | 0 |
| ts/jobs/initializeAllJobQueues.preload.ts | 3446 | `3af5d85e21dd390dff9ec02cbb519f1d7babe50015de38ac354c83cde9e2efbe` | 0 |
| ts/jobs/readSyncJobQueue.preload.ts | 1701 | `6762953a4d532a0a7496ed974957d27c70989f8ff61e9a842d9c3ee5a2d609c5` | 0 |
| ts/jobs/registrationJobQueue.preload.ts | 20802 | `26a068884a992a3bf344fff007dfbe7e593257f92bcd0ea2eb3e142014e5c502` | 0 |
| ts/jobs/removeStorageKeyJobQueue.preload.ts | 1448 | `a2752edc4f3af48dacadf9a59e7de5b9198fa1d0a2151a1864d7734c1d5f701b` | 0 |
| ts/jobs/reportSpamJobQueue.preload.ts | 4028 | `d87027a00546fdd80b861bb34b41298fc2c9a42fb6b487dfa546cd49a0500403` | 0 |
| ts/jobs/singleProtoJobQueue.preload.ts | 4164 | `a7135c2b2f4eb5b981d1ca010037374606083691528832c9c31e08f63c12ef9f` | 0 |
| ts/jobs/types.std.ts | 1258 | `2dd4d9df6ce7a1a4667c6f04fdff7d3b5c6b63dbb4eededdb2447f61287c0843` | 0 |
| ts/jobs/viewOnceOpenJobQueue.preload.ts | 1780 | `72a2fd18113b68f5b0fe46f0aa04b2862fa5b1dd6f0e4e7d267c0262b9eea23c` | 0 |
| ts/jobs/viewSyncJobQueue.preload.ts | 1701 | `73132d27fb6a28a4a6bb54067b36494271ca59bd134e1fd425fcce0d837f0570` | 0 |
| ts/linkPreviews/isLinkPreviewDateValid.std.ts | 385 | `806a9b605900aaba92928fe82588e6de78e97c20d3c93c665cf88b1294692eba` | 0 |
| ts/linkPreviews/linkPreviewFetch.preload.ts | 18252 | `326c29422fa7daa990f37b5e2856dfcfd3964a4c5a4d086a27dfe93e94b74257` | 0 |
| ts/linkPreviews/shouldUseFullSizeLinkPreviewImage.std.ts | 914 | `89adeec717a65b0b14080c0c9bd50485b5cb07a126092562f5e6aee6e471d936` | 0 |
| ts/logging/debuglogs.node.ts | 3413 | `11a522619e7361442f593755c7405a4ebdf659bfa998100c2136e2bb12febc85` | 0 |
| ts/logging/formatCountForLogging.std.ts | 287 | `cc6dbc76997b43458f5fed27868eabd5d3416f8f4f4b0e57982e1f0b14d22865` | 0 |
| ts/logging/log.std.ts | 6271 | `839a8494e5afebd2c01f035d504d0a683fe91808fbc1d41a1c380406994ea079` | 0 |
| ts/logging/main_process_logging.main.ts | 8437 | `1ade0ade4aedcb70da92717f2972244d02706f2a0ca296d1977e4c2db3fb3ea3` | 0 |
| ts/logging/set_up_renderer_logging.preload.ts | 2742 | `4446a3d7a74d7c3579e57dd3c29d226c7a491f16627602574750745667c96197` | 0 |
| ts/logging/shared.std.ts | 2861 | `bbe8d4ac60e94037f23548987561a1a328e534841cc980b7c824010c273a75d5` | 0 |
| ts/logging/uploadDebugLog.node.ts | 3330 | `ccee788257a8cc58fdbe45a71e9948279ab1dbaa58c098abc801b0592d7e0897` | 0 |
| ts/main/NativeThemeNotifier.main.ts | 1101 | `b3d44bab6892449ca9981e251c2b5526f3f685abfaa070ec8e3f6a4c6785417b` | 0 |
| ts/main/challengeMain.main.ts | 1937 | `908350473556cf49e91e160ba4cff3401ea294bf05013f2aed70fa028633cd1e` | 0 |
| ts/main/clipboardMain.main.ts | 934 | `b76f6aa5076ad672c86494fecb0bfa543aae9fa593b9e731b3560b6e35d3ae67` | 0 |
| ts/main/powerChannel.main.ts | 705 | `230bfe718cf430713eecb838ec6416fe076db7f0a8b3732bbea0e0204e0594ee` | 0 |
| ts/main/settingsChannel.main.ts | 4880 | `5efd573ae4d4f59b032078c361a9e3f2d63b7a6a544c948e17e7c3b9e2309e4d` | 0 |
| ts/mediaEditor/ImageStateType.std.ts | 239 | `3cc85ff665b182c610617ecf6bee0e12be85fdb5985d45231b148cd854372f8f` | 0 |
| ts/mediaEditor/MediaEditorFabricAnalogTimeSticker.dom.ts | 6879 | `dfa312048753db6c1a0bc2600f49232d20c2b1d2130df5840aca7e9ac34c183d` | 0 |
| ts/mediaEditor/MediaEditorFabricCropRect.dom.ts | 4280 | `d554ebdbaca29158d1e79cd1e2e9496338dedab6ff8c5e6c4d78b488ad34e5d7` | 0 |
| ts/mediaEditor/MediaEditorFabricDigitalTimeSticker.dom.ts | 5388 | `3bb00fcaeb8c87d5336896503cd5dfae88f64c90d4767fd4bce6bfef70c68a15` | 0 |
| ts/mediaEditor/MediaEditorFabricIText.dom.ts | 1200 | `92c6c130949620162bf4ed8b3ec79bc0e2c2354968b0b370976853fc14904a61` | 0 |
| ts/mediaEditor/MediaEditorFabricPath.dom.ts | 913 | `3f54a8e6412063fb67fa3c66f21783e2d7790cbfc4bd4b64cf8ff42f98d8ff70` | 0 |
| ts/mediaEditor/MediaEditorFabricPencilBrush.dom.ts | 723 | `7f140bb6b9e9fa19788bebe32992520f81db2c2049ce6ae8e0f38241ba3d3cef` | 0 |
| ts/mediaEditor/MediaEditorFabricSticker.dom.ts | 1613 | `88a1608ed841be9d26f92e758d0d4c2df2e5ebb401c698eb271ca8e17ea47320` | 0 |
| ts/mediaEditor/fabricEffectListener.std.ts | 563 | `d694181ce5c5a146c5651d9a3e3167d2da1987fa075322e59a4ad57e11a1dd59` | 0 |
| ts/mediaEditor/useFabricHistory.dom.ts | 7957 | `a1551e9e4159aaa7427793d65d63a3df19c067799c8769e7d326433b431b3ae4` | 0 |
| ts/mediaEditor/util/color.std.ts | 1336 | `3e758b40f796db52f8eaf36e3dcf017f98d2b05c5b9b7e0035829de8bed2561a` | 0 |
| ts/mediaEditor/util/customFabricObjectControls.dom.ts | 3486 | `eb2e7c9a173e604b06799bd7fdad216be41350227d8e3ea7714bd5a82a0ca165` | 0 |
| ts/mediaEditor/util/getTextStyleAttributes.std.ts | 1316 | `38e72c86a7ed355d1931c4770539955d73691a087ae8b34a57ec33f926b89174` | 0 |
| ts/mediaEditor/util/moreStyles.dom.ts | 1029 | `b8fce44506601babf0f380be5c9dda16afb2c12414d1e7a41d6ec90ac13851f5` | 0 |
| ts/messageModifiers/AttachmentDownloads.preload.ts | 10312 | `a374f3b55c6133c3b110f1958d8513f7feff2da786422872c15976cdd03f5def` | 0 |
| ts/messageModifiers/Deletes.preload.ts | 3364 | `5c2cc3fe745d88d181683573fe01112d6b09bf16240c3a31cff05dcf532a7a1c` | 0 |
| ts/messageModifiers/DeletesForMe.preload.ts | 3871 | `d3a9ce0e7948e5c28cca1d3c45887d04a2c427e17abc0b710017988e727d664a` | 0 |
| ts/messageModifiers/Edits.preload.ts | 4315 | `3554c3afd56f7d4d2cbb2d26cbc16306b649c2b5999c423330b6a86ecae0b471` | 0 |
| ts/messageModifiers/MessageReceipts.preload.ts | 17615 | `960069b8c920a61d831f9086aec69d6ecf1d638639d0fc530d17f8087c318010` | 0 |
| ts/messageModifiers/MessageRequests.dom.ts | 2249 | `091db7bcda2f89f3292fe6c60dba16530da2340a2e4bdfe8271bd2076e4f2e82` | 0 |
| ts/messageModifiers/PinnedMessages.preload.ts | 8021 | `3467ae250d9268d913a80046b856e051d3e461772241b5ca1ca8d1d24c930309` | 0 |
| ts/messageModifiers/Polls.preload.ts | 18313 | `74ba3d381ea6f7adfa0d05fa3667539ab8c432e77a3f289d9aa44032849b741c` | 0 |
| ts/messageModifiers/Reactions.preload.ts | 19680 | `69af6c7c9cc92022ba9f130f6cd99266992441e1a2f31cf58a0be8085c205794` | 0 |
| ts/messageModifiers/ReadSyncs.preload.ts | 8018 | `4bac721b8ed2c05059e2071a33122eed5d180629e31fe97f63607407b7f046c6` | 0 |
| ts/messageModifiers/ViewOnceOpenSyncs.preload.ts | 2758 | `7de1489332b6dd3fbde4c51d5b611bb2b9ce2339521d643a9446f92e0369028d` | 0 |
| ts/messageModifiers/ViewSyncs.preload.ts | 4462 | `61faf85048eface34008bade7ae9e8ce75afeb11673906c25f8f0d652e187a96` | 0 |
| ts/messageModifiers/helpers/findMessageModifierTarget.preload.ts | 1403 | `39b8c1b7870f5ee4b9d32237fd4d21b977d28f42777162331f43c6eb71eff0c5` | 0 |
| ts/messageModifiers/helpers/isValidSenderAciForConversation.preload.ts | 564 | `fc488636050c91361218f55b7b375a22280c6f0b6e90923b886aab98c5184203` | 0 |
| ts/messages/MessageReadStatus.std.ts | 839 | `c1c2941551cf96f524bd5b1b74a63bdd7d511fb971649c48e8f0fec0cd7a7c1b` | 0 |
| ts/messages/MessageSendState.std.ts | 8909 | `6615a0f75371920082c3f51da5565f22d59a8577b0f86ed614aeb4778c818e03` | 0 |
| ts/messages/copyQuote.preload.ts | 6298 | `18c5b5ddda7018ca6163d0c228ac498dd9f32c96cf29613971a7897d6af99240` | 0 |
| ts/messages/getMessageById.preload.ts | 993 | `b3d6690683938be645cbd6a8eff4218cc9509c5d35886a2d4086b27507e174ac` | 0 |
| ts/messages/getMessagesById.preload.ts | 1452 | `e1b6297f97084d389454d2274449fa04c74c94f3545529f7f2fee7fc531ec258` | 0 |
| ts/messages/handleDataMessage.preload.ts | 27806 | `e6168bc4dbc589b464abc699a546f2810b1bea70511128d0e350de448b51ae27` | 0 |
| ts/messages/helpers.std.ts | 2092 | `247ddc7f23d5f80b7a459cd8781d0f8097b720776441fde62c58feaaffec2790` | 0 |
| ts/messages/maybeNotify.preload.ts | 8956 | `e5f96a77e0a28805b84e3bff2bd29b3f0b295aec13523a3da410281b1aabb4f9` | 0 |
| ts/messages/migrateLegacyReadStatus.std.ts | 563 | `7cc0e8f0f1998af87acbd4e641075bbfc631ed9ec20b9db19d029802a2c3f845` | 0 |
| ts/messages/migrateLegacySendAttributes.preload.ts | 4758 | `239a24e0580d80f1897b91953e2703cf6bfa702e476bd6da7454991a52611478` | 0 |
| ts/messages/migrateMessageData.preload.ts | 6056 | `e3dfdbbbb85a7ba0f096fc179e4ba1bb48bf6ca24b27aa5958543fc06c0e5105` | 0 |
| ts/messages/payments.std.ts | 2611 | `6a9ad0a89d7d7be721ba52955b1996968f0d5cc0f3933b884dee69431aca53dd` | 0 |
| ts/messages/quotes.preload.ts | 871 | `df077e1f04f12cf1c60ea0c48116d7ebd9d573e8f7cbf97d4265618e90732957` | 0 |
| ts/messages/saveAndNotify.preload.ts | 2328 | `be3ea7930845c0b1f1df057c8e9e483ad40eacbea6fd828b5a7072297ce597fc` | 0 |
| ts/messages/send.preload.ts | 14754 | `1712eeaedc165f18ad2d3fe7288a707dfc5a42021c169b55ee589bfbd4d2a6b7` | 0 |
| ts/messages/sources.preload.ts | 2214 | `05c0e955a4cd89ce8c6fda4e82ce83d7609800788b5236f2727db05b449d4e7b` | 0 |
| ts/model-types.d.ts | 19795 | `3b62b277b63ccef24a1d4a78d09a7e3768be4d8b52bfe979b3d53c54d34fac1d` | 0 |
| ts/models/conversations.preload.ts | 188778 | `eeabdad028c8edfb3928175132b261c9c8606b83ef3f33b5a9869f5447ee00b9` | 0 |
| ts/models/messages.preload.ts | 1967 | `ac31a89ca1162ee4a9dc7fab15a208a17dba6b671c17205b63bd274cfe5a12f0` | 0 |
| ts/mp4box.d.ts | 1426 | `d9637e3f078db9f3022f78b2ae5ea83d3067e5a52249cb6c230e97a66e4b7c95` | 0 |
| ts/polls/enqueuePollTerminateForSend.preload.ts | 2531 | `803b36531ed38064d11e0451febf340ce218ac053dedaafc55db59860ef4d3db` | 0 |
| ts/polls/enqueuePollVoteForSend.preload.ts | 3042 | `0b42efb25f30872322975c92b720078cb754a3a2a3ee9b064dd5a08ea76f1356` | 0 |
| ts/polls/util.std.ts | 3621 | `edf4ddab8e3c98d29b113a723d6095cf155d87846156e7e1560b88f31d9b5f98` | 0 |
| ts/protobuf/index.std.ts | 286 | `8ed85a7ce1e4a865e21c7aa5201d863763c240c1a530e83b60091f6ed7026b91` | 0 |
| ts/quill/auto-substitute-ascii-emojis/index.dom.tsx | 3437 | `39a1e8ec3f11befeb138d2ed8206682b3cdbdb4725f4e761f7117ee5091c7777` | 0 |
| ts/quill/block/blot.dom.tsx | 384 | `e796d3545cc80b3a128a25bf8b2254b137e39eaddc7e5e04696f175a03fba28b` | 0 |
| ts/quill/emoji/blot.dom.tsx | 1743 | `e42b52b9aacc976d79fe5bbf3fc3e6fc79e1e68994668b83d4db389424adb248` | 0 |
| ts/quill/emoji/completion.dom.tsx | 12908 | `564c166b3fed7edc36c76189ddc9bed97d14d8d6a605004b8c7745e189b7d3b9` | 0 |
| ts/quill/emoji/index.dom.tsx | 183 | `79ed327d42811a45145619c34ea718e51fff1a81e90ca3d9ace9b7f6b39b155d` | 0 |
| ts/quill/emoji/matchers.dom.ts | 1055 | `fe786ffbf8e55473bf8ef79f33f0d571a6cc13ab9302a8af801f865564b21da5` | 0 |
| ts/quill/formatting/matchers.dom.ts | 2163 | `820abf4cf8152fd4190e29d35f7db5d24a0a55713ceec170c3eff381e1921b07` | 0 |
| ts/quill/formatting/menu.dom.tsx | 16812 | `09c8a3c10af80e6f62db4b2b7233e64cf6c4fb6260d68d47d4c6c4c43332061b` | 0 |
| ts/quill/formatting/monospaceBlot.std.ts | 813 | `3d4c6dd2576960bc363dcbdf237cebed1533de25670ea94017d190d137098db8` | 0 |
| ts/quill/formatting/spoilerBlot.std.ts | 831 | `2a8c5bda39b4de2d0f5a81e0d2114d9b886af43bdb65ff4eb46f7fc94b3f6011` | 0 |
| ts/quill/memberRepository.std.ts | 3681 | `91cc3808cca11e196ddc9b5b42ea45bc2832d01e0da1107f5ee02212f346aca5` | 0 |
| ts/quill/mentions/blot.dom.tsx | 1882 | `ba3be572190aff7d2c178d58841616f4f7e3ff18887869ebf7a816e5619de43f` | 0 |
| ts/quill/mentions/completion.dom.tsx | 9959 | `086420de72387c3c44705d6a74b7ef02e359066b7cae731fcc6e91b87c2f670c` | 0 |
| ts/quill/mentions/matchers.std.ts | 1878 | `7ca8aaf2eb5c0557f3d13418b468a68ac85842317ef205df3309a1d2b68ef202` | 0 |
| ts/quill/signal-clipboard/index.dom.ts | 4228 | `1d9c0ac07aa011d29eeacdb9892f4fa9145018198a5d9b1478339d9cfb4edd54` | 0 |
| ts/quill/signal-clipboard/util.dom.ts | 7035 | `2565bf4cd5b327d01b1a4365c4082af5ef85c072c8ae1773607940621ef6d32f` | 0 |
| ts/quill/util.dom.ts | 12197 | `3dbc5768ad777d01ff1ae6fca8f1330656b24da9d3155459e89a4c704702ef4b` | 0 |
| ts/reactions/ReactionSource.std.ts | 163 | `4a5e900f42fa3eebc9b43f3799968552973eaa3baf4b56eec126a90736b83e4b` | 0 |
| ts/reactions/enqueueReactionForSend.preload.ts | 4853 | `01adaec0ab9ae7881a4e5f0a227d839c4ba554e872c6797017c791e53f233ef5` | 0 |
| ts/reactions/preferredReactionEmoji.std.ts | 1123 | `7bb7371fb7609a17051daa320cfa6952e52207b0f1f8fa422e2c6b8dc302d837` | 0 |
| ts/reactions/util.std.ts | 5501 | `d9f9a602345f2ef8b1307c6e366cce08304132ab64159be9f88e0b102eed0e43` | 0 |
| ts/routineProfileRefresh.preload.ts | 7271 | `da07fdb8730d12b0fbfce36583831bdf2d8de8491c6dd25fda1ea4443558dc32` | 0 |
| ts/services/ActiveWindowService.std.ts | 5385 | `b2d7410c8d28f50a920a436d7ce3cf26e9ccadd24100d2e24f54896d38be147d` | 0 |
| ts/services/BeforeNavigate.std.ts | 3035 | `e4ac50584219403399dbe7f07cd3e4b9301eb4fd48e6f61f55d29dfbec06afcc` | 0 |
| ts/services/LinkPreview.preload.ts | 17196 | `b0c9f2a1fd58f9e665fc2513bc4c86af45cf121686806d7b203fc213b44a7789` | 0 |
| ts/services/MessageCache.preload.ts | 9091 | `9e6a53108452d5c30fe7736a1650ade9ddd965201c6eb5af4db80d85d6ee6776` | 0 |
| ts/services/MessageUpdater.preload.ts | 5370 | `971d64ad8cf4a9267c17e2e942885c9d893d2c1713cb918cec60ba78e21a11f4` | 0 |
| ts/services/ZoomFactorService.main.ts | 4654 | `f68a00f9210d7267b2e8b18dfc9f1ec9266ec884cbf1d5f444d8d68c851f46a7` | 0 |
| ts/services/addGlobalKeyboardShortcuts.preload.ts | 14400 | `633c403e3dfbf77edf2d9217a62a04c50c14f55d7bfffae3536732c4ec8c78ba` | 0 |
| ts/services/allLoaders.preload.ts | 2988 | `399b83ae0cf8751a9762996d7aebe0761e22dc1bce46cc4216b8e11e3606f4d8` | 0 |
| ts/services/areWeASubscriber.dom.ts | 1200 | `dbca1e2e01ef26a19417c5c021040c48b003eacdd6ad800e24c394b1f0ebb43c` | 0 |
| ts/services/audioRecorder.dom.ts | 3904 | `70c926e0923f740506377bc765f06a3da322e1c7e5091b8b07ac8e8b1c52b03e` | 0 |
| ts/services/backups/api.preload.ts | 7879 | `3227fff70be4930f35519c13f558ae9fc3d5edc080f08fcdb2a08690b0171231` | 0 |
| ts/services/backups/constants.std.ts | 1657 | `8ef19c987035da83f6c7ca44285f735c986fecdcf677e95007b11cb8663ae355` | 0 |
| ts/services/backups/credentials.preload.ts | 12052 | `3674707883b98ca453598791fa6d8aebe836b6ab9d46d37f91f5af53fd6ebad3` | 0 |
| ts/services/backups/crypto.preload.ts | 4508 | `1107bb73feca5f198a5138f146d5736854dfa933d3f5421d52b7d187a4561ac5` | 0 |
| ts/services/backups/encoding.node.ts | 6601 | `cdc7e0507f192cd3b701f72c3a66f4dd050649daf8cf9d688812d7dac2bc813c` | 0 |
| ts/services/backups/errors.std.ts | 1366 | `bee5eec8e203dde7e09bc8e9a28aa4219f78f3dce1d476f0fd546a5fcb0ebf47` | 0 |
| ts/services/backups/export.preload.ts | 129923 | `f81c79502ff00fff4f307d761020d91e331959b40dd142b3008fe5a62ee29846` | 0 |
| ts/services/backups/import.preload.ts | 148081 | `a4e039aa3e96b2aabaf0406df09d2972d363c312e21d4f3fbf8af7119e4194d0` | 0 |
| ts/services/backups/index.preload.ts | 45210 | `c10feb35f57b3cc2cfa22d5d11913eb5fd9f40fe71cf0eb25e9b38f3e282b8fa` | 0 |
| ts/services/backups/types.std.ts | 2412 | `afb1ffa64bc896ed4ad3a108f450e760fb0325693375f67dc9b16a9e6dd5b1f7` | 0 |
| ts/services/backups/util/FileStream.node.ts | 1404 | `95ef973408ef98f7bc08cdc0218fccc2b229cb25dcdd3e91531390aab7fe150b` | 0 |
| ts/services/backups/util/expiration.std.ts | 662 | `c1160f5b3caa7dccce939739c9b32c768010985440258fc86908012b0f889589` | 0 |
| ts/services/backups/util/filePointers.preload.ts | 14241 | `d04c0a7f69caaf638987c57958e52abe5a009f468503ad26bbdae5cdf2b74cf0` | 0 |
| ts/services/backups/util/localBackup.node.ts | 10754 | `7e7bab8ee3eb95319fb8c6c85adbdff27c3307a035069512d016040a9e1a95cd` | 0 |
| ts/services/backups/util/mediaId.preload.ts | 2967 | `afd160fdfa1ac6d5b398f88ae536b89a14f7c3197511b74f31ca7a1171cb7fc2` | 0 |
| ts/services/backups/validator.preload.ts | 2463 | `0b2fdf9dc237ad6c13ffe51074ac854f407fc2c0d68b09b2ae92737803ee2889` | 0 |
| ts/services/badgeLoader.preload.ts | 694 | `9a07b7efe9ed4123eae710bc71d748391b6d99cf441047de59338c2a792f8dd0` | 0 |
| ts/services/bounce.main.ts | 843 | `f02289bda24d8d4b7c175c46033dacaa4d5ea92cdc5d6b0a57266a6eb807c4d0` | 0 |
| ts/services/buildExpiration.preload.ts | 2411 | `8e06c3b269e98b6bd814ac478d1e7e2db40c03ebd31e0836e6edcca615537676` | 0 |
| ts/services/callHistoryLoader.preload.ts | 1142 | `004fd9682e33f783887caa70be4cf22c1ac2257333b86fcbf9e97c7697c982fc` | 0 |
| ts/services/callLinksLoader.preload.ts | 584 | `aa45cc732e593c1a4b71d6498e60b7f9ce8b92157974498ca83bc708b5758245` | 0 |
| ts/services/calling.preload.ts | 140526 | `263fb57ee68f9baee6de1e339156c7b8aff3aa869cfffc63e80e4a520d3fdb26` | 0 |
| ts/services/challengeHandler.preload.ts | 1322 | `03a75dde5e08748b4d4755f79b42c44ea719bd7b5cefaa9480a705823b240bab` | 0 |
| ts/services/chatFoldersLoader.preload.ts | 613 | `6a3674b4baccc155ad2d83f5e99d0a64e45b15d4ea1162ca60d237962e78837e` | 0 |
| ts/services/contactSync.preload.ts | 9163 | `81288d0640f5ac18efa5e0de216068372eb0b64d3b511f689221ea5c7a6336d3` | 0 |
| ts/services/distributionListLoader.preload.ts | 1133 | `57fb843d19c1e9e88627c1eb642151c6f1f0660b9f6d2e0296d95b30dfa90de3` | 0 |
| ts/services/donationPermits.preload.ts | 4829 | `cbb42b7c88320145f2895c519a955112f490a1b5c022b41ff2b1073f100bba21` | 0 |
| ts/services/donations.preload.ts | 43915 | `21941a6d419cad097a2457cae9101ace36dc487aa468469e467d68e5d60aaa61` | 0 |
| ts/services/donationsLoader.preload.ts | 1020 | `42b82d17ba38833164128ab68dced5d0fd6a4aa383ea8b2b284904854a9546cd` | 0 |
| ts/services/expiring/callLinkCleanupService.preload.ts | 1392 | `a066239ea7562e2b55d5c0b214033ece4ba05440f91c944481e204101a04210f` | 0 |
| ts/services/expiring/chatFolderCleanupService.preload.ts | 1530 | `a8184c2169b5775e2ad08ba2c245321a8566c9ab08a235e50b1c3211d945e06e` | 0 |
| ts/services/expiring/createExpiringEntityCleanupService.std.ts | 8079 | `189614c7126083496ff89bf1bc6acf11d3466e79c864f433998a7a99f227c500` | 0 |
| ts/services/expiring/defunctCallLinkCleanupService.preload.ts | 1475 | `d4d9479443b29f77f76750f19d0ea1539d250a014bc94682847ded9aa0b55dc9` | 0 |
| ts/services/expiring/pinnedMessagesCleanupService.preload.ts | 2355 | `5a330b6f056064e1d0f3fb95f36b28ef6f301767892f59ed1a969a7e7a3576ff` | 0 |
| ts/services/expiringMessagesDeletion.preload.ts | 3436 | `d159a5b11248d5bcaeeb0d92aad888828aa13c85a6db7bb91695b6f573af4320` | 0 |
| ts/services/gifsLoader.preload.ts | 676 | `6d0fe656d95808bb74c0da27cd9f122f5f517954d0a76b612c04db5dba21ee4a` | 0 |
| ts/services/globalMessageAudio.std.ts | 3003 | `b6689aafe92500f27b2c83a7afa97cf347dbd5cc11d4c5a7128af7fb082a3b08` | 0 |
| ts/services/groupCredentialFetcher.preload.ts | 11357 | `65ec1219927c2f6064f77ab04c6ef11a2413f6dc7e3a72d4e90695c522af996c` | 0 |
| ts/services/keyTransparency.preload.ts | 12020 | `95b9feede8f57b6f69e23fb9825aa324ed353617119a059cd638cda177399756` | 0 |
| ts/services/localizedEmojiListLoader.dom.ts | 526 | `df57ce363c5ac52376b78ccb12cb49a5dda5cd211b24acd34776688cadc45e6b` | 0 |
| ts/services/megaphone.preload.ts | 6389 | `783deab06378029d449f999b6e13af86d38a7370f1ecd8a98e5d21c7f8dda4ec` | 0 |
| ts/services/messageStateCleanup.dom.ts | 445 | `ec8db7f540a5b3527e3d96f2c9192d850936418989f4c88cc314d1d92aa48027` | 0 |
| ts/services/networkObserver.preload.ts | 3179 | `f7ea91c364365e2d227d7348c78c0e8a3dbb79a9075a271f818f954f947e6682` | 0 |
| ts/services/notificationProfilesService.preload.ts | 9573 | `c51ca60950aa92c93f61a81add3d6bae42d0abfc52f71d2940453bd3fafe929d` | 0 |
| ts/services/notifications.preload.ts | 20582 | `ecae876aa4a3e371be2bf9ca451093e57ee8c2772a34d836e7a038cce9d14a7b` | 0 |
| ts/services/ourProfileKey.std.ts | 3084 | `c82768cee4df012fb0455e0cd8fc257edc38389d6631439c87d243fa257bc9c3` | 0 |
| ts/services/pinReminder.preload.ts | 5602 | `f6e9f84969cee38839ea7c43af791233789c773207ea5b7a8b5509f802c6b105` | 0 |
| ts/services/profiles.preload.ts | 28286 | `55fa11573ef3ced4ce96125b57f019a88221f9820e9af1a3b66289bfb47fdbf0` | 0 |
| ts/services/recentEmojisLoader.preload.ts | 515 | `ad74b8e25b2c16bfddf9e7e2b53eec77c759d9772e795e8de918e3ae2a204349` | 0 |
| ts/services/releaseNoteAndMegaphoneFetcher.preload.ts | 22622 | `2b5545e30a05f10709d8dc6900e65a81cc8c7c2215ab342dea43a770bf8190ee` | 0 |
| ts/services/retryPlaceholders.std.ts | 6502 | `e0cee91b65454ec752c3881faeee5f214d36c7b2392c4255766c1cd5f2c402c9` | 0 |
| ts/services/senderCertificate.preload.ts | 7728 | `e68775cfd44f2453a820b18b1e4a2a796bbeb068d86e43d97b3d121a966597e8` | 0 |
| ts/services/singleServePromise.std.ts | 1378 | `0a5ab01d047776999e1cde2f039596e793311239a406209a57f51bc6718d238e` | 0 |
| ts/services/storage.preload.ts | 93823 | `c1e8a6b61f931520e9f5c6488a89899d4ef5ec5bbea9edeec7051b826cc68cf0` | 0 |
| ts/services/storageConstants.std.ts | 183 | `b99fb2cb7e544f031c39da7a2ac77ccefd1bd6a47a4046f83d4204ed25b7c40c` | 0 |
| ts/services/storageRecordOps.preload.ts | 107053 | `a68242f2345c512367435e859703b6a01270605f37d1cb0bb340f2d6dae3de59` | 0 |
| ts/services/storyLoader.preload.ts | 5927 | `aa7c94f76b1a6648016a21aee98b7d1152ce9d6eb29705672010ef6be9c9a2f5` | 0 |
| ts/services/tapToViewMessagesDeletionService.preload.ts | 3920 | `5b3c6de8809d1b6c017ad64fa5d52fb839ded479ad6c75a0a01a0c833c4c6255` | 0 |
| ts/services/unreadReminders.preload.ts | 7971 | `672dd1053982bd2a0f064ba2d8c4f6dd8bf78c28697eb9d086d1ea3a0539f100` | 0 |
| ts/services/updateListener.preload.ts | 713 | `0335d79404133fc71a095d00308c1a5f6589daab7804e8814ac031cb3002c0f7` | 0 |
| ts/services/userLoader.dom.ts | 1185 | `9100b87fe39b24fc28baf5074c6ddc700b9b1fba0735b1cf7c087f23bba520c0` | 0 |
| ts/services/username.preload.ts | 12293 | `ee0322e908892c9d8f2359e14aa2a2f9078d39dc64ea6858dd5d695e68fdaf37` | 0 |
| ts/services/usernameIntegrity.preload.ts | 4658 | `4709370bb8107a301119013cf072fe96881235ecf635164b9d8693168789de53` | 0 |
| ts/services/writeProfile.preload.ts | 5063 | `8c7124cf9f095b0a6a28761c77ca079f28814aefb57f40c9d292c911d6aa7564` | 0 |
| ts/setAppLoadingScreenMessage.dom.ts | 1097 | `cea00b470fe2bb7012780f02df2437bfa9a2c27e28f04fabb77348fdfadafaf8` | 0 |
| ts/shims/bounceAppIcon.preload.ts | 337 | `dda3e9dd3b37ea6e1978b6291ffc528894fae3d486e0f21e4fb77221e1bd8588` | 0 |
| ts/shims/contactVerification.dom.ts | 449 | `9458e3b7d87aa1b3094bb6921b5f5385f533faadc4c19cb4b6b08aa918cdf04e` | 0 |
| ts/shims/deleteAllData.preload.ts | 1765 | `b622869d8a7651c32b3d3fd89a69412cbdd380dbf37924e0956fea18318ca8ea` | 0 |
| ts/shims/dispatchItemsMiddleware.preload.ts | 1002 | `cf1aefb4f9f6e877e01d6182fc034a4c5de884408f275bdb55b47cbba29a126c` | 0 |
| ts/shims/events.dom.ts | 738 | `a76a2c812b458256af94fb37c381685822394f056f1295ebd86cc6956219260f` | 0 |
| ts/shims/reloadSelectedConversation.dom.ts | 622 | `bde8f61d437d8ee774fa80b48ed93b8013dbebf0312d2c7fad314456dae3e960` | 0 |
| ts/shims/renderClearingDataView.preload.tsx | 735 | `c667def0748298f833b36542abf0a16c3f4ffb027d65310e31f0210140a8adc0` | 0 |
| ts/shims/storage.preload.ts | 512 | `97ddc901cfabe7c36fecb7fe2dc3c033740d4fa2d9b890ecc04ec2f016d8072e` | 0 |
| ts/shims/textsecure.preload.ts | 994 | `711904e42cb0bc22cdc2cce2e3ae30a1ffe8f97e6193b3dbea67e32291e3fe71` | 0 |
| ts/shims/themeChanged.dom.ts | 354 | `be0c435f296c4e7b16c717ed0630d7389c9ea399049cbf09d7ee7af26a3a4eb5` | 0 |
| ts/shims/updateIpc.preload.ts | 319 | `29dd3119080a0c16d2a267381124267894a48883e9eba0f999e15d1a7aaf032f` | 0 |
| ts/signal.preload.ts | 979 | `e5200c67ae95e29a4bce285fe1fc02a921853b2c11ccf421c40ec352e98dd515` | 0 |
| ts/sql/Client.preload.ts | 25978 | `ee200e499e6d87fba1e2589817f347679e1b831ef770dded7a091382a20c54bc` | 0 |
| ts/sql/Interface.std.ts | 56952 | `6505387fb130e170a8c6e216ad043e3aab5d7b0d19bd3e4ba6bafb2cc591a0ae` | 0 |
| ts/sql/Server.node.ts | 257148 | `9571e7318f73f7f947541f3c651edf22d9a677586baa3805586660c505f12026` | 0 |
| ts/sql/WalCheckpoints.std.ts | 5747 | `0f87475ce92c89ce01bb89a0491c176e889a3fa2d2e047e13d88922923ceeea7` | 0 |
| ts/sql/channels.preload.ts | 2319 | `4e312f5ef11a179c1c8d2072fcfe3d800dd2723fbb627d9fb45a300cefc7214f` | 0 |
| ts/sql/cleanDataForIpc.std.ts | 5273 | `fc3ca747de053be4a4e96e261dcb205e5f8edbdf99bfab5b12232d16eb6a9a25` | 0 |
| ts/sql/errors.std.ts | 854 | `86782d18926360987c43f64774fad38363c97125f6b80ad9ef34939216f4656f` | 0 |
| ts/sql/hydration.std.ts | 12833 | `e4b823e48a8d7a00e21a40bfeaab5bb27c5a6a094ff2efdcec587ff3e0e66bc8` | 0 |
| ts/sql/main.main.ts | 17125 | `4c5ecb36d3c1f1908d963f0d8f56d5d5afc180a523cdda291fd4d12c61e17d9f` | 0 |
| ts/sql/mainWorker.node.ts | 4769 | `0f333465db6108697e021033ce3bcdf5b58ce1895e6323c5a407d3453dd5b807` | 0 |
| ts/sql/migrations/1000-mark-unread-call-history-messages-as-unseen.std.ts | 1333 | `fb0fb1252a5e69782a189a787454e318cd4e8da591960e6d1505518b79af541d` | 0 |
| ts/sql/migrations/1010-call-links-table.std.ts | 624 | `2e4f6c099567a8b29401afb3800a5e2da6d161039f0eef17196960e409493237` | 0 |
| ts/sql/migrations/1020-self-merges.std.ts | 1121 | `0ae1f52ca4db6311fa3c7ea139f7c586babdac17f0feb6c2d45ac0ead38fa79a` | 0 |
| ts/sql/migrations/1030-unblock-event.std.ts | 2328 | `2dd55b8b9a4c6592614a62e80f50e359732d279c93cbe4160b9e6ccc3e03bc04` | 0 |
| ts/sql/migrations/1040-undownloaded-backed-up-media.std.ts | 6940 | `e8e9626091802d94a439a71844bb4625f92fbc3d0d5cc993bbea678e6bbab976` | 0 |
| ts/sql/migrations/1050-group-send-endorsements.std.ts | 1235 | `d012cfee58e9c86407ce6eec7adf8fcd336f37d1e5d18f82f2fc424a9b31ef58` | 0 |
| ts/sql/migrations/1060-addressable-messages-and-sync-tasks.std.ts | 925 | `eaa833dfa67b6df6edc346e1aba073d6943e25811a95d0677861f86c2d0e0d03` | 0 |
| ts/sql/migrations/1070-attachment-backup.std.ts | 971 | `475cdb67ba7fdb7f8a39b3b78733d1b88801566f4d08f46ef8ee980acdec8e12` | 0 |
| ts/sql/migrations/1080-nondisappearing-addressable.std.ts | 412 | `663672d8e424cae8add2157bff0f3b7e9d05bc0d5eb2cb7332c013b72c042b41` | 0 |
| ts/sql/migrations/1090-message-delete-indexes.std.ts | 367 | `7507ecf03d9930cb226323e17f9a47b27dfbe317f44b6d65cf659736344a20e9` | 0 |
| ts/sql/migrations/1100-optimize-mark-call-history-read-in-conversation.std.ts | 1967 | `c60f167bd6fa1a62322d41f9438ce98b638a74219e352588a5ec3be45a82da18` | 0 |
| ts/sql/migrations/1110-sticker-local-key.std.ts | 423 | `38d7fce23d667d3cedca4974459c8700e4f502987dc631ae0396570d542eac11` | 0 |
| ts/sql/migrations/1120-messages-foreign-keys-indexes.std.ts | 461 | `e72836e35e14ea1dfbf426ead925bbf217af67bd80c21477790621cb10cf20ca` | 0 |
| ts/sql/migrations/1130-isStory-index.std.ts | 386 | `d3ea91eb99450778f3ea2dd8f9e358824f4fdfa63f74da5532c472a3684487cf` | 0 |
| ts/sql/migrations/1140-call-links-deleted-column.std.ts | 427 | `e267b099bd5bfff3b3085a92140ec1f87f3f6b89ad27a1b5633d03403a1aefa3` | 0 |
| ts/sql/migrations/1150-expire-timer-version.std.ts | 482 | `381fbc6a7364fdfb0db33f1945d03f9fe2791c5457ee0a5f4e34feea68d6adbb` | 0 |
| ts/sql/migrations/1160-optimize-calls-unread-count.std.ts | 781 | `0576bc9191c181372d71e934a43f06177b8590d233b6573c4fdce786714e6473` | 0 |
| ts/sql/migrations/1170-update-call-history-unread-index.std.ts | 501 | `747bbe203f25bbe8b68aa4698e5452c8a62cf306b7deac7fa29c92ab8d1427e8` | 0 |
| ts/sql/migrations/1180-add-attachment-download-source.std.ts | 757 | `6ee2875db70695365f57ef62b55b7c70c120751b25a9505ab163f2ce6ec5b08d` | 0 |
| ts/sql/migrations/1190-call-links-storage.std.ts | 703 | `26fc5ec6ef140ce6104dc91c771d6a4eec4bf3af3e220e71dd1849efbed13236` | 0 |
| ts/sql/migrations/1200-attachment-download-source-index.std.ts | 491 | `9a68b64d7a3e706f0e1b9e8f44a4ddb52e7cd104b2cd76e669356a29404f136a` | 0 |
| ts/sql/migrations/1210-call-history-started-id.std.ts | 505 | `526ca33f3f4bac1dde3a6f70a2e8c3954546d55091a0b6dea03255084fa9dfed` | 0 |
| ts/sql/migrations/1220-blob-sessions.node.ts | 5326 | `66f2e1ac284862ce8193d5dc16e9ab24dbf990761fa000d53e8ba029e1d8a2a1` | 0 |
| ts/sql/migrations/1230-call-links-admin-key-index.std.ts | 342 | `e571b2138230a66fda425f081d9806fad8b0d6356bd92c7334ba7c02a6cd2fb4` | 0 |
| ts/sql/migrations/1240-defunct-call-links-table.std.ts | 449 | `887662fd3ba041d380fdad4023f2e50879584545b03a6000346d73726ef75ab2` | 0 |
| ts/sql/migrations/1250-defunct-call-links-storage.std.ts | 517 | `3fb53855af84243b23cf5be0f02c67f7e63d6266206fc60eba439c5043f8dd9d` | 0 |
| ts/sql/migrations/1260-sync-tasks-rowid.std.ts | 402 | `e50bb4c20106d1c4f64b97acbc5feef3db063b61385bce40e1b930de9d2183b8` | 0 |
| ts/sql/migrations/1270-normalize-messages.std.ts | 1142 | `ef76649c0a2f011d84e3f2f1c7e82799afc4d638a772795cdb19006e64520f26` | 0 |
| ts/sql/migrations/1280-blob-unprocessed.std.ts | 4630 | `36b540aacdcb42150f608c4d5c3e69a45f69b3f1709309b93fdcec37781f4347` | 0 |
| ts/sql/migrations/1290-int-unprocessed-source-device.std.ts | 565 | `705975b1c93b9ecec27a4ca7cb8ca7b89bf833115df84b314432406a0c4e0f3b` | 0 |
| ts/sql/migrations/1300-sticker-pack-refs.std.ts | 599 | `29691a61e106f9d7411837cb462500743c3f93c785008fb8269454adab058616` | 0 |
| ts/sql/migrations/1310-muted-fixup.std.ts | 835 | `74646537d92045750b4a03b6db881199318664e5bbfb548c24802233c9e0c1df` | 0 |
| ts/sql/migrations/1320-unprocessed-received-at-date.std.ts | 574 | `5d130c98135c8c14cc3df35a91406bfc2ffbc5d9691ed4b1bbc70359df2909ae` | 0 |
| ts/sql/migrations/1330-sync-tasks-type-index.std.ts | 349 | `2e2f11aa7566d60119d38ffe4fdd34fc5116c19d668bf3faadda4c383db2e820` | 0 |
| ts/sql/migrations/1340-recent-gifs.std.ts | 809 | `9223487601a607d3b1900cc589dc6cc391e4505e159dc8a1e59ca2c20aef0382` | 0 |
| ts/sql/migrations/1350-notification-profiles.std.ts | 1204 | `7b70021472342cd9337fb50b90a41b80070f0875f59ee4ba6a4f53eb6946d85b` | 0 |
| ts/sql/migrations/1360-attachments.std.ts | 3229 | `3bb10347423b430a615426f4abab2e61f64b3b8ec06fde4ba8d52f1931e8687f` | 0 |
| ts/sql/migrations/1370-message-attachment-indexes.std.ts | 599 | `5b04c76c2e26a14ffeb99dba59b82320019860a9f1821a661cf01aa46a272706` | 0 |
| ts/sql/migrations/1380-donation-receipts.std.ts | 574 | `3a86ea48fb037b4d12ca243a50c97c2a98ee6471d14f9d29840e51d9a317cfb3` | 0 |
| ts/sql/migrations/1390-attachment-download-keys.std.ts | 1203 | `1f969586ef47d41fd0122a86da95ed6a6a375b4c53a67560f20384a6c8870068` | 0 |
| ts/sql/migrations/1400-simplify-receipts.std.ts | 355 | `26f96dea1a0eb0294ca5bea01c60b33e493ab6964059dec62e165a309f44b356` | 0 |
| ts/sql/migrations/1410-remove-wallpaper.std.ts | 636 | `b6af895d5ed70ec8555ae76898fef8f5ad53d394166a25d3fe370812cd0cdeb0` | 0 |
| ts/sql/migrations/1420-backup-downloads.std.ts | 1723 | `673e2d05f81fa1334b48cba6940410493e266c84ca8e044946ac6cc1f512b254` | 0 |
| ts/sql/migrations/1430-call-links-epoch-id.std.ts | 369 | `913eaf49f1e189cc0ce7ac4d54f38815f2252b0806e4d7d743c84d3036108ddc` | 0 |
| ts/sql/migrations/1440-chat-folders.std.ts | 976 | `70eaa76b855f65ecf9e130744d51e2207c11d328925943ab0e70dd335ba06021` | 0 |
| ts/sql/migrations/1450-all-media.std.ts | 1221 | `d33e9a18def4a283de2e8256a8a620dcaaeaa380b5aa78858dbedafa3835e526` | 0 |
| ts/sql/migrations/1460-attachment-duration.std.ts | 301 | `61ad5dc42778edebbd5dd6c0eecc6adcaaa09b044faf74ee54105b58bff45edf` | 0 |
| ts/sql/migrations/1470-kyber-triple.std.ts | 483 | `5c70fe2b3406ac513150e996b0e17582f3c1c61bdccf728a1fa361bb80124184` | 0 |
| ts/sql/migrations/1480-chat-folders-remove-duplicates.std.ts | 692 | `4c00656cd5e7201b7f6619b07c9af6d21a00d11ba5ef9f6073f7ee41d5689803` | 0 |
| ts/sql/migrations/1490-lowercase-notification-profiles.std.ts | 587 | `958c084f6ec412e64421bf9aa0562bbe9a4b9edfdd6163bfc0b8deefb1396ad1` | 0 |
| ts/sql/migrations/1500-search-polls.std.ts | 1601 | `6c4986cb28dcfaaf35c8d5216e5ed5c5ac6ba830b501dad51a270f4854dd1557` | 0 |
| ts/sql/migrations/1510-chat-folders-normalize-all-chats.std.ts | 800 | `c4a851ba14f42e7ff233940e21b5832d433d1037d0d90fe8071852b9e03bb8a8` | 0 |
| ts/sql/migrations/1520-poll-votes-unread.std.ts | 630 | `b357c4c7283370cef8892f4bb664c754d297e4337402e0d65fb7a9f9d078bb51` | 0 |
| ts/sql/migrations/1530-update-expiring-index.std.ts | 589 | `6d4c90c68b378a32cb2902221da687dc4fe9e4a60f763ac54b6359e34c89884c` | 0 |
| ts/sql/migrations/1540-partial-expiring-index.std.ts | 495 | `75ec91c2d7235b62d61fb9568802ea8bb2cef871fd942c440d0e8d3a86d1237b` | 0 |
| ts/sql/migrations/1550-has-link-preview.std.ts | 622 | `f46890fc641e5b954e4880e732316a446280fb31861356fdc893f4fef84f4579` | 0 |
| ts/sql/migrations/1560-pinned-messages.std.ts | 1083 | `e3a1ef1b80950bb72494e42c62a009398d67cceae72804a1af122ea456682278` | 0 |
| ts/sql/migrations/1561-cleanup-polls.std.ts | 771 | `f67be707071559b435d7a76b2eb6547e4903569fbf3588a8580ca7ff742b7413` | 0 |
| ts/sql/migrations/1570-pinned-messages-updates.std.ts | 569 | `6e62177c8890684bf74cfc0a58afeebd40bf02593cfc180373127c5a0199361e` | 0 |
| ts/sql/migrations/1580-expired-group-replies.std.ts | 1009 | `e9b3d3c743783e8a300b4b1de94aebd571e851bb07990d7f8f8ca73fba9cdc11` | 0 |
| ts/sql/migrations/1590-megaphones.std.ts | 1003 | `e69d00f9695a30947efdb5c5eac6e8a88dcec8a9ac4b4ae41adb5cd87a1a8bad` | 0 |
| ts/sql/migrations/1600-deduplicate-usernames.std.ts | 1069 | `61d33e58e716f9f1d7fc9a958a13a0e81ee39213e842ff07d5ff89bb92c10456` | 0 |
| ts/sql/migrations/1610-has-contacts.std.ts | 622 | `756e460b9f94d7a620e491f56aa589fa7fd8a0fa72dcdbf67f168b226b3372ae` | 0 |
| ts/sql/migrations/1620-sort-bigger-media.std.ts | 507 | `c7144508bca88460570e253a5b474e828e03f63a1315ee3ef133bd65d9717267` | 0 |
| ts/sql/migrations/1630-message-pin-message-data.std.ts | 2184 | `e0b1fbded2b91a18b1d622bac44c0f9a08db67ef7a7d39a70578dceca5d7d6eb` | 0 |
| ts/sql/migrations/1640-key-transparency.std.ts | 357 | `c6f2e102288dac65074cdeb680b7fce8c2f81579f9f7f20ae88c59358051d171` | 0 |
| ts/sql/migrations/1650-protected-attachments.std.ts | 1760 | `7bccfd34341e0ec9e8cf8a75841bdded860b3ebe5c9fa4d3a9d7446401af26a0` | 0 |
| ts/sql/migrations/1660-protected-attachments-non-unique.std.ts | 1640 | `cd6fa9d957eae33fc3f496e6c0378d00ca96ac53efd21b352eee34d02afbee46` | 0 |
| ts/sql/migrations/1670-drop-call-link-epoch.std.ts | 395 | `4cf0666c1d788e071fae2186940a33f705b688a45df0a04aa58c3ec9c9392f0a` | 0 |
| ts/sql/migrations/1680-cleanup-empty-strings.std.ts | 2251 | `39e6a9121f01eb89bc9b3d52647ed5ab845a922f31492c124cb5cc88a6843829` | 0 |
| ts/sql/migrations/1690-poll-terminate-notification-timestamp.std.ts | 1091 | `c9a325c14040ca8398791cb8aaf1e66a68a55c699db6bca1a288217068ee0827` | 0 |
| ts/sql/migrations/1700-trim-profile-names.std.ts | 2016 | `1fb9e12d39a0e9d6c491c2861686cb71421f0e0d1665bbf04b132786ead8a1b6` | 0 |
| ts/sql/migrations/1710-emoji-skin-tone-default.std.ts | 764 | `c2f607d57e193ba2a5981c4c073c2b797f25c07c4711b8eb42869b5b4ebbad78` | 0 |
| ts/sql/migrations/1720-update-recent-emoji.std.ts | 2338 | `76e838f865336eb5e62d77410707eb36e0f5096f7125658a7eca5ad66859406e` | 0 |
| ts/sql/migrations/1730-protected-attachments-dedupe-token.std.ts | 937 | `221e396a29911716dc7e6fdd23675c0baeb64dd7e7ef70af5a907c75e02d5dd3` | 0 |
| ts/sql/migrations/1740-cleanup-groups.node.ts | 16222 | `20791f2c12760e66ed7eb12a1b7058c09685f8e475ab4d528fdbea12bdc57113` | 0 |
| ts/sql/migrations/1750-fts-url.std.ts | 389 | `46b50f4752a3c3dbd8958e33509bf95e21de4d0db99a608f89d645e6921e0a83` | 0 |
| ts/sql/migrations/1760-delete-story-reply-attachment.std.ts | 971 | `08580e42cdbeddcb4b3b8fd3a1f18cf06408c5c4c75699ea3e87f1069611504c` | 0 |
| ts/sql/migrations/1770-add-blocked-at.std.ts | 3318 | `4bcd2a1b3edd6c0c2bc4785b938478918b228ac2ea10f45d48e02e5d8ed2ca59` | 0 |
| ts/sql/migrations/1780-fts-reindex.std.ts | 385 | `0dcbbc9890b7290878fb0b03fdfc93d3c6d79fd4ec55711cb5195f5c46bb84cc` | 0 |
| ts/sql/migrations/1790-notify-for-mentions-if-muted.std.ts | 848 | `335d3e9e4d868d14a87627381ae697adf907758b45ef3fcc3bc9ae4a82e412a7` | 0 |
| ts/sql/migrations/1800-deleted-fields-for-defunct-call-links.std.ts | 1283 | `4531369a8b375ef611804e62486028b37943bd9e06f47f9e892921ee3f511272` | 0 |
| ts/sql/migrations/1810-sync-conversation-group-id.std.ts | 784 | `d277de926952ccd0227a18bb894e69d1b17b1e8e3a7b98cd2b12b9086e449e85` | 0 |
| ts/sql/migrations/1820-persist-waveform.std.ts | 306 | `86fd1b5b0805ee789bf01bad2e1e0e52a7c2a5ea298f0a7bd5deb85234ffc799` | 0 |
| ts/sql/migrations/1830-fix-salt-storage.node.ts | 1177 | `d36c854e55fa3cf716af01762f0d35d6ad618d875a748d3559000a3abd0b58f9` | 0 |
| ts/sql/migrations/1840-transcoding.std.ts | 320 | `359a86a3cedd70e256829d75204d383d5af10892cd3edc9789103bebaf7890e9` | 0 |
| ts/sql/migrations/41-uuid-keys.std.ts | 10222 | `db75c7ee30c172c7e7a793d3d5e8600efb3b27cab432c4fff773c8d84910a831` | 0 |
| ts/sql/migrations/42-stale-reactions.std.ts | 1962 | `f9e58dee6e0e94078ab64c985b7a5cd0ec7184938559c0672f6918e50df09c47` | 0 |
| ts/sql/migrations/43-gv2-uuid.std.ts | 10206 | `eff575dbf98556e97f6fbd2b482ef58f1caafc79550237257ed5c689f6ad21dd` | 0 |
| ts/sql/migrations/44-badges.std.ts | 634 | `d261f3c75ad1bb5cacd67ae242f6a032afe3fb451ea032ce5ba8e58cee4c1649` | 0 |
| ts/sql/migrations/45-stories.std.ts | 3737 | `c4a2ec13913c424714b093ab0725f1cf7085e3d04e24708857d3f784a24b445c` | 0 |
| ts/sql/migrations/46-optimize-stories.std.ts | 580 | `6a6348b27e074d527218275147ae843a4446d75cae702c7c97f5158b69d48104` | 0 |
| ts/sql/migrations/47-further-optimize.std.ts | 3602 | `b696e9aae59c69cbc8fed89c60bddc066dbb066631df76f51ed207c0a36002fb` | 0 |
| ts/sql/migrations/48-fix-user-initiated-index.std.ts | 374 | `8417ef25212abaaa51a21c4921be33f2836a0c15bdb280602a9acc04da4041d4` | 0 |
| ts/sql/migrations/49-fix-preview-index.std.ts | 555 | `ade4e52d8817864e951c3345eb4124347070f6b4e193b376ec35f5dfbd2aa9ac` | 0 |
| ts/sql/migrations/50-fix-messages-unread-index.std.ts | 513 | `dc141dfcef8c0fe92f68b8f36f0cd5d0b31ce822e39f0451c84296a666d890d8` | 0 |
| ts/sql/migrations/51-centralize-conversation-jobs.node.ts | 2242 | `b0c1d2198b8b62804a74d91e2ab243cd4c66e7600057c636f964897b72f4855e` | 0 |
| ts/sql/migrations/52-optimize-stories.std.ts | 674 | `99648bbd6ed6db9e79fda7e51898e097eddaf1ae353b01a9dd0d2d4b88d9503c` | 0 |
| ts/sql/migrations/53-gv2-banned-members.std.ts | 1982 | `c082622d0079082baf8a941b582be3c289bfadd1188216c656feaadf87abb5d6` | 0 |
| ts/sql/migrations/54-unprocessed-received-at-counter.std.ts | 306 | `882f9b18a4e6f82e1e8990adfffb45d1d1e77196452d64d4145ce6554c37e428` | 0 |
| ts/sql/migrations/55-report-message-aci.node.ts | 1512 | `2f05c125806fdfef6b8cd9fd4708ffd430ec4bc5aa75f507847ae20b3a51b559` | 0 |
| ts/sql/migrations/56-add-unseen-to-message.std.ts | 2031 | `42cab0a59db206fb4f02d67dddd418098a771bf47dea194d46400c92cc5381e3` | 0 |
| ts/sql/migrations/57-rm-message-history-unsynced.std.ts | 309 | `713c02ee1ff764314cf5bf82af699ec46881c95289de7925bfedc0a355dde97b` | 0 |
| ts/sql/migrations/58-update-unread.std.ts | 3179 | `d19d7389e4fd0b3c8179264b6c6f56a6e230a5b389bfe4cce46a6b69f92384f4` | 0 |
| ts/sql/migrations/59-unprocessed-received-at-counter-index.std.ts | 332 | `30cbe7c7bfcff4b229becbaeb58e9fa61d4d7b9880948f836bd2cfbb0630742a` | 0 |
| ts/sql/migrations/60-update-expiring-index.std.ts | 591 | `462d18d2b5da0ecfac6d10870d508179ed66623588548823cf216def348f527b` | 0 |
| ts/sql/migrations/61-distribution-list-storage.std.ts | 1071 | `8fb6a830e1ff7e636c02f755a5cd20c582f1618e50726c17b780263f16017a73` | 0 |
| ts/sql/migrations/62-add-urgent-to-send-log.std.ts | 297 | `519ff6bd106a206aeb9c073f07283797591c3fa9bb83867bc26022492f5a3980` | 0 |
| ts/sql/migrations/63-add-urgent-to-unprocessed.std.ts | 293 | `9850bce01649f0b165dc32939bd3caea3f3f9b471e686dd29bae6a842f64d75a` | 0 |
| ts/sql/migrations/64-uuid-column-for-pre-keys.std.ts | 603 | `11e1730f03a0dcec1366622d10d376adeaf30faed5bad67a230e040d5c69f208` | 0 |
| ts/sql/migrations/65-add-storage-id-to-stickers.std.ts | 1304 | `58c5ddf162ae8caad7409df0b30a457cf5b8fbd211c767ca152e29fa35bd8ab9` | 0 |
| ts/sql/migrations/66-add-pni-signature-to-sent-protos.std.ts | 336 | `a85c092b4281dbeae1790b17c81c697a4ff2ab65e1da463fd490e982dcff6290` | 0 |
| ts/sql/migrations/67-add-story-to-unprocessed.std.ts | 292 | `456a0b5a1dbdafff26603a9a441741cba53681eba33f3a86410a6262212af0e4` | 0 |
| ts/sql/migrations/68-drop-deprecated-columns.std.ts | 375 | `d7647ffe83eb12e8ee3afdfb88f305bc274bb62d0d1d80fb8bcbb7d891d3a48a` | 0 |
| ts/sql/migrations/69-group-call-ring-cancellations.std.ts | 399 | `b8ebbefa98a955abb2b9bffd7b2cf251bfac85107a58b49d9c05c5419944f57b` | 0 |
| ts/sql/migrations/70-story-reply-index.std.ts | 328 | `c1fe02abdd05b09d30e314466d651b1ce75427b37f307f43ea0b9af6e33cd5aa` | 0 |
| ts/sql/migrations/71-merge-notifications.std.ts | 3326 | `f789b390abb9b76f1ee1af5b20783b35c795d8c3b58c03f6a530919628d40d21` | 0 |
| ts/sql/migrations/72-optimize-call-id-message-lookup.std.ts | 631 | `8c7a3fc65975ddb66594f1f418f1d00d9e7cca7181f83893f32cf623d0cd8cd7` | 0 |
| ts/sql/migrations/73-remove-phone-number-discovery.std.ts | 2903 | `8a001f96ecf37a33f9cad64280cda6bd197be8886e4c1fccbdc20f4f919bc5b9` | 0 |
| ts/sql/migrations/74-optimize-convo-open.std.ts | 586 | `f2068e2320cbed6c12d1e6aa4868b96e8d0b9f19fba682008818de2c296a13bc` | 0 |
| ts/sql/migrations/75-noop.std.ts | 275 | `651c81a39ae936e490b61dc2747a96438a943c69f61543643c20ad5c922a7161` | 0 |
| ts/sql/migrations/76-optimize-convo-open-2.std.ts | 1323 | `da14024ac927433f3a0e06c3da012df4248e238c75d46d80836b0aee1b77c488` | 0 |
| ts/sql/migrations/77-signal-tokenizer.std.ts | 688 | `4aa109f77db231e19c285b054c2175402f1ad27bfb0ea1c4db83ec3a3467c6ef` | 0 |
| ts/sql/migrations/78-merge-receipt-jobs.node.ts | 3013 | `bd7c09c095d718190560c03d748c10498f576c04c64e7d025cadc2b88ed91908` | 0 |
| ts/sql/migrations/79-paging-lightbox.std.ts | 503 | `012ec6e1420c3449ab148520fc557d9c0c8d108b9ed233e3cc77c771e9cfc491` | 0 |
| ts/sql/migrations/80-edited-messages.std.ts | 482 | `5cbac7b2ddeff2cbfc6e787ada43beaae3e70332c3788ff81765a4dca40f07f7` | 0 |
| ts/sql/migrations/81-contact-removed-notification.std.ts | 3148 | `0ca8d2113ff588592ecf87d094cbc2038ccb7e0ae5f5f203f41c557f3ee2f95d` | 0 |
| ts/sql/migrations/82-edited-messages-read-index.std.ts | 436 | `a15e02abf074588c98da4554cfcf01933ca7690b85977bb1986a9fb5473e2820` | 0 |
| ts/sql/migrations/83-mentions.std.ts | 804 | `8d00a09b63efc067559a7f027a79f839a91c97fc5d67a7a40fbd6269ccb32cca` | 0 |
| ts/sql/migrations/84-all-mentions.std.ts | 1561 | `0e53660f3fb546e76ddb8dc7abd95ac1bb0fcd2e23f8d03163f45cc061ac84bf` | 0 |
| ts/sql/migrations/85-add-kyber-keys.std.ts | 722 | `c0c8288f2ba4b645d708a6d1019076605a394b6ed91a723a6f7d62c7e3e0790c` | 0 |
| ts/sql/migrations/86-story-replies-index.std.ts | 552 | `cbb45f9bd18ae8f462d2dca1378b75ff0171c2e0e14b526d63a5c5eb7ff88894` | 0 |
| ts/sql/migrations/87-cleanup.std.ts | 1383 | `e25ae17d22028f4cf806cd802a2bd28fd5e512912349617ae94eb9c1acd0d67a` | 0 |
| ts/sql/migrations/88-service-ids.std.ts | 32846 | `21231af12d857045f8f556aa4f5a7a8f47fa4d8ba49c605e2e2cf508114a0686` | 0 |
| ts/sql/migrations/89-call-history.node.ts | 11754 | `de5712a24dfc83157e2ca292a93445cd74af24725f2abd21668d09fb55072d2d` | 0 |
| ts/sql/migrations/90-delete-story-reply-screenshot.std.ts | 1027 | `2d274f8c6834f02306540ef6146b5a49e84cec7ad8df40447f750f3802f00950` | 0 |
| ts/sql/migrations/91-clean-keys.std.ts | 5109 | `0318b5795efab9d8ba80e945f17e0c0f4f7e148f9b2fc68826843b91dfb3be41` | 0 |
| ts/sql/migrations/920-clean-more-keys.std.ts | 4757 | `4d0a7c801c044468b1c53fb6c7867128353cb4483166d26dd4cf0d98d14d1d3d` | 0 |
| ts/sql/migrations/930-fts5-secure-delete.std.ts | 206 | `c7303df53416c9bedad3584ae0b86636df24f1d08730bcc0d8981480e568af27` | 0 |
| ts/sql/migrations/940-fts5-revert.std.ts | 220 | `ebed9a091dc094768c59941b15bbd2381e19a5a69bfdc87aa2bc10aa1970c68a` | 0 |
| ts/sql/migrations/950-fts5-secure-delete.std.ts | 196 | `c1525ad373c2434ad1a4033bb245a1f08425e71785e151b9bf628c4ac35d04f3` | 0 |
| ts/sql/migrations/960-untag-pni.std.ts | 5366 | `68e6c396ba7427498477cd26e5cf11c65b0f68ede52a9f0357aa733121566fbf` | 0 |
| ts/sql/migrations/970-fts5-optimize.std.ts | 293 | `9b4c7a29ce669a4339ba2189bdcb68842eec7ab0da92c167c95525bdafe57dfb` | 0 |
| ts/sql/migrations/980-reaction-timestamp.std.ts | 366 | `21579d41bbcd903646baeffecfd14f1d0560d8267c4b265108df4718ce72953a` | 0 |
| ts/sql/migrations/990-phone-number-sharing.std.ts | 825 | `29e82a32646183dfd18ba869795602976385e5b4254508d558c5785b695994bd` | 0 |
| ts/sql/migrations/index.node.ts | 58854 | `da506dc3a6a3e3dcc6a6fb70e9d8460ba577ca807859cc6dfb88d745de255e60` | 0 |
| ts/sql/server/callLinks.node.ts | 14762 | `e8db04893d2d8f4e6cb33536c1b3564bb94b99bb908b66d033fc41227fdd1e0c` | 0 |
| ts/sql/server/chatFolders.std.ts | 11913 | `e8e4e67eafeb884e44b494fd3adc10aa38ffa902171f79bd682120cfbf75e7cb` | 0 |
| ts/sql/server/donationReceipts.std.ts | 1440 | `6b1925ce99b931c62930c414ac93d64393523ba99d8ae744bff882cebfbf07b5` | 0 |
| ts/sql/server/groupSendEndorsements.std.ts | 5102 | `fc4486cce0cf50a5a080d805299f2eecc70b2f7a19af14c6cfff71b803165ca3` | 0 |
| ts/sql/server/keyTransparency.std.ts | 1222 | `939d806693e2caffe4b345e7de13f99115018da6dc58ca5440151cdfb17112a3` | 0 |
| ts/sql/server/megaphones.std.ts | 6582 | `31eccc56ef0fa2d821c1f0214fa03d5b48fa9bcc1a75aea5353f406bfcca615b` | 0 |
| ts/sql/server/messageAttachments.std.ts | 4207 | `d37525006cc2d7e032aad0e786eb6fc54b5119c6b3ccec0710cebe2660915ef4` | 0 |
| ts/sql/server/pinnedMessages.std.ts | 6187 | `27818c1da1827b56fa9be0602baf23ab8e4019ccb124d24665b194596a5c77a4` | 0 |
| ts/sql/server/unreadReminders.std.ts | 5631 | `dae43651dc8f612ac9b9369939e87ea39b11f2c07fccf3db73ac7c96b61edfe6` | 0 |
| ts/sql/sqlLogger.node.ts | 1713 | `010fc97d17056180b923262fbd1477c51d0e66aba281d6a8d2febcd56c2cd48d` | 0 |
| ts/sql/util.std.ts | 11731 | `c9feb5901fa42295c80846c0dd96a6f610481f139cc9f3c00b0e51039211e06a` | 0 |
| ts/state/actions.preload.ts | 3145 | `b3c3d46e6524c7701b382af4b9d0db082cadf230551296175de7e69f349278a3` | 0 |
| ts/state/createStore.preload.ts | 2677 | `bec8180f9ff17b579fe83b7452fa5577e7bff84719f4d0ec019e60c8e06389ca` | 0 |
| ts/state/ducks/app.preload.ts | 3160 | `671e9712321fd64cdb8d1d38ce00e485978aead4bab0e68ccd7d538289095b8e` | 0 |
| ts/state/ducks/audioPlayer.preload.ts | 13348 | `382d49c9fe8213470edf824dfcd8a219bf49bc2557607634a6a31fc213db8b73` | 0 |
| ts/state/ducks/audioRecorder.preload.ts | 7414 | `9feab5dc8103f982e8abbf6479b011b1e70d70ea9c25fa8992c01ac1ec7ec81f` | 0 |
| ts/state/ducks/backups.preload.ts | 16031 | `4094d9844e263939b4278fa571e106838df78dcdaff9ead0f0194b69cfbaa9b0` | 0 |
| ts/state/ducks/badges.preload.ts | 4806 | `1ea6715030561ed73e78b7a2f06f52ea82d365b46ab52130e771a72166c44219` | 0 |
| ts/state/ducks/callHistory.preload.ts | 9782 | `3d1e3e2ffba53108a1a5ce63cbcd043fac76e91b941ff390323adc3bd491d7c0` | 0 |
| ts/state/ducks/calling.preload.ts | 130817 | `02a9477c1ea313ec33a38d14d5f400fff02b6e9c8048b42e1c2dbe44afa2c905` | 0 |
| ts/state/ducks/callingHelpers.std.ts | 3984 | `f7139599847dc05b433ca8df9b5165281a5c3d084688b216352020701e5b344f` | 0 |
| ts/state/ducks/chatFolders.preload.ts | 12527 | `255c89d7fa56ee5a20370fd923624723ec9a952ee1f590786566099fde9e6b37` | 0 |
| ts/state/ducks/composer.preload.ts | 49955 | `dabcca371e0da85b8f31d934e6323fb4e7076face36ff904db60b1447c8553fc` | 0 |
| ts/state/ducks/conversations.preload.ts | 210706 | `a89d0d1adfe6b9deb4d93166075066587274d62e0c3996b9906c68ba10b8e24a` | 0 |
| ts/state/ducks/conversationsEnums.std.ts | 1014 | `a80aaadf301dc248794f19900aec73448209e08d05f637e334a10d2ac14a73e6` | 0 |
| ts/state/ducks/crashReports.preload.ts | 3489 | `5d8ecc582082375dc1f8eee4e6bc24f5089ed3611faa90d906e4b68ef04b4755` | 0 |
| ts/state/ducks/donations.preload.ts | 13173 | `a1d946356e75232a98bd4c13c7ff6b8280dbd775e693eb33601bb478a4a6d529` | 0 |
| ts/state/ducks/emojis.preload.ts | 2006 | `5106f9d7d0c692b599d0172cb6ceec4533b47c7d9c42c04bdc6690c469e7fc59` | 0 |
| ts/state/ducks/expiration.std.ts | 1205 | `c242440907c9f7d61f872c5d38deaaf1cf44d6e0d018b1529870ffdab9f2925c` | 0 |
| ts/state/ducks/gifs.preload.ts | 2906 | `d79514f7e177a2c34677e377bb409b4a0a5d2119bb6ea6443e82dd0dcd14bb26` | 0 |
| ts/state/ducks/globalModals.preload.ts | 61518 | `2e7f54e6b313cfe36e53fdee85bc1dece278606f7155f5bc3e693d180f42e8d2` | 0 |
| ts/state/ducks/inbox.std.ts | 1881 | `9280c95c311fb83232ae8d28c57bedb4f83a0093671143011812b91f96852ce1` | 0 |
| ts/state/ducks/installer.preload.ts | 18866 | `af70c23e2cd5a71e47d4c7bf4e3274af1ec4d54bc7355c26effec258eb7bcd52` | 0 |
| ts/state/ducks/items.preload.ts | 7654 | `e58c3cfd422160b9c31f0174cd1445fca4d77f64706e104a4d19343c1052a5cb` | 0 |
| ts/state/ducks/lightbox.preload.ts | 18653 | `2ba8bb0115df448f52803b22ef8471b71b54b3e25cca395fe0307ae3196cc413` | 0 |
| ts/state/ducks/linkPreviews.preload.ts | 4168 | `5ef7cb7fe33669c7be3a4858bfdc1794a69fc0a548d7fa07c0a4226806d93323` | 0 |
| ts/state/ducks/mediaGallery.preload.ts | 21371 | `5e5924909fe2bd952ca0d711215aa3fbf94b6131e09255ebb9cf706e1427c4d1` | 0 |
| ts/state/ducks/megaphones.preload.ts | 4438 | `9a2380ed3c8f2f98d44f0042d799adcb0f20f29a22662da9a1872f32aedb5b19` | 0 |
| ts/state/ducks/nav.std.ts | 8809 | `1d191b9b2eb7a6cc398904bd00f5d9c729fc523fee9ede70851afc61fa8c5ba8` | 0 |
| ts/state/ducks/network.dom.ts | 4503 | `7092a0b8cf3c378a89da853d3e8dbda78b74565996e0118cc79d07b69fb57075` | 0 |
| ts/state/ducks/noop.std.ts | 347 | `7d2094c5117bdd9dfe8aba7532ae17eea74216b22ff6913b34e99c033a081816` | 0 |
| ts/state/ducks/notificationProfiles.preload.ts | 16608 | `3882f3da7061df1df4253d7bb90b3642e81ec048a9dada934a6b40d04f35e1c1` | 0 |
| ts/state/ducks/preferredReactions.preload.ts | 10251 | `0433ee855e4226dfae8ba7c5456ebbf3bcda196a522c9b5e6b8cba94dfbaa80c` | 0 |
| ts/state/ducks/safetyNumber.preload.ts | 6395 | `ae4722ac20343a7d8bdd8b8a7729a0fe31d01e54a5d4d6ac1ab50529c1b6597f` | 0 |
| ts/state/ducks/search.preload.ts | 23271 | `5ef214bb6823da337212c873e3f70fd52435f8d30819d90a1638800e0ae74155` | 0 |
| ts/state/ducks/standaloneInstaller.preload.ts | 43617 | `d8ddb63a4a2c4ab358fd6f57f66e0ae83c7172b8e466c002a5d4d369dc5b0b41` | 0 |
| ts/state/ducks/stickers.preload.ts | 17402 | `aec6d55cf0319efc3fd7aa4484d3143095a9938840666793e48fdc89035e6a96` | 0 |
| ts/state/ducks/stories.preload.ts | 52803 | `14593e3fad4be56d527963e4cf0c4364050130bdb0fbf9230299209e7aa5253e` | 0 |
| ts/state/ducks/storyDistributionLists.preload.ts | 18553 | `f084185ea4615766e0f4b1dc1b9e1e1488039f377cf34b632b92fd28f6ff7e62` | 0 |
| ts/state/ducks/toast.preload.ts | 2400 | `6d5413aa98caa64a3b1ce1a4e9af5aebb9527b1f7e8f2eaabd8ece681aa48dd5` | 0 |
| ts/state/ducks/updates.preload.ts | 5703 | `74a3cd674628dc639213f1571d956eec658f1281137b36a8859a1d673f0922c6` | 0 |
| ts/state/ducks/user.preload.ts | 4590 | `4db0d73a13ef95e7d65676c365bbced6812e4ff5af22e639d6efb220cb38db7d` | 0 |
| ts/state/ducks/username.preload.ts | 17254 | `8e916b9446829fdb0d88911dc69167f62e6952c802d640251d7ab14bea6535f3` | 0 |
| ts/state/ducks/usernameEnums.std.ts | 1049 | `abe6a175c063b13350586b96a0fc3d24b995d47a20ce06586c1a7f1f5261ddd6` | 0 |
| ts/state/getInitialState.preload.ts | 9343 | `f7f586eacf0faf6380de42852965ddf96c38d1d236b7e043af010c563ac938ad` | 0 |
| ts/state/initializeRedux.preload.ts | 5361 | `cc6e0846008ddab754b9e20b09adb4531fa0178ae55e7d69c007ad277e0dc217` | 0 |
| ts/state/reducer.preload.ts | 3293 | `691b90758289e5ffdd08bf68889daedbe564d1b74ebebb83e6c630bf88c91407` | 0 |
| ts/state/reinitializeRedux.preload.ts | 1795 | `34d6c36361d3fbd7c56f73762a84537a8b498e2aee3e70a764a34d8d09b02aef` | 0 |
| ts/state/roots/createApp.preload.tsx | 664 | `19971990677fc82833fec9f9fc7451caef418fd96021cc0af1631798ec8d57bc` | 0 |
| ts/state/roots/createGroupV2JoinModal.dom.tsx | 909 | `ab25c58c86d50958933a89a97763abd1e8cecdc326385d43e9b5ea4e248e3d03` | 0 |
| ts/state/selectors/app.std.ts | 443 | `f9827d90c9a02d2c301b038f90d99040061efcc5ecde8518c13ae880a0795246` | 0 |
| ts/state/selectors/audioPlayer.preload.ts | 4944 | `a06f6ef36f7109c55d7967771413b6cf1fab070556f80ccd209978977da3b40c` | 0 |
| ts/state/selectors/audioRecorder.std.ts | 801 | `8ac04b980b178b3429201d6f156ff585b69c8ec06e18cba11ab8c40aa04d08a5` | 0 |
| ts/state/selectors/backups.std.ts | 1523 | `83ddd9370db62d8a0d859f428e6920b15008209389f48ed74e718bcbe14d800a` | 0 |
| ts/state/selectors/badges.preload.ts | 2777 | `c339de2dbc3bd6b32f28a2d4bf1ee111eeb7206eeb4e9597ea90d584a9210aff` | 0 |
| ts/state/selectors/blocked.dom.ts | 3011 | `4fd9661e6e387aca050366852a891c35e1c68b61bcb9a2ec8e3c442a081c257e` | 0 |
| ts/state/selectors/callHistory.std.ts | 1621 | `6a40f3489ff447c5dce45688be19a62a5fc388b90959d0f21a6f6c4284ebe0ac` | 0 |
| ts/state/selectors/calling.std.ts | 5617 | `ecea957f129634721c2eb3c7bc010b1341324d722df835b2fe20847992a106cc` | 0 |
| ts/state/selectors/chatFolders.std.ts | 1785 | `43cad936860896cf13e0b423d5f5b8336fdced25faa9790161b7974fb09d4911` | 0 |
| ts/state/selectors/composer.preload.ts | 953 | `85a8cc991912502bb1dff986cd66170f2ad6f90bd52d375d1b22e3ef9b38ad7e` | 0 |
| ts/state/selectors/conversations-extra.preload.ts | 4144 | `ccf3c012a52e90f8f578389bd1ab5789978c72cf5e6526830d6c744afd1a952c` | 0 |
| ts/state/selectors/conversations.dom.ts | 48290 | `32b23f8614d158c3c1aa53e034a9f881f3b6c9dabd258775dea63c876bad7708` | 0 |
| ts/state/selectors/crashReports.std.ts | 559 | `a6d554c97a47fab73db42415b4e3721f4760baa4aa7247b0a534633163ca781c` | 0 |
| ts/state/selectors/donations.std.ts | 706 | `0b8585aafc393974502957aff6eb48cd4ea1463d3b22592611225f6f66a73369` | 0 |
| ts/state/selectors/emojis.std.ts | 609 | `fae4789ec65717d62d54f37a2d1c0376a2630bc2c93e59d1c888fc51538fdf02` | 0 |
| ts/state/selectors/expiration.dom.ts | 1684 | `5a9691ac29137fcc2d891ea3e9c5d56a6bd81be298842cd13fd2c9b32b614bae` | 0 |
| ts/state/selectors/gifs.std.ts | 410 | `42b98efebda2408c3fd0a4c195d59fdb5af7eee4cc4bd11f5d364147ac0fc5a0` | 0 |
| ts/state/selectors/globalModals.std.ts | 3881 | `9f7c4c3dfc510e68fb9f37e77fefa58b2ce64962a216417399489718ce61e819` | 0 |
| ts/state/selectors/installer.std.ts | 307 | `3a5560e2bbe9fc1f5c38b1c8c8427f09e4e85807bdb42e773973aa0e1a1be818` | 0 |
| ts/state/selectors/isInFullScreenCall.std.ts | 1362 | `afaf3c63f3dc50506827333090b71d8c134ae8c10811d40a211101666ee958bf` | 0 |
| ts/state/selectors/items.dom.ts | 11223 | `0ffbcb89e68e0fd810963cb05588beadaff49314237ef1954b23d7a1ce63c66c` | 0 |
| ts/state/selectors/lightbox.std.ts | 1522 | `0af4bca85d366fb4211b25f9e04837f08633e6b74a346ba6d155508c8f6f8db2` | 0 |
| ts/state/selectors/linkPreviews.std.ts | 592 | `73933d4c198ee57999a170119951d4461ac0c8b2cc888a01c43aef8446cbc4c1` | 0 |
| ts/state/selectors/mediaGallery.std.ts | 322 | `95e22b4b0ea887282cf6249b253ef43c5945dac483873a6320f18f6246bc7e7e` | 0 |
| ts/state/selectors/megaphones.preload.ts | 1572 | `a7e23ab438d1ec360782e01fc5fb7facd8db9f39e5c518a97451397a13de8a29` | 0 |
| ts/state/selectors/message.preload.ts | 82634 | `23077add65dffe16946f26045c8fcedb6498f9bf91f0ec790bedd9ac49e37795` | 0 |
| ts/state/selectors/nav.std.ts | 2554 | `10c1013eb2763db55daf233a003b5d05e4b8fc63eb667810fb1327fc46fe9f57` | 0 |
| ts/state/selectors/network.preload.ts | 1277 | `34fb0b33cacb71d82fa57fa65339819c22c0a0f44771bd0fb910935c350ec221` | 0 |
| ts/state/selectors/notificationProfiles.dom.ts | 2673 | `147a1e56278f0c23dd63b19fcf9ebce55120b3b5f0eae4d922e3c2234fa6014b` | 0 |
| ts/state/selectors/preferredReactions.std.ts | 735 | `6025d28c27dd9eb1876c50d968eb6211e20d6d8e29463f58d8b957c34b3ec6c9` | 0 |
| ts/state/selectors/safetyNumber.std.ts | 544 | `e5282cb927325a8c0c808684efb3d91afd76c0984b3d503786fada11637495e4` | 0 |
| ts/state/selectors/search.preload.ts | 11411 | `0224e939e0f9cdc71fc24b72c4c0ab07a56860f3ea467e09186e09ac031c5afd` | 0 |
| ts/state/selectors/sharedContact.dom.ts | 1637 | `f919cd4acd43ae74cc9c4f1b067b257fc31319adeb5189ea027197aec7280ede` | 0 |
| ts/state/selectors/standaloneInstaller.std.ts | 1138 | `a15fcdc56efc765dd671243a135916b65f7b420a5085d7c349fc5fb6890f83cd` | 0 |
| ts/state/selectors/stickers.std.ts | 5395 | `ec9f6e729559127bc5cb2cc37a50d808a35b2a99dbba1fa25fc906958ffc9574` | 0 |
| ts/state/selectors/stories.preload.ts | 15678 | `185707392dfe22d81e8d04bece42ea35befb69243a966f70db22f95f2a50729c` | 0 |
| ts/state/selectors/stories2.dom.ts | 1266 | `b235a03f34908a5c82b7da47df09771f5d1a216a81df46e206a2b9b0239b659b` | 0 |
| ts/state/selectors/storyDistributionLists.dom.ts | 1306 | `e4138b253a3bdae2f92c93a9a91ff77bc7164da832fe8b74b2b3168fd9e48b28` | 0 |
| ts/state/selectors/timeline.preload.ts | 7215 | `7017dd57205683d01c77f08423d48079e38fb1c240cb5acb9df22099aeef46c2` | 0 |
| ts/state/selectors/toast.std.ts | 408 | `2e6042f7a766bd240a77f17e210e3014c4a8f3078836126a82ed91c5e1d5f4f9` | 0 |
| ts/state/selectors/updates.std.ts | 1648 | `8a4ae87bf9fc63785ee58f56015d3bf70a5c4525253b8882a38a92e1957ca822` | 0 |
| ts/state/selectors/user.std.ts | 2625 | `fddaf11bb4860394c1a797b3288b4e5ee8f94df85d67ed7ce5e42274c63cd08a` | 0 |
| ts/state/selectors/username.std.ts | 1832 | `b7cdd01241eca59cb2d15b16cf083a818be5663b30746b12c810c31e00830a08` | 0 |
| ts/state/smart/AboutContactModal.preload.tsx | 6407 | `25bddcd9d4ea89097ce24413a35796de3426bc71fdea0585ed432aea69b74c8a` | 0 |
| ts/state/smart/AddUserToAnotherGroupModal.preload.tsx | 1693 | `6f8324224f7f5de04af55e3f24a99aef3e8a2d063f42546fba3b4ec17b667855` | 0 |
| ts/state/smart/AllMedia.preload.tsx | 3783 | `af25261eabc6f28bf539cf51a0ec9f975a318ac2b9ee6a9ab4570ef978101045` | 0 |
| ts/state/smart/AllMediaHeader.preload.tsx | 849 | `9b5b01634c36156542f71fff64bc863fececb02d1c4055eb37762579c06e7ab3` | 0 |
| ts/state/smart/App.preload.tsx | 3651 | `bb07d21d26d78e3de1f3af43bffcd3d0b7f794b514315081ae3df5bcec3fefe1` | 0 |
| ts/state/smart/CallLinkAddNameModal.preload.tsx | 2135 | `93ea42722b2f44fee3e14adf9edad845dbcc50d984a8042b6839f919bf9a338d` | 0 |
| ts/state/smart/CallLinkDetails.preload.tsx | 3624 | `96736347334f0101c36ec56d3d99a9fd4e3262c5279fbcccedeee66d27adead4` | 0 |
| ts/state/smart/CallLinkEditModal.preload.tsx | 3842 | `4ce42744178235e8d516266dba188cd57f70afe709b3920b1ac3df0f4e5860c5` | 0 |
| ts/state/smart/CallLinkPendingParticipantModal.preload.tsx | 1787 | `249c25e649ca6aa3cf6d9ba8160dff875076abb1a6576eae0ee5349315ab4606` | 0 |
| ts/state/smart/CallManager.preload.tsx | 18540 | `627f03276a8feaecf63426f15004516e256fa7b996d0ec6aa54b847d1902c86f` | 0 |
| ts/state/smart/CallQualitySurveyDialog.preload.tsx | 2539 | `7e7bafa258a4751b49942f86371376df4dac75a460e66ccf134067ff0ccd1d66` | 0 |
| ts/state/smart/CallingDeviceSelection.preload.tsx | 1576 | `2aacf59f82b848596a8eccfbddaf8c78461d830f8294176c905c940c57d720d4` | 0 |
| ts/state/smart/CallingParticipantMenu.preload.tsx | 5289 | `603ececba83d6e562713c37f4f43b7b0427b41a60ae626cd8cea688315b814ab` | 0 |
| ts/state/smart/CallsTab.preload.tsx | 8588 | `fa93d13de779767352af873302fbd3b7d3c8e0eba741da41bd870d8decc9614b` | 0 |
| ts/state/smart/CaptchaDialog.preload.tsx | 1111 | `01b4b96428ce9c770cb2269fdb4dca2ce638c2e0bdc3e508e6e122d4e0bb4623` | 0 |
| ts/state/smart/ChatColorPicker.preload.tsx | 2934 | `0ec6e85c27d3b6289c110ba9de3c5edbe9c98487548d93a97c113f96fe714005` | 0 |
| ts/state/smart/ChatsTab.preload.tsx | 5707 | `c6ed7cc58ccfc4b32206f24b369f5eea15d4bc05825cab332394c791b0a3d4c8` | 0 |
| ts/state/smart/ChooseGroupMembersModal.preload.tsx | 3136 | `e11459a928a967e78344c348f40ca6076cd9ef8419143dc79d810352817ebdba` | 0 |
| ts/state/smart/CollidingAvatars.dom.tsx | 1009 | `12ef058126c213736c5ff6ec295d7fadd02ad099f1431d6a1d2fd5514083b7c9` | 0 |
| ts/state/smart/CompositionArea.preload.tsx | 14611 | `ffbf65232e4c9338a735668c6e9d68c235225eb6fde1ff1965fb798ed570265b` | 0 |
| ts/state/smart/CompositionRecording.preload.tsx | 2219 | `720cd7368085c7fb89c281517f1c89935a6a65ecdf44dcd7c890c5ca2b22b1a1` | 0 |
| ts/state/smart/CompositionRecordingDraft.preload.tsx | 4790 | `3fd3ffe53b81001debc229e9c292ef8acacfcb8488be45e795ef918c02fb7d6b` | 0 |
| ts/state/smart/CompositionTextArea.preload.tsx | 2674 | `452b23d13c449395fa0caf730a07b91bcb9f5e1b15dfe7cceacfc7953e02f669` | 0 |
| ts/state/smart/ConfirmAdditionsModal.dom.tsx | 1783 | `5037509ba4e0c4d63ffff849e05f6160c19a771977abaf16294b8b3890984994` | 0 |
| ts/state/smart/ConfirmLeaveCallModal.preload.tsx | 1279 | `152e60cb8c92f735aa7021131985dcd118ac13708f9d416fb2e6d3c34132a068` | 0 |
| ts/state/smart/ContactDetail.preload.tsx | 4210 | `1b61a21540be9e8279215ac09747bd9100409a2edb6cbafaf58ea485fdfd16de` | 0 |
| ts/state/smart/ContactModal.preload.tsx | 7060 | `0b7717546c6e1f435c928250c8954650a6c9f13dc7e2446c52d733e0cdacd4e6` | 0 |
| ts/state/smart/ContactName.preload.tsx | 1326 | `0d312b81c22c15d2d029f8cb34a49fc69c69ef4b5e0ad04f9951e83472fa245c` | 0 |
| ts/state/smart/ContactSpoofingReviewDialog.preload.tsx | 5021 | `d09a0e651415184bbc7c0fd2af2ae18d3b190a74b20950faf713a6cbf088f2cd` | 0 |
| ts/state/smart/ConversationDetails.preload.tsx | 12016 | `540b5a42859047610c67fb55fca714a720da1747b79c868f04d848ce2ea4c865` | 0 |
| ts/state/smart/ConversationHeader.preload.tsx | 13342 | `afa5ac6ac1600af2c069079fcd61d9f202f06d3abd51a5eb61e2a3bb81e151df` | 0 |
| ts/state/smart/ConversationNotificationsSettings.preload.tsx | 2974 | `24622c9ca3eb0294d57fa1ba2c05a9bc67f3edb7a343d252749afb65781c641c` | 0 |
| ts/state/smart/ConversationPanel.preload.tsx | 13924 | `a8ebbbdedd754ec7e802f5dbf013a16bcaf0bb6965b115c150a30c21badd3919` | 0 |
| ts/state/smart/ConversationView.preload.tsx | 2713 | `05e99bed40557ca2a0a01ebdb4bc0046b5cfa7ef47947e0227da25519806a66b` | 0 |
| ts/state/smart/CrashReportDialog.preload.tsx | 869 | `68d77661e7f38e43ea6d9b2b45c9eea2c25919a1892a2e39312a46281d591a66` | 0 |
| ts/state/smart/CustomizingPreferredReactionsModal.preload.tsx | 2604 | `64a05a929253bcc04e089fd77d11891bc6d50601e8f9d8cf2696a7bc4c8d4245` | 0 |
| ts/state/smart/DeleteMessagesModal.preload.tsx | 3863 | `2fbae2a4c41fa3656a8b44273861bae5f0ff99a5c19abae62a3fec6caf942bdb` | 0 |
| ts/state/smart/DiscardDraftDialog.preload.tsx | 1730 | `d177f2240b09c9dfd2c86037a109130d6e36be8ac89d892a17ffd610aa2f3830` | 0 |
| ts/state/smart/DraftGifMessageSendModal.preload.tsx | 5722 | `5ddc93c3ae7f28d8268ba08b5ff4255c3b6ec0fc55c0363696e93b31f4e5df02` | 0 |
| ts/state/smart/EditHistoryMessagesModal.preload.tsx | 2671 | `6a011f8586389e1118c52f22c5e0fc1fd94a9b1810ca919ecc2d8ccd90a1e7ff` | 0 |
| ts/state/smart/EditNicknameAndNoteModal.preload.tsx | 2231 | `db35d77083fd2a059122e71317c40cbb6c5acd0ed02864f7fc862d774e968606` | 0 |
| ts/state/smart/ForwardMessagesModal.preload.tsx | 6248 | `fd970d5d400f622609eb263802d2f107b55238f6376d707204dad40418f868a5` | 0 |
| ts/state/smart/FunProvider.preload.tsx | 5158 | `26a6a89c7785f399c50a6ca79eaaa1646388aa9f0a2eb2b0a3c55a7f0ca1ba1d` | 0 |
| ts/state/smart/GV1Members.preload.tsx | 2378 | `27d9224c4e6531a470f1f911e6fe5225baaba1a38645bd022665e1d2be3d2d1b` | 0 |
| ts/state/smart/GlobalModalContainer.preload.tsx | 15964 | `d006ec424fc0c6e4b191f9d791ba6b8daae227177322a6a91e280e6320411439` | 0 |
| ts/state/smart/GroupLinkManagement.preload.tsx | 1390 | `c1f5342e9859cea78a6f525baac43cb39310eb9329b739aa85fcbc4add4d6b2c` | 0 |
| ts/state/smart/GroupMemberLabelEditor.preload.tsx | 3670 | `b3728d148ea4e4738e1d9285fea8991bb87231b30f5820fed6b556f1624588cf` | 0 |
| ts/state/smart/GroupMemberLabelInfoModal.preload.tsx | 3342 | `41780f45654a6fab722e6383f3c1bb4b1b3516c6775e61b03f595e7cb8684b6c` | 0 |
| ts/state/smart/GroupV2JoinDialog.dom.tsx | 1294 | `c965461cce332cc7da97a4e5b1635e847a6c530fc350ae206e68a8ec0d2997b5` | 0 |
| ts/state/smart/GroupV2Permissions.preload.tsx | 1414 | `d0dc19b2c303617256dfe78b0ef98a5e085fbc4a667d1a45ba57b1d38df76e65` | 0 |
| ts/state/smart/HeroRow.preload.tsx | 5293 | `202be7f8d61565c8bee1b8ee7158d336512cbdb4678966f1f327e220e9dba667` | 0 |
| ts/state/smart/Inbox.preload.tsx | 2146 | `296ef6865025456cdff5d5fb7946561b2a1b1356f72c85377dde7eadb9588c49` | 0 |
| ts/state/smart/InstallScreen.preload.tsx | 3934 | `a4906ab70b3031000e895bd69ed06019de2fe366156f23f0ef0bf4cb91c7710d` | 0 |
| ts/state/smart/KeyTransparencyErrorDialog.preload.tsx | 2380 | `f04427b1370a5abd2d5112e234dd2d41bd6b6e1ba7ed4f1138a880b829f6f4a5` | 0 |
| ts/state/smart/LeftPane.preload.tsx | 21698 | `7b521a4c6c09bcb9163914ae261d975e79ce314416cbb58a2d70c9cad296fc47` | 0 |
| ts/state/smart/LeftPaneChatFolders.preload.tsx | 3011 | `443a3e0870069fb6c3253a8b484ef842dd8e4257b16b91178dcc417eb48f7b7b` | 0 |
| ts/state/smart/LeftPaneConversationListItemContextMenu.preload.tsx | 4145 | `9d2fe6cb2e68d37345c593a6343780fb1528552302a00d78f9a0b4a4c66d45d6` | 0 |
| ts/state/smart/Lightbox.preload.tsx | 3109 | `6bd17057ea18f3be417574e322761c38719491852da39f9b76e478e463498fa6` | 0 |
| ts/state/smart/LocalBackupExportWorkflow.preload.tsx | 1886 | `3d82e72878570607176706b44133b4efde86eaf2f85a3d7e443424b3b999d627` | 0 |
| ts/state/smart/MediaContextMenu.preload.tsx | 9325 | `e8c818301e333606694601aa0be3805175ce898c7e965617632e11833784730e` | 0 |
| ts/state/smart/MediaItem.preload.tsx | 4723 | `4595112e339dadce8a95741e573594e3592301134762d891fab7bde949160539` | 0 |
| ts/state/smart/MessageAudio.preload.tsx | 2973 | `471b17099c72a720852c944464d2d820cf815c635e391488b399e229da237d6c` | 0 |
| ts/state/smart/MessageDetail.preload.tsx | 5960 | `92b99badfb87eead48739359d5ce1afacd6fc721f08c9690c53ce61192ebe079` | 0 |
| ts/state/smart/MessageRequestActionsConfirmation.preload.tsx | 3446 | `349137b087481581a2a9ecf641f61894738a61fb8d85267a92043b751bf50286` | 0 |
| ts/state/smart/MessageSearchResult.preload.tsx | 1756 | `b338cf8d360a35578a0c3e2894e85e8fde88ec8d1ec34717092112276decea65` | 0 |
| ts/state/smart/MiniPlayer.preload.tsx | 2141 | `c6e8a5153bca1af91aa81852910c79f401b70f5bfe1630ce90c41c665512fac6` | 0 |
| ts/state/smart/NavTabs.preload.tsx | 3043 | `a1899a73ed96d56c3776f3aeaf5038344f0397e9ddb951b9a3d37e6a9f01f3ca` | 0 |
| ts/state/smart/NetworkStatus.preload.tsx | 1264 | `a68e6934cd230515b0d40b028ba47d559f1cb5e66570458a2022c0b7a964a64a` | 0 |
| ts/state/smart/NotePreviewModal.preload.tsx | 1556 | `115d1087dcc870ab20fc7102ac69ab9cb79d5884dd59f95ec941b4ca6d33a112` | 0 |
| ts/state/smart/NotificationProfilesMenu.preload.tsx | 1525 | `671eb97c025186e4baf4e3dfecaa70926e91b749d46ada8ccaef2bd1c892dc77` | 0 |
| ts/state/smart/PendingInvites.preload.tsx | 2213 | `69410c7cd34d45054fc0c66e1dc15eff73d1ebc7f860c52b00bbd9da2f98a89a` | 0 |
| ts/state/smart/PinChangeModal.preload.tsx | 820 | `2504f4ef50ed9aa6cce367b697af7845a82f86a855bf8415a961e72c06f44483` | 0 |
| ts/state/smart/PinMessageDialog.preload.tsx | 2389 | `7906a1f3fc3ed32bce544f1072b7b99da3a51f0a93ea20f49e89825455d87fa7` | 0 |
| ts/state/smart/PinReminderModal.preload.tsx | 1420 | `cb7a73628e19c2c2a41eadf734963c1e04a449f40285cffc3b855fae4fec7d06` | 0 |
| ts/state/smart/PinnedMessagesBar.preload.tsx | 13866 | `7d2f06118d0c1fabc57488c0a1b0af0f2fda2e131305593e730b1b35ba529d5b` | 0 |
| ts/state/smart/PinnedMessagesPanel.preload.tsx | 2260 | `cbf80143f431aeab6aeaf71e5cb1c90c34d6bc0095f49f5fab0fcd3504af3f1d` | 0 |
| ts/state/smart/PlaintextExportWorkflow.preload.tsx | 1925 | `c490f1581f75d8795e9de7ad243278213b1de7b78c956cb527559b4bd0a398e8` | 0 |
| ts/state/smart/Preferences.preload.tsx | 47811 | `5233f9184234e53a1abf0819b32d762cd9f4d273080793cbe1c7318ce89cf319` | 0 |
| ts/state/smart/PreferencesBlocked.preload.tsx | 1600 | `b1622f6cb6b00ffcacfd35ce869052da8a0e9be412316956f0924c35835aaf27` | 0 |
| ts/state/smart/PreferencesChatFoldersPage.preload.tsx | 1873 | `205f32862bb5b3653d5caa2a3c87d02221205b3b36c0f59c412a983c9ce467e3` | 0 |
| ts/state/smart/PreferencesDonations.preload.tsx | 5774 | `94d72f4377a02d6d3e8133416a35e9070e585054135cea9765130ec7e8ac6ec5` | 0 |
| ts/state/smart/PreferencesEditChatFolderPage.preload.tsx | 3148 | `62ec0a769678666f6ee587a815c9fd054ee97045e0320aa90240943a3513a172` | 0 |
| ts/state/smart/PreferencesNotificationProfiles.preload.tsx | 4460 | `f3caa0a123b13f07671402804dae04f5e8e840f34042447b681b4fdd397bdb55` | 0 |
| ts/state/smart/ProfileEditor.preload.tsx | 5319 | `8b9ed8e21b6dcaf8a081177a3d1c380d2cfb9284847ae9e67c84253d3abefe28` | 0 |
| ts/state/smart/ProfileNameWarningModal.preload.tsx | 1215 | `2ba1bc6a967ea14bdc4fdb573625e6da6076fe98049f6e80a3dc9b8f3002ab3a` | 0 |
| ts/state/smart/ReactionPicker.dom.tsx | 1164 | `4b2a8b84cecf3a107c9c04ce045d9b257a322fa66130d20d5d6b7dffc8eb02c4` | 0 |
| ts/state/smart/RelinkDialog.preload.tsx | 1186 | `bb1a40c54a7c79907fc95c7ce25041a8f9ad60a6fa13ce5ba12a0d47c7a62ce5` | 0 |
| ts/state/smart/SafetyNumberModal.preload.tsx | 1385 | `ce784fb1512d183babb2d9de4c248c1fc67cc839af6c6d73d9e5511f0548f898` | 0 |
| ts/state/smart/SafetyNumberViewer.preload.tsx | 3662 | `8b81c8fe6e75ed383d062fbff5aff52b13b8e9725dd618fadb3d9d5a713d699c` | 0 |
| ts/state/smart/SendAnywayDialog.preload.tsx | 3717 | `b66f40d120b8d76b2b3da33d3c8ca841e7715a5283d71c1a97d7bafb6cb2b365` | 0 |
| ts/state/smart/ShortcutGuideModal.preload.tsx | 757 | `47fd5481b4fcb9ec886d9a8b735d7a7511f36c7fc3e605bd755a9e2fce557329` | 0 |
| ts/state/smart/StandaloneRegistration.preload.tsx | 4748 | `9abc724f7d9e94e913da25e2346844fa2138a5f29bcd2df2278e0892cb39cfcf` | 0 |
| ts/state/smart/StickerManager.preload.tsx | 1930 | `b943737045f1f91eee877d1ab69988c7c020c9bf8274e64cd2fa56bddf08f823` | 0 |
| ts/state/smart/StickerManagerHeader.preload.tsx | 817 | `5ab4d2bf63492781a4c3d929aa563beb51ceff7a2e1d11c65a1fa8a1bc563e3d` | 0 |
| ts/state/smart/StickerPreviewModal.preload.tsx | 1551 | `a9ad7d5088baeac8452fa6ee21110935200ebee4576adf9cc5e369aaca427c33` | 0 |
| ts/state/smart/StoriesSettingsModal.preload.tsx | 3863 | `36e0d3fcc4c928d2a41c362204f2579ea2ac60c7fb1795ef46fc25736c5e5b38` | 0 |
| ts/state/smart/StoriesTab.preload.tsx | 5470 | `999c7109a15359967942c60cfd5e4744fbb6348f982cbdff0297683de78a7a12` | 0 |
| ts/state/smart/StoryCreator.preload.tsx | 6718 | `a542696fbf2bf82e4f57142d7193e095c9c361ad5d083ac6d209715dbdbed92b` | 0 |
| ts/state/smart/StoryViewer.preload.tsx | 6674 | `ca0dae575f9fb24d81b18ccd88899866110f984945f1dd3a4d0b0e75116106c6` | 0 |
| ts/state/smart/TerminateGroupFailedModal.preload.tsx | 1058 | `f63ee27c63691e64458752bf875d313ef497fa2a280647143ec0fe048dd46458` | 0 |
| ts/state/smart/Timeline.preload.tsx | 9058 | `34c40c429be974a56ed17b9828637e44883ee2958548d3865ba1405957eb09bf` | 0 |
| ts/state/smart/TimelineItem.preload.tsx | 12677 | `4e6930bc81280128728ce6919d45d1b30cc8bead920eb487b242c050de62cbda` | 0 |
| ts/state/smart/ToastManager.preload.tsx | 6383 | `5ac73beebc7f04b3aff64eaaa097a35461d50e22bbb13ddb95ce974cd02bb741` | 0 |
| ts/state/smart/TypingBubble.preload.tsx | 2361 | `ebf025fcb0f2e5a7dfbeb7487e37cb4d532313fd979d6af8290e7d071d013be6` | 0 |
| ts/state/smart/UniversalTimerNotification.dom.tsx | 678 | `cedca5545737ce0a22407630941a911b77d38dc7673783ff42481e1b8d1ad7c7` | 0 |
| ts/state/smart/UnsupportedOSDialog.preload.tsx | 1018 | `a5328859bc905e5117a8508aa3127ca2836d0d13ea9319e41e2723693236ba7d` | 0 |
| ts/state/smart/UpdateDialog.preload.tsx | 1907 | `f88ca6935baa75833ced08e5d61d76fdb83718da80beb724ded1802823f87d5a` | 0 |
| ts/state/smart/UsernameEditor.preload.tsx | 2273 | `3301a09cbef12de4b83ec2850d76e9513497aba7e4767695f281029af6dcd5dd` | 0 |
| ts/state/smart/UsernameOnboardingModal.preload.tsx | 1841 | `371b5202de23f774975372fcbcfb7fa2a3bfac806a64eb5631b55edf270ba110` | 0 |
| ts/state/smart/VoiceNotesPlaybackProvider.preload.tsx | 7015 | `ffc04fe9f10fea2e37894a989be3307de6234ba54b2f8df67d61649b56bff0d7` | 0 |
| ts/state/smart/WhileMutedSettings.preload.tsx | 1904 | `1d4036c2b3f02cde8d5da8d0fe7c982440503592928e2067663a9449d0408c6d` | 0 |
| ts/state/smart/fun/giphy.preload.ts | 6190 | `ae94107c7c743d236be8f7223b908c93fd819ad12ff02331a738598335a256e9` | 1 |
| ts/state/smart/renderAudioAttachment.preload.tsx | 849 | `0ded997b828106b5e67266c359bf57cd68af2dfbac1557a92a1cab08af4a9f68` | 0 |
| ts/state/smart/renderReactionPicker.dom.tsx | 343 | `df70fd8a39624bbc5c3c0e95fdeb7551ce244f09a7ceaf718906ba343fc5d324` | 0 |
| ts/state/types.std.ts | 4827 | `88faa6799c4de08aae77ac2426a21b7c5ba296d52ca4cba9fbac2503a5e13021` | 0 |
| ts/state/util.std.ts | 566 | `6803681c19e6c9fe0cf6ef8b7184ca4c40caa59d2d6bcc0d1d48770dee3cd213` | 0 |
| ts/storybook/Fixtures.std.ts | 489 | `ce8905ad6a2014adedfd072e582d7d25f4176c96da159104a8809ea6dbbb9c87` | 0 |
| ts/storybook/types.std.ts | 1460 | `4d183f09827acf6f07be0b5d482caa86f8ef3f3f7cf7738a28bc7ec38663e02e` | 0 |
| ts/textsecure/AccountManager.preload.ts | 51159 | `25d2f5a562cd45592dcf623a7804ea7460a5c33e8789a79adf29bbbe7a3889ea` | 0 |
| ts/textsecure/ContactsParser.preload.ts | 4478 | `cce49df697e1e10d3a452fcc5efab855d0428c8b285c98ff8306432861903694` | 0 |
| ts/textsecure/Errors.std.ts | 8476 | `2f99320e2a9c2825104c0897e01336a9af45b19918f9e73ca2b76ef09e94f773` | 0 |
| ts/textsecure/EventTarget.std.ts | 2272 | `143baf6487ae8a4f0ed447311cd78bf68f98e6006de8867f9fcc6f17f9087413` | 0 |
| ts/textsecure/KeyChangeListener.dom.ts | 619 | `a80124e936294f8a9e4e042c3bfab01753c1d0e66ec8d780c5fda7de41dd2b3e` | 0 |
| ts/textsecure/MessageReceiver.preload.ts | 136397 | `9d554ed9eb83614b12c0d7bfa05fdb89b2b704c699e2c5eb9bd04295e0c44414` | 0 |
| ts/textsecure/OutgoingMessage.preload.ts | 23724 | `13e5c627c15a35409b119788ce8a6ca6c85f916b593be4ff7ccb6baddc695ad8` | 0 |
| ts/textsecure/Provisioner.preload.ts | 13102 | `5bad8c5fec60e2cb23438cb50a459a5a3736be23facc1e814cb6f766419a350d` | 0 |
| ts/textsecure/ProvisioningCipher.node.ts | 5764 | `e5e1afd2325788b9364f1f79d79e6cbf9e8034cc15d3d0b49f158692dbf73c7f` | 0 |
| ts/textsecure/SendMessage.preload.ts | 82375 | `1965936f8593f6225a5925f7b11ed4c4684c50fc1eaf2d5f2aa56cf1b40b3de0` | 0 |
| ts/textsecure/SocketManager.preload.ts | 29532 | `9c7b693f8cc0754fc42ef7564f4fccc07743d06ac500ccb8bf44e225df6af07e` | 0 |
| ts/textsecure/Storage.preload.ts | 3337 | `c08da455432919baadb79f4d383cefcc2e8e6f98849299aa80316508bb791860` | 0 |
| ts/textsecure/TaskWithTimeout.std.ts | 2605 | `48235bf9ae3c0e8926f38fba2a667c59ce2165d16fb8ed12ab6789dd36607588` | 0 |
| ts/textsecure/Types.d.ts | 8971 | `3d3dcb043402bdb1341fdf9b49aec2801ca401fd35fe130bc2a2228cf534240d` | 0 |
| ts/textsecure/UpdateKeysListener.preload.ts | 3756 | `ae1322c68b004bb8d70a76a3dce66b17ba77a289e75c45b89d98c68c0f5df38c` | 0 |
| ts/textsecure/Utils.dom.ts | 1389 | `98b7a7f5cd53f6d4b99c07118319756c66db0326a17520a7803e92955c7469d9` | 0 |
| ts/textsecure/WebAPI.preload.ts | 143756 | `43bd2bc272bbb7c18b1dc8e01e9698af4f1dd37e6b08fbf30bc7dac4eaf70f9d` | 5 |
| ts/textsecure/WebsocketResources.preload.ts | 18703 | `9138f7d8844502a34f4cf816fd024d7680ac3aa99f78cad5afbc84a2022d2e5f` | 0 |
| ts/textsecure/cds/CDSBase.node.ts | 1846 | `b5096922dd0fe29c75302b792f57bd55f21583775675f216cef8cfd460e8097a` | 0 |
| ts/textsecure/cds/CDSI.node.ts | 2248 | `8a259c275353874442eff5834e5b83f8fe1f380c8732741c72c5ab131fbda886` | 0 |
| ts/textsecure/cds/Types.d.ts | 633 | `a513d26fc5236802dbb0e099f90b4206d3d886be5d801b5dd81a7705d489fa84` | 0 |
| ts/textsecure/downloadAttachment.preload.ts | 13697 | `7c9bd05aabb69d89f119e35642111ecfc68704065e596514f06265d1268f9e21` | 0 |
| ts/textsecure/getKeysForServiceId.preload.ts | 6035 | `4db4c826e30ccf85882f5ca5a14f31e7469231adda82c11895863d70150aefcf` | 0 |
| ts/textsecure/messageReceiverEvents.std.ts | 20078 | `52ea1d72d45b384d769d7ec99264623d805987da80a8c42133c90de7c5b96534` | 0 |
| ts/textsecure/preconnect.preload.ts | 3086 | `b5efbf64475ff2c0fde4ff011f60775dde7eb1058d0bc78712b67c87ebd2d419` | 0 |
| ts/textsecure/processDataMessage.preload.ts | 22479 | `ef3750360fe4ca71d182540a01456f169a8aa0b4904e3b2ae1adc9c8840a71b6` | 0 |
| ts/textsecure/processSyncMessage.node.ts | 2567 | `d021594dec6c6e92fde162af2ba54d5515227ac63b5c8314331c4a821fb12e81` | 0 |
| ts/textsecure/storage/Blocked.std.ts | 7276 | `1f0349209151426da3bcc6913f043e80d78b0603c27ceea238a8ad3460d97820` | 0 |
| ts/textsecure/storage/User.dom.ts | 6472 | `94d4a1c9101c304da2c1513746de94ad5e011d35d8680d704db882d1b19ad155` | 0 |
| ts/textsecure/syncRequests.preload.ts | 1100 | `65698c18d0a849d96cce58e10b129e858da06869deefe25572df8e2d6b410d84` | 0 |
| ts/types/Address.std.ts | 669 | `0d2e900f84ab0f5d30da477595f70520faa9a0ac944673910578de64bc02675c` | 0 |
| ts/types/Attachment.std.ts | 7659 | `4ce49c3c8cd55a0121f8f18053cb983ef3498ec41f6c444a5b1440ebeb7eb989` | 0 |
| ts/types/AttachmentBackup.std.ts | 2940 | `6ff05ed50a49651ebb4bf4d65924df30dda5572322cdfb1c1cb011d7b9f4ef33` | 0 |
| ts/types/AttachmentDownload.std.ts | 2129 | `94193bb83169e23e8644a6eda340f956cf1dab61c27ed83670c0103f1c676145` | 0 |
| ts/types/AttachmentSize.std.ts | 3127 | `10ebf39216580ae6c287718d9f2e6c2c093b10cfd80d64d791b47c83415e6951` | 0 |
| ts/types/Audio.dom.tsx | 318 | `a624addd679eec24218eec0292d49c19310db20113a5d8fb83d877d745605792` | 0 |
| ts/types/AudioRecorder.std.ts | 862 | `6beef314783a9679dc48f0b91e1b23cd6d1c8aa4fe47e78d10ab7e6164e408a9` | 0 |
| ts/types/Avatar.std.ts | 3216 | `1368fff80cfc35ab7b56e6ee91222feb1e996d3eb0fcd49b7c83f2b6070be04e` | 0 |
| ts/types/BodyRange.std.ts | 22417 | `2aeba01be62f914eff8fa29d8cbec68dac97529594eab5dd222a36b8b9adb50a` | 0 |
| ts/types/CallDisposition.std.ts | 9762 | `e6cfae8d7e8a621a418925ef61027dfc988ccba0b156a7e1c5a89d71c90c322c` | 0 |
| ts/types/CallLink.std.ts | 4502 | `5718264c9ff29010bf5a5bd596127c005db575ba61074c1392d5794e5ca3980d` | 0 |
| ts/types/CallQualitySurvey.std.ts | 939 | `deb2b3c9737589f68fd2a88e686ac028bdbf088587ac6bba6820f3c8a9c6fa49` | 0 |
| ts/types/Calling.std.ts | 7210 | `af7ba0b936933e96c3415720abf694a0549809aa8e90ba9512569dc16df7856a` | 0 |
| ts/types/Capabilities.d.ts | 437 | `250a4fe8f79dc87d47725e69b1920b128b54e4b85302c250f041b9579e0741ae` | 0 |
| ts/types/ChatFolder.std.ts | 6090 | `06bba81573fe40a709e0b244b26e4abbe304ed8ca5585d2b9a99622e39dd363a` | 0 |
| ts/types/Colors.std.ts | 2179 | `a31224395165ce7dc5f5d3c50183afa3588c276d8c5e1ac4e75fd90c70d02c93` | 0 |
| ts/types/Crypto.std.ts | 1422 | `b394d28f69b5a4f13a2710881db41a22e39da13b5579501bd10911f19239622b` | 0 |
| ts/types/CurrentChatFolders.std.ts | 4131 | `9e1b6fa134ff15e2498eff45f2a6ef3f95694e2a03bba92e970a960e3c18f8a8` | 0 |
| ts/types/DNSFallback.std.ts | 386 | `86efb3200dc7d8b71b8dfdaad932438c19d131029e159ba2c1e5dda6a2ec504e` | 0 |
| ts/types/Dialogs.std.ts | 507 | `3f540755dfad104d103d031a419c12edc51718a20fd3d0263182828a149adad4` | 0 |
| ts/types/Donations.std.ts | 9380 | `b14816aef9f0c98ab1a15b5c0073b13e3050bf0fc9ea958d9377295badef29b9` | 0 |
| ts/types/DonationsCardForm.std.ts | 12006 | `b4b75a43b5c9e1c9549d796875fb1c5772a82e4afc7b3f62f838fb8adaf8c626` | 0 |
| ts/types/EmbeddedContact.std.ts | 8602 | `ac1ffb161947fcc08f3d0983c8eac13604e518574d47988d324a73cbf9bca88e` | 0 |
| ts/types/ErrorWithToast.std.ts | 323 | `75e49924e1a4c0e386f3093bc2163e6a47e04bc3e4ea97fff2e66a31a306f954` | 0 |
| ts/types/ForwardDraft.std.ts | 2285 | `28eb7b7fd387e9c90a1897c49f051efbeaac9e86398b2d5a319f3d0810bdbd36` | 0 |
| ts/types/GiftBadgeStates.std.ts | 207 | `08ed48d571ab617a0d90de6ec0a87c76a120b1e01bd7e88a847ffbac53fee7c9` | 0 |
| ts/types/GroupMemberLabels.std.ts | 1022 | `151bab37c193160e29dff895f5d84bf47fbc88a69eb985a387077a165f134be8` | 0 |
| ts/types/GroupSendEndorsements.std.ts | 3048 | `06b6c438007601f3250b79ae29ab73834c65fcb65a02a389700d75040fbe2095` | 0 |
| ts/types/HTTPError.std.ts | 1137 | `87c741e4e09ee94c5ffe9f7b2be1a8c63e49cb0e4cf13d15172a7f749d0d7c14` | 0 |
| ts/types/I18N.std.ts | 1144 | `c85654a59c549ce035a4a9a357457edd550effffd777597beed0e076c207c494` | 0 |
| ts/types/InstallScreen.std.ts | 1168 | `585f4f005ebce97239918380d946a19d86db70973daad9b23b0e649325ea2125` | 0 |
| ts/types/KeyTransparency.d.ts | 187 | `37585cfa3cccc85c813a5865d1818ec28ebf88750314a0a670912d02f2332599` | 0 |
| ts/types/LinkPreview.std.ts | 7698 | `2708e9f2e0d92eba123eab7a524ca47291cce1d1d42808b1e90bfcbe1a737388` | 0 |
| ts/types/LocalExport.std.ts | 5299 | `959f85dcafae7235c9a8cf70997affefa87bf2072dcd7c7a5d5eb7c49840208a` | 0 |
| ts/types/Logging.std.ts | 557 | `141bd8e62a0900d1b35439ce1a56e0c2dd121f1fea52ae458960bc0973cb6589` | 0 |
| ts/types/MIME.std.ts | 2382 | `801a7bfa62ae69d60bc3e0361016ef74ac3fcea83a6d74643eddb2a2cd5e2f16` | 0 |
| ts/types/MediaItem.std.ts | 1740 | `90b93f26b51428240f297532f96c8d79de9f4dbd01d04af2fbb7814452bbef11` | 0 |
| ts/types/Megaphone.std.ts | 4681 | `7b1750c0d1d6c1c0a8e198d0f1131fcd65e7cbf86a03951ec9133d6d3b8cbbad` | 0 |
| ts/types/Message.std.ts | 3768 | `4464022d61e85906b253e1a9dcf3b243dd0d6c623a9c59e1d3f325e8edc3a724` | 0 |
| ts/types/Message2.preload.ts | 30156 | `36940930618423ade7c7f4668b73425f0b6ead951bd7072ab3c8e1cb91de8cf7` | 0 |
| ts/types/MessageRequestResponseEvent.std.ts | 878 | `0670d5833e02ac016afab11045c4fa3eacf3997c5a152e83f1b9edd6f224cd56` | 0 |
| ts/types/NativeThemeNotifier.d.ts | 161 | `f8c7d7b7d17f0f6c13b1f625b088dfbc5ead46f8e8240fbf4873f03f2532d240` | 0 |
| ts/types/Nav.std.ts | 2821 | `e42590bfa33a07e65af5cd49becb9d92115209a082996583db4075506e2ae265` | 0 |
| ts/types/NotificationProfile-node.node.ts | 1479 | `ae6ffe1b9c5352f1a88b6cce4efdddb89b60cb221d5d0bbb6af8819afe1eecad` | 0 |
| ts/types/NotificationProfile.std.ts | 15936 | `a8e767a6496be4a57c1a6e0beaf9b5d7d704f14125aa93178cd021ef7be62278` | 0 |
| ts/types/OptionalResource.std.ts | 481 | `5546b1c74db4d961636a18b5632887db40d530a093128edcbc6825308c69d45b` | 0 |
| ts/types/Panels.std.ts | 1111 | `c496667a2b4d11ad97b3afe1f04e128b4027fab854aad3fa4b88cded72bb5061` | 0 |
| ts/types/Payment.std.ts | 945 | `7d22a3e7308ac65d5d0f2214dd41043fba61e7bdb3ca3635ce518722c93e04ed` | 0 |
| ts/types/PhoneNumber.std.ts | 2401 | `d4da90f1ce0b0847557a9fa11132f319ffd058b0c1c0d49c8fc01efdcb509bdd` | 0 |
| ts/types/PhoneNumberSharingMode.std.ts | 449 | `d236a44d390097e09eb373fe1b35abff65335cabc1fa70305ef5535525d8d01e` | 0 |
| ts/types/PinnedMessage.std.ts | 1032 | `049c141a4823a3a1182d3a001fcde2c7b8aee3df666ac7bca440415bfc2a9c6e` | 0 |
| ts/types/Polls.dom.ts | 4143 | `af9f3107eab137e7964e4c83196bfd3eb73d28baf6f02ae98d79f9cd9e046523` | 0 |
| ts/types/PreferencesBackupPage.std.ts | 845 | `d68aa123cea3e72e83c475f45486ae92d0563ecacc1bfef4628826e52036bdfd` | 0 |
| ts/types/QualifiedAddress.std.ts | 1941 | `91be5cfd7ce586ed6bd2298540b28f2df4e77d65ef1052299f7bca180017f339` | 0 |
| ts/types/Reactions.std.ts | 499 | `42287b2b5eb0fa5d3f30ab79b05fd5b1e43c6a14422ee3b0872bf27f8654558b` | 0 |
| ts/types/Receipt.std.ts | 668 | `d5fc6d7a579d72093a80ee9d639ad46562342ec1e9023dff78636823a8745c04` | 0 |
| ts/types/RendererConfig.std.ts | 3088 | `ad39feb6a671c677ae54a5c5d6e3d289379e3700a76cf724338856bcc1cb024c` | 0 |
| ts/types/RenderingContext.d.ts | 325 | `ca8fe9c3db10bc6b64db378d5098f81387bb8768eb01d1d0c1e6a82df5bdc41a` | 0 |
| ts/types/SafeStorageBackendChangeError.std.ts | 647 | `ead380d47a09ca79395bc5291bd8ff4bba8897d0953247a77845ececaab53d5c` | 0 |
| ts/types/SafeStorageDecryptionError.std.ts | 189 | `0c7634505ce476b517d45c0be372d1d7cc8b2545902456660186896aa1b24fe6` | 0 |
| ts/types/SafetyNumberChangeSource.std.ts | 232 | `765fb780336c9ff3ac042fdde78ff4d21f677cd93a5dce9055124c6e21d00b3d` | 0 |
| ts/types/SchemaVersion.std.ts | 248 | `3647794532892b0532e65458c84c43e3d942649faef920a17fa300b0441ec805` | 0 |
| ts/types/SealedSender.std.ts | 225 | `44b114552f57e20ed9fad09b7e9d7f2cef45cc04fd06005a743f2c6edb77d061` | 1 |
| ts/types/ServerAlert.std.ts | 478 | `753f31ef33ec9d1c821c5b6f44c8d6ce2be5a8abe68a31f704e5f8e05c013b3a` | 0 |
| ts/types/ServiceId.std.ts | 4420 | `0136b319667cfcc405767065b698b4ed14950f78bbdca83d5652947b9ce3942b` | 0 |
| ts/types/Settings.std.ts | 2678 | `9193c6b3ab48ac7217c92d26cff8d045aae7514465383e592b379eaa488e3bd4` | 0 |
| ts/types/SignalConversation.std.ts | 407 | `a02a47ea7292a9368ca887cfa9bedd624a761d8977572ab20c3b242250b6b39a` | 0 |
| ts/types/SocketStatus.std.ts | 450 | `151ab04c19358d2e8ca4bd7bd3931b33b239d8c1c16e79ec1eebf7621aa426b2` | 0 |
| ts/types/StandaloneRegistration.std.ts | 14476 | `90a298460447efaed4152409d82e0d3116f838416f03e55da6a9c9340d58f8a2` | 0 |
| ts/types/Stickers.preload.ts | 35558 | `71c4f19ef9e0473a8287193bdde3b754d2288ac9380386e838cfa9d452493362` | 0 |
| ts/types/Storage.d.ts | 694 | `742e970eb79487ac3e71db7b68b06103dac2d2d9cc6301353c849d907db4dcd3` | 0 |
| ts/types/StorageKeys.std.ts | 21850 | `aeb2f8c57b41737782beb46dcb7e0402f9ab693f44e4c0f99027cf687d2de8bf` | 0 |
| ts/types/StorageService.d.ts | 355 | `d5cfe9964903019142c360ff9a58c343a1998bcdc01712aca4212d418ac9d1e2` | 0 |
| ts/types/Stories.std.ts | 4502 | `4d9046c6c299d1029a80d35328dbed548ab54549c71b49a4994439017276db3b` | 0 |
| ts/types/StoryDistributionId.std.ts | 1216 | `d66f9e877ccb2d1b64e24709f1772a657b73a1b9ee9dc037b37bab997e176ba6` | 0 |
| ts/types/SystemTraySetting.std.ts | 756 | `1f317bcfe3270094697501912b3c30bb6396279cf4c30453c6797568725422e7` | 0 |
| ts/types/Toast.dom.tsx | 11227 | `a2e77fbfc7fbce339ee8af449a9fd576e07f722ead202c07616cd5eac856c5e1` | 0 |
| ts/types/Username.std.ts | 1440 | `2819bbed90a0d7746495ed0627be34d688afe2cd35b65133e059dd38020b330e` | 0 |
| ts/types/Util.std.ts | 4484 | `f9434c86464bfb2e9563dc49b8557f365327e6ec7445915e3f246f274b404102` | 0 |
| ts/types/VerificationTransport.std.ts | 155 | `99157a983d37a7516610bd5b152b3a248257f82dc5bb102862352b2ac5f52cdc` | 0 |
| ts/types/VisualAttachment.dom.ts | 7456 | `3152f095c735e66ebaee9925c53dc923569e3f651f5c3e8bde337e14ff5c336d` | 0 |
| ts/types/WebAPI.d.ts | 164 | `db79cfc03cb5b13bad74fad1760447d2dfe1435ce069bca4c82722345c3c0670` | 0 |
| ts/types/app.std.ts | 205 | `c997187dedd720b1840809bd46af935b0acd964767749ee8b2e115180f22ecd8` | 0 |
| ts/types/backups.node.ts | 1727 | `be11e3154f3596c3a192b192b757545c6203ab3b0c0116a95251dab1f1751458` | 0 |
| ts/types/emoji.std.ts | 445 | `ae0006016d1321325984cfc472642114a233b107d90ddb638b21268280fa1733` | 0 |
| ts/types/errors.std.ts | 1032 | `9ada0ff9ef5b529bf11420dcbb0fed70a50d0cb7ce2649e9362b180a2dfc273b` | 0 |
| ts/types/globalModals.std.ts | 469 | `83faabf6a43f2ef865e122269778a96e6a061ba907d1e11ae2aec2b983bbe978` | 0 |
| ts/types/groups.std.ts | 4511 | `284bc8dd6e76ad636d6a67ac8a7ce55a4c095ed33f95e6be927efb78e2df33cd` | 0 |
| ts/types/leftPane.std.ts | 234 | `8521d7d7e3391267a80f25e1bd01b0d2a5e6f04a2a2da747f63ab5dc8fd39439` | 0 |
| ts/types/menu.std.ts | 1068 | `d5a1afa66227c2dc163d0d8776dc74a5e831bdd9be2922fb6085c13a56b67d01` | 0 |
| ts/types/message/LinkPreviews.std.ts | 1229 | `f29620419268da80f6fd57d7df96bc2a0dd951925dfb35f8e9c1d2d7fb73a92e` | 0 |
| ts/types/message/MessageStatus.std.ts | 295 | `510c5c98ba3accee1bc4c0144cb67b3ba244e0ff4b7a33b55fc4e6bafed1ff6d` | 0 |
| ts/types/notifications.std.ts | 310 | `bb95b05df89eb69ff3d52ae4feab4e23d4a89e1a85806a1df5bb71e1e59a4944` | 0 |
| ts/types/packageJson.d.ts | 482 | `1da4239aea552c54a77f98a9a7c705124f34eddd9027c248dd3b76a578c0751a` | 0 |
| ts/types/releaseNotes.std.ts | 251 | `0e97d58cbbff279adba56f1bc463fe11f03b40f48a746a8c22ea4022989e5aca` | 0 |
| ts/types/safetyNumber.std.ts | 203 | `b3b23b00d24f7054c003f52d60f1632feae7aa73ec58042086982682a6db2dd6` | 0 |
| ts/types/support.std.ts | 812 | `6ae296c63e7c5ec2134d907f55dfaea278f47c022b266257fd89a297bdf5b7a1` | 0 |
| ts/types/transcoding.std.ts | 147 | `b060a26a3ac9e1aa8bc5da2b20dcc95fc4a5bb41b961b864ed569c38debb27c6` | 0 |
| ts/updateConversationsWithUuidLookup.dom.ts | 2796 | `6fcbd3dde482b6a2acdf0096306ba1dae08cf73d7c38c50993a5354ffc6d4885` | 0 |
| ts/updater/common.main.ts | 34468 | `69442bb89a317b5ddc1ec5c87b10e2c065750edb501a09b3432f6aef881c9836` | 0 |
| ts/updater/curve.node.ts | 680 | `56513ba6e83839851e6bd9b68e3e6b6d3ed8819e2efe379343928dc359eca313` | 0 |
| ts/updater/differential.main.ts | 13391 | `0899250ba956d42b3adfbca6896c21e70f62f27c438e35258c16db01ce184b44` | 0 |
| ts/updater/got.main.ts | 1989 | `85a8c8107926ee1f2066115ef2e4778b91dc767bf17ff935e3d0b728f0aea2c3` | 0 |
| ts/updater/index.main.ts | 1809 | `947e0e24712ad3e2af26cc22540c02d05ad379d14147e766a84b101178b0d894` | 0 |
| ts/updater/linux.main.ts | 3002 | `fe3eb34e97d456f186db125e7a2588b68338fe106640a4a6333aa3bd3edbe239` | 0 |
| ts/updater/linuxAppImage.main.ts | 3946 | `5969934ba26e957f941e8394d65afb945e0171bd05c557e59e82583b36c0148f` | 0 |
| ts/updater/macos.main.ts | 4102 | `9f0b8afb011069a8c2abddc4a01b526b036c51b4293f121467728b312ce217b2` | 0 |
| ts/updater/signature.node.ts | 2894 | `13949ba4a5942ea588da767c07b705ceac6231202914927e48aee2ba87b4cc17` | 0 |
| ts/updater/util.node.ts | 2194 | `2ed7534ea7d5917cf0ecc2082c2a5678dd11898cf74691af9f31cdb537f83834` | 0 |
| ts/updater/windows.main.ts | 3628 | `55eccc2b483981eea9e7b5b7b2114d07644abee37130b785d74a3edd4c823a2e` | 0 |
| ts/util/AbortableProcess.std.ts | 999 | `862936ad254fd15b0cd004d5796fc773be27eb6ad580c1a9eef96d9e0555d6f8` | 0 |
| ts/util/AsyncQueue.std.ts | 1190 | `6223c174243500fce5b2c534d8c6751826abf39d1f963e1e0e9fd0dade7debd8` | 0 |
| ts/util/Attachment.std.ts | 23505 | `d2096633d8af02f843354dd238ab1c1b235b77f5320c36924fe833a382b96fbb` | 0 |
| ts/util/AttachmentCrypto.std.ts | 1292 | `a9e2568895a42ec5e4c89f86b2dde64d7ca1292b5f05a893167d2fbe1ed71d75` | 0 |
| ts/util/BackOff.std.ts | 1907 | `01aad750065e51472aae3e5546014b54d8131eb216b6a5238c4878ab662f5bb8` | 0 |
| ts/util/BodyRange.node.ts | 3458 | `9d2b74444f29943882838ef99d2d71429d2a98f9365ef3aeb4e364150916bdf8` | 0 |
| ts/util/CheckScheduler.preload.ts | 4111 | `35d89b2bf4babc8d95715720c035fe7e5526b1c147cfc84b5fc349adc1cd2666` | 0 |
| ts/util/CollapseSet.std.ts | 17086 | `2abcb25ad266a2c4b9c91d32d6aa5445087429770e4c39b4e8cb5ccab4fc48f3` | 0 |
| ts/util/Conversation.preload.ts | 1603 | `1e5e2db5345468de1f03ce15933189ae3027e3ba53c14bdfbbab48565773a624` | 0 |
| ts/util/DelimitedStream.node.ts | 4155 | `71842eaaddd0c8590e3223525e6a2aeb8e33679cce58a3148f285b40d2bc5aa7` | 0 |
| ts/util/GoogleChrome.std.ts | 1564 | `4adeb0ce12ce802637167f6ea1e369663ec19066a99a2d035620cd1540e2582a` | 0 |
| ts/util/JobQueue.std.ts | 479 | `d679877c5f59792464232c01974175a46d3120cc18b04aca0ce9ebb27f895fef` | 0 |
| ts/util/LatestQueue.std.ts | 2330 | `1155626acfcbd61d04feb18cfdd8320913673a6ce0eca6bb3bc97503d2d6b2af` | 0 |
| ts/util/MemoryStream.node.ts | 665 | `3e3958b7cdeaaa819a935bebd90635ac453886e3cfbff65c13b89ec5610af5e5` | 0 |
| ts/util/ServiceId.node.ts | 3232 | `e516e59b979689deb128493e7c8dcff97a8fed9f7c62382ddc7a9c30ba3897a7` | 0 |
| ts/util/Settings.preload.ts | 776 | `d69b8e33aef784fda1317c1865a4dcef14b5447b012918d76d11923262ffbfb0` | 0 |
| ts/util/Sound.std.ts | 3767 | `fc7d75044615efbab4f583dfc80eb71dab7cd656bf050502134421b2ee34ebf1` | 0 |
| ts/util/StartupQueue.std.ts | 2054 | `742bf15c1de25c91a3aaad6de99963f952b447e9b159cc10ef3768c41a0d5993` | 0 |
| ts/util/Stickers.std.ts | 531 | `5dc81f4a7aea53e312da155417d9b367f20cd578af5179047ca3127088096839` | 0 |
| ts/util/TaskDeduplicator.std.ts | 2022 | `873338781451e4802c71f1cfa4eb85c8e93a08f6f9fd4146a1f2b204fc543754` | 0 |
| ts/util/Username.dom.ts | 2132 | `73ec666167c8eb80120ef3d060d70602e7e21ffa817ea97c129df95ae267d416` | 0 |
| ts/util/Zone.std.ts | 1093 | `e9d07704c0a279c72f12c2ce58e031dd976ec9a894c0a376c7dcd89903cdcf88` | 0 |
| ts/util/appRootDir.main.ts | 513 | `c63cd354e911741048e96f347abd648d8b99e8a7f8d3e28e8679763a1f0354ee` | 0 |
| ts/util/appendMacStream.node.ts | 1057 | `4d06ecb93ab86d2a7100a3c6e102b949fcade9a9f8089b35a57d693755de4203` | 0 |
| ts/util/areObjectEntriesEqual.std.ts | 255 | `d8f76f78ea30d9c92ecccac85e97cecf1ea68454969f4328b0fcf45b6e423229` | 0 |
| ts/util/arePinnedConversationsEqual.node.ts | 1961 | `ddda5e231fbe7f591fa6c838f60bec45900e2bce55e8e5544f3bde66f872d37d` | 0 |
| ts/util/areWeAdmin.preload.ts | 815 | `f7154901e69123e33e1f3aeb67b7b96390cc980969d334979896a335d8c7969e` | 0 |
| ts/util/areWeInGroupWith.preload.ts | 761 | `59b51529168b10d8b4ba6000512d7c947eb4a1b9ed5a410309f59987b2feb24e` | 0 |
| ts/util/assembleAccountAttributes.preload.ts | 2695 | `fc2f9524ed0fc3db5c4473dac142b467652927ae5678782c6a622e620fa8b17a` | 0 |
| ts/util/assert.std.ts | 1988 | `b4b95deaf59fbf07d413ed2192884e3f32d3f5ac7215ac1866dcc397214a5cf3` | 0 |
| ts/util/assignWithNoUnnecessaryAllocation.std.ts | 927 | `b9b9dec9933cae963f16216bf887aca909da76ed83f1b509e80c40ba2af94410` | 0 |
| ts/util/asyncIterables.std.ts | 1278 | `4b23f64f053aba36a7c4cc84decd543db700a3603d32465699cb47aa85cde2ab` | 0 |
| ts/util/attachmentDownloadQueue.preload.ts | 4064 | `0cbe2010457a550421d4329d1c60dca59c5b46797bdaba9a860cc990f472c846` | 0 |
| ts/util/attachmentPath.node.ts | 581 | `b335fbb3f261b9c6c208bb466c686cb8a51f17c4bcb9c49d65cb501a8916d046` | 0 |
| ts/util/attachments/deduplicateAttachment.preload.ts | 3315 | `cba9ec13dcd58bfb63e3f5c9b3aefacac673e65f3c37b10efb06293d84e4252b` | 0 |
| ts/util/attachments/markAttachmentAsErrored.std.ts | 949 | `082ff3f2b18d85a172edb018ebec5f78360bd0dc5d12bb865f6ae561c7370abc` | 0 |
| ts/util/attachments/migrateDataToFilesystem.std.ts | 1853 | `fd84907f718927fe123cae271fac7a82e2d94d4c07640aff4871f36a03c1640e` | 0 |
| ts/util/attachments.preload.ts | 3558 | `41b870c253240919ceda4dbe4635a0cbb375625ae9bdc278f7ced07da4f8d99b` | 0 |
| ts/util/avatarDataToBytes.dom.ts | 3821 | `dcae205384b7d9337e97334cb740ed2a0cee64fce7cbdcb3715d250e3166261e` | 0 |
| ts/util/avatarTextSizeCalculator.std.ts | 1127 | `56bf49443c130f642e1031c5da849a83cef733fb4b97275c04f91c422513530b` | 0 |
| ts/util/avatarUtils.preload.ts | 2471 | `6fdb096f099221b3f12647d746ad0d838fdb3a04a47a1591b133719696fe5131` | 0 |
| ts/util/backupMediaDownload.preload.ts | 1923 | `64669dec008293dfd850a52f46af8419480cc3dc4f3fd1078985292a89d8bb70` | 0 |
| ts/util/backupSubscriptionData.preload.ts | 3631 | `98ddb897ae8df7b931ae177de7bc0c4213bf0c5562ec4751c9a559ffeb1e3e7a` | 0 |
| ts/util/basePaths.preload.ts | 817 | `014bec526dcda424792a425ca128528c8853505f26eed3180e5fd6495640acbe` | 0 |
| ts/util/batcher.std.ts | 3520 | `609c8c6f99d25ffa267aff0d7f7a98150e6926886e9ddf1f7ce209babeec99f4` | 0 |
| ts/util/blockSendUntilConversationsAreVerified.dom.ts | 4718 | `56e6bb6ed39b348232af6b417f2624d2ebb70a0c68e8fa05ecbcd13e88bb38a0` | 0 |
| ts/util/buildExpiration.std.ts | 2422 | `b515fa79ee409a8755773442cde9cf9e2674573b6235d3e22a92d9691da9f560` | 0 |
| ts/util/callDisposition.preload.ts | 51059 | `f75ae1b5b0b0a5aa005c9a98aafd5ed5bbc5e983fabfd8946f90962b754c81b2` | 0 |
| ts/util/callLinkRootKeyToUrl.std.ts | 249 | `4573c86d34af17a6d7b3fce05a11aebd25dae6efc1fd8d8570bfe5c6fd990a56` | 0 |
| ts/util/callLinks/zkgroup.preload.ts | 1769 | `97a59fec544161121896ab4559c86fd64b434013f80d88c0f276e682d758be76` | 0 |
| ts/util/callLinks.std.ts | 2953 | `178190ba107c537893130245cf06bd329420ab274b461148c62077d381268ca4` | 0 |
| ts/util/callLinksRingrtc.node.ts | 5563 | `a42e660891cc0a61f8738c56f49c8c4c98e69eada7d11920af1bdd291435d683` | 0 |
| ts/util/callQualitySurvey.dom.ts | 2550 | `990171a63106b15e89a07f5a32057526ca37bcb668f7153113aa48f6bae19de9` | 0 |
| ts/util/callingGetParticipantName.std.ts | 572 | `a6e4188b35f1f794f1d9e4e5f4a90d0f7f6efdac9a82bac32a14b7ee858ebeef` | 0 |
| ts/util/callingIsReconnecting.std.ts | 673 | `7bdf302dc17223da7c299c83ba463dec0ada684c09a3475ee4d9974778fb400e` | 0 |
| ts/util/callingMessageToProto.node.ts | 3141 | `243d52c87b1138bffc743ea5a5614faa77af8fbe471fa1612826f8a09e46cde4` | 0 |
| ts/util/callingNotification.std.ts | 6690 | `755c1b8c28ef8235da9c40df4f11e042eaec9cbbf98f0495e53ef314e479cba1` | 0 |
| ts/util/callingPermissions.dom.ts | 414 | `9d7fdb448ca2bc63d36de4fce61ef05194903954a4bb721b6594e0d68dbe62d0` | 0 |
| ts/util/callingTones.preload.ts | 1958 | `efdaaac424e9d0615e69fd41735f8034e1b30570dafe17e334f60ba2358fbdee` | 0 |
| ts/util/canAddNewMembers.preload.ts | 762 | `69062a0ad2be757b5670d7dac744951e208018a15e8fd7d27e1c19a951508eda` | 0 |
| ts/util/canBeAnnouncementGroup.dom.ts | 469 | `5ba39e56d3a81d156b1466402584adaa153f6f4ef3dc540421c7115fc7c94470` | 0 |
| ts/util/canChangeTimer.preload.ts | 1053 | `7ac819708032a167c75264b8349478360db2d3aa7e4c1e5b3d904cf4de185b46` | 0 |
| ts/util/canConversationBeUnarchived.preload.ts | 590 | `2bb3ea85b7747b9d56ea307170f420c8c5c6457ab667fd28c36a1e5df2306983` | 0 |
| ts/util/canDeleteForEveryone.preload.ts | 7285 | `4f6d363f96b16b22804d92fe2d63581b22ee6337d3c1e5589d050731a96500ec` | 0 |
| ts/util/canEditGroupInfo.preload.ts | 787 | `938151f9cd260d9a2f49d8c0beceaed960eb841096c1e206d26759c22ce8cdfc` | 0 |
| ts/util/canEditMessage.dom.ts | 961 | `0c52fc3c9099f7cd20b0d70a4c5e64b92e1fb21a8163e32948f969efe92b6614` | 0 |
| ts/util/canvasToBlob.std.ts | 705 | `0941f7c473b98fcf123aac9a1dc48524675921ff774678bdfca367e8d75eeb2b` | 0 |
| ts/util/canvasToBytes.std.ts | 453 | `b0cf1a8d1d044de7835cc3f5dd6979d236e3f28b2efb319e44e4b84778aa6ac1` | 0 |
| ts/util/captureAudioDuration.dom.ts | 1256 | `cea4f8f99ae7afe01302547232827ba17d9f91f0fb49deaab6c1de51dd9d3fd6` | 0 |
| ts/util/captureDimensionsAndScreenshot.dom.ts | 5489 | `924fbc128fe33e29bd8f3919339da8aed4fc0e7cd3500643c065ec85b8194ba7` | 0 |
| ts/util/checkFirstEnvelope.dom.ts | 2630 | `0506ace18f7b975e739c010019e62a9ab9b4f5ff87f992c35949eb718e0ba2c2` | 0 |
| ts/util/checkOurPniIdentityKey.preload.ts | 1556 | `ae1acbf88d45a571ad4b864ba55152fe49ccf3ece6b91c9852f94a82c5ec76c3` | 0 |
| ts/util/cleanup.preload.ts | 12966 | `8db946421c5aa86d5541050a790fd5b958ba169bd9ed0517c1009099ba6049a1` | 0 |
| ts/util/clearConversationDraftAttachments.preload.ts | 1070 | `8dda60f04de5929edf737c734d85d6595fac650f2b40dfa05fe46ec01f78a1be` | 0 |
| ts/util/clearTimeoutIfNecessary.std.ts | 389 | `d2c8c523f34a46b2987d6e63b6ac19f054277c7f0c7885aca8d50249957c0e1f` | 0 |
| ts/util/combineNames.std.ts | 4110 | `6f67cbfade2d113b1e951a82e2863d65bc64c408585336091be31656a9e88b83` | 0 |
| ts/util/computeBlurHashUrl.std.ts | 3939 | `7ff3927212e356600fe8c9616d4cd68ddeb61c290ba3964bb29488209b5e0869` | 0 |
| ts/util/consoleLogger.std.ts | 796 | `f8320f2a866b3fee80d0d10eb5c0ae8c0867cb7848cd8453ab8cfe86dad83344` | 0 |
| ts/util/contactSpoofing.std.ts | 191 | `1450424c77e5d04806dcbffdadefe8809b3d922dc977cb39cc5b1ade7961031b` | 0 |
| ts/util/contactSupport.dom.tsx | 448 | `bd27227bc51d26304a42ec48bf247d5425e1f098cf3de2943e0df3d593d70ab0` | 0 |
| ts/util/conversationFilePaths.std.ts | 1434 | `4f40b43e70e7403254e311f22f0c0d7fd3724c5c638ca1baf5d33b15013bce16` | 0 |
| ts/util/copyDataMessageIntoMessage.std.ts | 641 | `93038df716a8a1f182594c3fd2bf0c1694d60c3f72761ac69efa8fcd69dcdbbc` | 0 |
| ts/util/copyLinksWithToast.dom.ts | 557 | `87826e261a8e012a97e3f70ae4ac0992effe8b263790ebaa2b0921e5ecc4fa3e` | 0 |
| ts/util/countMutedStats.std.ts | 1843 | `a56889e505e57fc442ffd4ced81bff3de24b6367741148f98327781b5659124b` | 0 |
| ts/util/countUnreadStats.std.ts | 7880 | `e891d24fa05293766218a2d8616f58d6a9495544f03cc2fd3274afab2321f002` | 0 |
| ts/util/createAvatarData.std.ts | 353 | `6067d34fc7b5889701a39afc10b6aa242f42a6b18a3898234467f4d38c79c2bf` | 0 |
| ts/util/createHTTPSAgent.node.ts | 6807 | `30c28a42da057a07668c90fc34940097db5085f8a1202a8d582d9b8209d0664a` | 0 |
| ts/util/createIPCEvents.preload.ts | 15893 | `ac4ca385212d9da25a37038b243301cab73ddde91f6984c4799e1ef36a50deb3` | 0 |
| ts/util/createIdenticon.preload.tsx | 3917 | `9652a858c49239016c7d1dff4fbe938435bbc41938daa9713f2dfeb12cf29058` | 0 |
| ts/util/createProxyAgent.node.ts | 4062 | `be23491877cdbe4e227e2f2bb6c0843f287245e3141abab44b44517151290206` | 0 |
| ts/util/createSupportUrl.std.ts | 1306 | `182ff95c5cc135be11f05791a167f7bf8eb2dba1e9e046c721ebf0fa7a32b697` | 0 |
| ts/util/currency.dom.ts | 7332 | `38e5d35bdaa0a378f31ed0a5b3bf886287a453d4e8049ad50bc5a75df4b84725` | 0 |
| ts/util/decipherWithAesKey.node.ts | 1869 | `57d7fc3e5a4407eddcffb861488394df0ba9a8d2380cbcfa88f41224be8c8c64` | 0 |
| ts/util/deconstructLookup.std.ts | 558 | `1eb3fd62d57f4c28715f5aa5bcd05bbfac50ceb1a6550be4c8a567990598d44a` | 0 |
| ts/util/deepClone.std.ts | 391 | `7214c01125a2ecde07db18fc488954e864bdd37fa1a41203026d8b9259384d48` | 0 |
| ts/util/deleteAllLogs.preload.ts | 523 | `79ee4d0fb0047ac99c63d4b3ae5baddc9cd168b4ad57806ca01701bcb37a709c` | 0 |
| ts/util/deleteAllMyStories.preload.ts | 472 | `68614a2bae87e8fda6e1018f01f8f42f3f16178543eb3e7dd905034a4c204e5f` | 0 |
| ts/util/deleteDraftAttachment.preload.ts | 503 | `f2e7481f1cac76aa430599b9cd51e9e5b287300473ede60e7f31f1553480160b` | 0 |
| ts/util/deleteForEveryone.preload.ts | 4770 | `9b1cfa96abb87d74b4bbabcc4d3da910a1538234c4cc3588b6d218edc9ef4183` | 0 |
| ts/util/deleteForMe.preload.ts | 7713 | `b5f48be805b3ef3ae625eb7923dfdde974381eb3d7346649166e786bfb0ddaf5` | 0 |
| ts/util/deleteForMe.types.std.ts | 121 | `24c354bb4ace5f4a803adaf580f39ff6f66ca27eb12423b7529aa67e2aabf556` | 0 |
| ts/util/deleteGroupStoryReplyForEveryone.preload.ts | 1059 | `e785c8bf488e796d838a9d9b4fe22b8caef69b05d50ad0022f2cf7db2c7b357b` | 0 |
| ts/util/deleteStoryForEveryone.preload.ts | 7320 | `e96d8745c59b8cc39e699e5b413d9b2ee6716160f8ef940970c420b68d7dedc3` | 0 |
| ts/util/deliveryReceipt.preload.ts | 1179 | `cf9cd33ccb09cecb12742cfb7586745bfea7193fd811f7b323303ba95ec080a5` | 0 |
| ts/util/denyPendingApprovalRequest.preload.ts | 1515 | `51a26b630f1d2ebdede476e5e13e0251347b4f49db8f54d14925ee6e3c3b4de2` | 0 |
| ts/util/desktopCapturer.preload.ts | 11679 | `5751c67e51513ff0dbd050f4e62b26cf37d713ca04b453f99380ac7ccc9a9ed5` | 0 |
| ts/util/diffArraysAsSets.std.ts | 586 | `c25b79ad5cb431167ad0733282425d6c2b87bce9f2dca6ea97c75d7c15405247` | 0 |
| ts/util/disableSignalPin.preload.ts | 1542 | `6541880970b38d77e96dbaed456fd80f310f9bcb5a877ab865db7bb3cc744518` | 0 |
| ts/util/distributionListToSendTarget.preload.ts | 1415 | `4fff73eb1643de0dbd0a87af653b8e814df4fd6dfbaf5d5b1e983374bfe264d5` | 0 |
| ts/util/dns.node.ts | 4601 | `aed823b42fa84ba32578cb4ae66c79c0755643add451c8963568782ca742a913` | 0 |
| ts/util/donations.dom.ts | 1570 | `ba099f6f95681ff3d6b5b3b29e2ea53348833d321eb29ef014f434fc1ce31a39` | 0 |
| ts/util/doubleCheckMissingQuoteReference.preload.ts | 2217 | `4d21f7e6b1f5643192fa1cc8e83311e4c2d34f93e8b8b2d1f512121b69bb9c9a` | 0 |
| ts/util/downloadAttachment.preload.ts | 6780 | `9c7c3bb3e1336e26fc017b9614725c90498e219d94c98b556354428c7064d18d` | 0 |
| ts/util/downloadAttachmentFromLocalBackup.preload.ts | 1666 | `12202d77c32225c1c5269cd11fe1616f54c798df7305e2677fe592fd39b1e3e5` | 0 |
| ts/util/downloadOnboardingStory.preload.ts | 3902 | `cdcaabd32ba68b6c5880f20a0b3aae569b40ef3b07520d3a531a6c1a9d399046` | 0 |
| ts/util/drop.std.ts | 258 | `319d372bd6ebb7647f15d651d4df88385f8efeed0d0b197f78c61e6187e0ce1e` | 0 |
| ts/util/dropNull.std.ts | 1785 | `63e273aa79de731ee67b1b231a07c80c81cfb2323457fa40d10e55f2e726b5e9` | 0 |
| ts/util/durationToPlaybackText.std.ts | 618 | `98ad06a72d6b7660d43c7566ebc420af0aafb55708caa2095620340da089f528` | 0 |
| ts/util/durations/constants.std.ts | 269 | `32a6a4d011b301ab152c0b140266799f71ba44e518110d67ea70f26c3fc6daee` | 0 |
| ts/util/durations/duration-in-seconds.std.ts | 1563 | `b6032890915e2329e25374e3f3599a0b4fa04fba40a8807fb4cae73678890031` | 0 |
| ts/util/durations/index.std.ts | 185 | `a87ac0623a0e03eaef56fa35f2b3879ce63c0ed7bd3b76360b68db31731540d7` | 0 |
| ts/util/editHelpers.std.ts | 5054 | `5947680f88d1b5081f7231add069a5f9dbb89d1b1f0f9fb8856ec31399b6c713` | 0 |
| ts/util/encodeDelimited.std.ts | 1741 | `f9a3c0b3d90401721068904ed51b6d1ccac7872e7f8ba67b95713cc79109671e` | 0 |
| ts/util/encryptConversationAttachments.preload.ts | 5415 | `b7f0b269ae7289d8ab63b1463de069a8a28e52e83d4716096988986fb7c84058` | 0 |
| ts/util/encryptLegacyAttachment.preload.ts | 3224 | `e8ffc56b989a8703615b6cc01d0e2885d1a346b8c7de1770e37b8491bb4b7ef0` | 0 |
| ts/util/encryptProfileData.preload.ts | 2830 | `d97e6c949a760e1e39a5851c91d88531790f0055cc941d8dc827c5c548909fc5` | 0 |
| ts/util/enqueuePollCreateForSend.dom.ts | 804 | `555e94af05b273433a86a5cc12fd63a585aefe8dfdc5e7daddf7ef776433a159` | 0 |
| ts/util/enum.std.ts | 1216 | `9583bbb9b4f3d5efd2f8776c9fe79669240188569f5728d4d1ef69366414d393` | 0 |
| ts/util/expirationTimer.std.ts | 3387 | `ce455bb945878cfec31886cc32450a0d95d553f08f8f5d0c665a384ca705a9cf` | 0 |
| ts/util/explodePromise.std.ts | 778 | `e7ba47eb633d574044f93af3d65091238d61f88f7af110a5207826188fe46e5f` | 0 |
| ts/util/exponentialBackoff.std.ts | 2406 | `66ba5c4d42ebb268e933383cf7f2519c8a47569f9cc1551a67794044726c3b3a` | 0 |
| ts/util/fileToBytes.std.ts | 618 | `91d3d3a27b806dd0944be7d40383c1336bc86772acb6539cf5d6973e4281ac69` | 0 |
| ts/util/filterAndSortConversations.std.ts | 7866 | `78f27dd564daa8ba76f26dbf6c438f72623a543097be462b92c164ed472a8019` | 0 |
| ts/util/filterCallLinks.dom.ts | 2290 | `cc8bc265367d52ac637a1f621bed863339e5c559535050969b846ca7003c7b49` | 0 |
| ts/util/finalStream.node.ts | 510 | `03c1d7d71b9cc3cff5dcd873d7abd7be4245959b2a52860d6144c0404fcf06b7` | 0 |
| ts/util/findAndDeleteOnboardingStoryIfExists.preload.ts | 2061 | `1fdeb839daa99b098f5b485b24dfc19576d813c2391d1d74025bcdc93a26275e` | 0 |
| ts/util/findAndFormatContact.preload.ts | 1274 | `a63f585b6f6ca570ab911f344254f120cde11884d65d9425db1deb9ca01a1bde` | 0 |
| ts/util/findStoryMessage.preload.ts | 3052 | `f0e4d78e0f4d9ba18411f559e4fffb2602594636b58d4b440d00bbb7fc988c21` | 0 |
| ts/util/focusableSelectors.std.ts | 1654 | `6f28ba7560c8aabe55ec610732f6e7edc3dbd9a5bac7d9a015a16bbedd29a649` | 0 |
| ts/util/formatBackupKeyForDisplay.std.ts | 477 | `b11de1d35d739741d00149faadd071608daf86738741f5b2e87cc53d86828470` | 0 |
| ts/util/formatDuration.std.ts | 598 | `0b65d435fd4e07a327e606e13e13461b66c2a8f42b2297829f14fd772f87f1fa` | 0 |
| ts/util/formatFileSize.std.ts | 317 | `132051552bda432300b8feb2b3ff708f1d28ea8754b430a0465ca94da5cb1167` | 0 |
| ts/util/formatTimestamp.dom.ts | 6543 | `ac59506aa0e7a30ef743cecde187c72bc5f9e7bdecc917878fcf8614967ab925` | 0 |
| ts/util/fuse.std.ts | 1535 | `cb74e0a12a1d5e3218cebf58f3f72ec0b951721715dcb8f54d1433b0dade80d4` | 0 |
| ts/util/generateBlurHash.std.ts | 868 | `5ed614bc09128a7d3bd89c553650b004246d8276215f75fc09eb1451bc480fa0` | 0 |
| ts/util/generateDonationReceipt.dom.ts | 16522 | `2c35857b33fff2669bd67e98c35361b2874c3e84a865c949edfb8a6c4eea13a5` | 0 |
| ts/util/generateMessageId.node.ts | 1827 | `016da4cad1d9feb7f6c20a3aa7b50be0db24f490905a3b51d2ea47c9c7cad9b1` | 0 |
| ts/util/getAboutText.dom.ts | 571 | `5d50f517a6af5dc3fc6eb609a58f0339f850187c9d9194af9e1c5a5a837856b6` | 0 |
| ts/util/getAddedByForGroup.preload.ts | 875 | `7ee408bbc5c94219e275afd14bbcebe364c7b3046d3ebe40bca274a5192cfbe6` | 0 |
| ts/util/getAnalogTime.std.ts | 533 | `bec812106faeec08de69132559a1ba197469f44de21d9398d494bcaeffdb357d` | 0 |
| ts/util/getAppErrorIcon.node.ts | 387 | `6eb276669fa27edef1cf17d8ad92c5c7d126e8b28c882e67d16454dad7ac77d6` | 0 |
| ts/util/getAvatarData.dom.ts | 691 | `679e3eb459ac1d4bdaa9f66b313417f5e607c3f6ffbc1f896e37fcf6e8dbce75` | 0 |
| ts/util/getBasicAuth.std.ts | 420 | `621fe836614b93deddcf27c5713006c4ba6740ff4ab6b3b14810d0e0bb044ae0` | 0 |
| ts/util/getCapabilities.std.ts | 407 | `c4371e38335bb1d9eab3f00c22458d9b4787285e0363679730d2d0f95e82ae4e` | 0 |
| ts/util/getChatBubbleColorData.std.ts | 1477 | `a1843f8db96d7ee845b0e4dab1d766c64d2688e2cb372696b06165cfb4031b7e` | 0 |
| ts/util/getColorForCallLink.std.ts | 980 | `711750e2d06e5fac7974b340ae6547b256b2f60b3294cc4f7b09f21ffceb7c6e` | 0 |
| ts/util/getConversation.preload.ts | 11163 | `078764b79ba25b88424d49eb71529146125f9ef442f78bc16db23c1be94f92e3` | 0 |
| ts/util/getConversationCallMode.std.ts | 676 | `ab86712ca609a66aa3ac375dea03a73c9a06932033e0ec50ecbd01e620c0b392` | 0 |
| ts/util/getConversationColorAttributes.std.ts | 1171 | `d3013c464453e5a410a50af7b96e519566bd6a029d94ef5efea75296f5940b0c` | 0 |
| ts/util/getConversationMembers.dom.ts | 2034 | `2dbdf8508adba7ce5ee91f9480bc089ea24ce2e754be64bd8ed494c6321846a9` | 0 |
| ts/util/getConversationTitleForPanelType.std.ts | 1892 | `b0576393b7b443104a10b1a989b92441e7e699b0ed8a9d7bbd4dc61180494472` | 0 |
| ts/util/getCountryData.dom.ts | 2357 | `12299cfadcb786ea2466d8ed7ea7c2e7148cde0f8a25f734bc092916e875d995` | 0 |
| ts/util/getCustomColorStyle.std.ts | 716 | `5d6abeedad8ab54ab54cfd493e4f3cc2976fef753cde029d840ec43d15a7b34e` | 0 |
| ts/util/getDeleteMaxAgeMs.dom.ts | 809 | `74e7e203cc68480435ea5a49d159a2f4344ede6a1f524b87d25ca80be070022b` | 0 |
| ts/util/getDraftPreview.preload.ts | 1831 | `df36fa8d23a5f6cb39d1107a7839a72a9c0985a59b6bcabcd3ff6639abfd4fba` | 0 |
| ts/util/getE164.std.ts | 746 | `6c49a2c7f900f753798221d663c1df951d61e5c4325e7f4db1a3ccb2d3a37625` | 0 |
| ts/util/getFontNameByTextScript.std.ts | 5606 | `eb4fa88bcfdb000dc472a7b180dadc156c130e7d44c09c0e45bc21dd8888faa8` | 0 |
| ts/util/getFreeDiskSpace.node.ts | 278 | `221feb792b7c0ae4474e1976aa22b45c0ef0fd310708a88b7df8b126c53c22fd` | 0 |
| ts/util/getGroupMemberships.dom.ts | 2588 | `664e7cf7ab76c431911af3daf78e67a320d4565d894f2a2c26b19a7619a4ed17` | 0 |
| ts/util/getHSL.std.ts | 1526 | `db3c579fd2602a4d8bdc330a31f9b9b6cd3b1304d6ece707918edfc97696b5af` | 0 |
| ts/util/getInitials.std.ts | 883 | `088dc964447dfd915ba9a26631f48807e195ef6f8ab3e089a7d16da99d85130d` | 0 |
| ts/util/getLastMessage.preload.ts | 3594 | `4500a638316bc85668a81b47644f27e5c2b1f8d0ab216e04c46f10ffa1abf22e` | 0 |
| ts/util/getLocalAttachmentUrl.std.ts | 3385 | `521982cf21b5d5aac77f52068bca618b2a60f49a87206eedf2a470086e397447` | 0 |
| ts/util/getMacAndUpdateHmac.node.ts | 1568 | `9c62ce1838fccff7d96f913ce0b5d29af68523b1b58662c734c0e96f7309808e` | 0 |
| ts/util/getMessageAge.std.ts | 415 | `e734bfe1b91b5eeca1c93ff8b07530b32df4738036a1a84ba09a963a88023d0b` | 0 |
| ts/util/getMessageAuthorText.preload.ts | 1999 | `46a7075427acbe9e2ea59dcee5034c8f478d75f82e0bd22399fce9560d611d6c` | 0 |
| ts/util/getMessageConversation.dom.ts | 453 | `2bc89f38d9d62121709f64f93d59be76dd1bd069d56a044d2911ee65c1761a85` | 0 |
| ts/util/getMessageQueueTime.dom.ts | 568 | `599b9b56dd17a8b1a338f8981dc1e4dfb4715037305eddeb9e9842f279d7befc` | 0 |
| ts/util/getMessageSentTimestamp.std.ts | 1025 | `04bd96e5258107f00dbea0ead84d2abf0070d8f24d31551e15eea890ccf5e154` | 0 |
| ts/util/getMessageSentTimestampSet.std.ts | 435 | `66447f00cf9d1d52f388a751a309dc05ba4015ada2b9e40fd951399ee845062f` | 0 |
| ts/util/getMockServerPort.dom.ts | 237 | `3d83c4c22b81346e0283cf942affa23be27bd8fc9adae365cf75ebe4f9baedd7` | 0 |
| ts/util/getMuteOptions.std.ts | 2604 | `ad40fea79a5180febc42c8c24adfacc69e8ac19afcbc0a4989f6a252469270ba` | 0 |
| ts/util/getMutedUntilText.std.ts | 830 | `3a2d062c85590a37dedae22b0951fa532d7903c387f26f2cdc3c54a030be7c14` | 0 |
| ts/util/getNotificationDataForMessage.preload.ts | 16972 | `8051b0792706343247f6f01b8f8975cd7953b797f95ba6924365db5d432f20d1` | 0 |
| ts/util/getNotificationTextForMessage.preload.ts | 2791 | `bf2320acb2ac68530ab11228e9cb97d34cc4488a6650ac7c5e8eb297dc24845f` | 0 |
| ts/util/getOwn.std.ts | 277 | `d1e284db150be54ec448894059f2e05608990a91d07d204ec2b455f0caec727c` | 0 |
| ts/util/getPinMessageTarget.preload.ts | 1740 | `b2377f8d144005f585acc46c9a404fed79437c05b5a5f0b3945470616de44f09` | 0 |
| ts/util/getProfile.preload.ts | 741 | `14405fdd892778e60357c6b3a9dff929ee8487570d333af1ec4bae67f06ab759` | 0 |
| ts/util/getQuoteBodyText.std.ts | 1294 | `5f8db3272c4f545f9f698c12181b83f0957f9cbb9cbefc21e0ee00ec49496212` | 0 |
| ts/util/getRecipientConversationIds.dom.ts | 862 | `5ff8f5092516a34628c9a5a5a238ccdbb112b66c7fc05c8d2a3c52afea4fca3e` | 0 |
| ts/util/getRecipients.dom.ts | 1799 | `f33e100a2dfc7188fdbc28f76ecce9e505783164cd0ba8d8cbb8f7fefc641842` | 0 |
| ts/util/getRecipientsByConversation.dom.ts | 930 | `7a07b8a74c46e04edcb8eca340ca169469ae2f9bd94a3ec77368a53a377eef4e` | 0 |
| ts/util/getRecoveryPassword.preload.ts | 615 | `b716bd966d1b45de93bdc2aee6eadbff8cfb38046383b3c229ecbdaa5688d341` | 0 |
| ts/util/getRegistrationLockString.preload.ts | 646 | `22dd71b71f3844a743cac3023109d36ea775800243db3f3281f7f4831d2a7d61` | 0 |
| ts/util/getSendOptions.preload.ts | 5781 | `55c6782ba399e473f8661c4ff6356b547c7595f02394d5dacba394f2f7d94293` | 0 |
| ts/util/getSendTarget.std.ts | 397 | `22651c11f80900a55e4f339b701ecdbd11115bc14be9646d4dafc8c1c5fbcff6` | 0 |
| ts/util/getServiceIdsForE164s.dom.ts | 4304 | `f83b2616f1b7d71bc43acb642cb1dfe276233a7cf915c5cfe462e81f801fcf1b` | 0 |
| ts/util/getSignalConnections.preload.ts | 1488 | `a596789d22044e12e363899a76587b4417a247497bf9d36226e2842c35d333fe` | 0 |
| ts/util/getStoryBackground.std.ts | 1793 | `813f5c07877d70460edf674ebc71d1457f58270851fc3099e3207634067c7911` | 0 |
| ts/util/getStoryDuration.dom.ts | 2915 | `46e54f29b6f5c0653f345fe8aef20cc38da848fea4d9faa6cd6aee22dc8ded6e` | 0 |
| ts/util/getStoryReplyContext.std.ts | 582 | `6a93f6aa8da87d9e8f9924065d3bdda9f1d2e211b9c06dde22870c606757c2e1` | 0 |
| ts/util/getStoryReplyText.std.ts | 940 | `2d83a3db45806383be7be32fcc5c3e0e9cb744124d7f53167386c49508f5c872` | 0 |
| ts/util/getStreamWithTimeout.node.ts | 1149 | `2edc8fc7448c02a1503e9a2c0d4ca4dde13bd08ba664688d72fffdef29f1cc03` | 0 |
| ts/util/getStringForConversationMerge.std.ts | 882 | `b2d50f106ddb55f8c61eebc70ad21e9c71ba6324db5067daca478701013d4402` | 0 |
| ts/util/getStringForPhoneNumberDiscovery.std.ts | 665 | `4bae9f6a7ab45547a2aa7a3da3f6a972ecc3c6ad38c47ccda8b78799feaf8eba` | 0 |
| ts/util/getStringForProfileChange.std.ts | 862 | `3c581ba3dd8f03d00f6e64515cf1142cc3b3f939b1ade14f62e52c267eee9ba8` | 0 |
| ts/util/getTestMegaphone.std.ts | 1504 | `a6cc56c97c9f21bc69b955ce95359f1a5bf7e31b8aa32a0c3338c4a96dfa69af` | 0 |
| ts/util/getThemeType.dom.ts | 778 | `345c3f07086fef6d4b9f456031f2f1f5ec9a73670758b273561c9202fcaa5e42` | 0 |
| ts/util/getTitle.preload.ts | 6470 | `fd052b4950f4b14b512508299b3a2c27e74eafe1fc22d28d29ade78fe5ef87f2` | 0 |
| ts/util/getUserAgent.node.ts | 765 | `836ec21adbfcf5f9f73393352ff086bb20ec62e7d856de594ee2b693b0ced59a` | 0 |
| ts/util/getValidLinkPreviews.node.ts | 1007 | `3ed38e90435ae7396f5c3a732156497fd856bd16df0987364bf86e52eb769f1f` | 0 |
| ts/util/giphy.std.ts | 759 | `b43d6b5e6cd086cbfcda17b7961da6f047ba8a945e2d064486c1b5c2c23757a4` | 0 |
| ts/util/gracefulFs.node.ts | 2245 | `da2060b956770d3f692cc49c5e04deeb1d849ea7e034522ab6b751d38bf179f6` | 0 |
| ts/util/grapheme.std.ts | 1161 | `7d725c474685a7519e781a958da9ed139c2a1cb0ec34b2362645f1941abe1b20` | 0 |
| ts/util/graphemeAndLinkAwareSlice.std.ts | 1539 | `06877c8d0a978cf3218cf58ddfca4a706af1755229ad30207cc2c4f2d8269623` | 0 |
| ts/util/groupAndOrderReactions.std.ts | 1703 | `bede34a9cd48807cc78f88957950afab0514e1706002f664e5b4f361d3c504a6` | 0 |
| ts/util/groupMemberNameCollisions.std.ts | 3061 | `fb80969f1305d4ca1b7e1406fb5c9df89cf5dcc5cd2eb52d508f31a3adda00a3` | 0 |
| ts/util/groupMembershipUtils.preload.ts | 6126 | `cc3aa3ea025fbfed09fdb0b10a48b45209592c4002441d346df536c617fcfc3d` | 0 |
| ts/util/groupSendEndorsements.preload.ts | 14725 | `5f0aa6d05a2e95de0fcf17cc7df1a674c9b61c3596c64cf08ac51ccc155c9677` | 0 |
| ts/util/groupWhile.std.ts | 1850 | `e23c5cb8ae323ca5d407fad547beb5f4f2f398e317b9a344dcaeb0bebbf2332c` | 0 |
| ts/util/handleEditMessage.preload.ts | 11858 | `2845f3fb492eea29e6d63dcfc10bc67619b467e886e870ab369e7d14ec6d2684` | 0 |
| ts/util/handleImageAttachment.preload.ts | 2567 | `483d5d3eea5edd24c69d0b67ca43685009d05d4320271f227588f87d01dffb9c` | 0 |
| ts/util/handleMessageSend.preload.ts | 8129 | `70bce55be05a167e55df188bee312ccc8c9fa494e679bfd573c2e44105d46f0e` | 0 |
| ts/util/handleMismatchedDevicesError.preload.ts | 2490 | `e620e7d86ac97afa4c15986a0ed93bd8e2dc7ea496aae43195ae74597247cb91` | 0 |
| ts/util/handleOutsideClick.dom.ts | 2917 | `f74a62f46831a2a6fdba78555b6b2ba71e552aa0735eaf20b5409ce93e0053aa` | 0 |
| ts/util/handleRetry.preload.ts | 20485 | `339eee3f740f2daa7b6ac46d7cd0118ff7bbeec1ef64a1ec51f7702dbf042e1f` | 0 |
| ts/util/handleServerAlerts.preload.ts | 4482 | `f1fe463950d20a974775a112b94fadbc4521b4231c1c90a0f0f7b5fdf93e08c6` | 0 |
| ts/util/handleVideoAttachment.dom.ts | 1995 | `95121dda94cc58ab525277e937da9562947764973733b770664e7d8bc0a67e43` | 0 |
| ts/util/hasAttachmentDownloads.std.ts | 2760 | `068cb856c34d2c5799de74d6f310dd3685231b32176228e9316ce93aaabcb3ed` | 0 |
| ts/util/hasDraft.std.ts | 482 | `6fcdfe55af5fb27b6c29044c9ff46e28b61c28bc366e68666381917e480b4250` | 0 |
| ts/util/hasDraftAttachments.std.ts | 496 | `a96f681064a0dd6c10659e04f8e696c9bcb1785a4fd50f1c7ec255302143165a` | 0 |
| ts/util/hslToRGB.std.ts | 803 | `3bc2f429fcd5532e79040c6165ee41c76bfedb7bfe97f88af4b38e9703d2dbf9` | 0 |
| ts/util/idForLogging.preload.ts | 1288 | `8dd886d40bca80e45ba79219fcfa1594bb08fb7423d0aca4f35ed109f5e22443` | 0 |
| ts/util/imagePathToBytes.dom.ts | 688 | `a8c252998ef1bbb495dbbafef9ad55417af9dc13a06eb0bdab3979cf0ae00700` | 0 |
| ts/util/imageToBlurHash.dom.ts | 1856 | `c00e34aeb16bda36f9e39dc850e5cd3b7eea763984203c8939b47ef811c9e776` | 0 |
| ts/util/incrementMessageCounter.preload.ts | 2211 | `309110c7b0b120670b29d25992029197563c750b6da1d92261ddac914a58bb46` | 0 |
| ts/util/inspectProtobufs.std.ts | 1399 | `100841cd08a317c5257b6a198fd1cf596d8324dda85aa9e432529c4009072c7d` | 0 |
| ts/util/isAbortError.std.ts | 303 | `4a043f32901780df5c32285c20788f26af2423342df451f5b22d60b51501bcfa` | 0 |
| ts/util/isAciString.std.ts | 300 | `8a3f506b4cd95701164c2a5eeb4c82e57f4640f6ae3549475c393a7cb14f3286` | 0 |
| ts/util/isAdminDeleteEnabled.dom.ts | 544 | `b4e9731a21077e68399f7c745b36bcdcea1ec7b5dbedf23aa938195daee1af0f` | 0 |
| ts/util/isBackupEnabled.preload.ts | 485 | `0b96e98575425cfd78e4b9264259d4e2358aa03667b7156980c5f67af64965df` | 0 |
| ts/util/isBlocked.preload.ts | 938 | `218285338867ac70a6acf38d54669cf1a48936ce710917d258c14e105c9d51d9` | 0 |
| ts/util/isCallSafe.dom.ts | 1000 | `ee10d177b75185d0ecd59e3ae0c9c1c4d12f2d3ad0409696dd8176a6433739e0` | 0 |
| ts/util/isConversationAccepted.preload.ts | 3503 | `a51aa78d4022a17d9f267f88438e8ee0dd76ee464897f93ed2be839a37cbce66` | 0 |
| ts/util/isConversationMuted.std.ts | 404 | `e0ae91ca02d8d41e41c5825b04ce381156abcd8fabe02bed23b6156536b53435` | 0 |
| ts/util/isConversationNameKnown.std.ts | 663 | `1bb0afa60e3b2de1d671d8a7a507a151d6b27e4f902910abe6b6f2b0febd0657` | 0 |
| ts/util/isConversationSMSOnly.std.ts | 681 | `1cd6b70868c7c624d2797d6cd2e8d86d2b06c7809de4f48c34aaf39348280dee` | 0 |
| ts/util/isConversationUnread.std.ts | 353 | `55338c9efc2fa6d29d228ae061dd6b6b4a2614b9ad49a5946369c91d6cd60c9f` | 0 |
| ts/util/isConversationUnregistered.dom.ts | 1285 | `866317525360b28c6f957384e717c94bdd0f6449e0290106b108c72a2f1a12b4` | 0 |
| ts/util/isFeatureEnabled.dom.ts | 2329 | `73a676e74cf5c3a7a8abe56ed350404e7f1d2e19572f6a92c97865c3c3fa381e` | 0 |
| ts/util/isFileDangerous.std.ts | 449 | `25b7503879278d8e5e2f274b92dce4c3692221a154def49121f33c7c179d0769` | 0 |
| ts/util/isGroupInStoryMode.std.ts | 721 | `c820ad7c24160704eddff1d59f16a4b2d85b176c981d2d9db3984daf293e71fe` | 0 |
| ts/util/isGroupOrAdhocCall.std.ts | 1016 | `554aca605911f4d83b2170e51532c8ce8977538ad64a4191c601632813b8de94` | 0 |
| ts/util/isInSystemContacts.std.ts | 588 | `499b44d22bb306fca450f20c4dfcf848bd2d83427562c27704e380bb45d473ba` | 0 |
| ts/util/isInternalFeaturesEnabled.dom.ts | 664 | `c3517e44fb38b471c3cad69763057139bc4da85c1a99556e687bc28c72e61f36` | 0 |
| ts/util/isKnownProtoEnumMember.std.ts | 361 | `d0da8604e6f098430c8a4251efe4a9ceef6e6774a746e1c36765728f0805d612` | 0 |
| ts/util/isLinkAndSyncEnabled.preload.ts | 535 | `5a91781d55b8936c3c60dd3db47f1fd8c1fd65b1437fd9a16f1d3e9f385e1cd4` | 0 |
| ts/util/isLocalBackupsEnabled.dom.ts | 822 | `fc70c8e47bf5fb349a19d8467b2ca1de9adec39c64f6bcda713aad521107895b` | 0 |
| ts/util/isMessageEmpty.preload.ts | 3494 | `35c5c9d2855e1bbb9e22ddb9c969830f50f69dc476149f42da4872629f8dea21` | 0 |
| ts/util/isMessageNoteToSelf.dom.ts | 379 | `34a62bd632d456021f7d71e056f44aa58a744e2f075032bb680371181feef7b1` | 0 |
| ts/util/isMessageUnread.std.ts | 375 | `70fa4c4fed37d05f40a7cc5bf19e2620d144c92b1f549a17a290f3263d24ff06` | 0 |
| ts/util/isMockServer.dom.ts | 415 | `cfeaaced47de568b64664dcf3b9dbda19face88b1868d830d3fdf80c16731bc0` | 0 |
| ts/util/isNormalNumber.std.ts | 247 | `87e6a773fe4ef60cd327e9fe3244ab0d1f35fa3f111b53545a9b4bdeff65c438` | 0 |
| ts/util/isNotNil.std.ts | 216 | `34b01b48c1757b71431f4023837da67f55a35de85ad58bbd6c3d851d89a7bae0` | 0 |
| ts/util/isPathInside.node.ts | 572 | `d4b017f2791cb92120feef9514fd340f5adacf0d9a358bdc915a27a01c3fe560` | 0 |
| ts/util/isProtoBinaryEncodingEnabled.dom.ts | 577 | `e2b50777d721d690ba8f1bcc02068517a0b4b8c62dd87f6802296b58578d6847` | 0 |
| ts/util/isRecord.std.ts | 232 | `46cc64e2b274f8587c447833a7633baf5eebb4ff4a509e851a88361fb2f50c6d` | 0 |
| ts/util/isRelinkingToSameAccount.std.ts | 1281 | `caff088a3ab94e314c97d867554f0c8864f0413e775acddbab09cb79d487be22` | 0 |
| ts/util/isSafetyNumberNotAvailable.std.ts | 414 | `3711e376ef0283c0818fb2fd7a134294031bf1546e790ddb1e9ad50724d28cd1` | 0 |
| ts/util/isSameAvatarData.std.ts | 450 | `87d47fe15c87927b7a4a6dcfc5b2b4ba774a5944bf14c5573de89a88ac2c017a` | 0 |
| ts/util/isShallowEqual.std.ts | 649 | `101b0f45b8b9f046ff2fc5c8fa4df37e7e29129a0dab4d6f8d7b77da728796fd` | 0 |
| ts/util/isSignalConversation.dom.ts | 511 | `dfe48ad7c8d08974b81124631ec63c2f93f49acf8d02bd69ce223104cc6babd8` | 0 |
| ts/util/isSorted.std.ts | 345 | `4359ac509ee215b578c3152535a65347e9dd03fc3ce53dc7c0abf86cb0838cdb` | 0 |
| ts/util/isStagingServer.dom.ts | 482 | `3a0e870a3b75b613ea6e81dbf3744dead953e3e787fd8735a419dcd69aec679f` | 0 |
| ts/util/isTooOldToEditMessage.std.ts | 481 | `614d4e38e1737a33f2dd1f6f6a2690ae08f709b6d81917a110f4b66f8aa3ebd5` | 0 |
| ts/util/isValidE164.std.ts | 644 | `d8e54c5f6afd894a31205cce2d8d80ac59e7942742530ee1fa3874235ee6592d` | 0 |
| ts/util/isValidTapToView.std.ts | 884 | `c64e24066e921b604d88beefd11fa24fb2f92ce4f7d0e28788b676fd9d543dfa` | 0 |
| ts/util/isValidUuid.std.ts | 870 | `1824687fd1b9336d8bbc64e08cf8d24a70b7b439fab96d9491ec33d2e661d81c` | 0 |
| ts/util/isVideoGoodForStories.std.ts | 3676 | `3c4291bd590841869636b2fbec3cef471585f4e1340d54d94bbd5520d20dc420` | 0 |
| ts/util/isVoiceMessagePlayed.std.ts | 1369 | `d71b4d58dec91682e28d3c34398eeb1374f27ce50090ee5e71663afd3fdc85d7` | 0 |
| ts/util/isWindowDragElement.std.ts | 583 | `1c59db38c72f57b64f504ef0e87798c8b5222554f86a40de04627528c8f195ab` | 0 |
| ts/util/iterables.std.ts | 9012 | `df1481f5fc8d2299a6ee9cd00ec833bff46c5908f8c65224f89c0fdb6aa403a9` | 0 |
| ts/util/keyboard.dom.ts | 692 | `1dfc49c43ab76995ec4b8585a7ac87ee44b12833bdcaf0f54b6c29f60f8400b1` | 0 |
| ts/util/leaveAllGroups.preload.ts | 1142 | `0316c120affbe195660084da2a14cdba3ff9f4ee19acd638034f5805018a7c58` | 0 |
| ts/util/leftPaneWidth.std.ts | 821 | `2a7a84a9cd0def169de2d4d4c4ebeb6a2fdf69dc6bc5993b21f9fbf43c3fe5bd` | 0 |
| ts/util/libphonenumberInstance.std.ts | 857 | `4b851bf8a287dcee36725d894ce720f02e66e5881f96e3aff9a933829b7548aa` | 0 |
| ts/util/libphonenumberUtil.std.ts | 1366 | `6e9655a86fd4c7f2b15f10f5412dcd4c6317687e7c9e8d5a4f77896ec5699974` | 0 |
| ts/util/lightSessionResetQueue.std.ts | 217 | `652c1b8fad79dcc2aed708702c72aed3675a862b1aba0196959b1a8131072cf0` | 0 |
| ts/util/lint/license_comments.node.ts | 7669 | `19e32144898e12fa88b8918a7fe856ee76eb3fe24a8daeff607259192433d787` | 0 |
| ts/util/lint/linter.node.ts | 16254 | `cddf75c403af03840aeb492131e343db8acfdb79507601c6f98636d9e58a2a6f` | 0 |
| ts/util/lint/sort_exceptions.node.ts | 404 | `da7913c91ea28c4113276b419374c9136567f2ec5822081ac0c679ae8e988d26` | 0 |
| ts/util/lint/types.std.ts | 1607 | `ded0e836c4de50dee595a5485525a532cc0e3a71be31ead24e20839e3c98885d` | 0 |
| ts/util/lint/util.node.ts | 762 | `01ab57611205f716ae1650d6112aca3e0b626d7a0788cc4c53806b6d7c0e995d` | 0 |
| ts/util/linuxPasswordStoreFlags.std.ts | 415 | `e4de7129d4e90fbd10ab0ac1317094ef39ef4b0b2c068d6ea52375b0bcad8cc3` | 0 |
| ts/util/linuxPasswordStoreMigration.main.ts | 1825 | `6daa1884a80a2029a25a184a34d1a3c6e6cb3250fc1b1cb2668f2e8f7fe8d1ac` | 0 |
| ts/util/loadImage.std.ts | 621 | `c71cfb43d9d9bfc3720630b605b328ad0ac679bcb8e2928120fc85e288225404` | 0 |
| ts/util/loadable.std.ts | 442 | `fea1d5a9696510d80e17edefd18bddef651140425ecc2db9db4c5d0e2087875d` | 0 |
| ts/util/logPadSize.std.ts | 236 | `8622de3deaf36a85434c39fb240b34005f8b0536ad626b4b1b5468641125ca4c` | 0 |
| ts/util/logPadding.node.ts | 2193 | `f85a4841470616b88a9635811e3b944fafff3e52e4ec7bf48b649fa939b8891d` | 0 |
| ts/util/longAttachment.std.ts | 679 | `d4b567273470502c22f6159b7b6e064f7120a1241c5d06d1a5177dcaaf0d14a3` | 0 |
| ts/util/longRunningTaskWrapper.dom.tsx | 2715 | `67a5fdb17f6dfef2ce5425955a299656594f7ab09ac4b5b0d5c0f84e6697653d` | 0 |
| ts/util/lookupConversationWithoutServiceId.preload.ts | 4778 | `b378a74ee925e7291fd4ac722aefb853f89bf7c849cabab7355a0ec7ce034a01` | 0 |
| ts/util/makeLookup.std.ts | 369 | `a7be278b3cbb3e6cccc6b1347e9ab7990c031240ab266c59b5e3c62874364d00` | 0 |
| ts/util/makeQuote.preload.ts | 4187 | `4e08350d74d018a968d2d8962e7cf322686c6f931b6230f981a0e6890a4ede7e` | 0 |
| ts/util/mapEmplace.std.ts | 2295 | `6f223db742d8f85ac9b178d63a629257a763045b5e07786498ab8d1571558d41` | 0 |
| ts/util/mapObjectWithSpec.std.ts | 1516 | `e533c5e775266bec0577cf82de4421b05a6ad5407d5e204b9746f9bd32d813ab` | 0 |
| ts/util/mapUtil.std.ts | 975 | `ebf97aadf04e88133a1a8ebaab767dc3938a303f4ae5d0c1b3129c20eccf742a` | 0 |
| ts/util/markConversationRead.preload.ts | 9352 | `79b8e11eaaf973fbd69780c3e7ebfebce7a3f16b99270130c89b09ebf2055b6e` | 0 |
| ts/util/markOnboardingStoryAsRead.preload.ts | 1771 | `74fec0cf37bdaf270885bd0d40e62e6d0df345b4d75c90b31ed199e8692b77e6` | 0 |
| ts/util/maybeForwardMessages.preload.ts | 7812 | `8ff1857a84cb2ae68b9a1884724f3d33f09bf260fd44d0401c9866bbf06a395f` | 0 |
| ts/util/messageBatcher.preload.ts | 2300 | `e171034f13a238360f4646124b5217fad1f90e05e35f18f6c1730d114c9eb4f9` | 0 |
| ts/util/messageFilePaths.std.ts | 3267 | `4299b1f4df915e8830f693f7772d276ff0b69ace643cb0b745793c8c04eab670` | 0 |
| ts/util/mightStillBeOnTransitTier.dom.ts | 1024 | `f9548e2f6167cb2fff4af59b90a11a9a043aa3523928afdb25f2e33e49e6ef18` | 0 |
| ts/util/migrateColor.node.ts | 1067 | `b5768d42e11b5498b5d431b031fd107dded42b66949843a5ca01afb5e697f550` | 0 |
| ts/util/migrations.preload.ts | 7484 | `2dd03eff9a77ebc847551cf4e18a506b663c9127e41686caf11bc7e3e23dd42b` | 0 |
| ts/util/missingCaseError.std.ts | 949 | `27302430e0afc5c3b40f249762f1bfa5298052051cd6463bf055bb5beaa48aa4` | 0 |
| ts/util/modifyTargetMessage.preload.ts | 13351 | `d353356bb8b8bb2617b4710e7ba7ae927a87a4805fbb3dc6c7eb01b132b42fc8` | 0 |
| ts/util/nicknames.dom.ts | 442 | `fda15e8600878b7bf06771e2ca7ef1ae8bd6c5eefe573614f759b7a622136e00` | 0 |
| ts/util/normalizeAci.std.ts | 1256 | `3fbbedf8c961a43ca13d33a97b682526d05c546ffd172e637114d33955e1575e` | 0 |
| ts/util/normalizeDeviceName.std.ts | 272 | `c42ea4e27610657aca43eab2c284672cc6cf2e4be3f4cc9f150cb9a1b044a199` | 0 |
| ts/util/normalizePin.std.ts | 862 | `175b04c334f137a925297b2a25871a9e0bbec538595ca52bfed4bdfd4e983abb` | 0 |
| ts/util/normalizeProfileName.std.ts | 224 | `f7413bf0f577d4f08d70dad470b77b50470d60066b8b1aa59a6afa80316e613d` | 0 |
| ts/util/notifyWhileMuted.preload.ts | 1000 | `7c5a4611e338cc56564f8142d41d8830fd78c83b14f88baca9da4e3b53f6ad23` | 0 |
| ts/util/notifyWhileMuted.std.ts | 3123 | `21f6dcd2ac6ec2f827f61100c557a53c79c0ea5c9aa4ec723003619e42474155` | 0 |
| ts/util/numbers.std.ts | 1268 | `247531cd6c54fc589b93cdc3483d81837cf8b9fe74fcf5ca9f434b0cbc3685b9` | 0 |
| ts/util/objectMap.std.ts | 298 | `5ef850ab78f8b1d742f7cc55069c7c4f19fe679d2551e350b1ff276e1eac5289` | 0 |
| ts/util/onCallEventSync.preload.ts | 1171 | `e97c7c89919f6b9eafab8c6d7d14cf02ce85748340d411d7c0ec0596c5717381` | 0 |
| ts/util/onCallLinkUpdateSync.preload.ts | 3270 | `256765506b23f36ce083c31178f46c7f7d4d8d2f942e97ca90640280c41df5de` | 0 |
| ts/util/onCallLogEventSync.preload.ts | 2559 | `e4ff30eac9ad05f5853b7be345149400b6800ea0cb33dbecc513534ff2e7db40` | 0 |
| ts/util/onDeviceNameChangeSync.preload.ts | 3812 | `4bbc564ad03167f66fd1ad783cc9c10eefcf32e5a40ae5d0361c676c07cac6f9` | 0 |
| ts/util/onStoryRecipientUpdate.preload.ts | 7456 | `4076a98c7c0f05af1c69af64c940ad5fd8d4efac76b1717681c76a77043584b8` | 0 |
| ts/util/oomNotifier.node.ts | 727 | `e4bb1eef348f05831ff1644ee9b46307a36e0d2447ccebf70b984f6b090f65bf` | 0 |
| ts/util/openLinkInWebBrowser.dom.ts | 276 | `f9da9691fabaed65b02682e0dbc56e1f58548c41b614402e1d7909cf9bd54e12` | 0 |
| ts/util/os/osMain.node.ts | 1368 | `227d0a38947d6cb8d95eee01cecf17c060f81a6e8859eda2ab2c704d92321106` | 0 |
| ts/util/os/osPreload.preload.ts | 257 | `616dbb400892ccc1e6826c20600d1b93eef26cb4dc1b039c895e247a376bf7c4` | 0 |
| ts/util/os/promptOSAuthMain.main.ts | 5209 | `a2879695be293056a3097ae81676c2a1b1737667ca6cae853d2f83ce89ffb9f7` | 0 |
| ts/util/os/shared.std.ts | 1709 | `a5204cbc9d8158a13516a7f5cf20d49479d4b1d7649a516e7293648d96f2b31d` | 0 |
| ts/util/packageJson.main.ts | 445 | `ea3839c6837774e76fb9fe5a316512fd51a7613fc74b52fb6a248b96a7bfb4b1` | 0 |
| ts/util/parseIntOrThrow.std.ts | 469 | `f7bc8ddecacc312a5f0d21386867ae1976e6ecb6193a633ad8f307e23bf3c325` | 0 |
| ts/util/parseIntWithFallback.std.ts | 332 | `9acf22e1c298903da55370430f5fce5548c2d951c52868861967142e014e5f09` | 0 |
| ts/util/parseRemoteClientExpiration.dom.ts | 840 | `ca25ac93e341e7a85797f23845e2178ba69c225d849086ab55de275efcb4173c` | 0 |
| ts/util/parseRetryAfter.std.ts | 862 | `82806919f239bee72021d3666d5b59a0cbf425786a8d002e03ad7e7939825443` | 0 |
| ts/util/pemToDer.std.ts | 396 | `3733684ba6f972e15640944e364dd2732c7e2685aca80ce501560373babdb83b` | 0 |
| ts/util/phoneNumberDiscoverability.std.ts | 456 | `79298cd07de6f65f2372fa4340a51f4f089e2ab57eaf7210f5ae0499c604fa4b` | 0 |
| ts/util/phoneNumberSharingMode.preload.ts | 1176 | `6df08d2462c65867000ca63f97d36fb4cce4276b4aca48b77e184f2216e646bc` | 0 |
| ts/util/pinnedMessages.dom.ts | 384 | `fcb599b524e63ab0faaecdadd581ffaa4b85f1c7629c0111938308671aa73e54` | 0 |
| ts/util/pinnedMessages.std.ts | 469 | `963302a611b19787159df6191102e1a1d49755437a6b12976244ff6acd76e88c` | 0 |
| ts/util/popperUtil.std.ts | 1014 | `2ea01a703ed94ae8aeaf9e89882eb4bc0d4f0d42d4ebb9dbf3bbe7096053a65b` | 0 |
| ts/util/preload.preload.ts | 4352 | `f1604dc4c130aa603020bf3fb16499caf7cdefe391995daa10a617af33e59433` | 0 |
| ts/util/prependStream.node.ts | 426 | `176396e8dddb72b5434264748cc074563ec30a343ba3d1b644d120732b664ecf` | 0 |
| ts/util/privacy.node.ts | 7354 | `cf795712483bce49a4226e2d7456ac79ec104f2279fcc224d532e5e8627f97bf` | 0 |
| ts/util/processAttachment.preload.ts | 2699 | `6848127c0df1c69aea4a8103511465e4f686beb2fd4ee5e2699af9b471d92595` | 0 |
| ts/util/processImageFile.dom.ts | 1080 | `48b3e0972cf228b8c31d8410729e2eaf50320348d69a7d066f571ac8d2a67965` | 0 |
| ts/util/promptOSAuth.preload.ts | 1959 | `b457f7bd1543ce86fbb56de0437581e8180a38b176fe9360601f6bc272eed73b` | 0 |
| ts/util/queueAttachmentDownloads.preload.ts | 24756 | `d97fbb45ba2412c90ef14543c9684587a0670b88cee4cbbf98d4180b761148be` | 0 |
| ts/util/reallyJsonStringify.std.ts | 1115 | `0e13a2b7367ea40ed11f0599a7214c68d8bb756c88dbf2060ce8c79518f4a91b` | 0 |
| ts/util/refMerger.std.ts | 1347 | `da3ea4496e16953969703ff52ff0939b58d31e54cbb5eaf566a9caad81bd4e1a` | 0 |
| ts/util/registration.preload.ts | 716 | `0f6e6b9a0fbab38c03c771e56776677f2a9e78c023093e43b216c72b478a9ddf` | 0 |
| ts/util/registrationLock.preload.ts | 1351 | `b54cc405725299ab9fd8bbccbe04e3fb0a59413a8a31dad260dfbce702214aa1` | 0 |
| ts/util/relaunch.main.ts | 537 | `214cb4d8cf08757ad4083fbea1751f48b665c815b87414a137a226b09710c266` | 0 |
| ts/util/removeDiacritics.std.ts | 205 | `b79d37ea3aa5f9bb82ebea05b1f99ffea1045376b51dfebca9b9fb0309b2787d` | 0 |
| ts/util/removePendingMember.preload.ts | 1627 | `4a2290ad33ef151f617b5bb4e6515a5ea4d70b62783c90219aeb4ab3cfb377d3` | 0 |
| ts/util/replaceIndex.std.ts | 353 | `39a0b6ff218acaa5487d84c07414d74436b113fed63c5a8feee496b75abd238d` | 0 |
| ts/util/requestMicrophonePermissions.dom.ts | 473 | `a98181c2f033d20c36daa278e7bfcae1a5af7fc14d7fc868b7a51147bb85b22a` | 0 |
| ts/util/resolveAttachmentDraftData.preload.ts | 854 | `d82c3f807eba950eb1354ffbf8a486aa6a3194e40c7cf971b26bbf94bc124e04` | 0 |
| ts/util/resolveCanonicalLocales.std.ts | 505 | `8852fa895c58066c10f53d490e3f423488b60592bf92fda522ad2a296b2ace9d` | 0 |
| ts/util/resolveDraftAttachmentOnDisk.preload.ts | 1740 | `4705ddf537ec2363e12e597d9267131dcdb49efd0c63988db47779b5af59af64` | 0 |
| ts/util/resolveStorySendStatus.std.ts | 1998 | `36390d26dee425bd5e519bda5336f93038de7444b48d07455f014cbf82de15ed` | 0 |
| ts/util/rgbToHSL.std.ts | 1200 | `3601642cbda8f45d3541367690dcd1f155624935e8b1a749ec3995148b0c637f` | 0 |
| ts/util/ringrtc/nonRenderedRemoteParticipant.std.ts | 318 | `895338c0c92e7d7f8b39e1f5bc2558eb9f224c513a56dd6c85405b3e4b8ad196` | 0 |
| ts/util/ringrtc/normalizeGroupCallTimestamp.std.ts | 429 | `514065c65f54d482c2cb641943d6b5fe806b1ddc16be6e79d6abcd5295163993` | 0 |
| ts/util/rotatingPinoDest.node.ts | 2417 | `b53861891275d741dfc90e062b8e395e3a7b141bbfb02cf5a1e59f297ff7dea4` | 0 |
| ts/util/safetyNumber.preload.ts | 2247 | `0bde70dffb488248fcc242aee8fab8d2632ab428833f08dcc971605e9c79f8f2` | 0 |
| ts/util/scaleImageToLevel.preload.ts | 4263 | `2b06014c813158c2878c19c2fc49d0c50c11cf8068f7d69f7f3db75a369706a8` | 0 |
| ts/util/schemas.std.ts | 5921 | `ec5efbfff14875a501ea3d99c88b7388589fc76b83f8c27efe541188b5d0ff94` | 0 |
| ts/util/scrollUtil.std.ts | 789 | `4e3152a39ea26b3e1049c5561f2b28012b74b15f42a8e001324214fe57b89f54` | 0 |
| ts/util/search.std.ts | 3487 | `59652eb55b091f486291292893ee5a16a4c9651b64dcb776d0d39d5fa1a74533` | 0 |
| ts/util/searchConversationTitles.std.ts | 1521 | `2cb68789c7e0110edb020842e2317753e91b688b01e89057f21239af07c9ba79` | 0 |
| ts/util/sendCallLinkUpdateSync.preload.ts | 2660 | `440609832fb7638ced1c4fa48f0cbf293e446c7fa0d0d1a3d23014fc442eb4e9` | 0 |
| ts/util/sendDeleteForEveryoneMessage.preload.ts | 3959 | `ce6c9ad23bff898d2cdf2c05056010e7b39d1ad743257f71dccbabff22e47c48` | 0 |
| ts/util/sendEditedMessage.preload.ts | 7154 | `59881af8070e251d19243faa7f2cd2d123d63f6b073dad520bd7d006ef803943` | 0 |
| ts/util/sendReceipts.preload.ts | 5053 | `2ed5ac888a947440a8047fa4430899595101d85d58cdbb96e2ede838babeb31b` | 0 |
| ts/util/sendStoryMessage.preload.ts | 12655 | `cad4deb2cdceb1f9f59013bcc0c622056c59fe940ad1aeab8e89d5bdc1440a6c` | 0 |
| ts/util/sendToGroup.preload.ts | 44699 | `3db9f7d2202dc1efcb42f30de056e71bbdc2e1b9e99ef9de5e2a5a1db5624e04` | 0 |
| ts/util/sessionTranslation.node.ts | 10108 | `4f869cb73e3f03c961b488855596c4c349a3d8f29bd73ef528cd5e773b5a6155` | 0 |
| ts/util/setDocumentLocale.dom.ts | 395 | `1bf3d9105a598300110ad5bc12e478671a334080abaa727c24b6d7eeb94b8357` | 0 |
| ts/util/setUtil.std.ts | 728 | `f5637faeaffe6ae8a6cc6add659652a3f3ae27bb5efecbbc55bdb50f6745c837` | 0 |
| ts/util/setupI18n.dom.tsx | 1363 | `0015d1a75a7eaa4f41317d2d2084c0de65335a9c5699f4274551433c849950bb` | 0 |
| ts/util/setupI18nMain.std.ts | 4911 | `20dc09f8370322d8813fc2383c63b526364045a06a23a5ab4bf6ca1c1ccd4c02` | 0 |
| ts/util/sharedContact.std.ts | 2779 | `efbe6bce7d27c4719da029975c3ea9525321c7f41d8ba10dbbe09f9270fa6fb8` | 0 |
| ts/util/sharedContactCreateConversation.dom.ts | 1562 | `cbc5992119a90468bf668e79d30e1f6ad3ba780e09fd3e1a5acbe7b4110c2162` | 0 |
| ts/util/sharedGroupNames.dom.ts | 2631 | `3df15c0dbf841cfccac944ece8a0e2123ba5397872f3646927628a7fe80e4d4b` | 0 |
| ts/util/shouldDownloadStory.preload.ts | 831 | `bc477f71e3d47cc5ce54461dbc8991681f631cebadaa3369f9a561e08169851c` | 0 |
| ts/util/shouldNeverBeCalled.std.ts | 432 | `6b64237ba0a0061556ef3581442cd957f09a4b2f93d1d0c4b39bfed87d97e02a` | 0 |
| ts/util/shouldShowInvalidMessageToast.preload.ts | 2033 | `2e2d32d6378a4c8cb30566d7cdddcbfff5ed9a4f286bb902c05329c1f3e2b898` | 0 |
| ts/util/shouldStoryReplyNotifyUser.preload.ts | 2269 | `43d076852b7ad843b28d947b152ea995314b6f9cb2334095958762b95bf8bdec` | 0 |
| ts/util/showConfirmationDialog.dom.tsx | 2428 | `df1349e87266dc7d4d6611093748a29b2bfc95432894fcb37bbe115538af662e` | 0 |
| ts/util/showDownloadFailedToast.dom.ts | 881 | `1f0856006edc82bbe9aee5f3657f785cb7e8fcace1986380c84243163448780f` | 0 |
| ts/util/signalRoutes.std.ts | 21999 | `50fc40181d8f1950541ed4ca82ed6b132d0b054ec4addb61922e5c52c9d8ece1` | 0 |
| ts/util/sleep.std.ts | 483 | `ba5d4901ebb43ad3b641d24a0d6421d8b4206b8e80cd8f28019c38a345667969` | 0 |
| ts/util/sleeper.std.ts | 2637 | `99ebcacb7b112ab31fd6d365a7b208a7cc47d0164b85220375a01c65dec7b0c8` | 0 |
| ts/util/sniffImageMimeType.std.ts | 2469 | `8d1d8a5f134bc4a631cfd0f449dc6f9fcccf84c0676681bc03ea971771260c87` | 0 |
| ts/util/sortByTitle.std.ts | 277 | `9d3e7916c507adfbc88f4e44414f8483aab57fa27c09ab5aa1f502ec94079b53` | 0 |
| ts/util/splitText.std.ts | 1079 | `d945e135f8cb15f7ae33569e4c786cddc9e4846929f4b151fbab0bb71ec7bb11` | 0 |
| ts/util/startTimeTravelDetector.std.ts | 429 | `ad8b0036571ded8f72af1942187147dd142718cdbf3cd10c5ff327e665918e23` | 0 |
| ts/util/stories.preload.ts | 682 | `0f37eec3a3a74fb575cc5cf13d056939baf4502a696da3badba815f2535a685c` | 0 |
| ts/util/stripNewlinesForLeftPane.std.ts | 685 | `b04c7af6bf9275f3eb89476dfe08cdad1ac019d9cfbb8e7def39143fd50592ff` | 0 |
| ts/util/subscriptionConfiguration.preload.ts | 2569 | `a89e5ee10d42ed8c27f536480f4fb1916663e221d457ff121acbbe2f6fda1525` | 0 |
| ts/util/syncIdentifiers.preload.ts | 5288 | `76e4d8a0b5959e68bd2d22e3aebfb5d5e9c0bfd2a3cf914fe44b476b74a00e03` | 0 |
| ts/util/syncTasks.preload.ts | 7851 | `1f3f19614d04af5c1a619824245e4716e64ba5a7035d18b567550d144c7c12ea` | 0 |
| ts/util/syncTasks.types.std.ts | 124 | `6e0f354f03c3b231f59babb4fe5ce6a4326be78ff4cf207678075b59d2e0354d` | 0 |
| ts/util/theme.std.ts | 770 | `420bc0ebdb52af90f7c3ba27c7ad1fa8dd842915f30d79066b3d46b1245d657a` | 0 |
| ts/util/throttle.std.ts | 1592 | `d0864a505ce755b33f01673306a1856d7a4840b1d968029be0ef23b2d3a16ef0` | 0 |
| ts/util/timeAndLogIfTooLong.std.ts | 537 | `de9a94399e0395170d2d52a5563e69b5e27fc6d332d35428f0c46d48b316c7ab` | 0 |
| ts/util/timelineUtil.std.ts | 6163 | `18b1d6b5f0875e3aeb3f90e5f1711f5e66b585e22f963458a3ffa4d11b23f31d` | 0 |
| ts/util/timeout.std.ts | 2616 | `a6447127bc4eabc1e3eb9d55ec5a9e927e58430682238476d604281158e0b4e3` | 0 |
| ts/util/timer.std.ts | 808 | `45aa9dcdae83c7b78c69a8da1bfd563b2cc7278470eee4323e9007184784794c` | 0 |
| ts/util/timestamp.std.ts | 1868 | `27e8706533c59cd902c728ea0c5af9605925c9f0dea13d9ea3e2324547b8753a` | 0 |
| ts/util/timestampLongUtils.std.ts | 1620 | `968cdab3b72e138c55465a4ea2d8a66f6cf61190a329723a33fd7baf1cdea9c2` | 0 |
| ts/util/toNumber.std.ts | 490 | `15c8901c7516c2dd918aade3819fdf8b4be8d0fe71ee4755ca3aa5d248ca5148` | 0 |
| ts/util/toWebStream.node.ts | 1200 | `c1bc7cda4bc374b50feb7da3123fdbbc02d0b6c003fe6e50ba34d78ca7efa62c` | 0 |
| ts/util/toggleMaximizedBrowserWindow.std.ts | 334 | `b19173366eccb0ddefa116e33c7db7238d0a265d920c4cca068ca063d20d2649` | 0 |
| ts/util/transcodeAttachment.preload.ts | 3405 | `607ff226849ccb756861cdb2ce753caa0839675b104cf3eef5bddfa2465d9722` | 0 |
| ts/util/trimPadding.node.ts | 897 | `5bfd576d0c63cb111d9ce386974fdbc12f6e4fffa8ae448f1f61270d3e6f8c68` | 0 |
| ts/util/truncateString.std.ts | 629 | `432b92c376d90bf49dd0131f799f2cadf2d588524ac248daaa70c49a54cb63ed` | 0 |
| ts/util/unencodeNumber.std.ts | 190 | `36139d0e229bb338cdabbf433cf564fdc9227ee647e99fe26817465f23455fe9` | 0 |
| ts/util/unicodeBidi.std.ts | 5720 | `385feb624b6c4df3f47b6014ebac3144e33e2acc9b3e2fca48f4e0e900e83974` | 0 |
| ts/util/unicodeSlice.std.ts | 1777 | `5f0d3e15a54e62d9a08989467008b97e38980389fa82acb4fc05d5c17e4d4845` | 0 |
| ts/util/universalExpireTimer.preload.ts | 733 | `fe2f1b9d53cc95761dbda547923c9447945340c4e0f6c1b6090d54a1f3f1b9a6` | 0 |
| ts/util/unreadReminders.std.ts | 7221 | `d19471a3bd029df87bcc0ec701f1d8497a56ac9ae0c860960b77b1cdc7f5a83e` | 0 |
| ts/util/updateBackupMediaDownloadProgress.preload.ts | 827 | `496260755fa59267057d52c79e588745de5815df7eb1690c2f41a592b14f9a8e` | 0 |
| ts/util/updateProfileKeyForAllGroups.preload.ts | 3069 | `740fe4c1c5ecf5f4103afc3199747234db6188daf65c7581ed6e6811143a3092` | 0 |
| ts/util/uploadAttachment.preload.ts | 9164 | `bcc240f44324059c5a2febcae181b1205b8aae6e24fb1183d17bd6d1906e92c9` | 0 |
| ts/util/uploads/tusProtocol.node.ts | 10365 | `753e6aa3599392ffec0fe38b20d8e595208a059f02b5c98ff17e7191d7eeb626` | 0 |
| ts/util/uploads/uploads.node.ts | 3092 | `58563768f1fe12dd473a36b4db9406de8dc238971ebb643b22e7667bddb35569` | 0 |
| ts/util/url.std.ts | 959 | `2b4a71278e5064f48fbabcb37508fb5dfb0bff0870886e3dd08e75262940541c` | 0 |
| ts/util/userLanguages.std.ts | 827 | `58c6e076f002ec267b31abcdfc86d50bddefa1bdd3bc6dd4f93384d984bf102a` | 0 |
| ts/util/utf16ToEmoji.node.ts | 397 | `9e527b8e71d902439480f09fdad0e0c138ce56bd5b50fb0c01cae68fa7e2f9d0` | 0 |
| ts/util/uuidFetchState.std.ts | 542 | `677c8eaa639b9ccb9568498368b0960857a5d626992b2538d714ae6100ebc34f` | 0 |
| ts/util/uuidToBytes.std.ts | 1877 | `b189e82d400e367d39ebaddc6d8b270b00fa324d80c230edd1318d0d1f1a823f` | 0 |
| ts/util/validateConversation.dom.ts | 1560 | `820528bc6a541bed7711790071c4764b6a05c42eea7b4f3d369703ad2d4ba48c` | 0 |
| ts/util/verifyStoryListMembers.preload.ts | 1899 | `f0c6ab7938f38b555dc6c54cc8bebd961e49a8dbea9966f7f831031bab0c99a3` | 0 |
| ts/util/version.std.ts | 1035 | `388f29e3f5eb781fed5d0871da21c19476362a47bfa9c2b4ec3a372090540cf0` | 0 |
| ts/util/viewOnceEligibility.std.ts | 495 | `d383e739fdc465956150f2b522cb46a9a45d589160fdbec9b1435879ea697684` | 0 |
| ts/util/waitBatcher.std.ts | 4957 | `8a63486caa5aac97b08bca3380997d80a68984202bb51e32311eebacfa51bad6` | 0 |
| ts/util/waitForAll.std.ts | 493 | `b3fcf3ad911db04aa828e98d91b46646f46741427ff9259b50d2d4c8991320b1` | 0 |
| ts/util/waitForOnline.dom.ts | 1142 | `d41e9804d44b006db39618d5bbdfc1de06cdaefc4b6ebc8069ade003b787f46c` | 0 |
| ts/util/waveformBuilder.std.ts | 2452 | `18f5f5ce30f69218c27c4597ea9e97b73c17a965c994a9173f64ccd0d7b4258b` | 0 |
| ts/util/webSafeBase64.std.ts | 691 | `dc705ae1edb448cac9964b3158599b03dc0c85cc29f529b8cdea645f7e019f3a` | 0 |
| ts/util/whatTypeOfConversation.dom.ts | 2700 | `e15872085136ae5e6be2642210ccb28447baddb79e5bac967c39150f50c798d3` | 0 |
| ts/util/windowsZoneIdentifier.node.ts | 1548 | `7951666f7cf7338091473b0e31a07b5b54544828cab062044c2863fce63dbc75` | 0 |
| ts/util/wrapEventEmitterOnce.node.ts | 675 | `fcb5cb4e2614c8cb2c0d1356b5019f2526363fc5034108293e10e6b57328619a` | 0 |
| ts/util/wrapWithSyncMessageSend.preload.ts | 3537 | `26c0dad46e40a7edffcea9078b21759a2f90e483620e168869e448288f633725` | 0 |
| ts/util/wrappingAdd.std.ts | 387 | `6a75f041d42a950141c39dcc1556aeeeb5865205326cc346888fcda727f0fc82` | 0 |
| ts/util/writeDraftAttachment.preload.ts | 1954 | `12514f981e4df8356523e77650a6eb5127fafd21ac00834d9b1d956c707a86a8` | 0 |
| ts/util/zkgroup.node.ts | 9324 | `064c57576943ef4332ad93d945002ba2c86784969e426e1714f29a9488cd42d5` | 0 |
| ts/utils/getAvatarPlaceholderGradient.std.ts | 360 | `336ce973d5531793f240dce5bd79aab9bb1f93839d52e3db2813186870fe18cf` | 0 |
| ts/window.d.ts | 9719 | `387cf82ee65f906909e5d7a89cedf942dab6fbf7e7397d50324a5bc20ffb18b0` | 0 |
| ts/windows/AppProvider.dom.tsx | 1982 | `e6b72da5508e4adec07e78cdda816e18e9a3e88c137f08cd48d217bb8a78973c` | 0 |
| ts/windows/about/app.dom.tsx | 1000 | `f1b66dcd1548e11e684083a8205475fbbcd2342a3a4d9d7ad5c51adff8df92f3` | 0 |
| ts/windows/about/preload.preload.ts | 707 | `167a14a9b3de3710f90df963d3a61dd5af9c9462639e5343601fd3209a8f7d5e` | 0 |
| ts/windows/applyTheme.dom.ts | 1222 | `1d12bc83c5ab4b6f56194c4be68006429cb35ee58deaa0eb937dd30f3d9bf546` | 0 |
| ts/windows/calldiagnostic/app.dom.tsx | 1245 | `19c5aa4140deb715ebfb0dff71a3723f99b73a285f8059bd8a99ddbdc5b6bd44` | 0 |
| ts/windows/calldiagnostic/preload.preload.ts | 997 | `a26243e05c0e25f116001ad4aad41ee8b3c6ce9d59cd058e9f940c78561e360e` | 0 |
| ts/windows/clipboard.preload.ts | 660 | `43488fd4315fff7d273674f3213eeddffd8de72ad6293bf45933654c19f8dbb3` | 0 |
| ts/windows/context.preload.ts | 3959 | `00e059088f3908098bd477c19826c6e1182649cfcf1dce5430a8d86031a5db2e` | 0 |
| ts/windows/debuglog/app.dom.tsx | 1054 | `85cb4e4b7e02891d45328603a248221488d40e669d52b25e5512b9d3ac30f5a7` | 0 |
| ts/windows/debuglog/preload.preload.ts | 954 | `e96a0af3178f9cedbad596e9a38e7719ac9b440c59517df51edb9630a7b4ff79` | 0 |
| ts/windows/loading/preload.preload.ts | 267 | `28b07412a5afc9cbd94154ea672a61594294679d709d709aaeab9705e7fdcc9f` | 0 |
| ts/windows/loading/start.dom.ts | 264 | `4676bf9722f3df5b21b68a4f950cc084adcddf743c46cfb9890a4b1742fda56e` | 0 |
| ts/windows/main/attachments.preload.ts | 8203 | `60f6eba876c485373e0658872da3efbeca114131808354c5c4089cc1753542f3` | 0 |
| ts/windows/main/phase1-ipc.preload.ts | 17902 | `f0ce8e900f1807548e6065a43b2f7719f67303aab29ed8902030be570356cd47` | 0 |
| ts/windows/main/phase2-dependencies.preload.ts | 1557 | `acda771445ca842e7575d174bb0c56180255a3d4a4541df935fef7f25407f658` | 0 |
| ts/windows/main/phase3-post-signal.preload.ts | 304 | `057d086d71e48b6de6a10bfb12887f6926e098f3d9f3af0e95ffe8d5052e95d5` | 0 |
| ts/windows/main/phase4-test.preload.ts | 768 | `c5342f3a9ca7470e52480cbe94ed0ceede1f85998b0a5f09470fc11183c6c5fa` | 0 |
| ts/windows/main/preload.preload.ts | 569 | `ca272cc960d9f80cfada35e257effa811d8e8a60ff4185a821a49d0074a790d7` | 0 |
| ts/windows/main/preload_test.preload.ts | 4798 | `1a19a28eb6043e838e35b6ae3c81a47000af089a2a732cad04928236dcfaccd6` | 0 |
| ts/windows/main/start.preload.ts | 6248 | `3ea200fe8b4ab44f69965311ba673f48832ef195c9fe0a2a3aeec7f8bf7e2818` | 0 |
| ts/windows/main/tsx.preload.js | 170 | `d0561d36d1658aa11c6a989bb8a2528928ddd29cc29cfdb79393a96dc09c740d` | 0 |
| ts/windows/minimalContext.preload.ts | 2982 | `7127f9a7a389b53825fd40caace02c33db20d654304a7cdfce66370853227f62` | 0 |
| ts/windows/pdf/app.dom.tsx | 989 | `59efcfc11714b5656fd39a88c475fc3d523476b07d9234433e5ea71acbd73ee1` | 0 |
| ts/windows/pdf/preload.preload.ts | 498 | `7996072a8fc77dd56d22f4833f1460f0d74a9b6a825df27a87a0e5d1920b1678` | 0 |
| ts/windows/pdf/types.std.ts | 448 | `284284eec48671afdde1e767891c6984f670a29103179d3bf298e1938a530d9f` | 0 |
| ts/windows/permissions/app.dom.tsx | 1220 | `3bd8c28499217e511233117720b621482cfb1aa81fc9cbb8711eec881a08ed20` | 0 |
| ts/windows/permissions/preload.preload.ts | 1147 | `47b2fb086b194723314f28d773018bbb9c600842ddfdb130422421aa1a5de570` | 0 |
| ts/windows/preload.preload.ts | 369 | `6334fd80f8b52718428aa644a17765a5db8cf60721630388770b6c4abcd043c8` | 0 |
| ts/windows/sandboxedInit.dom.ts | 183 | `95df6143c97d8e384f73b1789c5c49a71554c28ab7218d7b561bb31c6317c34a` | 0 |
| ts/windows/screenShare/app.dom.tsx | 1686 | `ee9f2aceb1e8de33921cfcb65a500d5182a43ccba1a8521826374003b8a0cccb` | 0 |
| ts/windows/screenShare/preload.preload.ts | 993 | `483ae8138df47670d13812aec61d92685a6030f72a40fe3229836c09b0be3eb7` | 0 |
| ts/windows/sticker-creator/preload.preload.ts | 1058 | `2cde5030ffd8e14594b8a2b98339d21f071ff27a22e565f71e0bc00ea5f985c7` | 0 |
| ts/workers/heicConverterMain.main.ts | 1389 | `a676dc1b6133392d8f1927f7325facfbef2441799108b554dd348fd6e52a6da8` | 0 |
| ts/workers/heicConverterWorker.node.ts | 919 | `d41ff48f8ad49fd222cf0a9e104709205212a99bbca13e0e67c57728fb21dbef` | 0 |
| ts/workers/mp3Encoder.std.ts | 3492 | `913735197962f582e3b9deca9aab2caec52a6634a65b65934c93f5959523f7c2` | 0 |
