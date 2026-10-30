# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** reddsa @ 04e973bcf8d4 · Zcash Foundation — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-29 23:42 UTC |
| Версия отчёта | 1 |
| Запуск аудита | eb279341-8c00-4ae1-9a0f-b358aa847fc9 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `d9243f8dfd3941e5e6a92db037b26c39dbdc1672e3532e89daa13c24c6b57733` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **0**
- Средняя: **2**
- Низкая: **0**
- Информационная: **2**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 0
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 2
- Рекомендация по улучшению: 1
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/ZcashFoundation/reddsa> @ `04e973bcf8d46819db055ebd0d44304c24a156a4` — ссылки в доказательствах открывают строки на этом коммите.

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| Cargo.lock | 30238 | `217f7f54967a76b15a91e0d0c3bccf5b3f067f3fcd77eab0d2acac4b405b9ecb` | 0 |
| Cargo.toml | 2180 | `1583dbe342f22d6c74c38285fbb41471faeb998d920394519798e1b454c979de` | 0 |
| src/batch.rs | 10206 | `a4fa2e3dcd45fb3dc060d8dcd0fe14dd6184383e04c6c8e08f4db763a72a8c4d` | 0 |
| src/constants.rs | 890 | `bf76bc1fe6375973a72af170f91f51ce1a34fc7b39b3c9f4b03ffa0ec90d419c` | 0 |
| src/error.rs | 1049 | `993754bf8dd056065f8ea7b1ac253fb330bd9fd520d27fe132625ec0d894116c` | 0 |
| src/hash.rs | 1622 | `96e2e2e0fb88bd1b25b07900a13c3f40590e0dac046ef46b1bef4ebb86fc561a` | 0 |
| src/internal.rs | 493 | `4cac9407db2114ae96fe24d0fcd029d22f66c8d2512cfbb0a4263121f19985be` | 0 |
| src/lib.rs | 4754 | `0e8171122eb4d548d709e8b1e86f56041d6ec618a72ca03b9df63d3f858bbf4d` | 0 |
| src/messages.rs | 11571 | `c562ab55a1fd8475000bdc7149193a3a8f8651077e57de8074508fcdb835e787` | 0 |
| src/orchard.rs | 4926 | `bbe653123789105467c177913fc8f84c1b1da6524eac8095d4c38b315b8f1c4a` | 0 |
| src/sapling.rs | 797 | `e1a79c4db2d7e3d7984a6bbdfdd3d915cbdec6509064b4b726f9b9b139e1cf51` | 0 |
| src/scalar_mul.rs | 8326 | `641a008b6d9d4c97649143b292c92b23b266c333c65fe5289722090fa2ed0854` | 0 |
| src/signature.rs | 1585 | `9c9bdf2359aad47f48db150a9ba781ccf2dcf0b91b05d0f0a11a1306b85fb8de` | 0 |
| src/signing_key.rs | 6963 | `a06db739109eea3939c6f5f5e6e704f0079cc298e83ce4e1ff103fa85a6a8aba` | 0 |
| src/verification_key.rs | 7478 | `173f8f563bcf59d253d8420ac55eb2d931b654f915a4922912878d5b09dc6584` | 0 |

## 3. Методология

