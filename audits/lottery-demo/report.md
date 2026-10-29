# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** lottery-demo · Демо-клиент
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-21 18:06 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 99320e04-794b-4c57-b9a9-0ea147fbcfb9 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `73de6bbc6c9edcedd4634eb26480047a3070d69b3c2421b669a4a8148817a2c0` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **3**
- Средняя: **1**
- Низкая: **0**
- Информационная: **1**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 0
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 5
- Долгосрочный постквантовый риск: 0
- Рекомендация по улучшению: 0
- Недостаточность данных: 0

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| Lottery.sol | 529 | `b067d3e6b6cebe0e9b77210cad59bb5db3fbf2e358115f7d25f35d1688d79463` | 0 |

## 3. Методология

| Область | Статус | Подробности |
|---|---|---|
| smart_contracts | проверено | Lottery.sol: built-in Solidity pattern checks |
| slither | проверено | Lottery.sol: slither 0.11.6 (pragma 0.8.28 -> solc 0.8.28) |

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree lottery-demo. 1 files analysed; of 1 files, 0 are test, fuzzing, benchmark or example code and were left out, 0 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **71** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 0.0%

## 7. Подробное описание находок

### QSI-2026-00254 — tx.origin используется для авторизации в Lottery.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Высокая
- Затронутый актив: `contract:Lottery.sol`
- Источник данных: Lottery.sol
- Метод обнаружения: Анализ шаблонов исходного кода Solidity.
- Анализатор: solidity 1.2.0 · 2026-10-21 18:06 UTC
- Балл приоритета: 71.6 / 100
- CVSS v3.1: неприменимо

Проверка авторизации через tx.origin в строка 14. (см. SWC-115)

**Возможные последствия.** Вредоносный контракт, вызванный владельцем, может пройти проверку (фишинговая атака).

**Шаги воспроизведения.**

```
Откройте строка 14 в предоставленном файле Lottery.sol и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · Lottery.sol · line 14 · SHA-256 2ba9b426538197a1edca2a6573fd3189e94ae6eb3bbf359d7ea987bf25b2b01d_

```
   12 | 
   13 |     function withdraw() external {
   14 |         require(tx.origin == owner, "not owner");
   15 |         payable(msg.sender).transfer(address(this).balance);
   16 |     }
```

**Ограничения проверки.** Облегчённый статический анализ шаблонов Solidity без компиляции и символьного исполнения. Не заменяет полноценный аудит смарт-контрактов; подтвердите вручную или специализированными инструментами (Slither, тесты Foundry).

**Рекомендация.** Используйте msg.sender для авторизации.

**Повторная проверка.** Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон.

### QSI-2026-00255 — Slither: arbitrary-send-eth в Lottery.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:Lottery.sol`
- Источник данных: Lottery.sol
- Метод обнаружения: JSON-вывод Slither 0.11.6.
- Анализатор: slither 1.2.0 · 2026-10-21 18:06 UTC
- Балл приоритета: 46.4 / 100
- CVSS v3.1: неприменимо

