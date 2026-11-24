# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** scroll @ 3046bbd18a6a · scroll — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-11-24 17:22 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 498c6e51-d506-4b5e-8c75-d9dbcddc1905 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.21.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `b66307f2b2bc454e65fcd895e9d042e915ba094dcaa747a4b18b64c10d95f7ed` |
| Ключ подписи (отпечаток SHA-256 ключа Ed25519, затем ML-DSA-65, если он подписывает вместе с ним; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **5**
- Высокая: **26**
- Средняя: **33**
- Низкая: **65**
- Информационная: **142**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 213
- Подтверждённая ошибка конфигурации: 1
- Потенциальный криптографический риск: 3
- Долгосрочный постквантовый риск: 4
- Рекомендация по улучшению: 50
- Недостаточность данных: 0

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

Проверка аналитика: подтверждено — 0, не применимо — 0, отклонено как ложные срабатывания — 4.

**Постквантовая зрелость: Уровень 3 из 4 — гибридная защита в критичном пути.** Следующий шаг: Закрепите версию тулчейна и задайте группы TLS в коде (X25519MLKEM768 первой): найденный гибридный обмен ключами держится на умолчании, которого код не показывает, и смена тулчейна или библиотеки его изменит.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/scroll-tech/scroll> @ `3046bbd18a6a05bf29dd3ffef7b5676203201050` — ссылки в доказательствах открывают строки на этом коммите.

385 файлов, всего 2790659 байт, редактирований: 0; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 216 | .github/scripts/bump_version_dot_go.mjs: 37 lines scanned with 17 rule patterns and 340 registry patterns; bridge-history-api/abi/backend_abi.go: 344 lines scanned with 17 rule patterns and 340 registry patterns; bridge-history-api/cmd/api/app/app.go: 114 lines scanned with 17 rule patterns and 340 registry patterns |
| dependencies | проверено | 16 | Cargo.lock: 938 dependencies parsed (938 pinned); Cargo.toml: 29 dependencies parsed (7 pinned); bridge-history-api/go.mod: 111 dependencies parsed (111 pinned) |
| tls_code | проверено | 1 | bridge-history-api/cmd/api/app/app.go: TLS key-exchange settings read |
| tls_code | Недостаточность данных | 5 | bridge-history-api/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS; common/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS; coordinator/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS |
| smart_contracts | проверено | 152 | scroll-contracts/lib/solmate/src/auth/Auth.sol: built-in Solidity pattern checks; scroll-contracts/lib/solmate/src/auth/Owned.sol: built-in Solidity pattern checks; scroll-contracts/lib/solmate/src/auth/authorities/MultiRolesAuthority.sol: built-in Solidity pattern checks |
| slither | не проверено | 152 | slither is not installed on the server (pip install slither-analyzer + solc) |
| entropy | проверено | 1 | random-number generation: 216 code files read with 1 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| key_storage | проверено | 1 | key settings with a fallback in the code: 0; decryption fallbacks: 0; derived nonces: 0; key columns: 0 (a KMS, HSM or vault service is used); author warnings: 0 |
| govulncheck | проверено | 1 | govulncheck@v1.9.0 with the Go vulnerability database of 2026-11-23: 5 of 6 Go module(s) scanned from their product packages; not scanned: tests/integration-test (no product packages in this module) |
| osv_advisories | не проверено | 1 | 137 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: ecies, encoder-standard, ethers-core, halo2-axiom, halo2-axiom-gpu, halo2-base, halo2-ecc, halo2curves-axiom, k256, openvm, openvm-algebra-circuit, openvm-algebra-complex-macros … |
| osv_advisories | проверено | 1 | 2634 pinned packages queried at OSV.dev; 175 affected (84 of them only in development or build dependencies) |
| osv_advisories | Недостаточность данных | 1 | Go/golang.org/x/crypto@v0.32.0: 21 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- tls_code — Недостаточность данных: 5 (примеры: bridge-history-api/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS; common/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS; coordinator/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS)
- slither — не проверено: 152 (примеры: slither is not installed on the server (pip install slither-analyzer + solc))
- osv_advisories — не проверено: 1 (примеры: 137 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: ecies, encoder-standard, ethers-core, halo2-axiom, halo2-axiom-gpu, halo2-base, halo2-ecc, halo2curves-axiom, k256, openvm, openvm-algebra-circuit, openvm-algebra-complex-macros …)
- osv_advisories — Недостаточность данных: 1 (примеры: Go/golang.org/x/crypto@v0.32.0: 21 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest)

## 5. Краткое описание архитектуры

Static review of the source tree scroll at 3046bbd18a6a05bf29dd3ffef7b5676203201050. 385 files analysed; of 883 files, 335 are test, fuzzing, benchmark or example code and were left out, 163 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .claude/agents/local-e2e-tester.md, .claude/agents/skill-tester.md, .claude/agents/zkvm-prover-runner.md, .claude/settings.json, .claude/skills/agent-memory/SKILL.md. 389 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. 163 files come from directories a .gitmodules pins and are read as shipped source rather than skipped as a dependency cache: scroll-contracts (141), scroll-contracts/lib/solmate (22). No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **0** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 10.8%

## 7. Подробное описание находок

### QSI-2026-50810 — github.com/gin-contrib/cors v1.5.0 затронут GHSA-869c-j7wc-8jqv (CVE-2019-25211, GO-2024-2955)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/github.com/gin-contrib/cors@v1.5.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 67.7 / 100
- CVSS v3.1: 9.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-869c-j7wc-8jqv (CVE-2019-25211, GO-2024-2955) для пакета Go github.com/gin-contrib/cors версии v1.5.0: Gin mishandles a wildcard at the end of an origin string. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/route.Route → github.com/gin-contrib/cors.New.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.6.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50834 — golang.org/x/crypto v0.32.0 затронут GHSA-f5wc-c3c7-36mc (CVE-2026-39832, GO-2026-5006)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 67.7 / 100
- CVSS v3.1: 9.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-f5wc-c3c7-36mc (CVE-2026-39832, GO-2026-5006) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto doesn't drop invoking agent constraints when forwarding keys. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/logic/provertask.NewBatchProverTask → … → golang.org/x/crypto/ssh/agent.keyring.Add.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-f5wc-c3c7-36mc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-f5wc-c3c7-36mc](https://osv.dev/vulnerability/GHSA-f5wc-c3c7-36mc) · line 111 · SHA-256 67c43f8d6c4ce229ae11ed6cd042845cb0ed7a461d4bc4817b2fc43e47a3a220_

```
{"id": "GHSA-f5wc-c3c7-36mc", "aliases": ["CVE-2026-39832", "GO-2026-5006"], "modified": "2026-09-10T03:50:49.274413517Z", "summary": "golang.org/x/crypto doesn't drop invoking agent constraints when forwarding keys", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.52.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50838 — golang.org/x/crypto v0.32.0 затронут GHSA-jppx-rxg9-jmrx (CVE-2026-39833, GO-2026-5005)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 67.7 / 100
- CVSS v3.1: 9.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-jppx-rxg9-jmrx (CVE-2026-39833, GO-2026-5005) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto doesn't enforce invoking key constraints. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/logic/provertask.NewBatchProverTask → … → golang.org/x/crypto/ssh/agent.keyring.Add.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-jppx-rxg9-jmrx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-jppx-rxg9-jmrx](https://osv.dev/vulnerability/GHSA-jppx-rxg9-jmrx) · line 111 · SHA-256 74c040c1569f8cbf67f613fbf7ebbda4b6de9ad3b085b370db517748b8d342ec_

```
{"id": "GHSA-jppx-rxg9-jmrx", "aliases": ["CVE-2026-39833", "GO-2026-5005"], "modified": "2026-09-10T03:50:50.029914620Z", "summary": "golang.org/x/crypto doesn't enforce invoking key constraints", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.52.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50951 — proxy-addr 2.0.7 затронут GHSA-jqcg-44mw-7w3h (CVE-2026-90711)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/proxy-addr@2.0.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 40.6 / 100
- CVSS v3.1: 9.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-jqcg-44mw-7w3h (CVE-2026-90711) для пакета npm proxy-addr версии 2.0.7: proxy-addr vulnerable to IP spoofing via IPv4-mapped IPv6 trust subnet. Ни один исходный файл продукта не импортирует proxy-addr: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-jqcg-44mw-7w3h
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-jqcg-44mw-7w3h](https://osv.dev/vulnerability/GHSA-jqcg-44mw-7w3h) · line 8537 · SHA-256 068ebda1c94e135a6ba184368cc0247de44a750d8b4a53b327cb3256fede4aa0_

```
{"id": "GHSA-jqcg-44mw-7w3h", "aliases": ["CVE-2026-90711"], "modified": "2026-10-05T23:45:07.322157228Z", "summary": "proxy-addr vulnerable to IP spoofing via IPv4-mapped IPv6 trust subnet", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.0.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50971 — underscore 1.9.1 затронут GHSA-cf4h-3jhx-xvhq (CVE-2021-23358)

- Серьёзность: **Критическая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/underscore@1.9.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 40.6 / 100
- CVSS v3.1: 9.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-cf4h-3jhx-xvhq (CVE-2021-23358) для пакета npm underscore версии 1.9.1: Arbitrary Code Execution in underscore. Ни один исходный файл продукта не импортирует underscore: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-cf4h-3jhx-xvhq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-cf4h-3jhx-xvhq](https://osv.dev/vulnerability/GHSA-cf4h-3jhx-xvhq) · line 10494 · SHA-256 6724d7fde4702ec6347ca3bc7c9f3badb6d31babb165c517de175de99d00a6b0_

```
{"id": "GHSA-cf4h-3jhx-xvhq", "aliases": ["CVE-2021-23358"], "modified": "2025-11-04T16:33:59Z", "summary": "Arbitrary Code Execution in underscore", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.12.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50705 — Проверка TLS-сертификата отключена в bridge-history-api/cmd/api/app/app.go

- Серьёзность: **Высокая** · Классификация: Подтверждённая ошибка конфигурации · Уверенность: Высокая
- Затронутый актив: `file:bridge-history-api/cmd/api/app/app.go`
- Источник данных: bridge-history-api/cmd/api/app/app.go
- Метод обнаружения: Сопоставление регулярных выражений с API конкретного языка.
- Анализатор: source_code 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50814 — github.com/consensys/gnark-crypto v0.16.0 затронут GHSA-fj2x-735w-74vq (GO-2025-4087)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/github.com/consensys/gnark-crypto@v0.16.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 62.7 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-fj2x-735w-74vq (GO-2025-4087) для пакета Go github.com/consensys/gnark-crypto версии v0.16.0: gnark-crypto allows unchecked memory allocation during vector deserialization. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/controller/api.InitController → … → github.com/consensys/gnark-crypto/ecc/bls12-381/fr.Vector.ReadFrom.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.18.1, 0.19.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50843 — golang.org/x/crypto v0.32.0 затронут GHSA-w879-237q-wc7r (CVE-2026-39829, GO-2026-5018)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 62.7 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-w879-237q-wc7r (CVE-2026-39829, GO-2026-5018) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto: Invoking pathological RSA/DSA parameters may cause DoS. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/logic/provertask.NewBatchProverTask → … → golang.org/x/crypto/ssh.ParsePublicKey.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w879-237q-wc7r
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w879-237q-wc7r](https://osv.dev/vulnerability/GHSA-w879-237q-wc7r) · line 111 · SHA-256 be81c970b9360c2e2acdbe4c847c0e96c0da46ecff8a93472d3f6d32541055c5_

```
{"id": "GHSA-w879-237q-wc7r", "aliases": ["CVE-2026-39829", "GO-2026-5018"], "modified": "2026-09-10T03:50:50.833802829Z", "summary": "golang.org/x/crypto: Invoking pathological RSA/DSA parameters may cause DoS", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.52.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50910 — github.com/golang-jwt/jwt/v4 v4.5.0 затронут GHSA-mh63-6h87-95cp (CVE-2025-30204, GO-2025-3553)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/github.com/golang-jwt/jwt/v4@v4.5.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 62.7 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-mh63-6h87-95cp (CVE-2025-30204, GO-2025-3553) для пакета Go github.com/golang-jwt/jwt/v4 версии v4.5.0: jwt-go allows excessive memory allocation during header parsing. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/cmd/api/app.Run → … → github.com/golang-jwt/jwt/v4.Parser.ParseUnverified.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mh63-6h87-95cp
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mh63-6h87-95cp](https://osv.dev/vulnerability/GHSA-mh63-6h87-95cp) · line 31 · SHA-256 1c46a44dbca84b8ba050d374b445250b54474d4376bdf3893c0f721ce054a33d_

```
{"id": "GHSA-mh63-6h87-95cp", "aliases": ["CVE-2025-30204", "GO-2025-3553"], "modified": "2026-09-10T03:50:56.801646453Z", "summary": "jwt-go allows excessive memory allocation during header parsing", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.5.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50779 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0340

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает RUSTSEC-2026-0340 для пакета crates.io quinn-proto версии 0.11.16: Peer minimum ACK delay can panic quinn-proto when ACK_FREQUENCY transmission is enabled. Ни один исходный файл продукта не импортирует quinn-proto: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.11.18).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50780 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0341

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает RUSTSEC-2026-0341 для пакета crates.io quinn-proto версии 0.11.16: Stream reassembly memory-exhaustion guard in quinn-proto can be bypassed. Ни один исходный файл продукта не импортирует quinn-proto: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.11.17).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50936 — body-parser 1.19.2 затронут GHSA-27r3-jxmh-p828 (CVE-2026-111181)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/body-parser@1.19.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-27r3-jxmh-p828 (CVE-2026-111181) для пакета npm body-parser версии 1.19.2: body-parser vulnerable to Denial of Service via trailing bytes after a compressed request body. Ни один исходный файл продукта не импортирует body-parser: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-27r3-jxmh-p828
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-27r3-jxmh-p828](https://osv.dev/vulnerability/GHSA-27r3-jxmh-p828) · line 2566 · SHA-256 d543d5d551c4905cfb479113347b1052576dde0acd9bf492cd62c4e048d1ccf8_

```
{"id": "GHSA-27r3-jxmh-p828", "aliases": ["CVE-2026-111181"], "modified": "2026-10-23T21:00:06.131613693Z", "summary": "body-parser vulnerable to Denial of Service via trailing bytes after a compressed request body", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.9, 2.4.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50937 — body-parser 1.19.2 затронут GHSA-qwcr-r2fm-qrc7 (CVE-2024-45590)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/body-parser@1.19.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-qwcr-r2fm-qrc7 (CVE-2024-45590) для пакета npm body-parser версии 1.19.2: body-parser vulnerable to denial of service when url encoding is enabled. Ни один исходный файл продукта не импортирует body-parser: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qwcr-r2fm-qrc7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qwcr-r2fm-qrc7](https://osv.dev/vulnerability/GHSA-qwcr-r2fm-qrc7) · line 2566 · SHA-256 012609ef9f8a2c51b034d2d1cc1de31e8e4ab1249dbf4fba3d800c42a9ef0070_

```
{"id": "GHSA-qwcr-r2fm-qrc7", "aliases": ["CVE-2024-45590"], "modified": "2026-09-10T03:50:18.292199548Z", "summary": "body-parser vulnerable to denial of service when url encoding is enabled", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50939 — body-parser 1.20.0 затронут GHSA-27r3-jxmh-p828 (CVE-2026-111181)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/body-parser@1.20.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-27r3-jxmh-p828 (CVE-2026-111181) для пакета npm body-parser версии 1.20.0: body-parser vulnerable to Denial of Service via trailing bytes after a compressed request body. Ни один исходный файл продукта не импортирует body-parser: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-27r3-jxmh-p828
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-27r3-jxmh-p828](https://osv.dev/vulnerability/GHSA-27r3-jxmh-p828) · line 2582 · SHA-256 d543d5d551c4905cfb479113347b1052576dde0acd9bf492cd62c4e048d1ccf8_

```
{"id": "GHSA-27r3-jxmh-p828", "aliases": ["CVE-2026-111181"], "modified": "2026-10-23T21:00:06.131613693Z", "summary": "body-parser vulnerable to Denial of Service via trailing bytes after a compressed request body", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.9, 2.4.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50940 — body-parser 1.20.0 затронут GHSA-qwcr-r2fm-qrc7 (CVE-2024-45590)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/body-parser@1.20.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-qwcr-r2fm-qrc7 (CVE-2024-45590) для пакета npm body-parser версии 1.20.0: body-parser vulnerable to denial of service when url encoding is enabled. Ни один исходный файл продукта не импортирует body-parser: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qwcr-r2fm-qrc7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qwcr-r2fm-qrc7](https://osv.dev/vulnerability/GHSA-qwcr-r2fm-qrc7) · line 2582 · SHA-256 012609ef9f8a2c51b034d2d1cc1de31e8e4ab1249dbf4fba3d800c42a9ef0070_

```
{"id": "GHSA-qwcr-r2fm-qrc7", "aliases": ["CVE-2024-45590"], "modified": "2026-09-10T03:50:18.292199548Z", "summary": "body-parser vulnerable to denial of service when url encoding is enabled", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50942 — browserify-sign 4.2.1 затронут GHSA-x9w5-v3q2-3rhw (CVE-2023-46234)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/browserify-sign@4.2.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-x9w5-v3q2-3rhw (CVE-2023-46234) для пакета npm browserify-sign версии 4.2.1: browserify-sign upper bound check issue in `dsaVerify` leads to a signature forgery attack. Ни один исходный файл продукта не импортирует browserify-sign: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x9w5-v3q2-3rhw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-x9w5-v3q2-3rhw](https://osv.dev/vulnerability/GHSA-x9w5-v3q2-3rhw) · line 2701 · SHA-256 0acdbc6a4bb5482f30a32977a7bcd70032b43491b3fdcc217fd8073b50ff4dd7_

```
{"id": "GHSA-x9w5-v3q2-3rhw", "aliases": ["CVE-2023-46234"], "modified": "2026-09-10T03:50:08.674168828Z", "summary": "browserify-sign upper bound check issue in `dsaVerify` leads to a signature forgery attack", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.2.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50948 — http-cache-semantics 4.1.0 затронут GHSA-rc47-6667-2j5j (CVE-2022-25881)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/http-cache-semantics@4.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-rc47-6667-2j5j (CVE-2022-25881) для пакета npm http-cache-semantics версии 4.1.0: http-cache-semantics vulnerable to Regular Expression Denial of Service. Ни один исходный файл продукта не импортирует http-cache-semantics: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rc47-6667-2j5j
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rc47-6667-2j5j](https://osv.dev/vulnerability/GHSA-rc47-6667-2j5j) · line 6046 · SHA-256 1aaf98cc6c7be197b42d6dec9a69d20499295cc1367748bc694fc6775af63451_

```
{"id": "GHSA-rc47-6667-2j5j", "aliases": ["CVE-2022-25881"], "modified": "2026-09-10T03:49:51.817106987Z", "summary": "http-cache-semantics vulnerable to Regular Expression Denial of Service", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.1.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50949 — path-to-regexp 0.1.7 затронут GHSA-37ch-88jc-xwx2 (CVE-2024-45296, CVE-2026-4867, GHSA-9wv6-86v2-598j)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/path-to-regexp@0.1.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-37ch-88jc-xwx2 (CVE-2024-45296, CVE-2026-4867, GHSA-9wv6-86v2-598j) для пакета npm path-to-regexp версии 0.1.7: path-to-regexp vulnerable to Regular Expression Denial of Service via multiple route parameters. Ни один исходный файл продукта не импортирует path-to-regexp: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-37ch-88jc-xwx2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-37ch-88jc-xwx2](https://osv.dev/vulnerability/GHSA-37ch-88jc-xwx2) · line 8361 · SHA-256 37242ff70b6bb8c1c985072103e8e4a6b5b1513f02830586f318b20781196a81_

```
{"id": "GHSA-37ch-88jc-xwx2", "aliases": ["CVE-2024-45296", "CVE-2026-4867", "GHSA-9wv6-86v2-598j"], "modified": "2026-09-10T03:50:36.768786245Z", "summary": "path-to-regexp vulnerable to Regular Expression Denial of Service via multiple route parameters", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.1.13).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50950 — path-to-regexp 0.1.7 затронут GHSA-rhx6-c78j-4q9w (CVE-2024-52798)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/path-to-regexp@0.1.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-rhx6-c78j-4q9w (CVE-2024-52798) для пакета npm path-to-regexp версии 0.1.7: path-to-regexp contains a ReDoS. Ни один исходный файл продукта не импортирует path-to-regexp: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rhx6-c78j-4q9w
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rhx6-c78j-4q9w](https://osv.dev/vulnerability/GHSA-rhx6-c78j-4q9w) · line 8361 · SHA-256 be8e8da1029118f01fd6984d52c33d0d2fc940fb509484b602952df6c54aac87_

```
{"id": "GHSA-rhx6-c78j-4q9w", "aliases": ["CVE-2024-52798"], "modified": "2026-09-10T03:50:56.223604407Z", "summary": "path-to-regexp contains a ReDoS", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.1.12).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50958 — tar 4.4.19 затронут GHSA-23hp-3jrh-7fpw (CVE-2026-59873)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/tar@4.4.19`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-23hp-3jrh-7fpw (CVE-2026-59873) для пакета npm tar версии 4.4.19: node-tar: Decompression/parse DoS via unlimited input. Ни один исходный файл продукта не импортирует tar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-23hp-3jrh-7fpw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-23hp-3jrh-7fpw](https://osv.dev/vulnerability/GHSA-23hp-3jrh-7fpw) · line 10076 · SHA-256 276d1e846cb7e92cee9ddade9aa5bb24d61b108d20805a2ac571e9fd96604b1a_

```
{"id": "GHSA-23hp-3jrh-7fpw", "aliases": ["CVE-2026-59873"], "modified": "2026-09-10T03:51:09.781853040Z", "summary": "node-tar: Decompression/parse DoS via unlimited input", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.5.19).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50959 — tar 4.4.19 затронут GHSA-34x7-hfp2-rc4v (CVE-2026-24842)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/tar@4.4.19`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 8.2 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N`)

OSV.dev сообщает GHSA-34x7-hfp2-rc4v (CVE-2026-24842) для пакета npm tar версии 4.4.19: node-tar Vulnerable to Arbitrary File Creation/Overwrite via Hardlink Path Traversal. Ни один исходный файл продукта не импортирует tar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-34x7-hfp2-rc4v
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-34x7-hfp2-rc4v](https://osv.dev/vulnerability/GHSA-34x7-hfp2-rc4v) · line 10076 · SHA-256 9fb73088fa579d89539dc76b86232dbc8c57d1acff9f450c8cab212ce011bd7b_

```
{"id": "GHSA-34x7-hfp2-rc4v", "aliases": ["CVE-2026-24842"], "modified": "2026-09-10T03:50:32.616577975Z", "summary": "node-tar Vulnerable to Arbitrary File Creation/Overwrite via Hardlink Path Traversal", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:H/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.5.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50960 — tar 4.4.19 затронут GHSA-83g3-92jg-28cx (CVE-2026-26960)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/tar@4.4.19`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.1 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-83g3-92jg-28cx (CVE-2026-26960) для пакета npm tar версии 4.4.19: Arbitrary File Read/Write via Hardlink Target Escape Through Symlink Chain in node-tar Extraction. Ни один исходный файл продукта не импортирует tar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-83g3-92jg-28cx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-83g3-92jg-28cx](https://osv.dev/vulnerability/GHSA-83g3-92jg-28cx) · line 10076 · SHA-256 ab11e4e8fecb5e911af0b96aad429a294d6e8a492e2a09cf5d908f993b7e747a_

```
{"id": "GHSA-83g3-92jg-28cx", "aliases": ["CVE-2026-26960"], "modified": "2026-09-10T03:50:34.418493270Z", "summary": "Arbitrary File Read/Write via Hardlink Target Escape Through Symlink Chain in node-tar Extraction", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.5.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50961 — tar 4.4.19 затронут GHSA-8qq5-rm4j-mr97 (CVE-2026-23745)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/tar@4.4.19`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-8qq5-rm4j-mr97 (CVE-2026-23745) для пакета npm tar версии 4.4.19: node-tar is Vulnerable to Arbitrary File Overwrite and Symlink Poisoning via Insufficient Path Sanitization. Ни один исходный файл продукта не импортирует tar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8qq5-rm4j-mr97
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8qq5-rm4j-mr97](https://osv.dev/vulnerability/GHSA-8qq5-rm4j-mr97) · line 10076 · SHA-256 8fdc582c24b2c7a0062464aef066d471c68c527d4136238d0d93bd6da151058e_

```
{"id": "GHSA-8qq5-rm4j-mr97", "aliases": ["CVE-2026-23745"], "modified": "2026-09-10T03:50:59.009017334Z", "summary": "node-tar is Vulnerable to Arbitrary File Overwrite and Symlink Poisoning via Insufficient Path Sanitization", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:H/VI:L/VA:N/SC:H/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.5.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50962 — tar 4.4.19 затронут GHSA-8x88-c5mf-7j5w (CVE-2026-59874)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/tar@4.4.19`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-8x88-c5mf-7j5w (CVE-2026-59874) для пакета npm tar версии 4.4.19: node-tar: Negative tar entry size causes infinite loop in archive replace. Ни один исходный файл продукта не импортирует tar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8x88-c5mf-7j5w
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8x88-c5mf-7j5w](https://osv.dev/vulnerability/GHSA-8x88-c5mf-7j5w) · line 10076 · SHA-256 dc7a74a5ba01a09895ff25def512cee6cbcff04987e267cf604bf35e3abba583_

```
{"id": "GHSA-8x88-c5mf-7j5w", "aliases": ["CVE-2026-59874"], "modified": "2026-09-10T03:51:11.200904859Z", "summary": "node-tar: Negative tar entry size causes infinite loop in archive replace", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.5.18).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50963 — tar 4.4.19 затронут GHSA-9ppj-qmqm-q256 (CVE-2026-31802)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/tar@4.4.19`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-9ppj-qmqm-q256 (CVE-2026-31802) для пакета npm tar версии 4.4.19: node-tar Symlink Path Traversal via Drive-Relative Linkpath. Ни один исходный файл продукта не импортирует tar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9ppj-qmqm-q256
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9ppj-qmqm-q256](https://osv.dev/vulnerability/GHSA-9ppj-qmqm-q256) · line 10076 · SHA-256 7b70992f07e35bc33e0484d3d63a8102e7ee3350c3c73da1e9a4c9c303d82928_

```
{"id": "GHSA-9ppj-qmqm-q256", "aliases": ["CVE-2026-31802"], "modified": "2026-09-10T03:50:38.398085665Z", "summary": "node-tar Symlink Path Traversal via Drive-Relative Linkpath", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.5.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50966 — tar 4.4.19 затронут GHSA-qffp-2rhf-9h96 (CVE-2026-29786)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/tar@4.4.19`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-qffp-2rhf-9h96 (CVE-2026-29786) для пакета npm tar версии 4.4.19: tar has Hardlink Path Traversal via Drive-Relative Linkpath. Ни один исходный файл продукта не импортирует tar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qffp-2rhf-9h96
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qffp-2rhf-9h96](https://osv.dev/vulnerability/GHSA-qffp-2rhf-9h96) · line 10076 · SHA-256 cbe18f81c5a374868579eddd593e6ce85980a23d12aaecdb882fd7daadb9451e_

```
{"id": "GHSA-qffp-2rhf-9h96", "aliases": ["CVE-2026-29786"], "modified": "2026-09-10T03:50:40.605623006Z", "summary": "tar has Hardlink Path Traversal via Drive-Relative Linkpath", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:P/VC:N/VI:H/VA:L/SC:N/SI:H/SA:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.5.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50967 — tar 4.4.19 затронут GHSA-r292-9mhp-454m (CVE-2026-73566)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/tar@4.4.19`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-r292-9mhp-454m (CVE-2026-73566) для пакета npm tar версии 4.4.19: node-tar: Uncontrolled recursion in mapHas/filesFilter allows uncatchable stack-overflow DoS via crafted long-path tar with member selection. Ни один исходный файл продукта не импортирует tar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-r292-9mhp-454m
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-r292-9mhp-454m](https://osv.dev/vulnerability/GHSA-r292-9mhp-454m) · line 10076 · SHA-256 c2841865d98ff8cf133f3ba222211e7f7e0b059111be20d9c3ec91c007355494_

```
{"id": "GHSA-r292-9mhp-454m", "aliases": ["CVE-2026-73566"], "modified": "2026-09-10T03:51:11.855710545Z", "summary": "node-tar: Uncontrolled recursion in mapHas/filesFilter allows uncatchable stack-overflow DoS via crafted long-path tar with member selection", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.5.21).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50968 — tar 4.4.19 затронут GHSA-r6q2-hw4h-h46w (CVE-2026-23950)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/tar@4.4.19`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 8.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:H/A:L`)

OSV.dev сообщает GHSA-r6q2-hw4h-h46w (CVE-2026-23950) для пакета npm tar версии 4.4.19: Race Condition in node-tar Path Reservations via Unicode Ligature Collisions on macOS APFS. Ни один исходный файл продукта не импортирует tar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-r6q2-hw4h-h46w
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-r6q2-hw4h-h46w](https://osv.dev/vulnerability/GHSA-r6q2-hw4h-h46w) · line 10076 · SHA-256 05374d8495772cd1ac897167064ae3d81d1abf703d192ea1aaa04fba26af0ffb_

```
{"id": "GHSA-r6q2-hw4h-h46w", "aliases": ["CVE-2026-23950"], "modified": "2026-09-10T03:50:59.225342497Z", "summary": "Race Condition in node-tar Path Reservations via Unicode Ligature Collisions on macOS APFS", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:H/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.5.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50973 — uuid 3.3.2 затронут GHSA-w5hq-g745-h8pq (CVE-2026-41907, CVE-2026-41988)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/uuid@3.3.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-w5hq-g745-h8pq (CVE-2026-41907, CVE-2026-41988) для пакета npm uuid версии 3.3.2: uuid: Missing buffer bounds check in v3/v5/v6 when buf is provided. Ни один исходный файл продукта не импортирует uuid: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w5hq-g745-h8pq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w5hq-g745-h8pq](https://osv.dev/vulnerability/GHSA-w5hq-g745-h8pq) · line 10636 · SHA-256 f94cf00d6646863e6202ca5032c2fa134f1f32236a5f5563b53c63a3fd7c36fc_

```
{"id": "GHSA-w5hq-g745-h8pq", "aliases": ["CVE-2026-41907", "CVE-2026-41988"], "modified": "2026-09-10T03:51:03.663336650Z", "summary": "uuid: Missing buffer bounds check in v3/v5/v6 when buf is provided", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (11.1.1, 12.0.1, 13.0.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50977 — ws 3.3.3 затронут GHSA-3h5v-q93c-6h6q (CVE-2024-37890)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/ws@3.3.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-3h5v-q93c-6h6q (CVE-2024-37890) для пакета npm ws версии 3.3.3: ws affected by a DoS when handling a request with many HTTP headers. Ни один исходный файл продукта не импортирует ws: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3h5v-q93c-6h6q
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3h5v-q93c-6h6q](https://osv.dev/vulnerability/GHSA-3h5v-q93c-6h6q) · line 11202 · SHA-256 3501f0a557eeb2cecd3d128ba7db71ca5906ff46f6703e83e30bc64ca4cf6c62_

```
{"id": "GHSA-3h5v-q93c-6h6q", "aliases": ["CVE-2024-37890"], "modified": "2026-09-10T03:50:14.788589634Z", "summary": "ws affected by a DoS when handling a request with many HTTP headers", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (5.2.4, 6.2.3, 7.5.10, 8.17.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50978 — ws 3.3.3 затронут GHSA-96hv-2xvq-fx4p (CVE-2026-48779)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/ws@3.3.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-96hv-2xvq-fx4p (CVE-2026-48779) для пакета npm ws версии 3.3.3: ws: Memory exhaustion DoS from tiny fragments and data chunks. Ни один исходный файл продукта не импортирует ws: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-96hv-2xvq-fx4p
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-96hv-2xvq-fx4p](https://osv.dev/vulnerability/GHSA-96hv-2xvq-fx4p) · line 11202 · SHA-256 5c75ebd76cc50a27635938f1c0f2ce228e66b824d41638bb63da88d8092bd1ff_

```
{"id": "GHSA-96hv-2xvq-fx4p", "aliases": ["CVE-2026-48779"], "modified": "2026-09-10T03:50:49.163643932Z", "summary": "ws: Memory exhaustion DoS from tiny fragments and data chunks", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (5.2.5, 6.2.4, 7.5.11, 8.21.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50823 — github.com/gorilla/websocket v1.5.0 затронут GHSA-w67g-5rqw-f597 (GO-2026-6278)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/github.com/gorilla/websocket@v1.5.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 55.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-w67g-5rqw-f597 (GO-2026-6278) для пакета Go github.com/gorilla/websocket версии v1.5.0: Gorilla WebSocket Uses Cryptographically Weak PRNG for WebSocket Mask Key. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/controller/api.InitController → … → github.com/gorilla/websocket.Conn.Close.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w67g-5rqw-f597
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w67g-5rqw-f597](https://osv.dev/vulnerability/GHSA-w67g-5rqw-f597) · line 56 · SHA-256 7de9e7bbb6825a2986abd386a9fae7a562d84e6b074081c8d22ac27d99696b39_

```
{"id": "GHSA-w67g-5rqw-f597", "aliases": ["GO-2026-6278"], "modified": "2026-09-10T03:50:54.128553228Z", "summary": "Gorilla WebSocket Uses Cryptographically Weak PRNG for WebSocket Mask Key", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.5.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50833 — golang.org/x/crypto v0.32.0 затронут GHSA-9m57-25v3-79x9 (CVE-2026-46598, GO-2026-5033)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 55.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-9m57-25v3-79x9 (CVE-2026-46598, GO-2026-5033) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto: Invoking pathological inputs can lead to client panic. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/logic/provertask.NewBatchProverTask → … → golang.org/x/crypto/ssh/agent.ServeAgent.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9m57-25v3-79x9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9m57-25v3-79x9](https://osv.dev/vulnerability/GHSA-9m57-25v3-79x9) · line 111 · SHA-256 4081cc7d5b546f765534ef0de0f679b36fe76216056a572fc152c1bb89c59ebb_

```
{"id": "GHSA-9m57-25v3-79x9", "aliases": ["CVE-2026-46598", "GO-2026-5033"], "modified": "2026-09-10T03:50:55.369516615Z", "summary": "golang.org/x/crypto: Invoking pathological inputs can lead to client panic", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.52.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50835 — golang.org/x/crypto v0.32.0 затронут GHSA-f6x5-jh6r-wrfv (CVE-2025-47914, GO-2025-4135)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 55.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-f6x5-jh6r-wrfv (CVE-2025-47914, GO-2025-4135) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto/ssh/agent vulnerable to panic if message is malformed due to out of bounds read. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/logic/provertask.NewBatchProverTask → … → golang.org/x/crypto/ssh/agent.ServeAgent.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-f6x5-jh6r-wrfv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-f6x5-jh6r-wrfv](https://osv.dev/vulnerability/GHSA-f6x5-jh6r-wrfv) · line 111 · SHA-256 2bada5788b5e09f3aba90bd4d02b5feeb8ad952ffd72f8d1f24c85742e624dd1_

```
{"id": "GHSA-f6x5-jh6r-wrfv", "aliases": ["CVE-2025-47914", "GO-2025-4135"], "modified": "2026-09-10T03:50:30.884151926Z", "summary": "golang.org/x/crypto/ssh/agent vulnerable to panic if message is malformed due to out of bounds read", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.45.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50851 — golang.org/x/net v0.25.0 затронут GHSA-vvgc-356p-c3xw (CVE-2025-22872, GO-2025-3595)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 55.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-vvgc-356p-c3xw (CVE-2025-22872, GO-2025-3595) для пакета Go golang.org/x/net версии v0.25.0: golang.org/x/net vulnerable to Cross-site Scripting. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/controller/api.TxsByHashesController.PostQueryTxsByHashes → … → golang.org/x/net/html.Tokenizer.Next.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vvgc-356p-c3xw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vvgc-356p-c3xw](https://osv.dev/vulnerability/GHSA-vvgc-356p-c3xw) · line 112 · SHA-256 109e6c01855d433b163ba29e8b1379aca3cc3b18ce096c793df9109cdc0b1a2e_

```
{"id": "GHSA-vvgc-356p-c3xw", "aliases": ["CVE-2025-22872", "GO-2025-3595"], "modified": "2026-09-10T03:50:24.031676301Z", "summary": "golang.org/x/net vulnerable to Cross-site Scripting", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:N/SC:L/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.38.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50913 — golang.org/x/net v0.23.0 затронут GHSA-vvgc-356p-c3xw (CVE-2025-22872, GO-2025-3595)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 55.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-vvgc-356p-c3xw (CVE-2025-22872, GO-2025-3595) для пакета Go golang.org/x/net версии v0.23.0: golang.org/x/net vulnerable to Cross-site Scripting. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/controller/proxy.GetTaskController.GetTasks → … → golang.org/x/net/html.Tokenizer.Next.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vvgc-356p-c3xw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vvgc-356p-c3xw](https://osv.dev/vulnerability/GHSA-vvgc-356p-c3xw) · line 43 · SHA-256 109e6c01855d433b163ba29e8b1379aca3cc3b18ce096c793df9109cdc0b1a2e_

```
{"id": "GHSA-vvgc-356p-c3xw", "aliases": ["CVE-2025-22872", "GO-2025-3595"], "modified": "2026-09-10T03:50:24.031676301Z", "summary": "golang.org/x/net vulnerable to Cross-site Scripting", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:N/VI:N/VA:N/SC:L/SI:L/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.38.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50931 — github.com/gorilla/websocket v1.4.2 затронут GHSA-w67g-5rqw-f597 (GO-2026-6278)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/github.com/gorilla/websocket@v1.4.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 55.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-w67g-5rqw-f597 (GO-2026-6278) для пакета Go github.com/gorilla/websocket версии v1.4.2: Gorilla WebSocket Uses Cryptographically Weak PRNG for WebSocket Mask Key. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/logic/verifier.NewVerifier → … → github.com/gorilla/websocket.messageReader.Read.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w67g-5rqw-f597
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w67g-5rqw-f597](https://osv.dev/vulnerability/GHSA-w67g-5rqw-f597) · line 67 · SHA-256 7de9e7bbb6825a2986abd386a9fae7a562d84e6b074081c8d22ac27d99696b39_

```
{"id": "GHSA-w67g-5rqw-f597", "aliases": ["GO-2026-6278"], "modified": "2026-09-10T03:50:54.128553228Z", "summary": "Gorilla WebSocket Uses Cryptographically Weak PRNG for WebSocket Mask Key", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.5.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50932 — github.com/aws/aws-sdk-go-v2/service/s3 v1.80.0 затронут GHSA-xmrv-pmrh-hhx2 (CVE-2026-89090, GO-2026-5764)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/github.com/aws/aws-sdk-go-v2/service/s3@v1.80.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 55.2 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-xmrv-pmrh-hhx2 (CVE-2026-89090, GO-2026-5764) для пакета Go github.com/aws/aws-sdk-go-v2/service/s3 версии v1.80.0: Denial of Service due to Panic in AWS SDK for Go v2 SDK EventStream Decoder. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/rollup/internal/controller/sender.Sender.SendTransaction → github.com/aws/aws-sdk-go-v2/service/s3/types.NotFound.Error.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xmrv-pmrh-hhx2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xmrv-pmrh-hhx2](https://osv.dev/vulnerability/GHSA-xmrv-pmrh-hhx2) · line 11 · SHA-256 15d8b4646fcc4908c052eea7f8932ce8adde5e240c61e80ce3104bd27a06dd2f_

```
{"id": "GHSA-xmrv-pmrh-hhx2", "aliases": ["CVE-2026-89090", "GO-2026-5764"], "modified": "2026-09-12T04:10:37.759930105Z", "summary": "Denial of Service due to Panic in AWS SDK for Go v2 SDK EventStream Decoder", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.97.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50933 — github.com/aws/aws-sdk-go-v2/aws/protocol/eventstream v1.6.10 затронут GHSA-xmrv-pmrh-hhx2 (CVE-2026-89090, GO-2026-5764)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/github.com/aws/aws-sdk-go-v2/aws/protocol/eventstream@v1.6.10`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 55.2 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-xmrv-pmrh-hhx2 (CVE-2026-89090, GO-2026-5764) для пакета Go github.com/aws/aws-sdk-go-v2/aws/protocol/eventstream версии v1.6.10: Denial of Service due to Panic in AWS SDK for Go v2 SDK EventStream Decoder. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/rollup/internal/controller/sender.Sender.SendTransaction → github.com/aws/aws-sdk-go-v2/service/s3/types.NotFound.Error.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xmrv-pmrh-hhx2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xmrv-pmrh-hhx2](https://osv.dev/vulnerability/GHSA-xmrv-pmrh-hhx2) · line 30 · SHA-256 162c292e6344e54170fb5ec72004a2fb986450ee14d32da318a0dc74f4bdc39b_

```
{"id": "GHSA-xmrv-pmrh-hhx2", "aliases": ["CVE-2026-89090", "GO-2026-5764"], "modified": "2026-09-12T04:10:37.759930105Z", "summary": "Denial of Service due to Panic in AWS SDK for Go v2 SDK EventStream Decoder", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.7.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50934 — @openzeppelin/contracts-upgradeable 4.9.3 затронут GHSA-9vx6-7xxf-x967 (CVE-2024-27094)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/@openzeppelin/contracts-upgradeable@4.9.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H`)

OSV.dev сообщает GHSA-9vx6-7xxf-x967 (CVE-2024-27094) для пакета npm @openzeppelin/contracts-upgradeable версии 4.9.3: OpenZeppelin Contracts base64 encoding may read from potentially dirty memory. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9vx6-7xxf-x967
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9vx6-7xxf-x967](https://osv.dev/vulnerability/GHSA-9vx6-7xxf-x967) · line 968 · SHA-256 f50c51a969cd09898613e36784a2ae70898d488ed8ae6c2640fb125c863ff3e8_

```
{"id": "GHSA-9vx6-7xxf-x967", "aliases": ["CVE-2024-27094"], "modified": "2025-12-05T12:36:38.324850Z", "summary": "OpenZeppelin Contracts base64 encoding may read from potentially dirty memory", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.9.6, 5.0.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50935 — @openzeppelin/contracts 4.9.3 затронут GHSA-9vx6-7xxf-x967 (CVE-2024-27094)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:npm/@openzeppelin/contracts@4.9.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H`)

OSV.dev сообщает GHSA-9vx6-7xxf-x967 (CVE-2024-27094) для пакета npm @openzeppelin/contracts версии 4.9.3: OpenZeppelin Contracts base64 encoding may read from potentially dirty memory. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9vx6-7xxf-x967
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9vx6-7xxf-x967](https://osv.dev/vulnerability/GHSA-9vx6-7xxf-x967) · line 973 · SHA-256 f50c51a969cd09898613e36784a2ae70898d488ed8ae6c2640fb125c863ff3e8_

```
{"id": "GHSA-9vx6-7xxf-x967", "aliases": ["CVE-2024-27094"], "modified": "2025-12-05T12:36:38.324850Z", "summary": "OpenZeppelin Contracts base64 encoding may read from potentially dirty memory", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:H"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.9.6, 5.0.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50718 — Вызывающий относится к контрактам или обычным аккаунтам по одной проверке (msg.sender == tx.origin) в scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol`
- Источник данных: scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 39.9 / 100
- CVSS v3.1: неприменимо

Защита в строка 95 по одной проверке (msg.sender == tx.origin) решает, является ли вызывающий контрактом или внешним аккаунтом (EOA). (см. SWC-115, EIP-7702)

**Возможные последствия.** После EIP-7702 (Pectra, 2025; действует также в BNB Smart Chain и основных роллапах) внешний аккаунт может делегировать исполнение коду. Такой аккаунт проходит проверку msg.sender == tx.origin, выполняя произвольную логику в той же транзакции — пакетные вызовы, атомарные многошаговые сделки, повторный вход из собственного кода, — поэтому защита от флеш-займов, ботов и повторного входа, построенная на этой проверке, больше не работает. У него также ненулевой размер кода: проверка размера кода теперь принимает обычных пользователей за контракты и пропускает как контракт любой делегирующий аккаунт. До Pectra проверку размера кода уже можно было пройти из конструктора.

**Шаги воспроизведения.**

```
Откройте строка 95 в предоставленном файле scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol#L95) · line 95 · SHA-256 41ace0cd92cb1c9b4c4f134113693600d663684ebbf2dcf5792349b73db5d6c8_

```
   93 |     ) external payable whenNotPaused {
   94 |         // solhint-disable-next-line avoid-tx-origin
   95 |         require(msg.sender == tx.origin, "Only EOA senders are allowed to send enforced transaction");
   96 | 
   97 |         _sendTransaction(msg.sender, _target, _value, _gasLimit, _data, msg.sender);
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Не полагайтесь на код вызывающего. То, что защищала эта проверка, защитите блокировкой повторного входа, лимитами на блок или транзакцию, схемой commit-reveal или белым списком; если вызывающий действительно должен быть без кода, проверяйте происхождение и размер кода вместе.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-50708 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (5 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: rollup/internal/controller/relayer/l2_relayer.go
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

8 упоминаний ECDSA в 5 файл(ах), например rollup/internal/controller/relayer/l2_relayer.go:1305. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте rollup/internal/controller/relayer/l2_relayer.go:1305 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [rollup/internal/controller/relayer/l2_relayer.go](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/rollup/internal/controller/relayer/l2_relayer.go#L1305) · line 1305 · SHA-256 59a13c6f5e5fe5cba732d56c58bb972bbffcd1268070a8d12170ac5cb62ab627_

```
 1304 | 	case sender.PrivateKeySignerType:
 1305 | 		privKey, err := crypto.ToECDSA(common.FromHex(config.PrivateKeySignerConfig.PrivateKey))
 1306 | 		if err != nil {
```

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

_file_excerpt · [rollup/internal/controller/sender/transaction_signer.go](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/rollup/internal/controller/sender/transaction_signer.go#L43) · line 43 · SHA-256 c7abe5587d6aa522d0d090dbec20ad92c2205c8078d2cd1478a499280eea3467_

```
   42 | 	case PrivateKeySignerType:
   43 | 		privKey, err := crypto.ToECDSA(common.FromHex(config.PrivateKeySignerConfig.PrivateKey))
   44 | 		if err != nil {
```

_file_excerpt · [scroll-contracts/src/lido/L2WstETHToken.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/lido/L2WstETHToken.sol#L43) · line 43 · SHA-256 ed1f1287cd4dbdfa2460c94bb6fe236af24ff2474533da4da640caa27c1a7a34_

```
   41 | 
   42 |         require(
   43 |             SignatureCheckerUpgradeable.isValidSignatureNow(owner, hash, abi.encodePacked(r, s, v)),
   44 |             "ERC20Permit: invalid signature"
   45 |         );
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

### QSI-2026-50706 — Квантово-уязвимый ECDSA: роль не определена (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: common/utils/keystore.go
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

3 упоминаний ECDSA в 2 файл(ах), например common/utils/keystore.go:4. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

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

_file_excerpt · [coordinator/internal/controller/proxy/client_manager.go](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/coordinator/internal/controller/proxy/client_manager.go#L53) · line 53 · SHA-256 a54f5fa38f9f52103f9c4350c06b7d7c03d779938634448cf0a9f1b0ccec9426_

```
   52 | 		// Try to create private key from hash
   53 | 		if k, err := crypto.ToECDSA(hash); err == nil {
   54 | 			return k, nil
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-50707 — Квантово-уязвимый ECDSA: аутентификация и идентификация (сертификаты, токены, аттестация устройств) (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:authentication`
- Источник данных: coordinator/internal/types/auth.go
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50748 — Криптография на спариваниях в контракте: BN254 (alt_bn128) (scroll-contracts/src/libraries/verifier/RollupVerifier.sol)

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:scroll-contracts/src/libraries/verifier/RollupVerifier.sol`
- Источник данных: scroll-contracts/src/libraries/verifier/RollupVerifier.sol
- Метод обнаружения: Сопоставление шаблонов реестра с учётом комментариев.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50757 — block-buffer 0.11.0 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/block-buffer@0.11.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-qwgh-2vcv-g2f7 для пакета crates.io block-buffer версии 0.11.0: block_buffer: panic corrupts inline buffer position. Ни один исходный файл продукта не импортирует block-buffer: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50787 — rustls 0.23.41 затронут GHSA-2mjx-qc3c-rqvc (CVE-2026-123613, RUSTSEC-2026-0285)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.23.41`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-2mjx-qc3c-rqvc (CVE-2026-123613, RUSTSEC-2026-0285) для пакета crates.io rustls версии 0.23.41: Rustls: TLS 1.3 handshake messages incorrectly accepted across encryption level boundaries. Ни один исходный файл продукта не импортирует rustls: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2mjx-qc3c-rqvc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2mjx-qc3c-rqvc](https://osv.dev/vulnerability/GHSA-2mjx-qc3c-rqvc) · manifest · SHA-256 27d1fd62c5110767bb200358c8938aa31e7a2c8002b938045a39437cc6ad385d_

```
{"id": "GHSA-2mjx-qc3c-rqvc", "aliases": ["CVE-2026-123613", "RUSTSEC-2026-0285"], "modified": "2026-11-08T10:55:54.395419388Z", "summary": "Rustls: TLS 1.3 handshake messages incorrectly accepted across encryption level boundaries", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.45).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50788 — rustls 0.23.41 затронут GHSA-c8m5-c952-6cm4 (CVE-2026-123609, RUSTSEC-2026-0346)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.23.41`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-c8m5-c952-6cm4 (CVE-2026-123609, RUSTSEC-2026-0346) для пакета crates.io rustls версии 0.23.41: Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs. Ни один исходный файл продукта не импортирует rustls: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-c8m5-c952-6cm4
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-c8m5-c952-6cm4](https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4) · manifest · SHA-256 db21533e93ce33709016b3df1ccf6fa4b9c394d59f597caf8a06cf90ca35b744_

```
{"id": "GHSA-c8m5-c952-6cm4", "aliases": ["CVE-2026-123609", "RUSTSEC-2026-0346"], "modified": "2026-11-08T10:55:36.514447652Z", "summary": "Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.46, 0.24.0-dev.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50943 — cookiejar 2.1.3 затронут GHSA-h452-7996-h45h (CVE-2022-25901)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/cookiejar@2.1.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-h452-7996-h45h (CVE-2022-25901) для пакета npm cookiejar версии 2.1.3: cookiejar Regular Expression Denial of Service via Cookie.parse function. Ни один исходный файл продукта не импортирует cookiejar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-h452-7996-h45h
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-h452-7996-h45h](https://osv.dev/vulnerability/GHSA-h452-7996-h45h) · line 3396 · SHA-256 15bb7e42e4e291fba91161b5bdf93ca34de24a2ce99dc8f2bc73efa3336e760d_

```
{"id": "GHSA-h452-7996-h45h", "aliases": ["CVE-2022-25901"], "modified": "2025-02-13T19:03:25.062781Z", "summary": "cookiejar Regular Expression Denial of Service via Cookie.parse function", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.1.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50944 — express 4.17.3 затронут GHSA-qw6h-vgh9-j6wx (CVE-2024-43796)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/express@4.17.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.0 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:L`)

OSV.dev сообщает GHSA-qw6h-vgh9-j6wx (CVE-2024-43796) для пакета npm express версии 4.17.3: express vulnerable to XSS via response.redirect(). Ни один исходный файл продукта не импортирует express: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qw6h-vgh9-j6wx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qw6h-vgh9-j6wx](https://osv.dev/vulnerability/GHSA-qw6h-vgh9-j6wx) · line 4897 · SHA-256 37b8271da60a50417e558ac3e704c89524c68ee989ad5e7784be1960da96336c_

```
{"id": "GHSA-qw6h-vgh9-j6wx", "aliases": ["CVE-2024-43796"], "modified": "2026-09-10T03:50:18.298562940Z", "summary": "express vulnerable to XSS via response.redirect()", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:N/VI:N/VA:N/SC:L/SI:L/SA:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.20.0, 5.0.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50945 — express 4.17.3 затронут GHSA-rv95-896h-c2vc (CVE-2024-29041)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/express@4.17.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 6.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-rv95-896h-c2vc (CVE-2024-29041) для пакета npm express версии 4.17.3: Express.js Open Redirect in malformed URLs. Ни один исходный файл продукта не импортирует express: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rv95-896h-c2vc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rv95-896h-c2vc](https://osv.dev/vulnerability/GHSA-rv95-896h-c2vc) · line 4897 · SHA-256 23426f8a0b08558211d10681840738db4ddd94b3081744aba9dedb184be7c279_

```
{"id": "GHSA-rv95-896h-c2vc", "aliases": ["CVE-2024-29041"], "modified": "2026-09-10T03:50:10.750068508Z", "summary": "Express.js Open Redirect in malformed URLs", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.19.2, 5.0.0-beta.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50946 — got 9.6.0 затронут GHSA-pfrx-2q88-qq97 (CVE-2022-33987)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/got@9.6.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-pfrx-2q88-qq97 (CVE-2022-33987) для пакета npm got версии 9.6.0: Got allows a redirect to a UNIX socket. Ни один исходный файл продукта не импортирует got: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pfrx-2q88-qq97
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pfrx-2q88-qq97](https://osv.dev/vulnerability/GHSA-pfrx-2q88-qq97) · line 5736 · SHA-256 db9378561bbe6bfbb4b3c5723f5ca44968c6e698b76b6144b4d529aff06a2e28_

```
{"id": "GHSA-pfrx-2q88-qq97", "aliases": ["CVE-2022-33987"], "modified": "2026-09-10T03:49:55.225771209Z", "summary": "Got allows a redirect to a UNIX socket", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (11.8.5, 12.1.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50947 — got 7.1.0 затронут GHSA-pfrx-2q88-qq97 (CVE-2022-33987)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/got@7.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-pfrx-2q88-qq97 (CVE-2022-33987) для пакета npm got версии 7.1.0: Got allows a redirect to a UNIX socket. Ни один исходный файл продукта не импортирует got: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pfrx-2q88-qq97
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pfrx-2q88-qq97](https://osv.dev/vulnerability/GHSA-pfrx-2q88-qq97) · line 5753 · SHA-256 db9378561bbe6bfbb4b3c5723f5ca44968c6e698b76b6144b4d529aff06a2e28_

```
{"id": "GHSA-pfrx-2q88-qq97", "aliases": ["CVE-2022-33987"], "modified": "2026-09-10T03:49:55.225771209Z", "summary": "Got allows a redirect to a UNIX socket", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (11.8.5, 12.1.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50952 — qs 6.9.7 затронут GHSA-4mjr-xmp4-gh2g (CVE-2026-82417)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/qs@6.9.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-4mjr-xmp4-gh2g (CVE-2026-82417) для пакета npm qs версии 6.9.7: qs: Denial of Service via Attacker Controlled isBuffer. Ни один исходный файл продукта не импортирует qs: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4mjr-xmp4-gh2g
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4mjr-xmp4-gh2g](https://osv.dev/vulnerability/GHSA-4mjr-xmp4-gh2g) · line 8650 · SHA-256 afef9a11fcfc48b7311cfed5a422a080a74b32761380006786083623b479434f_

```
{"id": "GHSA-4mjr-xmp4-gh2g", "aliases": ["CVE-2026-82417"], "modified": "2026-09-10T03:51:14.991984096Z", "summary": "qs: Denial of Service via Attacker Controlled isBuffer", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.16.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50953 — qs 6.9.7 затронут GHSA-6pq8-jhm2-2vcw (CVE-2026-110816)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/qs@6.9.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-6pq8-jhm2-2vcw (CVE-2026-110816) для пакета npm qs версии 6.9.7: qs : qs.stringify with arrayFormat 'comma' throws an uncaught TypeError on array elements carrying a non-callable own toString (DoS). Ни один исходный файл продукта не импортирует qs: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6pq8-jhm2-2vcw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-6pq8-jhm2-2vcw](https://osv.dev/vulnerability/GHSA-6pq8-jhm2-2vcw) · line 8650 · SHA-256 4fd7af689173b0c3abc4f3e9006070e7de778a692b621288cc277cd4bcb7ab05_

```
{"id": "GHSA-6pq8-jhm2-2vcw", "aliases": ["CVE-2026-110816"], "modified": "2026-10-27T16:15:05.324423680Z", "summary": "qs : qs.stringify with arrayFormat 'comma' throws an uncaught TypeError on array elements carrying a non-callable own toString (DoS)", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.16.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50956 — send 0.17.2 затронут GHSA-m6fv-jmcg-4jfg (CVE-2024-43799)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/send@0.17.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.0 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:L`)

OSV.dev сообщает GHSA-m6fv-jmcg-4jfg (CVE-2024-43799) для пакета npm send версии 0.17.2: send vulnerable to template injection that can lead to XSS. Ни один исходный файл продукта не импортирует send: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-m6fv-jmcg-4jfg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-m6fv-jmcg-4jfg](https://osv.dev/vulnerability/GHSA-m6fv-jmcg-4jfg) · line 9278 · SHA-256 81b7f94fc105fde0bdc5486b55fe5a717d4687b91ba43cd898bded7e08c90eba_

```
{"id": "GHSA-m6fv-jmcg-4jfg", "aliases": ["CVE-2024-43799"], "modified": "2026-09-10T03:50:18.939403414Z", "summary": "send vulnerable to template injection that can lead to XSS", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:N/VI:N/VA:N/SC:L/SI:L/SA:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.19.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50957 — serve-static 1.14.2 затронут GHSA-cm22-4g7w-348p (CVE-2024-43800)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/serve-static@1.14.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.0 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:L`)

OSV.dev сообщает GHSA-cm22-4g7w-348p (CVE-2024-43800) для пакета npm serve-static версии 1.14.2: serve-static vulnerable to template injection that can lead to XSS. Ни один исходный файл продукта не импортирует serve-static: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-cm22-4g7w-348p
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-cm22-4g7w-348p](https://osv.dev/vulnerability/GHSA-cm22-4g7w-348p) · line 9311 · SHA-256 7bcd2eaa63b8b69a7e86b9871724c07aa2ea7bed17edb440ca4002e3a57270e6_

```
{"id": "GHSA-cm22-4g7w-348p", "aliases": ["CVE-2024-43800"], "modified": "2026-09-10T03:50:18.868190591Z", "summary": "serve-static vulnerable to template injection that can lead to XSS", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:N/VI:N/VA:N/SC:L/SI:L/SA:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.0, 2.1.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50964 — tar 4.4.19 затронут GHSA-f5x3-32g6-xq36 (CVE-2024-28863)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/tar@4.4.19`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-f5x3-32g6-xq36 (CVE-2024-28863) для пакета npm tar версии 4.4.19: Denial of service while parsing a tar file due to lack of folders count validation. Ни один исходный файл продукта не импортирует tar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-f5x3-32g6-xq36
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-f5x3-32g6-xq36](https://osv.dev/vulnerability/GHSA-f5x3-32g6-xq36) · line 10076 · SHA-256 cde8f34c6021f43017ff24965a5530ef0109098f7c3c644766223827e997ebc3_

```
{"id": "GHSA-f5x3-32g6-xq36", "aliases": ["CVE-2024-28863"], "modified": "2026-09-10T03:50:10.480254172Z", "summary": "Denial of service while parsing a tar file due to lack of folders count validation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.2.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50965 — tar 4.4.19 затронут GHSA-gvwx-54wh-qm9j (CVE-2026-59875)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/tar@4.4.19`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-gvwx-54wh-qm9j (CVE-2026-59875) для пакета npm tar версии 4.4.19: node-tar: Uncaught Exception DoS via NUL byte in PAX path/linkpath records. Ни один исходный файл продукта не импортирует tar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-gvwx-54wh-qm9j
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-gvwx-54wh-qm9j](https://osv.dev/vulnerability/GHSA-gvwx-54wh-qm9j) · line 10076 · SHA-256 01e0ce837d2e265b07c59f6eb024ba06bafbc0dd1496ccaee746257925d16bd2_

```
{"id": "GHSA-gvwx-54wh-qm9j", "aliases": ["CVE-2026-59875"], "modified": "2026-09-10T03:50:52.205344551Z", "summary": "node-tar: Uncaught Exception DoS via NUL byte in PAX path/linkpath records", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.5.17).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50969 — tar 4.4.19 затронут GHSA-vmf3-w455-68vh (CVE-2026-53655)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/tar@4.4.19`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-vmf3-w455-68vh (CVE-2026-53655) для пакета npm tar версии 4.4.19: node-tar applies PAX size override to intermediary GNU long-name/long-link headers, causing tar parser interpretation differential (file smuggling). Ни один исходный файл продукта не импортирует tar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vmf3-w455-68vh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vmf3-w455-68vh](https://osv.dev/vulnerability/GHSA-vmf3-w455-68vh) · line 10076 · SHA-256 4b9ea42469ca1bcd0630d1510b3351bd4f38ae118c52d36e43972d6cdf2c6f3c_

```
{"id": "GHSA-vmf3-w455-68vh", "aliases": ["CVE-2026-53655"], "modified": "2026-09-10T03:51:09.639522869Z", "summary": "node-tar applies PAX size override to intermediary GNU long-name/long-link headers, causing tar parser interpretation differential (file smuggling)", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.5.16).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50970 — tar 4.4.19 затронут GHSA-w8wr-v893-vjvp (CVE-2026-59871)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/tar@4.4.19`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-w8wr-v893-vjvp (CVE-2026-59871) для пакета npm tar версии 4.4.19: node-tar: Process crash via PAX numeric path type confusion. Ни один исходный файл продукта не импортирует tar: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w8wr-v893-vjvp
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w8wr-v893-vjvp](https://osv.dev/vulnerability/GHSA-w8wr-v893-vjvp) · line 10076 · SHA-256 349d2c1dc757fe532459ba2ec92ea48f6a26c29bf9dca632df176838450ccc7c_

```
{"id": "GHSA-w8wr-v893-vjvp", "aliases": ["CVE-2026-59871"], "modified": "2026-09-10T03:51:12.362978491Z", "summary": "node-tar: Process crash via PAX numeric path type confusion", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (7.5.18).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50972 — underscore 1.9.1 затронут GHSA-qpx9-hpmf-5gmw (CVE-2026-27601)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/underscore@1.9.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-qpx9-hpmf-5gmw (CVE-2026-27601) для пакета npm underscore версии 1.9.1: Underscore has unlimited recursion in _.flatten and _.isEqual, potential for DoS attack. Ни один исходный файл продукта не импортирует underscore: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qpx9-hpmf-5gmw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qpx9-hpmf-5gmw](https://osv.dev/vulnerability/GHSA-qpx9-hpmf-5gmw) · line 10494 · SHA-256 90e8e1045cd04ec7b466b4c0e1075255658f932f1e7a977150bc9f6d8f8887f7_

```
{"id": "GHSA-qpx9-hpmf-5gmw", "aliases": ["CVE-2026-27601"], "modified": "2026-09-10T03:51:00.752419958Z", "summary": "Underscore has unlimited recursion in _.flatten and _.isEqual, potential for DoS attack", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.13.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50746 — ERC-20 transfer вызывается напрямую, не через SafeERC20 (возвращаемое значение не проверяется) в scroll-contracts/src/libraries/token/ScrollStandardERC20.sol

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:scroll-contracts/src/libraries/token/ScrollStandardERC20.sol`
- Источник данных: scroll-contracts/src/libraries/token/ScrollStandardERC20.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 28.1 / 100
- CVSS v3.1: неприменимо

Прямых вызовов токена, который контракту передают извне: 1; первый — ERC20Upgradeable.transfer(...) в строка 62: возвращаемое значение не проверяется. (см. SWC-104)

**Возможные последствия.** USDT в Ethereum ничего не возвращает из transfer, transferFrom и approve, а USDT в Tron, по сообщениям, возвращает false при успешном transfer: вызов через интерфейс, объявляющий bool, откатывается или читает неверный ответ, и функция не работает с крупнейшим стейблкоином. Токен, возвращающий false вместо отката, при игнорировании значения отказывает молча, и контракт учитывает перевод, которого не было. Безвредно только для токена, о котором известно, что он откатывается при ошибке и возвращает true.

**Шаги воспроизведения.**

```
Откройте строка 62 в предоставленном файле scroll-contracts/src/libraries/token/ScrollStandardERC20.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [scroll-contracts/src/libraries/token/ScrollStandardERC20.sol](https://github.com/scroll-tech/scroll/blob/3046bbd18a6a05bf29dd3ffef7b5676203201050/scroll-contracts/src/libraries/token/ScrollStandardERC20.sol#L62) · line 62 · SHA-256 b6e5f2383c7825d97b5f4302139469b361c44de93a4cbdfe469f150eaf63d474_

```
   60 |         bytes calldata data
   61 |     ) external returns (bool success) {
   62 |         ERC20Upgradeable.transfer(receiver, amount);
   63 |         if (isContract(receiver)) {
   64 |             contractFallback(receiver, amount, data);
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin SafeERC20 (safeTransfer, safeTransferFrom, forceApprove) или эквивалент, принимающий и пустой ответ, и true.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-50825 — github.com/jackc/pgx/v5 v5.5.4 затронут GHSA-j88v-2chj-qfwx (CVE-2026-41889, GO-2026-5004)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/github.com/jackc/pgx/v5@v5.5.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 49.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-j88v-2chj-qfwx (CVE-2026-41889, GO-2026-5004) для пакета Go github.com/jackc/pgx/v5 версии v5.5.4: pgx: SQL Injection via placeholder confusion with dollar quoted string literals. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/orm/migrate.Current → … → github.com/jackc/pgx/v5/internal/sanitize.SanitizeSQL.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (5.9.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50909 — github.com/golang-jwt/jwt/v4 v4.5.0 затронут GHSA-29wx-vh33-7x7r (CVE-2024-51744, GO-2024-3250)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая
- Затронутый актив: `dependency:Go/github.com/golang-jwt/jwt/v4@v4.5.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 49.0 / 100
- CVSS v3.1: 3.1 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-29wx-vh33-7x7r (CVE-2024-51744, GO-2024-3250) для пакета Go github.com/golang-jwt/jwt/v4 версии v4.5.0: Bad documentation of error handling in ParseWithClaims can lead to potentially dangerous situations. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/cmd/api/app.Run → … → github.com/golang-jwt/jwt/v4.Parse.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-29wx-vh33-7x7r
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-29wx-vh33-7x7r](https://osv.dev/vulnerability/GHSA-29wx-vh33-7x7r) · line 31 · SHA-256 33722fb420a0bc38418ef7562076a0a3828b3f03f40ca883d6c33b1171977d85_

```
{"id": "GHSA-29wx-vh33-7x7r", "aliases": ["CVE-2024-51744", "GO-2024-3250"], "modified": "2026-09-10T03:50:20.232143805Z", "summary": "Bad documentation of error handling in ParseWithClaims can lead to potentially dangerous situations", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (4.5.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50793 — tracing-subscriber 0.2.25 затронут GHSA-xwfj-jgwm-7wp5 (CVE-2025-58160, RUSTSEC-2025-0055)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/tracing-subscriber@0.2.25`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.3.20).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50712 — Плавающая версия компилятора (^0.8.10) в 1 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.10`
- Источник данных: scroll-contracts/scripts/foundry/DeployLidoGateway.s.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50713 — Плавающая версия компилятора (^0.8.24) в 58 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.24`
- Источник данных: scroll-contracts/src/L1/IL1ScrollMessenger.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50742 — Плавающая версия компилятора (^0.8.0) в 5 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.0`
- Источник данных: scroll-contracts/src/L2/predeploys/WrappedEther.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50828 — github.com/klauspost/compress v1.17.9 затронут GO-2026-6865 (CVE-2026-116591) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/klauspost/compress@v1.17.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6865 (CVE-2026-116591) для пакета Go github.com/klauspost/compress версии v1.17.9: Panic on two-block frames in github.com/klauspost/compress. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/logic.L1EventParser.ParseL1BatchEventLogs → … → github.com/klauspost/compress/huff0.ReadTable.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6865
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6865](https://osv.dev/vulnerability/GO-2026-6865) · line 68 · SHA-256 2aa0756615e0716b75174745db11008de5c2427c3e52d618c93c9d2ade31496f_

```
{"id": "GO-2026-6865", "aliases": ["CVE-2026-116591", "GHSA-fpmh-frq8-7rj8"], "modified": "2026-11-05T23:15:14.472777299Z", "summary": "Panic on two-block frames in github.com/klauspost/compress", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.20.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50845 — golang.org/x/crypto v0.32.0 затронут GO-2025-4116 (CVE-2025-47913) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2025-4116 (CVE-2025-47913) для пакета Go golang.org/x/crypto версии v0.32.0: Potential denial of service in golang.org/x/crypto/ssh/agent. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/logic/provertask.NewBatchProverTask → … → golang.org/x/crypto/ssh/agent.client.List.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2025-4116
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2025-4116](https://osv.dev/vulnerability/GO-2025-4116) · line 111 · SHA-256 dd9dc67ce1c135e7d52fd8915c54a886ce471f066c04ff0664541801aa0e0550_

```
{"id": "GO-2025-4116", "aliases": ["CVE-2025-47913", "GHSA-56w8-48fp-6mgv"], "modified": "2026-11-23T21:12:30.039587020Z", "summary": "Potential denial of service in golang.org/x/crypto/ssh/agent", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.43.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50855 — golang.org/x/net v0.25.0 затронут GO-2026-4918 (CVE-2026-33814) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-4918 (CVE-2026-33814) для пакета Go golang.org/x/net версии v0.25.0: Infinite loop in HTTP/2 transport when given bad SETTINGS_MAX_FRAME_SIZE in net/http/internal/http2 in golang.org/x/net. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/controller/fetcher.NewL1MessageFetcher → … → golang.org/x/net/http2.clientConnReadLoop.processSettingsNoWrite.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-4918
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-4918](https://osv.dev/vulnerability/GO-2026-4918) · line 112 · SHA-256 669b07afc8d08c551f79a30192afcf2cbb4767ec56b5cacd92c0a7677ce22cee_

```
{"id": "GO-2026-4918", "aliases": ["BIT-golang-2026-33814", "CVE-2026-33814"], "modified": "2026-11-23T21:12:28.465241903Z", "summary": "Infinite loop in HTTP/2 transport when given bad SETTINGS_MAX_FRAME_SIZE in net/http/internal/http2 in golang.org/x/net", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.53.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50857 — golang.org/x/net v0.25.0 затронут GO-2026-5026 (CVE-2026-39821) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5026 (CVE-2026-39821) для пакета Go golang.org/x/net версии v0.25.0: Invoking failure to reject ASCII-only Punycode-encoded labels in golang.org/x/net/idna. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/controller/fetcher.NewL1MessageFetcher → … → golang.org/x/net/idna.ToASCII.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5026
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5026](https://osv.dev/vulnerability/GO-2026-5026) · line 112 · SHA-256 0c8c1c1d52d99f1aa4409e163a96e360b04c6bb0633261fe5b868c1a207a5cdc_

```
{"id": "GO-2026-5026", "aliases": ["CVE-2026-39821"], "modified": "2026-11-23T21:12:28.671130412Z", "summary": "Invoking failure to reject ASCII-only Punycode-encoded labels in golang.org/x/net/idna", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.57.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50862 — golang.org/x/net v0.25.0 затронут GO-2026-6603 (CVE-2026-78659) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6603 (CVE-2026-78659) для пакета Go golang.org/x/net версии v0.25.0: HTTP/2 server memory exhaustion due to Trailer headers in net/http. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/types.RenderJSON → golang.org/x/net/http2.pseudoHeaderError.Error.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6603
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6603](https://osv.dev/vulnerability/GO-2026-6603) · line 112 · SHA-256 41efef6f9e261038a26d570f9d667deff8b8cf67065d827b3e65e9b8473ee664_

```
{"id": "GO-2026-6603", "aliases": ["BIT-golang-2026-78659", "CVE-2026-78659"], "modified": "2026-11-23T21:12:29.903950358Z", "summary": "HTTP/2 server memory exhaustion due to Trailer headers in net/http", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.60.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50863 — golang.org/x/net v0.25.0 затронут GO-2026-6610 (CVE-2026-78660) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6610 (CVE-2026-78660) для пакета Go golang.org/x/net версии v0.25.0: HTTP/2 transport accepts malformed framing-related headers in net/http. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/controller/fetcher.NewL1MessageFetcher → … → golang.org/x/net/http2.clientConnReadLoop.handleResponse.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6610
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6610](https://osv.dev/vulnerability/GO-2026-6610) · line 112 · SHA-256 0ed28b7d57d567c00a5d74ef09d210e9b41ca752a9f786aab84734fcca7dab74_

```
{"id": "GO-2026-6610", "aliases": ["BIT-golang-2026-78660", "CVE-2026-78660"], "modified": "2026-11-23T21:12:29.831892156Z", "summary": "HTTP/2 transport accepts malformed framing-related headers in net/http", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.60.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50864 — golang.org/x/net v0.25.0 затронут GO-2026-6611 (CVE-2026-78669) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6611 (CVE-2026-78669) для пакета Go golang.org/x/net версии v0.25.0: Excessive CPU consumption from repeated initial window changes in net/http. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/types.RenderJSON → golang.org/x/net/http2.ConnectionError.Error.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6611
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6611](https://osv.dev/vulnerability/GO-2026-6611) · line 112 · SHA-256 3f6098f691faf768a7e747628144bd25947e949fc71b328f78074bdf4638333d_

```
{"id": "GO-2026-6611", "aliases": ["BIT-golang-2026-78669", "CVE-2026-78669"], "modified": "2026-11-23T21:12:29.007257358Z", "summary": "Excessive CPU consumption from repeated initial window changes in net/http", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.60.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50865 — golang.org/x/net v0.25.0 затронут GO-2026-6612 (CVE-2026-78663) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6612 (CVE-2026-78663) для пакета Go golang.org/x/net версии v0.25.0: Double flow control refund on HTTP/2 server streams in net/http. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/types.RenderJSON → golang.org/x/net/http2.headerFieldNameError.Error.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6612
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6612](https://osv.dev/vulnerability/GO-2026-6612) · line 112 · SHA-256 40f1c70bf5caae6f0b12a32a6c014a0273cd45a558ef1781abe540233ca17af8_

```
{"id": "GO-2026-6612", "aliases": ["BIT-golang-2026-78663", "CVE-2026-78663"], "modified": "2026-11-23T21:12:28.295006823Z", "summary": "Double flow control refund on HTTP/2 server streams in net/http", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.60.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50866 — golang.org/x/net v0.25.0 затронут GO-2026-6617 (CVE-2026-97032) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6617 (CVE-2026-97032) для пакета Go golang.org/x/net версии v0.25.0: HTTP/2 server crash due to HPACK encoder race in net/http. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/types.RenderJSON → golang.org/x/net/http2.pseudoHeaderError.Error.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6617
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6617](https://osv.dev/vulnerability/GO-2026-6617) · line 112 · SHA-256 1800738d8fafba90c8d7a323150d3d2a9a4d5c3c678c22ad01fcea25a234a31e_

```
{"id": "GO-2026-6617", "aliases": ["BIT-golang-2026-97032", "CVE-2026-97032"], "modified": "2026-11-23T21:12:28.960393562Z", "summary": "HTTP/2 server crash due to HPACK encoder race in net/http", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.60.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50870 — golang.org/x/text v0.21.0 затронут GO-2026-5970 (CVE-2026-56852) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/text@v0.21.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5970 (CVE-2026-56852) для пакета Go golang.org/x/text версии v0.21.0: Infinite loop on invalid input in golang.org/x/text. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/controller/fetcher.NewL1MessageFetcher → … → golang.org/x/text/unicode/norm.Form.String.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5970
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5970](https://osv.dev/vulnerability/GO-2026-5970) · line 114 · SHA-256 e965b42570e47460633ab14761c247210322f7fd2bcaec0ba80a47fa7231bc2a_

```
{"id": "GO-2026-5970", "aliases": ["CVE-2026-56852"], "modified": "2026-11-23T21:12:29.269820156Z", "summary": "Infinite loop on invalid input in golang.org/x/text", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.39.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50871 — golang.org/x/text v0.21.0 затронут GO-2026-6629 (CVE-2026-56851) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/text@v0.21.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6629 (CVE-2026-56851) для пакета Go golang.org/x/text версии v0.21.0: Panic parsing crafted input in x/text/secure/precis in golang.org/x/text. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/bridge-history-api/internal/orm.BatchEvent.InsertOrUpdateBatchEvents → … → golang.org/x/text/secure/precis.Profile.Bytes.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6629
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6629](https://osv.dev/vulnerability/GO-2026-6629) · line 114 · SHA-256 41214c2900243582e86ff2d02722e1ef316bbc64e14dce6180f3c37e992fdcaa_

```
{"id": "GO-2026-6629", "aliases": ["CVE-2026-56851"], "modified": "2026-11-23T21:12:29.495073874Z", "summary": "Panic parsing crafted input in x/text/secure/precis in golang.org/x/text", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.41.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50917 — golang.org/x/net v0.23.0 затронут GO-2026-4918 (CVE-2026-33814) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-4918 (CVE-2026-33814) для пакета Go golang.org/x/net версии v0.23.0: Infinite loop in HTTP/2 transport when given bad SETTINGS_MAX_FRAME_SIZE in net/http/internal/http2 in golang.org/x/net. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/controller/proxy.upClient.SubmitProof → … → golang.org/x/net/http2.noDialH2RoundTripper.RoundTrip.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-4918
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-4918](https://osv.dev/vulnerability/GO-2026-4918) · line 43 · SHA-256 669b07afc8d08c551f79a30192afcf2cbb4767ec56b5cacd92c0a7677ce22cee_

```
{"id": "GO-2026-4918", "aliases": ["BIT-golang-2026-33814", "CVE-2026-33814"], "modified": "2026-11-23T21:12:28.465241903Z", "summary": "Infinite loop in HTTP/2 transport when given bad SETTINGS_MAX_FRAME_SIZE in net/http/internal/http2 in golang.org/x/net", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.53.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50919 — golang.org/x/net v0.23.0 затронут GO-2026-5026 (CVE-2026-39821) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5026 (CVE-2026-39821) для пакета Go golang.org/x/net версии v0.23.0: Invoking failure to reject ASCII-only Punycode-encoded labels in golang.org/x/net/idna. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/controller/proxy.upClient.SubmitProof → … → golang.org/x/net/idna.ToASCII.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5026
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5026](https://osv.dev/vulnerability/GO-2026-5026) · line 43 · SHA-256 0c8c1c1d52d99f1aa4409e163a96e360b04c6bb0633261fe5b868c1a207a5cdc_

```
{"id": "GO-2026-5026", "aliases": ["CVE-2026-39821"], "modified": "2026-11-23T21:12:28.671130412Z", "summary": "Invoking failure to reject ASCII-only Punycode-encoded labels in golang.org/x/net/idna", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.57.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50924 — golang.org/x/net v0.23.0 затронут GO-2026-6603 (CVE-2026-78659) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6603 (CVE-2026-78659) для пакета Go golang.org/x/net версии v0.23.0: HTTP/2 server memory exhaustion due to Trailer headers in net/http. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/controller/proxy.upClient.SubmitProof → … → golang.org/x/net/http2.requestBody.Close.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6603
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6603](https://osv.dev/vulnerability/GO-2026-6603) · line 43 · SHA-256 41efef6f9e261038a26d570f9d667deff8b8cf67065d827b3e65e9b8473ee664_

```
{"id": "GO-2026-6603", "aliases": ["BIT-golang-2026-78659", "CVE-2026-78659"], "modified": "2026-11-23T21:12:29.903950358Z", "summary": "HTTP/2 server memory exhaustion due to Trailer headers in net/http", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.60.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50925 — golang.org/x/net v0.23.0 затронут GO-2026-6610 (CVE-2026-78660) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6610 (CVE-2026-78660) для пакета Go golang.org/x/net версии v0.23.0: HTTP/2 transport accepts malformed framing-related headers in net/http. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/controller/proxy.upClient.SubmitProof → … → golang.org/x/net/http2.noDialH2RoundTripper.RoundTrip.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6610
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6610](https://osv.dev/vulnerability/GO-2026-6610) · line 43 · SHA-256 0ed28b7d57d567c00a5d74ef09d210e9b41ca752a9f786aab84734fcca7dab74_

```
{"id": "GO-2026-6610", "aliases": ["BIT-golang-2026-78660", "CVE-2026-78660"], "modified": "2026-11-23T21:12:29.831892156Z", "summary": "HTTP/2 transport accepts malformed framing-related headers in net/http", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.60.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50926 — golang.org/x/net v0.23.0 затронут GO-2026-6611 (CVE-2026-78669) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6611 (CVE-2026-78669) для пакета Go golang.org/x/net версии v0.23.0: Excessive CPU consumption from repeated initial window changes in net/http. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/controller/proxy.upClient.SubmitProof → … → golang.org/x/net/http2.gzipReader.Close.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6611
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6611](https://osv.dev/vulnerability/GO-2026-6611) · line 43 · SHA-256 3f6098f691faf768a7e747628144bd25947e949fc71b328f78074bdf4638333d_

```
{"id": "GO-2026-6611", "aliases": ["BIT-golang-2026-78669", "CVE-2026-78669"], "modified": "2026-11-23T21:12:29.007257358Z", "summary": "Excessive CPU consumption from repeated initial window changes in net/http", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.60.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50927 — golang.org/x/net v0.23.0 затронут GO-2026-6612 (CVE-2026-78663) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6612 (CVE-2026-78663) для пакета Go golang.org/x/net версии v0.23.0: Double flow control refund on HTTP/2 server streams in net/http. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/controller/proxy.upClient.SubmitProof → … → golang.org/x/net/http2.requestBody.Close.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6612
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6612](https://osv.dev/vulnerability/GO-2026-6612) · line 43 · SHA-256 40f1c70bf5caae6f0b12a32a6c014a0273cd45a558ef1781abe540233ca17af8_

```
{"id": "GO-2026-6612", "aliases": ["BIT-golang-2026-78663", "CVE-2026-78663"], "modified": "2026-11-23T21:12:28.295006823Z", "summary": "Double flow control refund on HTTP/2 server streams in net/http", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.60.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50928 — golang.org/x/net v0.23.0 затронут GO-2026-6617 (CVE-2026-97032) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 33.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6617 (CVE-2026-97032) для пакета Go golang.org/x/net версии v0.23.0: HTTP/2 server crash due to HPACK encoder race in net/http. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызов из кода продукта до затронутого кода: scroll-tech/coordinator/internal/controller/proxy.upClient.SubmitProof → … → golang.org/x/net/http2.transportResponseBody.Close.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6617
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6617](https://osv.dev/vulnerability/GO-2026-6617) · line 43 · SHA-256 1800738d8fafba90c8d7a323150d3d2a9a4d5c3c678c22ad01fcea25a234a31e_

```
{"id": "GO-2026-6617", "aliases": ["BIT-golang-2026-97032", "CVE-2026-97032"], "modified": "2026-11-23T21:12:28.960393562Z", "summary": "HTTP/2 server crash due to HPACK encoder race in net/http", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.60.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50769 — lru 0.12.5 затронут GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/lru@0.12.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002) для пакета crates.io lru версии 0.12.5: `IterMut` violates Stacked Borrows by invalidating internal pointer. Ни один исходный файл продукта не импортирует lru: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.16.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50771 — lru 0.13.0 затронут GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/lru@0.13.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002) для пакета crates.io lru версии 0.13.0: `IterMut` violates Stacked Borrows by invalidating internal pointer. Ни один исходный файл продукта не импортирует lru: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.16.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50773 — p3-symmetric 0.4.3 затронут GHSA-3g92-f9ch-qjcm

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/p3-symmetric@0.4.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3g92-f9ch-qjcm для пакета crates.io p3-symmetric версии 0.4.3: Plonky3: The sponge construction used to get a hash function from a cryptographic permutation is not collision resistant for inputs of different lengths. Ни один исходный файл продукта не импортирует p3-symmetric: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50790 — rustls 0.23.41 затронут GHSA-w44r-93j7-qv28 (CVE-2026-123611, RUSTSEC-2026-0349)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.23.41`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-w44r-93j7-qv28 (CVE-2026-123611, RUSTSEC-2026-0349) для пакета crates.io rustls версии 0.23.41: rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share. Ни один исходный файл продукта не импортирует rustls: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w44r-93j7-qv28
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w44r-93j7-qv28](https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28) · manifest · SHA-256 8ccd9599884b4730640347a2a7b992b8b80c3163286e3af1b4c5340b999f2f18_

```
{"id": "GHSA-w44r-93j7-qv28", "aliases": ["CVE-2026-123611", "RUSTSEC-2026-0349"], "modified": "2026-11-08T10:55:46.312019109Z", "summary": "rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.46, 0.24.0-dev.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50938 — body-parser 1.19.2 затронут GHSA-v422-hmwv-36x6 (CVE-2026-12590)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/body-parser@1.19.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-v422-hmwv-36x6 (CVE-2026-12590) для пакета npm body-parser версии 1.19.2: body-parser vulnerable to denial of service when invalid limit value silently disables size enforcement. Ни один исходный файл продукта не импортирует body-parser: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-v422-hmwv-36x6
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-v422-hmwv-36x6](https://osv.dev/vulnerability/GHSA-v422-hmwv-36x6) · line 2566 · SHA-256 1f0069b4d9a1341e91257b0b8af961b3092d155007db68bfd11835cae37bcd52_

```
{"id": "GHSA-v422-hmwv-36x6", "aliases": ["CVE-2026-12590"], "modified": "2026-09-10T03:50:53.014509971Z", "summary": "body-parser vulnerable to denial of service when invalid limit value silently disables size enforcement", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.6, 2.3.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50941 — body-parser 1.20.0 затронут GHSA-v422-hmwv-36x6 (CVE-2026-12590)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/body-parser@1.20.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-v422-hmwv-36x6 (CVE-2026-12590) для пакета npm body-parser версии 1.20.0: body-parser vulnerable to denial of service when invalid limit value silently disables size enforcement. Ни один исходный файл продукта не импортирует body-parser: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-v422-hmwv-36x6
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-v422-hmwv-36x6](https://osv.dev/vulnerability/GHSA-v422-hmwv-36x6) · line 2582 · SHA-256 1f0069b4d9a1341e91257b0b8af961b3092d155007db68bfd11835cae37bcd52_

```
{"id": "GHSA-v422-hmwv-36x6", "aliases": ["CVE-2026-12590"], "modified": "2026-09-10T03:50:53.014509971Z", "summary": "body-parser vulnerable to denial of service when invalid limit value silently disables size enforcement", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.20.6, 2.3.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50954 — qs 6.9.7 затронут GHSA-6rw7-vpxm-498p (CVE-2025-15284)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/qs@6.9.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-6rw7-vpxm-498p (CVE-2025-15284) для пакета npm qs версии 6.9.7: qs's arrayLimit bypass in its bracket notation allows DoS via memory exhaustion. Ни один исходный файл продукта не импортирует qs: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6rw7-vpxm-498p
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-6rw7-vpxm-498p](https://osv.dev/vulnerability/GHSA-6rw7-vpxm-498p) · line 8650 · SHA-256 141136de198feaa7dd923faa5b81ee1ef3beaec823783b9b69e8553de66ad6ac_

```
{"id": "GHSA-6rw7-vpxm-498p", "aliases": ["CVE-2025-15284"], "modified": "2026-09-10T03:50:31.670581449Z", "summary": "qs's arrayLimit bypass in its bracket notation allows DoS via memory exhaustion", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.14.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50955 — qs 6.9.7 затронут GHSA-w7fw-mjwx-w883 (CVE-2026-2391)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/qs@6.9.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-w7fw-mjwx-w883 (CVE-2026-2391) для пакета npm qs версии 6.9.7: qs's arrayLimit bypass in comma parsing allows denial of service. Ни один исходный файл продукта не импортирует qs: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w7fw-mjwx-w883
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w7fw-mjwx-w883](https://osv.dev/vulnerability/GHSA-w7fw-mjwx-w883) · line 8650 · SHA-256 25d0e7190c29994dccc533e56ced6871aa52975dccc6195bf5176f904a52d1e8_

```
{"id": "GHSA-w7fw-mjwx-w883", "aliases": ["CVE-2026-2391"], "modified": "2026-09-10T03:50:35.973235487Z", "summary": "qs's arrayLimit bypass in comma parsing allows denial of service", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (6.14.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50974 — web3-core-method 1.2.11 затронут GHSA-2j4c-9qqq-896r (CVE-2025-57329)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/web3-core-method@1.2.11`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-2j4c-9qqq-896r (CVE-2025-57329) для пакета npm web3-core-method версии 1.2.11: web3-core-method is vulnerable to prototype pollution. Ни один исходный файл продукта не импортирует web3-core-method: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2j4c-9qqq-896r
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2j4c-9qqq-896r](https://osv.dev/vulnerability/GHSA-2j4c-9qqq-896r) · line 10743 · SHA-256 33d0142bbc7d50f64bf3f279791f83f43537b94ec9ebdc45be3e5a85d84e5360_

```
{"id": "GHSA-2j4c-9qqq-896r", "aliases": ["CVE-2025-57329"], "modified": "2025-09-26T13:27:21.954183Z", "summary": "web3-core-method is vulnerable to prototype pollution", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:P/PR:N/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50975 — web3-core-subscriptions 1.2.11 затронут GHSA-hhf6-3xpg-pggx (CVE-2025-57330)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/web3-core-subscriptions@1.2.11`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-hhf6-3xpg-pggx (CVE-2025-57330) для пакета npm web3-core-subscriptions версии 1.2.11: web3-core-subscriptions has a Prototype Pollution vulnerability. Ни один исходный файл продукта не импортирует web3-core-subscriptions: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hhf6-3xpg-pggx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-hhf6-3xpg-pggx](https://osv.dev/vulnerability/GHSA-hhf6-3xpg-pggx) · line 10773 · SHA-256 0ced323fbcca522da25e279e4c2b303c385bcc4f03c499d46ef320174d710f64_

```
{"id": "GHSA-hhf6-3xpg-pggx", "aliases": ["CVE-2025-57330"], "modified": "2025-09-25T17:12:19.059943Z", "summary": "web3-core-subscriptions has a Prototype Pollution vulnerability", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50976 — web3 1.2.11 затронут GHSA-27v7-qhfv-rqq8

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:npm/web3@1.2.11`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 3.3 (`CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-27v7-qhfv-rqq8 для пакета npm web3 версии 1.2.11: Insecure Credential Storage in web3. Ни один исходный файл продукта не импортирует web3: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-27v7-qhfv-rqq8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-27v7-qhfv-rqq8](https://osv.dev/vulnerability/GHSA-27v7-qhfv-rqq8) · line 11003 · SHA-256 f03b253d16d6a6b93e71cd22c22a18eaa0486758e36f29ad1a53df3cb642d330_

```
{"id": "GHSA-27v7-qhfv-rqq8", "aliases": [], "modified": "2021-08-31T20:56:47Z", "summary": "Insecure Credential Storage in web3", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50789 — rustls 0.23.41 затронут GHSA-h2v8-394m-p7vv (CVE-2026-123610, RUSTSEC-2026-0348)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustls@0.23.41`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 25.0 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-h2v8-394m-p7vv (CVE-2026-123610, RUSTSEC-2026-0348) для пакета crates.io rustls версии 0.23.41: Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication. Затронутый код находится за флагом Cargo `brotli`, выключенным по умолчанию; ни один проверенный манифест его не включает — бюллетень не применим, если флаг не включает другая зависимость.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-h2v8-394m-p7vv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-h2v8-394m-p7vv](https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv) · manifest · SHA-256 c263367634d669fe7d4a5d388304c4f40b83d9837549f87b19d1fc0a9e26d648_

```
{"id": "GHSA-h2v8-394m-p7vv", "aliases": ["CVE-2026-123610", "RUSTSEC-2026-0348"], "modified": "2026-11-08T10:55:59.261359726Z", "summary": "Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication.", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.46, 0.24.0-dev.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50759 — crypto-bigint 0.5.5 затронут RUSTSEC-2026-0387 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crypto-bigint@0.5.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0387 для пакета crates.io crypto-bigint версии 0.5.5: Multiple timing variability issues in operations intended to be constant-time. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует crypto-bigint: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.7.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50763 — h2 0.4.15 затронут RUSTSEC-2026-0258 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/h2@0.4.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0258 для пакета crates.io h2 версии 0.4.15: h2 unbounded empty DATA frames. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует h2: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.4.16).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50767 — libz-sys 1.1.29 затронут RUSTSEC-2026-0418 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/libz-sys@1.1.29`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.1.31).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50768 — libz-sys 1.1.29 затронут RUSTSEC-2026-0544 (CVE-2026-85091) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/libz-sys@1.1.29`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0544 (CVE-2026-85091) для пакета crates.io libz-sys версии 1.1.29: libs-sys: heap buffer overflow. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0544
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0544](https://osv.dev/vulnerability/RUSTSEC-2026-0544) · manifest · SHA-256 fc0224ada61ed9bbe0b0f3f0aeb3ca77f1145b2f420b1f7f9fd101c9dc1e85a1_

```
{"id": "RUSTSEC-2026-0544", "aliases": ["CVE-2026-85091"], "modified": "2026-11-17T10:15:02.362721160Z", "summary": "libs-sys: heap buffer overflow", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.1.33).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50770 — lru 0.12.5 затронут RUSTSEC-2026-0253 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/lru@0.12.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0253 для пакета crates.io lru версии 0.12.5: Potential use-after-free due to lack of panic safety in `LruCache::pop()`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует lru: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.18.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50772 — lru 0.13.0 затронут RUSTSEC-2026-0253 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/lru@0.13.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0253 для пакета crates.io lru версии 0.13.0: Potential use-after-free due to lack of panic safety in `LruCache::pop()`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует lru: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.18.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50777 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0338 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0338 для пакета crates.io quinn-proto версии 0.11.16: Remote peer can panic quinn-proto with zero-length STREAM frames during unordered reads. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует quinn-proto: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.11.18).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50778 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0339 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0339 для пакета crates.io quinn-proto версии 0.11.16: Unbounded growth of pending connection ID retirements in quinn-proto. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует quinn-proto: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.11.17).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50781 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0342 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0342 для пакета crates.io quinn-proto версии 0.11.16: Zero-length DATAGRAM frames bypass the receive buffer limit in quinn-proto. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует quinn-proto: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.11.17).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50782 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0523 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0523 для пакета crates.io quinn-proto версии 0.11.16: MAX_STREAM_DATA frame can open streams beyond the stream limit. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует quinn-proto: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0523
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0523](https://osv.dev/vulnerability/RUSTSEC-2026-0523) · manifest · SHA-256 ba38a838d4e45dd6958b4102d8a1ec90700c5ca22b5da6f35671a03ddf163935_

```
{"id": "RUSTSEC-2026-0523", "aliases": ["GHSA-53rm-773f-4q8c"], "modified": "2026-11-13T12:45:04.789912316Z", "summary": "MAX_STREAM_DATA frame can open streams beyond the stream limit", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.11.19).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50783 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0524 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0524 для пакета crates.io quinn-proto версии 0.11.16: Long Retry token can panic or exhaust memory in a QUIC client. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует quinn-proto: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0524
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0524](https://osv.dev/vulnerability/RUSTSEC-2026-0524) · manifest · SHA-256 9f8eaf429d5c8dd463becfc33bc7e125bb3ab1967308406c7556f423cdd5abd1_

```
{"id": "RUSTSEC-2026-0524", "aliases": ["GHSA-wppq-2f6r-wfvm"], "modified": "2026-11-13T12:45:06.127108520Z", "summary": "Long Retry token can panic or exhaust memory in a QUIC client", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.11.19).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50784 — quinn-udp 0.5.15 затронут RUSTSEC-2026-0538 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-udp@0.5.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0538 для пакета crates.io quinn-udp версии 0.5.15: Receive loop can spin after a truncated datagram. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует quinn-udp: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0538
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0538](https://osv.dev/vulnerability/RUSTSEC-2026-0538) · manifest · SHA-256 a253fc85c2462bf8cb9613adb913b5e61c4a5d4ae73f83f65e16cf568f6c2409_

```
{"id": "RUSTSEC-2026-0538", "aliases": ["GHSA-6pp4-4cxf-xf88"], "modified": "2026-11-13T12:45:08.844283231Z", "summary": "Receive loop can spin after a truncated datagram", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.5.16, 0.6.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50785 — ruint 1.19.0 затронут RUSTSEC-2026-0220 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/ruint@1.19.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0220 для пакета crates.io ruint версии 1.19.0: Uint shift operations: incorrect overflow flags and truncated shift amounts. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует ruint: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (ruint::Uint::checked_shl, ruint::Uint::checked_shr, ruint::Uint::overflowing_shl, ruint::Uint::overflowing_shr, ruint::Uint::saturating_shl, ruint::Uint::saturating_shr …); ruint приходит через другие зависимости, которые могут их вызывать.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.20.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50786 — rustix 1.1.4 затронут RUSTSEC-2026-0486 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustix@1.1.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0486 для пакета crates.io rustix версии 1.1.4: xattr functions mark unwritten bytes as initialized when given a zero-length buffer. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует rustix: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (rustix::fs::fgetxattr, rustix::fs::flistxattr, rustix::fs::getxattr, rustix::fs::lgetxattr, rustix::fs::listxattr, rustix::fs::llistxattr); rustix приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0486
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0486](https://osv.dev/vulnerability/RUSTSEC-2026-0486) · manifest · SHA-256 3a9db0a5ea2efefb678d315af96712a5f277c0e348371bd9630df7afe1635fbe_

```
{"id": "RUSTSEC-2026-0486", "aliases": ["GHSA-jh2m-fhpj-3vr7"], "modified": "2026-11-11T08:45:02.466292839Z", "summary": "xattr functions mark unwritten bytes as initialized when given a zero-length buffer", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.1.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50791 — rustls-webpki 0.103.13 затронут RUSTSEC-2026-0382 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.103.13`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0382 (CVE-2026-111943) для пакета crates.io rustls-webpki версии 0.103.13: Certificate verification may accept distrusted intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует rustls-webpki: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.103.16, 0.104.0-alpha.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50795 — webpki-roots 1.0.8 затронут RUSTSEC-2026-0381 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/webpki-roots@1.0.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0381 (CVE-2026-111943) для пакета crates.io webpki-roots версии 1.0.8: Bundled root certificates allow trust in distrusted emSign intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует webpki-roots: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.26.11, 1.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50796 — zstd 0.13.3 затронут RUSTSEC-2026-0391 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd@0.13.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0391 для пакета crates.io zstd версии 0.13.3: Data from an abandoned stream leaks into the next stream on a reused context. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует zstd: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (zstd::stream::raw::Decoder::with_context, zstd::stream::raw::Encoder::with_context); zstd приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0391
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0391](https://osv.dev/vulnerability/RUSTSEC-2026-0391) · manifest · SHA-256 f6b1f88e9d83bcb9d217fcbdccae0800038e990f9744b0323a94b3c98f05b7b9_

```
{"id": "RUSTSEC-2026-0391", "aliases": [], "modified": "2026-11-02T09:30:03.590733846Z", "summary": "Data from an abandoned stream leaks into the next stream on a reused context", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.13.4, 0.14.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50797 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0395 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0395 для пакета crates.io zstd-safe версии 7.2.4: Use-after-free with `CParameter::StableInBuffer`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует zstd-safe: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::set_parameter); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0395
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0395](https://osv.dev/vulnerability/RUSTSEC-2026-0395) · manifest · SHA-256 728850176f43ecf2b9c562524c791d0da3abc31547980bb333caeadf51eb3ce4_

```
{"id": "RUSTSEC-2026-0395", "aliases": [], "modified": "2026-11-02T09:30:03.420559993Z", "summary": "Use-after-free with `CParameter::StableInBuffer`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (7.4.0, 8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50798 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0396 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0396 для пакета crates.io zstd-safe версии 7.2.4: `Seekable` reads a NULL or out-of-bounds seek table. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует zstd-safe: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (zstd_safe::seekable::SeekTable::frame_decompressed_size, zstd_safe::seekable::Seekable::decompress, zstd_safe::seekable::Seekable::decompress_frame, zstd_safe::seekable::Seekable::frame_decompressed_size, zstd_safe::seekable::Seekable::offset_to_frame_index); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0396
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0396](https://osv.dev/vulnerability/RUSTSEC-2026-0396) · manifest · SHA-256 4530740c3dd2640b5c96ad098b4e771f286dd562d83e8e4aa6214c518b1f08ee_

```
{"id": "RUSTSEC-2026-0396", "aliases": [], "modified": "2026-11-02T09:30:03.400899521Z", "summary": "`Seekable` reads a NULL or out-of-bounds seek table", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (7.4.0, 8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50799 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0397 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0397 для пакета crates.io zstd-safe версии 7.2.4: `OutBuffer::around_pos` exposes uninitialized memory. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует zstd-safe: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (zstd_safe::OutBuffer::around_pos); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0397
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0397](https://osv.dev/vulnerability/RUSTSEC-2026-0397) · manifest · SHA-256 4ad3bc187fa64e24d070e53c5d01373b2aba040ea27757bbf26f8efea74c0967_

```
{"id": "RUSTSEC-2026-0397", "aliases": [], "modified": "2026-11-02T09:30:03.445177143Z", "summary": "`OutBuffer::around_pos` exposes uninitialized memory", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (7.4.0, 8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50800 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0398 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0398 для пакета crates.io zstd-safe версии 7.2.4: `Seekable::decompress` sets a `Vec` length beyond its capacity for offsets past the end. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует zstd-safe: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (zstd_safe::seekable::AdvancedSeekable::decompress, zstd_safe::seekable::Seekable::decompress); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0398
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0398](https://osv.dev/vulnerability/RUSTSEC-2026-0398) · manifest · SHA-256 7e1e8fe35e2578f061734431e3a9558d8cc0dab6043f409c833b43c905bf10d3_

```
{"id": "RUSTSEC-2026-0398", "aliases": [], "modified": "2026-11-02T09:30:03.419709171Z", "summary": "`Seekable::decompress` sets a `Vec` length beyond its capacity for offsets past the end", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (7.4.0, 8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50801 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0399 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0399 для пакета crates.io zstd-safe версии 7.2.4: Use-after-free through `init_using_cdict` and `init_using_ddict`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует zstd-safe: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::init_using_cdict, zstd_safe::DCtx::init_using_ddict); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0399
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0399](https://osv.dev/vulnerability/RUSTSEC-2026-0399) · manifest · SHA-256 58cd19f1b734988f6219b3659cd613c349a5c6693e08cb4e8b9846d1f92bb38f_

```
{"id": "RUSTSEC-2026-0399", "aliases": [], "modified": "2026-11-02T09:30:03.328955732Z", "summary": "Use-after-free through `init_using_cdict` and `init_using_ddict`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (7.4.0, 8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50802 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0400 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0400 для пакета crates.io zstd-safe версии 7.2.4: Use-after-free of a dictionary after a one-shot call on a context with an open stream. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует zstd-safe: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (zstd_safe::DCtx::decompress, zstd_safe::DCtx::decompress_using_ddict, zstd_safe::DCtx::decompress_using_dict); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0400
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0400](https://osv.dev/vulnerability/RUSTSEC-2026-0400) · manifest · SHA-256 00f83f7c4931137d6b18e25256c039f2c52bd627946f5f05f74c2cc7b2615d30_

```
{"id": "RUSTSEC-2026-0400", "aliases": [], "modified": "2026-11-02T09:30:03.428341570Z", "summary": "Use-after-free of a dictionary after a one-shot call on a context with an open stream", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (7.4.0, 8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50803 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0401 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0401 для пакета crates.io zstd-safe версии 7.2.4: Out-of-bounds read in `train_from_buffer` when sample sizes overflow. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует zstd-safe: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (zstd_safe::train_from_buffer); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0401
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0401](https://osv.dev/vulnerability/RUSTSEC-2026-0401) · manifest · SHA-256 dd6e9bd27e75cf4c8d9a5333bbc4dda81ef2f2990271b711f964d6bc829e71fd_

```
{"id": "RUSTSEC-2026-0401", "aliases": [], "modified": "2026-11-02T09:30:03.353698025Z", "summary": "Out-of-bounds read in `train_from_buffer` when sample sizes overflow", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (7.4.0, 8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50804 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0402 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0402 для пакета crates.io zstd-safe версии 7.2.4: Heap buffer overflow in `CCtx::try_clone` on a multithreaded context. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует zstd-safe: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::try_clone); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0402
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0402](https://osv.dev/vulnerability/RUSTSEC-2026-0402) · manifest · SHA-256 464c8c61aa6d0a29b646ba665145c6d256c18786ece14e1921252cecf4a4e54e_

```
{"id": "RUSTSEC-2026-0402", "aliases": [], "modified": "2026-11-02T09:30:04.162155944Z", "summary": "Heap buffer overflow in `CCtx::try_clone` on a multithreaded context", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (7.4.0, 8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50805 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0403 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0403 для пакета crates.io zstd-safe версии 7.2.4: Uninitialized memory exposed when streaming decompression of a legacy frame fails. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует zstd-safe: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (zstd_safe::DCtx::decompress_stream); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0403
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0403](https://osv.dev/vulnerability/RUSTSEC-2026-0403) · manifest · SHA-256 09699f0d23ac15a18937ce02a1b778a246ec661449852b62d6415d8d60ed2147_

```
{"id": "RUSTSEC-2026-0403", "aliases": [], "modified": "2026-11-02T09:30:04.136442771Z", "summary": "Uninitialized memory exposed when streaming decompression of a legacy frame fails", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (7.4.0, 8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50806 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0404 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0404 для пакета crates.io zstd-safe версии 7.2.4: Double free in `DCtx::try_clone`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует zstd-safe: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (zstd_safe::DCtx::try_clone); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0404
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0404](https://osv.dev/vulnerability/RUSTSEC-2026-0404) · manifest · SHA-256 e265647b9f2c582eebfcac7889bee04fada79ea833147205829d693f4c6f8131_

```
{"id": "RUSTSEC-2026-0404", "aliases": [], "modified": "2026-11-02T09:30:04.168804805Z", "summary": "Double free in `DCtx::try_clone`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (7.4.0, 8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50807 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0405 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0405 для пакета crates.io zstd-safe версии 7.2.4: Out-of-bounds read with an out-of-range `InBuffer::pos`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует zstd-safe: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (zstd_safe::seekable::SeekableCStream::compress_stream); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0405
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0405](https://osv.dev/vulnerability/RUSTSEC-2026-0405) · manifest · SHA-256 e784735107b5a74149056e3244a7f30afbcf59892ceaa6d018ec1739be5661d5_

```
{"id": "RUSTSEC-2026-0405", "aliases": [], "modified": "2026-11-02T09:30:03.399517581Z", "summary": "Out-of-bounds read with an out-of-range `InBuffer::pos`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (7.4.0, 8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50808 — zstd-safe 7.2.4 затронут RUSTSEC-2026-0406 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.2.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0406 для пакета crates.io zstd-safe версии 7.2.4: Use-after-free when changing a multithreaded context with an unfinished frame. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует zstd-safe: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::disable_dictionary, zstd_safe::CCtx::init, zstd_safe::CCtx::load_dictionary, zstd_safe::CCtx::ref_cdict, zstd_safe::CCtx::ref_prefix, zstd_safe::CCtx::reset …); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0406
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0406](https://osv.dev/vulnerability/RUSTSEC-2026-0406) · manifest · SHA-256 f08bb0f8849019aa21c995ae08e9c10ff924c83b0464e87d3143ab07935008f5_

```
{"id": "RUSTSEC-2026-0406", "aliases": [], "modified": "2026-11-02T09:30:03.591194710Z", "summary": "Use-after-free when changing a multithreaded context with an unfinished frame", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (7.4.0, 8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50710 — В стороннем коде в дереве: Привилегированные административные функции в scroll-contracts/lib/solmate/src/auth/Owned.sol: transferOwnership

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/lib/solmate/src/auth/Owned.sol`
- Источник данных: scroll-contracts/lib/solmate/src/auth/Owned.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50717 — Привилегированные административные функции в scroll-contracts/src/L1/L1ScrollMessenger.sol: updateMaxReplayTimes

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/L1ScrollMessenger.sol`
- Источник данных: scroll-contracts/src/L1/L1ScrollMessenger.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50719 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol: updateFeeVault, setPause

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol`
- Источник данных: scroll-contracts/src/L1/gateways/EnforcedTxGateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50720 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/L1CustomERC20Gateway.sol: updateTokenMapping

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/L1CustomERC20Gateway.sol`
- Источник данных: scroll-contracts/src/L1/gateways/L1CustomERC20Gateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50721 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/L1ERC1155Gateway.sol: updateTokenMapping

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/L1ERC1155Gateway.sol`
- Источник данных: scroll-contracts/src/L1/gateways/L1ERC1155Gateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50722 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/L1ERC721Gateway.sol: updateTokenMapping

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/L1ERC721Gateway.sol`
- Источник данных: scroll-contracts/src/L1/gateways/L1ERC721Gateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50723 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/L1GatewayRouter.sol: setETHGateway, setDefaultERC20Gateway, setERC20Gateway

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/L1GatewayRouter.sol`
- Источник данных: scroll-contracts/src/L1/gateways/L1GatewayRouter.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50724 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/usdc/L1USDCGateway.sol: updateCircleCaller, pauseDeposit, pauseWithdraw

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/usdc/L1USDCGateway.sol`
- Источник данных: scroll-contracts/src/L1/gateways/usdc/L1USDCGateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50725 — Привилегированные административные функции в scroll-contracts/src/L1/gateways/usdc/draft-L1USDCGatewayCCTP.sol: updateCCTPContracts

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/gateways/usdc/draft-L1USDCGatewayCCTP.sol`
- Источник данных: scroll-contracts/src/L1/gateways/usdc/draft-L1USDCGatewayCCTP.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50726 — Привилегированные административные функции в scroll-contracts/src/L1/rollup/L1MessageQueue.sol: updateGasOracle, updateMaxGasLimit

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/rollup/L1MessageQueue.sol`
- Источник данных: scroll-contracts/src/L1/rollup/L1MessageQueue.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50727 — Привилегированные административные функции в scroll-contracts/src/L1/rollup/L1MessageQueueWithGasPriceOracle.sol: updateWhitelistChecker

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/rollup/L1MessageQueueWithGasPriceOracle.sol`
- Источник данных: scroll-contracts/src/L1/rollup/L1MessageQueueWithGasPriceOracle.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50728 — Привилегированные административные функции в scroll-contracts/src/L1/rollup/L2GasPriceOracle.sol: updateWhitelist, setIntrinsicParams

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/rollup/L2GasPriceOracle.sol`
- Источник данных: scroll-contracts/src/L1/rollup/L2GasPriceOracle.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50729 — Привилегированные административные функции в scroll-contracts/src/L1/rollup/MultipleVersionRollupVerifier.sol: updateVerifier

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/rollup/MultipleVersionRollupVerifier.sol`
- Источник данных: scroll-contracts/src/L1/rollup/MultipleVersionRollupVerifier.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50730 — Привилегированные административные функции в scroll-contracts/src/L1/rollup/ScrollChain.sol: revertBatch, finalizeEuclidInitialBatch, addSequencer, removeSequencer, addProver, removeProver, updateMaxNumTxInChunk, setPause

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L1/rollup/ScrollChain.sol`
- Источник данных: scroll-contracts/src/L1/rollup/ScrollChain.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50732 — Привилегированные административные функции в scroll-contracts/src/L2/gateways/L2ERC1155Gateway.sol: updateTokenMapping

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/gateways/L2ERC1155Gateway.sol`
- Источник данных: scroll-contracts/src/L2/gateways/L2ERC1155Gateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50733 — Привилегированные административные функции в scroll-contracts/src/L2/gateways/L2ERC721Gateway.sol: updateTokenMapping

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/gateways/L2ERC721Gateway.sol`
- Источник данных: scroll-contracts/src/L2/gateways/L2ERC721Gateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50734 — Привилегированные административные функции в scroll-contracts/src/L2/gateways/L2GatewayRouter.sol: setETHGateway, setDefaultERC20Gateway, setERC20Gateway

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/gateways/L2GatewayRouter.sol`
- Источник данных: scroll-contracts/src/L2/gateways/L2GatewayRouter.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50735 — Привилегированные административные функции в scroll-contracts/src/L2/gateways/usdc/L2USDCGateway.sol: updateCircleCaller, pauseDeposit, pauseWithdraw

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/gateways/usdc/L2USDCGateway.sol`
- Источник данных: scroll-contracts/src/L2/gateways/usdc/L2USDCGateway.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50736 — Привилегированные административные функции в scroll-contracts/src/L2/gateways/usdc/draft-L2USDCGatewayCCTP.sol: updateCCTPContracts

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/gateways/usdc/draft-L2USDCGatewayCCTP.sol`
- Источник данных: scroll-contracts/src/L2/gateways/usdc/draft-L2USDCGatewayCCTP.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50737 — Привилегированные административные функции в scroll-contracts/src/L2/predeploys/L1BlockContainer.sol: initialize, updateWhitelist

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/predeploys/L1BlockContainer.sol`
- Источник данных: scroll-contracts/src/L2/predeploys/L1BlockContainer.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50738 — Привилегированные административные функции в scroll-contracts/src/L2/predeploys/L1GasPriceOracle.sol: setOverhead, setScalar, setCommitScalar, setBlobScalar, updateWhitelist, enableCurie

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/predeploys/L1GasPriceOracle.sol`
- Источник данных: scroll-contracts/src/L2/predeploys/L1GasPriceOracle.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50739 — Привилегированные административные функции в scroll-contracts/src/L2/predeploys/L2MessageQueue.sol: initialize

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/predeploys/L2MessageQueue.sol`
- Источник данных: scroll-contracts/src/L2/predeploys/L2MessageQueue.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50740 — Привилегированные административные функции в scroll-contracts/src/L2/predeploys/L2TxFeeVault.sol: updateMessenger, updateRecipient, updateMinWithdrawAmount

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/predeploys/L2TxFeeVault.sol`
- Источник данных: scroll-contracts/src/L2/predeploys/L2TxFeeVault.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50741 — Привилегированные административные функции в scroll-contracts/src/L2/predeploys/Whitelist.sol: updateWhitelistStatus

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/L2/predeploys/Whitelist.sol`
- Источник данных: scroll-contracts/src/L2/predeploys/Whitelist.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50743 — Привилегированные административные функции в scroll-contracts/src/gas-swap/GasSwap.sol: withdraw, updateFeeRatio, updateApprovedTarget

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/gas-swap/GasSwap.sol`
- Источник данных: scroll-contracts/src/gas-swap/GasSwap.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50744 — Привилегированные административные функции в scroll-contracts/src/libraries/ScrollMessengerBase.sol: updateFeeVault, setPause

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/libraries/ScrollMessengerBase.sol`
- Источник данных: scroll-contracts/src/libraries/ScrollMessengerBase.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50745 — Привилегированные административные функции в scroll-contracts/src/libraries/common/OwnableBase.sol: renounceOwnership, transferOwnership

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/libraries/common/OwnableBase.sol`
- Источник данных: scroll-contracts/src/libraries/common/OwnableBase.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50747 — Привилегированные административные функции в scroll-contracts/src/libraries/token/ScrollStandardERC20Factory.sol: deployL2Token

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/libraries/token/ScrollStandardERC20Factory.sol`
- Источник данных: scroll-contracts/src/libraries/token/ScrollStandardERC20Factory.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50749 — Привилегированные административные функции в scroll-contracts/src/lido/LidoGatewayManager.sol: grantRole, revokeRole

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/lido/LidoGatewayManager.sol`
- Источник данных: scroll-contracts/src/lido/LidoGatewayManager.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50750 — Привилегированные административные функции в scroll-contracts/src/misc/Fallback.sol: withdraw, execute

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/misc/Fallback.sol`
- Источник данных: scroll-contracts/src/misc/Fallback.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50751 — Привилегированные административные функции в scroll-contracts/src/rate-limiter/ETHRateLimiter.sol: updateTotalLimit

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:scroll-contracts/src/rate-limiter/ETHRateLimiter.sol`
- Источник данных: scroll-contracts/src/rate-limiter/ETHRateLimiter.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50711 — В стороннем коде в дереве: Прямое использование ecrecover в scroll-contracts/lib/solmate/src/tokens/ERC20.sol

- Серьёзность: **Информационная** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:scroll-contracts/lib/solmate/src/tokens/ERC20.sol`
- Источник данных: scroll-contracts/lib/solmate/src/tokens/ERC20.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 35.9 / 100
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

### QSI-2026-50816 — github.com/docker/docker v26.1.0+incompatible затронут GHSA-4vq8-7jfc-9cvp (CVE-2025-54410)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 35.2 / 100
- CVSS v3.1: 3.3 (`CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:U/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-4vq8-7jfc-9cvp (CVE-2025-54410) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Moby firewalld reload removes bridge network isolation. github.com/docker/docker не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (25.0.13, 28.0.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50817 — github.com/docker/docker v26.1.0+incompatible затронут GHSA-pxq6-2prw-chj9 (CVE-2026-33997, GO-2026-4883)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 35.2 / 100
- CVSS v3.1: 6.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-pxq6-2prw-chj9 (CVE-2026-33997, GO-2026-4883) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Moby has an Off-by-one error in its plugin privilege validation. Сборка продукта включает github.com/docker/docker, но govulncheck не нашёл импорта ни одного затронутого пакета: к поставляемому коду бюллетень не применим.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50818 — github.com/docker/docker v26.1.0+incompatible затронут GHSA-rg2x-37c3-w2rh (CVE-2026-42306, GO-2026-5617)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 35.2 / 100
- CVSS v3.1: 7.2 (`CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:N/I:H/A:H`)

OSV.dev сообщает GHSA-rg2x-37c3-w2rh (CVE-2026-42306, GO-2026-5617) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Docker: Race condition in docker cp allows bind mount redirection to host path. Сборка продукта включает github.com/docker/docker, но govulncheck не нашёл импорта ни одного затронутого пакета: к поставляемому коду бюллетень не применим.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50819 — github.com/docker/docker v26.1.0+incompatible затронут GHSA-v23v-6jw2-98fq (CVE-2024-41110, GO-2024-3005)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 35.2 / 100
- CVSS v3.1: 9.9 (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:C/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-v23v-6jw2-98fq (CVE-2024-41110, GO-2024-3005) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Authz zero length regression. Сборка продукта включает github.com/docker/docker, но govulncheck не нашёл импорта ни одного затронутого пакета: к поставляемому коду бюллетень не применим.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (23.0.15, 25.0.6, 26.1.5, 27.1.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50820 — github.com/docker/docker v26.1.0+incompatible затронут GHSA-vp62-88p7-qqf5 (CVE-2026-41568, GO-2026-5668)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 35.2 / 100
- CVSS v3.1: 6.1 (`CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:N/I:L/A:H`)

OSV.dev сообщает GHSA-vp62-88p7-qqf5 (CVE-2026-41568, GO-2026-5668) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Docker: Race condition in docker cp allows creation of arbitrary empty files on the host via symlink swap. Сборка продукта включает github.com/docker/docker, но govulncheck не нашёл импорта ни одного затронутого пакета: к поставляемому коду бюллетень не применим.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50821 — github.com/docker/docker v26.1.0+incompatible затронут GHSA-x86f-5xw2-fm2r (CVE-2026-41567, GO-2026-5746)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 35.2 / 100
- CVSS v3.1: 7.2 (`CVSS:3.1/AV:L/AC:H/PR:L/UI:R/S:C/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-x86f-5xw2-fm2r (CVE-2026-41567, GO-2026-5746) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Docker: `PUT /containers/{id}/archive` executes container binary on the host. Сборка продукта включает github.com/docker/docker, но govulncheck не нашёл импорта ни одного затронутого пакета: к поставляемому коду бюллетень не применим.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50824 — github.com/jackc/pgx/v5 v5.5.4 затронут GHSA-9jj7-4m8r-rfcm (CVE-2026-33816, GO-2026-4772)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/jackc/pgx/v5@v5.5.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 35.2 / 100
- CVSS v3.1: 9.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-9jj7-4m8r-rfcm (CVE-2026-33816, GO-2026-4772) для пакета Go github.com/jackc/pgx/v5 версии v5.5.4: Memory-safety vulnerability in github.com/jackc/pgx/v5. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (5.9.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50826 — github.com/jackc/pgx/v5 v5.5.4 затронут GHSA-xgrm-4fwx-7qm8 (CVE-2026-33815, GO-2026-4771)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/jackc/pgx/v5@v5.5.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 35.2 / 100
- CVSS v3.1: 9.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-xgrm-4fwx-7qm8 (CVE-2026-33815, GO-2026-4771) для пакета Go github.com/jackc/pgx/v5 версии v5.5.4: pgx contains memory-safety vulnerability. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (5.9.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50709 — В стороннем коде в дереве: Плавающая версия компилятора (>=0.8.0) в 20 файл(ах)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.8.0`
- Источник данных: scroll-contracts/lib/solmate/src/auth/Auth.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 29.8 / 100
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

### QSI-2026-50811 — github.com/btcsuite/btcd v0.20.1-beta затронут GHSA-27vh-h6mc-q6g8 (CVE-2024-38365, GO-2024-3189)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/btcsuite/btcd@v0.20.1-beta`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 7.4 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H`)

OSV.dev сообщает GHSA-27vh-h6mc-q6g8 (CVE-2024-38365, GO-2024-3189) для пакета Go github.com/btcsuite/btcd версии v0.20.1-beta: btcd did not correctly re-implement Bitcoin Core's "FindAndDelete()" functionality. github.com/btcsuite/btcd не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-27vh-h6mc-q6g8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-27vh-h6mc-q6g8](https://osv.dev/vulnerability/GHSA-27vh-h6mc-q6g8) · line 26 · SHA-256 aad45df9ea24ed9cb0025b159b66f7504dba04005332fd66de0b07a5deb64e7e_

```
{"id": "GHSA-27vh-h6mc-q6g8", "aliases": ["CVE-2024-38365", "GO-2024-3189"], "modified": "2025-08-21T04:05:13Z", "summary": "btcd did not correctly re-implement Bitcoin Core's \"FindAndDelete()\" functionality", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:H/A:H"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.24.2-beta.rc1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50812 — github.com/btcsuite/btcd v0.20.1-beta затронут GHSA-2chg-86hq-7w38 (CVE-2022-44797, GO-2022-1098)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/btcsuite/btcd@v0.20.1-beta`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 9.8 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-2chg-86hq-7w38 (CVE-2022-44797, GO-2022-1098) для пакета Go github.com/btcsuite/btcd версии v0.20.1-beta: btcd mishandles witness size checking. github.com/btcsuite/btcd не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2chg-86hq-7w38
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2chg-86hq-7w38](https://osv.dev/vulnerability/GHSA-2chg-86hq-7w38) · line 26 · SHA-256 934555a4169a908193bc80baf88a2a7d73b6df756a423d5fbf8e3a5b8c1264b7_

```
{"id": "GHSA-2chg-86hq-7w38", "aliases": ["CVE-2022-44797", "GO-2022-1098"], "modified": "2024-05-20T21:36:55Z", "summary": "btcd mishandles witness size checking", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.23.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50813 — github.com/btcsuite/btcd v0.20.1-beta затронут GHSA-3jgf-r68h-xfqm (CVE-2024-34478, GO-2024-2818)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/btcsuite/btcd@v0.20.1-beta`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3jgf-r68h-xfqm (CVE-2024-34478, GO-2024-2818) для пакета Go github.com/btcsuite/btcd версии v0.20.1-beta: btcd susceptible to consensus failures. github.com/btcsuite/btcd не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3jgf-r68h-xfqm
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3jgf-r68h-xfqm](https://osv.dev/vulnerability/GHSA-3jgf-r68h-xfqm) · line 26 · SHA-256 92991e69119721eebd4a44773bcf6428311d44a55b1a748067b4c51c8ae0e1a2_

```
{"id": "GHSA-3jgf-r68h-xfqm", "aliases": ["CVE-2024-34478", "GO-2024-2818"], "modified": "2024-08-07T19:55:49Z", "summary": "btcd susceptible to consensus failures", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.24.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50815 — github.com/docker/cli v25.0.4-0.20240305161310-2bf4225ad269+incompatible затронут GHSA-p436-gjf2-799p (CVE-2025-15558, GO-2026-4610)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/docker/cli@v25.0.4-0.20240305161310-2bf4225ad269+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-p436-gjf2-799p (CVE-2025-15558, GO-2026-4610) для пакета Go github.com/docker/cli версии v25.0.4-0.20240305161310-2bf4225ad269+incompatible: Docker CLI Plugins: Uncontrolled Search Path Element Leads to Local Privilege Escalation on Windows. github.com/docker/cli не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-p436-gjf2-799p
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-p436-gjf2-799p](https://osv.dev/vulnerability/GHSA-p436-gjf2-799p) · line 38 · SHA-256 9e7463cc51241d7d54cd03576b6471e4049378946386d026292f941726799a7a_

```
{"id": "GHSA-p436-gjf2-799p", "aliases": ["BIT-docker-cli-2025-15558", "CVE-2025-15558", "GO-2026-4610"], "modified": "2026-09-10T03:50:39.956404854Z", "summary": "Docker CLI Plugins: Uncontrolled Search Path Element Leads to Local Privilege Escalation on Windows", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (29.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50827 — github.com/klauspost/compress v1.17.9 затронут GHSA-259r-337f-4rfw (CVE-2026-63209, GO-2026-5841)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/klauspost/compress@v1.17.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-259r-337f-4rfw (CVE-2026-63209, GO-2026-5841) для пакета Go github.com/klauspost/compress версии v1.17.9: Compress/s2: Integer Overflow or Wraparound and Out-of-bounds Write in compress. Сборка продукта включает github.com/klauspost/compress, но govulncheck не нашёл импорта ни одного затронутого пакета: к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-259r-337f-4rfw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-259r-337f-4rfw](https://osv.dev/vulnerability/GHSA-259r-337f-4rfw) · line 68 · SHA-256 e6c57fd94c9c9b3c584e2538b60d5c2e56f5af7ee56e91b0fec61f04bf868019_

```
{"id": "GHSA-259r-337f-4rfw", "aliases": ["CVE-2026-63209", "GO-2026-5841"], "modified": "2026-10-20T14:45:03.782718646Z", "summary": "Compress/s2: Integer Overflow or Wraparound and Out-of-bounds Write in compress", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.18.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50829 — golang.org/x/crypto v0.32.0 затронут GHSA-45gg-vh54-h5m9 (CVE-2026-39828, GO-2026-5014)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 6.3 (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L`)

OSV.dev сообщает GHSA-45gg-vh54-h5m9 (CVE-2026-39828, GO-2026-5014) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto vulnerable to invoking bypass of certificate restrictions. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-45gg-vh54-h5m9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-45gg-vh54-h5m9](https://osv.dev/vulnerability/GHSA-45gg-vh54-h5m9) · line 111 · SHA-256 3ae25d8e675d3cd931a189040f5a83188ab1f3abb9dda4489467e5f0495ee6b1_

```
{"id": "GHSA-45gg-vh54-h5m9", "aliases": ["CVE-2026-39828", "GO-2026-5014"], "modified": "2026-09-10T03:51:07.761861882Z", "summary": "golang.org/x/crypto vulnerable to invoking bypass of certificate restrictions", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.52.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50830 — golang.org/x/crypto v0.32.0 затронут GHSA-5cgq-3rg8-m6cv (CVE-2026-42508, GO-2026-5021)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 9.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-5cgq-3rg8-m6cv (CVE-2026-42508, GO-2026-5021) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto vulnerable to auth bypass via unenforced @revoked status. Сборка продукта включает golang.org/x/crypto, но govulncheck не нашёл импорта ни одного затронутого пакета: к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5cgq-3rg8-m6cv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-5cgq-3rg8-m6cv](https://osv.dev/vulnerability/GHSA-5cgq-3rg8-m6cv) · line 111 · SHA-256 c210a3eb646370a68fa71187380de5b1b5863fd4075692308b50f1b437448671_

```
{"id": "GHSA-5cgq-3rg8-m6cv", "aliases": ["CVE-2026-42508", "GO-2026-5021"], "modified": "2026-09-10T03:50:48.271021372Z", "summary": "golang.org/x/crypto vulnerable to auth bypass via unenforced @revoked status", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.52.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50831 — golang.org/x/crypto v0.32.0 затронут GHSA-78mq-xcr3-xm33 (CVE-2026-39835, GO-2026-5015)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-78mq-xcr3-xm33 (CVE-2026-39835, GO-2026-5015) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto is vulnerable to invoking server panic during CheckHostKey/Authenticate flow. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-78mq-xcr3-xm33
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-78mq-xcr3-xm33](https://osv.dev/vulnerability/GHSA-78mq-xcr3-xm33) · line 111 · SHA-256 2324f204b71432fd7cb52ac18140c5840e16dfdf265320d924d12818be330235_

```
{"id": "GHSA-78mq-xcr3-xm33", "aliases": ["CVE-2026-39835", "GO-2026-5015"], "modified": "2026-09-11T15:45:36.488635295Z", "summary": "golang.org/x/crypto is vulnerable to invoking server panic during CheckHostKey/Authenticate flow", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.52.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50832 — golang.org/x/crypto v0.32.0 затронут GHSA-89gr-r52h-f8rx (CVE-2026-39831, GO-2026-5019)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 9.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-89gr-r52h-f8rx (CVE-2026-39831, GO-2026-5019) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto: FIDO/U2F security key physical presence check can be bypassed. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-89gr-r52h-f8rx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-89gr-r52h-f8rx](https://osv.dev/vulnerability/GHSA-89gr-r52h-f8rx) · line 111 · SHA-256 e91adcdab498357c45e1e5aae13033566fe7ce8344fa138549d03364c02a63b4_

```
{"id": "GHSA-89gr-r52h-f8rx", "aliases": ["CVE-2026-39831", "GO-2026-5019"], "modified": "2026-09-10T03:50:48.773810556Z", "summary": "golang.org/x/crypto: FIDO/U2F security key physical presence check can be bypassed", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.52.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50836 — golang.org/x/crypto v0.32.0 затронут GHSA-hcg3-q754-cr77 (CVE-2025-22869, GO-2025-3487)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-hcg3-q754-cr77 (CVE-2025-22869, GO-2025-3487) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto Vulnerable to Denial of Service (DoS) via Slow or Incomplete Key Exchange. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hcg3-q754-cr77
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-hcg3-q754-cr77](https://osv.dev/vulnerability/GHSA-hcg3-q754-cr77) · line 111 · SHA-256 f303738ce96439e4c8316d21f686a5cecf335b367bd9d80e77aeef2b204f5caa_

```
{"id": "GHSA-hcg3-q754-cr77", "aliases": ["CVE-2025-22869", "GO-2025-3487"], "modified": "2026-09-10T03:50:23.913440018Z", "summary": "golang.org/x/crypto Vulnerable to Denial of Service (DoS) via Slow or Incomplete Key Exchange", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.35.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50837 — golang.org/x/crypto v0.32.0 затронут GHSA-j5w8-q4qc-rx2x (CVE-2025-58181, GO-2025-4134)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-j5w8-q4qc-rx2x (CVE-2025-58181, GO-2025-4134) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto/ssh allows an attacker to cause unbounded memory consumption. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j5w8-q4qc-rx2x
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j5w8-q4qc-rx2x](https://osv.dev/vulnerability/GHSA-j5w8-q4qc-rx2x) · line 111 · SHA-256 f8d1d00909e44bf5ef2c034138d296fc86fac2a46f6cf9c0098b0cd595495b82_

```
{"id": "GHSA-j5w8-q4qc-rx2x", "aliases": ["CVE-2025-58181", "GO-2025-4134"], "modified": "2026-09-10T03:50:30.983878807Z", "summary": "golang.org/x/crypto/ssh allows an attacker to cause unbounded memory consumption", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.45.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50839 — golang.org/x/crypto v0.32.0 затронут GHSA-q4h4-gmj2-qvw2 (CVE-2026-46597, GO-2026-5013)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-q4h4-gmj2-qvw2 (CVE-2026-46597, GO-2026-5013) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto: Invoking byte arithmetic causes underflow and panic. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-q4h4-gmj2-qvw2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-q4h4-gmj2-qvw2](https://osv.dev/vulnerability/GHSA-q4h4-gmj2-qvw2) · line 111 · SHA-256 e22588c34a52695e292acb0fa8ca09d16f11a52ec3e57cf4eb14bb334cc43487_

```
{"id": "GHSA-q4h4-gmj2-qvw2", "aliases": ["CVE-2026-46597", "GO-2026-5013"], "modified": "2026-09-10T03:50:50.202568323Z", "summary": "golang.org/x/crypto: Invoking byte arithmetic causes underflow and panic", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.52.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50840 — golang.org/x/crypto v0.32.0 затронут GHSA-qpw4-5x99-6vjp (CVE-2026-39827, GO-2026-5016)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-qpw4-5x99-6vjp (CVE-2026-39827, GO-2026-5016) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto: Invoking memory leak when rejecting channels can lead to DoS. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qpw4-5x99-6vjp
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qpw4-5x99-6vjp](https://osv.dev/vulnerability/GHSA-qpw4-5x99-6vjp) · line 111 · SHA-256 0a1a57b1f34f031af84f7c80faafc461ef40056e1d6534fa95bf87a6ccba797b_

```
{"id": "GHSA-qpw4-5x99-6vjp", "aliases": ["CVE-2026-39827", "GO-2026-5016"], "modified": "2026-09-10T03:50:50.295705701Z", "summary": "golang.org/x/crypto: Invoking memory leak when rejecting channels can lead to DoS", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.52.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50841 — golang.org/x/crypto v0.32.0 затронут GHSA-rm3j-f69w-wqmq (CVE-2026-39834, GO-2026-5020)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 9.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H`)

OSV.dev сообщает GHSA-rm3j-f69w-wqmq (CVE-2026-39834, GO-2026-5020) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto vulnerable to infinite loop on large channel writes. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rm3j-f69w-wqmq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rm3j-f69w-wqmq](https://osv.dev/vulnerability/GHSA-rm3j-f69w-wqmq) · line 111 · SHA-256 434f5c9970e2d2e59fffeb71f0238112aa0b33bfadfa53581d59df3b87daddae_

```
{"id": "GHSA-rm3j-f69w-wqmq", "aliases": ["CVE-2026-39834", "GO-2026-5020"], "modified": "2026-09-10T03:50:50.499928973Z", "summary": "golang.org/x/crypto vulnerable to infinite loop on large channel writes", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.52.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50842 — golang.org/x/crypto v0.32.0 затронут GHSA-vgwf-h737-ff37 (CVE-2026-39830, GO-2026-5017)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 9.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H`)

OSV.dev сообщает GHSA-vgwf-h737-ff37 (CVE-2026-39830, GO-2026-5017) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto: Invoking client can cause server deadlock on unexpected responses. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vgwf-h737-ff37
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vgwf-h737-ff37](https://osv.dev/vulnerability/GHSA-vgwf-h737-ff37) · line 111 · SHA-256 5df97ecf16d199b43056669f8c4d272817f843a810aae4f0d5e2745288658b3e_

```
{"id": "GHSA-vgwf-h737-ff37", "aliases": ["CVE-2026-39830", "GO-2026-5017"], "modified": "2026-09-15T12:45:34.863978347Z", "summary": "golang.org/x/crypto: Invoking client can cause server deadlock on unexpected responses", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.52.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50844 — golang.org/x/crypto v0.32.0 затронут GHSA-x527-x647-q7gg (CVE-2026-46595)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 10.0 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L`)

OSV.dev сообщает GHSA-x527-x647-q7gg (CVE-2026-46595) для пакета Go golang.org/x/crypto версии v0.32.0: golang.org/x/crypto: Invoking VerifiedPublicKeyCallback permissions skip enforcement. golang.org/x/crypto не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-x527-x647-q7gg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-x527-x647-q7gg](https://osv.dev/vulnerability/GHSA-x527-x647-q7gg) · line 111 · SHA-256 1e71c185d81f7f0c837e9fce57f0c1ea1c342c1b663f1e3ee7958cfc44ff4976_

```
{"id": "GHSA-x527-x647-q7gg", "aliases": ["CVE-2026-46595", "GO-2026-5023"], "modified": "2026-09-10T03:50:51.157351033Z", "summary": "golang.org/x/crypto: Invoking VerifiedPublicKeyCallback permissions skip enforcement", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.52.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50849 — golang.org/x/net v0.25.0 затронут GHSA-5cv4-jp36-h3mw (CVE-2026-25680, GO-2026-5028)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-5cv4-jp36-h3mw (CVE-2026-25680, GO-2026-5028) для пакета Go golang.org/x/net версии v0.25.0: Go Net HTML parser is vulnerable to denial of service. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5cv4-jp36-h3mw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-5cv4-jp36-h3mw](https://osv.dev/vulnerability/GHSA-5cv4-jp36-h3mw) · line 112 · SHA-256 9eb940a510edc67a0602da898a09dec5f6df07648ae4055c09b64e227fafa40d_

```
{"id": "GHSA-5cv4-jp36-h3mw", "aliases": ["CVE-2026-25680", "GO-2026-5028"], "modified": "2026-09-10T03:50:45.494180024Z", "summary": "Go Net HTML parser is vulnerable to denial of service", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.55.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50850 — golang.org/x/net v0.25.0 затронут GHSA-qxp5-gwg8-xv66 (CVE-2025-22870, GO-2025-3503)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 4.4 (`CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:L`)

OSV.dev сообщает GHSA-qxp5-gwg8-xv66 (CVE-2025-22870, GO-2025-3503) для пакета Go golang.org/x/net версии v0.25.0: HTTP Proxy bypass using IPv6 Zone IDs in golang.org/x/net. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qxp5-gwg8-xv66
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qxp5-gwg8-xv66](https://osv.dev/vulnerability/GHSA-qxp5-gwg8-xv66) · line 112 · SHA-256 80c439bfcabcd34c2204066f529bba29e9557b78460115cf2b65cc8aa76db117_

```
{"id": "GHSA-qxp5-gwg8-xv66", "aliases": ["CVE-2025-22870", "GO-2025-3503"], "modified": "2026-09-10T03:50:23.280114085Z", "summary": "HTTP Proxy bypass using IPv6 Zone IDs in golang.org/x/net", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.36.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50872 — github.com/containerd/containerd v1.7.12 затронут GHSA-265r-hfxg-fhmg (CVE-2024-40635, GO-2025-3528)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/containerd/containerd@v1.7.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 4.6 (`CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:L/A:N`)

OSV.dev сообщает GHSA-265r-hfxg-fhmg (CVE-2024-40635, GO-2025-3528) для пакета Go github.com/containerd/containerd версии v1.7.12: containerd has an integer overflow in User ID handling. github.com/containerd/containerd не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-265r-hfxg-fhmg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-265r-hfxg-fhmg](https://osv.dev/vulnerability/GHSA-265r-hfxg-fhmg) · line 64 · SHA-256 e1ad0048b05791818710141cf5b0095ff6caf410451399fa44ec6cb6a14b3e67_

```
{"id": "GHSA-265r-hfxg-fhmg", "aliases": ["CVE-2024-40635", "GO-2025-3528"], "modified": "2026-09-10T03:50:06.145474067Z", "summary": "containerd has an integer overflow in User ID handling", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:C/C:L/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.6.38, 1.7.27).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50873 — github.com/containerd/containerd v1.7.12 затронут GHSA-7jxh-36q5-gcqv (CVE-2026-53495, GO-2026-6444)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/containerd/containerd@v1.7.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7jxh-36q5-gcqv (CVE-2026-53495, GO-2026-6444) для пакета Go github.com/containerd/containerd версии v1.7.12: containerd: CRI ExecSync Goroutine Leak Leads to Node-Level Denial of Service. github.com/containerd/containerd не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7jxh-36q5-gcqv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7jxh-36q5-gcqv](https://osv.dev/vulnerability/GHSA-7jxh-36q5-gcqv) · line 64 · SHA-256 ab014eb7139668b9c697a22164b7df778ba18dc63b39d03dbe2111c4accda880_

```
{"id": "GHSA-7jxh-36q5-gcqv", "aliases": ["CVE-2026-53495", "GO-2026-6444"], "modified": "2026-09-17T17:40:55.122822852Z", "summary": "containerd: CRI ExecSync Goroutine Leak Leads to Node-Level Denial of Service", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.7.35).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50874 — github.com/containerd/containerd v1.7.12 затронут GHSA-jpcc-p29g-p8mq (CVE-2026-47262, GO-2026-5475)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/containerd/containerd@v1.7.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-jpcc-p29g-p8mq (CVE-2026-47262, GO-2026-5475) для пакета Go github.com/containerd/containerd версии v1.7.12: containerd image-triggered runtime DoS via unbounded group parsing. github.com/containerd/containerd не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-jpcc-p29g-p8mq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-jpcc-p29g-p8mq](https://osv.dev/vulnerability/GHSA-jpcc-p29g-p8mq) · line 64 · SHA-256 814ff0b6c5bcf171eeb6d529d9bf2fe8591d3461ce8d65c9c9e84acff96b331d_

```
{"id": "GHSA-jpcc-p29g-p8mq", "aliases": ["CVE-2026-47262", "GO-2026-5475"], "modified": "2026-09-10T03:50:50.032144703Z", "summary": "containerd image-triggered runtime DoS via unbounded group parsing", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.7.33).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50875 — github.com/containerd/containerd v1.7.12 затронут GHSA-m6hq-p25p-ffr2 (CVE-2025-64329, GO-2025-4108)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/containerd/containerd@v1.7.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-m6hq-p25p-ffr2 (CVE-2025-64329, GO-2025-4108) для пакета Go github.com/containerd/containerd версии v1.7.12: containerd CRI server: Host memory exhaustion through Attach goroutine leak. github.com/containerd/containerd не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-m6hq-p25p-ffr2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-m6hq-p25p-ffr2](https://osv.dev/vulnerability/GHSA-m6hq-p25p-ffr2) · line 64 · SHA-256 f06809086abb2f1475884aacfbadb0c83391da8e55041f2b5476002d023632c7_

```
{"id": "GHSA-m6hq-p25p-ffr2", "aliases": ["CVE-2025-64329", "GO-2025-4108"], "modified": "2026-09-10T03:50:58.362479211Z", "summary": "containerd CRI server: Host memory exhaustion through Attach goroutine leak", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.7.29).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50876 — github.com/containerd/containerd v1.7.12 затронут GHSA-pg57-6jwg-q645 (CVE-2026-53493, GO-2026-6597)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/containerd/containerd@v1.7.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-pg57-6jwg-q645 (CVE-2026-53493, GO-2026-6597) для пакета Go github.com/containerd/containerd версии v1.7.12: Containerd has image-pull DoS via crafted OCI index graph amplification. github.com/containerd/containerd не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pg57-6jwg-q645
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pg57-6jwg-q645](https://osv.dev/vulnerability/GHSA-pg57-6jwg-q645) · line 64 · SHA-256 eb374cbf8922062776520589dffca362f074d1dc478f2860f638953c2ce01efe_

```
{"id": "GHSA-pg57-6jwg-q645", "aliases": ["CVE-2026-53493", "GO-2026-6597"], "modified": "2026-10-01T20:55:46.094271282Z", "summary": "Containerd has image-pull DoS via crafted OCI index graph amplification", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.7.36).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50877 — github.com/containerd/containerd v1.7.12 затронут GHSA-pwhc-rpq9-4c8w (CVE-2024-25621, GO-2025-4100)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/containerd/containerd@v1.7.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 7.3 (`CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-pwhc-rpq9-4c8w (CVE-2024-25621, GO-2025-4100) для пакета Go github.com/containerd/containerd версии v1.7.12: containerd affected by a local privilege escalation via wide permissions on CRI directory. github.com/containerd/containerd не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pwhc-rpq9-4c8w
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pwhc-rpq9-4c8w](https://osv.dev/vulnerability/GHSA-pwhc-rpq9-4c8w) · line 64 · SHA-256 e41d2cd80807bc3b7314dc6b1c1e0a56f7df82e3be2fcc0f9ed17e1ab4be07f4_

```
{"id": "GHSA-pwhc-rpq9-4c8w", "aliases": ["CVE-2024-25621", "GO-2025-4100"], "modified": "2026-09-10T03:50:58.430975281Z", "summary": "containerd affected by a local privilege escalation via wide permissions on CRI directory", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:L/UI:R/S:U/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.7.29).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50878 — github.com/containerd/containerd v1.7.12 затронут GHSA-rp3h-jf77-q9p4 (CVE-2026-95838, GO-2026-6796)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/containerd/containerd@v1.7.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-rp3h-jf77-q9p4 (CVE-2026-95838, GO-2026-6796) для пакета Go github.com/containerd/containerd версии v1.7.12: containerd: Unpack DoS via repeated opaque whiteouts. github.com/containerd/containerd не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rp3h-jf77-q9p4
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rp3h-jf77-q9p4](https://osv.dev/vulnerability/GHSA-rp3h-jf77-q9p4) · line 64 · SHA-256 645841425a190a576445b1fd9a95e8dc48070f03a1a7ccd1221b24cd228201b9_

```
{"id": "GHSA-rp3h-jf77-q9p4", "aliases": ["CVE-2026-95838", "GO-2026-6796"], "modified": "2026-10-19T21:40:52.337183596Z", "summary": "containerd: Unpack DoS via repeated opaque whiteouts", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:A/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.7.35).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50879 — github.com/containerd/containerd v1.7.12 затронут GHSA-xhf5-7wjv-pqxp (CVE-2026-53488, GO-2026-5758)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/containerd/containerd@v1.7.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-xhf5-7wjv-pqxp (CVE-2026-53488, GO-2026-5758) для пакета Go github.com/containerd/containerd версии v1.7.12: containerd CRI — image-config `LABEL` flows to restart-monitor `binary://` logger: host-root command execution from an image pull. github.com/containerd/containerd не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xhf5-7wjv-pqxp
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xhf5-7wjv-pqxp](https://osv.dev/vulnerability/GHSA-xhf5-7wjv-pqxp) · line 64 · SHA-256 1f65b336b14adde7861933d0a67c208a1f77ea4299ebc36ed82e76005e4e9883_

```
{"id": "GHSA-xhf5-7wjv-pqxp", "aliases": ["CVE-2026-53488", "GO-2026-5758"], "modified": "2026-09-10T03:51:09.792384728Z", "summary": "containerd CRI — image-config `LABEL` flows to restart-monitor `binary://` logger: host-root command execution from an image pull", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.7.33).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50880 — github.com/docker/buildx v0.12.0-rc2.0.20231219140829-617f538cb315 затронут GHSA-m4gq-fm9h-8q75 (CVE-2025-0495, GO-2025-3527)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/docker/buildx@v0.12.0-rc2.0.20231219140829-617f538cb315`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-m4gq-fm9h-8q75 (CVE-2025-0495, GO-2025-3527) для пакета Go github.com/docker/buildx версии v0.12.0-rc2.0.20231219140829-617f538cb315: buildx allows a possible credential leakage to telemetry endpoint. github.com/docker/buildx не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-m4gq-fm9h-8q75
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-m4gq-fm9h-8q75](https://osv.dev/vulnerability/GHSA-m4gq-fm9h-8q75) · line 74 · SHA-256 5b93d45db0eac23fbd34a4d98c927be3826309252073e675f01b2fd319cca8f3_

```
{"id": "GHSA-m4gq-fm9h-8q75", "aliases": ["CVE-2025-0495", "GO-2025-3527"], "modified": "2026-09-10T03:50:56.838694902Z", "summary": "buildx allows a possible credential leakage to telemetry endpoint", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:L/UI:P/VC:L/VI:N/VA:N/SC:H/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.21.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50882 — github.com/docker/distribution v2.8.3+incompatible затронут GHSA-685w-q87j-wqw3 (CVE-2026-85747, GO-2026-6778)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/docker/distribution@v2.8.3+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 6.8 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-685w-q87j-wqw3 (CVE-2026-85747, GO-2026-6778) для пакета Go github.com/docker/distribution версии v2.8.3+incompatible: Distribution: Client `manifests.Get()` does not verify returned content against requested digest. github.com/docker/distribution не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-685w-q87j-wqw3
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-685w-q87j-wqw3](https://osv.dev/vulnerability/GHSA-685w-q87j-wqw3) · line 77 · SHA-256 ba22f4fb3ac22a62eaf660a46e0f60299437658af640c5182ec36c985404e039_

```
{"id": "GHSA-685w-q87j-wqw3", "aliases": ["BIT-distribution-2026-85747", "CVE-2026-85747", "GO-2026-6778"], "modified": "2026-11-05T23:25:40.391377389Z", "summary": "Distribution: Client `manifests.Get()` does not verify returned content against requested digest", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (2.8.4-0.20260923142519-db037680f2ac+incompatible).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50883 — github.com/in-toto/in-toto-golang v0.5.0 затронут GHSA-pmwq-pjrm-6p5r (GO-2026-5547)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/in-toto/in-toto-golang@v0.5.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 4.1 (`CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-pmwq-pjrm-6p5r (GO-2026-5547) для пакета Go github.com/in-toto/in-toto-golang версии v0.5.0: in-toto-golang and in-toto-python have inconsistent negation behavior. github.com/in-toto/in-toto-golang не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pmwq-pjrm-6p5r
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pmwq-pjrm-6p5r](https://osv.dev/vulnerability/GHSA-pmwq-pjrm-6p5r) · line 129 · SHA-256 7087038b3fc77875c8cdd12a4c653c8459fdc223c6fd3ea799f05ab80ff9dd3c_

```
{"id": "GHSA-pmwq-pjrm-6p5r", "aliases": ["GO-2026-5547"], "modified": "2026-09-10T03:51:06.602952009Z", "summary": "in-toto-golang and in-toto-python have inconsistent negation behavior", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:H/UI:N/S:U/C:N/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.11.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50884 — github.com/moby/buildkit v0.13.0-beta1.0.20231219135447-957cb50df991 затронут GHSA-4c29-8rgm-jvjj (CVE-2026-33747, GO-2026-4858)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/moby/buildkit@v0.13.0-beta1.0.20231219135447-957cb50df991`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 8.4 (`CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-4c29-8rgm-jvjj (CVE-2026-33747, GO-2026-4858) для пакета Go github.com/moby/buildkit версии v0.13.0-beta1.0.20231219135447-957cb50df991: BuildKit's Malicious frontend can cause file escape outside of storage root. github.com/moby/buildkit не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4c29-8rgm-jvjj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4c29-8rgm-jvjj](https://osv.dev/vulnerability/GHSA-4c29-8rgm-jvjj) · line 155 · SHA-256 15c1f4430dbbc4f344170d36bb9ebef99af1765a5bef428de1411de0eb0c741b_

```
{"id": "GHSA-4c29-8rgm-jvjj", "aliases": ["CVE-2026-33747", "GO-2026-4858"], "modified": "2026-09-10T03:50:37.172155078Z", "summary": "BuildKit's Malicious frontend can cause file escape outside of storage root", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.28.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50885 — github.com/moby/buildkit v0.13.0-beta1.0.20231219135447-957cb50df991 затронут GHSA-4vrq-3vrq-g6gg (CVE-2026-33748, GO-2026-4859)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/moby/buildkit@v0.13.0-beta1.0.20231219135447-957cb50df991`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-4vrq-3vrq-g6gg (CVE-2026-33748, GO-2026-4859) для пакета Go github.com/moby/buildkit версии v0.13.0-beta1.0.20231219135447-957cb50df991: BuildKit Git URL subdir component can cause access to restricted files. github.com/moby/buildkit не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4vrq-3vrq-g6gg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4vrq-3vrq-g6gg](https://osv.dev/vulnerability/GHSA-4vrq-3vrq-g6gg) · line 155 · SHA-256 f3952d10328f59e0a508140802da2d8a120f604607697753a91275e496904172_

```
{"id": "GHSA-4vrq-3vrq-g6gg", "aliases": ["CVE-2026-33748", "GO-2026-4859"], "modified": "2026-09-10T03:50:59.724878717Z", "summary": "BuildKit Git URL subdir component can cause access to restricted files", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:H/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.28.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50886 — github.com/moby/buildkit v0.13.0-beta1.0.20231219135447-957cb50df991 затронут GHSA-7236-3392-c5c6 (CVE-2026-61711, GO-2026-6255)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/moby/buildkit@v0.13.0-beta1.0.20231219135447-957cb50df991`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7236-3392-c5c6 (CVE-2026-61711, GO-2026-6255) для пакета Go github.com/moby/buildkit версии v0.13.0-beta1.0.20231219135447-957cb50df991: BuildKit: Custom frontend could bypass Seccomp/AppArmor. github.com/moby/buildkit не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7236-3392-c5c6
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7236-3392-c5c6](https://osv.dev/vulnerability/GHSA-7236-3392-c5c6) · line 155 · SHA-256 4f6eae29d996fddd010e8fc8fddbf87bdf8c711e8fc188a1274ddbe18c57e018_

```
{"id": "GHSA-7236-3392-c5c6", "aliases": ["CVE-2026-61711", "GO-2026-6255"], "modified": "2026-09-10T03:51:13.277422932Z", "summary": "BuildKit: Custom frontend could bypass Seccomp/AppArmor", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:L/VI:L/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50887 — github.com/moby/buildkit v0.13.0-beta1.0.20231219135447-957cb50df991 затронут GHSA-72x6-4j93-7w86 (CVE-2026-61712, GO-2026-6256)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/moby/buildkit@v0.13.0-beta1.0.20231219135447-957cb50df991`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-72x6-4j93-7w86 (CVE-2026-61712, GO-2026-6256) для пакета Go github.com/moby/buildkit версии v0.13.0-beta1.0.20231219135447-957cb50df991: BuildKit has a possible runtime DoS via unbounded group parsing. github.com/moby/buildkit не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-72x6-4j93-7w86
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-72x6-4j93-7w86](https://osv.dev/vulnerability/GHSA-72x6-4j93-7w86) · line 155 · SHA-256 db61a3df27e55d87b018ef95410192bfc4c73663ca540a9ff1bddd7cecbdb0fb_

```
{"id": "GHSA-72x6-4j93-7w86", "aliases": ["CVE-2026-61712", "GO-2026-6256"], "modified": "2026-09-10T03:51:13.226978985Z", "summary": "BuildKit has a possible runtime DoS via unbounded group parsing", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:P/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.31.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50888 — github.com/moby/spdystream v0.2.0 затронут GHSA-pc3f-x583-g7j2 (CVE-2026-35469, GO-2026-4958)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/moby/spdystream@v0.2.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-pc3f-x583-g7j2 (CVE-2026-35469, GO-2026-4958) для пакета Go github.com/moby/spdystream версии v0.2.0: SpdyStream: DOS on CRI. github.com/moby/spdystream не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pc3f-x583-g7j2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pc3f-x583-g7j2](https://osv.dev/vulnerability/GHSA-pc3f-x583-g7j2) · line 159 · SHA-256 736d8474ca354f8276a7f0bdee1ff8f6eb209f4f8ef5959118c5f095dd71d7d9_

```
{"id": "GHSA-pc3f-x583-g7j2", "aliases": ["CVE-2026-35469", "GO-2026-4958"], "modified": "2026-09-10T03:51:02.523109450Z", "summary": "SpdyStream: DOS on CRI", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.5.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50889 — github.com/moby/sys/user v0.1.0 затронут GHSA-mjcv-p78q-w5fw (CVE-2026-61801, GO-2026-6686)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/github.com/moby/sys/user@v0.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 5.5 (`CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-mjcv-p78q-w5fw (CVE-2026-61801, GO-2026-6686) для пакета Go github.com/moby/sys/user версии v0.1.0: github.com/moby/sys/user has a possible DoS via unbounded parsing of user and group database files. github.com/moby/sys/user не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mjcv-p78q-w5fw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mjcv-p78q-w5fw](https://osv.dev/vulnerability/GHSA-mjcv-p78q-w5fw) · line 164 · SHA-256 ba40c902a140bce209c973900a8d55acde8190e9e0836bae907de154703d4b0c_

```
{"id": "GHSA-mjcv-p78q-w5fw", "aliases": ["CVE-2026-61801", "GO-2026-6686"], "modified": "2026-10-19T21:40:47.349593935Z", "summary": "github.com/moby/sys/user has a possible DoS via unbounded parsing of user and group database files", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.4.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50890 — go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc v0.45.0 затронут GHSA-8pgv-569h-w5rw (CVE-2023-47108, GO-2023-2331)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc@v0.45.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-8pgv-569h-w5rw (CVE-2023-47108, GO-2023-2331) для пакета Go go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc версии v0.45.0: otelgrpc DoS vulnerability due to unbound cardinality metrics. go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8pgv-569h-w5rw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8pgv-569h-w5rw](https://osv.dev/vulnerability/GHSA-8pgv-569h-w5rw) · line 219 · SHA-256 c93330fb4a2cc3c96a4a2a483684d271fad8297857b487b14e06fbb4a249cbdd_

```
{"id": "GHSA-8pgv-569h-w5rw", "aliases": ["CVE-2023-47108", "GO-2023-2331"], "modified": "2026-09-10T03:49:58.904350912Z", "summary": "otelgrpc DoS vulnerability due to unbound cardinality metrics ", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.46.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50892 — go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp v0.42.0 затронут GHSA-w8rr-5gcm-pp58 (CVE-2026-39882, GO-2026-4985)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp@v0.42.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-w8rr-5gcm-pp58 (CVE-2026-39882, GO-2026-4985) для пакета Go go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp версии v0.42.0: opentelemetry-go: OTLP HTTP exporters read unbounded HTTP response bodies. go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w8rr-5gcm-pp58
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w8rr-5gcm-pp58](https://osv.dev/vulnerability/GHSA-w8rr-5gcm-pp58) · line 225 · SHA-256 ca54eb73bf035264a9099d99a7b6f8c5259cf0bb0cfd5a6131a8862d71f11ae1_

```
{"id": "GHSA-w8rr-5gcm-pp58", "aliases": ["CVE-2026-39882", "GO-2026-4985"], "modified": "2026-09-10T03:51:03.562742514Z", "summary": "opentelemetry-go: OTLP HTTP exporters read unbounded HTTP response bodies", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.43.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50893 — go.opentelemetry.io/otel/exporters/otlp/otlptrace v1.19.0 затронут GHSA-8wmf-6v46-5gfg (CVE-2026-81870, GO-2026-6505)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/go.opentelemetry.io/otel/exporters/otlp/otlptrace@v1.19.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-8wmf-6v46-5gfg (CVE-2026-81870, GO-2026-6505) для пакета Go go.opentelemetry.io/otel/exporters/otlp/otlptrace версии v1.19.0: OpenTelemetry-Go: Exporter config logging may leak endpoint URLs in info logs. go.opentelemetry.io/otel/exporters/otlp/otlptrace не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8wmf-6v46-5gfg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8wmf-6v46-5gfg](https://osv.dev/vulnerability/GHSA-8wmf-6v46-5gfg) · line 226 · SHA-256 46993eff31ca3e37f0fc48a72831cfe45d83daf84e09fb9140b9052cb0c78bf3_

```
{"id": "GHSA-8wmf-6v46-5gfg", "aliases": ["CVE-2026-81870", "GO-2026-6505"], "modified": "2026-10-01T20:55:52.479756803Z", "summary": "OpenTelemetry-Go: Exporter config logging may leak endpoint URLs in info logs", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.45.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50894 — go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc v1.19.0 затронут GHSA-8wmf-6v46-5gfg (CVE-2026-81870, GO-2026-6505)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc@v1.19.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-8wmf-6v46-5gfg (CVE-2026-81870, GO-2026-6505) для пакета Go go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc версии v1.19.0: OpenTelemetry-Go: Exporter config logging may leak endpoint URLs in info logs. go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8wmf-6v46-5gfg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8wmf-6v46-5gfg](https://osv.dev/vulnerability/GHSA-8wmf-6v46-5gfg) · line 227 · SHA-256 46993eff31ca3e37f0fc48a72831cfe45d83daf84e09fb9140b9052cb0c78bf3_

```
{"id": "GHSA-8wmf-6v46-5gfg", "aliases": ["CVE-2026-81870", "GO-2026-6505"], "modified": "2026-10-01T20:55:52.479756803Z", "summary": "OpenTelemetry-Go: Exporter config logging may leak endpoint URLs in info logs", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.45.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50895 — go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp v1.19.0 затронут GHSA-8wmf-6v46-5gfg (CVE-2026-81870, GO-2026-6505)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp@v1.19.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-8wmf-6v46-5gfg (CVE-2026-81870, GO-2026-6505) для пакета Go go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp версии v1.19.0: OpenTelemetry-Go: Exporter config logging may leak endpoint URLs in info logs. go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8wmf-6v46-5gfg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8wmf-6v46-5gfg](https://osv.dev/vulnerability/GHSA-8wmf-6v46-5gfg) · line 228 · SHA-256 46993eff31ca3e37f0fc48a72831cfe45d83daf84e09fb9140b9052cb0c78bf3_

```
{"id": "GHSA-8wmf-6v46-5gfg", "aliases": ["CVE-2026-81870", "GO-2026-6505"], "modified": "2026-10-01T20:55:52.479756803Z", "summary": "OpenTelemetry-Go: Exporter config logging may leak endpoint URLs in info logs", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.45.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50896 — go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp v1.19.0 затронут GHSA-w8rr-5gcm-pp58 (CVE-2026-39882, GO-2026-4985)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp@v1.19.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-w8rr-5gcm-pp58 (CVE-2026-39882, GO-2026-4985) для пакета Go go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp версии v1.19.0: opentelemetry-go: OTLP HTTP exporters read unbounded HTTP response bodies. go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w8rr-5gcm-pp58
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w8rr-5gcm-pp58](https://osv.dev/vulnerability/GHSA-w8rr-5gcm-pp58) · line 228 · SHA-256 ca54eb73bf035264a9099d99a7b6f8c5259cf0bb0cfd5a6131a8862d71f11ae1_

```
{"id": "GHSA-w8rr-5gcm-pp58", "aliases": ["CVE-2026-39882", "GO-2026-4985"], "modified": "2026-09-10T03:51:03.562742514Z", "summary": "opentelemetry-go: OTLP HTTP exporters read unbounded HTTP response bodies", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.43.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50897 — go.opentelemetry.io/otel/sdk v1.24.0 затронут GHSA-8wmf-6v46-5gfg (CVE-2026-81870, GO-2026-6505)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/go.opentelemetry.io/otel/sdk@v1.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-8wmf-6v46-5gfg (CVE-2026-81870, GO-2026-6505) для пакета Go go.opentelemetry.io/otel/sdk версии v1.24.0: OpenTelemetry-Go: Exporter config logging may leak endpoint URLs in info logs. go.opentelemetry.io/otel/sdk не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8wmf-6v46-5gfg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8wmf-6v46-5gfg](https://osv.dev/vulnerability/GHSA-8wmf-6v46-5gfg) · line 231 · SHA-256 46993eff31ca3e37f0fc48a72831cfe45d83daf84e09fb9140b9052cb0c78bf3_

```
{"id": "GHSA-8wmf-6v46-5gfg", "aliases": ["CVE-2026-81870", "GO-2026-6505"], "modified": "2026-10-01T20:55:52.479756803Z", "summary": "OpenTelemetry-Go: Exporter config logging may leak endpoint URLs in info logs", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:P/PR:L/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.45.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50898 — go.opentelemetry.io/otel/sdk v1.24.0 затронут GHSA-9h8m-3fm2-qjrq (CVE-2026-24051, GO-2026-4394)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/go.opentelemetry.io/otel/sdk@v1.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 7.0 (`CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H`)

OSV.dev сообщает GHSA-9h8m-3fm2-qjrq (CVE-2026-24051, GO-2026-4394) для пакета Go go.opentelemetry.io/otel/sdk версии v1.24.0: OpenTelemetry Go SDK Vulnerable to Arbitrary Code Execution via PATH Hijacking. go.opentelemetry.io/otel/sdk не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9h8m-3fm2-qjrq
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9h8m-3fm2-qjrq](https://osv.dev/vulnerability/GHSA-9h8m-3fm2-qjrq) · line 231 · SHA-256 d495ad199e55d0a2f62956ce6b635f62010f8c3c140de07116960e17ab6bf690_

```
{"id": "GHSA-9h8m-3fm2-qjrq", "aliases": ["CVE-2026-24051", "GO-2026-4394"], "modified": "2026-09-10T03:50:34.801777790Z", "summary": "OpenTelemetry Go SDK Vulnerable to Arbitrary Code Execution via PATH Hijacking", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:H/I:H/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.40.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50899 — go.opentelemetry.io/otel/sdk v1.24.0 затронут GHSA-hfvc-g4fc-pqhx (CVE-2026-39883, GO-2026-5426)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/go.opentelemetry.io/otel/sdk@v1.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-hfvc-g4fc-pqhx (CVE-2026-39883, GO-2026-5426) для пакета Go go.opentelemetry.io/otel/sdk версии v1.24.0: opentelemetry-go: BSD kenv command not using absolute path enables PATH hijacking. go.opentelemetry.io/otel/sdk не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hfvc-g4fc-pqhx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-hfvc-g4fc-pqhx](https://osv.dev/vulnerability/GHSA-hfvc-g4fc-pqhx) · line 231 · SHA-256 4ca6833a5cc016be498ff7a83ee0c6229be6394fbe0d857f8137bd24a04c7bc2_

```
{"id": "GHSA-hfvc-g4fc-pqhx", "aliases": ["CVE-2026-39883", "GO-2026-5426"], "modified": "2026-09-10T03:51:01.896515018Z", "summary": "opentelemetry-go: BSD kenv command not using absolute path enables PATH hijacking", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:H/AT:N/PR:L/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.43.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50900 — go.opentelemetry.io/otel/sdk v1.24.0 затронут GHSA-p9f8-wvj8-2fg8 (CVE-2026-81869, GO-2026-6616)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/go.opentelemetry.io/otel/sdk@v1.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-p9f8-wvj8-2fg8 (CVE-2026-81869, GO-2026-6616) для пакета Go go.opentelemetry.io/otel/sdk версии v1.24.0: OpenTelemetry-Go: UTF-8 replacement rune bypasses attribute length truncation. go.opentelemetry.io/otel/sdk не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-p9f8-wvj8-2fg8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-p9f8-wvj8-2fg8](https://osv.dev/vulnerability/GHSA-p9f8-wvj8-2fg8) · line 231 · SHA-256 39f0426a5029695ce7678ce238e74bef55e6cefe9854bb1ee4df74d4979c9269_

```
{"id": "GHSA-p9f8-wvj8-2fg8", "aliases": ["CVE-2026-81869", "GO-2026-6616"], "modified": "2026-10-01T20:56:23.877100823Z", "summary": "OpenTelemetry-Go: UTF-8 replacement rune bypasses attribute length truncation", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.33.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50903 — golang.org/x/oauth2 v0.16.0 затронут GHSA-6v2p-p543-phr9 (CVE-2025-22868, GO-2025-3488)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/oauth2@v0.16.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-6v2p-p543-phr9 (CVE-2025-22868, GO-2025-3488) для пакета Go golang.org/x/oauth2 версии v0.16.0: golang.org/x/oauth2 Improper Validation of Syntactic Correctness of Input vulnerability. golang.org/x/oauth2 не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-6v2p-p543-phr9
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-6v2p-p543-phr9](https://osv.dev/vulnerability/GHSA-6v2p-p543-phr9) · line 243 · SHA-256 de68cb8ff34bd59b46a824437e12befc60649c3be224bfe99db0da3309377ac8_

```
{"id": "GHSA-6v2p-p543-phr9", "aliases": ["CVE-2025-22868", "GO-2025-3488"], "modified": "2026-09-10T03:50:26.016569187Z", "summary": "golang.org/x/oauth2 Improper Validation of Syntactic Correctness of Input vulnerability", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.27.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50904 — google.golang.org/grpc v1.59.0 затронут GHSA-2v4p-qf9q-27wj (CVE-2026-84445, GO-2026-6443)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/google.golang.org/grpc@v1.59.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-2v4p-qf9q-27wj (CVE-2026-84445, GO-2026-6443) для пакета Go google.golang.org/grpc версии v1.59.0: gRPC-Go xDS servers: Denial of Service (DoS) via crash due to missing `:authority` and `Host` headers. google.golang.org/grpc не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2v4p-qf9q-27wj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2v4p-qf9q-27wj](https://osv.dev/vulnerability/GHSA-2v4p-qf9q-27wj) · line 254 · SHA-256 4dbe7a3a9cbbac8cbd273a244c6da2910d88f82b747be650d23c01e61121613c_

```
{"id": "GHSA-2v4p-qf9q-27wj", "aliases": ["CVE-2026-84445", "GO-2026-6443"], "modified": "2026-09-25T18:00:05.270054427Z", "summary": "gRPC-Go xDS servers: Denial of Service (DoS) via crash due to missing `:authority` and `Host` headers", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:X/CR:X/IR:X/AR:X/MAV:X/MAC:X/MAT:X/MPR:X/MUI:X/MVC:X/MVI:X/MVA:X/MSC:X/MSI:X/MSA:X/S:X/AU:X/R:X/V:X/RE:X/U:X"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.82.2, 1.83.2, 1.84.0-dev.0.20260825144003-d5a41119e0e3, 1.85.0-dev.0.20260825072537-93e31b48545e).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50905 — google.golang.org/grpc v1.59.0 затронут GHSA-hrxh-6v49-42gf (GO-2026-6061)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/google.golang.org/grpc@v1.59.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-hrxh-6v49-42gf (GO-2026-6061) для пакета Go google.golang.org/grpc версии v1.59.0: gRPC-Go: xDS RBAC and HTTP/2 Vulnerabilities. google.golang.org/grpc не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-hrxh-6v49-42gf
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-hrxh-6v49-42gf](https://osv.dev/vulnerability/GHSA-hrxh-6v49-42gf) · line 254 · SHA-256 c431c4daa81149293908704a4f883c817e7eba6cb420cc77f01381c250b545a4_

```
{"id": "GHSA-hrxh-6v49-42gf", "aliases": ["GO-2026-6061"], "modified": "2026-09-10T03:51:11.547405330Z", "summary": "gRPC-Go: xDS RBAC and HTTP/2 Vulnerabilities", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:H/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.82.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50906 — google.golang.org/grpc v1.59.0 затронут GHSA-p77j-4mvh-x3m3 (CVE-2026-33186, GO-2026-4762)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/google.golang.org/grpc@v1.59.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 9.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-p77j-4mvh-x3m3 (CVE-2026-33186, GO-2026-4762) для пакета Go google.golang.org/grpc версии v1.59.0: gRPC-Go has an authorization bypass via missing leading slash in :path. google.golang.org/grpc не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-p77j-4mvh-x3m3
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-p77j-4mvh-x3m3](https://osv.dev/vulnerability/GHSA-p77j-4mvh-x3m3) · line 254 · SHA-256 1a87ff87c9504faca8efb5288f94ad12665617f570f67ec763d4a99d50a79c1c_

```
{"id": "GHSA-p77j-4mvh-x3m3", "aliases": ["CVE-2026-33186", "GO-2026-4762"], "modified": "2026-09-10T03:50:40.107473327Z", "summary": "gRPC-Go has an authorization bypass via missing leading slash in :path", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.79.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50907 — google.golang.org/grpc v1.59.0 затронут GHSA-qc2q-p7wx-3px3 (CVE-2026-84303, GO-2026-6441)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/google.golang.org/grpc@v1.59.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-qc2q-p7wx-3px3 (CVE-2026-84303, GO-2026-6441) для пакета Go google.golang.org/grpc версии v1.59.0: gRPC-Go: xDS RBAC HTTP Filter bypass via mixed-case Header Matching and gRFC A41 validation evasion. google.golang.org/grpc не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qc2q-p7wx-3px3
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qc2q-p7wx-3px3](https://osv.dev/vulnerability/GHSA-qc2q-p7wx-3px3) · line 254 · SHA-256 7fd599a2808f80a77ccd1ce7b99b5c035f488cf145861f5089ca014de8ef0cbc_

```
{"id": "GHSA-qc2q-p7wx-3px3", "aliases": ["CVE-2026-84303", "GO-2026-6441"], "modified": "2026-09-15T19:10:32.558419529Z", "summary": "gRPC-Go: xDS RBAC HTTP Filter bypass via mixed-case Header Matching and gRFC A41 validation evasion", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.83.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50908 — google.golang.org/grpc v1.59.0 затронут GHSA-vp52-pcj8-j9qc (CVE-2026-84304, GO-2026-6348)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/google.golang.org/grpc@v1.59.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-vp52-pcj8-j9qc (CVE-2026-84304, GO-2026-6348) для пакета Go google.golang.org/grpc версии v1.59.0: gRPC-Go: Heap Memory Exhaustion (OOM) via HTTP/2 DATA Frame Fragmentation. google.golang.org/grpc не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vp52-pcj8-j9qc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vp52-pcj8-j9qc](https://osv.dev/vulnerability/GHSA-vp52-pcj8-j9qc) · line 254 · SHA-256 e3cb0cc53716d4b2c1d5075abe994d05d5a0154a33cf6edb35ad05d456d69fb9_

```
{"id": "GHSA-vp52-pcj8-j9qc", "aliases": ["CVE-2026-84304", "GO-2026-6348"], "modified": "2026-09-15T19:10:44.560975305Z", "summary": "gRPC-Go: Heap Memory Exhaustion (OOM) via HTTP/2 DATA Frame Fragmentation", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.83.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50911 — golang.org/x/net v0.23.0 затронут GHSA-5cv4-jp36-h3mw (CVE-2026-25680, GO-2026-5028)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-5cv4-jp36-h3mw (CVE-2026-25680, GO-2026-5028) для пакета Go golang.org/x/net версии v0.23.0: Go Net HTML parser is vulnerable to denial of service. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-5cv4-jp36-h3mw
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-5cv4-jp36-h3mw](https://osv.dev/vulnerability/GHSA-5cv4-jp36-h3mw) · line 43 · SHA-256 9eb940a510edc67a0602da898a09dec5f6df07648ae4055c09b64e227fafa40d_

```
{"id": "GHSA-5cv4-jp36-h3mw", "aliases": ["CVE-2026-25680", "GO-2026-5028"], "modified": "2026-09-10T03:50:45.494180024Z", "summary": "Go Net HTML parser is vulnerable to denial of service", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.55.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50912 — golang.org/x/net v0.23.0 затронут GHSA-qxp5-gwg8-xv66 (CVE-2025-22870, GO-2025-3503)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: 4.4 (`CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:L`)

OSV.dev сообщает GHSA-qxp5-gwg8-xv66 (CVE-2025-22870, GO-2025-3503) для пакета Go golang.org/x/net версии v0.23.0: HTTP Proxy bypass using IPv6 Zone IDs in golang.org/x/net. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-qxp5-gwg8-xv66
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-qxp5-gwg8-xv66](https://osv.dev/vulnerability/GHSA-qxp5-gwg8-xv66) · line 43 · SHA-256 80c439bfcabcd34c2204066f529bba29e9557b78460115cf2b65cc8aa76db117_

```
{"id": "GHSA-qxp5-gwg8-xv66", "aliases": ["CVE-2025-22870", "GO-2025-3503"], "modified": "2026-09-10T03:50:23.280114085Z", "summary": "HTTP Proxy bypass using IPv6 Zone IDs in golang.org/x/net", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:L"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.36.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50753 — atty 0.2.14 затронут GHSA-g98v-hv3f-hcfr (RUSTSEC-2021-0145)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/atty@0.2.14`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50755 — bincode 1.3.3: информационный бюллетень RUSTSEC-2025-0141 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `dependency:crates.io/bincode@1.3.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50756 — bincode 2.0.1: информационный бюллетень RUSTSEC-2025-0141 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `dependency:crates.io/bincode@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50792 — tokio 1.52.3 затронут RUSTSEC-2026-0386 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/tokio@1.52.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.51.6, 1.53.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50794 — url 2.5.8 затронут RUSTSEC-2026-0592 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/url@2.5.8`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0592 для пакета crates.io url версии 2.5.8: Stack overflow in `Url::origin()` on nested `blob:` URLs. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни одна из затронутых функций (url::Url::origin, url::quirks::origin) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0592
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0592](https://osv.dev/vulnerability/RUSTSEC-2026-0592) · manifest · SHA-256 9fdeb08e523b9b634ce52d0e2982b63623de0fbbf6a079d9d20e6e24f3cc4522_

```
{"id": "RUSTSEC-2026-0592", "aliases": ["GHSA-hrj5-67jp-wqp9"], "modified": "2026-11-22T10:00:02.260974192Z", "summary": "Stack overflow in `Url::origin()` on nested `blob:` URLs", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (2.5.9).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50809 — zstd-sys 2.0.16+zstd.1.5.7 затронут RUSTSEC-2026-0410 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-sys@2.0.16+zstd.1.5.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (2.1.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50822 — github.com/docker/docker v26.1.0+incompatible затронут GO-2026-4887 (CVE-2026-34040) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/docker/docker@v26.1.0+incompatible`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-4887 (CVE-2026-34040) для пакета Go github.com/docker/docker версии v26.1.0+incompatible: Moby has AuthZ plugin bypass when provided oversized request bodies in github.com/docker/docker. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Сборка продукта включает github.com/docker/docker, но govulncheck не нашёл импорта ни одного затронутого пакета: к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-4887
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-4887](https://osv.dev/vulnerability/GO-2026-4887) · line 39 · SHA-256 8f5eb166a62445c07f12c47f23fd744ece52fb0884486bc8756f2150eaaae6ac_

```
{"id": "GO-2026-4887", "aliases": ["CVE-2026-34040", "GHSA-x744-4wpc-v9h2"], "modified": "2026-11-23T20:30:07.958815145Z", "summary": "Moby has AuthZ plugin bypass when provided oversized request bodies in github.com/docker/docker", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50846 — golang.org/x/crypto v0.32.0 затронут GO-2026-5932 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5932 для пакета Go golang.org/x/crypto версии v0.32.0: The golang.org/x/crypto/openpgp package is unmaintained, unsafe by design, and has known security issues. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Сборка продукта включает golang.org/x/crypto, но govulncheck не нашёл импорта ни одного затронутого пакета: к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5932
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5932](https://osv.dev/vulnerability/GO-2026-5932) · line 111 · SHA-256 7567598e736f75fe8f2c913606229875f197cdfc5e798ba52e2dfa3ab75088b4_

```
{"id": "GO-2026-5932", "aliases": [], "modified": "2026-11-02T22:15:06.677088389Z", "summary": "The golang.org/x/crypto/openpgp package is unmaintained, unsafe by design, and has known security issues", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.58.1-0.20261009181718-2f1f834330b2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50847 — golang.org/x/crypto v0.32.0 затронут GO-2026-6303 (CVE-2026-56854) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6303 (CVE-2026-56854) для пакета Go golang.org/x/crypto версии v0.32.0: Source-address critical option not enforced for non-public-key auth callbacks in golang.org/x/crypto/ssh. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6303
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6303](https://osv.dev/vulnerability/GO-2026-6303) · line 111 · SHA-256 ec2ba174bedfaf875dcd1b7ac4bcd7f495d0dea9d077b54300ec42333daedd57_

```
{"id": "GO-2026-6303", "aliases": ["CVE-2026-56854"], "modified": "2026-08-29T10:10:52.440319762Z", "summary": "Source-address critical option not enforced for non-public-key auth callbacks in golang.org/x/crypto/ssh", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.55.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50848 — golang.org/x/crypto v0.32.0 затронут GO-2026-6354 (CVE-2026-78662) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/crypto@v0.32.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6354 (CVE-2026-78662) для пакета Go golang.org/x/crypto версии v0.32.0: Prevent DoS on deadlocked undecided channel in golang.org/x/crypto/ssh. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6354
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6354](https://osv.dev/vulnerability/GO-2026-6354) · line 111 · SHA-256 b86b82c732322f2a8c1cf4850d66c74ee8f6ef65173c30f0b3da9481469cf43b_

```
{"id": "GO-2026-6354", "aliases": ["CVE-2026-78662"], "modified": "2026-09-03T10:10:55.147673102Z", "summary": "Prevent DoS on deadlocked undecided channel in golang.org/x/crypto/ssh", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.56.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50852 — golang.org/x/net v0.25.0 затронут GO-2024-3333 (CVE-2024-45338) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2024-3333 (CVE-2024-45338) для пакета Go golang.org/x/net версии v0.25.0: Non-linear parsing of case-insensitive content in golang.org/x/net/html. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2024-3333
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2024-3333](https://osv.dev/vulnerability/GO-2024-3333) · line 112 · SHA-256 19787df89623951148a2a7a084bcccb50bf9a64faa4c21b5075894f6f4a3dc95_

```
{"id": "GO-2024-3333", "aliases": ["CVE-2024-45338", "GHSA-w32m-9786-jp63"], "modified": "2026-03-24T23:55:17.997380Z", "summary": "Non-linear parsing of case-insensitive content in golang.org/x/net/html", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.33.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50853 — golang.org/x/net v0.25.0 затронут GO-2026-4440 (CVE-2025-47911) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-4440 (CVE-2025-47911) для пакета Go golang.org/x/net версии v0.25.0: Quadratic parsing complexity in golang.org/x/net/html. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-4440
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-4440](https://osv.dev/vulnerability/GO-2026-4440) · line 112 · SHA-256 810c43c05af16b2d74cd1e7079ff4e6ac758e7ce311fcb7f1ab1a37278d77382_

```
{"id": "GO-2026-4440", "aliases": ["CVE-2025-47911", "GHSA-w4gw-w5jq-g9jh"], "modified": "2026-05-15T10:59:23.883331519Z", "summary": "Quadratic parsing complexity in golang.org/x/net/html", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.45.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50854 — golang.org/x/net v0.25.0 затронут GO-2026-4441 (CVE-2025-58190) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-4441 (CVE-2025-58190) для пакета Go golang.org/x/net версии v0.25.0: Infinite parsing loop in golang.org/x/net. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-4441
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-4441](https://osv.dev/vulnerability/GO-2026-4441) · line 112 · SHA-256 d84a71bcd914561b3d0a250113736b0da37029149d2ba8285f5d10990335d42d_

```
{"id": "GO-2026-4441", "aliases": ["CVE-2025-58190"], "modified": "2026-05-15T10:59:23.510056268Z", "summary": "Infinite parsing loop in golang.org/x/net", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.45.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50856 — golang.org/x/net v0.25.0 затронут GO-2026-5025 (CVE-2026-42506) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5025 (CVE-2026-42506) для пакета Go golang.org/x/net версии v0.25.0: Invoking incorrect handling of namespaced elements in foreign content in golang.org/x/net/html. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5025
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5025](https://osv.dev/vulnerability/GO-2026-5025) · line 112 · SHA-256 729eaacf2ace57a657d06bb24a02ca018a5fabcb321fce088c3e7d52ca0e24ed_

```
{"id": "GO-2026-5025", "aliases": ["CVE-2026-42506"], "modified": "2026-05-30T05:14:17.563517047Z", "summary": "Invoking incorrect handling of namespaced elements in foreign content in golang.org/x/net/html", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.55.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50858 — golang.org/x/net v0.25.0 затронут GO-2026-5027 (CVE-2026-42502) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5027 (CVE-2026-42502) для пакета Go golang.org/x/net версии v0.25.0: Invoking incorrect handling of HTML elements in foreign content in golang.org/x/net/html. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5027
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5027](https://osv.dev/vulnerability/GO-2026-5027) · line 112 · SHA-256 5389cdeb4820dfb70f8dd44fd2d9c150e3e4ea744cb8dced8202c7ed38bf0bc3_

```
{"id": "GO-2026-5027", "aliases": ["CVE-2026-42502"], "modified": "2026-11-23T21:12:29.472586555Z", "summary": "Invoking incorrect handling of HTML elements in foreign content in golang.org/x/net/html", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.55.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50859 — golang.org/x/net v0.25.0 затронут GO-2026-5029 (CVE-2026-25681) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5029 (CVE-2026-25681) для пакета Go golang.org/x/net версии v0.25.0: Invoking incorrect handling of character references in DOCTYPE nodes in golang.org/x/net/html. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5029
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5029](https://osv.dev/vulnerability/GO-2026-5029) · line 112 · SHA-256 c064ba5455b8f417db2c56741f0351bc16de82a8c15c235089038f02c823f383_

```
{"id": "GO-2026-5029", "aliases": ["CVE-2026-25681"], "modified": "2026-11-23T21:12:28.895525167Z", "summary": "Invoking incorrect handling of character references in DOCTYPE nodes in golang.org/x/net/html", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.55.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50860 — golang.org/x/net v0.25.0 затронут GO-2026-5030 (CVE-2026-27136) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5030 (CVE-2026-27136) для пакета Go golang.org/x/net версии v0.25.0: Invoking duplicate attributes can cause XSS in golang.org/x/net/html. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5030
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5030](https://osv.dev/vulnerability/GO-2026-5030) · line 112 · SHA-256 cf1c47436d9a7e5382eac1f7cea5039975382d2829bf382b9020d1d17a0bdff8_

```
{"id": "GO-2026-5030", "aliases": ["CVE-2026-27136"], "modified": "2026-11-23T21:12:28.405165939Z", "summary": "Invoking duplicate attributes can cause XSS in golang.org/x/net/html", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.55.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50861 — golang.org/x/net v0.25.0 затронут GO-2026-5942 (CVE-2026-46600) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5942 (CVE-2026-46600) для пакета Go golang.org/x/net версии v0.25.0: Parsing an invalid SVCB or HTTPS RR can panic in golang.org/x/net/dns/dnsmessage. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Сборка продукта включает golang.org/x/net, но govulncheck не нашёл импорта ни одного затронутого пакета: к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5942
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5942](https://osv.dev/vulnerability/GO-2026-5942) · line 112 · SHA-256 b350c02f839159da0b17f9fc366081b6ecbfab32d57793400c90cafc79008499_

```
{"id": "GO-2026-5942", "aliases": ["BIT-golang-2026-46600", "CVE-2026-46600"], "modified": "2026-08-17T12:25:32.471119200Z", "summary": "Parsing an invalid SVCB or HTTPS RR can panic in golang.org/x/net/dns/dnsmessage", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.56.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50867 — golang.org/x/net v0.25.0 затронут GO-2026-6860 (CVE-2026-78661) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6860 (CVE-2026-78661) для пакета Go golang.org/x/net версии v0.25.0: Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6860
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6860](https://osv.dev/vulnerability/GO-2026-6860) · line 112 · SHA-256 850b298c34c0a0f97f8e85b1a9e277a2618a27421c9c964f241541b7a5147e9e_

```
{"id": "GO-2026-6860", "aliases": ["CVE-2026-78661"], "modified": "2026-10-27T21:30:04.890809062Z", "summary": "Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.62.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50868 — golang.org/x/net v0.25.0 затронут GO-2026-6866 (CVE-2026-97045) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.25.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6866 (CVE-2026-97045) для пакета Go golang.org/x/net версии v0.25.0: Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6866
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6866](https://osv.dev/vulnerability/GO-2026-6866) · line 112 · SHA-256 1950021930f2080580e00f4ada7bb415c92766857f916c4a233c6035c68078b8_

```
{"id": "GO-2026-6866", "aliases": ["CVE-2026-97045"], "modified": "2026-10-27T21:45:08.978077289Z", "summary": "Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.62.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50869 — golang.org/x/sys v0.30.0 затронут GO-2026-5024 (CVE-2026-39824) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/sys@v0.30.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5024 (CVE-2026-39824) для пакета Go golang.org/x/sys версии v0.30.0: Invoking integer overflow in NewNTUnicodeString in golang.org/x/sys/windows. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Сборка продукта включает golang.org/x/sys, но govulncheck не нашёл импорта ни одного затронутого пакета: к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5024
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5024](https://osv.dev/vulnerability/GO-2026-5024) · line 113 · SHA-256 8eb5752b5fe8b0b40442b7564eadf8462df856b5178998d8492d711b89916943_

```
{"id": "GO-2026-5024", "aliases": ["CVE-2026-39824"], "modified": "2026-06-09T18:59:22.740765220Z", "summary": "Invoking integer overflow in NewNTUnicodeString in golang.org/x/sys/windows", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.44.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50881 — github.com/docker/compose/v2 v2.24.7 затронут GO-2025-4077 (CVE-2025-62725) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/docker/compose/v2@v2.24.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2025-4077 (CVE-2025-62725) для пакета Go github.com/docker/compose/v2 версии v2.24.7: Docker Compose Vulnerable to Path Traversal via OCI Artifact Layer Annotations in github.com/docker/compose. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. github.com/docker/compose/v2 не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2025-4077
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2025-4077](https://osv.dev/vulnerability/GO-2025-4077) · line 76 · SHA-256 74b88bb0d0973ab11a33317c7b58d679ca711259999b6cd533321b858025c632_

```
{"id": "GO-2025-4077", "aliases": ["CVE-2025-62725", "GHSA-gv8h-7v7w-r22q"], "modified": "2026-03-03T04:57:05.845934Z", "summary": "Docker Compose Vulnerable to Path Traversal via OCI Artifact Layer Annotations in github.com/docker/compose", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (2.40.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50891 — go.opentelemetry.io/otel v1.24.0 затронут GO-2026-6975 (CVE-2026-128086) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/go.opentelemetry.io/otel@v1.24.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6975 (CVE-2026-128086) для пакета Go go.opentelemetry.io/otel версии v1.24.0: Memory allocation amplification in W3C baggage parsing in go.opentelemetry.io/otel. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. go.opentelemetry.io/otel не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6975
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6975](https://osv.dev/vulnerability/GO-2026-6975) · line 222 · SHA-256 a6f114650ff4cb30cb77e2928f51b6f8c82a9e27a3c811ca73df87338cb0aad4_

```
{"id": "GO-2026-6975", "aliases": ["CVE-2026-128086", "GHSA-rrfc-gjm9-cgrj"], "modified": "2026-11-23T20:30:17.039860504Z", "summary": "Memory allocation amplification in W3C baggage parsing in go.opentelemetry.io/otel", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.47.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50901 — golang.org/x/mod v0.17.0 затронут GO-2026-6179 (CVE-2026-56865) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/mod@v0.17.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6179 (CVE-2026-56865) для пакета Go golang.org/x/mod версии v0.17.0: Fix transparency log tile verification bypass in golang.org/x/mod/sumdb/tlog. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. golang.org/x/mod не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6179
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6179](https://osv.dev/vulnerability/GO-2026-6179) · line 241 · SHA-256 3890508ec809472d1fb79a06e92dbc0cea6a35f34bcf7c7f0fe51836b4764b8e_

```
{"id": "GO-2026-6179", "aliases": ["BIT-golang-2026-56865", "CVE-2026-56865"], "modified": "2026-08-19T12:25:40.780492871Z", "summary": "Fix transparency log tile verification bypass in golang.org/x/mod/sumdb/tlog", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.40.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50902 — golang.org/x/mod v0.17.0 затронут GO-2026-6180 (CVE-2026-56864) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/mod@v0.17.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6180 (CVE-2026-56864) для пакета Go golang.org/x/mod версии v0.17.0: Ignore unrelated, unauthenticated hashes in Lookup in golang.org/x/mod/sumdb. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. golang.org/x/mod не входит в сборку ни одного пакета продукта (govulncheck): его используют только тесты или инструменты, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6180
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6180](https://osv.dev/vulnerability/GO-2026-6180) · line 241 · SHA-256 c07c1002c6e2af97f043365acf157e06adc6bbe27ee9707ef4d0256cca66f0f1_

```
{"id": "GO-2026-6180", "aliases": ["BIT-golang-2026-56864", "CVE-2026-56864"], "modified": "2026-08-19T12:25:49.995487491Z", "summary": "Ignore unrelated, unauthenticated hashes in Lookup in golang.org/x/mod/sumdb", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.40.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50914 — golang.org/x/net v0.23.0 затронут GO-2024-3333 (CVE-2024-45338) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2024-3333 (CVE-2024-45338) для пакета Go golang.org/x/net версии v0.23.0: Non-linear parsing of case-insensitive content in golang.org/x/net/html. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2024-3333
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2024-3333](https://osv.dev/vulnerability/GO-2024-3333) · line 43 · SHA-256 19787df89623951148a2a7a084bcccb50bf9a64faa4c21b5075894f6f4a3dc95_

```
{"id": "GO-2024-3333", "aliases": ["CVE-2024-45338", "GHSA-w32m-9786-jp63"], "modified": "2026-03-24T23:55:17.997380Z", "summary": "Non-linear parsing of case-insensitive content in golang.org/x/net/html", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.33.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50915 — golang.org/x/net v0.23.0 затронут GO-2026-4440 (CVE-2025-47911) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-4440 (CVE-2025-47911) для пакета Go golang.org/x/net версии v0.23.0: Quadratic parsing complexity in golang.org/x/net/html. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-4440
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-4440](https://osv.dev/vulnerability/GO-2026-4440) · line 43 · SHA-256 810c43c05af16b2d74cd1e7079ff4e6ac758e7ce311fcb7f1ab1a37278d77382_

```
{"id": "GO-2026-4440", "aliases": ["CVE-2025-47911", "GHSA-w4gw-w5jq-g9jh"], "modified": "2026-05-15T10:59:23.883331519Z", "summary": "Quadratic parsing complexity in golang.org/x/net/html", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.45.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50916 — golang.org/x/net v0.23.0 затронут GO-2026-4441 (CVE-2025-58190) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-4441 (CVE-2025-58190) для пакета Go golang.org/x/net версии v0.23.0: Infinite parsing loop in golang.org/x/net. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-4441
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-4441](https://osv.dev/vulnerability/GO-2026-4441) · line 43 · SHA-256 d84a71bcd914561b3d0a250113736b0da37029149d2ba8285f5d10990335d42d_

```
{"id": "GO-2026-4441", "aliases": ["CVE-2025-58190"], "modified": "2026-05-15T10:59:23.510056268Z", "summary": "Infinite parsing loop in golang.org/x/net", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.45.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50918 — golang.org/x/net v0.23.0 затронут GO-2026-5025 (CVE-2026-42506) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5025 (CVE-2026-42506) для пакета Go golang.org/x/net версии v0.23.0: Invoking incorrect handling of namespaced elements in foreign content in golang.org/x/net/html. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5025
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5025](https://osv.dev/vulnerability/GO-2026-5025) · line 43 · SHA-256 729eaacf2ace57a657d06bb24a02ca018a5fabcb321fce088c3e7d52ca0e24ed_

```
{"id": "GO-2026-5025", "aliases": ["CVE-2026-42506"], "modified": "2026-05-30T05:14:17.563517047Z", "summary": "Invoking incorrect handling of namespaced elements in foreign content in golang.org/x/net/html", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.55.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50920 — golang.org/x/net v0.23.0 затронут GO-2026-5027 (CVE-2026-42502) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5027 (CVE-2026-42502) для пакета Go golang.org/x/net версии v0.23.0: Invoking incorrect handling of HTML elements in foreign content in golang.org/x/net/html. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5027
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5027](https://osv.dev/vulnerability/GO-2026-5027) · line 43 · SHA-256 5389cdeb4820dfb70f8dd44fd2d9c150e3e4ea744cb8dced8202c7ed38bf0bc3_

```
{"id": "GO-2026-5027", "aliases": ["CVE-2026-42502"], "modified": "2026-11-23T21:12:29.472586555Z", "summary": "Invoking incorrect handling of HTML elements in foreign content in golang.org/x/net/html", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.55.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50921 — golang.org/x/net v0.23.0 затронут GO-2026-5029 (CVE-2026-25681) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5029 (CVE-2026-25681) для пакета Go golang.org/x/net версии v0.23.0: Invoking incorrect handling of character references in DOCTYPE nodes in golang.org/x/net/html. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5029
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5029](https://osv.dev/vulnerability/GO-2026-5029) · line 43 · SHA-256 c064ba5455b8f417db2c56741f0351bc16de82a8c15c235089038f02c823f383_

```
{"id": "GO-2026-5029", "aliases": ["CVE-2026-25681"], "modified": "2026-11-23T21:12:28.895525167Z", "summary": "Invoking incorrect handling of character references in DOCTYPE nodes in golang.org/x/net/html", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.55.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50922 — golang.org/x/net v0.23.0 затронут GO-2026-5030 (CVE-2026-27136) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5030 (CVE-2026-27136) для пакета Go golang.org/x/net версии v0.23.0: Invoking duplicate attributes can cause XSS in golang.org/x/net/html. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5030
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5030](https://osv.dev/vulnerability/GO-2026-5030) · line 43 · SHA-256 cf1c47436d9a7e5382eac1f7cea5039975382d2829bf382b9020d1d17a0bdff8_

```
{"id": "GO-2026-5030", "aliases": ["CVE-2026-27136"], "modified": "2026-11-23T21:12:28.405165939Z", "summary": "Invoking duplicate attributes can cause XSS in golang.org/x/net/html", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.55.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50923 — golang.org/x/net v0.23.0 затронут GO-2026-5942 (CVE-2026-46600) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5942 (CVE-2026-46600) для пакета Go golang.org/x/net версии v0.23.0: Parsing an invalid SVCB or HTTPS RR can panic in golang.org/x/net/dns/dnsmessage. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Сборка продукта включает golang.org/x/net, но govulncheck не нашёл импорта ни одного затронутого пакета: к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5942
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5942](https://osv.dev/vulnerability/GO-2026-5942) · line 43 · SHA-256 b350c02f839159da0b17f9fc366081b6ecbfab32d57793400c90cafc79008499_

```
{"id": "GO-2026-5942", "aliases": ["BIT-golang-2026-46600", "CVE-2026-46600"], "modified": "2026-08-17T12:25:32.471119200Z", "summary": "Parsing an invalid SVCB or HTTPS RR can panic in golang.org/x/net/dns/dnsmessage", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.56.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50929 — golang.org/x/net v0.23.0 затронут GO-2026-6860 (CVE-2026-78661) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6860 (CVE-2026-78661) для пакета Go golang.org/x/net версии v0.23.0: Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6860
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6860](https://osv.dev/vulnerability/GO-2026-6860) · line 43 · SHA-256 850b298c34c0a0f97f8e85b1a9e277a2618a27421c9c964f241541b7a5147e9e_

```
{"id": "GO-2026-6860", "aliases": ["CVE-2026-78661"], "modified": "2026-10-27T21:30:04.890809062Z", "summary": "Avoid quadratic complexity when coalescing text nodes in html in golang.org/x/net", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.62.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50930 — golang.org/x/net v0.23.0 затронут GO-2026-6866 (CVE-2026-97045) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/net@v0.23.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-6866 (CVE-2026-97045) для пакета Go golang.org/x/net версии v0.23.0: Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. govulncheck проследил вызовы от пакетов продукта через все зависимости: затронутый пакет импортирован, но ни один вызов не доходит до затронутых функций, поэтому к поставляемому коду бюллетень не применим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-6866
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-6866](https://osv.dev/vulnerability/GO-2026-6866) · line 43 · SHA-256 1950021930f2080580e00f4ada7bb415c92766857f916c4a233c6035c68078b8_

```
{"id": "GO-2026-6866", "aliases": ["CVE-2026-97045"], "modified": "2026-10-27T21:45:08.978077289Z", "summary": "Check all ancestor namespace transitions when rendering raw text in html in golang.org/x/net", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость определил govulncheck@v1.9.0 по базе уязвимостей Go от 2026-11-23: граф вызовов от пакетов продукта (без тестов, примеров и бенчмарков) через все зависимости до затронутых функций. Вызовы через рефлексию, unsafe-указатели и ассемблер не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.62.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50979 — 213 бюллетеней в 84 пакет(ах) npm, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:npm:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 15.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 213 бюллетеней (120 с оценкой high или critical) для 84 пакет(ов) npm, которые подтягивают только инструменты разработки или сборки (scroll-contracts/package.json, scroll-contracts/yarn.lock): например, @fastify/busboy@2.1.1 [dev]: GHSA-gxm5-99cw-xjw9, GHSA-x8mw-p69m-v3mx; adm-zip@0.4.16 [dev]: GHSA-7q85-xj36-vmfc, GHSA-8238-w5pm-2374, GHSA-c6fg-446q-cg94, GHSA-j5f4-cc29-5x44, GHSA-p634-w6r4-rjp2, GHSA-rcw4-f5rp-g42v, GHSA-xcpc-8h2w-3j85; ajv@6.12.6 [dev]: GHSA-2g4f-4pwh-qvx6; ajv@8.11.0 [dev]: GHSA-2g4f-4pwh-qvx6; async@2.6.2 [dev]: GHSA-fwr7-v2mv-hh25. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в scroll-contracts/package.json, scroll-contracts/yarn.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · scroll-contracts/package.json · SHA-256 95e67388793186d6151f7b5f952e2ea36c6b0df306b9215e83f587aefebaed52_

```
@fastify/busboy@2.1.1 [dev]: GHSA-gxm5-99cw-xjw9, GHSA-x8mw-p69m-v3mx
adm-zip@0.4.16 [dev]: GHSA-7q85-xj36-vmfc, GHSA-8238-w5pm-2374, GHSA-c6fg-446q-cg94, GHSA-j5f4-cc29-5x44, GHSA-p634-w6r4-rjp2, GHSA-rcw4-f5rp-g42v, GHSA-xcpc-8h2w-3j85
ajv@6.12.6 [dev]: GHSA-2g4f-4pwh-qvx6
ajv@8.11.0 [dev]: GHSA-2g4f-4pwh-qvx6
async@2.6.2 [dev]: GHSA-fwr7-v2mv-hh25
babel-traverse@6.26.0 [dev]: GHSA-67hx-6x53-jw92
base-x@3.0.9 [dev]: GHSA-xq7p-g2vc-g82p
bn.js@4.11.6 [dev]: GHSA-378v-28hj-76wf
bn.js@4.12.0 [dev]: GHSA-378v-28hj-76wf
bn.js@5.2.0 [dev]: GHSA-378v-28hj-76wf
bn.js@5.2.1 [dev]: GHSA-378v-28hj-76wf
brace-expansion@1.1.11 [dev]: GHSA-3jxr-9vmj-r5cp, GHSA-6j4f-fj2g-mc7p, GHSA-f886-m6hf-6m8v, GHSA-mh99-v99m-4gvg, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895, GHSA-v6h2-p8h4-qcjw
brace-expansion@2.0.1 [dev]: GHSA-3jxr-9vmj-r5cp, GHSA-6j4f-fj2g-mc7p, GHSA-f886-m6hf-6m8v, GHSA-mh99-v99m-4gvg, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895, GHSA-v6h2-p8h4-qcjw
braces@2.3.2 [dev]: GHSA-grv7-fg5c-xmjg
braces@3.0.2 [dev]: GHSA-grv7-fg5c-xmjg
browserslist@3.2.8 [dev]: GHSA-73wf-gq98-2v4g, GHSA-c83g-rgw3-j3cx
cipher-base@1.0.4 [dev]: GHSA-cpq7-6gpm-g9rc
cookie@0.4.2 [dev]: GHSA-pxg6-pf52-xh8x
cross-spawn@6.0.5 [dev]: GHSA-3xgq-45jj-v275
cross-spawn@7.0.3 [dev]: GHSA-3xgq-45jj-v275
debug@3.2.6 [dev]: GHSA-gxpj-cx7g-858c
decode-uri-component@0.2.0 [dev]: GHSA-qr28-fpjm-wq7f, GHSA-vcc3-ghjq-m6fr, GHSA-w573-4hg7-7wgq
diff@3.5.0 [dev]: GHSA-73rr-hh4g-fpgx
diff@4.0.2 [dev]: GHSA-73rr-hh4g-fpgx
diff@5.0.0 [dev]: GHSA-73rr-hh4g-fpgx
ejs@3.1.8 [dev]: GHSA-ghr5-ch3p-vcr6
elliptic@6.5.4 [dev]: GHSA-434g-2637-qmqr, GHSA-49q7-c7j4-3p7m, GHSA-848j-6mx2-7j84, GHSA-977x-g7h5-7qgw, GHSA-f7q4-pwc6-w24p, GHSA-fc9h-whq2-v747, GHSA-vjh7-7g9h-fjfh
es5-ext@0.10.60 [dev]: GHSA-4gmj-3p3h-gm8h
flatted@2.0.2 [dev]: GHSA-25h7-pfq9-p65f, GHSA-rf6f-7fwh-wjgh
flatted@3.2.5 [dev]: GHSA-25h7-pfq9-p65f, GHSA-rf6f-7fwh-wjgh
follow-redirects@1.14.9 [dev]: GHSA-cxjh-pqwp-8mfp, GHSA-jchw-25xp-jwwc, GHSA-r4q5-vmmm-2653
form-data@2.3.3 [dev]: GHSA-fjxv-7rqg-78g4, GHSA-hmw2-7cc7-3qxx
form-data@2.5.1 [dev]: GHSA-fjxv-7rqg-78g4, GHSA-hmw2-7cc7-3qxx
form-data@3.0.1 [dev]: GHSA-fjxv-7rqg-78g4, GHSA-hmw2-7cc7-3qxx
get-func-name@2.0.0 [dev]: GHSA-4q6p-r6v2-jvc5
handlebars@4.7.7 [dev]: GHSA-2qvq-rjwj-gvw9, GHSA-2w6w-674q-4c4q, GHSA-3mfm-83xf-c92r, GHSA-442j-39wm-28r2, GHSA-7rx3-28cr-v5wh, GHSA-8r5x-fm3f-whwj, GHSA-9cx6-37pm-9jff, GHSA-p8wg-vrv2-v86f, GHSA-xhpv-hc6g-r9c6, GHSA-xjpj-3mr7-gcpf, GHSA-xw65-4hp5-5hc7
immutable@4.0.0 [dev]: GHSA-v56q-mh7h-f735, GHSA-wf6x-7x77-mvgw, GHSA-xvcm-6775-5m9r
js-yaml@3.13.1 [dev]: GHSA-2883-xcg3-v3hh, GHSA-52cp-r559-cp3m, GHSA-5p4m-2wfm-xmqj, GHSA-h67p-54hq-rp68, GHSA-mh29-5h37-fv8m
js-yaml@3.14.1 [dev]: GHSA-2883-xcg3-v3hh, GHSA-52cp-r559-cp3m, GHSA-5p4m-2wfm-xmqj, GHSA-h67p-54hq-rp68, GHSA-mh29-5h37-fv8m
js-yaml@4.0.0 [dev]: GHSA-2883-xcg3-v3hh, GHSA-52cp-r559-cp3m, GHSA-5p4m-2wfm-xmqj, GHSA-h67p-54hq-rp68, GHSA-mh29-5h37-fv8m
js-yaml@4.1.0 [dev]: GHSA-2883-xcg3-v3hh, GHSA-52cp-r559-cp3m, GHSA-5p4m-2wfm-xmqj, GHSA-h67p-54hq-rp68, GHSA-mh29-5h37-fv8m
json5@0.5.1 [dev]: GHSA-9c47-m6qq-7p4h
json5@1.0.1 [dev]: GHSA-9c47-m6qq-7p4h
lodash@4.17.20 [dev]: GHSA-29mw-wpgm-hmr9, GHSA-35jh-r3h4-6jhm, GHSA-r5fr-rjxr-66jc, GHSA-xxjr-mmjv-4gpg
lodash@4.17.21 [dev]: GHSA-r5fr-rjxr-66jc, GHSA-xxjr-mmjv-4gpg
micromatch@3.1.10 [dev]: GHSA-952p-6rrq-rcjv
micromatch@4.0.5 [dev]: GHSA-952p-6rrq-rcjv
min-document@2.19.0 [dev]: GHSA-rx8g-88g5-qh64
minimatch@3.0.4 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj, GHSA-f8q6-p94x-37v3
minimatch@3.1.2 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
minimatch@5.0.1 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
minimatch@5.1.6 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
minimatch@9.0.3 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj, GHSA-g3hv-75wg-m249
nanoid@3.1.20 [dev]: GHSA-28wg-ghj8-5hjv, GHSA-2v37-7h3g-55p8, GHSA-mwcw-c2x4-8c55, GHSA-qrpm-p2h7-hrv2, GHSA-xwg4-73v4-xw9w
node-fetch@1.7.3 [dev]: GHSA-r683-j2x4-v87g
pbkdf2@3.1.2 [dev]: GHSA-477h-4r7f-fvrx, GHSA-h7cp-r72f-jxh6, GHSA-v62p-rq8g-8h59
picomatch@2.3.1 [dev]: GHSA-3v7f-55p6-f55p, GHSA-c2c7-rcm5-vvqj
qs@6.10.3 [dev]: GHSA-4mjr-xmp4-gh2g, GHSA-6pq8-jhm2-2vcw, GHSA-6rw7-vpxm-498p, GHSA-w7fw-mjwx-w883
qs@6.5.3 [dev]: GHSA-4mjr-xmp4-gh2g, GHSA-6rw7-vpxm-498p
request@2.88.2 [dev]: GHSA-p8p7-x288-28g6
… 24 more
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-50752 — ansi_term 0.12.1: информационный бюллетень RUSTSEC-2021-0139 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/ansi_term@0.12.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50754 — atty 0.2.14: информационный бюллетень RUSTSEC-2024-0375 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/atty@0.2.14`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50758 — chrono 0.4.45: информационный бюллетень RUSTSEC-2026-0543 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/chrono@0.4.45`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2026-0543 для пакета crates.io chrono версии 0.4.45 как информационный (unmaintained): chrono is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0543
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0543](https://osv.dev/vulnerability/RUSTSEC-2026-0543) · manifest · SHA-256 37d2d647609cf3ea819b650afa04f4f974a83c89d3c0613ec3b45f6d0e14c207_

```
{"id": "RUSTSEC-2026-0543", "aliases": [], "modified": "2026-11-17T10:15:02.344223779Z", "summary": "chrono is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-50760 — derivative 2.2.0: информационный бюллетень RUSTSEC-2024-0388 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/derivative@2.2.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50761 — fxhash 0.2.1: информационный бюллетень RUSTSEC-2025-0057 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/fxhash@0.2.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50762 — generational-arena 0.2.9: информационный бюллетень RUSTSEC-2024-0014 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/generational-arena@0.2.9`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50764 — humantime 1.3.0: информационный бюллетень RUSTSEC-2026-0542 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/humantime@1.3.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2026-0542 для пакета crates.io humantime версии 1.3.0 как информационный (unmaintained): humantime is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0542
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0542](https://osv.dev/vulnerability/RUSTSEC-2026-0542) · manifest · SHA-256 caf5ab6a2010add85bc70c11c514b3b9da488452dbd5e9996fdfaff17f0eb536_

```
{"id": "RUSTSEC-2026-0542", "aliases": [], "modified": "2026-11-17T10:15:02.347148964Z", "summary": "humantime is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-50765 — instant 0.1.13: информационный бюллетень RUSTSEC-2024-0384 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/instant@0.1.13`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50766 — libsecp256k1 0.7.2: информационный бюллетень RUSTSEC-2025-0161 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/libsecp256k1@0.7.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50774 — paste 1.0.15: информационный бюллетень RUSTSEC-2024-0436 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/paste@1.0.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

### QSI-2026-50775 — pin-utils 0.1.0: информационный бюллетень RUSTSEC-2026-0441 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/pin-utils@0.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2026-0441 для пакета crates.io pin-utils версии 0.1.0 как информационный (unmaintained): `pin-utils` is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0441
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0441](https://osv.dev/vulnerability/RUSTSEC-2026-0441) · manifest · SHA-256 514334496eebf73f46fcfef878104d886070964aa0d513b9f9078d9475b291ad_

```
{"id": "RUSTSEC-2026-0441", "aliases": [], "modified": "2026-11-05T09:00:02.627533155Z", "summary": "`pin-utils` is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-50776 — proc-macro-error2 2.0.1: информационный бюллетень RUSTSEC-2026-0173 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/proc-macro-error2@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.21.0 · 2026-11-24 17:22 UTC
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

### Отклонено после проверки

_Эти находки аналитик отклонил как ложные срабатывания; в подсчётах отчёта они не учитываются._

| ID | Подробное описание находок | Проверка аналитика |
|---|---|---|
| QSI-2026-50714 | Цель и данные вызова задаёт вызывающий в relayMessageWithProof (scroll-contracts/src/L1/L1ScrollMessenger.sol) | Calling the target a message names is what a cross-domain messenger is for. L1ScrollMessenger.relayMessageWithProof (line 192) makes the call only after the batch holding the L2 message is finalized and the message's Merkle proof checks out against that batch's withdraw root; it refuses the message queue as a target, runs the call with xDomainMessageSender set to the message's sender, and marks a successful message executed. The arbitrary target is the feature, guarded by the proof. |
| QSI-2026-50715 | Возможный повторный вход (внешний вызов до изменения состояния) в scroll-contracts/src/L1/L1ScrollMessenger.sol | Both calls are guarded. relayMessageWithProof (line 192) and replayMessage (the fee sent to feeVault, line 231) run under notInExecution, which refuses to start while xDomainMessageSender holds a message's sender — that is, during another relay — and replayMessage's fee goes to feeVault, which only the owner sets (updateFeeVault, onlyOwner). Sending messages (_sendMessage) is nonReentrant. |
| QSI-2026-50716 | Возможный повторный вход (внешний вызов до изменения состояния) в scroll-contracts/src/L1/L1ScrollMessenger.sol | Both calls are guarded. relayMessageWithProof (line 192) and replayMessage (the fee sent to feeVault, line 231) run under notInExecution, which refuses to start while xDomainMessageSender holds a message's sender — that is, during another relay — and replayMessage's fee goes to feeVault, which only the owner sets (updateFeeVault, onlyOwner). Sending messages (_sendMessage) is nonReentrant. |
| QSI-2026-50731 | Возможный повторный вход (внешний вызов до изменения состояния) в scroll-contracts/src/L2/L2ScrollMessenger.sol | L2ScrollMessenger.relayMessage, whose _executeMessage makes the call at line 159, accepts only the aliased L1 messenger as its caller (AddressAliasHelper.undoL1ToL2Alias(msg.sender) == counterpart), so the called contract cannot enter it again; an executed message is recorded and refused a second time. |

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

### Постквантовая зрелость: Уровень 3 из 4 — гибридная защита в критичном пути

- Гибрид — обмен ключами в канале (TLS, Noise, рукопожатия): bridge-history-api/cmd/api/app/app.go (классическая группа + X25519MLKEM768)
- Используется: X25519MLKEM768 — bridge-history-api/cmd/api/app/app.go
- Гибрид держится только на умолчании тулчейна или библиотеки (Go crypto/tls без CurvePreferences, rustls с aws-lc-rs без prefer-post-quantum): код его не задаёт

**Следующий шаг:** Закрепите версию тулчейна и задайте группы TLS в коде (X25519MLKEM768 первой): найденный гибридный обмен ключами держится на умолчании, которого код не показывает, и смена тулчейна или библиотеки его изменит.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **подпись транзакций и сообщений** | ECDSA (5) | QSI-2026-50708 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |
| **аутентификация и идентификация (сертификаты, токены, аттестация устройств)** | ECDSA (1) | QSI-2026-50707 | Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме |
| **роль не определена** | ECDSA (2) | QSI-2026-50706 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм в конечных полях | взламывает | Q1 | BN254 (alt_bn128) (1) | Взламывает Диффи–Хеллмана в конечных полях и DSA при любом размере. Переводите установление ключей на ML-KEM (на переходный период — гибрид с X25519 или ECDH), подписи — на ML-DSA или SLH-DSA. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | BN254 (alt_bn128) (1), ECDSA (9), X25519MLKEM768 (1) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (36), Poseidon (4), SHA-2 (1), STARK (FRI) (7) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (36), Poseidon (4), SHA-2 (1), STARK (FRI) (7) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |
| Квантовое решетчатое просеивание | учтено в стандартных параметрах | Q1 | X25519MLKEM768 (1) | Для ML-KEM и ML-DSA в стандартных наборах параметров ничего менять не нужно. Заявление 2024 года о полиномиальном квантовом алгоритме для LWE отозвано после обнаружения ошибки (см. заявления). |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- tls_code: 5 (примеры: bridge-history-api/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS; common/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS; coordinator/go.mod: go 1.22 — before Go 1.24 crypto/tls offers no X25519MLKEM768 by default; relevant if the module uses TLS)
- slither: 152 (примеры: slither is not installed on the server (pip install slither-analyzer + solc))
- osv_advisories: 1 (примеры: 137 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: ecies, encoder-standard, ethers-core, halo2-axiom, halo2-axiom-gpu, halo2-base, halo2-ecc, halo2curves-axiom, k256, openvm, openvm-algebra-circuit, openvm-algebra-complex-macros …)
- osv_advisories: 1 (примеры: Go/golang.org/x/crypto@v0.32.0: 21 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest)

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P1 | QSI-2026-50705 | Удалите отключение проверки сертификатов в bridge-history-api/cmd/api/app/app.go. | устранение первопричины | Отключений проверки не осталось вне явно помеченного тестового кода. |
| P2 | QSI-2026-50810 | Обновите github.com/gin-contrib/cors до исправленной версии (1.6.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-869c-j7wc-8jqv (CVE-2019-25211, GO-2024-2955). |
| P2 | QSI-2026-50834 | Обновите golang.org/x/crypto до исправленной версии (0.52.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-f5wc-c3c7-36mc (CVE-2026-39832, GO-2026-5006). |
| P2 | QSI-2026-50838 | Обновите golang.org/x/crypto до исправленной версии (0.52.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-jppx-rxg9-jmrx (CVE-2026-39833, GO-2026-5005). |
| P2 | QSI-2026-50951 | Обновите proxy-addr до исправленной версии (2.0.8). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-jqcg-44mw-7w3h (CVE-2026-90711). |
| P2 | QSI-2026-50971 | Обновите underscore до исправленной версии (1.12.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-cf4h-3jhx-xvhq (CVE-2021-23358). |
| P2 | QSI-2026-50814 | Обновите github.com/consensys/gnark-crypto до исправленной версии (0.18.1, 0.19.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-fj2x-735w-74vq (GO-2025-4087). |
| P2 | QSI-2026-50843 | Обновите golang.org/x/crypto до исправленной версии (0.52.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w879-237q-wc7r (CVE-2026-39829, GO-2026-5018). |
| P2 | QSI-2026-50910 | Обновите github.com/golang-jwt/jwt/v4 до исправленной версии (4.5.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mh63-6h87-95cp (CVE-2025-30204, GO-2025-3553). |
| P2 | QSI-2026-50779 | Обновите quinn-proto до исправленной версии (0.11.18). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2026-0340. |
| P2 | QSI-2026-50780 | Обновите quinn-proto до исправленной версии (0.11.17). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2026-0341. |
| P2 | QSI-2026-50936 | Обновите body-parser до исправленной версии (1.20.9, 2.4.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-27r3-jxmh-p828 (CVE-2026-111181). |
| P2 | QSI-2026-50937 | Обновите body-parser до исправленной версии (1.20.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwcr-r2fm-qrc7 (CVE-2024-45590). |
| P2 | QSI-2026-50939 | Обновите body-parser до исправленной версии (1.20.9, 2.4.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-27r3-jxmh-p828 (CVE-2026-111181). |
| P2 | QSI-2026-50940 | Обновите body-parser до исправленной версии (1.20.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwcr-r2fm-qrc7 (CVE-2024-45590). |
| P2 | QSI-2026-50942 | Обновите browserify-sign до исправленной версии (4.2.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-x9w5-v3q2-3rhw (CVE-2023-46234). |
| P2 | QSI-2026-50948 | Обновите http-cache-semantics до исправленной версии (4.1.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rc47-6667-2j5j (CVE-2022-25881). |
| P2 | QSI-2026-50949 | Обновите path-to-regexp до исправленной версии (0.1.13). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-37ch-88jc-xwx2 (CVE-2024-45296, CVE-2026-4867, GHSA-9wv6-86v2-598j). |
| P2 | QSI-2026-50950 | Обновите path-to-regexp до исправленной версии (0.1.12). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rhx6-c78j-4q9w (CVE-2024-52798). |
| P2 | QSI-2026-50958 | Обновите tar до исправленной версии (7.5.19). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-23hp-3jrh-7fpw (CVE-2026-59873). |
| P2 | QSI-2026-50959 | Обновите tar до исправленной версии (7.5.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-34x7-hfp2-rc4v (CVE-2026-24842). |
| P2 | QSI-2026-50960 | Обновите tar до исправленной версии (7.5.8). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-83g3-92jg-28cx (CVE-2026-26960). |
| P2 | QSI-2026-50961 | Обновите tar до исправленной версии (7.5.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8qq5-rm4j-mr97 (CVE-2026-23745). |
| P2 | QSI-2026-50962 | Обновите tar до исправленной версии (7.5.18). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8x88-c5mf-7j5w (CVE-2026-59874). |
| P2 | QSI-2026-50963 | Обновите tar до исправленной версии (7.5.11). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9ppj-qmqm-q256 (CVE-2026-31802). |
| P2 | QSI-2026-50966 | Обновите tar до исправленной версии (7.5.10). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qffp-2rhf-9h96 (CVE-2026-29786). |
| P2 | QSI-2026-50967 | Обновите tar до исправленной версии (7.5.21). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-r292-9mhp-454m (CVE-2026-73566). |
| P2 | QSI-2026-50968 | Обновите tar до исправленной версии (7.5.4). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-r6q2-hw4h-h46w (CVE-2026-23950). |
| P2 | QSI-2026-50973 | Обновите uuid до исправленной версии (11.1.1, 12.0.1, 13.0.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w5hq-g745-h8pq (CVE-2026-41907, CVE-2026-41988). |
| P2 | QSI-2026-50977 | Обновите ws до исправленной версии (5.2.4, 6.2.3, 7.5.10, 8.17.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3h5v-q93c-6h6q (CVE-2024-37890). |
| P2 | QSI-2026-50978 | Обновите ws до исправленной версии (5.2.5, 6.2.4, 7.5.11, 8.21.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-96hv-2xvq-fx4p (CVE-2026-48779). |
| P2 | QSI-2026-50823 | Обновите github.com/gorilla/websocket до исправленной версии (1.5.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w67g-5rqw-f597 (GO-2026-6278). |
| P2 | QSI-2026-50833 | Обновите golang.org/x/crypto до исправленной версии (0.52.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9m57-25v3-79x9 (CVE-2026-46598, GO-2026-5033). |
| P2 | QSI-2026-50835 | Обновите golang.org/x/crypto до исправленной версии (0.45.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-f6x5-jh6r-wrfv (CVE-2025-47914, GO-2025-4135). |
| P2 | QSI-2026-50851 | Обновите golang.org/x/net до исправленной версии (0.38.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vvgc-356p-c3xw (CVE-2025-22872, GO-2025-3595). |
| P2 | QSI-2026-50913 | Обновите golang.org/x/net до исправленной версии (0.38.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vvgc-356p-c3xw (CVE-2025-22872, GO-2025-3595). |
| P2 | QSI-2026-50931 | Обновите github.com/gorilla/websocket до исправленной версии (1.5.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w67g-5rqw-f597 (GO-2026-6278). |
| P2 | QSI-2026-50932 | Обновите github.com/aws/aws-sdk-go-v2/service/s3 до исправленной версии (1.97.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xmrv-pmrh-hhx2 (CVE-2026-89090, GO-2026-5764). |
| P2 | QSI-2026-50933 | Обновите github.com/aws/aws-sdk-go-v2/aws/protocol/eventstream до исправленной версии (1.7.8). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xmrv-pmrh-hhx2 (CVE-2026-89090, GO-2026-5764). |
| P2 | QSI-2026-50934 | Обновите @openzeppelin/contracts-upgradeable до исправленной версии (4.9.6, 5.0.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9vx6-7xxf-x967 (CVE-2024-27094). |
| P2 | QSI-2026-50935 | Обновите @openzeppelin/contracts до исправленной версии (4.9.6, 5.0.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9vx6-7xxf-x967 (CVE-2024-27094). |
| P2 | QSI-2026-50757 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-50787 | Обновите rustls до исправленной версии (0.23.45). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2mjx-qc3c-rqvc (CVE-2026-123613, RUSTSEC-2026-0285). |
| P2 | QSI-2026-50788 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c8m5-c952-6cm4 (CVE-2026-123609, RUSTSEC-2026-0346). |
| P2 | QSI-2026-50943 | Обновите cookiejar до исправленной версии (2.1.4). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h452-7996-h45h (CVE-2022-25901). |
| P2 | QSI-2026-50944 | Обновите express до исправленной версии (4.20.0, 5.0.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qw6h-vgh9-j6wx (CVE-2024-43796). |
| P2 | QSI-2026-50945 | Обновите express до исправленной версии (4.19.2, 5.0.0-beta.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rv95-896h-c2vc (CVE-2024-29041). |
| P2 | QSI-2026-50946 | Обновите got до исправленной версии (11.8.5, 12.1.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pfrx-2q88-qq97 (CVE-2022-33987). |
| P2 | QSI-2026-50947 | Обновите got до исправленной версии (11.8.5, 12.1.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pfrx-2q88-qq97 (CVE-2022-33987). |
| P2 | QSI-2026-50952 | Обновите qs до исправленной версии (6.16.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4mjr-xmp4-gh2g (CVE-2026-82417). |
| P2 | QSI-2026-50953 | Обновите qs до исправленной версии (6.16.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-6pq8-jhm2-2vcw (CVE-2026-110816). |
| P2 | QSI-2026-50956 | Обновите send до исправленной версии (0.19.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-m6fv-jmcg-4jfg (CVE-2024-43799). |
| P2 | QSI-2026-50957 | Обновите serve-static до исправленной версии (1.16.0, 2.1.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-cm22-4g7w-348p (CVE-2024-43800). |
| P2 | QSI-2026-50964 | Обновите tar до исправленной версии (6.2.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-f5x3-32g6-xq36 (CVE-2024-28863). |
| P2 | QSI-2026-50965 | Обновите tar до исправленной версии (7.5.17). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-gvwx-54wh-qm9j (CVE-2026-59875). |
| P2 | QSI-2026-50969 | Обновите tar до исправленной версии (7.5.16). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vmf3-w455-68vh (CVE-2026-53655). |
| P2 | QSI-2026-50970 | Обновите tar до исправленной версии (7.5.18). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w8wr-v893-vjvp (CVE-2026-59871). |
| P2 | QSI-2026-50972 | Обновите underscore до исправленной версии (1.13.8). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qpx9-hpmf-5gmw (CVE-2026-27601). |
| P2 | QSI-2026-50825 | Обновите github.com/jackc/pgx/v5 до исправленной версии (5.9.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j88v-2chj-qfwx (CVE-2026-41889, GO-2026-5004). |
| P2 | QSI-2026-50909 | Обновите github.com/golang-jwt/jwt/v4 до исправленной версии (4.5.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-29wx-vh33-7x7r (CVE-2024-51744, GO-2024-3250). |
| P2 | QSI-2026-50793 | Обновите tracing-subscriber до исправленной версии (0.3.20). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xwfj-jgwm-7wp5 (CVE-2025-58160, RUSTSEC-2025-0055). |
| P2 | QSI-2026-50769 | Обновите lru до исправленной версии (0.16.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002). |
| P2 | QSI-2026-50771 | Обновите lru до исправленной версии (0.16.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002). |
| P2 | QSI-2026-50773 | Обновите p3-symmetric до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3g92-f9ch-qjcm. |
| P2 | QSI-2026-50790 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w44r-93j7-qv28 (CVE-2026-123611, RUSTSEC-2026-0349). |
| P2 | QSI-2026-50938 | Обновите body-parser до исправленной версии (1.20.6, 2.3.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-v422-hmwv-36x6 (CVE-2026-12590). |
| P2 | QSI-2026-50941 | Обновите body-parser до исправленной версии (1.20.6, 2.3.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-v422-hmwv-36x6 (CVE-2026-12590). |
| P2 | QSI-2026-50954 | Обновите qs до исправленной версии (6.14.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-6rw7-vpxm-498p (CVE-2025-15284). |
| P2 | QSI-2026-50955 | Обновите qs до исправленной версии (6.14.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w7fw-mjwx-w883 (CVE-2026-2391). |
| P2 | QSI-2026-50974 | Обновите web3-core-method до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2j4c-9qqq-896r (CVE-2025-57329). |
| P2 | QSI-2026-50975 | Обновите web3-core-subscriptions до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-hhf6-3xpg-pggx (CVE-2025-57330). |
| P2 | QSI-2026-50976 | Обновите web3 до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-27v7-qhfv-rqq8. |
| P2 | QSI-2026-50789 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h2v8-394m-p7vv (CVE-2026-123610, RUSTSEC-2026-0348). |
| P2 | QSI-2026-50816 | Обновите github.com/docker/docker до исправленной версии (25.0.13, 28.0.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4vq8-7jfc-9cvp (CVE-2025-54410). |
| P2 | QSI-2026-50817 | Обновите github.com/docker/docker до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pxq6-2prw-chj9 (CVE-2026-33997, GO-2026-4883). |
| P2 | QSI-2026-50818 | Обновите github.com/docker/docker до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rg2x-37c3-w2rh (CVE-2026-42306, GO-2026-5617). |
| P2 | QSI-2026-50819 | Обновите github.com/docker/docker до исправленной версии (23.0.15, 25.0.6, 26.1.5, 27.1.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-v23v-6jw2-98fq (CVE-2024-41110, GO-2024-3005). |
| P2 | QSI-2026-50820 | Обновите github.com/docker/docker до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vp62-88p7-qqf5 (CVE-2026-41568, GO-2026-5668). |
| P2 | QSI-2026-50821 | Обновите github.com/docker/docker до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-x86f-5xw2-fm2r (CVE-2026-41567, GO-2026-5746). |
| P2 | QSI-2026-50824 | Обновите github.com/jackc/pgx/v5 до исправленной версии (5.9.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9jj7-4m8r-rfcm (CVE-2026-33816, GO-2026-4772). |
| P2 | QSI-2026-50826 | Обновите github.com/jackc/pgx/v5 до исправленной версии (5.9.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xgrm-4fwx-7qm8 (CVE-2026-33815, GO-2026-4771). |
| P2 | QSI-2026-50811 | Обновите github.com/btcsuite/btcd до исправленной версии (0.24.2-beta.rc1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-27vh-h6mc-q6g8 (CVE-2024-38365, GO-2024-3189). |
| P2 | QSI-2026-50812 | Обновите github.com/btcsuite/btcd до исправленной версии (0.23.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2chg-86hq-7w38 (CVE-2022-44797, GO-2022-1098). |
| P2 | QSI-2026-50813 | Обновите github.com/btcsuite/btcd до исправленной версии (0.24.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3jgf-r68h-xfqm (CVE-2024-34478, GO-2024-2818). |
| P2 | QSI-2026-50815 | Обновите github.com/docker/cli до исправленной версии (29.2.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-p436-gjf2-799p (CVE-2025-15558, GO-2026-4610). |
| P2 | QSI-2026-50827 | Обновите github.com/klauspost/compress до исправленной версии (1.18.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-259r-337f-4rfw (CVE-2026-63209, GO-2026-5841). |
| P2 | QSI-2026-50829 | Обновите golang.org/x/crypto до исправленной версии (0.52.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-45gg-vh54-h5m9 (CVE-2026-39828, GO-2026-5014). |
| P2 | QSI-2026-50830 | Обновите golang.org/x/crypto до исправленной версии (0.52.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-5cgq-3rg8-m6cv (CVE-2026-42508, GO-2026-5021). |
| P2 | QSI-2026-50831 | Обновите golang.org/x/crypto до исправленной версии (0.52.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-78mq-xcr3-xm33 (CVE-2026-39835, GO-2026-5015). |
| P2 | QSI-2026-50832 | Обновите golang.org/x/crypto до исправленной версии (0.52.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-89gr-r52h-f8rx (CVE-2026-39831, GO-2026-5019). |
| P2 | QSI-2026-50836 | Обновите golang.org/x/crypto до исправленной версии (0.35.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-hcg3-q754-cr77 (CVE-2025-22869, GO-2025-3487). |
| P2 | QSI-2026-50837 | Обновите golang.org/x/crypto до исправленной версии (0.45.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j5w8-q4qc-rx2x (CVE-2025-58181, GO-2025-4134). |
| P2 | QSI-2026-50839 | Обновите golang.org/x/crypto до исправленной версии (0.52.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-q4h4-gmj2-qvw2 (CVE-2026-46597, GO-2026-5013). |
| P2 | QSI-2026-50840 | Обновите golang.org/x/crypto до исправленной версии (0.52.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qpw4-5x99-6vjp (CVE-2026-39827, GO-2026-5016). |
| P2 | QSI-2026-50841 | Обновите golang.org/x/crypto до исправленной версии (0.52.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rm3j-f69w-wqmq (CVE-2026-39834, GO-2026-5020). |
| P2 | QSI-2026-50842 | Обновите golang.org/x/crypto до исправленной версии (0.52.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vgwf-h737-ff37 (CVE-2026-39830, GO-2026-5017). |
| P2 | QSI-2026-50844 | Обновите golang.org/x/crypto до исправленной версии (0.52.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-x527-x647-q7gg (CVE-2026-46595). |
| P2 | QSI-2026-50849 | Обновите golang.org/x/net до исправленной версии (0.55.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-5cv4-jp36-h3mw (CVE-2026-25680, GO-2026-5028). |
| P2 | QSI-2026-50850 | Обновите golang.org/x/net до исправленной версии (0.36.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qxp5-gwg8-xv66 (CVE-2025-22870, GO-2025-3503). |
| P2 | QSI-2026-50872 | Обновите github.com/containerd/containerd до исправленной версии (1.6.38, 1.7.27). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-265r-hfxg-fhmg (CVE-2024-40635, GO-2025-3528). |
| P2 | QSI-2026-50873 | Обновите github.com/containerd/containerd до исправленной версии (1.7.35). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7jxh-36q5-gcqv (CVE-2026-53495, GO-2026-6444). |
| P2 | QSI-2026-50874 | Обновите github.com/containerd/containerd до исправленной версии (1.7.33). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-jpcc-p29g-p8mq (CVE-2026-47262, GO-2026-5475). |
| P2 | QSI-2026-50875 | Обновите github.com/containerd/containerd до исправленной версии (1.7.29). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-m6hq-p25p-ffr2 (CVE-2025-64329, GO-2025-4108). |
| P2 | QSI-2026-50876 | Обновите github.com/containerd/containerd до исправленной версии (1.7.36). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pg57-6jwg-q645 (CVE-2026-53493, GO-2026-6597). |
| P2 | QSI-2026-50877 | Обновите github.com/containerd/containerd до исправленной версии (1.7.29). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pwhc-rpq9-4c8w (CVE-2024-25621, GO-2025-4100). |
| P2 | QSI-2026-50878 | Обновите github.com/containerd/containerd до исправленной версии (1.7.35). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rp3h-jf77-q9p4 (CVE-2026-95838, GO-2026-6796). |
| P2 | QSI-2026-50879 | Обновите github.com/containerd/containerd до исправленной версии (1.7.33). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xhf5-7wjv-pqxp (CVE-2026-53488, GO-2026-5758). |
| P2 | QSI-2026-50880 | Обновите github.com/docker/buildx до исправленной версии (0.21.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-m4gq-fm9h-8q75 (CVE-2025-0495, GO-2025-3527). |
| P2 | QSI-2026-50882 | Обновите github.com/docker/distribution до исправленной версии (2.8.4-0.20260923142519-db037680f2ac+incompatible). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-685w-q87j-wqw3 (CVE-2026-85747, GO-2026-6778). |
| P2 | QSI-2026-50883 | Обновите github.com/in-toto/in-toto-golang до исправленной версии (0.11.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pmwq-pjrm-6p5r (GO-2026-5547). |
| P2 | QSI-2026-50884 | Обновите github.com/moby/buildkit до исправленной версии (0.28.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4c29-8rgm-jvjj (CVE-2026-33747, GO-2026-4858). |
| P2 | QSI-2026-50885 | Обновите github.com/moby/buildkit до исправленной версии (0.28.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4vrq-3vrq-g6gg (CVE-2026-33748, GO-2026-4859). |
| P2 | QSI-2026-50886 | Обновите github.com/moby/buildkit до исправленной версии (0.31.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7236-3392-c5c6 (CVE-2026-61711, GO-2026-6255). |
| P2 | QSI-2026-50887 | Обновите github.com/moby/buildkit до исправленной версии (0.31.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-72x6-4j93-7w86 (CVE-2026-61712, GO-2026-6256). |
| P2 | QSI-2026-50888 | Обновите github.com/moby/spdystream до исправленной версии (0.5.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pc3f-x583-g7j2 (CVE-2026-35469, GO-2026-4958). |
| P2 | QSI-2026-50889 | Обновите github.com/moby/sys/user до исправленной версии (0.4.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mjcv-p78q-w5fw (CVE-2026-61801, GO-2026-6686). |
| P2 | QSI-2026-50890 | Обновите go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc до исправленной версии (0.46.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8pgv-569h-w5rw (CVE-2023-47108, GO-2023-2331). |
| P2 | QSI-2026-50892 | Обновите go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp до исправленной версии (1.43.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w8rr-5gcm-pp58 (CVE-2026-39882, GO-2026-4985). |
| P2 | QSI-2026-50893 | Обновите go.opentelemetry.io/otel/exporters/otlp/otlptrace до исправленной версии (1.45.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8wmf-6v46-5gfg (CVE-2026-81870, GO-2026-6505). |
| P2 | QSI-2026-50894 | Обновите go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc до исправленной версии (1.45.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8wmf-6v46-5gfg (CVE-2026-81870, GO-2026-6505). |
| P2 | QSI-2026-50895 | Обновите go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp до исправленной версии (1.45.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8wmf-6v46-5gfg (CVE-2026-81870, GO-2026-6505). |
| P2 | QSI-2026-50896 | Обновите go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp до исправленной версии (1.43.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w8rr-5gcm-pp58 (CVE-2026-39882, GO-2026-4985). |
| P2 | QSI-2026-50897 | Обновите go.opentelemetry.io/otel/sdk до исправленной версии (1.45.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8wmf-6v46-5gfg (CVE-2026-81870, GO-2026-6505). |
| P2 | QSI-2026-50898 | Обновите go.opentelemetry.io/otel/sdk до исправленной версии (1.40.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9h8m-3fm2-qjrq (CVE-2026-24051, GO-2026-4394). |
| P2 | QSI-2026-50899 | Обновите go.opentelemetry.io/otel/sdk до исправленной версии (1.43.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-hfvc-g4fc-pqhx (CVE-2026-39883, GO-2026-5426). |
| P2 | QSI-2026-50900 | Обновите go.opentelemetry.io/otel/sdk до исправленной версии (1.33.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-p9f8-wvj8-2fg8 (CVE-2026-81869, GO-2026-6616). |
| P2 | QSI-2026-50903 | Обновите golang.org/x/oauth2 до исправленной версии (0.27.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-6v2p-p543-phr9 (CVE-2025-22868, GO-2025-3488). |
| P2 | QSI-2026-50904 | Обновите google.golang.org/grpc до исправленной версии (1.82.2, 1.83.2, 1.84.0-dev.0.20260825144003-d5a41119e0e3, 1.85.0-dev.0.20260825072537-93e31b48545e). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2v4p-qf9q-27wj (CVE-2026-84445, GO-2026-6443). |
| P2 | QSI-2026-50905 | Обновите google.golang.org/grpc до исправленной версии (1.82.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-hrxh-6v49-42gf (GO-2026-6061). |
| P2 | QSI-2026-50906 | Обновите google.golang.org/grpc до исправленной версии (1.79.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-p77j-4mvh-x3m3 (CVE-2026-33186, GO-2026-4762). |
| P2 | QSI-2026-50907 | Обновите google.golang.org/grpc до исправленной версии (1.83.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qc2q-p7wx-3px3 (CVE-2026-84303, GO-2026-6441). |
| P2 | QSI-2026-50908 | Обновите google.golang.org/grpc до исправленной версии (1.83.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vp52-pcj8-j9qc (CVE-2026-84304, GO-2026-6348). |
| P2 | QSI-2026-50911 | Обновите golang.org/x/net до исправленной версии (0.55.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-5cv4-jp36-h3mw (CVE-2026-25680, GO-2026-5028). |
| P2 | QSI-2026-50912 | Обновите golang.org/x/net до исправленной версии (0.36.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qxp5-gwg8-xv66 (CVE-2025-22870, GO-2025-3503). |
| P2 | QSI-2026-50753 | Обновите atty до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-g98v-hv3f-hcfr (RUSTSEC-2021-0145). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-50718 | Не полагайтесь на код вызывающего. То, что защищала эта проверка, защитите блокировкой повторного входа, лимитами на блок или транзакцию, схемой commit-reveal или белым списком; если вызывающий действительно должен быть без кода, проверяйте происхождение и размер кода вместе. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P2 | QSI-2026-50746 | Используйте OpenZeppelin SafeERC20 (safeTransfer, safeTransferFrom, forceApprove) или эквивалент, принимающий и пустой ответ, и true. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-50828 | Разберите GO-2026-6865 (CVE-2026-116591); при необходимости обновите github.com/klauspost/compress до исправленной версии (1.20.2). | устранение первопричины | Сканирование больше не сообщает GO-2026-6865 (CVE-2026-116591) или результат разбора записан. |
| P3 | QSI-2026-50845 | Разберите GO-2025-4116 (CVE-2025-47913); при необходимости обновите golang.org/x/crypto до исправленной версии (0.43.0). | устранение первопричины | Сканирование больше не сообщает GO-2025-4116 (CVE-2025-47913) или результат разбора записан. |
| P3 | QSI-2026-50855 | Разберите GO-2026-4918 (CVE-2026-33814); при необходимости обновите golang.org/x/net до исправленной версии (0.53.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-4918 (CVE-2026-33814) или результат разбора записан. |
| P3 | QSI-2026-50857 | Разберите GO-2026-5026 (CVE-2026-39821); при необходимости обновите golang.org/x/net до исправленной версии (0.57.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5026 (CVE-2026-39821) или результат разбора записан. |
| P3 | QSI-2026-50862 | Разберите GO-2026-6603 (CVE-2026-78659); при необходимости обновите golang.org/x/net до исправленной версии (0.60.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6603 (CVE-2026-78659) или результат разбора записан. |
| P3 | QSI-2026-50863 | Разберите GO-2026-6610 (CVE-2026-78660); при необходимости обновите golang.org/x/net до исправленной версии (0.60.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6610 (CVE-2026-78660) или результат разбора записан. |
| P3 | QSI-2026-50864 | Разберите GO-2026-6611 (CVE-2026-78669); при необходимости обновите golang.org/x/net до исправленной версии (0.60.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6611 (CVE-2026-78669) или результат разбора записан. |
| P3 | QSI-2026-50865 | Разберите GO-2026-6612 (CVE-2026-78663); при необходимости обновите golang.org/x/net до исправленной версии (0.60.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6612 (CVE-2026-78663) или результат разбора записан. |
| P3 | QSI-2026-50866 | Разберите GO-2026-6617 (CVE-2026-97032); при необходимости обновите golang.org/x/net до исправленной версии (0.60.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6617 (CVE-2026-97032) или результат разбора записан. |
| P3 | QSI-2026-50870 | Разберите GO-2026-5970 (CVE-2026-56852); при необходимости обновите golang.org/x/text до исправленной версии (0.39.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5970 (CVE-2026-56852) или результат разбора записан. |
| P3 | QSI-2026-50871 | Разберите GO-2026-6629 (CVE-2026-56851); при необходимости обновите golang.org/x/text до исправленной версии (0.41.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6629 (CVE-2026-56851) или результат разбора записан. |
| P3 | QSI-2026-50917 | Разберите GO-2026-4918 (CVE-2026-33814); при необходимости обновите golang.org/x/net до исправленной версии (0.53.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-4918 (CVE-2026-33814) или результат разбора записан. |
| P3 | QSI-2026-50919 | Разберите GO-2026-5026 (CVE-2026-39821); при необходимости обновите golang.org/x/net до исправленной версии (0.57.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5026 (CVE-2026-39821) или результат разбора записан. |
| P3 | QSI-2026-50924 | Разберите GO-2026-6603 (CVE-2026-78659); при необходимости обновите golang.org/x/net до исправленной версии (0.60.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6603 (CVE-2026-78659) или результат разбора записан. |
| P3 | QSI-2026-50925 | Разберите GO-2026-6610 (CVE-2026-78660); при необходимости обновите golang.org/x/net до исправленной версии (0.60.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6610 (CVE-2026-78660) или результат разбора записан. |
| P3 | QSI-2026-50926 | Разберите GO-2026-6611 (CVE-2026-78669); при необходимости обновите golang.org/x/net до исправленной версии (0.60.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6611 (CVE-2026-78669) или результат разбора записан. |
| P3 | QSI-2026-50927 | Разберите GO-2026-6612 (CVE-2026-78663); при необходимости обновите golang.org/x/net до исправленной версии (0.60.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6612 (CVE-2026-78663) или результат разбора записан. |
| P3 | QSI-2026-50928 | Разберите GO-2026-6617 (CVE-2026-97032); при необходимости обновите golang.org/x/net до исправленной версии (0.60.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6617 (CVE-2026-97032) или результат разбора записан. |
| P3 | QSI-2026-50759 | Разберите RUSTSEC-2026-0387; при необходимости обновите crypto-bigint до исправленной версии (0.7.6). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0387 или результат разбора записан. |
| P3 | QSI-2026-50763 | Разберите RUSTSEC-2026-0258; при необходимости обновите h2 до исправленной версии (0.4.16). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0258 или результат разбора записан. |
| P3 | QSI-2026-50767 | Разберите RUSTSEC-2026-0418; при необходимости обновите libz-sys до исправленной версии (1.1.31). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0418 или результат разбора записан. |
| P3 | QSI-2026-50768 | Разберите RUSTSEC-2026-0544 (CVE-2026-85091); при необходимости обновите libz-sys до исправленной версии (1.1.33). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0544 (CVE-2026-85091) или результат разбора записан. |
| P3 | QSI-2026-50770 | Разберите RUSTSEC-2026-0253; при необходимости обновите lru до исправленной версии (0.18.2). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0253 или результат разбора записан. |
| P3 | QSI-2026-50772 | Разберите RUSTSEC-2026-0253; при необходимости обновите lru до исправленной версии (0.18.2). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0253 или результат разбора записан. |
| P3 | QSI-2026-50777 | Разберите RUSTSEC-2026-0338; при необходимости обновите quinn-proto до исправленной версии (0.11.18). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0338 или результат разбора записан. |
| P3 | QSI-2026-50778 | Разберите RUSTSEC-2026-0339; при необходимости обновите quinn-proto до исправленной версии (0.11.17). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0339 или результат разбора записан. |
| P3 | QSI-2026-50781 | Разберите RUSTSEC-2026-0342; при необходимости обновите quinn-proto до исправленной версии (0.11.17). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0342 или результат разбора записан. |
| P3 | QSI-2026-50782 | Разберите RUSTSEC-2026-0523; при необходимости обновите quinn-proto до исправленной версии (0.11.19). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0523 или результат разбора записан. |
| P3 | QSI-2026-50783 | Разберите RUSTSEC-2026-0524; при необходимости обновите quinn-proto до исправленной версии (0.11.19). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0524 или результат разбора записан. |
| P3 | QSI-2026-50784 | Разберите RUSTSEC-2026-0538; при необходимости обновите quinn-udp до исправленной версии (0.5.16, 0.6.3). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0538 или результат разбора записан. |
| P3 | QSI-2026-50785 | Разберите RUSTSEC-2026-0220; при необходимости обновите ruint до исправленной версии (1.20.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0220 или результат разбора записан. |
| P3 | QSI-2026-50786 | Разберите RUSTSEC-2026-0486; при необходимости обновите rustix до исправленной версии (1.1.6). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0486 или результат разбора записан. |
| P3 | QSI-2026-50791 | Разберите RUSTSEC-2026-0382 (CVE-2026-111943); при необходимости обновите rustls-webpki до исправленной версии (0.103.16, 0.104.0-alpha.8). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0382 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-50795 | Разберите RUSTSEC-2026-0381 (CVE-2026-111943); при необходимости обновите webpki-roots до исправленной версии (0.26.11, 1.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0381 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-50796 | Разберите RUSTSEC-2026-0391; при необходимости обновите zstd до исправленной версии (0.13.4, 0.14.3). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0391 или результат разбора записан. |
| P3 | QSI-2026-50797 | Разберите RUSTSEC-2026-0395; при необходимости обновите zstd-safe до исправленной версии (7.4.0, 8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0395 или результат разбора записан. |
| P3 | QSI-2026-50798 | Разберите RUSTSEC-2026-0396; при необходимости обновите zstd-safe до исправленной версии (7.4.0, 8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0396 или результат разбора записан. |
| P3 | QSI-2026-50799 | Разберите RUSTSEC-2026-0397; при необходимости обновите zstd-safe до исправленной версии (7.4.0, 8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0397 или результат разбора записан. |
| P3 | QSI-2026-50800 | Разберите RUSTSEC-2026-0398; при необходимости обновите zstd-safe до исправленной версии (7.4.0, 8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0398 или результат разбора записан. |
| P3 | QSI-2026-50801 | Разберите RUSTSEC-2026-0399; при необходимости обновите zstd-safe до исправленной версии (7.4.0, 8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0399 или результат разбора записан. |
| P3 | QSI-2026-50802 | Разберите RUSTSEC-2026-0400; при необходимости обновите zstd-safe до исправленной версии (7.4.0, 8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0400 или результат разбора записан. |
| P3 | QSI-2026-50803 | Разберите RUSTSEC-2026-0401; при необходимости обновите zstd-safe до исправленной версии (7.4.0, 8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0401 или результат разбора записан. |
| P3 | QSI-2026-50804 | Разберите RUSTSEC-2026-0402; при необходимости обновите zstd-safe до исправленной версии (7.4.0, 8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0402 или результат разбора записан. |
| P3 | QSI-2026-50805 | Разберите RUSTSEC-2026-0403; при необходимости обновите zstd-safe до исправленной версии (7.4.0, 8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0403 или результат разбора записан. |
| P3 | QSI-2026-50806 | Разберите RUSTSEC-2026-0404; при необходимости обновите zstd-safe до исправленной версии (7.4.0, 8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0404 или результат разбора записан. |
| P3 | QSI-2026-50807 | Разберите RUSTSEC-2026-0405; при необходимости обновите zstd-safe до исправленной версии (7.4.0, 8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0405 или результат разбора записан. |
| P3 | QSI-2026-50808 | Разберите RUSTSEC-2026-0406; при необходимости обновите zstd-safe до исправленной версии (7.4.0, 8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0406 или результат разбора записан. |
| P3 | QSI-2026-50792 | Разберите RUSTSEC-2026-0386; при необходимости обновите tokio до исправленной версии (1.51.6, 1.53.3). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0386 или результат разбора записан. |
| P3 | QSI-2026-50794 | Разберите RUSTSEC-2026-0592; при необходимости обновите url до исправленной версии (2.5.9). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0592 или результат разбора записан. |
| P3 | QSI-2026-50809 | Разберите RUSTSEC-2026-0410; при необходимости обновите zstd-sys до исправленной версии (2.1.2). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0410 или результат разбора записан. |
| P3 | QSI-2026-50822 | Разберите GO-2026-4887 (CVE-2026-34040); при необходимости обновите github.com/docker/docker до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование больше не сообщает GO-2026-4887 (CVE-2026-34040) или результат разбора записан. |
| P3 | QSI-2026-50846 | Разберите GO-2026-5932; при необходимости обновите golang.org/x/crypto до исправленной версии (0.58.1-0.20261009181718-2f1f834330b2). | устранение первопричины | Сканирование больше не сообщает GO-2026-5932 или результат разбора записан. |
| P3 | QSI-2026-50847 | Разберите GO-2026-6303 (CVE-2026-56854); при необходимости обновите golang.org/x/crypto до исправленной версии (0.55.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6303 (CVE-2026-56854) или результат разбора записан. |
| P3 | QSI-2026-50848 | Разберите GO-2026-6354 (CVE-2026-78662); при необходимости обновите golang.org/x/crypto до исправленной версии (0.56.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6354 (CVE-2026-78662) или результат разбора записан. |
| P3 | QSI-2026-50852 | Разберите GO-2024-3333 (CVE-2024-45338); при необходимости обновите golang.org/x/net до исправленной версии (0.33.0). | устранение первопричины | Сканирование больше не сообщает GO-2024-3333 (CVE-2024-45338) или результат разбора записан. |
| P3 | QSI-2026-50853 | Разберите GO-2026-4440 (CVE-2025-47911); при необходимости обновите golang.org/x/net до исправленной версии (0.45.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-4440 (CVE-2025-47911) или результат разбора записан. |
| P3 | QSI-2026-50854 | Разберите GO-2026-4441 (CVE-2025-58190); при необходимости обновите golang.org/x/net до исправленной версии (0.45.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-4441 (CVE-2025-58190) или результат разбора записан. |
| P3 | QSI-2026-50856 | Разберите GO-2026-5025 (CVE-2026-42506); при необходимости обновите golang.org/x/net до исправленной версии (0.55.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5025 (CVE-2026-42506) или результат разбора записан. |
| P3 | QSI-2026-50858 | Разберите GO-2026-5027 (CVE-2026-42502); при необходимости обновите golang.org/x/net до исправленной версии (0.55.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5027 (CVE-2026-42502) или результат разбора записан. |
| P3 | QSI-2026-50859 | Разберите GO-2026-5029 (CVE-2026-25681); при необходимости обновите golang.org/x/net до исправленной версии (0.55.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5029 (CVE-2026-25681) или результат разбора записан. |
| P3 | QSI-2026-50860 | Разберите GO-2026-5030 (CVE-2026-27136); при необходимости обновите golang.org/x/net до исправленной версии (0.55.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5030 (CVE-2026-27136) или результат разбора записан. |
| P3 | QSI-2026-50861 | Разберите GO-2026-5942 (CVE-2026-46600); при необходимости обновите golang.org/x/net до исправленной версии (0.56.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5942 (CVE-2026-46600) или результат разбора записан. |
| P3 | QSI-2026-50867 | Разберите GO-2026-6860 (CVE-2026-78661); при необходимости обновите golang.org/x/net до исправленной версии (0.62.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6860 (CVE-2026-78661) или результат разбора записан. |
| P3 | QSI-2026-50868 | Разберите GO-2026-6866 (CVE-2026-97045); при необходимости обновите golang.org/x/net до исправленной версии (0.62.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6866 (CVE-2026-97045) или результат разбора записан. |
| P3 | QSI-2026-50869 | Разберите GO-2026-5024 (CVE-2026-39824); при необходимости обновите golang.org/x/sys до исправленной версии (0.44.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5024 (CVE-2026-39824) или результат разбора записан. |
| P3 | QSI-2026-50881 | Разберите GO-2025-4077 (CVE-2025-62725); при необходимости обновите github.com/docker/compose/v2 до исправленной версии (2.40.2). | устранение первопричины | Сканирование больше не сообщает GO-2025-4077 (CVE-2025-62725) или результат разбора записан. |
| P3 | QSI-2026-50891 | Разберите GO-2026-6975 (CVE-2026-128086); при необходимости обновите go.opentelemetry.io/otel до исправленной версии (1.47.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6975 (CVE-2026-128086) или результат разбора записан. |
| P3 | QSI-2026-50901 | Разберите GO-2026-6179 (CVE-2026-56865); при необходимости обновите golang.org/x/mod до исправленной версии (0.40.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6179 (CVE-2026-56865) или результат разбора записан. |
| P3 | QSI-2026-50902 | Разберите GO-2026-6180 (CVE-2026-56864); при необходимости обновите golang.org/x/mod до исправленной версии (0.40.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6180 (CVE-2026-56864) или результат разбора записан. |
| P3 | QSI-2026-50914 | Разберите GO-2024-3333 (CVE-2024-45338); при необходимости обновите golang.org/x/net до исправленной версии (0.33.0). | устранение первопричины | Сканирование больше не сообщает GO-2024-3333 (CVE-2024-45338) или результат разбора записан. |
| P3 | QSI-2026-50915 | Разберите GO-2026-4440 (CVE-2025-47911); при необходимости обновите golang.org/x/net до исправленной версии (0.45.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-4440 (CVE-2025-47911) или результат разбора записан. |
| P3 | QSI-2026-50916 | Разберите GO-2026-4441 (CVE-2025-58190); при необходимости обновите golang.org/x/net до исправленной версии (0.45.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-4441 (CVE-2025-58190) или результат разбора записан. |
| P3 | QSI-2026-50918 | Разберите GO-2026-5025 (CVE-2026-42506); при необходимости обновите golang.org/x/net до исправленной версии (0.55.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5025 (CVE-2026-42506) или результат разбора записан. |
| P3 | QSI-2026-50920 | Разберите GO-2026-5027 (CVE-2026-42502); при необходимости обновите golang.org/x/net до исправленной версии (0.55.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5027 (CVE-2026-42502) или результат разбора записан. |
| P3 | QSI-2026-50921 | Разберите GO-2026-5029 (CVE-2026-25681); при необходимости обновите golang.org/x/net до исправленной версии (0.55.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5029 (CVE-2026-25681) или результат разбора записан. |
| P3 | QSI-2026-50922 | Разберите GO-2026-5030 (CVE-2026-27136); при необходимости обновите golang.org/x/net до исправленной версии (0.55.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5030 (CVE-2026-27136) или результат разбора записан. |
| P3 | QSI-2026-50923 | Разберите GO-2026-5942 (CVE-2026-46600); при необходимости обновите golang.org/x/net до исправленной версии (0.56.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5942 (CVE-2026-46600) или результат разбора записан. |
| P3 | QSI-2026-50929 | Разберите GO-2026-6860 (CVE-2026-78661); при необходимости обновите golang.org/x/net до исправленной версии (0.62.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6860 (CVE-2026-78661) или результат разбора записан. |
| P3 | QSI-2026-50930 | Разберите GO-2026-6866 (CVE-2026-97045); при необходимости обновите golang.org/x/net до исправленной версии (0.62.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-6866 (CVE-2026-97045) или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-50708 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-50706 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-50707 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-50748 | Внесите использования ? в contract:scroll-contracts/src/libraries/verifier/RollupVerifier.sol в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-50712 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-50713 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-50742 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50708 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-50706 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-50707 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-50748 | Запланируйте миграцию ? на ? (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ? или гибридной схемы. |
| P4 | QSI-2026-50710 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50717 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50719 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50720 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50721 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50722 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50723 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50724 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50725 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50726 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50727 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50728 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50729 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50730 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50732 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50733 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50734 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50735 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50736 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50737 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50738 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50739 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50740 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50741 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50743 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50744 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50745 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50747 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50749 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50750 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50751 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50711 | Используйте OpenZeppelin ECDSA.recover с разделением доменов EIP-712 и nonce. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50709 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-50755 | Замените bincode поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | bincode заменён или решение зафиксировано. |
| P4 | QSI-2026-50756 | Замените bincode поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | bincode заменён или решение зафиксировано. |
| P4 | QSI-2026-50979 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |
| P4 | QSI-2026-50752 | Замените ansi_term поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | ansi_term заменён или решение зафиксировано. |
| P4 | QSI-2026-50754 | Замените atty поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | atty заменён или решение зафиксировано. |
| P4 | QSI-2026-50758 | Замените chrono поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | chrono заменён или решение зафиксировано. |
| P4 | QSI-2026-50760 | Замените derivative поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | derivative заменён или решение зафиксировано. |
| P4 | QSI-2026-50761 | Замените fxhash поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | fxhash заменён или решение зафиксировано. |
| P4 | QSI-2026-50762 | Замените generational-arena поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | generational-arena заменён или решение зафиксировано. |
| P4 | QSI-2026-50764 | Замените humantime поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | humantime заменён или решение зафиксировано. |
| P4 | QSI-2026-50765 | Замените instant поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | instant заменён или решение зафиксировано. |
| P4 | QSI-2026-50766 | Замените libsecp256k1 поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | libsecp256k1 заменён или решение зафиксировано. |
| P4 | QSI-2026-50774 | Замените paste поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | paste заменён или решение зафиксировано. |
| P4 | QSI-2026-50775 | Замените pin-utils поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | pin-utils заменён или решение зафиксировано. |
| P4 | QSI-2026-50776 | Замените proc-macro-error2 поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | proc-macro-error2 заменён или решение зафиксировано. |

## 11. Использованные инструменты

- blockchain 1.0.0
- certificates 1.2.0
- chain_map 1.0.0
- configs 1.1.0
- crediting 1.4.0
- dependencies 1.6.1
- hndl 1.0.0
- inventory_document 1.1.0
- key_storage 1.0.0
- mpc 1.0.0
- solidity 1.8.1
- source_code 1.11.0
- tls_code 1.1.0
- tls_live 1.0.0
- ton_contracts 1.0.0
- validator_keys 1.2.0
- wallet_login 1.0.0
- qsi-engine 1.21.0
- OSV.dev API v1

## 12. Источники и нормативные документы

1. A. Becker, L. Ducas, N. Gama, T. Laarhoven — New directions in nearest neighbor searching with applications to lattice sieving (SODA 2016; IACR ePrint 2015/1128) — IACR ePrint. <https://eprint.iacr.org/2015/1128> (peer-reviewed article: classical sieving in 2^{0.292n + o(n)})
2. A. Chailloux, J. Loyer — Lattice sieving via quantum random walks (ASIACRYPT 2021; IACR ePrint 2021/570) — IACR ePrint. <https://eprint.iacr.org/2021/570> (peer-reviewed article: 2^{0.2570d + o(d)}, previously 2^{0.2653d + o(d)} (Laarhoven))
3. A. Chailloux, M. Naya-Plasencia, A. Schrottenloher — An Efficient Quantum Collision Search Algorithm and Implications on Symmetric Cryptography (ASIACRYPT 2017; IACR ePrint 2017/847) — IACR ePrint. <https://eprint.iacr.org/2017/847> (peer-reviewed article: Õ(2^{2n/5}) time, O(n) qubits, Õ(2^{n/5}) classical memory)
4. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
5. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
6. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
7. CRYSTALS-Kyber — Algorithm Specifications and Supporting Documentation (round 3, 2021-08-04) — CRYSTALS team. <https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf> (NIST round-3 submission: core-SVP cost 2^{0.292β} classical, 2^{0.265β} quantum; Kyber768 166 quantum bits)
8. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
9. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
10. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
11. EIP-197 — Precompiled contract for optimal ate pairing check on alt_bn128 (0x08) — Ethereum. <https://eips.ethereum.org/EIPS/eip-197> (final)
12. EIP-2537 — Precompile for BLS12-381 curve operations (0x0b–0x11) — Ethereum. <https://eips.ethereum.org/EIPS/eip-2537> (final)
13. EIP-7702 — Set Code for EOAs — Ethereum Improvement Proposals. <https://eips.ethereum.org/EIPS/eip-7702> (final; activated on Ethereum mainnet with Pectra (May 2025): an externally owned account can delegate to contract code, so msg.sender == tx.origin and code-size tests no longer identify a codeless caller)
14. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
15. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
16. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
17. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
18. J. Groth — On the Size of Pairing-based Non-interactive Arguments (EUROCRYPT 2016) — IACR. <https://eprint.iacr.org/2016/260> (peer-reviewed article)
19. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
20. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
21. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
22. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
23. M. Ekerå, J. Gärtner — A high-level comparison of state-of-the-art quantum algorithms for breaking asymmetric cryptography (arXiv:2405.14381) — arXiv. <https://arxiv.org/abs/2405.14381> (preprint (2024-05-23): Regev-style algorithms show no overall advantage yet for cryptographic RSA and finite-field sizes)
24. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
25. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
26. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
27. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
28. OSV advisory GHSA-23hp-3jrh-7fpw — OSV.dev. <https://osv.dev/vulnerability/GHSA-23hp-3jrh-7fpw> (modified 2026-09-10T03:51:09.781853040Z)
29. OSV advisory GHSA-259r-337f-4rfw — OSV.dev. <https://osv.dev/vulnerability/GHSA-259r-337f-4rfw> (modified 2026-10-20T14:45:03.782718646Z)
30. OSV advisory GHSA-265r-hfxg-fhmg — OSV.dev. <https://osv.dev/vulnerability/GHSA-265r-hfxg-fhmg> (modified 2026-09-10T03:50:06.145474067Z)
31. OSV advisory GHSA-27r3-jxmh-p828 — OSV.dev. <https://osv.dev/vulnerability/GHSA-27r3-jxmh-p828> (modified 2026-10-23T21:00:06.131613693Z)
32. OSV advisory GHSA-27v7-qhfv-rqq8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-27v7-qhfv-rqq8> (modified 2021-08-31T20:56:47Z)
33. OSV advisory GHSA-27vh-h6mc-q6g8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-27vh-h6mc-q6g8> (modified 2025-08-21T04:05:13Z)
34. OSV advisory GHSA-29wx-vh33-7x7r — OSV.dev. <https://osv.dev/vulnerability/GHSA-29wx-vh33-7x7r> (modified 2026-09-10T03:50:20.232143805Z)
35. OSV advisory GHSA-2chg-86hq-7w38 — OSV.dev. <https://osv.dev/vulnerability/GHSA-2chg-86hq-7w38> (modified 2024-05-20T21:36:55Z)
36. OSV advisory GHSA-2j4c-9qqq-896r — OSV.dev. <https://osv.dev/vulnerability/GHSA-2j4c-9qqq-896r> (modified 2025-09-26T13:27:21.954183Z)
37. OSV advisory GHSA-2mjx-qc3c-rqvc — OSV.dev. <https://osv.dev/vulnerability/GHSA-2mjx-qc3c-rqvc> (modified 2026-11-08T10:55:54.395419388Z)
38. OSV advisory GHSA-2v4p-qf9q-27wj — OSV.dev. <https://osv.dev/vulnerability/GHSA-2v4p-qf9q-27wj> (modified 2026-09-25T18:00:05.270054427Z)
39. OSV advisory GHSA-34x7-hfp2-rc4v — OSV.dev. <https://osv.dev/vulnerability/GHSA-34x7-hfp2-rc4v> (modified 2026-09-10T03:50:32.616577975Z)
40. OSV advisory GHSA-37ch-88jc-xwx2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-37ch-88jc-xwx2> (modified 2026-09-10T03:50:36.768786245Z)
41. OSV advisory GHSA-3g92-f9ch-qjcm — OSV.dev. <https://osv.dev/vulnerability/GHSA-3g92-f9ch-qjcm> (modified 2026-04-16T23:04:45.978452Z)
42. OSV advisory GHSA-3h5v-q93c-6h6q — OSV.dev. <https://osv.dev/vulnerability/GHSA-3h5v-q93c-6h6q> (modified 2026-09-10T03:50:14.788589634Z)
43. OSV advisory GHSA-3jgf-r68h-xfqm — OSV.dev. <https://osv.dev/vulnerability/GHSA-3jgf-r68h-xfqm> (modified 2024-08-07T19:55:49Z)
44. OSV advisory GHSA-45gg-vh54-h5m9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-45gg-vh54-h5m9> (modified 2026-09-10T03:51:07.761861882Z)
45. OSV advisory GHSA-4c29-8rgm-jvjj — OSV.dev. <https://osv.dev/vulnerability/GHSA-4c29-8rgm-jvjj> (modified 2026-09-10T03:50:37.172155078Z)
46. OSV advisory GHSA-4mjr-xmp4-gh2g — OSV.dev. <https://osv.dev/vulnerability/GHSA-4mjr-xmp4-gh2g> (modified 2026-09-10T03:51:14.991984096Z)
47. OSV advisory GHSA-4vq8-7jfc-9cvp — OSV.dev. <https://osv.dev/vulnerability/GHSA-4vq8-7jfc-9cvp> (modified 2026-09-10T03:50:25.738441655Z)
48. OSV advisory GHSA-4vrq-3vrq-g6gg — OSV.dev. <https://osv.dev/vulnerability/GHSA-4vrq-3vrq-g6gg> (modified 2026-09-10T03:50:59.724878717Z)
49. OSV advisory GHSA-5cgq-3rg8-m6cv — OSV.dev. <https://osv.dev/vulnerability/GHSA-5cgq-3rg8-m6cv> (modified 2026-09-10T03:50:48.271021372Z)
50. OSV advisory GHSA-5cv4-jp36-h3mw — OSV.dev. <https://osv.dev/vulnerability/GHSA-5cv4-jp36-h3mw> (modified 2026-09-10T03:50:45.494180024Z)
51. OSV advisory GHSA-685w-q87j-wqw3 — OSV.dev. <https://osv.dev/vulnerability/GHSA-685w-q87j-wqw3> (modified 2026-11-05T23:25:40.391377389Z)
52. OSV advisory GHSA-6pq8-jhm2-2vcw — OSV.dev. <https://osv.dev/vulnerability/GHSA-6pq8-jhm2-2vcw> (modified 2026-10-27T16:15:05.324423680Z)
53. OSV advisory GHSA-6rw7-vpxm-498p — OSV.dev. <https://osv.dev/vulnerability/GHSA-6rw7-vpxm-498p> (modified 2026-09-10T03:50:31.670581449Z)
54. OSV advisory GHSA-6v2p-p543-phr9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-6v2p-p543-phr9> (modified 2026-09-10T03:50:26.016569187Z)
55. OSV advisory GHSA-7236-3392-c5c6 — OSV.dev. <https://osv.dev/vulnerability/GHSA-7236-3392-c5c6> (modified 2026-09-10T03:51:13.277422932Z)
56. OSV advisory GHSA-72x6-4j93-7w86 — OSV.dev. <https://osv.dev/vulnerability/GHSA-72x6-4j93-7w86> (modified 2026-09-10T03:51:13.226978985Z)
57. OSV advisory GHSA-78mq-xcr3-xm33 — OSV.dev. <https://osv.dev/vulnerability/GHSA-78mq-xcr3-xm33> (modified 2026-09-11T15:45:36.488635295Z)
58. OSV advisory GHSA-7jxh-36q5-gcqv — OSV.dev. <https://osv.dev/vulnerability/GHSA-7jxh-36q5-gcqv> (modified 2026-09-17T17:40:55.122822852Z)
59. OSV advisory GHSA-83g3-92jg-28cx — OSV.dev. <https://osv.dev/vulnerability/GHSA-83g3-92jg-28cx> (modified 2026-09-10T03:50:34.418493270Z)
60. OSV advisory GHSA-869c-j7wc-8jqv — OSV.dev. <https://osv.dev/vulnerability/GHSA-869c-j7wc-8jqv> (modified 2025-11-03T22:47:01Z)
61. OSV advisory GHSA-89gr-r52h-f8rx — OSV.dev. <https://osv.dev/vulnerability/GHSA-89gr-r52h-f8rx> (modified 2026-09-10T03:50:48.773810556Z)
62. OSV advisory GHSA-8pgv-569h-w5rw — OSV.dev. <https://osv.dev/vulnerability/GHSA-8pgv-569h-w5rw> (modified 2026-09-10T03:49:58.904350912Z)
63. OSV advisory GHSA-8qq5-rm4j-mr97 — OSV.dev. <https://osv.dev/vulnerability/GHSA-8qq5-rm4j-mr97> (modified 2026-09-10T03:50:59.009017334Z)
64. OSV advisory GHSA-8wmf-6v46-5gfg — OSV.dev. <https://osv.dev/vulnerability/GHSA-8wmf-6v46-5gfg> (modified 2026-10-01T20:55:52.479756803Z)
65. OSV advisory GHSA-8x88-c5mf-7j5w — OSV.dev. <https://osv.dev/vulnerability/GHSA-8x88-c5mf-7j5w> (modified 2026-09-10T03:51:11.200904859Z)
66. OSV advisory GHSA-96hv-2xvq-fx4p — OSV.dev. <https://osv.dev/vulnerability/GHSA-96hv-2xvq-fx4p> (modified 2026-09-10T03:50:49.163643932Z)
67. OSV advisory GHSA-9h8m-3fm2-qjrq — OSV.dev. <https://osv.dev/vulnerability/GHSA-9h8m-3fm2-qjrq> (modified 2026-09-10T03:50:34.801777790Z)
68. OSV advisory GHSA-9jj7-4m8r-rfcm — OSV.dev. <https://osv.dev/vulnerability/GHSA-9jj7-4m8r-rfcm> (modified 2026-09-10T03:50:43.842159740Z)
69. OSV advisory GHSA-9m57-25v3-79x9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-9m57-25v3-79x9> (modified 2026-09-10T03:50:55.369516615Z)
70. OSV advisory GHSA-9ppj-qmqm-q256 — OSV.dev. <https://osv.dev/vulnerability/GHSA-9ppj-qmqm-q256> (modified 2026-09-10T03:50:38.398085665Z)
71. OSV advisory GHSA-9vx6-7xxf-x967 — OSV.dev. <https://osv.dev/vulnerability/GHSA-9vx6-7xxf-x967> (modified 2025-12-05T12:36:38.324850Z)
72. OSV advisory GHSA-c8m5-c952-6cm4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4> (modified 2026-11-08T10:55:36.514447652Z)
73. OSV advisory GHSA-cf4h-3jhx-xvhq — OSV.dev. <https://osv.dev/vulnerability/GHSA-cf4h-3jhx-xvhq> (modified 2025-11-04T16:33:59Z)
74. OSV advisory GHSA-cm22-4g7w-348p — OSV.dev. <https://osv.dev/vulnerability/GHSA-cm22-4g7w-348p> (modified 2026-09-10T03:50:18.868190591Z)
75. OSV advisory GHSA-f5wc-c3c7-36mc — OSV.dev. <https://osv.dev/vulnerability/GHSA-f5wc-c3c7-36mc> (modified 2026-09-10T03:50:49.274413517Z)
76. OSV advisory GHSA-f5x3-32g6-xq36 — OSV.dev. <https://osv.dev/vulnerability/GHSA-f5x3-32g6-xq36> (modified 2026-09-10T03:50:10.480254172Z)
77. OSV advisory GHSA-f6x5-jh6r-wrfv — OSV.dev. <https://osv.dev/vulnerability/GHSA-f6x5-jh6r-wrfv> (modified 2026-09-10T03:50:30.884151926Z)
78. OSV advisory GHSA-fj2x-735w-74vq — OSV.dev. <https://osv.dev/vulnerability/GHSA-fj2x-735w-74vq> (modified 2026-09-10T03:50:29.734008925Z)
79. OSV advisory GHSA-g98v-hv3f-hcfr — OSV.dev. <https://osv.dev/vulnerability/GHSA-g98v-hv3f-hcfr> (modified 2026-09-10T03:49:53.897184297Z)
80. OSV advisory GHSA-gvwx-54wh-qm9j — OSV.dev. <https://osv.dev/vulnerability/GHSA-gvwx-54wh-qm9j> (modified 2026-09-10T03:50:52.205344551Z)
81. OSV advisory GHSA-h2v8-394m-p7vv — OSV.dev. <https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv> (modified 2026-11-08T10:55:59.261359726Z)
82. OSV advisory GHSA-h452-7996-h45h — OSV.dev. <https://osv.dev/vulnerability/GHSA-h452-7996-h45h> (modified 2025-02-13T19:03:25.062781Z)
83. OSV advisory GHSA-hcg3-q754-cr77 — OSV.dev. <https://osv.dev/vulnerability/GHSA-hcg3-q754-cr77> (modified 2026-09-10T03:50:23.913440018Z)
84. OSV advisory GHSA-hfvc-g4fc-pqhx — OSV.dev. <https://osv.dev/vulnerability/GHSA-hfvc-g4fc-pqhx> (modified 2026-09-10T03:51:01.896515018Z)
85. OSV advisory GHSA-hhf6-3xpg-pggx — OSV.dev. <https://osv.dev/vulnerability/GHSA-hhf6-3xpg-pggx> (modified 2025-09-25T17:12:19.059943Z)
86. OSV advisory GHSA-hrxh-6v49-42gf — OSV.dev. <https://osv.dev/vulnerability/GHSA-hrxh-6v49-42gf> (modified 2026-09-10T03:51:11.547405330Z)
87. OSV advisory GHSA-j5w8-q4qc-rx2x — OSV.dev. <https://osv.dev/vulnerability/GHSA-j5w8-q4qc-rx2x> (modified 2026-09-10T03:50:30.983878807Z)
88. OSV advisory GHSA-j88v-2chj-qfwx — OSV.dev. <https://osv.dev/vulnerability/GHSA-j88v-2chj-qfwx> (modified 2026-09-10T03:51:02.204456790Z)
89. OSV advisory GHSA-jpcc-p29g-p8mq — OSV.dev. <https://osv.dev/vulnerability/GHSA-jpcc-p29g-p8mq> (modified 2026-09-10T03:50:50.032144703Z)
90. OSV advisory GHSA-jppx-rxg9-jmrx — OSV.dev. <https://osv.dev/vulnerability/GHSA-jppx-rxg9-jmrx> (modified 2026-09-10T03:50:50.029914620Z)
91. OSV advisory GHSA-jqcg-44mw-7w3h — OSV.dev. <https://osv.dev/vulnerability/GHSA-jqcg-44mw-7w3h> (modified 2026-10-05T23:45:07.322157228Z)
92. OSV advisory GHSA-m4gq-fm9h-8q75 — OSV.dev. <https://osv.dev/vulnerability/GHSA-m4gq-fm9h-8q75> (modified 2026-09-10T03:50:56.838694902Z)
93. OSV advisory GHSA-m6fv-jmcg-4jfg — OSV.dev. <https://osv.dev/vulnerability/GHSA-m6fv-jmcg-4jfg> (modified 2026-09-10T03:50:18.939403414Z)
94. OSV advisory GHSA-m6hq-p25p-ffr2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-m6hq-p25p-ffr2> (modified 2026-09-10T03:50:58.362479211Z)
95. OSV advisory GHSA-mh63-6h87-95cp — OSV.dev. <https://osv.dev/vulnerability/GHSA-mh63-6h87-95cp> (modified 2026-09-10T03:50:56.801646453Z)
96. OSV advisory GHSA-mjcv-p78q-w5fw — OSV.dev. <https://osv.dev/vulnerability/GHSA-mjcv-p78q-w5fw> (modified 2026-10-19T21:40:47.349593935Z)
97. OSV advisory GHSA-p436-gjf2-799p — OSV.dev. <https://osv.dev/vulnerability/GHSA-p436-gjf2-799p> (modified 2026-09-10T03:50:39.956404854Z)
98. OSV advisory GHSA-p77j-4mvh-x3m3 — OSV.dev. <https://osv.dev/vulnerability/GHSA-p77j-4mvh-x3m3> (modified 2026-09-10T03:50:40.107473327Z)
99. OSV advisory GHSA-p9f8-wvj8-2fg8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-p9f8-wvj8-2fg8> (modified 2026-10-01T20:56:23.877100823Z)
100. OSV advisory GHSA-pc3f-x583-g7j2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-pc3f-x583-g7j2> (modified 2026-09-10T03:51:02.523109450Z)
101. OSV advisory GHSA-pfrx-2q88-qq97 — OSV.dev. <https://osv.dev/vulnerability/GHSA-pfrx-2q88-qq97> (modified 2026-09-10T03:49:55.225771209Z)
102. OSV advisory GHSA-pg57-6jwg-q645 — OSV.dev. <https://osv.dev/vulnerability/GHSA-pg57-6jwg-q645> (modified 2026-10-01T20:55:46.094271282Z)
103. OSV advisory GHSA-pmwq-pjrm-6p5r — OSV.dev. <https://osv.dev/vulnerability/GHSA-pmwq-pjrm-6p5r> (modified 2026-09-10T03:51:06.602952009Z)
104. OSV advisory GHSA-pwhc-rpq9-4c8w — OSV.dev. <https://osv.dev/vulnerability/GHSA-pwhc-rpq9-4c8w> (modified 2026-09-10T03:50:58.430975281Z)
105. OSV advisory GHSA-pxq6-2prw-chj9 — OSV.dev. <https://osv.dev/vulnerability/GHSA-pxq6-2prw-chj9> (modified 2026-09-10T03:50:40.571293679Z)
106. OSV advisory GHSA-q4h4-gmj2-qvw2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-q4h4-gmj2-qvw2> (modified 2026-09-10T03:50:50.202568323Z)
107. OSV advisory GHSA-qc2q-p7wx-3px3 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qc2q-p7wx-3px3> (modified 2026-09-15T19:10:32.558419529Z)
108. OSV advisory GHSA-qffp-2rhf-9h96 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qffp-2rhf-9h96> (modified 2026-09-10T03:50:40.605623006Z)
109. OSV advisory GHSA-qpw4-5x99-6vjp — OSV.dev. <https://osv.dev/vulnerability/GHSA-qpw4-5x99-6vjp> (modified 2026-09-10T03:50:50.295705701Z)
110. OSV advisory GHSA-qpx9-hpmf-5gmw — OSV.dev. <https://osv.dev/vulnerability/GHSA-qpx9-hpmf-5gmw> (modified 2026-09-10T03:51:00.752419958Z)
111. OSV advisory GHSA-qw6h-vgh9-j6wx — OSV.dev. <https://osv.dev/vulnerability/GHSA-qw6h-vgh9-j6wx> (modified 2026-09-10T03:50:18.298562940Z)
112. OSV advisory GHSA-qwcr-r2fm-qrc7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwcr-r2fm-qrc7> (modified 2026-09-10T03:50:18.292199548Z)
113. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-10-30T15:45:11.580215361Z)
114. OSV advisory GHSA-qxp5-gwg8-xv66 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qxp5-gwg8-xv66> (modified 2026-09-10T03:50:23.280114085Z)
115. OSV advisory GHSA-r292-9mhp-454m — OSV.dev. <https://osv.dev/vulnerability/GHSA-r292-9mhp-454m> (modified 2026-09-10T03:51:11.855710545Z)
116. OSV advisory GHSA-r6q2-hw4h-h46w — OSV.dev. <https://osv.dev/vulnerability/GHSA-r6q2-hw4h-h46w> (modified 2026-09-10T03:50:59.225342497Z)
117. OSV advisory GHSA-rc47-6667-2j5j — OSV.dev. <https://osv.dev/vulnerability/GHSA-rc47-6667-2j5j> (modified 2026-09-10T03:49:51.817106987Z)
118. OSV advisory GHSA-rg2x-37c3-w2rh — OSV.dev. <https://osv.dev/vulnerability/GHSA-rg2x-37c3-w2rh> (modified 2026-09-10T03:50:47.528575532Z)
119. OSV advisory GHSA-rhfx-m35p-ff5j — OSV.dev. <https://osv.dev/vulnerability/GHSA-rhfx-m35p-ff5j> (modified 2026-09-10T03:50:59.064354050Z)
120. OSV advisory GHSA-rhx6-c78j-4q9w — OSV.dev. <https://osv.dev/vulnerability/GHSA-rhx6-c78j-4q9w> (modified 2026-09-10T03:50:56.223604407Z)
121. OSV advisory GHSA-rm3j-f69w-wqmq — OSV.dev. <https://osv.dev/vulnerability/GHSA-rm3j-f69w-wqmq> (modified 2026-09-10T03:50:50.499928973Z)
122. OSV advisory GHSA-rp3h-jf77-q9p4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-rp3h-jf77-q9p4> (modified 2026-10-19T21:40:52.337183596Z)
123. OSV advisory GHSA-rv95-896h-c2vc — OSV.dev. <https://osv.dev/vulnerability/GHSA-rv95-896h-c2vc> (modified 2026-09-10T03:50:10.750068508Z)
124. OSV advisory GHSA-v23v-6jw2-98fq — OSV.dev. <https://osv.dev/vulnerability/GHSA-v23v-6jw2-98fq> (modified 2026-09-10T03:50:16.900418046Z)
125. OSV advisory GHSA-v422-hmwv-36x6 — OSV.dev. <https://osv.dev/vulnerability/GHSA-v422-hmwv-36x6> (modified 2026-09-10T03:50:53.014509971Z)
126. OSV advisory GHSA-vgwf-h737-ff37 — OSV.dev. <https://osv.dev/vulnerability/GHSA-vgwf-h737-ff37> (modified 2026-09-15T12:45:34.863978347Z)
127. OSV advisory GHSA-vmf3-w455-68vh — OSV.dev. <https://osv.dev/vulnerability/GHSA-vmf3-w455-68vh> (modified 2026-09-10T03:51:09.639522869Z)
128. OSV advisory GHSA-vp52-pcj8-j9qc — OSV.dev. <https://osv.dev/vulnerability/GHSA-vp52-pcj8-j9qc> (modified 2026-09-15T19:10:44.560975305Z)
129. OSV advisory GHSA-vp62-88p7-qqf5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-vp62-88p7-qqf5> (modified 2026-09-10T03:51:07.017544565Z)
130. OSV advisory GHSA-vvgc-356p-c3xw — OSV.dev. <https://osv.dev/vulnerability/GHSA-vvgc-356p-c3xw> (modified 2026-09-10T03:50:24.031676301Z)
131. OSV advisory GHSA-w44r-93j7-qv28 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28> (modified 2026-11-08T10:55:46.312019109Z)
132. OSV advisory GHSA-w5hq-g745-h8pq — OSV.dev. <https://osv.dev/vulnerability/GHSA-w5hq-g745-h8pq> (modified 2026-09-10T03:51:03.663336650Z)
133. OSV advisory GHSA-w67g-5rqw-f597 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w67g-5rqw-f597> (modified 2026-09-10T03:50:54.128553228Z)
134. OSV advisory GHSA-w7fw-mjwx-w883 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w7fw-mjwx-w883> (modified 2026-09-10T03:50:35.973235487Z)
135. OSV advisory GHSA-w879-237q-wc7r — OSV.dev. <https://osv.dev/vulnerability/GHSA-w879-237q-wc7r> (modified 2026-09-10T03:50:50.833802829Z)
136. OSV advisory GHSA-w8rr-5gcm-pp58 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w8rr-5gcm-pp58> (modified 2026-09-10T03:51:03.562742514Z)
137. OSV advisory GHSA-w8wr-v893-vjvp — OSV.dev. <https://osv.dev/vulnerability/GHSA-w8wr-v893-vjvp> (modified 2026-09-10T03:51:12.362978491Z)
138. OSV advisory GHSA-x527-x647-q7gg — OSV.dev. <https://osv.dev/vulnerability/GHSA-x527-x647-q7gg> (modified 2026-09-10T03:50:51.157351033Z)
139. OSV advisory GHSA-x86f-5xw2-fm2r — OSV.dev. <https://osv.dev/vulnerability/GHSA-x86f-5xw2-fm2r> (modified 2026-09-10T03:50:47.998689316Z)
140. OSV advisory GHSA-x9w5-v3q2-3rhw — OSV.dev. <https://osv.dev/vulnerability/GHSA-x9w5-v3q2-3rhw> (modified 2026-09-10T03:50:08.674168828Z)
141. OSV advisory GHSA-xgrm-4fwx-7qm8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-xgrm-4fwx-7qm8> (modified 2026-09-10T03:50:44.892822027Z)
142. OSV advisory GHSA-xhf5-7wjv-pqxp — OSV.dev. <https://osv.dev/vulnerability/GHSA-xhf5-7wjv-pqxp> (modified 2026-09-10T03:51:09.792384728Z)
143. OSV advisory GHSA-xmrv-pmrh-hhx2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-xmrv-pmrh-hhx2> (modified 2026-09-12T04:10:37.759930105Z)
144. OSV advisory GHSA-xwfj-jgwm-7wp5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-xwfj-jgwm-7wp5> (modified 2026-09-10T03:50:27.766863705Z)
145. OSV advisory GO-2024-3333 — OSV.dev. <https://osv.dev/vulnerability/GO-2024-3333> (modified 2026-03-24T23:55:17.997380Z)
146. OSV advisory GO-2025-4077 — OSV.dev. <https://osv.dev/vulnerability/GO-2025-4077> (modified 2026-03-03T04:57:05.845934Z)
147. OSV advisory GO-2025-4116 — OSV.dev. <https://osv.dev/vulnerability/GO-2025-4116> (modified 2026-11-23T21:12:30.039587020Z)
148. OSV advisory GO-2026-4440 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-4440> (modified 2026-05-15T10:59:23.883331519Z)
149. OSV advisory GO-2026-4441 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-4441> (modified 2026-05-15T10:59:23.510056268Z)
150. OSV advisory GO-2026-4887 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-4887> (modified 2026-11-23T20:30:07.958815145Z)
151. OSV advisory GO-2026-4918 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-4918> (modified 2026-11-23T21:12:28.465241903Z)
152. OSV advisory GO-2026-5024 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5024> (modified 2026-06-09T18:59:22.740765220Z)
153. OSV advisory GO-2026-5025 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5025> (modified 2026-05-30T05:14:17.563517047Z)
154. OSV advisory GO-2026-5026 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5026> (modified 2026-11-23T21:12:28.671130412Z)
155. OSV advisory GO-2026-5027 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5027> (modified 2026-11-23T21:12:29.472586555Z)
156. OSV advisory GO-2026-5029 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5029> (modified 2026-11-23T21:12:28.895525167Z)
157. OSV advisory GO-2026-5030 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5030> (modified 2026-11-23T21:12:28.405165939Z)
158. OSV advisory GO-2026-5932 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5932> (modified 2026-11-02T22:15:06.677088389Z)
159. OSV advisory GO-2026-5942 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5942> (modified 2026-08-17T12:25:32.471119200Z)
160. OSV advisory GO-2026-5970 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5970> (modified 2026-11-23T21:12:29.269820156Z)
161. OSV advisory GO-2026-6179 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6179> (modified 2026-08-19T12:25:40.780492871Z)
162. OSV advisory GO-2026-6180 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6180> (modified 2026-08-19T12:25:49.995487491Z)
163. OSV advisory GO-2026-6303 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6303> (modified 2026-08-29T10:10:52.440319762Z)
164. OSV advisory GO-2026-6354 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6354> (modified 2026-09-03T10:10:55.147673102Z)
165. OSV advisory GO-2026-6603 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6603> (modified 2026-11-23T21:12:29.903950358Z)
166. OSV advisory GO-2026-6610 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6610> (modified 2026-11-23T21:12:29.831892156Z)
167. OSV advisory GO-2026-6611 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6611> (modified 2026-11-23T21:12:29.007257358Z)
168. OSV advisory GO-2026-6612 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6612> (modified 2026-11-23T21:12:28.295006823Z)
169. OSV advisory GO-2026-6617 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6617> (modified 2026-11-23T21:12:28.960393562Z)
170. OSV advisory GO-2026-6629 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6629> (modified 2026-11-23T21:12:29.495073874Z)
171. OSV advisory GO-2026-6860 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6860> (modified 2026-10-27T21:30:04.890809062Z)
172. OSV advisory GO-2026-6865 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6865> (modified 2026-11-05T23:15:14.472777299Z)
173. OSV advisory GO-2026-6866 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6866> (modified 2026-10-27T21:45:08.978077289Z)
174. OSV advisory GO-2026-6975 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-6975> (modified 2026-11-23T20:30:17.039860504Z)
175. OSV advisory RUSTSEC-2021-0139 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2021-0139> (modified 2023-09-06T22:52:31Z)
176. OSV advisory RUSTSEC-2024-0014 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0014> (modified 2024-02-18T04:06:15Z)
177. OSV advisory RUSTSEC-2024-0375 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0375> (modified 2024-09-26T12:26:22Z)
178. OSV advisory RUSTSEC-2024-0384 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0384> (modified 2024-11-10T13:10:28Z)
179. OSV advisory RUSTSEC-2024-0388 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0388> (modified 2024-11-10T13:34:40Z)
180. OSV advisory RUSTSEC-2024-0436 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0436> (modified 2026-01-27T22:03:15.694766Z)
181. OSV advisory RUSTSEC-2025-0057 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0057> (modified 2025-09-05T19:09:01Z)
182. OSV advisory RUSTSEC-2025-0141 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0141> (modified 2026-01-16T11:07:28.867553Z)
183. OSV advisory RUSTSEC-2025-0161 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0161> (modified 2026-04-14T11:30:08.962845Z)
184. OSV advisory RUSTSEC-2026-0173 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0173> (modified 2026-06-07T21:00:04.318567692Z)
185. OSV advisory RUSTSEC-2026-0220 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0220> (modified 2026-07-30T19:15:04.025918010Z)
186. OSV advisory RUSTSEC-2026-0253 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0253> (modified 2026-08-11T11:15:06.101553049Z)
187. OSV advisory RUSTSEC-2026-0258 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0258> (modified 2026-10-12T18:00:10.934581734Z)
188. OSV advisory RUSTSEC-2026-0338 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0338> (modified 2026-10-12T18:15:01.969514645Z)
189. OSV advisory RUSTSEC-2026-0339 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0339> (modified 2026-10-12T18:15:01.956822776Z)
190. OSV advisory RUSTSEC-2026-0340 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0340> (modified 2026-10-12T18:15:01.975478256Z)
191. OSV advisory RUSTSEC-2026-0341 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0341> (modified 2026-10-12T18:15:01.969505433Z)
192. OSV advisory RUSTSEC-2026-0342 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0342> (modified 2026-10-12T18:15:01.956681478Z)
193. OSV advisory RUSTSEC-2026-0381 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0381> (modified 2026-10-29T10:55:54.096394276Z)
194. OSV advisory RUSTSEC-2026-0382 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0382> (modified 2026-10-29T10:55:54.096394276Z)
195. OSV advisory RUSTSEC-2026-0386 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0386> (modified 2026-10-23T14:45:03.847864944Z)
196. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
197. OSV advisory RUSTSEC-2026-0391 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0391> (modified 2026-11-02T09:30:03.590733846Z)
198. OSV advisory RUSTSEC-2026-0395 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0395> (modified 2026-11-02T09:30:03.420559993Z)
199. OSV advisory RUSTSEC-2026-0396 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0396> (modified 2026-11-02T09:30:03.400899521Z)
200. OSV advisory RUSTSEC-2026-0397 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0397> (modified 2026-11-02T09:30:03.445177143Z)
201. OSV advisory RUSTSEC-2026-0398 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0398> (modified 2026-11-02T09:30:03.419709171Z)
202. OSV advisory RUSTSEC-2026-0399 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0399> (modified 2026-11-02T09:30:03.328955732Z)
203. OSV advisory RUSTSEC-2026-0400 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0400> (modified 2026-11-02T09:30:03.428341570Z)
204. OSV advisory RUSTSEC-2026-0401 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0401> (modified 2026-11-02T09:30:03.353698025Z)
205. OSV advisory RUSTSEC-2026-0402 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0402> (modified 2026-11-02T09:30:04.162155944Z)
206. OSV advisory RUSTSEC-2026-0403 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0403> (modified 2026-11-02T09:30:04.136442771Z)
207. OSV advisory RUSTSEC-2026-0404 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0404> (modified 2026-11-02T09:30:04.168804805Z)
208. OSV advisory RUSTSEC-2026-0405 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0405> (modified 2026-11-02T09:30:03.399517581Z)
209. OSV advisory RUSTSEC-2026-0406 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0406> (modified 2026-11-02T09:30:03.591194710Z)
210. OSV advisory RUSTSEC-2026-0410 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0410> (modified 2026-10-26T14:00:05.788985783Z)
211. OSV advisory RUSTSEC-2026-0418 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0418> (modified 2026-10-29T14:15:02.333141406Z)
212. OSV advisory RUSTSEC-2026-0441 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0441> (modified 2026-11-05T09:00:02.627533155Z)
213. OSV advisory RUSTSEC-2026-0486 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0486> (modified 2026-11-11T08:45:02.466292839Z)
214. OSV advisory RUSTSEC-2026-0523 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0523> (modified 2026-11-13T12:45:04.789912316Z)
215. OSV advisory RUSTSEC-2026-0524 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0524> (modified 2026-11-13T12:45:06.127108520Z)
216. OSV advisory RUSTSEC-2026-0538 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0538> (modified 2026-11-13T12:45:08.844283231Z)
217. OSV advisory RUSTSEC-2026-0542 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0542> (modified 2026-11-17T10:15:02.347148964Z)
218. OSV advisory RUSTSEC-2026-0543 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0543> (modified 2026-11-17T10:15:02.344223779Z)
219. OSV advisory RUSTSEC-2026-0544 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0544> (modified 2026-11-17T10:15:02.362721160Z)
220. OSV advisory RUSTSEC-2026-0592 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0592> (modified 2026-11-22T10:00:02.260974192Z)
221. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
222. OWASP Application Security Verification Standard — OWASP. <https://owasp.org/www-project-application-security-verification-standard/> (living standard — check the project page for the current version)
223. OpenZeppelin Contracts — SafeERC20 (wrappers around ERC-20 operations that throw on failure) — OpenZeppelin. <https://docs.openzeppelin.com/contracts/5.x/api/token/erc20#SafeERC20> (library documentation: handles tokens that return no value (USDT) or false, and forceApprove for tokens that require the allowance to be reset to zero first)
224. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
225. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
226. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)
227. Smart Contract Weakness Classification (SWC) Registry — SWC community (no longer actively maintained). <https://swcregistry.io/> (historic reference; still widely cited)

## Приложения: Криптографическая инвентаризация

По происхождению: манифесты зависимостей 34 (0 уязвимы для алгоритма Шора) · собственный код 55 (9 уязвимы для алгоритма Шора) · сторонний код в дереве 4 (1 уязвимы для алгоритма Шора).

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| Keccak-256 | Keccak-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 36 | 36 | bridge-history-api/internal/logic/l1_event_parser.go:417; bridge-history-api/internal/logic/l2_fetcher.go:178; bridge-history-api/internal/utils/utils.go:27 |
| Poseidon |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 4 | 4 | crates/prover-bin/src/deferral.rs:58; scroll-contracts/circomlib.d.ts:2; scroll-contracts/scripts/hardhat/ScrollChainCommitmentVerifier.deploy.ts:5 |
| SHA-2 | SHA-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 1 | 1 | common/utils/blob.go:4 |
| STARK (FRI) |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 7 | 7 | common/types/message/message.go:189; coordinator/internal/logic/submitproof/proof_receiver.go:234; coordinator/internal/logic/verifier/mock.go:24 |
| X25519MLKEM768 | X25519MLKEM768 |  | гибрид | допустимо | 1 | 1 | bridge-history-api/cmd/api/app/app.go:67 |
| Crypto library | 0.1.0 | halo2_proofs (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.1.0-beta.2 | halo2 (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.10.81 | openssl (OpenSSL) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.4 | k256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.17.14 | ring (ring (Rust)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.23.41 | rustls (rustls) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.30.0 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.31.1 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.4.1 | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.5.1 | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.7.1 | bls12_381 (bls12_381) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.9.0 | jubjub (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | v0.32.0 | golang.org/x/crypto (Go x/crypto) | н/п | допустимо | 4 | 4 | bridge-history-api/go.mod:111; common/go.mod:239; coordinator/go.mod:104 |
| Crypto library | v1.1.1 | github.com/miekg/pkcs11 (PKCS#11 bindings (HSM access)) | н/п | допустимо | 1 | 1 | common/go.mod:150 |
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
| ECDSA |  |  | уязвим (Шор) | допустимо | 6 | 6 | common/utils/keystore.go:4; coordinator/internal/controller/proxy/client_manager.go:5; coordinator/internal/types/auth.go:4 |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 2 | 2 | rollup/internal/controller/sender/kms_signer.go:64; scroll-contracts/src/lido/L2WstETHToken.sol:43 |
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
