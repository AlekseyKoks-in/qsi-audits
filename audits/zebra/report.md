# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** zebra @ 147a6a8bf7d3 · Zcash Foundation — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-29 23:49 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 8d18afbc-4df4-4a08-b655-7271d4eadaa9 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `91cfb3dd01b634fae7dd5a8e161479a5e242739f2957bd218e9a221f11e5df4c` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **2**
- Средняя: **13**
- Низкая: **5**
- Информационная: **6**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 10
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 11
- Рекомендация по улучшению: 4
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

Проверка аналитика: подтверждено — 0, не применимо — 0, отклонено как ложные срабатывания — 1.

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/ZcashFoundation/zebra> @ `147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522` — ссылки в доказательствах открывают строки на этом коммите.

439 файлов, всего 6520513 байт, редактирований: 0; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| dependencies | проверено | 13 | Cargo.lock: 709 dependencies parsed (709 pinned); Cargo.toml: 148 dependencies parsed (0 pinned); tower-batch-control/Cargo.toml: 16 dependencies parsed (0 pinned) |
| keys | Недостаточность данных | 1 | SECURITY.md line 70: OpenPGP algorithm ID 18 is not in the algorithm registry |
| certificates_and_keys | проверено | 1 | SECURITY.md: certificates/keys parsed |
| source_code | проверено | 419 | book/lens-init.js: 132 lines scanned with 16 rule patterns and 128 registry patterns; book/mermaid-init.js: 1 lines scanned with 16 rule patterns and 128 registry patterns; book/mermaid.min.js: 4 lines scanned with 16 rule patterns and 128 registry patterns |
| tls_configuration | проверено | 1 | book/src/user/lightwalletd.md: nginx TLS directives parsed |
| osv_advisories | проверено | 1 | 709 pinned packages queried at OSV.dev; 11 affected (2 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- keys — Недостаточность данных: SECURITY.md line 70: OpenPGP algorithm ID 18 is not in the algorithm registry

## 5. Краткое описание архитектуры

Static review of the source tree zebra at 147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522. 439 files analysed; of 1600 files, 836 are test, fuzzing, benchmark or example code and were left out, 325 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .agents/skills/zebra-pr/SKILL.md, .changes/header.tpl.md, .changes/tower-batch-control/v1.1.1.md, .changes/tower-fallback/v0.2.43.md, .changes/unreleased/.gitkeep. 56 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **62** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 43.9%

## 7. Подробное описание находок

### QSI-2026-07371 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0340

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
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

### QSI-2026-07372 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0341

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
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

### QSI-2026-07350 — Квантово-уязвимый ключ Ed25519 (Ed25519) в SECURITY.md

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
- Затронутый актив: `file:SECURITY.md#line 70`
- Источник данных: SECURITY.md
- Метод обнаружения: Разбор открытого ключа.
- Анализатор: certificates 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 50.3 / 100
- CVSS v3.1: неприменимо

Найден открытый ключ Ed25519 Ed25519 (строка 70).

**Возможные последствия.** Долгосрочный риск при появлении CRQC; для обмена ключами записанный трафик может быть расшифрован задним числом.

**Шаги воспроизведения.**

```
Откройте строка 70 в предоставленном файле SECURITY.md и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_key · SECURITY.md · line 70 · SHA-256 6dbf836a10cb57142effcc3f89dd5e74340870bac059dd57e9f528bf344e8db8_

```
OpenPGP primary key: algorithm ID 22 (Ed25519) Ed25519
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня.

**Рекомендация.** Внесите в инвентаризацию и запланируйте миграцию на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it..

**Повторная проверка.** Повторный аудит после миграции.

### QSI-2026-07367 — opentelemetry_sdk 0.31.0 затронут GHSA-w9wp-h8wv-79jx (CVE-2026-48504)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/opentelemetry_sdk@0.31.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-w9wp-h8wv-79jx (CVE-2026-48504) для пакета crates.io opentelemetry_sdk версии 0.31.0: opentelemetry_sdk has unbounded memory allocation in W3C Baggage propagation. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-w9wp-h8wv-79jx
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-w9wp-h8wv-79jx](https://osv.dev/vulnerability/GHSA-w9wp-h8wv-79jx) · manifest · SHA-256 2fdd505d93a06e3777486ba943c941dd9227d6544f3653f928247551ce3382ce_

```
{"id": "GHSA-w9wp-h8wv-79jx", "aliases": ["CVE-2026-48504"], "modified": "2026-09-10T03:50:50.807599062Z", "summary": "opentelemetry_sdk has unbounded memory allocation in W3C Baggage propagation", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L"}], "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.32.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07353 — Квантово-уязвимый Pedersen commitment: пороговая подпись и протоколы MPC (12 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Pedersen commitment:threshold_mpc`
- Источник данных: zebra-chain/src/orchard.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

82 упоминаний Pedersen commitment в 12 файл(ах), например zebra-chain/src/orchard.rs:22. Роль по путям, именам функций и соседнему коду: пороговая подпись и протоколы MPC. Paillier, обязательства Педерсена и доказательства на дискретном логарифме внутри пороговых ECDSA и EdDSA ломаются алгоритмом Шора; постквантовая пороговая схема — это смена протокола, а не параметра.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте zebra-chain/src/orchard.rs:22 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [zebra-chain/src/orchard.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard.rs#L22) · line 22 · SHA-256 f6d08ee12325483da3dbe2df9e5f13d685efad82cd10d2bc18fabc25522d5b0e_

```
   21 | pub use address::Address;
   22 | pub use commitment::{CommitmentRandomness, NoteCommitment, ValueCommitment};
   23 | pub use keys::Diversifier;
```

_file_excerpt · [zebra-chain/src/orchard/action.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/action.rs#L11) · line 11 · SHA-256 cf94db56886a8d071e1e21d46d4cbf3649f1b646e5c32bac092eb7d0eb0fb336_

```
   10 | use super::{
   11 |     commitment::{self, ValueCommitment},
   12 |     keys,
```

_file_excerpt · [zebra-chain/src/orchard/action.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/action.rs#L26) · line 26 · SHA-256 826ab4e1514de78219079f6b2165b83d604063d72a410ebe5b5baa3c82d80fd7_

```
   25 |     /// A value commitment to net value of the input note minus the output note
   26 |     pub cv: commitment::ValueCommitment,
   27 |     /// The nullifier of the input note being spent.
```

_file_excerpt · [zebra-chain/src/orchard/action.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/action.rs#L75) · line 75 · SHA-256 3be0d0808ca91c377eb7a42b499031a63fada120adc8bfa4f05298668fa36bc2_

```
   74 |             // See [`ValueCommitment::zcash_deserialize`].
   75 |             cv: ValueCommitment::zcash_deserialize(&mut reader)?,
   76 |             // Type is `{0 .. 𝑞_ℙ − 1}`. See [`Nullifier::try_from`].
```

_file_excerpt · [zebra-chain/src/orchard/arbitrary.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/arbitrary.rs#L13) · line 13 · SHA-256 1ed2ce6ff82f4c37762407c3c49f9f7f2fb752e4c9d2116aa67f10e8f404b764_

```
   12 | use super::{
   13 |     keys::*, note, tree, Action, AuthorizedAction, Flags, NoteCommitment, ValueCommitment,
   14 | };
```

_file_excerpt · [zebra-chain/src/orchard/arbitrary.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/arbitrary.rs#L27) · line 27 · SHA-256 207ee8f19d55595b48bba6b8182485f0a51d069d4470178b3c7341c9612cc687_

```
   26 |             .prop_map(|(nullifier, rk, enc_ciphertext, out_ciphertext)| Self {
   27 |                 cv: ValueCommitment(pallas::Affine::identity()),
   28 |                 nullifier,
```

_file_excerpt · [zebra-chain/src/orchard/commitment.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/commitment.rs#L106) · line 106 · SHA-256 08f8542a29446e7fda07bc27147d3f2a10e4f01644379e61049e5e722ef2bdc3_

```
  105 | #[derive(Clone, Copy, Deserialize, PartialEq, Eq, Serialize)]
  106 | pub struct ValueCommitment(#[serde(with = "serde_helpers::Affine")] pub pallas::Affine);
  107 | 
```

_file_excerpt · [zebra-chain/src/orchard/commitment.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/commitment.rs#L108) · line 108 · SHA-256 b68baeff124b8c3148a522a34bbbe6e3181df1dabbeddcadc9f062b6da23429a_

```
  107 | 
  108 | impl<'a> std::ops::Add<&'a ValueCommitment> for ValueCommitment {
  109 |     type Output = Self;
```

_file_excerpt · [zebra-chain/src/orchard/commitment.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/commitment.rs#L111) · line 111 · SHA-256 f05e3e2c063b4935a0e59eb800a4c5a04881f15e0338d77c5f3007972fd86d02_

```
  110 | 
  111 |     fn add(self, rhs: &'a ValueCommitment) -> Self::Output {
  112 |         self + *rhs
```

_file_excerpt · [zebra-chain/src/orchard/shielded_data.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/shielded_data.rs#L16) · line 16 · SHA-256 b4dfbca3397f23d45a911b1ccaec4f293bd4d98a42e9eddf9542d86762a03e42_

```
   15 |     block::MAX_BLOCK_BYTES,
   16 |     orchard::{tree, Action, Nullifier, ValueCommitment},
   17 |     primitives::Halo2Proof,
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07357 — Квантово-уязвимый Halo 2 (IPA): подпись транзакций и сообщений (5 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Halo 2 (IPA):transaction_signing`
- Источник данных: zebra-chain/src/primitives/proofs/halo2.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

18 упоминаний Halo 2 (IPA) в 5 файл(ах), например zebra-chain/src/primitives/proofs/halo2.rs:15. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте zebra-chain/src/primitives/proofs/halo2.rs:15 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [zebra-chain/src/primitives/proofs/halo2.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/primitives/proofs/halo2.rs#L15) · line 15 · SHA-256 3fb839f296b33815e4e260d3a077c35f6b376a3b533e8a3b39f7b2d579b72410_

```
   14 | #[derive(Clone, Eq, PartialEq, Serialize, Deserialize)]
   15 | pub struct Halo2Proof(pub Vec<u8>);
   16 | 
```

_file_excerpt · [zebra-chain/src/primitives/proofs/halo2.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/primitives/proofs/halo2.rs#L17) · line 17 · SHA-256 e08cc192d13bc0734e6c4d309d2581a33638e384d5da3069f435021d90c74e9c_

```
   16 | 
   17 | impl Halo2Proof {
   18 |     /// Encode as bytes for RPC usage.
```

_file_excerpt · [zebra-chain/src/primitives/proofs/halo2.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/primitives/proofs/halo2.rs#L24) · line 24 · SHA-256 a317cb19142d43c90ba727a134f664d9e3eb6473c3b1ed22477fd5a172f9b8fb_

```
   23 | 
   24 | impl fmt::Debug for Halo2Proof {
   25 |     fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
```

_file_excerpt · [zebra-chain/src/transaction/arbitrary.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transaction/arbitrary.rs#L23) · line 23 · SHA-256 2a3cc9295bdcf82ce5e2f03b098204c896d3963fc7bbeec86ffb435febd2e652_

```
   22 |     parameters::{Network, NetworkUpgrade},
   23 |     primitives::{Halo2Proof, ZkSnarkProof},
   24 |     sapling::{self, AnchorVariant, PerSpendAnchor, SharedAnchor},
```

_file_excerpt · [zebra-chain/src/transaction/arbitrary.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transaction/arbitrary.rs#L754) · line 754 · SHA-256 b09d9f14818cad29469bff6e6e4af613ffe3e0ee6ef208c1256cd6ff3f977a49_

```
  753 |                         Just(shared_anchor),
  754 |                         vec(any::<u8>(), proof_size).prop_map(Halo2Proof),
  755 |                         Just(actions),
```

_file_excerpt · [zebra-chain/src/transaction/arbitrary/shielded.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transaction/arbitrary/shielded.rs#L21) · line 21 · SHA-256 69e43a64dc3e4160f4ddf4178fbb2c94ded8e90907efed13240f873e4d5bc6c2_

```
   20 | };
   21 | use halo2::pasta::pallas;
   22 | use nonempty::NonEmpty;
```

_file_excerpt · [zebra-chain/src/transaction/serialize.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transaction/serialize.rs#L6) · line 6 · SHA-256 89eb454cabb9555d702bf81f201bfbedaed739a5c891ded0e6de215085f3d123_

```
    5 | 
    6 | use halo2::pasta::{group::ff::PrimeField, pallas};
    7 | use hex::FromHex;
```

_file_excerpt · [zebra-chain/src/transaction/serialize.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transaction/serialize.rs#L25) · line 25 · SHA-256 f0922cf27393c471f87082b31d4518fb9fd4d85160bcd5867a35e27054489f30_

```
   24 |     amount, ironwood, orchard,
   25 |     primitives::Halo2Proof,
   26 |     sapling,
```

_file_excerpt · [zebra-chain/src/transaction/serialize.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transaction/serialize.rs#L657) · line 657 · SHA-256 f202e314ccd0b908398ce33bacd115a6c2e9881131d6ee7b33dad51daf328f64_

```
  656 |     // https://zips.z.cash/protocol/protocol.pdf#halo2encoding
  657 |     let proof: Halo2Proof = (&mut reader).zcash_deserialize_into()?;
  658 | 
```

_file_excerpt · [zebra-consensus/src/transaction.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-consensus/src/transaction.rs#L1436) · line 1436 · SHA-256 3655d7e12a53e45280e92591d9fcdde298488e391eb653c1c082bcc50b5319c8_

```
 1435 |     queue_orchard_bundle(
 1436 |         || primitives::halo2::cached_orchard_v5_verifier_for(network_upgrade),
 1437 |         bundle,
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07358 — Квантово-уязвимый RedDSA: подпись транзакций и сообщений (3 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:RedDSA:transaction_signing`
- Источник данных: zebra-chain/src/transaction/arbitrary.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

6 упоминаний RedDSA в 3 файл(ах), например zebra-chain/src/transaction/arbitrary.rs:16. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте zebra-chain/src/transaction/arbitrary.rs:16 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [zebra-chain/src/transaction/arbitrary.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transaction/arbitrary.rs#L16) · line 16 · SHA-256 14fb1e83c0850cdff4bcaa4ed51bd8127eee8188f0a0c409f8ff82eaf7811b5f_

```
   15 | use proptest::{array, collection::vec, option, prelude::*};
   16 | use reddsa::{orchard::Binding, Signature};
   17 | 
```

_file_excerpt · [zebra-chain/src/transaction/arbitrary/shielded.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transaction/arbitrary/shielded.rs#L60) · line 60 · SHA-256 9e9556eb1c075707348f12dc9376cb21d3228980eac5a34d46f86db365aa7da4_

```
   59 |     let sk_bytes = scalar_from_seed(seed).to_repr();
   60 |     let sk = reddsa::SigningKey::<reddsa::orchard::SpendAuth>::from_bytes(&sk_bytes)
   61 |         .expect("a canonical scalar is a valid signing key");
```

_file_excerpt · [zebra-chain/src/transaction/arbitrary/shielded.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transaction/arbitrary/shielded.rs#L62) · line 62 · SHA-256 953f972dcd8576796d134435f501c55ff678f7173bd86787614e01b43c882408_

```
   61 |         .expect("a canonical scalar is a valid signing key");
   62 |     let pk_bytes: [u8; 32] = reddsa::VerificationKey::from(&sk).into();
   63 | 
```

_file_excerpt · [zebra-chain/src/transaction/serialize.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transaction/serialize.rs#L33) · line 33 · SHA-256 c456d56f57bf7875db3002833cf9b0fb22583e23d4965e87a39efe47dc77eee4_

```
   32 | #[cfg(any(test, feature = "proptest-impl"))]
   33 | use reddsa::{orchard::Binding, orchard::SpendAuth, Signature};
   34 | 
```

_file_excerpt · [zebra-chain/src/transaction/serialize.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transaction/serialize.rs#L691) · line 691 · SHA-256 4cf81900a9b2c9848d998c66036024024bf094c7ecc7549f585af410dc97e631_

```
  690 | 
  691 | impl<T: reddsa::SigType> ZcashSerialize for reddsa::Signature<T> {
  692 |     fn zcash_serialize<W: io::Write>(&self, mut writer: W) -> Result<(), io::Error> {
```

_file_excerpt · [zebra-chain/src/transaction/serialize.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transaction/serialize.rs#L698) · line 698 · SHA-256 1daeeeed5e587757293b12574738781592e8c7f6d8cd8f68dd544dc998e71366_

```
  697 | 
  698 | impl<T: reddsa::SigType> ZcashDeserialize for reddsa::Signature<T> {
  699 |     fn zcash_deserialize<R: io::Read>(mut reader: R) -> Result<Self, SerializationError> {
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07359 — Квантово-уязвимый Ed25519: подпись транзакций и сообщений (3 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Ed25519:transaction_signing`
- Источник данных: zebra-chain/src/transaction/joinsplit.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

3 упоминаний Ed25519 в 3 файл(ах), например zebra-chain/src/transaction/joinsplit.rs:49. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте zebra-chain/src/transaction/joinsplit.rs:49 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [zebra-chain/src/transaction/joinsplit.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transaction/joinsplit.rs#L49) · line 49 · SHA-256 7b5f18c28d4b4cf995c8c645d6699ea435fc2e3771326fafe98976648f3dc02c_

```
   48 |     /// The JoinSplit signature, denoted as `joinSplitSig` in the spec.
   49 |     pub sig: ed25519::Signature,
   50 | }
```

_file_excerpt · [zebra-consensus/src/transaction.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-consensus/src/transaction.rs#L1340) · line 1340 · SHA-256 c5cd881930df105bad00840a473fa63cec1e81b86bb4c8096b356109c586ef9f_

```
 1339 |         );
 1340 |         let sig = zebra_chain::primitives::ed25519::Signature::from(sprout_bundle.joinsplit_sig);
 1341 |         let ed25519_item = (pub_key, sig, shielded_sighash).into();
```

_file_excerpt · [zebra-rpc/src/methods/types/transaction.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-rpc/src/methods/types/transaction.rs#L380) · line 380 · SHA-256 ad4a7b87509a64c51a6849f560fe90747a31fde83bee6d59e22d8cff6b3eb64e_

```
  379 |     #[getter(copy)]
  380 |     pub(crate) joinsplit_sig: Option<[u8; ed25519::Signature::BYTE_SIZE]>,
  381 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07352 — Квантово-уязвимый Halo 2 (IPA): роль не определена (17 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Halo 2 (IPA):general`
- Источник данных: zebra-chain/src/amount.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

32 упоминаний Halo 2 (IPA) в 17 файл(ах), например zebra-chain/src/amount.rs:264. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте zebra-chain/src/amount.rs:264 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [zebra-chain/src/amount.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/amount.rs#L264) · line 264 · SHA-256 0f499c9032c128f4ac0e8f0bc2eacb60034977b1a442f1a28245d974e3c61e74_

```
  263 | 
  264 | impl<C> From<Amount<C>> for halo2::pasta::pallas::Scalar {
  265 |     fn from(a: Amount<C>) -> halo2::pasta::pallas::Scalar {
```

_file_excerpt · [zebra-chain/src/amount.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/amount.rs#L265) · line 265 · SHA-256 c137fa530a8a9e88261a37c65bf44d08350e20ab5649205ae1a44a6523a98517_

```
  264 | impl<C> From<Amount<C>> for halo2::pasta::pallas::Scalar {
  265 |     fn from(a: Amount<C>) -> halo2::pasta::pallas::Scalar {
  266 |         // TODO: this isn't constant time -- does that matter?
```

_file_excerpt · [zebra-chain/src/amount.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/amount.rs#L273) · line 273 · SHA-256 e0dce8b5041ea8280d5b5e775e7661462617916cb277ab9dbfb72ac62262f9bf_

```
  272 | 
  273 |             halo2::pasta::pallas::Scalar::from(abs_amount).neg()
  274 |         } else {
```

_file_excerpt · [zebra-chain/src/block.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/block.rs#L5) · line 5 · SHA-256 eb4e5e9b7b24d0c980195d6f122583c83f067c0bb10274f47bfe589303e4114a_

```
    4 | 
    5 | use halo2::pasta::{group::ff::PrimeField, pallas};
    6 | 
```

_file_excerpt · [zebra-chain/src/block/arbitrary.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/block/arbitrary.rs#L492) · line 492 · SHA-256 8a41c9cdc06dbfa4a8ef5e7ecd09e446a62e548a27965c4f0a9421ab7d435fd6_

```
  491 |                             for orchard_note_commitment in transaction.orchard_note_commitments() {
  492 |                                 use halo2::pasta::group::ff::PrimeField;
  493 |                                 let cm =
```

_file_excerpt · [zebra-chain/src/block/arbitrary.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/block/arbitrary.rs#L500) · line 500 · SHA-256 ad6311b9b3237b7c651149259b770a03746022a64a10f31589ab2f50e6c49578_

```
  499 |                             {
  500 |                                 use halo2::pasta::group::ff::PrimeField;
  501 |                                 let cm =
```

_file_excerpt · [zebra-chain/src/orchard/action.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/action.rs#L3) · line 3 · SHA-256 e97967ce213a5d55c7e7d018a23b72bdd98520e92cf30ccd33e1458d2054d81c_

```
    2 | 
    3 | use halo2::pasta::pallas;
    4 | use reddsa::orchard::SpendAuth;
```

_file_excerpt · [zebra-chain/src/orchard/arbitrary.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/arbitrary.rs#L7) · line 7 · SHA-256 a98ae52f00d0d763d02b607e03ab85354a3b5ab4dbabdd655e98061a2e198947_

```
    6 | };
    7 | use halo2::pasta::pallas;
    8 | use reddsa::{orchard::SpendAuth, Signature, SigningKey, VerificationKey, VerificationKeyBytes};
```

_file_excerpt · [zebra-chain/src/orchard/commitment.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/commitment.rs#L9) · line 9 · SHA-256 c21ce720a70617f6374576d5f00e60f395e2291b8583ddff9c39d22857b8e658_

```
    8 | };
    9 | use halo2::{
   10 |     arithmetic::{Coordinates, CurveAffine},
```

_file_excerpt · [zebra-chain/src/orchard/keys.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/keys.rs#L10) · line 10 · SHA-256 79749f287d5681d4019f20674ea4752cf8c60e5a0d616eb696c31113050d9f45_

```
    9 | use group::{ff::PrimeField, CurveAffine as _, Group, GroupEncoding};
   10 | use halo2::{
   11 |     arithmetic::{Coordinates, CurveAffine},
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07354 — Квантово-уязвимый Sinsemilla: роль не определена (6 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Sinsemilla:general`
- Источник данных: zebra-chain/src/orchard.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

8 упоминаний Sinsemilla в 6 файл(ах), например zebra-chain/src/orchard.rs:9. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте zebra-chain/src/orchard.rs:9 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [zebra-chain/src/orchard.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard.rs#L9) · line 9 · SHA-256 3b67ef923d961149efb00f6ae9dbe804ab39b415d63f7fc31456b54350dac30f_

```
    8 | mod note;
    9 | mod sinsemilla;
   10 | 
```

_file_excerpt · [zebra-chain/src/orchard/commitment.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/commitment.rs#L24) · line 24 · SHA-256 759614e46c59a32604ca466c4fdf33c7380c57380f0ee6faa3ff4ff03121df17_

```
   23 | 
   24 | use super::sinsemilla::*;
   25 | 
```

_file_excerpt · [zebra-chain/src/orchard/keys.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/keys.rs#L23) · line 23 · SHA-256 d8c680a1ef1dba8520e3471fa7e16fe8eafdbe47341e52fa779e06707478c8f9_

```
   22 | 
   23 | use super::sinsemilla::*;
   24 | 
```

_file_excerpt · [zebra-chain/src/orchard/note.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/note.rs#L12) · line 12 · SHA-256 2a9b89642610ce16b99f2c49d1a6ac3a26812553854fd4db8e87b86d1eb4db2a_

```
   11 | 
   12 | use super::{address::Address, sinsemilla::extract_p};
   13 | 
```

_file_excerpt · [zebra-chain/src/orchard/sinsemilla.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/sinsemilla.rs#L8) · line 8 · SHA-256 ebba5b336aa1193eee04cf9385b4382b89726b4d996d257f3cc903a3110dd87a_

```
    7 | };
    8 | use sinsemilla::HashDomain;
    9 | 
```

_file_excerpt · [zebra-chain/src/orchard/sinsemilla.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/sinsemilla.rs#L56) · line 56 · SHA-256 0b729075d003b23bf83db693195bdc10ecadd9f6a5ea735febd02f98de9a09b2_

```
   55 | #[allow(non_snake_case)]
   56 | pub fn sinsemilla_hash(D: &[u8], M: &BitVec<u8, Lsb0>) -> Option<pallas::Base> {
   57 |     let domain = std::str::from_utf8(D).expect("must be valid UTF-8");
```

_file_excerpt · [zebra-chain/src/orchard/tree.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/tree.rs#L28) · line 28 · SHA-256 ff1093e3202ecaa0751fa2beaa039f6f853311b18224a7d7257b8ca0ca9fe750_

```
   27 | 
   28 | use super::sinsemilla::*;
   29 | 
```

_file_excerpt · [zebra-chain/src/orchard/tree.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/tree.rs#L70) · line 70 · SHA-256 ba679fb73afb557b58362e64580a98bc4240d594d40fe31436b0d158a10b87f9_

```
   69 | 
   70 |     match sinsemilla_hash(b"z.cash:Orchard-MerkleCRH", &s) {
   71 |         Some(h) => h,
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07355 — Квантово-уязвимый RedDSA: роль не определена (5 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:RedDSA:general`
- Источник данных: zebra-chain/src/orchard/action.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

13 упоминаний RedDSA в 5 файл(ах), например zebra-chain/src/orchard/action.rs:4. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте zebra-chain/src/orchard/action.rs:4 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [zebra-chain/src/orchard/action.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/action.rs#L4) · line 4 · SHA-256 e2c48f0e724b34c8f8ab0872b5c5ed671fe2af526f04c78ca72682a63cab9fc5_

```
    3 | use halo2::pasta::pallas;
    4 | use reddsa::orchard::SpendAuth;
    5 | 
```

_file_excerpt · [zebra-chain/src/orchard/action.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/action.rs#L30) · line 30 · SHA-256 77e3131a65f5bc2d4cc1ac6fa8f6cc6e73668f652359dc4c5ad74c499b559f09_

```
   29 |     /// The randomized validating key for spendAuthSig,
   30 |     pub rk: reddsa::VerificationKeyBytes<SpendAuth>,
   31 |     /// The x-coordinate of the note commitment for the output note.
```

_file_excerpt · [zebra-chain/src/orchard/arbitrary.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/arbitrary.rs#L8) · line 8 · SHA-256 5f29a767440e7d72f55106e4e8de16a27d0144668635ebc29595eeed8f28d792_

```
    7 | use halo2::pasta::pallas;
    8 | use reddsa::{orchard::SpendAuth, Signature, SigningKey, VerificationKey, VerificationKeyBytes};
    9 | 
```

_file_excerpt · [zebra-chain/src/orchard/shielded_data.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/shielded_data.rs#L11) · line 11 · SHA-256 3d3c73ed944bd7739526c51a997b8ca2d31189b699f00a4872118bcd683f13a2_

```
   10 | use halo2::pasta::pallas;
   11 | use reddsa::{orchard::Binding, orchard::SpendAuth, Signature};
   12 | 
```

_file_excerpt · [zebra-chain/src/orchard/shielded_data.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/orchard/shielded_data.rs#L155) · line 155 · SHA-256 6518bd553df49ab1982de0bfbe4f911e36c5f3f8ffbede5de7504f8b00dd304e_

```
  154 |     /// <https://zips.z.cash/protocol/protocol.pdf#orchardbalance>
  155 |     pub fn binding_verification_key(&self) -> reddsa::VerificationKeyBytes<Binding> {
  156 |         let cv: ValueCommitment = self.actions().map(|action| action.cv).sum();
```

_file_excerpt · [zebra-consensus/src/error.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-consensus/src/error.rs#L161) · line 161 · SHA-256 49dad86aeb537aaef8e7dac418ce302a67a21d1c8d976bdf333e7987004a0ca1_

```
  160 |     #[cfg_attr(any(test, feature = "proptest-impl"), proptest(skip))]
  161 |     RedJubjub(zebra_chain::primitives::redjubjub::Error),
  162 | 
```

_file_excerpt · [zebra-consensus/src/error.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-consensus/src/error.rs#L165) · line 165 · SHA-256 0636f9ee2617c92cf51606927211bda1df10df6e2cfeb9b9c69e872804642678_

```
  164 |     #[cfg_attr(any(test, feature = "proptest-impl"), proptest(skip))]
  165 |     RedPallas(zebra_chain::primitives::reddsa::Error),
  166 | 
```

_file_excerpt · [zebra-consensus/src/error.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-consensus/src/error.rs#L377) · line 377 · SHA-256 e5672ad6ec7127e2f464a40145220e4087d37a6b5ddb34c5b987eb5b44897144_

```
  376 |         match err.downcast::<zebra_chain::primitives::redjubjub::Error>() {
  377 |             Ok(e) => return TransactionError::RedJubjub(*e),
  378 |             Err(e) => err = e,
```

_file_excerpt · [zebra-consensus/src/primitives/redpallas.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-consensus/src/primitives/redpallas.rs#L18) · line 18 · SHA-256 cab621136d5932e1ce3fa2d608672e03e9a2267d02a669e4ffb39919d932eabe_

```
   17 | 
   18 | use zebra_chain::primitives::reddsa::{batch, orchard, Error, Signature, VerificationKeyBytes};
   19 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07356 — Квантово-уязвимый X25519: роль не определена (3 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:X25519:general`
- Источник данных: zebra-chain/src/primitives.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

6 упоминаний X25519 в 3 файл(ах), например zebra-chain/src/primitives.rs:18. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте zebra-chain/src/primitives.rs:18 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [zebra-chain/src/primitives.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/primitives.rs#L18) · line 18 · SHA-256 891112a1f260bc480aedb877c789e052eb787dd7a112114ee4a3e84515a363c3_

```
   17 | pub use redjubjub;
   18 | pub use x25519_dalek as x25519;
   19 | 
```

_file_excerpt · [zebra-chain/src/sprout/arbitrary.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/sprout/arbitrary.rs#L45) · line 45 · SHA-256 6cca04a7b460f9f82202ad7ad023ebc45568a78ab720f6ad0d67cbbfcdceb1b9_

```
   44 |                         commitments,
   45 |                         ephemeral_key: x25519_dalek::PublicKey::from(ephemeral_key_bytes),
   46 |                         random_seed,
```

_file_excerpt · [zebra-chain/src/sprout/joinsplit.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/sprout/joinsplit.rs#L11) · line 11 · SHA-256 04fa2797580674ce63171073ee35b73933dbee77849cf3418329cec5339caaaa_

```
   10 |     fmt::HexDebug,
   11 |     primitives::{x25519, Bctv14Proof, Groth16Proof, ZkSnarkProof},
   12 |     serialization::{
```

_file_excerpt · [zebra-chain/src/sprout/joinsplit.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/sprout/joinsplit.rs#L79) · line 79 · SHA-256 f6084a25657a411e99c200c5a6172e4c4dcc30f2a2bece2efc2ba74e614b0e5b_

```
   78 |     /// An X25519 public key.
   79 |     pub ephemeral_key: x25519::PublicKey,
   80 |     /// A 256-bit seed that must be chosen independently at random for each
```

_file_excerpt · [zebra-chain/src/sprout/joinsplit.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/sprout/joinsplit.rs#L112) · line 112 · SHA-256 ed85f11f64c582dc33a2adabf9830c2e07e0075ff6d95e607338500956ae1868_

```
  111 |     /// An X25519 public key.
  112 |     pub ephemeral_key: x25519::PublicKey,
  113 |     /// A 256-bit seed that must be chosen independently at random for each
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07360 — Квантово-уязвимый ECDSA: роль не определена (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: zebra-chain/src/transparent/keys.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

2 упоминаний ECDSA в 1 файл(ах), например zebra-chain/src/transparent/keys.rs:8. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте zebra-chain/src/transparent/keys.rs:8 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [zebra-chain/src/transparent/keys.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transparent/keys.rs#L8) · line 8 · SHA-256 e6db1fc498541110585d827e4bac54be3b4b372fdaeff6e13618a2acdab2c3fb_

```
    7 | 
    8 | use secp256k1::PublicKey;
    9 | 
```

_file_excerpt · [zebra-chain/src/transparent/keys.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-chain/src/transparent/keys.rs#L24) · line 24 · SHA-256 d97661ad177e37ab994807da754d0fe72a88b080e505a55e17bef046f02558a5_

```
   23 |         Self::from_slice(&bytes[..])
   24 |             .map_err(|_| SerializationError::Parse("invalid secp256k1 compressed public key"))
   25 |     }
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07361 — Квантово-уязвимый BLS12-381: роль не определена (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:BLS12-381:general`
- Источник данных: zebra-consensus/src/primitives/groth16.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

2 упоминаний BLS12-381 в 2 файл(ах), например zebra-consensus/src/primitives/groth16.rs:6. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте zebra-consensus/src/primitives/groth16.rs:6 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [zebra-consensus/src/primitives/groth16.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-consensus/src/primitives/groth16.rs#L6) · line 6 · SHA-256 9c7451fbee4e424ccf8cc8e4eab9f659bc9f37487c42750508c0b205aff30493_

```
    5 | use bellman::{gadgets::multipack, VerificationError};
    6 | use bls12_381::Bls12;
    7 | use futures::{future::BoxFuture, FutureExt};
```

_file_excerpt · [zebra-consensus/src/primitives/groth16/params.rs](https://github.com/ZcashFoundation/zebra/blob/147a6a8bf7d3b1427a9c0557f284d5bfa7b0e522/zebra-consensus/src/primitives/groth16/params.rs#L3) · line 3 · SHA-256 5e29d8128b44e2bb4efd6dc475ca29362aab72f84889d77e9d20bdf3b044b441_

```
    2 | 
    3 | use bls12_381::Bls12;
    4 | use derive_getters::Getters;
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07364 — block-buffer 0.10.4 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/block-buffer@0.10.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 33.1 / 100
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

### QSI-2026-07365 — libz-sys 1.1.28 затронут RUSTSEC-2026-0418 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/libz-sys@1.1.28`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0418 для пакета crates.io libz-sys версии 1.1.28: libz-sys build script leaks environment variables in the build directory. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07369 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0338 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
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

### QSI-2026-07370 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0339 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
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

### QSI-2026-07373 — quinn-proto 0.11.16 затронут RUSTSEC-2026-0342 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/quinn-proto@0.11.16`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
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

### QSI-2026-07375 — webpki-root-certs 1.0.7 затронут RUSTSEC-2026-0383 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/webpki-root-certs@1.0.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0383 (CVE-2026-111943) для пакета crates.io webpki-root-certs версии 1.0.7: Bundled root certificates allow trust in distrusted emSign intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0383
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0383](https://osv.dev/vulnerability/RUSTSEC-2026-0383) · manifest · SHA-256 3246026933edff30d4662b8425596fe73691a2ab5c886d1d7d3a6808822713fb_

```
{"id": "RUSTSEC-2026-0383", "aliases": ["BIT-golang-2026-111943", "CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0381", "RUSTSEC-2026-0382"], "modified": "2026-10-29T10:55:54.096394276Z", "summary": "Bundled root certificates allow trust in distrusted emSign intermediates", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.26.11, 1.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07363 — bincode 1.3.3: информационный бюллетень RUSTSEC-2025-0141 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
- Затронутый актив: `dependency:crates.io/bincode@1.3.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
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

### QSI-2026-07374 — tokio 1.52.1 затронут RUSTSEC-2026-0386 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/tokio@1.52.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0386 для пакета crates.io tokio версии 1.52.1: `AsyncFd::new` and related constructors violate I/O safety. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни одна из затронутых функций (tokio::io::unix::AsyncFd::new, tokio::io::unix::AsyncFd::try_new, tokio::io::unix::AsyncFd::try_with_interest, tokio::io::unix::AsyncFd::with_interest) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

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

### QSI-2026-07376 — 3 бюллетеней в 2 пакет(ах) crates.io, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:crates.io:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 15.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 3 бюллетеней (1 с оценкой high или critical) для 2 пакет(ов) crates.io, которые подтягивают только инструменты разработки или сборки (Cargo.lock): например, git2@0.20.4 [build]: RUSTSEC-2026-0183, RUSTSEC-2026-0184; pulldown-cmark@0.13.3 [build]: RUSTSEC-2026-0414. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в Cargo.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (crates.io)](https://osv.dev/) · Cargo.lock · SHA-256 ef4e8ed1d4a904a99effd30e97246700ef1f5b6684029bd2111f907ae591afcc_

```
git2@0.20.4 [build]: RUSTSEC-2026-0183, RUSTSEC-2026-0184
pulldown-cmark@0.13.3 [build]: RUSTSEC-2026-0414
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07362 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 13.3 / 100
- CVSS v3.1: неприменимо

В 13 манифестах зависимостей QSI нашёл криптобиблиотеки (bellman, bls12_381, curve25519-dalek, ff, group, halo2, halo2_gadgets, halo2_poseidon, halo2_proofs, jubjub, orchard, pasta_curves, reddsa, redjubjub, ring), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · Cargo.lock, Cargo.toml, tower-batch-control/Cargo.toml, tower-fallback/Cargo.toml, zebra-chain/Cargo.toml, zebra-consensus/Cargo.toml, zebra-network/Cargo.toml, zebra-node-services/Cargo.toml, zebra-rpc/Cargo.toml, zebra-script/Cargo.toml, zebra-state/Cargo.toml, zebra-utils/Cargo.toml, zebrad/Cargo.toml · SHA-256 d087fd86fa294e82d9381ade65c78545fe4fd99b0af163dbc8ba8273327b8a93_

```
Crypto libraries: bellman, bls12_381, curve25519-dalek, ff, group, halo2, halo2_gadgets, halo2_poseidon, halo2_proofs, jubjub, orchard, pasta_curves, reddsa, redjubjub, ring, rustls, sapling-crypto, secp256k1, sinsemilla, x25519-dalek, zcash_keys, zcash_note_encryption, zcash_primitives, zcash_proofs, zcash_protocol, zcash_spec, zip32
```

**Ограничения проверки.** Отсутствие доказательств не является доказательством отсутствия: системные библиотеки и транзитивные зависимости могут не указываться.

**Рекомендация.** Определите источник поддержки PQC (TLS-терминатор, KMS/HSM, обновление библиотек).

**Повторная проверка.** Повторите сканирование после обновлений.

### QSI-2026-07366 — number_prefix 0.4.0: информационный бюллетень RUSTSEC-2025-0119 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/number_prefix@0.4.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
- Балл приоритета: 11.8 / 100
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

### QSI-2026-07368 — proc-macro-error2 2.0.1: информационный бюллетень RUSTSEC-2026-0173 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/proc-macro-error2@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:49 UTC
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
| QSI-2026-07351 | Некриптографический ГСЧ рядом с чувствительными идентификаторами в book/mermaid.min.js | book/mermaid.min.js is the minified Mermaid diagram library bundled into the mdBook documentation output. It is third-party code vendored for rendering docs, never runs in the node, and the Math.random calls are Mermaid's own layout code rather than anything security-sensitive in Zebra. |

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
| **пороговая подпись и протоколы MPC** | Pedersen commitment (12) | QSI-2026-07353 | Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли |
| **подпись транзакций и сообщений** | Halo 2 (IPA) (5), Ed25519 (3), RedDSA (3) | QSI-2026-07357, QSI-2026-07358, QSI-2026-07359 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |
| **роль не определена** | Halo 2 (IPA) (17), Sinsemilla (6), RedDSA (5), X25519 (3), BLS12-381 (2), ECDSA (1) | QSI-2026-07352, QSI-2026-07354, QSI-2026-07355, QSI-2026-07356, QSI-2026-07360, QSI-2026-07361 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм в конечных полях | взламывает | Q1 | BLS12-381 (2), Groth16 (2) | Взламывает Диффи–Хеллмана в конечных полях и DSA при любом размере. Переводите установление ключей на ML-KEM (на переходный период — гибрид с X25519 или ECDH), подписи — на ML-DSA или SLH-DSA. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | BLS12-381 (2), ECDSA (1), Ed25519 (5), Groth16 (2), Halo 2 (IPA) (22), Pedersen commitment (12), RedDSA (11), Sinsemilla (6), X25519 (4) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | SHA-2 (3) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | SHA-2 (3) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- keys: SECURITY.md line 70: OpenPGP algorithm ID 18 is not in the algorithm registry

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-07371 | Обновите quinn-proto до исправленной версии (0.11.18). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2026-0340. |
| P2 | QSI-2026-07372 | Обновите quinn-proto до исправленной версии (0.11.17). | устранение первопричины | Сканирование зависимостей больше не сообщает RUSTSEC-2026-0341. |
| P2 | QSI-2026-07367 | Обновите opentelemetry_sdk до исправленной версии (0.32.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w9wp-h8wv-79jx (CVE-2026-48504). |
| P2 | QSI-2026-07364 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-07365 | Разберите RUSTSEC-2026-0418; при необходимости обновите libz-sys до исправленной версии (1.1.31). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0418 или результат разбора записан. |
| P3 | QSI-2026-07369 | Разберите RUSTSEC-2026-0338; при необходимости обновите quinn-proto до исправленной версии (0.11.18). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0338 или результат разбора записан. |
| P3 | QSI-2026-07370 | Разберите RUSTSEC-2026-0339; при необходимости обновите quinn-proto до исправленной версии (0.11.17). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0339 или результат разбора записан. |
| P3 | QSI-2026-07373 | Разберите RUSTSEC-2026-0342; при необходимости обновите quinn-proto до исправленной версии (0.11.17). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0342 или результат разбора записан. |
| P3 | QSI-2026-07375 | Разберите RUSTSEC-2026-0383 (CVE-2026-111943); при необходимости обновите webpki-root-certs до исправленной версии (0.26.11, 1.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0383 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-07374 | Разберите RUSTSEC-2026-0386; при необходимости обновите tokio до исправленной версии (1.51.6, 1.53.3). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0386 или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-07350 | Внесите использования Ed25519 в file:SECURITY.md в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07353 | Внесите использования Pedersen commitment в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07357 | Внесите использования Halo 2 (IPA) в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07358 | Внесите использования RedDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07359 | Внесите использования Ed25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07352 | Внесите использования Halo 2 (IPA) в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07354 | Внесите использования Sinsemilla в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07355 | Внесите использования RedDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07356 | Внесите использования X25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07360 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07361 | Внесите использования BLS12-381 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-07350 | Запланируйте миграцию Ed25519 на ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it. или гибридной схемы. |
| P4 | QSI-2026-07353 | Запланируйте миграцию Pedersen commitment на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07357 | Запланируйте миграцию Halo 2 (IPA) на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07358 | Запланируйте миграцию RedDSA на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07359 | Запланируйте миграцию Ed25519 на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-07352 | Запланируйте миграцию Halo 2 (IPA) на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07354 | Запланируйте миграцию Sinsemilla на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07355 | Запланируйте миграцию RedDSA на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07356 | Запланируйте миграцию X25519 на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-07360 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-07361 | Запланируйте миграцию BLS12-381 на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07363 | Замените bincode поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | bincode заменён или решение зафиксировано. |
| P4 | QSI-2026-07376 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |
| P4 | QSI-2026-07366 | Замените number_prefix поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | number_prefix заменён или решение зафиксировано. |
| P4 | QSI-2026-07368 | Замените proc-macro-error2 поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | proc-macro-error2 заменён или решение зафиксировано. |

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
22. OSV advisory GHSA-w9wp-h8wv-79jx — OSV.dev. <https://osv.dev/vulnerability/GHSA-w9wp-h8wv-79jx> (modified 2026-09-10T03:50:50.807599062Z)
23. OSV advisory RUSTSEC-2025-0119 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0119> (modified 2025-11-18T08:13:56Z)
24. OSV advisory RUSTSEC-2025-0141 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0141> (modified 2026-01-16T11:07:28.867553Z)
25. OSV advisory RUSTSEC-2026-0173 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0173> (modified 2026-06-07T21:00:04.318567692Z)
26. OSV advisory RUSTSEC-2026-0338 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0338> (modified 2026-10-12T18:15:01.969514645Z)
27. OSV advisory RUSTSEC-2026-0339 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0339> (modified 2026-10-12T18:15:01.956822776Z)
28. OSV advisory RUSTSEC-2026-0340 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0340> (modified 2026-10-12T18:15:01.975478256Z)
29. OSV advisory RUSTSEC-2026-0341 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0341> (modified 2026-10-12T18:15:01.969505433Z)
30. OSV advisory RUSTSEC-2026-0342 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0342> (modified 2026-10-12T18:15:01.956681478Z)
31. OSV advisory RUSTSEC-2026-0383 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0383> (modified 2026-10-29T10:55:54.096394276Z)
32. OSV advisory RUSTSEC-2026-0386 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0386> (modified 2026-10-23T14:45:03.847864944Z)
33. OSV advisory RUSTSEC-2026-0418 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0418> (modified 2026-10-29T14:15:02.333141406Z)
34. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
35. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
36. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
37. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| SHA-2 | SHA-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 3 | 3 | zebra-chain/src/serialization/sha256d.rs:17; zebra-chain/src/sprout/commitment.rs:53; zebrad/src/components/zcashd_compat/managed.rs:424 |
| Crypto library | 0.11.0 | zcash_protocol (Zcash protocol crates) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.11.1 | jubjub (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | group (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | ff (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.15.0 | bellman (bellman) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.16.0 | orchard (Zcash protocol crates) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.17.0 | zcash_keys (Zcash protocol crates) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.17.14 | ring (ring (Rust)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.2.0 | halo2_poseidon (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.2.0 | sinsemilla (sinsemilla) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.2.1 | zcash_spec (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.23.46 | rustls (rustls) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.3.0 | zip32 (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.31.0 | zcash_proofs (Zcash protocol crates) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.31.0 | zcash_primitives (Zcash protocol crates) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.33.1 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.4.0 | halo2_proofs (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.5.1 | zcash_note_encryption (Zcash protocol crates) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.6.0 | halo2_gadgets (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.6.1 | reddsa (reddsa) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.6.1 | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.9.0 | bls12_381 (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.9.0 | redjubjub (reddsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.9.0 | sapling-crypto (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 3.0.0 | x25519-dalek (ed25519-dalek) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 5.0.0 | curve25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.11 | jubjub (jubjub) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.14 | group (jubjub) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.14 | ff (jubjub) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.15 | bellman (bellman) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.2 | sinsemilla (sinsemilla) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.3 | zip32 (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.33 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.4 | halo2 (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.9 | sapling-crypto (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.9 | redjubjub (reddsa) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.9 | bls12_381 (jubjub) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.4 | halo2_proofs (halo2 (Zcash)) | н/п | допустимо | 3 | 3 | zebra-chain/Cargo.toml; zebra-consensus/Cargo.toml; zebra-state/Cargo.toml |
| Crypto library | workspace | orchard (Zcash protocol crates) | н/п | допустимо | 3 | 3 | zebra-chain/Cargo.toml; zebra-consensus/Cargo.toml; zebra-rpc/Cargo.toml |
| Crypto library | workspace | x25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | zebra-chain/Cargo.toml |
| Crypto library | workspace | zcash_primitives (Zcash protocol crates) | н/п | допустимо | 5 | 5 | zebra-chain/Cargo.toml; zebra-consensus/Cargo.toml; zebra-rpc/Cargo.toml |
| Crypto library | workspace | redjubjub (reddsa) | н/п | допустимо | 1 | 1 | zebra-chain/Cargo.toml |
| Crypto library | workspace | sinsemilla (sinsemilla) | н/п | допустимо | 1 | 1 | zebra-chain/Cargo.toml |
| Crypto library | workspace | sapling-crypto (Zcash protocol crates) | н/п | допустимо | 4 | 4 | zebra-chain/Cargo.toml; zebra-consensus/Cargo.toml; zebra-rpc/Cargo.toml |
| Crypto library | workspace | jubjub (jubjub) | н/п | допустимо | 3 | 3 | zebra-chain/Cargo.toml; zebra-consensus/Cargo.toml; zebra-state/Cargo.toml |
| Crypto library | workspace | group (jubjub) | н/п | допустимо | 1 | 1 | zebra-chain/Cargo.toml |
| Crypto library | workspace | reddsa (reddsa) | н/п | допустимо | 1 | 1 | zebra-chain/Cargo.toml |
| Crypto library | workspace | zcash_protocol (Zcash protocol crates) | н/п | допустимо | 4 | 4 | zebra-chain/Cargo.toml; zebra-consensus/Cargo.toml; zebra-rpc/Cargo.toml |
| Crypto library | workspace | zcash_note_encryption (Zcash protocol crates) | н/п | допустимо | 1 | 1 | zebra-chain/Cargo.toml |
| Crypto library | workspace | secp256k1 (secp256k1 bindings) | н/п | допустимо | 2 | 2 | zebra-chain/Cargo.toml; zebra-script/Cargo.toml |
| Crypto library | workspace | bellman (bellman) | н/п | допустимо | 1 | 1 | zebra-consensus/Cargo.toml |
| Crypto library | workspace | zcash_proofs (Zcash protocol crates) | н/п | допустимо | 1 | 1 | zebra-consensus/Cargo.toml |
| Crypto library | workspace | bls12_381 (jubjub) | н/п | допустимо | 1 | 1 | zebra-consensus/Cargo.toml |
| Crypto library | workspace | zcash_keys (Zcash protocol crates) | н/п | допустимо | 2 | 2 | zebra-rpc/Cargo.toml; zebrad/Cargo.toml |
| BLS12-381 |  |  | уязвим (Шор) | допустимо | 2 | 2 | zebra-consensus/src/primitives/groth16.rs:6; zebra-consensus/src/primitives/groth16/params.rs:3 |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 1 | 1 | zebra-chain/src/transparent/keys.rs:8 |
| Ed25519 | Ed25519 |  | уязвим (Шор) | допустимо | 5 | 5 | SECURITY.md (line 70); zebra-chain/src/transaction/joinsplit.rs:49; zebra-consensus/src/primitives/ed25519.rs |
| Groth16 |  |  | уязвим (Шор) | допустимо | 2 | 2 | zebra-chain/src/primitives/proofs/groth16.rs; zebra-consensus/src/primitives/groth16.rs |
| Halo 2 (IPA) |  |  | уязвим (Шор) | допустимо | 22 | 22 | zebra-chain/src/amount.rs:264; zebra-chain/src/block.rs:5; zebra-chain/src/block/arbitrary.rs:492 |
| Pedersen commitment |  |  | уязвим (Шор) | допустимо | 12 | 12 | zebra-chain/src/orchard.rs:22; zebra-chain/src/orchard/action.rs:11; zebra-chain/src/orchard/arbitrary.rs:13 |
| RedDSA |  |  | уязвим (Шор) | допустимо | 8 | 8 | zebra-chain/src/orchard/action.rs:4; zebra-chain/src/orchard/arbitrary.rs:8; zebra-chain/src/orchard/shielded_data.rs:11 |
| RedDSA | RedJubjub |  | уязвим (Шор) | допустимо | 2 | 2 | zebra-consensus/src/error.rs:161; zebra-consensus/src/primitives/redjubjub.rs |
| RedDSA | RedPallas |  | уязвим (Шор) | допустимо | 1 | 1 | zebra-consensus/src/error.rs:165 |
| Sinsemilla |  |  | уязвим (Шор) | допустимо | 6 | 6 | zebra-chain/src/orchard.rs:9; zebra-chain/src/orchard/commitment.rs:24; zebra-chain/src/orchard/keys.rs:23 |
| X25519 | X25519 |  | уязвим (Шор) | допустимо | 4 | 4 | zebra-chain/src/primitives.rs:18; zebra-chain/src/sprout/arbitrary.rs:45; zebra-chain/src/sprout/joinsplit.rs:11 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| .cargo/config.toml | 603 | `dff3518ee1e2ad6ee6398cfa26a9fd7848684707097382aa5fc6b9f89a16055f` | 0 |
| Cargo.lock | 187356 | `31268fbfed2d1ab05e8e561c75b7ed13f252cc361b8cabb4ddb2d6bc1f828a48` | 0 |
| Cargo.toml | 9681 | `f40661a9b68a8e78079cd541f480fd8607b99585587d198d8a0251e70478a854` | 0 |
| SECURITY.md | 7370 | `fdf8e8c7b66b1c640102ef75de09b95e23577560eec69998771454639f621771` | 0 |
| book/lens-init.js | 5043 | `49002bf2f55877de5dd757cf6edba104327a2872d379a9961e2b8784a1207f79` | 0 |
| book/mermaid-init.js | 40 | `4533fb1122e7a9ba074cd643af9dfcb80ac55d856f404809b64f825a968a69b1` | 0 |
| book/mermaid.min.js | 1102136 | `cc85eceaea4013d34222f27899942954cf0bab6ea5bb905d5e729c863f0d2bab` | 0 |
| book/src/user/lightwalletd.md | 12256 | `ad8a9013e04f614e75d6ea060f2b8a14392de076d6e7cf4f4a600fd9762c6ea2` | 0 |
| rust-toolchain.toml | 116 | `cdfe339851a0498ade3c898923a8b85ef0d0b8e62f89b17acedd84215f631b39` | 0 |
| tower-batch-control/Cargo.toml | 1803 | `628573df8b60fb6427ea3bddb62ecf9c590dd11b9fc83c0aa40dc4d43d053d58` | 0 |
| tower-batch-control/src/error.rs | 1481 | `35901dc0c75beb0414425cde78b7db648f67d2084b0d7abbc3f0641f72a3097b` | 0 |
| tower-batch-control/src/future.rs | 2114 | `b2f05b6976b9ef7337cd5f919d945a010d12de0107c6015a20725999155bf4f5` | 0 |
| tower-batch-control/src/layer.rs | 2302 | `db41eec5e5d5da7bce0a24984dc3e734575c56991b3cf835ba3ef49553e6d028` | 0 |
| tower-batch-control/src/lib.rs | 7087 | `e78ad738c7495b0fc8ef038be6c6c581e3a8ae1a5ab29fab2c3637fa06e01a7c` | 0 |
| tower-batch-control/src/message.rs | 537 | `9ecd17807122051b4d73c1cae2ada043d94e2197bf90fbd5519000ceab431daf` | 0 |
| tower-batch-control/src/service.rs | 13398 | `0f9c9a11cac0c21849ee2a30521da26758aafc2e173d1fda4b44a42ce1fde5a0` | 0 |
| tower-batch-control/src/worker.rs | 15068 | `d5f5c91bc6ca570dfeeca60931872783b802cccb2cf7bf2f81c63134eab7e77a` | 0 |
| tower-fallback/Cargo.toml | 966 | `6f6d497e2823096f5c843614281abd4a20b45c814cfef72d5c6bb451ddccfb96` | 0 |
| tower-fallback/src/future.rs | 6118 | `821fa33ac72bbc373655ac60bec7d1bdb9bb12d7b242c47c16b082e525976e8f` | 0 |
| tower-fallback/src/lib.rs | 894 | `57c7730d3834b8872b4e0c63997aa705e0b74b346c5a97449342efde5aef3cd4` | 0 |
| tower-fallback/src/service.rs | 3021 | `43782a22f8f7dd114b81d5cfa25160fb8365d27ab7121dc826e4318bcdb1f2eb` | 0 |
| zebra-chain/Cargo.toml | 4688 | `44e15e5b237327f489597cda1b77c69c440ac927d8551c96bb9e8fd5ae517cf1` | 0 |
| zebra-chain/src/amount.rs | 18625 | `e15a28102acccd42d64392c3bcceefaf9a8faf5d454f12b12ed68360060378e0` | 0 |
| zebra-chain/src/amount/arbitrary.rs | 389 | `aa32760cc0157fc35a503adbe2b568cc17bf1eaae0a97723d40147f10748dd9d` | 0 |
| zebra-chain/src/block.rs | 17661 | `9bd39dc802c8dc796514c3a8e56868edd9b4542100ab6c6591abba776a2d2431` | 0 |
| zebra-chain/src/block/arbitrary.rs | 34669 | `098a8c1d268edd40a80dc7f36ba78a97fd5e045f6c10a76419ff51da21fad9d3` | 0 |
| zebra-chain/src/block/commitment.rs | 14574 | `39b46bb7447e89451c4f526ff658eaec8d40bcb52b28dbfa71fb615d0fd1d69c` | 0 |
| zebra-chain/src/block/error.rs | 296 | `a4b8243c60f155e0034561d8f001f711e2b6199984582b318ea15ce337d384b3` | 0 |
| zebra-chain/src/block/genesis.rs | 632 | `4b9028a0c6e7d6a1572d9626d80f7ff968ed984ab2e8b6d34108bc3ac41dfa21` | 0 |
| zebra-chain/src/block/hash.rs | 3859 | `ca00b4348b24744c4601a13d9e6957770718f3420b2fb245877fffff3f27b8a8` | 0 |
| zebra-chain/src/block/header.rs | 7709 | `f39aaff28500b78710c17b046dba65d696145ab1912d6f1f2aa901048a4abd24` | 0 |
| zebra-chain/src/block/height.rs | 11056 | `6c660e1495d45b55f90dcedd12197e98f4e630b2146fffdcaca65a29d8822b5d` | 0 |
| zebra-chain/src/block/height/json_conversion.rs | 610 | `1fa73aa793ecf9186042e1c2f8e087f1c22cdb405a5bd6d7a38504fadeb9683e` | 0 |
| zebra-chain/src/block/merkle.rs | 14822 | `407c6eac0137b4b323f42dd2bcab9c2718b95f153ad302e298e8cc8c961d929e` | 0 |
| zebra-chain/src/block/serialize.rs | 8112 | `029e7606cc75087e0a1db4b51c6d0735b4ce31953da2ca14072e6eac016331b6` | 0 |
| zebra-chain/src/block_info.rs | 818 | `4beefa42b13e2c438e0428d87809b183dea12853b6962a72f4124931794e8358` | 0 |
| zebra-chain/src/chain_sync_status.rs | 485 | `b95881d999d704f40e1d96ab5839c2771e222ccbbddd883cc0b90a92cad6f318` | 0 |
| zebra-chain/src/chain_sync_status/mock.rs | 731 | `36a21322f4b5a99a0093e89ee05dde7b99ddd210a86528b996f18d0c858998fe` | 0 |
| zebra-chain/src/chain_tip.rs | 6495 | `8097d0688ae51b012415e5d78b861d4fdf0a0d95e1f17a4a6654749d574adefb` | 0 |
| zebra-chain/src/chain_tip/mock.rs | 6939 | `ee59ec57f1eb77fb0333f0e5a470ea7b1e392c01e5a7ae7cb553bc0c68072c45` | 0 |
| zebra-chain/src/chain_tip/network_chain_tip_height_estimator.rs | 6483 | `1be19e70741e76dd84e206e4169961ef18571480ecb81ca890da1bc26bff23c9` | 0 |
| zebra-chain/src/common.rs | 2131 | `dcf90854986f510c261e7814bf9abe77777bb5fd076366311635200bf534e89f` | 0 |
| zebra-chain/src/diagnostic.rs | 4205 | `63bd5393a2157e454c91162a51d0f0d67a6436c2fa6ebd31dfb30f00261cfeb6` | 0 |
| zebra-chain/src/diagnostic/task.rs | 3711 | `0265858a459153dcb9620469bd90a74910ffebbf3346aa42338d00206085ac05` | 0 |
| zebra-chain/src/diagnostic/task/future.rs | 3908 | `d955b3670e3125abde50c6f96687ec5ab0dc11bf2c88702266c7271d06be45cb` | 0 |
| zebra-chain/src/diagnostic/task/thread.rs | 4841 | `e247c84fbdf62349aa9d9a3e7c19203bef587fe1d7b2616fb3edb281585791a5` | 0 |
| zebra-chain/src/error.rs | 3996 | `4afde6617d6b3ee1dcb4d884f113c2000ac9e5fb485141df04885cb28eb75956` | 0 |
| zebra-chain/src/fmt.rs | 5555 | `4da4e06d8c9649a4a2f1a4a6878891242641e652563688aebf11c6bfc9a48b1f` | 0 |
| zebra-chain/src/fmt/time.rs | 2342 | `1649f9d937e997da7d23a08efcc5263447c16147812462da5386198971515831` | 0 |
| zebra-chain/src/history_tree.rs | 19397 | `0cb24cc368a7a17db48a674a001cbe091531adc30fc3db321db2a4d736b75bfd` | 0 |
| zebra-chain/src/ironwood.rs | 2953 | `de87d15629219937b55b53f685b037d1aeb748534c685990a6d56e6d07806ebf` | 0 |
| zebra-chain/src/ironwood/arbitrary.rs | 1233 | `043fd48b3c50d09bf4763c2d903590f1931d9c2ee4d24e3c5ad49dfdc6131bee` | 0 |
| zebra-chain/src/lib.rs | 1562 | `e48b0ec19655441fe086c03c49c784dbb43a84163576de607cddbe8c073d7c4e` | 0 |
| zebra-chain/src/orchard.rs | 598 | `b7f0abb3cbf0981292a87835c0eea78ac2be639a5437024e5d07f03d7b26665f` | 0 |
| zebra-chain/src/orchard/action.rs | 5420 | `c5068a760712065f44b778c4ccdb4533bb457d78b4b9d6011a68ebf13a1922aa` | 0 |
| zebra-chain/src/orchard/address.rs | 820 | `257fc309060e5636708c22dc699845f5dcef46d3f22685684c30986f26bc98c2` | 0 |
| zebra-chain/src/orchard/arbitrary.rs | 5686 | `2eabb4db744661c2725262b2d6d3152b2f14b9b73f2e2e4438399389ce0341f4` | 0 |
| zebra-chain/src/orchard/commitment.rs | 9137 | `8179aae615fc05d61f0c62b42f5c399d695958bc3cd8058b25fda8b980cb7fe0` | 0 |
| zebra-chain/src/orchard/keys.rs | 7762 | `67d77ec4946b8439f69756fb2809de0394293957613a803f64b51c2342ff8897` | 0 |
| zebra-chain/src/orchard/note.rs | 3848 | `0e66b1742e47bcec0e13659be92ce4403c6ddf1372105ccbe9abc0699401f9d9` | 0 |
| zebra-chain/src/orchard/note/arbitrary.rs | 857 | `6bee4793cf9dfbc26d2067f79b7e6e13342987045cd2bf77d968603e0d5fcd01` | 0 |
| zebra-chain/src/orchard/note/ciphertexts.rs | 4023 | `88a1b4e069c8f84ef33fff3d4dcd39fed39f86f81aa0ad305afeeeb330b56c18` | 0 |
| zebra-chain/src/orchard/note/nullifiers.rs | 1162 | `03df8a232a1b86e118e7556434d7488476f94c66ab15decf86852fe0ca05566b` | 0 |
| zebra-chain/src/orchard/shielded_data.rs | 16997 | `c4873e6049ab863eccb08538f6762795b8e027bde737af269eacf37d2314baa7` | 0 |
| zebra-chain/src/orchard/sinsemilla.rs | 3726 | `cea1cfff25c7bb20799c38cf934576d5190228db0a840f21307be0f83ee6815f` | 0 |
| zebra-chain/src/orchard/tree.rs | 24324 | `5d583db4505ee612894a01cf01a97b61d321f09615a7a3f2ec56d42006e800ad` | 0 |
| zebra-chain/src/orchard/tree/legacy.rs | 4600 | `258771be5efaae5745acc0db5e4930f67e38bd5896a00e522e5ab65487ef777d` | 0 |
| zebra-chain/src/parallel.rs | 50 | `ebbfb209c4f369a11112a321b5cfd9a6aef5bfcbb432b6d5e5eca7609427f16d` | 0 |
| zebra-chain/src/parallel/tree.rs | 11332 | `5ba43594a39938e06775bdd78431040d3d81690988a2a06e14e26e667d58a810` | 0 |
| zebra-chain/src/parameters.rs | 958 | `23803edfe51d24ac0ee1986111a9fdd5bfcf01c602173984d35135fac0243970` | 0 |
| zebra-chain/src/parameters/arbitrary.rs | 2132 | `f37328224e67d0dd960b2f65cfe02c38caa37ab4cbe10cc5c698fc04733d06e9` | 0 |
| zebra-chain/src/parameters/checkpoint.rs | 132 | `d97706dd4dba16c13c9dc94b127bb0dcc2963d2f03181b195957878b1bc83147` | 0 |
| zebra-chain/src/parameters/checkpoint/constants.rs | 1012 | `b2bb552020f2b36e6cad1f167866046275a47a37c430f4ebb745ad1981354ab1` | 0 |
| zebra-chain/src/parameters/checkpoint/list.rs | 9141 | `e46116db16c16dc26495836cc5193ffe4155bbe80693f8297c08321c47811046` | 0 |
| zebra-chain/src/parameters/constants.rs | 5172 | `cee7b0c58f32f01852f17aa8241a25c78bffd408844fd1c28e8d616af9f74634` | 0 |
| zebra-chain/src/parameters/genesis.rs | 330 | `ac7ed04e2281411a4871bdc40c64b66055a3e348f492d86adf26e5ece0774e5f` | 0 |
| zebra-chain/src/parameters/network.rs | 17334 | `e4d766dec1b9cf7eeca712b82763d4e33d32b83b94793e16d7d2c07abd35a52c` | 0 |
| zebra-chain/src/parameters/network/error.rs | 5052 | `e4a8d3b842f54e59a6cf51123f960570c8bbcdff30bdda97f73bb3819501ef50` | 0 |
| zebra-chain/src/parameters/network/magic.rs | 1485 | `4b7388c7671c53479fef36495c186a0c900a0a1cfe39196b29150ba7c351964f` | 0 |
| zebra-chain/src/parameters/network/subsidy.rs | 43747 | `6e17a1e16929b92798fd69f9118f10575a66714388588c6bf13d23ca8bf44e49` | 0 |
| zebra-chain/src/parameters/network/subsidy/check.rs | 12041 | `e54ea88ec6c2eee7012f73b77deaa189de9998591fd17d9da88327e9e976d62d` | 0 |
| zebra-chain/src/parameters/network/subsidy/constants.rs | 2843 | `cbfca164c313ae2e4f1a53b39c804be08a1e915ad43015aecfc2aee60c8a49ad` | 0 |
| zebra-chain/src/parameters/network/subsidy/constants/mainnet.rs | 11820 | `f6869352ac82da7f44f09f9d266c5e7060de4e63b1f34dab4d5d7abd27d4461b` | 0 |
| zebra-chain/src/parameters/network/subsidy/constants/testnet.rs | 11177 | `30640db066a2fa7ac23fe8e20a072560306eb1f02a242887c00609a4a52772ea` | 0 |
| zebra-chain/src/parameters/network/testnet.rs | 64246 | `3a53e4fe036c2dd982461c0450d1b5f3e6e8e8d87c96fbecb5a6894b0dc36979` | 0 |
| zebra-chain/src/parameters/network_upgrade.rs | 25183 | `87c4eaa567f370c8abcee6c3ff1ce8ec273aa28f423df0245006c3fdd9ea294e` | 0 |
| zebra-chain/src/parameters/transaction.rs | 627 | `f0b3473484b99c45fd2b4d9dc66d47df07d8924f28bed95d429bd9ea2f0de59c` | 0 |
| zebra-chain/src/primitives.rs | 604 | `ac08248210a1b0715d3addffbbceefb58af2364f902a00b1b24b4167c81c4340` | 0 |
| zebra-chain/src/primitives/address.rs | 6945 | `01f3e586d7c4474d6830b6e38c6062b46fd5beee98636a8c44cd328f459b368e` | 0 |
| zebra-chain/src/primitives/byte_array.rs | 591 | `773e9af39b36d8f5e14420a17d216aa8a233ca411644c030af9144c535887020` | 0 |
| zebra-chain/src/primitives/proofs.rs | 773 | `06c9bbb9a03f9043302e7a3aee5bc52271bcb9be54cd5f31508a4f656a1b87f3` | 0 |
| zebra-chain/src/primitives/proofs/bctv14.rs | 1853 | `1c47358444f620a39dfb63b0f568e61da03c0332dac7c7d47a31b8af8522e028` | 0 |
| zebra-chain/src/primitives/proofs/groth16.rs | 2089 | `18533ba477cd2f05b647fa47bcd97973d77b6544263fa63d39783db0a6075d1e` | 0 |
| zebra-chain/src/primitives/proofs/halo2.rs | 1585 | `8d099e24b371dd6f71ccba106cdec0d114b3acf0d383573586d972d7fd77162e` | 0 |
| zebra-chain/src/primitives/zcash_history.rs | 13671 | `5afc3d83e3ac22d89d32a8a36f69fca175ef7c515257b2c2300dfdbc32542c79` | 0 |
| zebra-chain/src/primitives/zcash_note_encryption.rs | 2715 | `7116a10cac1a7967d8b7370f700ae4f9e1b74044b663fe92644516c64ebe0543` | 0 |
| zebra-chain/src/primitives/zcash_primitives.rs | 20361 | `367fb2a554dc6fe631176e15a088f3f82fa78b27f184f2bf98fff79e62cf5741` | 0 |
| zebra-chain/src/sapling.rs | 1087 | `44ae19da15e35988abbfa94f93a2023f869188cff52a55f22523395f36d6b4d1` | 0 |
| zebra-chain/src/sapling/arbitrary.rs | 4816 | `3e1e6cb51df6f1d628b475fc3eac6ec4addaafb4ae8c4c0c1b1e957ac8d35778` | 0 |
| zebra-chain/src/sapling/commitment.rs | 4339 | `d0317def005af6256855210d70c74125cf4ecc58bcf6ea44f9012c13c6c8fedc` | 0 |
| zebra-chain/src/sapling/keys.rs | 12808 | `03b4a8a0d9eaf0c324eea219e1ee0488a1d8359507289590f6bc7ab856e2ac32` | 0 |
| zebra-chain/src/sapling/note.rs | 1097 | `45b7021ec07f8a5f1563f84690a7ae7ec067f65a675ec02e794fc443d7cc5703` | 0 |
| zebra-chain/src/sapling/note/arbitrary.rs | 857 | `6bee4793cf9dfbc26d2067f79b7e6e13342987045cd2bf77d968603e0d5fcd01` | 0 |
| zebra-chain/src/sapling/note/ciphertexts.rs | 3903 | `a2aba8d43f997995a7f43e017cbbe1063e71c21f943828e297d899c3b878f3d3` | 0 |
| zebra-chain/src/sapling/note/nullifiers.rs | 1646 | `cae53d6498a61d058c58a60ce7c3e7e51585556e31fba7b3304a6109dde41da9` | 0 |
| zebra-chain/src/sapling/output.rs | 13221 | `ba0547370f0283c4c3112a76ad83d833b0f82a2120c470ad4bbe3f46495ecbf4` | 0 |
| zebra-chain/src/sapling/shielded_data.rs | 13922 | `504e5a9aaa55839aea6d2c6dde024a27932e999c794ff89e5f6e767923a183e5` | 0 |
| zebra-chain/src/sapling/spend.rs | 14770 | `957b2cb4a712a0e7c3e0931642b557afa0f7885e3e80ae2b8eb4a962cedd1931` | 0 |
| zebra-chain/src/sapling/tree.rs | 18270 | `d4c4b3593b1ffdfbf8cf97ee9d374970e5b8dc8242aa27d999409d7fa668ede9` | 0 |
| zebra-chain/src/sapling/tree/legacy.rs | 5391 | `8d13e720180681dd31955acec27207a13f668ca964ae81d150fe2b996a89e08a` | 0 |
| zebra-chain/src/serialization.rs | 1525 | `ebbbed84ff65f46a705f687d5760572444e76d9fea97c70e8815e00eda4ae41f` | 0 |
| zebra-chain/src/serialization/arbitrary.rs | 4595 | `4b041e61cfb03b854997a48f9095558b3fb24b94e628a4c3562646cdc0c2acc1` | 0 |
| zebra-chain/src/serialization/compact_size.rs | 12681 | `ee2d9fb79d02cd62c0f956442e18ee57201f239b6aa66f5193eb9857d9e33706` | 0 |
| zebra-chain/src/serialization/constraint.rs | 1828 | `7205b3b6d684ae47b18bd4ef31bdf02e98b94ddb4d49244c3770218443063f19` | 0 |
| zebra-chain/src/serialization/date_time.rs | 12483 | `d506fd40b83e2973c895ec36d27235c809bc6577813365434d23c4524267e8b2` | 0 |
| zebra-chain/src/serialization/display_order.rs | 1579 | `6f9eef415a1e46bf2a2847466e65feeb59d8e2d60efe8552577713fa03fda8aa` | 0 |
| zebra-chain/src/serialization/error.rs | 4875 | `ebd54eca9cad08f85f0f0c079f347d1981a7c6f3e9419d79c0ceb97ef66b1c57` | 0 |
| zebra-chain/src/serialization/read_zcash.rs | 1168 | `62670e1401bdca94f4d9f6cd2b6c3c85c7584dcbb3831379a7d33429e50baf40` | 0 |
| zebra-chain/src/serialization/serde_helpers.rs | 3152 | `8c99449a279a4ebfbbec19e29db59948d4b3a5372027b31fe0645771f2c2028e` | 0 |
| zebra-chain/src/serialization/sha256d.rs | 2063 | `de768bf81066e297f7f63f4cfa3d17c9d3af882a27867c5e8c4b9055ed99f830` | 0 |
| zebra-chain/src/serialization/write_zcash.rs | 662 | `4efa398b718d08fd2eaadfb532243c17c43fe488fbe0ce3d52049de3982dabb3` | 0 |
| zebra-chain/src/serialization/zcash_deserialize.rs | 10532 | `14b4c9824995eca9cefbc58cb3d44934957eff97673f930c1101eb27c60172fb` | 0 |
| zebra-chain/src/serialization/zcash_serialize.rs | 7108 | `55c9faa8ecd0891ca27af3d89f246d0d5fdd6988e7d9fcc56004909bac40eb97` | 0 |
| zebra-chain/src/shutdown.rs | 928 | `01b43125129536b7d964368d5a40dae892bd9bb74b456eead8afc0540df70a10` | 0 |
| zebra-chain/src/sprout.rs | 364 | `6bbede02b43bbf7a935458e4b1703f4e74218e41f4384d287d7473dd59b3df6f` | 0 |
| zebra-chain/src/sprout/arbitrary.rs | 1764 | `f60e27780ae48066f427d32c054ae0d14eeb341a101987799ee3a3a03cbfd0d0` | 0 |
| zebra-chain/src/sprout/commitment.rs | 1959 | `b5cd52f35dd286b4443d748f68d0a5ca6ba6a1f5e1f1f053fc0aac8d5b048319` | 0 |
| zebra-chain/src/sprout/joinsplit.rs | 12408 | `225314a0c4d61733ecda0df7371e4d1402c4d9dc5c3c5bcf61607d1551a50cc9` | 0 |
| zebra-chain/src/sprout/keys.rs | 920 | `ae215808e68ef32bde73763b47088ca8e1b152ef536a841649f6f4781283a341` | 0 |
| zebra-chain/src/sprout/note.rs | 1166 | `78660a4ac0863cda459e07c7c75b00fda43d622292382064a2cd4413e5495191` | 0 |
| zebra-chain/src/sprout/note/arbitrary.rs | 451 | `69dee95b10e0716bb56fcd3bf6afcbd88c094b46eab666a3fc430941ba805675` | 0 |
| zebra-chain/src/sprout/note/ciphertexts.rs | 1871 | `78084e824e1e3a149c1ce3915b0643e05178e33981f3f17286b423dbdfa81ff3` | 0 |
| zebra-chain/src/sprout/note/mac.rs | 1505 | `a21e86a1105814f54ad84a92574b86698165c6dd0d1d7ed4cabedd2dafd0415f` | 0 |
| zebra-chain/src/sprout/note/nullifiers.rs | 1551 | `0d64e64a4822b3ddd1725a0c0b287964104e7d13e5023a048cfec614d04f97d7` | 0 |
| zebra-chain/src/sprout/tree.rs | 13981 | `996c2fd30b1ca8082bf871119305068d14cdd04eec9c7d3df5894eb496ff94cc` | 0 |
| zebra-chain/src/sprout/tree/legacy.rs | 4551 | `4032a5bc7c51e428314399c8334015176847871b722271887585703e48ada6b5` | 0 |
| zebra-chain/src/subtree.rs | 3886 | `4dbe0b16ea003164a1d1f48b218baf494117836b1fdc5eead9814363fac906a8` | 0 |
| zebra-chain/src/transaction.rs | 60832 | `8c24c5c78507be94b192690c46e4847da30f24b922013a9de872b6b1befdeb06` | 0 |
| zebra-chain/src/transaction/arbitrary.rs | 40697 | `140024574bacd582d1cb281a3671983040423e6557ba740f87359cdbf24fce1b` | 0 |
| zebra-chain/src/transaction/arbitrary/shielded.rs | 21374 | `da2dcb7e899c41a867fc382a4f96565ef72282086ca758066f3f51649aafb4c4` | 0 |
| zebra-chain/src/transaction/auth_digest.rs | 3496 | `1e6ce46a66da8d4d35e18b9c220d9aaef74a34dbbdeb994bf971d813a1a8718f` | 0 |
| zebra-chain/src/transaction/compat.rs | 14448 | `ddf86281e59c80e95b1ec3edd3af7ec65d8ff5cc5f7164c2febf5be8a10ae109` | 0 |
| zebra-chain/src/transaction/hash.rs | 9968 | `c25708575e6843b699facbe77784cd7b2421cfe7ebdfa0fe95a050b4068fec20` | 0 |
| zebra-chain/src/transaction/joinsplit.rs | 4891 | `155b6fd2368259208ed8d92f9e86cc6a206fd5deca6b827b6be3a73a4d3a9875` | 0 |
| zebra-chain/src/transaction/lock_time.rs | 5099 | `dae806f6fda11960bdd9057da307f62155f5385bdc134388b343187820745544` | 0 |
| zebra-chain/src/transaction/memo.rs | 4615 | `08a875626482ceaf141f1f0c57998229491530518269b57f9d02eebd858e72c5` | 0 |
| zebra-chain/src/transaction/serialize.rs | 32372 | `7fceb04ef65c4829fbcb3ce253280d34ea6fe64817e2e4a65f3b6e775ef0ab2c` | 0 |
| zebra-chain/src/transaction/sighash.rs | 5568 | `3db6896163dbdb4a0c88e788d3d9e2ec29374e0f8900378c55a251f2f97da193` | 0 |
| zebra-chain/src/transaction/unmined.rs | 16261 | `f852ba4af9c812fa777c5a795caae250994946e7f09d69a221d0d0c98ecf9216` | 0 |
| zebra-chain/src/transaction/unmined/zip317.rs | 10256 | `f9963948c37ad2a23e2febdfe0eac6d7d5f3b663d8dc412a9b6e841ba205f708` | 0 |
| zebra-chain/src/transparent.rs | 14247 | `3db4148660472fd980c0650bb517fb0beebb8f2e49ccbc3b021a354243ac3c01` | 0 |
| zebra-chain/src/transparent/address.rs | 18822 | `7865566939e6b3222a12a534225bb2df5869aa4c6cbf5fdbf854208e004737c0` | 0 |
| zebra-chain/src/transparent/arbitrary.rs | 2638 | `9be4a12a5f30af236055a2ac52a1b95b844df6429e8a7685240dcade94c9ce6c` | 0 |
| zebra-chain/src/transparent/keys.rs | 846 | `88ba431df453bf5fe71627394e61f4246e4cc3f1e66944562a8df27009a506bc` | 0 |
| zebra-chain/src/transparent/opcodes.rs | 407 | `d45a159a18bb94c33394c54b2e2a4c3cec812702ebf6002e48cba16f13a12f32` | 0 |
| zebra-chain/src/transparent/script.rs | 3318 | `d85b97c2a244dc88a614e8170980be2cda7d6785a446b550b7642059daed6da9` | 0 |
| zebra-chain/src/transparent/serialize.rs | 11181 | `04a4b80a25ad61446c6a0bb94d843bca2d984dd099a4301b0551aa9ed660c0f9` | 0 |
| zebra-chain/src/transparent/utxo.rs | 8200 | `fb9a156731d924a0e41fb37c4903f50630eac0f304dfea9e4d00be4a3ba69714` | 0 |
| zebra-chain/src/value_balance.rs | 25713 | `f259fe4e9cb12149cd8b38cf900e8dd80e1c3de571f480912c1203eb3abb13d0` | 0 |
| zebra-chain/src/value_balance/arbitrary.rs | 1854 | `125e78fa73d41745a0824dedb3111bee24330ec3dda13c1a1d04a13712514583` | 0 |
| zebra-chain/src/work.rs | 168 | `09c782cfa1b6b6b997f5666cca8e54e2ef01d4ea01b2b8356f4aed1176b18ac5` | 0 |
| zebra-chain/src/work/arbitrary.rs | 512 | `3b187c27d5a165cdca00f04c5484a15788c22a90863a75d0ec7ae3e98200bd17` | 0 |
| zebra-chain/src/work/difficulty.rs | 28204 | `82adf21c7a8d95d50f5cd1b73cc70b32e5b956f54f284a1bbdf6d31c1d1f4a59` | 0 |
| zebra-chain/src/work/difficulty/arbitrary.rs | 2535 | `6100459afb3105a3c4042ff14c7f365b5f8f1dd580ada704f640071d18636c39` | 0 |
| zebra-chain/src/work/equihash.rs | 11789 | `55f50d87fa325f94611b3b8b6f06e84f2c7ce475bc6334f86463353ff34639d5` | 0 |
| zebra-chain/src/work/u256.rs | 648 | `ac8d55d47e3e6a677bcccbc7144fa491fb45fb46d13882b344c043a9380013e0` | 0 |
| zebra-consensus/Cargo.toml | 3748 | `d723c9e8bc329f5929d138e6bbe87e4126a6784b50dd303ecf42ef1aceab855f` | 0 |
| zebra-consensus/src/block.rs | 21360 | `44bb3b00a101ed03177c4add8a4db66bcf13e48170063d67acdebc730b9e9ab9` | 0 |
| zebra-consensus/src/block/check.rs | 11620 | `cecf89ce3c9b4b9498d79803b6bf63df85219c4eb6a0ffb45d60570cc5336d51` | 0 |
| zebra-consensus/src/block/request.rs | 990 | `8e608e56375e3dc238b9ad9e7a00c2bb57e636016011f22bfc96971f80ccf91f` | 0 |
| zebra-consensus/src/checkpoint.rs | 57423 | `fc2586f730f2cead457ed0be072a98970e2d68e19a33aa94e858a85b6cf98d07` | 0 |
| zebra-consensus/src/checkpoint/types.rs | 4573 | `463874ec0d7e38cf6a7a14af6a96991b51ca2a8468c9cc7ee749956c4be98f8d` | 0 |
| zebra-consensus/src/config.rs | 2773 | `ba25240087fbdf66e96b92bd27134a005834d4e0b73e0a8ab601249dbc62fa30` | 0 |
| zebra-consensus/src/error.rs | 21408 | `b19e8f0bb9708a090e61f9083c509093913d25f96412ab2ac01d7a7dcd17c18a` | 0 |
| zebra-consensus/src/lib.rs | 2664 | `91568d6f45e413a5273a2e4a248f4e46daf5f08140de686522885bfb97532589` | 0 |
| zebra-consensus/src/primitives.rs | 1498 | `a9659d944688bc47150e520ab223401083a78d247e9017f970b1bd70f4afb554` | 0 |
| zebra-consensus/src/primitives/cache.rs | 20322 | `8d6c0c47d7278672bea75ab3564276b174c8f2989253b54e8b083503d9a4b36c` | 0 |
| zebra-consensus/src/primitives/ed25519.rs | 8118 | `a3ce7906723003adde35d2ec0f1dd8bb797adf559aba6410d685e6ed7efb5aaa` | 0 |
| zebra-consensus/src/primitives/groth16.rs | 6820 | `278bda853282f1e905f75dde83800f827cafc4677557f2ed3ca9933c0afc18f0` | 0 |
| zebra-consensus/src/primitives/groth16/params.rs | 1151 | `f0746e2513991205ec706e041d43994219cc8f8765e19e9c1451533d9049d47d` | 0 |
| zebra-consensus/src/primitives/groth16/vectors.rs | 2746 | `67b0a451a9247c6e03fd812f010a1d71cb5588ffcb107c6fc50e4ee913e9986b` | 0 |
| zebra-consensus/src/primitives/halo2.rs | 28247 | `437f487a9a5240b1303448877fd2161aa6b3b0032782c3d4fab630c5b3b67c2c` | 0 |
| zebra-consensus/src/primitives/redjubjub.rs | 7934 | `c65f9bfa6d6de25aee537ada8fc08137b25b57661716cf077a02996d0cf9de02` | 0 |
| zebra-consensus/src/primitives/redpallas.rs | 8681 | `260cef69fe3728981e7108b9a3a6d6f16dde7512da8ec6fb2d9be86732131f92` | 0 |
| zebra-consensus/src/primitives/sapling.rs | 11298 | `486142019610ae247b0be4537f3b2eb73c388360c2fdaa70f700757b2966e5ef` | 0 |
| zebra-consensus/src/router.rs | 18915 | `bc499c2357c9ad63bf32e8ccf0ec3df27d7e6a91a2c09225d06976f3e3e35bd0` | 0 |
| zebra-consensus/src/router/service_trait.rs | 625 | `2bd2c1e22580d70ac0d70aaa7684bcf9167f1c67414ac440f906fc240bfb2c91` | 0 |
| zebra-consensus/src/script.rs | 2220 | `e244b00fc1c084f5c48a8c07a56155d98805a843967571426b3596098cd204cc` | 0 |
| zebra-consensus/src/transaction.rs | 63491 | `cb84a61366b275f76e144aff8fa2a374053741a567ee6dd5a070c75985424afe` | 0 |
| zebra-consensus/src/transaction/check.rs | 35390 | `14a3995600fe10344672ee7aba44fc87fc527cee758b60ff391235407b98154b` | 0 |
| zebra-network/Cargo.toml | 3570 | `8a428d90481eb5a1eefae34b0eb0441d96613d94bdbaed7505692f66c5cf9995` | 0 |
| zebra-network/src/address_book.rs | 37540 | `0c4ca80d952f174b04374bb5201946474c7a6ae141ed83bec072ca0b334a7de8` | 0 |
| zebra-network/src/address_book_peers.rs | 1184 | `55d724e4d4f6e15d35fa67fc88eb45b1dfe004c22b49eab50f415ae0f639c038` | 0 |
| zebra-network/src/address_book_peers/mock.rs | 2599 | `d42e6f85abdcb2acfa65baa37a0f8586c141f7b30237328ac703220d228318d2` | 0 |
| zebra-network/src/address_book_updater.rs | 16551 | `e579c9b0cc6dcc572e4714eb6eb2737de730039d5acac4bc1c792a74cab90bc7` | 0 |
| zebra-network/src/ban_list.rs | 4247 | `d4530bac69640902bc74f366e4b1bab97bccc09156455f4acf0fa41819c1837a` | 0 |
| zebra-network/src/config.rs | 46088 | `915904806ecf15f43ba41498178ff3bd7d4632b58e226431ee7d076eb61d6435` | 0 |
| zebra-network/src/config/cache_dir.rs | 2334 | `2636a3b0ca50996bc77a6a90f49cdfa1e35b391692e8ed53cddf6aed4b01418b` | 0 |
| zebra-network/src/connection_metrics.rs | 16592 | `18ae40f2b8f01902efeba315fbc9417ec6a1fbc5fbe9083287719ec5e52daae0` | 0 |
| zebra-network/src/constants.rs | 26598 | `3d6366de5794f0ce33e9933830a27cf723fe4d5abee359cabd3b1c168f88f077` | 0 |
| zebra-network/src/isolated.rs | 5742 | `843cab4371ee5a146477a5dad755f1e0b11d0af73adcfabe77dfd3ddfa8f6c34` | 0 |
| zebra-network/src/isolated/tor.rs | 4908 | `a3ddad853b71e8a780edeb904ed9b1ebf5e7cb23e792ecc09c3c16d10aceb3d2` | 0 |
| zebra-network/src/lib.rs | 9059 | `881795f1aaa97d5130991d0833514f7e9043fc745103323236e3009d64afc3f8` | 0 |
| zebra-network/src/meta_addr.rs | 55335 | `578598a8051f2fbb6db11b7cbdc1d0c986edc58f2fa7c921639cf59bf3037035` | 0 |
| zebra-network/src/meta_addr/arbitrary.rs | 4067 | `916cc073daa359d4e1b11269721c34a4bc9af1c33bfbe60ff30a4693ebfa8a92` | 0 |
| zebra-network/src/meta_addr/peer_addr.rs | 2325 | `bf52563c0c38e7ca1065ce969abf41f728a5b55aa96858640eb14f2c48473a00` | 0 |
| zebra-network/src/peer.rs | 1132 | `c8fd05c3b1aa1ffd88706542e9f0e111689cf9c7eba7927bb3d77d7e5324e45c` | 0 |
| zebra-network/src/peer/client.rs | 26617 | `71a7ac6fb96ada2c34af1e7a7189b08faf2d94a281c1ccbbed44c027caf84ae0` | 0 |
| zebra-network/src/peer/connection.rs | 86775 | `030a663cb31274a2d43e8c69bfafceb6c4786362e19ca54d001a7b0fab1b9b87` | 0 |
| zebra-network/src/peer/connection/peer_tx.rs | 2329 | `04ceafe3973143a92f43c2d21a8a52724e60fafdba69ed8cb2d599f14f6d186c` | 0 |
| zebra-network/src/peer/connector.rs | 3476 | `bdffba1f63a5acb063d212a8912f5b1275c8dcdd5f26f5574e5c0b3462f3a894` | 0 |
| zebra-network/src/peer/error.rs | 11294 | `562ad412dd784c815eb17d72033c53d6893d2ee8a090a89c6e7dc0243b26266e` | 0 |
| zebra-network/src/peer/handshake.rs | 62855 | `61148a6d2f06956aea0730b2f68a56d922a0047245a83c7ad91d5773790844d1` | 0 |
| zebra-network/src/peer/load_tracked_client.rs | 3309 | `096826fa1b70fd83ffcd0994226600146b9edf4a3e907f5f1b3dd7f2681b353c` | 0 |
| zebra-network/src/peer/minimum_peer_version.rs | 1766 | `e84e1ac97c27df881a0b985ca91dbb30219ae206ce3a81becd451a81b7bddb09` | 0 |
| zebra-network/src/peer/priority.rs | 5427 | `89c24936424cb7d706e0be4535aa34d86362a531a1131352ceba7928896b1da6` | 0 |
| zebra-network/src/peer_cache_updater.rs | 3224 | `d0d73a836a2f16be7e5df862349638818659b4b185b48bc3e0add6e3894dcd2b` | 0 |
| zebra-network/src/peer_set.rs | 7286 | `ddc54fc2f0eefd0f9ca1f91f43888458416948394b119a08d06c6fcd774cb721` | 0 |
| zebra-network/src/peer_set/candidate_set.rs | 12289 | `8e43158894c50e025b5083b4b6ef00765221ab4cc138dac27007b00fd8ced0a3` | 0 |
| zebra-network/src/peer_set/candidate_set/crawl.rs | 14148 | `95fb8fbdef0fe25499863e454b9931fad43181993e74b74ddb96e1f9f567bef7` | 0 |
| zebra-network/src/peer_set/candidate_set/rate_limit.rs | 10739 | `b145656b67564bbb1aabe8b169a5b480ae3b6df13e5d7bdcee5f895e687f7c12` | 0 |
| zebra-network/src/peer_set/initialize.rs | 56355 | `4e5274859e28d08778a300b6b08ae221d80b27c84be6bf95d3038fc1d61f01db` | 0 |
| zebra-network/src/peer_set/initialize/recent_by_ip.rs | 3501 | `d5e7fc5ec63e5fad4aa3f084e114b12cdef52a98cbb805d84a38188e4855b4c9` | 0 |
| zebra-network/src/peer_set/inventory_registry.rs | 20018 | `164fce04348567ebd30ba27a7e53bcfb452d223fee4d5a6f78febde9461e2238` | 0 |
| zebra-network/src/peer_set/inventory_registry/update.rs | 1121 | `807397cebe2dd765b201f2d3272668deecbed42b0b965754ba72421cd7c57e65` | 0 |
| zebra-network/src/peer_set/limit.rs | 8287 | `ef54417e4d8f9337243c2aea6eb41104d4587dd27eecc8494729bebecea58b70` | 0 |
| zebra-network/src/peer_set/service.rs | 4173 | `ed613f79e668a1bd0b5f5e46976851f9607eea1152fc5b29de9ef040ef570e1e` | 0 |
| zebra-network/src/peer_set/set.rs | 99829 | `9cf13afb49bb795d633889f72eb6427e05b6515e6530287940312c1baef75542` | 0 |
| zebra-network/src/peer_set/stall_tracker.rs | 1770 | `e3abcc336324de2c141c0fb56b1729b45e859540cd6edf3110e682e33bcc7bf6` | 0 |
| zebra-network/src/peer_set/unready_service.rs | 3632 | `3bb430290a2716863150876a7382576cd75636fb91c8a19e45201414ef66dd78` | 0 |
| zebra-network/src/policies.rs | 2034 | `2b87c933ecc92f00c9d57c154c9a5d17c228872442ac42cb18bf697452cdebdb` | 0 |
| zebra-network/src/protocol.rs | 243 | `5a1d111f074080ea6f2aa7097fa5cae6e59a4d9328b54464cb10083d4fa5bf77` | 0 |
| zebra-network/src/protocol/external.rs | 789 | `c1dac27487c69d78d79063fe410c1bfa0d2802c97d286dbff443c4a845d37a7b` | 0 |
| zebra-network/src/protocol/external/addr.rs | 838 | `1503d33f9a825a63fb248425061e7c3ae3259f5d3a9aa7ae65867981e74e2bcd` | 0 |
| zebra-network/src/protocol/external/addr/canonical.rs | 3900 | `21785f2c73b6a501f763ae9f99a319413c3d8655a432751f7b449d9dbc011635` | 0 |
| zebra-network/src/protocol/external/addr/in_version.rs | 3495 | `d1df383a9adc5dc6df27743b96bf0b1a1c66a046e398c37e60a4c985f79881e3` | 0 |
| zebra-network/src/protocol/external/addr/v1.rs | 5351 | `5d67060fe9d72950c89cb022f9a11d6ef428e32632fcdfb81b607a3147f4e9de` | 0 |
| zebra-network/src/protocol/external/addr/v2.rs | 12580 | `4a805fcb71e65d24b4386026695302d16c5b36a5ff91ca948ca20330d0e09442` | 0 |
| zebra-network/src/protocol/external/arbitrary.rs | 4086 | `51b20d867a54f435c7b31ff8b78b97a180faf7e770c5febb396920b338894fa9` | 0 |
| zebra-network/src/protocol/external/codec.rs | 33791 | `16af05828ad59fe29e7ab7171c2d2ffd0717b5820503560f363a0d4bd959e7aa` | 0 |
| zebra-network/src/protocol/external/inv.rs | 7873 | `dd872231f6f0483035bba0ff6375b2a1f22cbc30b879f6c8422a6c45770e7e6f` | 0 |
| zebra-network/src/protocol/external/message.rs | 20628 | `2088412c6f61a59f7363fdfb7f7437d3eb7d274fb6e18f1240210e61065c7f90` | 0 |
| zebra-network/src/protocol/external/types.rs | 8076 | `38a4036c037409b65e7771d6064f1a1ea0b277a43e3b9597e231ccac20130e32` | 0 |
| zebra-network/src/protocol/internal.rs | 147 | `f518710a0001cc025b65ed95aaa4822ad1d25b9a741951d414b2d13bc8e69ab3` | 0 |
| zebra-network/src/protocol/internal/request.rs | 15177 | `5c2c28d395fbef23b317fd656ac791afe17d2912beb1b67748fffaa11e29e18a` | 0 |
| zebra-network/src/protocol/internal/response.rs | 5960 | `51c8e9591fc5b8b8ce40df7081acb82a9a28de70935cfa13235825963b4da1b6` | 0 |
| zebra-network/src/protocol/internal/response_status.rs | 3073 | `b4998072c9eb8c7cf3870d4064e0f75e093f25bf3ad5971ac0aa81bf6d5f63e7` | 0 |
| zebra-network/src/protocol/types.rs | 196 | `44822b63b4b7eb4c917cad8a8b4fa284b223d17449d61225ea4a44f2d64fc970` | 0 |
| zebra-node-services/Cargo.toml | 1631 | `b285520f28ee0ed043e1d4aec3f96b3ad8ab57565264b91955b6689fb5899be3` | 0 |
| zebra-node-services/src/lib.rs | 572 | `fb72ff78f17a7d9f42bebeb3b4f5d715e8d0a9235c8152bd4a42606e7edf0689` | 0 |
| zebra-node-services/src/mempool.rs | 8437 | `e65205394d08dd6c7bd0a1800bb30583d67f919e85a17a8c8fafb119ac72baad` | 0 |
| zebra-node-services/src/mempool/gossip.rs | 1091 | `fdb0f24298fdc4c19c79532b10bb3b2a4ad8df360b6fda9dbabaccb5778ec49a` | 0 |
| zebra-node-services/src/mempool/mempool_change.rs | 3200 | `7f1472a544f286f120d5d7788d9cd8011d82bfcdbb338f220f6b609eab6ff27b` | 0 |
| zebra-node-services/src/mempool/service_trait.rs | 567 | `b246580f9f90cea8fc4ca0b4b51ff8d525eaf70546eb25c6ea66f74b5f2663c2` | 0 |
| zebra-node-services/src/mempool/transaction_dependencies.rs | 6431 | `b61684106f462af64fed36b17add84ad7896063e7a046ddddc089c2310732eed` | 0 |
| zebra-node-services/src/rpc_client.rs | 10715 | `5e970858a4ffe20de69bd449e20f9549c657125cb06d51e3f3cc6a03f4bc1e25` | 0 |
| zebra-node-services/src/service_traits.rs | 681 | `88a4a73bdbec68de62d530dc8b618dc62167e2dd930b07f8c16b309f757ecad7` | 0 |
| zebra-rpc/Cargo.toml | 4503 | `d13812caab253b9984e1229dc347205ceb83c098462814bf229318e6e1eb96e7` | 0 |
| zebra-rpc/build.rs | 6074 | `56c959b4d2157692acdbabe696d8d40ac1fd71502338bf92c15b020d7d1baa1f` | 0 |
| zebra-rpc/proto/__generated__/cash.z.wallet.sdk.rpc.rs | 110589 | `de4c9bf91cbb4ebead4a0b88f09da398246b0c68910a5b905165d0a58da3c2b7` | 0 |
| zebra-rpc/proto/__generated__/zebra.indexer.rpc.rs | 29727 | `af2d02371d71162de13cb4754efddedecdffd5e3c17f7eaffe8450e5066ab094` | 0 |
| zebra-rpc/proto/compact_formats.proto | 4762 | `913dec2938b0301f41577ef5927734ba8af0e7ebefeb6588a2c62299875e0387` | 0 |
| zebra-rpc/proto/indexer.proto | 2914 | `b8395c6d0a676651da0434d1515733edf2840f0ae08809d353fccef6b84e80b5` | 0 |
| zebra-rpc/proto/service.proto | 10892 | `77454df4cfb67e1fdc66039a43ec0bf3d6f2fae7b6eb66bec11ac7d63bd22eac` | 0 |
| zebra-rpc/src/client.rs | 2403 | `39bc8c4103fe737b5a880beaa65dd3fd75b87f8c6c43877251e8b8b18f982d20` | 0 |
| zebra-rpc/src/config.rs | 62 | `e54857d5e854c77ca9b69c4060e44e7935577b6e0eb8c288f9c6ad536da0a89c` | 0 |
| zebra-rpc/src/config/mining.rs | 7832 | `9f79e938e006ca571e631d5f159f723b56c9c7720219fadc2f4578c77e7ec56c` | 0 |
| zebra-rpc/src/config/rpc.rs | 4866 | `0c127b3b0c691f1a621f667a85c09e427374810e2fbf665ace7352b38aceb68d` | 0 |
| zebra-rpc/src/indexer.rs | 2630 | `af51c7ecae54ad330524ec76c8e54eecda6793ecf29c0f4bd77b5b7edefca9c2` | 0 |
| zebra-rpc/src/indexer/methods.rs | 15589 | `6c74175740dfe0048f162f0f3e892ba0bcd383558f1336608569a25fce969759` | 0 |
| zebra-rpc/src/indexer/server.rs | 2878 | `0e377d5efcfa0c59c8e47b169d6059e4d7db444f8af44ff9b7f99e2a4ea186a5` | 0 |
| zebra-rpc/src/lib.rs | 610 | `8df5b30d41157599a400a55c2240da6aad08d8ad8003c5436ddb9f7757371fbd` | 0 |
| zebra-rpc/src/lightwalletd.rs | 6656 | `01c998ea7b9d20a437c7022a5747a35fe293dc713398ab3d69faf248b4654890` | 0 |
| zebra-rpc/src/lightwalletd/methods.rs | 50411 | `9e4d55a8fa44115958fb83b131f1e43a1bbd38184034a665bef5564ff1f64cf2` | 0 |
| zebra-rpc/src/lightwalletd/server.rs | 3724 | `703c589ff746a83566b1e248f7d0469f1043d620f0dcdb5be5255c0767f8a02b` | 0 |
| zebra-rpc/src/lightwalletd/tracing.rs | 6674 | `06af1349ca6b94824d878f9b7704238bfbde0bc0718194341732ab99bcc7a777` | 0 |
| zebra-rpc/src/methods.rs | 211166 | `eadbe226e9950590359847c7b640b8f75e84c80d097887f6fc805a1bee82559e` | 0 |
| zebra-rpc/src/methods/hex_data.rs | 352 | `36e347b9b0c10aa786084d02de1a09fe2cdb061537fcdc450ee34758b3f34197` | 0 |
| zebra-rpc/src/methods/trees.rs | 8112 | `dbdcaa31d92b06507adf36ea5bc6167595fe89b90d6aeba37ff3b95a6dd6b5af` | 0 |
| zebra-rpc/src/methods/types.rs | 426 | `68140a90fe4cb0a1c07ccf200297790e3e4ad9970f9f7aad5a0d0b1a7f18b159` | 0 |
| zebra-rpc/src/methods/types/default_roots.rs | 3958 | `f210e97f16e0164dfa9e7cb8caa7b65f042c4e0166d4bbfca4e00e00db8c8234` | 0 |
| zebra-rpc/src/methods/types/get_block_template.rs | 40875 | `acff697fe4a82cfe2394eb3d0fb312e1e3f397d4de39c00ae7caff1c0a0c8b03` | 0 |
| zebra-rpc/src/methods/types/get_block_template/constants.rs | 2700 | `e3f546ffcfd51a36da2eca8cbeecbcb5e516e80d9a85f61df929333becf6a2a6` | 0 |
| zebra-rpc/src/methods/types/get_block_template/parameters.rs | 4231 | `7361c51ace781e9608f0365015247f7f43de237478c5e311ea9fe9a14366bf37` | 0 |
| zebra-rpc/src/methods/types/get_block_template/precompute.rs | 19702 | `a3cd0dcbdea5d841d70dc05446c9ec2383ca6caeaf6e39d3af92981f33705878` | 0 |
| zebra-rpc/src/methods/types/get_block_template/proposal.rs | 8495 | `b3a505b59cef0d085f9c4416a8bb97757d8f862a02acf91a7f8fa456bf89de15` | 0 |
| zebra-rpc/src/methods/types/get_block_template/zip317.rs | 19132 | `f0b2e3a856bb80f794d0c7010072787d2c559f7ab25c614ac0d1153376a9428d` | 0 |
| zebra-rpc/src/methods/types/get_blockchain_info.rs | 5496 | `338236d6d26464953be896b91996b7f1e65f9550548dcb3fe70d6a699ab0186b` | 0 |
| zebra-rpc/src/methods/types/get_mempool_info.rs | 697 | `9a5cc253df43124520b84e3529fd16d746a495d989de73da43708ad34adc90b1` | 0 |
| zebra-rpc/src/methods/types/get_mining_info.rs | 1683 | `6d0823dc4a0cd83d46f64f250b9d8efaeb79d338c5c436956b387ad02c47050c` | 0 |
| zebra-rpc/src/methods/types/get_raw_mempool.rs | 4388 | `b469e45bfca190619736350163a6f22e08deeb6e138a922dc0b344eb0cba57ac` | 0 |
| zebra-rpc/src/methods/types/get_standard_fee.rs | 1824 | `88a128d2601d5853d836ff262758910122389c909333313b1d25f89ee6404a35` | 0 |
| zebra-rpc/src/methods/types/long_poll.rs | 12013 | `046be6efcc09b8e24c7535d74df829a2f4666d01b64820e14bf74d1e3d6ce157` | 0 |
| zebra-rpc/src/methods/types/network_info.rs | 2021 | `6cf18d1a8024adf4a7f65da84e5f365930ec9440ca6b67f55b861c221e9acbad` | 0 |
| zebra-rpc/src/methods/types/peer_info.rs | 3275 | `134bc60a847f74cdf0c2078f614425b89095ce8119f6216d4288bf42bb6c21a4` | 0 |
| zebra-rpc/src/methods/types/submit_block.rs | 4029 | `1ff39142dbba6b562aca9f91cc2a9ce3b1bb53436d6ba6f39ca07fba02fa6378` | 0 |
| zebra-rpc/src/methods/types/subsidy.rs | 3730 | `4c046d7c4fae5ed819db02f95fa3c8c5d454575d904e8635eac580ad130a4550` | 0 |
| zebra-rpc/src/methods/types/transaction.rs | 56642 | `b0d6338831d0dbd929a08f441b6d95fc6d24a1b9fa11e97f2e9f67a4985c0d8f` | 0 |
| zebra-rpc/src/methods/types/unified_address.rs | 945 | `0fd42df2db48e76c2dbdec97984d38ef7ba9027f237e26dfcb163a63ae20ad6a` | 0 |
| zebra-rpc/src/methods/types/validate_address.rs | 2578 | `129d0c7437c80e83d1cc00d0102e272ccc05348e29de8e9ad7ca17150f162c6b` | 0 |
| zebra-rpc/src/methods/types/z_validate_address.rs | 3786 | `a96423c7e994bf0f257225f66d401493936a3a856fb818edbd76b1b1e4055e42` | 0 |
| zebra-rpc/src/methods/types/zec.rs | 6706 | `7b7fbce7b2ed5da18be4f49fbfed4de08726ec0e57e22f3b0d4c88439e23aa0b` | 0 |
| zebra-rpc/src/queue.rs | 11436 | `3cb47ea763a62686c5d3521a38ea5cd17caaf3c73b6f6097f7544040d3fec4d7` | 0 |
| zebra-rpc/src/server.rs | 8462 | `d091d3e58859f87b225ec8fd7602ac7329018de95b6a1cebdccda672b3714efa` | 0 |
| zebra-rpc/src/server/cookie.rs | 2403 | `27bbc9950d8bcf4205bb70855b524a6c50094c7701ce6b537b8bd95e9d42ccbf` | 0 |
| zebra-rpc/src/server/error.rs | 4427 | `8f0442b00c49678db3eed2d373b9c62b3e0fbf0f71f3b42e65f78ce418d95f21` | 0 |
| zebra-rpc/src/server/http_request_compatibility.rs | 13127 | `322d240680f9a084e834501e814e5b7494f929108dc58e38b60160e41980248c` | 0 |
| zebra-rpc/src/server/rpc_call_compatibility.rs | 6616 | `3821156f7d0b7a65297d9d82ed99c2e30802563175cba5dd01ef085cbc38932e` | 0 |
| zebra-rpc/src/server/rpc_metrics.rs | 4027 | `2a2ced4880a96e25f122595c3b73a1e78ea294c3555621ba7bfb963fb8e19c83` | 0 |
| zebra-rpc/src/server/rpc_tracing.rs | 3660 | `5a12bafac5019423ff20854407cb9755b325c271ecdedfc1a4b81394663ca3d9` | 0 |
| zebra-rpc/src/sync.rs | 29922 | `8cd437859f39b271643cd7a0230ec79dbd78c28ec90ec8115f709ca7b1e059d6` | 0 |
| zebra-script/Cargo.toml | 1451 | `a7877eb8f872c67f2ce79f5ae936baf243a6a8992c0a5f97f9461b9f749b0cef` | 0 |
| zebra-script/src/lib.rs | 19139 | `8e3e24c4c68f464e628e25f722f68a6f5d7a8c37f4ea4562c8e060178e63fd97` | 0 |
| zebra-state/Cargo.toml | 3444 | `5b64a2d0c0fff829a720054b2d28caa2d7576da3c3909fee5d581c22ea754102` | 0 |
| zebra-state/src/arbitrary.rs | 3743 | `4385f83332b6ff6fc77ea3598b60b5544ab058c58c47117faccf67c2620c9628` | 0 |
| zebra-state/src/config.rs | 22511 | `e9b28f9ef9e0add64b337f1a2c2fb2450de73c2d5e2828e377ec7e9d00ad393b` | 0 |
| zebra-state/src/constants.rs | 6446 | `a355d3f1b07f3a82ca673d80deab163b22c479b45558f5ea8a584abc5aeb0f5c` | 0 |
| zebra-state/src/error.rs | 29378 | `15c39917660edc96a60a84cc33ef7d66a4b3708b7d4a6d06984c9be098aa184b` | 0 |
| zebra-state/src/lib.rs | 3454 | `c685d45f261106f61aed627db3f9f8d4d447731d3a58981fd3d88280cef6826c` | 0 |
| zebra-state/src/request.rs | 73952 | `819b801382a2fe1dfa3a1e1dd240be9832662779c96cc4f338935b3239443a0e` | 0 |
| zebra-state/src/response.rs | 27434 | `a18cc3f68271c6c1e959df2f9791f0d59f3ad32c35099066495420dd3577fa95` | 0 |
| zebra-state/src/service.rs | 89598 | `e55de008aabc58d32acd2aa5db926a4b8a1abad25785e635354b72410d3b1046` | 0 |
| zebra-state/src/service/arbitrary.rs | 9145 | `40d69854b7c961e248194fac9726bdea0716b7204bc421cd07341e943e1416ba` | 0 |
| zebra-state/src/service/block_iter.rs | 6661 | `a04b688c87babc2b397b51088d5c5a73c28aeab90c3b13d094f69a90666a1f0c` | 0 |
| zebra-state/src/service/chain_tip.rs | 26686 | `19318cb5a1de6743264aaea1267e4042f45d0e8112b923f4cf4fecbda3e066d3` | 0 |
| zebra-state/src/service/check.rs | 18459 | `5e7db52f0d578345d34f1ef1f1a8b65ca3d86ac4cb1dfee24848b173a8e3abdc` | 0 |
| zebra-state/src/service/check/anchors.rs | 19417 | `6e4699c1c092aadfa6f75a67b5543792051eae0f45f3e4e7b5e99efbe6e6f72b` | 0 |
| zebra-state/src/service/check/difficulty.rs | 16820 | `7e21f95a20446bd5c719a0f5febceda95a41523589e0831222ec1d02a318b9ba` | 0 |
| zebra-state/src/service/check/nullifier.rs | 9082 | `749be77f30b15da3e68f4471d8994056e4518c0adacac9009f76adccc94a77a7` | 0 |
| zebra-state/src/service/check/utxo.rs | 11844 | `e165110675ff77ec5e4144527c63b564e43de69f568349bdf50e0dd2206306f5` | 0 |
| zebra-state/src/service/finalized_state.rs | 26964 | `e2058ef9a866ba28f1088d126cb8e08baeeb2747197650b0e2c4135c41b6e83a` | 0 |
| zebra-state/src/service/finalized_state/arbitrary.rs | 1984 | `dac47f5015238073f5e19e2823150c552d8a173fb1c38482c165a10c54e7ca3d` | 0 |
| zebra-state/src/service/finalized_state/column_family.rs | 10664 | `16ba1885be079d656ae288444356b899a1f5c8272627ea0270e3e340ce8d80dd` | 0 |
| zebra-state/src/service/finalized_state/disk_db.rs | 67360 | `2e8195b747134db362606f9a0ca1431e997c81bbbef53c815564f2dcff081785` | 0 |
| zebra-state/src/service/finalized_state/disk_format.rs | 5344 | `d60a25b81ddddcd06478afeef7d7f80f53e33d8424ee5519b6869017e724965c` | 0 |
| zebra-state/src/service/finalized_state/disk_format/block.rs | 11557 | `c915f7db3d7e447fb8c682ce9460d88a5cf9a3c013ab1dbd0bf612352ff1222e` | 0 |
| zebra-state/src/service/finalized_state/disk_format/chain.rs | 8404 | `bc3a868af5b0c7c567f92f8fd57b08e7bec176b3a682ba36935f67c22627a8fd` | 0 |
| zebra-state/src/service/finalized_state/disk_format/shielded.rs | 6227 | `5be1b8b9f01b8f92544d699501f36c38837f5e4d768aaed03c44d85723765e73` | 0 |
| zebra-state/src/service/finalized_state/disk_format/transparent.rs | 32712 | `8f49aa674fae2967ed6eb741a6fd465f1194975dee63d59c43195d3910759b4f` | 0 |
| zebra-state/src/service/finalized_state/disk_format/upgrade.rs | 34142 | `bfdca0019cf7fc9f849469f4d571d7d7b2189d66f17a5e81d441dc390d87f162` | 0 |
| zebra-state/src/service/finalized_state/disk_format/upgrade/add_ironwood_tree.rs | 4058 | `129f367d5e30958aadf3b2a181b71b9aa903d4ecf87289b7246310728b0fbffa` | 0 |
| zebra-state/src/service/finalized_state/disk_format/upgrade/add_subtrees.rs | 36415 | `633e1a6cc2e31b2b6cd84fd0511006dd475787511816548e1353511f2cdfc8ab` | 0 |
| zebra-state/src/service/finalized_state/disk_format/upgrade/block_info_and_address_received.rs | 12654 | `a8c927868d47fc4403f52f06703190b14556736a0bf6623917843a40714d5238` | 0 |
| zebra-state/src/service/finalized_state/disk_format/upgrade/cache_genesis_roots.rs | 6316 | `358c1b99b73cf022bb032bfead1da247bf3e05a0f8be178b0d7213b6ff989dcf` | 0 |
| zebra-state/src/service/finalized_state/disk_format/upgrade/drop_tx_locs_by_spends.rs | 2399 | `f0ee95b702f14faf8c15d7bcd63e96169c40a1c5493e118fb4e2c6d6777f8b0c` | 0 |
| zebra-state/src/service/finalized_state/disk_format/upgrade/fix_tree_key_type.rs | 5316 | `2fe6d0b5b4ff4cd8cea2ffc4d2568e902fbac61a544f79c15799ba7816baf1c4` | 0 |
| zebra-state/src/service/finalized_state/disk_format/upgrade/no_migration.rs | 1243 | `631b361bf44bf5a8273943821d816f7cb94bc9812c5e6b60d5c59e8cbec16e1a` | 0 |
| zebra-state/src/service/finalized_state/disk_format/upgrade/prune_trees.rs | 5330 | `3386c552662ef780579749f012a6095eebfef1166ff3b3d7115fba457d6c0c92` | 0 |
| zebra-state/src/service/finalized_state/disk_format/upgrade/track_tx_locs_by_spends.rs | 3959 | `32288068ac736fb662d4bb1efe47efe197c6ac372ec511b1ffaef6aa6e8d559b` | 0 |
| zebra-state/src/service/finalized_state/disk_format/upgrade/tree_keys_and_caches_upgrade.rs | 1795 | `4c77ec574152a4911e501c644adbbf6655cfc98b3f85cc52fbf5a7214fa243f3` | 0 |
| zebra-state/src/service/finalized_state/zebra_db.rs | 17407 | `2d4b60deba1582b2db7cdecb63ce7ad2ca6b57fab08b7d36df8457cfb160b271` | 0 |
| zebra-state/src/service/finalized_state/zebra_db/arbitrary.rs | 2745 | `9a73a46fc0b4001f9da6525b5ffedd0dae4d795a733ec4cb3fadafc43af6f89c` | 0 |
| zebra-state/src/service/finalized_state/zebra_db/block.rs | 29154 | `0acff88f1145be9bbd7310f1af9ba079a51e9cb714f22e98f0dabe2076481af0` | 0 |
| zebra-state/src/service/finalized_state/zebra_db/chain.rs | 12542 | `fe325e785bdbbd0604cb15ba3387987688122c973ab2b1dd8ca80ce8ad9676ec` | 0 |
| zebra-state/src/service/finalized_state/zebra_db/metrics.rs | 4165 | `aeb82941b63d769625c5538ad77cb5164b6ecec35efd9c5f16ed3ac673f08b5a` | 0 |
| zebra-state/src/service/finalized_state/zebra_db/shielded.rs | 39719 | `70753fe5df387b775d4a67cf3ef37844b2ec6a854537f04f5e58c285643adf49` | 0 |
| zebra-state/src/service/finalized_state/zebra_db/transparent.rs | 37562 | `ef3e4244939bf6bc6b2d926473ea1aa15d7e971982790f8ebd25c35ae35f225a` | 0 |
| zebra-state/src/service/non_finalized_state.rs | 44387 | `ad078fbb3820508e7d3bfb73808079410eefc850defae6953c9735fb07034bb9` | 0 |
| zebra-state/src/service/non_finalized_state/backup.rs | 12980 | `dfb6b760333bf2a7d0cf9335e99e9237b4e97e2a945ab51d3daccc032f546a77` | 0 |
| zebra-state/src/service/non_finalized_state/chain.rs | 99848 | `45a866fc6aa9a25b33b3f3d0fe9c9e7b6b342321c053fb98cc627510c2e652d9` | 0 |
| zebra-state/src/service/non_finalized_state/chain/index.rs | 12771 | `875806ff47630be0417e01afd0cb55f5703efb1316c638f30aed51a205d53cf0` | 0 |
| zebra-state/src/service/pending_utxos.rs | 2447 | `e4e6bcb31580ecb4149bd73f6e29b4c25c26e851e505eed11903ad854a864c5c` | 0 |
| zebra-state/src/service/queued_blocks.rs | 18212 | `a72e3b8224116ade6e374046d8b1e9cb02e81604a770775faf5685e4e6e923cd` | 0 |
| zebra-state/src/service/read.rs | 1967 | `c97d9377ed551ec9a1c5840269283ab660bd9657354770f86be0ac411839859b` | 0 |
| zebra-state/src/service/read/address.rs | 76 | `7322803accbf92cdda3465716747331dfe4ff312d5e114dec63a0a4b1682a07f` | 0 |
| zebra-state/src/service/read/address/balance.rs | 5446 | `d508b7f7cd3d6fb7072c285a24b63cd0a5cb686b45e69378f56a186e38a05bec` | 0 |
| zebra-state/src/service/read/address/tx_id.rs | 11271 | `3a64ace37573d494cf7ba05cb18bce81b9792992abc1c8b8a56d986455346d83` | 0 |
| zebra-state/src/service/read/address/utxo.rs | 22150 | `f5da3cfa0f19649587aec3894bb935837bbfe78feea1d922b6af6c07f06f2d48` | 0 |
| zebra-state/src/service/read/block.rs | 16716 | `91a1a61d0efb0303ce9ee330e03450caf02f660fb249157290bc5f959d135efd` | 0 |
| zebra-state/src/service/read/difficulty.rs | 23109 | `d3cb7d54208bb38859f4d90d75a865e7f112097c953a8fc71c7ffd92e6193306` | 0 |
| zebra-state/src/service/read/find.rs | 24184 | `c71cac21cf69336d842f9134fc29702e576698aadbbbd4b80ffae8a7f5e7bf88` | 0 |
| zebra-state/src/service/read/tree.rs | 13003 | `2acc5833a4623a19535b72674ebf2d16b812213662d04e10b9b78100e6fd3e7e` | 0 |
| zebra-state/src/service/traits.rs | 844 | `45b3d542f053bd8051ba7a0a09c4bbcf1c52e085db3ccdd207d548dffe1ee20e` | 0 |
| zebra-state/src/service/watch_receiver.rs | 5221 | `d7b19a5e719c87955d199c47342f841b5debb9d1f12a5645fe48e5a59017f1a0` | 0 |
| zebra-state/src/service/write.rs | 21424 | `32d969a4deceeecf356111601ea53c6a769969b8fd501a94f4d799e78325e958` | 0 |
| zebra-utils/Cargo.toml | 2479 | `4cd13d8311ff49ef02b5bbe0a4bf173206a877620d18268ac1cc74fed3e1d901` | 0 |
| zebra-utils/src/bin/block-template-to-proposal/args.rs | 1124 | `292747763d9a0cac875df0db80332121dca5196023ec15412052b559d6ea307a` | 0 |
| zebra-utils/src/bin/block-template-to-proposal/main.rs | 3341 | `acd70253ff5be567fb201bd1dcf9c22ea67b6356850e3c57dbf1300e7881eb37` | 0 |
| zebra-utils/src/bin/search-issue-refs/main.rs | 11383 | `4bf797fa77f1aa361f1b1c0961c75fb430323a724391722226a2c2c3b4a221c1` | 0 |
| zebra-utils/src/bin/zebra-checkpoints/args.rs | 4235 | `82749ca2aff21f997852631d2f52eacc50f45b363703d893e181f757929031dc` | 0 |
| zebra-utils/src/bin/zebra-checkpoints/main.rs | 10779 | `e12afab038dd4d963a578c7f13363e41474b8c7b35cd854b37ff9db342a42f5d` | 0 |
| zebra-utils/src/lib.rs | 569 | `57751376f2086415d8daf5d91199b1b6acea7db7aa965a7a656a3958dd0ee319` | 0 |
| zebrad/Cargo.toml | 11898 | `5009e65e19acd07abc76242e6985e58af12392f4212cd8a0fd2a43949321c673` | 0 |
| zebrad/build.rs | 2801 | `bf2e6e5ed85c550e066f76d09358ba6556ee9888b325eaa0f795966900e70093` | 0 |
| zebrad/src/application.rs | 24460 | `e8c626c846beb2a7d0ddc7fe4c62e536ce4221a18535f1f809aeee2abf837f0b` | 0 |
| zebrad/src/bin/zebrad/main.rs | 615 | `b4a238827f3c997a0480f55ca11091cf38bd96c10a15230fac179b7f1da5497a` | 0 |
| zebrad/src/commands.rs | 4461 | `a1226fcce74583a5b315f6a17eb15397a96cd490a9cac5864e7f4b69e46a0e39` | 0 |
| zebrad/src/commands/copy_state.rs | 16366 | `a0f607a11e34724f69b00cd48ffb0128d5ccd9d249c463762d774143ca8640b1` | 0 |
| zebrad/src/commands/entry_point.rs | 3919 | `ffcec92681b4fc230be1f57caa5e9a5f2da1ff850f5a305220fbf6d63345bf4f` | 0 |
| zebrad/src/commands/generate.rs | 3607 | `4fe97463036fb18c5c1eacb957d94a7a216517bf61e6a28f53c8abe41c22257f` | 0 |
| zebrad/src/commands/start.rs | 50122 | `09f04051904bd18e5b9d48fbd3b8a10eb1368b09d902593fa1fdf719a95b43ed` | 0 |
| zebrad/src/commands/tip_height.rs | 2075 | `2b081aac7ecb4216fa309092e165920e2418425048f13f1b276d66c85eb4a647` | 0 |
| zebrad/src/components.rs | 838 | `c17d1c9751ee8e18b042702b60af0a494630ffa291728d9e78f1dffca7328043` | 0 |
| zebrad/src/components/health.rs | 12857 | `479a0f58078467c0e7915023852303922d844dc72a5928aa78fa60bb5493bbd6` | 0 |
| zebrad/src/components/health/config.rs | 1414 | `f6167e6458048f08b2ad95d0b49126d5475d8a8765a3342c3f1062acb3f8345a` | 0 |
| zebrad/src/components/inbound.rs | 30028 | `e298cc9545b1c65950d500e58bc7cfbbbb9461c86555c8129686e10bf4630fbc` | 0 |
| zebrad/src/components/inbound/cached_peer_addr_response.rs | 3718 | `5a64415750b63e0e31ab7d95ed5707557c3d4edd666fa16c60d92792f57384d3` | 0 |
| zebrad/src/components/inbound/downloads.rs | 24041 | `e98333a03cad20d8097dc59fde005e296877dfc55ff361976121c895049e7224` | 0 |
| zebrad/src/components/mempool.rs | 48032 | `f4d5a3c3e984201e3f89788de2e922a5d93e42ea6f61dea13e434d64de39467d` | 0 |
| zebrad/src/components/mempool/config.rs | 3115 | `cf47f56cd0540fd0aae98d5a6b9049903a7770b428fc14e9067143e53cdbbac4` | 0 |
| zebrad/src/components/mempool/crawler.rs | 10379 | `6738235e04f548f3e1dde890ed42a958fdadac681c420c208d8c56dba62a0dc1` | 0 |
| zebrad/src/components/mempool/downloads.rs | 27739 | `725e13e314d39f9671be2d7d361bb23d5c7d84573fc3edfe46b236ba03ba03f4` | 0 |
| zebrad/src/components/mempool/error.rs | 3362 | `fc2a8f1602a7ad6b8f39eac699938685deda9dcaf5e722473e81e39a0d4b7d46` | 0 |
| zebrad/src/components/mempool/gossip.rs | 4912 | `c2918e119119042163ac700837d0fd015dd55ec7aa6c08ba1bb96265afb30efe` | 0 |
| zebrad/src/components/mempool/pending_outputs.rs | 2309 | `0f35179be39c78ff5cfbed9807c4a65bb28f8513fa53439c0b5268d02fb7e51a` | 0 |
| zebrad/src/components/mempool/queue_checker.rs | 2896 | `9dea92e21ed3ed08842d055725b4ad44ca8ca90059ce69bcf725734e0126a6e6` | 0 |
| zebrad/src/components/mempool/storage.rs | 39586 | `608fe5e3849a0cbc8d214661d147c92e0c67038206c69ab5596bf5a4b17c227c` | 0 |
| zebrad/src/components/mempool/storage/eviction_list.rs | 5492 | `cd2e406b864977498110f1d9a78b5ea089cf59d6e963873fa366832f22660fb6` | 0 |
| zebrad/src/components/mempool/storage/policy.rs | 14196 | `89fdd3a1723f56d15848ea5b4836cc0153d69d33a54821fae565496e4721f45e` | 0 |
| zebrad/src/components/mempool/storage/verified_set.rs | 19581 | `1d2355c61bc7cd504bcae3704ea218a1f7f5828dc9ae544c40ec224063a9b7d7` | 0 |
| zebrad/src/components/metrics.rs | 2775 | `e5f414f200ff61ac6b7e43ffd798848c830c8fdb2f5d57d5d274d27a4e805d64` | 0 |
| zebrad/src/components/miner.rs | 22597 | `8929f63db7eb43e30d416c52b61b34f9749ba4bc611fdc6d56a8675187fc75ed` | 0 |
| zebrad/src/components/notify.rs | 7218 | `37581938e8cd8cd279c799278ad711266cf4566cde1417bbc524593e41fcf9c9` | 0 |
| zebrad/src/components/sync.rs | 69320 | `cd8dbc4c6a466d4905b8b56b44676efbbf670d72133c7b38a97baeddbd6fa260` | 0 |
| zebrad/src/components/sync/downloads.rs | 30750 | `876a9233e37317b7a07fc29067763766c1f1659c9d2ad9511e0151665bdd671c` | 0 |
| zebrad/src/components/sync/end_of_support.rs | 4448 | `51d368743189e923cfbb506e04b5f84b1b5aa04ce8175606a985ed8b9a3a9875` | 0 |
| zebrad/src/components/sync/gossip.rs | 9570 | `53d2494a541b11685b8f8359fb29e71af484aaa6d3d2dee33e0c08040a2774f0` | 0 |
| zebrad/src/components/sync/hedge.rs | 7930 | `20bb9eb249654b096888376c28b97c886e15cfe7d8d39d70d203254fee4daf8c` | 0 |
| zebrad/src/components/sync/progress.rs | 17110 | `413575e4caa05f3319ac7d866bdd22c18370021cc0837f7be8af4af4202d6ca1` | 0 |
| zebrad/src/components/sync/recent_sync_lengths.rs | 3461 | `c914e79f9004b0c00ab7b55098845e60de8eb2b50cd175b441e6823c2cdecb57` | 0 |
| zebrad/src/components/sync/status.rs | 3302 | `dea341fd74e3702ff529e96e46322eae4cfb46fe0dde9440780b3bcb3d010e89` | 0 |
| zebrad/src/components/sync/status/mock.rs | 985 | `3d00fc970c96832beb0bc9269494692980639e55ef44d6f4cada5f9fe624c440` | 0 |
| zebrad/src/components/tokio.rs | 5744 | `664a837a178bd3d8f9800aaafb55eb7584f3e86530de46f3998e1a4bba0630cf` | 0 |
| zebrad/src/components/tracing.rs | 11997 | `58a5e65a0625cfc4ea48d4e809005bea39bb0a915ea8668f581a925f179a0c29` | 0 |
| zebrad/src/components/tracing/component.rs | 20990 | `606674e14b908fee082c838e4fc2c0db081fa23c393d649879f68aeb8ee62d11` | 0 |
| zebrad/src/components/tracing/endpoint.rs | 5790 | `041160c0d76ca1ac93924d214b2ead8ebe021d85af2d81900b96102c7e46bbde` | 0 |
| zebrad/src/components/tracing/flame.rs | 1284 | `0f405afc0d1d047e2673f5f7461ebcef22f72100209e8079a7cac768ea5cef70` | 0 |
| zebrad/src/components/tracing/otel.rs | 3877 | `c701aa2660b3036ad8644d9cfc5617a7ce89548206bb5ef98f6dfa7a7eb69aac` | 0 |
| zebrad/src/components/zcashd_compat.rs | 919 | `9915d1f955a02c290e4bacfbc1159cecb2fbf07f2969bfbb6c02708537da8317` | 0 |
| zebrad/src/components/zcashd_compat/config.rs | 11346 | `25491271b3035609008bbc38a4232d61795e86bab316066af0cedf904b72d6bd` | 0 |
| zebrad/src/components/zcashd_compat/datadir.rs | 21111 | `4d5e76b865d078fe3380b71ecc841db52e7e6b9b07e632dfd6321b4f8579627a` | 0 |
| zebrad/src/components/zcashd_compat/managed.rs | 31634 | `49205c41376f20657cc3a22a33c7f0fc5bf32fbe6ce14c66e96bc42d191ef948` | 0 |
| zebrad/src/components/zcashd_compat/manifest.rs | 3720 | `0f65a7929bff4a42f02e79562389524137ee0ffd4c7e673e7def3b90ae1c188e` | 0 |
| zebrad/src/components/zcashd_compat/preflight.rs | 49050 | `367a84fcd608aa60318b05e32fb15f0bae97fe61a469fa14e364335f8203fd2a` | 0 |
| zebrad/src/components/zcashd_compat/supervisor.rs | 39059 | `45af07d79069d559c694f628a70a12678542da82bc0d2fa69d864ccd08d39311` | 0 |
| zebrad/src/config.rs | 8478 | `f855468bf1695ae8f653573bafb9da3d97a4daaa75c9678be5c37915526542b3` | 0 |
| zebrad/src/lib.rs | 7582 | `1dc46a83cc05319f39a9db483964f3193f877b356caf6654da36bd8f0e57646f` | 0 |
| zebrad/src/prelude.rs | 307 | `02129974f3ab542a5807384e0ac63a5c00681fbfec9fe3349028c78e7b9b6886` | 0 |
| zebrad/src/sentry.rs | 34587 | `d08e1a7cd0dbd01c61934c391fc0cb85aa9038a0e2316b2c0bc06872ea3f2ca8` | 0 |
