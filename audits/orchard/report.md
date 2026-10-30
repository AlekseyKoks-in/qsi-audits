# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** orchard @ 616a669df8c9 · Electric Coin Company (Zcash) — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-29 23:44 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 0cc500f4-9a7d-4d9d-946a-1fe4829c79a6 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `638cc4f1f581e5f8f4b801f9303b6938cf0c446fb09c5fc6e07d71953fd31043` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **0**
- Средняя: **6**
- Низкая: **4**
- Информационная: **6**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 5
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 5
- Рекомендация по улучшению: 5
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/zcash/orchard> @ `616a669df8c9a59c33d47064d3ce04b25d026b2e` — ссылки в доказательствах открывают строки на этом коммите.

49 файлов, всего 1692129 байт, редактирований: 0; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| dependencies | проверено | 2 | Cargo.lock: 341 dependencies parsed (341 pinned); Cargo.toml: 43 dependencies parsed (0 pinned) |
| source_code | проверено | 46 | src/action.rs: 392 lines scanned with 16 rule patterns and 128 registry patterns; 205 lines in #[cfg(test)] modules ignored; src/address.rs: 101 lines scanned with 16 rule patterns and 128 registry patterns; 20 lines in #[cfg(test)] modules ignored; src/builder.rs: 3316 lines scanned with 16 rule patterns and 128 registry patterns; 1149 lines in #[cfg(test)] modules ignored |
| osv_advisories | проверено | 1 | 341 pinned packages queried at OSV.dev; 11 affected (2 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree orchard at 616a669df8c9a59c33d47064d3ce04b25d026b2e. 49 files analysed; of 109 files, 20 are test, fuzzing, benchmark or example code and were left out, 40 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .github/workflows/bench.yml, .github/workflows/book.yml, .github/workflows/ci.yml, .github/workflows/lints-beta.yml, .github/workflows/lints-stable.yml. 30 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **91** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 59.4%

## 7. Подробное описание находок

### QSI-2026-07278 — Квантово-уязвимый Pedersen commitment: пороговая подпись и протоколы MPC (14 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Pedersen commitment:threshold_mpc`
- Источник данных: src/action.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

98 упоминаний Pedersen commitment в 14 файл(ах), например src/action.rs:12. Роль по путям, именам функций и соседнему коду: пороговая подпись и протоколы MPC. Paillier, обязательства Педерсена и доказательства на дискретном логарифме внутри пороговых ECDSA и EdDSA ломаются алгоритмом Шора; постквантовая пороговая схема — это смена протокола, а не параметра.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/action.rs:12 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/action.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/action.rs#L12) · line 12 · SHA-256 e5d8830b9f60595446d63c29d4904e1b0929f88ea9cc24cedf1f95113d96aa54_

```
   11 |     primitives::redpallas::{self, SpendAuth},
   12 |     value::ValueCommitment,
   13 | };
```

_file_excerpt · [src/action.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/action.rs#L35) · line 35 · SHA-256 972403f772b62fb7f315b39c8842d56e99d3bf5e0aac977ceb207f4bad05cae6_

```
   34 |     /// A commitment to the net value created or consumed by this action.
   35 |     cv_net: ValueCommitment,
   36 |     /// The authorization for this action.
```

_file_excerpt · [src/action.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/action.rs#L62) · line 62 · SHA-256 824f61a2a3abdd887f8106d29a20c9778b28a3a1eb7379cc89164222a8bba71e_

```
   61 |         encrypted_note: TransmittedNoteCiphertext,
   62 |         cv_net: ValueCommitment,
   63 |         authorization: T,
```

_file_excerpt · [src/builder.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/builder.rs#L23) · line 23 · SHA-256 82bbd588ddd2f3212ccfc607449a81f488a0f4a1c15bdd6d1d14502fa12e6553_

```
   22 |     tree::{Anchor, MerklePath},
   23 |     value::{self, BalanceError, NoteValue, ValueCommitTrapdoor, ValueCommitment, ValueSum},
   24 |     Proof,
```

_file_excerpt · [src/builder.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/builder.rs#L561) · line 561 · SHA-256 bf43470bb74580f5684224cdf375be40ae62938b5cb7d392e1c963506647113b_

```
  560 |         &self,
  561 |         cv_net: &ValueCommitment,
  562 |         nf_old: Nullifier,
```

_file_excerpt · [src/builder.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/builder.rs#L600) · line 600 · SHA-256 b8bc237c3ba4c3e6683dbdf21c8e8fddf2b5ddcf3d157a293e4d6b3410574036_

```
  599 |         self,
  600 |         cv_net: &ValueCommitment,
  601 |         nf_old: Nullifier,
```

_file_excerpt · [src/bundle.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/bundle.rs#L30) · line 30 · SHA-256 9657b354fe5a1def177280be196c1d882e0269df8475a49977833b6ed8a30bb2_

```
   29 |     tree::Anchor,
   30 |     value::{ValueCommitTrapdoor, ValueCommitment, ValueSum},
   31 |     Proof, ProtocolVersion, ValuePool,
```

_file_excerpt · [src/bundle.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/bundle.rs#L773) · line 773 · SHA-256 65682451219d3eeaaf00c0b737928e8685d5b814d76d992c118d59a95d721ae0_

```
  772 |             .map(|a| a.cv_net())
  773 |             .sum::<ValueCommitment>()
  774 |             - ValueCommitment::derive(
```

_file_excerpt · [src/bundle.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/bundle.rs#L774) · line 774 · SHA-256 667aaf19ff04cd8e52e0be57a2c46c9694e11fc555cc16eb1233912af2444e54_

```
  773 |             .sum::<ValueCommitment>()
  774 |             - ValueCommitment::derive(
  775 |                 ValueSum::from_raw(self.value_balance.into()),
```

_file_excerpt · [src/circuit.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit.rs#L44) · line 44 · SHA-256 350ccda8f79df0f8ca95418c29b13ca81627d6d528168fab0603d8e7a1ef19d6_

```
   43 |     tree::{Anchor, MerkleHashOrchard},
   44 |     value::{NoteValue, ValueCommitTrapdoor, ValueCommitment},
   45 | };
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07279 — Квантово-уязвимый Halo 2 (IPA): роль не определена (16 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Halo 2 (IPA):general`
- Источник данных: src/builder.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

38 упоминаний Halo 2 (IPA) в 16 файл(ах), например src/builder.rs:175. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/builder.rs:175 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/builder.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/builder.rs#L175) · line 175 · SHA-256 aa83a0541362884c99cd3d1433eec24bc6c4475c901e2c35fa61d27a241a065f_

```
  174 |     #[cfg(feature = "circuit")]
  175 |     Proof(halo2_proofs::plonk::Error),
  176 |     /// An overflow error occurred while attempting to construct the value
```

_file_excerpt · [src/builder.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/builder.rs#L213) · line 213 · SHA-256 7a6ff77cfe4f75248f1186fbcbef8d52745123f76c045b8e3f8e2244390c2ddf_

```
  212 |             #[cfg(feature = "circuit")]
  213 |             Proof(halo2_proofs::plonk::Error::InvalidInstances) => f.write_str(
  214 |                 "Could not create proof: provided instances do not match the circuit, or \
```

_file_excerpt · [src/builder.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/builder.rs#L263) · line 263 · SHA-256 a5ee79a37e37bfee599723658b682905117aa8e496e2ff64ea07eac3cf1e7b6f_

```
  262 | #[cfg(feature = "circuit")]
  263 | impl From<halo2_proofs::plonk::Error> for BuildError {
  264 |     fn from(e: halo2_proofs::plonk::Error) -> Self {
```

_file_excerpt · [src/bundle.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/bundle.rs#L994) · line 994 · SHA-256 b85407df5b82b26e5f80fbcacf4d713d31af30e8f446961c0fe8e5e0cf6e9f79_

```
  993 |     #[cfg(feature = "circuit")]
  994 |     pub fn verify_proof(&self, vk: &VerifyingKey) -> Result<(), halo2_proofs::plonk::Error> {
  995 |         self.authorization()
```

_file_excerpt · [src/bundle/batch.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/bundle/batch.rs#L4) · line 4 · SHA-256 b344fb383055e558ec2ee08c9aac997d0a054e34fdde166d7893a529801c5d6d_

```
    3 | 
    4 | use halo2_proofs::plonk;
    5 | use pasta_curves::vesta;
```

_file_excerpt · [src/circuit.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit.rs#L6) · line 6 · SHA-256 a5ec358aa8647a7a4521e411f7053ad1f909f4e4897f732e86819baae2a48a9d_

```
    5 | use group::{Curve, GroupEncoding};
    6 | use halo2_proofs::{
    7 |     circuit::{floor_planner, Layouter, Value},
```

_file_excerpt · [src/circuit.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit.rs#L46) · line 46 · SHA-256 67027352377c7215dca0e0220c2898dcfc4882e7a9d53d2d0fdeb0e073efb778_

```
   45 | };
   46 | use halo2_gadgets::{
   47 |     ecc::{
```

_file_excerpt · [src/circuit.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit.rs#L1084) · line 1084 · SHA-256 469460fd1efe3a59a4dcb07be54ba4465e76e25c1d61e4426fb9a829ad476467_

```
 1083 | pub struct VerifyingKey {
 1084 |     pub(crate) params: halo2_proofs::poly::commitment::Params<vesta::Affine>,
 1085 |     pub(crate) vk: plonk::VerifyingKey<vesta::Affine>,
```

_file_excerpt · [src/circuit/commit_ivk.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit/commit_ivk.rs#L11) · line 11 · SHA-256 e0dce980da151ec8b1d48997a87add72640da9eb8848c99094286856261ecdfb_

```
   10 | use group::ff::{Field, PrimeField};
   11 | use halo2_proofs::{
   12 |     circuit::{AssignedCell, Layouter, Value},
```

_file_excerpt · [src/circuit/commit_ivk.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit/commit_ivk.rs#L19) · line 19 · SHA-256 d691a5d17cf21c26fa80b85ace59e4621e6696de2ad130975b848c2587fd9d8d_

```
   18 | use crate::constants::{OrchardCommitDomains, OrchardFixedBases, OrchardHashDomains, T_P};
   19 | use halo2_gadgets::{
   20 |     ecc::{chip::EccChip, ScalarFixed, X},
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07280 — Квантово-уязвимый RedDSA: роль не определена (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:RedDSA:general`
- Источник данных: src/bundle/batch.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

1 упоминаний RedDSA в 1 файл(ах), например src/bundle/batch.rs:141. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/bundle/batch.rs:141 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/bundle/batch.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/bundle/batch.rs#L141) · line 141 · SHA-256 cd05302928e4635fd465edcdb188eb27d7b531b4c24d08727d7cb530c642440c_

```
  140 |             Err(e) => {
  141 |                 debug!("RedPallas batch validation failed: {}", e);
  142 |                 false
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07281 — Квантово-уязвимый Sinsemilla: роль не определена (9 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Sinsemilla:general`
- Источник данных: src/circuit.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

61 упоминаний Sinsemilla в 9 файл(ах), например src/circuit.rs:53. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/circuit.rs:53 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/circuit.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit.rs#L53) · line 53 · SHA-256 5cfdaf4aa8e3530135c304111a3ad9c253e74031e78b5c3c46d39f873ce7ff4c_

```
   52 |     poseidon::{primitives as poseidon, Pow5Chip as PoseidonChip, Pow5Config as PoseidonConfig},
   53 |     sinsemilla::{
   54 |         chip::{SinsemillaChip, SinsemillaConfig},
```

_file_excerpt · [src/circuit.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit.rs#L54) · line 54 · SHA-256 35cb3cc6b4ce753a858f7094a10cc562e7e8282bb89f6d7eba16def3a1e81e77_

```
   53 |     sinsemilla::{
   54 |         chip::{SinsemillaChip, SinsemillaConfig},
   55 |         merkle::{
```

_file_excerpt · [src/circuit.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit.rs#L105) · line 105 · SHA-256 ffc3a9cefb7347d291e61139893647a6d7c03e5eb7134ab6003c71089e45f863_

```
  104 |     merkle_config_2: MerkleConfig<OrchardHashDomains, OrchardCommitDomains, OrchardFixedBases>,
  105 |     sinsemilla_config_1:
  106 |         SinsemillaConfig<OrchardHashDomains, OrchardCommitDomains, OrchardFixedBases>,
```

_file_excerpt · [src/circuit/commit_ivk.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit/commit_ivk.rs#L21) · line 21 · SHA-256 e288e7407359fe86c8dfb11546b83d626e4495da73a5542b6d1ee1b793799ab3_

```
   20 |     ecc::{chip::EccChip, ScalarFixed, X},
   21 |     sinsemilla::{chip::SinsemillaChip, CommitDomain, Message, MessagePiece},
   22 |     utilities::{bool_check, RangeConstrained},
```

_file_excerpt · [src/circuit/commit_ivk.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit/commit_ivk.rs#L261) · line 261 · SHA-256 f3a1b25ca018b62f8f7ae98c67dcafde74a4ca70019a617818d61af487becc65_

```
  260 |     pub(in crate::circuit) fn commit_ivk(
  261 |         sinsemilla_chip: SinsemillaChip<
  262 |             OrchardHashDomains,
```

_file_excerpt · [src/circuit/commit_ivk.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit/commit_ivk.rs#L273) · line 273 · SHA-256 bb5744fcd3a4303abe48dd365fd01940038f6ae7b2f3ebd305f25799e2bece09_

```
  272 |     ) -> Result<X<pallas::Affine, EccChip<OrchardFixedBases>>, Error> {
  273 |         let lookup_config = sinsemilla_chip.config().lookup_config();
  274 | 
```

_file_excerpt · [src/circuit/gadget.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit/gadget.rs#L20) · line 20 · SHA-256 197036e6dc95da5e1c46294e6464d7e201c68884abc672861bec1a9cdd0a3309_

```
   19 |     },
   20 |     sinsemilla::{chip::SinsemillaChip, merkle::chip::MerkleChip},
   21 | };
```

_file_excerpt · [src/circuit/gadget.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit/gadget.rs#L46) · line 46 · SHA-256 68451e2605261fd9ccef4ef33d6d3061da2e1721512fe5543fe00362cdc038fc_

```
   45 | 
   46 |     pub(super) fn sinsemilla_chip_1(
   47 |         &self,
```

_file_excerpt · [src/circuit/gadget.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit/gadget.rs#L48) · line 48 · SHA-256 0e7e45ddcf19d38afa525a0ba29131ecdf8c513e66bfb166e642678bd6da0c1d_

```
   47 |         &self,
   48 |     ) -> SinsemillaChip<OrchardHashDomains, OrchardCommitDomains, OrchardFixedBases> {
   49 |         SinsemillaChip::construct(self.sinsemilla_config_1.clone())
```

_file_excerpt · [src/circuit/note_commit.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/circuit/note_commit.rs#L28) · line 28 · SHA-256 301d50ca2c9b51fc5eb073ab9d33caa643b759c469eb7005174941ee14ba6945_

```
   27 |     },
   28 |     sinsemilla::{
   29 |         chip::{SinsemillaChip, SinsemillaConfig},
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07282 — Квантово-уязвимый RedDSA: аутентификация и идентификация (сертификаты, токены, аттестация устройств) (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:RedDSA:authentication`
- Источник данных: src/primitives/redpallas.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

14 упоминаний RedDSA в 1 файл(ах), например src/primitives/redpallas.rs:11. Роль по путям, именам функций и соседнему коду: аутентификация и идентификация (сертификаты, токены, аттестация устройств). Краткоживущая аутентификация безопасна до появления CRQC; долгоживущим идентификаторам (аттестация устройств, ключи УЦ и SSH) план нужен раньше.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/primitives/redpallas.rs:11 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/primitives/redpallas.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/primitives/redpallas.rs#L11) · line 11 · SHA-256 20b6c92840064dacb9b8f031eeaf5f58e8cf7007b1806e45b2bbe3db75ffaed7_

```
   10 | #[cfg(feature = "std")]
   11 | pub use reddsa::batch;
   12 | 
```

_file_excerpt · [src/primitives/redpallas.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/primitives/redpallas.rs#L17) · line 17 · SHA-256 e55901da5d1f5bf297e719b3ebb973481517bcb88cea54bd0fc519a61ef00e84_

```
   16 | /// A RedPallas signature type.
   17 | pub trait SigType: reddsa::SigType + private::Sealed {}
   18 | 
```

_file_excerpt · [src/primitives/redpallas.rs](https://github.com/zcash/orchard/blob/616a669df8c9a59c33d47064d3ce04b25d026b2e/src/primitives/redpallas.rs#L20) · line 20 · SHA-256 ed5fe6cfa4b058c5b2858ece79aa91869d5bb15599ac1e81b25c0c8dbced81cd_

```
   19 | /// A type variable corresponding to an Orchard spend authorization signature.
   20 | pub type SpendAuth = reddsa::orchard::SpendAuth;
   21 | impl SigType for SpendAuth {}
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07291 — rustix 0.38.11 затронут GHSA-c827-hfw6-qwvm (CVE-2024-43806)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustix@0.38.11`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 6.5 (`CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-c827-hfw6-qwvm (CVE-2024-43806) для пакета crates.io rustix версии 0.38.11: rustix's `rustix::fs::Dir` iterator with the `linux_raw` backend can cause memory explosion. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-c827-hfw6-qwvm
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-c827-hfw6-qwvm](https://osv.dev/vulnerability/GHSA-c827-hfw6-qwvm) · manifest · SHA-256 9c2468db6c4225cd0b638f111cbc67a3f01a6b4433bdbe4c9b587cb7712c486e_

```
{"id": "GHSA-c827-hfw6-qwvm", "aliases": ["CVE-2024-43806"], "modified": "2026-09-10T03:50:03.698097046Z", "summary": "rustix's `rustix::fs::Dir` iterator with the `linux_raw` backend can cause memory explosion", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.35.15, 0.36.16, 0.37.25, 0.38.19).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07290 — rand 0.8.5 затронут GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rand@0.8.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 39.2 / 100
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

### QSI-2026-07285 — anyhow 1.0.75 затронут RUSTSEC-2026-0190 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/anyhow@1.0.75`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0190 для пакета crates.io anyhow версии 1.0.75: Unsoundness in `Error::downcast_mut()`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (anyhow::Error::downcast_mut); anyhow приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07286 — crossbeam-epoch 0.9.15 затронут RUSTSEC-2026-0204 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crossbeam-epoch@0.9.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0204 для пакета crates.io crossbeam-epoch версии 0.9.15: Invalid pointer dereference in `fmt::Pointer` impl for `Atomic` and `Shared` when the underlying pointer is invalid. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07287 — ctutils 0.4.2 затронут RUSTSEC-2026-0385 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/ctutils@0.4.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-07293 — 4 бюллетеней в 2 пакет(ах) crates.io, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:crates.io:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 15.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 4 бюллетеней (2 с оценкой high или critical) для 2 пакет(ов) crates.io, которые подтягивают только инструменты разработки или сборки (Cargo.lock): например, atty@0.2.14 [dev]: GHSA-g98v-hv3f-hcfr, RUSTSEC-2024-0375; quick-xml@0.26.0 [dev]: RUSTSEC-2026-0194, RUSTSEC-2026-0195. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в Cargo.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (crates.io)](https://osv.dev/) · Cargo.lock · SHA-256 e22695b368f9e87a47d361b015b702b9ae8607b8cc11a6f7193d4090df5e10c5_

```
atty@0.2.14 [dev]: GHSA-g98v-hv3f-hcfr, RUSTSEC-2024-0375
quick-xml@0.26.0 [dev]: RUSTSEC-2026-0194, RUSTSEC-2026-0195
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07283 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 13.3 / 100
- CVSS v3.1: неприменимо

В 2 манифестах зависимостей QSI нашёл криптобиблиотеки (bls12_381, ff, group, halo2_gadgets, halo2_poseidon, halo2_proofs, jubjub, pasta_curves, reddsa, sinsemilla, zcash_note_encryption, zcash_spec, zip32), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · Cargo.lock, Cargo.toml · SHA-256 93da48a60b7ceb57dadf6ec0ef009f1d4dfdf2016efcc6d2545211294f3efa4c_

```
Crypto libraries: bls12_381, ff, group, halo2_gadgets, halo2_poseidon, halo2_proofs, jubjub, pasta_curves, reddsa, sinsemilla, zcash_note_encryption, zcash_spec, zip32
```

**Ограничения проверки.** Отсутствие доказательств не является доказательством отсутствия: системные библиотеки и транзитивные зависимости могут не указываться.

**Рекомендация.** Определите источник поддержки PQC (TLS-терминатор, KMS/HSM, обновление библиотек).

**Повторная проверка.** Повторите сканирование после обновлений.

### QSI-2026-07284 — adler 1.0.2: информационный бюллетень RUSTSEC-2025-0056 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/adler@1.0.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 11.8 / 100
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

### QSI-2026-07288 — paste 1.0.15: информационный бюллетень RUSTSEC-2024-0436 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/paste@1.0.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:44 UTC
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

### QSI-2026-07289 — proc-macro-error2 2.0.1: информационный бюллетень RUSTSEC-2026-0173 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/proc-macro-error2@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:44 UTC
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

### QSI-2026-07292 — ttf-parser 0.20.0: информационный бюллетень RUSTSEC-2026-0192 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/ttf-parser@0.20.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:44 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2026-0192 для пакета crates.io ttf-parser версии 0.20.0 как информационный (unmaintained): `ttf-parser` is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0192
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0192](https://osv.dev/vulnerability/RUSTSEC-2026-0192) · manifest · SHA-256 d3f7ce2105a490b5cc0802ff198a1ca809120d266ed32b6200a30a1ab6d06752_

```
{"id": "RUSTSEC-2026-0192", "aliases": [], "modified": "2026-06-29T21:15:04.384453633Z", "summary": "`ttf-parser` is unmaintained", "severity": null, "declared_in_manifest": false}
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
| **пороговая подпись и протоколы MPC** | Pedersen commitment (14) | QSI-2026-07278 | Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли |
| **аутентификация и идентификация (сертификаты, токены, аттестация устройств)** | RedDSA (1) | QSI-2026-07282 | Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме |
| **роль не определена** | Halo 2 (IPA) (16), Sinsemilla (9), RedDSA (1) | QSI-2026-07279, QSI-2026-07280, QSI-2026-07281 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | Halo 2 (IPA) (16), Pedersen commitment (14), RedDSA (2), Sinsemilla (9) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | AES-256 (1), Poseidon (3) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Poseidon (3) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-07291 | Обновите rustix до исправленной версии (0.35.15, 0.36.16, 0.37.25, 0.38.19). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c827-hfw6-qwvm (CVE-2024-43806). |
| P2 | QSI-2026-07290 | Обновите rand до исправленной версии (0.10.1, 0.8.6, 0.9.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-07285 | Разберите RUSTSEC-2026-0190; при необходимости обновите anyhow до исправленной версии (1.0.103). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0190 или результат разбора записан. |
| P3 | QSI-2026-07286 | Разберите RUSTSEC-2026-0204; при необходимости обновите crossbeam-epoch до исправленной версии (0.9.20). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0204 или результат разбора записан. |
| P3 | QSI-2026-07287 | Разберите RUSTSEC-2026-0385; при необходимости обновите ctutils до исправленной версии (0.4.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0385 или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-07278 | Внесите использования Pedersen commitment в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07279 | Внесите использования Halo 2 (IPA) в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07280 | Внесите использования RedDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07281 | Внесите использования Sinsemilla в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07282 | Внесите использования RedDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-07278 | Запланируйте миграцию Pedersen commitment на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07279 | Запланируйте миграцию Halo 2 (IPA) на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07280 | Запланируйте миграцию RedDSA на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07281 | Запланируйте миграцию Sinsemilla на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07282 | Запланируйте миграцию RedDSA на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07293 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |
| P4 | QSI-2026-07284 | Замените adler поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | adler заменён или решение зафиксировано. |
| P4 | QSI-2026-07288 | Замените paste поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | paste заменён или решение зафиксировано. |
| P4 | QSI-2026-07289 | Замените proc-macro-error2 поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | proc-macro-error2 заменён или решение зафиксировано. |
| P4 | QSI-2026-07292 | Замените ttf-parser поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | ttf-parser заменён или решение зафиксировано. |

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
19. OSV advisory GHSA-c827-hfw6-qwvm — OSV.dev. <https://osv.dev/vulnerability/GHSA-c827-hfw6-qwvm> (modified 2026-09-10T03:50:03.698097046Z)
20. OSV advisory GHSA-cq8v-f236-94qc — OSV.dev. <https://osv.dev/vulnerability/GHSA-cq8v-f236-94qc> (modified 2026-09-10T03:50:43.958966498Z)
21. OSV advisory RUSTSEC-2024-0436 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0436> (modified 2026-01-27T22:03:15.694766Z)
22. OSV advisory RUSTSEC-2025-0056 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0056> (modified 2025-09-05T09:05:48Z)
23. OSV advisory RUSTSEC-2026-0173 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0173> (modified 2026-06-07T21:00:04.318567692Z)
24. OSV advisory RUSTSEC-2026-0190 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0190> (modified 2026-06-29T14:15:03.650725453Z)
25. OSV advisory RUSTSEC-2026-0192 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0192> (modified 2026-06-29T21:15:04.384453633Z)
26. OSV advisory RUSTSEC-2026-0204 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0204> (modified 2026-07-06T22:30:04.159269138Z)
27. OSV advisory RUSTSEC-2026-0385 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0385> (modified 2026-10-23T08:30:02.389575143Z)
28. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
29. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
30. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
31. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| AES-256 | AES-256 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/keys.rs:9 |
| Poseidon |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 3 | 3 | src/circuit.rs:52; src/circuit/gadget.rs:16; src/spec.rs:10 |
| Crypto library | 0.11.1 | jubjub (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | ff (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | group (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.2.0 | halo2_poseidon (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.2.0 | sinsemilla (sinsemilla) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.2.1 | zcash_spec (Zcash protocol crates) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.3.0 | zip32 (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.4.0 | halo2_proofs (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.5.1 | zcash_note_encryption (Zcash protocol crates) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.6.0 | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.6.0 | halo2_gadgets (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.6.1 | reddsa (reddsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.9.0 | bls12_381 (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14 | group (jubjub) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.14 | ff (jubjub) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.2 | sinsemilla (sinsemilla) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.2 | halo2_poseidon (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.3 | zip32 (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.4 | halo2_proofs (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.6 | reddsa (reddsa) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.6 | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.6 | halo2_gadgets (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Halo 2 (IPA) |  |  | уязвим (Шор) | допустимо | 16 | 16 | src/builder.rs:175; src/bundle.rs:994; src/bundle/batch.rs:4 |
| Pedersen commitment |  |  | уязвим (Шор) | допустимо | 14 | 14 | src/action.rs:12; src/builder.rs:23; src/bundle.rs:30 |
| RedDSA | RedPallas |  | уязвим (Шор) | допустимо | 1 | 1 | src/bundle/batch.rs:141 |
| RedDSA |  |  | уязвим (Шор) | допустимо | 1 | 1 | src/primitives/redpallas.rs:11 |
| Sinsemilla |  |  | уязвим (Шор) | допустимо | 9 | 9 | src/circuit.rs:53; src/circuit/commit_ivk.rs:21; src/circuit/gadget.rs:20 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| Cargo.lock | 81957 | `885baff50aa2e919620270de3b9f07f7333b0169c199869dcf2a7787b64505d8` | 0 |
| Cargo.toml | 4121 | `7e77f561f41a9f281617490ad26bd4c9776b25e8685d51727031016ea73c08ae` | 0 |
| rust-toolchain.toml | 66 | `c6a9ed2b4322e7dcd47629cee8a2ff9f25fb5e50e1041acce4cb4cf6aaff2a09` | 0 |
| src/action.rs | 14533 | `3f80c4d1ee3bed8fc4548c26fddd425c6727cea87758b4f4fe8843fec98902af` | 0 |
| src/address.rs | 3822 | `a0c93310d2fd64c0f2b32e0dfdf667e4e02b6f235852eed2ef07108b98012250` | 0 |
| src/builder.rs | 129594 | `4535e4fd73b38529e6d3ac88b337a335df35eb64734cba074a506554640a4a81` | 0 |
| src/bundle.rs | 72629 | `2b2071844373ac89aed0533ec5734ba9f241a977158ced05f9f1734b80215737` | 0 |
| src/bundle/batch.rs | 7297 | `3358e5fdd1400d3801b8df3b7ea36acd21a1d04ee53665e4da1d40c3fc16a880` | 0 |
| src/bundle/commitments.rs | 9504 | `70cfa70459973596c2fc4bb729c6ec15047dd341e0cb962b58f049adf03bf733` | 0 |
| src/circuit.rs | 82824 | `ce6506c490ce3ebea6ac833432052a8928051c5bea34bb5cdea22ce9ac49600c` | 0 |
| src/circuit/commit_ivk.rs | 36683 | `f6f69debeac9cee654c51c31851a05e2b1ef1466fd9b750d93df3ed8fd8dcaeb` | 0 |
| src/circuit/fingerprint/mod.rs | 9618 | `6e569b29e22118b994a56ce10d9f9db1018e9e69d799c3e4c5e743dffc9713d0` | 0 |
| src/circuit/fingerprint/random.rs | 11636 | `ffe8b2e8b33994d73e3df5641d095af98c842523e13c15caac455c899d7441b1` | 0 |
| src/circuit/fingerprint/rejected.rs | 10243 | `9a0057e6f6bf0a116dd59087a64dd49d774051fe9407f3f34a3c0c4f5f3e6823` | 0 |
| src/circuit/gadget.rs | 7774 | `46110394daa01a948e50e899840a44fd5095ce5daea259f1a6f280316763d820` | 0 |
| src/circuit/gadget/add_chip.rs | 2797 | `45fef9130ab5b56d1ec449ffcdf3f04c183db0754ac3f04e35fce27b8d9ac261` | 0 |
| src/circuit/note_commit.rs | 88878 | `f44b6fa63163cf0f297d2dafdcd029bb9a3dfb3587b675853cb3a1a00a101c10` | 0 |
| src/constants.rs | 2172 | `7e03a2704dd4eb59185e2c5e3de7454e693ae46024abbdd39e8817fd68095075` | 0 |
| src/constants/fixed_bases.rs | 22726 | `95089325c822c3fb4c8e063554db617c9b050b3f4e48844ad0dd5f5cb8f4b32e` | 0 |
| src/constants/fixed_bases/commit_ivk_r.rs | 133464 | `97432a3c56aa1070ed9880fc07dae954abe834258390b113cd11952bb26f6970` | 0 |
| src/constants/fixed_bases/note_commit_r.rs | 133413 | `dd1bf9303c3b1f885116da8b014f2d7d540312463b0eaa120ffb50d3d8c410a8` | 0 |
| src/constants/fixed_bases/nullifier_k.rs | 133377 | `123ac9ac6a602d4c8a97786df3a0213d4a5c1fb86fea4c24eaa83bab55fb3e07` | 0 |
| src/constants/fixed_bases/spend_auth_g.rs | 168322 | `e964a715b814c827f6088af3a14a71dc189a62c4a74e527750939e0d35268592` | 0 |
| src/constants/fixed_bases/value_commit_r.rs | 133576 | `8540a9f3bf0123761077a456e847e803e59e947e2f6c5274e6e3a6d26077cdce` | 0 |
| src/constants/fixed_bases/value_commit_v.rs | 36261 | `f0cc4fa936497d2235cb53d2f12b8a95012905b7f1b9ab676713c84bcdeafa81` | 0 |
| src/constants/load.rs | 7952 | `1c6b6167d4d7bdf5f7c99a67035f45004171e81901afcb1f977d25f3ac118da7` | 0 |
| src/constants/sinsemilla.rs | 8135 | `fc16c2e185abf2dd0be1f0d672d1548f4c8a341e4703528b2cde871085788b4f` | 0 |
| src/constants/util.rs | 701 | `259085a426c8e7cd21832b9f483ec5102f7479dcd86aa01ba99f4262af69d970` | 0 |
| src/keys.rs | 46924 | `ed5c26bc7907a928134f07612af322c2f55dd5da28b452660bff77f959c287ba` | 0 |
| src/lib.rs | 7014 | `a484249961efb89dff7c2febe014c6d2d9e37a584319ab44e8e93483108fca73` | 0 |
| src/note.rs | 19564 | `fdd312b64b14071c15b6a460776bc9a94d7d3cc245b3b379aff42c28830e22cc` | 0 |
| src/note/commitment.rs | 4334 | `23e5f36abb0d4724d12ab22b13f763e31f78210aa599bd84065a1a96fa4d51c2` | 0 |
| src/note/nullifier.rs | 4037 | `860747577a477fa387af512262c7f391593d74f4ac619a86b5c6c897bf18c659` | 0 |
| src/note_encryption.rs | 39339 | `0e1785ecb66dfbb343674afa8e8e037710f1b26d340804ce03aa502a33e464f3` | 0 |
| src/pczt.rs | 58304 | `ef0da92db2992fd1a3dcfcd43667d72e89bf1e883e5e363bf3146a1d9748ff80` | 0 |
| src/pczt/io_finalizer.rs | 4138 | `6c52857ee837bdd5621843f9a1fb2c035507aa62de1b2a1cfb4e41ddf57d6d07` | 0 |
| src/pczt/note_encryption.rs | 28289 | `65a9597778f49fa7065463439b38adc4b107fa0340a52e3e74d984fa65557aca` | 0 |
| src/pczt/parse.rs | 18573 | `2f6293a857bc374a04a09584a500d50fd2b1cf39cd4bea558ae5e95d59829e7d` | 0 |
| src/pczt/prover.rs | 10543 | `f919074defb82cde48d0b8d9a4c0ad0d98027bb066959f2c9c92de4640b577ae` | 0 |
| src/pczt/signer.rs | 3109 | `de136896bc37a126f6074a5978bf957342ad907aea638ec63c86bbc3c0c7a80e` | 0 |
| src/pczt/tx_extractor.rs | 8657 | `8aafd9b876be6fdd1f52cf5ee572ac9c84768ea0a909310012e6ac07b00f43c8` | 0 |
| src/pczt/updater.rs | 3478 | `74c485d6c926d3b10c33a3a6a57494d8b090bad49deaaf6e394a467ccd43a5b7` | 0 |
| src/pczt/verify.rs | 10857 | `5b89e8af64bd90ab0bb06daef0d51472181191fb5fa0616cfefc1320d6cdcc8a` | 0 |
| src/primitives.rs | 144 | `8fd884e8d918f42b2bcd56ced3860b86b126eb6779ab57dd77b73113ed56145e` | 0 |
| src/primitives/redpallas.rs | 8190 | `f9bde36b81685daaa0076e730d4b3e52bbb1a4958d8de9279124e9b1584b32fa` | 0 |
| src/spec.rs | 16291 | `5e2636a16681a34656f1740df28a94ef12bd2db092ca8d66b640e114e6385bb2` | 0 |
| src/tree.rs | 19280 | `7602ebde6aeadac78d401131900a3ef06469bc27a7e2d69f68173220cc89d39b` | 0 |
| src/value.rs | 17365 | `7ef315a72f6ff6fe0ff6c13bb71fed1fab59dde7658a7d9bd6917347808e90cb` | 0 |
| src/zip32.rs | 9624 | `c6ffb22e2903f629f6114d052829ed3203cdb84a6c2a930650c3a7bb7f3a48f4` | 0 |