| Область | Статус | Подробности |
|---|---|---|
| dependencies | проверено | Cargo.lock: 130 dependencies parsed (130 pinned) |
| dependencies | проверено | Cargo.toml: 22 dependencies parsed (0 pinned) |
| source_code | проверено | src/batch.rs: 278 lines scanned with 16 rule patterns and 128 registry patterns |
| source_code | проверено | src/constants.rs: 24 lines scanned with 16 rule patterns and 128 registry patterns |
| source_code | проверено | src/error.rs: 35 lines scanned with 16 rule patterns and 128 registry patterns |
| source_code | проверено | src/hash.rs: 61 lines scanned with 16 rule patterns and 128 registry patterns |
| source_code | проверено | src/internal.rs: 14 lines scanned with 16 rule patterns and 128 registry patterns |
| source_code | проверено | src/lib.rs: 154 lines scanned with 16 rule patterns and 128 registry patterns |
| source_code | проверено | src/messages.rs: 277 lines scanned with 16 rule patterns and 128 registry patterns |
| source_code | проверено | src/orchard.rs: 157 lines scanned with 16 rule patterns and 128 registry patterns |
| source_code | проверено | src/sapling.rs: 27 lines scanned with 16 rule patterns and 128 registry patterns |
| source_code | проверено | src/scalar_mul.rs: 246 lines scanned with 16 rule patterns and 128 registry patterns |
| source_code | проверено | src/signature.rs: 55 lines scanned with 16 rule patterns and 128 registry patterns |
| source_code | проверено | src/signing_key.rs: 227 lines scanned with 16 rule patterns and 128 registry patterns; 29 lines in #[cfg(test)] modules ignored |
| source_code | проверено | src/verification_key.rs: 207 lines scanned with 16 rule patterns and 128 registry patterns |
| osv_advisories | проверено | 130 pinned packages queried at OSV.dev; 1 affected (1 of them only in development or build dependencies) |

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree reddsa at 04e973bcf8d46819db055ebd0d44304c24a156a4. 15 files analysed; of 42 files, 9 are test, fuzzing, benchmark or example code and were left out, 18 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .github/dependabot.yml, .github/release-drafter.yml, .github/workflows/coverage.yaml, .github/workflows/main.yml, .github/workflows/release-drafter.yml. 31 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **100** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 33.3%

## 7. Подробное описание находок

### QSI-2026-07275 — Квантово-уязвимый FROST: пороговая подпись и протоколы MPC (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:FROST:threshold_mpc`
- Источник данных: src/messages.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:42 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

