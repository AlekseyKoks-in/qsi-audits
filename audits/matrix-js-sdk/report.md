# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** matrix-js-sdk @ 61b08bd037a3 · Matrix.org Foundation — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-28 18:22 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 259476ec-cff6-4f97-af62-52170c902315 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Разработчик ПО безопасности |
| SHA-256 содержимого | `6b99f797316754f231b4b06db6d193f9d0893a7f657f49253d76cbd060ebaeb3` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **2**
- Средняя: **1**
- Низкая: **1**
- Информационная: **1**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 3
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 1
- Рекомендация по улучшению: 1
- Недостаточность данных: 0

Неравенство Моски (x + y > z): x = 10, y = 3, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/matrix-org/matrix-js-sdk> @ `61b08bd037a3b987f267e2e8ac47002c75d59d85` — ссылки в доказательствах открывают строки на этом коммите.

240 файлов, всего 3159398 байт, редактирований: 2; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 238 | babel.config.cjs: 33 lines scanned with 16 rule patterns and 122 registry patterns; knip.ts: 45 lines scanned with 16 rule patterns and 122 registry patterns; scripts/changelog_head.py: 18 lines scanned with 16 rule patterns and 122 registry patterns |
| dependencies | проверено | 2 | package.json: 49 dependencies parsed (3 pinned); pnpm-lock.yaml: 487 dependencies parsed (487 pinned) |
| secrets | проверено | 2 | src/interactive-auth.ts: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); src/logger.ts: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| osv_advisories | проверено | 1 | 487 pinned packages queried at OSV.dev; 3 affected (1 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree matrix-js-sdk at 61b08bd037a3b987f267e2e8ac47002c75d59d85. 240 files analysed; of 489 files, 196 are test, fuzzing, benchmark or example code and were left out, 53 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **74** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 16.7%

## 7. Подробное описание находок

### QSI-2026-05835 — markdown-it 14.3.2 затронут GHSA-gfr2-rv44-r23c (CVE-2026-111758)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/markdown-it@14.3.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:22 UTC
- Балл приоритета: 37.7 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-gfr2-rv44-r23c (CVE-2026-111758) для пакета npm markdown-it версии 14.3.2: markdown-it: Quadratic-time rendering of a single multi-line link reference definition with default options (regression since 14.0). Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-gfr2-rv44-r23c
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-gfr2-rv44-r23c](https://osv.dev/vulnerability/GHSA-gfr2-rv44-r23c) · manifest · SHA-256 b0f56e1087570043d40ebe490125d4879ff93876350edee5858cf5249d19c659_

```
{"id": "GHSA-gfr2-rv44-r23c", "aliases": ["CVE-2026-111758"], "modified": "2026-10-20T20:45:05.953469039Z", "summary": "markdown-it: Quadratic-time rendering of a single multi-line link reference definition with default options (regression since 14.0)", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (14.3.3, 15.0.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05837 — zod 4.6.5 затронут GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/zod@4.6.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:22 UTC
- Балл приоритета: 37.7 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404) для пакета npm zod версии 4.6.5: Zod can exhaust memory while validating oversized constrained collections. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mrhx-c7xc-m3w5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mrhx-c7xc-m3w5](https://osv.dev/vulnerability/GHSA-mrhx-c7xc-m3w5) · manifest · SHA-256 a49e02cfde3c6444146081879a6e65025dde29e8aca8c1e27449299070b2de78_

```
{"id": "GHSA-mrhx-c7xc-m3w5", "aliases": ["CVE-2023-54404"], "modified": "2026-10-23T18:30:09.376405885Z", "summary": "Zod can exhaust memory while validating oversized constrained collections", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.6.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05834 — Квантово-уязвимый ECDH: обмен ключами в канале (TLS, Noise, рукопожатия) (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDH:channel`
- Источник данных: src/rendezvous/channels/MSC4108SecureChannel.ts
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:22 UTC
- Балл приоритета: 36.7 / 100
- CVSS v3.1: неприменимо

2 упоминаний ECDH в 1 файл(ах), например src/rendezvous/channels/MSC4108SecureChannel.ts:109. Роль по путям, именам функций и соседнему коду: обмен ключами в канале (TLS, Noise, рукопожатия). Трафик под этим обменом ключами можно записать сейчас и расшифровать позже; гибридный обмен сохраняет классические гарантии и добавляет постквантовые.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/rendezvous/channels/MSC4108SecureChannel.ts:109 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/rendezvous/channels/MSC4108SecureChannel.ts](https://github.com/matrix-org/matrix-js-sdk/blob/61b08bd037a3b987f267e2e8ac47002c75d59d85/src/rendezvous/channels/MSC4108SecureChannel.ts#L109) · line 109 · SHA-256 6b0afe39c4b8782fe2c057524dbf28e4c5d12981ba44c92d874936f156a63ec7_

```
  108 |              Nonce := 0
  109 |              SH := ECDH(Ss, Gp)
  110 |              EncKey := HKDF_SHA256(SH, "MATRIX_QR_CODE_LOGIN|" || Gp || "|" || Sp, 0, 32)
```

_file_excerpt · [src/rendezvous/channels/MSC4108SecureChannel.ts](https://github.com/matrix-org/matrix-js-sdk/blob/61b08bd037a3b987f267e2e8ac47002c75d59d85/src/rendezvous/channels/MSC4108SecureChannel.ts#L158) · line 158 · SHA-256 66f212ef044f2d1d30441468f096f6c543825f8fb6cd4691236b10021cebfe58_

```
  157 |             (TaggedCiphertext, Sp) := Unpack(LoginInitiateMessage)
  158 |             SH := ECDH(Gs, Sp)
  159 |             EncKey := HKDF_SHA256(SH, "MATRIX_QR_CODE_LOGIN|" || Gp || "|" || Sp, 0, 32)
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Переведите рукопожатие на гибридный обмен ключами (X25519MLKEM768 в TLS 1.3; гибридный KEM в протоколах на основе Noise).

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05836 — markdown-it 14.3.2 затронут GHSA-vfgh-jcmw-g37q (CVE-2026-111766)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/markdown-it@14.3.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:22 UTC
- Балл приоритета: 29.5 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-vfgh-jcmw-g37q (CVE-2026-111766) для пакета npm markdown-it версии 14.3.2: markdown-it: Quadratic-time denial of service in inline HTML parsing with html enabled. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vfgh-jcmw-g37q
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vfgh-jcmw-g37q](https://osv.dev/vulnerability/GHSA-vfgh-jcmw-g37q) · manifest · SHA-256 beb06991ca4608c3fb72076c861f838df0f3ab50c9407b3e6769fc5e7ad6c3e4_

```
{"id": "GHSA-vfgh-jcmw-g37q", "aliases": ["CVE-2026-111766"], "modified": "2026-10-20T20:15:05.220039200Z", "summary": "markdown-it: Quadratic-time denial of service in inline HTML parsing with html enabled", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (14.3.3, 15.0.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05838 — 1 бюллетеней в 1 пакет(ах) npm, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:npm:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:22 UTC
- Балл приоритета: 15.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 1 бюллетеней (1 с оценкой high или critical) для 1 пакет(ов) npm, которые подтягивают только инструменты разработки или сборки (pnpm-lock.yaml): например, happy-dom@21.0.3 [dev]: GHSA-834v-8h66-3h79. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в pnpm-lock.yaml.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · pnpm-lock.yaml · SHA-256 740af9fc707d62bb061ed54085924e55fa634b368786e710aa6e924e366f8307_

```
happy-dom@21.0.3 [dev]: GHSA-834v-8h66-3h79
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.


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

- Только классика — обмен ключами в канале (TLS, Noise, рукопожатия): ECDH (1 файл(ов))

**Следующий шаг:** Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **обмен ключами в канале (TLS, Noise, рукопожатия)** | ECDH (1) | QSI-2026-05834 | Переведите рукопожатие на гибридный обмен ключами (X25519MLKEM768 в TLS 1.3; гибридный KEM в протоколах на основе Noise) |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | ECDH (1) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | HKDF (1), HMAC (3), PBKDF2 (1) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-05835 | Обновите markdown-it до исправленной версии (14.3.3, 15.0.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-gfr2-rv44-r23c (CVE-2026-111758). |
| P2 | QSI-2026-05837 | Обновите zod до исправленной версии (4.6.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mrhx-c7xc-m3w5 (CVE-2023-54404). |
| P2 | QSI-2026-05836 | Обновите markdown-it до исправленной версии (14.3.3, 15.0.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vfgh-jcmw-g37q (CVE-2026-111766). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-05834 | Внесите использования ECDH в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-05834 | Запланируйте миграцию ECDH на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-05838 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |

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
2. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
3. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
4. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
5. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
6. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
7. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
8. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
9. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
10. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
11. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
12. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
13. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
14. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
15. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
16. OSV advisory GHSA-gfr2-rv44-r23c — OSV.dev. <https://osv.dev/vulnerability/GHSA-gfr2-rv44-r23c> (modified 2026-10-20T20:45:05.953469039Z)
17. OSV advisory GHSA-mrhx-c7xc-m3w5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-mrhx-c7xc-m3w5> (modified 2026-10-23T18:30:09.376405885Z)
18. OSV advisory GHSA-vfgh-jcmw-g37q — OSV.dev. <https://osv.dev/vulnerability/GHSA-vfgh-jcmw-g37q> (modified 2026-10-20T20:15:05.220039200Z)
19. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
20. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
21. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
22. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Расположение | Квантовый статус | Классический статус |
|---|---|---|---|---|---|
| HKDF |  |  | src/utils/internal/deriveKeys.ts:29 | сниженный запас (Гровер), одобрен | допустимо |
| HMAC |  |  | src/utils/decryptAESSecretStorageItem.ts:39 | сниженный запас (Гровер), одобрен | допустимо |
| HMAC |  |  | src/utils/encryptAESSecretStorageItem.ts:66 | сниженный запас (Гровер), одобрен | допустимо |
| HMAC |  |  | src/utils/internal/deriveKeys.ts:54 | сниженный запас (Гровер), одобрен | допустимо |
| PBKDF2 |  |  | src/crypto-api/key-passphrase.ts:41 | сниженный запас (Гровер), одобрен | допустимо |
| ECDH |  |  | src/rendezvous/channels/MSC4108SecureChannel.ts:109 | уязвим (Шор) | допустимо |

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| babel.config.cjs | 838 | `d8487617a57ed6e8f76916f79b2ac697ce565aace57c6e4cf4798a8ae966be89` | 0 |
| knip.ts | 1496 | `1c88e8e97b0b64ea37ee3a1cbb245d2596b4371c28c2652202bb1b1f1c5632b5` | 0 |
| package.json | 3986 | `8ae6857538fa3eab294a871bd8ac2416c5b75f17aa23152a56221ae7bee80f45` | 0 |
| pnpm-lock.yaml | 169329 | `fa7755cd81af319523d2b6e2c565d4db3aa3e47b9706d1b0fc93aff829e56b21` | 0 |
| scripts/changelog_head.py | 396 | `213633aabe6b0ecd0b41661926bbb92562a70bb5f2f21d4408461a6c08af42c6` | 0 |
| scripts/release/merge-release-notes.cjs | 5718 | `e88315a38e05813c79a9f1ba8aadde595815524dd961baba4fda58ba7e507585` | 0 |
| src/@types/AESEncryptedSecretStoragePayload.ts | 1020 | `20510dba8ceb6f5b4c0fa3e4b348c00a85a65a4b5ac920e2b4eed81d8b78ef95` | 0 |
| src/@types/IIdentityServerProvider.ts | 846 | `39910b15ca704703fe5389ab6011d23c249539ef81b71ded3ae002298294523a` | 0 |
| src/@types/PushRules.ts | 6806 | `3ff431925e7fcfb9d8b117af81136a4b58cb3d8635045b58fddd95257b5e61c7` | 0 |
| src/@types/another-json.d.ts | 664 | `bcb997cdd9864124ca69331883aad3bdc4895b331aa91f8c1f987449cce87efb` | 0 |
| src/@types/auth.ts | 7952 | `effa5bfaf6e950c1460b1df65d01d174e42cf744635322ee097df103502e67c2` | 0 |
| src/@types/beacon.ts | 4488 | `948b55f6dd4dbc7d97741d9324b25d212dd6479494b8db35338dee4138f30c8d` | 0 |
| src/@types/common.ts | 968 | `cadb03da235959cbfb07724ee89c2376fed46020f31454279aaed3325a68be5b` | 0 |
| src/@types/crypto.ts | 2242 | `1662efde2e5664a155a59e98d7baeafb21ca48e506101e208dde144879da1f96` | 0 |
| src/@types/event.ts | 18605 | `a59aed0213e99e7090ab404ae748d3258cb75c14a847363f37d89546de9d624a` | 0 |
| src/@types/events.ts | 3452 | `ae9a96475201d45afde8ea1af4764613b477da8221f604066de57b615d14d204` | 0 |
| src/@types/extensible_events.ts | 4482 | `0fe97d0c836327a0dbb9e5fe88570f4de20f3a08adc9ca6e91f6c61415c80c2c` | 0 |
| src/@types/global.d.ts | 2591 | `354a8b07308d5b357cbdc1b1ccf9df79c6dc87e3e028eb1df522e4c314187c38` | 0 |
| src/@types/json.ts | 1020 | `7b5b40c9afd5ee029af5f4b1e8021da72f96be836d96944eee6c8274747d854b` | 0 |
| src/@types/local_notifications.ts | 653 | `b9c6ca061ec461e72548e1ddabb1cb23bd60dad5b5093e90fdab4380fa26618f` | 0 |
| src/@types/location.ts | 3093 | `34940336609eef50853f24331ea594c4cd19eee78430540a2120d0202b2465c8` | 0 |
| src/@types/matrix-sdk-crypto-wasm.d.ts | 1247 | `ca107d72268a8bedfb6a48ef46e976ac0bd3325d4b58f97e4a341737acfdeb29` | 0 |
| src/@types/media.ts | 6625 | `caa697aceb489de1b42bbe7f7f3a27732b2482b5fc582c7de925ee3012c291b8` | 0 |
| src/@types/membership.ts | 1963 | `4bcb367817978b17d16993b7f7d9b3de1c66dab8e22f6f6e14c78fa6befec62f` | 0 |
| src/@types/partials.ts | 2930 | `0462b5311be09a1b538f2d219ba9009adca0888d25edae3d9ccfccac38f578a7` | 0 |
| src/@types/polls.ts | 3497 | `ef73efd29ce7875b31041543420be7859f2cc1b8a53f4e575ecd9bf8729e08d2` | 0 |
| src/@types/read_receipts.ts | 1641 | `09edb9131e7b138fe4fd64efd10928a65db127dbd2e3c19d32412db7fc7e340c` | 0 |
| src/@types/registration.ts | 3808 | `6e884107390fbb0e175895443eb861d6a1f2c7bf73be82fa721da7a5b54f6b54` | 0 |
| src/@types/requests.ts | 9798 | `37f93e9be6b1d34a910556b98f6f1fea94acb42a332e910e7ab5bd6f7c9a277b` | 0 |
| src/@types/retention.ts | 479 | `a0af5b6d61f44494aae8315608fe8b23c3047448498969dd354dbe91daf63f31` | 0 |
| src/@types/search.ts | 2984 | `93633a66a7172469c832320700620ff3d808a59451886a399e8e7a5c4b3cb54b` | 0 |
| src/@types/signed.ts | 737 | `71cceb07439f89b166f88e60e056f8afd5cd1f32bf745ddcbb4db6686e797ba3` | 0 |
| src/@types/spaces.ts | 1145 | `6f68c7edf5e135f59bea777f27fe1f125a6d96854fea5b9e410281888a763798` | 0 |
| src/@types/state_events.ts | 3874 | `33ecbcb7b9e8546c0d670e4dcb0aeb3291f0edd5f4838b3631a9819ada9bced8` | 0 |
| src/@types/synapse.ts | 1144 | `8458b4597eb9f6a788a130ea558014910cb8260c9a8a5abb894519bf509a665a` | 0 |
| src/@types/sync.ts | 908 | `d7436c88c3df472ce8b9eece06c8b1448d65a67a2bdd8ff8d5c45008b0005813` | 0 |
| src/@types/threepids.ts | 875 | `7e5254649443769e67e13d456d199f1bb8c9ce0e261ec092b08388f0eb58b0ec` | 0 |
| src/@types/topic.ts | 2060 | `57c2040dde964caf0796016e2ceda1cf2f97845cdb06a6e6ffb933325bb52482` | 0 |
| src/@types/type-guards.ts | 4261 | `655dccaf0c7ab81d815a838579e0bdbc62e2abf35a9a37006d2e9da4550f356a` | 0 |
| src/@types/uia.ts | 776 | `48bce6f2ee9a86af6f106a5e6d2292b19888e7ed44d33fd6f039daee869b5a88` | 0 |
| src/NamespacedValue.ts | 3866 | `1c5448e4432b8ea80e6bf99bca08a190818f35f77c42254a14954335414e3d75` | 0 |
| src/ReEmitter.ts | 4189 | `d7fa5703fe86b04ea36a111ae42acdd200db5dc5c0a4f218be1204d17bd02868` | 0 |
| src/ToDeviceMessageQueue.ts | 5877 | `38dff9d72492dbbc020072e7f023bd148266fdc855b5c49022cce9ea718f3403` | 0 |
| src/autodiscovery.ts | 21527 | `9efb22539c918c0ddf852256df7066359f13afc2f074ad2817330aa2bf1e45ad` | 0 |
| src/base64.ts | 3254 | `c2a93ebbe5eece1cd11cf596fbd068ae441320facfe076860614be6337903000` | 0 |
| src/browser-index.ts | 1349 | `27a292283dd8afe1ab2aa229f0a663cb5664aaa30f0990dede77d678091b499c` | 0 |
| src/capabilityPoller.ts | 3587 | `6614aa776dc1a08d5d29149036dd1b6bf83ba7470d9533326ed90d5b3f81b93a` | 0 |
| src/client.ts | 367565 | `800d9d53d093e2ab714c52ce7d1f6cfe297ba2aae7e988a27f7b3b3fece07d19` | 0 |
| src/common-crypto/CryptoBackend.ts | 12906 | `761d044db45fbcfcded2dc7c17dd45436f940c63c34d953a7c0505227f24ff97` | 0 |
| src/common-crypto/key-passphrase.ts | 1666 | `0497286a5c2b87322efe2277542da41397a693bf427943ed23df847fc2d4ba61` | 0 |
| src/content-helpers.ts | 9767 | `b76aee41c31f897738340b506b96144f814bdf959d165c4e2c7df92858a979d7` | 0 |
| src/content-repo.ts | 4753 | `23335245613a79a43c5c6ab4c734e9f542d98ae11a8d404803ee7fcd6f20e7dc` | 0 |
| src/crypto/store/base.ts | 11763 | `25a3357b33b9882138ccdd2fc657c797de6c3692f112e597e9cd30a23869bd3b` | 0 |
| src/crypto/store/indexeddb-crypto-store-backend.ts | 23284 | `6588d87733a9338da870a0368164a83bba038a26583862202069b75993c8eb2f` | 0 |
| src/crypto/store/indexeddb-crypto-store.ts | 21319 | `b8522f1c25d9facd08ca9eb51172eb7bf1a87bbf459e756de5c0a949b76adf1d` | 0 |
| src/crypto/store/localStorage-crypto-store.ts | 14334 | `e94d62c588e95676802531dfbc29d9daef13dbb252250019006e333060e90c1c` | 0 |
| src/crypto/store/memory-crypto-store.ts | 10567 | `1076fa25d42978d7679b82f97541d3e9fbd8fb18850a8c38a7aef3887c216522` | 0 |
| src/crypto-api/CryptoEvent.ts | 6111 | `fa30bfb3616d19f67f5c020a1cad02970159a45c88594df4a6611fac1e9ddcb5` | 0 |
| src/crypto-api/CryptoEventHandlerMap.ts | 2172 | `7f7afc73296aa48175bbf40d8db645aaa3faad969eeaa095a8328dcb81999121` | 0 |
| src/crypto-api/index.ts | 57450 | `81d909f45999be8257af79de4726eafc0a4f995d7acfa852a7ad7878c9b3e51e` | 0 |
| src/crypto-api/key-passphrase.ts | 1879 | `a1bf4b485d1b360ec6f84d003cad7a471a4a67964160b11463179765367fe645` | 0 |
| src/crypto-api/keybackup.ts | 3483 | `dde2c150bdedea6659a64a23c79a56bc2b3a9282f502165feeb392c3b46be6a2` | 0 |
| src/crypto-api/recovery-key.ts | 2459 | `f4e4b9d8362eb8df77da57953482e0241186a9a66a359bdf88281944757a2ca1` | 0 |
| src/crypto-api/verification.ts | 14929 | `2b23f38b315c32b57339ec46b09b8648aadc2d5d894421ae508a5f9c7007637e` | 0 |
| src/digest.ts | 1329 | `244e0b9d539bf1f18349b6a616d31c677bdfb2d8b0fa63cb38ab2833fddbccdb` | 0 |
| src/embedded.ts | 43095 | `146f21cacab40a49b8ddcb5f280e4b88b1c665d5841174a44de234c3e34f2b76` | 0 |
| src/errors.ts | 2729 | `63e21fd48f51cf763d5f3f8cbf64fd113a171be3ecb6f0cf6ba844ed4b89a50a` | 0 |
| src/event-mapper.ts | 3800 | `58c8cbdff06bae6db3c93843e92176d92b22be27dab558a70b3239c8bb047d9b` | 0 |
| src/extensible_events_v1/ExtensibleEvent.ts | 2179 | `f9bbea5242e6b31b0353851c0baf0f6dcf3584dbccfbfe2fcfa7f6a2a2cbcccc` | 0 |
| src/extensible_events_v1/InvalidEventError.ts | 768 | `cced0ac4b3ab82b4a68f9bd97da729e545a6256f27d0e1d43371e0de4b28eb86` | 0 |
| src/extensible_events_v1/MessageEvent.ts | 5084 | `f6e929502c7d0da0a4a3f29694a577a62ded7ed680f0ce3232c9b410c78d814b` | 0 |
| src/extensible_events_v1/PollEndEvent.ts | 3275 | `0e9c4467aedaa65721a6c9857c2605e563d9fb9c3c3b882b7b883d7ba4cc51be` | 0 |
| src/extensible_events_v1/PollResponseEvent.ts | 5056 | `31f0b3d3a42d1bc8d3107aa567d1eb58b52010e39916f0476c5f449b02474d93` | 0 |
| src/extensible_events_v1/PollStartEvent.ts | 6945 | `c92eb6dc3927e0a1698c69c9553ced92866d4842512b39b608e261f13e706376` | 0 |
| src/extensible_events_v1/utilities.ts | 1162 | `2092972fe8de9be061f3f9b0c02f9b3d19a7acd73cfbca3c1054039ff8e489d3` | 0 |
| src/feature.ts | 2996 | `2e24b41c7451fc7c4ec9b4f6fd760c35bcec2bcf9dac04d5b1d84f4e14bdbdde` | 0 |
| src/filter-component.ts | 8063 | `00f05c2de44b03dc220bf59c1f7bf2667407abfba17382fab771602e104dcfae` | 0 |
| src/filter.ts | 9092 | `dd80a302fdcffabce87ac316dfa3beb629c5f98cd9123bea21af93841565e4c2` | 0 |
| src/http-api/errors.ts | 9914 | `5270b7eff25eabf044e9e07985658e6657819326c5845454f9fc4b4fe3728a54` | 0 |
| src/http-api/fetch.ts | 14063 | `3d7ae9021672e214486b011644dd51a7750004c37ac9ccfd1d2ffc4a00e6b2a1` | 0 |
| src/http-api/index.ts | 6933 | `0a64857990faf90f5982a749c8dfd6221fc78dc7004ddcc7edf08a22b9860871` | 0 |
| src/http-api/interface.ts | 8530 | `43698eff8415956711c001dbf2b787847e9b1461d85a80edfbd994f6c4b9316b` | 0 |
| src/http-api/logging.ts | 1634 | `b99dd7591f264a2c8c438d780b5a500bc7334f5335cd124d64a90886766e0707` | 0 |
| src/http-api/method.ts | 744 | `ea8f9e89d2efb1bb6192f224d42016349a1d3f61d68862975ef9a394f19cfcfa` | 0 |
| src/http-api/prefix.ts | 1480 | `66b5a853cf17b7f855037bcc32ac329e1aa296e417a8eba5611153983657c775` | 0 |
| src/http-api/refresh.ts | 11981 | `395da66d8f54d75958acb25342dabe03c3b2afcddc24aa7b4c2f777e3dc37f84` | 0 |
| src/http-api/utils.ts | 7120 | `e1c0540813071a798f3e97ee8c12776a661d2512a70ef08ee9d282958217c201` | 0 |
| src/index.ts | 825 | `a3aa4efcb1b97f77a506e7658562d37623b082b478fc9285129361db15afc215` | 0 |
| src/indexeddb-helpers.ts | 2051 | `12d3639b721c26c152998f13c68eca81f3d008c8e68b44b7a98680d7cfe7b3ec` | 0 |
| src/indexeddb-worker.ts | 844 | `a1960982fc087aa2614cf37ec6747982b905ea826acff12e9b975ac643c3bf49` | 0 |
| src/interactive-auth.ts | 27333 | `7006d8316421c79e7433913c72ff3985d1cb23baa1509d6b825064913bdeb3a7` | 1 |
| src/logger.ts | 9396 | `bcb5d9c019239d881e1f395d953e5e29595606f78d96f93b7d031f04057ef72e` | 1 |
| src/matrix.ts | 7402 | `b9042cdc15ad1b12d7ebd0e99cab15237b3ff3b9dee207ddeea72c1e31e2c114` | 0 |
| src/matrixrtc/CallMembership.ts | 18412 | `972414c3a8cd1454602b22b94baf573ef4c6e845e9f1e39c8464ede58f260f85` | 0 |
| src/matrixrtc/EncryptionManager.ts | 2217 | `2ccc57e6c7b597c0ea00de7c0ffd2ee10fc4b432c4572d7ca951fc871837fd9c` | 0 |
| src/matrixrtc/IKeyTransport.ts | 2344 | `a1c72008ca532a3a8774c4d65e71b81b3ac7bbd3d2fbb6828a90090a6e23533f` | 0 |
| src/matrixrtc/IMembershipManager.ts | 4752 | `5729e6fe9bddf142ec97f38bdb6c01b56fcfde01fcee88ef98b199c44ad4fabd` | 0 |
| src/matrixrtc/LivekitTransport.ts | 6796 | `d77dc18e9d6507a6bb2f562969429c0b82911e6d73fe569fb5507c700f4fb071` | 0 |
| src/matrixrtc/MatrixRTCSession.ts | 44404 | `afa1b8a5fc8e2cb674dcb81f23fa39a88c75c72c893ed1564ed631cd1f1314ea` | 0 |
| src/matrixrtc/MatrixRTCSessionManager.ts | 8056 | `3bfe402da2c23d7ff3f66083613ad7b980396b62fc731c432f28b32a80d43b58` | 0 |
| src/matrixrtc/MembershipManager.ts | 70530 | `5d9bdd3f6870aafd9823890110bb915afe648728450312162ef028fb5b1dd935` | 0 |
| src/matrixrtc/MembershipManagerActionScheduler.ts | 5838 | `3a4ef26cc897253e2498bb593d008485ee5aa98f33793660f892003f13ae9628` | 0 |
| src/matrixrtc/RTCEncryptionManager.ts | 23203 | `4833a51c3359a55a0d536c6b2da0a4f538af21625ccaff4315f0d7ea785f6434` | 0 |
| src/matrixrtc/ToDeviceKeyTransport.ts | 8527 | `295cbe9859623de1625dc88a2ad189848b1f998b9cb00a75d2868dd83588dd79` | 0 |
| src/matrixrtc/index.ts | 1170 | `a8a1509f9bf9c1bd765f5739b34b36971b8a0db574a2ad8d071d0e1db3a76a38` | 0 |
| src/matrixrtc/membershipData/common.ts | 1589 | `ad1bb426add45bf9141b5d5c1fbac16027d3f63174fe7e44a370b6fa209904aa` | 0 |
| src/matrixrtc/membershipData/index.ts | 927 | `f7cdca646ee94a839a4b52888b1c5e85083fee432b4578836cd04460e2ad12d8` | 0 |
| src/matrixrtc/membershipData/rtc.ts | 7523 | `7afd5aaa0a32207bd9c45c2b2e5bc88f2ef739dd68926a1bc202c27ce0c922e4` | 0 |
| src/matrixrtc/membershipData/session.ts | 6096 | `ccb0c9ea9dc963913932fd8db688e3294d6759a393a8adefc87cd43094c7e36d` | 0 |
| src/matrixrtc/types.ts | 23653 | `cdd5f60cc80fec04e320a154557f4153909f9fbc393332cbb82384607437d48b` | 0 |
| src/matrixrtc/utils.ts | 4521 | `3e4a831d70244139c3f23425f86e4781e80226e75d387155a68b012bdda308da` | 0 |
| src/models/MSC3089Branch.ts | 9116 | `4074d38b089d1cd6c0cac673309574726d2e0660d5f268d5eae2e5337d7f9f3b` | 0 |
| src/models/MSC3089TreeSpace.ts | 21966 | `b2601d996f1a6d2f85a8b55001cdda3d57eb79a240f1602ad5c99df668af0852` | 0 |
| src/models/ToDeviceMessage.ts | 1054 | `354dbded9593d4ddd47d114f9bfa77b2c66e1f8bb6a01fb7ee0cf4e8ce7f7069` | 0 |
| src/models/beacon.ts | 7912 | `3693974c1df9a8dae9b53cd6f09c8fcec2ecf05aac634a35fdcc0458022ae454` | 0 |
| src/models/compare-event-ordering.ts | 5231 | `481e38e6586a51747ca320c38fb40c1e30fe0b17d56a5feb04272ff9760b7dd1` | 0 |
| src/models/device.ts | 2810 | `18ac35d9b9f2dcd6d648a9404ad02bcea23208ff92ae98c10187183c496e3d8d` | 0 |
| src/models/event-context.ts | 3426 | `16a58be3f94bf5cc98500bf75899a70c13e1243e8ccedd1f203107aad28cb312` | 0 |
| src/models/event-status.ts | 1196 | `b078fba2106c6124a93ff4940c6806af1571583a66a438e244ab558d7a1e7320` | 0 |
| src/models/event-timeline-set.ts | 38025 | `ae6d2dcaac213ffaab4479ede9412726fc2281486feb0291d0f8790679d9628b` | 0 |
| src/models/event-timeline.ts | 17804 | `c1a81a590b53e4338746e71be48486096a9cf6c61c6b2f5281b0ac4529d2461b` | 0 |
| src/models/event.ts | 65156 | `728e50cacb7cef2035718356be17450366201eae16b3ce3cf2513a957157d1b5` | 0 |
| src/models/invites-ignorer-types.ts | 1676 | `65c3454002fea8a39b04ba32ff8e45c1666ef05a6560b76469f528510482585d` | 0 |
| src/models/invites-ignorer.ts | 13110 | `81da95c6882d1861fb8fa5f679133496a113387ec3b5f9994a70316266a0ec65` | 0 |
| src/models/poll.ts | 9618 | `cc8a4d9c6f6c6c41c06a18b69d27e855ec163119c24f8ace9bf45f3c597b0832` | 0 |
| src/models/profile-keys.ts | 1238 | `f674468cd75106ca4b9806d1a439461116807fd9ab8e3c4830e43c0342259a33` | 0 |
| src/models/read-receipt.ts | 17755 | `be5ae6a6eb646d0fde186633b286b08894ade58f1560c84679707b725680e892` | 0 |
| src/models/related-relations.ts | 1437 | `585cdea6d03094f09b68d9b02364d51e473cfa03a33a6bc6b00306a14b8630e1` | 0 |
| src/models/relations-container.ts | 7959 | `b4a93146ae6f76eb0b377711a11a4e59e49ffdebaf53b890c9b013ef6d86adb0` | 0 |
| src/models/relations.ts | 14652 | `1d97cacb6ff9599a77c0b5f118b63aeae75dc212cfa02707bcdfd345aa90fd9a` | 0 |
| src/models/room-member.ts | 18099 | `3661c90c98f93e4adb5faa9149c4bb57218acfa46f2a2f2b07a29d917488ac0c` | 0 |
| src/models/room-receipts.ts | 17020 | `da78d7ba3e655e1d21e7536807a2216c023e8f5341e0abfc03be963b73a10d15` | 0 |
| src/models/room-retention.ts | 9530 | `b0e890b7963e2c81026f27128b7b715b7b9dd2f1a42f20333dd711bb46566bb4` | 0 |
| src/models/room-state.ts | 50103 | `f91b2e95f7b42a1a7ac149ff2e399be4b3e36ee98bd61909877c155b561f8581` | 0 |
| src/models/room-sticky-events.ts | 19477 | `cd5ffd89151377771108b91731bf92560ac9777d8537096804644a6bf85ca352` | 0 |
| src/models/room-summary.ts | 2560 | `6426b176e81418e80711e4ab105cd9d15fb3b2b7e7fa9852d23b3b7234856874` | 0 |
| src/models/room.ts | 167450 | `4976465f362fc7e8790e1b6a3c1986a194e985a503a7d681eebf9acc79d5ac0a` | 0 |
| src/models/search-result.ts | 2196 | `0fc61ec647138279b7c973325a0090b7540d2bef0a18b45a28802b5f8935c27c` | 0 |
| src/models/thread.ts | 45029 | `e85b3f2848922b182ba8e68d23cbea40a93698cfe7e64e37d8870b29cfef1444` | 0 |
| src/models/typed-event-emitter.ts | 9887 | `cb12d8ff1a35a791659f58e3da9695e9cc2dd891525c4f5af03f18aae800e9f2` | 0 |
| src/models/user.ts | 10505 | `56bb8cfbc8bb29cb1596ffc79751c80527efe87576af0a8f2108fadda954b510` | 0 |
| src/oauth/authorize.ts | 10988 | `4ba90565262ef275a7bd251ab3eac49b9b468151a858e266e45d2d83defea7fa` | 0 |
| src/oauth/discover.ts | 5150 | `19e641fb6b38ca2c1fa18409c94f432f63f3828fe333d660f71ac1a3fbc8d657` | 0 |
| src/oauth/error.ts | 4263 | `7af7a2776a1549cbb9f81afd2dd1822386ee8161d26bbf6b6b2040408b3cb028` | 0 |
| src/oauth/fetch.ts | 2136 | `60558cde378df42637e6710913167a0d1137911eee8ebeba320405d7e9ce2e07` | 0 |
| src/oauth/index.ts | 15803 | `beda6be4deac26d2a12ecd040e540baf752a4cdc2d3df7d330366bd71675a235` | 0 |
| src/oauth/register.ts | 6371 | `e86713edc415bbc7e5a6a646aabf0bc918b03028c7e304a00991d64599a5e25f` | 0 |
| src/oauth/tokenRefresher.ts | 3893 | `1decce2d46fd3016c1d3c2bb983730a2a042d854b9ce176ff893fe9abbb993bc` | 0 |
| src/pollingCachedValue.ts | 6379 | `e435c8d82c1a08da83e462c2370997c03fcab8f7b00a5032332676870e298065` | 0 |
| src/pushprocessor.ts | 31074 | `5a2575ea60ab16d5a33bd91ca6c04d9980869191b4a5a09fbd3c7a284780c053` | 0 |
| src/randomstring.ts | 4348 | `fe71468843d165ab583cb979192743bff24a0ce173a4a88dbc8f1dda962cddf0` | 0 |
| src/realtime-callbacks.ts | 5674 | `e63fa71d8f3661356e60137939599cc126478474102d417a6d3f22654e680545` | 0 |
| src/receipt-accumulator.ts | 8390 | `1d2ecfe2c66188ece295fc7511eb8ec8b2ea7d72c1260f58874f1eba1a6eaf39` | 0 |
| src/rendezvous/MSC4108SignInWithQR.ts | 21110 | `925187960dfff07845867ff3a74faf85d8e2ee5d44ba8025bfaeacb3fb3df7ef` | 0 |
| src/rendezvous/RendezvousChannel.ts | 1451 | `1ea65e1917379fca5782f5f47da0c438fc08fce9e17f81369fcc9b60f7314359` | 0 |
| src/rendezvous/RendezvousCode.ts | 832 | `11be1f05c09de3b557093db04ff6b5c98f69c69a5fd14e7161bc88ac27c83680` | 0 |
| src/rendezvous/RendezvousError.ts | 829 | `2131ea8a277b4cac473168728e5a458771a50a7041c369534d334a8ed9eb6242` | 0 |
| src/rendezvous/RendezvousFailureReason.ts | 2008 | `858699640806fb28c533e97734ac83f9d40cc9a02e7c315434e9a517d67be2af` | 0 |
| src/rendezvous/RendezvousIntent.ts | 718 | `c71f317d2df74b603d4eccab6835f297554f1d885c3878b5693d597b54b889b0` | 0 |
| src/rendezvous/RendezvousTransport.ts | 1740 | `991721867dd0b8c2ef6567cf28f58431b74f0e2024b5ebfeac71d905c053d414` | 0 |
| src/rendezvous/SignInWithQRFlow.ts | 4540 | `2b2bd60ebc9cd7f7730e4e032af3fc13373a8aea8929e4fe65028d9c45508a0a` | 0 |
| src/rendezvous/channels/MSC4108SecureChannel.ts | 9892 | `99cb0cdd4a82c41e00eead904cf0a000034110973af769842541a89ab98db64c` | 0 |
| src/rendezvous/channels/index.ts | 623 | `ef7aa8d1738686cc5b718a7832704b2da0206c47edbf7b6e2253eb96a5d04ad4` | 0 |
| src/rendezvous/index.ts | 5824 | `53ac165dc75663cabca7f96a6404fc0203964b9c5a0ade61501319a8e1d995b6` | 0 |
| src/rendezvous/transports/MSC4108RendezvousSession.ts | 9060 | `865fdbcf852ac598cc8ae59ff5356cecb854ca4bd9d3430cc78b9e6f571dbe4c` | 0 |
| src/rendezvous/transports/index.ts | 627 | `989be957b9236c1b71e89e0ea4e8fd4b5d5ea95caf4106771b106c509ce9133d` | 0 |
| src/retentionPolicy.ts | 2063 | `b8caa86221cfe5f20ccff56f9fdf6d1996a8121271789160739a41802a4827af` | 0 |
| src/room-hierarchy.ts | 5405 | `bc100c5cba12f338b4f546f9ae310c6d9ebf3f3d70ec71643911c55d24df88b7` | 0 |
| src/room-summary-api.ts | 4825 | `b4cdbb3ab8d1ab8c995187ed9c204cbb2c855ef70132f30624aa5f5d89cf898c` | 0 |
| src/rtcTransportsCachedValue.ts | 1746 | `f950137da8f72e830d86e9d0cb3a95f62c0f14665f103be6dd9e62c82cf05218` | 0 |
| src/rust-crypto/CrossSigningIdentity.ts | 9487 | `e2366abe19f8076a530ac9396ee0d13759f1612763890e0a35812df33ece7eaa` | 0 |
| src/rust-crypto/DehydratedDeviceManager.ts | 15261 | `477011159b88e67df40be583e6271106734a3bbc18251498ef2ac747459028b1` | 0 |
| src/rust-crypto/KeyClaimManager.ts | 3571 | `9a9e03f41cbf7cfc583e789c40cc5933c4dc8aae654243b42c828746e7063125` | 0 |
| src/rust-crypto/OutgoingRequestProcessor.ts | 9576 | `d23c183e6887110f85e941a8538b719db187e2a2f5ad1c79eb01796df2043cf6` | 0 |
| src/rust-crypto/OutgoingRequestsManager.ts | 7792 | `9a97dd4bfe10496fe4c09e4b62933d1e99354100e98b6e96e981b22b9c820c97` | 0 |
| src/rust-crypto/PerSessionKeyBackupDownloader.ts | 22375 | `d9a2f9770fd79ff4ef8df35c95f6a4ca4bf683cb5d03011162853b2ecd406b29` | 0 |
| src/rust-crypto/RoomEncryptor.ts | 17345 | `5e765d042c692c59ec58153f8091bfd3ae5ef220ce457ce538cdc0c09b7e1acc` | 0 |
| src/rust-crypto/backup.ts | 43711 | `0035718d4b52dd39964519ed204cf25887214b6a0104755f3119d187d731af41` | 0 |
| src/rust-crypto/constants.ts | 694 | `71dd26458c9d5eb99d484609365c6a47a3bcf5b718d904e972aaa7ebe5b76e08` | 0 |
| src/rust-crypto/device-converter.ts | 4512 | `f509daf3849824b479a132b2ef4d9316081244a9cac7cefd688017c52ce8d248` | 0 |
| src/rust-crypto/index.ts | 12193 | `b76c96fa2cd65147622d3f4c91559548da7c32211dbc6eab5334b013d666924d` | 0 |
| src/rust-crypto/libolm_migration.ts | 23501 | `8f5d5aa20614a49e855d21e6377cadc18b3d53f588bd4badc25694312066f631` | 0 |
| src/rust-crypto/rust-crypto.ts | 110017 | `d9ceb74fad995cc8f9c64b7ef419f61b60013b834fc04ffd3c891fed4fab7986` | 0 |
| src/rust-crypto/secret-storage.ts | 2260 | `17e0294adf6b2c600067bbcd629dd646374270e7d8c662d34c54c07c2e62b7b8` | 0 |
| src/rust-crypto/verification.ts | 33650 | `efcf60058c76106c7b4de92f320edf896b386c9aa37c98be6f2bd32a5e99b153` | 0 |
| src/scheduler.ts | 12287 | `d149c0154588fed8858f3ffd5d34e4656c5240314672c021567b2c3ff71b9f91` | 0 |
| src/secret-storage.ts | 26566 | `8722cb2b6e1e8f68f6174f527ca0eea15c6a5b955210ba96674dcb2d79ee3a61` | 0 |
| src/serverCapabilities.ts | 2950 | `c989d09e10b42f97fe107d1dfc09936dce398856faf05d137bc8b1e1adbc6c49` | 0 |
| src/service-types.ts | 721 | `5e48fe607051965406a73b44f92ce75442e2ecf6a14e877faeedc85fd5006034` | 0 |
| src/sliding-sync-sdk.ts | 44910 | `8661849d8dcee600c0955da41978fb59e1e636cda18a88a0b41fff88386fd879` | 0 |
| src/sliding-sync.ts | 27535 | `e0cceacb26c49b6274bc0a997b7b75c6c770108fbf91568ad68b4b2505d69064` | 0 |
| src/store/index.ts | 9226 | `a4c54803d0c8e1dbf92dc8591477ca24333c017a705274e4eaca82300c1fcb77` | 0 |
| src/store/indexeddb-backend.ts | 2211 | `5cd1fdae79c7011129dfba4151f366138ca0e5c9854d1e0b7cc2c11c521918a6` | 0 |
| src/store/indexeddb-local-backend.ts | 26077 | `da2854c9469853a6b497803e10b8ae3265dde110c5b0af0f29cfd904a85ae87f` | 0 |
| src/store/indexeddb-remote-backend.ts | 9114 | `556f633671521246aaf0ff55590b319a3ac403a2ff0b8408d436c67111218024` | 0 |
| src/store/indexeddb-store-worker.ts | 6046 | `474cbca7c93511c83c67306186f92207be5fb2d0fc4146bc588c21529f51bf30` | 0 |
| src/store/indexeddb.ts | 17247 | `d5020b51f9a60e71ce977813866008404782abd71946ead89da74dd282505668` | 0 |
| src/store/local-storage-events-emitter.ts | 2045 | `1f123f1c351923540faa95889d0961fc028a75e5f616848725fa0988fd057b8b` | 0 |
| src/store/memory.ts | 15594 | `5592ba38069de2b8583382d317451af56b624aaa230630fa9ab19572b6891895` | 0 |
| src/store/stub.ts | 7611 | `3445f68b4c4050b3e87e2c899d9a5e12750e7d23c1f31e76a803f73436d6b74d` | 0 |
| src/sync-accumulator.ts | 34890 | `98f0f4f808d91404f271a9736d8d1b2dcebee1b3263e4812fc29c5edd5b0ab1b` | 0 |
| src/sync.ts | 93097 | `19b79aa8a268472f7ce56865ca33ed22b664a8aba29ee3553747957c28255de6` | 0 |
| src/testing.ts | 6908 | `903c8f4bc6b109c578406a6bba7821f98b67b525ea6e05391d943194c5300331` | 0 |
| src/thread-utils.ts | 1258 | `c531d4a91a8124026f98fd9012db84f93a35d3eef33f7bc6f1d4d94a6d3b3ad7` | 0 |
| src/timeline-window.ts | 19595 | `05301487a143cdb69e6bca783ad71a7b9a7e99386e652f879dad54fcb71d9430` | 0 |
| src/types.ts | 2035 | `3850d38c16d9c0b03931eb2f99cf708fa4cb9052574277a982d068fb8a0b8110` | 0 |
| src/utils/decryptAESSecretStorageItem.ts | 2264 | `5c53b9ac52ee3cbd47e7ca56fe3db3f72063e8abfbed9ffb7c8bb95bc0082868` | 0 |
| src/utils/encryptAESSecretStorageItem.ts | 2843 | `bf40753c5a65f16b9a5886488d80e7a66fc777d93d134c15b7e9a45bc49be3f8` | 0 |
| src/utils/internal/deriveKeys.ts | 2005 | `fab4c426a661592eb5a5b40588e9a9c6fd40a5979370121c731385d768766500` | 0 |
| src/utils/roomVersion.ts | 1467 | `481c12212e6f04b16b2c1095d7a14c22ab2aaa21c1758904484c632bc139754f` | 0 |
| src/utils.ts | 27415 | `4faf2126db1ed8aad725b932bea303c5c479269c2cdedb40bb8a2f83ca1bd5d8` | 0 |
| src/version-support.ts | 1577 | `6669ba730d7298a6d45ba40041952ddedf2abf1c2998557cec8e453ae9d902c7` | 0 |
| src/webrtc/audioContext.ts | 1477 | `831090f15b5220517c57d9fa2c933c383e3794f33cace713b1a916e511687de7` | 0 |
| src/webrtc/call.ts | 123321 | `e17b2fc7175a8c66e0506cf8e61b39b20b6efec3716dd7dccb837ad10bef5929` | 0 |
| src/webrtc/callEventHandler.ts | 17298 | `283ccca3d2a468ffaaa0a9baa74d769b7abac09d9152fdd11834a1d487042f07` | 0 |
| src/webrtc/callEventTypes.ts | 2496 | `70708254b828611f755dffe95c2cf9af116ee9d33756ba9151a3fbb3e47e3d8e` | 0 |
| src/webrtc/callFeed.ts | 12065 | `8ebe216d2898b458a4dfb4b38608777239e962b1430d0def2a73c17c9aa03ad6` | 0 |
| src/webrtc/groupCall.ts | 68210 | `a61054771c760ec292c058e8aac89c036e2d178877f1daf6f45b9be39cdc6840` | 0 |
| src/webrtc/groupCallEventHandler.ts | 9298 | `9337e8b6c2f4a1e49ce7a8722a1a848df66d3bd6852d0c0cef4c1c75da1e3e89` | 0 |
| src/webrtc/mediaHandler.ts | 19176 | `18cda97b96758ff4962f1fc1ed93e24b2f173c34e07d867987c104d45502625f` | 0 |
| src/webrtc/stats/callFeedStatsReporter.ts | 3496 | `f2c3dd8282b23e3042be1bc84d84f6e72ed4d0125499a2ca505f8c1da9ad73f0` | 0 |
| src/webrtc/stats/callStatsReportGatherer.ts | 10228 | `b491689b1af9ec33f8fdf5b09bbedbc45fa1cac1bd4cf08533e5b6a052f720db` | 0 |
| src/webrtc/stats/callStatsReportSummary.ts | 993 | `c54b4406c0798c790afc79cba592e9f8e689f343ac4acf170e2d9bb739f02b80` | 0 |
| src/webrtc/stats/connectionStats.ts | 1349 | `afd082c7cfc4240bb1cc9fa682c4d9f8361d68e5c6702c83111f468470c52303` | 0 |
| src/webrtc/stats/connectionStatsBuilder.ts | 1131 | `1381fda8aa3750634bf6a396d237753a2e4558b6ca5630bf88ca9d879a88725b` | 0 |
| src/webrtc/stats/connectionStatsReportBuilder.ts | 5292 | `7869e4f9bfae21c390b7329a895f493a1d581040cf67d7aa1676296a620e64cd` | 0 |
| src/webrtc/stats/groupCallStats.ts | 3371 | `bd2b420619f6cd1985243f08f6d95e68ff10dc8f7d130fa1eb80f845a0751919` | 0 |
| src/webrtc/stats/media/mediaSsrcHandler.ts | 1907 | `c6b75144798c1d48d9bb1111a7529a12fbe56ddbdd5e475b6ecf81b9969cdd94` | 0 |
| src/webrtc/stats/media/mediaTrackHandler.ts | 2637 | `9a07a863c721f264ff93fbe658204203178ae5e005b0a78004ae1acee2410ec3` | 0 |
| src/webrtc/stats/media/mediaTrackStats.ts | 4477 | `c04232716c147a8c0fcefeffe9829012f2469e5984fbd37cd4215a195a44db2b` | 0 |
| src/webrtc/stats/media/mediaTrackStatsHandler.ts | 3481 | `92812080650bc2da12e8ba2f702775d41e865f77bd51b37a52c8e2bc3dc5fafd` | 0 |
| src/webrtc/stats/statsReport.ts | 4561 | `3045a650ce872682e61c2bdfe41f2fa90481a9368b980df524a792aa3212a8ac` | 0 |
| src/webrtc/stats/statsReportEmitter.ts | 1795 | `4bec70aa41d8693d903d0846b7d629f5463b7204f778d2b481187a35d0a6ac39` | 0 |
| src/webrtc/stats/summaryStatsReportGatherer.ts | 6470 | `099c58b3ddc43eac4d99f870ac702d27ac6b8e9c1219c6cb78bbcabeeb9dc0cd` | 0 |
| src/webrtc/stats/trackStatsBuilder.ts | 7631 | `7edf66a452f0552d75a45b7fff299dba2954a1f1503773dd60bf267d6cefb6d1` | 0 |
| src/webrtc/stats/transportStats.ts | 800 | `61e6f86550bb6de2f3f882c1a7079af16876be11929de3752b3870a8e1580cbf` | 0 |
| src/webrtc/stats/transportStatsBuilder.ts | 2010 | `95211b2daa84be1eeea410b0ef25c28380db6d5a4df16bfc6633ac41bca36d93` | 0 |
| src/webrtc/stats/valueFormatter.ts | 885 | `c03b184006a65bf8b1942c47fabf777341c77a35ad251da66254ad34e3b7cb11` | 0 |
| src/wellKnownCachedValue.ts | 1358 | `c47bdc52b01888fcb04ee4b079762ed6f99650fb0ac7ed552780468acf4f3464` | 0 |
| vitest.config.ts | 2153 | `9c5aa10acada72503b56023cc19cf4520e500e35b19960da6e6546150b8060f8` | 0 |
