# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** safe-smart-account @ 247b8ce3bdbf · Safe — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-28 12:53 UTC |
| Версия отчёта | 1 |
| Запуск аудита | b1c7d303-5af9-48a1-91d2-59255d391677 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Финансовая организация |
| SHA-256 содержимого | `0da61727ced613d6767f96b37828d8b962f93bc2e81d7a8c2e0fab5270116a40` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **0**
- Средняя: **3**
- Низкая: **3**
- Информационная: **2**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 0
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 2
- Долгосрочный постквантовый риск: 1
- Рекомендация по улучшению: 4
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/safe-global/safe-smart-account> @ `247b8ce3bdbf204a120e77f5b369d137424ddc58` — ссылки в доказательствах открывают строки на этом коммите.

77 файлов, всего 722848 байт, редактирований: 6; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 20 | .solcover.js: 15 lines scanned with 16 rule patterns and 122 registry patterns; eslint.config.mjs: 20 lines scanned with 16 rule patterns and 122 registry patterns; hardhat.config.ts: 134 lines scanned with 16 rule patterns and 122 registry patterns |
| smart_contracts | проверено | 54 | certora/harnesses/ExtensibleFallbackHandlerHarness.sol: built-in Solidity pattern checks; certora/harnesses/SafeHarness.sol: built-in Solidity pattern checks; contracts/Safe.sol: built-in Solidity pattern checks |
| slither | не проверено | 54 | slither is not installed on the server (pip install slither-analyzer + solc) |
| dependencies | проверено | 3 | certora/requirements.txt: 1 dependencies parsed (1 pinned); package-lock.json: 831 dependencies parsed (831 pinned); package.json: 30 dependencies parsed (0 pinned) |
| secrets | проверено | 4 | contracts/Safe.sol: 2 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); contracts/handler/CompatibilityFallbackHandler.sol: 2 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); contracts/handler/extensible/SignatureVerifierMuxer.sol: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| osv_advisories | проверено | 1 | 736 pinned packages queried at OSV.dev; 45 affected (45 of them only in development or build dependencies) |
| osv_advisories | Недостаточность данных | 2 | npm/axios@0.21.4: 23 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest; npm/axios@1.13.2: 35 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- slither — не проверено: 54 (примеры: slither is not installed on the server (pip install slither-analyzer + solc))
- osv_advisories — Недостаточность данных: 2 (примеры: npm/axios@0.21.4: 23 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest; npm/axios@1.13.2: 35 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest)

## 5. Краткое описание архитектуры

Static review of the source tree safe-smart-account at 247b8ce3bdbf204a120e77f5b369d137424ddc58. 77 files analysed; of 236 files, 81 are test, fuzzing, benchmark or example code and were left out, 78 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **94** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 15.2%

## 7. Подробное описание находок

