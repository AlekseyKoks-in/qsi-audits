# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** aave-v3-origin @ 8305565ae342 · Aave DAO — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-29 06:16 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 621b91b7-50f0-4a96-bb2c-fd8f374d3ff9 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Финансовая организация |
| SHA-256 содержимого | `e7d4254918ac124d044234875cf5eaf0ca41e8942ad34749fce947e2c8940dca` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **9**
- Средняя: **3**
- Низкая: **14**
- Информационная: **32**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 0
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 11
- Долгосрочный постквантовый риск: 1
- Рекомендация по улучшению: 45
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/aave-dao/aave-v3-origin> @ `8305565ae342f1773c42cd2e4593f175fe5968a0` — ссылки в доказательствах открывают строки на этом коммите.

645 файлов, всего 3567520 байт, редактирований: 44; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| smart_contracts | проверено | 520 | certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol: built-in Solidity pattern checks; certora/atoken-with-delegation/harness/DummyERC20Impl.sol: built-in Solidity pattern checks; certora/atoken-with-delegation/harness/DummyERC20_aTokenUnderlying.sol: built-in Solidity pattern checks |
| slither | не проверено | 520 | slither is not installed on the server (pip install slither-analyzer + solc) |
| source_code | проверено | 113 | echidna-parser.py: 70 lines scanned with 16 rule patterns and 123 registry patterns; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/.mocharc.js: 4 lines scanned with 16 rule patterns and 123 registry patterns; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/.solcover.js: 21 lines scanned with 16 rule patterns and 123 registry patterns |
| secrets | проверено | 43 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/AccessControlUpgradeable.sol: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| dependencies | проверено | 12 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/package.json: 1 dependencies parsed (1 pinned); lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/package.json: 0 dependencies parsed (0 pinned); lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json: 931 dependencies parsed (930 pinned) |
| osv_advisories | проверено | 1 | 852 pinned packages queried at OSV.dev; 53 affected (53 of them only in development or build dependencies) |
| osv_advisories | Недостаточность данных | 2 | npm/axios@1.6.8: 31 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest; npm/undici@6.12.0: 21 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- slither — не проверено: 520 (примеры: slither is not installed on the server (pip install slither-analyzer + solc))
- osv_advisories — Недостаточность данных: 2 (примеры: npm/axios@1.6.8: 31 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest; npm/undici@6.12.0: 21 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest)

## 5. Краткое описание архитектуры

Static review of the source tree aave-v3-origin at 8305565ae342f1773c42cd2e4593f175fe5968a0. 645 files analysed; of 2245 files, 985 are test, fuzzing, benchmark or example code and were left out, 615 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. 420 files come from directories a .gitmodules pins and are read as shipped source rather than skipped as a dependency cache. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **29** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 2.2%

## 7. Подробное описание находок

### QSI-2026-06514 — Использование delegatecall в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 36.1 / 100
- CVSS v3.1: неприменимо

delegatecall в строка 97. (см. SWC-112)

**Возможные последствия.** Если цель контролируется пользователем, атакующий может выполнить произвольный код в контексте хранилища контракта.

**Шаги воспроизведения.**

```
Откройте строка 97 в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol#L97) · line 97 · SHA-256 de90734492398d249f990996f44e7767a3e9ae43db2e357697f6ccfc0437f3af_

```
   95 |      */
   96 |     function functionDelegateCall(address target, bytes memory data) internal returns (bytes memory) {
   97 |         (bool success, bytes memory returndata) = target.delegatecall(data);
   98 |         return verifyCallResultFromTarget(target, success, returndata);
   99 |     }
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Ограничьте цели delegatecall доверенными неизменяемыми реализациями.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06520 — Использование delegatecall в src/contracts/dependencies/openzeppelin/contracts/Address.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:src/contracts/dependencies/openzeppelin/contracts/Address.sol`
- Источник данных: src/contracts/dependencies/openzeppelin/contracts/Address.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 36.1 / 100
- CVSS v3.1: неприменимо

delegatecall в строка 189. (см. SWC-112)

**Возможные последствия.** Если цель контролируется пользователем, атакующий может выполнить произвольный код в контексте хранилища контракта.

**Шаги воспроизведения.**

```
Откройте строка 189 в предоставленном файле src/contracts/dependencies/openzeppelin/contracts/Address.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/dependencies/openzeppelin/contracts/Address.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/dependencies/openzeppelin/contracts/Address.sol#L189) · line 189 · SHA-256 3f41fe8f856b2b05c34725b783da3a450085d424f989736aeff250750bb3d31d_

```
  187 |     require(isContract(target), 'Address: delegate call to non-contract');
  188 | 
  189 |     (bool success, bytes memory returndata) = target.delegatecall(data);
  190 |     return verifyCallResult(success, returndata, errorMessage);
  191 |   }
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Ограничьте цели delegatecall доверенными неизменяемыми реализациями.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06522 — Использование delegatecall в src/contracts/dependencies/openzeppelin/upgradeability/BaseAdminUpgradeabilityProxy.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:src/contracts/dependencies/openzeppelin/upgradeability/BaseAdminUpgradeabilityProxy.sol`
- Источник данных: src/contracts/dependencies/openzeppelin/upgradeability/BaseAdminUpgradeabilityProxy.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 36.1 / 100
- CVSS v3.1: неприменимо

delegatecall в строка 91. (см. SWC-112)

**Возможные последствия.** Если цель контролируется пользователем, атакующий может выполнить произвольный код в контексте хранилища контракта.

**Шаги воспроизведения.**

```
Откройте строка 91 в предоставленном файле src/contracts/dependencies/openzeppelin/upgradeability/BaseAdminUpgradeabilityProxy.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/dependencies/openzeppelin/upgradeability/BaseAdminUpgradeabilityProxy.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/dependencies/openzeppelin/upgradeability/BaseAdminUpgradeabilityProxy.sol#L91) · line 91 · SHA-256 30bb80efff819543847ca3ea9fdb97572d3f1828bc2244825ae0252a20766d9d_

```
   89 |   ) external payable ifAdmin {
   90 |     _upgradeTo(newImplementation);
   91 |     (bool success, ) = newImplementation.delegatecall(data);
   92 |     require(success);
   93 |   }
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Ограничьте цели delegatecall доверенными неизменяемыми реализациями.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06523 — initialize() без модификатора initializer в src/contracts/dependencies/openzeppelin/upgradeability/InitializableAdminUpgradeabilityProxy.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:src/contracts/dependencies/openzeppelin/upgradeability/InitializableAdminUpgradeabilityProxy.sol`
- Источник данных: src/contracts/dependencies/openzeppelin/upgradeability/InitializableAdminUpgradeabilityProxy.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 36.1 / 100
- CVSS v3.1: неприменимо

Функция initialize в строка 25 не имеет защиты initializer/onlyInitializing. (см. SWC-118)

**Возможные последствия.** В обновляемых прокси кто угодно может (пере)инициализировать контракт и стать владельцем.

**Шаги воспроизведения.**

```
Откройте строка 25 в предоставленном файле src/contracts/dependencies/openzeppelin/upgradeability/InitializableAdminUpgradeabilityProxy.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/dependencies/openzeppelin/upgradeability/InitializableAdminUpgradeabilityProxy.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/dependencies/openzeppelin/upgradeability/InitializableAdminUpgradeabilityProxy.sol#L25) · line 25 · SHA-256 266753de8a965b154d9cf5cb60c956bb9ceb40a7c27e18ac21d79ceb040945bb_

```
   23 |    * This parameter is optional, if no data is given the initialization call to proxied contract will be skipped.
   24 |    */
   25 |   function initialize(address logic, address admin, bytes memory data) public payable {
   26 |     require(_implementation() == address(0));
   27 |     InitializableUpgradeabilityProxy.initialize(logic, data);
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06524 — Использование delegatecall в src/contracts/dependencies/openzeppelin/upgradeability/InitializableUpgradeabilityProxy.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:src/contracts/dependencies/openzeppelin/upgradeability/InitializableUpgradeabilityProxy.sol`
- Источник данных: src/contracts/dependencies/openzeppelin/upgradeability/InitializableUpgradeabilityProxy.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 36.1 / 100
- CVSS v3.1: неприменимо

delegatecall в строка 25. (см. SWC-112)

**Возможные последствия.** Если цель контролируется пользователем, атакующий может выполнить произвольный код в контексте хранилища контракта.

**Шаги воспроизведения.**

```
Откройте строка 25 в предоставленном файле src/contracts/dependencies/openzeppelin/upgradeability/InitializableUpgradeabilityProxy.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/dependencies/openzeppelin/upgradeability/InitializableUpgradeabilityProxy.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/dependencies/openzeppelin/upgradeability/InitializableUpgradeabilityProxy.sol#L25) · line 25 · SHA-256 77ddd394b1d27e3a1150cfc9375eda6fb448bd6ff809d1f14a0fc0ce5384ab74_

```
   23 |     _setImplementation(_logic);
   24 |     if (_data.length > 0) {
   25 |       (bool success, ) = _logic.delegatecall(_data);
   26 |       require(success);
   27 |     }
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Ограничьте цели delegatecall доверенными неизменяемыми реализациями.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06525 — initialize() без модификатора initializer в src/contracts/dependencies/openzeppelin/upgradeability/InitializableUpgradeabilityProxy.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:src/contracts/dependencies/openzeppelin/upgradeability/InitializableUpgradeabilityProxy.sol`
- Источник данных: src/contracts/dependencies/openzeppelin/upgradeability/InitializableUpgradeabilityProxy.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 36.1 / 100
- CVSS v3.1: неприменимо

Функция initialize в строка 20 не имеет защиты initializer/onlyInitializing. (см. SWC-118)

**Возможные последствия.** В обновляемых прокси кто угодно может (пере)инициализировать контракт и стать владельцем.

**Шаги воспроизведения.**

```
Откройте строка 20 в предоставленном файле src/contracts/dependencies/openzeppelin/upgradeability/InitializableUpgradeabilityProxy.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/dependencies/openzeppelin/upgradeability/InitializableUpgradeabilityProxy.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/dependencies/openzeppelin/upgradeability/InitializableUpgradeabilityProxy.sol#L20) · line 20 · SHA-256 b49e18aa0ee1e666897edb35832e4e1d84deea105daa78f560d2b286e6edf4e9_

```
   18 |    * This parameter is optional, if no data is given the initialization call to proxied contract will be skipped.
   19 |    */
   20 |   function initialize(address _logic, bytes memory _data) public payable {
   21 |     require(_implementation() == address(0));
   22 |     assert(IMPLEMENTATION_SLOT == bytes32(uint256(keccak256('eip1967.proxy.implementation')) - 1));
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06526 — Использование delegatecall в src/contracts/dependencies/openzeppelin/upgradeability/UpgradeabilityProxy.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:src/contracts/dependencies/openzeppelin/upgradeability/UpgradeabilityProxy.sol`
- Источник данных: src/contracts/dependencies/openzeppelin/upgradeability/UpgradeabilityProxy.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 36.1 / 100
- CVSS v3.1: неприменимо

delegatecall в строка 24. (см. SWC-112)

**Возможные последствия.** Если цель контролируется пользователем, атакующий может выполнить произвольный код в контексте хранилища контракта.

**Шаги воспроизведения.**

```
Откройте строка 24 в предоставленном файле src/contracts/dependencies/openzeppelin/upgradeability/UpgradeabilityProxy.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/dependencies/openzeppelin/upgradeability/UpgradeabilityProxy.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/dependencies/openzeppelin/upgradeability/UpgradeabilityProxy.sol#L24) · line 24 · SHA-256 8d39b3af4143d6cc3798aa604fa89f9559f48adb93c28b93bb10fcba492680ef_

```
   22 |     _setImplementation(_logic);
   23 |     if (_data.length > 0) {
   24 |       (bool success, ) = _logic.delegatecall(_data);
   25 |       require(success);
   26 |     }
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Ограничьте цели delegatecall доверенными неизменяемыми реализациями.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06530 — Использование delegatecall в src/contracts/misc/aave-upgradeability/BaseImmutableAdminUpgradeabilityProxy.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:src/contracts/misc/aave-upgradeability/BaseImmutableAdminUpgradeabilityProxy.sol`
- Источник данных: src/contracts/misc/aave-upgradeability/BaseImmutableAdminUpgradeabilityProxy.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 36.1 / 100
- CVSS v3.1: неприменимо

delegatecall в строка 74. (см. SWC-112)

**Возможные последствия.** Если цель контролируется пользователем, атакующий может выполнить произвольный код в контексте хранилища контракта.

**Шаги воспроизведения.**

```
Откройте строка 74 в предоставленном файле src/contracts/misc/aave-upgradeability/BaseImmutableAdminUpgradeabilityProxy.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/misc/aave-upgradeability/BaseImmutableAdminUpgradeabilityProxy.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/misc/aave-upgradeability/BaseImmutableAdminUpgradeabilityProxy.sol#L74) · line 74 · SHA-256 90dc75b9009ea707b86a26f2347c3f9ad73ab2594bd13bada9b043af50848e02_

```
   72 |   ) external payable ifAdmin {
   73 |     _upgradeTo(newImplementation);
   74 |     (bool success, ) = newImplementation.delegatecall(data);
   75 |     require(success);
   76 |   }
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Ограничьте цели delegatecall доверенными неизменяемыми реализациями.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06533 — initialize() без модификатора initializer в src/contracts/protocol/libraries/logic/ReserveLogic.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:src/contracts/protocol/libraries/logic/ReserveLogic.sol`
- Источник данных: src/contracts/protocol/libraries/logic/ReserveLogic.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 36.1 / 100
- CVSS v3.1: неприменимо

Функция initialize в строка 109 не имеет защиты initializer/onlyInitializing. (см. SWC-118)

**Возможные последствия.** В обновляемых прокси кто угодно может (пере)инициализировать контракт и стать владельцем.

**Шаги воспроизведения.**

