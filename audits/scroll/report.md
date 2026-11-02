# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** scroll @ 3046bbd18a6a · Scroll — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-30 23:51 UTC |
| Версия отчёта | 1 |
| Запуск аудита | c69e1f34-353d-49b8-8de3-4ff0b67f4ee6 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `2ba03a86d58a4d1243d2942f3659345ecc600994baf0104b133b23a18e89dfb6` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **1**
- Высокая: **9**
- Средняя: **11**
- Низкая: **36**
- Информационная: **57**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 56
- Подтверждённая ошибка конфигурации: 1
- Потенциальный криптографический риск: 6
- Долгосрочный постквантовый риск: 4
- Рекомендация по улучшению: 46
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/scroll-tech/scroll> @ `3046bbd18a6a05bf29dd3ffef7b5676203201050` — ссылки в доказательствах открывают строки на этом коммите.

387 файлов, всего 2800964 байт, редактирований: 0; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 218 | .github/scripts/bump_version_dot_go.mjs: 37 lines scanned with 16 rule patterns and 136 registry patterns; bridge-history-api/abi/backend_abi.go: 344 lines scanned with 16 rule patterns and 136 registry patterns; bridge-history-api/cmd/api/app/app.go: 114 lines scanned with 16 rule patterns and 136 registry patterns |
| dependencies | проверено | 16 | Cargo.lock: 938 dependencies parsed (938 pinned); Cargo.toml: 29 dependencies parsed (7 pinned); bridge-history-api/go.mod: 111 dependencies parsed (111 pinned) |
| tls_code | проверено | 1 | bridge-history-api/cmd/api/app/app.go: TLS key-exchange settings read |
| tls_code | Недостаточность данных | 5 | bridge-history-api/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS; common/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS; coordinator/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS |
| smart_contracts | проверено | 152 | scroll-contracts/lib/solmate/src/auth/Auth.sol: built-in Solidity pattern checks; scroll-contracts/lib/solmate/src/auth/Owned.sol: built-in Solidity pattern checks; scroll-contracts/lib/solmate/src/auth/authorities/MultiRolesAuthority.sol: built-in Solidity pattern checks |
| slither | не проверено | 152 | slither is not installed on the server (pip install slither-analyzer + solc) |
| osv_advisories | проверено | 1 | 1000 pinned packages queried at OSV.dev; 36 affected |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- tls_code — Недостаточность данных: 5 (примеры: bridge-history-api/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS; common/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS; coordinator/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS)
- slither — не проверено: 152 (примеры: slither is not installed on the server (pip install slither-analyzer + solc))

## 5. Краткое описание архитектуры

Static review of the source tree scroll at 3046bbd18a6a05bf29dd3ffef7b5676203201050. 387 files analysed; of 883 files, 311 are test, fuzzing, benchmark or example code and were left out, 185 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .claude/agents/local-e2e-tester.md, .claude/agents/skill-tester.md, .claude/agents/zkvm-prover-runner.md, .claude/settings.json, .claude/skills/agent-memory/SKILL.md. 380 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. 163 files come from directories a .gitmodules pins and are read as shipped source rather than skipped as a dependency cache: scroll-contracts (163). No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **0** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 7.6%

## 7. Подробное описание находок

### QSI-2026-09219 — github.com/gin-contrib/cors v1.5.0 затронут GHSA-869c-j7wc-8jqv (CVE-2019-25211, GO-2024-2955)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/gin-contrib/cors@v1.5.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 54.2 / 100
- CVSS v3.1: 9.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-869c-j7wc-8jqv (CVE-2019-25211, GO-2024-2955) для пакета Go github.com/gin-contrib/cors версии v1.5.0: Gin mishandles a wildcard at the end of an origin string. Проверенный код называет github.com/gin-contrib/cors.New: затронутый код может быть достижим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-869c-j7wc-8jqv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-869c-j7wc-8jqv](https://osv.dev/vulnerability/GHSA-869c-j7wc-8jqv) · line 8 · SHA-256 dc496aa23daf62242a3c7d40b2e031e7ee93e0af363e203c2866389d3a5c53cc_

```
{"id": "GHSA-869c-j7wc-8jqv", "aliases": ["CVE-2019-25211", "GO-2024-2955"], "modified": "2025-11-03T22:47:01Z", "summary": "Gin mishandles a wildcard at the end of an origin string", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.6.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09123 — Проверка TLS-сертификата отключена в bridge-history-api/cmd/api/app/app.go

- Серьёзность: **Высокая** · Классификация: Подтверждённая ошибка конфигурации · Уверенность: Высокая
- Затронутый актив: `file:bridge-history-api/cmd/api/app/app.go`
- Источник данных: bridge-history-api/cmd/api/app/app.go
- Метод обнаружения: Сопоставление регулярных выражений с API конкретного языка.
- Анализатор: source_code 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 70.4 / 100
- CVSS v3.1: 6.8 (`CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

1 случаев отключения проверки (InsecureSkipVerify: true), первый — строка 69.

**Возможные последствия.** Соединения уязвимы к перехвату «человек посередине».

**Шаги воспроизведения.**

```
Откройте строка 69 в предоставленном файле bridge-history-api/cmd/api/app/app.go и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [bridge-history-api/cmd/api/app/app.go](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/bridge-history-api/cmd/api/app/app.go#L69) · line 69 · SHA-256 edce4750653abe234eb4418e449aa04c9c36023fa0403f3bf0c6aa2b163c64c7_

```
   67 | 		opts.TLSConfig = &tls.Config{
   68 | 			MinVersion:         tls.VersionTLS12,
   69 | 			InsecureSkipVerify: true, //nolint:gosec
   70 | 		}
   71 | 	}
