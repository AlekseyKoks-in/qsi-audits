# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** bitbox02-firmware @ ae548ef4e40f · BitBox (Shift Crypto) — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-29 21:07 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 882ca3ae-fad1-4229-865a-9a11ad5e8585 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `e5697285d21aad4283fd8ec1366faa0baad4b8e6f794b6459f1d7678347d9cb4` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **1**
- Высокая: **11**
- Средняя: **56**
- Низкая: **3**
- Информационная: **7**

- Подтверждённая техническая уязвимость: 1
- Известная уязвимая версия компонента: 33
- Подтверждённая ошибка конфигурации: 1
- Потенциальный криптографический риск: 3
- Долгосрочный постквантовый риск: 38
- Рекомендация по улучшению: 1
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

Проверка аналитика: подтверждено — 13, не применимо — 6, отклонено как ложные срабатывания — 0.

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/BitBoxSwiss/bitbox02-firmware> @ `ae548ef4e40f548a17542ba457f138db4fa0069d` — ссылки в доказательствах открывают строки на этом коммите.

2645 файлов, всего 52428220 байт, редактирований: 19; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 2556 | external/CMSIS/Include/cmsis_armclang.h: 707 lines scanned with 16 rule patterns and 123 registry patterns; external/CMSIS/Include/cmsis_clang.h: 708 lines scanned with 16 rule patterns and 123 registry patterns; external/CMSIS/Include/cmsis_compiler.h: 292 lines scanned with 16 rule patterns and 123 registry patterns |
| chain_map | проверено | 3 | messages/btc.proto: Bitcoin; messages/cardano.proto: Cardano; messages/eth.proto: Ethereum and EVM chains |
| dependencies | проверено | 48 | py/pyproject.toml: 0 dependencies parsed (0 pinned); py/requirements.txt: 8 dependencies parsed (0 pinned); src/rust/Cargo.lock: 135 dependencies parsed (135 pinned) |
| certificates_and_keys | проверено | 23 | releases/pubkeys/JuliusWiedemann.asc: certificates/keys parsed; releases/pubkeys/JunghoonLee.asc: certificates/keys parsed; releases/pubkeys/My1.asc: certificates/keys parsed |
| keys | Недостаточность данных | 1 | releases/pubkeys/psteiger.asc line 1: OpenPGP algorithm ID 18 is not in the algorithm registry |
| secrets | проверено | 9 | src/rust/bitbox-secp256k1/src/lib.rs: value(s) at line(s) 375 (test_dleq), 407 (test_secp256k1_sign), 441 (test_secp256k1_sign_zero_host_nonce_differs_from_no_host_nonce_sign), 456 (test_secp256k1_sign_no_host_nonce_deterministic), 491 (test_secp256k1_nonce_commit) are declared inside a fixture and treated as test data, although the file itself is not test code; src/rust/bitbox-secp256k1/src/lib.rs: 5 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); src/rust/bitbox02-rust/src/hww/api/change_password.rs: value(s) at line(s) 196 (test_process_confirm_password_mismatch) are declared inside a fixture and treated as test data, although the file itself is not test code |
| tls_code | Недостаточность данных | 1 | tools/atecc608/go.mod: go 1.19 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS |
| certificates | ошибка (не проверено) | 1 | external/cryptoauthlib/lib/atcacert/atcacert_pem.h line 37: certificate could not be parsed (ValueError) |
| tls_key_exchange_groups | Недостаточность данных | 4 | external/lvgl/docs/doxygen_xml.py line 349: not in the algorithm registry, not assessed: {}; external/lvgl/docs/src/details/main-modules/indev/groups.rst line 4: not in the algorithm registry, not assessed: =====; external/lvgl/scripts/generate_lv_conf.py line 67: not in the algorithm registry, not assessed: re.search(r'([A-Z0-9_]+)\s+(.+)' |
| tls_configuration | проверено | 4 | external/lvgl/docs/doxygen_xml.py: openssl TLS directives parsed; external/lvgl/docs/src/details/main-modules/indev/groups.rst: openssl TLS directives parsed; external/lvgl/scripts/generate_lv_conf.py: openssl TLS directives parsed |
| osv_advisories | проверено | 1 | 207 pinned packages queried at OSV.dev; 15 affected |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- keys — Недостаточность данных: releases/pubkeys/psteiger.asc line 1: OpenPGP algorithm ID 18 is not in the algorithm registry
- tls_code — Недостаточность данных: tools/atecc608/go.mod: go 1.19 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS
- certificates — ошибка (не проверено): external/cryptoauthlib/lib/atcacert/atcacert_pem.h line 37: certificate could not be parsed (ValueError)
- tls_key_exchange_groups — Недостаточность данных: external/lvgl/docs/doxygen_xml.py line 349: not in the algorithm registry, not assessed: {}
- tls_key_exchange_groups — Недостаточность данных: external/lvgl/docs/src/details/main-modules/indev/groups.rst line 4: not in the algorithm registry, not assessed: =====
- tls_key_exchange_groups — Недостаточность данных: external/lvgl/scripts/generate_lv_conf.py line 67: not in the algorithm registry, not assessed: re.search(r'([A-Z0-9_]+)\s+(.+)'
- tls_key_exchange_groups — Недостаточность данных: external/lvgl/scripts/update_version.py line 28: not in the algorithm registry, not assessed: re.search(self.RE_PATTERN

## 5. Краткое описание архитектуры

Static review of the source tree bitbox02-firmware at ae548ef4e40f548a17542ba457f138db4fa0069d. 2645 files analysed; of 8952 files, 4270 are test, fuzzing, benchmark or example code and were left out, 1518 are not read by any analyzer, 1 exceed the per-file limit and 518 did not fit the total limit. Files the total limit could not fit include: external/optiga-trust-m/external/mbedtls/include/mbedtls/compat-1.3.h, external/optiga-trust-m/external/mbedtls/include/mbedtls/config.h, external/optiga-trust-m/external/mbedtls/include/mbedtls/debug.h, external/optiga-trust-m/external/mbedtls/include/mbedtls/des.h, external/optiga-trust-m/external/mbedtls/include/mbedtls/dhm.h. 15718 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. 1543 files come from directories a .gitmodules pins and are read as shipped source rather than skipped as a dependency cache. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **0** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 52.8%

## 7. Подробное описание находок

### QSI-2026-06913 — certifi 2022.12.7 затронут GHSA-6q48-6c7w-9gw2 (PYSEC-2026-4320)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/certifi@2022.12.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 54.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-6q48-6c7w-9gw2 (PYSEC-2026-4320) для пакета PyPI certifi версии 2022.12.7: certifi bundles emSign root CAs with compromised intermediate CA keys. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6q48-6c7w-9gw2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-6q48-6c7w-9gw2](https://osv.dev/vulnerability/GHSA-6q48-6c7w-9gw2) · line 13 · SHA-256 87c1ba23d8d1ad688cb3d3331ff88fa3cb0ba134a6064a4568a2d5aa2751c508_

```
{"id": "GHSA-6q48-6c7w-9gw2", "aliases": ["PYSEC-2026-4320"], "modified": "2026-10-26T16:15:35.371128995Z", "summary": "certifi bundles emSign root CAs with compromised intermediate CA keys", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2026.10.18).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06890 — Проверка TLS-сертификата отключена в scripts/generate_version_headers.py

- Серьёзность: **Высокая** · Классификация: Подтверждённая ошибка конфигурации · Уверенность: Высокая
- Затронутый актив: `file:scripts/generate_version_headers.py`
- Источник данных: scripts/generate_version_headers.py
- Метод обнаружения: Сопоставление регулярных выражений с API конкретного языка.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 70.4 / 100
- CVSS v3.1: 6.8 (`CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

1 случаев отключения проверки (verify=False), первый — строка 230.

**Возможные последствия.** Соединения уязвимы к перехвату «человек посередине».

**Шаги воспроизведения.**

```
Откройте строка 230 в предоставленном файле scripts/generate_version_headers.py и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scripts/generate_version_headers.py](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/scripts/generate_version_headers.py#L230) · line 230 · SHA-256 14c945f1f3952da4886e703323a55eaab298fcd6ce757a9042715deadd5611f1_

```
  228 | 
  229 | def strict_tag_version(repo_root: str | os.PathLike[str], prefix: str | None) -> str:
  230 |     return compute_tag_version(repo_root, prefix, check_gpg=True, verify=False, check_semver=True)
  231 | 
  232 | 
```

**Ограничения проверки.** Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Удалите отключение; используйте корректный набор УЦ или пиннинг.

**Повторная проверка.** Повторно просканируйте код и проверьте места вызова из доказательства.

### QSI-2026-06914 — certifi 2022.12.7 затронут GHSA-xqr8-7jwr-rhp7 (CVE-2023-37920, PYSEC-2023-135)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/certifi@2022.12.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-xqr8-7jwr-rhp7 (CVE-2023-37920, PYSEC-2023-135) для пакета PyPI certifi версии 2022.12.7: Removal of e-Tugra root certificate. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xqr8-7jwr-rhp7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xqr8-7jwr-rhp7](https://osv.dev/vulnerability/GHSA-xqr8-7jwr-rhp7) · line 13 · SHA-256 2f94715e09d8ea440753f6e548090fbc7961491b5ef65e35a87333a63bafe263_

```
{"id": "GHSA-xqr8-7jwr-rhp7", "aliases": ["CVE-2023-37920", "PYSEC-2023-135"], "modified": "2026-09-10T03:50:08.653753752Z", "summary": "Removal of e-Tugra root certificate", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2023.7.22).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06918 — jinja2 3.1.2 затронут GHSA-gmj6-6f8f-6699 (CVE-2024-56201, PYSEC-2026-1472)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/jinja2@3.1.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: 8.8 (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-gmj6-6f8f-6699 (CVE-2024-56201, PYSEC-2026-1472) для пакета PyPI jinja2 версии 3.1.2: Jinja has a sandbox breakout through malicious filenames. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-gmj6-6f8f-6699
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-gmj6-6f8f-6699](https://osv.dev/vulnerability/GHSA-gmj6-6f8f-6699) · line 28 · SHA-256 1fc2fcfcf66b7cde744640e67903559b4f93dfc0417870f1dfc401d100a387c4_

```
{"id": "GHSA-gmj6-6f8f-6699", "aliases": ["CVE-2024-56201", "PYSEC-2026-1472"], "modified": "2026-09-10T03:50:56.152882717Z", "summary": "Jinja has a sandbox breakout through malicious filenames", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.1.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06921 — jinja2 3.1.2 затронут GHSA-q2x7-8rv6-6q7h (CVE-2024-56326, PYSEC-2026-1475)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/jinja2@3.1.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: 7.8 (`CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-q2x7-8rv6-6q7h (CVE-2024-56326, PYSEC-2026-1475) для пакета PyPI jinja2 версии 3.1.2: Jinja has a sandbox breakout through indirect reference to format method. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-q2x7-8rv6-6q7h
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-q2x7-8rv6-6q7h](https://osv.dev/vulnerability/GHSA-q2x7-8rv6-6q7h) · line 28 · SHA-256 cf69831558e5cfcc55e9251c195c61130015555745da08e16087c26c514b3d75_

```
{"id": "GHSA-q2x7-8rv6-6q7h", "aliases": ["CVE-2024-56326", "PYSEC-2026-1475"], "modified": "2026-09-10T03:50:21.662855250Z", "summary": "Jinja has a sandbox breakout through indirect reference to format method", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.1.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06928 — urllib3 1.26.15 затронут GHSA-2xpw-w6gg-jr37 (CVE-2025-66471, PYSEC-2026-1994)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/urllib3@1.26.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-2xpw-w6gg-jr37 (CVE-2025-66471, PYSEC-2026-1994) для пакета PyPI urllib3 версии 1.26.15: urllib3 streaming API improperly handles highly compressed data. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2xpw-w6gg-jr37
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2xpw-w6gg-jr37](https://osv.dev/vulnerability/GHSA-2xpw-w6gg-jr37) · line 60 · SHA-256 8f549172278134db8bb6a128450758a9ebfe0537c99993930a95ab78795b6dd1_

```
{"id": "GHSA-2xpw-w6gg-jr37", "aliases": ["CVE-2025-66471", "PYSEC-2026-1994"], "modified": "2026-09-25T17:15:05.968189421Z", "summary": "urllib3 streaming API improperly handles highly compressed data", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.6.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06930 — urllib3 1.26.15 затронут GHSA-38jv-5279-wg99 (CVE-2026-21441, PYSEC-2026-1996)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/urllib3@1.26.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-38jv-5279-wg99 (CVE-2026-21441, PYSEC-2026-1996) для пакета PyPI urllib3 версии 1.26.15: Decompression-bomb safeguards bypassed when following HTTP redirects (streaming API). Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-38jv-5279-wg99
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-38jv-5279-wg99](https://osv.dev/vulnerability/GHSA-38jv-5279-wg99) · line 60 · SHA-256 528407f765ddc33699b8c258636cc375710304468ddc58652eaa66f3f06d7c16_

```
{"id": "GHSA-38jv-5279-wg99", "aliases": ["CVE-2026-21441", "PYSEC-2026-1996"], "modified": "2026-09-10T03:50:32.562010895Z", "summary": "Decompression-bomb safeguards bypassed when following HTTP redirects (streaming API)", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.6.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06931 — urllib3 1.26.15 затронут GHSA-8988-9cw3-xx77 (CVE-2026-97687, PYSEC-2026-4175)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/urllib3@1.26.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-8988-9cw3-xx77 (CVE-2026-97687, PYSEC-2026-4175) для пакета PyPI urllib3 версии 1.26.15: urllib3: HTTPS proxy TLS configuration may be ignored or overridden. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8988-9cw3-xx77
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8988-9cw3-xx77](https://osv.dev/vulnerability/GHSA-8988-9cw3-xx77) · line 60 · SHA-256 c51c0d680d885d638def44e1b95a18c000c1eb5bbeb4a65fa11f7653bf1a7c7d_

```
{"id": "GHSA-8988-9cw3-xx77", "aliases": ["CVE-2026-97687", "PYSEC-2026-4175"], "modified": "2026-10-01T17:55:53.793608550Z", "summary": "urllib3: HTTPS proxy TLS configuration may be ignored or overridden", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.8.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06933 — urllib3 1.26.15 затронут GHSA-gm62-xv2j-4w53 (CVE-2025-66418, PYSEC-2026-1998)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/urllib3@1.26.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-gm62-xv2j-4w53 (CVE-2025-66418, PYSEC-2026-1998) для пакета PyPI urllib3 версии 1.26.15: urllib3 allows an unbounded number of links in the decompression chain. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-gm62-xv2j-4w53
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-gm62-xv2j-4w53](https://osv.dev/vulnerability/GHSA-gm62-xv2j-4w53) · line 60 · SHA-256 b69c9a68201dc7d1cd1c1c737f9fd193a253ad102d274aa1778f180f82596148_

```
{"id": "GHSA-gm62-xv2j-4w53", "aliases": ["CVE-2025-66418", "PYSEC-2026-1998"], "modified": "2026-09-10T03:50:58.741847479Z", "summary": "urllib3 allows an unbounded number of links in the decompression chain", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.6.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06937 — urllib3 1.26.15 затронут GHSA-vxq7-64xx-v4gw (CVE-2026-97689, PYSEC-2026-4177)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/urllib3@1.26.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-vxq7-64xx-v4gw (CVE-2026-97689, PYSEC-2026-4177) для пакета PyPI urllib3 версии 1.26.15: urllib3: HTTPResponse.stream()/read_chunked() buffers an unbounded chunk-size line into memory. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vxq7-64xx-v4gw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vxq7-64xx-v4gw](https://osv.dev/vulnerability/GHSA-vxq7-64xx-v4gw) · line 60 · SHA-256 cbf2e0ae22b277477ba53ac789fc1c2df8d7fa5808195e02870fcf446461ec1c_

```
{"id": "GHSA-vxq7-64xx-v4gw", "aliases": ["CVE-2026-97689", "PYSEC-2026-4177"], "modified": "2026-10-01T17:55:57.514829071Z", "summary": "urllib3: HTTPResponse.stream()/read_chunked() buffers an unbounded chunk-size line into memory", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.8.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06861 — Режим ECB блочного шифра в external/samd51a-ds/include/component/aes.h

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `file:external/samd51a-ds/include/component/aes.h`
- Источник данных: external/samd51a-ds/include/component/aes.h
- Метод обнаружения: Сопоставление регулярных выражений с API конкретного языка.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 38.8 / 100
- CVSS v3.1: неприменимо

1 использований режима ECB (первое — строка 81).

**Возможные последствия.** ECB раскрывает закономерности в зашифрованных данных и не обеспечивает целостность.

**Шаги воспроизведения.**

```
Откройте строка 81 в предоставленном файле external/samd51a-ds/include/component/aes.h и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [external/samd51a-ds/include/component/aes.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/samd51a-ds/include/component/aes.h#L81) · line 81 · SHA-256 92ef17166ab022a20ad6f4d44119934fae3cc5b8789a3e7c85b0fa7458e9450e_

```
   79 | #define   AES_CTRLA_AESMODE_CCM_Val       _U_(0x5)   /**< \brief (AES_CTRLA) CCM mode */
   80 | #define   AES_CTRLA_AESMODE_GCM_Val       _U_(0x6)   /**< \brief (AES_CTRLA) Galois counter mode */
   81 | #define AES_CTRLA_AESMODE_ECB       (AES_CTRLA_AESMODE_ECB_Val     << AES_CTRLA_AESMODE_Pos)
   82 | #define AES_CTRLA_AESMODE_CBC       (AES_CTRLA_AESMODE_CBC_Val     << AES_CTRLA_AESMODE_Pos)
   83 | #define AES_CTRLA_AESMODE_OFB       (AES_CTRLA_AESMODE_OFB_Val     << AES_CTRLA_AESMODE_Pos)
```

**Ограничения проверки.** Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Используйте AEAD-режим (GCM) с уникальными nonce.

**Повторная проверка.** Повторно просканируйте код и проверьте места вызова из доказательства.

### QSI-2026-06901 — Режим ECB блочного шифра в external/optiga-trust-m/external/mbedtls/include/mbedtls/cipher.h

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `file:external/optiga-trust-m/external/mbedtls/include/mbedtls/cipher.h`
- Источник данных: external/optiga-trust-m/external/mbedtls/include/mbedtls/cipher.h
- Метод обнаружения: Сопоставление регулярных выражений с API конкретного языка.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 38.8 / 100
- CVSS v3.1: неприменимо

1 использований режима ECB (первое — строка 184).

**Возможные последствия.** ECB раскрывает закономерности в зашифрованных данных и не обеспечивает целостность.

**Шаги воспроизведения.**

```
Откройте строка 184 в предоставленном файле external/optiga-trust-m/external/mbedtls/include/mbedtls/cipher.h и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [external/optiga-trust-m/external/mbedtls/include/mbedtls/cipher.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/optiga-trust-m/external/mbedtls/include/mbedtls/cipher.h#L184) · line 184 · SHA-256 b4ca0728db5ccfb494e9c1d28a1f570024b573214a88c0c50c5651e07549de35_

```
  182 | typedef enum {
  183 |     MBEDTLS_MODE_NONE = 0,               /**< None.                        */
  184 |     MBEDTLS_MODE_ECB,                    /**< The ECB cipher mode.         */
  185 |     MBEDTLS_MODE_CBC,                    /**< The CBC cipher mode.         */
  186 |     MBEDTLS_MODE_CFB,                    /**< The CFB cipher mode.         */
```

**Ограничения проверки.** Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Используйте AEAD-режим (GCM) с уникальными nonce.

**Повторная проверка.** Повторно просканируйте код и проверьте места вызова из доказательства.

### QSI-2026-06902 — Подпись транзакций для сетей (3) основана на подписях на эллиптических кривых

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** True by construction. messages/btc.proto, cardano.proto and eth.proto define the supported chains, whose signature schemes are set by consensus rather than by the wallet. The wallet cannot migrate them unilaterally, so this is a readiness map rather than a defect.
- Затронутый актив: `chain-map`
- Источник данных: messages/btc.proto
- Метод обнаружения: Определения сообщений (.proto) сопоставлены с таблицей схем подписи сетей QSI.
- Анализатор: chain_map 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 56.8 / 100
- CVSS v3.1: неприменимо

Определения сообщений кошелька охватывают сети: Bitcoin, Cardano, Ethereum and EVM chains. Эти сети авторизуют транзакции подписями ECDSA, Ed25519, Schnorr (BIP-340), которые алгоритм Шора взламывает на криптографически значимом квантовом компьютере. Кошелёк не может сам перевести сеть на постквантовые подписи: сначала схему должна принять сеть.

**Возможные последствия.** Когда появится CRQC, атакующий, увидевший открытый ключ аккаунта, сможет вычислить закрытый ключ и вывести средства; когда ключи раскрываются, зависит от сети (повторное использование адресов, модель аккаунтов).

**Шаги воспроизведения.**

```
Откройте файлы .proto, указанные в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [messages/btc.proto](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/messages/btc.proto#L4) · line 4 · SHA-256 9397cf36c17bba81b4bbbc6db29f3dc450925e4566727b47ce57892de62d691d_

```
package shiftcrypto.bitbox02;
```

_file_excerpt · [messages/cardano.proto](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/messages/cardano.proto#L4) · line 4 · SHA-256 9397cf36c17bba81b4bbbc6db29f3dc450925e4566727b47ce57892de62d691d_

```
package shiftcrypto.bitbox02;
```

_file_excerpt · [messages/eth.proto](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/messages/eth.proto#L4) · line 4 · SHA-256 9397cf36c17bba81b4bbbc6db29f3dc450925e4566727b47ce57892de62d691d_

```
package shiftcrypto.bitbox02;
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Сети распознаются по именам определений сообщений (файлы .proto и пакеты); схемы — документированные подписи аккаунтов сетей, а не анализ кода подписи кошелька.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями. Сохраняйте криптогибкость слоя подписи по каждой сети (идентификаторы алгоритмов в сообщениях и хранилище, место под более длинные ключи и подписи) и отслеживайте постквантовые предложения сетей, чтобы добавить новую схему, когда сеть её активирует.

**Повторная проверка.** Повторить, когда сеть активирует постквантовую схему подписи или кошелёк добавит её поддержку.

### QSI-2026-06864 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/JuliusWiedemann.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/JuliusWiedemann.asc#line 1`
- Источник данных: releases/pubkeys/JuliusWiedemann.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/JuliusWiedemann.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/JuliusWiedemann.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/JuliusWiedemann.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06865 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/JunghoonLee.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/JunghoonLee.asc#line 1`
- Источник данных: releases/pubkeys/JunghoonLee.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/JunghoonLee.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/JunghoonLee.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/JunghoonLee.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06866 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/My1.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/My1.asc#line 1`
- Источник данных: releases/pubkeys/My1.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/My1.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/My1.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06867 — Квантово-уязвимый ключ RSA (2048-bit) в releases/pubkeys/My1.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/My1.asc#line 1`
- Источник данных: releases/pubkeys/My1.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 2048-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/My1.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/My1.asc · line 1 · SHA-256 a744425426415d58dbeef862a6f1d8bcf6b00820639c8784270363d0b6330969_

```
OpenPGP subkey: algorithm ID 1 (RSA) 2048-bit
```

_key · releases/pubkeys/My1.asc · line 1 · SHA-256 a744425426415d58dbeef862a6f1d8bcf6b00820639c8784270363d0b6330969_

```
OpenPGP subkey: algorithm ID 1 (RSA) 2048-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06868 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/TheCharlatan.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/TheCharlatan.asc#line 1`
- Источник данных: releases/pubkeys/TheCharlatan.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/TheCharlatan.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/TheCharlatan.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/TheCharlatan.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/TheCharlatan.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/TheCharlatan.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06869 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/beerosagos.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/beerosagos.asc#line 1`
- Источник данных: releases/pubkeys/beerosagos.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/beerosagos.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/beerosagos.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/beerosagos.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06870 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/benma.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/benma.asc#line 1`
- Источник данных: releases/pubkeys/benma.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/benma.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/benma.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/benma.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/benma.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06871 — Квантово-уязвимый ключ RSA (2048-bit) в releases/pubkeys/brianddk.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/brianddk.asc#line 1`
- Источник данных: releases/pubkeys/brianddk.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 2048-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/brianddk.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/brianddk.asc · line 1 · SHA-256 99f8a76d7955bc1cad612c6fe14ee442ba2c3ba5655096eda02d83c54d97d810_

```
OpenPGP primary key: algorithm ID 1 (RSA) 2048-bit
```

_key · releases/pubkeys/brianddk.asc · line 1 · SHA-256 a744425426415d58dbeef862a6f1d8bcf6b00820639c8784270363d0b6330969_

```
OpenPGP subkey: algorithm ID 1 (RSA) 2048-bit
```

_key · releases/pubkeys/brianddk.asc · line 1 · SHA-256 a744425426415d58dbeef862a6f1d8bcf6b00820639c8784270363d0b6330969_

```
OpenPGP subkey: algorithm ID 1 (RSA) 2048-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06872 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/cstenglein.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/cstenglein.asc#line 1`
- Источник данных: releases/pubkeys/cstenglein.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/cstenglein.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/cstenglein.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/cstenglein.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06873 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/frknakk.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/frknakk.asc#line 1`
- Источник данных: releases/pubkeys/frknakk.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/frknakk.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/frknakk.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/frknakk.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06874 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/guggerf.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/guggerf.asc#line 1`
- Источник данных: releases/pubkeys/guggerf.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/guggerf.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/guggerf.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/guggerf.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06875 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/jonathancross.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/jonathancross.asc#line 1`
- Источник данных: releases/pubkeys/jonathancross.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/jonathancross.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/jonathancross.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06876 — Квантово-уязвимый ключ RSA (2048-bit) в releases/pubkeys/jonathancross.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/jonathancross.asc#line 1`
- Источник данных: releases/pubkeys/jonathancross.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 2048-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/jonathancross.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/jonathancross.asc · line 1 · SHA-256 a744425426415d58dbeef862a6f1d8bcf6b00820639c8784270363d0b6330969_

```
OpenPGP subkey: algorithm ID 1 (RSA) 2048-bit
```

_key · releases/pubkeys/jonathancross.asc · line 1 · SHA-256 a744425426415d58dbeef862a6f1d8bcf6b00820639c8784270363d0b6330969_

```
OpenPGP subkey: algorithm ID 1 (RSA) 2048-bit
```

_key · releases/pubkeys/jonathancross.asc · line 1 · SHA-256 a744425426415d58dbeef862a6f1d8bcf6b00820639c8784270363d0b6330969_

```
OpenPGP subkey: algorithm ID 1 (RSA) 2048-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06877 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/nickez.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/nickez.asc#line 1`
- Источник данных: releases/pubkeys/nickez.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/nickez.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/nickez.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/nickez.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/nickez.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/nickez.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/nickez.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/nickez.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/nickez.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06878 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/offbyn.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/offbyn.asc#line 1`
- Источник данных: releases/pubkeys/offbyn.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/offbyn.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/offbyn.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/offbyn.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/offbyn.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/offbyn.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06879 — Квантово-уязвимый ключ Ed25519 (Ed25519) в releases/pubkeys/psteiger.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/psteiger.asc#line 1`
- Источник данных: releases/pubkeys/psteiger.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ Ed25519 Ed25519 (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/psteiger.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/psteiger.asc · line 1 · SHA-256 6dbf836a10cb57142effcc3f89dd5e74340870bac059dd57e9f528bf344e8db8_

```
OpenPGP primary key: algorithm ID 22 (Ed25519) Ed25519
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06880 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/stadicus.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/stadicus.asc#line 1`
- Источник данных: releases/pubkeys/stadicus.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/stadicus.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/stadicus.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/stadicus.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/stadicus.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/stadicus.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06881 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/strnbrg.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/strnbrg.asc#line 1`
- Источник данных: releases/pubkeys/strnbrg.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/strnbrg.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/strnbrg.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/strnbrg.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06882 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/sutterseba.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/sutterseba.asc#line 1`
- Источник данных: releases/pubkeys/sutterseba.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/sutterseba.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/sutterseba.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/sutterseba.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06883 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/tomasvrba.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/tomasvrba.asc#line 1`
- Источник данных: releases/pubkeys/tomasvrba.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/tomasvrba.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/tomasvrba.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/tomasvrba.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/tomasvrba.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/tomasvrba.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/tomasvrba.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/tomasvrba.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/tomasvrba.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06884 — Квантово-уязвимый ключ RSA (3072-bit) в releases/pubkeys/userofreddit44.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/userofreddit44.asc#line 1`
- Источник данных: releases/pubkeys/userofreddit44.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 3072-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/userofreddit44.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/userofreddit44.asc · line 1 · SHA-256 315636b2f7e00661811d8d8feee53223db00c9277ae1194dcaf9d4fb25bf6194_

```
OpenPGP primary key: algorithm ID 1 (RSA) 3072-bit
```

_key · releases/pubkeys/userofreddit44.asc · line 1 · SHA-256 6ccbdce52e43463e8b282489a66bb4553923cec099cc342f213f584e97c81df4_

```
OpenPGP subkey: algorithm ID 1 (RSA) 3072-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06885 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/x1ddos.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/x1ddos.asc#line 1`
- Источник данных: releases/pubkeys/x1ddos.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/x1ddos.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/x1ddos.asc · line 1 · SHA-256 18fb5f0b9bd19412cb5c0404d29bd26dc62ba6e0ff99543463ebc0757b50ef09_

```
OpenPGP primary key: algorithm ID 1 (RSA) 4096-bit
```

_key · releases/pubkeys/x1ddos.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06886 — Квантово-уязвимый ключ RSA (2048-bit) в releases/pubkeys/x1ddos.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/x1ddos.asc#line 1`
- Источник данных: releases/pubkeys/x1ddos.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 2048-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/x1ddos.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/x1ddos.asc · line 1 · SHA-256 a744425426415d58dbeef862a6f1d8bcf6b00820639c8784270363d0b6330969_

```
OpenPGP subkey: algorithm ID 1 (RSA) 2048-bit
```

_key · releases/pubkeys/x1ddos.asc · line 1 · SHA-256 a744425426415d58dbeef862a6f1d8bcf6b00820639c8784270363d0b6330969_

```
OpenPGP subkey: algorithm ID 1 (RSA) 2048-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06887 — Квантово-уязвимый ключ RSA (3072-bit) в releases/pubkeys/x1ddos.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/x1ddos.asc#line 1`
- Источник данных: releases/pubkeys/x1ddos.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 3072-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/x1ddos.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/x1ddos.asc · line 1 · SHA-256 6ccbdce52e43463e8b282489a66bb4553923cec099cc342f213f584e97c81df4_

```
OpenPGP subkey: algorithm ID 1 (RSA) 3072-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06888 — Квантово-уязвимый ключ Ed25519 (Ed25519) в releases/pubkeys/yaziza.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/yaziza.asc#line 1`
- Источник данных: releases/pubkeys/yaziza.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ Ed25519 Ed25519 (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/yaziza.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/yaziza.asc · line 1 · SHA-256 6dbf836a10cb57142effcc3f89dd5e74340870bac059dd57e9f528bf344e8db8_

```
OpenPGP primary key: algorithm ID 22 (Ed25519) Ed25519
```

_key · releases/pubkeys/yaziza.asc · line 1 · SHA-256 065d4edee7f1048b4c864ef703528e93278d15340d378d5c518a3b27a7094692_

```
OpenPGP subkey: algorithm ID 22 (Ed25519) Ed25519
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06889 — Квантово-уязвимый ключ RSA (4096-bit) в releases/pubkeys/yaziza.asc

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:releases/pubkeys/yaziza.asc#line 1`
- Источник данных: releases/pubkeys/yaziza.asc
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ RSA 4096-bit (строка 1).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 1 в предоставленном файле releases/pubkeys/yaziza.asc и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · releases/pubkeys/yaziza.asc · line 1 · SHA-256 484f2172c4dd53b29fd23e321304b308266950550fb37c83431470e8045649f0_

```
OpenPGP subkey: algorithm ID 1 (RSA) 4096-bit
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06896 — Квантово-уязвимый ключ ECDSA (secp256r1) в external/cryptoauthlib/app/pkcs11/README.md

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:external/cryptoauthlib/app/pkcs11/README.md#line 280`
- Источник данных: external/cryptoauthlib/app/pkcs11/README.md
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ ECDSA secp256r1 (строка 280).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 280 в предоставленном файле external/cryptoauthlib/app/pkcs11/README.md и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · external/cryptoauthlib/app/pkcs11/README.md · line 280 · SHA-256 87a3decbb47c307b59a5585db9eecff49e5997a1eb7350dbfae08a97c0f3fa07_

```
ECDSA public key, secp256r1
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-06915 — idna 3.4 затронут GHSA-65pc-fj4g-8rjx (CVE-2026-45409, PYSEC-2026-215)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/idna@3.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-65pc-fj4g-8rjx (CVE-2026-45409, PYSEC-2026-215) для пакета PyPI idna версии 3.4: Internationalized Domain Names in Applications (IDNA): Specially crafted inputs to idna.encode() can bypass CVE-2024-3651 fix. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-65pc-fj4g-8rjx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-65pc-fj4g-8rjx](https://osv.dev/vulnerability/GHSA-65pc-fj4g-8rjx) · line 22 · SHA-256 1b180b3ab94317455b5be8428a3b6ed5d0f401ab156e3fc18e2d9b9849857b58_

```
{"id": "GHSA-65pc-fj4g-8rjx", "aliases": ["CVE-2026-45409", "PYSEC-2026-215"], "modified": "2026-09-10T03:50:45.700124422Z", "summary": "Internationalized Domain Names in Applications (IDNA): Specially crafted inputs to idna.encode() can bypass CVE-2024-3651 fix", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.15).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06916 — idna 3.4 затронут GHSA-jjg7-2v4v-x38h (CVE-2024-3651, PYSEC-2024-60)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/idna@3.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 6.2 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-jjg7-2v4v-x38h (CVE-2024-3651, PYSEC-2024-60) для пакета PyPI idna версии 3.4: Internationalized Domain Names in Applications (IDNA) vulnerable to denial of service from specially crafted inputs to idna.encode. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-jjg7-2v4v-x38h
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-jjg7-2v4v-x38h](https://osv.dev/vulnerability/GHSA-jjg7-2v4v-x38h) · line 22 · SHA-256 b260da6fe71df346fc2fbff5eb48b5cd290f2fcaa442b8e591d4cd0cb116bbb1_

```
{"id": "GHSA-jjg7-2v4v-x38h", "aliases": ["CVE-2024-3651", "PYSEC-2024-60"], "modified": "2026-09-10T03:50:12.774088619Z", "summary": "Internationalized Domain Names in Applications (IDNA) vulnerable to denial of service from specially crafted inputs to idna.encode", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06917 — jinja2 3.1.2 затронут GHSA-cpwx-vrp4-4pq7 (CVE-2025-27516, PYSEC-2026-1471)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/jinja2@3.1.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-cpwx-vrp4-4pq7 (CVE-2025-27516, PYSEC-2026-1471) для пакета PyPI jinja2 версии 3.1.2: Jinja2 vulnerable to sandbox breakout through attr filter selecting format method. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-cpwx-vrp4-4pq7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-cpwx-vrp4-4pq7](https://osv.dev/vulnerability/GHSA-cpwx-vrp4-4pq7) · line 28 · SHA-256 e28b14906d20d0da1a5a90a9cd8900c0e9f3f8e617101292dbb5c6bedb863524_

```
{"id": "GHSA-cpwx-vrp4-4pq7", "aliases": ["CVE-2025-27516", "PYSEC-2026-1471"], "modified": "2026-09-10T03:49:48.526758681Z", "summary": "Jinja2 vulnerable to sandbox breakout through attr filter selecting format method", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.1.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06919 — jinja2 3.1.2 затронут GHSA-h5c8-rqwp-cp95 (CVE-2024-22195, PYSEC-2026-1473)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/jinja2@3.1.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 5.4 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-h5c8-rqwp-cp95 (CVE-2024-22195, PYSEC-2026-1473) для пакета PyPI jinja2 версии 3.1.2: Jinja vulnerable to HTML attribute injection when passing user input as keys to xmlattr filter. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-h5c8-rqwp-cp95
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-h5c8-rqwp-cp95](https://osv.dev/vulnerability/GHSA-h5c8-rqwp-cp95) · line 28 · SHA-256 3bcb93126b62e63f1ce99f0dbbef076e72a4be50e744eb19c8c285de5787f69a_

```
{"id": "GHSA-h5c8-rqwp-cp95", "aliases": ["CVE-2024-22195", "PYSEC-2026-1473"], "modified": "2026-09-10T03:50:00.236017440Z", "summary": "Jinja vulnerable to HTML attribute injection when passing user input as keys to xmlattr filter", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.1.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06920 — jinja2 3.1.2 затронут GHSA-h75v-3vvj-5mfj (CVE-2024-34064, PYSEC-2026-1474)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/jinja2@3.1.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 5.4 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-h75v-3vvj-5mfj (CVE-2024-34064, PYSEC-2026-1474) для пакета PyPI jinja2 версии 3.1.2: Jinja vulnerable to HTML attribute injection when passing user input as keys to xmlattr filter. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-h75v-3vvj-5mfj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-h75v-3vvj-5mfj](https://osv.dev/vulnerability/GHSA-h75v-3vvj-5mfj) · line 28 · SHA-256 8d178561724d57b3a1b58e1376ccee532051838cf1bd2f1b097a503006be4129_

```
{"id": "GHSA-h75v-3vvj-5mfj", "aliases": ["CVE-2024-34064", "PYSEC-2026-1474"], "modified": "2026-09-10T03:50:13.786450101Z", "summary": "Jinja vulnerable to HTML attribute injection when passing user input as keys to xmlattr filter", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.1.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06923 — pygments 2.14.0 затронут GHSA-mrwq-x4v8-fh7p (CVE-2022-40896, PYSEC-2023-117)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/pygments@2.14.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 5.5 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-mrwq-x4v8-fh7p (CVE-2022-40896, PYSEC-2023-117) для пакета PyPI pygments версии 2.14.0: Pygments vulnerable to ReDoS. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mrwq-x4v8-fh7p
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mrwq-x4v8-fh7p](https://osv.dev/vulnerability/GHSA-mrwq-x4v8-fh7p) · line 34 · SHA-256 6da07c6d923c992526545174c0d85c361cfb51e714fe54fb739d059ae2356ae4_

```
{"id": "GHSA-mrwq-x4v8-fh7p", "aliases": ["CVE-2022-40896", "PYSEC-2023-117"], "modified": "2024-10-24T22:27:47.389299Z", "summary": "Pygments vulnerable to ReDoS", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.15.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06924 — requests 2.28.2 затронут GHSA-9hjg-9r4m-mvj7 (CVE-2024-47081, PYSEC-2026-1872)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/requests@2.28.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-9hjg-9r4m-mvj7 (CVE-2024-47081, PYSEC-2026-1872) для пакета PyPI requests версии 2.28.2: Requests vulnerable to .netrc credentials leak via malicious URLs. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9hjg-9r4m-mvj7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9hjg-9r4m-mvj7](https://osv.dev/vulnerability/GHSA-9hjg-9r4m-mvj7) · line 36 · SHA-256 54566624d8668e64e97057d595c41cb500bb80cf1058002a3401dbcedc46f106_

```
{"id": "GHSA-9hjg-9r4m-mvj7", "aliases": ["CVE-2024-47081", "PYSEC-2026-1872"], "modified": "2026-10-19T20:00:04.716114530Z", "summary": "Requests vulnerable to .netrc credentials leak via malicious URLs", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.32.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06925 — requests 2.28.2 затронут GHSA-9wx4-h78v-vm56 (CVE-2024-35195, PYSEC-2026-1873)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/requests@2.28.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 5.6 (`CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-9wx4-h78v-vm56 (CVE-2024-35195, PYSEC-2026-1873) для пакета PyPI requests версии 2.28.2: Requests `Session` object does not verify requests after making first request with verify=False. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9wx4-h78v-vm56
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9wx4-h78v-vm56](https://osv.dev/vulnerability/GHSA-9wx4-h78v-vm56) · line 36 · SHA-256 38975a9d04ed33a4ee36cb1327ae63c2711a85bbd849c980a35cf0b0daa8b384_

```
{"id": "GHSA-9wx4-h78v-vm56", "aliases": ["CVE-2024-35195", "PYSEC-2026-1873"], "modified": "2026-09-10T03:50:13.740879755Z", "summary": "Requests `Session` object does not verify requests after making first request with verify=False", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:H/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.32.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06926 — requests 2.28.2 затронут GHSA-gc5v-m9x4-r6x2 (CVE-2026-25645, PYSEC-2026-2275)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/requests@2.28.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 4.4 (`CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-gc5v-m9x4-r6x2 (CVE-2026-25645, PYSEC-2026-2275) для пакета PyPI requests версии 2.28.2: Requests has Insecure Temp File Reuse in its extract_zipped_paths() utility function. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-gc5v-m9x4-r6x2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-gc5v-m9x4-r6x2](https://osv.dev/vulnerability/GHSA-gc5v-m9x4-r6x2) · line 36 · SHA-256 f74704bb5c636714db99ca4783e4a2b3be4ccd7fe7421013ca903d4c418bcc13_

```
{"id": "GHSA-gc5v-m9x4-r6x2", "aliases": ["CVE-2026-25645", "PYSEC-2026-2275"], "modified": "2026-09-10T03:50:39.207922076Z", "summary": "Requests has Insecure Temp File Reuse in its extract_zipped_paths() utility function", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:U/C:N/I:H/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.33.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06927 — requests 2.28.2 затронут GHSA-j8r2-6x86-q33q (CVE-2023-32681, PYSEC-2023-74)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/requests@2.28.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 6.1 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-j8r2-6x86-q33q (CVE-2023-32681, PYSEC-2023-74) для пакета PyPI requests версии 2.28.2: Unintended leak of Proxy-Authorization header in requests. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j8r2-6x86-q33q
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j8r2-6x86-q33q](https://osv.dev/vulnerability/GHSA-j8r2-6x86-q33q) · line 36 · SHA-256 913766f1fff73012784b74cfa767f1c83b6cd5ccb2339129a2df5bdc554b643f_

```
{"id": "GHSA-j8r2-6x86-q33q", "aliases": ["CVE-2023-32681", "PYSEC-2023-74"], "modified": "2026-09-10T03:50:01.756149727Z", "summary": "Unintended leak of Proxy-Authorization header in requests", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:C/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.31.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06929 — urllib3 1.26.15 затронут GHSA-34jh-p97f-mpxf (CVE-2024-37891, PYSEC-2026-1995)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/urllib3@1.26.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 4.4 (`CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-34jh-p97f-mpxf (CVE-2024-37891, PYSEC-2026-1995) для пакета PyPI urllib3 версии 1.26.15: urllib3's Proxy-Authorization request header isn't stripped during cross-origin redirects. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-34jh-p97f-mpxf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-34jh-p97f-mpxf](https://osv.dev/vulnerability/GHSA-34jh-p97f-mpxf) · line 60 · SHA-256 70e2b3135eba6c4126c184770467f1dd8b42cba4057694f5cae8217b50efdc85_

```
{"id": "GHSA-34jh-p97f-mpxf", "aliases": ["CVE-2024-37891", "PYSEC-2026-1995"], "modified": "2026-09-10T03:50:14.811193644Z", "summary": "urllib3's Proxy-Authorization request header isn't stripped during cross-origin redirects", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.26.19, 2.2.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06932 — urllib3 1.26.15 затронут GHSA-g4mx-q9vg-27p4 (CVE-2023-45803, PYSEC-2023-212)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/urllib3@1.26.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 4.2 (`CVSS:3.1/AV:A/AC:H/PR:H/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-g4mx-q9vg-27p4 (CVE-2023-45803, PYSEC-2023-212) для пакета PyPI urllib3 версии 1.26.15: urllib3's request body not stripped after redirect from 303 status changes request method to GET. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-g4mx-q9vg-27p4
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-g4mx-q9vg-27p4](https://osv.dev/vulnerability/GHSA-g4mx-q9vg-27p4) · line 60 · SHA-256 9068d64596de74c3e90b47341a42014cea57c6cc121e804ce5fd84ce40b51bd3_

```
{"id": "GHSA-g4mx-q9vg-27p4", "aliases": ["CVE-2023-45803", "PYSEC-2023-212"], "modified": "2026-09-10T03:50:03.706889410Z", "summary": "urllib3's request body not stripped after redirect from 303 status changes request method to GET", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:A/AC:H/PR:H/UI:N/S:U/C:H/I:N/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:A/AC:L/AT:P/PR:H/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.26.18, 2.0.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06934 — urllib3 1.26.15 затронут GHSA-pq67-6m6q-mj2v (CVE-2025-50181, PYSEC-2026-1999)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/urllib3@1.26.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-pq67-6m6q-mj2v (CVE-2025-50181, PYSEC-2026-1999) для пакета PyPI urllib3 версии 1.26.15: urllib3 redirects are not disabled when retries are disabled on PoolManager instantiation. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pq67-6m6q-mj2v
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pq67-6m6q-mj2v](https://osv.dev/vulnerability/GHSA-pq67-6m6q-mj2v) · line 60 · SHA-256 788a2cf91f9eaf45aa98c3450fb81db5550fdc6d8ec5c3a2e0f8be882fa8d4e1_

```
{"id": "GHSA-pq67-6m6q-mj2v", "aliases": ["CVE-2025-50181", "PYSEC-2026-1999"], "modified": "2026-09-10T03:50:25.299291456Z", "summary": "urllib3 redirects are not disabled when retries are disabled on PoolManager instantiation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.5.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06935 — urllib3 1.26.15 затронут GHSA-qccp-gfcp-xxvc (CVE-2026-44431, PYSEC-2026-141)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/urllib3@1.26.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-qccp-gfcp-xxvc (CVE-2026-44431, PYSEC-2026-141) для пакета PyPI urllib3 версии 1.26.15: urllib3: Sensitive headers forwarded across origins in proxied low-level redirects. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qccp-gfcp-xxvc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qccp-gfcp-xxvc](https://osv.dev/vulnerability/GHSA-qccp-gfcp-xxvc) · line 60 · SHA-256 c7033c35f2861e3d21a7968a87a6a0bb5131d057bb7ab67da86828d47241bac6_

```
{"id": "GHSA-qccp-gfcp-xxvc", "aliases": ["CVE-2026-44431", "PYSEC-2026-141"], "modified": "2026-09-10T03:50:47.272765640Z", "summary": "urllib3: Sensitive headers forwarded across origins in proxied low-level redirects", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.7.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06936 — urllib3 1.26.15 затронут GHSA-v845-jxx5-vc9f (CVE-2023-43804, PYSEC-2023-192)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/urllib3@1.26.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-v845-jxx5-vc9f (CVE-2023-43804, PYSEC-2023-192) для пакета PyPI urllib3 версии 1.26.15: `Cookie` HTTP header isn't stripped on cross-origin redirects. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-v845-jxx5-vc9f
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-v845-jxx5-vc9f](https://osv.dev/vulnerability/GHSA-v845-jxx5-vc9f) · line 60 · SHA-256 4436cbacc6451b228d4eb5436fea1a53cd8e207e7f17bde22899e1323c5f0fb6_

```
{"id": "GHSA-v845-jxx5-vc9f", "aliases": ["CVE-2023-43804", "PYSEC-2023-192"], "modified": "2026-09-10T03:49:24.753610811Z", "summary": "`Cookie` HTTP header isn't stripped on cross-origin redirects", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:H/I:H/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:H/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.26.17, 2.0.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06938 — zipp 3.15.0 затронут GHSA-jfmj-5v4g-7637 (CVE-2024-5569, PYSEC-2026-2074)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/zipp@3.15.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 6.2 (`CVSS:3.0/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-jfmj-5v4g-7637 (CVE-2024-5569, PYSEC-2026-2074) для пакета PyPI zipp версии 3.15.0: zipp Denial of Service vulnerability. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-jfmj-5v4g-7637
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-jfmj-5v4g-7637](https://osv.dev/vulnerability/GHSA-jfmj-5v4g-7637) · line 62 · SHA-256 27a0d57ee49a9e56ef66b7abab8b3aca4800e47d4fb3cae8962ba129790e3ec9_

```
{"id": "GHSA-jfmj-5v4g-7637", "aliases": ["CVE-2024-5569", "PYSEC-2026-2074"], "modified": "2026-09-10T03:49:18.747455573Z", "summary": "zipp Denial of Service vulnerability", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.0/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.19.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06891 — Квантово-уязвимый ECDSA: проверка прошивки и загрузки (корень доверия) (3 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Затронутый актив: `source-code:ECDSA:root_of_trust`
- Источник данных: src/bootloader/bootloader.c
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 43.4 / 100
- CVSS v3.1: неприменимо

7 упоминаний ECDSA в 3 файл(ах), например src/bootloader/bootloader.c:537. Роль по путям, именам функций и соседнему коду: проверка прошивки и загрузки (корень доверия). Эти открытые ключи зашиты в загрузчик или устройство: с криптографически значимым квантовым компьютером (CRQC) злоумышленник подделает подпись прошивки, а замена ключей требует обновления загрузчика на устройствах в поле.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/bootloader/bootloader.c:537 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/bootloader/bootloader.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/bootloader/bootloader.c#L537) · line 537 · SHA-256 a692ec93e05c715e251b70d5df1203b876ed7d82bd28e9c6b1c10a24cdb7c3d9_

```
  536 |         // First is sanity check
  537 |         if (pukcc_ecdsa_verify(_root_pubkeys[i], sig, random, sizeof(random), curve_p256) != 0) {
  538 |             if (pukcc_ecdsa_verify(_root_pubkeys[i], sig, hash, sizeof(hash), curve_p256) == 0) {
```

_file_excerpt · [src/bootloader/bootloader.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/bootloader/bootloader.c#L538) · line 538 · SHA-256 c8910947b0750cbb6c7959f9780e84bfbe3cd04a9d2bb09cbbf7cc1ab9daef34_

```
  537 |         if (pukcc_ecdsa_verify(_root_pubkeys[i], sig, random, sizeof(random), curve_p256) != 0) {
  538 |             if (pukcc_ecdsa_verify(_root_pubkeys[i], sig, hash, sizeof(hash), curve_p256) == 0) {
  539 |                 valid++;
```

_file_excerpt · [src/bootloader/bootloader.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/bootloader/bootloader.c#L609) · line 609 · SHA-256 110ab61f5a0020b335e42ad45c11bc760596590d7806f6ab45ae8af2068235cd_

```
  608 |         // First is sanity check
  609 |         if (pukcc_ecdsa_verify(pubkey, sig, random, sizeof(random), curve_p256) != 0) {
  610 |             if (pukcc_ecdsa_verify(pubkey, sig, hash, sizeof(hash), curve_p256) == 0) {
```

_file_excerpt · [src/bootloader/stage0/stage1_sigcheck.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/bootloader/stage0/stage1_sigcheck.c#L165) · line 165 · SHA-256 40465ea406a87913706627f03d6592256e6307cc6510acfb3fd097deefc1140b_

```
  164 |         const size_t signature_offset = (size_t)key_idx * BB02_STAGE1_SIGNATURE_LEN;
  165 |         const uint8_t valid = _is_zero_u8(pukcc_ecdsa_verify(
  166 |             pubkeys[key_idx],
```

_file_excerpt · [src/rust/bitbox02-rust-c/src/firmware_c_api.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust-c/src/firmware_c_api.rs#L23) · line 23 · SHA-256 0239908a79adffb8db0de707bb0d8d79652f9eee0c4c289c416254e3f87e156a_

```
   22 |     let mut hal = crate::HalImpl::new();
   23 |     util::bb02_async::block_on(bitbox02_rust::secp256k1::init(&mut hal))
   24 |         .expect("secp256k1 context initialization failed");
```

_file_excerpt · [src/rust/bitbox02-rust-c/src/firmware_c_api.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust-c/src/firmware_c_api.rs#L24) · line 24 · SHA-256 d2c149057a83a51f66f258261f3e75f6e5d333f7e7cf8e4fb0e01a56de1f4257_

```
   23 |     util::bb02_async::block_on(bitbox02_rust::secp256k1::init(&mut hal))
   24 |         .expect("secp256k1 context initialization failed");
   25 |     bitbox02_rust::main_loop::main_loop(&mut hal)
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Запланируйте гибридную подпись прошивки (классическая плюс ML-DSA или SLH-DSA, обе обязательны) и способ доставить новые ключи обновлением загрузчика.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06893 — Квантово-уязвимый X25519: обёртка ключей и шифрование хранимых данных (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Затронутый актив: `source-code:X25519:key_wrapping`
- Источник данных: src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 43.4 / 100
- CVSS v3.1: неприменимо

4 упоминаний X25519 в 1 файл(ах), например src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:15. Роль по путям, именам функций и соседнему коду: обёртка ключей и шифрование хранимых данных. Ключи или данные, зашифрованные на эти открытые ключи, хранятся: кто скопирует их сейчас, расшифрует, когда появится CRQC («собери сейчас — расшифруй потом»).

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:15 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs#L15) · line 15 · SHA-256 1c153d0b1adf9cd8ecf03da5502f8e68db447b4ab09e5e61188fc538699029d9_

```
   14 | use sha2::{Digest, Sha256};
   15 | use x25519_dalek::{PublicKey as X25519PublicKey, StaticSecret as X25519StaticSecret};
   16 | use zeroize::{Zeroize, Zeroizing};
```

_file_excerpt · [src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs#L19) · line 19 · SHA-256 4b67afd4d285deeff00b1d8a4e6ef086fbb387cad74ce1646456a0830671584e_

```
   18 | const AUTH_SEED_LABEL: &[u8] = b"bitboxsync-auth-ed25519-seed-v1";
   19 | const WRAP_SEED_LABEL: &[u8] = b"bitboxsync-wrap-x25519-seed-v1";
   20 | 
```

_file_excerpt · [src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs#L60) · line 60 · SHA-256 f8ee14a435cd94f2c3694c380ab36b8cca17c6d237875854295e567d7ab0e0ef_

```
   59 |     let wrap_secret = [REDACTED]
   60 |     let wrap_public_key = X25519PublicKey::from(&wrap_secret).to_bytes();
   61 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Оборачивайте ключи ML-KEM или гибридным KEM (X25519 + ML-KEM-768) и переоберните хранимые ключи; для данных, которые уже могли скопировать, нужна отдельная оценка.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06898 — Квантово-уязвимый ECDH: обёртка ключей и шифрование хранимых данных (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Затронутый актив: `source-code:ECDH:key_wrapping`
- Источник данных: external/cryptoauthlib/python/cryptoauthlib/atcab.py
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 43.4 / 100
- CVSS v3.1: неприменимо

23 упоминаний ECDH в 1 файл(ах), например external/cryptoauthlib/python/cryptoauthlib/atcab.py:974. Роль по путям, именам функций и соседнему коду: обёртка ключей и шифрование хранимых данных. Ключи или данные, зашифрованные на эти открытые ключи, хранятся: кто скопирует их сейчас, расшифрует, когда появится CRQC («собери сейчас — расшифруй потом»).

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте external/cryptoauthlib/python/cryptoauthlib/atcab.py:974 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [external/cryptoauthlib/python/cryptoauthlib/atcab.py](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/cryptoauthlib/python/cryptoauthlib/atcab.py#L974) · line 974 · SHA-256 87004ff616be22235a821a5c8d5b9ead791c529f62209f2bc0cea638b486c206_

```
  973 |     """
  974 |     Base function for generating premaster secret key using ECDH.
  975 | 
```

_file_excerpt · [external/cryptoauthlib/python/cryptoauthlib/atcab.py](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/cryptoauthlib/python/cryptoauthlib/atcab.py#L977) · line 977 · SHA-256 8e5f1c528fbe7b2ee242f9afec3b53fc230249d43b130247f4590ed07951b297_

```
  976 |     Args:
  977 |         mode                Mode to be used for ECDH computation (int)
  978 |         key_id              Slot of key for ECDH computation (int)
```

_file_excerpt · [external/cryptoauthlib/python/cryptoauthlib/atcab.py](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/cryptoauthlib/python/cryptoauthlib/atcab.py#L978) · line 978 · SHA-256 204aab89e32c109386818d0b5149a61c7c3ce73f3684eb12b5709f32b09a5a47_

```
  977 |         mode                Mode to be used for ECDH computation (int)
  978 |         key_id              Slot of key for ECDH computation (int)
  979 |         public_key          Public key input to ECDH calculation. X and Y
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Оборачивайте ключи ML-KEM или гибридным KEM (X25519 + ML-KEM-768) и переоберните хранимые ключи; для данных, которые уже могли скопировать, нужна отдельная оценка.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06863 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (14 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: py/bitbox02/bitbox02/bitbox02/secp256k1.py
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

50 упоминаний ECDSA в 14 файл(ах), например py/bitbox02/bitbox02/bitbox02/secp256k1.py:3. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте py/bitbox02/bitbox02/bitbox02/secp256k1.py:3 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [py/bitbox02/bitbox02/bitbox02/secp256k1.py](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/py/bitbox02/bitbox02/bitbox02/secp256k1.py#L3) · line 3 · SHA-256 f1b7aa46e3d0b50c48a6a1863e881efc3f3599b1f51734acef93ab966ea7b144_

```
    2 | 
    3 | """secp256k1 util functions"""
    4 | import hashlib
```

_file_excerpt · [src/rust/bitbox-secp256k1/build.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/build.rs#L6) · line 6 · SHA-256 c0e8a8076dd2e70e550d1aa3c11d2672989702f68a84802e08636e784b6d41f8_

```
    5 | fn main() {
    6 |     let secp_dir = PathBuf::from("depend/secp256k1-zkp");
    7 |     let callbacks = PathBuf::from("src/default_callbacks.c");
```

_file_excerpt · [src/rust/bitbox-secp256k1/build.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/build.rs#L18) · line 18 · SHA-256 25e9545e63d24ed02198281c8da70ca8d5106db13c770d3cb0563ef91611ce31_

```
   17 |     build
   18 |         .file(secp_dir.join("src/secp256k1.c"))
   19 |         .file(secp_dir.join("src/precomputed_ecmult.c"))
```

_file_excerpt · [src/rust/bitbox-secp256k1/build.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/build.rs#L37) · line 37 · SHA-256 47d7abfe9efe1b2bea40a263634d29da5de554eb838641f36186b8d302876eb6_

```
   36 | 
   37 |     build.compile("secp256k1");
   38 | }
```

_file_excerpt · [src/rust/bitbox-secp256k1/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/src/lib.rs#L7) · line 7 · SHA-256 27351363967fb644277306e8bdedc7dfa7e9c4e0d23be03ec2a3b056ce0f7cc5_

```
    6 | 
    7 | pub use bitcoin::secp256k1::constants::PUBLIC_KEY_SIZE;
    8 | use bitcoin::secp256k1::ffi::CPtr;
```

_file_excerpt · [src/rust/bitbox-secp256k1/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/src/lib.rs#L8) · line 8 · SHA-256 1ae312353045cae568e231b036e3b831f53cd99c54b61952e50f75cec17b70c2_

```
    7 | pub use bitcoin::secp256k1::constants::PUBLIC_KEY_SIZE;
    8 | use bitcoin::secp256k1::ffi::CPtr;
    9 | use bitcoin::secp256k1::{All, Secp256k1};
```

_file_excerpt · [src/rust/bitbox-secp256k1/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-secp256k1/src/lib.rs#L9) · line 9 · SHA-256 63fd03f40121775b3740c6e1e00a3eb82337e0d734dfcffdce1ec08de5c178be_

```
    8 | use bitcoin::secp256k1::ffi::CPtr;
    9 | use bitcoin::secp256k1::{All, Secp256k1};
   10 | 
```

_file_excerpt · [src/rust/bitbox02-rust-c/src/secp256k1.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust-c/src/secp256k1.rs#L3) · line 3 · SHA-256 32c3110f30785a45f30291b04aaed8f855161da3b48a5d627b55bb9cc2e4bb52_

```
    2 | 
    3 | use bitcoin::secp256k1::{
    4 |     Message, PublicKey,
```

_file_excerpt · [src/rust/bitbox02-rust-c/src/secp256k1.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust-c/src/secp256k1.rs#L42) · line 42 · SHA-256 26f131e03c434e4bb99270182a8393193a714d40ef826c5534f8f5a3ef76c862_

```
   41 |     let Ok(signature) =
   42 |         bitcoin::secp256k1::ecdsa::Signature::from_compact(signature_compact.as_ref())
   43 |     else {
```

_file_excerpt · [src/rust/bitbox02-rust-c/src/secp256k1.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust-c/src/secp256k1.rs#L56) · line 56 · SHA-256 bf55765f36e34101d8c06c2f514fa6a3aabb581d93221c944b40863ae1e4a428_

```
   55 |     unsafe {
   56 |         ffi::secp256k1_ecdsa_verify(
   57 |             ffi::secp256k1_context_no_precomp,
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06892 — Квантово-уязвимый X25519: обмен ключами в канале (TLS, Noise, рукопожатия) (5 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Затронутый актив: `source-code:X25519:channel`
- Источник данных: src/rust/bitbox-noise/src/lib.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

11 упоминаний X25519 в 5 файл(ах), например src/rust/bitbox-noise/src/lib.rs:16. Роль по путям, именам функций и соседнему коду: обмен ключами в канале (TLS, Noise, рукопожатия). Трафик под этим обменом ключами можно записать сейчас и расшифровать позже; гибридный обмен сохраняет классические гарантии и добавляет постквантовые.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/rust/bitbox-noise/src/lib.rs:16 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/rust/bitbox-noise/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-noise/src/lib.rs#L16) · line 16 · SHA-256 bec1cc899b2ee57631342068081612e177c1e131b0062f84dbf4bd19b81f7b9e_

```
   15 | pub mod testing;
   16 | mod x25519;
   17 | 
```

_file_excerpt · [src/rust/bitbox-noise/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-noise/src/lib.rs#L19) · line 19 · SHA-256 57cd8f7157563d1d7dcdedce2582f83213eb268d9f974d8d82700859104ba8c2_

```
   18 | pub use noise_xx::{Error, HandshakeHash, HandshakeResult, State};
   19 | pub use x25519::{X25519, genkey};
   20 | 
```

_file_excerpt · [src/rust/bitbox-noise/src/noise_xx.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-noise/src/noise_xx.rs#L8) · line 8 · SHA-256 784affd9139fdfbf69bb890deb430326b00ccb48a47de6340bd5071c807628b4_

```
    7 | 
    8 | use crate::x25519::{PrivateKey, PublicKey, X25519, genkey};
    9 | use noise_rust_crypto::{ChaCha20Poly1305, Sha256, sensitive::Sensitive};
```

_file_excerpt · [src/rust/bitbox-noise/src/x25519.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-noise/src/x25519.rs#L49) · line 49 · SHA-256 43d70ab747c41c47e17b5ba00fdf0933116113165cc5310d5e74f3736664266f_

```
   48 |     fn pubkey(k: &Self::Key) -> Self::Pubkey {
   49 |         let static_secret = [REDACTED]
   50 |         *x25519_dalek::PublicKey::from(&static_secret).as_bytes()
```

_file_excerpt · [src/rust/bitbox-noise/src/x25519.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-noise/src/x25519.rs#L54) · line 54 · SHA-256 fae4ff917820e0219e7ac326306ae796207dce8f7af4ff5e75fd4328d8d0eaee_

```
   53 |     fn dh(k: &Self::Key, pk: &Self::Pubkey) -> Result<Self::Output, ()> {
   54 |         let k = x25519_dalek::StaticSecret::from(*k.deref());
   55 |         let pk = x25519_dalek::PublicKey::from(*pk);
```

_file_excerpt · [src/rust/bitbox-noise/src/x25519.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox-noise/src/x25519.rs#L55) · line 55 · SHA-256 9cb9b67a0b6ccdefe882b0cd12a8a8e62cc7886bd8c3fa9cc44154fd180c819c_

```
   54 |         let k = x25519_dalek::StaticSecret::from(*k.deref());
   55 |         let pk = x25519_dalek::PublicKey::from(*pk);
   56 |         Ok(*k.diffie_hellman(&pk).as_bytes())
```

_file_excerpt · [external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/everest.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/everest.h#L25) · line 25 · SHA-256 805839a03b00bfe936a91234a33a359e26d3cc0294734ba3ffba86e04622b9f6_

```
   24 | 
   25 | #include "everest/x25519.h"
   26 | 
```

_file_excerpt · [external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/x25519.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/x25519.c#L35) · line 35 · SHA-256 9ca103a64c6b7d9f9370997f71d0b11e98331c8e1228627873d68b532b073c3c_

```
   34 | 
   35 | #include "x25519.h"
   36 | 
```

_file_excerpt · [external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/x25519.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/x25519.c#L81) · line 81 · SHA-256 fbaaec05ef452c03ec3e2c812b4b680704b7c7a0f16e42a0ef9052897222cd03_

```
   80 |     base[0] = 9;
   81 |     Hacl_Curve25519_crypto_scalarmult( buf, ctx->our_secret, base );
   82 | 
```

_file_excerpt · [external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/x25519.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/x25519.c#L134) · line 134 · SHA-256 21b4c7046cce778fb5b5fd9cc64b7a419ba11a10d999477df74ff1d62ee0bc60_

```
  133 | 
  134 |     Hacl_Curve25519_crypto_scalarmult( buf, ctx->our_secret, ctx->peer_point);
  135 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Переведите рукопожатие на гибридный обмен ключами (X25519MLKEM768 в TLS 1.3; гибридный KEM в протоколах на основе Noise).

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06895 — Квантово-уязвимый Ed25519: подпись транзакций и сообщений (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Затронутый актив: `source-code:Ed25519:transaction_signing`
- Источник данных: src/rust/bitbox02-rust/src/keystore/ed25519.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

2 упоминаний Ed25519 в 1 файл(ах), например src/rust/bitbox02-rust/src/keystore/ed25519.rs:10. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/rust/bitbox02-rust/src/keystore/ed25519.rs:10 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/rust/bitbox02-rust/src/keystore/ed25519.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust/src/keystore/ed25519.rs#L10) · line 10 · SHA-256 0d1f71033a48c3c6e0b8363e9a41c2f5e9ee07f08735238e9856e64b2125dfbc_

```
    9 | use digest::Digest;
   10 | use ed25519_dalek::VerifyingKey;
   11 | use ed25519_dalek::hazmat::{ExpandedSecretKey, raw_sign};
```

_file_excerpt · [src/rust/bitbox02-rust/src/keystore/ed25519.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust/src/keystore/ed25519.rs#L11) · line 11 · SHA-256 449e9e250d19db94ff94019815e29a47323da4b3df842285684544d908651dd6_

```
   10 | use ed25519_dalek::VerifyingKey;
   11 | use ed25519_dalek::hazmat::{ExpandedSecretKey, raw_sign};
   12 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06862 — Квантово-уязвимый ECDSA: роль не определена (10 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Role resolved for all six files, and they are three different roles rather than one. src/pukcc/pukcc.c:181 is pukcc_ecdsa_verify, the ATSAM PUKCC hardware public-key controller performing ECDSA *verification* — the bootloader's signature check, so a root-of-trust item, and verification uses public keys only, which puts it outside any timing concern. src/rust/streaming-silent-payments/{lib,hash}.rs is BIP-352 silent payments, i.e. address derivation on secp256k1. src/rust/util/src/p256.rs is the U2F/FIDO P-256 signing described in the crypto-bigint decision above. Each has a different migration deadline, which is why leaving them merged as "role not determined" would be the wrong input to a plan.
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: py/bitbox02/bitbox02/bitbox02/bitbox02.py
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 40.2 / 100
- CVSS v3.1: неприменимо

20 упоминаний ECDSA в 10 файл(ах), например py/bitbox02/bitbox02/bitbox02/bitbox02.py:21. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте py/bitbox02/bitbox02/bitbox02/bitbox02.py:21 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [py/bitbox02/bitbox02/bitbox02/bitbox02.py](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/py/bitbox02/bitbox02/bitbox02/bitbox02.py#L21) · line 21 · SHA-256 c1697b58eea8e082fa9f5090e083f0e57d75e65cdb346518fab79a473aad04e9_

```
   20 | 
   21 | from .secp256k1 import (
   22 |     antiklepto_host_commit,
```

_file_excerpt · [src/pukcc/pukcc.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/pukcc/pukcc.c#L181) · line 181 · SHA-256 53085ff2be44540f9ac0d6f54f71ca19c4e1ac12898aef6c3ecb093df8a5a67f_

```
  180 | // Returns 0 on success
  181 | uint8_t pukcc_ecdsa_verify(
  182 |     const uint8_t* public_key,
```

_file_excerpt · [src/pukcc/pukcc.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/pukcc/pukcc.h#L30) · line 30 · SHA-256 dae3c783558d199701f2f4d6fa2a10c198ed29cea93653a188e191295bde9364_

```
   29 | 
   30 | uint8_t pukcc_ecdsa_verify(
   31 |     const uint8_t* public_key,
```

_file_excerpt · [src/rust/bitbox02-rust-c/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust-c/src/lib.rs#L23) · line 23 · SHA-256 e527a51a0f0f62d0ee3a3e27b910a798f61d791ba1bc143ec92bfdcc1f607025_

```
   22 | #[cfg(feature = "factory-setup")]
   23 | mod secp256k1;
   24 | 
```

_file_excerpt · [src/rust/streaming-silent-payments/src/hash.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/streaming-silent-payments/src/hash.rs#L7) · line 7 · SHA-256 33201f813f216ace1faa8378e7cbee0f992739d6b30c90a1a740a8cc81e3f455_

```
    6 | use bitcoin::hashes::{Hash, HashEngine, sha256t_hash_newtype};
    7 | use bitcoin::secp256k1::{PublicKey, Scalar};
    8 | 
```

_file_excerpt · [src/rust/streaming-silent-payments/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/streaming-silent-payments/src/lib.rs#L12) · line 12 · SHA-256 08a764387fbe8ba1e77642c172a087172ccf897e6ed0de3209ef2dc8587547dc_

```
   11 | use bitcoin::hashes::Hash;
   12 | use bitcoin::secp256k1::{self, PublicKey, Scalar, Secp256k1, SecretKey, XOnlyPublicKey};
   13 | 
```

_file_excerpt · [src/rust/streaming-silent-payments/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/streaming-silent-payments/src/lib.rs#L43) · line 43 · SHA-256 08787745f17bf5694851af8a934a9791f92c751c329c4e20cd230db9145ae5ba_

```
   42 | pub struct SilentPayment<'a> {
   43 |     secp: &'a Secp256k1<secp256k1::All>,
   44 |     network: Network,
```

_file_excerpt · [src/rust/streaming-silent-payments/src/lib.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/streaming-silent-payments/src/lib.rs#L124) · line 124 · SHA-256 14bc8680433716b8fc52ba9a85b1577a9648567735eefacba61ba01fa093709e_

```
  123 | fn create_dleq_proof(
  124 |     secp: &Secp256k1<secp256k1::All>,
  125 |     a_sum: &SecretKey,
```

_file_excerpt · [src/rust/util/src/p256.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/util/src/p256.rs#L28) · line 28 · SHA-256 925484476bdd234888084554a30574f13c31fd235705950f76e225d606f36aee_

```
   27 | ) {
   28 |     use p256::ecdsa::{Signature, SigningKey, signature::hazmat::PrehashSigner};
   29 |     let signing_key = SigningKey::from_slice(private_key.as_ref()).unwrap();
```

_file_excerpt · [external/cryptoauthlib/lib/mbedtls/atca_mbedtls_ecdsa.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/cryptoauthlib/lib/mbedtls/atca_mbedtls_ecdsa.c#L51) · line 51 · SHA-256 f4cdd327029f645a34c8dbe10f7c918b7d043ffe26b21bb5095c676d674ce48b_

```
   50 |  */
   51 | int mbedtls_ecdsa_sign(mbedtls_ecp_group *grp, mbedtls_mpi *r, mbedtls_mpi *s,
   52 |                        const mbedtls_mpi *d, const unsigned char *buf, size_t blen,
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06894 — Квантово-уязвимый Ed25519: роль не определена (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Role resolved: the single anchor is src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:11, the same file that carries the X25519 at-rest row. BitBoxSync wraps synchronised data to a recipient public key, so this is key wrapping and encryption at rest, and harvest-now-decrypt-later applies: anything copied today is readable once a CRQC exists. Highest-urgency class in this repository, because unlike signing it cannot be fixed retroactively.
- Затронутый актив: `source-code:Ed25519:general`
- Источник данных: src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 40.2 / 100
- CVSS v3.1: неприменимо

1 упоминаний Ed25519 в 1 файл(ах), например src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:11. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:11 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs#L11) · line 11 · SHA-256 3637a75aa4245184b2de8e6f4f098698530fa03b423eab7638b978e20ddeb24d_

```
   10 | use chacha20poly1305::aead::{AeadInPlace, KeyInit};
   11 | use ed25519_dalek::VerifyingKey;
   12 | use hkdf::Hkdf;
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06897 — Квантово-уязвимый ECDH: роль не определена (4 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Затронутый актив: `source-code:ECDH:general`
- Источник данных: external/cryptoauthlib/lib/calib/calib_command.h
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 40.2 / 100
- CVSS v3.1: неприменимо

7 упоминаний ECDH в 4 файл(ах), например external/cryptoauthlib/lib/calib/calib_command.h:181. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте external/cryptoauthlib/lib/calib/calib_command.h:181 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [external/cryptoauthlib/lib/calib/calib_command.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/cryptoauthlib/lib/calib/calib_command.h#L181) · line 181 · SHA-256 9b4d335853d5e7147b112d99ade016f7fe1862a3158ed862fc5d1b9491b79b6c_

```
  180 | #define ATCA_WRITE        ((uint8_t)0x12)  //!< Write command op-code
  181 | #define ATCA_ECDH         ((uint8_t)0x43)  //!< ECDH command op-code
  182 | #define ATCA_COUNTER      ((uint8_t)0x24)  //!< Counter command op-code
```

_file_excerpt · [external/cryptoauthlib/lib/calib/calib_command.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/cryptoauthlib/lib/calib/calib_command.h#L357) · line 357 · SHA-256 55dbcbc6be030b16f3c3b4c2ef5c73c86905d38266e2c344af0782e5ae97da93_

```
  356 | #define ECDH_MODE_COPY_OUTPUT_BUFFER        ((uint8_t)0x0C)
  357 | #define ECDH_KEY_SIZE                       ATCA_BLOCK_SIZE     //!< ECDH output data size
  358 | #define ECDH_RSP_SIZE                       ATCA_RSP_SIZE_64    //!< ECDH command packet size
```

_file_excerpt · [external/cryptoauthlib/lib/calib/calib_command.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/cryptoauthlib/lib/calib/calib_command.h#L358) · line 358 · SHA-256 0b55dd8a591437d1f5b60f510e56c4247e835c1955a33d9490500bbd2c111953_

```
  357 | #define ECDH_KEY_SIZE                       ATCA_BLOCK_SIZE     //!< ECDH output data size
  358 | #define ECDH_RSP_SIZE                       ATCA_RSP_SIZE_64    //!< ECDH command packet size
  359 | /** @} */
```

_file_excerpt · [external/cryptoauthlib/lib/calib/calib_ecdh.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/cryptoauthlib/lib/calib/calib_ecdh.c#L159) · line 159 · SHA-256 cc79ff1975ef75f3d142805474f71988336ac4bdec7e77815f619991225013d2_

```
  158 |         {
  159 |             ATCA_TRACE(status, "ECDH Failed"); break;
  160 |         }
```

_file_excerpt · [external/cryptoauthlib/lib/pkcs11/pkcs11_key.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/cryptoauthlib/lib/pkcs11/pkcs11_key.c#L953) · line 953 · SHA-256 c41a3072038479a783a892f81f7afc850c71c7798fb752eb6480c7f82e64ee87_

```
  952 |             /* Because of the number of ECDH options this function unfortunately has a complex bit of logic
  953 |                to walk through to select the proper ECDH command. Normally this would be left up to the user
  954 |                to chose */
```

_file_excerpt · [external/cryptoauthlib/python/setup.py](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/cryptoauthlib/python/setup.py#L224) · line 224 · SHA-256 2ebf64b8e13175e127281f9b0d8e537854b0323a91c1f0f101a328a5d1e7c09e_

```
  223 |         download_url=_DOWNLOAD_URL,
  224 |         keywords='Microchip ATECC508A ATECC608 ECDSA ECDH',
  225 |         project_urls=_PROJECT_URLS,
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06900 — Квантово-уязвимый X25519: роль не определена (6 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** The remaining rows carry roles the engine determined and review agrees with, each checked against the cited file. ECDSA at src/bootloader/bootloader.c:537 and stage0/stage1_sigcheck.c is firmware and boot verification, with the public keys fixed in the bootloader: the hardest item to migrate, because it needs new hardware or a signed transition path. X25519 at bitbox-noise/{lib,noise_xx,x25519}.rs is the Noise channel to the host — recordable now, decryptable later, answered by a hybrid exchange. X25519 at bitboxsync.rs is key wrapping at rest. ECDSA across bitbox-secp256k1 and bitbox02-rust (bip32.rs, bip39.rs, hww/api/bitcoin/signmsg.rs) is transaction and message signing on secp256k1. Ed25519 at bitbox02-rust/src/keystore/ed25519.rs is transaction signing on the Cardano path.
- Затронутый актив: `source-code:X25519:general`
- Источник данных: external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/Hacl_Curve25519.h
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 40.2 / 100
- CVSS v3.1: неприменимо

6 упоминаний X25519 в 6 файл(ах), например external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/Hacl_Curve25519.h:18. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/Hacl_Curve25519.h:18 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/Hacl_Curve25519.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/Hacl_Curve25519.h#L18) · line 18 · SHA-256 6b26d494a6e0efb7718fecc1d561c12f021e02c91d67b217b25e424c3a1402a5_

```
   17 | 
   18 | void Hacl_Curve25519_crypto_scalarmult(uint8_t *mypublic, uint8_t *secret, uint8_t *basepoint);
   19 | 
```

_file_excerpt · [external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/vs2010/Hacl_Curve25519.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/vs2010/Hacl_Curve25519.h#L18) · line 18 · SHA-256 6b26d494a6e0efb7718fecc1d561c12f021e02c91d67b217b25e424c3a1402a5_

```
   17 | 
   18 | void Hacl_Curve25519_crypto_scalarmult(uint8_t *mypublic, uint8_t *secret, uint8_t *basepoint);
   19 | 
```

_file_excerpt · [external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/x25519.h](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/x25519.h#L190) · line 190 · SHA-256 93ca5e6bc26dc7e7424ffbcda870ae8b7506c5289cd5316dfba229a797d6040f_

```
  189 | 
  190 | #endif /* x25519.h */
```

_file_excerpt · [external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/Hacl_Curve25519.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/Hacl_Curve25519.c#L724) · line 724 · SHA-256 2e635634cbb35ab0ee5084a79fefb67ecaa5885f8782e471bd9477f4fb0d669e_

```
  723 | 
  724 | void Hacl_Curve25519_crypto_scalarmult(uint8_t *mypublic, uint8_t *secret, uint8_t *basepoint)
  725 | {
```

_file_excerpt · [external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/everest.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/everest.c#L28) · line 28 · SHA-256 fef5bf54076fc78fac6206b8a538ffa1b3f43863a516019d43b136b53dc6cf20_

```
   27 | 
   28 | #include "everest/x25519.h"
   29 | #include "everest/everest.h"
```

_file_excerpt · [external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/legacy/Hacl_Curve25519.c](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/legacy/Hacl_Curve25519.c#L769) · line 769 · SHA-256 f6b2d5d0e7eb831dcff73317fa844f9e075b7b7e750fb599f86d126842e0d437_

```
  768 | 
  769 | void Hacl_Curve25519_crypto_scalarmult(uint8_t *mypublic, uint8_t *secret, uint8_t *basepoint)
  770 | {
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06911 — bytes 1.5.0 затронут GHSA-434x-w66g-qw3r (CVE-2026-25541, RUSTSEC-2026-0007)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/bytes@1.5.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-434x-w66g-qw3r (CVE-2026-25541, RUSTSEC-2026-0007) для пакета crates.io bytes версии 1.5.0: bytes has integer overflow in BytesMut::reserve. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-434x-w66g-qw3r
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-434x-w66g-qw3r](https://osv.dev/vulnerability/GHSA-434x-w66g-qw3r) · manifest · SHA-256 58c8425f679122ea78208908d7c42d7c0f6eb030e5fbaef6d65097f3e6709156_

```
{"id": "GHSA-434x-w66g-qw3r", "aliases": ["CVE-2026-25541", "RUSTSEC-2026-0007"], "modified": "2026-09-10T03:50:33.995841351Z", "summary": "bytes has integer overflow in BytesMut::reserve", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.11.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06899 — Некриптографический ГСЧ рядом с чувствительными идентификаторами в external/lvgl/docs/src/_static/jquery.js

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `file:external/lvgl/docs/src/_static/jquery.js`
- Источник данных: external/lvgl/docs/src/_static/jquery.js
- Метод обнаружения: Сопоставление регулярных выражений с API конкретного языка.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 25.2 / 100
- CVSS v3.1: неприменимо

«Math.random()» в строка 2 в строке, упоминающей key/token/secret/password/nonce.

**Возможные последствия.** Предсказуемые значения могут позволить угадать токен или ключ.

**Шаги воспроизведения.**

```
Откройте строка 2 в предоставленном файле external/lvgl/docs/src/_static/jquery.js и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [external/lvgl/docs/src/_static/jquery.js](https://github.com/BitBoxSwiss/bitbox02-firmware/blob/ae548ef4e40f548a17542ba457f138db4fa0069d/external/lvgl/docs/src/_static/jquery.js#L2) · line 2 · SHA-256 22dc2b5ae897fe9b7d69c804eda741771a2b85daae153267199b7d950838df19_

```
    1 | /*! jQuery v3.6.0 | (c) OpenJS Foundation and other contributors | jquery.org/license */
    2 | !function(e,t){"use strict";"object"==typeof module&&"object"==typeof module.exports?module.exports=e.document?t(e,!0):function(e){if(!e.document)throw new Error("jQuery requires a window with a document");return t(e)}:t(e)}("undefined"!=typeof window?window:this,function(C,e){"use strict";var t=[],
```

**Ограничения проверки.** Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Используйте CSPRNG (secrets, crypto.getRandomValues, crypto/rand).

**Повторная проверка.** Повторно просканируйте код и проверьте места вызова из доказательства.

### QSI-2026-06912 — certifi 2022.12.7 затронут GHSA-248v-346w-9cwc (CVE-2024-39689, PYSEC-2024-230)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/certifi@2022.12.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-248v-346w-9cwc (CVE-2024-39689, PYSEC-2024-230) для пакета PyPI certifi версии 2022.12.7: Certifi removes GLOBALTRUST root certificate. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-248v-346w-9cwc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-248v-346w-9cwc](https://osv.dev/vulnerability/GHSA-248v-346w-9cwc) · line 13 · SHA-256 3d74205f26ab1e3c65bcb869a954fae59f9758d2bbf87e429684d71964bbb864_

```
{"id": "GHSA-248v-346w-9cwc", "aliases": ["CVE-2024-39689", "PYSEC-2024-230"], "modified": "2026-09-10T03:50:15.994602411Z", "summary": "Certifi removes GLOBALTRUST root certificate", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2024.7.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06922 — pygments 2.14.0 затронут GHSA-5239-wwwm-4pmq (CVE-2026-4539, PYSEC-2026-2987)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:PyPI/pygments@2.14.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 3.3 (`CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-5239-wwwm-4pmq (CVE-2026-4539, PYSEC-2026-2987) для пакета PyPI pygments версии 2.14.0: Pygments has Regular Expression Denial of Service (ReDoS) due to Inefficient Regex for GUID Matching. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5239-wwwm-4pmq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-5239-wwwm-4pmq](https://osv.dev/vulnerability/GHSA-5239-wwwm-4pmq) · line 34 · SHA-256 3a3de252c0c0118999a686c303b22756537724efae2e918007008069280ec161_

```
{"id": "GHSA-5239-wwwm-4pmq", "aliases": ["CVE-2026-4539", "PYSEC-2026-2987"], "modified": "2026-09-10T03:50:59.780634752Z", "summary": "Pygments has Regular Expression Denial of Service (ReDoS) due to Inefficient Regex for GUID Matching", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06907 — crypto-bigint 0.5.5 затронут RUSTSEC-2026-0387 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Подтверждённая техническая уязвимость · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** crypto-bigint 0.5.5 (multiple timing variability issues in operations intended to be constant-time) is reachable in shipped firmware, and the path is worth stating exactly because it is narrower than it looks. src/rust/util/Cargo.toml:17 takes p256 as an *optional* dependency with features ["arithmetic", "ecdsa"], and lib.rs guards it with #[cfg(feature = "p256")]. That feature is switched on in exactly one place: src/rust/bitbox02-rust-c/Cargo.toml, inside the app-u2f feature block ("util/p256"). So p256 -> elliptic-curve -> crypto-bigint is compiled in whenever the U2F/FIDO app is built — the Multi edition — and is absent from a Bitcoin-only build. What it does there is secret-dependent: util/src/p256.rs exports rust_p256_sign, which calls SigningKey::sign_prehash with a private key over the C FFI, i.e. U2F authentication signatures on NIST P-256. The keys at stake are therefore FIDO credentials, NOT bitcoin spending keys: those go through bitbox-secp256k1 (libsecp256k1 in C), which this advisory does not touch. Stated precisely: no exploit is demonstrated, and the attacker model is physical possession plus timing measurement, which is the threat a hardware wallet exists to resist — hence medium rather than low. Fix available in crypto-bigint 0.7.6; maintainers should match the advisory's named operations against p256's scalar arithmetic.
- Затронутый актив: `dependency:crates.io/crypto-bigint@0.5.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 23.9 / 100
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

### QSI-2026-06908 — keccak 0.1.4 затронут GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** keccak 0.1.4's unsoundness is in the opt-in ARMv8 assembly backend behind the asm Cargo feature, which is off by default and which no manifest in src/rust enables. Its consumers are bitbox02-rust and sha3, both using the portable implementation. Upgrading to 0.1.6 is still the cheap move during routine maintenance.
- Затронутый актив: `dependency:crates.io/keccak@0.1.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 35.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012) для пакета crates.io keccak версии 0.1.4: Unsoundness in opt-in ARMv8 assembly backend for `keccak`. Затронутый код находится за флагом Cargo `asm`, выключенным по умолчанию; ни один проверенный манифест его не включает — бюллетень не применим, если флаг не включает другая зависимость.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3288-p39f-rqpv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3288-p39f-rqpv](https://osv.dev/vulnerability/GHSA-3288-p39f-rqpv) · manifest · SHA-256 638750a493b76f126adef65e1dd53e2ef494cf4b1d4c7edcc7db12181ba27f6c_

```
{"id": "GHSA-3288-p39f-rqpv", "aliases": ["RUSTSEC-2026-0012"], "modified": "2026-09-10T03:50:59.332505686Z", "summary": "Unsoundness in opt-in ARMv8 assembly backend for `keccak`", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.1.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06909 — time 0.3.44 затронут GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** time 0.3.44's stack-exhaustion issue is in the RFC 2822 and RFC 3339 parsing entry points (time::Date::parse, time::OffsetDateTime::parse and friends). time is pulled in by the workspace's own util crate, which uses it for datetime formatting in util/src/datetime.rs, not for parsing attacker-supplied strings, and no audited file names the affected functions. _автоматическая серьёзность: Средняя._
- Затронутый актив: `dependency:crates.io/time@0.3.44`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 35.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009) для пакета crates.io time версии 0.3.44: time vulnerable to stack exhaustion Denial of Service attack. Часть исходных файлов продукта не уместилась в ограничения размера, поэтому затронутые функции не искались.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-r6v5-fh4h-64xc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-r6v5-fh4h-64xc](https://osv.dev/vulnerability/GHSA-r6v5-fh4h-64xc) · manifest · SHA-256 f9407c25f7cc6bacd2695a5be9ea893203cf87df27320f0289d5e50d5077d0d1_

```
{"id": "GHSA-r6v5-fh4h-64xc", "aliases": ["CVE-2026-25727", "RUSTSEC-2026-0009"], "modified": "2026-09-10T03:50:35.583241382Z", "summary": "time vulnerable to stack exhaustion Denial of Service attack", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:A/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.3.47).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06906 — block-buffer 0.10.3 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** block-buffer 0.10.3 reaches this tree through digest, so every hash in it (sha2, sha3, blake2, hmac, ripemd, the dalek curves) sits above it and the dependency really is there. But the advisory is that a panic leaves the inline buffer position corrupted, which only matters if the panic is caught and the same buffer is then reused. This is no_std firmware on Cortex-M: std::panic::catch_unwind does not exist in that build. Checked rather than assumed — of 30 catch_unwind occurrences in the repository, 26 are in external/vendor third-party crates and the 4 under src/ are all test code: a #[cfg(test)] mod in bitbox-executor/src/lib.rs, two TestingHal tests in bitbox02-rust/src/hww.rs and async_usb.rs, and the integration test bitbox-secp256k1/tests/context.rs. The precondition cannot occur on the device. _автоматическая серьёзность: Средняя._
- Затронутый актив: `dependency:crates.io/block-buffer@0.10.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-qwgh-2vcv-g2f7 для пакета crates.io block-buffer версии 0.10.3: block_buffer: panic corrupts inline buffer position. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-06904 — anyhow 1.0.31 затронут RUSTSEC-2026-0190 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** anyhow 1.0.31 (unsoundness in Error::downcast_mut) enters only through prost-derive, which is a proc-macro crate, so it runs in the code generator at build time and is never linked into the firmware image. Traced in src/rust/Cargo.lock: anyhow <- prost-derive <- prost <- bitbox-proto <- bitbox02-rust <- bitbox02-rust-c. Error::downcast_mut is not called anywhere in the audited tree. _автоматическая серьёзность: Низкая._
- Затронутый актив: `dependency:crates.io/anyhow@1.0.31`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 20.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0190 для пакета crates.io anyhow версии 1.0.31: Unsoundness in `Error::downcast_mut()`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Часть исходных файлов продукта не уместилась в ограничения размера, поэтому затронутые функции не искались.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0190
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0190](https://osv.dev/vulnerability/RUSTSEC-2026-0190) · manifest · SHA-256 12d4b3eeb5a7dc67549bc112051813542621c4c3bb2d3ddfb353886e687f8013_

```
{"id": "RUSTSEC-2026-0190", "aliases": [], "modified": "2026-06-29T14:15:03.650725453Z", "summary": "Unsoundness in `Error::downcast_mut()`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.0.103).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06910 — anyhow 1.0.75 затронут RUSTSEC-2026-0190 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** anyhow 1.0.31 (unsoundness in Error::downcast_mut) enters only through prost-derive, which is a proc-macro crate, so it runs in the code generator at build time and is never linked into the firmware image. Traced in src/rust/Cargo.lock: anyhow <- prost-derive <- prost <- bitbox-proto <- bitbox02-rust <- bitbox02-rust-c. Error::downcast_mut is not called anywhere in the audited tree. _автоматическая серьёзность: Низкая._
- Затронутый актив: `dependency:crates.io/anyhow@1.0.75`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 20.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0190 для пакета crates.io anyhow версии 1.0.75: Unsoundness in `Error::downcast_mut()`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Часть исходных файлов продукта не уместилась в ограничения размера, поэтому затронутые функции не искались.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0190
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0190](https://osv.dev/vulnerability/RUSTSEC-2026-0190) · manifest · SHA-256 12d4b3eeb5a7dc67549bc112051813542621c4c3bb2d3ddfb353886e687f8013_

```
{"id": "RUSTSEC-2026-0190", "aliases": [], "modified": "2026-06-29T14:15:03.650725453Z", "summary": "Unsoundness in `Error::downcast_mut()`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.0.103).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06903 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Accurate and the single most quotable row for a migration budget: across 40 dependency manifests the tree declares curve25519-dalek, ecdsa, ed25519-dalek, p256, secp256k1 and x25519-dalek, and nothing PQC-capable. On a Cortex-M target that is not an oversight — ML-DSA and SLH-DSA signature and key sizes are the constraint, and a no_std PQ implementation that fits the flash and RAM budget is itself the engineering problem. Worth stating as a finding precisely because the fix is not "add a crate".
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 15.0 / 100
- CVSS v3.1: неприменимо

В 48 манифестах зависимостей QSI нашёл криптобиблиотеки (curve25519-dalek, ecdsa, ed25519-dalek, p256, secp256k1, x25519-dalek), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · py/pyproject.toml, py/requirements.txt, src/rust/Cargo.lock, src/rust/Cargo.toml, src/rust/bins/bitbox03-boot0/Cargo.toml, src/rust/bins/bitbox03-boot1/Cargo.toml, src/rust/bins/bitbox03-factorysetup/Cargo.toml, src/rust/bins/bitbox03-firmware/Cargo.toml, src/rust/bitbox-aes/Cargo.toml, src/rust/bitbox-board-stm32u5a9j-dk-build/Cargo.toml, src/rust/bitbox-board-stm32u5a9j-dk-sys/Cargo.toml, src/rust/bitbox-board-stm32u5a9j-dk/Cargo.toml, src/rust/bitbox-boot-utils/Cargo.toml, src/rust/bitbox-byt · SHA-256 bf8c520f29fbbee5a6f56af359cab24476ceec5fc694f1dd615a03d9b2a066fd_

```
Crypto libraries: curve25519-dalek, ecdsa, ed25519-dalek, p256, secp256k1, x25519-dalek
```

**Ограничения проверки.** Отсутствие доказательств не является доказательством отсутствия: системные библиотеки и транзитивные зависимости могут не указываться.

**Рекомендация.** Определите источник поддержки PQC (TLS-терминатор, KMS/HSM, обновление библиотек).

**Повторная проверка.** Повторите сканирование после обновлений.

### QSI-2026-06905 — bare-metal 0.2.5: информационный бюллетень RUSTSEC-2026-0110 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** bare-metal 0.2.5 is flagged as deprecated, not vulnerable; the advisory reports no defect. Recording the decision to keep it, which is what an informational advisory asks for. It is relevant to post-quantum readiness only in the weak sense that an unmaintained crate will not gain PQ support, and this one carries no cryptography at all.
- Затронутый актив: `dependency:crates.io/bare-metal@0.2.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:07 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2026-0110 для пакета crates.io bare-metal версии 0.2.5 как информационный (unmaintained): bare-metal is deprecated. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0110
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0110](https://osv.dev/vulnerability/RUSTSEC-2026-0110) · manifest · SHA-256 1377cbc63847011c54324d486e3a7bae12ccbda6c1c9a981451db3532783f3c2_

```
{"id": "RUSTSEC-2026-0110", "aliases": [], "modified": "2026-04-24T09:45:08.136572Z", "summary": "bare-metal is deprecated", "severity": null, "declared_in_manifest": false}
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

### Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет

- Только классика — обмен ключами в канале (TLS, Noise, рукопожатия): X25519 (5 файл(ов))
- Только классика — обёртка ключей и шифрование хранимых данных: ECDH, X25519 (2 файл(ов))
- Только классика — проверка прошивки и загрузки (корень доверия): ECDSA (3 файл(ов))

**Следующий шаг:** Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **проверка прошивки и загрузки (корень доверия)** | ECDSA (3) | QSI-2026-06891 | Запланируйте гибридную подпись прошивки (классическая плюс ML-DSA или SLH-DSA, обе обязательны) и способ доставить новые ключи обновлением загрузчика |
| **обёртка ключей и шифрование хранимых данных** | ECDH (1), X25519 (1) | QSI-2026-06893, QSI-2026-06898 | Оборачивайте ключи ML-KEM или гибридным KEM (X25519 + ML-KEM-768) и переоберните хранимые ключи; для данных, которые уже могли скопировать, нужна отдельная оценка |
| **обмен ключами в канале (TLS, Noise, рукопожатия)** | X25519 (5) | QSI-2026-06892 | Переведите рукопожатие на гибридный обмен ключами (X25519MLKEM768 в TLS 1.3; гибридный KEM в протоколах на основе Noise) |
| **подпись транзакций и сообщений** | ECDSA (17), Ed25519 (4), Schnorr (BIP-340) (3) | QSI-2026-06863, QSI-2026-06895, QSI-2026-06902 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |
| **роль не определена** | ECDSA (10), X25519 (6), ECDH (4), Ed25519 (1) | QSI-2026-06862, QSI-2026-06894, QSI-2026-06897, QSI-2026-06900 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — факторизация | взламывает | Q1 | RSA (41) | Взламывает RSA при любой длине ключа: более длинный модуль лишь полиномиально повышает стоимость. Планируйте переход на ML-KEM (или гибрид) для установления ключей и ML-DSA / SLH-DSA для подписей; начинайте с ключей, защищающих данные, которые должны оставаться конфиденциальными годами («собери сейчас — расшифруй потом»), и с долгоживущих подписей. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | ECDH (6), ECDSA (35), Ed25519 (6), Schnorr (BIP-340) (1), X25519 (15) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | AES-128 (4), Blowfish (1), CMAC (3), Camellia (1), ChaCha20-Poly1305 (4), HKDF (1), HMAC (12), Keccak-256 (4), RC4 (1), RIPEMD-160 (1), SHA-1 (5), SHA-2 (31) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (4), RIPEMD-160 (1), SHA-1 (5), SHA-2 (31) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |
| Алгоритм Саймона — суперпозиционные атаки на симметричные конструкции | только при суперпозиционных запросах | Q2 | GCM mode (2) | Для обычного применения AES-GCM или CBC-MAC действий не требуется — модель атаки неприменима. Зафиксируйте это как допущение модели; для конструкций типа Even–Mansour см. офлайн-вариант. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- keys: releases/pubkeys/psteiger.asc line 1: OpenPGP algorithm ID 18 is not in the algorithm registry
- tls_code: tools/atecc608/go.mod: go 1.19 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS
- certificates: external/cryptoauthlib/lib/atcacert/atcacert_pem.h line 37: certificate could not be parsed (ValueError)
- tls_key_exchange_groups: external/lvgl/docs/doxygen_xml.py line 349: not in the algorithm registry, not assessed: {}
- tls_key_exchange_groups: external/lvgl/docs/src/details/main-modules/indev/groups.rst line 4: not in the algorithm registry, not assessed: =====
- tls_key_exchange_groups: external/lvgl/scripts/generate_lv_conf.py line 67: not in the algorithm registry, not assessed: re.search(r'([A-Z0-9_]+)\s+(.+)'
- tls_key_exchange_groups: external/lvgl/scripts/update_version.py line 28: not in the algorithm registry, not assessed: re.search(self.RE_PATTERN

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P1 | QSI-2026-06890 | Удалите отключение проверки сертификатов в scripts/generate_version_headers.py. | устранение первопричины | Отключений проверки не осталось вне явно помеченного тестового кода. |
| P1 | QSI-2026-06861 | Используйте AEAD-режим (GCM) с уникальными nonce. | устранение первопричины | Повторно просканируйте код и проверьте места вызова из доказательства. |
| P1 | QSI-2026-06901 | Используйте AEAD-режим (GCM) с уникальными nonce. | устранение первопричины | Повторно просканируйте код и проверьте места вызова из доказательства. |
| P2 | QSI-2026-06913 | Обновите certifi до исправленной версии (2026.10.18). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-6q48-6c7w-9gw2 (PYSEC-2026-4320). |
| P2 | QSI-2026-06914 | Обновите certifi до исправленной версии (2023.7.22). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xqr8-7jwr-rhp7 (CVE-2023-37920, PYSEC-2023-135). |
| P2 | QSI-2026-06918 | Обновите jinja2 до исправленной версии (3.1.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-gmj6-6f8f-6699 (CVE-2024-56201, PYSEC-2026-1472). |
| P2 | QSI-2026-06921 | Обновите jinja2 до исправленной версии (3.1.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-q2x7-8rv6-6q7h (CVE-2024-56326, PYSEC-2026-1475). |
| P2 | QSI-2026-06928 | Обновите urllib3 до исправленной версии (2.6.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2xpw-w6gg-jr37 (CVE-2025-66471, PYSEC-2026-1994). |
| P2 | QSI-2026-06930 | Обновите urllib3 до исправленной версии (2.6.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-38jv-5279-wg99 (CVE-2026-21441, PYSEC-2026-1996). |
| P2 | QSI-2026-06931 | Обновите urllib3 до исправленной версии (2.8.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8988-9cw3-xx77 (CVE-2026-97687, PYSEC-2026-4175). |
| P2 | QSI-2026-06933 | Обновите urllib3 до исправленной версии (2.6.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-gm62-xv2j-4w53 (CVE-2025-66418, PYSEC-2026-1998). |
| P2 | QSI-2026-06937 | Обновите urllib3 до исправленной версии (2.8.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vxq7-64xx-v4gw (CVE-2026-97689, PYSEC-2026-4177). |
| P2 | QSI-2026-06915 | Обновите idna до исправленной версии (3.15). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-65pc-fj4g-8rjx (CVE-2026-45409, PYSEC-2026-215). |
| P2 | QSI-2026-06916 | Обновите idna до исправленной версии (3.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-jjg7-2v4v-x38h (CVE-2024-3651, PYSEC-2024-60). |
| P2 | QSI-2026-06917 | Обновите jinja2 до исправленной версии (3.1.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-cpwx-vrp4-4pq7 (CVE-2025-27516, PYSEC-2026-1471). |
| P2 | QSI-2026-06919 | Обновите jinja2 до исправленной версии (3.1.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h5c8-rqwp-cp95 (CVE-2024-22195, PYSEC-2026-1473). |
| P2 | QSI-2026-06920 | Обновите jinja2 до исправленной версии (3.1.4). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h75v-3vvj-5mfj (CVE-2024-34064, PYSEC-2026-1474). |
| P2 | QSI-2026-06923 | Обновите pygments до исправленной версии (2.15.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mrwq-x4v8-fh7p (CVE-2022-40896, PYSEC-2023-117). |
| P2 | QSI-2026-06924 | Обновите requests до исправленной версии (2.32.4). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9hjg-9r4m-mvj7 (CVE-2024-47081, PYSEC-2026-1872). |
| P2 | QSI-2026-06925 | Обновите requests до исправленной версии (2.32.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9wx4-h78v-vm56 (CVE-2024-35195, PYSEC-2026-1873). |
| P2 | QSI-2026-06926 | Обновите requests до исправленной версии (2.33.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-gc5v-m9x4-r6x2 (CVE-2026-25645, PYSEC-2026-2275). |
| P2 | QSI-2026-06927 | Обновите requests до исправленной версии (2.31.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j8r2-6x86-q33q (CVE-2023-32681, PYSEC-2023-74). |
| P2 | QSI-2026-06929 | Обновите urllib3 до исправленной версии (1.26.19, 2.2.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-34jh-p97f-mpxf (CVE-2024-37891, PYSEC-2026-1995). |
| P2 | QSI-2026-06932 | Обновите urllib3 до исправленной версии (1.26.18, 2.0.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-g4mx-q9vg-27p4 (CVE-2023-45803, PYSEC-2023-212). |
| P2 | QSI-2026-06934 | Обновите urllib3 до исправленной версии (2.5.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pq67-6m6q-mj2v (CVE-2025-50181, PYSEC-2026-1999). |
| P2 | QSI-2026-06935 | Обновите urllib3 до исправленной версии (2.7.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qccp-gfcp-xxvc (CVE-2026-44431, PYSEC-2026-141). |
| P2 | QSI-2026-06936 | Обновите urllib3 до исправленной версии (1.26.17, 2.0.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-v845-jxx5-vc9f (CVE-2023-43804, PYSEC-2023-192). |
| P2 | QSI-2026-06938 | Обновите zipp до исправленной версии (3.19.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-jfmj-5v4g-7637 (CVE-2024-5569, PYSEC-2026-2074). |
| P2 | QSI-2026-06911 | Обновите bytes до исправленной версии (1.11.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-434x-w66g-qw3r (CVE-2026-25541, RUSTSEC-2026-0007). |
| P2 | QSI-2026-06912 | Обновите certifi до исправленной версии (2024.7.4). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-248v-346w-9cwc (CVE-2024-39689, PYSEC-2024-230). |
| P2 | QSI-2026-06922 | Обновите pygments до исправленной версии (2.20.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-5239-wwwm-4pmq (CVE-2026-4539, PYSEC-2026-2987). |
| P2 | QSI-2026-06908 | Обновите keccak до исправленной версии (0.1.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012). |
| P2 | QSI-2026-06909 | Обновите time до исправленной версии (0.3.47). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009). |
| P2 | QSI-2026-06906 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-06899 | Используйте CSPRNG (secrets, crypto.getRandomValues, crypto/rand). | устранение первопричины | Повторно просканируйте код и проверьте места вызова из доказательства. |
| P3 | QSI-2026-06907 | Разберите RUSTSEC-2026-0387; при необходимости обновите crypto-bigint до исправленной версии (0.7.6). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0387 или результат разбора записан. |
| P3 | QSI-2026-06904 | Разберите RUSTSEC-2026-0190; при необходимости обновите anyhow до исправленной версии (1.0.103). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0190 или результат разбора записан. |
| P3 | QSI-2026-06910 | Разберите RUSTSEC-2026-0190; при необходимости обновите anyhow до исправленной версии (1.0.103). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0190 или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-06902 | Внесите использования ECDSA, Ed25519, Schnorr (BIP-340) в the wallet's transaction signing в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06864 | Внесите использования RSA в file:releases/pubkeys/JuliusWiedemann.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06865 | Внесите использования RSA в file:releases/pubkeys/JunghoonLee.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06866 | Внесите использования RSA в file:releases/pubkeys/My1.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06867 | Внесите использования RSA в file:releases/pubkeys/My1.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06868 | Внесите использования RSA в file:releases/pubkeys/TheCharlatan.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06869 | Внесите использования RSA в file:releases/pubkeys/beerosagos.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06870 | Внесите использования RSA в file:releases/pubkeys/benma.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06871 | Внесите использования RSA в file:releases/pubkeys/brianddk.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06872 | Внесите использования RSA в file:releases/pubkeys/cstenglein.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06873 | Внесите использования RSA в file:releases/pubkeys/frknakk.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06874 | Внесите использования RSA в file:releases/pubkeys/guggerf.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06875 | Внесите использования RSA в file:releases/pubkeys/jonathancross.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06876 | Внесите использования RSA в file:releases/pubkeys/jonathancross.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06877 | Внесите использования RSA в file:releases/pubkeys/nickez.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06878 | Внесите использования RSA в file:releases/pubkeys/offbyn.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06879 | Внесите использования Ed25519 в file:releases/pubkeys/psteiger.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06880 | Внесите использования RSA в file:releases/pubkeys/stadicus.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06881 | Внесите использования RSA в file:releases/pubkeys/strnbrg.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06882 | Внесите использования RSA в file:releases/pubkeys/sutterseba.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06883 | Внесите использования RSA в file:releases/pubkeys/tomasvrba.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06884 | Внесите использования RSA в file:releases/pubkeys/userofreddit44.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06885 | Внесите использования RSA в file:releases/pubkeys/x1ddos.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06886 | Внесите использования RSA в file:releases/pubkeys/x1ddos.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06887 | Внесите использования RSA в file:releases/pubkeys/x1ddos.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06888 | Внесите использования Ed25519 в file:releases/pubkeys/yaziza.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06889 | Внесите использования RSA в file:releases/pubkeys/yaziza.asc в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06896 | Внесите использования ECDSA в file:external/cryptoauthlib/app/pkcs11/README.md в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06891 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06893 | Внесите использования X25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06898 | Внесите использования ECDH в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06863 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06892 | Внесите использования X25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06895 | Внесите использования Ed25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06862 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06894 | Внесите использования Ed25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06897 | Внесите использования ECDH в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06900 | Внесите использования X25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-06902 | Запланируйте миграцию ECDSA, Ed25519, Schnorr (BIP-340) на ? (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ? или гибридной схемы. |
| P4 | QSI-2026-06864 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06865 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06866 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06867 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06868 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06869 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06870 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06871 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06872 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06873 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06874 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06875 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06876 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06877 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06878 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06879 | Запланируйте миграцию Ed25519 на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06880 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06881 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06882 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06883 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06884 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06885 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06886 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06887 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06888 | Запланируйте миграцию Ed25519 на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06889 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06896 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-06891 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06893 | Запланируйте миграцию X25519 на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-06898 | Запланируйте миграцию ECDH на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-06863 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06892 | Запланируйте миграцию X25519 на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-06895 | Запланируйте миграцию Ed25519 на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06862 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06894 | Запланируйте миграцию Ed25519 на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06897 | Запланируйте миграцию ECDH на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-06900 | Запланируйте миграцию X25519 на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-06905 | Замените bare-metal поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | bare-metal заменён или решение зафиксировано. |

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
6. CWE-338 — Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG) — MITRE. <https://cwe.mitre.org/data/definitions/338.html> (weakness catalogue entry: the consequence is predictable values where unpredictability was assumed, which is what makes a token or key guessable)
7. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
8. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
9. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
10. D. R. Simon — On the Power of Quantum Computation (SIAM J. Comput. 26, 1997) — SIAM. <https://doi.org/10.1137/S0097539796298637> (peer-reviewed article)
11. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
12. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
13. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
14. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
15. H. Kuwakado, M. Morii — Quantum distinguisher between the 3-round Feistel cipher and the random permutation (IEEE ISIT 2010) — IEEE. <https://ieeexplore.ieee.org/document/5513654> (peer-reviewed conference paper)
16. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
17. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
18. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
19. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
20. M. Kaplan, G. Leurent, A. Leverrier, M. Naya-Plasencia — Breaking Symmetric Cryptosystems using Quantum Period Finding (CRYPTO 2016; arXiv:1602.05973) — Springer / arXiv. <https://arxiv.org/abs/1602.05973> (peer-reviewed article: superposition-query forgeries on CBC-MAC, PMAC, GMAC, GCM, OCB)
21. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
22. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
23. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
24. NIST SP 800-131A Rev. 2 — Transitioning the Use of Cryptographic Algorithms and Key Lengths — NIST. <https://csrc.nist.gov/pubs/sp/800/131/a/r2/final> (final (2019))
25. NIST SP 800-90A Rev. 1 — Recommendation for Random Number Generation Using Deterministic Random Bit Generators — NIST. <https://csrc.nist.gov/pubs/sp/800/90/a/r1/final> (final (June 2015; supersedes SP 800-90A of 2012): which constructions count as a cryptographically secure generator, and why a general-purpose PRNG does not)
26. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
27. OSV advisory GHSA-248v-346w-9cwc — OSV.dev. <https://osv.dev/vulnerability/GHSA-248v-346w-9cwc> (modified 2026-09-10T03:50:15.994602411Z)
28. OSV advisory GHSA-2xpw-w6gg-jr37 — OSV.dev. <https://osv.dev/vulnerability/GHSA-2xpw-w6gg-jr37> (modified 2026-09-25T17:15:05.968189421Z)
29. OSV advisory GHSA-3288-p39f-rqpv — OSV.dev. <https://osv.dev/vulnerability/GHSA-3288-p39f-rqpv> (modified 2026-09-10T03:50:59.332505686Z)
30. OSV advisory GHSA-34jh-p97f-mpxf — OSV.dev. <https://osv.dev/vulnerability/GHSA-34jh-p97f-mpxf> (modified 2026-09-10T03:50:14.811193644Z)
31. OSV advisory GHSA-38jv-5279-wg99 — OSV.dev. <https://osv.dev/vulnerability/GHSA-38jv-5279-wg99> (modified 2026-09-10T03:50:32.562010895Z)
32. OSV advisory GHSA-434x-w66g-qw3r — OSV.dev. <https://osv.dev/vulnerability/GHSA-434x-w66g-qw3r> (modified 2026-09-10T03:50:33.995841351Z)
33. OSV advisory GHSA-5239-wwwm-4pmq — OSV.dev. <https://osv.dev/vulnerability/GHSA-5239-wwwm-4pmq> (modified 2026-09-10T03:50:59.780634752Z)
34. OSV advisory GHSA-65pc-fj4g-8rjx — OSV.dev. <https://osv.dev/vulnerability/GHSA-65pc-fj4g-8rjx> (modified 2026-09-10T03:50:45.700124422Z)
35. OSV advisory GHSA-6q48-6c7w-9gw2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-6q48-6c7w-9gw2> (modified 2026-10-26T16:15:35.371128995Z)
36. OSV advisory GHSA-8988-9cw3-xx77 — OSV.dev. <https://osv.dev/vulnerability/GHSA-8988-9cw3-xx77> (modified 2026-10-01T17:55:53.793608550Z)
37. OSV advisory GHSA-9hjg-9r4m-mvj7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-9hjg-9r4m-mvj7> (modified 2026-10-19T20:00:04.716114530Z)
38. OSV advisory GHSA-9wx4-h78v-vm56 — OSV.dev. <https://osv.dev/vulnerability/GHSA-9wx4-h78v-vm56> (modified 2026-09-10T03:50:13.740879755Z)
39. OSV advisory GHSA-cpwx-vrp4-4pq7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-cpwx-vrp4-4pq7> (modified 2026-09-10T03:49:48.526758681Z)
40. OSV advisory GHSA-g4mx-q9vg-27p4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-g4mx-q9vg-27p4> (modified 2026-09-10T03:50:03.706889410Z)
41. OSV advisory GHSA-gc5v-m9x4-r6x2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-gc5v-m9x4-r6x2> (modified 2026-09-10T03:50:39.207922076Z)
42. OSV advisory GHSA-gm62-xv2j-4w53 — OSV.dev. <https://osv.dev/vulnerability/GHSA-gm62-xv2j-4w53> (modified 2026-09-10T03:50:58.741847479Z)
43. OSV advisory GHSA-gmj6-6f8f-6699 — OSV.dev. <https://osv.dev/vulnerability/GHSA-gmj6-6f8f-6699> (modified 2026-09-10T03:50:56.152882717Z)
44. OSV advisory GHSA-h5c8-rqwp-cp95 — OSV.dev. <https://osv.dev/vulnerability/GHSA-h5c8-rqwp-cp95> (modified 2026-09-10T03:50:00.236017440Z)
45. OSV advisory GHSA-h75v-3vvj-5mfj — OSV.dev. <https://osv.dev/vulnerability/GHSA-h75v-3vvj-5mfj> (modified 2026-09-10T03:50:13.786450101Z)
46. OSV advisory GHSA-j8r2-6x86-q33q — OSV.dev. <https://osv.dev/vulnerability/GHSA-j8r2-6x86-q33q> (modified 2026-09-10T03:50:01.756149727Z)
47. OSV advisory GHSA-jfmj-5v4g-7637 — OSV.dev. <https://osv.dev/vulnerability/GHSA-jfmj-5v4g-7637> (modified 2026-09-10T03:49:18.747455573Z)
48. OSV advisory GHSA-jjg7-2v4v-x38h — OSV.dev. <https://osv.dev/vulnerability/GHSA-jjg7-2v4v-x38h> (modified 2026-09-10T03:50:12.774088619Z)
49. OSV advisory GHSA-mrwq-x4v8-fh7p — OSV.dev. <https://osv.dev/vulnerability/GHSA-mrwq-x4v8-fh7p> (modified 2024-10-24T22:27:47.389299Z)
50. OSV advisory GHSA-pq67-6m6q-mj2v — OSV.dev. <https://osv.dev/vulnerability/GHSA-pq67-6m6q-mj2v> (modified 2026-09-10T03:50:25.299291456Z)
51. OSV advisory GHSA-q2x7-8rv6-6q7h — OSV.dev. <https://osv.dev/vulnerability/GHSA-q2x7-8rv6-6q7h> (modified 2026-09-10T03:50:21.662855250Z)
52. OSV advisory GHSA-qccp-gfcp-xxvc — OSV.dev. <https://osv.dev/vulnerability/GHSA-qccp-gfcp-xxvc> (modified 2026-09-10T03:50:47.272765640Z)
53. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-08-19T19:30:06.686866977Z)
54. OSV advisory GHSA-r6v5-fh4h-64xc — OSV.dev. <https://osv.dev/vulnerability/GHSA-r6v5-fh4h-64xc> (modified 2026-09-10T03:50:35.583241382Z)
55. OSV advisory GHSA-v845-jxx5-vc9f — OSV.dev. <https://osv.dev/vulnerability/GHSA-v845-jxx5-vc9f> (modified 2026-09-10T03:49:24.753610811Z)
56. OSV advisory GHSA-vxq7-64xx-v4gw — OSV.dev. <https://osv.dev/vulnerability/GHSA-vxq7-64xx-v4gw> (modified 2026-10-01T17:55:57.514829071Z)
57. OSV advisory GHSA-xqr8-7jwr-rhp7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-xqr8-7jwr-rhp7> (modified 2026-09-10T03:50:08.653753752Z)
58. OSV advisory RUSTSEC-2026-0110 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0110> (modified 2026-04-24T09:45:08.136572Z)
59. OSV advisory RUSTSEC-2026-0190 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0190> (modified 2026-06-29T14:15:03.650725453Z)
60. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
61. OWASP Application Security Verification Standard — OWASP. <https://owasp.org/www-project-application-security-verification-standard/> (living standard — check the project page for the current version)
62. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
63. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
64. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| Blowfish |  |  | слаб классически | устаревающий | 1 | 1 | external/optiga-trust-m/external/mbedtls/include/mbedtls/blowfish.h |
| RC4 |  |  | слаб классически | взломан | 1 | 1 | external/optiga-trust-m/external/mbedtls/include/mbedtls/arc4.h |
| RIPEMD-160 | RIPEMD-160 |  | слаб классически | устаревающий | 1 | 1 | src/rust/bitbox02-rust/src/hww/api/bitcoin/policies.rs:51 |
| SHA-1 | SHA-1 |  | слаб классически | устаревший | 5 | 5 | external/cryptoauthlib/lib/crypto/atca_crypto_sw_sha1.c; external/cryptoauthlib/lib/crypto/atca_crypto_sw_sha1.h; external/cryptoauthlib/lib/crypto/hashes/sha1_routines.c |
| CMAC |  |  | сниженный запас (Гровер), одобрен | допустимо | 3 | 3 | external/cryptoauthlib/lib/crypto/atca_crypto_hw_aes_cmac.c; external/cryptoauthlib/lib/openssl/atca_openssl_interface.c:442; external/optiga-trust-m/external/mbedtls/include/mbedtls/cmac.h |
| Camellia |  |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | external/optiga-trust-m/external/mbedtls/include/mbedtls/camellia.h |
| ChaCha20-Poly1305 |  |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | external/optiga-trust-m/external/mbedtls/include/mbedtls/chacha20.h |
| ChaCha20-Poly1305 | ChaCha20-Poly1305 |  | сниженный запас (Гровер), одобрен | допустимо | 3 | 3 | py/send_message.py:1778; src/rust/bitbox-noise/src/noise_xx.rs:9; src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:549 |
| HKDF |  |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:12 |
| HMAC |  |  | сниженный запас (Гровер), одобрен | допустимо | 11 | 11 | external/cryptoauthlib/lib/calib/calib_hmac.c; external/cryptoauthlib/lib/openssl/atca_openssl_interface.c:512; external/cryptoauthlib/python/cryptoauthlib/atjwt.py:95 |
| HMAC | HMAC-SHA-256 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/rust/bitbox02/src/securechip/imp_fake.rs:16 |
| SHA-2 | SHA-512 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/rust/bitbox02-rust/src/keystore/ed25519.rs:85 |
| AES-128 | AES-128 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 4 | 4 | external/cryptoauthlib/lib/mbedtls/atca_mbedtls_wrap.c:100; external/cryptoauthlib/lib/openssl/atca_openssl_interface.c:83; external/optiga-trust-m/external/mbedtls/configs/config-suite-b.h:90 |
| Keccak-256 | Keccak-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 4 | 4 | src/rust/bitbox02-rust/src/hww/api/ethereum/address.rs:17; src/rust/bitbox02-rust/src/hww/api/ethereum/sighash.rs:3; src/rust/bitbox02-rust/src/hww/api/ethereum/sign_typed_msg.rs:274 |
| SHA-2 |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 5 | 5 | external/cryptoauthlib/lib/crypto/atca_crypto_sw_sha2.c; external/cryptoauthlib/lib/crypto/atca_crypto_sw_sha2.h; external/cryptoauthlib/lib/crypto/hashes/sha2_routines.c |
| SHA-2 | SHA-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 25 | 25 | py/bitbox02/bitbox02/bitbox02/bootloader.py:268; py/bitbox02/bitbox02/bitbox02/secp256k1.py:18; py/bitbox02/bitbox02/communication/bitbox_api_protocol.py:187 |
| CBC mode |  |  | н/п | допустимо | 1 | 1 | external/cryptoauthlib/lib/crypto/atca_crypto_hw_aes_cbc.c |
| CCM mode |  |  | н/п | допустимо | 4 | 4 | external/cryptoauthlib/lib/crypto/atca_crypto_hw_aes_ccm.c; external/optiga-trust-m/external/mbedtls/configs/config-ccm-psk-dtls1_2.h; external/optiga-trust-m/external/mbedtls/configs/config-ccm-psk-tls1_2.h |
| CTR mode |  |  | н/п | допустимо | 2 | 2 | external/cryptoauthlib/lib/crypto/atca_crypto_hw_aes_ctr.c; external/optiga-trust-m/external/mbedtls/include/mbedtls/ctr_drbg.h |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 2 | 2 | src/rust/Cargo.lock; src/rust/util/Cargo.toml |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | н/п | допустимо | 1 | 1 | src/rust/Cargo.lock |
| Crypto library | 0.29.0 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | src/rust/Cargo.lock |
| Crypto library | 2.0.0 | x25519-dalek (ed25519-dalek) | н/п | допустимо | 3 | 3 | src/rust/Cargo.lock; src/rust/bitbox-noise/Cargo.toml; src/rust/bitbox02-rust/Cargo.toml |
| Crypto library | 2.1.1 | ed25519-dalek (ed25519-dalek) | н/п | допустимо | 2 | 2 | src/rust/Cargo.lock; src/rust/bitbox02-rust/Cargo.toml |
| Crypto library | 4.1.3 | curve25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | src/rust/Cargo.lock |
| GCM mode |  |  | н/п | допустимо | 2 | 2 | external/cryptoauthlib/lib/calib/calib_aes_gcm.c; external/cryptoauthlib/lib/calib/calib_aes_gcm.h |
| JWS alg "none" |  |  | н/п | взломан | 2 | 2 | external/lvgl/src/osal/lv_os_none.c; external/lvgl/src/osal/lv_os_none.h |
| TLS 1.0 |  |  | н/п | устаревший | 2 | 2 | external/optiga-trust-m/external/mbedtls/configs/config-ccm-psk-tls1_2.h; external/optiga-trust-m/external/mbedtls/configs/config-mini-tls1_1.h |
| TLS 1.1 |  |  | н/п | устаревший | 1 | 1 | external/optiga-trust-m/external/mbedtls/configs/config-mini-tls1_1.h |
| TLS 1.2 |  |  | н/п | допустимо | 1 | 1 | external/optiga-trust-m/external/mbedtls/configs/config-ccm-psk-tls1_2.h |
| ECDH |  |  | уязвим (Шор) | допустимо | 6 | 6 | external/cryptoauthlib/lib/calib/calib_command.h:181; external/cryptoauthlib/lib/calib/calib_ecdh.c:159; external/cryptoauthlib/lib/mbedtls/atca_mbedtls_ecdh.c |
| ECDSA | secp256r1 |  | уязвим (Шор) | допустимо | 1 | 1 | external/cryptoauthlib/app/pkcs11/README.md (line 280) |
| ECDSA |  |  | уязвим (Шор) | допустимо | 12 | 12 | external/cryptoauthlib/lib/crypto/atca_crypto_sw_ecdsa.c; external/cryptoauthlib/lib/crypto/atca_crypto_sw_ecdsa.h; external/cryptoauthlib/lib/mbedtls/atca_mbedtls_ecdsa.c:51 |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 21 | 21 | messages/btc.proto:4; messages/eth.proto:4; py/bitbox02/bitbox02/bitbox02/bitbox02.py:21 |
| ECDSA | P-256 |  | уязвим (Шор) | допустимо | 1 | 1 | src/rust/util/src/p256.rs:28 |
| Ed25519 | BIP32-Ed25519 |  | уязвим (Шор) | допустимо | 1 | 1 | messages/cardano.proto:4 |
| Ed25519 | Ed25519 |  | уязвим (Шор) | допустимо | 5 | 5 | releases/pubkeys/psteiger.asc (line 1); releases/pubkeys/yaziza.asc (line 1); src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs:11 |
| RSA | 4096-bit |  | уязвим (Шор) | допустимо | 33 | 33 | releases/pubkeys/JuliusWiedemann.asc (line 1); releases/pubkeys/JunghoonLee.asc (line 1); releases/pubkeys/My1.asc (line 1) |
| RSA | 2048-bit |  | уязвим (Шор) | допустимо | 5 | 5 | releases/pubkeys/My1.asc (line 1); releases/pubkeys/brianddk.asc (line 1); releases/pubkeys/jonathancross.asc (line 1) |
| RSA | 3072-bit |  | уязвим (Шор) | допустимо | 3 | 3 | releases/pubkeys/userofreddit44.asc (line 1); releases/pubkeys/x1ddos.asc (line 1) |
| Schnorr (BIP-340) | secp256k1, Taproot |  | уязвим (Шор) | допустимо | 1 | 1 | messages/btc.proto:4 |
| X25519 | X25519 |  | уязвим (Шор) | допустимо | 14 | 14 | external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/Hacl_Curve25519.h:18; external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/everest.h:25; external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/vs2010/Hacl_Curve25519.h:18 |
| X25519 |  |  | уязвим (Шор) | допустимо | 1 | 1 | external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/Hacl_Curve25519_joined.c |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| .cargo/config.toml | 943 | `b3cb95e3866ea74ba9a0e56cb71a0bf3564d4242f1c06aa751705c79b8b25ccb` | 0 |
| external/CMSIS/Include/cmsis_armclang.h | 20706 | `f7361b36a56909eff2b1cecd778443fd9da21eaa86878dabf5e8e216f6bfea29` | 0 |
| external/CMSIS/Include/cmsis_clang.h | 20700 | `015fd70aaca6475443082154b7c844d6db58e757b2dbe3fa3bd2673e0c353ba0` | 0 |
| external/CMSIS/Include/cmsis_compiler.h | 9526 | `ef7a1f9cb34ac7731500ab17edb7a9516a9d29e984a23da90b9b18db3a9bed68` | 0 |
| external/CMSIS/Include/cmsis_gcc.h | 30171 | `8fd513058bc3d10f1b3929c648023964dd32f375d5be39ad31a13e2038763405` | 0 |
| external/CMSIS/Include/cmsis_version.h | 1936 | `3b9195c5373a2a4dbfd968b083b3d7f5f446f9ec2e126f75928ac1ff4356b91e` | 0 |
| external/CMSIS/Include/core_cm4.h | 125284 | `4dc3fd737b06d5cd228260815756c3236d49ad68a2efd57c939c41ffb252b263` | 0 |
| external/CMSIS/Include/m-profile/armv7m_cachel1.h | 13032 | `f7905d3e336feccda0647f214e791b424c5f92e788f1303e587cebca729b6dc3` | 0 |
| external/CMSIS/Include/m-profile/armv7m_mpu.h | 11458 | `44294dc3e331deb8daae269793e579cc10920a9b88d133bbaf3a7af65d29f9e4` | 0 |
| external/CMSIS/Include/m-profile/armv81m_pac.h | 5832 | `fe2f5db52980237fe8bafe265b660ef9caac90bae4c478d34f243e82346d1daa` | 0 |
| external/CMSIS/Include/m-profile/armv8m_mpu.h | 13978 | `287fcabda261890f568009423ab2beb163bdcc9af591b4ce9e28f4e465f4e202` | 0 |
| external/CMSIS/Include/m-profile/armv8m_pmu.h | 22537 | `1323587da9fea03c96a685a9cf60c576b4d0532b3339501401332ff8a6c58e32` | 0 |
| external/CMSIS/Include/m-profile/cmsis_armclang_m.h | 23616 | `b8257289970f5ede78fe52cbbbb1a0575a1654968067a9e8043a4051c74b9e1b` | 0 |
| external/CMSIS/Include/m-profile/cmsis_clang_m.h | 23632 | `d735406717f198ddf2636858bcc56c448d3e2bbd91b3e70e7bfb0367fa62718d` | 0 |
| external/CMSIS/Include/m-profile/cmsis_gcc_m.h | 20714 | `beee8eb228280fb29b41438e98de4afb4e5f265ddb3cabf5d4be6424131bc658` | 0 |
| external/CMSIS/Include/m-profile/cmsis_iccarm_m.h | 30666 | `6307b35bc85f3f413e6ad1d200da6baa31851ce21d13f439ef6e6916dbf5206d` | 0 |
| external/CMSIS/Include/m-profile/cmsis_tiarmclang_m.h | 41815 | `c39b3c60adbcf55327d8f01d3d1a78a5e83c09f73396a48960d9b5432810f2f9` | 0 |
| external/CMSIS/Include/tz_context.h | 2452 | `2bcc2a5fea0567eff96dd3f2fd197b88feaa144bfe0df6146abd802701456d3b` | 0 |
| external/ST/Common/Inc/stm32u5xx_hal_conf.h | 19574 | `70eba04baadf4b8dcb13c2a9c71387e004a9a828d843700832b5eeca9109e6ac` | 0 |
| external/ST/Drivers/CMSIS/Device/ST/STM32U5xx/Include/stm32u5a9xx.h | 2467242 | `26c12881f0c94386f5fd8ace417bf41ea05ccb7deb2141dfe4f2b3f8c2cef417` | 0 |
| external/ST/Drivers/CMSIS/Device/ST/STM32U5xx/Include/stm32u5xx.h | 10767 | `0f5a0e434a7b081836f69648d9fc94f58bbfd00cb76a4fae5b411feaf1a8e7c3` | 0 |
| external/ST/Drivers/CMSIS/Device/ST/STM32U5xx/Include/system_stm32u5xx.h | 2713 | `73675e7a1dfd4a6378f08f6dce3ec072d6244f70365276ef52704144559b289e` | 0 |
| external/ST/Drivers/CMSIS/Include/cachel1_armv7.h | 13255 | `b211a8bbcfd62c9f0b3b3f1674927c9b58a0d95b02e449a0866ad2c99cb64232` | 0 |
| external/ST/Drivers/CMSIS/Include/cmsis_armcc.h | 27999 | `5bc0d7ed8e36e9bcb868c4042fff350c702eca305df4162fb00384789e35ee1c` | 0 |
| external/ST/Drivers/CMSIS/Include/cmsis_armclang.h | 48417 | `d5da2b48204f0d0cf1ff38ffccb527e5706cd0a091ff0a331eb41d6596c33fe5` | 0 |
| external/ST/Drivers/CMSIS/Include/cmsis_armclang_ltm.h | 56021 | `3e8ffb284f4f155de3ea93841cca853b41d5e812b53e52c64c3d4a67b7f1ec7c` | 0 |
| external/ST/Drivers/CMSIS/Include/cmsis_compiler.h | 9481 | `b51963d271c1571ca3463654c76aa7ea50c4eac5d0a2710df10414ac64d9e0f8` | 0 |
| external/ST/Drivers/CMSIS/Include/cmsis_gcc.h | 63374 | `43bfd1fe69fbbc2ca70aaf7d43cc3e20f16e0c7f66e1bdef9b51af6dc14b2617` | 0 |
| external/ST/Drivers/CMSIS/Include/cmsis_iccarm.h | 29069 | `2d255c8429e507e52cb603f2970bed4cc4a6cdcc3eb7fc7997385abad7364837` | 0 |
| external/ST/Drivers/CMSIS/Include/cmsis_version.h | 1680 | `184c19fd3ee73632edf35a0b4d49cd48be75fbf49e6ccb19d9db05fa83bea4b3` | 0 |
| external/ST/Drivers/CMSIS/Include/core_armv81mml.h | 276640 | `a40954bccbf202bd65ee721ea688122561e005c9f9f9d18e082280c5b897d0e4` | 0 |
| external/ST/Drivers/CMSIS/Include/core_armv8mbl.h | 115004 | `458b1e6788079ded52adc7d06383701c865ca97b67c5e7a0a44884194f91a842` | 0 |
| external/ST/Drivers/CMSIS/Include/core_armv8mml.h | 183191 | `5a68204fa31cda7d04d41c9ceaf3f4b1217908f59366f757ee778181c7cc8cb9` | 0 |
| external/ST/Drivers/CMSIS/Include/core_cm0.h | 41643 | `ac13cb645f108666a0e57c93467872660d6bc860a839f840dc870b7a5863b4bf` | 0 |
| external/ST/Drivers/CMSIS/Include/core_cm0plus.h | 49877 | `a09fa9c6b8b21d1920bce15b98aa56182b027e9278cca0b154812bac2aea3cfa` | 0 |
| external/ST/Drivers/CMSIS/Include/core_cm1.h | 42626 | `944bf0c4f940eef30a632cd99d5dcfe8270e8a8431eb98c0f081bcf4f61f728e` | 0 |
| external/ST/Drivers/CMSIS/Include/core_cm23.h | 121556 | `77822e9738885394ec52fca6f617452b823a0b55e2664ee225e65576cf0e8f2d` | 0 |
| external/ST/Drivers/CMSIS/Include/core_cm3.h | 109529 | `c9937781259a8897adf514445441c68570087d6a72a558d8a4afe75cdb62dbd2` | 0 |
| external/ST/Drivers/CMSIS/Include/core_cm33.h | 189524 | `225c47c36230edaa314f1e7a45b38279f6ab4d58faeb132226db35f7007d58aa` | 0 |
| external/ST/Drivers/CMSIS/Include/core_cm35p.h | 189539 | `206b427589981b78169c1d9b73e898e4e8de4efbd76fd0c2df7df81d645b9fa2` | 0 |
| external/ST/Drivers/CMSIS/Include/core_cm4.h | 120975 | `f5b63d52dd1557b15ca414cb59c264f595a7b5669db2a5878dffe22f4caedc8c` | 0 |
| external/ST/Drivers/CMSIS/Include/core_cm55.h | 317450 | `5707f716cf03f7e80151108ae94601fcfdf362dd2d830876040213318f6dee3a` | 0 |
| external/ST/Drivers/CMSIS/Include/core_cm7.h | 138948 | `e974d0a91752487d0154457cd422c37667328e9ddb7ba4fa2fed479a63577f63` | 0 |
| external/ST/Drivers/CMSIS/Include/core_cm85.h | 308328 | `75bc123889f0f5ca33c4d16b6cbdd580a3572663c899fadb2c8e28f6a5e6fead` | 0 |
| external/ST/Drivers/CMSIS/Include/core_sc000.h | 46562 | `c81377a69a4ea8ecaead42194f2ce8ab59bd4ee7bd638e423f5b1f5ec283d154` | 0 |
| external/ST/Drivers/CMSIS/Include/core_sc300.h | 108524 | `73dd461c12c7d3a693840df3084fd8f85122095c6f21fa3d779b0f3eceaebad5` | 0 |
| external/ST/Drivers/CMSIS/Include/core_starmc1.h | 193055 | `92d8661f2947d00da91653d04794cde0593fdaafb3438842a0477775716aafc5` | 0 |
| external/ST/Drivers/CMSIS/Include/mpu_armv7.h | 11731 | `29206b52ee02290ed6f5a5415ebd4187de802cf176d9b3cb844390d8e5571372` | 0 |
| external/ST/Drivers/CMSIS/Include/mpu_armv8.h | 11370 | `2c7d22a344cedcc1e35380d1f76f0e6c55da5e3101e6a41fd85497d1841fe8c9` | 0 |
| external/ST/Drivers/CMSIS/Include/pac_armv81.h | 6062 | `d76f5cc0c59a59e035115f700b8e8d95b7b98ecb99a2924e885f82a94903d984` | 0 |
| external/ST/Drivers/CMSIS/Include/pmu_armv8.h | 22786 | `cea8c105c5f41ba831fe4d9e8e39758068cd4c414383348dc2835d6be447cca0` | 0 |
| external/ST/Drivers/CMSIS/Include/tz_context.h | 2687 | `45565c8cb04c653aabaf3cceddfc848b6a0de28c20d4f7e3d475a992c7eee788` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/Legacy/stm32_hal_legacy.h | 240941 | `b23aaf341a5f9102a3030c1087cac535f369ce6bd84380f4f4fa130e26b8ef63` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal.h | 39344 | `be0aa206bbdbd4be224282ab540aa1b2545b41981b61893ca9c2868c10d45e43` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_cortex.h | 16590 | `d839d550236888f60248d33a19ed31a5fe0bece6a6dde6b2dbf9e01f776f8b25` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_def.h | 7638 | `73a911c835b4c7f75b7d4c7e47847f9776c5b55dc265bb59c17dfbbc6488e2b9` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_dma.h | 45368 | `0d4f824e3037433289958fb4d590807e04390bd707b503844286da39e11f1205` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_dma_ex.h | 38799 | `5465ca6acdf8fce2f81d9efebfc131bcd9ad2a7fa7debfabd9e0645e33588146` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_exti.h | 15761 | `9fa3b01b38b1b9376e4ac9a6f4985e319c08420b67b229db919e8e8a429f3bbe` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_flash.h | 56604 | `e59f8e71dee58b4b1cb40f9e35e14fd895f05bc3c151b8909a58cb080077aa08` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_flash_ex.h | 8978 | `8943fc2f847e40a811a27ccac5628b2b7ed19f40ab4b1dc30a813d5574778fc6` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_gpio.h | 16246 | `6d9e6c1abe6303f3e72f488c21fe2a1272a033a8309e6b8da4a3f2f62c3ced23` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_gpio_ex.h | 16959 | `40848fe334a9252b50e7a941537312443ba0830ef0a3f2a2c283151f0f4fa23c` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_gtzc.h | 26421 | `00906371d13f23982d72d85765aa40a8be03fd6e68e95d65938c1025c86bf840` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_i2c.h | 39289 | `a6c5c538d478ec7ae8d4e8813a1086cbebcd45396b7e316eb507ef5c4f4ba147` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_i2c_ex.h | 13411 | `b3db3fb637456e6076b7c253226c8fe3f204e2c6bb96ed1e65f906a7bbfa648d` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_icache.h | 9552 | `9c37a28d8f269113d93817fc5a7f7ed48ca59966a9726edd47ad4fd1a12f1aea` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_pwr.h | 49154 | `d1b3888b86f2c25b4d64a0ff6b47fc968eeb9dd0c68baf0cd7e76654b63891ab` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_pwr_ex.h | 46635 | `dd70ff0d9345914c8eac245ae7750eb66be1bb93c408a2716054a63e05eb4de2` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_rcc.h | 249034 | `5aad60929187c63f40511fcef8d762c914e9bd3b1295ea1e7cab12c719e2de7e` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_hal_rcc_ex.h | 122138 | `79e433bc3ff360f10f4e06aba39ff398d9c21199fdbed7338793bd23ac054f25` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_ll_bus.h | 149841 | `a771a988182391a991c4b419c47d4e2cbf70f79f378add0c60fe9f3cb5cac6f2` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_ll_cortex.h | 50141 | `5c088a21f30fcb18195239281377da49b063c4caf0e9055498400b914082af83` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_ll_crs.h | 24677 | `7e8889489c8ccd768d38fd3bd30aa8d7787fe7807f2630a66e945b61808be060` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_ll_dma.h | 325732 | `1114f18bd2fc05dd8dcf0a8e16d84fbd17101395a54083d494e9a6fe624c44f0` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_ll_exti.h | 58302 | `abedfbc2cc3afd1e620e0e73743dbbc7de6fda47a51d528fe08308365404665b` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_ll_gpio.h | 45676 | `e2915fdd634fe93aec7bfd6ffaa59c555e4c5edba91318b1f421cfc0e187859a` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_ll_pwr.h | 135768 | `dd616b1bd6bdf3ea369c279498ba07bd0feffb7ae3568289404acf78738298d7` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_ll_rcc.h | 243265 | `9d05359c0e477fee75927edfacebff6d862de97a08f08d8107ce2a115e434591` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_ll_system.h | 90249 | `e482344b634537f1c518a531106be559a668252e9d0119ac623f4ab535b4d04c` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Inc/stm32u5xx_ll_utils.h | 14219 | `35a84353fe5d938a7c099e761a5c1c0e4684b72327898160cb75c8019d6341ac` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal.c | 33035 | `ffb55394183c29b2d99ca0e2cffee37f3d316127258a387dc5909b25c2b660fc` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_cortex.c | 31975 | `adc1de7635bc42dd76a376614abe09c5e77733571ac376a0beaf5cf3aa14a3a3` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_dma.c | 56742 | `55390442b90c03dbe0ec51487db7e15e3cc1b05a90cca161dd32c2d53544c3f9` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_dma_ex.c | 173296 | `c172034158503449abb317e1afff86415afe036c1d5569e3f6db9d66ee4ef84d` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_exti.c | 23771 | `6e552a440b1d6333f950b74da575faa82340e1f2fc0383de55216122bb92753b` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_flash.c | 23311 | `ae1f9cc749c14d5183041cad7b4ce4a12a8ea85875bb5347bd4d20a4300da576` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_flash_ex.c | 58686 | `858308fc88f1a75eed0608ea1afaa14ee27b60177506ad1f23202597cb7c0601` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_gpio.c | 33435 | `2d7b5f252bf1bf2ad0fff46ac4fa7050bf437b23802f212051a0a595a283fffd` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_gtzc.c | 73331 | `4f4433f59e3d3e9b5207b6bf47ee4bad9225fca1cde40c1d58ec7bf56612931f` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_i2c.c | 256810 | `2f1a167093470b000b8e93968c6e0f62ef0da27253e1094b691889da56ada0dd` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_i2c_ex.c | 14226 | `43589137818ca179eebc3e43085dddd7bfd2bc04b2fb253924fc6508d2573acd` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_icache.c | 21837 | `f567b029cc3854aedda85357c300cb5df269fdfe440a24c93db90a61093271ba` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_pwr.c | 37205 | `39a009767b01100b602becf7f9c166e813baf1380d5245c0e0a67e12d97ea6dc` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_pwr_ex.c | 95646 | `2e7539e029556909828b4e9b2eede71fff772343ad8a93adee88394ac79ba0c2` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_rcc.c | 84672 | `e0314297b6d02761675651f6d46d01831e4631a4484c3962545a9a3126f99ae3` | 0 |
| external/ST/Drivers/STM32U5xx_HAL_Driver/Src/stm32u5xx_hal_rcc_ex.c | 144981 | `0a45772828e1039466f4652770b60aec034a464bb604e372626ea8a4f901aaf4` | 0 |
| external/ST/stm32u5a9j-dk/Inc/board.h | 1939 | `21fc97e0ff9eb3c4a3887b6f8176a7e0843f2dbaded4a52de6cd22136da675ba` | 0 |
| external/ST/stm32u5a9j-dk/Inc/flash.h | 1272 | `64d5076c23cc8b8bcd9171df777b5b93f8cf2c2682449a82e657dc3ee79153ab` | 0 |
| external/ST/stm32u5a9j-dk/Src/board.c | 5001 | `94f4ec7918cd843c5319594c5af8e1995c6ff5e6be8535faac8b09b8d3790caf` | 0 |
| external/ST/stm32u5a9j-dk/Src/flash.c | 1327 | `a7ae0c1bf85177b8b9d6ec8502815161bff359133c6dffeda6890028491235a1` | 0 |
| external/ST/stm32u5a9j-dk/Src/stm32u5xx_hal_msp.c | 2117 | `2cae850303d454a5092d3cd0a33c87f5dde8875a4e255003c4248f47b051d54b` | 0 |
| external/ST/stm32u5a9j-dk/Src/syscalls.c | 5109 | `03c06c72eafb44b499814cf9234aba57dd830f345d9b8779b5d7090e78517600` | 0 |
| external/ST/stm32u5a9j-dk/Src/sysmem.c | 2986 | `ad20f7b1fa1e7c73330727747222cf2ffa3245ebf035230ee9a157545e79df95` | 0 |
| external/ST/stm32u5a9j-dk/Src/system_stm32u5xx.c | 13775 | `28d00434c85c76af756649577d6b2096f3810e2adb137203b5ebe4c33020622f` | 0 |
| external/asf4-drivers/Config/hpl_cmcc_config.h | 1312 | `f151793abbc058cdd3b2a4362295ad50e387cea72730c161bf47e07f21f7bc22` | 0 |
| external/asf4-drivers/Config/hpl_dmac_config.h | 238602 | `72c57807a82c3d1059522ebc97f84b408c7a81f7da961ddf0a75910563740691` | 0 |
| external/asf4-drivers/Config/hpl_gclk_config.h | 29582 | `78ae2f945d5af55b5a9f2869e16af0c56b2ed8511a89f22f15bddee790d8c3d3` | 0 |
| external/asf4-drivers/Config/hpl_mclk_config.h | 2739 | `4b2a59f122a2add44ffe324f50884e8a18203782a285f32067e66bf9250b1748` | 0 |
| external/asf4-drivers/Config/hpl_nvmctrl_config.h | 794 | `1cb6127249f449a6ac08e3782e102a35ab36a41fd9ce204862b1a76474181f9b` | 0 |
| external/asf4-drivers/Config/hpl_osc32kctrl_config.h | 4397 | `b58ea361bb036d4d196d22fe076df84c7c6dcaaa41d2a46a99d0ae9a77d2e8fc` | 0 |
| external/asf4-drivers/Config/hpl_oscctrl_config.h | 18017 | `5fb71a801744eea831d7bc0740b7ee90210682a0432d6506d1cf44f30cd17805` | 0 |
| external/asf4-drivers/Config/hpl_port_config.h | 10431 | `eb018815c4396485ed2398490680de939e3a7c3e99f46e364a96d5ff5397ef53` | 0 |
| external/asf4-drivers/Config/hpl_rtc_config.h | 10103 | `0d209d15f595ceebb32177e624adfae310886c0b366bf29b5e27aee9d87191b7` | 0 |
| external/asf4-drivers/Config/hpl_sdhc_config.h | 611 | `545b79294fa88c876737a0df0a38d333ca66ecc1ab365750057aaca893fb5534` | 0 |
| external/asf4-drivers/Config/hpl_sercom_config.h | 12313 | `cb896c04f9b9617114ee79b5747c20b5af3b9c89114b0b259aa5dc1192112b76` | 0 |
| external/asf4-drivers/Config/hpl_systick_config.h | 480 | `10c45230fd2d62d3612e88cbcfff13b9b5acf86b0bccd090b055413d0188d230` | 0 |
| external/asf4-drivers/Config/hpl_trng_config.h | 622 | `cf280b6c908d5676a537650c471b0045e69cca7f0b418416e673aa18820f7f4a` | 0 |
| external/asf4-drivers/Config/hpl_usb_config.h | 16526 | `e04608dd087c9a668054ac1de496f13de48dfbf75ae72fb9d6b77a0c3c8ada13` | 0 |
| external/asf4-drivers/Config/peripheral_clk_config.h | 13094 | `af90e135d137c680b12757900de10bb2b118b9ffc9b818fc2bf94fbd5451b043` | 0 |
| external/asf4-drivers/Config/usbd_config.h | 8575 | `37ffa9817a035ad26181f85a9f32f735a16e9355449e3054f6caed928c6fffd4` | 0 |
| external/asf4-drivers/diskio/diskio.h | 6753 | `85811b83545e109da212b9185d89031b0318a03c62689dd8290026f935480243` | 0 |
| external/asf4-drivers/diskio/sdmmc_diskio.c | 9156 | `2fd3791050cbe4d642d004eb38f3e27fa56a8eb567961abbe4dc0cffba7ffeb4` | 0 |
| external/asf4-drivers/hal/include/hal_atomic.h | 3877 | `cecc60dd86d9ad9f1cb38c3846fe5f4ab0809f654209c4cf99ec1c6868d8a708` | 0 |
| external/asf4-drivers/hal/include/hal_cache.h | 2596 | `9a4ef6ff55e895277b7c34839f8579dd82a5a0dae4095d341901b94c775ae93f` | 0 |
| external/asf4-drivers/hal/include/hal_delay.h | 2300 | `e254bd63b1b2c6a52133de73a7cbcee3ea8f857fdad2b9470705588e4cdcb3f0` | 0 |
| external/asf4-drivers/hal/include/hal_flash.h | 6851 | `e09c82a89990ed9ab325d5b3d02d71b203d4d41fda197f3e57808aca0c045143` | 0 |
| external/asf4-drivers/hal/include/hal_gpio.h | 6478 | `8279d6f57d6d6ab08fa0a2b9791392665ba143c8e4acd1e2060f03a694900656` | 0 |
| external/asf4-drivers/hal/include/hal_i2c_m_sync.h | 8708 | `3c498f7a5a87277540af344d9adea5093e1163a4c367954847ead7c9a63d8632` | 0 |
| external/asf4-drivers/hal/include/hal_init.h | 2014 | `517751d60cb1722b851e7a7ed8ccfe66f9579c32b5b03474afbfab01786c0c51` | 0 |
| external/asf4-drivers/hal/include/hal_io.h | 3385 | `beb3ea3aae1f8aaf23f672cd65b8e3fb7dc8c44d274b533a871ff03a1c435c4a` | 0 |
| external/asf4-drivers/hal/include/hal_mci_sync.h | 7065 | `93066364411ef41034432d46ec232136f40a73c1e734bca687ac77e2541b11b5` | 0 |
| external/asf4-drivers/hal/include/hal_pac.h | 2387 | `d8e44fdd98591ae2849e0528a92a57593be44c64029662a002057cfbac0c12c3` | 0 |
| external/asf4-drivers/hal/include/hal_rand_sync.h | 4348 | `a00aa2ab017d7cdb89279bc763f148f1b35e2033df5ef7b9e556e68f1d911cd0` | 0 |
| external/asf4-drivers/hal/include/hal_sha_sync.h | 5651 | `ed3624440a83cfa7ca29abcf008499ec9f73d44e1df5fb2f41082b5ae99fff65` | 0 |
| external/asf4-drivers/hal/include/hal_sleep.h | 2189 | `0f63d55bb8f62876e6f3887bd02e4817f926b1fe762f8c332a9cc01cd4203d0f` | 0 |
| external/asf4-drivers/hal/include/hal_timer.h | 5944 | `a1947f71ec813e165d8aba175b6d095d55019e498f2fc7f5222099cfaf3fb15c` | 0 |
| external/asf4-drivers/hal/include/hal_usart_async.h | 10435 | `1a1ce2e9aab2a0d015120c0a7cc5c3290263b29217bca90448bb47e39289a00b` | 0 |
| external/asf4-drivers/hal/include/hal_usb_device.h | 8172 | `c80f51876cddd5fef1a54fe63c7aebf814eb6f7d310f393c9d423e05210390e6` | 0 |
| external/asf4-drivers/hal/include/hpl_calendar.h | 8961 | `90cb567474f4f1c89f0f9f889e95760887775d2ae85d464920f44a33e2f469c2` | 0 |
| external/asf4-drivers/hal/include/hpl_cmcc.h | 7351 | `a79aa8cb4c0f347be8f10ee6dda2f22ca137aecf55b2d50af57ce77a7954efcb` | 0 |
| external/asf4-drivers/hal/include/hpl_core.h | 1647 | `8c308843b7a5c35e34cd81b15af54c681b2746d71b21ff765f20e9eeb33445d1` | 0 |
| external/asf4-drivers/hal/include/hpl_delay.h | 2505 | `01a8ddb6c143eb6e2d878e515e46e964428bd493de53352100250aff1651522d` | 0 |
| external/asf4-drivers/hal/include/hpl_dma.h | 4827 | `beae645e6616cb1364da3679b85147b6f2d44a489b1f081240e6940317f139e8` | 0 |
| external/asf4-drivers/hal/include/hpl_flash.h | 9031 | `bc78cbc7f60de621e7f4eeede70c92bd135e1a2b95d9693f0dd070363aab001e` | 0 |
| external/asf4-drivers/hal/include/hpl_gpio.h | 6277 | `a1f35be42c644145d04a6e3ee4e53600a9dab12f087f0b97bfa529f7c1951e5d` | 0 |
| external/asf4-drivers/hal/include/hpl_i2c_m_async.h | 6304 | `91561cfe002c5dcd103b44188818621b4bd75a79ecf85352a4a57bfce7ebca0a` | 0 |
| external/asf4-drivers/hal/include/hpl_i2c_m_sync.h | 5275 | `da13b738b4ec45c8392c1748a888009e84ba6cde5870b2217edb88a6a9b3392a` | 0 |
| external/asf4-drivers/hal/include/hpl_i2c_s_async.h | 5375 | `0e8c33fd15e668a700c9d8a5488667b656255d9733057ebeff612ac38eef8d63` | 0 |
| external/asf4-drivers/hal/include/hpl_i2c_s_sync.h | 5245 | `f5d0598b4829518be2e6a2c27577751f362303082313ba209b751f8bc769e48b` | 0 |
| external/asf4-drivers/hal/include/hpl_init.h | 2745 | `5c715f98a96cbe4df6263908b9cdfa8a928caa2a49611381d1d7bdcc4c2aa1b2` | 0 |
| external/asf4-drivers/hal/include/hpl_irq.h | 2735 | `ea4ddd896ccea01cf58a8878af56a3336ca0187958e720d11562d3d65f1f9366` | 0 |
| external/asf4-drivers/hal/include/hpl_mci_sync.h | 8018 | `7b7af8a1df99d7f35322fe686fe4462a56d9e66792ae7416903a97dccef074c0` | 0 |
| external/asf4-drivers/hal/include/hpl_missing_features.h | 1438 | `c78fef96c98773d8daf5c7079c318aebca6d921de31afaf793a8101407953468` | 0 |
| external/asf4-drivers/hal/include/hpl_pac.h | 2693 | `07b3bce23bf4d1f5547fb5a4f0234835a73bb729ff3c71f05cdaf5ac35afde8f` | 0 |
| external/asf4-drivers/hal/include/hpl_ramecc.h | 2507 | `bd8fc42ee6508a389caab1e28a3f1161d9f00dc67fa7ee8496a2e183bbe15223` | 0 |
| external/asf4-drivers/hal/include/hpl_rand_sync.h | 3306 | `7f94483912a845967c1c54af07d78a92de68dafb3270cf593d1c257bd0d04e63` | 0 |
| external/asf4-drivers/hal/include/hpl_reset.h | 2297 | `81db88674e7be881799def980457290dea1c25580b54ec48c3cce7ade3574268` | 0 |
| external/asf4-drivers/hal/include/hpl_sha.h | 1793 | `dc81e4dac4a42d1d485e50924a7f3bb9cde4a9880cf0ea5e91003788759846b8` | 0 |
| external/asf4-drivers/hal/include/hpl_sha_sync.h | 3906 | `464bc960d8e61fd637b522e7bcd61dc76befa63c305fdcf7e45d7cbfbe420eae` | 0 |
| external/asf4-drivers/hal/include/hpl_sleep.h | 2290 | `480c40e7686c4e3ffa61cf3cd2024b57b37ddcbf69f28e8c42a506440edf04c0` | 0 |
| external/asf4-drivers/hal/include/hpl_spi.h | 4680 | `4161e16d4b40d5b28f313037f6d3361f422680588fb8e5849fb5c170dcb507dc` | 0 |
| external/asf4-drivers/hal/include/hpl_spi_async.h | 4027 | `6fba055e16b46ad4fa8872e71a733e65b8801e3ef0abd33a4ee1ece1accc51e5` | 0 |
| external/asf4-drivers/hal/include/hpl_spi_m_async.h | 8366 | `d03a0e3af98c9c9713d93b41f882aaccdd813c1625f786fe72d301baab6fdd8d` | 0 |
| external/asf4-drivers/hal/include/hpl_spi_m_dma.h | 6557 | `e5ae7632ac427b4cd38099ba53f4808e7a6a13a6e9568d08b17721960ac09317` | 0 |
| external/asf4-drivers/hal/include/hpl_spi_m_sync.h | 5941 | `d84061ed2f95e757a894b8d052009003284ed6e8317793840e43641b3a9ecd9d` | 0 |
| external/asf4-drivers/hal/include/hpl_spi_s_async.h | 7919 | `d1b2b242a4ee39b70c48ceebfa1c8550e256abcec7d97f10b78a72994b952776` | 0 |
| external/asf4-drivers/hal/include/hpl_spi_s_sync.h | 7312 | `06400c8d53610d9176b4980c9029ad73e459c1071ddda78860fa84a80ad9ef86` | 0 |
| external/asf4-drivers/hal/include/hpl_spi_sync.h | 2020 | `e0142ebb39f54527a9f755cecb8396d27d61e34adeafa5d67121724fe625fd4a` | 0 |
| external/asf4-drivers/hal/include/hpl_time_measure.h | 2455 | `9a99acea0c1cf4e22646af6feecd68162d35e10559495eac43ed32ad41b961ae` | 0 |
| external/asf4-drivers/hal/include/hpl_timer.h | 4299 | `810f1b185d4ceb2a5d414fdb5b20d40f452195fe763ccdf9362e7add7420e5d3` | 0 |
| external/asf4-drivers/hal/include/hpl_usart.h | 2805 | `d82cc2e7e51d5a135b44b6fa8d066f9ac4cf710c085dc72eeebbef47446a0962` | 0 |
| external/asf4-drivers/hal/include/hpl_usart_async.h | 8007 | `91ee6b12f089eb076773d7076eec7355736b11fce1535b3c167337a7dd0af2a8` | 0 |
| external/asf4-drivers/hal/include/hpl_usart_sync.h | 7477 | `acbfcf477447cf7ca8a502abb686132720cac55fcf6733f218e5bd8c7d572a00` | 0 |
| external/asf4-drivers/hal/include/hpl_usb.h | 7775 | `3c4dc0b12b2a90ac68850b6df081211e32c5b4c2d634157fcf11a6dd9c30a218` | 0 |
| external/asf4-drivers/hal/include/hpl_usb_device.h | 11293 | `df2d59f55ee2d5a7ad22b938c676fac78e9d23822d203b78761f9a5ca691e910` | 0 |
| external/asf4-drivers/hal/include/hpl_usb_host.h | 18701 | `950d8a8c839aad5a8d100e602366df862e0267da948490b23872407d04a5d4a2` | 0 |
| external/asf4-drivers/hal/include/hpl_user_area.h | 4704 | `859beae1217e9691a27b49bbe53a92784303d3c78335065ecfc58c041ea42413` | 0 |
| external/asf4-drivers/hal/src/hal_atomic.c | 1874 | `db89288e13c7ce35dde4b25170607cd5ab2ae020309ccd3a998a6a592098a9f8` | 0 |
| external/asf4-drivers/hal/src/hal_cache.c | 2062 | `4cc33a23d079c39d3b2ccaa43469e7f1c2f43c7ea8dddf21ab1eb30bb6e1103a` | 0 |
| external/asf4-drivers/hal/src/hal_delay.c | 2095 | `54c05baff4f0a9ac2a868d8b366cc74e549d0fc875a70f87cdf86725caf37d7e` | 0 |
| external/asf4-drivers/hal/src/hal_flash.c | 8088 | `d7197dc8b031570a61972c00accde8d560cc8be03ea5cfb3b5861cd1cb3be24d` | 0 |
| external/asf4-drivers/hal/src/hal_gpio.c | 1449 | `2f97bef2239628e6d6cf4bacd45f9c1c6eac04000655116cd299b0b714dcdd58` | 0 |
| external/asf4-drivers/hal/src/hal_i2c_m_sync.c | 5689 | `a9b5555a584768beec67504bf8ff4313e66312b95b9b4671c51e782054f9cb6e` | 0 |
| external/asf4-drivers/hal/src/hal_init.c | 1559 | `95a43e91805799c5147985bd7804a2fb4c4d3779efe21fdee80ac68fc583aea3` | 0 |
| external/asf4-drivers/hal/src/hal_io.c | 1933 | `ff0e7fbc899dfe0fc45c1810377b8120de5b184012dffb659605653bb5dda024` | 0 |
| external/asf4-drivers/hal/src/hal_mci_sync.c | 5785 | `1fd5a4c7892a3e16eeacde0d4e8f0a26cd770822f0e0bcf96fb8885320434c33` | 0 |
| external/asf4-drivers/hal/src/hal_pac.c | 1522 | `ed29fde8a32a6deb3a799437722eebb2d81d0e81984091a692f90e96a47bca20` | 0 |
| external/asf4-drivers/hal/src/hal_rand_sync.c | 3314 | `39ec437452732d1dec85be9ea1c923e4e428938ccefe2fc784541702571a2ab5` | 0 |
| external/asf4-drivers/hal/src/hal_sha_sync.c | 7117 | `d6075d16bee673560f1d5836da06fd59a5998175d9b9e0add376be0d9f9ea08a` | 0 |
| external/asf4-drivers/hal/src/hal_sleep.c | 2184 | `c72b49d5479d558925caf315840ea5b21e620edb7b61b1e60d244b7dc6d2b183` | 0 |
| external/asf4-drivers/hal/src/hal_timer.c | 6505 | `0c2338021d4ea4e34b74c18a2a71cb35fefe3ac08890fa621fd7da87f3fc383c` | 0 |
| external/asf4-drivers/hal/src/hal_usart_async.c | 11134 | `e2d7c2890dd90468824eaf669f130c3a539a326b83e4e93b405bdeee775f4b04` | 0 |
| external/asf4-drivers/hal/src/hal_usb_device.c | 15543 | `2b9e65a8fef0c2a9dad9a245561bd259b4cee675264d933542fe834e6b419bf6` | 0 |
| external/asf4-drivers/hal/utils/include/compiler.h | 1888 | `0af8238fed92a95fe7aa6378470eae23ca068c0daa575f0ba9b948926db02021` | 0 |
| external/asf4-drivers/hal/utils/include/err_codes.h | 2401 | `c536f0ca2a4911aad836a164e7e31f13f62e44a6b93bb24645e36edb96addda6` | 0 |
| external/asf4-drivers/hal/utils/include/events.h | 1684 | `2d1d2d1addf2c96c4d3464a3020bc178cc13cb8723dd961cf90c5c3d22288449` | 0 |
| external/asf4-drivers/hal/utils/include/parts.h | 1440 | `37e29a9a267008dc0b3d618434f1665ee52f48f6f28940590bb54512c38ab3aa` | 0 |
| external/asf4-drivers/hal/utils/include/utils.h | 48419 | `a7cacf3555c5077da7a20d24129747fc911072e0d1d7e49a06696aada7880315` | 0 |
| external/asf4-drivers/hal/utils/include/utils_assert.h | 2909 | `9d2a2edc0efde0376185ee17f04f0230c808995f692e59eab998556c14454758` | 0 |
| external/asf4-drivers/hal/utils/include/utils_decrement_macro.h | 6588 | `6c267e0a57c8da5169df7edfd1e7eaa020015c8e6870e724e315c2dd1edc883e` | 0 |
| external/asf4-drivers/hal/utils/include/utils_event.h | 3427 | `c9f829e4bce355e5ca56ea63fde43aaa81917f5bf19f4def1607bea330629c3e` | 0 |
| external/asf4-drivers/hal/utils/include/utils_increment_macro.h | 7346 | `4593febf45443c8217f34ba532a703708426a4c91a92330f16ed0d4976524764` | 0 |
| external/asf4-drivers/hal/utils/include/utils_list.h | 4360 | `38204dbfceb50c7b6b2a847dc5cfbc32c908381f9cf6e736fa298d0b97c41e16` | 0 |
| external/asf4-drivers/hal/utils/include/utils_recursion_macro.h | 2460 | `f8362947ebb5a334a976057d175410334bec312be9052648db80a779e06833d0` | 0 |
| external/asf4-drivers/hal/utils/include/utils_repeat_macro.h | 23132 | `59ab6f690e84be0ecc16d76e12ce66ada0ab4f5cb240d81d4753fe1a590152ad` | 0 |
| external/asf4-drivers/hal/utils/include/utils_ringbuffer.h | 3567 | `bfcbec9bda89cf5f30cfaf179ebaa9097c87dec5aa93d2c76189a317d52d864b` | 0 |
| external/asf4-drivers/hal/utils/src/utils_assert.c | 1532 | `4a49855bf156bd76b0322d0c477b2e1038b6cbe2301f8c6d1fc07610dbb91485` | 0 |
| external/asf4-drivers/hal/utils/src/utils_event.c | 3736 | `70adb6e723bcbbc53585b51544ed1cdd34976ac0764e33463e3718583aca0994` | 0 |
| external/asf4-drivers/hal/utils/src/utils_list.c | 3494 | `741dc6007c2695727e97cf79419a4dfed60d67da08d225a1eecd953b99d88235` | 0 |
| external/asf4-drivers/hal/utils/src/utils_ringbuffer.c | 2860 | `db8251f7d5497a207d6ecb878a05c363a4b5a4c648d763dcbc51f4094e9800e3` | 0 |
| external/asf4-drivers/hal/utils/src/utils_syscalls.c | 3173 | `2f8cc421ba88995d6473ccbdfe71d1afd226aeccd3b2d9913b713476798724a8` | 0 |
| external/asf4-drivers/hpl/cmcc/hpl_cmcc.c | 8720 | `34ff9cd93ef6b41de79d630b9b1026790e02ecaeab110cf6a229223aa51eb803` | 0 |
| external/asf4-drivers/hpl/core/hpl_core_m4.c | 4642 | `622d7047ed6165dc118dcd3513d833614e78761601c6d5a9d0f4143876e17fd0` | 0 |
| external/asf4-drivers/hpl/core/hpl_core_port.h | 2084 | `b985ef04775ea0fe2211edc9fa43dadd3568bdf2bdf3df9b7b7da1cb0e24ea75` | 0 |
| external/asf4-drivers/hpl/core/hpl_init.c | 2403 | `d59b6a2105c2af1623489a01eb0abcf46c2eb093fcf151fc5993bfee368c1d3d` | 0 |
| external/asf4-drivers/hpl/dmac/hpl_dmac.c | 8773 | `7d48048dd88e6df989344d34903a626527f90342bb972f45f2cab893a8f14607` | 0 |
| external/asf4-drivers/hpl/gclk/hpl_gclk.c | 14096 | `f5a7bd522ee72aef4f0a3ba1eaa79ececa991bba115f6be639f4e07b49e3b1a0` | 0 |
| external/asf4-drivers/hpl/gclk/hpl_gclk_base.h | 2459 | `b52e883e479f96f64e3bae8de656b9b15c1fe37578c29fcd1db15f76a871294c` | 0 |
| external/asf4-drivers/hpl/icm/hpl_icm.c | 7232 | `bb1696c251fad634c9be4e9062b8e0201e118e3115c770c9e3a5cd2c007775bd` | 0 |
| external/asf4-drivers/hpl/mclk/hpl_mclk.c | 1531 | `5fd59517a4e3ffb6fd6f06f315524610f55cb480cb9c7a366774ebedd6e9dcfe` | 0 |
| external/asf4-drivers/hpl/nvmctrl/hpl_nvmctrl.c | 21096 | `d796f22652b603026a72bf33b66fc9d6f32eaae0151b0a3667e613d59ece6c4a` | 0 |
| external/asf4-drivers/hpl/osc32kctrl/hpl_osc32kctrl.c | 2910 | `f5288ce4cd9195c777f7b01f62cf4bc75417426b349845fa6138325491352445` | 0 |
| external/asf4-drivers/hpl/oscctrl/hpl_oscctrl.c | 8695 | `091a9fa621d53af321728a68e9e7099b976aba5495b3b5c7f5d48edf040d4e8b` | 0 |
| external/asf4-drivers/hpl/pac/hpl_pac.c | 3445 | `2382d02cbef36a5ec801ee6e83cda9864e978d0dd8efd889ce8939b95dfdd452` | 0 |
| external/asf4-drivers/hpl/pm/hpl_pm.c | 1981 | `c544df613c3c1630242ce55581daff1b490bc9e7638702fd95e153ea176e16b7` | 0 |
| external/asf4-drivers/hpl/pm/hpl_pm_base.h | 1504 | `8f977e4d6289ee9e75480ba74a95fe8d60b1bfbfa76d4c3cf6cf54ff743d2675` | 0 |
| external/asf4-drivers/hpl/port/hpl_gpio_base.h | 4977 | `576a9e052b58d39052b2253a560837abca18e3b2397f2911984ccf32938e9082` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_CRT_pb.h | 2028 | `0fd91e883322baff1d72c13ba7bcb25597236ed540ba1d4d6afab96aa846b3dd` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_ClearFlags_pb.h | 1868 | `a15b1f3342f48ed4ecddfd7f79169e3f26916fcf3ba7fa9fd4ce2fab168e8784` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_Comp_pb.h | 1804 | `cb9e172f88863e5b282c173eeddc4f6d1bdaffec180967768d20fc757e9d5efa` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_CondCopy_pb.h | 2019 | `ea9b5efc1311b82ef26b324cebeaccf320ee1f32d0a9fd90e3b79728a003b685` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_Div_pb.h | 1976 | `4184edb3bd9f6af69d3e7026c7b6f2c17d14792aa68714006830fecc433e77b5` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_ExpMod_pb.h | 2513 | `d9c290f5bbafc3cb5f2b96a0fdb356a7d65682a12c926ffa90c923576f43d9aa` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_FastCopy_pb.h | 1849 | `fd2f231f31983639536245896bc1f88f84667493866255fbf964f565608c37dc` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_Fill_pb.h | 1808 | `c121ccdfd33908a411da05dc623262478612533ac76b22ab9039753fc6e6a553` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_Fmult_pb.h | 1932 | `3cc1e69387580b7de35f603169d61b0c0dec0184b2f8c9acb84985c465ec4e86` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_GCD_pb.h | 1894 | `076dadfc71fd7e5129756d989b5b4383c3571ea6709a95865071cd028f2d811d` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_GF2NEcDsa_pb.h | 2260 | `9cc5677e4d9598138d10d643a05e04707eafac281a716f470b416fa3f7a2f0b5` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_GF2NEccAdd_pb.h | 1831 | `c6b58f88b75219297a0ce734d0d0c76613034e77a1aab57660b59c4a45277d0f` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_GF2NEccConv_pb.h | 2713 | `56ecb702fec90eacab1578674a332bb074e187de9abca6ed735620a230fc25f3` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_GF2NEccDbl_pb.h | 1828 | `130748c9ed40aacffdb2c5ef8092886389ecd436e5498096cd4edf8a68a8f05e` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_GF2NEccMul_pb.h | 1823 | `9a7118109fe720026a05a7edf6d7cebb804d2ac918cee689abe5dc8f1281c8e1` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_Hardware_pb.h | 1773 | `682017ea066799d74325a4d97ee099576a3b63c320598f74a746899f8b87f955` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_Headers_pb.h | 9897 | `dd4fa7be2d08013a75fd63491fc768c945d810799de50c483adfb7c3faef5f3d` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_JumpTable_pb.h | 4771 | `ea3b237d92b0bb638a3ccbd1c6fe53abd6d251989ed2f5aab2431069d0e8fa46` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_PrimeGen_pb.h | 2119 | `f7e274fb433a0607a1e9de86aa049250aff6eeb1c9981aa5928155b7bc520a72` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_Rc_pb.h | 3451 | `86bb24849b50c5cd6e25922c5d52a58f71d1e0725820c8e75597097d08dff4b1` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_RedMod_pb.h | 2100 | `928ab1a472a9a3ac673cc140c5d97b42534e2bdad681c07c7b4f31ac9b4e8351` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_Rng_pb.h | 2451 | `87f63663441f017fb757f58819bf206ed1473d8d6a5d2869fae4cc8e044364a2` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_SelfTest_pb.h | 1763 | `d533743164fc7f7ae2c03f8f9faafbe270d2fe2b8c66503acf3bb1f85a9c17bc` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_Services_pb.h | 4862 | `ce1452057529d1c7417764d7c8d96237e826cf65641b2c8ea3bfd385ccf10248` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_Smult_pb.h | 1934 | `4f3d50812b21022fd46c2ebc9a169c7b475b84fb188f4c48a3435bf77635e9b5` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_Square_pb.h | 1945 | `a2e858469f16322a2e8284c8173ccb0e3f56db26c44479ae515af59dad9a0b4e` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_Swap_pb.h | 1805 | `ad42c7f5653c53a8ffc0672075e011e754c40a515ec43b59fb69d1fcbeaeea48` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_ZpEcDsa_pb.h | 2640 | `c680e1d3b575a42126f62d5cdc314c2da1c4155c3cf4d5f4de115324462ce911` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_ZpEccAddSub_pb.h | 1904 | `5d5554a09e2cefa4f73083925810265744b2a795cbbbaa3d6c0f2697d5a04320` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_ZpEccAdd_pb.h | 1821 | `d1afcfc71fe2555cab049480c42375326747381900a6560eb514a102dd64b10a` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_ZpEccConv_pb.h | 2679 | `3659c7d6087f26e4186aa01c6233237c4895e6b269b25a43b1b9dc923d27bca7` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_ZpEccDbl_pb.h | 1812 | `0b58826b9ece4ab6a3d28b2c46343d8304d0382f9bd605c2e81519b3861d592c` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_ZpEccMul_pb.h | 1808 | `ed6c79fc6cdac0e2d49d929edaea446b6e553a2a5244e06291114e3862de9806` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_ZpEccQuickDualMul_pb.h | 2398 | `5c86ff92b258e834ae1366aac3d475f5d09e13fc52cc3964e6e2224c4fcbe608` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_cf_pb.h | 1866 | `4caeb61c372352ad52ffd61869a3d9f51f34340e3d5a937a67f3ff5df29fe50b` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_mapping_pb.h | 1764 | `133ce455b80dca9f2166bcc8f4981625051494510f6c1622d3725e3f087d2d19` | 0 |
| external/asf4-drivers/hpl/pukcc/CryptoLib_typedef_pb.h | 7494 | `25f48abc69c7c261468b4740fa92893fc9114a254e2b7f12f2f45fb7095ffaad` | 0 |
| external/asf4-drivers/hpl/ramecc/hpl_ramecc.c | 2642 | `f7722b527ebf2b1aebe8a138a08ac4887d98dcd3c459cc2f9037db57abc23224` | 0 |
| external/asf4-drivers/hpl/rtc/hpl_rtc.c | 4852 | `6ac36c4bf6c189f3ac234a9008723cd52e3de6faa088fd0958e5441d5bcae5f2` | 0 |
| external/asf4-drivers/hpl/rtc/hpl_rtc_base.h | 1652 | `093b1d7588db0e70cb41a781710000b6d77f75857272a3f7d644fb0b74d02b56` | 0 |
| external/asf4-drivers/hpl/sdhc/hpl_sdhc.c | 15744 | `7c23d813eeacbd1dfd2381b666481f0fb993925e89c3d5ef7a75eb05f5b6c4b2` | 0 |
| external/asf4-drivers/hpl/sercom/hpl_sercom.c | 84402 | `8403abfc554414d4978c5a5611bd1ce85bc577f0cc83e1bd0f83504dda63753f` | 0 |
| external/asf4-drivers/hpl/spi/spi_lite.c | 9867 | `0b6aaa607f2cdc4fc6a28c0eedfe6bdfd2d636affd984cd85f8b47e2b31e50ab` | 0 |
| external/asf4-drivers/hpl/spi/spi_lite.h | 3513 | `eaf7f6c1c2d83c6cef2effa5240a552ea2d9726d6cfcd3b732553a0b0933fb10` | 0 |
| external/asf4-drivers/hpl/systick/hpl_systick.c | 2791 | `c7af47de984cc39dc774ecb00e2de0bc76e095b4d282aa19f69d37b3a35cfc92` | 0 |
| external/asf4-drivers/hpl/trng/hpl_trng.c | 2881 | `3d443cdb79b9894f5c65ede48b8d2f5b465951c97b534f8212128f620e868eec` | 0 |
| external/asf4-drivers/hpl/usb/hpl_usb.c | 62288 | `30021e816cfb62f72a3a9400b8884c9bc036b5ad8a0cae6bd1ae8ba399fb7736` | 0 |
| external/asf4-drivers/hri/hri_ac_d51.h | 54344 | `b471b3b2d554a7addcfab25b741272d7a6eee4847fd75514d43f37f9e59c180f` | 0 |
| external/asf4-drivers/hri/hri_adc_d51.h | 119963 | `029b3204640648b7b4e8f5027c2be74cfc4683d733b47fd4986f46bfdad73c97` | 0 |
| external/asf4-drivers/hri/hri_aes_d51.h | 35605 | `f1a54fcff49df03031d2a8965ec8dd8d8c83414dca836dc5cf341f3667f9eb05` | 0 |
| external/asf4-drivers/hri/hri_ccl_d51.h | 23922 | `ff293d538fc2dd597139c8bd7bc6cf4910e9184b61b241ad5441805de12a2c8f` | 0 |
| external/asf4-drivers/hri/hri_cmcc_d51.h | 10262 | `094d8fb7c92f9f6468188f9c74653ecab08bf22ffdf4ba844c9723297a400422` | 0 |
| external/asf4-drivers/hri/hri_d51.h | 2375 | `fb15b07aafb9fecff237bcd8f8ab69d03d33b5e38504fb9f806cc36fbd1a5419` | 0 |
| external/asf4-drivers/hri/hri_dac_d51.h | 50209 | `bf13d7cd4cd315b8cd15fb48935889fc6c9138b882224e9e265ab9413e746463` | 0 |
| external/asf4-drivers/hri/hri_dmac_d51.h | 219222 | `a637d7085631fc80361b8d94b1545d60f895dac7c946ab24a30806434bc98c6f` | 0 |
| external/asf4-drivers/hri/hri_dsu_d51.h | 35905 | `607a43d4cc2b50843b4db11fd7ef946c40018a9850addbdebb0cbf0f88884c01` | 0 |
| external/asf4-drivers/hri/hri_eic_d51.h | 55700 | `18e926641d37ba129a32b5bca01256d181561474a581eeaeaabece63cb19f0c9` | 0 |
| external/asf4-drivers/hri/hri_evsys_d51.h | 56659 | `915fcf1997fa369adad12d2b437f7725e225f2c7cf4743f535c513660c890981` | 0 |
| external/asf4-drivers/hri/hri_freqm_d51.h | 13672 | `95277a1ae04ec7bb104202271274947bb4130851663014e5d1620fd9388a8856` | 0 |
| external/asf4-drivers/hri/hri_gclk_d51.h | 25859 | `b7b35f8b57442290cf5b502cdbf6f8e2e8a6a4376581205b02fe1070bf3a8366` | 0 |
| external/asf4-drivers/hri/hri_hmatrixb_d51.h | 7903 | `c148ba15466555f5253172afcdb786ae7d5c6ebd0bbf384d07af74ad895d7420` | 0 |
| external/asf4-drivers/hri/hri_i2s_d51.h | 87926 | `ae94a47c9c1adeec79ed14db6ef4e6c9824d972ef8d4c569b302b82390aab5fc` | 0 |
| external/asf4-drivers/hri/hri_icm_d51.h | 21744 | `c85a4d3a216a767ec6a877719d434b301414cca1a8ee31d9b592016a9e373d36` | 0 |
| external/asf4-drivers/hri/hri_mclk_d51.h | 94032 | `78dd43dec0e73ec0b681dd28b0fd93f62f95d85c82825d617abc37d6cc2e2099` | 0 |
| external/asf4-drivers/hri/hri_nvmctrl_d51.h | 50196 | `b2a36107c2fc9f38b00c27bb3f394cb7e3e32bdfbd35f566cdcf048aec19cc80` | 0 |
| external/asf4-drivers/hri/hri_osc32kctrl_d51.h | 39739 | `c78363a4e0870ac36822aacb50b84d686aafc75e6d0b5085f59fe2217780c40f` | 0 |
| external/asf4-drivers/hri/hri_oscctrl_d51.h | 153893 | `b46a7ee2e6807aef0d3a182c28c6ebd2a313450b9f0f089b11b8e2dc64070da5` | 0 |
| external/asf4-drivers/hri/hri_pac_d51.h | 42409 | `de8e820ba75a58d3d592e446e2eb67e0708f4bcd9d04e2de705f659a84a9e575` | 0 |
| external/asf4-drivers/hri/hri_pcc_d51.h | 7868 | `ef4d3232ab2f3709c14b22126e4ed8e96cb1960f99ee56eabebf93185693db79` | 0 |
| external/asf4-drivers/hri/hri_pdec_d51.h | 80311 | `77f52d23b1a88b535f565969c4f909f72567e1e36d96fd502375f91d65c6c096` | 0 |
| external/asf4-drivers/hri/hri_pm_d51.h | 23086 | `b3608d92d49d4ee84a852584207c4fe80bb9623149040d2e1b8f741ee8c4904f` | 0 |
| external/asf4-drivers/hri/hri_port_d51.h | 85724 | `b1c6d6cc436fae499b35ea2aab9b049c38758ad0949793ac2447cb40e1cb9acd` | 0 |
| external/asf4-drivers/hri/hri_qspi_d51.h | 60193 | `eb7fc6fe9fdc54781494a18329d0af13a88d7269cbe461241a0d3dbe568a522e` | 0 |
| external/asf4-drivers/hri/hri_ramecc_d51.h | 10805 | `9e529997cd83333828f3b82e852869456a5c3917bcb414c23f6747fd1d485ba1` | 0 |
| external/asf4-drivers/hri/hri_rstc_d51.h | 4288 | `43471574d299d489312c42834ba55a1a07a68ecb3941526f75320667b62ce185` | 0 |
| external/asf4-drivers/hri/hri_rtc_d51.h | 356515 | `f9c252a7ac1e0baf13931479bfa449e5f5068d8604b4eef87b313532b94f1aab` | 0 |
| external/asf4-drivers/hri/hri_sdhc_d51.h | 223935 | `c3826c3beb2c31231f72525a2e0f623824ac11de0e2c3445df2bef150217ba2e` | 0 |
| external/asf4-drivers/hri/hri_sercom_d51.h | 302258 | `9320a3f062807e2a5c8a1dcf3e01327429cac83434cbed6de8a778b8ffa56eb4` | 0 |
| external/asf4-drivers/hri/hri_supc_d51.h | 49356 | `8eabcdc3980a9428fa4003ddd3ef4ebb5fcb78c24d2fec1ab4b57c0a3ee41e6b` | 0 |
| external/asf4-drivers/hri/hri_tc_d51.h | 93837 | `3fb89518295d4e77dd7e83817bc735d77c67614bb8e25856db340731bb556de6` | 0 |
| external/asf4-drivers/hri/hri_tcc_d51.h | 289575 | `890860bd2d6c1c5e99f8715032388d6e56eb3892b583d60f5251ae1eec05e0db` | 0 |
| external/asf4-drivers/hri/hri_trng_d51.h | 10663 | `f93ef7547da17f1c8fa1ff90170476eccd1e769af757b45acc30ee5802f2a8da` | 0 |
| external/asf4-drivers/hri/hri_usb_d51.h | 354474 | `e6d14e9ea14b0304f2dd44b4d8aec07e5e3a1fb6136389cc3c208be4aacb3bec` | 0 |
| external/asf4-drivers/hri/hri_wdt_d51.h | 18441 | `691945e6f92a429e2068f167d4aac36cf0191df6f8d937c61b061e56bc248509` | 0 |
| external/asf4-drivers/qtouch/include/qtm_acq_samd51_0x000f_api.h | 1077 | `432de7866a01b1ca978240dea47d81572651148603e6b06b47a738f0d6ce215f` | 0 |
| external/asf4-drivers/qtouch/include/qtm_acq_same54_0x000f_api.h | 13446 | `f309079b7e6b27130322a15c95f1c9bbe30fbc82ad86803afd95de59b1bc5c88` | 0 |
| external/asf4-drivers/qtouch/include/qtm_binding_layer_0x0005_api.h | 7811 | `853c7d2ec996e13ac89945c2ab138fb4dff0c4d5d12ec6ca3d406063d6cabce7` | 0 |
| external/asf4-drivers/qtouch/include/qtm_common_components_api.h | 6189 | `d5f19bbba531b6c2b18655312929af4722f790de8c6a1efd3240f2507b8231fc` | 0 |
| external/asf4-drivers/qtouch/include/qtm_scroller_0x000b_api.h | 4985 | `efe8d5abcfd2b79a05e908072cac908e8bd7bfdaa9d935029cbba12c3dab3fcf` | 0 |
| external/asf4-drivers/qtouch/include/qtm_touch_key_0x0002_api.h | 8184 | `97214b7b5af0eb742c9fd00e1895e7ce1893baa2ab832faddd4f8c3eff7dd306` | 0 |
| external/asf4-drivers/qtouch/include/touch_api_ptc.h | 2364 | `3228eaa831b19c670ac66207b8f5965a200e1f9d50268a0358138bcc850ecc42` | 0 |
| external/asf4-drivers/qtouch/license.h | 7274 | `bcb02cdca42690d15e4d1385c4d1d57e5fb882e99a3437ae42bfabcfb1ec8666` | 0 |
| external/asf4-drivers/sd_mmc/sd_mmc.c | 38799 | `6f08817c8e76ac8597685cb64559c6d7e0d44b9d57e28d5cf965632d151d5138` | 0 |
| external/asf4-drivers/sd_mmc/sd_mmc.h | 10885 | `4932d0baffd05f5c7dd4083ba52c11a6408d25993b8ac9002fa3f32dbfed0961` | 0 |
| external/asf4-drivers/sd_mmc/sd_mmc_protocol.h | 44290 | `a55af38a659f08fec2b3a0afc308b79f9bdeea29e2c4b8048ddac2ec4d7e400a` | 0 |
| external/asf4-drivers/usb/class/hid/usb_protocol_hid.h | 18586 | `e37898ef14bea30fcd007e9f281e8fcd6fcf1b2ea53f030f86fbdc495bd0c296` | 0 |
| external/asf4-drivers/usb/device/usbdc.c | 24565 | `27b2999e673efd37499f4fe57fc758919ae04891e53c32ce6dbb7556533c5475` | 0 |
| external/asf4-drivers/usb/device/usbdc.h | 7456 | `a74520ef0f9ffbee2c7d80afa81cbc87cd1c1c8acbd2eb36bb745000c8355a34` | 0 |
| external/asf4-drivers/usb/usb_includes.h | 4508 | `4c0ec815d94b0ced96e967da950f6ead588adf29ef674589db92f9c349b4ff2a` | 0 |
| external/asf4-drivers/usb/usb_protocol.c | 4288 | `be475c1d0b5a42cda96e7217b4c9d0b4acd8f0f4c4f08b88ba29d80cae6390b4` | 0 |
| external/asf4-drivers/usb/usb_protocol.h | 25218 | `305dffdd8d1ec030c80b13b9d6e32e0455063ea2dd8a81a6187e803d143dfe9a` | 0 |
| external/atca_config.h | 790 | `5e3d48c93b6e11ae6154b6003b83bc725d477f155bb8f7016dd36a240562c1e3` | 0 |
| external/mbedtls_config.h | 2993 | `bdd0ca3b7f47578557a8059b6bd1b1729b427c952fa8c550d0b1c23965d5123a` | 0 |
| external/optiga_config.h | 5769 | `e0741d8a61db528afd7660d332d83a2cd6deba38ea514ddbd3aa702c24d80b43` | 0 |
| external/samd51a-ds/gcc/gcc/startup_samd51.c | 45555 | `3acad5194aa7be5ca2273af9fc6c4913a1a4acde46e825bdf79c00f872ccebc3` | 0 |
| external/samd51a-ds/gcc/system_samd51.c | 1695 | `f54a5b2febc9671ae8b633ab51111fbc8ff1cb33b00e5d25d2db221936d4e175` | 0 |
| external/samd51a-ds/include/component-version.h | 1962 | `6a109468076f1307748994331fa3f3b28c2d43b0ad6a55dcf5a29c543aaadf94` | 0 |
| external/samd51a-ds/include/component/ac.h | 43843 | `009c567c2f4155bf526a66997369eda51d288a69575ea0323d88113c400eb7f0` | 0 |
| external/samd51a-ds/include/component/adc.h | 65662 | `8af32bfa63c1c1f3fb7de6679e2157fd625ad910afc27a4a79ded94bcfefcd18` | 0 |
| external/samd51a-ds/include/component/aes.h | 25607 | `aa117523ab12a7faacc1afee879be710851774456d8bb70204e70295acc95bf1` | 0 |
| external/samd51a-ds/include/component/can.h | 245804 | `093465d99290c8e0d7e62f0c504dc4d04521a059aee31af5e2d7dfcae2122ded` | 0 |
| external/samd51a-ds/include/component/ccl.h | 16432 | `81f2bdb883a3ea58d4873e25ca7c627dcdd90058aee5cbfbecfeca493a924357` | 0 |
| external/samd51a-ds/include/component/cmcc.h | 24851 | `0a286b1cd8d2e962fd021a7b0c83bdbaeec2469792558e01ecbe96cc2513c1ed` | 0 |
| external/samd51a-ds/include/component/dac.h | 39416 | `1e97189db313d734da6ab05463ce4b433e02cda7d9a23a25d74b9f53d99269ab` | 0 |
| external/samd51a-ds/include/component/dmac.h | 113464 | `65c6e1e2886bd1d2f401dc756c2c7b35ffb29093771e68bbdf624162196d0729` | 0 |
| external/samd51a-ds/include/component/dsu.h | 91387 | `1b135b4ffd85b30ece7f2d80a794f0c03f49d073c83343c523282314580009dd` | 0 |
| external/samd51a-ds/include/component/eic.h | 37003 | `169eb9121f291aac485fceacb77f6c76a52de2a95e442dbb4bb1a79b1d6f6b74` | 0 |
| external/samd51a-ds/include/component/evsys.h | 44353 | `edfa59daac85613e031fa24a997096b3aee4c2fa8a25bae044807f63fd2752c1` | 0 |
| external/samd51a-ds/include/component/freqm.h | 13845 | `f6ba6ea0b2618d67cf98e4728c535c1ebfb6814ccbe324db5d6308464457dff0` | 0 |
| external/samd51a-ds/include/component/gclk.h | 21116 | `d2aa2101309fb980696fe439d551742b90f44d595c3fc3e5f55a5fb1d4deff0e` | 0 |
| external/samd51a-ds/include/component/hmatrixb.h | 3438 | `2fde77b34fff846b984641f4e6b6751483a92d704034d0e405201cc206c2e54b` | 0 |
| external/samd51a-ds/include/component/i2s.h | 61284 | `99b805bf3923a836ddf4d88954235b193a5882f8cc11093f0abdfc43c2aa5183` | 0 |
| external/samd51a-ds/include/component/icm.h | 41828 | `d176e43b49dfd865cc4b98211b5ed1b6391b6eed6e9d45189e881666a63eac33` | 0 |
| external/samd51a-ds/include/component/mclk.h | 34840 | `a15fe47dd19b47a5a1f207a940d694790c80b42856912192d667539d09fb50df` | 0 |
| external/samd51a-ds/include/component/nvmctrl.h | 62659 | `736da0e7e8223acff30ac5b4cf0730e5ff796d87a23d75ed282076ac6d2dbaa3` | 0 |
| external/samd51a-ds/include/component/osc32kctrl.h | 21935 | `16e53fff483a3cfe540afcf0d9bd032ef29d117d4029f79d6956a213ec5d0632` | 0 |
| external/samd51a-ds/include/component/oscctrl.h | 63931 | `4a687faf9b1e824a8398e9fc58c4e3360809fe774672ef0557e99427a5ec9e4b` | 0 |
| external/samd51a-ds/include/component/pac.h | 51510 | `e819ea71cb0ba59f327c0989dc5d069b001ba6884967c211dcbf73de5193ecdb` | 0 |
| external/samd51a-ds/include/component/pcc.h | 15502 | `2505b23a1292a160ae1b39c91e9058cab86997b6205cfefa8b958826db012ea4` | 0 |
| external/samd51a-ds/include/component/pdec.h | 54513 | `1fffafef84c5f0dfd27cbade9ad78cb3b064e99d3e43df6eb211ebc539157c93` | 0 |
| external/samd51a-ds/include/component/pm.h | 16417 | `5d27ae66524474b40399ad0c58a53bdf8c5107e3803274a2f33e46515a20eca0` | 0 |
| external/samd51a-ds/include/component/port.h | 27576 | `3b11d12312c1f9c6e7ed42a958816a3635f2c56200d4867c48b6a8a3d3dbdfe2` | 0 |
| external/samd51a-ds/include/component/qspi.h | 40215 | `a89b5dcd034703a5a6728fabc95606053bac656ee15813e9a524a63a6a38d8f5` | 0 |
| external/samd51a-ds/include/component/ramecc.h | 10325 | `6ff9267c0a0daac15d63127a5efccbfd552fd678f7c133cd5cec8f5f634f9159` | 0 |
| external/samd51a-ds/include/component/rstc.h | 6202 | `f743b5bcfe16db10ece3efcd1c09aae3c5d83cb080a01c35bcadf139690c3a84` | 0 |
| external/samd51a-ds/include/component/rtc.h | 175646 | `0d561d7619a10811d33563851f5ab892ed02ac6da4018b0c9a2905d8dfc1d15f` | 0 |
| external/samd51a-ds/include/component/sdhc.h | 216816 | `16a1123b9e17a0ae6538cee211dd18828c9386286a59806ce15018100f288b06` | 0 |
| external/samd51a-ds/include/component/sercom.h | 128866 | `f4cd0d5ff26f42952b03617aa947e8f7fdafed7cb95be6692d5739d451534d64` | 0 |
| external/samd51a-ds/include/component/supc.h | 42386 | `3caa785dae92f395f41196fc13b8a3d858bbbc7dc36f798290349f9795ff3a35` | 0 |
| external/samd51a-ds/include/component/tal.h | 149332 | `0abdcc821e4fb1266879a01c5ee5fb371f0c36354d8859aaae4ac554a4ce0a07` | 0 |
| external/samd51a-ds/include/component/tc.h | 61893 | `07a9de0c3b9ba89790fc130f7bac59ffac1f725a455da82f1464918010f7ca9e` | 0 |
| external/samd51a-ds/include/component/tcc.h | 146064 | `7378baac1d2d3a07bbfa6e013f138862a3961006f3ef77c829f9f04e1353d60f` | 0 |
| external/samd51a-ds/include/component/trng.h | 9494 | `a26efab320022f24f94bdfba350d7d0f0f4d1232cdfebc42ab3c0670add8742c` | 0 |
| external/samd51a-ds/include/component/usb.h | 140383 | `4b242d6e254d3208c21ce6b729171321909a0d246303486976ce57dbca9d22df` | 0 |
| external/samd51a-ds/include/component/wdt.h | 20549 | `865ba6d637efc15d3a3c301db2e6a95aa02749acfc6391300c7277dc5d7d85d7` | 0 |
| external/samd51a-ds/include/instance/ac.h | 4609 | `a23321163fd6d6b6c70456f1de1600ec2d67e9e995004030fe0fdfca10010b6e` | 0 |
| external/samd51a-ds/include/instance/adc0.h | 6654 | `c4d5ea1c872bf1b0e64df85382da8f5535fdfff4b27a272c09d10b39d229d18e` | 0 |
| external/samd51a-ds/include/instance/adc1.h | 6725 | `5836756078d20cee86343858b6780346e8e335276c559e3b14a69bbad14ac0ed` | 0 |
| external/samd51a-ds/include/instance/aes.h | 6952 | `bd5066041b54e6f3c5a2f4d42a8bc09a22f14c88848f050a831510c78ef408be` | 0 |
| external/samd51a-ds/include/instance/can0.h | 12047 | `a20bcdd0720c54e2dda86e112e73787f24e0268b278c2a7435fe1609f3d05630` | 0 |
| external/samd51a-ds/include/instance/can1.h | 11934 | `1402bd26abd857d8dc718905614994e42aded797b37714718ccdf0d8e279864a` | 0 |
| external/samd51a-ds/include/instance/ccl.h | 2675 | `2dd13890492e9117ee712f4df7505773fd784fe8bea17804a8401a24c008a3e8` | 0 |
| external/samd51a-ds/include/instance/cmcc.h | 3442 | `63786baa38876a9aba0a6492dadefe7e59bdb67d8269c245dcb82a15367fc004` | 0 |
| external/samd51a-ds/include/instance/dac.h | 5016 | `dfa8fcd9662364a70a50aa08409517408c64e6587f69e156c592c9087395d418` | 0 |
| external/samd51a-ds/include/instance/dmac.h | 58807 | `b7f3c5719ee91f1a1b404611c809268f8e7d6d19bb1cf6cc487b24b68c2742ea` | 0 |
| external/samd51a-ds/include/instance/dsu.h | 9032 | `48e2d32bd7e3b1a4a384d69f2ab4d8f38bb6219ba5e89b274d7649fb48266ca9` | 0 |
| external/samd51a-ds/include/instance/eic.h | 4449 | `f906244a5256693fed98637d1857c3b8f543eba244143134b2cc57198a870b3a` | 0 |
| external/samd51a-ds/include/instance/evsys.h | 58944 | `7bad44d3cdc3808191328f4024ef77ff2190cca4705344a89baf91cb26267fd3` | 0 |
| external/samd51a-ds/include/instance/freqm.h | 3107 | `fa238c880c38bde570bfe9318d81caa98d49e568048acf9d500e8fc292f6120f` | 0 |
| external/samd51a-ds/include/instance/gclk.h | 16320 | `d62ea0f8e6d323047a6c3c7e58578cc0820a16934e77d9c79936a3330c83e88a` | 0 |
| external/samd51a-ds/include/instance/hmatrix.h | 9072 | `46a00d10a0e65ab8bd966a5eee503b8463e84c2f87e43a3273b0a0b066d8ae7b` | 0 |
| external/samd51a-ds/include/instance/i2s.h | 4195 | `8a87922c5148e79b79017749a4eab634e0f838487712c7db1cc366684a306572` | 0 |
| external/samd51a-ds/include/instance/icm.h | 4770 | `63ecba2bfd70c8637430b49a8dca4eab92fb650d64c5e386706d114180dd5a33` | 0 |
| external/samd51a-ds/include/instance/mclk.h | 3145 | `2451b0943874596ea013543e581a1abad537fb7f26c584687d81388d09723c4f` | 0 |
| external/samd51a-ds/include/instance/nvmctrl.h | 4764 | `bd198ff2bb16137e551a3f440a11aa39cb52fd5657e991ae31a53af5685a9e79` | 0 |
| external/samd51a-ds/include/instance/osc32kctrl.h | 3374 | `f718298ac6ca3eb85246c5b2015769ec3a373413a430bfc3065f127a93023a2e` | 0 |
| external/samd51a-ds/include/instance/oscctrl.h | 9404 | `ac683d81c36a75638cadcc19a9d6410a1dc6027882ede9bd23917638beb72477` | 0 |
| external/samd51a-ds/include/instance/pac.h | 4310 | `205c202f3b716ffc843eed3a903032ee15e52da153c9ddc5a4823085d9899750` | 0 |
| external/samd51a-ds/include/instance/pcc.h | 2904 | `321ed94d838f9113ff76e1668761dc9357ee8fde86dde5ae49dc39c9ee3c27cf` | 0 |
| external/samd51a-ds/include/instance/pdec.h | 4997 | `be6f0c806e40df2b7b367d21e8bb584326bbffd15f40f19f60518b3607a008f4` | 0 |
| external/samd51a-ds/include/instance/pm.h | 3029 | `fb04ed4d1eab24f3a0aaacb587e4cb7420e8b238650ca169e3df9fac4e6622c2` | 0 |
| external/samd51a-ds/include/instance/port.h | 14920 | `51d06558014fadc43992f49226db75fef6b070386d8e30d3f8f69dbf8c9d9871` | 0 |
| external/samd51a-ds/include/instance/pukcc.h | 2306 | `a6e95de5a4fd22c09d771abfda8a5d2646d7f43d26177c74d597a8c1a5252b0e` | 0 |
| external/samd51a-ds/include/instance/qspi.h | 3989 | `e7dd9c1b34f841c7d015dcf7d37e684733ec8d7ae9fa006a00f282e450935419` | 0 |
| external/samd51a-ds/include/instance/ramecc.h | 2489 | `bfdf55fd56bcd524ace6e714da3c63f4e60baf575b242e452723de876c096a56` | 0 |
| external/samd51a-ds/include/instance/rstc.h | 1759 | `f85d5be85fe73504f2a0f3686933095d2a68cfca19c9a86aab4c810db7d366d6` | 0 |
| external/samd51a-ds/include/instance/rtc.h | 12265 | `fc1b40545f0069b2af11073c75156057bd536645fc345ae025b19b91397ac6a9` | 0 |
| external/samd51a-ds/include/instance/sdhc0.h | 11125 | `58583687fba58d56f10d744b084bbc53187ba30382814cd3f6780908b6263bb1` | 0 |
| external/samd51a-ds/include/instance/sdhc1.h | 11125 | `df6d2fbd0167e23761229fd4ac4a641aafec725adb72a85b2dd4949b3ed971bb` | 0 |
| external/samd51a-ds/include/instance/sercom0.h | 14324 | `3f65c4b6f9ae5a5b286b1f6f084800abf245475a31ad272993a95b87da23bfbe` | 0 |
| external/samd51a-ds/include/instance/sercom1.h | 14324 | `f84e56a416d8e3b5c41fbf6d5bd9fca08120eb6d4a7dee9e9c25a1b8d45983e5` | 0 |
| external/samd51a-ds/include/instance/sercom2.h | 14325 | `a49abb125e29afd3f316fe88e0708ffc71d3f480def6846588dfc4b0b89d538e` | 0 |
| external/samd51a-ds/include/instance/sercom3.h | 14325 | `eb17328f2f56136dbf32859d35fb6fc89af1c708314700c331e5eef5a4686f24` | 0 |
| external/samd51a-ds/include/instance/sercom4.h | 14325 | `c32c05647815f02e3d3101d97e669a3e11fd156445d7dfe8142701fadb05e093` | 0 |
| external/samd51a-ds/include/instance/sercom5.h | 14325 | `91e92e3f7ab720ef079a4dfde7f05ff00fe16268cbe6dc298138d9401082204d` | 0 |
| external/samd51a-ds/include/instance/sercom6.h | 14325 | `fc8030aef0fd7f02e0d42bb452d34add603985af1b7195e8bd17ef4762195ddf` | 0 |
| external/samd51a-ds/include/instance/sercom7.h | 14325 | `1c2ef9acc848885a61abc6914124308a0e5bd06f24226a48f5612e8d6d4b6efb` | 0 |
| external/samd51a-ds/include/instance/supc.h | 3423 | `651194193151b6d77ed9fe6020e2b6ad70b40efc78a2a548d01e30e96a8d5ca4` | 0 |
| external/samd51a-ds/include/instance/tal.h | 51688 | `a80905367a6a552e05fdfa188f897c132b0a835efdd816ec4b1cd8008b34c739` | 0 |
| external/samd51a-ds/include/instance/tc0.h | 7651 | `19940f669d1346c77c5efbe19728cea80e79b3de88d0a1cd736ba28ac93da0ca` | 0 |
| external/samd51a-ds/include/instance/tc1.h | 7651 | `542b7b1ad008902b90cd3c59dffd0ef5640b8857f8599176eeeacb9321a011c6` | 0 |
| external/samd51a-ds/include/instance/tc2.h | 7651 | `891296ffe11d9caf3ec32cc7d863c3f1c0e9ac5d30cc0654fa724928de4872da` | 0 |
| external/samd51a-ds/include/instance/tc3.h | 7651 | `760c2e1ce3a30b703a10e4228bb8e12e227ea229d4ab81bf09d78e8286db0071` | 0 |
| external/samd51a-ds/include/instance/tc4.h | 7651 | `d8247d03d14b3cd1638dc452afce712b5b41757e168139ec2a6f1c0e87dec3ce` | 0 |
| external/samd51a-ds/include/instance/tc5.h | 7651 | `ab7ea618eb9cf37ac9847339e4803174ea72bc015fe67876007a3fdd987b887b` | 0 |
| external/samd51a-ds/include/instance/tc6.h | 7651 | `438213dcae61fcd4798bd91dcafeed5d46c76c0bb75b20a3eeb34d1a605aacd1` | 0 |
| external/samd51a-ds/include/instance/tc7.h | 7651 | `f2a0551d0d3ef280ee7947acba30d3537a13666d495f6000e2fc41f3aac65052` | 0 |
| external/samd51a-ds/include/instance/tcc0.h | 8792 | `26dc7f685789fa6ddb1849fc4a6f4a0c0bc4d9ce26249bfec731e0845d7054e0` | 0 |
| external/samd51a-ds/include/instance/tcc1.h | 7888 | `fd67d160887c270ff92c53a64cc1e5d7b9863923d81c7b3c51953a864c88d9c1` | 0 |
| external/samd51a-ds/include/instance/tcc2.h | 7080 | `90bccf2d7518252739f7504000611782ab85b62ab0833bc45d10e8ad27391fd6` | 0 |
| external/samd51a-ds/include/instance/tcc3.h | 6407 | `3fe8fe6400967da703c0edc321704848ef67b8a4d6294f222b188f55418d9531` | 0 |
| external/samd51a-ds/include/instance/tcc4.h | 6407 | `90dc5f2fcb3949db6db1f69c721df389770292281dea1bba27d50d620bf0c3ea` | 0 |
| external/samd51a-ds/include/instance/trng.h | 2275 | `8d2c8368a9d22e8e863d9d4c270f3992e028b8dd0a64e0a37b31bc6ef0e9ff1b` | 0 |
| external/samd51a-ds/include/instance/usb.h | 36661 | `095de164cca5f9df0f939b93a5290877ea4e7dd569352b16138dcbb199d0bb8e` | 0 |
| external/samd51a-ds/include/instance/wdt.h | 2654 | `44796f78b838ee00b7dcbc8951513e5b08f671818fbb8e2cdeadf3d2d4031a29` | 0 |
| external/samd51a-ds/include/pio/samd51j20a.h | 132487 | `9fe311d69d97adafc1469a6ec45fa3dfc814cf4b7d7d0865101b349a923e8a9b` | 0 |
| external/samd51a-ds/include/sam.h | 1689 | `00190accf1e328471874b96548c5ec1fcaed1a871c7db5ac00cc9d7538f98190` | 0 |
| external/samd51a-ds/include/samd51.h | 1810 | `62c99f36fb052bd36ffdb72931e36de663c944d29bd9b2c93289413d15f2aadb` | 0 |
| external/samd51a-ds/include/samd51j20a.h | 73653 | `cbac37b093963fc1b96a1668369546ab2f419f79243adf725f4cd8ef32a8004d` | 0 |
| external/samd51a-ds/include/system_samd51.h | 1194 | `f7ce006d7b5078b003ed2181e30b582a8c067a9f55b556520019effd512e0068` | 0 |
| messages/antiklepto.proto | 284 | `89caa2946283a469e5c783b9dd886d99728a40dd36b0e6156abe83c025ec9f0c` | 0 |
| messages/backup.proto | 1713 | `4616978a3a2b14c4523d1823c1a2b48373bcf731e5e35ff59f48316ada556737` | 0 |
| messages/backup_commands.proto | 724 | `17a8e01da16b238061f256546900a21af5b3a5bbe150b39e5d519a360e459488` | 0 |
| messages/bitbox02_system.proto | 1509 | `5e3ff16c8571d177180788a164d64bfb61e0e94415307a1f5f861965839743b8` | 0 |
| messages/bitboxsync.proto | 1814 | `8d87a05e25ba6cfec7f68a878906677ed218d64f663f6a20b24724f0d38ec54f` | 0 |
| messages/bluetooth.proto | 705 | `d7944887f55ee5e5196e4c62ea60564ad2a94e9d47257e49d05dbf3c4e805a0e` | 0 |
| messages/btc.proto | 9302 | `6f2fe1d3b1663e2617fd9587e6ec21242d02140624c797f222db4f8a26701928` | 0 |
| messages/cardano.proto | 4114 | `8e11c3628cc98b02d5904edf3a4d21e0492bad53ad74c89009b086e5ff111523` | 0 |
| messages/common.proto | 870 | `369ca12555a7810d196055abb643594d0723c7807fd46e5cca8a4a4ae8421342` | 0 |
| messages/eth.proto | 5601 | `3e2422076d196a16b59f743651cb1d6beecd9dae5a183bfc0c813936d49642ff` | 0 |
| messages/hww.proto | 3047 | `1faae60899577cf627e7c54b319b34f883aa126393d94d0cc1b84471b12cbaae` | 0 |
| messages/keystore.proto | 1894 | `ed5c5d677e3c017c55d71ce274246a4cd55cc8a867b259eaa9be77f204bb45a7` | 0 |
| messages/mnemonic.proto | 282 | `9cd94eff3b2bdd7a9d60981db9f487d2104119088ff7a912a8536654d571024b` | 0 |
| messages/perform_attestation.proto | 436 | `632df1278569322d391e4648de139ddf81ca83b26b5d14a0b3f0818605c0d5d5` | 0 |
| messages/system.proto | 195 | `706284195da36379d9d511f54e0ecc6a910b8fa8fa8158a47459567129fde382` | 0 |
| py/bitbox02/bitbox02/__init__.py | 882 | `d9c472a05bb8d5684e48938e061b5f9a10eb405c53853b22791c338f8ff5a13c` | 0 |
| py/bitbox02/bitbox02/bitbox02/__init__.py | 1148 | `cfcf44d5cca32b8142d9d7d93829f89a61f5b77eaae024476f471a6970ce5976` | 0 |
| py/bitbox02/bitbox02/bitbox02/bitbox02.py | 60915 | `fd62ecc298b45f0684968cf1b77d2e8357fa01583c3be6699e39867b633d7ba2` | 0 |
| py/bitbox02/bitbox02/bitbox02/bootloader.py | 10571 | `25ca224abc783f35996b1ef338e852eda9ac34329dd627f266689f18578318ba` | 0 |
| py/bitbox02/bitbox02/bitbox02/secp256k1.py | 3700 | `6903d0adce82573c7e3b5bcf40ef4ab09b964b5ff859bdb408365f6694abb670` | 0 |
| py/bitbox02/bitbox02/communication/__init__.py | 498 | `0cc6de915b3383e9c0c26be6d9cdd0f8edd701517b8c94748433f2d801125a0b` | 0 |
| py/bitbox02/bitbox02/communication/bitbox_api_protocol.py | 47007 | `5aaea77dde27d11e51bb17dc8f73451971d82c0cfd475e0c543fe3811b867e1e` | 0 |
| py/bitbox02/bitbox02/communication/communication.py | 1047 | `bf927b525b0f3b6800b71bb56a3a0b531137820715148467eb7217dde046fcf9` | 0 |
| py/bitbox02/bitbox02/communication/devices.py | 4522 | `27e2ceab732301eaa115fb5cc655414d7f496d56a146d42f71e290664ac6afb3` | 0 |
| py/bitbox02/bitbox02/communication/generated/__init__.py | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| py/bitbox02/bitbox02/communication/generated/antiklepto_pb2.py | 1401 | `002c48b4a60d4ccffed0d11a0c9404042ee25ebfe11eafe363d0eb3e383ad33f` | 0 |
| py/bitbox02/bitbox02/communication/generated/backup_commands_pb2.py | 2102 | `76a031ae9de53c9cfee71697e9c30ef36e3cdf6aa5c93a0cb6181d94905eb116` | 0 |
| py/bitbox02/bitbox02/communication/generated/bitbox02_system_pb2.py | 3362 | `7b7336678c9891da9d457a05d2e4f8dea403d66b6464c0ba652c580858db0000` | 0 |
| py/bitbox02/bitbox02/communication/generated/bitboxsync_pb2.py | 4721 | `4d1ccbc51d2721ca65b8b0f552e0b9b823ca3f7de898e6ff7300b26df8ef4ce9` | 0 |
| py/bitbox02/bitbox02/communication/generated/bluetooth_pb2.py | 2457 | `e1b063fbcae61d5359b0f75ae7e27239e0b1330f13b7fdba49bf6ff48301113e` | 0 |
| py/bitbox02/bitbox02/communication/generated/btc_pb2.py | 14672 | `a81dfc78da5294d567398b1deb8b958be2bedbf46723673be413d378796a92e6` | 0 |
| py/bitbox02/bitbox02/communication/generated/cardano_pb2.py | 7698 | `7438e0c6df1a52b61d83ae7b37c508d1abcb23c08d68d7c5a98b97dcd337aa84` | 0 |
| py/bitbox02/bitbox02/communication/generated/common_pb2.py | 2044 | `f76860eac5b1fbfd43107106e5bbd88099c9c8064c6631b2213c89eb25777678` | 0 |
| py/bitbox02/bitbox02/communication/generated/eth_pb2.py | 8782 | `9672d0458e47e65533e4b4937c669a8a95679ba59375ae6e30373c0ef6cd098f` | 0 |
| py/bitbox02/bitbox02/communication/generated/hww_pb2.py | 6892 | `9ef9b913ec39d1b08486e630c41481a129488faba729f1096ffa99261d78fc43` | 0 |
| py/bitbox02/bitbox02/communication/generated/keystore_pb2.py | 2898 | `5a7b7c7d197d889cf23bf0c7f0daaf2ed95d85967cb571ede2e7ca0a5c913d27` | 0 |
| py/bitbox02/bitbox02/communication/generated/mnemonic_pb2.py | 1386 | `c30ee7944adbbac452288b0b7580c9da11e24cf6ba3fb4b42ca5cce259cf4eec` | 0 |
| py/bitbox02/bitbox02/communication/generated/perform_attestation_pb2.py | 1444 | `4177a19aae7d7b3ffa532606295188ba87475e9650bb4af0ef55906bd8d7e014` | 0 |
| py/bitbox02/bitbox02/communication/generated/system_pb2.py | 1186 | `52405697ace035f84e1743af4ae4046f550c6de80a10a9ef9af3bad8a3bb9b6e` | 0 |
| py/bitbox02/bitbox02/communication/u2fhid/__init__.py | 159 | `7583c55d986b90efdb2fbbd39b022968f6e1fcd3e37c01ea29250855d2f0d92d` | 0 |
| py/bitbox02/bitbox02/communication/u2fhid/u2fhid.py | 5339 | `6791dd27b621d46a37729704ab182f7b4cd89d45d592d215a4a172edb988ffc8` | 0 |
| py/bitbox02/bitbox02/util.py | 7474 | `d879c3f4c1bfa9a9166d8974bb5fe4e1c63bc2807100a2edf2f2d29d17f86cc0` | 0 |
| py/bitbox02/setup.py | 2374 | `df4b02be80f5664e130fe7329538a87a81341f796325ffa3f93966080edaded8` | 0 |
| py/load_firmware.py | 12912 | `c2e8e0955cd508374d023dbb978c7dc45b4dd30a81f168475ed1f84ccac8f542` | 0 |
| py/pyproject.toml | 31 | `55e581d5626a46609d16456b1d075222dd645f52d16bf493bf44d1860272c98a` | 0 |
| py/requirements.txt | 152 | `055756030dfe1bc5d65a42ef9e785f015c7170aee3d15a766dc935383e36789a` | 0 |
| py/send_message.py | 90420 | `c9c1cf0d64bb467e00dada86bf99d1f0b86c0c5d1c5e709c2e150b26a70e1795` | 0 |
| py/u2f/__init__.py | 563 | `42a99f304be6223c23109d3b83492abf5bb4c4b30e50794c496b0b60c203fa92` | 0 |
| py/u2f/bitbox02.py | 3558 | `28f6b2e9fff944c91ff004ae53ec8b14b50518764fefe1587ae8ecdcf9ad8810` | 0 |
| py/u2f/u2f.py | 11815 | `5e0fd84da87b2f0183ae0f3c1183ee247b909937e6ca4421008dda805c85fcf1` | 0 |
| releases/describe_signed_firmware.py | 3419 | `61ff7716f98d83efff1ef364c6b173bf7deeca2662caea3c83a9f9ec9c86d399` | 0 |
| releases/pubkeys/JuliusWiedemann.asc | 3199 | `4c174a88f6da9f8d93faf08291aa32101e69017fa73102d353c63eafadcfac85` | 0 |
| releases/pubkeys/JunghoonLee.asc | 3139 | `33671dc21911a1750070735f332cce7c84380bd1ab7cc74fd69714f40e69cf7b` | 0 |
| releases/pubkeys/My1.asc | 4618 | `c3884ccc2c92a15ad9be2523730182a40d523e5a3ec3a4b9abfe761cb23a1bf1` | 0 |
| releases/pubkeys/TheCharlatan.asc | 20351 | `c229c79d3677332d6eb406d406e2c7daef67fcad6439bb8224c4e3b3ccfef1e0` | 0 |
| releases/pubkeys/beerosagos.asc | 3134 | `77547ad2b0bd39e591192f3d4df3e57e48c6acc1cfbcf7a7a4262018473dd7dd` | 0 |
| releases/pubkeys/benma.asc | 6238 | `bebf447de75bcc5015b0f9699a459fb21f61c230bc1a54c29b62ef3c8c153824` | 0 |
| releases/pubkeys/brianddk.asc | 2513 | `fa82b4b5c2c4dd6c4066aa113212f89e99aa6f33c29f6c2ab57931566a422c5c` | 0 |
| releases/pubkeys/cstenglein.asc | 3175 | `1697a4111b88a52d7a7d7ccc941ed11338d9578732f05fb0b2569e2eec94d170` | 0 |
| releases/pubkeys/frknakk.asc | 3139 | `a3d9760761bedbb8f2b156c0d5fa3551e5aee570659e92af6e6752daf041911b` | 0 |
| releases/pubkeys/guggerf.asc | 3139 | `1b1ae8bf1e853163d565a32344854b57b2ceadf9246384b7fdbc26fd19f2f586` | 0 |
| releases/pubkeys/jonathancross.asc | 167853 | `4092962b5065adad6acb1602ef0a0d5f20f32af83d52ce3b18564fa92a15c795` | 0 |
| releases/pubkeys/nickez.asc | 34777 | `dfeee318e1e971fadd704779c023b0690800b63656d4f56e0c5052c9d62cd581` | 0 |
| releases/pubkeys/offbyn.asc | 14696 | `b6136c3272711fcddd8ca49f9916a79a54677bbcb38a32859112cc067fd6ebfe` | 0 |
| releases/pubkeys/psteiger.asc | 648 | `fe123e4a583a9dc4d271ffd0af7c54ec135728575a5c171dc0fddbec285201ab` | 0 |
| releases/pubkeys/stadicus.asc | 6892 | `6b7a866cccd4028fc58c5de6f8629919f7f5062c32e58c7866ead6d538cb79f1` | 0 |
| releases/pubkeys/strnbrg.asc | 3175 | `3c725e0b54589026d856b7050b29c6c2c323306e2c1a8261569552a6b8539d6c` | 0 |
| releases/pubkeys/sutterseba.asc | 3155 | `5c279fb6619893e66372f5752c954d79a586920b49367bd3b681ead39e46e103` | 0 |
| releases/pubkeys/tomasvrba.asc | 21018 | `88b2e37b7a8cccf75e40f7019a669f4699237716d38831d0c29108cc0835a8e2` | 0 |
| releases/pubkeys/userofreddit44.asc | 3772 | `e67ca6a20f1bee441598fe784ec7789ceed4a82e0a1c725deef34efde1dc3a94` | 0 |
| releases/pubkeys/x1ddos.asc | 7091 | `c6cd70e5656c75ac96db731fcbc37c6cfbb26f0d1720a0f6b8ac3181379f48eb` | 0 |
| releases/pubkeys/yaziza.asc | 1530 | `2108a376fad98106ace21d60169de8eef8cec4dbc7626b66b72765e21328b0b0` | 0 |
| scripts/bootloader_update.py | 12651 | `942f2c3383a9d764a1ba19dbaf1742af5641f6965d9bffeea6a46e21534bd394` | 0 |
| scripts/build_config.py | 9820 | `6eae2fc0b63a3637b2192c0195fa2dcabff85fc7370089f40c3dc8995514a3f8` | 0 |
| scripts/build_product.py | 4631 | `4d5d00b246a2428d721c05d0229b8d171dfcb5d8572c0b8cb531e6d799cafc31` | 0 |
| scripts/copy_st_drivers.py | 11544 | `1fdcf9f29b9e4a51531bf8e3108e0cbe4af5f40c4482438b725b01b34e870a17` | 0 |
| scripts/create_release.py | 14352 | `ffdeafdd62d7c7b55ac3916bc170791df35c44e4b190586410cc9da7bbfd0917` | 0 |
| scripts/create_release_assertions.py | 6458 | `c2ac06c2099ada49cba1eabbf77d97164be0f20609741e05e03eb7fc8519a254` | 0 |
| scripts/generate_version_headers.py | 17004 | `675bbd250e4d75df70f430abc30595ab8bc0ebf69592a44982a6e71f7747a994` | 0 |
| scripts/graphics/convert.py | 1832 | `9488be1ec0cc6aafd3f9d88fdaea5fb226f4e3dc628b26895cae23dc183dc7b1` | 0 |
| scripts/image_header.py | 11499 | `b0b7aef7a47fb3ebdf6ce8309aca81c87d78d940aae82395afe7e3e3914bb822` | 0 |
| scripts/probe.py | 5185 | `1e00bfa09028e533e317890133a1a549ba9f04f7d0aab89b3ae0ec1ac18a8890` | 0 |
| scripts/signed_firmware.py | 3144 | `480f05f317d9cb451a3d7e2d3b5e6ce21149cf7663a0daea2b0863b7bc4aefa2` | 0 |
| src/atecc/atecc.c | 24952 | `b08f8a566a7090a9f9ca736145e9565a28add3f47c8572f3a3013d56551d7266` | 0 |
| src/atecc/atecc.h | 1332 | `fa90590d9c07db88f66b7714dd7e74603c2f5c228332228df162c9e3e1ce3af0` | 0 |
| src/bootloader/boot_args.h | 1954 | `4211ed331ec60a4cebd8a66a05bc924d06a1eaf6808d6247d96c5a495b57cd7f` | 0 |
| src/bootloader/bootloader.c | 36479 | `f168d61e94931ac4ebd646e1317716b95b7ceb6ad14a2642b08d46ef28fe4d6e` | 0 |
| src/bootloader/bootloader.h | 589 | `06c21dcaacb655508bf4cf0f7fce19c7b556c589717595a45fb348c1c3b81051` | 0 |
| src/bootloader/bootloader_format.c | 2480 | `a8d11e946c4155c4ad0bd9cde5c67e6bd7bb2677af3e2a14dae78252e1720c43` | 0 |
| src/bootloader/bootloader_format.h | 1521 | `201e9cc589180cef9de3abfce4b2e98139402faf6b99ebe9accf5a8313f1b583` | 0 |
| src/bootloader/bootloader_product.h | 1455 | `bc0884527d99033bc323721392226a690153d3f874fd573493e02a3d1db6c467` | 0 |
| src/bootloader/mpu_regions.c | 4998 | `ce6c37a9c92a7ef982192a5e7e1df86a4f147fca5c9f22735276606f4124f870` | 0 |
| src/bootloader/mpu_regions.h | 633 | `2e0d365b60c5f4af7308cc1a3bf726beabda6581ad8d989ad111b18062b66504` | 0 |
| src/bootloader/stage0/stage0.c | 21703 | `e7602bdbf3060508b511e757832adbe9a9995bc6dd13477ba481d8970abdbdeb` | 0 |
| src/bootloader/stage0/stage0_descriptor.c | 648 | `e466f37f5e5ab14d521c3bef5ca673a0d824a5dad24bf67b0616d4f7bb9e21a6` | 0 |
| src/bootloader/stage0/stage0_descriptor.h | 1483 | `9a5d822def8bdb79e9505ef0453bb8214024bc4667d893f4beecad143f650d5d` | 0 |
| src/bootloader/stage0/stage0_flash.h | 7485 | `923840cec8b59d2a0150b15a393a36ff4ca70547602a3769a1475073ae838c82` | 0 |
| src/bootloader/stage0/stage0_runtime.c | 1000 | `27538c86f302b07025f7be542832db5d2843e8fa6893bc523724968ad4486e31` | 0 |
| src/bootloader/stage0/stage0_startup.c | 1872 | `570ef28ad3f830c70d9713b0dbe9a2323172df00e1240964459cf0541a447881` | 0 |
| src/bootloader/stage0/stage1_sigcheck.c | 9311 | `5704d66ba1ca763bac3bd4e998eb68c26d63ddcc74c8912267a4d5cfecd9a083` | 0 |
| src/bootloader/stage0/stage1_sigcheck.h | 333 | `cd78c8accb34bfcc118cdf91425314a0a79cd67d91eeb560080cbdaecbb1a602` | 0 |
| src/bootloader/startup.c | 7383 | `0790af69af4ff3105e7b5be5f3107d14a66043b7ca893f402be9790b49b62a67` | 0 |
| src/bootloader_upgrade/bootloader_upgrade.h | 4938 | `5509b50fcadf1b81604abb566a2655e91ea46525627c4bede0ce55cf00629753` | 0 |
| src/bootloader_upgrade/firmware_installer.c | 6308 | `fbe4a58ce6c5ee5a49b10482f7cb082c5a5ab846d7cf4dfae408f3cf86689374` | 0 |
| src/bootloader_upgrade/firmware_installer.h | 198 | `db2fe193d39c09380b6cec28f9190146e837048cf3c9f7ff5473ecd2ca551bad` | 0 |
| src/bootloader_upgrade/firmware_installer_check.c | 3641 | `2ffa4ba9da129ca84ec2eb826fa2233378ea07bedd12e6188c32a22e7889a5b8` | 0 |
| src/bootloader_upgrade/firmware_installer_check.h | 626 | `e6b04cd3dba6479e1d4a52f0d018c75bfa28ec4a531cc5641b5804f8a6137df7` | 0 |
| src/bootloader_upgrade/stage1_pubkeys.c | 1453 | `d0dbfb66799b31c124d1d47a5536b3d0ee40afb323563a7f2104668ea43d5ec7` | 0 |
| src/bootloader_upgrade/stage1_pubkeys.h | 268 | `6861334872aa5690cb7d9c0f6fca8b2da3c0224ccb1f2e09c2898ef50a6cc4e1` | 0 |
| src/common_main.c | 2237 | `6a5a78f034fdb3ff90f6b29937b3f7370b75996d6f8599ae1f28d5426580b1ad` | 0 |
| src/common_main.h | 258 | `00c2607686f4b979a45b494dd6465be74028d95f3758fa9cdcccd3b4b4a09011` | 0 |
| src/compiler_util.h | 156 | `766b232901874eff32c3045b845cdbf8b7f26bede78a78e6ea66668b04bef762` | 0 |
| src/da14531/da14531.c | 148 | `0e137eb5f9ed0c6017372cebe6a13c665f179c73d7ee74c5281f6ea3d5b5ccd4` | 0 |
| src/da14531/da14531.h | 757 | `699f504277cca1dec2db35d3a729c3d2496af56bee2d715460a9cf8bca9007aa` | 0 |
| src/da14531/da14531_binary.h | 615 | `ab36b4d19ab2e92690987e13a9bb764070dc4fe1b37f582b13dfb1920dbd7378` | 0 |
| src/da14531/da14531_handler.c | 10934 | `470474701180c1c3a831ca43c73b3323456cc31f063eac2cc536b77fe5cd8a9c` | 0 |
| src/da14531/da14531_handler.h | 488 | `c4f4950fa1e7095bf80defffee2d29224512c369d4d42a51c3b37b7f7a9a0075` | 0 |
| src/da14531/da14531_protocol.c | 14092 | `fccf1437f23c480e2b2675366367ab4ce8d4f41ebef6584a5c729f14c0a32697` | 0 |
| src/da14531/da14531_protocol.h | 2026 | `b35f9a6a828becdd2ae5b9e93f8615982afd923518df14ee269d34d27493c248` | 0 |
| src/delay.c | 2214 | `d9b814da8a0b29b9316c7d4d9062aad566376b3f580111e44e62b572c218aaa7` | 0 |
| src/delay.h | 527 | `b181e4281855a1a7ee890769b72d7884157729456e11760b93319ea8065c54ff` | 0 |
| src/factorysetup.c | 40551 | `f23340c080fa71056e24109f64c2404ff90acf2b6bcc516e5daa267731c94e18` | 0 |
| src/firmware.c | 1346 | `e8c3cd856d1329684a6519d907dc516953a5da6260bb895cb8288986fa80058f` | 0 |
| src/flags.h | 4465 | `20b4d9f439ebac1783b6a6a9b58d3f44f5795a4da84148d9f7772c2d7234fa77` | 0 |
| src/hardfault.c | 1227 | `5d2a769cf3e77da97afcea5b416c9853b2c8db0db8bfb6c52a9de6345d16eea4` | 0 |
| src/hardfault.h | 858 | `5944df9738bce65d30ad8a83310a4ba489613bc075efd653c2807edd20232a12` | 0 |
| src/hww.c | 8090 | `a01aa7f5b50ae9766c9316cdfc8a4fea04f22202b5dfeec770bbb2042e3496f7` | 0 |
| src/hww.h | 1190 | `3dc95f986eab99ef6868410b64498f5af12e661ab68871c0c8c6f61912b85fd1` | 0 |
| src/i2c_ecc.c | 2276 | `ed06ab53c14f7911372708f60f040238decc514e7163c2decb99e8db658ffc96` | 0 |
| src/i2c_ecc.h | 1462 | `c36dd2e4b88288c1d4d5422884b2eaf273edc3973dc880ea06c30f3035a59496` | 0 |
| src/memory/bitbox02_smarteeprom.c | 4544 | `2d4869e79d0baa5614a11659bea610b382cf25f17fb5ba76683cacba93dc0eea` | 0 |
| src/memory/bitbox02_smarteeprom.h | 891 | `a014fb1fc58e11fcd563a9281dd3b992c0aa75385b54be6124ae950e85c32ad3` | 0 |
| src/memory/memory.c | 35229 | `10d47933c8921fb95a5c15b3e91291f273a5ace9f1ee9c98568bffc8c894820a` | 0 |
| src/memory/memory.h | 10717 | `f5f44c8b0780a106f193a012d03db97abf90230eed6b88491df8146610f95963` | 0 |
| src/memory/memory_shared.c | 8175 | `4b5997eff681a1063e56e689a03adae0a6edfa5ccddd5eb12f966c759096bb9f` | 0 |
| src/memory/memory_shared.h | 5977 | `b7c85bf18214d96b882c4e5ababf4bfe5194a8d29e3db15d9d07dbde50912f5b` | 0 |
| src/memory/memory_spi.c | 2980 | `5c7ec0943599eb710ab7d2b1681fa72fa2e7148ad26f1f2d73e90127682438e1` | 0 |
| src/memory/memory_spi.h | 1279 | `8810697f34c32b38045a4e398daf86d59353a28cb0b35a9bfe0bb39e4bf3b49a` | 0 |
| src/memory/mpu.c | 1183 | `428c3a5c05260bea2d6c8fd7a9648904c05ef48e756ce13d54ec8b2cc49a8919` | 0 |
| src/memory/mpu.h | 3189 | `e3e8eeaa6c7f657e82c8afbf80ee43af9268ac058bfe93c5bbe289012097de4c` | 0 |
| src/memory/nvmctrl.c | 383 | `51c13e773d9816fa9b3d8a4fb402ca07aec6d745072f4616c3c04a7dec09ad50` | 0 |
| src/memory/nvmctrl.h | 312 | `eb730b09fd1ba0120da5f956d8dfb4d2a39f5ca55f8660d8777dd1ab59717937` | 0 |
| src/memory/smarteeprom.c | 5033 | `28653e4583b809e72e8bb6104a23db25c6fa963dd12f0a4b7c9b142fa4d961e4` | 0 |
| src/memory/smarteeprom.h | 3092 | `eac71c154b3af713597f18c878aa2c2d2b72b43a811df1220b46710b27f07a42` | 0 |
| src/memory/spi_mem.c | 11033 | `9f2bba7727e4ee26a6e3c29b3108259feb98bce5515d8397ff9dff907ba179d8` | 0 |
| src/memory/spi_mem.h | 3912 | `032202c6f683a3a269ceba9e51ad78d9b11bd12924eb29b765caf3ea09fc62c2` | 0 |
| src/optiga/optiga.c | 36862 | `d81c6f4b45d9923458bf7b218170acfaf729a6d36876d9bea34b848e03c6a54f` | 0 |
| src/optiga/optiga.h | 4906 | `d992cdf0cda34979f1a75dbca2c1307f5aaf6fded168246fe36a9e771bdcad96` | 0 |
| src/optiga/optiga_ops.c | 5215 | `faeb33491aae26ecb601778ffad183100f4fd698bda52e9b1321d353b69b58ad` | 0 |
| src/optiga/optiga_ops.h | 1694 | `ab2ed1d32962652a76c14fc95fd58b1ad24d273d3a692a896d2cd23ab4a8055a` | 0 |
| src/optiga/pal/pal.c | 1558 | `3769a1635f88870578cbd926257df76749f1b9774f78bcf82569fab8efe527a7` | 0 |
| src/optiga/pal/pal_gpio.c | 1979 | `89e0f438ddc439ed69d259aa4f760fe92f41f2f5751fcd1b570b21a31d00912e` | 0 |
| src/optiga/pal/pal_i2c.c | 11391 | `8e9c342201674cdb6241e0b3fd9dfc7efa17100944b49c8660fff0dec82071fa` | 0 |
| src/optiga/pal/pal_ifx_i2c_config.c | 2906 | `e4ff9782e587b6fb265086c5dace6a2ae8d2d15709d7a79dcd085ca48e731303` | 0 |
| src/optiga/pal/pal_logger.c | 2858 | `ed4810ab3dbb786ec7cd1902053f342869822b9ff765497cd256ff1887a73de3` | 0 |
| src/optiga/pal/pal_os_datastore.c | 2763 | `178127d32e56421ee047b0cc0e6ee0afa935fa85c717c7da6cdf1c8fa2306195` | 0 |
| src/optiga/pal/pal_os_event.c | 3355 | `245c5a1d4c696fdbb90764e6b2b5b8dd59fd531929e856f3a57b2916eadf6ae0` | 0 |
| src/optiga/pal/pal_os_lock.c | 2603 | `71ffab63bbf2f395b09df0a1b198a6d418473d35b06263f64639816eefb08709` | 0 |
| src/optiga/pal/pal_os_memory.c | 470 | `7b29109eb25ffa9f501f444ac0e7675a8e9cea8068a395a6b85ef59864105eff` | 0 |
| src/optiga/pal/pal_os_timer.c | 2550 | `ecf6f183c7cb7b6c865f9e58ad392ebf6a69718c7faddceeceed0beeb8642b55` | 0 |
| src/pac_ext.h | 654 | `1b829db5cbc08b8d68626be28855dc5508bd39233aadb20cd5b347b39b84c0b3` | 0 |
| src/platform/bitbox02_pins.h | 1308 | `7b73cfee547ae31cadde79c3c727001b7f8268b132a446d7884bb78401ba9d70` | 0 |
| src/platform/driver_init.c | 13012 | `ce0ab53cd6fab718023fca835d52705f61e6b1b412d85fba33e74dec346e7189` | 0 |
| src/platform/driver_init.h | 2021 | `057862dc09feac0d0d67e191dd027d26cc0d91677b29838111b46140d1b1f745` | 0 |
| src/platform/platform_config.h | 1732 | `c6a8ff515fcf1c87f79c366b42870d3ad34b09adac5b02a4d6451b658b2b6374` | 0 |
| src/platform/platform_init.c | 2465 | `cc2d88ab9b7eee346288271974f1200f40ce6b33f233877990d1889a93961a6c` | 0 |
| src/platform/platform_init.h | 359 | `d4c05fefa903b6446086660da71863f44bc3baa11b76f7148caf14815c026123` | 0 |
| src/platform/sbrk.c | 1187 | `5552fa9172238701b473d3b0bfa0df1b1906e85037596958d12305850e73c8ad` | 0 |
| src/pukcc/curve_p256.c | 4832 | `f4aba16f4398bbf89102e62b826cefc8c02d3a4731a73387393d48a864a8b212` | 0 |
| src/pukcc/curve_p256.h | 211 | `c620f92a051fc37d6c4b976a72cadc61f24595dbfa1dfed6326dddcde19f1225` | 0 |
| src/pukcc/pukcc.c | 9798 | `b5049dd725362a4217e5797928ba8ad32e3c7235d029f366a411e38631151540` | 0 |
| src/pukcc/pukcc.h | 1169 | `a7650ddfd0bfe8a9c23dce685d1d648c412ea08b65c28f1403569071e88d5e74` | 0 |
| src/qtouch/qtouch.c | 28561 | `a3ce935421670987dcc50cbb7fa710d2e507fd5f5dff108a1c53ecbc3205da6c` | 0 |
| src/qtouch/qtouch.h | 10273 | `ece235d4e91d9b3b459490b835463f2c1e9a621ea7e327c42cc5c4eb0a917a86` | 0 |
| src/random.c | 2290 | `8e70d7c104bf78ace2348c526b5e4e12625ad8bb56b0938be2bcf88421054019` | 0 |
| src/random.h | 711 | `8c2bca629ef2ac0214138b7c3756b271540426323fb18c0a80b1d1a14ecfd64b` | 0 |
| src/reset.c | 648 | `817e226f032c6a0fc76fde0f4906ff0c6151f609bb4d6c38d4fc86bed4e074d0` | 0 |
| src/reset.h | 243 | `7050c993ba457968af7b3411d33e22754620c9aee2a8000305488e92ea3653fa` | 0 |
| src/rust/.cargo/config.toml | 1932 | `a6bddaebf210d9245b6e206167b95b578e86e14a44e8ebf6c588fd7ae3669b72` | 0 |
| src/rust/Cargo.lock | 37444 | `26c6fdf274b15f25b33b594f5adaae1be5d54998c1ab4584a91a53be681c323a` | 0 |
| src/rust/Cargo.toml | 4099 | `73bfb23592887b4a84691a76f5034f4c29830dbcfeff26eb17d8b6e5d9dbbce4` | 0 |
| src/rust/bins/bitbox03-boot0/Cargo.toml | 602 | `b45eb014db8ef2e7ac79a791989422bcfbae6bf8e6bd6254b37d887b5fae035e` | 0 |
| src/rust/bins/bitbox03-boot0/build.rs | 1188 | `ce807537a25ae8a54e4d07708b44fa86de7cd518bd820c4fd493cf05378d58ae` | 0 |
| src/rust/bins/bitbox03-boot0/src/main.rs | 1411 | `65d8b40c8876936d6b38e3fec8aa11fdc622c8a984a0ba697abe7bdc3f01d7c2` | 0 |
| src/rust/bins/bitbox03-boot1/Cargo.toml | 602 | `dd41d2262a5b31bb5233966eb1a761d326f1ceff70144a451f406eb427bcabaf` | 0 |
| src/rust/bins/bitbox03-boot1/build.rs | 2885 | `56d2bc01330a026f7ecca4fbdd782a6ab33a2f99e50a75cbae2f8f449b962151` | 0 |
| src/rust/bins/bitbox03-boot1/src/main.rs | 1452 | `5147e04dc133dc02a987c6d5fea26176da929eb8adbb89d36cd5786ad81a90e7` | 0 |
| src/rust/bins/bitbox03-factorysetup/Cargo.toml | 900 | `7e0ad6e8bdd8aae31eac633c9da465cbc325a4b27f587e3a6f320c75ffddc1de` | 0 |
| src/rust/bins/bitbox03-factorysetup/build.rs | 2285 | `d29edafa35af5298df345ada8e61b938812591fb73cf0655bb022b7375a20d9a` | 0 |
| src/rust/bins/bitbox03-factorysetup/src/main.rs | 3628 | `a253e1c4415b9ffd333355e274b1ec08c9cfa1adc0eb9af9cbb97d6cfafd589d` | 0 |
| src/rust/bins/bitbox03-firmware/Cargo.toml | 819 | `93fc8dab006fc6c5b9b5336b7ac129445d9a47a4aca353989674a928a3244ed1` | 0 |
| src/rust/bins/bitbox03-firmware/build.rs | 3198 | `a7109b841bc352e2af96fd651504faa5bb14d263843df3f99a3e177fe2e5d179` | 0 |
| src/rust/bins/bitbox03-firmware/src/main.rs | 556 | `e02dc06cc0918423fbc2fca5b373064fd2086c68ee174e9e7b41fb218f8e9860` | 0 |
| src/rust/bitbox-aes/Cargo.toml | 315 | `f8c0eda103f0f2a76ea59a2ee7469215f09951ef490a28b9bb1a1c478ea0dc1c` | 0 |
| src/rust/bitbox-aes/src/lib.rs | 189665 | `d1b6231d59cddb178fbde87ab0f9ab35fb8bdbdc5c1d197e8298dfb13f5f2394` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk-build/Cargo.toml | 331 | `f3b43b17755cd35be3bb7cdc2a5a3f635864ba7a72098d51c0898bdeb1608477` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk-build/src/lib.rs | 2349 | `ef079b608145f4834765b3aea1cee1f7ab519853e1e9892f712d8b3fb2961721` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk-sys/Cargo.toml | 363 | `e86eece21be38507a20b4c38642399bf2e5d404343c0ad8ac8cf39708cc7644c` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk-sys/build.rs | 4573 | `94c13a1fdaf427adcdff8c386e2a44644c58c21ea8e7f2e7261fe8024b867922` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk-sys/src/lib.rs | 272 | `1b57158882a13471de4be80cc918e22e9628a33222e9d20fdd21b2cdedeb5d45` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk-sys/wrapper.h | 141 | `100e3781691854b92ceb38c0eb2f61f40f7da3c1245e7b158a6480dc670c0a5f` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk/Cargo.toml | 497 | `b41260fdc41c8a6146e9325384c72c19e3eea5bf026ca13af9e370bb0f85e87c` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk/build.rs | 2484 | `342a59fec95ff796491f0382609d4885c17a70bd9c4ca4350cb5b7065cdd95c1` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk/src/lib.rs | 629 | `98780551b6e10d5bdb56bca266d7c84c7bd5b2f1ec9cfb4d985cab2383af6d04` | 0 |
| src/rust/bitbox-board-stm32u5a9j-dk/src/memory.rs | 4370 | `59076a19e7152ab2f5a5aab0d9005a31fdfa297bb68e03f37a18b32f32f22999` | 0 |
| src/rust/bitbox-boot-utils/Cargo.toml | 143 | `25690b5da7d4452621cd5ab17a91bea7ffe634075f88dc5a97bba49181347b6a` | 0 |
| src/rust/bitbox-boot-utils/src/image_header.rs | 3066 | `0a54aa9230fd76555626b278bfac1ea7a7a280d93ac20635a1efb26c11da3cf7` | 0 |
| src/rust/bitbox-boot-utils/src/lib.rs | 22385 | `517532d8b9006f867adb50754bcdbf773e43afb4fc7e90abfbbf0ace89ef9234` | 0 |
| src/rust/bitbox-bytequeue/Cargo.toml | 230 | `1b9256563d1f7b139b57c44e71673f17b4e6adf34023ebfddb15a93c839c0f7f` | 0 |
| src/rust/bitbox-bytequeue/src/lib.rs | 11527 | `a297010473f7b7f5043a2cead7181cccbc5dd5acf852059bd2ccaa55f7bb00ad` | 0 |
| src/rust/bitbox-core-utils/Cargo.toml | 535 | `ea9a88c066735da317bb3c937e841a12c93b005dc41cbff7647080dbefbfc1e0` | 0 |
| src/rust/bitbox-core-utils/src/lib.rs | 103 | `0096bd43bcfd4ce09e49a2e95943e5bf27f8f73611d08b61dcbd9f061f5ba220` | 0 |
| src/rust/bitbox-core-utils/src/random.rs | 4073 | `27fc4f4a389b1010b5ce0f37de67f00751724b1a9fdf83d10e2e601ab42a8b35` | 0 |
| src/rust/bitbox-core-utils/src/salt.rs | 1973 | `0a5be445ef7f2d5a2b1df43462fff5b4dd52b7a2e5cb6e5492ca6054f61cd035` | 0 |
| src/rust/bitbox-da14531/Cargo.toml | 401 | `dc7a28ec383a3eb83ecb0f364d10b1da99b32f8be098e990488693c4fa075e79` | 0 |
| src/rust/bitbox-da14531/src/lib.rs | 7209 | `ff8cb7cd0e1ee5290e86ce22f3629aec737ebde2ca1ca5cf87334d3886e717a4` | 0 |
| src/rust/bitbox-debug/Cargo.toml | 275 | `82ccb7a869fb1c4fcfa222bd5fa9e74389a268f45d746282a625bf40f4219a0a` | 0 |
| src/rust/bitbox-debug/src/lib.rs | 949 | `140a69f4d3b87b65e651e7af56f409c94b8db6324409636938c2444879bbf32c` | 0 |
| src/rust/bitbox-executor/Cargo.toml | 267 | `98befdb3a6d49e8b576b0ac2f21918db7f94b0d24620878be6e3c2674b81512a` | 0 |
| src/rust/bitbox-executor/src/lib.rs | 7140 | `facd59247f5511a85d021b99e248223d4c98ca45e97a89fd2824f900fe3b061a` | 0 |
| src/rust/bitbox-framed-serial-link/Cargo.toml | 360 | `0b715df72f2c74113151e0b699e79c6661e8f2091e0bb80434aab754a2ee4e3f` | 0 |
| src/rust/bitbox-framed-serial-link/src/lib.rs | 17048 | `c97d73bd553608be30463d109f86b23b0284e973c5ffdaadef961aadf00dcb31` | 0 |
| src/rust/bitbox-hal/Cargo.toml | 252 | `8e639839c006a38521fe6ef232ce70588f8b88a404f68bf0053526fad2d6dd6d` | 0 |
| src/rust/bitbox-hal/src/eeprom.rs | 1948 | `200715d25813eeb9d50c237a7c8d4a0861cf7de64d38f81b6fe0cff849389a93` | 0 |
| src/rust/bitbox-hal/src/lib.rs | 1913 | `456f9367a84f57322c65ae911c5e1aeb41c33c020343204d4b78db1d02a42e97` | 0 |
| src/rust/bitbox-hal/src/memory.rs | 4151 | `ed950634d4ebb11fa50c62f323f2dcd92901986820d8c0d769146e9f31f51d4e` | 0 |
| src/rust/bitbox-hal/src/random.rs | 172 | `3d53abdd13fc8d9c29b0534d41864d1f8fb97c9a04c38da2ad112fc391761b8a` | 0 |
| src/rust/bitbox-hal/src/sd.rs | 588 | `7a3c3a204b2985238560a1951307ae884f86f5c9c76e66391b0ad84981381306` | 0 |
| src/rust/bitbox-hal/src/securechip.rs | 4226 | `da71595a0cca42f468cb939ff2a6fbd9c62eed395caf4d4d16425a1f8d3bb36e` | 0 |
| src/rust/bitbox-hal/src/system.rs | 1019 | `6da346170863b3ba80e5d7ab3e456fa322d94d0a36ab1e1a1769ceb3cfd87771` | 0 |
| src/rust/bitbox-hal/src/timer.rs | 159 | `ab7bfc9e02e33d3b86168f606ced6332ea33d39b5503fae655b11cae2a52dfd9` | 0 |
| src/rust/bitbox-hal/src/ui.rs | 8042 | `bc9fb5c0d36d1a1e879cd4d02e116998272c37f1e537d48eb6a505d20946f1b7` | 0 |
| src/rust/bitbox-lvgl-sys/Cargo.toml | 248 | `389cb4c1c28f0ccc4a422025b75061db160cc8fdbfb68b51f77fd00e1bba91be` | 0 |
| src/rust/bitbox-lvgl-sys/build.rs | 9866 | `d28e575ad9baa893bce904d3b2b74b2db3fb600a1b4ee36f6a911c7040bf7366` | 0 |
| src/rust/bitbox-lvgl-sys/lv_conf.h | 51220 | `5a13d194e9d7013099caf89cea5091b78ff16a22b9c9ea928f7276c1f35bf7d1` | 0 |
| src/rust/bitbox-lvgl-sys/src/lib.rs | 341 | `fcab8b13940551094a4a7a4fe477bc6186711f50e0dfa2026dfab7013858f313` | 0 |
| src/rust/bitbox-lvgl-sys/wrapper.h | 338 | `acd8d58b7615012977b0147392b8c616a71205c3b2cbc66b9953a5d0bfbe1f09` | 0 |
| src/rust/bitbox-lvgl/Cargo.toml | 268 | `daefc6d741706e60098419b9ec4d5b2ceb5a3de23878b9bc7206085aaa9cf3bb` | 0 |
| src/rust/bitbox-lvgl/src/color.rs | 473 | `71d7bea77d1589672a954ef696f73db64bb36192eae7d0f37898c13d04bfe829` | 0 |
| src/rust/bitbox-lvgl/src/display.rs | 5374 | `916b3d2e5a95aea091b5f9368115cc017ce770ed6c7f2e1fd2f001651822469e` | 0 |
| src/rust/bitbox-lvgl/src/font.rs | 1900 | `5f87b8d677c62d374ffe1c4d4c557abcec777306bcf8e8c877840fe449ea9d8c` | 0 |
| src/rust/bitbox-lvgl/src/indev.rs | 2037 | `bbf58a031fdbf5b41ef0f9b6616b54a24891ed27481c92a9b41d6d59f24bccfd` | 0 |
| src/rust/bitbox-lvgl/src/lib.rs | 3486 | `7b69d1adbd4abb46f93f8ab9312bf857383eb1f18acf73e3116216070dbfa9de` | 0 |
| src/rust/bitbox-lvgl/src/log.rs | 985 | `fe230bbebb5892fa4ea4fa3d6f3fe7b0034bf21fd318a2265db03267b814dc7d` | 0 |
| src/rust/bitbox-lvgl/src/style.rs | 3816 | `6db64a1617b4f2647ec3d2c6de756f7a027b773a27bd7d92f2778779ce8b30b4` | 0 |
| src/rust/bitbox-lvgl/src/system.rs | 105 | `ffd20d867f7d4328e68d59f135e9134ca691dd5851cd271a609b6c96b6e02036` | 0 |
| src/rust/bitbox-lvgl/src/tick.rs | 157 | `ad20354b120701fbd19ef4be25425cdc219eeb71e5951ea0c0ab28de87a8ee89` | 0 |
| src/rust/bitbox-lvgl/src/timer.rs | 130 | `3eabc6b60fd7223fbef597a37088779ffda143d1bc6985f3918f280ce5c78e3b` | 0 |
| src/rust/bitbox-lvgl/src/util.rs | 1312 | `f3f9f97063188336dd790b1aba5c0b085020096af6a57711c0401ae575eae491` | 0 |
| src/rust/bitbox-lvgl/src/widgets/arc.rs | 3409 | `0a116c3cc38d71e7fb015b929fe518a3dcbd44e7bf0d046390c0fb67f7fc2238` | 0 |
| src/rust/bitbox-lvgl/src/widgets/bar.rs | 2207 | `1684518d5e6da6338ef0df80538b98941221ecb55002d737b76a4eb2e1532a07` | 0 |
| src/rust/bitbox-lvgl/src/widgets/button.rs | 521 | `3f8a2ac68192d05fc1539694ab44e2f6f8b28c6fc72bb1d2b757474ddde8083c` | 0 |
| src/rust/bitbox-lvgl/src/widgets/buttonmatrix.rs | 6488 | `5024d703f760384f238652d387ded9200aa1baebce14e48d5c0848e441538121` | 0 |
| src/rust/bitbox-lvgl/src/widgets/canvas.rs | 4115 | `a5b70aa02b2edb1924c0945b781853a9172f0ba1f18a66dc830d2eb838896c62` | 0 |
| src/rust/bitbox-lvgl/src/widgets/class.rs | 2361 | `efa9537454a60a2d4db805c8139483aee33a8fd71e7a1a9d3dc59d035a8310f8` | 0 |
| src/rust/bitbox-lvgl/src/widgets/image.rs | 3280 | `fd27b5b532c89fea4ad00cd82e0aad8551b4b8720565d3e09a0a32047a640faa` | 0 |
| src/rust/bitbox-lvgl/src/widgets/keyboard.rs | 4508 | `267840305dfce7dd03cee5bbd73c66b2c0acf6484fbd6937ab9719baaf7e5ea7` | 0 |
| src/rust/bitbox-lvgl/src/widgets/label.rs | 3497 | `9c01936e4c2ffea788935298186fa3165630ec5d5d7993cb1aad1ef9a3220cd6` | 0 |
| src/rust/bitbox-lvgl/src/widgets/line.rs | 2822 | `65f099ad38111fdbd0092cea34299168ef3886c47f10a94569fd887db9a28f84` | 0 |
| src/rust/bitbox-lvgl/src/widgets/mod.rs | 2567 | `4a1f2a556ae514d9a87b742134f675d8f8fa041a1a832699c434a5419425e335` | 0 |
| src/rust/bitbox-lvgl/src/widgets/obj.rs | 26478 | `986a3fb1a9bd5628a7428f9feb7f6d9c2b0aa2436ac7e25ca5fbba866f0ba007` | 0 |
| src/rust/bitbox-lvgl/src/widgets/slider.rs | 2700 | `7ff614b820dbb41728c77822445f8d9acabf0eb2405fdbc54c13ca5a10bfcf2c` | 0 |
| src/rust/bitbox-lvgl/src/widgets/span.rs | 18294 | `d53070663d6ebff5243cbffc2a73460492fd4d5e6465a7a09947974fbe263f6e` | 0 |
| src/rust/bitbox-lvgl/src/widgets/spinner.rs | 774 | `c3f69a2baf9c498ba1574b2133fb1a10fc3f66e01ca0efe6735f214d7f70b896` | 0 |
| src/rust/bitbox-lvgl/src/widgets/textarea.rs | 6641 | `c0a550e929d8ef527d767c582394858c4d0a3a9eeb1b3182a4298ab68ebc2658` | 0 |
| src/rust/bitbox-lvgl/src/widgets/util.rs | 3599 | `64c737a005a0aba480725702fe5539a2fbfd92ad419678a82bfd03ef3219e715` | 0 |
| src/rust/bitbox-mcu-stm32u5/Cargo.toml | 356 | `4980c20d6863a9faddd52520b0ea0f39205f5ea2baa2441d203e6b6cb38c08e4` | 0 |
| src/rust/bitbox-mcu-stm32u5/src/lib.rs | 87 | `33f59b81e49b867519f3e09635f27a1a46f6bc4acd9d0f4aacbbc0adaca3d127` | 0 |
| src/rust/bitbox-noise/Cargo.toml | 620 | `1903f4c84f747fe0de9b1af349aa437b9ca54624f36075226df2314080c4e751` | 0 |
| src/rust/bitbox-noise/src/lib.rs | 556 | `6787c6b484f801c7d4e95443f0512b7247bff8dba8f871c54b92f21685e2d930` | 0 |
| src/rust/bitbox-noise/src/noise_xx.rs | 10043 | `4ade64136c560f523c56ae0e567721938ae097ab6a192c547f5891d45764c599` | 0 |
| src/rust/bitbox-noise/src/x25519.rs | 2023 | `63617ea3d8acc0f018c1664ce5abae381d71c29cec4b9f994bd042e92d982315` | 0 |
| src/rust/bitbox-platform-host/Cargo.toml | 534 | `e13d76508db7d5e832dbcea9d159fd868d9705976d3f96491af589acac2cc51d` | 0 |
| src/rust/bitbox-platform-host/src/eeprom.rs | 1808 | `e90f8286ddc5068a56e3b59f033f32e0292148117c35f826df0ee2fd36e3c259` | 0 |
| src/rust/bitbox-platform-host/src/lib.rs | 199 | `aa279b040b8a9357dd020dba45c6996af8780a46caa027bd1adb80c7dbfb116f` | 0 |
| src/rust/bitbox-platform-host/src/memory.rs | 12192 | `702d8734b4db0d0a259d6bc831b273411179bf57fdad065bd47c6cd677d60ed4` | 0 |
| src/rust/bitbox-platform-host/src/random.rs | 2083 | `fde390232194f51b1530025eec812bda2d16781b2ff11b7fa72b68d5a472a393` | 0 |
| src/rust/bitbox-platform-host/src/sd.rs | 3060 | `3f40d002d85cd970f8c70473f32197c54313c5766203d5fce33f2a5371c82b3b` | 0 |
| src/rust/bitbox-platform-host/src/securechip.rs | 7297 | `a383fe084917e785e7794e8950397b3fb5d39628ea0a926efdcb1bf9746c0bad` | 0 |
| src/rust/bitbox-platform-host/src/timer.rs | 1617 | `0e643681b0e7089742a91cb2621e39fa2123f634f50e908f6140751f8fa44f5e` | 0 |
| src/rust/bitbox-platform-stm32u5-sys/Cargo.toml | 345 | `f00953d4fdd7b0a339a4275ba3a016813153790f1440bda76edffc6bb65a7700` | 0 |
| src/rust/bitbox-platform-stm32u5-sys/build.rs | 4624 | `e5a03d01598e2c749dc94ca18a3d1c069e1726108c863a167648be5c5f450f98` | 0 |
| src/rust/bitbox-platform-stm32u5-sys/src/lib.rs | 1804 | `7779a494a7b1f81a99cfe6da8e827ffaafa632b1e15d543bc8b55ba93aa53ace` | 0 |
| src/rust/bitbox-platform-stm32u5-sys/wrapper.h | 67 | `7bdf790812e8172badd61a9db85127dff2425a4654ecad202c1840d37e733db4` | 0 |
| src/rust/bitbox-platform-stm32u5/Cargo.toml | 718 | `5501510cdaf7eb902f231f719b19f3fec7a542b4dc3160310cacc4a5e129d3cf` | 0 |
| src/rust/bitbox-platform-stm32u5/build.rs | 597 | `ab8ee6746d73105d4ea8cdb73205d7b3422b288c16cd5922c2ea5ca146b0697d` | 0 |
| src/rust/bitbox-platform-stm32u5/src/flash.rs | 3007 | `a128bfb727a5d77c521eadc35601cc385be833f8d0ce7089aa9bbdddd4a59bdb` | 0 |
| src/rust/bitbox-platform-stm32u5/src/inner.rs | 2010 | `f3c9459d7051aab14209a7e53d6995a9c9c2aa500ff9b1c910f522f74b57def9` | 0 |
| src/rust/bitbox-platform-stm32u5/src/lib.rs | 185 | `2ee9aac744280d9c128b6d74eab47a33a60e8f4524aaf75cf6ae1a8c1a0041b9` | 0 |
| src/rust/bitbox-proto/Cargo.toml | 529 | `21decdfa25e99c6645d4bfa993c898bdace001c059e9f7fa7b0023e22a0768ec` | 0 |
| src/rust/bitbox-proto/build.rs | 808 | `6d4f6136eadec490c81d39aae758968650da4c2442022749a034d968f027d141` | 0 |
| src/rust/bitbox-proto/src/generated/shiftcrypto.bitbox02.backups.rs | 3421 | `45f3b31bcbddbb90b7b8b29ebb0fa4cde683b573ea309bfa41e9c08f4a7122af` | 0 |
| src/rust/bitbox-proto/src/generated/shiftcrypto.bitbox02.rs | 86465 | `5b538703f43ef6f30896a79c051a3e37caf7b6c365b5493db6d535adba0c6fad` | 0 |
| src/rust/bitbox-proto/src/lib.rs | 1372 | `1d36872343cc062e807a7315fead89a405251f59fb66be5980de93594fdbf647` | 0 |
| src/rust/bitbox-secp256k1/Cargo.toml | 484 | `77442775d85b6ad99b047180d03c077b5427273e767a06175c5befb7ffb275a6` | 0 |
| src/rust/bitbox-secp256k1/build.rs | 1565 | `91983851f534bb1e29d57360162a303f9847ba6378c5873aa4088c655c748f7e` | 0 |
| src/rust/bitbox-secp256k1/src/default_callbacks.c | 297 | `da45e3b9ba84a8289455a354a0e12d934ac515a09c0c0080afd1561c08ba0074` | 0 |
| src/rust/bitbox-secp256k1/src/lib.rs | 15733 | `42fc499883f91dea548d9ff0b11ad9770a60a560c74271563e66e7e573d77e28` | 5 |
| src/rust/bitbox-securechip-sys/Cargo.toml | 259 | `c8ecf19222651c1788eb0599179b20ee850fff55cc34e3ab9c36952289951d71` | 0 |
| src/rust/bitbox-securechip-sys/build.rs | 7537 | `3c435995bb9a2ac536ea75f6bc5d2857a14214b43e24d496e5413b4cce091855` | 0 |
| src/rust/bitbox-securechip-sys/src/lib.rs | 311 | `1531ac58123bde8556099e327af91ec8e5db645bd971854fa6876e7a8d100ffa` | 0 |
| src/rust/bitbox-securechip-sys/wrapper.h | 123 | `c2f4dac6ec8ac622887b6938beb8ea123b16d32fc64c151256fc5bef9159917b` | 0 |
| src/rust/bitbox-securechip/Cargo.toml | 862 | `6f3d69d24c02306d7c1b1ebb8d0e6f53e386217cc4132f786bdf4c14b259c373` | 0 |
| src/rust/bitbox-securechip/src/atecc.rs | 3668 | `a8cbd36ebbda21ff5f525a3842e75e94fc76bf377aba97ee8c924a87e0c7f7e5` | 0 |
| src/rust/bitbox-securechip/src/lib.rs | 3301 | `9d71da45b4b72c61b0f0648a6e2756ade7604486ecb0f2d331ca1896c6e3764e` | 0 |
| src/rust/bitbox-securechip/src/optiga.rs | 37182 | `dd80d44ba7dd070e3c0c1c2ef42c318cfabf7e96eaaa9817aae6e4ff1beea024` | 0 |
| src/rust/bitbox-securechip/src/optiga/der.rs | 1945 | `51c9a5b5999f696830104a30fc38669b68985cc1fa15ebe1a2c8717fcc4bd124` | 0 |
| src/rust/bitbox-securechip/src/optiga/ops.rs | 20626 | `28f6ef019296d7087c62a4ade4089952ed70e8b5f4f1151b1f2061c495442071` | 0 |
| src/rust/bitbox-securechip/src/optiga/ops_fake.rs | 15685 | `de3f330803a923572ae8e073ae4af8a057a0391c32a6499d62bd4c962eef60b2` | 0 |
| src/rust/bitbox-u2fhid/Cargo.toml | 212 | `3e941a6766699c0e11a57e5a81779d4563e0ef4cf9b71bdc56a4be0bfbaea031` | 0 |
| src/rust/bitbox-u2fhid/src/lib.rs | 23418 | `7b70b84d5579fba6237c5a176e5479c5b94502f655d63e81e047400350dc8b07` | 0 |
| src/rust/bitbox-usb-report-queue/Cargo.toml | 291 | `053b288e4a5823e95b6362dfd133f63f2bd87634db7343b95c931ac75007b710` | 0 |
| src/rust/bitbox-usb-report-queue/src/lib.rs | 10931 | `5a161e6b53648bda9c93dc66bbe58e5f1de2019925404073a2ebecaf474f807f` | 0 |
| src/rust/bitbox02-rust-c/Cargo.toml | 3932 | `2c730e8b213a5d8e3a381d0a5e4c2745e0ba2a12344883db570fd8d70ddd061c` | 0 |
| src/rust/bitbox02-rust-c/src/async_usb.rs | 2063 | `47a9499822950a6254d095bc1561302952fe6335fa5563cc400b79426b97978a` | 0 |
| src/rust/bitbox02-rust-c/src/c_alloc.rs | 905 | `471866858b22495db4c369feba9db9b5af816cb01d5e4c87f0f882573f1fa697` | 0 |
| src/rust/bitbox02-rust-c/src/communication_mode.rs | 378 | `c8d296555831770fa32351f31bad19787ed3693d366c9f42f2e4c9d9515e971f` | 0 |
| src/rust/bitbox02-rust-c/src/firmware_c_api.rs | 5436 | `029d99f0ae93aafe5fa6331d4ed1787be0189241340a75018052958599fa4358` | 0 |
| src/rust/bitbox02-rust-c/src/lib.rs | 5125 | `c872df632ac63a1f4735660e6ac132b661f80f0939a38c07914203d6a3ac31f8` | 0 |
| src/rust/bitbox02-rust-c/src/secp256k1.rs | 6624 | `54c1ff4e1f9ed19a0c92a26d1f83cc8a2fea72509e0394ce4ed01973e0f2c3c6` | 0 |
| src/rust/bitbox02-rust-c/src/u2f_c_api.rs | 9830 | `f9dd4d7daa5fcf8b4361292668bfaf314c9e817e2a6d8bdeb8f22e9d476ba5e9` | 0 |
| src/rust/bitbox02-rust-c/src/u2f_c_api_stubs.rs | 781 | `e7f0952fdbfff2c7a2f00c76c01ad871c4ce0bcc8d783a445321b1f27840ef5a` | 0 |
| src/rust/bitbox02-rust/Cargo.toml | 4607 | `70708f2472b1cc14d6973c14214edd75afdc82ef08293b74fa3212b721ec253a` | 0 |
| src/rust/bitbox02-rust/build.rs | 2374 | `0fdd53625ca0ef342a07b6511534ccc0413dfb7ae06c455dbc58e14661a39798` | 0 |
| src/rust/bitbox02-rust/src/async_usb.rs | 16034 | `f24da5058d7c408f62069012f5f2463b1c76a5421a3d4e370c556121859da605` | 0 |
| src/rust/bitbox02-rust/src/attestation.rs | 2902 | `c20b01cb077b8baaa32a6ee878c0fd3038266ad5659829bdfbb1ec9bfcb19404` | 0 |
| src/rust/bitbox02-rust/src/backup.rs | 21345 | `4efaf420eec850fec73301ebd5a101c28acd12a1fbcad82d7a2cd32321a34fa4` | 0 |
| src/rust/bitbox02-rust/src/bip32.rs | 13090 | `69904362ecbb2911101474f83924b9dd5cbd17e7ea748a733573e9d09d02d7ea` | 0 |
| src/rust/bitbox02-rust/src/bip39.rs | 10472 | `3066de8005955ca3128da1bab484d55ba24d368a5ea113d36f1d89123ffe47a5` | 0 |
| src/rust/bitbox02-rust/src/communication_mode.rs | 1970 | `f0301d116abedb634542e247de509b5893e48290c851a420a948cf3db219fff8` | 0 |
| src/rust/bitbox02-rust/src/general.rs | 367 | `51fc5e6dda75ecf8de8e25c673afc1bb44214079f9fc848b5f1b733e7191dc09` | 0 |
| src/rust/bitbox02-rust/src/hal.rs | 120 | `18d3943a548c4b5d51e366ea87f01d61e419958ea8f91002d931ea04c1da10cd` | 0 |
| src/rust/bitbox02-rust/src/hash.rs | 1517 | `4b667a9836bade2671d5c320ba17c8644e245b613d4e6cee8d5f155697952ade` | 0 |
| src/rust/bitbox02-rust/src/hww.rs | 28291 | `2927bcad9778746803fd0da2c14bf7959bea20c137c5fd572a5e3968e3614cb8` | 0 |
| src/rust/bitbox02-rust/src/hww/api.rs | 8874 | `4e88939f98f0466f8f635eac082d397f58abb032590ea8f0a29afe55741f1f7c` | 0 |
| src/rust/bitbox02-rust/src/hww/api/backup.rs | 14916 | `5374eff995386d703bcf4520b299484ee5673049bcb93f968f49c5374c0f0657` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bip85.rs | 4647 | `ca089a3a18442b292edfe900b31b8c59f600cdaa5e9cfb287c4683474a39834d` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitboxsync.rs | 41098 | `e15d530066a769341285a06cd933c9a5bb5fbffee95c9d6abc10ed581713428d` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin.rs | 53465 | `181410dc293fae8eb397eeb72e4b0ac6094efb5740c9d8de249b12b8253e69cc` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/bip143.rs | 3095 | `1f374135c58bae745e88d9500fc29164ac723d522752bf67fbce069a45730684` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/bip341.rs | 5494 | `7217fe9028053addc3c36337b2a43958d7e56a3a4d8a92c1e630dba3301fadfc` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/common.rs | 26882 | `b8a6f3c01008c0631fb04cbc9b8f389c6cf30de321502f994110143f0a7eab56` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/keypath.rs | 18724 | `d5d08ddb0cf20c3ca0497a723a08d748f863118b90d170ddf1a0d308a7d39801` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/multisig.rs | 42734 | `cff6a02dc53347895b0f6c7562c316eb354eba5a81ecaf8cf111da6f00e8a88f` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/params.rs | 2291 | `fae19e0b1a338960fb97055efcd6bd6c1d1572962faf960644cdf239592341ff` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/policies.rs | 82001 | `abc68ccee396717d58844920139f2d29bb75a4fabc74f976897470f0232d4b91` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/registration.rs | 12363 | `338b00774cb29f0dbfe5a480dc6c944f70fa72d112e976fd4e9bb873ad1deda3` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/script_configs.rs | 5506 | `17594a528cf37f0398f0deb18b16e996060fb670dae8520de29c243379c7c170` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/signmsg.rs | 25339 | `7f2d957f821c1930f16dc8c1de5982ece4f50b3468307cdbc8925ff34b21a979` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/signtx.rs | 138278 | `195b930b906cd84cefc9bb4ceecae73268d702b22b019f80b18992d56c6a45d3` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bitcoin/xpubs.rs | 6970 | `4bc855177239b7b5cf15dd545a461bc421f39555d8f7fb3a65b672af96848836` | 0 |
| src/rust/bitbox02-rust/src/hww/api/bluetooth.rs | 14999 | `54fc1a9ca2d9412a3708551436f0d0b2b4c93ff2aaae3f51deee8c3a77c4e539` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano.rs | 782 | `fb2b77c02fecf5d5b0927aff56ec1ee7c4d90fdbaf3e112043b66f58508891e6` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/address.rs | 25289 | `2edeeab72109e5d9c5244ae16cf22b7397aa658364c5f27466538b16deb366ab` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/keypath.rs | 9489 | `669a3af625f388c46d5718aeb4cd88476c16a2629e3d12134b811f0068882350` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/params.rs | 1354 | `d7afb92488f4c471889b2d5db2526630a474377dcbd903d85659d12d671ace3e` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/sign_transaction.rs | 74982 | `5e94e09ed5e9e28ba9935be3120f5926f5ebcf6c4a275e79c2a25c2cc0564ad9` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/sign_transaction/cbor.rs | 11409 | `89e1d37d2bfb99b67ab18817241be589831874e5f56a5f0075f3a6bbf0bf70ec` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/sign_transaction/certificates.rs | 5772 | `039d3fb80dec40bf724d7daaf3dd4ab7c9d3f1d35b159a04503ead5a3564c8d4` | 0 |
| src/rust/bitbox02-rust/src/hww/api/cardano/xpubs.rs | 5566 | `ca845c4de879d93b868925ace61c0471acf3041011d8bb63f916239064c2055a` | 0 |
| src/rust/bitbox02-rust/src/hww/api/change_password.rs | 8093 | `df7e6672fc66ba2ce24c092ff0b58224b7181bf87fd978f501eea082a2aba4ab` | 6 |
| src/rust/bitbox02-rust/src/hww/api/device_info.rs | 3187 | `cf7700970753c5467429c85b88e4f21dd87f88aed83c0e879cfc899700c270f8` | 0 |
| src/rust/bitbox02-rust/src/hww/api/electrum.rs | 3010 | `9cf68840f7aed0f19a71e0ed7771e423a77cf662ae54ffc196e88999215249a7` | 0 |
| src/rust/bitbox02-rust/src/hww/api/error.rs | 4335 | `b6a13ec95227e726cf487267d3a0ed53bc9cab5b1d3860d497dee0ec97cd59c1` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum.rs | 5189 | `873ca1378407cae796dfac9032da1bc6e980612f5f2846592ff2d493384071bb` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/address.rs | 6735 | `57664aa3edfb4b15fc9341ccf65cc9c7da221fd0a59b988b4a4b2bbd05d42d37` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/amount.rs | 4447 | `78effd3b340e7034d0c5bb3332151d9fca0b944c312f2235be007a3bb7d0fb74` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/keypath.rs | 5510 | `e7129e999976e13aaed04d41604ae3e7d65b5d3e8c6da7d5ece9063554523369` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/params.rs | 6318 | `6d45acd07d99ea9e40064d668797b13f5b24947beca278a8ec67ec96a63c68ad` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/pubrequest.rs | 11492 | `1fb38f29c8acc366e5e28ee31505eda46b33d29abca6006453cfb3aeb5fb3614` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/sighash.rs | 27142 | `cccb0d7501d1db215c00bbc9586b3d873625b63606d2a072319eb5b1f7408e8e` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/sign.rs | 96116 | `1891a4b2d603dcb45aedd9b2fc409ddaf9d27a813264145b7b9b3cbda7001b46` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/sign_typed_msg.rs | 117444 | `890c26321761c405f6ec0b238a67ecfa3aa3ad9d2c594f2bcbb85487e57020de` | 0 |
| src/rust/bitbox02-rust/src/hww/api/ethereum/signmsg.rs | 10476 | `b4de40b5a63033ec24e52f0077c80a3a73a9471fdc6d10d5289322356cd626cc` | 0 |
| src/rust/bitbox02-rust/src/hww/api/payment_request.rs | 67439 | `c76bd2db8e0205ee3cf3e26cb00132da08975241342a6f88939966e2c4a24684` | 0 |
| src/rust/bitbox02-rust/src/hww/api/reset.rs | 2174 | `44fa3b048c424a65d24d853cd2fe6aaa805c37b6f23b2c7bc0bca915c98145d0` | 0 |
| src/rust/bitbox02-rust/src/hww/api/restore.rs | 9331 | `3afe08e63f02f6e0e547bced73824bb37800e52551da477c4cc95f1f2925f307` | 0 |
| src/rust/bitbox02-rust/src/hww/api/rootfingerprint.rs | 1540 | `bec5a60dbc30d5c9fbc4b387d121c35cc82420262422c85693f79b65d6c07626` | 0 |
| src/rust/bitbox02-rust/src/hww/api/sdcard.rs | 2540 | `9ac1af0cd1531ed86ab3dee9b9ca1711573ef131617453faec1a161a3245afc1` | 0 |
| src/rust/bitbox02-rust/src/hww/api/set_device_name.rs | 4581 | `b336413a7ca7043f89df8cfeb781e7c602739c44b6d17fd21811dde8b6e3f0f4` | 0 |
| src/rust/bitbox02-rust/src/hww/api/set_mnemonic_passphrase_enabled.rs | 2612 | `c1361dc350dcc62f74137349a37b5190afa02dfae0952e622569b8636f8b8e60` | 0 |
| src/rust/bitbox02-rust/src/hww/api/set_password.rs | 4915 | `34eb42602dc38d169e1994f8e360c960562739af09700e633fa6057dc09b4a05` | 0 |
| src/rust/bitbox02-rust/src/hww/api/show_mnemonic.rs | 7482 | `a5180d83d601f5774114f1cba451a2783358e952e52cbbc421a1de46c81f4f13` | 0 |
| src/rust/bitbox02-rust/src/hww/api/system.rs | 1785 | `a0527f375722906e809a1410e5cbbd8404ec3d19bbd8d4d278e675a8b69e2531` | 0 |
| src/rust/bitbox02-rust/src/hww/api/unlock.rs | 6665 | `29ec66437733d134968bb4e5b366d71cf0e47aeacbcaa8e5d157ad2fc90c889b` | 0 |
| src/rust/bitbox02-rust/src/hww/noise.rs | 5095 | `84f8975fbe603db802539bd6b6973505ce5938787617d4f53fa3923056d50024` | 0 |
| src/rust/bitbox02-rust/src/hww/transport.rs | 16808 | `371927da8fdefc6f47d8a5cdb7518242446f2340efdcca17ca0b90a5ee023dab` | 0 |
| src/rust/bitbox02-rust/src/keystore.rs | 83987 | `b7918fdd4b52ef1b088e28bf88f3442f8243d706fdf1db79c60e71fb8817420b` | 2 |
| src/rust/bitbox02-rust/src/keystore/ed25519.rs | 10193 | `85cb066d8f6e599c0f1eeafe7aa139d6c51c0bb678c4d0308173de566c61304d` | 0 |
| src/rust/bitbox02-rust/src/lib.rs | 869 | `54ccda57e672294cdd51137f4e529824830c58457644c67d8b6d2952442471b5` | 0 |
| src/rust/bitbox02-rust/src/main_loop.rs | 6571 | `8f8dc3d87d7a372ba046e88c3e844c1ca14b8ff5340d715af412297fe820f381` | 0 |
| src/rust/bitbox02-rust/src/reset.rs | 4440 | `fc08d0007d657de5b8f162034006b1eefd42822948c09ad247aacb2bd28ce528` | 0 |
| src/rust/bitbox02-rust/src/secp256k1.rs | 287 | `4da9a5cfc6fee6086c57c29d11367c6473c6f2bc7e7ec31c593ef67a6464883f` | 0 |
| src/rust/bitbox02-rust/src/u2f.rs | 6712 | `3d6bffb5411151496b3962d2f9c5ee559fc86e060f86791f8b2ca1b40439e5e9` | 0 |
| src/rust/bitbox02-rust/src/version.rs | 166 | `49bbc061dde4aa1a081e6e79d3e0a65ef4067cadfeb636c0b02a4aa6f311a33b` | 0 |
| src/rust/bitbox02-rust/src/workflow.rs | 296 | `885ca432cb372563ae134d554254bdbd8b914a880c12c5e15517df1b8fb668e0` | 0 |
| src/rust/bitbox02-rust/src/workflow/confirm.rs | 1449 | `84c4285756710f56d7ccabd75246644e49ae186c2d1d3aae6a4579911550bc02` | 0 |
| src/rust/bitbox02-rust/src/workflow/mnemonic.rs | 34778 | `2257e6aceeca61f3939defe9bb98fa092f5ce6bcd4a424b84aa298af40037831` | 0 |
| src/rust/bitbox02-rust/src/workflow/pairing.rs | 1690 | `345b1b3d5c9873b12eff6f03f40d279bdd27dd077daeddab88199d49874315b7` | 0 |
| src/rust/bitbox02-rust/src/workflow/password.rs | 6278 | `f0a995ecf8584cd5c58cb37f20686d39e9654c5cfa35289d267b3ff939c3b019` | 0 |
| src/rust/bitbox02-rust/src/workflow/transaction.rs | 3554 | `6451402352fb8ff628bba81fabd478aec289f32385735b8b68a1372b6fc02c05` | 0 |
| src/rust/bitbox02-rust/src/workflow/unlock.rs | 17747 | `065962fe57d9cb6640869677d8f5489bc0fc188a060f746dd83b562f80805fa9` | 0 |
| src/rust/bitbox02-rust/src/workflow/verify_message.rs | 13559 | `4a2c0f3cea125caeae7d0371c7629ae08b03f3cb6d76f183cd6d11385e6fe846` | 0 |
| src/rust/bitbox02-rust/src/xpubcache.rs | 11790 | `fcc3f7f8340292a2d682a108772c490f6d41827c31f331a0edd32f4d7fddfc8d` | 0 |
| src/rust/bitbox02-sys/Cargo.toml | 390 | `4492ef51f8a188413a4ee87a0dc30f58c2cd5a28f890a631480558672e3faaeb` | 0 |
| src/rust/bitbox02-sys/build.rs | 21680 | `6370b2397f94e9e9531ae43ecb9dfba9e819e1d7f0dae4c23a3e89d8658a3a07` | 0 |
| src/rust/bitbox02-sys/src/lib.rs | 892 | `8ed5a6852000ff1e71639e70b0d8243624213c16d85a0f7b64aff02ab41a6e9e` | 0 |
| src/rust/bitbox02-sys/wrapper.h | 2101 | `ce7ee138f934a422cd5a49f23498dab908a330bbc1ebba755c99bb1832c385b9` | 0 |
| src/rust/bitbox02/Cargo.toml | 1669 | `b70d719688aa910b578befca33864e88ee5c4011f2c03e68cb22e3ff612bf4df` | 0 |
| src/rust/bitbox02/src/da14531_handler.rs | 584 | `a4ef27ce8aa7d67aed9ec004d45235b0ebbb9cf9f6cc3f27b4f2963edf179343` | 0 |
| src/rust/bitbox02/src/da14531_protocol.rs | 880 | `63a96c8132ae1e3c14081bd8cef8b1f4617c4ea1ef586091cd8dd70c0205d72b` | 0 |
| src/rust/bitbox02/src/event.rs | 248 | `bf922d48b6110e575cf44bc25bbdafe56949fd54ef922730cf2b028d092735db` | 0 |
| src/rust/bitbox02/src/hal.rs | 2058 | `d6915485b75c894ba22b5a62c8b90d521f53157ce6c2d217d4bead82eccce5a8` | 0 |
| src/rust/bitbox02/src/hal/eeprom.rs | 942 | `8154b22c49dfc6aba4a2c3b9940a0691738d899e4fe1f086c35a992e9a6f6a14` | 0 |
| src/rust/bitbox02/src/hal/memory.rs | 13523 | `473863fe6af3fb418ab72f97c99e8312d305a39517412a675e08e8175b793259` | 0 |
| src/rust/bitbox02/src/hal/random.rs | 783 | `2e1db38e7270a448d0ec60d8edfaec3156bdca102d6c3daa149748289fa5c22d` | 0 |
| src/rust/bitbox02/src/hal/sd.rs | 1306 | `7ab3174a13fd91733d38d08b24bd2ccafbcf1243dfecaa37d93527ad095b77aa` | 0 |
| src/rust/bitbox02/src/hal/securechip.rs | 11172 | `1cd7cce092509b4025fea0317afe9aa7ef2e59bcf9958b3c20d0de3d51bf0a94` | 0 |
| src/rust/bitbox02/src/hal/system.rs | 1477 | `6b1b1d5546d581e3ffc1fe9d7da92e52d312e0078cdee9db506dcd2ed04ce170` | 0 |
| src/rust/bitbox02/src/hal/timer.rs | 2636 | `85c0bed052cc43976f4c401ffdf5d83bfe1d7d15b2b84a6c2aa0d80984b3b5dc` | 0 |
| src/rust/bitbox02/src/hal/ui.rs | 14681 | `8e7d3ad2359f392ae852b68da7d6723f831adabedaf5883e9d00fa8012d81a96` | 0 |
| src/rust/bitbox02/src/hid_hww.rs | 321 | `724870b9fac503e4e30a9dcfa7f3bc066419776ff26fdc2ca94f88fb72aa312c` | 0 |
| src/rust/bitbox02/src/hid_u2f.rs | 321 | `8643cda0f6b2d05d969ce9173354761b2264745d3c4b65277a5e8650389300e1` | 0 |
| src/rust/bitbox02/src/hww.rs | 101 | `d4cbb84bb30eae55a5d2a57c3b4cd3d1581c465305f0a7aa8228c62e6cb09d75` | 0 |
| src/rust/bitbox02/src/lib.rs | 3431 | `b6e93585807f0e85bf91e713932d289f18759f3e9f90871f3e1e2d24030a5c0a` | 0 |
| src/rust/bitbox02/src/memory.rs | 29086 | `d3ad0bad7493c2002c330e45c3fde403fb95d37db43f9cd3f9c7ea68fd9c6548` | 0 |
| src/rust/bitbox02/src/platform.rs | 387 | `d2ecae56b160e9760f16ced2e9a17174b270fe43e0d7b714358bfa17f4f50e0f` | 0 |
| src/rust/bitbox02/src/random.rs | 1425 | `edcc95719949a75adde6a34205951544cd8960c8f8742cf82d7e1a24480aa218` | 0 |
| src/rust/bitbox02/src/screen.rs | 1206 | `6b5d0d4eab685a82c934dea778c963e411c91aabd8a62f943931d734c566eabc` | 0 |
| src/rust/bitbox02/src/screen_saver.rs | 686 | `f08978cd4f9adc7285150e7fc806a61df24fda669027b9137356b44c113e3948` | 0 |
| src/rust/bitbox02/src/sd.rs | 3633 | `332eed271f3a1b655dd3bca4a6e4de60a011e46d9da11fdabfc70e294110065e` | 0 |
| src/rust/bitbox02/src/securechip.rs | 259 | `74f1549267b89c45abeb33faa7b537897aad0c8fc1257ce160dc50e960a24cc5` | 0 |
| src/rust/bitbox02/src/securechip/imp.rs | 6338 | `83020355fa265b9e4e37c87c4f36c5909b62d628162b1982f065c6ed6b54d55c` | 0 |
| src/rust/bitbox02/src/securechip/imp_fake.rs | 3211 | `330cd9da55af9c84a08d8f350e84e2fdc8c1c73ee96ea77c91681efd17c22af7` | 1 |
| src/rust/bitbox02/src/spi_mem.rs | 1334 | `f62ac7882ba064c5e08ef0f6e6d6fd466bfa68adda78f14a34c55f5772cd8049` | 0 |
| src/rust/bitbox02/src/u2f.rs | 198 | `1a80974c4b199c6418d90887e5895b2e89ea249936bfd652315fe8dec147305c` | 0 |
| src/rust/bitbox02/src/u2f_packet.rs | 463 | `1de6b32c0488616e6343e5ceeb4131d1621a35824139984fb1510d09c052def3` | 0 |
| src/rust/bitbox02/src/uart.rs | 822 | `12c23b2e2d988d49d67a3efb9647408309d40fa0e95b1f4054090e6e321d0d15` | 0 |
| src/rust/bitbox02/src/ui.rs | 632 | `29e754c46c1185d2fefa2261446a4d6cdf656ff2f2675233ea373e46fac5d8fa` | 0 |
| src/rust/bitbox02/src/ui/types.rs | 3770 | `09f8ea3ffa8ca24ade9793ffd205a1eda3ac3216bb291daf72fc3a770d29572c` | 0 |
| src/rust/bitbox02/src/ui/ugui.rs | 72 | `c3c17298da8d70199030dfc0c054cd953f08460fb924f74ad9dab7a9dc2860d1` | 0 |
| src/rust/bitbox02/src/ui/ui.rs | 32463 | `df7dbba10ee96a9ded04a6cf9891b49bb239d8374911e637073d315b1fdbe02b` | 0 |
| src/rust/bitbox02/src/ui/ui_stub.rs | 2885 | `44a7c3b57ab698f176f1a6dd661d2b4fdd8e44481e70f3b52da95b50e2b8b820` | 0 |
| src/rust/bitbox02/src/usb.rs | 153 | `965aefb4815cdccdf10f5a2898efd9506e6fff5de3ca33e5ce9234acfd353544` | 0 |
| src/rust/bitbox02/src/usb_packet.rs | 912 | `b54e3d1f804137366c10d343e0b69b0433384ec1ff156e15d108ff61c0362eba` | 0 |
| src/rust/bitbox02/src/usb_processing.rs | 1240 | `60de0f4120276030ec4689de0b3e2df8e83779f34627eeee87533081970fbaa5` | 0 |
| src/rust/bitbox03/Cargo.toml | 400 | `6927165100e35a7e5b2e199208a4c7db809060ea479f375649961c1658d8c3c3` | 0 |
| src/rust/bitbox03/src/eeprom.rs | 792 | `ddfb8813943a33930450b01e2bb1616811ee5ba688a51a5cec5f37ed4bc39ede` | 0 |
| src/rust/bitbox03/src/io.rs | 61 | `2953777db481a5a05c64b72d4f3a9ba953aa2f72a9b38c2ffc270b50c2a644f5` | 0 |
| src/rust/bitbox03/src/io/touchscreen.rs | 1866 | `ae775069eb670b7d1f0e62545590e920d12b10a817b7e031a9829b2cf360b471` | 0 |
| src/rust/bitbox03/src/lib.rs | 2578 | `38cd67b71d70f90fee279114ad5d1398c695eaa859950b85d5a022ae358368c5` | 0 |
| src/rust/bitbox03/src/memory.rs | 3894 | `4245c2ea7d8b4506f821543c2b4f92c9c03b7da8c6575f7d6ac344f07b592284` | 0 |
| src/rust/bitbox03/src/random.rs | 259 | `19138960ca09317cf42a71bd818c0171ddd703c0db9c1ff6a0019157bd492420` | 0 |
| src/rust/bitbox03/src/sd.rs | 727 | `6d7d16479a0cdd1f9fbd270ded12f5d8231208e48299c62bf1086112e9da162c` | 0 |
| src/rust/bitbox03/src/securechip.rs | 1946 | `42c32de5b793c2c21ef8cd188192fb821c778cb6b47e5c9d37eccdca3452862c` | 0 |
| src/rust/bitbox03/src/system.rs | 446 | `d748f74fd561901eeec5b1e43bfc50a30d3515b57090f468f786009b394d3613` | 0 |
| src/rust/bitbox03/src/timer.rs | 239 | `71b861386ab450012cb83ff87a1a5799dd4ebfb234b3f7781a65d5872c815409` | 0 |
| src/rust/bitbox03/src/ui.rs | 14682 | `1d353457089c94e7747b248670e64a5203f4407e0aee997d325d5afacf872e34` | 0 |
| src/rust/bitbox03/src/ui/choice.rs | 3868 | `161d493f0600ce9c57d8ecdeafde6066ebb5ecd02e94c0e201c8d69be5852779` | 0 |
| src/rust/bitbox03/src/ui/confirm.rs | 6097 | `38396a0ad70cbc306c39df4293d497916bcffde5674b5918c7f7b81f385625d7` | 0 |
| src/rust/bitbox03/src/ui/demo.rs | 3421 | `1d9858404809ee7f4b0d9bcbba9b76fa7360386db1064c7784a6b9bf45dbb3b6` | 0 |
| src/rust/bitbox03/src/ui/enter_string.rs | 98270 | `3742ca93ba5aeed6c2a0a5d1a1a4d0f0797c8b0ee01e5217072e1c2bd0c4d5a3` | 0 |
| src/rust/bitbox03/src/ui/keyboard.rs | 33770 | `8e3bf28083cf243c0c9f45f7c30675ba0655c488ef01480bf845293f26c4d01c` | 0 |
| src/rust/bitbox03/src/ui/keypad.rs | 5537 | `67c0c3ed07ff6dfbd20609f8f95854356e7bf107bcd00217a3fbfaf30fd5891b` | 0 |
| src/rust/bitbox03/src/ui/menu.rs | 4895 | `cf75ab296292809f1b3c571e2e47024268d50aa889cf81dac52a27f2846460da` | 0 |
| src/rust/bitbox03/src/ui/nav_button.rs | 8533 | `695ae86711d9a7bb9b5e4dbbcb96f988de3200878dae044a86b7cb9c72a15d9a` | 0 |
| src/rust/bitbox03/src/ui/recovery_words.rs | 21855 | `8693f42ae62696f45f923dfadb51c55349385f2ff23484a158fb8741f8ca662a` | 0 |
| src/rust/bitbox03/src/ui/slide_to_confirm.rs | 33146 | `f2cc8a66ddfef7be8e0d521e23104cdfb7eeba3ff1129c99adb135883a97bc57` | 0 |
| src/rust/bitbox03/src/ui/status.rs | 2746 | `28cfc602ea285c799d834462b8013ee85bd14e11a0eb94f6473211d26ddee11a` | 0 |
| src/rust/erc20_params/Cargo.toml | 309 | `9e7f84d4c08350c9fd01151b5e00bc58ae558fb6b612678ffc0b5ad9a81ec76d` | 0 |
| src/rust/erc20_params/build.rs | 5606 | `036ca79ff51cde8f3d84746440840185f617b63d2068367058c566003d0651f7` | 0 |
| src/rust/erc20_params/src/lib.rs | 7510 | `2692c60e866fd7ef4fbc5c3691b101e43f50255e99c3fe8d877fdf3211c24b5e` | 0 |
| src/rust/fatfs-sys/Cargo.toml | 253 | `8e99c5b88d0e76f8c315afb2a1b7cd57da52bcc40e673b717b7d0a13e9dff266` | 0 |
| src/rust/fatfs-sys/build.rs | 590 | `19030cba4386dfedb0e812698684f5b7f225079e2c9e3218fe44886a59b26e63` | 0 |
| src/rust/fatfs-sys/depend/fatfs/documents/res/app1.c | 1135 | `17f99c12e7017ceaf25734165745b5b43b734fdd6fdabf5c8c6a01ec2e778aef` | 0 |
| src/rust/fatfs-sys/depend/fatfs/documents/res/app2.c | 2236 | `11c9bf944aca5e55c7642225e1a59f5998a3dc43a302b6f1c5310e9a4ad1433a` | 0 |
| src/rust/fatfs-sys/depend/fatfs/documents/res/app3.c | 4133 | `e5b1c71593750cda3cb11ca638f75d55e23578515fcebcc7607cb66de4e21bec` | 0 |
| src/rust/fatfs-sys/depend/fatfs/documents/res/app4.c | 10567 | `11ff9994c90bd50a04754f6aae344cd2863b2de142d401ec86f81d9d99232dc9` | 0 |
| src/rust/fatfs-sys/depend/fatfs/documents/res/app5.c | 1411 | `ed551e157dc26a5902e59beba3dabe3052d1cacdb806ccfcefa76a519c9893cc` | 0 |
| src/rust/fatfs-sys/depend/fatfs/documents/res/app6.c | 1974 | `209a05020537c1a63cff1d5a4c48a8510ac05fddce400d2e7f440e721c330b68` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/diskio.c | 5385 | `435567bf00b4607a803339ec31d9402ea12536cbf65bb65ef9301027f7d38836` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/diskio.h | 2733 | `1c2b29f53e061c55d43b2e412c3a61320b2621bac7561a05e275514baa44785a` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/ff.c | 266970 | `58ec7816a45870331b2a9c0eb977db19d1f0d95d7416a1482df07675a402c8a6` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/ff.h | 17365 | `42920ae4d6080bfc2a72d92a9969b5e94eeaff070e5e71d90da9ab6d7d8e158e` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/ffconf.h | 12714 | `6dc2ff2adf09b990a5b91eb253543061bd77ed498f92f4887837b35e8ffa5236` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/ffsystem.c | 6172 | `4ef367d61c6060d2bedeac57985ec293cf29d33faa98d15fbd78c5d63260eac7` | 0 |
| src/rust/fatfs-sys/depend/fatfs/source/ffunicode.c | 1974995 | `3f1632c1f1e64b0b683b0d7e51341b9870728f398604869dd8211f1819509a8e` | 0 |
| src/rust/fatfs-sys/src/lib.rs | 11 | `bdf6c7cf1fc01f69cc1d4e52948d1f246fdd310e6323d5dd1efd23f1daf382ef` | 0 |
| src/rust/rust-toolchain.toml | 178 | `adc23c7a875dbd0c12bae71d2e35f74ef87baf17d0660dd4ec245ea41d14e5ff` | 0 |
| src/rust/streaming-silent-payments/Cargo.toml | 404 | `b7a6dba7cfde137b16a86d3d65157dc965d70835aa6f6ee6cea66dfe2d23b044` | 0 |
| src/rust/streaming-silent-payments/src/hash.rs | 1776 | `ec49885fa0902fafb0b1bbd6ac6e4444aee0a3edb622adbd887f23792b637219` | 0 |
| src/rust/streaming-silent-payments/src/lib.rs | 14461 | `4e33062aad0ad48284857ac80a9b626078474c94ab7901ba3f2c17eedf925488` | 0 |
| src/rust/util/Cargo.toml | 878 | `543d8a138679badb32951a85c9c276ce05fd7ba1ca05952148f1f844e69be7ef` | 0 |
| src/rust/util/src/ascii.rs | 2089 | `fde025eaad4c2af6ae324939a7fdf659c09af403649596354181de113363b640` | 0 |
| src/rust/util/src/bb02_async.rs | 1686 | `6ed61692ba8092d58add3b157ed5eb9cb1fa81dd448f53cf5b56ba7ae025cb21` | 0 |
| src/rust/util/src/bip32.rs | 1412 | `457688519fc8b6a097ccabd27c189b1f6ed218437d8b478e029459d58c781125` | 0 |
| src/rust/util/src/bytes.rs | 7737 | `9e7f5104142dc0fd492bcaf693ebbb2c4bc98a91f19cf3c929b4185f3ce4c5fa` | 0 |
| src/rust/util/src/cell.rs | 1286 | `4fb9bdf81aa82bac48d10dd8ba8b2443e2fd5d523ef6b6275cc09ac5d614b975` | 0 |
| src/rust/util/src/datetime.rs | 3468 | `741a7d3fdce76a0a30d332b29f73f237691783190c06f9c3922b0a532fe0e939` | 0 |
| src/rust/util/src/decimal.rs | 4784 | `01a1b5c401e594edfbbe05a5261deaf57841f8a63c5f762238f07b580db22509` | 0 |
| src/rust/util/src/futures.rs | 60 | `8fdafb7122f20d1b5ce988e860031c57512db4fcc1d0a86d01e53777f5c4b0c1` | 0 |
| src/rust/util/src/futures/completion.rs | 3750 | `339f12b2cffad430257aee544aba322fdcdd803a23b52dc443480e22f0988980` | 0 |
| src/rust/util/src/lib.rs | 2166 | `dbba9c609740021556b8cde831364aa22ae8415addf76f481941ee34c09c2de9` | 0 |
| src/rust/util/src/log.rs | 4249 | `d9b518ed3e5292c284bf90958e551320c39b18c1bf88f79094dedc7ee3698be8` | 0 |
| src/rust/util/src/name.rs | 1558 | `998da04d404cfd53209df659581886544d34ae1a4c314a0c044086f7b837e883` | 0 |
| src/rust/util/src/p256.rs | 3298 | `7662a6309089b842bfba84fb5a187419ef8588678035d9f9766bc456d9ab0185` | 2 |
| src/rust/util/src/sha2.rs | 11704 | `ea2cb924dd5d2189531c80450997fba14624ba4244fc2063ded4b5bf7f4c5648` | 0 |
| src/rust/util/src/strings.rs | 9623 | `bb60b4f1763c9444ff1675b49c130c87ed3394b6ef479589abb168e6ac86b811` | 0 |
| src/screen.c | 3476 | `cfe33ab69a62ae78bf8bd1a52d007ecbe0a2d8799f1917ce5052f259acabaeb5` | 0 |
| src/screen.h | 943 | `35e89291cfb88bbc08bcd4ab8b913e406808ac84fc5a112743ad60eb32775262` | 0 |
| src/sd.c | 10969 | `8dcf171b7d515317a15e17a90a6fb1073bb4175e9eb3561e415aad93c5de6f31` | 0 |
| src/sd.h | 1898 | `c91c4fd60a64f13e33871264bc51668534a51576535f4b39378f24b2f1be79eb` | 0 |
| src/sd_mmc/sd_mmc_ext.c | 698 | `79fb100d033d6068fc812405f98f56ebfdc9536fc350fbc80bec1629e1839fe7` | 0 |
| src/sd_mmc/sd_mmc_ext.h | 206 | `6b4c4b41838ce53d4723c1566344eb30dfa8292e3ff033e33dbc6bed601345d2` | 0 |
| src/sd_mmc/sd_mmc_start.c | 430 | `ffd9c7aa3251780e2374147433d3bad4e01b670ad9b0e6eb0c0c5f59a4fa5659` | 0 |
| src/sd_mmc/sd_mmc_start.h | 51 | `ec31f931047363fac9aee9778d3afc0b523683a9d5b21701c424f062a30a3848` | 0 |
| src/securechip/securechip.h | 2253 | `553fd604572b88af6d037102db994a94ffbf5bab836db0783d439b3d70e6f9be` | 0 |
| src/system.c | 1093 | `b6ff1e7ab0ec14f265f906eaae439977df28d9b9bfe7835aee62a71dfdd792e9` | 0 |
| src/system.h | 262 | `b2188c4cdc59fd46318d22edd41cf2ddfbe25023c3226490c7b2716ca64db2c0` | 0 |
| src/touch/gestures.c | 7780 | `15d289b74f8d1afd120c857425dc1b5614c3aac3bd767564056cad032ee00228` | 0 |
| src/touch/gestures.h | 1036 | `f1431c6bc572c1ff0bb639b596d83bfbda72e30440550db2f7af5b943e45650f` | 0 |
| src/u2f.c | 32289 | `5f6bfa1e7cc4b94edf3c23fcfe699c74c484856841debe934de3f86abef08ce6` | 0 |
| src/u2f.h | 1076 | `85ee65d73887ef958af72a5495e5134c5619b2db53a1817379c7e90ae2af84e7` | 0 |
| src/u2f/u2f_app.c | 2770 | `0cdd0a8722f62744d8f89ef5d303b007836f4fb5ab5c70086639149abf965394` | 0 |
| src/u2f/u2f_app.h | 1429 | `4922af347b06b58cf350f854f0e3d824d34c4d6ebbd5252ec37e7dad3bb3877f` | 0 |
| src/u2f/u2f_packet.c | 5265 | `b255472c0baaf4fa28be35ceaf7f367bfac3c144800080815b0ace821daf9c55` | 0 |
| src/u2f/u2f_packet.h | 1048 | `62fec15e5a9779ba29e3876e6979f65a3e9918c7758a467c3099028b64fb8f0e` | 0 |
| src/uart.c | 3229 | `8a2f1cc8191b42d45b03d0712e73a238b6c1de7bd126d8325cc1b7df7fa123b3` | 0 |
| src/uart.h | 545 | `e43783cf909e54c395b4d4f7b9f8059ec4ee8c99a080ed4acdc9fff84b2c2296` | 0 |
| src/ui/component.h | 1821 | `a07473e0ffc5c839fba5d583fa2a5d543facc81064f087f04b3d79fd2605ccf5` | 0 |
| src/ui/components/button.c | 5022 | `cc451912b4ccd09fed913d03fd0369ad53acaffaf8778e24b9c02889046fbe47` | 0 |
| src/ui/components/button.h | 1399 | `3a1736c1bd6fc90a784a73bf31d7afa16714dbc5c16996049f9aaf1b65d88408` | 0 |
| src/ui/components/confirm.c | 4677 | `ff7fc3bff893ce08e68a27c1a73c3d21a061d03b574d7557dff7ee86e52cd525` | 0 |
| src/ui/components/confirm.h | 1636 | `e8bed0d30352f14a1301317974040fd9a631ffd1193fed5e1e2559a86a91b060` | 0 |
| src/ui/components/confirm_gesture.c | 4737 | `b74d570fd5e75f68404265f705fe36fdfd0b611122732ec21c458df31dd8edb9` | 0 |
| src/ui/components/confirm_gesture.h | 493 | `447f87d9695c6941ad76066593024fd4128ccf286db7ea105b9be27031c09c4c` | 0 |
| src/ui/components/confirm_swap.c | 3118 | `e54acf522bfd2eea84a76be00993c645a92995312eb3b385fa97f68215f76fa8` | 0 |
| src/ui/components/confirm_swap.h | 686 | `7a4a9ffc3cd075256c6135bf9436a36e4b0e492eced8187af5d9af66f17d01ce` | 0 |
| src/ui/components/confirm_transaction.c | 4813 | `810d55e494198ee188e15aa696d2354c6ef6041fa79181d385dc74d96cd37643` | 0 |
| src/ui/components/confirm_transaction.h | 1200 | `61f867ffb8af1557dc717e5b667f5f52ed7d4ce2255ec8f2ed591f6dc5fa0936` | 0 |
| src/ui/components/empty.c | 679 | `cd1c8fc5e607e841c9d92235e2ebcfba6c8cbcd6425cb39060f2d8040ef34ffe` | 0 |
| src/ui/components/empty.h | 225 | `6c17f7e1f19f22a91275f7c6093def976bd7de8c997ac927ffd7fc10a1705656` | 0 |
| src/ui/components/icon_button.c | 5054 | `ecb4e2b2970c787c8db7deed590b4633ffa6f100c7b86bae5d7520e54b481bea` | 0 |
| src/ui/components/icon_button.h | 616 | `4ee6d9866e86b07ca04465d3164b8773d83bedc6752cb856ed25ee1652a2eec5` | 0 |
| src/ui/components/image.c | 2682 | `9000e883ffc7ddc70e34bc49bf145bc31eb3af716ec6ef9b79e42fdbbcca8b38` | 0 |
| src/ui/components/image.h | 753 | `f749e5a75baf96d686d30acccfb1b1c4d739353799d340ced306c8be48dac2e8` | 0 |
| src/ui/components/info_centered.c | 1662 | `be0d954ae5733ed1ea1eb5fe759236704a98e246c45f9b067719068d76b8c956` | 0 |
| src/ui/components/info_centered.h | 550 | `2cc0857e51f6966a3225bb5796e8e1295f8d5bd92154a16244d548974617bb95` | 0 |
| src/ui/components/keyboard_switch.c | 5153 | `4ee1d5a0b16f35b8e986e3d16cb50086340db1c5a665c4fbf79f2e7e7938c536` | 0 |
| src/ui/components/keyboard_switch.h | 958 | `78786a829330eaf101021614d0f9aa94d76319965e16ef37e165393a0a71ee58` | 0 |
| src/ui/components/knight_rider.c | 1836 | `e227df5a99bfb0fb90159492462438e4871b089d96f676ae0cef2194db397a0d` | 0 |
| src/ui/components/knight_rider.h | 425 | `5b38b3b1f8a035e4446c84eda0a9a305cb80b80f1d7ef7bc89208213cb6af382` | 0 |
| src/ui/components/label.c | 8871 | `208edee08788d00a3ccdde38fcb505a6279b0a90c7cefd00bafcbd803412e23d` | 0 |
| src/ui/components/label.h | 3426 | `f135077b533da03cc075498e897570a3f0161bef23aa48864becb5977167bac0` | 0 |
| src/ui/components/left_arrow.c | 3444 | `09d2d637d63f8a5c6c61ec0c6276d7f2f6fa97b23d58a6582af3f21569efc5e0` | 0 |
| src/ui/components/left_arrow.h | 511 | `3196849704e2eba89ba6c5ea85f0ea13127dd1081445818ec9fa409d046730f5` | 0 |
| src/ui/components/lockscreen.c | 3456 | `199c5bd8d11f4aece24ca0ec834764cf799cb2db3175fee5bb89ece21f7c5db7` | 0 |
| src/ui/components/lockscreen.h | 223 | `900e7f56572d6f06caec37d075aa969818a165ccaa7c5bc4b917362560dcd34c` | 0 |
| src/ui/components/menu.c | 9273 | `21ebdaac62d659f4a8019c82ab870e764626fa348923a3231e59d111ed115ef1` | 0 |
| src/ui/components/menu.h | 1345 | `706c6ff3f2345513b3c10cff0806c5b85b27cb4a35c087d80716fff790912a99` | 0 |
| src/ui/components/orientation_arrows.c | 6207 | `71686192af175d7e295191e46879b26be6b44c59ed696329cc1530467fa608b5` | 0 |
| src/ui/components/orientation_arrows.h | 530 | `1bf76607ee6050cffed3efe2faa9a9e8ad81190411f803ee0dac28d273ab8544` | 0 |
| src/ui/components/progress.c | 1648 | `947e90bc3a27026e979ce9f48f5ed71c30d9e62e11449c27ef72dc60a3eebc37` | 0 |
| src/ui/components/progress.h | 402 | `8232044dd9aef38e46af994c30c99b30303d61f2d6c8ec442d3ec45f7bfcb9b9` | 0 |
| src/ui/components/right_arrow.c | 3650 | `83a10b58ca690de826c330750f2e24a09eebe43a5390a304236078e97cc1dfcc` | 0 |
| src/ui/components/right_arrow.h | 515 | `8ba6ea528f44d08b61d363e81d5f65d2caca802205d89c8b18df130ef736eddb` | 0 |
| src/ui/components/screensaver.c | 3122 | `474414d341c7f942ca9435d3eef090a1e4d0cc6bd507eacd20fb4e9584b5d75d` | 0 |
| src/ui/components/screensaver.h | 375 | `7ec6bd40c73af2d8f8fb5cf196568acfed60b2979463df6cc9c590d7bd42a62d` | 0 |
| src/ui/components/sdcard.c | 2748 | `8c319b47b9d4c4041cafdf47c7094e2ff5daadc6b7d522e977ebd6b1fb937f30` | 0 |
| src/ui/components/sdcard.h | 389 | `2287aa5eced8006a9e9b407923b89841de7cc505a78bb84ec5372a51c4f3b89d` | 0 |
| src/ui/components/status.c | 1672 | `56d47212b55dd91f6cc887b1a1d877ebc8a8f6d3a4f778aa37ee5939fed34041` | 0 |
| src/ui/components/status.h | 507 | `afa759656dc103c185a053bf5ec2643fc5a7f3df5464ab170938b6cf217467c3` | 0 |
| src/ui/components/trinary_choice.c | 3257 | `4b7f85ae36693ca5a89323187fb542474277fed672670351e5ea096b38868688` | 0 |
| src/ui/components/trinary_choice.h | 905 | `86a614340e27105664d95ae72c1579823cdacad01250dcb35aa2495a2dcf477e` | 0 |
| src/ui/components/trinary_input_char.c | 14903 | `bc419ea37ed53cfb0c960c2aecde3c9b040ad7aa5e07081116e8f0eeda293ed2` | 0 |
| src/ui/components/trinary_input_char.h | 1663 | `ed246da425389a34d86d366639ce4a8ca5a1b8b93458de5b4a6f39c736ac6b35` | 0 |
| src/ui/components/trinary_input_string.c | 18762 | `c565e0b6e2e4f32072a611c257b76f29d20efb27aea23a38c26672a6a14bbad9` | 0 |
| src/ui/components/trinary_input_string.h | 2123 | `d7c341feef38c0723581490bcc465a243460a5085792d83baad8f32e17281d0d` | 0 |
| src/ui/components/ui_images.c | 14893 | `38788e6b993403db59eb8b9675c05c5b5f82ef12f9d059491b98dac29e3b1c36` | 0 |
| src/ui/components/ui_images.h | 1814 | `9d0d48dc2a867a42c1c1f8935d6964906f18c509b5183d9ef5f18b8e7027a6e2` | 0 |
| src/ui/components/unlock_animation.c | 10949 | `8cfedb0276426a8b6ad17cc94382d747285b74e95c820cb0b8a1f9cd62322bd1` | 0 |
| src/ui/components/unlock_animation.h | 269 | `031cb5d1a4a989b037b9c91785b7128f7e4a02621c4bb72973eb80e60ffd7221` | 0 |
| src/ui/components/waiting.c | 2901 | `876058da24e77fa58c9f4799480b7def7ffcd96bc3b80d5705fc74d140ba8fb6` | 0 |
| src/ui/components/waiting.h | 611 | `0c497151feb5ed87172f218a79524b725ba06c6b8ad2dac99e9123988313514d` | 0 |
| src/ui/event.h | 563 | `ceb3e26bfa9d5441f571eb846273ecade740f6b1353311ce55e990dd5e659779` | 0 |
| src/ui/event_handler.c | 1520 | `7e183e8ce31c33254a45ec1a02e2fd7d3fb91e69bb1cef7e5e190030fb08dea9` | 0 |
| src/ui/event_handler.h | 267 | `43ec16c77d45de807db6cd8a50463e1fc7bc4a79443493973eaccd70ce019467` | 0 |
| src/ui/fonts/inter_bold_32.c | 220230 | `a1b38b3f0de200baeff70ca8d4342fd1e003c319b455b3bd8797a524470ada2a` | 0 |
| src/ui/fonts/inter_bold_48.c | 477264 | `8f262bd976dddec9c9fc69fb6cbedad692ef7fb05ebc10219aecbbf743214621` | 0 |
| src/ui/fonts/inter_medium_20.c | 109924 | `6d2067839ae61ff2ceb6c4b85da0025bc8baffe5462486e46bf555412769c08e` | 0 |
| src/ui/fonts/inter_medium_32.c | 218261 | `9445298cfc9ce4141e95c867e65aaf87a5cd2a5c6d6ae71ffae4b0689c8f9fe3` | 0 |
| src/ui/fonts/inter_regular_24.c | 130640 | `0f898381eda14ad4bf04eb3d1eca09bae336e85b0c35565ca06a719653ef0ac4` | 0 |
| src/ui/fonts/inter_regular_32.c | 195082 | `14680f1a8e90933a0d6d84e0e8760548cc3a456392c5703a3dc9de8053f1fd18` | 0 |
| src/ui/fonts/inter_regular_48.c | 416631 | `fa6169cb2efdf02dd8ba3dc4642001d1e5efcc24ede28723902003fc653c97d1` | 0 |
| src/ui/fonts/lvgl.h | 391 | `11c17c628828fa80cf4d76e36e738c309ee0e5bd18344dd8175625733c54ac68` | 0 |
| src/ui/fonts/lvgl_font_compat.c | 3435 | `67a8045562eb177d9798515529acd8c3927cd7045953c9960e8b7c35a1c991c2` | 0 |
| src/ui/fonts/monogram_16.c | 16168 | `a0e5970175aaeabbac7299cadbb545920af1f31d076539c44d0ff0bc4e7649a3` | 0 |
| src/ui/fonts/monogram_16.h | 158 | `9c1f589005022ab443d2e0320d282e4aa4c5799b3d255fab19a8df68d2d4c426` | 0 |
| src/ui/fonts/monogram_16_bootloader.c | 4840 | `5de1f46de5c48efdb1ee97ddde36b48ab68c1dd84ed87d92795c461a71c77fc4` | 0 |
| src/ui/fonts/monogram_16_bootloader.h | 191 | `be9c3f187d51c4c9d06de25ef871450fec51b85ee964da350ec7babc30f64d67` | 0 |
| src/ui/fonts/password_12.c | 1405 | `3e9db0e36887259c555fe1ba6393ef9efa4f66c8f7bcb9daca4d13f66fbb724e` | 0 |
| src/ui/fonts/password_12.h | 198 | `c52f920e705997665f8d6a6a14cf4071f8953dae7f047ee8781bf40b29898369` | 0 |
| src/ui/fonts/password_9.c | 1388 | `b089160d8076d8b1b0fec785e8ad9e17870aaaebd543a44ce40598a0f9cda800` | 0 |
| src/ui/fonts/password_9.h | 154 | `90f8f69a18d7dc70b40620af8974468d44b61f899f6db6139ba61f0f4676910b` | 0 |
| src/ui/fonts/regular_11.c | 32527 | `7b364b0fc185ca3f17222133fea1ce2ea7551077cdabdeb1e9a404f7f9f1d4d5` | 0 |
| src/ui/fonts/regular_11.h | 154 | `0a98c23bac34f471d61acf4fa92a2c837e07806433ca95aa131eb5086c6b8835` | 0 |
| src/ui/fonts/regular_12.c | 33621 | `061359ab0984d07b83e698f7cec0082d786731378f288b383fd8710f418a946f` | 0 |
| src/ui/fonts/regular_12.h | 154 | `c284235a85a0a20cbe2546d488d6588be37e6df1b84e6d780d293f646813cb9a` | 0 |
| src/ui/fonts/regular_9.c | 31381 | `7aaab51be31de788729c9fe46ec4024079fe1bbf7fb5f389c064af8e0eb91a31` | 0 |
| src/ui/fonts/regular_9.h | 150 | `98f7215d5be8c70c3cc3aa8e97184a5f391201367c8b73d7a3ccc56b1f528af3` | 0 |
| src/ui/fonts/regular_9_bootloader.c | 15876 | `5453ccee1557b14014c4b4a7ab57004ab4b814d98f454bd04756ae80a7b2dae2` | 0 |
| src/ui/fonts/regular_9_bootloader.h | 183 | `e1d321850785b1cf43e041776fb84f961f042c34baf1809870e1a716ad1483e6` | 0 |
| src/ui/fonts/regular_fonts.h | 197 | `8a8e025aa12cff224593361e93ac0b80822f17945e297ba5271c0cbbbff12580` | 0 |
| src/ui/graphics/graphics.c | 700 | `04b7f519cfb183a24fe900af85577a43332d093b5602cab775604fe2979e2920` | 0 |
| src/ui/graphics/graphics.h | 496 | `a4ce7700e842555679eb3e4413370cefa48cd2a27861e272f5e0c0bd64fbba96` | 0 |
| src/ui/oled/oled.c | 4379 | `ed7a0ba91c16163d3b5b8cd5dbba05d155c6cc8f2a46d812775324ab03a88757` | 0 |
| src/ui/oled/oled.h | 2770 | `11bc1ea771b107fc399ab5830fc6a542d1b85f8f41dad91abe2d870bcf2ec96c` | 0 |
| src/ui/oled/oled_writer.c | 1290 | `1e49807ebed8391f58f225bc0e3ddbc5bc47a8be969e00ffb18f8aea69c96840` | 0 |
| src/ui/oled/oled_writer.h | 436 | `484da60c1c4ace43f60680ab6067265cb3201962065648c3475b8a2f04be65c4` | 0 |
| src/ui/oled/sh1107.c | 4742 | `4cdbdd49fb69f9a9ae925988c4bbfc477e61fd884492347a09375e665e1de17c` | 0 |
| src/ui/oled/sh1107.h | 424 | `6f11af7cd69de4fccf04a5ca441b9d39c7b4c40f06bc9937ec17283af768348c` | 0 |
| src/ui/oled/ssd1312.c | 4806 | `c229caef4b0b9f99872bdf2b6015d38a180a85f9aa248521c490262ca2fb1173` | 0 |
| src/ui/oled/ssd1312.h | 412 | `7e80fa18a1ff73103d7420dc2f8e028b1746d879739f49dbcc264c27821e6b9a` | 0 |
| src/ui/screen_process.c | 2920 | `c797a0a0dd7f8a7519bcc53fcefb344d5b5fb78baf2691d3c40e655197e9107a` | 0 |
| src/ui/screen_process.h | 1324 | `4925324ae565ea56f3b245de7e65211ba042e42d3ca1f08f9959f59a26302bbf` | 0 |
| src/ui/screen_saver.c | 1605 | `e5d01795a1d6c770a03cd378030fb5badf2394bd018ed5b839dd4913f299ef7e` | 0 |
| src/ui/screen_saver.h | 841 | `6d9596bf239ce5933c80ceaaf9ea6f1e8072a6abb18ced3780aa21d32ac4628f` | 0 |
| src/ui/screen_stack.c | 2027 | `197e7ea15e96db7fd131ea244c960a3d4832517ebd3f0a3d79d3a64af3042241` | 0 |
| src/ui/screen_stack.h | 541 | `15906232878e5958c681a35ed055844d98b3dd1aac15978929c8736e47fcb6ae` | 0 |
| src/ui/ugui/ugui.c | 24444 | `220bfa84f9ce74facbe56797bb218cb57d22c4bf009f083cf8a3dc5cd03a695f` | 0 |
| src/ui/ugui/ugui.h | 5912 | `d6faaeecf2aa46263906f5ac5a062b10e74583c75a783dd0f3ebee5cc98627d0` | 0 |
| src/ui/ui_util.c | 8629 | `9de60147f2cb3098e19bfff7bca0b9d88c5aa3a48e1f004ea14f57d02dd4aae4` | 0 |
| src/ui/ui_util.h | 5096 | `c27d10d4029d2bb1093a8a9c119157e89d60f49a3d3b9c78c7f896525767a2f2` | 0 |
| src/usb/class/hid/hid.c | 11109 | `bcd4ce1b19d1124edb7e01ef42f03e770287cf5d1657bc6d20775a084f958019` | 0 |
| src/usb/class/hid/hid.h | 4109 | `577de80520fb227d0c59d54cbee8b7e2a433255b9d57b63e02de85666d087e0f` | 0 |
| src/usb/class/hid/hww/hid_hww.c | 4754 | `6386782800379810d5b871a51d656181425832582fe7186513a0d7cd894bc042` | 0 |
| src/usb/class/hid/hww/hid_hww.h | 1709 | `c55cc67135f87e9364a8b27a1cbc8c9c1c1c532c1f483357194be370fb74fb3c` | 0 |
| src/usb/class/hid/u2f/hid_u2f.c | 5262 | `ce8506310c076ae0cb615c00b78afab8d9958f9cbc5de15cfc7e7bd32ab55cb5` | 0 |
| src/usb/class/hid/u2f/hid_u2f.h | 1623 | `bcec43c5c70c6eefbbdc8d1e6005860562c9af74c9bda31084b76fd16266ec5d` | 0 |
| src/usb/class/usb_desc.h | 7046 | `5065da9afd04d585483cb4bb706a6ecfd53e3504c5a96c757959f36385d9c377` | 0 |
| src/usb/class/usb_desc_bitbox02plus.h | 5016 | `4538dd98aad944ad1a79ef1004234c299475cb6fe215ad3f4bc62b10a294172b` | 0 |
| src/usb/class/usb_desc_common.h | 6509 | `f81e45537c09af04b33ff8a5705458630940f4ab89805dad0b68b2f5567ea801` | 0 |
| src/usb/class/usb_size.h | 166 | `f9ec0deac44a546890d03fd364d6f7c30337cf3af0bf10b8dfd544210082621d` | 0 |
| src/usb/class/usb_u2f_desc.h | 3758 | `6d7dd70956c39337cceb388e23a971840d5d4dd1e6aac0907fb2184b52fa1b50` | 0 |
| src/usb/u2f/u2f.h | 3133 | `d76b09a8fb63da8ecf6b6490b165c20005247b9b1a0c391070c60e030a42b63e` | 0 |
| src/usb/u2f/u2f_hid.h | 2982 | `66976af1f1a767ae9c7e4632d530cfbe0e7849e4acdeb2c13d020dede7ecee9c` | 0 |
| src/usb/u2f/u2f_keys.h | 2313 | `a162f73d950ca857744d864a07e27d90dd9f78c0be9ddc86114a2d1ae22ff97b` | 0 |
| src/usb/usb.c | 3090 | `0d427e3fb7ab2dbba2b65367e70ae6d2017d9c8ff3191109467c9edb7890564e` | 0 |
| src/usb/usb.h | 275 | `f40df9cad0283326621b13dae6dd0027f43acb95ce640f28c7e6914a8d2fa809` | 0 |
| src/usb/usb_frame.c | 5540 | `92d3fe3c443ca9989db2f96c976a931517c41394342bd98f314d1d3c215c78b0` | 0 |
| src/usb/usb_frame.h | 4220 | `b4e0030db88b0911f7ee8a8ffa623a6bd470b0eb543eb7b4422ce6b507d3737d` | 0 |
| src/usb/usb_packet.c | 3034 | `a08a57316ff2a59ced1b13b2518bfc12ba116b19feede5d5e147e73a8fab2db1` | 0 |
| src/usb/usb_packet.h | 865 | `7d2d02d5d55c31764bd99c5585730cbbf2baf6442fcd63ccae826284baee801a` | 0 |
| src/usb/usb_processing.c | 13698 | `e62fb4705df80476c55490f83bd3889603916eca52be3a6cd3a80ca7794e4645` | 0 |
| src/usb/usb_processing.h | 2167 | `b13ab589a15524572845e28b92af5bcd1757e9bad4fa92d7e74d5a75c1fe1e27` | 0 |
| src/util.c | 3410 | `c89f4e11e0a50684fd7986a85a7d84749b53f7870b6e89c7d88326f2c3192452` | 0 |
| src/util.h | 5262 | `8bfcd192ef4b5709bdc647646e9e595c2aefd6dbcd94fa79a84c13161992183b` | 0 |
| tools/atecc608/config/config.go | 11409 | `184f8b713ca7771f8f16299f960f301884ee2794e40a7db2754844bfa4db1f08` | 0 |
| tools/atecc608/go.mod | 26 | `f4755a635cb61efa0b2312266e47f195381c2c2ff373ca9f1a193f0f432e3999` | 0 |
| tools/atecc608/main.go | 14826 | `39a1a4d3f2edbcd638d83e20f8b5c858c432a749e2a538711b3f498b461176c2` | 0 |
| tools/prost-build-proto/Cargo.lock | 10683 | `7082227fd2d30d56308df664b7832f0d586d68eb22710492096d6c86e442eb73` | 0 |
| tools/prost-build-proto/Cargo.toml | 334 | `1f669b2998c5ed56cef2f50a1c27ecaa047877d58c4d16d4d134dc2bcef3b991` | 0 |
| tools/prost-build-proto/src/main.rs | 437 | `b3f4fa1151df049a8db26afe78f28128843d6dd27f02c665f0a61a1194f8880e` | 0 |
| tools/ttf2lvgl/ttf2lvgl.c | 41257 | `14e0cae684c38939e0b962515b027de2999b25f16cb5137b3ba3230936d2b40a` | 0 |
| external/cryptoauthlib/app/api_206a/api_206a.c | 15307 | `d5ce1f2d962566807980f8c02fba4975a854dd93453a0acfa95e09cc5e88bb22` | 0 |
| external/cryptoauthlib/app/api_206a/api_206a.h | 2891 | `becd7c920e878939d3c172ef89000633b0f66dd5614465f8f0c3e400ad77fdd7` | 0 |
| external/cryptoauthlib/app/ip_protection/symmetric_authentication.c | 4967 | `94ef44e7695fe4dee92bcd78acdb062c0ed4765e7083097339207f9ce8d13be0` | 0 |
| external/cryptoauthlib/app/ip_protection/symmetric_authentication.h | 1648 | `c49d4fe6f78bea0aa00d03bca44c6257c69cc2b6174890ae2201ecfdb6d9401b` | 0 |
| external/cryptoauthlib/app/pkcs11/README.md | 9751 | `336cffbc3ef5787fdcc41289bcab29a3668cc03d10e2bf936c7264ece11f2fa0` | 3 |
| external/cryptoauthlib/app/pkcs11/example_cert_chain.c | 11711 | `4de8a105d778e914baeaa5cb60304a48a658e3cc1eba43c016286e96b60aca60` | 0 |
| external/cryptoauthlib/app/pkcs11/example_cert_chain.h | 291 | `f5a21d013a2bb13d7722707f24dc270becbf9bf65a635f99e148bb6c09398ea6` | 0 |
| external/cryptoauthlib/app/pkcs11/example_pkcs11_config.c | 6435 | `dcad1f6bc70e99f032de41746fbb3aa95947ef1619bcce470941e6a20469e068` | 0 |
| external/cryptoauthlib/app/pkcs11/trust_pkcs11_config.c | 5959 | `a3a6f251fb95901129df19e70a07875c04cee0bcb7fe6a57c1286bc3aca7eb23` | 0 |
| external/cryptoauthlib/app/secure_boot/io_protection_key.h | 1570 | `c23acbe676d767d275ab00252cbb6c857aa7bd2c2c1de16db5b71cb4762d54e9` | 0 |
| external/cryptoauthlib/app/secure_boot/secure_boot.c | 9473 | `e76cfe687fdd89da8287eeb746fa26e628bcbb6512a8fb3a4f219c44b396931a` | 0 |
| external/cryptoauthlib/app/secure_boot/secure_boot.h | 2898 | `d2a8870794496b5b92ff057fc88b9fc0f898bd99c43f511d0da8e543e7cbf491` | 0 |
| external/cryptoauthlib/app/secure_boot/secure_boot_memory.h | 2336 | `c1b98745643ddb1b6d6fd7516b2e97a41aac6d737b8168d239bafb7b6e7ee1a3` | 0 |
| external/cryptoauthlib/app/tng/tflxtls_cert_def_4_device.c | 7675 | `174bd2615d7d94f5235a0c28f30127ffe095aef3843b78956f3b34fad129c725` | 0 |
| external/cryptoauthlib/app/tng/tflxtls_cert_def_4_device.h | 1555 | `cead3ee8d90f74f240feb6bfabb4324c01e91b9cd00da6991e93d18f0fd4699a` | 0 |
| external/cryptoauthlib/app/tng/tng_atca.c | 3727 | `98decda85d261c15f156fa2159d4e6c6f956222be004d5e87dafb2f3e2091b10` | 0 |
| external/cryptoauthlib/app/tng/tng_atca.h | 2599 | `5886a2065b7aee185e214b89306c6ca75f7567a543bea1eec64b7f5e8d47c01d` | 0 |
| external/cryptoauthlib/app/tng/tng_atcacert_client.c | 7115 | `acad9769b2fe1283a641c49d6871bb4069012be07e9681e10e5bfeea70e41417` | 0 |
| external/cryptoauthlib/app/tng/tng_atcacert_client.h | 5987 | `cf89eec191bb7f31fab46b389c91390e25c1d6087ebcce8dd8da76e845941100` | 0 |
| external/cryptoauthlib/app/tng/tng_root_cert.c | 4624 | `6e5af7e514a2b82df638ecbe8e3149e4b7fa5c9272e58fda33f39c3467498ab2` | 0 |
| external/cryptoauthlib/app/tng/tng_root_cert.h | 1614 | `3d5c093d4fca74f84bd42f044e8fac18c7af893a792353cbe2cba69d02d74c9a` | 0 |
| external/cryptoauthlib/app/tng/tnglora_cert_def_1_signer.c | 3680 | `38a976b4983c2c8dffddb28d70b39cbb1e67e43f7ade08026bfa34345bb78675` | 0 |
| external/cryptoauthlib/app/tng/tnglora_cert_def_1_signer.h | 1560 | `d5ac56e11f96e7884224f22a62808c3ffbf1ca38da45682f013d0b7f9e8c230a` | 0 |
| external/cryptoauthlib/app/tng/tnglora_cert_def_2_device.c | 3814 | `410d547617400f45670eda995e18035a99141eddb32be660e8b47b10311a6fd2` | 0 |
| external/cryptoauthlib/app/tng/tnglora_cert_def_2_device.h | 1561 | `700f180e789e32522f43096a9f1d967aee8ace1af061bb822669977e189f1e5f` | 0 |
| external/cryptoauthlib/app/tng/tnglora_cert_def_4_device.c | 8508 | `d51973a657797423363cf872a6c928ac1013ca030e803c8e57a7256ecf940cb3` | 0 |
| external/cryptoauthlib/app/tng/tnglora_cert_def_4_device.h | 1608 | `f20b178d3be797085c20df335fa2d50b4fea2c31b1e3fa758cfba17f96d2ee55` | 0 |
| external/cryptoauthlib/app/tng/tngtls_cert_def_1_signer.c | 7196 | `42dc9ed786c7ac8597200b948558df9fe1b6226671ca5841fc7aacfc5735a236` | 0 |
| external/cryptoauthlib/app/tng/tngtls_cert_def_1_signer.h | 1604 | `b8a2b9cb4996ef4a2073b9ec974b8288cd75179a1df32a5306e83f1d0c714663` | 0 |
| external/cryptoauthlib/app/tng/tngtls_cert_def_2_device.c | 7855 | `2712f973bc26a1065558e373b6a3aacf61473bd419f38b15e3996d05828b1096` | 0 |
| external/cryptoauthlib/app/tng/tngtls_cert_def_2_device.h | 1650 | `54b76930db788172a154b071d7f1030ed1753c46e983d442926f3ea2c263d754` | 0 |
| external/cryptoauthlib/app/tng/tngtls_cert_def_3_device.c | 8458 | `ff07b415bcf72ff5ce20f27f3ad8f5450d1ddacdb291a6cf00e383d5cd2e7122` | 0 |
| external/cryptoauthlib/app/tng/tngtls_cert_def_3_device.h | 1602 | `615687631e3abc316c67635db8299d59dfeda6428c1e0b364c4ec7275c312a2d` | 0 |
| external/cryptoauthlib/harmony/config/cryptoauthlib.py | 15305 | `2fa0310a4270809b4dd6f137a6a258e30dd2a61b2239222c638db711d82d2fbc` | 0 |
| external/cryptoauthlib/harmony/config/device_common.py | 1532 | `359798fab180049617b73d7a00edfbab2360b82ed1c5cb93165b72296d715824` | 0 |
| external/cryptoauthlib/harmony/config/device_instance.py | 9213 | `3feac52fe247d01a57e97481410c2d1b127510d857b30b158f45cc5eac646c70` | 0 |
| external/cryptoauthlib/harmony/config/pkcs11.py | 5674 | `a6c657c04cd273b3492deaca43b3db58a4f6f99fe8cd90ed0d80562470b5f5cd` | 0 |
| external/cryptoauthlib/harmony/config/tng.py | 4447 | `2a3e5cc106cb09b7251713ebe8c95e167750890f2deed01ccf1e70a6f3c26293` | 0 |
| external/cryptoauthlib/harmony/module.py | 3670 | `13e2cce6acd1fc65f94bffa2ef34ccb05c798b680bfa3adc71dec80d0280e70a` | 0 |
| external/cryptoauthlib/harmony/src/cryptoauthlib_main.h | 745 | `e04e243dbc3d235affbca4a1fae7891a6a70d12985dfeecb9f7608a4ca0daf43` | 0 |
| external/cryptoauthlib/harmony/src/hal_i2c_harmony.h | 2082 | `28ab8149f62a76ef256163daf02bf3b123e22e9e09538f5c6a15607c0ac89d70` | 0 |
| external/cryptoauthlib/lib/atca_basic.c | 126331 | `ad66baae8500efb167badb7512b93e4130b607cc6b07d55249dda5aa08fe2607` | 0 |
| external/cryptoauthlib/lib/atca_basic.h | 37087 | `97be5cfbe62f4841539573ad75792ae8aaf04fc8d4cba14b0204663843cadb7d` | 0 |
| external/cryptoauthlib/lib/atca_bool.h | 1586 | `926074b48e3db661fe4d5652a76baee68b91bc18efb4d77b4c072b81ac325ab7` | 0 |
| external/cryptoauthlib/lib/atca_cfgs.c | 5536 | `5be8cb927756553b5b5d2e705eaa0c5d5c92e671472c17c106025bdff1cbb4dd` | 0 |
| external/cryptoauthlib/lib/atca_cfgs.h | 2529 | `4c1b73724196b5ae946010b1cd397fa3f16ed43d45e3b51cda97fb57e837edb2` | 0 |
| external/cryptoauthlib/lib/atca_command.c | 3454 | `052196da2fe9ac0f7ad441baebb18c6bc669db1afc9ee1844c7df472603dee73` | 0 |
| external/cryptoauthlib/lib/atca_command.h | 2566 | `3e1e6181d2b3189674ba09d7756ba8e6d7b9da9c54129f17345236632707ccae` | 0 |
| external/cryptoauthlib/lib/atca_compiler.h | 8939 | `d6eeeb082d65cd1001c42cea28a00bfc9ec56d4f59c689525e22b8e04a4f13c1` | 0 |
| external/cryptoauthlib/lib/atca_debug.c | 1643 | `797bc4a42065b9889215b0e1dbee3978d7186ee5432c3a0e4446ce74a741e264` | 0 |
| external/cryptoauthlib/lib/atca_debug.h | 246 | `9fe972773847b28f97ee17c0704bdc2de7d10af4bdc0f7ca3b133e1d7daf4809` | 0 |
| external/cryptoauthlib/lib/atca_device.c | 4882 | `34afd9aa03e931c1d1fd00bbadd767d0cfeff25e05d89f2691911685e9ea2707` | 0 |
| external/cryptoauthlib/lib/atca_device.h | 13269 | `d48ef66f48efb3e0c5f7750e5a9f97602422590f99dfec5b9599ac50386c25e5` | 0 |
| external/cryptoauthlib/lib/atca_devtypes.h | 1747 | `cd0082011dddf700281801090e969d589c848a802b807752a256a52c7dcda231` | 0 |
| external/cryptoauthlib/lib/atca_helpers.c | 25755 | `4cb89568e6e1fd8742e7ad9acf0d24e92602db0cdddfb1af2012e40b09b57e0f` | 0 |
| external/cryptoauthlib/lib/atca_helpers.h | 3416 | `d5232f199ee469ae317938193582b392a0b3dba5457b278d9b6194f32cec83c8` | 0 |
| external/cryptoauthlib/lib/atca_iface.c | 9159 | `b3e55a5e5f8b82691ee51640d1169d86f3af682b308bd7fc4fa9d11648e227ae` | 0 |
| external/cryptoauthlib/lib/atca_iface.h | 7399 | `10260b76b9bbef7c8dc0fff866b136b019ed8c39a3ce61ff9d078e0479458cfc` | 0 |
| external/cryptoauthlib/lib/atca_status.h | 5366 | `45641f02fb165c14152e3ea14b41a9c34094d559947b07c119ad38a6778fb601` | 0 |
| external/cryptoauthlib/lib/atca_utils_sizes.c | 3418 | `bd958ae085c2c5751a4e0b736b0a57c5de29f5a247fab60f888620efe2a5f5c8` | 0 |
| external/cryptoauthlib/lib/atca_version.h | 1545 | `ba246e92a539d86d1ba5d827da852b30cc017f84345dbb4ca6a91ef57c1b053b` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert.h | 3032 | `852db1817d64561bdbbe2906056d766a38c2bd9a1847e7e2220acab7bb3304db` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_client.c | 13525 | `01378b673dccca786a0bf4e4c6d2cd1b9f8e68b05e158cb64268cf7c17f9efe6` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_client.h | 8213 | `2ebd2bff70eb2b865e734b69bd02dc8080662dc54a22b23dea7378a0cd5aa379` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_date.c | 32659 | `911508f55380dd08a5f4f0dce248931e18ee10254c0471263be30899f43ba294` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_date.h | 8397 | `e63b01a374519138f01db2cc5879e357ed9582d5ff1336afc51a075ecb927f0a` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_def.c | 57772 | `e3d470d3bbc5efe5e2bb2dc53a10980172fa0dd4ec1a5da080a15117f8479474` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_def.h | 41649 | `eefff3e9ea019b12aca38ce057f5b5e4584a3629f74d36650922a5e402da16cc` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_der.c | 16350 | `c13f286af27adb864023ed2d19c6d8e138bb2f45a0c601a1c1c24e6a96aef564` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_der.h | 7558 | `afaebdd08edc55db6465795aefe56ebbdaef8d0350924d8f70ef8d875f0fa398` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_host_hw.c | 3114 | `46648cf1d28767eb64a522a3d460a054df305287953d1221b11b47b2623c9729` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_host_hw.h | 4450 | `3554a583c4d5cb10264dda55a459bf475a6a529b591c79bc11bd2e56f4713527` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_host_sw.c | 2924 | `6706cdc3e8eda7475acbe110c1434feed6a733c8c59daabdfb4e6595c4a854f9` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_host_sw.h | 4336 | `e4cd37f9f6223473b2f2c384962cb3564212e9ff95e89019b04b3b98d80011b4` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_pem.c | 5824 | `8775d02cee595578f602085bb3e8d2f9d4a2f5992963038357b0516fd004cd7f` | 0 |
| external/cryptoauthlib/lib/atcacert/atcacert_pem.h | 5600 | `3a8840e28ca222153aafdb946359c11109ba1a0ceeb7b6649d5c6e527fbe69c5` | 0 |
| external/cryptoauthlib/lib/calib/calib_aes.c | 6075 | `b0ee8c5ee772efbbb3e605b0ee3e809ae02d8056f06535ffefcd3d19e05b8fb7` | 0 |
| external/cryptoauthlib/lib/calib/calib_aes_gcm.c | 21139 | `a41e3eafc70d079d17d0ccc620bc25f609d659d7245f9bd60770f195040b8761` | 0 |
| external/cryptoauthlib/lib/calib/calib_aes_gcm.h | 3926 | `c0add73cff66de9b61d8770d6ee732323fe7df634594364ebac008a79b24808e` | 0 |
| external/cryptoauthlib/lib/calib/calib_basic.c | 9400 | `a069cc571c623a21a5b0183ec00365c61cb188297f88a03f6fd64f66df8d4277` | 0 |
| external/cryptoauthlib/lib/calib/calib_basic.h | 12173 | `cab07399a08f1f920d85aacda4453cecc1f74073a9aa8524340aab78b18c3646` | 0 |
| external/cryptoauthlib/lib/calib/calib_checkmac.c | 3718 | `a8641e57fe4254055139476a623553feeb524aae6ba819c87f11864ec845222a` | 0 |
| external/cryptoauthlib/lib/calib/calib_command.c | 20906 | `f1a6400f05ed6c11a851e976f53a8898826df6406199b21dd50df42159881a4a` | 0 |
| external/cryptoauthlib/lib/calib/calib_command.h | 53202 | `daa823f84a4a6a32cce2cf7d42bfd1d97fabb5d46df2c3228d0de96259386782` | 0 |
| external/cryptoauthlib/lib/calib/calib_counter.c | 4562 | `c1d01ea200bc8e15ef95eabd5d4e0af203f47a8fe0b377902bc33960e0204e30` | 0 |
| external/cryptoauthlib/lib/calib/calib_derivekey.c | 3191 | `594fe02c9af7db294e311b93e55e0fcc9a8936a31bfae1ca3cc94a95f11c9f76` | 0 |
| external/cryptoauthlib/lib/calib/calib_ecdh.c | 10853 | `c6471c07c0685ef5da7b6889d27f75f58a7f5c3f16e29c57819e3173c9d4573e` | 0 |
| external/cryptoauthlib/lib/calib/calib_execution.c | 12160 | `ea99cb59f721f6aa0485bc541660f1e5795f726840c4f3ac18ff4e2ffeab2f36` | 0 |
| external/cryptoauthlib/lib/calib/calib_execution.h | 2273 | `a98dc9774080ed54d4c261c40c66a4f9cc75886b55df46484baf66471576dee9` | 0 |
| external/cryptoauthlib/lib/calib/calib_gendig.c | 3856 | `47ef2824db5c16ef34467382f384536083bc3a21a3198807b061f702c4a416fc` | 0 |
| external/cryptoauthlib/lib/calib/calib_genkey.c | 5605 | `5b86a68cc2260b003d5bfe19e5ee8278f18765e3696f9c7ed451f38bd60e302a` | 0 |
| external/cryptoauthlib/lib/calib/calib_hmac.c | 3552 | `c6c089eed42405869075e0345d87e07dec0d99ce47568b00c37cee0727a37d34` | 0 |
| external/cryptoauthlib/lib/calib/calib_info.c | 5163 | `8fbe4234e1459aab7ab630fb7c0bbd87175e5df62018fbfc6cfeff722961cc67` | 0 |
| external/cryptoauthlib/lib/calib/calib_kdf.c | 5520 | `34e91586920a2bb029c27766a94a57ab399ac6dadaaab1d72eba1329d48264fe` | 0 |
| external/cryptoauthlib/lib/calib/calib_lock.c | 5715 | `3d48b48914e2a6cad1b8a1a68ea869de0730f32c22e40760f8fcac398ce4bfb9` | 0 |
| external/cryptoauthlib/lib/calib/calib_mac.c | 3667 | `806ec85793d069373840e227ee614b99d696cbc33c34a61cd2a71e839a9cfb7b` | 0 |
| external/cryptoauthlib/lib/calib/calib_nonce.c | 8412 | `ecde35178d24ef5bb46bec55ef99db9fcd259381271810cb174a45716ba10ee6` | 0 |
| external/cryptoauthlib/lib/calib/calib_privwrite.c | 8240 | `1d2ad034a4490d282424c969e5836f4d213f1b2d2012f394dd95b39a210bfdb4` | 0 |
| external/cryptoauthlib/lib/calib/calib_random.c | 3060 | `91d2e658769c5878b180cf12fcc7cf7be6e3c43afa29e4eeed1d9f0b92a2ba84` | 0 |
| external/cryptoauthlib/lib/calib/calib_read.c | 25781 | `293b19883f692fe37e9eec6e329e82ba7caa10a476d6a710889f67b9695f9957` | 0 |
| external/cryptoauthlib/lib/calib/calib_secureboot.c | 8352 | `b5cda1a38ee600a6d3c1498c861a2a0180ee1eb235b0dba6d9c32a9fc8bf08ed` | 0 |
| external/cryptoauthlib/lib/calib/calib_selftest.c | 4052 | `1dad33906c11210bc6a35aae483112b60c92664449e8077d7c392c2a9de76564` | 0 |
| external/cryptoauthlib/lib/calib/calib_sha.c | 20407 | `65d38dce718560bc3eab0a7528bb4349212deb5219c152ad4d805d16a057758c` | 0 |
| external/cryptoauthlib/lib/calib/calib_sign.c | 6997 | `b5eeba1bb7ce5ac077f3eb1f3d4001f12d3fe99ea4aa6596ff9a66a6e5dded5b` | 0 |
| external/cryptoauthlib/lib/calib/calib_updateextra.c | 3144 | `9a712cf53d09ccb4ac17c7c655a85054575519e15560aee14b67f1f490684233` | 0 |
| external/cryptoauthlib/lib/calib/calib_verify.c | 20657 | `6ccbf9461762e51d163fd4b69fc3bb678d12d27b503378a327578c8b1751c83c` | 0 |
| external/cryptoauthlib/lib/calib/calib_write.c | 20897 | `de896466e15a5739b55ca4b66c658ae9e6ffc192e0e90164cb2b3f71ef7c4a3a` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_hw_aes.h | 4230 | `d8a1af7bb9ee93f918bcc8f87c610fc29e31033abd51344d98e96f33fd9849fc` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_hw_aes_cbc.c | 5937 | `6d574d733ec2a449c0ba752a5feb3722ae6491833189fba8506f21e6d61af02f` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_hw_aes_cbcmac.c | 5692 | `3b60e0686502863af9d557646d09e68b93b3b607c0d3ffddee0791c831adead7` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_hw_aes_ccm.c | 21098 | `1e2f566947cebe288aa5280c12404c3f8836ed64e2bd8422355fe3c521ce0796` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_hw_aes_cmac.c | 8072 | `fe3ffbf587b5c2291eba649534ef689b85d9cee18fa1a45082e7af8dc5613b19` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_hw_aes_ctr.c | 11347 | `40cdc322529bde9af6e018a92f4fc1eabeb2e2895cee6bee8743ea14b456c403` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_sw.h | 6515 | `d172810d2e7532b940cf8fc0b096ecc7631286ea3d370183438aa1ae0581a989` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_sw_ecdsa.c | 2080 | `fa2c8da252a940e6bfbfd53cc1952d0fb96146f96c6c5d051b853b46a2e459e4` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_sw_ecdsa.h | 2126 | `a0f3b3dd9c260a216adc49e4f13a0edc9e2891e67496a674dd66696b092af221` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_sw_rand.c | 1672 | `54353489786253ab575083702ba1b31564d2af17b719288ce82abdec981a54c1` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_sw_rand.h | 1669 | `6a0f009d909b9dd465b6dcbadec774c07ff90f9081b3c44c6bdac005ee0afe53` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_sw_sha1.c | 3317 | `cd088f7167eab6bef18f31ea83d9a356276814006707d836dde8f01ba4ee181f` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_sw_sha1.h | 1965 | `36b6ba8f892bd697b2a97ddcdfe1626c9b84fc7820ca537d871d4d82c0feae23` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_sw_sha2.c | 7728 | `147701ce979daf7e95fed5e4599d71f2e8689ec0fe1f73da2cd8de7552a867f3` | 0 |
| external/cryptoauthlib/lib/crypto/atca_crypto_sw_sha2.h | 2492 | `53d8fec4e82f0921736b3295e8d0451707d5d77c74952a89c1cd8f8a7b447de3` | 0 |
| external/cryptoauthlib/lib/crypto/hashes/sha1_routines.c | 7838 | `6a62989a2ce78d332733511b3d05d52c5b219aab7f86fbfc0b109a134555f029` | 0 |
| external/cryptoauthlib/lib/crypto/hashes/sha1_routines.h | 2364 | `8e8463f36541cd7bd3b1bf3353b9851b327e830bcb6af7aa08a7feafeddcef1f` | 0 |
| external/cryptoauthlib/lib/crypto/hashes/sha2_routines.c | 9945 | `08c3849a3f4d1b985056e267c7eb2c147489b4c1b61239cc583555578b626673` | 0 |
| external/cryptoauthlib/lib/crypto/hashes/sha2_routines.h | 2160 | `1132df96ae80fbb6da122a13fd36e912014c77462efe02ed7822986d9da8de31` | 0 |
| external/cryptoauthlib/lib/cryptoauthlib.h | 4072 | `136c985bee9e975bdb7b2145ef362ffb3aba0712772753b2a54d3a2d77aa142a` | 0 |
| external/cryptoauthlib/lib/hal/atca_hal.c | 8930 | `e7456b5445e3e6df2d7cb487942ac68517c5425a776f20e7f5d26e474dcd5af7` | 0 |
| external/cryptoauthlib/lib/hal/atca_hal.h | 10037 | `174121242701462c013e1041e689f87938245c75736ea65a928ad20bf6b07197` | 0 |
| external/cryptoauthlib/lib/hal/atca_start_config.h | 186 | `b29a69137b3e32126b54d5e7077e9f9e1ccbd24fdacacf7197257c974ebe0435` | 0 |
| external/cryptoauthlib/lib/hal/atca_start_iface.h | 185 | `a4d3739b7689019106ba8a9d479832da72af89b62b9d6ede4c1f4a24c97a7618` | 0 |
| external/cryptoauthlib/lib/hal/hal_all_platforms_kit_hidapi.c | 9504 | `dfeb4bd23627caafdc9ad7f3f3bc5ef23e3c8c4627f53f6deab4fe16e29accbf` | 0 |
| external/cryptoauthlib/lib/hal/hal_esp32_i2c.c | 14787 | `d73c4884df15729de1089ae8bf8722b94fc2569b305803b8462c24d1f0d17f78` | 0 |
| external/cryptoauthlib/lib/hal/hal_esp32_timer.c | 886 | `3ab492f1a9b6f69ae6afa65244984e5d5e89170a6aa7e108045fbc3eff637525` | 0 |
| external/cryptoauthlib/lib/hal/hal_freertos.c | 3344 | `62b51adb663528c24c980ed647a7708cb7792a25cc0f1e04c2eb3318a375070f` | 0 |
| external/cryptoauthlib/lib/hal/hal_i2c_harmony.c | 17184 | `b177a6046b83763f4930907397ca5b85f77eac912967c07941bad733831b6e91` | 0 |
| external/cryptoauthlib/lib/hal/hal_i2c_start.c | 14731 | `2f97a83b88296088939446176b88eb763aee2ce4b4356c2d99c8b57ec168bcf0` | 0 |
| external/cryptoauthlib/lib/hal/hal_i2c_start.h | 1983 | `42b500a589fe060b1ac1994a8d42453d60802785049b222e721160b45755b1a5` | 0 |
| external/cryptoauthlib/lib/hal/hal_kit_bridge.c | 12159 | `31877777bc183bb0a51ca3e62bfc3162999d2c05fe8be556a462117454e14a05` | 0 |
| external/cryptoauthlib/lib/hal/hal_kit_bridge.h | 2273 | `5d72a272a62ccd5072df5ad89242c496bb1de2e20895caf5242b118f595a1fdc` | 0 |
| external/cryptoauthlib/lib/hal/hal_linux.c | 7741 | `6bda8a1997786ef309ec64be421edc9022f1e48ea31dbe4484035c8b2780c0bc` | 0 |
| external/cryptoauthlib/lib/hal/hal_linux_i2c_userspace.c | 12381 | `45f0f446a83dbb8fe068cfa31e01a42b53309c3f4eb61c156740d02a920a6926` | 0 |
| external/cryptoauthlib/lib/hal/hal_linux_i2c_userspace.h | 1764 | `92f271c142f48a5c19f81c88083f1eeaa9cc8d6fc200641dc76e86194dff65fa` | 0 |
| external/cryptoauthlib/lib/hal/hal_linux_spi_userspace.c | 9828 | `7ddfedf9487031496afeb17f24475dd59c12c12d86138b880ace50165fb130d3` | 0 |
| external/cryptoauthlib/lib/hal/hal_linux_spi_userspace.h | 1790 | `0307866a7b5de9e3a38e9b1b22119a852cdc32143461b6d441db7cce33f3bd8b` | 0 |
| external/cryptoauthlib/lib/hal/hal_sam0_i2c_asf.c | 14048 | `29a1696595af9c62435dd8bb1d7f076f8660c9bbe98d676c9fcdab70a18d3a1e` | 0 |
| external/cryptoauthlib/lib/hal/hal_sam0_i2c_asf.h | 1755 | `52780a0a5eebea2dc7f8937614e19e32084a20077a007181f801ea1ede64422c` | 0 |
| external/cryptoauthlib/lib/hal/hal_sam_i2c_asf.c | 13812 | `5986590e8bc60f64b3d825f1efdc8f5b3f874c188fee6195c040575daffd3b9c` | 0 |
| external/cryptoauthlib/lib/hal/hal_sam_i2c_asf.h | 1984 | `b335f7a4430bb97aeea42d1c6cc49c4676a83088261be14788292bc98d98b725` | 0 |
| external/cryptoauthlib/lib/hal/hal_sam_timer_asf.c | 2422 | `4a6a9a8a83be4f99e4f5df44470fc1b187c5cd2c8d8afd2fd123da3fb7bcefd7` | 0 |
| external/cryptoauthlib/lib/hal/hal_spi_harmony.c | 10580 | `d44bc8504b19e1cdcaa20fcc270c391d790d0ffdc6ce4712989a599640a17212` | 0 |
| external/cryptoauthlib/lib/hal/hal_swi_uart.c | 17208 | `ed7474bba42e374d06d1626fdf363313e841cefec98cddad922b9168e89f7393` | 0 |
| external/cryptoauthlib/lib/hal/hal_swi_uart.h | 2305 | `f953ec28677bef82c4428328c78e18fdca9455c0deb62f856ec78684cc5c7b28` | 0 |
| external/cryptoauthlib/lib/hal/hal_timer_start.c | 2408 | `9cafec72d0291552aa3a86c619d10641961c066263156f3f8cc30497ac4ffccb` | 0 |
| external/cryptoauthlib/lib/hal/hal_uc3_i2c_asf.c | 14682 | `19cf7396599d3deef903e3920af64c6585b8e6f664f54b8ca8680c9238739e0a` | 0 |
| external/cryptoauthlib/lib/hal/hal_uc3_i2c_asf.h | 2108 | `8ef0df9c3ff24b735bd500863cf12f8ee361d0437e8449cbe1249ac88493f6d8` | 0 |
| external/cryptoauthlib/lib/hal/hal_uc3_timer_asf.c | 2490 | `fdc3693c67a7c11dbdde051554b745c9d4f98fc58a904e966f95090a0f3aea12` | 0 |
| external/cryptoauthlib/lib/hal/hal_windows.c | 4420 | `d0ba1a98dd1d985dc5b0cbb94b5c72867443853db8608f90b55e4292733c2538` | 0 |
| external/cryptoauthlib/lib/hal/kit_phy.h | 2013 | `b1c095ca9d45279fca11db28b230908829f84cf99fad115f57c69b5239f4c438` | 0 |
| external/cryptoauthlib/lib/hal/kit_protocol.c | 19206 | `01461be8ea78c36e5f3a03132b4c6a837f12891fdaaff8aca13bf9c4d915a5ec` | 0 |
| external/cryptoauthlib/lib/hal/kit_protocol.h | 2530 | `40ce866c994e12f982f93c659bf35001baa3db35616bd0b7b27d920e2dac5a01` | 0 |
| external/cryptoauthlib/lib/hal/swi_uart_samd21_asf.c | 8578 | `58a4b311dae88fca6d0a8ab9d7a55b27120885229b3cc5a8a56e77d9d1334a58` | 0 |
| external/cryptoauthlib/lib/hal/swi_uart_samd21_asf.h | 3101 | `0278f828afb343edf034d1126d3fe7e3648023c6d945dd397b11b6bac33cb264` | 0 |
| external/cryptoauthlib/lib/hal/swi_uart_start.c | 7289 | `94bbca7da6cdd17f48e6bb9d77400e6b8fc07d1529e8887e8603c759651690a4` | 0 |
| external/cryptoauthlib/lib/hal/swi_uart_start.h | 2928 | `fb931c1211ea9da17384961ed2d7f2623a77f7be40ade0a4081024d38fad0385` | 0 |
| external/cryptoauthlib/lib/host/atca_host.c | 51312 | `192be7ba2b6e97f849d2e4bcb3c312b34bd8741599166890ab543219121b747b` | 0 |
| external/cryptoauthlib/lib/host/atca_host.h | 21629 | `24128a71c25ff78e44febbe6c686cc49e77798aac12b05a0dd8da2d6f4becfbe` | 0 |
| external/cryptoauthlib/lib/jwt/atca_jwt.c | 10008 | `e4c73e6243b26c748e9a74c2e8d468096cb952d652d9740f5b1e2a3c5da01612` | 0 |
| external/cryptoauthlib/lib/jwt/atca_jwt.h | 2339 | `337cc8eee0e4bd9c21d40f4029fc9b9758861e033610e49d45e9c78bd0956e22` | 0 |
| external/cryptoauthlib/lib/mbedtls/atca_mbedtls_ecdh.c | 4676 | `7b02184224a8fd6ac79b51f40f2718d73e00cf0ca367b356d635c6552a01be64` | 0 |
| external/cryptoauthlib/lib/mbedtls/atca_mbedtls_ecdsa.c | 4106 | `bc7452fc887862b6d8c30b65b06786f34818f69016d7921df4d183bb8edd8e6c` | 0 |
| external/cryptoauthlib/lib/mbedtls/atca_mbedtls_wrap.c | 32586 | `e5352695b155b49d60ba7266be6cefbe8455ff3484126fcf35ec35cac34b0ef4` | 0 |
| external/cryptoauthlib/lib/mbedtls/atca_mbedtls_wrap.h | 2499 | `c5feaaa7e3154d8b70ef4d39c5eb95fc5a746dd8826c00e48def9b80dcfdb2f3` | 0 |
| external/cryptoauthlib/lib/openssl/atca_openssl_interface.c | 24449 | `59d86ea0cebf67d5792e4a02cd8c3245b3bedfbf5706aaff1b855a4225ad75a7` | 0 |
| external/cryptoauthlib/lib/pkcs11/cryptoki.h | 4025 | `832a50660b1f6c31c502044917bf228ad82c014460bbeaa069d3b7715b491309` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11.h | 8007 | `4d6b1d0deb87f238a8657cffafc21bfa6fa495584474ec32d683e830b2be6a1d` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_attrib.c | 5205 | `14e49b5d5319bc6912a76f31147107a61091deb9eb28556409fdc8fca0b29795` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_attrib.h | 2193 | `d4877ab759e181f20a1dd1d5e7e462fc12e1ad81e1cb76687585c5c7d6e66666` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_cert.c | 27802 | `037c20ce13e40352b41dfaed3be564d29e067d662be5bb93a642d38a8d19a342` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_cert.h | 1916 | `4dc40ab96a3aefdf44259d8e3f2d3ca0bb89c771f8a818456160602897c7872a` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_config.c | 23577 | `26877e33fcd307dc95e7bf6b2cd50427aee373fb53d640cdf5764b89155b6d86` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_debug.c | 10836 | `76d11cc6f191beaddefbb6a87778ffbd84d47c3a52d49c0081ceeb2a61ee3c9c` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_debug.h | 2328 | `caee1d1b40c42fd9f62bb00c16ed2ad41bfc54cf65b6d6538c38db78c8a2af25` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_digest.c | 4277 | `bf6aa073112025d18b0770310bb55b2e8d9af39d0abacd685581913b2e17e347` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_digest.h | 1867 | `eef454bb5d1915216c64f8b0b4073e262f286fda13c5405c6ae96308e3c7a4d9` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_find.c | 12527 | `ef7222b702be6113c90eae1146f1b55ae3943977948f2cb8ec2f6d5b9109ae89` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_find.h | 1898 | `6d1f29d3cac5555c20daf441aa8781c7b22b55ee728ab8d6b78edd6396c1c73d` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_info.c | 2848 | `28176eb34f062b13f02dcd11aa3541be93f6e3550c6129ffa384e5cc07c86b67` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_info.h | 1512 | `737388ab3ea314fb25424964a06e10c90f488c23eeb9564e687a4b6a99cd4ded` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_init.c | 8397 | `66f8a6d62aa003cb28ad6f00d48625e44bf3a2daae4bb7fb537647892dfa7aac` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_init.h | 2218 | `cb8cfe7c01ea22c60dc4637dcbade4aacce5da93931d13777a0ec899877790ed` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_key.c | 44050 | `90f5684d266788ebfb04feb7b887139cb38f3ced88464bc9e49dae54cff7e642` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_key.h | 2514 | `89afd86e229a83027cc64354c5183750c3e98c974333de23b863b0d57892a241` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_main.c | 26795 | `611e4afb07aa3a67bd41d573a86c51b73576ca95bbf00051b3a655ac2daf925d` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_mech.c | 16944 | `b1caee30981af17aab2b43efc98fde99aad6015e94137b71cc63308df13ff537` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_mech.h | 1646 | `39ed9021ed937542ccae4a62a5603a6e6dae603b058fe15bb5f1ba43c26f2e14` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_object.c | 15862 | `4a054140f9f97536bf60f52cdbf1f3a5a199f9b9123de9505fa9b96f24a3b157` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_object.h | 4022 | `6246f5fd54f9e5c3f8bd6bf616fa55f4b21acc0a476d14ea2c6ffa347b27003b` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_os.c | 2567 | `c7cfca5c9e72d02aaeacb251d6d2373c026d11dfc619f3d1d93a91079de90200` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_os.h | 1683 | `46c6282de15c3ae9257cb71b3b6b715578f324c5f89900fa8b9486722437103c` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_session.c | 14352 | `2be1cf4c0d6b284711b19e3cee2bae803aff344c395fa7d838c0d17e0d9a3e75` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_session.h | 2843 | `60084f9ad5069272223277deaa7d4150daa8a666f31d6de076bae406346fdc58` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_signature.c | 7402 | `2ca5a72d428158653964b3f43595b95598ad3bd9b20218d4e643b0f9864b652a` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_signature.h | 2428 | `7871fd22ae08b8c21235fbfe49a7287c0301ce3ada615f9116cf5465e01a43d9` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_slot.c | 11468 | `6ea2778e98b261a73cd4ac6f4d9e78e8ebbd81a18aeccec59b09a3c35fdac66c` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_slot.h | 2402 | `282614aa6a611ee0d495f2d4e04ac3a1d3be4bb774bb38463994ef1f0244d04d` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_token.c | 19567 | `41211cb282065f42b40bb3e8c70490dc13253912a4fe4762a9a9475e369dc04d` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_token.h | 2357 | `dc1727ad53dfaeacd475f89e490473feafceb776ca7456958a242dd259e48ee4` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_util.c | 2592 | `384d4db087605cc3f04043a0fd4af05505c4afc232e652efb101a136fdfd9e28` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11_util.h | 1672 | `c0c2de6af3612688fa7f232b5c74b47eafe61fa6a29e3db047b64886c4920f89` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11f.h | 27386 | `69ae90423046bc74d6bc4fa81c7a93dd9daee35b988dfca88a5b875f4b416631` | 0 |
| external/cryptoauthlib/lib/pkcs11/pkcs11t.h | 72149 | `f30b9254acb8b1592f62a0f101432b381ac530716ba48ad7fb2c24b5cc3679f8` | 0 |
| external/cryptoauthlib/lib/wolfssl/atca_wolfssl_interface.c | 10099 | `093a1f68d4aff61717680b1065f9ea1a9465a33478fa4decd951c351d2dcd7c7` | 0 |
| external/cryptoauthlib/python/cryptoauthlib/__init__.py | 1352 | `40fb2a9e9f2a9835ee72854060ea00f78012da0d63155ab90527dd4a52f80af9` | 0 |
| external/cryptoauthlib/python/cryptoauthlib/atcab.py | 114570 | `0b92b5429170956ee3b25c3dcecc05f822715a44b5f6d1b48e06e9863c18d1b9` | 0 |
| external/cryptoauthlib/python/cryptoauthlib/atcacert.py | 27170 | `17bca2af987ea156db0f0a46e8d7069915efa3e7f8f9f37ab74a6ab63b2eb359` | 0 |
| external/cryptoauthlib/python/cryptoauthlib/atcaenum.py | 1004 | `d3317de13e3ea2916df82ca8676f8dbbc9e750607d1689f07f790a30e9963fdd` | 0 |
| external/cryptoauthlib/python/cryptoauthlib/atjwt.py | 4082 | `b28b739ecce2f085ad0c234005f0553a7e0b8c86259f4b1621956ec96257d2f2` | 0 |
| external/cryptoauthlib/python/cryptoauthlib/device.py | 8243 | `21d6d279d890bdc5c1ce2d49e2d6dbab84f2be9a97cd928710eef4ed4c4fcdc2` | 0 |
| external/cryptoauthlib/python/cryptoauthlib/exceptions.py | 4679 | `be356526d4db995abe6ea2b5add82931d0df1359c4adeb60ad0e51c991062af7` | 0 |
| external/cryptoauthlib/python/cryptoauthlib/iface.py | 5610 | `acd167417a54c6184772d45c3563804f1de0b72f612fa5465a80efcba2e4d485` | 0 |
| external/cryptoauthlib/python/cryptoauthlib/library.py | 8521 | `86289d795b378c255c85d77fd2dea9977e1462cb6ed4868cd83faa64add5611b` | 0 |
| external/cryptoauthlib/python/cryptoauthlib/sha206_api.py | 11289 | `070b0dbafa75c9c7ab4966d1be314111e8e6b432b2a0c1b6522352438d233263` | 0 |
| external/cryptoauthlib/python/cryptoauthlib/status.py | 6743 | `41344e72bb7f16616e7bed1c61598f0dc4c673835c12b82e5e4ce8ae9bc0875d` | 0 |
| external/cryptoauthlib/python/cryptoauthlib/tng.py | 10283 | `bddcf0eab7817600b12bac69f986212176299fb9d1cf52dc90a2fba2bb644242` | 0 |
| external/cryptoauthlib/python/setup.py | 8396 | `b79e2c2b9b52dce089ce97767fa1c444a872329a0a6b3ac52942a7fc0349949d` | 0 |
| external/cryptoauthlib/third_party/hidapi/hidapi/hidapi.h | 13870 | `113efe421189dfefd6b7946f1605b1eaabca70d79deb87e58d5ca1a8922c3011` | 0 |
| external/cryptoauthlib/third_party/hidapi/libusb/hid.c | 40667 | `c1c9a663237a5360ee0da2087bf4c4cd655fd4d9c2b8db464ff53b966f5157e1` | 0 |
| external/cryptoauthlib/third_party/hidapi/linux/hid.c | 19857 | `b712f3a6ab4005e3bc9ab67155b078a6c958f8f09f42cc69680dfd87b21f63ed` | 0 |
| external/cryptoauthlib/third_party/hidapi/mac/hid.c | 29609 | `24618c9712cbfcf5394c84378cb31de97404ae0e41bff953a7026ba0edf25b35` | 0 |
| external/cryptoauthlib/third_party/hidapi/windows/hid.c | 25457 | `cb314715fa194ce86b888a6dcc7ac1e9e596e4e6991352fa788257fd1bd7a7a1` | 0 |
| external/cryptoauthlib/third_party/unity/unity.c | 65366 | `d7a7255e0fc01418a412d01780aa69c10c64fe03eebfce0e8e2be1144c5959c8` | 0 |
| external/cryptoauthlib/third_party/unity/unity.h | 89027 | `7c8da363b67a7e37cd1052baf2b7043a702c36772d34c81992666454c1357e3f` | 0 |
| external/cryptoauthlib/third_party/unity/unity_fixture.c | 8392 | `090875bd5b4d55966fdd6f9d984aa9883924a395d1a56a78ccbf9885e058a643` | 0 |
| external/cryptoauthlib/third_party/unity/unity_fixture.h | 3220 | `73854da3d615a041ab114be64bb98debfa8b186ac9741682f3de4cabc153100b` | 0 |
| external/cryptoauthlib/third_party/unity/unity_fixture_internals.h | 1476 | `adf665b853438b5e35ffc72e6d0f1bd404a09188fbd4fc7c64c2eb30b25781ea` | 0 |
| external/cryptoauthlib/third_party/unity/unity_internals.h | 86767 | `c97938da35602ea0759fdbe2bbae9464fc374190584df4e217cb4493745bb92c` | 0 |
| external/cryptoauthlib/third_party/unity/unity_memory.c | 4865 | `7bc202de8e950466f713b2c3918beb824a10d33cd7df43058dd4676573fc2645` | 0 |
| external/cryptoauthlib/third_party/unity/unity_memory.h | 1980 | `85ea1b5fa55bd59f03901fad4272a938a33696d9f0821d085ba6fc5463fb391b` | 0 |
| external/cryptoauthlib/third_party/unity/unity_to_junit.py | 5939 | `0743f26b5ae67af204981293337f9cc9a8cb46c90aaa3f46f31fd9658ab65990` | 0 |
| external/embedded-swd/dap.c | 12150 | `fa5957cf285a88068a40cea0f7ccd82185d5f62e840ffa8d8ec2963071c8e2a0` | 0 |
| external/embedded-swd/dap.h | 2529 | `c9caf8a0d8c293d6d4ae8413680061c407b6de0c188f1c942ba85190713bac0d` | 0 |
| external/embedded-swd/dap_config.h | 4040 | `c884d6e8418634980324b354e558cc8708063902c695fd7bdffcf21cd4247f9b` | 0 |
| external/embedded-swd/dap_target.c | 3219 | `33bed9cd1c968b17a50c5eab41c51b908eaab8501bbd3b1dc1d1035ea1cf8e05` | 0 |
| external/embedded-swd/main.c | 5566 | `5b525ade80cda064547da403bab33088091069d557fadb951f15b2beaa6f0bdd` | 0 |
| external/embedded-swd/raspberry-pi/dap.c | 10537 | `1af13298edba706a77639fcda65dee669b7571773e5a21c16a3c638df41ac065` | 0 |
| external/embedded-swd/raspberry-pi/dap.h | 2572 | `fccdb45752ef643a8a6a26e6240abe4f55ca4538c627592590c42ded96d4e503` | 0 |
| external/embedded-swd/raspberry-pi/dap_config.h | 3981 | `d83687a623aa46793496bf37054f297c821bc1e1d9844d3ac7932f6a7ef5562c` | 0 |
| external/embedded-swd/raspberry-pi/dap_target.c | 5095 | `3d17629e6fb9250628ef47e04b49c690c5b2ca60739e9b69a3984f1e1bdf7933` | 0 |
| external/embedded-swd/raspberry-pi/hal_gpio.h | 7121 | `6248f2a07feca6ff5fe6d8005a44de40192217f5a0b7242f248bce1fff47ed75` | 0 |
| external/embedded-swd/raspberry-pi/main.c | 6122 | `a388df9fa00862fbcdc50e2cc4cda54bea5a93460a5543b7203a3c5425b5ef08` | 0 |
| external/embedded-swd/swd_hal_gpio.h | 5149 | `db63582c8a163d01a7a5b23543ec2854ffc224e85e11d85e3d6964b3c94b36a3` | 0 |
| external/lvgl/docs/add_translation.py | 1209 | `4f7f3ea87cae36fbb2e51bb149be6fb46c9f50bad5ae94b1679ca71fa79a7d30` | 0 |
| external/lvgl/docs/announce.py | 3836 | `d498243f64e94469de0f5114250cb98b3d9d45eedd41585471a972083d821b16` | 0 |
| external/lvgl/docs/api_doc_builder.py | 35433 | `01460953b7e211e20950de5c3629f93f7fc8e0dc09d58518d1144290e2b6f59e` | 0 |
| external/lvgl/docs/build.py | 32744 | `f4731d969f05e2b5f1334136e095c131ad1823bff08da687d9d361462cb50853` | 0 |
| external/lvgl/docs/config_builder.py | 2107 | `de13b0e12b73a739b211de964460bf5b9a05ad7b6f759b6743356bd14476bd6d` | 0 |
| external/lvgl/docs/doxygen_config.py | 17842 | `3fd06d11c47f894e0de5e56ca2b6f9240f3777211af077c6ff9a7f583abbf26b` | 0 |
| external/lvgl/docs/doxygen_xml.py | 60891 | `b4c91f0e0c3a6eb920df70e36e440e8223194592ed2badcb09e77a3e32d87ba2` | 0 |
| external/lvgl/docs/example_list.py | 3762 | `a943490a0bbeb7b06513cdf200eb178a2c1708ae071892897ca7b33d1c52d281` | 0 |
| external/lvgl/docs/requirements.txt | 331 | `6bf9b19c3da97d1d1036ecad16f9cfb18b72220514d13ad78b0cbb39cc5d70d1` | 0 |
| external/lvgl/docs/src/_ext/link_roles.py | 2146 | `fbc140462fecce7862f04edceed96a9e6e59265ef2bcaaa617cc7e1f54907fbe` | 0 |
| external/lvgl/docs/src/_ext/lv_example.py | 5651 | `02f1180eb189d48b44497ed6b819ad388414576552d40c6ee35b379fd6e8c817` | 0 |
| external/lvgl/docs/src/_static/jquery.js | 89501 | `ff1523fb7389539c84c65aba19260648793bb4f5e29329d2ee8804bc37a3fe6e` | 0 |
| external/lvgl/docs/src/_static/js/custom.js | 13577 | `3234d7e597bf5c95c59122aa89849afab6d6a365c2c5795f0fc916d1c440584c` | 0 |
| external/lvgl/docs/src/_static/js/include_html.js | 999 | `67002468f527c257a6bc2550bc8c792fe097b5df05f709f9c7fa7fdf337600a5` | 0 |
| external/lvgl/docs/src/conf.py | 38876 | `f7ff853b3f5566b3d017db44533e2112d514e0869ceff0896c8fa3e38731571c` | 0 |
| external/lvgl/docs/src/details/main-modules/indev/groups.rst | 3883 | `b9765d511013b2ff991168636c450efecea5268180421221256cb99028be20f8` | 0 |
| external/lvgl/docs/src/lvgl_version.py | 1695 | `93c4f7ea0beb6b44d4d77e18bfe8d60f80dbf1c79362d636b5fdf69c32fbcc61` | 0 |
| external/lvgl/env_support/cmsis-pack/lv_conf_cmsis.h | 47770 | `4e6120b2b5148a24b104ad356be872cc9360145577a077e1024fde2516a09c59` | 0 |
| external/lvgl/env_support/pikascript/pika_lv_point_t.c | 376 | `85d246f40965bafbbcb48bf36c544bd85ff82b94cfbb4340c112b4b8f7bdd19b` | 0 |
| external/lvgl/env_support/pikascript/pika_lv_timer_t.c | 1395 | `4237a13e337846c3c8690d27098b65cc0390732da614394d28cdae97b7f21061` | 0 |
| external/lvgl/env_support/pikascript/pika_lv_wegit.c | 12866 | `56941aed303d49db2a722ab443125ed3c1d10ac8f8180c2f3cf6129f2fb23727` | 0 |
| external/lvgl/env_support/pikascript/pika_lvgl.c | 8617 | `1fde6d4e5d8c6cd930a55b6266242b77a159e93ad9b77426de1dd8d11e9721d9` | 0 |
| external/lvgl/env_support/pikascript/pika_lvgl_indev_t.c | 459 | `f21c09c63b5475ba768d7b25d5d34b0c6c0da557c50d00907d4444db800bb4e0` | 0 |
| external/lvgl/env_support/pikascript/pika_lvgl_lv_event.c | 634 | `25ac679fa36c0393379d128c7985be6310c4781694791717fb0b1e5532f28090` | 0 |
| external/lvgl/env_support/pikascript/pika_lvgl_lv_obj.c | 3756 | `a9788269f563d2b228fc7d97e3518f77d682a47b97069f3757c5afc9219f3270` | 0 |
| external/lvgl/env_support/pikascript/pika_lvgl_lv_style_t.c | 2283 | `5f2c4adabae75e3045a518ed0bdfd49d4beb8afa6f586d3bef1579db08d9d3d2` | 0 |
| external/lvgl/env_support/rt-thread/lv_rt_thread_conf.h | 1646 | `8cad8d615b627e27a7d4ab176fedb686d24fccdb54b27409314fba0a9d63b2b7` | 0 |
| external/lvgl/env_support/rt-thread/lv_rt_thread_port.c | 2369 | `098718c060699ff59c339f2beb269830c1d3c9a41045877a55d16a1408e51e53` | 0 |
| external/lvgl/env_support/rt-thread/squareline/lv_ui_entry.c | 327 | `d9652420881c304d9ec81667af9aa7a7608263c5733e39e8c35e19cc62aee380` | 0 |
| external/lvgl/env_support/rt-thread/squareline/ui/lvgl/lvgl.h | 323 | `c946643df67fa07b5b170d7bb04321671ef839347e3fbb4efa2571327fcfaf66` | 0 |
| external/lvgl/libs/nema_gfx/include/build_version.h | 56 | `8e2782c46b5d13eface3d33395cffea72b5c46ac4c8a4ff236f4ffbb7a40035f` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_blender.h | 8202 | `5785a5bd1ba1567c35f305f755ca6cc90c50b46cfd989d0e3b141e07f68174ea` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_cmdlist.h | 6196 | `0a2076f182dceb99c15b7780be7a0cccb10ead829de0b8632df4ab0c9594be15` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_core.h | 1780 | `74312d6770b3a8becb5b7dcbd1f4bc729a2d8c0129b9ef6a5018ac6ee3b20f5b` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_easing.h | 10260 | `a499ed663b981e36b2de1fbd896ef9a7177e6a4fa178b2a0576b9001d6c8eae2` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_error.h | 3402 | `42934847c93dbef5b2177a63d6d929790c8a384af0a4c3dca49b700120b37c18` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_font.h | 7084 | `7a1a0c63b09abc26e4dce43ebf567d30b4dfb97707353982e110f12ce2a4c03b` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_graphics.h | 37346 | `6a8d24edd082e50684518528a7aa40fb69bcc15709ee3902526a28a77f725aac` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_hal.h | 5556 | `752ec40cd2f581c191ab531a88cc8c8064f9948a131375f8c3c79959e7d35265` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_interpolators.h | 5484 | `11755946b9f00e63819a0cc43a569334e4b8d1d834f15e2e9368d206ebd36f42` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_math.h | 7231 | `8d105b7e03ed0f619b50619e9d88838fb9737f98909865baa3a7555aab92b930` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_matrix3x3.h | 6688 | `9d37d476ff4bdc96e06fdeedcf7ed435220538fa0219f970d9547f993af618fb` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_matrix4x4.h | 8405 | `495ef5ca0c19bb2ab826a1aae15865923052d267407f927563050ed02fd7ab8c` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_provisional.h | 5286 | `ad6cdd8afb24c6b4ee6aca896fafab4e125e73ab34cdfdfcb7b507db7894a54a` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_raster.h | 3624 | `f07b4d8da69424f9630ac4a275d6f2cc9a2c4dd8318f92dbc5ba59a716617036` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_sys_defs.h | 1740 | `793904b437eb61c8fb32a18a29e2aeccc5b3c66595bfd186745f06af89860eb6` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_transitions.h | 8600 | `c725eff5efa9a7e0fbf60992cbb161248ecfaf7bb4b091f6425da4c12d1655db` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_utils.h | 2033 | `1bcfa011a73eff0e979ed4353b720c5f5e020776ffabbccbb340aaedc9c4e809` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_version.h | 2399 | `a526b8831aa2157247975786aa2fda5a773171528a559f8f7984c261a9f3f6d6` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_vg.h | 10078 | `0e56276dc34882de944369d018f0085b943156a3b0133131afe29c4540eeb511` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_vg_context.h | 10407 | `685b22a4e235568047f942a4977aa8b913b27d948a3a7b0b98fbc13caaf6d832` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_vg_font.h | 10504 | `89e9ae0f91364b44e33def3e9b3b16a543513871085ebcb28af540e9058944d6` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_vg_paint.h | 8458 | `e0ca2a336b6a61cb462c8b6da1afda41ddb6acddfd812fd0caa13ed234815a0f` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_vg_path.h | 6810 | `ec6a4eab89c120c14cbd64b40b3565747fd8ad2831f8f46a111c728ffe826f86` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_vg_tsvg.h | 2047 | `fe43fcca248e5bbd78859de9471a0d86c0c7a0f1c65f5cea89f1cbcb0e536f83` | 0 |
| external/lvgl/libs/nema_gfx/include/nema_vg_version.h | 2430 | `713c8158b78339c7cf26d9da163239119d6f06830ef1ec52e17268766a831510` | 0 |
| external/lvgl/libs/nema_gfx/include/tsi_malloc.h | 2380 | `326c15b478813266fd73391bcae4003e05b7ea02db150f69a09877a7f6116db8` | 0 |
| external/lvgl/lv_conf_template.h | 51370 | `ac25beccf7ca971a52b761a4a20d68a37c65ad54fc52cb11e29e7e2a42f886df` | 0 |
| external/lvgl/lv_version.h | 248 | `9cf9add2c92c0f70b6a764766605a4f199d3885e5d3ed4e9dac32043bbfb0448` | 0 |
| external/lvgl/lvgl.h | 5942 | `9f421571d2fbeaee457e24f8aaa8a94bdc6e31e4202bf5e6a6223f343d211664` | 0 |
| external/lvgl/lvgl_private.h | 4639 | `89c13853ed6f348f4d4c3e8737f50a5ea75dba79e569d667e2e938a2b55809c5` | 0 |
| external/lvgl/scripts/LVGLImage.py | 49858 | `cf02850de3b4b8ae89f8ae5a52c4d682cc6efac4d4e9d61d94681e2710af4ee8` | 0 |
| external/lvgl/scripts/built_in_font/built_in_font_gen.py | 2465 | `e06f0e0feef35ea7343ce0b99e956f0827f3509ed65c59ce0150a453050198cb` | 0 |
| external/lvgl/scripts/built_in_font/generate_all.py | 11561 | `179af7094ac7ebf75c0af9f89f25eae129860fd58e9f196b3ad797a92dc792f9` | 0 |
| external/lvgl/scripts/code-format.py | 1943 | `ce8739ccdf825976d3154d5d45e9d2c3caa2c476c328c1c0a0a22cfb80b68534` | 0 |
| external/lvgl/scripts/filetohex.py | 343 | `a8ab114103add8516f973982e0ad21258b04564c49467fd0d1bfbe2ee217f5ae` | 0 |
| external/lvgl/scripts/font_license_verify.py | 3877 | `66ec4c66eac7af95e5e76d79c5a06a45f4cf1b49e179f6bf9eb4379a429da00f` | 0 |
| external/lvgl/scripts/gdb/gdbinit.py | 315 | `399b35fcfb4167b03cde418fae1936ee1527f4551408279886d98fd08b56ee5f` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/__init__.py | 269 | `2d686809021771dad9ade8ee285fb1f4b42cd210ff899954657a8efe3e7b1a53` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/cmds/__init__.py | 478 | `4cc6b5ad9a60a6007785fa30f1ed201f8ff90ef698c6fcd2fe0059e793b09b7d` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/cmds/core/__init__.py | 58 | `0ebecc840b368a9816d77c8fa5e981c6ce23f1af1f7702c3c70b662ef7bcc8f1` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/cmds/core/lv_obj.py | 1796 | `ea9aeec2c7c46312d8be3690c6ecdaf2ac4005c5ba71c85a61a387945065e455` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/cmds/debugger.py | 2082 | `39bc0893cb38c9f3fff8d7128db6b61065484ff8da59af61cb472ffe205db9bd` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/cmds/display/__init__.py | 76 | `ab4dfed12aadf9cb10e44489e2ed6c4cccbf93fc90efa98d6a6c3ca55b25b71c` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/cmds/display/lv_display.py | 1579 | `4dd3ac679127c4ac30eb6cd860880767f2283b4450a0d24373abaac0baea3640` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/cmds/draw/__init__.py | 69 | `c12317334c5e4574899777012a2d5f0dc668d8946007a9fc2a49385352689cbd` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/cmds/draw/lv_draw.py | 1681 | `d8743313be0decf6aaceda2dae0e83046fa0ce218ab0412eb1c1730f24e7abbe` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/cmds/misc/__init__.py | 64 | `261955d7b21b56dedb5fb66ddfd5858dab1c0d93b29319f945485a5e206a257f` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/cmds/misc/lv_style.py | 1035 | `8d8901b2543109f1c8f960707b129796a203874948015df0143f03512815fec6` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/lvgl/__init__.py | 294 | `2c69acdac1dcd135b60a45bd71fc044230e1ac0834cfa03d01d767f0bb044287` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/lvgl/core/__init__.py | 146 | `8c5ab80798228e16b76da4793c5d3a880407d354fc8f8fe68349291e623901ab` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/lvgl/core/lv_global.py | 2854 | `18501d5634fe88f6618336903a7e0c4b774440cf9d505d46e6e04cd8e6b31c10` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/lvgl/core/lv_obj.py | 1843 | `d388f5c9c2d2fcd77e0d3a5478316ab7b046a3e09145cceb73d472611a32635e` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/lvgl/display/__init__.py | 66 | `48ae83d03ead74722706cf46eb5c26e2ecf64c43fb4431e84ce6ecdb26224d03` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/lvgl/display/lv_display.py | 1277 | `2d1e5c6dec9ad913ed347594e2df80450a12de62eb466cc9f398d883612fe3f2` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/lvgl/draw/__init__.py | 67 | `84c5710ab20061963d9a1d7587b05b72d498e93709a6cdd710e28cbf9831e01d` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/lvgl/draw/lv_draw.py | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/lvgl/draw/lv_draw_buf.py | 6962 | `4e9bbf8017264c1ab71710e79777563af54bb85bd2e597c6250635b8cc8f182e` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/lvgl/misc/__init__.py | 116 | `f97667f7e5c3abd728cd10fc3ed2ea4f4bcdca175b2f74642da807baa64041a1` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/lvgl/misc/lv_ll.py | 1473 | `f8fcc1bd245b87ca41aab46a1c593360b685dc7399f62f4b2089617c5e2aebcd` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/lvgl/misc/lv_style.py | 151 | `b8b065122fdba27d0956e13a67c75455cbc957884d175d4d1526f345a9abc900` | 0 |
| external/lvgl/scripts/gdb/lvglgdb/value.py | 1012 | `892533149356cc3ed86f937d829029e0f03424b7d53637560997d610d86341ef` | 0 |
| external/lvgl/scripts/gen_json/create_fake_lib_c.py | 19229 | `8cfb968793fca2875fdfc2f41aabdef98fb79042299906b82fd3b3bd42f19077` | 0 |
| external/lvgl/scripts/gen_json/gen_json.py | 10581 | `e67f8b5da262792b31788a5bf630ce71fd57dd6f882fbfab3280a777db8850a0` | 0 |
| external/lvgl/scripts/gen_json/get_sdl2.py | 1744 | `2423a34037dc9aa56e4ebf48a14cfb65199af9b52621746ecc167d1898efed19` | 0 |
| external/lvgl/scripts/gen_json/pycparser_monkeypatch.py | 47201 | `9119656fa48834288ce7a79b954f62575288ae2e1fad53affeaa44ee1da59a0d` | 0 |
| external/lvgl/scripts/gen_json/requirements.txt | 315 | `0b1bfaaeb328ee5660f6e28e1e02bc12f10adf409d039f44f6f40d74e575fad4` | 0 |
| external/lvgl/scripts/generate_cmake_variables.py | 4664 | `1d4670abf9b97ad30e2a05de1e3b1f3565311ff19779ca7068521f37374401cb` | 0 |
| external/lvgl/scripts/generate_lv_conf.py | 4263 | `6ff8548398f9a5ffc52b76c2cbcdfb4259e762828fe59cbd3dddfc0e2ea60a47` | 0 |
| external/lvgl/scripts/image_viewer.py | 802 | `d8e0a0cc296912bd29c1a355af27d489ea3e9e49921d6d51e7a1e475f08ffd64` | 0 |
| external/lvgl/scripts/jpg_to_sjpg.py | 3582 | `fc2d077a4445d6bd8d4aaf2b1f5329af3c388c063614580f6e08ad076ff308d8` | 0 |
| external/lvgl/scripts/kconfig.py | 12588 | `87f0c9f386f1e4904b4a153c8dfd5980c58c98422e508edb9af247151fa17ddd` | 0 |
| external/lvgl/scripts/kconfig_verify.py | 1816 | `45ca26e71b63ef7d8d9eff6607a59dbbdf8723b12f5ab0aa8f4d692b6df2c029` | 0 |
| external/lvgl/scripts/lv_conf_internal_gen.py | 9318 | `13a3c4a22ddcd9b8be6442cc63573083149762231c2f27f299b672c18b856001` | 0 |
| external/lvgl/scripts/lv_templ_check.py | 5220 | `d6a483e378ddbf1da553b97a4ac6da25f5afc27b900d879f6379a8687825de55` | 0 |
| external/lvgl/scripts/perf/filter_docker_benchmark_logs.py | 4862 | `60797656e60f8432f5dd052995b6503e9c1456e735c4b125ec99fdc8471ade03` | 0 |
| external/lvgl/scripts/perf/serialize_results.py | 4312 | `5f10b30a1845addf747d6b8a0065810db89fcf8dea608139d752c4238090352d` | 0 |
| external/lvgl/scripts/preprocess_lv_conf_internal.py | 5676 | `b48746adc8b9690f67de9f8b4f92d6d6a13f88c1ab0736f40db4db4c72d792f8` | 0 |
| external/lvgl/scripts/properties.py | 7087 | `2378003c388907776544cd409bc4f124dbc70a01b3b21b0e2cdbcd2be49cb298` | 0 |
| external/lvgl/scripts/release_branch_updater.py | 13951 | `ee2fb8168740c20d8cbd8484d928c9b9637439e107ac28d3e08c53887d7a4e4a` | 0 |
| external/lvgl/scripts/style_api_gen.py | 38625 | `899725f6565c374383d65f81ec6aa4148271976f2d49528cb3334354907fa8ed` | 0 |
| external/lvgl/scripts/trace_filter.py | 1348 | `b92d69e103b6c76c7b8684f7e5c3d8c655c21aed80330b5965acab8b7610d1a0` | 0 |
| external/lvgl/scripts/update_version.py | 5796 | `68aff60460b00a4edeb3bbdd113d80a47e6ab1c1c7f21bfa6b0a3a47f2b983d2` | 0 |
| external/lvgl/src/core/lv_global.h | 7062 | `3101940e6d5930dda9f9a4e1a97b2cc2a6248637752e4559313b76a4f185b405` | 0 |
| external/lvgl/src/core/lv_group.c | 14144 | `9e41401ac5dd23fd359f21bdf740aee0d4fea16275568bd42383d88e30818e3f` | 0 |
| external/lvgl/src/core/lv_group.h | 6793 | `1187cb25d3c22f0d0e04b74e516a954f8581a146d3c3eeb3c7b3a4d4f11146cf` | 0 |
| external/lvgl/src/core/lv_group_private.h | 2026 | `efe339d1c3714017938309410d659a4ad1fe5f9fcb733d9d995aa082d53640b0` | 0 |
| external/lvgl/src/core/lv_obj.c | 39822 | `6d47497cf60fb6065d07a90ebe454d1ba10c50d21142b2544f9b26553404ed68` | 0 |
| external/lvgl/src/core/lv_obj.h | 21806 | `f1ea113fe1ba4429f490ef825d182933b577a4d79382fd60269268c3ecd98d37` | 0 |
| external/lvgl/src/core/lv_obj_class.c | 5888 | `5c33b982c91c13cd7a2baa26b5bb523af51f9c81ff18cd83c80828735eeb7e1f` | 0 |
| external/lvgl/src/core/lv_obj_class.h | 1789 | `51448cfa46f8b0b3031bf3552a031e5c07ce0db5caf4a5f65ffc73ae8d929f27` | 0 |
| external/lvgl/src/core/lv_obj_class_private.h | 1914 | `ee176e8c0abc4dc395dae7ff1cf0e46f7de04123a39810f7f093b343ffdc8453` | 0 |
| external/lvgl/src/core/lv_obj_draw.c | 16521 | `1afcb881e6e76eaa8b578087c72d7a1fa24bd62f6fb36a7f0e279038911be328` | 0 |
| external/lvgl/src/core/lv_obj_draw.h | 4981 | `46727969cf4c1b993aaa09cef54cc07daeecd7c17d7cf4df2e323f725070c731` | 0 |
| external/lvgl/src/core/lv_obj_draw_private.h | 867 | `6f6076a40e5e733aab92b5ac705c54b7f3e6b13a0b8d5a3daaf0471e83143550` | 0 |
| external/lvgl/src/core/lv_obj_event.c | 12927 | `da6526213686972b24922053926905f5a8808db0e5e01fa59c28af0140be4724` | 0 |
| external/lvgl/src/core/lv_obj_event.h | 7258 | `8c8bc14c50686689ef4deee0dd0a035f228c2b60f4940f567253723a6258897a` | 0 |
| external/lvgl/src/core/lv_obj_event_private.h | 1661 | `00ebd83bbb3cabc0a6b9d1e8cd459d2eeba968d12ba86bd88e547bac88a5f3fd` | 0 |
| external/lvgl/src/core/lv_obj_id_builtin.c | 2690 | `616756187ce046dc9b19ddd6654d564b77c5771b62357e54e044cb374d9f3f1a` | 0 |
| external/lvgl/src/core/lv_obj_pos.c | 41976 | `0ed16a104c71395e1165540bf24ee7b1658f6666ebf9019ad86a00c92b0726c1` | 0 |
| external/lvgl/src/core/lv_obj_pos.h | 19536 | `4f3e2b847c5cc6aa2965b0c59e77d13a98c1ba11638b2ec2d722fd9965f51b7f` | 0 |
| external/lvgl/src/core/lv_obj_private.h | 2571 | `8542b1490e64eb0e74591395ac0c913a56d19ec641dd1e487dd64dbbf0897be5` | 0 |
| external/lvgl/src/core/lv_obj_property.c | 11236 | `0ceb9072315c72eb508006d8f68ffcac1833bc8d0cfdb6da81ef1f4df183d905` | 0 |
| external/lvgl/src/core/lv_obj_property.h | 9208 | `eae9e5e513a16a105d23963967e20c1213b1941dd109dc78c000616e41737f39` | 0 |
| external/lvgl/src/core/lv_obj_scroll.c | 28233 | `16bf27aec253dfc711e3056c7ea09067c50dbb19afba92b536b0962e38f7e5e6` | 0 |
| external/lvgl/src/core/lv_obj_scroll.h | 11006 | `334b0ae0003d46c1984ea4a214bf35bfa011ae4cde46d3c6164279a7fd4e8014` | 0 |
| external/lvgl/src/core/lv_obj_scroll_private.h | 1061 | `621f784b8783cafaf7c4f9b31cbf488c0506479aa0e3496e031fe6cb65fdfcfa` | 0 |
| external/lvgl/src/core/lv_obj_style.c | 44128 | `1bb880078f512c3f914be452755b11b45c0d299fa83a81b5a7ef3d8a445f5642` | 0 |
| external/lvgl/src/core/lv_obj_style.h | 16144 | `3674ef17b8324b4f86b57185a8f49743c869888ff327cbb8499976072294750d` | 0 |
| external/lvgl/src/core/lv_obj_style_gen.c | 28941 | `8db2135e3494b13e0ad92fcbdee17899069ba5fa1603daefe317d107fa40150f` | 0 |
| external/lvgl/src/core/lv_obj_style_gen.h | 40131 | `a3f682bde495e18cdd00831c320e540461116d8c4c092b1103ea107b6f88dd91` | 0 |
| external/lvgl/src/core/lv_obj_style_private.h | 2029 | `bd8f841f501e1708105bf27472fcc1e2ea594dcc1dae7d36f06662bc5a996298` | 0 |
| external/lvgl/src/core/lv_obj_tree.c | 24638 | `ae99d2dd726d9e35594fcced3e6b2242db93d27d1ec25a22bf5b250631efafc2` | 0 |
| external/lvgl/src/core/lv_obj_tree.h | 11529 | `f9f97cb31b5c23881867078fbb56bd74846a0d085fbc9b2fc1593b91b5969e8c` | 0 |
| external/lvgl/src/core/lv_refr.c | 52497 | `7b3854c6d51995b85d23cc55207a3102206fbe3b5110e130e0e9533d0ebfbde5` | 0 |
| external/lvgl/src/core/lv_refr.h | 1660 | `a42e51c6c1f50187e96ff74033b59ef7e27fdd0680ffec06eb18d7418f850546` | 0 |
| external/lvgl/src/core/lv_refr_private.h | 1776 | `cb2a164ccab1b2888b665b979ac04055d660f061505cab73cb6b482d50ea4c3e` | 0 |
| external/lvgl/src/display/lv_display.c | 40448 | `178f673b4b72ea3b54f4a3d09897c815a893a4fc5f2572d8a007ccd087557b43` | 0 |
| external/lvgl/src/display/lv_display.h | 27397 | `3a5d42f1fdfce16e0a80a23e71ac85e4218820bf731c60d996882822b749d781` | 0 |
| external/lvgl/src/display/lv_display_private.h | 5741 | `8d52dda563b07a25fe85ba506bfe74bb036bb28118ef2e6323e8ec6b45dcef2c` | 0 |
| external/lvgl/src/draw/convert/helium/lv_draw_buf_convert_helium.c | 3768 | `26b44a4896eb19113c4e404472b455ba776d345fc6783a915ee2d8cd6853a5ca` | 0 |
| external/lvgl/src/draw/convert/helium/lv_draw_buf_convert_helium.h | 1388 | `2549a1126579992c29137fc6bf5ee62e1e7a91a745fac92e148b26bce23aa02b` | 0 |
| external/lvgl/src/draw/convert/lv_draw_buf_convert.c | 4300 | `fb946aa5069a5604f4efae7fab9b4d082b2a982a5da089cbe17eef894c703df3` | 0 |
| external/lvgl/src/draw/convert/lv_draw_buf_convert.h | 649 | `c04acd44fb3bd38ac8dacc589cf1bb673ccaffe79fad0a6b0e710b19629dd296` | 0 |
| external/lvgl/src/draw/convert/neon/lv_draw_buf_convert_neon.c | 3672 | `b5ed283aef2a677bb9cbd266e809922e83c8936255f441496abfa775acf5c239` | 0 |
| external/lvgl/src/draw/convert/neon/lv_draw_buf_convert_neon.h | 1365 | `954859a165ff94b681f265bbfc166adb4ce389f8fde9ccf4e11066c581566f33` | 0 |
| external/lvgl/src/draw/dma2d/lv_draw_dma2d.c | 12583 | `7c4e3d7293af2ea9294beaaacf769fa414092f469d4d19c69096c70552ee7ffb` | 0 |
| external/lvgl/src/draw/dma2d/lv_draw_dma2d.h | 785 | `7ba993a2007d5b9d9da637a8a5b61544c0c67944bdffe7e17c699b319d370eb0` | 0 |
| external/lvgl/src/draw/dma2d/lv_draw_dma2d_fill.c | 3830 | `5ace4bfcd3edb7c60beaf7f8f30552f65063bc92a7e8e78ec1f6fd8a4e483916` | 0 |
| external/lvgl/src/draw/dma2d/lv_draw_dma2d_img.c | 9915 | `76bb1b84d840ec7d8b58186859f45a3166b8b331a5ec4f9cc641a1b4b788b3a5` | 0 |
| external/lvgl/src/draw/dma2d/lv_draw_dma2d_private.h | 4211 | `11ecb03e114b5d1ff50223a59aed9da345caaedebc60d9a4d6f2f5cab81c5ae1` | 0 |
| external/lvgl/src/draw/espressif/ppa/lv_draw_ppa.c | 7850 | `0fd18ae3f2c51d98619b21ab345752382aa12905fee519a21f6376bea82a04b2` | 0 |
| external/lvgl/src/draw/espressif/ppa/lv_draw_ppa.h | 1082 | `12eef580b0b8d64e3affad72a6ffb31ef87969b290b5a5ca5b097f850c98d366` | 0 |
| external/lvgl/src/draw/espressif/ppa/lv_draw_ppa_buf.c | 1372 | `365ca9961a8910f0b13e0b4f0fb39b08be2fc0f4fd7b9c6419e4fc9a4256f437` | 0 |
| external/lvgl/src/draw/espressif/ppa/lv_draw_ppa_fill.c | 1333 | `584eeb197d7dd3477df356359dd81c410b0aef11132e1e5c266868daefad6e55` | 0 |
| external/lvgl/src/draw/espressif/ppa/lv_draw_ppa_img.c | 2514 | `3cbed4ccb45697d12a6cffc35d75feab8601302854c3e32ef338e67cee2d7b8a` | 0 |
| external/lvgl/src/draw/espressif/ppa/lv_draw_ppa_private.h | 4719 | `e529f5c343d5f94b64b2cfed83f729490e2fbe005f6fd2670587086cfa9ca7b4` | 0 |
| external/lvgl/src/draw/eve/lv_draw_eve.c | 4084 | `c9d256820f3efeb0733fed9c759ed21dd0f8013546e518c99d40e3603c633d2d` | 0 |
| external/lvgl/src/draw/eve/lv_draw_eve.h | 917 | `6fbfeb4fe2a13b61634a0c5888891d4015c4407b1dc05205a27cface94b7330a` | 0 |
| external/lvgl/src/draw/eve/lv_draw_eve_arc.c | 10566 | `098945c35a840f15f0d6cff3bc9f4f40188d120d3bb723b9511e248eab4ea9c2` | 0 |
| external/lvgl/src/draw/eve/lv_draw_eve_fill.c | 3574 | `853a06ea4e89abaa55a29e2cfff9677dcc5d14842f16a563f79a537df20db6da` | 0 |
| external/lvgl/src/draw/eve/lv_draw_eve_image.c | 9075 | `3431e9a6ffb50df7a1eec7bfc847c1f9297f8e0271f1c877f506f190774cd18a` | 0 |
| external/lvgl/src/draw/eve/lv_draw_eve_letter.c | 6942 | `1d6bb9f977b8f9ce1b3207fa4d7890c2e3a3a3e264370650da61ea5362e675cc` | 0 |
| external/lvgl/src/draw/eve/lv_draw_eve_line.c | 1631 | `0beecb6c6ba7a0c10ec0bea46c68f832bf03502e511405094ee37c703c555e8f` | 0 |
| external/lvgl/src/draw/eve/lv_draw_eve_private.h | 3249 | `ca72d04c60ea70d9d19d8a3d83dc3c387cf78df26dba56e5fd4ce3c2b79cdadc` | 0 |
| external/lvgl/src/draw/eve/lv_draw_eve_ram_g.c | 5916 | `b8da47a84075d348b0130029c07f7008a3ca0d480b3988e396c871ba08210d62` | 0 |
| external/lvgl/src/draw/eve/lv_draw_eve_ram_g.h | 823 | `ced2ec42b040c7a48316145db90e06c6a3464094f1e92561d46143403f413be6` | 0 |
| external/lvgl/src/draw/eve/lv_draw_eve_target.h | 2817 | `e3f199452fffb98edbdea94cc4f29ae1f7825daf7d9e63abe342e7905359eb9f` | 0 |
| external/lvgl/src/draw/eve/lv_draw_eve_triangle.c | 3334 | `aa4578bdbcd64b8facc891e6e22371789ea385adac51a2dc922f727960a9ce3b` | 0 |
| external/lvgl/src/draw/eve/lv_eve.c | 6657 | `1e584761376c4585ac569b35f34171a14257246c8a2abda5502ba2d7c96275de` | 0 |
| external/lvgl/src/draw/eve/lv_eve.h | 4787 | `2444ad1b0fe0a5ff9f1b959628498594077c169fe260ebc5b16cee6eb05a75d8` | 0 |
| external/lvgl/src/draw/lv_draw.c | 21952 | `c39fb2bcf23683ec0e84dbf042d79a6410959e83116da5dcd17d5874941df409` | 0 |
| external/lvgl/src/draw/lv_draw.h | 11851 | `ce774bd8650db80704ac6497857464be4da2f8488443d3c914a3ce933553113a` | 0 |
| external/lvgl/src/draw/lv_draw_3d.c | 1447 | `5d87908d026ab2e8cc736da11b92a61d2bed4403ad6b6400fc7aca24b4f58fa8` | 0 |
| external/lvgl/src/draw/lv_draw_3d.h | 1417 | `6bee682f396e70fb2d80dfc9b3ac139581a4fdde43cd9b5bb846c91af09bb854` | 0 |
| external/lvgl/src/draw/lv_draw_arc.c | 6661 | `1d82fa5144fc675285b7eae4e76142cd597d3c9fe5303593ae5e740a6a0bb09a` | 0 |
| external/lvgl/src/draw/lv_draw_arc.h | 2997 | `92f196095341ff18c7577ece941d0156e6c2a721bd26941803ab3b4cfc38832a` | 0 |
| external/lvgl/src/draw/lv_draw_buf.c | 21548 | `21ad8877fc3bd99bdcea9aa77383055fabb728cc39ef7c17f67d19b7f99c3671` | 0 |
| external/lvgl/src/draw/lv_draw_buf.h | 14726 | `933ab3b7b298480bbff21ae2fe7221df786d10fb29f2ac54e6443ad8998dcefe` | 0 |
| external/lvgl/src/draw/lv_draw_buf_private.h | 1067 | `01cbffca7f45dd65ffe329658491156ee5c1d43621ad9615e2d45d1eec043aa0` | 0 |
| external/lvgl/src/draw/lv_draw_image.c | 13581 | `3373652248781e086e6eeaaf012985de304367cd09741a5c17e94690d0f8d30a` | 0 |
| external/lvgl/src/draw/lv_draw_image.h | 5920 | `1bb2dc5db4b6d6d0948d31a7881545ff9f36c4d8ddb62a07d3086958dda7dc0e` | 0 |
| external/lvgl/src/draw/lv_draw_image_private.h | 2466 | `cd21588b7c5c20a25e3cf3cf7640a5a8b962f3a93d4d012682eb595fa8e9be9d` | 0 |
| external/lvgl/src/draw/lv_draw_label.c | 23656 | `70149624a5515f39b46e0a50155b487620dfa6b20225fa5a1511882327ed0008` | 0 |
| external/lvgl/src/draw/lv_draw_label.h | 8112 | `37b57eeae472aad4e4bbdb3386ddd5baa7f9abbec1f2520b449a2935cece1942` | 0 |
| external/lvgl/src/draw/lv_draw_label_private.h | 2031 | `2fc8b82558c99931ffb6f333e09e7c5eb8d2f3597905a2704b58317618c47175` | 0 |
| external/lvgl/src/draw/lv_draw_line.c | 1836 | `1985f06a7de6955d95303f3f10036934ee031d4e9e4766c4fee59744959c6016` | 0 |
| external/lvgl/src/draw/lv_draw_line.h | 2272 | `9301c854dc2b5de50c2a140cbec45f7dbd86a1b9da198d860765e1527526cb1b` | 0 |
| external/lvgl/src/draw/lv_draw_mask.c | 2160 | `311d4973746c83016adf97f445274736b6bac4a8c49541a9f6389b884656e723` | 0 |
| external/lvgl/src/draw/lv_draw_mask.h | 1281 | `d09a5b02620c8ad2d2ddfdcd5c6df1dbfdc2ced66841fa55f9bb64a920e41618` | 0 |
| external/lvgl/src/draw/lv_draw_mask_private.h | 964 | `0fae20393279d2bb329991c2a297dc912aa11c16881092c228d670550f4d6b1e` | 0 |
| external/lvgl/src/draw/lv_draw_private.h | 6592 | `e2b9f51c56b4b4728558257e504786e212548faffcc3e9cd56a503bdfd614b1c` | 0 |
| external/lvgl/src/draw/lv_draw_rect.c | 11959 | `8df5eeae23da8587bd1abca7c3aeb7c427c747be0c4bfa831ab4a7f1626ebca2` | 0 |
| external/lvgl/src/draw/lv_draw_rect.h | 6633 | `095f632dd4ae843336db0821b247b5d95df2667eea15d8712e8ca59bf51479de` | 0 |
| external/lvgl/src/draw/lv_draw_rect_private.h | 584 | `e7c2b4e419878a865c065cfaf00825c4c00d551657fb5d09b04f3943058f3478` | 0 |
| external/lvgl/src/draw/lv_draw_triangle.c | 2065 | `98715f7c24bf532702d36d6cc342b201aa6070b84d0c5b44dd5fe53fd7531c5d` | 0 |
| external/lvgl/src/draw/lv_draw_triangle.h | 1767 | `0da7fa16c0b675feb103e059b0d58bd53116992a131d47d43ef7ce6ef0f130e6` | 0 |
| external/lvgl/src/draw/lv_draw_triangle_private.h | 671 | `c920e5df472e2a018ef1da0b5a293d2f119b3c72e9017cdff44f8edab5dde3f4` | 0 |
| external/lvgl/src/draw/lv_draw_vector.c | 29698 | `a27ed7f84dc6a483147348655673fec01a35889a5279ec69b5a3bfbd8e3b254f` | 0 |
| external/lvgl/src/draw/lv_draw_vector.h | 22541 | `98b30ffa70fe02f2b7bebe7e808b99f34c0bf2d59c0aa208cf96b62f24628fc3` | 0 |
| external/lvgl/src/draw/lv_draw_vector_private.h | 3493 | `e8d3604efeba91926491cf296349605f80273bfedaf9a8a1eefce1c0883b67a6` | 0 |
| external/lvgl/src/draw/lv_image_decoder.c | 14622 | `8d001a4e4a024b9a3d247abd1fc7a31d1fc09f14d8a02807d5955508aa551a3c` | 0 |
| external/lvgl/src/draw/lv_image_decoder.h | 8498 | `cf8cb23198e97741d52771974ea7276fd2c79b59c425a020ed4dae9f45820b04` | 0 |
| external/lvgl/src/draw/lv_image_decoder_private.h | 3926 | `e3c20296ecf46c9741f1884aa89822889020dc35973695f864cf977291c5e0f3` | 0 |
| external/lvgl/src/draw/lv_image_dsc.h | 4564 | `f6c5b2290a39dd8906305a5d3340a20feafbd3ce99bd458bb0ab1d58f7f6bb96` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx.c | 13949 | `8a3f71ccd93e7f4cb397c3383971edaf4a2ce93a72c00608938640ff0bf07658` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx.h | 4043 | `f3ae2b3783e49b832cb8f4d9202a77d8fd371f8a46d96a20746c0627c7d57032` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx_arc.c | 3760 | `4d83f93dbd578159c8e181bb3abbfae81cff39aa9919c31c261a38803580b296` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx_border.c | 8501 | `9986854a223fce80112170d67e832dc1290a01d917b0c69827d42e772757b920` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx_fill.c | 7609 | `8005fcfa6bd5fafa1ce4a647a538f0378a7f0992428e3dbc3e040b8986874806` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx_img.c | 9118 | `bf4f5579334e5b58e9213d46d4fccab95556a1109c9b2976cd78133d8d2aaea4` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx_label.c | 33003 | `1ad6f9664e3cde141509a8e466b0e28c0cf6d464d084850c4843239d2a48fd71` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx_layer.c | 2123 | `b4c37d4af2dbfc864c0b903d681c98b9f29c9c26b310d338c0f89eae560873a3` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx_line.c | 3801 | `e082813e86c083cebc5d5dc189976e7921316588fae9f34deb43c23896055ed8` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx_stm32_hal.c | 5103 | `73cfa4bda569c8f6d71931fc55d53a113ae2d75eba8af0cd34ba89a35e6e445d` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx_triangle.c | 6818 | `50580187911ab6a6045c4b6018e9db271ffefb1d3a085e3695ec688f173877b6` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx_utils.c | 4538 | `b1f7036456c1a8fa7a706a33634225183f6d897fe392a0c438b2788b2650c87a` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx_utils.h | 3645 | `8d612cc41b5c8358a44e23abb9ad160c446ad4e55024a00a8d5097895795ab58` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_draw_nema_gfx_vector.c | 6101 | `0640d8ae6132c14d636b4a1781c037daa17964e0df37cf08ab06c565271e6e32` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_nema_gfx_path.c | 5036 | `998c95499a1f0161a51e80e52985adfc87db8ffd76d2f28a9dcf71e102aadee1` | 0 |
| external/lvgl/src/draw/nema_gfx/lv_nema_gfx_path.h | 2951 | `e8085d601c42c45a4293c6c699d2c0a3e0eb594abef303f0853b7eb7ccf16c4e` | 0 |
| external/lvgl/src/draw/nxp/g2d/lv_draw_buf_g2d.c | 2038 | `08652d22f1a267949f8c604262fddfc6e20786fd996c67efbeed75e1d84ed175` | 0 |
| external/lvgl/src/draw/nxp/g2d/lv_draw_g2d.c | 9266 | `afdc785d77336b03ab273f7fc8a19f28232c023d95ed2a76828a92a752d3750e` | 0 |
| external/lvgl/src/draw/nxp/g2d/lv_draw_g2d.h | 1172 | `23d2b49f0260b54312663e8ec09667f7170da1a724659b2ba9f101b56ba5069e` | 0 |
| external/lvgl/src/draw/nxp/g2d/lv_draw_g2d_fill.c | 5360 | `982971531a8be210e2f6d640435cc30c3321bdad2ff77c97d79b68965a70777f` | 0 |
| external/lvgl/src/draw/nxp/g2d/lv_draw_g2d_img.c | 10189 | `ead930179547172c88c336c8b0520f55b0c0b2c03b8b64e6f03b1d4a515166da` | 0 |
| external/lvgl/src/draw/nxp/g2d/lv_g2d_buf_map.c | 7480 | `5557e697ec6f9e53a9e50d6b9ca722f72d898eb3787a9173aa817010e22e4c30` | 0 |
| external/lvgl/src/draw/nxp/g2d/lv_g2d_buf_map.h | 1376 | `eeb9efdf194b8d2649c8434aa0899b475a2489883027a77405e3632183ec460a` | 0 |
| external/lvgl/src/draw/nxp/g2d/lv_g2d_utils.c | 4376 | `9c9cb49ad993ac40ea28f582e368d696ef3493c42bf94c6ea92d852a7b163d0d` | 0 |
| external/lvgl/src/draw/nxp/g2d/lv_g2d_utils.h | 1821 | `327e2a8610a407d612adfa3ffa2441e0f503f3bd49bfa873dc6f5d1c7eb4ef88` | 0 |
| external/lvgl/src/draw/nxp/pxp/lv_draw_buf_pxp.c | 2988 | `26a23284b6cef33c081baa32c09a641aa4ab5e21bea419acc86303941ed600d1` | 0 |
| external/lvgl/src/draw/nxp/pxp/lv_draw_pxp.c | 14308 | `1082a2cc04a32195f7709b245e4835e201781bc0685f532b83befe64e060430b` | 0 |
| external/lvgl/src/draw/nxp/pxp/lv_draw_pxp.h | 1667 | `59c57bc35e618145b7d90e1520fa35476d69be71956c77e3de924ebd6974b565` | 0 |
| external/lvgl/src/draw/nxp/pxp/lv_draw_pxp_fill.c | 4537 | `38e29397af24e8726c8a97b3becbddad6f15818be2f51902a691a7ead1ff5469` | 0 |
| external/lvgl/src/draw/nxp/pxp/lv_draw_pxp_img.c | 13109 | `9e5ecd83552171a84cdc75a615484e8720cebdf59b8216e9ebf27b3f29362b29` | 0 |
| external/lvgl/src/draw/nxp/pxp/lv_draw_pxp_layer.c | 4226 | `52747b09c518d0885e7ae4fa21104a796feffb70a8f1867aef5ca0e8b22d2ca2` | 0 |
| external/lvgl/src/draw/nxp/pxp/lv_pxp_cfg.c | 1756 | `3e6896af0328593ba3a8fac91906c0f044072ddcf9d1fd49f57d9e77fa0c1721` | 0 |
| external/lvgl/src/draw/nxp/pxp/lv_pxp_cfg.h | 1955 | `683f6ba650d4a8f019343089220c2c7960fe7b7c49147e2dd3f023bae9ecfbe7` | 0 |
| external/lvgl/src/draw/nxp/pxp/lv_pxp_osa.c | 3478 | `7e4f45345847abfbe6f41b08879bebb5eb78349e517d1fabde843171174b0590` | 0 |
| external/lvgl/src/draw/nxp/pxp/lv_pxp_osa.h | 983 | `498117629c6f40c98a99ac003f80030ac706d6c8da1f87b3e8fb6980332ef8cb` | 0 |
| external/lvgl/src/draw/nxp/pxp/lv_pxp_utils.c | 3794 | `626787a5ba5ad10201d7fd0113cf082c1bfda7c86a8c32794fc3c99493219ea5` | 0 |
| external/lvgl/src/draw/nxp/pxp/lv_pxp_utils.h | 1819 | `d3df2791035e240abfe184521162e18a36c9383bcb62b84932026fe9bc51e9d2` | 0 |
| external/lvgl/src/draw/opengles/lv_draw_opengles.c | 24674 | `ad7ab5c62d0277475e590fdf2fb0cd4058df2d29a6aaffe2e41a497c5de3ae2e` | 0 |
| external/lvgl/src/draw/opengles/lv_draw_opengles.h | 707 | `545e95d96ac46ddd3d96373f5cb8cabc7a9551b0bc231660e4b47b516f367d8d` | 0 |
| external/lvgl/src/draw/renesas/dave2d/lv_draw_dave2d.c | 19946 | `f053e39b176f7b698c11a700fb7a36ceb521888994ac9003adf66a9bf10d1613` | 0 |
| external/lvgl/src/draw/renesas/dave2d/lv_draw_dave2d.h | 3839 | `c1e25cee536f373059b345f0482c301722b20e6012e15d6c7032493ccffcad6c` | 0 |
| external/lvgl/src/draw/renesas/dave2d/lv_draw_dave2d_arc.c | 6955 | `6799666a7884b0dee2d6fb8b787885a1d0a505f96f425d4e4adc8ff6d2f10701` | 0 |
| external/lvgl/src/draw/renesas/dave2d/lv_draw_dave2d_border.c | 15271 | `5d4139208574ea7fc7ce6624c5745553f847d9226d06394d856982b0a44383b4` | 0 |
| external/lvgl/src/draw/renesas/dave2d/lv_draw_dave2d_fill.c | 11912 | `2a8bcfae5090dbf8570d1f2855da6b91e6f856db676ead663b48ba02cdc94229` | 0 |
| external/lvgl/src/draw/renesas/dave2d/lv_draw_dave2d_image.c | 11682 | `983eb6edcf154eb109ea94466cc39eb9f5ee39a512713267c033d724207922fd` | 0 |
| external/lvgl/src/draw/renesas/dave2d/lv_draw_dave2d_label.c | 7343 | `7e55461f97ee73489e32751e3621e1d40ce2f62a0fc113b21545822e04c16b22` | 0 |
| external/lvgl/src/draw/renesas/dave2d/lv_draw_dave2d_line.c | 2225 | `2848032d838c5d201329bec08955592b5d151fccddcf2ed0deb549d72a9ba4d3` | 0 |
| external/lvgl/src/draw/renesas/dave2d/lv_draw_dave2d_mask_rectangle.c | 1455 | `e6c405281319801c26efc11d9d1b2a831c8bc3a44fa7972e0d1483762eb40362` | 0 |
| external/lvgl/src/draw/renesas/dave2d/lv_draw_dave2d_triangle.c | 4507 | `c0df1dcfb31a018084c6ebc1ebf766cef3d74f4178683cd99f8dbeaa45a79652` | 0 |
| external/lvgl/src/draw/renesas/dave2d/lv_draw_dave2d_utils.c | 3663 | `703b15dad391091739692b1534b2cdde5b2044221121fe44e7f5a9ebcecc5263` | 0 |
| external/lvgl/src/draw/renesas/dave2d/lv_draw_dave2d_utils.h | 843 | `7df826a57f751c26f11655b8248344f6359655ab21dac3586b15f8665dce8e41` | 0 |
| external/lvgl/src/draw/sdl/lv_draw_sdl.c | 18896 | `3cbc348ddcb33512f433fa04db3408e236415a11cde88c6bad10724f07b4edce` | 0 |
| external/lvgl/src/draw/sdl/lv_draw_sdl.h | 2268 | `11c0190a36fdaf75bec381a01c7b946593cd0e48e65e467ec315642fc13e32d0` | 0 |
| external/lvgl/src/draw/sw/arm2d/lv_draw_sw_arm2d.h | 26909 | `62aed206e4d11943395cef613b66a67b5088ffa1a7eb01439c5dcc22f986a992` | 0 |
| external/lvgl/src/draw/sw/arm2d/lv_draw_sw_helium.h | 1106 | `4f035faa6d0959f853f2f53049e1ee32ec8fceb1cc637b4691f5038b4b4d91a3` | 0 |
| external/lvgl/src/draw/sw/blend/arm2d/lv_blend_arm2d.h | 39784 | `37ca545d7e8095ef8df5d01e21d805270c080f07ce9b916caa258d7d47009669` | 0 |
| external/lvgl/src/draw/sw/blend/helium/lv_blend_helium.h | 47947 | `2d2f8b8569c7b985e40614bae6c4d90847ff12c6b055397b73213449875dc1a2` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend.c | 9678 | `61631e4f9b4e9117fe17387a22da2f11428952255da46869b7e229f4d59c7865` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend.h | 1363 | `0865a61b9cc65c54e1b5ce029465f0955a6c77e6126ca38d9f28b945ff2b5344` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_private.h | 2372 | `5e889bf2ba481a13f2b20003761a11709f734dbd47ce0de922f806e4687c3f37` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_al88.c | 41160 | `bf746eae222b1a5162916cd4240973ed0b31f4d4bc1117acfbc771e31df72fb6` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_al88.h | 849 | `9eff75b0e87916ff2c0c3407a3fc8a3e6309e5be0e5d7485b24eac1f6e032d69` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_argb8888.c | 57757 | `c3d7dbb731076fe4a906a97611e77ad5419893efaec067a89860666389bec4bf` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_argb8888.h | 873 | `dbf68d652e1abc0a8cf7c15ef3d178ae642e35e8c33ad51019246c9cdf95b56e` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_argb8888_premultiplied.c | 37235 | `40de554dfcfca2081769a861960abbcc35dd89582c64f1a3f9a0ebaa67309d10` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_argb8888_premultiplied.h | 956 | `538e58c98bcde31fcff3b5ff2217922a869910f88f6e96fc3c40bc34b375d307` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_i1.c | 54018 | `2209204b678672bd09924418205bb78e1960f17aee0df696bd5068911546d446` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_i1.h | 837 | `c0dc5caf960277d2a562675b1f43e08d73cf4f0aaf17958a4b6f0f4da608803f` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_l8.c | 40219 | `c4c26a11d1e3018dff6f9be34a57ba2979cf1f2913ad9e4b7cbf1ea0bcdd207d` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_l8.h | 837 | `a4734fbf57818420c94986f38cdda2d51dd4b635c2debdb2fae79a046a11848f` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_rgb565.c | 68705 | `b25dfda8103b8c5844b06d705fafc341533bcf82f7b87c069f6d53e775580c5b` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_rgb565.h | 861 | `c4567efcf56ceb2e1743a0c5174ab84f9ef28371cbce01b39b5cde34d2d3a350` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_rgb565_swapped.c | 75389 | `42ac068b7b79cf40ad0ea9006976ef51eca125251c0bed3f04804a203c97deb4` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_rgb565_swapped.h | 909 | `9d666a65971eee9c7f53b378b1c60c6b2416c01a3dcf056c104b4fb8febf5c33` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_rgb888.c | 48857 | `6d070bbff6d038fd795d25fcaeede12e080bc7d0440e75063c31472002c236f0` | 0 |
| external/lvgl/src/draw/sw/blend/lv_draw_sw_blend_to_rgb888.h | 1039 | `dc54eee5def983eceb520fa2f1f5852fa1d3af1b40d55d474166ae1541eb6a49` | 0 |
| external/lvgl/src/draw/sw/blend/neon/lv_blend_neon.h | 856 | `d2425f67137d2c5cf78e2259bff78aeae006c0806116a47c4df3ab4fd793e687` | 0 |
| external/lvgl/src/draw/sw/blend/neon/lv_draw_sw_blend_neon_to_rgb565.c | 100019 | `ddb05548df7076f5dca4fc4a565926d003938643262a424060a5d6e710675919` | 0 |
| external/lvgl/src/draw/sw/blend/neon/lv_draw_sw_blend_neon_to_rgb565.h | 8189 | `17f6c440d7514f796501fc3e698afaae42972bfa9696fe0c457345d0694982e2` | 0 |
| external/lvgl/src/draw/sw/blend/neon/lv_draw_sw_blend_neon_to_rgb888.c | 75484 | `2474db675a391795172ae856a3649062f894c9f72dfb3428d3732c8baec74c6d` | 0 |
| external/lvgl/src/draw/sw/blend/neon/lv_draw_sw_blend_neon_to_rgb888.h | 8036 | `4e40c15062e01172772a9e1ffdb1a553e30077e9589e21287c0be0a2ea5a4fe8` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw.c | 13944 | `815767c3484098bd5d505968d4fb24d579adbf8fa9a76b05429e72068d7696c6` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw.h | 6298 | `dcbb10b5cb1135c20d65eb6732637e40f76b42e4d13dd29f61d6af27288bb81d` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_arc.c | 11289 | `a1b0eb4671e553590848813d8b1993b1dea3544eb96a6987edd2efcf90aab123` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_border.c | 11417 | `9d9b8083284c459edcd4f09d7d98f878250b01c670366cc503cabb89761b5650` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_box_shadow.c | 27811 | `7fd22e75af363ac148f9e10e37a14233cc3056dd30ba907dbcc985da824340d4` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_fill.c | 12974 | `fb44ea37597348ad96ea1bc89c8361d6b5be034aa6d7409207f6772ccc3d7251` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_grad.c | 19929 | `b5089de0fb5e3ee4720b1bc8300adf2076d0af6aa1e997fadfaf6741cc8426a1` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_grad.h | 5034 | `984308dbe083609ae6e6b2d7411ffa9c2050674feebe3420a61194265c20b4f4` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_img.c | 41944 | `aaf1f0d1605fec25ff996591710bd6b6ae6961ea010bed3b16b81fdb678cd972` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_letter.c | 16240 | `1a816965ccb153dab44136c3c8d6241e4f128a9d121056240bdc52508876b6d4` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_line.c | 13595 | `40ca00c3fad2850a4f375553ae1e62ae9c52b18f99dd9efa32d374477e358a05` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_mask.c | 43448 | `79840ecf88dc2e1ac5f9b33cf33144078a93cbfb66f721f5be0f9fe0107eebf3` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_mask.h | 6967 | `672b4d9981bdbfe8d006fdaf6034534cd6883f20c9299081b64930c899c9b3fa` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_mask_private.h | 3863 | `6e5e74fd4ab4d7ac6e6e0ff6956786893d7bd5a4dbfa4361385d2a1e62dfa66b` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_mask_rect.c | 3887 | `e1f3c696daef7677a0928bdfea687f65d25312b88ef8e44db3f6ad418c0d7c9e` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_private.h | 1355 | `4596522585731ad498b83dc759f03653e1848e68f1c0c81848dd35086f444c5e` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_transform.c | 38613 | `7563df59d359659efcbf70973a388c8b26eb6137b2ee6d78a44b75e75bee1592` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_triangle.c | 7118 | `1d5d3ce1e18efb912d4d6f47b46ba394462028051cf3e795d5f7ca7e0edc3211` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_utils.c | 20110 | `9fcad9796d421f99a88ceae4c498d9e23042c82e809a67df90370b2b44874a5b` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_utils.h | 3957 | `b9371ce464c848fffb7233dd61ee296c26cb3417f46938df2fdb45f70a1e54b1` | 0 |
| external/lvgl/src/draw/sw/lv_draw_sw_vector.c | 17270 | `64d26f57983373f3dde3d90225798328115952f4618147f37fdf36aae74797b1` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_buf_vg_lite.c | 1313 | `598b9b388f3e7f9200f3d648a6f5f0cfe8f03d1e7b3b216550000d24824802ba` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite.c | 9360 | `a35a4c0f82c8a5e7ba26c616ab50040ac38a7a2778285b7f5fea1e1fad8326a1` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite.h | 2723 | `0bc611ff2059d4f9036526ae081f342914b18d59e3fc3e5b43070b05f9ab878c` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite_arc.c | 6656 | `66ec3c4eb6f48169307c8ba0f3f02fa6174e33bc9ede856c7ad79d119ffd9c24` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite_border.c | 13793 | `9e333e0a3cb87f2a1fb4ed48ff6961a6cd594e3429c47bd700554745306b8790` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite_box_shadow.c | 2685 | `023787977bdf32bd9860609a7906dd591815342b5e988431ce6fe2d5a98196dc` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite_fill.c | 3046 | `53f9d280672233d60ced1760c77987ce9960301ca754ed9864ec549728e1ce28` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite_img.c | 8069 | `51978c364d80ca0aba277bc69089946cfa611d06ee1d7db6ae818b76d44b4574` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite_label.c | 20162 | `aaae9ad2265224f10766ac469c51df7a752e0c3045d5a04319e41e6c019171be` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite_layer.c | 1776 | `d443f3cc2b11eba46bca90b2e9df14efa807781fe5375697bd78317fd8062cd1` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite_line.c | 6082 | `2f20b0232fa4372dc365221881135e98f1c8d1ef448fbeba2278cf6830aae0f3` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite_mask_rect.c | 4920 | `90806e37fb80b5a1912bfe5a092334865a9ee8d927b2c585ff9d838a70ce7bc4` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite_triangle.c | 2705 | `b22092f6f5fb2384fd54acd462b6d1d3f6663ab66a7cb6b8b9aff3492b53752d` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite_type.h | 1494 | `cf6a3e619677498a760f9406552298c6172a33aa69102e87cda4eb8891c63f49` | 0 |
| external/lvgl/src/draw/vg_lite/lv_draw_vg_lite_vector.c | 16979 | `575ecb436bf90152b61418485ba9e7b805981179d39cc53699732f095412a76f` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_decoder.c | 11494 | `eae1b3b636e2d56bee4d4816c85e10259fd4759277ca628727c5d1eef49caf7e` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_decoder.h | 716 | `9bea602776b03689fe5b5f59b934a61fee52293b9d8cd25020850728592df2c8` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_grad.c | 29769 | `fe108d9d5c2c9aa2af18ccc357b762314a70cc8608ea6c9ae47dc81b175fd15c` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_grad.h | 2841 | `b3000d010ba4087098fd1043a6dfe097ed83a202f4d304e0ced1d04abce5347d` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_math.c | 1034 | `6ec7978735aaec7605d3642a2117e7061986cb0d40703c983d5535344f715897` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_math.h | 1447 | `db649b02817074778294f90a23cbde87f95a46cd7d1826e4f519ad09e97bf836` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_path.c | 20843 | `5b6d972466183730974c8ba7181dd90ff31591ee23957b8252393e6ad68c8921` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_path.h | 4398 | `2ed6cc0924a7792089aa7efdbb6393b894fb438dc8f55cea244b8417ad59a4e4` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_pending.c | 2977 | `53ed7fc2bf687d24331e0472f7998d0a4da490c0dd55089bcb71ac8d6cdc97e5` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_pending.h | 2119 | `dd98bcf394a2c0448486dc087667abb3eaeae03f482e600d9766d9a6cc0873f9` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_stroke.c | 12148 | `9edda809acff250de8bfbe6655606cf7884e08e479adad8461d0dff5d99fb19a` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_stroke.h | 1916 | `878f6248cc0da84cf946d8b75701c270f239295cbb5d2e1a42e0b8b463cc7eb6` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_utils.c | 46419 | `03b1c354e6d2d39bb5ef4d07f449160f9c3cf3f0b5b446e708ac8bbd9e7164ee` | 0 |
| external/lvgl/src/draw/vg_lite/lv_vg_lite_utils.h | 11165 | `106452077e428d48049aa4beba84a53506808f5f7ef727cdfdebf6439ca8d333` | 0 |
| external/lvgl/src/drivers/display/drm/lv_linux_drm.c | 30389 | `578a80b9f422f4410a86af59a31a1845dd5d2c2bb1180f29d14034e376ce3e25` | 0 |
| external/lvgl/src/drivers/display/drm/lv_linux_drm.h | 4058 | `c45d281d6fbfad07b2826cce92aa631a3bdb84a88a204e4fe869197089b2565f` | 0 |
| external/lvgl/src/drivers/display/drm/lv_linux_drm_common.c | 2689 | `5ab61fbc6fccff4aaaaa7c1e8dd4f7c0507513d8d04fa4904c0f51e2c07222f4` | 0 |
| external/lvgl/src/drivers/display/drm/lv_linux_drm_egl.c | 23441 | `f230226e365addac8a03cc8159f5841c4c79c2bbca80ee2cbe79b81ff13cadce` | 0 |
| external/lvgl/src/drivers/display/drm/lv_linux_drm_egl_private.h | 1519 | `a97b9d62b8517715238cb596da6688b06eb4356b10aa921be94f832451249695` | 0 |
| external/lvgl/src/drivers/display/fb/lv_linux_fbdev.c | 12414 | `f4a258cceaf8d88ee9aebe57ae075efc50913d8246820baf7b941ece60a39617` | 0 |
| external/lvgl/src/drivers/display/fb/lv_linux_fbdev.h | 978 | `597c23b9fce5bcbed8a043585872c36adeac86038815b91dd7e313a68bd9d3df` | 0 |
| external/lvgl/src/drivers/display/ft81x/lv_ft81x.c | 16207 | `fa590caf11cdde2eeca8bdd18f117ebe001ace8cda4a11fae97e5a5231d3eef3` | 0 |
| external/lvgl/src/drivers/display/ft81x/lv_ft81x.h | 3002 | `274a32a0104cfe5b9bd06831cc4b08b7228b5429d033cfc6bfec461283147303` | 0 |
| external/lvgl/src/drivers/display/ft81x/lv_ft81x_defines.h | 32280 | `90a7f28424d96e201f51ce9f5c0f8b3bc7d96603fff33d48053cae05874c97b5` | 0 |
| external/lvgl/src/drivers/display/ili9341/lv_ili9341.c | 3858 | `1843fc84c50c6cd135864752a42b3ad39fcb979ed38a2346e5f4acfb896b4278` | 0 |
| external/lvgl/src/drivers/display/ili9341/lv_ili9341.h | 2463 | `d64e6b253ea17a7445df7a18813d7e278320bc23f468924cadd81a069a23b124` | 0 |
| external/lvgl/src/drivers/display/lcd/lv_lcd_generic_mipi.c | 11626 | `e6db705a7467cb8e76cb1e619d9ac121ce31c09c4d3d8786b6e808973c5b5db8` | 0 |
| external/lvgl/src/drivers/display/lcd/lv_lcd_generic_mipi.h | 13743 | `4c3e8bff229771dfce6d46ec8e4a1ad867af8ee474c0983f748dffc8d04d4633` | 0 |
| external/lvgl/src/drivers/display/lovyan_gfx/lv_lgfx_user.hpp | 1103 | `a63a0a92f428cd4702811c0b38653866fe9a72363425c1086914a0e378394b77` | 0 |
| external/lvgl/src/drivers/display/lovyan_gfx/lv_lovyan_gfx.cpp | 4192 | `73260a0231fa5c9dc63588ac9220c8cbb5af4e234e12f6bf984894f23d0b7678` | 0 |
| external/lvgl/src/drivers/display/lovyan_gfx/lv_lovyan_gfx.h | 824 | `ca95498b3430316e70019afc467cb97c778d4431b40a8f8f6a996c90cff4aac6` | 0 |
| external/lvgl/src/drivers/display/nv3007/lv_nv3007.c | 4620 | `35b006ebed76755f7896a9b5249b1ebd495f49c9b870aa234389871f58ae7acc` | 0 |
| external/lvgl/src/drivers/display/nv3007/lv_nv3007.h | 2446 | `8067399de0e506b922912e1119cf9d07412cb82771b839e588d5f36908785f19` | 0 |
| external/lvgl/src/drivers/display/nxp_elcdif/lv_nxp_elcdif.c | 6120 | `9c3910fcc81947f63c8d82fa63784ea399e0e2ae0d5f9e6c73e7c3fb7373f75c` | 0 |
| external/lvgl/src/drivers/display/nxp_elcdif/lv_nxp_elcdif.h | 2716 | `3c5c8efdd091fc7ea65b6c8c5c8f9ad9d4ff9ed4770c5c356f449ceee433d6c4` | 0 |
| external/lvgl/src/drivers/display/renesas_glcdc/lv_renesas_glcdc.c | 10581 | `20c3f2fbce8543f537158346e5f667156bdd7ddfaee27d8b9a1642d4f43b9b09` | 0 |
| external/lvgl/src/drivers/display/renesas_glcdc/lv_renesas_glcdc.h | 1175 | `f011bdb819609fa8b15aba55c145eccb1cebe9fe2298c6b83b52c0d90dc46e01` | 0 |
| external/lvgl/src/drivers/display/st7735/lv_st7735.c | 2815 | `3e72a08a0cc201252fa932e89bf09f8453b76ab2c62ff82853de6aafc5443912` | 0 |
| external/lvgl/src/drivers/display/st7735/lv_st7735.h | 2445 | `50d5e8756c0bbe7e50164a6aa83ec391cc004203513741b50e80b6dec1aea5a1` | 0 |
| external/lvgl/src/drivers/display/st7789/lv_st7789.c | 3405 | `fba5a64365089202cc802abf5e5fe267d2670810d1531be3e74142d67451475f` | 0 |
| external/lvgl/src/drivers/display/st7789/lv_st7789.h | 2446 | `895d19a03d674ed131f4ac7a3ed169809fd4851cd70154da0fb9e3534e42c451` | 0 |
| external/lvgl/src/drivers/display/st7796/lv_st7796.c | 4173 | `1205a543091051367c5f53d1bdbf9feb819d11f95128602278380c063dd72371` | 0 |
| external/lvgl/src/drivers/display/st7796/lv_st7796.h | 2445 | `ed7354b1587ae2b9a01a58603fe09b81fc51d3ed2d6ec00f4c937e5cf4c1c283` | 0 |
| external/lvgl/src/drivers/display/st_ltdc/lv_st_ltdc.c | 9956 | `b29d16172ed77aeedadbbda422546541fc65fecbe84dfdf80d1648cbb0789a3d` | 0 |
| external/lvgl/src/drivers/display/st_ltdc/lv_st_ltdc.h | 1767 | `12802eb8fcfc1a8819ce92341607a09f138bdf362bbc20ef621fd48b60b05f3c` | 0 |
| external/lvgl/src/drivers/display/tft_espi/lv_tft_espi.cpp | 3127 | `a4a80f734a5162f03cc2e0800535f5e29e77455547532fbb675862c20e337fd8` | 0 |
| external/lvgl/src/drivers/display/tft_espi/lv_tft_espi.h | 725 | `fa191eb8b82497016e734c88b0433bc48a94ea9919da7b616402a154037db105` | 0 |
| external/lvgl/src/drivers/draw/eve/lv_draw_eve_display.c | 9131 | `55c673d5755b3c726ae666b46a7f419ca0a93ffb64362b1cea70c3a7d8a0bdf2` | 0 |
| external/lvgl/src/drivers/draw/eve/lv_draw_eve_display.h | 5233 | `511a0c79d9958a506ddf4d306e15a7186fea9b5c46596244c490925df583d9ea` | 0 |
| external/lvgl/src/drivers/draw/eve/lv_draw_eve_display_defines.h | 55974 | `c42b2fe7c2d0b738330af46b5ccc5c99f5cdee9531e687ab1b3f9d7b2108061d` | 0 |
| external/lvgl/src/drivers/evdev/lv_evdev.c | 23497 | `8d552ad90054450a36594d8a983a8a39e10e70e9cd65059d44709cdcb8872dc4` | 0 |
| external/lvgl/src/drivers/evdev/lv_evdev.h | 3169 | `46d2db37aa3d0ab398df9c4de6a374f23a7e4d5825aaa9270f39f8d3476101d0` | 0 |
| external/lvgl/src/drivers/evdev/lv_evdev_private.h | 636 | `8809d95f2ff47cb8e69cd181d201ce45ff12c336f00684a84f0ae8df05f5e9ed` | 0 |
| external/lvgl/src/drivers/libinput/lv_libinput.c | 22681 | `a100da0d6933788839db59a63f5ed608fe82eddead2ac6dc5676de6f2f0eb2f0` | 0 |
| external/lvgl/src/drivers/libinput/lv_libinput.h | 2855 | `35417de00e0b20dd18a394c136b01f02562b930b81b89483302f32c5815ee70a` | 0 |
| external/lvgl/src/drivers/libinput/lv_libinput_private.h | 1798 | `a390580971a6eb78df2aae3b0503007e2ce437cec3f4c78dc6cb07b3da209051` | 0 |
| external/lvgl/src/drivers/libinput/lv_xkb.c | 4281 | `7028055834da6aa234ab1578875b7155a0344e42e0140cbbf6730c330d973c89` | 0 |
| external/lvgl/src/drivers/libinput/lv_xkb.h | 1335 | `7ffc7ecc19e3808171685ea7d7c9e8721bf120f7f89c83b097718cda24d12022` | 0 |
| external/lvgl/src/drivers/libinput/lv_xkb_private.h | 814 | `5addb372832853b95e9275117ddae8b9d480b55852c3d59d76caa82e08faa057` | 0 |
| external/lvgl/src/drivers/lv_drivers.h | 1976 | `a62f6cc8e1b85453b003880180643b017608e31af9d1d0f8946989d519f6bfd9` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_cache.c | 2948 | `3bce5b0dfd7dc86915f63286836973bde044e48f933da79b94eaf317b5d0fb02` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_cache.h | 601 | `f4c649e574422b470c156103805512db23a38c433f3509f13f877ae8857e17cf` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_entry.c | 7237 | `b9ac4529a667b01f6ce6fd947846cdd8852e806f471a90483560d74a1fc21808` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_entry.h | 3258 | `502b299ccc2a9e39882f27595d5db3ed31042bc6f696bd324a94c5cad386d8ff` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_fbdev.c | 14163 | `10125f69afa288bf2dc6098589852cdef707229a783693203c3330500e650f48` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_fbdev.h | 961 | `548617e25ae1c45417b4dda90698c0f39be1f9056d34672a5cd238a4decfad89` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_image_cache.c | 6488 | `8589d4a5db3fca9e4324ad0187a2917c96956db0ee7a9e0bccc641e684e405a5` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_image_cache.h | 729 | `d7c1b5e6a079afc7f67df996a96fd8d97eef92a9c901b9405afbc135489df968` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_lcd.c | 6428 | `128f17043200456b37e20072dfbbfb9ed431ecbcf88610de7bcb798a211c79a5` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_lcd.h | 725 | `2b5b27d1dce048517247b981fa39bdcd58601e8f3eef4d031ccd5f3772aa569a` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_libuv.c | 9328 | `83dccc9731828b17768a638acb6f00bc059770bf72444fa8f1546ad926d70381` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_libuv.h | 1166 | `1cbc89bff67c97fa70897c03a2964517f25e8f9c80eb29ef37b04b73ace42896` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_mouse.c | 5004 | `5dc96193b49ae340821d42c0630cd13b8acafb57d22009dcb96470bd7cb0d9a6` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_mouse.h | 900 | `c0187ecbf603f9be5c957a82c345b693fa4dab21f0b789b77a99b65a03fb35b6` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_profiler.c | 2783 | `9424f2ace74632be50d366a9267f5a7a6c5d887f06360e1b4cd26393352119cf` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_profiler.h | 670 | `617861f393e090eab96bc52fa801ce27f22f31fb52bfa91a654353dc19dff8cf` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_touchscreen.c | 6612 | `ed4357f0cafad4dc91f9d2bd242d0e7a34ab9f5ec411be9e2263948852b711a8` | 0 |
| external/lvgl/src/drivers/nuttx/lv_nuttx_touchscreen.h | 942 | `6cb7ccca66b96c6f6f8928ca9c8bd6462201c5dbf8e1d20d60680f729728cdfe` | 0 |
| external/lvgl/src/drivers/opengles/assets/lv_opengles_shader.c | 8768 | `c69798030f537370b941aa365bac6ebfccee3ab8a148b5cc2c16e97c95e1bc18` | 0 |
| external/lvgl/src/drivers/opengles/assets/lv_opengles_shader.h | 775 | `b44ba66d8ec357d6beb48926b4bc425610470616b59130d237bc6e658b932376` | 0 |
| external/lvgl/src/drivers/opengles/glad/include/EGL/eglplatform.h | 5317 | `3e9962fb42f7ba918c6ce41b3006465c88d4773107f8865c4798983ec7ae1bb3` | 0 |
| external/lvgl/src/drivers/opengles/glad/include/KHR/khrplatform.h | 11211 | `e5152137e667069b624d2555bb3ccf18ceb4110e0b6c3809a590cbe4c7f682b7` | 0 |
| external/lvgl/src/drivers/opengles/glad/include/glad/egl.h | 29149 | `ad8f200ee64e3e466a8fd4635a3a774e53f4c88e8a4f1f23165076a170831732` | 0 |
| external/lvgl/src/drivers/opengles/glad/include/glad/gles2.h | 52985 | `899f85d3da31315e17c514c475bb3b645765d6c8d1e8714c74442ec369bab497` | 0 |
| external/lvgl/src/drivers/opengles/glad/src/egl.c | 17947 | `aad5ba6461d42961f44099ef843982eb9ca647d138258bec0fe382c5ce061321` | 0 |
| external/lvgl/src/drivers/opengles/glad/src/gles2.c | 29734 | `ad4af201d75ee1bc412f6f33a1a07ae46f1b5b8dfc9865ba2e0f79bc0135846a` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_debug.c | 1064 | `c8b30cd6f46e085c8feea011b412535a17b651eb4e904552bd6c1d3b19a05ed5` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_debug.h | 948 | `5da13c9a57c223045651f701d048c14849a2d1fe78ad03c4877053560cfaf64f` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_driver.c | 21813 | `b38f8686ea80a11cde2fab37a185f03eba8a84ecd1b8a886e1b940c501a0b27f` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_driver.h | 2856 | `2d97a7466f90f3d0ca3dacc15142f8ac06b14d098694b8e260463647113ca6ea` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_egl.c | 17366 | `355370d4c21d37bed7cb7f1d3fab7b4e8aa03d6ceeaa3d88d901cfc29750bb99` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_egl.h | 1189 | `4442c18d56fb4be597f2a18d7d6fa0a406ff3afd944a1391fd6027ce9fd4c007` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_egl_private.h | 2404 | `effeb9557cfafb13e4e82665986328bce8669328c3a758ec5bae9360ee81728f` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_glfw.c | 22608 | `108edca42175da074aa4befb79141b884e1bf80b07b136c9864cff40ab1e4bd4` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_glfw.h | 2686 | `650bdb9a1756effe450e61ca87274c50e516bf123b1bf97730a53a12e9e5202f` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_private.h | 2330 | `16ece7520705eb67c2a6889a6a4170e30ee2cdc7b742a2dd8640e8c9452762ea` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_texture.c | 8630 | `3e24a78e3edd9f2090e8446c9acec86757b7471ee2598f4ebe5c4bfe88009334` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_texture.h | 2019 | `c53c603cac4fe5d586a058a3bf8d953100fad6b07d75c6c25840baf9aee491a2` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_texture_private.h | 1147 | `a99e002e3cb636573383c906e15aa0063ba14fa475e4336af28d078b59899504` | 0 |
| external/lvgl/src/drivers/opengles/lv_opengles_window.h | 3105 | `4e754aa023140cfe72dffc36967df37b58a00faa91db03979298e7ae008599ab` | 0 |
| external/lvgl/src/drivers/opengles/opengl_shader/lv_opengl_shader_internal.h | 3911 | `71bc2f5d7b47592f762e6d4739cd9d16babc57a0188d5d570cc853e70091e3d8` | 0 |
| external/lvgl/src/drivers/opengles/opengl_shader/lv_opengl_shader_manager.c | 21813 | `8c70e7393b904e16edbf3436461f5f605af202f3011fe65b9975a9f7cffe060c` | 0 |
| external/lvgl/src/drivers/opengles/opengl_shader/lv_opengl_shader_program.c | 3309 | `8a660df9bb3b587db178505941256ed6278d466c76811833a9de5b49484d8df2` | 0 |
| external/lvgl/src/drivers/qnx/lv_qnx.c | 15688 | `c56a8d45841ab43202ad2d25e4138fa69fcdd4b51baebb2d3d9cdd5cf364778f` | 0 |
| external/lvgl/src/drivers/qnx/lv_qnx.h | 2104 | `f6c1bcefce8be2e657197f1a36983d823b90db23839b96f54c9edcd604abbc6f` | 0 |
| external/lvgl/src/drivers/sdl/lv_sdl_keyboard.c | 5981 | `8506876cdafb7841c897f3368e77d9a62171acc5a2f8e13f9537c9e86ed2e8d3` | 0 |
| external/lvgl/src/drivers/sdl/lv_sdl_keyboard.h | 718 | `53fa5ef7779bca17c50de2cb9badd964bf9146fda373655f53fce86b1ec18405` | 0 |
| external/lvgl/src/drivers/sdl/lv_sdl_mouse.c | 6167 | `640cc17d3e0ad42300d428f0babe6c6a8ef592147298bab462eae84565affa52` | 0 |
| external/lvgl/src/drivers/sdl/lv_sdl_mouse.h | 635 | `a6bb44241ba8de6768c6d59e3afa87787c4a2c53b84332ce47caa627d831f7fd` | 0 |
| external/lvgl/src/drivers/sdl/lv_sdl_mousewheel.c | 3711 | `af4ee511aa4ed7261bd8718ec6b3405648174ccd048800f3f690af00fd6ea83d` | 0 |
| external/lvgl/src/drivers/sdl/lv_sdl_mousewheel.h | 720 | `90dcee8eb66a8ea9f8c3bdaba04c068889857efef1963f6b30b3c25672de56d1` | 0 |
| external/lvgl/src/drivers/sdl/lv_sdl_private.h | 847 | `be020917737a650ddd16505414b9026adafe4dea383ca106ebb0710e6d5eac7f` | 0 |
| external/lvgl/src/drivers/sdl/lv_sdl_window.c | 17903 | `77336ce61c14defdd81bc122be81258ec1796ab1cc73558af7f69e01d18d3b09` | 0 |
| external/lvgl/src/drivers/sdl/lv_sdl_window.h | 1599 | `22d07e4ed15992a11f39b56bd4a5f0bd510e8b86aabffed842d306ba9b2fd0e8` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi.h | 4029 | `ae55b5c18afdb934e5fbdb4f57894e2a629a05f9006844d13de26f5a1b7070e2` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi_context.c | 1961 | `99ff738925e23a907ea30a5813d5d4eaa596e48f712d48ff3a88120ad6c2a2ee` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi_context.h | 1458 | `c03d161b4d017e1a5ed095a20e801c35f397c5d48c17c47b44f5f7d4545a4ac2` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi_display.c | 8253 | `675ec8cd4c18dbd5e0102dd1426805bcb0fb7a80ac9de1ad38cc087b0df0a6fe` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi_display.h | 1253 | `5bea6ad59c2c76aa6b15b5fe575ba78ce53abd1067d12ca62e16d4f1b88d20ca` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi_edk2.h | 585 | `b2e8bba8db7952e9da2c9d37a413a93f6eea2b8c7544e96bcd27d8860974d53d` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi_gnu_efi.h | 187 | `cfdcbcf9b3d4647923cbd99d995cd4c58690a7d0d7c60662e801b646147676d9` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi_indev.h | 3250 | `b22bfc4e8b44dcc94a329ddd4c792a1ca492c15590e6412a6be51145f335fe39` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi_indev_keyboard.c | 11112 | `db9a8124a7b8cd2fe89a65eb2214ee1b66fa9f32ebfb2d7aa91841f4d82a78da` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi_indev_pointer.c | 9752 | `20793168b305d82655a41ef2ae5e77738ffbc0459fd2a4f8b3be547a56579f1d` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi_indev_touch.c | 10263 | `c45b234a33cbda277a65df633a2a3e9ba480fcb9bb6923655b07824f2153463d` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi_private.c | 6328 | `643ad6c9d8c872c39d51f6de66a29fd30580d48e87efc2ca77521af7912f32dc` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi_private.h | 2774 | `1a2fdabcd6aab35d1e2e5b19b8f1a9955d35018a80f517cff5ae267ff25648cc` | 0 |
| external/lvgl/src/drivers/uefi/lv_uefi_std_wrapper.h | 3297 | `0d94750752e94f6b6aee5b40d7c270549cf50538ba5eff7d17573a3a92f92e62` | 0 |
| external/lvgl/src/drivers/wayland/lv_wayland.c | 17896 | `ee8391509bbbc386cafdb30b9906bf653d063440942337fe7bb226b91b0c1871` | 0 |
| external/lvgl/src/drivers/wayland/lv_wayland.h | 1086 | `c46975afae0bb65cf6d70a74fe9591412254f7e253878e9d7b121be3ed098af9` | 0 |
| external/lvgl/src/drivers/wayland/lv_wayland_private.h | 12423 | `fc6c35a43c7e171069b6033dab42f3de7bd4d44ae320502e863b42232f153553` | 0 |
| external/lvgl/src/drivers/wayland/lv_wayland_smm.c | 18155 | `4d9b808d6ac6a24ef9e4eae934c50bc81c6d82b6aa3a972431a991f089841ca1` | 0 |
| external/lvgl/src/drivers/wayland/lv_wayland_smm.h | 2397 | `7a0312b54eed81e77855ccf1f9305427bc300511c62ba7cb8026d5d5db72819b` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_cache.c | 3705 | `bb40a30337bbefef4cf5b94ed750faf23a1ec356f572c2a5f2d7f1c5d099ff9b` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_dmabuf.c | 25480 | `344cf05068d5e1deef15acebbe448c94c41487461788b339c3a98dbac78ad400` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_keyboard.c | 8423 | `3843c94a3380f15ecb5f6b29a13e1bfae907a4b05f724b4e4d31c96228204e8a` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_keyboard.h | 924 | `546b3152f1624e4a1065af0dc2f82af2bee00237d0ad5a2182fd1855a5b48114` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_pointer.c | 7125 | `f869c71cd4b2bf8ab5cae37e8b6a9a3b31f940af4b68a3c4f238dff8d778e88a` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_pointer.h | 982 | `6909f1ad66c6449caa9ba28b1365bbc98c0653ff3348bcb5afbf925902d86379` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_pointer_axis.c | 1614 | `4a994f1379373c354618936bd59cd336172b770ca85e803ce2c3c49f1d0bbaae` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_pointer_axis.h | 1011 | `847981e6f3bfb6c784f58f8ea0da5ae855f53efcf7820d22594dfcb892cc07fe` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_seat.c | 2674 | `bcd2e440dba8e5ac30c7853b0113e6a150f7cd08c940568c1f27bb70394dd90e` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_shm.c | 15976 | `7c3cebf9188a8fd64784649cfe59ddb3a4d167eb770a5523aa4ef03f3fc8e62e` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_touch.c | 8616 | `e1a7eaa6e6ad07a5d32258ee3455d9ada20b0cb9e4d53404697b8ce1d9691511` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_touch.h | 920 | `382ee96fc2e0f0bacdf0d81f2a0b4191cc585828c5b5f86b559ecfb006316613` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_window.c | 14867 | `c8ea19b4ad0b9a993b4f5ff8ff14e3ac723c084ae1e52364f26964d65976a903` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_window.h | 2498 | `4fb171c14b33b270f38dcc1eff5e66e33f5481c6c45411fbad3709a06056af87` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_window_decorations.c | 13372 | `61f6b2f5679af7fe53f169dd207bae4b6ad37512c4272230a725566b1871be93` | 0 |
| external/lvgl/src/drivers/wayland/lv_wl_xdg_shell.c | 16240 | `17543f3ec374fdbb95223f0320d5f9e0dd3ea1c950df6725c511087e59c28f6f` | 0 |
| external/lvgl/src/drivers/windows/lv_windows_context.c | 24748 | `fcc680da7d61a8b9be18c74f0db41637b63d6bbb574a5c2bd01c52c937041321` | 0 |
| external/lvgl/src/drivers/windows/lv_windows_context.h | 3378 | `c7d0c06b516cc27951c5baeaedc4d754bc944f3745031f2d1b52f0c083b817c2` | 0 |
| external/lvgl/src/drivers/windows/lv_windows_display.c | 4469 | `39266b93622cb84824a6bc3faa45afaa5c8b76a75cb9adae59a9cd64e437e3b3` | 0 |
| external/lvgl/src/drivers/windows/lv_windows_display.h | 4082 | `17bc028841450212864fc32d4a43e6dd3006183b6f1d9bd252f44a9716a0b2d6` | 0 |
| external/lvgl/src/drivers/windows/lv_windows_input.c | 28018 | `83a8b18c7fe8af8025a612639d4d7af0fbcdb56d431fa2409ab78dc544223ea8` | 0 |
| external/lvgl/src/drivers/windows/lv_windows_input.h | 2212 | `32eda79c6b62e5107ea7033678993985d256b871589a4781254e7355f789d245` | 0 |
| external/lvgl/src/drivers/windows/lv_windows_input_private.h | 1108 | `2756efae19fb95a24537c49c69ac68ce240403230aeed8f4d452b6274919da72` | 0 |
| external/lvgl/src/drivers/x11/lv_x11.h | 2378 | `ee421aac355a9fe8504cecd8adaaa4719741c3861b79a7e7bb48b83ac9891489` | 0 |
| external/lvgl/src/drivers/x11/lv_x11_display.c | 14647 | `ad352b905d1eca667a0ad4caba4fb8ee914caa26eb2d2e15c7013399284df4b4` | 0 |
| external/lvgl/src/drivers/x11/lv_x11_input.c | 11665 | `c9f7ce3a8ce0a32f69dd20c4cd562d69d06c5ff2e071949bfad3f024608c019c` | 0 |
| external/lvgl/src/font/lv_binfont_loader.c | 22180 | `8ecd5e70445313e4b810d81db5b860765b43e85f29e173b73391b704a6fa635a` | 0 |
| external/lvgl/src/font/lv_binfont_loader.h | 1692 | `ae529c7706a7a53d9652b0380c9d54558ba2f50e51cc75c43c12a10168271664` | 0 |
| external/lvgl/src/font/lv_font.c | 4958 | `64e6b5b180a2986a1f1b82a2884a89114165604be0588ebff7b740f3ea6234fd` | 0 |
| external/lvgl/src/font/lv_font.h | 11377 | `f8628984c4f5f94a6ce6af1184f1e3e41bff567377b366619cccb882809fc884` | 0 |
| external/lvgl/src/font/lv_font_dejavu_16_persian_hebrew.c | 287976 | `8599edbcdd1d2facbade0f07d09c6ab8bc82e8944bafc3668cd7219653cfca7c` | 0 |
| external/lvgl/src/font/lv_font_fmt_txt.c | 22317 | `b462bdd8430e37dea15e69d4173b75f12b57b4e2f13e857d432f5ea36d4d386e` | 0 |
| external/lvgl/src/font/lv_font_fmt_txt.h | 8342 | `06cc5c66d872d7349c3449b2625a99d45e161ea88ffd75f2d9d4cacc16e5bbf7` | 0 |
| external/lvgl/src/font/lv_font_fmt_txt_private.h | 921 | `509384e80e9a679c82cc533b895594e02d1da9461faca3b89a908e1fae7a21ef` | 0 |
| external/lvgl/src/font/lv_font_montserrat_10.c | 63143 | `afc14fefad31c0fe072fd6d3846c89df1277b77713d458e8b3e4ceaafec30d39` | 0 |
| external/lvgl/src/font/lv_font_montserrat_12.c | 76198 | `5be9c2a8878c694e8abd55643352023a7071e5bac474423337ed2e2eefcd8b7e` | 0 |
| external/lvgl/src/font/lv_font_montserrat_14.c | 89473 | `a050906a9d05b51d4678b8beecf41bdb353d161729c34fe9c930856a3036d353` | 0 |
| external/lvgl/src/font/lv_font_montserrat_14_aligned.c | 183182 | `9b576bd9452ff8ce78a1f9f2d6421a2a9386606f4ff681e8501fd820ea4297a6` | 0 |
| external/lvgl/src/font/lv_font_montserrat_16.c | 103154 | `bfe04c1059a2cb310c8c7a69e72d52e720f743e26065fd0ddc4561f2423ed372` | 0 |
| external/lvgl/src/font/lv_font_montserrat_18.c | 122375 | `cc3b22b9d8c7689d4250e319136d26f4808ed59da1ca753f06305d3f2ff22248` | 0 |
| external/lvgl/src/font/lv_font_montserrat_20.c | 139125 | `d8b67ea4c76ae2c71bf8203521de9f74fe17ac01fd6eb7fff4918057d5c59f34` | 0 |
| external/lvgl/src/font/lv_font_montserrat_22.c | 161216 | `43c3c6d4b39cb1884dbacec21c4cfee820466e39523acf082f9128e06e0899f0` | 0 |
| external/lvgl/src/font/lv_font_montserrat_24.c | 181037 | `530fb723e9f225b8d203f359fdb70ec59ef2e1a043a6bc6ebaad0768050ec91e` | 0 |
| external/lvgl/src/font/lv_font_montserrat_26.c | 206668 | `6a0ab0686efc751cc41c0df15e77cff137c4f515d1674b65943d71bfffc17908` | 0 |
| external/lvgl/src/font/lv_font_montserrat_28.c | 233057 | `779d47f0eb18c2563fb8bffe50dd9f797fcebced2abfe7edb9c961413f9fbce8` | 0 |
| external/lvgl/src/font/lv_font_montserrat_28_compressed.c | 145127 | `6e104239c45fb0ddbcfb1fabd8125c1cfd33ea582c85588a7fb9871c4c749e4f` | 0 |
| external/lvgl/src/font/lv_font_montserrat_30.c | 261203 | `d9dfc1bf226beb682eef29b3f0d72f69d36395df5258b2834a13d92af23505ab` | 0 |
| external/lvgl/src/font/lv_font_montserrat_32.c | 284811 | `0f0b77e61b63d712b728e523d9139dcee810794055773d8699d9787c48aa63f7` | 0 |
| external/lvgl/src/font/lv_font_montserrat_34.c | 323533 | `fce37859b82016ace4d1482319d31a227824b81779e3696befb809e828ed7aef` | 0 |
| external/lvgl/src/font/lv_font_montserrat_36.c | 354598 | `2388d7a652aa52a479c6410bd0ebdf31e2e6d0f8be58f61ecf5b41e1981fc159` | 0 |
| external/lvgl/src/font/lv_font_montserrat_38.c | 390343 | `823f2450ddca033e38addd2a08dd9cf2f01e840ab1a0a917444391f234976e8d` | 0 |
| external/lvgl/src/font/lv_font_montserrat_40.c | 431710 | `0e13032310141859ec8c337358488d85af560e96d0dc18c81138e25212ddd25a` | 0 |
| external/lvgl/src/font/lv_font_montserrat_42.c | 472438 | `b4fe50b53c59078d46db3315afee59559e629ef6fbb52c6cc80010a0b834ea27` | 0 |
| external/lvgl/src/font/lv_font_montserrat_44.c | 511317 | `bb5b7ef84e4878ce37c64f3149afa956ee05b5ef284a89ceda33f73c2cc8354f` | 0 |
| external/lvgl/src/font/lv_font_montserrat_46.c | 557657 | `75e6da97e36ef8d7c3c17d6e0b7b4f880265ef408bcb279521bf69092d674933` | 0 |
| external/lvgl/src/font/lv_font_montserrat_48.c | 591315 | `e68fa0e706d2a18d66dfbe536d9fab83068145159b40091fd261e8be21ace985` | 0 |
| external/lvgl/src/font/lv_font_montserrat_8.c | 52949 | `334eb715262c7d7df7b91a610a29afcc359f1a3c206b388cbf5294ba2219a7bb` | 0 |
| external/lvgl/src/font/lv_font_source_han_sans_sc_14_cjk.c | 1020007 | `b7491cbd00936487ae1cf08c914ca202e64c0604d3b7c0c0aec56d90ac34bb4a` | 0 |
| external/lvgl/src/font/lv_font_source_han_sans_sc_16_cjk.c | 1220369 | `4caaa2aff00bb59d1155227c838ced106ab4d61717afcaa66328cb0b3136785b` | 0 |
| external/lvgl/src/font/lv_font_unscii_16.c | 24392 | `e794d86db88db9a1a9216ac6a564dece6f78e71eca6915f122bca97d0f0ff792` | 0 |
| external/lvgl/src/font/lv_font_unscii_8.c | 16540 | `fc22dae14096a1a6f9365dbcd646c62216cc693cb89c77e22d66a205e61ffba6` | 0 |
| external/lvgl/src/font/lv_symbol_def.h | 9423 | `67884ce07db66697d54f518d04e34dd7d521f7235b7196ed5f828cf1f240052b` | 0 |
| external/lvgl/src/indev/lv_indev.c | 64893 | `94d9d28d51946127d897f5128496fdc899c5e2ffbcfb09db35a632c79fda36dc` | 0 |
| external/lvgl/src/indev/lv_indev.h | 14804 | `314b10ca15b42378b9ce520cac4d6f156e56327ec95534b6db64662e944bc149` | 0 |
| external/lvgl/src/indev/lv_indev_gesture.c | 32938 | `d075b5b878eda78d9c518e2915cc061db0e99aac4f2b9e5dcdc5cc743e6c8f9c` | 0 |
| external/lvgl/src/indev/lv_indev_gesture.h | 9910 | `49fb7df618c84affb253f480b8a076efcf1fa03850d3357adfae27c54197cea6` | 0 |
| external/lvgl/src/indev/lv_indev_gesture_private.h | 3030 | `1fff50b148f7024fdf06e7762ed867c9730aff1dcaa6ec214ca9c999e75e676a` | 0 |
| external/lvgl/src/indev/lv_indev_private.h | 4853 | `ddf3812102d6b4d00f8c6770a4cf14911b469ca568cf0d1640d16a78c4ff0477` | 0 |
| external/lvgl/src/indev/lv_indev_scroll.c | 31063 | `8502fb1b70de2708e54b2f373a1efa8eafc948e37d74ba436737c48ae268c1ba` | 0 |
| external/lvgl/src/indev/lv_indev_scroll.h | 1513 | `278f8447c6dc5823a19ee63b8e1459454c091e31b7e22231f0edfac8092785cc` | 0 |
| external/lvgl/src/layouts/flex/lv_flex.c | 21643 | `2b5ac5ca32dc015dd3d760aa3a2aa33e50b7f148c46f09d9daa73eac92a6e48f` | 0 |
| external/lvgl/src/layouts/flex/lv_flex.h | 3018 | `e20e9d294f2f91f47dae2a1d176b0f00deb17c40fe2b39df8b4e1c8d2fe6cfa3` | 0 |
| external/lvgl/src/layouts/grid/lv_grid.c | 22539 | `2d9131ad6ad481756dcef1bbecdd8f326b19ae3203a3447fcc2e811a6aa145c7` | 0 |
| external/lvgl/src/layouts/grid/lv_grid.h | 2462 | `d8676b7913973640068eeb387c651264017f6fb0465ca854185752004f6613f6` | 0 |
| external/lvgl/src/layouts/lv_layout.c | 1705 | `d083c1b1f92085aad955a8a1f292c57e00c37ff39ef4a68b8af71893e1aeaf77` | 0 |
| external/lvgl/src/layouts/lv_layout.h | 1133 | `6414fb1124d73dd912bc9120916a6fdfb6c49c0cd1d0012382a3584e53c5a8f5` | 0 |
| external/lvgl/src/layouts/lv_layout_private.h | 903 | `a77ddd34114a69c2d4c725ffc7a03c08a25a09086b862742dcc71775edf97877` | 0 |
| external/lvgl/src/libs/FT800-FT813/EVE.h | 53412 | `bd4991bc28dde8f1153d4bc1ed324dd70d56e94f5007556652a7e7f3f11bfcb5` | 0 |
| external/lvgl/src/libs/FT800-FT813/EVE_commands.c | 134988 | `bf57833c09abd0509e0e138dbc2b4a1e22c67f35d693316784e1fbdb9deee1f3` | 0 |
| external/lvgl/src/libs/FT800-FT813/EVE_commands.h | 18573 | `f875ed379fa26a001921b805fd41e28dbed0bf107a7012a19c6e28e4873fd4d0` | 0 |
| external/lvgl/src/libs/FT800-FT813/EVE_config.h | 1335 | `dd8004dc7cf5cdcb4dbb29585c0a415b7127484ea3c5db931ed64a875c77d142` | 0 |
| external/lvgl/src/libs/FT800-FT813/EVE_supplemental.c | 5405 | `48490d7271723a65a4de0122296da6a840e3e69d3e83ee37ed2d52a327b0ea4c` | 0 |
| external/lvgl/src/libs/FT800-FT813/EVE_suppplemental.h | 1786 | `2db47c4599bf7dafb56fda062813bd0406ce5419ec50aa8526d7b550150f7046` | 0 |
| external/lvgl/src/libs/FT800-FT813/EVE_target.h | 3235 | `c42d6aafbde5a56fe7687332f0f6450c9e614b1caceac0cea1d832bc11bfb456` | 0 |
| external/lvgl/src/libs/barcode/code128.c | 18957 | `c7ce6a8685ea560b5896f27f2a6764110639b03d968ae710dc4f67d8880e902f` | 0 |
| external/lvgl/src/libs/barcode/code128.h | 1926 | `cbbc24883857d1191321863b0dc55bba797d524992c41a1390c476e436237642` | 0 |
| external/lvgl/src/libs/barcode/lv_barcode.c | 8905 | `a13c086d4fe4ed12398143d059321ac322b21ce2513429ac5b62aa39476ffdf6` | 0 |
| external/lvgl/src/libs/barcode/lv_barcode.h | 3442 | `578bb41368cbeaeb9423d940c7643556367371a58cb57fd0238a5d651c8151d6` | 0 |
| external/lvgl/src/libs/barcode/lv_barcode_private.h | 898 | `6dff8ae531c7945711a71d4e77e9b4aa4867eee691d9ed95f38b0d5b464b8a40` | 0 |
| external/lvgl/src/libs/bin_decoder/lv_bin_decoder.c | 42258 | `39416e4f018263a5f231cd7065fef4a849c15e5b9b56b33eadfe03d6028f4ef3` | 0 |
| external/lvgl/src/libs/bin_decoder/lv_bin_decoder.h | 1990 | `60588913df80866205d836c5592fc9f427c800a4cccf65683f6e7313a36483cd` | 0 |
| external/lvgl/src/libs/bmp/lv_bmp.c | 7780 | `52f839a5b1a4ed59947572266237f43427b3fe86601fabcb4e23bd3f7fc3f91b` | 0 |
| external/lvgl/src/libs/bmp/lv_bmp.h | 627 | `f33aa945052d97abc55b810b41d3adcdf59ede566fdcaac7784fb3100043bcfd` | 0 |
| external/lvgl/src/libs/expat/ascii.h | 3760 | `ffdf2fb7f4bacbbdbcd5846981e609b6a542c8bd33c6bda646284c1578816e95` | 0 |
| external/lvgl/src/libs/expat/asciitab.h | 3598 | `840e5f0e715572c377be35e365d7363cae3568de2d22d56c5c9ea03c935f9cec` | 0 |
| external/lvgl/src/libs/expat/expat.h | 44148 | `5cd870fd3aa0931ba249e12ececb8ef8358e75f00008c8be397023c300f75089` | 0 |
| external/lvgl/src/libs/expat/expat_config.h | 4332 | `c2dac34784ad0ec553e1a6df74782fd164446e39d17436b06f1410e6af321e8a` | 0 |
| external/lvgl/src/libs/expat/expat_external.h | 6107 | `592a84df04a167b2bf87b46cd7fa201e02975e618312775fa50d16738230ac99` | 0 |
| external/lvgl/src/libs/expat/iasciitab.h | 3668 | `1ac587935add708e8a0a6aaccdfb2935c08e562d21f179c5d9552da0764d2c90` | 0 |
| external/lvgl/src/libs/expat/internal.h | 6421 | `795df2a1fd5310f91abfc55bf3e58bd0686779a2faf2a66ec1bd93ebd9b338d4` | 0 |
| external/lvgl/src/libs/expat/latin1tab.h | 3651 | `1e077d96b08ac8ef7d068e5501038c4c1f017f76aabb3df8e245a2574028eae9` | 0 |
| external/lvgl/src/libs/expat/nametab.h | 9122 | `95b7eba4ea83e78b777e38c5bdb3b3c12e6ad1dea2b3c6364271bef1b4c17313` | 0 |
| external/lvgl/src/libs/expat/siphash.h | 13092 | `8f5fd5fe98e3da3732ed79605c32f60df7de79ba14cf68065f80ce81d849c01b` | 0 |
| external/lvgl/src/libs/expat/utf8tab.h | 3600 | `1051bdd95827cc5f1da02853a13ea982e186f9cc38cc97866de362fa0e657909` | 0 |
| external/lvgl/src/libs/expat/winconfig.h | 2116 | `fa36cfe1bfba4e3a6ce48b18948fb2948c2ebe0f1892cefcc72a8968b1712d5b` | 0 |
| external/lvgl/src/libs/expat/xmlparse.c | 287077 | `68ad04fe38876258a1b742a9294f3fed80a7cc56961fd2fe438609f1f9678844` | 0 |
| external/lvgl/src/libs/expat/xmlrole.c | 35553 | `c0dc74774865d8e4b10dbfb7dcc39fa801c1b98bd214ad9b8cc2f0c7e3f63bdd` | 0 |
| external/lvgl/src/libs/expat/xmlrole.h | 4757 | `c7082469eacbad69a1e59486639993e68900a66f3bb632675b1221244f685dbf` | 0 |
| external/lvgl/src/libs/expat/xmltok.c | 54424 | `efa3e7c677ce15a7187dd5eb40a2f88f4c4e7c13993f5d5047237749d72298e2` | 0 |
| external/lvgl/src/libs/expat/xmltok.h | 12972 | `84ea927045a031d00f2080692f87ae2bc5d2921b8c809d5feb912f350f27185f` | 0 |
| external/lvgl/src/libs/expat/xmltok_impl.c | 53798 | `5f94aa327e58905de8cf1fbb76816c4cff0004773307d72b8e238ba10f208942` | 0 |
| external/lvgl/src/libs/expat/xmltok_impl.h | 3508 | `0a3d8b35138c2ecacbc451f24c36a2b45872074e96b6f6769e30210b23999a39` | 0 |
| external/lvgl/src/libs/expat/xmltok_ns.c | 4718 | `23fa4f71b5896564741d8ac331f753e53a4da2244fa8190a4da9ae76bf05562a` | 0 |
| external/lvgl/src/libs/ffmpeg/lv_ffmpeg.c | 30329 | `0e355c2ad815d27e7691b654056985f7418bfebdfe8b0b8ea2386c9d1f707ac9` | 0 |
| external/lvgl/src/libs/ffmpeg/lv_ffmpeg.h | 2252 | `4cee83fb5de1893fc00c7be5b5f0b2ad3677700b8007c03b07da54ed3e866119` | 0 |
| external/lvgl/src/libs/ffmpeg/lv_ffmpeg_private.h | 837 | `87d46278faf0d56ccee57428e1f4addb0e0f56a55c9fcd4e4b8918af21b946d6` | 0 |
| external/lvgl/src/libs/freetype/ftmodule.h | 1533 | `c8d5ec90afe9db74bde516e03f122b1e236adfd8d5b23feb321a1219371acf08` | 0 |
| external/lvgl/src/libs/freetype/ftoption.h | 38678 | `63aae93dcdcc40c402e52d6f0f3dac548c6e906ebc13312975f61aee420fe274` | 0 |
| external/lvgl/src/libs/freetype/lv_freetype.c | 14849 | `60cca5c319906e2be30ee42873a0b4bc9c2683379e02b9a43f929b3e66d02560` | 0 |
| external/lvgl/src/libs/freetype/lv_freetype.h | 3968 | `e7e7df0a56311f1b4b238a012817efa14e56e0030bbd5995e5a5b3fdf24d3eb7` | 0 |
| external/lvgl/src/libs/freetype/lv_freetype_glyph.c | 8329 | `51da7c19c32f856e5f3271c17db1519804fb6200e6b3d96ba0be891359f2360b` | 0 |
| external/lvgl/src/libs/freetype/lv_freetype_image.c | 6994 | `4f2bd8e157a0ae2970be3a478bb80b36f86d63bb805da74f81c9a73e17da0e82` | 0 |
| external/lvgl/src/libs/freetype/lv_freetype_outline.c | 14465 | `3f5bf86d89f8d68bfb5d9d157190a446f68b92f284f4d8a5089361c1aee4e07b` | 0 |
| external/lvgl/src/libs/freetype/lv_freetype_private.h | 4260 | `5188cdfd9f1a7d9a230a47b7d8125017771793e348c9b64cb2dd226b8bdae702` | 0 |
| external/lvgl/src/libs/freetype/lv_ftsystem.c | 7138 | `a153a7f684956da3cb0fc31607d9cbb8b23ccaca2c3586a4aa6cad738bc0bb5e` | 0 |
| external/lvgl/src/libs/frogfs/include/frogfs/frogfs.h | 7628 | `1536945f54d175415b39d2c750beb07dd4f3063828c829390ff348a5706597a3` | 0 |
| external/lvgl/src/libs/frogfs/include/frogfs/frogfs_types.h | 110 | `3f4fc3ebc763c3bb40df3a971f5584a71d8c5a94a584f8c434c10c1597b7eed2` | 0 |
| external/lvgl/src/libs/frogfs/src/decomp_raw.c | 1934 | `9f1755b0b65832e73445c76fa0020845206d62151cc0d56271c46e81706a5a8c` | 0 |
| external/lvgl/src/libs/frogfs/src/frogfs.c | 10758 | `00878fbbce108ba6f728b3f0627c741783a800ed91999e02c2726107ab6cb6c6` | 0 |
| external/lvgl/src/libs/frogfs/src/frogfs_format.h | 2174 | `aa20c60989450b712a0ae1c7df94f7f75a5b5434767d7d435e591d45c86df2e1` | 0 |
| external/lvgl/src/libs/frogfs/src/frogfs_priv.h | 2076 | `1d813cc2932c575d145e202a16385190d0e5a0e7f9af230d723b12f206509449` | 0 |
| external/lvgl/src/libs/fsdrv/lv_fs_arduino_esp_littlefs.cpp | 6375 | `f4388838820db298b20fc0d4567608f9b16c4c6e0bab17dd9348c87e92c5e1d7` | 0 |
| external/lvgl/src/libs/fsdrv/lv_fs_arduino_sd.cpp | 5910 | `d3e114fbb956dc1bcd0471081f9c78aa790f6d3b1467c6cec6e0a455d798432d` | 0 |
| external/lvgl/src/libs/fsdrv/lv_fs_cbfs.c | 192 | `d5c0b97cee156e0097a22635397a79978146eb6e11e61a69b29cceb89ee8a9e5` | 0 |
| external/lvgl/src/libs/fsdrv/lv_fs_fatfs.c | 9244 | `cedb11239c009ca4f3e555b0412fa10ecdb975c2f6acad1348af3e138edf920e` | 0 |
| external/lvgl/src/libs/fsdrv/lv_fs_frogfs.c | 8651 | `1bd50de532a6cad4bef9c1537a2cd322be24ed0abd9d52c7cb01ed5964b7dd65` | 0 |
| external/lvgl/src/libs/fsdrv/lv_fs_littlefs.c | 8865 | `dc603f5fe9d89acf83991668827051083cc292d321a64872926459bf7bea6a37` | 0 |
| external/lvgl/src/libs/fsdrv/lv_fs_memfs.c | 6673 | `663f9e6dd26fccc62f10de636de52d54e4ad4424cf08430ab6bc0c3ef1ecef25` | 0 |
| external/lvgl/src/libs/fsdrv/lv_fs_posix.c | 11328 | `3e9747910b815393ff7b3a6ed98d4b7ca8d8ab22cb9bc1f1f1c8111df44d42c0` | 0 |
| external/lvgl/src/libs/fsdrv/lv_fs_stdio.c | 10773 | `7a5c2a5052fbde6da0d7426a3b905735e378ee4d0b2804132f72d553d3ed266c` | 0 |
| external/lvgl/src/libs/fsdrv/lv_fs_uefi.c | 17496 | `cceea4b6934e7b3502fb94af27f836cea76398422733a5f7c056a803707a1bb5` | 0 |
| external/lvgl/src/libs/fsdrv/lv_fs_win32.c | 14376 | `a1a86edc1f5def81b28c3cd9caffc5ebe1eaad4caba6daca0f17442a89c7db9f` | 0 |
| external/lvgl/src/libs/fsdrv/lv_fsdrv.h | 2132 | `85267a9054143c5c3ad2b2d9534ac07cbf71881da79abf777cc6972b6682ecbd` | 0 |
| external/lvgl/src/libs/gif/AnimatedGIF/src/AnimatedGIF.h | 9543 | `16cfb600821d2a7e8762fa064e363633158f86929321696f1e8e9c029d61afbf` | 0 |
| external/lvgl/src/libs/gif/AnimatedGIF/src/gif.c | 62992 | `b0c66e3559f4b3c3416c0cdbcbcd6af99deb455ed90a5b89b09f1502b02d578e` | 0 |
| external/lvgl/src/libs/gif/lv_gif.c | 8078 | `89db4162c3d4bd2681550ee0b8a358907247e311cc42a31eb4e027eb0dd9ae3a` | 0 |
| external/lvgl/src/libs/gif/lv_gif.h | 2455 | `d7bd5193b6c9ff515c18782f59fc5d1aab1ced01202af3253768548c50563e7b` | 0 |
| external/lvgl/src/libs/gltf/fastgltf/lv_fastgltf.hpp | 4358 | `9ee6254bfd5869598b68955f7cbaee0eff417ab9e8de1e57173b5201e7970ec2` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_bind.cpp | 5277 | `0708b759f2937b8a9e52ac03fb85adeb1a8019821ca8c878170390c06e063be3` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_bind.h | 3847 | `d1041b1fd0ffa148087bc351b91c5210fc1c2383ec95f6c752316abc335b8baf` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_data.cpp | 7306 | `738af4f9dc9a262765d0027c9df5e507239e0d730d5d3dd52f0f5ad0077cec50` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_data_animations.cpp | 9866 | `e9e70115083da7afad289966d58ae345f7c92802162b6f68393530c0ce24b58c` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_data_cache.cpp | 3146 | `09203fc2c5ef8a66508c612a01c93ec14fca77f36909ae3e900364cc90016828` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_data_injest.cpp | 38075 | `af217b63abab12a0e5aa7ea66823a11d512d6e663a7531fb5770f63d8364f2ab` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_data_internal.h | 7411 | `40aa3ac0482df6e26d5d2732f814c2b8c2bd20d9b8f5fd1516a77d4274712bde` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_data_internal.hpp | 14842 | `a41d361aafcaa6d16813f1bc24b5b12f1c0005f364260a7388acac630f027cbe` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_data_mesh.cpp | 972 | `2d603c6d8a33e2818e402bf8d936cecb0d39c18fd352224a27a32cdc445073cc` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_data_node.cpp | 2507 | `ec8d5afd076591afba7ba182fe487377fc185763fdbfd13a56070a5a4d7f1dfc` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_data_primitive.cpp | 3784 | `a6bc7efa733e4e3119b701e8df32b8789fcae53a1d438571f62e9c7be317013a` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_data_shader.cpp | 1456 | `e84278585c75612a2b782790a16b58b2d9535b1c0209d04323d02b7ee120ec56` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_data_skin.cpp | 1398 | `41cb7f147d5e15662d8f5417e0fca32e34f5f1f609409826022c61bc3f71331a` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_data_texture.cpp | 2063 | `2b20dcaf815ce2aa1ffb97b84a28d1b2311644d697b8081468d2477d8c5f4737` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_model.h | 4586 | `3e5f350939dca4facde29b419dd06d72605a65ec156783c491a35ea4adbe3d5c` | 0 |
| external/lvgl/src/libs/gltf/gltf_data/lv_gltf_uniform_locations.cpp | 9603 | `4ed3971f0ed840161430a0fc5b89ca7730c0740c759d0faf62aa5146d0dc4f1a` | 0 |
| external/lvgl/src/libs/gltf/gltf_view/assets/chromatic.c | 557855 | `2bd0f0553b2a96be5d0ae54ab9ccfb9119dba0e87b9c0c47a70d76f98e9aa652` | 0 |
| external/lvgl/src/libs/gltf/gltf_view/assets/lv_gltf_view_shader.c | 118827 | `b7a5094ab552f184dc3275d9b8e1fc5f76acdd2176ce03e9dc8bc0ff1169c145` | 0 |
| external/lvgl/src/libs/gltf/gltf_view/assets/lv_gltf_view_shader.h | 780 | `38a98d33a2fba8d0a354bcb931502f2678f7ba37c0554a4a5c142a2556b4c2e6` | 0 |
| external/lvgl/src/libs/gltf/gltf_view/ibl/lv_gltf_ibl_sampler.c | 25041 | `52339f357a11111ecba219bd433cb63ef1a5b9d4b80d026a8733ba6d6d8b7020` | 0 |
| external/lvgl/src/libs/gltf/gltf_view/ibl/lv_gltf_ibl_sampler.h | 1964 | `8ddfdcc743f8185a40e6bbd462b49fef11e449dcedc79ff98b1f2cf66ba41741` | 0 |
| external/lvgl/src/libs/gltf/gltf_view/lv_gltf.h | 9625 | `6e3bcb8bd3aad0fc6ff958a719a8b9cec12482792c6265ee46135f8e165cfb1b` | 0 |
| external/lvgl/src/libs/gltf/gltf_view/lv_gltf_view.cpp | 21537 | `df3f99796774ed479e41795f4f262a9c36c8297fee4fb2b6bc556cfa2abcd846` | 0 |
| external/lvgl/src/libs/gltf/gltf_view/lv_gltf_view_internal.h | 3782 | `e91e0accc449dbe2220d43716ee1142012e99f5835296c90e31951432b4b86fa` | 0 |
| external/lvgl/src/libs/gltf/gltf_view/lv_gltf_view_render.cpp | 62146 | `1c69e645f754faf3f2e682c9891c85322d56db8b0e497b6ad9c542510d92348e` | 0 |
| external/lvgl/src/libs/gltf/gltf_view/lv_gltf_view_shader.cpp | 17453 | `31b03114051e74d7ba377c15fcb5428bf75927ac05c717f127225ee83af1c95f` | 0 |
| external/lvgl/src/libs/gltf/math/lv_gltf_math.cpp | 2025 | `871294c14d234ec44db0fc08dad80835ccac867ee3e68121308f8e4be6e597f1` | 0 |
| external/lvgl/src/libs/gltf/math/lv_gltf_math.hpp | 2399 | `838f98e47f3f428b8d0a4016fa8661383072816a65a7f9051e4d7d1e2a2f9e9e` | 0 |
| external/lvgl/src/libs/gltf/stb_image/stb_image.h | 303477 | `d81d95287ae188e472fe66ddcad8635041e8f29d51a799cc77c65c6e94400f1c` | 0 |
| external/lvgl/src/libs/gstreamer/lv_gstreamer.c | 20893 | `3f65c28ff411cf0ba0f0855f2af83afda1398da617ed05e4539a68cdba49c88d` | 0 |
| external/lvgl/src/libs/gstreamer/lv_gstreamer.h | 5789 | `3e8f33004b0731521ca947edd3d3a1642ef3466b020959424269ac451aff410b` | 0 |
| external/lvgl/src/libs/gstreamer/lv_gstreamer_internal.h | 1329 | `ac63d83ff7c18b145aaaa52e43c3689c0965d25204efa9a2038f78f7a9d11ec6` | 0 |
| external/lvgl/src/libs/libjpeg_turbo/lv_libjpeg_turbo.c | 20209 | `37ae6afdbbe1b84009b5353ab08a6ca5f3b387e49c0ae500159c5e8230b04f66` | 0 |
| external/lvgl/src/libs/libjpeg_turbo/lv_libjpeg_turbo.h | 770 | `dda5ec8e9b10055a313d0755c26d85f405e3c16937ef16b06542ebf5dc6d5be2` | 0 |
| external/lvgl/src/libs/libpng/lv_libpng.c | 9807 | `f500b381fb5c6877c6fc3fe9cc7057d6d8e1270e834ac4918f92aaf4c9eb1d36` | 0 |
| external/lvgl/src/libs/libpng/lv_libpng.h | 707 | `f70a2a12727f3ef27521527bf4fef42b4e1526bf772932d86bbd66cec4d180c5` | 0 |
| external/lvgl/src/libs/lodepng/lodepng.c | 328422 | `d8356d63aaf018f50eefea3153c37c969cada4490761736afb3a55a1d744cd7c` | 0 |
| external/lvgl/src/libs/lodepng/lodepng.h | 104022 | `9c5db08ee60e791b0d74e1a1d2f5e4fe9310d5eace2647197068556fd791fb2b` | 0 |
| external/lvgl/src/libs/lodepng/lv_lodepng.c | 8826 | `845fd3b2529cf2040850e1c74b7bd7f1f30a7c0856530a0c19345f2521a5c788` | 0 |
| external/lvgl/src/libs/lodepng/lv_lodepng.h | 715 | `6595eb11cdc6ae9f22dbee944e19aebca9660e600cd20116da6929d0d8e5ac0c` | 0 |
| external/lvgl/src/libs/lz4/lz4.c | 118248 | `dde3a9c6bbef76d82040fc1baa66debe539472cbd7c532108aa443cfb57ad0c6` | 0 |
| external/lvgl/src/libs/lz4/lz4.h | 46282 | `7797c082c6b10de6aa2ef0d0671c205c4067db848612fd39fabc5e71f168984d` | 0 |
| external/lvgl/src/libs/qrcode/lv_qrcode.c | 8097 | `34677f81ee2af29e8e3df7a301aeeb9068c7b64b57fa46c63365329fea001d83` | 0 |
| external/lvgl/src/libs/qrcode/lv_qrcode.h | 2403 | `42ef852423757d5c90d449fe8ac74ba9b313480a5cc3ce8e2dbe3c71e1f79183` | 0 |
| external/lvgl/src/libs/qrcode/lv_qrcode_private.h | 817 | `9e2fd66f3c30b9c85536a86f1e37beeaeeefe979e56a0e4f2312b710873b1e4c` | 0 |
| external/lvgl/src/libs/qrcode/qrcodegen.c | 45011 | `53158b9b2dce1ff635e0279ddae975b07fa8d1c57d4ec2445abe12b8bca20f56` | 0 |
| external/lvgl/src/libs/qrcode/qrcodegen.h | 14758 | `2acb64b7c97e947726bab18f7fd1273a26f4435f90484ecd5cc9d6111d1e9cca` | 0 |
| external/lvgl/src/libs/rle/lv_rle.c | 2839 | `78a35fa1f874f09d3cff77a4d8be3d0a4001dd2d083f064bc46f3931e074e20e` | 0 |
| external/lvgl/src/libs/rle/lv_rle.h | 771 | `27ec8477769453a02191aebcc7e7dac2bd594cccf3824ae56ff226809b9c6815` | 0 |
| external/lvgl/src/libs/rlottie/lv_rlottie.c | 7400 | `d87a78f044b321cb0c643930850538a4936ef2ade43bbd5045eaea8920374ca0` | 0 |
| external/lvgl/src/libs/rlottie/lv_rlottie.h | 1346 | `f26327195f2b8187641ba5b8a1295fb5702ec76343d6886ff856811e691b27ff` | 0 |
| external/lvgl/src/libs/rlottie/lv_rlottie_private.h | 1106 | `b986fff3bf79804ba9a63dacb5a1af4e92cb09a1d7c1a62f36efcb589aa456a8` | 0 |
| external/lvgl/src/libs/svg/lv_svg.c | 3130 | `43cf51298d750f76cbd3ad237d8017d650a2e0bd02c294b90463ada98445c118` | 0 |
| external/lvgl/src/libs/svg/lv_svg.h | 8021 | `1f40e9111068dca437f4509bf54223f15cd3cb0992991fce337bc2f0dd679c27` | 0 |
| external/lvgl/src/libs/svg/lv_svg_decoder.c | 11780 | `1a792ea775d3ee51f5435a5e43f3c7a32e3be5015514bc7812c0beb6b5751b22` | 0 |
| external/lvgl/src/libs/svg/lv_svg_decoder.h | 772 | `a5cdddb04bac4ebad9670a676d85fbc0d1dccf5cea7b2db0571c77dbb10f33f0` | 0 |
| external/lvgl/src/libs/svg/lv_svg_parser.c | 80306 | `30aad4a3108dd3928ddb7d8e7a3335dcdc4031a6780b7036c35cbe4dfbb18e7b` | 0 |
| external/lvgl/src/libs/svg/lv_svg_parser.h | 1870 | `5f968f8027809be567f2f1e9dc9102eb3d68d35fccaee2c3dd42bd615128c580` | 0 |
| external/lvgl/src/libs/svg/lv_svg_render.c | 87409 | `dcf991ed266e47de977076210c0c2ba9e1fddd0fe04bbc6adc933e91937df731` | 0 |
| external/lvgl/src/libs/svg/lv_svg_render.h | 3848 | `6d2038840a7e1364718d5904627cfe96ce426f048ed20a88d653aece7c936179` | 0 |
| external/lvgl/src/libs/svg/lv_svg_token.c | 15638 | `1eca40e7a44167d4729048a13e076a4267830134f8eed79c1dce866e794e32cb` | 0 |
| external/lvgl/src/libs/svg/lv_svg_token.h | 1581 | `51fb0383f2a1b7911101f8aa870191c817e8d3ea3dd6b7af7ad7d1a94e244c3e` | 0 |
| external/lvgl/src/libs/thorvg/config.h | 448 | `d539475746af7f9a73cdc8231a923d065df59cb3728baceddf8866bbb3054e2b` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/allocators.h | 22744 | `beec8171ae738ed7b9e7cba42eaca945d285e5da6117c06bfe11912554bbdc2d` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/cursorstreamwrapper.h | 2260 | `9e619d9a57c2fdf51e89e422668d6fe3065cf227a66261ac2519f1870398fe39` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/document.h | 133685 | `92995df5ea1a67400fe3dd649ac3a5fdf97ddef17005f4f933b242f4f830c0c6` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/encodedstream.h | 10641 | `9f966d81e21540888470fe0901b2ba9026b0b662dd29f76f741bafaa9d9c3358` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/encodings.h | 29240 | `766732e0d0f4e08c7667371b3e9e2f172b0d7c35f6501651bc9c35cbaad0a692` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/error/en.h | 13025 | `3cc7a00f9252b1183f3a108a9c7ceed59e408cd7b5a04f4c202a66a84a0fb578` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/error/error.h | 13353 | `648743428973469227f6b419f80a979809c33bb8d66c409c8f3775f4f7381121` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/filereadstream.h | 2974 | `6427374b5f814840d47f7646b5eefcc3286323922713924d0c2aeea4237d1c30` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/filewritestream.h | 3119 | `eab610840c5d225ad29aa6bb1885c6cd612be8555fd00125bd2186dbf68b7107` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/fwd.h | 4007 | `05043f27ea8a2cc773671d90ca80d4d5c2024dfdffcc85b3fe67fd0367c41dcd` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/internal/biginteger.h | 9252 | `76fc3ac1eeb1308228abd834cb01c8b297318668bcffdb5df404c25e0e34497d` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/internal/clzll.h | 2045 | `4ca3e63eaae4c67b049e8a6cbb532182e1d9c9023b7d992c556fcab0c2f4c045` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/internal/diyfp.h | 11580 | `b1c63c28dec8f82f7fdc2a39193d7a09a4c30343c3f008f060adc70e710e0a32` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/internal/dtoa.h | 8469 | `839551a35826b5cf2a5289cee282714882ed4ba97b30e9c9f1e2f73a51514038` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/internal/ieee754.h | 2969 | `3eab1c7d0b052c81bb66fbce3186b3a67851fbd2bc2bbf2b635dc6bee656fe34` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/internal/itoa.h | 10110 | `a0f965f33b11ce112b7bf2fbdeaf5338fca174e33f9f47608ccdd6d8559f3871` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/internal/meta.h | 6616 | `fbc1e3fa746a68a60bf236a922e19ecdf9572b814164f198e810334a1826aa05` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/internal/pow10.h | 3567 | `b8bf6bd27304d9d38f4cda49f249de0d3b97e4226e8dcdd04f75c473380b50e8` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/internal/regex.h | 26102 | `e7f64e62a005f74661a1d63a09672d870d39914bc4a2f165b4165338020a10cc` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/internal/stack.h | 7157 | `8b7efceeef0a0721ac98965ab6bef6c8507b0d0fcd205e35e0eec84e42cffb03` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/internal/strfunc.h | 2721 | `6ee8658c852b9c076e1893425d718cdca4089948b7c6b91e3653c1b407e431ad` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/internal/strtod.h | 9032 | `0638724ffa4198da3678dba1457cb4abfe36b48d8be78132822af0946e6c111f` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/internal/swap.h | 1398 | `72acfabebd33f44869e7724603e57744da33337998b32443b66eaba58d2bbbfd` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/istreamwrapper.h | 4051 | `e11984b1ab67d74d87dfcd478bc1059e67720ab2d0de6e8fb57c55e2e053bdc6` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/memorybuffer.h | 2534 | `87d8c876554e50698a3e9f3cac49896d4b1f15eb814e279d01b2bb79f3aa3e1c` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/memorystream.h | 2642 | `9bf7c6bd1a657f48ba53c386f6dd116c1d5d8471d04c92216680bcd979fe6aad` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/msinttypes/inttypes.h | 8361 | `f95f632862138ad569a6e3adc431d867e6fb5ee5f8cf23e8cd1e942a1fd1fc55` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/msinttypes/stdint.h | 9375 | `c3f7d184f187b82c617134170bf9a02c3233413cb3bfc0ee4aa363055464886d` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/ostreamwrapper.h | 2303 | `1f0c6cdebf9a4e31c53e59091c411e359e6e2c504790eafe55680a4ff98e0efa` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/pointer.h | 63123 | `113861bc59a7a273e22299305a16cb3600c0eaa5dd1d7554a30213c54b8f8bcc` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/prettywriter.h | 10504 | `27ae70723851da686c9a829f8404fa2e18e787eab9dfee16fe43303d8a2faa68` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/rapidjson.h | 25613 | `a5d7f757ee6ecbd8834fdf532096a5762deb568a16d8b0284ea2b55666141842` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/reader.h | 94332 | `214ba7447b544217dd005020010fdcf5241ac7866607b94704bfe1642720a5ed` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/schema.h | 146749 | `fb800528abcbe0fc44f343d111267b3383edf85fb0a328d3b671d3d72b4862a7` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/stream.h | 6732 | `a3708a941a130a5679d2302368169852e5c4ca5f54758ea0e94caf61615c8ae0` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/stringbuffer.h | 3968 | `5f01edff23eb9f98997a766e12873e23afa205fdd20a8cf2bebfcb8665737fec` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/uri.h | 19752 | `53d200ad6eae23399fab31687c50511b3a14cd32c0a36900151f34ea0bf4cde9` | 0 |
| external/lvgl/src/libs/thorvg/rapidjson/writer.h | 26817 | `8b27f983418c95d36c24d484c3271129980f0db91a50193fac206bf40d65ec33` | 0 |
| external/lvgl/src/libs/thorvg/thorvg.h | 86121 | `dc8b6c756ca7478ae5e1164806c15b934d7fce88fc7df38c797383648becf609` | 0 |
| external/lvgl/src/libs/thorvg/thorvg_capi.h | 103534 | `bcd1ea248bf5741bd47fa398bfb957b9363147167f3a754dcc55fa844708ceb6` | 0 |
| external/lvgl/src/libs/thorvg/thorvg_lottie.h | 2819 | `b01f57cb6924bf0372aba3b88bd3136ba70a50631a23eeea372d194c47efc0be` | 0 |
| external/lvgl/src/libs/thorvg/tvgAccessor.cpp | 3450 | `20bb66760a7527a6f5b817734332b9f864004b0f867fd00e4072954602498e16` | 0 |
| external/lvgl/src/libs/thorvg/tvgAnimation.cpp | 3822 | `7dc4b0e0cbf09805b210b837450a0d0b1ca1350704e8719507124b69b1d2ae67` | 0 |
| external/lvgl/src/libs/thorvg/tvgAnimation.h | 1655 | `d821663d63749dd59b05e0db38df5be2b2fc4ee09619b06c6f6bd8b6579f226a` | 0 |
| external/lvgl/src/libs/thorvg/tvgArray.h | 4495 | `1e2a12674188c91449cf5c29cb101d6c532a6be38542cec859904c4b055bf29e` | 0 |
| external/lvgl/src/libs/thorvg/tvgBinaryDesc.h | 4652 | `4bf27031f659f6b4b5e5c6541c91909f0ae3c76f078ee577feaebb6ca784cd50` | 0 |
| external/lvgl/src/libs/thorvg/tvgCanvas.cpp | 2679 | `dcb0c08007fc51c70b2a5d599112ec890cfa9fc3b8d692c47a0ab6ada9ac4aa8` | 0 |
| external/lvgl/src/libs/thorvg/tvgCanvas.h | 4791 | `0506c718bf3b9d2cc1bd9b7c89c093445f53e86b398b455865d78dc549ef9587` | 0 |
| external/lvgl/src/libs/thorvg/tvgCapi.cpp | 31533 | `b09a98b36c20c249969fc438459722e06cbc08f85e3227429f7e00005975738a` | 0 |
| external/lvgl/src/libs/thorvg/tvgCommon.h | 3332 | `b11e439af5c6e9f271233838f79d05e6737957b9ea0899a826be1a423415efc9` | 0 |
| external/lvgl/src/libs/thorvg/tvgCompressor.cpp | 16779 | `fdda523535dd439cf6a77c3d07617284b5748869ded64901eaaa5df467d9b04f` | 0 |
| external/lvgl/src/libs/thorvg/tvgCompressor.h | 1784 | `032d5b75a7a462d6e1ba6c1621fd6ab05bfa5cdffa1521e8fe51cce10c948ab2` | 0 |
| external/lvgl/src/libs/thorvg/tvgFill.cpp | 5983 | `6cc53f7873993fca46b9a35c0db18baea8cc0dc7f150fc9ee6803160b4fafd79` | 0 |
| external/lvgl/src/libs/thorvg/tvgFill.h | 3086 | `0f46a71ac80432069a19cf765001981c38080c071a9399dfb39ac3d96986a786` | 0 |
| external/lvgl/src/libs/thorvg/tvgFrameModule.h | 2200 | `7a7472c9c8785db5b4c0fb35e12887cafd8d657b3127cf8efe051e4bbd07576f` | 0 |
| external/lvgl/src/libs/thorvg/tvgGlCanvas.cpp | 3130 | `e51a00346f19e5fc867cb59dde1618756e9d2dcfe3c53091000a240c5df3033f` | 0 |
| external/lvgl/src/libs/thorvg/tvgInitializer.cpp | 5303 | `c7c15aee550dc8335f8fcb82f878c0af536771247709de41540693f42fa70d19` | 0 |
| external/lvgl/src/libs/thorvg/tvgInlist.h | 3016 | `ccf3172650aa2d63f5504f9c3b9270276ce9e8ee4cf4da3fd69346a6a12836f4` | 0 |
| external/lvgl/src/libs/thorvg/tvgIteratorAccessor.h | 1576 | `db767a17cfdef2319d65ed0c0a59c51db7aef40b6f37ed81ff8147e66143e009` | 0 |
| external/lvgl/src/libs/thorvg/tvgLoadModule.h | 3366 | `8fc4fddf59a69e5e2ed3eef709aadf30d909125290ef639f640b8e546f53d7af` | 0 |
| external/lvgl/src/libs/thorvg/tvgLoader.cpp | 12712 | `9643c50315a0b8506fa7c9d1dffa35c03a17d649c126f06167f7c30cf38d15fc` | 0 |
| external/lvgl/src/libs/thorvg/tvgLoader.h | 1929 | `217e76a4c56506d0544f22df1697a1541985e91ca08815192d81d039b070d96e` | 0 |
| external/lvgl/src/libs/thorvg/tvgLock.h | 2000 | `0674f716557079ee1c8e291a275a2f931534deaf32c5ee639aa1a702ef784ec9` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieAnimation.cpp | 3148 | `1de32d5a682fc93764bc1eaaf5a4f21dc9e39aef2628610185f3f8ef0cb80471` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieBuilder.cpp | 55376 | `ce7f5bdb1c56b8b7775e850a9f8a53134a1fbf95caf74478c8d3983907745954` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieBuilder.h | 6125 | `e4da96de4cb4d75cd9d8414e8fa091511f824d0374ac75a446aa8f31aa8d2bc6` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieCommon.h | 2625 | `50461b091c5232763eccaade09fe3031f02e8a232a667f8c73e2e0f1fc13e9c4` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieExpressions.cpp | 47947 | `f1c9ed921af36723b37f92fc735195914ed2563b9e84745e351d8a9127e72261` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieExpressions.h | 6562 | `4787a484c7c019d75eb2bf8b1b089a36c66d8f0206f77d06947a859f7bcf7c65` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieInterpolator.cpp | 5356 | `dabf651e523b942def00b10665781d7fe468a9011734c87c12b9fbde054c352d` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieInterpolator.h | 1843 | `763f0fa122b01f321ec6a0b3fa3464ed648900b97ec3ba8abc24d0df645c55c6` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieLoader.cpp | 10039 | `a2205417a99159929d948617626f81309d4c8245390274dc8c9b51670bfe3481` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieLoader.h | 2967 | `35bdf6f88caacaa2a832c13b50efc8954ea8f423ee6298456f271462a20ffd6c` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieModel.cpp | 16905 | `570ac58d20a322a52f03b32e84d66ed1ea7c9a49ac972b578d669ea8f4e3b686` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieModel.h | 22235 | `933df7149486e97889e8ad09ee44a8f06165af0968036e151f54481d9f79bdee` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieModifier.cpp | 15849 | `e39ef19e0ff242c409c17a1c09a32ce7c44d6ed275b65348bcd36ae7f09e941e` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieModifier.h | 3284 | `071587d6a2b0ebaefba575e442bc139bf56c468c8d8f082c0a7fcca55404489b` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieParser.cpp | 47104 | `b514a38427623477d3d65fc2d3ebc1d30c24c435eb62700822d3b2ece20b3501` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieParser.h | 5050 | `ff8dc6f949c6cf510ca6e67f556fe02942654af76a71887f4ef25ffc5def3e5f` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieParserHandler.cpp | 6450 | `68b6cd4070b83a01ffb6e6effa9a45be3ce40188fc7d7f8720c0938c53ec5e75` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieParserHandler.h | 5217 | `58b90961e2ab3c7ab86c8602b5b3597ac9dfe84e70c724fd2d8e80f126bdf59d` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieProperty.h | 25046 | `7b112d5526410e199fe97fda8deca9e1cc286a5b5bb1f2602d7f1a03f2fd9987` | 0 |
| external/lvgl/src/libs/thorvg/tvgLottieRenderPooler.h | 2052 | `d38bbccdfe62c00d1b754a59095db0cc566721cf757fa56f999698bf21862018` | 0 |
| external/lvgl/src/libs/thorvg/tvgMath.cpp | 11055 | `d7a6297f6be4de2e14da2f50243badccf3ff1ff2336cfff06cce98219c2a5a7c` | 0 |
| external/lvgl/src/libs/thorvg/tvgMath.h | 7507 | `2862fc814ddf890644c792c0aa6c0582a6bd8f51d58e74832fc809dcfcf31fdf` | 0 |
| external/lvgl/src/libs/thorvg/tvgPaint.cpp | 15670 | `5fe8fe698636a4aed439d2c3184739283c39e603cb572d962c48de3570612e7f` | 0 |
| external/lvgl/src/libs/thorvg/tvgPaint.h | 6054 | `10754172acdf8bde978e6549b9237cef6964ec019ce50f9087cf3be7e1b66597` | 0 |
| external/lvgl/src/libs/thorvg/tvgPicture.cpp | 6109 | `696a14aa2b7ca8d51a229eecaf948a7f274f586964f0721dedcf6a74972af415` | 0 |
| external/lvgl/src/libs/thorvg/tvgPicture.h | 6013 | `d16599837916dab26457f3a6ffe1b8ef5c80634cac6acb535c8c3eef4e11b8e4` | 0 |
| external/lvgl/src/libs/thorvg/tvgRawLoader.cpp | 2758 | `4d7c42aa94e4e8d4161f76d83ca5a0b91bbfd24c7c9a03c966152bd08f3c7aef` | 0 |
| external/lvgl/src/libs/thorvg/tvgRawLoader.h | 1570 | `41f9c37fdd3a41ec04e43f5452fc0a1fe3040795611276ea892010120093c172` | 0 |
| external/lvgl/src/libs/thorvg/tvgRender.cpp | 2567 | `832d2ce7ea01bcc7d514a7e2d5b53b9c8912ce28d855e6919de36e305bb9b51a` | 0 |
| external/lvgl/src/libs/thorvg/tvgRender.h | 12125 | `874267a7e5d4c0273a02ec8811333bbd7468747df34eb6678fc89e3185b53a40` | 0 |
| external/lvgl/src/libs/thorvg/tvgSaveModule.h | 1668 | `52928fe8c921eb4d17d59348c394c01b634e807adf16b33cc05ed1b158df6189` | 0 |
| external/lvgl/src/libs/thorvg/tvgSaver.cpp | 5403 | `ccd3924404d6a37dfa7b8708d17e05e2737714920e9421f2902290b373adc341` | 0 |
| external/lvgl/src/libs/thorvg/tvgScene.cpp | 3356 | `a2056d58518bda25238c98af68a402fb6f9db2c3353864c8815b847daa83beb5` | 0 |
| external/lvgl/src/libs/thorvg/tvgScene.h | 7712 | `ed43c44978864bb328a7f71cadd2ca4bc3ce22e44b290802b6b7e84e1a13ae62` | 0 |
| external/lvgl/src/libs/thorvg/tvgShape.cpp | 10750 | `8a37b73dfb50b5a399fc0955d04b3a92f0eceef092cda9febb3d1eab7c397e53` | 0 |
| external/lvgl/src/libs/thorvg/tvgShape.h | 12434 | `72155f4a3640ad52da34e5832c5162e601ec3f7c9757847168acf1b451a66eb6` | 0 |
| external/lvgl/src/libs/thorvg/tvgStr.cpp | 7261 | `87d9bcf1471140568ba660a317518ff4a843b6b21ac3b415eb4325a055e02dc0` | 0 |
| external/lvgl/src/libs/thorvg/tvgStr.h | 1661 | `1978f13a077bb9b8c0db59fd4daf7d9bc49ebdc8fcf6dfe0c3513e04b04b9d61` | 0 |
| external/lvgl/src/libs/thorvg/tvgSvgCssStyle.cpp | 12645 | `43d168cb860e3ec22824ff7a68e5e4f3a43d13dc50280d2fbc0552a97c5f2135` | 0 |
| external/lvgl/src/libs/thorvg/tvgSvgCssStyle.h | 1719 | `8b2f71217c9d5ab67ebadab065ffa269b2d1efc5fb106b803793f2702e040b19` | 0 |
| external/lvgl/src/libs/thorvg/tvgSvgLoader.cpp | 138351 | `0131b47d7545e9fcc3693c0e3941b3932f3ac001233bd14ba76ff617e2046949` | 0 |
| external/lvgl/src/libs/thorvg/tvgSvgLoader.h | 2298 | `b14b28ede797f3d39c510cccac1133ef82c027906497b0fccdb47d50ce7c6451` | 0 |
| external/lvgl/src/libs/thorvg/tvgSvgLoaderCommon.h | 10682 | `4307b541a80af9e5d32e816faa9cab00b7ccaf79e1e85fdc970b1b37f1355f7d` | 0 |
| external/lvgl/src/libs/thorvg/tvgSvgPath.cpp | 17766 | `0e1f3a5c9124457e6e832d0000ed02e5dbb2c5d70a8d6db1e9f691289a556659` | 0 |
| external/lvgl/src/libs/thorvg/tvgSvgPath.h | 1407 | `82d3d33c6a0cdc4a5f8a6ad7b38937608a147ebb171543c50f74e342c769745c` | 0 |
| external/lvgl/src/libs/thorvg/tvgSvgSceneBuilder.cpp | 36622 | `3d6027f4c0e769ea9b80fb5b8d63de04f3d3b71bcf95e61bad0ca3e6bcbda022` | 0 |
| external/lvgl/src/libs/thorvg/tvgSvgSceneBuilder.h | 1560 | `3caed8c5dcf2b91204cfe52aa1b0be9ae4305a544e8e8df3b7307f05ffdaf0b8` | 0 |
| external/lvgl/src/libs/thorvg/tvgSvgUtil.cpp | 2628 | `fbb5e747121684eadd2e8129f6596779e453d3205e758b54a28be35a006e4fc3` | 0 |
| external/lvgl/src/libs/thorvg/tvgSvgUtil.h | 1405 | `77749b1016c3e3d6fa81c034fe7b60ce54fec5f15147ca2c5d4345d1badba612` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwCanvas.cpp | 3962 | `fd90edcdace547b6deca32f04f00e8ad88f2dd11b84f8528c458e8e45aec45b9` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwCommon.h | 20273 | `662df4788c7f0ccbe63e4688d2e98260daa203b8b95463632efabf33973242b2` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwFill.cpp | 31658 | `eb03a7cef708ff4c518323db0800b35b102dad7cf5a821a038d61e5125aa6818` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwImage.cpp | 4290 | `86405ea251d00072fa91ce6a984b0292b675cc1326e8adc54735ba5f20e7311e` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwMath.cpp | 9042 | `4a40115be3e1d3fbb7e2c5540dec2b6111d6577e843d5cd7c4cd22c4bbc3154c` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwMemPool.cpp | 4221 | `85b9a4ae8356eed9891ae5ddd802ad51df5f58a0121002410d9be3a9a1315fad` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwPostEffect.cpp | 7348 | `45e5a1682fa57f5c64e5b2331b9d72c44b5609c63b4250e2652a27bdd08baf4a` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwRaster.cpp | 71214 | `17ff3ec3e855193e8b99e65efebbafedae300a1c2da47b16d0f6b15754649c67` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwRasterAvx.h | 8865 | `ee0978343463edc33a365f698d71a0377e1e9c2288831a85424937c440c36c60` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwRasterC.h | 6166 | `70ef91c9508f1e807445399a833c120245f82ee86bf03518f85a094b1654a682` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwRasterNeon.h | 6733 | `f56d712270a0cfce3aaf194b6deaad597d6d9167152b7528a6d58a2872c41166` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwRasterTexmap.h | 39642 | `bb97202102161e8e4ae9357d18be491b5d937087ae0a194d122569e4056aabfc` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwRenderer.cpp | 22607 | `61f0d5a60e89b202be8d575a89da154ecc998af88d3efaa41c8485ffab63d9ce` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwRenderer.h | 3701 | `25afe63e4e4017d186d3d25927b1b68e1ae1089582b80240b4c2e81223d9493f` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwRle.cpp | 32280 | `1a9690a1a4844ce9b80a9498c54a809db7eb554588bb13f0aca9f62f696fcb22` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwShape.cpp | 21083 | `916559b8ee01407841810f50ae72bb3cc5da06d817e9ea9d674f9ef425cc9d89` | 0 |
| external/lvgl/src/libs/thorvg/tvgSwStroke.cpp | 28271 | `55ef4b306ef7db69435dee427f2b3aab7b196ea91a5c52b4f1a49259d2394d88` | 0 |
| external/lvgl/src/libs/thorvg/tvgTaskScheduler.cpp | 5897 | `8ca1f330f1a2d88c3499bbb2a55d40cdc7c2344dc1abff7e3b0911f311a8cf09` | 0 |
| external/lvgl/src/libs/thorvg/tvgTaskScheduler.h | 2918 | `d8ef0c805cd1a972573b5b89c7dbe242442a4cb6790465f15bc2878fd46483b2` | 0 |
| external/lvgl/src/libs/thorvg/tvgText.cpp | 3249 | `ec8553d3790fccb9aa39d98c67e765387fd2a47ef82c73e2e74f1137e21deb5b` | 0 |
| external/lvgl/src/libs/thorvg/tvgText.h | 5284 | `5259fba506b348e93d5136adb034352af0d961aee6862bc07acbc6e0d8aabb43` | 0 |
| external/lvgl/src/libs/thorvg/tvgWgCanvas.cpp | 3291 | `a90ef1245442f861ba0baef2bfa53d197938f5a0932a67ac11fae5e7a7d45b18` | 0 |
| external/lvgl/src/libs/thorvg/tvgXmlParser.cpp | 18538 | `766eeefd0730869b582f1c8a2579586eaa51aa2f4109192aa2891de46395cada` | 0 |
| external/lvgl/src/libs/thorvg/tvgXmlParser.h | 2989 | `741daffc46056927f4d63daeb131bd23a7a13e51b5e9e602b77b9058b68867ff` | 0 |
| external/lvgl/src/libs/tiny_ttf/lv_tiny_ttf.c | 24232 | `ba5b184fa1e9a7826c4ad84eae868bac95cf27c0657802197fdc831c43e9cfb6` | 0 |
| external/lvgl/src/libs/tiny_ttf/lv_tiny_ttf.h | 3048 | `b74742be3f172e9f5826791ca02d5fdad2b7a5423e17c356c09e85536a60832b` | 0 |
| external/lvgl/src/libs/tiny_ttf/stb_rect_pack.h | 21136 | `a77b5e58de68d892c0c880ff62f6de7a7a669503cf04fa6cd0af7492e149c413` | 0 |
| external/lvgl/src/libs/tiny_ttf/stb_truetype_htcw.h | 228103 | `bf989936a0e69b53b455e583b583d0bffb6feaaa72b8c2a05af4bacfef7c6ed9` | 0 |
| external/lvgl/src/libs/tjpgd/lv_tjpgd.c | 9608 | `e86658188441209ca9512c1025080e18dc7c4556a5a2e825ecf5878e2ec0c1f6` | 0 |
| external/lvgl/src/libs/tjpgd/lv_tjpgd.h | 595 | `602b5d249967fe2a489c04eed922f35d3389fc9188a2d2839d5c230c87078d6d` | 0 |
| external/lvgl/src/libs/tjpgd/tjpgd.c | 48709 | `869f12918ddd795c97ac36c281683fc3f18c81b9e0279c6219f8bbe70c03a26a` | 0 |
| external/lvgl/src/libs/tjpgd/tjpgd.h | 4056 | `7f768047e0b1947cd1eb55e29890137645042bfdb03fdcb56634ad7df8224d66` | 0 |
| external/lvgl/src/libs/tjpgd/tjpgdcnf.h | 865 | `ca1d5bc5fd41f3800238c56ea4322d5c0824df4e5fce5eb47ef9989cdf00728e` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLite/Series/gc255/0x40A/vg_lite_options.h | 4831 | `67ee639e90fba4fcc9feb3c8a6ebe6a082ff12358e74b6e70ad6564ff3224097` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLite/Series/gc355/0x0_1215/vg_lite_options.h | 5621 | `bc15d52c0a3565d6ac273d457c814898914274c25b5d6b77755c80e5a2b4d2ad` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLite/Series/gc355/0x0_1216/vg_lite_options.h | 5621 | `98661466f2adb3ad1a1b16c188646beb9326f36cc6c218f9f0aa7d176d1146bc` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLite/Series/gc555/0x423/vg_lite_options.h | 4908 | `99a3f53c25cf1c98d5965d8fb7349ac34c7af5a9decb76ee3578e366f62dbd95` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLite/Series/gc555/0x423_ECO/vg_lite_options.h | 4901 | `4fa0c4e37a5bee7c168c50921bb95ec01a2dca6102384a828b9811d7ea36acfd` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLite/vg_lite.c | 246765 | `245267ce41526aa7452c8b17851c89c2c87b3e0dc40e37f2f76901b08fd1f9d0` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLite/vg_lite_context.h | 14042 | `64139ce95bd81c3a8e567cd1f0362d5c69a5556a499fb2abd73d78789e9192cb` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLite/vg_lite_image.c | 68825 | `646f96defc01df2ac023e7c902dd133b66907fe6e5e443142ea5e1436d5510c6` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLite/vg_lite_matrix.c | 4999 | `3b6cbde78015e7c2c2fe3b996d792b483ceb16ce3117bdde38a9017f14ee4625` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLite/vg_lite_options.h | 1813 | `d6c23a205d4b54f1ae122c944887126c2d8094a99af3100a75fbea3c73a8f7af` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLite/vg_lite_path.c | 222940 | `af08fc671e7baea596b739870223ee5ca877b2173684ce7c5f39c040b6fdd040` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLite/vg_lite_stroke.c | 189186 | `95257167e183aead7b0cb3f8d75b8b6309ff50cf1c2f4bb5a14f0ff39831e828` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLiteKernel/vg_lite_debug.h | 2508 | `6682e2d4f26c927280062c62252355df15bf8bf2a199827bb0e5496c76637454` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLiteKernel/vg_lite_hal.h | 11755 | `9ec83334f5a6743b89d9e9ca380dab7584baeed30200eb801dfea67d5f35e0a1` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLiteKernel/vg_lite_hw.h | 3881 | `ce106316f44e43875e4521c3ff44e010fd2a77ecb3ee234ff80e8d77054aa944` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLiteKernel/vg_lite_kernel.c | 47635 | `75ed772288fda564830824d3c69cb05b173821e787dccad756500059244bf07f` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLiteKernel/vg_lite_kernel.h | 15987 | `cf0896b5db723112cd8f640cd44a72af299ef864234bc02c3dc2a13ebbc8eb04` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLiteKernel/vg_lite_option.h | 4612 | `1276d8cdaba15a74dc6eff5ff0433d6a2c4653031f39cc5892fd0beb1eaa4ca7` | 0 |
| external/lvgl/src/libs/vg_lite_driver/VGLiteKernel/vg_lite_type.h | 2796 | `00e2bff15f1fea0b52ed87d41914636ac60680c48b245c1c58f543f95f8ed461` | 0 |
| external/lvgl/src/libs/vg_lite_driver/inc/vg_lite.h | 72778 | `0215eb21202ca3d9e90d357e3ceec9843bf449b848619901f744d717070af94b` | 0 |
| external/lvgl/src/libs/vg_lite_driver/lv_vg_lite_hal/lv_vg_lite_hal.c | 16309 | `6fcfc96c0f00ccd096c87bbb4c96b54647a3556e6672e797268c7d7bc6024251` | 0 |
| external/lvgl/src/libs/vg_lite_driver/lv_vg_lite_hal/vg_lite_os.c | 236 | `61b5263ff7fbd585a7c44d9b83dfe98c30d8cdb51303e25b5cd6bf08b78be1b0` | 0 |
| external/lvgl/src/libs/vg_lite_driver/lv_vg_lite_hal/vg_lite_platform.h | 1220 | `e50e57ab2a556889cabd8eb1a627883d5577686028a967ba08203013787c2eb2` | 0 |
| external/lvgl/src/lv_api_map_v8.h | 14790 | `8b6659fbe747dee915425404cdf2a4e1f9e883e6927f28752a8c228a4194a7a8` | 0 |
| external/lvgl/src/lv_api_map_v9_0.h | 1718 | `d31e9ac2965968328225aba92614d349fca2c9fa0d378ea3ea766d55b31e290f` | 0 |
| external/lvgl/src/lv_api_map_v9_1.h | 4151 | `ec57f2c537290de6df954bfc8cf31b9f2a28d8cd83137eaebc3b377066424596` | 0 |
| external/lvgl/src/lv_api_map_v9_2.h | 1720 | `63216986c429213255b37d857cfc6ca162aef71dd87ac920418609e88afe430c` | 0 |
| external/lvgl/src/lv_api_map_v9_3.h | 5094 | `e6739cccd0c255aa460478544c9bff7d6cde89ce0a4cd9be7836fdbba703f471` | 0 |
| external/lvgl/src/lv_conf_internal.h | 154141 | `300c93bd1db6543af213c2a614e4f09ecd1742c945d18b7bc6b20cec0a237d58` | 0 |
| external/lvgl/src/lv_conf_kconfig.h | 11822 | `503d1deda84867c1b55ef19929b82205de40160a7ea8f45afa01b71e51619cef` | 0 |
| external/lvgl/src/lv_init.c | 11407 | `15738eb7eb04342eb28c1651c9d79df442087bacde3fdda1acc36c15c842927f` | 0 |
| external/lvgl/src/lv_init.h | 837 | `48acde7f63dc2aaed4bcd4e6156f64171e3432cebbf0b4fa0d6c9337176193b1` | 0 |
| external/lvgl/src/lvgl.h | 630 | `3c739c642fbe68e57e1efa52ca197a54250c5ece0c865950d21f8008c6789dee` | 0 |
| external/lvgl/src/lvgl_private.h | 640 | `9fed0e26d5d4e13af98fd317ffff0b2d3ec43b62b8717e764c264ca507c3bf8f` | 0 |
| external/lvgl/src/misc/cache/class/lv_cache_class.h | 268 | `e1efd6ce9bb28c42279dc069374d814339e252f6ebbd30adc2300db052a0f0b2` | 0 |
| external/lvgl/src/misc/cache/class/lv_cache_lru_ll.c | 12193 | `ce2477d2585f3efc16e103ecad507c4d1c8bc0b9a7e138fd87c0720c303cd24b` | 0 |
| external/lvgl/src/misc/cache/class/lv_cache_lru_ll.h | 813 | `869ada3fc4002572b11dbb471e70e535f49eb296c15415078876a2ccae0103ce` | 0 |
| external/lvgl/src/misc/cache/class/lv_cache_lru_rb.c | 16289 | `a24cfa05f34a7de472714de952cf4184ea9a48af57597521fb9f8095e1b80f27` | 0 |
| external/lvgl/src/misc/cache/class/lv_cache_lru_rb.h | 813 | `d82926b1230444c4f5e96a248238cc742b37380db17c0f8636f90857a33d37fa` | 0 |
| external/lvgl/src/misc/cache/class/lv_cache_sc_da.c | 16560 | `de59aba04e8dfff491f4550568e754331719b53bcc0cfb10b2fb571b6f955ed0` | 0 |
| external/lvgl/src/misc/cache/class/lv_cache_sc_da.h | 720 | `d6abb87999ac79d248b1be091e41896311c7a45a4cdb8dbd3be8079db40f0c08` | 0 |
| external/lvgl/src/misc/cache/instance/lv_cache_instance.h | 256 | `fab16d7f0d51d7acfa6593af23b03a1ee470a4d979d9454bc049a4703bd1948a` | 0 |
| external/lvgl/src/misc/cache/instance/lv_image_cache.c | 5664 | `d3ceb1cca351a75feace1b09c1905386d2845cbb9e85b41e9a06672054f44715` | 0 |
| external/lvgl/src/misc/cache/instance/lv_image_cache.h | 1745 | `d2287b0d4cfbfeb3d422df0db32b9c95754bd33ec8042b84f56e7284fc2d4881` | 0 |
| external/lvgl/src/misc/cache/instance/lv_image_header_cache.c | 5445 | `b46115a0baa0803c71cfbf455f3a54040438d6cb21c0c2557da29c5ee1a3723f` | 0 |
| external/lvgl/src/misc/cache/instance/lv_image_header_cache.h | 1965 | `74a1eed9a6636c6c53f57a8f3e0bcf0cfcc8bd500b781bdbafd970028c671f08` | 0 |
| external/lvgl/src/misc/cache/lv_cache.c | 9593 | `d45a3df0cf144cd56c70aeee10f1817f55480e1a6cb22ce43eeaf4f88219b60c` | 0 |
| external/lvgl/src/misc/cache/lv_cache.h | 11294 | `ee21712d894191713297045ced7fdb2ac56445968c92352709ace099c8b5082b` | 0 |
| external/lvgl/src/misc/cache/lv_cache_entry.c | 4292 | `96d2aad16cb52229084c02e54c4e7ef3f4bd829655d93faeeb892d79720a7451` | 0 |
| external/lvgl/src/misc/cache/lv_cache_entry.h | 3373 | `4318c88bc4001cdfd9dd828ce9316a92e1df14f3ef9c429f86d84e5ce5baefab` | 0 |
| external/lvgl/src/misc/cache/lv_cache_entry_private.h | 1893 | `3c747101cfb03ca87d659d75d3e243dbe4af52ea2db4bcb4cf5631f93f1267c6` | 0 |
| external/lvgl/src/misc/cache/lv_cache_private.h | 7589 | `6a4e2bad87c3d44a670002e9aefdc8df6260f3b56101d1ba43f968b70ca57288` | 0 |
| external/lvgl/src/misc/lv_anim.c | 23840 | `2682a1fd6fa908737e64d20dacaf348060000f624193257a39ce79eb2e3f074e` | 0 |
| external/lvgl/src/misc/lv_anim.h | 22375 | `909e1d5ed39a896c69e847bb99556b2e532c86f6f4c111a6ae49ac2f62e287d1` | 0 |
| external/lvgl/src/misc/lv_anim_private.h | 1014 | `f0f7e852cd7f462813b4a7112febdc576a9bb84666de53dc8dd426955d1d32d6` | 0 |
| external/lvgl/src/misc/lv_anim_timeline.c | 9474 | `61e235ed14b86a45399b9094cc8d298a72991d04aeb8f2b857e15c8184e256e4` | 0 |
| external/lvgl/src/misc/lv_anim_timeline.h | 5345 | `dc3dd6b5ab0a6691387328fa9a2042fccea345eaee4ec66e2d24e345346b580b` | 0 |
| external/lvgl/src/misc/lv_anim_timeline_private.h | 1206 | `8eb0b9e887e5d4bd551ade2a0bba17e61398c1227f1f3061db29323ee34370d1` | 0 |
| external/lvgl/src/misc/lv_area.c | 16791 | `f97a87781f9c36bf2ee0288401526d9027e3f7fbc0d54ca7a563d6d6bda11480` | 0 |
| external/lvgl/src/misc/lv_area.h | 7411 | `5f92c841954d11a1bb27311730a174ed02922d1601a6a4ba63cf87b57ee11755` | 0 |
| external/lvgl/src/misc/lv_area_private.h | 3431 | `567579a0ed9b9ace5228d6517b493a3fe7d189ecc2c1c16b2294063e8caec2eb` | 0 |
| external/lvgl/src/misc/lv_array.c | 5471 | `c194246f1038177e437e576fa8cb8007d293566efcdaefebc381230cfe57d5fc` | 0 |
| external/lvgl/src/misc/lv_array.h | 7027 | `81c2fcfe0fb65de1aa73f2ee64ce7a86999339a52a8a953aa5b9f4af1e6a1f72` | 0 |
| external/lvgl/src/misc/lv_assert.h | 2586 | `e2981f5118b8188088ab5b5344c8d39e37d554c5f59427d94976f96244cd8b11` | 0 |
| external/lvgl/src/misc/lv_async.c | 2464 | `c1efac14a51c20d24625cf8b9283abae2990156e892c30ec3fc9629bb2acf5c8` | 0 |
| external/lvgl/src/misc/lv_async.h | 1342 | `43d380375967f57c436ff68a81a10584343ffdd37886cc579ba968826fcb3372` | 0 |
| external/lvgl/src/misc/lv_bidi.c | 21559 | `b1efa85dedca496a49b89ceab624dc1e4be743f1af0514b4f2376c0fa160f0f8` | 0 |
| external/lvgl/src/misc/lv_bidi.h | 2241 | `f947c2791343e2c86b70c961c7fc296b3bc02d6fc371a27d338bd82e9b739598` | 0 |
| external/lvgl/src/misc/lv_bidi_private.h | 3390 | `8a2385f09dee20f8ff2731c32ffc810c7e0615e81db0aa38893584e06a393280` | 0 |
| external/lvgl/src/misc/lv_circle_buf.c | 6992 | `07bb1a0e02a6505ca8ad6c594c30af3cf20895625f5488d6a6f17a9a771deb0c` | 0 |
| external/lvgl/src/misc/lv_circle_buf.h | 5572 | `1194e0ab32d01cd24e4c4395fb8419fdad9bee8ed4003f9692a9e1240d99e82f` | 0 |
| external/lvgl/src/misc/lv_color.c | 10422 | `c7b03a0e103c48a97969b9d657b76a5e4d6f743ac316e42cd0442e503ab99328` | 0 |
| external/lvgl/src/misc/lv_color.h | 16313 | `94fd3ebccdd9a7069e6f2fced6c289d7fcffe2420d25ab947b81e0e1865d3edc` | 0 |
| external/lvgl/src/misc/lv_color_op.c | 3021 | `c59308f21cea56668f5a1b54d599feee72b97526697e7aefd9976d0a7b74b909` | 0 |
| external/lvgl/src/misc/lv_color_op.h | 2657 | `3d7f7ea009ca1b1a7771a41d06869a6add81e3e29733d2ceb3922fb82513a998` | 0 |
| external/lvgl/src/misc/lv_color_op_private.h | 579 | `8368a2c9fb90d933881bbfeaacb99cbeb56342a1c5874dc6e61e66f8e8836ffa` | 0 |
| external/lvgl/src/misc/lv_event.c | 12208 | `d1c4bb5f304cc10b5671c0c523c88518a0418dcfda7d13447f6e6b995307343d` | 0 |
| external/lvgl/src/misc/lv_event.h | 11441 | `e8799b9043844f2c0148f962143a02dcc3af6c598d60cffafe097f48a6cf405f` | 0 |
| external/lvgl/src/misc/lv_event_private.h | 1589 | `1cda17926012d39e5529b8e61c4f98ac14ae57b1f97b11681875996000310915` | 0 |
| external/lvgl/src/misc/lv_fs.c | 23360 | `594bce8c830614d5032ee40d102ed75e96a905893972009b286d8535616fa072` | 0 |
| external/lvgl/src/misc/lv_fs.h | 11577 | `9962b6b3764fb881a895b8bf9524d9dbe5abc75390fb96ede4020b6731d2dec0` | 0 |
| external/lvgl/src/misc/lv_fs_private.h | 815 | `584db57e43d707b69148f95bc42cb7c9745af661a42313dba2f5980e792bf17d` | 0 |
| external/lvgl/src/misc/lv_grad.c | 3180 | `3e0e139f8ca9dbfbc060f44161b8d0738ee6925b08d0948b431f2dd5c3a081f3` | 0 |
| external/lvgl/src/misc/lv_grad.h | 7334 | `245b64abd976aa2169fe3073a9420be4c4c8127105d6100acf507a16926fe987` | 0 |
| external/lvgl/src/misc/lv_iter.c | 5337 | `c645dd99be4f4247be8d9f9a4caefea257ce3458db1a952de415b9c069942ae2` | 0 |
| external/lvgl/src/misc/lv_iter.h | 3938 | `2e60c4319cedacac3476df8e82f0863484ff1459ac4af4037be5d74f61fdade3` | 0 |
| external/lvgl/src/misc/lv_ll.c | 9341 | `2ca526b6f8880425b0d0c38b471c8b81ebbcd2dfd1f0b369b46558fcd65a0099` | 0 |
| external/lvgl/src/misc/lv_ll.h | 4203 | `7a020a8d646c37f5760ec228c49955da3f731865e63bf6af4d83f6080d389d7c` | 0 |
| external/lvgl/src/misc/lv_log.c | 3518 | `86e97097989d274adbda9af1536acf4d2d0c1b5a6d44b0f18f19789645e56274` | 0 |
| external/lvgl/src/misc/lv_log.h | 4623 | `87409bbd86419e606dccc62a4555c20d67850fdc5d1e92a69852a6bda4e43238` | 0 |
| external/lvgl/src/misc/lv_lru.c | 9387 | `0a73d5367879f63f05f33eff773ccd9fab14297ffbbee319b47c284085b033ba` | 0 |
| external/lvgl/src/misc/lv_lru.h | 1822 | `d7d76fb6a0936c31aa040989d692df62986d8f3d5bb02efbcda6f2995d0b3a7a` | 0 |
| external/lvgl/src/misc/lv_math.c | 14598 | `58e309b8dd6a450684814e043b9b1724ebe2cac1058de1597679e7de7291bc4f` | 0 |
| external/lvgl/src/misc/lv_math.h | 5459 | `c93ab3593e02af43048bfd266872f26a19756d3c16978fadc6684ba09acf781f` | 0 |
| external/lvgl/src/misc/lv_matrix.c | 6988 | `00108f9e3f298ebfe3d1c9f8c29647cfd6ab1c6960d56bd6414db0e566508ca2` | 0 |
| external/lvgl/src/misc/lv_matrix.h | 3575 | `e5636e653c9416586765a74e97a968d9429026b87bafd15b60c069faa79f8a3e` | 0 |
| external/lvgl/src/misc/lv_palette.c | 8267 | `87e038f4b160d274318663ab3214aade8eaadbba094095416fca7d9d8895f915` | 0 |
| external/lvgl/src/misc/lv_palette.h | 1315 | `57f6853a9a1f9b014d4e75d96858c2fee09e31878b99d7fd8f2ad3cb1a4ac36f` | 0 |
| external/lvgl/src/misc/lv_profiler.h | 5462 | `ae1d658d3a4dac133642720b486022b5196aa685354d9b9d53f2d0964deea2c5` | 0 |
| external/lvgl/src/misc/lv_profiler_builtin.c | 7417 | `23d32ef8bbd72f8ac5db9483946f32753c010e7f14cfd71ccaa208ce59346752` | 0 |
| external/lvgl/src/misc/lv_profiler_builtin.h | 2127 | `83f5b32e9214fd2b42a4012e1953a4f54f7f87f2b0f3a162e2b9961bedb6305d` | 0 |
| external/lvgl/src/misc/lv_profiler_builtin_posix.c | 2746 | `7d5de1faf1c5f786ca484c0340a25993eedf8b48dff86e2e99a7f677876e0f9a` | 0 |
| external/lvgl/src/misc/lv_profiler_builtin_private.h | 1570 | `8235644274254cdb3fbd1c8ff4eb7100f9aced31562ad1abde514b832919df29` | 0 |
| external/lvgl/src/misc/lv_rb.c | 13646 | `376ed3247c31f42e7841fdc9a253f4a3c8eb895da5c11a8c553b9278cc44d4ef` | 0 |
| external/lvgl/src/misc/lv_rb.h | 1500 | `b758d58da2016f02fd8503a747a362a0037e5adb11752caa86b9c2a0568970d1` | 0 |
| external/lvgl/src/misc/lv_rb_private.h | 814 | `69915d754585ada469c9893bbdb5df89305b3da9e5cd211ca514413adbb542a5` | 0 |
| external/lvgl/src/misc/lv_style.c | 19723 | `5407b0d05c928d7be0b2b989e3b4765163d7083b1ed9047b19c41d14ad280d14` | 0 |
| external/lvgl/src/misc/lv_style.h | 21904 | `0c5d713bbf38bd8d02d39634a2a7381ab2198c831cb74ed712afdd055f14e786` | 0 |
| external/lvgl/src/misc/lv_style_gen.c | 23231 | `ef357db4a7c8fe4410df855171456c75d16e3f0e86685ea4a28d1100bd623056` | 0 |
| external/lvgl/src/misc/lv_style_gen.h | 24421 | `f91315f21669235972e64efd1f973c32be59dd74d8e3d8f8e53a0355b3cf496d` | 0 |
| external/lvgl/src/misc/lv_style_private.h | 564 | `3cb6afad2988cbcc320f33fcf536cbac490772a2ca71295c75b08f5e3c7a0ba5` | 0 |
| external/lvgl/src/misc/lv_templ.c | 717 | `40d1b3dab81753f66ebca0b6d0b3065bc92d317c3c54e1809628d666dbeff767` | 0 |
| external/lvgl/src/misc/lv_templ.h | 509 | `7cc6e2a787852952c13d4d42b1e9b3967bcac6c27341390a58cf470e868c30a4` | 0 |
| external/lvgl/src/misc/lv_text.c | 30304 | `37453be77fd8fc841e747de58e1d8610fa926eca97dc6a5327f00820a64bcd7a` | 0 |
| external/lvgl/src/misc/lv_text.h | 2265 | `750449ca510f8c7d4b2c286fb29c2e4af648c6d0f0be0e1a9949157bbbf47b5b` | 0 |
| external/lvgl/src/misc/lv_text_ap.c | 10094 | `cf3d20b8995203508d71eb871f5f2383ec34818e6f737797b698b4d1ccdc1215` | 0 |
| external/lvgl/src/misc/lv_text_ap.h | 942 | `a355b36465a9e2dd21234c376886d262b1e56ca8663fdc4fbf283aea6529391c` | 0 |
| external/lvgl/src/misc/lv_text_private.h | 10560 | `093c1a850fe0ff5e3e71de2ab1db0aa8c50af961b7e7d6de015d9534057a7971` | 0 |
| external/lvgl/src/misc/lv_timer.c | 10363 | `bcec8183d48745433cb744bb1ded8a6a1aff15d47d34664bc22072fcfdd062b2` | 0 |
| external/lvgl/src/misc/lv_timer.h | 5626 | `87157dafe2d3ee9873950bd88243b9941d4ed0915d4daabb4395521b6b2fcc59` | 0 |
| external/lvgl/src/misc/lv_timer_private.h | 1611 | `1a1d568decbea4d6765c9ebf5b15e01cb45a23cc2aeb9dc89108d77815aa8f2d` | 0 |
| external/lvgl/src/misc/lv_tree.c | 4968 | `242feeedba53d5f883155a9506c5de58ac11b27296c68b66c01b63d66d2ff943` | 0 |
| external/lvgl/src/misc/lv_tree.h | 3061 | `b7bab62a7b0bc2bf4adca28688d61ab73ab42f11b33e79df24f1cfcc79601ffd` | 0 |
| external/lvgl/src/misc/lv_types.h | 11427 | `137469b8ddfb40890982d18ee5f787c6f2c9e695e77c7bfeb9c7c05083131652` | 0 |
| external/lvgl/src/misc/lv_utils.c | 2272 | `3bf2782c33509353e48169e2b769283e8fab5bf4508d9500e775535883c460bc` | 0 |
| external/lvgl/src/misc/lv_utils.h | 2254 | `85a27f6fff5bd2f686636f3f96f1675165701b1e6f762fc07a8e7b9be06e651a` | 0 |
| external/lvgl/src/osal/lv_cmsis_rtos2.c | 4891 | `bf57eba6877405164ae3be3871b190e090b1375cb1eb0636f9c3c49881d28ed7` | 0 |
| external/lvgl/src/osal/lv_cmsis_rtos2.h | 870 | `6fb1ef9a8fb9b5ce63c251ccb66b8f22d81375fc6264f8ba23dd3921601ccbff` | 0 |
| external/lvgl/src/osal/lv_freertos.c | 17555 | `524e27835ec9dd9e916e9ce67e39f026e83d11ae994d929d08b917061d93d1da` | 0 |
| external/lvgl/src/osal/lv_freertos.h | 2570 | `58fd3aaaf404170659c16cce87a510b2f14f0ee3b2d630d4fce6e69daef6c7b6` | 0 |
| external/lvgl/src/osal/lv_linux.c | 6692 | `05639308fad6f06a323506da514d357f450f76626ade2188d72bcbf735f64e60` | 0 |
| external/lvgl/src/osal/lv_linux.h | 1045 | `d1f3d049bd68593971da951925413e7bf598af58f2062491172d1c1780f5a464` | 0 |
| external/lvgl/src/osal/lv_mqx.c | 4041 | `1d4adb5fb4bc2a7fcc10ec2d0305a682ba0ae15f774f16cfbda494c69fd46f6f` | 0 |
| external/lvgl/src/osal/lv_mqx.h | 733 | `53f52015930e67b88807b5408432f2caf5a770db9601580e1e76022152f0e7c0` | 0 |
| external/lvgl/src/osal/lv_os.c | 1268 | `644bdea60d965b610efb2efc77c59c351991b8cc49ce4aac9090059d0ac75bb2` | 0 |
| external/lvgl/src/osal/lv_os.h | 1541 | `1523589a733911ef70cc2322c692ab72cc725ef503529147595a74d23eb80a9d` | 0 |
| external/lvgl/src/osal/lv_os_none.c | 824 | `fce07fb098f6fcdc4af2c271aaeeefacbbe25b7644cbd74336a8a38b7b98e5a4` | 0 |
| external/lvgl/src/osal/lv_os_none.h | 660 | `74dddc25a66bfa264eb6076996c046f8c90f4cffaf793ddcbc744fa675259ca3` | 0 |
| external/lvgl/src/osal/lv_os_private.h | 6981 | `e6a069dd95c7bd620c103b4debcf3fc7c43e4cbe4e5de4d1b026da58e334bd7b` | 0 |
| external/lvgl/src/osal/lv_pthread.c | 4159 | `8200ffa89ca9e72c9a1ec2a27ad4d0a5a9510aa9e4e79755cf1d7591c064e503` | 0 |
| external/lvgl/src/osal/lv_pthread.h | 918 | `dc67af93628bb5a7548ade85252963e8f96c8084da4d5579e00aaff4be2534aa` | 0 |
| external/lvgl/src/osal/lv_rtthread.c | 4308 | `0e47d2f7f6e0dee5a1889287e932f825555f84def68a24eca968752588ae556a` | 0 |
| external/lvgl/src/osal/lv_rtthread.h | 803 | `91a9691e84901b3806237dae07273d795fbedc7baf61a7c7bdad948dece54723` | 0 |
| external/lvgl/src/osal/lv_sdl2.c | 4085 | `dc22aa730d09e9d6b28278aabb65ebdd512fa0f50221b8957c95185c8bc9078a` | 0 |
| external/lvgl/src/osal/lv_sdl2.h | 848 | `b4438bedf5cbef3c670239216f7d17161095f5b9ecc30a340291f06ab3753020` | 0 |
| external/lvgl/src/osal/lv_windows.c | 5168 | `e453c309d1cd5d7ca15ca8c19a981321c0f09f9bfa3a01f0d8b2f85b8ffe8056` | 0 |
| external/lvgl/src/osal/lv_windows.h | 800 | `83fbfdfb6c89ac3a743a819242a6e9406a62944f2e346908bb5378bc9be67640` | 0 |
| external/lvgl/src/others/file_explorer/lv_file_explorer.c | 27380 | `80ffe04c1974669c23c5956c63ac8f979b7f0832a2a5b3123faaa3cef6a896a5` | 0 |
| external/lvgl/src/others/file_explorer/lv_file_explorer.h | 4201 | `88f779f2ab44abbb2a2ce35eb0ff37e13293a55c372210156632bef2fa8e6aed` | 0 |
| external/lvgl/src/others/file_explorer/lv_file_explorer_private.h | 1631 | `ee2eec609ef20c702ffcd89ae52a88d7b234680127e57eb0c228d6fdfa2ca957` | 0 |
| external/lvgl/src/others/font_manager/lv_font_manager.c | 19174 | `a5151f16c6b443503434e2a9652b37f83dbc380c76c3d7bea640061815f2d095` | 0 |
| external/lvgl/src/others/font_manager/lv_font_manager.h | 3581 | `98fd33dfcedafde66cf5c3cb736a19936dca99405a59a16e87fadd885e4904dc` | 0 |
| external/lvgl/src/others/font_manager/lv_font_manager_recycle.c | 4994 | `4c3058e4a8c578322b6f7885ab96c1f47329385a3a0dc611ed7521c401992037` | 0 |
| external/lvgl/src/others/font_manager/lv_font_manager_recycle.h | 1934 | `70032d2d7cfd008faa9b125258f9becbd34f639b69a31247b74f21e90652dfb1` | 0 |
| external/lvgl/src/others/fragment/lv_fragment.c | 4356 | `ac125bd0061620bd0b65114a5912f746105e498c9bbd6b5388e3f27b57bbf5ec` | 0 |
| external/lvgl/src/others/fragment/lv_fragment.h | 8351 | `9c3c12ff88dbd08a62498057a388561487842681fb6e0b4d1f1679b428ee4cfa` | 0 |
| external/lvgl/src/others/fragment/lv_fragment_manager.c | 8453 | `36edd107275c67c6b1d87d53eebadf68faeb8db6beb75b3f9b67e23c2a1dc1d0` | 0 |
| external/lvgl/src/others/fragment/lv_fragment_private.h | 1385 | `f9412421aad95a3fbe95ea9c719b1a1fdb123fafc15fdcb91e3a373eb2765acf` | 0 |
| external/lvgl/src/others/gridnav/lv_gridnav.c | 14610 | `302f684fc8cc8d6c6c30c0e9203794f097a10adeb32f2fc4ed32ced32f07f999` | 0 |
| external/lvgl/src/others/gridnav/lv_gridnav.h | 2574 | `65fb4ced703e4eb0359a6dc249fc5c61c27c708a522d0e3fc0fb6dbc7c363654` | 0 |
| external/lvgl/src/others/ime/lv_ime_pinyin.c | 40355 | `7c69ed3ab9a23b0eb4ffff23f3475242cd990c69d065be27b9c912c84e397212` | 0 |
| external/lvgl/src/others/ime/lv_ime_pinyin.h | 2792 | `c2a95e087a4dfa4c1bc3fa8db193fe3556bfa296b5bb938a86414c1847e37d54` | 0 |
| external/lvgl/src/others/ime/lv_ime_pinyin_private.h | 1789 | `3ff2434a93cd32b0745da9974864af706acbe0c79f7da31c8163ea71084567a1` | 0 |
| external/lvgl/src/others/imgfont/lv_imgfont.c | 3002 | `b78cbf7b92746f3e9fce1ab6bc5411c628e8a6702964e8afe32acc45e9078418` | 0 |
| external/lvgl/src/others/imgfont/lv_imgfont.h | 1444 | `134619f5278016d7406191816d506f97e3c9a3eb76abd6c48ca69a33d8cbda94` | 0 |
| external/lvgl/src/others/monkey/lv_monkey.c | 4803 | `553a89b1eea0a65d7cdc150a829273e4cb03cd1d7c98ed0c392b9894693e2b2d` | 0 |
| external/lvgl/src/others/monkey/lv_monkey.h | 2422 | `4b40ab13480ae56fa55442341ee26266f0425dc77cc52466195d529c2521e945` | 0 |
| external/lvgl/src/others/monkey/lv_monkey_private.h | 626 | `f2b18e5230d65ee0e4c1c9edf9936e1dcc24326ad83263778e7f9ccb34d5c57f` | 0 |
| external/lvgl/src/others/observer/lv_observer.c | 33981 | `f2dda22b8c18796b49b73b60f2354969826bdb4c2cffb79d400354f74ea8ac2f` | 0 |
| external/lvgl/src/others/observer/lv_observer.h | 24263 | `70395d0d596f81f91612ae4a967b1d13ad3a77f7cd66ca2d73b70599b1c4e460` | 0 |
| external/lvgl/src/others/observer/lv_observer_private.h | 1863 | `ed1c33fcd98c2093a2d244b475b605ab3973df74cd7a56428f61a3da8ce3bfee` | 0 |
| external/lvgl/src/others/snapshot/lv_snapshot.c | 6553 | `4e22d544380f72c0db8dc6c55fe25dfcbe26ab8b2c1c6f9761bfb7c4de675312` | 0 |
| external/lvgl/src/others/snapshot/lv_snapshot.h | 3265 | `267d83666b874e795f46928f87980e2a354ca21b54d2978644e9a8319d54f8d2` | 0 |
| external/lvgl/src/others/sysmon/lv_sysmon.c | 13894 | `2558b74ecef2fad07d79f790185bd5bdcffb3255d8436292901ae7473bcb92cf` | 0 |
| external/lvgl/src/others/sysmon/lv_sysmon.h | 2583 | `8fb01d8343f671f12b481dc16291cab3416d8db432afaf3eeea1e6a077f0e225` | 0 |
| external/lvgl/src/others/sysmon/lv_sysmon_private.h | 2081 | `e7cc2404a6d1461f2bc86463441ebc7166caf0d94128abffa8dc0d592852ebdc` | 0 |
| external/lvgl/src/others/translation/lv_translation.c | 9352 | `78ea3080c589a6d3c3aca740c956047602719c4d8fe84d035d625297d7d7d8da` | 0 |
| external/lvgl/src/others/translation/lv_translation.h | 4868 | `531ffe9bd555bee7b35bd7d35dd8a6aa58efff71a6951d2770f082e709f7c6ae` | 0 |
| external/lvgl/src/others/translation/lv_translation_private.h | 1132 | `6fbe61c001a6b4b13c7719658d5fa251224e2d6752767744a82eaf8b140b0b78` | 0 |
| external/lvgl/src/others/vg_lite_tvg/vg_lite.h | 69659 | `1a7bbe4f52957197646ee72db3d9d94acff123e720c2de9473b314c2929a53f7` | 0 |
| external/lvgl/src/others/vg_lite_tvg/vg_lite_matrix.c | 3952 | `58d313b99765f1f460323610fc7a12c0104f473bd42d723bd240308355090930` | 0 |
| external/lvgl/src/others/vg_lite_tvg/vg_lite_tvg.cpp | 101625 | `ff43b8c947d157f2a127cfc989d6e74816d7a357c2387a21812cd16daecb3d58` | 0 |
| external/lvgl/src/others/xml/lv_xml.c | 35696 | `638486b538a70956de840b08a47bf8a2ac13b344a6130ebefa91eebab3ed9dd6` | 0 |
| external/lvgl/src/others/xml/lv_xml.h | 4571 | `9f13145d7192c40125d11ae3d674c1cd46c53cf848b2897b07b9b1013e8dbcb9` | 0 |
| external/lvgl/src/others/xml/lv_xml_base_types.c | 24588 | `419fc993d598f20f622f4a1a2d8ac24fe66262e09c3fdeb441c47995275027f9` | 0 |
| external/lvgl/src/others/xml/lv_xml_base_types.h | 5210 | `6670fddddae3604136d537c1a99fdadcdd81d5b94c2ec735fa7d8dcc1a4415fe` | 0 |
| external/lvgl/src/others/xml/lv_xml_component.c | 36609 | `f4e1af79f3d296cd2cefb65d0c491810acefc6dd391e2e4dfbb64bfa8da845d4` | 0 |
| external/lvgl/src/others/xml/lv_xml_component.h | 2324 | `ea2a2667acbd0f5395073f15fc09b4e7ffbe2f4ab3083e1eb7f40a04ea20079d` | 0 |
| external/lvgl/src/others/xml/lv_xml_component_private.h | 1947 | `347c75b4f3d4421792333663b264c9bdd87fdeb51e7488750e49326a5a63c69d` | 0 |
| external/lvgl/src/others/xml/lv_xml_load.c | 10119 | `17b3e761cf894c8a4f1858ef914e7dadb792524b74873c3123a53ddf777f693d` | 0 |
| external/lvgl/src/others/xml/lv_xml_load.h | 1930 | `83f15962f5cd38895c2ecaf196aac273f852a8323963ddc6e5e9e201ca2f9628` | 0 |
| external/lvgl/src/others/xml/lv_xml_load_private.h | 679 | `9228dd097e2d64c96044ce9c062434535281d087bd295ebd0dc670ef10a1cade` | 0 |
| external/lvgl/src/others/xml/lv_xml_parser.c | 3428 | `670548b6f14b04d1e7ba43d4656bb0194f87ebc5c80ae0443e9a239417cde597` | 0 |
| external/lvgl/src/others/xml/lv_xml_parser.h | 1991 | `ffb143c282be817c381cc09f0f4c1eca2d6aab7f01b34f4b6ce035ff18f4a9c4` | 0 |
| external/lvgl/src/others/xml/lv_xml_private.h | 1454 | `56e3da1d485a627f712ced3072c4277923826946698b4c77e8d2eabf621b65ac` | 0 |
| external/lvgl/src/others/xml/lv_xml_style.c | 16539 | `173349148203f5b3a3d4c34be6efb3c80da6e81a93e84283d2a9a24a718a9aa4` | 0 |
| external/lvgl/src/others/xml/lv_xml_style.h | 2085 | `913a9574d8aee3a823456d2877b1d54e837a35dc7c20bca6d7022ced928b1aea` | 0 |
| external/lvgl/src/others/xml/lv_xml_translation.c | 5233 | `1a5f601a2527022330d1588c0a64dd49f88621e390023d314c1804e87ee04681` | 0 |
| external/lvgl/src/others/xml/lv_xml_translation.h | 1037 | `68a230ef54a3965db037ae8ecad04dffa9c258ab776e12e96aa92e4dfbef0449` | 0 |
| external/lvgl/src/others/xml/lv_xml_update.c | 3227 | `c3285a86dedf65898a6dfc4b471ea99ac31dfb3fb1b1b0fba9406ef895b9b344` | 0 |
| external/lvgl/src/others/xml/lv_xml_update.h | 1007 | `19c921bc1da120189782bfc8d6328b1d52fe1b356203e0696d99860ca9358b89` | 0 |
| external/lvgl/src/others/xml/lv_xml_utils.c | 6759 | `68474a9f7393010dfe5654d867b0ed2b0c228cb2f15049ec81c253caa12020d7` | 0 |
| external/lvgl/src/others/xml/lv_xml_utils.h | 2143 | `64de4da79c701e4aa90aa43ba501e8e6e3d021cf3f9524a25f8b7db495858af1` | 0 |
| external/lvgl/src/others/xml/lv_xml_widget.c | 2688 | `262a9c06ee5480956408d181823538541664cf1c56735ca5469939df1e44c07e` | 0 |
| external/lvgl/src/others/xml/lv_xml_widget.h | 2664 | `5b43e423a2e6589705c1442ae743a8e260bee30d35b8b4cd1184187cd818fc60` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_arc_parser.c | 2914 | `2b4601232835e63bcba60472f3da8d6ae7ad000a802d5d5993bc16bce27330af` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_arc_parser.h | 712 | `746bab9adb668054711195feffd5b2e7115e93cb5f53b532027f3c8b027f1dc0` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_bar_parser.c | 3556 | `d3f19fd8d5c0b6457e61a73cc3adba0629f26ba141837a40617e9d05c8fa852a` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_bar_parser.h | 712 | `c32248230e0c882e1cdb63808a78f8f2d41cb376c1e6948c8863f02dafe414f2` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_button_parser.c | 1132 | `6e92a92a57462b556b73d597d78cd7060448c2816d1ae12faccbf6e34e4c4229` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_button_parser.h | 734 | `d3e3fefc677e5a1004e00560dd9a033f47a72b1c54b5c57aead095e3d05b1b25` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_buttonmatrix_parser.c | 6616 | `9826dad5b1c2623a762b188cef9b92ef7a81d8f0f70cb659cf6288c4c3d9db0b` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_buttonmatrix_parser.h | 776 | `21cac6dc02e1a1e0aeca715f765ec27ec8b03fd7afdea7f7afd9cea492276ffe` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_calendar_parser.c | 2753 | `3994df3d3c5f4de058bdc72e29d644659c2dd6543548f52b8f924b0e15c64aa7` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_calendar_parser.h | 1111 | `8f36da0c03896acec0ea9ae3ad4dbf15340685a80b9f37dc6cbef81e64e0b90f` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_canvas_parser.c | 1115 | `060956284027fd5e164a14800bd1dbbc29160129063a7d37215a8e37e097f2de` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_canvas_parser.h | 717 | `acf0e5863d2ad25edb01e5facec0f56036567e7176f1cc97b40bfd1d236ac085` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_chart_parser.c | 6497 | `dc992ba2bedae2ec9b22478202354686f2bf85ac5aa9244a5e06b4b996a04a7e` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_chart_parser.h | 1234 | `4007a0ce34b5ef2d2905465f0f9f780b17a411f0a238faf22e38a37265ed1be2` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_checkbox_parser.c | 1366 | `08e8dd64ab869e32546300919b2ba0adaf48d9f633a8ca3bb64c502d9631628f` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_checkbox_parser.h | 728 | `6106e4d102cdbd4fa9e019b2097167845cd5a601e18a30db20a5b80b13adada3` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_dropdown_parser.c | 2381 | `266cdf46bbce5bcdfdf1ebf84f3e8a2626f2be1ffe71bfedb065943ae2e20f08` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_dropdown_parser.h | 919 | `d3b9d1d4fe9d04ee474fec98f1f173d6eaff1ba5f0bd2b0d458ee676e0003aa4` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_image_parser.c | 3392 | `b1e97d1b8567e710acba67860b61b8ab9ef79b0e7964349f1c9687dd8a1468cd` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_image_parser.h | 775 | `e99ebdcce89fd5a637503ac64ab6886a8ad8092474eaaa6fd6d73c28e8918fc6` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_keyboard_parser.c | 2524 | `907d36dccd1306548c527e431302cc2a1d3135592d21f5735fe8deb851a81265` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_keyboard_parser.h | 748 | `e461872ac793348f2680492cb2c98820ef1079c55ae2edcdbd82c85095f31355` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_label_parser.c | 2820 | `d487b34f2e2a8abe5d7ead7c4920610c82d07be935c55c93cac8b7447bc88e80` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_label_parser.h | 727 | `41160d0a2b65368356e14a0e5b25f3cff592c4ee451dffa394222998561c5422` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_obj_parser.c | 45589 | `e07fe3f0317abfa569aae6cbd1866d1209165561c2b186272ad7883fba14caff` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_obj_parser.h | 3060 | `e49e1d2f9c66c4dd96f1c095b468b8b114196a5eb31b87c5cf0f29cbafc14f65` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_qrcode_parser.c | 1764 | `651e063dbb32b748a515dc5774ccbb2afe4f13c803ad53e49abc20b8d98ec402` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_qrcode_parser.h | 736 | `b50aedff5997d7d2e0151a0159637094a338333fe20976b6c1791feac2d03a72` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_roller_parser.c | 2762 | `591db8e3a88bedbd622e5e754ddf7a28f2fb5a25e130c567828061e74974e0bb` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_roller_parser.h | 733 | `dac7485a5071fb5afcd7a7e1c34e921ce59d4805057fa1f344fe3bb9d86b1a26` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_scale_parser.c | 5343 | `e99150ecc891151e1e4ae84de9685b37c545670902374acbf6e951a26f563255` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_scale_parser.h | 898 | `3cb35c87cb9f7967df523f55c7c91abf949e52eacccbd8b1f6fe8130687cc77f` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_slider_parser.c | 3634 | `f76062dd01459681826cad65a7dd27f9ebedd8212b9277978dccb3743afad80e` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_slider_parser.h | 733 | `a22820d86c1eec078ce06018394f2de70511ac412b5e3668e12d5726eed33277` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_spangroup_parser.c | 3539 | `56e2ee37264bf05d2a473b416903275f8402c0e3a4c81fff3ffd39658b93a0f3` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_spangroup_parser.h | 923 | `ce1e357c8140946aa0066c38711640886bde56645c97aa9437c3344c69d18a1d` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_spinbox_parser.c | 2331 | `4b3c7701fc56a094a0c7dfa10134c343500f102f0538a51f7fe83d1afeb90e4d` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_spinbox_parser.h | 740 | `8bc90a095a5b8a57da1d4a2869d442fd711996c15e5387ce82aa774f12a2bc71` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_switch_parser.c | 1911 | `e77bec91a3bef1b2516b25759dda0ca2ccd0d8987c5be799db6b62c8a4ebbacf` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_switch_parser.h | 716 | `c0c2efe53d8cc9ad3c453ac944beed0270a50a005170760c9656b450052b399c` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_table_parser.c | 4050 | `3bbb241433f6289aebf417d242bf0e12a47bada70cffc19a6b04a17ac3fcf68e` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_table_parser.h | 1063 | `935d546c7006fb4d98ae522574ca98b522521de03b2b52360edd2d29d4e560b6` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_tabview_parser.c | 3295 | `7dd6d99c0c2e41a803a7aa803bfb79c31addf49425b73a95f278c70520042622` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_tabview_parser.h | 1269 | `dda379f1da9de438a76ed75bf225cb2755cb7e7b442e5bf499687688540ee578` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_textarea_parser.c | 2020 | `927052390280e70d68608baf60e74cd83b9ff3bae81aaeaa8a590274a4bb2d86` | 0 |
| external/lvgl/src/others/xml/parsers/lv_xml_textarea_parser.h | 748 | `ea90fbc60bd608104f9f5c7850413766ad3f68b995694372180be1c876849b9e` | 0 |
| external/lvgl/src/stdlib/builtin/lv_mem_core_builtin.c | 6431 | `a186e9a3ccb47906f960b8b50cf9a38727e2d4c6f2cab0a048bc2d960493d4a0` | 0 |
| external/lvgl/src/stdlib/builtin/lv_sprintf_builtin.c | 30272 | `4efe0afd79c703eaef6f8629194aa79831480a5e7acfa9ecbc1c1ecd2bf5d681` | 0 |
| external/lvgl/src/stdlib/builtin/lv_string_builtin.c | 6596 | `025a30ff53e5d8b6a44a2ca8f1247f2f39f0b1ebb486ebdb101ed447f4860a36` | 0 |
| external/lvgl/src/stdlib/builtin/lv_tlsf.c | 38016 | `fb67f7034a5fb9f4176fa2d0c7c31937a60c955e0dd5351dee24134833e9716e` | 0 |
| external/lvgl/src/stdlib/builtin/lv_tlsf.h | 3742 | `d133a30d9dfdd2cec4a6e26d3124aa9d079d397d276df338fd83637466a3e3c3` | 0 |
| external/lvgl/src/stdlib/builtin/lv_tlsf_private.h | 862 | `11d7dc0fed370a35c8d65bcb685bc32dd82ec0efa6f65fefceb600ae8a0f5269` | 0 |
| external/lvgl/src/stdlib/clib/lv_mem_core_clib.c | 1498 | `f626a9ea8cf60dee9ef8ecc0d8032286ab7ee420e1d7605129c27530eec6bc72` | 0 |
| external/lvgl/src/stdlib/clib/lv_sprintf_clib.c | 1082 | `b5053f9c6b8f8398eb280fe64a034aa153fdfdd83b7795356bf4bdbba97d1b94` | 0 |
| external/lvgl/src/stdlib/clib/lv_string_clib.c | 2884 | `76cac93eb37945ecfb835ba8c9e21f58d6adefa26cabed6d63aef9f79d2e515a` | 0 |
| external/lvgl/src/stdlib/lv_mem.c | 4379 | `00d8226e661600d059aecad01f28fadb2bc469cd7cd87a84c7a069b0b4b35d76` | 0 |
| external/lvgl/src/stdlib/lv_mem.h | 4272 | `93adf94a575981657bd15176488e833aa18065acc42604dc72a61379820d58ad` | 0 |
| external/lvgl/src/stdlib/lv_mem_private.h | 554 | `9201a978bed0a0409a8c08f31080a4a56f6189ea2e8336b134517426822998d1` | 0 |
| external/lvgl/src/stdlib/lv_sprintf.h | 1410 | `43f6f5359097c346c78e09eb3827a0e5bbe62260af57150122e21c5302f750ac` | 0 |
| external/lvgl/src/stdlib/lv_string.h | 7741 | `668a5be6caffb6cf21964a47d9dffd18b3d937c30080d8af5099e2da102b714c` | 0 |
| external/lvgl/src/stdlib/micropython/lv_mem_core_micropython.c | 1802 | `e4099b52b4f4ffe22caf1eb7f6a7b892e2ad3dcf8852ac421fb5ff9bf97108e3` | 0 |
| external/lvgl/src/stdlib/rtthread/lv_mem_core_rtthread.c | 1637 | `da0fe8d34f416ca1d1f44de85e5910f0dd455812a9b9ac0ae5d9ed03199593ba` | 0 |
| external/lvgl/src/stdlib/rtthread/lv_sprintf_rtthread.c | 1225 | `d7599be3b9416ef5ae2bfcfa1db51560bca20c8d9ea1b8b9f34db9774255fc9e` | 0 |
| external/lvgl/src/stdlib/rtthread/lv_string_rtthread.c | 3251 | `544daafe2e237bc70fb803d83ed9b8288278af46375c1f5101b9fb35bf3cfbb6` | 0 |
| external/lvgl/src/stdlib/uefi/lv_mem_core_uefi.c | 2327 | `e26069f90a8135cb07442ea75f8f4cfcdcf61be09f63d96d5564ba0bd8fba2f8` | 0 |
| external/lvgl/src/themes/default/lv_theme_default.c | 54412 | `413abb720f698ec622411b84cdaea7d2b245aba763e901cc61f50d5c97f4bebe` | 0 |
| external/lvgl/src/themes/default/lv_theme_default.h | 1448 | `2f569db7bcca41560cef96b28dd20274412d6784dd73810378c46cd5a447d511` | 0 |
| external/lvgl/src/themes/lv_theme.c | 3005 | `4b8f12f433517cb02e211621b7cae73146f94cc05004572b865770ad5eaedd01` | 0 |
| external/lvgl/src/themes/lv_theme.h | 2555 | `0897d702dddfcbe00a84b216474ba4cd7d99f531e9dae7560c3d7bde313cddf5` | 0 |
| external/lvgl/src/themes/lv_theme_private.h | 1012 | `be35765d5d3c23b9c06bd2a6ba17f8edc7263eab33bacf2437ffe26ea979dd96` | 0 |
| external/lvgl/src/themes/mono/lv_theme_mono.c | 21032 | `1d0e8f548ec9b9f266523191f215f114a4611ed527420dac81b684ea90035176` | 0 |
| external/lvgl/src/themes/mono/lv_theme_mono.h | 1209 | `14b152f62b6d98815d47f4a953ab35c30cfa646c4524a29d2e4c3bda807393d1` | 0 |
| external/lvgl/src/themes/simple/lv_theme_simple.c | 13953 | `33887b4dc97e020f1f6d69a6fa4100c0d7c1a1ab48ea161dd2c65701ddedb15a` | 0 |
| external/lvgl/src/themes/simple/lv_theme_simple.h | 1172 | `20e1c612ba2f2d1383c936b9d544da4d29e25aa45085de520a79f06d72bc6190` | 0 |
| external/lvgl/src/tick/lv_tick.c | 2548 | `3a72269e2c36f37119c9ce0baba438f1f8b88fa62199e9ef4385133c826b041e` | 0 |
| external/lvgl/src/tick/lv_tick.h | 2409 | `1e77b5ba509c0f8aa24b7f6418d00084cb033facb1a47ff926c3e4b03577d3d4` | 0 |
| external/lvgl/src/tick/lv_tick_private.h | 725 | `a4250ae24958892696061c06e52b46bb64047044309de369759d1fb1b329f284` | 0 |
| external/lvgl/src/widgets/3dtexture/lv_3dtexture.c | 3753 | `4f3fe1d1a5a60af87fdc4b374e0a5ed4a854f068c623ee92db66c80189eb5202` | 0 |
| external/lvgl/src/widgets/3dtexture/lv_3dtexture.h | 1815 | `8d714c108fb9bade8c7d708272279501de3e65f25c13ce8280abacf257f13d81` | 0 |
| external/lvgl/src/widgets/3dtexture/lv_3dtexture_private.h | 803 | `ce6b78b3eedf2a6a317abb615c465eb9b19e8950236ff01025b15c1a5e23c82c` | 0 |
| external/lvgl/src/widgets/animimage/lv_animimage.c | 7146 | `60c52250234aad96eaa4ddc3678318ac86baad646273a68c5db308b186eade8d` | 0 |
| external/lvgl/src/widgets/animimage/lv_animimage.h | 5188 | `e9ebeb5adcafb34920339dd42014502a68a49e6d2eeb83b68fd41d03d6135db1` | 0 |
| external/lvgl/src/widgets/animimage/lv_animimage_private.h | 892 | `a2b07314afd9beba8a6a3bffb5978cfa700873903ae35718205002fa4fe8648f` | 0 |
| external/lvgl/src/widgets/arc/lv_arc.c | 36673 | `ed6347f5ff868930ef45d245a98023e8e3ae17ea6f9fa273ad40913788f0a5c5` | 0 |
| external/lvgl/src/widgets/arc/lv_arc.h | 8111 | `c7a8609222fa28694a1646b55c5fba90f202a9589bdb3f8da3f8f1b2c1cbf877` | 0 |
| external/lvgl/src/widgets/arc/lv_arc_private.h | 1637 | `1eb31bc2b518360a0f6247f3d9cc66afc720ad9644d7e10e7dde9b2c80b550a7` | 0 |
| external/lvgl/src/widgets/arclabel/lv_arclabel.c | 19709 | `3c9ab9a2d8abf2ec6f855d4499a8aa1170815ef8f72fbc2163554bea9c7d6ea4` | 0 |
| external/lvgl/src/widgets/arclabel/lv_arclabel.h | 7455 | `282031fe85d46abc3ca6f2ff80b14b71fef305189872415c18cbef1cd2d79b8c` | 0 |
| external/lvgl/src/widgets/arclabel/lv_arclabel_private.h | 2212 | `ab9ea6aadc652d192ceed23f4cce9998dbea39c9b674a2cdf5f316c3a17a2d4b` | 0 |
| external/lvgl/src/widgets/bar/lv_bar.c | 24258 | `ac24457e63f831a7fdab81e44ee669591073a09fff0ca35f16f1c70522e76891` | 0 |
| external/lvgl/src/widgets/bar/lv_bar.h | 4731 | `fb739ad5392370b762532c0a61df1c3ef7a0ff77ced9085849e386f4d61576c2` | 0 |
| external/lvgl/src/widgets/bar/lv_bar_private.h | 1411 | `6c55351866f55b2401680065ed1bb517286fb2bc4f4963fc4b16334f57222d41` | 0 |
| external/lvgl/src/widgets/button/lv_button.c | 1594 | `792b2e7d2d440b9b099ef5c9dab62c2e6fd62bf018f30825f241727fcb560fb6` | 0 |
| external/lvgl/src/widgets/button/lv_button.h | 849 | `a5373650a63c4818004036d109c72886d1067acd77901cc5be675ee3b671e2c5` | 0 |
| external/lvgl/src/widgets/button/lv_button_private.h | 777 | `3c58c69ee43b7c119eb5026a63789ee7905586cb58fbfc6d3746ed65113c43dd` | 0 |
| external/lvgl/src/widgets/buttonmatrix/lv_buttonmatrix.c | 39637 | `899105e43c1098368b562f6bc8e88ea2db16d4ad25bca69f993e811604cf7db4` | 0 |
| external/lvgl/src/widgets/buttonmatrix/lv_buttonmatrix.h | 10309 | `2a58ddd955def471bcf46309a46f14143edcf6c407e65d84e8375167fe51e9a3` | 0 |
| external/lvgl/src/widgets/buttonmatrix/lv_buttonmatrix_private.h | 1534 | `217c197a0def005b7eefb9447a4856ae8137754a8d208d518d5ae2a0dfe18e43` | 0 |
| external/lvgl/src/widgets/calendar/lv_calendar.c | 17049 | `77931dc4509fd2e64d6b56980226152492798ae48f23af6e616c7a98ae1e8528` | 0 |
| external/lvgl/src/widgets/calendar/lv_calendar.h | 5516 | `1f102a7a1a167e39d4682fc5a6f8bafa2c09b28f9b6caf810c1126f3220f9bac` | 0 |
| external/lvgl/src/widgets/calendar/lv_calendar_chinese.c | 11127 | `3c5adca5a2ea8184cd6c0399844907ce7bec850ed7ac4b97b517b3b4ea9eb9a6` | 0 |
| external/lvgl/src/widgets/calendar/lv_calendar_chinese.h | 1596 | `d6819a00581c5b5c72d15024a42b0a5109949045d127de3aa2210904b3fbd8d1` | 0 |
| external/lvgl/src/widgets/calendar/lv_calendar_header_arrow.c | 4644 | `5a42b9eab6151336fad0c045c4f5ce7273cdc4b86e50e481db2d0afdba4e7bbe` | 0 |
| external/lvgl/src/widgets/calendar/lv_calendar_header_arrow.h | 1014 | `ed322fb42ac911ccbc63f7f1e37a2ae2c5f8465cbd2685e51ceb4d5190063e2e` | 0 |
| external/lvgl/src/widgets/calendar/lv_calendar_header_dropdown.c | 6233 | `4892e5e58cb97eabc4bec838398b85caf329f0fc7b02a88d1a1efda988e11e25` | 0 |
| external/lvgl/src/widgets/calendar/lv_calendar_header_dropdown.h | 1629 | `c39ffbacd33237f45ac3c53a3786991e9be5a7ee4177f1ae59954396e5ceb83a` | 0 |
| external/lvgl/src/widgets/calendar/lv_calendar_private.h | 1707 | `8780ecad6b85c35f734a2a20da5b8311c84d62d5c2ac33219f74fc3bc51a270f` | 0 |
| external/lvgl/src/widgets/canvas/lv_canvas.c | 12315 | `f5e65f05b3ccbcbe2e35920a924c1e61b55e696cdc6e3f86b2c9749abb51f2d1` | 0 |
| external/lvgl/src/widgets/canvas/lv_canvas.h | 5971 | `2b547c53a7d3ea96963b225ebb10bda3779477d90a5a44cd8819fe40ceb8aeb1` | 0 |
| external/lvgl/src/widgets/canvas/lv_canvas_private.h | 791 | `f6aa387198c498914abad0ac058e025f9842d479b5aabd7880929271153e19ce` | 0 |
| external/lvgl/src/widgets/chart/lv_chart.c | 55633 | `5ab1050c6981a037f915295f5f9a2f536a8679b2a78ae127f437dcf75bad1cd6` | 0 |
| external/lvgl/src/widgets/chart/lv_chart.h | 15420 | `b0e2d896e06fb3ed7919aa96dc27c34894714a942a3f06ecfdc82c24f3ca7bc8` | 0 |
| external/lvgl/src/widgets/chart/lv_chart_private.h | 1852 | `6e53ca0b9241edb3c15d9e470b700f5cf4cbfd88f950bc7aae02390dd01356b9` | 0 |
| external/lvgl/src/widgets/checkbox/lv_checkbox.c | 9269 | `c2a2c97b5012d542e783f1246d3125b515a0cee5c0a8d9fce941af15d6191775` | 0 |
| external/lvgl/src/widgets/checkbox/lv_checkbox.h | 1762 | `5448695c34a149458f04d10cb55a1f00a529c602da9cf3e2c8b13ca7d7e50143` | 0 |
| external/lvgl/src/widgets/checkbox/lv_checkbox_private.h | 838 | `eb48a09475723e95b84995c1828571c700bc350235f901f66d58a341919eded6` | 0 |
| external/lvgl/src/widgets/dropdown/lv_dropdown.c | 42213 | `3b9d793dbe4ac37c7879d2b1b93e8df12db4602d7d6ff6a37712d4064ed45f6c` | 0 |
| external/lvgl/src/widgets/dropdown/lv_dropdown.h | 8473 | `9724afc5ee20d6311487fafda59f001bfc57039d615c46eaefb533852fea05c3` | 0 |
| external/lvgl/src/widgets/dropdown/lv_dropdown_private.h | 1753 | `c664192b033e10c3b1ee6916d71f2dbfe07d50309955944adcc084a289f44ac9` | 0 |
| external/lvgl/src/widgets/image/lv_image.c | 33426 | `b8fa1ff90d3199c417d4b3e1ae474ce0100d2b7df265c8fca83c7de658657c54` | 0 |
| external/lvgl/src/widgets/image/lv_image.h | 11944 | `4674449acf594ee03e1f9ba7c24795e86fa31e63c7682292ef77408983fbae9d` | 0 |
| external/lvgl/src/widgets/image/lv_image_private.h | 1776 | `eacf3dde3339bf0b0150eaee07f5bcdb2099eba28daefebf1dddcdd7c205a83d` | 0 |
| external/lvgl/src/widgets/imagebutton/lv_imagebutton.c | 11722 | `4451d5dd7b1348860782f2dbe164d99503076d4e6626d2b513a8a781f1fcde58` | 0 |
| external/lvgl/src/widgets/imagebutton/lv_imagebutton.h | 3663 | `64d1bbebd3a490a8e9c57bc825059c8379a21b88fbac2efaa89c142f0b7053a1` | 0 |
| external/lvgl/src/widgets/imagebutton/lv_imagebutton_private.h | 1208 | `b42f109ef7dfc5201bd62232a0463ef181743a318ce9aac35aee7673c51c1b01` | 0 |
| external/lvgl/src/widgets/keyboard/lv_keyboard.c | 18283 | `ebeaf92da138676a72c705db67d9f2b56f6658e646047fadb2d9b0732a0e378d` | 0 |
| external/lvgl/src/widgets/keyboard/lv_keyboard.h | 5281 | `077da9d353ec8275059a6ed4643c781df8298ee351556a9e376aa2dd9428c225` | 0 |
| external/lvgl/src/widgets/keyboard/lv_keyboard_private.h | 971 | `3dca68ab692f6570df240e0f9706fabb2d3850a313061f167ad73c929ffd02e6` | 0 |
| external/lvgl/src/widgets/label/lv_label.c | 50177 | `82dc5fe50869a85312b1cefd37017293a024221ab4c71ddf06b43e7c6176f56a` | 0 |
| external/lvgl/src/widgets/label/lv_label.h | 10099 | `720121d2292b43350bc1e986e7f7ece38e5d6be8042cff1c45e36d175ed3b4d6` | 0 |
| external/lvgl/src/widgets/label/lv_label_private.h | 1783 | `b0d96fbbd7d216f926a673b98a03f79a7c8fd3f55890b71f1b4c46d98988651a` | 0 |
| external/lvgl/src/widgets/led/lv_led.c | 5908 | `1d1a3b3f296289d0530461544fb2cc1eb6042f1ee50d14c50e7128c513670a9a` | 0 |
| external/lvgl/src/widgets/led/lv_led.h | 1983 | `bd8f1531b0df411eeb04c146189879a75835e185c41df38ffda07774b03b9635` | 0 |
| external/lvgl/src/widgets/led/lv_led_private.h | 787 | `5ddc7b9581f7813bc3c03a07b20c06e31bee20e44ef9d1e958e14f8a3a171c31` | 0 |
| external/lvgl/src/widgets/line/lv_line.c | 7277 | `e3f0318f970cdbf33d4f0a151323bb1a47c3afa0fec83bec0b505489822a6cb8` | 0 |
| external/lvgl/src/widgets/line/lv_line.h | 3409 | `fbd0140da04c4c90c0f9dcf2671820bb4708897571ab8b4460d5e2c83e3a6d29` | 0 |
| external/lvgl/src/widgets/line/lv_line_private.h | 1153 | `bfd93ccc72f5769b03748c14323e95a87a25ee7b4cf7e6786976686479d08905` | 0 |
| external/lvgl/src/widgets/list/lv_list.c | 3364 | `5d3a883118cf688f14683b63e13dcc648da1334de2658979aed01c2f94348225` | 0 |
| external/lvgl/src/widgets/list/lv_list.h | 2284 | `0c2d57924af52e016372523c9f43f89269c180f487a96000d661bc9a8e3b382c` | 0 |
| external/lvgl/src/widgets/lottie/lv_lottie.c | 7397 | `9e014662a251372fe9c40c4028fc76bf7b7178f6b42034b6b83b377cdcb25882` | 0 |
| external/lvgl/src/widgets/lottie/lv_lottie.h | 2646 | `8eeb596ffcf969b25954db0fe7aa68b72d84cfe8b4e4e01552b30217be78e4d5` | 0 |
| external/lvgl/src/widgets/lottie/lv_lottie_private.h | 995 | `5e18bb1ee0349716d4ab02c420ccd6ee1ab03666662f8b5c4272624c090a1611` | 0 |
| external/lvgl/src/widgets/menu/lv_menu.c | 26353 | `d71f2f6db8c65c3ba9a92791104a20204f39a001c1a642772db4f7bb159da79e` | 0 |
| external/lvgl/src/widgets/menu/lv_menu.h | 6851 | `e15b496883a185d508467913856a26d11d3f08848c0c7d12aecd9794515b7b22` | 0 |
| external/lvgl/src/widgets/menu/lv_menu_private.h | 1774 | `83b80efa18dc9f46bbaba2cb864f42c4b083341774bda30fd61a5b446b6c1a39` | 0 |
| external/lvgl/src/widgets/msgbox/lv_msgbox.c | 8862 | `62bd69088fbdbe20ee4b56a529d209fe0ef9d8de136a275e76da6632c5286706` | 0 |
| external/lvgl/src/widgets/msgbox/lv_msgbox.h | 3731 | `b94c9f7dc23c39b70d085919f27968cfd8692d6dc433fd6f1f120f30294963d0` | 0 |
| external/lvgl/src/widgets/msgbox/lv_msgbox_private.h | 859 | `78088a5fd5982fa15b82593193152bc6b92c96184edfb1085be1508a209bbd59` | 0 |
| external/lvgl/src/widgets/objx_templ/lv_objx_templ.c | 3338 | `a94e852c094ff6c2c783b3ae987f4ac86459b6656c600f4823e99d4c6f4bd71e` | 0 |
| external/lvgl/src/widgets/objx_templ/lv_objx_templ.h | 1584 | `8861758b3c67c6836a53f69d186a746a1bd4d9ad19f8715819828b978155643a` | 0 |
| external/lvgl/src/widgets/property/lv_animimage_properties.c | 694 | `855918a1be03919099a0394f89b9cb0cecb617c4f4b154de3ce31dab93ef7d33` | 0 |
| external/lvgl/src/widgets/property/lv_dropdown_properties.c | 1000 | `c46c467ae40faba6e7e6daaf7af2b1988613f4f0c1c43435acaf09130dcd905f` | 0 |
| external/lvgl/src/widgets/property/lv_image_properties.c | 1071 | `b7ce94f64743a8b26d74a31fca92f2c9d9ca54ef1c6ae2b785438d394e099d50` | 0 |
| external/lvgl/src/widgets/property/lv_keyboard_properties.c | 686 | `42db2b3f7e82d0b02aec7b11a55b089d9caf14b63b4db0746e383b465fa0e066` | 0 |
| external/lvgl/src/widgets/property/lv_label_properties.c | 669 | `41a77ebb1f97559d8ebd37c627751ca52eba4cbdca083e1b69ff3921119a3774` | 0 |
| external/lvgl/src/widgets/property/lv_obj_properties.c | 5139 | `9fb7af523a72a3fb8f7ebc939def3af1d7c01c34781d6afc85e3a1196988ded8` | 0 |
| external/lvgl/src/widgets/property/lv_obj_property_names.h | 901 | `129be4260ac3d94c7637169a60fcd76b63cd8a30d3206af72a23feb5e2e01300` | 0 |
| external/lvgl/src/widgets/property/lv_roller_properties.c | 607 | `bf76dc63a7ddd0ad401c6e327d4f6d672569cc2ef29887aad74b77d4663d44b6` | 0 |
| external/lvgl/src/widgets/property/lv_slider_properties.c | 911 | `6e3189f68180dd5b90c6a9a7f73ca32b048a4dd325d33a76743dae5515f3af39` | 0 |
| external/lvgl/src/widgets/property/lv_style_properties.c | 8255 | `e40d9ddba9701a2a93b8fbe702a1517d9971d099cc1b8f097a62b9f46b9f946e` | 0 |
| external/lvgl/src/widgets/property/lv_style_properties.h | 12998 | `825c4877999765928e72c95992e8355ae7577a3b6d92e8af596ec4ca898587e8` | 0 |
| external/lvgl/src/widgets/property/lv_textarea_properties.c | 1453 | `45c88147f26cbb85a28a7a87dfc2ac70345ba55e908a2c112f4441ab1c81f767` | 0 |
| external/lvgl/src/widgets/roller/lv_roller.c | 34299 | `91dda7dc1cfab908b9f5f665f098cbfdc2caf3fd3518c346f52ed0c72f87463e` | 0 |
| external/lvgl/src/widgets/roller/lv_roller.h | 4890 | `5780babd0eff95c207a48480ffc7f20cb94cee9bd5bc6860abe84eacf4e35a89` | 0 |
| external/lvgl/src/widgets/roller/lv_roller_private.h | 1071 | `11a1aabae67e273839a47b00c56ab8726a44746600616f5254982266e1aeae40` | 0 |
| external/lvgl/src/widgets/scale/lv_scale.c | 67684 | `c25d05846b0d02e93b0a2b1c2dffa19547d28e432d4bcd060f80f01f47931194` | 0 |
| external/lvgl/src/widgets/scale/lv_scale.h | 12220 | `68af8395c779997cd022fc26aa002d83f42ca06755edb44750900d10ad8315fe` | 0 |
| external/lvgl/src/widgets/scale/lv_scale_private.h | 4169 | `f53ea6ffcea11e323b373813ae450d24b3ef1985565199ebd6f2f40d2a918a25` | 0 |
| external/lvgl/src/widgets/slider/lv_slider.c | 24686 | `04f85af6888db4ebcd1f27b9187c242f3395361025b0ced47eb830ce4b6134c1` | 0 |
| external/lvgl/src/widgets/slider/lv_slider.h | 6033 | `407170590001420262cb00847316969f286c68eac3531d43a0aa90fffd04d804` | 0 |
| external/lvgl/src/widgets/slider/lv_slider_private.h | 1082 | `5e260e41b42cf3e29a852dd4c86e828a6af733972ef72c60ef0f1c778363e4a9` | 0 |
| external/lvgl/src/widgets/span/lv_span.c | 48073 | `f596e2284c87a2108e232bf80a61a83d8e41bb22d5036916375d79ac5f9854df` | 0 |
| external/lvgl/src/widgets/span/lv_span.h | 11701 | `bac0ef29b4202c37603260d66f8d2f3b66b84b20d152d7c31ba46b0268d1ae13` | 0 |
| external/lvgl/src/widgets/span/lv_span_private.h | 1375 | `6a69d21b844a8061f03b04af3e00e0134d0448884efd567a2f3a98fb6ec8b1b7` | 0 |
| external/lvgl/src/widgets/spinbox/lv_spinbox.c | 16494 | `364ef15e72d0cd555166422ae2245008bd489c80305c849fd84774a25797dc37` | 0 |
| external/lvgl/src/widgets/spinbox/lv_spinbox.h | 5238 | `ec782e8b4d9ce4ff4c1d2be2ecfefac1a687b8bdddbcfb35018ff6ba2849ecde` | 0 |
| external/lvgl/src/widgets/spinbox/lv_spinbox_private.h | 1215 | `c369823ecae7dbc56cbaa603ba6306dfc3c050d80d931e3c859d04684c19fab2` | 0 |
| external/lvgl/src/widgets/spinner/lv_spinner.c | 2631 | `2481c33fbdbb5b9e960fb906636bb021f388bab62ebadfd58be871723e4b335a` | 0 |
| external/lvgl/src/widgets/spinner/lv_spinner.h | 1307 | `d921ef516b71dcaa4c6b22e9b4cee0ef97656061026ae4de462a1d37c4b3dd28` | 0 |
| external/lvgl/src/widgets/switch/lv_switch.c | 10460 | `042cb210c0ae31de121c228620db34d4e0ef09a77c0a6846540a4d7e062eb40e` | 0 |
| external/lvgl/src/widgets/switch/lv_switch.h | 1775 | `9e63c9ac9d3ff66f2cd3d4678f4dec98241c4f54857792f22bbda14ed7f467e7` | 0 |
| external/lvgl/src/widgets/switch/lv_switch_private.h | 875 | `4779d1a427c11cf549b2dae16d7e1b6e01cd6eda6bceb2bc784a955c47ba7ff3` | 0 |
| external/lvgl/src/widgets/table/lv_table.c | 39006 | `a4c33f085ea91e6520dfd991d9fdd2bb687e582f8d5672e0161567973d28658c` | 0 |
| external/lvgl/src/widgets/table/lv_table.h | 6898 | `c175832c138c0bfd686cbba880e21ced000bdfd37e9591a62c7c31194aaf0479` | 0 |
| external/lvgl/src/widgets/table/lv_table_private.h | 1061 | `bb00879178b9e1ee5ed436ddafbbfb1931bd8096a2479036ad44e4a8cdcafaf4` | 0 |
| external/lvgl/src/widgets/tabview/lv_tabview.c | 11298 | `b60bab81372de5c65cb1f3b97b374fe95bd7e8747b774961c778ec0383004b7f` | 0 |
| external/lvgl/src/widgets/tabview/lv_tabview.h | 3321 | `27ab978c44ef10a9de1b797a0841a525168997c4cf83238422c6507f93b968c8` | 0 |
| external/lvgl/src/widgets/tabview/lv_tabview_private.h | 819 | `f2b48583ddc5a0f548c408833791fb165dafe29abab8c834a18a6484367ac24b` | 0 |
| external/lvgl/src/widgets/textarea/lv_textarea.c | 47048 | `a25877928de5cfd36185d03bd8b47871b7172af526cff8d6e45cafcbdcd1d8ea` | 0 |
| external/lvgl/src/widgets/textarea/lv_textarea.h | 11124 | `e4d4fbc93a9ef1f967920caddfe67f93baeccc4eaefa7397c2aac90536928993` | 0 |
| external/lvgl/src/widgets/textarea/lv_textarea_private.h | 2510 | `f698207fc5a265310c7831f0be8f56a36bd4b1e4f229c8b314952a28a9221788` | 0 |
| external/lvgl/src/widgets/tileview/lv_tileview.c | 5448 | `d170b80b605bd160a4a26e289305c647c08653dcabacf0e2f24479a9304332d1` | 0 |
| external/lvgl/src/widgets/tileview/lv_tileview.h | 2346 | `4a57c8b7b68506b248d02e48b4b51d16de812f3ccaa652a74f6490479222c029` | 0 |
| external/lvgl/src/widgets/tileview/lv_tileview_private.h | 876 | `9f66c4d9e7556d6580772c618500a3519854264b159b4266085978b26b134c6c` | 0 |
| external/lvgl/src/widgets/win/lv_win.c | 2785 | `b134782018d2c18dcce20c2158ad194eee9eb1aafae7696ecaa08646777a849f` | 0 |
| external/lvgl/src/widgets/win/lv_win.h | 1739 | `8ff6fdd0a92320f6ffb6933c62ad4c94ca3e4d48a1657ab652208cc2fd28422f` | 0 |
| external/lvgl/src/widgets/win/lv_win_private.h | 742 | `c3c7d3eb71d15f58980eb028eb719957501a34af5cf2fb00da54d4ed415a22e6` | 0 |
| external/optiga-trust-m/config/mbedtls_default_config.h | 44543 | `5d2d35534e9e4b30148baf3d2349f137c010e3a0f4f7d6d813245752b4905a05` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/Hacl_Curve25519.h | 1096 | `463d56088a31cbacf694eb20a7397e1689da0ba5fc0b37445784c08df5465fc0` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/everest.h | 8235 | `ddc6c96ec9598fe10c389c155467d4a2cdedf488da8d2186303442ede7a4db08` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/kremlib.h | 985 | `05db27dda38b43f0d9745a36e20f6ec5ce18fd6f8c130d64c3b8faf27400b4fb` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/kremlib/FStar_UInt128.h | 7003 | `4b1ee5b71376af6e6d2f80303b7fdda4427cdf0be8c153dd6821215434ed5588` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/kremlib/FStar_UInt64_FStar_UInt32_FStar_UInt16_FStar_UInt8.h | 10800 | `32ba176eeced425da0d539d3a406275bb880cc78fa67c5e3a4937206f0e42122` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/kremlin/c_endianness.h | 6747 | `98dfac843cae9138c543d90e900029a04cab0a990c714e5d9edc5ee0d8bce322` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/kremlin/internal/builtin.h | 471 | `836d849eb5f824531d5c4e9d3bec50d203461b672b868d17f8f618bd60655fd5` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/kremlin/internal/callconv.h | 1416 | `d62185807f5b016b46f9fd10bcf5ec1debdaba721909e4c59c8b181cb9268120` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/kremlin/internal/compat.h | 1346 | `7304c71089f76077ae2b5cbcc9493512bb71c8a615bbec5eb3823f5d3f9b4888` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/kremlin/internal/debug.h | 3056 | `f154ee91dee1dba31c1039d28b3b39edd9d08b20abac62c33ef6cfff1363ebfc` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/kremlin/internal/target.h | 3672 | `923a6430d90e681115c7467dc553a54750292da2d5119b40e2d144d4550969aa` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/kremlin/internal/types.h | 2009 | `c3def1c71d571f97be579e535ad79f892be998b1b5702bd68608925b2a63ae8e` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/kremlin/internal/wasmsupport.h | 237 | `6e1b236e46ba8f6df8b503a0ec4283b795db56950eb24623c96801a072f78716` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/vs2010/Hacl_Curve25519.h | 1078 | `c2e5a6ee616f8410ce8581dd1740a5b3d56dd036904a24ec431bbf0ccfcfeb0d` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/vs2010/inttypes.h | 1029 | `485a92f0e19ee0f9a9ea3033f995162d4083a065ef73b004ab57fda234983daa` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/vs2010/stdbool.h | 960 | `a3e67d667976f94bda628738440fd2b8110eccb49cac509ab4bd2675640fd987` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/include/everest/x25519.h | 6225 | `da28aebd8413ebfbe7b0d8069d40ab7cebf24725b5c41c83a3dbd316622c8f2c` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/Hacl_Curve25519.c | 22405 | `ff662cfae5e65d968d487a687db5fdc05c357ec9b2035ac9e380c9f8ec7eb6eb` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/Hacl_Curve25519_joined.c | 1261 | `3a208016cbdb5a5368562c59a346f3b742ea8adf00f809dfafdf771aeabbc9c3` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/everest.c | 3718 | `2d7f6fccc2e11f3eafea2e606f23ef57d55fcc83f346b8b178a4cdc0d3036bd7` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/kremlib/FStar_UInt128_extracted.c | 14010 | `b75508632b4729497ae042851e3e3b996a93e2ef5ad0688785931725361bc88f` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/kremlib/FStar_UInt64_FStar_UInt32_FStar_UInt16_FStar_UInt8.c | 5314 | `9a3504b115dcc34581dff4dd1f4adb96f7119d2d4d5e0612fc0342a1562727dc` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/legacy/Hacl_Curve25519.c | 24161 | `fd769ba72bed1ca61a4e286d7ef1751931fda5707881df514335f97ccafb5984` | 0 |
| external/optiga-trust-m/external/mbedtls/3rdparty/everest/library/x25519.c | 5937 | `b4dc100b030f55689fdcde10014dfb3f0a57f6d1f3362ef2e5f0f70686b381ba` | 0 |
| external/optiga-trust-m/external/mbedtls/configs/config-ccm-psk-dtls1_2.h | 3142 | `c4f842bf5525957ea482df6003c742766fde695574a27c221d51f9c5b4a2fed6` | 0 |
| external/optiga-trust-m/external/mbedtls/configs/config-ccm-psk-tls1_2.h | 2725 | `8e6f83df978d5fe30a8c1872ce957bb4f448d10f6d8886c8a7d4e11010a7ba3b` | 0 |
| external/optiga-trust-m/external/mbedtls/configs/config-mini-tls1_1.h | 1978 | `9bfb7c3305fce663a9f1109ae39e05ce7375bb1d694c4be212e63d31638c8195` | 0 |
| external/optiga-trust-m/external/mbedtls/configs/config-no-entropy.h | 2016 | `f4641d2141b18ab6ab000079d4ac4e7d1b5b9c4205d54737efbea64237e7fce1` | 0 |
| external/optiga-trust-m/external/mbedtls/configs/config-suite-b.h | 3418 | `1804e1026e204cc0b913577fa4253d14fbf651473f3ea31c5f609955f8a62d98` | 0 |
| external/optiga-trust-m/external/mbedtls/configs/config-symmetric-only.h | 2179 | `436d2d57c0204a0abffab65b7713baf8f79bd339f106c54d83cc84ecf1ec8c1e` | 0 |
| external/optiga-trust-m/external/mbedtls/configs/config-thread.h | 2221 | `e96fc915b82f3553e00af693c64712db4e13e4e8cf23acee4258bf729ef57cd4` | 0 |
| external/optiga-trust-m/external/mbedtls/docs/conf.py | 1179 | `ddb943e9ccdb4892b01b9b798519604def81196e1dd94097495d92f63dcf38ea` | 0 |
| external/optiga-trust-m/external/mbedtls/docs/requirements.txt | 1344 | `dce4f3d684dc1e1270a8b811bbff57e50f6f293bfa448e2d725b22a1258449fc` | 0 |
| external/optiga-trust-m/external/mbedtls/doxygen/input/doc_encdec.h | 2728 | `6c812f9c228d9cdc6b37748beeeabded85e85857f8c8f00d4c1d42b349eaff70` | 0 |
| external/optiga-trust-m/external/mbedtls/doxygen/input/doc_hashing.h | 952 | `55fe54656b1ad1ab2d4a12e6ec41d5019475a23f4b7df4b7c9fbd8fc21c2a5e9` | 0 |
| external/optiga-trust-m/external/mbedtls/doxygen/input/doc_mainpage.h | 497 | `4f948452f8539361ab323bf050f8981cf27dd1e0a70bd235094a92aa64faa6fa` | 0 |
| external/optiga-trust-m/external/mbedtls/doxygen/input/doc_rng.h | 1174 | `47237b1eeb5093bdc06ff0373b3170efef8b860d910429894fcc562f7fac893d` | 0 |
| external/optiga-trust-m/external/mbedtls/doxygen/input/doc_ssltls.h | 1425 | `3023fe21b3b398afd527ff00a38d142e883b1256bd510e140a364eff5c51f4fa` | 0 |
| external/optiga-trust-m/external/mbedtls/doxygen/input/doc_tcpip.h | 1143 | `21355833cbc6d797b675fbe968f4a86066dcd9dbbeaa3684822be876e76231e5` | 0 |
| external/optiga-trust-m/external/mbedtls/doxygen/input/doc_x509.h | 1165 | `ade5c11ce2be981f62d75d737a5327da1ad7a7742ecbf702c490299c5798952f` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/aes.h | 29146 | `cdadaa287185b4ed689b8190c3e82f2e2bdb20bdaeb1afa1849797a40d4226ee` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/aesni.h | 5771 | `eafbf804daa73bd2916bd87f6fe4744d61a9260161f03db7fdb6b102424b7cbc` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/arc4.h | 3514 | `d66d70b8dfc0b53452c7617fe07bff4f57c8f9f1994924361443f632bbb867c5` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/aria.h | 15462 | `20664462c7aa9d3607fa5b517ed0acc2cddf9b73ca1a7d25c5ece2f751e9648d` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/asn1.h | 25621 | `833a64871d59694686e23bd85e655c0bcbb004f0775bb5b91a9068ce54e8eeea` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/asn1write.h | 15838 | `9cf3e48c2ca600d45360df23c97f66074661df52bfeecb635494ad52effb20b0` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/base64.h | 2685 | `dc7ef7c15b67e935cd01ceee229aa45ef0381c4e16999b9961c4f2c0024e8a30` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/bignum.h | 45717 | `b756e8734133affa7c6eee0012e1d7ea09f991385327269add333fe1eff28de6` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/blowfish.h | 12081 | `d21f1b322d233db8cddc2c486a0d075be4adc106a477bff2de42d98ca0e1934b` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/bn_mul.h | 39354 | `268324971674f7187be79de77d1e711ce1df112f328ab104d3eec456ba77787d` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/camellia.h | 13657 | `367b12fc0a88e140f33c9048c4e2fa2d80b8b6fa2628a6e83dc1d54641601fe9` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/ccm.h | 13561 | `b8f5d5163cfa884d038c53db38d5466d484080bd76728a1b1656d03b9c96f969` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/certs.h | 8777 | `f3750cf0092afc527c9cf18cdf0f3db63a6f37e1031416b22862cb4ad5524742` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/chacha20.h | 8152 | `c30b39f660fed23d810072271da7b398686b52af01fe9f34a61022cc90c20e0d` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/chachapoly.h | 15531 | `8da9cde93f46936690b869e7810531e610b37b514ac92ca29300ab2a9e800f7c` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/check_config.h | 38401 | `7896c05cd6f28fda00548e6dc2ff70434e6db8f660dc70f6117a8602c52bcb8a` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/cipher.h | 53820 | `58fcbbcc35638a6ad1a71232f406441f1530ab15c25704643665524d4d74d991` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/cipher_internal.h | 4317 | `a2f3b2fb6347c613ba9eff1b5e16e2ccfe0b921874051a38430e47280b2936b9` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/cmac.h | 9798 | `a20ad14a7b8bf5c8277461d60725103b4fb3fef9ce51f0c8876256219c4f5896` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/config_psa.h | 26677 | `52c260c3883770d2fff61ec760f936d3b20e584afbeb85e0c133ec73434f05a0` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/constant_time.h | 954 | `0e4eb0021fe1f271edb21a2fc80bad0c3e25bc48000b789e5986bea7fe5c3ecf` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/ctr_drbg.h | 25108 | `39dd6377a415897d0e26e81ca6bf1f70f1de5898d5528a73a94f9e15d3645566` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/entropy_poll.h | 2692 | `82def6b820fa4127de1274e04c7e5deb344187acbc3d2bc7efbb5c98c2752448` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/havege.h | 1312 | `13a8f93d9b584e280e0a7dbc776c4efba7353e97e33ba5214bc0493048bfa35c` | 0 |
| external/optiga-trust-m/external/mbedtls/include/mbedtls/net.h | 619 | `02c9a6ed25f9361bd5b3ee2df5a82a85848d45b1e603a396c5f7e99602571e57` | 0 |
| external/optiga-trust-m/external/mbedtls/scripts/mbedtls_dev/__init__.py | 146 | `b4c5c80120c7707ab1c6e27adc8b6dbab55388d5451547422263e071421f396b` | 0 |
| src/rust/bitbox-secp256k1/depend/secp256k1-zkp/src/int128_impl.h | 376 | `5683c02dfc495639da259d80624711c1c449bbaee6186729e399e713a28b4719` | 0 |
