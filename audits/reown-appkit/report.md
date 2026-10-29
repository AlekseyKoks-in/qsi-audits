# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** reown-appkit @ 8f9f39f1dfe0 · Reown (ex-WalletConnect) — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-28 18:40 UTC |
| Версия отчёта | 1 |
| Запуск аудита | dd8e60cb-c366-4665-b04b-b118a24f1860 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Web3-проект |
| SHA-256 содержимого | `9a4a12ceaaf420315869a8bf23c8b27c9c28ae606706d313eac55d1ed8f78f46` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **9**
- Высокая: **33**
- Средняя: **54**
- Низкая: **5**
- Информационная: **2**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 99
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 2
- Рекомендация по улучшению: 1
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 5, y = 5, z = 12 → запас минимален. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/reown-com/appkit> @ `8f9f39f1dfe0a21bb619dd9a33b6d7500523298b` — ссылки в доказательствах открывают строки на этом коммите.

1249 файлов, всего 6080944 байт, редактирований: 3; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 1215 | .size-limit.js: 59 lines scanned with 16 rule patterns and 122 registry patterns; apps/browser-extension/src/App.tsx: 25 lines scanned with 16 rule patterns and 122 registry patterns; apps/browser-extension/src/background.ts: 26 lines scanned with 16 rule patterns and 122 registry patterns |
| dependencies | проверено | 34 | apps/browser-extension/package.json: 62 dependencies parsed (59 pinned); apps/gallery/package.json: 13 dependencies parsed (10 pinned); apps/laboratory/package.json: 69 dependencies parsed (49 pinned) |
| secrets | проверено | 2 | packages/common/src/utils/SafeLocalStorage.ts: 2 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); packages/scaffold-ui/src/views/w3m-swap-select-token-view/index.ts: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| osv_advisories | проверено | 1 | 1000 pinned packages queried at OSV.dev; 30 affected (8 of them only in development or build dependencies) |
| osv_advisories | Недостаточность данных | 3 | npm/axios@1.12.2: 32 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest; npm/next@15.5.9: 32 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest; npm/next@15.3.8: 33 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- osv_advisories — Недостаточность данных: npm/axios@1.12.2: 32 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories — Недостаточность данных: npm/next@15.5.9: 32 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories — Недостаточность данных: npm/next@15.3.8: 33 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest

## 5. Краткое описание архитектуры

Static review of the source tree reown-appkit at 8f9f39f1dfe0a21bb619dd9a33b6d7500523298b. 1249 files analysed; of 2930 files, 1405 are test, fuzzing, benchmark or example code and were left out, 276 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **0** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 24.2%

## 7. Подробное описание находок

### QSI-2026-05990 — storybook 9.0.15 затронут GHSA-f2ph-cmg5-wxc8 (CVE-2026-114125)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/storybook@9.0.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 54.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-f2ph-cmg5-wxc8 (CVE-2026-114125) для пакета npm storybook версии 9.0.15: Storybook: Missing origin validation in Storybook preview allows code injection from malicious websites. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-f2ph-cmg5-wxc8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-f2ph-cmg5-wxc8](https://osv.dev/vulnerability/GHSA-f2ph-cmg5-wxc8) · manifest · SHA-256 23424603775b4b99ec5eac9aef718370171c6fe96038aa99427baf6847ad5eae_

```
{"id": "GHSA-f2ph-cmg5-wxc8", "aliases": ["CVE-2026-114125"], "modified": "2026-10-21T17:35:19.889160714Z", "summary": "Storybook: Missing origin validation in Storybook preview allows code injection from malicious websites", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.6.2, 11.0.0-alpha.6, 8.6.19, 9.1.21).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06013 — next 15.5.9 затронут GHSA-2464-fhr4-w9xw

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 54.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-2464-fhr4-w9xw для пакета npm next версии 15.5.9: Next.js: Unauthenticated Remote Code Execution in Image Optimization API when SVG files are used. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2464-fhr4-w9xw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2464-fhr4-w9xw](https://osv.dev/vulnerability/GHSA-2464-fhr4-w9xw) · manifest · SHA-256 f8ec9ad1e0512ba160d6c05735e4fd47f01a2fadcc100fec86152cd4150abc2b_

```
{"id": "GHSA-2464-fhr4-w9xw", "aliases": [], "modified": "2026-10-22T16:00:09.125335909Z", "summary": "Next.js: Unauthenticated Remote Code Execution in Image Optimization API when SVG files are used", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.28, 16.4.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06016 — next 15.5.9 затронут GHSA-2xp9-vwfh-vxw4

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 54.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-2xp9-vwfh-vxw4 для пакета npm next версии 15.5.9: Next.js: Unauthenticated Remote Code Execution in Image Optimization API when AVIF files are used. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2xp9-vwfh-vxw4
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2xp9-vwfh-vxw4](https://osv.dev/vulnerability/GHSA-2xp9-vwfh-vxw4) · manifest · SHA-256 8af173b20503114a58de0c83b691233a93ecc133ed13369038ae939cacf0da13_

```
{"id": "GHSA-2xp9-vwfh-vxw4", "aliases": [], "modified": "2026-09-08T21:30:04.767189946Z", "summary": "Next.js: Unauthenticated Remote Code Execution in Image Optimization API when AVIF files are used", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.24, 16.3.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06034 — next-auth 5.0.0-beta.29 затронут GHSA-7rqj-j65f-68wh (CVE-2026-73420)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next-auth@5.0.0-beta.29`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 54.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7rqj-j65f-68wh (CVE-2026-73420) для пакета npm next-auth версии 5.0.0-beta.29: Auth.js: Email normalizer validates the address before Unicode normalization, allowing a homoglyph @ bypass. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7rqj-j65f-68wh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7rqj-j65f-68wh](https://osv.dev/vulnerability/GHSA-7rqj-j65f-68wh) · manifest · SHA-256 decf822bc1f082557a902bb38a2c1fcacd8ff560db311907d310455ee4d15b01_

```
{"id": "GHSA-7rqj-j65f-68wh", "aliases": ["CVE-2026-73420"], "modified": "2026-09-10T03:50:51.566945120Z", "summary": "Auth.js: Email normalizer validates the address before Unicode normalization, allowing a homoglyph @ bypass", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.24.15, 5.0.0-beta.32).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06035 — next-auth 5.0.0-beta.29 затронут GHSA-8fpg-xm3f-6cx3 (CVE-2026-73421)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next-auth@5.0.0-beta.29`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 54.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-8fpg-xm3f-6cx3 (CVE-2026-73421) для пакета npm next-auth версии 5.0.0-beta.29: Auth.js: Configuration errors can cause existence-based auth checks to fail open (auth object populated with an error). Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8fpg-xm3f-6cx3
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8fpg-xm3f-6cx3](https://osv.dev/vulnerability/GHSA-8fpg-xm3f-6cx3) · manifest · SHA-256 57720c18f5f086c5e794e56ab9909312c36927448472b410eb0c4b18a0705eaa_

```
{"id": "GHSA-8fpg-xm3f-6cx3", "aliases": ["CVE-2026-73421"], "modified": "2026-08-12T20:56:01.891204Z", "summary": "Auth.js: Configuration errors can cause existence-based auth checks to fail open (auth object populated with an error)", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (5.0.0-beta.32).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06040 — next 15.3.8 затронут GHSA-2464-fhr4-w9xw

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 54.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-2464-fhr4-w9xw для пакета npm next версии 15.3.8: Next.js: Unauthenticated Remote Code Execution in Image Optimization API when SVG files are used. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2464-fhr4-w9xw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2464-fhr4-w9xw](https://osv.dev/vulnerability/GHSA-2464-fhr4-w9xw) · manifest · SHA-256 f8ec9ad1e0512ba160d6c05735e4fd47f01a2fadcc100fec86152cd4150abc2b_

```
{"id": "GHSA-2464-fhr4-w9xw", "aliases": [], "modified": "2026-10-22T16:00:09.125335909Z", "summary": "Next.js: Unauthenticated Remote Code Execution in Image Optimization API when SVG files are used", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.28, 16.4.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06043 — next 15.3.8 затронут GHSA-2xp9-vwfh-vxw4

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 54.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-2xp9-vwfh-vxw4 для пакета npm next версии 15.3.8: Next.js: Unauthenticated Remote Code Execution in Image Optimization API when AVIF files are used. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2xp9-vwfh-vxw4
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2xp9-vwfh-vxw4](https://osv.dev/vulnerability/GHSA-2xp9-vwfh-vxw4) · manifest · SHA-256 8af173b20503114a58de0c83b691233a93ecc133ed13369038ae939cacf0da13_

```
{"id": "GHSA-2xp9-vwfh-vxw4", "aliases": [], "modified": "2026-09-08T21:30:04.767189946Z", "summary": "Next.js: Unauthenticated Remote Code Execution in Image Optimization API when AVIF files are used", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.24, 16.3.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06071 — @auth/core 0.40.0 затронут GHSA-7rqj-j65f-68wh (CVE-2026-73420)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@auth/core@0.40.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 40.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7rqj-j65f-68wh (CVE-2026-73420) для пакета npm @auth/core версии 0.40.0: Auth.js: Email normalizer validates the address before Unicode normalization, allowing a homoglyph @ bypass. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7rqj-j65f-68wh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7rqj-j65f-68wh](https://osv.dev/vulnerability/GHSA-7rqj-j65f-68wh) · manifest · SHA-256 540eef679439b9917540dd3e978abc59e5b92dab34b8dc186d7f35c1759a6234_

```
{"id": "GHSA-7rqj-j65f-68wh", "aliases": ["CVE-2026-73420"], "modified": "2026-09-10T03:50:51.566945120Z", "summary": "Auth.js: Email normalizer validates the address before Unicode normalization, allowing a homoglyph @ bypass", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.41.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06076 — @nuxt/devtools 2.7.0 затронут GHSA-279x-mwfv-vcqv (CVE-2026-71319)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@nuxt/devtools@2.7.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 40.5 / 100
- CVSS v3.1: 9.6 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-279x-mwfv-vcqv (CVE-2026-71319) для пакета npm @nuxt/devtools версии 2.7.0: Unauthenticated Nuxt DevTools RPC allows arbitrary command execution on the developer's host. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-279x-mwfv-vcqv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-279x-mwfv-vcqv](https://osv.dev/vulnerability/GHSA-279x-mwfv-vcqv) · manifest · SHA-256 e7484d3a0c7cf5fefc186bdf944516c04e8d3caa2a02d87a4a93d899dd63fb2a_

```
{"id": "GHSA-279x-mwfv-vcqv", "aliases": ["CVE-2026-71319"], "modified": "2026-08-20T05:15:07.135772644Z", "summary": "Unauthenticated Nuxt DevTools RPC allows arbitrary command execution on the developer's host", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.3.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05986 — uuid 10.0.0 затронут GHSA-w5hq-g745-h8pq (CVE-2026-41907, CVE-2026-41988)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/uuid@10.0.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-w5hq-g745-h8pq (CVE-2026-41907, CVE-2026-41988) для пакета npm uuid версии 10.0.0: uuid: Missing buffer bounds check in v3/v5/v6 when buf is provided. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-05989 — storybook 9.0.15 затронут GHSA-8452-54wp-rmv6 (CVE-2025-68429)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/storybook@9.0.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L`)

OSV.dev сообщает GHSA-8452-54wp-rmv6 (CVE-2025-68429) для пакета npm storybook версии 9.0.15: Storybook manager bundle may expose environment variables during build. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8452-54wp-rmv6
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8452-54wp-rmv6](https://osv.dev/vulnerability/GHSA-8452-54wp-rmv6) · manifest · SHA-256 b856e33d3dfcda863c991a1d39b71c7b393409da1b1b9f3eff8cf4a5c1141519_

```
{"id": "GHSA-8452-54wp-rmv6", "aliases": ["CVE-2025-68429"], "modified": "2026-09-10T03:50:31.796824882Z", "summary": "Storybook manager bundle may expose environment variables during build", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.1.10, 7.6.21, 8.6.15, 9.1.17).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05991 — storybook 9.0.15 затронут GHSA-mjf5-7g4m-gx5w (CVE-2026-27148)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/storybook@9.0.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-mjf5-7g4m-gx5w (CVE-2026-27148) для пакета npm storybook версии 9.0.15: Storybook Dev Server is Vulnerable to WebSocket Hijacking. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mjf5-7g4m-gx5w
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mjf5-7g4m-gx5w](https://osv.dev/vulnerability/GHSA-mjf5-7g4m-gx5w) · manifest · SHA-256 6c00226c5c17c8efd8630daabd32153d9753e4ac6ca82b09878bab6133e8a39d_

```
{"id": "GHSA-mjf5-7g4m-gx5w", "aliases": ["CVE-2026-27148"], "modified": "2026-02-26T15:32:56.650508Z", "summary": "Storybook Dev Server is Vulnerable to WebSocket Hijacking", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.2.10, 8.6.17, 9.1.19).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05992 — storybook 9.0.15 затронут GHSA-px85-f4q5-jh77 (CVE-2026-114126)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/storybook@9.0.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-px85-f4q5-jh77 (CVE-2026-114126) для пакета npm storybook версии 9.0.15: Storybook dev server vulnerable to code injection from the local network. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-px85-f4q5-jh77
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-px85-f4q5-jh77](https://osv.dev/vulnerability/GHSA-px85-f4q5-jh77) · manifest · SHA-256 237f78c36e49fe91632ae7e1ac842f2fe38211f5d9435dd424844db2b07c48d1_

```
{"id": "GHSA-px85-f4q5-jh77", "aliases": ["CVE-2026-114126"], "modified": "2026-10-22T16:45:03.723842082Z", "summary": "Storybook dev server vulnerable to code injection from the local network", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.6.2, 11.0.0-alpha.6, 8.6.19, 9.1.21).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05993 — axios 1.12.2 затронут GHSA-35jp-ww65-95wh (CVE-2026-44494)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 8.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-35jp-ww65-95wh (CVE-2026-44494) для пакета npm axios версии 1.12.2: axios Vulnerable to Full Man-in-the-Middle via Prototype Pollution Gadget in `config.proxy`. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-35jp-ww65-95wh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-35jp-ww65-95wh](https://osv.dev/vulnerability/GHSA-35jp-ww65-95wh) · manifest · SHA-256 783ae382b2562448d5ce4a76ac95b9e0102d525fe591ccc69aec2d39d480ac80_

```
{"id": "GHSA-35jp-ww65-95wh", "aliases": ["CVE-2026-44494"], "modified": "2026-09-10T03:51:04.268287831Z", "summary": "axios Vulnerable to Full Man-in-the-Middle via Prototype Pollution Gadget in `config.proxy`", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:H/I:H/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05994 — axios 1.12.2 затронут GHSA-3g43-6gmg-66jw (CVE-2026-44495)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.0 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L`)

OSV.dev сообщает GHSA-3g43-6gmg-66jw (CVE-2026-44495) для пакета npm axios версии 1.12.2: axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3g43-6gmg-66jw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3g43-6gmg-66jw](https://osv.dev/vulnerability/GHSA-3g43-6gmg-66jw) · manifest · SHA-256 b481f03f11ed32ac5f779905e6af4e895b1bd3ca2a39c888b0d7cb1df1933931_

```
{"id": "GHSA-3g43-6gmg-66jw", "aliases": ["CVE-2026-44495"], "modified": "2026-09-10T03:51:04.440180855Z", "summary": "axios Vulnerable to Credential Theft and Response Hijacking via Prototype Pollution Gadget in Config Merge", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05998 — axios 1.12.2 затронут GHSA-43fc-jf86-j433 (CVE-2026-25639)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-43fc-jf86-j433 (CVE-2026-25639) для пакета npm axios версии 1.12.2: Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-43fc-jf86-j433
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-43fc-jf86-j433](https://osv.dev/vulnerability/GHSA-43fc-jf86-j433) · manifest · SHA-256 c27bf845de3a3c8d48f188cb13846c1e6d52900bd87b07d9d53ed80531253b74_

```
{"id": "GHSA-43fc-jf86-j433", "aliases": ["CVE-2026-25639"], "modified": "2026-09-10T03:50:34.100599628Z", "summary": "Axios is Vulnerable to Denial of Service via __proto__ Key in mergeConfig", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.30.3, 1.13.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06002 — axios 1.12.2 затронут GHSA-62hf-57xw-28j9 (CVE-2026-42039)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-62hf-57xw-28j9 (CVE-2026-42039) для пакета npm axios версии 1.12.2: Axios: unbounded recursion in toFormData causes DoS via deeply nested request data. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-62hf-57xw-28j9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-62hf-57xw-28j9](https://osv.dev/vulnerability/GHSA-62hf-57xw-28j9) · manifest · SHA-256 20145b1854d25b632657e6b51fe8b7f4fc13b9c4401040a9f57b13e0129d6d1c_

```
{"id": "GHSA-62hf-57xw-28j9", "aliases": ["CVE-2026-42039"], "modified": "2026-09-10T03:50:45.703789635Z", "summary": "Axios: unbounded recursion in toFormData causes DoS via deeply nested request data", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06003 — axios 1.12.2 затронут GHSA-6chq-wfr3-2hj9 (CVE-2026-42035)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.4 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-6chq-wfr3-2hj9 (CVE-2026-42035) для пакета npm axios версии 1.12.2: Axios: Header Injection via Prototype Pollution. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6chq-wfr3-2hj9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-6chq-wfr3-2hj9](https://osv.dev/vulnerability/GHSA-6chq-wfr3-2hj9) · manifest · SHA-256 65a099ebde93e36a9fd15b1bbf5db5a3d6716af146a0a9bbf3e516cfa77bf8f7_

```
{"id": "GHSA-6chq-wfr3-2hj9", "aliases": ["CVE-2026-42035"], "modified": "2026-09-10T03:51:04.772235088Z", "summary": "Axios: Header Injection via Prototype Pollution", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06004 — axios 1.12.2 затронут GHSA-777c-7fjr-54vf (CVE-2026-44488)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-777c-7fjr-54vf (CVE-2026-44488) для пакета npm axios версии 1.12.2: Allocation of Resources Without Limits or Throttling in Axios. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-777c-7fjr-54vf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-777c-7fjr-54vf](https://osv.dev/vulnerability/GHSA-777c-7fjr-54vf) · manifest · SHA-256 2d0a2e358c8f39856a95ad796f12158f06d1b60df1aca37f8f85a8dfeeb41bd4_

```
{"id": "GHSA-777c-7fjr-54vf", "aliases": ["CVE-2026-44488"], "modified": "2026-09-10T03:50:48.738717543Z", "summary": "Allocation of Resources Without Limits or Throttling in Axios", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06009 — axios 1.12.2 затронут GHSA-hfxv-24rg-xrqf (CVE-2026-44496)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496) для пакета npm axios версии 1.12.2: Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hfxv-24rg-xrqf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-hfxv-24rg-xrqf](https://osv.dev/vulnerability/GHSA-hfxv-24rg-xrqf) · manifest · SHA-256 6b4b4c75f0d4abad76624e9b591076339a0af2e44f00e098ea5c8c2a7134fcee_

```
{"id": "GHSA-hfxv-24rg-xrqf", "aliases": ["CVE-2026-44496"], "modified": "2026-09-10T03:50:49.732285826Z", "summary": "Axios: Regular Expression Denial of Service (ReDoS) via Cookie Name Injection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06010 — axios 1.12.2 затронут GHSA-j5f8-grm9-p9fc (CVE-2026-44486)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486) для пакета npm axios версии 1.12.2: Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j5f8-grm9-p9fc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j5f8-grm9-p9fc](https://osv.dev/vulnerability/GHSA-j5f8-grm9-p9fc) · manifest · SHA-256 d0b3bd3df0758f091aa317e68476a04a0e006d5dcaace5ff739bf0a87530834b_

```
{"id": "GHSA-j5f8-grm9-p9fc", "aliases": ["CVE-2026-44486"], "modified": "2026-09-10T03:50:50.017253448Z", "summary": "Axios: Proxy-Authorization header leaks to redirect target when proxy is re-evaluated to direct connection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06014 — next 15.5.9 затронут GHSA-267c-6grr-h53f (CVE-2026-44575)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-267c-6grr-h53f (CVE-2026-44575) для пакета npm next версии 15.5.9: Next.js has a Middleware / Proxy bypass in App Router applications via segment-prefetch routes. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-267c-6grr-h53f
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-267c-6grr-h53f](https://osv.dev/vulnerability/GHSA-267c-6grr-h53f) · manifest · SHA-256 37676ba1d5f94607e4e8d171f32a2c24fa080cf3e3eb0c7e86c54aaf5d335e4a_

```
{"id": "GHSA-267c-6grr-h53f", "aliases": ["CVE-2026-44575"], "modified": "2026-09-10T03:51:03.970900692Z", "summary": "Next.js has a Middleware / Proxy bypass in App Router applications via segment-prefetch routes", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06015 — next 15.5.9 затронут GHSA-26hh-7cqf-hhc6 (CVE-2026-45109)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-26hh-7cqf-hhc6 (CVE-2026-45109) для пакета npm next версии 15.5.9: Next.js has a Middleware / Proxy bypass in App Router applications via segment-prefetch routes - Incomplete Fix Follow-Up. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-26hh-7cqf-hhc6
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-26hh-7cqf-hhc6](https://osv.dev/vulnerability/GHSA-26hh-7cqf-hhc6) · manifest · SHA-256 c37d452be32c7d20c9756317568e8853b6cc15b73db8df5d05c6ac1f3f7bb9e2_

```
{"id": "GHSA-26hh-7cqf-hhc6", "aliases": ["CVE-2026-45109"], "modified": "2026-09-10T03:50:45.324330779Z", "summary": "Next.js has a Middleware / Proxy bypass in App Router applications via segment-prefetch routes - Incomplete Fix Follow-Up", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.18, 16.2.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06017 — next 15.5.9 затронут GHSA-36qx-fr4f-26g5 (CVE-2026-44573)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-36qx-fr4f-26g5 (CVE-2026-44573) для пакета npm next версии 15.5.9: Next.js has a Middleware / Proxy bypass in Pages Router applications using i18n. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-36qx-fr4f-26g5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-36qx-fr4f-26g5](https://osv.dev/vulnerability/GHSA-36qx-fr4f-26g5) · manifest · SHA-256 2f6556ebf7a6e831522ad882f265c3fad8c9c49ab2ff9ed07e427ef79851925b_

```
{"id": "GHSA-36qx-fr4f-26g5", "aliases": ["CVE-2026-44573"], "modified": "2026-09-10T03:51:04.325298044Z", "summary": "Next.js has a Middleware / Proxy bypass in Pages Router applications using i18n", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06021 — next 15.5.9 затронут GHSA-492v-c6pp-mqqv (CVE-2026-44574)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 8.1 (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-492v-c6pp-mqqv (CVE-2026-44574) для пакета npm next версии 15.5.9: Next.js has a Middleware / Proxy bypass through dynamic route parameter injection. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-492v-c6pp-mqqv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-492v-c6pp-mqqv](https://osv.dev/vulnerability/GHSA-492v-c6pp-mqqv) · manifest · SHA-256 69b53561feb125411569a76037d64bb290f66c1dd7099bc8f097bc74b652f7da_

```
{"id": "GHSA-492v-c6pp-mqqv", "aliases": ["CVE-2026-44574"], "modified": "2026-09-10T03:51:04.588942784Z", "summary": "Next.js has a Middleware / Proxy bypass through dynamic route parameter injection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06025 — next 15.5.9 затронут GHSA-89xv-2m56-2m9x (CVE-2026-64649)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-89xv-2m56-2m9x (CVE-2026-64649) для пакета npm next версии 15.5.9: Next.js: Server-Side Request Forgery in Server Actions on custom servers. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-89xv-2m56-2m9x
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-89xv-2m56-2m9x](https://osv.dev/vulnerability/GHSA-89xv-2m56-2m9x) · manifest · SHA-256 fa3fa166cbe110200cb785c14958b009fc194c025ff2db03d54365b24b179ed5_

```
{"id": "GHSA-89xv-2m56-2m9x", "aliases": ["CVE-2026-64649"], "modified": "2026-09-10T03:50:51.547474623Z", "summary": "Next.js: Server-Side Request Forgery in Server Actions on custom servers", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.21, 16.2.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06026 — next 15.5.9 затронут GHSA-8h8q-6873-q5fj

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-8h8q-6873-q5fj для пакета npm next версии 15.5.9: Next.js Vulnerable to Denial of Service with Server Components. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8h8q-6873-q5fj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8h8q-6873-q5fj](https://osv.dev/vulnerability/GHSA-8h8q-6873-q5fj) · manifest · SHA-256 adbb9c7a5ff197004af1328127763df622d4bf6b606b16ba0283852b0cecac88_

```
{"id": "GHSA-8h8q-6873-q5fj", "aliases": [], "modified": "2026-09-10T03:51:04.979274056Z", "summary": "Next.js Vulnerable to Denial of Service with Server Components", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06029 — next 15.5.9 затронут GHSA-c4j6-fc7j-m34r (CVE-2026-44578)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 8.6 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-c4j6-fc7j-m34r (CVE-2026-44578) для пакета npm next версии 15.5.9: Next.js vulnerable to server-side request forgery in applications using WebSocket upgrades. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-c4j6-fc7j-m34r
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-c4j6-fc7j-m34r](https://osv.dev/vulnerability/GHSA-c4j6-fc7j-m34r) · manifest · SHA-256 8618d02186542e6ed87eafff5fb1d53114740df1bb535845e1d35265e76d0edf_

```
{"id": "GHSA-c4j6-fc7j-m34r", "aliases": ["CVE-2026-44578"], "modified": "2026-09-10T03:50:46.499274814Z", "summary": "Next.js vulnerable to server-side request forgery in applications using WebSocket upgrades", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06037 — next-auth 5.0.0-beta.29 затронут GHSA-xmf8-cvqr-rfgj (CVE-2026-73418)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next-auth@5.0.0-beta.29`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-xmf8-cvqr-rfgj (CVE-2026-73418) для пакета npm next-auth версии 5.0.0-beta.29: Auth.js: getToken() throws an uncaught exception on malformed Bearer authorization headers. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xmf8-cvqr-rfgj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xmf8-cvqr-rfgj](https://osv.dev/vulnerability/GHSA-xmf8-cvqr-rfgj) · manifest · SHA-256 463533fbffa64d1805c6ee4e464184099671b00f622520bf5a0439ad3f258aba_

```
{"id": "GHSA-xmf8-cvqr-rfgj", "aliases": ["CVE-2026-73418"], "modified": "2026-09-10T03:51:12.549867672Z", "summary": "Auth.js: getToken() throws an uncaught exception on malformed Bearer authorization headers", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.24.15, 5.0.0-beta.32).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06038 — @opennextjs/cloudflare 1.5.3 затронут GHSA-2vc4-c4r6-p6v6 (CVE-2026-100409)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/@opennextjs/cloudflare@1.5.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-2vc4-c4r6-p6v6 (CVE-2026-100409) для пакета npm @opennextjs/cloudflare версии 1.5.3: OpenNext Cloudflare: Cache interception can bypass middleware protection for encoded paths. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2vc4-c4r6-p6v6
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2vc4-c4r6-p6v6](https://osv.dev/vulnerability/GHSA-2vc4-c4r6-p6v6) · manifest · SHA-256 04588159e7a178ae7c356da1292113c92fe76d0119b2c16a05194880fb426e98_

```
{"id": "GHSA-2vc4-c4r6-p6v6", "aliases": ["CVE-2026-100409"], "modified": "2026-10-15T20:30:05.349670038Z", "summary": "OpenNext Cloudflare: Cache interception can bypass middleware protection for encoded paths", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06039 — @opennextjs/cloudflare 1.5.3 затронут GHSA-c7mq-gh6q-6q7c (CVE-2025-6087, CVE-2026-3125)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/@opennextjs/cloudflare@1.5.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-c7mq-gh6q-6q7c (CVE-2025-6087, CVE-2026-3125) для пакета npm @opennextjs/cloudflare версии 1.5.3: opennextjs-cloudflare has SSRF vulnerability via /cdn-cgi/ path normalization bypass. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-c7mq-gh6q-6q7c
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-c7mq-gh6q-6q7c](https://osv.dev/vulnerability/GHSA-c7mq-gh6q-6q7c) · manifest · SHA-256 fa9e50b00e3c7b4c769559964293b0c15cedf044c3c38f64a095f8d80ebd3b1f_

```
{"id": "GHSA-c7mq-gh6q-6q7c", "aliases": ["CVE-2025-6087", "CVE-2026-3125", "GHSA-rvpw-p7vw-wj3m"], "modified": "2026-03-16T03:05:38.239106Z", "summary": "opennextjs-cloudflare has SSRF vulnerability via /cdn-cgi/ path normalization bypass", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:N/SC:H/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.17.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06041 — next 15.3.8 затронут GHSA-267c-6grr-h53f (CVE-2026-44575)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-267c-6grr-h53f (CVE-2026-44575) для пакета npm next версии 15.3.8: Next.js has a Middleware / Proxy bypass in App Router applications via segment-prefetch routes. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-267c-6grr-h53f
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-267c-6grr-h53f](https://osv.dev/vulnerability/GHSA-267c-6grr-h53f) · manifest · SHA-256 37676ba1d5f94607e4e8d171f32a2c24fa080cf3e3eb0c7e86c54aaf5d335e4a_

```
{"id": "GHSA-267c-6grr-h53f", "aliases": ["CVE-2026-44575"], "modified": "2026-09-10T03:51:03.970900692Z", "summary": "Next.js has a Middleware / Proxy bypass in App Router applications via segment-prefetch routes", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06042 — next 15.3.8 затронут GHSA-26hh-7cqf-hhc6 (CVE-2026-45109)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-26hh-7cqf-hhc6 (CVE-2026-45109) для пакета npm next версии 15.3.8: Next.js has a Middleware / Proxy bypass in App Router applications via segment-prefetch routes - Incomplete Fix Follow-Up. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-26hh-7cqf-hhc6
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-26hh-7cqf-hhc6](https://osv.dev/vulnerability/GHSA-26hh-7cqf-hhc6) · manifest · SHA-256 c37d452be32c7d20c9756317568e8853b6cc15b73db8df5d05c6ac1f3f7bb9e2_

```
{"id": "GHSA-26hh-7cqf-hhc6", "aliases": ["CVE-2026-45109"], "modified": "2026-09-10T03:50:45.324330779Z", "summary": "Next.js has a Middleware / Proxy bypass in App Router applications via segment-prefetch routes - Incomplete Fix Follow-Up", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.18, 16.2.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06044 — next 15.3.8 затронут GHSA-36qx-fr4f-26g5 (CVE-2026-44573)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-36qx-fr4f-26g5 (CVE-2026-44573) для пакета npm next версии 15.3.8: Next.js has a Middleware / Proxy bypass in Pages Router applications using i18n. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-36qx-fr4f-26g5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-36qx-fr4f-26g5](https://osv.dev/vulnerability/GHSA-36qx-fr4f-26g5) · manifest · SHA-256 2f6556ebf7a6e831522ad882f265c3fad8c9c49ab2ff9ed07e427ef79851925b_

```
{"id": "GHSA-36qx-fr4f-26g5", "aliases": ["CVE-2026-44573"], "modified": "2026-09-10T03:51:04.325298044Z", "summary": "Next.js has a Middleware / Proxy bypass in Pages Router applications using i18n", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06052 — next 15.3.8 затронут GHSA-89xv-2m56-2m9x (CVE-2026-64649)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-89xv-2m56-2m9x (CVE-2026-64649) для пакета npm next версии 15.3.8: Next.js: Server-Side Request Forgery in Server Actions on custom servers. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-89xv-2m56-2m9x
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-89xv-2m56-2m9x](https://osv.dev/vulnerability/GHSA-89xv-2m56-2m9x) · manifest · SHA-256 fa3fa166cbe110200cb785c14958b009fc194c025ff2db03d54365b24b179ed5_

```
{"id": "GHSA-89xv-2m56-2m9x", "aliases": ["CVE-2026-64649"], "modified": "2026-09-10T03:50:51.547474623Z", "summary": "Next.js: Server-Side Request Forgery in Server Actions on custom servers", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.21, 16.2.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06053 — next 15.3.8 затронут GHSA-8h8q-6873-q5fj

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-8h8q-6873-q5fj для пакета npm next версии 15.3.8: Next.js Vulnerable to Denial of Service with Server Components. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8h8q-6873-q5fj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8h8q-6873-q5fj](https://osv.dev/vulnerability/GHSA-8h8q-6873-q5fj) · manifest · SHA-256 adbb9c7a5ff197004af1328127763df622d4bf6b606b16ba0283852b0cecac88_

```
{"id": "GHSA-8h8q-6873-q5fj", "aliases": [], "modified": "2026-09-10T03:51:04.979274056Z", "summary": "Next.js Vulnerable to Denial of Service with Server Components", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06056 — next 15.3.8 затронут GHSA-c4j6-fc7j-m34r (CVE-2026-44578)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 8.6 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-c4j6-fc7j-m34r (CVE-2026-44578) для пакета npm next версии 15.3.8: Next.js vulnerable to server-side request forgery in applications using WebSocket upgrades. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-c4j6-fc7j-m34r
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-c4j6-fc7j-m34r](https://osv.dev/vulnerability/GHSA-c4j6-fc7j-m34r) · manifest · SHA-256 8618d02186542e6ed87eafff5fb1d53114740df1bb535845e1d35265e76d0edf_

```
{"id": "GHSA-c4j6-fc7j-m34r", "aliases": ["CVE-2026-44578"], "modified": "2026-09-10T03:50:46.499274814Z", "summary": "Next.js vulnerable to server-side request forgery in applications using WebSocket upgrades", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06061 — vite 5.4.20 затронут GHSA-587h-7wmj-h5pm (CVE-2026-112942)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/vite@5.4.20`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-587h-7wmj-h5pm (CVE-2026-112942) для пакета npm vite версии 5.4.20: launch-editor: `fs.existsSync()` existence check can be bypassed on Windows. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-587h-7wmj-h5pm
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-587h-7wmj-h5pm](https://osv.dev/vulnerability/GHSA-587h-7wmj-h5pm) · manifest · SHA-256 c834c0505fc275e6d70ff5927caa10644d8fbc47d8ff7c4a1b94681b7914b0cb_

```
{"id": "GHSA-587h-7wmj-h5pm", "aliases": ["CVE-2026-112942"], "modified": "2026-10-20T20:00:04.608979840Z", "summary": "launch-editor: `fs.existsSync()` existence check can be bypassed on Windows", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.4.4, 7.3.7, 8.1.6, 8.2.4, 8.3.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06069 — figlet 1.9.1 затронут GHSA-62ch-8vmq-8xm7 (CVE-2026-96780)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/figlet@1.9.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-62ch-8vmq-8xm7 (CVE-2026-96780) для пакета npm figlet версии 1.9.1: figlet is vulnerable to denial of service via unbounded loop when whitespaceBreak is used with a small width. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-62ch-8vmq-8xm7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-62ch-8vmq-8xm7](https://osv.dev/vulnerability/GHSA-62ch-8vmq-8xm7) · manifest · SHA-256 6f42f9a49e7be08e196d54f926f94fd196d56af24e2b7f6b4d943667d49d7220_

```
{"id": "GHSA-62ch-8vmq-8xm7", "aliases": ["CVE-2026-96780"], "modified": "2026-10-02T23:01:22.706221290Z", "summary": "figlet is vulnerable to denial of service via unbounded loop when whitespaceBreak is used with a small width", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.11.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06070 — zod 3.22.4 затронут GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/zod@3.22.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404) для пакета npm zod версии 3.22.4: Zod can exhaust memory while validating oversized constrained collections. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-06073 — @auth/core 0.40.0 затронут GHSA-xmf8-cvqr-rfgj (CVE-2026-73418)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@auth/core@0.40.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 36.9 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-xmf8-cvqr-rfgj (CVE-2026-73418) для пакета npm @auth/core версии 0.40.0: Auth.js: getToken() throws an uncaught exception on malformed Bearer authorization headers. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xmf8-cvqr-rfgj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xmf8-cvqr-rfgj](https://osv.dev/vulnerability/GHSA-xmf8-cvqr-rfgj) · manifest · SHA-256 00bbadeed684ae1ec71315d77c8cbd3c9951f0cd40c41563e52933a119d59f19_

```
{"id": "GHSA-xmf8-cvqr-rfgj", "aliases": ["CVE-2026-73418"], "modified": "2026-09-10T03:51:12.549867672Z", "summary": "Auth.js: getToken() throws an uncaught exception on malformed Bearer authorization headers", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.41.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06075 — @fastify/busboy 2.1.1 затронут GHSA-x8mw-p69m-v3mx (CVE-2026-19481)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@fastify/busboy@2.1.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 36.9 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-x8mw-p69m-v3mx (CVE-2026-19481) для пакета npm @fastify/busboy версии 2.1.1: @fastify/busboy vulnerable to Denial of Service via prototype-named multipart part header. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x8mw-p69m-v3mx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-x8mw-p69m-v3mx](https://osv.dev/vulnerability/GHSA-x8mw-p69m-v3mx) · manifest · SHA-256 11787bedd6a3b453009465eb81de9fa50c00a1c956fa0961a425ea767cb92ca7_

```
{"id": "GHSA-x8mw-p69m-v3mx", "aliases": ["CVE-2026-19481"], "modified": "2026-10-02T23:30:05.651087437Z", "summary": "@fastify/busboy vulnerable to Denial of Service via prototype-named multipart part header", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.2.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05995 — axios 1.12.2 затронут GHSA-3p68-rc4w-qgx5 (CVE-2025-62718)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-3p68-rc4w-qgx5 (CVE-2025-62718) для пакета npm axios версии 1.12.2: Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3p68-rc4w-qgx5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3p68-rc4w-qgx5](https://osv.dev/vulnerability/GHSA-3p68-rc4w-qgx5) · manifest · SHA-256 7150afa7c2a38fac85edc3a2e7fdd17ba3f973dcb4982f55d4260f3604428a07_

```
{"id": "GHSA-3p68-rc4w-qgx5", "aliases": ["CVE-2025-62718"], "modified": "2026-09-10T03:50:42.452672741Z", "summary": "Axios has a NO_PROXY Hostname Normalization Bypass that Leads to SSRF", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:L/SI:L/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.0, 1.15.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05996 — axios 1.12.2 затронут GHSA-3w6x-2g7m-8v23 (CVE-2026-42044)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:N`)

OSV.dev сообщает GHSA-3w6x-2g7m-8v23 (CVE-2026-42044) для пакета npm axios версии 1.12.2: Axios: Invisible JSON Response Tampering via Prototype Pollution Gadget in `parseReviver`. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3w6x-2g7m-8v23
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3w6x-2g7m-8v23](https://osv.dev/vulnerability/GHSA-3w6x-2g7m-8v23) · manifest · SHA-256 46d97b7263fe5e5223533fb98e81ec0291e267b6aed2af76118a44a32623b0f5_

```
{"id": "GHSA-3w6x-2g7m-8v23", "aliases": ["CVE-2026-42044"], "modified": "2026-09-10T03:50:45.398396828Z", "summary": "Axios: Invisible JSON Response Tampering via Prototype Pollution Gadget in `parseReviver`", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.15.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05997 — axios 1.12.2 затронут GHSA-42h9-826w-cgv3 (CVE-2026-67313)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-42h9-826w-cgv3 (CVE-2026-67313) для пакета npm axios версии 1.12.2: Axios: Excessive recursion in formDataToJSON can cause denial of service. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-42h9-826w-cgv3
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-42h9-826w-cgv3](https://osv.dev/vulnerability/GHSA-42h9-826w-cgv3) · manifest · SHA-256 a686657ae0246ed9ff23a42e52e88713e8102c70ddfbc5eee6a582f06871c8a0_

```
{"id": "GHSA-42h9-826w-cgv3", "aliases": ["CVE-2026-67313"], "modified": "2026-09-10T03:51:10.187294734Z", "summary": "Axios: Excessive recursion in formDataToJSON can cause denial of service", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05999 — axios 1.12.2 затронут GHSA-445q-vr5w-6q77 (CVE-2026-42037)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-445q-vr5w-6q77 (CVE-2026-42037) для пакета npm axios версии 1.12.2: Axios: CRLF Injection in multipart/form-data body via unsanitized blob.type in formDataToStream. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-445q-vr5w-6q77
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-445q-vr5w-6q77](https://osv.dev/vulnerability/GHSA-445q-vr5w-6q77) · manifest · SHA-256 3e796f9bf266da05d5995ab86fb00fc28f74682b92659c3257dbc55eeb132480_

```
{"id": "GHSA-445q-vr5w-6q77", "aliases": ["CVE-2026-42037"], "modified": "2026-09-10T03:50:45.396631689Z", "summary": "Axios: CRLF Injection in multipart/form-data body via unsanitized blob.type in formDataToStream", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06000 — axios 1.12.2 затронут GHSA-4hqw-qxg8-jxx2 (CVE-2026-101900)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-4hqw-qxg8-jxx2 (CVE-2026-101900) для пакета npm axios версии 1.12.2: Axios: Fetch Adapter Header Injection via Inherited FormData getHeaders. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4hqw-qxg8-jxx2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4hqw-qxg8-jxx2](https://osv.dev/vulnerability/GHSA-4hqw-qxg8-jxx2) · manifest · SHA-256 a6e58cc75f56e56a447cb5214554c3d95ff1bb006258c66a322141d128062db8_

```
{"id": "GHSA-4hqw-qxg8-jxx2", "aliases": ["CVE-2026-101900"], "modified": "2026-09-30T15:46:17.701967512Z", "summary": "Axios: Fetch Adapter Header Injection via Inherited FormData getHeaders", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:L/SI:H/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06001 — axios 1.12.2 затронут GHSA-5c9x-8gcm-mpgx (CVE-2026-42034)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-5c9x-8gcm-mpgx (CVE-2026-42034) для пакета npm axios версии 1.12.2: Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5c9x-8gcm-mpgx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-5c9x-8gcm-mpgx](https://osv.dev/vulnerability/GHSA-5c9x-8gcm-mpgx) · manifest · SHA-256 160419f7b435329e1aa01c0bb6e30c10760c12e1819b9d511a39a795c8472dbc_

```
{"id": "GHSA-5c9x-8gcm-mpgx", "aliases": ["CVE-2026-42034"], "modified": "2026-09-10T03:50:45.707956373Z", "summary": "Axios' HTTP adapter-streamed uploads bypass maxBodyLength when maxRedirects: 0", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1, 1.15.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06005 — axios 1.12.2 затронут GHSA-7q8q-rj6j-mhjq (CVE-2026-67319)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319) для пакета npm axios версии 1.12.2: Axios: Nested axios option objects can consume polluted prototype values. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7q8q-rj6j-mhjq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7q8q-rj6j-mhjq](https://osv.dev/vulnerability/GHSA-7q8q-rj6j-mhjq) · manifest · SHA-256 67a785b830c22e65a0875455b8b6724252a6154c9a18808a51df782939b55132_

```
{"id": "GHSA-7q8q-rj6j-mhjq", "aliases": ["CVE-2026-67319"], "modified": "2026-09-10T03:51:10.872027953Z", "summary": "Axios: Nested axios option objects can consume polluted prototype values", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:L/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.33.0, 1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06006 — axios 1.12.2 затронут GHSA-898c-q2cr-xwhg (CVE-2026-44490)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L`)

OSV.dev сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490) для пакета npm axios версии 1.12.2: axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-898c-q2cr-xwhg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-898c-q2cr-xwhg](https://osv.dev/vulnerability/GHSA-898c-q2cr-xwhg) · manifest · SHA-256 61a3bd342f996b7a15accd78ca6ab3011ba6d168e56084c7a2878a0afe0e4b19_

```
{"id": "GHSA-898c-q2cr-xwhg", "aliases": ["CVE-2026-44490"], "modified": "2026-09-10T03:51:04.811379218Z", "summary": "axios has DoS & Header Injection via Prototype Pollution Read-Side Gadgets in axios merge functions", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.0, 1.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06007 — axios 1.12.2 затронут GHSA-9fr6-4gfg-395g (CVE-2026-101902)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-9fr6-4gfg-395g (CVE-2026-101902) для пакета npm axios версии 1.12.2: Axios: Prototype-Pollution Gadget in the Default Instance Allows Inherited Object.prototype.method to Override HTTP Method. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9fr6-4gfg-395g
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9fr6-4gfg-395g](https://osv.dev/vulnerability/GHSA-9fr6-4gfg-395g) · manifest · SHA-256 f717c3585d8810d7820ba651ec8d84c6e6f272722b178cef9adfa66d23a49df9_

```
{"id": "GHSA-9fr6-4gfg-395g", "aliases": ["CVE-2026-101902"], "modified": "2026-09-30T15:30:03.718390401Z", "summary": "Axios: Prototype-Pollution Gadget in the Default Instance Allows Inherited Object.prototype.method to Override HTTP Method", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:H/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.34.0, 1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06008 — axios 1.12.2 затронут GHSA-fvcv-3m26-pcqx (CVE-2026-40175)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 4.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-fvcv-3m26-pcqx (CVE-2026-40175) для пакета npm axios версии 1.12.2: Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-fvcv-3m26-pcqx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-fvcv-3m26-pcqx](https://osv.dev/vulnerability/GHSA-fvcv-3m26-pcqx) · manifest · SHA-256 abca6a7b81eb08cc2395a8f39c0d6cbf79093b4dc25ba685386e68c7472a9a76_

```
{"id": "GHSA-fvcv-3m26-pcqx", "aliases": ["CVE-2026-40175"], "modified": "2026-09-10T03:50:44.273401032Z", "summary": "Axios has Unrestricted Cloud Metadata Exfiltration via Header Injection Chain", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.0, 1.15.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06011 — axios 1.12.2 затронут GHSA-j8rh-479h-cp32 (CVE-2026-101904)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-j8rh-479h-cp32 (CVE-2026-101904) для пакета npm axios версии 1.12.2: Axios: Header Injection via Inherited headers After Minimal Interceptor. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j8rh-479h-cp32
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j8rh-479h-cp32](https://osv.dev/vulnerability/GHSA-j8rh-479h-cp32) · manifest · SHA-256 f539745e6470f1ff1bc7717b0c67a98ba684979378967ec357065e5d14dd4663_

```
{"id": "GHSA-j8rh-479h-cp32", "aliases": ["CVE-2026-101904"], "modified": "2026-09-30T15:46:18.108444439Z", "summary": "Axios: Header Injection via Inherited headers After Minimal Interceptor", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:N/SC:L/SI:H/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06012 — axios 1.12.2 затронут GHSA-jqh4-m9w3-8hp9 (CVE-2026-67317)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/axios@1.12.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-jqh4-m9w3-8hp9 (CVE-2026-67317) для пакета npm axios версии 1.12.2: Axios: Fetch adapter `ReadableStream` uploads bypass `maxBodyLength`. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-jqh4-m9w3-8hp9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-jqh4-m9w3-8hp9](https://osv.dev/vulnerability/GHSA-jqh4-m9w3-8hp9) · manifest · SHA-256 16a8069bd7dea2e9f7aaf21d337a30fc172f6a6831c5212be838956bb7b5f98b_

```
{"id": "GHSA-jqh4-m9w3-8hp9", "aliases": ["CVE-2026-67317"], "modified": "2026-09-10T03:50:52.448472902Z", "summary": "Axios: Fetch adapter `ReadableStream` uploads bypass `maxBodyLength`", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.18.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06019 — next 15.5.9 затронут GHSA-3x4c-7xq6-9pq8 (CVE-2026-27980)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3x4c-7xq6-9pq8 (CVE-2026-27980) для пакета npm next версии 15.5.9: Next.js: Unbounded next/image disk cache growth can exhaust storage. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3x4c-7xq6-9pq8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3x4c-7xq6-9pq8](https://osv.dev/vulnerability/GHSA-3x4c-7xq6-9pq8) · manifest · SHA-256 7d5aab6bba46c21b1813b72e8ce87efa70f7b8b814b880f9c5c0ea963f0b9a74_

```
{"id": "GHSA-3x4c-7xq6-9pq8", "aliases": ["CVE-2026-27980"], "modified": "2026-09-10T03:50:36.950018769Z", "summary": "Next.js: Unbounded next/image disk cache growth can exhaust storage", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.14, 16.1.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06020 — next 15.5.9 затронут GHSA-4633-3j49-mh5q (CVE-2026-64647)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-4633-3j49-mh5q (CVE-2026-64647) для пакета npm next версии 15.5.9: Next.js: Cache confusion of response bodies for requests with bodies containing invalid UTF-8 byte sequences. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4633-3j49-mh5q
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4633-3j49-mh5q](https://osv.dev/vulnerability/GHSA-4633-3j49-mh5q) · manifest · SHA-256 7420b5b5742a23d83bb5acf4649fa8d0192088904eb2634f39d9d5d8cec65f4e_

```
{"id": "GHSA-4633-3j49-mh5q", "aliases": ["CVE-2026-64647"], "modified": "2026-09-10T03:50:51.390157243Z", "summary": "Next.js: Cache confusion of response bodies for requests with bodies containing invalid UTF-8 byte sequences", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.21, 16.2.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06022 — next 15.5.9 затронут GHSA-4c39-4ccg-62r3 (CVE-2026-64646)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-4c39-4ccg-62r3 (CVE-2026-64646) для пакета npm next версии 15.5.9: Next.js: Unbounded Server Action payload in Edge runtime. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4c39-4ccg-62r3
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4c39-4ccg-62r3](https://osv.dev/vulnerability/GHSA-4c39-4ccg-62r3) · manifest · SHA-256 5c9f84af8d713159459f897539d6f7b39f3e3ee2cde2a71957d649357dbe58b6_

```
{"id": "GHSA-4c39-4ccg-62r3", "aliases": ["CVE-2026-64646"], "modified": "2026-09-10T03:50:51.398762372Z", "summary": "Next.js: Unbounded Server Action payload in Edge runtime", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.21, 16.2.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06023 — next 15.5.9 затронут GHSA-4jqv-mc3x-m676 (CVE-2026-94543)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-4jqv-mc3x-m676 (CVE-2026-94543) для пакета npm next версии 15.5.9: Next.js has cache poisoning of SSG and ISR pages in self-hosted applications. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4jqv-mc3x-m676
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4jqv-mc3x-m676](https://osv.dev/vulnerability/GHSA-4jqv-mc3x-m676) · manifest · SHA-256 3da12d6118b9c8f9be68f2d3d34fe127c12486b41bb82358a75ad1bc5a50e4e4_

```
{"id": "GHSA-4jqv-mc3x-m676", "aliases": ["CVE-2026-94543"], "modified": "2026-10-07T20:45:06.342983181Z", "summary": "Next.js has cache poisoning of SSG and ISR pages in self-hosted applications", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.27, 16.3.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06024 — next 15.5.9 затронут GHSA-68g3-v927-f742 (CVE-2026-64648)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-68g3-v927-f742 (CVE-2026-64648) для пакета npm next версии 15.5.9: Next.js: Cache confusion of response bodies for requests with bodies. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-68g3-v927-f742
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-68g3-v927-f742](https://osv.dev/vulnerability/GHSA-68g3-v927-f742) · manifest · SHA-256 67bad25fdf4036bd6994b55f566c71a3b5c4d252652cb2524757452d06e798ac_

```
{"id": "GHSA-68g3-v927-f742", "aliases": ["CVE-2026-64648"], "modified": "2026-09-10T03:51:10.587986551Z", "summary": "Next.js: Cache confusion of response bodies for requests with bodies", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.21, 16.2.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06027 — next 15.5.9 затронут GHSA-955p-x3mx-jcvp (CVE-2026-64643)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-955p-x3mx-jcvp (CVE-2026-64643) для пакета npm next версии 15.5.9: Next.js: Unauthenticated disclosure of internal Server Function endpoints. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-955p-x3mx-jcvp
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-955p-x3mx-jcvp](https://osv.dev/vulnerability/GHSA-955p-x3mx-jcvp) · manifest · SHA-256 3d9a703112e42338524054a7b9d5a30eddc8bd4bda25a239cab3ed64f0a6733d_

```
{"id": "GHSA-955p-x3mx-jcvp", "aliases": ["CVE-2026-64643"], "modified": "2026-09-10T03:51:11.198992864Z", "summary": "Next.js: Unauthenticated disclosure of internal Server Function endpoints", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.21, 16.2.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06028 — next 15.5.9 затронут GHSA-9g9p-9gw9-jx7f (CVE-2025-59471)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-9g9p-9gw9-jx7f (CVE-2025-59471) для пакета npm next версии 15.5.9: Next.js self-hosted applications vulnerable to DoS via Image Optimizer remotePatterns configuration. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9g9p-9gw9-jx7f
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9g9p-9gw9-jx7f](https://osv.dev/vulnerability/GHSA-9g9p-9gw9-jx7f) · manifest · SHA-256 8f8a980faea6084564436720362b9d0b40a40361f136c8799cab60074be16057_

```
{"id": "GHSA-9g9p-9gw9-jx7f", "aliases": ["CVE-2025-59471"], "modified": "2026-09-10T03:50:59.013924260Z", "summary": "Next.js self-hosted applications vulnerable to DoS via Image Optimizer remotePatterns configuration", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.10, 16.1.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06030 — next 15.5.9 затронут GHSA-ffhc-5mcf-pf4q (CVE-2026-44581)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 4.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-ffhc-5mcf-pf4q (CVE-2026-44581) для пакета npm next версии 15.5.9: Next.js vulnerable to cross-site scripting in App Router applications using CSP nonces. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-ffhc-5mcf-pf4q
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-ffhc-5mcf-pf4q](https://osv.dev/vulnerability/GHSA-ffhc-5mcf-pf4q) · manifest · SHA-256 810079ef8dc5eaa280e4e8a3e812d5c2e63da98b796b146637b1036f770da719_

```
{"id": "GHSA-ffhc-5mcf-pf4q", "aliases": ["CVE-2026-44581"], "modified": "2026-09-10T03:51:05.447940563Z", "summary": "Next.js vulnerable to cross-site scripting in App Router applications using CSP nonces", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:L/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06031 — next 15.5.9 затронут GHSA-ggv3-7p47-pfv8 (CVE-2026-29057)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-ggv3-7p47-pfv8 (CVE-2026-29057) для пакета npm next версии 15.5.9: Next.js: HTTP request smuggling in rewrites. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-ggv3-7p47-pfv8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-ggv3-7p47-pfv8](https://osv.dev/vulnerability/GHSA-ggv3-7p47-pfv8) · manifest · SHA-256 52f0a1d6b4eba8994cc24d41c5d471ff9244c62011d5a3ec86e71508059fb688_

```
{"id": "GHSA-ggv3-7p47-pfv8", "aliases": ["CVE-2026-29057"], "modified": "2026-09-10T03:50:39.201962373Z", "summary": "Next.js: HTTP request smuggling in rewrites", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.13, 16.1.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06032 — next 15.5.9 затронут GHSA-gx5p-jg67-6x7h (CVE-2026-44580)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 6.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-gx5p-jg67-6x7h (CVE-2026-44580) для пакета npm next версии 15.5.9: Next.js has cross-site scripting in beforeInteractive scripts with untrusted input. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-gx5p-jg67-6x7h
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-gx5p-jg67-6x7h](https://osv.dev/vulnerability/GHSA-gx5p-jg67-6x7h) · manifest · SHA-256 35de60948d74593c5fcebcae6555fa161d7fd261475f9930b9daaf4e9b53909f_

```
{"id": "GHSA-gx5p-jg67-6x7h", "aliases": ["CVE-2026-44580"], "modified": "2026-09-10T03:51:05.785143220Z", "summary": "Next.js has cross-site scripting in beforeInteractive scripts with untrusted input", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06033 — next-auth 5.0.0-beta.29 затронут GHSA-5jpx-9hw9-2fx4

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next-auth@5.0.0-beta.29`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-5jpx-9hw9-2fx4 для пакета npm next-auth версии 5.0.0-beta.29: NextAuthjs Email misdelivery Vulnerability. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5jpx-9hw9-2fx4
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-5jpx-9hw9-2fx4](https://osv.dev/vulnerability/GHSA-5jpx-9hw9-2fx4) · manifest · SHA-256 f05eb5ebbaa4b6eb0a9f71f9d069c0cc723f98501582c0d575984d863f4baa41_

```
{"id": "GHSA-5jpx-9hw9-2fx4", "aliases": [], "modified": "2026-09-10T03:50:29.281362473Z", "summary": "NextAuthjs Email misdelivery Vulnerability", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.24.12, 5.0.0-beta.30).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06036 — next-auth 5.0.0-beta.29 затронут GHSA-x445-f3h2-j279 (CVE-2026-73419)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next-auth@5.0.0-beta.29`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 6.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-x445-f3h2-j279 (CVE-2026-73419) для пакета npm next-auth версии 5.0.0-beta.29: Auth.js: OAuth state, nonce, and PKCE check cookies are not bound to the provider that created them. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x445-f3h2-j279
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-x445-f3h2-j279](https://osv.dev/vulnerability/GHSA-x445-f3h2-j279) · manifest · SHA-256 3d09817224e9e9d930245325de10f3439c6c969795326b920ba5d883a82e22f4_

```
{"id": "GHSA-x445-f3h2-j279", "aliases": ["CVE-2026-73419"], "modified": "2026-09-10T03:50:53.095011411Z", "summary": "Auth.js: OAuth state, nonce, and PKCE check cookies are not bound to the provider that created them", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.24.15, 5.0.0-beta.32).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06046 — next 15.3.8 затронут GHSA-3x4c-7xq6-9pq8 (CVE-2026-27980)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3x4c-7xq6-9pq8 (CVE-2026-27980) для пакета npm next версии 15.3.8: Next.js: Unbounded next/image disk cache growth can exhaust storage. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3x4c-7xq6-9pq8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3x4c-7xq6-9pq8](https://osv.dev/vulnerability/GHSA-3x4c-7xq6-9pq8) · manifest · SHA-256 7d5aab6bba46c21b1813b72e8ce87efa70f7b8b814b880f9c5c0ea963f0b9a74_

```
{"id": "GHSA-3x4c-7xq6-9pq8", "aliases": ["CVE-2026-27980"], "modified": "2026-09-10T03:50:36.950018769Z", "summary": "Next.js: Unbounded next/image disk cache growth can exhaust storage", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.14, 16.1.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06047 — next 15.3.8 затронут GHSA-4342-x723-ch2f (CVE-2025-57822)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:N`)

OSV.dev сообщает GHSA-4342-x723-ch2f (CVE-2025-57822) для пакета npm next версии 15.3.8: Next.js Improper Middleware Redirect Handling Leads to SSRF. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4342-x723-ch2f
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4342-x723-ch2f](https://osv.dev/vulnerability/GHSA-4342-x723-ch2f) · manifest · SHA-256 2b92df1b6397760c0627352d6b3787ad2c3418a108e4ae2ed2ba785e1f5c7c67_

```
{"id": "GHSA-4342-x723-ch2f", "aliases": ["CVE-2025-57822"], "modified": "2026-09-10T03:50:26.545785200Z", "summary": "Next.js Improper Middleware Redirect Handling Leads to SSRF", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:L/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (14.2.32, 15.4.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06048 — next 15.3.8 затронут GHSA-4633-3j49-mh5q (CVE-2026-64647)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-4633-3j49-mh5q (CVE-2026-64647) для пакета npm next версии 15.3.8: Next.js: Cache confusion of response bodies for requests with bodies containing invalid UTF-8 byte sequences. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4633-3j49-mh5q
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4633-3j49-mh5q](https://osv.dev/vulnerability/GHSA-4633-3j49-mh5q) · manifest · SHA-256 7420b5b5742a23d83bb5acf4649fa8d0192088904eb2634f39d9d5d8cec65f4e_

```
{"id": "GHSA-4633-3j49-mh5q", "aliases": ["CVE-2026-64647"], "modified": "2026-09-10T03:50:51.390157243Z", "summary": "Next.js: Cache confusion of response bodies for requests with bodies containing invalid UTF-8 byte sequences", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.21, 16.2.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06049 — next 15.3.8 затронут GHSA-4c39-4ccg-62r3 (CVE-2026-64646)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-4c39-4ccg-62r3 (CVE-2026-64646) для пакета npm next версии 15.3.8: Next.js: Unbounded Server Action payload in Edge runtime. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4c39-4ccg-62r3
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4c39-4ccg-62r3](https://osv.dev/vulnerability/GHSA-4c39-4ccg-62r3) · manifest · SHA-256 5c9f84af8d713159459f897539d6f7b39f3e3ee2cde2a71957d649357dbe58b6_

```
{"id": "GHSA-4c39-4ccg-62r3", "aliases": ["CVE-2026-64646"], "modified": "2026-09-10T03:50:51.398762372Z", "summary": "Next.js: Unbounded Server Action payload in Edge runtime", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.21, 16.2.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06050 — next 15.3.8 затронут GHSA-4jqv-mc3x-m676 (CVE-2026-94543)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-4jqv-mc3x-m676 (CVE-2026-94543) для пакета npm next версии 15.3.8: Next.js has cache poisoning of SSG and ISR pages in self-hosted applications. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4jqv-mc3x-m676
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4jqv-mc3x-m676](https://osv.dev/vulnerability/GHSA-4jqv-mc3x-m676) · manifest · SHA-256 3da12d6118b9c8f9be68f2d3d34fe127c12486b41bb82358a75ad1bc5a50e4e4_

```
{"id": "GHSA-4jqv-mc3x-m676", "aliases": ["CVE-2026-94543"], "modified": "2026-10-07T20:45:06.342983181Z", "summary": "Next.js has cache poisoning of SSG and ISR pages in self-hosted applications", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.27, 16.3.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06051 — next 15.3.8 затронут GHSA-68g3-v927-f742 (CVE-2026-64648)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-68g3-v927-f742 (CVE-2026-64648) для пакета npm next версии 15.3.8: Next.js: Cache confusion of response bodies for requests with bodies. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-68g3-v927-f742
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-68g3-v927-f742](https://osv.dev/vulnerability/GHSA-68g3-v927-f742) · manifest · SHA-256 67bad25fdf4036bd6994b55f566c71a3b5c4d252652cb2524757452d06e798ac_

```
{"id": "GHSA-68g3-v927-f742", "aliases": ["CVE-2026-64648"], "modified": "2026-09-10T03:51:10.587986551Z", "summary": "Next.js: Cache confusion of response bodies for requests with bodies", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.21, 16.2.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06054 — next 15.3.8 затронут GHSA-955p-x3mx-jcvp (CVE-2026-64643)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-955p-x3mx-jcvp (CVE-2026-64643) для пакета npm next версии 15.3.8: Next.js: Unauthenticated disclosure of internal Server Function endpoints. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-955p-x3mx-jcvp
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-955p-x3mx-jcvp](https://osv.dev/vulnerability/GHSA-955p-x3mx-jcvp) · manifest · SHA-256 3d9a703112e42338524054a7b9d5a30eddc8bd4bda25a239cab3ed64f0a6733d_

```
{"id": "GHSA-955p-x3mx-jcvp", "aliases": ["CVE-2026-64643"], "modified": "2026-09-10T03:51:11.198992864Z", "summary": "Next.js: Unauthenticated disclosure of internal Server Function endpoints", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.21, 16.2.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06055 — next 15.3.8 затронут GHSA-9g9p-9gw9-jx7f (CVE-2025-59471)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-9g9p-9gw9-jx7f (CVE-2025-59471) для пакета npm next версии 15.3.8: Next.js self-hosted applications vulnerable to DoS via Image Optimizer remotePatterns configuration. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9g9p-9gw9-jx7f
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9g9p-9gw9-jx7f](https://osv.dev/vulnerability/GHSA-9g9p-9gw9-jx7f) · manifest · SHA-256 8f8a980faea6084564436720362b9d0b40a40361f136c8799cab60074be16057_

```
{"id": "GHSA-9g9p-9gw9-jx7f", "aliases": ["CVE-2025-59471"], "modified": "2026-09-10T03:50:59.013924260Z", "summary": "Next.js self-hosted applications vulnerable to DoS via Image Optimizer remotePatterns configuration", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.10, 16.1.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06057 — next 15.3.8 затронут GHSA-ffhc-5mcf-pf4q (CVE-2026-44581)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 4.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-ffhc-5mcf-pf4q (CVE-2026-44581) для пакета npm next версии 15.3.8: Next.js vulnerable to cross-site scripting in App Router applications using CSP nonces. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-ffhc-5mcf-pf4q
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-ffhc-5mcf-pf4q](https://osv.dev/vulnerability/GHSA-ffhc-5mcf-pf4q) · manifest · SHA-256 810079ef8dc5eaa280e4e8a3e812d5c2e63da98b796b146637b1036f770da719_

```
{"id": "GHSA-ffhc-5mcf-pf4q", "aliases": ["CVE-2026-44581"], "modified": "2026-09-10T03:51:05.447940563Z", "summary": "Next.js vulnerable to cross-site scripting in App Router applications using CSP nonces", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:L/I:L/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06058 — next 15.3.8 затронут GHSA-g5qg-72qw-gw5v (CVE-2025-57752)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 6.2 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-g5qg-72qw-gw5v (CVE-2025-57752) для пакета npm next версии 15.3.8: Next.js Affected by Cache Key Confusion for Image Optimization API Routes. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-g5qg-72qw-gw5v
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-g5qg-72qw-gw5v](https://osv.dev/vulnerability/GHSA-g5qg-72qw-gw5v) · manifest · SHA-256 a090f76ac4bfea6a867bd84fe784cffe05ea11374766ce4a1ec6bc1561eaf25e_

```
{"id": "GHSA-g5qg-72qw-gw5v", "aliases": ["CVE-2025-57752"], "modified": "2026-09-10T03:50:26.953168554Z", "summary": "Next.js Affected by Cache Key Confusion for Image Optimization API Routes", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (14.2.31, 15.4.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06059 — next 15.3.8 затронут GHSA-ggv3-7p47-pfv8 (CVE-2026-29057)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-ggv3-7p47-pfv8 (CVE-2026-29057) для пакета npm next версии 15.3.8: Next.js: HTTP request smuggling in rewrites. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-ggv3-7p47-pfv8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-ggv3-7p47-pfv8](https://osv.dev/vulnerability/GHSA-ggv3-7p47-pfv8) · manifest · SHA-256 52f0a1d6b4eba8994cc24d41c5d471ff9244c62011d5a3ec86e71508059fb688_

```
{"id": "GHSA-ggv3-7p47-pfv8", "aliases": ["CVE-2026-29057"], "modified": "2026-09-10T03:50:39.201962373Z", "summary": "Next.js: HTTP request smuggling in rewrites", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.13, 16.1.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06060 — vite 5.4.20 затронут GHSA-4w7w-66w2-5vf9 (CVE-2026-39365)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/vite@5.4.20`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-4w7w-66w2-5vf9 (CVE-2026-39365) для пакета npm vite версии 5.4.20: Vite Vulnerable to Path Traversal in Optimized Deps `.map` Handling. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4w7w-66w2-5vf9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4w7w-66w2-5vf9](https://osv.dev/vulnerability/GHSA-4w7w-66w2-5vf9) · manifest · SHA-256 2d8af461ca5b9c8da132da217cea3bb2b6099d17661201d0761cb8bba5fcf263_

```
{"id": "GHSA-4w7w-66w2-5vf9", "aliases": ["CVE-2026-39365"], "modified": "2026-09-10T03:50:42.779400319Z", "summary": "Vite Vulnerable to Path Traversal in Optimized Deps `.map` Handling", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.4.2, 7.3.2, 8.0.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06062 — vite 5.4.20 затронут GHSA-698v-4r3x-3vcv (CVE-2026-112943)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/vite@5.4.20`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-698v-4r3x-3vcv (CVE-2026-112943) для пакета npm vite версии 5.4.20: launch-editor: escapeCmdArgs() omits % escaping on Windows. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-698v-4r3x-3vcv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-698v-4r3x-3vcv](https://osv.dev/vulnerability/GHSA-698v-4r3x-3vcv) · manifest · SHA-256 3d880c5ce372ee43fa6ebbf567d9fa716d9e60131f9973c5c56248a33ee61f2b_

```
{"id": "GHSA-698v-4r3x-3vcv", "aliases": ["CVE-2026-112943"], "modified": "2026-10-20T18:45:09.467993691Z", "summary": "launch-editor: escapeCmdArgs() omits % escaping on Windows", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.4.4, 7.3.7, 8.1.6, 8.2.4, 8.3.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06063 — vite 5.4.20 затронут GHSA-93m4-6634-74q7 (CVE-2025-62522)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/vite@5.4.20`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-93m4-6634-74q7 (CVE-2025-62522) для пакета npm vite версии 5.4.20: vite allows server.fs.deny bypass via backslash on Windows. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-93m4-6634-74q7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-93m4-6634-74q7](https://osv.dev/vulnerability/GHSA-93m4-6634-74q7) · manifest · SHA-256 9ce67f87142a21ecc9de243b1c2d27732b6041d87501d832af52623d13bcd02c_

```
{"id": "GHSA-93m4-6634-74q7", "aliases": ["CVE-2025-62522"], "modified": "2026-09-10T03:50:29.574857832Z", "summary": "vite allows server.fs.deny bypass via backslash on Windows", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (5.4.21, 6.4.1, 7.0.8, 7.1.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06065 — vite 5.4.20 затронут GHSA-fx2h-pf6j-xcff (CVE-2026-53571)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/vite@5.4.20`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-fx2h-pf6j-xcff (CVE-2026-53571) для пакета npm vite версии 5.4.20: vite: `server.fs.deny` bypass on Windows alternate paths. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-fx2h-pf6j-xcff
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-fx2h-pf6j-xcff](https://osv.dev/vulnerability/GHSA-fx2h-pf6j-xcff) · manifest · SHA-256 6401e2d9418c8e34b0ccf53d72ca312e91a8da46875677694958fe3acda1cf38_

```
{"id": "GHSA-fx2h-pf6j-xcff", "aliases": ["CVE-2026-53571"], "modified": "2026-10-27T15:15:07.885624041Z", "summary": "vite: `server.fs.deny` bypass on Windows alternate paths", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:N/SC:H/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.4.3, 7.3.5, 8.0.16).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06066 — vite 5.4.20 затронут GHSA-r825-w8mm-5pxw (CVE-2026-112944)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/vite@5.4.20`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-r825-w8mm-5pxw (CVE-2026-112944) для пакета npm vite версии 5.4.20: launch-editor: Editor CLI flag misinterpretation causing arbitrary command execution for some editors. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-r825-w8mm-5pxw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-r825-w8mm-5pxw](https://osv.dev/vulnerability/GHSA-r825-w8mm-5pxw) · manifest · SHA-256 1d1fc9462fe03e400685191017eea42d4a3eb01d86bf299e4a97e2a13b714bd6_

```
{"id": "GHSA-r825-w8mm-5pxw", "aliases": ["CVE-2026-112944"], "modified": "2026-10-20T20:00:04.608907013Z", "summary": "launch-editor: Editor CLI flag misinterpretation causing arbitrary command execution for some editors", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.4.4, 7.3.7, 8.1.6, 8.2.4, 8.3.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06067 — vite 5.4.20 затронут GHSA-rq7h-c2jc-7f22 (CVE-2026-112946)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/vite@5.4.20`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-rq7h-c2jc-7f22 (CVE-2026-112946) для пакета npm vite версии 5.4.20: Vite: Files outside `server.fs.allow` could be served when project paths match system paths on non-Windows machine. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rq7h-c2jc-7f22
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rq7h-c2jc-7f22](https://osv.dev/vulnerability/GHSA-rq7h-c2jc-7f22) · manifest · SHA-256 81d835b65622def1bcfa136dfe243a69349ccdb05fd2eae110f35eccbe536d25_

```
{"id": "GHSA-rq7h-c2jc-7f22", "aliases": ["CVE-2026-112946"], "modified": "2026-10-21T17:00:06.336868869Z", "summary": "Vite: Files outside `server.fs.allow` could be served when project paths match system paths on non-Windows machine", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.4.4, 7.3.7, 8.1.6, 8.2.4, 8.3.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06068 — vite 5.4.20 затронут GHSA-v6wh-96g9-6wx3 (CVE-2026-53632)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/vite@5.4.20`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-v6wh-96g9-6wx3 (CVE-2026-53632) для пакета npm vite версии 5.4.20: launch-editor: NTLMv2 hash disclosure via UNC path handling on Windows. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-v6wh-96g9-6wx3
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-v6wh-96g9-6wx3](https://osv.dev/vulnerability/GHSA-v6wh-96g9-6wx3) · manifest · SHA-256 612ffce7fd26a70e70cd4ca05a081231b9c81d440b83548d1e59509bc63cf1c3_

```
{"id": "GHSA-v6wh-96g9-6wx3", "aliases": ["CVE-2026-53632"], "modified": "2026-09-10T03:50:50.705036566Z", "summary": "launch-editor: NTLMv2 hash disclosure via UNC path handling on Windows", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:A/VC:N/VI:N/VA:N/SC:H/SI:H/SA:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.4.3, 7.3.5, 8.0.16).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05983 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (4 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: apps/browser-extension/src/core/BitcoinProvider.ts
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 33.0 / 100
- CVSS v3.1: неприменимо

5 упоминаний ECDSA в 4 файл(ах), например apps/browser-extension/src/core/BitcoinProvider.ts:1. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте apps/browser-extension/src/core/BitcoinProvider.ts:1 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [apps/browser-extension/src/core/BitcoinProvider.ts](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/apps/browser-extension/src/core/BitcoinProvider.ts#L1) · line 1 · SHA-256 cc7b2c4dae48a77ce2f9a384e5d46b7de8ce4ca6a7e24c3d60ccaf45dec7dad7_

```
    1 | import ecc from '@bitcoinerlab/secp256k1'
    2 | import type { IdentifierArray, WalletAccount } from '@wallet-standard/base'
```

_file_excerpt · [apps/browser-extension/src/core/transport.ts](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/apps/browser-extension/src/core/transport.ts#L23) · line 23 · SHA-256 92c895fac8b058f6d089bd95bf1e679f1e51cdd0be88b1b0d6a87a984b6e1a09_

```
   22 |       const account = privateKeyToAccount(AccountUtil.privateKeyEvm)
   23 |       const { address, signMessage, signTypedData } = account
   24 | 
```

_file_excerpt · [apps/browser-extension/src/core/transport.ts](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/apps/browser-extension/src/core/transport.ts#L93) · line 93 · SHA-256 ef300d8f42176e425dfa45039f64627f2d47931082c26bf1e680eb24d60d3322_

```
   92 | 
   93 |           return signTypedData(JSON.parse(typedData))
   94 |         }
```

_file_excerpt · [apps/laboratory/src/components/Wagmi/WagmiRequestPermissionsAsyncTest.tsx](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/apps/laboratory/src/components/Wagmi/WagmiRequestPermissionsAsyncTest.tsx#L75) · line 75 · SHA-256 e31b4519f2097f02dedb7b234c12edf950d556511f10c26c4070d7a617c4126a_

```
   74 |               {
   75 |                 type: 'secp256k1',
   76 |                 publicKey: signer.publicKey
```

_file_excerpt · [apps/laboratory/src/utils/BitcoinUtil.ts](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/apps/laboratory/src/utils/BitcoinUtil.ts#L1) · line 1 · SHA-256 53787a7bb11c746410e3c36c76cb422436e9f4709ad1a6e2ef2c09e660faf955_

```
    1 | import ecc from '@bitcoinerlab/secp256k1'
    2 | import * as bitcoin from 'bitcoinjs-lib'
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05984 — Квантово-уязвимый ECDSA: роль не определена (8 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: apps/gallery/utils/PresetUtils.ts
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 31.7 / 100
- CVSS v3.1: неприменимо

14 упоминаний ECDSA в 8 файл(ах), например apps/gallery/utils/PresetUtils.ts:367. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте apps/gallery/utils/PresetUtils.ts:367 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [apps/gallery/utils/PresetUtils.ts](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/apps/gallery/utils/PresetUtils.ts#L367) · line 367 · SHA-256 c7756c80855236e7dada117f38cad57f2b6da546ed5b148a0fa051443040152d_

```
  366 | 
  367 | export const signTypedData = {
  368 |   domain: {
```

_file_excerpt · [apps/laboratory/src/components/Ethers/EthersSignTypedDataTest.tsx](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/apps/laboratory/src/components/Ethers/EthersSignTypedDataTest.tsx#L58) · line 58 · SHA-256 9b5545ec626d33aa6a52b8c36b370e7651a1ecd2ab001d4f3b8bab485ac188a4_

```
   57 | 
   58 |       const signature = await signer?.signTypedData(domain, types, message)
   59 | 
```

_file_excerpt · [apps/laboratory/src/components/Wagmi/WagmiRequestPermissionsSyncTest.tsx](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/apps/laboratory/src/components/Wagmi/WagmiRequestPermissionsSyncTest.tsx#L94) · line 94 · SHA-256 1e443b35eca2686f8f5e8736116ade7bbe6f3fddc5480978ac8b825501111b2a_

```
   93 |               {
   94 |                 type: 'secp256r1',
   95 |                 publicKey: passkeyPublicKey
```

_file_excerpt · [apps/laboratory/src/utils/EncodingUtils.ts](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/apps/laboratory/src/utils/EncodingUtils.ts#L10) · line 10 · SHA-256 5fdbeecacbf3de93cc8fa3a8fba5b374d7f0717ee48b263ab3c93445727596a3_

```
    9 | export enum KeyTypes {
   10 |   secp256k1 = 'secp256k1',
   11 |   secp256r1 = 'secp256r1'
```

_file_excerpt · [apps/laboratory/src/utils/EncodingUtils.ts](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/apps/laboratory/src/utils/EncodingUtils.ts#L11) · line 11 · SHA-256 50523307d14fc74ec251d66c920485157b2813e58dba73d92347260e63ea312e_

```
   10 |   secp256k1 = 'secp256k1',
   11 |   secp256r1 = 'secp256r1'
   12 | }
```

_file_excerpt · [apps/laboratory/src/utils/EncodingUtils.ts](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/apps/laboratory/src/utils/EncodingUtils.ts#L17) · line 17 · SHA-256 7cf8030e042d8a5e382f0fb25b07d31c6e02c5228aa2f6e34f57f2784af9393e_

```
   16 |   const keyTypeToDIDPrefix: Record<string, string> = {
   17 |     secp256k1: 'did:key:zQ3s',
   18 |     secp256r1: 'did:key:zDn'
```

_file_excerpt · [packages/experimental/src/smart-session/controllers/SmartSessionsController.ts](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/packages/experimental/src/smart-session/controllers/SmartSessionsController.ts#L271) · line 271 · SHA-256 def397fa8c6c545f5edceda42619bae47b9b26c5ce5008b194a16eceb8e2fb62_

```
  270 |             {
  271 |               type: 'secp256k1',
  272 |               publicKey: request.signerPublicKey
```

_file_excerpt · [packages/experimental/src/smart-session/helper/index.ts](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/packages/experimental/src/smart-session/helper/index.ts#L143) · line 143 · SHA-256 8a4ec6f461bbc27347fd5598b7634f3997334b06d94a8979462bcff4d27db938_

```
  142 | 
  143 |   if ((type as string).toLowerCase() !== 'secp256k1' && type !== 'secp256r1') {
  144 |     throw new Error('Invalid key type')
```

_file_excerpt · [packages/experimental/src/smart-session/schema/index.ts](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/packages/experimental/src/smart-session/schema/index.ts#L21) · line 21 · SHA-256 b606994f1a01b4cf2d3f30b4cc411976fdb5c3d3fda665981b05aa0d06ee8a46_

```
   20 |   UNSUPPORTED_SIGNER_TYPE: 'Unsupported signer type',
   21 |   UNSUPPORTED_KEY_TYPE: 'Unsupported key type: must be secp256r1 or secp256k1',
   22 |   INVALID_PUBLIC_KEY_FORMAT: 'Invalid public key: must start with "0x"',
```

_file_excerpt · [packages/experimental/src/smart-session/schema/index.ts](https://github.com/reown-com/appkit/blob/8f9f39f1dfe0a21bb619dd9a33b6d7500523298b/packages/experimental/src/smart-session/schema/index.ts#L65) · line 65 · SHA-256 bd371f6e7e79053a73e69ff8420aa5a8b3d4102f32714b4836a500659dc628cd_

```
   64 | const KeySchema = z.object({
   65 |   type: z.enum(['secp256r1', 'secp256k1'], {
   66 |     errorMap: () => ({ message: ERROR_MESSAGES.UNSUPPORTED_KEY_TYPE })
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06072 — @auth/core 0.40.0 затронут GHSA-x445-f3h2-j279 (CVE-2026-73419)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@auth/core@0.40.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: 6.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-x445-f3h2-j279 (CVE-2026-73419) для пакета npm @auth/core версии 0.40.0: Auth.js: OAuth state, nonce, and PKCE check cookies are not bound to the provider that created them. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x445-f3h2-j279
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-x445-f3h2-j279](https://osv.dev/vulnerability/GHSA-x445-f3h2-j279) · manifest · SHA-256 ddf6dc879fe94600e3ff69520df9b5e98497efa6d316ca0b34998855217c7ce6_

```
{"id": "GHSA-x445-f3h2-j279", "aliases": ["CVE-2026-73419"], "modified": "2026-09-10T03:50:53.095011411Z", "summary": "Auth.js: OAuth state, nonce, and PKCE check cookies are not bound to the provider that created them", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.41.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06074 — @fastify/busboy 2.1.1 затронут GHSA-gxm5-99cw-xjw9 (CVE-2026-74866)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@fastify/busboy@2.1.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: 5.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-gxm5-99cw-xjw9 (CVE-2026-74866) для пакета npm @fastify/busboy версии 2.1.1: @fastify/busboy vulnerable to CRLF injection via multipart Content-Disposition filename and name. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-gxm5-99cw-xjw9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-gxm5-99cw-xjw9](https://osv.dev/vulnerability/GHSA-gxm5-99cw-xjw9) · manifest · SHA-256 0319fd5b25e01743025ab808de0d7288eb9b9e77cea0d537f8acbbc04de704c6_

```
{"id": "GHSA-gxm5-99cw-xjw9", "aliases": ["CVE-2026-74866"], "modified": "2026-10-05T22:45:04.558942837Z", "summary": "@fastify/busboy vulnerable to CRLF injection via multipart Content-Disposition filename and name", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.2.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06077 — @opentelemetry/core 1.30.1 затронут GHSA-8988-4f7v-96qf (CVE-2026-54285)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@opentelemetry/core@1.30.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-8988-4f7v-96qf (CVE-2026-54285) для пакета npm @opentelemetry/core версии 1.30.1: OpenTelemetry Core: Unbounded memory allocation in W3C Baggage propagation. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8988-4f7v-96qf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8988-4f7v-96qf](https://osv.dev/vulnerability/GHSA-8988-4f7v-96qf) · manifest · SHA-256 e87c8a224bbf883f910163ad20592f74bb8ce978a87cb96bf8f0254bcee9cc91_

```
{"id": "GHSA-8988-4f7v-96qf", "aliases": ["CVE-2026-54285"], "modified": "2026-09-10T03:50:48.883260062Z", "summary": "OpenTelemetry Core: Unbounded memory allocation in W3C Baggage propagation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.8.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06078 — @opentelemetry/instrumentation-knex 0.44.0 затронут GHSA-qqmp-wf37-98f9 (CVE-2026-104872)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@opentelemetry/instrumentation-knex@0.44.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: 5.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-qqmp-wf37-98f9 (CVE-2026-104872) для пакета npm @opentelemetry/instrumentation-knex версии 0.44.0: Multiple @opentelemetry/instrumentation-* packages expose database username via unconditional db.user span attribute. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qqmp-wf37-98f9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qqmp-wf37-98f9](https://osv.dev/vulnerability/GHSA-qqmp-wf37-98f9) · manifest · SHA-256 b3a30705ee170d493a18b8f634198867bee48da8daa6f025b63bca31c5b9d1a5_

```
{"id": "GHSA-qqmp-wf37-98f9", "aliases": ["CVE-2026-104872"], "modified": "2026-10-05T23:00:05.311085601Z", "summary": "Multiple @opentelemetry/instrumentation-* packages expose database username via unconditional db.user span attribute", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.65.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06079 — @opentelemetry/instrumentation-mongoose 0.46.0 затронут GHSA-qqmp-wf37-98f9 (CVE-2026-104872)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@opentelemetry/instrumentation-mongoose@0.46.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: 5.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-qqmp-wf37-98f9 (CVE-2026-104872) для пакета npm @opentelemetry/instrumentation-mongoose версии 0.46.0: Multiple @opentelemetry/instrumentation-* packages expose database username via unconditional db.user span attribute. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qqmp-wf37-98f9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qqmp-wf37-98f9](https://osv.dev/vulnerability/GHSA-qqmp-wf37-98f9) · manifest · SHA-256 b3a30705ee170d493a18b8f634198867bee48da8daa6f025b63bca31c5b9d1a5_

```
{"id": "GHSA-qqmp-wf37-98f9", "aliases": ["CVE-2026-104872"], "modified": "2026-10-05T23:00:05.311085601Z", "summary": "Multiple @opentelemetry/instrumentation-* packages expose database username via unconditional db.user span attribute", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.67.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06080 — @opentelemetry/instrumentation-mysql2 0.45.0 затронут GHSA-qqmp-wf37-98f9 (CVE-2026-104872)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@opentelemetry/instrumentation-mysql2@0.45.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: 5.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-qqmp-wf37-98f9 (CVE-2026-104872) для пакета npm @opentelemetry/instrumentation-mysql2 версии 0.45.0: Multiple @opentelemetry/instrumentation-* packages expose database username via unconditional db.user span attribute. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qqmp-wf37-98f9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qqmp-wf37-98f9](https://osv.dev/vulnerability/GHSA-qqmp-wf37-98f9) · manifest · SHA-256 b3a30705ee170d493a18b8f634198867bee48da8daa6f025b63bca31c5b9d1a5_

```
{"id": "GHSA-qqmp-wf37-98f9", "aliases": ["CVE-2026-104872"], "modified": "2026-10-05T23:00:05.311085601Z", "summary": "Multiple @opentelemetry/instrumentation-* packages expose database username via unconditional db.user span attribute", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.67.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06081 — @opentelemetry/instrumentation-mysql 0.45.0 затронут GHSA-qqmp-wf37-98f9 (CVE-2026-104872)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@opentelemetry/instrumentation-mysql@0.45.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: 5.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-qqmp-wf37-98f9 (CVE-2026-104872) для пакета npm @opentelemetry/instrumentation-mysql версии 0.45.0: Multiple @opentelemetry/instrumentation-* packages expose database username via unconditional db.user span attribute. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qqmp-wf37-98f9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qqmp-wf37-98f9](https://osv.dev/vulnerability/GHSA-qqmp-wf37-98f9) · manifest · SHA-256 b3a30705ee170d493a18b8f634198867bee48da8daa6f025b63bca31c5b9d1a5_

```
{"id": "GHSA-qqmp-wf37-98f9", "aliases": ["CVE-2026-104872"], "modified": "2026-10-05T23:00:05.311085601Z", "summary": "Multiple @opentelemetry/instrumentation-* packages expose database username via unconditional db.user span attribute", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.67.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06082 — @opentelemetry/instrumentation-pg 0.50.0 затронут GHSA-qqmp-wf37-98f9 (CVE-2026-104872)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@opentelemetry/instrumentation-pg@0.50.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: 5.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-qqmp-wf37-98f9 (CVE-2026-104872) для пакета npm @opentelemetry/instrumentation-pg версии 0.50.0: Multiple @opentelemetry/instrumentation-* packages expose database username via unconditional db.user span attribute. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qqmp-wf37-98f9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qqmp-wf37-98f9](https://osv.dev/vulnerability/GHSA-qqmp-wf37-98f9) · manifest · SHA-256 b3a30705ee170d493a18b8f634198867bee48da8daa6f025b63bca31c5b9d1a5_

```
{"id": "GHSA-qqmp-wf37-98f9", "aliases": ["CVE-2026-104872"], "modified": "2026-10-05T23:00:05.311085601Z", "summary": "Multiple @opentelemetry/instrumentation-* packages expose database username via unconditional db.user span attribute", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.73.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06083 — @opentelemetry/instrumentation-tedious 0.18.0 затронут GHSA-qqmp-wf37-98f9 (CVE-2026-104872)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@opentelemetry/instrumentation-tedious@0.18.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: 5.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-qqmp-wf37-98f9 (CVE-2026-104872) для пакета npm @opentelemetry/instrumentation-tedious версии 0.18.0: Multiple @opentelemetry/instrumentation-* packages expose database username via unconditional db.user span attribute. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qqmp-wf37-98f9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qqmp-wf37-98f9](https://osv.dev/vulnerability/GHSA-qqmp-wf37-98f9) · manifest · SHA-256 b3a30705ee170d493a18b8f634198867bee48da8daa6f025b63bca31c5b9d1a5_

```
{"id": "GHSA-qqmp-wf37-98f9", "aliases": ["CVE-2026-104872"], "modified": "2026-10-05T23:00:05.311085601Z", "summary": "Multiple @opentelemetry/instrumentation-* packages expose database username via unconditional db.user span attribute", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.40.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06084 — @parcel/reporter-dev-server 2.13.3 затронут GHSA-qm9p-f9j5-w83w (CVE-2025-56648)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/@parcel/reporter-dev-server@2.13.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-qm9p-f9j5-w83w (CVE-2025-56648) для пакета npm @parcel/reporter-dev-server версии 2.13.3: Parcel has an Origin Validation Error vulnerability. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qm9p-f9j5-w83w
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qm9p-f9j5-w83w](https://osv.dev/vulnerability/GHSA-qm9p-f9j5-w83w) · manifest · SHA-256 e6625d4f89f721210af62b1518dc31b19fe473403644450d303458b933710a4b_

```
{"id": "GHSA-qm9p-f9j5-w83w", "aliases": ["CVE-2025-56648"], "modified": "2026-04-13T19:02:07.652067Z", "summary": "Parcel has an Origin Validation Error vulnerability", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.16.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05987 — webpack 5.94.0 затронут GHSA-38r7-794h-5758 (CVE-2025-68157)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/webpack@5.94.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 36.0 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-38r7-794h-5758 (CVE-2025-68157) для пакета npm webpack версии 5.94.0: webpack buildHttp HttpUriPlugin allowedUris bypass via HTTP redirects → SSRF + cache persistence. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-38r7-794h-5758
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-38r7-794h-5758](https://osv.dev/vulnerability/GHSA-38r7-794h-5758) · manifest · SHA-256 dbb1acf5d775fc8d200ace74d0710cfa904a43ac2b038e0491f27e62fa9f006d_

```
{"id": "GHSA-38r7-794h-5758", "aliases": ["CVE-2025-68157"], "modified": "2026-09-10T03:50:33.757470252Z", "summary": "webpack buildHttp HttpUriPlugin allowedUris bypass via HTTP redirects → SSRF + cache persistence", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:L/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (5.104.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05988 — webpack 5.94.0 затронут GHSA-8fgc-7cc6-rx7x (CVE-2025-68458)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/webpack@5.94.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 36.0 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-8fgc-7cc6-rx7x (CVE-2025-68458) для пакета npm webpack версии 5.94.0: webpack buildHttp: allowedUris allow-list bypass via URL userinfo (@) leading to build-time SSRF behavior. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8fgc-7cc6-rx7x
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8fgc-7cc6-rx7x](https://osv.dev/vulnerability/GHSA-8fgc-7cc6-rx7x) · manifest · SHA-256 586289730ad161ee01952dd52730382b043bfd7ee9733ed9308674a0ef5e7d14_

```
{"id": "GHSA-8fgc-7cc6-rx7x", "aliases": ["CVE-2025-68458"], "modified": "2026-09-10T03:50:34.472343977Z", "summary": "webpack buildHttp: allowedUris allow-list bypass via URL userinfo (@) leading to build-time SSRF behavior", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:L/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (5.104.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06018 — next 15.5.9 затронут GHSA-3g8h-86w9-wvmq (CVE-2026-44572)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.5.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 36.0 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-3g8h-86w9-wvmq (CVE-2026-44572) для пакета npm next версии 15.5.9: Next.js's Middleware / Proxy redirects can be cache-poisoned. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3g8h-86w9-wvmq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3g8h-86w9-wvmq](https://osv.dev/vulnerability/GHSA-3g8h-86w9-wvmq) · manifest · SHA-256 f0d0cad7d1e8fe59288e33ea590561f52e5302339ea14cf182821c218cac5f38_

```
{"id": "GHSA-3g8h-86w9-wvmq", "aliases": ["CVE-2026-44572"], "modified": "2026-09-10T03:51:04.422954573Z", "summary": "Next.js's Middleware / Proxy redirects can be cache-poisoned", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06045 — next 15.3.8 затронут GHSA-3g8h-86w9-wvmq (CVE-2026-44572)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/next@15.3.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 36.0 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-3g8h-86w9-wvmq (CVE-2026-44572) для пакета npm next версии 15.3.8: Next.js's Middleware / Proxy redirects can be cache-poisoned. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3g8h-86w9-wvmq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3g8h-86w9-wvmq](https://osv.dev/vulnerability/GHSA-3g8h-86w9-wvmq) · manifest · SHA-256 f0d0cad7d1e8fe59288e33ea590561f52e5302339ea14cf182821c218cac5f38_

```
{"id": "GHSA-3g8h-86w9-wvmq", "aliases": ["CVE-2026-44572"], "modified": "2026-09-10T03:51:04.422954573Z", "summary": "Next.js's Middleware / Proxy redirects can be cache-poisoned", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (15.5.16, 16.2.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06064 — vite 5.4.20 затронут GHSA-9jrq-w75r-8gcw (CVE-2026-112945)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/vite@5.4.20`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 36.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-9jrq-w75r-8gcw (CVE-2026-112945) для пакета npm vite версии 5.4.20: Vite: Cross origin script execution through Vite custom middleware. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9jrq-w75r-8gcw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9jrq-w75r-8gcw](https://osv.dev/vulnerability/GHSA-9jrq-w75r-8gcw) · manifest · SHA-256 b9cadeb1b3d0e221a0b498a223b125206256dd81815711e358f14498516515fb_

```
{"id": "GHSA-9jrq-w75r-8gcw", "aliases": ["CVE-2026-112945"], "modified": "2026-10-21T17:00:26.569382874Z", "summary": "Vite: Cross origin script execution through Vite custom middleware", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:A/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.4.4, 7.3.7, 8.1.6, 8.2.4, 8.3.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06085 — 19 бюллетеней в 8 пакет(ах) npm, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:npm:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 13.7 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 19 бюллетеней (9 с оценкой high или critical) для 8 пакет(ов) npm, которые подтягивают только инструменты разработки или сборки (apps/browser-extension/package.json, apps/pay-test-exchange/package.json, package.json, packages/adapters/polkadot/package.json, packages/siwx/package.json): например, danger@13.0.2 [dev]: GHSA-3x93-p86w-5jvh; happy-dom@15.11.7 [dev]: GHSA-37j7-fg3j-429f, GHSA-6q6h-j7hj-3r64, GHSA-w4gp-fjgq-3q4g; postcss@8.5.3 [dev]: GHSA-6g55-p6wh-862q, GHSA-fxqj-rqcc-2cmp, GHSA-qx2v-qp2m-jg93, GHSA-r28c-9q8g-f849; turbo@2.5.8 [dev]: GHSA-3qcw-2rhx-2726, GHSA-hcf7-66rw-9f5r; vitest@2.1.9 [dev]: GHSA-5xrq-8626-4rwp, GHSA-82fw-gwwq-j7x9. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в apps/browser-extension/package.json, apps/pay-test-exchange/package.json, package.json, packages/adapters/polkadot/package.json, packages/siwx/package.json.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · apps/browser-extension/package.json · SHA-256 12d21c4696696581601a4ab1044cc08adc3cc4215a78e366c3ebbeccb7300597_

```
danger@13.0.2 [dev]: GHSA-3x93-p86w-5jvh
happy-dom@15.11.7 [dev]: GHSA-37j7-fg3j-429f, GHSA-6q6h-j7hj-3r64, GHSA-w4gp-fjgq-3q4g
postcss@8.5.3 [dev]: GHSA-6g55-p6wh-862q, GHSA-fxqj-rqcc-2cmp, GHSA-qx2v-qp2m-jg93, GHSA-r28c-9q8g-f849
turbo@2.5.8 [dev]: GHSA-3qcw-2rhx-2726, GHSA-hcf7-66rw-9f5r
vitest@2.1.9 [dev]: GHSA-5xrq-8626-4rwp, GHSA-82fw-gwwq-j7x9
vitest@3.1.3 [dev]: GHSA-5xrq-8626-4rwp, GHSA-82fw-gwwq-j7x9
webpack-dev-server@5.2.1 [dev]: GHSA-79cf-xcqc-c78w, GHSA-f5vj-f2hx-8m93, GHSA-m28w-2pqf-7qgj, GHSA-mx8g-39q3-5c79
wrangler@4.25.1 [dev]: GHSA-36p8-mvp6-cv38
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05985 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:40 UTC
- Балл приоритета: 12.2 / 100
- CVSS v3.1: неприменимо

В 34 манифестах зависимостей QSI нашёл криптобиблиотеки (@noble/curves, @noble/hashes, @noble/secp256k1, @solana/web3.js, bitcoinjs-lib, elliptic, ethers, jose, jsonwebtoken, node-forge, secp256k1, tweetnacl), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · apps/browser-extension/package.json, apps/gallery/package.json, apps/laboratory/package.json, apps/pay-test-exchange/package.json, package.json, packages/adapters/bitcoin/package.json, packages/adapters/ethers/package.json, packages/adapters/ethers5/package.json, packages/adapters/polkadot/package.json, packages/adapters/solana/package.json, packages/adapters/stellar/package.json, packages/adapters/ton/package.json, packages/adapters/tron/package.json, packages/adapters/wagmi/package.json, packa · SHA-256 2d4b0b61022e8ab71cf828ac9cf60ebe3d2d9d2a2158916dfb3e37af51d831bf_

```
Crypto libraries: @noble/curves, @noble/hashes, @noble/secp256k1, @solana/web3.js, bitcoinjs-lib, elliptic, ethers, jose, jsonwebtoken, node-forge, secp256k1, tweetnacl
```

**Ограничения проверки.** Отсутствие доказательств не является доказательством отсутствия: системные библиотеки и транзитивные зависимости могут не указываться.

**Рекомендация.** Определите источник поддержки PQC (TLS-терминатор, KMS/HSM, обновление библиотек).

**Повторная проверка.** Повторите сканирование после обновлений.


## 8. Постквантовая оценка

| | Обмен ключами (x — сколько данные должны оставаться конфиденциальными; «собери сейчас, расшифруй потом») | Подписи (x — сколько подписи и ключи должны оставаться доверенными) |
|---|---|---|
| Срок жизни данных/ключей x | 5 | 10 |
| Время миграции y | 5 | 5 |
| Принятое число лет до CRQC z | 12 (central) | 12 |
| x + y − z | -2 → запас минимален | 3 → при этом сценарии миграция завершится слишком поздно |
#### Откуда взято z

Усреднённая оценка экспертов, что CRQC появится в пределах горизонта, из ежегодного опроса, который публикует автор этого неравенства. Это оценки вероятности, а не предсказание даты.

| В пределах | Вероятность | Формулировка отчёта |
|---|---|---|
| 5 лет | ~15% | усреднённая оценка |
| 10 лет | 28-49% | вполне возможно |
| 15 лет | 51-70% | вероятно |

**Почему выбран этот сценарий (central, z = 12):** Между 10-летней полосой (28-49%) и 15-летней (51-70%): примерно там, где усреднённая оценка экспертов переходит половину. Больше половины опрошенных (13 из 26) уже считают вероятность 50% или выше для какого-либо горизонта.
_Допущения планирования: x для обмена ключами, x для подписей, y — значения по умолчанию профиля риска «Web3-проект», а не данные клиента; с фактическими сроками клиента вывод может измениться._

### Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет


**Следующий шаг:** Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **подпись транзакций и сообщений** | ECDSA (4) | QSI-2026-05983 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |
| **роль не определена** | ECDSA (8) | QSI-2026-05984 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | ECDSA (16) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (1), SHA-2 (1) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (1), SHA-2 (1) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- osv_advisories: npm/axios@1.12.2: 32 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories: npm/next@15.5.9: 32 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest
- osv_advisories: npm/next@15.3.8: 33 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-05990 | Обновите storybook до исправленной версии (10.6.2, 11.0.0-alpha.6, 8.6.19, 9.1.21). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-f2ph-cmg5-wxc8 (CVE-2026-114125). |
| P2 | QSI-2026-06013 | Обновите next до исправленной версии (15.5.28, 16.4.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2464-fhr4-w9xw. |
| P2 | QSI-2026-06016 | Обновите next до исправленной версии (15.5.24, 16.3.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2xp9-vwfh-vxw4. |
| P2 | QSI-2026-06034 | Обновите next-auth до исправленной версии (4.24.15, 5.0.0-beta.32). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7rqj-j65f-68wh (CVE-2026-73420). |
| P2 | QSI-2026-06035 | Обновите next-auth до исправленной версии (5.0.0-beta.32). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8fpg-xm3f-6cx3 (CVE-2026-73421). |
| P2 | QSI-2026-06040 | Обновите next до исправленной версии (15.5.28, 16.4.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2464-fhr4-w9xw. |
| P2 | QSI-2026-06043 | Обновите next до исправленной версии (15.5.24, 16.3.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2xp9-vwfh-vxw4. |
| P2 | QSI-2026-06071 | Обновите @auth/core до исправленной версии (0.41.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7rqj-j65f-68wh (CVE-2026-73420). |
| P2 | QSI-2026-06076 | Обновите @nuxt/devtools до исправленной версии (3.3.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-279x-mwfv-vcqv (CVE-2026-71319). |
| P2 | QSI-2026-05986 | Обновите uuid до исправленной версии (11.1.1, 12.0.1, 13.0.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w5hq-g745-h8pq (CVE-2026-41907, CVE-2026-41988). |
| P2 | QSI-2026-05989 | Обновите storybook до исправленной версии (10.1.10, 7.6.21, 8.6.15, 9.1.17). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8452-54wp-rmv6 (CVE-2025-68429). |
| P2 | QSI-2026-05991 | Обновите storybook до исправленной версии (10.2.10, 8.6.17, 9.1.19). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mjf5-7g4m-gx5w (CVE-2026-27148). |
| P2 | QSI-2026-05992 | Обновите storybook до исправленной версии (10.6.2, 11.0.0-alpha.6, 8.6.19, 9.1.21). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-px85-f4q5-jh77 (CVE-2026-114126). |
| P2 | QSI-2026-05993 | Обновите axios до исправленной версии (1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-35jp-ww65-95wh (CVE-2026-44494). |
| P2 | QSI-2026-05994 | Обновите axios до исправленной версии (0.31.1, 1.15.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3g43-6gmg-66jw (CVE-2026-44495). |
| P2 | QSI-2026-05998 | Обновите axios до исправленной версии (0.30.3, 1.13.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-43fc-jf86-j433 (CVE-2026-25639). |
| P2 | QSI-2026-06002 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-62hf-57xw-28j9 (CVE-2026-42039). |
| P2 | QSI-2026-06003 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-6chq-wfr3-2hj9 (CVE-2026-42035). |
| P2 | QSI-2026-06004 | Обновите axios до исправленной версии (1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-777c-7fjr-54vf (CVE-2026-44488). |
| P2 | QSI-2026-06009 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-hfxv-24rg-xrqf (CVE-2026-44496). |
| P2 | QSI-2026-06010 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j5f8-grm9-p9fc (CVE-2026-44486). |
| P2 | QSI-2026-06014 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-267c-6grr-h53f (CVE-2026-44575). |
| P2 | QSI-2026-06015 | Обновите next до исправленной версии (15.5.18, 16.2.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-26hh-7cqf-hhc6 (CVE-2026-45109). |
| P2 | QSI-2026-06017 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-36qx-fr4f-26g5 (CVE-2026-44573). |
| P2 | QSI-2026-06021 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-492v-c6pp-mqqv (CVE-2026-44574). |
| P2 | QSI-2026-06025 | Обновите next до исправленной версии (15.5.21, 16.2.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-89xv-2m56-2m9x (CVE-2026-64649). |
| P2 | QSI-2026-06026 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8h8q-6873-q5fj. |
| P2 | QSI-2026-06029 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c4j6-fc7j-m34r (CVE-2026-44578). |
| P2 | QSI-2026-06037 | Обновите next-auth до исправленной версии (4.24.15, 5.0.0-beta.32). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xmf8-cvqr-rfgj (CVE-2026-73418). |
| P2 | QSI-2026-06038 | Обновите @opennextjs/cloudflare до исправленной версии (1.20.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2vc4-c4r6-p6v6 (CVE-2026-100409). |
| P2 | QSI-2026-06039 | Обновите @opennextjs/cloudflare до исправленной версии (1.17.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c7mq-gh6q-6q7c (CVE-2025-6087, CVE-2026-3125). |
| P2 | QSI-2026-06041 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-267c-6grr-h53f (CVE-2026-44575). |
| P2 | QSI-2026-06042 | Обновите next до исправленной версии (15.5.18, 16.2.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-26hh-7cqf-hhc6 (CVE-2026-45109). |
| P2 | QSI-2026-06044 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-36qx-fr4f-26g5 (CVE-2026-44573). |
| P2 | QSI-2026-06052 | Обновите next до исправленной версии (15.5.21, 16.2.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-89xv-2m56-2m9x (CVE-2026-64649). |
| P2 | QSI-2026-06053 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8h8q-6873-q5fj. |
| P2 | QSI-2026-06056 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c4j6-fc7j-m34r (CVE-2026-44578). |
| P2 | QSI-2026-06061 | Обновите vite до исправленной версии (6.4.4, 7.3.7, 8.1.6, 8.2.4, 8.3.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-587h-7wmj-h5pm (CVE-2026-112942). |
| P2 | QSI-2026-06069 | Обновите figlet до исправленной версии (1.11.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-62ch-8vmq-8xm7 (CVE-2026-96780). |
| P2 | QSI-2026-06070 | Обновите zod до исправленной версии (4.6.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404). |
| P2 | QSI-2026-06073 | Обновите @auth/core до исправленной версии (0.41.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xmf8-cvqr-rfgj (CVE-2026-73418). |
| P2 | QSI-2026-06075 | Обновите @fastify/busboy до исправленной версии (3.2.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-x8mw-p69m-v3mx (CVE-2026-19481). |
| P2 | QSI-2026-05995 | Обновите axios до исправленной версии (0.31.0, 1.15.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3p68-rc4w-qgx5 (CVE-2025-62718). |
| P2 | QSI-2026-05996 | Обновите axios до исправленной версии (1.15.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3w6x-2g7m-8v23 (CVE-2026-42044). |
| P2 | QSI-2026-05997 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-42h9-826w-cgv3 (CVE-2026-67313). |
| P2 | QSI-2026-05999 | Обновите axios до исправленной версии (1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-445q-vr5w-6q77 (CVE-2026-42037). |
| P2 | QSI-2026-06000 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4hqw-qxg8-jxx2 (CVE-2026-101900). |
| P2 | QSI-2026-06001 | Обновите axios до исправленной версии (0.31.1, 1.15.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-5c9x-8gcm-mpgx (CVE-2026-42034). |
| P2 | QSI-2026-06005 | Обновите axios до исправленной версии (0.33.0, 1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7q8q-rj6j-mhjq (CVE-2026-67319). |
| P2 | QSI-2026-06006 | Обновите axios до исправленной версии (0.32.0, 1.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-898c-q2cr-xwhg (CVE-2026-44490). |
| P2 | QSI-2026-06007 | Обновите axios до исправленной версии (0.34.0, 1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9fr6-4gfg-395g (CVE-2026-101902). |
| P2 | QSI-2026-06008 | Обновите axios до исправленной версии (0.31.0, 1.15.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fvcv-3m26-pcqx (CVE-2026-40175). |
| P2 | QSI-2026-06011 | Обновите axios до исправленной версии (1.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j8rh-479h-cp32 (CVE-2026-101904). |
| P2 | QSI-2026-06012 | Обновите axios до исправленной версии (1.18.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-jqh4-m9w3-8hp9 (CVE-2026-67317). |
| P2 | QSI-2026-06019 | Обновите next до исправленной версии (15.5.14, 16.1.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3x4c-7xq6-9pq8 (CVE-2026-27980). |
| P2 | QSI-2026-06020 | Обновите next до исправленной версии (15.5.21, 16.2.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4633-3j49-mh5q (CVE-2026-64647). |
| P2 | QSI-2026-06022 | Обновите next до исправленной версии (15.5.21, 16.2.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4c39-4ccg-62r3 (CVE-2026-64646). |
| P2 | QSI-2026-06023 | Обновите next до исправленной версии (15.5.27, 16.3.8). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4jqv-mc3x-m676 (CVE-2026-94543). |
| P2 | QSI-2026-06024 | Обновите next до исправленной версии (15.5.21, 16.2.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-68g3-v927-f742 (CVE-2026-64648). |
| P2 | QSI-2026-06027 | Обновите next до исправленной версии (15.5.21, 16.2.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-955p-x3mx-jcvp (CVE-2026-64643). |
| P2 | QSI-2026-06028 | Обновите next до исправленной версии (15.5.10, 16.1.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9g9p-9gw9-jx7f (CVE-2025-59471). |
| P2 | QSI-2026-06030 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-ffhc-5mcf-pf4q (CVE-2026-44581). |
| P2 | QSI-2026-06031 | Обновите next до исправленной версии (15.5.13, 16.1.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-ggv3-7p47-pfv8 (CVE-2026-29057). |
| P2 | QSI-2026-06032 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-gx5p-jg67-6x7h (CVE-2026-44580). |
| P2 | QSI-2026-06033 | Обновите next-auth до исправленной версии (4.24.12, 5.0.0-beta.30). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-5jpx-9hw9-2fx4. |
| P2 | QSI-2026-06036 | Обновите next-auth до исправленной версии (4.24.15, 5.0.0-beta.32). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-x445-f3h2-j279 (CVE-2026-73419). |
| P2 | QSI-2026-06046 | Обновите next до исправленной версии (15.5.14, 16.1.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3x4c-7xq6-9pq8 (CVE-2026-27980). |
| P2 | QSI-2026-06047 | Обновите next до исправленной версии (14.2.32, 15.4.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4342-x723-ch2f (CVE-2025-57822). |
| P2 | QSI-2026-06048 | Обновите next до исправленной версии (15.5.21, 16.2.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4633-3j49-mh5q (CVE-2026-64647). |
| P2 | QSI-2026-06049 | Обновите next до исправленной версии (15.5.21, 16.2.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4c39-4ccg-62r3 (CVE-2026-64646). |
| P2 | QSI-2026-06050 | Обновите next до исправленной версии (15.5.27, 16.3.8). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4jqv-mc3x-m676 (CVE-2026-94543). |
| P2 | QSI-2026-06051 | Обновите next до исправленной версии (15.5.21, 16.2.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-68g3-v927-f742 (CVE-2026-64648). |
| P2 | QSI-2026-06054 | Обновите next до исправленной версии (15.5.21, 16.2.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-955p-x3mx-jcvp (CVE-2026-64643). |
| P2 | QSI-2026-06055 | Обновите next до исправленной версии (15.5.10, 16.1.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9g9p-9gw9-jx7f (CVE-2025-59471). |
| P2 | QSI-2026-06057 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-ffhc-5mcf-pf4q (CVE-2026-44581). |
| P2 | QSI-2026-06058 | Обновите next до исправленной версии (14.2.31, 15.4.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-g5qg-72qw-gw5v (CVE-2025-57752). |
| P2 | QSI-2026-06059 | Обновите next до исправленной версии (15.5.13, 16.1.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-ggv3-7p47-pfv8 (CVE-2026-29057). |
| P2 | QSI-2026-06060 | Обновите vite до исправленной версии (6.4.2, 7.3.2, 8.0.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4w7w-66w2-5vf9 (CVE-2026-39365). |
| P2 | QSI-2026-06062 | Обновите vite до исправленной версии (6.4.4, 7.3.7, 8.1.6, 8.2.4, 8.3.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-698v-4r3x-3vcv (CVE-2026-112943). |
| P2 | QSI-2026-06063 | Обновите vite до исправленной версии (5.4.21, 6.4.1, 7.0.8, 7.1.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-93m4-6634-74q7 (CVE-2025-62522). |
| P2 | QSI-2026-06065 | Обновите vite до исправленной версии (6.4.3, 7.3.5, 8.0.16). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fx2h-pf6j-xcff (CVE-2026-53571). |
| P2 | QSI-2026-06066 | Обновите vite до исправленной версии (6.4.4, 7.3.7, 8.1.6, 8.2.4, 8.3.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-r825-w8mm-5pxw (CVE-2026-112944). |
| P2 | QSI-2026-06067 | Обновите vite до исправленной версии (6.4.4, 7.3.7, 8.1.6, 8.2.4, 8.3.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rq7h-c2jc-7f22 (CVE-2026-112946). |
| P2 | QSI-2026-06068 | Обновите vite до исправленной версии (6.4.3, 7.3.5, 8.0.16). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-v6wh-96g9-6wx3 (CVE-2026-53632). |
| P2 | QSI-2026-06072 | Обновите @auth/core до исправленной версии (0.41.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-x445-f3h2-j279 (CVE-2026-73419). |
| P2 | QSI-2026-06074 | Обновите @fastify/busboy до исправленной версии (3.2.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-gxm5-99cw-xjw9 (CVE-2026-74866). |
| P2 | QSI-2026-06077 | Обновите @opentelemetry/core до исправленной версии (2.8.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8988-4f7v-96qf (CVE-2026-54285). |
| P2 | QSI-2026-06078 | Обновите @opentelemetry/instrumentation-knex до исправленной версии (0.65.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qqmp-wf37-98f9 (CVE-2026-104872). |
| P2 | QSI-2026-06079 | Обновите @opentelemetry/instrumentation-mongoose до исправленной версии (0.67.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qqmp-wf37-98f9 (CVE-2026-104872). |
| P2 | QSI-2026-06080 | Обновите @opentelemetry/instrumentation-mysql2 до исправленной версии (0.67.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qqmp-wf37-98f9 (CVE-2026-104872). |
| P2 | QSI-2026-06081 | Обновите @opentelemetry/instrumentation-mysql до исправленной версии (0.67.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qqmp-wf37-98f9 (CVE-2026-104872). |
| P2 | QSI-2026-06082 | Обновите @opentelemetry/instrumentation-pg до исправленной версии (0.73.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qqmp-wf37-98f9 (CVE-2026-104872). |
| P2 | QSI-2026-06083 | Обновите @opentelemetry/instrumentation-tedious до исправленной версии (0.40.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qqmp-wf37-98f9 (CVE-2026-104872). |
| P2 | QSI-2026-06084 | Обновите @parcel/reporter-dev-server до исправленной версии (2.16.4). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qm9p-f9j5-w83w (CVE-2025-56648). |
| P2 | QSI-2026-05987 | Обновите webpack до исправленной версии (5.104.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-38r7-794h-5758 (CVE-2025-68157). |
| P2 | QSI-2026-05988 | Обновите webpack до исправленной версии (5.104.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8fgc-7cc6-rx7x (CVE-2025-68458). |
| P2 | QSI-2026-06018 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3g8h-86w9-wvmq (CVE-2026-44572). |
| P2 | QSI-2026-06045 | Обновите next до исправленной версии (15.5.16, 16.2.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3g8h-86w9-wvmq (CVE-2026-44572). |
| P2 | QSI-2026-06064 | Обновите vite до исправленной версии (6.4.4, 7.3.7, 8.1.6, 8.2.4, 8.3.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9jrq-w75r-8gcw (CVE-2026-112945). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-05983 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-05984 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-05983 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05984 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06085 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |

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
7. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
8. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
9. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
10. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
11. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
12. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
13. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
14. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
15. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
16. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
17. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
18. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
19. OSV advisory GHSA-2464-fhr4-w9xw — OSV.dev. <https://osv.dev/vulnerability/GHSA-2464-fhr4-w9xw> (modified 2026-10-22T16:00:09.125335909Z)
20. OSV advisory GHSA-267c-6grr-h53f — OSV.dev. <https://osv.dev/vulnerability/GHSA-267c-6grr-h53f> (modified 2026-09-10T03:51:03.970900692Z)
21. OSV advisory GHSA-26hh-7cqf-hhc6 — OSV.dev. <https://osv.dev/vulnerability/GHSA-26hh-7cqf-hhc6> (modified 2026-09-10T03:50:45.324330779Z)
22. OSV advisory GHSA-279x-mwfv-vcqv — OSV.dev. <https://osv.dev/vulnerability/GHSA-279x-mwfv-vcqv> (modified 2026-08-20T05:15:07.135772644Z)
23. OSV advisory GHSA-2vc4-c4r6-p6v6 — OSV.dev. <https://osv.dev/vulnerability/GHSA-2vc4-c4r6-p6v6> (modified 2026-10-15T20:30:05.349670038Z)
24. OSV advisory GHSA-2xp9-vwfh-vxw4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-2xp9-vwfh-vxw4> (modified 2026-09-08T21:30:04.767189946Z)
25. OSV advisory GHSA-35jp-ww65-95wh — OSV.dev. <https://osv.dev/vulnerability/GHSA-35jp-ww65-95wh> (modified 2026-09-10T03:51:04.268287831Z)
26. OSV advisory GHSA-36qx-fr4f-26g5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-36qx-fr4f-26g5> (modified 2026-09-10T03:51:04.325298044Z)
27. OSV advisory GHSA-38r7-794h-5758 — OSV.dev. <https://osv.dev/vulnerability/GHSA-38r7-794h-5758> (modified 2026-09-10T03:50:33.757470252Z)
28. OSV advisory GHSA-3g43-6gmg-66jw — OSV.dev. <https://osv.dev/vulnerability/GHSA-3g43-6gmg-66jw> (modified 2026-09-10T03:51:04.440180855Z)
29. OSV advisory GHSA-3g8h-86w9-wvmq — OSV.dev. <https://osv.dev/vulnerability/GHSA-3g8h-86w9-wvmq> (modified 2026-09-10T03:51:04.422954573Z)
30. OSV advisory GHSA-3p68-rc4w-qgx5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-3p68-rc4w-qgx5> (modified 2026-09-10T03:50:42.452672741Z)
31. OSV advisory GHSA-3w6x-2g7m-8v23 — OSV.dev. <https://osv.dev/vulnerability/GHSA-3w6x-2g7m-8v23> (modified 2026-09-10T03:50:45.398396828Z)
32. OSV advisory GHSA-3x4c-7xq6-9pq8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-3x4c-7xq6-9pq8> (modified 2026-09-10T03:50:36.950018769Z)
33. OSV advisory GHSA-42h9-826w-cgv3 — OSV.dev. <https://osv.dev/vulnerability/GHSA-42h9-826w-cgv3> (modified 2026-09-10T03:51:10.187294734Z)
34. OSV advisory GHSA-4342-x723-ch2f — OSV.dev. <https://osv.dev/vulnerability/GHSA-4342-x723-ch2f> (modified 2026-09-10T03:50:26.545785200Z)
35. OSV advisory GHSA-43fc-jf86-j433 — OSV.dev. <https://osv.dev/vulnerability/GHSA-43fc-jf86-j433> (modified 2026-09-10T03:50:34.100599628Z)
36. OSV advisory GHSA-445q-vr5w-6q77 — OSV.dev. <https://osv.dev/vulnerability/GHSA-445q-vr5w-6q77> (modified 2026-09-10T03:50:45.396631689Z)
37. OSV advisory GHSA-4633-3j49-mh5q — OSV.dev. <https://osv.dev/vulnerability/GHSA-4633-3j49-mh5q> (modified 2026-09-10T03:50:51.390157243Z)
38. OSV advisory GHSA-492v-c6pp-mqqv — OSV.dev. <https://osv.dev/vulnerability/GHSA-492v-c6pp-mqqv> (modified 2026-09-10T03:51:04.588942784Z)
39. OSV advisory GHSA-4c39-4ccg-62r3 — OSV.dev. <https://osv.dev/vulnerability/GHSA-4c39-4ccg-62r3> (modified 2026-09-10T03:50:51.398762372Z)
40. OSV advisory GHSA-4hqw-qxg8-jxx2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-4hqw-qxg8-jxx2> (modified 2026-09-30T15:46:17.701967512Z)
41. OSV advisory GHSA-4jqv-mc3x-m676 — OSV.dev. <https://osv.dev/vulnerability/GHSA-4jqv-mc3x-m676> (modified 2026-10-07T20:45:06.342983181Z)
42. OSV advisory GHSA-4w7w-66w2-5vf9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-4w7w-66w2-5vf9> (modified 2026-09-10T03:50:42.779400319Z)
43. OSV advisory GHSA-587h-7wmj-h5pm — OSV.dev. <https://osv.dev/vulnerability/GHSA-587h-7wmj-h5pm> (modified 2026-10-20T20:00:04.608979840Z)
44. OSV advisory GHSA-5c9x-8gcm-mpgx — OSV.dev. <https://osv.dev/vulnerability/GHSA-5c9x-8gcm-mpgx> (modified 2026-09-10T03:50:45.707956373Z)
45. OSV advisory GHSA-5jpx-9hw9-2fx4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-5jpx-9hw9-2fx4> (modified 2026-09-10T03:50:29.281362473Z)
46. OSV advisory GHSA-62ch-8vmq-8xm7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-62ch-8vmq-8xm7> (modified 2026-10-02T23:01:22.706221290Z)
47. OSV advisory GHSA-62hf-57xw-28j9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-62hf-57xw-28j9> (modified 2026-09-10T03:50:45.703789635Z)
48. OSV advisory GHSA-68g3-v927-f742 — OSV.dev. <https://osv.dev/vulnerability/GHSA-68g3-v927-f742> (modified 2026-09-10T03:51:10.587986551Z)
49. OSV advisory GHSA-698v-4r3x-3vcv — OSV.dev. <https://osv.dev/vulnerability/GHSA-698v-4r3x-3vcv> (modified 2026-10-20T18:45:09.467993691Z)
50. OSV advisory GHSA-6chq-wfr3-2hj9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-6chq-wfr3-2hj9> (modified 2026-09-10T03:51:04.772235088Z)
51. OSV advisory GHSA-777c-7fjr-54vf — OSV.dev. <https://osv.dev/vulnerability/GHSA-777c-7fjr-54vf> (modified 2026-09-10T03:50:48.738717543Z)
52. OSV advisory GHSA-7q8q-rj6j-mhjq — OSV.dev. <https://osv.dev/vulnerability/GHSA-7q8q-rj6j-mhjq> (modified 2026-09-10T03:51:10.872027953Z)
53. OSV advisory GHSA-7rqj-j65f-68wh — OSV.dev. <https://osv.dev/vulnerability/GHSA-7rqj-j65f-68wh> (modified 2026-09-10T03:50:51.566945120Z)
54. OSV advisory GHSA-8452-54wp-rmv6 — OSV.dev. <https://osv.dev/vulnerability/GHSA-8452-54wp-rmv6> (modified 2026-09-10T03:50:31.796824882Z)
55. OSV advisory GHSA-8988-4f7v-96qf — OSV.dev. <https://osv.dev/vulnerability/GHSA-8988-4f7v-96qf> (modified 2026-09-10T03:50:48.883260062Z)
56. OSV advisory GHSA-898c-q2cr-xwhg — OSV.dev. <https://osv.dev/vulnerability/GHSA-898c-q2cr-xwhg> (modified 2026-09-10T03:51:04.811379218Z)
57. OSV advisory GHSA-89xv-2m56-2m9x — OSV.dev. <https://osv.dev/vulnerability/GHSA-89xv-2m56-2m9x> (modified 2026-09-10T03:50:51.547474623Z)
58. OSV advisory GHSA-8fgc-7cc6-rx7x — OSV.dev. <https://osv.dev/vulnerability/GHSA-8fgc-7cc6-rx7x> (modified 2026-09-10T03:50:34.472343977Z)
59. OSV advisory GHSA-8fpg-xm3f-6cx3 — OSV.dev. <https://osv.dev/vulnerability/GHSA-8fpg-xm3f-6cx3> (modified 2026-08-12T20:56:01.891204Z)
60. OSV advisory GHSA-8h8q-6873-q5fj — OSV.dev. <https://osv.dev/vulnerability/GHSA-8h8q-6873-q5fj> (modified 2026-09-10T03:51:04.979274056Z)
61. OSV advisory GHSA-93m4-6634-74q7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-93m4-6634-74q7> (modified 2026-09-10T03:50:29.574857832Z)
62. OSV advisory GHSA-955p-x3mx-jcvp — OSV.dev. <https://osv.dev/vulnerability/GHSA-955p-x3mx-jcvp> (modified 2026-09-10T03:51:11.198992864Z)
63. OSV advisory GHSA-9fr6-4gfg-395g — OSV.dev. <https://osv.dev/vulnerability/GHSA-9fr6-4gfg-395g> (modified 2026-09-30T15:30:03.718390401Z)
64. OSV advisory GHSA-9g9p-9gw9-jx7f — OSV.dev. <https://osv.dev/vulnerability/GHSA-9g9p-9gw9-jx7f> (modified 2026-09-10T03:50:59.013924260Z)
65. OSV advisory GHSA-9jrq-w75r-8gcw — OSV.dev. <https://osv.dev/vulnerability/GHSA-9jrq-w75r-8gcw> (modified 2026-10-21T17:00:26.569382874Z)
66. OSV advisory GHSA-c4j6-fc7j-m34r — OSV.dev. <https://osv.dev/vulnerability/GHSA-c4j6-fc7j-m34r> (modified 2026-09-10T03:50:46.499274814Z)
67. OSV advisory GHSA-c7mq-gh6q-6q7c — OSV.dev. <https://osv.dev/vulnerability/GHSA-c7mq-gh6q-6q7c> (modified 2026-03-16T03:05:38.239106Z)
68. OSV advisory GHSA-f2ph-cmg5-wxc8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-f2ph-cmg5-wxc8> (modified 2026-10-21T17:35:19.889160714Z)
69. OSV advisory GHSA-ffhc-5mcf-pf4q — OSV.dev. <https://osv.dev/vulnerability/GHSA-ffhc-5mcf-pf4q> (modified 2026-09-10T03:51:05.447940563Z)
70. OSV advisory GHSA-fvcv-3m26-pcqx — OSV.dev. <https://osv.dev/vulnerability/GHSA-fvcv-3m26-pcqx> (modified 2026-09-10T03:50:44.273401032Z)
71. OSV advisory GHSA-fx2h-pf6j-xcff — OSV.dev. <https://osv.dev/vulnerability/GHSA-fx2h-pf6j-xcff> (modified 2026-10-27T15:15:07.885624041Z)
72. OSV advisory GHSA-g5qg-72qw-gw5v — OSV.dev. <https://osv.dev/vulnerability/GHSA-g5qg-72qw-gw5v> (modified 2026-09-10T03:50:26.953168554Z)
73. OSV advisory GHSA-ggv3-7p47-pfv8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-ggv3-7p47-pfv8> (modified 2026-09-10T03:50:39.201962373Z)
74. OSV advisory GHSA-gx5p-jg67-6x7h — OSV.dev. <https://osv.dev/vulnerability/GHSA-gx5p-jg67-6x7h> (modified 2026-09-10T03:51:05.785143220Z)
75. OSV advisory GHSA-gxm5-99cw-xjw9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-gxm5-99cw-xjw9> (modified 2026-10-05T22:45:04.558942837Z)
76. OSV advisory GHSA-hfxv-24rg-xrqf — OSV.dev. <https://osv.dev/vulnerability/GHSA-hfxv-24rg-xrqf> (modified 2026-09-10T03:50:49.732285826Z)
77. OSV advisory GHSA-j5f8-grm9-p9fc — OSV.dev. <https://osv.dev/vulnerability/GHSA-j5f8-grm9-p9fc> (modified 2026-09-10T03:50:50.017253448Z)
78. OSV advisory GHSA-j8rh-479h-cp32 — OSV.dev. <https://osv.dev/vulnerability/GHSA-j8rh-479h-cp32> (modified 2026-09-30T15:46:18.108444439Z)
79. OSV advisory GHSA-jqh4-m9w3-8hp9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-jqh4-m9w3-8hp9> (modified 2026-09-10T03:50:52.448472902Z)
80. OSV advisory GHSA-mjf5-7g4m-gx5w — OSV.dev. <https://osv.dev/vulnerability/GHSA-mjf5-7g4m-gx5w> (modified 2026-02-26T15:32:56.650508Z)
81. OSV advisory GHSA-mrhx-c7xc-m3w5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-mrhx-c7xc-m3w5> (modified 2026-10-23T18:30:09.376405885Z)
82. OSV advisory GHSA-px85-f4q5-jh77 — OSV.dev. <https://osv.dev/vulnerability/GHSA-px85-f4q5-jh77> (modified 2026-10-22T16:45:03.723842082Z)
83. OSV advisory GHSA-qm9p-f9j5-w83w — OSV.dev. <https://osv.dev/vulnerability/GHSA-qm9p-f9j5-w83w> (modified 2026-04-13T19:02:07.652067Z)
84. OSV advisory GHSA-qqmp-wf37-98f9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qqmp-wf37-98f9> (modified 2026-10-05T23:00:05.311085601Z)
85. OSV advisory GHSA-r825-w8mm-5pxw — OSV.dev. <https://osv.dev/vulnerability/GHSA-r825-w8mm-5pxw> (modified 2026-10-20T20:00:04.608907013Z)
86. OSV advisory GHSA-rq7h-c2jc-7f22 — OSV.dev. <https://osv.dev/vulnerability/GHSA-rq7h-c2jc-7f22> (modified 2026-10-21T17:00:06.336868869Z)
87. OSV advisory GHSA-v6wh-96g9-6wx3 — OSV.dev. <https://osv.dev/vulnerability/GHSA-v6wh-96g9-6wx3> (modified 2026-09-10T03:50:50.705036566Z)
88. OSV advisory GHSA-w5hq-g745-h8pq — OSV.dev. <https://osv.dev/vulnerability/GHSA-w5hq-g745-h8pq> (modified 2026-09-10T03:51:03.663336650Z)
89. OSV advisory GHSA-x445-f3h2-j279 — OSV.dev. <https://osv.dev/vulnerability/GHSA-x445-f3h2-j279> (modified 2026-09-10T03:50:53.095011411Z)
90. OSV advisory GHSA-x8mw-p69m-v3mx — OSV.dev. <https://osv.dev/vulnerability/GHSA-x8mw-p69m-v3mx> (modified 2026-10-02T23:30:05.651087437Z)
91. OSV advisory GHSA-xmf8-cvqr-rfgj — OSV.dev. <https://osv.dev/vulnerability/GHSA-xmf8-cvqr-rfgj> (modified 2026-09-10T03:51:12.549867672Z)
92. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
93. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
94. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
95. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| Keccak-256 | Keccak-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 1 | 1 | packages/siwx/src/verifiers/TronVerifier.ts:89 |
| SHA-2 | SHA-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 1 | 1 | apps/browser-extension/src/core/TronProvider.ts:24 |
| Crypto library | 1.0.3 | tweetnacl (TweetNaCl) | н/п | допустимо | 3 | 3 | apps/browser-extension/package.json; packages/siwx/package.json; pnpm-lock.yaml |
| Crypto library | 1.7.2 | @noble/secp256k1 (noble-curves) | н/п | допустимо | 2 | 2 | apps/browser-extension/package.json; pnpm-lock.yaml |
| Crypto library | 1.9.2 | @noble/curves (noble-curves) | н/п | допустимо | 2 | 2 | apps/browser-extension/package.json; pnpm-lock.yaml |
| Crypto library | 1.98.4 | @solana/web3.js (Solana web3.js) | н/п | допустимо | 5 | 5 | apps/browser-extension/package.json; apps/laboratory/package.json; packages/adapters/solana/package.json |
| Crypto library | 6.1.7 | bitcoinjs-lib (bitcoinjs-lib) | н/п | допустимо | 3 | 3 | apps/browser-extension/package.json; packages/adapters/bitcoin/package.json; pnpm-lock.yaml |
| Crypto library | 6.14.0 | ethers (ethers.js) | н/п | допустимо | 2 | 2 | apps/laboratory/package.json; pnpm-lock.yaml |
| Crypto library | 7.0.0-rc.0 | bitcoinjs-lib (bitcoinjs-lib) | н/п | допустимо | 2 | 2 | apps/laboratory/package.json; pnpm-lock.yaml |
| Crypto library | >=6 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | packages/adapters/ethers/package.json |
| Crypto library | >=4.1 <6.0.0 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | packages/adapters/ethers5/package.json |
| Crypto library | 1.1.5 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.2.0 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.3.2 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.3.3 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.4.0 | node-forge (node-forge) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.4.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.4.2 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.5.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.7.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.7.1 | @noble/secp256k1 (noble-curves) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.7.1 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.7.2 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.8.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.8.0 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.8.1 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.8.2 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.9.1 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 1.9.7 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 2.4.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 3.8.1 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 5.0.2 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 5.10.0 | jose (jose (Node)) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 5.8.0 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 6.17.0 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 6.2.12 | jose (jose (Node)) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 6.6.1 | elliptic (elliptic (Node)) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| Crypto library | 9.0.3 | jsonwebtoken (jsonwebtoken (Node)) | н/п | допустимо | 1 | 1 | pnpm-lock.yaml |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 8 | 8 | apps/browser-extension/src/core/BitcoinProvider.ts:1; apps/laboratory/src/components/Wagmi/WagmiRequestPermissionsAsyncTest.tsx:75; apps/laboratory/src/utils/BitcoinUtil.ts:1 |
| ECDSA |  |  | уязвим (Шор) | допустимо | 3 | 3 | apps/browser-extension/src/core/transport.ts:23; apps/gallery/utils/PresetUtils.ts:367; apps/laboratory/src/components/Ethers/EthersSignTypedDataTest.tsx:58 |
| ECDSA | P-256 |  | уязвим (Шор) | допустимо | 5 | 5 | apps/laboratory/src/components/Wagmi/WagmiRequestPermissionsSyncTest.tsx:94; apps/laboratory/src/utils/EncodingUtils.ts:11; packages/experimental/src/smart-session/helper/index.ts:143 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| .size-limit.js | 1844 | `3ad2476ef0f2fd09154b91314ffa7becd75d054654c6f775fbe802671d70fdd2` | 0 |
| apps/browser-extension/package.json | 2376 | `557f066b84ce9cba239cdc92e7a9d2d7b98eaf83c4e09f39245d4172ac2d1494` | 0 |
| apps/browser-extension/src/App.tsx | 662 | `cdf0899818f61cce7b1e969f4ca4408b3deb0ceec32e6e0815765660ae206bf7` | 0 |
| apps/browser-extension/src/background.ts | 715 | `1c2b3fc7a7447ed5d22e4aff29bc77e568a827e19aba7aa5648d8adf918472af` | 0 |
| apps/browser-extension/src/components/ArrowRightUp/index.tsx | 897 | `028d6e1d7735e721bc86e4cf92baa4668dea69b4477cc7c56578222582cda265` | 0 |
| apps/browser-extension/src/components/Box/index.tsx | 1271 | `d47577c04cbd83f957b128e22f2bfcf898bf3c0dff2be8914d7ad10ba1690af5` | 0 |
| apps/browser-extension/src/components/ChainTabs/index.tsx | 1916 | `81386db567357ff506fd0c929c3dd83ae02178e0b1ddb56f7b341bde03bb9371` | 0 |
| apps/browser-extension/src/components/Checkmark/index.tsx | 1067 | `a8f607517d3bde6ee5a23fa138baaa31d8dd3e9b6e4d92f04b517a1f61b547f9` | 0 |
| apps/browser-extension/src/components/Copy/index.tsx | 862 | `515cb4eca69b9958a4137e422c8d72b848d1a2fca036caa0d70db364e8f38f51` | 0 |
| apps/browser-extension/src/components/IconButton/index.tsx | 1276 | `d7f41a3f553e84e8874397deb5dbefd2f2e22bc66c9d9657e177dce4771669e1` | 0 |
| apps/browser-extension/src/components/Icons/Btc.tsx | 1493 | `7c897cae66efc9fc7b294b5eefbdb32dae6eeac8bef32ee889f14ac758c6fbf0` | 0 |
| apps/browser-extension/src/components/Icons/Eth.tsx | 878 | `1eae7c6c55200e6dc9860e47b60536b9d4754d6e8b7f1d510097ce0ed0b560d1` | 0 |
| apps/browser-extension/src/components/Icons/Sol.tsx | 2116 | `b9ab6ed476cdeb4f7d1ae2bc0f43edc70fb45da9b7e5aab7eab6303df10a1cc6` | 0 |
| apps/browser-extension/src/components/Icons/Ton.tsx | 813 | `1d0f4138e68bedab72eac0b6412470dc0eab3cfec2a0681e296e4978d185412a` | 0 |
| apps/browser-extension/src/components/Icons/Trx.tsx | 709 | `c45b88ca2a835cc55aa6601e74d6b9b2efcbe00255cfcca6a92659dfc75da338` | 0 |
| apps/browser-extension/src/components/Logo/index.tsx | 2919 | `69ac7f27782f1eee236562267e516e36d3fe39dce543fd81cc1ba01de16a5eb5` | 0 |
| apps/browser-extension/src/components/Switch/index.tsx | 2172 | `c68b1dd403f7a1ed255c1d622eba8a90e3af2d90662308fbd0b00ccabaffdf6c` | 0 |
| apps/browser-extension/src/components/Text/index.tsx | 293 | `0de6af8584f1a5e374ae777d4913fab55cc452e1e8260b2400fce21cc8a2e95c` | 0 |
| apps/browser-extension/src/components/Token/index.tsx | 2027 | `9a74f9c340218be3c8c57471fb297019d60bd0b9a191e88fc2c42e2050f4c93c` | 0 |
| apps/browser-extension/src/components/Zorb/index.tsx | 1039 | `2be35f3d6c9a80f8cff01fe94f7d4de419659ef1bacaf13867081cfe3893faa5` | 0 |
| apps/browser-extension/src/content.ts | 27 | `4a1ebe3871654d570e2d52899b6d0e7c800cc406b486beff4c5e269b968935eb` | 0 |
| apps/browser-extension/src/core/BitcoinProvider.ts | 5020 | `dd35b72c93c633589b491ce16c3619fc85c3382d7588ce5175801eef34ebb2bf` | 0 |
| apps/browser-extension/src/core/EvmProvider.ts | 344 | `4f3224cd905321657de52d058050f73e664e7a352a8b712e611d6ce13addcc52` | 0 |
| apps/browser-extension/src/core/SolanaProvider.ts | 3219 | `e9b59f42e6a7a452ac953b8494bb0a0533b38f4bae67eb0791c0d9d137723cb5` | 0 |
| apps/browser-extension/src/core/TonProvider.ts | 10285 | `be4d8bf15200a4c4547b01a4545049d381a5c4532990db905d59a81860a45f54` | 0 |
| apps/browser-extension/src/core/TronProvider.ts | 5702 | `3ee9c96c6c43075b3768a0063f1a639f99f4458bf95b29bc9f11c546bddd4630` | 0 |
| apps/browser-extension/src/core/transport.ts | 2836 | `9bd6a1b5822641acfec1ec3819f80911f3c9ad662e2ec1a747408a707cae1ac1` | 0 |
| apps/browser-extension/src/core/wagmi.ts | 455 | `d35134aa8bcbaa32641e713632751cb5c7df15e62fee509e0480314aa7c25e08` | 0 |
| apps/browser-extension/src/css/atoms.ts | 629 | `d2c658c2d1e190dfa891402bcc05e5fdf0b3ffc599c9dc3f758301b952b2fedd` | 0 |
| apps/browser-extension/src/css/reset.css.ts | 231 | `05ab7b92f8074ccb8157b508801d339c2aabf092b303aad281374b30f07c2a95` | 0 |
| apps/browser-extension/src/css/sprinkless.css.ts | 3775 | `2d084eda8041fd95f72572e982c9cb4b3a3ffa762d093c212933a979d4741750` | 0 |
| apps/browser-extension/src/css/touchableStyles.css.ts | 1243 | `0cef0bac773fc844b5adbb6519b2dd742cfb5d9b8234981ce037ab53acc3acf7` | 0 |
| apps/browser-extension/src/css/touchableStyles.ts | 340 | `6ba5be2455acf22575f3ed2de997bee9587aa1163cc89c6f54041e4c4eb168c6` | 0 |
| apps/browser-extension/src/globals.css.ts | 300 | `f1f833c3309f335ba632b83b44d807487dfd06ebb80120b50aa1dd5c725eb758` | 0 |
| apps/browser-extension/src/hooks/useBalance.ts | 2038 | `e536daafe3ed1a050ed100d358faee786ca531ce3e579b886b62307079971fb9` | 0 |
| apps/browser-extension/src/index.tsx | 290 | `73552dc22c819fa9c248a9ee010968321cda240772f64c6de4a42a9309677150` | 0 |
| apps/browser-extension/src/inpage.ts | 1563 | `cd0bb752b5e8ea46b8c0f10124ac9040fa10cef75e61cbcd1fec5c6fa18ff122` | 0 |
| apps/browser-extension/src/pages/Home/index.tsx | 4063 | `1693f27a4eb91fb139888f570f3b9abf9eed088c9d79b020261bf7d1e7101681` | 0 |
| apps/browser-extension/src/utils/AccountUtil.ts | 355 | `c4bee3d18c2a10b45ef61d2b8b05d50355996509cc7ac2bae7ac0c8c66b70886` | 0 |
| apps/browser-extension/src/utils/ConstantsUtil.ts | 8629 | `2e55c1d2bf49f842bc28dc909a90b80b0b517710d8668fcfc572d1d586d21ad9` | 0 |
| apps/browser-extension/src/utils/HelperUtil.ts | 131 | `2f734f585aa132285d14e77e3104862695dcd74892a632f1842f59d0e0f7707c` | 0 |
| apps/browser-extension/src/webapp.tsx | 286 | `42951b7fc2703f17d2b967eb822ee3eaaa05d1ca2f276fb16360906e4d4aa255` | 0 |
| apps/browser-extension/webpack.config.js | 3119 | `a9da1bfabda189c1501fddf8ec95cd8c0975f7c89e763e1d5e31fabba789d75a` | 0 |
| apps/gallery/.storybook/main.ts | 701 | `39f0b05fb42d02d1644599f19b988b2b73b1d70f8a5581e8136da294f3745e54` | 0 |
| apps/gallery/.storybook/manager.ts | 883 | `f5e88116cc1e15138b4ff16af00a4cc61b775f953b5c03415d947ed5654f06be` | 0 |
| apps/gallery/.storybook/preview.tsx | 1201 | `bbb02a5c284d64d4079ac3641454b1ecd1f6afa24cfa83b8c9fc45dce54a3cc0` | 0 |
| apps/gallery/components/gallery-container/index.ts | 820 | `e817d11b81f807e036d51693cef5d6c6627d0f0d4cde61911f8ddb448415047e` | 0 |
| apps/gallery/components/gallery-container/styles.ts | 237 | `c276e731ea5d3a244b1c50a99d00adf4d78d50a7b462569be28018cba771157e` | 0 |
| apps/gallery/components/gallery-placeholder/index.ts | 1060 | `881a77ab3acec580f333fca08263441060254080cf74ac20f78a27aa21a07f07` | 0 |
| apps/gallery/components/gallery-placeholder/styles.ts | 620 | `9a9128de18e72e0467a4715c733ea66c7a3946ca64083a772d70059dc0d1c2e4` | 0 |
| apps/gallery/package.json | 788 | `bee2891277528022b9f16e7337c20575c109823ce9c9d9062476e8cb41d727a1` | 0 |
| apps/gallery/stories/partials/w3m-router-container.components.ts | 3346 | `d6b7d46cca4e03d9c4fc31d565efabe13c52c2339d4d076c7c6cba81b2e3c26e` | 0 |
| apps/gallery/utils/PresetUtils.ts | 9878 | `ffbaf9541fe1f3c8681000ac738f8d3c79737edd97c71e34b7f4da60cb47e074` | 0 |
| apps/laboratory/app/api/auth/[...nextauth]/route.ts | 117 | `14dbd3de8022c1ec2e32daa0226eee1d6b9c5d10f1d827433d44e40c5939e7e4` | 0 |
| apps/laboratory/app/appkit/page.tsx | 1958 | `de352f5eb8ecc2ce8eeec3815eb2b8ea753d98a8fd50f1893f08c8b7f2c63a7f` | 0 |
| apps/laboratory/app/appkit-core/constants.ts | 1491 | `9f90aec1a25a2fa379482f750b3c6ed4e6d7507d1203a27c66bef86dda92b199` | 0 |
| apps/laboratory/app/appkit-core/page.tsx | 940 | `3ef099ab9f256cf18b4509543039543acdc2990ad9b83dfad2f80e3cb9225b85` | 0 |
| apps/laboratory/app/appkit-core/sign-client/page.tsx | 10191 | `39e74fdd0f0c62ce37866b1a5a4eae16833ba53c156ab57fa65dc94722d838a7` | 0 |
| apps/laboratory/app/appkit-core/universal-connector/page.tsx | 6869 | `c55870ea8b56f696354ae10790dba1ac77e23ab620d0a2b582c92a67b7e31a1c` | 0 |
| apps/laboratory/app/appkit-core/universal-provider/page.tsx | 10434 | `88f7b9d1f06c1744c77e8e9242b5505246b61964b5273ed9502d90e01406a2ed` | 0 |
| apps/laboratory/app/appkit-core/wallet-standard/page.tsx | 10592 | `77b458dc28121faba48eb60a3f0f02283cca72fafad03011ecd7aec6f8580490` | 0 |
| apps/laboratory/app/layout.tsx | 831 | `e99d85549f93abc2c7de712f9d045b6acce44c116a7bc4ac72dcdaab8fa43498` | 0 |
| apps/laboratory/app/manifest.ts | 511 | `cb3e0680aec5263a8ee09b2725bd96e799306464c63bd2428a6224aa03c844b7` | 0 |
| apps/laboratory/app/page.tsx | 1673 | `04cb66d580dd3d3d4e509317e56a052f5f5e9fd1d037a85891f18f8f5655d2f5` | 0 |
| apps/laboratory/auth.ts | 2208 | `e5ccc88fe95a8f328d77e68dd1bf1607283d800e01667d6614f0d4ec5b20b80e` | 0 |
| apps/laboratory/middleware.ts | 4014 | `5c144498b1ec7046cce3ecf459f710597431fee431f574d1792566969be98769` | 0 |
| apps/laboratory/next-env.d.ts | 260 | `2b85ba46ad73ba79949cba0230a56ef00424904a56457bbb83b90f3b63574f73` | 0 |
| apps/laboratory/next.config.mjs | 1166 | `cfa30ef349782d7e1fba2d970f2ef64aaa146b32fd92cdc5c2c2fc88a06d8441` | 0 |
| apps/laboratory/package.json | 12118 | `abcd31a4cb5e2d2ed3dd8afb0cf63dff5f6dc2bd7ddd6f03d7b0d1452f72663a` | 0 |
| apps/laboratory/playwright-merge.config.ts | 733 | `f86bf45db544d3e12206734c1290f44ac1f3d90e1ecfbdca0748b5b4a39a84c0` | 0 |
| apps/laboratory/playwright.config.ts | 2029 | `c196e148ec8952b8bd8a55a8956555e9e266eefad7c79c7ad932085e28e43be8` | 0 |
| apps/laboratory/src/components/AccountCard.tsx | 5309 | `ccdd33a3a33c73eec156aeceef48f5973aaa1cc100b3b6c390cc0e0643191e87` | 0 |
| apps/laboratory/src/components/AddTransactionModal.tsx | 2237 | `d4490cd103a409fbb5f6f94127c5cb55251129c476bcdb7bc1f7f72b4db2b24d` | 0 |
| apps/laboratory/src/components/AppKitButtonsMultiChain.tsx | 11208 | `b8d3adffa09e136713d8621036009fbfcb1ff3f5c8ec68f3c8276961c72b5178` | 0 |
| apps/laboratory/src/components/AppKitConnections.tsx | 3677 | `be1792efb015ada378141865dfc2980de7a90077688ec5bffb57b2af1e5ef9ef` | 0 |
| apps/laboratory/src/components/AppKitCoreHooks.tsx | 2565 | `d4cc15776c1e9db5a2f7206b0b8b98a9bce200e37fea684122fa06f2a5cb3929` | 0 |
| apps/laboratory/src/components/AppKitInfo.tsx | 4146 | `070cf1eb36719b3b47f0d856cacc6c567eb94d83fc33b80e051e6412fcbb52f0` | 0 |
| apps/laboratory/src/components/AppKitInfoMultiChain.tsx | 2011 | `118e38b19bfc4702d2fae3dbc314c63217343e39d51adaa689ba0de80bcea53a` | 0 |
| apps/laboratory/src/components/AppKitNetworkInfo.tsx | 1226 | `3f529352ee8866c0ca1d1d1841a637c85a54b283a93bc0a7ddb86a789a1e8fc6` | 0 |
| apps/laboratory/src/components/AppKitPay.tsx | 8673 | `52aa27ff26d482be6b15f850a24e92ee04b8822b1179a253ae02024f91d62b38` | 0 |
| apps/laboratory/src/components/AppKitWalletButtons.tsx | 5066 | `3746e2d594a35b8d1d6cd2343daeeea1f2452ff5319277d01f5d80038b8bfad0` | 0 |
| apps/laboratory/src/components/Bitcoin/BitcoinSendTransferTest.tsx | 2006 | `1820eafb093a63d1d7fbf103dc2a4ccbeeda2e6cb761eef687298c9ed2ed5edc` | 0 |
| apps/laboratory/src/components/Bitcoin/BitcoinSignMessageTest.tsx | 2326 | `d30f547206c2cee62c4ec3c1153a3e1d19b5071378e47640bacc462c9f32c508` | 0 |
| apps/laboratory/src/components/Bitcoin/BitcoinSignPSBTTest.tsx | 2985 | `f1c5babe7106c6585f7b083b2b55b07510a973b64456b91979aa40120a4fceb1` | 0 |
| apps/laboratory/src/components/Bitcoin/BitcoinTests.tsx | 1822 | `5b7928848c25820a4a38e1e2ac2739935d8eda97bb5ac25ff08845d558dc7198` | 0 |
| apps/laboratory/src/components/ConfigurationList.tsx | 2232 | `33b7241974cbcca9c1326b313e2294c8f5bb1a6f2fc5fa256ab8fbfd6174c3b5` | 0 |
| apps/laboratory/src/components/Connection/ConnectionAccount.tsx | 3301 | `64b27eb2de97f46e5fe9bb2ff83dc7ecea09ff963a751e845cf8ec72a832ff58` | 0 |
| apps/laboratory/src/components/Connection/ConnectionCard.tsx | 2831 | `0a77321e1fafdb2f9d9e6525a56f3d1c6297c08a53c6e33c0243149151baaa36` | 0 |
| apps/laboratory/src/components/Connection/ConnectionList.tsx | 1974 | `77d02f080b4598963601b80d230eb3932e37e09f969950c5c9dc747df143354e` | 0 |
| apps/laboratory/src/components/DefaultSIWXStatus.tsx | 2008 | `86466fbb2f19cedec90fa70e2fbe7311fece042ad22e9005b12ca52f0adcb116` | 0 |
| apps/laboratory/src/components/DemoContent.tsx | 4235 | `7cdd318122641ac6b6efe7c0bab6810168e429af4d7aca3360ca5c49d4c28b1d` | 0 |
| apps/laboratory/src/components/EmbeddedWalletInfo.tsx | 1432 | `40c058219e134762e4360ff3c195bcc151f1f7d8387ce1c225cee3011796e6a3` | 0 |
| apps/laboratory/src/components/Ethers/Ethers5GetCallsStatusTest.tsx | 3046 | `4185926f2a2d55526ba35481600955808758458143f1c360c00a2a86a380901f` | 0 |
| apps/laboratory/src/components/Ethers/Ethers5SendCallsTest.tsx | 3837 | `346c20221ce6383cc49abb06918d20e75a251bc811e5c0f8d7e3fd0724df3a34` | 0 |
| apps/laboratory/src/components/Ethers/Ethers5SendCallsWithPaymasterServiceTest.tsx | 4905 | `5f0e190ffbeb7fae25ba550408b005d37901539cf685f7cf33078a46e2e43c8d` | 0 |
| apps/laboratory/src/components/Ethers/Ethers5SendUSDCTest.tsx | 7645 | `90d01cd6b0a6453a4b6de5fc15d2caa9eead1aa079ae406474cfbc01fcdb1317` | 0 |
| apps/laboratory/src/components/Ethers/Ethers5SignMessageTest.tsx | 1554 | `081528446d7ab70fa17d34cdb639e002d436f70ce42c397bb0e02a9a2d6af562` | 0 |
| apps/laboratory/src/components/Ethers/Ethers5SignTypedDataTest.tsx | 1960 | `de39fb54815f035e53bc88f13d535948582fef40bae56eb49fa8b4653ba0f250` | 0 |
| apps/laboratory/src/components/Ethers/Ethers5Tests.tsx | 3814 | `afa97c96b7e035c7f7bb5f50d9af171027911aa1faf6dfd6b44cc77e5c573da4` | 0 |
| apps/laboratory/src/components/Ethers/Ethers5TransactionTest.tsx | 2347 | `1b5dc4fbd30ef2e076df21198195adc656a36efd2330d8d3e40898337ed167cf` | 0 |
| apps/laboratory/src/components/Ethers/Ethers5WriteContractTest.tsx | 2508 | `6dc0a759e6e6f1b2510fe0a2a89aab40abc18e0590d578f48678c581561b9325` | 0 |
| apps/laboratory/src/components/Ethers/EthersGetCallsStatusTest.tsx | 2729 | `cc07bf4f2c410612237127c212f3f3e124bbaf87f34880b67b05f62c3341235b` | 0 |
| apps/laboratory/src/components/Ethers/EthersSendCallsTest.tsx | 6653 | `4655a916f930551cdb47549b2e069eee7973b2f0e2ed9ab399199a8e727f8165` | 0 |
| apps/laboratory/src/components/Ethers/EthersSendCallsWithPaymasterServiceTest.tsx | 4979 | `17f2e1c2953afc252e40a255d5583c7b585ba55f25d6b72f4fe1d0beecc0f0a9` | 0 |
| apps/laboratory/src/components/Ethers/EthersSendUSDCTest.tsx | 7648 | `313a18063963a2cb438eae91ed53e89ad7696498e23db61950e5baee487c94b0` | 0 |
| apps/laboratory/src/components/Ethers/EthersSignMessageTest.tsx | 1506 | `80d9b6217526edca5fbebc888f337988ea6f73fb04c8a5a6a906bae5f3ef2c84` | 0 |
| apps/laboratory/src/components/Ethers/EthersSignTypedDataTest.tsx | 1974 | `e2530515ca8e59485484d4a9af967f6d981a8a1f440842386b2a5a5b52a9f70f` | 0 |
| apps/laboratory/src/components/Ethers/EthersTests.tsx | 4126 | `324d79776655daf15e2f1b90def5c92ba1397368a0681a165a9b8bab418753b5` | 0 |
| apps/laboratory/src/components/Ethers/EthersTransactionTest.tsx | 2365 | `2cf8e7d9875fd1562716b388d89bfb71597403a0ec33394a7caac8ec09265a87` | 0 |
| apps/laboratory/src/components/Ethers/EthersWriteContractTest.tsx | 2532 | `a31d2574056dc83ed378bf23f76ed07b12ac98973e3dc33f8fcd9beafcdf961f` | 0 |
| apps/laboratory/src/components/Headless/AppKitHeadlessInjectedWallets.tsx | 1409 | `af5e4c2be4107847ad7839c3c90b55f84a7c90ef878d1a62d35ec786efe3548a` | 0 |
| apps/laboratory/src/components/Headless/AppKitHeadlessQRCode.tsx | 6476 | `ee7f28b1285fbca3e8c61e39b840093268b335a69888fdb01366fdf3c9acb9f7` | 0 |
| apps/laboratory/src/components/Headless/AppKitHeadlessWcWallets.tsx | 3165 | `30facdc565d168a83086e5394c853169a793b2029901afdb12a3f8db09914096` | 0 |
| apps/laboratory/src/components/Headless/DemoContentHeadless.tsx | 1897 | `4cce75740a9457ad3de9f21e4a0779d0a45e99110cca2b0c3545ffc739517a11` | 0 |
| apps/laboratory/src/components/Headless/InjectedWalletItem.tsx | 4194 | `48f08e2d704bff569fc9596c21748ecf24300ae6f2723a455e8d8cb49c3773df` | 0 |
| apps/laboratory/src/components/Headless/WcWalletItem.tsx | 1962 | `a02d739dbb81f4b2a83e5b3d79e80c78209552a5efe74dab955df72bedad0291` | 0 |
| apps/laboratory/src/components/InitializeBoundary.tsx | 349 | `ca0edf22be5327f1de715186a77d9950cf6dd2ecbe81b6fae50d4a1b2ec08a9c` | 0 |
| apps/laboratory/src/components/MultiChainInfo.tsx | 1246 | `28ad3a7a12f202567978d3c06c104e8148edb90e5757359b912f9c05329804cf` | 0 |
| apps/laboratory/src/components/Pay/PayExchangesList.tsx | 3761 | `1bafd2acc989be19270fae5525b17fd7314a207c7a86532b2741a715f698391a` | 0 |
| apps/laboratory/src/components/Pay/PayModalTest.tsx | 1670 | `d5996a11b73a709f3a09d6c582a913a5fada397190988d5adcd067d773f2c86a` | 0 |
| apps/laboratory/src/components/Pay/PayPresetSelector.tsx | 1555 | `82d36469938eb1b10a8a75008bd591594406f153a1579775ab374f6c2a0f0f93` | 0 |
| apps/laboratory/src/components/Pay/PayStatusTracker.tsx | 3346 | `936795f8516ec88e2edef6eb8afd1daf30b74df8c5fd01ccf5597ca80dd7a9bc` | 0 |
| apps/laboratory/src/components/Pay/PayVanillaTest.tsx | 2332 | `9ab5c143c75520a429d2456f346c6b43b68b558a5dcc4574f7a2aeee822d3cf8` | 0 |
| apps/laboratory/src/components/RandomLink.tsx | 468 | `f610bc09c2fb7c9e610eb55e0415797cc49bbcee61787fea5ef47bc303c7cdf0` | 0 |
| apps/laboratory/src/components/RelayClientInfo.tsx | 927 | `69c9fc7834371131813107d0df81332abc2d41b17e50a5e895903a57b3a88a4d` | 0 |
| apps/laboratory/src/components/ReownAuthentication.tsx | 6214 | `365a1290cda7241158547b904b140c6015184a7be7e7dd282e281bbd60a909b3` | 0 |
| apps/laboratory/src/components/Siwe/SiweData.tsx | 1810 | `d7c8f045df8dcbdc1a16523685fc40048a5828e5e7b965ed58707ca329e6d6b6` | 0 |
| apps/laboratory/src/components/SmartAccount/SmartAccountVersionInput.tsx | 1675 | `2828f25db24f0e664d42e96439eb6621e641642d84be1a80ab27f537d2581f63` | 0 |
| apps/laboratory/src/components/SmartSessionGrantedPermissionsInfo.tsx | 1478 | `feb7ba141249ab5ffe757efc2e14129f9fd04d44a6044db689efeaeb9e0a85d8` | 0 |
| apps/laboratory/src/components/Solana/SolanaAddressTest.tsx | 886 | `eac97490a7b408f1d94160929dd44141aeb612efe25c7e078eee547dfa7456d2` | 0 |
| apps/laboratory/src/components/Solana/SolanaSPLTransferKitTest.tsx | 3878 | `c6e5b1732f8a9f198610ac972acf9e4766a439f0614018c6790dcfde97ff98f6` | 0 |
| apps/laboratory/src/components/Solana/SolanaSendTransactionTest.tsx | 4883 | `2127c18e12705744c91441d3757f6deb97638f80ef99ad923caaab6db0a55eec` | 0 |
| apps/laboratory/src/components/Solana/SolanaSignAllTransactionsTest.tsx | 3377 | `16a2cb45d74b297c654ba119a1f3469bb4e18e704d4dbbc2ebb9eea2efa67883` | 0 |
| apps/laboratory/src/components/Solana/SolanaSignAndSendTransactionTest.tsx | 4862 | `05b88d5a355dab31ae02f3fe5d5439fd8b878fa1941ebb75de126d4f4deb08ee` | 0 |
| apps/laboratory/src/components/Solana/SolanaSignJupiterSwapTest.tsx | 3244 | `a67b54746a30e09fc0cdcfd1d398762a4b46f76807f1b476db8a79f775888127` | 0 |
| apps/laboratory/src/components/Solana/SolanaSignMessageTest.tsx | 1302 | `e421fcce0e64425de1ba30be00c4e529ca5cd35a9f7d01d570f3d1454cb58335` | 0 |
| apps/laboratory/src/components/Solana/SolanaSignTransactionTest.tsx | 6101 | `c1fae332069abebd46d252e67d340f4772a11f66aafc01347057fa73f1aee29e` | 0 |
| apps/laboratory/src/components/Solana/SolanaTests.tsx | 5309 | `4af44370108cb14fe49a9f89f488e168982075282ab77815f8aad35b2d09c9a1` | 0 |
| apps/laboratory/src/components/Solana/SolanaWriteContractTest.tsx | 3995 | `24d085056ee463b0be4700639809ca4c7ccb4598c7341aa0765553c026582431` | 0 |
| apps/laboratory/src/components/Stellar/StellarSignMessageTest.tsx | 1726 | `787df96c5ff2e7b42e01055c5211246c477de99900f485f0aa5ab2fbf48163b6` | 0 |
| apps/laboratory/src/components/Stellar/StellarSignXDRTest.tsx | 4190 | `e1be0e949cb26cad77d3557c91bd8c23be987d71a6ecda1ba25e4e02c91bd436` | 0 |
| apps/laboratory/src/components/Stellar/StellarTests.tsx | 1156 | `413f7119f4fec755b4675d42defb28147a99cae79f8daa17f1df65588a828c0c` | 0 |
| apps/laboratory/src/components/Theming/AccentColorInput.tsx | 1053 | `46bfac546c39cc10613904e5fbb3949ece344ad34c6097f8ccc40db1e6b78e9b` | 0 |
| apps/laboratory/src/components/Theming/BorderRadiusInput.tsx | 1068 | `7b2ac7081e0181380de1e6f1c014585daadbe1f4da3a3ca888a355ecc8b957d8` | 0 |
| apps/laboratory/src/components/Theming/MixColorInput.tsx | 1706 | `b623d7679cf8d74bb4e56f1a44b77ce5a2a812d8b74765bc9fba3ea05dd18146` | 0 |
| apps/laboratory/src/components/Theming/QrColorInput.tsx | 1030 | `fae602025b181e87cb03f01fac69c70365e6a75915a63cb515ac9c386af93074` | 0 |
| apps/laboratory/src/components/Theming/RadioColor.tsx | 769 | `ee548c97dac835ade91a7b3a3949c47fc41401b45f00f9ac9d1c69c3e8f45b75` | 0 |
| apps/laboratory/src/components/Toast.tsx | 2513 | `0e156717b53fda4ad49203d8e44dfe1b514b0d8eec455681a1805e8a1ef16a95` | 0 |
| apps/laboratory/src/components/Ton/TonSendMessageTest.tsx | 2316 | `f43b098bf235d9c8f82f27453bcec174c1f5091544b9675758358b78702d0e1c` | 0 |
| apps/laboratory/src/components/Ton/TonSignDataTest.tsx | 3223 | `01d7886d81ed2effebed4bcf4cbb0f6fd5372f564babb0bbf460560b95134273` | 0 |
| apps/laboratory/src/components/Ton/TonTests.tsx | 1120 | `9bacc525933ac87575d48dd51c8a43a9cc2958f44d1137574b405bb6b2b8590b` | 0 |
| apps/laboratory/src/components/TransactionToast.tsx | 3331 | `956d1a1e3ecfff30b5e4dce090757862a9ebf6d0404e0d2e161f86451d0d93ce` | 0 |
| apps/laboratory/src/components/Tron/TronSendTransactionTest.tsx | 2258 | `80de03f3ed272713452291d495b7ddfdc1bb0633604461341e1258c19608c6e3` | 0 |
| apps/laboratory/src/components/Tron/TronSignMessageTest.tsx | 1851 | `e746f3cd5c2964812c2a444bbcd329747fdec2e608825563110519f87cdd1bee` | 0 |
| apps/laboratory/src/components/Tron/TronTests.tsx | 1158 | `78bc80a6af9c62e286a06d6f7d57122799d81075bc1cbd93e60f38a1b1d95cd0` | 0 |
| apps/laboratory/src/components/UPA/UpaSignMessageTest.tsx | 3925 | `6a7595cc61446f2e931161d9247b6aa6ee4793cec275ba2f904d561e27d800d3` | 0 |
| apps/laboratory/src/components/UPA/UpaTests.tsx | 683 | `16e85b1a3244c2aba7f79d855d3cadd6fdc52675603026d66d28a7bd633930ec` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiCreatePasskeySignerTest.tsx | 1551 | `02254ac6677be2f0365149f261357a90d2f990bdd1c9e6d3d4cacdf0fbb6035e` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiDisconnectTest.tsx | 1682 | `671dd257aa95afb9f0166416b249a0f07cf2d54f5449892482cea69d1de98d96` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiGetCallsStatusTest.tsx | 2411 | `7f18ffa3b74510f078891e37bc6e553fd7adf9e9934f172363f17ef74473d94a` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiPermissionsAsyncTest.tsx | 1712 | `37347d0e9263bf5261e49bca5cdeab4ed929c63016a7c7d106b956e0ee4562da` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiPermissionsSyncTest.tsx | 1995 | `fcd47bd96be3f21cb026aed96c77ad5f450e7042c9c4031d987ae8bf662185bc` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiPurchaseDonutAsyncPermissionsTest.tsx | 3830 | `bae5e1ee995a45d08d534dc7686ba839f74974914b88a73f0c58c4b88d6b55a1` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiPurchaseDonutSyncPermissionsTest.tsx | 3780 | `301c579fd594a268606188e70761e7b161b86777060bf604d67cf12408f8052c` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiRequestPermissionsAsyncTest.tsx | 5392 | `a533233c0d82b8a0d2fdfca9be8aa17bf0e6bf2ad72e46952ae0ef96b8a4763b` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiRequestPermissionsSyncTest.tsx | 4696 | `43d736924aeee50f907d63132494ae7ba7fa59e5c6522a2979a2ac3e3a5b6219` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiSendCallsCustomAbiWithPaymasterServiceTest.tsx | 8972 | `d55772cf9845f3b0317c29b2319c4b604e141c145fe43c6879bfca4e4b7cb4ca` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiSendCallsTest.tsx | 3316 | `5af86e3e6d73cd8d51e936d40c12b37a9f273a71bd1cada9aa9944d71cc78ddc` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiSendCallsWithPaymasterServiceTest.tsx | 5503 | `8a27439ef3068a115e2ccd8f0d591e7299b5b9cd7e81ef0ee6f9bc35dadb0fae` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiSendUSDCTest.tsx | 7219 | `91b7cbc4eb68ce3d2b101491e5e81ffbf9d2c276d9bccb82df3aba6b47b9ea8b` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiSignMessageTest.tsx | 3093 | `542a605379c0d5d7dd29d93b3fb944678a994424760c717871589bec03580f4f` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiSignTypedDataTest.tsx | 1765 | `4a02abcdeed8affcb94bd7675c797c92c7558b6152848a5232817295dfbd9adb` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiTests.tsx | 4419 | `0b2dac0150c46a52f0f7f64164c22d3ceb222f7265085b38915e5f87aa77248c` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiTransactionTest.tsx | 2711 | `97a077dde08974fe5b2879699f2cfb66a404d83a52b867de5d1603fb236fc126` | 0 |
| apps/laboratory/src/components/Wagmi/WagmiWriteContractTest.tsx | 3605 | `dfadd16c17f5c3ced80e1f47dd8b6ef6e8fc522093ead89949a9aad2feb8a4a1` | 0 |
| apps/laboratory/src/constants/appKitConfigs.ts | 17669 | `d3fe774b35e540807267f9249e883dbb6ef3b588189fd6dc0dde2b97b0b86631` | 0 |
| apps/laboratory/src/context/AppKitContext.tsx | 2235 | `ea17327436f2ab4495ba00fde01c5531c4f0d03e732c25b252461082881f9c7f` | 0 |
| apps/laboratory/src/context/ERC7715PermissionsContext.tsx | 2027 | `70c37ef37c32b8b3089e01ed0ec0e4c2996188b4414a12e69660dfaf76c51765` | 0 |
| apps/laboratory/src/context/LocalEcdsaKeyContext.tsx | 2141 | `b43405d4731610b01317c5933535cada85ec74d9902301a1b744720491f353c5` | 0 |
| apps/laboratory/src/context/PasskeyContext.tsx | 1943 | `46f0d17f7f052e7b82563b6fc0c90961b053e645b6b601bed5cdf7704f599fc4` | 0 |
| apps/laboratory/src/context/ProjectIdContext.tsx | 2335 | `a9a10aee5133f86babc6c7fe04327f84b4c6bf28314004bbd1d1b3982fb54423` | 0 |
| apps/laboratory/src/hooks/useCapabilities.ts | 1507 | `fee90583d506ba836f20d36e87e12e4d486d3927124fc69d7c0fd23572a2b478` | 0 |
| apps/laboratory/src/hooks/useDebounceValue.ts | 379 | `91ed3d2e11512118ac10ec3cce2bbe8302ade295ee34fd156ac52f3213a4d1c9` | 0 |
| apps/laboratory/src/hooks/useERC7715Permissions.ts | 497 | `98239773495eaf55576a02eda564964c3f683bce0159523659bbe5fa81279406` | 0 |
| apps/laboratory/src/hooks/useEthersActiveCapabilities.ts | 2023 | `0a5f45deb3741c7847c9a351b6df24632335c170f2e111df356cd8ac2c406a24` | 0 |
| apps/laboratory/src/hooks/useLocalStorageState.ts | 1227 | `d4fc40f762012f21643994e077f4f2a4e8e1599f7ca9c4c51d8dec53729b5a5d` | 0 |
| apps/laboratory/src/hooks/useProjectId.ts | 240 | `3a1303b812e3665d437b29aba8323d9f29e8da574bdbecf65191e4661de56a75` | 0 |
| apps/laboratory/src/hooks/useWagmiActiveCapabilities.ts | 2793 | `b04e51ff39ef0455aa0789ef585c00f90602d5861d1a432a78ac6b53d12ae50d` | 0 |
| apps/laboratory/src/hooks/useWalletGetAssets.ts | 6224 | `ec0240d78f462cc1cdbc2ad5ced3930103d1e24b01dc7f49645bee43c31988c4` | 0 |
| apps/laboratory/src/layout/AppkitConnectDrawer.tsx | 5994 | `78777a047ebb1445a92b42c1dd69671cdea5991966321fe8e7f8645f66b8d92b` | 0 |
| apps/laboratory/src/layout/CustomWallet.tsx | 2940 | `5291c11cd261802b30a342438b6c84579b220ddb79fa771e1dfc2f54bc32577d` | 0 |
| apps/laboratory/src/layout/LayoutHeader.tsx | 3168 | `06e7104cf2f4490cc9181a8baf4d51c70aa393136f7364a668be2d4ec75aebb4` | 0 |
| apps/laboratory/src/layout/NetworksDrawer.tsx | 8374 | `1a10318885ae8f12321fed4adaacb06f433d640b755e893480997ba32f6d6560` | 0 |
| apps/laboratory/src/layout/OptionsDrawer.tsx | 2886 | `1c2a2ef5d18daba9e8d016406d0ca3408a39ef631e01c4112c606bcc1ca09cba` | 0 |
| apps/laboratory/src/layout/ProjectIdDrawer.tsx | 2768 | `af6cac48f0a4b130338057bdcfbfa4da6c9cd9a2fc9a30f29cd3abaee2721359` | 0 |
| apps/laboratory/src/layout/index.tsx | 871 | `ee51388fc577a9ae3f8841b0e63452b717d34e82dd7a57ed9a4e38fcb3ae6856` | 0 |
| apps/laboratory/src/types/EIP5792.ts | 740 | `3eedfa3381674e9b46456387c2b234dfb46acfdd129a9dc3c015e125b78a9569` | 0 |
| apps/laboratory/src/types/ERC7811.ts | 502 | `6c3ebc7b36cda551a1713bf45a27ce42a0538295a29574d97fdb7fe605a5bcdd` | 0 |
| apps/laboratory/src/utils/AppKitConfigUtil.ts | 2811 | `b8bd978f548fc9b43fb0eb74771c6e1cfc5e0b9b928d81c0f856281ce6247bf1` | 0 |
| apps/laboratory/src/utils/AppKitStore.ts | 264 | `147aa7127f8fac810b2b786535959b9c69fbaf70f77935f9431305308abab870` | 0 |
| apps/laboratory/src/utils/AppKitWagmiConstants.ts | 481 | `5a6a811dfcab87b95e5a8236ecc3413b3a0a94655b32297755e4837ec0e9922b` | 0 |
| apps/laboratory/src/utils/BalanceFetcherUtil.ts | 3499 | `e312517a71c59379f3cdbe3fe3b94a5585c87d241023e3591fd76dc920025620` | 0 |
| apps/laboratory/src/utils/BitcoinUtil.ts | 4995 | `5a7aa32d537d5dc131c7bdbb173fb5c4240e911013823b4d27637e6bebf44dbc` | 0 |
| apps/laboratory/src/utils/CATokensUtil.ts | 858 | `f8cd1f59d36aafd25fa74dadaf9ca374f129583012aa6ce01fa786e0cd1b2dac` | 0 |
| apps/laboratory/src/utils/CommonUtils.ts | 366 | `ac53d5a2bb9a622642c5d81e1bed103e31820c5600f9e179c9cfd4be2f28ec80` | 0 |
| apps/laboratory/src/utils/ConnectorUtil.ts | 1604 | `bdd63b7fb6b81345a75e0e6c4c7e11e8000ab6b625d982d9b3faf0d927859466` | 0 |
| apps/laboratory/src/utils/ConstantsUtil.ts | 5774 | `06f7c6ee2d985ad7c99af3bc1cf752df950d4d871d8df9f44dbbd2226002152f` | 0 |
| apps/laboratory/src/utils/DataUtil.ts | 9367 | `e9eb3fa78debcf5abea8869bf438fe28e50c641d2b74906802ef29c7d1cecd65` | 0 |
| apps/laboratory/src/utils/DonutContract.ts | 1566 | `53d8582e1c0a312ae1ea8b77b084f6876a880a7925fbb216529744d0fc1a4e01` | 0 |
| apps/laboratory/src/utils/EIP5792Utils.ts | 4069 | `f165764b65c4899210b1a62f9af81272d5e45737ba93dda3bccd533f2ac93fab` | 0 |
| apps/laboratory/src/utils/ERC7715Utils.ts | 4809 | `3a833ae3ebc2d90a4289d94d0d19b837f95777e88f6d12ebca564fe4e492054a` | 0 |
| apps/laboratory/src/utils/EncodingUtils.ts | 3078 | `f8f461ff0d28340e88c19845b90af3ef8ec6f74a07c1e4a68d0f96e0f565e9c6` | 0 |
| apps/laboratory/src/utils/ErrorUtil.ts | 215 | `529940a7ff7cd6025c7a9f925e34dce8de444dff7dcb65c8998db41a67eaed6e` | 0 |
| apps/laboratory/src/utils/EthersConstants.ts | 411 | `e1713ab3342218f8048d70bf4c415f4b386325f24cc4740499437336eafe35c4` | 0 |
| apps/laboratory/src/utils/FormatterUtil.ts | 423 | `33807f5c369de4e423d535c9de26a705fdfe86f3d1e693fb117a2f2ac20f3c47` | 0 |
| apps/laboratory/src/utils/LocalStorage.ts | 1542 | `3000330e3570a8c4d363ea5d0025be89fd36e646abf965a740c47f8465ac6120` | 0 |
| apps/laboratory/src/utils/NetworkUtil.ts | 416 | `d8a88aded66b60a31c1ca82dea28989a09f00cf6b3ccba2b839f0037574242fb` | 0 |
| apps/laboratory/src/utils/NetworksUtil.ts | 294 | `6aae5c9b06e51531ef9314b4187ab013666e7fadebd06591dcc160fd4e79d74b` | 0 |
| apps/laboratory/src/utils/SentryUtil.ts | 324 | `0bb2be919e76c24d3c5dd0bf6f48394facaa5538314b838f3e7b727d9af57cfc` | 0 |
| apps/laboratory/src/utils/SignatureUtil.ts | 687 | `f8813d398f1c65767d7876fa29250882c8c0d0b98e04896d85a71b2f584fbf41` | 0 |
| apps/laboratory/src/utils/SiweUtils.ts | 2774 | `3a227185ac702b750c4dd3c1aa302d254122fc41dd5655243b7a73eddf13a11d` | 0 |
| apps/laboratory/src/utils/SolanaConstants.ts | 512 | `1a10c5a4bc2fe3c1c545996366911c92bf147bd210709a4e5641a8050509bfe2` | 0 |
| apps/laboratory/src/utils/SolanaUtil.ts | 439 | `6e739a28bdcfc172e9fed2afe5d6ebc46d44ca343dbdd301804ed25d18cb0fa5` | 0 |
| apps/laboratory/src/utils/StoreUtil.ts | 2041 | `763398b1c77527530f74e18abe46c1975183c3bbcdde53b5102227e11d7b8144` | 0 |
| apps/laboratory/src/utils/UserOpBuilderServiceUtils.ts | 3685 | `fbf12b1242688b9f208db91d66e6c3b06e82852f63edcf98a5c911a56f0dd5fc` | 0 |
| apps/laboratory/src/utils/WagmiConstants.ts | 481 | `5a6a811dfcab87b95e5a8236ecc3413b3a0a94655b32297755e4837ec0e9922b` | 0 |
| apps/laboratory/src/utils/auth-get-session.ts | 478 | `113d9cdc8b801d17e88df9dfafb64d25890da347ad46feccdc3df78d902107b6` | 0 |
| apps/laboratory/src/utils/auth.ts | 2919 | `6821b38f93ae5274fa316dfb1338afff96c70189b0a7245214eb5cb915d1be44` | 0 |
| apps/pay-test-exchange/app/api/status/route.ts | 647 | `cac1e4891f24abbdee208feb3f00fe1f46476b98b2847b58161b7f4de2ee5047` | 0 |
| apps/pay-test-exchange/app/api/update/route.ts | 1622 | `0e7f78b2bc46456b6f2951973ecc5c86779df62a675213bb08629c734ab1a054` | 0 |
| apps/pay-test-exchange/app/error/page.tsx | 520 | `2e09120c48be457a19964a6b9acf376d35275e30cfc0b501de02b7b1b40a01d0` | 0 |
| apps/pay-test-exchange/app/layout.tsx | 860 | `684a951e04a19b44ffa8a16b533b4a200d7fc58639105c10c0265dfc71c7c870` | 0 |
| apps/pay-test-exchange/app/page.tsx | 911 | `599c8c8a9700fae1a44b47394e92c13e64240dd04feb3101d798fde997530725` | 0 |
| apps/pay-test-exchange/app/success/page.tsx | 706 | `6f4a2ebca28a0ff2518263b74412220b39a085016482d58fdc728f621987f58b` | 0 |
| apps/pay-test-exchange/cloudflare-env.d.ts | 288878 | `01cfce6fa82c7750d908e12ca4e838b5ccc1573c5fdce8529e1588bb773a6539` | 0 |
| apps/pay-test-exchange/components/action-result.tsx | 1410 | `2ef36d95648153c39c87a6118916f7beffaa1947f57a4d2f852b5ce36f31f8b5` | 0 |
| apps/pay-test-exchange/components/error-screen.tsx | 577 | `8de93453ae48672847034de1652a12fc0b56d126a1b7d63833bd60f86dc7f5f7` | 0 |
| apps/pay-test-exchange/components/exchange-actions.tsx | 2532 | `1a976d96ced1971cce21cc054bc696771ef8263d1902ceadadcd140a58d2d8d1` | 0 |
| apps/pay-test-exchange/components/payment-info.tsx | 3545 | `b63aea2be55ea90e7a30e629da41a4a667c6e47dd26f54d37d69c18531ace979` | 0 |
| apps/pay-test-exchange/components/theme-provider.tsx | 296 | `f77b8dd6c14d2ee8b5bff7665d6643768b9dde23fde94d69e8e63d690abc5780` | 0 |
| apps/pay-test-exchange/components/ui/accordion.tsx | 2019 | `ebd7e82a61a4943eafc6a98e2d22068653b9fa12974808a72c71d0f6879999ee` | 0 |
| apps/pay-test-exchange/components/ui/button.tsx | 1857 | `cb1f8b6ea99ff9e68cdf1360d028824e67cb41f657dd2b08b4d41c860ddb81fe` | 0 |
| apps/pay-test-exchange/components/ui/card.tsx | 1918 | `98e67f17e7902bc9e2696aad1b1436b179ef7ea2dd5261ada57814e8a1e93952` | 0 |
| apps/pay-test-exchange/eslint.config.mjs | 379 | `48f8a2790f821e069ce3c511f227f74982e9219476674be36ecccdf2854c0968` | 0 |
| apps/pay-test-exchange/lib/fonts.ts | 1395 | `e60d6a31866ada0b1918a5bc0d6f68a8e03326059deb34e7936b280b3f0d01fb` | 0 |
| apps/pay-test-exchange/lib/session-actions.ts | 1071 | `5a044e3bb0dde2368d4c60cdaf28beae13c0aeece0f07a78aaa39d01c6439ecf` | 0 |
| apps/pay-test-exchange/lib/types.ts | 104 | `f6d410415605ac929fcbd80c2cd27c7fdf73bc022bca1ad64f6670b639af9dcc` | 0 |
| apps/pay-test-exchange/lib/utils.ts | 166 | `746e4d9beb1a5b6f0e047ec19d5f1c542c9f8117f4ea7c80d7b9bd0fe2128e91` | 0 |
| apps/pay-test-exchange/next.config.ts | 319 | `c2df2d6e27ab597abd2cbb1c6e9e05692339a745fc1c176166918ab0333a95c5` | 0 |
| apps/pay-test-exchange/open-next.config.ts | 107 | `71b7739b2354d935c674e67db55c860c28b972eb70f3e184c5957c996e00a38a` | 0 |
| apps/pay-test-exchange/package.json | 1254 | `ccd9ff7470cf56978436bc034d767c2867f3f51744ecd9b439285361bb2b0bd5` | 0 |
| apps/pay-test-exchange/postcss.config.mjs | 210 | `dbea5869c7e47efd6189f95eba5802cfc8a65b5e874d04d5f1ce7cba6e40b9e8` | 0 |
| apps/pay-test-exchange/tailwind.config.ts | 3434 | `cc8508a03cf2386c29d871fe1254ef08f8865e91cc2d7d3141572b987f89a902` | 0 |
| apps/pay-test-exchange/worker-configuration.d.ts | 288856 | `cc1414a53ce2ddebd667ed2bce660ee852fbae1e61894cff18ce0f66bf7c6fe7` | 0 |
| dangerfile.ts | 25096 | `ed0844124aef08c4558b5a3ecbd49994889e7e64e3a11b6a145320cb63e11288` | 0 |
| fix_parentheses.py | 612 | `add8f6cd8c9dcd70e1b63c5664a4c65dd340cdf1550c452e7c1b1d3f7bc58df5` | 0 |
| package.json | 6183 | `08e5a087b12fb84650b0d48a2be68a9bb5425c50c17226b2fcadb61649c2f14e` | 0 |
| packages/adapters/bitcoin/exports/index.ts | 66 | `c379a46d621e58a585b57f8604fb52d3904f48e405b05d71e74b9653768746ba` | 0 |
| packages/adapters/bitcoin/package.json | 2005 | `48f25bb715d85ce5edf744f3898eba5ecc75c2afe653791a4dac9c0142fce1d1` | 0 |
| packages/adapters/bitcoin/src/adapter.ts | 19796 | `9788b2b28b927468c1c854d7e7e9aa994effdd652afd58bebd6730340bc7ea8c` | 0 |
| packages/adapters/bitcoin/src/connectors/BitcoinWalletConnectConnector.ts | 8915 | `77e194bf985134cb591f7d3ceba274f3e4f182aa4a87db48b03659bc77a661ec` | 0 |
| packages/adapters/bitcoin/src/connectors/LeatherConnector.ts | 4498 | `193b0568fb4be7b0260998e9da581640ba685858cb4106a08d1182a249ef2f46` | 0 |
| packages/adapters/bitcoin/src/connectors/OKXConnector.ts | 8050 | `7376df35983d020f1db61c09e86c9267ba2d8d6f4f71ddd9ae1cb04a7ffe5e52` | 0 |
| packages/adapters/bitcoin/src/connectors/SatsConnectConnector.ts | 7822 | `aab6d1948ecfa95b1c998b7ec811f9ea0c64aaa729db7440041b616876951db5` | 0 |
| packages/adapters/bitcoin/src/connectors/UnisatConnector/index.ts | 6163 | `2725039241b1b6d1356427d5007effcbd2266dee5d9d24a5a9266d6702ae8397` | 0 |
| packages/adapters/bitcoin/src/connectors/UnisatConnector/types.ts | 2346 | `5f321b84cb74df6669a69ab03fd11be107c83d8d268d8ddc7642c4a65b7dafbb` | 0 |
| packages/adapters/bitcoin/src/connectors/WalletStandardConnector.ts | 7912 | `8b022b6b2f88e0b1e36a50214c9e20731f970930ebc4834380285d4468ba7dda` | 0 |
| packages/adapters/bitcoin/src/errors/MethodNotSupportedError.ts | 543 | `5606fb606c5ea3d69b373193f9643c3800af050b1981979e139f8ee2e6f5a061` | 0 |
| packages/adapters/bitcoin/src/index.ts | 143 | `863c36f35e6d89d9c21c58878c651c0b102e06f39d1b11524b4fb142b0c69292` | 0 |
| packages/adapters/bitcoin/src/utils/BitcoinApi.ts | 1059 | `50f71d3a02511804241a9adea195d4cb2fa667a95045003024bcfc901e63eb69` | 0 |
| packages/adapters/bitcoin/src/utils/BitcoinConnector.ts | 625 | `60ff435f74148e9912bb8a76a1d50d0115f6a4198b9dd33044843b854f1f0888` | 0 |
| packages/adapters/bitcoin/src/utils/HelperUtil.ts | 957 | `5f91ee14369e980f655d60b3cfaf5a30a9a2d7456e4da7325cb268df2a9a22f5` | 0 |
| packages/adapters/bitcoin/src/utils/ProviderEventEmitter.ts | 1202 | `efd88a27a41e4303703152c23fcd1c78247240fe943ae53112fbd83300cce78a` | 0 |
| packages/adapters/bitcoin/src/utils/UnisatUtil.ts | 984 | `0710fba647451f3aff5df6ee8a68f9755171ec3892b707a85271733f0527d592` | 0 |
| packages/adapters/bitcoin/src/utils/UnitsUtil.ts | 394 | `d828c7a29a33e4151cbbb10816ce397d624d1ad0b9f2baf05ed4e93dfe6dc1b2` | 0 |
| packages/adapters/bitcoin/src/utils/wallet-standard/SignMessage.ts | 2350 | `c13e5c0d014735bcbafa5c2abb3abc0d62943eca1607402fc52d2558a026461c` | 0 |
| packages/adapters/bitcoin/src/utils/wallet-standard/SignTransaction.ts | 2741 | `b04272dc2f484147fc12be4517e2fd962c60d9d03398761be497ba0a67a06a50` | 0 |
| packages/adapters/bitcoin/src/utils/wallet-standard/WalletFeatures.ts | 647 | `3ba56d52b3b7f34aff88302025dff171d24507177520ebc68ca8b08b2efbea71` | 0 |
| packages/adapters/bitcoin/vitest.config.ts | 120 | `27d27d7b59d34ecbbdcd94c545de62a0448e5b1385bafda59a561d6109aa8eba` | 0 |
| packages/adapters/ethers/package.json | 1871 | `b1addbbd9fad36bb9f9d028b250dac73bc41935dc72578037231e152edc1978d` | 0 |
| packages/adapters/ethers/src/client.ts | 28422 | `b58ed88505a4a78011cc48fd7c5ec3d68aed74c8e4245421e2dd6b8aab3c100a` | 0 |
| packages/adapters/ethers/src/index.ts | 197 | `d747e9ac909493bf278cb04ef6f7dfdc4b620279d1d5edb0e52f0b428df909f6` | 0 |
| packages/adapters/ethers/src/utils/EthersMethods.ts | 3443 | `bcbc6e9c6609da0e7633e2710c7874c4281d0d057eb18aa07c023e12d857f684` | 0 |
| packages/adapters/ethers/vitest.config.ts | 80 | `edaa4113ae35e9507b5f1538604b5cc4120506d5631421e5068eeaadeec319d7` | 0 |
| packages/adapters/ethers5/package.json | 1881 | `f7f3795b46fe09b7e44b28a0ae63fe7b0f5a0461da4b2f1c9255dc520475e416` | 0 |
| packages/adapters/ethers5/src/client.ts | 28295 | `44ed11693470f99dbe90233b65e78071c2f89fc9b3d298425f2402ee41c26f3d` | 0 |
| packages/adapters/ethers5/src/index.ts | 198 | `2411132c4979ec1f358df9adb32d5a348510e50beca3d4e51a1bcc845a2396fb` | 0 |
| packages/adapters/ethers5/src/utils/Ethers5Methods.ts | 3598 | `17b75f374853146f3c7e4c62bc3a780deaac54a43a01e7683f057da390f6576c` | 0 |
| packages/adapters/ethers5/vitest.config.ts | 80 | `edaa4113ae35e9507b5f1538604b5cc4120506d5631421e5068eeaadeec319d7` | 0 |
| packages/adapters/polkadot/package.json | 849 | `b73f8dd0243f7fe71a0b04c56bdeda3d5670b858020d7723aaeda0f50cef883d` | 0 |
| packages/adapters/polkadot/src/client.ts | 634 | `af81cc19d9563459d57f6a5954d7ad1915bd20567d16ad57209f052dcb596bed` | 0 |
| packages/adapters/polkadot/src/index.ts | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| packages/adapters/polkadot/vitest.config.ts | 80 | `edaa4113ae35e9507b5f1538604b5cc4120506d5631421e5068eeaadeec319d7` | 0 |
| packages/adapters/solana/exports/index.ts | 148 | `b24adea0b9da25d1369da19d839b4dcb9b24da3aab247b680a36091a7b74ac4c` | 0 |
| packages/adapters/solana/exports/react.ts | 760 | `85dd1bc8ef28f7645a0370706e200c066d6463195070a5806a636415f2e8c28c` | 0 |
| packages/adapters/solana/exports/vue.ts | 753 | `93f0a414fb43074dbba7d794e3c75e67a0011c98651866b6f47f6ad7802293cc` | 0 |
| packages/adapters/solana/package.json | 3019 | `08b361594b26a40789ba5ee12811f7ce92cab3b568f6007c0062f558483e48c3` | 0 |
| packages/adapters/solana/src/client.ts | 21924 | `c8de317aff5033a81c974022fad81ba11000ddeb4ebcafea909c5c76986040f0` | 0 |
| packages/adapters/solana/src/index.ts | 591 | `badf4ddcbae40b8e8e339ca35b9ccd9b35fde83a81ba4bbc75a568af037477d5` | 0 |
| packages/adapters/solana/src/providers/AuthProvider.ts | 7103 | `cd4ee791f2a35d57153fb02441032b30b2eccbb786b4d27147ecfa09da048901` | 0 |
| packages/adapters/solana/src/providers/CoinbaseWalletProvider.ts | 7330 | `5b931e670a6e690c1799a83160908afc1b7405eeb5c4e5f8d28da030747d5a5c` | 0 |
| packages/adapters/solana/src/providers/SolanaWalletConnectProvider.ts | 13662 | `79bcf5444f8a23d902e31b44a9353dbfa6b92de449f1b0f8eb0517c17a662210` | 0 |
| packages/adapters/solana/src/providers/WalletStandardProvider.ts | 9800 | `ea72194df3c79be14d67b153afd3eebdcf437cdbd860ca56898e3d885905c8f6` | 0 |
| packages/adapters/solana/src/providers/shared/Errors.ts | 388 | `24321d38a8eab70220e98751c0575fbeac6a1327a863d4153ddbbaa7e3f25d51` | 0 |
| packages/adapters/solana/src/providers/shared/ProviderEventEmitter.ts | 1185 | `e4d400f299198f8b42af5ee4a6ef1377bca438b82197ba4ff517273645160b88` | 0 |
| packages/adapters/solana/src/providers/shared/SolanaKitTransaction.ts | 1427 | `441a7c670fa73f8798b59392779dedcf99848713d8fdb3c7f86857274c532e14` | 0 |
| packages/adapters/solana/src/utils/SolanaKitConnectionUtil.ts | 865 | `ce0368fcff4604e64e8e43049872998bb0bccc2b47f43b927f7f02eac79539d3` | 0 |
| packages/adapters/solana/src/utils/SolanaStoreUtil.ts | 816 | `b7fc671d73c7e4b3e13752bd86aed25245d10a4521e0745c15770c0523952d70` | 0 |
| packages/adapters/solana/src/utils/chains.ts | 629 | `a84b1d36cd5672877160e708c6605e368988a798e7df1f2606fc5df2a750db0f` | 0 |
| packages/adapters/solana/src/utils/createSPLTokenTransaction.ts | 4000 | `baa1e7baafd6c16ee20ec06a4bf418cbdd69235665274566af7ea0f4315faca9` | 0 |
| packages/adapters/solana/src/utils/createSPLTokenTransactionKit.ts | 6016 | `ef722f745dd35fa3f8a246aea12dad9b4d6479df7caab578cbb3a4f26aaa92b0` | 0 |
| packages/adapters/solana/src/utils/createSendTransaction.ts | 1474 | `035056d30be55b86c827c6e932501f665c0a192fa5135a08bf597b1e3760a718` | 0 |
| packages/adapters/solana/src/utils/resolveComputeBudgetInstructions.ts | 3062 | `93acb9c4b35539039b4efa30f9f6d8344918ca1b53b48522aa2d386974931240` | 0 |
| packages/adapters/solana/src/utils/watchStandard.ts | 1701 | `d8cb40cb4873cd2b9269879951ad1f161160432c0aa322a90bdbe96846b5cebc` | 0 |
| packages/adapters/solana/src/utils/withSolanaNamespace.ts | 330 | `844197a56c779d7026bb6644ef14009b1121cdfb73cb7089b08afffadacde137` | 0 |
| packages/adapters/solana/vitest.config.ts | 224 | `1d58382f53492ffdbf9990bdf769b9a4c7108bd6ca1b78f68ef18349421d1c35` | 0 |
| packages/adapters/stellar/exports/index.ts | 78 | `e3d0efc39bd70eab5dd2303068b2d055c7fc3e8faaf5c0dce1e27c4352cf67a9` | 0 |
| packages/adapters/stellar/exports/utils.ts | 51 | `deba72ff6865802733715fbadf84cd12e5ba180e08afde2cc860d47216a8518e` | 0 |
| packages/adapters/stellar/package.json | 1844 | `a18a0974af692479fc534441c02ee23b02cbfc202b1aebffa5aa916c86df44e2` | 0 |
| packages/adapters/stellar/src/adapter.ts | 11726 | `0a1d1abf3caaa48929f7f850ba2e53bc80a175e5f0a9ab52a39bd3a3faa925bb` | 0 |
| packages/adapters/stellar/src/connectors/StellarWalletConnectConnector.ts | 5290 | `91ec16046b5b22282da982a3798b817ed7791e8fd1c68bf058e007f6b8a10f8f` | 0 |
| packages/adapters/stellar/src/utils/ProviderEventEmitter.ts | 1202 | `efd88a27a41e4303703152c23fcd1c78247240fe943ae53112fbd83300cce78a` | 0 |
| packages/adapters/stellar/src/utils/StellarAddressUtil.ts | 614 | `c47f5175f364b20ba81877bbac099a3beb22493a2f2b0304550c8ae63c2565b0` | 0 |
| packages/adapters/stellar/vitest.config.ts | 130 | `7ecb1450894672e4bd88d1e6c3cc95446a94bff6eeb2c3e16e6ce550844321a0` | 0 |
| packages/adapters/ton/exports/index.ts | 74 | `7d55260a787f504957df750703c20572ea24138d229a4d6a9cb412277443a0b7` | 0 |
| packages/adapters/ton/exports/utils.ts | 47 | `5eb679fae9e563484e96cd6653ddea1ce56007d613a42175d75c97a75ce3bd63` | 0 |
| packages/adapters/ton/package.json | 1915 | `5797304a74273f5f39dae75736aef5ad5d35b6c0a104e6b022bcc84e9ea09422` | 0 |
| packages/adapters/ton/src/adapter.ts | 10811 | `224aabfb0ce7a36917757954ead1bab39c236a16a5e1a49d41026b5e1791dda9` | 0 |
| packages/adapters/ton/src/connectors/TonConnectConnector.ts | 8085 | `d0a14a13f53dc3669b27d105894252056da39e520b75951a760bcd012c675148` | 0 |
| packages/adapters/ton/src/connectors/TonWalletConnectConnector.ts | 3794 | `4276d78d01017a67ea8093efab1a59168bfeb52bb0088393dfb73cddff40ec58` | 0 |
| packages/adapters/ton/src/utils/Base64.ts | 1422 | `cb088634de25defc9ca05f1674fc2e3d5223f2ff0950a9edd93579ca6a1cf490` | 0 |
| packages/adapters/ton/src/utils/ProviderEventEmitter.ts | 1202 | `efd88a27a41e4303703152c23fcd1c78247240fe943ae53112fbd83300cce78a` | 0 |
| packages/adapters/ton/src/utils/TonConnectTypeUtils.ts | 1350 | `bfc598cbc4823144324b52b2e56893a965658a1c52d99eed950eafe996575b21` | 0 |
| packages/adapters/ton/src/utils/TonConnectUtil.ts | 17324 | `a61d2a9b047e0e75730751c0576494b77a297b199176738dcdc94a58672f2315` | 0 |
| packages/adapters/ton/src/utils/TonWalletUtils.ts | 5672 | `58c2d33cd9fdd665b86c2f7c160b1eead453aec7e7e34c189c1e43ed76911646` | 0 |
| packages/adapters/ton/vitest.config.ts | 224 | `1d58382f53492ffdbf9990bdf769b9a4c7108bd6ca1b78f68ef18349421d1c35` | 0 |
| packages/adapters/tron/exports/index.ts | 240 | `21010fc6fbcbd7238f976003b57ba2672f53465cb166fcdd43e0be32cdbc25c3` | 0 |
| packages/adapters/tron/exports/testing.ts | 188 | `1c7be0c6b55fff716a65d9714117d26c887603d40e736a7b5a0fb2cc98e243c5` | 0 |
| packages/adapters/tron/exports/utils.ts | 48 | `2cea374030f6e0013eaa8cfc64a12111e451bce6f0e2c230caab3ea97bac196f` | 0 |
| packages/adapters/tron/package.json | 2846 | `6aceaae0a4689317b67bdc0b7886fc8106fe774b254718a5b523e65cdf5929b9` | 0 |
| packages/adapters/tron/src/adapter.ts | 13461 | `806b1687074d2b2d25ac94fd48e26e14069681914fcec554beddc488ae19fd9b` | 0 |
| packages/adapters/tron/src/connectors/ReownTronAdapter.ts | 4376 | `da126f8cb8eb2317375a321ade313f6c867fad2225bf140a33048b793056b2b9` | 0 |
| packages/adapters/tron/src/connectors/TronConnectConnector.ts | 7729 | `e08f4f558704f4b85714b39636178d89d2cd015a43212f3c23b94c2f6ae53655` | 0 |
| packages/adapters/tron/src/connectors/TronWalletConnectConnector.ts | 8601 | `dac3fdd2f8d9be7c9a8772db56127f6e225d93753f30fdd3c2a209e48cfcb561` | 0 |
| packages/adapters/tron/src/utils/ProviderEventEmitter.ts | 1202 | `efd88a27a41e4303703152c23fcd1c78247240fe943ae53112fbd83300cce78a` | 0 |
| packages/adapters/tron/src/utils/TronAddressUtil.ts | 474 | `cc5dfcc9f2f72e17779a1806e67ef105ecb4f4e06417c0102022fd360bca3206` | 0 |
| packages/adapters/tron/src/utils/TronConnectUtil.ts | 5357 | `394ce4042ea846456eb14af4f72ead1985687ff4cf35958b463121f3576009f2` | 0 |
| packages/adapters/tron/src/utils/TronFullnodeUtil.ts | 1629 | `7f0ed6ec8c365fcee286fc5c0697437316598c74f1810defcaf29d19629a6b05` | 0 |
| packages/adapters/tron/vitest.config.ts | 180 | `d01a7b9fc07d8f8e49f31b58b17b4df80da5527f9110dfd3451d2900709ee4af` | 0 |
| packages/adapters/wagmi/package.json | 1983 | `ab95b512d8c7757397da8627a7e6077dfb8e1df1d31d759657c01a872416637f` | 0 |
| packages/adapters/wagmi/src/client.ts | 36827 | `a881527e034874ac42ae637d4b61f8fd42966800148ce40799b7e085d5819b7e` | 0 |
| packages/adapters/wagmi/src/connectors/AuthConnector.ts | 10096 | `99bb5ac7e9fc66447e2be55072727068cc0bacc5fa35db7d239e5cee1c7dcd0b` | 0 |
| packages/adapters/wagmi/src/connectors/AuthConnectorExport.ts | 407 | `5fbda1487753f5cfdd36c9451fb472f883910c8b81b42803e35cc3fed788108f` | 0 |
| packages/adapters/wagmi/src/connectors/WalletConnectConnector.ts | 17013 | `a54c2ebfd570dc7026949a02ddac2f828fd38306cc56405c7556e1d7069c942c` | 0 |
| packages/adapters/wagmi/src/index.ts | 157 | `0f7f5c3fc578a18ffdfa3f102a229138c9b2bb410715d223cbfae0dbe3b40385` | 0 |
| packages/adapters/wagmi/src/utils/LimitterUtil.ts | 832 | `9da4133a547ee84c22c4a394e37f6c2ca6132417c80838942b3b0f168470340a` | 0 |
| packages/adapters/wagmi/src/utils/constants.ts | 45 | `ca4bd43002a115407959fa940c35730141149fac663f0319f4e005673f6976f9` | 0 |
| packages/adapters/wagmi/src/utils/helpers.ts | 2795 | `d4095ac13220204e5ea45727bf46e584421cb1581fc92d9dc8264bc7ff4735de` | 0 |
| packages/adapters/wagmi/src/utils/provider.ts | 1000 | `49f02afa00caa3a20329c852bfac4f15da15822c12aa5b46d3c7a782d2e21401` | 0 |
| packages/adapters/wagmi/vitest.config.ts | 80 | `edaa4113ae35e9507b5f1538604b5cc4120506d5631421e5068eeaadeec319d7` | 0 |
| packages/appkit/exports/auth-provider.ts | 46 | `c0c235fca77f4568a8a698d7a3389989200fdc57c6c3f023440142c4a98449b1` | 0 |
| packages/appkit/exports/constants.ts | 40 | `c6c209ede13306642911c982d45c57e5b8fb3e628c372531a0984972857b345d` | 0 |
| packages/appkit/exports/core.ts | 719 | `161f40b061717f3e899dbe47cee6159dcb711c0d6feb60f2476ecbfe735c0fcc` | 0 |
| packages/appkit/exports/index.ts | 856 | `17ad01473fab145638420e6552919240f39a66fdadab2494d7ed9b17526c116e` | 0 |
| packages/appkit/exports/library/react.ts | 49 | `d1237e0f2a6993f1ab3b92344372d49ab4bb4e3775289bfda94cadc2b7bb5699` | 0 |
| packages/appkit/exports/library/vue.ts | 47 | `c7ef3569397a63220f25892abf45354851411ee1f647cec5a173eca1a3df8362` | 0 |
| packages/appkit/exports/networks.ts | 41 | `72f50fe2588ce7cbb66142d6e7b7cde1c6d6f9020770bcf1b46e121b6d73a7df` | 0 |
| packages/appkit/exports/react-core.ts | 1879 | `6fb537f8284504f36c9d095939d486e108c26635315d700f718db0ab56a4c830` | 0 |
| packages/appkit/exports/react.ts | 2699 | `2a6d2a56b5294855709f9d9f402a8bda3b15ed3bd3229275da15e29db7b6d0ac` | 0 |
| packages/appkit/exports/testing.ts | 890 | `9b4833f1a7147ff1d29a7650ff5131a6c590fa0e7538aaca1ae75d92cc4f0d2c` | 0 |
| packages/appkit/exports/utils.ts | 38 | `e8bf1b1ef48dab1db73fa63cadcf1c3c1c352dd93919ffc865e2d39abfb78ad5` | 0 |
| packages/appkit/exports/vue-core.ts | 2971 | `b92288456346aa5d5fed6be46bb8509e4ed1a45e4bd8b974224f6ee4b30f2b1e` | 0 |
| packages/appkit/exports/vue.ts | 3247 | `a57604c13efe6607015292b5413dea2b3a98ba2f97bc2e1c4f5d5442b9f4a6fa` | 0 |
| packages/appkit/package.json | 5076 | `91d1cc3f420025f41d0b9266ad39d13bad67c4b0c9f8701a14871436633a94df` | 0 |
| packages/appkit/scripts/appkit-version-check.js | 6752 | `c0cee122dbe4fd506a71c0530206068f35df89c748ccdf23854b9e11ceba4d0a` | 0 |
| packages/appkit/src/auth-provider/W3MFrameProviderSingleton.ts | 1639 | `b7a585d9f39a3de23847bcc6c03b135c6a247c1cde35246e2f43dff0de4e0a64` | 0 |
| packages/appkit/src/auth-provider/index.ts | 47 | `b8cd04e2561a6330ef52a4006cf51e9a2b52aba4cb6da6c94bc3a65e376c9854` | 0 |
| packages/appkit/src/client/appkit-base-client.ts | 93982 | `24678f82744aa7ab3665506115deefea88a6ad57df7d187be66470925e03613c` | 0 |
| packages/appkit/src/client/appkit-core.ts | 2659 | `243e2bf787d961191614af435ab204b1578a067947e877a70793a8c4d97164b0` | 0 |
| packages/appkit/src/client/appkit.ts | 24230 | `8f6a38d3319ec0f29ef5d6c17ba385b72f08da2eb9df211a1b26445c7c51c0b0` | 0 |
| packages/appkit/src/library/react/components.ts | 916 | `4f127ee0f0bb6fb93bf41de556ce284429893bd866693aba1616f44ef2975489` | 0 |
| packages/appkit/src/library/react/index.ts | 5715 | `4df10f78613ed27d03f17c77f00c8dc69433fe16f27d003065a2bfe1b2d279dc` | 0 |
| packages/appkit/src/library/react/providers.ts | 887 | `ce70e1d9b8f2efbbdc72ab27cd2a79554658acbc454a881d423c8abe674f9252` | 0 |
| packages/appkit/src/library/vue/index.ts | 5163 | `916273920b6f16175dfe336981f09d567192358f3df07edd78c314ffe5c008b6` | 0 |
| packages/appkit/src/networks/bitcoin.ts | 1147 | `d3e98fb66a8a3955a3b77d34a871dd17bf2f0b06a74df9de8267bc6b6699ac1a` | 0 |
| packages/appkit/src/networks/index.ts | 586 | `f75f1825ed6743977ae1f99f1746b67f2093999055bd17d9c7bef0d89ef4d848` | 0 |
| packages/appkit/src/networks/solana/index.ts | 97 | `2d02ff2f994491f93acbd1936a85d6198a7b61279515b50f1d8f3d0d36e4e702` | 0 |
| packages/appkit/src/networks/solana/solana.ts | 569 | `9d4e6b63dc5848653537af20635ad5362896023e17a1965e5e5be6cc6c2908ed` | 0 |
| packages/appkit/src/networks/solana/solanaDevnet.ts | 580 | `928da99f00cfc2d392e1804333cde49cd5f9bde036f09bbb36c755b162fceb9a` | 0 |
| packages/appkit/src/networks/solana/solanaTestnet.ts | 513 | `15f718db6a05e130d8d1e209fb9cc4da0252285b7e9e91c63e3e4180e178a1ab` | 0 |
| packages/appkit/src/networks/stellar/index.ts | 65 | `26e5b8d53fbfe7ece239a8af6af14a57b711b3920e8baa0532d834ef3576de5a` | 0 |
| packages/appkit/src/networks/stellar/stellar.ts | 540 | `43696055534c26865744622ee40bce8738f20e076eee009524000a93dc4850c7` | 0 |
| packages/appkit/src/networks/stellar/stellarTestnet.ts | 574 | `25bdf3bd4303f6259ac222e82205c70f2e696cfc8546c8419d4ece0a5ca529e2` | 0 |
| packages/appkit/src/networks/ton/index.ts | 57 | `8170159d61c382bcd96cdaa20b9965124af6e86038890fc298a26b1a2c265c87` | 0 |
| packages/appkit/src/networks/ton/ton.ts | 426 | `09e1ee8f5a0d6875a1cc1d148949a8ffbd16f386316a98d200e790aa621e0b09` | 0 |
| packages/appkit/src/networks/ton/tonTestnet.ts | 444 | `7aa5716422ecbe151875fb0bd52c9bd339fa97d735a24878c2c5b08f81012b5e` | 0 |
| packages/appkit/src/networks/tron/index.ts | 88 | `305ca92595c57d5c2c1caf02e834996daa8f2907ff2fb539828bac39f1f37128` | 0 |
| packages/appkit/src/networks/tron/tron.ts | 509 | `4ae36dc3c3a06067d106725d745be9d95f25dec9e9acd02204b50be9e7ea41b1` | 0 |
| packages/appkit/src/networks/tron/tronNile.ts | 520 | `4336589b7e349fe7e239d49ac7a13a408821e3d452f12741d4dd6f8ddfe5da89` | 0 |
| packages/appkit/src/networks/tron/tronShasta.ts | 534 | `0fa02e8711e03bda1771f8d5d7c89d7fa00b2cc2a42763605ab8c58fa0e7d7ce` | 0 |
| packages/appkit/src/networks/utils.ts | 447 | `d19eb743e7acbe3a57df46b429e0a3298524064f4927da908744be1b3fd621c3` | 0 |
| packages/appkit/src/universal-adapter/client.ts | 8305 | `50aded933ab0e4c1d412c1da3b06ce693cc398ba8a84601b823cdb9ab29641f4` | 0 |
| packages/appkit/src/universal-adapter/index.ts | 47 | `d684a6e655bcff70c83fc5f0cc7afe47597fda7ba795253c2462b049c348205b` | 0 |
| packages/appkit/src/utils/BalanceUtil.ts | 1122 | `8362b33727f931bce55628e1bed4a3db5c27c09d75c8dea969c84efd3319407b` | 0 |
| packages/appkit/src/utils/ConfigUtil.ts | 11426 | `ecbf18afba7bc65ed65a1ad031f6c3ff6661eab223a61def12e073dbc3d6fda6` | 0 |
| packages/appkit/src/utils/ConstantsUtil.ts | 137 | `ea546311700fe897cfda77a2d03846c42ad58a27620bcc4c1665ec234df89146` | 0 |
| packages/appkit/src/utils/TypesUtil.ts | 3829 | `47e391c0075f9b0d65159d4ad0d58980a606d0e26c5d51f90dda1c85961d273f` | 0 |
| packages/appkit/src/utils/index.ts | 66 | `4561824c797415c40c7c33768d3f476f1e64306bc338deae409b93db5ded4de1` | 0 |
| packages/appkit/vitest.config.ts | 492 | `ce095a937997794be07f83838df8c8d612718b41bf4aa68044102c461bb1c275` | 0 |
| packages/appkit-utils/exports/bitcoin.ts | 111 | `6b080c4fb5b45b9e86adb88442975d2259674ccd8d1e56412e31c8804325522e` | 0 |
| packages/appkit-utils/exports/ethers.ts | 345 | `15dc1f37dd2304c7c251bad30f83d2878277d72cec1f98244696b063fedf8fbc` | 0 |
| packages/appkit-utils/exports/index.ts | 1454 | `8cffd044bd75199ba8a90ac37cdcf1dbe2d819082f6a8be3cd29a0e14b0bc38e` | 0 |
| packages/appkit-utils/exports/solana.ts | 159 | `b8208aee6b89c8ff261acb0376f1fcd75e04fc059d5533f34c8b6bf1bd88b1ea` | 0 |
| packages/appkit-utils/exports/stellar.ts | 56 | `e3af14d985148d0c6cb58f96acf98c395eda65f43bae0b8c101956ce22ba8504` | 0 |
| packages/appkit-utils/exports/ton.ts | 48 | `3c4a4443d74945ec6b4c598d57f8b3ac55e3e88d5770aee1ac75446a6c0c3ed3` | 0 |
| packages/appkit-utils/exports/tron.ts | 50 | `e803f36665ad48e89023428b0e985a74a79ecb25daa765a04ae46286312e7298` | 0 |
| packages/appkit-utils/exports/wallet-standard.ts | 112 | `dc8a093c72b7851f2ff55d0922936e9591bab7092aa26dd226831c4bafdc1013` | 0 |
| packages/appkit-utils/package.json | 4049 | `d867c64a8b0690a70d9be9f60f9149716bf1f74b87df7850baca7159724f36ac` | 0 |
| packages/appkit-utils/src/CaipNetworkUtil.ts | 10226 | `b2968495bc219d37064396dcf40b8901e9c48beccb74e9180c99e9bdf4dc3e4f` | 0 |
| packages/appkit-utils/src/ConstantsUtil.ts | 2370 | `80f940fabc804ebc605b9438fe314e8ee2e5a2a041cf2267421ca50b6f646cd0` | 0 |
| packages/appkit-utils/src/ErrorUtil.ts | 4263 | `229aca3240298167a533afdf0674619033de253b9872d803a01ab877ac603ae2` | 0 |
| packages/appkit-utils/src/HelpersUtil.ts | 3836 | `199cacdb1033d0338cc75e64ed7ed4108476e99215e89ec3ff3d291e89f0c677` | 0 |
| packages/appkit-utils/src/LoggerUtil.ts | 606 | `70b01b7fe5b5f717503eccd52a36696b721c2b9b28ea1dd212df58fb039d29b1` | 0 |
| packages/appkit-utils/src/PresetsUtil.ts | 8423 | `81b38af965aa27015b9c90e8027b559879cf23bbd0ef4998831946061d62e522` | 0 |
| packages/appkit-utils/src/SemVerUtils.ts | 2958 | `9c1f5e6989cf086810c27a34fbbf37f3077ca308b92bb06b21d9aeeaa93d6a6a` | 0 |
| packages/appkit-utils/src/TokenUtil.ts | 534 | `e8158b39cca86869bcca76e55e237f95fbfc00d41f0a91e0ffc5d177ed3ffb0a` | 0 |
| packages/appkit-utils/src/TypeUtil.ts | 1216 | `9c27bd445ee290aa6bcfaef98850901980203766a0748bc73b21edc535c9f941` | 0 |
| packages/appkit-utils/src/WCNamespaceUtil.ts | 2873 | `0a89246105c2c2891469fbef02f5210f464a48cf8f3fecc36961ceeca3115750` | 0 |
| packages/appkit-utils/src/bitcoin/BitcoinConstantsUtil.ts | 96 | `eafee408c9fcd691708d710dd1d02dde0fd5579a0ade3dd9e58a9948d726f692` | 0 |
| packages/appkit-utils/src/bitcoin/BitcoinTypesUtil.ts | 3786 | `dc280d84a68c9f60e56120df561e9330920608e6d3a0ad411e86a275c6eed2c2` | 0 |
| packages/appkit-utils/src/ethers/BaseProvider.ts | 1319 | `a6c9b6f6a5486e04209f6cf3d7094c084c060e975a344f0e6c820b48a14b6db0` | 0 |
| packages/appkit-utils/src/ethers/CoinbaseProvider.ts | 1450 | `1e4761b8582e1583792c4ddf4222956b43d48214cdc66c2519fbf49910ca1db6` | 0 |
| packages/appkit-utils/src/ethers/EthersHelpersUtil.ts | 1903 | `63eaf038b205f3d73e6938a21681232645e7e4163eae0e1871961c3225ecc5d7` | 0 |
| packages/appkit-utils/src/ethers/EthersProvider.ts | 360 | `59c09958fd0dbd2e978d34dfb77c4bfbfaacfec65db5ef365da074036b4be534` | 0 |
| packages/appkit-utils/src/ethers/EthersStoreUtil.ts | 2558 | `eadf95d7bcf0bc8633529cce9b3769dcc76330659af22d140f8fb88db0a344d1` | 0 |
| packages/appkit-utils/src/ethers/EthersTypesUtil.ts | 1718 | `adcf4afbc6de47f1f69b610c9b12785238237457376960c6b9f2b4c4755116ef` | 0 |
| packages/appkit-utils/src/ethers/InjectedProvider.ts | 445 | `d56786d2295b41009d1d46cf70cca25be20b5bbc83e01a8eb1bb67c4e2cae164` | 0 |
| packages/appkit-utils/src/ethers/SafeProvider.ts | 1302 | `95d22939f7ed673935e72ab6e761af17833a20089c1523d0a1fccfdcc7a2ebe5` | 0 |
| packages/appkit-utils/src/solana/SolanaConstantsUtil.ts | 1892 | `280f0dd09e6b9447f123f3d7cc522f999b6675c65b13363ade8b4955e3d5b8cb` | 0 |
| packages/appkit-utils/src/solana/SolanaHelpersUtils.ts | 1142 | `1bdf75715b9f08d22eeca1f340d396489631d630596b856bb0a35685774f43bc` | 0 |
| packages/appkit-utils/src/solana/SolanaTypesUtil.ts | 3938 | `34c122bcbd05e8143c6805938632fc97fac39ab02bffc973064f4d09bf322219` | 0 |
| packages/appkit-utils/src/stellar/StellarTypesUtil.ts | 2408 | `d780e42c69d5f52eee5acfadfc19148b311de8d87df471e91868b23898b3a965` | 0 |
| packages/appkit-utils/src/ton/TonTypesUtil.ts | 2315 | `fc33213aee03bc01c68bd0bae5b9132ff98f6c5d1fc322c1c9d4f063dd5b1d9a` | 0 |
| packages/appkit-utils/src/tron/TronTypesUtil.ts | 723 | `d466fe52edaeda2603c95ad49b538684054f1a2686d559f725216101fc3f31ac` | 0 |
| packages/appkit-utils/src/wallet-standard/SolanaWalletConnectStandardWallet.ts | 14997 | `0a9df151fa68dceb1c92f32c72d86c50cad2f877e26ba92d7ae05a494f4cad57` | 0 |
| packages/appkit-utils/src/wallet-standard/WalletConnectAccount.ts | 1208 | `346834391b11634ee66715c3eda32898debcc65416b68abaea8c1e4187081dcc` | 0 |
| packages/appkit-utils/src/wallet-standard/constants.ts | 157 | `6f901bcb7022687d2d4585c98199bf3bb3705017d0c59db914f658a28a2a9f0b` | 0 |
| packages/appkit-utils/src/wallet-standard/utils.ts | 621 | `8d6b4c43a8476f905d9fe87809c9cc485d95323998cbce2e78bfead4281fd57c` | 0 |
| packages/appkit-utils/vitest.config.ts | 80 | `edaa4113ae35e9507b5f1538604b5cc4120506d5631421e5068eeaadeec319d7` | 0 |
| packages/cdn/lib/appkit.ts | 1637 | `8031ca9f01d34803580af579ee442404e9697ad4a0bd1ac28348f55806e9ffa2` | 0 |
| packages/cdn/package.json | 1407 | `a265a6be43f92b619e5cf598fcfc46cfb6a8cf750aa88524a9a3760fc78be073` | 0 |
| packages/cdn/vite.config.ts | 526 | `d31e1391fa913d80770bb6edb69dcaf9d4caebbc874b0ff3a15c03995d301e7a` | 0 |
| packages/cli/index.js | 2300 | `f4957544aa37cfa7879d307ec5ee88c18fbdd3af407396081fdb16142c5e5095` | 0 |
| packages/cli/package.json | 865 | `73eff06f6e3cdd07836aceb89f1fb781f629160b09fa7cde5e91c0f01bb0f518` | 0 |
| packages/cli/utils.js | 2607 | `02fb25d2fde19d0a5136013a063fa0dbdd40d4a38962a234dcf8de75a4890c25` | 0 |
| packages/codemod/package.json | 811 | `b2091298a892d50a1a1e23d44ee1cd7ea9ad8c24c1cd6d65c0e27fe908ef82a6` | 0 |
| packages/codemod/src/index.js | 457 | `e2bff5ba2c3f0d14ae112f22624d42ca55a796e1efa08b03e569cc7edced241a` | 0 |
| packages/codemod/src/utils.js | 4685 | `8c48c5758c1b6561399741c31bc2c720f12d0e6a2be3d2430a0a2c1d20144a8e` | 0 |
| packages/common/index.ts | 1509 | `2b45a999923d676f6501494d7704372b19b21e8fa31e6a15b30549a1dd2a6797` | 0 |
| packages/common/package.json | 1419 | `af006f311fc283e9524480fe34c1b99270575e7cec9a604fad973af1c264794e` | 0 |
| packages/common/src/contracts/erc20.ts | 717 | `7b09e75b214143497cb14b94ad6233486a277851f4fff010caa5e3f947323f8c` | 0 |
| packages/common/src/contracts/swap.ts | 261 | `88d8fa2d66c961c72bcd277238e7c7c00bf1571935348d5a917662387c790a19` | 0 |
| packages/common/src/contracts/usdt.ts | 669 | `91e313ba8db5fdbdd3eae43996e5240caf84c061cc96d59db753fc05128545e2` | 0 |
| packages/common/src/utils/ConstantsUtil.ts | 7023 | `6187f5db37013cafe73d4af58adff26e6e099b5b635a01e1918792e977b9d261` | 0 |
| packages/common/src/utils/ContractUtil.ts | 488 | `b59190fb80a591360ba1aeb6186798211ef56593273d894155bef48c43c4720f` | 0 |
| packages/common/src/utils/DateUtil.ts | 1184 | `a6b1c1c9d9662fee866c9985d33545ccb9ff0dfee653bc8eba28cc562c5f65f9` | 0 |
| packages/common/src/utils/EmitterUtil.ts | 1180 | `42880dfc1658b1a8de774be089538a64ed1de04f89af638454e54e319e0a97ba` | 0 |
| packages/common/src/utils/ErrorUtil.ts | 3260 | `b2da66c489a9301d081fb4dc4e941958de05b393472cf4ed284a05a8d619602d` | 0 |
| packages/common/src/utils/HelpersUtil.ts | 141 | `0588b5e9233a7d08da3dcef2648e54f105aa375cfc51284851969b825223edd0` | 0 |
| packages/common/src/utils/InputUtil.ts | 2190 | `2ed5fd3bd348cd14ca3c4d73eaddf51c7f8055db88395c153a0a34804cff28d4` | 0 |
| packages/common/src/utils/NamesUtil.ts | 224 | `41f80e7f5f66f8fecfb0ae49498a40bb6300a02ce68d9bcf2ce5ca54e55a9604` | 0 |
| packages/common/src/utils/NavigationUtil.ts | 89 | `bf129ebf25e10d18df593c3a4ef44cdcd5761af4d71f841e1ae25254dcdf5a33` | 0 |
| packages/common/src/utils/NetworkUtil.ts | 1439 | `b89fd84f448bc8310865f7086d8103a1adf5056b23c660eceefdb3597499bc01` | 0 |
| packages/common/src/utils/NumberUtil.ts | 3394 | `95f4ac24fa17016d619d7d36c1f87fec8b6849af8f6dd7b6964f34fcdb18a751` | 0 |
| packages/common/src/utils/ParseUtil.ts | 1511 | `b5a16755f82ca510743dd89db691139c2440fbb50a9536d4e08dbc53297b56e3` | 0 |
| packages/common/src/utils/PresetsUtil.ts | 7981 | `927f8faaef92eb83d14c6b5548ba381ee4f1ef627fd42ccd3eadc661a25cf6a9` | 0 |
| packages/common/src/utils/SafeLocalStorage.ts | 3862 | `10fff1174fff35ce4ddeea46d3db2060430d42bde239eb4bb57d1d50e92a94b6` | 2 |
| packages/common/src/utils/StellarStrKeyUtil.ts | 2864 | `3f701c89aa4cc0cea1ca87b655ee9f1c85964be53b8dd994756188739852f193` | 0 |
| packages/common/src/utils/ThemeUtil.ts | 1342 | `1b982885ac2464d01104c3ccf1ae1d6bea7d84cf6610dc3e4519e39ecd2c62b9` | 0 |
| packages/common/src/utils/TypeUtil.ts | 5739 | `1b9c3ae3ceac0bcd51bbc08975e8cc393fe24cf754ece182021415deac7ee2ad` | 0 |
| packages/common/vitest.config.ts | 80 | `edaa4113ae35e9507b5f1538604b5cc4120506d5631421e5068eeaadeec319d7` | 0 |
| packages/controllers/exports/features.ts | 67 | `a14ffc56cf290953f371861d3c8b87ffaeff73df5e4fd315aa5d1d04d85b5ea3` | 0 |
| packages/controllers/exports/index.ts | 6735 | `f3e1097ac66769c9365951b723968a5a30277fa83148a93db572ba6f6f0ba1b6` | 0 |
| packages/controllers/exports/react.ts | 21235 | `06a097f966385cd288a55667ea18eb87aa8bb00ad27d10d7da3d7a1bb6897495` | 0 |
| packages/controllers/exports/testing.ts | 2948 | `75f237777bfe51d72df21068a7af61dcf86c26db3fcb495335b2a9a034f7ae19` | 0 |
| packages/controllers/exports/utils.ts | 770 | `22adfc1244f3c3903e2b733853097ae82c985246407109d1bc90e25cb2039f20` | 0 |
| packages/controllers/exports/vue.ts | 11966 | `cecb13d635203e2bbbfbe952512673570ae2d586044ff8dad43c3638aae20ba6` | 0 |
| packages/controllers/package.json | 2815 | `c842dc7b46dbc59fd02b2294fde53f87732b9174f094c393f9a07cc8ba42c232` | 0 |
| packages/controllers/src/controllers/AdapterController/ChainAdapterBlueprint.ts | 29765 | `ca10a1e23038df7a96761af3a6bb907d580428eec0257638bb8caef09ea51417` | 0 |
| packages/controllers/src/controllers/AdapterController/WalletConnectConnector.ts | 3200 | `be37fd42789177fa49bb6bab92634bda4d82614043310728b8be8f7e25d6b5be` | 0 |
| packages/controllers/src/controllers/AdapterController/index.ts | 517 | `d83e5225bc0fe827f518a8fa7e0f58279ae9d66378998b03cba5615461de3285` | 0 |
| packages/controllers/src/controllers/AdapterController/types.ts | 200 | `80d035be7823c84f0133512090b8c90f846026fa9043648958fc94e67843b17a` | 0 |
| packages/controllers/src/controllers/AlertController.ts | 2391 | `372498f1f5d9a0b664800c1a786a87b7d9aba66f0e724558de37bfbfc31d00b1` | 0 |
| packages/controllers/src/controllers/ApiController.ts | 18825 | `d7ddec0a3ae7236872fe5afb30816609c04f175882d430205e5b5c282954db5b` | 0 |
| packages/controllers/src/controllers/AssetController.ts | 2022 | `be934a59c3d1ee809c2d9ef19177954cf593b3adebe26f4902fadbf3685d067d` | 0 |
| packages/controllers/src/controllers/BlockchainApiController.ts | 18745 | `45cba5266169f33aaf88cf38d3f6d8c64ca8923c4f6368add638d18bbb98a37a` | 0 |
| packages/controllers/src/controllers/ChainController.ts | 28085 | `26a5a9ca47f41fe75df3c795b1491b49e8a05e2534bc3cb7a7356b5b8641e596` | 0 |
| packages/controllers/src/controllers/ConnectionController/entities/Account/Account.ts | 1636 | `c56a51e231bae8169fbd145f3c5a491473f6de17159a608f2ab4d6741a67d1d1` | 0 |
| packages/controllers/src/controllers/ConnectionController/entities/Account/BitcoinAccount.ts | 592 | `6b2dacd67fed2adb793a53512b6cdb37d2f39f6fa5b9e33efb0e760b834fd6e7` | 0 |
| packages/controllers/src/controllers/ConnectionController/entities/Account/EvmAccount.ts | 735 | `aedecc97cc0a119dc47d153c76bed2a51aa1df50ccdf8c9bf2986d3e308c86ae` | 0 |
| packages/controllers/src/controllers/ConnectionController/entities/Account/SolanaAccount.ts | 630 | `d7196e5c0024696decb45dc543dd98193150cc4d19dc1d729b34378a496bd193` | 0 |
| packages/controllers/src/controllers/ConnectionController/entities/Connection/index.ts | 3792 | `ceb9ea3197502201e0af9137a5ddb88efc7960f0d0c685943fb038f3e3ac8894` | 0 |
| packages/controllers/src/controllers/ConnectionController/index.ts | 5866 | `b8bacbfc830176b41f26840fc541b9801af0bcfc8f919eefb8e9988fa54b852a` | 0 |
| packages/controllers/src/controllers/ConnectionController.ts | 21559 | `29eeac0363aa6d47d1688b7b98f649a61a2d0cbfaa95801baf08eab6724bbbdd` | 0 |
| packages/controllers/src/controllers/ConnectorController.ts | 16744 | `5c0514490f2f4d6d31d7a9aba790163020b8f25851ea8c034381b7ed58fb6281` | 0 |
| packages/controllers/src/controllers/EnsController.ts | 5452 | `814de2069c0196d0f6603bfaf822e5636d378c1e416f85fe0bfad41baf260d5c` | 0 |
| packages/controllers/src/controllers/EventsController.ts | 6350 | `6ce0c5ec057015c36424e48404aee1c102d24daa95fd51ff0f5e2d83fc6caf63` | 0 |
| packages/controllers/src/controllers/ExchangeController.ts | 10813 | `c8bbcf41a077562860bd3bf04300ec43d4103750667cc449294efe455d417e34` | 0 |
| packages/controllers/src/controllers/ModalController.ts | 5419 | `86baf1077fc26d493801784923003fe33f737ea554f798cd24e1b8c510acf3b0` | 0 |
| packages/controllers/src/controllers/OnRampController.ts | 5958 | `e7ffd09ea4d2575d4b626628a54c44a8afbca9e89a04092484c6adfa62c1ed98` | 0 |
| packages/controllers/src/controllers/OptionsController.ts | 15084 | `e1c4d4505a28e8cb00d3c6fb452594093f99ed2027a5d9b897a16725bf256e08` | 0 |
| packages/controllers/src/controllers/OptionsStateController.ts | 988 | `c02d8008d370f1138dbf51c887627a3782fb42fa3ccccad7734d29dba9ae0acd` | 0 |
| packages/controllers/src/controllers/ProviderController.ts | 2812 | `5ecd5c52f6afb101fa86ddfa7aa8ea84320ddc7414634704b0ec9fcde52aee88` | 0 |
| packages/controllers/src/controllers/PublicStateController.ts | 1999 | `82a3d8f870bff258ab5e05f324b1c8c327becb1d48a41a7158c0232a62cd7313` | 0 |
| packages/controllers/src/controllers/RouterController.ts | 7497 | `204a6eb8936cb95f4ed741791676b923b3a398261e3580ad9af4a063a1ae6faf` | 0 |
| packages/controllers/src/controllers/SendController.ts | 12893 | `f9a604d32b6993de0a89cf35c821af182b7ab48b1d8b0fc590bcfabea482715e` | 0 |
| packages/controllers/src/controllers/SnackController.ts | 2603 | `8f9705e7e2d7c46504f29ba878475e5cf74614b207b837ade79c4c6ddf99f5d8` | 0 |
| packages/controllers/src/controllers/SwapController.ts | 31780 | `318ee268347f26558033c3db1feff581c9ecd22d732973f1e67ffdb64d84ce6a` | 0 |
| packages/controllers/src/controllers/TelemetryController.ts | 3115 | `8c90d3a148d1d5d86dc3f30d939890d04f527be08620f88c83a2960373173656` | 0 |
| packages/controllers/src/controllers/ThemeController.ts | 2426 | `3a352e5d7ee3095a332f44d752b1076d6ab75ebb7eafe667d038bc4da4f0003b` | 0 |
| packages/controllers/src/controllers/TooltipController.ts | 1653 | `27d8c6d32cc28d8b86a8f3dd293a1e2ca97f0a3345f3f245932357e3ded671f5` | 0 |
| packages/controllers/src/controllers/TransactionsController.ts | 5314 | `62f9e2ee3074689f778948618b9a9d6aa03a3184137b09c30fb61788c7d621c5` | 0 |
| packages/controllers/src/features/siwx/DefaultSigner.ts | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| packages/controllers/src/features/siwx/reown-authentication/ReownAuthentication.ts | 14469 | `b28d34300916eea0282b1a5214e247c7f82a4bb5e4ba5b28a818dd0d1604c600` | 0 |
| packages/controllers/src/features/siwx/reown-authentication/ReownAuthenticationMessenger.ts | 2813 | `b684c6025e0d7f18dc53174ab039269ca24bc507d418f1cbff3172b56f9c3318` | 0 |
| packages/controllers/src/features/siwx/reown-authentication/index.ts | 91 | `3dfe499d48d07f6d08ed3e4eda3cf9f372758fc7fd91d48d8417abf01d38febc` | 0 |
| packages/controllers/src/features/siwx/types.ts | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| packages/controllers/src/utils/ApiControllerUtil.ts | 1076 | `c21bbf00affe16e9ab9e1857eaa25469a5aa200b994485055a5be128724bcc9a` | 0 |
| packages/controllers/src/utils/AssetUtil.ts | 6405 | `b1597ad1f49d54a154c840bdb280b14ad55c0caf0e24443e2be8c4bddca37f03` | 0 |
| packages/controllers/src/utils/BalanceUtil.ts | 5761 | `262a92ca1cefec34f436b53f2cd644bae5cd30c6f5f5960ca7807b563b99f5f1` | 0 |
| packages/controllers/src/utils/ChainControllerUtil.ts | 3575 | `0d7cc62f5b15c4cb5e6a9c24eadfad0a9332eac0f7bdecd3549574a0407920b4` | 0 |
| packages/controllers/src/utils/ConnectUtil.ts | 5457 | `464ee8a72a8f3f08d33189107ec626f89e52aec39933932523d9957c18ca5ec7` | 0 |
| packages/controllers/src/utils/ConnectionControllerUtil.ts | 5973 | `0932bcd9d79fa5b84faaa91577a23f2be243fc9684678b323323e31b96f35c02` | 0 |
| packages/controllers/src/utils/ConnectorControllerUtil.ts | 12253 | `8e91a699b1138fe6468add88e09307c4a1f86dde40ca7b43fee7f22c346fcef4` | 0 |
| packages/controllers/src/utils/ConnectorUtil.ts | 15903 | `c5ba4e4734b1fad53838dbad1e339406eb9dadb8271f4b7ea1823639a02d4cfd` | 0 |
| packages/controllers/src/utils/ConstantsUtil.ts | 7026 | `f17f632d142e1c1231393439f34e27334ec68e4f56fe39568a0dac2dfa22658f` | 0 |
| packages/controllers/src/utils/CoreHelperUtil.ts | 15098 | `65363998fa63f4399bb6353c9268ef073de77783b777eab7ca3d57abddcb7fca` | 0 |
| packages/controllers/src/utils/ERC7811Util.ts | 4743 | `894f0635c63e489c3507b1c661dd1f26d3211556236aed76623f8b4296a8472d` | 0 |
| packages/controllers/src/utils/EnsUtil.ts | 240 | `667e407bc2d67210ad79751591a9933c6153e0a21839dae481621d70b9fc2f94` | 0 |
| packages/controllers/src/utils/ExchangeUtil.ts | 7956 | `45cc6b1723e0999f7ea85105942088fdd090a95528eb2151df7c2762881f8c3a` | 0 |
| packages/controllers/src/utils/FetchUtil.ts | 3038 | `890d6307a895e320c71f4158b02283005442155c323b126afc10eff9e05a81f7` | 0 |
| packages/controllers/src/utils/HeadlessWalletUtil.ts | 11045 | `f2d6dbf5e39ee5bfa225b6515432243088c9ef859c1009ab52e02428a317a57a` | 0 |
| packages/controllers/src/utils/MobileWallet.ts | 7112 | `11692fd570365882e1d6dfb5d8bb78cb9411c2f371f2dd7460038ae87a138840` | 0 |
| packages/controllers/src/utils/ModalUtil.ts | 1015 | `02a1271acec9de5caa984a84c2a87470bf087ab1763c6ff9fc5e2b51ef4cfce0` | 0 |
| packages/controllers/src/utils/NetworkUtil.ts | 3095 | `fa70a59c91e3d162c0ef5f88b4cfc7a0a5c7c62a9cbb2921ef6fc6c7b7ab0f17` | 0 |
| packages/controllers/src/utils/OptionsUtil.ts | 1743 | `aee9bdfef7532f5f8f8e3a25896bbe5411886b9e20191d4acc5992a7ae1298f4` | 0 |
| packages/controllers/src/utils/ProviderReauthUtil.ts | 6688 | `94d3d322f45877e17d86cd7856adfb26a790c25baa5ef9e09859005f85c8f916` | 0 |
| packages/controllers/src/utils/RouterUtil.ts | 641 | `10d55e524616535417f1245fbddeb6628a162b79488aae0284f8396a5d768bf2` | 0 |
| packages/controllers/src/utils/SIWXUtil.ts | 21265 | `4d4ca9524b65d9a6b8881eced8c8d6be7f7a55fb1adb7896803b73d21f1765df` | 0 |
| packages/controllers/src/utils/SocialsUtil.ts | 3649 | `5f0ad365f72f0cacec2db80f1dc047d5ac715bf9555efd7f1b8b72c550446e78` | 0 |
| packages/controllers/src/utils/StorageUtil.ts | 29774 | `85829255583c7b2648deb2d8a110fc2484c9bee8963abd13897e3ebe834d84e9` | 0 |
| packages/controllers/src/utils/SwapApiUtil.ts | 4362 | `1a9550ee0af14722fd703952a37e94103af8431602923257197c756fa10f2046` | 0 |
| packages/controllers/src/utils/SwapCalculationUtil.ts | 2566 | `9fe0e6fea29fd98ea6d1f69dea062a7ce6ab48233553a38475e01b8240a8dba9` | 0 |
| packages/controllers/src/utils/TypeUtil.ts | 35398 | `3e7d1689bdd2ec26c9bd185edbf8502706bf4f74662b770c321bd57f3eb6d418` | 0 |
| packages/controllers/src/utils/UrlUtils.ts | 5343 | `8ff9d73c230d4114f3e3bc1a8928294b6a4aed0d6c61de6225d3494b95b05a45` | 0 |
| packages/controllers/src/utils/ViemUtil.ts | 2440 | `0e5adaa737f34320722bf37f20c82bce3ae17da3b77f5cc3e6817ae872d281e9` | 0 |
| packages/controllers/src/utils/WalletConnectUtil.ts | 14952 | `da32a712acc8a4f308074e640dc021ec5e402ef205da8de6c584ec5e6a13d1d2` | 0 |
| packages/controllers/src/utils/WalletUtil.ts | 7574 | `6bc82923fb51a71f39b1e35e0a9f30d8a7d5b8c73cdae0af3d2f2e913b238554` | 0 |
| packages/controllers/src/utils/withErrorBoundary.ts | 4256 | `f1767ccf632934bef3e911ce04cef2e31249b119d10e1a7920e9de0439dfa16b` | 0 |
| packages/controllers/vitest.config.ts | 120 | `27d27d7b59d34ecbbdcd94c545de62a0448e5b1385bafda59a561d6109aa8eba` | 0 |
| packages/core-legacy/exports/index.ts | 42 | `850d03b3e1fc6e071f701dd22a0a20814e7e05f538d1e705fc61b7dd88b6ea69` | 0 |
| packages/core-legacy/exports/react.ts | 48 | `0a358decf743ee5cd607b1e4041b1074cede8ef81608c3a72c5b2883fd66192b` | 0 |
| packages/core-legacy/exports/vue.ts | 46 | `fb5a41b4ce0920708dac59c4a13c9729f4e21890081c23392c0c115e8515507a` | 0 |
| packages/core-legacy/package.json | 1999 | `3ee084a5bb8f90f93b8e96c1e1e089e48b2c6a9a4ba00320f5f4808836c1a386` | 0 |
| packages/core-legacy/vitest.config.ts | 120 | `27d27d7b59d34ecbbdcd94c545de62a0448e5b1385bafda59a561d6109aa8eba` | 0 |
| packages/experimental/exports/erc3770/index.ts | 351 | `2f801849ea4ddb10a904b9353fee4c54ad06c42e29fd43ad5625d761ccf9e3ac` | 0 |
| packages/experimental/exports/index.ts | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| packages/experimental/exports/smart-session/index.ts | 1403 | `6a4641ad28e100e86e4dcc3d22a5b57ca11c350740f85641f0d6af8f0fd96695` | 0 |
| packages/experimental/package.json | 2347 | `ee1293a90a9a8d61a453682002b898e33596e35387e27cb47c189e1d56a0ef41` | 0 |
| packages/experimental/src/erc3770/utils/ConstantsUtil.ts | 48459 | `0f93decdce28bf3904030d777a2fe1ee67f0b4f4a2af90c5dbd6c9f291f65104` | 0 |
| packages/experimental/src/erc3770/utils/ConverterUtil.ts | 1407 | `c93565b02260cd2f6bd44b57b1008e95a3692345df208b18b5d99cf8c076f9b0` | 0 |
| packages/experimental/src/smart-session/controllers/SmartSessionsController.ts | 8820 | `61fe337abe90357c4a24456c481fc44bca7d6b159aaf34b98e7c34d4a77358fb` | 0 |
| packages/experimental/src/smart-session/helper/index.ts | 5119 | `3873c67482c1bd97f60285df391b28d31c0a399d2669d3d8dec34e4f2ebaab16` | 0 |
| packages/experimental/src/smart-session/schema/index.ts | 5810 | `d7d9f49464705bd48cb0596fa16aba907bae21188c52367c0ee9e091e7b21ee5` | 0 |
| packages/experimental/src/smart-session/ui/permissions/wui-permission-contract-call/index.ts | 2743 | `c27481f4d5a449f7fedc96c4c6588447b9eb67c971469eb399a21672e722fc3d` | 0 |
| packages/experimental/src/smart-session/ui/permissions/wui-permission-contract-call/styles.ts | 155 | `ef494dedbfc9d040cdb033eb96a07b71b249c827a59598e0ef67501bc51883d8` | 0 |
| packages/experimental/src/smart-session/ui/views/w3m-smart-session-created-view/index.ts | 2482 | `29c0b97915405c8cae2b77eb88a278683383e49e65f074224d582fe2eaefb12f` | 0 |
| packages/experimental/src/smart-session/ui/views/w3m-smart-session-created-view/styles.ts | 101 | `fdf80c8e58cf8f236dc045278409779412eb8099b33edca58dbf6ba284c49065` | 0 |
| packages/experimental/src/smart-session/ui/views/w3m-smart-session-list-view/index.ts | 8198 | `d778c49a3e1a44ee16c1152c6c43e0a131c7965566abe4a6b29289f279391fc6` | 0 |
| packages/experimental/src/smart-session/ui/views/w3m-smart-session-list-view/styles.ts | 709 | `76f1716e0c16a373399275d88e95ea3a3756c292140a0c64c8440995256096c8` | 0 |
| packages/experimental/src/smart-session/utils/ConstantUtils.ts | 155 | `859e6af5d4b290df94716b1c8041dc26b9ae4e2a9e992527589b6a92c884e012` | 0 |
| packages/experimental/src/smart-session/utils/CosignerService.ts | 4947 | `bc90670a409bbd766137d6d45f9885ac05d9caba93b78278a6e7be314ecac476` | 0 |
| packages/experimental/src/smart-session/utils/ERC5792Types.ts | 593 | `806e1aa88cc9375a692a73ef23debef1c10a2fb0324c061d8759ac82d88df116` | 0 |
| packages/experimental/src/smart-session/utils/TypeUtils.ts | 4001 | `7619ba8a0455784a45df8b5e7515b01463edb7ebcb58ff5426b54526a3a19cb2` | 0 |
| packages/experimental/vitest.config.ts | 120 | `27d27d7b59d34ecbbdcd94c545de62a0448e5b1385bafda59a561d6109aa8eba` | 0 |
| packages/pay/exports/index.ts | 1244 | `606ace95713ed66aafc2cd3b0810d8a1e131cccfa1b220cb8b59b8638afe3f8a` | 0 |
| packages/pay/exports/react.ts | 12789 | `7531c0aa56f6e9c31762b30d5e712299cf8e6bf7f6b0f11bbdb3b912375ddd32` | 0 |
| packages/pay/package.json | 1834 | `24f26f139fb48d37529dfb75a28be661a039e04788c92cd77482d4b4ef19760d` | 0 |
| packages/pay/src/client.ts | 4058 | `fae5c46a50ba06a7cde6241853461803c5331c6b9c1c87af19d9131e6be1bf14` | 0 |
| packages/pay/src/controllers/PayController.ts | 25675 | `aba914ad5464a8ab08712378c2465b83ce9889ef4a935d62ef5151dbb11870f9` | 0 |
| packages/pay/src/controllers/index.ts | 139 | `0b8df9c9281b581d1f2ce41cc8b3259a386440f8799490e6950019665a1f71c6` | 0 |
| packages/pay/src/partials/w3m-pay-fees/index.ts | 3889 | `8542b8d38f6da806d6c087ba38f906d92b8a9156bf4f6a861d6360d79868330e` | 0 |
| packages/pay/src/partials/w3m-pay-fees/styles.ts | 179 | `3176e4a32ccb21b64f449371dc994b86991fe88e7f779341655c111f8fb0481a` | 0 |
| packages/pay/src/partials/w3m-pay-fees-skeleton/index.ts | 1995 | `a32ee08b29b45838f8fcea60d056a0835e18a9fc4a23cbe4f24fd7a1d55cb875` | 0 |
| packages/pay/src/partials/w3m-pay-fees-skeleton/styles.ts | 83 | `1e7cc13213dcf0fe4d9db707a94504fcc81dc5e9e3eb3ed7e4d45ffd381aea4a` | 0 |
| packages/pay/src/partials/w3m-pay-options/index.ts | 5955 | `0f2a67fff9bc830a08baf29fa8bb08bfe5e97eed4a9c21337c9a79de384e57ad` | 0 |
| packages/pay/src/partials/w3m-pay-options/styles.ts | 1375 | `9229180fc862e2a509c76fac9d7754d42462563e31c5370a6ada95ab760f9748` | 0 |
| packages/pay/src/partials/w3m-pay-options-empty/index.ts | 2299 | `7c9180b8657815ba83205c97f530b14af93b2b4a26ab552640fc18e4583e5577` | 0 |
| packages/pay/src/partials/w3m-pay-options-empty/styles.ts | 366 | `decb3f5aa5ce6a8f4a29e36f9f60a007605f148c05165ef371e0b3a43e7bdc81` | 0 |
| packages/pay/src/partials/w3m-pay-options-skeleton/index.ts | 1994 | `a40a5192bc1b553125d0c8db4f1081b2fd675d09972d725abf047cac23917aa2` | 0 |
| packages/pay/src/partials/w3m-pay-options-skeleton/styles.ts | 737 | `b8169035766884c541b7fd780dcdaf3a7f82fc29b128481544710d2262c831b6` | 0 |
| packages/pay/src/types/assets.ts | 2874 | `d22b6bbbff76bcc10f670befacb4d33a4f909ba2f121957ba39410742d4da324` | 0 |
| packages/pay/src/types/errors.ts | 3231 | `60b5daf7f75fa0bb1ffe650298bdbc87bc77f7e043906c3bea7bcc7e95a7df8c` | 0 |
| packages/pay/src/types/exchange.ts | 156 | `c67005419b269f0daf628e0bd52509c015999a5ad67ba6cf87b882248956f3d4` | 0 |
| packages/pay/src/types/options.ts | 980 | `a0ef1ca2e01eedc0996d024712aac00cf79738e92511bebc6be157f271b9e65c` | 0 |
| packages/pay/src/types/payment.ts | 86 | `8068a9961fe517cac3a33ae34b640ea4698d9358a582b9089b0c1aa2569a8b1e` | 0 |
| packages/pay/src/types/quote.ts | 954 | `c028122aa55cd8f0b349c65c5b2c6ec515aa347836732d863cc1e9e644366250` | 0 |
| packages/pay/src/ui/w3m-pay-loading-view/constants.ts | 506 | `131bb888995958bef5d79f1cec67a7c709f9a37e7bd4d03e6e549b215dcc4924` | 0 |
| packages/pay/src/ui/w3m-pay-loading-view/index.ts | 15686 | `06aad2a85cbfe693b9a75a981a0dfc4bfbc542809b8a907bff61f006e4999b23` | 0 |
| packages/pay/src/ui/w3m-pay-loading-view/styles.ts | 3010 | `09d94ed523c54426669ac9e056f8fa0d58576579da5b395914481088d0e6bae5` | 0 |
| packages/pay/src/ui/w3m-pay-quote-view/index.ts | 20673 | `8a7c4791272af83da934a6df8ccc81684453e9811c5a58a19522eb441b1d07fc` | 0 |
| packages/pay/src/ui/w3m-pay-quote-view/styles.ts | 815 | `64cc99fb04628299b174c6fd753841e51b0f51679906159faf5c8fc2d4adfe60` | 0 |
| packages/pay/src/ui/w3m-pay-view/index.ts | 9671 | `47134dbf3a2cf5758aa5f75529c140197c3811c4dc5e738089e5a55d0be3c6d5` | 0 |
| packages/pay/src/ui/w3m-pay-view/styles.ts | 1397 | `985fd9eb4e7b9a4c45646a5d96103a92364a608d9016812741ce19c521299fd1` | 0 |
| packages/pay/src/utils/ApiUtil.ts | 5404 | `5c91b2b933e6338ab3daab41d4bf49631ce14516cf10fda0c8793cff99c64715` | 0 |
| packages/pay/src/utils/AssetUtil.ts | 4094 | `da33b415505cd19fd24dc04e8bfd5cac3340afb58c7402b94c3174cca64e86a0` | 0 |
| packages/pay/src/utils/ConstantsUtil.ts | 118 | `df5004bc6c1aa152a86b4f0acc937d6b7418e2efcec2bccaae1756eb6b590e6a` | 0 |
| packages/pay/src/utils/PaymentUtil.ts | 8283 | `0fb6a4d168df4ebb537601888276951a65a5ced1cd502374d33f561c8534fe0f` | 0 |
| packages/pay/vitest.config.ts | 120 | `27d27d7b59d34ecbbdcd94c545de62a0448e5b1385bafda59a561d6109aa8eba` | 0 |
| packages/polyfills/index.ts | 385 | `cda38431dc2af4a17233cee4d0dfa88217981a6b716c9d8d5c404435e2ad5fed` | 0 |
| packages/polyfills/package.json | 1073 | `da8e8b807ed9407014df97e0cf266ec2a2c1fd1812e664a961c8169cd916d6e5` | 0 |
| packages/scaffold-ui/exports/basic.ts | 183 | `d9d563146b04fce9bc9ca09fcee23f909d025c99cc27bf4c91fcf4aeba01d4d0` | 0 |
| packages/scaffold-ui/exports/core.ts | 96 | `cc15477468cc126885d99675890cb0980fc7d2962f469c7a47b333bb91c4bbef` | 0 |
| packages/scaffold-ui/exports/email.ts | 462 | `95f4e214ddb064a92b288e5f5a3f2af676efd89c00456b2f8b26a0cb72986216` | 0 |
| packages/scaffold-ui/exports/embedded-wallet.ts | 355 | `866f2a9ffb88829ffbd5d0981df69c4810eb58b5598c67f2b08bde825ae44b99` | 0 |
| packages/scaffold-ui/exports/index.ts | 2199 | `d9739596d8ce89875fa4264a75d69e36593c4925e5c988ca3771bb2f116f1a0d` | 0 |
| packages/scaffold-ui/exports/onramp.ts | 500 | `4edc56a01c091595dde2fc532469dc566b62d13f3546aaa68e24dc06eefd2fe7` | 0 |
| packages/scaffold-ui/exports/partials/w3m-list-wallet.ts | 60 | `cb525eb81064cdd06acdf68a3bfe10ba3b2abfa95f8c54cd47741dee1f75b14e` | 0 |
| packages/scaffold-ui/exports/partials/w3m-router-container.ts | 65 | `69122a74537404674a22739e7896e635d90b600ce1a7d39e66769a472c9f5681` | 0 |
| packages/scaffold-ui/exports/pay-with-exchange.ts | 151 | `1d013f38e5966ef775641974453abd79c4cd2a44ad8268eccba0978ac4f27ca5` | 0 |
| packages/scaffold-ui/exports/receive.ts | 62 | `29bf4259b8e3afb4335b06bb03d99565d0736454d1d7dd8bb75532b036f5cd08` | 0 |
| packages/scaffold-ui/exports/reown-authentication/data-capture.ts | 299 | `42ef42ae023782e6da7c0fc530f215e784ecbf5542d08a29c2e4bd6b2e929ee0` | 0 |
| packages/scaffold-ui/exports/reown-authentication/index.ts | 34 | `915d42a6ca8d97d9d3d006e0a9a9938de7de597d1510c112235cd036475f0b36` | 0 |
| packages/scaffold-ui/exports/send.ts | 260 | `cbea73c4ae492b43ec193ef1314169d57638d675f3361e79aec5cd4afae5de39` | 0 |
| packages/scaffold-ui/exports/socials.ts | 196 | `6ce57b35b1108299020104a4db69eb8ce975f649ea47208bd4984034a7e50741` | 0 |
| packages/scaffold-ui/exports/swaps.ts | 229 | `0a788c22766349612f3098c0d135300894f1198c37b8affaee9fde8d20a4242d` | 0 |
| packages/scaffold-ui/exports/transactions.ts | 60 | `c00f94eb78abd4987d72c533e89274d73d3c53f065ce7a87f255a69b59c37222` | 0 |
| packages/scaffold-ui/exports/utils.tsx | 46 | `dd696abc5fdcc14c5a0b5ee03c564a23efe9f9b717868e77d8934bf96f47040b` | 0 |
| packages/scaffold-ui/exports/w3m-modal.ts | 229 | `a6ce8067a2e016e3593f8c2344b9844e23040e395089461417516183b217427d` | 0 |
| packages/scaffold-ui/package.json | 4935 | `faa7e330538143a3fc09d43f23fbfa6484994cadecf9e47401de97e705c4c684` | 0 |
| packages/scaffold-ui/src/modal/w3m-account-button/index.ts | 6331 | `204740dd064dc2d17149a2c3391ed6e022e78eaee162e209e50adacbc626f1c1` | 0 |
| packages/scaffold-ui/src/modal/w3m-button/index.ts | 3197 | `e62818d92b4af681e8f1cfa227a25f17a241158c9602ffba387c911a237e9fdd` | 0 |
| packages/scaffold-ui/src/modal/w3m-button/styles.ts | 107 | `bed840cdb9548262f055ef8ff690f651462dfa6b61a47f645df43276987248c3` | 0 |
| packages/scaffold-ui/src/modal/w3m-connect-button/index.ts | 2543 | `4e40e08c5d406a5d22f66df9b0928477e6f0805d39cc586ab343fa2f2f6b0f95` | 0 |
| packages/scaffold-ui/src/modal/w3m-footer/index.ts | 3537 | `3a44a9ff3c6e56a9fda105b35e56ccaceab106eb9575d0a436fac9f28438af65` | 0 |
| packages/scaffold-ui/src/modal/w3m-footer/styles.ts | 1069 | `5b435566f57cd7c408e4fb363aa6b2b59dac7166447a96d8aadda3dd427de2aa` | 0 |
| packages/scaffold-ui/src/modal/w3m-modal/index.ts | 9465 | `0cf635087d84f1c9303d48869a30c6ee3c87eca03bd983dc049e54e78b42ea13` | 0 |
| packages/scaffold-ui/src/modal/w3m-modal/styles.ts | 6076 | `d7ee175ff7283428320b0507acc22ea52518b4328f4ee600b450547d3cd0f71d` | 0 |
| packages/scaffold-ui/src/modal/w3m-network-button/index.ts | 4036 | `f98086a84cf25e8579588095c1810c1e549b26163b6c2640841cf2dfd695ce28` | 0 |
| packages/scaffold-ui/src/modal/w3m-network-button/styles.ts | 107 | `bed840cdb9548262f055ef8ff690f651462dfa6b61a47f645df43276987248c3` | 0 |
| packages/scaffold-ui/src/modal/w3m-onramp-widget/index.ts | 4628 | `e580e98b0800f065e83cfc3fd33d1cca741716aa40df776a25da6b1e96e5c0be` | 0 |
| packages/scaffold-ui/src/modal/w3m-onramp-widget/styles.ts | 288 | `f8fd9f741f4a13a8fe69c5d670fd0b490ddb0488f3ad24d40078ea1efd6b2d7c` | 0 |
| packages/scaffold-ui/src/modal/w3m-router/index.ts | 8795 | `9148d69fcc3f6f9ee6e8cee4c634d47e829cc89dbf6a3347c4aba353d7d35c9b` | 0 |
| packages/scaffold-ui/src/modal/w3m-router/styles.ts | 116 | `af0a6f5e5be2b1ec7d9f6206163ce67a5f7812213550ffd96ced41d53c60fbbb` | 0 |
| packages/scaffold-ui/src/partials/w3m-account-activity-widget/index.ts | 600 | `8090dcbde652c8168166256fe8eb675b89bf1fde35293b0fbd96b87d5ceefcbb` | 0 |
| packages/scaffold-ui/src/partials/w3m-account-activity-widget/styles.ts | 205 | `caabc1029cda04568b7897f88656008c6b42d62c31156f0b359faac0c631d5ea` | 0 |
| packages/scaffold-ui/src/partials/w3m-account-auth-button/index.ts | 2881 | `4e193cee06b3ed9e9c031b3bdc214a893c18553afd25d09db1fe4eed9d95261a` | 0 |
| packages/scaffold-ui/src/partials/w3m-account-default-widget/index.ts | 12618 | `7528c7b04207101b71e0fc2807cba2f6f5876b35d143da0080a11b617aa33b49` | 0 |
| packages/scaffold-ui/src/partials/w3m-account-default-widget/styles.ts | 2953 | `ce8a8b411ed67fadb7a3ff6c4ea5b0946f3665b94c8c75fce606d69dfd42cb54` | 0 |
| packages/scaffold-ui/src/partials/w3m-account-tokens-widget/index.ts | 3644 | `e0adccd140087c8584f667ef12e2c4e65acdae3e211274333c5d0e9e6f17d6c3` | 0 |
| packages/scaffold-ui/src/partials/w3m-account-tokens-widget/styles.ts | 279 | `bb1e5ff085561dec4c6f431af69a9eec79efc40b500735174ab8d1d4d1313e17` | 0 |
| packages/scaffold-ui/src/partials/w3m-account-wallet-features-widget/index.ts | 11805 | `0209e23a25181ab6fc1569e1d911807afd0398875681fb4e51801461c7476328` | 0 |
| packages/scaffold-ui/src/partials/w3m-account-wallet-features-widget/styles.ts | 613 | `561d65b2a15c54728ce88f18fd664a1fbde591268607b81197e56d134f3365f0` | 0 |
| packages/scaffold-ui/src/partials/w3m-activity-list/index.ts | 10335 | `cfc794963cb345e48ec89118025cc995c309de8a503ff6da1edd9583652b6d07` | 0 |
| packages/scaffold-ui/src/partials/w3m-activity-list/styles.ts | 484 | `3833b7db2891976fbadc5bac74950da73946baf50c76d020aaa54f2df1a4fd40` | 0 |
| packages/scaffold-ui/src/partials/w3m-alertbar/index.ts | 2758 | `df758597e519c6db9cc47b47ab2aa3c03f1964f73da32c6fda930bfa3a2acb2c` | 0 |
| packages/scaffold-ui/src/partials/w3m-alertbar/styles.ts | 294 | `06432fb33077905dd0c7e9935457f84f825719854f32b6aec4c3f3cb2cda4570` | 0 |
| packages/scaffold-ui/src/partials/w3m-all-wallets-list/index.ts | 4917 | `22184fa46e7db0a9be47edf4fbd37e1fa1e8ba8536a4c467923b3989150c61f0` | 0 |
| packages/scaffold-ui/src/partials/w3m-all-wallets-list/styles.ts | 1102 | `1a1ec4925d0420af898b966a4cb4a35010115c6d7d31f111c930f0e7fa03f79b` | 0 |
| packages/scaffold-ui/src/partials/w3m-all-wallets-list-item/index.ts | 3961 | `e2065f8aed40e81f862213d9e2e7cb838ee3da60e7774d451b39a36a76b3c229` | 0 |
| packages/scaffold-ui/src/partials/w3m-all-wallets-list-item/styles.ts | 1920 | `d0c077db5d7b0ee9ebb2d4492c63b0addc0ea1dd3325ffd8447df7a860176466` | 0 |
| packages/scaffold-ui/src/partials/w3m-all-wallets-search/index.ts | 3558 | `856ccc9bdd6a239f61db224b182b188f81aa8d7ae9a26bd5894064fbdeb6c109` | 0 |
| packages/scaffold-ui/src/partials/w3m-all-wallets-search/styles.ts | 671 | `7a2e8cb9217ffd3ae09f598a214748e5f119d317f1eaacf2b8d4f5c11b635476` | 0 |
| packages/scaffold-ui/src/partials/w3m-all-wallets-widget/index.ts | 3485 | `5bba3deaa69102190a8a8fcfd1eef78bed8fe85990a17c87a3c9c0d82ae893a8` | 0 |
| packages/scaffold-ui/src/partials/w3m-connecting-header/index.ts | 2336 | `5e28428ea61a6929fc985eab546429f514cd3b727af239f5d7f6bc4d7bfd2b55` | 0 |
| packages/scaffold-ui/src/partials/w3m-connecting-wc-browser/index.ts | 2625 | `fb590387f6a60949c1d787b88aac87d37c40f94a60530430cc6091125bac6a67` | 0 |
| packages/scaffold-ui/src/partials/w3m-connecting-wc-desktop/index.ts | 1714 | `d8122523511d48b831f0c72d4c32b65d8a1a7b62c00b1632d8cd27ed034a31de` | 0 |
| packages/scaffold-ui/src/partials/w3m-connecting-wc-mobile/index.ts | 2628 | `b8285e883cfbf1522152a283e383d6c059d4953107f493633a496ebabe2ee850` | 0 |
| packages/scaffold-ui/src/partials/w3m-connecting-wc-qrcode/index.ts | 3475 | `7f69bef629527c98226581259c05fe25e2d94d23d30c53e8ec30b16f1942f16b` | 0 |
| packages/scaffold-ui/src/partials/w3m-connecting-wc-qrcode/styles.ts | 525 | `4da2e77df8cce08f1aeaf268bdca2f80f1131c6de271b5d751fca432a0522561` | 0 |
| packages/scaffold-ui/src/partials/w3m-connecting-wc-unsupported/index.ts | 1820 | `40772228c7c494b078ec1f7679088b73395ffb5d35593b65add65f381760ae31` | 0 |
| packages/scaffold-ui/src/partials/w3m-connecting-wc-web/index.ts | 2179 | `d1dd24e8fa48034f0539502c510a8d79013e573857dbe0837f5213b986489748` | 0 |
| packages/scaffold-ui/src/partials/w3m-connector-list/index.ts | 8920 | `0fdb682f549e5090ee874df5cd93bbe715dee220d9d85e7f751fbffd0b30330c` | 0 |
| packages/scaffold-ui/src/partials/w3m-connector-list/styles.ts | 383 | `5ff73094185827a639f495685a5cb861b54105b2468280ed1bb94d46f61b9f01` | 0 |
| packages/scaffold-ui/src/partials/w3m-email-login-widget/index.ts | 6606 | `0bc19b9aca5f9c32a68e994cdf780df610a41131eb63055e02f71fdfdb2d9f7d` | 0 |
| packages/scaffold-ui/src/partials/w3m-email-login-widget/styles.ts | 781 | `9bea98a7fecf348c1358d5afa611adfc3b5837b55ce7e39b53d714e5edd394c1` | 0 |
| packages/scaffold-ui/src/partials/w3m-email-suffixes-widget/index.ts | 1667 | `6aaddc9edfb9e2ff506897038139c2056e6a6a50d5260513a79589ccee319602` | 0 |
| packages/scaffold-ui/src/partials/w3m-email-suffixes-widget/styles.ts | 561 | `643871a609318db441de5ac01578fe1218130aa4cb0b6306331a6f772af3122a` | 0 |
| packages/scaffold-ui/src/partials/w3m-fund-input/index.ts | 1366 | `b6240aecc7aff8b8640604559ad91b1c40440953e5ada0d283f5b88cf348a589` | 0 |
| packages/scaffold-ui/src/partials/w3m-header/index.ts | 11463 | `e4692a927e3811ba51590462c8618701ac0393f0382a93eb7fcb0bffb1f1c4d5` | 0 |
| packages/scaffold-ui/src/partials/w3m-header/styles.ts | 1687 | `c2e578af4dd27cc19c6f90366fd3d0167f42520318634e4e05ef1729c09445cc` | 0 |
| packages/scaffold-ui/src/partials/w3m-help-widget/index.ts | 1575 | `035718baea76ab19ed61bd7273ae8d82a7e3529516f35a7d6c6a1046daabdbde` | 0 |
| packages/scaffold-ui/src/partials/w3m-input-address/index.ts | 6040 | `3783796a17f8b439bb7a8d7703e3747d45790269f0043a4a7da5aa05a855a232` | 0 |
| packages/scaffold-ui/src/partials/w3m-input-address/styles.ts | 1714 | `84f8fa9ab90389e2c643dee6436506a65e5b6dd3e613e846a700ded2d7ef86d9` | 0 |
| packages/scaffold-ui/src/partials/w3m-input-token/index.ts | 4888 | `5fb147da8c05542e13f8cd2747d6021d5b064078cda4856d21f7e3d43400d0e9` | 0 |
| packages/scaffold-ui/src/partials/w3m-input-token/styles.ts | 1075 | `0e64b6589a4db0f5d92bca7eb9c0d77e8de7a60368cf5dfb1c750700265c8f27` | 0 |
| packages/scaffold-ui/src/partials/w3m-legal-checkbox/index.ts | 2772 | `289b6c58c9202cb435c4a41a42be6808f34eb1be2ba8587f9986118810e8c8c2` | 0 |
| packages/scaffold-ui/src/partials/w3m-legal-checkbox/styles.ts | 334 | `e4ca38929a922af37aa80cf70907c1e2cc0268601a02474577a211ec6ccab2fe` | 0 |
| packages/scaffold-ui/src/partials/w3m-legal-footer/index.ts | 3119 | `515b2548ab914f7dafa0db3ca1c4e532d8e651d514486e5240f8acf39e35823a` | 0 |
| packages/scaffold-ui/src/partials/w3m-legal-footer/styles.ts | 329 | `6953f146aa10588fa25defbee3aa1a65295683eb7234dec478f5d121a0bc2536` | 0 |
| packages/scaffold-ui/src/partials/w3m-list-wallet/index.ts | 4619 | `d16546c78e8aeb96fcb7af5a0c61e442bde38711dc63dc9224ec3d4ef9bc610c` | 0 |
| packages/scaffold-ui/src/partials/w3m-list-wallet/styles.ts | 93 | `97085089bd2c380b6e3bb330cee104f458ef482961c3d909818537bf44fb619b` | 0 |
| packages/scaffold-ui/src/partials/w3m-mobile-download-links/index.ts | 2718 | `6e8c053e80b320ef684d3653349bbcda41df1210633e0520b59ac20f03006f63` | 0 |
| packages/scaffold-ui/src/partials/w3m-mobile-download-links/styles.ts | 178 | `80e3debe1f71a54728a7f90db4e0a37c3d23921928f135fd2af0889fc210a95f` | 0 |
| packages/scaffold-ui/src/partials/w3m-onramp-activity-item/index.ts | 3130 | `c4db418978b1dbe0e62173ccd1e471d1a71210bc24726b2cfe91292383cb92db` | 0 |
| packages/scaffold-ui/src/partials/w3m-onramp-activity-item/styles.ts | 1317 | `e4be1b215343d4c5b1822a45d4f7b2140a7d6e8032693be525a74c56fbcb4ead` | 0 |
| packages/scaffold-ui/src/partials/w3m-onramp-input/index.ts | 3771 | `696a13e7fe7bc431a1ac56c69fdceded9a6420c1ad85040c90b85b21343468d2` | 0 |
| packages/scaffold-ui/src/partials/w3m-onramp-input/styles.ts | 874 | `52080c2c09aaadd94df467a26a36c1b9219d6a5d9b3cbe479110286ba45ce6af` | 0 |
| packages/scaffold-ui/src/partials/w3m-onramp-provider-item/index.ts | 3016 | `5c769b24c6c06b0a35273d3a01c5eab0fc0e4d6df4bdaf67712221bd79c5dbaa` | 0 |
| packages/scaffold-ui/src/partials/w3m-onramp-provider-item/styles.ts | 1715 | `d98f9c8260e1dd0f96a0911aef18697675d278704b4d624abf0dd09b5f296a74` | 0 |
| packages/scaffold-ui/src/partials/w3m-onramp-providers-footer/index.ts | 2141 | `499ca99bcc9950b0bea14170e2fcd781e887e603494479f431726bb11f81704a` | 0 |
| packages/scaffold-ui/src/partials/w3m-onramp-providers-footer/styles.ts | 48 | `4adadffdb8232762efda435d0ee263249d7c531fa3b92679201fe80828ba5909` | 0 |
| packages/scaffold-ui/src/partials/w3m-pay-header/index.ts | 2135 | `c0bb859b6262e4b6d96c21b834322957cb71ae5a0638b5fd724ee2f25aa7aedc` | 0 |
| packages/scaffold-ui/src/partials/w3m-pay-header/styles.ts | 379 | `26539014b6ca5d9c1531133e6884abfe2477c9be4d8b4e45f76329f4ac755a44` | 0 |
| packages/scaffold-ui/src/partials/w3m-recent-emails-widget/index.ts | 1357 | `a9eaa303e217eba346959ff8c74d4bc7d02f21eaf3bd129cd692d51171bcba19` | 0 |
| packages/scaffold-ui/src/partials/w3m-recent-emails-widget/styles.ts | 429 | `65a90c90cb1724a1603d28db8c8a5431f915fc0faea0b731d73964214a99d515` | 0 |
| packages/scaffold-ui/src/partials/w3m-router-container/index.ts | 6767 | `12eafaf6163e7ce26b2fc385da827fd78e184e5ef63bf01f35247a2c0c7f862f` | 0 |
| packages/scaffold-ui/src/partials/w3m-router-container/styles.ts | 2922 | `734b20bbbcd66be4af9e54ba134230a342596d97dbab7cf8ec439d328e399b35` | 0 |
| packages/scaffold-ui/src/partials/w3m-siwx-sign-message-thumbnails/index.ts | 1798 | `ecf3ad915692dc32072cc2e9ad32ca02d1cf786a6e54e2884e199c180e85611d` | 0 |
| packages/scaffold-ui/src/partials/w3m-siwx-sign-message-thumbnails/styles.ts | 226 | `67f504efb5dae35bce038de5e61bd1ce89e54378104304b4a6c1210186559fe8` | 0 |
| packages/scaffold-ui/src/partials/w3m-snackbar/index.ts | 2301 | `520e43a9f11032df58ae958b5c4f773c10cf77ceca03e232ba3b3c4bfd8ee846` | 0 |
| packages/scaffold-ui/src/partials/w3m-snackbar/styles.ts | 203 | `649edf4338a3ebd7a25ac06c0782dbf15841b0b8e263646c198fe30cc20e2aac` | 0 |
| packages/scaffold-ui/src/partials/w3m-social-login-list/index.ts | 3832 | `086b64fd318a1dc891c213609211777b8935cfbbd2a2667bcb56375b4b7cd5f8` | 0 |
| packages/scaffold-ui/src/partials/w3m-social-login-list/styles.ts | 383 | `5ff73094185827a639f495685a5cb861b54105b2468280ed1bb94d46f61b9f01` | 0 |
| packages/scaffold-ui/src/partials/w3m-social-login-widget/index.ts | 7961 | `39783862c81ea95d0d8a525b1044b25f580fdfb53df99e624b814cc9f7046bf4` | 0 |
| packages/scaffold-ui/src/partials/w3m-social-login-widget/styles.ts | 319 | `6093fe2c4c900f7ccac5080915aed3ef47ba0b2b5905748f640decafa04c7d22` | 0 |
| packages/scaffold-ui/src/partials/w3m-swap-details/index.ts | 8421 | `7130e90ddff3967c65d2b9d3195cbb0f071079a48a7304df06edd48c25aad137` | 0 |
| packages/scaffold-ui/src/partials/w3m-swap-details/styles.ts | 1270 | `6d186bf9d6d5d2e36f4ecf293ab8455bba7a58ae065ab6bebcfddfde600cb2dc` | 0 |
| packages/scaffold-ui/src/partials/w3m-swap-input/index.ts | 6129 | `15039bdf17045a72ae63b2a2c6c51ea76d26dc59394c86287eeb3e2c2ba547ef` | 0 |
| packages/scaffold-ui/src/partials/w3m-swap-input/styles.ts | 2293 | `4bbdce291472e2bd23f3a0edcc7a7d09052922cc34603ba8dd81ac718161a705` | 0 |
| packages/scaffold-ui/src/partials/w3m-swap-input-skeleton/index.ts | 1629 | `855cc511b0bf07cc03744f02dbd2db993ff0219c9a2f41ca976f5c79d548dcb1` | 0 |
| packages/scaffold-ui/src/partials/w3m-swap-input-skeleton/styles.ts | 1211 | `b5fa22298290430566f1f9b96244cc240ad48a80e47f4f1a4d58e0eae8f39f54` | 0 |
| packages/scaffold-ui/src/partials/w3m-tooltip/index.ts | 2173 | `4e72414659695b7ac85bd2eac03f25aefc4e4961031984b735bb8e287204507e` | 0 |
| packages/scaffold-ui/src/partials/w3m-tooltip/styles.ts | 2218 | `16638b23f57483dd801e08a20088cea7234cc3247a160b73d7acaf52da4bcc4d` | 0 |
| packages/scaffold-ui/src/partials/w3m-tooltip-trigger/index.ts | 2638 | `669ae0d67e7002c156ecca6aa3908e8b602b712354b044de73b7c0797f42e40e` | 0 |
| packages/scaffold-ui/src/partials/w3m-tooltip-trigger/styles.ts | 100 | `38d8138daef378947e8662675908f1ab0180ff03be86273924de8793c745a33e` | 0 |
| packages/scaffold-ui/src/partials/w3m-wallet-login-list/index.ts | 987 | `5f4c480d33d1b14c13d2a9b24e761d02449382612233da1451ed43df735c5a6f` | 0 |
| packages/scaffold-ui/src/partials/w3m-wallet-send-details/index.ts | 2111 | `dedd79ec28e92db84127a78aaa55002cfe7589567900418f43bb422d7cacb68e` | 0 |
| packages/scaffold-ui/src/partials/w3m-wallet-send-details/styles.ts | 1479 | `b052e22898d34496bfd6c3ad08fe8848ce00fc4d568dc8e7c2d4d259939983c1` | 0 |
| packages/scaffold-ui/src/utils/ConnectionUtil.ts | 1180 | `1bd3c0842b461ca15f8c2c1de1a06b0c1db92e843b89a1558c250e8baca30251` | 0 |
| packages/scaffold-ui/src/utils/ConstantsUtil.ts | 717 | `cf0ba6a3fa421513b4b3064559105f99d5559604c355c227afdd69507d497183` | 0 |
| packages/scaffold-ui/src/utils/HelpersUtil.ts | 1504 | `81ca60e665bdec8ed5808389fda61b89c357073cfee954a704d7082efa1c62fb` | 0 |
| packages/scaffold-ui/src/utils/w3m-connecting-widget/index.ts | 7439 | `37633f5408e9006b566b6e6e550de17e45bcd80a78174fbf766775c8075600f5` | 0 |
| packages/scaffold-ui/src/utils/w3m-connecting-widget/styles.ts | 1470 | `55112b6a1b1b3ecbfc510082357f4ac68191cc0264194ac3daf8528e604d8302` | 0 |
| packages/scaffold-ui/src/utils/w3m-email-otp-widget/index.ts | 5856 | `3795ae4eff85eea70bf563349b4a7745a384ec8fbbe36cb889472927b9ae7828` | 0 |
| packages/scaffold-ui/src/utils/w3m-email-otp-widget/styles.ts | 171 | `c60b055408caa3ccc3673a568ea0b012f78a04f2b9e12ad67787dae59663a3d3` | 0 |
| packages/scaffold-ui/src/views/w3m-account-settings-view/index.ts | 9398 | `20a4a17c61bb6527ce7bd695e740cd530485a1923ee49c4eb34a1a941962b2ff` | 0 |
| packages/scaffold-ui/src/views/w3m-account-view/index.ts | 1787 | `d8956f10a1f2e059cb96f0898aba861419d1860ad6bf63d1fe22c792eb8d8cf3` | 0 |
| packages/scaffold-ui/src/views/w3m-all-wallets-view/index.ts | 2821 | `5033758bb437950960382c9934470d435b2cb52d7bf93a123f4e0efa94034906` | 0 |
| packages/scaffold-ui/src/views/w3m-approve-transaction-view/index.ts | 4783 | `e2e016dc2b8d2a0f0cd8a2f20f0d72d944cd7cc18754769af36ceeabd215df1e` | 0 |
| packages/scaffold-ui/src/views/w3m-approve-transaction-view/styles.ts | 240 | `7523b807ce2ecf4b6e1bbfe771c8e7d5e533eed5dfbf2edc06131c05eba3cc24` | 0 |
| packages/scaffold-ui/src/views/w3m-buy-in-progress-view/index.ts | 5271 | `1603798524219e3de12357f42d6b6f3683018b38502fc660b8482511f1f1ef02` | 0 |
| packages/scaffold-ui/src/views/w3m-buy-in-progress-view/styles.ts | 1672 | `8fa92eb81604c836b03eac0aaec784da3f96aede3bbdf71c00d8151c099c1549` | 0 |
| packages/scaffold-ui/src/views/w3m-choose-account-name-view/index.ts | 3250 | `1c15f5dc9bf121aa6a926f2125b1f599dcc943bf310743c1fc92ef2a74677363` | 0 |
| packages/scaffold-ui/src/views/w3m-choose-account-name-view/styles.ts | 101 | `fdf80c8e58cf8f236dc045278409779412eb8099b33edca58dbf6ba284c49065` | 0 |
| packages/scaffold-ui/src/views/w3m-connect-socials-view/index.ts | 2103 | `dcd07633391baa295d5fbeb7b2a2907e2ce2d1e7d132303e0f28125dde117bc1` | 0 |
| packages/scaffold-ui/src/views/w3m-connect-socials-view/styles.ts | 464 | `1f9727c706674c89092d02a86c55edc850ce0c881c7997ba7d84327a3d4ea2c0` | 0 |
| packages/scaffold-ui/src/views/w3m-connect-view/index.ts | 13392 | `e701a3bd4617e2011d502b623438af4eb9bc654534dbcb98f633f9924c387ec1` | 0 |
| packages/scaffold-ui/src/views/w3m-connect-view/styles.ts | 1057 | `e50601731493b6ba46e4d647b8b407e6cf8cc62a0ef786e299557c41688a47c6` | 0 |
| packages/scaffold-ui/src/views/w3m-connect-wallets-view/index.ts | 2119 | `e55c103f539e2766af12ef03a13430ac2375ff9c861813d43a76a94968fec42e` | 0 |
| packages/scaffold-ui/src/views/w3m-connect-wallets-view/styles.ts | 462 | `0aae7acdfc099c66687921ddb9fa3c1fa064d0d4a7015c081d51d529a3e490d7` | 0 |
| packages/scaffold-ui/src/views/w3m-connecting-external-view/index.ts | 6847 | `53d477d162adab6a54597d70927b0e63d5dc8e914949c9de8b9de2bb7027578b` | 0 |
| packages/scaffold-ui/src/views/w3m-connecting-farcaster-view/index.ts | 9429 | `81747aa6eeec6fbbda163b9af12cf0166260c0c91fd61b91befab0575cd398fd` | 0 |
| packages/scaffold-ui/src/views/w3m-connecting-farcaster-view/styles.ts | 1234 | `8283c2b0d41e60f07fcac49b05b873e22c0c9c124eddae61f1db68790b199341` | 0 |
| packages/scaffold-ui/src/views/w3m-connecting-multi-chain-view/index.ts | 4016 | `67be34301ea3bd0231bfd2b79200eff9ec90a904e6cb1c2f06d293a893997994` | 0 |
| packages/scaffold-ui/src/views/w3m-connecting-multi-chain-view/styles.ts | 102 | `00e32ea0e4f6e902fce128b71747d01a87e07356b7b2c8696c99144e50492270` | 0 |
| packages/scaffold-ui/src/views/w3m-connecting-social-view/index.ts | 9126 | `425223402ba697201712fa244f65b9f38b5d16ec8cc1527c2746d0d6e0998213` | 0 |
| packages/scaffold-ui/src/views/w3m-connecting-social-view/styles.ts | 1254 | `5c6bbc806047fc93ab3d6c1e662f638c5fff297210e9f1d06a74bab3f1ebbe25` | 0 |
| packages/scaffold-ui/src/views/w3m-connecting-wc-basic-view/index.ts | 2592 | `51ea2539d9e744693fefd5d3bf4fb9e9abba95aad0a23d1715ded19f624658d6` | 0 |
| packages/scaffold-ui/src/views/w3m-connecting-wc-view/index.ts | 9743 | `c1a44d97789fdfd168565dc3772c0a478ffef6112f0f2d2ed51df587dec4a8b1` | 0 |
| packages/scaffold-ui/src/views/w3m-connecting-wc-view/styles.ts | 260 | `1f8b95265de33981d3f895d2d305d356651bdc1376d613aae24e21b795415af0` | 0 |
| packages/scaffold-ui/src/views/w3m-data-capture-otp-confirm-view/index.ts | 1542 | `adc9901bd9e1e94acac1c1459a073b8c78ee5223b69f39544ea49dd9b36322f7` | 0 |
| packages/scaffold-ui/src/views/w3m-data-capture-view/index.ts | 8349 | `cc4dc7a73c88f48d5aa97f0676c629dcd772ae854d8c42a3ed3ebe625768b193` | 0 |
| packages/scaffold-ui/src/views/w3m-data-capture-view/styles.ts | 1937 | `0145a90758e2bdeb2ceb2281e884adc78578c26d0152617646604f0cc128e89c` | 0 |
| packages/scaffold-ui/src/views/w3m-deposit-from-exchange-select-asset-view/index.ts | 4680 | `bb73713b1c75763f38c7fcf1d41088a56770c54be2747ee7e1874b0de887655b` | 0 |
| packages/scaffold-ui/src/views/w3m-deposit-from-exchange-select-asset-view/styles.ts | 341 | `945221fe42525676151a744d16860326b85b1534d24f872cb5ad95694cd0db3b` | 0 |
| packages/scaffold-ui/src/views/w3m-deposit-from-exchange-view/index.ts | 9329 | `3e72050c1852cd44d8998166ad4b359e5d3b392eb505aaef85f41b1c4fe00faa` | 0 |
| packages/scaffold-ui/src/views/w3m-deposit-from-exchange-view/styles.ts | 383 | `cabad02f234794c5464d02e23f7f0c9617c49a160c33283649d6e6661d0bb265` | 0 |
| packages/scaffold-ui/src/views/w3m-downloads-view/index.ts | 3625 | `54d8588e86de079c5894817c07493e5d4a2b1e9207c94865eec2f05d6636e8f1` | 0 |
| packages/scaffold-ui/src/views/w3m-email-login-view/index.ts | 2150 | `09098abbc1a6ec00d5e5b73c31806b49fcd091337cca937d32c9995f65932350` | 0 |
| packages/scaffold-ui/src/views/w3m-email-verify-device-view/index.ts | 3741 | `03766df3a1f45324c8a9e2f1800f6620b38c1aae5481426bbb6006b791628327` | 0 |
| packages/scaffold-ui/src/views/w3m-email-verify-device-view/styles.ts | 176 | `6e73d6340e2b86280babe688c67bbb898a5ebedf06dbb0272709a83ab6fd2ad2` | 0 |
| packages/scaffold-ui/src/views/w3m-email-verify-otp-view/index.ts | 2550 | `e853140cd158340cfbd9f0aa36e1d1b4951362b06c15479be3f259ebc747323e` | 0 |
| packages/scaffold-ui/src/views/w3m-fund-wallet-view/index.ts | 4954 | `c6ab9ce2a51f258f5af06752ec95d9dd1443c2b15f8d0441161d7a2ed7449edd` | 0 |
| packages/scaffold-ui/src/views/w3m-get-wallet-view/index.ts | 2271 | `21def426815e3492d8c298e8a7ed882e6468c28a570bbb3f0fd342d1bca7e00c` | 0 |
| packages/scaffold-ui/src/views/w3m-network-switch-view/index.ts | 5988 | `80c3ae1a858903922bf85962cf907d52b5b6b975503354f05721fee7dfcf352b` | 0 |
| packages/scaffold-ui/src/views/w3m-network-switch-view/styles.ts | 1232 | `c7bda55b69380dea4379b4df73920106fedc5d97625325311d9e5f27b1486ead` | 0 |
| packages/scaffold-ui/src/views/w3m-networks-view/index.ts | 3879 | `ff4c4817826fd7ef6680a9433be9ee58b26e945bb5a1750df500fb81a8e33c75` | 0 |
| packages/scaffold-ui/src/views/w3m-networks-view/styles.ts | 169 | `d8a0fbcd59d5653ea7a6d06961d44bac83bea44fbf8cc6ec6779bb7f64818b3b` | 0 |
| packages/scaffold-ui/src/views/w3m-onramp-fiat-select-view/index.ts | 3371 | `5af7b903a41f2eb7454c5ca6cf5caea9ce14d3465754e07ba684226b3cf6aadb` | 0 |
| packages/scaffold-ui/src/views/w3m-onramp-fiat-select-view/styles.ts | 441 | `5241d7c7e59ec75c5f387919324b593f397bb6374b87ee17fe7e4d496730395c` | 0 |
| packages/scaffold-ui/src/views/w3m-onramp-providers-view/index.ts | 2680 | `e17d3e0ba980709a456cb05a04af2e605ceadd2ca50ba38214bb752187c40b51` | 0 |
| packages/scaffold-ui/src/views/w3m-onramp-tokens-select-view/index.ts | 3496 | `fa8fe6537ba0b922c2da060790644f67a1d6c893faf33ab2856c13c0aefa960e` | 0 |
| packages/scaffold-ui/src/views/w3m-onramp-tokens-select-view/styles.ts | 441 | `5241d7c7e59ec75c5f387919324b593f397bb6374b87ee17fe7e4d496730395c` | 0 |
| packages/scaffold-ui/src/views/w3m-profile-wallets-view/index.ts | 26689 | `3db85086379f54c1cedd445b6c19075cf119b6c4b2947cf57f568de56aa009e2` | 0 |
| packages/scaffold-ui/src/views/w3m-profile-wallets-view/styles.ts | 1787 | `93b2c5320636ec7a52fdbe9c3c2fcdccafe70a74755063f5803251760509e905` | 0 |
| packages/scaffold-ui/src/views/w3m-register-account-name-success-view/index.ts | 2591 | `07d01f21a0131aa0db8b327e6291e3580c3379ef7459a5c6ad3a9857f847648d` | 0 |
| packages/scaffold-ui/src/views/w3m-register-account-name-success-view/styles.ts | 101 | `fdf80c8e58cf8f236dc045278409779412eb8099b33edca58dbf6ba284c49065` | 0 |
| packages/scaffold-ui/src/views/w3m-register-account-name-view/index.ts | 7533 | `1add18537999c9bd8facb87fd6ec13ff24059d09aa2f450c2dafe9403df1f5a8` | 0 |
| packages/scaffold-ui/src/views/w3m-register-account-name-view/styles.ts | 1203 | `245b416e165aa85c3b0c15eb7f367bc1b0cdd8bf668a52303382d378e0375f78` | 0 |
| packages/scaffold-ui/src/views/w3m-send-confirmed-view/index.ts | 1638 | `7cd732480d74534c4d56a699d0304fb37c4d3eaa59cc9bc97b8e71f95f5afb81` | 0 |
| packages/scaffold-ui/src/views/w3m-send-confirmed-view/styles.ts | 328 | `198ccdad8f90fc83627d92fdeb413440b79a0c802064a807096da4414f3312c9` | 0 |
| packages/scaffold-ui/src/views/w3m-siwx-sign-message-view/index.ts | 3249 | `068fa08a69695b5393609e8824b16174bad19fdd4e7e88c9cbf2c6b04e9e1fb9` | 0 |
| packages/scaffold-ui/src/views/w3m-smart-account-settings-view/index.ts | 4025 | `93786de9bed3b381254d16ce42f3b7f499c2c947e87a6c15cc311aff1c09da52` | 0 |
| packages/scaffold-ui/src/views/w3m-swap-preview-view/index.ts | 8832 | `a2cb61aa21c60a85e3a8f174a922c20de51a20bedeb001eb792b7e30ad74a27f` | 0 |
| packages/scaffold-ui/src/views/w3m-swap-preview-view/styles.ts | 3491 | `9ff9de1af895557698d442f7e077d7b073682fb0fdbb24e68efd5adf9fc53945` | 0 |
| packages/scaffold-ui/src/views/w3m-swap-select-token-view/index.ts | 10092 | `768a1f078674b6fca00b7c12b1118aa573815643772b7aeb4fc50c6d9205893d` | 1 |
| packages/scaffold-ui/src/views/w3m-swap-select-token-view/styles.ts | 2812 | `0822b2ea9f5917b0af6a49c4526beeb4fb389b0525c564fcd8bd5147e9995dfd` | 0 |
| packages/scaffold-ui/src/views/w3m-swap-view/index.ts | 16202 | `10ea83b4105247253a15eefc42010e90c274af81f937459c53f5a9fd3fd3af03` | 0 |
| packages/scaffold-ui/src/views/w3m-swap-view/styles.ts | 2497 | `89944e5d727d1528573d773d4dc2476f7b40120187d486ceb3a9385e5e3c5e38` | 0 |
| packages/scaffold-ui/src/views/w3m-switch-active-chain-view/index.ts | 3742 | `3e165ebdf4fd96a2d0eebf663162b0cb60b7dcab0370e2ec61b45ed1f478cb9e` | 0 |
| packages/scaffold-ui/src/views/w3m-switch-active-chain-view/styles.ts | 2065 | `65ebef4df2c43e456a303f5a002a86e2533cf6514d596e490e6659ecf28aea2f` | 0 |
| packages/scaffold-ui/src/views/w3m-transactions-view/index.ts | 739 | `f48768d4b4f9d70d86d618259b59e60ce468325751b35f30979b838b6d862431` | 0 |
| packages/scaffold-ui/src/views/w3m-transactions-view/styles.ts | 254 | `1466fad93114922169054f676335fa73c0455ed6a77532c36a3fe78df390d9bf` | 0 |
| packages/scaffold-ui/src/views/w3m-unsupported-chain-view/index.ts | 6347 | `445d91cb5012f4f610a467901aac5b9bf31e3de6d8d8b8141282f93958f8f751` | 0 |
| packages/scaffold-ui/src/views/w3m-unsupported-chain-view/styles.ts | 230 | `b0eea0426b46c0e55b393823c7a8b96aadac8df50e2c87ea7715e9aeb7b6d21a` | 0 |
| packages/scaffold-ui/src/views/w3m-update-email-primary-otp-view/index.ts | 1424 | `e1b1f08f405ffba2d5d06ff822a852b014f6192095d0563191fbaa7801119bfa` | 0 |
| packages/scaffold-ui/src/views/w3m-update-email-secondary-otp-view/index.ts | 1512 | `c4070a02fbf6edb353aae483a7a08fd8a356f6f7e747e5ed2528390777800328` | 0 |
| packages/scaffold-ui/src/views/w3m-update-email-wallet-view/index.ts | 4076 | `c52cfe21bda0f8a6399cb7da0a9718bcf8f0d4ff7eb7a12584bcbb9fd798987e` | 0 |
| packages/scaffold-ui/src/views/w3m-update-email-wallet-view/styles.ts | 165 | `0db41de94077130b544f2c06a8b42dc9517aff2c7aa0c72984be62aac7d550d1` | 0 |
| packages/scaffold-ui/src/views/w3m-upgrade-wallet-view/index.ts | 1254 | `ccae331ce64cb7fde339ae7d8a6aedef66cf596fafffe3cbadbf2a9413db384d` | 0 |
| packages/scaffold-ui/src/views/w3m-usage-exceeded-view/index.ts | 1818 | `1fc8aa1c3dfaea398cb3de113cbb3c386b83655665bf90102b4d4c21f5559275` | 0 |
| packages/scaffold-ui/src/views/w3m-usage-exceeded-view/styles.ts | 242 | `04063525bd43c43165c25eb9250c1eefb9cfc7a5efe1f75a50aa3a016c09e0d2` | 0 |
| packages/scaffold-ui/src/views/w3m-wallet-compatible-networks-view/index.ts | 2684 | `4ff1940a139ecec9c857bcaf1a41f31686c155dabc247f652ce22aac93d45e41` | 0 |
| packages/scaffold-ui/src/views/w3m-wallet-compatible-networks-view/styles.ts | 230 | `b0eea0426b46c0e55b393823c7a8b96aadac8df50e2c87ea7715e9aeb7b6d21a` | 0 |
| packages/scaffold-ui/src/views/w3m-wallet-receive-view/index.ts | 5561 | `6228ba9ad31c1be72e5b713a173227000c93826d645848504254d4b0fe7f9768` | 0 |
| packages/scaffold-ui/src/views/w3m-wallet-receive-view/styles.ts | 283 | `47e464b29ae30ac4e2e65f8aceabf2954a6804a62f169e8acf79b1c91ce629fb` | 0 |
| packages/scaffold-ui/src/views/w3m-wallet-send-preview-view/index.ts | 6992 | `7dfbdfaea9feac4103564eb01b1d60232fc15735615c70a2ef91798b708262e9` | 0 |
| packages/scaffold-ui/src/views/w3m-wallet-send-preview-view/styles.ts | 524 | `3d29c3232c6434b8f5dc10ef8de77c59ba762d48953336b9ea0221ac3d4da5f3` | 0 |
| packages/scaffold-ui/src/views/w3m-wallet-send-select-token-view/index.ts | 5619 | `295535a52b9080a88d9fc3a5abbc6ccf96319137847190f6d929a58e83f9462b` | 0 |
| packages/scaffold-ui/src/views/w3m-wallet-send-select-token-view/styles.ts | 341 | `945221fe42525676151a744d16860326b85b1534d24f872cb5ad95694cd0db3b` | 0 |
| packages/scaffold-ui/src/views/w3m-wallet-send-view/index.ts | 9499 | `ac7987c3c0f4d812ac33de08009042ffb0b748171b6992578798cc8d7fc143d5` | 0 |
| packages/scaffold-ui/src/views/w3m-wallet-send-view/styles.ts | 669 | `2634abfa18053803809a0b7c761167618268d444161ea453d93e4ce4df8d7cac` | 0 |
| packages/scaffold-ui/src/views/w3m-what-is-a-buy-view/index.ts | 1529 | `8ffe0430aedf88017637e24e3bf1a30a410c4a3226e9f340e034047ede47ac23` | 0 |
| packages/scaffold-ui/src/views/w3m-what-is-a-network-view/index.ts | 1695 | `0d7ce0e138a3fe8186b198ecf1a88692845d6c28d2d3f9ba6fa943250806cf74` | 0 |
| packages/scaffold-ui/src/views/w3m-what-is-a-wallet-view/index.ts | 1904 | `0be1000c425875f4a1e1757d85c463185a3fbaf79eba084af5789dabf9ef3a1a` | 0 |
| packages/scaffold-ui/vitest.config.ts | 157 | `3aa116fb8ed482e92643629c786d42ad2565e756f3f3213fb0f7a5396761de56` | 0 |
| packages/siwe/core/controller/SIWEController.ts | 3510 | `df57fc4ff3082a292cc85ec6e372fcca5cf71ebed3641f38ed9f306225bc6e79` | 0 |
| packages/siwe/core/helpers/index.ts | 1161 | `e02eec6db9cd423d620713e11854d3b2cdd138869d055324404f3e4db7803da6` | 0 |
| packages/siwe/core/utils/ConstantsUtil.ts | 63 | `7f886d456fd620250d60b8641aeff6b24ecfad9c566fa2dc4111b3c0e27bbe8b` | 0 |
| packages/siwe/core/utils/TypeUtils.ts | 1601 | `6dae179ee12c8590c90dcb396dc9d1b447e3a189de06dac95c974d93af719516` | 0 |
| packages/siwe/exports/index.ts | 757 | `6eeb2a406117b2dec0608b2ac456073d8eb456cd694bacca8d926d8730b678ce` | 0 |
| packages/siwe/package.json | 1512 | `10f5cfd45bf5705acbf3c43cb9452d5efb64cc6f140cadaed17fbfbd365fba1c` | 0 |
| packages/siwe/scaffold/partials/w3m-connecting-siwe/index.ts | 1703 | `0f521e9e20cf470f4fe51b93908c09c5133851eaf05eb471e3f8b6ba4cc0e63d` | 0 |
| packages/siwe/scaffold/partials/w3m-connecting-siwe/styles.ts | 202 | `8236c118b65f1585facfc329c95da8f01367d305ff77e5fda0322c98ed9cb0a7` | 0 |
| packages/siwe/scaffold/views/w3m-connecting-siwe-view/index.ts | 5049 | `b734151cc18b4ce966d0dc459a94c43c2b008762315031e50418bea2e5f1812f` | 0 |
| packages/siwe/src/client.ts | 2643 | `bb3c31ed1c0fa5fc4224c902d56b21eebf181ee88dd1d8c61cccede8fa402478` | 0 |
| packages/siwe/src/mapToSIWX.ts | 6391 | `b6c56bc6579bfffa7000a4dc0188e3ecbdf071720431e81024b9c8a5110cdd8b` | 0 |
| packages/siwe/vitest.config.ts | 80 | `edaa4113ae35e9507b5f1538604b5cc4120506d5631421e5068eeaadeec319d7` | 0 |
| packages/siwx/exports/index.ts | 32 | `2b70c60d55197cc950a2858966ec5c6bc6f597cf9d3253527b536267ea63a341` | 0 |
| packages/siwx/exports/react.ts | 445 | `b4c7aafdef07f57892a2a8ce271ebdafcba1334bbeb332006dd452a817b358e4` | 0 |
| packages/siwx/exports/vue.ts | 527 | `abde0c0061969c479f65e704988080b6665f2419468c499de27585ca45afcca0` | 0 |
| packages/siwx/package.json | 2111 | `a9d31b6b749551dc47b98544994143aadf0e70797de8ba3aba59397c710ef38c` | 0 |
| packages/siwx/src/configs/DefaultSIWX.ts | 1997 | `34e666a079f45d900cee89ddcc736df98bc022418c93c70e6b60ce425508ea27` | 0 |
| packages/siwx/src/configs/ReownAuthenticationSIWX.ts | 143 | `4807916f1187fc04310fc4050a0b76348c099ea6848a15a6a055dbe94f428f1a` | 0 |
| packages/siwx/src/configs/index.ts | 78 | `a36fcfbd864c8ec5bcf2a602d5b1bc0d79c1b55b3c8fd1602ce6a38dd465ae40` | 0 |
| packages/siwx/src/core/SIWXConfig.ts | 5272 | `5f5a84a0f887ca73e8cb165e9d2b41a9bdf3a6914a7682f1c6bdd8685f16a20e` | 0 |
| packages/siwx/src/core/SIWXMessenger.ts | 4787 | `acded11000f129dd5d00a79f77fdf78918f13c829de9649b3d020f479c09cc2c` | 0 |
| packages/siwx/src/core/SIWXSigner.ts | 119 | `154140d4d95dd29cf31d59be69f8741d1be8c30f46b594dfd9d71944db656f2a` | 0 |
| packages/siwx/src/core/SIWXStorage.ts | 1234 | `c0c2fff616085392d883572e7d8c8d670ac1323393a8a1a40c1c62c86d9b234b` | 0 |
| packages/siwx/src/core/SIWXVerifier.ts | 1012 | `9c0f45815879c5aec099952b890d59f7e140df46723c86eb8c6a7dffc83a9f6f` | 0 |
| packages/siwx/src/core/index.ts | 134 | `3c18e0b3ce04eb4fa619f836bc15761721dc2709c9f5ea990794c73ee196f15b` | 0 |
| packages/siwx/src/index.ts | 265 | `5c57d2fcf539f8f1fa701bb8b23c91f1b8df1dc04e16ae3e2be0c48c81cea223` | 0 |
| packages/siwx/src/messengers/DefaultMessenger.ts | 853 | `bdbdfa0a4ce2e263c92f14fe4c1585d106e00371aaabb3e61f1265b05e5e81fc` | 0 |
| packages/siwx/src/messengers/InformalMessenger.ts | 2940 | `e3045fa11da91c5e94629d93fc8cbcf9a2f9741037a86ed9c12882ff1243f6d3` | 0 |
| packages/siwx/src/messengers/index.ts | 39 | `3e936192d8379bb89697cc0b9e69f7396f1fd12725f3f329325e2ad862805ad6` | 0 |
| packages/siwx/src/signers/DefaultSigner.ts | 1502 | `a6d43655abfe66a445f945867340c76ad512f3c93ccfea4402737d259ec72e33` | 0 |
| packages/siwx/src/storages/LocalStorage.ts | 2264 | `94fb476ced2c79dedeb1d10f5656fb44ebbb4de466dcacdafda06958de5a6e72` | 0 |
| packages/siwx/src/storages/index.ts | 34 | `e1a487b505341bcf3cff571abc793679050660c401d0bd219780fefd50d7ccf5` | 0 |
| packages/siwx/src/verifiers/BIP122Verifier.ts | 636 | `5d77caa56b693d1ccb5e4bd8011af20ea014aec6d880083fed763583298330dd` | 0 |
| packages/siwx/src/verifiers/EIP155Verifier.ts | 1162 | `28c69c958ac66e8a227a14f92341a04775ef3ee95fed84937160d387a679b010` | 0 |
| packages/siwx/src/verifiers/SolanaVerifier.ts | 846 | `532c35025492c29038752228974be550b5d8743d09af9e29a5ca048d83de5969` | 0 |
| packages/siwx/src/verifiers/StellarVerifier.ts | 1742 | `cf2adb6938c697a0bc2a06293eff873445a0b7f7c6d49d361f3cf7d75f43300f` | 0 |
| packages/siwx/src/verifiers/TronVerifier.ts | 3127 | `0edf7c9536ca7567e6050cb8722c652a27b007dfedb242c5872f0c24f70ef6e9` | 0 |
| packages/siwx/src/verifiers/index.ts | 179 | `9c7480c63c5c500ed86da6a4bcc5e90a2975deea14d2fc8ed9e483a53c061845` | 0 |
| packages/siwx/vitest.config.ts | 124 | `2280afba9da86c8cb1ee00b9ea75075c157f99f0635febfdf8ec28c4b4df347c` | 0 |
| packages/ui/exports/index.ts | 616 | `4f37444c00975b354a7d05c9899473720e179d653bec07d06a0575aba2e75a6e` | 0 |
| packages/ui/exports/jsx.ts | 44 | `dc6d0c993a5db14706a26dbf0cfa36d4e6748251ba818cb8524e13676ced7f92` | 0 |
| packages/ui/exports/wui-account-button.ts | 62 | `a05d996421ae4acaa5e1c756a9696c04993e354da974cfe74e9c526d2fb8fc86` | 0 |
| packages/ui/exports/wui-account-name-suggestion-item.ts | 76 | `3a2057e3da445e45c9bec3e726b8dac7a14524f3a01d82db3903a23e5ca6cf90` | 0 |
| packages/ui/exports/wui-active-profile-wallet-item.ts | 74 | `54da69ac2a71acddfc584fbe2e6ce9e3586920ed3fce9c859c8b02693b989f8d` | 0 |
| packages/ui/exports/wui-alertbar.ts | 56 | `ce32417a87872e22d00d7b04623e509a8804c9d415971769f25b4969d9aa18ad` | 0 |
| packages/ui/exports/wui-all-wallets-image.ts | 65 | `89772adf5adc8a616f9cf5d54164320dda349e6d1f95f2c350ec32d4ab738b1e` | 0 |
| packages/ui/exports/wui-avatar.ts | 54 | `f75519eb3391bf436a291721ffac727fd25b0b8497ae1eff7ecbb2dc1388f7b8` | 0 |
| packages/ui/exports/wui-balance.ts | 55 | `6393ad7b983e81bb5260cb78dbd33b25f3f1e702f31d24062f5be92eabd25f75` | 0 |
| packages/ui/exports/wui-banner.ts | 54 | `22db8ac74edb37fcdfb12c2cb6f36bd07b443c0c12dda136026d39ae412511af` | 0 |
| packages/ui/exports/wui-button.ts | 54 | `8af952e1b6a6bafad78d41ea5e67e10d5678da895f8a024ede8d7b28479737e1` | 0 |
| packages/ui/exports/wui-card-select-loader.ts | 66 | `a81497465c0995613b1f55ceca2fc5856bb6f9851a9aae219ffe1b88dcf93c24` | 0 |
| packages/ui/exports/wui-card-select.ts | 59 | `e8a8023499458d8ce1509246001c5bc66f0630b8ab7c559d371afe4b874acdd2` | 0 |
| packages/ui/exports/wui-card.ts | 52 | `5d5304e0245b017195e1e220bb48489a8fd71cbd4434919a708606a467fe4ed1` | 0 |
| packages/ui/exports/wui-certified-switch.ts | 64 | `ffbdebafc0e8fdbc6e4840f1732faadddcc1b2c1f4a1467dc9ae10a5e4ef696d` | 0 |
| packages/ui/exports/wui-checkbox.ts | 56 | `a5847e3b4dc20ad8320d7f536651eadc72935ac44287907693ad444378260441` | 0 |
| packages/ui/exports/wui-chip-button.ts | 59 | `cbd63dad6e22796aeea5cf2a50e6c519049300918861c1ea31e70e5661a1d73e` | 0 |
| packages/ui/exports/wui-compatible-network.ts | 66 | `ad597edd3bdd305bd0be4925885fc72a4d8cf34de99053b1bd64a011786aee34` | 0 |
| packages/ui/exports/wui-connect-button.ts | 62 | `af5e409064404e37d951939c84a7b131c5c983d0df31ba6c39102947aedb374f` | 0 |
| packages/ui/exports/wui-cta-button.ts | 58 | `51b2133f99ed3e64e9b706f8d30477a19062dd5ac235aefd48dfd3861308bac9` | 0 |
| packages/ui/exports/wui-details-group-item.ts | 66 | `064e9cb0a0864f7e41d3c71d7f3a6d796d0efa1aeadb5f8565289c851eae0aeb` | 0 |
| packages/ui/exports/wui-details-group.ts | 61 | `f34ec3a09cc9258f4ec4d55160898389e4c5f36a244d2a1195096c0c567b8151` | 0 |
| packages/ui/exports/wui-email-input.ts | 59 | `0dfe21fb848481bde148a47475e1635b5f77c4cd551cb1110521c599a1288572` | 0 |
| packages/ui/exports/wui-ens-input.ts | 57 | `5be2e1712d7d8687167e378055a54f4c9a1c154944318b1fd49975e4ba2ea3fa` | 0 |
| packages/ui/exports/wui-flex.ts | 48 | `77db34ad4949a6f06377b0e766716b1da5772aa3d88a0508ae432c91b6aa49af` | 0 |
| packages/ui/exports/wui-grid.ts | 48 | `dd618962b80b8031e56c6c16a426c338cb1309f53388fa51ea407d72731ab0cd` | 0 |
| packages/ui/exports/wui-icon-box.ts | 56 | `08adb07e29c8f0c04ef70dcf93cb859bccf6cb4ad9da77013d43b800605f123d` | 0 |
| packages/ui/exports/wui-icon-button.ts | 59 | `ae18b2eb29d3dc0b03226468b0224fbffc988454c115a3ebd1a9713940ab4647` | 0 |
| packages/ui/exports/wui-icon-link.ts | 57 | `ce1e7a4f1e623e7958afa97ffdcd6561209d9f6b32d02605e393f107121f58a2` | 0 |
| packages/ui/exports/wui-icon.ts | 52 | `cfb1c88da65e60c1056f35ef85a0e67b3ee4cc4780d3d7f8bb6ff0631b4d4628` | 0 |
| packages/ui/exports/wui-image.ts | 53 | `13ab882d93cbfdd7d81608d1c8add0370554d3616894b261384870fe1d6320fa` | 0 |
| packages/ui/exports/wui-inactive-profile-wallet-item.ts | 76 | `c68c9c40205376809a8b1dbb620ab4e7eea08e2a4edb71b6a69a82f5cd62b65e` | 0 |
| packages/ui/exports/wui-input-amount.ts | 60 | `92fa6814f9805ca4feb890e197c537d0a36ea32f5b3ee48210fc703d5240c0f6` | 0 |
| packages/ui/exports/wui-input-numeric.ts | 61 | `85d61c425b92964cca0e5ee636e7591255a4783d46b63ebca70126ef64b9f4c4` | 0 |
| packages/ui/exports/wui-input-text.ts | 58 | `1a3100334cce8e8e8ce80ccd46dc124c5942864f736735a7a894bdfdc913ea7d` | 0 |
| packages/ui/exports/wui-link.ts | 52 | `71f698171d6f0a4f8a581317be2ec8d1bf7058b006b4c70f4519040dc5ba2f7b` | 0 |
| packages/ui/exports/wui-list-accordion.ts | 62 | `4b2f1835a9932fe57391dc43a9ee0a3a122a8fd64f6e7b8da986f1a3c6eb2083` | 0 |
| packages/ui/exports/wui-list-account.ts | 60 | `46e679e31fa956c0a53a539668d2712ea6913ffc99816315ab60e0c629c9cc4d` | 0 |
| packages/ui/exports/wui-list-button.ts | 59 | `098ab32b1811a57ac954afb595149a0f27c337dac64b314bd7a1c2b297bcdc71` | 0 |
| packages/ui/exports/wui-list-content.ts | 60 | `4daeea1bf5f16047cc5c4c2d22601e8456cea2b27e74c743527e57b8b131db16` | 0 |
| packages/ui/exports/wui-list-description.ts | 64 | `eabc982c33d1c79b0d911d4cb1ae92626ad700e0fd498488fdad742ea61d5def` | 0 |
| packages/ui/exports/wui-list-item.ts | 57 | `850f2622a63b04e03ebed71dd9ec389c18898bba66b470e57f5d045ebeb55f8b` | 0 |
| packages/ui/exports/wui-list-network.ts | 60 | `63aa5154be7b6de49fba776f5d6492b088c2047b7c94701b63e553019ff96395` | 0 |
| packages/ui/exports/wui-list-social.ts | 59 | `7bd4bb2b7d516366bb2fee8afdaadd9b029951b8299240ad77ac53388e92cdb5` | 0 |
| packages/ui/exports/wui-list-token.ts | 58 | `6e38b1d619411668ffff2428943de2a736bf22ed4bb5d8c58939641bbe08c9b6` | 0 |
| packages/ui/exports/wui-list-wallet.ts | 59 | `4619474fe1c3dde7ec2be71975494255907a896a06a0e1b01610cebc7e2f0c8e` | 0 |
| packages/ui/exports/wui-loading-hexagon.ts | 63 | `8bc90fccb94c63391f2411980bc30cdc5b8f61197601a64f26a87cc462638542` | 0 |
| packages/ui/exports/wui-loading-spinner.ts | 63 | `e32044434684a4bb519d0d7fdec7446d651a60280854356a2c21b6a5e0193fff` | 0 |
| packages/ui/exports/wui-loading-thumbnail.ts | 65 | `bc5f53f1bf64e36e7a56d491581d5186de814ab270e47e4102a21166308efefc` | 0 |
| packages/ui/exports/wui-logo-select.ts | 59 | `d9692fc4cd04c55a639a07caf3c2865f02a6d8ff715e3e79c03f624ec43586eb` | 0 |
| packages/ui/exports/wui-logo.ts | 52 | `01624f0ffdf0ee52248c70bc1a7bf0c8069a369e69e582eb0cbe43a61cdda2dd` | 0 |
| packages/ui/exports/wui-network-button.ts | 62 | `ab2e4683787064592b0a801c1bfd45897306c6b592a6aded05f8d80593fa0754` | 0 |
| packages/ui/exports/wui-network-image.ts | 61 | `0623ed513fd9e9578d837ff99cdeaa649c54f12ae13e0663349508ee9a8b36e9` | 0 |
| packages/ui/exports/wui-network-switch.ts | 62 | `872ef4a1896874cabb37c9041ac4c2c902853fe8605ec0b7d8653a3ea33f5b1f` | 0 |
| packages/ui/exports/wui-notice-card.ts | 59 | `16b18343303a94708f562bede90553e4c33007a7aec226dfc228d088ebaf113f` | 0 |
| packages/ui/exports/wui-otp.ts | 51 | `4cd818afa3508cbb250e10b2130f88600998b8e149a238618bc49b99c5257b7e` | 0 |
| packages/ui/exports/wui-preview-item.ts | 60 | `417834e6769f45449e7037c047d5830f326579055dc261a9a7184b89b27b8c71` | 0 |
| packages/ui/exports/wui-profile-button.ts | 62 | `bb0a6da3f900107df428fafca6c05f673df3550502f45f97ef77a32504f4b897` | 0 |
| packages/ui/exports/wui-promo.ts | 53 | `b8d0e947ed1b71866baa3c0571627c226519befab9f0b58a6ccee9674b5ea577` | 0 |
| packages/ui/exports/wui-pulse.ts | 53 | `1354f76f1b2ecf086e8d0352ad79494a079c5c31383f60a893aee41f867186c8` | 0 |
| packages/ui/exports/wui-qr-code.ts | 55 | `b80ea8348b3760580ef0211f8a269c63db39216d04e39a5ad33c6fb43447df15` | 0 |
| packages/ui/exports/wui-search-bar.ts | 58 | `2b44f965e45d03455e9a7e67b3fbc5f05442cd71b2a0769b7885a752adcb555f` | 0 |
| packages/ui/exports/wui-select.ts | 54 | `df45ac46d91f898263b5de0c36f51e5da0c87625a850c6e1e2fe20034cee3adb` | 0 |
| packages/ui/exports/wui-semantic-chip.ts | 61 | `cbb4b989f243dd19e7d6c66647e656ec858cd12b0c15f88bc728a11ab361d432` | 0 |
| packages/ui/exports/wui-separator.ts | 53 | `f8b69922fcaaa343c59a44a74c30869dd7f08bb08ab7bcd40e75c3e495f44af1` | 0 |
| packages/ui/exports/wui-shimmer.ts | 55 | `087e2d19b9936518d3575ddc10335271c7f33009c5b93dd425b6c584514a7028` | 0 |
| packages/ui/exports/wui-snackbar.ts | 56 | `92e97618cd8094212f095daefaee8088a7dd5865e63111ca0821be9cfd67811d` | 0 |
| packages/ui/exports/wui-tab-item.ts | 56 | `4e1ff8270e3252fe705c4156008ef17421700f4b0d7bb2f80874155f60b0257c` | 0 |
| packages/ui/exports/wui-tabs.ts | 52 | `68ca4a56ba85f7a2108e34b2de5cdd8aeaf6a31536d42788f88fc4193cbbef2e` | 0 |
| packages/ui/exports/wui-tag.ts | 51 | `1c48cf398fc34edeaaebb1333bf252bc1dd6a363a60e2b1a1cc4f273870e5a71` | 0 |
| packages/ui/exports/wui-text.ts | 52 | `556757daf17b3966a678226971ce6601f3372268630f18f7842eb3bf0ab6b207` | 0 |
| packages/ui/exports/wui-toast-message.ts | 61 | `70fe4624c765a1891c1c026d543a78bfe4ff795bb48c7d0b4c6252607cf09e54` | 0 |
| packages/ui/exports/wui-toggle.ts | 54 | `843c567c36a58fd52551454f8928480bd6b4cf40567271d81419e71280e55d2f` | 0 |
| packages/ui/exports/wui-token-button.ts | 60 | `69b4a33df7f6f344ec4321cbd86b24d7001b075e602c1aa4e9477ba0da65b602` | 0 |
| packages/ui/exports/wui-token-list-item-loader.ts | 70 | `1fce49a4a87861044ed841e620c365d2794959bfaba4e426a046802856846124` | 0 |
| packages/ui/exports/wui-token-list-item.ts | 63 | `956a72764f13b59bb15648cde3441ba66e24f8ccb453ca8fb37f7920300db75e` | 0 |
| packages/ui/exports/wui-tooltip.ts | 55 | `d758ee7bb27cac33d9c07759f33a0543b7af9d37729e0ce045ab0cfe19fdae0a` | 0 |
| packages/ui/exports/wui-transaction-list-item-loader.ts | 76 | `4246c0541aefa5d063013d9ef625fa73a63aa355b4c2d106a569a3d55f401e7a` | 0 |
| packages/ui/exports/wui-transaction-list-item.ts | 69 | `9cf567db022096b0744d5093cc017962d283a18a4da0fc55c46c9a957025f3cf` | 0 |
| packages/ui/exports/wui-transaction-thumbnail.ts | 69 | `f72b2d651dff5ac4127a87af13d1ef94236e32d9e88467b1dac458b2c35aa206` | 0 |
| packages/ui/exports/wui-transaction-visual.ts | 66 | `a94ffc6f22e5f1b014447c1d9fb5ea2508e2fcda4e51017e88391753ae7d171f` | 0 |
| packages/ui/exports/wui-ux-by-reown.ts | 59 | `631cab44924a2cea42ae4b21714ded6a2c5212b92111ff22e41ef7d640a78cb3` | 0 |
| packages/ui/exports/wui-visual-thumbnail.ts | 64 | `af6f817e3cf3e6c57a0e2010b735b528f4735b2bb02374804fe842a8ebd382be` | 0 |
| packages/ui/exports/wui-visual.ts | 54 | `322d0223609f8905ef3c8079380db9f16d4ba07ed0bfb4d7bb13af17fb22e133` | 0 |
| packages/ui/exports/wui-wallet-button.ts | 61 | `a599f7c6c6b2be144129d65c371c5423185c53be1112a8920fc22c34208246e5` | 0 |
| packages/ui/exports/wui-wallet-image.ts | 60 | `80bf36f69a9034229c2dfd2cc888c4db890b67f8481cf79c98639a5aa0f7f880` | 0 |
| packages/ui/exports/wui-wallet-switch.ts | 61 | `026f2988c1a7c96de815358aa62d34acda6cf272800bf69bc8ae411fb959de13` | 0 |
| packages/ui/package.json | 20022 | `ee1cda7c5475018b5f5f8c4573ddcd830a585f30669b323d360e1137ff16debf` | 0 |
| packages/ui/src/assets/svg/app-store.ts | 3117 | `1bf6b05c5fc0d88e3e78ec1a60ae61c5e156da08525f2f58505feecb04bf3552` | 0 |
| packages/ui/src/assets/svg/apple.ts | 883 | `26272325458d610aaa3d356fcbd95afbb6b00a0a8adc16da5bb241bbf583e25d` | 0 |
| packages/ui/src/assets/svg/bitcoin.ts | 938 | `7eadf66ce8d1d1bcddd668660a2dc6fc411ccadb04599e85f7cd24d3603022cf` | 0 |
| packages/ui/src/assets/svg/checkmark.ts | 994 | `86350c0b2cdbbdebd3241586b60a193ae34fddd99275f6fd2833788b146899d4` | 0 |
| packages/ui/src/assets/svg/chrome-store.ts | 3082 | `1d9424a3a2281a9f2ec84bca4e24951e914f614347d28a6179f9ab7ef79edf61` | 0 |
| packages/ui/src/assets/svg/coins.ts | 1182 | `65d317906ec3e7b747049323f1042e9070556718687b5b0d3fdbc1420db9f4e0` | 0 |
| packages/ui/src/assets/svg/cursor-transparent.ts | 553 | `7954f5ef243f6c87f780de4bdfa3fa02fc0f33cb03bd2e35e6149694c6baed8d` | 0 |
| packages/ui/src/assets/svg/cursor.ts | 183 | `a0ba318ce440b24c7b463a2544fdcab68db827bab5bd3625b993cab67a977186` | 0 |
| packages/ui/src/assets/svg/discord.ts | 1225 | `277f2f6036005f846a09b3c4016614797cf6909aeb0b9b7e57c9783742ae1274` | 0 |
| packages/ui/src/assets/svg/dollar.ts | 7151 | `b1724f27d89b4b552d305aea84f62d37fc076a713ba72aeadb5d9891bd503f63` | 0 |
| packages/ui/src/assets/svg/download.ts | 1078 | `e3b033cab33d951b16f7b19464a46f9ac618d0b5d7e71b64c37ddd77c31872ae` | 0 |
| packages/ui/src/assets/svg/ethereum.ts | 493 | `f798310722a71ba4c41916b03ab37be06d4de4c78f3093f62d1cbf116147a1c0` | 0 |
| packages/ui/src/assets/svg/etherscan.ts | 628 | `0a4fcbde16bdd35fd18cf3397c4dffe40f3e23b9edc6c1e9a45c15bdabe510e2` | 0 |
| packages/ui/src/assets/svg/facebook.ts | 1158 | `f1ff4300ce033177b3d64a17a01bba8dc66c81048569d1ce0ec2776260f2a7bf` | 0 |
| packages/ui/src/assets/svg/farcaster.ts | 940 | `6b61613d9c1c7d53b22f1e019b9c72f989ef78dbd8316fed2ca1527ce6b9e85d` | 0 |
| packages/ui/src/assets/svg/github.ts | 1054 | `3e71dd6b776817dde01064da783d5e216a3a1f38b66312bf390e69159d3ec36e` | 0 |
| packages/ui/src/assets/svg/google.ts | 736 | `8a2fc4db8c87e50e743283edf07ddf2522606ca5f388e21ffa180a476042e4d9` | 0 |
| packages/ui/src/assets/svg/info.ts | 1681 | `09ce4adcadcec924cce137c4c4e79ec6e7ed8cc6052d9caf46d3ab78e6673ec1` | 0 |
| packages/ui/src/assets/svg/networkLg.ts | 491 | `b81dff0b5398b39117a9a2104b00048b199890cd63535aba3d68ceb2356ad1ee` | 0 |
| packages/ui/src/assets/svg/networkMd.ts | 492 | `d107660a954677b54cfb13a7c6d60c3a430115589ef00c18457459669225d4f6` | 0 |
| packages/ui/src/assets/svg/networkSm.ts | 342 | `d942526c700e1e0b87e57f97fe01890e56884bcbb769d083f5cb6c1b9748de96` | 0 |
| packages/ui/src/assets/svg/paper-plane-titl.ts | 1306 | `63b56a41488505dbc4df042fb4ceff5fd8572fa1cf43cbfeb215d5b68a832de7` | 0 |
| packages/ui/src/assets/svg/play-store.ts | 1222 | `a3d257f5e08df32aff7d81eab1e9c6aae13754a032a1f8bfb2580d9d99243d5a` | 0 |
| packages/ui/src/assets/svg/reown-logo.ts | 2867 | `32bf46e756cf2a00435ac5f3c824cfa192f5378d88c745f7ce5f88c3e9fa2081` | 0 |
| packages/ui/src/assets/svg/solana.ts | 771 | `c94a9f9c60ec523188a234824c2a72a1299b4357638e65f9b45b4171c7ccda6b` | 0 |
| packages/ui/src/assets/svg/swap-input-mask-bottom.ts | 4629 | `1a1fc413e4c5f676450af1d9d7289d09068c2a20ff554991f5364306a6e4f129` | 0 |
| packages/ui/src/assets/svg/swap-input-mask-top.ts | 4599 | `f74ce70c505fdd9f061dc8c30abcd6355a65e1e8d07c247a33ae5f9dd8d81d12` | 0 |
| packages/ui/src/assets/svg/telegram.ts | 1376 | `11ab034628d9311e494bc62b99b66d855e051fd8872489bf7c4536008711b354` | 0 |
| packages/ui/src/assets/svg/ton.ts | 633 | `773d2d3c6c73a1baebc8f0ea8601d879e4dd209075c2ef8e53d5961a80bfbf6b` | 0 |
| packages/ui/src/assets/svg/tron.ts | 652 | `299ea3a31df709eff85aeeb571f627e0a83945dbe633399579100c3485f3271b` | 0 |
| packages/ui/src/assets/svg/twitch.ts | 823 | `57e5898aae721a288731130f6cbae553441087e36c5a5f1bacfdf1f0214b09a8` | 0 |
| packages/ui/src/assets/svg/twitterIcon.ts | 508 | `abdcc66abb5d74201cc1c3a7f036a2995df80671ba39bd9c608d958d829b7ddf` | 0 |
| packages/ui/src/assets/svg/user.ts | 1974 | `57866af947f5228bc9e1f498550c98180350615e66c07048f818daeed88890df` | 0 |
| packages/ui/src/assets/svg/walletconnect.ts | 3877 | `21d90ac16f0cca8057ba5ab02807c4ad26aa08ceb6a9285706e93cc3920ea73a` | 0 |
| packages/ui/src/assets/svg/x-mark.ts | 719 | `bcb8383c494e71247b4f62174244a5afc2e0e8e8a27d9c8e687f402c8cdbbf9f` | 0 |
| packages/ui/src/assets/svg/x.ts | 493 | `933ac30194624df5094f270471ef3c736d813fd2adbed383402ea841d7a67a07` | 0 |
| packages/ui/src/assets/visual/bitcoin.ts | 1900 | `1160bd2ef2bf8aed4a28d27589e494bb663b1696480cd8e1a6799cc2796a7f41` | 0 |
| packages/ui/src/assets/visual/browser.ts | 1339 | `47a0eaab7732f27ddd5c50f48f4bd63aacc736a4ae6cf23f60cea44894adc5c5` | 0 |
| packages/ui/src/assets/visual/dao.ts | 3778 | `bccfa2f4692c48c101cf862b21c43145e87900baacc148671a3aedd12eba65da` | 0 |
| packages/ui/src/assets/visual/defi.ts | 2615 | `1cb6dc5e4472bdd5ea2e103e1525d4c54c32c8e1d0d1dd1b21bc29198bd006b4` | 0 |
| packages/ui/src/assets/visual/defiAlt.ts | 1629 | `90b4f615717ef562b36535bf81864e0f48d4d3e5caf158b63864ce8d1b540989` | 0 |
| packages/ui/src/assets/visual/eth.ts | 1435 | `6a7675dc95201b3facc2a2fcade7a735701fa9bbf0680f5a8db2883acbb6b9bc` | 0 |
| packages/ui/src/assets/visual/google.ts | 2161 | `386cc9daed2e116b5c4be77af5fc4628460ca79d3e607fffccc81f014738c2b7` | 0 |
| packages/ui/src/assets/visual/layers.ts | 1914 | `21ac9d901fad88026512f203ce6070b6b12c56e1c99632ed90dceefc717c16cb` | 0 |
| packages/ui/src/assets/visual/lightbulb.ts | 4256 | `c212d838539c29832f82a8b822ed305067761de84386812458d25f27ef2974f8` | 0 |
| packages/ui/src/assets/visual/lock.ts | 1787 | `259492c51594feeb269d57218bf81eb62720d4f3aeb79b11f82194f0637f6570` | 0 |
| packages/ui/src/assets/visual/login.ts | 1922 | `36697485cd50dc7b77528d977e081136672b62349c3617eb028618f3882ab0b0` | 0 |
| packages/ui/src/assets/visual/meld.ts | 1952 | `bdf041ec2d6f853f0119539cfc4334b499e55ed61bb2f2b6d3f0f706bd606c37` | 0 |
| packages/ui/src/assets/visual/network.ts | 1037 | `f3216ab78b267e5792caec355f8ca09fbaa85ab445b6a9fb209b101b2166a83a` | 0 |
| packages/ui/src/assets/visual/nft.ts | 1391 | `8c120514da55da62f3d1ec9c3b916cb5acc7e13dd3bb718fdc5e3a800fc54900` | 0 |
| packages/ui/src/assets/visual/noun.ts | 633 | `894aacf6aaab242daf25984a048c87c8281d603ac429b3a484f585884d907068` | 0 |
| packages/ui/src/assets/visual/onramp-card.ts | 3369 | `ef5982945ed81e14c41a0fd903433b31ba6df6d507eb75c69cdc899980bbf686` | 0 |
| packages/ui/src/assets/visual/pencil.ts | 3468 | `c368af5c90ccfcef76502fe012d8d9f57d94ea36fe0a09a93b2a6b96b5907c33` | 0 |
| packages/ui/src/assets/visual/profile.ts | 1552 | `7125dba2fa1b8534188f8cab02f8724882e42f9c0bb9cf36a2c54e0c038dbf5b` | 0 |
| packages/ui/src/assets/visual/solana.ts | 1400 | `6bedb5417a0e739b086a756f186e337e4354dd521ef5083a3e9495f2f96add73` | 0 |
| packages/ui/src/assets/visual/system.ts | 6376 | `889d5db2fbfe11bfa037d05f5580aeab5b34db6c86d69ad72a20425db190a33d` | 0 |
| packages/ui/src/components/wui-card/index.ts | 533 | `ecd4c4aee6c37d63d0757cfaca8b37a82dfc42dbeff51a307b9a2210d0e1cafb` | 0 |
| packages/ui/src/components/wui-card/styles.ts | 290 | `cd7056310cc6855e1cfb07e4bcfafc512ab4b5ba3cafd7364731993e8ce41dce` | 0 |
| packages/ui/src/components/wui-divider/index.ts | 946 | `7ea21982f895e7df8cca93d72ffcfbb8e901c7d3196f8f9e5101463e400eadd5` | 0 |
| packages/ui/src/components/wui-divider/styles.ts | 494 | `8f8da128b08ead1b14d994d1d836095d48c5f6c507fd6977b4a33d935d8733cf` | 0 |
| packages/ui/src/components/wui-icon/index.ts | 12117 | `aa6d2aa907bd6b2659edb1126a0ce4bfc616b39c7ed66fda2b6894501a5fac72` | 0 |
| packages/ui/src/components/wui-icon/styles.ts | 331 | `54a161417df5d13f0a709e3122f2b76d5c81f8cf3920c2ce007474209a366f30` | 0 |
| packages/ui/src/components/wui-image/index.ts | 2427 | `c06be16beda7fd332b1b4e7ada70499fc1dd2efac20b5297807fb1531380e1bd` | 0 |
| packages/ui/src/components/wui-image/styles.ts | 1255 | `4635a9d7431a74e7fdd314a7d68b35c267b7b5ef4c1830b75d82886a84c10885` | 0 |
| packages/ui/src/components/wui-loading-hexagon/index.ts | 1378 | `efbd4703d4fafca26164e295cdadf69fee2dfdaffc4755edcfe0f0e83ffaacc8` | 0 |
| packages/ui/src/components/wui-loading-hexagon/styles.ts | 520 | `ca21b9fedd4ed71c883ee507808f20400df2a141f01b79a7481a4faea06cc18a` | 0 |
| packages/ui/src/components/wui-loading-spinner/index.ts | 4599 | `875f499940d274e5e8565003e6707da8c6d39e0b40af75dccd1eee523770c130` | 0 |
| packages/ui/src/components/wui-loading-spinner/styles.ts | 685 | `4207b5ca338fd8198483d0dc94e06410c0aacc604db47ec5cbfe440a9fe6c081` | 0 |
| packages/ui/src/components/wui-loading-thumbnail/index.ts | 1380 | `00a60bc170a5db3a0cfcbeb63f5d5cd2225574a096ed646dcf25318b745a4db1` | 0 |
| packages/ui/src/components/wui-loading-thumbnail/styles.ts | 437 | `0f87f2355c7ce0e9aa444a3f7d2da2b1cb06da33e3b3009131bda1a83f4e19d0` | 0 |
| packages/ui/src/components/wui-shimmer/index.ts | 1009 | `dba25c9abc5e0435051340d22ea5e66d94d1e5f4f6688a6d1ba9210da6352b1c` | 0 |
| packages/ui/src/components/wui-shimmer/styles.ts | 714 | `7038bed776817c01ed6f2bdfa307a98800697bbce3d6918e0f3ffe39f6d27d60` | 0 |
| packages/ui/src/components/wui-text/index.ts | 2070 | `4dc126f4456224b9e18131cebfa0b800f9af536883bbd18f1bbcc81d30af3dca` | 0 |
| packages/ui/src/components/wui-text/styles.ts | 11548 | `dac50cc69d32b906de004ac5ce3680d1a0689e78748240db0eed405899db6b90` | 0 |
| packages/ui/src/components/wui-visual/index.ts | 2691 | `122b4d03f5aa00dfa523c0634b59926ddb3451a23f14037465f614041645b9a0` | 0 |
| packages/ui/src/components/wui-visual/styles.ts | 198 | `1a5d0af68a2eaa1d690db39dde45e90cd628c472e887a0a504a77f675da77d43` | 0 |
| packages/ui/src/composites/wui-account-button/index.ts | 3332 | `24f9d192410c219a6b2b5ce211c0b98bc55e79630d302dd93e3da6e3125b73e7` | 0 |
| packages/ui/src/composites/wui-account-button/styles.ts | 2333 | `de1d13c74ff3c2b0664f60133bbee89e5f875132d5ab87fbb1492f5beb4518e7` | 0 |
| packages/ui/src/composites/wui-account-name-suggestion-item/index.ts | 1675 | `c57671be819c02a9af805b644cc8b71e6792cc62f8ceaefa4a4e4cf7dc0fdbd7` | 0 |
| packages/ui/src/composites/wui-account-name-suggestion-item/styles.ts | 1012 | `2858278625121a075c699e1a8529e46809ca7b49167afb3cd15f34dca4e88557` | 0 |
| packages/ui/src/composites/wui-active-profile-wallet-item/index.ts | 7214 | `470c85328f7746af55e45229e2adb3a76b73d4568e3759d0be793b021e44c2fe` | 0 |
| packages/ui/src/composites/wui-active-profile-wallet-item/styles.ts | 885 | `1066957cba1525cc532141a8b253d97f507999d2313eac564383383a11ec9b00` | 0 |
| packages/ui/src/composites/wui-alertbar/index.ts | 2177 | `1e46d1af2d69c0d2bdf609290f3530ecab20c6c4554a4b1ca8aff7d4356fc919` | 0 |
| packages/ui/src/composites/wui-alertbar/styles.ts | 1914 | `74fa667d74df19ce7ab312de5593b9fc7601bb554a7d357c3adc9e17c5d175f5` | 0 |
| packages/ui/src/composites/wui-all-wallets-image/index.ts | 1488 | `c68548bbec792213868c3da705b5c0fafde1d4048b3d2e6391cb5cd44ca34dbd` | 0 |
| packages/ui/src/composites/wui-all-wallets-image/styles.ts | 579 | `ec012cd149c7a493f3bcceebb694223f814563dd4aa1debc8d342a769173135e` | 0 |
| packages/ui/src/composites/wui-avatar/index.ts | 1907 | `c364be88aa12e2f869803695f00d48feb1ea059a1c084cfac207b4d4edc2de1d` | 0 |
| packages/ui/src/composites/wui-avatar/styles.ts | 1151 | `38bcb7c9c48f0c568f806438d03bde4b39edab16a8ed0889e1f5d54dd8efcd06` | 0 |
| packages/ui/src/composites/wui-balance/index.ts | 773 | `a42256c07f3fe2bc5ab6fc56044f170b20c0a968cc8b1ae6c22b260b3c7be6d7` | 0 |
| packages/ui/src/composites/wui-balance/styles.ts | 385 | `e2e46f972bb780501d8461c03080a460ecfc16459e16a0ea5d5921b64a268bbe` | 0 |
| packages/ui/src/composites/wui-banner/index.ts | 1209 | `44e1d865500b2b8d736d6b5aee563e88970915391d4c9cc07cf998259b0c87f8` | 0 |
| packages/ui/src/composites/wui-banner/styles.ts | 1587 | `d35467a3c8560fcf087b543422a52e0f5f7e873517e11f6186ebba2726ac2de1` | 0 |
| packages/ui/src/composites/wui-button/index.ts | 2395 | `3296d3a431b77c0aad037ca1366f3fb8e87f6f858071fb98fb9dfcc5d6267f3d` | 0 |
| packages/ui/src/composites/wui-button/styles.ts | 4398 | `a44bc44798745bef6b7d52d77d5eef0a01eade2176ac4121083b2c8b05dbea35` | 0 |
| packages/ui/src/composites/wui-card-select/index.ts | 1949 | `6cfdd6895c8c85f6a0768b4a7f5304c6031bcdc703997eea2d92e84f7bcc345a` | 0 |
| packages/ui/src/composites/wui-card-select/styles.ts | 1036 | `2992d8308bf525ec965f4e582aad50df3722ccb730fe50ae006913c9a2769466` | 0 |
| packages/ui/src/composites/wui-card-select-loader/index.ts | 1303 | `e2a896c9cc5087e4065a8bf06df5885cb56f109efe70202489b4a2f2ad13e0c7` | 0 |
| packages/ui/src/composites/wui-card-select-loader/styles.ts | 849 | `25e4be1c004d07aedec03e04c3f391f1d4c92ab226f0500562163d1079acdaa6` | 0 |
| packages/ui/src/composites/wui-certified-switch/index.ts | 1480 | `7fc747a3aea4bf5882694d8f370cc0136edaa0719a98580b3d712c19e560904e` | 0 |
| packages/ui/src/composites/wui-certified-switch/styles.ts | 802 | `71908bdeb0417abdd5b2e4b6c142e6ac1e3d02a5abe5cd70825d879e253d2169` | 0 |
| packages/ui/src/composites/wui-checkbox/index.ts | 2150 | `32c2084d4551ab3f93ea38823dfb8dbbbc91357f2e80189dc047596434d199ab` | 0 |
| packages/ui/src/composites/wui-checkbox/styles.ts | 3160 | `0d5153239f73fbc92e1d8b929e80283b6ac29b1b722b5d3c520d2471e758189f` | 0 |
| packages/ui/src/composites/wui-chip-button/index.ts | 2015 | `e1593a782bf33b85030c7561e5ac9e33c9a40508345d6e5205f701ef30541aca` | 0 |
| packages/ui/src/composites/wui-chip-button/styles.ts | 2803 | `594a4cec2ef58c8e46131b014ebb1205e58e9fac58e3f3d0a8205703c6266708` | 0 |
| packages/ui/src/composites/wui-compatible-network/index.ts | 1624 | `f160d1e1cec3c6ac919cca735d6c1e7dc506ca9ff022a62acbfb991c7a2f4bae` | 0 |
| packages/ui/src/composites/wui-compatible-network/styles.ts | 1614 | `add83cdd3a4a5c6809f00b1c3816acde275110c8030d275c7c23194d4c9ba148` | 0 |
| packages/ui/src/composites/wui-connect-button/index.ts | 2001 | `b1a37bff355bb8234e8c4a4ae1ffa237ebfc421f43c25f545d8e546c3084bd2e` | 0 |
| packages/ui/src/composites/wui-connect-button/styles.ts | 1440 | `6caebec0371f394e686c115a22bc6c9ff11b70f2b6765ef8c59bf6fbe4837b1e` | 0 |
| packages/ui/src/composites/wui-cta-button/index.ts | 1349 | `e4210ca7eb6c03e6f1dcd7e9f5de01c3e9be296b706d010b3a16dcb11a446b44` | 0 |
| packages/ui/src/composites/wui-cta-button/styles.ts | 795 | `3b64688046bd518e3b85fbbe4ff0e38dd8fc78aa0b11019111154246c0a03058` | 0 |
| packages/ui/src/composites/wui-details-group/index.ts | 768 | `dd052d618f0bb84f940400e50a53076de6f748d44c3c14933944b699d0265349` | 0 |
| packages/ui/src/composites/wui-details-group/styles.ts | 463 | `bc435dbdc6fc2c88466e5085ea6f2d500750610955d2c445abbc15ce8a66b8f3` | 0 |
| packages/ui/src/composites/wui-details-group-item/index.ts | 1105 | `312b4369946612636ba05aa824f7d79a3f839c4cf568df067cd5980e3d081725` | 0 |
| packages/ui/src/composites/wui-details-group-item/styles.ts | 253 | `50045db87728be8be758634caebcb0a754a1d23c6ce17d6dc5c981de4fc1779d` | 0 |
| packages/ui/src/composites/wui-domain-chip/index.ts | 1836 | `6c701c5ad28eff14a51941b1973eaeae1d5d4badacd71129057befea74e36ed3` | 0 |
| packages/ui/src/composites/wui-domain-chip/styles.ts | 2557 | `7cc78b806257e59b4ff1e49121e2585ca2bf51e88a8045cb7cc48f13e47aa417` | 0 |
| packages/ui/src/composites/wui-email-input/index.ts | 1566 | `3dcf1f7bbba99e005735f61d8cb5de949a235e4d76a3662473640c7844af92bf` | 0 |
| packages/ui/src/composites/wui-email-input/styles.ts | 131 | `3b1b4e0dec032b02a555d369e9c8f3247a4c6548aa55d057134d3152bf15879d` | 0 |
| packages/ui/src/composites/wui-ens-input/index.ts | 1392 | `2ec222c1d5253b251a82c7e1a4bc16d32aeaa3a5df57acc2b0208601994bb385` | 0 |
| packages/ui/src/composites/wui-ens-input/styles.ts | 566 | `98747b69ebf02c574bcbe2dc8919753461ff5f97f82793dab7dac16f19e102b0` | 0 |
| packages/ui/src/composites/wui-icon-box/index.ts | 1348 | `5ee1bca431aeafc622a3175692c03d7daf1514aff3672672298d6b47ae233bdb` | 0 |
| packages/ui/src/composites/wui-icon-box/styles.ts | 2174 | `535b7b47634146e5ead2c37f2450773ab602521bf968be66d350db778b985b42` | 0 |
| packages/ui/src/composites/wui-icon-button/index.ts | 1554 | `66e56cd44f7ce6c82d0f8440a6f691a57431e4ca2c9f8c38547c97161ab3cbd9` | 0 |
| packages/ui/src/composites/wui-icon-button/styles.ts | 3014 | `bc5711f9f564630fe1f4711f87a9e825d85245ecef4582bcee92a9e6adeba0b6` | 0 |
| packages/ui/src/composites/wui-icon-link/index.ts | 1489 | `f524d0c3a7feb143fc9b547087e4a380fdc86c3673b62db252ca401664c37ce5` | 0 |
| packages/ui/src/composites/wui-icon-link/styles.ts | 1695 | `eb40806b13db5a3cf43e1a8ce6f38d3ea76524c990edff1bb36d8a7f8137ac54` | 0 |
| packages/ui/src/composites/wui-inactive-profile-wallet-item/index.ts | 4417 | `21f7e8adbab1704ebc41fbf1d03c25098d8c49ae66e94857dd4a0b14c1b59ff3` | 0 |
| packages/ui/src/composites/wui-inactive-profile-wallet-item/styles.ts | 679 | `0c839e3b81522db2a595eb8d16342feeca83dcfde22626dee492f6654cae6bbe` | 0 |
| packages/ui/src/composites/wui-input-amount/index.ts | 3543 | `3b851786eb2c6984d6c4682d4f80c7b65dae1f2a19b05b8d0e31b92b21c69ed8` | 0 |
| packages/ui/src/composites/wui-input-amount/styles.ts | 1637 | `5004238b8c280a028f919eb061b3a4ea328825886533b9ddabce7b705a824b3a` | 0 |
| packages/ui/src/composites/wui-input-numeric/index.ts | 951 | `a9fbc6d600888eb7dca1ab285740257e8c586f999a1549db15ca80dd64ca1df1` | 0 |
| packages/ui/src/composites/wui-input-numeric/styles.ts | 1734 | `2171cce3f50e922da33f6df3ad4bae462495a1a31c16c6a9fef0dfae5280ee8a` | 0 |
| packages/ui/src/composites/wui-input-text/index.ts | 3684 | `ea654c118e0b4ce881dc5caf1767e52b59221148c86e82faec5e6039df8ee9eb` | 0 |
| packages/ui/src/composites/wui-input-text/styles.ts | 3733 | `1b02ddcdfe2f44ec5a96fbed39936b687223950a080cdb9d53aecac967011630` | 0 |
| packages/ui/src/composites/wui-link/index.ts | 1850 | `6ac3718230aa850c9bcc536f2b7505265636d4891b137c455b39b5eebe9a6e2a` | 0 |
| packages/ui/src/composites/wui-link/styles.ts | 1864 | `87b6ca5d0ae2d9e5b6b662ed6aeef5faf3411c2cfc8e542f81a1a7244a24f35d` | 0 |
| packages/ui/src/composites/wui-list-accordion/index.ts | 3919 | `3e6f0f10838f20e23b566ee6ce4520b5867f6cfc3b0a486f6d4d343b86644c8e` | 0 |
| packages/ui/src/composites/wui-list-accordion/styles.ts | 1332 | `cb3e2f1cd2e0fc3706a31013f1fd7de152900e973b9092c9cf6debe5da2e7005` | 0 |
| packages/ui/src/composites/wui-list-account/index.ts | 4623 | `3ee715c0af32f2906b340710cf974bb85b9f613f0d9c221257421501ac21dfb0` | 0 |
| packages/ui/src/composites/wui-list-account/styles.ts | 1234 | `fbbb0541ab290541e7168664d097cce3231a12c8509dffe8fe0bf3f3a6b87ffc` | 0 |
| packages/ui/src/composites/wui-list-button/index.ts | 1463 | `826a52611ee612c23562dad6bd7ec637b1cb7075f6dcd1696cc7f6d68840b108` | 0 |
| packages/ui/src/composites/wui-list-button/styles.ts | 833 | `917d1f3a0f537cd6788d1e7d80f98e35b6c33c2a9fe277f029081fda9b719171` | 0 |
| packages/ui/src/composites/wui-list-content/index.ts | 1659 | `d95d1413da3ae9cf3ee46e0b4ed13ba457d4a3db7c6e6741b30f7b9d569e962d` | 0 |
| packages/ui/src/composites/wui-list-content/styles.ts | 505 | `db15b8a386d0c3ea8f0bc3ae9079f8007d53de4972a792eab9a5959ec49455c4` | 0 |
| packages/ui/src/composites/wui-list-description/index.ts | 2034 | `85a843e91ee0190020f32d7a374b52f1df6fc3729b475c338a702f22a0e5f004` | 0 |
| packages/ui/src/composites/wui-list-description/styles.ts | 629 | `478d4f3980e805e3ddd9b6570d3f6af817da64250c93063393dc28b4f4464ad4` | 0 |
| packages/ui/src/composites/wui-list-item/index.ts | 3023 | `61af315b36849f1ae690181f58785516b213d6447c04cb1450926253bbd9321d` | 0 |
| packages/ui/src/composites/wui-list-item/styles.ts | 1350 | `5832b531cddc83d49d33d305e9af88a11635007ef2b7400527fa36eef1a219a5` | 0 |
| packages/ui/src/composites/wui-list-network/index.ts | 1647 | `084c6e55597a85a99a84cc5aea6073cec237c429b56f94794ed3cd60711b9b53` | 0 |
| packages/ui/src/composites/wui-list-network/styles.ts | 618 | `a0639045e7bbd2d74599451e72c97070bac438531abb2e21db2945d193a4a5a8` | 0 |
| packages/ui/src/composites/wui-list-select-account/index.ts | 2513 | `1a50109cb469d02b18b162d155ae20476222d98d1595d9ccff6e15ef252f9260` | 0 |
| packages/ui/src/composites/wui-list-select-account/styles.ts | 1769 | `a7cb04fb74b5b6e2a3bf7d675f2ff306aa26ddd1de54b3e6f570413b8ef277c1` | 0 |
| packages/ui/src/composites/wui-list-select-wallet/index.ts | 1995 | `452aaf4b0d4eff988d08f0a0ebbfd1b944f90554166e8db13785d446af5378e8` | 0 |
| packages/ui/src/composites/wui-list-select-wallet/styles.ts | 1337 | `f1a88779bc4e29349a1c27690213abc5ef497e88bfb80d70e876dd7853905b50` | 0 |
| packages/ui/src/composites/wui-list-social/index.ts | 1455 | `bac2d4497dd565d59657c597b210f794467e0bb8e2a993307fd42ed7484bd749` | 0 |
| packages/ui/src/composites/wui-list-social/styles.ts | 618 | `a0639045e7bbd2d74599451e72c97070bac438531abb2e21db2945d193a4a5a8` | 0 |
| packages/ui/src/composites/wui-list-token/index.ts | 3046 | `1f65552987b1c3b4323b8ae9befa2c75be2a2b8becebddf5a0a56a067a7ce94e` | 0 |
| packages/ui/src/composites/wui-list-token/styles.ts | 1055 | `1eeae8634dbfa4c7f741732a65b95b45bc126048b7b495e1c8339a0264131af8` | 0 |
| packages/ui/src/composites/wui-list-wallet/index.ts | 4565 | `493c1aef4d5a22ad8f60201dbb2e736af4f4ca1c70067650d5474e356f2e64c2` | 0 |
| packages/ui/src/composites/wui-list-wallet/styles.ts | 2057 | `6a7db7961a3762c8cf92a6a502355edfd67dfe29e5b246b7020c3ce79e00e2ba` | 0 |
| packages/ui/src/composites/wui-logo/index.ts | 847 | `87c39439becd3cbf5bd71b412845a3d78c95eb07e499295c60ad68023c7f9801` | 0 |
| packages/ui/src/composites/wui-logo/styles.ts | 337 | `a0c733fd632998c56651cb38e1976333b8bc5beabcaccc16dde97d469cc4836e` | 0 |
| packages/ui/src/composites/wui-logo-select/index.ts | 1138 | `2b128cd0bdf552a1d65b1f8ed10d32083602f8d0904d50a0aca8a9b9deb27279` | 0 |
| packages/ui/src/composites/wui-logo-select/styles.ts | 582 | `df7c8694c89e1200b901c5a7e0e8b246f18b85c8302ca0f83b222b0de6e7f2f9` | 0 |
| packages/ui/src/composites/wui-network-button/index.ts | 1852 | `7169e1c5b4130b5920bbde4be9f981b9f1d543811556ca658d7ccaf2736924e0` | 0 |
| packages/ui/src/composites/wui-network-button/styles.ts | 1131 | `91ccb5ed334bb5788e120e082328ee1d7c7316c8c1446db5da9db7f362146f37` | 0 |
| packages/ui/src/composites/wui-network-image/index.ts | 2583 | `fa25e68db3fe0876041f054feb4e13685c4f2fea92d6a3165d23ffd7d3001b34` | 0 |
| packages/ui/src/composites/wui-network-image/styles.ts | 955 | `79b5131f32bcabe62e76e155461647d49ad12f0e2271f77fec74d425fbfd84be` | 0 |
| packages/ui/src/composites/wui-network-switch/index.ts | 2165 | `6d8f10956f186d5ed1ab66d5c51f22280e304b3fec73d897ed6ccef89be2b564` | 0 |
| packages/ui/src/composites/wui-network-switch/styles.ts | 1305 | `09762bd25f02e76bcab751a55de127ccdccdea58053a28556d7c1c60eb0a61a7` | 0 |
| packages/ui/src/composites/wui-notice-card/index.ts | 1534 | `b0081565a5f2960d0dbc39d0173baa93cb0e1573bb2bb62d9b9e95e3bb16539f` | 0 |
| packages/ui/src/composites/wui-notice-card/styles.ts | 877 | `a035ca7248e442fa01ffacfb572d65b6ecb633730564c17c7cb835023381abd2` | 0 |
| packages/ui/src/composites/wui-otp/index.ts | 6516 | `603ffce337114edc892fd9ea8597ce0228d73b1b4fe5b896014913dbe126a660` | 0 |
| packages/ui/src/composites/wui-otp/styles.ts | 107 | `0fb97a61a7bb3322d897b134e75b5f31dcf6f1fff29e4accde7933cc18cf5a99` | 0 |
| packages/ui/src/composites/wui-preview-item/index.ts | 1562 | `98d67d47b6a1898b2311447daf26d7310194f1bc184ccc2a632b5eb9663eb5b7` | 0 |
| packages/ui/src/composites/wui-preview-item/styles.ts | 633 | `9ed2c5186395520e6ae8c13e1f8b6d837fccf722bd9551fa1dc6c1a006e08f36` | 0 |
| packages/ui/src/composites/wui-profile-button/index.ts | 2419 | `fdd0cdc79004c9436c2d4a977889a831002ae090c1f1bb5c4ab9d122a634611b` | 0 |
| packages/ui/src/composites/wui-profile-button/styles.ts | 897 | `ecbe488391ab44834ae1fceaf85635c0a83cb93f66cc1a88b292685300c27d8b` | 0 |
| packages/ui/src/composites/wui-promo/index.ts | 1042 | `632e5dff00b23af56b4e01fec89e12aa0b1839c9f5a9da19e0586386cf4b9add` | 0 |
| packages/ui/src/composites/wui-promo/styles.ts | 788 | `1b71ff96aa8539b17bae416b1197a3916835ddb93ba4a3c1e1d299deb760b1db` | 0 |
| packages/ui/src/composites/wui-pulse/index.ts | 2058 | `7a0063a7cd0699e82ff800e84ebb9859d05b81b1baff48e1a5ef6613b1d8c16c` | 0 |
| packages/ui/src/composites/wui-pulse/styles.ts | 1030 | `43eb84444ca61d8b7df9aa7acb9a881f7d76bda44c4edb4a8f2db2ba58e28e49` | 0 |
| packages/ui/src/composites/wui-qr-code/index.ts | 2379 | `8bd7990df0ecfd88957042724f26b9d8df0df5271602db1dc1ef7338e29802e8` | 0 |
| packages/ui/src/composites/wui-qr-code/styles.ts | 1272 | `528420f182dd0b772e7a37534adbf37b5ee4b0edd3eb14db00926bcac851f4af` | 0 |
| packages/ui/src/composites/wui-search-bar/index.ts | 1875 | `6654bacefd1af417dc15dfaf441dfb4e01ea8487fba9a91ab7149ff9ef24b0fc` | 0 |
| packages/ui/src/composites/wui-search-bar/styles.ts | 769 | `0ed6f071491737677db6cef33e1f9a7fa6064f4051b7c999d6d7df6a38e6c573` | 0 |
| packages/ui/src/composites/wui-select/index.ts | 2291 | `c3852c8d36c155c5a009032c580253a333059e5284aea17b93831f1feebccbf0` | 0 |
| packages/ui/src/composites/wui-select/styles.ts | 2486 | `85122904c28da0611971eb03ce62e5c6e407475d78ec621668f6f48bed63fb51` | 0 |
| packages/ui/src/composites/wui-semantic-chip/index.ts | 2219 | `054e359f7e221ee27b570b90b3d9d9aab32e9e70627986cbb872a3a29d157065` | 0 |
| packages/ui/src/composites/wui-semantic-chip/styles.ts | 3639 | `8a571cce6410eee46af3a7694e22da7cfd75013f369d1a98113257174b77934f` | 0 |
| packages/ui/src/composites/wui-snackbar/index.ts | 1716 | `2b91c8beb33d5b122b824465441b7c31fae0bd9e6efff8181967a5c2cc3812c0` | 0 |
| packages/ui/src/composites/wui-snackbar/styles.ts | 945 | `99c1c3b3289e78a0f6183715fe02586c9ab380a060687d5036ff749f84772bd7` | 0 |
| packages/ui/src/composites/wui-tab-item/index.ts | 1631 | `133a2bd99ee34157e2155c83dc42402dfc9c034a656c5aaa8b0df9fd666d0a03` | 0 |
| packages/ui/src/composites/wui-tab-item/styles.ts | 1122 | `a82fd0fac0c07c1ec282eb78a077d5e9422564a6198a1621d194c984f22ec9cd` | 0 |
| packages/ui/src/composites/wui-tabs/index.ts | 1604 | `977a652fd76dfff6634c605a5f4db9c8a81ff28cd15e97140382bacd065f13f8` | 0 |
| packages/ui/src/composites/wui-tabs/styles.ts | 456 | `5970f32aa63b4b67a81f3dd0ea1b8941f06efde36fc04b365c9bdbba92071062` | 0 |
| packages/ui/src/composites/wui-tag/index.ts | 1429 | `a60bf7c6877a5f95362a8b4d041d7f14c3dafa3d154d287c10f06d94b7d208a3` | 0 |
| packages/ui/src/composites/wui-tag/styles.ts | 1598 | `e9187868ca051095d43855612ecbdc0d0f85e55fd46a0c527e5003e20e0e1621` | 0 |
| packages/ui/src/composites/wui-toast-message/index.ts | 1641 | `36f35d4a3d3b11a5036b721ceb771876e03cfe19fc399e0599792dd76c3d2fcd` | 0 |
| packages/ui/src/composites/wui-toast-message/styles.ts | 1663 | `6d231766094025b02f4ce3eb3e6df351ab17866964cdeadb718d7cd73e626c24` | 0 |
| packages/ui/src/composites/wui-toggle/index.ts | 1679 | `033bd5d479f531e573008a1f15e1160771d772151f0f15b4d2733b65817892a5` | 0 |
| packages/ui/src/composites/wui-toggle/styles.ts | 5236 | `baed595376cd0b944651c1d83df147083c30dfb1a89bdbfcd17b813d4be6fd99` | 0 |
| packages/ui/src/composites/wui-token-button/index.ts | 2766 | `88b56ac546817267cc6c9703128e6653c82cfdfd8947ca896a0de1882a4cc847` | 0 |
| packages/ui/src/composites/wui-token-button/styles.ts | 2831 | `1354509389ddb8aeb492c3acef9639220c3261d7fa317944937fb113b35f89b4` | 0 |
| packages/ui/src/composites/wui-token-list-item/index.ts | 3498 | `2ea6b49e2a9bf5fd01f75d0c6da04b0a1f08370a7485489b953a5e1d1b70564d` | 0 |
| packages/ui/src/composites/wui-token-list-item/styles.ts | 2146 | `a8cd3a3c3e03aed3b24e43fccce628a8ff85c00492fbf3fe9b91a8eaf85e4693` | 0 |
| packages/ui/src/composites/wui-token-list-item-loader/index.ts | 1295 | `95f3408ce02c63c98f849ba5d96bfde6198ea2baf3b21a8a3d35f9e7af1cb8b8` | 0 |
| packages/ui/src/composites/wui-token-list-item-loader/styles.ts | 408 | `86200340215d1684ea73fc69802a1abdc45e6601fd702e810f51af72884a2289` | 0 |
| packages/ui/src/composites/wui-tooltip/index.ts | 1433 | `02d0f3a834c13f130507a0c6842cf6099913945ebba93ec0e7da051ac0e1420e` | 0 |
| packages/ui/src/composites/wui-tooltip/styles.ts | 1925 | `a2f345dec5398b523bb29aae25199c9fff7f31b592355338444c062835dfeb6f` | 0 |
| packages/ui/src/composites/wui-transaction-list-item/index.ts | 2900 | `0593eede4d3f908de039462e15a554bcf9d7f1a41eb50c604b07ba037ffba7dc` | 0 |
| packages/ui/src/composites/wui-transaction-list-item/styles.ts | 908 | `9dffd3ef9519829964f3ae4540c142ec172b3781ab244ccd9c38d8be4024c9bc` | 0 |
| packages/ui/src/composites/wui-transaction-list-item-loader/index.ts | 1249 | `78dd2c5ab0faf721799b8c9627379202f16faad28a4b0adc438cc13ceb4911c2` | 0 |
| packages/ui/src/composites/wui-transaction-list-item-loader/styles.ts | 266 | `46b30ee961edb19b93913ce66ff02ef8e7dc80b3d9349e43ee98032d6dcba63c` | 0 |
| packages/ui/src/composites/wui-transaction-thumbnail/index.ts | 3321 | `ac17d21a6d933c6945c2e6aa8c5000a08ac4e1fee4d7d2a9b8a95666686fb939` | 0 |
| packages/ui/src/composites/wui-transaction-thumbnail/styles.ts | 2416 | `e54f2e674b808d1919c9e5f21a725168713b64d9bbcb214e29e8a02d34e4c88b` | 0 |
| packages/ui/src/composites/wui-transaction-visual/index.ts | 5733 | `58e52768eb46ad77da8cab0b400f87f17d5e4267065006d4cabce27f94bfde02` | 0 |
| packages/ui/src/composites/wui-transaction-visual/styles.ts | 2166 | `bc6fbe6c340857c581445d221feb89c7296abd796c93a269fc4ab4dcd8cb0055` | 0 |
| packages/ui/src/composites/wui-ux-by-reown/index.ts | 1284 | `6aa3733fea3a5617c7c76e234539849f4ff71f909bb1aee00c6c1fe49133a2cd` | 0 |
| packages/ui/src/composites/wui-ux-by-reown/styles.ts | 266 | `ecefe21bd628e62642bd0e295b61ca62e01cdeefa646643be7b2ca6e7845b63b` | 0 |
| packages/ui/src/composites/wui-visual-thumbnail/index.ts | 1366 | `2e270bae18eb30ae42f9df4c608bd3d80dd3b56a5478e6d39ac2d4a5def5fab6` | 0 |
| packages/ui/src/composites/wui-visual-thumbnail/styles.ts | 467 | `45814db3a309085b9f66513ca537672859bb05bc0a9dd64743ede5f45bee6faa` | 0 |
| packages/ui/src/composites/wui-wallet-button/index.ts | 2588 | `1f94b7725f3656297bff44aeffc7398e1a258b7ba68a175d5cac42ecfed14465` | 0 |
| packages/ui/src/composites/wui-wallet-button/styles.ts | 2926 | `b68a6651c826f030a5ee22ae3077fab038255a3930339ab69036ad5fd086a5f1` | 0 |
| packages/ui/src/composites/wui-wallet-image/index.ts | 2247 | `2b9de18a16d2ada22a6a08a496c48b9c1d51fd05b52859989fe4cb12d9b77a36` | 0 |
| packages/ui/src/composites/wui-wallet-image/styles.ts | 1497 | `70bbcf6aeabccdc1739577185c07e263be18c4e1afd674e551483157e55ea087` | 0 |
| packages/ui/src/composites/wui-wallet-switch/index.ts | 2874 | `96151dcad1b42561ba08812ce172b473ffb52423db180758557d888a2bfea330` | 0 |
| packages/ui/src/composites/wui-wallet-switch/styles.ts | 1402 | `3298705f16b5fe53975477d0d75afbcc8aa21b83b1f717a4eb56e3d3a8cc79af` | 0 |
| packages/ui/src/layout/wui-flex/index.ts | 2783 | `c2b79c08d6d13ad7d40ce897ed0f93d8dd6f9bdedea5bbc6e42920836044a542` | 0 |
| packages/ui/src/layout/wui-flex/styles.ts | 151 | `321878b633d1dc9b2612aa79d1f3493c8080031f13d89a60ddf82c8b03bd0a28` | 0 |
| packages/ui/src/layout/wui-grid/index.ts | 2562 | `7b10a384af1083c7c45cb670a3eac081476898881bc3c153a202ceb87d4a085c` | 0 |
| packages/ui/src/layout/wui-grid/styles.ts | 123 | `f46e620019376d0185ada88867e5fa4e180f5c2e28e56c3612a34eda5b048bcc` | 0 |
| packages/ui/src/layout/wui-separator/index.ts | 1080 | `d65c5ba71c23ad46e2853dc945e564c206bb1b936d540c612c7b19166f96a996` | 0 |
| packages/ui/src/layout/wui-separator/styles.ts | 777 | `fcad0415655a82a42af023e8519de67dba3962c53b128af00d6de40488608d3e` | 0 |
| packages/ui/src/utils/CacheUtil.ts | 465 | `7ef58986de58835e0dc97fe88aca48ae7e8823d4b8e03e94d83061a0bf2ff2a0` | 0 |
| packages/ui/src/utils/ConstantsUtil.ts | 45 | `7765edce201ed71727ee00436ff79b179d7191a9807cfad34ac04a1f3d06e584` | 0 |
| packages/ui/src/utils/JSXTypeUtil.ts | 11406 | `c2aa1943975aaceca3a49c19d59b9b123f557225d14e36afb75dbfaff355d9d5` | 0 |
| packages/ui/src/utils/MathUtil.ts | 1022 | `606919e1f387e2a422860eaf81f242642807bd7d59164937fe52f159bf80dff6` | 0 |
| packages/ui/src/utils/QrCode.ts | 6230 | `0da92200fb8ed070f32517ee2413645e35a645b7826e7c018ae96f16d3bd218e` | 0 |
| packages/ui/src/utils/ThemeConstantsUtil.ts | 9591 | `71918b4b1f9cc2f318674bce0f6830c6fc57b51795e15828b116546281dbe363` | 0 |
| packages/ui/src/utils/ThemeHelperUtil.ts | 17970 | `3bf091d81ab4a61961a8bee4e942f50128fca6871c88286ed59e287775ed80c1` | 0 |
| packages/ui/src/utils/ThemeUtil.ts | 10763 | `10eb4febdee48f847bf7043fada14836e160eb876640d086a014636b70448ddf` | 0 |
| packages/ui/src/utils/TransactionUtil.ts | 9957 | `d2ddc15be33b668e58ad554bcfe8d78b7316e8f39c3a8fbaaed2f700cc009b8f` | 0 |
| packages/ui/src/utils/TypeUtil.ts | 8543 | `c4842b40a90984247d0d5a8da7e428d2a7182963784ee341934631a036ff4659` | 0 |
| packages/ui/src/utils/UiHelperUtil.ts | 5598 | `7aa6e7126671686a5c3efb39a5d0e16c3832933d350d85218dc95d0a6244d083` | 0 |
| packages/ui/src/utils/WebComponentsUtil.ts | 1542 | `94b5897a7d38e90dce532c2e35a43f36025b28de95f246a7a0849b8b9b0046d3` | 0 |
| packages/ui/vitest.config.ts | 80 | `edaa4113ae35e9507b5f1538604b5cc4120506d5631421e5068eeaadeec319d7` | 0 |
| packages/universal-connector/exports/index.ts | 228 | `f77298c736d99b10073cd679f0dd9ecbd15a6890d960b3ba3efb241989adf799` | 0 |
| packages/universal-connector/exports/react.tsx | 1882 | `ab9054cd23881a3bb8259492e4c90767cfcda0b5a4d22e4435c3c6228e266700` | 0 |
| packages/universal-connector/index.ts | 226 | `34e9bc5c02e0af2384b046a6f0f3eeda03a97f589ad63b15785f99853f91a869` | 0 |
| packages/universal-connector/package.json | 1817 | `887aace2fc9c5549bc8a3fa1098baf346456398beb496a26a41ac7299212d1ea` | 0 |
| packages/universal-connector/src/UniversalConnector.ts | 3267 | `6dfcd5c9dced02d7506f4982be274b1f954d88799c58a93ac252a5498985d7a3` | 0 |
| packages/universal-connector/vitest.config.ts | 80 | `edaa4113ae35e9507b5f1538604b5cc4120506d5631421e5068eeaadeec319d7` | 0 |
| packages/wallet/exports/index.ts | 547 | `8c2b81e65213af96c2894c27097996a4da944f6fe93d26ea08520b20ac62ce5b` | 0 |
| packages/wallet/exports/utils.ts | 141 | `e4f6173720a15f2f4182f23f54d8e0959278caad0a7714342067eea5cd249e7d` | 0 |
| packages/wallet/package.json | 1650 | `9f7cee56780d1ebab345f6242855cd1c4ef421c61bebf4819a44d146d3f582c9` | 0 |
| packages/wallet/src/RegexUtil.ts | 208 | `a45300db828128e6a648cc086baf405ba83af7bad54c07a08560c244f1f5753d` | 0 |
| packages/wallet/src/W3mFrame.ts | 8069 | `78849fcc76df891935db1744a9c3edb3925919ba55109be552a7924f2cf7e649` | 0 |
| packages/wallet/src/W3mFrameConstants.ts | 7894 | `11a6d7c161e2c3d3163f66ea9c272844edd48cfaccf454dbf410000a69e3e149` | 0 |
| packages/wallet/src/W3mFrameHelpers.ts | 1952 | `71d4027779e6850a8542113ba2a9307cb40497609830ed345915427774a8b4b2` | 0 |
| packages/wallet/src/W3mFrameLogger.ts | 1230 | `4962d732997186260650a00490ba42067afcc93893ebf248aa85f8a463abaf03` | 0 |
| packages/wallet/src/W3mFrameProvider.ts | 27324 | `ed68a154b258e9885863f8174839c094b13c252ac9a5f86ee71e1b94da90c9b1` | 0 |
| packages/wallet/src/W3mFrameSchema.ts | 23166 | `b345c4b5ef126fd39163a029c920f7902012603ef0abc03c0fb78f10a592f19a` | 0 |
| packages/wallet/src/W3mFrameStorage.ts | 714 | `94eabfb29d362fb79de55d944ee39dea106a7e89710cb4659a41967fdb163915` | 0 |
| packages/wallet/src/W3mFrameTypes.ts | 8597 | `6eb18b65d0121d5a27dd353b921e300b187360c46e87566e968fb4079409681d` | 0 |
| packages/wallet/vitest.config.ts | 120 | `27d27d7b59d34ecbbdcd94c545de62a0448e5b1385bafda59a561d6109aa8eba` | 0 |
| packages/wallet-button/exports/index.ts | 728 | `7b7472e3b2ae42e9ba38446967ae06c916cb8d68d465e4fdcf16a96879bc811f` | 0 |
| packages/wallet-button/exports/react.ts | 6956 | `2a2323875bfefd6c1f4329628d839aa0df975bd827f7ab71725dd6fe22368f7d` | 0 |
| packages/wallet-button/package.json | 2129 | `624eef588bc65b23ede213b3a0b9a32b8529914097292875ec23ee8fdd4803c1` | 0 |
| packages/wallet-button/src/client.ts | 3238 | `545af5cbd96902a27075bb5deecb7e2bd61a40697df4b4562ac8ddac5e84029f` | 0 |
| packages/wallet-button/src/controllers/ApiController.ts | 1741 | `707a4bd12a97dde49dd043dc975d0111712f5bf9a2b632051c151b151bc027e6` | 0 |
| packages/wallet-button/src/controllers/WalletButtonController.ts | 803 | `be90725ae5f2465e3b009731483850baebe01d0a9c1295c2ae58cb721c6087f8` | 0 |
| packages/wallet-button/src/scaffold-ui/appkit-wallet-button/index.ts | 8272 | `21e43dfbd66c9c6319b89410c4a752682156738e9e319c0e427ce91573ee9a14` | 0 |
| packages/wallet-button/src/utils/ConstantsUtil.ts | 4074 | `1fc582cb369ecbcd9e4e22768a8e1dc7d71cb4f701f5850638d533905300adb5` | 0 |
| packages/wallet-button/src/utils/TypeUtil.ts | 245 | `7ab70fd6ea7fca8c702ad71c5ba236851c47a440a8c6e01fd5771981d33dee59` | 0 |
| packages/wallet-button/src/utils/WalletUtil.ts | 649 | `263896ec3e53de2334ef8500c0f72a5794ca3dff3d08adebc1a2f9da1aaeb452` | 0 |
| packages/wallet-button/vitest.config.ts | 120 | `27d27d7b59d34ecbbdcd94c545de62a0448e5b1385bafda59a561d6109aa8eba` | 0 |
| pnpm-lock.yaml | 1849447 | `84bda5cf03d66c4d94de879ca1ce5a9c18b829acdc1c9f687acaca2e1b3ebf08` | 0 |
| scripts/inject-version.js | 1122 | `fe63757d40fdbbe95590c6c9a9ce187f399bf5985dd49c37d6ae5c1a62999270` | 0 |
| scripts/update-dependencies.ts | 7783 | `2046a55e416f9972e744ab27c1043ad1b492c941d5591eb23a6181557a251a6e` | 0 |
| services/id-allocation-service/package.json | 328 | `30c44d816ad763272af629456e54542a0e708ab6c5e2c088f42991cca329386b` | 0 |
| services/id-allocation-service/src/index.ts | 1013 | `75002431ea9e45152ebf2f97943b380cce3072350921a55e1142f6b064f6f4fe` | 0 |
| vite.config.ts | 256 | `facb03cb1eac7fb171f00ec628482a009e15ba4bcf2c095d241fab19700caefc` | 0 |
| vitest.config.ts | 137 | `6fe09e2e0ea61002e4d78595dddebbbc0f23d975d52cf2cd675d3cabcffb5cb6` | 0 |
| vitest.workspace.ts | 159 | `972f7bc1017555e2a5c6f8a2e260b4f5145febea1c6acd3eefd0c650a5543172` | 0 |