```

**Ограничения проверки.** Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Удалите отключение; используйте корректный набор УЦ или пиннинг.

**Повторная проверка.** Повторно просканируйте код и проверьте места вызова из доказательства.

### QSI-2026-09220 — github.com/btcsuite/btcd v0.20.1-beta затронут GHSA-27vh-h6mc-q6g8 (CVE-2024-38365, GO-2024-3189)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/btcsuite/btcd@v0.20.1-beta`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 50.2 / 100
- CVSS v3.1: 7.4 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H`)

OSV.dev сообщает GHSA-27vh-h6mc-q6g8 (CVE-2024-38365, GO-2024-3189) для пакета Go github.com/btcsuite/btcd версии v0.20.1-beta: btcd did not correctly re-implement Bitcoin Core's "FindAndDelete()" functionality. Проверенный код называет github.com/btcsuite/btcd/txscript.Engine.Step: затронутый код может быть достижим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-27vh-h6mc-q6g8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-27vh-h6mc-q6g8](https://osv.dev/vulnerability/GHSA-27vh-h6mc-q6g8) · line 26 · SHA-256 ff74528063f3adda5c06b22b192859164e12b45da07b71183a0e524bc21207b8_

```
{"id": "GHSA-27vh-h6mc-q6g8", "aliases": ["CVE-2024-38365", "GO-2024-3189"], "modified": "2025-08-21T04:05:13Z", "summary": "btcd did not correctly re-implement Bitcoin Core's \"FindAndDelete()\" functionality", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.24.2-beta.rc1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09193 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0340

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает RUSTSEC-2026-0340 для пакета crates.io quinn-proto версии 0.11.16: Peer minimum ACK delay can panic quinn-proto when ACK_FREQUENCY transmission is enabled. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0340
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0340](https://osv.dev/vulnerability/RUSTSEC-2026-0340) · manifest · SHA-256 20321fd13a708b936ab6ccc115a6ed97f9b78eb43a4e76d134ec1664a5fc8feb_

```
{"id": "RUSTSEC-2026-0340", "aliases": ["GHSA-3g6h-r5qx-f6hq"], "modified": "2026-10-12T18:15:01.975478256Z", "summary": "Peer minimum ACK delay can panic quinn-proto when ACK_FREQUENCY transmission is enabled", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.11.18).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09194 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0341

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает RUSTSEC-2026-0341 для пакета crates.io quinn-proto версии 0.11.16: Stream reassembly memory-exhaustion guard in quinn-proto can be bypassed. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0341
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0341](https://osv.dev/vulnerability/RUSTSEC-2026-0341) · manifest · SHA-256 843224ae2e1a0c898b003d66aa1610a8f10928c662ad0f000421250465a638ae_

```
{"id": "RUSTSEC-2026-0341", "aliases": ["GHSA-qfwj-vfxf-92j2"], "modified": "2026-10-12T18:15:01.969505433Z", "summary": "Stream reassembly memory-exhaustion guard in quinn-proto can be bypassed", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.11.17).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09132 — Возможный повторный вход (внешний вызов до изменения состояния) в scroll-contracts/src/L1/L1ScrollMessenger.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:scroll-contracts/src/L1/L1ScrollMessenger.sol`
- Источник данных: scroll-contracts/src/L1/L1ScrollMessenger.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 36.5 / 100
- CVSS v3.1: неприменимо

В функции relayMessageWithProof внешний вызов в строка 192 предшествует записи состояния в строке 194. (см. SWC-107)

**Возможные последствия.** Контракт атакующего может выполнить повторный вход до обновления состояния и вывести средства.

**Шаги воспроизведения.**

```
Откройте строка 192 в предоставленном файле scroll-contracts/src/L1/L1ScrollMessenger.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/L1ScrollMessenger.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/L1ScrollMessenger.sol#L192) · line 192 · SHA-256 f4f1b0112884e9b3d0e334f42c4814dc01366df462038674f7f86449d010bc2a_

```
  190 | 
  191 |         xDomainMessageSender = _from;
  192 |         (bool success, ) = _to.call{value: _value}(_message);
  193 |         // reset value to refund gas.
  194 |         xDomainMessageSender = ScrollConstants.DEFAULT_XDOMAIN_MESSAGE_SENDER;
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Примените шаблон checks-effects-interactions и/или ReentrancyGuard.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09133 — Возможный повторный вход (внешний вызов до изменения состояния) в scroll-contracts/src/L1/L1ScrollMessenger.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:scroll-contracts/src/L1/L1ScrollMessenger.sol`
- Источник данных: scroll-contracts/src/L1/L1ScrollMessenger.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 36.5 / 100
- CVSS v3.1: неприменимо

В функции replayMessage внешний вызов в строка 231 предшествует записи состояния в строке 244. (см. SWC-107)

**Возможные последствия.** Контракт атакующего может выполнить повторный вход до обновления состояния и вывести средства.

**Шаги воспроизведения.**

```
Откройте строка 231 в предоставленном файле scroll-contracts/src/L1/L1ScrollMessenger.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/L1ScrollMessenger.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/L1ScrollMessenger.sol#L231) · line 231 · SHA-256 da026ca30bc15720b495ea1fae4875e46ecf02996c36ba2e5fedfda59cdee030_

```
  229 |         require(msg.value >= _fee, "Insufficient msg.value for fee");
  230 |         if (_fee > 0) {
  231 |             (bool _success, ) = feeVault.call{value: _fee}("");
  232 |             require(_success, "Failed to deduct the fee");
  233 |         }
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Примените шаблон checks-effects-interactions и/или ReentrancyGuard.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09147 — Возможный повторный вход (внешний вызов до изменения состояния) в scroll-contracts/src/L2/L2ScrollMessenger.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:scroll-contracts/src/L2/L2ScrollMessenger.sol`
- Источник данных: scroll-contracts/src/L2/L2ScrollMessenger.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 36.5 / 100
- CVSS v3.1: неприменимо

В функции _executeMessage внешний вызов в строка 159 предшествует записи состояния в строке 161. (см. SWC-107)

**Возможные последствия.** Контракт атакующего может выполнить повторный вход до обновления состояния и вывести средства.

**Шаги воспроизведения.**

```
Откройте строка 159 в предоставленном файле scroll-contracts/src/L2/L2ScrollMessenger.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/L2ScrollMessenger.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/L2ScrollMessenger.sol#L159) · line 159 · SHA-256 2649304147ef4bd103508a6b49910d52ccbcc418a86182fd2f053184a509b5b5_

```
  157 |         xDomainMessageSender = _from;
  158 |         // solhint-disable-next-line avoid-low-level-calls
  159 |         (bool success, ) = _to.call{value: _value}(_message);
  160 |         // reset value to refund gas.
  161 |         xDomainMessageSender = ScrollConstants.DEFAULT_XDOMAIN_MESSAGE_SENDER;
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Примените шаблон checks-effects-interactions и/или ReentrancyGuard.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09153 — initialize() без модификатора initializer в scroll-contracts/src/L2/predeploys/L1BlockContainer.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:scroll-contracts/src/L2/predeploys/L1BlockContainer.sol`
- Источник данных: scroll-contracts/src/L2/predeploys/L1BlockContainer.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 36.5 / 100
- CVSS v3.1: неприменимо

Функция initialize в строка 63 не имеет защиты initializer/onlyInitializing. (см. SWC-118)

**Возможные последствия.** В обновляемых прокси кто угодно может (пере)инициализировать контракт и стать владельцем.

**Шаги воспроизведения.**

```
Откройте строка 63 в предоставленном файле scroll-contracts/src/L2/predeploys/L1BlockContainer.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/predeploys/L1BlockContainer.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/predeploys/L1BlockContainer.sol#L63) · line 63 · SHA-256 4b809c2dc16a948ad7a1ea666c1f698b6114eaf7d2c6c125beec3119b0a7a9d6_

```
   61 |     }
   62 | 
   63 |     function initialize(
   64 |         bytes32 _startBlockHash,
   65 |         uint64 _startBlockHeight,
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09156 — initialize() без модификатора initializer в scroll-contracts/src/L2/predeploys/L2MessageQueue.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:scroll-contracts/src/L2/predeploys/L2MessageQueue.sol`
- Источник данных: scroll-contracts/src/L2/predeploys/L2MessageQueue.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 36.5 / 100
- CVSS v3.1: неприменимо

Функция initialize в строка 42 не имеет защиты initializer/onlyInitializing. (см. SWC-118)

**Возможные последствия.** В обновляемых прокси кто угодно может (пере)инициализировать контракт и стать владельцем.

**Шаги воспроизведения.**

```
Откройте строка 42 в предоставленном файле scroll-contracts/src/L2/predeploys/L2MessageQueue.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/predeploys/L2MessageQueue.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/predeploys/L2MessageQueue.sol#L42) · line 42 · SHA-256 815138f70b3bbcc59e47c256deb7ece3f85abf2abaa459387fcd0deb8aab58cb_

```
   40 |     /// @dev You are not allowed to initialize when there are some messages appended.
   41 |     /// @param _messenger The address of messenger to update.
   42 |     function initialize(address _messenger) external onlyOwner {
   43 |         require(nextMessageIndex == 0, "cannot initialize");
   44 | 
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09222 — github.com/btcsuite/btcd v0.20.1-beta затронут GHSA-3jgf-r68h-xfqm (CVE-2024-34478, GO-2024-2818)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/btcsuite/btcd@v0.20.1-beta`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3jgf-r68h-xfqm (CVE-2024-34478, GO-2024-2818) для пакета Go github.com/btcsuite/btcd версии v0.20.1-beta: btcd susceptible to consensus failures. Проверенный код называет github.com/btcsuite/btcd/blockchain.txValidator.Validate, github.com/btcsuite/btcd/txscript.Engine.Step: затронутый код может быть достижим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3jgf-r68h-xfqm
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3jgf-r68h-xfqm](https://osv.dev/vulnerability/GHSA-3jgf-r68h-xfqm) · line 26 · SHA-256 c535e168fc079608620751f63c2950e5391c783db799b2e67d203eba75220946_

```
{"id": "GHSA-3jgf-r68h-xfqm", "aliases": ["CVE-2024-34478", "GO-2024-2818"], "modified": "2024-08-07T19:55:49Z", "summary": "btcd susceptible to consensus failures", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.24.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09226 — github.com/docker/docker v26.1.0+incompatible затронут GHSA-pxq6-2prw-chj9 (CVE-2026-33997, GO-2026-4883)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 6.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-pxq6-2prw-chj9 (CVE-2026-33997, GO-2026-4883) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Moby has an Off-by-one error in its plugin privilege validation. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pxq6-2prw-chj9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pxq6-2prw-chj9](https://osv.dev/vulnerability/GHSA-pxq6-2prw-chj9) · line 39 · SHA-256 a1f97854af5b75958bb95b60d587d295c47edf095a7267badd9405b3c80f7afb_

```
{"id": "GHSA-pxq6-2prw-chj9", "aliases": ["CVE-2026-33997", "GO-2026-4883"], "modified": "2026-09-10T03:50:40.571293679Z", "summary": "Moby has an Off-by-one error in its plugin privilege validation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09232 — github.com/gorilla/websocket v1.5.0 затронут GHSA-w67g-5rqw-f597 (GO-2026-6278)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/gorilla/websocket@v1.5.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-w67g-5rqw-f597 (GO-2026-6278) для пакета Go github.com/gorilla/websocket версии v1.5.0: Gorilla WebSocket Uses Cryptographically Weak PRNG for WebSocket Mask Key. Проверенный код называет github.com/gorilla/websocket.Conn.Close, github.com/gorilla/websocket.NewClient, github.com/gorilla/websocket.httpProxyDialer.Dial, github.com/gorilla/websocket.netDialerFunc.Dial …: затронутый код может быть достижим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w67g-5rqw-f597
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w67g-5rqw-f597](https://osv.dev/vulnerability/GHSA-w67g-5rqw-f597) · line 56 · SHA-256 3fee799e1426dfa658884e378d6f3bcd030db0c65d802c9625786e69e373c51b_

```
{"id": "GHSA-w67g-5rqw-f597", "aliases": ["GO-2026-6278"], "modified": "2026-09-10T03:50:54.128553228Z", "summary": "Gorilla WebSocket Uses Cryptographically Weak PRNG for WebSocket Mask Key", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.5.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09129 — Прямое использование ecrecover в scroll-contracts/lib/solmate/src/tokens/ERC20.sol

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:scroll-contracts/lib/solmate/src/tokens/ERC20.sol`
- Источник данных: scroll-contracts/lib/solmate/src/tokens/ERC20.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 43.6 / 100
- CVSS v3.1: неприменимо

ecrecover в строка 130. (см. SWC-117/SWC-121)

**Возможные последствия.** Без проверок s-значения/нулевого адреса и nonce подписи могут быть изменяемыми или повторно используемыми. ecrecover основан на secp256k1 ECDSA (долгосрочно квантово-уязвим).

**Шаги воспроизведения.**

```
Откройте строка 130 в предоставленном файле scroll-contracts/lib/solmate/src/tokens/ERC20.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/lib/solmate/src/tokens/ERC20.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/lib/solmate/src/tokens/ERC20.sol#L130) · line 130 · SHA-256 d41f7bb35e5522e67c7809f4b8f088dcccb35a08f1c232db2eb54370446601e2_

```
  128 |         // the owner's nonce which cannot realistically overflow.
  129 |         unchecked {
  130 |             address recoveredAddress = ecrecover(
  131 |                 keccak256(
  132 |                     abi.encodePacked(
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin ECDSA.recover с разделением доменов EIP-712 и nonce.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09126 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: rollup/internal/controller/sender/kms_signer.go
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

5 упоминаний ECDSA в 2 файл(ах), например rollup/internal/controller/sender/kms_signer.go:5. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте rollup/internal/controller/sender/kms_signer.go:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [rollup/internal/controller/sender/kms_signer.go](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/rollup/internal/controller/sender/kms_signer.go#L5) · line 5 · SHA-256 a946707a5431416fc04c9ea88c7fce501e1976d756266d0bb50f3c6fed6d6353_

```
    4 | 	"context"
    5 | 	"crypto/ecdsa"
    6 | 	"encoding/asn1"
```

_file_excerpt · [rollup/internal/controller/sender/kms_signer.go](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/rollup/internal/controller/sender/kms_signer.go#L64) · line 64 · SHA-256 62bee3e9910de110b08646c5a408b8d8c61744405207afb573bf85579f47c77f_

```
   63 | 	oidPublicKeyECDSA = asn1.ObjectIdentifier{1, 2, 840, 10045, 2, 1} // id-ecPublicKey
   64 | 	oidNamedCurveS256 = asn1.ObjectIdentifier{1, 3, 132, 0, 10}       // secp256k1
   65 | )
```

_file_excerpt · [rollup/internal/controller/sender/kms_signer.go](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/rollup/internal/controller/sender/kms_signer.go#L140) · line 140 · SHA-256 fc59e9f71af5ce30f8cf09a34c05380e0c25f14694e60faf3f1788ebfd21766e_

```
  139 | 	if !spki.Algorithm.Algorithm.Equal(oidPublicKeyECDSA) || !spki.Algorithm.Parameters.Equal(oidNamedCurveS256) {
  140 | 		return nil, fmt.Errorf("aws kms signer: unexpected public key algorithm/curve, want id-ecPublicKey/secp256k1")
  141 | 	}
```

_file_excerpt · [scroll-contracts/lib/solmate/src/tokens/ERC20.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/lib/solmate/src/tokens/ERC20.sol#L130) · line 130 · SHA-256 d41f7bb35e5522e67c7809f4b8f088dcccb35a08f1c232db2eb54370446601e2_

```
  128 |         // the owner's nonce which cannot realistically overflow.
  129 |         unchecked {
  130 |             address recoveredAddress = ecrecover(
  131 |                 keccak256(
  132 |                     abi.encodePacked(
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-09124 — Квантово-уязвимый ECDSA: роль не определена (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: common/utils/keystore.go
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

2 упоминаний ECDSA в 2 файл(ах), например common/utils/keystore.go:4. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте common/utils/keystore.go:4 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [common/utils/keystore.go](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/common/utils/keystore.go#L4) · line 4 · SHA-256 477db8762fa92569d31b62e6d7466b65eb650a0935e45eefac93b4cc01ba4e3d_

```
    3 | import (
    4 | 	"crypto/ecdsa"
    5 | 	"errors"
```

_file_excerpt · [coordinator/internal/controller/proxy/client_manager.go](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/coordinator/internal/controller/proxy/client_manager.go#L5) · line 5 · SHA-256 0a3914ad29653b3674c9c73c87cbf54cf4e9217d73ccfa1c2fbc380b889ec818_

```
    4 | 	"context"
    5 | 	"crypto/ecdsa"
    6 | 	"fmt"
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-09125 — Квантово-уязвимый ECDSA: аутентификация и идентификация (сертификаты, токены, аттестация устройств) (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:authentication`
- Источник данных: coordinator/internal/types/auth.go
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

1 упоминаний ECDSA в 1 файл(ах), например coordinator/internal/types/auth.go:4. Роль по путям, именам функций и соседнему коду: аутентификация и идентификация (сертификаты, токены, аттестация устройств). Краткоживущая аутентификация безопасна до появления CRQC; долгоживущим идентификаторам (аттестация устройств, ключи УЦ и SSH) план нужен раньше.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте coordinator/internal/types/auth.go:4 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [coordinator/internal/types/auth.go](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/coordinator/internal/types/auth.go#L4) · line 4 · SHA-256 754608aa95082d2e114584f2a6d68378067ee8d9ecbeea560d49878e38dece03_

```
    3 | import (
    4 | 	"crypto/ecdsa"
    5 | 	"encoding/hex"
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-09165 — Криптография на спариваниях в контракте: BN254 (alt_bn128) (scroll-contracts/src/libraries/verifier/RollupVerifier.sol)

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:scroll-contracts/src/libraries/verifier/RollupVerifier.sol`
- Источник данных: scroll-contracts/src/libraries/verifier/RollupVerifier.sol
- Метод обнаружения: Сопоставление шаблонов реестра с учётом комментариев.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 33.7 / 100
- CVSS v3.1: неприменимо

scroll-contracts/src/libraries/verifier/RollupVerifier.sol использует BN254 (alt_bn128) (впервые в строка 24): эллиптические кривые со спариванием (прекомпилы alt_bn128 0x06–0x08 или BLS12-381 0x0b–0x11) и/или верификатор доказательств на спариваниях.

**Возможные последствия.** Они опираются на дискретный логарифм в группах эллиптических кривых, который алгоритм Шора решает на CRQC; доказательства или агрегированные подписи, принимаемые контрактом, тогда можно будет подделать. Сегодня не эксплуатируется.

**Шаги воспроизведения.**

```
Откройте строка 24 в предоставленном файле scroll-contracts/src/libraries/verifier/RollupVerifier.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/libraries/verifier/RollupVerifier.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/libraries/verifier/RollupVerifier.sol#L24) · line 24 · SHA-256 1c7f6da98e4391b6498b701ef8d1a7980da16b77df27cb41791a84d92b444db4_

```
   22 | 
   23 |         assembly {
   24 |             ret := staticcall(gas(), 8, add(input, 0x20), mul(length, 0x20), result, 0x20)
   25 |         }
   26 |         require(ret);
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Обнаружение по шаблонам; используемую схему следует подтвердить по исходному коду верификатора.

**Рекомендация.** Внесите контракт в PQC-инвентаризацию и предусмотрите путь обновления (обновляемый верификатор, системы доказательств/подписи на хешах или решётках по мере их зрелости).

**Повторная проверка.** Повторите аудит после обновления верификатора.

### QSI-2026-09175 — block-buffer 0.11.0 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/block-buffer@0.11.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-qwgh-2vcv-g2f7 для пакета crates.io block-buffer версии 0.11.0: block_buffer: panic corrupts inline buffer position. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qwgh-2vcv-g2f7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qwgh-2vcv-g2f7](https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7) · manifest · SHA-256 7591b0713b64478fa8ad16a5dd54163bfd64b0d142da6666684f3debae896c25_

```
{"id": "GHSA-qwgh-2vcv-g2f7", "aliases": [], "modified": "2026-10-30T15:45:11.580215361Z", "summary": "block_buffer: panic corrupts inline buffer position", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09197 — rustls 0.23.41 затронут GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.23.41`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285) для пакета crates.io rustls версии 0.23.41: Rustls: TLS 1.3 handshake messages incorrectly accepted across encryption level boundaries. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2mjx-qc3c-rqvc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2mjx-qc3c-rqvc](https://osv.dev/vulnerability/GHSA-2mjx-qc3c-rqvc) · manifest · SHA-256 f20e4b21c01d3d75460ac8d90a54d541a1a34187a4f05b501e4f46c27c564e86_

```
{"id": "GHSA-2mjx-qc3c-rqvc", "aliases": ["RUSTSEC-2026-0285"], "modified": "2026-10-27T15:30:05.509305490Z", "summary": "Rustls: TLS 1.3 handshake messages incorrectly accepted across encryption level boundaries", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.45).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09198 — rustls 0.23.41 затронут GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.23.41`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) для пакета crates.io rustls версии 0.23.41: Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-c8m5-c952-6cm4
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-c8m5-c952-6cm4](https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4) · manifest · SHA-256 87554a0cce34470a221f04ad57566b2b512ff6299ad3ee95b190df659d646e3d_

```
{"id": "GHSA-c8m5-c952-6cm4", "aliases": ["RUSTSEC-2026-0346"], "modified": "2026-10-27T16:15:05.354395696Z", "summary": "Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.46, 0.24.0-dev.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09203 — tracing-subscriber 0.2.25 затронут GHSA-xwfj-jgwm-7wp5 (CVE-2025-58160, RUSTSEC-2025-0055)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/tracing-subscriber@0.2.25`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-xwfj-jgwm-7wp5 (CVE-2025-58160, RUSTSEC-2025-0055) для пакета crates.io tracing-subscriber версии 0.2.25: Tracing logging user input may result in poisoning logs with ANSI escape sequences. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xwfj-jgwm-7wp5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xwfj-jgwm-7wp5](https://osv.dev/vulnerability/GHSA-xwfj-jgwm-7wp5) · manifest · SHA-256 a3249213cfcaf11938eca6db0ff56d5636ca4a09bf8ea0cca9f92a52b2e4c20f_

```
{"id": "GHSA-xwfj-jgwm-7wp5", "aliases": ["CVE-2025-58160", "RUSTSEC-2025-0055"], "modified": "2026-09-10T03:50:27.766863705Z", "summary": " Tracing logging user input may result in poisoning logs with ANSI escape sequences", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.3.20).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09225 — github.com/docker/docker v26.1.0+incompatible затронут GHSA-4vq8-7jfc-9cvp (CVE-2025-54410)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: 3.3 (`CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-4vq8-7jfc-9cvp (CVE-2025-54410) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Moby firewalld reload removes bridge network isolation. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4vq8-7jfc-9cvp
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4vq8-7jfc-9cvp](https://osv.dev/vulnerability/GHSA-4vq8-7jfc-9cvp) · line 39 · SHA-256 dee43ec41d2fe7fef219613e010a0504110ce6e3a02652085adb3b1cb64a5334_

```
{"id": "GHSA-4vq8-7jfc-9cvp", "aliases": ["CVE-2025-54410", "GO-2025-3829"], "modified": "2026-09-10T03:50:25.738441655Z", "summary": "Moby firewalld reload removes bridge network isolation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:U/C:L/I:L/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (25.0.13, 28.0.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09127 — Плавающая версия компилятора (>=0.8.0) в 20 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.8.0`
- Источник данных: scroll-contracts/lib/solmate/src/auth/Auth.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 34.8 / 100
- CVSS v3.1: неприменимо

pragma >=0.8.0 в 20 файл(ах), впервые в scroll-contracts/lib/solmate/src/auth/Auth.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте scroll-contracts/lib/solmate/src/auth/Auth.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/lib/solmate/src/auth/Auth.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/lib/solmate/src/auth/Auth.sol#L2) · line 2 · SHA-256 9498e7a7f87af2cd59e0fa5f1e66710f854cb43557c82a40cef5bed6669ed818_

```
    1 | // SPDX-License-Identifier: AGPL-3.0-only
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | /// @notice Provides a flexible and updatable auth pattern which is completely separate from application logic.
```

_file_excerpt · [scroll-contracts/lib/solmate/src/auth/Owned.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/lib/solmate/src/auth/Owned.sol#L2) · line 2 · SHA-256 cec42a0375b3ee8d0381596e3ec1ac2031df2ca449c6af91cffa667aff05e977_

```
    1 | // SPDX-License-Identifier: AGPL-3.0-only
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | /// @notice Simple single owner authorization mixin.
```

_file_excerpt · [scroll-contracts/lib/solmate/src/auth/authorities/MultiRolesAuthority.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/lib/solmate/src/auth/authorities/MultiRolesAuthority.sol#L2) · line 2 · SHA-256 a8b2b4c6d913d3db2817cd4c431ac08c303a15d55dcc67a8f03af556db62180c_

```
    1 | // SPDX-License-Identifier: AGPL-3.0-only
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | import {Auth, Authority} from "../Auth.sol";
```

_file_excerpt · [scroll-contracts/lib/solmate/src/auth/authorities/RolesAuthority.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/lib/solmate/src/auth/authorities/RolesAuthority.sol#L2) · line 2 · SHA-256 a8b2b4c6d913d3db2817cd4c431ac08c303a15d55dcc67a8f03af556db62180c_

```
    1 | // SPDX-License-Identifier: AGPL-3.0-only
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | import {Auth, Authority} from "../Auth.sol";
```

_file_excerpt · [scroll-contracts/lib/solmate/src/tokens/ERC1155.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/lib/solmate/src/tokens/ERC1155.sol#L2) · line 2 · SHA-256 0a27d4e4c242ed315ee139e504758c6745fcd0c2fe9a6f2ab98f77010d19be35_

```
    1 | // SPDX-License-Identifier: AGPL-3.0-only
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | /// @notice Minimalist and gas efficient standard ERC1155 implementation.
```

_file_excerpt · [scroll-contracts/lib/solmate/src/tokens/ERC20.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/lib/solmate/src/tokens/ERC20.sol#L2) · line 2 · SHA-256 b93695ee22c4af8b671e5dff401933e8c220393b36ddcdbec36ae27870b72c7b_

```
    1 | // SPDX-License-Identifier: AGPL-3.0-only
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | /// @notice Modern and gas efficient ERC20 + EIP-2612 implementation.
```

_file_excerpt · [scroll-contracts/lib/solmate/src/tokens/ERC4626.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/lib/solmate/src/tokens/ERC4626.sol#L2) · line 2 · SHA-256 3e08f13cb30c22968448516a6a8bfb9e7d5c15d4a646f57c4f11ee41965524d8_

```
    1 | // SPDX-License-Identifier: AGPL-3.0-only
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | import {ERC20} from "../tokens/ERC20.sol";
```

_file_excerpt · [scroll-contracts/lib/solmate/src/tokens/ERC6909.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/lib/solmate/src/tokens/ERC6909.sol#L2) · line 2 · SHA-256 242d667b6e8c811192327f4d941bfbe53f68479b7f470fcdeac666284d2889f9_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | /// @notice Minimalist and gas efficient standard ERC6909 implementation.
```

_file_excerpt · [scroll-contracts/lib/solmate/src/tokens/ERC721.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/lib/solmate/src/tokens/ERC721.sol#L2) · line 2 · SHA-256 f360056d129ce016eda8dabee5aecef50144ca53742b3a1b4deec6074375b934_

```
    1 | // SPDX-License-Identifier: AGPL-3.0-only
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | /// @notice Modern, minimalist, and gas efficient ERC-721 implementation.
```

_file_excerpt · [scroll-contracts/lib/solmate/src/tokens/WETH.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/lib/solmate/src/tokens/WETH.sol#L2) · line 2 · SHA-256 c898105d2f1519ed2ffbd3c3fffd780775839973744c3cd66ae3abaa3249d6ea_

```
    1 | // SPDX-License-Identifier: AGPL-3.0-only
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | import {ERC20} from "./ERC20.sol";
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09130 — Плавающая версия компилятора (^0.8.10) в 1 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.10`
- Источник данных: scroll-contracts/scripts/foundry/DeployLidoGateway.s.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 34.8 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.10 в 1 файл(ах), впервые в scroll-contracts/scripts/foundry/DeployLidoGateway.s.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте scroll-contracts/scripts/foundry/DeployLidoGateway.s.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/scripts/foundry/DeployLidoGateway.s.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/scripts/foundry/DeployLidoGateway.s.sol#L2) · line 2 · SHA-256 9f5e4972786d80906fd7ad2fb04b6aeda51d41ab5ff6d37a63bda80cc583ef08_

```
    1 | // SPDX-License-Identifier: UNLICENSED
    2 | pragma solidity ^0.8.10;
    3 | 
    4 | import {Script} from "forge-std/Script.sol";
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09131 — Плавающая версия компилятора (^0.8.24) в 58 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.24`
- Источник данных: scroll-contracts/src/L1/IL1ScrollMessenger.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 34.8 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.24 в 58 файл(ах), впервые в scroll-contracts/src/L1/IL1ScrollMessenger.sol:3. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте scroll-contracts/src/L1/IL1ScrollMessenger.sol:3 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/IL1ScrollMessenger.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/IL1ScrollMessenger.sol#L3) · line 3 · SHA-256 e237fc6f80bcc953a42e21073a458e9e61aa51047216453dd436eb1a0b3b2a13_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.24;
    4 | 
    5 | import {IScrollMessenger} from "../libraries/IScrollMessenger.sol";
```

_file_excerpt · [scroll-contracts/src/L1/gateways/IL1ERC1155Gateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/IL1ERC1155Gateway.sol#L3) · line 3 · SHA-256 ada29c078e375ee6b2cbd7b69e4eef45b058107cd209bf9516adcd98a58c31a4_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.24;
    4 | 
    5 | /// @title The interface for the ERC1155 cross chain gateway on layer 1.
```

_file_excerpt · [scroll-contracts/src/L1/gateways/IL1ERC20Gateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/IL1ERC20Gateway.sol#L3) · line 3 · SHA-256 6a361406dea27df7c5642c5db36f7196031c76ac3ed083e616bc25854158a2c2_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.24;
    4 | 
    5 | interface IL1ERC20Gateway {
```

_file_excerpt · [scroll-contracts/src/L1/gateways/IL1ERC721Gateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/IL1ERC721Gateway.sol#L3) · line 3 · SHA-256 e971500b65b8b24e036b90917f8e4abfa6344b0fd8a93da924bbfea30a1598b7_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.24;
    4 | 
    5 | /// @title The interface for the ERC721 cross chain gateway on layer 1.
```

_file_excerpt · [scroll-contracts/src/L1/gateways/IL1ETHGateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/IL1ETHGateway.sol#L3) · line 3 · SHA-256 60d32afb10a932db9df16552fdf386a18265b1e286406a5ce7e7c59242c80e66_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.24;
    4 | 
    5 | interface IL1ETHGateway {
```

_file_excerpt · [scroll-contracts/src/L1/gateways/IL1GatewayRouter.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/IL1GatewayRouter.sol#L3) · line 3 · SHA-256 d6b8adb2dd6346cd4d876a7be40732d5bbe7e9afac19d877cf76292a9eaee3c3_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.24;
    4 | 
    5 | import {IL1ETHGateway} from "./IL1ETHGateway.sol";
```

_file_excerpt · [scroll-contracts/src/L1/gateways/L1ERC20Gateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/L1ERC20Gateway.sol#L3) · line 3 · SHA-256 281e6787d0cc90c04f8952b8208f8077415f0b9ea9c9d6acb343e4fa3d02bb52_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.24;
    4 | 
    5 | import {IERC20Upgradeable} from "@openzeppelin/contracts-upgradeable/token/ERC20/IERC20Upgradeable.sol";
```

_file_excerpt · [scroll-contracts/src/L1/rollup/IL1MessageQueue.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/rollup/IL1MessageQueue.sol#L3) · line 3 · SHA-256 fe63083e556e7d4a3c633ba1b3af47bc2f71b98ef20ee0106a1ff91df7c4ad67_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.24;
    4 | 
    5 | interface IL1MessageQueue {
```

_file_excerpt · [scroll-contracts/src/L1/rollup/IL1MessageQueueWithGasPriceOracle.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/rollup/IL1MessageQueueWithGasPriceOracle.sol#L3) · line 3 · SHA-256 9b4c3a93ad3bc5a3b5af67d70bf4282725bf78a2bd29b27503e6a697455a039c_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.24;
    4 | 
    5 | import {IL1MessageQueue} from "./IL1MessageQueue.sol";
```

_file_excerpt · [scroll-contracts/src/L1/rollup/IL2GasPriceOracle.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/rollup/IL2GasPriceOracle.sol#L3) · line 3 · SHA-256 a98cb27929f6e50e2487d34a84171807028b2ba415dd8ab14643081eac42befb_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.24;
    4 | 
    5 | interface IL2GasPriceOracle {
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09160 — Плавающая версия компилятора (^0.8.0) в 5 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.0`
- Источник данных: scroll-contracts/src/L2/predeploys/WrappedEther.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 34.8 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.0 в 5 файл(ах), впервые в scroll-contracts/src/L2/predeploys/WrappedEther.sol:3. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте scroll-contracts/src/L2/predeploys/WrappedEther.sol:3 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/predeploys/WrappedEther.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/predeploys/WrappedEther.sol#L3) · line 3 · SHA-256 b4d288526b881ed29c412a0ced5eb78877e76329149168e465a25562e763071a_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.0;
    4 | 
    5 | import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
```

_file_excerpt · [scroll-contracts/src/libraries/gateway/CCTPGatewayBase.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/libraries/gateway/CCTPGatewayBase.sol#L3) · line 3 · SHA-256 1c44403c40a2b0061553bf83cca6abe8d6a594e5ed0b2c1df1223b28b913f0bc_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.0;
    4 | 
    5 | import {IMessageTransmitter} from "../../interfaces/IMessageTransmitter.sol";
```

_file_excerpt · [scroll-contracts/src/libraries/token/IScrollERC1155Extension.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/libraries/token/IScrollERC1155Extension.sol#L3) · line 3 · SHA-256 3546282441b6170c6d88edfdb2609e8fda3eb8315c2560304b03e77d5c579168_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.0;
    4 | 
    5 | // Functions needed on top of the ERC1155 standard to be compliant with the Scroll bridge
```

_file_excerpt · [scroll-contracts/src/libraries/token/IScrollERC20Extension.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/libraries/token/IScrollERC20Extension.sol#L3) · line 3 · SHA-256 faeecba0e85125176456cc117e5bf0333dda2afdc80fc043fc958f2c44f59ebc_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.0;
    4 | 
    5 | // Functions needed on top of the ERC20 standard to be compliant with the Scroll bridge
```

_file_excerpt · [scroll-contracts/src/libraries/token/IScrollERC721Extension.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/libraries/token/IScrollERC721Extension.sol#L3) · line 3 · SHA-256 68b1b7d7965bd46cbdb816d008e4664698c795528e9b5f7c2125e55999e03560_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.0;
    4 | 
    5 | // Functions needed on top of the ERC721 standard to be compliant with the Scroll bridge
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09184 — lru 0.12.5 затронут GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/lru@0.12.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002) для пакета crates.io lru версии 0.12.5: `IterMut` violates Stacked Borrows by invalidating internal pointer. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rhfx-m35p-ff5j
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rhfx-m35p-ff5j](https://osv.dev/vulnerability/GHSA-rhfx-m35p-ff5j) · manifest · SHA-256 74c3e26941575e818cf192f0511138a6719b2124292f8348b2d299a631095b03_

```
{"id": "GHSA-rhfx-m35p-ff5j", "aliases": ["RUSTSEC-2026-0002"], "modified": "2026-09-10T03:50:59.064354050Z", "summary": "`IterMut` violates Stacked Borrows by invalidating internal pointer", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.16.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09186 — lru 0.13.0 затронут GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/lru@0.13.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002) для пакета crates.io lru версии 0.13.0: `IterMut` violates Stacked Borrows by invalidating internal pointer. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rhfx-m35p-ff5j
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rhfx-m35p-ff5j](https://osv.dev/vulnerability/GHSA-rhfx-m35p-ff5j) · manifest · SHA-256 74c3e26941575e818cf192f0511138a6719b2124292f8348b2d299a631095b03_

```
{"id": "GHSA-rhfx-m35p-ff5j", "aliases": ["RUSTSEC-2026-0002"], "modified": "2026-09-10T03:50:59.064354050Z", "summary": "`IterMut` violates Stacked Borrows by invalidating internal pointer", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.16.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09188 — p3-symmetric 0.4.3 затронут GHSA-3g92-f9ch-qjcm

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/p3-symmetric@0.4.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3g92-f9ch-qjcm для пакета crates.io p3-symmetric версии 0.4.3: Plonky3: The sponge construction used to get a hash function from a cryptographic permutation is not collision resistant for inputs of different lengths. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3g92-f9ch-qjcm
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3g92-f9ch-qjcm](https://osv.dev/vulnerability/GHSA-3g92-f9ch-qjcm) · manifest · SHA-256 a27fd662d8b302d27a961e04dc71b7a4ef49c239577a1f90a03d0b1035ef7366_

```
{"id": "GHSA-3g92-f9ch-qjcm", "aliases": [], "modified": "2026-04-16T23:04:45.978452Z", "summary": "Plonky3: The sponge construction used to get a hash function from a cryptographic permutation is not collision resistant for inputs of different lengths", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09200 — rustls 0.23.41 затронут GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.23.41`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349) для пакета crates.io rustls версии 0.23.41: rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w44r-93j7-qv28
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w44r-93j7-qv28](https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28) · manifest · SHA-256 f0fcaa2fa7a56e188458f39e55b23e999d0c7da6d3c1294c014c64ab37b33dee_

```
{"id": "GHSA-w44r-93j7-qv28", "aliases": ["RUSTSEC-2026-0349"], "modified": "2026-10-27T16:15:05.340347056Z", "summary": "rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.46, 0.24.0-dev.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09199 — rustls 0.23.41 затронут GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustls@0.23.41`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 25.0 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348) для пакета crates.io rustls версии 0.23.41: Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication. Затронутый код находится за флагом Cargo `brotli`, выключенным по умолчанию; ни один проверенный манифест его не включает — бюллетень не применим, если флаг не включает другая зависимость.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-h2v8-394m-p7vv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-h2v8-394m-p7vv](https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv) · manifest · SHA-256 9118726d52fea7cee09a6b4a21a10d2a7bab860f9762fff4658cb78db0453744_

```
{"id": "GHSA-h2v8-394m-p7vv", "aliases": ["RUSTSEC-2026-0348"], "modified": "2026-10-27T16:15:05.337819489Z", "summary": "Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication.", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.46, 0.24.0-dev.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09176 — crypto-bigint 0.5.5 затронут RUSTSEC-2026-0387 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crypto-bigint@0.5.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
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

### QSI-2026-09180 — h2 0.4.15 затронут RUSTSEC-2026-0258 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/h2@0.4.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
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

### QSI-2026-09183 — libz-sys 1.1.29 затронут RUSTSEC-2026-0418 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/libz-sys@1.1.29`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0418 для пакета crates.io libz-sys версии 1.1.29: libz-sys build script leaks environment variables in the build directory. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0418
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0418](https://osv.dev/vulnerability/RUSTSEC-2026-0418) · manifest · SHA-256 c5853994609eb6005df3fdabfd8d90722c9213a6b6ddc9f03b43ae0e4a747b57_

```
{"id": "RUSTSEC-2026-0418", "aliases": ["GHSA-8p3x-q3q3-q3v5"], "modified": "2026-10-29T14:15:02.333141406Z", "summary": "libz-sys build script leaks environment variables in the build directory", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.1.31).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09185 — lru 0.12.5 затронут RUSTSEC-2026-0253 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/lru@0.12.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0253 для пакета crates.io lru версии 0.12.5: Potential use-after-free due to lack of panic safety in `LruCache::pop()`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0253
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0253](https://osv.dev/vulnerability/RUSTSEC-2026-0253) · manifest · SHA-256 06df98c5350689983b2fda96297e3527fd26f472c5d474c041975b220e7ffc2c_

```
{"id": "RUSTSEC-2026-0253", "aliases": [], "modified": "2026-08-11T11:15:06.101553049Z", "summary": "Potential use-after-free due to lack of panic safety in `LruCache::pop()`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.18.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09187 — lru 0.13.0 затронут RUSTSEC-2026-0253 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/lru@0.13.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0253 для пакета crates.io lru версии 0.13.0: Potential use-after-free due to lack of panic safety in `LruCache::pop()`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0253
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0253](https://osv.dev/vulnerability/RUSTSEC-2026-0253) · manifest · SHA-256 06df98c5350689983b2fda96297e3527fd26f472c5d474c041975b220e7ffc2c_

```
{"id": "RUSTSEC-2026-0253", "aliases": [], "modified": "2026-08-11T11:15:06.101553049Z", "summary": "Potential use-after-free due to lack of panic safety in `LruCache::pop()`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.18.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09191 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0338 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0338 для пакета crates.io quinn-proto версии 0.11.16: Remote peer can panic quinn-proto with zero-length STREAM frames during unordered reads. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0338
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0338](https://osv.dev/vulnerability/RUSTSEC-2026-0338) · manifest · SHA-256 2d8a96c1ccb5782dfd51ab6c6bfc548092df0a416eb5a7c29ca5b5ffdce603ea_

```
{"id": "RUSTSEC-2026-0338", "aliases": ["GHSA-465w-v9q3-7j98"], "modified": "2026-10-12T18:15:01.969514645Z", "summary": "Remote peer can panic quinn-proto with zero-length STREAM frames during unordered reads", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.11.18).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09192 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0339 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0339 для пакета crates.io quinn-proto версии 0.11.16: Unbounded growth of pending connection ID retirements in quinn-proto. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0339
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0339](https://osv.dev/vulnerability/RUSTSEC-2026-0339) · manifest · SHA-256 b5c8da254e3051004bc694e865ed6cf27e63c10cddc5641f13f42bd290bdb54a_

```
{"id": "RUSTSEC-2026-0339", "aliases": ["GHSA-hmxj-32vh-65vr"], "modified": "2026-10-12T18:15:01.956822776Z", "summary": "Unbounded growth of pending connection ID retirements in quinn-proto", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.11.17).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09195 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0342 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0342 для пакета crates.io quinn-proto версии 0.11.16: Zero-length DATAGRAM frames bypass the receive buffer limit in quinn-proto. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0342
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0342](https://osv.dev/vulnerability/RUSTSEC-2026-0342) · manifest · SHA-256 41dfd63166e25757cdb189c219a98c5e4b8d6b2e389f484cc583556a378073e4_

```
{"id": "RUSTSEC-2026-0342", "aliases": ["GHSA-2hv7-gw8g-gpq5"], "modified": "2026-10-12T18:15:01.956681478Z", "summary": "Zero-length DATAGRAM frames bypass the receive buffer limit in quinn-proto", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.11.17).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09196 — ruint 1.19.0 затронут RUSTSEC-2026-0220 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/ruint@1.19.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0220 для пакета crates.io ruint версии 1.19.0: Uint shift operations: incorrect overflow flags and truncated shift amounts. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (ruint::Uint::checked_shl, ruint::Uint::checked_shr, ruint::Uint::overflowing_shl, ruint::Uint::overflowing_shr, ruint::Uint::saturating_shl, ruint::Uint::saturating_shr …); ruint приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0220
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0220](https://osv.dev/vulnerability/RUSTSEC-2026-0220) · manifest · SHA-256 f42394932e247da212898e7d0d34cec3f04961c857380e305a289974569d677f_

```
{"id": "RUSTSEC-2026-0220", "aliases": [], "modified": "2026-07-30T19:15:04.025918010Z", "summary": "Uint shift operations: incorrect overflow flags and truncated shift amounts", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09201 — rustls-webpki 0.103.13 затронут RUSTSEC-2026-0382 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.103.13`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
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

### QSI-2026-09204 — webpki-roots 1.0.8 затронут RUSTSEC-2026-0381 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/webpki-roots@1.0.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0381 (CVE-2026-111943) для пакета crates.io webpki-roots версии 1.0.8: Bundled root certificates allow trust in distrusted emSign intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-09205 — zstd 0.13.3 затронут RUSTSEC-2026-0391 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd@0.13.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-09206 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0395 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-09207 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0396 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-09208 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0397 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-09209 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0398 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-09210 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0399 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-09211 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0400 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-09212 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0401 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-09213 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0402 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-09214 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0403 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-09215 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0404 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-09216 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0405 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-09217 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0406 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-09231 — github.com/docker/docker v26.1.0+incompatible затронут GO-2026-4887 (CVE-2026-34040) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-4887 (CVE-2026-34040) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Moby has AuthZ plugin bypass when provided oversized request bodies in github.com/docker/docker. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-4887
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-4887](https://osv.dev/vulnerability/GO-2026-4887) · line 39 · SHA-256 b0413de8db38a9ae7e52f49ec09801d729ca5107accd4bd112b3ae32be052e95_

```
{"id": "GO-2026-4887", "aliases": ["CVE-2026-34040", "GHSA-x744-4wpc-v9h2"], "modified": "2026-04-03T20:59:19.226161232Z", "summary": "Moby has AuthZ plugin bypass when provided oversized request bodies in github.com/docker/docker", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09128 — Привилегированные административные функции в scroll-contracts/lib/solmate/src/auth/Owned.sol: transferOwnership

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/lib/solmate/src/auth/Owned.sol`
- Источник данных: scroll-contracts/lib/solmate/src/auth/Owned.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: transferOwnership. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/lib/solmate/src/auth/Owned.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/lib/solmate/src/auth/Owned.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/lib/solmate/src/auth/Owned.sol) · multiple · SHA-256 3ef6a6924988649e26a7e42a450b6976f80844a318d3ab2418fc99e4bae2bcee_

```
Privileged functions: transferOwnership
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09134 — Привилегированные административные функции в scroll-contracts/src/L1/L1ScrollMessenger.sol: updateMaxReplayTimes

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/L1ScrollMessenger.sol`
- Источник данных: scroll-contracts/src/L1/L1ScrollMessenger.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateMaxReplayTimes. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L1/L1ScrollMessenger.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/L1ScrollMessenger.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/L1ScrollMessenger.sol) · multiple · SHA-256 e0ee97f1849f91b3f6e72d51e254baa56f2b56e5cfb2c0d09755fe89b4e782c5_

```
Privileged functions: updateMaxReplayTimes
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09135 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol: updateFeeVault, setPause

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol`
- Источник данных: scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateFeeVault, setPause. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol) · multiple · SHA-256 0bc53cba0e646a9050b16b3b4b5df422672d2e8175f2e4faeb2c9a66035002d9_

```
Privileged functions: updateFeeVault, setPause
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09136 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/L1CustomERC20Gateway.sol: updateTokenMapping

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/L1CustomERC20Gateway.sol`
- Источник данных: scroll-contracts/src/L1/gateways/L1CustomERC20Gateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateTokenMapping. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L1/gateways/L1CustomERC20Gateway.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/gateways/L1CustomERC20Gateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/L1CustomERC20Gateway.sol) · multiple · SHA-256 567d5823d91cba01d4a889468f89c726bb465044004c517c148ce8cd3d1fafa7_

```
Privileged functions: updateTokenMapping
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09137 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/L1ERC1155Gateway.sol: updateTokenMapping

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/L1ERC1155Gateway.sol`
- Источник данных: scroll-contracts/src/L1/gateways/L1ERC1155Gateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateTokenMapping. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L1/gateways/L1ERC1155Gateway.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/gateways/L1ERC1155Gateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/L1ERC1155Gateway.sol) · multiple · SHA-256 567d5823d91cba01d4a889468f89c726bb465044004c517c148ce8cd3d1fafa7_

```
Privileged functions: updateTokenMapping
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09138 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/L1ERC721Gateway.sol: updateTokenMapping

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/L1ERC721Gateway.sol`
- Источник данных: scroll-contracts/src/L1/gateways/L1ERC721Gateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateTokenMapping. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L1/gateways/L1ERC721Gateway.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/gateways/L1ERC721Gateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/L1ERC721Gateway.sol) · multiple · SHA-256 567d5823d91cba01d4a889468f89c726bb465044004c517c148ce8cd3d1fafa7_

```
Privileged functions: updateTokenMapping
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09139 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/L1GatewayRouter.sol: setETHGateway, setDefaultERC20Gateway, setERC20Gateway

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/L1GatewayRouter.sol`
- Источник данных: scroll-contracts/src/L1/gateways/L1GatewayRouter.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: setETHGateway, setDefaultERC20Gateway, setERC20Gateway. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L1/gateways/L1GatewayRouter.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/gateways/L1GatewayRouter.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/L1GatewayRouter.sol) · multiple · SHA-256 0ba5b5898f9bf7cc74eff33ce5345afae100dbe0cb78eed820313e5d279abbb6_

```
Privileged functions: setETHGateway, setDefaultERC20Gateway, setERC20Gateway
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09140 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/usdc/L1USDCGateway.sol: updateCircleCaller, pauseDeposit, pauseWithdraw

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/usdc/L1USDCGateway.sol`
- Источник данных: scroll-contracts/src/L1/gateways/usdc/L1USDCGateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateCircleCaller, pauseDeposit, pauseWithdraw. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L1/gateways/usdc/L1USDCGateway.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/gateways/usdc/L1USDCGateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/usdc/L1USDCGateway.sol) · multiple · SHA-256 76008f6dc4b691df13710a02121b96b76410e9863a09e512b2c81c014dc85fd1_

```
Privileged functions: updateCircleCaller, pauseDeposit, pauseWithdraw
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09141 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/usdc/draft-L1USDCGatewayCCTP.sol: updateCCTPContracts

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/usdc/draft-L1USDCGatewayCCTP.sol`
- Источник данных: scroll-contracts/src/L1/gateways/usdc/draft-L1USDCGatewayCCTP.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateCCTPContracts. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L1/gateways/usdc/draft-L1USDCGatewayCCTP.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/gateways/usdc/draft-L1USDCGatewayCCTP.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/usdc/draft-L1USDCGatewayCCTP.sol) · multiple · SHA-256 927a9a131474771e7a6025b058886c146d56b8594bfb46b0ff92124a3d41459a_

```
Privileged functions: updateCCTPContracts
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09142 — Привилегированные административные функции в scroll-contracts/src/L1/rollup/L1MessageQueue.sol: updateGasOracle, updateMaxGasLimit

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/rollup/L1MessageQueue.sol`
- Источник данных: scroll-contracts/src/L1/rollup/L1MessageQueue.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateGasOracle, updateMaxGasLimit. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L1/rollup/L1MessageQueue.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/rollup/L1MessageQueue.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/rollup/L1MessageQueue.sol) · multiple · SHA-256 abc3ca57c063b06e3357f32e9853f137df9b7d34269ed773e60736cbb9cd03eb_

```
Privileged functions: updateGasOracle, updateMaxGasLimit
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09143 — Привилегированные административные функции в scroll-contracts/src/L1/rollup/L1MessageQueueWithGasPriceOracle.sol: updateWhitelistChecker

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/rollup/L1MessageQueueWithGasPriceOracle.sol`
- Источник данных: scroll-contracts/src/L1/rollup/L1MessageQueueWithGasPriceOracle.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateWhitelistChecker. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L1/rollup/L1MessageQueueWithGasPriceOracle.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/rollup/L1MessageQueueWithGasPriceOracle.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/rollup/L1MessageQueueWithGasPriceOracle.sol) · multiple · SHA-256 44324bf7f526384bee7d9b7420069abf57e78176be87c8f8c7bbdbb9e5206240_

```
Privileged functions: updateWhitelistChecker
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09144 — Привилегированные административные функции в scroll-contracts/src/L1/rollup/L2GasPriceOracle.sol: updateWhitelist, setIntrinsicParams

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/rollup/L2GasPriceOracle.sol`
- Источник данных: scroll-contracts/src/L1/rollup/L2GasPriceOracle.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateWhitelist, setIntrinsicParams. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L1/rollup/L2GasPriceOracle.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/rollup/L2GasPriceOracle.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/rollup/L2GasPriceOracle.sol) · multiple · SHA-256 6b172d915567b07a4372e2adab3671bf1b00c11817c0193da6496e8317a735fc_

```
Privileged functions: updateWhitelist, setIntrinsicParams
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09145 — Привилегированные административные функции в scroll-contracts/src/L1/rollup/MultipleVersionRollupVerifier.sol: updateVerifier

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/rollup/MultipleVersionRollupVerifier.sol`
- Источник данных: scroll-contracts/src/L1/rollup/MultipleVersionRollupVerifier.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateVerifier. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L1/rollup/MultipleVersionRollupVerifier.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/rollup/MultipleVersionRollupVerifier.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/rollup/MultipleVersionRollupVerifier.sol) · multiple · SHA-256 309bc55aa192b32f088e252a0e07c64d7600dcb4636af440ecb00b4e24dc4c72_

```
Privileged functions: updateVerifier
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09146 — Привилегированные административные функции в scroll-contracts/src/L1/rollup/ScrollChain.sol: revertBatch, finalizeEuclidInitialBatch, addSequencer, removeSequencer, addProver, removeProver, updateMaxNumTxInChunk, setPause

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/rollup/ScrollChain.sol`
- Источник данных: scroll-contracts/src/L1/rollup/ScrollChain.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: revertBatch, finalizeEuclidInitialBatch, addSequencer, removeSequencer, addProver, removeProver, updateMaxNumTxInChunk, setPause. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L1/rollup/ScrollChain.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/rollup/ScrollChain.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/rollup/ScrollChain.sol) · multiple · SHA-256 a10806b8e8f277e558509fe1076d3280f0b4723e358bc94f5382be15fdd03fe3_

```
Privileged functions: revertBatch, finalizeEuclidInitialBatch, addSequencer, removeSequencer, addProver, removeProver, updateMaxNumTxInChunk, setPause
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09148 — Привилегированные административные функции в scroll-contracts/src/L2/gateways/L2ERC1155Gateway.sol: updateTokenMapping

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/gateways/L2ERC1155Gateway.sol`
- Источник данных: scroll-contracts/src/L2/gateways/L2ERC1155Gateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateTokenMapping. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L2/gateways/L2ERC1155Gateway.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/gateways/L2ERC1155Gateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/gateways/L2ERC1155Gateway.sol) · multiple · SHA-256 567d5823d91cba01d4a889468f89c726bb465044004c517c148ce8cd3d1fafa7_

```
Privileged functions: updateTokenMapping
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09149 — Привилегированные административные функции в scroll-contracts/src/L2/gateways/L2ERC721Gateway.sol: updateTokenMapping

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/gateways/L2ERC721Gateway.sol`
- Источник данных: scroll-contracts/src/L2/gateways/L2ERC721Gateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateTokenMapping. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L2/gateways/L2ERC721Gateway.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/gateways/L2ERC721Gateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/gateways/L2ERC721Gateway.sol) · multiple · SHA-256 567d5823d91cba01d4a889468f89c726bb465044004c517c148ce8cd3d1fafa7_

```
Privileged functions: updateTokenMapping
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09150 — Привилегированные административные функции в scroll-contracts/src/L2/gateways/L2GatewayRouter.sol: setETHGateway, setDefaultERC20Gateway, setERC20Gateway

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/gateways/L2GatewayRouter.sol`
- Источник данных: scroll-contracts/src/L2/gateways/L2GatewayRouter.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: setETHGateway, setDefaultERC20Gateway, setERC20Gateway. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L2/gateways/L2GatewayRouter.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/gateways/L2GatewayRouter.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/gateways/L2GatewayRouter.sol) · multiple · SHA-256 0ba5b5898f9bf7cc74eff33ce5345afae100dbe0cb78eed820313e5d279abbb6_

```
Privileged functions: setETHGateway, setDefaultERC20Gateway, setERC20Gateway
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09151 — Привилегированные административные функции в scroll-contracts/src/L2/gateways/usdc/L2USDCGateway.sol: updateCircleCaller, pauseDeposit, pauseWithdraw

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/gateways/usdc/L2USDCGateway.sol`
- Источник данных: scroll-contracts/src/L2/gateways/usdc/L2USDCGateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateCircleCaller, pauseDeposit, pauseWithdraw. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L2/gateways/usdc/L2USDCGateway.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/gateways/usdc/L2USDCGateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/gateways/usdc/L2USDCGateway.sol) · multiple · SHA-256 76008f6dc4b691df13710a02121b96b76410e9863a09e512b2c81c014dc85fd1_

```
Privileged functions: updateCircleCaller, pauseDeposit, pauseWithdraw
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09152 — Привилегированные административные функции в scroll-contracts/src/L2/gateways/usdc/draft-L2USDCGatewayCCTP.sol: updateCCTPContracts

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/gateways/usdc/draft-L2USDCGatewayCCTP.sol`
- Источник данных: scroll-contracts/src/L2/gateways/usdc/draft-L2USDCGatewayCCTP.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateCCTPContracts. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L2/gateways/usdc/draft-L2USDCGatewayCCTP.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/gateways/usdc/draft-L2USDCGatewayCCTP.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/gateways/usdc/draft-L2USDCGatewayCCTP.sol) · multiple · SHA-256 927a9a131474771e7a6025b058886c146d56b8594bfb46b0ff92124a3d41459a_

```
Privileged functions: updateCCTPContracts
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09154 — Привилегированные административные функции в scroll-contracts/src/L2/predeploys/L1BlockContainer.sol: initialize, updateWhitelist

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/predeploys/L1BlockContainer.sol`
- Источник данных: scroll-contracts/src/L2/predeploys/L1BlockContainer.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: initialize, updateWhitelist. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L2/predeploys/L1BlockContainer.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/predeploys/L1BlockContainer.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/predeploys/L1BlockContainer.sol) · multiple · SHA-256 cff0c68f0fd06e1f3a4ee54f3445c04164d2782e0ca86268f4a07efa7dace055_

```
Privileged functions: initialize, updateWhitelist
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09155 — Привилегированные административные функции в scroll-contracts/src/L2/predeploys/L1GasPriceOracle.sol: setOverhead, setScalar, setCommitScalar, setBlobScalar, updateWhitelist, enableCurie

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/predeploys/L1GasPriceOracle.sol`
- Источник данных: scroll-contracts/src/L2/predeploys/L1GasPriceOracle.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: setOverhead, setScalar, setCommitScalar, setBlobScalar, updateWhitelist, enableCurie. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L2/predeploys/L1GasPriceOracle.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/predeploys/L1GasPriceOracle.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/predeploys/L1GasPriceOracle.sol) · multiple · SHA-256 f51c35bb04fbd70c342ae93dbf5d235ff8535e18e3eb065cdfde3f4e141acdc7_

```
Privileged functions: setOverhead, setScalar, setCommitScalar, setBlobScalar, updateWhitelist, enableCurie
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09157 — Привилегированные административные функции в scroll-contracts/src/L2/predeploys/L2MessageQueue.sol: initialize

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/predeploys/L2MessageQueue.sol`
- Источник данных: scroll-contracts/src/L2/predeploys/L2MessageQueue.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: initialize. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L2/predeploys/L2MessageQueue.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/predeploys/L2MessageQueue.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/predeploys/L2MessageQueue.sol) · multiple · SHA-256 e4ca59164f6e3ff1d9e10ad8a622313b85edf2aadad2678eaefa6a16425e39d7_

```
Privileged functions: initialize
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09158 — Привилегированные административные функции в scroll-contracts/src/L2/predeploys/L2TxFeeVault.sol: updateMessenger, updateRecipient, updateMinWithdrawAmount

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/predeploys/L2TxFeeVault.sol`
- Источник данных: scroll-contracts/src/L2/predeploys/L2TxFeeVault.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateMessenger, updateRecipient, updateMinWithdrawAmount. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L2/predeploys/L2TxFeeVault.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/predeploys/L2TxFeeVault.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/predeploys/L2TxFeeVault.sol) · multiple · SHA-256 9b6a64a9f27391ea141163a1e7ced8c2fe432a22fa8fbad9a3e8440d4c9c1c59_

```
Privileged functions: updateMessenger, updateRecipient, updateMinWithdrawAmount
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09159 — Привилегированные административные функции в scroll-contracts/src/L2/predeploys/Whitelist.sol: updateWhitelistStatus

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/predeploys/Whitelist.sol`
- Источник данных: scroll-contracts/src/L2/predeploys/Whitelist.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateWhitelistStatus. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/L2/predeploys/Whitelist.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L2/predeploys/Whitelist.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L2/predeploys/Whitelist.sol) · multiple · SHA-256 b618c4ce5d2a585fe810fba8f3f2d5cd292b3697b149e1fc02d693c9fc47eb53_

```
Privileged functions: updateWhitelistStatus
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09161 — Привилегированные административные функции в scroll-contracts/src/gas-swap/GasSwap.sol: withdraw, updateFeeRatio, updateApprovedTarget

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/gas-swap/GasSwap.sol`
- Источник данных: scroll-contracts/src/gas-swap/GasSwap.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: withdraw, updateFeeRatio, updateApprovedTarget. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/gas-swap/GasSwap.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/gas-swap/GasSwap.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/gas-swap/GasSwap.sol) · multiple · SHA-256 e2050d93291c41fb274d2dc7c6e1f2ee3fecbd3d6e20a867023e5bdacaff2a06_

```
Privileged functions: withdraw, updateFeeRatio, updateApprovedTarget
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09162 — Привилегированные административные функции в scroll-contracts/src/libraries/ScrollMessengerBase.sol: updateFeeVault, setPause

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/libraries/ScrollMessengerBase.sol`
- Источник данных: scroll-contracts/src/libraries/ScrollMessengerBase.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateFeeVault, setPause. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/libraries/ScrollMessengerBase.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/libraries/ScrollMessengerBase.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/libraries/ScrollMessengerBase.sol) · multiple · SHA-256 0bc53cba0e646a9050b16b3b4b5df422672d2e8175f2e4faeb2c9a66035002d9_

```
Privileged functions: updateFeeVault, setPause
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09163 — Привилегированные административные функции в scroll-contracts/src/libraries/common/OwnableBase.sol: renounceOwnership, transferOwnership

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/libraries/common/OwnableBase.sol`
- Источник данных: scroll-contracts/src/libraries/common/OwnableBase.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: renounceOwnership, transferOwnership. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/libraries/common/OwnableBase.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/libraries/common/OwnableBase.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/libraries/common/OwnableBase.sol) · multiple · SHA-256 c9178db25d8ef1b1a83ff9fe952090d86c1ef54a1f84a5a67cc0aac7fdd62bd6_

```
Privileged functions: renounceOwnership, transferOwnership
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09164 — Привилегированные административные функции в scroll-contracts/src/libraries/token/ScrollStandardERC20Factory.sol: deployL2Token

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/libraries/token/ScrollStandardERC20Factory.sol`
- Источник данных: scroll-contracts/src/libraries/token/ScrollStandardERC20Factory.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: deployL2Token. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/libraries/token/ScrollStandardERC20Factory.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/libraries/token/ScrollStandardERC20Factory.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/libraries/token/ScrollStandardERC20Factory.sol) · multiple · SHA-256 fde0c93920eae0f64b7046c86bd2511daef797adfae7878fd43b6c17036aeb1d_

```
Privileged functions: deployL2Token
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09166 — Привилегированные административные функции в scroll-contracts/src/lido/LidoGatewayManager.sol: grantRole, revokeRole

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/lido/LidoGatewayManager.sol`
- Источник данных: scroll-contracts/src/lido/LidoGatewayManager.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: grantRole, revokeRole. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/lido/LidoGatewayManager.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/lido/LidoGatewayManager.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/lido/LidoGatewayManager.sol) · multiple · SHA-256 4a2ad8b435792e795c4d4a91364ba673646d967d0f6d0166280410436b889be6_

```
Privileged functions: grantRole, revokeRole
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09167 — Привилегированные административные функции в scroll-contracts/src/misc/Fallback.sol: withdraw, execute

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/misc/Fallback.sol`
- Источник данных: scroll-contracts/src/misc/Fallback.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: withdraw, execute. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/misc/Fallback.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/misc/Fallback.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/misc/Fallback.sol) · multiple · SHA-256 ba80cb3fc345c9c268fb142dc621dbde8a20e93b38d439f2fd72bf79ef8a4437_

```
Privileged functions: withdraw, execute
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09168 — Привилегированные административные функции в scroll-contracts/src/rate-limiter/ETHRateLimiter.sol: updateTotalLimit

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/rate-limiter/ETHRateLimiter.sol`
- Источник данных: scroll-contracts/src/rate-limiter/ETHRateLimiter.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 37.0 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateTotalLimit. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле scroll-contracts/src/rate-limiter/ETHRateLimiter.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/rate-limiter/ETHRateLimiter.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/rate-limiter/ETHRateLimiter.sol) · multiple · SHA-256 e3534e87c12567c01be52d05897cdb34730e50ce0f8bf08d67330ffa7745cf95_

```
Privileged functions: updateTotalLimit
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-09221 — github.com/btcsuite/btcd v0.20.1-beta затронут GHSA-2chg-86hq-7w38 (CVE-2022-44797, GO-2022-1098)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/btcsuite/btcd@v0.20.1-beta`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.9 / 100
- CVSS v3.1: 9.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-2chg-86hq-7w38 (CVE-2022-44797, GO-2022-1098) для пакета Go github.com/btcsuite/btcd версии v0.20.1-beta: btcd mishandles witness size checking. Ни одна из затронутых функций (github.com/btcsuite/btcd/wire.MsgBlock.BtcDecode, github.com/btcsuite/btcd/wire.MsgBlock.Deserialize, github.com/btcsuite/btcd/wire.MsgBlock.DeserializeNoWitness, github.com/btcsuite/btcd/wire.MsgBlock.DeserializeTxLoc, github.com/btcsuite/btcd/wire.MsgTx.BtcDecode, github.com/btcsuite/btcd/wire.MsgTx.Deserialize …) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2chg-86hq-7w38
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2chg-86hq-7w38](https://osv.dev/vulnerability/GHSA-2chg-86hq-7w38) · line 26 · SHA-256 28eb7bd6b28f9fe087095a5d3cdea6c2e8334b9e816c8e69f1cb613d0f143917_

```
{"id": "GHSA-2chg-86hq-7w38", "aliases": ["CVE-2022-44797", "GO-2022-1098"], "modified": "2024-05-20T21:36:55Z", "summary": "btcd mishandles witness size checking", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09223 — github.com/consensys/gnark-crypto v0.16.0 затронут GHSA-fj2x-735w-74vq (GO-2025-4087)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/consensys/gnark-crypto@v0.16.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.9 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-fj2x-735w-74vq (GO-2025-4087) для пакета Go github.com/consensys/gnark-crypto версии v0.16.0: gnark-crypto allows unchecked memory allocation during vector deserialization. Ни одна из затронутых функций (github.com/consensys/gnark-crypto/ecc/secp256k1/fr.Vector.AsyncReadFrom, github.com/consensys/gnark-crypto/ecc/secp256k1/fr.Vector.ReadFrom, github.com/consensys/gnark-crypto/ecc/secp256k1/fr.Vector.UnmarshalBinary, github.com/consensys/gnark-crypto/ecc/bw6-633/fp.Vector.AsyncReadFrom, github.com/consensys/gnark-crypto/ecc/bw6-633/fp.Vector.ReadFrom, github.com/consensys/gnark-crypto/ecc/bw6-633/fp.Vector.UnmarshalBinary …) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-fj2x-735w-74vq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-fj2x-735w-74vq](https://osv.dev/vulnerability/GHSA-fj2x-735w-74vq) · line 32 · SHA-256 7b4771c79cb8a0f08814dbf3793abb7c4b41d6f7d5951179fce2f230ab9707b0_

```
{"id": "GHSA-fj2x-735w-74vq", "aliases": ["GO-2025-4087"], "modified": "2026-09-10T03:50:29.734008925Z", "summary": "gnark-crypto allows unchecked memory allocation during vector deserialization", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.18.1, 0.19.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09224 — github.com/docker/cli v25.0.4-0.20240305161310-2bf4225ad269+incompatible затронут GHSA-p436-gjf2-799p (CVE-2025-15558, GO-2026-4610)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/docker/cli@v25.0.4-0.20240305161310-2bf4225ad269+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-p436-gjf2-799p (CVE-2025-15558, GO-2026-4610) для пакета Go github.com/docker/cli версии v25.0.4-0.20240305161310-2bf4225ad269+incompatible: Docker CLI Plugins: Uncontrolled Search Path Element Leads to Local Privilege Escalation on Windows. Ни одна из затронутых функций (github.com/docker/cli/cli-plugins/manager.defaultSystemPluginDirs) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-p436-gjf2-799p
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-p436-gjf2-799p](https://osv.dev/vulnerability/GHSA-p436-gjf2-799p) · line 38 · SHA-256 2f7237556abb24430f3781ebb08f5844efe5c4d2fb42168e3ae41ee89acd1feb_

```
{"id": "GHSA-p436-gjf2-799p", "aliases": ["BIT-docker-cli-2025-15558", "CVE-2025-15558", "GO-2026-4610"], "modified": "2026-09-10T03:50:39.956404854Z", "summary": "Docker CLI Plugins: Uncontrolled Search Path Element Leads to Local Privilege Escalation on Windows", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (29.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09227 — github.com/docker/docker v26.1.0+incompatible затронут GHSA-rg2x-37c3-w2rh (CVE-2026-42306, GO-2026-5617)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.9 / 100
- CVSS v3.1: 7.2 (`CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:N/I:H/A:H`)

OSV.dev сообщает GHSA-rg2x-37c3-w2rh (CVE-2026-42306, GO-2026-5617) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Docker: Race condition in docker cp allows bind mount redirection to host path. Ни одна из затронутых функций (github.com/docker/docker/daemon.Daemon.openContainerFS) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rg2x-37c3-w2rh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rg2x-37c3-w2rh](https://osv.dev/vulnerability/GHSA-rg2x-37c3-w2rh) · line 39 · SHA-256 1e37c034d0c067cb8cd66e219cb54fb68eb260f0ad00b3cc8953501288ec0324_

```
{"id": "GHSA-rg2x-37c3-w2rh", "aliases": ["CVE-2026-42306", "GO-2026-5617"], "modified": "2026-09-10T03:50:47.528575532Z", "summary": "Docker: Race condition in docker cp allows bind mount redirection to host path", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:N/I:H/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09228 — github.com/docker/docker v26.1.0+incompatible затронут GHSA-v23v-6jw2-98fq (CVE-2024-41110, GO-2024-3005)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.9 / 100
- CVSS v3.1: 9.9 (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-v23v-6jw2-98fq (CVE-2024-41110, GO-2024-3005) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Authz zero length regression. Ни одна из затронутых функций (github.com/docker/docker/pkg/authorization.Ctx.AuthZRequest, github.com/docker/docker/pkg/authorization.Ctx.AuthZResponse, github.com/docker/docker/pkg/authorization.sendBody) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-v23v-6jw2-98fq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-v23v-6jw2-98fq](https://osv.dev/vulnerability/GHSA-v23v-6jw2-98fq) · line 39 · SHA-256 7390f2eb685de469a6fab83459f3e95e4bf8b0fa74deee29cd2fdebb4493beeb_

```
{"id": "GHSA-v23v-6jw2-98fq", "aliases": ["CVE-2024-41110", "GO-2024-3005"], "modified": "2026-09-10T03:50:16.900418046Z", "summary": "Authz zero length regression", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (23.0.15, 25.0.6, 26.1.5, 27.1.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09229 — github.com/docker/docker v26.1.0+incompatible затронут GHSA-vp62-88p7-qqf5 (CVE-2026-41568, GO-2026-5668)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.9 / 100
- CVSS v3.1: 6.1 (`CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:N/I:L/A:H`)

OSV.dev сообщает GHSA-vp62-88p7-qqf5 (CVE-2026-41568, GO-2026-5668) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Docker: Race condition in docker cp allows creation of arbitrary empty files on the host via symlink swap. Ни одна из затронутых функций (github.com/docker/docker/daemon.Daemon.createIfNotExists, github.com/docker/docker/daemon.Daemon.openContainerFS) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vp62-88p7-qqf5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vp62-88p7-qqf5](https://osv.dev/vulnerability/GHSA-vp62-88p7-qqf5) · line 39 · SHA-256 ebf7b606499a4435f059ad63b1893b11c29261567570d083a5aff397fdb23f99_

```
{"id": "GHSA-vp62-88p7-qqf5", "aliases": ["CVE-2026-41568", "GO-2026-5668"], "modified": "2026-09-10T03:51:07.017544565Z", "summary": "Docker: Race condition in docker cp allows creation of arbitrary empty files on the host via symlink swap", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:N/I:L/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09230 — github.com/docker/docker v26.1.0+incompatible затронут GHSA-x86f-5xw2-fm2r (CVE-2026-41567, GO-2026-5746)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.9 / 100
- CVSS v3.1: 7.2 (`CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-x86f-5xw2-fm2r (CVE-2026-41567, GO-2026-5746) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Docker: `PUT /containers/{id}/archive` executes container binary on the host. Ни одна из затронутых функций (github.com/docker/docker/daemon.Daemon.containerExtractToDir) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x86f-5xw2-fm2r
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-x86f-5xw2-fm2r](https://osv.dev/vulnerability/GHSA-x86f-5xw2-fm2r) · line 39 · SHA-256 5bc10da6eec232c1f263d2cf4ba5656f8695307a0c4ad5bd13ee536999509f78_

```
{"id": "GHSA-x86f-5xw2-fm2r", "aliases": ["CVE-2026-41567", "GO-2026-5746"], "modified": "2026-09-10T03:50:47.998689316Z", "summary": "Docker: `PUT /containers/{id}/archive` executes container binary on the host", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09233 — github.com/jackc/pgx/v5 v5.5.4 затронут GHSA-9jj7-4m8r-rfcm (CVE-2026-33816, GO-2026-4772)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/jackc/pgx/v5@v5.5.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.9 / 100
- CVSS v3.1: 9.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-9jj7-4m8r-rfcm (CVE-2026-33816, GO-2026-4772) для пакета Go github.com/jackc/pgx/v5 версии v5.5.4: Memory-safety vulnerability in github.com/jackc/pgx/v5. Ни одна из затронутых функций (github.com/jackc/pgx/v5/pgproto3.Backend.Receive, github.com/jackc/pgx/v5/pgproto3.FunctionCall.Decode) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9jj7-4m8r-rfcm
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9jj7-4m8r-rfcm](https://osv.dev/vulnerability/GHSA-9jj7-4m8r-rfcm) · line 63 · SHA-256 7a0b31d7d1db8544206a5adb2d42c055d0bd19b4d22bec4feecfab5ab9aff27b_

```
{"id": "GHSA-9jj7-4m8r-rfcm", "aliases": ["CVE-2026-33816", "GO-2026-4772"], "modified": "2026-09-10T03:50:43.842159740Z", "summary": "Memory-safety vulnerability in github.com/jackc/pgx/v5.", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (5.9.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09234 — github.com/jackc/pgx/v5 v5.5.4 затронут GHSA-j88v-2chj-qfwx (CVE-2026-41889, GO-2026-5004)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/jackc/pgx/v5@v5.5.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-j88v-2chj-qfwx (CVE-2026-41889, GO-2026-5004) для пакета Go github.com/jackc/pgx/v5 версии v5.5.4: pgx: SQL Injection via placeholder confusion with dollar quoted string literals. Ни одна из затронутых функций (github.com/jackc/pgx/v5/internal/sanitize.Query.Sanitize, github.com/jackc/pgx/v5/internal/sanitize.SanitizeSQL) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j88v-2chj-qfwx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j88v-2chj-qfwx](https://osv.dev/vulnerability/GHSA-j88v-2chj-qfwx) · line 63 · SHA-256 51d4ffce36c02ebf4fc4e684785597c5615f1b4a246bb2dcf589a2afe1405744_

```
{"id": "GHSA-j88v-2chj-qfwx", "aliases": ["CVE-2026-41889", "GO-2026-5004"], "modified": "2026-09-10T03:51:02.204456790Z", "summary": "pgx: SQL Injection via placeholder confusion with dollar quoted string literals", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:L/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (5.9.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09235 — github.com/jackc/pgx/v5 v5.5.4 затронут GHSA-xgrm-4fwx-7qm8 (CVE-2026-33815, GO-2026-4771)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/jackc/pgx/v5@v5.5.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.9 / 100
- CVSS v3.1: 9.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-xgrm-4fwx-7qm8 (CVE-2026-33815, GO-2026-4771) для пакета Go github.com/jackc/pgx/v5 версии v5.5.4: pgx contains memory-safety vulnerability. Ни одна из затронутых функций (github.com/jackc/pgx/v5/pgproto3.Backend.Receive, github.com/jackc/pgx/v5/pgproto3.Bind.Decode) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xgrm-4fwx-7qm8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xgrm-4fwx-7qm8](https://osv.dev/vulnerability/GHSA-xgrm-4fwx-7qm8) · line 63 · SHA-256 d767e8df58c71c89100e456cbaa841a2ce73eaefe6275f6ccfe808edc242b19d_

```
{"id": "GHSA-xgrm-4fwx-7qm8", "aliases": ["CVE-2026-33815", "GO-2026-4771"], "modified": "2026-09-10T03:50:44.892822027Z", "summary": "pgx contains memory-safety vulnerability", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (5.9.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09236 — github.com/klauspost/compress v1.17.9 затронут GHSA-259r-337f-4rfw (CVE-2026-63209, GO-2026-5841)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/klauspost/compress@v1.17.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 29.9 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-259r-337f-4rfw (CVE-2026-63209, GO-2026-5841) для пакета Go github.com/klauspost/compress версии v1.17.9: Compress/s2: Integer Overflow or Wraparound and Out-of-bounds Write in compress. Ни одна из затронутых функций (github.com/klauspost/compress/s2.NewDict) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-259r-337f-4rfw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-259r-337f-4rfw](https://osv.dev/vulnerability/GHSA-259r-337f-4rfw) · line 68 · SHA-256 b415f1a2f3e954680bf032db6b47454a035b6a2af6b7a5a152588cc24bafce59_

```
{"id": "GHSA-259r-337f-4rfw", "aliases": ["CVE-2026-63209", "GO-2026-5841"], "modified": "2026-10-20T14:45:03.782718646Z", "summary": "Compress/s2: Integer Overflow or Wraparound and Out-of-bounds Write in compress", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.18.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09171 — atty 0.2.14 затронут GHSA-g98v-hv3f-hcfr (RUSTSEC-2021-0145)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/atty@0.2.14`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 22.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-g98v-hv3f-hcfr (RUSTSEC-2021-0145) для пакета crates.io atty версии 0.2.14: atty potential unaligned read. Бюллетень касается только целевых платформ windows; репозиторий объявляет цели сборки Rust riscv32im-unknown-none-elf, x86_64-unknown-linux-gnu.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-g98v-hv3f-hcfr
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-g98v-hv3f-hcfr](https://osv.dev/vulnerability/GHSA-g98v-hv3f-hcfr) · manifest · SHA-256 9228a57a9a8b7f41b438674902973bd538b3153409c5cadbe3da3a6d7bda8588_

```
{"id": "GHSA-g98v-hv3f-hcfr", "aliases": ["RUSTSEC-2021-0145"], "modified": "2026-09-10T03:49:53.897184297Z", "summary": "atty potential unaligned read", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-09173 — bincode 1.3.3: информационный бюллетень RUSTSEC-2025-0141 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `dependency:crates.io/bincode@1.3.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 19.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2025-0141 для пакета crates.io bincode версии 1.3.3 как информационный (unmaintained): Bincode is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0141
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2025-0141](https://osv.dev/vulnerability/RUSTSEC-2025-0141) · manifest · SHA-256 2d4ec91d374dc1d163952a86f9da46edd4e89ca1a0fd828fd523b2b1dcfe3a14_

```
{"id": "RUSTSEC-2025-0141", "aliases": [], "modified": "2026-01-16T11:07:28.867553Z", "summary": "Bincode is unmaintained", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-09174 — bincode 2.0.1: информационный бюллетень RUSTSEC-2025-0141 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `dependency:crates.io/bincode@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 19.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2025-0141 для пакета crates.io bincode версии 2.0.1 как информационный (unmaintained): Bincode is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0141
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2025-0141](https://osv.dev/vulnerability/RUSTSEC-2025-0141) · manifest · SHA-256 2d4ec91d374dc1d163952a86f9da46edd4e89ca1a0fd828fd523b2b1dcfe3a14_

```
{"id": "RUSTSEC-2025-0141", "aliases": [], "modified": "2026-01-16T11:07:28.867553Z", "summary": "Bincode is unmaintained", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-09202 — tokio 1.52.3 затронут RUSTSEC-2026-0386 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/tokio@1.52.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0386 для пакета crates.io tokio версии 1.52.3: `AsyncFd::new` and related constructors violate I/O safety. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни одна из затронутых функций (tokio::io::unix::AsyncFd::new, tokio::io::unix::AsyncFd::try_new, tokio::io::unix::AsyncFd::try_with_interest, tokio::io::unix::AsyncFd::with_interest) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

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

### QSI-2026-09218 — zstd-sys 2.0.16+zstd.1.5.7 затронут RUSTSEC-2026-0410 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-sys@2.0.16+zstd.1.5.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0410 для пакета crates.io zstd-sys версии 2.0.16+zstd.1.5.7: WebAssembly allocator shim corrupts memory on allocation failure. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень касается только целевых платформ wasm32; репозиторий объявляет цели сборки Rust riscv32im-unknown-none-elf, x86_64-unknown-linux-gnu.

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

### QSI-2026-09169 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 13.3 / 100
- CVSS v3.1: неприменимо

В 16 манифестах зависимостей QSI нашёл криптобиблиотеки (@noble/curves, @noble/hashes, @noble/secp256k1, bls12_381, ecdsa, elliptic, ethers, ff, golang.org/x/crypto, group, halo2, halo2_proofs, jubjub, k256, openssl), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · Cargo.lock, Cargo.toml, bridge-history-api/go.mod, common/go.mod, coordinator/go.mod, crates/l2geth/Cargo.toml, crates/libzkp/Cargo.toml, crates/libzkp_c/Cargo.toml, crates/prover-bin/Cargo.toml, database/go.mod, rollup/go.mod, scroll-contracts/lib/solmate/package-lock.json, scroll-contracts/lib/solmate/package.json, scroll-contracts/package.json, scroll-contracts/src/package.json, scroll-contracts/yarn.lock · SHA-256 ef277622fb248d216b2888b625b3f7717bf1d6447d41b0de6d0d8739e3eade2d_

```
Crypto libraries: @noble/curves, @noble/hashes, @noble/secp256k1, bls12_381, ecdsa, elliptic, ethers, ff, golang.org/x/crypto, group, halo2, halo2_proofs, jubjub, k256, openssl, p256, pasta_curves, ring, rustls, secp256k1, tweetnacl, web3. PQC support depends on the version for: openssl
```

**Ограничения проверки.** Отсутствие доказательств не является доказательством отсутствия: системные библиотеки и транзитивные зависимости могут не указываться.

**Рекомендация.** Определите источник поддержки PQC (TLS-терминатор, KMS/HSM, обновление библиотек).

**Повторная проверка.** Повторите сканирование после обновлений.

### QSI-2026-09170 — ansi_term 0.12.1: информационный бюллетень RUSTSEC-2021-0139 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/ansi_term@0.12.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2021-0139 для пакета crates.io ansi_term версии 0.12.1 как информационный (unmaintained): ansi_term is Unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2021-0139
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2021-0139](https://osv.dev/vulnerability/RUSTSEC-2021-0139) · manifest · SHA-256 de5d4542b27afa47634a32a636aaf6122580e13132fee8a7d4fc9eec3cbb2e7f_

```
{"id": "RUSTSEC-2021-0139", "aliases": [], "modified": "2023-09-06T22:52:31Z", "summary": "ansi_term is Unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-09172 — atty 0.2.14: информационный бюллетень RUSTSEC-2024-0375 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/atty@0.2.14`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2024-0375 для пакета crates.io atty версии 0.2.14 как информационный (unmaintained): `atty` is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0375
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2024-0375](https://osv.dev/vulnerability/RUSTSEC-2024-0375) · manifest · SHA-256 39d224b85bb38fb881a0b8e5f3a7a1bf4bfbc155c7be81a36b13991da6de9490_

```
{"id": "RUSTSEC-2024-0375", "aliases": [], "modified": "2024-09-26T12:26:22Z", "summary": "`atty` is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-09177 — derivative 2.2.0: информационный бюллетень RUSTSEC-2024-0388 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/derivative@2.2.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
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

### QSI-2026-09178 — fxhash 0.2.1: информационный бюллетень RUSTSEC-2025-0057 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/fxhash@0.2.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 11.8 / 100
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

### QSI-2026-09179 — generational-arena 0.2.9: информационный бюллетень RUSTSEC-2024-0014 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/generational-arena@0.2.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2024-0014 для пакета crates.io generational-arena версии 0.2.9 как информационный (unmaintained): `generational-arena` is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0014
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2024-0014](https://osv.dev/vulnerability/RUSTSEC-2024-0014) · manifest · SHA-256 6de48eaa3191b0b0ab99e1d0875c9a8fc60eb7a93700f740cc02617df7efd54b_

```
{"id": "RUSTSEC-2024-0014", "aliases": [], "modified": "2024-02-18T04:06:15Z", "summary": "`generational-arena` is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-09181 — instant 0.1.13: информационный бюллетень RUSTSEC-2024-0384 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/instant@0.1.13`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2024-0384 для пакета crates.io instant версии 0.1.13 как информационный (unmaintained): `instant` is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0384
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2024-0384](https://osv.dev/vulnerability/RUSTSEC-2024-0384) · manifest · SHA-256 7f4b719b4e4bb232235b9d7f05f5a0b3918208f119164caa2133d8b6ed869cee_

```
{"id": "RUSTSEC-2024-0384", "aliases": [], "modified": "2024-11-10T13:10:28Z", "summary": "`instant` is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-09182 — libsecp256k1 0.7.2: информационный бюллетень RUSTSEC-2025-0161 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/libsecp256k1@0.7.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2025-0161 для пакета crates.io libsecp256k1 версии 0.7.2 как информационный (unmaintained): libsecp256k1 is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0161
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2025-0161](https://osv.dev/vulnerability/RUSTSEC-2025-0161) · manifest · SHA-256 5a68aff0a0c8df7049664eab824bf743ee2c13e46cc82b6b7741a61779b10920_

```
{"id": "RUSTSEC-2025-0161", "aliases": [], "modified": "2026-04-14T11:30:08.962845Z", "summary": "libsecp256k1 is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-09189 — paste 1.0.15: информационный бюллетень RUSTSEC-2024-0436 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/paste@1.0.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
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

### QSI-2026-09190 — proc-macro-error2 2.0.1: информационный бюллетень RUSTSEC-2026-0173 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/proc-macro-error2@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 23:51 UTC
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
| **подпись транзакций и сообщений** | ECDSA (2) | QSI-2026-09126 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |
| **аутентификация и идентификация (сертификаты, токены, аттестация устройств)** | ECDSA (1) | QSI-2026-09125 | Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме |
| **роль не определена** | ECDSA (2) | QSI-2026-09124 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм в конечных полях | взламывает | Q1 | BN254 (alt_bn128) (1) | Взламывает Диффи–Хеллмана в конечных полях и DSA при любом размере. Переводите установление ключей на ML-KEM (на переходный период — гибрид с X25519 или ECDH), подписи — на ML-DSA или SLH-DSA. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | BN254 (alt_bn128) (1), ECDSA (6) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (36), Poseidon (4), SHA-2 (1), STARK (FRI) (7) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (36), Poseidon (4), SHA-2 (1), STARK (FRI) (7) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- tls_code: 5 (примеры: bridge-history-api/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS; common/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS; coordinator/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS)
- slither: 152 (примеры: slither is not installed on the server (pip install slither-analyzer + solc))

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P1 | QSI-2026-09123 | Удалите отключение проверки сертификатов в bridge-history-api/cmd/api/app/app.go. | устранение первопричины | Отключений проверки не осталось вне явно помеченного тестового кода. |
| P1 | QSI-2026-09132 | Примените шаблон checks-effects-interactions и/или ReentrancyGuard. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-09133 | Примените шаблон checks-effects-interactions и/или ReentrancyGuard. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-09147 | Примените шаблон checks-effects-interactions и/или ReentrancyGuard. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-09153 | Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-09156 | Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P2 | QSI-2026-09219 | Обновите github.com/gin-contrib/cors до исправленной версии (1.6.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-869c-j7wc-8jqv (CVE-2019-25211, GO-2024-2955). |
| P2 | QSI-2026-09220 | Обновите github.com/btcsuite/btcd до исправленной версии (0.24.2-beta.rc1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-27vh-h6mc-q6g8 (CVE-2024-38365, GO-2024-3189). |
| P2 | QSI-2026-09193 | Обновите quinn-proto до исправленной версии (0.11.18). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2026-0340. |
| P2 | QSI-2026-09194 | Обновите quinn-proto до исправленной версии (0.11.17). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2026-0341. |
| P2 | QSI-2026-09222 | Обновите github.com/btcsuite/btcd до исправленной версии (0.24.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3jgf-r68h-xfqm (CVE-2024-34478, GO-2024-2818). |
| P2 | QSI-2026-09226 | Обновите github.com/docker/docker до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pxq6-2prw-chj9 (CVE-2026-33997, GO-2026-4883). |
| P2 | QSI-2026-09232 | Обновите github.com/gorilla/websocket до исправленной версии (1.5.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w67g-5rqw-f597 (GO-2026-6278). |
| P2 | QSI-2026-09175 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-09197 | Обновите rustls до исправленной версии (0.23.45). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285). |
| P2 | QSI-2026-09198 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346). |
| P2 | QSI-2026-09203 | Обновите tracing-subscriber до исправленной версии (0.3.20). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xwfj-jgwm-7wp5 (CVE-2025-58160, RUSTSEC-2025-0055). |
| P2 | QSI-2026-09225 | Обновите github.com/docker/docker до исправленной версии (25.0.13, 28.0.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4vq8-7jfc-9cvp (CVE-2025-54410). |
| P2 | QSI-2026-09184 | Обновите lru до исправленной версии (0.16.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002). |
| P2 | QSI-2026-09186 | Обновите lru до исправленной версии (0.16.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002). |
| P2 | QSI-2026-09188 | Обновите p3-symmetric до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3g92-f9ch-qjcm. |
| P2 | QSI-2026-09200 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349). |
| P2 | QSI-2026-09199 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348). |
| P2 | QSI-2026-09221 | Обновите github.com/btcsuite/btcd до исправленной версии (0.23.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2chg-86hq-7w38 (CVE-2022-44797, GO-2022-1098). |
| P2 | QSI-2026-09223 | Обновите github.com/consensys/gnark-crypto до исправленной версии (0.18.1, 0.19.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fj2x-735w-74vq (GO-2025-4087). |
| P2 | QSI-2026-09224 | Обновите github.com/docker/cli до исправленной версии (29.2.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-p436-gjf2-799p (CVE-2025-15558, GO-2026-4610). |
| P2 | QSI-2026-09227 | Обновите github.com/docker/docker до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rg2x-37c3-w2rh (CVE-2026-42306, GO-2026-5617). |
| P2 | QSI-2026-09228 | Обновите github.com/docker/docker до исправленной версии (23.0.15, 25.0.6, 26.1.5, 27.1.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-v23v-6jw2-98fq (CVE-2024-41110, GO-2024-3005). |
| P2 | QSI-2026-09229 | Обновите github.com/docker/docker до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vp62-88p7-qqf5 (CVE-2026-41568, GO-2026-5668). |
| P2 | QSI-2026-09230 | Обновите github.com/docker/docker до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-x86f-5xw2-fm2r (CVE-2026-41567, GO-2026-5746). |
| P2 | QSI-2026-09233 | Обновите github.com/jackc/pgx/v5 до исправленной версии (5.9.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9jj7-4m8r-rfcm (CVE-2026-33816, GO-2026-4772). |
| P2 | QSI-2026-09234 | Обновите github.com/jackc/pgx/v5 до исправленной версии (5.9.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j88v-2chj-qfwx (CVE-2026-41889, GO-2026-5004). |
| P2 | QSI-2026-09235 | Обновите github.com/jackc/pgx/v5 до исправленной версии (5.9.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xgrm-4fwx-7qm8 (CVE-2026-33815, GO-2026-4771). |
| P2 | QSI-2026-09236 | Обновите github.com/klauspost/compress до исправленной версии (1.18.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-259r-337f-4rfw (CVE-2026-63209, GO-2026-5841). |
| P2 | QSI-2026-09171 | Обновите atty до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-g98v-hv3f-hcfr (RUSTSEC-2021-0145). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-09129 | Используйте OpenZeppelin ECDSA.recover с разделением доменов EIP-712 и nonce. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-09176 | Разберите RUSTSEC-2026-0387; при необходимости обновите crypto-bigint до исправленной версии (0.7.6). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0387 или результат разбора записан. |
| P3 | QSI-2026-09180 | Разберите RUSTSEC-2026-0258; при необходимости обновите h2 до исправленной версии (0.4.16). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0258 или результат разбора записан. |
| P3 | QSI-2026-09183 | Разберите RUSTSEC-2026-0418; при необходимости обновите libz-sys до исправленной версии (1.1.31). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0418 или результат разбора записан. |
| P3 | QSI-2026-09185 | Разберите RUSTSEC-2026-0253; при необходимости обновите lru до исправленной версии (0.18.2). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0253 или результат разбора записан. |
| P3 | QSI-2026-09187 | Разберите RUSTSEC-2026-0253; при необходимости обновите lru до исправленной версии (0.18.2). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0253 или результат разбора записан. |
| P3 | QSI-2026-09191 | Разберите RUSTSEC-2026-0338; при необходимости обновите quinn-proto до исправленной версии (0.11.18). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0338 или результат разбора записан. |
| P3 | QSI-2026-09192 | Разберите RUSTSEC-2026-0339; при необходимости обновите quinn-proto до исправленной версии (0.11.17). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0339 или результат разбора записан. |
| P3 | QSI-2026-09195 | Разберите RUSTSEC-2026-0342; при необходимости обновите quinn-proto до исправленной версии (0.11.17). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0342 или результат разбора записан. |
| P3 | QSI-2026-09196 | Разберите RUSTSEC-2026-0220; при необходимости обновите ruint до исправленной версии (1.20.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0220 или результат разбора записан. |
| P3 | QSI-2026-09201 | Разберите RUSTSEC-2026-0382 (CVE-2026-111943); при необходимости обновите rustls-webpki до исправленной версии (0.103.16, 0.104.0-alpha.8). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0382 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-09204 | Разберите RUSTSEC-2026-0381 (CVE-2026-111943); при необходимости обновите webpki-roots до исправленной версии (0.26.11, 1.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0381 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-09205 | Разберите RUSTSEC-2026-0391; при необходимости обновите zstd до исправленной версии (0.14.3). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0391 или результат разбора записан. |
| P3 | QSI-2026-09206 | Разберите RUSTSEC-2026-0395; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0395 или результат разбора записан. |
| P3 | QSI-2026-09207 | Разберите RUSTSEC-2026-0396; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0396 или результат разбора записан. |
| P3 | QSI-2026-09208 | Разберите RUSTSEC-2026-0397; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0397 или результат разбора записан. |
| P3 | QSI-2026-09209 | Разберите RUSTSEC-2026-0398; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0398 или результат разбора записан. |
| P3 | QSI-2026-09210 | Разберите RUSTSEC-2026-0399; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0399 или результат разбора записан. |
| P3 | QSI-2026-09211 | Разберите RUSTSEC-2026-0400; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0400 или результат разбора записан. |
| P3 | QSI-2026-09212 | Разберите RUSTSEC-2026-0401; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0401 или результат разбора записан. |
| P3 | QSI-2026-09213 | Разберите RUSTSEC-2026-0402; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0402 или результат разбора записан. |
| P3 | QSI-2026-09214 | Разберите RUSTSEC-2026-0403; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0403 или результат разбора записан. |
| P3 | QSI-2026-09215 | Разберите RUSTSEC-2026-0404; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0404 или результат разбора записан. |
| P3 | QSI-2026-09216 | Разберите RUSTSEC-2026-0405; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0405 или результат разбора записан. |
| P3 | QSI-2026-09217 | Разберите RUSTSEC-2026-0406; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0406 или результат разбора записан. |
| P3 | QSI-2026-09231 | Разберите GO-2026-4887 (CVE-2026-34040); при необходимости обновите github.com/docker/docker до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование больше не сообщает GO-2026-4887 (CVE-2026-34040) или результат разбора записан. |
| P3 | QSI-2026-09202 | Разберите RUSTSEC-2026-0386; при необходимости обновите tokio до исправленной версии (1.51.6, 1.53.3). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0386 или результат разбора записан. |
| P3 | QSI-2026-09218 | Разберите RUSTSEC-2026-0410; при необходимости обновите zstd-sys до исправленной версии (2.1.2). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0410 или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-09126 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-09124 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-09125 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-09165 | Внесите использования ? в contract:scroll-contracts/src/libraries/verifier/RollupVerifier.sol в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-09127 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-09130 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-09131 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-09160 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09126 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-09124 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-09125 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-09165 | Запланируйте миграцию ? на ? (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ? или гибридной схемы. |
| P4 | QSI-2026-09128 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09134 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09135 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09136 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09137 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09138 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09139 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09140 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09141 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09142 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09143 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09144 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09145 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09146 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09148 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09149 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09150 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09151 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09152 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09154 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09155 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09157 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09158 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09159 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09161 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09162 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09163 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09164 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09166 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09167 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09168 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-09173 | Замените bincode поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | bincode заменён или решение зафиксировано. |
| P4 | QSI-2026-09174 | Замените bincode поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | bincode заменён или решение зафиксировано. |
| P4 | QSI-2026-09170 | Замените ansi_term поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | ansi_term заменён или решение зафиксировано. |
| P4 | QSI-2026-09172 | Замените atty поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | atty заменён или решение зафиксировано. |
| P4 | QSI-2026-09177 | Замените derivative поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | derivative заменён или решение зафиксировано. |
| P4 | QSI-2026-09178 | Замените fxhash поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | fxhash заменён или решение зафиксировано. |
| P4 | QSI-2026-09179 | Замените generational-arena поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | generational-arena заменён или решение зафиксировано. |
| P4 | QSI-2026-09181 | Замените instant поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | instant заменён или решение зафиксировано. |
| P4 | QSI-2026-09182 | Замените libsecp256k1 поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | libsecp256k1 заменён или решение зафиксировано. |
| P4 | QSI-2026-09189 | Замените paste поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | paste заменён или решение зафиксировано. |
| P4 | QSI-2026-09190 | Замените proc-macro-error2 поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | proc-macro-error2 заменён или решение зафиксировано. |

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
24. OSV advisory GHSA-259r-337f-4rfw — OSV.dev. <https://osv.dev/vulnerability/GHSA-259r-337f-4rfw> (modified 2026-10-20T14:45:03.782718646Z)
25. OSV advisory GHSA-27vh-h6mc-q6g8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-27vh-h6mc-q6g8> (modified 2025-08-21T04:05:13Z)
26. OSV advisory GHSA-2chg-86hq-7w38 — OSV.dev. <https://osv.dev/vulnerability/GHSA-2chg-86hq-7w38> (modified 2024-05-20T21:36:55Z)
27. OSV advisory GHSA-2mjx-qc3c-rqvc — OSV.dev. <https://osv.dev/vulnerability/GHSA-2mjx-qc3c-rqvc> (modified 2026-10-27T15:30:05.509305490Z)
28. OSV advisory GHSA-3g92-f9ch-qjcm — OSV.dev. <https://osv.dev/vulnerability/GHSA-3g92-f9ch-qjcm> (modified 2026-04-16T23:04:45.978452Z)
29. OSV advisory GHSA-3jgf-r68h-xfqm — OSV.dev. <https://osv.dev/vulnerability/GHSA-3jgf-r68h-xfqm> (modified 2024-08-07T19:55:49Z)
30. OSV advisory GHSA-4vq8-7jfc-9cvp — OSV.dev. <https://osv.dev/vulnerability/GHSA-4vq8-7jfc-9cvp> (modified 2026-09-10T03:50:25.738441655Z)
31. OSV advisory GHSA-869c-j7wc-8jqv — OSV.dev. <https://osv.dev/vulnerability/GHSA-869c-j7wc-8jqv> (modified 2025-11-03T22:47:01Z)
32. OSV advisory GHSA-9jj7-4m8r-rfcm — OSV.dev. <https://osv.dev/vulnerability/GHSA-9jj7-4m8r-rfcm> (modified 2026-09-10T03:50:43.842159740Z)
33. OSV advisory GHSA-c8m5-c952-6cm4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4> (modified 2026-10-27T16:15:05.354395696Z)
34. OSV advisory GHSA-fj2x-735w-74vq — OSV.dev. <https://osv.dev/vulnerability/GHSA-fj2x-735w-74vq> (modified 2026-09-10T03:50:29.734008925Z)
35. OSV advisory GHSA-g98v-hv3f-hcfr — OSV.dev. <https://osv.dev/vulnerability/GHSA-g98v-hv3f-hcfr> (modified 2026-09-10T03:49:53.897184297Z)
36. OSV advisory GHSA-h2v8-394m-p7vv — OSV.dev. <https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv> (modified 2026-10-27T16:15:05.337819489Z)
37. OSV advisory GHSA-j88v-2chj-qfwx — OSV.dev. <https://osv.dev/vulnerability/GHSA-j88v-2chj-qfwx> (modified 2026-09-10T03:51:02.204456790Z)
38. OSV advisory GHSA-p436-gjf2-799p — OSV.dev. <https://osv.dev/vulnerability/GHSA-p436-gjf2-799p> (modified 2026-09-10T03:50:39.956404854Z)
39. OSV advisory GHSA-pxq6-2prw-chj9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-pxq6-2prw-chj9> (modified 2026-09-10T03:50:40.571293679Z)
40. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-10-30T15:45:11.580215361Z)
41. OSV advisory GHSA-rg2x-37c3-w2rh — OSV.dev. <https://osv.dev/vulnerability/GHSA-rg2x-37c3-w2rh> (modified 2026-09-10T03:50:47.528575532Z)
42. OSV advisory GHSA-rhfx-m35p-ff5j — OSV.dev. <https://osv.dev/vulnerability/GHSA-rhfx-m35p-ff5j> (modified 2026-09-10T03:50:59.064354050Z)
43. OSV advisory GHSA-v23v-6jw2-98fq — OSV.dev. <https://osv.dev/vulnerability/GHSA-v23v-6jw2-98fq> (modified 2026-09-10T03:50:16.900418046Z)
44. OSV advisory GHSA-vp62-88p7-qqf5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-vp62-88p7-qqf5> (modified 2026-09-10T03:51:07.017544565Z)
45. OSV advisory GHSA-w44r-93j7-qv28 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28> (modified 2026-10-27T16:15:05.340347056Z)
46. OSV advisory GHSA-w67g-5rqw-f597 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w67g-5rqw-f597> (modified 2026-09-10T03:50:54.128553228Z)
47. OSV advisory GHSA-x86f-5xw2-fm2r — OSV.dev. <https://osv.dev/vulnerability/GHSA-x86f-5xw2-fm2r> (modified 2026-09-10T03:50:47.998689316Z)
48. OSV advisory GHSA-xgrm-4fwx-7qm8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-xgrm-4fwx-7qm8> (modified 2026-09-10T03:50:44.892822027Z)
49. OSV advisory GHSA-xwfj-jgwm-7wp5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-xwfj-jgwm-7wp5> (modified 2026-09-10T03:50:27.766863705Z)
50. OSV advisory GO-2026-4887 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-4887> (modified 2026-04-03T20:59:19.226161232Z)
51. OSV advisory RUSTSEC-2021-0139 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2021-0139> (modified 2023-09-06T22:52:31Z)
52. OSV advisory RUSTSEC-2024-0014 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0014> (modified 2024-02-18T04:06:15Z)
53. OSV advisory RUSTSEC-2024-0375 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0375> (modified 2024-09-26T12:26:22Z)
54. OSV advisory RUSTSEC-2024-0384 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0384> (modified 2024-11-10T13:10:28Z)
55. OSV advisory RUSTSEC-2024-0388 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0388> (modified 2024-11-10T13:34:40Z)
56. OSV advisory RUSTSEC-2024-0436 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0436> (modified 2026-01-27T22:03:15.694766Z)
57. OSV advisory RUSTSEC-2025-0057 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0057> (modified 2025-09-05T19:09:01Z)
58. OSV advisory RUSTSEC-2025-0141 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0141> (modified 2026-01-16T11:07:28.867553Z)
59. OSV advisory RUSTSEC-2025-0161 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0161> (modified 2026-04-14T11:30:08.962845Z)
60. OSV advisory RUSTSEC-2026-0173 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0173> (modified 2026-06-07T21:00:04.318567692Z)
61. OSV advisory RUSTSEC-2026-0220 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0220> (modified 2026-07-30T19:15:04.025918010Z)
62. OSV advisory RUSTSEC-2026-0253 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0253> (modified 2026-08-11T11:15:06.101553049Z)
63. OSV advisory RUSTSEC-2026-0258 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0258> (modified 2026-10-12T18:00:10.934581734Z)
64. OSV advisory RUSTSEC-2026-0338 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0338> (modified 2026-10-12T18:15:01.969514645Z)
65. OSV advisory RUSTSEC-2026-0339 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0339> (modified 2026-10-12T18:15:01.956822776Z)
66. OSV advisory RUSTSEC-2026-0340 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0340> (modified 2026-10-12T18:15:01.975478256Z)
67. OSV advisory RUSTSEC-2026-0341 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0341> (modified 2026-10-12T18:15:01.969505433Z)
68. OSV advisory RUSTSEC-2026-0342 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0342> (modified 2026-10-12T18:15:01.956681478Z)
69. OSV advisory RUSTSEC-2026-0381 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0381> (modified 2026-10-29T10:55:54.096394276Z)
70. OSV advisory RUSTSEC-2026-0382 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0382> (modified 2026-10-29T10:55:54.096394276Z)
71. OSV advisory RUSTSEC-2026-0386 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0386> (modified 2026-10-23T14:45:03.847864944Z)
72. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
73. OSV advisory RUSTSEC-2026-0391 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0391> (modified 2026-10-26T14:00:04.269245609Z)
74. OSV advisory RUSTSEC-2026-0395 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0395> (modified 2026-10-26T14:00:06.388344282Z)
75. OSV advisory RUSTSEC-2026-0396 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0396> (modified 2026-10-26T14:00:05.789682118Z)
76. OSV advisory RUSTSEC-2026-0397 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0397> (modified 2026-10-26T14:00:05.089587004Z)
77. OSV advisory RUSTSEC-2026-0398 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0398> (modified 2026-10-26T14:00:05.092082939Z)
78. OSV advisory RUSTSEC-2026-0399 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0399> (modified 2026-10-26T14:00:05.792431051Z)
79. OSV advisory RUSTSEC-2026-0400 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0400> (modified 2026-10-26T14:00:05.692077560Z)
80. OSV advisory RUSTSEC-2026-0401 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0401> (modified 2026-10-26T14:00:04.231502512Z)
81. OSV advisory RUSTSEC-2026-0402 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0402> (modified 2026-10-26T14:00:05.685817733Z)
82. OSV advisory RUSTSEC-2026-0403 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0403> (modified 2026-10-26T14:00:05.787441176Z)
83. OSV advisory RUSTSEC-2026-0404 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0404> (modified 2026-10-26T14:00:05.092817237Z)
84. OSV advisory RUSTSEC-2026-0405 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0405> (modified 2026-10-26T14:00:05.680942523Z)
85. OSV advisory RUSTSEC-2026-0406 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0406> (modified 2026-10-26T14:00:05.095427051Z)
86. OSV advisory RUSTSEC-2026-0410 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0410> (modified 2026-10-26T14:00:05.788985783Z)
87. OSV advisory RUSTSEC-2026-0418 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0418> (modified 2026-10-29T14:15:02.333141406Z)
88. OWASP Application Security Verification Standard — OWASP. <https://owasp.org/www-project-application-security-verification-standard/> (living standard — check the project page for the current version)
89. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
90. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
91. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)
92. Smart Contract Weakness Classification (SWC) Registry — SWC community (no longer actively maintained). <https://swcregistry.io/> (historic reference; still widely cited)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| Keccak-256 | Keccak-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 36 | 36 | bridge-history-api/internal/logic/l1_event_parser.go:417; bridge-history-api/internal/logic/l2_fetcher.go:178; bridge-history-api/internal/utils/utils.go:27 |
| Poseidon |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 4 | 4 | crates/prover-bin/src/deferral.rs:58; scroll-contracts/circomlib.d.ts:2; scroll-contracts/scripts/hardhat/ScrollChainCommitmentVerifier.deploy.ts:5 |
| SHA-2 | SHA-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 1 | 1 | common/utils/blob.go:4 |
| STARK (FRI) |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 7 | 7 | common/types/message/message.go:189; coordinator/internal/logic/submitproof/proof_receiver.go:234; coordinator/internal/logic/verifier/mock.go:24 |
| Crypto library | 0.1.0 | halo2_proofs (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.1.0-beta.2 | halo2 (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.10.81 | openssl (OpenSSL) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.12.1 | ff (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.12.1 | group (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.0 | group (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.1 | ff (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.4 | k256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.17.14 | ring (ring (Rust)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.23.41 | rustls (rustls) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.30.0 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.31.1 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.4.1 | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.5.1 | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.7.1 | bls12_381 (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.9.0 | jubjub (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | v0.32.0 | golang.org/x/crypto (Go x/crypto) | н/п | допустимо | 4 | 4 | bridge-history-api/go.mod:111; common/go.mod:239; coordinator/go.mod:104 |
| Crypto library | ^6.11.1 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | scroll-contracts/package.json |
| Crypto library | 0.14.5 | tweetnacl (TweetNaCl) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:10334 |
| Crypto library | 1.0.3 | tweetnacl (TweetNaCl) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:10339 |
| Crypto library | 1.2.11 | web3 (web3) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:11003 |
| Crypto library | 6.5.4 | elliptic (elliptic (Node)) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:3853 |
| Crypto library | 4.0.49 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:4771 |
| Crypto library | 5.6.4 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:4786 |
| Crypto library | 6.11.1 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:4822 |
| Crypto library | 1.2.0 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:736 |
| Crypto library | 1.3.0 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:743 |
| Crypto library | 1.0.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:750 |
| Crypto library | 1.3.2 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:755 |
| Crypto library | 1.3.3 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:760 |
| Crypto library | 1.5.5 | @noble/secp256k1 (noble-curves) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:765 |
| Crypto library | 4.0.3 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | scroll-contracts/yarn.lock:9225 |
| BN254 (alt_bn128) |  |  | уязвим (Шор) | допустимо | 1 | 1 | scroll-contracts/src/libraries/verifier/RollupVerifier.sol:24 |
| ECDSA |  |  | уязвим (Шор) | допустимо | 4 | 4 | common/utils/keystore.go:4; coordinator/internal/controller/proxy/client_manager.go:5; coordinator/internal/types/auth.go:4 |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 1 | 1 | rollup/internal/controller/sender/kms_signer.go:64 |
| ECDSA | secp256k1 (ecrecover) |  | уязвим (Шор) | допустимо | 1 | 1 | scroll-contracts/lib/solmate/src/tokens/ERC20.sol:130 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| .github/scripts/bump_version_dot_go.mjs | 1016 | `f5d1c54556940092885bcc1c919b9983bcf7c52b6cbc0ee6031d2574908e732f` | 0 |
| Cargo.lock | 265985 | `e4d0bf99df000206317c1f2fd9085488f72d05272a8cedfab99fb63e1555b5e7` | 0 |
| Cargo.toml | 3307 | `aa9d9a041e4ccf003e3d0573eebf876e0e13f57301cf4a42edc0ad4477a93ccd` | 0 |
| bridge-history-api/abi/backend_abi.go | 87007 | `4fc00b704b7e1e8acacf44b62121636d9c4790e0ac4e610ae47b0722cf7518ec` | 0 |
| bridge-history-api/cmd/api/app/app.go | 3115 | `3ba7c1d55a3a3f07c4a3b080b9597a8031dfec8ad0204fb137f0728c9a7bf436` | 0 |
| bridge-history-api/cmd/api/main.go | 94 | `8574b0b31ace70793a4610a2adbba7f39e1143c9dc590a0c7796d8a7b33df32e` | 0 |
| bridge-history-api/cmd/db_cli/app/app.go | 1267 | `17b0cd7c91a050fe9aac072c8995e02cc7b64c0c0cf140b17a415686f092a017` | 0 |
| bridge-history-api/cmd/db_cli/app/client.go | 2212 | `ec64def7bd47c610ddb7a83abfff5f29ee4af5be5bb755c68ca75999c3303c62` | 0 |
| bridge-history-api/cmd/db_cli/main.go | 97 | `69a9b0b430620aee987e0457bc71c0e463e75d581b966d96a2fce82daa27002f` | 0 |
| bridge-history-api/cmd/fetcher/app/app.go | 2553 | `d61e6259360bd6e617dc18e31217b66a9a97786ac50870dc54f921fd606a91a5` | 0 |
| bridge-history-api/cmd/fetcher/main.go | 98 | `c67862deba164e934ad3d161786c236d380f8448784d074746c945d9056150e1` | 0 |
| bridge-history-api/go.mod | 5818 | `acce397760f3b45e7b218d7b0ac7c4c7dc4e81f9e77cf830001980aad9874afd` | 0 |
| bridge-history-api/internal/config/config.go | 2940 | `548f3a75786598d07a6f33baad82c43dbbbe99f3dd8a90dadf3d78501f429708` | 0 |
| bridge-history-api/internal/controller/api/controller.go | 1203 | `aae89898ed52d1986beabad1a628dab63e919d670d207a49766eb45d427f61ab` | 0 |
| bridge-history-api/internal/controller/api/l2unclaimed_withdrawals_by_address.go | 1419 | `af1192bfde21c6d9b1041a3aaa0a5b6fff37e8b66a830b4f9def491b5a964da0` | 0 |
| bridge-history-api/internal/controller/api/l2withdrawals_by_address.go | 1302 | `c5e1fba46143a33275206381377407f01ef25ba365718ae3a769269cd180caf6` | 0 |
| bridge-history-api/internal/controller/api/txs_by_address.go | 1172 | `313fc7ab155e3864b7c71051248e7746f97dd3ddbc9dfdb3b8ac3386905af757` | 0 |
| bridge-history-api/internal/controller/api/txs_by_hashes.go | 1820 | `795418f1bd8d773799e7743e71769c05067898b3bd2bc897ea42f1c6d9f4db65` | 0 |
| bridge-history-api/internal/controller/fetcher/l1_fetcher.go | 6184 | `2484aabfc60b0ed9ac6eddb07eb45428f6078baed9a9ead2fb29a6af08382eb1` | 0 |
| bridge-history-api/internal/controller/fetcher/l2_fetcher.go | 5702 | `bcb5dab53a1122e2c3f07ae8f789523bc787a34e2139ebae36a7e0da9e05c783` | 0 |
| bridge-history-api/internal/logic/event_update.go | 11574 | `3a706e2ef5cba90eaf0f49b0fb8322cc9182176bc32c20077aa5dadeecc0ab05` | 0 |
| bridge-history-api/internal/logic/history_logic.go | 17915 | `56bf0a8dff9349c2ff882f2e8fb9ccac50f5570f423b1f10e6d0c030525c2fea` | 0 |
| bridge-history-api/internal/logic/history_logic_metrics.go | 822 | `9fdaf85af6b3c47241a877aedcb37a59ead23c7070f101430208a00793cc3855` | 0 |
| bridge-history-api/internal/logic/l1_event_parser.go | 23685 | `3feb3a699c5871cd6050a4a32a855fe1b304affc76890ff38167d2029a0ecfb0` | 0 |
| bridge-history-api/internal/logic/l1_fetcher.go | 15233 | `0a46c45526925bae7670f86b592ab74c05b8bbb8fda8d673f770fa1e55fff675` | 0 |
| bridge-history-api/internal/logic/l2_event_parser.go | 10708 | `9ee57cd4b8f395c07c579761ef267063d93bac6806ba8ca83ee1e7cef96f23f5` | 0 |
| bridge-history-api/internal/logic/l2_fetcher.go | 12880 | `b163f81dbbf79503d9229905b5570732678041a2c02babd5b5761040028ddf66` | 0 |
| bridge-history-api/internal/orm/batch_event.go | 5842 | `fb29fb34daac99f07a67615caacfa58a8cb8306220c5f7e466e9152d604e1448` | 0 |
| bridge-history-api/internal/orm/bridge_batch_deposit.go | 6983 | `5a5370c51e66f809fe82199ede2d12380ee71c00a50606366a30f1c94f569bc4` | 0 |
| bridge-history-api/internal/orm/cross_message.go | 24696 | `ec2383f784d8cb3b657f9bc0b7c93be982d1c2df7dece8d0df48a724010fef30` | 0 |
| bridge-history-api/internal/orm/migrate/migrate.go | 1307 | `32bc13ad2069deefce198d9c2270120e5bd78f381b4bfbb2d552743645f0c2e3` | 0 |
| bridge-history-api/internal/route/route.go | 1049 | `4ce8d7f9c525fc2c0c685f93d595e1cd1c9855317524eb428a5f7ac3d71e5dbe` | 0 |
| bridge-history-api/internal/types/events.go | 3259 | `d7d1047e1c56b38cbc5e18e471b3bcbe3b3ed01310d826c230676ed0f6f1ca5b` | 0 |
| bridge-history-api/internal/types/schema.go | 4814 | `d43e72d4e4f4c0c3344d3c2ecf7b53725817a0da8adaa463256e5f6b454ba494` | 0 |
| bridge-history-api/internal/utils/utils.go | 10379 | `e9e0ccc0594d70c05abc92db49dc60b0d85dd480f083cf8d370f1cda34dc0a68` | 0 |
| bridge-history-api/internal/utils/withdraw_trie.go | 5599 | `492e13bc4e9980e7804d732c50255d1517b3b41e496823847fa5b68a7b9717b1` | 0 |
| common/cmd/cmd.go | 2065 | `3512404d34682c901dffc105158ceed4d53135604d4a3028eaaa5003662b394f` | 0 |
| common/cmd/cmd_app.go | 2979 | `1feec376079efb40dd65c0dd6b713f1f043c1ee8e9a826ec11b63fb72144fb9f` | 0 |
| common/database/config.go | 580 | `024730f3fc3cb0236dd1c475d8ba47c63ee2da86025d75e548b5fe9229fd3da8` | 0 |
| common/database/db.go | 3448 | `9ecc36c5e232572a2a69ad0870aa247a6c953962eacfddb4da6c08346be43482` | 0 |
| common/database/iam.go | 3889 | `8411038f8a8e27dcf91e6365f76df702cbbb0b04293c9170bd6f7699a1ff2b1f` | 0 |
| common/database/iam_metrics.go | 1273 | `be0086ba01c29d4ededd745a7a27bbd2c46ba490c9353b6dfd0a02092dd92462` | 0 |
| common/go.mod | 14361 | `c940f27f76b9d34b17764cfabe77ef9f12407457aee6c1a0716ae1eb478303d5` | 0 |
| common/observability/ginmetrics/bloom.go | 1091 | `832eda7ba3e339662347f91c6968c7deeff26697a7290d85fb0c2ce4e857e9a2` | 0 |
| common/observability/ginmetrics/metric.go | 2441 | `459882d00d74512e4604f47da697546ef748ae4f0c3213378be73b3bad1c1a54` | 0 |
| common/observability/ginmetrics/middleware.go | 4773 | `88e8b40e8b7dc3dc94d88d4afc720dd821844c05d9df37851b469515ae6bf345` | 0 |
| common/observability/ginmetrics/types.go | 4201 | `d39725499a35df533822e9d372d9ca16c858f5bf6282bc0d38604ef3cd522df0` | 0 |
| common/observability/middleware.go | 488 | `381696fe80b172662ec04ad5802286b0e0206e9cc34100ed28d4c7dd6dcb2562` | 0 |
| common/observability/probes.go | 744 | `dc7154711f4113a4a4c20356055c5c8fc2e792174b5cd11ce14159e2be9ed9f6` | 0 |
| common/observability/server.go | 1514 | `817db9d9427e9457e6bd096c02dd95431c9ac53532563dc5b4cb2f9bcbf81025` | 0 |
| common/testcontainers/docker/interface.go | 939 | `e116a892737084d01b6ef9c993e7fd925e192fa32a1291d7bab37eaac6c176ad` | 0 |
| common/testcontainers/testcontainers.go | 9366 | `31d9fe1b046048421cd442a58d3286e1a0ad57844d0e60817990c434684d2d3a` | 0 |
| common/types/db.go | 11976 | `203f0821e7f463824ce37e306f7a47f937162e3f203a60ade68ff7ebbeafde5a` | 0 |
| common/types/errno.go | 1024 | `b5812a5fd0b36351b14f42c9798e2819a17f84bc4065d2a4c2321c8fbbbb74ad` | 0 |
| common/types/message/message.go | 10985 | `6ac79cdb11cc00e6ee70a0d71df9ff4822347511ca23ec672849d8a09342e6cb` | 0 |
| common/types/response.go | 1605 | `b1293a1d1d133d847254a14b0e91f7cd0b4ae79e3994fbc6aa72ca7c02915f6f` | 0 |
| common/utils/blob.go | 604 | `02dda04a4cd79b6ce7b9755ae8e963bc12acb59c604999069497c9893d109a09` | 0 |
| common/utils/flags.go | 3019 | `fa64c1df8b2bcd3c8bdb55b4256d171e9d33edf82898fcedc0dcc16adfb968c0` | 0 |
| common/utils/http.go | 542 | `19eb7bf391fa3dd84784d008024e1d0e244d75d5e4f01a243d481f9f6f34cfe3` | 0 |
| common/utils/keystore.go | 1240 | `756dd85807bc5ec75fcd06e13e087de2ceb1a275b6cb8e532e1fcec52e7876b8` | 0 |
| common/utils/logger.go | 1252 | `e0821252ce808f35b500c5e170f662bcf055def6e199577938f64ecb4f421206` | 0 |
| common/utils/rpc.go | 1512 | `aebe6ddf83eaa044e1e91816b4bede1369e4cbd2ba58638aee47a929b11f5e70` | 0 |
| common/utils/simulation.go | 1038 | `0921a2600b7ab138240a1640b2b410b75442ccffc292598333558818e598cb56` | 0 |
| common/utils/timezone.go | 149 | `282b21036b74009e14c98ff1ebe83dff194663d9b9368cc824c0b71cda244efc` | 0 |
| common/utils/trace_gas.go | 251 | `2c5456438c2adae5f55f7755544683111d5ba40dac09320311d61fcffb18235f` | 0 |
| common/utils/utils.go | 3823 | `e0746c8371a7f7fff5253a56a9a9c9563d4d97c2f3a9dd1665ecbe3a471e2de0` | 0 |
| common/utils/workerpool/workerpool.go | 1057 | `6eafb76b8eb58f7423e219d6441b4233f4312c75f630bfe5803b98303d4e83fd` | 0 |
| common/version/prover_version.go | 1880 | `8c9311baf9c88d6d5f847f3ac56be1ddc5691999b08f64cdec092cb90c293d0a` | 0 |
| common/version/version.go | 855 | `152e8c94eed22b880bb0f8c7406c562bb3b3d9a017e433a73910325b13484025` | 0 |
| coordinator/cmd/api/app/app.go | 3313 | `2b8f8650d2478d2c89cc9894995d9b317544ce8a1ac1e073136774a51c49c154` | 0 |
| coordinator/cmd/api/app/flags.go | 628 | `cae8ba098d44748054599eca1191cb2930ae257f2fab983d03f2066295a30e37` | 0 |
| coordinator/cmd/api/app/mock_app.go | 3732 | `0ecc3a5d6b2ee8c042cc79b627c2aa5090a399a70485c9c059b2416976a4d110` | 0 |
| coordinator/cmd/api/main.go | 87 | `36aba0447c1767f702e18026b1871f73011b84d489c8f32896400413bae2d2f2` | 0 |
| coordinator/cmd/cron/app/app.go | 2084 | `826a2fe4921bd59e67c2d3c72569ca747bfabd1bf430adf0eff95b4b745b3485` | 0 |
| coordinator/cmd/cron/main.go | 88 | `261fe29e7d87c5b591e2272f02a44f07e70a0b9e7b8cf98665f948fea105aff9` | 0 |
| coordinator/cmd/proxy/app/app.go | 3206 | `caf53185d635c6ffbe881052462c8e929f8b5264fcd56da95a4a012ce6241543` | 0 |
| coordinator/cmd/proxy/app/flags.go | 628 | `2c9de6b550b6f35cdb78943b9ca5ca73aad1905c752226cd4321321cc9171b0d` | 0 |
| coordinator/cmd/proxy/main.go | 89 | `3b6dc794a6dc00e81fda765152be91271bcbbb010ecee88a19d74d396dcaaacd` | 0 |
| coordinator/cmd/tool/tool.go | 3011 | `1c237127153b3b92f2cd29ab034c7ce07033dbbc0a2f04b567e900645ddffc43` | 0 |
| coordinator/cmd/tool/verify.go | 2604 | `58ceb55092a191ca1f733e69fd4e78f202284ca530329bcbc7af5028347d142f` | 0 |
| coordinator/go.mod | 5242 | `89e0160326fece48df3a159e84942b8d57384590b92bd677dd1b16ad21665ebd` | 0 |
| coordinator/internal/config/config.go | 3176 | `9fd01359fb54dcdc5483dee97b1b22906b13316a6fbfc57c62fc6a0ccf8e3a8e` | 0 |
| coordinator/internal/config/proxy_config.go | 1903 | `6d0204cce099ec58cb9735563c6220e3b37abaab12807bb652c17692093ab045` | 0 |
| coordinator/internal/controller/api/auth.go | 3787 | `28505ef283955f12be72bca33dee6d40129863b3939c4176ac2a3b9ff48b71ba` | 0 |
| coordinator/internal/controller/api/controller.go | 1374 | `1dc276ad389549c7351d4eb2a0516ad3154ad9f147ea79acd55b39352f0159d9` | 0 |
| coordinator/internal/controller/api/get_task.go | 4884 | `c16ab50cc09cc8c9d0cb341ce3ff9c91d48dc18660b6bae82f008dd530cc911d` | 0 |
| coordinator/internal/controller/api/l2_syncer.go | 1847 | `a099a15a220cb582521c781d6ef285ad18f26a4ec65a2c9ecc994f9d691d3beb` | 0 |
| coordinator/internal/controller/api/mock_syncer.go | 432 | `fe060da5cc3a499306782e318a04bdcbf943c52031dd7c54f2d674b3b62ec505` | 0 |
| coordinator/internal/controller/api/submit_proof.go | 1567 | `45d6b0a3c7df429348b4d9947c8c5ceea1bf2d61e505290cfc89d98eb739fb86` | 0 |
| coordinator/internal/controller/cron/cleanup_challenge.go | 841 | `5ab6840d0dce46a2e5d36a14c3e5b009c5a138b9b08d532d2c6b530647ff7dbc` | 0 |
| coordinator/internal/controller/cron/collect_proof.go | 14351 | `05689ab44f94a63c1b7b1603e7c6d2181f4e8c5b49b35552add756f86b6b4d5b` | 0 |
| coordinator/internal/controller/proxy/auth.go | 4449 | `7172ce57828c4e3561a7e86526ce7b539fa39da06b475699ca22e82ea568dac7` | 0 |
| coordinator/internal/controller/proxy/client.go | 7424 | `2670baa96d768aa79949ad6a44d89dfd4c1472dcebf8e43ed531695f31a30153` | 0 |
| coordinator/internal/controller/proxy/client_manager.go | 6048 | `6c09723039bef43302847c21ae5063aa30b9864fd71f1612ca33fc201a18e9cb` | 0 |
| coordinator/internal/controller/proxy/controller.go | 1244 | `f70d422b693d73d1382e54d2a833f4f9889fe493dc56d6a8f75098db94760670` | 0 |
| coordinator/internal/controller/proxy/get_task.go | 7391 | `5ea0bfd8ea0922271e2a46c28c16e7ae257b93b7d88c94a046ee20e8a2995e3b` | 0 |
| coordinator/internal/controller/proxy/persistent.go | 3179 | `69fe68dc9d078cda46ab9bb5a1e8d9f788f42c87c08182125fc03c4c1b36a3c6` | 0 |
| coordinator/internal/controller/proxy/prover_session.go | 9511 | `6fbc4f7bbf0fc253847b3c6cd1c28fcbf934afb3545703cb21d58a5757495ee7` | 0 |
| coordinator/internal/controller/proxy/submit_proof.go | 3319 | `e77b01584eaf6e3767692c0adbf593033d499d65b6b9c0ef7161699883b21243` | 0 |
| coordinator/internal/logic/auth/login.go | 5038 | `7b41462196427c004c8fa813d52c032425f44174a0b421048724078ed86027d1` | 0 |
| coordinator/internal/logic/libzkp/lib.go | 2943 | `c4f99e7b46afbfe6cbc956ef7ae0fcfb67809d16385525eda13220c0e6a46e47` | 0 |
| coordinator/internal/logic/libzkp/lib_mock.go | 1312 | `f34deaf22a6d32703359ee1ccf0a8b2fb0341d979bc74bcae0f758793c87a39d` | 0 |
| coordinator/internal/logic/libzkp/libzkp.h | 1909 | `53840cee67b9b672d85d7a97bc63ac3102790f4e733c9b4dba27b0ef4cf8d40e` | 0 |
| coordinator/internal/logic/libzkp/message_types.go | 510 | `b13bbaa03b3f1d072eb640f7f4a00ae326ca5e759ccf6305d7361a8ff8608d85` | 0 |
| coordinator/internal/logic/libzkp/mock_universal_task.go | 1536 | `2090e869c7a71fb837fd3c6c141e41dc536c8da38c46a78d154b7d57aab5f559` | 0 |
| coordinator/internal/logic/libzkp/universal_task.go | 1749 | `a2cba0d8c0ae847010cf5e4ccba51bc8366d8bdffb4a2ef6b88c3b3b21c503a1` | 0 |
| coordinator/internal/logic/provertask/batch_prover_task.go | 14135 | `ec97a5a4e45a7199c0108de7e32f0b9d84af63dee7de0af337f69e29eca57a92` | 0 |
| coordinator/internal/logic/provertask/bundle_prover_task.go | 12688 | `a097e25e46a16ecdb8558a37652d4851c0d7eb10ab12d691c0b22f7e615b0519` | 0 |
| coordinator/internal/logic/provertask/chunk_prover_task.go | 11465 | `3b7ef6d2c232e0d56cfa9b0e6568625dce91f64358fec62ee633a55afabf49f0` | 0 |
| coordinator/internal/logic/provertask/prover_task.go | 8378 | `f8ad45e3bee5a926f64dbbe60e1eecbee42fab9a77f79fe7e4aafee93c8050ca` | 0 |
| coordinator/internal/logic/submitproof/proof_receiver.go | 23751 | `824f4a28eb56e7e9058189803984211c21a2fab480ddca52bdd50af1e7ee54ed` | 0 |
| coordinator/internal/logic/verifier/mock.go | 1319 | `7c85d28508754a560659ee12c81e53a4c49c8f59068f11587bbc3589a4cea058` | 0 |
| coordinator/internal/logic/verifier/types.go | 409 | `cd899dfc45d58b64658e06fff0eb750685f43ca6bb39ff09a27a4e00c56ab794` | 0 |
| coordinator/internal/logic/verifier/verifier.go | 5927 | `09dc1fa48a00ee7f1bfc935b26f5130d6cca4aaec5bbcc69031b1d948c74d7a1` | 0 |
| coordinator/internal/middleware/challenge_jwt.go | 1258 | `beed6de5d9f98d071f22b5794f676a275fe33fc1cc365eafa042abfbc345a6ea` | 0 |
| coordinator/internal/middleware/jwt.go | 706 | `21ce120d617606bb673f1b9dbcb095b79e0b63912953c8114ab52ff3aa41f1c1` | 0 |
| coordinator/internal/middleware/login_jwt.go | 2265 | `922f98e20a8f7f4d48c7ca5f41637c38595e54327e53e062a8e68678caad5f49` | 0 |
| coordinator/internal/orm/batch.go | 19177 | `154036f1914b14f1bc7c619d197c209b9af539218c1617fcd0034cda9fa40373` | 0 |
| coordinator/internal/orm/bundle.go | 10079 | `968f08b85f1276ff13e90f8e75ea5da3648816d7002ba4acb02fd2914a154aaf` | 0 |
| coordinator/internal/orm/challenge.go | 1887 | `c804cbfca7814a3db17fdf428b7099675dd7c85a0157ca9bf9f35e565907290e` | 0 |
| coordinator/internal/orm/chunk.go | 17181 | `92b9d15bb20baf35af6f56aea111daf65eb2edc77a7ec69fd538eba98d994bdb` | 0 |
| coordinator/internal/orm/l2_block.go | 7644 | `bf6d7d1c1bcd6c986e32b7cb6e5cbbf3e70a976ae6c70b032bb5897108bf2a57` | 0 |
| coordinator/internal/orm/prover_block_list.go | 2518 | `680b8fc33e354a0ec3d10a5265aac7d3eacbe12fd2c55032a3a56fd29096f7f3` | 0 |
| coordinator/internal/orm/prover_task.go | 10622 | `2c59f612ed36f812a53618dac0e8654ebb250b8502a69e70e848bf0e4eeb49dc` | 0 |
| coordinator/internal/route/route.go | 1991 | `e1eb9aaf5301f70d10d326f8240648fbb49095fba4c25f3034068f413a1ef054` | 0 |
| coordinator/internal/types/auth.go | 4279 | `45593a8284650616059875aa9b31ee543bf3e95d5cfbee1f76451c4f5e6e4e69` | 0 |
| coordinator/internal/types/block.go | 193 | `48c747890d4e9a6dcd9d472f93e873febab32ed1471861ef12a36419e5aa0d2d` | 0 |
| coordinator/internal/types/get_task.go | 725 | `bffcb1a9eb0e68bb8dd9ffbf4aefd4d55673ec33b19d69117fc66f7f7b26883e` | 0 |
| coordinator/internal/types/metric.go | 369 | `6c56be5635ab52b7f7fa8cede171ee7cae259526360bdc709e52ae479a55d42c` | 0 |
| coordinator/internal/types/prover.go | 2278 | `60239e676cf30ca2d56df218d9069afd630f1d73d3e15711771dede370ead009` | 0 |
| coordinator/internal/types/submit_proof.go | 602 | `26595fa556e22a79141a016bdb51328f7d56714ff4bd7a0e39d04c4b4797b46b` | 0 |
| coordinator/internal/utils/codec_validium.go | 2508 | `4e0a56d6af9e3fa6cd40a921e13f8da9a7445dd6ef4f13f527a85b6e70a24edb` | 0 |
| coordinator/internal/utils/prover_name.go | 575 | `c7003a96e30dc1f83c1051eb38c67f3ab8b82c64cd4c6df2af61d268a8d78a12` | 0 |
| coordinator/internal/utils/version.go | 992 | `ef9cf581d44fa013268f08817caa4faa6d84dc53aee9fc073218835f6fef32a4` | 0 |
| crates/l2geth/Cargo.toml | 1033 | `4e81176ccf708e5bf5de4e4ccb0c77fba4d47f782013f648371945455f3389f0` | 0 |
| crates/l2geth/src/lib.rs | 551 | `91b730cc521bf8293d7d7b642184f283dfe55d9b66eff31f2d300988cd7021cb` | 0 |
| crates/l2geth/src/rpc_client.rs | 8784 | `b1e72a1cfd71bfd8c491a488e02dfb958f2fd2791a0051e8052683f907389704` | 0 |
| crates/libzkp/Cargo.toml | 1024 | `f8ef67039067d615caec5bdbc9e288258185f71370848dc02bb3659522f0591a` | 0 |
| crates/libzkp/src/lib.rs | 8329 | `f001ec684cb816ffeb9270ebf058aa834598bd78d6e14f2dd78eaea90aa5c3fb` | 0 |
| crates/libzkp/src/proofs.rs | 11108 | `22cef48ed3e7b3dbf4e9e4002085a859c3e1814aca7f8d72cd61fd6941371bde` | 0 |
| crates/libzkp/src/tasks.rs | 2737 | `ba4ac32fa9d4a011e1bc226bb8fcafdc8277a1cf84b10c1ed753c9bae218b8d6` | 0 |
| crates/libzkp/src/tasks/batch.rs | 14493 | `4ab53753c791a6a70d607ac86abb07b82d58996425d4fccda9cf0e69c1c0177d` | 0 |
| crates/libzkp/src/tasks/batch/utils.rs | 2791 | `586e0f7ef7d919d9839bb4bf363a5d258d9160d4714484a256fde64d489eec28` | 0 |
| crates/libzkp/src/tasks/bundle.rs | 3225 | `b0d80c6862f6b8bec236afffe1cd11b2e2e192c642d65826aa565ead6be4a652` | 0 |
| crates/libzkp/src/tasks/chunk.rs | 8334 | `4e36824012d46d19fef2afddb024cd75d41892323f2cc1bf35bf04a2149888ef` | 0 |
| crates/libzkp/src/tasks/chunk_interpreter.rs | 1035 | `897a8681e18706869cb7db8b56ca73059966538733406259948657cd1fa0d4d2` | 0 |
| crates/libzkp/src/utils.rs | 1717 | `49175f6a0562d93fccd83436470a32d16cd4cdc15a9223537c7db0769430cdd0` | 0 |
| crates/libzkp/src/verifier.rs | 2656 | `b274fedd3ad57bf0f7c15700415a3166768c7ffe2ed6a200a53161724620574d` | 0 |
| crates/libzkp/src/verifier/universal.rs | 3189 | `30f2f35e49fffe20d1e5eafc33fdbf4103a08664084cc4c0d135f5975f94ac55` | 0 |
| crates/libzkp_c/Cargo.toml | 391 | `eeba46d38a48d9e75b9867de29a4a6d5fff751f7cc95482457c08570bb63802f` | 0 |
| crates/libzkp_c/src/lib.rs | 8056 | `db7f054b496c45cd459a23954c45343c07eadbcd823a041b51d310b535b8f371` | 0 |
| crates/libzkp_c/src/utils.rs | 314 | `99f7f4db572ff4e42fa21e5fac43919e9379d7273b41af842e41ce6c3c31d068` | 0 |
| crates/prover-bin/Cargo.toml | 1796 | `304147a38f56cf4c52e55b7964ed292b94e8861aa6f556507734639e43938c00` | 0 |
| crates/prover-bin/src/deferral.rs | 4274 | `f76c8aabc380d0912f2bbe14d6578154ebc9076e393f0384bbfd6bebe0ba15ff` | 0 |
| crates/prover-bin/src/dumper.rs | 2816 | `135b858ea6ca616458eecc03728b445b8c8d6631ae19e6e799956a95f1969709` | 0 |
| crates/prover-bin/src/main.rs | 4735 | `a48fd9df899d98c6f537f12deeb6d845c888098ca6481b142d10792a14ff7218` | 0 |
| crates/prover-bin/src/prover.rs | 19934 | `806101996a2b1c3b54d5af3af401861653eea686f21b40843a67758c1c044e01` | 0 |
| crates/prover-bin/src/types.rs | 2292 | `eb924bd75fe68dff788b598fda2e9c2682a465e0257e542c149d6fb8c684bdf1` | 0 |
| crates/prover-bin/src/zk_circuits_handler.rs | 63 | `d8149a08fbf6293bf47e563930c310acf91517261aee1f5b7fb045d903809399` | 0 |
| crates/prover-bin/src/zk_circuits_handler/universal.rs | 4774 | `d306308a66b19e1cb37700cdc01534b16ebeb6539c0a802d37931641f2a6539d` | 0 |
| database/cmd/app/app.go | 1691 | `87f8cb8c8357791c3397747fffac015092d81caedef57c0af41499be91a40cb1` | 0 |
| database/cmd/app/client.go | 2078 | `c81824348ccdd096303fc1aba678565152e569e24df1657e3c48a1797ebba192` | 0 |
| database/cmd/main.go | 85 | `5a9652c7be8f3127fc57941573577b919f40bf82bd852835e3b80c9867152e26` | 0 |
| database/config.go | 1111 | `ba319606f816bd5340d08d98df856c10664a4cc1d8f92d578925371456336563` | 0 |
| database/go.mod | 1758 | `1dc8194628b1ad67a51934da47f8ea6d9722963c8c1b4410655a99b430ff0777` | 0 |
| database/migrate/migrate.go | 2497 | `88ccf8c5d37aed04cab47579eaf69b4f66f268ca36f7bb06741c7149c78a814d` | 0 |
| database/orm_factory.go | 1466 | `acda5958214fd43fb5d1aa42668485e6dfdf3da51c0053341e419c86a91a9003` | 0 |
| rollup/abi/bridge_abi.go | 16668 | `55c5e2954f7896d040a5b5357320f060e6307ebb8a81fd2b16ee3214e5da0493` | 0 |
| rollup/abi/validium_abi.go | 9793 | `10ba7f1ca8e36b59b07b98027f676e65e99875384351a6c54dcf125a96483594` | 0 |
| rollup/cmd/blob_uploader/app/app.go | 2347 | `5a9793733184f8891c6b4747aa56e04c7722f2638ea23c959fbbcf6715bbd83c` | 0 |
| rollup/cmd/blob_uploader/main.go | 92 | `5fdc02b2b6dc5295c295dfb42131dbe000a8f70a64ddeebd7f6ff4425e72362b` | 0 |
| rollup/cmd/gas_oracle/app/app.go | 3947 | `2726845ae1315012855e709d89dd43edb83a64a7f5b8c7e8def3ed87254d990e` | 0 |
| rollup/cmd/gas_oracle/main.go | 89 | `e4067c59a4f2d554c277f53de08eef2e5689f9cdeb7fcf3ddcc032988d1ecac9` | 0 |
| rollup/cmd/mock_app.go | 2889 | `038088b966b5f53ee480a2cd68753b2abaafd38658b5f4a944b3949c45def39e` | 0 |
| rollup/cmd/permissionless_batches/app/app.go | 4738 | `9ce3bb394fd8e7131af38534dd9c1796731f7c95244a7f2f7cc1ca120f2fe46a` | 0 |
| rollup/cmd/permissionless_batches/main.go | 101 | `4c7ebea913962a406de09666cbb7d9e7835235a829d4c666cf6f2ce2ebe02c48` | 0 |
| rollup/cmd/proposer_tool/app/app.go | 2730 | `45e16e98396404779cccd5344dcefe24c768db42c752a53c3e29552d71319956` | 0 |
| rollup/cmd/proposer_tool/main.go | 92 | `ec4b48bd88e20649046a56204474dcbc1f68159a793a5d4fc19946a42cd94cd2` | 0 |
| rollup/cmd/rollup_relayer/app/app.go | 7071 | `ae26730abc7f34dbd99fdc3b40f9e7d74269a3af8376601139249bf53b10462b` | 0 |
| rollup/cmd/rollup_relayer/main.go | 93 | `5a38c69fd06dd348ec6527004e3bebfa86dfdf9171770c51d91d582ed635e228` | 0 |
| rollup/go.mod | 7282 | `c89c1cedbc2b4c0ed0c79ed551fefe446eddedb8431cecc25795bb815c68b433` | 0 |
| rollup/internal/config/config.go | 2585 | `183d3629830809f046a456ed1df6d660d22e217aa5b9524cf3130b4b299fb860` | 0 |
| rollup/internal/config/l1.go | 387 | `dab812d35e87322bc1d94cbb557e6441e4ef0082c4596577bce54958a3f1e479` | 0 |
| rollup/internal/config/l2.go | 2545 | `07ff3aef2ffc6c7937e6c728387819c7b68ac9cab45c969b2d8f4e313f0288da` | 0 |
| rollup/internal/config/recovery.go | 911 | `277657568839792bea3632585aa4978d2b5a1e5c5ab3e28a90ec0d81746e3b1a` | 0 |
| rollup/internal/config/relayer.go | 8152 | `9a139ea808a9cf83f6a5ac9088b63f8175868db8e92836497aba59054828f912` | 0 |
| rollup/internal/controller/blob_uploader/arweave_sender.go | 22 | `3ba036c5847f0a8a9d4cf83ac35a84f3becdc77ca3225566cc9ac564a754de62` | 0 |
| rollup/internal/controller/blob_uploader/blob_uploader.go | 9194 | `0e13962a2f5f0577a1c88f4447d8a87d6254f569396e0c602e1bdfaf4b29355d` | 0 |
| rollup/internal/controller/blob_uploader/blob_uploader_metrics.go | 1083 | `86aca4bc7a5cca20ca4b77b34f17ca78daf2216bf245ea74a122b0cbdf54b18e` | 0 |
| rollup/internal/controller/blob_uploader/s3_sender.go | 1682 | `e315c3cfb2bab966c92ea470f1a8e6e8fb3e6e389b95b71334b274913a0b9255` | 0 |
| rollup/internal/controller/permissionless_batches/minimal_recovery.go | 19710 | `e8fd1547d06d308592bccf84efa2b30b7c2889d91a95ad05a700224b15f002a1` | 0 |
| rollup/internal/controller/permissionless_batches/submitter.go | 10220 | `3dfc555fdddab287e52b80dc5aef77d8df9db135d0cac7aabb11e0a7a272ea31` | 0 |
| rollup/internal/controller/relayer/common.go | 646 | `61438d128d299b11eff636405ed344206b1a790622f0bbc14b76b2f77387672b` | 0 |
| rollup/internal/controller/relayer/full_recovery.go | 19220 | `b3ca5fa7925e6c52117c2ae128a7bd48300096cd91e17b155ed4aa68ff85488e` | 0 |
| rollup/internal/controller/relayer/l1_relayer.go | 11923 | `8af454ca71f7cc878ccc733f560ad30464c0c8f45a2baaa40680256d84453d29` | 0 |
| rollup/internal/controller/relayer/l1_relayer_metrics.go | 2230 | `6dc051a8eab490707267fc8adc93ac3b8f57062311556d6653cabb64610ac229` | 0 |
| rollup/internal/controller/relayer/l2_relayer.go | 52074 | `f1dba01e1e22c089b7a7c940555f209bcc58f9ff6900e55417a03ef43dcd43f0` | 0 |
| rollup/internal/controller/relayer/l2_relayer_metrics.go | 7381 | `8ff9142247cbc84def013352bf3c343034d979a0640d64e6fff2848904c81551` | 0 |
| rollup/internal/controller/relayer/l2_relayer_sanity.go | 19842 | `72e51f01dbf1c28ffe0f4172342efe2c850c4c33cfe9ff4f69ab0efbb6225972` | 0 |
| rollup/internal/controller/sender/estimategas.go | 7148 | `e48316016cc354544609a1f9b38679ea6fa04111ed805a56bad06bce7dd4e1af` | 0 |
| rollup/internal/controller/sender/kms_signer.go | 8580 | `5ea4720bbc6ef9586cae9c8b352bb1408685aea27b8909d3d085b21279c017e5` | 0 |
| rollup/internal/controller/sender/sender.go | 37135 | `bc4c800297129466f74eca5076da4e0e63db99f23c934d69ef8b5955413347a1` | 0 |
| rollup/internal/controller/sender/sender_metrics.go | 3601 | `0d3deef02f9c6dae077ff24d08f35b85e993e0feb024d0e906e5f51ef73d4a68` | 0 |
| rollup/internal/controller/sender/transaction_signer.go | 5605 | `9173fafba9fa9e1804004f47030047becd75e9f05d30103a88c2625f4acb1a5c` | 0 |
| rollup/internal/controller/watcher/batch_proposer.go | 16027 | `841ef16ea6879057dc01df7b5b6694618bd4645eeacfa707a6b4722b59c42822` | 0 |
| rollup/internal/controller/watcher/bundle_proposer.go | 9876 | `006b33aa94bbb6c68c19f158d66095db8bddc74fced53cc39e0404b242385e53` | 0 |
| rollup/internal/controller/watcher/chunk_proposer.go | 14956 | `148bb9c10787ca93b272d648be857e439216acd0558c79fda9def8612d4984a1` | 0 |
| rollup/internal/controller/watcher/common.go | 52 | `3931c5819a846d4bcd0a021d0eaf723ff7fda3c4189153fff29fe02297a73921` | 0 |
| rollup/internal/controller/watcher/l1_watcher.go | 4269 | `24032f11ae481d5a846a5ba7ce9ae0ceb26c39d3f57168a5e23f5ebe0d39c5e6` | 0 |
| rollup/internal/controller/watcher/l1_watcher_metrics.go | 1063 | `f80fa57dcadd65d34bcc52f6265fce63d4ac2dcfef6933dd19d017f5989375d1` | 0 |
| rollup/internal/controller/watcher/l2_watcher.go | 5743 | `f6b909e5e2f6513cddcb6f2a5db3c182ddd71f5d1b0496b079fd907831bda85c` | 0 |
| rollup/internal/controller/watcher/l2_watcher_metrics.go | 1508 | `3ddd3906a212158321662c42b8c2cd2c8d4c0b2eef7b61b397d95f5c432b45cc` | 0 |
| rollup/internal/controller/watcher/proposer_tool.go | 5275 | `2c5960337527c5cc111889fb2d37d8c19743dba9d48c33282986f4db0fe7cd3a` | 0 |
| rollup/internal/orm/batch.go | 23309 | `0b291b61be652b9f18f4997abd1879462ce9ffdb00363764c6839c94dfc3f91f` | 0 |
| rollup/internal/orm/blob_upload.go | 4084 | `eadef40d02c0eef6f5e97a216a3caac90377b53c9ad4f03a6e79e57ab4e0b9d3` | 0 |
| rollup/internal/orm/bundle.go | 9840 | `e1eb236d47d441eb1f881dc30fb9ea2eef1e6f84c3762d05e49b653039299ed1` | 0 |
| rollup/internal/orm/chunk.go | 17666 | `242185884ef602f3a864434f702aaf54e27e6ff9faf0aa23943893c16acf41e7` | 0 |
| rollup/internal/orm/l1_block.go | 4501 | `082b46289374aebb4c57346a238e0f4fa8389de2cfd8a456f566943510d11f49` | 0 |
| rollup/internal/orm/l2_block.go | 8718 | `d9c4a93be4bcacf5b82cfc2422b26f15181efb5a79df41627f31907579fcd13b` | 0 |
| rollup/internal/orm/pending_transaction.go | 10339 | `f19de05369e4d75fb509e978980dc94f2f3f8c1f0394c5b1614cb2c2810dc9dd` | 0 |
| rollup/internal/utils/confirmation.go | 1527 | `b1800d24c3c7e7e9af0d061e02518f06c52e06adec4a3933d89fdfd000670dfc` | 0 |
| rollup/internal/utils/exchange_rate.go | 1630 | `c36b1a84247b622e38a7ece3ff9607ba19ccf716742752c771783ae92baad2e2` | 0 |
| rollup/internal/utils/utils.go | 9536 | `dfdcb44572071a90676254f4f422a35837381f8fae3e2e3db2c8877244eb1ed6` | 0 |
| rust-toolchain | 151 | `bf2f28108d500ed456d904590f731a4efebabd426ddfaf6d6279d25b33f9a1d2` | 0 |
| scroll-contracts/.eslintrc.js | 444 | `3812d4e7393c65ce9e58f89764654da11767dafd3574aa18caf94625f13e0e5f` | 0 |
| scroll-contracts/.solcover.js | 247 | `d68a2be7dfa3f14685b3027f7e4e132b290f444f126e2db18b537d6ce98238f1` | 0 |
| scroll-contracts/circomlib.d.ts | 143 | `f23d42634ad05626bcce72cd3273b49e725d802055f47455eb403594d747d534` | 0 |
| scroll-contracts/hardhat.config.ts | 3139 | `064d4446632cb5db673bafda3f48b7bfac8bde60b9693a2675b615be61e6946c` | 0 |
| scroll-contracts/lib/solmate/package-lock.json | 5069 | `570062e883c42cb00737a891f7d60268e2afb0be05d63d26331c276b4fe99e9d` | 0 |
| scroll-contracts/lib/solmate/package.json | 486 | `6036c21e67a74502cbb47ec24d91141fa256caf2de46f67cf1d210dcc5165fdc` | 0 |
| scroll-contracts/lib/solmate/src/auth/Auth.sol | 2577 | `8689fc68a85e5942f8b814efc14cee691fff188594bd7dcefc969ccc65bd115a` | 0 |
| scroll-contracts/lib/solmate/src/auth/Owned.sol | 1476 | `8ac2f2dc41ab8012e93adb3791326ffa1e4059a20c306a777109dd81816b9125` | 0 |
| scroll-contracts/lib/solmate/src/auth/authorities/MultiRolesAuthority.sol | 4789 | `5ab0b9540f4bafa542ecf11251ba988e07896b4e572d2c82f5f56edd82e743ef` | 0 |
| scroll-contracts/lib/solmate/src/auth/authorities/RolesAuthority.sol | 3950 | `51040c1f37851e8fdf1bc900f50231783bd485b00a9658420c55e75b0f0cfd9b` | 0 |
| scroll-contracts/lib/solmate/src/tokens/ERC1155.sol | 8196 | `3dbbc6faef59c3ee32b1c202510fab2ac6084faf19c164e0d85a392be1fd52ae` | 0 |
| scroll-contracts/lib/solmate/src/tokens/ERC20.sol | 6812 | `a3a7e839f42762ef24623581542a916e838f3c7c0bef647963d1fdad0f9d208a` | 0 |
| scroll-contracts/lib/solmate/src/tokens/ERC4626.sol | 6519 | `f7febaa5999e4b4255e5c4fb3f898428fe74a7b153110064f44d973e85479276` | 0 |
| scroll-contracts/lib/solmate/src/tokens/ERC6909.sol | 3836 | `efe0bdc5ef262bb17ed8b72d455bd46449cb5bdeb05b1e681c4da93cf7f48d58` | 0 |
| scroll-contracts/lib/solmate/src/tokens/ERC721.sol | 7365 | `2da0cca384448208e25d43eeb5953a237de0e6712942a07d0f2674e895b0d3d3` | 0 |
| scroll-contracts/lib/solmate/src/tokens/WETH.sol | 1025 | `22277963408ee27ddbc769fa27b5a09031b0f699e6b24d36f55435c6a2039ac1` | 0 |
| scroll-contracts/lib/solmate/src/utils/Bytes32AddressLib.sol | 560 | `a98260423087aa794384b5afa952c0b4beed4be080e355ac8995224d852e2851` | 0 |
| scroll-contracts/lib/solmate/src/utils/CREATE3.sol | 4319 | `0eff8e4b9ef607a8d82422fe9796517782e2b1b98ff9ad4386e899e0af363685` | 0 |
| scroll-contracts/lib/solmate/src/utils/FixedPointMathLib.sol | 10054 | `edfd7fa8ec4087d252f637df16669599d5c0ac803ab465730f8cc3a5e8a8d55a` | 0 |
| scroll-contracts/lib/solmate/src/utils/LibString.sol | 3330 | `8fabed55720de277dfd74fd6f11a78cb97f59bf571d53b0ae987734a0e5e5209` | 0 |
| scroll-contracts/lib/solmate/src/utils/MerkleProofLib.sol | 2032 | `59581539c278fd2a3e8e69e9a3994bc5f487ee35d6ebf2f09b9a0040cdd103b5` | 0 |
| scroll-contracts/lib/solmate/src/utils/ReentrancyGuard.sol | 602 | `e69ce8729cd5ff2caac16efa4498e967fc6bf85bbad4003be87c8a0757fd8a0c` | 0 |
| scroll-contracts/lib/solmate/src/utils/SSTORE2.sol | 5457 | `2819718fe1f9557c54562f9012b958de6851c37d1f0f66a97888d851a4bef74f` | 0 |
| scroll-contracts/lib/solmate/src/utils/SafeCastLib.sol | 4605 | `818c6ab372ca3b5881054c8cc9a3aae3dbf6cabd8b565bdbea3ff0cc4c21eb98` | 0 |
| scroll-contracts/lib/solmate/src/utils/SafeTransferLib.sol | 6337 | `ed12cae0865a8a92adb9dadd125b2cf23920870845ef128431d811963b474103` | 0 |
| scroll-contracts/lib/solmate/src/utils/SignedWadMath.sol | 10426 | `f606afc7c279737a02ebbaaec3025f16b971db0afef6bef4e21bb1ae5dfc74f6` | 0 |
| scroll-contracts/package.json | 2384 | `3de14357bc669b259f086c0c704ef8aa5b532f3fa750534ca7b5e1a0e7a928ae` | 0 |
| scroll-contracts/scripts/foundry/DeployFallbackContracts.s.sol | 963 | `f7a3d34806bcf814180ee505b4a010d7693086a36d7af9917a07b03f4987be77` | 0 |
| scroll-contracts/scripts/foundry/DeployL1BridgeContracts.s.sol | 9409 | `69237afe09d8cd9e4ba039ac26fe69defb8e03057a6fcb9841d4600d8ff86d96` | 0 |
| scroll-contracts/scripts/foundry/DeployL1BridgeProxyPlaceholder.s.sol | 4453 | `73a1b849fcbdbdc06a3aca457d1edbd5ae1e979ad37b7d4ba1f7b5e166c3f575` | 0 |
| scroll-contracts/scripts/foundry/DeployL1ScrollOwner.s.sol | 2369 | `e28c38dc6bf7711127ee321c3e13b2546bbe3f67d6c6589bc2f5ac73d487ebdb` | 0 |
| scroll-contracts/scripts/foundry/DeployL2BridgeContracts.s.sol | 8892 | `90eb25b767744237eccc4405d6d8301b9da00b082260914929a2427b81c5aa94` | 0 |
| scroll-contracts/scripts/foundry/DeployL2BridgeProxyPlaceholder.s.sol | 3815 | `a971f7b1ea4bec0c7efb489a10fae69c7ff9113c32fba289e8baebd7bdd3c1c9` | 0 |
| scroll-contracts/scripts/foundry/DeployL2ScrollOwner.s.sol | 2369 | `0ff25c7be61a70f09066b0f90abfa83674ec3253eee73ccd1fe7a4e048475c3e` | 0 |
| scroll-contracts/scripts/foundry/DeployLidoGateway.s.sol | 2534 | `4d060d089f1a7604f3331484e9c05a886fe5718f72f872f76cacee5111418891` | 0 |
| scroll-contracts/scripts/foundry/DeployScrollChainCommitmentVerifier.s.sol | 1204 | `e0ec5350756a3dc7ff85f4ee7570fa1f4f2f26655b625b3dc1f63e3faee6e075` | 0 |
| scroll-contracts/scripts/foundry/DeployWeth.s.sol | 1085 | `dbb15e8a9605f7f09d082717dc2d0a9981bf96d278ebe80be434392f2457d8ce` | 0 |
| scroll-contracts/scripts/foundry/InitializeL1BridgeContracts.s.sol | 10930 | `5c64afa9bedb004840a61ad6fe6f86dec8bdcbe0dc1a765e1535a6537f259619` | 0 |
| scroll-contracts/scripts/foundry/InitializeL1ScrollOwner.s.sol | 13562 | `5c5c9d91c1252858a90866dada17083e15753e4d6a3d2bf1c1f6c6deb90774f7` | 0 |
| scroll-contracts/scripts/foundry/InitializeL2BridgeContracts.s.sol | 8620 | `ab9cb3598e9863cecc1831486c3ab3b90bb091b58b6f77d4be7fbd2721d031f3` | 0 |
| scroll-contracts/scripts/foundry/InitializeL2ScrollOwner.s.sol | 11132 | `6bbf11d1c727b199f8da83e83481101b7da9dfcbcef6dd081cd7ae987f87e9a6` | 0 |
| scroll-contracts/scripts/hardhat/ScrollChainCommitmentVerifier.deploy.ts | 1678 | `71b9b6514f6e5132024cc0d30aa01b105ce13a2359092ba171ca55d78ac4ec22` | 0 |
| scroll-contracts/scripts/poseidon.ts | 5135 | `7a12384d8c387d0c3fdfc61083e4830823c9a96681c5bb5c465fb726aaca4329` | 0 |
| scroll-contracts/src/External.sol | 443 | `7d713b80972b03f30a4e7e215c8c1173e78ee4c62cd5d1ab88d4192424d36696` | 0 |
| scroll-contracts/src/L1/IL1ScrollMessenger.sol | 2895 | `b53351a515ea15f5b9b5c7c7326447d67d764f066acbf17504d591bb1f8deb43` | 0 |
| scroll-contracts/src/L1/L1ScrollMessenger.sol | 15402 | `d5f24ac5e19fd3a7cf15f0de727025c7b949cdb796253a355e16bf9e4d57cea3` | 0 |
| scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol | 7737 | `c1acce6f43b20fe2680bf2323cdcc6e8e5b3914fbf96902836b623697a008f26` | 0 |
| scroll-contracts/src/L1/gateways/IL1ERC1155Gateway.sol | 7950 | `dc47b9986026a9f5ce1aeeb1b0d23c9be1b4bf67e4b5014ff19eb2db410f24eb` | 0 |
| scroll-contracts/src/L1/gateways/IL1ERC20Gateway.sol | 4674 | `20a99fab221d229a722cfc482477f1bed85fc15a44018d20d8f83c696688dbeb` | 0 |
| scroll-contracts/src/L1/gateways/IL1ERC721Gateway.sol | 6828 | `c96a0655ea4372ba4f5904c5289580b0ec2aec122f698b985e5886d3dbde0a7d` | 0 |
| scroll-contracts/src/L1/gateways/IL1ETHGateway.sol | 3091 | `b12e4d951a528a5d4bb3e1d3b8e8dde1b48b6c58edaf0a8b0007db89832453c5` | 0 |
| scroll-contracts/src/L1/gateways/IL1GatewayRouter.sol | 3061 | `77c874526824735891f9bcfe73f89f0205bf972887416a22ba1833005849ed84` | 0 |
| scroll-contracts/src/L1/gateways/L1CustomERC20Gateway.sol | 5863 | `790ae9ca1880bd29a938cd998e47e75fab0ed76e307a2897b14ab647eac61d69` | 0 |
| scroll-contracts/src/L1/gateways/L1ERC1155Gateway.sol | 10577 | `2f18be697f5f023f79128c905140f65cedce690f9f7ba3122f18115beaeb655c` | 0 |
| scroll-contracts/src/L1/gateways/L1ERC20Gateway.sol | 6737 | `5f1a6cfd4d6e69ce5349515d90a1a692cbf9276b89bf7dc4e5d63a7ec9396a47` | 0 |
| scroll-contracts/src/L1/gateways/L1ERC721Gateway.sol | 9842 | `ca7f93e9364dbe8007387f505c085f79a0f3a2585bed22bce4292c8b6750babc` | 0 |
| scroll-contracts/src/L1/gateways/L1ETHGateway.sol | 5432 | `b57ceeba44905028ed7e1538984591049e7fd9183e814f68e86b65405a17010a` | 0 |
| scroll-contracts/src/L1/gateways/L1GatewayRouter.sol | 8523 | `49332de77c5b4ce2b6cd58c704aabc66d1d11fc07a06cfc4d1861e7f03c644c7` | 0 |
| scroll-contracts/src/L1/gateways/L1ReverseCustomERC20Gateway.sol | 2767 | `4206823f24deac26fc1efef11fc27dcecc57ab3946c2ddd98b30c9eccfaba5e9` | 0 |
| scroll-contracts/src/L1/gateways/L1StandardERC20Gateway.sol | 7414 | `8032acfe9c50e3c1ac12c012cac14854b45e938521345a24c299af89f1f4b35c` | 0 |
| scroll-contracts/src/L1/gateways/L1WETHGateway.sol | 5017 | `807fc830883b17bada1882d9849f93d53fec7801e169413fd53b1b17e4eddbb7` | 0 |
| scroll-contracts/src/L1/gateways/usdc/L1USDCGateway.sol | 6739 | `ef0b48329c4f4a5ea86a280c086c3ab4810d2f8eb30015720faffb9d3878f3ae` | 0 |
| scroll-contracts/src/L1/gateways/usdc/draft-L1USDCGatewayCCTP.sol | 7059 | `a8133b9fb10040e12c57b25bd87eef2ca670512ecbdbafec8eacbba9f0b07a77` | 0 |
| scroll-contracts/src/L1/rollup/IL1MessageQueue.sol | 7054 | `bb0d956a465c90d9ab2750dcb00c57d2b645da4a0761ddaee86b6cc15809bc87` | 0 |
| scroll-contracts/src/L1/rollup/IL1MessageQueueWithGasPriceOracle.sol | 1326 | `2f03488822031773e35c82575cf44fc371d4caf41823533af404ef82c7be811d` | 0 |
| scroll-contracts/src/L1/rollup/IL2GasPriceOracle.sol | 780 | `5a5f0c3eaf6afc3b1cb654cd932e2e9633072fa138d4d78cdf894d3d14267e4c` | 0 |
| scroll-contracts/src/L1/rollup/IScrollChain.sol | 5084 | `5eee413d6aa9636329d544c274e902cbd3406f4f7e2efc61fd3f317c5ec43329` | 0 |
| scroll-contracts/src/L1/rollup/L1MessageQueue.sol | 18449 | `d5a27387feeacc678ef0a00d47b556d7b287cfd9bcd475b4f92ecde85e353001` | 0 |
| scroll-contracts/src/L1/rollup/L1MessageQueueWithGasPriceOracle.sol | 3864 | `0745ebc47c657d4a45747aacc1cc052f74b4e48df23ce483e0c6962c8ef43638` | 0 |
| scroll-contracts/src/L1/rollup/L2GasPriceOracle.sol | 6389 | `5c5cb9f805d43dbe2df76ae8be39f3f35dbfb19cb0e88ea43a3d0b15b5712939` | 0 |
| scroll-contracts/src/L1/rollup/MultipleVersionRollupVerifier.sol | 6479 | `d8348e2de11c6c0ce3023fec6e5f3abf003bff14018e7b9cd4684e603ac6a7b8` | 0 |
| scroll-contracts/src/L1/rollup/ScrollChain.sol | 42282 | `122e007a87f4e5dec3439eaf7a64248dda0be3b6da9628f349508bb7c78c8732` | 0 |
| scroll-contracts/src/L1/rollup/ScrollChainCommitmentVerifier.sol | 2372 | `0dead420b12b8169fc72e8f7e3f497f8d44e2cbc0beaa06252bf2a1ae42194e1` | 0 |
| scroll-contracts/src/L2/IL2ScrollMessenger.sol | 1334 | `cad97fa468f6c2007ccc40764faea49b794b7be4495f8af807df17d7f23c1cba` | 0 |
| scroll-contracts/src/L2/L2ScrollMessenger.sol | 6367 | `4b07ab7176f12746d99eb0ad109743becfcf60061db7820464b8e300e707c3c2` | 0 |
| scroll-contracts/src/L2/gateways/IL2ERC1155Gateway.sol | 7034 | `6f037fc307244c37278645d603f3c2b3f5b877a066b99d9d4db25a07886f7844` | 0 |
| scroll-contracts/src/L2/gateways/IL2ERC20Gateway.sol | 4606 | `fe21359fc7bace1a3ec226319acf61b293e586fc2bd00fe94f6f789fba08f133` | 0 |
| scroll-contracts/src/L2/gateways/IL2ERC721Gateway.sol | 6099 | `8ad1d37bbc93b7f37c4dcb77b18f910bd4c4406c9aeec4206421e8e3dd19686b` | 0 |
| scroll-contracts/src/L2/gateways/IL2ETHGateway.sol | 2847 | `fc24e528359db2b94680d204b00b84ca245800056905f8bf4fb8b89b71577475` | 0 |
| scroll-contracts/src/L2/gateways/IL2GatewayRouter.sol | 2287 | `2e1da5192950049a7e5c4230fc3320adaff34f6a4a3081489fd5def6a178949f` | 0 |
| scroll-contracts/src/L2/gateways/L2CustomERC20Gateway.sol | 5984 | `1dec163dd0294485b2d43653628bb79a3ca4fab74cb8698a76bd3258b0cca942` | 0 |
| scroll-contracts/src/L2/gateways/L2ERC1155Gateway.sol | 9192 | `304a7b51c3fadfc12cc271ab7b555bd7a87a7b3e6a3848ee3a6a372734b2fe39` | 0 |
| scroll-contracts/src/L2/gateways/L2ERC20Gateway.sol | 1596 | `8a9c2d799f3a940eaca539a382814ef62a9cf0edf9d119886b6422b3d4dcfc84` | 0 |
| scroll-contracts/src/L2/gateways/L2ERC721Gateway.sol | 8760 | `f884fa9218630b2c3f55955522ed96c4af64d8859fd6a7418f0a73e09ee0c9d5` | 0 |
| scroll-contracts/src/L2/gateways/L2ETHGateway.sol | 4489 | `6aa1094c5c3893b02aa0497bf5b320fd1b9eadfb5c70cea625c2a49f0a235b41` | 0 |
| scroll-contracts/src/L2/gateways/L2GatewayRouter.sol | 6768 | `ce19c2c3f403776f8b0003838c66696e4a8e59642619e04107d337627d845828` | 0 |
| scroll-contracts/src/L2/gateways/L2ReverseCustomERC20Gateway.sol | 4532 | `7584a453ca37a412920e7238da003c0130a18555df8cdb7c6069fab313468aa9` | 0 |
| scroll-contracts/src/L2/gateways/L2StandardERC20Gateway.sol | 7085 | `fdc37478828c83dcfcb9ffd1034beee9807a1871293328540b3d055a7d4be58e` | 0 |
| scroll-contracts/src/L2/gateways/L2WETHGateway.sol | 5645 | `ffd5335a96f6f47149885de6962a9478dea7e550701691a24de93ca502ea872d` | 0 |
| scroll-contracts/src/L2/gateways/usdc/L2USDCGateway.sol | 7192 | `160bf80b861e8da3d357126020bf64418c601737a400c59f9c55c3548289e9cc` | 0 |
| scroll-contracts/src/L2/gateways/usdc/draft-L2USDCGatewayCCTP.sol | 6021 | `cfcd5df2ba819608ef653da7a77f12731764331fc198ae2b90f3f64d5b422aa6` | 0 |
| scroll-contracts/src/L2/predeploys/IL1BlockContainer.sol | 2260 | `6b9df42101c8b0996d97a42c921a220f52df46223fedeb0227179882282616b6` | 0 |
| scroll-contracts/src/L2/predeploys/IL1GasPriceOracle.sol | 3440 | `d3babbc8fd86d580420c0054f0413eb7c25d67059db83b17e3256703f4b2d180` | 0 |
| scroll-contracts/src/L2/predeploys/L1BlockContainer.sol | 11157 | `e72617f1c9fa18ffec37af20e83cdc060b7d8e3bab4e4ac9595dfaf0cda2d6bf` | 0 |
| scroll-contracts/src/L2/predeploys/L1GasPriceOracle.sol | 9265 | `a38d150cc80a57c9ab1bebbfdb2268ee5de4702b44745a7ff2423a63c4874bdd` | 0 |
| scroll-contracts/src/L2/predeploys/L2MessageQueue.sol | 2464 | `9427eee5a1f80eafa3ea480ae338ec4dde19665f15959864005a9ee947beae5a` | 0 |
| scroll-contracts/src/L2/predeploys/L2TxFeeVault.sol | 6250 | `2dee511dc410374f9c4dbdbcfef806e724187e72efe8b0d927504888db015731` | 0 |
| scroll-contracts/src/L2/predeploys/Whitelist.sol | 1315 | `63fb506aebf233982bb56598ffdf9e4b451d2419924de0e7ba272684c40d0eca` | 0 |
| scroll-contracts/src/L2/predeploys/WrappedEther.sol | 1459 | `60b7f0696cad7d9b4ce8eead8542a14d5991420c8407b2258c74f9c73981b8a3` | 0 |
| scroll-contracts/src/batch-bridge/BatchBridgeCodec.sol | 1202 | `4f7cbec0c5bd17c5e9d00782e56efd687f217de22a155ba25497b21329d72a55` | 0 |
| scroll-contracts/src/batch-bridge/L1BatchBridgeGateway.sol | 16981 | `4d7897aa5b7c97bd449d57afb995c015f33dd4a4114d7b9c20d761504a357971` | 0 |
| scroll-contracts/src/batch-bridge/L2BatchBridgeGateway.sol | 9393 | `7b712d191d55b763ede8f90aab8bac7e8afd501885c4ab569a962ee22c3910d8` | 0 |
| scroll-contracts/src/gas-swap/GasSwap.sol | 6839 | `1ebac760c5525385e113691f6af72b2b90a8577fb92cac270da3752833fb718f` | 0 |
| scroll-contracts/src/interfaces/IFiatToken.sol | 808 | `dea1c0051899b8fd440b38e0bde704580a7a9f088f96e342af524861a38e2c01` | 0 |
| scroll-contracts/src/interfaces/IMessageTransmitter.sol | 816 | `108406edde027d6ae5f5d42ed4daabae08ae6a6c96e7a551af66abcd4c577722` | 0 |
| scroll-contracts/src/interfaces/ITokenMessenger.sol | 3368 | `eb6c0661eb93f92eba4ce3141e6f0ebbe7256fb67ae124fb93e620b1b617a360` | 0 |
| scroll-contracts/src/interfaces/IUSDCBurnableSourceBridge.sol | 372 | `8646fad70708e7745d550daf1e4836cee758dc1e8f16c883acd0e8933ebc46ec` | 0 |
| scroll-contracts/src/interfaces/IUSDCDestinationBridge.sol | 377 | `1b703d9f11d9636e6ac009ebf527f9382d6cd520aea94b4482df448e9f95fd05` | 0 |
| scroll-contracts/src/interfaces/IWETH.sol | 166 | `8fcbdd93099cd4dc3300e1b5692a8f74768612e4d22a33a5b503faa5c600de39` | 0 |
| scroll-contracts/src/libraries/IScrollMessenger.sol | 2788 | `796f0691d9c3d2ff2aed6757bc785abd449afd2b797ece3e4e5e863e3468d7a5` | 0 |
| scroll-contracts/src/libraries/ScrollMessengerBase.sol | 5140 | `edefc59828cac7175bce345900ce14c5dbf4af642e5636e9122f2b4daf34498b` | 0 |
| scroll-contracts/src/libraries/callbacks/IERC677Receiver.sol | 208 | `2f7b39100d5cf514350f8bc4744fd0762ba11834f017d7f4d0562fec38215f59` | 0 |
| scroll-contracts/src/libraries/callbacks/IMessageDropCallback.sol | 161 | `8cd2da92f636bac9af66946f66ab8cc62d0b830725cec26d4f65734269718d4c` | 0 |
| scroll-contracts/src/libraries/callbacks/IScrollGatewayCallback.sol | 162 | `f5e6f03134708452dda6e304e8eb0d1a4fec1974ac601a647789e163cc7857f4` | 0 |
| scroll-contracts/src/libraries/codec/BatchHeaderV0Codec.sol | 9734 | `bbe3954cf2eec2f6b09edc6d656acd1dd6a1337bc300e27b7b40cc8b875dcbcb` | 0 |
| scroll-contracts/src/libraries/codec/BatchHeaderV1Codec.sol | 6107 | `179566ff8e4a63956e08726bdd592fdac0d887d30a9aa60ce072cf4c7951de73` | 0 |
| scroll-contracts/src/libraries/codec/BatchHeaderV3Codec.sol | 3836 | `9f57bcc41292fd1d457a54b0f1d23fb00a1c84c71a80b943780f1a05ab94fce1` | 0 |
| scroll-contracts/src/libraries/codec/ChunkCodecV0.sol | 5689 | `c1aa9e4bce73efa4e18d745bc597b0752f4fffac1d64299af200e75fa6abfcf1` | 0 |
| scroll-contracts/src/libraries/codec/ChunkCodecV1.sol | 4835 | `cb3adb282aeb5722e4eff17b115c2d7b224782dbb0bc4c08d4548bc1b71a8414` | 0 |
| scroll-contracts/src/libraries/common/AddressAliasHelper.sol | 1179 | `b3a48807eb0ec4bc36e21eaca7c6b1d83c927524092444ebd30e64456f5faac9` | 0 |
| scroll-contracts/src/libraries/common/AppendOnlyMerkleTree.sol | 2607 | `87cd0165e5fd06b382c0ed6b2120346fbda99f2a0ac517841949ea204cd49524` | 0 |
| scroll-contracts/src/libraries/common/IWhitelist.sol | 275 | `de9f5cba8f683994dd7974e70f25329feeda3cc89349c35751654f0b5fde9b40` | 0 |
| scroll-contracts/src/libraries/common/OwnableBase.sol | 2047 | `c1ff538a054ce49c22b3a755ceed226eb06c5aed4138e9b5fa1b79cfa9024489` | 0 |
| scroll-contracts/src/libraries/constants/ScrollConstants.sol | 434 | `2bb10023011def574565fe295cbd2fbd10ee07bd16aa4dfff132c6b36f9e6a25` | 0 |
| scroll-contracts/src/libraries/constants/ScrollPredeploy.sol | 373 | `66a6be0122108fea3c1de5442986741d58e50c820b68875011aec65a71897510` | 0 |
| scroll-contracts/src/libraries/gateway/CCTPGatewayBase.sol | 3137 | `bf0f6f6b2b302bfa38acbbb79215c1d2b7d56fb705f586a7a0e7d66575c212b0` | 0 |
| scroll-contracts/src/libraries/gateway/IScrollGateway.sol | 1120 | `bcbaca0e9a80c386a3c326d1b8c9aa4fb1b5c00b123e715e0ab560a5a0d549f4` | 0 |
| scroll-contracts/src/libraries/gateway/ScrollGatewayBase.sol | 3799 | `a6f02734f939a5976a26f0bf9f5725b6cdb204ec9b988e3e02d4b6263ad6beba` | 0 |
| scroll-contracts/src/libraries/token/IScrollERC1155.sol | 429 | `e6d18eed0c2654418678d9aa2f193706b93132e1812e44ce5233ef22a6905710` | 0 |
| scroll-contracts/src/libraries/token/IScrollERC1155Extension.sol | 2201 | `2d471c9da443b3cc4ab297f36754a07e501001e7b81859c9b1e4495d59a1e915` | 0 |
| scroll-contracts/src/libraries/token/IScrollERC20.sol | 525 | `bd26aa6842d1cbb44f822ebae06e2bbaf5241af65e5dc7209aaee816a4dd2524` | 0 |
| scroll-contracts/src/libraries/token/IScrollERC20Extension.sol | 1330 | `ba1beca4af7a80ffcd8841236f748298ca2e7de63ec7a88496637b247b989c38` | 0 |
| scroll-contracts/src/libraries/token/IScrollERC20Upgradeable.sol | 1683 | `877c660a086dc2c7f1437a500070b001650faa4eb10cf6fb018fc98017ab7b9e` | 0 |
| scroll-contracts/src/libraries/token/IScrollERC721.sol | 420 | `7c8d28b081d038ebb5c5e642981aae64608f113fa83a754624ad816ed2c23eaf` | 0 |
| scroll-contracts/src/libraries/token/IScrollERC721Extension.sol | 898 | `e129af1d73c0ba16644c958854755c4725a5b4b81356f77f1d510b88bb73808d` | 0 |
| scroll-contracts/src/libraries/token/IScrollStandardERC20Factory.sol | 909 | `0d1f239a646b5cbdc561692bc86bad2ff10d38c70124bc70fd1d772833db4bf9` | 0 |
| scroll-contracts/src/libraries/token/ScrollStandardERC20.sol | 3094 | `072e35266cf6643911e21a1826b5d8063e1dcced80f5d38a6c35c745b83acacc` | 0 |
| scroll-contracts/src/libraries/token/ScrollStandardERC20Factory.sol | 2063 | `56ea99d71ab47b482b4d7518b6e57cdd7de61fba03997e8a8b6f85e1a6b1feec` | 0 |
| scroll-contracts/src/libraries/verifier/IRollupVerifier.sol | 1372 | `cc41a4f7f1558fe9127a508301d02ee0877e9b1bfc40ac11b6b014f7e37f9445` | 0 |
| scroll-contracts/src/libraries/verifier/IZkEvmVerifier.sol | 583 | `3256c6cf80afd3e502948e6441bd30e65e71a618d1de0c4314cddab236eab519` | 0 |
| scroll-contracts/src/libraries/verifier/PatriciaMerkleTrieVerifier.sol | 21206 | `1015675bf201501d99514128a400099d09c54aa6d6b423740bd0ed990fd943b5` | 0 |
| scroll-contracts/src/libraries/verifier/RollupVerifier.sol | 40670 | `69d78c950cc41490bb239404f6be572786450b6038493e2b44d182b6b7b5a50f` | 0 |
| scroll-contracts/src/libraries/verifier/WithdrawTrieVerifier.sol | 2012 | `e27826f4a1f3ce9ba73cbde12a3d729b56d5c98c17bcfea7559d09f146bfce21` | 0 |
| scroll-contracts/src/libraries/verifier/ZkEvmVerifierPostEuclid.sol | 3875 | `2c07ffbfc801faa1a0474539fdad77dc5e7420ec734747e3c51e537a19968626` | 0 |
| scroll-contracts/src/libraries/verifier/ZkEvmVerifierV1.sol | 1991 | `46bf8a4f752f8a47a5ad9e1a3eec23d1f05c0537d635e1bb435eed995ce27d14` | 0 |
| scroll-contracts/src/libraries/verifier/ZkEvmVerifierV2.sol | 5204 | `a67bfc111fadfb53876c4f8ac04e52075e59de34a661c2333ab39d0b5c386115` | 0 |
| scroll-contracts/src/libraries/verifier/ZkTrieVerifier.sol | 12926 | `f6ed6a2157117f57ded4962f31c268d2454b7d44ca59b195bafa49fba8fb1735` | 0 |
| scroll-contracts/src/lido/L1LidoGateway.sol | 5592 | `cb1b87e72895b8533cbf9363ebc39e4aadfc88c7afdf465a7d66855e10e64a87` | 0 |
| scroll-contracts/src/lido/L2LidoGateway.sol | 6287 | `82f0a9e7851d6ba5dfa124f195f12a241f154059a175fe1673e08ce2c805a72a` | 0 |
| scroll-contracts/src/lido/L2WstETHToken.sol | 1841 | `151736579a11060d5b8b1f55b0e8c410e339a19a32b1e6aa92ea2d2b2cdaa15c` | 0 |
| scroll-contracts/src/lido/LidoBridgeableTokens.sol | 1930 | `22a74aaa2ab33352b2de053e5689bab30247c4d4063f9317d8eddb189c6c1184` | 0 |
| scroll-contracts/src/lido/LidoGatewayManager.sol | 10615 | `1a718a7450f3193a3d18f1c35efb17cad613f108dc8f4b12fd0b0e83138f8177` | 0 |
| scroll-contracts/src/misc/ERC2771Forwarder.sol | 17287 | `bbab6b1135ed8a1f07ae403a0f062a57c2e61286ec5ef720f04ec61a6b752148` | 0 |
| scroll-contracts/src/misc/EmptyContract.sol | 122 | `f29f74786c177430af5a2591f8f05806900bb90bd5a622d4c6ca8aef797f4563` | 0 |
| scroll-contracts/src/misc/Fallback.sol | 1352 | `a0fc79f1b508550e0e82269c406554b4a476d13b0f416ece53ececdf419a0a52` | 0 |
| scroll-contracts/src/misc/Nonces.sol | 1702 | `3820c588f490a94de60063f4d404604b63003aff5cd8d35563af83c9db76c709` | 0 |
| scroll-contracts/src/misc/ScrollOwner.sol | 5219 | `1b619fac0f10aeea239b20742ac5c98472500c17c1a8b347930285f8786baef5` | 0 |
| scroll-contracts/src/package.json | 1580 | `03e4c0c9721f0332a2b014ace38c6840bd187da754f367893b492758fa43cf30` | 0 |
| scroll-contracts/src/rate-limiter/ETHRateLimiter.sol | 3444 | `bc5996d07b3171005c7b84598f8bfe26640fde33839659ad8f82382951656a31` | 0 |
| scroll-contracts/src/rate-limiter/IETHRateLimiter.sol | 1124 | `18fbc2cc112f2c5980cb09f79974c41542cc2b31bd2639b4786c5e765c07c96d` | 0 |
| scroll-contracts/src/rate-limiter/ITokenRateLimiter.sol | 1252 | `d5cbbf76c1e37bbfaa4fdd0e56fb033215753eb37b192eebaec636a89230971d` | 0 |
| scroll-contracts/src/rate-limiter/TokenRateLimiter.sol | 3408 | `637e1e9864d2b3121d26259a43f5c0635839940ad0f96b5e9974c089e557b693` | 0 |
| scroll-contracts/yarn.lock | 487566 | `e4a9097a1bf5beebb1fdea1f089022009a37470d4e6411cbdec0bae6a877cf5b` | 0 |
