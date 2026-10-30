# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** halo2 @ 3442dd33754a · Electric Coin Company (Zcash) — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-29 23:45 UTC |
| Версия отчёта | 1 |
| Запуск аудита | d67212cf-da52-4f4f-9ed8-97b7d8bd0835 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `78926dc2f6ba69925f7b5b54cd0fde297409fa72872eddb930be8eaf5f1f29da` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **0**
- Средняя: **2**
- Низкая: **0**
- Информационная: **3**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 0
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 2
- Рекомендация по улучшению: 2
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/zcash/halo2> @ `3442dd33754ae0d44b8970e5a4eea79b0c3360bf` — ссылки в доказательствах открывают строки на этом коммите.

100 файлов, всего 1451944 байт, редактирований: 0; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| dependencies | проверено | 6 | Cargo.lock: 223 dependencies parsed (223 pinned); Cargo.toml: 25 dependencies parsed (0 pinned); halo2/Cargo.toml: 1 dependencies parsed (0 pinned) |
| source_code | проверено | 93 | halo2/src/lib.rs: 7 lines scanned with 16 rule patterns and 128 registry patterns; halo2_gadgets/src/ecc.rs: 1117 lines scanned with 16 rule patterns and 128 registry patterns; 474 lines in #[cfg(test)] modules ignored; halo2_gadgets/src/ecc/chip.rs: 719 lines scanned with 16 rule patterns and 128 registry patterns |
| osv_advisories | проверено | 1 | 223 pinned packages queried at OSV.dev; 3 affected (2 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree halo2 at 3442dd33754ae0d44b8970e5a4eea79b0c3360bf. 100 files analysed; of 235 files, 55 are test, fuzzing, benchmark or example code and were left out, 80 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .github/ISSUE_TEMPLATE/eli15.md, .github/actions/prepare/action.yml, .github/dependabot.yml, .github/workflows/bench.yml, .github/workflows/book.yml. 30 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **100** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 61.6%

## 7. Подробное описание находок

### QSI-2026-07294 — Квантово-уязвимый Halo 2 (IPA): роль не определена (34 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Halo 2 (IPA):general`
- Источник данных: halo2_gadgets/src/ecc.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:45 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

41 упоминаний Halo 2 (IPA) в 34 файл(ах), например halo2_gadgets/src/ecc.rs:5. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте halo2_gadgets/src/ecc.rs:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [halo2_gadgets/src/ecc.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/ecc.rs#L5) · line 5 · SHA-256 9e744d2ffbb0484896345bbcd45ec0752fe8a6897889f019f125dfdd1c1bc8d4_

```
    4 | 
    5 | use halo2_proofs::{
    6 |     arithmetic::CurveAffine,
```

_file_excerpt · [halo2_gadgets/src/ecc/chip.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/ecc/chip.rs#L12) · line 12 · SHA-256 ae82b6164e511c052b5f66681f77f732f4d79a6a62a7990fe1f8b2a57746dfc8_

```
   11 | use group::CurveAffine as _;
   12 | use halo2_proofs::{
   13 |     circuit::{AssignedCell, Chip, Layouter, Value},
```

_file_excerpt · [halo2_gadgets/src/ecc/chip/add.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/ecc/chip/add.rs#L4) · line 4 · SHA-256 ba8fe6bf018f9e7feb579efe8423698eba158ff884d9faf434822de4bc328c90_

```
    3 | use group::ff::PrimeField;
    4 | use halo2_proofs::{
    5 |     circuit::Region,
```

_file_excerpt · [halo2_gadgets/src/ecc/chip/add_incomplete.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/ecc/chip/add_incomplete.rs#L4) · line 4 · SHA-256 e0b2038aa27837669eb57d099d4381d764f3e354417ca59b395ca7b8020fefa1_

```
    3 | use super::NonIdentityEccPoint;
    4 | use halo2_proofs::{
    5 |     circuit::Region,
```

_file_excerpt · [halo2_gadgets/src/ecc/chip/constants.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/ecc/chip/constants.rs#L5) · line 5 · SHA-256 be4c7428a26ba3d085a1f0820c0fd1ea0cdacd7c2ccb2e543d1e4b0a87fcdd88_

```
    4 | use group::ff::{Field, PrimeField};
    5 | use halo2_proofs::arithmetic::lagrange_interpolate;
    6 | use pasta_curves::{
```

_file_excerpt · [halo2_gadgets/src/ecc/chip/layout_dump.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/ecc/chip/layout_dump.rs#L5) · line 5 · SHA-256 26379000da5a020d9e36dd44dc3f25f2e77afe45c558c5ce0ce14e727690a68d_

```
    4 | use crate::utilities::lookup_range_check::{LookupRangeCheck, PallasLookupRangeCheckConfig};
    5 | use halo2_proofs::{
    6 |     circuit::{Layouter, SimpleFloorPlanner, Value},
```

_file_excerpt · [halo2_gadgets/src/ecc/chip/layout_dump.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/ecc/chip/layout_dump.rs#L231) · line 231 · SHA-256 190334e42429d1f6b19211a6528e7cd0b73bafac8fa3ae184eab0f0d03c97009_

```
  230 | 
  231 | const MUL_LAYOUT_HEADER: &str = "-- Auto-generated by halo2 `dump_lean` (Halo2-Clean VK-matching, Phase 2 layout). Do not edit by hand.
  232 | -- Phase 2 layout of the isolated mul chain (`configure_mul` / `MulDumpCircuit`,
```

_file_excerpt · [halo2_gadgets/src/ecc/chip/layout_dump.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/ecc/chip/layout_dump.rs#L268) · line 268 · SHA-256 01cee9ca5f2a30bac8a9913250ac1f295b7ee0c13cba13f7af224ed6bef62fc6_

```
  267 | const MUL_SELMAP_HEADER: &str =
  268 |     "-- Auto-generated by halo2 `dump_lean` (Halo2-Clean VK-matching). Do not edit by hand.
  269 | -- Selector-compression map (see `compress_selectors.rs`): per selector, the packed
```

_file_excerpt · [halo2_gadgets/src/ecc/chip/mul.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/ecc/chip/mul.rs#L12) · line 12 · SHA-256 7acb57b0c0ef4067d0352685d00d393e28cf04d42062857429e73befaa763f51_

```
   11 | use ff::{Field, PrimeField};
   12 | use halo2_proofs::{
   13 |     circuit::{AssignedCell, Layouter, Region, Value},
```

_file_excerpt · [halo2_gadgets/src/ecc/chip/mul/complete.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/ecc/chip/mul/complete.rs#L5) · line 5 · SHA-256 a7d7ad8a617509d058101e1f6e166614219a8f55d79c054028c433fece5f4596_

```
    4 | 
    5 | use halo2_proofs::{
    6 |     circuit::{Region, Value},
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07295 — Квантово-уязвимый Sinsemilla: роль не определена (9 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Sinsemilla:general`
- Источник данных: halo2_gadgets/src/ecc/chip/mul/overflow.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:45 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

173 упоминаний Sinsemilla в 9 файл(ах), например halo2_gadgets/src/ecc/chip/mul/overflow.rs:3. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте halo2_gadgets/src/ecc/chip/mul/overflow.rs:3 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [halo2_gadgets/src/ecc/chip/mul/overflow.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/ecc/chip/mul/overflow.rs#L3) · line 3 · SHA-256 61473701044b00a24e8b2948c40c32dbc3e16a230dab868526877e8a5a09db8b_

```
    2 | use crate::{
    3 |     sinsemilla::primitives as sinsemilla,
    4 |     utilities::lookup_range_check::{PallasLookupRangeCheck, PallasLookupRangeCheckConfig},
```

_file_excerpt · [halo2_gadgets/src/ecc/chip/mul/overflow.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/ecc/chip/mul/overflow.rs#L196) · line 196 · SHA-256 d2f4cb9aa13b9f5ccf2304d9a9ee85fd54de84c51ab8c4564a2a0908e5b25cba_

```
  195 |         // Number of k-bit words we can use in the lookup decomposition.
  196 |         let num_words = 130 / sinsemilla::K;
  197 |         assert!(num_words * sinsemilla::K == 130);
```

_file_excerpt · [halo2_gadgets/src/ecc/chip/mul/overflow.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/ecc/chip/mul/overflow.rs#L197) · line 197 · SHA-256 5bbefdc3ba4e31fe189d9510accebddf6ee3906a4ee0647237cd0fe017f4c732_

```
  196 |         let num_words = 130 / sinsemilla::K;
  197 |         assert!(num_words * sinsemilla::K == 130);
  198 | 
```

_file_excerpt · [halo2_gadgets/src/lib.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/lib.rs#L26) · line 26 · SHA-256 7f45c76f548f226657d7df19a6981a3f52ab4069301de34bed3372100aa241ea_

```
   25 | pub mod poseidon;
   26 | pub mod sinsemilla;
   27 | pub mod utilities;
```

_file_excerpt · [halo2_gadgets/src/sinsemilla.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/sinsemilla.rs#L20) · line 20 · SHA-256 8e138d1047bdd1d0ed85ffbdc93ada1a7eb922d7d4f9b76ae4173aa08ffca322_

```
   19 | 
   20 | pub use ::sinsemilla as primitives;
   21 | 
```

_file_excerpt · [halo2_gadgets/src/sinsemilla.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/sinsemilla.rs#L26) · line 26 · SHA-256 99a1d2d2b6a53adc468da6ef45edfd75eecc776d41d76bd2d2706e2d4bf414f9_

```
   25 | /// number of words that a single hash instance can process.
   26 | pub trait SinsemillaInstructions<C: CurveAffine, const K: usize, const MAX_WORDS: usize> {
   27 |     /// A variable in the circuit.
```

_file_excerpt · [halo2_gadgets/src/sinsemilla.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/sinsemilla.rs#L121) · line 121 · SHA-256 43755b6d17985b02c033966cd61a74f023cb2aa64a145e7ee02fd3e05ad14292_

```
  120 | #[derive(Clone, Debug)]
  121 | pub struct Message<C: CurveAffine, SinsemillaChip, const K: usize, const MAX_WORDS: usize>
  122 | where
```

_file_excerpt · [halo2_gadgets/src/sinsemilla/chip.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/sinsemilla/chip.rs#L5) · line 5 · SHA-256 b419059e91e6474372f4fc3227c6aff5fa80a6beab13b809d08628d36fa6314c_

```
    4 |     message::{Message, MessagePiece},
    5 |     primitives as sinsemilla, CommitDomains, HashDomains, SinsemillaInstructions,
    6 | };
```

_file_excerpt · [halo2_gadgets/src/sinsemilla/chip.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/sinsemilla/chip.rs#L39) · line 39 · SHA-256 76d32e781d39f14fedf833bd8677408480635d843cf59b53de8720cd674c0759_

```
   38 | #[derive(Eq, PartialEq, Clone, Debug)]
   39 | pub struct SinsemillaConfig<Hash, Commit, F, Lookup = PallasLookupRangeCheckConfig>
   40 | where
```

_file_excerpt · [halo2_gadgets/src/sinsemilla/chip.rs](https://github.com/zcash/halo2/blob/3442dd33754ae0d44b8970e5a4eea79b0c3360bf/halo2_gadgets/src/sinsemilla/chip.rs#L76) · line 76 · SHA-256 b1107413b5bff30832ec37e0b00500bae36ef605c95fbbb9a3759062dd2fe6ab_

```
   75 | 
   76 | impl<Hash, Commit, F, Lookup> SinsemillaConfig<Hash, Commit, F, Lookup>
   77 | where
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07298 — 3 бюллетеней в 2 пакет(ах) crates.io, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:crates.io:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:45 UTC
- Балл приоритета: 15.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 3 бюллетеней (2 с оценкой high или critical) для 2 пакет(ов) crates.io, которые подтягивают только инструменты разработки или сборки (Cargo.lock): например, gumdrop@0.8.1 [dev]: RUSTSEC-2026-0214; quick-xml@0.26.0 [dev]: RUSTSEC-2026-0194, RUSTSEC-2026-0195. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в Cargo.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (crates.io)](https://osv.dev/) · Cargo.lock · SHA-256 616397a43959bf6a4ed1107e089d8fabf0b48f7c38a24a6c6d33520152314344_

```
gumdrop@0.8.1 [dev]: RUSTSEC-2026-0214
quick-xml@0.26.0 [dev]: RUSTSEC-2026-0194, RUSTSEC-2026-0195
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07296 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:45 UTC
- Балл приоритета: 13.3 / 100
- CVSS v3.1: неприменимо

В 6 манифестах зависимостей QSI нашёл криптобиблиотеки (ff, group, halo2_gadgets, halo2_poseidon, halo2_proofs, pasta_curves, sinsemilla), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · Cargo.lock, Cargo.toml, halo2/Cargo.toml, halo2_gadgets/Cargo.toml, halo2_poseidon/Cargo.toml, halo2_proofs/Cargo.toml · SHA-256 e3f047d63f0a64fea96d533760fe7bdaa0eb56367b01de8a327ec457c0414f85_

```
Crypto libraries: ff, group, halo2_gadgets, halo2_poseidon, halo2_proofs, pasta_curves, sinsemilla
```

**Ограничения проверки.** Отсутствие доказательств не является доказательством отсутствия: системные библиотеки и транзитивные зависимости могут не указываться.

**Рекомендация.** Определите источник поддержки PQC (TLS-терминатор, KMS/HSM, обновление библиотек).

**Повторная проверка.** Повторите сканирование после обновлений.

### QSI-2026-07297 — ttf-parser 0.20.0: информационный бюллетень RUSTSEC-2026-0192 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/ttf-parser@0.20.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:45 UTC
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
| **роль не определена** | Halo 2 (IPA) (34), Sinsemilla (9) | QSI-2026-07294, QSI-2026-07295 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм в конечных полях | взламывает | Q1 | PLONK (KZG) (1) | Взламывает Диффи–Хеллмана в конечных полях и DSA при любом размере. Переводите установление ключей на ML-KEM (на переходный период — гибрид с X25519 или ECDH), подписи — на ML-DSA или SLH-DSA. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | ECDSA (1), Halo 2 (IPA) (34), PLONK (KZG) (1), Sinsemilla (9) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Poseidon (4) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Poseidon (4) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-07294 | Внесите использования Halo 2 (IPA) в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07295 | Внесите использования Sinsemilla в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-07294 | Запланируйте миграцию Halo 2 (IPA) на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07295 | Запланируйте миграцию Sinsemilla на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07298 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |
| P4 | QSI-2026-07297 | Замените ttf-parser поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | ttf-parser заменён или решение зафиксировано. |

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
21. OSV advisory RUSTSEC-2026-0192 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0192> (modified 2026-06-29T21:15:04.384453633Z)
22. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
23. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
24. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
25. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| Poseidon |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 4 | 4 | halo2_gadgets/src/lib.rs:25; halo2_gadgets/src/poseidon.rs:28; halo2_gadgets/src/poseidon/pow5.rs:15 |
| Crypto library | 0.14.0 | group (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | ff (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.2.0 | sinsemilla (sinsemilla) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.6.0 | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14 | ff (jubjub) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.14 | group (jubjub) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.2 | sinsemilla (sinsemilla) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.2 | halo2_poseidon (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.4 | halo2_proofs (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.6 | halo2_gadgets (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.6 | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | workspace | halo2_proofs (halo2 (Zcash)) | н/п | допустимо | 2 | 2 | halo2/Cargo.toml; halo2_gadgets/Cargo.toml |
| Crypto library | workspace | ff (jubjub) | н/п | допустимо | 3 | 3 | halo2_gadgets/Cargo.toml; halo2_poseidon/Cargo.toml; halo2_proofs/Cargo.toml |
| Crypto library | workspace | group (jubjub) | н/п | допустимо | 3 | 3 | halo2_gadgets/Cargo.toml; halo2_poseidon/Cargo.toml; halo2_proofs/Cargo.toml |
| Crypto library | workspace | sinsemilla (sinsemilla) | н/п | допустимо | 1 | 1 | halo2_gadgets/Cargo.toml |
| Crypto library | workspace | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 3 | 3 | halo2_gadgets/Cargo.toml; halo2_poseidon/Cargo.toml; halo2_proofs/Cargo.toml |
| Crypto library | workspace | halo2_poseidon (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | halo2_gadgets/Cargo.toml |
| ECDSA |  |  | уязвим (Шор) | допустимо | 1 | 1 | halo2_gadgets/src/ecc.rs |
| Halo 2 (IPA) |  |  | уязвим (Шор) | допустимо | 34 | 34 | halo2_gadgets/src/ecc.rs:5; halo2_gadgets/src/ecc/chip.rs:12; halo2_gadgets/src/ecc/chip/add.rs:4 |
| PLONK (KZG) |  |  | уязвим (Шор) | допустимо | 1 | 1 | halo2_proofs/src/plonk.rs |
| Sinsemilla |  |  | уязвим (Шор) | допустимо | 9 | 9 | halo2_gadgets/src/ecc/chip/mul/overflow.rs:3; halo2_gadgets/src/lib.rs:26; halo2_gadgets/src/sinsemilla.rs:20 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| Cargo.lock | 52901 | `0d4591933364c0c38945a6a639e84f2697fd4d6ecb448516fae5f81147bb923f` | 0 |
| Cargo.toml | 1373 | `4b5a832a64a61d476f8308e2d4fd102c05ebeabaf11e043384001de989125ee9` | 0 |
| halo2/Cargo.toml | 653 | `3f91a00fb9ea69b3c120f1b15893b19aa729627c89adbb1c4c9326e16dc87294` | 0 |
| halo2/src/lib.rs | 179 | `9e5d7cabd77e1c97f5e4368d38e787895144b63acabff3aa766c4079beabcf99` | 0 |
| halo2_gadgets/Cargo.toml | 2095 | `b9faefa2af2f8aa2d3ca10c7ed3132a2f9fd4d941cbbb11409a759c811a5a7f2` | 0 |
| halo2_gadgets/src/ecc.rs | 38996 | `59b832b8e6dd618a572fb726f6f45b3aea939baf7b5c9398ae9cd1d4a2c6f510` | 0 |
| halo2_gadgets/src/ecc/chip.rs | 25666 | `9d001517c6028308060d635f6c10772308c2af7c2c430f6666290f4d4fc20a09` | 0 |
| halo2_gadgets/src/ecc/chip/add.rs | 16086 | `a81bad0a96c5991a25f4f3d5ea24a41823cd2e1fdbd423d4ec4db16e1f421c75` | 0 |
| halo2_gadgets/src/ecc/chip/add_incomplete.rs | 6540 | `1e0083b20f89a8469c42ad18d7d6915012c2132b3a86b1ab772f714b5ae98bad` | 0 |
| halo2_gadgets/src/ecc/chip/constants.rs | 11090 | `4598ca03006b5c001af74425ca19f96e439a20ca7e9a573a1697656b96aa20a9` | 0 |
| halo2_gadgets/src/ecc/chip/layout_dump.rs | 13318 | `0ddff158e1d972a0ab1c268b84d13b8658c886b170cac56ef867b68d0cee1682` | 0 |
| halo2_gadgets/src/ecc/chip/mul.rs | 33200 | `5bd412ea5e8c90006ffd3e653d92918a4a33ce58c120e7b5acec3848864b66f0` | 0 |
| halo2_gadgets/src/ecc/chip/mul/complete.rs | 7295 | `514390b1e77f4e81d2745418ba7209b80958ad3fe4dbc8dc0f894a8e7c8abcc3` | 0 |
| halo2_gadgets/src/ecc/chip/mul/incomplete.rs | 15923 | `4bfadb52be382f57421201840cf295938055c482bf66e11536c0df167d0dd0f6` | 0 |
| halo2_gadgets/src/ecc/chip/mul/overflow.rs | 7696 | `20acfebd3f3ed5dd71fa04c0115d3ccb77dcf919968c8809d03a6df979c0e77a` | 0 |
| halo2_gadgets/src/ecc/chip/mul_fixed.rs | 18388 | `7a2ce8d4f8b4efca580dbbaa76c0f2e583f84296d589d08078db02649d01a85b` | 0 |
| halo2_gadgets/src/ecc/chip/mul_fixed/base_field_elem.rs | 20665 | `5d48742efdf2c656031929e640f0c64a8747dea9697428cdcdeb3bc219220d07` | 0 |
| halo2_gadgets/src/ecc/chip/mul_fixed/full_width.rs | 11233 | `8f7b5c58b38a7f68b873c0a06e53dca6f5cba4452a865c3ff009daaa8abb5d0b` | 0 |
| halo2_gadgets/src/ecc/chip/mul_fixed/short.rs | 37451 | `a656d7e876d829fa4c2629c7ec7b25f9f5106ba68e4935daab21a1ec1e172538` | 0 |
| halo2_gadgets/src/ecc/chip/witness_point.rs | 9346 | `6a25767a86718b17faa506446666cd25aa6f919f2af336f81ec9c6c746e84136` | 0 |
| halo2_gadgets/src/lib.rs | 1068 | `4434c72bd5a92f8cba995ec280ae3b20a25308accbf6058e411fa84988b49dac` | 0 |
| halo2_gadgets/src/poseidon.rs | 8406 | `a88f1571da14aa48bd95f65e3ced755c22e41fd7c803961af0d7748af2f6a2d6` | 0 |
| halo2_gadgets/src/poseidon/pow5.rs | 32386 | `6c2af6c6ce64a2b20fec991febeaf73c5d8c03d8758a0a3aed1f9983f56d485e` | 0 |
| halo2_gadgets/src/sinsemilla.rs | 34183 | `99d33149e2725ac6d4458f8fb123537347bb0e1627fafd2d8a480e1b1a697f3e` | 0 |
| halo2_gadgets/src/sinsemilla/chip.rs | 13786 | `ffb7017d18da2ec4568114fab60eb82ac18544e5ebdc17cdbceaca3928a53b82` | 0 |
| halo2_gadgets/src/sinsemilla/chip/generator_table.rs | 3739 | `e5dea0027acc6c137914ad8264eec0013cb9b14e276ccfa235ea5d9f5bbade60` | 0 |
| halo2_gadgets/src/sinsemilla/chip/hash_to_point.rs | 20495 | `563d89356cfaeebc511463aa39e41af4dfab33d7bf5635e7daf863fb601297d1` | 0 |
| halo2_gadgets/src/sinsemilla/merkle.rs | 22965 | `374bc76a06ebba158b966e6f565c40198870d86f0de0370dfcd6cad1d5abb321` | 0 |
| halo2_gadgets/src/sinsemilla/merkle/chip.rs | 22905 | `637f0ceda4dee675a31bfe173c1a7ebf032e99a9d173894e05928ac5933748de` | 0 |
| halo2_gadgets/src/sinsemilla/message.rs | 1899 | `d6753477bd6acb43d25a666236023cc99daea2d7045dab4a4a616a9dbe3a37fd` | 0 |
| halo2_gadgets/src/utilities.rs | 16175 | `c3d825adfd762fbf8dd66822c62aed4483136a15207b1463ae2e8eafc8432a8b` | 0 |
| halo2_gadgets/src/utilities/cond_swap.rs | 23059 | `2c120756704aa47e35f6a3fb895849ab3db5e830a3035ae18b575f73194450d8` | 0 |
| halo2_gadgets/src/utilities/decompose_running_sum.rs | 14830 | `23e41f239fb643ba3d487a5e8b99bce21b61632b576cdd105e7a0511814c9e97` | 0 |
| halo2_gadgets/src/utilities/lookup_range_check.rs | 46351 | `7128b99d319e3d9d4dd21f1b65b6b911e0812de45d67bb58a74b9845c65e27cb` | 0 |
| halo2_poseidon/Cargo.toml | 540 | `38f284c9eac342191e7649fbed8ac5272b272d9f15f193d1ad112deef20b1ab0` | 0 |
| halo2_poseidon/src/fp.rs | 40637 | `b19d4e50867e67af232db34f88d2bf8629d6d7ee2496458a8e37ae758772acd5` | 0 |
| halo2_poseidon/src/fq.rs | 40404 | `ae1743650291a44631323c565f71b7de8e0bca98ab4ee363f10b173ebdc575c5` | 0 |
| halo2_poseidon/src/grain.rs | 6178 | `788a280714b291ea41c991ad9ba21d8c9e6ad02d5ec52fd6ebd7fe14b478eaff` | 0 |
| halo2_poseidon/src/lib.rs | 15643 | `8a6d626c5024157fc09e4e1daf811ee4d1e81acfa1ca6592e663934c13dd2d56` | 0 |
| halo2_poseidon/src/mds.rs | 4707 | `10cb39b77faf243f1e57e9813e9ee435677f1860b1b6190e6813019450da0599` | 0 |
| halo2_poseidon/src/p128pow5t3.rs | 9958 | `5b46bc7ef7ee2480b85c7aeb96052301abb7dbff16f8d9d87c0c0abac3b6fc9c` | 0 |
| halo2_proofs/Cargo.toml | 2694 | `02b6eb98c619e24c023a2357d37768be75aac58f09fc18ce7666d1fddd7bdffb` | 0 |
| halo2_proofs/src/arithmetic.rs | 22070 | `c344c3e01cdf17d144781dd1e8807cecef70b8460a408979222e28e533c59350` | 0 |
| halo2_proofs/src/circuit.rs | 18063 | `d031fc3532cbe7225400855aee3cd5296f6dc4490e64ac7ecb442877d9e61abb` | 0 |
| halo2_proofs/src/circuit/floor_planner.rs | 118 | `73c23da5835a26594486155a010b48bbef7e81cf7aab3ff443e790763bcdf158` | 0 |
| halo2_proofs/src/circuit/floor_planner/single_pass.rs | 13243 | `f6f983929bbb2c37b70afddb5a1ed61ec387b9411aa297cc9ef1d565e0c9fb4e` | 0 |
| halo2_proofs/src/circuit/floor_planner/v1.rs | 16036 | `1801cbb554cc55265dea4b2865eb59c483ad64489349b03eb5823f7590c41e18` | 0 |
| halo2_proofs/src/circuit/floor_planner/v1/strategy.rs | 9479 | `aa08a851f21b8d37b7d1bc89f0cfa1ba56f9db6cff07cf1de236d9c88cc05649` | 0 |
| halo2_proofs/src/circuit/layouter.rs | 9182 | `be0d46973890b5557543da47ee781b384221fd5b9489d70809682a5a173f5dcc` | 0 |
| halo2_proofs/src/circuit/table_layouter.rs | 13110 | `979e0133df95b7795d9f39cd7c0b5282f4c48242a1b98f49ece9814bb17c1cff` | 0 |
| halo2_proofs/src/circuit/value.rs | 17275 | `71efd7c047c78295b977cf9907bf192f4a00fc87273a398de71313b600a2637b` | 0 |
| halo2_proofs/src/dev.rs | 41923 | `da9ea8c560dfed04d4d183a1108c95f5b6551a1c328c0e9608aebbc3a5382b69` | 0 |
| halo2_proofs/src/dev/circuit_fixture.rs | 20699 | `ac892c9d0c640b41c004de21ded7d406c2f08fbe14984e1fd649c3af25a417bc` | 0 |
| halo2_proofs/src/dev/cost.rs | 17485 | `db4c0bec1fea2c835d6f54bb68c4e6a5c271045330767df742597c666aeba45f` | 0 |
| halo2_proofs/src/dev/failure.rs | 19868 | `1c1aaafdec7e42c701f6d5cddfa0d1e2d748b61b130d9b283cf8b542fa3269fa` | 0 |
| halo2_proofs/src/dev/failure/emitter.rs | 5029 | `b4d30d490c6dcdf1c66b82935e9a3674aa22a7a69008067e32e053739767d8a8` | 0 |
| halo2_proofs/src/dev/gates.rs | 9709 | `e08ad44741c8df6589144fd3ab0e13bcd54c92f786de5fd4827cdde9b0dbfeb4` | 0 |
| halo2_proofs/src/dev/graph.rs | 5268 | `1f5db2a77692fdd0a0f37dba163a39665126c27b22b21446c7acc92ec87404b9` | 0 |
| halo2_proofs/src/dev/graph/layout.rs | 11850 | `f3d21cac94ad74855f8cd9f1eecdb9016053891586f848fc92c56f4a2d5c8316` | 0 |
| halo2_proofs/src/dev/metadata.rs | 5079 | `def5eafe66b5055af7e2a19da6df4393851da0892bd9b8b813191499f12beb7e` | 0 |
| halo2_proofs/src/dev/tfp.rs | 14735 | `fc0c31b71e8d38d910be878b93ae14e28028637a9cb1410e66fdaa75d6f0612d` | 0 |
| halo2_proofs/src/dev/util.rs | 4517 | `61a315c9ef7c8c6d7d8ef70fc676664abc95d14e2b0dd1ad1ec98112de6feaf7` | 0 |
| halo2_proofs/src/helpers.rs | 549 | `1b1424c2a8f8f3ade35b68849bc84bb12aaed08cf06e9d065f192f32895c1367` | 0 |
| halo2_proofs/src/lib.rs | 444 | `87ecbfa3de85666ce660fdc8bf896196b9f93585384fd6170868e84c8cf3686e` | 0 |
| halo2_proofs/src/multicore.rs | 3700 | `ec65ea5a455d2c4ef12097391850af1a98f44464652d55c24bc58d8e3214e1e8` | 0 |
| halo2_proofs/src/plonk.rs | 5277 | `12b80139f13e6d51eb5913855ec6e7de89534e43ea41f989b50ddfe02f1a9a95` | 0 |
| halo2_proofs/src/plonk/assigned.rs | 20524 | `a7452e96d75956e1f47ee93373804f899eb1f69bbf970cf944148d55e2556e25` | 0 |
| halo2_proofs/src/plonk/circuit.rs | 52203 | `c6efa09bdbe9081861fe2bd469b8b9b547beeee1e95c4d66e6896050d5e45db0` | 0 |
| halo2_proofs/src/plonk/circuit/compress_selectors.rs | 13724 | `95e78cb9dea30e887727a09dcf29c39fa2c9e5c6392f7c45a661ca6a9338d086` | 0 |
| halo2_proofs/src/plonk/circuit/fixture.rs | 13111 | `b3df664c714babbad68664e5f0a14a1ca791ad3fdb7e6381c62ad719e5926799` | 0 |
| halo2_proofs/src/plonk/error.rs | 5214 | `088fddace0899454b6aea2ec83c5bf123e4759aa8bc0a121f10295bb7a81d0b4` | 0 |
| halo2_proofs/src/plonk/fingerprint/mod.rs | 2380 | `9c0c55aa94658ae00aa2aa6cd19219f547e9c34845469129257293713482b1bf` | 0 |
| halo2_proofs/src/plonk/fingerprint/transcript.rs | 3757 | `95d66fa2ee46eeb49551cd760c26e18008adc1bb6e620181efe63029c391bcaa` | 0 |
| halo2_proofs/src/plonk/fingerprint/vesta_lean.rs | 74191 | `76d2861eef11278e774628949c3fdf34978bbd2a1f4eb3c49152d83524fafa2e` | 0 |
| halo2_proofs/src/plonk/keygen.rs | 9607 | `655240dcff4491d7adc10840831b2a57af0e1a3b64599f90f92dadc00ef8389f` | 0 |
| halo2_proofs/src/plonk/lookup.rs | 2874 | `d6923b5f9f82f52a646fae18e4b512c4c6ff086c09641537434177eb2e974356` | 0 |
| halo2_proofs/src/plonk/lookup/prover.rs | 27778 | `590093529a746a23750375ca5ebc3ae379d434c47cdd03ca2d3e29f8f780e90f` | 0 |
| halo2_proofs/src/plonk/lookup/verifier.rs | 7421 | `b2c7f87f441a756cac394d0fc342bdeea5d6c06eea21526eaae5194207d2b6b6` | 0 |
| halo2_proofs/src/plonk/permutation.rs | 2874 | `8c12169e2fac91f4f2dd4a0a4576357b9a54dda21cd8e400ad088b0e24500410` | 0 |
| halo2_proofs/src/plonk/permutation/keygen.rs | 7093 | `d8edd2203cc933a6979d58ce221cccf210f0f65ce2b2b577e3efc764fe208ce3` | 0 |
| halo2_proofs/src/plonk/permutation/prover.rs | 17191 | `005dd6ee995f825b0535168d366a193952190df35deef3dd332ec563018d0615` | 0 |
| halo2_proofs/src/plonk/permutation/verifier.rs | 9027 | `09bc9b6ac9200d1c4e3015b3ed642737375f81ddda2f38ecebec98d5a528e179` | 0 |
| halo2_proofs/src/plonk/prover.rs | 27928 | `ac2307d197dd1dab34c9b07e7311f0ce02b42f068b017ee6ebaaa27a1916b512` | 0 |
| halo2_proofs/src/plonk/vanishing.rs | 197 | `b664ff3220d71fb1d89d809d628e1969ff5bdd38edbba863733960a1213407bc` | 0 |
| halo2_proofs/src/plonk/vanishing/prover.rs | 5370 | `c04196e395de38a0329ca42e35858939e65f1f38ddd795cb8f649fb46ba1cd9c` | 0 |
| halo2_proofs/src/plonk/vanishing/verifier.rs | 3870 | `20e0b7596ef47067849ab714e277065d87e2a7f87aaccbedddcfb00c030f2e5f` | 0 |
| halo2_proofs/src/plonk/verifier.rs | 17848 | `8a3452866320e535570d78db098147838d015f985af214e6f3d60195606e2ef2` | 0 |
| halo2_proofs/src/plonk/verifier/batch.rs | 4170 | `dd91b8e915794516665df699a3e8b63c81b8618d98d510ffb06d2c0b7bdd0f12` | 0 |
| halo2_proofs/src/poly.rs | 10683 | `0bc0a71b19ca7dbc408a41a455d4787e3986629d1742737282cea6816d8b9998` | 0 |
| halo2_proofs/src/poly/commitment.rs | 11738 | `9e1ebff98d5e531d03485afe1d8c52bf6c291c462f6efb751f2085daa6535653` | 0 |
| halo2_proofs/src/poly/commitment/msm.rs | 9099 | `3a5b7850f8c588d4eb3d7aa4d2941c5b5ea756dbcf99adfda6aa58e94d7cbd47` | 0 |
| halo2_proofs/src/poly/commitment/prover.rs | 6314 | `4ff3438614a1766e34f21babc7d886664db736f734f524b1c5cc96062ba03e5e` | 0 |
| halo2_proofs/src/poly/commitment/verifier.rs | 5297 | `d9b79f66cdb6ee8b1e52adbc5bdcf98d133ee44e0c76e94b0728204e6de4476f` | 0 |
| halo2_proofs/src/poly/domain.rs | 20912 | `379599939d3db1cc10ce2d4cd7cfdf3b41858421d6cc2a734b4b54989b4d105c` | 0 |
| halo2_proofs/src/poly/evaluator.rs | 21957 | `e8799c2a0cb184008f1401df7be55d23c96092aebad996e543518f81f875b53e` | 0 |
| halo2_proofs/src/poly/multiopen.rs | 19064 | `2979e465953235e186c3a69105205248dd7907a31fd5174178f986fa5b5c9861` | 0 |
| halo2_proofs/src/poly/multiopen/prover.rs | 4907 | `383fd403995decdb7843481734fb84f2056dddf098b01b69865ce5e997471128` | 0 |
| halo2_proofs/src/poly/multiopen/verifier.rs | 5413 | `72cace4d1abfa1e1800c3bad8215f0b7b51ee49005fbf427c5be807b22a7c435` | 0 |
| halo2_proofs/src/transcript.rs | 10332 | `f5dbd474c532e9355271116ab4d3d7211e93ff2f661d27bdd4a56f026412a3ad` | 0 |
| rust-toolchain.toml | 66 | `fc9d487b329e61afae23a5a03c5b0097290d9c15b980233e1168e7f09cacfcd9` | 0 |