### QSI-2026-05092 — Прямое использование ecrecover в certora/harnesses/SafeHarness.sol

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:certora/harnesses/SafeHarness.sol`
- Источник данных: certora/harnesses/SafeHarness.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-28 12:53 UTC
- Балл приоритета: 43.0 / 100
- CVSS v3.1: неприменимо

ecrecover в строка 32. (см. SWC-117/SWC-121)

**Возможные последствия.** Без проверок s-значения/нулевого адреса и nonce подписи могут быть изменяемыми или повторно используемыми. ecrecover основан на secp256k1 ECDSA (долгосрочно квантово-уязвим).

**Шаги воспроизведения.**

```
Откройте строка 32 в предоставленном файле certora/harnesses/SafeHarness.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [certora/harnesses/SafeHarness.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/certora/harnesses/SafeHarness.sol#L32) · line 32 · SHA-256 e416f88cf9d56a07a6ec143b9f07aa6080e9077660994d8459f67a4f2d8d05f0_

```
   30 |             currentOwner = address(uint160(uint256(r)));
   31 |         } else if (v > 30) {
   32 |             currentOwner = ecrecover(keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", dataHash)), v - 4, r, s);
   33 |         } else {
   34 |             currentOwner = ecrecover(dataHash, v, r, s);
```

_file_excerpt · [certora/harnesses/SafeHarness.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/certora/harnesses/SafeHarness.sol#L34) · line 34 · SHA-256 3a44416872ad9ffc133c483f76208b50cb892390311baf7040e8c9825678d4ef_

```
   32 |             currentOwner = ecrecover(keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", dataHash)), v - 4, r, s);
   33 |         } else {
   34 |             currentOwner = ecrecover(dataHash, v, r, s);
   35 |         }
   36 |     }
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin ECDSA.recover с разделением доменов EIP-712 и nonce.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-05093 — Непроверенный низкоуровневый вызов в certora/harnesses/SafeHarness.sol

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:certora/harnesses/SafeHarness.sol`
- Источник данных: certora/harnesses/SafeHarness.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-28 12:53 UTC
- Балл приоритета: 43.0 / 100
- CVSS v3.1: неприменимо

Результат низкоуровневого вызова не проверяется в строка 88. (см. SWC-104)

**Возможные последствия.** Неудачные вызовы остаются незамеченными, что ведёт к несогласованному состоянию.

**Шаги воспроизведения.**

```
Откройте строка 88 в предоставленном файле certora/harnesses/SafeHarness.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [certora/harnesses/SafeHarness.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/certora/harnesses/SafeHarness.sol#L88) · line 88 · SHA-256 8e885c80b50cce328ce145786c0515613599e25c3226c2115c450b873c5e9506_

```
   86 | 
   87 |     function callDummyHandler(bytes4 selector) public {
   88 |         address(this).call(abi.encodeWithSelector(selector));
   89 |     }
   90 | 
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Проверяйте возвращаемое значение или используйте OpenZeppelin Address.sendValue / functionCall.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-05091 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (3 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: certora/harnesses/SafeHarness.sol
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:53 UTC
- Балл приоритета: 39.6 / 100
- CVSS v3.1: неприменимо

5 упоминаний ECDSA в 3 файл(ах), например certora/harnesses/SafeHarness.sol:32. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте certora/harnesses/SafeHarness.sol:32 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [certora/harnesses/SafeHarness.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/certora/harnesses/SafeHarness.sol#L32) · line 32 · SHA-256 e416f88cf9d56a07a6ec143b9f07aa6080e9077660994d8459f67a4f2d8d05f0_

```
   30 |             currentOwner = address(uint160(uint256(r)));
   31 |         } else if (v > 30) {
   32 |             currentOwner = ecrecover(keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", dataHash)), v - 4, r, s);
   33 |         } else {
   34 |             currentOwner = ecrecover(dataHash, v, r, s);
```

_file_excerpt · [certora/harnesses/SafeHarness.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/certora/harnesses/SafeHarness.sol#L34) · line 34 · SHA-256 3a44416872ad9ffc133c483f76208b50cb892390311baf7040e8c9825678d4ef_

```
   32 |             currentOwner = ecrecover(keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", dataHash)), v - 4, r, s);
   33 |         } else {
   34 |             currentOwner = ecrecover(dataHash, v, r, s);
   35 |         }
   36 |     }
```

_file_excerpt · [contracts/Safe.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/Safe.sol#L403) · line 403 · SHA-256 be7c18bdbce908e503f1c899b447b921a9a3880ec49ae5d3d5ea33045ae5aec7_

```
  401 |                 // If `v > 30` then default `v` (27, 28) has been adjusted to encode an `eth_sign` signature.
  402 |                 // To support `eth_sign` and similar we adjust `v` and hash the `dataHash` with the EIP-191 message prefix before applying `ecrecover`.
  403 |                 currentOwner = ecrecover(keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", dataHash)), uint8(v - 4), r, s);
  404 |             } else {
  405 |                 // Default is `ecrecover` for the provided `dataHash`.
```

_file_excerpt · [contracts/Safe.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/Safe.sol#L406) · line 406 · SHA-256 361e3d349b65a6cf85ae3cc313307e936af7349c06d154fd2e39b0f84d9b4714_

```
  404 |             } else {
  405 |                 // Default is `ecrecover` for the provided `dataHash`.
  406 |                 currentOwner = ecrecover(dataHash, uint8(v), r, s);
  407 |             }
  408 |             if (currentOwner <= lastOwner || owners[currentOwner] == address(0) || currentOwner == SENTINEL_OWNERS)
```

_file_excerpt · [src/utils/execution.ts](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/src/utils/execution.ts#L113) · line 113 · SHA-256 a189cee56b6fb9aa095cce0a3b5099d5f195bc22ad24f9e656e950cde6a753c0_

```
  112 |         signer: signerAddress,
  113 |         data: await signer.signTypedData({ verifyingContract: safeAddress, chainId: cid }, EIP712_SAFE_TX_TYPE, safeTx),
  114 |     };
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05094 — Плавающая версия компилятора (>=0.7.0 <0.9.0) в 50 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.7.0 <0.9.0`
- Источник данных: contracts/Safe.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-28 12:53 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.7.0 <0.9.0 в 50 файл(ах), впервые в contracts/Safe.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте contracts/Safe.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/Safe.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/Safe.sol#L2) · line 2 · SHA-256 e88d87460c9e31999f74a385f7211f2a3d247576a8d5e7321fb8ab7610726718_

```
    1 | // SPDX-License-Identifier: LGPL-3.0-only
    2 | pragma solidity >=0.7.0 <0.9.0;
    3 | 
    4 | import {FallbackManager} from "./base/FallbackManager.sol";
```

_file_excerpt · [contracts/SafeL2.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/SafeL2.sol#L2) · line 2 · SHA-256 15c9f4200fba8411f86f51e4783fa81326529bbdedb3a85d3d69541f7783cbd7_

```
    1 | // SPDX-License-Identifier: LGPL-3.0-only
    2 | pragma solidity >=0.7.0 <0.9.0;
    3 | 
    4 | // The import is used in the @inheritdoc, false positive
```

_file_excerpt · [contracts/accessors/SimulateTxAccessor.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/accessors/SimulateTxAccessor.sol#L2) · line 2 · SHA-256 af5c840a272a5dab66211c10e60731181ce16ddf9518928201829db6baacef22_

```
    1 | // SPDX-License-Identifier: LGPL-3.0-only
    2 | pragma solidity >=0.7.0 <0.9.0;
    3 | 
    4 | import {Executor, Enum} from "../base/Executor.sol";
```

_file_excerpt · [contracts/base/Executor.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/base/Executor.sol#L2) · line 2 · SHA-256 c8eec2e4083c16adc0bf1e7eea14ca740cca55b1f5676d9cb4a355576c6800c6_

```
    1 | // SPDX-License-Identifier: LGPL-3.0-only
    2 | pragma solidity >=0.7.0 <0.9.0;
    3 | import {Enum} from "../interfaces/Enum.sol";
    4 | 
```

_file_excerpt · [contracts/base/FallbackManager.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/base/FallbackManager.sol#L2) · line 2 · SHA-256 f0696aecda7f2d4390ae2470ec51a56b07a6565df8ff4be3d0a6524628ffb825_

```
    1 | // SPDX-License-Identifier: LGPL-3.0-only
    2 | pragma solidity >=0.7.0 <0.9.0;
    3 | 
    4 | import {SelfAuthorized} from "../common/SelfAuthorized.sol";
```

_file_excerpt · [contracts/base/GuardManager.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/base/GuardManager.sol#L3) · line 3 · SHA-256 2f8023b221054a49f2c7512edfc7f592b58e8c7053625f4af7216c1251f2bd74_

```
    1 | // SPDX-License-Identifier: LGPL-3.0-only
    2 | /* solhint-disable one-contract-per-file */
    3 | pragma solidity >=0.7.0 <0.9.0;
    4 | 
    5 | import {SelfAuthorized} from "./../common/SelfAuthorized.sol";
```

_file_excerpt · [contracts/base/ModuleManager.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/base/ModuleManager.sol#L3) · line 3 · SHA-256 6fd7193061543bd17b02478604b1e136ee186957854410e2482d2fd544017605_

```
    1 | // SPDX-License-Identifier: LGPL-3.0-only
    2 | /* solhint-disable one-contract-per-file */
    3 | pragma solidity >=0.7.0 <0.9.0;
    4 | import {SelfAuthorized} from "./../common/SelfAuthorized.sol";
    5 | import {IERC165} from "./../interfaces/IERC165.sol";
```

_file_excerpt · [contracts/base/OwnerManager.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/base/OwnerManager.sol#L2) · line 2 · SHA-256 43281753a6047468ec8145eb656909a730f9b1bb7e3a6388e81a52f7cc0c1714_

```
    1 | // SPDX-License-Identifier: LGPL-3.0-only
    2 | pragma solidity >=0.7.0 <0.9.0;
    3 | 
    4 | import {EIP7702} from "../common/EIP7702.sol";
```

_file_excerpt · [contracts/common/EIP7702.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/common/EIP7702.sol#L2) · line 2 · SHA-256 4664953c5c56b94f26d9fa72c0444fa3beca0a4b56a03b25c953cc22e4ff357f_

```
    1 | // SPDX-License-Identifier: LGPL-3.0-only
    2 | pragma solidity >=0.7.0 <0.9.0;
    3 | 
    4 | /**
```

_file_excerpt · [contracts/common/EIP7951.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/common/EIP7951.sol#L2) · line 2 · SHA-256 4664953c5c56b94f26d9fa72c0444fa3beca0a4b56a03b25c953cc22e4ff357f_

```
    1 | // SPDX-License-Identifier: LGPL-3.0-only
    2 | pragma solidity >=0.7.0 <0.9.0;
    3 | 
    4 | /**
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-05095 — Плавающая версия компилятора (>=0.5.0 <0.9.0) в 1 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.5.0 <0.9.0`
- Источник данных: contracts/interfaces/ViewStorageAccessible.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-28 12:53 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.5.0 <0.9.0 в 1 файл(ах), впервые в contracts/interfaces/ViewStorageAccessible.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте contracts/interfaces/ViewStorageAccessible.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/interfaces/ViewStorageAccessible.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/interfaces/ViewStorageAccessible.sol#L2) · line 2 · SHA-256 983f9c51447ea383d35f05b85564c2a8e5c2eb17d9109edf52dad4e588c49ca6_

```
    1 | // SPDX-License-Identifier: LGPL-3.0-only
    2 | pragma solidity >=0.5.0 <0.9.0;
    3 | 
    4 | /**
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-05096 — Плавающая версия компилятора (>=0.7.4 <0.9.0) в 1 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.7.4 <0.9.0`
- Источник данных: contracts/libraries/SafeStorage.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-28 12:53 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.7.4 <0.9.0 в 1 файл(ах), впервые в contracts/libraries/SafeStorage.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте contracts/libraries/SafeStorage.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [contracts/libraries/SafeStorage.sol](https://github.com/safe-global/safe-smart-account/blob/247b8ce3bdbf204a120e77f5b369d137424ddc58/contracts/libraries/SafeStorage.sol#L2) · line 2 · SHA-256 11c26335bd27fe89dda40165c6fea219ab0021d1c0b45a5bace32a1322a9ae25_

```
    1 | // SPDX-License-Identifier: LGPL-3.0-only
    2 | pragma solidity >=0.7.4 <0.9.0;
    3 | 
    4 | /**
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-05098 — 174 бюллетеней в 45 пакет(ах) npm, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:npm:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:53 UTC
- Балл приоритета: 17.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 174 бюллетеней (95 с оценкой high или critical) для 45 пакет(ов) npm, которые подтягивают только инструменты разработки или сборки (package-lock.json): например, @fastify/busboy@2.1.1 [dev]: GHSA-gxm5-99cw-xjw9, GHSA-x8mw-p69m-v3mx; @humanfs/node@0.16.7 [dev]: GHSA-p498-v437-472g; @isaacs/brace-expansion@5.0.0 [dev]: GHSA-7h2j-956f-4vf2; @openzeppelin/contracts@3.4.2 [dev]: GHSA-7grf-83vw-6f5x, GHSA-88g8-f5mf-f5rj, GHSA-mx2q-35m2-x2rh; adm-zip@0.4.16 [dev]: GHSA-7q85-xj36-vmfc, GHSA-8238-w5pm-2374, GHSA-c6fg-446q-cg94, GHSA-j5f4-cc29-5x44, GHSA-p634-w6r4-rjp2, GHSA-rcw4-f5rp-g42v, GHSA-xcpc-8h2w-3j85. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в package-lock.json.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · package-lock.json · SHA-256 246d1fc835bf80bae1bffb3a9be4793d552a4248f1d02f0cec4af5e423ea4959_

```
@fastify/busboy@2.1.1 [dev]: GHSA-gxm5-99cw-xjw9, GHSA-x8mw-p69m-v3mx
@humanfs/node@0.16.7 [dev]: GHSA-p498-v437-472g
@isaacs/brace-expansion@5.0.0 [dev]: GHSA-7h2j-956f-4vf2
@openzeppelin/contracts@3.4.2 [dev]: GHSA-7grf-83vw-6f5x, GHSA-88g8-f5mf-f5rj, GHSA-mx2q-35m2-x2rh
adm-zip@0.4.16 [dev]: GHSA-7q85-xj36-vmfc, GHSA-8238-w5pm-2374, GHSA-c6fg-446q-cg94, GHSA-j5f4-cc29-5x44, GHSA-p634-w6r4-rjp2, GHSA-rcw4-f5rp-g42v, GHSA-xcpc-8h2w-3j85
ajv@6.12.6 [dev]: GHSA-2g4f-4pwh-qvx6
ajv@8.17.1 [dev]: GHSA-2g4f-4pwh-qvx6
axios@0.21.4 [dev]: GHSA-3g43-6gmg-66jw, GHSA-3p68-rc4w-qgx5, GHSA-43fc-jf86-j433, GHSA-5c9x-8gcm-mpgx, GHSA-62hf-57xw-28j9, GHSA-6chq-wfr3-2hj9, GHSA-7q8q-rj6j-mhjq, GHSA-898c-q2cr-xwhg, GHSA-fvcv-3m26-pcqx, GHSA-hfxv-24rg-xrqf, GHSA-j5f8-grm9-p9fc, GHSA-jr5f-v2jv-69x6, GHSA-m7pr-hjqh-92cm, GHSA-mmx7-hfxf-jppx, GHSA-p92q-9vqr-4j8v, GHSA-pf86-5x62-jrwf, GHSA-pjwm-pj3p-43mv, GHSA-pmwg-cvhr-8vh7, GHSA-vf2m-468p-8v99, GHSA-w9j2-pvgh-6h63
axios@1.13.2 [dev]: GHSA-35jp-ww65-95wh, GHSA-3g43-6gmg-66jw, GHSA-3p68-rc4w-qgx5, GHSA-3pq3-5fj3-cg6v, GHSA-3w6x-2g7m-8v23, GHSA-42h9-826w-cgv3, GHSA-43fc-jf86-j433, GHSA-445q-vr5w-6q77, GHSA-4hqw-qxg8-jxx2, GHSA-542g-h47m-68v8, GHSA-5c9x-8gcm-mpgx, GHSA-62hf-57xw-28j9, GHSA-6chq-wfr3-2hj9, GHSA-777c-7fjr-54vf, GHSA-7q8q-rj6j-mhjq, GHSA-898c-q2cr-xwhg, GHSA-9fr6-4gfg-395g, GHSA-fvcv-3m26-pcqx, GHSA-hfxv-24rg-xrqf, GHSA-j5f8-grm9-p9fc
bn.js@4.11.6 [dev]: GHSA-378v-28hj-76wf
bn.js@4.12.2 [dev]: GHSA-378v-28hj-76wf
bn.js@5.2.2 [dev]: GHSA-378v-28hj-76wf
brace-expansion@1.1.12 [dev]: GHSA-3jxr-9vmj-r5cp, GHSA-6j4f-fj2g-mc7p, GHSA-f886-m6hf-6m8v, GHSA-mh99-v99m-4gvg, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895
brace-expansion@2.0.2 [dev]: GHSA-3jxr-9vmj-r5cp, GHSA-6j4f-fj2g-mc7p, GHSA-f886-m6hf-6m8v, GHSA-mh99-v99m-4gvg, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895
cookie@0.4.2 [dev]: GHSA-pxg6-pf52-xh8x
diff@4.0.2 [dev]: GHSA-73rr-hh4g-fpgx
diff@5.2.0 [dev]: GHSA-73rr-hh4g-fpgx
elliptic@6.5.4 [dev]: GHSA-434g-2637-qmqr, GHSA-49q7-c7j4-3p7m, GHSA-848j-6mx2-7j84, GHSA-977x-g7h5-7qgw, GHSA-f7q4-pwc6-w24p, GHSA-fc9h-whq2-v747, GHSA-vjh7-7g9h-fjfh
elliptic@6.6.1 [dev]: GHSA-848j-6mx2-7j84
fast-uri@3.1.0 [dev]: GHSA-333x-w4r6-6crp, GHSA-4c8g-83qw-93j6, GHSA-7p8r-x3mc-p8w7, GHSA-f65p-4m7j-42xc, GHSA-hrr3-gc8f-f4qj, GHSA-jqff-g426-hqxp, GHSA-q3j6-qgpj-74h6, GHSA-qw65-cvwx-89v3, GHSA-v2hh-gcrm-f6hx, GHSA-v39h-62p7-jpjc, GHSA-w74x-v6f9-j3xg, GHSA-xhq7-xmqj-769h
flatted@3.3.3 [dev]: GHSA-25h7-pfq9-p65f, GHSA-rf6f-7fwh-wjgh
follow-redirects@1.15.11 [dev]: GHSA-r4q5-vmmm-2653
form-data@4.0.5 [dev]: GHSA-hmw2-7cc7-3qxx
handlebars@4.7.8 [dev]: GHSA-2qvq-rjwj-gvw9, GHSA-2w6w-674q-4c4q, GHSA-3mfm-83xf-c92r, GHSA-442j-39wm-28r2, GHSA-7rx3-28cr-v5wh, GHSA-8r5x-fm3f-whwj, GHSA-9cx6-37pm-9jff, GHSA-p8wg-vrv2-v86f, GHSA-xhpv-hc6g-r9c6, GHSA-xjpj-3mr7-gcpf, GHSA-xw65-4hp5-5hc7
http-cache-semantics@4.2.0 [dev]: GHSA-ch52-4w7c-c8xp
immutable@4.3.7 [dev]: GHSA-v56q-mh7h-f735, GHSA-wf6x-7x77-mvgw, GHSA-xvcm-6775-5m9r
js-yaml@3.14.2 [dev]: GHSA-2883-xcg3-v3hh, GHSA-52cp-r559-cp3m, GHSA-5p4m-2wfm-xmqj, GHSA-h67p-54hq-rp68
js-yaml@4.1.1 [dev]: GHSA-2883-xcg3-v3hh, GHSA-52cp-r559-cp3m, GHSA-5p4m-2wfm-xmqj, GHSA-h67p-54hq-rp68
lodash@4.17.21 [dev]: GHSA-f23m-r3pf-42rh, GHSA-r5fr-rjxr-66jc, GHSA-xxjr-mmjv-4gpg
minimatch@10.1.1 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
minimatch@3.1.2 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
minimatch@5.1.6 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
minimatch@9.0.5 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
pbkdf2@3.1.5 [dev]: GHSA-477h-4r7f-fvrx
picomatch@2.3.1 [dev]: GHSA-3v7f-55p6-f55p, GHSA-c2c7-rcm5-vvqj
picomatch@4.0.3 [dev]: GHSA-3v7f-55p6-f55p, GHSA-c2c7-rcm5-vvqj
serialize-javascript@6.0.2 [dev]: GHSA-5c6j-r48x-rmvq, GHSA-m5mm-p8h7-m29v, GHSA-qj8w-gfj5-8c6v
tmp@0.0.33 [dev]: GHSA-52f5-9888-hmc6, GHSA-ph9p-34f9-6g65
undici@5.29.0 [dev]: GHSA-2m5v-pch6-74hx, GHSA-2mjp-6q6p-2qxm, GHSA-35p6-xmwp-9g52, GHSA-4992-7rv2-5pvq, GHSA-8xcm-r25x-g524, GHSA-9fm3-97px-rjf6, GHSA-g8m3-5g58-fq7m, GHSA-g9mf-h72j-4rw9, GHSA-m8rv-5g2x-5cg5, GHSA-p88m-4jfj-68fv, GHSA-qrxm-fqhp-jwvm, GHSA-r53p-7pc4-xj5r, GHSA-v3r7-h72x-cjcm, GHSA-v9p9-hfj2-hcw8, GHSA-vrm6-8vpv-qv8q, GHSA-vxpw-j846-p89q
uuid@8.3.2 [dev]: GHSA-w5hq-g745-h8pq
ws@7.4.6 [dev]: GHSA-3h5v-q93c-6h6q, GHSA-96hv-2xvq-fx4p
ws@7.5.10 [dev]: GHSA-96hv-2xvq-fx4p
ws@8.17.1 [dev]: GHSA-58qx-3vcg-4xpx, GHSA-96hv-2xvq-fx4p
ws@8.18.0 [dev]: GHSA-58qx-3vcg-4xpx, GHSA-96hv-2xvq-fx4p
ws@8.18.3 [dev]: GHSA-58qx-3vcg-4xpx, GHSA-96hv-2xvq-fx4p
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05097 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:53 UTC
- Балл приоритета: 14.5 / 100
- CVSS v3.1: неприменимо

В 3 манифестах зависимостей QSI нашёл криптобиблиотеки (@noble/curves, @noble/hashes, @noble/secp256k1, elliptic, ethers, secp256k1), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · certora/requirements.txt, package-lock.json, package.json · SHA-256 47e156b611a62a94da8b2ebeeacd5c7d245cbbdc38b44af530ee4ffe425233ff_

```
Crypto libraries: @noble/curves, @noble/hashes, @noble/secp256k1, elliptic, ethers, secp256k1
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
| **подпись транзакций и сообщений** | ECDSA (3) | QSI-2026-05091 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | ECDSA (5) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (8) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (8) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- slither: 54 (примеры: slither is not installed on the server (pip install slither-analyzer + solc))
- osv_advisories: 2 (примеры: npm/axios@0.21.4: 23 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest; npm/axios@1.13.2: 35 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest)

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-05092 | Используйте OpenZeppelin ECDSA.recover с разделением доменов EIP-712 и nonce. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P2 | QSI-2026-05093 | Проверяйте возвращаемое значение или используйте OpenZeppelin Address.sendValue / functionCall. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-05091 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-05094 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-05095 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-05096 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-05091 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05098 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |

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
19. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
20. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
21. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
22. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)
23. Smart Contract Weakness Classification (SWC) Registry — SWC community (no longer actively maintained). <https://swcregistry.io/> (historic reference; still widely cited)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| Keccak-256 | Keccak-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 8 | 8 | certora/harnesses/SafeHarness.sol:32; contracts/Safe.sol:396; contracts/handler/CompatibilityFallbackHandler.sol:52 |
| Crypto library | 1.2.0 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 1.2.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 1.3.2 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 1.4.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 1.4.2 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 1.7.1 | @noble/secp256k1 (noble-curves) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 1.7.2 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 1.8.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 1.8.2 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 1.9.1 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 1.9.7 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 2.0.1 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 2.0.1 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 4.0.4 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 5.7.2 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 5.8.0 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 6.15.0 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 6.5.4 | elliptic (elliptic (Node)) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 6.6.1 | elliptic (elliptic (Node)) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | ^2.0.1 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | package.json |
| ECDSA | secp256k1 (ecrecover) |  | уязвим (Шор) | допустимо | 4 | 4 | certora/harnesses/SafeHarness.sol:32; certora/harnesses/SafeHarness.sol:34; contracts/Safe.sol:403 |
| ECDSA |  |  | уязвим (Шор) | допустимо | 1 | 1 | src/utils/execution.ts:113 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| .solcover.js | 433 | `e082bfb212d25c3367596453ba28440137a54a63b8ff8072b5e004fb98629686` | 0 |
| certora/harnesses/ExtensibleFallbackHandlerHarness.sol | 368 | `a23d35cd9283f8262742377b7862f63c10aeeec1964f31b610dc35e53ea9f911` | 0 |
| certora/harnesses/SafeHarness.sol | 3751 | `0c6a4b08571e47ad101a82574a077630f939562100cb09dec20dda1a8f7cc401` | 0 |
| certora/requirements.txt | 20 | `138d8afeb220dd3aadad0b7221d49d76c3ec475ca2c6f5bed4f44298b41af4fa` | 0 |
| contracts/Safe.sol | 30242 | `60d4d0321549c9aac50e381d55d64d7837d886f3956382bd1a4dfec1789db130` | 2 |
| contracts/SafeL2.sol | 3685 | `6030700562329d1ebd42ec3c0494b10c9001dbe9080fbb4abf75c1563ed466db` | 0 |
| contracts/accessors/SimulateTxAccessor.sol | 2900 | `ea5890f27c3a488246ecb1880d632f4a5a30fcbbb65a512bad7a1c5b88f86082` | 0 |
| contracts/base/Executor.sol | 1674 | `dcea582290abd1dc0ce89171389d78b716e89f6c788fce523c5cb562e81743e8` | 0 |
| contracts/base/FallbackManager.sol | 4005 | `da724d64eb3238f1cb3355bf8b87c459cf812fc3f6dd100f2f89290a8a169eb9` | 0 |
| contracts/base/GuardManager.sol | 3922 | `e1db96b2ed4f15aa42c8ceca0d8701048e7b6fe276cb437a4f814d85f69119a9` | 0 |
| contracts/base/ModuleManager.sol | 12927 | `3b7be17091c7c9e37c9ddaba41e57464b1c4a334500d34eaddd94721f8cd83b3` | 0 |
| contracts/base/OwnerManager.sol | 7302 | `c9744122158f543336c11bafc70d376711f48c4dd310fe09f385231f264a3fc1` | 0 |
| contracts/common/EIP7702.sol | 1385 | `719f239f789764c2d79150ab0d6d5b3b49af4fee4409f0e6c3303350e30aad3a` | 0 |
| contracts/common/EIP7951.sol | 2378 | `445d712873ba07b5ef800edd7038d8483da9d2ae1f56ee972e18076a7ee90992` | 0 |
| contracts/common/ErrorMessage.sol | 1497 | `7844168e46d0802b3a07a27e974e8db13ba7ff26486d9fc5a746ef272b32c2da` | 0 |
| contracts/common/NativeCurrencyPaymentFallback.sol | 592 | `401744eb862f9f731819c8f904d2ca5768825c0d7680d3448f1a1232cac36ef5` | 0 |
| contracts/common/SecuredSignatureValidator.sol | 1442 | `506e766774ac7800a022d4316831a483af05cd0d42fd1561e00a6a23c48cb1d5` | 0 |
| contracts/common/SecuredTokenTransfer.sol | 1913 | `4aaa684a44631b1a6b14ee97b894380431014abf1fec8e4e4118fd7b275c7010` | 0 |
| contracts/common/SelfAuthorized.sol | 879 | `002069912ab0cb639e0e0eebd5293ceee76530aeaae17a9e0512ea4871ef868f` | 0 |
| contracts/common/SignatureDecoder.sol | 1559 | `784cb20d89bb46765bb8cdf6c5b6e3dada2fa4e932f8afbf1f5d7159ccd8d5c6` | 0 |
| contracts/common/Singleton.sol | 734 | `8bc56aad42a49782b135011e29323cd5117dc41c3a7451470eefe748b5dfab3c` | 0 |
| contracts/common/StorageAccessible.sol | 2087 | `d6ea29d3e65b9a72357e1433aa3798a3d48afe8d8ff1faedf335dcc225302df8` | 0 |
| contracts/external/SafeMath.sol | 1762 | `f56c2b3b9f29c9b8854e6a656ef01577a1fd553e17462119960c45a412c42a9b` | 0 |
| contracts/handler/CompatibilityFallbackHandler.sol | 11112 | `6d52fbba9bdea0f5e47999219e566b1f5983ccd69fcace78579f6f3873a98fe1` | 2 |
| contracts/handler/ExtensibleFallbackHandler.sol | 1422 | `79616d9746ee36e264be7ff2bfc2b7d48e5eba4c43c285cd42d28a8eb19b5cab` | 0 |
| contracts/handler/HandlerContext.sol | 3000 | `120c699c7c7807684c28ed650b2e290353aab5d738d6a388b8a95de1f0e49632` | 0 |
| contracts/handler/TokenCallbackHandler.sol | 2895 | `87853ae257aa5790cd834d88e1db479aa15b308de49d9641df35be45cccb6ffb` | 0 |
| contracts/handler/extensible/ERC165Handler.sol | 4560 | `4d8e55c1e4878665300a43c6b4d7f61bfad9a835754a803e0c33d44355e8f703` | 0 |
| contracts/handler/extensible/ExtensibleBase.sol | 3597 | `ab19a4e9dfae9bc43c635e561bec080c86b81ea68659df5f52f1b7a5eb7bf727` | 0 |
| contracts/handler/extensible/FallbackHandler.sol | 1689 | `c1ee9193eebab1be01513a3ea32c63512c3061c898622b234f74f60e3af49070` | 0 |
| contracts/handler/extensible/MarshalLib.sol | 3362 | `8e8d769dbc1f46a31ad64a5263236d5b464fcb8b886d3055bc06bb66c0292481` | 0 |
| contracts/handler/extensible/SignatureVerifierMuxer.sol | 8119 | `ab760df5f703d6cdbdc16afaa0a8df211520739411ca4a3d76422d94bc5a3d3e` | 1 |
| contracts/handler/extensible/TokenCallbacks.sol | 1750 | `91b1a830a84b55df375737867402183301ef826ecdd3f0e70b13c76694cff382` | 0 |
| contracts/interfaces/ERC1155TokenReceiver.sol | 2983 | `41f98fce7278be0b07c77526565272372b227ec773c85adc22fff9fb3cbc7a95` | 0 |
| contracts/interfaces/ERC721TokenReceiver.sol | 1136 | `df706828bef2646a8770edb2e6aa93aeb07ed5aaabc953896c87c314218d5ba9` | 0 |
| contracts/interfaces/ERC777TokensRecipient.sol | 1155 | `ecbca6e65b6f18f30a61351fd3fe92c635be3aa8a7f9f9442c06e5bbb280eed5` | 0 |
| contracts/interfaces/Enum.sol | 531 | `320aa4eafeefda680db5d0c57ceb0823a93f8a5e85a6c2a2a01d2779f8c2b4ee` | 0 |
| contracts/interfaces/IERC165.sol | 829 | `423a812abe03f809ca695223a1a8ea070fb2e7fd7a7e41b3b629004bd0236b2f` | 0 |
| contracts/interfaces/IFallbackManager.sol | 2778 | `1035a4feaecda99b3263bad0af092396a820f093c52f7c95ea70e5feca486135` | 0 |
| contracts/interfaces/IGuardManager.sol | 1165 | `209325b458c3a401952e6f9172cedb2f1e7b2ed5f09e044621ed2cb543432d6c` | 0 |
| contracts/interfaces/IModuleManager.sol | 5409 | `9251c075d62d1a3667ccbbb77237addd4d3d014ca64ec1fb9d532e44449ddb69` | 0 |
| contracts/interfaces/INativeCurrencyPaymentFallback.sol | 718 | `4c369916f727133f5d9084f69e541bbd7674621f047d9e8810430838817b0e28` | 0 |
| contracts/interfaces/IOwnerManager.sol | 4338 | `15e46219c43b16d649bbe4c8e21598821f572e9f5b70d76067235b45b0eda47d` | 0 |
| contracts/interfaces/ISafe.sol | 11532 | `102d7a71f3be160a7a98536ea6c447df599693e7d4f2f195c63c47118c10d448` | 0 |
| contracts/interfaces/ISignatureValidator.sol | 1205 | `da8e2d45e549c2e94f185cf4c8fbb2294feef389b1fa4b913d65d22466bb44d7` | 0 |
| contracts/interfaces/IStorageAccessible.sol | 1369 | `664c8393448986b757a4cddf58e84be6a9a6d4883a49645545dc1d7450e7dc35` | 0 |
| contracts/interfaces/ViewStorageAccessible.sol | 837 | `c03720d0b31ec9208f2372c1ed397e2b4e7c77f60dc80a571721e50d66a598cf` | 0 |
| contracts/libraries/CreateCall.sol | 2130 | `710ece301e83835acffe0448001c41a912410cb331c81372fe199bab37b7ae1c` | 0 |
| contracts/libraries/MultiSend.sol | 3913 | `7fa2709d8434193d3eeb7e78910d00731b842de71584e0caf3db5417cb6d9c87` | 0 |
| contracts/libraries/MultiSendCallOnly.sol | 3825 | `70b259054dfced971ef259e9f29842ba79a00b34c260fba7d96dbf39613c874a` | 0 |
| contracts/libraries/SafeMigration.sol | 4868 | `4dcfcce8929dceb78331698e71eef595da61ed2b3ee9cbceb3556d22cb948837` | 0 |
| contracts/libraries/SafeStorage.sol | 2125 | `642b3e3f69348c8bb715ed222fd510f71e265f6cf45b71b8d7d88b2bdff00cea` | 0 |
| contracts/libraries/SafeToL2Setup.sol | 3028 | `1e644dbebf6bf8674fb3dc09a681cbc3284463098446464f9b87b89d31014b2f` | 0 |
| contracts/libraries/SignMessageLib.sol | 1705 | `e4a3e7d20f385bd984aa91cb8c8a863bc3a75a25e550144bb4ca88b2a6c0ebf9` | 1 |
| contracts/proxies/SafeProxy.sol | 4223 | `c867699db68a9e0bc9cbde5561a99d88be71fd4e8d82532e79a464e34bd9d3b2` | 0 |
| contracts/proxies/SafeProxyFactory.sol | 9439 | `f5bee22d37e20de6967c4f9eeb7cd099652d83f5a5815eb0118c352ea79bc721` | 0 |
| eslint.config.mjs | 600 | `006760d41bce4c0a43b2de66bc3b0169d9c6c7fe7de6ff051d5cea8cc96fe6ea` | 0 |
| hardhat.config.ts | 3899 | `c20bc7de941edd9ab880721b2d6fdf54f822e79bfde0691d0d22381706f103a1` | 0 |
| package-lock.json | 491576 | `0c9c252a258643903bcbbe7dd88370ca331b6dbeac50004ea387c60ae8ac0476` | 0 |
| package.json | 3644 | `c511ccd2c192aec0465222ddb88e0f14637683627120fb5204819c6cb14f8cc8` | 0 |
| src/deploy/deploy_accessors.ts | 523 | `212f7de0c1c9a1c53bf45642f56dbdc237bca3aa236c73fab33467f34b2a1bd3` | 0 |
| src/deploy/deploy_factories.ts | 519 | `40be845012ef729a2a4064405001dc626d601cc8c3b13f434fe0e2ab1816aff3` | 0 |
| src/deploy/deploy_handlers.ts | 887 | `6a618e83a095dff59bcf3de49fc6d905a1abaf16d835a6f469ac0376d197ef36` | 0 |
| src/deploy/deploy_libraries.ts | 1188 | `3e8c1def9e86c56dfe7e540e7bad0ea5c69e3d3712c3965f9e587ac3d37c4f94` | 0 |
| src/deploy/deploy_migrations.ts | 848 | `3e6d315deaa8623422d9a4efbdfb8c34b692d0a6b5645d2dc64448ffacc89fc1` | 0 |
| src/deploy/deploy_safe_l2.ts | 504 | `34831ce49f360236eb31430caed6736c07021d9a1afac968fb340f66f0fb6953` | 0 |
| src/deploy/deploy_safe_singleton.ts | 497 | `95c750d38a54d68faf7846634fcc05912ea206b93f0bec5c80e93d5778dbf2e2` | 0 |
| src/index.ts | 138 | `c28eecba58a69976643c7f065158bc48e26fab159001a43a7f248990abc242d9` | 0 |
| src/tasks/deploy_contracts.ts | 343 | `8fdf706d87497d9556a2b1ce25b1e6f2056cea8094e4e93964851955e46386fe` | 0 |
| src/tasks/local_verify.ts | 2405 | `2a65e63f135cac4ec6d0f4d9c60021793cd56dead066c8fc1c9386cf56bca703` | 0 |
| src/tasks/show_codesize.ts | 1867 | `b8bbf4580179fdf67e1621d5a20dc19f7bb244edd64f527042f8fc7b4ece7277` | 0 |
| src/utils/constants.ts | 72 | `8d14c53227906c725b97fb116b673c25f06f2b8f18dda038259132bf963cbb5c` | 0 |
| src/utils/execution.ts | 10195 | `d2d395bd775bb64117ad4d323fb164f4dd5ef7c616c64f26beeabbf0096121b3` | 0 |
| src/utils/multisend.ts | 941 | `a6192636ef8e58f6a4a147c9998d635eb5852ceb39de03751c54ad1d1295d143` | 0 |
| src/utils/proxies.ts | 1410 | `8607ae9d409cfb95c2b84f9a939e9d8a0e35d643b9596443e2f9bd5da94eada5` | 0 |
| src/utils/solc.ts | 565 | `c8ba714eb2cc44edc0b1e4de52b7200445d715d54a9eb3a38d9576ed92638f71` | 0 |
| types/solc.d.ts | 23 | `c2232cadfd97cc9479df2315795d7dac60974b2fa08404d4aef03129d084e3d5` | 0 |
