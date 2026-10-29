# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** noir @ 5c98fecd3fe6 · Aztec / Noir — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-28 12:43 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 0108930a-6e1d-4e97-9cb8-4ce727b1eddd (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Web3-проект |
| SHA-256 содержимого | `2512370e8b29a06abeaab2de23760dd081e1e98edb7e4afa39272d2dc1a07889` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **2**
- Средняя: **5**
- Низкая: **3**
- Информационная: **3**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 7
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 3
- Рекомендация по улучшению: 2
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 5, y = 5, z = 12 → запас минимален. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/noir-lang/noir> @ `5c98fecd3fe6c51bd9e3a605cafe412d25ae8915` — ссылки в доказательствах открывают строки на этом коммите.

783 файлов, всего 15026939 байт, редактирований: 6; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 730 | .claude/skills/reduce-ssa-repro/scripts/reduce_branches.py: 76 lines scanned with 16 rule patterns and 122 registry patterns; .claude/skills/reduce-ssa-repro/scripts/reduce_instructions.py: 36 lines scanned with 16 rule patterns and 122 registry patterns; .claude/skills/reduce-ssa-repro/scripts/ssa_reduce_common.py: 90 lines scanned with 16 rule patterns and 122 registry patterns |
| dependencies | проверено | 49 | Cargo.lock: 626 dependencies parsed (626 pinned); Cargo.toml: 92 dependencies parsed (1 pinned); acvm-repo/acir/Cargo.toml: 26 dependencies parsed (0 pinned) |
| secrets | проверено | 4 | docs/docusaurus.config.ts: value(s) at line(s) 173 are not reported as secrets because the source annotates them as published (publishable, search-only, safe to commit); that is the project's own decision, recorded here rather than raised against it; docs/docusaurus.config.ts: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); docs/src/theme/SearchBar/index.js: 2 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| osv_advisories | проверено | 1 | 1000 pinned packages queried at OSV.dev; 9 affected (3 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree noir at 5c98fecd3fe6c51bd9e3a605cafe412d25ae8915. 783 files analysed; of 7491 files, 5336 are test, fuzzing, benchmark or example code and were left out, 1371 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **63** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 23.1%

## 7. Подробное описание находок

