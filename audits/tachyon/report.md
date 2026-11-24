# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** tachyon @ 6cdaebccf147 · Tachyon (Zcash) — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-11-24 11:26 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 1def9d6b-b8d8-4d5e-b916-b10c6dd0a7ca (Документальный аудит) |
| Версия анализатора | qsi-engine 1.20.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `d2582758173de8cfbdbd330e9c2fa474974d00acd862a78e5003fd9874e6dd55` |
| Ключ подписи (отпечаток SHA-256 ключа Ed25519, затем ML-DSA-65, если он подписывает вместе с ним; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **0**
- Средняя: **3**
- Низкая: **10**
- Информационная: **1**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 10
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 3
- Рекомендация по улучшению: 1
- Недостаточность данных: 0

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/tachyon-zcash/tachyon> @ `6cdaebccf147c5a013d212f9d7302924a9570626` — ссылки в доказательствах открывают строки на этом коммите.

57 файлов, всего 463845 байт, редактирований: 0; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| dependencies | проверено | 3 | Cargo.lock: 98 dependencies parsed (98 pinned); Cargo.toml: 0 dependencies parsed (0 pinned); crates/tachyon/Cargo.toml: 16 dependencies parsed (0 pinned) |
| source_code | проверено | 52 | book/mermaid-init.js: 39 lines scanned with 17 rule patterns and 340 registry patterns; crates/tachyon/src/action.rs: 324 lines scanned with 17 rule patterns and 340 registry patterns; crates/tachyon/src/bundle/mod.rs: 1237 lines scanned with 17 rule patterns and 340 registry patterns |
| entropy | проверено | 1 | random-number generation: 52 code files read with 0 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| key_storage | проверено | 1 | key settings with a fallback in the code: 0; decryption fallbacks: 0; derived nonces: 0; key columns: 0 (no KMS, HSM or vault service found); author warnings: 0 |
| osv_advisories | не проверено | 1 | 7 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: ragu, ragu_arithmetic, ragu_circuits, ragu_core, ragu_macros, ragu_pasta, ragu_primitives |
| osv_advisories | проверено | 1 | 91 pinned packages queried at OSV.dev; 3 affected |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- osv_advisories — не проверено: 7 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: ragu, ragu_arithmetic, ragu_circuits, ragu_core, ragu_macros, ragu_pasta, ragu_primitives

## 5. Краткое описание архитектуры

Static review of the source tree tachyon at 6cdaebccf147c5a013d212f9d7302924a9570626. 57 files analysed; of 138 files, 9 are test, fuzzing, benchmark or example code and were left out, 71 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .github/actions/rust-nightly-setup/action.yml, .github/actions/rust-setup/action.yml, .github/workflows/book.yml, .github/workflows/rust.yml, .github/workflows/zizmor.yml. 33 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **91** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 40.0%

## 7. Подробное описание находок

### QSI-2026-49589 — Квантово-уязвимый Pedersen commitment: пороговая подпись и протоколы MPC (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Pedersen commitment:threshold_mpc`
- Источник данных: crates/tachyon/src/value.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

3 упоминаний Pedersen commitment в 1 файл(ах), например crates/tachyon/src/value.rs:18. Роль по путям, именам функций и соседнему коду: пороговая подпись и протоколы MPC. Paillier, обязательства Педерсена и доказательства на дискретном логарифме внутри пороговых ECDSA и EdDSA ломаются алгоритмом Шора; постквантовая пороговая схема — это смена протокола, а не параметра.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте crates/tachyon/src/value.rs:18 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [crates/tachyon/src/value.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/value.rs#L18) · line 18 · SHA-256 9ff0ec5ef69430ebe9a6c4b3b79ee6e5250d9fcac040615717f1d682c5490930_

```
   17 | /// Alias for [`ValueCommitment`].
   18 | pub type Commitment = ValueCommitment;
   19 | 
```

_file_excerpt · [crates/tachyon/src/value.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/value.rs#L79) · line 79 · SHA-256 f1812189e951dd7c0b54be48946948862b7c298c797f8073ddeb42dec03b9189_

```
   78 |         let commit_trapdoor = *VALUE_COMMIT_R * self.0;
   79 |         ValueCommitment(commit_value + commit_trapdoor)
   80 |     }
```

_file_excerpt · [crates/tachyon/src/value.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/value.rs#L93) · line 93 · SHA-256 599fff9d6a98290efca0ab16885161a6bc8f04a94d51fc6cd9fb2dbcac1895b5_

```
   92 | #[expect(clippy::module_name_repetitions, reason = "deliberate name")]
   93 | pub struct ValueCommitment(#[debug(skip)] Ep);
   94 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-49587 — Квантово-уязвимый RedDSA: роль не определена (6 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:RedDSA:general`
- Источник данных: crates/tachyon/src/action.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

24 упоминаний RedDSA в 6 файл(ах), например crates/tachyon/src/action.rs:267. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте crates/tachyon/src/action.rs:267 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [crates/tachyon/src/action.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/action.rs#L267) · line 267 · SHA-256 665b8939749dc8191eb086848a64e3e5f20038a1d4ed0cd282fafe9b5d480ec5_

```
  266 | #[display("Signature({:?})", self.0)]
  267 | pub struct Signature(pub(crate) reddsa::Signature<reddsa::ActionAuth>);
  268 | 
```

_file_excerpt · [crates/tachyon/src/bundle/mod.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/bundle/mod.rs#L1215) · line 1215 · SHA-256 60e1af3bbf6b5ab3ceb775dc6a92938642e8b6b2d4daf43fbd19721ec7d0aca7_

```
 1214 | #[derive(Clone, Copy, Debug, PartialEq, TotalEq)]
 1215 | pub struct Signature(pub(crate) reddsa::Signature<reddsa::BindingAuth>);
 1216 | 
```

_file_excerpt · [crates/tachyon/src/keys/proof.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/keys/proof.rs#L60) · line 60 · SHA-256 42275e11e48ddc762025e9716308a53fc22c29e8c9e19365cd392e20089b0a34_

```
   59 | pub struct SpendValidatingKey(
   60 |     #[debug(skip)] pub(crate) reddsa::VerificationKey<reddsa::ActionAuth>,
   61 | );
```

_file_excerpt · [crates/tachyon/src/keys/public.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/keys/public.rs#L27) · line 27 · SHA-256 f2e806a6896e88ca2dd32fa70a75bcc42c3c4b0b797dc53f5cab00e499e34851_

```
   26 | #[derive(Clone, Copy, Debug, Display)]
   27 | #[display("ActionVerificationKey({:?})", reddsa::VerificationKeyBytes::from(self.0))]
   28 | pub struct ActionVerificationKey(pub(crate) reddsa::VerificationKey<reddsa::ActionAuth>);
```

_file_excerpt · [crates/tachyon/src/keys/public.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/keys/public.rs#L28) · line 28 · SHA-256 0fe24d0700a23e727cdd92a3075ce1e5d47345bd712bea8ed8caf7252dde4fb8_

```
   27 | #[display("ActionVerificationKey({:?})", reddsa::VerificationKeyBytes::from(self.0))]
   28 | pub struct ActionVerificationKey(pub(crate) reddsa::VerificationKey<reddsa::ActionAuth>);
   29 | 
```

_file_excerpt · [crates/tachyon/src/keys/public.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/keys/public.rs#L46) · line 46 · SHA-256 e53bb10a3849ab6c1aa1cdede1370153eafe5cbd06594d238b360386fe4646f3_

```
   45 |     /// key for that sighash.
   46 |     pub fn verify(&self, sighash: &[u8; 32], sig: &action::Signature) -> Result<(), reddsa::Error> {
   47 |         self.0.verify(sighash, &sig.0)
```

_file_excerpt · [crates/tachyon/src/reddsa.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/reddsa.rs#L7) · line 7 · SHA-256 6d4ccd8d10424d3d378a9a7e88892d8bc25ae06e9f350b6bf4c022f6172af00d_

```
    6 | 
    7 | use ::reddsa::orchard;
    8 | pub(crate) use ::reddsa::{Error, Signature, SigningKey, VerificationKey, VerificationKeyBytes};
```

_file_excerpt · [crates/tachyon/src/reddsa.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/reddsa.rs#L8) · line 8 · SHA-256 77eeae14bf7b8f347d48553bd3036a1dbf5076b9b6a91017473345c2668b0dcb_

```
    7 | use ::reddsa::orchard;
    8 | pub(crate) use ::reddsa::{Error, Signature, SigningKey, VerificationKey, VerificationKeyBytes};
    9 | 
```

_file_excerpt · [crates/tachyon/src/serialization/mod.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/serialization/mod.rs#L79) · line 79 · SHA-256 79c1e52cddc7e58d0fee89c204f80be9de528bc26eeef673e55a8df88ec638c8_

```
   78 |     mut reader: R,
   79 | ) -> io::Result<reddsa::VerificationKey<reddsa::ActionAuth>> {
   80 |     let mut bytes = [0u8; 32];
```

_file_excerpt · [crates/tachyon/src/serialization/mod.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/serialization/mod.rs#L82) · line 82 · SHA-256 1cf340d889c5613d44c473cb72b2e4e3372a6fd1c50b2550c07ef0a465a6cc18_

```
   81 |     reader.read_exact(&mut bytes)?;
   82 |     reddsa::VerificationKey::<reddsa::ActionAuth>::try_from(bytes).map_err(|_err| {
   83 |         io::Error::new(
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-49588 — Квантово-уязвимый RedDSA: аутентификация и идентификация (сертификаты, токены, аттестация устройств) (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:RedDSA:authentication`
- Источник данных: crates/tachyon/src/keys/private.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

16 упоминаний RedDSA в 1 файл(ах), например crates/tachyon/src/keys/private.rs:95. Роль по путям, именам функций и соседнему коду: аутентификация и идентификация (сертификаты, токены, аттестация устройств). Краткоживущая аутентификация безопасна до появления CRQC; долгоживущим идентификаторам (аттестация устройств, ключи УЦ и SSH) план нужен раньше.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте crates/tachyon/src/keys/private.rs:95 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [crates/tachyon/src/keys/private.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/keys/private.rs#L95) · line 95 · SHA-256 e1d11199ceccc6f1c27e4c457f1441994aa647da905f30db1592d61987b2f3dc_

```
   94 |         // the y-sign bit (byte 31, bit 7 of the compressed encoding).
   95 |         let ak: [u8; 32] = reddsa::VerificationKey::from(
   96 |             &reddsa::SigningKey::<reddsa::ActionAuth>::try_from(ask.to_repr())
```

_file_excerpt · [crates/tachyon/src/keys/private.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/keys/private.rs#L96) · line 96 · SHA-256 d516b781a8f2f8dbce8d5cfa82f44e4f864ca9f0b882d7462edb8e615fbf862f_

```
   95 |         let ak: [u8; 32] = reddsa::VerificationKey::from(
   96 |             &reddsa::SigningKey::<reddsa::ActionAuth>::try_from(ask.to_repr())
   97 |                 .expect("PRF-derived ask should be a valid RedPallas scalar"),
```

_file_excerpt · [crates/tachyon/src/keys/private.rs](https://github.com/tachyon-zcash/tachyon/blob/6cdaebccf147c5a013d212f9d7302924a9570626/crates/tachyon/src/keys/private.rs#L97) · line 97 · SHA-256 8c3d41d1466260fe9cbf9603ba9f9b83fbe6fd57fdff0118f14b2fa9a9fd9d26_

```
   96 |             &reddsa::SigningKey::<reddsa::ActionAuth>::try_from(ask.to_repr())
   97 |                 .expect("PRF-derived ask should be a valid RedPallas scalar"),
   98 |         )
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-49591 — crossbeam-epoch 0.9.18 затронут RUSTSEC-2026-0204 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crossbeam-epoch@0.9.18`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0204 для пакета crates.io crossbeam-epoch версии 0.9.18: Invalid pointer dereference in `fmt::Pointer` impl for `Atomic` and `Shared` when the underlying pointer is invalid. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует crossbeam-epoch: он приходит через другие зависимости, и как они его используют, не прослеживалось. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.9.20).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-49592 — heapless 0.7.17 затронут RUSTSEC-2026-0574 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/heapless@0.7.17`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0574 для пакета crates.io heapless версии 0.7.17: `FindMutView::pop` after mutating the value would lead to a use after free. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует heapless: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (heapless::sorted_linked_list::FindMutView::pop); heapless приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0574
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0574](https://osv.dev/vulnerability/RUSTSEC-2026-0574) · manifest · SHA-256 8036d7decb205a3a78a01ce5b0c508dd8b0522d0e0ac6e4be98d7cc2a3a88814_

```
{"id": "RUSTSEC-2026-0574", "aliases": [], "modified": "2026-11-19T09:00:03.915405109Z", "summary": "`FindMutView::pop` after mutating the value would lead to a use after free", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.9.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-49593 — heapless 0.7.17 затронут RUSTSEC-2026-0575 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/heapless@0.7.17`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0575 для пакета crates.io heapless версии 0.7.17: `Spsc::peek` used `Relaxed` ordering where it should have use `Acquire`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует heapless: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (heapless::spsc::Spsc::peek); heapless приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0575
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0575](https://osv.dev/vulnerability/RUSTSEC-2026-0575) · manifest · SHA-256 9f03365d2d31b79a56c6ea51189c7bce15fb54454c2d6742f955918015ec6112_

```
{"id": "RUSTSEC-2026-0575", "aliases": [], "modified": "2026-11-19T09:00:04.331392862Z", "summary": "`Spsc::peek` used `Relaxed` ordering where it should have use `Acquire`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.9.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-49594 — heapless 0.7.17 затронут RUSTSEC-2026-0576 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/heapless@0.7.17`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0576 для пакета crates.io heapless версии 0.7.17: `IndexMap::truncate` could lead to an inconsistent state. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует heapless: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (heapless::index_map::IndexMap::truncate); heapless приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0576
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0576](https://osv.dev/vulnerability/RUSTSEC-2026-0576) · manifest · SHA-256 cac89759a1ba626d6fdebb9eb010c068a97a8d8680f22993b22c42ee2997fa94_

```
{"id": "RUSTSEC-2026-0576", "aliases": [], "modified": "2026-11-19T09:00:03.918246184Z", "summary": "`IndexMap::truncate` could lead to an inconsistent state", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.9.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-49595 — heapless 0.7.17 затронут RUSTSEC-2026-0577 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/heapless@0.7.17`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0577 для пакета crates.io heapless версии 0.7.17: Panicking `Drop` implementation could lead to UB. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует heapless: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (heapless::deque::Deque::clear, heapless::history_buf::HistoryBuf::clear, heapless::history_buf::HistoryBuf::write, heapless::index_map::IndexMap::clear, heapless::index_map::IndexMap::retain, heapless::index_map::IndexMap::truncate …); heapless приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0577
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0577](https://osv.dev/vulnerability/RUSTSEC-2026-0577) · manifest · SHA-256 5b57e830ce2d429efd9cb1e499aa9b3c6aaf89deaa7402e9c7e0faac2758e903_

```
{"id": "RUSTSEC-2026-0577", "aliases": [], "modified": "2026-11-19T09:00:04.328496490Z", "summary": "Panicking `Drop` implementation could lead to UB", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.9.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-49596 — heapless 0.7.17 затронут RUSTSEC-2026-0578 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/heapless@0.7.17`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0578 для пакета crates.io heapless версии 0.7.17: `SortedLinkedList::zeroize` lead to an inconsistent state. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует heapless: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (heapless::sorted_linked_list::SortedLinkedList::zeroize); heapless приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0578
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0578](https://osv.dev/vulnerability/RUSTSEC-2026-0578) · manifest · SHA-256 e8d0c30a9cc7cab83146a688628a34d55adcbfab254506dc2b0192d326846460_

```
{"id": "RUSTSEC-2026-0578", "aliases": [], "modified": "2026-11-19T09:00:04.321872625Z", "summary": "`SortedLinkedList::zeroize` lead to an inconsistent state", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.9.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-49597 — heapless 0.7.17 затронут RUSTSEC-2026-0579 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/heapless@0.7.17`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0579 для пакета crates.io heapless версии 0.7.17: The `Deque` implementation from `TryFrom` was wrong when the `Deque` ended up full. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует heapless: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (heapless::Deque::try_from); heapless приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0579
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0579](https://osv.dev/vulnerability/RUSTSEC-2026-0579) · manifest · SHA-256 bea200d5cec036d98e0f13e7fc6b2e9ce592314cb1918a6a21d2d1c2eea51dd8_

```
{"id": "RUSTSEC-2026-0579", "aliases": [], "modified": "2026-11-19T09:00:03.915731439Z", "summary": "The `Deque` implementation from `TryFrom` was wrong when the `Deque` ended up full", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.9.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-49598 — heapless 0.7.17 затронут RUSTSEC-2026-0580 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/heapless@0.7.17`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0580 для пакета crates.io heapless версии 0.7.17: The treiber stack implementation in heapless had a race condition. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код называет heapless::pool: затронутый код может быть достижим.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0580
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0580](https://osv.dev/vulnerability/RUSTSEC-2026-0580) · manifest · SHA-256 d7fc272ae71e632e608f39a00a878d7c148b3534146d7d3f3c1ab40d7a839470_

```
{"id": "RUSTSEC-2026-0580", "aliases": [], "modified": "2026-11-19T09:00:04.526645559Z", "summary": "The treiber stack implementation in heapless had a race condition", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.9.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-49599 — heapless 0.7.17 затронут RUSTSEC-2026-0581 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/heapless@0.7.17`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0581 для пакета crates.io heapless версии 0.7.17: `Deque::make_contiguous` could lead to broken invariants. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует heapless: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (heapless::deque::Deque::make_contiguous); heapless приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0581
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0581](https://osv.dev/vulnerability/RUSTSEC-2026-0581) · manifest · SHA-256 e134d1cf51573225805d3457b5cc7efecd5c9cb917a4b4da1ece41317c0894f4_

```
{"id": "RUSTSEC-2026-0581", "aliases": [], "modified": "2026-11-19T09:00:03.911566789Z", "summary": "`Deque::make_contiguous` could lead to broken invariants", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.9.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-49600 — heapless 0.7.17 затронут RUSTSEC-2026-0582 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/heapless@0.7.17`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0582 для пакета crates.io heapless версии 0.7.17: On maps of `u16::MAX` elements, `IndexMap::insert` could lead to a broken invariant. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни один исходный файл продукта не импортирует heapless: он приходит через другие зависимости, и как они его используют, не прослеживалось. Проверенный код не упоминает затронутые функции (heapless::index_map::IndexMap::insert); heapless приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0582
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0582](https://osv.dev/vulnerability/RUSTSEC-2026-0582) · manifest · SHA-256 a4a714de3b1b4b8b4b7f6f8c97a3c93cae061db7faeca3ee0605e5a9c03d4830_

```
{"id": "RUSTSEC-2026-0582", "aliases": [], "modified": "2026-11-19T09:00:04.317864790Z", "summary": "On maps of `u16::MAX` elements, `IndexMap::insert` could lead to a broken invariant", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: импортирует ли проверенный код продукта пакет вообще (пути импорта Go, import и require в JavaScript, имена крейтов Rust), затронутые функции из бюллетеня — по идентификаторам этого кода, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.9.4).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-49590 — atomic-polyfill 1.0.3: информационный бюллетень RUSTSEC-2023-0089 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/atomic-polyfill@1.0.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.20.0 · 2026-11-24 11:26 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2023-0089 для пакета crates.io atomic-polyfill версии 1.0.3 как информационный (unmaintained): atomic-polyfill is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2023-0089
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2023-0089](https://osv.dev/vulnerability/RUSTSEC-2023-0089) · manifest · SHA-256 0fcfb6f26f61ecb982bc38b6d6f12db7c77d0fc40bf9353a089129368e765f0f_

```
{"id": "RUSTSEC-2023-0089", "aliases": [], "modified": "2025-04-29T08:31:10Z", "summary": "atomic-polyfill is unmaintained", "severity": null, "declared_in_manifest": false}
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

- Только классика — пороговая подпись и протоколы MPC: Pedersen commitment (1 файл(ов))

**Следующий шаг:** Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **пороговая подпись и протоколы MPC** | Pedersen commitment (1) | QSI-2026-49589 | Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли |
| **аутентификация и идентификация (сертификаты, токены, аттестация устройств)** | RedDSA (1) | QSI-2026-49588 | Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме |
| **роль не определена** | RedDSA (6) | QSI-2026-49587 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | Pedersen commitment (1), RedDSA (9) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | BLAKE2 (1), Poseidon (14) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | BLAKE2 (1), Poseidon (14) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- osv_advisories: 7 package(s) are built from git repositories (forks or unreleased code), so registry advisories were not looked up for them: ragu, ragu_arithmetic, ragu_circuits, ragu_core, ragu_macros, ragu_pasta, ragu_primitives

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-49591 | Разберите RUSTSEC-2026-0204; при необходимости обновите crossbeam-epoch до исправленной версии (0.9.20). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0204 или результат разбора записан. |
| P3 | QSI-2026-49592 | Разберите RUSTSEC-2026-0574; при необходимости обновите heapless до исправленной версии (0.9.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0574 или результат разбора записан. |
| P3 | QSI-2026-49593 | Разберите RUSTSEC-2026-0575; при необходимости обновите heapless до исправленной версии (0.9.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0575 или результат разбора записан. |
| P3 | QSI-2026-49594 | Разберите RUSTSEC-2026-0576; при необходимости обновите heapless до исправленной версии (0.9.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0576 или результат разбора записан. |
| P3 | QSI-2026-49595 | Разберите RUSTSEC-2026-0577; при необходимости обновите heapless до исправленной версии (0.9.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0577 или результат разбора записан. |
| P3 | QSI-2026-49596 | Разберите RUSTSEC-2026-0578; при необходимости обновите heapless до исправленной версии (0.9.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0578 или результат разбора записан. |
| P3 | QSI-2026-49597 | Разберите RUSTSEC-2026-0579; при необходимости обновите heapless до исправленной версии (0.9.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0579 или результат разбора записан. |
| P3 | QSI-2026-49598 | Разберите RUSTSEC-2026-0580; при необходимости обновите heapless до исправленной версии (0.9.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0580 или результат разбора записан. |
| P3 | QSI-2026-49599 | Разберите RUSTSEC-2026-0581; при необходимости обновите heapless до исправленной версии (0.9.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0581 или результат разбора записан. |
| P3 | QSI-2026-49600 | Разберите RUSTSEC-2026-0582; при необходимости обновите heapless до исправленной версии (0.9.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0582 или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-49589 | Внесите использования Pedersen commitment в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-49587 | Внесите использования RedDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-49588 | Внесите использования RedDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-49589 | Запланируйте миграцию Pedersen commitment на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-49587 | Запланируйте миграцию RedDSA на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-49588 | Запланируйте миграцию RedDSA на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-49590 | Замените atomic-polyfill поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | atomic-polyfill заменён или решение зафиксировано. |

## 11. Использованные инструменты

- blockchain 1.0.0
- certificates 1.2.0
- chain_map 1.0.0
- configs 1.1.0
- crediting 1.4.0
- dependencies 1.6.0
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
- qsi-engine 1.20.0
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
17. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
18. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
19. OSV advisory RUSTSEC-2023-0089 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2023-0089> (modified 2025-04-29T08:31:10Z)
20. OSV advisory RUSTSEC-2026-0204 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0204> (modified 2026-07-06T22:30:04.159269138Z)
21. OSV advisory RUSTSEC-2026-0574 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0574> (modified 2026-11-19T09:00:03.915405109Z)
22. OSV advisory RUSTSEC-2026-0575 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0575> (modified 2026-11-19T09:00:04.331392862Z)
23. OSV advisory RUSTSEC-2026-0576 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0576> (modified 2026-11-19T09:00:03.918246184Z)
24. OSV advisory RUSTSEC-2026-0577 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0577> (modified 2026-11-19T09:00:04.328496490Z)
25. OSV advisory RUSTSEC-2026-0578 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0578> (modified 2026-11-19T09:00:04.321872625Z)
26. OSV advisory RUSTSEC-2026-0579 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0579> (modified 2026-11-19T09:00:03.915731439Z)
27. OSV advisory RUSTSEC-2026-0580 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0580> (modified 2026-11-19T09:00:04.526645559Z)
28. OSV advisory RUSTSEC-2026-0581 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0581> (modified 2026-11-19T09:00:03.911566789Z)
29. OSV advisory RUSTSEC-2026-0582 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0582> (modified 2026-11-19T09:00:04.317864790Z)
30. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
31. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
32. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

По происхождению: собственный код 25 (10 уязвимы для алгоритма Шора).

| Алгоритм | Параметр | Библиотека | Расположение | Квантовый статус | Классический статус |
|---|---|---|---|---|---|
| BLAKE2 |  |  | crates/tachyon/src/digest/blake2b.rs | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/digest/mod.rs:8 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/digest/poseidon.rs:14 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/fee.rs:10 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/keys/master.rs:7 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/keys/note.rs:8 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/note.rs:41 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/primitives/action_digest.rs:4 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/primitives/anchor.rs:9 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/primitives/effect.rs:12 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/stamp/proof/delegation.rs:17 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/stamp/proof/evidence.rs:26 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/stamp/proof/output.rs:11 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/stamp/proof/qr.rs:36 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Poseidon |  |  | crates/tachyon/src/stamp/proof/stamp.rs:15 | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо |
| Pedersen commitment |  |  | crates/tachyon/src/value.rs:18 | уязвим (Шор) | допустимо |
| RedDSA |  |  | crates/tachyon/src/action.rs:267 | уязвим (Шор) | допустимо |
| RedDSA |  |  | crates/tachyon/src/bundle/mod.rs:1215 | уязвим (Шор) | допустимо |
| RedDSA |  |  | crates/tachyon/src/keys/private.rs:95 | уязвим (Шор) | допустимо |
| RedDSA | RedPallas |  | crates/tachyon/src/keys/private.rs:97 | уязвим (Шор) | допустимо |
| RedDSA |  |  | crates/tachyon/src/keys/proof.rs:60 | уязвим (Шор) | допустимо |
| RedDSA | RedPallas |  | crates/tachyon/src/keys/public.rs:151 | уязвим (Шор) | допустимо |
| RedDSA |  |  | crates/tachyon/src/keys/public.rs:27 | уязвим (Шор) | допустимо |
| RedDSA |  |  | crates/tachyon/src/reddsa.rs:7 | уязвим (Шор) | допустимо |
| RedDSA |  |  | crates/tachyon/src/serialization/mod.rs:79 | уязвим (Шор) | допустимо |

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| .cargo/config.toml | 52 | `428938c0741ca2a18a8203d557a18b08225f3d9d4df9cdf03791e5b57cb9893c` | 0 |
| Cargo.lock | 23377 | `b67aefb4e4da4534279c4f4936d58a13893ac693574966a10722db4b85e1b291` | 0 |
| Cargo.toml | 7786 | `1fca0bda74e9127531bbe858d3e3fa24659c430054f5269c093a1c9f3ae48bcf` | 0 |
| book/mermaid-init.js | 1262 | `ccf746f10c0a71bd34799867d2f9860dddb5fc6efc6c50d1ea55a1eb1a7bd406` | 0 |
| crates/tachyon/Cargo.toml | 3113 | `bf28d8b3bd41d2d14e91d7321cb30a44b0a74357233aae213d89b0d565c941e1` | 0 |
| crates/tachyon/src/action.rs | 9008 | `e44def1c1daed39201890625a754c686e2787b110cdf178f912efc6ca31b54c9` | 0 |
| crates/tachyon/src/bundle/mod.rs | 45384 | `89739155e7e88dfdb57d2c662377599e2bd86e302c44614e3e9d6ecf3a429f82` | 0 |
| crates/tachyon/src/collections/indexed_multiset.rs | 5220 | `f5575e48ecefda1fef1ee4bb63c5bdb6ec839d00b0f48628325688d35bfda6a2` | 0 |
| crates/tachyon/src/collections/mod.rs | 3151 | `35d6ad8a0197d0827629457b5c8d5f80acea275548da9a11ae415206afdca707` | 0 |
| crates/tachyon/src/collections/multiset.rs | 423 | `22a8dcdf5f31a2c52df2b2edcb1d23db9fbf846385526ef5b7042f7a6d51c508` | 0 |
| crates/tachyon/src/collections/qr.rs | 16544 | `15456586329a2eb7c432a89ad6e23db031bac087789bb4b6a1856e902be1aba2` | 0 |
| crates/tachyon/src/constants.rs | 850 | `4b998e60e05da28da9d042c0f0b8ca44793591e4b9d581389cff3762012ead0b` | 0 |
| crates/tachyon/src/digest/blake2b.rs | 9025 | `777db0305807af132b4a0a90dde2bfe2889ec3eb02e5735490d45dd050529ab1` | 0 |
| crates/tachyon/src/digest/mod.rs | 294 | `672e241df48535eb0339a0caf1401a7bf986e243c277174c6ef838adbdd120ef` | 0 |
| crates/tachyon/src/digest/poseidon.rs | 9073 | `9f822d99a1d7185b52485e10ec3da43496353d985e9c55305937f9ec656288dd` | 0 |
| crates/tachyon/src/entropy.rs | 6263 | `e56db1c8b9ccf7cd2b0647574dde253442aa57550cebb7e03d8fab95397d7101` | 0 |
| crates/tachyon/src/fee.rs | 1867 | `4868083f2b7d2ba5fbfc94ab2250062e568587287b7420edfc1b18ca529aef6a` | 0 |
| crates/tachyon/src/keys/master.rs | 3142 | `00836539de80b74d3467b34763ed90e13fe1f309231bbf91fded3135b1e9ea24` | 0 |
| crates/tachyon/src/keys/mod.rs | 8008 | `973b459e39dbcab74e5260a6411f8af08049313ae0ca5700a0371645417e1039` | 0 |
| crates/tachyon/src/keys/note.rs | 6248 | `a51c30cf8f6d04763baac65ae26af61433c5d8e3ab3a61d75f1334a05c16db5c` | 0 |
| crates/tachyon/src/keys/private.rs | 11035 | `d14059dbeff2c2b5aef4a26967e86cdcfbd7a21e9de8be695718fd58d0ae9935` | 0 |
| crates/tachyon/src/keys/proof.rs | 3069 | `f177d7eaecd09ddb2e0a1849eba276a2004b1a7f0cff95019e61753c65b3e53e` | 0 |
| crates/tachyon/src/keys/public.rs | 5658 | `a2b330c55873c67c258ab44395e78044d450cd1415b63473aa53ae6c17175411` | 0 |
| crates/tachyon/src/lib.rs | 987 | `47b57a395c75eaddfe3d5284eac64a7e25fe2d9bca8d51dd6ff1fd768bbef6c3` | 0 |
| crates/tachyon/src/note.rs | 5343 | `361d20b7ebffaa92a36ba83f361ba865d0bc4f2a143909ae086fcda5300c32e4` | 0 |
| crates/tachyon/src/nullifier/mod.rs | 1896 | `f50d9be8e47cfd49620de661ef51bde8b9a1e17ff06c911a03b690fd85e8cc71` | 0 |
| crates/tachyon/src/primitives/action_digest.rs | 3998 | `0e3ded8378b19d4c44d81157f5ca23d9749b3d57ab2495e7f2d7563062f17a1e` | 0 |
| crates/tachyon/src/primitives/anchor.rs | 5272 | `1e5b9553a9d2168d9878289e08460876033e79e3b23d82999b6d3b3c92d5a8a8` | 0 |
| crates/tachyon/src/primitives/block_height.rs | 2348 | `47de268427c9dfa9bb90bf32e2023508ace29707bcb9bd1c0cf53d74765ab4a5` | 0 |
| crates/tachyon/src/primitives/effect.rs | 2052 | `f69dcfddd89110b70e9d08aff9ed2d15a381ad339a8a421f6a08a68a016574d8` | 0 |
| crates/tachyon/src/primitives/epoch.rs | 4011 | `26f93e49de8b801f8c28ed5d7c04e1f2410ecf4bcf1ea60245df2019e1bd7eac` | 0 |
| crates/tachyon/src/primitives/evidence.rs | 365 | `468098d982be84be6b9f6a8b3b55171bfe20e54d5358756210e5b6d45c60bbb4` | 0 |
| crates/tachyon/src/primitives/mod.rs | 702 | `2f8ec1a4f18b62fdacd7c40721b9c23cb22111a908422b3418aa698b4061144b` | 0 |
| crates/tachyon/src/primitives/qr.rs | 9049 | `66fb158bad16bea5a28dec2353847b07fd6f8792fa2ef2a7ddbd153f9c9c56a6` | 0 |
| crates/tachyon/src/primitives/seq.rs | 1911 | `348cd8b4eadaa5025db4cba9d2b8b7d55448dede3bb7fe2e6c1ba12dd8e141fb` | 0 |
| crates/tachyon/src/primitives/sets.rs | 5897 | `12099f6c23382cc169e0e68b49937013de8b8e96f8ded33f11c9656d8ae6bab3` | 0 |
| crates/tachyon/src/primitives/tachygram.rs | 2285 | `6a1b5faac4ffd142d79996a8055edeb6c8a751299bcaea7c399e83da6322621f` | 0 |
| crates/tachyon/src/ragu_constraint.rs | 1895 | `933ff2698dbb28adb1121237ab7818cb8ba38e3f05b9931bd4c198fd71c524c5` | 0 |
| crates/tachyon/src/reddsa.rs | 664 | `383bf0dab67da97d8c05c3d17810cc82560faba6c8960541aa56c4b62c8680ff` | 0 |
| crates/tachyon/src/relations/enforce.rs | 6181 | `6969f2838db81f394e4394a44be0fa68f7f86c7a3bd75c754232a045ed2d9ece` | 0 |
| crates/tachyon/src/relations/mod.rs | 278 | `5b63b54412f40b975e095ca60e3727316afd0b9e7a6efacf61b0a27b929af4e2` | 0 |
| crates/tachyon/src/serialization/compactsize.rs | 17214 | `384b1ffd39a70173b9f2c0870172b16ef6907d0b91d4d3afd383c2d2b2c186b4` | 0 |
| crates/tachyon/src/serialization/mod.rs | 4732 | `4c5d40d9da4cbfaa6360fbeb1df898773a7f1df0805f917c3eee89fabeaff06c` | 0 |
| crates/tachyon/src/stamp/mod.rs | 41833 | `57bd4d85c56a49e1558d21ef78131dd1006bd34a1e29a0bcd678b16defbddd01` | 0 |
| crates/tachyon/src/stamp/proof/delegation.rs | 11915 | `bc295aceaf1d0a2aa0c5e0296fd37d2ee5f07b1537fc8cebbae0d8410d04f524` | 0 |
| crates/tachyon/src/stamp/proof/evidence.rs | 18911 | `98181f231fb7ec28063ffcd3b208ed0b5bc2a3e80e2806f6039c237e5a731ab2` | 0 |
| crates/tachyon/src/stamp/proof/mod.rs | 3089 | `c2c68afbd41046fba0ac5e7903c50722721936258f75b130c515e52540e8dba0` | 0 |
| crates/tachyon/src/stamp/proof/output.rs | 2897 | `3067f8f9a16dea2e609f06d66d9ccaef0d6159593600523022a57f1f0bb9a4e8` | 0 |
| crates/tachyon/src/stamp/proof/pool.rs | 21575 | `e3adec9456045e58575bacc1502fef2ea85acf3b0fb83ad8b3fcd7aa6b88eaf1` | 0 |
| crates/tachyon/src/stamp/proof/qr.rs | 30724 | `e2d3f5048ff20818a445e6ea2c22dabf5745c9cfc1b5f8698abb42cec2f065b9` | 0 |
| crates/tachyon/src/stamp/proof/spend.rs | 5019 | `c32b5ec9af52c23ed7ef2ed8e7b7a9447ca5816cb45087759a88ea6826ef81d1` | 0 |
| crates/tachyon/src/stamp/proof/spendable.rs | 10176 | `f2bde364fa9b7a360434fa748b53b8a750d82b3a13ffedc50d25eca6b0ee52ea` | 0 |
| crates/tachyon/src/stamp/proof/stamp.rs | 26299 | `13de79e7b476999fe8363a66299e32d608641f6093d0fb15a3ba5f4e1c2e4821` | 0 |
| crates/tachyon/src/stamp/proof/summary.rs | 4533 | `051856e8dd8c680bfd3b392085bc651525e201160e87d0a04f22351d20ab5f69` | 0 |
| crates/tachyon/src/value.rs | 9043 | `5bc365a663432264e7c4c995a3474ad5a4796b7c8759bfbe4e1418120e0f69d6` | 0 |
| crates/tachyon/src/witness.rs | 20784 | `56cbfdcf9b3dc1565ff2cfa687c5407f444d8acef1afe7e90d8d95e3116b3f0d` | 0 |
| rust-toolchain.toml | 115 | `c54d9d27dffd85dc7b368bc6c85376b99a6ccb54b44f6a0a0c1a511d9ce35e41` | 0 |
