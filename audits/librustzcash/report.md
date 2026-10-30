# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** librustzcash @ 8672a4b2d60f · Electric Coin Company (Zcash) — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-30 00:13 UTC |
| Версия отчёта | 1 |
| Запуск аудита | eeafaa62-023c-4463-ba69-6cc641c1beb4 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `2067f3243e2369935d24cf68a0c3ac722f9a8d4e819bd2211c6bcafbb8a5e36b` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **2**
- Средняя: **11**
- Низкая: **32**
- Информационная: **7**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 43
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 3
- Рекомендация по улучшению: 5
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/zcash/librustzcash> @ `8672a4b2d60f432664780e6a4e85f49a36805a2a` — ссылки в доказательствах открывают строки на этом коммите.

333 файлов, всего 8100632 байт, редактирований: 3; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 307 | .github/helpers/check-dep-graph.py: 115 lines scanned with 16 rule patterns and 128 registry patterns; .github/helpers/check-release-tags.py: 167 lines scanned with 16 rule patterns and 128 registry patterns; components/eip681/src/error.rs: 290 lines scanned with 16 rule patterns and 128 registry patterns |
| dependencies | проверено | 21 | Cargo.lock: 690 dependencies parsed (690 pinned); Cargo.toml: 101 dependencies parsed (10 pinned); components/eip681/Cargo.toml: 11 dependencies parsed (0 pinned) |
| secrets | проверено | 1 | components/eip681/src/request.rs: 3 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| tls_code | проверено | 2 | zcash_client_backend/src/tor.rs: TLS key-exchange settings read; zcash_client_backend/src/tor/http.rs: TLS key-exchange settings read |
| osv_advisories | проверено | 1 | 700 pinned packages queried at OSV.dev; 28 affected (2 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree librustzcash at 8672a4b2d60f432664780e6a4e85f49a36805a2a. 333 files analysed; of 484 files, 54 are test, fuzzing, benchmark or example code and were left out, 97 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .editorconfig, .gitattributes, .github/actions/prepare/action.yml, .github/dependabot.yml, .github/workflows/aggregate-audits.yml. 103 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **1** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 14.7%

## 7. Подробное описание находок

### QSI-2026-07531 — rustls-webpki 0.101.7 затронут GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.101.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104) для пакета crates.io rustls-webpki версии 0.101.7: rustls-webpki: Denial of service via panic on malformed CRL BIT STRING. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-82j2-j2ch-gfr8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-82j2-j2ch-gfr8](https://osv.dev/vulnerability/GHSA-82j2-j2ch-gfr8) · manifest · SHA-256 a2f685e85eb5c808cb9d2de44620be02b2f87b43da592ad8769d4abeedddf3f4_

```
{"id": "GHSA-82j2-j2ch-gfr8", "aliases": ["CVE-2026-93599", "RUSTSEC-2026-0104"], "modified": "2026-09-19T03:55:33.412079637Z", "summary": "rustls-webpki: Denial of service via panic on malformed CRL BIT STRING", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.103.13, 0.104.0-alpha.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07535 — rustls-webpki 0.103.3 затронут GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104)

- Серьёзность: **Высокая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.103.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 37.6 / 100
- CVSS v3.1: 7.5 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`)

