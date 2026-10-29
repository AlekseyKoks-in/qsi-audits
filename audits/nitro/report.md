# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** nitro @ ccc5c828d9ea · Offchain Labs (Arbitrum) — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-28 18:10 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 2f44e0e2-8dfe-4ec4-afed-af68a2bd8ac3 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Web3-проект |
| SHA-256 содержимого | `bef977ec125421b714625439bc8fe3108a1e36383f7644d7a141aacbdc8ff184` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **1**
- Высокая: **8**
- Средняя: **18**
- Низкая: **24**
- Информационная: **19**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 51
- Подтверждённая ошибка конфигурации: 1
- Потенциальный криптографический риск: 1
- Долгосрочный постквантовый риск: 4
- Рекомендация по улучшению: 12
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 5, y = 5, z = 12 → запас минимален. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/OffchainLabs/nitro> @ `ccc5c828d9ea22f161efc784bac4d4a6559b7e59` — ссылки в доказательствах открывают строки на этом коммите.

1038 файлов, всего 9196286 байт, редактирований: 2; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 967 | .github/workflows/process_junit.py: 65 lines scanned with 16 rule patterns and 122 registry patterns; arbcompress/compress_common.go: 24 lines scanned with 16 rule patterns and 122 registry patterns; arbcompress/native.go: 84 lines scanned with 16 rule patterns and 122 registry patterns |
| dependencies | проверено | 66 | Cargo.lock: 591 dependencies parsed (591 pinned); Cargo.toml: 54 dependencies parsed (1 pinned); crates/arbutil/Cargo.toml: 10 dependencies parsed (0 pinned) |
| tls_code | проверено | 4 | arbnode/dataposter/externalsigner/client.go: TLS key-exchange settings read; arbnode/dataposter/externalsignertest/externalsignertest.go: TLS key-exchange settings read; broadcastclient/broadcastclient.go: TLS key-exchange settings read |
| smart_contracts | проверено | 1 | contracts-local/src/osp/ReferenceDAProofValidator.sol: built-in Solidity pattern checks |
| slither | не проверено | 1 | slither is not installed on the server (pip install slither-analyzer + solc) |
| secrets | проверено | 3 | util/signature/simple_hmac.go: value(s) at line(s) 77 (TestSimpleHmacConfig) are declared inside a fixture and treated as test data, although the file itself is not test code; util/signature/simple_hmac.go: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); wavmio/common.go: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| osv_advisories | проверено | 1 | 1000 pinned packages queried at OSV.dev; 46 affected (2 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- slither — не проверено: slither is not installed on the server (pip install slither-analyzer + solc)

## 5. Краткое описание архитектуры

Static review of the source tree nitro at ccc5c828d9ea22f161efc784bac4d4a6559b7e59. 1038 files analysed; of 2840 files, 1399 are test, fuzzing, benchmark or example code and were left out, 400 are not read by any analyzer, 1 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **0** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 12.0%

## 7. Подробное описание находок

### QSI-2026-05596 — wee_alloc 0.4.5: информационный бюллетень GHSA-rc23-xxgq-x27g (RUSTSEC-2022-0054) (unmaintained)

- Серьёзность: **Критическая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `dependency:crates.io/wee_alloc@0.4.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 47.2 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает GHSA-rc23-xxgq-x27g (RUSTSEC-2022-0054) для пакета crates.io wee_alloc версии 0.4.5 как информационный (unmaintained): wee_alloc is Unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rc23-xxgq-x27g
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rc23-xxgq-x27g](https://osv.dev/vulnerability/GHSA-rc23-xxgq-x27g) · manifest · SHA-256 c3d07b81aaa2dcd84986660e0f634f038a795d46704859c38b3823b24a456ab9_

```
{"id": "GHSA-rc23-xxgq-x27g", "aliases": ["RUSTSEC-2022-0054"], "modified": "2023-11-08T04:22:41.320727Z", "summary": "wee_alloc is Unmaintained", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-05550 — Проверка TLS-сертификата отключена в arbnode/dataposter/config/config.go

- Серьёзность: **Высокая** · Классификация: Подтверждённая ошибка конфигурации · Уверенность: Высокая
- Затронутый актив: `file:arbnode/dataposter/config/config.go`
- Источник данных: arbnode/dataposter/config/config.go
- Метод обнаружения: Сопоставление регулярных выражений с API конкретного языка.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 68.3 / 100
- CVSS v3.1: 6.8 (`CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N`)

1 случаев отключения проверки (InsecureSkipVerify: true), первый — строка 237.

**Возможные последствия.** Соединения уязвимы к перехвату «человек посередине».

**Шаги воспроизведения.**

```
Откройте строка 237 в предоставленном файле arbnode/dataposter/config/config.go и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [arbnode/dataposter/config/config.go](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/arbnode/dataposter/config/config.go#L237) · line 237 · SHA-256 bd1419d0ecd1802678113c2ff2ea8b2e266d84fedcd58b8f50345d5bd744f74d_

```
  235 | 	UseNoOpStorage:         false,
  236 | 	LegacyStorageEncoding:  false,
  237 | 	ExternalSigner:         ExternalSignerConfig{Method: "eth_signTransaction", InsecureSkipVerify: true},
  238 | 	MaxFeeCapFormula:       "((BacklogOfBatches * UrgencyGWei) ** 2) + ((ElapsedTime/ElapsedTimeBase) ** 2) * ElapsedTimeImportance + TargetPriceGWei",
  239 | 	ElapsedTimeBase:        10 * time.Minute,
```

**Ограничения проверки.** Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Удалите отключение; используйте корректный набор УЦ или пиннинг.

**Повторная проверка.** Повторно просканируйте код и проверьте места вызова из доказательства.

### QSI-2026-05614 — github.com/ethereum/go-ethereum v1.16.2 затронут GHSA-mq3p-rrmp-79jg (CVE-2026-22868, GO-2026-4314)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/ethereum/go-ethereum@v1.16.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-mq3p-rrmp-79jg (CVE-2026-22868, GO-2026-4314) для пакета Go github.com/ethereum/go-ethereum версии v1.16.2: go-ethereum is vulnerable to high CPU usage leading to DoS via malicious p2p message. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mq3p-rrmp-79jg
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mq3p-rrmp-79jg](https://osv.dev/vulnerability/GHSA-mq3p-rrmp-79jg) · line 28 · SHA-256 fd9d39f1d092ebd0dd52c83ddc9bb186ee3ba5955756c2c9b302c5d189e45e4e_

```
{"id": "GHSA-mq3p-rrmp-79jg", "aliases": ["CVE-2026-22868", "GO-2026-4314"], "modified": "2026-02-03T02:58:49.032697Z", "summary": "go-ethereum is vulnerable to high CPU usage leading to DoS via malicious p2p message", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05615 — github.com/ethereum/go-ethereum v1.16.2 затронут GHSA-mr7q-c9w9-wh4h (CVE-2026-22862, GO-2026-4315)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/ethereum/go-ethereum@v1.16.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 49.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-mr7q-c9w9-wh4h (CVE-2026-22862, GO-2026-4315) для пакета Go github.com/ethereum/go-ethereum версии v1.16.2: go-ethereum is vulnerable to DoS via malicious p2p message affecting a vulnerable node. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-mr7q-c9w9-wh4h
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-mr7q-c9w9-wh4h](https://osv.dev/vulnerability/GHSA-mr7q-c9w9-wh4h) · line 28 · SHA-256 0bc1d4ae8d0fafd3c47a394c6c22d5f18e6f783b3faa1578873e747ed372b1a5_

```
{"id": "GHSA-mr7q-c9w9-wh4h", "aliases": ["CVE-2026-22862", "GO-2026-4315"], "modified": "2026-02-03T02:59:06.834692Z", "summary": "go-ethereum is vulnerable to DoS via malicious p2p message affecting a vulnerable node", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:L/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05574 — quinn-proto 0.11.14 затронут GHSA-4w2j-m93h-cj5j (CVE-2026-25800, RUSTSEC-2026-0185)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.14`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 36.9 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-4w2j-m93h-cj5j (CVE-2026-25800, RUSTSEC-2026-0185) для пакета crates.io quinn-proto версии 0.11.14: Quinn: Remote memory exhaustion in quinn-proto from unbounded out-of-order stream reassembly. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4w2j-m93h-cj5j
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4w2j-m93h-cj5j](https://osv.dev/vulnerability/GHSA-4w2j-m93h-cj5j) · manifest · SHA-256 fa6c8edbbf8c387448ccf15110b434332c2275859f1876d9ce7202c841abc9cb_

```
{"id": "GHSA-4w2j-m93h-cj5j", "aliases": ["CVE-2026-25800", "RUSTSEC-2026-0185"], "modified": "2026-09-10T03:51:10.288925502Z", "summary": "Quinn: Remote memory exhaustion in quinn-proto from unbounded out-of-order stream reassembly", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.11.15).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05577 — quinn-proto 0.11.14 затронут RUSTSEC-2026-0340

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.14`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 36.9 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает RUSTSEC-2026-0340 для пакета crates.io quinn-proto версии 0.11.14: Peer minimum ACK delay can panic quinn-proto when ACK_FREQUENCY transmission is enabled. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-05590 — ruzstd 0.8.2 затронут RUSTSEC-2026-0344

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/ruzstd@0.8.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 36.9 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает RUSTSEC-2026-0344 для пакета crates.io ruzstd версии 0.8.2: Decompression bomb in `ruzstd`: a tiny input can exhaust memory (OOM). Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0344
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0344](https://osv.dev/vulnerability/RUSTSEC-2026-0344) · manifest · SHA-256 89775c541792252f5a8282788debf79a598a367aca82a30e2f0e5c528e75b878_

```
{"id": "RUSTSEC-2026-0344", "aliases": [], "modified": "2026-10-13T10:45:04.080993335Z", "summary": "Decompression bomb in `ruzstd`: a tiny input can exhaust memory (OOM)", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.9.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05593 — tar 0.4.44 затронут GHSA-gchp-q4r4-x4ff (CVE-2026-33055, RUSTSEC-2026-0068)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/tar@0.4.44`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 36.9 / 100
- CVSS v3.1: 8.1 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N`)

OSV.dev сообщает GHSA-gchp-q4r4-x4ff (CVE-2026-33055, RUSTSEC-2026-0068) для пакета crates.io tar версии 0.4.44: tar-rs incorrectly ignores PAX size headers if header size is nonzero. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-gchp-q4r4-x4ff
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-gchp-q4r4-x4ff](https://osv.dev/vulnerability/GHSA-gchp-q4r4-x4ff) · manifest · SHA-256 a618d65c9bd92ed77229a7c0d02d406983a6fc58437fe17ca5a620a2bcfad2d0_

```
{"id": "GHSA-gchp-q4r4-x4ff", "aliases": ["CVE-2026-33055", "RUSTSEC-2026-0068"], "modified": "2026-09-10T03:50:39.204912381Z", "summary": "tar-rs incorrectly ignores PAX size headers if header size is nonzero", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:L/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.4.45).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05601 — p3-challenger 0.3.3-succinct затронут GHSA-vj64-rjf3-w3v7 (CVE-2026-46654)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/p3-challenger@0.3.3-succinct`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 36.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-vj64-rjf3-w3v7 (CVE-2026-46654) для пакета crates.io p3-challenger версии 0.3.3-succinct: Plonky3 MultiField32Challenger: transcript malleability and challenge entropy loss. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vj64-rjf3-w3v7
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vj64-rjf3-w3v7](https://osv.dev/vulnerability/GHSA-vj64-rjf3-w3v7) · manifest · SHA-256 b4ef9c398c5930334db16a5981c791a931962c756c9645b86081682d441c29d5_

```
{"id": "GHSA-vj64-rjf3-w3v7", "aliases": ["CVE-2026-46654"], "modified": "2026-06-11T14:15:08.995914138Z", "summary": "Plonky3 MultiField32Challenger: transcript malleability and challenge entropy loss", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:N/PR:N/UI:N/VC:N/VI:H/VA:N/SC:N/SI:H/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.4.3, 0.5.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05556 — Прямое использование ecrecover в contracts-local/src/osp/ReferenceDAProofValidator.sol

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:contracts-local/src/osp/ReferenceDAProofValidator.sol`
- Источник данных: contracts-local/src/osp/ReferenceDAProofValidator.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 43.2 / 100
- CVSS v3.1: неприменимо

ecrecover в строка 173. (см. SWC-117/SWC-121)

**Возможные последствия.** Без проверок s-значения/нулевого адреса и nonce подписи могут быть изменяемыми или повторно используемыми. ecrecover основан на secp256k1 ECDSA (долгосрочно квантово-уязвим).

**Шаги воспроизведения.**

```
Откройте строка 173 в предоставленном файле contracts-local/src/osp/ReferenceDAProofValidator.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts-local/src/osp/ReferenceDAProofValidator.sol](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/contracts-local/src/osp/ReferenceDAProofValidator.sol#L173) · line 173 · SHA-256 80da80e1745a6bc9859852783e7849c88e0f42c2ef67cede0bdf6856499c5d06_

```
  171 | 
  172 |         // Recover signer from signature
  173 |         address signer = ecrecover(dataHash, v, r, s);
  174 | 
  175 |         // Check if signature is valid (ecrecover returns 0 on invalid signature)
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin ECDSA.recover с разделением доменов EIP-712 и nonce.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-05580 — rkyv 0.8.15 затронут GHSA-vfvv-c25p-m7mm (RUSTSEC-2026-0122)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rkyv@0.8.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-vfvv-c25p-m7mm (RUSTSEC-2026-0122) для пакета crates.io rkyv версии 0.8.15: rkyv: Panic safety bugs in `InlineVec::clear` and `SerVec::clear` enable arbitrary code execution. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-vfvv-c25p-m7mm
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-vfvv-c25p-m7mm](https://osv.dev/vulnerability/GHSA-vfvv-c25p-m7mm) · manifest · SHA-256 de3af97c6950fb418c59cbe6d58a7a4762649e87b102f4b066385074cbe04c17_

```
{"id": "GHSA-vfvv-c25p-m7mm", "aliases": ["RUSTSEC-2026-0122"], "modified": "2026-09-10T03:50:47.714144241Z", "summary": "rkyv: Panic safety bugs in `InlineVec::clear` and `SerVec::clear` enable arbitrary code execution", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.8.16).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05591 — serde_with 3.9.0 затронут GHSA-7gcf-g7xr-8hxj

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/serde_with@3.9.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7gcf-g7xr-8hxj для пакета crates.io serde_with версии 3.9.0: serde_with: KeyValueMap serialization panics on empty sequence or map entries. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7gcf-g7xr-8hxj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7gcf-g7xr-8hxj](https://osv.dev/vulnerability/GHSA-7gcf-g7xr-8hxj) · manifest · SHA-256 b42c751004bfb387a1f24d4e9b23157ae70dc8f33fdb503f87f6d04255008aa3_

```
{"id": "GHSA-7gcf-g7xr-8hxj", "aliases": [], "modified": "2026-09-10T03:51:10.897685062Z", "summary": "serde_with: KeyValueMap serialization panics on empty sequence or map entries", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.21.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05608 — serde_with 3.16.1 затронут GHSA-7gcf-g7xr-8hxj

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/serde_with@3.16.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7gcf-g7xr-8hxj для пакета crates.io serde_with версии 3.16.1: serde_with: KeyValueMap serialization panics on empty sequence or map entries. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-7gcf-g7xr-8hxj
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-7gcf-g7xr-8hxj](https://osv.dev/vulnerability/GHSA-7gcf-g7xr-8hxj) · manifest · SHA-256 b42c751004bfb387a1f24d4e9b23157ae70dc8f33fdb503f87f6d04255008aa3_

```
{"id": "GHSA-7gcf-g7xr-8hxj", "aliases": [], "modified": "2026-09-10T03:51:10.897685062Z", "summary": "serde_with: KeyValueMap serialization panics on empty sequence or map entries", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.21.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05610 — github.com/codeclysm/extract/v3 v3.0.2 затронут GHSA-8rm2-93mq-jqhc (CVE-2024-47877, GO-2024-3196)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/codeclysm/extract/v3@v3.0.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-8rm2-93mq-jqhc (CVE-2024-47877, GO-2024-3196) для пакета Go github.com/codeclysm/extract/v3 версии v3.0.2: Extract has insufficient checks allowing attacker to create symlinks outside the extraction directory. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-8rm2-93mq-jqhc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-8rm2-93mq-jqhc](https://osv.dev/vulnerability/GHSA-8rm2-93mq-jqhc) · line 25 · SHA-256 0e0cf935b92bb84476967cfa384be7cbfc1c15de4137d5fa4965b27a5f2c7859_

```
{"id": "GHSA-8rm2-93mq-jqhc", "aliases": ["CVE-2024-47877", "GO-2024-3196"], "modified": "2024-10-15T19:53:17Z", "summary": "Extract has insufficient checks allowing attacker to create symlinks outside the extraction directory.", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05612 — github.com/ethereum/go-ethereum v1.16.2 затронут GHSA-689v-6xwf-5jf3 (CVE-2026-26313, GO-2026-4508)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:Go/github.com/ethereum/go-ethereum@v1.16.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-689v-6xwf-5jf3 (CVE-2026-26313, GO-2026-4508) для пакета Go github.com/ethereum/go-ethereum версии v1.16.2: Go Ethereum affected by DoS via malicious p2p message. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-689v-6xwf-5jf3
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-689v-6xwf-5jf3](https://osv.dev/vulnerability/GHSA-689v-6xwf-5jf3) · line 28 · SHA-256 83352d861902e9c470b720eed886b8c4872d7ae08ca9e28535d6213c3c7f91e0_

```
{"id": "GHSA-689v-6xwf-5jf3", "aliases": ["CVE-2026-26313", "GO-2026-4508"], "modified": "2026-02-28T06:26:25.973770Z", "summary": "Go Ethereum affected by DoS via malicious p2p message", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.17.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05552 — Квантово-уязвимый Ed25519: подпись транзакций и сообщений (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Ed25519:transaction_signing`
- Источник данных: cmd/filtering-report/signer/signer.go
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 33.0 / 100
- CVSS v3.1: неприменимо

2 упоминаний Ed25519 в 2 файл(ах), например cmd/filtering-report/signer/signer.go:133. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте cmd/filtering-report/signer/signer.go:133 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [cmd/filtering-report/signer/signer.go](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/cmd/filtering-report/signer/signer.go#L133) · line 133 · SHA-256 46de9ee17d4a2241e171c2e5a1d3d27472c0c0bc02bf91c7bfccb82fec9bdc0b_

```
  132 | 	payload := BuildSigningPayload(timestamp, body)
  133 | 	signature := ed25519.Sign(creds.privateKey, payload)
  134 | 
```

_file_excerpt · [cmd/filtering-report/signer/signertest/verifier.go](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/cmd/filtering-report/signer/signertest/verifier.go#L129) · line 129 · SHA-256 ba0a3417761e9385115b7942c3ca1caf7e9eb04449df0e64a82a9bb43770823e_

```
  128 | 	payload := signer.BuildSigningPayload(tsHeader, rawBody)
  129 | 	if !ed25519.Verify(publicKey, payload, signature) {
  130 | 		return errors.New("signature verification failed")
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05555 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (3 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: contracts-local/src/osp/ReferenceDAProofValidator.sol
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 33.0 / 100
- CVSS v3.1: неприменимо

4 упоминаний ECDSA в 3 файл(ах), например contracts-local/src/osp/ReferenceDAProofValidator.sol:173. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте contracts-local/src/osp/ReferenceDAProofValidator.sol:173 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts-local/src/osp/ReferenceDAProofValidator.sol](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/contracts-local/src/osp/ReferenceDAProofValidator.sol#L173) · line 173 · SHA-256 80da80e1745a6bc9859852783e7849c88e0f42c2ef67cede0bdf6856499c5d06_

```
  171 | 
  172 |         // Recover signer from signature
  173 |         address signer = ecrecover(dataHash, v, r, s);
  174 | 
  175 |         // Check if signature is valid (ecrecover returns 0 on invalid signature)
```

_file_excerpt · [nitro-reth/crates/arb-primitives/src/signed_tx.rs](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/nitro-reth/crates/arb-primitives/src/signed_tx.rs#L20) · line 20 · SHA-256 29c28398a7cba71e392275ed36f3c0ea058fd72d86761ce552ba63ab5e4b5058_

```
   19 |     InMemorySize,
   20 |     crypto::secp256k1::{recover_signer, recover_signer_unchecked},
   21 | };
```

_file_excerpt · [nitro-reth/crates/arb-test-harness/src/messaging/signed_tx.rs](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/nitro-reth/crates/arb-test-harness/src/messaging/signed_tx.rs#L3) · line 3 · SHA-256 4714618c877285ef540d7ecdef22e309fd824bc1bc433ecbaa7eb2107342f73a_

```
    2 |     EthereumTxEnvelope, SignableTransaction, TxEip1559, TxEip2930, TxEip7702, TxLegacy,
    3 |     crypto::secp256k1::sign_message,
    4 | };
```

_file_excerpt · [nitro-reth/crates/arb-test-harness/src/messaging/signed_tx.rs](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/nitro-reth/crates/arb-test-harness/src/messaging/signed_tx.rs#L239) · line 239 · SHA-256 1b9b13e531df8c5b0c01bf581b099a6d5eca65bfc459da1ee07ae083f274bd3f_

```
  238 | pub fn derive_address(sk: B256) -> Address {
  239 |     let signing_key = k256::ecdsa::SigningKey::from_slice(sk.as_slice()).expect("32-byte secret");
  240 |     let verifying = *signing_key.verifying_key();
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05551 — Квантово-уязвимый ECDSA: роль не определена (6 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: cmd/anytrusttool/main.go
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 31.7 / 100
- CVSS v3.1: неприменимо

7 упоминаний ECDSA в 6 файл(ах), например cmd/anytrusttool/main.go:9. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте cmd/anytrusttool/main.go:9 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [cmd/anytrusttool/main.go](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/cmd/anytrusttool/main.go#L9) · line 9 · SHA-256 cfbd1e66b6bf34a9aa148b95a8ecfaaaf8550a213d2657576f3873a0b87eb009_

```
    8 | 	"context"
    9 | 	"crypto/ecdsa"
   10 | 	"crypto/rand"
```

_file_excerpt · [cmd/nitro/nitro.go](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/cmd/nitro/nitro.go#L8) · line 8 · SHA-256 dc42e6ffb7bc0259716b8b13d6e8748144a6eb985c178e84f87c68e5e72105b6_

```
    7 | 	"context"
    8 | 	"crypto/ecdsa"
    9 | 	"encoding/hex"
```

_file_excerpt · [crates/caller-env/src/arbcrypto.rs](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/crates/caller-env/src/arbcrypto.rs#L5) · line 5 · SHA-256 c262e6fccffb3e764a87157812722e5b3acd9351cbe883658049ab6e30899fc5_

```
    4 | 
    5 | use k256::ecdsa::{RecoveryId, Signature, VerifyingKey};
    6 | use tiny_keccak::{Hasher, Keccak};
```

_file_excerpt · [nitro-reth/crates/arb-precompiles/src/lib.rs](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/nitro-reth/crates/arb-precompiles/src/lib.rs#L94) · line 94 · SHA-256 137322a6f950fd4125cbc61b66cb36aaad48cd2e69fa622e226079c0014c8a41_

```
   93 |     DynPrecompile::new(PrecompileId::P256Verify, |input: PrecompileInput<'_>| {
   94 |         revm::precompile::secp256r1::p256_verify(input.data, input.gas)
   95 |     })
```

_file_excerpt · [nitro-reth/crates/arb-precompiles/src/lib.rs](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/nitro-reth/crates/arb-precompiles/src/lib.rs#L100) · line 100 · SHA-256 7f0c503bcd28b2b64a69d6b0cb9033d41d1ce5c14ec5eb7e9d2ed0e084b2ac4e_

```
   99 |     DynPrecompile::new(PrecompileId::P256Verify, |input: PrecompileInput<'_>| {
  100 |         revm::precompile::secp256r1::p256_verify_osaka(input.data, input.gas)
  101 |     })
```

_file_excerpt · [util/signature/datasigner.go](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/util/signature/datasigner.go#L7) · line 7 · SHA-256 60098a6b34b64d14bdec3fadd36b18dbe0a11964343ee3edbb9b66bb88ceafb1_

```
    6 | import (
    7 | 	"crypto/ecdsa"
    8 | 
```

_file_excerpt · [util/testhelpers/testhelpers.go](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/util/testhelpers/testhelpers.go#L8) · line 8 · SHA-256 7bb601697126eb0a3f7c00251276a41bfdd7d71c9e9c3bba017bc4195ea58855_

```
    7 | 	"context"
    8 | 	"crypto/ecdsa"
    9 | 	crypto "crypto/rand"
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05553 — Квантово-уязвимый Ed25519: аутентификация и идентификация (сертификаты, токены, аттестация устройств) (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Ed25519:authentication`
- Источник данных: cmd/filtering-report/signer/signertest/pki.go
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 31.7 / 100
- CVSS v3.1: неприменимо

2 упоминаний Ed25519 в 1 файл(ах), например cmd/filtering-report/signer/signertest/pki.go:32. Роль по путям, именам функций и соседнему коду: аутентификация и идентификация (сертификаты, токены, аттестация устройств). Краткоживущая аутентификация безопасна до появления CRQC; долгоживущим идентификаторам (аттестация устройств, ключи УЦ и SSH) план нужен раньше.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте cmd/filtering-report/signer/signertest/pki.go:32 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [cmd/filtering-report/signer/signertest/pki.go](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/cmd/filtering-report/signer/signertest/pki.go#L32) · line 32 · SHA-256 d887d4145c828defa8014afd04c87c463bb1404019855890b87615c593c7166b_

```
   31 | 	t.Helper()
   32 | 	caPub, caPriv, err := ed25519.GenerateKey(rand.Reader)
   33 | 	if err != nil {
```

_file_excerpt · [cmd/filtering-report/signer/signertest/pki.go](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/cmd/filtering-report/signer/signertest/pki.go#L78) · line 78 · SHA-256 1824f187b4c922bb10ec365f5193d33d7ca9cad4842aa4ce8842551fdc308394_

```
   77 | 	t.Helper()
   78 | 	leafPub, leafPriv, err := ed25519.GenerateKey(rand.Reader)
   79 | 	if err != nil {
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05561 — block-buffer 0.10.4 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/block-buffer@0.10.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 31.5 / 100
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

### QSI-2026-05562 — block-buffer 0.12.0 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/block-buffer@0.12.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-qwgh-2vcv-g2f7 для пакета crates.io block-buffer версии 0.12.0: block_buffer: panic corrupts inline buffer position. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-05567 — jsonwebtoken 9.3.1 затронут GHSA-h395-gr6q-cpjc (CVE-2026-25537)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/jsonwebtoken@9.3.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-h395-gr6q-cpjc (CVE-2026-25537) для пакета crates.io jsonwebtoken версии 9.3.1: jsonwebtoken has Type Confusion that leads to potential authorization bypass. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-h395-gr6q-cpjc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-h395-gr6q-cpjc](https://osv.dev/vulnerability/GHSA-h395-gr6q-cpjc) · manifest · SHA-256 9720a2b2a209b67bfbbc4e56983234a05152e9af7cbd900765a7d1b7af1735b2_

```
{"id": "GHSA-h395-gr6q-cpjc", "aliases": ["CVE-2026-25537"], "modified": "2026-09-10T03:50:35.169824826Z", "summary": "jsonwebtoken has Type Confusion that leads to potential authorization bypass", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (10.3.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05585 — rustls 0.23.36 затронут GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.23.36`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285) для пакета crates.io rustls версии 0.23.36: Rustls: TLS 1.3 handshake messages incorrectly accepted across encryption level boundaries. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-05586 — rustls 0.23.36 затронут GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.23.36`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) для пакета crates.io rustls версии 0.23.36: Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-05592 — tar 0.4.44 затронут GHSA-3pv8-6f4r-ffg2

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/tar@0.4.44`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3pv8-6f4r-ffg2 для пакета crates.io tar версии 0.4.44: tar has a PAX header desynchronization issue. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3pv8-6f4r-ffg2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3pv8-6f4r-ffg2](https://osv.dev/vulnerability/GHSA-3pv8-6f4r-ffg2) · manifest · SHA-256 7347123ef62d6493fd7bf39f5c310a5e484c1ed6c3e865bc464fe665c066c7da_

```
{"id": "GHSA-3pv8-6f4r-ffg2", "aliases": [], "modified": "2026-09-10T03:51:04.454810375Z", "summary": "tar has a PAX header desynchronization issue", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.4.46).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05609 — tar 0.4.45 затронут GHSA-3pv8-6f4r-ffg2

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/tar@0.4.45`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 31.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3pv8-6f4r-ffg2 для пакета crates.io tar версии 0.4.45: tar has a PAX header desynchronization issue. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3pv8-6f4r-ffg2
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3pv8-6f4r-ffg2](https://osv.dev/vulnerability/GHSA-3pv8-6f4r-ffg2) · manifest · SHA-256 7347123ef62d6493fd7bf39f5c310a5e484c1ed6c3e865bc464fe665c066c7da_

```
{"id": "GHSA-3pv8-6f4r-ffg2", "aliases": [], "modified": "2026-09-10T03:51:04.454810375Z", "summary": "tar has a PAX header desynchronization issue", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.4.46).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05594 — tar 0.4.44 затронут GHSA-j4xf-2g29-59ph (CVE-2026-33056, RUSTSEC-2026-0067)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/tar@0.4.44`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 26.8 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-j4xf-2g29-59ph (CVE-2026-33056, RUSTSEC-2026-0067) для пакета crates.io tar версии 0.4.44: tar-rs `unpack_in` can chmod arbitrary directories by following symlinks. Проверенный код не упоминает затронутые функции (tar::Entry::unpack, tar::Entry::unpack_in); tar приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-j4xf-2g29-59ph
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-j4xf-2g29-59ph](https://osv.dev/vulnerability/GHSA-j4xf-2g29-59ph) · manifest · SHA-256 f6451dee584946ad1f285b7bf362e4e592d4e34e698030833083f24c72f38cfd_

```
{"id": "GHSA-j4xf-2g29-59ph", "aliases": ["CVE-2026-33056", "RUSTSEC-2026-0067"], "modified": "2026-09-10T03:50:39.751471613Z", "summary": "tar-rs `unpack_in` can chmod arbitrary directories by following symlinks", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:H/A:N"}, {"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:A/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.4.45).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05579 — rand 0.8.5 затронут GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rand@0.8.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 36.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097) для пакета crates.io rand версии 0.8.5: Rand is unsound with a custom logger using rand::rng(). Проверенный код называет rand::rng: затронутый код может быть достижим.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-cq8v-f236-94qc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-cq8v-f236-94qc](https://osv.dev/vulnerability/GHSA-cq8v-f236-94qc) · manifest · SHA-256 a61cde8ef254431f750cff43ce8ebe999ba61525990761c3c15b83d24b6124b6_

```
{"id": "GHSA-cq8v-f236-94qc", "aliases": ["RUSTSEC-2026-0097"], "modified": "2026-09-10T03:50:43.958966498Z", "summary": "Rand is unsound with a custom logger using rand::rng()", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.10.1, 0.8.6, 0.9.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05598 — lru 0.12.5 затронут GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/lru@0.12.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 36.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002) для пакета crates.io lru версии 0.12.5: `IterMut` violates Stacked Borrows by invalidating internal pointer. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-rhfx-m35p-ff5j
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-rhfx-m35p-ff5j](https://osv.dev/vulnerability/GHSA-rhfx-m35p-ff5j) · manifest · SHA-256 9bd1c3868d7fb09703315200579795af27b05959323658e708c1fa1810329225_

```
{"id": "GHSA-rhfx-m35p-ff5j", "aliases": ["RUSTSEC-2026-0002"], "modified": "2026-09-10T03:50:59.064354050Z", "summary": "`IterMut` violates Stacked Borrows by invalidating internal pointer", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.16.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05554 — Плавающая версия компилятора (^0.8.0) в 1 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.0`
- Источник данных: contracts-local/src/osp/ReferenceDAProofValidator.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 31.6 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.0 в 1 файл(ах), впервые в contracts-local/src/osp/ReferenceDAProofValidator.sol:5. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте contracts-local/src/osp/ReferenceDAProofValidator.sol:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts-local/src/osp/ReferenceDAProofValidator.sol](https://github.com/OffchainLabs/nitro/blob/ccc5c828d9ea22f161efc784bac4d4a6559b7e59/contracts-local/src/osp/ReferenceDAProofValidator.sol#L5) · line 5 · SHA-256 54e89a8284e131e84bee9f5064d03bf9ef58139c4247b3eb1a6b1f6bfe46b519_

```
    3 | // SPDX-License-Identifier: BUSL-1.1
    4 | 
    5 | pragma solidity ^0.8.0;
    6 | 
    7 | import "@nitro-contracts/osp/ICustomDAProofValidator.sol";
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-05587 — rustls 0.23.36 затронут GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.23.36`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 27.0 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348) для пакета crates.io rustls версии 0.23.36: Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-05588 — rustls 0.23.36 затронут GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.23.36`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 27.0 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349) для пакета crates.io rustls версии 0.23.36: rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-05602 — p3-symmetric 0.3.3-succinct затронут GHSA-3g92-f9ch-qjcm

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/p3-symmetric@0.3.3-succinct`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 27.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3g92-f9ch-qjcm для пакета crates.io p3-symmetric версии 0.3.3-succinct: Plonky3: The sponge construction used to get a hash function from a cryptographic permutation is not collision resistant for inputs of different lengths. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-05568 — keccak 0.1.5 затронут GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/keccak@0.1.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 22.9 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012) для пакета crates.io keccak версии 0.1.5: Unsoundness in opt-in ARMv8 assembly backend for `keccak`. Затронутый код находится за флагом Cargo `asm`, выключенным по умолчанию; ни один проверенный манифест его не включает — бюллетень не применим, если флаг не включает другая зависимость.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-3288-p39f-rqpv
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-3288-p39f-rqpv](https://osv.dev/vulnerability/GHSA-3288-p39f-rqpv) · manifest · SHA-256 d5a8f5565101ab9d60521142f31c54583db5b87e9a59fc99e1fa93d6c2e5f782_

```
{"id": "GHSA-3288-p39f-rqpv", "aliases": ["RUSTSEC-2026-0012"], "modified": "2026-09-10T03:50:59.332505686Z", "summary": "Unsoundness in opt-in ARMv8 assembly backend for `keccak`", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:H/AT:P/PR:N/UI:N/VC:N/VI:L/VA:N/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.1.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05563 — crossbeam-epoch 0.9.18 затронут RUSTSEC-2026-0204 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crossbeam-epoch@0.9.18`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0204 для пакета crates.io crossbeam-epoch версии 0.9.18: Invalid pointer dereference in `fmt::Pointer` impl for `Atomic` and `Shared` when the underlying pointer is invalid. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0204
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0204](https://osv.dev/vulnerability/RUSTSEC-2026-0204) · manifest · SHA-256 87f069b4fa857d22ba2571deff7f541f4622924fb5fc8545cd46d35b7d427b95_

```
{"id": "RUSTSEC-2026-0204", "aliases": [], "modified": "2026-07-06T22:30:04.159269138Z", "summary": "Invalid pointer dereference in `fmt::Pointer` impl for `Atomic` and `Shared` when the underlying pointer is invalid", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.9.20).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05564 — crypto-bigint 0.5.5 затронут RUSTSEC-2026-0387 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crypto-bigint@0.5.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
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

### QSI-2026-05566 — h2 0.4.13 затронут RUSTSEC-2026-0258 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/h2@0.4.13`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0258 для пакета crates.io h2 версии 0.4.13: h2 unbounded empty DATA frames. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-05569 — lru 0.16.3 затронут RUSTSEC-2026-0253 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/lru@0.16.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0253 для пакета crates.io lru версии 0.16.3: Potential use-after-free due to lack of panic safety in `LruCache::pop()`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0253
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0253](https://osv.dev/vulnerability/RUSTSEC-2026-0253) · manifest · SHA-256 82a341ad1e624183fd43c087afde5eb620b02fb5f5dbd7e44d5cee598aa0935c_

```
{"id": "RUSTSEC-2026-0253", "aliases": [], "modified": "2026-08-11T11:15:06.101553049Z", "summary": "Potential use-after-free due to lack of panic safety in `LruCache::pop()`", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.18.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05570 — memmap2 0.6.2 затронут RUSTSEC-2026-0186 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/memmap2@0.6.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0186 для пакета crates.io memmap2 версии 0.6.2: Unchecked pointer offset in crate `memmap2`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (memmap2::Mmap::advise_range, memmap2::Mmap::unchecked_advise_range, memmap2::MmapMut::advise_range, memmap2::MmapMut::flush_async_range, memmap2::MmapMut::flush_range, memmap2::MmapMut::unchecked_advise_range); memmap2 приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0186
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0186](https://osv.dev/vulnerability/RUSTSEC-2026-0186) · manifest · SHA-256 70b02eedb4e58b99412d14613c1a9dc60f7cb08fd4835cd298286af4dc42664e_

```
{"id": "RUSTSEC-2026-0186", "aliases": [], "modified": "2026-06-22T18:15:03.600280397Z", "summary": "Unchecked pointer offset in crate `memmap2`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.9.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05571 — memmap2 0.9.10 затронут RUSTSEC-2026-0186 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/memmap2@0.9.10`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0186 для пакета crates.io memmap2 версии 0.9.10: Unchecked pointer offset in crate `memmap2`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (memmap2::Mmap::advise_range, memmap2::Mmap::unchecked_advise_range, memmap2::MmapMut::advise_range, memmap2::MmapMut::flush_async_range, memmap2::MmapMut::flush_range, memmap2::MmapMut::unchecked_advise_range); memmap2 приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0186
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0186](https://osv.dev/vulnerability/RUSTSEC-2026-0186) · manifest · SHA-256 70b02eedb4e58b99412d14613c1a9dc60f7cb08fd4835cd298286af4dc42664e_

```
{"id": "RUSTSEC-2026-0186", "aliases": [], "modified": "2026-06-22T18:15:03.600280397Z", "summary": "Unchecked pointer offset in crate `memmap2`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.9.11).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05575 — quinn-proto 0.11.14 затронут RUSTSEC-2026-0338 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.14`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0338 для пакета crates.io quinn-proto версии 0.11.14: Remote peer can panic quinn-proto with zero-length STREAM frames during unordered reads. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-05576 — quinn-proto 0.11.14 затронут RUSTSEC-2026-0339 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.14`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0339 для пакета crates.io quinn-proto версии 0.11.14: Unbounded growth of pending connection ID retirements in quinn-proto. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-05578 — quinn-proto 0.11.14 затронут RUSTSEC-2026-0342 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.14`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0342 для пакета crates.io quinn-proto версии 0.11.14: Zero-length DATAGRAM frames bypass the receive buffer limit in quinn-proto. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-05581 — rkyv 0.8.15 затронут RUSTSEC-2026-0233 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rkyv@0.8.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0233 для пакета crates.io rkyv версии 0.8.15: Crafted archives can cause a use-after-free during deserialization. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0233
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0233](https://osv.dev/vulnerability/RUSTSEC-2026-0233) · manifest · SHA-256 7a21fd0c0791d8db79d4a5331398d113589a7d6f1574b6b7ba948ddbc958e452_

```
{"id": "RUSTSEC-2026-0233", "aliases": [], "modified": "2026-08-04T09:30:04.420572601Z", "summary": "Crafted archives can cause a use-after-free during deserialization", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.8.17).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05582 — rkyv 0.8.15 затронут RUSTSEC-2026-0234 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rkyv@0.8.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0234 для пакета crates.io rkyv версии 0.8.15: Insufficient archive validation can cause out-of-bounds reads in archives containing hash tables. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0234
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0234](https://osv.dev/vulnerability/RUSTSEC-2026-0234) · manifest · SHA-256 5903a56887880f9d8208771aa158c18761b76d03fa39c5849463420b7ef8c1a4_

```
{"id": "RUSTSEC-2026-0234", "aliases": [], "modified": "2026-08-04T09:30:04.411453104Z", "summary": "Insufficient archive validation can cause out-of-bounds reads in archives containing hash tables", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.8.17).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05583 — rkyv 0.8.15 затронут RUSTSEC-2026-0235 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rkyv@0.8.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0235 для пакета crates.io rkyv версии 0.8.15: Insufficient archive validation can cause out-of-bounds reads in archives containing Rc/Arc. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0235
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0235](https://osv.dev/vulnerability/RUSTSEC-2026-0235) · manifest · SHA-256 73e1a541852639bb4264bd984666da1689d870d1672957f9f6335455693a19b1_

```
{"id": "RUSTSEC-2026-0235", "aliases": [], "modified": "2026-08-04T09:30:04.382146100Z", "summary": "Insufficient archive validation can cause out-of-bounds reads in archives containing Rc/Arc", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.8.17).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05584 — ruint 1.17.2 затронут RUSTSEC-2026-0220 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/ruint@1.17.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0220 для пакета crates.io ruint версии 1.17.2: Uint shift operations: incorrect overflow flags and truncated shift amounts. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код называет ruint::Uint::checked_shl: затронутый код может быть достижим.

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

### QSI-2026-05589 — rustls-webpki 0.103.13 затронут RUSTSEC-2026-0382 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.103.13`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0382 (CVE-2026-111943) для пакета crates.io rustls-webpki версии 0.103.13: Certificate verification may accept distrusted intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0382
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0382](https://osv.dev/vulnerability/RUSTSEC-2026-0382) · manifest · SHA-256 9111e73d752392534752d5ea5c9da4ec9a422a29c088531d446d16b27a016fa8_

```
{"id": "RUSTSEC-2026-0382", "aliases": ["CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0381", "RUSTSEC-2026-0383"], "modified": "2026-10-21T00:55:56.763143468Z", "summary": "Certificate verification may accept distrusted intermediates", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.103.16, 0.104.0-alpha.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05599 — lru 0.12.5 затронут RUSTSEC-2026-0253 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/lru@0.12.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0253 для пакета crates.io lru версии 0.12.5: Potential use-after-free due to lack of panic safety in `LruCache::pop()`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0253
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0253](https://osv.dev/vulnerability/RUSTSEC-2026-0253) · manifest · SHA-256 82a341ad1e624183fd43c087afde5eb620b02fb5f5dbd7e44d5cee598aa0935c_

```
{"id": "RUSTSEC-2026-0253", "aliases": [], "modified": "2026-08-11T11:15:06.101553049Z", "summary": "Potential use-after-free due to lack of panic safety in `LruCache::pop()`", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.18.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05604 — scc 2.4.0 затронут RUSTSEC-2026-0205 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/scc@2.4.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0205 для пакета crates.io scc версии 2.4.0: `Array::insert` violates exception safety if compare function panics, leading to potential Double-Free. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0205
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0205](https://osv.dev/vulnerability/RUSTSEC-2026-0205) · manifest · SHA-256 1052eebb807359861be7509067db80a5c1e2c649df3cc0ec55be382a548eba95_

```
{"id": "RUSTSEC-2026-0205", "aliases": [], "modified": "2026-07-07T09:30:04.274635773Z", "summary": "`Array::insert` violates exception safety if compare function panics, leading to potential Double-Free", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (3.8.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05605 — webpki-roots 1.0.7 затронут RUSTSEC-2026-0381 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/webpki-roots@1.0.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0381 (CVE-2026-111943) для пакета crates.io webpki-roots версии 1.0.7: Bundled root certificates allow trust in distrusted emSign intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0381
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0381](https://osv.dev/vulnerability/RUSTSEC-2026-0381) · manifest · SHA-256 a97aff76592b60902cd4b16acc1ea2e7be27cd23fb1cd59575028f4953d51114_

```
{"id": "RUSTSEC-2026-0381", "aliases": ["CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0382", "RUSTSEC-2026-0383"], "modified": "2026-10-21T06:30:02.818201920Z", "summary": "Bundled root certificates allow trust in distrusted emSign intermediates", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.26.11, 1.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05611 — github.com/ethereum/go-ethereum v1.16.2 затронут GHSA-2gjw-fg97-vg3r (CVE-2026-26314, GO-2026-4507)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/ethereum/go-ethereum@v1.16.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 26.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-2gjw-fg97-vg3r (CVE-2026-26314, GO-2026-4507) для пакета Go github.com/ethereum/go-ethereum версии v1.16.2: Go Ethereum affected by DoS via malicious p2p message. Ни одна из затронутых функций (github.com/ethereum/go-ethereum/crypto/secp256k1.BitCurve.IsOnCurve) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-2gjw-fg97-vg3r
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-2gjw-fg97-vg3r](https://osv.dev/vulnerability/GHSA-2gjw-fg97-vg3r) · line 28 · SHA-256 e5b4dabd74c53584a475c57834341993de247a2586bb694ece39cfd600d656aa_

```
{"id": "GHSA-2gjw-fg97-vg3r", "aliases": ["CVE-2026-26314", "GO-2026-4507"], "modified": "2026-02-28T06:26:28.686606Z", "summary": "Go Ethereum affected by DoS via malicious p2p message", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.9).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05613 — github.com/ethereum/go-ethereum v1.16.2 затронут GHSA-m6j8-rg6r-7mv8 (CVE-2026-26315, GO-2026-4511)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/ethereum/go-ethereum@v1.16.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 26.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-m6j8-rg6r-7mv8 (CVE-2026-26315, GO-2026-4511) для пакета Go github.com/ethereum/go-ethereum версии v1.16.2: Go Ethereum Improperly Validates the ECIES Public Key in RLPx Handshake. Ни одна из затронутых функций (github.com/ethereum/go-ethereum/crypto/ecies.Encrypt, github.com/ethereum/go-ethereum/crypto/ecies.PrivateKey.Decrypt, github.com/ethereum/go-ethereum/crypto/ecies.PrivateKey.GenerateShared) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-m6j8-rg6r-7mv8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-m6j8-rg6r-7mv8](https://osv.dev/vulnerability/GHSA-m6j8-rg6r-7mv8) · line 28 · SHA-256 964f80060e6787b2dbb9df3bbffbed1a12532004d1792590f6732e67939d0477_

```
{"id": "GHSA-m6j8-rg6r-7mv8", "aliases": ["CVE-2026-26315", "GO-2026-4511"], "modified": "2026-02-28T06:26:19.014657Z", "summary": "Go Ethereum Improperly Validates the ECIES Public Key in RLPx Handshake", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.16.9).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05617 — github.com/pion/dtls/v3 v3.1.2 затронут GHSA-wg4g-wm44-ch5j (CVE-2026-54908, GO-2026-6165)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/pion/dtls/v3@v3.1.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 26.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-wg4g-wm44-ch5j (CVE-2026-54908, GO-2026-6165) для пакета Go github.com/pion/dtls/v3 версии v3.1.2: Pion DTLS vulnerable to denial of service via panic while parsing a crafted ECDHE_PSK ServerKeyExchange message. Ни одна из затронутых функций (github.com/pion/dtls/v3/pkg/protocol/handshake.Handshake.Unmarshal, github.com/pion/dtls/v3/pkg/protocol/handshake.MessageServerKeyExchange.Unmarshal) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-wg4g-wm44-ch5j
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-wg4g-wm44-ch5j](https://osv.dev/vulnerability/GHSA-wg4g-wm44-ch5j) · line 91 · SHA-256 4fe5a380070c77e14e3215966d60d62e5d2776379f34912eccee3054d2d2bf20_

```
{"id": "GHSA-wg4g-wm44-ch5j", "aliases": ["CVE-2026-54908", "GO-2026-6165"], "modified": "2026-09-10T03:51:12.447888499Z", "summary": "Pion DTLS vulnerable to denial of service via panic while parsing a crafted ECDHE_PSK ServerKeyExchange message", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:P/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.1.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05618 — github.com/pion/stun/v3 v3.1.2 затронут GHSA-34rh-wp3j-6cxc (CVE-2026-54909, GO-2026-6163)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/github.com/pion/stun/v3@v3.1.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 26.5 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-34rh-wp3j-6cxc (CVE-2026-54909, GO-2026-6163) для пакета Go github.com/pion/stun/v3 версии v3.1.2: Pion STUN vulnerable to remote denial of service via panic while parsing a malformed XOR-MAPPED-ADDRESS attribute. Ни одна из затронутых функций (github.com/pion/stun/v3.XORMappedAddress.GetFrom, github.com/pion/stun/v3.XORMappedAddress.GetFromAs) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-34rh-wp3j-6cxc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-34rh-wp3j-6cxc](https://osv.dev/vulnerability/GHSA-34rh-wp3j-6cxc) · line 93 · SHA-256 25b88eee7863898f5def9a554b94bf4f6ddbae56da03d4abd189bf9ea0cea347_

```
{"id": "GHSA-34rh-wp3j-6cxc", "aliases": ["CVE-2026-54909", "GO-2026-6163"], "modified": "2026-09-10T03:50:51.344851444Z", "summary": "Pion STUN vulnerable to remote denial of service via panic while parsing a malformed XOR-MAPPED-ADDRESS attribute", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (3.1.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05560 — bincode 1.3.3: информационный бюллетень RUSTSEC-2025-0141 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `dependency:crates.io/bincode@1.3.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.7 / 100
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

### QSI-2026-05565 — derivative 2.2.0: информационный бюллетень RUSTSEC-2024-0388 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `dependency:crates.io/derivative@2.2.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.7 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2024-0388 для пакета crates.io derivative версии 2.2.0 как информационный (unmaintained): `derivative` is unmaintained; consider using an alternative. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0388
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2024-0388](https://osv.dev/vulnerability/RUSTSEC-2024-0388) · manifest · SHA-256 0624a2acbe96d2e8c44b2e7c9e0253aa4d99e8e969cd062a4b077f6a30749e57_

```
{"id": "RUSTSEC-2024-0388", "aliases": [], "modified": "2024-11-10T13:34:40Z", "summary": "`derivative` is unmaintained; consider using an alternative", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-05572 — paste 1.0.15: информационный бюллетень RUSTSEC-2024-0436 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `dependency:crates.io/paste@1.0.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 18.7 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2024-0436 для пакета crates.io paste версии 1.0.15 как информационный (unmaintained): paste - no longer maintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0436
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2024-0436](https://osv.dev/vulnerability/RUSTSEC-2024-0436) · manifest · SHA-256 a05e9b714be6a38828db6db916da526a791846f91cce87246d6b9d7fbc0b7108_

```
{"id": "RUSTSEC-2024-0436", "aliases": [], "modified": "2026-01-27T22:03:15.694766Z", "summary": "paste - no longer maintained", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-05559 — anyhow 1.0.100 затронут RUSTSEC-2026-0190 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/anyhow@1.0.100`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 15.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0190 для пакета crates.io anyhow версии 1.0.100: Unsoundness in `Error::downcast_mut()`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни одна из затронутых функций (anyhow::Error::downcast_mut) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0190
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0190](https://osv.dev/vulnerability/RUSTSEC-2026-0190) · manifest · SHA-256 9b326e11cad5998fcbb9f1ebd28aa1272c12693cad71de91698880f0657cc0b1_

```
{"id": "RUSTSEC-2026-0190", "aliases": [], "modified": "2026-06-29T14:15:03.650725453Z", "summary": "Unsoundness in `Error::downcast_mut()`", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.0.103).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05595 — tokio 1.48.0 затронут RUSTSEC-2026-0386 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/tokio@1.48.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 15.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0386 для пакета crates.io tokio версии 1.48.0: `AsyncFd::new` and related constructors violate I/O safety. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни одна из затронутых функций (tokio::io::unix::AsyncFd::new, tokio::io::unix::AsyncFd::try_new, tokio::io::unix::AsyncFd::try_with_interest, tokio::io::unix::AsyncFd::with_interest) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

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

### QSI-2026-05606 — anyhow 1.0.102 затронут RUSTSEC-2026-0190 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/anyhow@1.0.102`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 15.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0190 для пакета crates.io anyhow версии 1.0.102: Unsoundness in `Error::downcast_mut()`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни одна из затронутых функций (anyhow::Error::downcast_mut) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0190
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0190](https://osv.dev/vulnerability/RUSTSEC-2026-0190) · manifest · SHA-256 9b326e11cad5998fcbb9f1ebd28aa1272c12693cad71de91698880f0657cc0b1_

```
{"id": "RUSTSEC-2026-0190", "aliases": [], "modified": "2026-06-29T14:15:03.650725453Z", "summary": "Unsoundness in `Error::downcast_mut()`", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (1.0.103).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05616 — golang.org/x/sys v0.41.0 затронут GO-2026-5024 (CVE-2026-39824) (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:Go/golang.org/x/sys@v0.41.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 15.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GO-2026-5024 (CVE-2026-39824) для пакета Go golang.org/x/sys версии v0.41.0: Invoking integer overflow in NewNTUnicodeString in golang.org/x/sys/windows. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни одна из затронутых функций (golang.org/x/sys/windows.NewNTUnicodeString) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GO-2026-5024
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GO-2026-5024](https://osv.dev/vulnerability/GO-2026-5024) · line 56 · SHA-256 420cf99d07213297031057b23f827a6ef0b52d25c5af472d5b7f7cd7244e2331_

```
{"id": "GO-2026-5024", "aliases": ["CVE-2026-39824"], "modified": "2026-06-09T18:59:22.740765220Z", "summary": "Invoking integer overflow in NewNTUnicodeString in golang.org/x/sys/windows", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.44.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05619 — 6 бюллетеней в 2 пакет(ах) crates.io, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:crates.io:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 13.7 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 6 бюллетеней (4 с оценкой high или critical) для 2 пакет(ов) crates.io, которые подтягивают только инструменты разработки или сборки (Cargo.lock): например, aws-lc-sys@0.37.0 [dev]: GHSA-394x-vwmw-crm3, GHSA-65p9-r9h6-22vj, GHSA-9f94-5g5w-gf6r, GHSA-hfpc-8r3f-gw53, GHSA-vw5v-4f2q-w9xf; webpki-root-certs@1.0.5 [dev]: RUSTSEC-2026-0383. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в Cargo.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (crates.io)](https://osv.dev/) · Cargo.lock · SHA-256 8584b0a179203757b0268f65a7d0319e9433f08d38b40aec0264e91a513cb4a9_

```
aws-lc-sys@0.37.0 [dev]: GHSA-394x-vwmw-crm3, GHSA-65p9-r9h6-22vj, GHSA-9f94-5g5w-gf6r, GHSA-hfpc-8r3f-gw53, GHSA-vw5v-4f2q-w9xf
webpki-root-certs@1.0.5 [dev]: RUSTSEC-2026-0383
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05557 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 12.2 / 100
- CVSS v3.1: неприменимо

В 66 манифестах зависимостей QSI нашёл криптобиблиотеки (curve25519-dalek, ecdsa, ed25519-dalek, golang.org/x/crypto, jose, jsonwebtoken, k256, p256, ring, rustls, secp256k1), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · Cargo.lock, Cargo.toml, crates/arbutil/Cargo.toml, crates/brotli/Cargo.toml, crates/caller-env/Cargo.toml, crates/jit/Cargo.toml, crates/prover/Cargo.toml, crates/prover-ffi/Cargo.toml, crates/sp1/Cargo.lock, crates/sp1/Cargo.toml, crates/sp1/replay-builder/Cargo.toml, crates/sp1/replay-io/Cargo.toml, crates/sp1/replay-program/Cargo.toml, crates/sp1/replay-runner/Cargo.toml, crates/sp1/stylus-compiler-program/Cargo.toml, crates/sp1/stylus-compiler-runner/Cargo.toml, crates/stylus/Cargo.toml, cra · SHA-256 5baaa43efbe07ca5dc33cc42f05b15645cf3f4b75217f49448e5d895271851ea_

```
Crypto libraries: curve25519-dalek, ecdsa, ed25519-dalek, golang.org/x/crypto, jose, jsonwebtoken, k256, p256, ring, rustls, secp256k1
```

**Ограничения проверки.** Отсутствие доказательств не является доказательством отсутствия: системные библиотеки и транзитивные зависимости могут не указываться.

**Рекомендация.** Определите источник поддержки PQC (TLS-терминатор, KMS/HSM, обновление библиотек).

**Повторная проверка.** Повторите сканирование после обновлений.

### QSI-2026-05558 — adler 1.0.2: информационный бюллетень RUSTSEC-2025-0056 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/adler@1.0.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 11.2 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2025-0056 для пакета crates.io adler версии 1.0.2 как информационный (unmaintained): adler crate is unmaintained, use adler2 instead. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0056
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2025-0056](https://osv.dev/vulnerability/RUSTSEC-2025-0056) · manifest · SHA-256 e9b7ae0431d69f626bc876560ccaff44bb57b35757fd9296256424ca73e69fd2_

```
{"id": "RUSTSEC-2025-0056", "aliases": [], "modified": "2025-09-05T09:05:48Z", "summary": "adler crate is unmaintained, use adler2 instead", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-05573 — proc-macro-error2 2.0.1: информационный бюллетень RUSTSEC-2026-0173 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/proc-macro-error2@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 11.2 / 100
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

### QSI-2026-05597 — ansi_term 0.12.1: информационный бюллетень RUSTSEC-2021-0139 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/ansi_term@0.12.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 11.2 / 100
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

### QSI-2026-05600 — number_prefix 0.4.0: информационный бюллетень RUSTSEC-2025-0119 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/number_prefix@0.4.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 11.2 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2025-0119 для пакета crates.io number_prefix версии 0.4.0 как информационный (unmaintained): number_prefix crate is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0119
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2025-0119](https://osv.dev/vulnerability/RUSTSEC-2025-0119) · manifest · SHA-256 fdb2df9598c08223c197071bbc0a302c79f15f783a40297c48b4513e4162cda5_

```
{"id": "RUSTSEC-2025-0119", "aliases": [], "modified": "2025-11-18T08:13:56Z", "summary": "number_prefix crate is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-05603 — rustls-pemfile 2.2.0: информационный бюллетень RUSTSEC-2025-0134 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls-pemfile@2.2.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 11.2 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2025-0134 для пакета crates.io rustls-pemfile версии 2.2.0 как информационный (unmaintained): rustls-pemfile is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0134
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2025-0134](https://osv.dev/vulnerability/RUSTSEC-2025-0134) · manifest · SHA-256 8a337a969850fe57bfcbd48340c157654002251ff4155f018ebd3fc00f0657fc_

```
{"id": "RUSTSEC-2025-0134", "aliases": [], "modified": "2025-12-05T19:07:59.622592Z", "summary": "rustls-pemfile is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-05607 — mach 0.3.2: информационный бюллетень RUSTSEC-2020-0168 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/mach@0.3.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:10 UTC
- Балл приоритета: 11.2 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2020-0168 для пакета crates.io mach версии 0.3.2 как информационный (unmaintained): mach is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2020-0168
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2020-0168](https://osv.dev/vulnerability/RUSTSEC-2020-0168) · manifest · SHA-256 3fabfdc54105fbb9d74ee0b7313974e2609cdd9df50a070060f4f4505bc30480_

```
{"id": "RUSTSEC-2020-0168", "aliases": [], "modified": "2023-03-12T06:59:25Z", "summary": "mach is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.


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
| **подпись транзакций и сообщений** | ECDSA (3), Ed25519 (2) | QSI-2026-05552, QSI-2026-05555 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |
| **аутентификация и идентификация (сертификаты, токены, аттестация устройств)** | Ed25519 (1) | QSI-2026-05553 | Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме |
| **роль не определена** | ECDSA (6) | QSI-2026-05551 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм в конечных полях | взламывает | Q1 | BLS12-381 (1) | Взламывает Диффи–Хеллмана в конечных полях и DSA при любом размере. Переводите установление ключей на ML-KEM (на переходный период — гибрид с X25519 или ECDH), подписи — на ML-DSA или SLH-DSA. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | BLS12-381 (1), ECDSA (9), Ed25519 (3) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | HMAC (2), Keccak-256 (54), SHA-2 (12) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (54), SHA-2 (12) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- slither: slither is not installed on the server (pip install slither-analyzer + solc)

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P1 | QSI-2026-05550 | Удалите отключение проверки сертификатов в arbnode/dataposter/config/config.go. | устранение первопричины | Отключений проверки не осталось вне явно помеченного тестового кода. |
| P2 | QSI-2026-05614 | Обновите github.com/ethereum/go-ethereum до исправленной версии (1.16.8). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mq3p-rrmp-79jg (CVE-2026-22868, GO-2026-4314). |
| P2 | QSI-2026-05615 | Обновите github.com/ethereum/go-ethereum до исправленной версии (1.16.8). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-mr7q-c9w9-wh4h (CVE-2026-22862, GO-2026-4315). |
| P2 | QSI-2026-05574 | Обновите quinn-proto до исправленной версии (0.11.15). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4w2j-m93h-cj5j (CVE-2026-25800, RUSTSEC-2026-0185). |
| P2 | QSI-2026-05577 | Обновите quinn-proto до исправленной версии (0.11.18). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2026-0340. |
| P2 | QSI-2026-05590 | Обновите ruzstd до исправленной версии (0.9.1). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2026-0344. |
| P2 | QSI-2026-05593 | Обновите tar до исправленной версии (0.4.45). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-gchp-q4r4-x4ff (CVE-2026-33055, RUSTSEC-2026-0068). |
| P2 | QSI-2026-05601 | Обновите p3-challenger до исправленной версии (0.4.3, 0.5.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vj64-rjf3-w3v7 (CVE-2026-46654). |
| P2 | QSI-2026-05580 | Обновите rkyv до исправленной версии (0.8.16). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-vfvv-c25p-m7mm (RUSTSEC-2026-0122). |
| P2 | QSI-2026-05591 | Обновите serde_with до исправленной версии (3.21.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7gcf-g7xr-8hxj. |
| P2 | QSI-2026-05608 | Обновите serde_with до исправленной версии (3.21.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7gcf-g7xr-8hxj. |
| P2 | QSI-2026-05610 | Обновите github.com/codeclysm/extract/v3 до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-8rm2-93mq-jqhc (CVE-2024-47877, GO-2024-3196). |
| P2 | QSI-2026-05612 | Обновите github.com/ethereum/go-ethereum до исправленной версии (1.17.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-689v-6xwf-5jf3 (CVE-2026-26313, GO-2026-4508). |
| P2 | QSI-2026-05561 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-05562 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-05567 | Обновите jsonwebtoken до исправленной версии (10.3.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h395-gr6q-cpjc (CVE-2026-25537). |
| P2 | QSI-2026-05585 | Обновите rustls до исправленной версии (0.23.45). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285). |
| P2 | QSI-2026-05586 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346). |
| P2 | QSI-2026-05592 | Обновите tar до исправленной версии (0.4.46). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3pv8-6f4r-ffg2. |
| P2 | QSI-2026-05609 | Обновите tar до исправленной версии (0.4.46). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3pv8-6f4r-ffg2. |
| P2 | QSI-2026-05594 | Обновите tar до исправленной версии (0.4.45). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-j4xf-2g29-59ph (CVE-2026-33056, RUSTSEC-2026-0067). |
| P2 | QSI-2026-05579 | Обновите rand до исправленной версии (0.10.1, 0.8.6, 0.9.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097). |
| P2 | QSI-2026-05598 | Обновите lru до исправленной версии (0.16.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-rhfx-m35p-ff5j (RUSTSEC-2026-0002). |
| P2 | QSI-2026-05587 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348). |
| P2 | QSI-2026-05588 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349). |
| P2 | QSI-2026-05602 | Обновите p3-symmetric до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3g92-f9ch-qjcm. |
| P2 | QSI-2026-05568 | Обновите keccak до исправленной версии (0.1.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012). |
| P2 | QSI-2026-05611 | Обновите github.com/ethereum/go-ethereum до исправленной версии (1.16.9). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2gjw-fg97-vg3r (CVE-2026-26314, GO-2026-4507). |
| P2 | QSI-2026-05613 | Обновите github.com/ethereum/go-ethereum до исправленной версии (1.16.9). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-m6j8-rg6r-7mv8 (CVE-2026-26315, GO-2026-4511). |
| P2 | QSI-2026-05617 | Обновите github.com/pion/dtls/v3 до исправленной версии (3.1.4). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-wg4g-wm44-ch5j (CVE-2026-54908, GO-2026-6165). |
| P2 | QSI-2026-05618 | Обновите github.com/pion/stun/v3 до исправленной версии (3.1.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-34rh-wp3j-6cxc (CVE-2026-54909, GO-2026-6163). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-05556 | Используйте OpenZeppelin ECDSA.recover с разделением доменов EIP-712 и nonce. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-05563 | Разберите RUSTSEC-2026-0204; при необходимости обновите crossbeam-epoch до исправленной версии (0.9.20). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0204 или результат разбора записан. |
| P3 | QSI-2026-05564 | Разберите RUSTSEC-2026-0387; при необходимости обновите crypto-bigint до исправленной версии (0.7.6). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0387 или результат разбора записан. |
| P3 | QSI-2026-05566 | Разберите RUSTSEC-2026-0258; при необходимости обновите h2 до исправленной версии (0.4.16). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0258 или результат разбора записан. |
| P3 | QSI-2026-05569 | Разберите RUSTSEC-2026-0253; при необходимости обновите lru до исправленной версии (0.18.2). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0253 или результат разбора записан. |
| P3 | QSI-2026-05570 | Разберите RUSTSEC-2026-0186; при необходимости обновите memmap2 до исправленной версии (0.9.11). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0186 или результат разбора записан. |
| P3 | QSI-2026-05571 | Разберите RUSTSEC-2026-0186; при необходимости обновите memmap2 до исправленной версии (0.9.11). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0186 или результат разбора записан. |
| P3 | QSI-2026-05575 | Разберите RUSTSEC-2026-0338; при необходимости обновите quinn-proto до исправленной версии (0.11.18). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0338 или результат разбора записан. |
| P3 | QSI-2026-05576 | Разберите RUSTSEC-2026-0339; при необходимости обновите quinn-proto до исправленной версии (0.11.17). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0339 или результат разбора записан. |
| P3 | QSI-2026-05578 | Разберите RUSTSEC-2026-0342; при необходимости обновите quinn-proto до исправленной версии (0.11.17). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0342 или результат разбора записан. |
| P3 | QSI-2026-05581 | Разберите RUSTSEC-2026-0233; при необходимости обновите rkyv до исправленной версии (0.8.17). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0233 или результат разбора записан. |
| P3 | QSI-2026-05582 | Разберите RUSTSEC-2026-0234; при необходимости обновите rkyv до исправленной версии (0.8.17). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0234 или результат разбора записан. |
| P3 | QSI-2026-05583 | Разберите RUSTSEC-2026-0235; при необходимости обновите rkyv до исправленной версии (0.8.17). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0235 или результат разбора записан. |
| P3 | QSI-2026-05584 | Разберите RUSTSEC-2026-0220; при необходимости обновите ruint до исправленной версии (1.20.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0220 или результат разбора записан. |
| P3 | QSI-2026-05589 | Разберите RUSTSEC-2026-0382 (CVE-2026-111943); при необходимости обновите rustls-webpki до исправленной версии (0.103.16, 0.104.0-alpha.8). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0382 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-05599 | Разберите RUSTSEC-2026-0253; при необходимости обновите lru до исправленной версии (0.18.2). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0253 или результат разбора записан. |
| P3 | QSI-2026-05604 | Разберите RUSTSEC-2026-0205; при необходимости обновите scc до исправленной версии (3.8.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0205 или результат разбора записан. |
| P3 | QSI-2026-05605 | Разберите RUSTSEC-2026-0381 (CVE-2026-111943); при необходимости обновите webpki-roots до исправленной версии (0.26.11, 1.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0381 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-05559 | Разберите RUSTSEC-2026-0190; при необходимости обновите anyhow до исправленной версии (1.0.103). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0190 или результат разбора записан. |
| P3 | QSI-2026-05595 | Разберите RUSTSEC-2026-0386; при необходимости обновите tokio до исправленной версии (1.51.6, 1.53.3). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0386 или результат разбора записан. |
| P3 | QSI-2026-05606 | Разберите RUSTSEC-2026-0190; при необходимости обновите anyhow до исправленной версии (1.0.103). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0190 или результат разбора записан. |
| P3 | QSI-2026-05616 | Разберите GO-2026-5024 (CVE-2026-39824); при необходимости обновите golang.org/x/sys до исправленной версии (0.44.0). | устранение первопричины | Сканирование больше не сообщает GO-2026-5024 (CVE-2026-39824) или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-05552 | Внесите использования Ed25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-05555 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-05551 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-05553 | Внесите использования Ed25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-05554 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-05596 | Замените wee_alloc поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | wee_alloc заменён или решение зафиксировано. |
| P4 | QSI-2026-05552 | Запланируйте миграцию Ed25519 на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05555 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05551 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05553 | Запланируйте миграцию Ed25519 на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05560 | Замените bincode поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | bincode заменён или решение зафиксировано. |
| P4 | QSI-2026-05565 | Замените derivative поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | derivative заменён или решение зафиксировано. |
| P4 | QSI-2026-05572 | Замените paste поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | paste заменён или решение зафиксировано. |
| P4 | QSI-2026-05619 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |
| P4 | QSI-2026-05558 | Замените adler поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | adler заменён или решение зафиксировано. |
| P4 | QSI-2026-05573 | Замените proc-macro-error2 поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | proc-macro-error2 заменён или решение зафиксировано. |
| P4 | QSI-2026-05597 | Замените ansi_term поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | ansi_term заменён или решение зафиксировано. |
| P4 | QSI-2026-05600 | Замените number_prefix поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | number_prefix заменён или решение зафиксировано. |
| P4 | QSI-2026-05603 | Замените rustls-pemfile поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | rustls-pemfile заменён или решение зафиксировано. |
| P4 | QSI-2026-05607 | Замените mach поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | mach заменён или решение зафиксировано. |

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
8. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
9. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
10. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
11. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
12. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
13. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
14. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
15. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
16. M. Ekerå, J. Gärtner — A high-level comparison of state-of-the-art quantum algorithms for breaking asymmetric cryptography (arXiv:2405.14381) — arXiv. <https://arxiv.org/abs/2405.14381> (preprint (2024-05-23): Regev-style algorithms show no overall advantage yet for cryptographic RSA and finite-field sizes)
17. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
18. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
19. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
20. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
21. OSV advisory GHSA-2gjw-fg97-vg3r — OSV.dev. <https://osv.dev/vulnerability/GHSA-2gjw-fg97-vg3r> (modified 2026-02-28T06:26:28.686606Z)
22. OSV advisory GHSA-2mjx-qc3c-rqvc — OSV.dev. <https://osv.dev/vulnerability/GHSA-2mjx-qc3c-rqvc> (modified 2026-10-27T15:30:05.509305490Z)
23. OSV advisory GHSA-3288-p39f-rqpv — OSV.dev. <https://osv.dev/vulnerability/GHSA-3288-p39f-rqpv> (modified 2026-09-10T03:50:59.332505686Z)
24. OSV advisory GHSA-34rh-wp3j-6cxc — OSV.dev. <https://osv.dev/vulnerability/GHSA-34rh-wp3j-6cxc> (modified 2026-09-10T03:50:51.344851444Z)
25. OSV advisory GHSA-3g92-f9ch-qjcm — OSV.dev. <https://osv.dev/vulnerability/GHSA-3g92-f9ch-qjcm> (modified 2026-04-16T23:04:45.978452Z)
26. OSV advisory GHSA-3pv8-6f4r-ffg2 — OSV.dev. <https://osv.dev/vulnerability/GHSA-3pv8-6f4r-ffg2> (modified 2026-09-10T03:51:04.454810375Z)
27. OSV advisory GHSA-4w2j-m93h-cj5j — OSV.dev. <https://osv.dev/vulnerability/GHSA-4w2j-m93h-cj5j> (modified 2026-09-10T03:51:10.288925502Z)
28. OSV advisory GHSA-689v-6xwf-5jf3 — OSV.dev. <https://osv.dev/vulnerability/GHSA-689v-6xwf-5jf3> (modified 2026-02-28T06:26:25.973770Z)
29. OSV advisory GHSA-7gcf-g7xr-8hxj — OSV.dev. <https://osv.dev/vulnerability/GHSA-7gcf-g7xr-8hxj> (modified 2026-09-10T03:51:10.897685062Z)
30. OSV advisory GHSA-8rm2-93mq-jqhc — OSV.dev. <https://osv.dev/vulnerability/GHSA-8rm2-93mq-jqhc> (modified 2024-10-15T19:53:17Z)
31. OSV advisory GHSA-c8m5-c952-6cm4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4> (modified 2026-10-27T16:15:05.354395696Z)
32. OSV advisory GHSA-cq8v-f236-94qc — OSV.dev. <https://osv.dev/vulnerability/GHSA-cq8v-f236-94qc> (modified 2026-09-10T03:50:43.958966498Z)
33. OSV advisory GHSA-gchp-q4r4-x4ff — OSV.dev. <https://osv.dev/vulnerability/GHSA-gchp-q4r4-x4ff> (modified 2026-09-10T03:50:39.204912381Z)
34. OSV advisory GHSA-h2v8-394m-p7vv — OSV.dev. <https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv> (modified 2026-10-27T16:15:05.337819489Z)
35. OSV advisory GHSA-h395-gr6q-cpjc — OSV.dev. <https://osv.dev/vulnerability/GHSA-h395-gr6q-cpjc> (modified 2026-09-10T03:50:35.169824826Z)
36. OSV advisory GHSA-j4xf-2g29-59ph — OSV.dev. <https://osv.dev/vulnerability/GHSA-j4xf-2g29-59ph> (modified 2026-09-10T03:50:39.751471613Z)
37. OSV advisory GHSA-m6j8-rg6r-7mv8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-m6j8-rg6r-7mv8> (modified 2026-02-28T06:26:19.014657Z)
38. OSV advisory GHSA-mq3p-rrmp-79jg — OSV.dev. <https://osv.dev/vulnerability/GHSA-mq3p-rrmp-79jg> (modified 2026-02-03T02:58:49.032697Z)
39. OSV advisory GHSA-mr7q-c9w9-wh4h — OSV.dev. <https://osv.dev/vulnerability/GHSA-mr7q-c9w9-wh4h> (modified 2026-02-03T02:59:06.834692Z)
40. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-08-19T19:30:06.686866977Z)
41. OSV advisory GHSA-rc23-xxgq-x27g — OSV.dev. <https://osv.dev/vulnerability/GHSA-rc23-xxgq-x27g> (modified 2023-11-08T04:22:41.320727Z)
42. OSV advisory GHSA-rhfx-m35p-ff5j — OSV.dev. <https://osv.dev/vulnerability/GHSA-rhfx-m35p-ff5j> (modified 2026-09-10T03:50:59.064354050Z)
43. OSV advisory GHSA-vfvv-c25p-m7mm — OSV.dev. <https://osv.dev/vulnerability/GHSA-vfvv-c25p-m7mm> (modified 2026-09-10T03:50:47.714144241Z)
44. OSV advisory GHSA-vj64-rjf3-w3v7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-vj64-rjf3-w3v7> (modified 2026-06-11T14:15:08.995914138Z)
45. OSV advisory GHSA-w44r-93j7-qv28 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28> (modified 2026-10-27T16:15:05.340347056Z)
46. OSV advisory GHSA-wg4g-wm44-ch5j — OSV.dev. <https://osv.dev/vulnerability/GHSA-wg4g-wm44-ch5j> (modified 2026-09-10T03:51:12.447888499Z)
47. OSV advisory GO-2026-5024 — OSV.dev. <https://osv.dev/vulnerability/GO-2026-5024> (modified 2026-06-09T18:59:22.740765220Z)
48. OSV advisory RUSTSEC-2020-0168 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2020-0168> (modified 2023-03-12T06:59:25Z)
49. OSV advisory RUSTSEC-2021-0139 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2021-0139> (modified 2023-09-06T22:52:31Z)
50. OSV advisory RUSTSEC-2024-0388 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0388> (modified 2024-11-10T13:34:40Z)
51. OSV advisory RUSTSEC-2024-0436 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0436> (modified 2026-01-27T22:03:15.694766Z)
52. OSV advisory RUSTSEC-2025-0056 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0056> (modified 2025-09-05T09:05:48Z)
53. OSV advisory RUSTSEC-2025-0119 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0119> (modified 2025-11-18T08:13:56Z)
54. OSV advisory RUSTSEC-2025-0134 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0134> (modified 2025-12-05T19:07:59.622592Z)
55. OSV advisory RUSTSEC-2025-0141 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0141> (modified 2026-01-16T11:07:28.867553Z)
56. OSV advisory RUSTSEC-2026-0173 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0173> (modified 2026-06-07T21:00:04.318567692Z)
57. OSV advisory RUSTSEC-2026-0186 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0186> (modified 2026-06-22T18:15:03.600280397Z)
58. OSV advisory RUSTSEC-2026-0190 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0190> (modified 2026-06-29T14:15:03.650725453Z)
59. OSV advisory RUSTSEC-2026-0204 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0204> (modified 2026-07-06T22:30:04.159269138Z)
60. OSV advisory RUSTSEC-2026-0205 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0205> (modified 2026-07-07T09:30:04.274635773Z)
61. OSV advisory RUSTSEC-2026-0220 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0220> (modified 2026-07-30T19:15:04.025918010Z)
62. OSV advisory RUSTSEC-2026-0233 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0233> (modified 2026-08-04T09:30:04.420572601Z)
63. OSV advisory RUSTSEC-2026-0234 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0234> (modified 2026-08-04T09:30:04.411453104Z)
64. OSV advisory RUSTSEC-2026-0235 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0235> (modified 2026-08-04T09:30:04.382146100Z)
65. OSV advisory RUSTSEC-2026-0253 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0253> (modified 2026-08-11T11:15:06.101553049Z)
66. OSV advisory RUSTSEC-2026-0258 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0258> (modified 2026-10-12T18:00:10.934581734Z)
67. OSV advisory RUSTSEC-2026-0338 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0338> (modified 2026-10-12T18:15:01.969514645Z)
68. OSV advisory RUSTSEC-2026-0339 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0339> (modified 2026-10-12T18:15:01.956822776Z)
69. OSV advisory RUSTSEC-2026-0340 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0340> (modified 2026-10-12T18:15:01.975478256Z)
70. OSV advisory RUSTSEC-2026-0342 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0342> (modified 2026-10-12T18:15:01.956681478Z)
71. OSV advisory RUSTSEC-2026-0344 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0344> (modified 2026-10-13T10:45:04.080993335Z)
72. OSV advisory RUSTSEC-2026-0381 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0381> (modified 2026-10-21T06:30:02.818201920Z)
73. OSV advisory RUSTSEC-2026-0382 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0382> (modified 2026-10-21T00:55:56.763143468Z)
74. OSV advisory RUSTSEC-2026-0386 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0386> (modified 2026-10-23T14:45:03.847864944Z)
75. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
76. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
77. OWASP Application Security Verification Standard — OWASP. <https://owasp.org/www-project-application-security-verification-standard/> (living standard — check the project page for the current version)
78. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
79. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
80. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)
81. Smart Contract Weakness Classification (SWC) Registry — SWC community (no longer actively maintained). <https://swcregistry.io/> (historic reference; still widely cited)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| HMAC |  |  | сниженный запас (Гровер), одобрен | допустимо | 2 | 2 | daprovider/anytrust/redis_storage_service.go:8; util/signature/simple_hmac.go |
| SHA-2 | SHA-512 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | scripts/create-test-preimages.py:21 |
| Keccak-256 | Keccak-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 54 | 54 | arbnode/batch_poster.go:581; arbnode/mel/messages.go:56; arbos/l1pricing/l1pricing.go:560 |
| SHA-2 | SHA-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 11 | 11 | cmd/nitro/init/init.go:8; crates/caller-env/src/wavmio.rs:172; crates/prover/src/kzg.rs:45 |
| Crypto library | 0.13.4 | k256 (RustCrypto elliptic curves) | н/п | допустимо | 4 | 4 | Cargo.lock; Cargo.toml; crates/sp1/Cargo.lock |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | н/п | допустимо | 3 | 3 | Cargo.lock; crates/sp1/Cargo.lock; nitro-reth/Cargo.lock |
| Crypto library | 0.17.14 | ring (ring (Rust)) | н/п | допустимо | 3 | 3 | Cargo.lock; crates/sp1/Cargo.lock; nitro-reth/Cargo.lock |
| Crypto library | 0.23.36 | rustls (rustls) | н/п | допустимо | 2 | 2 | Cargo.lock; crates/sp1/Cargo.lock |
| Crypto library | 0.30.0 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 2 | 2 | Cargo.lock; nitro-reth/Cargo.lock |
| Crypto library | 9.3.1 | jsonwebtoken (jsonwebtoken (Node)) | н/п | допустимо | 2 | 2 | Cargo.lock; nitro-reth/Cargo.lock |
| Crypto library | workspace | k256 (RustCrypto elliptic curves) | н/п | допустимо | 2 | 2 | crates/caller-env/Cargo.toml; nitro-reth/crates/arb-test-harness/Cargo.toml |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 2 | 2 | crates/sp1/Cargo.lock; nitro-reth/Cargo.lock |
| Crypto library | v0.48.0 | golang.org/x/crypto (Go x/crypto) | н/п | допустимо | 1 | 1 | go.mod:105 |
| Crypto library | 0.23.37 | rustls (rustls) | н/п | допустимо | 1 | 1 | nitro-reth/Cargo.lock |
| Crypto library | 0.31.1 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | nitro-reth/Cargo.lock |
| Crypto library | 2.2.0 | ed25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | nitro-reth/Cargo.lock |
| Crypto library | 4.1.3 | curve25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | nitro-reth/Cargo.lock |
| Crypto library | 0.13 | k256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | nitro-reth/Cargo.toml |
| Crypto library | 6.2.3 | jose (jose (Node)) | н/п | допустимо | 1 | 1 | nitro-reth/docs/package-lock.json |
| BLS12-381 |  |  | уязвим (Шор) | допустимо | 1 | 1 | blsSignatures/blsSignatures.go |
| ECDSA |  |  | уязвим (Шор) | допустимо | 4 | 4 | cmd/anytrusttool/main.go:9; cmd/nitro/nitro.go:8; util/signature/datasigner.go:7 |
| ECDSA | secp256k1 (ecrecover) |  | уязвим (Шор) | допустимо | 1 | 1 | contracts-local/src/osp/ReferenceDAProofValidator.sol:173 |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 3 | 3 | crates/caller-env/src/arbcrypto.rs:5; nitro-reth/crates/arb-primitives/src/signed_tx.rs:20; nitro-reth/crates/arb-test-harness/src/messaging/signed_tx.rs:3 |
| ECDSA | P-256 |  | уязвим (Шор) | допустимо | 1 | 1 | nitro-reth/crates/arb-precompiles/src/lib.rs:94 |
| Ed25519 | Ed25519 |  | уязвим (Шор) | допустимо | 3 | 3 | cmd/filtering-report/signer/signer.go:133; cmd/filtering-report/signer/signertest/pki.go:32; cmd/filtering-report/signer/signertest/verifier.go:129 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| .github/workflows/process_junit.py | 1831 | `501cf4ac2e1c9730dad137edf41820cacf35a560ad39b78e6b9271a6c108ad3c` | 0 |
| Cargo.lock | 152805 | `0a90dde1a45d9abb5c54503fa89efe5abd0fe0ca2531071f445cfcc92b14f42a` | 0 |
| Cargo.toml | 4240 | `1b9466f1ad4137896c9574b12596ec24ef72e5e33ff54ce38783a649554e7e9e` | 0 |
| arbcompress/compress_common.go | 656 | `06ee4b1dade3dc08229be5af853f24f7237d8a086acc73d197e05b6bba7b34ef` | 0 |
| arbcompress/native.go | 2228 | `e42cb64d4eeafc6af03760635644c8d02aecc3eecf27114661ef0bad44294d70` | 0 |
| arbcompress/wasm.go | 1824 | `2c079b62336528f4ca42aa4f7f3c64dfdb3a9e48b1f02add8a3e3e992fce6b9b` | 0 |
| arbnode/api.go | 3333 | `dab6f699de3d943ebc8adcd0b14f088db4676fec1a71f73596e34f7a82bab2b9` | 0 |
| arbnode/batch_poster.go | 94737 | `849b74897184943a1a9e2d782c74f382ed7a18b130c291a3ddd3d40a9dd87872` | 0 |
| arbnode/block_recordings_pruner.go | 2718 | `2de60bbe1faabb79385c1ae5386de01e1da3f4834695401ebb7bdcf41105dfec` | 0 |
| arbnode/blockmetadata.go | 9008 | `01f8ff801594b9c36c257b424c81edc26d7afc1d353ddbeb1bdd7783e716166d` | 0 |
| arbnode/compression_level.go | 5978 | `9208a6e9430805ae2e8080d00dbe0aea3afaa03ad7074c58e96e45b13a54eb91` | 0 |
| arbnode/consensus_execution_syncer.go | 6747 | `61462047a3acd6e98d7149610120dbd907b73089fd6370b2e808ab3031112d33` | 0 |
| arbnode/dataposter/config/config.go | 15011 | `2271637bbe10189d175f2aba4cd8a7f825028201b6a98987f0424d6381f3751e` | 0 |
| arbnode/dataposter/data_poster.go | 6982 | `251644b610f765417d2d8c49134ff3fc0dc1ded2ad19293849e2760cb6aab684` | 0 |
| arbnode/dataposter/dbstorage/storage.go | 5124 | `05eca677f294c302a35ea85fd11c77dcf409583590ace652243b1e0b543d6653` | 0 |
| arbnode/dataposter/externalsigner/client.go | 1643 | `a46a3a6b0c01b2cc86e337d2335dbab7975d3f124c7e41f4ef9361254b18374a` | 0 |
| arbnode/dataposter/externalsigner/signer.go | 3495 | `9a1e159925daa08211756db2759d2ea00072096788f303538e044a5f878597c8` | 0 |
| arbnode/dataposter/externalsigner/tx.go | 2017 | `d829aacae6cd7f9997787595a740e467cf0fe82340185ec2fa75b9f8420ff194` | 0 |
| arbnode/dataposter/externalsignertest/externalsignertest.go | 5617 | `7c36377d764e2185596c82131abcb49a657187b7fe4d62f72420edab5a570de3` | 0 |
| arbnode/dataposter/fees/allocation.go | 5596 | `7c93362ca3b9d71cca9cddcca84260813db0b064796256485758dc90d59c633a` | 0 |
| arbnode/dataposter/fees/calculator.go | 8142 | `49b45895606e140d6e252c6503ad7d07bdc3fb24dbb0a5c29391a76dae012c91` | 0 |
| arbnode/dataposter/fees/types.go | 497 | `8d81c0a3e6d5ce3fb65374677688ab6f95dde33e4a7be3d898be87fd35979b23` | 0 |
| arbnode/dataposter/fees/update_caps.go | 1357 | `9ac19c4cb9bf5d81d098f5a85992b72fef2f646d458ad4f01bfbd701a868497b` | 0 |
| arbnode/dataposter/lifecycle.go | 11051 | `9cc0e28cb9459b04fcebf8bda20e141c411fc27467a31c839ebea4a3e0afd6df` | 0 |
| arbnode/dataposter/mainloop.go | 3961 | `d8e399b890c69e6c273d1ebae6db21681aa02856776f65af04bd78a30e6dac82` | 0 |
| arbnode/dataposter/metrics/gauges.go | 1299 | `1d8ca498eee7a103d1d7842013907627ff708fd9e175738a7a84c4900571c13f` | 0 |
| arbnode/dataposter/noop/storage.go | 1128 | `f4d9bfe60b5916057a2dce4f8c05700c535d2195f9cd975bb1357030834da104` | 0 |
| arbnode/dataposter/redis/redisstorage.go | 6527 | `3d272e0d2ec0444b7f942b2cbf09119dd5a32d28fa4b7169206fba01be9bb707` | 0 |
| arbnode/dataposter/slice/slicestorage.go | 3415 | `d8cb010fbd51c008b80037856c744bd76830850514704506456096683d5eaa57` | 0 |
| arbnode/dataposter/state/state.go | 2488 | `fc90f95efe4a333e75a32d0339cebb208c16cbfc2f0749c5d8d0748c49e69dad` | 0 |
| arbnode/dataposter/storage/storage.go | 6728 | `43d9281845ed14031f0d49cb99446f0d6dee8152d532636f3a9e71bada8e12d7` | 0 |
| arbnode/dataposter/storage/time.go | 1147 | `3917bd5b6da37a2e2463e2c2fb0891fd200569728701daf356b26b4a1542321e` | 0 |
| arbnode/dataposter/txns.go | 17702 | `9d942244f7d38105f695808793aa6a6d11e73762d2e6fed45c25e291903b4691` | 0 |
| arbnode/db/read/read.go | 2235 | `eaeab9e59bef67121f8cadf4914622a5239fb93819ed3929357b51fbe5070e3f` | 0 |
| arbnode/db/schema/schema.go | 3111 | `eb913953e2b5d761e33c2642062caf40a754eca39d2c5928a52248bf7991c599` | 0 |
| arbnode/delay_buffer.go | 3491 | `974f1d5c8a5e5d588954692683d97a75c093d1e7235448ab6cd72af7a2239458` | 0 |
| arbnode/delayed.go | 10206 | `db770bb0f842a17e166431c3c5379679b1288ffb163a9080a661a8adbbd1f49f` | 0 |
| arbnode/delayed_sequencer.go | 8491 | `1da8911c5405aa5990b680839bbe9651d90083a8eed985900c4537a707eea35d` | 0 |
| arbnode/inbox_reader.go | 30105 | `daa5c5ea09fd7e161243804d7eb74d62f3633b84b9f170a8ed8acae5bf6d7d8d` | 0 |
| arbnode/inbox_tracker.go | 26012 | `6a11212ab18850574bd0a5d596e4dc3a056e7bb217780df5fd701ae51741683b` | 0 |
| arbnode/maintenance.go | 4709 | `cbe1f7b22be202e7b7d0e09653fe0ed3bdad1c2999f029bd0305446f96ab6b62` | 0 |
| arbnode/mel/mel.go | 4002 | `4089e57cbabc44aea99ffe6cd8aad0b95db359658a16df056e3340aef94b6fd9` | 0 |
| arbnode/mel/messages.go | 2717 | `e0e3c4f2eb78adf0832fe0fea2c82630745765a7cbcd323919fd1e93c053f2a7` | 0 |
| arbnode/mel/rpc_runner/rpc_client/client.go | 8255 | `de16df8ec264677a260c63c3f4c8cc53fc7e6f517d943b6a5a2c98fb412584ac` | 0 |
| arbnode/mel/rpc_runner/rpc_server/server.go | 1761 | `5d45debbf414770da461789a48f56c908242c5b6068048ba02a3f8c7eee78ca8` | 0 |
| arbnode/mel/runner/database.go | 8008 | `edf73b7e76b97c7576239bf01bff755ed545cb9c9b0258e55dab67a56a0b9b8f` | 0 |
| arbnode/mel/runner/extraction/abis.go | 1456 | `b67e47a42e570fd7b7180fd21fa4b05886e15648e4868d5f33e639b4598572fc` | 0 |
| arbnode/mel/runner/extraction/batch_lookup.go | 2757 | `77948962f5e5157385536a7308bc6e149cf8eca3ea7e6f4ea2de75d091a949cb` | 0 |
| arbnode/mel/runner/extraction/batch_serialization.go | 3708 | `e3cf18b747d88d6085a246713b9d446203a4440341320f57f39c532a13010517` | 0 |
| arbnode/mel/runner/extraction/delayed_message_lookup.go | 7977 | `7bc4e947cd5502156a5af31e4a444df6b5ace72d8442dc015fa827866c1cbfac` | 0 |
| arbnode/mel/runner/extraction/message_extraction_function.go | 9221 | `bb8d0355bcd3b1a36a8932b8b2e3cb558069e4288c0f165c300f47ea07e54121` | 0 |
| arbnode/mel/runner/extraction/messages_in_batch.go | 6937 | `b3d8ff39bf54fdc667bf880205424675d6e3d9cf67793aee890e95df4b32cc76` | 0 |
| arbnode/mel/runner/extraction/types.go | 2710 | `66b8b411294794ba0d6ea1f71a47490b76fbdf2f8c648bc2f90121a8a927c843` | 0 |
| arbnode/mel/runner/fsm.go | 2834 | `483f034d5186cc80e6315f664050869e35142f5f6d0612d3579dda68d2401c02` | 0 |
| arbnode/mel/runner/initialize.go | 1947 | `7e1ac36470738374e2bf03e6510f92fd9d528f0818b951de2691895b3b1f8613` | 0 |
| arbnode/mel/runner/legacy_db_reads.go | 9815 | `9f02efa9521d867446ede051f9a4309d493573be19c0d77221674240d4714e77` | 0 |
| arbnode/mel/runner/logs_and_headers_fetcher.go | 6848 | `b7c557925c920f8e60624a38fd3d19ebbfb1e0d65e8e7bfbb90acbf2da807218` | 0 |
| arbnode/mel/runner/mel.go | 24811 | `7886fd04235a68e68531057d5e22a7681b62983112fc434adc98b4aa29879eff` | 0 |
| arbnode/mel/runner/metrics.go | 1593 | `a8f5975572462f112ef55fc7542bf56bafe54c5f9785cb782a33ddb8b1737ade` | 0 |
| arbnode/mel/runner/process_next_block.go | 5374 | `b35fad063f1e49f7caf9adbf165c031e32ecf01ea99c55046d67cd49823d1631` | 0 |
| arbnode/mel/runner/recording/dap_reader_source.go | 3304 | `a29e02d47381167779a0d438ea569526c273a2955c8d75396d3da14557b62845` | 0 |
| arbnode/mel/runner/recording/receipt_recorder.go | 4350 | `116dbeb002ef72e4147fa57e23b1754acec6eba2e3165f5f503bdd44f55614b5` | 0 |
| arbnode/mel/runner/recording/tx_recorder.go | 4915 | `383c445858513ae4d32ef435fbb7334dbf4cceecac5313dd4d51ac401d597081` | 0 |
| arbnode/mel/runner/recording/txs_recording_database.go | 4160 | `e136ca66aef20c2bf3ff19c3f9aa59dc50de8d10db9ee73178c104cc511c36dd` | 0 |
| arbnode/mel/runner/reorg.go | 1086 | `6131f427576b5ba09c604661ec23247caa2fac58ebda7e3e9498bc10fec0cc24` | 0 |
| arbnode/mel/runner/save_messages.go | 1368 | `e36c929335f11ba70be46cb2024f679c726a8e3a01a1bf5a29a28a30e184fba1` | 0 |
| arbnode/mel/state.go | 18152 | `654593b5c965b47e59ced80b3b2e65653906d5bfe58620b1248f670e1bfd3a7a` | 0 |
| arbnode/message_pruner.go | 7968 | `4d663af1b8566c8e70f7aec6baf1405a18666eb59cfbe996b824618ef888a170` | 0 |
| arbnode/nitro-version-alerter/client.go | 5165 | `054e3191f71a81769af6c565c99affdd8b7138c6ee6a729dcae09d731ce0e0eb` | 0 |
| arbnode/nitro-version-alerter/server.go | 2216 | `52d8bc330c44bccdf1df76b068ed63714e44ce6688660cca3026064779af35bf` | 0 |
| arbnode/node.go | 81331 | `22f5a6126fd6dc84a0fb43b1605efec7ae8a69a02f34a889b46f58a3d8347c3a` | 0 |
| arbnode/parent/parent.go | 11959 | `8ce3626094090615fd64ccbf7ccb06c39e932f4ec5a9b7fd48534e8c97e6d9f3` | 0 |
| arbnode/redislock/redis.go | 7397 | `8ed558d9c654a8d12c6887f2370e7d85e63a4505b0c90f57d5f8c82f0f4178a6` | 0 |
| arbnode/resourcemanager/resource_management.go | 9414 | `52c37498d4c8444c833c90beae9dcf100e3d5f50499692d1a7e3262961d06cf2` | 0 |
| arbnode/schema.go | 1395 | `f4aa9f634c9ea5fdd9e856d6897fe6b3883843f4b6d6734e24820f3426940935` | 0 |
| arbnode/seq_coordinator.go | 44174 | `aedab5383e5376fe188dfdfbf6af0a0817595987624539b7be471815a3594362` | 0 |
| arbnode/sequencer_inbox.go | 7146 | `1ed19f8e1b14bd12ddc1529494ad01fd6701bfd895e34380f4afea8174861ce0` | 0 |
| arbnode/sync_monitor.go | 6304 | `fc49b20ed7437c2db44768c8208ff14c7fe1ecccb2bbf33d89504e8d04430260` | 0 |
| arbnode/transaction_streamer.go | 61618 | `fe3bba51daad9a74c10c239674ee1d220bf76b160c0a101790bfd08cbb0f0091` | 0 |
| arbos/addressSet/addressSet.go | 4733 | `64de5db4b3f9de60f4a6b8ce7919cbf6e4a679f20a095e42d22b9848c610d3d5` | 0 |
| arbos/addressTable/addressTable.go | 3441 | `b567eff3341b52ff4ea69e41960d60e6fddaa2bceceaa319211b55555c7bfb0f` | 0 |
| arbos/arbosState/arbosstate.go | 28493 | `d784755e8b24c799e374206f613f606f7a184d60df4040885ec2175dfd706faf` | 0 |
| arbos/arbosState/initialize.go | 8220 | `dee4381c0e13b55921a05658ff6e0bd0f2223d3559cd25ba6e23b7339f26416a` | 0 |
| arbos/arbostypes/incomingmessage.go | 13119 | `10ed476fcc6da061d49658f171013b21184a860378bbe6650e50cca248f9f9eb` | 0 |
| arbos/arbostypes/messagewithmeta.go | 1246 | `21f89d19c7b1660c5cb787f5cfbc5990c815befaee4ae588f26e7ed27702fb14` | 0 |
| arbos/block_processor.go | 33262 | `1a847ed646a64f8df933d44dcce75f7dd062890363927739395f077cd906ac34` | 0 |
| arbos/blockhash/blockhash.go | 2235 | `3c70cec4d47a9cd744152ad6c4dfc43536b698cd0170cf0bde66570e14432ec8` | 0 |
| arbos/burn/burn.go | 1888 | `2e09245863e18a643632871b126e11a6fda09652be10f83b985d95357938bc71` | 0 |
| arbos/engine.go | 2385 | `e7e8ef4f2a5fab9da01c6fedaeb059cdf57409d10a4fdf39d91bc17e2e4607ad` | 0 |
| arbos/extra_transaction_checks.go | 1506 | `3b5703060979d049396a9305e11cc65a34e43cf2176a8b542a6bbdc6fd27d5aa` | 0 |
| arbos/features/features.go | 1580 | `6cb8308a7e2efbca9a592f4c81595aa95cc5dbee6e04113d61e07e1e6ef84fd4` | 0 |
| arbos/filteredTransactions/state.go | 1674 | `f3abb1583c504d525208b529d243ddf06bfa5cc706236f9d73633d933e69deea` | 0 |
| arbos/internal_tx.go | 7313 | `c48800495c1d4fa564c10948ea753b66be9ef47baf2c592064eb2ae01b96110a` | 0 |
| arbos/l1pricing/batchPoster.go | 4655 | `9235317cbc58ca352d877687319ca64895b45ab8ee927601c80ea7ae87941d36` | 0 |
| arbos/l1pricing/l1PricingOldVersions.go | 11786 | `bedb965068040f79f2861621bf0216f2def12e673d9097716d10f3d97fef4765` | 0 |
| arbos/l1pricing/l1pricing.go | 20102 | `73dc5dc56215d3617c816884e76491bffce93bd93f1626fe2e886cea0e140dd6` | 0 |
| arbos/l2pricing/gas_constraint.go | 1873 | `b105dc65de2c732f6db7652f7aa0db3461d39f83fe3099b7572a2b45d922fd02` | 0 |
| arbos/l2pricing/l2pricing.go | 10152 | `3b59b6f6d5b2ada784819f0cc5b765c8d2cd805d73e0aeb0d571969a97cb1c12` | 0 |
| arbos/l2pricing/model.go | 13257 | `6d8959dd7f2ec8f532293ab8c4cdc8bf363234b6eb853a4c8d912eae239419af` | 0 |
| arbos/l2pricing/multi_gas_constraint.go | 5504 | `e78a48d45460a38d5f76fc6814cc524a0a00a4ea80bfa943ace9aa0d488d712c` | 0 |
| arbos/l2pricing/multi_gas_fees.go | 2328 | `bd3b07a68d4515aed647d1514b659cf4fbeccb46a3f63ec8794872cbe89e4e91` | 0 |
| arbos/merkleAccumulator/merkleAccumulator.go | 7272 | `d1b6f806059cb09473a2c31a7ae01fcc545200911726219aa09a18190cdf8557` | 0 |
| arbos/parse_l2.go | 13508 | `af23196d1e1c9f77e5aa098d1b71e8d9b9015dcf4e09048c31213e5cc6e84ee1` | 0 |
| arbos/programs/api.go | 17896 | `fbabb413388fb40666fe1cafc33ad0b1c224338974aebce1610a3d71896fa894` | 0 |
| arbos/programs/data_pricer.go | 3095 | `a38c52a53998a58d7bc8e5f7ac33bc387103691a54f16f702efa442d4c858406` | 0 |
| arbos/programs/memory.go | 2213 | `ef37b819f154af4e0c7ab90715108d7785a5c11fadfa7b7fffed9c8cd9133b04` | 0 |
| arbos/programs/native.go | 35809 | `82f9f86b2738eda5810dd3a64d08a82d1123453439d18f618282e431331848c3` | 0 |
| arbos/programs/native_api.go | 2512 | `f14409e0ab8a3290201b1ccc1d3de4059faae9ffa94f01337bedcf124b043cd9` | 0 |
| arbos/programs/node_config.go | 7224 | `5dd371e9d60436593a007f7dbbe85e861ca53c7bdebe94bc73cc04d27cf7436d` | 0 |
| arbos/programs/params.go | 9293 | `c748b57e1b30fa26c6e353a63b3d3072ddf4ca4d651c24b045be42b879c6434a` | 0 |
| arbos/programs/programs.go | 28679 | `eabecb9fd2c659a05be891583ff860d766a345ef5bad1b1ce50d0a93ff08c036` | 0 |
| arbos/programs/testcompile.go | 43747 | `f6aca325999ec9ecae9fd6fba7b5036d3606ba9e9485bb8d4076aab143a5bff6` | 0 |
| arbos/programs/testconstants.go | 3780 | `193297da5c45f5cc046707879d3d6714ffeeeeab738cd2e2d67398bbd33ad7b4` | 0 |
| arbos/programs/wasm.go | 7260 | `bd825835a1ec9fbe49d323c1cba3b3500b0cb6035a8ef9435d7b94af7f07e03d` | 0 |
| arbos/programs/wasm_api.go | 1881 | `a5c5aa104b0844c28678c04e06b09583b38a3d42410b5eaa4a0160d7cbbded9f` | 0 |
| arbos/programs/wasmstorehelper.go | 3989 | `560e718e6b66aa1b0312dc18fc808ff42e3bd91c7de29af931f07a095f49883b` | 0 |
| arbos/retryables/retryable.go | 12964 | `36beedf7fae0ab6b8d23b09bf6ae4623a962588a3bd4815183b6a39e5ce2b705` | 0 |
| arbos/storage/queue.go | 2835 | `d227c510f90302f064c5ab04ac65a39d4094433d6dccbd3f8390bdf4a996d8a4` | 0 |
| arbos/storage/storage.go | 24631 | `215365ed7a172c6d5057d4affe8c76f48515452b4e81c96aa80036e1a9865b85` | 0 |
| arbos/storage/vector.go | 2065 | `2924271cee8b3ff5cc71efaad63f3ed1db274d310276b0d7161fd2df499a8784` | 0 |
| arbos/tx_processor.go | 44828 | `0e9a8e2e56f348b4bbd86edeaaad1aaeb5a1fe419909a3d8ee51526eb99a1f6c` | 0 |
| arbos/util/storage_cache.go | 1969 | `d81d59b197bd4698df3723c6c645239dc0e47b17cc9e49eb3f0b91629c251fe4` | 0 |
| arbos/util/tracing.go | 14420 | `82c864cad06dc86dc015269e57a830648da0307e52f32ff520601bcbea754c40` | 0 |
| arbos/util/transfer.go | 3088 | `cb06f6410fcfb4b7f45e19a6834894d69c5d17bb4af4dc3c6322e505cdb76779` | 0 |
| arbos/util/util.go | 7887 | `3146c023a53925264531afb7738edabb2f9b6f4c3aebba11ebf35636d1ff896f` | 0 |
| arbstate/inbox.go | 16709 | `ce4fddc29f39d953d9bc4203ec1d3277ecf7ae3b38a2e28333b38910ca7fd719` | 0 |
| arbutil/block_message_relation.go | 561 | `9e605fd46111edfd09d84203f0cfdbf0e8332fd70be1e06592122d942e275216` | 0 |
| arbutil/correspondingl1blocknumber.go | 983 | `d5daa43167fb94c93a402047ce20fab1f93a1f94a97613ceeda8b2e05dcbfa58` | 0 |
| arbutil/finality_data.go | 322 | `95e67319f8278ee74e4bd55d3420c9ed55fa4f7d2575375e93f7cd11a1c32cab` | 0 |
| arbutil/format.go | 361 | `0a735177ad09b254f4949074bce0da137b3d46041b28b1a780fd1b0dbf2f0d41` | 0 |
| arbutil/hash.go | 836 | `79d6b3e0e47f7dcd9e1622521a08bbcfe9debe6eeee6c0b8ac1644591aeae960` | 0 |
| arbutil/preimage_type.go | 494 | `3a7eca9d075852911c7f4d81291819bff1c37f35759862b74bbb0315eed4c7e7` | 0 |
| arbutil/transaction_data.go | 1170 | `db509dc7f66fc0a4284c285b43dbfb532d891197d7f58fc6e9623eb487575489` | 0 |
| arbutil/unsafe.go | 664 | `d418b4aa29f7e89d62ab635b92315252dcfc62e002268069bfcb812daf473be1` | 0 |
| arbutil/wait_for_l1.go | 3291 | `da64ff39780bec5f0659ea1f777babcaa2fb89d3ab00384e028036ae5e8dbe27` | 0 |
| blocks_reexecutor/blocks_reexecutor.go | 16904 | `08fc5917e470982d6653f6d4cb78cbec14f4dfa3e90a63f0cad9312c18faf230` | 0 |
| blsSignatures/blsSignatures.go | 7714 | `494f60e368610e3b8216730cfe6889867814baf2dfddd5433ec53da15fca9a27` | 0 |
| bold/api/backend/backend.go | 8780 | `db83a622428e7ca81abdf5a2d58114e06663613f132b19e1b56a6e0ff1a8d6d7` | 0 |
| bold/api/db/db.go | 27505 | `0e54b5f4ed05570f74359a8c819e78845cacef5a88f32b7989f54d594a4f607c` | 0 |
| bold/api/db/schema.go | 4517 | `bb0035aab7610f465edf7362bd51803a0e0e82c97168a113d1a4bd5cff2df72b` | 0 |
| bold/api/server/methods.go | 20851 | `7889e420107a58c65f1c3772928d6de8a75b28963f35fd8e50c52745d63311e5` | 0 |
| bold/api/server/server.go | 2682 | `c35e0a21abbb1e56a023cdfb3841d146384c09449bdce357d64a4a4ec4675d14` | 0 |
| bold/api/types.go | 7215 | `34cc8f684a6cb522f10e6abc7f71ae465588c0b9d78d4d832b86d6b9aaaf4b9d` | 0 |
| bold/assertions/confirmation.go | 5597 | `8d787f3accf6a22e61d6295edc881c1e658d2d0db3d73d717c9aded438610258` | 0 |
| bold/assertions/manager.go | 14897 | `08b0f1c79be97f5e989f2ae4291e05c745c9e74b2170179b0827c8e6e92ce9ac` | 0 |
| bold/assertions/poster.go | 12278 | `99f8b26bd045c203bfd82ed9d855391ab133a03bffebe96bfe0d66bed19fc4f5` | 0 |
| bold/assertions/sync.go | 22256 | `46adebaa6a0253222822aac9e39c00b590b131c4b140bac08a2d3e68bf86d51c` | 0 |
| bold/challenge/chain/watcher.go | 35470 | `3bb222f042cbd2819536e8fe7d6042fe3138dd86860b5e23e8ee2f3b3508cd3e` | 0 |
| bold/challenge/challenges.go | 7193 | `585213e3bb7a502ad7e0b51d0a00503f13841292742b7890f34b468a387cc407` | 0 |
| bold/challenge/manager.go | 13447 | `2d5a52f228732a8e34bf4e1b5192b44a602195e7f28a3ee4e1e40eb38218b158` | 0 |
| bold/challenge/stack.go | 9270 | `3b3588ccb9479eba615408a71cd9c2c2f37bf7c8285bd6acbe3bfcf4764e0f3a` | 0 |
| bold/challenge/tracker/challenge_confirmation.go | 12593 | `956ce18f82ee71aac1949eca68a2b9759f663d7a5e1a28ea4a62e5abfb4cd3a7` | 0 |
| bold/challenge/tracker/fsm_states.go | 2614 | `7de316e82c7964d2168fbc4f3a0a4114d91b92ed2f88f5d15b48983b29721f55` | 0 |
| bold/challenge/tracker/tracker.go | 31060 | `c06940835ba5c8d227521a24e03613b91bb9e65537022e425ae69197be717e1a` | 0 |
| bold/challenge/tracker/transition_table.go | 1593 | `65614a78e7ea080076e12c928b1f114f00323cc771072db94f08b72d53d6b5f1` | 0 |
| bold/challenge/tree/add_edge.go | 8181 | `9e18fca9bd64a6c5c0a9ed28485d5e320e47f54cf673325001f4427544864033` | 0 |
| bold/challenge/tree/ancestors.go | 9902 | `24ba79c7e395cda336b4a22df205dfa11a2ccb1631abce1af9847043a2f67ff1` | 0 |
| bold/challenge/tree/local_timer.go | 4073 | `8a5b60bf1c89c4bdc222acbbfbebcad65da10524e9c0ed231eb3bcf4bbb6bd6d` | 0 |
| bold/challenge/tree/paths.go | 9624 | `8ce371b11e16f8db48ec5565995e880edd60aea29acb1fd73cbbe930e19369f9` | 0 |
| bold/challenge/tree/tree.go | 6790 | `ed65605f8a1b4591a79205415a8b0193f813a84ec5fdf31b93b6fa9a2d8c43e8` | 0 |
| bold/challenge/types/interfaces.go | 912 | `da3615d76b9a8108f44212a4eea549805fe77cefc0da144c9ea5ff22d785d753` | 0 |
| bold/challenge/types/mode.go | 1018 | `09a2212e58f5df10993aefa8a805a849f0c14616c429f45f37e82c2f973b751a` | 0 |
| bold/clock/time_reference.go | 3929 | `fa88450dd759892f850e91c5bea96e78a2faa76a6dc92c7644ae28354c0860de` | 0 |
| bold/commitment/history/history.go | 19516 | `61ac693f5b514694becb3d8d6fdbff7e3c357eca8dfb275ab0da15abf0cb227b` | 0 |
| bold/commitment/legacy/legacy.go | 2576 | `ee75f03d9f291d5a6cad4e1378fb92e3f34bd67de313e0795e75e30bdce5db00` | 0 |
| bold/commitment/proof/inclusion/inclusion.go | 3594 | `73db3ed5ac76d34c12ef3a41cbdaf23f2fc72dca9016a785de5f43c0d4943f35` | 0 |
| bold/commitment/proof/prefix/merkle.go | 1608 | `2a9ab15e20009b21a450c684acc4e6b671f597007070575961b9e1e9777a1c80` | 0 |
| bold/commitment/proof/prefix/prefix.go | 18580 | `bce7df74fc2eb59bb035ceb9aedbe048bf24bbb2319699bf6f03fdb92a09bd08` | 0 |
| bold/containers/events/producer.go | 4928 | `71fdc5b51e0ba60c4df9d2fbba5ce192973b62524f5734174f927b618f513490` | 0 |
| bold/containers/fsm/fsm.go | 5391 | `f21095d0009b2f637e1d5f829651f81096fc7976ed1d65587837c69d2f7ba981` | 0 |
| bold/containers/slice.go | 600 | `ae0287c463b8e86e34ab33b6d7ba4c527b593962a7cc9886eeae0c93b5715e0f` | 0 |
| bold/containers/threadsafe/lru_map.go | 1738 | `6eb6381318c0eb5ef5304a759e61b5c65c58261f72ab92309ab8a30e55ae2e0e` | 0 |
| bold/containers/threadsafe/lru_set.go | 1397 | `fee77ce4715d1f128e101841ca83cb5eec043a7f6e7e6feb9db6727a49ee6cf7` | 0 |
| bold/containers/threadsafe/map.go | 1774 | `754771e3f1b2a2d67cb0e7b223d210a2793e2ed6720599ad3ab2d00140dcd4e8` | 0 |
| bold/containers/threadsafe/set.go | 1248 | `248f1d452b6a7654f4936e72d2c63fc94092dbfa4ae6a3090aebdc3265593327` | 0 |
| bold/containers/threadsafe/slice.go | 1060 | `b3391847f48b8242a91ec94aeadcf0fcbea3bb59727071f6c82f26015672b321` | 0 |
| bold/protocol/execution_state.go | 3879 | `e70ac93100905f40d43e1d86e27c5ab133a6a792281491680b2e9a2994dd9e47` | 0 |
| bold/protocol/interfaces.go | 16116 | `3b02b002848e2066cefbd754b8fe93422bf67ad7f979e5796e7f18781ebd8af2` | 0 |
| bold/protocol/sol/assertion_chain.go | 40661 | `0623413835d2831f01df45b623af71d39dc5e960c6bc4c3e8b0483b8a1d8e362` | 0 |
| bold/protocol/sol/edge_challenge_manager.go | 37548 | `e60efe2038a3cad23955120e2680f8fda5629f36f817ca2555d749d305ba5f5d` | 0 |
| bold/protocol/sol/fast_confirm.go | 7158 | `df4528759dc679d0d32db9099f8ef0a44b97e0feda894a57c31698294b9bd706` | 0 |
| bold/protocol/sol/fifo_lock.go | 1467 | `8fd24104e5a41e6ccb8434a724d860218afced546b60391f114915d32afd655f` | 0 |
| bold/protocol/sol/metrics_contract_backend.go | 4109 | `bdb6e01c92c197b54de935dccb86764b82a5a1db32050eade87ecbf78212e8c1` | 0 |
| bold/protocol/sol/tracked_contract_backend.go | 3186 | `50473ad41198472424673d0a21568cc276274e6b9548f8b4c6c9119b1bbf0487` | 0 |
| bold/protocol/sol/transact.go | 6705 | `2dbf5a3ca277784458a62947976aa89304dabf07f762b86adb277144e037043f` | 0 |
| bold/protocol/sol/types.go | 5980 | `db206d3b1673c1093411c6f8882b98b89d855484271a8e3fde69f02c6a375512` | 0 |
| bold/retry/retry.go | 3058 | `6b0a3d0af97dae0586cb1b65a08caf2efd2f766753d33482545c8c07391afe79` | 0 |
| bold/state/history_commitment_provider.go | 25469 | `7d90482fbfb062c9dbe8c66efbd2f9d2b47b1edbffc79f6dcde3c503327229cd` | 0 |
| bold/state/provider.go | 5303 | `463803d53e1cf32ccc613ceed0d84681da52cc6fabbf6a38d7a015baa3920bf3` | 0 |
| broadcastclient/broadcastclient.go | 18715 | `37e7b4dc1cda1ac6a5801c33ccc0c930a05c65274923410ab91fcea5a73d4a38` | 0 |
| broadcastclients/broadcastclients.go | 11012 | `21ead69b966983b482338f9305ababad878e308e06ecfa101d0b0af0bd5961ee` | 0 |
| broadcaster/backlog/backlog.go | 15482 | `f084a8e5c84ad28d1c3c3da97f3f565e6753009971bc78c28519f7b2fc971142` | 0 |
| broadcaster/backlog/config.go | 927 | `101b3beee142f476d153ba56bd90e5db3d88ae6b343412842d2a0d87938729c4` | 0 |
| broadcaster/broadcaster.go | 3491 | `be1bcc14ece58a1488485980a4921b5f124b31c748113f178defe6b42f21890e` | 0 |
| broadcaster/message/message.go | 3602 | `9fffd1440cf13a9b514fbc50b8210b5044d7e72ec1aa3c3326860cb7fb153734` | 0 |
| broadcaster/message/message_test_utils.go | 1024 | `934d30020dceddf9ffe800a5a6cbdefd4f89878c8e32de1e2c34d810cfee42b2` | 0 |
| cmd/anytrustserver/main.go | 10641 | `e0a56f34389cd8a15392a674373852d5d7edfcc52ee04288262b975031cb9fbb` | 0 |
| cmd/anytrusttool/main.go | 10910 | `2c500ab7fe5f18bc47d4f9076908dd98c2b884174038e804147c5e931f4780d1` | 0 |
| cmd/autonomous-auctioneer/config.go | 5782 | `95a91eba1866fe43e8d0358ab2977add03141fbd14c78fa26055434868e748d7` | 0 |
| cmd/autonomous-auctioneer/main.go | 5375 | `8572c154e8d7a660718d1e0dcce55dc3a1511ba889cff2da8b9cc9ae6bc67f62` | 0 |
| cmd/bidder-client/main.go | 2360 | `0dee43508d938b0391268b371021cb638a0aee5a84d71563384b087b8a2018d9` | 0 |
| cmd/blobtool/blobtool.go | 3856 | `fd0638e8b9933cfba3a2ed1f9b44fef62a138ff35a8ed53aa4946ce2e15273ed` | 0 |
| cmd/chaininfo/chain_defaults.go | 7420 | `533484a452eaa0abee62556d2650dc1fa63320bdf245d264265ea2a798a0acb1` | 0 |
| cmd/chaininfo/chain_info.go | 5056 | `f0af2269dd6338cd4c7a31513749d9307fdcb7bc37088e479d5564fd2cb71554` | 0 |
| cmd/conf/chain.go | 2944 | `8cbef01990734e1f894e85cbe13615c76c373f24277bef78f25ff819cee43a53` | 0 |
| cmd/conf/database.go | 18947 | `9635471590296afae6c4b132e8f80be32c5b9349540266722692c08fb80016e3` | 0 |
| cmd/conf/init.go | 12327 | `be015a76f43cb959b7c4020649dcb9e84b1e0a4d17eed961aa2f302cc6d7cff6` | 0 |
| cmd/daprovider/daprovider.go | 11214 | `59777664dcef5579ebc4e26a0a60b0c043ea6f730683c1e59b34fb923c391c12` | 0 |
| cmd/dataavailability/data_availability_check.go | 10448 | `4ad0d5c77cba94f744704f87e1a0288d83ae44df8a2a7321d7977ecf8b67fa81` | 0 |
| cmd/dbconv/dbconv/config.go | 4322 | `17f626610a4e0c673eb72cf76047ece5fcdbb3d81f90a09dce49e849a007af4c` | 0 |
| cmd/dbconv/dbconv/dbconv.go | 4572 | `11fb9ba6f102d151313b5ba2f120b41988c81e865169aea72b3c312c4c574297` | 0 |
| cmd/dbconv/dbconv/stats.go | 1997 | `7e48c7fb150fdf67f8386406f6d29828b7a017e2df4258b9a8b6325b0ae7ead4` | 0 |
| cmd/dbconv/main.go | 3275 | `72040e959ef68201a1ac8199d8ecaa7e0e370be41dc1ff9b7d83117d95777ccf` | 0 |
| cmd/deploy/deploy.go | 8140 | `26c16298f5f8730e5ab13b598765e1cf38734d21c1e75568a85e1972e5e99a33` | 0 |
| cmd/el-proxy/api.go | 1664 | `f7f8bff9c0cc1124a311f694892524b23d42048273fbf996fd423d95aafd9cc8` | 0 |
| cmd/el-proxy/config.go | 6881 | `e7ea2c09b687bd2807c33f6927f2acb03849e1095455f04dd9d6a1e679521221` | 0 |
| cmd/el-proxy/main.go | 12806 | `8beb6d95fc2251a6f8635cccfc83acf65fa10a71860cd3fa9a95947e7dca5c59` | 0 |
| cmd/filtering-report/api/api.go | 2774 | `06f1de1b02736d4d1f08dae62fd9f1839bfba3575efb38a658ec920c942debf8` | 0 |
| cmd/filtering-report/api/api_testhelpers.go | 964 | `c8c712ae826ebac14970a02bdf077cca0e044ede40db0084c32f39ecef01523b` | 0 |
| cmd/filtering-report/api/report_current_filter_set_ids.go | 1274 | `4885882bc82c6748d9626351be92248cd4094e6494659038434f21175284c278` | 0 |
| cmd/filtering-report/api/report_filtered_transactions.go | 1910 | `b4bb4c99a21c6217bacb6d8dc8e88d4cf4975a45854fe4f0d74b7617b118ad0b` | 0 |
| cmd/filtering-report/forwarder/forwarder.go | 11252 | `41fc65d386392425444232731dc0d0b1c20c3fd859faf5a0a2840c45c9fbae02` | 0 |
| cmd/filtering-report/forwarder/forwarder_testhelpers.go | 2814 | `0da99b0f204e06d129fe9b91513d81ea09a2e6000299b8ccae262910a05b015b` | 0 |
| cmd/filtering-report/main.go | 8754 | `4d941eeb414aaf373fe49cadabcfb38fec8e115a069068b015aed2924b8d0f8b` | 0 |
| cmd/filtering-report/signer/pem.go | 2300 | `0a3fb3e63a105d826bb2186df3ca737080d1411a2a68b2cb28c191bb128e5bb8` | 0 |
| cmd/filtering-report/signer/signer.go | 4103 | `6096de80bed5f4b33a56a40b3417288a1a6f7e1eb8c87be15bb6f166f9449c78` | 0 |
| cmd/filtering-report/signer/signertest/pki.go | 4533 | `94707c55b629232109a47909c520097c18415f2d9d0a00d8a8ca73d3e301358b` | 0 |
| cmd/filtering-report/signer/signertest/verifier.go | 3768 | `d85f3df6159c1a6e0eb2048fae0dda10171534ab493e86b90e75902c6c765791` | 0 |
| cmd/genericconf/config.go | 6084 | `860446bfea8a93f68c6556dbbf2b6ebb21821fed24c41e2cf6faed722c24d64b` | 0 |
| cmd/genericconf/httpclient.go | 851 | `954c2a3744c508102c5aecedfa679e42e975c378bc8a9d8de17a8bd822296323` | 0 |
| cmd/genericconf/jwt.go | 1203 | `196a4e2e92dc6fab62923d7ddbb598ebccc5b2b8722540ed0559fb53e150717b` | 0 |
| cmd/genericconf/liveconfig.go | 2691 | `899a97e85d387fa1b6b4337fb54b04bf78cd0376dde39b0188f2ed8e7296ebd6` | 0 |
| cmd/genericconf/logging.go | 4597 | `55336876db60fb21ab73f380a530438d08129892cd0a10d23853ac1c8550f48c` | 0 |
| cmd/genericconf/loglevel.go | 894 | `28cef66239102b62b33066466475b5398d283d7b599e60eca556dd95af5dbd8f` | 0 |
| cmd/genericconf/pathresolver.go | 555 | `c95df7672b69820b85e393d0db44acb8286a9cc9d7581ec6698f5de2eff7217d` | 0 |
| cmd/genericconf/pprof.go | 841 | `3d388195c446e45b30b63b61e6c40f37ab5376f9460b6b3711f5fc4d0cfa3366` | 0 |
| cmd/genericconf/server.go | 8845 | `f5cbc2a6724c0237bbfb2ba1ae9bcc940435432cb8756e035d77ff0f697d4ce0` | 0 |
| cmd/genericconf/wallet.go | 1605 | `f598dfef36e469ae7cabb9369e51f52f59557543cd1c5b98900f31e3a34dbb4e` | 0 |
| cmd/genesis-generator/genesis-generator.go | 6079 | `39e352017f9ff25145d8b4e608ff2716a983aac9e1a60de6a881147a95d28a92` | 0 |
| cmd/l2pricing-simulator/config.go | 7067 | `e7411cc502bf3e8305632cace5849c8c9c9e5eb41588460dda5d844372828c1e` | 0 |
| cmd/l2pricing-simulator/gas.go | 1818 | `702fb6f4b736a27ad4044e3c3a551d8f75e626f2a5b55fb1a71f2dae3d888c65` | 0 |
| cmd/l2pricing-simulator/main.go | 5008 | `654ecd9be5d85077a805228294d13cb07525e4e13a00ef94be63c7374071b7a0` | 0 |
| cmd/l2pricing-simulator/multigas.go | 3746 | `d4149a484a31f4bc4cd3ef8268e438f033ef098a6f99d23f0219dc4a05d43f86` | 0 |
| cmd/l2pricing-simulator/output.go | 1862 | `327da9ca6ee0753f53bfd195089caca51d45f83d034df609d6c0adce7c95b94a` | 0 |
| cmd/mel-replay/main.go | 168 | `7ee84de2875aedfd78e9aaf3c816c74ba9595d40a123eef05051b80585bf2c0d` | 0 |
| cmd/mockexternalsigner/mockexternalsigner.go | 2626 | `be59f93f6773a4a7eb18550e844ed3b7d3152266f5b27966704e153a903822bf` | 0 |
| cmd/nitro/config/config.go | 21188 | `a9204c4f02a1d4f81120488438bd197092742e9b9395ef337f895635fb5d02b7` | 0 |
| cmd/nitro/init/init.go | 63006 | `59c2f6dc3ce147bbfc513dd0b2c5e451811f24051be7aafb45070b54e88b1df8` | 0 |
| cmd/nitro/nitro.go | 32496 | `a86ea4ebbd9580a37ae1235d3d5de1bd162deba8416ddeb9282b3fe6fb23c1f7` | 0 |
| cmd/nitro-val/config.go | 6267 | `0de32e69259a3f66d4076a3ad1819d06e3f58fcbc420bfca6d8c2b1ad9d7d19c` | 0 |
| cmd/nitro-val/nitro_val.go | 5494 | `8e4ee4297932e3e7ea1e42546e1a82582171db7e98f62fd34847ecf1b6117c99` | 0 |
| cmd/pruning/pruning.go | 10698 | `d8922319448a1090269a90c668b9e396ac945d0d5e6439667553375cb4e4d28d` | 0 |
| cmd/relay/relay.go | 2537 | `5ce3b5ffe80164f8dca9021cb7d9a31cd651b0c5a847141c5e5471926740cb0e` | 0 |
| cmd/replay/db.go | 2701 | `eea5817ed7f8e5e00d28394607f4f9510d66ae99ae868ca3790eb34589a3a279` | 0 |
| cmd/replay/main.go | 15048 | `b87cbac6189e1c61c1f338de7e4066231a1e7519ee7894799779931f382304ad` | 0 |
| cmd/replay/native.go | 202 | `a26a092e6c07884599acfe57fcb44113105eb1230217f26ac284e65e8e230695` | 0 |
| cmd/replay/wasm.go | 387 | `dbd591b1c5a3a1e17c12052aa0c99a021ed5dd83d4ae42d4c771a400738d6b93` | 0 |
| cmd/seq-coordinator-invalidate/seq-coordinator-invalidate.go | 1062 | `00b4e4ddd831eeb6909213ae4390f473f35a27ed93e72267c1eeb4c60a38de3a` | 0 |
| cmd/seq-coordinator-manager/rediscoordinator/redis_coordinator.go | 954 | `caf35b48a732105eed5a774b98433546ce8c58820db77281593dbac7780f7398` | 0 |
| cmd/seq-coordinator-manager/seq-coordinator-manager.go | 10011 | `3dbdc83494e3fcdd30b4d90a00fa8770f3a2c702dc233eb56e3d079e511cf701` | 0 |
| cmd/staterecovery/staterecovery.go | 3805 | `cfc9120b479ae0442aa2ec3a3e33182f8b46b401d17398ec4826d8422d5d01c0` | 0 |
| cmd/stylus-raw-deploycode/main.go | 2172 | `1528d155cf065ee20a1918dd5df5a1407fdfa79ffb35f61c0ec6a7c4d95a69bb` | 0 |
| cmd/transaction-filterer/api/api.go | 6032 | `df396192bb6db5c42e373d160b9579a12c1b6688718e814816f86e5ffef17ed3` | 0 |
| cmd/transaction-filterer/main.go | 7508 | `e578c22f5c20186a77069041b48d45fdde3966fdde1c6aac2497ee283645345d` | 0 |
| cmd/unified-replay/db.go | 2687 | `505a9db7eb93fcd350a75e53729b7d80700382b4ba539c8a7400e11fc04f8c2e` | 0 |
| cmd/unified-replay/main.go | 13597 | `dca8f124e89c64ef20f447a9bbfc7bda7a0d77a49e7dd2f2c6ad3eae38ef1254` | 0 |
| cmd/unified-replay/preimage_resolver.go | 1314 | `f544390cd927c58b4a4781318d905cf8a9250a637848451ed095e10018530aec` | 0 |
| cmd/util/confighelpers/configuration.go | 11086 | `0d4fa29865164907a0b6ad1b490bffdb11d2de2bfa013f1fd25121d055fd6672` | 0 |
| cmd/util/keystore.go | 4002 | `7645e538d65e36421735740b31bfe4ea54a8357b7244564dd8c39457fbff7df3` | 0 |
| cmd/util/metrics.go | 1243 | `c76e4f6d79c79728450c6437b6315335d2a885e0d8cad77dd25326cd0d620467` | 0 |
| cmd/util/util.go | 2287 | `d2fc162956f1957cffae744c6536498cabb55e2aa31a0430f31a69756e7219b1` | 0 |
| consensus/consensusrpcclient/client.go | 2426 | `ffb9a0b0dbce41de1b0cf5e944c30af36caf66575d0b4af4287cb3e5a9cfc010` | 0 |
| consensus/consensusrpcserver/server.go | 1103 | `7b19c9097f5b27c6a9fc228f7c777b3c0bf8919d79f23f3c4951c0fb4c7a7989` | 0 |
| consensus/interface.go | 919 | `aec2f6d74ddfa8e8672f0953393af4ae6d4d7a9ed391e16b85676a3bf271f2b7` | 0 |
| contracts-local/src/osp/ReferenceDAProofValidator.sol | 8303 | `5bac04a66a2dd19f7c252906d0d61a08570d4004fe34f805e083becbca0b6d82` | 0 |
| crates/arbutil/Cargo.toml | 656 | `1b80e8e6da3511496551f7c8ef771d2681a47c80a5e94a456175c10f283ab102` | 0 |
| crates/arbutil/src/benchmark.rs | 461 | `3b3e5de20ed028294bd523c6fc81b8da5be982cd4de42e8ddee63d294b76faaa` | 0 |
| crates/arbutil/src/color.rs | 3089 | `3577caabd940a79321ef92ff5d9e0c6dbbbdd3777c86d4c4a58a15a564657d0c` | 0 |
| crates/arbutil/src/crypto.rs | 2133 | `c3f8466ec4a351dc7e827977b79944a1fd48df711482b6526572b9f0cad6d4a6` | 0 |
| crates/arbutil/src/evm/api.rs | 9057 | `8ccfe2bb830836eb2123bd8baeeae576a6091a3bd961b0b87a81c46439def6b4` | 0 |
| crates/arbutil/src/evm/mod.rs | 2970 | `03ea9040321397bb5fc2e7e92dd95b18ea7897ffbd668d3ba3f1e3a610ad3834` | 0 |
| crates/arbutil/src/evm/req.rs | 10348 | `3603e644747fe776c77adf0d3cd3a11a1ba064c294161c406dbdfcc5b0e0aaf0` | 0 |
| crates/arbutil/src/evm/storage.rs | 6465 | `37fea66495ae2a329083f484dd1cacee7f4396512e8f4c19672035591b70550e` | 0 |
| crates/arbutil/src/evm/user.rs | 3670 | `44ae38325424c90702b3f9e938838e5d74438a5b3ab97b5172b56ef7d46c7765` | 0 |
| crates/arbutil/src/format.rs | 1733 | `1d8e295ce7fce169ebc74df3c0d35bd433702794ab0c3f9bef2e65e3fae6dd41` | 0 |
| crates/arbutil/src/lib.rs | 1705 | `be0351a610740db07478484b46b4dfadf93c0c1452e235412428837bb6984e49` | 0 |
| crates/arbutil/src/math.rs | 1053 | `aa20e9a086723e55afaa87a0b75b281efdbd6e1dc38f5ceba81585330df8e729` | 0 |
| crates/arbutil/src/operator.rs | 45774 | `e72aba3a296318df4ffd087212ac0f4acb942910bd1222887a18dac22a754ce7` | 0 |
| crates/arbutil/src/pricing.rs | 4242 | `32cc9bed10279674215e9974ceec0be42585e531f960aac4bd4300a955043bdf` | 0 |
| crates/arbutil/src/types.rs | 9620 | `f1dbb25fd8b5039e6cd26c5d1272c23420a8723001d93903bf602d05edfe7abc` | 0 |
| crates/brotli/Cargo.toml | 587 | `f93b759285cd3e5526a7beabfb2f61a440d9c7f986406c617ccaf0d8f2d9796d` | 0 |
| crates/brotli/build.rs | 3619 | `99399958a127541bc403c2546045f3353284ecd2338e0f9ddb91db6bec5f3bc2` | 0 |
| crates/brotli/src/cgo.rs | 2180 | `9146e6252b5cc319bd7e0a277d080672204eeb68ea963235fa4043ac20dada39` | 0 |
| crates/brotli/src/dicts/mod.rs | 3856 | `e90eeb6d4ddfe7ffbe3eb559d173d1154f76458d60528067e51ebd973b836cc8` | 0 |
| crates/brotli/src/host_imports.rs | 2791 | `fb176b4f77a0508ffdb2ce1c2ba80b4db2743268baae9c490edbad5ebb7fbe83` | 0 |
| crates/brotli/src/lib.rs | 606 | `bb0c1a63f331ef1619d40921c55f35acd0f24e5557df7021671d6160f437bd13` | 0 |
| crates/brotli/src/native.rs | 9516 | `fa023831db0958a38444236ba1abfe60420bd1fa55bd2a8b48472e5e54db940a` | 0 |
| crates/brotli/src/types.rs | 2493 | `24756e60992f774093d7a93cbe3a7edba1184e1b7537548abde45c03764510f2` | 0 |
| crates/brotli/src/wasmer_traits.rs | 790 | `0c0fdfb84855118a0767add1e557acbcbb484b29ed80195ac469c66ab82f4b7d` | 0 |
| crates/caller-env/Cargo.toml | 941 | `69277f34b9707d8eed4a43acea81e1b8d7235c74b64872312baf79e3a8600826` | 0 |
| crates/caller-env/src/arbcrypto.rs | 6215 | `f5677ed3e86ddb5290ce7718f6eb5532e9f89bf7ea9fe74a382561d47043c02d` | 0 |
| crates/caller-env/src/brotli.rs | 2138 | `61ec3886f819e838e97f2a870133c722ac40a07155dbf42faef8d79c42700be6` | 0 |
| crates/caller-env/src/guest_ptr.rs | 943 | `b58c1d3c03c81cf2482353caa74b4e9ea7aff024c4e4330a9aa82b6ae90d907e` | 0 |
| crates/caller-env/src/lib.rs | 3540 | `33e42282d08438935e70f76bbbadef32152988a79d74916b2814ae7868bdb895` | 0 |
| crates/caller-env/src/static_caller.rs | 3433 | `ad0ee95ff4328445ceadb5c5a88038a1b46c25dd8dde9807b979321d3e9d1611` | 0 |
| crates/caller-env/src/wasip1_stub.rs | 12441 | `4d117534c40ca4afa7f066c01be6cef80c9a85565270093e59d7fb17f11bd098` | 0 |
| crates/caller-env/src/wasmer_traits.rs | 2963 | `84f1564378292c09215ccb31bc90abb39d5522b7d37eba7e62359cc818d1de4a` | 0 |
| crates/caller-env/src/wavmio.rs | 9201 | `1838acacfcc973ea4c082bc4e6a4dbf48a82ffe18eab02255ff2ae7d658c1610` | 0 |
| crates/jit/.cargo/config.toml | 129 | `f5a62a708e5d60299d422e4ed3c42ef5c92967fbd75f015665702dfc7968039f` | 0 |
| crates/jit/Cargo.toml | 1069 | `21b1542523959aae6e5bff7b5d425407f7bb439a538d9096ada369dbe8b1f106` | 0 |
| crates/jit/programs/print/main.go | 554 | `0ae740468e770a3ad5d50c9bcae656ed0662399922ed42cb537167f81ee36dbd` | 0 |
| crates/jit/programs/time/main.go | 315 | `d90fcf8f7321d1566712a09f2831982cb9e01c61863aacf0e621a0667c65e4d0` | 0 |
| crates/jit/src/caller_env.rs | 1295 | `4d0e7661155e514e4378d6157b6f0db972369a0c6d7bacffad17be57f83002c5` | 0 |
| crates/jit/src/lib.rs | 6366 | `3fead9139de14f7cac7d13f6a04281a08775dad2b7c0eac3eb7533f6aaf561a5` | 0 |
| crates/jit/src/machine.rs | 15932 | `87b5ba62d395c3a4b6988387d37ab9530356e8e829d6688a5065c35f9657c0b7` | 0 |
| crates/jit/src/main.rs | 3808 | `f162b177f695574ef50c2151821d9c37e1bdef6fef77ba74bb32b8a7f6b61b31` | 0 |
| crates/jit/src/program.rs | 12702 | `1268899b445798ee421e8b237c05b92d9b74b5c76ca71377ccaa43e68693208a` | 0 |
| crates/jit/src/stylus_backend.rs | 5661 | `1f39c53db2dde16eb41f63c30780677f89b5ea65269394423f5bb17ae59be617` | 0 |
| crates/prover/Cargo.toml | 2193 | `7c37e8d1dc447d95bf66d7bd1d2bb084475314fadadddb99bd1258bdc14ff0f6` | 0 |
| crates/prover/build.rs | 444 | `62223efa20bbb31bada02d9357230ba2e85a1a81be53d1d45f499dc2a75f306a` | 0 |
| crates/prover/src/binary.rs | 32845 | `e0fdc7f94af2b838cd3352b5cc508c575800eea33d93e611977bb4b9c6d88129` | 0 |
| crates/prover/src/cbytes.rs | 3907 | `60925d0a715bd7633d5e7af3b3c7af95acff1457eb370b336bc146e23f43937c` | 0 |
| crates/prover/src/host.rs | 22155 | `ca6d8d426413358074367026dbb695d7697bec2970de61d18600644ac5c41f06` | 0 |
| crates/prover/src/internal_func.rs | 1759 | `a3fd6fc140460a614499575812e75c7a79660e66443963de5a1ad7b840fdfd7c` | 0 |
| crates/prover/src/kzg.rs | 3520 | `80b1288f44e38b9a8fc680f2de41c8c3727f599f337788ee08a79aa1bb17f116` | 0 |
| crates/prover/src/lib.rs | 653 | `376827cf8aa7bc9b8c9b86ad247dcb1457616f9040f1133ec593f3d8ffa883d8` | 0 |
| crates/prover/src/machine.rs | 143581 | `dd4d680215bcd1152e42541793bec39a2924b5ade57d61447bd89471b25de59d` | 0 |
| crates/prover/src/main.rs | 22541 | `d90bff0e6b25cc28b287728abab9669cf326d744623f23f9ae880a6327f90673` | 0 |
| crates/prover/src/memory.rs | 13702 | `dff2cdde109ece23f9c5fead402044f4a188e6a6cdd29f81f55f50519079cb24` | 0 |
| crates/prover/src/memory_type.rs | 879 | `d0f03f25fdd3e9ea5c2bd48d6f53fbdca5823c9ec1d8146e377e7d2920c12a33` | 0 |
| crates/prover/src/merkle/zerohashes.rs | 83102 | `28d4a2eb407a6b2500acaf990a923bfc67fbd7cb11c42f2d28a0a5ede12ecce4` | 0 |
| crates/prover/src/merkle.rs | 20903 | `617645dbc92b496508882e4c13b724530c8dc1fb323a6ba751263beaac5995c5` | 0 |
| crates/prover/src/prepare.rs | 2502 | `285614b51ec8e3f3e5a852e3d99fc4688ad40bdb4d78f29e747e18ed600ca34d` | 0 |
| crates/prover/src/print.rs | 10691 | `613706d9a37f3f270c5a231a7b30982d8da311e4149a9b165cdc9899358dd611` | 0 |
| crates/prover/src/programs/config.rs | 8102 | `f7473f57c760160781871829983f8501303f2b48a4524268c3f487c6aee937b4` | 0 |
| crates/prover/src/programs/counter.rs | 4658 | `22a7e2e909c756ac73fb733e04d356b00659ac23e9418665fe55774a6ce61cda` | 0 |
| crates/prover/src/programs/depth.rs | 24582 | `5b13a10ffba16aae17c95193a9d8d950e6f59d8be8e6830c4c42c604719986c6` | 0 |
| crates/prover/src/programs/dynamic.rs | 4340 | `0e2774f18e5f11aa1623cbab5fcbebf8b5b019b0dae779b498dbbb41837689b3` | 0 |
| crates/prover/src/programs/heap.rs | 3719 | `2a004bb6553ec5f195473aef67a8c8628dbf268c9256b1a3c8f0328509387f33` | 0 |
| crates/prover/src/programs/memory.rs | 4187 | `a5345d7acb7f89a09bf10a5fd6f7ea883ec25293c50c6457ac483a9ac0c0965c` | 0 |
| crates/prover/src/programs/meter.rs | 20899 | `3b354e5adc0942daef9a58d36c8e115f5346066b573c18167bae102c225008de` | 0 |
| crates/prover/src/programs/mod.rs | 22371 | `dc0ddb72bcd3da128d5b3338196427ce181034a2f0704128abe434261b696e10` | 0 |
| crates/prover/src/programs/prelude.rs | 392 | `5a952e2a5a9ad8c491d03957e2a9aa54e9c1db2711e7599d750cc466e7eed2b4` | 0 |
| crates/prover/src/programs/start.rs | 1790 | `6ea25220663e49a2ba447578c382c34151237193f07e2de832bcc4ddd61b0aca` | 0 |
| crates/prover/src/reinterpret.rs | 2395 | `930b4112cc7744cb5d2c22317634c07433da6bbf69b6de517ac7d52d2a234097` | 0 |
| crates/prover/src/utils.rs | 3775 | `2c8edb145290abc185c1c85dc85a682f3c59cbfefdd249478837891f69fb0186` | 0 |
| crates/prover/src/value.rs | 14471 | `11e92f7a249c7c8106b2a8b4423eb22a1cdc0ccbe9ccade998a52446bb322307` | 0 |
| crates/prover/src/wavm.rs | 59969 | `0362fe5d5621b22d659fe019a8b83e608628611a7d66eec2f4707146e2be8723` | 0 |
| crates/prover/src/wavm_serialize.rs | 34506 | `ec0bd177c1781402b597bba550d25cd56ba4ae80531d8bbd3ee049dc494c49e0` | 0 |
| crates/prover-ffi/Cargo.toml | 587 | `da08c0ddca313c57f679645f3414d16265738b18463fd8032e4ee705ea408797` | 0 |
| crates/prover-ffi/src/c_strings.rs | 1102 | `48010036aea4bccef73c12bdfeb29e2c0e9e963abd1dccb3733f6d848723dc4c` | 0 |
| crates/prover-ffi/src/lib.rs | 967 | `e11e12a56983df5e88f04fa6b0e81b26fa6cced20c809735e7fb48d84cfe0454` | 0 |
| crates/prover-ffi/src/machine.rs | 9497 | `3d1dd89a819122e22b320d50ec641d583bda92ad63d072585cae996243b7857f` | 0 |
| crates/prover-ffi/src/preimage.rs | 3100 | `b01e4ba81f0bc118d0221b2d7f04c68e2295ad598416a22184b3e064a73e2692` | 0 |
| crates/prover-ffi/src/types.rs | 1859 | `b1b31251b74b19e30cb84d90fea6b8224de93e7bfee90153064b1e007fa032af` | 0 |
| crates/sp1/Cargo.lock | 173737 | `15f38f8778f1e8987b12311d8a8a12fc8c5b062d0fa03fe4733ec17eb8bc3ec0` | 0 |
| crates/sp1/Cargo.toml | 1790 | `f9477646ac2d074b54286fdc2bc81647dcd161b21f9ce4340b0977e6948504f5` | 0 |
| crates/sp1/replay-builder/Cargo.toml | 839 | `c9ef0087c5f40b645ec752185d71410f116d3e3979ef15dcf65fdbdf6947a020` | 0 |
| crates/sp1/replay-builder/build.rs | 450 | `ae269e0422e3b861487127a1ca928211f10414a50c55f91a29a519d866f567e2` | 0 |
| crates/sp1/replay-builder/src/lib.rs | 8391 | `9522ff72a087a7045bdf050a2832783b9894dd9c276b443cde6725986f984305` | 0 |
| crates/sp1/replay-builder/src/main.rs | 4975 | `a681f978a3f56bc53b3ac49dda3a3c707dd97bd3a6285e963958660a4877a879` | 0 |
| crates/sp1/replay-io/Cargo.toml | 467 | `4c1f5f0fd12e025bb8fe80755015f0aaadbdce35b085eb23332190b75ff66ff1` | 0 |
| crates/sp1/replay-io/lib.rs | 2806 | `a5d4ace22e56ce9b47f360a7b83749f129d6aea2324ef3a2cb3659746ef63166` | 0 |
| crates/sp1/replay-program/Cargo.toml | 530 | `d72b2d04c24765358ba533f9e11800838caa188c7cd767c47712c2bc49a2786e` | 0 |
| crates/sp1/replay-program/src/main.rs | 846 | `84fba4b06b4c8aa8c742e0d963c289a1902953c9aac341d3ab0bdbbe0464f5a6` | 0 |
| crates/sp1/replay-runner/Cargo.toml | 793 | `7a18b3296a0a3792a3b8326d045ef6eaa9a01857f30f143115d18ded71187b02` | 0 |
| crates/sp1/replay-runner/main.rs | 4219 | `ba6687d62ada97791681f76b11520d3a01de7ee84f5e203ac7529a813156f7ca` | 0 |
| crates/sp1/stylus-compiler-program/Cargo.toml | 639 | `8013e046a54af5be9693534de2929aad59a1750113f5b0c33ffb68397d0542dc` | 0 |
| crates/sp1/stylus-compiler-program/src/lib.rs | 1573 | `a8ab3ad46946053101ccf1322882b9032a47ea4c436d4ec104a1c10b98c38645` | 0 |
| crates/sp1/stylus-compiler-program/src/main.rs | 708 | `8fd59b2ceccd11ee023d13bab4917935b2635858fb5f7ac901adc9336fe6fcec` | 0 |
| crates/sp1/stylus-compiler-runner/Cargo.toml | 619 | `e6476a3f4291a0820fdb0ed70245794e61dfb6edce7f7a9efbf8f736c0e19f2f` | 0 |
| crates/sp1/stylus-compiler-runner/build.rs | 364 | `ced5f85211d395c9ece285a0b1535551822c7467d94d508185693acdfaafc7d8` | 0 |
| crates/sp1/stylus-compiler-runner/main.rs | 4799 | `df38fb9c9dfd3555e1549a12715907c7cbafbc8dd9cf81b13ead5ff84bababc4` | 0 |
| crates/stylus/Cargo.toml | 1457 | `130174cffe3f04df934e3d55bf906cbe41b105ea4331895ebdc0764668801dad` | 0 |
| crates/stylus/src/benchmarks.rs | 3172 | `b54cfa3d6c072a0ad7955cc7f97c690e5eb27cfb39f0841f22125e2c62766480` | 0 |
| crates/stylus/src/cache.rs | 11041 | `8f743806514c969c8086baa64c7a52a63d4493ffbc9bdcd582d836176aa67bec` | 0 |
| crates/stylus/src/env.rs | 7147 | `cdd18a3ed29cbac63ad48c2102f3e355284bc4c1a4fd674237f4fec8a5564d02` | 0 |
| crates/stylus/src/evm_api.rs | 1399 | `229a45cd00ac326db5a07894a9b60237a5ba0e6c3f9cd579d95539f64a3b5565` | 0 |
| crates/stylus/src/host.rs | 12201 | `d70657b5f0dcc80112dd707e85cf69aa448e4ee4afbf55d5afe24c58a72c50ec` | 0 |
| crates/stylus/src/lib.rs | 13401 | `1acc08dae3762b21a95db7e8730e939384f3acfbdb26433d69b203342f4bee56` | 0 |
| crates/stylus/src/native.rs | 19637 | `3c6c6ebabe1bbb6f8cc6a6d1b43c0a4ab98bf550eca3a332ade535d8a9ac6b93` | 0 |
| crates/stylus/src/run.rs | 5308 | `3d3f18e86917cbeddef018736e9e11ac7cdb9e3778bc6beed9a8d66fd96be1f3` | 0 |
| crates/stylus/src/target_cache.rs | 3057 | `270c6e59fd46385787775ef6aded849f5b08e3ecc91857d289bfd81cd3ee9de6` | 0 |
| crates/tools/module_roots/Cargo.lock | 79438 | `a4e91f029cafb518db44630caffad1b29fcd2aee68538facbc817ed2129a235f` | 0 |
| crates/tools/module_roots/Cargo.toml | 237 | `17dae8218562a1660d32b855711c29db0ae661c183cceca4e112a08dbba1f154` | 0 |
| crates/tools/module_roots/src/main.rs | 2112 | `7b6ac5876ac9888abcacde008132c280e091b9a6f1511f561aa4c1d69993f587` | 0 |
| crates/validation/Cargo.toml | 713 | `c11126c278f1af122138e4dc01b9115f5ed381345cce630e59a27c560a82d14c` | 0 |
| crates/validation/src/lib.rs | 12556 | `aba057c378ed340b18284431f489a30986c44f27640a0443b5b5f22f27d3e0d9` | 0 |
| crates/validation/src/transfer/markers.rs | 299 | `a5727359971d3f617b1cf91f14ed93dc615f3a13f002ff98cfd5605fe765a914` | 0 |
| crates/validation/src/transfer/mod.rs | 312 | `d0a1a1c4e5576a710b49f4d68355ddb48457470a3f7a7d85d40546822b895998` | 0 |
| crates/validation/src/transfer/primitives.rs | 1380 | `d73d9b3509f1c8a2473a96d761e697e29864d7ab2a253f9e7bf838d4bcd838d1` | 0 |
| crates/validation/src/transfer/receiver.rs | 3690 | `6bfba374bb5f7460005d4be53d7a86c3860bb38dc1e2ed2b191cc722933ac3e3` | 0 |
| crates/validation/src/transfer/sender.rs | 2722 | `11df83b824cef4882dc177f8b955f2c0ae755a92ce1dc60f6bf912dc35582a42` | 0 |
| crates/validator/Cargo.toml | 1065 | `077f7ffbafe60fc79e8d722ba04867999a15e211f73c3c6ac93fb8d16d2427bc` | 0 |
| crates/validator/src/config.rs | 8229 | `0feff5285b346970b9acfa458f4bdc5b55fabf188e25118e262d1a85d62397c8` | 0 |
| crates/validator/src/engine/execution.rs | 3094 | `c1e7e3571efb719220e0226616a26b3a9e46970dbe926e7fda8133b92836ffb1` | 0 |
| crates/validator/src/engine/machine.rs | 9252 | `d6b2ad1ceeeb75b22cbdcaa9f9c5832e17c39ae4691bd6e52f1931e04c3275e4` | 0 |
| crates/validator/src/engine/machine_locator.rs | 11507 | `d675eb183d7fdbecf0e5fde3e7dd32490b808aaba7bac587a62409e16df218e5` | 0 |
| crates/validator/src/engine/mod.rs | 538 | `8f34b982f842ad887f67fb11eefd638ca4320becf3994dee0facc65474c12c1d` | 0 |
| crates/validator/src/jwt.rs | 3064 | `05d899b1b3bb1c744f1966df25b3c6268f54fd572195181f9bba2cbc2de0f0c7` | 0 |
| crates/validator/src/logging.rs | 976 | `4567f6411a07fbf9a4e915db775d8e33139a1a7146410298890d733ff1ccfd7d` | 0 |
| crates/validator/src/main.rs | 1313 | `c204f7403dcea1a6deca43cf0cbc214d06a5fdc6591cf28bd2e5cee5a43e345a` | 0 |
| crates/validator/src/server.rs | 7756 | `95ee6022813a3b0ed463c0a94af13a466e677791898db0b50c84bb44d0c9cc92` | 0 |
| crates/validator/src/spawner_endpoints.rs | 4102 | `5ead6296787ba9bda59213a91bfd42646f81a58acebab3a2447af9e5aefebbd9` | 0 |
| crates/wasm-libraries/.cargo/config.toml | 202 | `d4ae994928d8bc67bf76dea5d343c9ff257df2e783581de3ffe65f20cbecc5a0` | 0 |
| crates/wasm-libraries/arbcompress/Cargo.toml | 430 | `b58acb7b10b0a250d37b5cf16dd6361fe934e8df75c64a9231a345223468b3d7` | 0 |
| crates/wasm-libraries/arbcompress/build.rs | 452 | `f460e6ee62dabc6aa7f5ec9eb8f19658860c2814321f2e02d8d0e07690e93758` | 0 |
| crates/wasm-libraries/arbcompress/lib.rs | 1274 | `57ae8c4e562af2282921200958d5361cd0f356016d579588f1f5d95b60a4a517` | 0 |
| crates/wasm-libraries/arbcrypto/Cargo.toml | 358 | `5b24f3b487a4bd60134415f61f2774181765312711855527c04e50ce79000ef7` | 0 |
| crates/wasm-libraries/arbcrypto/lib.rs | 822 | `914330c09107341e6a1ec8f386c9ad9ab17b01471747a00a45018fe18cea1020` | 0 |
| crates/wasm-libraries/forward/Cargo.toml | 389 | `12da06d9be3eab1dfd11c41b66b9cc7457f40cd79e81b740997d603082372458` | 0 |
| crates/wasm-libraries/forward/bin.rs | 668 | `5409d901f9d8816a35f62364342c0abed21077d0c9d545006b6940984b06ab40` | 0 |
| crates/wasm-libraries/forward/lib.rs | 5638 | `01ca2cd6e82b8fb8f4c4cf58ebcc7d387378fdfc839155f8618b962879459a35` | 0 |
| crates/wasm-libraries/host-io/Cargo.toml | 387 | `044bc234332fe39e31c847e88d03facd91768c07dc5499c4b379664ba41327c5` | 0 |
| crates/wasm-libraries/host-io/lib.rs | 6369 | `76dc9b9d740b833f6a97e52e9ce70342ce52a57d27e9af44c470230a93905724` | 0 |
| crates/wasm-libraries/program-exec/Cargo.toml | 281 | `d7fd8d81c0a7aa961540c739b14631f4df69152f3632e0b6de7ac8c0e03e68cb` | 0 |
| crates/wasm-libraries/program-exec/lib.rs | 2107 | `5a4e1afc65f9e2ba0e5612202a073229c37e46d2170b8a12601b09f7295a8ee2` | 0 |
| crates/wasm-libraries/soft-float/bindings32.c | 8155 | `041e89bdb7583f217be7488075f3a681b91df65f4ab41be9b1c0554de19c06f9` | 0 |
| crates/wasm-libraries/soft-float/bindings64.c | 8488 | `bb9294aac27a7f184d540d920db4a72d8214b3054ec2a32e5a8f215ef89fe355` | 0 |
| crates/wasm-libraries/soft-float/canonicalize.h | 1254 | `0e52c7f58ac85453a708ee4c256c5c8565a9645e4d8434f30ca51f4818317a00` | 0 |
| crates/wasm-libraries/user-host/Cargo.toml | 560 | `fdf4f8cbff48e058e718525bf22bc832d981ae36a15bdc37c3ea6a37a67a107f` | 0 |
| crates/wasm-libraries/user-host/src/host.rs | 8053 | `bd8e4c46189ab51220861e1f045b927f29ab001b6f8f7ed28984687aef60a8f8` | 0 |
| crates/wasm-libraries/user-host/src/ink.rs | 1014 | `a65c9b7295f35a648f506eee42bcfb2034855f237db18faba212655871f93848` | 0 |
| crates/wasm-libraries/user-host/src/lib.rs | 180 | `56eed4cfa806a3a63ee40708071790b700010f926442e2d5129f6788cf3562ba` | 0 |
| crates/wasm-libraries/user-host/src/link.rs | 11538 | `c84a7224408896913b9cbbecedf7a95b17d984d38843aa05cdf5849a1a5bbca4` | 0 |
| crates/wasm-libraries/user-host/src/program.rs | 10241 | `f4a7e72811bf39eb9020e2871726f1da10a91f1bd874c45f7b1dd41739de88a9` | 0 |
| crates/wasm-libraries/user-host-trait/Cargo.toml | 429 | `4021c1dd36ce1ea8f61b8dab598d4f0f7c49c614d5c937bd1dfa2082397168dd` | 0 |
| crates/wasm-libraries/user-host-trait/lib.rs | 44801 | `cf99ce7c58f7ab09860a2df5a6c74de865847a4d36b3c075a0155506020d1df4` | 0 |
| crates/wasm-libraries/wasi-stub/Cargo.toml | 420 | `89576865d74fe3197916b12099fc2bb691271e4d227aa52aaf51686ae13d9cf3` | 0 |
| crates/wasm-libraries/wasi-stub/lib.rs | 3737 | `e3d374983c9a6822a1f844a25b3b533f878f8ef58720fb8da07b7cd47c372105` | 0 |
| crates/wasm-testsuite/Cargo.lock | 77096 | `9179bddfa76c5ce4a7166ceb2885a4349c5ef8d10c934745bd4726f0e8d34906` | 0 |
| crates/wasm-testsuite/Cargo.toml | 439 | `fe8eee8209d15700d7f611993b25099c234df28e4f22bf7d5e49aef3782dd2ba` | 0 |
| crates/wasm-testsuite/src/main.rs | 15034 | `87f00bd44d933343c05aa39a30068be010ce45c55521f2a7b2ed46950fd17c27` | 0 |
| daprovider/anytrust/aggregator.go | 11530 | `db3290ec505169ccd10137df528a731f83b555bfefa453939c16f157bdef3c2f` | 0 |
| daprovider/anytrust/cache_storage_service.go | 2754 | `ba7e20c2cc3e9b2be74626b9b95df8c736e258b1bd4c9a11ea9f141ddeb10c65` | 0 |
| daprovider/anytrust/config.go | 6435 | `3222848d6fca159f6bbcc62ec75d092f00d48a292136ed678a3d73b4330e78bd` | 0 |
| daprovider/anytrust/factory.go | 8725 | `a6d91fe77bc7415ef710ae323c676cbeea22dd66180f10202935c4442ba00969` | 0 |
| daprovider/anytrust/fallback_storage_service.go | 3761 | `6cb4a7f0f6ee15bc7fd143c1681c5cc7b815f1bb01583571cdba8b8e0cf10f24` | 0 |
| daprovider/anytrust/google_cloud_storage_service.go | 6747 | `439c1e4934f3d8c52e315cd59f50e1f03b97622fbcfb9d3dc6fdf981c71afed4` | 0 |
| daprovider/anytrust/key_utils.go | 3736 | `a7afba2fd063067f037ae582323d00fe6638f3960999f08198736d3b7fd951e1` | 0 |
| daprovider/anytrust/keyset_fetcher.go | 2726 | `cab6d2367a2de82283732b62e977b44c57969d5c26d7208c5f1e47ea9153e79b` | 0 |
| daprovider/anytrust/lifecycle.go | 774 | `eb3acc896c3b551cda5e77476666051b14f05b220e215e2ff174f7ddebe6ee0a` | 0 |
| daprovider/anytrust/local_file_storage_service.go | 24152 | `cc5118cfb7eacc3afb9d13f99c23d5b060ee395b71ec250df45956d52986b370` | 0 |
| daprovider/anytrust/memory_backed_storage_service.go | 2162 | `9f6acc1980ba862ace2f45c44d4f6e987290b248f48a3ed39fde019c4486196b` | 0 |
| daprovider/anytrust/panic_wrapper.go | 1650 | `241740ee571c5e4cc1561c19b65742bd671d7f6739974dd3c3fd7f028bbdb572` | 0 |
| daprovider/anytrust/provider_factory.go | 5324 | `db267c2c8442d596ff2fec189458c3ed37a1759e678033f8e037fb43a659edef` | 0 |
| daprovider/anytrust/read_limited.go | 2006 | `3026b14ae69901d4c9e64e240919b994a1974abb2216d26703a9bb42b595b15c` | 0 |
| daprovider/anytrust/reader_aggregator.go | 13996 | `8d84b6d7b7e53bfbaa814ff7f7730ed1110adc44427c68f8afb1a73d7f6f8bfd` | 0 |
| daprovider/anytrust/reader_aggregator_strategies.go | 3008 | `b83adcd8267e786a661b387f55032be9d43024b06be9ad06c0c1b9908464479d` | 0 |
| daprovider/anytrust/redis_storage_service.go | 4965 | `408bcbd8cee48df7b04ad06137dbb7a1efc272f1c5f570f33bb2e9f05035fd15` | 0 |
| daprovider/anytrust/redundant_storage_service.go | 4713 | `882dd8cc226c8e5e1a91ead9a22ece11151469470bf20213893438840d490def` | 0 |
| daprovider/anytrust/rest_server_list.go | 4583 | `b05839fbfd0ad9882bcc5e632735485425260c089bf93f5b9955cdc8136bb832` | 0 |
| daprovider/anytrust/restful_client.go | 3124 | `3757753f20986160c6a0d86696de48adf826498689d7f84298f1c3e1b004a5f2` | 0 |
| daprovider/anytrust/restful_server.go | 7421 | `0eed3513bc50551220c09de72af263690968d6d54ddc5e059a2fb10aecb01baf` | 0 |
| daprovider/anytrust/rpc_aggregator.go | 3550 | `7213bd5ba45c798ce06fefb55a0fe898f924520f23089ae2c33988f164e5f5c0` | 0 |
| daprovider/anytrust/rpc_client.go | 6952 | `fabf46c6766117ae9bfd92e14997307705653bb8352839ecc1a24f9ed2034b6c` | 0 |
| daprovider/anytrust/rpc_server.go | 8535 | `7f8607e9242f83d2074bbacae7ba997cf3a34899a5ccb06f29fe553ad41ca187` | 0 |
| daprovider/anytrust/s3_storage_service.go | 4264 | `c8e03e92e3bcf0ee1b1ffc642813d7d3ac8a7e693f27c9edbf51a74ffea4071e` | 0 |
| daprovider/anytrust/sign_after_store_writer.go | 4450 | `5f12c1d2078fa01bcb6037615690b596c5452fc9d6f0429e470aac0f28fbf13d` | 0 |
| daprovider/anytrust/signature_verifier.go | 2948 | `b75d813656874ccbb0aa487e88e8c9283a63044f42a4de5863c833ef409068d5` | 0 |
| daprovider/anytrust/storage_service.go | 1074 | `905f274374567289837dfbf31ca216c8db200d36e20a9d9b5a8aef8ff192c7a2` | 0 |
| daprovider/anytrust/store_signing.go | 1227 | `dab8d90140aca8811d13e601e531277377e181435f560a35e7305798d23c3382` | 0 |
| daprovider/anytrust/syncing_fallback_storage.go | 14516 | `7ec322a1dc4c094c59fbb228934547166fa0e874a8cf7b53e8061772284c86d6` | 0 |
| daprovider/anytrust/timeout_wrapper.go | 1108 | `bec5805dc9184652fc58b9fcf08dd7c514e53f96fb432303e36192fedd223345` | 0 |
| daprovider/anytrust/tree/tree.go | 7098 | `89411af233c7ac6d0a75b8766b63d17861a7608e80b1fc99e2b27679c8479409` | 0 |
| daprovider/anytrust/util/util.go | 17109 | `9079ef41a751097778f372ab3278bc74857a789410f7f34359eb081e107d000a` | 0 |
| daprovider/anytrust/util.go | 767 | `bd0a01db64bdde820a4222f0171e7e0dc9077879143973f82983b5a4e92c2d24` | 0 |
| daprovider/config/config.go | 931 | `4a17fe17443763cd7c7a673877cad0775f1a367a021036996862a1d4c9ecd511` | 0 |
| daprovider/daclient/daclient.go | 10913 | `528a949555ae825974728419eed4e3fd0936616b26f8999d2728d37a5eda5dcb` | 0 |
| daprovider/data_streaming/receiver.go | 10634 | `82225c67324efecfc0d39696bf3920c2788b01a48b8ced33b9a0e2ca131f605f` | 0 |
| daprovider/data_streaming/sender.go | 6554 | `cf81b07e263231deba35d0486778ae33edf62f48588d52bfcd690d8b7b09a9b8` | 0 |
| daprovider/data_streaming/signing.go | 2619 | `f2698099143ca6cc6e5b95901b73d2c75f0ab070312cb2ec7d8cc61c8292f7a6` | 0 |
| daprovider/reader.go | 8947 | `f7760c6334c76d6edf4a3f650abb8b407c5e779dea0c169288c3c18a688c8920` | 0 |
| daprovider/referenceda/certificate.go | 4041 | `a2b262f8838aa10db967a10cfbaf2e5d0f017c2895bf1e837ad1a730fe27dfb8` | 0 |
| daprovider/referenceda/config.go | 1559 | `a6a9ba56896702fcbfd689360a7ae01ac2c01fffe38e29916e42cf1c22390ac6` | 0 |
| daprovider/referenceda/provider_factory.go | 2953 | `0f6513fb1628009a2030543e1a5986c85399400f351134e095fe995b60f89ffc` | 0 |
| daprovider/referenceda/reference_reader.go | 5439 | `e681f15c2e92a21e6d674c345fc4447e94890117b169acebbf8c357ed0ae32fa` | 0 |
| daprovider/referenceda/reference_validator.go | 5609 | `1951ed1724bbb285ec60e79af04b3e25766ab6df5dc306250d81b2a892843f93` | 0 |
| daprovider/referenceda/reference_writer.go | 1800 | `e5f80dcdc2a0b71306721e6bc72b2c96149bd05618b8e72c1c4095af9ad90f0b` | 0 |
| daprovider/referenceda/storage.go | 1159 | `1f9df5807fc3292a7a6ab9619ef76af71c1e9e161136b5a83ac6ce1df73b7576` | 0 |
| daprovider/registry.go | 3279 | `e80df2dfc48061716ffa1eb3c863ee46bdba6b7153369793dc26302a7d17e001` | 0 |
| daprovider/server/provider_server.go | 9920 | `e8b7915ac5c600b1cae89789ec66a1c73625f8ccf21316ebd669d5f39a081c06` | 0 |
| daprovider/server_api/types.go | 1363 | `75a29f1a8af816fb08eb3684252d02f35dbeac6c0b6e486b249a0592bf3f8f66` | 0 |
| daprovider/util.go | 4739 | `f153c36c2eadb147536c23df27c91c9815470abfe0d95235f17f6842947e5ed7` | 0 |
| daprovider/validator.go | 1201 | `d572db85876380879e34348fd018590358103055f59de2f69f3c9548223200af` | 0 |
| daprovider/writer.go | 1962 | `1c61803bba8c678b9172db8988b398142fa140e07c9b06954c62d5a80f38dfe5` | 0 |
| deploy/deploy.go | 13707 | `47bc329a1630f545a7e468243313f8a7740eb92d2a34c867fd2f25762863148f` | 0 |
| execution/gethexec/addressfilter/address_checker.go | 3620 | `18b283c24d222ba062239945b330115b3b35d1ec6aa287ac3671aa1cd81d8822` | 0 |
| execution/gethexec/addressfilter/config.go | 5973 | `58c82ad13dd09106522324220619e513e29fee38e2893cf330cfbff686a44f31` | 0 |
| execution/gethexec/addressfilter/filter_report.go | 1490 | `2b70718cd5aca563a2929ff79f32c32e462c80b9f428eb790e964416808f8dc5` | 0 |
| execution/gethexec/addressfilter/hash_store.go | 8358 | `84a0afeaa9b70081426c58d5bdbce51729f9947631a5a7fa87829a0c7dd3e94d` | 0 |
| execution/gethexec/addressfilter/s3_sync.go | 9929 | `ab2427d8aa18dd37343c863fbe76479df61aa27066c0029337143517267884bb` | 0 |
| execution/gethexec/addressfilter/service.go | 6302 | `d53e38d5ad521f9c5b3b4468faeb9a852849ccd739a075bce5e9f4d0067c4263` | 0 |
| execution/gethexec/api.go | 15751 | `c499b2c444602aa40b205b346c038ba0b9d32f0d3b77359bff8d50f6fed27ee1` | 0 |
| execution/gethexec/arb_interface.go | 2061 | `2860f052a7d390c593d55ec7ecd33d6d38a5b375d6cbc36e3f62a62c1925ef08` | 0 |
| execution/gethexec/block_recorder.go | 13680 | `0a1443a0a4de444ff4640a2a3124dba5b307f0a128d26d110271d5c3978ec3ee` | 0 |
| execution/gethexec/block_records_freezer.go | 8761 | `572694c17fa7f7e3694bcb4f066d61868b6a60cfa78b34d7e8d91527e5863074` | 0 |
| execution/gethexec/block_sequencing_hooks.go | 2787 | `038bc40815e63c61320f95841400265abf6d434ede4d4466e44b4b0f588d53af` | 0 |
| execution/gethexec/blockchain.go | 16742 | `1b4e0cc46a4fb8ac77b45f22a932ae1f0505798003d2adee696aea274fd4490e` | 0 |
| execution/gethexec/blockmetadata.go | 5758 | `427421ccabbfe84d09f340a5b79647f3118f79f8ad3baba82656932c0eb742d1` | 0 |
| execution/gethexec/chain_tip_block_recorder.go | 7959 | `02e9060b0e54a76e89736dd635ab48e2467b4e59112c2315760e9692931bcd9a` | 0 |
| execution/gethexec/classicMessage.go | 3826 | `97fd881f29cf1fe813cf303f76add6d50df88a9461279d024f7af75efbae1805` | 0 |
| execution/gethexec/classicMessage_testhelpers.go | 2192 | `1c2be6ad5411909c5e96ebbabfe0c612e57e1d53e7200f7398e59428eb984a0f` | 0 |
| execution/gethexec/eventfilter/eventfilter.go | 7542 | `9aec39363b25bb4fafecb5dca1aa60882db2efaa5215fb0a48e0df3427e025f2` | 0 |
| execution/gethexec/executionengine.go | 63263 | `0ab9f9907f47b31827e85811febccf5d4fad061d9a4caddfa1a1c8a30b8fd7ae` | 0 |
| execution/gethexec/filtering_report_client.go | 4749 | `354c486902dab980990261f70f911ed7c86fe161727e73b7e792e792d346591b` | 0 |
| execution/gethexec/forwarder.go | 16469 | `301278aa39781041f66d7d4cea1965ee541a2f184ea20ef9145766c76afe8292` | 0 |
| execution/gethexec/full_sequencing_hooks.go | 7582 | `fdd1feedd2e997a84af22262171f89271c8122c92ccd2b952a794d014c40b2df` | 0 |
| execution/gethexec/node.go | 39100 | `7fceaaeee7eec3e7734782ccf7bc534bd7592a1b178736244d52f462de4e11d2` | 0 |
| execution/gethexec/nonce_failure_cache.go | 3522 | `799184db90fb6ef84997ff9e11a261089cde61c256fc60124d02e0ff4611ae50` | 0 |
| execution/gethexec/pga/heap.go | 3104 | `96d8db5241bb3cad5c260b4c20e143dec7ecd8ed2026ecf9552dba65e2338ef0` | 0 |
| execution/gethexec/pga/mempool.go | 4139 | `672f8a9a55ec9e72cafc4d2bcbb2e516d4ec067382f9561eb7c4e7c24ad2b5f4` | 0 |
| execution/gethexec/pga/schedule.go | 2551 | `f7b848763fa7d322b587ec8a595817f716d86caa897a2c0ef5eebfb785851941` | 0 |
| execution/gethexec/pga/tx.go | 2531 | `b84626861b4c2e927da15c240d8b414c48fd10611d3910beb7d653fc9fb5c9dc` | 0 |
| execution/gethexec/pga_adapter.go | 1192 | `4ed470369c172017747c728849b1ff1d9e657821c6d52da37b8927ad5f0332bb` | 0 |
| execution/gethexec/pga_tx_orderer.go | 7380 | `59d92a60bf54373bfd9415ecfeaa82c83b1b19ee53a282b8fb90686713611d64` | 0 |
| execution/gethexec/sequencer.go | 74131 | `af62829ffbbb1e79c387c91ee90e2b3cd0a182c12e9fd8c8bb39a57a70c0e467` | 0 |
| execution/gethexec/sequencing_state.go | 3445 | `811c8800aec0fe04d8efddb8bd4998515d7f3dd89e20795a26358a667179b2ef` | 0 |
| execution/gethexec/stylus_tracer.go | 5361 | `9ae3fa02d1c36ffce094638b79be51edc09bb76b59115cfc98550c9527ca0cef` | 0 |
| execution/gethexec/sync_monitor.go | 9824 | `e674bf8567c029b35d9d6718d1809908c0a9b41a587c6dce101acac5419b9e45` | 0 |
| execution/gethexec/transaction_filterer_client.go | 1731 | `74a470aec15a1a938846a4349c968c986e827d761350c5ef2a9b096b019bed69` | 0 |
| execution/gethexec/tx_filterer.go | 2868 | `df74ff6c975713b3d10b506a93dbd4d2f58c4223aa2f4166a56344acfadf9943` | 0 |
| execution/gethexec/tx_orderer.go | 5711 | `18fe6921e8a6d6c07cda6872be161471529d35aa31ccebe458c55f308c0da650` | 0 |
| execution/gethexec/tx_pre_checker.go | 13655 | `2205dab466e4ce8457dcc6763e8b63dc69412c897ca2e7eeb2ccb0944f59e03b` | 0 |
| execution/gethexec/wasmstorerebuilder.go | 6063 | `0d2abe549910b2f7763a101e31cde3ec3887497e7ead8cffbd8d33429535a9eb` | 0 |
| execution/interface.go | 11165 | `c2f0be025f0ed41cc053a9095f09b43722552abce668839efec59f44009dbf9a` | 0 |
| execution/nodeinterface/debug.go | 1645 | `6ecb35b02b963480aec9626c5c2886bb6815c93a9231daff63c915c29fc207a9` | 0 |
| execution/nodeinterface/node_interface.go | 21674 | `95d1112f677a9285e1884c032eec6172d00c268600871e8d63e0aa4c267f7439` | 0 |
| execution/nodeinterface/virtual_contracts.go | 6256 | `5c2017b4657b8a84d850b292c658e715937f571007a13133af2e68167de371ea` | 0 |
| execution/rpcclient/client.go | 4579 | `95facc7ab6a4a743ffcfbd657752a96d9a8b21db5e15a7b6362e5f65a6108fb4` | 0 |
| execution/rpcserver/server.go | 3477 | `0a808d33d767554ed2e32e3f2d3ebca87252a30775b67fac556976172e37659a` | 0 |
| execution_consensus/init.go | 1292 | `116fd58ea28305894d8364d1e70b0e1bc9fbf571b4c2e1610d872d16f70e2d05` | 0 |
| gethhook/geth-hook.go | 5974 | `2efe217e3c32e6407848149ec3e93450d6e114c798ce63543a3dc77cfbaa874d` | 0 |
| go.mod | 10227 | `52c9c08f0f13c2756e2082c46fab4d282bdc5e1f8678161a64528929043ec12e` | 0 |
| linters/deferinloop/deferinloop.go | 1956 | `c84e7e49cbc42b62573640c2a35be72e9a001dc78fdb1ca4c53deae1c151fddc` | 0 |
| linters/jsonneverempty/json_never_empty.go | 2534 | `5bec1ef868804fb3eb6076d0e63ddc695d474c4eaa5831a6b7de9744cd2198fc` | 0 |
| linters/koanf/handlers.go | 5912 | `8c818cc5794e428f65b53d37f1dc6761f3a76c707ec07be452a90f20bb53eda4` | 0 |
| linters/koanf/koanf.go | 2281 | `e342c55ed5f3f5d0e1232d199b25ede2bde85b684e9835adde4d0967d331fdeb` | 0 |
| linters/linters.go | 946 | `4b6affb1c1288765b2abbf9113ebef522902d3922ed996a3f9c202b6ed868b5d` | 0 |
| linters/logfmt/logfmt.go | 2685 | `dbea2bea1c63b478a94377a17595af523a6e343620261d216652e0f11d7dc1b0` | 0 |
| linters/namedfieldsinit/namedfieldsinit.go | 2227 | `1e0a76a7fc7ab623dff6bd8f0ce16d57acdf82a0101a8fe08e4fccda6aadfc95` | 0 |
| linters/pointercheck/pointercheck.go | 1915 | `f4bd09f15de15bb26f1ccf04ff45bb10561ec0c4c2584b93474ee1349f6bce66` | 0 |
| linters/prometheusmetrics/prometheusmetrics.go | 1909 | `47ee968438d508eed052f48e4d00e9ab722124964c28a11bc4c958862873f5de` | 0 |
| linters/rightshift/rightshift.go | 1570 | `9fdbe1ef241d108cbcdae567ed408953d884ef9fb883900bf2bbae3778b8a3d2` | 0 |
| linters/structinit/structinit.go | 4700 | `67313add6cd97205d59ba31e2f41379ae0acd7e2ce3968e4811089a9de93c186` | 0 |
| mel-replay/db.go | 3019 | `ff109c3351cdaa83df86e370fd5bd7c0521173ef197eb78c7c00b1b0298ebe37` | 0 |
| mel-replay/delayed_message_db.go | 3466 | `616d9b28f546c6c159937d0d35b385efc27969f3dfe0f37e75c6f59b87526526` | 0 |
| mel-replay/mel-replay.go | 1620 | `e04215bd442f811f5773702314f36a2c766483240b172f06aae73a22ad8e2ba6` | 0 |
| mel-replay/message_reader.go | 2532 | `be962fec06a01e9f255d1ae1b96ab6d30c2f4c7c5a905dcd88289b2f57b50c74` | 0 |
| mel-replay/receipt_fetcher.go | 4475 | `f4a4c38acc8ad86a7e6b5fdf4193d9c2b99a66d0d76de007543d6aea62caddcf` | 0 |
| mel-replay/trie_fetcher.go | 5004 | `3569712a3441dd091ce084a74b5621414665250862b6c4b9c821c2d33423c521` | 0 |
| mel-replay/tx_fetcher.go | 1034 | `ca6b93d32d6dcd0aebcaff3361692f53f57e8e24342400cfc2225a5b20bea36e` | 0 |
| melwavmio/higher.go | 2646 | `ead0c76799b7bd8b2e5145caea3c1369cb73d0f6e2e71cfac8020f3e47a99c9b` | 0 |
| melwavmio/raw.go | 838 | `45f33c6083b84729e369d4e31c49686bba6200a21154b170b14cfe794736f44e` | 0 |
| melwavmio/stub.go | 3025 | `a6d78e58523bde8a2ae8dc71759952b1b996d30bf488075e055d3bbf6a43abf7` | 0 |
| nitro-reth/.cargo/config.toml | 1775 | `b673642284f89fb97954b334f98b73a54dcb4854944c024294c9bf1bc5801f0d` | 0 |
| nitro-reth/Cargo.lock | 326629 | `22e260c9b83ffcef02e6155e12b6489eb389401e2cb61dddd9c11297638dccb9` | 0 |
| nitro-reth/Cargo.toml | 12860 | `4f02797fa0cfd78954897023ae2d0e7876be9a49f006b31ec72945bf0fe7d99a` | 0 |
| nitro-reth/bin/arb-mel-node/Cargo.toml | 879 | `be4ce186c05d4ddc8bd7106095f45b4530cc022e7b6c81e653e30086e019d8a5` | 0 |
| nitro-reth/bin/arb-mel-node/src/config.rs | 2508 | `0cdcc81c69f9d23c221bd9e745b774318c897d67cd36a2fe8904ce53f7984658` | 0 |
| nitro-reth/bin/arb-mel-node/src/consumer.rs | 787 | `ac6ddbad6cf4f81256fb5c81a6fdffdfe5b122a16f4c71dfc7dd16638a5e6cc4` | 0 |
| nitro-reth/bin/arb-mel-node/src/database.rs | 3099 | `1d04eafe9ef5c0993ce12679e91a2171609d4a69aa97ebf73be7dd61d632d39a` | 0 |
| nitro-reth/bin/arb-mel-node/src/main.rs | 795 | `5a589eb2b9deff28d72a06879c15ba62d250486e26dfc05f68991944e80f5005` | 0 |
| nitro-reth/bin/arb-mel-node/src/node.rs | 3828 | `f9bbe9dabc71295adad3f6a396cd60741c7345c2484732cd23742afb911c43d7` | 0 |
| nitro-reth/bin/arb-replay/Cargo.toml | 775 | `285e7f6b5ffaae20cf99fcf33e87389f52e36f24608b684262739de593ccc213` | 0 |
| nitro-reth/bin/arb-replay/src/main.rs | 958 | `27687000e16dd391aabf5827baa4267916d06a7eb47d8ea220d0c25422109d74` | 0 |
| nitro-reth/bin/arb-reth/Cargo.toml | 1144 | `3972ff9d981152455c12cd659b88193194d629bde6915181a04fab971fcba895` | 0 |
| nitro-reth/bin/arb-reth/src/commands/mod.rs | 87 | `ee0250cb99115b3396b871ea4c181fc92db129a5d79f0e164800a9b0b22cb423` | 0 |
| nitro-reth/bin/arb-reth/src/commands/re_execute.rs | 14091 | `dcc25afb368d8ef25ec57a81b1a7504623f32c8570c1bf97a709a3c9ba918df9` | 0 |
| nitro-reth/bin/arb-reth/src/commands/repair.rs | 4183 | `e0b7aa0d20b11008de8e96c50d6423660597ad8ec361f9984209b5e715b5f91c` | 0 |
| nitro-reth/bin/arb-reth/src/main.rs | 3098 | `b3b68d5788ca0e12a378bae446890981abcaa00b32eff01d99bb039004044c81` | 0 |
| nitro-reth/crates/arb-chainspec/Cargo.toml | 299 | `1ef304e3ef6cec89ba5503c037b5a3299b6f59abf7cc6f0e2c0be6e24165d6ac` | 0 |
| nitro-reth/crates/arb-chainspec/src/lib.rs | 5567 | `caf29ed9874e9ec3555d6812403c5e92cd246a7fd685663b17828bea67009d09` | 0 |
| nitro-reth/crates/arb-consensus/blob-client/Cargo.toml | 911 | `9d6253af8bce74f94fdb2546b3aef401ea64d865a218de273c473a59c1887dc6` | 0 |
| nitro-reth/crates/arb-consensus/blob-client/src/blobs.rs | 5532 | `ed35844f6bbba5bff0886644fdfa9d122b3675e8cfe7f9d8872dd2e9da0e9cc7` | 0 |
| nitro-reth/crates/arb-consensus/blob-client/src/da_reader.rs | 8484 | `9415ae69fba69e3f4398848961abcf08cbbe6a1797640589cc1096ef710b8276` | 0 |
| nitro-reth/crates/arb-consensus/blob-client/src/lib.rs | 3461 | `90127456dffb4fbc5177a2d48eb999a0c4da30998e992a2b6131970cadb05362` | 0 |
| nitro-reth/crates/arb-consensus/blob-client/src/mock.rs | 3780 | `90fe5ce4b4e737dfaa5a60d34f446236874ba12bd887019bc2cd81f59355d4c9` | 0 |
| nitro-reth/crates/arb-consensus/blob-client/src/rpc/config.rs | 748 | `402f92d5ac3fdb32e4463e99b89e7890d55908535dc5ba5adc902b4219d6adeb` | 0 |
| nitro-reth/crates/arb-consensus/blob-client/src/rpc/kzg.rs | 1545 | `b31ddc19b547165d2fff74713fc2ba9e838779f00e9a43653cd835a7c73a710e` | 0 |
| nitro-reth/crates/arb-consensus/blob-client/src/rpc/mod.rs | 11958 | `ea5e840f3c315101d02b29263af7bd0446ce93289ac564fb8fadf94500e6d885` | 0 |
| nitro-reth/crates/arb-consensus/da-provider/Cargo.toml | 340 | `b1ec587b8091df99925e6b6357706ddff677262d1f951089b19f32778d11b782` | 0 |
| nitro-reth/crates/arb-consensus/da-provider/rpc-client/Cargo.toml | 476 | `ce955b8580d0795707379220d0c4b5a6c61d5bba5f2acd2e07de114a831edf3f` | 0 |
| nitro-reth/crates/arb-consensus/da-provider/rpc-client/src/lib.rs | 11287 | `b7f46688db78ae3c8085fd623877ea7a27608528c4c9e0b1174ecc9fe23f2954` | 0 |
| nitro-reth/crates/arb-consensus/da-provider/src/lib.rs | 4404 | `2b18439b726dc527e0feb754f28cb0f463628a0a409396580f4387983a188976` | 0 |
| nitro-reth/crates/arb-consensus/da-provider/src/mock.rs | 10365 | `4d3d3b187e158ce3d046663c772754d93d32aaec31c8c60ed480d09f16ec1d99` | 0 |
| nitro-reth/crates/arb-consensus/da-provider/src/registry.rs | 4388 | `dfc3a715ed3826321a4b02efdd53be22c54807812623920d7b50d845db187ea3` | 0 |
| nitro-reth/crates/arb-consensus/db/Cargo.toml | 553 | `4a65a8ba75aae8cc44f4c9bfe833647378f31ee1d11764d67b39abce682f390a` | 0 |
| nitro-reth/crates/arb-consensus/db/src/codecs/mod.rs | 1393 | `7926cbc5f1bf59fd26a01d8d7923dca973a39c5f678b8da7de42be9bdba1869b` | 0 |
| nitro-reth/crates/arb-consensus/db/src/codecs/rlp.rs | 516 | `c8037c9db31340d90031198bda31bf1cca2812a4138894a1aa9075c15bb121a0` | 0 |
| nitro-reth/crates/arb-consensus/db/src/kv/libmdbx.rs | 8540 | `e433ad64a379059a26b37787f77a223430c86126c2b478efbf407a39f5a42be1` | 0 |
| nitro-reth/crates/arb-consensus/db/src/kv/memory.rs | 5145 | `efbc595097e7cdb06aaf808f131c00007a1df2e2c94a15140377ee0e092561e9` | 0 |
| nitro-reth/crates/arb-consensus/db/src/kv/mod.rs | 2735 | `29f515084b5a336f17b651408453d7a39d90c8acc07c79eb371b1b75b4d12824` | 0 |
| nitro-reth/crates/arb-consensus/db/src/lib.rs | 12312 | `e7bb1b3ddb9c298017683c482d5ae4eb1d55cccee5aeb37779b7cd3072a76f42` | 0 |
| nitro-reth/crates/arb-consensus/db/src/schema.rs | 18741 | `752b35149f3a617a96d5a00771c25b05cbecb0dad0d2a0f4a78546c4f6474a9b` | 0 |
| nitro-reth/crates/arb-consensus/mel/Cargo.toml | 994 | `c40e52531629aad68f43e21926df73e74e90d772bfea752ad73ac6c1551ebfa1` | 0 |
| nitro-reth/crates/arb-consensus/mel/db/Cargo.toml | 415 | `8c6af6bbcc84e6d268a1873a21ad5716d661e3ac939af9493dbd9bc7a4985801` | 0 |
| nitro-reth/crates/arb-consensus/mel/db/src/lib.rs | 28685 | `ab1184b2972f08bb30e7624063073524afd051b2efa5a24ee20e16fe5d046115` | 0 |
| nitro-reth/crates/arb-consensus/mel/db/src/schema.rs | 4640 | `8e51b13d05e449b16c682e1d864aa0324bec4a8f832a22f50b74ca3fd6a30af7` | 0 |
| nitro-reth/crates/arb-consensus/mel/runner/Cargo.toml | 1062 | `a371ed2558d4f8318ebd4925b0a0319c3bce749b6d15243442c9b41f86b5dcc3` | 0 |
| nitro-reth/crates/arb-consensus/mel/runner/src/config.rs | 5310 | `dcfd61218337450091e2370bd535bc9c40895ecdd9a85af320ec91b20c0fde29` | 0 |
| nitro-reth/crates/arb-consensus/mel/runner/src/consumer.rs | 3971 | `2b40fe44440e52b11e08778c4f04d46d9b9db2e99f9d908c514e7513e8edc3b5` | 0 |
| nitro-reth/crates/arb-consensus/mel/runner/src/database.rs | 8218 | `1c1a0c0162b3bdd324b7425715cef33faa68ea0adea095392130997856510e73` | 0 |
| nitro-reth/crates/arb-consensus/mel/runner/src/extractor.rs | 22774 | `affc0ff5dc212564331b7d4ebcb289cdee60f27d9fc8b0aaef44da1d3ca1ffea` | 0 |
| nitro-reth/crates/arb-consensus/mel/runner/src/fsm/initialize.rs | 2076 | `69adbc7256e5519835d39be089082d667b1da4e5cc825a05a94511fb206b1f30` | 0 |
| nitro-reth/crates/arb-consensus/mel/runner/src/fsm/mod.rs | 5597 | `48acb14cf5f27a9088e01544f992090ddc08d1b02d41702520f2bf71f7320469` | 0 |
| nitro-reth/crates/arb-consensus/mel/runner/src/fsm/process_next_block.rs | 9827 | `eb94c1d5c98853e4c03ee8a93a6482fb007f43803680df1181c8df1797593960` | 0 |
| nitro-reth/crates/arb-consensus/mel/runner/src/fsm/reorg.rs | 1655 | `89742bc55d0217787d3f10e56d799e04fcd73a440e3b6026c8591a728971e808` | 0 |
| nitro-reth/crates/arb-consensus/mel/runner/src/fsm/save_messages.rs | 2563 | `9016a13ed00915b524ac373e9de21bdf04ab424f59cab9eec691631a4c0a0e9c` | 0 |
| nitro-reth/crates/arb-consensus/mel/runner/src/lib.rs | 3080 | `06fdfb939852e612cc3660a7eddb8171d1a8de4da53b32432cb117a851fe2e4f` | 0 |
| nitro-reth/crates/arb-consensus/mel/runner/src/logs_and_headers_fetcher.rs | 19294 | `37c39fa3f25d0373e8699dd3eb92e12391765009fc9646fead48d7f3d829b5fa` | 0 |
| nitro-reth/crates/arb-consensus/mel/runner/src/types.rs | 801 | `c6253b633d02855b698012021fb5adfb43447c46d60b44c2e76fa81ac9eafe9f` | 0 |
| nitro-reth/crates/arb-consensus/mel/src/batch_lookup.rs | 8983 | `fc9bbabe04e985c134e2ff5579e0e568fcc434816173912ce445c87050e578e4` | 0 |
| nitro-reth/crates/arb-consensus/mel/src/batch_messages.rs | 14584 | `7e59cfa5499e584d0cb4488c41996fc804a95265824a92169bd8de373048d902` | 0 |
| nitro-reth/crates/arb-consensus/mel/src/delayed_message_lookup.rs | 16711 | `cb3145d044713de6dad2a0a72cd9171fe38489faf0b3d43296ae7ff375273ca0` | 0 |
| nitro-reth/crates/arb-consensus/mel/src/error.rs | 3614 | `c9f8159ebf8c6b1fc776aa14f636f8c5e92357b123d55d0632ac0962b9c7541b` | 0 |
| nitro-reth/crates/arb-consensus/mel/src/lib.rs | 1726 | `6fcb0ee0f410e79b289f50fd102389501c9ac4ad2c1f1a7d77f837615e61120f` | 0 |
| nitro-reth/crates/arb-consensus/mel/src/mel_config_lookup.rs | 4298 | `5ccc467ac9010da021469a4aba3ba9b32d5a2a35f1dfda8f1378b7537c9b3aee` | 0 |
| nitro-reth/crates/arb-consensus/mel/src/message_extraction.rs | 20054 | `88b76b1dc85522bf06ca5d2c187d39377e59a2aa2ec1184a327b696a1cdef4a9` | 0 |
| nitro-reth/crates/arb-consensus/mel/src/parse_sequencer_message.rs | 15929 | `42d0d12642f7d5e319d5ec2dafca3f9be53d2b22b0b3379a6304cf72578a5763` | 0 |
| nitro-reth/crates/arb-consensus/mel/src/serialize_batch.rs | 12500 | `45324dc59599658b0b438e345e9ece95e0bcfbc091341f2ca593cd004a5ce6d6` | 0 |
| nitro-reth/crates/arb-consensus/mel/src/state.rs | 2298 | `4c8fb9c0a3507097efdd75ef4ca7e00c4d9187a2ab72f31e2f3d7d1df9663be6` | 0 |
| nitro-reth/crates/arb-consensus/mel/src/types.rs | 2962 | `ae3371bb39da7d4a7461ecf09b1814a38833d50f1800b1c48d536d50707f70b7` | 0 |
| nitro-reth/crates/arb-consensus/mel/types/Cargo.toml | 500 | `537593412aa2e0f5cd07f6a550e136937bbe5729eb55bcc0b5f8a610b7739d35` | 0 |
| nitro-reth/crates/arb-consensus/mel/types/src/lib.rs | 7577 | `c16f1b381693284bd842e01b8d76c3713cf04378416ef5fdfe5a348c4bf27fa2` | 0 |
| nitro-reth/crates/arb-consensus/parent-chain-client/Cargo.toml | 836 | `cd808984e6dea29a522e39e26c87f4508c8ce9701870a7720b2a0d07b362aff0` | 0 |
| nitro-reth/crates/arb-consensus/parent-chain-client/src/lib.rs | 2988 | `2348baa7c97c8c92fe1aca27fa8f964951151242abe5bbd631459897227daef0` | 0 |
| nitro-reth/crates/arb-consensus/parent-chain-client/src/mock.rs | 17459 | `7b6cf5988bfa5df668afc4e50b41aacb60280ffc9de19964062227b06d500b94` | 0 |
| nitro-reth/crates/arb-consensus/parent-chain-client/src/rpc.rs | 7762 | `f9fa20dc00dfce740637b28e418cef40df593494b28046d86357464dc3354119` | 0 |
| nitro-reth/crates/arb-context/Cargo.toml | 451 | `f46138620aa8523eda8fb6411180ac1deb616eeb1b93c65ebfdfbc30ce874879` | 0 |
| nitro-reth/crates/arb-context/src/lib.rs | 17144 | `6a9c274c1697c4ac23f9de5b2346ae1d0c65129961e39ea8f1691572b212cc00` | 0 |
| nitro-reth/crates/arb-errors/Cargo.toml | 385 | `0326ae04de0ec92a2cc4c9944b1df5ad0dbfe8cf575c173c08190bdcbd584dc8` | 0 |
| nitro-reth/crates/arb-errors/src/error.rs | 592 | `d0b5066fcd2603ef229de428df0f6c4cf8e89b0660907799d513dafb3a54bae0` | 0 |
| nitro-reth/crates/arb-errors/src/lib.rs | 591 | `4d13fdef6f27a7792180b71da2da8174215c456fe7312c2d9bb173bcaef153b4` | 0 |
| nitro-reth/crates/arb-evm/Cargo.toml | 1637 | `45e262607730c764d7bf658840bb140523461d2803c69eae3f757a63b52c8446` | 0 |
| nitro-reth/crates/arb-evm/src/assembler.rs | 6922 | `65fd9078cca64023a2bed6bd124f421a73586ab7c2be36900a196fd568d3dcdb` | 0 |
| nitro-reth/crates/arb-evm/src/block_producer.rs | 7602 | `34ee1f455b973ec6a90a6b5d461121cbea77e93715f8f556e8f2352842b81254` | 0 |
| nitro-reth/crates/arb-evm/src/build.rs | 158781 | `d311f60fd4c55777644d554370cd453b21ad0ec9be77e2a979a668019e51e15d` | 0 |
| nitro-reth/crates/arb-evm/src/config.rs | 19225 | `5d6d84f80407cd91f8a53ad8920eb965e141fe216622389022ae4575522f7541` | 0 |
| nitro-reth/crates/arb-evm/src/context.rs | 9839 | `fceb9534da7b9d5d86d81ed0a10d2f6b5c9f8d0376542e58a82e1e758ab67415` | 0 |
| nitro-reth/crates/arb-evm/src/evm.rs | 90347 | `b60672538d3ffd157edc308be622ca9f9e82260b54691ae294c8b0071b612c3e` | 0 |
| nitro-reth/crates/arb-evm/src/executor.rs | 6043 | `97d1d884ebbe6c891da0b533ef2f550d755fee5c34734143983a0508375c39ca` | 0 |
| nitro-reth/crates/arb-evm/src/hooks.rs | 4215 | `b3bae42188cfb089b47693600b205e6ab766f9b8e696249b3c2c447c8046f617` | 0 |
| nitro-reth/crates/arb-evm/src/lib.rs | 958 | `23ceb6d4e77c2ece712b4ce8b522718a3715e454acf1748e7713027e1ae4c36f` | 0 |
| nitro-reth/crates/arb-evm/src/multi_gas/classify.rs | 11405 | `e490a494288a5aee34375c769a886fc355bbd064389e78bd123883c98a95b1be` | 0 |
| nitro-reth/crates/arb-evm/src/multi_gas/inspector.rs | 15599 | `afe61d558b4505e90deeb87ae8902772b044203962d59efb8362384b9b352f6d` | 0 |
| nitro-reth/crates/arb-evm/src/multi_gas/intrinsic.rs | 3775 | `ed174045524d340698d4ec4eb3f0240b7ad60c0b3057e78357de43cd86020492` | 0 |
| nitro-reth/crates/arb-evm/src/multi_gas/mod.rs | 418 | `280cdec8ee2192e5803000ed0daaed3a1930d9ca0284fcbde6feff391247dcae` | 0 |
| nitro-reth/crates/arb-evm/src/receipt.rs | 2015 | `7adddc7c341c285c6974d3dc9a5bc3ac517b3530f5bef0f06c917e262e899308` | 0 |
| nitro-reth/crates/arb-evm/src/state_overlay.rs | 19525 | `2ef052060cf3b7811d99cc773c4602e648649d15740216de7be70318b27790a7` | 0 |
| nitro-reth/crates/arb-evm/src/transaction.rs | 8306 | `4e0e3556b9d069830f8061c247ede9eac53561bcdf78c612b6e91a393212d4d0` | 0 |
| nitro-reth/crates/arb-math/Cargo.toml | 251 | `672f4471e8eee0d9bb96ceb5191b72b7e020f232f4b78b2694e7b50892d373bc` | 0 |
| nitro-reth/crates/arb-math/src/lib.rs | 3864 | `761f65769e3896eac80dd73adaece85cb72f3e9f6bd7af650e7d3f6b56db06ba` | 0 |
| nitro-reth/crates/arb-node/Cargo.toml | 3321 | `691d0eae0293001a9ceb74f0bfa9810bd1c593d62a32a91b2f9f4e6b9c26bfbf` | 0 |
| nitro-reth/crates/arb-node/src/addons.rs | 884 | `bcd0202a20fac7b17a7f73f9477ad8044e4e182ac550271eb3fa5475aa8b2ea4` | 0 |
| nitro-reth/crates/arb-node/src/args.rs | 286 | `345a5c21d75151f51b26d36225fbb9022d3f12e9e2ae304e889a4084ee9cbb1c` | 0 |
| nitro-reth/crates/arb-node/src/chainspec.rs | 29246 | `e8aa30bc412729e9aa268f58d45f0adaaac166a87f695a4637a0c63a8e9a0fa3` | 0 |
| nitro-reth/crates/arb-node/src/consensus.rs | 7146 | `63e2201d969e83494b5599865a5ff7868fd41b9b8b14d37be029098123172305` | 0 |
| nitro-reth/crates/arb-node/src/engine.rs | 4183 | `42de7da6b212e02ea487848d875f0befe2420721c432e6260a39a8e473358313` | 0 |
| nitro-reth/crates/arb-node/src/error.rs | 2790 | `6a2bd38c353ef160b1873e20b70ff0cb6d5ad1b9cbb36c8e644390fd86a938df` | 0 |
| nitro-reth/crates/arb-node/src/flush.rs | 1337 | `ba75baa8f8fd63c3318b0cc746bde636c36a5fed04c6659a1b4f366bcb9036f1` | 0 |
| nitro-reth/crates/arb-node/src/genesis.rs | 13691 | `855418b34a5b3b7467ac7123083d0d8a6d97cfcf6740fe0f253d94b138443668` | 0 |
| nitro-reth/crates/arb-node/src/launcher.rs | 28852 | `a8c81cd6dd85aa9fdf71475d3ab0677f8fe980297606727ce68e1cd0b0bdd46e` | 0 |
| nitro-reth/crates/arb-node/src/lib.rs | 9275 | `8d4db23b43d424767f995c1f6bcbd4538685d6474ad79adb9b5468bd8e9c8a3b` | 0 |
| nitro-reth/crates/arb-node/src/network.rs | 1313 | `e0678c9c2520072a1a46d159c87c7a428c0199c8676d97d0fb55306df65fa52a` | 0 |
| nitro-reth/crates/arb-node/src/payload.rs | 3823 | `b8be50b1a9a9d219d7274b2ea5233887437cb5d5801c6612eade545d5b842579` | 0 |
| nitro-reth/crates/arb-node/src/pool.rs | 2844 | `0b434d7be93f42663a4d6169edbd5efd7cdfd1c6b1809c8bce34faa722662798` | 0 |
| nitro-reth/crates/arb-node/src/producer.rs | 51535 | `ac5a80acee506f3da5d35aba698ba3c2a9dfc9619cf83d3f8f1aff68a74ebe2e` | 0 |
| nitro-reth/crates/arb-node/src/progress.rs | 7231 | `9c5e4b2107c1d06786b28cc8255224a0913f672a8d0d1702aef0e716e8644cfb` | 0 |
| nitro-reth/crates/arb-node/src/validator.rs | 2949 | `b95626b0e0490a9409880cb3a0f89b7232c7a5b7c91152d6ae1f21b0214ecec9` | 0 |
| nitro-reth/crates/arb-payload/Cargo.toml | 771 | `60eeedef1becc0b69d1f5e32686177aa4c64402647da2697e0615de9f170b295` | 0 |
| nitro-reth/crates/arb-payload/src/lib.rs | 10780 | `c2fa1c25483c60fd5633693dfbafe317767a84348a2a77258ac5c9a44e9235c2` | 0 |
| nitro-reth/crates/arb-precompiles/Cargo.toml | 997 | `2f968d82200e5689e2fb757e85102ec1533d83deef0ea0e742a68443e9133f56` | 0 |
| nitro-reth/crates/arb-precompiles/build.rs | 4270 | `836c90624e5f47caa5f23581cd105d0f6756b9ae3a99be5707b5392c9d532e00` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbaddresstable.rs | 10747 | `3bab3334d949bbc4ca485aeb3875f06eccc4206dba5c1c5bec4344e32945b979` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbaggregator.rs | 10174 | `b50d25efbab70f831aafa2df8a128da6596aeb7c700cfd42166f503746380611` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbbls.rs | 660 | `bde06f60a2af675377f9057a93d1e0cb2402e43a5203ad65408d34eafd7dda7f` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbdebug.rs | 9557 | `2685af642756034f300449c020b58f10968ed5d7475f82b9a678e626f4e9dda3` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbfilteredtxmanager.rs | 10120 | `070bc4d2bab7e085e12ff7fe9f8961fd17ce26a1f206419a4e6c4c178d4ffc40` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbfunctiontable.rs | 2689 | `ccd48df214edb20c8326e129edc966c49a08270cd3cf26248a1eb2a17ce1ead2` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbgasinfo.rs | 34501 | `f62773face73e5ed83b96aa9e4d12c229c2f8ed00244097b6b1013aed327c3db` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbinfo.rs | 3722 | `27b5e7b74dd842defbb78095cf14b276f8a2240ebb4c7e6465b66b2fb04db2ff` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbnativetokenmanager.rs | 6306 | `bc0dcc0093945074c52f54d7e14f1a9750db8d87647f5f8671ee1a98814e3675` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbosacts.rs | 1593 | `cf4bf2cb7902e0d6fd3d5878131c48665ff12f5006fb7d389327c010621c55b9` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbostest.rs | 2360 | `dec8755eb962b18d2be5507774452d23b6116d8a61ea123745b185ade48c68bc` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbowner.rs | 75105 | `e2387f1ca5805a7caaae770062827f61a1dd1834dfbe6bac6a101fc71c9c5c26` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbownerpublic.rs | 23066 | `aa5c92337738571fab020a4d99d2f9161c858db3b6c9edba38e1daa932205722` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbretryabletx.rs | 24740 | `b8e25155c77012fb9e0c2790dd19e69cdfa89985c8f6b38a9bc3704ff1dc4d0a` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbstatistics.rs | 2331 | `02ffbe0df02dd829874b2b8166267a5be6ca803f78b66a7af6e63f56d85680b8` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbsys.rs | 27503 | `833175da8df1f5a63aadb1c09ef978917e8d16ae3a8009eb9f126fe591452351` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbwasm.rs | 36265 | `302f196ee6591562b1d471dac405ec692bb32d6acd19cdc9c32019cc5359f38e` | 0 |
| nitro-reth/crates/arb-precompiles/src/arbwasmcache.rs | 13763 | `8eae331d4ded7d5dc704422179c95d4a5e736d0b3afda1d2e1a53cacb225f213` | 0 |
| nitro-reth/crates/arb-precompiles/src/error.rs | 3428 | `a99b4525abad10b992ef9c11a3cc887e1c9f14e90186367c59e0657d96bc8da8` | 0 |
| nitro-reth/crates/arb-precompiles/src/interfaces.rs | 2421 | `eefd68fbaadace4f8bcad0562cc6719d9889d3a925af38399dd80ec811baed3c` | 0 |
| nitro-reth/crates/arb-precompiles/src/lib.rs | 19306 | `8b916c634ad62c49a341e8b05e899234be35b0b043e8d8430312f9dcdcedb1eb` | 0 |
| nitro-reth/crates/arb-precompiles/src/nodeinterface.rs | 12092 | `22adb099aa90af69effb0df97c30663fab06d1202c88f8de2fad033272bb5be7` | 0 |
| nitro-reth/crates/arb-precompiles/src/nodeinterface_debug.rs | 1914 | `257af2f13af032175085bf7e5ca7e397d1160cc484b0879d49a3e8567c1bec39` | 0 |
| nitro-reth/crates/arb-primitives/Cargo.toml | 1054 | `7860f80bafb11668d516b574a236cd40868f36574264a4be2388907574b4c878` | 0 |
| nitro-reth/crates/arb-primitives/src/arbos_versions.rs | 2718 | `0956d3e20ce55ee5cf9d3765061d0c81f6e0f2f2634158efff6adf86eb755410` | 0 |
| nitro-reth/crates/arb-primitives/src/lib.rs | 1034 | `86be9be0bc1f6d31251e04c908f2136233a6893d08660c2a0634068bb67db7e8` | 0 |
| nitro-reth/crates/arb-primitives/src/multigas.rs | 13197 | `5d8a2c1bd8e84dd73e702b02fe4542d72611eaacfbf38fd11b6e86b981bf5542` | 0 |
| nitro-reth/crates/arb-primitives/src/receipt.rs | 33233 | `43c463a729adc8bec52a98e23eaa5484cd8c4ff98d43bd1ad7b2edf088f9f579` | 0 |
| nitro-reth/crates/arb-primitives/src/signed_tx.rs | 41614 | `80a2a7db0cfa79374ca65163031c9af61346b1c253eb8b0a9650a50213d8093d` | 0 |
| nitro-reth/crates/arb-primitives/src/tx_types.rs | 218 | `eb207649e3f240af3828629ff9c28cdad1d75809372d468a6ef70be71d3ca11a` | 0 |
| nitro-reth/crates/arb-rpc/Cargo.toml | 2042 | `4acecb66ad2624a752a7a209d9c5210681f8aef23fb765fb06539a8cc151246e` | 0 |
| nitro-reth/crates/arb-rpc/src/api.rs | 59003 | `57987960482bebd410528ae9955e5036e7073a81774180190a765bd64feee705` | 0 |
| nitro-reth/crates/arb-rpc/src/arb_api.rs | 8208 | `5dafa05623f19a4c2df9fe72ff1f338d789438e4f9254663e5def04e62f783f3` | 0 |
| nitro-reth/crates/arb-rpc/src/arbdebug.rs | 17652 | `8226b883e7c7faedc5ca894369320e97c23a91dade27e7276e0f51c43c7bc089` | 0 |
| nitro-reth/crates/arb-rpc/src/arbtimeboost.rs | 3676 | `a31c652315b64b67c747d8fa0d58774fafd3e994d0b4df2f7f92df1779614b20` | 0 |
| nitro-reth/crates/arb-rpc/src/arbtrace.rs | 7668 | `2c84aa08deb5ed8ee6a5eb01a96914270933f8cb7149692eb30c00e8abbc57b1` | 0 |
| nitro-reth/crates/arb-rpc/src/block_producer.rs | 3468 | `94c8985630fe79374dd543842968b0c4b22cb6cf95fe592b34606cbd133be172` | 0 |
| nitro-reth/crates/arb-rpc/src/builder.rs | 2419 | `69d95be66b2674497cac512d1ef5bd56c200416f5f671c023ad629ef72fe599b` | 0 |
| nitro-reth/crates/arb-rpc/src/conditional_tx.rs | 5705 | `3d0cec9a527c3ce157e76a286d0cef210d0ae1341f96eae0a79c87a36017f2e4` | 0 |
| nitro-reth/crates/arb-rpc/src/error.rs | 7078 | `156557f39abcc67abcfe108a454d77744593ed5fc2e2212fa15556fc9c5d376a` | 0 |
| nitro-reth/crates/arb-rpc/src/header.rs | 2407 | `2c74d06f66dad404c927fbe7ee701e1550cb41dabfdfad43c5d16548c661d23c` | 0 |
| nitro-reth/crates/arb-rpc/src/lib.rs | 3106 | `861d257c1e6335a4edddec6ab4f7fa935f92cf205b75f69d08c77554395bc8f6` | 0 |
| nitro-reth/crates/arb-rpc/src/mel.rs | 18063 | `3b3f1671e3efb7394acaed6d83a471fbc83bebc8874cf7c130536e6311b446c7` | 0 |
| nitro-reth/crates/arb-rpc/src/mel_handler.rs | 6365 | `23380158041e5a530002dcec9733c59f3839073a8500fd2245477c4a5b7aadb2` | 0 |
| nitro-reth/crates/arb-rpc/src/nitro_execution.rs | 9955 | `ddac7a1e7f1cb7b15a02b535e2420fef77b0a847a58bd708916a4c2a6449eb0d` | 0 |
| nitro-reth/crates/arb-rpc/src/nitro_execution_handler.rs | 18598 | `61ed78eb1bdf8462e14931657ed3d3d105ff6e94243db5f6e08d078cb171fa1e` | 0 |
| nitro-reth/crates/arb-rpc/src/nodeinterface_rpc.rs | 10251 | `736ed437eb9693649f8e4bd95445d61f19674b49dda19d539cf27b0a1041ab2d` | 0 |
| nitro-reth/crates/arb-rpc/src/outbox_proof.rs | 12686 | `a38ce07bfb7035e9cc712ce69e2e9923a47234e10e25991d5fb8ebcf7c417019` | 0 |
| nitro-reth/crates/arb-rpc/src/receipt.rs | 7070 | `2751fec7cbb0a749a1119cb7ffc6491f819abcc4a7ab84b5caded41901c8139b` | 0 |
| nitro-reth/crates/arb-rpc/src/response.rs | 4227 | `451fcf66c507eff8d33cc44f6f36d29363a7d1d222ae6210e58acdbf5948e8ec` | 0 |
| nitro-reth/crates/arb-rpc/src/stylus_debug.rs | 2176 | `f5480d5dcf3efc95b00b9650d3623e13a890b42e4368c78a26a552b161f23200` | 0 |
| nitro-reth/crates/arb-rpc/src/stylus_tracer.rs | 7978 | `d1f14f9515b05b65d8f8e01fd4ab6e41cf35e07acc769d3f113264f689000f44` | 0 |
| nitro-reth/crates/arb-rpc/src/transaction.rs | 2858 | `cb088be85a9005a0a0e213ceb5c7a5755fa1c46d833aaf53c096564b5184c5ea` | 0 |
| nitro-reth/crates/arb-rpc/src/types.rs | 666 | `9ba74561ba11ef972a74528fda23c1b63eafc98929b587d4b7ff465b5424f372` | 0 |
| nitro-reth/crates/arb-storage/Cargo.toml | 617 | `f4e9427bad7d4cf0a2693925498991cdd3770ae45a0a525a9e5943140cdfa145` | 0 |
| nitro-reth/crates/arb-storage/src/backed_types.rs | 7447 | `a4d4ce8fa6b0662e9a422b30ddcfc1568c7643c8193056bab23d7663a7cf4d36` | 0 |
| nitro-reth/crates/arb-storage/src/backend.rs | 4933 | `bf633872a772720ef2a1a92e2b432b1c9797bc9f1fe6936ac75cdd9abed40131` | 0 |
| nitro-reth/crates/arb-storage/src/bytes_storage.rs | 4205 | `957c40cdb0210425d4ee78a99005ef796cbd0f99a9f1fedafddf493819b99fba` | 0 |
| nitro-reth/crates/arb-storage/src/extra_types.rs | 4653 | `297bf3aa5440a580470e087c3fd9be9631dab93e45b58b4771ac5dc03ba2a649` | 0 |
| nitro-reth/crates/arb-storage/src/gas.rs | 647 | `374865dfb0ce0374b186aca6a83d8ab2aec784f3dc7f62028426e0114e28cb11` | 0 |
| nitro-reth/crates/arb-storage/src/layout.rs | 4905 | `dbec37d0abd9b59118f3c2935ff696914b3e14dfbc8327265dcf4d463b3d365a` | 0 |
| nitro-reth/crates/arb-storage/src/lib.rs | 1601 | `b261d4b167197490bdd43d8a5e7d045cf6e699d7ebdb1e95173af859b7a6a085` | 0 |
| nitro-reth/crates/arb-storage/src/queue.rs | 4343 | `3db5548999ea6bcc59a823ce32c65da6f345adaef696889fba177e29d89ef794` | 0 |
| nitro-reth/crates/arb-storage/src/slot.rs | 2356 | `3842c4f92a562b5f6d8f1f0b751175d952cca7ecb0242097d5d71a6e881a518f` | 0 |
| nitro-reth/crates/arb-storage/src/state_ops.rs | 16089 | `83f1f4b3cadc8f2d2500e7e56bf16ade8cb6394511c23db9662f3bb9de9b8ea6` | 0 |
| nitro-reth/crates/arb-storage/src/storage.rs | 9968 | `87ae15d2fa30247e5215793a70a1022f8343666963c863d314a94f1d5516de49` | 0 |
| nitro-reth/crates/arb-storage/src/vector.rs | 1688 | `0eead95ec3ccb23391917b5db2e537d8f7db7b9af1bca9a3a47eb0b51589c97e` | 0 |
| nitro-reth/crates/arb-storage-errors/Cargo.toml | 389 | `f03a1e69cf994de64ff2ffc6177f59598ee8dcce66e1978a2454a3caba0078dc` | 0 |
| nitro-reth/crates/arb-storage-errors/src/any.rs | 1158 | `8cddc306f57e0c0a0d7f3255bba62639f568a8e34ce65878abaf18d5d25d34d5` | 0 |
| nitro-reth/crates/arb-storage-errors/src/db.rs | 1810 | `b3066d640851787694d6898ae42790d1ae787f002fd40c05931240b022aa61c3` | 0 |
| nitro-reth/crates/arb-storage-errors/src/lib.rs | 671 | `202073e40a9ffa5f120d5e93d82c81f74f94a8bd9bc15ec20c28a2d6b5ac3866` | 0 |
| nitro-reth/crates/arb-storage-errors/src/storage.rs | 1174 | `10144ba198327e731c5c65d6b53f408f57cfd3e0c8052e53237e1ca1209b2fb8` | 0 |
| nitro-reth/crates/arb-stylus/Cargo.toml | 1059 | `59eaaf2f9ba8dfbedf0d3941e655f68b9804e1a1cff0d6dda8f79aa02060d6ee` | 0 |
| nitro-reth/crates/arb-stylus/build.rs | 310 | `16743dfa286deab076fdfb7b9e993da0f1aaba289b4207c4b351c2dc4cd3443a` | 0 |
| nitro-reth/crates/arb-stylus/probestack_stub.c | 580 | `8d3c4e7084177b96ec3031cb05bcfa79a04ccef36375b08c057729c1a5dc7016` | 0 |
| nitro-reth/crates/arb-stylus/src/cache.rs | 10695 | `e4d3dabf1c97526c15fda80969993be4d50f1d74030fbcca3890e4abbfa3ddd4` | 0 |
| nitro-reth/crates/arb-stylus/src/config.rs | 5301 | `b01b67f0c3ba730e6d7af37718dd3d61fb4943a98d17fcccc2db8ee5f1b1bf14` | 0 |
| nitro-reth/crates/arb-stylus/src/env.rs | 10148 | `1820661a5eca720b59d8ee49ec948468d284e0dacf63727bf01c937013f4f75b` | 0 |
| nitro-reth/crates/arb-stylus/src/error.rs | 4361 | `d3273c53d9b6ce5bbd7e41352993fb848b285028194c3e612121cde91d66d4b9` | 0 |
| nitro-reth/crates/arb-stylus/src/evm_api.rs | 3704 | `39cdb9cc4e4fa9a3be8f0ad9c151dd697fa05507ac68a89585095218c31a903c` | 0 |
| nitro-reth/crates/arb-stylus/src/evm_api_impl.rs | 43024 | `28343b22c66001b1d566ad83fa25eacb3b6371708b2feb6ed6d725e82934c1e7` | 0 |
| nitro-reth/crates/arb-stylus/src/host.rs | 50340 | `0aa4d4e1fa0d1cfdc1c749df0b3cc47bdf5d8e45fb34e45a9cc9ac51bcb02074` | 0 |
| nitro-reth/crates/arb-stylus/src/lib.rs | 16126 | `53e9bdcfe98aac4732ab0576f201340334448e88ce951b030acd9e8daee24e5d` | 0 |
| nitro-reth/crates/arb-stylus/src/meter.rs | 3326 | `19fbd2f62ef1f1a49222a627b48448842eb27dae89b4cd746147588c6289602d` | 0 |
| nitro-reth/crates/arb-stylus/src/middleware.rs | 41112 | `aa58c8ef7d9d8b77bf636fdfb82eef6d7f2fc66ab425548742411f6cef04dcfb` | 0 |
| nitro-reth/crates/arb-stylus/src/multi_gas.rs | 5767 | `6034e61a0e526b8bb6b167914b62e015d574e4da07f9ad832278bac804c78d0a` | 0 |
| nitro-reth/crates/arb-stylus/src/native.rs | 14054 | `9987c823cdcbdfef15ff36692afdeb690ca8a8036755bbe1bb1f57323a897566` | 0 |
| nitro-reth/crates/arb-stylus/src/run.rs | 4373 | `d9046095b7cb22aac4ae0c42a10ffaf01e882c97439f966a3430596471137986` | 0 |
| nitro-reth/crates/arb-stylus/src/trace.rs | 9212 | `98adac71e2ff10ecca8e293617a8d96803f3dc8101df5606aafe82e252e09147` | 0 |
| nitro-reth/crates/arb-test-harness/Cargo.toml | 1273 | `0826a829b88520842608235e318e09d5f108cf4da5d0680e26e48b8d2e271679` | 0 |
| nitro-reth/crates/arb-test-harness/src/capture.rs | 4679 | `916b7acf7cb47f83d221fb5013f29bc482b0efc691ac86d9d465a64c032ac1c5` | 0 |
| nitro-reth/crates/arb-test-harness/src/dual_exec.rs | 19888 | `4d323a1ab0036a05cc73e97d26fad1ec21b0ad4c19190ff7a720e8c7e50d892a` | 0 |
| nitro-reth/crates/arb-test-harness/src/error.rs | 924 | `3a46b3925a75126cf4321274c384df3e438cd045cbb08f0622d9a4dbced2034c` | 0 |
| nitro-reth/crates/arb-test-harness/src/genesis.rs | 8544 | `e840ebe94925649114539056ae64828b63d82445aab8a7691002ba18a0386b18` | 0 |
| nitro-reth/crates/arb-test-harness/src/lib.rs | 443 | `4db7aae1d9b635e2e8fb838120ae5a5e5587a95a47e542c352e3272ae1986a65` | 0 |
| nitro-reth/crates/arb-test-harness/src/messaging/batch.rs | 4664 | `6b4ee83c460a787f3afb2ab344d6d3b61adc3ebb07d13464c02eb633c31e421d` | 0 |
| nitro-reth/crates/arb-test-harness/src/messaging/contract.rs | 4282 | `92807bf49ce1bdc7541393adef05e8811313253b239b1552a0f88f71600e20cc` | 0 |
| nitro-reth/crates/arb-test-harness/src/messaging/delayed.rs | 3320 | `5acc3ba82787cc4eeffbf8d4b3633c6d906ab7a5a11895c4f82a189870acc945` | 0 |
| nitro-reth/crates/arb-test-harness/src/messaging/deposit.rs | 3509 | `fc7839565c6ca5024d775445297d4c2f5d920e0ae0d5bc6db497b0650e28b53d` | 0 |
| nitro-reth/crates/arb-test-harness/src/messaging/heartbeat.rs | 3916 | `69a65c080a6964916fe8c5b1eb91cfe481339d967afa698284e97b28f408e938` | 0 |
| nitro-reth/crates/arb-test-harness/src/messaging/internal.rs | 6823 | `3af9d37c813dda91bceb11713f02a20b404b614b36e92ffd15f12998b4629f30` | 0 |
| nitro-reth/crates/arb-test-harness/src/messaging/kinds.rs | 775 | `f46fe79af3850ee13bc49ee5c0fcbdbd1a8c1d0f99786832dcd61022b1105098` | 0 |
| nitro-reth/crates/arb-test-harness/src/messaging/mod.rs | 4873 | `e69066fcc089eef45dd4a2017a83699390085a157e1e524f2a2756a67f0ce586` | 0 |
| nitro-reth/crates/arb-test-harness/src/messaging/retryable.rs | 10947 | `aba87065cc1501647fae2cad6f5fb92e664f1a70fd5d8140e0ad79531344b414` | 0 |
| nitro-reth/crates/arb-test-harness/src/messaging/signed_tx.rs | 23091 | `fcc4c7d88b71f6bd8bcce9ab8eb6312a9f649aa4b502db0cf4cd787a2737e173` | 0 |
| nitro-reth/crates/arb-test-harness/src/messaging/unsigned.rs | 5514 | `0f43e56407863fc77b73b272e67f9c9163746d3031792b8d9512342f655643e3` | 0 |
| nitro-reth/crates/arb-test-harness/src/mock_l1.rs | 5561 | `4b02f9a558df40579dbf2caa571a81303d38b42f05a230ee9ca607e72b3e0f07` | 0 |
| nitro-reth/crates/arb-test-harness/src/node/arbreth.rs | 8847 | `688773f6242161162dedf383919e164660d4749304666f3bd6b594bdac07b7a4` | 0 |
| nitro-reth/crates/arb-test-harness/src/node/common.rs | 9572 | `f5a1500ffdb5a97672372f6ca48641d3570383f9969a4ed54aa34956ce849ef2` | 0 |
| nitro-reth/crates/arb-test-harness/src/node/mod.rs | 4108 | `486f53043a134c1558db83e31daa60155d330f108e18e2a4560139e8e622bcf7` | 0 |
| nitro-reth/crates/arb-test-harness/src/node/nitro_docker.rs | 16556 | `9581008949bc8b9e5e98a5e9d23ee99ac10afbe56e0667c0807f06e35190a37e` | 0 |
| nitro-reth/crates/arb-test-harness/src/node/reaper.rs | 3112 | `0f8d5d3f380b2354a457436e0b0c43ed170bb932f199860af685b5dcdaffa485` | 0 |
| nitro-reth/crates/arb-test-harness/src/node/remote.rs | 12550 | `b602f4246e1c794b734d1e89f4a06273aa382c3ef1d097086b42a2400ced5aca` | 0 |
| nitro-reth/crates/arb-test-harness/src/rpc.rs | 2601 | `cb24cc860eb8a2ca613a2f09dc9c09c4774ed6076c5404059686bd680b98e9ce` | 0 |
| nitro-reth/crates/arb-test-harness/src/scenario.rs | 1027 | `5ae8a3f6d2676bf98a8d466668f08472e1b987e8ba697798e4dc969b7c721f82` | 0 |
| nitro-reth/crates/arb-test-utils/Cargo.toml | 447 | `7607c60d23729f89c44008d5a2a93f14322a88c99856513ecc8cbbacdec9046a` | 0 |
| nitro-reth/crates/arb-test-utils/src/accounts.rs | 957 | `20c647f2de5cc7398a7ddd239c88b3811a54134a1ec8a80c815da637ba36ab67` | 0 |
| nitro-reth/crates/arb-test-utils/src/db.rs | 1749 | `eff9dadd1c65acdb0919aca2e334e518278152e3f716387eacff646bf8d3c013` | 0 |
| nitro-reth/crates/arb-test-utils/src/harness.rs | 6445 | `b7cd724509ee57a674c369209bd12f01042c8c98d386acdc3259290ac2a6d5f0` | 0 |
| nitro-reth/crates/arb-test-utils/src/lib.rs | 231 | `71003723e603a7c176333a5b101d165eecfab95a06034bdcffb49a9dc77570b5` | 0 |
| nitro-reth/crates/arb-txpool/Cargo.toml | 558 | `b67dcf0c3f08542a94bf09ce977ec9a2f4902174d742727096911590fa88bada` | 0 |
| nitro-reth/crates/arb-txpool/src/lib.rs | 239 | `8ea0f8c858d97261e020db417bdac061d2845aad103b518756bc093cda6997c6` | 0 |
| nitro-reth/crates/arb-txpool/src/transaction.rs | 4874 | `39bbe20037c367e48f235f9ffdf2a54aac8a72b85ae8b0c6780390f07aaed7c4` | 0 |
| nitro-reth/crates/arbos/Cargo.toml | 1154 | `0eba617db9d0cb122d9aaef6750a9214847f8ab9d0dfec69cd3ecf4ff0256246` | 0 |
| nitro-reth/crates/arbos/src/address_set/error.rs | 595 | `ac0311339ace219884ba8de597c77b16467ca96b738e29287399ebc09c53e4cc` | 0 |
| nitro-reth/crates/arbos/src/address_set/mod.rs | 8082 | `2942a427b584f0673514f0e61662532c8be0457e0ed0c1faf9146d2beefdc991` | 0 |
| nitro-reth/crates/arbos/src/address_table/error.rs | 619 | `3c609554df91287aa985fad7709c10cc4403034cdf295e7ac70441ec52dc7313` | 0 |
| nitro-reth/crates/arbos/src/address_table/mod.rs | 7245 | `a9879694a3bad45830289709f86d5ba88510f88e983e97c4dcaeb3fc0b0e2dee` | 0 |
| nitro-reth/crates/arbos/src/arbos_state/error.rs | 3626 | `b66b02db17fd8f31c0c53b54a54e752dabea7e77d183ab57d939b8e751ee4b7b` | 0 |
| nitro-reth/crates/arbos/src/arbos_state/initialize.rs | 9431 | `e509342ae136abc5eae3be85e23d39a2c80edb242a851679b9dcd5860c9bea92` | 0 |
| nitro-reth/crates/arbos/src/arbos_state/mod.rs | 28541 | `2c40401d2d2887e8398a71bfcb1036c9581940c09203f41dca87cac4016b5eb5` | 0 |
| nitro-reth/crates/arbos/src/balance_ledger.rs | 4558 | `8979597ab3acabae49f689f8f08156888460a5e9f1238f7206754eda2101c834` | 0 |
| nitro-reth/crates/arbos/src/block_metadata.rs | 928 | `fc197116346b8f9a3095fbda2b69312dbf015e2c2d6948186a29e783968f5dbe` | 0 |
| nitro-reth/crates/arbos/src/blockhash/error.rs | 254 | `9a7c4ad8773142d8767f8f82b4e8bef0dcbc20812be7e9ebb4ebeb61f96e6dfa` | 0 |
| nitro-reth/crates/arbos/src/blockhash/mod.rs | 2506 | `1d2694fc319951aaa3519f819a1809944495a94265e3ed126f1c03ff2be4e1ac` | 0 |
| nitro-reth/crates/arbos/src/burn/burner.rs | 2438 | `cca3824cdf745227553dd3ec877eda7814eef79fe7d9623aa7e557bf87dabd22` | 0 |
| nitro-reth/crates/arbos/src/burn/mod.rs | 53 | `71f7f2e001067939720a4fb3cd04e9bdda1c81b1f17033e0caf7c6cfb4d9e2ad` | 0 |
| nitro-reth/crates/arbos/src/compute_budget.rs | 9948 | `6b203b17d908ca46383265ca96ed0494712929f709496cd843da9be6115c8c69` | 0 |
| nitro-reth/crates/arbos/src/engine.rs | 372 | `6c4dfb9a78730f1b74e22c2dd9b353678962da0633ad896f7b0c0751c484df71` | 0 |
| nitro-reth/crates/arbos/src/features/error.rs | 245 | `e59c56127f132b3d91caffda843266b9d0ab0bda16d3fa2c6ffd9c3497ca2625` | 0 |
| nitro-reth/crates/arbos/src/features/mod.rs | 1875 | `61213da781a5fbc04297fe0bf85edc83be1c1e0a8a5714b1be2a3a1f6e2831b9` | 0 |
| nitro-reth/crates/arbos/src/filtered_transactions/error.rs | 255 | `6fa9226ba6b57a453bafce47a3101ae00c640b08c9de0cfca9c295f1e2a724b2` | 0 |
| nitro-reth/crates/arbos/src/filtered_transactions/mod.rs | 1713 | `a7dfdf32927802784231edde0f0431f03be779dbcdc45d44eba1d9f822af4d4b` | 0 |
| nitro-reth/crates/arbos/src/header.rs | 9909 | `6b7a2bd5a9f2b36e5df7bb90528512d4a25bcf5c0b74eae1a5f769d1d409ac88` | 0 |
| nitro-reth/crates/arbos/src/internal_tx.rs | 18366 | `eea5b067decb58413d59221c8904defc6850a42d5401058d3afe9edc1b64228b` | 0 |
| nitro-reth/crates/arbos/src/l1_pricing/batch_poster.rs | 6675 | `234d138990530b50f81a1a5f9fc4172e367f31b3ea118cc2d17dd797005633e1` | 0 |
| nitro-reth/crates/arbos/src/l1_pricing/error.rs | 1186 | `87e904e04bcc646db123161c1d1045a82a530da1fffd0cdac670d84f8fb9f061` | 0 |
| nitro-reth/crates/arbos/src/l1_pricing/mod.rs | 26925 | `1c90fdf7d7b7676b9b60783027a7d7125da2cc4939f51d8c4b596c510a818a6c` | 0 |
| nitro-reth/crates/arbos/src/l2_pricing/error.rs | 246 | `089abd74b63f8a0b5d5e68127b646851c88110651a447e6231d227d6018e2d9b` | 0 |
| nitro-reth/crates/arbos/src/l2_pricing/gas_constraint.rs | 2122 | `dc73ef9bf169932c424b180d72bc4e5196f725c5170cfa2bca8358d6ca460bba` | 0 |
| nitro-reth/crates/arbos/src/l2_pricing/mod.rs | 11401 | `aad284f3fe83d7cb05a805cfa1eaf05c3c61e1b8f59d5b6dc34a4c20a7d435d5` | 0 |
| nitro-reth/crates/arbos/src/l2_pricing/model.rs | 108225 | `99fd30102ef1db8889e09a87a6a9ad5f4b16467219fa525069b1c991e169af50` | 0 |
| nitro-reth/crates/arbos/src/l2_pricing/multi_gas_constraint.rs | 6714 | `d9b70d86903be7d424c754f7d46166b171a7f125c366a66f2277a85dd933ba7e` | 0 |
| nitro-reth/crates/arbos/src/l2_pricing/multi_gas_fees.rs | 2429 | `6198c5e6092b9ce36451c524538347f0252b1e2c9526f6bd2c0c54b376ce8070` | 0 |
| nitro-reth/crates/arbos/src/lib.rs | 689 | `c2b818697efe25a089936b541deb33affa7a7283590ddf9625931f1a63b69bb4` | 0 |
| nitro-reth/crates/arbos/src/merkle_accumulator/error.rs | 266 | `4a9538ab58aafa32e0fa33176de01172650c8d2162c0d6709bcb74d102b3d4c8` | 0 |
| nitro-reth/crates/arbos/src/merkle_accumulator/mod.rs | 10048 | `df6a24a2627319864a7b963cf18c396575bb76933e702b362c00ed1d5564cbad` | 0 |
| nitro-reth/crates/arbos/src/parse_l2.rs | 20673 | `f5f2ab4bfc3432482adab4b7e9376cc018232fd65409a69608359d92e0d0cceb` | 0 |
| nitro-reth/crates/arbos/src/programs/data_pricer.rs | 3890 | `792774613fecf317cbe3362061fd5410bfd14fcd49216d24bb0396bc80e46d65` | 0 |
| nitro-reth/crates/arbos/src/programs/error.rs | 3008 | `aa34345dfad175330741b4f7942073d64c8cb179b267720b023dd8c6c63932a1` | 0 |
| nitro-reth/crates/arbos/src/programs/memory.rs | 2152 | `58cfd5944d37fcb37d33fd5335e110ce132c3ec78206c2250c987392be26d5a8` | 0 |
| nitro-reth/crates/arbos/src/programs/mod.rs | 16632 | `6414e23a12b10498f54034a0233ae50a070c094cf411a3f55551fb3d9b07151f` | 0 |
| nitro-reth/crates/arbos/src/programs/params.rs | 11141 | `674bad6643fc874d24819e1de1783a531d201efca47569eb6d4d987f1b79777e` | 0 |
| nitro-reth/crates/arbos/src/programs/types.rs | 2219 | `a8314d2c60af6a77f8207dbe4cf823146456f459167aef9b2c5af20bdc1b6215` | 0 |
| nitro-reth/crates/arbos/src/retryables/error.rs | 1072 | `f1d4490f4ae111069a4e18c07fc1d8631f9cd75e7147e4e75c41b32bd6f250d0` | 0 |
| nitro-reth/crates/arbos/src/retryables/mod.rs | 21649 | `4f829015b82880e8cee36634f8ac8a56b731485c20fb3e439689ad5fda4fcdf8` | 0 |
| nitro-reth/crates/arbos/src/reverted_tx_gas.rs | 1630 | `a6090cd1e0f5b07476661507d740a8bf5332e6adc6df37239391d8f70f1421f7` | 0 |
| nitro-reth/crates/arbos/src/tx_processor.rs | 34439 | `d107418220cedb07e61bc14f4cb8764bdba3c308b347382f83e394f90076563a` | 0 |
| nitro-reth/crates/arbos/src/util/address_alias.rs | 2406 | `9a2e6dc280e404e8f906e96be0761d32e15bb95dbba4e71acad53d0d05829c1d` | 0 |
| nitro-reth/crates/arbos/src/util/mod.rs | 364 | `49ddde623f292f83dd6edf2e08871074649c72628e534f477eb4f23fd19cc1ad` | 0 |
| nitro-reth/crates/arbos/src/util/tracing_info.rs | 780 | `ae62abaa7416772c96b50ed1b85d33d6041f6c323d1fb8c9b45b2ad1f526ea1b` | 0 |
| nitro-reth/crates/arbos/src/util/transfer.rs | 1587 | `ed199e12a7610c8d1bb21385f9c4377c12d77639f7e9c7dde7038b5c65563026` | 0 |
| nitro-reth/crates/arbos-types/Cargo.toml | 325 | `36cd5a8fd4f223dca659aeaf5a64342a9256d0592ad8c7473a519699c13e7d4c` | 0 |
| nitro-reth/crates/arbos-types/src/incoming_message.rs | 12441 | `4fcef5be24c990318abf0fdd9b24d02ccee0c7cb88403526295e1d3f10ebd43c` | 0 |
| nitro-reth/crates/arbos-types/src/lib.rs | 1311 | `d9e3e7fc8d6829bc342254cc95dfc1cd1aa8aa61e572a9cf6af9a7d1885a8114` | 0 |
| nitro-reth/crates/arbos-types/src/message_with_meta.rs | 1285 | `bdd4e0af941a2f291c499a738520b74880fe52cd9ee004ec5b76cbc0ecb00cc5` | 0 |
| nitro-reth/crates/arbos-types/src/rlp.rs | 3253 | `c96d2f41eea602f34a5f42c16e1f9cce96d4e1e77a51e5e439d9dc66f4de5dc2` | 0 |
| nitro-reth/crates/arbos-types/src/serialization.rs | 3637 | `0e9a1c9bec83b4ee006a276fde0e34d56c766aa974cdf1ea351502474b1ce6b9` | 0 |
| nitro-reth/docs/package-lock.json | 406056 | `6260251ff3425acc78ba429167a054ac20456761d63bd3a53917b34acf2e21af` | 0 |
| nitro-reth/docs/package.json | 271 | `1030828b6849e881d819496ae5832ef3cf27660a7b94a7afb5497a9493d9db47` | 0 |
| nitro-reth/docs/vocs.config.ts | 1949 | `590c0a1603a02ef23350dcfb7c337750f445db2d539d5dbafe18732540e2270c` | 0 |
| nitroversion/current.go | 2177 | `b7aab81ed2039bb35f979163c66fcc288940e060e0a2100088bf6edfa1e59a33` | 0 |
| nitroversion/version.go | 7556 | `4614e93d426e31d99112f33d052e8c51ad3219a4bff3e35a91507169a691d473` | 0 |
| precompiles/ArbAddressTable.go | 2596 | `e7395408ab80eb63df3c659715ab820959b4556a2fb55501d83c1fb8ceb796aa` | 0 |
| precompiles/ArbAggregator.go | 3577 | `a9c22c66547e91d10a004495c1237fff52e4d630cde5b7f43617d6641b5b0e58` | 0 |
| precompiles/ArbBLS.go | 259 | `73fb359b55ff4b896fdf341756d8c4130ea9dd670379caaad7e3f5570e7c4c7c` | 0 |
| precompiles/ArbDebug.go | 2647 | `c53e795fd61c55c300da2c21d6c11470ad581346e7ec480e8d3ccd9a40dd18b1` | 0 |
| precompiles/ArbFilteredTransactionsManager.go | 2144 | `e1a0a62f8dc61d08d50a512ae1fe9cbd8ebc3bc803b025b82aefc3584a599ecd` | 0 |
| precompiles/ArbFunctionTable.go | 958 | `761515da44816bea73647a519968dd121374f100faea797bf4aaa11d5adbeeb8` | 0 |
| precompiles/ArbGasInfo.go | 13762 | `adf4bc79cf1cb650fd5a14f02f49578d39af8483d214be9c63769fef4701d54d` | 0 |
| precompiles/ArbInfo.go | 1203 | `d7ba3232f9587c93fb020d24405c20cf8f99373972a53152c0286826d4e3a401` | 0 |
| precompiles/ArbMultiGasConstraintsTypes.go | 568 | `c1103c33c8dde1e25769311c8d66e1441df2c78ed92a490a7e6d17c2444cdb81` | 0 |
| precompiles/ArbNativeTokenManager.go | 2250 | `7a657df13501c4638b33d764ebcf9989ebda5b3edcf0a967353ca95c4d14ed41` | 0 |
| precompiles/ArbOwner.go | 25491 | `ffe02545d3af25ab2aec245d70c8b7d511e1a27cc342c491299d90692a7df0f9` | 0 |
| precompiles/ArbOwnerPublic.go | 5018 | `3e7f40582f6446ec9b0030fb3ad6bf90c5d9dbc529140a09f2d083fdcdce7572` | 0 |
| precompiles/ArbRetryableTx.go | 10114 | `6d113ee3dd6617e0f9f13238cd1f17a99e8dd478aa8239072f12953eca332ad0` | 0 |
| precompiles/ArbStatistics.go | 1282 | `84d420a95f8fa1c10aa78db0ffc4009a542cec4ab502b6bba4a7486393605e7a` | 0 |
| precompiles/ArbSys.go | 8307 | `21534cbf1645dc6139219590714b9d91de44bf3b8ccad9463dcb2cc7e87543bd` | 0 |
| precompiles/ArbWasm.go | 8606 | `d69353ea1a6f2a083d3220491d2f3044a24d1e97fb56b869815b4e97e361e597` | 0 |
| precompiles/ArbWasmCache.go | 2666 | `e48a942fd72f604544d9736c64a7c30d82b41a5946a6e735eb2f0a1471d16c60` | 0 |
| precompiles/ArbosActs.go | 1034 | `a59f30c2b99de75a47e32b1be610178da86836829ea896fcd90d8143b23a4408` | 0 |
| precompiles/ArbosTest.go | 729 | `26429e31f81c999e7df50cd0280128acce7f70737317892af558c7e0db5b4b4a` | 0 |
| precompiles/context.go | 4383 | `f961d0a24f4fc44e9ab3c4251826df6ccc10e004911c9acaa2b8b860571848eb` | 0 |
| precompiles/precompile.go | 33644 | `c284cea90f037b84048ba59306d73fb7bce25b15e2e469ebc898c0d8b9838d3d` | 0 |
| precompiles/wrapper.go | 5926 | `fd770434dfafe6718bd53590f99476bd8a8dcffa43dbbc7b855e4f9b56abac45` | 0 |
| pubsub/common.go | 1555 | `96159ce996b6ce02a83b81b9a28e24c549828b1e5c247430312dcce76529e500` | 0 |
| pubsub/consumer.go | 12638 | `56e50275b83bcef6d190946ce10eb98940094aa47c3067958fbd8b4a23e117f3` | 0 |
| pubsub/producer.go | 10228 | `df09b04f2765b2d27d1d0c9f6b4c7ce497f1544bc76bd13bbfb7830f46fa464b` | 0 |
| relay/relay.go | 5944 | `eafb622ed0fc74ea0fb123cef9bc8afe095de510d9067a3f9814aa1594c407b5` | 0 |
| rust-toolchain.toml | 159 | `62d6122b7bd81f0d42d051084ec8ca9da4eef745033d73e1da8bf7dcb252f78f` | 0 |
| scripts/create-test-preimages.py | 1125 | `72d86d7d2e7de036172700a61a85263ec50dca3ce61e14c52c2a3ed02127219e` | 0 |
| scripts/licenser.go | 6095 | `f7262940dac0645daf7ba835c20ba6ca9b52587f85f2800a5c39819900b04842` | 0 |
| solgen/gen.go | 8801 | `54abce5afd85c027e418a6f6d4c7a0b92296a75805ff9305d65a2cf10f583013` | 0 |
| staker/block_validator.go | 59526 | `a1bec9a5928a6e6b8ca56fcfd94d98039542bf3502d25cfb4dca911459e40d4a` | 0 |
| staker/block_validator_schema.go | 759 | `15bc9cf7904677fcdb1f3d98cee4e2aa3d8b6855807dc1e765cae971d4bf6015` | 0 |
| staker/bold/bold_staker.go | 32148 | `ce6968cc4e28f5d360bdba77f6cc3c0f61bb7a1b81c455fc5a31b7a7a776889d` | 0 |
| staker/bold/bold_state_provider.go | 20454 | `3c5296bd37704db65a6f2bdb5befbe699f7b1352212bd06dd01ebce419fa7173` | 0 |
| staker/bold/data_poster_transactor.go | 1305 | `ba18c4758d3b0a9cbe9501d73dc7d17205e9be8a5595d4a6fbf5ba7dc5fb6f30` | 0 |
| staker/challenge-cache/cache.go | 9527 | `951077571b80112fc456ae3a64f0f9072eb2d8d6e3c7c35c2ef65f6096c28d75` | 0 |
| staker/execution_challenge_bakend.go | 1569 | `019254a2f237ac65be21c8430bc057b22e16be4f3a65febe97dd30fa479d4765` | 0 |
| staker/legacy/assertion.go | 2476 | `1b526d8af1a18cb508a08de08ff4810ecdd51e10ff0f19a532b5a6eabf918c28` | 0 |
| staker/legacy/block_challenge_backend.go | 7087 | `8a76697ec95f36ccb02f3287f2d63055fb0e6a43133e2e260b724f42e2ffdf9c` | 0 |
| staker/legacy/challenge_manager.go | 21509 | `8fcdc9297fe76a578611a7fb0e65c594b743d5397a3a93c29fffbba601e4354a` | 0 |
| staker/legacy/fast_confirm.go | 7565 | `132a86c181a7aa9ff86c1c7be2650844a391eea8ec73887a5b2f4f180d090b2e` | 0 |
| staker/legacy/l1_validator.go | 18560 | `195496b684574556e0fe6cc286bd3202b070f2dafea6874d9cfab23c29596900` | 0 |
| staker/legacy/rollup_watcher.go | 10520 | `fbe644d0ffa261e6b1b8fe4c95f36b5ad96c1047e3f9b2349162054a9d57ca8f` | 0 |
| staker/legacy/staker.go | 46931 | `a18804fade75d5586d8e7556ec5fbeeb96e8a962a08bd15490944d32137e87c8` | 0 |
| staker/multi_protocol/multi_protocol_staker.go | 10028 | `e3aab70acb32bfb9dd5bbca46a95e1031fd85bb3c6d871ce8de567761be4da04` | 0 |
| staker/stateless_block_validator.go | 20126 | `01e9c20ecf40b0a8ac3c39abad52e1e6a94a3fe1e2a0e6d8983916392c010d80` | 0 |
| staker/txbuilder/builder.go | 4532 | `fad7c97ba6ba6f6a7fce8451735dcfdac96107e328f498dae888648d7964742a` | 0 |
| staker/validatorwallet/contract.go | 13611 | `c70443ecf12364895ab38277e184755e023f0a0323a4a5b44377cbeddc25cebd` | 0 |
| staker/validatorwallet/eoa.go | 3330 | `e6eb4fbfdf37609a8a5a8bada1ba709a0dc92dedbef810fc1d7611ba6116c417` | 0 |
| staker/validatorwallet/noop.go | 1898 | `d12f017b31d0ffb4934bcd690b9261045cbd5304bbfc22e0b74903acd3f324c4` | 0 |
| statetransfer/data.go | 1233 | `a021f8327621dc83618244ff3b8831a270890252c31eca7660920ec5c49ca4dc` | 0 |
| statetransfer/interface.go | 898 | `7257b23e7511a8b81a37d3c2abdf82d05ca80f52c240f77a30bd6a0ba76b438d` | 0 |
| statetransfer/jsondatareader.go | 4920 | `6d967359b4efb78ebf742e3ecdebd6870ecc9e6dada36d519bac46ec0fd86e00` | 0 |
| statetransfer/memdatareader.go | 2236 | `58dc9155de4f6dee7268a3d844c037cd550618a994a4aa64cd331815c231dd1d` | 0 |
| timeboost/auctioneer.go | 35426 | `8c37f110d725512d329b8e693761ed73fe0c694955fffa2d2e77ee100d6bbb40` | 0 |
| timeboost/bid_cache.go | 3091 | `d0a13c08fb6374f46e7a2f8c1f827cfb2c24dc1737b5dc2bc14f6dff53f19d25` | 0 |
| timeboost/bid_validator.go | 18029 | `b8e88ec77ed0e356437484c38575d42a8204405812d4a9964168ddac1ef8b958` | 0 |
| timeboost/bidder_client.go | 7861 | `bd1aa09b3a8dc5cf8cb39a66ce5654947bf016d8f62ec3ee3a8a3cf6a9c751d3` | 0 |
| timeboost/bindings/mockerc20.go | 48584 | `d3a8ec36c2c2558a70672bf7e275743293d6dba68d46992c7f71a3576d41df23` | 0 |
| timeboost/config.go | 3414 | `ee858b3281a3ede4a5a80d12b75381b020d9ce14813d826cbe0b02127d8080da` | 0 |
| timeboost/contract_adapter.go | 4537 | `c0843a3fbe8b415d4d4a2a4bd177ea9d39d88e08f7febe3b4f6caa195cb8b9d2` | 0 |
| timeboost/db.go | 5093 | `99f23294fe952085150975cd45be058cdc6ae9c409a2b793226a6129c7868d8e` | 0 |
| timeboost/errors.go | 1115 | `470ef79775aad2f5ffb98b2e38aa324e33a4513f4c6d435e33056f5e1bf40d25` | 0 |
| timeboost/express_lane_service.go | 12509 | `abf8b32d900101dd5bfc2f9d246913cdb19c79351e5bf75756da3c382d8c13ed` | 0 |
| timeboost/express_lane_tracker.go | 11959 | `eb73abfa3243ce3bb1d689434e7246077b277b2b3380f6da76fc8e09da4a248f` | 0 |
| timeboost/redis_coordinator.go | 6735 | `985f3aad84eb678a964b6d8f198680b2aa994bc9b727f3cac253321523fc9291` | 0 |
| timeboost/roundtiminginfo.go | 5138 | `f8288ae03eb51e132d36af36aa98c0095c3c987098cc2fada1f9dd95da519202` | 0 |
| timeboost/s3_storage.go | 9047 | `5e26ff950f9c76b2774050b2e6ded674898b1c5f99e5c0a2e218224be884689b` | 0 |
| timeboost/schema.go | 759 | `ae64ca0f2b206d8ef310d8379ff8ac37af1ad8faa77d30516cee31fa8b86b49f` | 0 |
| timeboost/sequencer_endpoint_manager.go | 4544 | `7db8f57b0fe379905ac276167737a086885f758f1463c01789e6dbb22ba61a55` | 0 |
| timeboost/ticker.go | 1353 | `bd1330a62fe52da4a1f89f42872b11feb5b75114b845ada23aa69d9c55c809c7` | 0 |
| timeboost/types.go | 9793 | `302502193db3ce50f163e4dda6872491ba6907c10dcbbb3435e619da3fb593b5` | 0 |
| transactionfeed/config.go | 2569 | `c848a0307a9c99b4c599935ce4321598c80eb209d0f045ada5912a2a838e78a4` | 0 |
| transactionfeed/message.go | 4166 | `15dce65ba92c74d8a51fe490b07866cc7513b269016edcc3e0d5b2e2a74624b4` | 0 |
| transactionfeed/server.go | 8256 | `1352ae69511da5246893668cfdba7d84862a6e82820ad5e7e09940187ff1442e` | 0 |
| util/arbmath/bips.go | 2117 | `47106ad3c4cf26fdcc3a60e6c419cc1e8e47a627d025313636dd172dfad6430a` | 0 |
| util/arbmath/bits.go | 3469 | `0257f717385b87c46f2f0b028115622872cb298c820df1a7cd01a47b164cc22a` | 0 |
| util/arbmath/bold_math.go | 1054 | `edf21c4db3ec705abd48797377b212767537eaeaaf3437f43faeb63799a57a71` | 0 |
| util/arbmath/math.go | 11679 | `7b56cbdcda8acf3b3ab3bb718aa48213a430b0d96990ee20e4b5ba16f17c95a5` | 0 |
| util/arbmath/moving_average.go | 1128 | `c6db5fc05eeaa444f4cbb96dee446c7fecd6c16765a8796ada7fcb4df37153ff` | 0 |
| util/arbmath/time.go | 241 | `7e65a8945ab2ae9eaf2957026830cc522adead6ebee49235d1ac8443292df05e` | 0 |
| util/arbmath/uint24.go | 1383 | `72f7ae988607586d690f88737133744e0e06a012bd4664f499c395cdd44a2728` | 0 |
| util/blobs/blobs.go | 4508 | `7b378aed6e1aa89d1d66d4f9519b4d96b85d840f5c992df562cca55a7fa9f265` | 0 |
| util/colors/colors.go | 1341 | `50ca76535c64bb7afde44894127d26957991d7eb8140e8687fdb6a14b6da7b8c` | 0 |
| util/common.go | 306 | `a1fa0ccde8f6b80751a7974917d2d06404dbe92477f02db16ad954fbeec8f512` | 0 |
| util/containers/lru.go | 2490 | `a096333de2c1948c52bd2b226ef62913400fe0a6ba71e2f19e52e5af7b23c055` | 0 |
| util/containers/option_type.go | 805 | `8a13492195b7e12d0fe92caa244af7cd22aecc87c6f7cb0d683b106dcf831421` | 0 |
| util/containers/promise.go | 3022 | `2f985cb73cf781b43673c7a83a5aff218690ededa16d0d3fdae9f41889abd248` | 0 |
| util/containers/queue.go | 1236 | `d3b0b72a14351230222c000aee25dcccf33ed0077ca90758147693f737ee96cf` | 0 |
| util/containers/stack.go | 856 | `949e3674ccde455b2f8686cdfd59cbba6edd1478f15a0c6145c61cd5a465b0d1` | 0 |
| util/containers/syncmap.go | 964 | `1a7fd3c5f92db180ea342b2deb171aed38b82342030a441e44daf3b5e90231c2` | 0 |
| util/contracts/address_verifier.go | 2719 | `7c6abedf8d2381dd3fd78ccce154e10b70cbaf10e8eaef453998fac4a27664ac` | 0 |
| util/ctxhelper/ctxhelper.go | 544 | `e242e88bd54fa4efb05c7461951f50138b5783881c71b9da3efd92cd6ad9f8f3` | 0 |
| util/dbutil/dbutil.go | 1453 | `74753c0c7d9180d7380d2992697cdeeb6717e21a73a058a03a107941df2b992a` | 0 |
| util/floatmath/floatmath.go | 966 | `f924aed9356eabc8d574d5f9931992b4451ddc18260207a3d43ce1e5a1086bc4` | 0 |
| util/gasestimate.go | 654 | `f66f0c80a1fb24b06ba92a97d2fd88a11ec4046efda8144d2bb3dfbac4bd45be` | 0 |
| util/gzip/gzip_compression.go | 986 | `eeb53f69602949e5d3210781772ab4ca3a8afe9d0fdc30f5797bd14b79753e55` | 0 |
| util/headerreader/blob_client.go | 18182 | `d361dd60749e793519f0d5bdeebecf639f34763f17ec4698f36c83cc6aa9fe99` | 0 |
| util/headerreader/header_reader.go | 17123 | `9fda8080700d52bd4e8b1d7c83a97a4a46ba1495d1f654f228b224c5dbc1a87a` | 0 |
| util/httpclient/httpclient.go | 1527 | `4b77c1ef21e1a92c489747cc706fac2e6cadbcca17c9acc3ed3a3e4cdd2a45dd` | 0 |
| util/httperror/httperror.go | 567 | `92b92e73aee741533ddfabe4ce62c7b764d2d43b6099d7d484ac053cedbdc4a1` | 0 |
| util/iostat/iostat.go | 4105 | `e3722a92e36d93d9e1be0ecbb390a47b0a19510f1208d60ab0eb5f0f65c54277` | 0 |
| util/jsonapi/preimages.go | 4616 | `1701c804bdc2f07d70f00c3f6c16bf6443ee41142a1590e6fe3eacccde0bacba` | 0 |
| util/jsonapi/uint64_string.go | 744 | `3e9bebecda9a0fbb575969085e7974689d6104601aec32f5148127ec688121bc` | 0 |
| util/log.go | 2606 | `67e431107fae9c42bb396dd77b344277294ee1139b1025780e8c2e80f2a94bd0` | 0 |
| util/merkletree/merkleEventProof.go | 1875 | `bf551485bb6982ff65eb5bdf74be5d0f7dea6380645dac9fe6299ec9051225d1` | 0 |
| util/merkletree/merkleTree.go | 7383 | `7edb9cfce984c16470a82e2d1120f0637fce551616f5e977d047c853fecf65c6` | 0 |
| util/metricsutil/metricsutil.go | 423 | `32a01d0db4e858ccbd46dd0a381ac2c8ab685f969bdfb95c385400d666d30163` | 0 |
| util/normalizeGas.go | 572 | `8bd5b0e93437a15b44068b2a1339f027184025be49ae0ae8b5a7c10e0b0bbfa8` | 0 |
| util/pretty/pretty_printing.go | 731 | `cf69f772aa4b2cf10162802632f34e8ca7c7688904ad81dc66e9f1e0099cea95` | 0 |
| util/redisutil/redis_coordinator.go | 9129 | `342c342c99018118d0e750f09c63e3742507da8fd23a1fb31ed0304951c89581` | 0 |
| util/redisutil/redisutil.go | 6030 | `d2151fbe0eaaa5b759fa7aa9880ced9392d0e751fd18267be58f81fd97693a8b` | 0 |
| util/rpcclient/rpcclient.go | 9083 | `0cb202d0e5790d24dc4ccd7a90e5545082ba1ab56bfbb9a51b790c5aa3f6a53a` | 0 |
| util/rpcserver/rpcserver.go | 770 | `dacac4ee868d3d3f83dcb47b371e770fcd3ce34fbb25ef6f75860297fe2b3752` | 0 |
| util/runtime.go | 436 | `4a71625baa42e645a6102b0167845b1145d01a0c14fa9497b34fb433c46fcadb` | 0 |
| util/s3client/s3client.go | 3217 | `3ebbc3e2cbc3b896cf399bee8d7793f0c7ddc7b77e96d21f3b631efc7bd4f30b` | 0 |
| util/s3syncer/config.go | 3145 | `f5b13c2b1f5ecb4566f251fdf3865e68aaab354b1c8c893aa9f8f994bac5cc71` | 0 |
| util/s3syncer/s3syncertest/s3syncertest.go | 875 | `77ec072162bc55d751d1d0410e91cdf61b718186d1afa45cc8046794bc101a2a` | 0 |
| util/s3syncer/syncer.go | 6489 | `01c4b356488f25500ee614e34efe02522c210a7cba1663c3072e0531fcccf37f` | 0 |
| util/sharedmetrics/sharedmetrics.go | 747 | `c344879c165914ac0a43c4d4feace7726707e8f1e60120e5af0ed58f953819a5` | 0 |
| util/signature/datasigner.go | 443 | `510bffae8d84850312c73e0a13b7b773bd743beafab21f706892b9383590cf9b` | 0 |
| util/signature/sign_verify.go | 2743 | `92a9549841ca9771ac6818e9e6fec3c361ea276c7e87fabeabd96bc82fdd1f0d` | 0 |
| util/signature/simple_hmac.go | 4448 | `7559a2bb25fd61776090e54129b4548377daa60592af3ddcce421c34e1996338` | 1 |
| util/signature/verifier.go | 3758 | `21a3f94c7aa5be89eed7f1ecf25861c292f6336e818372026541acd0d69a764a` | 0 |
| util/sqsclient/queueclient.go | 2243 | `8c4a16f5118a7bfaae8824ffaca21742f272d9bba06d28c3566cf653d1383250` | 0 |
| util/sqsclient/queueclient_mock.go | 2155 | `4ceda754b480ce6b13f7fbc62eba002cd50076b6c2a6c02494babdd333bf4dcb` | 0 |
| util/sqsclient/sqsclient.go | 1431 | `0be93249f8c8d62e291aec3f01a1cd44e0e028eb386038851fc2e2693613d386` | 0 |
| util/stopwaiter/state/state.go | 2238 | `319dc7c02d0f0941291ebe8f11f794c11f93a4d8dac1bd1d68c63062f6b6278f` | 0 |
| util/stopwaiter/stoppable/stoppable.go | 506 | `aed5c8c35005a4c35ef1fc893abfd0568cd83a24469d3c1e73ac93324ca5bfe0` | 0 |
| util/stopwaiter/stopwaiter.go | 10030 | `600c0757547e7f6d33f7643b7e899d381f39883b5683c5daa251cfbb6298bbc5` | 0 |
| util/testhelpers/addresschecker.go | 921 | `8071b44a8f1ce6d0893aaad1738a8a4fbe13ddc094728b150619332a7280d151` | 0 |
| util/testhelpers/env/env.go | 1339 | `c30288ca752d7ff25342be6212720aba2d8404bb935db730bea94035342e890f` | 0 |
| util/testhelpers/flag/flag.go | 2806 | `0bbb67c5eace539063b88627efc61e42117e7c8ad6be6f1332cf86bd208d809d` | 0 |
| util/testhelpers/github/releases.go | 2978 | `2c8e28a93c6f315ea46373336c98fc451fa007a32b5215cfeb440dee816eadf6` | 0 |
| util/testhelpers/port.go | 820 | `e714bf4820785932fa8537daadf582adf2ff3d025bfc7b003ae819b2c74f5f6f` | 0 |
| util/testhelpers/pseudorandom.go | 1066 | `e79ae1b8c6f04987ffff9322f02fee2cee93fc710a0f82011371efec926696b5` | 0 |
| util/testhelpers/stackconfig.go | 1353 | `3deb57ba80c82f4486c2c7595dec0b20e07ce48541453bdc5a0eb6225b960800` | 0 |
| util/testhelpers/testhelpers.go | 4657 | `4ca4b20341898c3ae91f858e5ccbc40f38bf87e1daa136bd686cd82dbd9a1472` | 0 |
| util/warmbuffer/warmbuffer.go | 1607 | `8504dfa60f929cd1a61895c6592efabaad7f8e36645a8032fc5b8b8cea05a135` | 0 |
| validator/client/redis/producer.go | 10042 | `a72b61d571f4522f00fd0753a5d7891ce9c9ac710767296269c669a3f89ef02e` | 0 |
| validator/client/validation_client.go | 11204 | `065980abe347e8274d75d51b4f4d958d0ecd77ac300006d58c111028170ef15e` | 0 |
| validator/execution_state.go | 4222 | `eda817598b70069caab1b0c1a778b5bb0f9ff8cff3c0741ee071e17829279e78` | 0 |
| validator/inputs/writer.go | 4533 | `2ac4f8c3f1a0a9346e450e7c046636cac0040634317c6b91e11222c4f4730be6` | 0 |
| validator/interface.go | 1900 | `fa7d40703837b294eb6b911f34ef806662ed3255fea5a5c004af40dec823688f` | 0 |
| validator/proofenhancement/proof_enhancer.go | 7217 | `240c60284f1e65f62f4d02f03ece8a9ef2b0e01b40ef6aaecf8e68fb8d4d381d` | 0 |
| validator/proofenhancement/readpreimage_proof_enhancer.go | 3652 | `6e3126ecc6395d761fba0a84cc1cdf506ad96b0b685cd3cadb9a050989c17dd5` | 0 |
| validator/proofenhancement/validatecertificate_proof_enhancer.go | 2907 | `e1b65fe0ebd769389a11da2b9beffbb0b072bf2969cad9efb35bc749dcce4fb1` | 0 |
| validator/retry_wrapper/retry_wrapper.go | 2425 | `9797345bc1cb4baae3e704c2c9360049e1bf60828af9fcf6b61d5d2e8723ebdd` | 0 |
| validator/server_api/json.go | 5541 | `648c1c2fae20308d1ca5f13c7b2f12f63c446630ba99ed8c5764902c9ab96d01` | 0 |
| validator/server_arb/bold_machine.go | 4344 | `101e7ef583fc7b6c734b8effd496e3d914a7ad5afcbf45b96bd7faf427460664` | 0 |
| validator/server_arb/execution_run.go | 5808 | `46651d28e7aaaaf2df2f1f5cae3f9096f96fad9fcbea4ebd051954303f466aab` | 0 |
| validator/server_arb/machine.go | 11643 | `041f79129a1dabedca81c79a70d15dce7716536c06ebef7d577f4f1a27e6e640` | 0 |
| validator/server_arb/machine_cache.go | 8163 | `132c3cb95aee6fb1398e2f676ab280bb6398b11f059747cc2a9e45b60daff669` | 0 |
| validator/server_arb/machine_loader.go | 1580 | `0ba62d70feb7a4b73fad90a9aaf55693929e4ecee88d6a3dcb666bd4c8d7b5f8` | 0 |
| validator/server_arb/nitro_machine.go | 2591 | `f0f4fb33693defe1a69b8223822d1ec72bb926826fcff0af586c4b2e9a71c3b2` | 0 |
| validator/server_arb/preimage_resolver.go | 496 | `70a9fcf4ae5001e629ae00d3e41041582c0b6d9b1912e601d7199a5b031a1adc` | 0 |
| validator/server_arb/prover_interface.go | 2238 | `9f66e352841a32e3c26ed76d7de2215bb3fbd9027f3b86329148e9b45bf0fa85` | 0 |
| validator/server_arb/validator_spawner.go | 9133 | `00292e82ea82fbc61f74ff466591ebc489920d6fd9f176dd935226df05d5aac0` | 0 |
| validator/server_common/machine_loader.go | 1884 | `05ca6551f40a65f9306cee8df21eb5c07459818c0e0355a82534ae07da70f330` | 0 |
| validator/server_common/machine_locator.go | 3318 | `2fc711c082e74afabf8fe230ef9eec80b89fa3aabaa1bd3c764ad6c71908e7c9` | 0 |
| validator/server_common/valrun.go | 651 | `522519709f4c81090ed586169bc72b253b6a888902aaa9abbfcdd3cb73c36a12` | 0 |
| validator/server_jit/jit_machine.go | 8470 | `b538f8810f05aac44da39393dc300331f6c6a68a772465071dbb974e9560526e` | 0 |
| validator/server_jit/machine_loader.go | 2574 | `663e1b1f253d1128af3dc84cc840727f9118588003b45d863304e5e7af1f591f` | 0 |
| validator/server_jit/spawner.go | 4282 | `371f78622367d6e491affba00d0eeea3ea744abec23fa556cde82f23ecaccd4c` | 0 |
| validator/timeout.go | 1397 | `58382ebd4361d7f8ce44303b7546981571c1cf75358846fc429eafd1cc22c3ac` | 0 |
| validator/utils.go | 567 | `f8c561c998f958dc442c1f3f0cc2c11621784094c6211608df90cdebd659323b` | 0 |
| validator/validation_entry.go | 963 | `128ddf09b1f119a725c5e755a89320c2bffc360c2078ec773508f3969ee60bc1` | 0 |
| validator/valnode/redis/consumer.go | 12264 | `0226329dd9ec69d7f2fc1b889cfe09f0708b0e2a7177e46852ba5fc96ad242d9` | 0 |
| validator/valnode/validation_api.go | 8402 | `3999bd68742effb024e97440eb42ef8135b92d0cd99347d3b07a7001b88f6d7f` | 0 |
| validator/valnode/valnode.go | 5895 | `d87b9613b29453832bf071d1deef80d7f0c93f076a542925532f7fe4e390542c` | 0 |
| wavmio/common.go | 1107 | `513efdce3ced38efbd9b01a5e62afb8a2aa35612b454cab1efe755ce4da4717d` | 1 |
| wavmio/higher.go | 2678 | `b877afd88f70bc8c9f9c26f25ff65b0f2c1216c252b1887e783139fc8b92c904` | 0 |
| wavmio/native.go | 4248 | `fc79cabcdd6673d81b5e74917334fd64145e03d9948daa9728702d9d784ae038` | 0 |
| wavmio/raw.go | 1147 | `5d2adba61ef4c3b394b2bb2f1a0a32f7d78db74a04b144a532d6dade7bc1d3fd` | 0 |
| wsbroadcastserver/clientconnection.go | 9029 | `5ae62de8238ae0c6a4a8380440af447d0aa02602f77e5856b91613037808e126` | 0 |
| wsbroadcastserver/clientmanager.go | 12484 | `330109bbdcbf0fedc8b21b94e85ecd5c72cafde74b745149da92edeb6c8ac2b1` | 0 |
| wsbroadcastserver/connectionlimiter.go | 5474 | `2ce2f501da40a112d0a0c518dccbce488fbec8be478aff42d0835aec270da12e` | 0 |
| wsbroadcastserver/dictionary.go | 20847 | `06d0205d4ed365da858d611aafd3d75d687ffd11beb000ffb03618a288d6bfd6` | 0 |
| wsbroadcastserver/utils.go | 3706 | `22473003e84a1cf3944ab3aac77920da413dac1697d6d2beb933ee610a1f653e` | 0 |
| wsbroadcastserver/wsbroadcastserver.go | 20388 | `d25456d3f9803ab1648153bcab36c04741efaaaa917d46261363f3c0ea4f8e63` | 0 |
| zeroheavy/zeroheavy.go | 4220 | `856df2a15bb6957c904779b88b5b665f9d3a5ce049f9a3dfdd6277c3b59fb01f` | 0 |