```
Откройте строка 109 в предоставленном файле src/contracts/protocol/libraries/logic/ReserveLogic.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/protocol/libraries/logic/ReserveLogic.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/protocol/libraries/logic/ReserveLogic.sol#L109) · line 109 · SHA-256 bfa338b3393179446700603bc559ea36ccce1fb154f227d3e360d5d25a7cc303_

```
  107 |    * @param variableDebtTokenAddress The address of the overlying variable debt token contract
  108 |    */
  109 |   function init(
  110 |     DataTypes.ReserveData storage reserve,
  111 |     address aTokenAddress,
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06482 — Прямое использование ecrecover в certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol`
- Источник данных: certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 43.0 / 100
- CVSS v3.1: неприменимо

ecrecover в строка 98. (см. SWC-117/SWC-121)

**Возможные последствия.** Без проверок s-значения/нулевого адреса и nonce подписи могут быть изменяемыми или повторно используемыми. ecrecover основан на secp256k1 ECDSA (долгосрочно квантово-уязвим).

**Шаги воспроизведения.**

```
Откройте строка 98 в предоставленном файле certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol#L98) · line 98 · SHA-256 f341d040eab32a32d8c57d399be1f82e3cb0ddd7c9dce1f1a28cbbe4a62b96b4_

```
   96 |     bytes32 s
   97 |   ) public pure returns (address) {
   98 |     return ecrecover(hash, v, r, s);
   99 |   }
  100 |   function computeMetaDelegateHash(
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin ECDSA.recover с разделением доменов EIP-712 и nonce.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06515 — Прямое использование ecrecover в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 43.0 / 100
- CVSS v3.1: неприменимо

ecrecover в строка 148. (см. SWC-117/SWC-121)

**Возможные последствия.** Без проверок s-значения/нулевого адреса и nonce подписи могут быть изменяемыми или повторно используемыми. ecrecover основан на secp256k1 ECDSA (долгосрочно квантово-уязвим).

**Шаги воспроизведения.**

```
Откройте строка 148 в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol#L148) · line 148 · SHA-256 bbb05c626df7732576d2e3f08f6fcf908767b508ed20b71385b32c95794d893e_

```
  146 | 
  147 |         // If the signature is valid (and not malleable), return the signer address
  148 |         address signer = ecrecover(hash, v, r, s);
  149 |         if (signer == address(0)) {
  150 |             return (address(0), RecoverError.InvalidSignature, bytes32(0));
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте OpenZeppelin ECDSA.recover с разделением доменов EIP-712 и nonce.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06481 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 39.6 / 100
- CVSS v3.1: неприменимо

2 упоминаний ECDSA в 2 файл(ах), например certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol:98. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol:98 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol#L98) · line 98 · SHA-256 f341d040eab32a32d8c57d399be1f82e3cb0ddd7c9dce1f1a28cbbe4a62b96b4_

```
   96 |     bytes32 s
   97 |   ) public pure returns (address) {
   98 |     return ecrecover(hash, v, r, s);
   99 |   }
  100 |   function computeMetaDelegateHash(
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol#L148) · line 148 · SHA-256 bbb05c626df7732576d2e3f08f6fcf908767b508ed20b71385b32c95794d893e_

```
  146 | 
  147 |         // If the signature is valid (and not malleable), return the signer address
  148 |         address signer = ecrecover(hash, v, r, s);
  149 |         if (signer == address(0)) {
  150 |             return (address(0), RecoverError.InvalidSignature, bytes32(0));
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06480 — Плавающая версия компилятора (^0.8.0) в 116 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.0`
- Источник данных: certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.0 в 116 файл(ах), впервые в certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol:7. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol:7 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol#L7) · line 7 · SHA-256 d9e74f9f04af0442bac5a64083246a3c44a4dc2ee529e80a01a1bf464a07e543_

```
    5 |  */
    6 | 
    7 | pragma solidity ^0.8.0;
    8 | 
    9 | import {ATokenWithDelegationInstance} from 'certora/atoken-with-delegation/munged/src/contracts/instances/ATokenWithDelegationInstance.sol';
```

_file_excerpt · [certora/atoken-with-delegation/harness/DummyERC20Impl.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/atoken-with-delegation/harness/DummyERC20Impl.sol#L2) · line 2 · SHA-256 d6da26a109fcbcfe48b3ead0d1cf964ab2d25b2e1ec72df018af6bb75032a726_

```
    1 | // SPDX-License-Identifier: agpl-3.0
    2 | pragma solidity ^0.8.0;
    3 | 
    4 | // with mint
```

_file_excerpt · [certora/basic/harness/PoolInstanceHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/basic/harness/PoolInstanceHarness.sol#L2) · line 2 · SHA-256 da57c7eb8b978240f834d0886ba8f13d437fb7cd308efdb09e91d56969cd47c6_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.0;
    3 | 
    4 | import {Pool} from '../munged/src/contracts/protocol/pool/Pool.sol';
```

_file_excerpt · [certora/math-calculations/harnesses/PoolInstanceHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/math-calculations/harnesses/PoolInstanceHarness.sol#L2) · line 2 · SHA-256 da57c7eb8b978240f834d0886ba8f13d437fb7cd308efdb09e91d56969cd47c6_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.0;
    3 | 
    4 | import {Pool} from '../munged/src/contracts/protocol/pool/Pool.sol';
```

_file_excerpt · [certora/solvency/harnesses/Aave/PoolInstanceHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/solvency/harnesses/Aave/PoolInstanceHarness.sol#L2) · line 2 · SHA-256 98736a9b681094b8271db4452baf0324ae907d492e5983b49cd32465cb30877b_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.0;
    3 | 
    4 | import {Pool} from '../../munged/src/contracts/protocol/pool/Pool.sol';
```

_file_excerpt · [certora/solvency/harnesses/ERC20Like/DummyERC20A.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/solvency/harnesses/ERC20Like/DummyERC20A.sol#L4) · line 4 · SHA-256 c924b98cd72fe91e990d2a6d3211feda370bae7cc9f852ad558d420c8e372768_

```
    2 | 
    3 | // SPDX-License-Identifier: agpl-3.0
    4 | pragma solidity ^0.8.0;
    5 | 
    6 | contract DummyERC20A {
```

_file_excerpt · [certora/solvency/harnesses/ERC20Like/DummyERC20B.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/solvency/harnesses/ERC20Like/DummyERC20B.sol#L4) · line 4 · SHA-256 6c0cf6a837bdee3b219d7eef171c083d33713892fc8497043703edf702b86810_

```
    2 | 
    3 | // SPDX-License-Identifier: agpl-3.0
    4 | pragma solidity ^0.8.0;
    5 | 
    6 | contract DummyERC20B {
```

_file_excerpt · [certora/stata/harness/tokens/DummyERC20Impl.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/stata/harness/tokens/DummyERC20Impl.sol#L2) · line 2 · SHA-256 afd12dd35620a320e9a4292953a5a4781d914013f2a37313c9f7bcd1198c4f16_

```
    1 | // SPDX-License-Identifier: agpl-3.0
    2 | pragma solidity ^0.8.0;
    3 | 
    4 | contract DummyERC20Impl {
```

_file_excerpt · [lib/solidity-utils/script/DeployCreate3Factory.s.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/script/DeployCreate3Factory.s.sol#L2) · line 2 · SHA-256 f073d92b70a36ab471aacdc63b8bea1ef34caeb1fa16eb93fed6f108c1d51333_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.0;
    3 | 
    4 | import {Script} from 'forge-std/Script.sol';
```

_file_excerpt · [lib/solidity-utils/script/DeployTransparentProxyFactory.s.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/script/DeployTransparentProxyFactory.s.sol#L2) · line 2 · SHA-256 f073d92b70a36ab471aacdc63b8bea1ef34caeb1fa16eb93fed6f108c1d51333_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.0;
    3 | 
    4 | import {Script} from 'forge-std/Script.sol';
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06483 — Плавающая версия компилятора (^0.8.10) в 91 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.10`
- Источник данных: certora/atoken-with-delegation/harness/DummyERC20_aTokenUnderlying.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.10 в 91 файл(ах), впервые в certora/atoken-with-delegation/harness/DummyERC20_aTokenUnderlying.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте certora/atoken-with-delegation/harness/DummyERC20_aTokenUnderlying.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [certora/atoken-with-delegation/harness/DummyERC20_aTokenUnderlying.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/atoken-with-delegation/harness/DummyERC20_aTokenUnderlying.sol#L2) · line 2 · SHA-256 3f4a1d22a82973bb049cd9fb4690919c2da353bf6bb37eb1ce85c05dc5ccb5ab_

```
    1 | // SPDX-License-Identifier: agpl-3.0
    2 | pragma solidity ^0.8.10;
    3 | import './DummyERC20Impl.sol';
    4 | 
```

_file_excerpt · [certora/atoken-with-delegation/harness/SymbolicLendingPoolL1.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/atoken-with-delegation/harness/SymbolicLendingPoolL1.sol#L1) · line 1 · SHA-256 d1c3f956c97930fc8de9a0f274967aeefd14bf01f27af1310c3ea0ee4e5811ca_

```
    1 | pragma solidity ^0.8.10;
    2 | pragma experimental ABIEncoderV2;
    3 | 
```

_file_excerpt · [certora/stata/harness/StataTokenV2Harness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/stata/harness/StataTokenV2Harness.sol#L2) · line 2 · SHA-256 2b53497786e16d3e0ca1f9dc651d0ecab694a775a25d4989c816f2ec2c06775f_

```
    1 | // SPDX-License-Identifier: agpl-3.0
    2 | pragma solidity ^0.8.10;
    3 | 
    4 | import {IERC20} from 'openzeppelin-contracts/contracts/interfaces/IERC20.sol';
```

_file_excerpt · [certora/stata/harness/pool/SymbolicLendingPool.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/stata/harness/pool/SymbolicLendingPool.sol#L1) · line 1 · SHA-256 d1c3f956c97930fc8de9a0f274967aeefd14bf01f27af1310c3ea0ee4e5811ca_

```
    1 | pragma solidity ^0.8.10;
    2 | pragma experimental ABIEncoderV2;
    3 | 
```

_file_excerpt · [certora/stata/harness/rewards/RewardsControllerHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/stata/harness/rewards/RewardsControllerHarness.sol#L1) · line 1 · SHA-256 9372b15ef72f01a12dcf2cfafcf77b91177ed855c5bd5c7dae427ce94ddb1c41_

```
    1 | pragma solidity ^0.8.10;
    2 | 
    3 | import {RewardsController, RewardsDataTypes} from '../../munged/src/contracts/rewards/RewardsController.sol';
```

_file_excerpt · [certora/stata/harness/rewards/TransferStrategyHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/stata/harness/rewards/TransferStrategyHarness.sol#L1) · line 1 · SHA-256 8918629f0b4ee16e39cda4b40c958d8e55cbff27df98e3983c34bd2518ddf77a_

```
    1 | pragma solidity ^0.8.10;
    2 | 
    3 | import {IERC20} from 'openzeppelin-contracts/contracts/token/ERC20/IERC20.sol';
```

_file_excerpt · [certora/stata/harness/rewards/TransferStrategyMultiRewardHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/stata/harness/rewards/TransferStrategyMultiRewardHarness.sol#L1) · line 1 · SHA-256 abb8b785a9929500267f2715dea61d3584ddd46583c3679bbafa52de99a7d141_

```
    1 | pragma solidity ^0.8.10;
    2 | 
    3 | import {IERC20} from '../../munged/lib/aave-v3-core/contracts/dependencies/openzeppelin/contracts/IERC20.sol';
```

_file_excerpt · [certora/stata/harness/tokens/DummyERC20_aTokenUnderlying.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/stata/harness/tokens/DummyERC20_aTokenUnderlying.sol#L2) · line 2 · SHA-256 3f4a1d22a82973bb049cd9fb4690919c2da353bf6bb37eb1ce85c05dc5ccb5ab_

```
    1 | // SPDX-License-Identifier: agpl-3.0
    2 | pragma solidity ^0.8.10;
    3 | import './DummyERC20Impl.sol';
    4 | 
```

_file_excerpt · [certora/stata/harness/tokens/DummyERC20_rewardToken.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/stata/harness/tokens/DummyERC20_rewardToken.sol#L2) · line 2 · SHA-256 d11267193b3f90a28bf22d55c16525e7c11375116a83c98af7fadca6d16f83b4_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.10;
    3 | import './DummyERC20Impl.sol';
    4 | 
```

_file_excerpt · [lib/solidity-utils/src/contracts/transparent-proxy/interfaces/IProxyAdminOzV4.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/transparent-proxy/interfaces/IProxyAdminOzV4.sol#L2) · line 2 · SHA-256 53a9a15431851cfc4c1d9658d2a89ef900454527e9a4f8ab8bab76d0d3db92ad_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.10;
    3 | 
    4 | /**
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06484 — Плавающая версия компилятора (^0.8.19) в 8 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.19`
- Источник данных: certora/basic/harness/ATokenHarness.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.19 в 8 файл(ах), впервые в certora/basic/harness/ATokenHarness.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте certora/basic/harness/ATokenHarness.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [certora/basic/harness/ATokenHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/basic/harness/ATokenHarness.sol#L2) · line 2 · SHA-256 0c572c448d4e052ab1eaac66bb54b9ad683dee9dfc3a39aaefdaca3f515d9d09_

```
    1 | // SPDX-License-Identifier: agpl-3.0
    2 | pragma solidity ^0.8.19;
    3 | 
    4 | import {Pool} from '../munged/src/contracts/protocol/pool/Pool.sol';
```

_file_excerpt · [certora/basic/harness/EModeConfigurationHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/basic/harness/EModeConfigurationHarness.sol#L2) · line 2 · SHA-256 b52838116bb7b3c33adf25ee4550d0c3b5fa616e479c99319ecc08012ad4707a_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.19;
    3 | pragma experimental ABIEncoderV2;
    4 | 
```

_file_excerpt · [certora/basic/harness/PoolHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/basic/harness/PoolHarness.sol#L2) · line 2 · SHA-256 a01ca8d39017e2e3efa43e47fee1f5aaa8ecff98494e1dcf69954d4cef4df614_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.19;
    3 | 
    4 | import {PoolInstance} from '../munged/src/contracts/instances/PoolInstance.sol';
```

_file_excerpt · [certora/basic/harness/ReserveConfigurationHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/basic/harness/ReserveConfigurationHarness.sol#L2) · line 2 · SHA-256 b52838116bb7b3c33adf25ee4550d0c3b5fa616e479c99319ecc08012ad4707a_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.19;
    3 | pragma experimental ABIEncoderV2;
    4 | 
```

_file_excerpt · [certora/basic/harness/SimpleERC20.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/basic/harness/SimpleERC20.sol#L2) · line 2 · SHA-256 d054857602dde7d3e64e5065192e4bb321400d0f01121fd8c67088815eaa6abb_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.19;
    3 | 
    4 | import {IERC20} from 'openzeppelin-contracts/contracts/token/ERC20/IERC20.sol';
```

_file_excerpt · [certora/basic/harness/SymbolicPriceOracle.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/basic/harness/SymbolicPriceOracle.sol#L2) · line 2 · SHA-256 78526b3e7bfa8670bb1bd78631fb5964c96177c353527da6e3d649d0149e8fd2_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.19;
    3 | 
    4 | import {IPriceOracleGetter} from '../munged/src/contracts/interfaces/IPriceOracleGetter.sol';
```

_file_excerpt · [certora/basic/harness/UserConfigurationHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/basic/harness/UserConfigurationHarness.sol#L2) · line 2 · SHA-256 b52838116bb7b3c33adf25ee4550d0c3b5fa616e479c99319ecc08012ad4707a_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.19;
    3 | pragma experimental ABIEncoderV2;
    4 | 
```

_file_excerpt · [certora/basic/harness/VariableDebtTokenHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/basic/harness/VariableDebtTokenHarness.sol#L2) · line 2 · SHA-256 14c62e563a900d89c639b64cbe6bd05d02a677cf1bb7a3c98f35fba972999671_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.19;
    3 | 
    4 | import {VariableDebtTokenInstance} from '../munged/src/contracts/instances/VariableDebtTokenInstance.sol';
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06485 — Плавающая версия компилятора (>=0.8.0) в 5 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.8.0`
- Источник данных: certora/solvency/harnesses/ERC20Like/DummyWeth.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.8.0 в 5 файл(ах), впервые в certora/solvency/harnesses/ERC20Like/DummyWeth.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте certora/solvency/harnesses/ERC20Like/DummyWeth.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [certora/solvency/harnesses/ERC20Like/DummyWeth.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/certora/solvency/harnesses/ERC20Like/DummyWeth.sol#L2) · line 2 · SHA-256 785861bbc2e0a88eb0bd3b98cf2d84d2a34a2a761705ae60b484507be3c689b2_

```
    1 | // SPDX-License-Identifier: agpl-3.0
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | /**
```

_file_excerpt · [lib/solidity-utils/src/contracts/transparent-proxy/TransparentProxyFactory.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/transparent-proxy/TransparentProxyFactory.sol#L2) · line 2 · SHA-256 6d0558e6081d2b24d19a9d6f4980118ad69cf49fbe347361a405afeec8c90ed8_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | import {TransparentProxyFactoryBase} from './TransparentProxyFactoryBase.sol';
```

_file_excerpt · [lib/solidity-utils/src/contracts/transparent-proxy/TransparentProxyFactoryBase.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/transparent-proxy/TransparentProxyFactoryBase.sol#L2) · line 2 · SHA-256 5e012ccfa5ef0aef37479a143ad727d932e8fafbcc6fef7fd7f4328a817f40fc_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | import {TransparentUpgradeableProxy} from 'openzeppelin-contracts/contracts/proxy/transparent/TransparentUpgradeableProxy.sol';
```

_file_excerpt · [lib/solidity-utils/src/contracts/transparent-proxy/interfaces/ITransparentProxyFactory.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/transparent-proxy/interfaces/ITransparentProxyFactory.sol#L2) · line 2 · SHA-256 1162d8a266f347a4fcd4abfe105ce51b713291e4a5c89ddb83d25873bc31eea6_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | interface ITransparentProxyFactory {
```

_file_excerpt · [lib/solidity-utils/zksync/src/contracts/transparent-proxy/interfaces/ITransparentProxyFactoryZkSync.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/zksync/src/contracts/transparent-proxy/interfaces/ITransparentProxyFactoryZkSync.sol#L2) · line 2 · SHA-256 6d1f0a69f7f0b55664c1ffb266b72f667942d81bd0110b9e74130985fa5781e9_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity >=0.8.0;
    3 | 
    4 | interface ITransparentProxyFactoryZkSync {
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06486 — Плавающая версия компилятора (^0.8.20) в 259 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.20`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.20 в 259 файл(ах), впервые в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol#L2) · line 2 · SHA-256 756598f4bd85d94c54eb240ebeadf53780d19d71de6fe7a69ff53c1507742f21_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.20;
    3 | 
    4 | import {AccessControlDefaultAdminRules} from "../patched/access/extensions/AccessControlDefaultAdminRules.sol";
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlHarness.sol#L2) · line 2 · SHA-256 d3760e2e2e6b2de828a557f740f9904e637cc250bed6ea48140f2d7daef11453_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.20;
    3 | 
    4 | import {AccessControl} from "../patched/access/AccessControl.sol";
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessManagedHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessManagedHarness.sol#L3) · line 3 · SHA-256 8b82af0296a3ec37e4e214190af0400128d0db4f5ee34af49eec871b38137797_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.20;
    4 | 
    5 | import "../patched/access/manager/IAccessManager.sol";
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessManagerHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessManagerHarness.sol#L3) · line 3 · SHA-256 87d2bae8e69f1f7f97a6ba1e9699d0307d2dae27a7db50ac21f0dc2fb2cdf318_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.20;
    4 | 
    5 | import "../patched/access/manager/AccessManager.sol";
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/DoubleEndedQueueHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/DoubleEndedQueueHarness.sol#L2) · line 2 · SHA-256 7465f9b8e6c53057c2d9dfbc88a2b83fb14b813ca1d865da45a12143ec796206_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.20;
    3 | 
    4 | import {DoubleEndedQueue} from "../patched/utils/structs/DoubleEndedQueue.sol";
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20FlashMintHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20FlashMintHarness.sol#L3) · line 3 · SHA-256 d9268da21b039a53f3ffe15e3e1b64163968ef2adaabc61fb422f2327baf75d3_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.20;
    4 | 
    5 | import "../patched/token/ERC20/ERC20.sol";
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20PermitHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20PermitHarness.sol#L2) · line 2 · SHA-256 fe79ecdbebdd3812b94f5edab6c9b7572be14d41aa4c9be552aa6706e1ac1d3d_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.20;
    3 | 
    4 | import {ERC20Permit, ERC20} from "../patched/token/ERC20/extensions/ERC20Permit.sol";
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20WrapperHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20WrapperHarness.sol#L3) · line 3 · SHA-256 16d256728596f72ea22e19d41f979405a160b6d28721d44c83e4422d9017b2ce_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.20;
    4 | 
    5 | import {ERC20Permit} from "../patched/token/ERC20/extensions/ERC20Permit.sol";
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC3156FlashBorrowerHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC3156FlashBorrowerHarness.sol#L5) · line 5 · SHA-256 c5389bf3b06d502da28d0c5a350b10b0fabe82e0ffba247a522ea005b5e3ad09_

```
    3 | import {IERC3156FlashBorrower} from "../patched/interfaces/IERC3156FlashBorrower.sol";
    4 | 
    5 | pragma solidity ^0.8.20;
    6 | 
    7 | contract ERC3156FlashBorrowerHarness is IERC3156FlashBorrower {
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC721Harness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC721Harness.sol#L3) · line 3 · SHA-256 6f89bde0f57299ebcc2623cc87a97d97d48f0b4775ed243d802e69dc6d1fee44_

```
    1 | // SPDX-License-Identifier: MIT
    2 | 
    3 | pragma solidity ^0.8.20;
    4 | 
    5 | import {ERC721} from "../patched/token/ERC721/ERC721.sol";
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06498 — Плавающая версия компилятора (^0.8.24) в 5 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.24`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/draft-ERC20TemporaryApprovalUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.24 в 5 файл(ах), впервые в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/draft-ERC20TemporaryApprovalUpgradeable.sol:4. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/draft-ERC20TemporaryApprovalUpgradeable.sol:4 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/draft-ERC20TemporaryApprovalUpgradeable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/draft-ERC20TemporaryApprovalUpgradeable.sol#L4) · line 4 · SHA-256 5a11266dbe1e109cf348cb2e60914af74f8f403068ca4e8b2443a77173db6c29_

```
    2 | // OpenZeppelin Contracts (last updated v5.1.0) (token/ERC20/extensions/draft-ERC20TemporaryApproval.sol)
    3 | 
    4 | pragma solidity ^0.8.24;
    5 | 
    6 | import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/utils/ReentrancyGuardTransientUpgradeable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/utils/ReentrancyGuardTransientUpgradeable.sol#L4) · line 4 · SHA-256 3d1f7a4cfc04f0d2e70838925b10eb81294565debad269aa7b9bd9f6f12eccdf_

```
    2 | // OpenZeppelin Contracts (last updated v5.1.0) (utils/ReentrancyGuardTransient.sol)
    3 | 
    4 | pragma solidity ^0.8.24;
    5 | 
    6 | import {TransientSlot} from "@openzeppelin/contracts/utils/TransientSlot.sol";
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/draft-ERC20TemporaryApproval.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/draft-ERC20TemporaryApproval.sol#L4) · line 4 · SHA-256 9344f82d04b9f7af916cb0b1bcbdad2ef9615ff54cb15477e041ae21748d6164_

```
    2 | // OpenZeppelin Contracts (last updated v5.1.0) (token/ERC20/extensions/draft-ERC20TemporaryApproval.sol)
    3 | 
    4 | pragma solidity ^0.8.24;
    5 | 
    6 | import {IERC20, ERC20} from "../ERC20.sol";
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/ReentrancyGuardTransient.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/ReentrancyGuardTransient.sol#L4) · line 4 · SHA-256 9e0a013a63e72cf9e957ec0c3487550a116f2fbdf5efa8cfc44b766e244eaf70_

```
    2 | // OpenZeppelin Contracts (last updated v5.1.0) (utils/ReentrancyGuardTransient.sol)
    3 | 
    4 | pragma solidity ^0.8.24;
    5 | 
    6 | import {TransientSlot} from "./TransientSlot.sol";
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/TransientSlot.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/TransientSlot.sol#L5) · line 5 · SHA-256 7a9ea731dab1ba86bf5cf6db7408602602c49690ea2d1745a202dadb94d3781f_

```
    3 | // This file was procedurally generated from scripts/generate/templates/TransientSlot.js.
    4 | 
    5 | pragma solidity ^0.8.24;
    6 | 
    7 | /**
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06499 — Плавающая версия компилятора (>=0.8.0 <0.9.0) в 4 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.8.0 <0.9.0`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SVM.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.8.0 <0.9.0 в 4 файл(ах), впервые в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SVM.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SVM.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SVM.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SVM.sol#L2) · line 2 · SHA-256 bd471efc2f4d7d423e928467267caaddb41788dd0f77dd12ceceaf88d979eed2_

```
    1 | // SPDX-License-Identifier: AGPL-3.0
    2 | pragma solidity >=0.8.0 <0.9.0;
    3 | 
    4 | /// @notice Symbolic Virtual Machine
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SymTest.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SymTest.sol#L2) · line 2 · SHA-256 97630b16a584af991c523a19d6304c66e9d3e30b64896278317489cf5453873b_

```
    1 | // SPDX-License-Identifier: AGPL-3.0
    2 | pragma solidity >=0.8.0 <0.9.0;
    3 | 
    4 | import {SVM} from "./SVM.sol";
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SVM.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SVM.sol#L2) · line 2 · SHA-256 bd471efc2f4d7d423e928467267caaddb41788dd0f77dd12ceceaf88d979eed2_

```
    1 | // SPDX-License-Identifier: AGPL-3.0
    2 | pragma solidity >=0.8.0 <0.9.0;
    3 | 
    4 | /// @notice Symbolic Virtual Machine
```

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SymTest.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SymTest.sol#L2) · line 2 · SHA-256 97630b16a584af991c523a19d6304c66e9d3e30b64896278317489cf5453873b_

```
    1 | // SPDX-License-Identifier: AGPL-3.0
    2 | pragma solidity >=0.8.0 <0.9.0;
    3 | 
    4 | import {SVM} from "./SVM.sol";
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06511 — Плавающая версия компилятора (^0.8.21) в 1 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.21`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.21 в 1 файл(ах), впервые в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol:4. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol:4 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol#L4) · line 4 · SHA-256 92b44c1a06ddae2adf03930c44f71ad22432d5ea2f83bbc540521062e6f92f20_

```
    2 | // OpenZeppelin Contracts (last updated v5.1.0) (proxy/ERC1967/ERC1967Utils.sol)
    3 | 
    4 | pragma solidity ^0.8.21;
    5 | 
    6 | import {IBeacon} from "../beacon/IBeacon.sol";
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06516 — Плавающая версия компилятора (>=0.7.0) в 2 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.7.0`
- Источник данных: lib/solidity-utils/src/contracts/access-control/OwnableWithGuardian.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.7.0 в 2 файл(ах), впервые в lib/solidity-utils/src/contracts/access-control/OwnableWithGuardian.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте lib/solidity-utils/src/contracts/access-control/OwnableWithGuardian.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/src/contracts/access-control/OwnableWithGuardian.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/access-control/OwnableWithGuardian.sol#L2) · line 2 · SHA-256 73a344cd3aebcbdce655ee075d0f9c1d00cf226e3aedfd308dfba1b0631615a3_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity >=0.7.0;
    3 | 
    4 | import {Ownable} from 'openzeppelin-contracts/contracts/access/Ownable.sol';
```

_file_excerpt · [lib/solidity-utils/src/contracts/access-control/interfaces/IWithGuardian.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/access-control/interfaces/IWithGuardian.sol#L2) · line 2 · SHA-256 81db97b9ce570bb2ff5d09073f02e6711a46668d884419dd91f206b87520a3f1_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity >=0.7.0;
    3 | 
    4 | interface IWithGuardian {
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06517 — Плавающая версия компилятора (>=0.6.0) в 1 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.6.0`
- Источник данных: lib/solidity-utils/src/contracts/create3/interfaces/ICreate3Factory.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.6.0 в 1 файл(ах), впервые в lib/solidity-utils/src/contracts/create3/interfaces/ICreate3Factory.sol:3. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте lib/solidity-utils/src/contracts/create3/interfaces/ICreate3Factory.sol:3 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/src/contracts/create3/interfaces/ICreate3Factory.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/create3/interfaces/ICreate3Factory.sol#L3) · line 3 · SHA-256 4801b7f73f64b9c9437b99b7fe0d70c63c2ba7075177987580c2ce7cc31560ad_

```
    1 | // SPDX-License-Identifier: AGPL-3.0
    2 | // Modified from https://github.com/lifinance/create3-factory/blob/main/src/ICREATE3Factory.sol
    3 | pragma solidity >=0.6.0;
    4 | 
    5 | /**
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06518 — Плавающая версия компилятора (^0.8.8) в 9 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.8`
- Источник данных: lib/solidity-utils/src/contracts/utils/PermissionlessRescuable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.8 в 9 файл(ах), впервые в lib/solidity-utils/src/contracts/utils/PermissionlessRescuable.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте lib/solidity-utils/src/contracts/utils/PermissionlessRescuable.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/src/contracts/utils/PermissionlessRescuable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/utils/PermissionlessRescuable.sol#L2) · line 2 · SHA-256 eaa0f8c504eaf49ec742745fde5429da58205aa9cb40b32f8422df31098508cb_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.8;
    3 | 
    4 | import {IERC20} from 'openzeppelin-contracts/contracts/token/ERC20/IERC20.sol';
```

_file_excerpt · [lib/solidity-utils/src/contracts/utils/Rescuable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/utils/Rescuable.sol#L2) · line 2 · SHA-256 eaa0f8c504eaf49ec742745fde5429da58205aa9cb40b32f8422df31098508cb_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.8;
    3 | 
    4 | import {IERC20} from 'openzeppelin-contracts/contracts/token/ERC20/IERC20.sol';
```

_file_excerpt · [lib/solidity-utils/src/contracts/utils/Rescuable721.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/utils/Rescuable721.sol#L2) · line 2 · SHA-256 cc4dea6ba3598de0c2410be31b2f0a6951d833642bba7a010c49f2ce65d22cee_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.8;
    3 | 
    4 | import {IRescuable721, IERC721} from './interfaces/IRescuable721.sol';
```

_file_excerpt · [lib/solidity-utils/src/contracts/utils/RescuableACL.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/utils/RescuableACL.sol#L2) · line 2 · SHA-256 eaa0f8c504eaf49ec742745fde5429da58205aa9cb40b32f8422df31098508cb_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.8;
    3 | 
    4 | import {IERC20} from 'openzeppelin-contracts/contracts/token/ERC20/IERC20.sol';
```

_file_excerpt · [lib/solidity-utils/src/contracts/utils/RescuableBase.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/utils/RescuableBase.sol#L2) · line 2 · SHA-256 eaa0f8c504eaf49ec742745fde5429da58205aa9cb40b32f8422df31098508cb_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.8;
    3 | 
    4 | import {IERC20} from 'openzeppelin-contracts/contracts/token/ERC20/IERC20.sol';
```

_file_excerpt · [lib/solidity-utils/src/contracts/utils/interfaces/IPermissionlessRescuable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/utils/interfaces/IPermissionlessRescuable.sol#L2) · line 2 · SHA-256 14965fdd47357cdb76f96132017b043b9cd91aea525848ac67f27e4f6c3deb3c_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.8;
    3 | 
    4 | import {IRescuableBase} from './IRescuableBase.sol';
```

_file_excerpt · [lib/solidity-utils/src/contracts/utils/interfaces/IRescuable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/utils/interfaces/IRescuable.sol#L2) · line 2 · SHA-256 14965fdd47357cdb76f96132017b043b9cd91aea525848ac67f27e4f6c3deb3c_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.8;
    3 | 
    4 | import {IRescuableBase} from './IRescuableBase.sol';
```

_file_excerpt · [lib/solidity-utils/src/contracts/utils/interfaces/IRescuable721.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/utils/interfaces/IRescuable721.sol#L2) · line 2 · SHA-256 f64bd4eb0d63eddbeb5de692a797c9aae680c37454b5eca8f1da11d8ea2983a4_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.8;
    3 | 
    4 | /**
```

_file_excerpt · [lib/solidity-utils/src/contracts/utils/interfaces/IRescuableBase.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/src/contracts/utils/interfaces/IRescuableBase.sol#L2) · line 2 · SHA-256 f64bd4eb0d63eddbeb5de692a797c9aae680c37454b5eca8f1da11d8ea2983a4_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.8;
    3 | 
    4 | /**
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06519 — Плавающая версия компилятора (>=0.8.24) в 1 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:>=0.8.24`
- Источник данных: lib/solidity-utils/zksync/src/contracts/transparent-proxy/TransparentProxyFactoryZkSync.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma >=0.8.24 в 1 файл(ах), впервые в lib/solidity-utils/zksync/src/contracts/transparent-proxy/TransparentProxyFactoryZkSync.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте lib/solidity-utils/zksync/src/contracts/transparent-proxy/TransparentProxyFactoryZkSync.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/zksync/src/contracts/transparent-proxy/TransparentProxyFactoryZkSync.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/zksync/src/contracts/transparent-proxy/TransparentProxyFactoryZkSync.sol#L2) · line 2 · SHA-256 a657707a0166b09f8b36092851cd07fbb6a9ce291565bfd627ca8038297b9a95_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity >=0.8.24;
    3 | 
    4 | import {TransparentProxyFactoryBase} from '../../../../src/contracts/transparent-proxy/TransparentProxyFactoryBase.sol';
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06527 — Плавающая версия компилятора (^0.8.17) в 2 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.17`
- Источник данных: src/contracts/extensions/stata-token/ERC20AaveLMUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.17 в 2 файл(ах), впервые в src/contracts/extensions/stata-token/ERC20AaveLMUpgradeable.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте src/contracts/extensions/stata-token/ERC20AaveLMUpgradeable.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/extensions/stata-token/ERC20AaveLMUpgradeable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/extensions/stata-token/ERC20AaveLMUpgradeable.sol#L2) · line 2 · SHA-256 21291d3e7ca0e0403937e245bb8a6eca24e274760e069f5accc7441e24375e5b_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.17;
    3 | 
    4 | import {ERC20Upgradeable} from 'openzeppelin-contracts-upgradeable/contracts/token/ERC20/ERC20Upgradeable.sol';
```

_file_excerpt · [src/contracts/extensions/stata-token/ERC4626StataTokenUpgradeable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/extensions/stata-token/ERC4626StataTokenUpgradeable.sol#L2) · line 2 · SHA-256 e4f7afb0b75738dbe223abd04ec45905945431a2d367cb89fceb9220c56841c2_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.17;
    3 | 
    4 | import {ERC4626Upgradeable, Math, IERC4626} from 'openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC4626Upgradeable.sol';
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06528 — Плавающая версия компилятора (^0.8.18) в 10 файл(ах)

- Серьёзность: **Низкая** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `solidity:pragma:^0.8.18`
- Источник данных: src/contracts/extensions/v3-config-engine/AaveV3ConfigEngine.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.4 / 100
- CVSS v3.1: неприменимо

pragma ^0.8.18 в 10 файл(ах), впервые в src/contracts/extensions/v3-config-engine/AaveV3ConfigEngine.sol:2. (см. SWC-103)

**Возможные последствия.** Контракты могут быть развёрнуты непроверенной версией компилятора. Фактический компилятор задаёт конфигурация сборки, которую эта проверка не читает.

**Шаги воспроизведения.**

```
Откройте src/contracts/extensions/v3-config-engine/AaveV3ConfigEngine.sol:2 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/extensions/v3-config-engine/AaveV3ConfigEngine.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/extensions/v3-config-engine/AaveV3ConfigEngine.sol#L2) · line 2 · SHA-256 bc2d074ade6ff76f0f9fd8746a7cd9013ed8811bbcc5f0ed9937f32b583cb0b7_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.18;
    3 | 
    4 | import {CapsEngine} from './libraries/CapsEngine.sol';
```

_file_excerpt · [src/contracts/extensions/v3-config-engine/EngineFlags.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/extensions/v3-config-engine/EngineFlags.sol#L2) · line 2 · SHA-256 6dcfa481195d4d5ca533b0f4bc147d5723e90fed760088d59c5a8a94ba43eec6_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.18;
    3 | 
    4 | library EngineFlags {
```

_file_excerpt · [src/contracts/extensions/v3-config-engine/IAaveV3ConfigEngine.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/extensions/v3-config-engine/IAaveV3ConfigEngine.sol#L2) · line 2 · SHA-256 a288afc4df79d5498c8fd3eb98fbf6405acbcdc5db47b01026cb3ecfb80d214c_

```
    1 | // SPDX-License-Identifier: MIT
    2 | pragma solidity ^0.8.18;
    3 | 
    4 | import {IPool} from '../../interfaces/IPool.sol';
```

_file_excerpt · [src/contracts/extensions/v3-config-engine/libraries/BorrowEngine.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/extensions/v3-config-engine/libraries/BorrowEngine.sol#L2) · line 2 · SHA-256 3e79704ae9d0caf9067fc913cc0cdcea70cf45eef97551f3d4e5b00d2de27b62_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.18;
    3 | 
    4 | import {EngineFlags} from '../EngineFlags.sol';
```

_file_excerpt · [src/contracts/extensions/v3-config-engine/libraries/CapsEngine.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/extensions/v3-config-engine/libraries/CapsEngine.sol#L2) · line 2 · SHA-256 3e79704ae9d0caf9067fc913cc0cdcea70cf45eef97551f3d4e5b00d2de27b62_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.18;
    3 | 
    4 | import {EngineFlags} from '../EngineFlags.sol';
```

_file_excerpt · [src/contracts/extensions/v3-config-engine/libraries/CollateralEngine.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/extensions/v3-config-engine/libraries/CollateralEngine.sol#L2) · line 2 · SHA-256 864819c389369ac5c245a4400de3ede2506a2e611893c833aa6ea53f79f4d853_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.18;
    3 | 
    4 | import {DataTypes} from '../../../protocol/libraries/types/DataTypes.sol';
```

_file_excerpt · [src/contracts/extensions/v3-config-engine/libraries/EModeEngine.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/extensions/v3-config-engine/libraries/EModeEngine.sol#L2) · line 2 · SHA-256 f3fa8a68cbb51e71dd670b0824743219526b59fdb839dca214eb6963a9a704e8_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.18;
    3 | 
    4 | import {SafeCast} from 'openzeppelin-contracts/contracts/utils/math/SafeCast.sol';
```

_file_excerpt · [src/contracts/extensions/v3-config-engine/libraries/ListingEngine.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/extensions/v3-config-engine/libraries/ListingEngine.sol#L2) · line 2 · SHA-256 c1702751d7caa76faa1518991e51d8b563906a681e2fea08e277e461839fa781_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.18;
    3 | 
    4 | import {IAaveV3ConfigEngine as IEngine, IPoolConfigurator, IDefaultInterestRateStrategyV2} from '../IAaveV3ConfigEngine.sol';
```

_file_excerpt · [src/contracts/extensions/v3-config-engine/libraries/PriceFeedEngine.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/extensions/v3-config-engine/libraries/PriceFeedEngine.sol#L2) · line 2 · SHA-256 5b99f79ab9ea96a4858fe9e423dd00957460fcc6239d08b916223316d5f1deff_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.18;
    3 | 
    4 | import {IAaveV3ConfigEngine as IEngine, IAaveOracle} from '../IAaveV3ConfigEngine.sol';
```

_file_excerpt · [src/contracts/extensions/v3-config-engine/libraries/RateEngine.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/extensions/v3-config-engine/libraries/RateEngine.sol#L2) · line 2 · SHA-256 d5e33d92057ad3643644a2524e07ad10878cb5f333bd5907bd735cfce3fdf771_

```
    1 | // SPDX-License-Identifier: BUSL-1.1
    2 | pragma solidity ^0.8.18;
    3 | 
    4 | import {IDefaultInterestRateStrategyV2} from '../../../interfaces/IDefaultInterestRateStrategyV2.sol';
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Зафиксируйте версию компилятора, использованную при тестировании.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06487 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol: restricted

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: restricted. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol) · multiple · SHA-256 36ed478689eb7537103955dd954f943862d16e4135ccd297de1e6c99b9b9e5e5_

```
Privileged functions: restricted
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06488 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol: restricted

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: restricted. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol) · multiple · SHA-256 36ed478689eb7537103955dd954f943862d16e4135ccd297de1e6c99b9b9e5e5_

```
Privileged functions: restricted
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06489 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol: transferOwnership

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: transferOwnership. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol) · multiple · SHA-256 3ef6a6924988649e26a7e42a450b6976f80844a318d3ab2418fc99e4bae2bcee_

```
Privileged functions: transferOwnership
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06490 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol: renounceOwnership, transferOwnership

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: renounceOwnership, transferOwnership. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol) · multiple · SHA-256 c9178db25d8ef1b1a83ff9fe952090d86c1ef54a1f84a5a67cc0aac7fdd62bd6_

```
Privileged functions: renounceOwnership, transferOwnership
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06491 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol: relay

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: relay. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol) · multiple · SHA-256 7ffca126961e19e9d9b0edb533fbaeacef6491d5098a94c1d9d5b988a15cb6ba_

```
Privileged functions: relay
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06492 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol: setLateQuorumVoteExtension

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: setLateQuorumVoteExtension. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol) · multiple · SHA-256 514805472eac509275a6bf6ad6edb5f54cc24756ff9976c1eb00d142f771616d_

```
Privileged functions: setLateQuorumVoteExtension
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06493 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol: setVotingDelay, setVotingPeriod, setProposalThreshold

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: setVotingDelay, setVotingPeriod, setProposalThreshold. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol) · multiple · SHA-256 86374e75349ee43fad2906180e81f23f3c94d19c2162c84a665cf6d22130b06e_

```
Privileged functions: setVotingDelay, setVotingPeriod, setProposalThreshold
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06494 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol: setBaseDelaySeconds, setAccessManagerIgnored

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: setBaseDelaySeconds, setAccessManagerIgnored. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol) · multiple · SHA-256 f2f0ae2a1314268db485c56a4fe1f2d974856fd30405d8e1b223f1102f2a16d6_

```
Privileged functions: setBaseDelaySeconds, setAccessManagerIgnored
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06495 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol: updateTimelock

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateTimelock. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol) · multiple · SHA-256 825de8a0266ca176b55c917fd9450222f4d40ce841c16a9f026715c5a07f3d75_

```
Privileged functions: updateTimelock
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06496 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol: updateTimelock

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateTimelock. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol) · multiple · SHA-256 825de8a0266ca176b55c917fd9450222f4d40ce841c16a9f026715c5a07f3d75_

```
Privileged functions: updateTimelock
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06497 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol: updateQuorumNumerator

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateQuorumNumerator. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol) · multiple · SHA-256 37d9e023fde908bbc2e9347f91ad2aa3006ddd93480c2ac0413f2847e2b727b4_

```
Privileged functions: updateQuorumNumerator
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06500 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol: restricted

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: restricted. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol) · multiple · SHA-256 36ed478689eb7537103955dd954f943862d16e4135ccd297de1e6c99b9b9e5e5_

```
Privileged functions: restricted
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06501 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol: restricted

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: restricted. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol) · multiple · SHA-256 36ed478689eb7537103955dd954f943862d16e4135ccd297de1e6c99b9b9e5e5_

```
Privileged functions: restricted
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06502 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol: renounceOwnership, transferOwnership

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: renounceOwnership, transferOwnership. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol) · multiple · SHA-256 c9178db25d8ef1b1a83ff9fe952090d86c1ef54a1f84a5a67cc0aac7fdd62bd6_

```
Privileged functions: renounceOwnership, transferOwnership
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06503 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol: transferOwnership

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: transferOwnership. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol) · multiple · SHA-256 3ef6a6924988649e26a7e42a450b6976f80844a318d3ab2418fc99e4bae2bcee_

```
Privileged functions: transferOwnership
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06504 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol: relay

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: relay. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol) · multiple · SHA-256 7ffca126961e19e9d9b0edb533fbaeacef6491d5098a94c1d9d5b988a15cb6ba_

```
Privileged functions: relay
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06505 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol: setLateQuorumVoteExtension

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: setLateQuorumVoteExtension. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol) · multiple · SHA-256 514805472eac509275a6bf6ad6edb5f54cc24756ff9976c1eb00d142f771616d_

```
Privileged functions: setLateQuorumVoteExtension
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06506 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol: setVotingDelay, setVotingPeriod, setProposalThreshold

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: setVotingDelay, setVotingPeriod, setProposalThreshold. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol) · multiple · SHA-256 86374e75349ee43fad2906180e81f23f3c94d19c2162c84a665cf6d22130b06e_

```
Privileged functions: setVotingDelay, setVotingPeriod, setProposalThreshold
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06507 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol: setBaseDelaySeconds, setAccessManagerIgnored

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: setBaseDelaySeconds, setAccessManagerIgnored. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol) · multiple · SHA-256 f2f0ae2a1314268db485c56a4fe1f2d974856fd30405d8e1b223f1102f2a16d6_

```
Privileged functions: setBaseDelaySeconds, setAccessManagerIgnored
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06508 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol: updateTimelock

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateTimelock. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol) · multiple · SHA-256 825de8a0266ca176b55c917fd9450222f4d40ce841c16a9f026715c5a07f3d75_

```
Privileged functions: updateTimelock
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06509 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol: updateTimelock

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateTimelock. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol) · multiple · SHA-256 825de8a0266ca176b55c917fd9450222f4d40ce841c16a9f026715c5a07f3d75_

```
Privileged functions: updateTimelock
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06510 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol: updateQuorumNumerator

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: updateQuorumNumerator. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol) · multiple · SHA-256 37d9e023fde908bbc2e9347f91ad2aa3006ddd93480c2ac0413f2847e2b727b4_

```
Privileged functions: updateQuorumNumerator
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06512 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol: upgradeTo

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: upgradeTo. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol) · multiple · SHA-256 02e606b6560ec4a99c06589dd8655178cca253b457dcec0438b77dd4a8cb04f5_

```
Privileged functions: upgradeTo
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06513 — Привилегированные административные функции в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol: upgradeAndCall

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol`
- Источник данных: lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: upgradeAndCall. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol) · multiple · SHA-256 08d87f8ddab73b6f3211d313d176dd5e3323cdca43425bff268f49bee3960937_

```
Privileged functions: upgradeAndCall
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06521 — Привилегированные административные функции в src/contracts/dependencies/openzeppelin/contracts/Ownable.sol: renounceOwnership, transferOwnership

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:src/contracts/dependencies/openzeppelin/contracts/Ownable.sol`
- Источник данных: src/contracts/dependencies/openzeppelin/contracts/Ownable.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: renounceOwnership, transferOwnership. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле src/contracts/dependencies/openzeppelin/contracts/Ownable.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/dependencies/openzeppelin/contracts/Ownable.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/dependencies/openzeppelin/contracts/Ownable.sol) · multiple · SHA-256 c9178db25d8ef1b1a83ff9fe952090d86c1ef54a1f84a5a67cc0aac7fdd62bd6_

```
Privileged functions: renounceOwnership, transferOwnership
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06529 — Привилегированные административные функции в src/contracts/helpers/WrappedTokenGatewayV3.sol: emergencyTokenTransfer, emergencyEtherTransfer

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:src/contracts/helpers/WrappedTokenGatewayV3.sol`
- Источник данных: src/contracts/helpers/WrappedTokenGatewayV3.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: emergencyTokenTransfer, emergencyEtherTransfer. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле src/contracts/helpers/WrappedTokenGatewayV3.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/helpers/WrappedTokenGatewayV3.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/helpers/WrappedTokenGatewayV3.sol) · multiple · SHA-256 ae1eebfc8a6036d2c29389643704937275208626f52b0ec0d47ee7660b260342_

```
Privileged functions: emergencyTokenTransfer, emergencyEtherTransfer
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06531 — Привилегированные административные функции в src/contracts/protocol/configuration/PoolAddressesProvider.sol: setMarketId, setAddress, setAddressAsProxy, setPoolImpl, setPoolConfiguratorImpl, setPriceOracle, setACLManager, setACLAdmin, setPriceOracleSentinel, setPoolDataProvider

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:src/contracts/protocol/configuration/PoolAddressesProvider.sol`
- Источник данных: src/contracts/protocol/configuration/PoolAddressesProvider.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: setMarketId, setAddress, setAddressAsProxy, setPoolImpl, setPoolConfiguratorImpl, setPriceOracle, setACLManager, setACLAdmin, setPriceOracleSentinel, setPoolDataProvider. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле src/contracts/protocol/configuration/PoolAddressesProvider.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/protocol/configuration/PoolAddressesProvider.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/protocol/configuration/PoolAddressesProvider.sol) · multiple · SHA-256 d9e3ce89706a59f05d6add295039ebc76461b899e219aba0621503fb06133a16_

```
Privileged functions: setMarketId, setAddress, setAddressAsProxy, setPoolImpl, setPoolConfiguratorImpl, setPriceOracle, setACLManager, setACLAdmin, setPriceOracleSentinel, setPoolDataProvider
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06532 — Привилегированные административные функции в src/contracts/protocol/configuration/PoolAddressesProviderRegistry.sol: registerAddressesProvider, unregisterAddressesProvider

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:src/contracts/protocol/configuration/PoolAddressesProviderRegistry.sol`
- Источник данных: src/contracts/protocol/configuration/PoolAddressesProviderRegistry.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: registerAddressesProvider, unregisterAddressesProvider. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле src/contracts/protocol/configuration/PoolAddressesProviderRegistry.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/protocol/configuration/PoolAddressesProviderRegistry.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/protocol/configuration/PoolAddressesProviderRegistry.sol) · multiple · SHA-256 684daa325cd4d1376235ab82aadedfa879f161f18b836cd5a6c3f149b4c29b55_

```
Privileged functions: registerAddressesProvider, unregisterAddressesProvider
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06534 — Привилегированные административные функции в src/contracts/rewards/EmissionManager.sol: setClaimer, setEmissionAdmin, setRewardsController

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:src/contracts/rewards/EmissionManager.sol`
- Источник данных: src/contracts/rewards/EmissionManager.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: setClaimer, setEmissionAdmin, setRewardsController. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле src/contracts/rewards/EmissionManager.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/contracts/rewards/EmissionManager.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/contracts/rewards/EmissionManager.sol) · multiple · SHA-256 0bb64d88a83454d697b64f8400922d89f185270e446426625da15a5feb33c5ef_

```
Privileged functions: setClaimer, setEmissionAdmin, setRewardsController
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06535 — Привилегированные административные функции в src/deployments/projects/aave-v3-batched/batches/AaveV3SetupBatch.sol: setupAaveV3Market, setMarketReport, setProtocolDataProvider, transferMarketOwnership

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `contract:src/deployments/projects/aave-v3-batched/batches/AaveV3SetupBatch.sol`
- Источник данных: src/deployments/projects/aave-v3-batched/batches/AaveV3SetupBatch.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 38.5 / 100
- CVSS v3.1: неприменимо

Функции, защищённые модификаторами владельца/ролей: setupAaveV3Market, setMarketReport, setProtocolDataProvider, transferMarketOwnership. (см. —)

**Возможные последствия.** Риск централизации: компрометация ключа администратора компрометирует протокол.

**Шаги воспроизведения.**

```
Откройте contract в предоставленном файле src/deployments/projects/aave-v3-batched/batches/AaveV3SetupBatch.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/deployments/projects/aave-v3-batched/batches/AaveV3SetupBatch.sol](https://github.com/aave-dao/aave-v3-origin/blob/8305565ae342f1773c42cd2e4593f175fe5968a0/src/deployments/projects/aave-v3-batched/batches/AaveV3SetupBatch.sol) · multiple · SHA-256 7e54ce2c9b8d0fe8ad6b6bd9615ee248a4c4615916077187ef2eccd78b3d0c85_

```
Privileged functions: setupAaveV3Market, setMarketReport, setProtocolDataProvider, transferMarketOwnership
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте мультиподпись/таймлок для ролей администратора и документируйте их.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-06537 — 197 бюллетеней в 53 пакет(ах) npm, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:npm:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 17.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 197 бюллетеней (103 с оценкой high или critical) для 53 пакет(ов) npm, которые подтягивают только инструменты разработки или сборки (lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json, lib/solidity-utils/package-lock.json, package-lock.json): например, @babel/runtime@7.22.15 [dev]: GHSA-968p-4wvh-cqc8; @babel/runtime@7.26.9 [dev]: GHSA-968p-4wvh-cqc8; @fastify/busboy@2.0.0 [dev]: GHSA-gxm5-99cw-xjw9, GHSA-x8mw-p69m-v3mx; adm-zip@0.4.16 [dev]: GHSA-7q85-xj36-vmfc, GHSA-8238-w5pm-2374, GHSA-c6fg-446q-cg94, GHSA-j5f4-cc29-5x44, GHSA-p634-w6r4-rjp2, GHSA-rcw4-f5rp-g42v, GHSA-xcpc-8h2w-3j85; ajv@6.12.6 [dev]: GHSA-2g4f-4pwh-qvx6. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json, lib/solidity-utils/package-lock.json, package-lock.json.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json · SHA-256 8bf9311412f0d5ff02697949a7e6e1b43f373ef12e25c19cd155713ed9e3236e_

```
@babel/runtime@7.22.15 [dev]: GHSA-968p-4wvh-cqc8
@babel/runtime@7.26.9 [dev]: GHSA-968p-4wvh-cqc8
@fastify/busboy@2.0.0 [dev]: GHSA-gxm5-99cw-xjw9, GHSA-x8mw-p69m-v3mx
adm-zip@0.4.16 [dev]: GHSA-7q85-xj36-vmfc, GHSA-8238-w5pm-2374, GHSA-c6fg-446q-cg94, GHSA-j5f4-cc29-5x44, GHSA-p634-w6r4-rjp2, GHSA-rcw4-f5rp-g42v, GHSA-xcpc-8h2w-3j85
ajv@6.12.6 [dev]: GHSA-2g4f-4pwh-qvx6
ajv@8.12.0 [dev]: GHSA-2g4f-4pwh-qvx6
axios@1.6.8 [dev]: GHSA-35jp-ww65-95wh, GHSA-3g43-6gmg-66jw, GHSA-3p68-rc4w-qgx5, GHSA-3w6x-2g7m-8v23, GHSA-42h9-826w-cgv3, GHSA-43fc-jf86-j433, GHSA-445q-vr5w-6q77, GHSA-4hjh-wcwx-xvwj, GHSA-5c9x-8gcm-mpgx, GHSA-62hf-57xw-28j9, GHSA-6chq-wfr3-2hj9, GHSA-7q8q-rj6j-mhjq, GHSA-898c-q2cr-xwhg, GHSA-8hc4-vh64-cxmj, GHSA-9fr6-4gfg-395g, GHSA-fvcv-3m26-pcqx, GHSA-hfxv-24rg-xrqf, GHSA-j5f8-grm9-p9fc, GHSA-j8rh-479h-cp32, GHSA-jr5f-v2jv-69x6
base-x@3.0.9 [dev]: GHSA-xq7p-g2vc-g82p
bn.js@4.11.6 [dev]: GHSA-378v-28hj-76wf
bn.js@4.12.0 [dev]: GHSA-378v-28hj-76wf
bn.js@5.2.1 [dev]: GHSA-378v-28hj-76wf
brace-expansion@1.1.11 [dev]: GHSA-3jxr-9vmj-r5cp, GHSA-6j4f-fj2g-mc7p, GHSA-f886-m6hf-6m8v, GHSA-mh99-v99m-4gvg, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895, GHSA-v6h2-p8h4-qcjw
brace-expansion@2.0.1 [dev]: GHSA-3jxr-9vmj-r5cp, GHSA-6j4f-fj2g-mc7p, GHSA-f886-m6hf-6m8v, GHSA-mh99-v99m-4gvg, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895, GHSA-v6h2-p8h4-qcjw
brace-expansion@4.0.0 [dev]: GHSA-3jxr-9vmj-r5cp, GHSA-6j4f-fj2g-mc7p, GHSA-f886-m6hf-6m8v, GHSA-mh99-v99m-4gvg, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895, GHSA-v6h2-p8h4-qcjw
cipher-base@1.0.4 [dev]: GHSA-cpq7-6gpm-g9rc
cookie@0.4.2 [dev]: GHSA-pxg6-pf52-xh8x
cross-spawn@5.1.0 [dev]: GHSA-3xgq-45jj-v275
cross-spawn@7.0.3 [dev]: GHSA-3xgq-45jj-v275
csv-parse@4.16.3 [dev]: GHSA-8cw4-87c7-c6xx
diff@4.0.2 [dev]: GHSA-73rr-hh4g-fpgx
diff@5.0.0 [dev]: GHSA-73rr-hh4g-fpgx
elliptic@6.5.4 [dev]: GHSA-434g-2637-qmqr, GHSA-49q7-c7j4-3p7m, GHSA-848j-6mx2-7j84, GHSA-977x-g7h5-7qgw, GHSA-f7q4-pwc6-w24p, GHSA-fc9h-whq2-v747, GHSA-vjh7-7g9h-fjfh
flatted@3.2.9 [dev]: GHSA-25h7-pfq9-p65f, GHSA-rf6f-7fwh-wjgh
follow-redirects@1.15.6 [dev]: GHSA-r4q5-vmmm-2653
form-data@4.0.0 [dev]: GHSA-fjxv-7rqg-78g4, GHSA-hmw2-7cc7-3qxx
glob@10.3.10 [dev]: GHSA-5j98-mcp5-4vw2
glob@11.0.0 [dev]: GHSA-5j98-mcp5-4vw2
handlebars@4.7.8 [dev]: GHSA-2qvq-rjwj-gvw9, GHSA-2w6w-674q-4c4q, GHSA-3mfm-83xf-c92r, GHSA-442j-39wm-28r2, GHSA-7rx3-28cr-v5wh, GHSA-8r5x-fm3f-whwj, GHSA-9cx6-37pm-9jff, GHSA-p8wg-vrv2-v86f, GHSA-xhpv-hc6g-r9c6, GHSA-xjpj-3mr7-gcpf, GHSA-xw65-4hp5-5hc7
immutable@4.3.4 [dev]: GHSA-v56q-mh7h-f735, GHSA-wf6x-7x77-mvgw, GHSA-xvcm-6775-5m9r
js-yaml@3.14.1 [dev]: GHSA-2883-xcg3-v3hh, GHSA-52cp-r559-cp3m, GHSA-5p4m-2wfm-xmqj, GHSA-h67p-54hq-rp68, GHSA-mh29-5h37-fv8m
js-yaml@3.14.2 [dev]: GHSA-2883-xcg3-v3hh, GHSA-52cp-r559-cp3m, GHSA-5p4m-2wfm-xmqj, GHSA-h67p-54hq-rp68
js-yaml@4.1.0 [dev]: GHSA-2883-xcg3-v3hh, GHSA-52cp-r559-cp3m, GHSA-5p4m-2wfm-xmqj, GHSA-h67p-54hq-rp68, GHSA-mh29-5h37-fv8m
js-yaml@4.1.1 [dev]: GHSA-2883-xcg3-v3hh, GHSA-52cp-r559-cp3m, GHSA-5p4m-2wfm-xmqj, GHSA-h67p-54hq-rp68
lodash@4.17.21 [dev]: GHSA-f23m-r3pf-42rh, GHSA-r5fr-rjxr-66jc, GHSA-xxjr-mmjv-4gpg
micromatch@4.0.5 [dev]: GHSA-952p-6rrq-rcjv
minimatch@10.0.0 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
minimatch@3.1.2 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
minimatch@5.0.1 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
minimatch@5.1.6 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
minimatch@9.0.3 [dev]: GHSA-23c5-xmqv-rm74, GHSA-3ppc-4f35-3m26, GHSA-7r86-cg39-jmmj
nanoid@3.3.3 [dev]: GHSA-28wg-ghj8-5hjv, GHSA-2v37-7h3g-55p8, GHSA-mwcw-c2x4-8c55, GHSA-xwg4-73v4-xw9w
pbkdf2@3.1.2 [dev]: GHSA-477h-4r7f-fvrx, GHSA-h7cp-r72f-jxh6, GHSA-v62p-rq8g-8h59
picomatch@2.3.1 [dev]: GHSA-3v7f-55p6-f55p, GHSA-c2c7-rcm5-vvqj
secp256k1@4.0.3 [dev]: GHSA-584q-6j8j-r5pm
serialize-javascript@6.0.0 [dev]: GHSA-5c6j-r48x-rmvq, GHSA-76p7-773f-r4q5, GHSA-m5mm-p8h7-m29v, GHSA-qj8w-gfj5-8c6v
sha.js@2.4.11 [dev]: GHSA-95m3-7q98-8xr5
tmp@0.0.33 [dev]: GHSA-52f5-9888-hmc6, GHSA-ph9p-34f9-6g65
undici@5.28.4 [dev]: GHSA-2m5v-pch6-74hx, GHSA-2mjp-6q6p-2qxm, GHSA-35p6-xmwp-9g52, GHSA-4992-7rv2-5pvq, GHSA-8xcm-r25x-g524, GHSA-9fm3-97px-rjf6, GHSA-c76h-2ccp-4975, GHSA-cxrh-j4jr-qwg3, GHSA-g8m3-5g58-fq7m, GHSA-g9mf-h72j-4rw9, GHSA-m8rv-5g2x-5cg5, GHSA-p88m-4jfj-68fv, GHSA-qrxm-fqhp-jwvm, GHSA-r53p-7pc4-xj5r, GHSA-v3r7-h72x-cjcm, GHSA-v9p9-hfj2-hcw8, GHSA-vrm6-8vpv-qv8q, GHSA-vxpw-j846-p89q
undici@6.12.0 [dev]: GHSA-2m5v-pch6-74hx, GHSA-2mjp-6q6p-2qxm, GHSA-35p6-xmwp-9g52, GHSA-4992-7rv2-5pvq, GHSA-4qv8-2p9j-2685, GHSA-8xcm-r25x-g524, GHSA-9fm3-97px-rjf6, GHSA-c76h-2ccp-4975, GHSA-cxrh-j4jr-qwg3, GHSA-f269-vfmq-vjvj, GHSA-g8m3-5g58-fq7m, GHSA-g9mf-h72j-4rw9, GHSA-m8rv-5g2x-5cg5, GHSA-p88m-4jfj-68fv, GHSA-qrxm-fqhp-jwvm, GHSA-r53p-7pc4-xj5r, GHSA-rfgv-xxqx-mfg5, GHSA-v3r7-h72x-cjcm, GHSA-v9p9-hfj2-hcw8, GH
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06536 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-29 06:16 UTC
- Балл приоритета: 14.5 / 100
- CVSS v3.1: неприменимо

В 12 манифестах зависимостей QSI нашёл криптобиблиотеки (@noble/curves, @noble/hashes, @noble/secp256k1, elliptic, ethers, secp256k1, tweetnacl), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/package.json, lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/package.json, lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json, lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package.json, lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/solhint-custo · SHA-256 49a0b2cfa22c999965f749622f06b48a6edd611e28411faaf48b40bad22e538f_

```
Crypto libraries: @noble/curves, @noble/hashes, @noble/secp256k1, elliptic, ethers, secp256k1, tweetnacl
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
| **подпись транзакций и сообщений** | ECDSA (2) | QSI-2026-06481 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | ECDSA (2) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (59) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (59) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- slither: 520 (примеры: slither is not installed on the server (pip install slither-analyzer + solc))
- osv_advisories: 2 (примеры: npm/axios@1.6.8: 31 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest; npm/undici@6.12.0: 21 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest)

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P1 | QSI-2026-06514 | Ограничьте цели delegatecall доверенными неизменяемыми реализациями. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-06520 | Ограничьте цели delegatecall доверенными неизменяемыми реализациями. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-06522 | Ограничьте цели delegatecall доверенными неизменяемыми реализациями. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-06523 | Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-06524 | Ограничьте цели delegatecall доверенными неизменяемыми реализациями. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-06525 | Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-06526 | Ограничьте цели delegatecall доверенными неизменяемыми реализациями. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-06530 | Ограничьте цели delegatecall доверенными неизменяемыми реализациями. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-06533 | Используйте OpenZeppelin Initializable (модификатор initializer) и отключите инициализаторы в конструкторе реализации. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-06482 | Используйте OpenZeppelin ECDSA.recover с разделением доменов EIP-712 и nonce. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P2 | QSI-2026-06515 | Используйте OpenZeppelin ECDSA.recover с разделением доменов EIP-712 и nonce. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-06481 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06480 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06483 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06484 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06485 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06486 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06498 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06499 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06511 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06516 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06517 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06518 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06519 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06527 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P3 | QSI-2026-06528 | Зафиксируйте версию компилятора, использованную при тестировании. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06481 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06487 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06488 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06489 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06490 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06491 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06492 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06493 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06494 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06495 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06496 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06497 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06500 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06501 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06502 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06503 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06504 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06505 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06506 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06507 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06508 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06509 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06510 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06512 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06513 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06521 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06529 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06531 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06532 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06534 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06535 | Используйте мультиподпись/таймлок для ролей администратора и документируйте их. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P4 | QSI-2026-06537 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |

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
| Keccak-256 | Keccak-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 59 | 59 | certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol:109; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/manager/AccessManagerUpgradeable.sol:625; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol:34 |
| Crypto library | 1.0.3 | tweetnacl (TweetNaCl) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json |
| Crypto library | 1.1.0 | @noble/curves (noble-curves) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json |
| Crypto library | 1.1.2 | @noble/hashes (noble-hashes) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json |
| Crypto library | 1.2.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json |
| Crypto library | 1.2.0 | @noble/curves (noble-curves) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json |
| Crypto library | 1.3.0 | @noble/curves (noble-curves) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json |
| Crypto library | 1.3.1 | @noble/hashes (noble-hashes) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json |
| Crypto library | 1.3.2 | @noble/hashes (noble-hashes) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json |
| Crypto library | 1.3.3 | @noble/hashes (noble-hashes) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json |
| Crypto library | 1.7.1 | @noble/secp256k1 (noble-curves) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json |
| Crypto library | 4.0.3 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json |
| Crypto library | 6.5.4 | elliptic (elliptic (Node)) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json |
| Crypto library | 6.7.1 | ethers (ethers.js) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json |
| Crypto library | ^6.7.1 | ethers (ethers.js) | н/п | допустимо | 2 | 2 | lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package.json; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package.json |
| ECDSA | secp256k1 (ecrecover) |  | уязвим (Шор) | допустимо | 2 | 2 | certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol:98; lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol:148 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| certora/atoken-with-delegation/harness/ATokenWithDelegation_Harness.sol | 5219 | `bd4801cfdc7ceb0ece2ed11f68d2ddb641ee5381e287cd966d0f796939d92eb0` | 0 |
| certora/atoken-with-delegation/harness/DummyERC20Impl.sol | 1490 | `ee886c556ba043085a13dea66944e34686033388f9bce7fb614c50298a9552a6` | 0 |
| certora/atoken-with-delegation/harness/DummyERC20_aTokenUnderlying.sol | 152 | `5ab15bd047b5c50634e450cd39c7114ab8ffdc6824e8d8619368c157449866e7` | 0 |
| certora/atoken-with-delegation/harness/SimpleERC20.sol | 1582 | `c7c4838e044dcc6ff18aac280eb3bfd36ae1fc38d83260e12314c2933ea3af34` | 0 |
| certora/atoken-with-delegation/harness/SymbolicLendingPoolL1.sol | 2454 | `5377d17d0c6adf7de4480e5eb05219e37a138cb442fd0c2719697a7ec7279339` | 0 |
| certora/basic/harness/ATokenHarness.sol | 1598 | `fcb7dc84077a9c4a9d794b312443434de3fc155c5595bd25163d62845b6435d9` | 0 |
| certora/basic/harness/DummyContract.sol | 166 | `b9bf31caa85a3a04e4955cc92dcb8431f579646e6115ec4268a9b860d9f0a31e` | 0 |
| certora/basic/harness/EModeConfigurationHarness.sol | 1345 | `33e620181c35914fd6e15d3b68606eb825b5de573cbba835c1135378279608ee` | 0 |
| certora/basic/harness/PoolHarness.sol | 2950 | `e0cfca5681d7ea5902353630434ce999176386b3cce9b1ab8ce8f47167783595` | 0 |
| certora/basic/harness/PoolInstanceHarness.sol | 1638 | `71f3110e8cfd28d1900409e91051101c93c696d11f0f3508a5aa463bf5e8d331` | 0 |
| certora/basic/harness/ReserveConfigurationHarness.sol | 9229 | `4a0cce4afa7a32cd956eb05a74023b3cf483707da9ca866871daa40ee012c7f4` | 0 |
| certora/basic/harness/SimpleERC20.sol | 1584 | `86f5c97d33ff555420c48848655a52715800a18f8485d8dbd13b0bd14ac6b49d` | 0 |
| certora/basic/harness/SymbolicPriceOracle.sol | 596 | `aeb9be28bb1c99ac551c0482af7b09022f80e0822e70cda693daf38e2e9ae28b` | 0 |
| certora/basic/harness/UserConfigurationHarness.sol | 2547 | `0c0199cd8f022642a5cdf055ef0aa18bd6ee3e0463777abbcb2d306657081934` | 0 |
| certora/basic/harness/VariableDebtTokenHarness.sol | 724 | `6b5fd6e11305923164c110c445e4f3ba5cbc0734608de0b269e1c264b2e803a5` | 0 |
| certora/math-calculations/harnesses/PoolInstanceHarness.sol | 3421 | `34d1b5acf14e2299f1ae614f8f7aba4b309aadbc7e32f737e3a49d00538da4f9` | 0 |
| certora/math-calculations/harnesses/Utilities.sol | 2611 | `9df1a52bf6b04ad1e087e51d95a7f4ca602f0eda65ee9d55ea03ae33d2a0b271` | 0 |
| certora/solvency/harnesses/Aave/DummyContract.sol | 166 | `b9bf31caa85a3a04e4955cc92dcb8431f579646e6115ec4268a9b860d9f0a31e` | 0 |
| certora/solvency/harnesses/Aave/PoolInstanceForAToken.sol | 778 | `588d320c2b2eae282a67bc70b2df21c9efb30784afbc0847f2fa83c290671e5a` | 0 |
| certora/solvency/harnesses/Aave/PoolInstanceHarness.sol | 2158 | `6197e42e7723ac377d321035a417e7d6fcca54037e939787b9421a5c6774cdc2` | 0 |
| certora/solvency/harnesses/ERC20Like/DummyERC20A.sol | 1202 | `4eb8e726e65e4407ec112c1d012f3972f91e8198440ed45cefb64124070f3c5c` | 0 |
| certora/solvency/harnesses/ERC20Like/DummyERC20B.sol | 1202 | `3b3ca522c342987a2ffc4dbc37459c26ee23a8b6b76aaf8af86fde60fb0f0a16` | 0 |
| certora/solvency/harnesses/ERC20Like/DummyWeth.sol | 1417 | `dc3ad0140fe4ab2362f9f03a746ac53d3a9e892ef951716c1735c26ed734f815` | 0 |
| certora/solvency/harnesses/Utilities.sol | 1468 | `be7e23ac78cad5ac9e7cd6ca7d16a91e47cf476db2f26c19bc78b20957631af7` | 0 |
| certora/stata/harness/StataTokenV2Harness.sol | 2390 | `9933493dfbb819d68e48e2c60d5c0d3e68b83f948c06704d0e8ec0259fa16a48` | 0 |
| certora/stata/harness/pool/SymbolicLendingPool.sol | 4029 | `51910a3ff5aa68e9c0ac1bf45b334a639e30515eb92ab85db664661109893346` | 0 |
| certora/stata/harness/rewards/RewardsControllerHarness.sol | 1624 | `f376957102276b9f2f233dea6bb45c4ea7266ffb531029543b9de41b23565512` | 0 |
| certora/stata/harness/rewards/TransferStrategyHarness.sol | 729 | `001fe789bf01185a81f88dd802ec63e84348e586598a31b477c6d8c61a215702` | 0 |
| certora/stata/harness/rewards/TransferStrategyMultiRewardHarness.sol | 1014 | `f417d18f2f4b78132efde71087d687687c7319bc526d15c65cf4d26932e80dbc` | 0 |
| certora/stata/harness/tokens/DummyERC20Impl.sol | 1161 | `c82b77086fe66ebfbcc188b4cfd0afe5b2722973f997eeb12168fea64d430e68` | 0 |
| certora/stata/harness/tokens/DummyERC20_aTokenUnderlying.sol | 152 | `5ab15bd047b5c50634e450cd39c7114ab8ffdc6824e8d8619368c157449866e7` | 0 |
| certora/stata/harness/tokens/DummyERC20_rewardToken.sol | 142 | `46cf60eeab10148855e20168f6e5351b86b84c36b9f91bf4c66918d59a3e4349` | 0 |
| echidna-parser.py | 2400 | `9d8d2391a450bae08b573ca9246062cdf90d76455e455bca8acd1d5ba20a0fa1` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/.mocharc.js | 70 | `434e1df653523a6bce5e53a62690018b51039b10fab4a734a10948bedd06789d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/.solcover.js | 448 | `9111d1d9d5d8651916cf6e1afb033eeefd3f1ffa2d353a13f443518364c59420` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol | 1454 | `e0ba6d8a937323046f2bbcc72ba70f7406276aa37b562e1a362004872def3ac8` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessControlHarness.sol | 176 | `a49b1631dee3cd0b22358651751410bda67363f219d4c5dc5d9bcd105c5eb260` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessManagedHarness.sol | 1636 | `e6d084707582b75bf29e170ec02da237fc21541e793a15b2b17482ed9e1a63f9` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/AccessManagerHarness.sol | 4475 | `65fc78a99fd9cfc3daec97c3b5656338e526a7ec639aaa304b185afb32fa50cf` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/DoubleEndedQueueHarness.sol | 1399 | `7473e0ca273983325153604dde0906745542b4ce90bf94984a0c86ea1f54f3b8` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20FlashMintHarness.sol | 1028 | `d14171faf0d2ccb9bf14fd9ad252c07e386689e69a39f0a65a7f5dae6540bcfe` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20PermitHarness.sol | 493 | `7f5eee48c453af458cec04df5678ee8618dd198d3ef399bd1e9efc543491cb97` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC20WrapperHarness.sol | 1121 | `05f6d555cceadef86ae7dde4757897a685ed5c156e6034c7e1a760a8e54d133e` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC3156FlashBorrowerHarness.sol | 405 | `68d31d5af5df023d29304b43e3720164b00d09c75240e9bad83995a8e138c9a6` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC721Harness.sol | 891 | `69a5144e1ae8249774d795e69f815457f85d32b9aff3f3bcc8c15545233ff8bd` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/ERC721ReceiverHarness.sol | 325 | `ba334a1b77d8b0c5bf566957f03fab538938318f059fc1277ecd36e065e76ba1` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/EnumerableMapHarness.sol | 1488 | `9898955deb052f5c661ba6168e789f4f080f6a2a3411c7ad7412e76dd7b0a16b` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/EnumerableSetHarness.sol | 890 | `dc5621c2e221d8bf0e5eb74c841e44ab3f7b7568388f758db919c36e64658733` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/InitializableHarness.sol | 976 | `92af00cfefdefb5137d3fc9c0b615fd719a2ecab85832d28346b4d359ab54158` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/NoncesHarness.sol | 378 | `112c07190fdc3275661c418dcc9597de383422aa31fe76f861248bef979e9c94` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/Ownable2StepHarness.sol | 294 | `dd7ea7342e518bfdcbe4bf10980c1949e9ba67428f436b4d082b359560827eee` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/OwnableHarness.sol | 265 | `b285dad9f93bed4facd29fab94daea314baf78eab611daa3133323a2877a02ab` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/PausableHarness.sol | 387 | `d9c391078e05dceaa14d9731fb1542f5675b35670c556b705adb7c80b18e9374` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/harnesses/TimelockControllerHarness.sol | 405 | `02d61705a0cce4d30449a7250da8e51e9eca48ce5598d962d9eadf6864096079` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/certora/run.js | 4107 | `d2d11e62fd6e5cefbc43ebcf535ca140616e7fab85ce4c69d915dacd0495e691` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/AccessControlUpgradeable.sol | 8227 | `af65f33d5d4ee58be1871f806a6e5f76945ab93acc8579905348c0af9dbd6fdd` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/Ownable2StepUpgradeable.sol | 3433 | `e65937e8c36af5c343406e97399759bd576090c0599b864bbea3501d617f7e1f` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/OwnableUpgradeable.sol | 3969 | `9247b9ad7939d23990dbdc9274917c3762ffb37e5137ef7bbfcc2e2fba1b8dd2` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/extensions/AccessControlDefaultAdminRulesUpgradeable.sol | 17195 | `a0b367f3d905cd9bd7e2400f0ae9e59f614dee51ee089be7fec6363968851cf1` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/extensions/AccessControlEnumerableUpgradeable.sol | 4738 | `071bc543877c67cb0e50d0a067af352df2e9edc09e9d3660f18f838a34e95b35` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/manager/AccessManagedUpgradeable.sol | 5973 | `af836143d788c8f77dedd1e0787d106ece21c01f56dd57098c6c0f0ed16fd17f` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/access/manager/AccessManagerUpgradeable.sol | 32629 | `cc4a118823d84eeb7736b60208a5658a1addfceada363d3c75afaf7049c46e95` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/finance/VestingWalletCliffUpgradeable.sol | 3047 | `e1f8c203fd3ad167536df8dfa4fba69c67f02e19121992bf7dc3692f32b28104` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/finance/VestingWalletUpgradeable.sol | 7298 | `62620100fc0b9e2abfda587822f3c00165cdeeb34c446705fcc99806949d4677` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/GovernorUpgradeable.sol | 33538 | `dafe1155a93969bb87e417d1cebcf349b45089af4cd6ca567e08544e01b577c0` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/TimelockControllerUpgradeable.sol | 18135 | `242e38ddccb6c86ba0f3e66507ba8ab0ec27211b6918ec86c06cec9ea5421ecb` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorCountingFractionalUpgradeable.sol | 10837 | `d6d07a8fb58e11e521033c3299c02bccc0e350a5e3a0010dac3cddf07fb3325a` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorCountingSimpleUpgradeable.sol | 4609 | `d1eda2ca5173abc942a0fe275bbb5ab3a50704f2b426ccd421840e43be3554a9` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorPreventLateQuorumUpgradeable.sol | 5697 | `c6d4053375eba3754ccb3eeee8f7164bfa8f074895bf396dd74e6abdc68dce1c` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorSettingsUpgradeable.sol | 5063 | `ebbf33d35dde1a83b894ed2f0ba878fdf4550bd00245c92cc9fa282113dd1e3b` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorStorageUpgradeable.sol | 5554 | `687b706ebd469ca771e6fdcfd85330b6f716d86780713c36bfc7a1a659893271` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockAccessUpgradeable.sol | 18106 | `c7c35f9ba9baafac9e489d2715e6b06640001b01e28f2fe35d0cafbd0f8ce549` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockCompoundUpgradeable.sol | 8204 | `ad781eaf219aa5b24dcc61785d0b11118299e14ce1bf20c368de292e64955553` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorTimelockControlUpgradeable.sol | 8476 | `b37e18eb1feefc7bcdb98f31b8da7bc5dce5b2e33fff0801c4e85653f9ea0e09` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesQuorumFractionUpgradeable.sol | 5336 | `41af72239fdd8f7ef590f65f305743226fa3e0bdcf14476e627dd58415f37709` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/extensions/GovernorVotesUpgradeable.sol | 3075 | `bdc8a0b9615effb1359a4fbcbc018b943682e382ba8880951ce95eb95bf0df44` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/governance/utils/VotesUpgradeable.sol | 11059 | `ec19a0f6732feb2e1276e60346f14ad0dda335f390d908266d09b7ae937a3ad9` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/metatx/ERC2771ContextUpgradeable.sol | 3618 | `f739bce56b6005c7299a65ee24a8c5402da0e781e76134e9f92b9edc76f23ab2` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/metatx/ERC2771ForwarderUpgradeable.sol | 17345 | `3efd96bd4e3b77aa8d72c28de2fc665b338e3810c44d59b19b61a991e63b07ff` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/package.json | 878 | `c6ffb3c1a939a98f71ac8e9eebd31622e5401225c891be35344a55bb07572e55` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/proxy/utils/Initializable.sol | 8854 | `a8b7eafa0fdc7cb5a644c8c61a8e4c51e031d5e1e6f268f72dbe18b768ead56e` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/proxy/utils/UUPSUpgradeable.sol | 6598 | `3c76952e97e1cacfec407359b9fc7ae41a739fab804458ba7c0806206949570f` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC1155/ERC1155Upgradeable.sol | 15886 | `6ef323d20ffc6623ea89e3a3efc971ea3e35d2692a7cb6f3afab10bab8a296b0` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC1155/extensions/ERC1155BurnableUpgradeable.sol | 1281 | `97afd1059918bdf9b365fb10550ea221ef142d45294da21e3dfff1bae5c50fe9` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC1155/extensions/ERC1155PausableUpgradeable.sol | 1707 | `82c23a2f1578461e109829b91fccfd8bde5a204759cd0bffa3976cb583877842` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC1155/extensions/ERC1155SupplyUpgradeable.sol | 4159 | `10e1d2442f6bf36f8e0525078f9cd53e0a65a9211b00b557dbdcd55e83e2c2d7` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC1155/extensions/ERC1155URIStorageUpgradeable.sol | 3292 | `7d202632221962f77ed8c1b8a9db24f5570ede69839e6da2648594d31ef98893` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC1155/utils/ERC1155HolderUpgradeable.sol | 1750 | `7ab0380bad8a304c085fe2d2a7646f10eaedc204d9e4f51c1fd3e1f5d80da117` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/ERC20Upgradeable.sol | 12169 | `aaabbd0bac5de418bfd3c3c6429b2e9dbed8fd61fdb1ac1c4ef4434f803eda88` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC1363Upgradeable.sol | 5898 | `9fc9d03c226a7a798940de07f91e848028cc85b65ceb4ecf0a5e4ab8029b5eb8` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20BurnableUpgradeable.sol | 1495 | `15b8cfe5d0c0f93fd9cccdb25eb9b2e6ff6bf555bdf7110db305e53880435790` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20CappedUpgradeable.sol | 2334 | `e87efc3174cbae107ab5656481651d0a26bf36667d9a37d882c65cfb47a10a0e` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20FlashMintUpgradeable.sol | 6084 | `ef30fc8af78eb529259a0a3216fc1062a086771d885a2fae618cab7158f28e5f` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20PausableUpgradeable.sol | 1611 | `fcbcb1f80a2b2585dcc2fa0fe2edf5b300e53a5db77352c448250fc51b5e8601` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20PermitUpgradeable.sol | 3200 | `c538cb63958c81d3d796fae44104d42f2d0fa877a15ae8f5477593869c6e2a30` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20VotesUpgradeable.sol | 3928 | `84cdb63ccc1699bd1816e5b143c10f35396cc1a6d11920f2830da622e924dac0` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC20WrapperUpgradeable.sol | 4846 | `8b26e411d21bbd8d2e3572a2f3370ddced6e0fc4c0caf5ddc73a70d2e18a097b` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/ERC4626Upgradeable.sol | 13605 | `8c65f46c961932ab4113c4758fbc96aaf350e812b040a201603131be59ada737` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC20/extensions/draft-ERC20TemporaryApprovalUpgradeable.sol | 5557 | `dc027d63a6a3266944fef04599f274e3fbddd75e62702977f0315cc61c74dee5` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/ERC721Upgradeable.sol | 18098 | `7baa9bd7d920ed5264920052ecbaaede764ad684c5e85b859aeebb1a1ee5cc10` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721BurnableUpgradeable.sol | 1195 | `b3c5805a42ec983a1daebdaacf2e3dbdc1dc68f3d14aa9eb307c22c729d72643` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721ConsecutiveUpgradeable.sol | 8566 | `e1be139be8b241797237a2565bf8188431e90c0bcac562995427a77762a044d4` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721EnumerableUpgradeable.sol | 8798 | `0d19f100db77d29b4628360ed4186c7911e03d8d45b6130b42232d760ad62312` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721PausableUpgradeable.sol | 1680 | `cbaf8b41622a946f665c17b3de0aee2ec93f55d1e89ef9b75735d660f2f90922` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721RoyaltyUpgradeable.sol | 1573 | `4217cd3f43788f1cb538c16e0dd1d765a013d2497309443afafab3d9e24cd075` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721URIStorageUpgradeable.sol | 3108 | `7d950da19da0df704d4ed54a0e5ac944111d5d98b8037fb653bd4539d438472c` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721VotesUpgradeable.sol | 2140 | `6c22a84c27c0c12c9fea54db5e5fa95f542f64beafc03dd10bb427dbf1572b07` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/extensions/ERC721WrapperUpgradeable.sol | 5341 | `265e00d60b434aabd5d40d9cb87dd8a6faae545a0e2f9a1954b69d680b08db22` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/ERC721/utils/ERC721HolderUpgradeable.sol | 1074 | `5f819dbf73677aecc2a8e7e5309a403e1b6c36296270f878fd54b2859420c83b` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/token/common/ERC2981Upgradeable.sol | 6476 | `11ea92eaadaef54892c47211e955925061780d86982671906fee690a7ca6270d` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/utils/ContextUpgradeable.sol | 1194 | `a08e16324da33a9d666dc07a22ae58031c242a3869f6808e55b4b82fc70cb209` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/utils/MulticallUpgradeable.sol | 1989 | `45922f4ff1e446b61cb4677ef95833e1cb2b0276dfb8b3e47cae68f59af70832` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/utils/NoncesUpgradeable.sol | 2269 | `d63abfbf20ca119bf162ec5bb343df4b189208d1d0a73657555f688536498cd8` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/utils/PausableUpgradeable.sol | 3799 | `de9a20a313d34dd3b454c834606518390c8ead4dcca8137c879401fef62d8583` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/utils/ReentrancyGuardTransientUpgradeable.sol | 2354 | `9b7f12fb4521bcc04f278173bff4ce95673936c9066516244ae532b68144a83c` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/utils/ReentrancyGuardUpgradeable.sol | 4450 | `11b45418823fd6e961d8db5cf5c2795b08f51f88a66f8e37a38fcd052ee711a4` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/utils/cryptography/EIP712Upgradeable.sol | 8636 | `e4921efd4791f39deaa0cd71fee74de4f2c8320a99f388b4189df504157981c8` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/contracts/utils/introspection/ERC165Upgradeable.sol | 1184 | `586f77f25f65f2b957d5579c346d39cc883848962a375857c151c5bb15c0eb93` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/docs/config.js | 748 | `d5cdaf3c2d7b2724173f9664210cfae1aa4a700bf2a1f6a7b7820b74b04c15e7` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/docs/templates/helpers.js | 1423 | `c54072a039eb8e30ebdfc050e2366c4fd2d33aaef32693e000b355c28899fa13` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/docs/templates/properties.js | 2362 | `6963a4de368ade29eded9c3f8df165186be417f585a2a60c09a400921c7fd9c2` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/hardhat/async-test-sanity.js | 76 | `5103b71ce9ab1f95f16435805507b3c3a1ae06aff4dbd2f9e78f3c544ac161a8` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/hardhat/env-artifacts.js | 1019 | `53209232db89939f0f8e047febfe15adfd52580c65594443e395423c7421f671` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/hardhat/ignore-unreachable-warnings.js | 2018 | `5881535d1f4d05527a4481c6f0cd85156309e1623692b0d6a54139da67af96a3` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/hardhat/remappings.js | 508 | `8c937c074523720f867389503a24c6f1b24b729712995842fbb8fccf1c3fdb36` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/hardhat/skip-foundry-tests.js | 295 | `5e594373be07d38818abb95c62e159435c68e291aa230e7d95fc2e38f00cb8ea` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/hardhat/task-test-get-files.js | 1008 | `9851350b493983460df169f1c5dedac9c36930ee5bdbddaf977fb5fa75925a86` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/hardhat.config.js | 3094 | `114298824a9554ccb0e061e2023a4be605726717771508d6f8954d52ba850db9` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SVM.sol | 1594 | `35d3191997b0f778ba623c3f126aa2afacc486d7cbde83aa91cbe4aa089a9044` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/halmos-cheatcodes/src/SymTest.sol | 357 | `c5391a942e6ca4a31e1b48668ba80d12e5bc552453470fa153541ea322f8a88d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/.mocharc.js | 70 | `434e1df653523a6bce5e53a62690018b51039b10fab4a734a10948bedd06789d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/.solcover.js | 448 | `9111d1d9d5d8651916cf6e1afb033eeefd3f1ffa2d353a13f443518364c59420` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/AccessControlDefaultAdminRulesHarness.sol | 1454 | `e0ba6d8a937323046f2bbcc72ba70f7406276aa37b562e1a362004872def3ac8` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/AccessControlHarness.sol | 176 | `a49b1631dee3cd0b22358651751410bda67363f219d4c5dc5d9bcd105c5eb260` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/AccessManagedHarness.sol | 1636 | `e6d084707582b75bf29e170ec02da237fc21541e793a15b2b17482ed9e1a63f9` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/AccessManagerHarness.sol | 4475 | `65fc78a99fd9cfc3daec97c3b5656338e526a7ec639aaa304b185afb32fa50cf` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/DoubleEndedQueueHarness.sol | 1399 | `7473e0ca273983325153604dde0906745542b4ce90bf94984a0c86ea1f54f3b8` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/ERC20FlashMintHarness.sol | 1028 | `d14171faf0d2ccb9bf14fd9ad252c07e386689e69a39f0a65a7f5dae6540bcfe` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/ERC20PermitHarness.sol | 493 | `7f5eee48c453af458cec04df5678ee8618dd198d3ef399bd1e9efc543491cb97` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/ERC20WrapperHarness.sol | 1121 | `05f6d555cceadef86ae7dde4757897a685ed5c156e6034c7e1a760a8e54d133e` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/ERC3156FlashBorrowerHarness.sol | 405 | `68d31d5af5df023d29304b43e3720164b00d09c75240e9bad83995a8e138c9a6` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/ERC721Harness.sol | 891 | `69a5144e1ae8249774d795e69f815457f85d32b9aff3f3bcc8c15545233ff8bd` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/ERC721ReceiverHarness.sol | 325 | `ba334a1b77d8b0c5bf566957f03fab538938318f059fc1277ecd36e065e76ba1` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/EnumerableMapHarness.sol | 1488 | `9898955deb052f5c661ba6168e789f4f080f6a2a3411c7ad7412e76dd7b0a16b` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/EnumerableSetHarness.sol | 890 | `dc5621c2e221d8bf0e5eb74c841e44ab3f7b7568388f758db919c36e64658733` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/InitializableHarness.sol | 976 | `92af00cfefdefb5137d3fc9c0b615fd719a2ecab85832d28346b4d359ab54158` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/NoncesHarness.sol | 378 | `112c07190fdc3275661c418dcc9597de383422aa31fe76f861248bef979e9c94` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/Ownable2StepHarness.sol | 294 | `dd7ea7342e518bfdcbe4bf10980c1949e9ba67428f436b4d082b359560827eee` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/OwnableHarness.sol | 265 | `b285dad9f93bed4facd29fab94daea314baf78eab611daa3133323a2877a02ab` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/PausableHarness.sol | 387 | `d9c391078e05dceaa14d9731fb1542f5675b35670c556b705adb7c80b18e9374` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/harnesses/TimelockControllerHarness.sol | 405 | `02d61705a0cce4d30449a7250da8e51e9eca48ce5598d962d9eadf6864096079` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/certora/run.js | 4107 | `d2d11e62fd6e5cefbc43ebcf535ca140616e7fab85ce4c69d915dacd0495e691` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/AccessControl.sol | 7050 | `1086a1ad3788972b885ff3f209da510615dde6214d46b29e1cd2a4924f66c06d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/IAccessControl.sol | 3343 | `c112f5c86fdc4e862f88d4f5694530342320923ebd5b5e7d9d8493550d337c2d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable.sol | 3102 | `38578bd71c0a909840e67202db527cc6b4e6b437e0f39f0c909da32c1e30cb81` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/Ownable2Step.sol | 2476 | `c75345d7b9feef17ae29f2a800ca2f65f8021cf80436a41d6ec00f57f5180f36` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/extensions/AccessControlDefaultAdminRules.sol | 14810 | `fefdd334836d2fd96871284d4cc3877d95f081bbc54fc179a8572a5f2d50f7ad` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/extensions/AccessControlEnumerable.sol | 3373 | `d6c882c624699389abe9a4d8b6ad1f3d304ad6610221ac1cbd32f909e402629f` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/extensions/IAccessControlDefaultAdminRules.sol | 8171 | `c7bbf8bc9e68a131951d23f099b50e8d2737d07a0307dfcb26be0595f3efcfa6` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/extensions/IAccessControlEnumerable.sol | 1279 | `f91dc4b5750c1bac7a6a11a6057f14f01121847e6a6284e1200d8a87a4c4ff1e` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/AccessManaged.sol | 4725 | `6834e350bc8bedbb042a62f6681f7976186e92e7febac2575bae081d81244ea9` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/AccessManager.sol | 29876 | `72f06a0f03f2044d9b3bf036933aca7d589f0b8875a596206d50b696e59e8781` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/AuthorityUtils.sol | 1230 | `6a78662d327e8c82eee93a4659ddfb62a1f477f8cd9a2319848b3566e40baac8` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAccessManaged.sol | 1111 | `b6cbb31989224829b1bcbcb7c34088eb16362650174da2cc98b2d7e01a1609bd` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAccessManager.sol | 16366 | `11da09673a4026c23d15f88562cc8cfff23646fb8264dad62db7f6ff1e992297` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/access/manager/IAuthority.sol | 482 | `9fc27c63a17ed287dd1070ccca4bc9d3250af3d9e0c2c4ebf95173395ed98726` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/finance/VestingWallet.sol | 5641 | `8fd347d2b11c9e6203f29cde5d03bc51b17e94c3c74b93f0a4e5a36a1c1fe3f0` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/finance/VestingWalletCliff.sol | 2018 | `14981dea962b6c81e253295b702f2a461d7db60ae93715b293e95028d51b81f9` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/Governor.sol | 31608 | `0e94dff852ecc526a7fa21b8af8e91d799a1e50e5edbd1f3b933782936f704f6` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/IGovernor.sol | 15998 | `2f73642a69d9ff9033ffbb835dfac260c523e32d65e0eec3259857e5934882bc` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/TimelockController.sol | 16290 | `89a4cf0e404a42f13d01efefb5c1b3b1d46641c670b626b1b885330f3faccd2a` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorCountingFractional.sol | 9388 | `06fd91844a6e6c6ed4425cb5238e7c6dc2a99499d6b266286ed9ebdc8e34c4ec` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorCountingSimple.sol | 3321 | `fee9f14eae7b45504e19f2e5dd55e74d7ce05f9733157a5811bd883b80256639` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorPreventLateQuorum.sol | 4354 | `af733274a4e245341fdce2b827470a162e0f967b6b1f1b3573526b859d5467fc` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorSettings.sol | 3631 | `f6268357cb5aeb8c2509699f78127b9b360e9bb57c2b4cb1406ca24a4573d66e` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorStorage.sol | 4251 | `55ba9882c6d66026a6024cfe1db873754b0974a3859f709b765e35089e13d64c` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockAccess.sol | 15993 | `676584f6c287cd0efbf388bdf0881a1654f63562b9a7ea6be03cc1a93c938266` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockCompound.sol | 6397 | `ee11bd77cdfeaa113b804edb9ebc3c43e8fdc4a3f8c8dbd618af45e9f8a3b35a` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorTimelockControl.sol | 6711 | `4fe02228a581a7b5f0f322834b79a898c5d65e1222573ca8afc0334feb6ae48b` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotes.sol | 2048 | `bd306880ef79bac2fbd7ba3ed6ecc43bef4f78cbb5e26d12bdc0cc18a795163d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/extensions/GovernorVotesQuorumFraction.sol | 4033 | `9febb68a832e0bc5e15fee84a1112436c8839f7f2294b3ec103cb1700af71c3c` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/utils/IVotes.sol | 2322 | `f033b73ce92762d9ed9496b8a0f5f72bd0479e42388da584c2ff276cbb5cb9b1` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/governance/utils/Votes.sol | 9667 | `dea1532e5e0d920d9c40a6719a84e71b5de91391c1e2f65bb50d03878e7270bb` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155.sol | 189 | `6b08e7a48198dbe997205dad74a6dae1e5024dd4ef38ea7a70285950ba95bf24` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155MetadataURI.sol | 233 | `15df60a6b44a11ad12c8c6744ebb962834728fa4f20387430312c814394adf2a` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1155Receiver.sol | 213 | `ae9854dbfd4d879b6ed765d4de55ac7f9e67598ece010262bf46f3a86152115a` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1271.sol | 653 | `599887e85d375f463f30e3c4cf139ea541e73c7b3535eb040da5e8d8145a4f14` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1363.sol | 4454 | `54f427f63724d9760211dfa9e0cc5d79d86c0724becd81f8e638e2e27b0e2669` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1363Receiver.sol | 1316 | `21584d4866c59fed42491cfb43a009ab451d1c387c951c7b7cadc3fdab68baa2` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1363Spender.sol | 1119 | `6e27f3eafd6190ceea989405d9e6cd15aa00c6530d316f82fffa746412ef1d94` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC165.sol | 192 | `49abfb8fa26e3f1715fe05948a96e3762b805bd4a77d103eb40ba96b1acfa144` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1820Implementer.sol | 767 | `9b7704eb411b2ebde03bb2a0a866cab485a21c41891ad79c1acebe04afda4e68` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1820Registry.sol | 4836 | `70337a0847da40172c8461693d6048c7a159ee0db9e5df6d8bb6024ab38fbef3` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC1967.sol | 636 | `886b093d8f7c41f73af42b8e183314b3654531a9d5e11f07c41a5a7f11d3e006` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC20.sol | 181 | `cb42f0b4d269ba8ef2629c176a7f99bf4fb50837c92f45596b54822b26e3df4b` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC20Metadata.sol | 216 | `5fb70a9fa6d8e6193c557ea59dd18415bfe7facdf93fcf8ca1a415a9b7ff6706` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC2309.sol | 532 | `fb0568452aff870d2ec0e91c990f7b29d09001fc77c7413897f5fc5ccf492736` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC2612.sol | 245 | `8e9a3e95b74ab333b0d3319b4346293d3c84363bdfc6d95d08894f2bb95b94be` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC2981.sol | 1114 | `6a8ea184edb362922fb260ba9c43dc867e3b32cd3547d3de9299344cdf91c635` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC3156.sol | 263 | `27ed5fdc9ead61628277367c5fff80ace73defd91a69f9f9d9559a300f3ea8e6` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC3156FlashBorrower.sol | 900 | `91bbede9a1163c3522f50f558b0f3d1d9c95c0e404d9a42d30286c1f481b2c11` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC3156FlashLender.sol | 1453 | `dd1b735c90f497c80743934aa7ec874aa50c359e001dd19c83caff4a227ca804` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC4626.sol | 12184 | `76ac9a58abb54725e50d19c66583135efc523410f6d6fbcdfc0528c4cf070cbb` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC4906.sol | 841 | `2b81c911f4c289d34f8d11064ce495bb8f49ba9a408df6ee1cbe4020eaf0ec10` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC5267.sol | 739 | `efd1ebd1e04b6ef9c3b8781a097588f83da954323f438d54a71dc06508e6c7b8` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC5313.sol | 434 | `8bc20fb9e53bdb556386519448975a15afa3794230a90b6e3050fe00cbb48d50` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC5805.sol | 272 | `6ecc2370599496e6d862c2b4893975ec240f0ef8475daef1d20b5dd1efa90102` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC6372.sol | 519 | `2294c70df203a6a38985d064adca030293bec4b7aaa1237b62c7b1a34154f130` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC721.sol | 185 | `f33ff9bb851371eab816597d29e77dea7947c392de6bce6bea29df3439546b16` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC721Enumerable.sol | 226 | `3f2f9f48dbc9651ff725a00b0349b1a8280bdd309b97654d10e359739d1ff2dc` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC721Metadata.sol | 220 | `9b62abc2c247f42681d4f3261628e510dfe6cea0f433d2174b332739c6e349ca` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC721Receiver.sol | 209 | `d3ff9df7e9539f4eb7db7fc788d2e722ea7ba737de738d1c66e929fa6d158e8d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC777.sol | 6733 | `4d3d041b2a0d14e3f2da437ab17db313d14f36a631af84f8a88565d5bc7b43cf` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC777Recipient.sol | 1269 | `2c2e97190c7201dbec1d043c0515abd8c1f8d9ca3b6e3352c1d659e2c3e12251` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/IERC777Sender.sol | 1278 | `361a409d3a0058d75419d4c6c7340c8e4acc03ac9b98d09f4c0a01b8320397a7` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC1822.sol | 881 | `71190a8ee26dab908d3dad703ccfff09ebfc5850f2f405463e21df21a8643bbc` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC6093.sol | 6538 | `56380323009ef4a119d44550b910fde1bff9cedde8f7f4c690152c7629bc3338` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/interfaces/draft-IERC7674.sol | 567 | `c9aec3a4d47b7f8a8b4642b6616a685cf414346123daec9aab52eb51216ad2ca` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/metatx/ERC2771Context.sol | 3495 | `66e42d6798dedb18c2cdc92ca164aefb67ee3d37c90ec5aae0c311719c19d634` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/metatx/ERC2771Forwarder.sol | 16805 | `1e6659e3efa4ead550f6d3023ed30d56d499ddcb63916893ce7d5dbf58843498` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/package.json | 786 | `765a3a984fc182b033cc1daa3051c8b5c2d3b75d209765fe5a711b2023f06967` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/Clones.sol | 5510 | `178cb2b6d4e3ce038ce75114c862420f92bdd43360ef902f530139b4a80212cf` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Proxy.sol | 1718 | `03cdbd59c384fe18e74a2a0697ba167e7f545d6a1bbb3d52df502ab4fb108e0a` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/ERC1967/ERC1967Utils.sol | 6238 | `2ba1cb9e2c1a0518ac940fa1f10e62fa56f1ba2b13973f36a8b505de627e4119` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/Proxy.sol | 2670 | `5f5081378d4bc82b814b0d64990b7f7b9c69697593b73a3341f4a269940ba540` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/BeaconProxy.sol | 2311 | `f006ac05ec8509758348f9966c5aba64d695e99fb2d805eae9658114cefefb93` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/IBeacon.sol | 472 | `422eabc0e645e24c3a52898f6255b349323b013544a3ebdc4b2d3f7fc5bb7e9e` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/beacon/UpgradeableBeacon.sol | 2219 | `26dda9d5bb961b3df26602d49f9f5a0647cfdb78b63cc253aed8527030a64f25` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/ProxyAdmin.sol | 1965 | `5fac2946d312b6c192751da6b22de349e6ee0acf9d95afeb24d3780c2efc7f93` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/transparent/TransparentUpgradeableProxy.sol | 6546 | `1a81841003cfbf26875cbcd82f045f727661853bfc6042e17b909f39ea5d1658` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/utils/Initializable.sol | 8854 | `a8b7eafa0fdc7cb5a644c8c61a8e4c51e031d5e1e6f268f72dbe18b768ead56e` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/proxy/utils/UUPSUpgradeable.sol | 6332 | `09c7406cf8c50d31b77089a6860ad026cd65d48ed5b696e6cad905c4aff008d6` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol | 14532 | `560b187bb02cf3976455905e4f5bf6311e340e55e1e346a41ebf865e1c26b74c` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/IERC1155.sol | 4716 | `587171cdcc6eb94734c7893c0dea36bc0f2784f1c0186f2000e6be9a62fbad4c` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/IERC1155Receiver.sol | 2599 | `b3da220debe08c174f8848fa4c41cccf3d49e4e23c81d76528df99fb759f4937` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155Burnable.sol | 997 | `a8122e8e46870932b21294d5df9f013f6b1381fdad08ea7e7f48efe49cd3cb20` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155Pausable.sol | 1353 | `6bfd11fef86b179cc4369ebfc54926757d10820dd5552044215dc0213afe4c58` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155Supply.sol | 3164 | `d34254efe73662358ed7f40a9bb4906b6216708bbe334aea360b41565ff0254e` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/ERC1155URIStorage.sol | 2090 | `52bcb7aa728be29ef2dd0b328f1300a3748221b5c234ba71f80f979816d58196` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/extensions/IERC1155MetadataURI.sol | 677 | `77eee1fa8944ebb742db88b0edb0376b8ceb035b570950bdae8db7ded1869fca` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/utils/ERC1155Holder.sol | 1352 | `8e2baa224856aa31b2b8706b2a9eb9c43694a04cfd02cb7886aba2f88014b1dd` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC1155/utils/ERC1155Utils.sol | 3534 | `91338a168b1bbe35e59d5c21b259024e965a5e5a554a299900fa7a865bdd317a` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/ERC20.sol | 10895 | `be0df7e4b899a61a4beb3c8675088de494866438600ce2d529523807b558cf64` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/IERC20.sol | 2780 | `30edf7394bab78d48b7db3a059248e1ea7c2c77d2ec0e37a13bb91415aafbe5a` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC1363.sol | 5466 | `50a2b134a1e901b4dc2fc0a763ac53cea88cc8300afd8210782331c0f97b459f` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Burnable.sol | 1182 | `2e6108a11184dd0caab3f3ef31bd15fed1bc7e4c781a55bc867ccedd8474565c` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Capped.sol | 1433 | `cb15f210495f2119cfec53e32738ddb23469d414c45a2d7444c2181a9940bbed` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20FlashMint.sol | 5772 | `50a9e14561603af062887bb3820c32cca62e9339042d480a8bed92b637d93ecd` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Pausable.sol | 1261 | `12919f23b3b408e67b3b9c9543e37b7474e314d8f1c596472fd9201d9990a278` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Permit.sol | 2774 | `75f9f66db047b1413aa45538a53211e7b20479d74c3dd2657335bf4dc50b8811` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Votes.sol | 3606 | `f2a0c9b7b4b67cec3ae19dad94454da68da553512f22e4eaf39c46447e11815a` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC20Wrapper.sol | 3456 | `3cb248417b6d39e9b2894826069de17a15ca21555100f563928e5988bca4b52d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/ERC4626.sol | 12314 | `556f6226a37eca849ecf4801ed5571e24da593bf9a9ee6092f1510c1601b2468` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/IERC20Metadata.sol | 684 | `9e7c70ec72d2f7d592e23ea84f3852b04f91f6f644ce57e0263493046b36afb9` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/IERC20Permit.sol | 3805 | `026aca1c8ee4574eb9719dca7dfc33e3e57a618715ae702a675e8a8c9ea1e82d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/extensions/draft-ERC20TemporaryApproval.sol | 5125 | `362c2ebc6204fc35a0fc941145a41d0d347941d97bee4681162eb1799bdd6050` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/utils/ERC1363Utils.sol | 3293 | `a32004659b79673c1f41ffd717a6b752a9fe539d776bb485344e2c4a0de76fec` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC20/utils/SafeERC20.sol | 9443 | `d67b0f3d9302b2ff7cec76776fc2c1f3686082287441c15c6871c0086a8a4f74` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/ERC721.sol | 16456 | `1c470376ac5b8d29fd44139aa0fadf4904ea161ed460050ffd7866e0eea1e982` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/IERC721.sol | 4929 | `83dcde4af9ba4ded8b6e68e0cb8f4a9430dd23c423f6840d9f93fc6bb475f9ae` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/IERC721Receiver.sol | 997 | `2eae310f371d9107d81d4b1285f897e56074465f7caeeff90b5e3e1770dda7d6` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Burnable.sol | 880 | `7b212ebdf844128dd2b3f02f824d7e855983495a75eea9c23852301c3887e861` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Consecutive.sol | 7404 | `d500e45a69dfc5780d90b6f07e99ea62ac8f07cc69e9fb689478acc02285c93f` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Enumerable.sol | 7382 | `26ef6fbb12f45741f07cd0f00a147c34d02a19f37e5a9a329e8c82986b9ac9b7` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Pausable.sol | 1328 | `d773f8c1ad695bad18631cec9f3ddfa337982a75562bb061f09f7ef4f216af7d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Royalty.sol | 1238 | `5728aad19f726cd62001e01fb1c8857a166b24367a79e93214194bfa0db84d95` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721URIStorage.sol | 2093 | `ce36b2e59527b8a4890c68ca7f1e6c1b05661c2916660f63b00502c1394861a3` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Votes.sol | 1831 | `37fdb0786bdfedc9e89357a9e9388ee92445ef6e14573e97348d03248ff70a80` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/ERC721Wrapper.sol | 4291 | `e646308e346689526041583bb2a426c5e95fa5bd9e77081fdc635b449abda505` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/IERC721Enumerable.sol | 1040 | `1660995643782d34787929cf39dd3a0d44117f14c3ab278329cb079d5253f35f` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/extensions/IERC721Metadata.sol | 792 | `63d104c065c281e8d8e1fabe0eda19ff83d4660ce1378f9dad2471226d2bf34f` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/utils/ERC721Holder.sol | 795 | `fa1e231eedfd128232d8f34e9599165fb302c9dee5e58ef009f3b99f7e5d930d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/ERC721/utils/ERC721Utils.sol | 1912 | `368171cf1ce8adbf7b95515ecf3f2f2ca38b194c38bf43dab07b6e6c0fc32f3a` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/token/common/ERC2981.sol | 5372 | `e92ef291a91d7cf4bf178ea19abe680d2d9970f0c2cf24c57f01160639269e44` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Address.sol | 6033 | `8228692ef1ccb4cfe5b7cc58324cadd06045e10e386185f9e4d45173d6d6c633` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Arrays.sol | 18341 | `ba9eba95d720954becedb85977a4063ffebdfe56f2647705ef8a04945fb6fd5e` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Base64.sol | 5211 | `c3738c1be3c48c5f78e311119a74256f2df0336951369b1d8290838459f8b4a1` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Comparators.sol | 443 | `52fb1c8f57967d42a3214bde4a8a414ab25c2e3a844d00e171ca56487024e009` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Context.sol | 963 | `847fda5460fee70f56f4200f59b82ae622bb03c79c77e67af010e31b7e2cc5b6` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Create2.sol | 4466 | `1ddfef650decd5f4e4bb57ac5f42add20bf90bc8ff716de27b8f22619be332ef` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Errors.sol | 896 | `0704b9d6c032cca8512a3bc3f30f49f86f1f03102d2896a3d23e794b82efea66` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Multicall.sol | 1695 | `1f9eaa29689a4810ac91bebef305b700e7d0b387d12de41caa6209ed37435b89` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Nonces.sol | 1490 | `9b4cbb85d1f5053c744e83302538eb643a713ffd14bc37665b224f1c66529339` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Packing.sol | 44738 | `b8a34f90631d07edb45e491cbecb40e46022a9b59fb7fe7ac824cd49f7d82ec4` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Panic.sol | 1973 | `270fc8401c1a13fae6a7a4a2dd6e381b95d658896701e51f0d3e2688acab3dec` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Pausable.sol | 2830 | `6543160582b3c0319a180f31660faf6ba0a8444acbdb03357c09790a96256835` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/ReentrancyGuard.sol | 3384 | `32fbb1c908ec1b4de85cc1bb10091aebd5816ffe80dfdd5ca5e084fbea67a462` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/ReentrancyGuardTransient.sol | 2061 | `7884e70b6ee5c6f2b0dd7ae298ada9d58c8ae2c67f4489187dd5f639a9da2a56` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/ShortStrings.sol | 4226 | `c5970e9c77c9a797941fcb9ab8c9a5d0b1227c610a919ee8a04ba061e6881873` | 1 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/SlotDerivation.sol | 5322 | `08fcc8ff9c33f431aa55eb169597e2894bfc7665cc30756cc0706e32d2c49f19` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/StorageSlot.sol | 4182 | `75704538dcb223239280c6726d9a31cf769a7816718517c997fc7d63bdb70778` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/Strings.sol | 3932 | `27ab8a578913671cdda422a97e96c2239157be7a7c2cfb6d042ddd6963f200f9` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/TransientSlot.sol | 5069 | `172a2fd2dadb94effdaa97843e009619162cb887df38d04c6e5792290d23dac6` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/ECDSA.sol | 7815 | `0964ddd02f4a7a8cf9ba130e3aeead588ca3d425d5bc13cc4221358c69108ed0` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/EIP712.sol | 6611 | `e7f41ef62494c6c26ddaaac0f2790fa365b635e7c5aaacbeafba3067574e38d7` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/Hashes.sol | 1035 | `a83c3f8475456c2e8bf4655314f8e5d6af586f46e9dbd0b827009c57bb42ae96` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/MerkleProof.sol | 24336 | `a174525c74ab5d2f066206ec9cebb6b3c618384c53ec35ad224ac1fbbf06b3f0` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/MessageHashUtils.sol | 3703 | `93e4c09f9c65d37a14d796601b67a67fc918e16957a6328261f8635e136adf76` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/P256.sol | 17032 | `b94e697867944db51efb2f3d0d1ec19877ddfae7066cb5fb7387945e2cdc852c` | 2 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/RSA.sol | 8237 | `036c1fab2a132d7acb7fa0873812f2ad22c873d2efc91032b8ac7a1fda5ff476` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/cryptography/SignatureChecker.sol | 2338 | `37a06b31bce546a771a6450bdccf8f88ab3fef1d91e1aa5a2e10324cbbd9b2f0` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/introspection/ERC165.sol | 912 | `7fdc4dc9e3872f6a4c1ec9cfa9583a1fc18ccd7a416397a6e698bd5bbf92f32b` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/introspection/ERC165Checker.sol | 5054 | `4a258c80eb26f4e93b0d80e470ea690d485cf4c0bb35300a693eea25182d9b15` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/introspection/IERC165.sol | 870 | `7c5c3f98ab876991e7dd34b84d41137e836306eb9f36f6386a631f5be3f5d6d4` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/math/Math.sol | 28308 | `68cf79a637995d5ed243c4a5856b42a5e134ee8786a05034e24d75927fc40ebc` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/math/SafeCast.sol | 34943 | `9769274bf53f26a7c7896c526ea1980dc9bea5bf5c2a5fd04870008c4afc1de9` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/math/SignedMath.sol | 2613 | `1ed50b1056af886752f0fb48a0165d381e69bb4a4b18b893b066dc144a7e08d7` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/BitMaps.sol | 2020 | `12d7dd76e44e30d2d076df04f970a272969f30c2a2d240a89b6e2cac3f3e7c55` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/Checkpoints.sol | 21425 | `51fdad936cefb4c63e987e97e516af965fbfca31e1798f380ae16e5b3a6fb3d1` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/CircularBuffer.sol | 5131 | `471c15bba531238810d7ab94a30e0bad296caedaf194d50810e713d660bf2bc6` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/DoubleEndedQueue.sol | 5689 | `463c51e14acbb0b9afef3f1f6903203cce5798fb168742ccd7e049e0397b2184` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/EnumerableMap.sol | 32557 | `4e7258db20d558c64d06ad592e80718dd127d9553dc29632e7d73de26d6d2005` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/EnumerableSet.sol | 12890 | `ed0804f9dcff9d2dceba8cc83f31669a84491dfcfe510050c9371aa7c48db09c` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/Heap.sol | 10301 | `d9b945b169c77dd7d941a82e191edb709a31c0fb09e70252c32ec692b3d9c223` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/structs/MerkleTree.sol | 7846 | `547569e45b872344f4be6608ae4c69e074ef0da72e57476f4c17e85056944a9d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/utils/types/Time.sol | 5156 | `79534431c3934b23eafab9d02bda493cfc2ae383ba117a7c9698750c2e4845f1` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/contracts/vendor/compound/ICompoundTimelock.sol | 2357 | `94caa77588265fd0dd8d58bd687ab2845e5e3858557cd575a4c8bdbb3892d666` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/docs/config.js | 748 | `d5cdaf3c2d7b2724173f9664210cfae1aa4a700bf2a1f6a7b7820b74b04c15e7` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/docs/templates/helpers.js | 1423 | `c54072a039eb8e30ebdfc050e2366c4fd2d33aaef32693e000b355c28899fa13` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/docs/templates/properties.js | 2362 | `6963a4de368ade29eded9c3f8df165186be417f585a2a60c09a400921c7fd9c2` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat/async-test-sanity.js | 76 | `5103b71ce9ab1f95f16435805507b3c3a1ae06aff4dbd2f9e78f3c544ac161a8` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat/env-artifacts.js | 1019 | `53209232db89939f0f8e047febfe15adfd52580c65594443e395423c7421f671` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat/ignore-unreachable-warnings.js | 2018 | `5881535d1f4d05527a4481c6f0cd85156309e1623692b0d6a54139da67af96a3` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat/remappings.js | 508 | `8c937c074523720f867389503a24c6f1b24b729712995842fbb8fccf1c3fdb36` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat/skip-foundry-tests.js | 295 | `5e594373be07d38818abb95c62e159435c68e291aa230e7d95fc2e38f00cb8ea` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat/task-test-get-files.js | 1008 | `9851350b493983460df169f1c5dedac9c36930ee5bdbddaf977fb5fa75925a86` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/hardhat.config.js | 3094 | `114298824a9554ccb0e061e2023a4be605726717771508d6f8954d52ba850db9` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SVM.sol | 1594 | `35d3191997b0f778ba623c3f126aa2afacc486d7cbde83aa91cbe4aa089a9044` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/lib/halmos-cheatcodes/src/SymTest.sol | 357 | `c5391a942e6ca4a31e1b48668ba80d12e5bc552453470fa153541ea322f8a88d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package-lock.json | 414672 | `0b12305e50ac29f985ad2c1b8808842680ff1ddd244ce78803bf45fa46fb58c2` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/package.json | 3431 | `c57ecc49cdadc103b019cf7617c9415d9678c85f329792bb7518a19786a4a23d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/checks/compare-layout.js | 662 | `9db6f11c491c88e94eb7ca6700f50bfca1b6cd0ac5e1842ee797f89bff001140` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/checks/compareGasReports.js | 7020 | `d6023ec6f9b7ca10b8fd11c515fe945523d611295ce9b56b9282ca45c2c77401` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/checks/extract-layout.js | 1122 | `2c94e7b5cb32f542c6e4a7dd137a0d567114fa604d447d800013bed1b680ccb0` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/checks/inheritance-ordering.js | 1949 | `b3f0fa6fd440d2b953a929d01f50b5ea3c13040143f402a8c396925861bc2ade` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/gen-nav.js | 984 | `4705c4cecad88a47dbb0dc8f1d854d17669b74851d57c16d6130cc6ebcf73af8` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/format-lines.js | 422 | `de8e8ae2542d2db777ff3441efdd1b3f549c5ba473f1071180451c5e25575c12` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/helpers/sanitize.js | 190 | `aa9db8aae572c1076e7d081114673a8fa56e8e228ff2f5e43d9454421e0686bb` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/run.js | 2121 | `6e4641dbcfe2497aee22efd326966f4e0bd68594447bae18e04ee35da5e6b1a7` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Arrays.js | 12302 | `1ba1b9d59a8523fd8a423fb745ec400fbf244c6d982e0c95f32914460c00d45e` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Arrays.opts.js | 78 | `4bd89ea1be08ae608a28dbc75c45a54bbf733c0367a988ed2b84e92d0f4bf826` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Checkpoints.js | 8367 | `7fd21b768ec4dec279ec9f67b26375df5f9180cc294c5ac919c69482ca096121` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Checkpoints.opts.js | 411 | `47ac1d11a3e082049539e930b28e179cb665ce2c04e64bb434a606a591accaba` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Checkpoints.t.js | 4529 | `f7d2f5f48d755be28c6fe3df505a961b2042989fc77316f8bdf221891f7f6e10` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/EnumerableMap.js | 9028 | `9ed4c302f2381ab72fcc586229b573e67dbab29c677fbea54aa9cad0ace4faa7` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/EnumerableMap.opts.js | 528 | `164f1188f6352dc2cf424c4dbc1b92e40d9ffe6a1ffec065d33ffb7a42bff552` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/EnumerableSet.js | 7776 | `424d5ba705cb5fe8094c5bf1c0f136668a3d0e447dfbf1972a57de26be31250c` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/EnumerableSet.opts.js | 301 | `5c7a9371981122981dd2f2ae3eb856b4632151e816279403bcd037a00c8f2a0e` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/MerkleProof.js | 8002 | `7fd6aca712d3cdcb5aa6ca603747c7713bfb11da4ec3dfbb13e4f865de03afa4` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/MerkleProof.opts.js | 307 | `b2dd437a8f00e7a973cceaf3d0faaa81f68c6a5e44cc9a48c6a9335c7b374de9` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Packing.js | 2746 | `8fc4918bb789bf933638263c872ce22fc9f68ce6ae4c36d9d1f398b56a3faa54` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Packing.opts.js | 72 | `795f4fc5182404c9c21b9d71c8156899c8f6956e5dbf3f74d6cfb6c59934368c` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Packing.t.js | 1601 | `df80c5e4323bb6b5d58d5f7a0df3de1c4c1fe22ddcab16f141e35db5c5d371f4` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/SafeCast.js | 3827 | `19b182fa8b42bdd1444b448780470d5229126f4dd39478ab87ee822c84490562` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/Slot.opts.js | 632 | `f566f7646afaa4a9731d38f05870539a2d2bfea84721c320aa1f4dd8a2879bfc` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/SlotDerivation.js | 3582 | `f61661b71363c9cf872f4a9162740c9d31c5fe3460ce139c9414d4db6afa96e3` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/SlotDerivation.t.js | 3235 | `4fb95dbeefc4fb0e08e1361df4a4614e9f60ae301a414e770606bebf878ea0d5` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/StorageSlot.js | 2321 | `daf387a4f34b198c78fe70fbeee28d5921630c6243c84fef988d04e4cbd6575f` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/StorageSlotMock.js | 1622 | `17cfce493dcaaa2e85ca1b01eea5bdc0ff8e501a4281c58073dc4852d0ebe899` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/TransientSlot.js | 2133 | `11c898c4383f44d34341d9230593b9cb0b94c27b43a2d4a4d3e9b6bb67998e85` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/TransientSlotMock.js | 804 | `5b8320fc0615731a32816a51e6ed535c72eaf8911217a69c66e85c4e49ff33e6` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/generate/templates/conversion.js | 678 | `134a41ead4e00cff47ef7d0f99b68dea2e730f5a8cc02dbca22f7603fb5b10f8` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/helpers.js | 155 | `58660f4bfe243e8720a6001ae4380d4329b2891b973bccc19a53d831c9535808` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/format-changelog.js | 1227 | `e98c4c231803fb239db92fef68e6191349379c73751e015909c2b384a0754d08` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/synchronize-versions.js | 481 | `477c2b3c846a9faf36afa1a66d3ed8a7008a80aaec5a096ee7ed4d6a3ac1d54a` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/update-comment.js | 1280 | `258bad59128bf2f39480fc719a0d8b4b5874d84a877ca00953854f66ce3ef48d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/workflow/github-release.js | 1660 | `4b88436e2c81e284ee0875402f21f63bb693ae3da96eac6d18d6cfdefb4217b4` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/workflow/rerun.js | 250 | `e6463d98a64df5794190341fe03aa3123dbac1d7ac46160b95bed3daa038aa0c` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/workflow/set-changesets-pr-title.js | 768 | `05305204f28f947b74ffa055756958d8ed7589ef5ded1b7fe711d1e463064747` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/release/workflow/state.js | 3587 | `d118f68312375d260a438ebf70d01979fae780d35853b66bd873b72ee780979d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/remove-ignored-artifacts.js | 1318 | `d760c8c71b7a6936b34c663402ec735f254d157830c6f2df3c1497b59b4ec806` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/solhint-custom/index.js | 2652 | `ec74c407ef34fcd219172a93948f1b1dd8e68b945883f188ed478877593a65a3` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/solhint-custom/package.json | 85 | `61125d076ed3f59db01f41be15267ee9d40191d0d65e3083d515ee8810d7f761` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/scripts/update-docs-branch.js | 2099 | `8fdd058f08eb817bbf2e85565e8922cc4984a013909d8d4116006c147788f56d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/lib/openzeppelin-contracts/solhint.config.js | 619 | `008c12cfe2a018997f99bd41371fff76958fc1b6fbb6a43ecdd8ef5f989b1427` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package-lock.json | 414672 | `0b12305e50ac29f985ad2c1b8808842680ff1ddd244ce78803bf45fa46fb58c2` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/package.json | 3443 | `0b1026dd7a8713b67d5449919a4f78473f475217ec9e916b1f3987d1ec5f2689` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/checks/compare-layout.js | 662 | `9db6f11c491c88e94eb7ca6700f50bfca1b6cd0ac5e1842ee797f89bff001140` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/checks/compareGasReports.js | 7020 | `d6023ec6f9b7ca10b8fd11c515fe945523d611295ce9b56b9282ca45c2c77401` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/checks/extract-layout.js | 1122 | `2c94e7b5cb32f542c6e4a7dd137a0d567114fa604d447d800013bed1b680ccb0` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/checks/inheritance-ordering.js | 1949 | `b3f0fa6fd440d2b953a929d01f50b5ea3c13040143f402a8c396925861bc2ade` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/gen-nav.js | 984 | `4705c4cecad88a47dbb0dc8f1d854d17669b74851d57c16d6130cc6ebcf73af8` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/format-lines.js | 422 | `de8e8ae2542d2db777ff3441efdd1b3f549c5ba473f1071180451c5e25575c12` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/helpers/sanitize.js | 190 | `aa9db8aae572c1076e7d081114673a8fa56e8e228ff2f5e43d9454421e0686bb` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/run.js | 2121 | `6e4641dbcfe2497aee22efd326966f4e0bd68594447bae18e04ee35da5e6b1a7` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Arrays.js | 12302 | `1ba1b9d59a8523fd8a423fb745ec400fbf244c6d982e0c95f32914460c00d45e` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Arrays.opts.js | 78 | `4bd89ea1be08ae608a28dbc75c45a54bbf733c0367a988ed2b84e92d0f4bf826` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Checkpoints.js | 8367 | `7fd21b768ec4dec279ec9f67b26375df5f9180cc294c5ac919c69482ca096121` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Checkpoints.opts.js | 411 | `47ac1d11a3e082049539e930b28e179cb665ce2c04e64bb434a606a591accaba` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Checkpoints.t.js | 4529 | `f7d2f5f48d755be28c6fe3df505a961b2042989fc77316f8bdf221891f7f6e10` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/EnumerableMap.js | 9028 | `9ed4c302f2381ab72fcc586229b573e67dbab29c677fbea54aa9cad0ace4faa7` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/EnumerableMap.opts.js | 528 | `164f1188f6352dc2cf424c4dbc1b92e40d9ffe6a1ffec065d33ffb7a42bff552` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/EnumerableSet.js | 7776 | `424d5ba705cb5fe8094c5bf1c0f136668a3d0e447dfbf1972a57de26be31250c` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/EnumerableSet.opts.js | 301 | `5c7a9371981122981dd2f2ae3eb856b4632151e816279403bcd037a00c8f2a0e` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/MerkleProof.js | 8002 | `7fd6aca712d3cdcb5aa6ca603747c7713bfb11da4ec3dfbb13e4f865de03afa4` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/MerkleProof.opts.js | 307 | `b2dd437a8f00e7a973cceaf3d0faaa81f68c6a5e44cc9a48c6a9335c7b374de9` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Packing.js | 2746 | `8fc4918bb789bf933638263c872ce22fc9f68ce6ae4c36d9d1f398b56a3faa54` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Packing.opts.js | 72 | `795f4fc5182404c9c21b9d71c8156899c8f6956e5dbf3f74d6cfb6c59934368c` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Packing.t.js | 1601 | `df80c5e4323bb6b5d58d5f7a0df3de1c4c1fe22ddcab16f141e35db5c5d371f4` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/SafeCast.js | 3827 | `19b182fa8b42bdd1444b448780470d5229126f4dd39478ab87ee822c84490562` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/Slot.opts.js | 632 | `f566f7646afaa4a9731d38f05870539a2d2bfea84721c320aa1f4dd8a2879bfc` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/SlotDerivation.js | 3582 | `f61661b71363c9cf872f4a9162740c9d31c5fe3460ce139c9414d4db6afa96e3` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/SlotDerivation.t.js | 3235 | `4fb95dbeefc4fb0e08e1361df4a4614e9f60ae301a414e770606bebf878ea0d5` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/StorageSlot.js | 2321 | `daf387a4f34b198c78fe70fbeee28d5921630c6243c84fef988d04e4cbd6575f` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/StorageSlotMock.js | 1622 | `17cfce493dcaaa2e85ca1b01eea5bdc0ff8e501a4281c58073dc4852d0ebe899` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/TransientSlot.js | 2133 | `11c898c4383f44d34341d9230593b9cb0b94c27b43a2d4a4d3e9b6bb67998e85` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/TransientSlotMock.js | 804 | `5b8320fc0615731a32816a51e6ed535c72eaf8911217a69c66e85c4e49ff33e6` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/generate/templates/conversion.js | 678 | `134a41ead4e00cff47ef7d0f99b68dea2e730f5a8cc02dbca22f7603fb5b10f8` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/helpers.js | 155 | `58660f4bfe243e8720a6001ae4380d4329b2891b973bccc19a53d831c9535808` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/release/format-changelog.js | 1227 | `e98c4c231803fb239db92fef68e6191349379c73751e015909c2b384a0754d08` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/release/synchronize-versions.js | 481 | `477c2b3c846a9faf36afa1a66d3ed8a7008a80aaec5a096ee7ed4d6a3ac1d54a` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/release/update-comment.js | 1280 | `258bad59128bf2f39480fc719a0d8b4b5874d84a877ca00953854f66ce3ef48d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/release/workflow/github-release.js | 1660 | `4b88436e2c81e284ee0875402f21f63bb693ae3da96eac6d18d6cfdefb4217b4` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/release/workflow/rerun.js | 250 | `e6463d98a64df5794190341fe03aa3123dbac1d7ac46160b95bed3daa038aa0c` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/release/workflow/set-changesets-pr-title.js | 768 | `05305204f28f947b74ffa055756958d8ed7589ef5ded1b7fe711d1e463064747` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/release/workflow/state.js | 3587 | `d118f68312375d260a438ebf70d01979fae780d35853b66bd873b72ee780979d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/remove-ignored-artifacts.js | 1318 | `d760c8c71b7a6936b34c663402ec735f254d157830c6f2df3c1497b59b4ec806` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/solhint-custom/index.js | 2652 | `ec74c407ef34fcd219172a93948f1b1dd8e68b945883f188ed478877593a65a3` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/solhint-custom/package.json | 85 | `61125d076ed3f59db01f41be15267ee9d40191d0d65e3083d515ee8810d7f761` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/scripts/update-docs-branch.js | 2099 | `8fdd058f08eb817bbf2e85565e8922cc4984a013909d8d4116006c147788f56d` | 0 |
| lib/solidity-utils/lib/openzeppelin-contracts-upgradeable/solhint.config.js | 619 | `008c12cfe2a018997f99bd41371fff76958fc1b6fbb6a43ecdd8ef5f989b1427` | 0 |
| lib/solidity-utils/package-lock.json | 47298 | `a7c2dd97a9bcddd7dd0bbc24a64f8bb191199e1ee1cb675cf39fb1857e373404` | 0 |
| lib/solidity-utils/package.json | 1026 | `1134f75ad84e757e302b525d531d85896f123191938137e7056153adb0f2a033` | 0 |
| lib/solidity-utils/script/DeployCreate3Factory.s.sol | 548 | `ea9999f51bf86e79476d6f378491a01b9f71db19771fb06c938470a8d99c317e` | 0 |
| lib/solidity-utils/script/DeployTransparentProxyFactory.s.sol | 390 | `e97c23cc7b150f4c6c0c1d764a70882d71dc16ca6c8c0a88f870bc1d12aa927a` | 0 |
| lib/solidity-utils/src/contracts/access-control/Ownable2StepWithGuardian.sol | 1523 | `aa1f553084a1b43e8d3ee5c8af3ab3e0ffde9ebcd8d24421f03816761e3d56a6` | 0 |
| lib/solidity-utils/src/contracts/access-control/OwnableWithGuardian.sol | 1405 | `fe6accdda84a2cd84c1e1ee78272bdee37474caef987a9d33fdfb9598e2258b4` | 0 |
| lib/solidity-utils/src/contracts/access-control/UpgradeableOwnableWithGuardian.sol | 2840 | `c9cdc8141640c8bde0e7746d0d7474ea5d5e62f37863e56f188b46163ff9645d` | 0 |
| lib/solidity-utils/src/contracts/access-control/interfaces/IWithGuardian.sol | 861 | `c29e5b26507c8aebba6c527ca7b2e13d51345ffc71191d7f04f869b63e112105` | 0 |
| lib/solidity-utils/src/contracts/create3/Create3.sol | 5685 | `6b07f5f8628a6ffe15adbf2578e432c91e36fa256ed3ac5316899bcc04b52ff6` | 0 |
| lib/solidity-utils/src/contracts/create3/Create3Factory.sol | 1181 | `1aab50753bd407eea8f8643680a6965285bed1ae923693e09f0447bc318b89b2` | 0 |
| lib/solidity-utils/src/contracts/create3/interfaces/ICreate3Factory.sol | 1304 | `b84931d5a68e5e3fd6c89cecd9caded58312e90e7a23cb64ceb16b126606c59d` | 0 |
| lib/solidity-utils/src/contracts/oz-common/interfaces/IERC20WithPermit.sol | 295 | `26836607977779dfef47bbbdbf1ad921f357d5562009bce6ae046fb3cfee93df` | 0 |
| lib/solidity-utils/src/contracts/transparent-proxy/TransparentProxyFactory.sol | 938 | `a96f28c251e93ecbe9b95795253774bdc53cad21cbca0ad26463b4704f7ec923` | 0 |
| lib/solidity-utils/src/contracts/transparent-proxy/TransparentProxyFactoryBase.sol | 4072 | `a6d2c97623ac0ccdc258c70c92583fefb6d76eab77054723ce4aba2a4b2da9ee` | 0 |
| lib/solidity-utils/src/contracts/transparent-proxy/interfaces/IProxyAdminOzV4.sol | 600 | `656ca9d39211733a177038d9b3f1cdfafa5190a0e4ca25a5b94c46cb2b4a9fad` | 0 |
| lib/solidity-utils/src/contracts/transparent-proxy/interfaces/ITransparentProxyFactory.sol | 4626 | `4e3ec13b0802c245be9b3572242301e421d8a73730a937952f97ebe072a81d87` | 0 |
| lib/solidity-utils/src/contracts/utils/ChainHelpers.sol | 9962 | `120ee4b122e7ad7b44f627bf842e2258fa54a64ba5198e6a903dd0f9c072209d` | 0 |
| lib/solidity-utils/src/contracts/utils/PermissionlessRescuable.sol | 869 | `7ebffe62e4ffcf39be900346f934da6a175dbe4c44346039688b55e3e2d8bd4f` | 0 |
| lib/solidity-utils/src/contracts/utils/Rescuable.sol | 1109 | `b4056444ef602dce91173ca9633d967d050893c0bced667f76507b2533ff6c55` | 0 |
| lib/solidity-utils/src/contracts/utils/Rescuable721.sol | 706 | `bcf613ccb2f36c06cb55b03520c66b02ca0d9d318acdc25c004ed7d5694b5cf1` | 0 |
| lib/solidity-utils/src/contracts/utils/RescuableACL.sol | 1148 | `835b3d0fc5acd5f2b92b2f2c500b55568f8d8e51b78e9fdc7fc732c2435bfeb9` | 0 |
| lib/solidity-utils/src/contracts/utils/RescuableBase.sol | 1038 | `69ec34ed50cd18e36c22bdffd933c77b0ee0461c65a1a6a708c757fd8d20f636` | 0 |
| lib/solidity-utils/src/contracts/utils/ScriptUtils.sol | 6246 | `876ff2105d07c4d13c5cedd4e38c2879ea5d43f6e5383892b753665dd0e254e1` | 0 |
| lib/solidity-utils/src/contracts/utils/interfaces/IPermissionlessRescuable.sol | 1013 | `3230169945ae357ebdfc69e6d3123ac83499e1c5fa7dee4754137d5586fd3394` | 0 |
| lib/solidity-utils/src/contracts/utils/interfaces/IRescuable.sol | 936 | `31f74de49419286a116406d08c6d7c9973efb6119851f3b8a96cc60d822e77de` | 0 |
| lib/solidity-utils/src/contracts/utils/interfaces/IRescuable721.sol | 1099 | `2613b19ce07b44632c4e2d4752312449c0a9a1e4f252adb94e403d2c8836189e` | 0 |
| lib/solidity-utils/src/contracts/utils/interfaces/IRescuableBase.sol | 1302 | `b69ea2557f6b2b943e35c5ff4da1edbed8ebf55ecc932e1053915fb436c87f2f` | 0 |
| lib/solidity-utils/zksync/script/DeployTransparentProxyFactoryZkSync.s.sol | 377 | `fe83e1df43ba3fef4824a94d8e307cf95e7a344009492760a78c0f289fa09628` | 0 |
| lib/solidity-utils/zksync/src/contracts/transparent-proxy/TransparentProxyFactoryZkSync.sol | 2291 | `57a38e292f390866ef466bd5816f35da9375c798f021dc189554fbb75b73e12f` | 0 |
| lib/solidity-utils/zksync/src/contracts/transparent-proxy/interfaces/ITransparentProxyFactoryZkSync.sol | 341 | `3196f6f382883e3580f45cde2d417d385be0a18a0c5855cd3a3e47709bc07398` | 0 |
| lib/solidity-utils/zksync/src/contracts/utils/ScriptUtilsZkSync.sol | 3511 | `1b6a90b7e338efa127ca59f27a782ace2ab1b179830b5dac1f50a089952fcf8f` | 0 |
| lib/solidity-utils/zksync/src/contracts/utils/interfaces/ICreate2Factory.sol | 217 | `97f5be77accd440fc9b8f6e65d6aaad31ac3ee669d53850e1b25d73b223036d6` | 0 |
| package-lock.json | 47418 | `b7dccbe98cd688ee13df7b2a28b35020650a005855ff6541073c4fd7eab5efd1` | 0 |
| package.json | 884 | `18b7a1575cabf1d02382fbb5001cbe30e005f3b5b58a5c1341623a227de9117c` | 0 |
| scripts/DeployAaveV3MarketBatched.sol | 310 | `10b3a158c9af3446bd92ce58513de3351c4f1f2fbcb32c0e7d1c2566bee10e3d` | 0 |
| scripts/misc/DeployAaveV3MarketBatchedBase.sol | 2128 | `ed2bc5f813e279768ba2d787ea990779d32236574e28b4220d90f555a1a7df5e` | 0 |
| scripts/misc/LibraryPreCompileOne.sol | 3000 | `ea901b88e442755066b5e69867d087a66a68ed14a9680b3eb206b89030f07784` | 0 |
| scripts/misc/LibraryPreCompileTwo.sol | 3920 | `5044551d4dd39f64dd7fa76142605d945b13653d5ac60c4b927df003897c7126` | 0 |
| src/contracts/dependencies/chainlink/AggregatorInterface.sol | 1214 | `3dd71272f9898786dbdbdef85d458df2dd728c5ff81f27288f77db16c9d897ce` | 0 |
| src/contracts/dependencies/gnosis/contracts/GPv2SafeERC20.sol | 4742 | `f0ad28730616718a0d86eaebdaf1935ebdafcbf0fb4df4385cfac07c4515c02c` | 0 |
| src/contracts/dependencies/openzeppelin/contracts/AccessControl.sol | 6594 | `75f1dec8824dfe7cb89f98ae40d30b8898300898e2276e43a5fb0e9491d1d404` | 0 |
| src/contracts/dependencies/openzeppelin/contracts/Address.sol | 7381 | `1cb950c9d451fa88a3fcbec365945024eb7af7d100b240e7ae6ff6b89294188b` | 0 |
| src/contracts/dependencies/openzeppelin/contracts/Context.sol | 922 | `1217382f46e4175122036c664476e502ce49743c24c0efc930496662c8cbca99` | 0 |
| src/contracts/dependencies/openzeppelin/contracts/ERC165.sol | 908 | `0609907362f6c609348e2579fa37c210426027b2a98fd2f9ee166c7c3e7de774` | 0 |
| src/contracts/dependencies/openzeppelin/contracts/IAccessControl.sol | 2734 | `4b80cc5f5562669c36ff183211ea5738fe61ff6ff51b42dab5d1b6e98d82a147` | 0 |
| src/contracts/dependencies/openzeppelin/contracts/IERC165.sol | 769 | `0cc18a165b4201b999de9f90fdf23caa77f4bce8636e70c994c05c5c91350148` | 0 |
| src/contracts/dependencies/openzeppelin/contracts/Ownable.sol | 2105 | `663fc45b46658b2954e59e638c4073541a3e3a2d01e9aeb1d2a46636ef328072` | 0 |
| src/contracts/dependencies/openzeppelin/contracts/Strings.sol | 1834 | `25ff3f308b23f2d829f159005e5e917ce350c4b6161bdd43a9068808fe1cfa9f` | 0 |
| src/contracts/dependencies/openzeppelin/upgradeability/AdminUpgradeabilityProxy.sol | 1387 | `d6eb0c601beaf01f488ffe3a55634cc0203468cea7840564cfde95d36f63ba50` | 0 |
| src/contracts/dependencies/openzeppelin/upgradeability/BaseAdminUpgradeabilityProxy.sol | 3843 | `2ef03e9cf47b8fe0ac910dd0f9b130514df22398653512085ff2fd8f88bab660` | 0 |
| src/contracts/dependencies/openzeppelin/upgradeability/BaseUpgradeabilityProxy.sol | 1951 | `1b85e71d4ef4e473a7cd29c69f8f0845de7051d4f2aa2786ef1307893a93f04f` | 0 |
| src/contracts/dependencies/openzeppelin/upgradeability/InitializableAdminUpgradeabilityProxy.sol | 1545 | `4b2cb633246e7c198dbbebd11e10a483ac4d130525d52d8e87bded52ff6811db` | 0 |
| src/contracts/dependencies/openzeppelin/upgradeability/InitializableUpgradeabilityProxy.sol | 1223 | `496cde2ade866d2fcb6723dee4c1e42637c3a3437c3497e05d42763d362ac061` | 0 |
| src/contracts/dependencies/openzeppelin/upgradeability/Proxy.sol | 2448 | `f867281aaf8d9764c9b865176d65536253f108f24e5c6926fe0ac7b64c2d01e9` | 0 |
| src/contracts/dependencies/openzeppelin/upgradeability/UpgradeabilityProxy.sol | 1135 | `49d799e39488094998ebc2f7cf25643c09cd75b40e933cbf850a82f3bdb506e0` | 0 |
| src/contracts/dependencies/weth/WETH9.sol | 37536 | `442c9f615ae83aa474e6bd826f80cc90cc9a330a263c096a51af4126f53d1cdc` | 0 |
| src/contracts/extensions/stata-token/ERC20AaveLMUpgradeable.sol | 11510 | `5c385858549438c172f0376292466ad28c26f73ad1faa5a6b34cc42f68b1e96b` | 0 |
| src/contracts/extensions/stata-token/ERC4626StataTokenUpgradeable.sol | 11004 | `5078b1dbbf0c49ae635fc08db0f92d96d4fb45f1a5b9a0400d85734bf7f8515b` | 0 |
| src/contracts/extensions/stata-token/StataTokenFactory.sol | 3425 | `d0d03288a65b4361be1d897a75876858fe25e717935d0556dcbb0547dffcaebd` | 0 |
| src/contracts/extensions/stata-token/StataTokenV2.sol | 4247 | `b02df8d4107aa970bcab8e4449cd18afe4ba9e8a12e65f561e7aef60757f98c4` | 0 |
| src/contracts/extensions/stata-token/interfaces/IAToken.sol | 561 | `898118cddcdeb2e5dae95880add9f64f0c02995ba5aa51469151fd1f94f70767` | 0 |
| src/contracts/extensions/stata-token/interfaces/IERC20AaveLM.sol | 3649 | `82d63347e41c98dbb6e882d59dc87f644b07ad9b434840a06fe7155feb739ad2` | 0 |
| src/contracts/extensions/stata-token/interfaces/IERC4626StataToken.sol | 3034 | `400104a732c8ea99761070f9ef12e49646baa1091c425f14546551529cdacf10` | 0 |
| src/contracts/extensions/stata-token/interfaces/IStataTokenFactory.sol | 1879 | `068d757984b502b533a7083291cbe04caa5739fe78732063def144b0dea196ee` | 0 |
| src/contracts/extensions/stata-token/interfaces/IStataTokenV2.sol | 879 | `f1c3d00f7a022437cb6ae2ccd090d9c12acd7dce4fdb43fe1fd8fc8d466138e0` | 0 |
| src/contracts/extensions/v3-config-engine/AaveV3ConfigEngine.sol | 5204 | `8a5231bdf5dc1fe7dd4d844c67851e4c06923f6168d79f44426e0a2c54e8c18a` | 0 |
| src/contracts/extensions/v3-config-engine/AaveV3Payload.sol | 6794 | `cd0eb6523755f50d13bff0f5fea88b20f54d14536b03e185ff1e6af8433d0b9b` | 0 |
| src/contracts/extensions/v3-config-engine/EngineFlags.sol | 1497 | `8d316008b9d2c39df7a385fe167f42a312d5ad3ee4e508e971dad26e2daaeb10` | 0 |
| src/contracts/extensions/v3-config-engine/IAaveV3ConfigEngine.sol | 11388 | `23f6a26e179dbd9ae05f7832ab91373f9e53787629055c990b1076b6a532cc0e` | 0 |
| src/contracts/extensions/v3-config-engine/libraries/BorrowEngine.sol | 2023 | `d4d98cd55c6c50a2f02068a0ba4494b9ddf65748098dbd9bebbaf0444c5bafa5` | 0 |
| src/contracts/extensions/v3-config-engine/libraries/CapsEngine.sol | 959 | `bd64cc426751fa132607b61a7f125c59badd65be8113385c5ea8c7d3a88fa1a1` | 0 |
| src/contracts/extensions/v3-config-engine/libraries/CollateralEngine.sol | 3415 | `f79d8a95b074a97cb08af30e8b8da5e66566a93143387371ecb1589b46662099` | 0 |
| src/contracts/extensions/v3-config-engine/libraries/EModeEngine.sol | 7879 | `a1ac890a030a2ac3a0ffa66837e6f04cbb336cdd9461a3538364ece7b81a615b` | 0 |
| src/contracts/extensions/v3-config-engine/libraries/ListingEngine.sol | 5646 | `d06c0633de0b9d4f98c26bdb71f0f0a9d81276a5f58adcbf31f55c48df34199f` | 0 |
| src/contracts/extensions/v3-config-engine/libraries/PriceFeedEngine.sol | 1298 | `6b7cadf2a66bea01edfc7472c36a08dd52fc83f41dd2409f612c21225eb2ec06` | 0 |
| src/contracts/extensions/v3-config-engine/libraries/RateEngine.sol | 3622 | `e95bdbddc39d79b88a07c55d843301f3a0ed1f3bdf07c787ad56ae17354b1ba3` | 0 |
| src/contracts/helpers/AaveProtocolDataProvider.sol | 9769 | `0fe6e0b6a914b043557f3c29fe7c0c7a984a04a3e89941d0733a3534cc45f0ae` | 0 |
| src/contracts/helpers/L2Encoder.sol | 11816 | `a0b80d38d74a9ab7a2fb01d69193f0ef9f3a8b6676fb33234c047ae507d0c804` | 0 |
| src/contracts/helpers/LiquidationDataProvider.sol | 16062 | `2ef6d1e603584f5dc0aa09cb281327f134b4122b172d34203e75d1019a2e1420` | 0 |
| src/contracts/helpers/UiIncentiveDataProviderV3.sol | 12429 | `2a75d5d870bb233b60848675b26d40caec91fb3e8cc9481bdb25d550765185a0` | 0 |
| src/contracts/helpers/UiPoolDataProviderV3.sol | 11485 | `eedb5dd6006414590ca762254601a7e0cd1caf9b2e104f395253ee8bb958c79c` | 0 |
| src/contracts/helpers/WalletBalanceProvider.sol | 3681 | `28e7190c0289e72bd9f7f7420914678f96a785a618a3136fb35d0ec550f60fd4` | 0 |
| src/contracts/helpers/WrappedTokenGatewayV3.sol | 7966 | `7e6ca1463df95699c7e6a14dd80ab85e56bdf1b4dca03b2a1d8f3324fee6c91a` | 0 |
| src/contracts/helpers/interfaces/IERC20DetailedBytes.sol | 342 | `4049b52ec7da3cb852f9d5bea1054f74758a4523c929fefcc723f3bc6e56aa22` | 0 |
| src/contracts/helpers/interfaces/ILiquidationDataProvider.sol | 3827 | `382066ec4610e0853356f5d1a1fcba8f9cdf96234bf8b59488b40728c85704fe` | 0 |
| src/contracts/helpers/interfaces/IUiIncentiveDataProviderV3.sol | 1986 | `df49b6a87b301225cb645fd8eca75bfc17b4260292904a60ca9e119ac1e6e66d` | 0 |
| src/contracts/helpers/interfaces/IUiPoolDataProviderV3.sol | 2714 | `a59d9e5243d21299b8eff720ce0363f1b08926c442754a47b5d6ac7acb6a5145` | 0 |
| src/contracts/helpers/interfaces/IWETH.sol | 316 | `4c869110f35a0e9dbcd30fabf46b88a0bb1b3865416fb3b9f0e3bea99ace9c25` | 0 |
| src/contracts/helpers/interfaces/IWrappedTokenGatewayV3.sol | 828 | `0dc31b6ae9e04c226e7f96ece2d04ef417aedb533e479f54daef1db008178361` | 0 |
| src/contracts/instances/ATokenInstance.sol | 1663 | `5baee2a4b910e7b1a3532a57c7f7cda8b005024579e36e0aaca11395ca08560d` | 0 |
| src/contracts/instances/ATokenWithDelegationInstance.sol | 1803 | `26a88a7a71848d211e22edd8e8c563ad43edd7dd9a8beef9dde7c4133516b671` | 0 |
| src/contracts/instances/L2PoolInstance.sol | 695 | `29598978c55e5d6a04eb111831361d722be40db81ebac6e1a51c30b4077228a3` | 0 |
| src/contracts/instances/PoolConfiguratorInstance.sol | 773 | `588041d22fe79c8467622176cd6904f30d74de870ed2c686ffd8cd9675e2cfad` | 0 |
| src/contracts/instances/PoolInstance.sol | 1370 | `0062f84b7d8597fc9d25853a73fff8100e41cc9d6d3bc51b5571d15c1ae4c918` | 0 |
| src/contracts/instances/VariableDebtTokenInstance.sol | 1533 | `1d54af37833269dd9e1b0d36dbefdfa51dc981b676b6d8679a641c39edf7fab0` | 0 |
| src/contracts/instances/VariableDebtTokenMainnetInstanceGHO.sol | 1770 | `120648f447e9fd1bf931c93b7f11e910a1cfc651a284384c75749ba8e805e090` | 0 |
| src/contracts/interfaces/IACLManager.sol | 5458 | `079fec6a41263f1794fe150ef72afe3a91206a0e747b08e089a68241054c556a` | 0 |
| src/contracts/interfaces/IAToken.sol | 5688 | `d469a2379e46863f10835a93d4fadff7b75012352e65efc6de5d9c19de9cf665` | 0 |
| src/contracts/interfaces/IATokenWithDelegation.sol | 433 | `b8c411c7bd230df2b88a147174320106d57a2e427264c026d12bcdb25e34b76b` | 0 |
| src/contracts/interfaces/IAaveIncentivesController.sol | 842 | `9857909e595e80cab4df46c24a08fdcbb09661634da2dbd7fb3db3fc2e9a742f` | 0 |
| src/contracts/interfaces/IAaveOracle.sol | 2389 | `e55953dba6daa0883e7fb5776c6939cf6d28060e4d7733809a90bf454b31224b` | 0 |
| src/contracts/interfaces/ICreditDelegationToken.sol | 2711 | `7291dbabbb5ff0d8e3e550bef4ee6c6c43491bc46a8d0afaa121b50c4927d79a` | 0 |
| src/contracts/interfaces/IDefaultInterestRateStrategyV2.sol | 6100 | `d1764d65352eeb5dc1bc1114d9bb9e16528bf198a37cf4343d1b4baef01418ea` | 0 |
| src/contracts/interfaces/IDelegationToken.sol | 383 | `f3144b53fb3f17c2ab461aa89b8017c1ef0459360e198dd316834bf0c0d5decf` | 0 |
| src/contracts/interfaces/IERC20WithPermit.sol | 939 | `a171a6516109f7c0ba287460aa03ad5f88582182f0b15b6c27b96c7fb0587cef` | 0 |
| src/contracts/interfaces/IInitializableAToken.sol | 1703 | `314516bf207b02544a3bf78d9f572b91ad69de57f472a25bdc263e82eec8fef0` | 0 |
| src/contracts/interfaces/IInitializableDebtToken.sol | 1704 | `2de2252df825dbe518b1ab79507e937784a1e0e6b3ce80c45eae837a3ed10d5c` | 0 |
| src/contracts/interfaces/IL2Pool.sol | 5909 | `42694fa2d6962b1b6ae50c8fd1b30433b126f52b5434cdf19a89d3c2223c71e8` | 0 |
| src/contracts/interfaces/IPool.sol | 36349 | `ee58bacafc0b033adeaf673da3b08130d9f3a9a3eb563f7f19a03240e488eba7` | 0 |
| src/contracts/interfaces/IPoolAddressesProvider.sol | 8210 | `6a44f3a913093d62dd072d1691cf605a76262f56da42cbecdcf80607d8aeef94` | 0 |
| src/contracts/interfaces/IPoolAddressesProviderRegistry.sol | 2423 | `08d5c499c5256f79daa582e97324c6ddb60dce67586e27ad9776d8364602a3ae` | 0 |
| src/contracts/interfaces/IPoolConfigurator.sol | 19595 | `e84bcade8ae8bd981db571c25cab4f20f313b6e4800c4e0d8e9fff216b518da8` | 0 |
| src/contracts/interfaces/IPoolDataProvider.sol | 9705 | `1d0fef790c86ac5ad814320669b98023c93deb152dee43fd763d70837add400d` | 0 |
| src/contracts/interfaces/IPriceOracle.sol | 614 | `e87a38b53a95e45bf2cff3134982fd978394719bf16e06321e84574247d76573` | 0 |
| src/contracts/interfaces/IPriceOracleGetter.sol | 848 | `9bd6289493f501da6c097bedc6a01c69ea67eec5b15e644c585006452354580b` | 0 |
| src/contracts/interfaces/IReserveInterestRateStrategy.sol | 1120 | `e41e6d44206136dbba842ba00a24e7269ab9640fe81d44b1a51592b5a31b500e` | 0 |
| src/contracts/interfaces/IScaledBalanceToken.sol | 2735 | `ff2163d0ce74219b0df0211a1684d042aa6e545a01df5a78cef796673711b278` | 0 |
| src/contracts/interfaces/IVariableDebtToken.sol | 2251 | `0eec64cb5200a1a2fe2b4cdffa1716a00d132ddd0e3f1f709096f4996b7583c8` | 0 |
| src/contracts/misc/AaveOracle.sol | 5116 | `3dde068c1f25d0fa14508c0ba0521283b6df0ca2dd55bdbeb4d3e49efea0858a` | 0 |
| src/contracts/misc/DefaultReserveInterestRateStrategyV2.sol | 8506 | `74db0a12ae7a4312968c5db66d4f3dc46b0dadacfecd23d59905a75605b13a79` | 0 |
| src/contracts/misc/EmptyImplementation.sol | 247 | `3ff4a39eb6fa2f9db2ac971e62483622396a2bb05390ff0e8325873e8ca4d160` | 0 |
| src/contracts/misc/aave-upgradeability/BaseImmutableAdminUpgradeabilityProxy.sol | 2766 | `6314758bb3e9df078e5b686a6894cbf233d71206fde40efa438454fdf449c9f9` | 0 |
| src/contracts/misc/aave-upgradeability/InitializableImmutableAdminUpgradeabilityProxy.sol | 1060 | `b9db086d3c390c3e3fac8dfdf5795204e4e1746695ff37d511fc43c6d92d2337` | 0 |
| src/contracts/misc/aave-upgradeability/VersionedInitializable.sol | 2838 | `e948550a169e8060c75a55f9c003b80b7db4fbb6715723caa24be6f022f57ba3` | 0 |
| src/contracts/misc/flashloan/base/FlashLoanReceiverBase.sol | 699 | `9de5f04f8b7c3281ab5f2ac897ca7b017aae73639b9817f8055c0e4c3092b4d3` | 0 |
| src/contracts/misc/flashloan/base/FlashLoanSimpleReceiverBase.sol | 729 | `e872c503bfd7b59272d53fc4971ef14ba012c7cd02aa5337cb42ada373db9ff7` | 0 |
| src/contracts/misc/flashloan/interfaces/IFlashLoanReceiver.sol | 1433 | `1a0594fad068a04caf68d224954627dcc16f6ebcac9af8bf8a8eb1aadf7bc755` | 0 |
| src/contracts/misc/flashloan/interfaces/IFlashLoanSimpleReceiver.sol | 1399 | `ce956d7975d0bdb4b3f62596a58ffb4f60d2cba8d1d301ff1e5b2e424e2c78c5` | 0 |
| src/contracts/protocol/configuration/ACLManager.sol | 4389 | `47296b6e3f0b35de7c4856db24ce03fd748c140da7d02b53ed199dcf23c81c09` | 0 |
| src/contracts/protocol/configuration/PoolAddressesProvider.sol | 8296 | `134e0b3a2ac286d1a14459aae8a45541eed1877f3a043b7099e158d2332379a7` | 0 |
| src/contracts/protocol/configuration/PoolAddressesProviderRegistry.sol | 4064 | `add27223e76384b1097861ab3014630c243c7180326994badc5c8192996e90c6` | 0 |
| src/contracts/protocol/libraries/configuration/EModeConfiguration.sol | 1767 | `45c6e5140676fe39e4da32c3a77b4578862c72547ca48bc703f891bf592c8b9f` | 0 |
| src/contracts/protocol/libraries/configuration/ReserveConfiguration.sol | 17792 | `2c8bc42461625030d09ff1f82a2d0ff4ddb0843c633fe1f0c514998ce6ee422e` | 0 |
| src/contracts/protocol/libraries/configuration/UserConfiguration.sol | 7534 | `1cb5d65909b7e2d1c9fceb190d0e766a9a136454c62eec6fff63ee770052344c` | 0 |
| src/contracts/protocol/libraries/helpers/Errors.sol | 7363 | `3fcb25a17432c5787cb09e318a5f799ba9e87f890cc66b75f0a61ba3116c1e02` | 0 |
| src/contracts/protocol/libraries/helpers/TokenMath.sol | 4461 | `11ef1a7ea98b3fe23ff54a0de7b70e53a637ec40d74a7babcf3db89476d3c859` | 0 |
| src/contracts/protocol/libraries/logic/BorrowLogic.sol | 8125 | `daf57b87b1f9b669b7103c156ac6ae192b31ec74a60d57dc69e63730345d30bc` | 0 |
| src/contracts/protocol/libraries/logic/CalldataLogic.sol | 7725 | `22920525049b8598fdf7f4a0b1b03dd58a4cf5d4198695e2cf9a3eb1eba9003a` | 0 |
| src/contracts/protocol/libraries/logic/ConfiguratorLogic.sol | 6815 | `221fb8196a662db892cdc9b736b1ef448ac81357aaaf686681b17dfcf841d30d` | 0 |
| src/contracts/protocol/libraries/logic/FlashLoanLogic.sol | 10027 | `90df1fdadaa7702316e2847faa0ff99d36c27e56974a9d7abf393ece3e387b0c` | 0 |
| src/contracts/protocol/libraries/logic/GenericLogic.sol | 10585 | `4b18019505e4fbfab2624f371f28946557588c22f5c51e331fd2595613ba516d` | 0 |
| src/contracts/protocol/libraries/logic/LiquidationLogic.sol | 29642 | `5d344687e00ec2ced5d92e455bc2f8dd16af4ae547eea48ee8a3e840113ac291` | 0 |
| src/contracts/protocol/libraries/logic/PoolLogic.sol | 7259 | `1033a6ef0d1031f5e165faf7d3a912316310af7c37ac395379e3fbd2f8ca88d9` | 0 |
| src/contracts/protocol/libraries/logic/ReserveLogic.sol | 10890 | `1c32cb87bbc151310f151b9a3636086ecf6adfdc78610f4bf5b69e3299221d1a` | 0 |
| src/contracts/protocol/libraries/logic/SupplyLogic.sol | 12958 | `51a8ed9ed08bbe673809dd09af698f8a3f8de1f4aef9c83a04ae2fcfa62161a6` | 0 |
| src/contracts/protocol/libraries/logic/ValidationLogic.sol | 20419 | `0bfb51e54f0a8589fbf24bbc03046b12ee6f189641b7a2a6f1b2874acbb2bb45` | 0 |
| src/contracts/protocol/libraries/math/MathUtils.sol | 4474 | `92f6bc251d3ffb59eb2b338ae0a96da56016e2d37799b3587a34c943e39fa7b4` | 0 |
| src/contracts/protocol/libraries/math/PercentageMath.sol | 4088 | `26133fc790a19ad46e56a57e3698c1f03f651017fdeca13dcc808647c07b9e7f` | 0 |
| src/contracts/protocol/libraries/math/WadRayMath.sol | 5399 | `5155df4a005cb2e2901ae6752b3a30d57eb900eb91d2cd1bad0b9e12837c0d41` | 0 |
| src/contracts/protocol/libraries/types/ConfiguratorInputTypes.sol | 649 | `43ade55e20b7d84aa2bc4a4e1b55bb05eab37e3adff63a97d459693de5b0c6e7` | 0 |
| src/contracts/protocol/libraries/types/DataTypes.sol | 9720 | `fe0d923f73941f9dd674bbad4533379e2451fd04518bcd7bb6b3c14e57c49db1` | 0 |
| src/contracts/protocol/pool/L2Pool.sol | 3386 | `09adc62aab690e04fd7ab260e26a9b13fcd3004a86f4b1b9f8edd1d6a1e77b81` | 0 |
| src/contracts/protocol/pool/Pool.sol | 29046 | `ec6dbae72f43777446d8320f94eccbc6ae1dbe5daf1942502264bf0e35ef00fc` | 0 |
| src/contracts/protocol/pool/PoolConfigurator.sol | 23456 | `e9eb3e7d9f1b8c18bd1b265d5fcfe598a372d0b988daf403c082ae5afc5663ca` | 0 |
| src/contracts/protocol/pool/PoolStorage.sol | 2498 | `4433c66e52cb7e419da3dd523e6cbf324e87c2baaaa3c752f2b10513b7e147d2` | 0 |
| src/contracts/protocol/tokenization/AToken.sol | 12667 | `513164270664a93dc7714a95f32fe9388a34b19650ca46af71e356b22c9cc439` | 0 |
| src/contracts/protocol/tokenization/ATokenWithDelegation.sol | 4540 | `dc2107079711a666942950b41389cc483c894fecf9fe2557d8e832de59903268` | 0 |
| src/contracts/protocol/tokenization/VariableDebtToken.sol | 7674 | `244dea7e12ca08807e0718accece159867d9be8435808d5b495667e34ee50233` | 0 |
| src/contracts/protocol/tokenization/base/DebtTokenBase.sol | 4203 | `0c740994d6f62756a5ebc16197ef3f9e59df38424c4f769aecd89f744773dcd0` | 0 |
| src/contracts/protocol/tokenization/base/DelegationMode.sol | 166 | `dc51241d2b88bb2aff9fc883a61984594ac094fb31c09552508e98d83ef9c521` | 0 |
| src/contracts/protocol/tokenization/base/EIP712Base.sol | 1982 | `69274079f09e77d3c3282a7ab0315ab5aecb5f21bef491c8bfe77310331f01ea` | 0 |
| src/contracts/protocol/tokenization/base/IncentivizedERC20.sol | 10607 | `3f919aca784381b2384c8ab3eb49a42fa7576b302b93b22ee5c3164fdfba0cef` | 0 |
| src/contracts/protocol/tokenization/base/MintableIncentivizedERC20.sol | 2142 | `7d79efa674313cabb72a399b8f1c81cf803ad1053e4308accae82186026f47bd` | 0 |
| src/contracts/protocol/tokenization/base/ScaledBalanceTokenBase.sol | 5213 | `72d8157d7f31560d71b008f8ee0da540a737478364a12f9864d82cd8137fae78` | 0 |
| src/contracts/protocol/tokenization/delegation/BaseDelegation.sol | 16956 | `8c43b2cdd3e0ac56a750163667048b6d393765e567642ba8e2e4f34d0a0460a8` | 0 |
| src/contracts/protocol/tokenization/delegation/interfaces/IBaseDelegation.sol | 3775 | `20d9d651f79b13ac474b6b0ca46a7db4987c8d5776a62211669d7b14508a5c84` | 0 |
| src/contracts/rewards/EmissionManager.sol | 3698 | `1008b0c4bc306a2f1f8e47581921ead706819008dffedcb1ff9e275386a1c0b2` | 0 |
| src/contracts/rewards/RewardsController.sol | 13337 | `6aef6f4b12886409d875dc28775e38d3f5821453758dc38692f85eb2524cfd09` | 0 |
| src/contracts/rewards/RewardsDistributor.sol | 18309 | `87669efc1976d6b9a7f006373ce898a0f386d306470bb0a16841a731ab9c9d6e` | 0 |
| src/contracts/rewards/interfaces/IEmissionManager.sol | 5272 | `9dcfa2a9a8aeb4103dbe16c05336640a670fc8eb01b67c167e87746323224721` | 0 |
| src/contracts/rewards/interfaces/IPullRewardsTransferStrategy.sol | 374 | `edb1862101c364fc8ae887cc1c47abc23db39cb6532c58ac57825712b3901bd2` | 0 |
| src/contracts/rewards/interfaces/IRewardsController.sol | 9225 | `2c84525d80be02b2499124a21d1377bebcd5faf40ed9d069ed945e18408a93ef` | 0 |
| src/contracts/rewards/interfaces/IRewardsDistributor.sol | 6723 | `90bd37c6cf3797d64a96643ccffb4a38506a5cf87b54b06d20710472a03d8b54` | 0 |
| src/contracts/rewards/interfaces/IStakedToken.sol | 353 | `18e8c4f8978806d5579c500b293d8dcdd73dd43815cf86af127479a20dbc0688` | 0 |
| src/contracts/rewards/interfaces/IStakedTokenTransferStrategy.sol | 772 | `d1dd02034ef9a32c274ae4ee33957b4d8f92ef26ce1c02d17fc8deac65720115` | 0 |
| src/contracts/rewards/interfaces/ITransferStrategyBase.sol | 1369 | `e8577d5bcdb21dc6e7b0b96b3d114d2a48ac4c3d1251eb689824044924fea5da` | 0 |
| src/contracts/rewards/libraries/RewardsDataTypes.sol | 1667 | `7d2436d1de6c18932969fac63de0dd53343c7cfec1ec0133a8a644799918f85b` | 0 |
| src/contracts/rewards/transfer-strategies/PullRewardsTransferStrategy.sol | 1610 | `0d6a610715a16419ff7ace8f7efa10200691482582238dfac35e256e0b122b4f` | 0 |
| src/contracts/rewards/transfer-strategies/StakedTokenTransferStrategy.sol | 2558 | `849004de8ec2ad0f35791e42dd92959b82511decde40b613410aa38e96dd8933` | 0 |
| src/contracts/rewards/transfer-strategies/TransferStrategyBase.sol | 1831 | `f4f323fbf9167dcf73c34ea73ffd28a880bbe9611e7ce014788e8137fe8955ef` | 0 |
| src/contracts/treasury/Collector.sol | 11814 | `6b4f6b6402f85114c25f9856fee24c9d3747aeec816bf809e1b5e8d20304bb93` | 0 |
| src/contracts/treasury/ICollector.sol | 6611 | `7089f9689b61be533db9f7df0e40231bed6191f20257bd94e596e15517946f43` | 0 |
| src/deployments/contracts/LibraryReportStorage.sol | 339 | `9dde6d193d9b760a0f5954cd4c6ec5c4a07fba33cbef01f05d0d1e1df3ebd54b` | 0 |
| src/deployments/contracts/MarketReportStorage.sol | 217 | `6e543e3e01a938e9ba49224d0ba07fc08c3ad5676c0957d0889b2935d531bb2e` | 0 |
| src/deployments/contracts/procedures/AaveV3DefaultRateStrategyProcedure.sol | 464 | `fe63d70b5d5a7bb4e441266b9bc3ba14e47c7b3cfb134610432a29a8b9faf588` | 0 |
| src/deployments/contracts/procedures/AaveV3GettersProcedureOne.sol | 1467 | `7432112cd653c48413165048741b3327e60a10b31d3200fbfd9c00e61bfcf708` | 0 |
| src/deployments/contracts/procedures/AaveV3GettersProcedureTwo.sol | 1349 | `fde4efc2ece6302b5697940a7f06f5061c74dc619f1a01cf10097b388e4c3c4d` | 0 |
| src/deployments/contracts/procedures/AaveV3HelpersProcedureOne.sol | 1398 | `6155a7d57bd6fba2a68a7d95c1b8d692ca1e5e2edfa1678a823138d2d82cf775` | 0 |
| src/deployments/contracts/procedures/AaveV3HelpersProcedureTwo.sol | 1729 | `76b22e22def2a13e131ba4a48056b0e97c7ec79630e35ec45e73240645d49c12` | 0 |
| src/deployments/contracts/procedures/AaveV3IncentiveProcedure.sol | 585 | `73e02365cc836e66b8c75efbed6e75822f4f4e1b59f7138578efafe29d490bc8` | 0 |
| src/deployments/contracts/procedures/AaveV3L2PoolProcedure.sol | 1463 | `e76843913ba0c45554d508a2174bb56a96e950fc0a5d3f297936d3a50fd872f8` | 0 |
| src/deployments/contracts/procedures/AaveV3MiscProcedure.sol | 679 | `7254b0398c37b3ee298582a4c6d3f5ea87ba918aab94d5cfcacaa6f1adc5b2d0` | 0 |
| src/deployments/contracts/procedures/AaveV3OracleProcedure.sol | 636 | `2b5da269fbffd631ff2ff6884e85a25f9615081966fd1f0a66583e586244775e` | 0 |
| src/deployments/contracts/procedures/AaveV3PoolConfigProcedure.sol | 419 | `a8cf03aca962cf8964cec4e9fea0246b651dcaab583f839ba5c593002827d9e8` | 0 |
| src/deployments/contracts/procedures/AaveV3PoolProcedure.sol | 1445 | `060d0f5632bfc31205df1fee0db78a4aa188de0012b5eb54d5439cf09e599baa` | 0 |
| src/deployments/contracts/procedures/AaveV3SetupProcedure.sol | 7400 | `454c35b003b10070b2923dd3be78749bc79ae4ea6ae918eab5890b5837bf3fbf` | 0 |
| src/deployments/contracts/procedures/AaveV3TokensProcedure.sol | 1014 | `46f78a9d41059b1496c21534b2c1fbd87438d40d7d4001b7baf8647db54fe9c4` | 0 |
| src/deployments/contracts/procedures/AaveV3TreasuryProcedure.sol | 2193 | `d87504e5e478e169a1c94f6cbf1204f310f64d2123be94dc2b8cb8ec2d6e316d` | 0 |
| src/deployments/contracts/utilities/Create2Utils.sol | 1751 | `20b8622b31b0e7c32b0be18d42a85d73204b02225794a61c742ba760455ee983` | 0 |
| src/deployments/contracts/utilities/DeployUtils.sol | 2095 | `16c6c64c5a29158a9ffef6614eb83631dec3583db5a3c6851117e8ffdb6247fa` | 0 |
| src/deployments/contracts/utilities/FfiUtils.sol | 3273 | `6449401816fa437aab8c8ba39b63e49c9a39aab0265a09e5ce87e363cd1114d8` | 0 |
| src/deployments/contracts/utilities/MarketReportUtils.sol | 2284 | `14a0f8fa1148cdbea2906a54f6fe44a92fb9d5278c02fbb99f52d86efb9d3260` | 0 |
| src/deployments/contracts/utilities/MetadataReporter.sol | 6200 | `f03d3ffa6744396a26671581c1c3102cee9feb46cea4002836924bfed68db59e` | 0 |
| src/deployments/inputs/DefaultMarketInput.sol | 692 | `6379af0ba8736f5ce1870198cf1cef00d3ee4db9d8456bde13f195b52e69badb` | 0 |
| src/deployments/inputs/MarketInput.sol | 373 | `867a34edc518dcc7db3209f62d4c7ac92b76c44e875acc46fa1033a7a10080fe` | 0 |
| src/deployments/interfaces/IErrors.sol | 261 | `aee0fbc4f02390bbfd4dab916da59632086dcd9c6f0506ee7ac01e1a1bdaa849` | 0 |
| src/deployments/interfaces/ILibraryReportStorage.sol | 209 | `09be79affb6318239bc795ee1dac3a3e7859ce5d5c629f73746ab3a96ecbdcf9` | 0 |
| src/deployments/interfaces/IMarketReportStorage.sol | 169 | `240116f0692263c84752d8eed7cb4c4ad147c49e50549853760fab15af2a7ba1` | 0 |
| src/deployments/interfaces/IMarketReportTypes.sol | 4545 | `15d3ddd640acd0337cbab779d49797921f2eafc7e6f5fc0958fb41033b95795c` | 0 |
| src/deployments/interfaces/IMetadataReporter.sol | 531 | `1f564b50b334c3b84ee76b0bf77143a7de1f0d89bc054a4075ff1f0891e64826` | 0 |
| src/deployments/interfaces/IPoolReport.sol | 189 | `08d44dd8a13b08e8bc0b4d3078de5cfe373152f2d401b88b3e3beb9cbde4ef1f` | 0 |
| src/deployments/projects/aave-v3-batched/AaveV3BatchOrchestration.sol | 11401 | `cade82af4a6ec7e83b7c72964d3c97f899ac701a11dfad4503bd52b6b1a19bca` | 0 |
| src/deployments/projects/aave-v3-batched/batches/AaveV3GettersBatchOne.sol | 703 | `48ccd031c9af3d1881129f72b6cf73c361d33a2b605d9677458ab094f83deae2` | 0 |
| src/deployments/projects/aave-v3-batched/batches/AaveV3GettersBatchTwo.sol | 714 | `7e6743d68ce5cd20715d602f913fbdb744f3890129c8d43a02c8fb88061f48c3` | 0 |
| src/deployments/projects/aave-v3-batched/batches/AaveV3HelpersBatchOne.sol | 902 | `96dc8d9aa152bbe104e5e7ca0c411f75fb832409b896272a4cab13cde7ce1463` | 0 |
| src/deployments/projects/aave-v3-batched/batches/AaveV3HelpersBatchTwo.sol | 583 | `1fc6e81e6991638b3f82239112d1a9d4339667945b8f7b51c73b73de059b805d` | 0 |
| src/deployments/projects/aave-v3-batched/batches/AaveV3L2PoolBatch.sol | 574 | `d49441423fc1cfe7c625e81804b9d9a917620015f38f88f5e293e1403135e881` | 0 |
| src/deployments/projects/aave-v3-batched/batches/AaveV3MiscBatch.sol | 596 | `5e2137f2eb83479d55d2c8d1dc14aabbb90dc0ab900da06990552bc59b600466` | 0 |
| src/deployments/projects/aave-v3-batched/batches/AaveV3PeripheryBatch.sol | 1832 | `e3f875af23e512ef697524cd8e1f797b967660861b7bf5e1607df688a24accd1` | 0 |
| src/deployments/projects/aave-v3-batched/batches/AaveV3PoolBatch.sol | 637 | `040188b2cf539b0fd16a7ed4bd8d3facc77e55c8887461ac3b1884595fe38ce1` | 0 |
| src/deployments/projects/aave-v3-batched/batches/AaveV3SetupBatch.sol | 1971 | `9ebb6489cfaaa6903bb825937450d29383cdadd81f8ba54c285dad9939d36418` | 0 |
| src/deployments/projects/aave-v3-batched/batches/AaveV3TokensBatch.sol | 550 | `e10077917a01cc531b3e9f268e2bc3c223f32a9e5bde1cf2b75d234ac5387fa9` | 0 |
| src/deployments/projects/aave-v3-libraries/AaveV3LibrariesBatch1.sol | 676 | `e82dd02d6f3e5223fb9b3fe05b523d7aa4ed02c83565f06a652a62bd50feb188` | 0 |
| src/deployments/projects/aave-v3-libraries/AaveV3LibrariesBatch2.sol | 1271 | `97c775e90b63a857df7f562544e0e2dcc0ac3fa4e7a8e5df155eee49c525167e` | 0 |