OSV.dev сообщает GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104) для пакета crates.io rustls-webpki версии 0.103.3: rustls-webpki: Denial of service via panic on malformed CRL BIT STRING. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-82j2-j2ch-gfr8
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-82j2-j2ch-gfr8](https://osv.dev/vulnerability/GHSA-82j2-j2ch-gfr8) · manifest · SHA-256 a2f685e85eb5c808cb9d2de44620be02b2f87b43da592ad8769d4abeedddf3f4_

```
{"id": "GHSA-82j2-j2ch-gfr8", "aliases": ["CVE-2026-93599", "RUSTSEC-2026-0104"], "modified": "2026-09-19T03:55:33.412079637Z", "summary": "rustls-webpki: Denial of service via panic on malformed CRL BIT STRING", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.103.13, 0.104.0-alpha.7).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07540 — serde_with 3.16.0 затронут GHSA-7gcf-g7xr-8hxj

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/serde_with@3.16.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 44.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-7gcf-g7xr-8hxj для пакета crates.io serde_with версии 3.16.0: serde_with: KeyValueMap serialization panics on empty sequence or map entries. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07503 — Квантово-уязвимый Pedersen commitment: пороговая подпись и протоколы MPC (4 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:Pedersen commitment:threshold_mpc`
- Источник данных: pczt/src/orchard.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

13 упоминаний Pedersen commitment в 4 файл(ах), например pczt/src/orchard.rs:23. Роль по путям, именам функций и соседнему коду: пороговая подпись и протоколы MPC. Paillier, обязательства Педерсена и доказательства на дискретном логарифме внутри пороговых ECDSA и EdDSA ломаются алгоритмом Шора; постквантовая пороговая схема — это смена протокола, а не параметра.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте pczt/src/orchard.rs:23 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [pczt/src/orchard.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/pczt/src/orchard.rs#L23) · line 23 · SHA-256 ceab0b6e960329ba36b083a225009b5f573bb5a46353fd5bc02ebee6c199063e_

```
   22 |         },
   23 |         value::{NoteValue, ValueCommitTrapdoor, ValueCommitment},
   24 |     },
```

_file_excerpt · [pczt/src/orchard.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/pczt/src/orchard.rs#L2161) · line 2161 · SHA-256 6b6748f70bf576cd97e6461d8a6c1dfc5e0cd8335a7a03c4379d504ff3287943_

```
 2160 |         );
 2161 |         let rcv = ValueCommitTrapdoor::from_bytes(
 2162 |             self.rcv
```

_file_excerpt · [pczt/src/orchard.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/pczt/src/orchard.rs#L2168) · line 2168 · SHA-256 14e2a787d8c57b11ecb388d872ab15526a24526cbad0174a72c6e99de4057bce_

```
 2167 | 
 2168 |         self.cv_net = Some(ValueCommitment::derive(spend_value - output_value, rcv).to_bytes());
 2169 |         Ok(())
```

_file_excerpt · [zcash_primitives/src/transaction/components/orchard.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_primitives/src/transaction/components/orchard.rs#L17) · line 17 · SHA-256 b898fb36dbfe34ab7cb1b164bb079efb5379f9fbfa5c96a4e7ec555300893dfe_

```
   16 |     primitives::redpallas::{self, SigType, Signature, SpendAuth, VerificationKey},
   17 |     value::ValueCommitment,
   18 | };
```

_file_excerpt · [zcash_primitives/src/transaction/components/orchard.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_primitives/src/transaction/components/orchard.rs#L237) · line 237 · SHA-256 98f5867a31e27597c3c01fb15d4bff203c7c50e97aeb84452538a6608187c620_

```
  236 | 
  237 | pub fn read_value_commitment<R: Read>(mut reader: R) -> io::Result<ValueCommitment> {
  238 |     let mut bytes = [0u8; 32];
```

_file_excerpt · [zcash_primitives/src/transaction/components/orchard.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_primitives/src/transaction/components/orchard.rs#L240) · line 240 · SHA-256 4273fe713482d561f58f7ead2f139ac70d03ea9dbad8e017bd7461264afd750f_

```
  239 |     reader.read_exact(&mut bytes)?;
  240 |     let cv = ValueCommitment::from_bytes(&bytes);
  241 | 
```

_file_excerpt · [zcash_primitives/src/transaction/components/sapling.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_primitives/src/transaction/components/sapling.rs#L14) · line 14 · SHA-256 92e6baa4894cf218ffaee5a99ea7a496207f7809ceb7dd93bdad9617eac9e172_

```
   13 |     note_encryption::{ENC_CIPHERTEXT_SIZE, Zip212Enforcement},
   14 |     value::ValueCommitment,
   15 | };
```

_file_excerpt · [zcash_primitives/src/transaction/components/sapling.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_primitives/src/transaction/components/sapling.rs#L145) · line 145 · SHA-256 74cbf5fd547cd286f9ab13c63b7ff0d2a3e65edce93bf842d9941a5de530c7c6_

```
  144 | /// - "Not small order" is enforced here.
  145 | fn read_value_commitment<R: Read>(mut reader: R) -> io::Result<ValueCommitment> {
  146 |     let mut bytes = [0u8; 32];
```

_file_excerpt · [zcash_primitives/src/transaction/components/sapling.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_primitives/src/transaction/components/sapling.rs#L148) · line 148 · SHA-256 7d95f61598851f8f97630b7d4273b0d979553c0dd4163a84350ec07504f8e373_

```
  147 |     reader.read_exact(&mut bytes)?;
  148 |     let cv = ValueCommitment::from_bytes_not_small_order(&bytes);
  149 | 
```

_file_excerpt · [zcash_proofs/src/prover.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_proofs/src/prover.rs#L13) · line 13 · SHA-256 9157c5336593c406d960a2e8c63876e8949011faf52f1090e1a110015c78ccd0_

```
   12 |     prover::{OutputProver, SpendProver},
   13 |     value::{NoteValue, ValueCommitTrapdoor},
   14 | };
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07504 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (15 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: pczt/src/roles/signer/mod.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

59 упоминаний ECDSA в 15 файл(ах), например pczt/src/roles/signer/mod.rs:278. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте pczt/src/roles/signer/mod.rs:278 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [pczt/src/roles/signer/mod.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/pczt/src/roles/signer/mod.rs#L278) · line 278 · SHA-256 970c986b642832312ead47151a60f06858a4b568e9da6447791c151d9c3ee86e_

```
  277 |         index: usize,
  278 |         sk: &secp256k1::SecretKey,
  279 |     ) -> Result<(), Error> {
```

_file_excerpt · [pczt/src/roles/signer/mod.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/pczt/src/roles/signer/mod.rs#L299) · line 299 · SHA-256 9c9c7a2df266af024bfa9215a017640135b9c1b6f6054baeca62134856bd215a_

```
  298 |         index: usize,
  299 |         signature: secp256k1::ecdsa::Signature,
  300 |     ) -> Result<(), Error> {
```

_file_excerpt · [zcash_client_backend/src/data_api.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_client_backend/src/data_api.rs#L3935) · line 3935 · SHA-256 96b89b202e7e6ba5fb6a218ecdfd6e64c4c7f004c23a197ce1a7c0e358fc6d20_

```
 3934 |         _account: <Self as WalletRead>::AccountId,
 3935 |         _pubkey: secp256k1::PublicKey,
 3936 |     ) -> Result<(), <Self as WalletRead>::Error> {
```

_file_excerpt · [zcash_client_backend/src/data_api.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_client_backend/src/data_api.rs#L3956) · line 3956 · SHA-256 6ca8dc7f8ad6a96576c26f6abb806e86471829e7355b33eddfdef8e5002014bb_

```
 3955 |         account: <Self as WalletRead>::AccountId,
 3956 |         pubkeys: &[secp256k1::PublicKey],
 3957 |     ) -> Result<(), <Self as WalletRead>::Error> {
```

_file_excerpt · [zcash_client_backend/src/data_api/wallet.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_client_backend/src/data_api/wallet.rs#L1380) · line 1380 · SHA-256 3b9d26a9135dd6c0de7940c206e5fe0f7700515582a4903f60cef7b3fbe84335_

```
 1379 |     #[cfg(feature = "transparent-key-import")]
 1380 |     standalone_transparent_keys: HashMap<TransparentAddress, Vec<secp256k1::SecretKey>>,
 1381 | }
```

_file_excerpt · [zcash_client_backend/src/data_api/wallet.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_client_backend/src/data_api/wallet.rs#L1389) · line 1389 · SHA-256 9aa484cc95bda86ba52610e3ef95bd1009860a3b691a37e0f12d6aae37e82724_

```
 1388 |             TransparentAddress,
 1389 |             Vec<secp256k1::SecretKey>,
 1390 |         >,
```

_file_excerpt · [zcash_client_backend/src/wallet.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_client_backend/src/wallet.rs#L1093) · line 1093 · SHA-256 a2be08c32d9b6f7fab6974e5d502963b486a999af71b05061fca62ffb95d5a70_

```
 1092 |     pub fn standalone_p2pkh(
 1093 |         pubkey: secp256k1::PublicKey,
 1094 |         exposure: Exposure,
```

_file_excerpt · [zcash_client_backend/src/wallet.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_client_backend/src/wallet.rs#L1202) · line 1202 · SHA-256 d1380e8b926885cbf4d779915616b5696ec37a900f98f0a1505563ba0c25c84e_

```
 1201 |     #[cfg(feature = "transparent-key-import")]
 1202 |     StandalonePubkey(secp256k1::PublicKey),
 1203 | 
```

_file_excerpt · [zcash_client_sqlite/src/lib.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_client_sqlite/src/lib.rs#L1951) · line 1951 · SHA-256 0e87728a23fc63465b4ae99448d66aec1aee00fc60e55775df2fb66f029ceb12_

```
 1950 |         account: <Self as WalletRead>::AccountId,
 1951 |         pubkey: secp256k1::PublicKey,
 1952 |     ) -> Result<(), <Self as WalletRead>::Error> {
```

_file_excerpt · [zcash_client_sqlite/src/lib.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_client_sqlite/src/lib.rs#L1960) · line 1960 · SHA-256 0df3a5ae0ebfc4ea62b057c34c50c3fc68a6a763fcd7461a55656ffe68e3f4d9_

```
 1959 |         account: <Self as WalletRead>::AccountId,
 1960 |         pubkeys: &[secp256k1::PublicKey],
 1961 |     ) -> Result<(), <Self as WalletRead>::Error> {
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07505 — Квантово-уязвимый BLS12-381: подпись транзакций и сообщений (4 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:BLS12-381:transaction_signing`
- Источник данных: zcash_proofs/src/circuit/sprout/mod.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

5 упоминаний BLS12-381 в 4 файл(ах), например zcash_proofs/src/circuit/sprout/mod.rs:340. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте zcash_proofs/src/circuit/sprout/mod.rs:340 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [zcash_proofs/src/circuit/sprout/mod.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_proofs/src/circuit/sprout/mod.rs#L340) · line 340 · SHA-256 2756f21b7d7a8d3a022baf241563ed66e885559fd1f4c8cf87ae87c061bfb159_

```
  339 |     use bellman::gadgets::test::*;
  340 |     use bls12_381::Scalar;
  341 | 
```

_file_excerpt · [zcash_proofs/src/lib.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_proofs/src/lib.rs#L15) · line 15 · SHA-256 36b89a654296c8100d863d399d7c6fe1c0fda438afc6aea4b7621d0eeee699d6_

```
   14 | 
   15 | use bls12_381::Bls12;
   16 | use groth16::{PreparedVerifyingKey, VerifyingKey, prepare_verifying_key};
```

_file_excerpt · [zcash_proofs/src/prover.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_proofs/src/prover.rs#L3) · line 3 · SHA-256 07a530126847339f44470f24e6e9fc74c8ca1af51c614ea77c466f5bc8c90c76_

```
    2 | 
    3 | use bls12_381::Bls12;
    4 | use groth16::Proof;
```

_file_excerpt · [zcash_proofs/src/prover.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_proofs/src/prover.rs#L153) · line 153 · SHA-256 94cdcb3fa3766000a515cf37e8aa3a5d2a1c0cd7a54b33a3604a8255764ffd43_

```
  152 |         rcv: ValueCommitTrapdoor,
  153 |         anchor: bls12_381::Scalar,
  154 |         merkle_path: MerklePath,
```

_file_excerpt · [zcash_proofs/src/sprout.rs](https://github.com/zcash/librustzcash/blob/8672a4b2d60f432664780e6a4e85f49a36805a2a/zcash_proofs/src/sprout.rs#L4) · line 4 · SHA-256 927ccca4012b26eb057e2bbe1d966d250cb67af186853d25e3efbf9bbd7fb637_

```
    3 | use bellman::gadgets::multipack;
    4 | use bls12_381::Bls12;
    5 | use groth16::{Parameters, PreparedVerifyingKey, Proof, create_random_proof};
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-07510 — block-buffer 0.10.4 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/block-buffer@0.10.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
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

### QSI-2026-07511 — bytes 1.10.1 затронут GHSA-434x-w66g-qw3r (CVE-2026-25541, RUSTSEC-2026-0007)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/bytes@1.10.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-434x-w66g-qw3r (CVE-2026-25541, RUSTSEC-2026-0007) для пакета crates.io bytes версии 1.10.1: bytes has integer overflow in BytesMut::reserve. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-434x-w66g-qw3r
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-434x-w66g-qw3r](https://osv.dev/vulnerability/GHSA-434x-w66g-qw3r) · manifest · SHA-256 58c8425f679122ea78208908d7c42d7c0f6eb030e5fbaef6d65097f3e6709156_

```
{"id": "GHSA-434x-w66g-qw3r", "aliases": ["CVE-2026-25541", "RUSTSEC-2026-0007"], "modified": "2026-09-10T03:50:33.995841351Z", "summary": "bytes has integer overflow in BytesMut::reserve", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:L/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:H/SC:N/SI:N/SA:N/E:P"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (1.11.1).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07522 — rsa 0.9.6 затронут GHSA-4grx-2x9w-596c (CVE-2023-49092, GHSA-c38w-74pg-36hr, RUSTSEC-2023-0071)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rsa@0.9.6`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.9 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-4grx-2x9w-596c (CVE-2023-49092, GHSA-c38w-74pg-36hr, RUSTSEC-2023-0071) для пакета crates.io rsa версии 0.9.6: Marvin Attack: potential key recovery through timing sidechannels. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-4grx-2x9w-596c
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-4grx-2x9w-596c](https://osv.dev/vulnerability/GHSA-4grx-2x9w-596c) · manifest · SHA-256 0ad76c059f8d6aa8bafc0408cce98e5ddfd2906fe7f762bb486112aefdfd6ba6_

```
{"id": "GHSA-4grx-2x9w-596c", "aliases": ["CVE-2023-49092", "GHSA-c38w-74pg-36hr", "RUSTSEC-2023-0071"], "modified": "2026-09-10T03:50:04.002228238Z", "summary": "Marvin Attack: potential key recovery through timing sidechannels", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (пока не выпущена; меры смягчения — в бюллетене).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07524 — rustls 0.21.12 затронут GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.21.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) для пакета crates.io rustls версии 0.21.12: Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07527 — rustls 0.23.25 затронут GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.23.25`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 5.3 (`CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285) для пакета crates.io rustls версии 0.23.25: Rustls: TLS 1.3 handshake messages incorrectly accepted across encryption level boundaries. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07528 — rustls 0.23.25 затронут GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.23.25`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.0 (`CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:H/I:N/A:N`)

OSV.dev сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346) для пакета crates.io rustls версии 0.23.25: Rustls: Session Debug formatting exposes TLS master secrets and resumption PSKs. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07537 — rustls-webpki 0.103.3 затронут GHSA-pwjx-qhcg-rvj4 (CVE-2026-93602, RUSTSEC-2026-0049)

- Серьёзность: **Средняя** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.103.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 33.1 / 100
- CVSS v3.1: 4.4 (`CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:H/A:N`)

OSV.dev сообщает GHSA-pwjx-qhcg-rvj4 (CVE-2026-93602, RUSTSEC-2026-0049) для пакета crates.io rustls-webpki версии 0.103.3: webpki: CRLs not considered authoritative by Distribution Point due to faulty matching logic. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-pwjx-qhcg-rvj4
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-pwjx-qhcg-rvj4](https://osv.dev/vulnerability/GHSA-pwjx-qhcg-rvj4) · manifest · SHA-256 cfbfa2ab43dcd198e7076fcab3a8ad64c1c5d529fc6135a1b8e5d707cb9ac93d_

```
{"id": "GHSA-pwjx-qhcg-rvj4", "aliases": ["CVE-2026-93602", "RUSTSEC-2026-0049"], "modified": "2026-09-19T03:55:49.529651638Z", "summary": "webpki: CRLs not considered authoritative by Distribution Point due to faulty matching logic", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:H/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.103.10, 0.104.0-alpha.5).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07520 — rand 0.8.5 затронут GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rand@0.8.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
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

### QSI-2026-07521 — rand 0.9.2 затронут GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
- Затронутый актив: `dependency:crates.io/rand@0.9.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 39.2 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097) для пакета crates.io rand версии 0.9.2: Rand is unsound with a custom logger using rand::rng(). Проверенный код называет rand::rng: затронутый код может быть достижим.

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

### QSI-2026-07523 — rsa 0.9.6 затронут GHSA-9c48-w39g-hm26 (CVE-2026-21895)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rsa@0.9.6`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-9c48-w39g-hm26 (CVE-2026-21895) для пакета crates.io rsa версии 0.9.6: rsa crate has potential panic on a prime being equal to 1. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-9c48-w39g-hm26
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-9c48-w39g-hm26](https://osv.dev/vulnerability/GHSA-9c48-w39g-hm26) · manifest · SHA-256 3e86581a0f0d117fc19d0a64e364348f29c6c9ecc2309c5c504009aaf9076ec3_

```
{"id": "GHSA-9c48-w39g-hm26", "aliases": ["CVE-2026-21895"], "modified": "2026-09-10T03:50:32.802096391Z", "summary": "rsa crate has potential panic on a prime being equal to 1", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:L/SC:N/SI:N/SA:N/E:U"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.9.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07525 — rustls 0.21.12 затронут GHSA-h2v8-394m-p7vv

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.21.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-h2v8-394m-p7vv для пакета crates.io rustls версии 0.21.12: Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07526 — rustls 0.21.12 затронут GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.21.12`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349) для пакета crates.io rustls версии 0.21.12: rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07530 — rustls 0.23.25 затронут GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls@0.23.25`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N`)

OSV.dev сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349) для пакета crates.io rustls версии 0.23.25: rustls: An unauthenticated ServerHello poisons the per-name key-exchange record, so later ClientHellos carry only a classical X25519 share. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-07532 — rustls-webpki 0.101.7 затронут GHSA-965h-392x-2mh5 (CVE-2026-93600, RUSTSEC-2026-0098)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.101.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 2.2 (`CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-965h-392x-2mh5 (CVE-2026-93600, RUSTSEC-2026-0098) для пакета crates.io rustls-webpki версии 0.101.7: webpki: Name constraints for URI names were incorrectly accepted. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-965h-392x-2mh5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-965h-392x-2mh5](https://osv.dev/vulnerability/GHSA-965h-392x-2mh5) · manifest · SHA-256 7dfbf39859f726382fb5bacff8569cd96b6823e01f426668833099ff6d756657_

```
{"id": "GHSA-965h-392x-2mh5", "aliases": ["CVE-2026-93600", "RUSTSEC-2026-0098"], "modified": "2026-09-19T03:55:32.245575348Z", "summary": "webpki: Name constraints for URI names were incorrectly accepted", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.103.12, 0.104.0-alpha.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07533 — rustls-webpki 0.101.7 затронут GHSA-xgp8-3hg3-c2mh (CVE-2026-93601, RUSTSEC-2026-0099)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.101.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 2.2 (`CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-xgp8-3hg3-c2mh (CVE-2026-93601, RUSTSEC-2026-0099) для пакета crates.io rustls-webpki версии 0.101.7: webpki: Name constraints were accepted for certificates asserting a wildcard name. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xgp8-3hg3-c2mh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xgp8-3hg3-c2mh](https://osv.dev/vulnerability/GHSA-xgp8-3hg3-c2mh) · manifest · SHA-256 c068ea92e7b545b187eef89198d9b7ef2f675512c425f0664366565735f890b6_

```
{"id": "GHSA-xgp8-3hg3-c2mh", "aliases": ["CVE-2026-93601", "RUSTSEC-2026-0099"], "modified": "2026-09-19T03:55:49.146112754Z", "summary": "webpki: Name constraints were accepted for certificates asserting a wildcard name", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.103.12, 0.104.0-alpha.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07536 — rustls-webpki 0.103.3 затронут GHSA-965h-392x-2mh5 (CVE-2026-93600, RUSTSEC-2026-0098)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.103.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 2.2 (`CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-965h-392x-2mh5 (CVE-2026-93600, RUSTSEC-2026-0098) для пакета crates.io rustls-webpki версии 0.103.3: webpki: Name constraints for URI names were incorrectly accepted. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-965h-392x-2mh5
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-965h-392x-2mh5](https://osv.dev/vulnerability/GHSA-965h-392x-2mh5) · manifest · SHA-256 7dfbf39859f726382fb5bacff8569cd96b6823e01f426668833099ff6d756657_

```
{"id": "GHSA-965h-392x-2mh5", "aliases": ["CVE-2026-93600", "RUSTSEC-2026-0098"], "modified": "2026-09-19T03:55:32.245575348Z", "summary": "webpki: Name constraints for URI names were incorrectly accepted", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.103.12, 0.104.0-alpha.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07538 — rustls-webpki 0.103.3 затронут GHSA-xgp8-3hg3-c2mh (CVE-2026-93601, RUSTSEC-2026-0099)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.103.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 29.4 / 100
- CVSS v3.1: 2.2 (`CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N`)

OSV.dev сообщает GHSA-xgp8-3hg3-c2mh (CVE-2026-93601, RUSTSEC-2026-0099) для пакета crates.io rustls-webpki версии 0.103.3: webpki: Name constraints were accepted for certificates asserting a wildcard name. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-xgp8-3hg3-c2mh
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-xgp8-3hg3-c2mh](https://osv.dev/vulnerability/GHSA-xgp8-3hg3-c2mh) · manifest · SHA-256 c068ea92e7b545b187eef89198d9b7ef2f675512c425f0664366565735f890b6_

```
{"id": "GHSA-xgp8-3hg3-c2mh", "aliases": ["CVE-2026-93601", "RUSTSEC-2026-0099"], "modified": "2026-09-19T03:55:49.146112754Z", "summary": "webpki: Name constraints were accepted for certificates asserting a wildcard name", "severity": [{"type": "CVSS_V3", "score": "CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.103.12, 0.104.0-alpha.6).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07516 — keccak 0.1.4 затронут GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/keccak@0.1.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 25.0 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012) для пакета crates.io keccak версии 0.1.4: Unsoundness in opt-in ARMv8 assembly backend for `keccak`. Затронутый код находится за флагом Cargo `asm`, выключенным по умолчанию; ни один проверенный манифест его не включает — бюллетень не применим, если флаг не включает другая зависимость.

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

### QSI-2026-07529 — rustls 0.23.25 затронут GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustls@0.23.25`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 25.0 / 100
- CVSS v3.1: 3.7 (`CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:N/A:L`)

OSV.dev сообщает GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348) для пакета crates.io rustls версии 0.23.25: Rustls: Brotli certificate decompression can allocate an attacker-controlled amount of memory up to 1 GiB before authentication. Затронутый код находится за флагом Cargo `brotli`, выключенным по умолчанию; ни один проверенный манифест его не включает — бюллетень не применим, если флаг не включает другая зависимость.

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

### QSI-2026-07508 — anyhow 1.0.100 затронут RUSTSEC-2026-0190 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/anyhow@1.0.100`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0190 для пакета crates.io anyhow версии 1.0.100: Unsoundness in `Error::downcast_mut()`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (anyhow::Error::downcast_mut); anyhow приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07512 — crossbeam-epoch 0.9.18 затронут RUSTSEC-2026-0204 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crossbeam-epoch@0.9.18`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-07513 — crypto-bigint 0.5.5 затронут RUSTSEC-2026-0387 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/crypto-bigint@0.5.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
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

### QSI-2026-07514 — ctutils 0.4.2 затронут RUSTSEC-2026-0385 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/ctutils@0.4.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
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

### QSI-2026-07515 — event-listener 5.3.1 затронут RUSTSEC-2026-0221 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/event-listener@5.3.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0221 для пакета crates.io event-listener версии 5.3.1: `event-listener` allows `!Send` tags to cross thread boundaries via `StackSlot`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0221
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0221](https://osv.dev/vulnerability/RUSTSEC-2026-0221) · manifest · SHA-256 984b4e4e87b4e2cc5992a06daf6b6466ee08279d927a38dca105b75fa8546f7c_

```
{"id": "RUSTSEC-2026-0221", "aliases": [], "modified": "2026-07-31T12:15:04.629484145Z", "summary": "`event-listener` allows `!Send` tags to cross thread boundaries via `StackSlot`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (5.4.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07517 — memmap2 0.9.4 затронут RUSTSEC-2026-0186 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/memmap2@0.9.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0186 для пакета crates.io memmap2 версии 0.9.4: Unchecked pointer offset in crate `memmap2`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (memmap2::Mmap::advise_range, memmap2::Mmap::unchecked_advise_range, memmap2::MmapMut::advise_range, memmap2::MmapMut::flush_async_range, memmap2::MmapMut::flush_range, memmap2::MmapMut::unchecked_advise_range); memmap2 приходит через другие зависимости, которые могут их вызывать.

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

### QSI-2026-07534 — rustls-webpki 0.101.7 затронут RUSTSEC-2026-0382 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.101.7`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0382 (CVE-2026-111943) для пакета crates.io rustls-webpki версии 0.101.7: Certificate verification may accept distrusted intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0382
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0382](https://osv.dev/vulnerability/RUSTSEC-2026-0382) · manifest · SHA-256 4c972eb1d77abf0d1c39f2b402c5fea32a5dacf7dbbeac638e7549ce780805d1_

```
{"id": "RUSTSEC-2026-0382", "aliases": ["BIT-golang-2026-111943", "CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0381", "RUSTSEC-2026-0383"], "modified": "2026-10-29T10:55:54.096394276Z", "summary": "Certificate verification may accept distrusted intermediates", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.103.16, 0.104.0-alpha.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07539 — rustls-webpki 0.103.3 затронут RUSTSEC-2026-0382 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/rustls-webpki@0.103.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0382 (CVE-2026-111943) для пакета crates.io rustls-webpki версии 0.103.3: Certificate verification may accept distrusted intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0382
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0382](https://osv.dev/vulnerability/RUSTSEC-2026-0382) · manifest · SHA-256 4c972eb1d77abf0d1c39f2b402c5fea32a5dacf7dbbeac638e7549ce780805d1_

```
{"id": "RUSTSEC-2026-0382", "aliases": ["BIT-golang-2026-111943", "CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0381", "RUSTSEC-2026-0383"], "modified": "2026-10-29T10:55:54.096394276Z", "summary": "Certificate verification may accept distrusted intermediates", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.103.16, 0.104.0-alpha.8).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07542 — webpki-roots 0.25.4 затронут RUSTSEC-2026-0381 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/webpki-roots@0.25.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0381 (CVE-2026-111943) для пакета crates.io webpki-roots версии 0.25.4: Bundled root certificates allow trust in distrusted emSign intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0381
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0381](https://osv.dev/vulnerability/RUSTSEC-2026-0381) · manifest · SHA-256 34a59ae82e2e8e2cde2fe94cd0e4c1ee7c6bd3656c3229fa2fa49bb4c3c4a2a4_

```
{"id": "RUSTSEC-2026-0381", "aliases": ["BIT-golang-2026-111943", "CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0382", "RUSTSEC-2026-0383"], "modified": "2026-10-29T10:55:54.096394276Z", "summary": "Bundled root certificates allow trust in distrusted emSign intermediates", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.26.11, 1.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07543 — webpki-roots 1.0.3 затронут RUSTSEC-2026-0381 (CVE-2026-111943) (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/webpki-roots@1.0.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0381 (CVE-2026-111943) для пакета crates.io webpki-roots версии 1.0.3: Bundled root certificates allow trust in distrusted emSign intermediates. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0381
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0381](https://osv.dev/vulnerability/RUSTSEC-2026-0381) · manifest · SHA-256 34a59ae82e2e8e2cde2fe94cd0e4c1ee7c6bd3656c3229fa2fa49bb4c3c4a2a4_

```
{"id": "RUSTSEC-2026-0381", "aliases": ["BIT-golang-2026-111943", "CVE-2026-111943", "GO-2026-6809", "RUSTSEC-2026-0382", "RUSTSEC-2026-0383"], "modified": "2026-10-29T10:55:54.096394276Z", "summary": "Bundled root certificates allow trust in distrusted emSign intermediates", "severity": null, "declared_in_manifest": true}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (0.26.11, 1.0.10).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07544 — zstd-safe 7.1.0 затронут RUSTSEC-2026-0395 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0395 для пакета crates.io zstd-safe версии 7.1.0: Use-after-free with `CParameter::StableInBuffer`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::set_parameter); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0395
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0395](https://osv.dev/vulnerability/RUSTSEC-2026-0395) · manifest · SHA-256 cf314e3df3f714ad17083f648e4d6822839805759c13c152cf2b2edcfbba9cdb_

```
{"id": "RUSTSEC-2026-0395", "aliases": [], "modified": "2026-10-26T14:00:06.388344282Z", "summary": "Use-after-free with `CParameter::StableInBuffer`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07545 — zstd-safe 7.1.0 затронут RUSTSEC-2026-0397 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0397 для пакета crates.io zstd-safe версии 7.1.0: `OutBuffer::around_pos` exposes uninitialized memory. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::OutBuffer::around_pos); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0397
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0397](https://osv.dev/vulnerability/RUSTSEC-2026-0397) · manifest · SHA-256 e1cc2d6a8e69a560eb15d719dcb988b36e18b940b8913145ec52a73efd0b9fcc_

```
{"id": "RUSTSEC-2026-0397", "aliases": [], "modified": "2026-10-26T14:00:05.089587004Z", "summary": "`OutBuffer::around_pos` exposes uninitialized memory", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07546 — zstd-safe 7.1.0 затронут RUSTSEC-2026-0399 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0399 для пакета crates.io zstd-safe версии 7.1.0: Use-after-free through `init_using_cdict` and `init_using_ddict`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::init_using_cdict, zstd_safe::DCtx::init_using_ddict); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0399
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0399](https://osv.dev/vulnerability/RUSTSEC-2026-0399) · manifest · SHA-256 dde7c9d1fcd35a89a4e462b7b42373ae75187190ebfffa3876d9e2bba20e386a_

```
{"id": "RUSTSEC-2026-0399", "aliases": [], "modified": "2026-10-26T14:00:05.792431051Z", "summary": "Use-after-free through `init_using_cdict` and `init_using_ddict`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07547 — zstd-safe 7.1.0 затронут RUSTSEC-2026-0400 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0400 для пакета crates.io zstd-safe версии 7.1.0: Use-after-free of a dictionary after a one-shot call on a context with an open stream. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::DCtx::decompress, zstd_safe::DCtx::decompress_using_ddict, zstd_safe::DCtx::decompress_using_dict); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0400
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0400](https://osv.dev/vulnerability/RUSTSEC-2026-0400) · manifest · SHA-256 12a31cd97694259b60fd13de0204d4257a30facebdbf5eb19bc091d2b54c85f6_

```
{"id": "RUSTSEC-2026-0400", "aliases": [], "modified": "2026-10-26T14:00:05.692077560Z", "summary": "Use-after-free of a dictionary after a one-shot call on a context with an open stream", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07548 — zstd-safe 7.1.0 затронут RUSTSEC-2026-0401 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0401 для пакета crates.io zstd-safe версии 7.1.0: Out-of-bounds read in `train_from_buffer` when sample sizes overflow. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::train_from_buffer); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0401
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0401](https://osv.dev/vulnerability/RUSTSEC-2026-0401) · manifest · SHA-256 8f606743a027e187f8815975be52f1a4018a22a8d8cacc5d66407f974573c3a0_

```
{"id": "RUSTSEC-2026-0401", "aliases": [], "modified": "2026-10-26T14:00:04.231502512Z", "summary": "Out-of-bounds read in `train_from_buffer` when sample sizes overflow", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07549 — zstd-safe 7.1.0 затронут RUSTSEC-2026-0402 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0402 для пакета crates.io zstd-safe версии 7.1.0: Heap buffer overflow in `CCtx::try_clone` on a multithreaded context. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::try_clone); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0402
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0402](https://osv.dev/vulnerability/RUSTSEC-2026-0402) · manifest · SHA-256 1659ee65665b5ae755a87f2715370efa327fc3064514c61888dd4fa3a3f32642_

```
{"id": "RUSTSEC-2026-0402", "aliases": [], "modified": "2026-10-26T14:00:05.685817733Z", "summary": "Heap buffer overflow in `CCtx::try_clone` on a multithreaded context", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07550 — zstd-safe 7.1.0 затронут RUSTSEC-2026-0403 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0403 для пакета crates.io zstd-safe версии 7.1.0: Uninitialized memory exposed when streaming decompression of a legacy frame fails. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::DCtx::decompress_stream); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0403
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0403](https://osv.dev/vulnerability/RUSTSEC-2026-0403) · manifest · SHA-256 b1d1701270f636af5d21f2b55cbd122bcd0df90ce4dce6793aa9263b377caddb_

```
{"id": "RUSTSEC-2026-0403", "aliases": [], "modified": "2026-10-26T14:00:05.787441176Z", "summary": "Uninitialized memory exposed when streaming decompression of a legacy frame fails", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07551 — zstd-safe 7.1.0 затронут RUSTSEC-2026-0404 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0404 для пакета crates.io zstd-safe версии 7.1.0: Double free in `DCtx::try_clone`. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::DCtx::try_clone); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0404
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0404](https://osv.dev/vulnerability/RUSTSEC-2026-0404) · manifest · SHA-256 7c25f3932e55150f3788cd8fcee7738d3c905758f825a562b19f78d7e041b0b2_

```
{"id": "RUSTSEC-2026-0404", "aliases": [], "modified": "2026-10-26T14:00:05.092817237Z", "summary": "Double free in `DCtx::try_clone`", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07552 — zstd-safe 7.1.0 затронут RUSTSEC-2026-0406 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-safe@7.1.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0406 для пакета crates.io zstd-safe версии 7.1.0: Use-after-free when changing a multithreaded context with an unfinished frame. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Проверенный код не упоминает затронутые функции (zstd_safe::CCtx::disable_dictionary, zstd_safe::CCtx::init, zstd_safe::CCtx::load_dictionary, zstd_safe::CCtx::ref_cdict, zstd_safe::CCtx::ref_prefix, zstd_safe::CCtx::reset …); zstd-safe приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0406
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0406](https://osv.dev/vulnerability/RUSTSEC-2026-0406) · manifest · SHA-256 deca0b7103bdc0c3ed051bcdb0dbd3d63e215fecdbdba6a7f24f9fb8c2e93ecd_

```
{"id": "RUSTSEC-2026-0406", "aliases": [], "modified": "2026-10-26T14:00:05.095427051Z", "summary": "Use-after-free when changing a multithreaded context with an unfinished frame", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (8.2.0).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07553 — zstd-sys 2.0.10+zstd.1.5.6 затронут RUSTSEC-2026-0410 (без оценки серьёзности)

- Серьёзность: **Низкая** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/zstd-sys@2.0.10+zstd.1.5.6`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 20.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0410 для пакета crates.io zstd-sys версии 2.0.10+zstd.1.5.6: WebAssembly allocator shim corrupts memory on allocation failure. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена. Касается только целевых платформ wasm32.

**Возможные последствия.** Неизвестно без разбора: прочитайте бюллетень и проверьте, достижим ли затронутый код в вашей сборке.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2026-0410
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2026-0410](https://osv.dev/vulnerability/RUSTSEC-2026-0410) · manifest · SHA-256 1e892df4ce7c9911f01547e4a80d1fb3ea5a27b8c1c89c0514917e08bbf3bdc5_

```
{"id": "RUSTSEC-2026-0410", "aliases": [], "modified": "2026-10-26T14:00:05.788985783Z", "summary": "WebAssembly allocator shim corrupts memory on allocation failure", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. У бюллетеня нет оценки серьёзности. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Разберите бюллетень; если он применим, обновите до исправленной версии (2.1.2).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-07541 — tokio 1.50.0 затронут RUSTSEC-2026-0386 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependency:crates.io/tokio@1.50.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 17.8 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0386 для пакета crates.io tokio версии 1.50.0: `AsyncFd::new` and related constructors violate I/O safety. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Ни одна из затронутых функций (tokio::io::unix::AsyncFd::new, tokio::io::unix::AsyncFd::try_new, tokio::io::unix::AsyncFd::try_with_interest, tokio::io::unix::AsyncFd::with_interest) не упоминается в проверенном коде: бюллетень не применим, если они не вызываются косвенно (через трейты, макросы, другие зависимости).

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

### QSI-2026-07554 — 3 бюллетеней в 2 пакет(ах) crates.io, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:crates.io:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
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

### QSI-2026-07506 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 13.3 / 100
- CVSS v3.1: неприменимо

В 21 манифестах зависимостей QSI нашёл криптобиблиотеки (bellman, bls12_381, curve25519-dalek, ecdsa, ed25519-dalek, ff, group, halo2_gadgets, halo2_poseidon, halo2_proofs, jubjub, orchard, p256, p384, pasta_curves), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · Cargo.lock, Cargo.toml, components/eip681/Cargo.toml, components/equihash/Cargo.toml, components/f4jumble/Cargo.toml, components/payment_uri/Cargo.toml, components/zcash_address/Cargo.toml, components/zcash_encoding/Cargo.toml, components/zcash_protocol/Cargo.toml, components/zip321/Cargo.toml, pczt/Cargo.toml, zcash/Cargo.toml, zcash_client_backend/Cargo.toml, zcash_client_sqlite/Cargo.toml, zcash_history/Cargo.toml, zcash_keys/Cargo.toml, zcash_pool_migration/Cargo.toml, zcash_pool_migration_m · SHA-256 b99b5a2af900f746fc90533a5caa90485cae862c4d2caeaa8cb33155ed4c18fa_

```
Crypto libraries: bellman, bls12_381, curve25519-dalek, ecdsa, ed25519-dalek, ff, group, halo2_gadgets, halo2_poseidon, halo2_proofs, jubjub, orchard, p256, p384, pasta_curves, reddsa, redjubjub, ring, rsa, rustls, sapling-crypto, secp256k1, sinsemilla, x25519-dalek, zcash_client_backend, zcash_keys, zcash_note_encryption, zcash_primitives, zcash_proofs, zcash_protocol, zcash_spec, zip32
```

**Ограничения проверки.** Отсутствие доказательств не является доказательством отсутствия: системные библиотеки и транзитивные зависимости могут не указываться.

**Рекомендация.** Определите источник поддержки PQC (TLS-терминатор, KMS/HSM, обновление библиотек).

**Повторная проверка.** Повторите сканирование после обновлений.

### QSI-2026-07507 — adler 1.0.2: информационный бюллетень RUSTSEC-2025-0056 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/adler@1.0.2`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
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

### QSI-2026-07509 — bincode 2.0.1: информационный бюллетень RUSTSEC-2025-0141 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/bincode@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2025-0141 для пакета crates.io bincode версии 2.0.1 как информационный (unmaintained): Bincode is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2025-0141
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2025-0141](https://osv.dev/vulnerability/RUSTSEC-2025-0141) · manifest · SHA-256 532525d6fd3f2cb4701cae8133e80ff6557554f82b919c38fb8a089b03cf57f5_

```
{"id": "RUSTSEC-2025-0141", "aliases": [], "modified": "2026-01-16T11:07:28.867553Z", "summary": "Bincode is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-07518 — paste 1.0.15: информационный бюллетень RUSTSEC-2024-0436 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/paste@1.0.15`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
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

### QSI-2026-07519 — proc-macro-error2 2.0.1: информационный бюллетень RUSTSEC-2026-0173 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
- Затронутый актив: `dependency:crates.io/proc-macro-error2@2.0.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-30 00:13 UTC
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
| **пороговая подпись и протоколы MPC** | Pedersen commitment (4) | QSI-2026-07503 | Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли |
| **подпись транзакций и сообщений** | ECDSA (15), BLS12-381 (4) | QSI-2026-07504, QSI-2026-07505 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм в конечных полях | взламывает | Q1 | BLS12-381 (4) | Взламывает Диффи–Хеллмана в конечных полях и DSA при любом размере. Переводите установление ключей на ML-KEM (на переходный период — гибрид с X25519 или ECDH), подписи — на ML-DSA или SLH-DSA. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | BLS12-381 (4), ECDSA (15), Pedersen commitment (4) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | BLAKE2 (2), Keccak-256 (1), RIPEMD-160 (2), SHA-2 (4) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | BLAKE2 (2), Keccak-256 (1), RIPEMD-160 (2), SHA-2 (4) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-07531 | Обновите rustls-webpki до исправленной версии (0.103.13, 0.104.0-alpha.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104). |
| P2 | QSI-2026-07535 | Обновите rustls-webpki до исправленной версии (0.103.13, 0.104.0-alpha.7). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-82j2-j2ch-gfr8 (CVE-2026-93599, RUSTSEC-2026-0104). |
| P2 | QSI-2026-07540 | Обновите serde_with до исправленной версии (3.21.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7gcf-g7xr-8hxj. |
| P2 | QSI-2026-07510 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-07511 | Обновите bytes до исправленной версии (1.11.1). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-434x-w66g-qw3r (CVE-2026-25541, RUSTSEC-2026-0007). |
| P2 | QSI-2026-07522 | Обновите rsa до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-4grx-2x9w-596c (CVE-2023-49092, GHSA-c38w-74pg-36hr, RUSTSEC-2023-0071). |
| P2 | QSI-2026-07524 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346). |
| P2 | QSI-2026-07527 | Обновите rustls до исправленной версии (0.23.45). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-2mjx-qc3c-rqvc (RUSTSEC-2026-0285). |
| P2 | QSI-2026-07528 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-c8m5-c952-6cm4 (RUSTSEC-2026-0346). |
| P2 | QSI-2026-07537 | Обновите rustls-webpki до исправленной версии (0.103.10, 0.104.0-alpha.5). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-pwjx-qhcg-rvj4 (CVE-2026-93602, RUSTSEC-2026-0049). |
| P2 | QSI-2026-07520 | Обновите rand до исправленной версии (0.10.1, 0.8.6, 0.9.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097). |
| P2 | QSI-2026-07521 | Обновите rand до исправленной версии (0.10.1, 0.8.6, 0.9.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097). |
| P2 | QSI-2026-07523 | Обновите rsa до исправленной версии (0.9.10). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-9c48-w39g-hm26 (CVE-2026-21895). |
| P2 | QSI-2026-07525 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h2v8-394m-p7vv. |
| P2 | QSI-2026-07526 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349). |
| P2 | QSI-2026-07530 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-w44r-93j7-qv28 (RUSTSEC-2026-0349). |
| P2 | QSI-2026-07532 | Обновите rustls-webpki до исправленной версии (0.103.12, 0.104.0-alpha.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-965h-392x-2mh5 (CVE-2026-93600, RUSTSEC-2026-0098). |
| P2 | QSI-2026-07533 | Обновите rustls-webpki до исправленной версии (0.103.12, 0.104.0-alpha.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xgp8-3hg3-c2mh (CVE-2026-93601, RUSTSEC-2026-0099). |
| P2 | QSI-2026-07536 | Обновите rustls-webpki до исправленной версии (0.103.12, 0.104.0-alpha.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-965h-392x-2mh5 (CVE-2026-93600, RUSTSEC-2026-0098). |
| P2 | QSI-2026-07538 | Обновите rustls-webpki до исправленной версии (0.103.12, 0.104.0-alpha.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-xgp8-3hg3-c2mh (CVE-2026-93601, RUSTSEC-2026-0099). |
| P2 | QSI-2026-07516 | Обновите keccak до исправленной версии (0.1.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012). |
| P2 | QSI-2026-07529 | Обновите rustls до исправленной версии (0.23.46, 0.24.0-dev.2). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-h2v8-394m-p7vv (RUSTSEC-2026-0348). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-07508 | Разберите RUSTSEC-2026-0190; при необходимости обновите anyhow до исправленной версии (1.0.103). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0190 или результат разбора записан. |
| P3 | QSI-2026-07512 | Разберите RUSTSEC-2026-0204; при необходимости обновите crossbeam-epoch до исправленной версии (0.9.20). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0204 или результат разбора записан. |
| P3 | QSI-2026-07513 | Разберите RUSTSEC-2026-0387; при необходимости обновите crypto-bigint до исправленной версии (0.7.6). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0387 или результат разбора записан. |
| P3 | QSI-2026-07514 | Разберите RUSTSEC-2026-0385; при необходимости обновите ctutils до исправленной версии (0.4.4). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0385 или результат разбора записан. |
| P3 | QSI-2026-07515 | Разберите RUSTSEC-2026-0221; при необходимости обновите event-listener до исправленной версии (5.4.2). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0221 или результат разбора записан. |
| P3 | QSI-2026-07517 | Разберите RUSTSEC-2026-0186; при необходимости обновите memmap2 до исправленной версии (0.9.11). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0186 или результат разбора записан. |
| P3 | QSI-2026-07534 | Разберите RUSTSEC-2026-0382 (CVE-2026-111943); при необходимости обновите rustls-webpki до исправленной версии (0.103.16, 0.104.0-alpha.8). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0382 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-07539 | Разберите RUSTSEC-2026-0382 (CVE-2026-111943); при необходимости обновите rustls-webpki до исправленной версии (0.103.16, 0.104.0-alpha.8). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0382 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-07542 | Разберите RUSTSEC-2026-0381 (CVE-2026-111943); при необходимости обновите webpki-roots до исправленной версии (0.26.11, 1.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0381 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-07543 | Разберите RUSTSEC-2026-0381 (CVE-2026-111943); при необходимости обновите webpki-roots до исправленной версии (0.26.11, 1.0.10). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0381 (CVE-2026-111943) или результат разбора записан. |
| P3 | QSI-2026-07544 | Разберите RUSTSEC-2026-0395; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0395 или результат разбора записан. |
| P3 | QSI-2026-07545 | Разберите RUSTSEC-2026-0397; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0397 или результат разбора записан. |
| P3 | QSI-2026-07546 | Разберите RUSTSEC-2026-0399; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0399 или результат разбора записан. |
| P3 | QSI-2026-07547 | Разберите RUSTSEC-2026-0400; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0400 или результат разбора записан. |
| P3 | QSI-2026-07548 | Разберите RUSTSEC-2026-0401; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0401 или результат разбора записан. |
| P3 | QSI-2026-07549 | Разберите RUSTSEC-2026-0402; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0402 или результат разбора записан. |
| P3 | QSI-2026-07550 | Разберите RUSTSEC-2026-0403; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0403 или результат разбора записан. |
| P3 | QSI-2026-07551 | Разберите RUSTSEC-2026-0404; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0404 или результат разбора записан. |
| P3 | QSI-2026-07552 | Разберите RUSTSEC-2026-0406; при необходимости обновите zstd-safe до исправленной версии (8.2.0). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0406 или результат разбора записан. |
| P3 | QSI-2026-07553 | Разберите RUSTSEC-2026-0410; при необходимости обновите zstd-sys до исправленной версии (2.1.2). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0410 или результат разбора записан. |
| P3 | QSI-2026-07541 | Разберите RUSTSEC-2026-0386; при необходимости обновите tokio до исправленной версии (1.51.6, 1.53.3). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0386 или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-07503 | Внесите использования Pedersen commitment в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07504 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-07505 | Внесите использования BLS12-381 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-07503 | Запланируйте миграцию Pedersen commitment на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07504 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-07505 | Запланируйте миграцию BLS12-381 на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-07554 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |
| P4 | QSI-2026-07507 | Замените adler поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | adler заменён или решение зафиксировано. |
| P4 | QSI-2026-07509 | Замените bincode поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | bincode заменён или решение зафиксировано. |
| P4 | QSI-2026-07518 | Замените paste поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | paste заменён или решение зафиксировано. |
| P4 | QSI-2026-07519 | Замените proc-macro-error2 поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | proc-macro-error2 заменён или решение зафиксировано. |

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
21. OSV advisory GHSA-2mjx-qc3c-rqvc — OSV.dev. <https://osv.dev/vulnerability/GHSA-2mjx-qc3c-rqvc> (modified 2026-10-27T15:30:05.509305490Z)
22. OSV advisory GHSA-3288-p39f-rqpv — OSV.dev. <https://osv.dev/vulnerability/GHSA-3288-p39f-rqpv> (modified 2026-09-10T03:50:59.332505686Z)
23. OSV advisory GHSA-434x-w66g-qw3r — OSV.dev. <https://osv.dev/vulnerability/GHSA-434x-w66g-qw3r> (modified 2026-09-10T03:50:33.995841351Z)
24. OSV advisory GHSA-4grx-2x9w-596c — OSV.dev. <https://osv.dev/vulnerability/GHSA-4grx-2x9w-596c> (modified 2026-09-10T03:50:04.002228238Z)
25. OSV advisory GHSA-7gcf-g7xr-8hxj — OSV.dev. <https://osv.dev/vulnerability/GHSA-7gcf-g7xr-8hxj> (modified 2026-09-10T03:51:10.897685062Z)
26. OSV advisory GHSA-82j2-j2ch-gfr8 — OSV.dev. <https://osv.dev/vulnerability/GHSA-82j2-j2ch-gfr8> (modified 2026-09-19T03:55:33.412079637Z)
27. OSV advisory GHSA-965h-392x-2mh5 — OSV.dev. <https://osv.dev/vulnerability/GHSA-965h-392x-2mh5> (modified 2026-09-19T03:55:32.245575348Z)
28. OSV advisory GHSA-9c48-w39g-hm26 — OSV.dev. <https://osv.dev/vulnerability/GHSA-9c48-w39g-hm26> (modified 2026-09-10T03:50:32.802096391Z)
29. OSV advisory GHSA-c8m5-c952-6cm4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-c8m5-c952-6cm4> (modified 2026-10-27T16:15:05.354395696Z)
30. OSV advisory GHSA-cq8v-f236-94qc — OSV.dev. <https://osv.dev/vulnerability/GHSA-cq8v-f236-94qc> (modified 2026-09-10T03:50:43.958966498Z)
31. OSV advisory GHSA-h2v8-394m-p7vv — OSV.dev. <https://osv.dev/vulnerability/GHSA-h2v8-394m-p7vv> (modified 2026-10-27T16:15:05.337819489Z)
32. OSV advisory GHSA-pwjx-qhcg-rvj4 — OSV.dev. <https://osv.dev/vulnerability/GHSA-pwjx-qhcg-rvj4> (modified 2026-09-19T03:55:49.529651638Z)
33. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-08-19T19:30:06.686866977Z)
34. OSV advisory GHSA-w44r-93j7-qv28 — OSV.dev. <https://osv.dev/vulnerability/GHSA-w44r-93j7-qv28> (modified 2026-10-27T16:15:05.340347056Z)
35. OSV advisory GHSA-xgp8-3hg3-c2mh — OSV.dev. <https://osv.dev/vulnerability/GHSA-xgp8-3hg3-c2mh> (modified 2026-09-19T03:55:49.146112754Z)
36. OSV advisory RUSTSEC-2024-0436 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0436> (modified 2026-01-27T22:03:15.694766Z)
37. OSV advisory RUSTSEC-2025-0056 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0056> (modified 2025-09-05T09:05:48Z)
38. OSV advisory RUSTSEC-2025-0141 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0141> (modified 2026-01-16T11:07:28.867553Z)
39. OSV advisory RUSTSEC-2026-0173 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0173> (modified 2026-06-07T21:00:04.318567692Z)
40. OSV advisory RUSTSEC-2026-0186 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0186> (modified 2026-06-22T18:15:03.600280397Z)
41. OSV advisory RUSTSEC-2026-0190 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0190> (modified 2026-06-29T14:15:03.650725453Z)
42. OSV advisory RUSTSEC-2026-0204 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0204> (modified 2026-07-06T22:30:04.159269138Z)
43. OSV advisory RUSTSEC-2026-0221 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0221> (modified 2026-07-31T12:15:04.629484145Z)
44. OSV advisory RUSTSEC-2026-0381 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0381> (modified 2026-10-29T10:55:54.096394276Z)
45. OSV advisory RUSTSEC-2026-0382 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0382> (modified 2026-10-29T10:55:54.096394276Z)
46. OSV advisory RUSTSEC-2026-0385 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0385> (modified 2026-10-23T08:30:02.389575143Z)
47. OSV advisory RUSTSEC-2026-0386 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0386> (modified 2026-10-23T14:45:03.847864944Z)
48. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
49. OSV advisory RUSTSEC-2026-0395 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0395> (modified 2026-10-26T14:00:06.388344282Z)
50. OSV advisory RUSTSEC-2026-0397 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0397> (modified 2026-10-26T14:00:05.089587004Z)
51. OSV advisory RUSTSEC-2026-0399 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0399> (modified 2026-10-26T14:00:05.792431051Z)
52. OSV advisory RUSTSEC-2026-0400 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0400> (modified 2026-10-26T14:00:05.692077560Z)
53. OSV advisory RUSTSEC-2026-0401 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0401> (modified 2026-10-26T14:00:04.231502512Z)
54. OSV advisory RUSTSEC-2026-0402 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0402> (modified 2026-10-26T14:00:05.685817733Z)
55. OSV advisory RUSTSEC-2026-0403 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0403> (modified 2026-10-26T14:00:05.787441176Z)
56. OSV advisory RUSTSEC-2026-0404 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0404> (modified 2026-10-26T14:00:05.092817237Z)
57. OSV advisory RUSTSEC-2026-0406 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0406> (modified 2026-10-26T14:00:05.095427051Z)
58. OSV advisory RUSTSEC-2026-0410 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0410> (modified 2026-10-26T14:00:05.788985783Z)
59. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
60. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
61. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
62. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| RIPEMD-160 | RIPEMD-160 |  | слаб классически | устаревающий | 2 | 2 | zcash_transparent/src/pczt/updater.rs:3; zcash_transparent/src/util/hash160.rs:4 |
| BLAKE2 |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 2 | 2 | components/equihash/src/blake2b.rs; components/equihash/tromp/blake2b.h |
| Keccak-256 | Keccak-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 1 | 1 | components/eip681/src/parse.rs:15 |
| SHA-2 | SHA-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 4 | 4 | zcash_primitives/src/block.rs:124; zcash_transparent/src/pczt/updater.rs:98; zcash_transparent/src/util/hash160.rs:29 |
| Crypto library | 0.11.1 | jubjub (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.0 | p384 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.0 | ff (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.0 | group (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | ff (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.14.0 | group (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.15.0 | bellman (bellman) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.16.0 | orchard (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.16.9 | ecdsa (python-ecdsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.17.14 | ring (ring (Rust)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.2.0 | halo2_poseidon (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.2.0 | sinsemilla (sinsemilla) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.2.1 | zcash_spec (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.21.12 | rustls (rustls) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.23.25 | rustls (rustls) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.3.0 | zip32 (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.33.1 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.4.0 | halo2_proofs (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.5.1 | zcash_note_encryption (Zcash protocol crates) | н/п | допустимо | 2 | 2 | Cargo.lock; Cargo.toml |
| Crypto library | 0.6.0 | halo2_gadgets (halo2 (Zcash)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.6.0 | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.6.1 | reddsa (reddsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.9.0 | bls12_381 (jubjub) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.9.0 | redjubjub (reddsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.9.0 | sapling-crypto (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.9.6 | rsa (RustCrypto rsa) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 2.0.1 | x25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 2.2.0 | ed25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 4.1.3 | curve25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | Cargo.lock |
| Crypto library | 0.11 | jubjub (jubjub) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.14 | group (jubjub) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.14 | ff (jubjub) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.15 | bellman (bellman) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.16 | orchard (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.2 | zcash_spec (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.3 | zip32 (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.33 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.6 | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.9 | sapling-crypto (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.9 | bls12_381 (jubjub) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | 0.9 | redjubjub (reddsa) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | =0.11.0-pre.1 | zcash_protocol (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | =0.17.0-pre.2 | zcash_keys (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | =0.25.0-pre.2 | zcash_client_backend (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | =0.31.0-pre.2 | zcash_primitives (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | =0.31.0-pre.2 | zcash_proofs (Zcash protocol crates) | н/п | допустимо | 1 | 1 | Cargo.toml |
| Crypto library | workspace | zcash_protocol (Zcash protocol crates) | н/п | допустимо | 10 | 10 | components/zcash_address/Cargo.toml; components/zip321/Cargo.toml; pczt/Cargo.toml |
| Crypto library | workspace | pasta_curves (pasta_curves (Pallas/Vesta)) | н/п | допустимо | 3 | 3 | pczt/Cargo.toml; zcash_client_backend/Cargo.toml; zcash_client_sqlite/Cargo.toml |
| Crypto library | workspace | zip32 (Zcash protocol crates) | н/п | допустимо | 8 | 8 | pczt/Cargo.toml; zcash_client_backend/Cargo.toml; zcash_client_sqlite/Cargo.toml |
| Crypto library | workspace | zcash_note_encryption (Zcash protocol crates) | н/п | допустимо | 4 | 4 | pczt/Cargo.toml; zcash_client_backend/Cargo.toml; zcash_client_sqlite/Cargo.toml |
| Crypto library | workspace | zcash_proofs (Zcash protocol crates) | н/п | допустимо | 3 | 3 | pczt/Cargo.toml; zcash_client_backend/Cargo.toml; zcash_client_sqlite/Cargo.toml |
| Crypto library | workspace | zcash_primitives (Zcash protocol crates) | н/п | допустимо | 6 | 6 | pczt/Cargo.toml; zcash/Cargo.toml; zcash_client_backend/Cargo.toml |
| Crypto library | workspace | jubjub (jubjub) | н/п | допустимо | 6 | 6 | pczt/Cargo.toml; zcash_client_backend/Cargo.toml; zcash_client_sqlite/Cargo.toml |
| Crypto library | workspace | orchard (Zcash protocol crates) | н/п | допустимо | 7 | 7 | pczt/Cargo.toml; zcash_client_backend/Cargo.toml; zcash_client_sqlite/Cargo.toml |
| Crypto library | workspace | ff (jubjub) | н/п | допустимо | 2 | 2 | pczt/Cargo.toml; zcash_primitives/Cargo.toml |
| Crypto library | workspace | bls12_381 (jubjub) | н/п | допустимо | 6 | 6 | pczt/Cargo.toml; zcash_client_backend/Cargo.toml; zcash_client_sqlite/Cargo.toml |
| Crypto library | workspace | redjubjub (reddsa) | н/п | допустимо | 4 | 4 | pczt/Cargo.toml; zcash_client_backend/Cargo.toml; zcash_primitives/Cargo.toml |
| Crypto library | workspace | secp256k1 (secp256k1 bindings) | н/п | допустимо | 6 | 6 | pczt/Cargo.toml; zcash_client_backend/Cargo.toml; zcash_client_sqlite/Cargo.toml |
| Crypto library | workspace | zcash_keys (Zcash protocol crates) | н/п | допустимо | 3 | 3 | zcash_client_backend/Cargo.toml; zcash_client_sqlite/Cargo.toml; zcash_pool_migration/Cargo.toml |
| Crypto library | workspace | group (jubjub) | н/п | допустимо | 4 | 4 | zcash_client_backend/Cargo.toml; zcash_client_sqlite/Cargo.toml; zcash_keys/Cargo.toml |
| Crypto library | workspace | zcash_client_backend (Zcash protocol crates) | н/п | допустимо | 2 | 2 | zcash_client_sqlite/Cargo.toml; zcash_pool_migration/Cargo.toml |
| Crypto library | workspace | bellman (bellman) | н/п | допустимо | 1 | 1 | zcash_proofs/Cargo.toml |
| Crypto library | workspace | zcash_spec (Zcash protocol crates) | н/п | допустимо | 1 | 1 | zcash_transparent/Cargo.toml |
| BLS12-381 |  |  | уязвим (Шор) | допустимо | 4 | 4 | zcash_proofs/src/circuit/sprout/mod.rs:340; zcash_proofs/src/lib.rs:15; zcash_proofs/src/prover.rs:3 |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 15 | 15 | pczt/src/roles/signer/mod.rs:278; zcash_client_backend/src/data_api.rs:3935; zcash_client_backend/src/data_api/wallet.rs:1380 |
| Pedersen commitment |  |  | уязвим (Шор) | допустимо | 4 | 4 | pczt/src/orchard.rs:23; zcash_primitives/src/transaction/components/orchard.rs:17; zcash_primitives/src/transaction/components/sapling.rs:14 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| .cargo/config.toml | 27 | `c50d9a3b08fa6bb6b71d5d4f7af76b8a61fbd04efd207e60ee78b44007895803` | 0 |
| .github/helpers/check-dep-graph.py | 3784 | `b286aec9a590ce0319f4aee11cc48cbce887f92febf41741cdf90d0fa299786f` | 0 |
| .github/helpers/check-release-tags.py | 6021 | `1b89b7b1cb9e41b0e8d4b3d5979ca69ef31270418b39ee03aea1bc8aaa797663` | 0 |
| Cargo.lock | 187600 | `f218ea41f705a0d7db4156816fd1c6ecd95828064cc198cd489ae1b3882273a1` | 0 |
| Cargo.toml | 8344 | `2e9608a94f0314790472b62a27eaee56af1c42aa85eb1d386be211eee6bd4f71` | 0 |
| components/eip681/Cargo.toml | 999 | `1b6ffda755504c497286d2e03243e7e3daa49e71ac6266c6e4949198d5b22f0e` | 0 |
| components/eip681/src/error.rs | 9320 | `2737ae8953a208f2dfb3dfaa0f76748e3a43f116f6b974191e38e86f80a678af` | 0 |
| components/eip681/src/lib.rs | 2572 | `7980128f201cc345395dcb045518c797bf19941f57dd6975ca9212027df44e3b` | 0 |
| components/eip681/src/parse.rs | 76946 | `fee3ec17332402f6c9fe96c9b68b3008215a027a8efd85f7d13b568712c29cc3` | 0 |
| components/eip681/src/request.rs | 29780 | `12837d313debdad012e56a171c9bd8c75f5a667fe54ab4d987ef47b6b0f60f93` | 3 |
| components/equihash/Cargo.toml | 952 | `34a0876441a88a58f9fb7fb11b1b83aa10c2889f0c8c5abc0a0adeb16f5e6296` | 0 |
| components/equihash/build.rs | 433 | `2716a2cf3d85f116d8873b231b3fc19c3f9cc8aad95063592041767aab1a6752` | 0 |
| components/equihash/src/blake2b.rs | 1858 | `f7bf12ab1ddfc2693c6e7594cf00f77581a278b178ba9d8a144715faa38434c0` | 0 |
| components/equihash/src/lib.rs | 1619 | `4ec356326258ec10ed628cb4f481c2a8efbe79c374b8ec094ac0b6f98fcf8fe5` | 0 |
| components/equihash/src/minimal.rs | 9536 | `74bec30cd45cb772422bd76e4144774a880792e7ef6d59bc4e12b86e40d846f9` | 0 |
| components/equihash/src/params.rs | 1302 | `c77e235d106c1ad0b5a130ba3f9c54bed8b99d061f7dcaab4b1e9424ec03bed6` | 0 |
| components/equihash/src/tromp.rs | 9202 | `f5843bdfd4f3a6eac065554f694763467909068564f259b1ccb226fd3c1ccb5b` | 0 |
| components/equihash/src/verify.rs | 9595 | `1d2398f57391481d9f10030aadcbbc7a3230e0b0cbaabfcfd9793faa71ce097d` | 0 |
| components/equihash/tromp/blake2b.h | 1676 | `1006c3a6361483718cc7ba404b9078f233ea59a04887330902076c3ed1bf0855` | 0 |
| components/equihash/tromp/equi.h | 1100 | `94f0820ac42fe5ecfeaee857649afecf43d465068461bd4efb699050ed1c835e` | 0 |
| components/equihash/tromp/equi_miner.c | 22553 | `212d91f704d56a7faf071d41ffe88b0c98ea10ef0ccd1fe0f806fd88bc5fb2af` | 0 |
| components/equihash/tromp/portable_endian.h | 3176 | `e60f79c27af38844051bd9a62dcf2bca6a9131ee005959bf5919bb1fca2f4b02` | 0 |
| components/f4jumble/Cargo.toml | 876 | `54ced6c2c71f577c9d6bebca57ee26dece422b937e2c0e659d38b37c31cfda90` | 0 |
| components/f4jumble/src/lib.rs | 13874 | `c860d1b3b199cf5b5dc57eb63eca5c500a0d11a917d80a618477e0fba90d9d55` | 0 |
| components/payment_uri/Cargo.toml | 764 | `dafd5537e16bbad92e64108de3479cef376374319e215796a30cc5bd1889ce44` | 0 |
| components/payment_uri/src/bitcoin.rs | 8825 | `27c03e6863c0b591ed0f675e8c251ab7d1503dc2d2190e6389bb1ec950d7a2b0` | 0 |
| components/payment_uri/src/lib.rs | 15178 | `4d9b7fff3027fe4d40904b6df7cde56aa492920258658c7022324b618ba4a1c0` | 0 |
| components/payment_uri/src/solana.rs | 7304 | `11c3159e45160c5f8090f988adac744e8827e304898f696eb1b769fb692b8de4` | 0 |
| components/zcash_address/Cargo.toml | 1089 | `9db2888c15565750230a1798ecdd40666d511f27e82a40927e8161ee18534448` | 0 |
| components/zcash_address/src/constants.rs | 15691 | `542102eb1f87bc3746fdfc1f5d85fc3f26dafcec4ef32ec00e76655a9c3e09fe` | 0 |
| components/zcash_address/src/convert.rs | 12197 | `460a92b779817ceb1e51b8b4acbfcdc9e1d807f60a9284c5c042f8620827a14b` | 0 |
| components/zcash_address/src/encoding.rs | 14821 | `d2df7640e37fd24677ff5ab31245507380f1ce876a71f00f927b6afe03c644ad` | 0 |
| components/zcash_address/src/kind.rs | 17 | `1e1cac26248df3cbe9959d287d59160893b5b7ae273e76d9e344d2947b0d1417` | 0 |
| components/zcash_address/src/kind/unified.rs | 48512 | `edfa017f1b7534670be00d0f76bfc44666399678f000b62985c35938433491bc` | 0 |
| components/zcash_address/src/kind/unified/address.rs | 35355 | `8e22fd18ac1afd1a2688b2a6cb0bb36f74385d3226dff5d92d046b7ca8e08645` | 0 |
| components/zcash_address/src/kind/unified/fvk.rs | 28030 | `cc3974080fe53b2974f98354902d11804d2f621395a1a0154546e47f41187365` | 0 |
| components/zcash_address/src/kind/unified/ivk.rs | 23102 | `29d5c6ddfb5f57caa3e4659b02d0c1776c1f02851f9b291b970b9cfb94207012` | 0 |
| components/zcash_address/src/kind/unified/revision.rs | 2363 | `15376624d2ee7decca87551d9f7e467b1e36ed5b15afa9311efea146fe9abdfb` | 0 |
| components/zcash_address/src/lib.rs | 16793 | `a8ab232c059b661a295b258a132d9788952cf1806d83f75ff3bbef96031bc1b8` | 0 |
| components/zcash_encoding/Cargo.toml | 896 | `59fad1e11bce86da49aa97cc8b3ea7930f9cfe666d277deb7ae61051cd0a15cd` | 0 |
| components/zcash_encoding/src/lib.rs | 19244 | `79cd47d3d73370fff5745c3e2efaeebc0104c0ec96aaf20cb085670829459d31` | 0 |
| components/zcash_protocol/Cargo.toml | 1605 | `fd684937f5ed041aea5c6b4e5f0562860a28b0a3598dcc713006adaba17dafce` | 0 |
| components/zcash_protocol/src/consensus.rs | 48506 | `004f0da79523cbe407a477cb7cc3abf0735f72946defd61176ef1dde6fd7aeaf` | 0 |
| components/zcash_protocol/src/constants.rs | 2645 | `92bf49080134e943f100280f4046684734be9b652f1fc4f1a7fa4c7a1862b785` | 0 |
| components/zcash_protocol/src/constants/mainnet.rs | 4714 | `bc5ec2e50adf3945f3d2a846d4b9922cd53de08ec5a9d7a1d2764624dbe044e8` | 0 |
| components/zcash_protocol/src/constants/regtest.rs | 5099 | `db11b07c4b20e28901fe7018ad513d24a645c271c4d441e8d9c21b373ad3e5c0` | 0 |
| components/zcash_protocol/src/constants/testnet.rs | 4774 | `a4a154d59cab94159754c42305419af94edbffc10b2fa2212b21806b675e4dbf` | 0 |
| components/zcash_protocol/src/lib.rs | 2867 | `9def3b5138d0eae8153fc730cb4f033b75b8a8db00313062d7cf470b03d5ba23` | 0 |
| components/zcash_protocol/src/local_consensus.rs | 10334 | `05bb22840ac92f141fb5c8cfba7a77c0c53116a6f767ebb77f9a358475092ff8` | 0 |
| components/zcash_protocol/src/memo.rs | 18347 | `24a4f6444e20add60ec0b558a52125b38f161c394e64b6b07f44757426af076d` | 0 |
| components/zcash_protocol/src/txid.rs | 4047 | `7d19917afcf7b8f98fee478e50411673aed1d03883a0691800420bf783ffe02b` | 0 |
| components/zcash_protocol/src/value.rs | 19311 | `f44c8a8740df244cbd3f01ace6d8343382fa414d22a2b7269feb4fe264b6eccc` | 0 |
| components/zcash_protocol/src/zip318.rs | 69613 | `635e281901e1814b8b17ceaa1ef0e20650b2824549205157537f4e7040a2a184` | 0 |
| components/zip321/Cargo.toml | 1121 | `94b27b0f4640c9c671af2254381665e755418946238218bec039b8699c406ab7` | 0 |
| components/zip321/src/lib.rs | 51154 | `ed6f284170ad237f71b363cfeb5e5c45df7b997e6f68b3708326877219a5c445` | 0 |
| pczt/Cargo.toml | 4601 | `b2b58ab523aad8654013aa0bfb128511ec3cbba1383b3b5cd028901a889f9378` | 0 |
| pczt/src/common.rs | 22186 | `a58ee6e362805bf1f5534b5768639d9073b3f7798e73e49e9aa1554b1842eeac` | 0 |
| pczt/src/lib.rs | 39598 | `e5547e561f4f22fd0bdb931b90f4728006b24a4eee2b45114a47290250f6f37a` | 0 |
| pczt/src/orchard.rs | 103702 | `483324d3e983919c48ae0b7a94cbc7aec49d908fb328f4ea7a20210b4e66f8ac` | 0 |
| pczt/src/roles.rs | 20952 | `9cbf3067639b2a801f0fd8a3bba4a9c708a4041a337032923fa23b28fc3f522d` | 0 |
| pczt/src/roles/combiner/mod.rs | 3166 | `c44b30771ae5f2dd3ecf3ce1785fd50f9def83e6cb440d7c68ed89d708fa76f0` | 0 |
| pczt/src/roles/creator/mod.rs | 16763 | `e5593763da9d0668322d4e68eabeb94012ea4a130bbf49f9576b8bebff8c7752` | 0 |
| pczt/src/roles/io_finalizer/mod.rs | 4820 | `8b706b8b04db961ba551c330127f0991bff99cb6a5a1d14c00c486aa86b524f4` | 0 |
| pczt/src/roles/low_level_signer/mod.rs | 12419 | `ece5222d7f186669afb88bef74abc52c9d4b5b0fea10396199cc07603923424a` | 0 |
| pczt/src/roles/prover/mod.rs | 1718 | `362b884b4d44938e07d904918259fa427f5262df751e53cf456dc4ab938302aa` | 0 |
| pczt/src/roles/prover/orchard.rs | 6566 | `10575343ec692fdc7af0e8127f750d0c497064ff7ba769d9bedd3d763e4d78ab` | 0 |
| pczt/src/roles/prover/sapling.rs | 4252 | `188d4bad03cf4d0b310b61348c4288ac4c0658178d7a4854cd10015ceeae9041` | 0 |
| pczt/src/roles/redactor/mod.rs | 1437 | `e1e4d6d092720093205b2c9eeeeeac7b3f2443af4870c6826e88611b05e8fcfa` | 0 |
| pczt/src/roles/redactor/orchard.rs | 9162 | `3dadb7993fda81ecf4f2cf8c5ca33b04ed040c77a14a7b7a92f295b0fb2b3112` | 0 |
| pczt/src/roles/redactor/sapling.rs | 7324 | `1b359569364bb9079d22420e737cc96298943bde809a85ba10fa8a589e8fcf9a` | 0 |
| pczt/src/roles/redactor/transparent.rs | 6974 | `db5949deb4dd851de271f66246e51338385530fc644d5d7700bf301969782b7e` | 0 |
| pczt/src/roles/signer/batch.rs | 17769 | `0227a2c6cc10c71bf6505869514fcd35f45de6a4514cc33732dbd488ad61973c` | 0 |
| pczt/src/roles/signer/mod.rs | 31821 | `2145651f5e27de716cc6e0a308e0ea879a7e900f912506ab7ebf546cdcd95c0f` | 0 |
| pczt/src/roles/spend_finalizer/mod.rs | 2342 | `4e1cd75e16f8c27dc33fd79545d5104e902c73962ae94f5feeafde8799552d2a` | 0 |
| pczt/src/roles/tx_extractor/mod.rs | 5991 | `b7d097fe9de522d037d81c3b65af7efbd1cc3978a3fcd3a0fcbfe9d8e3c9b694` | 0 |
| pczt/src/roles/tx_extractor/orchard.rs | 1331 | `01f6047241666d2069c239f7bc76e5230c34ccba0ba0755d439954c75f8a8e5b` | 0 |
| pczt/src/roles/tx_extractor/sapling.rs | 870 | `54a870de9e89638820ba459bfec0e923e548280d29cc1f2df72a2ea501df87a9` | 0 |
| pczt/src/roles/tx_extractor/transparent.rs | 534 | `6ef0d010a927cc969b6a9f78fff37eb046fc4bdd959e816e41c32033416fe340` | 0 |
| pczt/src/roles/updater/mod.rs | 14631 | `4a798f0c0e1b2fe48e127ec14fbf2dd30ae5f2fc45a7159e2ac43fa9649e383f` | 0 |
| pczt/src/roles/updater/orchard.rs | 2528 | `25d3c19fb3025e6be3a58bd785235f95071f0e3f110f73b3155896c4fc7e7063` | 0 |
| pczt/src/roles/updater/sapling.rs | 1235 | `9551f53c850e5e3909228144b1152b76b6d9858128d10a210cf4f4e51869830e` | 0 |
| pczt/src/roles/updater/transparent.rs | 1105 | `cc24f415a7f1a5ea143972a0b564ff3fd6f80697a6f7293deeacbdda0959e474` | 0 |
| pczt/src/roles/verifier/mod.rs | 846 | `04d4616e82c37edc7672d7b4346c6bc5cbf1e2d00fccaf301d717c8a4fb4fa65` | 0 |
| pczt/src/roles/verifier/orchard.rs | 2527 | `f2c1e65e15176decca66927cbcaa3a38c3a09df08f78c4dc31f6f2d8682ca434` | 0 |
| pczt/src/roles/verifier/sapling.rs | 1310 | `818fb4ca3d242b4e35b55d8d26fb97b49879d12915e1cf8a432c70bb586f431b` | 0 |
| pczt/src/roles/verifier/transparent.rs | 1251 | `343696b07768a50068d924730e8869289f5489e04548e325060a0536de6e820c` | 0 |
| pczt/src/sapling.rs | 33117 | `404edf4e4b86fd4273e4dd092e899698c035dc381929388965246de9e7fe9479` | 0 |
| pczt/src/transparent.rs | 18048 | `c78e8f88ae58b2bb8fa91dcdb2ca35dbe3b964d6413e557e1a39a7963717e9f4` | 0 |
| rust-toolchain.toml | 66 | `33770f77c5cb48a231ed517388b85dda27873fceceaa52b18a06108af4fd879f` | 0 |
| zcash/Cargo.toml | 999 | `1b4b9b26c7729473798d483200452c80a4034661724804795bec208f8db15f21` | 0 |
| zcash/src/lib.rs | 360 | `8851e622aaaf23dabe44d82ad3224ace6016a91b4d07691d0794fbb9f2498a37` | 0 |
| zcash_client_backend/Cargo.toml | 10453 | `4e22a4980fe4dc63bc1f339b3bc8d15a8ae4762f6f9d4d302170aec0d331af14` | 0 |
| zcash_client_backend/build.rs | 4290 | `59c2c56d8e84904759c0cf65ca603c63024339972f65fa43fa1e88612f7e3411` | 0 |
| zcash_client_backend/lightwallet-protocol/walletrpc/compact_formats.proto | 6490 | `d8d0c8aaa5ceec7d5dcc188ef25b04011df2ec0254901620fce982fc13aeb32d` | 0 |
| zcash_client_backend/lightwallet-protocol/walletrpc/service.proto | 15232 | `80575dbe59a9bf2e6b79e2391eb78679c453f1a0477292eb97ea3b58bb6c8b10` | 0 |
| zcash_client_backend/proto/proposal.proto | 7211 | `f72aeefdee46bc9b42504faf0b3f811b736289ca9f1812ee0230428e7e371e44` | 0 |
| zcash_client_backend/src/data_api.rs | 245109 | `c0000e72322a214d7eba1d298a1b1c349f0c37b305de02515389be22d35de441` | 0 |
| zcash_client_backend/src/data_api/anchor_retention.rs | 18296 | `f9fe8ec75a850be553a2188601665a956d2f0ad7646892c65a1efbac0a1d2dd1` | 0 |
| zcash_client_backend/src/data_api/chain.rs | 29089 | `9626e0dd1824ed8d7a10d94fdedab843fa456703df8ed22908c1167c58dc349a` | 0 |
| zcash_client_backend/src/data_api/chain/error.rs | 1953 | `cfae1c314f0abf4a41b9c78e3e0055e87777bebdd1616be1e26de216912084a1` | 0 |
| zcash_client_backend/src/data_api/defaults.rs | 5487 | `a3d26ae57343909dbcc21dfe352200c7a0b1e4755cf78358f81982327c9f1a27` | 0 |
| zcash_client_backend/src/data_api/error.rs | 24427 | `2056fc5d453204b6819866625a69e729e5ddb723545fec8660240ef1cfcf78da` | 0 |
| zcash_client_backend/src/data_api/ll.rs | 42402 | `62df4bc82b5bcc7e0f48c0c6541ee1e917a97d201072b805ed7ad6cc5fe12b31` | 0 |
| zcash_client_backend/src/data_api/ll/wallet.rs | 87759 | `4dae07184069adcc411e3a05761c2989f1280140466c6dde7fe21e202ed4c890` | 0 |
| zcash_client_backend/src/data_api/locking.rs | 25153 | `11ee7c5309193cada1774298165df61b984265735844066f923c66d205ba7aca` | 0 |
| zcash_client_backend/src/data_api/scanning.rs | 6652 | `e65da16c7f09a9d70e93cba3c9a7773edd3d85a190b8e84d8033a2d4340b1f33` | 0 |
| zcash_client_backend/src/data_api/scanning/spanning_tree.rs | 27619 | `01e603b5a42b5fe7387782571bb5e6ede18b078f6479b4db83f41a4c97a1e225` | 0 |
| zcash_client_backend/src/data_api/wallet.rs | 183539 | `ae75d6dfecc19bc4941254734822cab1b9bbf982c175257f61c6dea7f578f616` | 0 |
| zcash_client_backend/src/data_api/wallet/input_selection.rs | 139583 | `fd057ab405a33ac03b81a6c7e69dc91739e8263b75cfb415831d22382575b4d4` | 0 |
| zcash_client_backend/src/data_api/zip318.rs | 6604 | `f9c191c87e6c196b7d09c7f318e583e58604e421282de05826f9e4d860e2232c` | 0 |
| zcash_client_backend/src/decrypt.rs | 32717 | `b160542f3aae544086c06aa66f59a5cef4ec2edf3743dde57effa6f8a4198ca3` | 0 |
| zcash_client_backend/src/fees.rs | 33472 | `8744c008a8eded3dc0d0698ca970f7438f21ef0494faaf07a7e604ca29c3cbc2` | 0 |
| zcash_client_backend/src/fees/common.rs | 59203 | `45b6e67e13bc3ba691169b60a156cdbce2fa66091ac1726e991075441a8eb48f` | 0 |
| zcash_client_backend/src/fees/fixed.rs | 10048 | `c937b76e00627ab3a0f11a99d808c896d408278a9cefc9b57fa54c90549f59ac` | 0 |
| zcash_client_backend/src/fees/orchard.rs | 3398 | `a25ca7f8f8abef02ac9e65a07e3537dfebca881a8b44876180a5621f20fd38a5` | 0 |
| zcash_client_backend/src/fees/sapling.rs | 2984 | `a32db08a0e1e0e8ded64f1565122b0b35325c3e6ebc2452119dcc3cfe462f2c9` | 0 |
| zcash_client_backend/src/fees/standard.rs | 949 | `941ad20e3bb39396b7c215a817ff8c12b9c195627b8d131d61a69810528f2d40` | 0 |
| zcash_client_backend/src/fees/zip317.rs | 85127 | `6a371e5dbe1e623f38f823962b575d04b80b2070c959dc1df7279ec4ac3cbc9f` | 0 |
| zcash_client_backend/src/lib.rs | 5709 | `13a038a66f74ce48ae05234e5e2a257fcbef8e7819c3749380d89b739b0b2f07` | 0 |
| zcash_client_backend/src/proposal.rs | 118472 | `e29c30b0ad345264d476cccd0922c90d40197de0c2184b4bbcc19e8cba86863b` | 0 |
| zcash_client_backend/src/proto.rs | 51915 | `e2b4494c29458019254d1ae59691db454e99ee4f67bf9407d82abc8d066631b1` | 0 |
| zcash_client_backend/src/proto/compact_formats.rs | 8097 | `d6672eb5c49b158bbe0614f161f4be292d3203fc3fe56dcda503e5c2769f5a6c` | 0 |
| zcash_client_backend/src/proto/proposal.rs | 11947 | `ec6933e5bf85f4492aaba37b0c7fddd6ae9d61c211fdd5d08bd21cfde5f94488` | 0 |
| zcash_client_backend/src/proto/service.rs | 45200 | `f5058c7c262ba409fba58d27afd78e1ad7fe371b3834c72e2a18ef39d291a1fd` | 0 |
| zcash_client_backend/src/scan.rs | 21712 | `c68b7bec12c77989eb688d7b04b1a861406d5c43aba5121b260d36e897862c6a` | 0 |
| zcash_client_backend/src/scanning.rs | 49247 | `ec0b5539e04cf07377f3b850c6fa47aa70aaf8b3d7b3af40e39888127cac5dc8` | 0 |
| zcash_client_backend/src/scanning/compact.rs | 52785 | `3a4d174fb58bf31bd66f18b1c1cd4f848469ddef7fc462315546cadc765d8fb8` | 0 |
| zcash_client_backend/src/scanning/full.rs | 46459 | `137dc8301d07063ccb5c652e6e603498e10cb64eb64d4ff0d5f94740a0d1cff8` | 0 |
| zcash_client_backend/src/serialization.rs | 19 | `5aa43d739cce707b80c859f04cbe56d453d2eef47fbb15701ab261d980b49eb4` | 0 |
| zcash_client_backend/src/serialization/shardtree.rs | 4157 | `5a428a638ac0e4675380527143aacee09882b1302d51921675cdcdcea1548fbf` | 0 |
| zcash_client_backend/src/sync.rs | 25733 | `5acf93c423c9ceab91d72e4569b41c77daa01a2faa17f1d102899661eadc0d45` | 0 |
| zcash_client_backend/src/sync/decryptor.rs | 19471 | `e3b92c0069d6ff8af8926746e2e61308ce03c65e5eba51a650ba826744f8a81a` | 0 |
| zcash_client_backend/src/task.rs | 737 | `8018642f411bba591196f3235d0eaa8bb2b38f3fa6624a144bbc07ab392397ee` | 0 |
| zcash_client_backend/src/tor.rs | 10717 | `9635522697a2597655e9edbf3642de711edb6b74939904a7a3b48cf7ce100cb2` | 0 |
| zcash_client_backend/src/tor/grpc.rs | 5346 | `ebe82a7c198de14a7aa1b5a2a0378ef9b27abb8997b30134808f2344193b38cd` | 0 |
| zcash_client_backend/src/tor/http.rs | 33664 | `95865c533750a44b372ac1f4c9c4c238524ed37b0ec0b22c0469412ba0df527e` | 0 |
| zcash_client_backend/src/tor/http/cryptex.rs | 8862 | `949045023c6219c056af17492297ca16fdf2e4477cf456eae9db54457d0938d9` | 0 |
| zcash_client_backend/src/tor/http/cryptex/binance.rs | 1677 | `bd7a0ab892ac86cb794c02ca5555259cd8d7bc92281f597b5b4411b45ff2c9c2` | 0 |
| zcash_client_backend/src/tor/http/cryptex/coin_ex.rs | 1990 | `2c8aa1ea109d607595a2abdfb04098db1c93362f413a924591ccaa6a67eae22c` | 0 |
| zcash_client_backend/src/tor/http/cryptex/coinbase.rs | 1390 | `986ebfdb3397eb380b9eeba9378ddf3e20a33eb4270bd9d36902d7403d4aa3f3` | 0 |
| zcash_client_backend/src/tor/http/cryptex/digi_finex.rs | 1475 | `0f504c2ccc68f0613b96d7b84e26bc3fe0f47c2299a5b2200d15d115750c5dd9` | 0 |
| zcash_client_backend/src/tor/http/cryptex/gemini.rs | 1206 | `d2877b178c91daca5786de3afe57c5885dac40641791dce77b238a22475e340e` | 0 |
| zcash_client_backend/src/tor/http/cryptex/kraken.rs | 1764 | `2883622a7d89c98d16053f836505b974c1a541b8e041984964de849e89314b5b` | 0 |
| zcash_client_backend/src/tor/http/cryptex/ku_coin.rs | 1652 | `50b04fa066a23dcfaf32b6c95077adf9e8666ed5413bd4f02a018779e3e4bd52` | 0 |
| zcash_client_backend/src/tor/http/cryptex/mexc.rs | 1544 | `b523ae37dd21910cb8af633f5cbbb6df6e7c2096b65bbbbfb226c4a023a444b4` | 0 |
| zcash_client_backend/src/tor/http/cryptex/xt.rs | 1349 | `baab400a2acda0cfa68fe36671181a6bc40bdd3e6d02f5e5b685b1438585f4c6` | 0 |
| zcash_client_backend/src/util.rs | 2217 | `33b077d3b3b477696da054899610e02e20a9a30f5ce775d14deefdcbc8e81aaf` | 0 |
| zcash_client_backend/src/wallet.rs | 52615 | `41e038af8afcdd9d7028619aa97c009c6be2ee08123a2d530b19f477b273e523` | 0 |
| zcash_client_sqlite/Cargo.toml | 8738 | `e004fc75fa8f0ca57c2b8697697409f9021faf01694992173b8bcd71ae59f890` | 0 |
| zcash_client_sqlite/src/chain.rs | 17888 | `448782a4c5939dfd1b09e820c38ddd5bd72a918117795c849cecd5f18fdb79b9` | 0 |
| zcash_client_sqlite/src/chain/init.rs | 2034 | `e5494c0db48acfc86b71f8c2ad1519e0fbae9efc867fe999f68c368cbbb29c04` | 0 |
| zcash_client_sqlite/src/chain/migrations.rs | 74 | `130503e1c24a905ecc03e0adbebf703e751eb2b3a7120ade154e6d85cd5d2b59` | 0 |
| zcash_client_sqlite/src/chain/migrations/blockmeta.rs | 1811 | `b8225c4718f9b8aa4cc49c29f70b1f5d8134a57570e22cd34c7e7f4971bb550c` | 0 |
| zcash_client_sqlite/src/error.rs | 28283 | `13be30df8619098d188304fc908b5b01a30fc33f0c6edfcd822041ed1460c2cf` | 0 |
| zcash_client_sqlite/src/lib.rs | 215065 | `c2517b23d072ff310ba22625dd394dc368f8549a1d9a1a279cf4553e221933c8` | 0 |
| zcash_client_sqlite/src/pool_migration.rs | 11321 | `64b16b055bb1c906722adea4c76ae069c4d19d92f156d6fd1880075266ab7b56` | 0 |
| zcash_client_sqlite/src/pool_migration/error.rs | 6722 | `83a237affd5a30d98ff5a83af8b508151804fbee26876fa6db9334dd447b76f8` | 0 |
| zcash_client_sqlite/src/pool_migration/orchard_ironwood.rs | 165551 | `f73e38bee4cf695144e7666e24c968505a1311eb9647a2a10c54412d7a171f20` | 0 |
| zcash_client_sqlite/src/pool_migration/store.rs | 100536 | `2db199ae15a7a84926abbb8e8e317cc00ce2ee76ba339a70c988649b82558ad7` | 0 |
| zcash_client_sqlite/src/util.rs | 387 | `19e90bdf9de56be56cf2a6a00479e9856f78b674ad30e79954546874108f15d1` | 0 |
| zcash_client_sqlite/src/wallet.rs | 349453 | `759b0d6c6a568b2a01a48049dddc38a06f1611e1dba52aded65232bcc14b0fbf` | 0 |
| zcash_client_sqlite/src/wallet/commitment_tree.rs | 79912 | `59ae465458b052defaf9684e1934c462211fb49a1f2f161cda59f3ffccac714d` | 0 |
| zcash_client_sqlite/src/wallet/common.rs | 53887 | `862e4652305a488cf95a41ba7912ef8729b90c0ff8b8bdffce307bf9c19f85d9` | 0 |
| zcash_client_sqlite/src/wallet/db.rs | 102081 | `2adf12f943266a11f64bc908b3970c2d3bd6c8ead2e6947d763b0f2dad5a0fd5` | 0 |
| zcash_client_sqlite/src/wallet/encoding.rs | 13943 | `8e4d77d8bcc541be8653c238873ec8e5c64ed0c69cdda89cbd8738b9e5d7537e` | 0 |
| zcash_client_sqlite/src/wallet/init.rs | 67895 | `3c7f94680655eebc5d3a479826ba349f230986741ee5a3d1e1672a18a28887c8` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations.rs | 55309 | `9c15a8cb6bd81699461a87c39365f4634d8f10437945579c9b0b45a86c6088ce` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/account_delete_cascade.rs | 31296 | `fa1c1ca1a2cbba3d5a3e0b03c0e0e829d27569816d479bb6c962dd114b72a9bb` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/add_account_birthdays.rs | 4347 | `310e3f68b83705ed58d9ec9a00f0085e8a3a382555b0874acc857ed80d0c6091` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/add_account_uuids.rs | 16228 | `131531f5d60981c620570d298093a7eae5cbfdc1cef6822a71c72c4b399356e7` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/add_transaction_trust_marker.rs | 8620 | `cd4f3b6e8c64a011fff7641ca218933b04f52c392900a2ae508169112e1270f0` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/add_transaction_views.rs | 22752 | `e7497f8b2a80d2ab609c58828acfd3fe99a223a5eaa1a3a82ad559fbde804a5c` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/add_transparent_receiver_address_index.rs | 40073 | `403669054ead8e1900edbf45aa9c19ab2f9de46c7fa20cc2605662b3707afa72` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/add_transparent_value_index.rs | 4433 | `c24e1a020968b27ce30ab91226ae0ae852b63c59a9588e4c0b50175cb886d640` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/add_utxo_account.rs | 8785 | `81142244ffd793cc474c6aa4e5fc21897b3659ddcb36c40a27d1c94e505ee397` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/addresses_table.rs | 8586 | `a2f0a1e56268152437d08cbfa3d9dbf1b9673f48ffb5708484609e18483bce3b` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/ensure_default_transparent_address.rs | 1770 | `53f868550008895da6a567d609be662dddecf418e352dfd560a8ce4cfcd9c294` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/ensure_orchard_ua_receiver.rs | 7050 | `677cb41c2312f6a684c1b2b2514ce0c7ed273f55af10f566fc5b5a28eb4aac01` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/ephemeral_addresses.rs | 5533 | `e9a88d7c24b6976f283a60c4cbed50709e86cc68f0624212181a0a2c89a194ec` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/fix_bad_change_flagging.rs | 2537 | `5fd840389fcfcb88a449471be1a910c552e29eb618a0436927657665d2c3e094` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/fix_bad_ironwood_change_flagging.rs | 22818 | `4dae69fdfc444c5fe60ecd15f253ccf7d3133fd04c609bf14851bbe7818d333f` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/fix_broken_commitment_trees.rs | 18081 | `e6f4c290f908a999b604f19e6ee6a144de548db4fafd6b0faa56eabac77e9abf` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/fix_transparent_received_outputs.rs | 2995 | `1cff58dfda8bb0629daf8c0a99a3a75ed75777a716099214a0cd57b6ebec5e47` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/fix_v_transactions_expired_unmined.rs | 11430 | `cea73bf94c60f7b74c7bae313a37b6a80ff698c16bdc0f05b050bcc8c44454a0` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/fix_v_transactions_multi_account_totals.rs | 18884 | `aa4ad6ddcb6679a2a0657db8c65f742459f1554dc2c80bba6475132a70be3cfb` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/full_account_ids.rs | 29007 | `605b19ea55f4a4efc7e06ef2822a1744037fd86554a04526b5a21c56e19ff334` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/initial_setup.rs | 4503 | `add91f083cf39ad1571be95c1753ec0b18adf6e8c6ddfeb8d3fb1d4c73f7333c` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/ironwood_pool_code_views.rs | 14288 | `041dfed30898dbaf21c37d39e7673840d0389ab09eba1a06ddd3686f0630bdcd` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/ironwood_received_notes.rs | 4283 | `94f2b7937b501acc388c826ca5d678920d7fb70137d584bc70ce7104fd35986b` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/ironwood_shardtree.rs | 15048 | `ff27fa1e55331b5af1955ad5ffd673ebc86c47b9b5c57cb4c55adf1d85437f6d` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/ivk_item_cache.rs | 18962 | `4308a8cc36ddf89eb618053326dae6418a54dc7a4e258261f8e9f596b85c290b` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/note_locking.rs | 3015 | `8cd352c8fc53308617b4d8675ff0f0ec9acac7e703255e9d2a540d845366bd8f` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/nullifier_map.rs | 2705 | `47e97be08acd840447062e20fe9d8e44e71bf3ebcc850e687daccdedc8d33e86` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/orchard_ironwood_broadcast_binding.rs | 10177 | `a9608a9d73bfe4b89c9e9e6b2b932f381a0151cc2fa2d9173027e0acc9260b7b` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/orchard_ironwood_migration_anchor_interval.rs | 8593 | `df6b00200c0adbe1662f831797a3d92e2ab487cb68a702201cc43c85c75a5d09` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/orchard_ironwood_migration_history.rs | 8802 | `fec7e08d071629ab2ac7c989622f8e5049be7d189c2426d054826ab96d9764a4` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/orchard_ironwood_migration_tables.rs | 8788 | `31717b78122ca049ce932f0391d94ff995e6e5851d4fe578ac84b41a80e47897` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/orchard_ironwood_migration_txid_blob.rs | 10033 | `44cbd5e0e37643efef1862c03ad49ca06e74d6d4c0b635566b79121830efb664` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/orchard_ironwood_migration_unsatisfiability.rs | 48868 | `79372e305f9e85fe0ebbb547eae8a5e071273a0377a55ba68c5d05f8b9174dfd` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/orchard_note_version.rs | 6786 | `364a7482f9da35b9b575a8f65079a83ff88a5661e254d78bf210861beaf2ba75` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/orchard_received_notes.rs | 15991 | `e507d78c88f006ab6f93cda9a988cb673603a41e6db3578febc6e72d8d5bf0e2` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/orchard_shardtree.rs | 10024 | `6ad70d1ce88834c642c64e9a446c917855e3142d28c405c2579baa0793e987d8` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/received_notes_nullable_nf.rs | 17731 | `3af819ec77a78081c2b6998c375e8eda9755dfab604a73f34431a6a8b0987d5c` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/receiving_key_scopes.rs | 35878 | `da2840dd7c17c3b95a93f46fa9fd8923bcfe683616b5b809dc82d209166194d6` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/restore_ua_transparent_receivers.rs | 19945 | `acad8bc4a0e1bcb1fd088abade5fa1cebff47219a1d02477bbffe7c3f5fd8ab8` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/sapling_memo_consistency.rs | 11851 | `873c8ba60cfccd14f6400fb35844679452a19b4af0218b7baf5b7d7c6780714d` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/sent_notes_to_internal.rs | 2978 | `3ea5c08d6a54873cd114ffeefee23fadca2866c5d923eb1d222492bf430afc24` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/shardtree_support.rs | 12354 | `27a78578362e7222817951d292b0fbbbb4072a648716b1b80cc88816f6a0d5ad` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/spend_key_available.rs | 1545 | `a94ed1ee3cc1d67812b4290a0e6f88c0309626dc5e825b4039b021be1443f061` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/standalone_address.rs | 12952 | `9931bdd4d3fe8cbb441e43d41ab4cc732fcc6d3839d42a30f41934f648c330c0` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/standalone_p2sh.rs | 12194 | `1fedcb2979bde6ebdecdf3c7f78c6043c01c09c37b4ff549ad912d2535be53ac` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/support_legacy_sqlite.rs | 3451 | `5c483f1bb18ddf7dd1c1bb3a0495f27b738d0d96338e2cc31de114dca9f03f7d` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/support_zcashd_wallet_import.rs | 4975 | `5a24aebb41da6c6f285ad2bb641e4e8ddc0dd08fe8703c01602985373836481b` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/transparent_gap_limit_handling.rs | 35549 | `931eb3f42473d6bc3437f1f03da14e3ccb0a14c28736c8047623c82968f62932` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/transparent_spend_locator_map.rs | 3515 | `363a1f1b46a5e4cef3163595bde46246e2999cefd338099aa641a422cca2ac69` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/tree_retained_checkpoints.rs | 2003 | `2f5136decc9113411340414eb148b1ee0bad42d3063945fc081615d62e579464` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/tx_observation_height.rs | 4312 | `71f2e2973f765e100ce1418fb683bc1aadff6da2dcf6479ffea4a57197e80d50` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/tx_retrieval_queue.rs | 15556 | `bb66209d9c0b85d9b02950fe1af6f1a097fdf081b7e4f4681fec7d5ef4e6b4fe` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/tx_retrieval_queue_expiry.rs | 2699 | `aeade75ebff45958f920193199f076f92e34c953a56446f69df832d13dd991c3` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/tx_status_observation_intent.rs | 4837 | `b7fdd04deff5f19a8c86bd4fe9b9f2ff85b2a9c3cc4e438dcf1a8109692d980e` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/ufvk_support.rs | 13412 | `378efd2dc5c11da405a0005c3a9aa5ac8cee484d2a21159550e936348ffc35da` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/utxos_table.rs | 1968 | `640627dfd0d12516cdd6788d5b7c444997bf8f8a1fe5cb4d031ba87773879e99` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/utxos_to_txos.rs | 16710 | `669feb2065f40eda87a9aa689202de8a039815570d42913168dbc5e2dc417f0b` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_address_uses_ironwood.rs | 17953 | `faf213325ae664c1cc93a32557f226c086531eb55e18d5366bc01370306c7453` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_migration_transactions.rs | 10722 | `157015449b027a41435f5718d527f0bee05d31496e629eb35f9218f4feff87c4` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_received_output_spends_account.rs | 2619 | `56eba967b26ebc66dcdafb7536ac147a222b904552d2db02970e1860854f152c` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_sapling_shard_unscanned_ranges.rs | 4147 | `033cabe7143f6e0b4de32d4ad137675013d17138ee7feea562b65a82dd2ccfc4` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_transactions_additional_totals.rs | 11460 | `d08b855526ff81d469ee62750f8853ef918cb1849022ee681cda65e521e4ed6c` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_transactions_net.rs | 26954 | `77de07654b2f02bd19555191452dc25ab89610223e9f9c8d60ba7ab2c81b22a2` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_transactions_note_uniqueness.rs | 11721 | `9b79484fb9d3892e7402b05c8176613f0ecb1f1c4e0663662dac3f9c5e6fe3c9` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_transactions_pool_crossing.rs | 13764 | `b84fa7018889d024565a0e27f65217e983f87dc1c3d0411bf73eb95ff88319ea` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_transactions_shielding_balance.rs | 7456 | `9dc520a6299c90c48b9be0a94cac043f1da7f40b0e56027663024b4d694da739` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_transactions_transparent_history.rs | 9583 | `1385d9534bee4c63c3e7ba6d8744faf2c73345a5f815e7697d250b9860a59ac6` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_transactions_zip318_kind.rs | 24512 | `9f8824f724d8b45a98f4017a52cd63633388b3ee53eefe4d11246134c7cce666` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_tx_outputs_diversifier_index.rs | 7209 | `96838ec6efd6278b6dd0f06dc8aba8fc823362a305d5245a093af21c866a287c` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_tx_outputs_key_scopes.rs | 7438 | `9de1f632b68aa633ba2bf4ce5dffe4c446210d6ef4e8403581e57b47b0c4a8b5` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_tx_outputs_return_addrs.rs | 4694 | `c75cffa566544cf90ff8121439845c5615193616c42f9afe730c70c416080e8f` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_tx_outputs_transparent_addresses.rs | 8108 | `2f7ccea9840897626415599bbaf23c9197ea90bf5ba4e348f0543175933a512d` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/v_tx_outputs_use_legacy_false.rs | 4273 | `5172fcb9f2508f75304c191a4ad4b78e1095ae8648597c5170fae15ed9a22540` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/wallet_summaries.rs | 3511 | `de375722dfdad7f620e5de700f1255395fda97cc5ccc6139e45b40cbe7d60e4e` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/witness_stabilized_notes.rs | 29059 | `edd790e468f9fdbfc798d06dd83f5d7a54b196df2fa6c768a139f9800d640831` | 0 |
| zcash_client_sqlite/src/wallet/init/migrations/zip318_classification.rs | 4375 | `055cf111a46c29af1b26ca308e97e1da3672d7188235cf2991e1a1548442594e` | 0 |
| zcash_client_sqlite/src/wallet/locking.rs | 56118 | `fc5469bec5281ee88a9170bcb7a8c08ba5a7fd491b2aa5f3e07380b9bab3f97e` | 0 |
| zcash_client_sqlite/src/wallet/orchard.rs | 127938 | `3c4e95f7dde5d47f588df147e99a6f7e65198a3f3e5cc1a6f832c414e95e118e` | 0 |
| zcash_client_sqlite/src/wallet/sapling.rs | 28207 | `60316cab5d6cd516b120e02f3016dd65a488050010d8db58d35056252816e1db` | 0 |
| zcash_client_sqlite/src/wallet/scanning.rs | 106495 | `fecf821f993583cd5dd916291a237e7ba90b19aade4f5ecd6a78bd802db76374` | 0 |
| zcash_client_sqlite/src/wallet/transparent.rs | 214071 | `84e2f48cd5852a7eab8a7ce8abefda436fe9b4c88357c7ea7b98ec0d557ef0ff` | 0 |
| zcash_client_sqlite/src/wallet/transparent/ephemeral.rs | 8865 | `1c31f267a81867448f336ff5d2aa95009d133891666a736c62c77c9af303883a` | 0 |
| zcash_client_sqlite/src/zewif.rs | 120590 | `60953a37840964dab7212eff27a39ea44b5d6f0ab5890fa826d88dfc0dfeb8ca` | 0 |
| zcash_history/Cargo.toml | 737 | `007d33a003baaf37bd7525a23b872279f717f0a63593ff67364b1852593305dc` | 0 |
| zcash_history/src/entry.rs | 4261 | `bfc5efe75f619147426eaee8351316702a90ab9c7ab230f17a12e4350f7d8394` | 0 |
| zcash_history/src/lib.rs | 2508 | `6404d6449ef8653ba945532ba3e51985fc80dab3e054598b26dcd09eb5473740` | 0 |
| zcash_history/src/node_data.rs | 21997 | `ef26fa5dec6df0714f93c21c32e4cebe5f7d405c268a578cc3bff394c8c1344a` | 0 |
| zcash_history/src/tree.rs | 26295 | `74630d10192edcaee9beedac18ad92d942b03cd6d7f079938040530b2a0336b8` | 0 |
| zcash_history/src/version.rs | 6454 | `08ca0b318412f6f4a5fe776847825e9696e2f28814f4277641770dbd68677795` | 0 |
| zcash_keys/Cargo.toml | 3839 | `410cc0bcb8164b68f0fb444f66eca1f17bf61f1fc8f04c76d1685624f478c121` | 0 |
| zcash_keys/src/address.rs | 50294 | `52e47576d0a2a94be1b549a55010b4e0ac784cab23d461121340971f394bdca9` | 0 |
| zcash_keys/src/constants.rs | 5910 | `3b7682d90f0dfbb8010aba93716e2d7476f7ab00abe7231c3a1575144b1905ac` | 0 |
| zcash_keys/src/encoding.rs | 25472 | `2be659e2ef6fc9782ae538c17f52b7ddda7714fe61008d67e7f0255138e37590` | 0 |
| zcash_keys/src/keys.rs | 141099 | `bd0082831768f382b2fb6d33c41403b7c8730d6e0a2453bf63a7ea741beba354` | 0 |
| zcash_keys/src/keys/transparent.rs | 18488 | `856dc76b2357dbcf0ab84b3e498152a00571b654bb1f2bd19b9501f8224fbe5a` | 0 |
| zcash_keys/src/keys/transparent/gap_limits.rs | 12352 | `7a648ae18f271410a5aea6721db339a5a25ab7f537f3b4d9679a6af0e5cc4f5c` | 0 |
| zcash_keys/src/keys/zcashd.rs | 9900 | `ec4e74fcfee42cc53f9213c854457f9ebf9b5755d8364af5852a0aaf2b1d97b8` | 0 |
| zcash_keys/src/lib.rs | 752 | `7dc430b8e92e66884febbff95df313fcf7f2e6cea2f2c2ed0cbeae7ce0d7031d` | 0 |
| zcash_pool_migration/Cargo.toml | 4427 | `84cb4c233c4b280b29b93c2c23d43d05d20ecee6fdd7a3e195301e7f75f0810a` | 0 |
| zcash_pool_migration/src/build.rs | 12554 | `22819e71f25e0bd91ff799c2c8b00c4c917a40bd9603cbf39dfaaabc8e780118` | 0 |
| zcash_pool_migration/src/denomination.rs | 21724 | `38609669ae371eb784956a7693a2bab0cd86e6326d601fec088707dd9e549b07` | 0 |
| zcash_pool_migration/src/denomination/strategies.rs | 47233 | `a78c67da51660b13097869dd8666491c200384ac76697772cf1cd0f9771fabf1` | 0 |
| zcash_pool_migration/src/engine.rs | 383516 | `aee6f68d4539cd01414db1c7427da14c31ac7c63410d233a62a75c39c38b40be` | 0 |
| zcash_pool_migration/src/lib.rs | 1710 | `9b116e1efff4dce35229cad7b271893ee3010bfc1695bc95416c59f9d1ba69b8` | 0 |
| zcash_pool_migration/src/pczt_spends.rs | 3970 | `9803b7ee1f23669c57340ec3b2655baff6b78340c4251852e70e2a69f1a64cfe` | 0 |
| zcash_pool_migration/src/pczt_txid.rs | 3430 | `10679e58849c4bd6f76b37cb8d2c1e44054f1208d5553d60c8b01cec8725444b` | 0 |
| zcash_pool_migration/src/preparation.rs | 44456 | `41b9d6cce1bae5f5e40d3e20e4bfda2c24b7e0a10a4c60d28f97e79cf869df3c` | 0 |
| zcash_pool_migration/src/preparation/first_fit_decreasing.rs | 11773 | `7660be41f417f9f78f852897194fb9ceb934c12cf5893d3e0962178ae8d411b7` | 0 |
| zcash_pool_migration/src/preparation/layered_greedy.rs | 53089 | `b03646d4c86b870fbf0fb3cd9c6a76d1d7485536e5ed449603a06d75611acf9d` | 0 |
| zcash_pool_migration/src/satisfiability.rs | 146836 | `575f140a8c640fe9222a4e343c9c28a3bb9300f39432ee7cae3fd547563b6fa6` | 0 |
| zcash_pool_migration/src/scheduling.rs | 113722 | `8026c5943974240474c06d942bc4c0f9307359945f8039d2b10e274f8654f5e8` | 0 |
| zcash_pool_migration/src/signing_rounds.rs | 42189 | `3721e27617e658af99ab33823b59f4639a6d8acd3de7eb22f3d23dc3a829ad25` | 0 |
| zcash_pool_migration/src/state.rs | 218376 | `33c36ea159ddbce8670ea9729c2e28d466cca2ca5bf27e1aeba18bc9688000be` | 0 |
| zcash_pool_migration/src/wallet.rs | 49949 | `7c8410b69ffcacd4dbb0dd9fcd8855bfa385cf011db35ed5bb3271c030c58f3d` | 0 |
| zcash_pool_migration_memory/Cargo.toml | 1314 | `8cbb83b9a2904b50ebaeb70a8507e3b3303c2a9f639e79c62c67fcd1954d6a21` | 0 |
| zcash_pool_migration_memory/src/lib.rs | 23628 | `495d726d074fb069a4eb8dc58685612d30b97a707f716216bd9556629279d36d` | 0 |
| zcash_primitives/Cargo.toml | 4287 | `0fa139a594a721f7b9e3c74013ffbff8ee76be67347f15f5c99732d639174c33` | 0 |
| zcash_primitives/src/block.rs | 23635 | `10bcceab220ab13b680f2461a27f375b292ad50a76abad9f6b1eeefdbac9628c` | 0 |
| zcash_primitives/src/encoding.rs | 2244 | `ea5912560f2c21a11481392a95a361b2cb0f2160e319c5529034300a6d27c4df` | 0 |
| zcash_primitives/src/lib.rs | 779 | `c98e5f8821a7a621efb81686391d09f33a215e7ca5df05972017d2b076110fd6` | 0 |
| zcash_primitives/src/merkle_tree.rs | 115486 | `364243f99d68009602c14be8c5543fabb04fa1e49be166e7ce3b8859692b726b` | 0 |
| zcash_primitives/src/transaction/builder.rs | 128016 | `56b71d41eee531b8ddbd13ab856c2d3654b19042051091b364722eb949f63298` | 0 |
| zcash_primitives/src/transaction/components.rs | 228 | `01ded28e2e67b2a3420dc7b20ad6e785b3e4a77c44e2a976421feb54d9f39c91` | 0 |
| zcash_primitives/src/transaction/components/orchard.rs | 24336 | `bf0f5a8044330d1c8eb55c3fefbe28b66cf3d502222ea1c65a30171589614a55` | 0 |
| zcash_primitives/src/transaction/components/sapling.rs | 25048 | `ec8e4d0d81abadf1d86b01394c00710f27d187c9fd9ef1e794ba8865cf53426d` | 0 |
| zcash_primitives/src/transaction/components/sprout.rs | 8128 | `6b70b0178ea3334a46daf7e6071dfe237b0b91be931be74883a5793010b64cf4` | 0 |
| zcash_primitives/src/transaction/fees.rs | 1339 | `e85c578cbc2916338cec03d1a378167d25dfb66003771f1f4b296c215ddf53be` | 0 |
| zcash_primitives/src/transaction/fees/fixed.rs | 1231 | `d95362cfd01c55cce089d826d05f15ea18efd05ae8bf0fd1ab3091485809a320` | 0 |
| zcash_primitives/src/transaction/fees/transparent.rs | 3878 | `531200a6aab1a990c335af28cb880f2751a17132e5d84848440b840cd3a7bca7` | 0 |
| zcash_primitives/src/transaction/fees/zip317.rs | 8832 | `45758141236b7745977bd95191dfab619d6588310720652a8af0cbdf0d1d926d` | 0 |
| zcash_primitives/src/transaction/mod.rs | 56478 | `39fcd714c806fcd1b4120536040153518177896823eca2f94a72a7ec89494456` | 0 |
| zcash_primitives/src/transaction/sighash.rs | 1908 | `6ee5ca91695de9095fe174265ade901703470a88544fe8825089d1eab585be2f` | 0 |
| zcash_primitives/src/transaction/sighash_v4.rs | 8975 | `59239c04ed59d0d5d19c58274524eeb0f588a4f690154d344ae880fa5f72183a` | 0 |
| zcash_primitives/src/transaction/sighash_v5.rs | 6221 | `13155ec1c819691f552d7bc364e3f7bbf24b9d7fa780dd922ddf8f423ab6fb2c` | 0 |
| zcash_primitives/src/transaction/sighash_v6.rs | 1126 | `76aa108bca4d920e5d889fe22318398b260b15a55ab5979bb71a228de9ba3b67` | 0 |
| zcash_primitives/src/transaction/txid.rs | 23942 | `7dd5b8d891270f207d7e6e0aee8681d2d7d38e77b74e9772267ee55c3e1f8af0` | 0 |
| zcash_proofs/Cargo.toml | 2551 | `b8a713169619b05777a544e928f72be5caeae02743683b36bd93d8e6c104ff2c` | 0 |
| zcash_proofs/src/circuit.rs | 87 | `b31c395401ea947e59c9779188267592ff37bf90deed3f92cdf1c3d56c861691` | 0 |
| zcash_proofs/src/circuit/sprout/commitment.rs | 1004 | `c90b73fdd046ca818bc80b92606e6a5a210e0fa809c09ba09f322655565d79c3` | 0 |
| zcash_proofs/src/circuit/sprout/input.rs | 5966 | `f488b72238ef3959b0686b25212ab35d44c050267062416e92f5b41989b4e30f` | 0 |
| zcash_proofs/src/circuit/sprout/mod.rs | 14049 | `2ef74af1024fb6cc5584eb781e52016032aa305d09db36950c56ddf39e079b4b` | 0 |
| zcash_proofs/src/circuit/sprout/output.rs | 1102 | `6139da53aaf18f813592752f245700acad467354f2482359997fc37f853092bc` | 0 |
| zcash_proofs/src/circuit/sprout/prfs.rs | 1939 | `cb836c15cb412fdc73b77c2a9eb9d91fc6846e20b5438c1545e37ac01b7f8106` | 0 |
| zcash_proofs/src/downloadreader.rs | 2893 | `4ae40df29495f54106dad9bd07d29293d313f0d1cf34964fc6e29dbd675e745e` | 0 |
| zcash_proofs/src/hashreader.rs | 1560 | `ed234ce00866121eba96024416e37341e265727612c46ec111c51e3b7a81626f` | 0 |
| zcash_proofs/src/lib.rs | 17442 | `c2050f2e89d86a3c7a4624a144b88599d2520d68e38e62664c5636ce2a02664e` | 0 |
| zcash_proofs/src/prover.rs | 6498 | `a0242a3ed972b317697275fb508347b681f2c8285f3d8435b36b9b0829ed4e13` | 0 |
| zcash_proofs/src/sprout.rs | 4687 | `7b077eeef2f8d854ef8017f66b644ac2272a3031663bd30232b9c6e96d58f81a` | 0 |
| zcash_transparent/Cargo.toml | 2115 | `266a1b202974c31e2aa2163d56262f133bbbe04b94d31d0b1f7a289967f29921` | 0 |
| zcash_transparent/src/address.rs | 7530 | `6a5e646631eaeaa8e301505af6302c5faa36b99aaf5769d3979c8e69472873d7` | 0 |
| zcash_transparent/src/builder.rs | 43233 | `21300a7a6424fc10a2c0dda16f6ddac7b295bf72f3e753fc0e48402f8609a997` | 0 |
| zcash_transparent/src/bundle.rs | 16351 | `61a4bd9b83e0d3951d22acc8d4aac8e04c3f27b98fe3e6290eed4794a14d400d` | 0 |
| zcash_transparent/src/coinbase.rs | 2327 | `aa3ba16769a0377c6616e2de244f707a12c3ca5ca20ca71003f9028586039404` | 0 |
| zcash_transparent/src/keys.rs | 34597 | `7f85ab00e7e7ea2e3f53d141d4c6376704c012ccc25a928bb5149ba2745db050` | 0 |
| zcash_transparent/src/lib.rs | 514 | `6143fcd0e33c0d4978931c1dbe09cfa21d01c33880511a0fd0c31314e83304e0` | 0 |
| zcash_transparent/src/pczt.rs | 15104 | `c98366910ea2df8ffbe9356fe62e10d9bdb71a94e535fd98bc93ce376dbd5ef0` | 0 |
| zcash_transparent/src/pczt/parse.rs | 7146 | `180d4cf4eef89d24e87d30a90fb84f2ca68479eab8c3c0e4152ad8f57f8c65cc` | 0 |
| zcash_transparent/src/pczt/signer.rs | 22060 | `7634be395365abd176a608264c15fef69e68584b1c952f6ecca08dacd45c3859` | 0 |
| zcash_transparent/src/pczt/spend_finalizer.rs | 17700 | `2dfb9441411641a48fc898ea0a5548e6a6ae3255e2d195ad9554fd614b298684` | 0 |
| zcash_transparent/src/pczt/tx_extractor.rs | 3441 | `fbc34ffca7f11fc41da31bf32afc4b87bf26d5eb55d5922961081f5695c060a5` | 0 |
| zcash_transparent/src/pczt/updater.rs | 5807 | `5451e8746f1a5108d7facedd6bb372978c671918c150f9b8ccf9814e5bbc789d` | 0 |
| zcash_transparent/src/pczt/verify.rs | 2297 | `9045b2585a927470ba9502cadb711076af10e2ac1aaa3dedab74a061c427fbac` | 0 |
| zcash_transparent/src/sighash.rs | 9614 | `4417b5e6a2cbfb68448fa7fec432b9a30849b78fafdb545ba192a55845a360fd` | 0 |
| zcash_transparent/src/util/hash160.rs | 2086 | `a813a76278afe5125733f3219585270fb88521cfbc061554d8f938fa3e923dc5` | 0 |
| zcash_transparent/src/util/mod.rs | 94 | `f59746e68267b6ce74ba40c9971820cfb3384f9884f77a4a25173a1222137e69` | 0 |
| zcash_transparent/src/util/sha256d.rs | 1609 | `89f5102feeaddd0b5d4895f563d84997631b36863b2743eb65cb33bce0da1ed0` | 0 |
| zcash_transparent/src/zip48.rs | 35462 | `cad42458c0611cd3aa21751df669c2b3a89e2c074bbcbc3bba25e65f3c91c172` | 0 |