6 упоминаний FROST в 1 файл(ах), например src/messages.rs:39. Роль по путям, именам функций и соседнему коду: пороговая подпись и протоколы MPC. Paillier, обязательства Педерсена и доказательства на дискретном логарифме внутри пороговых ECDSA и EdDSA ломаются алгоритмом Шора; постквантовая пороговая схема — это смена протокола, а не параметра.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/messages.rs:39 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/messages.rs](https://github.com/ZcashFoundation/reddsa/blob/04e973bcf8d46819db055ebd0d44304c24a156a4/src/messages.rs#L39) · line 39 · SHA-256 3ad3ca50bbcc97f879d408d4ad39d2bdede892e7a9d850c58b48241992b2b359_

```
   38 | 
   39 | impl<S: SpendAuth> From<frost::Commitment<S>> for Commitment {
   40 |     fn from(value: frost::Commitment<S>) -> Commitment {
```

_file_excerpt · [src/messages.rs](https://github.com/ZcashFoundation/reddsa/blob/04e973bcf8d46819db055ebd0d44304c24a156a4/src/messages.rs#L40) · line 40 · SHA-256 65d226a68df2d189afb1eaf7f3707c4560aa92f6c002f53abef1424875081306_

```
   39 | impl<S: SpendAuth> From<frost::Commitment<S>> for Commitment {
   40 |     fn from(value: frost::Commitment<S>) -> Commitment {
   41 |         // TODO(str4d): We need to either enforce somewhere that these messages are only
```

_file_excerpt · [src/messages.rs](https://github.com/ZcashFoundation/reddsa/blob/04e973bcf8d46819db055ebd0d44304c24a156a4/src/messages.rs#L228) · line 228 · SHA-256 62a5b176caa27cd457d4164701bc6e4f624d99ea5ddd17734ec6ee4d4af8ec5e_

```
  227 | 
  228 | impl<S: SpendAuth> From<SigningPackage> for frost::SigningPackage<S> {
  229 |     fn from(value: SigningPackage) -> frost::SigningPackage<S> {
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07274 — Квантово-уязвимый RedDSA: роль не определена (3 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:RedDSA:general`
- Источник данных: src/lib.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 23:42 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

8 упоминаний RedDSA в 3 файл(ах), например src/lib.rs:39. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/lib.rs:39 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/lib.rs](https://github.com/ZcashFoundation/reddsa/blob/04e973bcf8d46819db055ebd0d44304c24a156a4/src/lib.rs#L39) · line 39 · SHA-256 e05154e9a56cf4aa5879e5015ea625e4b0609d7031c391602b6a94430ecbbd7f_

```
   38 | /// An element of the protocol's scalar field used for randomization of public and secret keys.
   39 | pub type Randomizer<S> = <S as private::Sealed<S>>::Scalar;
   40 | 
```

_file_excerpt · [src/lib.rs](https://github.com/ZcashFoundation/reddsa/blob/04e973bcf8d46819db055ebd0d44304c24a156a4/src/lib.rs#L66) · line 66 · SHA-256 aed9696d7fe2dfdf006f303ffe492cc9d23031cf01aa014b288d2d60e0796016_

```
   65 | /// A trait corresponding to `SpendAuthSig` in Zcash protocols.
   66 | pub trait SpendAuth: SigType {}
   67 | 
```

_file_excerpt · [src/orchard.rs](https://github.com/ZcashFoundation/reddsa/blob/04e973bcf8d46819db055ebd0d44304c24a156a4/src/orchard.rs#L39) · line 39 · SHA-256 2a63a6db8262d59550636d8be561a03c127d81e0df6bb4a50505772b9d8f5460_

```
   38 | #[derive(Copy, Clone, PartialEq, Eq, Debug)]
   39 | pub enum SpendAuth {}
   40 | // This should not exist, but is necessary to use zeroize::DefaultIsZeroes.
```

_file_excerpt · [src/orchard.rs](https://github.com/ZcashFoundation/reddsa/blob/04e973bcf8d46819db055ebd0d44304c24a156a4/src/orchard.rs#L46) · line 46 · SHA-256 cd85b4b9b8ff5ecf99380306f0320d14b675282fc54a510bab492740bcdd948d_

```
   45 | }
   46 | impl SigType for SpendAuth {}
   47 | impl super::SpendAuth for SpendAuth {}
```

_file_excerpt · [src/orchard.rs](https://github.com/ZcashFoundation/reddsa/blob/04e973bcf8d46819db055ebd0d44304c24a156a4/src/orchard.rs#L58) · line 58 · SHA-256 7775dc8a2ccad06c7bc81924918e253589f66c95749a17f63a42a8745fb55e6d_

```
   57 | }
   58 | impl SigType for Binding {}
   59 | impl super::Binding for Binding {}
```

_file_excerpt · [src/sapling.rs](https://github.com/ZcashFoundation/reddsa/blob/04e973bcf8d46819db055ebd0d44304c24a156a4/src/sapling.rs#L7) · line 7 · SHA-256 8c20e0abac671beca5ba5446ada21d5ead436c57b5169019ad6ec95d3cbbb242_

```
    6 | #[derive(Copy, Clone, PartialEq, Eq, Debug)]
    7 | pub enum SpendAuth {}
    8 | // This should not exist, but is necessary to use zeroize::DefaultIsZeroes.
```

_file_excerpt · [src/sapling.rs](https://github.com/ZcashFoundation/reddsa/blob/04e973bcf8d46819db055ebd0d44304c24a156a4/src/sapling.rs#L14) · line 14 · SHA-256 ce98bcc2f0a6961c8dc1f8f8e589fb75d44de794a392e2945b741a7ba0c434c7_

```
   13 | }
   14 | impl SigType for SpendAuth {}
   15 | impl super::SpendAuth for SpendAuth {}
```

_file_excerpt · [src/sapling.rs](https://github.com/ZcashFoundation/reddsa/blob/04e973bcf8d46819db055ebd0d44304c24a156a4/src/sapling.rs#L26) · line 26 · SHA-256 6145abb25ce349b55814a6a97fda93c14c32044d2cfb405e7df16a90b8a9b83b_

```
   25 | }
   26 | impl SigType for Binding {}
   27 | impl super::Binding for Binding {}
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07277 — 1 бюллетеней в 1 пакет(ах) crates.io, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:crates.io:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:42 UTC
- Балл приоритета: 15.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 1 бюллетеней (0 с оценкой high или critical) для 1 пакет(ов) crates.io, которые подтягивают только инструменты разработки или сборки (Cargo.lock): например, bincode@1.3.3 [dev]: RUSTSEC-2025-0141. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в Cargo.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (crates.io)](https://osv.dev/) · Cargo.lock · SHA-256 92b1213d0f61091716e425a9a06466220ab9c470db4d48232eff3ef32c1a1443_

```
bincode@1.3.3 [dev]: RUSTSEC-2025-0141
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07276 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-29 23:42 UTC
- Балл приоритета: 13.3 / 100
- CVSS v3.1: неприменимо

В 2 манифестах зависимостей QSI нашёл криптобиблиотеки (bls12_381, ff, group, jubjub, pasta_curves), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · Cargo.lock, Cargo.toml · SHA-256 e88913eae28671436a0e91dd5f54d5fa0db5a5ae27bcda4c1ad423fed8b9f1dd_

```
Crypto libraries: bls12_381, ff, group, jubjub, pasta_curves
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
_Допущения планирования: x для обмена ключами, x для подписей, y — значения по умолчанию профиля риска «Криптобиржа, кастодиан или кошелёк», а не данные клиента; с фактическими сроками клиента вывод может измениться._

### Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет


**Следующий шаг:** Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **пороговая подпись и протоколы MPC** | FROST (1) | QSI-2026-07275 | Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли |
| **роль не определена** | RedDSA (3) | QSI-2026-07274 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на постквантовый алгоритм; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | FROST (1), RedDSA (3) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |

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
| P3 | QSI-2026-07275 | Внесите использования FROST в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07274 | Внесите использования RedDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-07275 | Запланируйте миграцию FROST на Как для обычной схемы, которую она порождает: ML-DSA или SLH-DSA там, где это допускает проверяющая сторона; пороговые постквантовые подписи пока в стадии исследований (NIST IR 8214C) (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Как для обычной схемы, которую она порождает: ML-DSA или SLH-DSA там, где это допускает проверяющая сторона; пороговые постквантовые подписи пока в стадии исследований (NIST IR 8214C) или гибридной схемы. |
| P4 | QSI-2026-07274 | Запланируйте миграцию RedDSA на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07277 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |

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

1. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
2. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
3. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
4. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
5. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
6. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
7. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
8. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
9. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
10. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
11. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
12. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
13. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
14. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Расположение | Квантовый статус | Классический статус |
|---|---|---|---|---|---|
| Crypto library | 0.11.1 | jubjub (jubjub) | Cargo.lock | н/п | допустимо |
| Crypto library | 0.14.0 | group (jubjub) | Cargo.lock | н/п | допустимо |
| Crypto library | 0.14.0 | ff (jubjub) | Cargo.lock | н/п | допустимо |
| Crypto library | 0.6.0 | pasta_curves (pasta_curves (Pallas/Vesta)) | Cargo.lock | н/п | допустимо |
| Crypto library | 0.9.0 | bls12_381 (jubjub) | Cargo.lock | н/п | допустимо |
| Crypto library | 0.11 | jubjub (jubjub) | Cargo.toml | н/п | допустимо |
| Crypto library | 0.14 | group (jubjub) | Cargo.toml | н/п | допустимо |
| Crypto library | 0.6 | pasta_curves (pasta_curves (Pallas/Vesta)) | Cargo.toml | н/п | допустимо |
| FROST |  |  | src/messages.rs:39 | уязвим (Шор) | допустимо |
| RedDSA |  |  | src/lib.rs:39 | уязвим (Шор) | допустимо |
| RedDSA |  |  | src/orchard.rs:39 | уязвим (Шор) | допустимо |
| RedDSA |  |  | src/sapling.rs:7 | уязвим (Шор) | допустимо |