### QSI-2026-04754 — quick-xml 0.26.0 затронут RUSTSEC-2026-0194

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/quick-xml@0.26.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:43 UTC
- Балл приоритета: 36.9 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает RUSTSEC-2026-0194 для пакета crates.io quick-xml версии 0.26.0: Quadratic run time when checking a start tag for duplicate attribute names. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0194
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0194](https://osv.dev/vulnerability/RUSTSEC-2026-0194) · manifest · SHA-256 028cd2f8044c5c52031532eb91141d581476948b4fd115c63b565c4f52398450_

```
{"id": "RUSTSEC-2026-0194", "aliases": [], "modified": "2026-07-02T08:00:03.849273679Z", "summary": "Quadratic run time when checking a start tag for duplicate attribute names", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.41.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04755 — quick-xml 0.26.0 затронут RUSTSEC-2026-0195

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/quick-xml@0.26.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:43 UTC
- Балл приоритета: 36.9 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает RUSTSEC-2026-0195 для пакета crates.io quick-xml версии 0.26.0: Unbounded namespace-declaration allocation in `NsReader` enables memory-exhaustion denial of service. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0195
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0195](https://osv.dev/vulnerability/RUSTSEC-2026-0195) · manifest · SHA-256 7934c935f3154b61c623e871c948769f40fd83ae102d44328fbedb576471f986_

```
{"id": "RUSTSEC-2026-0195", "aliases": [], "modified": "2026-07-02T09:00:04.037478193Z", "summary": "Unbounded namespace-declaration allocation in `NsReader` enables memory-exhaustion denial of service", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.41.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04747 — Квантово-уязвимый Pedersen commitment: пороговая подпись и протоколы MPC (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Pedersen commitment:threshold_mpc`
- Источник данных: noir_stdlib/docs/search-index.js
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:43 UTC
- Балл приоритета: 33.0 / 100
- CVSS v3.1: неприменимо

3 упоминаний Pedersen commitment в 2 файл(ах), например noir_stdlib/docs/search-index.js:747. Роль по путям, именам функций и соседнему коду: пороговая подпись и протоколы MPC. Paillier, обязательства Педерсена и доказательства на дискретном логарифме внутри пороговых ECDSA и EdDSA ломаются алгоритмом Шора; постквантовая пороговая схема — это смена протокола, а не параметра.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте noir_stdlib/docs/search-index.js:747 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [noir_stdlib/docs/search-index.js](https://github.com/noir-lang/noir/blob/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915/noir_stdlib/docs/search-index.js#L747) · line 747 · SHA-256 c865f6e9a97269c32e2fa4a30f1dd66762ce7273ba94d2214ba16c48e982cafe_

```
  746 |   {"name":"pattern","path":"std::meta::expr::LetExpression","kind":"method","url":"std/meta/expr/struct.LetExpression.html#pattern","desc":"The let pattern."},
  747 |   {"name":"pedersen_commitment","path":"std::hash","kind":"fn","url":"std/hash/fn.pedersen_commitment.html","desc":"Returns the Pedersen commitment to `input`, a point on the embedded curve."},
  748 |   {"name":"pedersen_commitment_with_separator","path":"std::hash","kind":"fn","url":"std/hash/fn.pedersen_commitment_with_separator.html","desc":"Returns the Pedersen commitment to `input`, using the generators starting at index `separator`."},
```

_file_excerpt · [noir_stdlib/docs/search-index.js](https://github.com/noir-lang/noir/blob/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915/noir_stdlib/docs/search-index.js#L748) · line 748 · SHA-256 b3e6981a6a935b9a5f50c20c520d81ceb087a2477f44d2030c3d8f65692837e3_

```
  747 |   {"name":"pedersen_commitment","path":"std::hash","kind":"fn","url":"std/hash/fn.pedersen_commitment.html","desc":"Returns the Pedersen commitment to `input`, a point on the embedded curve."},
  748 |   {"name":"pedersen_commitment_with_separator","path":"std::hash","kind":"fn","url":"std/hash/fn.pedersen_commitment_with_separator.html","desc":"Returns the Pedersen commitment to `input`, using the generators starting at index `separator`."},
  749 |   {"name":"pedersen_hash","path":"std::hash","kind":"fn","url":"std/hash/fn.pedersen_hash.html","desc":"Returns the Pedersen hash of `input`."},
```

_file_excerpt · [tooling/nargo_cli/build.rs](https://github.com/noir-lang/noir/blob/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915/tooling/nargo_cli/build.rs#L198) · line 198 · SHA-256 090e65c4c5b3665c3aef84188e286ed043308ab831eb05c782f35393d639d76e_

```
  197 |     "pedersen_hash",
  198 |     "pedersen_commitment",
  199 |     "simple_shield",
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-04745 — Квантово-уязвимый BLS12-381: роль не определена (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:BLS12-381:general`
- Источник данных: acvm-repo/acir_field/src/lib.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:43 UTC
- Балл приоритета: 31.7 / 100
- CVSS v3.1: неприменимо

4 упоминаний BLS12-381 в 2 файл(ах), например acvm-repo/acir_field/src/lib.rs:29. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте acvm-repo/acir_field/src/lib.rs:29 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [acvm-repo/acir_field/src/lib.rs](https://github.com/noir-lang/noir/blob/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915/acvm-repo/acir_field/src/lib.rs#L29) · line 29 · SHA-256 5ef8035ca5016f5ca434eb8295f1af786ef489ac4c8890078f4f8851d74cb6b6_

```
   28 | cfg_if::cfg_if! {
   29 |     if #[cfg(feature = "bls12_381")] {
   30 |         pub type FieldElement = field_element::FieldElement<ark_bls12_381::Fr>;
```

_file_excerpt · [acvm-repo/acir_field/src/lib.rs](https://github.com/noir-lang/noir/blob/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915/acvm-repo/acir_field/src/lib.rs#L51) · line 51 · SHA-256 fc93008b5289e4b009809dde3bdfb6bd7d8d552f31ca2bec12ba474c79fd6e9d_

```
   50 | // If another field/feature is added, we add it here too
   51 | assert_unique_feature!("bn254", "bls12_381");
```

_file_excerpt · [compiler/noirc_frontend/src/hir/def_collector/dc_mod.rs](https://github.com/noir-lang/noir/blob/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915/compiler/noirc_frontend/src/hir/def_collector/dc_mod.rs#L1574) · line 1574 · SHA-256 6f570af6c25488dc4995999726a07201763d6e51c3f699dd846170334b86760a_

```
 1573 | cfg_if::cfg_if! {
 1574 |     if #[cfg(feature = "bls12_381")] {
 1575 |         pub const CHOSEN_FIELD: &str = "bls12_381";
```

_file_excerpt · [compiler/noirc_frontend/src/hir/def_collector/dc_mod.rs](https://github.com/noir-lang/noir/blob/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915/compiler/noirc_frontend/src/hir/def_collector/dc_mod.rs#L1575) · line 1575 · SHA-256 a5e47145a00a8408eb20222f49c481a98309879a058cbd6528211ee46b47d4c1_

```
 1574 |     if #[cfg(feature = "bls12_381")] {
 1575 |         pub const CHOSEN_FIELD: &str = "bls12_381";
 1576 |     } else {
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-04746 — Квантово-уязвимый ECDSA: роль не определена (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: acvm-repo/blackbox_solver/src/ecdsa/mod.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:43 UTC
- Балл приоритета: 31.7 / 100
- CVSS v3.1: неприменимо

4 упоминаний ECDSA в 2 файл(ах), например acvm-repo/blackbox_solver/src/ecdsa/mod.rs:17. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте acvm-repo/blackbox_solver/src/ecdsa/mod.rs:17 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [acvm-repo/blackbox_solver/src/ecdsa/mod.rs](https://github.com/noir-lang/noir/blob/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915/acvm-repo/blackbox_solver/src/ecdsa/mod.rs#L17) · line 17 · SHA-256 f01f9f03b5190eedd00a0ec020b31adac727f7a27a09ca0c36a8d0e104dfc4fd_

```
   16 | 
   17 | mod secp256k1;
   18 | mod secp256r1;
```

_file_excerpt · [acvm-repo/blackbox_solver/src/ecdsa/mod.rs](https://github.com/noir-lang/noir/blob/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915/acvm-repo/blackbox_solver/src/ecdsa/mod.rs#L18) · line 18 · SHA-256 4d5337c2f8f0fa13ae1345bc7ec04c7db897a775799697da617aa523feae5c68_

```
   17 | mod secp256k1;
   18 | mod secp256r1;
   19 | 
```

_file_excerpt · [noir_stdlib/docs/search-index.js](https://github.com/noir-lang/noir/blob/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915/noir_stdlib/docs/search-index.js#L883) · line 883 · SHA-256 62da9cb93d0e74c59029e1ffed11489d4da682ad63a0673b17c0f8ba5d978046_

```
  882 |   {"name":"verify_proof_with_type","path":"std","kind":"fn","url":"std/fn.verify_proof_with_type.html","desc":"Asserts the validity of the provided proof and public inputs against the provided verification key and hash."},
  883 |   {"name":"verify_signature","path":"std::ecdsa_secp256k1","kind":"fn","url":"std/ecdsa_secp256k1/fn.verify_signature.html","desc":"Verifies an ECDSA signature over the secp256k1 curve, returning `true` if it is valid."},
  884 |   {"name":"verify_signature","path":"std::ecdsa_secp256r1","kind":"fn","url":"std/ecdsa_secp256r1/fn.verify_signature.html","desc":"Verifies an ECDSA signature over the secp256r1 curve, returning `true` if it is valid."},
```

_file_excerpt · [noir_stdlib/docs/search-index.js](https://github.com/noir-lang/noir/blob/5c98fecd3fe6c51bd9e3a605cafe412d25ae8915/noir_stdlib/docs/search-index.js#L884) · line 884 · SHA-256 9aac36b88cfefd6bd01be47f2f48f2a3f469bd3ac96bfb4c4934ddfacdd7c9ff_

```
  883 |   {"name":"verify_signature","path":"std::ecdsa_secp256k1","kind":"fn","url":"std/ecdsa_secp256k1/fn.verify_signature.html","desc":"Verifies an ECDSA signature over the secp256k1 curve, returning `true` if it is valid."},
  884 |   {"name":"verify_signature","path":"std::ecdsa_secp256r1","kind":"fn","url":"std/ecdsa_secp256r1/fn.verify_signature.html","desc":"Verifies an ECDSA signature over the secp256r1 curve, returning `true` if it is valid."},
  885 |   {"name":"visibility","path":"std::FunctionDefinition","kind":"method","url":"std/primitive.FunctionDefinition.html#visibility","desc":"Returns the function's visibility."},
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-04750 — block-buffer 0.10.4 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/block-buffer@0.10.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:43 UTC
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

### QSI-2026-04751 — block-buffer 0.12.0 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/block-buffer@0.12.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:43 UTC
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

### QSI-2026-04749 — anyhow 1.0.102 затронут RUSTSEC-2026-0190 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/anyhow@1.0.102`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:43 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0190 для пакета crates.io anyhow версии 1.0.102: Unsoundness in `Error::downcast_mut()`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (anyhow::Error::downcast_mut); anyhow приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-04752 — crypto-bigint 0.7.5 затронут RUSTSEC-2026-0387 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crypto-bigint@0.7.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:43 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0387 для пакета crates.io crypto-bigint версии 0.7.5: Multiple timing variability issues in operations intended to be constant-time. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-04753 — ctutils 0.4.2 затронут RUSTSEC-2026-0385 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/ctutils@0.4.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:43 UTC
- Балл приоритета: 18.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0385 для пакета crates.io ctutils версии 0.4.2: Non-constant-time mask generation and `u128` comparisons. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0385
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0385](https://osv.dev/vulnerability/RUSTSEC-2026-0385) · manifest · SHA-256 200470326c8a5ad19deb3639dff41d33749b1153097b6b87ef95e4beec747848_

```
{"id": "RUSTSEC-2026-0385", "aliases": [], "modified": "2026-10-23T08:30:02.389575143Z", "summary": "Non-constant-time mask generation and `u128` comparisons", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.4.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04756 — 2 бюллетеней в 2 пакет(ах) crates.io, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:crates.io:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:43 UTC
- Балл приоритета: 13.7 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 2 бюллетеней (0 с оценкой high или critical) для 2 пакет(ов) crates.io, которые подтягивают только инструменты разработки или сборки (Cargo.lock): например, memmap2@0.9.10 [dev]: RUSTSEC-2026-0186; paste@1.0.15 [dev]: RUSTSEC-2024-0436. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в Cargo.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (crates.io)](https://osv.dev/) · Cargo.lock · SHA-256 4432f38b22ecdb27f2fdf942c82ab00ad5ebdc8cb28f274788c454fae46b3131_

```
memmap2@0.9.10 [dev]: RUSTSEC-2026-0186
paste@1.0.15 [dev]: RUSTSEC-2024-0436
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04757 — 4 бюллетеней в 1 пакет(ах) npm, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:npm:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:43 UTC
- Балл приоритета: 13.7 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 4 бюллетеней (1 с оценкой high или critical) для 1 пакет(ов) npm, которые подтягивают только инструменты разработки или сборки (docs/yarn.lock): например, @fastify/static@9.0.0 [dev]: GHSA-83w8-p2f5-377r, GHSA-8pvw-jcv7-9cmj, GHSA-pr96-94w5-mx2h, GHSA-x428-ghpx-8j92. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в docs/yarn.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · docs/yarn.lock · SHA-256 57059e43bdd93f6f0fbb0262407368e044c83934ee508fccd0ff2e8b29eb781a_

```
@fastify/static@9.0.0 [dev]: GHSA-83w8-p2f5-377r, GHSA-8pvw-jcv7-9cmj, GHSA-pr96-94w5-mx2h, GHSA-x428-ghpx-8j92
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-04748 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:43 UTC
- Балл приоритета: 12.2 / 100
- CVSS v3.1: неприменимо

В 49 манифестах зависимостей QSI нашёл криптобиблиотеки (@noble/curves, @noble/hashes, ecdsa, elliptic, ethers, jsonwebtoken, k256, node-forge, p256, ring, rustls), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · Cargo.lock, Cargo.toml, acvm-repo/acir/Cargo.toml, acvm-repo/acir_field/Cargo.toml, acvm-repo/acvm/Cargo.toml, acvm-repo/acvm_js/Cargo.toml, acvm-repo/acvm_js/package.json, acvm-repo/blackbox_solver/Cargo.toml, acvm-repo/bn254_blackbox_solver/Cargo.toml, acvm-repo/brillig/Cargo.toml, acvm-repo/brillig_vm/Cargo.toml, acvm-repo/msgpack_tagged/Cargo.toml, acvm-repo/msgpack_tagged_derive/Cargo.toml, compiler/fm/Cargo.toml, compiler/noirc_arena/Cargo.toml, compiler/noirc_driver/Cargo.toml, compiler/n · SHA-256 66f3a6317b0d70de54ab9d35f6f0f7d0d79da34df4d6af027ed3ee449c742509_

```
Crypto libraries: @noble/curves, @noble/hashes, ecdsa, elliptic, ethers, jsonwebtoken, k256, node-forge, p256, ring, rustls
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
| **пороговая подпись и протоколы MPC** | Pedersen commitment (2) | QSI-2026-04747 | Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли |
| **роль не определена** | BLS12-381 (2), ECDSA (2) | QSI-2026-04745, QSI-2026-04746 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм в конечных полях | взламывает | Q1 | BLS12-381 (2) | Взламывает Диффи–Хеллмана в конечных полях и DSA при любом размере. Переводите установление ключей на ML-KEM (на переходный период — гибрид с X25519 или ECDH), подписи — на ML-DSA или SLH-DSA. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | BLS12-381 (2), ECDSA (5), Pedersen commitment (2) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | AES-128 (2), BLAKE3 (1) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | BLAKE3 (1) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-04754 | Обновите quick-xml до исправленной версии (0.41.0). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2026-0194. |
| P2 | QSI-2026-04755 | Обновите quick-xml до исправленной версии (0.41.0). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2026-0195. |
| P2 | QSI-2026-04750 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-04751 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-04749 | Разберите RUSTSEC-2026-0190; при необходимости обновите anyhow до исправленной версии (1.0.103). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0190 или результат разбора записан. |
| P3 | QSI-2026-04752 | Разберите RUSTSEC-2026-0387; при необходимости обновите crypto-bigint до исправленной версии (0.7.6). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0387 или результат разбора записан. |
| P3 | QSI-2026-04753 | Разберите RUSTSEC-2026-0385; при необходимости обновите ctutils до исправленной версии (0.4.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0385 или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-04747 | Внесите использования Pedersen commitment в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-04745 | Внесите использования BLS12-381 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-04746 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-04747 | Запланируйте миграцию Pedersen commitment на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-04745 | Запланируйте миграцию BLS12-381 на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-04746 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-04756 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |
| P4 | QSI-2026-04757 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |

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
21. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-08-19T19:30:06.686866977Z)
22. OSV advisory RUSTSEC-2026-0190 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0190> (modified 2026-06-29T14:15:03.650725453Z)
23. OSV advisory RUSTSEC-2026-0194 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0194> (modified 2026-07-02T08:00:03.849273679Z)
24. OSV advisory RUSTSEC-2026-0195 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0195> (modified 2026-07-02T09:00:04.037478193Z)
25. OSV advisory RUSTSEC-2026-0385 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0385> (modified 2026-10-23T08:30:02.389575143Z)
26. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
27. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
28. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
29. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
30. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| AES-128 | AES-128 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 2 | 2 | acvm-repo/acvm/src/pwg/blackbox/aes128.rs; acvm-repo/blackbox_solver/src/aes128.rs:4 |
| BLAKE3 |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 1 | 1 | acvm-repo/blackbox_solver/src/hash.rs:20 |
| Crypto library | 0.14.0 | k256 (RustCrypto elliptic curves) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.14.0 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.17.0 | ecdsa (python-ecdsa) | н/п | допустимо | 2 | 2 | Cargo.lock; acvm-repo/blackbox_solver/Cargo.toml |
| Crypto library | 0.17.14 | ring (ring (Rust)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.23.46 | rustls (rustls) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | workspace | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | acvm-repo/blackbox_solver/Cargo.toml |
| Crypto library | workspace | k256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | acvm-repo/blackbox_solver/Cargo.toml |
| Crypto library | 9.0.3 | jsonwebtoken (jsonwebtoken (Node)) | н/п | допустимо | 1 | 1 | docs/yarn.lock:15115 |
| Crypto library | 1.4.0 | node-forge (node-forge) | н/п | допустимо | 1 | 1 | docs/yarn.lock:17372 |
| Crypto library | 1.2.0 | @noble/curves (noble-curves) | н/п | допустимо | 2 | 2 | docs/yarn.lock:4910; yarn.lock:1640 |
| Crypto library | 1.3.2 | @noble/hashes (noble-hashes) | н/п | допустимо | 2 | 2 | docs/yarn.lock:4919; yarn.lock:1676 |
| Crypto library | 1.4.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 2 | 2 | docs/yarn.lock:4926; yarn.lock:1683 |
| Crypto library | 1.3.3 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | docs/yarn.lock:4933 |
| Crypto library | 1.9.0 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:1649 |
| Crypto library | 2.2.0 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:1658 |
| Crypto library | 1.9.7 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | yarn.lock:1667 |
| Crypto library | 1.8.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:1690 |
| Crypto library | 2.2.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:1697 |
| Crypto library | 2.4.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | yarn.lock:1704 |
| Crypto library | 6.6.1 | elliptic (elliptic (Node)) | н/п | допустимо | 1 | 1 | yarn.lock:5902 |
| Crypto library | 6.17.0 | ethers (ethers.js) | н/п | допустимо | 1 | 1 | yarn.lock:6351 |
| BLS12-381 |  |  | уязвим (Шор) | допустимо | 2 | 2 | acvm-repo/acir_field/src/lib.rs:29; compiler/noirc_frontend/src/hir/def_collector/dc_mod.rs:1574 |
| ECDSA |  |  | уязвим (Шор) | допустимо | 1 | 1 | acvm-repo/acvm/src/pwg/blackbox/signature/ecdsa.rs |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 2 | 2 | acvm-repo/blackbox_solver/src/ecdsa/mod.rs:17; noir_stdlib/docs/search-index.js:883 |
| ECDSA | P-256 |  | уязвим (Шор) | допустимо | 2 | 2 | acvm-repo/blackbox_solver/src/ecdsa/mod.rs:18; noir_stdlib/docs/search-index.js:884 |
| Pedersen commitment |  |  | уязвим (Шор) | допустимо | 2 | 2 | noir_stdlib/docs/search-index.js:747; tooling/nargo_cli/build.rs:198 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| .claude/skills/reduce-ssa-repro/scripts/reduce_branches.py | 3110 | `70839c108194af26fd3d9aa6aaf5271035bb87913faa0e2fa91b5498ad3a5e61` | 0 |
| .claude/skills/reduce-ssa-repro/scripts/reduce_instructions.py | 1400 | `cd59a1719b909b67d0faf5ca168a6b230abd4e9c3feace07d79795a5a918e0f9` | 0 |
| .claude/skills/reduce-ssa-repro/scripts/ssa_reduce_common.py | 3358 | `d9e027eed72e577bd71345326313ef4575b1a9892d712f7cbfd938ee369d0e5e` | 0 |
| Cargo.lock | 164950 | `ec3ab0b89cd8aa5a758ae62e78f29d3721691e137446c64a03f570b8078e1216` | 0 |
| Cargo.toml | 8364 | `9f411e26e8aab0426d8709b2777e3c33e96d89a1d9aa8df178db48558f5f6498` | 0 |
| acvm-repo/acir/Cargo.toml | 1698 | `9f8043f63bb4d9e5e1051669d4bc6ff266d5724517a9ac61d8652d5716299b93` | 0 |
| acvm-repo/acir/codegen/acir.cpp | 453651 | `57697b4da7d13101774a6c22cf27fdc731b8bce1bde379ce9d5bc9bf58b2b5b9` | 0 |
| acvm-repo/acir/codegen/witness.cpp | 15865 | `795d994ff21697d289c0f757349785fe17d61821a2eb4d9cb6af96ab7133cc91` | 0 |
| acvm-repo/acir/src/circuit/black_box_functions.rs | 8989 | `9f9a0bd65930300a5e8237eee16b2b93c4a03efa84f9573d0d50af5360584ddf` | 0 |
| acvm-repo/acir/src/circuit/brillig.rs | 5358 | `89d08b52da503419147d99f30ffdbce5f263f4e8ecac53c32ded19a455af3c79` | 0 |
| acvm-repo/acir/src/circuit/mod.rs | 27413 | `67783906d32070ca9ab9d098bd9d9915d13c5871f29e1bb34a7aab7e6763bc8f` | 0 |
| acvm-repo/acir/src/circuit/opcodes/black_box_function_call.rs | 37400 | `5fcccaca8a2cea678f99835b7f6a5b9cc3b293cf8036ef6807d7dfd27ad140ef` | 0 |
| acvm-repo/acir/src/circuit/opcodes/function_id.rs | 940 | `64ff11881dc81af5d67dc3d2897332370397c81ca90d292cd419fdd96275ca91` | 0 |
| acvm-repo/acir/src/circuit/opcodes/memory_operation.rs | 2575 | `5379deafef30f799e0c6d90ea3de9971c9c5beb4b2018cb3d92f07658567973f` | 0 |
| acvm-repo/acir/src/circuit/opcodes.rs | 11684 | `7c253548c71d4b36d014909d4a0f77c4de8a8c4926a286f0fade2569c3c9c73e` | 0 |
| acvm-repo/acir/src/lib.rs | 59318 | `0c3b50ed5a2bace10297512ee98793f5e1cd167e35d79fa3c9cedde2c1dde0e9` | 0 |
| acvm-repo/acir/src/native_types/expression/mod.rs | 24732 | `c843eeb23ab31418a27abfef80c56abe8dc408e2c3ef0a624edf0e39db825af5` | 0 |
| acvm-repo/acir/src/native_types/expression/operators.rs | 15602 | `cdffe0711720a51e0c0bcdb59254c74759ae9f2addca10688292cb11120b30cd` | 0 |
| acvm-repo/acir/src/native_types/mod.rs | 376 | `686e65be16912195a5441c57293253eb0fe03ceae408c5acff49458c54116cd2` | 0 |
| acvm-repo/acir/src/native_types/witness.rs | 908 | `e8b643d95fd3086b83e91ebd596941e1240c5b0d27770b4e0d4084abdfeaabd2` | 0 |
| acvm-repo/acir/src/native_types/witness_map.rs | 6316 | `24f06dd3fafc50b5d1ddfc20378ebd79d5932be1e9fa7aab1b0ca1d6572a93c2` | 0 |
| acvm-repo/acir/src/native_types/witness_stack.rs | 8561 | `f15996a1682290c7e4cd642ec946461bceeb63999005399b2ca0fa55b2677ed1` | 0 |
| acvm-repo/acir/src/parser/lexer.rs | 8743 | `5f08bc7bfa56bfb1bd950a9bcf183fe0366f663f8f259edc29b22b813114e978` | 0 |
| acvm-repo/acir/src/parser/mod.rs | 38947 | `96a5510fd9a5192bbadd2e647d176355bc5dda43aaf0c95871abfc19587a4875` | 0 |
| acvm-repo/acir/src/parser/span.rs | 1550 | `55f147d93fa0e379aa2da9f413dcd3cc50144df74dc33e65a5bba7a458027f5c` | 0 |
| acvm-repo/acir/src/parser/token.rs | 8197 | `5d77f576d7c2ad29ae0ec5b7d8c46bee6375c6f12406d32955c5c6da7878a2a0` | 0 |
| acvm-repo/acir/src/serialization.rs | 23441 | `4a0109a4f882c30658cd4a2fa2c513133d52606c72d7d438b885a9b43264bab7` | 0 |
| acvm-repo/acir_field/Cargo.toml | 887 | `5fd8d8241458b3aaf5398027af7bd4d3e023a3e8271292b65a3fa12ce930f932` | 0 |
| acvm-repo/acir_field/src/field_element.rs | 36294 | `08676d736eda3ebe3fe17850aa8533a361e1f9037d593ee7968bd3ee8a8277e5` | 0 |
| acvm-repo/acir_field/src/generic_ark.rs | 8915 | `f58b1232bdaf34fe847dba6e17d506ece14cd520c0bb813965ef6ec624999ee2` | 0 |
| acvm-repo/acir_field/src/lib.rs | 1782 | `9fbdab3d5a523f14a81ef30ba3e386b3114b3d08630970e392c3dd3787b85f98` | 0 |
| acvm-repo/acvm/Cargo.toml | 1549 | `231931e461bcf4c4ddc80cf6a8d94d32d981de2ef66ee41dbe34bf40f6503dbd` | 0 |
| acvm-repo/acvm/src/bin/generate_acvm_js_fixtures.rs | 17185 | `1ca235446fe08a6d6f99014df83ac5e3d40330ef8a3736c25531e3ca90117b44` | 0 |
| acvm-repo/acvm/src/compiler/mod.rs | 5642 | `2ccd2fd83fce3a5e333d0727f3ddaab22b17cd19d1712a99a375433ec069600a` | 0 |
| acvm-repo/acvm/src/compiler/optimizers/common_subexpression/csat.rs | 34115 | `9641516145924aba013a6f5f4d42fc25430698e5ea69ff31fe3473bdc22cbf20` | 0 |
| acvm-repo/acvm/src/compiler/optimizers/common_subexpression/merge_expressions.rs | 18146 | `0517317b9f36bad6e2d2c131dc00ba949acccb040c469fee1c0f721e0a4e5d32` | 0 |
| acvm-repo/acvm/src/compiler/optimizers/common_subexpression/mod.rs | 30078 | `835781fef49bc0ddca07bb1a3329af9fba4f56ab58292b31218926d4cc484de2` | 0 |
| acvm-repo/acvm/src/compiler/optimizers/general.rs | 7245 | `bac3a06cefcf35da32f0fec96b8a944440ede8101eb93805ab8b533699c0a609` | 0 |
| acvm-repo/acvm/src/compiler/optimizers/mod.rs | 5129 | `87656db759a7b37200381d7da3500e9a6e5ad332af148668017ad5e728366162` | 0 |
| acvm-repo/acvm/src/compiler/optimizers/redundant_range.rs | 35851 | `db13c99f30d83ed655b95ebf97d944ed715a92822f16fe259f22729c2e6c2e6c` | 0 |
| acvm-repo/acvm/src/compiler/simulator.rs | 16709 | `e91ee853b008a6f78eb303978b3e0a63f1a94e44b3b1f44abe8ee10289a85116` | 0 |
| acvm-repo/acvm/src/compiler/validator.rs | 48909 | `45cbb268aced56a3c4c8d45f103e67f23f5ba97bfd148e029a99f743b7ed3006` | 0 |
| acvm-repo/acvm/src/lib.rs | 621 | `480e5910c9bddf1307c425dd6634f9068eeb450112eabcb2dc5d9e005c048d5a` | 0 |
| acvm-repo/acvm/src/pwg/arithmetic.rs | 18306 | `796a570a67b74dc843061ea99df294cab9176f877d5bd80c577ad3f75e5d47c2` | 0 |
| acvm-repo/acvm/src/pwg/blackbox/aes128.rs | 9999 | `eb466b369c54a54341cfacc438388bf692b6ea07a68ef82374446b16770922be` | 0 |
| acvm-repo/acvm/src/pwg/blackbox/embedded_curve_ops.rs | 9860 | `d60cbeac1295d96102916b293d46fb6972f275e1daa45214c81e1e06991c0ccd` | 0 |
| acvm-repo/acvm/src/pwg/blackbox/hash.rs | 9086 | `1525051e55458e4e3880484944f1bb8a11e7ccbc9aaeb2aa81411fde7209300d` | 0 |
| acvm-repo/acvm/src/pwg/blackbox/logic.rs | 5913 | `9bf2cfd98ce982212b6d04083088ce6859099c4a73ea6355a3c58b7bd646ee6d` | 0 |
| acvm-repo/acvm/src/pwg/blackbox/mod.rs | 6723 | `cf80ddd3f387dc10283d57393c5f8edc54907129f4bbc0c4e66eb7ecd4d9e72f` | 0 |
| acvm-repo/acvm/src/pwg/blackbox/range.rs | 1945 | `e5cd0ba74cdcf17802afd04495876c1851f7e61c6c2acb5e7deca35a5ca5d025` | 0 |
| acvm-repo/acvm/src/pwg/blackbox/signature/ecdsa.rs | 1348 | `eaf48a147983d27fed05c4a30993a7c11ac5a3e8c1c85e187892f8ce4f917945` | 0 |
| acvm-repo/acvm/src/pwg/blackbox/signature/mod.rs | 22 | `ed2c51e41894469dbd58786325b8fc73c5fbd08634287fa02bc2a6ba2e9a1cf7` | 0 |
| acvm-repo/acvm/src/pwg/blackbox/utils.rs | 1224 | `03805c10a43581b9fbf8e3d3b4e325f836b06062b582d97560f67e61fc25b070` | 0 |
| acvm-repo/acvm/src/pwg/brillig.rs | 22242 | `1cde6b1d0c9ac7249791b7d9ee4886e027c8fde7de6f364aaa49d590a14a00c9` | 0 |
| acvm-repo/acvm/src/pwg/memory_op.rs | 7342 | `b5b0ca59b17796165eaa9e6a2df1437668fec97d03adee1c82fe9ea0dd12c5ed` | 0 |
| acvm-repo/acvm/src/pwg/mod.rs | 48800 | `bc95468315008937bcc7533ab16e5490e529e1de3f968ec0f18bcf77a14aad3d` | 0 |
| acvm-repo/acvm_js/.cargo/config.toml | 164 | `c0738019cf1c19917f4cf2353a20464b8cc1772749555b7cd379c90a8828d43e` | 0 |
| acvm-repo/acvm_js/Cargo.toml | 1490 | `f6c6e6e3fdedd6db494d84c6a15ebdd8d96048c5995d177a643e77c1268321da` | 0 |
| acvm-repo/acvm_js/build.rs | 259 | `2c7bcf65b5a6c2b15d33305f558b172b11c97f0a7f75c480245070eb87836c09` | 0 |
| acvm-repo/acvm_js/package.json | 1538 | `9a45b27073980edf9344d1ac876207220e5e8602df98a7efd995b2c204e0a998` | 0 |
| acvm-repo/acvm_js/src/black_box_solvers.rs | 2836 | `f3a73b441bc9b6cb2b5b2c0dc298b5fd1875ff8f545b3040a96029aa37b212c8` | 0 |
| acvm-repo/acvm_js/src/build_info.rs | 1471 | `58ba527f40cdb92195240c2a77fbd636b013f648ed50a60d648eee89801fd3e5` | 0 |
| acvm-repo/acvm_js/src/compression.rs | 2686 | `8df76f6bb8b0c17d3c8793cab1c7fbcb30f0c7cfe8993f217b6c9c716e947c5c` | 0 |
| acvm-repo/acvm_js/src/execute.rs | 13875 | `fb35d30f9038a0ca272675e6b5da216dd6e8d1f8fdc8102dc770085bc4efd0ff` | 0 |
| acvm-repo/acvm_js/src/foreign_call/inputs.rs | 596 | `785e05adbc27d48bdbc53b3576b39a6f12cc87e4e4cf7c01b7166dc5075da71d` | 0 |
| acvm-repo/acvm_js/src/foreign_call/mod.rs | 2790 | `28747d915cb9f90b7d9b7f99691dd11a7de9cd87e14c4f5dd63bd67ffa148a8d` | 0 |
| acvm-repo/acvm_js/src/foreign_call/outputs.rs | 1199 | `816d154c7e75da472a2864714c6ee3a3395a1948d73c4e407858a2e323cced17` | 0 |
| acvm-repo/acvm_js/src/js_execution_error.rs | 3729 | `c99c926322e4ff5abc78fa31361ffff3a1e72f0a13a9e559299615420b03faad` | 0 |
| acvm-repo/acvm_js/src/js_witness_map.rs | 5086 | `4d7198ecbd2acc71123d5ff8b4553019b75654707d3f6ab4272ccc7e4a1bfe1d` | 0 |
| acvm-repo/acvm_js/src/js_witness_stack.rs | 2388 | `3628a06b710cd1a2826e236fed36cfb8be86f21be2818d3e12adb3c87c6e1713` | 0 |
| acvm-repo/acvm_js/src/lib.rs | 1041 | `89d09755de093889182e73386bf0573a962eec1656f354492f32d8ec848ed5d9` | 0 |
| acvm-repo/acvm_js/src/logging.rs | 1622 | `cf5363298aab2829bae532395168ec9e1e21431fdc1ecb792993abfeec1ca892` | 0 |
| acvm-repo/acvm_js/src/public_witness.rs | 4939 | `c52b1f65f6cca083a6f70cc03c6122cdd958bef6ec0e0c0199abf242b0761ec7` | 0 |
| acvm-repo/acvm_js/web-test-runner.config.mjs | 812 | `0388db69afbcb04a1c21bd68c3247782afd5383b40a25569f06a43afae279a36` | 0 |
| acvm-repo/blackbox_solver/Cargo.toml | 1331 | `1d8977412d6f093b78f28efd984fc3cb235dd79a32dbb4bf409e44af1bbaa4ea` | 0 |
| acvm-repo/blackbox_solver/src/aes128.rs | 917 | `1959ae88c5548e39c877e6485da8c6d32924506e5c6cdd59099b8a992a6ad593` | 0 |
| acvm-repo/blackbox_solver/src/curve_specific_solver.rs | 1899 | `f7e21ab6422e14cbe5860017ce409a4b590314b01b211f6a6f89fba8e5cd66ef` | 0 |
| acvm-repo/blackbox_solver/src/ecdsa/mod.rs | 5381 | `df622a397fa228475a1d208be2675428e963447f72e71c2fe1757dcc7a320333` | 0 |
| acvm-repo/blackbox_solver/src/ecdsa/secp256k1.rs | 4098 | `61aeeec62a4fc7a565da779f66681a5560ed006d41b6ea836fdb7c1960bb3020` | 0 |
| acvm-repo/blackbox_solver/src/ecdsa/secp256r1.rs | 3825 | `54096363290947aba5ef2c01e743148b96c706df2d67269449a65910b2a28646` | 0 |
| acvm-repo/blackbox_solver/src/hash.rs | 3692 | `c88453111b46b5f377866dbfcc56400e57b69db47e3b1408b394b888bd314c99` | 0 |
| acvm-repo/blackbox_solver/src/lib.rs | 1093 | `00af3681a70830a49ac828b0c47ab720d86b8c1a8178147b3f9bfe95a51c1f69` | 0 |
| acvm-repo/blackbox_solver/src/logic.rs | 4516 | `8ee40c6214185ba7fa457bcddb861088bb593091ccf2a4ffcb4fe7f494209c5c` | 0 |
| acvm-repo/bn254_blackbox_solver/Cargo.toml | 919 | `285df8ebf092003a5bf05154e0b639a4f9ec3fa3078d2da84a13768c629d338e` | 0 |
| acvm-repo/bn254_blackbox_solver/src/embedded_curve_ops.rs | 15790 | `2e227412c7caa0edc74b70f25a22328fc3c5972b09b937135b1fe371bc074e6b` | 0 |
| acvm-repo/bn254_blackbox_solver/src/generator/generators.rs | 6973 | `b9c1f58e85ac79eae0e9a291584605e455dbe03cd1b6c56ba5b23598d7f48ea1` | 0 |
| acvm-repo/bn254_blackbox_solver/src/generator/hash_to_curve.rs | 4983 | `a9849a52fc57e93ccc601d7551792bf35a5a2f1ff8431280d567d13adada06c4` | 0 |
| acvm-repo/bn254_blackbox_solver/src/generator/mod.rs | 317 | `9e583b96d01a8eecfa9f2c6983fa74faf3316ce333466e87ebdf145e479bda09` | 0 |
| acvm-repo/bn254_blackbox_solver/src/lib.rs | 1848 | `0edd6798823980cbc2bba300e084bbc595b8e5ed10e30220f8bd60ff540fdb4a` | 0 |
| acvm-repo/bn254_blackbox_solver/src/poseidon2.rs | 9140 | `b337e12594a8d59d097d2bd84c8e0e6f3dcd4d07a88a0735c45935bc251afa42` | 0 |
| acvm-repo/bn254_blackbox_solver/src/poseidon2_constants.rs | 30136 | `97e0985b1ecb4400ee3526c5273ee1f44a80397ef7b822e8b9924b6c123175f7` | 0 |
| acvm-repo/brillig/Cargo.toml | 796 | `ac99544e46b29371d3702c2cdb697d4cc2fdcea7b2c9533af17d3555e0053110` | 0 |
| acvm-repo/brillig/src/black_box.rs | 7075 | `4a05789d7902f3a2cbc6794e9273ade3ad850fcc060378b7f683769707398213` | 0 |
| acvm-repo/brillig/src/foreign_call.rs | 7351 | `cc6d63f85ced306c8d0750b2a80455440a10288adfdec8cd1e1c41c33612ce57` | 0 |
| acvm-repo/brillig/src/lengths.rs | 9727 | `3bdb5eb53c6af7e47dc3d8a6a6277d1570fe81bc7c7223c8e4bebb2c70ac70d1` | 0 |
| acvm-repo/brillig/src/lib.rs | 496 | `c5c0eeb8a4540a148a20b01d4a394ccc6f843dc62f196f5ab80996876aa6c13f` | 0 |
| acvm-repo/brillig/src/opcodes.rs | 34320 | `b615829998c29caeabbec5061a8980d8c3ac478627175f3016d2c8400e6d8853` | 0 |
| acvm-repo/brillig_vm/Cargo.toml | 862 | `9decfd388603fe9e2a2b1f3f0a792739d90dcd954f69b8747226fbe00b68a75d` | 0 |
| acvm-repo/brillig_vm/src/arithmetic.rs | 40485 | `6d9bfe9438906ef6b4e1317399acd476e2f08c31923d58ce7dfcac0e1002384c` | 0 |
| acvm-repo/brillig_vm/src/black_box.rs | 20356 | `df0bda711c58003136b67eac124ceb316c9807df0b6a81c8ee143cb526430cef` | 0 |
| acvm-repo/brillig_vm/src/cast.rs | 4419 | `ac4be1ac68b1050b41d69ed0bdabc6cb5d0e52b922dcae2ae0d9aeb48f7f98ba` | 0 |
| acvm-repo/brillig_vm/src/foreign_call.rs | 25939 | `ae3cd0d5ae312840908ba172a93d84832c1b633152069f50fedf5dde6a37cc24` | 0 |
| acvm-repo/brillig_vm/src/fuzzing.rs | 8882 | `bf7cc1d582c11b87c1dea6a45b21be3b3dbc1a12e7ae7c3943878c0fef3c3a42` | 0 |
| acvm-repo/brillig_vm/src/lib.rs | 27571 | `0ffc83adf39f1565fbbecd5127ed6164c10c2e6d2fde66902f923f86d7e59e0f` | 0 |
| acvm-repo/brillig_vm/src/memory.rs | 25528 | `32afa4bba75b2ea3d96eaafc594fba8b37d86cf396dc0b697b8763625ee56be9` | 0 |
| acvm-repo/msgpack_tagged/Cargo.toml | 635 | `f58e2ef95e038a0bc610ae4b35a4a453859a9d09f56ab2d08aa14c223608d439` | 0 |
| acvm-repo/msgpack_tagged/src/containers.rs | 7221 | `aeb1dec64b5f1c838e86a75c078f70fc58e0c37d6026aa28abf18ceb0abb5a7f` | 0 |
| acvm-repo/msgpack_tagged/src/deserializer.rs | 55294 | `93b0e93d0210e07812140a02801c3cd0ae1ef1d4bb6ca34f236a9b79726a0837` | 0 |
| acvm-repo/msgpack_tagged/src/lib.rs | 7623 | `f929a880469a1985d4c879e960dd5ec2a7c852011a34a7d2ca919a3cf1e66890` | 0 |
| acvm-repo/msgpack_tagged/src/primitives.rs | 3865 | `71531df8164b91eb5cb4848b9aa06eba3dffb839feed31091714dcb30396dcd5` | 0 |
| acvm-repo/msgpack_tagged/src/registry.rs | 22894 | `363d9a26cebc1aa29622936a8b8666fcc4d5b61b0166d08d5dcf77cf0c7d5d4e` | 0 |
| acvm-repo/msgpack_tagged/src/serializer.rs | 51946 | `9d11fa7f92d243ae656e4d4993a69a682a7a82f6d8965bd968d488b99d102207` | 0 |
| acvm-repo/msgpack_tagged_derive/Cargo.toml | 495 | `33b4da18b598a944d9d473fd8bbbe904aeb2fa268fff683aa77eb9da5309d0d7` | 0 |
| acvm-repo/msgpack_tagged_derive/src/lib.rs | 66105 | `b700aab9a6271cd344a2b448f197aea2e1cbe9468f5a226891278400aa6485fa` | 0 |
| compiler/fm/Cargo.toml | 433 | `bede7b45af6381b06bd54bd35ff8e5d48f931c21558c74950edd6381d2b80fd1` | 0 |
| compiler/fm/src/file_map.rs | 4180 | `876d07a5cd7dfa82a46a178c328a14f27e0c03b3bfe9f374e27a299ae6e1d715` | 0 |
| compiler/fm/src/lib.rs | 10502 | `0058ba8f3ace65b32e4ca8635b0cca48aad91c83efbc7af078436260cbe99090` | 0 |
| compiler/fm/src/simple_files.rs | 2393 | `b1b3454c86c6fdbe48416636f0a73a22b8c36cefaa96370d0716202991b3c076` | 0 |
| compiler/noirc_arena/Cargo.toml | 186 | `790e35e3b1cd8cd5faa5fa7ce0354e9624e9fc9f689f3a0fe96d6c9be4110858` | 0 |
| compiler/noirc_arena/src/lib.rs | 1842 | `ce6baff2da1f4800d33e85a2abab79dbaf1dd607efdcceabf7edf4bd8a7d136c` | 0 |
| compiler/noirc_driver/Cargo.toml | 1206 | `d16759e4dc9ffec1275d60d5b7ade7c2cfaa2e76ff31fa51869fd4e6f697a75e` | 0 |
| compiler/noirc_driver/build.rs | 921 | `34dd493a8baac7c97b9c68f4adc61f6898e2aff92051ec4ae6e2038c812a841d` | 0 |
| compiler/noirc_driver/src/abi_gen.rs | 11077 | `23d60bd0d32be63ccb5539295db19232e95eb28040f1752bd53c75cfb3814421` | 0 |
| compiler/noirc_driver/src/crate_graph.rs | 2715 | `8beaba019d035bcdd1230c916d556ee4f22b8392d59a6faf66c1b3b65f4aa19c` | 0 |
| compiler/noirc_driver/src/file_manager/mod.rs | 1898 | `2d702e7cc83a1a398a50760d30e1bae861ca9d28b515cc9277f695eb29be053c` | 0 |
| compiler/noirc_driver/src/file_manager/stdlib.rs | 1804 | `2b92d32c8af25ec1e44f8dcacbfc42dc329ff2112912e7026d3966b43716ba28` | 0 |
| compiler/noirc_driver/src/lib.rs | 48240 | `f2d00077b285ad8c274d55fbb1104c276fd06123455b4acc9771752990a0bf89` | 0 |
| compiler/noirc_errors/Cargo.toml | 463 | `79d83f8a7d5ee046e5ae36eaeaf1fb00b5fcafb74d7d066d2f665b0caa9b03cd` | 0 |
| compiler/noirc_errors/src/call_stack.rs | 6097 | `68a3f42ea859043c9a425c7e3141f52a03e59645cb3c0b9079ebc63e995bde58` | 0 |
| compiler/noirc_errors/src/function_locations.rs | 1397 | `4911270da70368c78924843de047ebeff2f2b79a5b1a6e0fca33cd5a0c7a1344` | 0 |
| compiler/noirc_errors/src/lib.rs | 1994 | `2ad6e3b5c7006d65904d3074eed71e986f7c2daeef2400abe186c67a1f2c71ca` | 0 |
| compiler/noirc_errors/src/position.rs | 2923 | `ddfc458cb433cadc590a5124a9504f803d3c9984fbf305c1a61fc9c7197cb393` | 0 |
| compiler/noirc_errors/src/reporter.rs | 14937 | `624826dc1697db484156b2e0755395f218182453e27bf3afe6b795cecdec3325` | 0 |
| compiler/noirc_evaluator/Cargo.toml | 1417 | `880b577f2a8e4c38d485876c789984b8a97c57e4817e881bd1b68fd08c58a48a` | 0 |
| compiler/noirc_evaluator/src/acir/acir_context/black_box.rs | 15877 | `83ff632268c7d28fb11e6b201943881d44d7407c0eee459ee7c7394baea4c51f` | 0 |
| compiler/noirc_evaluator/src/acir/acir_context/brillig_call.rs | 10621 | `f8f2c078dba4b628d505309cd0a2b81cdcb89f319334ad55de62080fbc749541` | 0 |
| compiler/noirc_evaluator/src/acir/acir_context/generated_acir/brillig_directive.rs | 11544 | `db6914a307d03f3b42cee5cd60574d87396a8aa8baad2a65324f249fde6e15f0` | 0 |
| compiler/noirc_evaluator/src/acir/acir_context/generated_acir/mod.rs | 34411 | `ec5ce42ff5841e4d88ab57b19509094b25f61421ac02ef46c3767e51ef9c1496` | 0 |
| compiler/noirc_evaluator/src/acir/acir_context/mod.rs | 75060 | `3c4584e503b33b61aa3ae0fdba6348fe940c638a1db22ab06ec34ada594f2019` | 0 |
| compiler/noirc_evaluator/src/acir/arrays.rs | 87850 | `e6473fbf44121ca21e953a13ef34a8e8b4d6ad9cd81d79689498e69e1f0eaf90` | 0 |
| compiler/noirc_evaluator/src/acir/call/intrinsics/mod.rs | 7629 | `1e26a7079b9678c64984080a0fdb7dc96c457b3ac25c0ab7328004b88538cb08` | 0 |
| compiler/noirc_evaluator/src/acir/call/intrinsics/vector_ops.rs | 53780 | `18d96cc2acd9f53e5175521b1d9b45c3c5fcb9a6d95d5a33c84b33c9a049260e` | 0 |
| compiler/noirc_evaluator/src/acir/call/mod.rs | 14102 | `ac6fe91291c896692d1a396a082542412407e678cb35dd37d3596e9e90629290` | 0 |
| compiler/noirc_evaluator/src/acir/mod.rs | 51502 | `26184c7bda385a5be1b196b6561ca8d5e7b79f34cd2711326a94b120f855d749` | 0 |
| compiler/noirc_evaluator/src/acir/shared_context.rs | 14068 | `dcd76002f7563343595bad8e18b0b0468710ae6babda2a775585c325e342bc06` | 0 |
| compiler/noirc_evaluator/src/acir/side_effects.rs | 15032 | `39e5ee434da822474d6f5fa6022ffc3c245fc66cccf2979d5c38313c2bf71c0b` | 0 |
| compiler/noirc_evaluator/src/acir/ssa.rs | 5326 | `6d3771aa0d92e3bc6d0fdc5519411dd8778d77256eabd6abd7db47d9a08c4f45` | 0 |
| compiler/noirc_evaluator/src/acir/types.rs | 9256 | `8dc0361dfbf651e6fa407d08beef32e86f06a0553b6aa2b7e188c00879341391` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_check.rs | 55441 | `0f7421cd8bbb12cea6f367533e474f9a87724cb293ae489b92dc2bfc4b9ae7be` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/brillig_block.rs | 61343 | `21c169530ad75524253ec725b7b1307df9cf0df2744d7899596e3079d1fd25a8` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/brillig_block_variables.rs | 10896 | `0ae0b7171012bfc0c0a330fecd927b0a20217b0c8c3ade9cb91f5e911f28b1e8` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/brillig_call/brillig_black_box.rs | 11923 | `b56c91a9efc34f9caedace3d20a41bc507d9c05dde2dc0235ed8be4ed02e8202` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/brillig_call/brillig_vector_ops.rs | 30588 | `71d62689ccc0370d2a0f25cb5d43f761ae3ac37cb902c8b8579facde9811d2ae` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/brillig_call/code_gen_call.rs | 20043 | `8256304d5e764780a0b39dbf81d52079ef6092d304f9cc6184154c610feaa35f` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/brillig_call/mod.rs | 17993 | `c49bf0cc1a14455987c0696272eace801b8be5ffeb62e97dd010d49ea082a0cb` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/brillig_fn.rs | 7784 | `78220f2572078d2d26451248209539f2d51b7990f423cc6fb79a620d2cd51d6f` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/brillig_globals.rs | 29961 | `c8efd0baec0d321813e05ec23a9a5970fe387d023641d1fc9655564287e85ed5` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/brillig_instructions/brillig_binary.rs | 15999 | `8f4a8d09c470b0cabb5d82b9ff00cf8ad0484bb0ccdef89de044722053ffbfc1` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/brillig_instructions/brillig_memory.rs | 21415 | `9c448306439fce2855d24fe895cb0544f64bb6b31914290f4b74fa1b5a64951e` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/brillig_instructions/mod.rs | 62 | `1a45d07926c1009d089bdcb66b0cd8fdf12327eb9e71e389c57b7eeafb9af82a` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/coalescing.rs | 27514 | `3c5d23f13d22851295ded118a1fbe0b96f8af470dadb60203ae45d0cf7a1fe89` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/constant_allocation.rs | 7639 | `965f9aa894a6f002ebdb81850f59953f3fd997dae2ea09ada83784d34820e80f` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/live_intervals.rs | 38360 | `26e333d9c03262629ba5dfac09c5b9a4c172d1065a56dbca4e3d9004265c6884` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/spill_manager.rs | 41393 | `2c60097a0da5e3bac337822b555249db5f3d4391359a82662f9fe526ecdc0730` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen/variable_liveness.rs | 64655 | `88aa2dfec7ec904545151d547d932e16aff4ef67c8715f1032a36e594998ad98` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_gen.rs | 12125 | `f55238c4213926b914d8b0b9c9095de91f50d08a6ececf65ff1ec01e00921e9d` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/artifact.rs | 19462 | `a511bae62e5952060202ff8bf1b686e579e9319aa2f30da4599b9685f4a9a944` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/brillig_variable.rs | 8172 | `230901dac16f39edb7f4f28b0e774fbca1e5e4a21d212768ab165287eec28428` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/codegen_binary.rs | 7579 | `8720fb1ab41cc31dfc8613bc0916e1bd41429d7b44ad6d67a163603141f26d8c` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/codegen_calls.rs | 7091 | `b0284c8ada2e85000491735d3f4bc9c0e96b0c593a27f79a622245139ff2c5e6` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/codegen_control_flow.rs | 16524 | `aec2fec94fe9780e7a11b65f6c38400130d661f5a524416d374ba1cceeb75a5b` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/codegen_intrinsic.rs | 4183 | `3a564717b35918fad3818a66ecf5372b723dd8ac2e7538fa50b8875bc40d2bcf` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/codegen_memory.rs | 29933 | `0d310806b8a94bea3d0025faede271f74e3718dcd0a05714c921017226ecffb0` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/codegen_stack.rs | 16633 | `e52bf2cccb320c46ed924da06322402b444af99150058142b87db6f6b2d773da` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/count_array_copies.rs | 19583 | `2ef53e5e6f1933bb5708c20ea0ef0f591832a4fcaed8ba203b3fd63009efbd2f` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/debug_show.rs | 17136 | `7c453e247d94a0d24d8f804ffa8204ea7d1d0416dd449ec34a2f2deb890867d6` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/entry_point.rs | 23640 | `378b8590e33bfc39acb72044843e2a5ea433f5e362e0c87bb4010868ba83ffaf` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/instructions.rs | 20546 | `d939eb13ca46e117a7c9a6fd9c1c1375384723f4b5e4f27f21d749146b645ae4` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/procedures/array_copy.rs | 3848 | `60955dfe466efe878dd818d75f8f9c9e80fd715c3bce20741a49f787e3ce2d75` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/procedures/array_reverse.rs | 1269 | `4cec50fd7b7ade87aeb62a6b1a984beac87ff9c3d9cf082095cc7c78006b6d97` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/procedures/check_max_stack_depth.rs | 1714 | `1f549b15f64f89f40e4c1f9cef4d39537e9aecf82e8f51ac62483d0f258486e1` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/procedures/error_with_string.rs | 1549 | `f560bb324e26fbf5c7d2756f0651ab416400cbb0a1d4d19d20a677f02deb1136` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/procedures/mem_copy.rs | 1702 | `33170bf464e31373edcdac34389e2d4ea142b45db4d39c291858481e86b5a392` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/procedures/mod.rs | 12995 | `f260e781e214f96b6df5198af3d768566d867364746880910a11e8f11fcac62d` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/procedures/prepare_vector_insert.rs | 6103 | `7be71e94593f3e575db27dd088abb8c86d74d970bfe5ac5b6ceca4d2b6a5369e` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/procedures/prepare_vector_push.rs | 11608 | `27ec0c954706a402329cb11401007c5c011f18f5287522fb7ff343234f791bd8` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/procedures/vector_copy.rs | 3578 | `83899e5307f9b2d8d545da630ac7c52af48e6a0774771c7ddbcf4ca6922f294b` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/procedures/vector_pop_back.rs | 5004 | `fe6e7c60245139acf135c23041f4250f624427277bc2bd857941bd42cb74f76e` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/procedures/vector_pop_front.rs | 5268 | `fc2c11add0766d10f2ea1d11d1310dcab5f636cfc5ad2697452949c638fb1be5` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/procedures/vector_remove.rs | 6031 | `de0bf92acb04a3b51e769861bf6529682cd625f1add91fa3d4137bf7f61756dd` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir/registers.rs | 35431 | `1e2bceeb2b1e7eccf24f22d9a638beabbd42dd9049a10d09b808d3c55b09d220` | 0 |
| compiler/noirc_evaluator/src/brillig/brillig_ir.rs | 49453 | `6631a378d5394c084a1dd2e64adb9784b739442aa5793824dc173cbd5ce2c970` | 0 |
| compiler/noirc_evaluator/src/brillig/mod.rs | 34894 | `2831bbce63fe8f2903db6bd1eaa222b9c1d35a023aed46762a005219ade6342c` | 0 |
| compiler/noirc_evaluator/src/errors.rs | 12911 | `a37bc0802a017f3e6b4242136d5e5d1a0b075b4de69cc6247d682f47b390a1ad` | 0 |
| compiler/noirc_evaluator/src/lib.rs | 1711 | `2ff0ccd5d68c6ffb1c3375153ee17f73eaa86e318eca4335aabb80ec244959a9` | 0 |
| compiler/noirc_evaluator/src/ssa/artifact.rs | 1667 | `fd8f09a5796828ccb2d1aeee323013b9a0cb0d21cb4f21ba87e3577f8f4e7f0c` | 0 |
| compiler/noirc_evaluator/src/ssa/builder.rs | 10815 | `9f849b8ce3d8ac208b43f622aae2c1523f51be82b08cc02304d2d086b960079d` | 0 |
| compiler/noirc_evaluator/src/ssa/checks/check_for_missing_brillig_constraints/array_output_cases.rs | 30685 | `cded3caf48bf88fe0a1ec4da9cae8dbabdcecba5aa62f9423fc929fa53294e50` | 0 |
| compiler/noirc_evaluator/src/ssa/checks/check_for_missing_brillig_constraints.rs | 96618 | `d794781cb38619c0a77d7ac4f29addc56c2f6999f6568af3575f67f76c8c3eae` | 0 |
| compiler/noirc_evaluator/src/ssa/checks/check_for_underconstrained_values.rs | 14849 | `dbc3dbdf905fca07d4b6ac5ff9ff2caa7b2df963a058802794ee007378a3b5f0` | 0 |
| compiler/noirc_evaluator/src/ssa/checks/check_runtime_only_intrinsics.rs | 5241 | `b1bda5c6e6866c401fce21c9809daebd170bd9222755787b07ff9ec8db0ea22f` | 0 |
| compiler/noirc_evaluator/src/ssa/checks/mod.rs | 806 | `0f895dfb33afabddb710f9012d56505e06e766f26c34d29e05bc6c12d8d98bef` | 0 |
| compiler/noirc_evaluator/src/ssa/function_builder/data_bus.rs | 12018 | `542d4f7d3b3f33650de7fb0e1cc22ac9fd205a6cc928891fe4da5a7bceeb2410` | 0 |
| compiler/noirc_evaluator/src/ssa/function_builder/mod.rs | 26894 | `9f90bec81c5adaf1f037426067db7c2a7457abae6cf5e252f9a4acc7821f5a36` | 0 |
| compiler/noirc_evaluator/src/ssa/interpreter/errors.rs | 11084 | `e381ad52a319af1d219e3c9748ad178439c11342e263abed62d6ace4140bafbd` | 0 |
| compiler/noirc_evaluator/src/ssa/interpreter/intrinsics.rs | 40407 | `c3c8ba6df6d291c15af76c56614b161da3e3f1f3b37c3ebdb0536ea5645992a5` | 0 |
| compiler/noirc_evaluator/src/ssa/interpreter/mod.rs | 77150 | `60264e2981aae3880e278bb9a1c6d672d98f692d7e4f8c6671df3bcab8434e71` | 0 |
| compiler/noirc_evaluator/src/ssa/interpreter/shared_cell.rs | 1817 | `9a8db24ddda22b36946b80aa0b097b262b7a691f15bc49def07b76fe4f0f6e37` | 0 |
| compiler/noirc_evaluator/src/ssa/interpreter/value.rs | 26561 | `b14b996dad471bb7a12aca2112bafbc2cbf36cad107ebbcbde2c82cdb4eb8931` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/basic_block.rs | 6535 | `b80785c1078f4d39718ce6a5d26f6916da0880d328f6c2faf6055fb51c6a58d0` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/call_graph.rs | 36351 | `d5ec1c56725afc5de859e17d3598086359c8b33d68e87cc443a05a869c9212c2` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/cfg.rs | 20713 | `7bbcf426a912f01f177b560e810a9efe63a4351d66ab58b86396f84ed9d19d59` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/dfg/simplify/binary.rs | 19889 | `3f673bf9714c8bbe36f879644ee67e610e5c223f208744ae2e85d7f6bbd446c1` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/dfg/simplify/call/blackbox.rs | 31132 | `f9b444b9d40b6bf9c26f96e8f1d5d79cf3b073ceb9f240229580e596bd6b2b19` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/dfg/simplify/call.rs | 64765 | `95ec59e76a2364477719e99bba8926bb1b4b978d040b06ffbbf34ed6dd4e902b` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/dfg/simplify/cast.rs | 7008 | `60f7fd4634d95329836a0f405152afa2eb769a225a24e9cb78bffa192eaca99a` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/dfg/simplify/constrain.rs | 24593 | `eca912631a1a684d95b38e38d3fd84a9692808c7e05245ebafb8ccdc37c98899` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/dfg/simplify/value_merger.rs | 13924 | `bde7a7158e29c80ecd7e50f0dad77c5a42a50169c86b145d90984741a2301a69` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/dfg/simplify.rs | 51054 | `bfd90e68722a5f3d30c2bc0c82c445c262d75c13304724f1b3c84a6d03beb69f` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/dfg/vector_capacity.rs | 10927 | `f7d41d3670999df18c4141a57966c7131639bf60d20eefd79caef7675eb2e6e7` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/dfg.rs | 56994 | `5db2d5eda081ec46ffcdf9bc1310caf49d18611d586e8091cba143a18e6a757a` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/dom.rs | 62517 | `87eefaa7dfa8dee4171167457f088a9c7eb506a3e578e0325a205407f57531c8` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/function.rs | 14789 | `47a88ea196db74163307e8ec493c4038047d86464be2dd38fe952d6708720199` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/function_inserter.rs | 9178 | `d370d11a82e644c45cc6031dd2cbd9683d8b3b5f7b4341dd8b0033cc873f1ef2` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/instruction/binary.rs | 23350 | `76270f57b888e9711b706d4b34efc1ea68b5480f36458026e16b1536a24cacc2` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/instruction.rs | 60873 | `82d2e6c1cfc7f01d725a9c170ff9bf8f77fb50e35602e54b1233b4aba2cc1775` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/integer.rs | 4897 | `5f631a1dfd43d6768643cb285b59da21785764b6b443afda849c0231dfd380ea` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/map.rs | 8344 | `a25a3b5641eaa88f78a7c41ca3372c8752196fb317bbb78ea49bc45e1f6eff67` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/mod.rs | 390 | `f6a780759a1e07de81f058fe3e264cf0ebfa1c8907d9c4dd5d46893fb9bdab35` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/post_order.rs | 41647 | `25afd9d8e04efebcd540af104c3afe51e3fa6e520e48e1ec6a913050b70e9b55` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/printer.rs | 18629 | `67cea53c8ad3478ee7f7f88f28caafd9e32e5a66e635dd68725e1af6ba95da55` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/target_cost.rs | 11351 | `972ae2bd491462ab9a2d99baacf23d460ab1f4192e6b17fbf8532381793be438` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/types.rs | 20165 | `5715b0081e6646b7cd3a2f527ef363754c964dcfbb9d2b80cf73ee41e043bb3b` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/union_find.rs | 4206 | `bc360a79fd493c7b490b4cf61f87de5893dcfe149cbccd3d15744d3cc3998ce7` | 0 |
| compiler/noirc_evaluator/src/ssa/ir/value.rs | 5450 | `bf4a6576afa01326231220a97e5a79829fd121f615d517f94af411a0b854ceea` | 0 |
| compiler/noirc_evaluator/src/ssa/mod.rs | 37426 | `b461fabc9e3fcb7fedd4b3c203d396f056cd0ecda8f3a7dedd5510fce065205d` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/alias_analysis.rs | 155498 | `b338dc7de51be564e44327910ee686678e251b593a70e6e78a5597a8d9309030` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/array_get/array_view.rs | 5818 | `de3f2f8278ed04de5f58d2710fff8fa67ebcb9e1224420607782eed05c5cc7e2` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/array_get.rs | 32990 | `ca5d1774ac845a489f0b963c788b5f57674c1d226abd608390d8593b76455791` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/array_initialization.rs | 23315 | `fab9940f5b830adfe2c88770a71359dac58c1baa42c6b557a5d53ef932775da9` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/array_set.rs | 17982 | `eac2db74848685b3b2e486c965593d96ac1b8a2d24327e1e46a6e73fecc359a5` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/array_set_window_optimization.rs | 43046 | `34fbdab4a0889aa49efd20d415f5aab453ba86e4b53cf21d98c9b1f49b28541b` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/as_vector_length.rs | 4082 | `9af01100c8834fd51c5d80106d2992ee1c6db9f7c1830ffe40fe8f767a8d0049` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/basic_conditional.rs | 32291 | `2ea1c4bf6b14f53d380d9511b8d0a74725ae3f190e46251893b46d085a592f18` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/black_box_bypass.rs | 9503 | `92c322d699b9c782849ea99fced17cf92c3fc5eb071fc1406f1039de19a7635b` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/brillig_array_get_and_set.rs | 12858 | `bebafcb8fa52848c232b4220745a70f4403f65bcb8bb9bfd966aa8ea6a392c4a` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/brillig_entry_points.rs | 39319 | `2f72663e9289bf5696aee55e0d04e375a117079f917c9274c4a33f92b9edf732` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/brillig_function_specialization.rs | 27699 | `3bcb5d4e1b13be80674ec4448d19f4881da16031f718bd0962042984ade09af7` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/check_u128_mul_overflow.rs | 13435 | `da24a9785b6111f9a0ffff95c65ad20a796fc1dfde2406dd9b26c7b92dde6b77` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/checked_to_unchecked.rs | 13476 | `6a1fe7d85523c3c23662d5815db8a9ac55529d77dfbd737e6f00cf4131e7e2c8` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/checks.rs | 10654 | `099de2aecfc715a8f711d282ffbb05453e4b4fd2f4875acec11d56d133c32751` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/constant_folding/interpret.rs | 6724 | `d85341434d4561434c29ac5f7c6d6a371b4e0f1b0434bd899ac2b66eaf2930aa` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/constant_folding/mod.rs | 162549 | `74a8adb4975b9bffe43cc327afb5ffc2d7e3e4ed5b14742fea9b57fcc59f520a` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/constant_folding/result_cache.rs | 14063 | `ce9933dc9ff5d1dee5a66ebf03c64a4d468f4938514c1f273cd21618faad2be7` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/constant_folding/simplification_cache.rs | 4130 | `8075479745248dffffc7be7ac9d6b797c99054926b2d90b5a9bdb9214578019e` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/defunctionalize.rs | 96306 | `5ec909401ec1b2c0fd75efee561d6f27f529fac35ba11f6a6a4be72ecfa36547` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/die/array_oob_checks.rs | 19497 | `0ce8af11b3baadb8ce2328cfa5718cc52ff195e5090a82c8a152873f3b0035cb` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/die/prune_dead_parameters.rs | 26020 | `4d05df645fb45b51271dad76df2767456178f3dd9bcc46981577c19c0e6bac9e` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/die.rs | 51230 | `4ddbefbabc71311cb709cd62bb9dfa33e93ff0e01758d1ddb7d42e16144da0c4` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/evaluate_static_assert_and_assert_constant.rs | 22934 | `c4764723e09d38ecacdf42fa960f924c9e0c1d5ec2ec9622698ffac0031008a0` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/expand_signed_checks.rs | 27409 | `0ccdf7b6d19f0168c234ed39ca32ae79a5c42bf6605fd6718f5a31e0d2c2132f` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/expand_signed_math.rs | 21336 | `4750eccfde487b2688aa9269af28f0c83eb43be62542352b3c0b6364f642011d` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/flatten_cfg/branch_analysis.rs | 24161 | `51f02fa68782fcdccd725aa312bb0bc2676dd3f965bc16b85b35268c84c1864d` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/flatten_cfg.rs | 167555 | `f14228591e76798231f1a7ec2daf73d6f7ba7a87329eb6760062b75be43609f5` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/hint.rs | 2705 | `f4b82e1f638bf7bd373d0ff45117d917c56389b72891b83235e677f67b257e84` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/inline_simple_functions.rs | 12071 | `dcb952b6856a048736012fa58e9af50bfb7ab20211d85991debd2f7a65876823` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/inlining/inline_info.rs | 29996 | `892508e76ac04b96e7d010be443827b6d82a2d29896f43fecd86f8d28c6b148d` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/inlining.rs | 67160 | `ef7673a31acb9b5f2ccb0372edb2ebd52ed98926e4b116558fd398abd0c213af` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/load_store_forwarding.rs | 84983 | `f41895ed3e6b9b749b5d4f01d0ffd25bd39a76d79e81d8e3be11fbcc1a485010` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/loop_invariant/simplify.rs | 17997 | `8c5e308245a8aac063697663a49b729aa361ef3e59cfba875f9f10c61c3dbdf6` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/loop_invariant.rs | 192119 | `320e937e41ffedeef30593d5087b282d05c821c32280bca4570e3a02ff49d379` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/lower_refs_at_acir_brillig_boundary.rs | 16684 | `0004f350a8a3797693c3ee8fa525f164d05b2b6bf720049a7f98231d0a2d1e35` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/make_constrain_not_equal.rs | 6314 | `5704b64deca79cc8ea1619b8ba2c09a0b3cd48abad7953d8831bcd57cec5a262` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/mem2reg.rs | 63574 | `fcc02cff1ec0db5724a0bb54c01fd511c2ca435c61dd1601c6e2bf880866816e` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/mod.rs | 6250 | `14843214771cefa0bd69caa5b356c39055379fe4b9938d3b88c36b8aa316211d` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/mutable_array_set.rs | 31922 | `c5b6def3946833985f7367cd1cdfe120c2ff9e3db05b83d39e27ac56c0d50f16` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/normalize_value_ids.rs | 10935 | `c412749a96fcd98b9a32bb2e8c10225fe505e6e55eb9b11140ed6c178b8889fd` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/preprocess_fns.rs | 5333 | `8efeab7f61561b5832298893ae0571b46cd5f944c1675bb2f49bbbf340848e65` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/pure.rs | 68230 | `71849f6f19c9212391b18f93cdd53063f4d221f9ebd6258e89ec178ebd6b6381` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/remove_bit_shifts.rs | 47931 | `c6101c1d24e99e4a7bcebd8787ee0c782c4398a324aa897f8b746a7d922b8951` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/remove_enable_side_effects.rs | 24061 | `b205e84c41c32bd9b203ae1adb56fbac03b1b9d0711545d6fa98bd4d5129ab44` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/remove_if_else.rs | 51599 | `aa8e52f06abfc61e9876823f0b28b7eec2947726b20840ef8c770767a05b9475` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/remove_redundant_params.rs | 22601 | `c414c807c05b649dfac9705571d49edf2e514aed3ad61e397104210b9b4ec82e` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/remove_truncate_after_range_check.rs | 5704 | `cd4cdba6cc0eda94b92ab8bab8f81aaae91a2820620edf97c26312e60048b1ef` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/remove_unreachable_functions.rs | 8954 | `741ca495c21528e98dd3ac03d313bec4a0f293cc36e4c21872fbcb024dfad2d5` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/remove_unreachable_instructions.rs | 73785 | `5633bf3f19eb126732bc31236450fb964fda49e3d5bc28bc6acd83968c63df9a` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/remove_unused_instructions.rs | 961 | `7bcf4f429047370d10a5966f1caf4034b6b1ca388421f0df9e293be2eb6a97d6` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/simple_optimization.rs | 12404 | `d29507c8a13205e5021b775f927bbd5d483d35ba1a61bacbf8913ceca0f45b43` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/simplify_cfg.rs | 51196 | `b21cf5fd1ddb9e064c2474cdfea357b98faf2d6891c1ac047a79e43ad91f0f95` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/trivial_conditional.rs | 15286 | `b8d6704159b68724603de269ceb700718bcd426cbfb10cf41782043944461740` | 0 |
| compiler/noirc_evaluator/src/ssa/opt/unrolling.rs | 226579 | `1c747b562cb4acbb61ef34b54c80c7cbd420692a843a227c443d9b66028e0f09` | 0 |
| compiler/noirc_evaluator/src/ssa/parser/ast.rs | 5004 | `589f1dd9631f9452307e839edf5c0f9bda19bb841d40036ec42d84c5a8b5528b` | 0 |
| compiler/noirc_evaluator/src/ssa/parser/into_ssa.rs | 31388 | `41c2bf7938c57face7ebcab246c651ac4056a7139117832335681ddf74325c80` | 0 |
| compiler/noirc_evaluator/src/ssa/parser/lexer.rs | 11949 | `7ec0a93036cc5afc9ceb8b2a6b24fcb54e8a9c000e9f99d0a8472c19c4d31d47` | 0 |
| compiler/noirc_evaluator/src/ssa/parser/mod.rs | 49352 | `90be7cc8d5a57deadc2562058530bad297fc9a1bce48ea580a7c6cf23c314949` | 0 |
| compiler/noirc_evaluator/src/ssa/parser/token.rs | 10260 | `d0edf9b2969e8e14c1d58094776614abdba9117dbab8a5a43e61e40538094597` | 0 |
| compiler/noirc_evaluator/src/ssa/ssa_gen/context.rs | 53950 | `85fb717fd0f4f1b4751a8c514c9b0efdaf61df8b88fc655a8b309db439aadda5` | 0 |
| compiler/noirc_evaluator/src/ssa/ssa_gen/mod.rs | 74863 | `1742eb8f7699b3f04178c95464babd9c3cba55309769abf27aa7f371040aac00` | 0 |
| compiler/noirc_evaluator/src/ssa/ssa_gen/program.rs | 9413 | `6105f02693d9b649c6a8f44f5bdc96164601487b3c433b9563a2b86dcc5b5ce3` | 0 |
| compiler/noirc_evaluator/src/ssa/ssa_gen/value.rs | 6369 | `23d2c84cae25ae9089d11c1c693198a82e2e04c839ee544a77de3ba3a478e792` | 0 |
| compiler/noirc_evaluator/src/ssa/validation/dynamic_array_indices.rs | 13296 | `e78970dc13cd2cdb74829163425b62f636463ecd0f18569bd885a890692cdd54` | 0 |
| compiler/noirc_evaluator/src/ssa/validation/flatten_post_check.rs | 32578 | `0954477f8223d594570174bc83f66b5bc377887796addeab1242753788ed731c` | 0 |
| compiler/noirc_evaluator/src/ssa/validation/mod.rs | 139656 | `0c20bfbf2c736812a171e95f50bb9a96b66a1495161eba4f26664b8b834bf792` | 0 |
| compiler/noirc_evaluator/src/ssa/validation/rc_invariant/array_set.rs | 130100 | `b7537a4c7a6dc38174b06846a68ad951bb8e117020c5d12da5ceb113928ddf75` | 0 |
| compiler/noirc_evaluator/src/ssa/validation/rc_invariant/call.rs | 47362 | `a517067d6144c0fbfc573cfac0ef5fb2a6afe8336d848570a6b42e8807455d00` | 0 |
| compiler/noirc_evaluator/src/ssa/validation/rc_invariant/mod.rs | 109376 | `a6fb139e68906ca9950d3d2774cb825825da55a01adbad1c7509022225d9ca5f` | 0 |
| compiler/noirc_evaluator/src/ssa/visit_once_deque.rs | 2374 | `07fca5cf1437e209d9bb022375c6d268ed077bc7c28f55becf744bb246b01b14` | 0 |
| compiler/noirc_evaluator/src/ssa/visit_once_priority_queue.rs | 2321 | `5cb0cddddb499263d30fe7b604842fb8de75e8233a74c72e0ce51d3907494ade` | 0 |
| compiler/noirc_frontend/Cargo.toml | 1221 | `11c166aa17b8df4d752aaf08eb1ccaaa06912cc3f7eb0c9c323a0c324758d3a1` | 0 |
| compiler/noirc_frontend/src/ast/docs.rs | 512 | `501ef635b3863399a20176787fe9c523a3422b932e40696ad95cc4133d92d747` | 0 |
| compiler/noirc_frontend/src/ast/enumeration.rs | 1921 | `13d0ddf6865cb8bee2d2a1332813c8f2b8159f19c33b11dc973e55e81baddf27` | 0 |
| compiler/noirc_frontend/src/ast/expression.rs | 30563 | `58b9b31e90d4c582f0e7a03e68a1ed7e0bcd2aa89eecc601f601e48249d023e4` | 0 |
| compiler/noirc_frontend/src/ast/function.rs | 4564 | `584869864b751f2382e5100f389d2975db6e29d495244598bbb7e4fd45f8273d` | 0 |
| compiler/noirc_frontend/src/ast/mod.rs | 18954 | `f6e999debbe9d25c00e2b2a176811466b6f2963925a671828b9f0b275be10770` | 0 |
| compiler/noirc_frontend/src/ast/statement.rs | 37258 | `397b92ceab12483b8c5c2d85e20825374957e7f96688f542fbfd80579668506d` | 0 |
| compiler/noirc_frontend/src/ast/structure.rs | 1345 | `f6d8e698f6edb4cc078b458f66db0653a1367aa377f5963c8a830590afc13d75` | 0 |
| compiler/noirc_frontend/src/ast/traits.rs | 12763 | `cb38b2fa56c1e7230f7c42168b675de0c62e259020d86aee6292dff6fca35892` | 0 |
| compiler/noirc_frontend/src/ast/type_alias.rs | 868 | `33ef0086b308953eddcae03081f6cc48488e7522deb39d2383205762d0ea5516` | 0 |
| compiler/noirc_frontend/src/ast/visitor.rs | 52403 | `ccd3fb591afa041e7be39c23df78776bc5aa049a7021ec9ffc709a927581f4e3` | 0 |
| compiler/noirc_frontend/src/debug/mod.rs | 30174 | `59c3e62ffdaab56ce0502322067c872a448706b818a07cfcbe4d331b0f3573da` | 0 |
| compiler/noirc_frontend/src/elaborator/comptime.rs | 42730 | `f7bf57cd9dd5a9de58cf588288a0a2cdad73e6dd3348905ac64355b678e687d5` | 0 |
| compiler/noirc_frontend/src/elaborator/deferred.rs | 6986 | `811cc04439dba6c37b57e4e8325980d83a70392c7c90ee4e2151b18fafc7aa0a` | 0 |
| compiler/noirc_frontend/src/elaborator/enums.rs | 71981 | `9c96688067e0a60095bc87fbe33457a4e1a8dee6064e7e286e5a9a1fb91ff458` | 0 |
| compiler/noirc_frontend/src/elaborator/expressions.rs | 102863 | `d6641ee78378768f6b569020d1864da1bce562cdb544fff3aa7191bc2b97433a` | 0 |
| compiler/noirc_frontend/src/elaborator/function.rs | 38176 | `677f4399bbddae28f55d394cf147322896f7959ec4145c463e55a1169ce25c23` | 0 |
| compiler/noirc_frontend/src/elaborator/function_context.rs | 25795 | `6343bf1a412bb3a73167952fb83dabae2f2f51b2024c1efdf97d842dc722e582` | 0 |
| compiler/noirc_frontend/src/elaborator/generics.rs | 13096 | `aa4635149f31100746b3f8fc0d87f393e47053e15e1a95ab52980b83db77f677` | 0 |
| compiler/noirc_frontend/src/elaborator/globals.rs | 10275 | `5e228f2e420100dc978af48bf6ae48248502983d60adc30309be29ea17ca84fc` | 0 |
| compiler/noirc_frontend/src/elaborator/impls.rs | 11881 | `36ab8845f28e8bcf4d2e99fc380900fbc88a234be0b4fbd4d3214c158e494924` | 0 |
| compiler/noirc_frontend/src/elaborator/item_context/body_context.rs | 6942 | `34127ec8863b087668751038dbaf58a525e3b9510c72b263b0aeb0ef9779944d` | 0 |
| compiler/noirc_frontend/src/elaborator/item_context/generics_context.rs | 7059 | `d0eecb75568c8552fd11121e17d18877c3e6932803714eafb9c962749712c09a` | 0 |
| compiler/noirc_frontend/src/elaborator/item_context/impl_context.rs | 6681 | `67218f57198489647e42d5d259ccec0ad90837e67757e26a2e11eb8a1a777a66` | 0 |
| compiler/noirc_frontend/src/elaborator/item_context/module_context.rs | 3476 | `2e8427183e59dc2e9419ac2f9c31cd6100fab2f20f9de8f67db8de5fda04a7e8` | 0 |
| compiler/noirc_frontend/src/elaborator/item_context.rs | 5621 | `1e56cf97dd704512086eeb6c674fa6edd299232a9709ded303085222cac84369` | 0 |
| compiler/noirc_frontend/src/elaborator/lints.rs | 26442 | `271c1fd749eba2e0d838a6fb91a03496772871a56f3db9777b0485f758d20997` | 0 |
| compiler/noirc_frontend/src/elaborator/mod.rs | 44925 | `e0d63dffb8fb9bb9f1dffe2abe0d5c56b23c2e679aa0193f3e306de6a37c4c72` | 0 |
| compiler/noirc_frontend/src/elaborator/options.rs | 2263 | `846bf2fe6fc5381fa3c2e99b43b3a24ad09f0b02ba0e86a88242680f4ede087d` | 0 |
| compiler/noirc_frontend/src/elaborator/path_resolution.rs | 60492 | `8d8084e9bce44c702ad02d94b15e15e9ab0a3c40298bc1091e9c039864de296e` | 0 |
| compiler/noirc_frontend/src/elaborator/patterns.rs | 33854 | `76b8be11e76f66563df814cc81fe2c56ad8e3060942a168e363bb5a5e3a60906` | 0 |
| compiler/noirc_frontend/src/elaborator/primitive_types.rs | 18254 | `ca4b361e8a82d08bc3e4545952a0bdc85f2246a86500ddeb704e31e7b6bd1553` | 0 |
| compiler/noirc_frontend/src/elaborator/scope.rs | 18458 | `a310e97cc41fdd866a99ec4ab7fedff735b0a5af6dfd0a636fb58e513f6f781f` | 0 |
| compiler/noirc_frontend/src/elaborator/session.rs | 4837 | `dd0683b42e588d6bace92e403822281c58f8881355cae5863c1cf91627cc27bd` | 0 |
| compiler/noirc_frontend/src/elaborator/statements.rs | 46866 | `2f7ff8b145c9a9b91d51881619757d2b26011596f6bfba9d69562618c014986b` | 0 |
| compiler/noirc_frontend/src/elaborator/structs.rs | 9675 | `b8f7897640c6ed418b14517525313574c0a1a14a11627f41b40c5c38bd50aab7` | 0 |
| compiler/noirc_frontend/src/elaborator/trait_impls.rs | 55278 | `7424637fc955b2a3d50c62319a8fae97fcf2abc2fc4e1ba223798137086d1eee` | 0 |
| compiler/noirc_frontend/src/elaborator/traits.rs | 87721 | `ba57af82dcdd8704dbdc21b2230a0d271ae4ec6e728fc7bc7fc2a158afac6dd2` | 0 |
| compiler/noirc_frontend/src/elaborator/types/similarly_named_types.rs | 5117 | `79a1d95a5c97a02f20f9f9f5fc8343f49b439799a6db175bf980683e3822eecb` | 0 |
| compiler/noirc_frontend/src/elaborator/types.rs | 181841 | `50ee22a78afd7f5b7d992fa05541664ea3e4b69041dda10cb70dfb49658dea2b` | 0 |
| compiler/noirc_frontend/src/elaborator/unquote.rs | 3220 | `d5a648f849658fdcfdb5b3abd7c8fa8a80eacb37e07afa7b906d99a1761a5114` | 0 |
| compiler/noirc_frontend/src/elaborator/variable.rs | 75077 | `49e39698b4bfe0c11e32f63cec1d8e80786318f3aa7774190cdefb587fc8dd29` | 0 |
| compiler/noirc_frontend/src/elaborator/visibility.rs | 11911 | `639e3d7e0c99b181c81157da2e55ab6b366d18af943214a872309eac678e6d93` | 0 |
| compiler/noirc_frontend/src/error_reporting.rs | 7803 | `dcc3dd9cbaa7ea2283713dfe620885df3ee51c9513b90f3a957bf431a3a57cee` | 0 |
| compiler/noirc_frontend/src/graph/mod.rs | 16279 | `c6bcb749246131f4b11820650c0a13f4c56e48ee1072410d1a9e821483832f92` | 0 |
| compiler/noirc_frontend/src/hir/comptime/display.rs | 44833 | `e30b9b71f765e0a1581a640b70f95b6c38de5f1be39d7e2dea9acc970a917503` | 0 |
| compiler/noirc_frontend/src/hir/comptime/errors.rs | 41756 | `a73fe2d185be6f4659e6e2956fa94f8fde03c780e3c1c0bae7d02864efc20b2c` | 0 |
| compiler/noirc_frontend/src/hir/comptime/hir_to_display_ast.rs | 28198 | `0076a0dee952f5dab140a4ffbcefead9e283e4c450e91344ff09284be0ad68ca` | 0 |
| compiler/noirc_frontend/src/hir/comptime/integer.rs | 38724 | `ad8b3482863e9545ead93bef2c3f995e593dfc19bd7b4b277a679d3ed08711d7` | 0 |
| compiler/noirc_frontend/src/hir/comptime/interpreter/builtin/builtin_helpers.rs | 37162 | `8d2e975271b5fb93ce55587c447ad131cf3c7f6b15446426ee611928bd36c8ea` | 0 |
| compiler/noirc_frontend/src/hir/comptime/interpreter/builtin.rs | 129559 | `526cbb3445a6bb14170b36c787bf03aac2d52126362c3d891b13b9c85411493f` | 0 |
| compiler/noirc_frontend/src/hir/comptime/interpreter/cast.rs | 10949 | `44a87eec8ad38ed06f5427b9001e71fcdee437a1cecd7196f524685302f3b020` | 0 |
| compiler/noirc_frontend/src/hir/comptime/interpreter/foreign.rs | 14393 | `a31945d1ebddb005231e0f3a0633a33b53e0917940b6783818d846f32bdea320` | 0 |
| compiler/noirc_frontend/src/hir/comptime/interpreter/frame.rs | 5513 | `28c0f5a7ed09547f7ff3dae0b63807e948e3cc9a5919ebd67cc384fc7d71b97b` | 0 |
| compiler/noirc_frontend/src/hir/comptime/interpreter/infix.rs | 18899 | `a40d5d6febdd4280c2cfb9665065e9ac411926fc12518ff3a6a50a7a157f6526` | 0 |
| compiler/noirc_frontend/src/hir/comptime/interpreter/tracker.rs | 3357 | `f06f1763a82da8e339c59c04d6444706de09a01471e807f37eee75261d8ee6dd` | 0 |
| compiler/noirc_frontend/src/hir/comptime/interpreter/unquote.rs | 2901 | `7a11792fcd19032a90d9edd8cd47bf5906d471a45b797ee04d53d2e4be28c798` | 0 |
| compiler/noirc_frontend/src/hir/comptime/interpreter.rs | 91391 | `1927777a8e38ebc70619dd0b2c28744c2a95a89a9a82211f98ebc4d1d8eb4447` | 0 |
| compiler/noirc_frontend/src/hir/comptime/io.rs | 1154 | `29e1da6aca972c93bfebf51a7992b81539c7416a731fc012921123b276c2361b` | 0 |
| compiler/noirc_frontend/src/hir/comptime/mod.rs | 1344 | `c00a815e2b37c98770ccbbfe7463cb4bcade89a999759c90d1cfda41a5fd6e13` | 0 |
| compiler/noirc_frontend/src/hir/comptime/scopes.rs | 3407 | `636cfa9f717ad2204d629cded9cc536f40d2553f107657684fb74efe37bf764e` | 0 |
| compiler/noirc_frontend/src/hir/comptime/value.rs | 42216 | `2f96b6ca80f44e92e927dab1f0c4746e369cb43bda661e0757adf351e63ead86` | 0 |
| compiler/noirc_frontend/src/hir/comptime/value_cell.rs | 1573 | `e195a1a1ca0f8fe18b326b05382416505b8ba2d920c669731503fe358797e03d` | 0 |
| compiler/noirc_frontend/src/hir/def_collector/dc_crate.rs | 36973 | `523a91bc5636bd24a892b5ca0312ff156ac4841fc32c3cd1fd7fcd99cf373d3b` | 0 |
| compiler/noirc_frontend/src/hir/def_collector/dc_mod.rs | 71977 | `c59139de626d95a8bb12730d78fd75ad3b9cf07be478237e347668e3cfff065f` | 0 |
| compiler/noirc_frontend/src/hir/def_collector/errors.rs | 16447 | `673c166ab9e0c72a42eaff839bf45e3998b2a40d2e4a007e9e7c721256375541` | 0 |
| compiler/noirc_frontend/src/hir/def_collector/mod.rs | 1481 | `85a2b34f116008cb9f1f1b33644a49a5cb402aebd1735319c53ac2377e52c8e2` | 0 |
| compiler/noirc_frontend/src/hir/def_map/item_scope.rs | 5267 | `fb702e13f25b5da5a973f6057d72381bce7c3522d9f470db080946b1727e9e94` | 0 |
| compiler/noirc_frontend/src/hir/def_map/mod.rs | 15489 | `960179cc390bf45c612c1ab4412512a76258d9881b4d9d7372a1f86030822780` | 0 |
| compiler/noirc_frontend/src/hir/def_map/module_data.rs | 7903 | `b459b49e8f5920dd413800590fd9879d79cb5fdc9382f1009208d99d2338e994` | 0 |
| compiler/noirc_frontend/src/hir/def_map/module_def.rs | 3198 | `823b604149d43ea38d8168764fd336ac59c0a11f004648ad12ae9b254536f1e6` | 0 |
| compiler/noirc_frontend/src/hir/def_map/namespace.rs | 1386 | `df4900627159b00a502b37281fc92c1a117e981f6ead77995d9eecbabc770718` | 0 |
| compiler/noirc_frontend/src/hir/mod.rs | 15588 | `e8b4840c50db56ff31c7dda77755afdaa8c85387f12fbd088d09702f017490db` | 0 |
| compiler/noirc_frontend/src/hir/printer/items/hir_def.rs | 54366 | `858febacb7a28d82bdad32f015743a54385959286aacced3943c36866560097b` | 0 |
| compiler/noirc_frontend/src/hir/printer/items/types.rs | 8791 | `c5c24a9aa39e6cedca0536444149160d5998c62e415d52283d63d82cf93c3b0a` | 0 |
| compiler/noirc_frontend/src/hir/printer/items.rs | 34225 | `2fed72d65c8d7eef4149ac7a08e8b39df829d040ba97bbc205042b32a3bd7d29` | 0 |
| compiler/noirc_frontend/src/hir/printer/mod.rs | 63998 | `6fd7acd8ecd413e2d242c511f4fb11cceb708785053e3d2a3b635dc2a2bde781` | 0 |
| compiler/noirc_frontend/src/hir/resolution/errors.rs | 61888 | `2c820eb98291c5d19be94383bb65ba05161455ea8d669c3cdc0934a3ce3bdc60` | 0 |
| compiler/noirc_frontend/src/hir/resolution/import.rs | 28760 | `94f6d9f81abda31cc7f1e54534b3bb0df397d184d9a0b1c220801d31847e8f58` | 0 |
| compiler/noirc_frontend/src/hir/resolution/mod.rs | 596 | `15fc31a14b87ad8311f2adeb9a620c6cfba0c847fb481f1f0ef8fcf99f51c891` | 0 |
| compiler/noirc_frontend/src/hir/resolution/visibility.rs | 14341 | `ded90ed82eb42859bf9e0728130efc259bfea07864ec900c2ab2806ff4c9712f` | 0 |
| compiler/noirc_frontend/src/hir/scope/mod.rs | 6296 | `280b6943788fb4068396243c5f7db8a4ced6c00d11775241a7d4fba069059225` | 0 |
| compiler/noirc_frontend/src/hir/type_check/errors.rs | 53470 | `027f85ec3140e1653ed1fb39880a4f55bd745ae7f2f89aa4fc144b3b565d23c4` | 0 |
| compiler/noirc_frontend/src/hir/type_check/generics.rs | 7465 | `52d68b8cb292eb1e5aa024e2209ef02e58ce99412d09735e0a04763188d0c16a` | 0 |
| compiler/noirc_frontend/src/hir/type_check/mod.rs | 168 | `779d0e001349f2817197a407a3a396180ce6966b3d3afac75c183a53026a3f1c` | 0 |
| compiler/noirc_frontend/src/hir_def/expr.rs | 21326 | `6547a664fc2aef479cab933229a23e009cf491566a1c6473ac3fd67956832f85` | 0 |
| compiler/noirc_frontend/src/hir_def/function.rs | 9780 | `7dbb8825fdb0c869853cdc3b30e76d87a1f97735fa012af262b57861195711d0` | 0 |
| compiler/noirc_frontend/src/hir_def/mod.rs | 523 | `f0fc23a577398769463569884ed3e224ba218cca9adcc62bac0d0a3d3e359a00` | 0 |
| compiler/noirc_frontend/src/hir_def/stmt.rs | 5621 | `7539b9793d3590cfb7ca7b09825e903e37e709cffd0e51415f3dfff494517d44` | 0 |
| compiler/noirc_frontend/src/hir_def/traits.rs | 24547 | `47cac63830a29c385bdfaa5d33666358f7c0e74d54a9e40cfd293ed88f10408f` | 0 |
| compiler/noirc_frontend/src/hir_def/types/arithmetic.rs | 56228 | `961db08c20a12a773f0bd444db1a5d591ffe12c51836ddae19dc2484a9676799` | 0 |
| compiler/noirc_frontend/src/hir_def/types/recursion.rs | 11076 | `b3ebe41efdbff5e6764120131a6eef9a028f5f67b220cc748d92ad809cfaa4c0` | 0 |
| compiler/noirc_frontend/src/hir_def/types/unification.rs | 42362 | `86c32ea207ca044d9a7343c6f4de7cad13aa6d1a0f0627c8500bf5882241b644` | 0 |
| compiler/noirc_frontend/src/hir_def/types/validity.rs | 21315 | `fc44dbfb59ac2c5857d12fbccd1f08ac09aab4e6edbd816afdbacca82f73052d` | 0 |
| compiler/noirc_frontend/src/hir_def/types.rs | 148771 | `dd26877c429422366bd889f502f218faf82c7a264617378ea3c5d5783b6fc713` | 0 |
| compiler/noirc_frontend/src/lexer/errors.rs | 14597 | `c4a32329bdd47aaa7df1f8d72abd244379645a7e2d4a5d9b2eaa4ad9310e7312` | 0 |
| compiler/noirc_frontend/src/lexer/lexer.rs | 82612 | `071375dcce670206a910ca51fed86c3ce1617845bc220fe265b1f75d76d0a8cd` | 0 |
| compiler/noirc_frontend/src/lexer/mod.rs | 348 | `31378b27213bb96b5a6a8ea9305dce0fe4a0bd2b3b53f986877706180da1f326` | 0 |
| compiler/noirc_frontend/src/lexer/token.rs | 40396 | `0ffaa95da2b8072d1c149e5fb5b8d3da264de60b3c6e187bcfbc21fbb6c04f25` | 0 |
| compiler/noirc_frontend/src/lib.rs | 1359 | `5f25e10dbbfc8f6a29f9a0f0d48e6cfbc3a347e4e58d17ba61f97f124d19f0ab` | 0 |
| compiler/noirc_frontend/src/lint.rs | 3017 | `655d32643a3b71cbc1dd4ebe6afd6b460a0c197c27b33d1bd2489e5b47998959` | 0 |
| compiler/noirc_frontend/src/locations.rs | 16985 | `c0edbf7b75dca236e9086ce6fa87b7211741a1331f284f57b19f3ca7d891b748` | 0 |
| compiler/noirc_frontend/src/modules.rs | 14986 | `6e6bdf2236e8367258cd98fb9e59fa860bd1c3964156d7d401f1dd21ff87f114` | 0 |
| compiler/noirc_frontend/src/monomorphization/ast.rs | 27094 | `c6c399c91ac00746476111f3ee9de81617061e762bb35fdf21fe306d025270b7` | 0 |
| compiler/noirc_frontend/src/monomorphization/builtin.rs | 16783 | `39ededaacc964b22396ea7791bfd0618291861217c96d83533b2aa807f5e5819` | 0 |
| compiler/noirc_frontend/src/monomorphization/debug.rs | 9701 | `52043fd6ee07e9b5c06fb25dc1e4905b2f3ee0cbadb490ce30531f2beb34b0ca` | 0 |
| compiler/noirc_frontend/src/monomorphization/debug_types.rs | 5456 | `c26b92eb95eb5bf051fd01d91783c3a6a74ab37575a2d24dab71efb1ba100173` | 0 |
| compiler/noirc_frontend/src/monomorphization/errors.rs | 15970 | `e16f866da47f351732979ec6f049dd6a24953c073b8873825e26d1b41ed7f04d` | 0 |
| compiler/noirc_frontend/src/monomorphization/function_context.rs | 7884 | `f4f5b68e5b7173faae0952f4ceaeba9d8cb4d4a37a93ea982f8dd873c7818c96` | 0 |
| compiler/noirc_frontend/src/monomorphization/mod.rs | 167485 | `fec36123537cdb4afe72926c755fd880a31ae61b05e0416ce736bf610c1a1c79` | 0 |
| compiler/noirc_frontend/src/monomorphization/printer.rs | 29628 | `c2f486a82c41fa2731c42a8e53749f28ed318078ded753a6290ef8662e00b108` | 0 |
| compiler/noirc_frontend/src/monomorphization/proxies.rs | 14913 | `32772eddc7ec0fe4a8293c62fc07246531757c97d11ad04293f44436678464f9` | 0 |
| compiler/noirc_frontend/src/monomorphization/visitor.rs | 12056 | `6459ab2dd160a7c3fe15da4bf5c3dd25440654a030f39281bc6eaec4d7c4ac6b` | 0 |
| compiler/noirc_frontend/src/monomorphization/well_formed.rs | 6071 | `edb04c74805d905210e5d44790580915a3a5c2258ce66e55a2923b4f7cd678dc` | 0 |
| compiler/noirc_frontend/src/node_interner/dependency.rs | 9300 | `a11baea746eae85fac1275d3175355cc939b148c3309fd83adbb49723ed44964` | 0 |
| compiler/noirc_frontend/src/node_interner/function.rs | 8148 | `ebb12805c93334327917ffe6dffeb7e86b0f5554f1b306f12b184adcb88ed887` | 0 |
| compiler/noirc_frontend/src/node_interner/globals.rs | 5637 | `59b39e2aa4337e9e2d491577e295db2cb5d3d4979d4dd09dc5761661c64c642d` | 0 |
| compiler/noirc_frontend/src/node_interner/ids.rs | 4213 | `4b8dc830e15cc071484a0f52237fb545f75ac68c78073658870e39cf9a93a4f0` | 0 |
| compiler/noirc_frontend/src/node_interner/methods.rs | 8636 | `5afc88d435ca3946f8b148c479df1cae49cf4811663be15ca85daf59c42acdaf` | 0 |
| compiler/noirc_frontend/src/node_interner/mod.rs | 78009 | `ad72574872d8682ed515553f3760c74badd74f901d25a717b2c7f7d8a8fec580` | 0 |
| compiler/noirc_frontend/src/node_interner/pusher.rs | 2168 | `4c199a0776ac24d80fb004cef794fbb86818b273dd97483f17264d1899198934` | 0 |
| compiler/noirc_frontend/src/node_interner/reexports.rs | 1142 | `1909bc2d2b9399138e056bdc47a9182db5efd3954a6290ea70f70130f406c72c` | 0 |
| compiler/noirc_frontend/src/node_interner/trait_impl.rs | 40841 | `300a0aa8966936535e940c33177db224b9c89e3e14316f93d25b9d2f1cda8995` | 0 |
| compiler/noirc_frontend/src/ownership/clone_elision.rs | 9206 | `449c003eb9eb6b1fd58482661cb9a9c17001c994b2a825e1ddfdf99588b31236` | 0 |
| compiler/noirc_frontend/src/ownership/liveness.rs | 23331 | `40b7b196933a9a0b9479fe384ea542ebd39f1992c0a99ef167312f5c092d2ee0` | 0 |
| compiler/noirc_frontend/src/ownership/mod.rs | 23020 | `f85915191d6a9a1e150b75a4fe3fad73efdeaae4818c77b4287331ca37613685` | 0 |
| compiler/noirc_frontend/src/parser/errors.rs | 15793 | `65482b010ec923abe20e1c63625dba88324a8a5bab0168d96eedf20f49ed8361` | 0 |
| compiler/noirc_frontend/src/parser/labels.rs | 2683 | `daf80a9d9a4db6e47c91c6912568dfb4999f6ca5de543f1d85f6d91e4d63e2e0` | 0 |
| compiler/noirc_frontend/src/parser/mod.rs | 10403 | `a692774222147128dad27237d25d8887b611aff22d3926b201a81c4b34197edc` | 0 |
| compiler/noirc_frontend/src/parser/parser/arguments.rs | 1241 | `c7e56d4e10130f7ee747fe37b795269efb6a554f5601c26003e5c27771bc8ec0` | 0 |
| compiler/noirc_frontend/src/parser/parser/attributes.rs | 36033 | `e75d7777860d5c7407ddd071e38838659a397a62ea0fbc56568017ff15c86403` | 0 |
| compiler/noirc_frontend/src/parser/parser/doc_comments.rs | 6926 | `84130b834075927696ad3756a1f6300f108723c1657e3ed4d8e9d224399f319b` | 0 |
| compiler/noirc_frontend/src/parser/parser/enums.rs | 8705 | `93bab720084d538b91681e4ff95372b5a5458f530d0fdc270503811ffcec09ec` | 0 |
| compiler/noirc_frontend/src/parser/parser/expression.rs | 86214 | `f1584ade08ad0b226ff6131c1be47a15d1c607eefb4057d3ce9f645814b5f204` | 0 |
| compiler/noirc_frontend/src/parser/parser/function.rs | 25136 | `d9ddd73252bb77e9368909fae1ac3aa1f3d737ebd195033207ead2e0a06fbaa8` | 0 |
| compiler/noirc_frontend/src/parser/parser/generics.rs | 10870 | `a6295d3be2eccdec47a8f58efeb3be78a81347618ead1bcfac29102e61068776` | 0 |
| compiler/noirc_frontend/src/parser/parser/global.rs | 6454 | `a604ab6da26e9bcdbdd94be9f981fe3f159dce7584e8e01c86bbf27309fa9004` | 0 |
| compiler/noirc_frontend/src/parser/parser/impls.rs | 20304 | `317f4d8b860c00ddaf60245fef6148ddb3f39341f93f97c1fba0fba5d11ff399` | 0 |
| compiler/noirc_frontend/src/parser/parser/infix.rs | 7247 | `d3cd134fe647b53a68413bc86a2d2fc667372c5e20fee83555c99e88dccba0ba` | 0 |
| compiler/noirc_frontend/src/parser/parser/item.rs | 13646 | `5c40a31e08f9dacce6e4ddee0baa5213a0788d2877c20cfd1741dc271b8e81a0` | 0 |
| compiler/noirc_frontend/src/parser/parser/item_visibility.rs | 3031 | `7271b1cb51a46fa383e203daa839e7bb15c5562dd83bf68fb7f13b4e1ac992af` | 0 |
| compiler/noirc_frontend/src/parser/parser/lambda.rs | 1942 | `448ee0019e5e7e6974c74a765bc9fcbb71fdbba2336260399c3dda0c81f61078` | 0 |
| compiler/noirc_frontend/src/parser/parser/modifiers.rs | 2022 | `fc863670e631d751c6b19e714ed8af4e0fa1f2b236825fb3ed9a2d966271e9ca` | 0 |
| compiler/noirc_frontend/src/parser/parser/module.rs | 5745 | `2ef35a122a06eaec78b1c6d4e951852e2b6c2a2e2805607db553bc782c90b0e3` | 0 |
| compiler/noirc_frontend/src/parser/parser/parse_many.rs | 4334 | `33f09d44209ec8fdf4d7de012e55b720afdef8cdd886d6765134c68d078db6b0` | 0 |
| compiler/noirc_frontend/src/parser/parser/path.rs | 13168 | `b346fc85869fb2954f42bafeba8e1ec7dcb232176eccd4fb54f96f5ff558c28e` | 0 |
| compiler/noirc_frontend/src/parser/parser/pattern.rs | 12899 | `59dc08af7c9ef34468ea99257f20a0abafe41cbcfbbef7c0add1f7cef4dd7c1b` | 0 |
| compiler/noirc_frontend/src/parser/parser/statement.rs | 32300 | `3f8bcc9aee86a0db5097b7980f26b43145b841c25a96938cdf4e13103c5bdefc` | 0 |
| compiler/noirc_frontend/src/parser/parser/statement_or_expression_or_lvalue.rs | 3042 | `693a5bd01fb7a32103d2e045518350fff4541bc9673d57d5caf328853f1560da` | 0 |
| compiler/noirc_frontend/src/parser/parser/structs.rs | 8884 | `5c51a848a47cf8724e1c9a72d83860dfd439ec7112ac0b9cdfed59c232a43fc8` | 0 |
| compiler/noirc_frontend/src/parser/parser/traits.rs | 24811 | `07a424570351dd2d821c1ca5610a6311222822b8f5bea14e1e1b780d2b9dceb6` | 0 |
| compiler/noirc_frontend/src/parser/parser/type_alias.rs | 6002 | `e411394e3fa0825a28b5f4d212f98cc106e70ce22fc293258fe5daec5f401002` | 0 |
| compiler/noirc_frontend/src/parser/parser/type_expression.rs | 26417 | `f126e6edb2d2de9245e93574c5a26fb2a42a845f83daec86a5dc8495517fcc02` | 0 |
| compiler/noirc_frontend/src/parser/parser/types.rs | 21375 | `19e5dd617e208964722184b911633502110e5596bcad8d98ced604e78f21eef1` | 0 |
| compiler/noirc_frontend/src/parser/parser/use_tree.rs | 10543 | `12cb251e5ea327273af906f563f80fba89332e9b6b4788b420f4a73a7b7d894c` | 0 |
| compiler/noirc_frontend/src/parser/parser/where_clause.rs | 5793 | `1fa02ac9cbfe1d07d9d27f7cdfa68e996b4f20ccd856d280474403845aac7500` | 0 |
| compiler/noirc_frontend/src/parser/parser.rs | 33483 | `75ad3a09148cffb36dfb01618485a64c6e9d8da4a353683a1a5f7790352d50db` | 0 |
| compiler/noirc_frontend/src/resolve_locations.rs | 11094 | `f889c0d8807feddb809aa4b84e551a6b48a1d8980ca0a03ac8cd597a1d6cddc0` | 0 |
| compiler/noirc_frontend/src/shared/builtin.rs | 7363 | `b096b2d1e51d875365401cd5669135b85040a1e6d1bce58d6f30733948f9e9a9` | 0 |
| compiler/noirc_frontend/src/shared/foreign_calls.rs | 1660 | `fbb4257f286ebbc3960f7ea1786e9f0e569909e51756a1dfc09e86732dee9bc9` | 0 |
| compiler/noirc_frontend/src/shared/mod.rs | 436 | `481ea2311ae84af83cf49257e9f1762a4bf966be07dc7003cd2215f67134538f` | 0 |
| compiler/noirc_frontend/src/shared/signedness.rs | 297 | `6152d2139af6a0ac29fbc3349484263e9fb0c42566fa1d3592a19873f54f1437` | 0 |
| compiler/noirc_frontend/src/shared/visibility.rs | 1073 | `0430aada9f26e5c835200d2cbbe4e26aac7d35e358512d442085b8b7fe4e35ca` | 0 |
| compiler/noirc_frontend/src/usage_tracker.rs | 8551 | `49909075ebeffe1a05a008f53f28db2e7822c52f0ae9a510b548ccc3486d78d5` | 0 |
| compiler/noirc_printable_type/Cargo.toml | 487 | `3df877ab602e0fd7312df2e9cd6203d54d219c840cca07b86ef31c7ebe84f628` | 0 |
| compiler/noirc_printable_type/src/lib.rs | 28563 | `5e9561b17b6775401ed6ece5f166f28bff1a703eb2d156950505e52a6fc663aa` | 0 |
| compiler/noirc_span/Cargo.toml | 349 | `98529b40906a5a30ed458fd8e35cb6106b0610befd3dd0e2878e9b9c3017ff09` | 0 |
| compiler/noirc_span/src/lib.rs | 142 | `776f3124b4048c73db640376beb7087df590fa27d7cfb7f255209163f4bd9e70` | 0 |
| compiler/noirc_span/src/position.rs | 4750 | `92493b4776a9201cf88e79217210241dabae621ba5756e35ce7a7b2da8927e03` | 0 |
| compiler/wasm/.cargo/config.toml | 128 | `83a331309d4a5daef03f4a4073d59e927338f7a2465d6143bd530b2ff7237860` | 0 |
| compiler/wasm/Cargo.toml | 1737 | `f0c4b3bb08b2844f695a171af2e41074bb1abe7f478d024ae57c9d7548a21eb6` | 0 |
| compiler/wasm/build.rs | 113 | `04232025c39a2f83e4c6b3433af7e6e1c6511532d9e4b93c7e6ba170f4f1f53d` | 0 |
| compiler/wasm/package.json | 3050 | `413289b9356c7f431befcd951960c6764c97803fcbbba51a81f5b49c0055c3b0` | 0 |
| compiler/wasm/src/compile.rs | 15408 | `b588e3bfd26ed88b2eded3e53bb3a8c46ddae48620275ddb79b782bbae84fddd` | 0 |
| compiler/wasm/src/compile_new.rs | 13872 | `cf620782c07657e5e72557a19e00d042d1598bbe77b86b4d02e50c7fd5022d99` | 0 |
| compiler/wasm/src/errors.rs | 3532 | `1b034c59061c3ab2472aea788f2a888c115e0955e196eccec9f3b9309e7de518` | 0 |
| compiler/wasm/src/lib.rs | 1754 | `fa9899bbccea76d1311fbfdecc5b349079d2d5c23ccb6a11fa881d617f1ad294` | 0 |
| compiler/wasm/src/noir/debug.ts | 320 | `798d00c730e125394ead7b3b53b157c75641baf5986b0d5e41ba72b4d7350093` | 0 |
| compiler/wasm/src/noir/dependencies/dependency-manager.ts | 4254 | `ec8372e1adf50b88bf01940b86459dab97d428c15eb866d80807e88033553d06` | 0 |
| compiler/wasm/src/noir/dependencies/dependency-resolver.ts | 637 | `491630da0d7f169a7ceae6899403aa2e47c5d9881445384bfbed9205dcc79c74` | 0 |
| compiler/wasm/src/noir/dependencies/github-dependency-resolver.ts | 5333 | `b8292122afd3faaf009b847ec9afb9ca41b8918c2d33b0f571f970ed0ef95495` | 0 |
| compiler/wasm/src/noir/dependencies/local-dependency-resolver.ts | 1002 | `c331fc844d426428fe26fe57743c66effd4e9766f489acc67278ac0dedd9196a` | 0 |
| compiler/wasm/src/noir/file-manager/file-manager.ts | 4295 | `1ad4ea925376d8ff2ad05e6fa0436c0f236b83e45b7c09110142695f322addcf` | 0 |
| compiler/wasm/src/noir/file-manager/memfs-file-manager.ts | 1685 | `e2ee6864800cce7161ff8cea5f612e2c088133f32506636b51170bd97f4c5d66` | 0 |
| compiler/wasm/src/noir/file-manager/nodejs-file-manager.ts | 1860 | `decab79632f84b29b405337699387677f69e857ec4a6f967aea6c3facfc04da1` | 0 |
| compiler/wasm/src/noir/noir-wasm-compiler.ts | 7083 | `b890e6259ed34530be2daeeb5355d2f76929ee37a397342754524289c9324b9a` | 0 |
| compiler/wasm/src/noir/package.ts | 3869 | `0c2628253703e8575d7e16fcf9d813bda70e09ebc1a95e6c15d14c7771251528` | 0 |
| compiler/wasm/src/types/noir_artifact.ts | 5191 | `d2c7b4a8fe13ce4a46181cdfe93a127df9c21c1b67f3a0e92347b93ec3d53906` | 0 |
| compiler/wasm/src/types/noir_package_config.ts | 1171 | `92e4d4f4652c340fcee764eba37c4f4032084217067711501be7885aa3d82f68` | 0 |
| compiler/wasm/src/utils.ts | 1766 | `cb42bc3c27af8a7e1200b7c9ce4905eb9d677b903c32697baacab49655aa866f` | 0 |
| compiler/wasm/web-test-runner.config.mjs | 742 | `55d758f463148c79b62721450354da13466888f1d5c7b728c3ffd1ae528c40b1` | 0 |
| compiler/wasm/webpack.config.ts | 3651 | `5ea7531a428674f0061edb9d70c2feb7a3fa51b02fcc32a53e29ee40efc6408d` | 0 |
| docs/docusaurus.config.ts | 9328 | `8dcb888e3e81a3093396b5e0c96c95847785070731d40c8a19d0fcecd7037fd9` | 1 |
| docs/netlify/functions/subscribe.js | 7046 | `51c337ee318308569d3a1507cedcdf8fd90d8cc7b939c19959dace0bc65ff99a` | 0 |
| docs/package.json | 2179 | `91ef3c717eda87eab813371b5ba998d91c7989043c934a187f09a85c45280310` | 0 |
| docs/scripts/preprocess/include_code.js | 13205 | `5b49ff478115ec1a73e1d2a198eb54bc6b3f7b3b405221445993abc7c8d97325` | 0 |
| docs/scripts/preprocess/index.js | 5328 | `cf62edd709d56a1fb42fac291cee8ccd4dd54a4831ab988dcd19397fa60b8e16` | 0 |
| docs/scripts/setStable.ts | 2832 | `43e17383f748d8aa98d30ebce0ad1acc5ef7c3eec2e0cbb32ca602a873ad7d1d` | 0 |
| docs/sidebars.js | 7930 | `a05b6b6be6cfdee5ad00a0ddb5d6e3366f21e6596a69aa50faad248e0b6eb125` | 0 |
| docs/src/components/EmailSubscription/HeroSubscription.tsx | 5129 | `2321141a2639645baea0f8197b2ec0bea578f5576368ef42241f0e010bc5dc8a` | 0 |
| docs/src/components/Matomo/matomo.jsx | 3735 | `a0199a1bb78b0de0e924cc1c8cc1fa341482e686396b997dec4dcd279fa51857` | 0 |
| docs/src/components/NPSWidget/index.tsx | 10423 | `c401a8a13dbce9bb192de38c8c176e49bc245bbd24e390ca37b73a52c4c07d3e` | 0 |
| docs/src/components/Notes/_blackbox.jsx | 279 | `585130d5e367b6f4bff136f82cda16aa25f269905ae0968220b08e112ddc1741` | 0 |
| docs/src/theme/DocRoot/Layout/index.tsx | 516 | `a0d273f1dded7e7e6d6e08c873b7c029a5817e672bac3692ca40d8708d053dde` | 0 |
| docs/src/theme/Footer/index.js | 7052 | `159790daaeb5bf415ceee9cf62e325beb3290da6a24cbcc2d002b950c0024c9d` | 0 |
| docs/src/theme/Layout/index.tsx | 497 | `a0caeca73abfbe2c4d6cb639dbebc54afdef4e87b78c90a40e0683b9ae3f4ee3` | 0 |
| docs/src/theme/Root.js | 1407 | `dd393447ecedc12a78de5980cec686d1a5b5ab3b1086c00e30ab7780be46b2e2` | 0 |
| docs/src/theme/SearchBar/index.js | 494 | `fad8cb6f39695290f97b4c5c1e0bb367ae1477e5659ef1575c645e99fc75f1af` | 2 |
| docs/src/theme/cookbookIcon.js | 691 | `a6fdc62233c096ad30c7ed1eaabc9e4e5725f875c4882a0402c420e4060f9a8f` | 0 |
| docs/src/types/global.d.ts | 764 | `a1f923dc13bc373616bed07e96d491d65fc457738795d7586d348bc7849aa7e9` | 0 |
| docs/src/utils/analytics.ts | 3149 | `61c33331bcb63bdd0c00caa71aadd460bf45e7f8251d470ecbade27ff83d9c64` | 0 |
| docs/src/utils/emailValidation.js | 689 | `afe93c642348c8c5043baa7e17de150c093cbe9b9e386fc00f28b68c9ccd19b4` | 0 |
| docs/versioned_docs/version-v1.0.0-beta.25/reference/NoirJS/noir_js/typedoc-sidebar.cjs | 413 | `9338a8018ae8f97592af9f6abd8a6311819b494eb3e499911aaca48b08775dfd` | 0 |
| docs/versioned_docs/version-v1.0.0-beta.25/reference/NoirJS/noir_wasm/typedoc-sidebar.cjs | 480 | `0f8a694fde95538025f1741c96a6b4be7f13e10f7382ad7fe41de2c7fe736bfc` | 0 |
| docs/versioned_docs/version-v1.0.0-beta.26/reference/NoirJS/noir_js/typedoc-sidebar.cjs | 413 | `9338a8018ae8f97592af9f6abd8a6311819b494eb3e499911aaca48b08775dfd` | 0 |
| docs/versioned_docs/version-v1.0.0-beta.26/reference/NoirJS/noir_wasm/typedoc-sidebar.cjs | 480 | `0f8a694fde95538025f1741c96a6b4be7f13e10f7382ad7fe41de2c7fe736bfc` | 0 |
| docs/versioned_docs/version-v1.0.0-rc.0/reference/NoirJS/noir_js/typedoc-sidebar.cjs | 413 | `9338a8018ae8f97592af9f6abd8a6311819b494eb3e499911aaca48b08775dfd` | 0 |
| docs/versioned_docs/version-v1.0.0-rc.0/reference/NoirJS/noir_wasm/typedoc-sidebar.cjs | 480 | `0f8a694fde95538025f1741c96a6b4be7f13e10f7382ad7fe41de2c7fe736bfc` | 0 |
| docs/versioned_docs/version-v1.0.0-rc.1/reference/NoirJS/noir_js/typedoc-sidebar.cjs | 413 | `9338a8018ae8f97592af9f6abd8a6311819b494eb3e499911aaca48b08775dfd` | 0 |
| docs/versioned_docs/version-v1.0.0-rc.1/reference/NoirJS/noir_wasm/typedoc-sidebar.cjs | 480 | `0f8a694fde95538025f1741c96a6b4be7f13e10f7382ad7fe41de2c7fe736bfc` | 0 |
| docs/versioned_docs/version-v1.0.0-rc.2/reference/NoirJS/noir_js/typedoc-sidebar.cjs | 413 | `9338a8018ae8f97592af9f6abd8a6311819b494eb3e499911aaca48b08775dfd` | 0 |
| docs/versioned_docs/version-v1.0.0-rc.2/reference/NoirJS/noir_wasm/typedoc-sidebar.cjs | 480 | `0f8a694fde95538025f1741c96a6b4be7f13e10f7382ad7fe41de2c7fe736bfc` | 0 |
| docs/versioned_docs/version-v1.0.0-rc.3/reference/NoirJS/noir_js/typedoc-sidebar.cjs | 413 | `9338a8018ae8f97592af9f6abd8a6311819b494eb3e499911aaca48b08775dfd` | 0 |
| docs/versioned_docs/version-v1.0.0-rc.3/reference/NoirJS/noir_wasm/typedoc-sidebar.cjs | 480 | `0f8a694fde95538025f1741c96a6b4be7f13e10f7382ad7fe41de2c7fe736bfc` | 0 |
| docs/versioned_docs/version-v1.0.0-rc.4/reference/NoirJS/noir_js/typedoc-sidebar.cjs | 413 | `9338a8018ae8f97592af9f6abd8a6311819b494eb3e499911aaca48b08775dfd` | 0 |
| docs/versioned_docs/version-v1.0.0-rc.4/reference/NoirJS/noir_wasm/typedoc-sidebar.cjs | 480 | `0f8a694fde95538025f1741c96a6b4be7f13e10f7382ad7fe41de2c7fe736bfc` | 0 |
| docs/versioned_docs/version-v1.0.0-rc.5/reference/NoirJS/noir_js/typedoc-sidebar.cjs | 413 | `9338a8018ae8f97592af9f6abd8a6311819b494eb3e499911aaca48b08775dfd` | 0 |
| docs/versioned_docs/version-v1.0.0-rc.5/reference/NoirJS/noir_wasm/typedoc-sidebar.cjs | 480 | `0f8a694fde95538025f1741c96a6b4be7f13e10f7382ad7fe41de2c7fe736bfc` | 0 |
| docs/yarn.lock | 878568 | `ed3f8e28cd9e855933127e80d73c717e4491154be138975a3089dede52ed81cc` | 3 |
| eslint.config.mjs | 1292 | `4eacaa644944b08988dd41dd53099ec738635ee976ad9788386114813193846a` | 0 |
| noir_stdlib/docs/nargo_doc.js | 1072 | `fc7340dcd9f43ae23a13f198bfcde6e8dcc51f9bd624100f024870c4a6f02931` | 0 |
| noir_stdlib/docs/search-index.js | 143243 | `1260a210038b262fad281d7c2dd9a717881d8c6db674a6cae1bbbe264270f4ca` | 0 |
| noir_stdlib/docs/search.js | 7353 | `3c8caf5ebb8376a0ea652a2b6e58d2c54ccfa94fd9f2c2e379a3dc256e17edf8` | 0 |
| package.json | 1746 | `b9d2173382a6839ecbb540109635eb0196a28bfa9e82eb1dec34be43bb91922d` | 0 |
| rust-toolchain.toml | 159 | `6bb2c03e7043a5eb1af95b27e95364b76e4bdac91b85f51ecf41d46afb11d76a` | 0 |
| scripts/binary_to_fields.py | 1381 | `903fc5f03cc82392d6fdbc8d50e38618efa18c0c66a036c4a2e8866baa481f88` | 0 |
| scripts/check_stdlib_doc_examples.py | 9636 | `14f9021c658d934ead8390669a3f676023a35216898e29959c9745a77f252684` | 0 |
| scripts/stdlib_doc_inventory.py | 8105 | `8c22e179c95e0eed6c408bb362715cb484e0b4197020264da527b8c6d6e91a0e` | 0 |
| tooling/artifact_cli/Cargo.toml | 1065 | `9be99af7eb1a26122e7e0e401f834a8a9cfe54ce2385e615d7a8138f2e58ff46` | 0 |
| tooling/artifact_cli/src/bin/execute.rs | 4582 | `f63ab95972a6e0c818133f624ebbbb805f50f91dbfc41d77343f3a56f76ea106` | 0 |
| tooling/artifact_cli/src/commands/execute_cmd.rs | 8312 | `028b79aea5de9262403a6cc0bda5774be272529fb54c3d836f8161ef664bb576` | 0 |
| tooling/artifact_cli/src/commands/mod.rs | 591 | `b6672aa288524bd3b036409bc04c48d9331e734566b3efb718a56d6df488df37` | 0 |
| tooling/artifact_cli/src/errors.rs | 3330 | `f8a70bdd7c1328c299f6f63de798f512ff01a01fb68f8489eb1c3f0a304ae3fe` | 0 |
| tooling/artifact_cli/src/execution.rs | 11421 | `7d99c353d76416bf7a2c224f0ab0f75bf550d05f23dddbe52eea322e6c0fa8d2` | 0 |
| tooling/artifact_cli/src/fs/artifact.rs | 5287 | `673b47d6c749b2d3e1c757ce1108006a586101608be0bbb73fc3f0ea42c2c933` | 0 |
| tooling/artifact_cli/src/fs/inputs.rs | 3183 | `25b2b786ae4425e53862066b3c9c0195536aba2c47044db7d1a68f5fd34c0194` | 0 |
| tooling/artifact_cli/src/fs/mod.rs | 51 | `e67f0ef4588763085843a86da9830cb143b0dd44d001ab56c7af2d36fc7fc457` | 0 |
| tooling/artifact_cli/src/fs/witness.rs | 1177 | `f9879dcedb108f2f835cd11874fb197e3e539c65a5897bfcb95f61ed1c161448` | 0 |
| tooling/artifact_cli/src/lib.rs | 553 | `2d8d7146e49b72f212f2c53bb04c27788127d04c56ae7a63db1d28a38f9c599e` | 0 |
| tooling/debugger/Cargo.toml | 730 | `331c7dde519e1065670ef23d4c9a36eaa283007665cfd144baf7e0bdf8edb5d9` | 0 |
| tooling/debugger/build.rs | 6256 | `33c1e7f6c67b764789762a13b0aa33d644aad6b70d647f6d9b6f0e517d55e2f4` | 0 |
| tooling/debugger/src/context.rs | 57574 | `294dcfe06dcaf66369a55fbfc7d938e51c1d13f87b7ac8b99ae36b078dfc333f` | 0 |
| tooling/debugger/src/dap.rs | 24422 | `42c0dcc5cbe363faa312220c2720db930e20b6b2ea7683b51364f3bccab7ee9c` | 0 |
| tooling/debugger/src/errors.rs | 352 | `6e4e95bde762f00b9629530f504f1187fabef183dabc3e8eb24c2c96edb51f85` | 0 |
| tooling/debugger/src/foreign_calls.rs | 8256 | `9a57b8daff01913399da7254ae149515e5d56f822a507a027d2b9852fcede5d4` | 0 |
| tooling/debugger/src/lib.rs | 878 | `52bcaf2a7ec78f2c971c302283f66c7c43109f2172990665e9b6c0fa55df2c73` | 0 |
| tooling/debugger/src/repl.rs | 30845 | `63939cbdbddea94c055e7ddf51fed0e8e905d4dec87ffcba3b2047acd935b981` | 0 |
| tooling/debugger/src/source_code_printer.rs | 12027 | `fe4c6be60db486c4d47a5a5d90f2eb3a2f2f1bf892c6c8f4d02e8835d230b472` | 0 |
| tooling/inspector/Cargo.toml | 743 | `1856d0748d3bdf03515a9550b2e076970746f3937130c3a5b9522c83c24089de` | 0 |
| tooling/inspector/src/cli/info_cmd.rs | 7564 | `45d8cffa34329cd62e20185bcec72c586b2d819da6c9e8eb113715cf088a910f` | 0 |
| tooling/inspector/src/cli/mod.rs | 889 | `4d47123bc12eb34dc2d6d7153b31b5af7c08ed0f9c4b70f5d2597f439629b16a` | 0 |
| tooling/inspector/src/cli/print_acir_cmd.rs | 1117 | `90e4eecb02413ef223b8ba2278a32603a5ce06ebac5cde63c073b66c484bc672` | 0 |
| tooling/inspector/src/main.rs | 218 | `54de221b6fa1419b8cef77a2e27a93986cb3f8904252f66bdb77656d765aa220` | 0 |
| tooling/lsp/Cargo.toml | 1163 | `69444116509a71a3dc038dec563f0dccf478589d518c4fb15fcb0a5e0c2045b8` | 0 |
| tooling/lsp/src/actor.rs | 10273 | `9c7dd652dcc81a9368b1910c48130f1a70ee0157ae0bb91988a927f8f6cd61aa` | 0 |
| tooling/lsp/src/doc_comments.rs | 3187 | `98fd0073a9002918ed48bd33bdea8a1559c5982d9d0bbca17d8a2df8f6777059` | 0 |
| tooling/lsp/src/lib.rs | 23055 | `96e5f1e8b57748cf29474aeb3697f6372a5bda7ea88fe4ab1febf31946ef8cab` | 0 |
| tooling/lsp/src/notifications/mod.rs | 27187 | `7e39288e1a99027bd0782d8799530d46458487ce39b405d3d9e996415e82c17a` | 0 |
| tooling/lsp/src/requests/code_action/fill_struct_fields.rs | 7664 | `6baf03b73b63cfc12185cefa06e5fae32f3e674c523caf1a28b26461b9ec4f8c` | 0 |
| tooling/lsp/src/requests/code_action/implement_missing_members.rs | 10030 | `ad1e71af0c28e0e1c22843cfcba206b8e7915e06f1986feb7bc908ec5437d175` | 0 |
| tooling/lsp/src/requests/code_action/import_or_qualify.rs | 9226 | `9701fa29ad56e04dbd4bb5cf7443105aebdb99d5ba61217e56ad291beb9d2639` | 0 |
| tooling/lsp/src/requests/code_action/import_trait.rs | 10295 | `5eb2e5dacd6211479107b18cfb28557b4ca3390525cb6efaf808eacbbd691c8c` | 0 |
| tooling/lsp/src/requests/code_action/remove_bang_from_call.rs | 2231 | `36d96e6cb2a745363e58834566352edffb2bfaa5f9a0b7ab762a558aa0c79861` | 0 |
| tooling/lsp/src/requests/code_action/remove_unused_import.rs | 8793 | `50a0464c3c278231201cd7ff47340d169e4ef8e59d2a49ce8cb71f1e4dfb75cd` | 0 |
| tooling/lsp/src/requests/code_action.rs | 10369 | `25aed5a790f3d0cc8ee24e5649b8acb90bbde0597a52f7de44e5ef9dc07255d4` | 0 |
| tooling/lsp/src/requests/code_lens_request.rs | 13899 | `c4c3a60fd15e96c9ccd607e76ee8171c0113c8988ae488f84444e4506aa08867` | 0 |
| tooling/lsp/src/requests/completion/auto_import.rs | 4441 | `d114dc1b6db2d45d7b4685cacd481318309b7e0e095bb56a03858f89013271a3` | 0 |
| tooling/lsp/src/requests/completion/builtins.rs | 8467 | `9b815f4cf6f2536bc9cf80aa5e17f4322c9b68ef1125591bf484e6976bc77e79` | 0 |
| tooling/lsp/src/requests/completion/completion_items.rs | 26471 | `faa6518aab2a705fcfeb7fb17c410eb89419ff757213a117738f56c315e20d89` | 0 |
| tooling/lsp/src/requests/completion/kinds.rs | 1357 | `4bfb1b320a1deb4ac0d46cf8d9e676613fa515806c14ff2d94b59e16e15f0ccf` | 0 |
| tooling/lsp/src/requests/completion/params.rs | 6043 | `c42b0aa0408051a8fd98074cfc22314d1cdde5bd450b36831eb8971454347ba6` | 0 |
| tooling/lsp/src/requests/completion/sort_text.rs | 1325 | `8da9a49da679238d819ffb6258a57ac12fe3dbf052b2b625078b8952f702b91d` | 0 |
| tooling/lsp/src/requests/completion.rs | 72895 | `527ba0677b133184a8f2998c1ae2e30fed08420a69bcd1cedc565836c823e44d` | 0 |
| tooling/lsp/src/requests/document_symbol.rs | 29783 | `e4834e910687c59722f7627572d204587951b74e349ccbe7517b81e939c34ecf` | 0 |
| tooling/lsp/src/requests/expand.rs | 861 | `a099769c24381f0a7e4199143a0ed1fa86cef84194a7ed3d4d6452daa6469db5` | 0 |
| tooling/lsp/src/requests/folding_range/comments_collector.rs | 3874 | `be98287c3a082bf35c38033c9449a349c52cc1b7d10c76450bb1a6e09171cdb0` | 0 |
| tooling/lsp/src/requests/folding_range/nodes_collector.rs | 3809 | `887e3d79b90ce72d25c97d836a4546976018ca83b30e1e8d7713a227d30db73c` | 0 |
| tooling/lsp/src/requests/folding_range.rs | 1345 | `f708ca1cb8e9d019d91cfc197f29cdc1de064c9dea266369f3f41da88a4cc621` | 0 |
| tooling/lsp/src/requests/goto_declaration.rs | 980 | `7cab00130c261b745e53f82f2745d37bef35391cdcbeb8946c5a0bcf3fa1952d` | 0 |
| tooling/lsp/src/requests/goto_definition.rs | 12639 | `1aae9f368a9aa626ec35b51416bde4401e43039c8284dc9a29e0b070310b1111` | 0 |
| tooling/lsp/src/requests/hover/from_reference.rs | 37671 | `658d8b3a0adaa7b770eda59ef2596c061b36fc89fbf373118c04f350a41d78f6` | 0 |
| tooling/lsp/src/requests/hover/from_visitor.rs | 5483 | `04eaa02ab7f1784111aaa6bc09df958a4d74c2010968c4fb9df9c69c14da223d` | 0 |
| tooling/lsp/src/requests/hover.rs | 16829 | `f7b12dfaf3c50efe25295d1676681850b609e89aec692639fbbae6f2f8acf2e9` | 0 |
| tooling/lsp/src/requests/inlay_hint.rs | 46240 | `39c63c1b3eedf8aaf8043b204a3422e25d3d6b6f36d4f3b3c377277c35ce406b` | 0 |
| tooling/lsp/src/requests/mod.rs | 34058 | `1f725703adba4cf0f8a81ca4e0eacac36eb839f000b72603c703f415d31b8dd3` | 0 |
| tooling/lsp/src/requests/references.rs | 7535 | `57620550c7c2499a61608c89afa7346aab04bb6c880057e825c5d36f37046084` | 0 |
| tooling/lsp/src/requests/rename.rs | 7870 | `c421b5cdae84ec5fdd0799770d12b9d395c9d1b3960bfcd3c12616ae4d0c616d` | 0 |
| tooling/lsp/src/requests/semantic_tokens.rs | 28689 | `39805c11c61b17440b844d3c60bc9d0bb32014d57fbb2472efaa2cbe4d077636` | 0 |
| tooling/lsp/src/requests/signature_help.rs | 15004 | `8406fe1a179fc886f04bfda22b282b99a1fc81dfad8dc61961deac92f985ef61` | 0 |
| tooling/lsp/src/requests/std_source_code.rs | 651 | `897940b8b37c7ba9723bde5cbfd23ae1ac3763b9d494717772bed0e7d7f7e302` | 0 |
| tooling/lsp/src/requests/workspace_symbol.rs | 12865 | `44952da9d1e9d027d8c3e443c3e2979429b79b3a3b96e34894f87ef98cd88f2b` | 0 |
| tooling/lsp/src/solver.rs | 1383 | `05e0cd73c1c1cc01e1e24fcdcffdd3c426338684e7b2439e55f5d6f1333368f9` | 0 |
| tooling/lsp/src/trait_impl_method_stub_generator.rs | 16804 | `556638c5557f8b08c9716b11ff5b45c1e0eedcf30064f9a13a48ee1de786ac23` | 0 |
| tooling/lsp/src/types.rs | 10689 | `c399ef2617d760157b08018259e6880ae71bd002624eb6c0164ff04595ffbd84` | 0 |
| tooling/lsp/src/use_segment_positions.rs | 13370 | `7509293c8b86aacbafa2e7b37405e83702adca593510f26de52c170535accc31` | 0 |
| tooling/lsp/src/utils.rs | 2265 | `9399dd8805b0b1c6e0e3cae19ba0d8e10a9241eb4a3d0097003e98f7c6735791` | 0 |
| tooling/lsp/src/visitor_reference_finder.rs | 12356 | `a153bf1324f7a07275178bc1652c49db22d869cdd845fba24979b312fee62285` | 0 |
| tooling/lsp/src/with_file.rs | 43121 | `9ec8433153aebeb11ce54226544c16ffb4d999b7b0b8d0c1bc86d92289ea362a` | 0 |
| tooling/nargo/Cargo.toml | 1375 | `01115c025ced3f2fa52f58a0f00a4ac32090868eaee10b54835eb396d5957530` | 0 |
| tooling/nargo/src/constants.rs | 637 | `144335dfcc584a886531df4829b8d1817c1a9cd3bbacc13e0103d32970e6d40e` | 0 |
| tooling/nargo/src/errors.rs | 11141 | `e138e54cd70b5e159ecf4e732efc88d9cda1be99668ad5e758cd5cf4f8fad31b` | 0 |
| tooling/nargo/src/foreign_calls/default.rs | 5164 | `16da1589a7907d5cb5dde0fe3780c99f528813f3917992e610fe5ddc3f209411` | 0 |
| tooling/nargo/src/foreign_calls/layers.rs | 4677 | `1f2582a88c56242fa9c789e4837dd25e8365c56438552443fb51d2ac53f1b0f1` | 0 |
| tooling/nargo/src/foreign_calls/mocker.rs | 8298 | `1c485c9076193c10d191d7f28e637cedbfa90d42aae4d6778f76ec3c11c15883` | 0 |
| tooling/nargo/src/foreign_calls/mod.rs | 1871 | `63167d2c8b43a52f487814278c5ab4d9b755d8219d97ffa1c9ee9481413026cd` | 0 |
| tooling/nargo/src/foreign_calls/oracle_resolver_url.rs | 3025 | `bd65ab746c1077a65a80ea318f8749326080722a442a075087ee9598b93c21d2` | 0 |
| tooling/nargo/src/foreign_calls/print.rs | 3100 | `fb33bce4c5275974119a81b17e660b355c95cadaeef7e613e581fb8f303fb0d6` | 0 |
| tooling/nargo/src/foreign_calls/rpc.rs | 18750 | `23ef369824835d57c11bae410f30a700f7a56b92ef5e074b62164c52f3036747` | 0 |
| tooling/nargo/src/foreign_calls/transcript.rs | 3592 | `35202f99521c69d1aab055c50ac4299549b1a84e8d6c54b1fc079d6c35d568c1` | 0 |
| tooling/nargo/src/lib.rs | 10390 | `300f396f70279386e1894c891a4572228a021c211bfbc994471426442c0b161e` | 0 |
| tooling/nargo/src/ops/check.rs | 2062 | `b96878ce72714ed3ec11eab8af8682dcb8200c721c6b7cab37b5ee0e66f634e3` | 0 |
| tooling/nargo/src/ops/compile.rs | 4066 | `da9749c8da10043357fad96188c519aba9da338ce912cbf6f9e72d38c0cf13d7` | 0 |
| tooling/nargo/src/ops/debug.rs | 6518 | `a358523d1c6e66734a4fc08c6d1dbe64afc75163463025d5b33529b988ca06e6` | 0 |
| tooling/nargo/src/ops/execute.rs | 18045 | `66bce782709f6e6a3c7971f4b894f2711dae228d9417e0e041c78f6fce78befc` | 0 |
| tooling/nargo/src/ops/fuzz.rs | 17507 | `27b9f1effba53ed2ed810f28b7a0eb3b8c59734bf5f127870a250a780519c4b2` | 0 |
| tooling/nargo/src/ops/mod.rs | 703 | `9a6f4cba82a81c93490d98c887920ccec58da7693a41f18dd2899e17b141da8f` | 0 |
| tooling/nargo/src/package.rs | 2150 | `e5645edadc6f8efb046a2e21f9738cdaacef12da4c97035f50b2b687753b3ddd` | 0 |
| tooling/nargo/src/workspace.rs | 2894 | `a14d543f6c3ed95e47a1ce29d0102a5c7676bd672e7a0ac9dc2c09299cb74b2a` | 0 |
| tooling/nargo_cli/Cargo.toml | 3287 | `013113449ecf18e846db0ab6b796386904c70d2404148207159198b53b9839ab` | 0 |
| tooling/nargo_cli/build.rs | 36019 | `9cbd8d3238212831a3b28873b734125dad88cdc7ee59960375f3f000c14ac0db` | 0 |
| tooling/nargo_cli/src/cli/add_cmd.rs | 10104 | `650423ad440afe4290f28dbc2e5ef588667faec682d43cafdb1542634530b9ed` | 0 |
| tooling/nargo_cli/src/cli/check_cmd.rs | 7810 | `11c9012981c3c8345d38c70e0dbf6fdbe17424c00df0951692be7245a78a3226` | 0 |
| tooling/nargo_cli/src/cli/compile_cmd.rs | 12156 | `f9198de42c05f7cf7113dab6b6f5d9cc105df9375fc0dc454560535a22231cc8` | 0 |
| tooling/nargo_cli/src/cli/dap_cmd.rs | 22291 | `a1490b22cd54782cda0235dc4995f693006411a45208c83b7e2664c0120d1736` | 0 |
| tooling/nargo_cli/src/cli/debug_cmd.rs | 10782 | `44708e6d3ef5aff6de56f9c27d015b9b3e5ee6cad3b9eca9a620f5f56501ac95` | 0 |
| tooling/nargo_cli/src/cli/doc_cmd.rs | 8674 | `14275b0574a209d2cdad3332410ede114cf5fd63791e33bc43e62b998be31cdc` | 0 |
| tooling/nargo_cli/src/cli/execute_cmd/interpret.rs | 15082 | `fb5ed9ce00f4077e80f10296f30c17feafca92e56219627c3faeb46bcaf5b779` | 0 |
| tooling/nargo_cli/src/cli/execute_cmd.rs | 5832 | `cb77cc90fe76761d31552a8e80a30535ebd689407a2ff4d77550db150da76e0c` | 0 |
| tooling/nargo_cli/src/cli/expand_cmd.rs | 2595 | `2b2ada3d6ebeaf77e4d7f4b956037da25d3bef61ca37fe983833cb32bdbb0c4b` | 0 |
| tooling/nargo_cli/src/cli/export_cmd.rs | 3757 | `3399b700abed5fb9705444da78147578725122deaafb5565b8a25f91230f649e` | 0 |
| tooling/nargo_cli/src/cli/fetch_cmd.rs | 1922 | `a8b7c0fb7cfe65036a85367e7f82c7b101486b24138c623532e9ef3a793dd78b` | 0 |
| tooling/nargo_cli/src/cli/fmt_cmd.rs | 4227 | `8aef93d7ab4e78f53726b802e1e6afb5eaac3eb181a5b0f1f96ff4fb204bfe6d` | 0 |
| tooling/nargo_cli/src/cli/fuzz_cmd.rs | 19991 | `e7d3fe0802047598466fabe63e99bdbb1b1f73da81f3b82240e5631d006913fa` | 0 |
| tooling/nargo_cli/src/cli/generate_completion_script_cmd.rs | 1025 | `9f9385ce5afefcbf8ffafa100998aae9f9b70cb6a02708ddebdeefc5e2b72c94` | 0 |
| tooling/nargo_cli/src/cli/info_cmd.rs | 5689 | `71d9bcc2dd2765d61f3e08a99b9f02c607f188df253611b2b0cf397df2f3c423` | 0 |
| tooling/nargo_cli/src/cli/init_cmd.rs | 3066 | `cbf115a21c129f48886646f795dd49026157d316631c1ecb72b84c64efd75252` | 0 |
| tooling/nargo_cli/src/cli/interpret_cmd.rs | 25012 | `45146f98acd635343f0634df33bc990f201b10dd74cb8fd92663e1f3e1906855` | 0 |
| tooling/nargo_cli/src/cli/lsp_cmd.rs | 1878 | `317004a095fbea3b5bfdb667cc52086b93b0efd9654f58c3fa1ff0ffc7a2cfe6` | 0 |
| tooling/nargo_cli/src/cli/mod.rs | 14057 | `4c624ac22fd9b53fb9e721666f68bf382b1b22ebe0fcee13fdd7cc424b3c1f9f` | 0 |
| tooling/nargo_cli/src/cli/new_cmd.rs | 1619 | `13b4c75c117d8f2fc5d57c15414ca083ebe30e3698deb4acd4d91c6d982c12f5` | 0 |
| tooling/nargo_cli/src/errors.rs | 2101 | `f3d643ffa6563c4230590034e9b7505e0e93d368a56fbba55e811d757ee2a475` | 0 |
| tooling/nargo_cli/src/main.rs | 1707 | `bb80d3496e7ecbce23cd1f5dc6d691a638fd1f9d55fc513c5191ffb33a20fc7a` | 0 |
| tooling/nargo_doc/Cargo.toml | 509 | `155c74af773a1dfe73ab6282670be9b12fca1ea1ff2be54b5258a450f4395898` | 0 |
| tooling/nargo_doc/src/code_blocks.rs | 814 | `031a6119015b6822419fce8f702543db46568ebb1a1b0cf63f688b7f38fb8018` | 0 |
| tooling/nargo_doc/src/html/all_items.rs | 2727 | `1a153df1278c3d2f084cd90b2e0368d9eac15950622e0ec2dc1d86d6577d25e7` | 0 |
| tooling/nargo_doc/src/html/colorize.rs | 9504 | `18bbe1584d780c84b8fc52e7bd3d6f4df04d5b832e6216b62cb37aa1fe3dc01b` | 0 |
| tooling/nargo_doc/src/html/has_class.rs | 954 | `4cd82967ff9ac64b3111a781e075ceb372a452837704ddbd553979855735cc9e` | 0 |
| tooling/nargo_doc/src/html/has_uri.rs | 1363 | `41bf3a550591031af1dc46388899b62fee9446f5bf5bfdf8c64b748de2a716af` | 0 |
| tooling/nargo_doc/src/html/id_to_info.rs | 3624 | `38ef339d0ac4d604c5180688e570c0f2cb978fad0e8d1090adeaa8c966985ef1` | 0 |
| tooling/nargo_doc/src/html/markdown_utils.rs | 4424 | `00cec2e3354e132b64b8d751613023f34ba87a33b4766982dec61447370a9db0` | 0 |
| tooling/nargo_doc/src/html/search_index.rs | 19007 | `fb8f09fb51686b31a6b81a7f7a4a9e55da9cc663999dcb18423937d781d5914d` | 0 |
| tooling/nargo_doc/src/html/trait_impls.rs | 1737 | `dab1ccb6363d436433481559ef2593ca78feed8ab0fc9eeabb48cb4dea3dcc3d` | 0 |
| tooling/nargo_doc/src/html.rs | 80120 | `50eda47364e67375c92fd62553b27ae814be447f3c083a8eb38e5dc1b8d36388` | 0 |
| tooling/nargo_doc/src/ids.rs | 2613 | `10f302a4bc9c180921d20610d76a7b8fd9430488e3ac9176c592e8abe49a5998` | 0 |
| tooling/nargo_doc/src/items.rs | 13965 | `affb01f4611fb0ff49019d9aa871901ae03b175f3b5a8ec9969c9f95b5b2dc36` | 0 |
| tooling/nargo_doc/src/lib.rs | 50255 | `1d4b0372345d4b93811a3d2cb0371c9bb77bbfaf5c978b1373ec06eb1122723d` | 0 |
| tooling/nargo_doc/src/links.rs | 22989 | `ad44021dc5d85c3c6911c269423fb1c430f6dd77b657149d1b532e76bf48574b` | 0 |
| tooling/nargo_doc/src/nargo_doc.js | 1072 | `fc7340dcd9f43ae23a13f198bfcde6e8dcc51f9bd624100f024870c4a6f02931` | 0 |
| tooling/nargo_doc/src/search.js | 7353 | `3c8caf5ebb8376a0ea652a2b6e58d2c54ccfa94fd9f2c2e379a3dc256e17edf8` | 0 |
| tooling/nargo_expand/Cargo.toml | 333 | `934222a469c7a2066ab3ab1355c8fb51c620fc49093b835c5c9201df7c296b95` | 0 |
| tooling/nargo_expand/src/lib.rs | 1274 | `96f4a6e295b6740f9d4ad0d23a8371c5730e3a2230a4de5ef55a6bf700b62e77` | 0 |
| tooling/nargo_fmt/Cargo.toml | 415 | `b0785c3953dbc3907fce5af2c74dfc0507f21322a46e575ed4551f7bff0a1947` | 0 |
| tooling/nargo_fmt/build.rs | 3411 | `75776c2732f22998d5ba93646e146bf2ed5cba2e2e7b6ffc321abc220c96ea19` | 0 |
| tooling/nargo_fmt/src/chunks.rs | 57184 | `ea96ebe7e5de08b88f2f9540ec152c91aaa4dd28ff6f20b470e77cf33b9e8c2c` | 0 |
| tooling/nargo_fmt/src/config.rs | 4413 | `6db5a7c8433566cb736dd07e7c07257e71daaa3753e932a6ebf6b64c309bb510` | 0 |
| tooling/nargo_fmt/src/errors.rs | 289 | `2096c3c60d6dcae0c585053e86c351db71a3dc638e78a757ff70bab60b08da74` | 0 |
| tooling/nargo_fmt/src/formatter/alias.rs | 1805 | `5695bc2d11480262328c7c78e2674f7274f6d9bcfce56c72830f795ddca3a49b` | 0 |
| tooling/nargo_fmt/src/formatter/attribute.rs | 17128 | `bd88cdf0306ee8ae7ebd4d919e364c8b949d207b86eea2e1ae30a9df16fb4e2d` | 0 |
| tooling/nargo_fmt/src/formatter/buffer.rs | 2037 | `6ff265033cf6748f86b236c595ee0142bf72b77569aa2827779167da83e76cfc` | 0 |
| tooling/nargo_fmt/src/formatter/comment_reflow.rs | 27851 | `ffdefa612a20b23769f59ebd26138b6ade55be4dc7184f7234c9935930fa4c21` | 0 |
| tooling/nargo_fmt/src/formatter/comments_and_whitespace.rs | 59618 | `957c89d3434b24a2dc4b16a0f9923d6b69d291b60d3dcbb5f29e258df2978949` | 0 |
| tooling/nargo_fmt/src/formatter/doc_comments.rs | 12981 | `fc1d6cc7f618e2d3c9add1145e9b668e73cea5053bbcced993e57971cf85ef66` | 0 |
| tooling/nargo_fmt/src/formatter/enums.rs | 5391 | `4c91ce7405400b1bbd2390dac31cc27c647e529e21c397a83c3f090a983914b8` | 0 |
| tooling/nargo_fmt/src/formatter/expression.rs | 96968 | `0e7bdcf78f7e7d3cbc5d83d3190333ddb3219b73f5b8eb93782ec59079f05405` | 0 |
| tooling/nargo_fmt/src/formatter/function.rs | 17179 | `cf3b0b2a2de10fb66c08486fe39dc3289d3d75bbfab1b2bed0466c592665aa5a` | 0 |
| tooling/nargo_fmt/src/formatter/generics.rs | 3414 | `242b9de3eda8a5936c7585bd173dba281774da1c13553c9b8b2ff25bd3ee21e3` | 0 |
| tooling/nargo_fmt/src/formatter/global.rs | 3452 | `f9f3b5bf503a8294e491eaee8dcbf1c5b34c05a273028bd266922f9648120af6` | 0 |
| tooling/nargo_fmt/src/formatter/impls.rs | 2962 | `ae0dba8cd478bc8198974f0b1b754fdf3516d380ad3011067218b5549c188896` | 0 |
| tooling/nargo_fmt/src/formatter/item.rs | 7362 | `db639f5e9329fbb960c91774238f6875be032c132fe6bf3fcc786d26d5bd27d2` | 0 |
| tooling/nargo_fmt/src/formatter/lvalue.rs | 2280 | `f9d42d6720a288b422ed28f6cc7b9748ffe28d35a6680a3a258a5e1fcd42ccb3` | 0 |
| tooling/nargo_fmt/src/formatter/module.rs | 3684 | `e320f4e69d2f1d70ee8944c768f643138340e5a49b937e7c143cdfe606639697` | 0 |
| tooling/nargo_fmt/src/formatter/path.rs | 1832 | `a4cea79b5d6ef651203b9c3f11096c7fe77aa41e1c622a1590f117086392af84` | 0 |
| tooling/nargo_fmt/src/formatter/pattern.rs | 8659 | `14a0b6a8ab2fafe9a7c0fa54aae2ed77501792e0b24178bdfb1c8d7665559714` | 0 |
| tooling/nargo_fmt/src/formatter/statement.rs | 26364 | `bdaa22e97dc35ffa8f17918bdfff087412f9368980118f5fe2760640e4037be9` | 0 |
| tooling/nargo_fmt/src/formatter/structs.rs | 4903 | `aa1d9e88465b85103227aa7ddc9e03f2d273999c4cf2d61916965cf2485ae31d` | 0 |
| tooling/nargo_fmt/src/formatter/trait_impl.rs | 5860 | `80db89da875ce359d49c7cd2b2caae81b77475c65ae5873069d111f4f85c41b7` | 0 |
| tooling/nargo_fmt/src/formatter/traits.rs | 9066 | `b71cb7e884174885bbfba7b38d7389262caf605a6bdd7122d8b7803e20b1b6f7` | 0 |
| tooling/nargo_fmt/src/formatter/type_expression.rs | 1559 | `b6abbcdac02698e114233a7794f6e66fe5e80818546a0867a94019389aea2d45` | 0 |
| tooling/nargo_fmt/src/formatter/types.rs | 14135 | `7c220182a27a09de8b7fd3f906f046276657f0f2de37f8681f775bf7cfec3b5e` | 0 |
| tooling/nargo_fmt/src/formatter/use_tree.rs | 8671 | `fa2d914704c1e9c6559d79393a15d564532a35a42e520d9921fddc6eb41ea02c` | 0 |
| tooling/nargo_fmt/src/formatter/use_tree_merge.rs | 22254 | `3d56bd85b72acc79830eceefc561477930ccdb16e117af4e0744d88d16bcf154` | 0 |
| tooling/nargo_fmt/src/formatter/visibility.rs | 1652 | `e3ccc735aa616934db3bf988540ddde0bbbcd9d6923397fae4b3481d083f1575` | 0 |
| tooling/nargo_fmt/src/formatter/where_clause.rs | 2788 | `b765b2da288da6a6cd807ae975365b893457ec2f8a3dbfe8011a0646a8c7ade9` | 0 |
| tooling/nargo_fmt/src/formatter.rs | 13990 | `600483032f452cfffbcf3211aac858d4487f1b69d7447bcafa1dc00a6443adbb` | 0 |
| tooling/nargo_fmt/src/lib.rs | 7062 | `1f0e892548715bcb5d7a0681346ace9ccdabcd67cf5fa95285a2a6cbea608bfc` | 0 |
| tooling/nargo_toml/Cargo.toml | 760 | `778903f42fde089d34cc91fb5bc050773223ecc2feee8d14012ac620083f2392` | 0 |
| tooling/nargo_toml/src/deserializers.rs | 4716 | `5d086453f4a1194097c4b711ec167a56c0f3b295077935ecfc69f34b23c1f076` | 0 |
| tooling/nargo_toml/src/errors.rs | 5672 | `ba50cd89de74207e79cab6f574658ae778d0aa0709ca2cde38dc21d6950619ea` | 0 |
| tooling/nargo_toml/src/flock.rs | 851 | `9ecd8163ae6856edf4a54c0541a08e0eb575e093daa9222ee7126253965e39dc` | 0 |
| tooling/nargo_toml/src/git.rs | 11387 | `a729a0eb3cadce041ff6d07dc9cc272e6cdc68b31383f826c9f1b0197b255404` | 0 |
| tooling/nargo_toml/src/lib.rs | 38549 | `7af9136876079e8a379e1fc15e833471649a928af3d0bfde1a54c5ef1b69baba` | 0 |
| tooling/nargo_toml/src/semver.rs | 9515 | `9d9cd865a4085b8f3f3d25961e2f1b2e55ca0a4ca66120060ce86ad2cbe2ba60` | 0 |
| tooling/noir_codegen/package.json | 2072 | `e167f77657b64f48db0486351aa754b9102cf88d715fa026100ab43171a804f2` | 0 |
| tooling/noir_codegen/src/index.ts | 614 | `bc2fd8036c994a943aff8adf649c78a95e73cd0fd6a27b2f51c52bcea5e3bd83` | 0 |
| tooling/noir_codegen/src/main.ts | 1587 | `3a2bad781edd6321956f1770fc673251efb866b280b1e45ae868a68fc61c5e87` | 0 |
| tooling/noir_codegen/src/parseArgs.ts | 2490 | `94bc3f17868f6a357b9f507a10957a698f73f33c011ddc80fe454310e84d308c` | 0 |
| tooling/noir_codegen/src/utils/abi_type_with_generics.ts | 3300 | `30222fe3db4b16de4b2075d3deb479b244ddf2b422bb9e9754256985978e9820` | 0 |
| tooling/noir_codegen/src/utils/demonomorphizer.ts | 9784 | `80283fe42086504637aa4ddef6f957674182e31478f91f6fd00d2f68680057d6` | 0 |
| tooling/noir_codegen/src/utils/glob.ts | 267 | `95429ab3d635ff08373733e80787804adc758f803312d8e2beba56256f23982b` | 0 |
| tooling/noir_codegen/src/utils/typings_generator.ts | 11797 | `7e90aa5c5d6777d86d756cb5b0f6ccc1ba20f2f6f1cc93ee8a5302824bcffa7b` | 0 |
| tooling/noir_js/package.json | 2153 | `2d422a2a53593bb74d443f333a9ff7328c8e259c10a2ded7d8b42fc1192ace41` | 0 |
| tooling/noir_js/src/base64_decode.ts | 525 | `d670e18dc7e45fd56703d05bcc6d8d69202bcf185aef91b3723f6d421df92c08` | 0 |
| tooling/noir_js/src/debug.ts | 4770 | `e0b64ee7225b587ed86f62e8f24c77b56efe1d6db45ffa240e3d572c70740c4b` | 0 |
| tooling/noir_js/src/index.ts | 598 | `83f043cfb034bcef33a46b406c1acd70dbc1b9100f3edf17de590cf8e7acf4fa` | 0 |
| tooling/noir_js/src/program.ts | 1282 | `d3cdb396a343d267e8e9334483fa6abff47841d97e767b5e8dfaf401743401e6` | 0 |
| tooling/noir_js/src/witness_generation.ts | 3527 | `ba744d1f372b17a61f627769210c9fc5be634a13360107e12cfef85885b40f5e` | 0 |
| tooling/noir_js_types/package.json | 1433 | `3cab3bbda8a3df3091126a3ae535d68246a1a163f1c7221c8e23b3dc5e4add6e` | 0 |
| tooling/noir_js_types/src/types.ts | 4573 | `d5de8c7b979b308dd6f113fc95112c46040cb3eb55d4ee3572206873067323bd` | 0 |
| tooling/noirc_abi/Cargo.toml | 760 | `4ebcb545ef93c6b8caadcf735002b2ef80977873f2d7418892c07b6e7e35bb0f` | 0 |
| tooling/noirc_abi/src/arbitrary.rs | 5835 | `533bfe093cccf847406415a889174e2071e7aea5737063e895a3270868f7e1f8` | 0 |
| tooling/noirc_abi/src/errors.rs | 2996 | `29192ae98e0c9dc7cb65ce7b30d2acf03d13277512931a401cf88274dfec03b5` | 0 |
| tooling/noirc_abi/src/input_parser/json.rs | 13660 | `4c2540f7be92b9abcd2d7ac63a4c338435c194c2cf8e0637b13e180b0fcc23ce` | 0 |
| tooling/noirc_abi/src/input_parser/mod.rs | 19779 | `54bc70e6fbeb2eb9850f6a9953a7c4ee8dc72e0de50c19bffee8211e55464ca6` | 0 |
| tooling/noirc_abi/src/input_parser/toml.rs | 14876 | `01114f210445397a502262ad977cbff95ae85c04de010e99a87b8b7b99fa1138` | 0 |
| tooling/noirc_abi/src/lib.rs | 26281 | `ecc8a20f5812576d6245dcb12ff726bbd77172ac5ca30329b0e77ea58a8b3799` | 0 |
| tooling/noirc_abi/src/serialization.rs | 6386 | `914fe3ef0bac0bcfa4872544df88d527d636b5a832fece48321b16686885df20` | 0 |
| tooling/noirc_abi_wasm/.cargo/config.toml | 128 | `83a331309d4a5daef03f4a4073d59e927338f7a2465d6143bd530b2ff7237860` | 0 |
| tooling/noirc_abi_wasm/Cargo.toml | 1199 | `02d2b1505392c378fe45d722f1f72505a777150b9a12e3448e6b2cbefa45a75a` | 0 |
| tooling/noirc_abi_wasm/build.rs | 391 | `ee22c67c8b82692c9565a8d859693a6daa12a576ff9b70f8cf11eec2c080ccd0` | 0 |
| tooling/noirc_abi_wasm/package.json | 1517 | `fa20cb7b457a981115a1fc6cc846493970fb9e63898934c8fce524d7fcf0dbd8` | 0 |
| tooling/noirc_abi_wasm/src/errors.rs | 1473 | `4d857be038147ea1318ae921ea86d338e0bacaca3d6cd2d46a799a5018d41287` | 0 |
| tooling/noirc_abi_wasm/src/js_witness_map.rs | 3579 | `5e0653090cc55e308bc950e8fa8bc3356fc6b4528ac79dc114114f239ed13494` | 0 |
| tooling/noirc_abi_wasm/src/js_witness_stack.rs | 1832 | `e96e7e118b8413148228ecc279dacdeca02870cf760569c763c82a71bfdc8d95` | 0 |
| tooling/noirc_abi_wasm/src/lib.rs | 8893 | `a328c2bdc7c0ce8101638f39d915f4d0b5a5e43fddd2211f5c6d9545082421b9` | 0 |
| tooling/noirc_abi_wasm/web-test-runner.config.mjs | 825 | `30e43ea4093c157f1c04aa9496c3cc7dddd5aff66ee0312e7fbd12dafa122e96` | 0 |
| tooling/noirc_artifacts/Cargo.toml | 768 | `dd31fe086deb75fcf37f1a92424278f6351eff27d2486fffd86317dfcb6247f0` | 0 |
| tooling/noirc_artifacts/src/contract.rs | 5721 | `0fd17b05d088b15d96553e4b80b4718d21c7c19b2cc1557323dc5064762500c4` | 0 |
| tooling/noirc_artifacts/src/debug.rs | 21180 | `e48fc65e6a7ecf1d28179a05004d4092b99904fc4752aba0f8f1f9bef517e0fc` | 0 |
| tooling/noirc_artifacts/src/debug_vars.rs | 6706 | `f9109437e2c40063fb1edbe45d7713ab656c279978cc22051a9fef5954d2adac` | 0 |
| tooling/noirc_artifacts/src/lib.rs | 5206 | `381902c566dd08c608977dcab6dd094f633b246d23e5e2fa8f52dc633b0ec811` | 0 |
| tooling/noirc_artifacts/src/program.rs | 3279 | `a9eea427cdfc922e0b95a1ca4801707ed3129a1780f7f1306309c32883b6791c` | 0 |
| tooling/noirc_artifacts/src/ssa.rs | 918 | `44d117a982caef6dc53dfcf8ca64d6076369c0bae797aa2dff503a4db1288f0a` | 0 |
| tooling/noirc_artifacts_info/Cargo.toml | 439 | `57ea944f853920d80f0555e8069232be20097e4f3db98cb2363a76886080eb64` | 0 |
| tooling/noirc_artifacts_info/src/lib.rs | 3504 | `0b1f996262950356894c36ace027c51c4172e2a931744c7e2ea1c65126dc5a6d` | 0 |
| tooling/profiler/Cargo.toml | 1088 | `1188e322968c534f59e5cce1bdea608dd5d289f39a845927f63990cfc0bc31c3` | 0 |
| tooling/profiler/src/cli/execution_flamegraph_cmd.rs | 9037 | `d5795b398e54a74a2f7101a6ff3f6e131bb55da455cf3a516e3a15402ba67c40` | 0 |
| tooling/profiler/src/cli/gates_flamegraph_cmd.rs | 7719 | `9cb4a5f3057ac9dcf0cc6e80f78a134d400cf0f1592901fc0846f7ac6d3da82c` | 0 |
| tooling/profiler/src/cli/mod.rs | 1172 | `6f3a0b534a42a046818bfad8497f072d4819957c8dcbb74cc3882c3134aeb73f` | 0 |
| tooling/profiler/src/cli/opcodes_flamegraph_cmd.rs | 10540 | `5aa20e8db790dc8f31956e5d2a2a8d2163ad0c589ca8d9b09fc020d92a2c416e` | 0 |
| tooling/profiler/src/errors.rs | 631 | `74b800af6cde7b3cf9430e2ade4a69416a43686d80f1ee2ad0ae456fcbce261f` | 0 |
| tooling/profiler/src/flamegraph.rs | 15881 | `335d1b50e35b9ebbfed84a31357c944c669cbed5fbc363abe5dbc3b5057f2654` | 0 |
| tooling/profiler/src/gates_provider.rs | 1937 | `5f29316a9892a23ae32f0bb60e6f20249b9c23d9097cd2052ef3b93e92224702` | 0 |
| tooling/profiler/src/main.rs | 1047 | `880e30660bcf808e61e85964b062fc502ff715b609419342544c53e675c98307` | 0 |
| tooling/profiler/src/opcode_formatter.rs | 5690 | `952e0251e122dbb435e0c42e52db7c9393ef316139acc59c196335ceba448a22` | 0 |
| tooling/ssa_cli/Cargo.toml | 795 | `e1686e57f3025dc3d0b50d88cd1681b18bbfc5783aa182f041e08338fd6f7e5d` | 0 |
| tooling/ssa_cli/src/cli/interpret_cmd.rs | 7277 | `539df2145a608f43ae9377fa4400c4141f98896237c4526713595fb664d56b32` | 0 |
| tooling/ssa_cli/src/cli/mod.rs | 6529 | `bd1c72298d6acbefb6be1c1d2cb4fa8591a8bd6f01b2cb182c5e53c54925e76a` | 0 |
| tooling/ssa_cli/src/cli/transform_cmd.rs | 2954 | `aca608503069b1d4c671846bba91f34236131c06640a4b4f2b804c8d2b26ae2b` | 0 |
| tooling/ssa_cli/src/cli/visualize_cmd.rs | 3865 | `40183b766120b0449e6f8c5926279a1a9cc290693b145ce935b6872bb0f49e2f` | 0 |
| tooling/ssa_cli/src/main.rs | 549 | `f61690e4ce85375520775eac489e7be0a2ba2bb82a0093c85397f6abf63b9ae9` | 0 |
| tooling/workspace_layering/Cargo.toml | 274 | `9e8d97cf4be48438f2711d31e01a9ba71e13981cb22c7cf2ae925c51ca35571c` | 0 |
| tooling/workspace_layering/src/lib.rs | 79 | `c7332ebd65650bc85a2ff4418993e38e5842b5d6bc7e960440ca1315d785c001` | 0 |
| utils/iter-extended/Cargo.toml | 303 | `fc2a759fe468e9e6cf35d2f2dd2bd978653dec523cd4262740f9b73410c23c99` | 0 |
| utils/iter-extended/src/lib.rs | 1737 | `aa0f56b3525931027c7ef96adfb7d2d88507940136a1b69e428a1fd7f4cef696` | 0 |
| yarn.lock | 427731 | `eaecdd96e54993fbee5307979728c636966cd23d122c0031965c80fd974674a4` | 0 |