Lottery.withdraw() (Lottery.sol#13-16) sends eth to arbitrary user
	Dangerous calls:
	- address(msg.sender).transfer(address(this).balance) (Lottery.sol#15)


**Возможные последствия.** Влияние по оценке Slither: High.

**Шаги воспроизведения.**

```
slither Lottery.sol --detect arbitrary-send-eth
```

**Подтверждающие доказательства.**

_tool_output · slither 0.11.6 · line 13 · SHA-256 b80d4d2639b98f960875417a42224e70ac52945dffdcfd2f2f780b62d6983e4e_

```
Lottery.withdraw() (Lottery.sol#13-16) sends eth to arbitrary user
	Dangerous calls:
	- address(msg.sender).transfer(address(this).balance) (Lottery.sol#15)

```

**Ограничения проверки.** Результат внешнего статического анализатора; возможны ложные срабатывания.

**Рекомендация.** Изучите документацию детектора Slither «arbitrary-send-eth» и исправьте или обоснуйте.

**Повторная проверка.** Повторно запустите slither.

### QSI-2026-00256 — Slither: weak-prng в Lottery.sol

- Серьёзность: **Высокая** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:Lottery.sol`
- Источник данных: Lottery.sol
- Метод обнаружения: JSON-вывод Slither 0.11.6.
- Анализатор: slither 1.2.0 · 2026-10-21 18:06 UTC
- Балл приоритета: 46.4 / 100
- CVSS v3.1: неприменимо

Lottery.pickWinner(address[]) (Lottery.sol#8-11) uses a weak PRNG: "i = uint256(keccak256(bytes)(abi.encodePacked(block.timestamp,block.prevrandao))) % players.length (Lottery.sol#9)" 


**Возможные последствия.** Влияние по оценке Slither: High.

**Шаги воспроизведения.**

```
slither Lottery.sol --detect weak-prng
```

**Подтверждающие доказательства.**

_tool_output · slither 0.11.6 · line 8 · SHA-256 49aff3270921d2a86c544c28fa1c05962ebee3afbf1fff64c6a317c9c3410bef_

```
Lottery.pickWinner(address[]) (Lottery.sol#8-11) uses a weak PRNG: "i = uint256(keccak256(bytes)(abi.encodePacked(block.timestamp,block.prevrandao))) % players.length (Lottery.sol#9)" 

```

**Ограничения проверки.** Результат внешнего статического анализатора; возможны ложные срабатывания.

**Рекомендация.** Изучите документацию детектора Slither «weak-prng» и исправьте или обоснуйте.

**Повторная проверка.** Повторно запустите slither.

### QSI-2026-00257 — Slither: tx-origin в Lottery.sol

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:Lottery.sol`
- Источник данных: Lottery.sol
- Метод обнаружения: JSON-вывод Slither 0.11.6.
- Анализатор: slither 1.2.0 · 2026-10-21 18:06 UTC
- Балл приоритета: 41.3 / 100
- CVSS v3.1: неприменимо

Lottery.withdraw() (Lottery.sol#13-16) uses tx.origin for authorization: require(bool,string)(tx.origin == owner,not owner) (Lottery.sol#14)


**Возможные последствия.** Влияние по оценке Slither: Medium.

**Шаги воспроизведения.**

```
slither Lottery.sol --detect tx-origin
```

**Подтверждающие доказательства.**

_tool_output · slither 0.11.6 · line 13 · SHA-256 94e1c4c8f5c507814d63d8beccdf0c9acf3fb68f044e843b69f364d9366ce6ce_

```
Lottery.withdraw() (Lottery.sol#13-16) uses tx.origin for authorization: require(bool,string)(tx.origin == owner,not owner) (Lottery.sol#14)

```

**Ограничения проверки.** Результат внешнего статического анализатора; возможны ложные срабатывания.

**Рекомендация.** Изучите документацию детектора Slither «tx-origin» и исправьте или обоснуйте.

**Повторная проверка.** Повторно запустите slither.

### QSI-2026-00258 — Slither: immutable-states в Lottery.sol

- Серьёзность: **Информационная** · Классификация: Потенциальный криптографический риск · Уверенность: Высокая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `contract:Lottery.sol`
- Источник данных: Lottery.sol
- Метод обнаружения: JSON-вывод Slither 0.11.6.
- Анализатор: slither 1.2.0 · 2026-10-21 18:06 UTC
- Балл приоритета: 42.0 / 100
- CVSS v3.1: неприменимо

Lottery.owner (Lottery.sol#5) should be immutable 


**Возможные последствия.** Влияние по оценке Slither: Optimization.

**Шаги воспроизведения.**

```
slither Lottery.sol --detect immutable-states
```

**Подтверждающие доказательства.**

_tool_output · slither 0.11.6 · line 5 · SHA-256 fad8d91b70936aed2495f6871e3d8646d25422ceca5066eeea75429eaedc2dd5_

```
Lottery.owner (Lottery.sol#5) should be immutable 

```

**Ограничения проверки.** Результат внешнего статического анализатора; возможны ложные срабатывания.

**Рекомендация.** Изучите документацию детектора Slither «immutable-states» и исправьте или обоснуйте.

**Повторная проверка.** Повторно запустите slither.


## 8. Постквантовая оценка

| | Обмен ключами (x — сколько данные должны оставаться конфиденциальными; «собери сейчас, расшифруй потом») | Подписи (x — сколько подписи и ключи должны оставаться доверенными) |
|---|---|---|
| Срок жизни данных/ключей x | 10 | 10 |
| Время миграции y | 5 | 5 |
| Принятое число лет до CRQC z | 8 (early) | 8 |
| x + y − z | 7 → при этом сценарии миграция завершится слишком поздно | 7 → при этом сценарии миграция завершится слишком поздно |
_Допущения планирования: x для обмена ключами, x для подписей, y — значения по умолчанию профиля риска «Криптобиржа, кастодиан или кошелёк», а не данные клиента; с фактическими сроками клиента вывод может измениться._

### Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет


**Следующий шаг:** Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (вхождений) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (1) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (1) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P1 | QSI-2026-00254 | Используйте msg.sender для авторизации. | устранение первопричины | Повторите статический анализ и добавьте модульный/фазз-тест, проверяющий шаблон. |
| P1 | QSI-2026-00255 | Изучите документацию детектора Slither «arbitrary-send-eth» и исправьте или обоснуйте. | устранение первопричины | Повторно запустите slither. |
| P1 | QSI-2026-00256 | Изучите документацию детектора Slither «weak-prng» и исправьте или обоснуйте. | устранение первопричины | Повторно запустите slither. |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-00257 | Изучите документацию детектора Slither «tx-origin» и исправьте или обоснуйте. | устранение первопричины | Повторно запустите slither. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P4 | QSI-2026-00258 | Изучите документацию детектора Slither «immutable-states» и исправьте или обоснуйте. | устранение первопричины | Повторно запустите slither. |

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

## 12. Источники и нормативные документы

1. A. Chailloux, M. Naya-Plasencia, A. Schrottenloher — An Efficient Quantum Collision Search Algorithm and Implications on Symmetric Cryptography (ASIACRYPT 2017; IACR ePrint 2017/847) — IACR ePrint. <https://eprint.iacr.org/2017/847> (peer-reviewed article: Õ(2^{2n/5}) time, O(n) qubits, Õ(2^{n/5}) classical memory)
2. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
3. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
4. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
5. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
6. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
7. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
8. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
9. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
10. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
11. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
12. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
13. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
14. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)
15. Smart Contract Weakness Classification (SWC) Registry — SWC community (no longer actively maintained). <https://swcregistry.io/> (historic reference; still widely cited)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Расположение | Квантовый статус | Классический статус |
|---|---|---|---|---|---|
| Keccak-256 | Keccak-256 |  | Lottery.sol:9 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
