# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** coinbase-cb-mpc @ 0b716706f998 · Coinbase — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-29 05:55 UTC |
| Версия отчёта | 1 |
| Запуск аудита | f545845d-341c-4227-8f70-26ebf66e78fa (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `5d433828c591e8aefdd92255f0608faa75cf7abc16a936d706937669c31d694f` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **0**
- Средняя: **9**
- Низкая: **0**
- Информационная: **0**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 0
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 9
- Рекомендация по улучшению: 0
- Недостаточность данных: 0

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

Проверка аналитика: подтверждено — 9, не применимо — 0, отклонено как ложные срабатывания — 0.

**Постквантовая зрелость: Уровень 1 из 4 — постквантовый код есть, но не подключён.** Следующий шаг: Подключите имеющийся постквантовый примитив к критичному пути (обёртка ключей или канал) в гибридной схеме и проверьте совместимость.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/coinbase/cb-mpc> @ `0b716706f998633912ee2be9b9bf8909aed66088` — ссылки в доказательствах открывают строки на этом коммите.

174 файлов, всего 1453052 байт, редактирований: 0; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 174 | include/cbmpc/api/curve.h: 14 lines scanned with 16 rule patterns and 123 registry patterns; include/cbmpc/api/ecdsa_2p.h: 88 lines scanned with 16 rule patterns and 123 registry patterns; include/cbmpc/api/ecdsa_mp.h: 134 lines scanned with 16 rule patterns and 123 registry patterns |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree coinbase-cb-mpc at 0b716706f998633912ee2be9b9bf8909aed66088. 174 files analysed; of 182 files, 0 are test, fuzzing, benchmark or example code and were left out, 8 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **100** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 85.4%

## 7. Подробное описание находок

### QSI-2026-06433 — Квантово-уязвимый ECDH: обёртка ключей и шифрование хранимых данных (5 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** The highest-urgency class in this repository, and it is not signing. The anchors are the publicly verifiable encryption paths — include-internal/cbmpc/internal/protocol/pve_base.h:213 calls prv_key.ecdh(...) and checks a 32-byte output, and src/cbmpc/api/{pve_base_pke,pve_batch_ac, pve_batch_single_recipient}.cpp plus pve_internal.h:154 all guard on "missing HSM ECIES ECDH callback". PVE is how key shares are encrypted to a recipient for backup and escrow, so the ciphertexts are stored. Harvest-now-decrypt-later applies in full: a copy taken today of an encrypted share set becomes plaintext once a CRQC exists, and no later migration undoes that. Unlike a signature scheme, this can be fixed today by wrapping the share under a hybrid KEM, which makes it the first thing to do rather than the hardest — and nearer than it looks, because this repository already implements ML-KEM-768 without the PVE path using it. See the DEP-NO-PQC-LIBRARY decision below.
- Затронутый актив: `source-code:ECDH:key_wrapping`
- Источник данных: include-internal/cbmpc/internal/protocol/pve_base.h
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:55 UTC
- Балл приоритета: 43.4 / 100
- CVSS v3.1: неприменимо

5 упоминаний ECDH в 5 файл(ах), например include-internal/cbmpc/internal/protocol/pve_base.h:213. Роль по путям, именам функций и соседнему коду: обёртка ключей и шифрование хранимых данных. Ключи или данные, зашифрованные на эти открытые ключи, хранятся: кто скопирует их сейчас, расшифрует, когда появится CRQC («собери сейчас — расшифруй потом»).

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте include-internal/cbmpc/internal/protocol/pve_base.h:213 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [include-internal/cbmpc/internal/protocol/pve_base.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/pve_base.h#L213) · line 213 · SHA-256 02f0b0e2dc3db13d04880ba70b571232395b33294953c92a27a9d136fc05fe94_

```
  212 |     if (rv = prv_key.ecdh(prv_key.ctx, prv_key.dk_handle, kem_ct, dh)) return rv;
  213 |     if (dh.size() != 32) return coinbase::error(E_CRYPTO, "invalid ECDH output size");
  214 | 
```

_file_excerpt · [src/cbmpc/api/pve_base_pke.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/pve_base_pke.cpp#L325) · line 325 · SHA-256 7a1b1fff636e81f0627ac69da87fc93e1fcf0bf121c4e2297b0718d39ddb0d34_

```
  324 |   if (const error_t rv = coinbase::api::detail::validate_mem_arg(label, "label")) return rv;
  325 |   if (!cb.ecdh) return coinbase::error(E_BADARG, "missing HSM ECIES ECDH callback");
  326 | 
```

_file_excerpt · [src/cbmpc/api/pve_batch_ac.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/pve_batch_ac.cpp#L308) · line 308 · SHA-256 8e385b276c3dbb900f226e3840ad803a3463b08dc1a1f91ea262250d1691cba0_

```
  307 |   if (const error_t rv = coinbase::api::detail::validate_mem_arg(label, "label")) return rv;
  308 |   if (!cb.ecdh) return coinbase::error(E_BADARG, "missing HSM ECIES ECDH callback");
  309 | 
```

_file_excerpt · [src/cbmpc/api/pve_batch_single_recipient.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/pve_batch_single_recipient.cpp#L225) · line 225 · SHA-256 862c1cebf150e17798084f5554fc57ca003f1addc2df7e382327442969d14396_

```
  224 |   if (const error_t rv = coinbase::api::detail::validate_mem_arg(label, "label")) return rv;
  225 |   if (!cb.ecdh) return coinbase::error(E_BADARG, "missing HSM ECIES ECDH callback");
  226 | 
```

_file_excerpt · [src/cbmpc/api/pve_internal.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/pve_internal.h#L154) · line 154 · SHA-256 3fa55d0a81efe46a0c8448fd5d5943231913648274934d50546cae7b9f2196fc_

```
  153 |   error_t decrypt(mem_t dk_handle, mem_t label, mem_t ct, buf_t& out_plain) const override {
  154 |     if (!cb_.ecdh) return coinbase::error(E_BADARG, "missing HSM ECIES ECDH callback");
  155 |     coinbase::mpc::pve_ecies_p256_hsm_dk_t dk;
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Оборачивайте ключи ML-KEM или гибридным KEM (X25519 + ML-KEM-768) и переоберните хранимые ключи; для данных, которые уже могли скопировать, нужна отдельная оценка.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06430 — Квантово-уязвимый Threshold ECDSA: пороговая подпись и протоколы MPC (13 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** The claim is right — cb-mpc is a threshold ECDSA library and these 13 files are its protocol surface (api/ecdsa_2p.h, api/ecdsa_mp.h, internal/protocol/ecdsa_2p.h, ecdsa_mp.h, hd_keyset_ecdsa_2p.h) — but the cited evidence is weaker than the claim and a reader should know which is which. Most anchors are namespace declarations and their closing braces (namespace coinbase::api::ecdsa_2p, coinbase::mpc::ecdsampc), so the row follows from the library's purpose rather than from the quoted line. The substantive evidence for this class is in the Paillier and Pedersen rows above, which cite implementations. Confirmed on that basis, and the detector would serve better by anchoring on the protocol functions.
- Затронутый актив: `source-code:Threshold ECDSA:threshold_mpc`
- Источник данных: include/cbmpc/api/ecdsa_2p.h
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:55 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

102 упоминаний Threshold ECDSA в 13 файл(ах), например include/cbmpc/api/ecdsa_2p.h:12. Роль по путям, именам функций и соседнему коду: пороговая подпись и протоколы MPC. Paillier, обязательства Педерсена и доказательства на дискретном логарифме внутри пороговых ECDSA и EdDSA ломаются алгоритмом Шора; постквантовая пороговая схема — это смена протокола, а не параметра.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте include/cbmpc/api/ecdsa_2p.h:12 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [include/cbmpc/api/ecdsa_2p.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include/cbmpc/api/ecdsa_2p.h#L12) · line 12 · SHA-256 a78ce67e456bbade8e40693fbf9637650f04faa2e8891063ddeebead353fb6a4_

```
   11 | 
   12 | namespace coinbase::api::ecdsa_2p {
   13 | 
```

_file_excerpt · [include/cbmpc/api/ecdsa_2p.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include/cbmpc/api/ecdsa_2p.h#L88) · line 88 · SHA-256 2a83480fd5d03e50bebb35352c4cb14708fc498793961d1a8abf5db9ca7dc16f_

```
   87 | 
   88 | }  // namespace coinbase::api::ecdsa_2p
```

_file_excerpt · [include/cbmpc/api/ecdsa_mp.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include/cbmpc/api/ecdsa_mp.h#L15) · line 15 · SHA-256 eb3d5758c2755f9f5a315a84c4a64733cdf65c78f998b14de387f2616daa1a7e_

```
   14 | // requirements.
   15 | namespace coinbase::api::ecdsa_mp {
   16 | 
```

_file_excerpt · [include/cbmpc/api/ecdsa_mp.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include/cbmpc/api/ecdsa_mp.h#L134) · line 134 · SHA-256 6496220e2d3584960750a9402b32c82c32f580a8ea5e20a24637f04899b245f3_

```
  133 | 
  134 | }  // namespace coinbase::api::ecdsa_mp
```

_file_excerpt · [include-internal/cbmpc/internal/protocol/ecdsa_2p.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/ecdsa_2p.h#L10) · line 10 · SHA-256 4f07cdced92dd607c8b26f039382244c79cc890b96ad3e8306460858c0624a71_

```
    9 | 
   10 | namespace coinbase::mpc::ecdsa2pc {
   11 | 
```

_file_excerpt · [include-internal/cbmpc/internal/protocol/ecdsa_2p.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/ecdsa_2p.h#L122) · line 122 · SHA-256 eb44feaab487c80962c7a431cfbdf3361a9a37156029f2ec3d6219b7557e915a_

```
  121 | 
  122 | }  // namespace coinbase::mpc::ecdsa2pc
```

_file_excerpt · [include-internal/cbmpc/internal/protocol/ecdsa_mp.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/ecdsa_mp.h#L9) · line 9 · SHA-256 867210bf6da87290b3d8ca0486277ad9893eb8ba3d71cb1b0f72a3e135e96501_

```
    8 | 
    9 | namespace coinbase::mpc::ecdsampc {
   10 | 
```

_file_excerpt · [include-internal/cbmpc/internal/protocol/ecdsa_mp.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/ecdsa_mp.h#L129) · line 129 · SHA-256 1733ee2e1cb11d10a703f1fc869b155110678b46904534af78db5ddd3532d328_

```
  128 | 
  129 | }  // namespace coinbase::mpc::ecdsampc
```

_file_excerpt · [include-internal/cbmpc/internal/protocol/hd_keyset_ecdsa_2p.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/hd_keyset_ecdsa_2p.h#L3) · line 3 · SHA-256 219e8141fa597210bbafd00b034030aa8b243102ba810d0f7e1e7bb72f64d035_

```
    2 | #include <cbmpc/internal/protocol/ec_dkg.h>
    3 | #include <cbmpc/internal/protocol/ecdsa_2p.h>
    4 | #include <cbmpc/internal/protocol/hd_tree_bip32.h>
```

_file_excerpt · [include-internal/cbmpc/internal/protocol/hd_keyset_ecdsa_2p.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/hd_keyset_ecdsa_2p.h#L29) · line 29 · SHA-256 a5b11e730725f1172506a636b59dc27320599bd992208ea7d2320c00d8558da0_

```
   28 |                              const std::vector<bip32_path_t>& non_hardened_paths, buf_t& sid,
   29 |                              std::vector<ecdsa2pc::key_t>& derived_keys);
   30 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06431 — Квантово-уязвимый Ed25519: пороговая подпись и протоколы MPC (8 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Threshold EdDSA, which the library implements alongside threshold ECDSA: api/eddsa_2p.h, internal/protocol/eddsa.h (which includes schnorr_mp.h), hd_keyset_eddsa_2p.h and src/cbmpc/api/eddsa2pc.cpp, where blob_to_key validates the key blob role. Same conclusion as threshold ECDSA and the same caveat about namespace anchors; the protocol is a Schnorr-style multiparty scheme over Ed25519, so Shor breaks both the signature and the discrete-log proofs around it.
- Затронутый актив: `source-code:Ed25519:threshold_mpc`
- Источник данных: include/cbmpc/api/eddsa_2p.h
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:55 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

37 упоминаний Ed25519 в 8 файл(ах), например include/cbmpc/api/eddsa_2p.h:8. Роль по путям, именам функций и соседнему коду: пороговая подпись и протоколы MPC. Paillier, обязательства Педерсена и доказательства на дискретном логарифме внутри пороговых ECDSA и EdDSA ломаются алгоритмом Шора; постквантовая пороговая схема — это смена протокола, а не параметра.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте include/cbmpc/api/eddsa_2p.h:8 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [include/cbmpc/api/eddsa_2p.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include/cbmpc/api/eddsa_2p.h#L8) · line 8 · SHA-256 c37e0dee9fd8cf516ded4812f075b46479e94f71599bc145a46dd68978c6e49a_

```
    7 | 
    8 | namespace coinbase::api::eddsa_2p {
    9 | 
```

_file_excerpt · [include/cbmpc/api/eddsa_2p.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include/cbmpc/api/eddsa_2p.h#L79) · line 79 · SHA-256 1870990aac8e55e075d1ff1db55dfa554b8413e8081ccb3390a7b886119d2065_

```
   78 | 
   79 | }  // namespace coinbase::api::eddsa_2p
```

_file_excerpt · [include-internal/cbmpc/internal/protocol/eddsa.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/eddsa.h#L6) · line 6 · SHA-256 3c84aa793ed1f42936617a69b2658887b6d94795e53413cf8e15161241b933e1_

```
    5 | #include <cbmpc/internal/protocol/schnorr_mp.h>
    6 | namespace coinbase::mpc::eddsa2pc {
    7 | 
```

_file_excerpt · [include-internal/cbmpc/internal/protocol/eddsa.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/eddsa.h#L14) · line 14 · SHA-256 b312965fb62a137d3aae3bf51910e3d5803f05ece5bcf33078f902aa3dca78bc_

```
   13 | 
   14 | }  // namespace coinbase::mpc::eddsa2pc
   15 | 
```

_file_excerpt · [include-internal/cbmpc/internal/protocol/hd_keyset_eddsa_2p.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/hd_keyset_eddsa_2p.h#L26) · line 26 · SHA-256 ef05e73154048d3043c22b41a17397906767a18a0b8cf741d1cf1948271555b7_

```
   25 |                              const std::vector<bip32_path_t>& non_hardened_paths, buf_t& sid,
   26 |                              std::vector<eddsa2pc::key_t>& derived_keys);
   27 | 
```

_file_excerpt · [src/cbmpc/api/eddsa2pc.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/eddsa2pc.cpp#L1) · line 1 · SHA-256 0d8efb61e1de8ae34931c96eb484fc2f9c4ff617d0efa53fce450b3b65181ee8_

```
    1 | #include <cbmpc/api/eddsa_2p.h>
    2 | #include <cbmpc/internal/core/convert.h>
```

_file_excerpt · [src/cbmpc/api/eddsa2pc.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/eddsa2pc.cpp#L8) · line 8 · SHA-256 c37e0dee9fd8cf516ded4812f075b46479e94f71599bc145a46dd68978c6e49a_

```
    7 | 
    8 | namespace coinbase::api::eddsa_2p {
    9 | 
```

_file_excerpt · [src/cbmpc/api/eddsa2pc.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/eddsa2pc.cpp#L29) · line 29 · SHA-256 bebfad4c5352b665f0c5800512a735abd85c681f783086cf92dba60c0981bfd3_

```
   28 | 
   29 | static error_t blob_to_key(const key_blob_v1_t& blob, coinbase::mpc::eddsa2pc::key_t& key) {
   30 |   if (blob.role > 1) return coinbase::error(E_FORMAT, "invalid key blob role");
```

_file_excerpt · [src/cbmpc/api/hd_keyset_eddsa_2p.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/hd_keyset_eddsa_2p.cpp#L23) · line 23 · SHA-256 f5e7d1db58a72a542c853835f4f649afc616439e30444f917e9a5345e966b936_

```
   22 | // Mirror of the `coinbase::api::eddsa_2p` key blob format (see `src/cbmpc/api/eddsa2pc.cpp`).
   23 | constexpr uint32_t eddsa2pc_key_blob_version_v1 = 1;
   24 | struct eddsa2pc_key_blob_v1_t {
```

_file_excerpt · [src/cbmpc/api/hd_keyset_eddsa_2p.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/hd_keyset_eddsa_2p.cpp#L24) · line 24 · SHA-256 b14eb05d04888ba3a76cb7c9a40d1ecaabd069bdadb57f2e0c8ec39f5b5a59b2_

```
   23 | constexpr uint32_t eddsa2pc_key_blob_version_v1 = 1;
   24 | struct eddsa2pc_key_blob_v1_t {
   25 |   uint32_t version = eddsa2pc_key_blob_version_v1;
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06432 — Квантово-уязвимый Paillier: пороговая подпись и протоколы MPC (15 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Correct, with a parameter worth quoting: include-internal/cbmpc/internal/crypto/base_paillier.h declares class paillier_t with static constexpr int bit_size = 2048, so the modulus is 2048 bits and Shor's algorithm faces exactly the problem it faces for RSA-2048. The evidence is real implementation rather than a name match — base_paillier.h, zk/zk_paillier.h's valid_paillier_t, and the key structures in protocol/ecdsa_2p.h and hd_keyset_ecdsa_2p.h, which each hold a crypto::paillier_t and its c_key. This is the row that a post-quantum *signature* standard does not help with: Paillier is the homomorphic encryption the two-party ECDSA protocol is built on, so replacing it is a protocol redesign, and NIST's 2024 standards (ML-DSA, SLH-DSA) are single-signer schemes that do not offer a drop-in replacement.
- Затронутый актив: `source-code:Paillier:threshold_mpc`
- Источник данных: include-internal/cbmpc/internal/crypto/base_bn.h
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:55 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

352 упоминаний Paillier в 15 файл(ах), например include-internal/cbmpc/internal/crypto/base_bn.h:46. Роль по путям, именам функций и соседнему коду: пороговая подпись и протоколы MPC. Paillier, обязательства Педерсена и доказательства на дискретном логарифме внутри пороговых ECDSA и EdDSA ломаются алгоритмом Шора; постквантовая пороговая схема — это смена протокола, а не параметра.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте include-internal/cbmpc/internal/crypto/base_bn.h:46 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [include-internal/cbmpc/internal/crypto/base_bn.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/crypto/base_bn.h#L46) · line 46 · SHA-256 5b3069a225ca12ea3e28ab0aeabfda51b549f1b3b9d656edc897fe7e8f531eb7_

```
   45 | class mod_t;
   46 | class paillier_t;
   47 | class ecdsa_signature_t;
```

_file_excerpt · [include-internal/cbmpc/internal/crypto/base_bn.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/crypto/base_bn.h#L57) · line 57 · SHA-256 ee1680c40ae2e30e376737e08f755915785323d13d53983ed66744973fc95d78_

```
   56 |   friend class crypto::ecc_point_t;
   57 |   friend class crypto::paillier_t;
   58 |   friend class crypto::ecdsa_signature_t;
```

_file_excerpt · [include-internal/cbmpc/internal/crypto/base_paillier.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/crypto/base_paillier.h#L8) · line 8 · SHA-256 5e4a09314f2cd39ed8e8283c855838bd6ca755c5868d316db91eee3d56ad4bfe_

```
    7 | 
    8 | class paillier_t {
    9 |  public:
```

_file_excerpt · [include-internal/cbmpc/internal/crypto/base_paillier.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/crypto/base_paillier.h#L29) · line 29 · SHA-256 5f18c9d760a32724c050c5db7a67fbc655776bda0da0b20a58aad0bee1772158_

```
   28 |   static constexpr int bit_size = 2048;
   29 |   paillier_t() : has_private(false) {}
   30 |   ~paillier_t() {}
```

_file_excerpt · [include-internal/cbmpc/internal/crypto/base_paillier.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/crypto/base_paillier.h#L30) · line 30 · SHA-256 0cb26e46930009ca686d8c0d8cf27ded9d756b290f72260c02b479de1d9e13b7_

```
   29 |   paillier_t() : has_private(false) {}
   30 |   ~paillier_t() {}
   31 | 
```

_file_excerpt · [include-internal/cbmpc/internal/protocol/ecdsa_2p.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/ecdsa_2p.h#L18) · line 18 · SHA-256 ca851b698b030d5580b83a036c3c776223f359db508a167eef1d501155655ee7_

```
   17 |   bn_t c_key;
   18 |   crypto::paillier_t paillier;
   19 | };
```

_file_excerpt · [include-internal/cbmpc/internal/protocol/ecdsa_2p.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/ecdsa_2p.h#L66) · line 66 · SHA-256 0986d849de59c959f92b00dd88d412729fbe9ff0da5f142cd1c1029e0b413f96_

```
   65 |  */
   66 | struct paillier_gen_interactive_t {
   67 |   paillier_gen_interactive_t(const crypto::mpc_pid_t& pid) : range(pid), equal(pid) {}
```

_file_excerpt · [include-internal/cbmpc/internal/protocol/ecdsa_2p.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/ecdsa_2p.h#L67) · line 67 · SHA-256 220d61e7527123b6ac429da5f9c81c381cf521d6a0dd872c9c236eaef82f0b4b_

```
   66 | struct paillier_gen_interactive_t {
   67 |   paillier_gen_interactive_t(const crypto::mpc_pid_t& pid) : range(pid), equal(pid) {}
   68 | 
```

_file_excerpt · [include-internal/cbmpc/internal/protocol/hd_keyset_ecdsa_2p.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/protocol/hd_keyset_ecdsa_2p.h#L11) · line 11 · SHA-256 6626153477cce1abe743ecfb348e91e140577229a70e4d4dc32b35e698ff2be1_

```
   10 |   hd_root_t root;
   11 |   coinbase::crypto::paillier_t paillier;
   12 |   bn_t c_key;
```

_file_excerpt · [include-internal/cbmpc/internal/zk/zk_paillier.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/zk/zk_paillier.h#L9) · line 9 · SHA-256 b73ec02d5359acd4ea08e3bf49c6d23136c6a5d7bc3ff5e36548fa2c2dd8a7e1_

```
    8 | struct valid_paillier_t {
    9 |   using param = paillier_non_interactive_param_t;
   10 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06434 — Квантово-уязвимый Pedersen commitment: пороговая подпись и протоколы MPC (4 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Correct and anchored on real parameter generation, not a mention: src/cbmpc/zk/zk_pedersen.cpp constructs pedersen_commitment_params_t with primes generated via BN_generate_prime_ex (the comment names the OpenSSL function), zk_pedersen.h:13 exposes get() and check_safe_prime_subgroup, and both src/cbmpc/protocol/ecdsa_2p.cpp:28 and src/cbmpc/zk/zk_paillier.cpp:537 pull those parameters. Stated precisely, because the distinction decides how bad this is: breaking the discrete log costs a Pedersen commitment its *binding* property, not its hiding — the commitment is perfectly hiding, so no committed value is recoverable from it even with a CRQC. The exposure is forgeability inside the proofs, i.e. future protocol soundness, not retroactive disclosure.
- Затронутый актив: `source-code:Pedersen commitment:threshold_mpc`
- Источник данных: include-internal/cbmpc/internal/zk/zk_pedersen.h
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:55 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

21 упоминаний Pedersen commitment в 4 файл(ах), например include-internal/cbmpc/internal/zk/zk_pedersen.h:8. Роль по путям, именам функций и соседнему коду: пороговая подпись и протоколы MPC. Paillier, обязательства Педерсена и доказательства на дискретном логарифме внутри пороговых ECDSA и EdDSA ломаются алгоритмом Шора; постквантовая пороговая схема — это смена протокола, а не параметра.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте include-internal/cbmpc/internal/zk/zk_pedersen.h:8 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [include-internal/cbmpc/internal/zk/zk_pedersen.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/zk/zk_pedersen.h#L8) · line 8 · SHA-256 90f6fa4e7aa38c51851aec3f52cc5042b5a7d6cb58864e285ff27920ae55dc2c_

```
    7 | 
    8 | struct pedersen_commitment_params_t {
    9 |   mod_t p, p_tag;
```

_file_excerpt · [include-internal/cbmpc/internal/zk/zk_pedersen.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/zk/zk_pedersen.h#L13) · line 13 · SHA-256 beb6763be217e297856056988084ecbeb400ac2d7bf25b188e8104b30088b1a4_

```
   12 | 
   13 |   static const pedersen_commitment_params_t& get();
   14 |   error_t check_safe_prime_subgroup(const bn_t& x) const;
```

_file_excerpt · [include-internal/cbmpc/internal/zk/zk_pedersen.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/zk/zk_pedersen.h#L17) · line 17 · SHA-256 4a5620026d361a84899501efab6d448f6aaca1ec3470c5f81cf65597c77a20af_

```
   16 |  private:
   17 |   pedersen_commitment_params_t();
   18 | };
```

_file_excerpt · [src/cbmpc/protocol/ecdsa_2p.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/protocol/ecdsa_2p.cpp#L28) · line 28 · SHA-256 f6cd7432a9262739e96d7886c92f3c7506f35897ea1c58e6393e83e81e34c51c_

```
   27 | 
   28 |   const zk::pedersen_commitment_params_t& params = zk::pedersen_commitment_params_t::get();
   29 |   const mod_t& p_tag = params.p_tag;
```

_file_excerpt · [src/cbmpc/zk/zk_paillier.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/zk/zk_paillier.cpp#L537) · line 537 · SHA-256 cebe585f3f001af319bb63895f689e137cb8b6b68d327245e8efe2611a1a8f4f_

```
  536 |                                        const bn_t& r, mem_t session_id, uint64_t aux) {
  537 |   const pedersen_commitment_params_t& params = pedersen_commitment_params_t::get();
  538 |   const mod_t& p_tag = params.p_tag;
```

_file_excerpt · [src/cbmpc/zk/zk_pedersen.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/zk/zk_pedersen.cpp#L6) · line 6 · SHA-256 edeeb6e35af2f2dfeb59c3d504b58d0c9676130e51cab7743e716f1b20fe1dc9_

```
    5 | 
    6 | pedersen_commitment_params_t::pedersen_commitment_params_t() {
    7 |   // this was generated using https://www.openssl.org/docs/man1.1.1/man3/BN_generate_prime_ex.html
```

_file_excerpt · [src/cbmpc/zk/zk_pedersen.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/zk/zk_pedersen.cpp#L39) · line 39 · SHA-256 59b6c7a5b07fdfda0bfbf3c3cf9123cee14bec4790d944ee6da5b7441f752acd_

```
   38 | 
   39 | const pedersen_commitment_params_t& pedersen_commitment_params_t::get() {
   40 |   static pedersen_commitment_params_t params;
```

_file_excerpt · [src/cbmpc/zk/zk_pedersen.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/zk/zk_pedersen.cpp#L40) · line 40 · SHA-256 ad78a5b9a922f859724ed7a18381e655d3c93f4063474ab5e7f8364521d0a4c2_

```
   39 | const pedersen_commitment_params_t& pedersen_commitment_params_t::get() {
   40 |   static pedersen_commitment_params_t params;
   41 |   return params;
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06435 — Квантово-уязвимый ECDSA: пороговая подпись и протоколы MPC (3 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Plain (non-threshold) ECDSA on secp256k1 inside the Schnorr two-party API: src/cbmpc/api/schnorr2pc.cpp:31 and :48 validate and write blob.curve against curve_id::secp256k1 and serialise key.Q compressed. Key-blob handling for the signing keys, so the same migration item as the threshold rows; counted separately because it is the serialisation format, which is where a migration needs a version bump.
- Затронутый актив: `source-code:ECDSA:threshold_mpc`
- Источник данных: src/cbmpc/api/schnorr2pc.cpp
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:55 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

17 упоминаний ECDSA в 3 файл(ах), например src/cbmpc/api/schnorr2pc.cpp:31. Роль по путям, именам функций и соседнему коду: пороговая подпись и протоколы MPC. Paillier, обязательства Педерсена и доказательства на дискретном логарифме внутри пороговых ECDSA и EdDSA ломаются алгоритмом Шора; постквантовая пороговая схема — это смена протокола, а не параметра.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/cbmpc/api/schnorr2pc.cpp:31 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/cbmpc/api/schnorr2pc.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/schnorr2pc.cpp#L31) · line 31 · SHA-256 781d30e36a4e8dc2b8788c3413940215330fa9c99e7ede1cd51753e82cd69e8b_

```
   30 |   if (blob.role > 1) return coinbase::error(E_FORMAT, "invalid key blob role");
   31 |   if (static_cast<curve_id>(blob.curve) != curve_id::secp256k1)
   32 |     return coinbase::error(E_FORMAT, "invalid key blob curve");
```

_file_excerpt · [src/cbmpc/api/schnorr2pc.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/schnorr2pc.cpp#L48) · line 48 · SHA-256 70c0040ad2b59e8fc028bfe2b304bf1e5c190dcd9bd81c45122946853180c247_

```
   47 |   blob.role = static_cast<uint32_t>(key.role);
   48 |   blob.curve = static_cast<uint32_t>(curve_id::secp256k1);
   49 |   blob.Q_compressed = key.Q.to_compressed_bin();
```

_file_excerpt · [src/cbmpc/api/schnorr2pc.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/schnorr2pc.cpp#L67) · line 67 · SHA-256 8e0b65f6eab20ce3e7beabdf092159341fdbb8bce48e0965e1137569baf42221_

```
   66 |   if (const error_t rv = validate_job_2p(job)) return rv;
   67 |   if (curve != curve_id::secp256k1) return coinbase::error(E_BADARG, "unsupported curve");
   68 | 
```

_file_excerpt · [src/cbmpc/api/schnorr_mp.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/schnorr_mp.cpp#L46) · line 46 · SHA-256 6b5c5538004c224df21888f2ab7eb3b2283655671ec668e89d3b4466ff0cda99_

```
   45 |     return coinbase::error(E_FORMAT, "unsupported key blob version");
   46 |   if (static_cast<curve_id>(blob.curve) != curve_id::secp256k1)
   47 |     return coinbase::error(E_FORMAT, "invalid key blob curve");
```

_file_excerpt · [src/cbmpc/api/schnorr_mp.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/schnorr_mp.cpp#L71) · line 71 · SHA-256 6082a2958ef6b9148a404e06a13378b5ddeabf80c823bc9a75ba854116a3f8ff_

```
   70 |   blob.version = version;
   71 |   blob.curve = static_cast<uint32_t>(curve_id::secp256k1);
   72 |   blob.party_name = key.party_name;
```

_file_excerpt · [src/cbmpc/api/schnorr_mp.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/schnorr_mp.cpp#L117) · line 117 · SHA-256 516efb19886076797c71fe18d00e39cff6d00e5b16854aee71e290abcf13646c_

```
  116 |     return coinbase::error(E_FORMAT, "unsupported key blob version: " + std::to_string(blob.version));
  117 |   if (static_cast<curve_id>(blob.curve) != curve_id::secp256k1)
  118 |     return coinbase::error(E_FORMAT, "invalid key blob curve");
```

_file_excerpt · [src/cbmpc/protocol/schnorr_2p.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/protocol/schnorr_2p.cpp#L82) · line 82 · SHA-256 6933ccbb7668499bfc93936f9461308c76da160293ca96d96dc726de24666977_

```
   81 |   if (variant == variant_e::BIP340) {
   82 |     if (curve != crypto::curve_secp256k1) return coinbase::error(E_BADARG, "BIP340 variant requires secp256k1 curve");
   83 |     for (int i = 0; i < n_sigs; i++) {
```

_file_excerpt · [src/cbmpc/protocol/schnorr_2p.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/protocol/schnorr_2p.cpp#L136) · line 136 · SHA-256 a382d78dd9af5355999427605a0c64b9d3262c18a6290782f8046e6168e0ee69_

```
  135 |         if (rv = crypto::bip340::verify(pub_key, msgs[i], candidate_sigs[i]))
  136 |           return coinbase::error(rv, "schnorr_2p: secp256k1 verify failed");
  137 |       } else {
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06436 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Plain (non-threshold) ECDSA on secp256k1 inside the Schnorr two-party API: src/cbmpc/api/schnorr2pc.cpp:31 and :48 validate and write blob.curve against curve_id::secp256k1 and serialise key.Q compressed. Key-blob handling for the signing keys, so the same migration item as the threshold rows; counted separately because it is the serialisation format, which is where a migration needs a version bump.
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: src/cbmpc/crypto/base_ecc_secp256k1.cpp
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:55 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

45 упоминаний ECDSA в 1 файл(ах), например src/cbmpc/crypto/base_ecc_secp256k1.cpp:5. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/cbmpc/crypto/base_ecc_secp256k1.cpp:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/cbmpc/crypto/base_ecc_secp256k1.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/crypto/base_ecc_secp256k1.cpp#L5) · line 5 · SHA-256 872667182b513b2fb3be5898f64aee3035d69bc5401c5422a09fa424f8584f27_

```
    4 | // clang-format off
    5 | #include "secp256k1/src/assumptions.h"
    6 | #include "secp256k1/src/field_impl.h"
```

_file_excerpt · [src/cbmpc/crypto/base_ecc_secp256k1.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/crypto/base_ecc_secp256k1.cpp#L6) · line 6 · SHA-256 080665ef1f83af114ec0d02cf611f582583d388fba9861259f38e465461c1f25_

```
    5 | #include "secp256k1/src/assumptions.h"
    6 | #include "secp256k1/src/field_impl.h"
    7 | #include "secp256k1/src/scalar_impl.h"
```

_file_excerpt · [src/cbmpc/crypto/base_ecc_secp256k1.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/crypto/base_ecc_secp256k1.cpp#L7) · line 7 · SHA-256 3fef17948caa87b9d5b3b241d1f94b1459b96d31c44dc1188c4062b13cf9419f_

```
    6 | #include "secp256k1/src/field_impl.h"
    7 | #include "secp256k1/src/scalar_impl.h"
    8 | #include "secp256k1/src/scratch_impl.h"
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06429 — Квантово-уязвимый ECDSA: роль не определена (6 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Plain (non-threshold) ECDSA on secp256k1 inside the Schnorr two-party API: src/cbmpc/api/schnorr2pc.cpp:31 and :48 validate and write blob.curve against curve_id::secp256k1 and serialise key.Q compressed. Key-blob handling for the signing keys, so the same migration item as the threshold rows; counted separately because it is the serialisation format, which is where a migration needs a version bump.
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: include/cbmpc/api/curve.h
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:55 UTC
- Балл приоритета: 40.2 / 100
- CVSS v3.1: неприменимо

12 упоминаний ECDSA в 6 файл(ах), например include/cbmpc/api/curve.h:9. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте include/cbmpc/api/curve.h:9 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [include/cbmpc/api/curve.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include/cbmpc/api/curve.h#L9) · line 9 · SHA-256 8bc94e0040057c98486af0d2761abfd6ed943aa9547cb545354de9757f6294a4_

```
    8 | enum class curve_id : uint32_t {
    9 |   p256 = 1,       // NIST P-256 (aka prime256v1 / secp256r1)
   10 |   secp256k1 = 2,  // secp256k1
```

_file_excerpt · [include/cbmpc/api/curve.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include/cbmpc/api/curve.h#L10) · line 10 · SHA-256 0eb2996e7229d0e76b10f0da6cc1353d0ed4e76d9997664d08fa47e679e42bdc_

```
    9 |   p256 = 1,       // NIST P-256 (aka prime256v1 / secp256r1)
   10 |   secp256k1 = 2,  // secp256k1
   11 |   ed25519 = 3,    // Edwards25519
```

_file_excerpt · [include-internal/cbmpc/internal/crypto/base_ecc.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/crypto/base_ecc.h#L17) · line 17 · SHA-256 1acb65be89f9287ebf0f9fdd748084d46a04587d02e8e23bd77cb5aac0bae1a6_

```
   16 | 
   17 | namespace secp256k1 {
   18 | typedef struct point_t* point_ptr_t;
```

_file_excerpt · [include-internal/cbmpc/internal/crypto/base_ecc.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/crypto/base_ecc.h#L177) · line 177 · SHA-256 32e38a7fe938b9f819247a3f2b8f4009a857ae01cfb18dc6643580cb273c559f_

```
  176 |   explicit ecc_point_t(ecurve_t curve, const ecp_storage_t& storage);
  177 |   explicit ecc_point_t(const secp256k1::point_ptr_t p);
  178 | 
```

_file_excerpt · [include-internal/cbmpc/internal/crypto/base_ecc.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/include-internal/cbmpc/internal/crypto/base_ecc.h#L246) · line 246 · SHA-256 d6d38a0587aa30e2f8e219bbeb332a262f5d6e28c8f16c55803bbb011c8e1f62_

```
  245 |     EC_POINT* ptr = nullptr;
  246 |     secp256k1::point_ptr_t secp256k1;
  247 |     ecp_storage_t* storage;
```

_file_excerpt · [src/cbmpc/api/curve_util.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/curve_util.h#L13) · line 13 · SHA-256 4a75918a0824abc51d4df2f3b0053de2ad333c16fee4e66dc47eac2b874a1d67_

```
   12 |       return coinbase::crypto::curve_p256;
   13 |     case curve_id::secp256k1:
   14 |       return coinbase::crypto::curve_secp256k1;
```

_file_excerpt · [src/cbmpc/api/curve_util.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/api/curve_util.h#L30) · line 30 · SHA-256 ea0e22518060778a7a9df31ae979e7d72520b1fc3bebb5996fceb10bd64d2d91_

```
   29 |   if (curve == coinbase::crypto::curve_secp256k1) {
   30 |     out = curve_id::secp256k1;
   31 |     return true;
```

_file_excerpt · [src/cbmpc/c_api/util.h](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/c_api/util.h#L79) · line 79 · SHA-256 e7c477a077d0efbf921de86527e4f38cd37dec90e2fabbe063db58c2e9e90c3e_

```
   78 |     case CBMPC_CURVE_SECP256K1:
   79 |       out = coinbase::api::curve_id::secp256k1;
   80 |       return CBMPC_SUCCESS;
```

_file_excerpt · [src/cbmpc/crypto/base_ecc.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/crypto/base_ecc.cpp#L673) · line 673 · SHA-256 59055bc4efcd046ef6d49e3274cfc060c68a3620ea7436b2d76a3df41d2eaf5e_

```
  672 | 
  673 | namespace secp256k1 {
  674 | point_ptr_t new_point(const point_ptr_t);
```

_file_excerpt · [src/cbmpc/crypto/base_ecc.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/crypto/base_ecc.cpp#L677) · line 677 · SHA-256 8996735a795dea2a0988f9d89bf72c598a082466689a5c52c129920ca48e0c74_

```
  676 | 
  677 | ecc_point_t::ecc_point_t(const secp256k1::point_ptr_t p)
  678 |     : curve(curve_secp256k1)  // NOLINT:cppcoreguidelines-pro-type-member-init
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06437 — Квантово-уязвимый RSA: роль не определена (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Role resolved. src/cbmpc/crypto/base_rsa.cpp implements rsa_pub_key_t with encrypt_raw (deliberately RSA_NO_PADDING, because it is a primitive for a higher-level scheme rather than a general-purpose encryption API), verify_pkcs1, and EVP_RSA_gen(bits) for generation. It is included by internal/crypto/base_pki.h and internal/crypto/base_paillier.h and exercised by tests/unit/api/test_pve.cpp, so this is the PKI layer underneath publicly verifiable encryption and the modulus arithmetic that Paillier is built on. Same quantum exposure as the Paillier row, for the same reason: Shor factors the composite modulus. Because PVE ciphertexts are stored, this inherits the harvest-now-decrypt-later urgency of the ECDH row rather than the lower urgency of a signing path.
- Затронутый актив: `source-code:RSA:general`
- Источник данных: src/cbmpc/crypto/base_rsa.cpp
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:55 UTC
- Балл приоритета: 40.2 / 100
- CVSS v3.1: неприменимо

2 упоминаний RSA в 1 файл(ах), например src/cbmpc/crypto/base_rsa.cpp:96. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/cbmpc/crypto/base_rsa.cpp:96 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/cbmpc/crypto/base_rsa.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/crypto/base_rsa.cpp#L96) · line 96 · SHA-256 db6acbfbb01b1b6b2b382dc3e96fd9dbe38bd0d17244c79529f41f8bba9128ae_

```
   95 | 
   96 |   if (EVP_PKEY_id(pkey) != EVP_PKEY_RSA) {
   97 |     // Handle error: Not an RSA key
```

_file_excerpt · [src/cbmpc/crypto/base_rsa.cpp](https://github.com/coinbase/cb-mpc/blob/0b716706f998633912ee2be9b9bf8909aed66088/src/cbmpc/crypto/base_rsa.cpp#L201) · line 201 · SHA-256 2a07b530bd9526bfbff8696f00367319e11578e9fbdb917f5d310fcc4ba84c53_

```
  200 |   create();
  201 |   ptr = EVP_RSA_gen(bits);
  202 |   cb_assert(ptr);
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.


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

### Постквантовая зрелость: Уровень 1 из 4 — постквантовый код есть, но не подключён

- Есть, но не подключено: ML-KEM — include-internal/cbmpc/internal/crypto/mlkem768.h
- Есть, но не подключено: ML-KEM — src/cbmpc/crypto/mlkem768.cpp
- Только классика — обёртка ключей и шифрование хранимых данных: ECDH (5 файл(ов))

**Следующий шаг:** Подключите имеющийся постквантовый примитив к критичному пути (обёртка ключей или канал) в гибридной схеме и проверьте совместимость.

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **обёртка ключей и шифрование хранимых данных** | ECDH (5) | QSI-2026-06433 | Оборачивайте ключи ML-KEM или гибридным KEM (X25519 + ML-KEM-768) и переоберните хранимые ключи; для данных, которые уже могли скопировать, нужна отдельная оценка |
| **пороговая подпись и протоколы MPC** | Paillier (15), Threshold ECDSA (13), Ed25519 (8), Pedersen commitment (4), ECDSA (3) | QSI-2026-06430, QSI-2026-06431, QSI-2026-06432, QSI-2026-06434, QSI-2026-06435 | Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли |
| **подпись транзакций и сообщений** | ECDSA (1) | QSI-2026-06436 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |
| **роль не определена** | ECDSA (6), RSA (1) | QSI-2026-06429, QSI-2026-06437 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — факторизация | взламывает | Q1 | Paillier (15), RSA (3) | Взламывает RSA при любой длине ключа: более длинный модуль лишь полиномиально повышает стоимость. Планируйте переход на ML-KEM (или гибрид) для установления ключей и ML-DSA / SLH-DSA для подписей; начинайте с ключей, защищающих данные, которые должны оставаться конфиденциальными годами («собери сейчас — расшифруй потом»), и с долгоживущих подписей. |
| Алгоритм Шора — дискретный логарифм в конечных полях | взламывает | Q1 | BN254 (alt_bn128) (2), ElGamal (4) | Взламывает Диффи–Хеллмана в конечных полях и DSA при любом размере. Переводите установление ключей на ML-KEM (на переходный период — гибрид с X25519 или ECDH), подписи — на ML-DSA или SLH-DSA. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | BN254 (alt_bn128) (2), ECDH (5), ECDSA (26), Ed25519 (16), Pedersen commitment (4), Threshold ECDSA (13) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | AES-128 (1), AES-192 (1), AES-256 (1), BLAKE2 (1), HKDF (3), HMAC (1), RIPEMD-160 (1), SHA-1 (1), SHA-2 (2), SHA-3 (1) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | BLAKE2 (1), RIPEMD-160 (1), SHA-1 (1), SHA-2 (2), SHA-3 (1) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |
| Квантовое решетчатое просеивание | учтено в стандартных параметрах | Q1 | ML-KEM (2) | Для ML-KEM и ML-DSA в стандартных наборах параметров ничего менять не нужно. Заявление 2024 года о полиномиальном квантовом алгоритме для LWE отозвано после обнаружения ошибки (см. заявления). |

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
| P3 | QSI-2026-06433 | Внесите использования ECDH в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06430 | Внесите использования Threshold ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06431 | Внесите использования Ed25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06432 | Внесите использования Paillier в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06434 | Внесите использования Pedersen commitment в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06435 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06436 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06429 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06437 | Внесите использования RSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-06433 | Запланируйте миграцию ECDH на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-06430 | Запланируйте миграцию Threshold ECDSA на Схему подписи задаёт блокчейн или проверяющая сторона. Следите за постквантовыми предложениями на уровне сетей и пороговыми постквантовыми подписями (NIST IR 8214C); закладывайте обновление долей ключа и криптогибкость в архитектуру хранения (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Схему подписи задаёт блокчейн или проверяющая сторона. Следите за постквантовыми предложениями на уровне сетей и пороговыми постквантовыми подписями (NIST IR 8214C); закладывайте обновление долей ключа и криптогибкость в архитектуру хранения или гибридной схемы. |
| P4 | QSI-2026-06431 | Запланируйте миграцию Ed25519 на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06432 | Запланируйте миграцию Paillier на Стандартизованной постквантовой замены нет. Планируйте пороговые схемы над постквантовыми подписями по мере их зрелости (пороговый конкурс NIST, IR 8214C) или протоколы без Paillier (на основе забывчивой передачи) (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Стандартизованной постквантовой замены нет. Планируйте пороговые схемы над постквантовыми подписями по мере их зрелости (пороговый конкурс NIST, IR 8214C) или протоколы без Paillier (на основе забывчивой передачи) или гибридной схемы. |
| P4 | QSI-2026-06434 | Запланируйте миграцию Pedersen commitment на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-06435 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06436 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06429 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06437 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |

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

1. A. Becker, L. Ducas, N. Gama, T. Laarhoven — New directions in nearest neighbor searching with applications to lattice sieving (SODA 2016; IACR ePrint 2015/1128) — IACR ePrint. <https://eprint.iacr.org/2015/1128> (peer-reviewed article: classical sieving in 2^{0.292n + o(n)})
2. A. Chailloux, J. Loyer — Lattice sieving via quantum random walks (ASIACRYPT 2021; IACR ePrint 2021/570) — IACR ePrint. <https://eprint.iacr.org/2021/570> (peer-reviewed article: 2^{0.2570d + o(d)}, previously 2^{0.2653d + o(d)} (Laarhoven))
3. A. Chailloux, M. Naya-Plasencia, A. Schrottenloher — An Efficient Quantum Collision Search Algorithm and Implications on Symmetric Cryptography (ASIACRYPT 2017; IACR ePrint 2017/847) — IACR ePrint. <https://eprint.iacr.org/2017/847> (peer-reviewed article: Õ(2^{2n/5}) time, O(n) qubits, Õ(2^{n/5}) classical memory)
4. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
5. C. Gidney — How to factor 2048 bit RSA integers with less than a million noisy qubits (arXiv:2505.15917) — arXiv. <https://arxiv.org/abs/2505.15917> (preprint (2025-05-21): < 1 million noisy qubits, < 1 week, 0.1% gate error, 1 µs surface-code cycle)
6. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
7. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
8. CRYSTALS-Kyber — Algorithm Specifications and Supporting Documentation (round 3, 2021-08-04) — CRYSTALS team. <https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf> (NIST round-3 submission: core-SVP cost 2^{0.292β} classical, 2^{0.265β} quantum; Kyber768 166 quantum bits)
9. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
10. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
11. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
12. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
13. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
14. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
15. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
16. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
17. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
18. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
19. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
20. M. Ekerå, J. Gärtner — A high-level comparison of state-of-the-art quantum algorithms for breaking asymmetric cryptography (arXiv:2405.14381) — arXiv. <https://arxiv.org/abs/2405.14381> (preprint (2024-05-23): Regev-style algorithms show no overall advantage yet for cryptographic RSA and finite-field sizes)
21. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
22. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
23. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
24. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
25. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
26. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
27. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| RIPEMD-160 | RIPEMD-160 |  | слаб классически | устаревающий | 1 | 1 | src/cbmpc/crypto/base_hash.cpp:70 |
| SHA-1 | SHA-1 |  | слаб классически | устаревший | 1 | 1 | src/cbmpc/crypto/base_rsa_oaep.cpp:86 |
| AES-192 | AES-192 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/cbmpc/crypto/base.cpp:126 |
| AES-256 | AES-256 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/cbmpc/crypto/base.cpp:128 |
| HKDF |  |  | сниженный запас (Гровер), одобрен | допустимо | 3 | 3 | include-internal/cbmpc/internal/crypto/base_hash.h:351; include-internal/cbmpc/internal/crypto/base_pki.h:57; src/cbmpc/crypto/base_hash.cpp:212 |
| HMAC |  |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/cbmpc/crypto/base_hash.cpp:146 |
| AES-128 | AES-128 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 1 | 1 | src/cbmpc/crypto/base.cpp:124 |
| BLAKE2 |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 1 | 1 | src/cbmpc/crypto/base_hash.cpp:68 |
| SHA-2 |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 2 | 2 | include-internal/cbmpc/internal/zk/fischlin.h:49; src/cbmpc/crypto/base_hash.cpp:55 |
| SHA-3 |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 1 | 1 | src/cbmpc/crypto/base_hash.cpp:63 |
| ML-KEM | ML-KEM-768 |  | постквантовый | допустимо | 2 | 2 | include-internal/cbmpc/internal/crypto/mlkem768.h; src/cbmpc/crypto/mlkem768.cpp:8 |
| BN254 (alt_bn128) |  |  | уязвим (Шор) | допустимо | 2 | 2 | include-internal/cbmpc/internal/crypto/base_bn256.h; src/cbmpc/crypto/base_bn256.cpp |
| ECDH |  |  | уязвим (Шор) | допустимо | 5 | 5 | include-internal/cbmpc/internal/protocol/pve_base.h:213; src/cbmpc/api/pve_base_pke.cpp:325; src/cbmpc/api/pve_batch_ac.cpp:308 |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 10 | 10 | include-internal/cbmpc/internal/crypto/base_ecc.h:17; include/cbmpc/api/curve.h:10; src/cbmpc/api/curve_util.h:13 |
| ECDSA |  |  | уязвим (Шор) | допустимо | 15 | 15 | include-internal/cbmpc/internal/crypto/base_ecc_secp256k1.h; include-internal/cbmpc/internal/protocol/ecdsa_2p.h; include-internal/cbmpc/internal/protocol/ecdsa_mp.h |
| ECDSA | P-256 |  | уязвим (Шор) | допустимо | 1 | 1 | include/cbmpc/api/curve.h:9 |
| Ed25519 |  |  | уязвим (Шор) | допустимо | 8 | 8 | include-internal/cbmpc/internal/crypto/base_eddsa.h; include/cbmpc/api/eddsa_mp.h; include/cbmpc/api/hd_keyset_eddsa_2p.h |
| Ed25519 | Ed25519 |  | уязвим (Шор) | допустимо | 8 | 8 | include-internal/cbmpc/internal/protocol/eddsa.h:6; include-internal/cbmpc/internal/protocol/hd_keyset_eddsa_2p.h:26; include/cbmpc/api/eddsa_2p.h:8 |
| ElGamal |  |  | уязвим (Шор) | устаревший | 4 | 4 | include-internal/cbmpc/internal/crypto/elgamal.h; include-internal/cbmpc/internal/zk/zk_elgamal_com.h; src/cbmpc/crypto/elgamal.cpp |
| Paillier |  |  | уязвим (Шор) | допустимо | 15 | 15 | include-internal/cbmpc/internal/crypto/base_bn.h:46; include-internal/cbmpc/internal/crypto/base_paillier.h:8; include-internal/cbmpc/internal/protocol/ecdsa_2p.h:18 |
| Pedersen commitment |  |  | уязвим (Шор) | допустимо | 4 | 4 | include-internal/cbmpc/internal/zk/zk_pedersen.h:8; src/cbmpc/protocol/ecdsa_2p.cpp:28; src/cbmpc/zk/zk_paillier.cpp:537 |
| RSA |  |  | уязвим (Шор) | допустимо | 3 | 3 | include-internal/cbmpc/internal/crypto/base_rsa.h; src/cbmpc/crypto/base_rsa.cpp:96; src/cbmpc/crypto/base_rsa_oaep.cpp |
| Threshold ECDSA |  |  | уязвим (Шор) | допустимо | 13 | 13 | include-internal/cbmpc/internal/protocol/ecdsa_2p.h:10; include-internal/cbmpc/internal/protocol/ecdsa_mp.h:9; include-internal/cbmpc/internal/protocol/hd_keyset_ecdsa_2p.h:3 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| include/cbmpc/api/curve.h | 305 | `2facde4582730feb655e92033395aada9402fe2c32f78e6ac475bd8324936cad` | 0 |
| include/cbmpc/api/ecdsa_2p.h | 3871 | `105375859252d5a634822b7af6726a4a80003591cc2c8bcefdb6bf72674a1542` | 0 |
| include/cbmpc/api/ecdsa_mp.h | 6405 | `ab364b34f5c08cdcc436596ba385938b4853fb25bbc630ef507be7fa21d46588` | 0 |
| include/cbmpc/api/eddsa_2p.h | 3468 | `16ec1fa4dcb7e197b2ec1edb4f5fee3330b9d4b5016221c0292ca5c9208445d3` | 0 |
| include/cbmpc/api/eddsa_mp.h | 6602 | `3ab97cfccc9ad4c9ed383358f267e68140e69926bbafa9d98fa10ea2c09d477c` | 0 |
| include/cbmpc/api/hd_keyset_ecdsa_2p.h | 1761 | `fc16145b6c7db1ebf924e06172dbc041aca2a8b7186a79755d7f2cc88fb36399` | 0 |
| include/cbmpc/api/hd_keyset_eddsa_2p.h | 1946 | `ae8c48d856ea67d1aed7044aa7ab0df1e682a6a0fd062f8c8114fcbc75ff8070` | 0 |
| include/cbmpc/api/pve_base_pke.h | 7256 | `9280cee649b4752fc92360b22e6ba7ba8e6a2f588cb3bba2a9280a4135f23c2e` | 0 |
| include/cbmpc/api/pve_batch_ac.h | 6780 | `3fbe4705e6454184aec00705496ef78bcea0307f975fad7d1d77f0493e57cf8a` | 0 |
| include/cbmpc/api/pve_batch_single_recipient.h | 3445 | `f98c566cdba6caf7b3d6da68af9a773ae7946dc8f11451af43d573610a54ba57` | 0 |
| include/cbmpc/api/schnorr_2p.h | 3929 | `5b151a5677a5496d763f4e8f678a78b6b570dd8196d16f7eecd30605da3c5dc1` | 0 |
| include/cbmpc/api/schnorr_mp.h | 7143 | `39b31ba9980a43fb1fc8ba8a220ef25492b147ae020b1d0e540fe42b2d6bb53b` | 0 |
| include/cbmpc/api/tdh2.h | 4229 | `4292de2890a66de4ec19bd642ebbb68c0653bfd9e97957dc1d0153dee033308a` | 0 |
| include/cbmpc/c_api/access_structure.h | 2766 | `e9d53711590e479dd37c19a6c4d82cd08c6e9c1438121edb270c0690a9e71b9e` | 0 |
| include/cbmpc/c_api/cmem.h | 1198 | `29624c2da9423a7572f131eb244e216c2fe7944dfe59319edb3458b733c56fb4` | 0 |
| include/cbmpc/c_api/common.h | 2499 | `94bc94a3e819a719afa35151029c8964fb157cd7eb2609d93f257cd975b86746` | 0 |
| include/cbmpc/c_api/ecdsa_2p.h | 4212 | `88ab538b235f8a78490328bc6bf2ce39657689eab758413d36fdf7b00841f476` | 0 |
| include/cbmpc/c_api/ecdsa_mp.h | 8348 | `08b76cba5186c15ccfc1c7b6e49c290a4d4ab7c0fda98f3fab66eb3271a9bbed` | 0 |
| include/cbmpc/c_api/eddsa_2p.h | 3582 | `751f5fe0b4c9bdf3245a51887076846a0e89b0d6fc0ccbebc64c8470c92114f9` | 0 |
| include/cbmpc/c_api/eddsa_mp.h | 8026 | `22e2811912998b1feb41b8ddb171695f639e00af18c8258ebebe5b1e7de48bb9` | 0 |
| include/cbmpc/c_api/job.h | 2853 | `b61893a3c68d4ff836d4ffc6ca21bfa2601cc1b8c5161389217505ccaeee8d16` | 0 |
| include/cbmpc/c_api/pve_base_pke.h | 9594 | `7a93b2954d8f05745ba82a3238fe482f2c87aa593b60bb3f07048151c557b80d` | 0 |
| include/cbmpc/c_api/pve_batch_ac.h | 5993 | `2468fbb957d0607ea714fe4a5aecb91f8d46871053485c81f9d2490637dffda5` | 0 |
| include/cbmpc/c_api/pve_batch_single_recipient.h | 3786 | `f5d0f75b826da34508313415d8ce966191e701ce3184b230ee5cb0a3c8a84f43` | 0 |
| include/cbmpc/c_api/schnorr_2p.h | 3659 | `078fc3e11670dae87921ecc42238204196314aca571f4b328a726d2ea725b9e4` | 0 |
| include/cbmpc/c_api/schnorr_mp.h | 8242 | `daa14190b82a6adbe781120039be8f5f5d873c55e50d583c26569512d8b06dd6` | 0 |
| include/cbmpc/c_api/tdh2.h | 5404 | `67aac4a7c9032fa87988d1fdc559ae3b18df5773c4fcd0b59303afb6e0464cf1` | 0 |
| include/cbmpc/core/access_structure.h | 2181 | `168f318f2676eca879dd6567bc22aad1390c9f0217ce916134ec04a1b8e2a318` | 0 |
| include/cbmpc/core/access_structure_limits.h | 109 | `f6eb33c9c3f3ab6886e672f6b71ae35e21fd9895433c5d0845ea6036e66f4567` | 0 |
| include/cbmpc/core/bip32_path.h | 383 | `f404682cee2ab3b94e54ab3a625d74c6c483779aed72389cd63407ad0d3bd954` | 0 |
| include/cbmpc/core/buf.h | 8626 | `3211ba3cefa7bb2dc584fc4854d146b9830afcaa7040b64f31e4de89875d8c06` | 0 |
| include/cbmpc/core/buf128.h | 3122 | `8e2bef19a7dcab978acb3c29a992e12072f764b53f449d97e2dc907d5027c35c` | 0 |
| include/cbmpc/core/buf256.h | 1780 | `5c99e90645842aa88fa75191c7e138fe458b4605ae4b06b112e125aed7ba69e2` | 0 |
| include/cbmpc/core/error.h | 2750 | `82b6b7a47256c7fab6f46e74313f97291a634811f28cb64dd1486d95628182da` | 0 |
| include/cbmpc/core/job.h | 2073 | `0c35a15cdae4d5f4450d93e5ec27af30cc5550bf9722da8f2d41016fd71fc85f` | 0 |
| include/cbmpc/core/macros.h | 946 | `da42b82206cd7ae447f0dbb023494ba8cc4a94f36977faccd8a82e2648d5c50b` | 0 |
| include/cbmpc/core/precompiled.h | 3021 | `45071365b97849cfe36fea65e1a63b25a09078189e33495006cc592f8c44561a` | 0 |
| include-internal/cbmpc/internal/core/convert.h | 8184 | `a56e2e6c773cbb9de2df1dae1b5240c9162c788f2b59d596262f67e417fd9ef5` | 0 |
| include-internal/cbmpc/internal/core/extended_uint.h | 1264 | `8551e894af07214d5d4faf8fd32eb9c6d8fb5da19097bb2f5d5fcb323484aed0` | 0 |
| include-internal/cbmpc/internal/core/log.h | 2878 | `52ec905cb9fa56db485bb9ac1e0d5c82dfb63db54b3b4a7aba1120aba12efac9` | 0 |
| include-internal/cbmpc/internal/core/strext.h | 873 | `f245b9bb300b256ecb1b52bc1ae9f5685411a16ab67724cf60bf16bfe17a2053` | 0 |
| include-internal/cbmpc/internal/core/utils.h | 7111 | `b98488440036d38243111e9d5126426e71a0481921bf0ae35b099dd3af572413` | 0 |
| include-internal/cbmpc/internal/crypto/base.h | 5757 | `def0f4da84c6da78a3ec08c2a1dc2f00f71bf0fb4bf3d788ea9dfff923b7ba01` | 0 |
| include-internal/cbmpc/internal/crypto/base_bn.h | 8887 | `2ab03b1f64160824d980856f8bb4d91a3413b293c5ff6b897e6ddb825bdef696` | 0 |
| include-internal/cbmpc/internal/crypto/base_bn256.h | 4992 | `253d3c7e26e94204dad124a6e6450db90ae1dc3617c30d56c25d300b37bf0ff1` | 0 |
| include-internal/cbmpc/internal/crypto/base_ec_core.h | 18124 | `d675354dcb9d373c9e84a80ea4af72476caaa1c708a36ceed0330798a9c0a0e9` | 0 |
| include-internal/cbmpc/internal/crypto/base_ecc.h | 13930 | `4622c8393c4f4bf8d3abdc12789b328ec85e725874e01b02df1896b8c5b311d0` | 0 |
| include-internal/cbmpc/internal/crypto/base_ecc_secp256k1.h | 2905 | `4fd96cb7eca67bfa1627efa01a11f095c5467120c3fca5cda2cce50935884dc2` | 0 |
| include-internal/cbmpc/internal/crypto/base_eddsa.h | 2547 | `11b91f8dd6e32ed727a8838aae477b5198d73a0f46930c8fbf67fdfde33de3ac` | 0 |
| include-internal/cbmpc/internal/crypto/base_hash.h | 9641 | `4eea85e07fd6c13ffbc81910fa739f11f7b4b367607592fdfd203379b14caab0` | 0 |
| include-internal/cbmpc/internal/crypto/base_mod.h | 5488 | `9416b0b19f16e95b1a82029433dc8f2e606cfb21a5e9776f74f1b8b88a6ad2a9` | 0 |
| include-internal/cbmpc/internal/crypto/base_paillier.h | 7140 | `635074e16e9ac9d0941b425940da73aaa1cfcbf9d9bfc23dbcaa17220462cfb1` | 0 |
| include-internal/cbmpc/internal/crypto/base_pki.h | 7471 | `98b0c1f3a7cfed44bcf1f4326ca61c7f25f0f196b63c04c50349ca400cff8a83` | 0 |
| include-internal/cbmpc/internal/crypto/base_rsa.h | 4133 | `d57c2cbddf86fcabca1fece5f47377f3c6593e2bbe1fd0d609ce39f666925d18` | 0 |
| include-internal/cbmpc/internal/crypto/commitment.h | 5024 | `12acf4a73daffe317049c4adbf897cac2471d3b5399e8ff8a6338397d3763e8a` | 0 |
| include-internal/cbmpc/internal/crypto/ec25519_core.h | 1819 | `91af646c59ed5ed8b7adfb862229c2569f7f7f7e02b06cbfc322ad6de1cd758d` | 0 |
| include-internal/cbmpc/internal/crypto/elgamal.h | 3841 | `3e7e1dc52f7c63d54377c18ed4d65cb8e2b7bd01daaf085530e3431ba66b676c` | 0 |
| include-internal/cbmpc/internal/crypto/lagrange.h | 2296 | `98372b80b7f725bcc14ed22b542e2e4b0fb959393a8c5e0048af309b2d4d1546` | 0 |
| include-internal/cbmpc/internal/crypto/mlkem768.h | 701 | `f34c16ad0e3074f42661f769d8b68b6b72ef35c431db68982049d8f2816620bd` | 0 |
| include-internal/cbmpc/internal/crypto/ro.h | 4056 | `a2a83967f8151a94001dd3cb20c359a2946abb0bceb359df96cbf243e6467bb6` | 0 |
| include-internal/cbmpc/internal/crypto/scope.h | 1338 | `6ee20f03d2bc5e27c80255120ac9d21650e222971584093b821cb2989ce83669` | 0 |
| include-internal/cbmpc/internal/crypto/secret_sharing.h | 6159 | `183ec4af5557f2176b790d99316b7296041d40dab13c75e712bdd46f4bcb49f8` | 0 |
| include-internal/cbmpc/internal/crypto/tdh2.h | 4119 | `84dcbc72243ec5d7acbc9e44387a9ea28bfe25478d7dfed9b339463b65d0e4a6` | 0 |
| include-internal/cbmpc/internal/protocol/agree_random.h | 1227 | `6b3da20d98680a9f583ec4339f34444ad214ac84e1d96ed194a6bf7a29220153` | 0 |
| include-internal/cbmpc/internal/protocol/committed_broadcast.h | 2828 | `8248d3fd59ab317e917b1a8a7b45500e35e74c587392b028714f95d1912fb872` | 0 |
| include-internal/cbmpc/internal/protocol/ec_dkg.h | 4175 | `47f244abb153a3bcc5efec66471fb70d0b92d13188783d09bf07c823213ce03d` | 0 |
| include-internal/cbmpc/internal/protocol/ecdsa_2p.h | 4524 | `bb2d45c7091bcb2dbdc81e77b6712c519093577ceec7a937003e57228bd767bb` | 0 |
| include-internal/cbmpc/internal/protocol/ecdsa_mp.h | 4370 | `09e920ca00569b73af88dd9ac50b4e809d20e6ef6c57a8ada392a2a40e7ebf3f` | 0 |
| include-internal/cbmpc/internal/protocol/eddsa.h | 802 | `1bae54da49de50c02f780d2bd27bb548eadc22ad94e095c01ae16b7e3cd34270` | 0 |
| include-internal/cbmpc/internal/protocol/hd_keyset_ecdsa_2p.h | 1460 | `98cef577118dc981109e7eca78bf1f41d24967f84449bf597008d2c8a69c604c` | 0 |
| include-internal/cbmpc/internal/protocol/hd_keyset_eddsa_2p.h | 1401 | `0ec98767b365b0bcc4a52f1dbf47fb1096c0a580321abe70532ce3c0efacad91` | 0 |
| include-internal/cbmpc/internal/protocol/hd_tree_bip32.h | 1749 | `66bc9c67289298cc3d3bae9f1ba2a960aadcdc50e9069105fad3e1fae2edfcad` | 0 |
| include-internal/cbmpc/internal/protocol/int_commitment.h | 847 | `d64fd9bd118676bcd8f856a70de1bf1678fe9eeea3597f164ac180e67ca4780d` | 0 |
| include-internal/cbmpc/internal/protocol/mpc_job.h | 17919 | `a93a6744fe1693909d3e46a1f5976961df525f515c6b28f6c65e4094fbf14763` | 0 |
| include-internal/cbmpc/internal/protocol/ot.h | 8615 | `da042352cfa725c622efe54930f3019ff25ee9668e81cc0586b68c687e67a1e1` | 0 |
| include-internal/cbmpc/internal/protocol/pve.h | 1268 | `f3d48fad161594f0175ece90e99aa661df33257447229f54ae10ec09f1bf046f` | 0 |
| include-internal/cbmpc/internal/protocol/pve_ac.h | 4481 | `e6d60929413bf4fa70c899856329d5f096062b0f39fc3d0e74e92c58f94d9824` | 0 |
| include-internal/cbmpc/internal/protocol/pve_base.h | 9109 | `26dcc28fef1f2733ed7c10f2f9a389df73ecd8cc981358367c67b29d930ebfc1` | 0 |
| include-internal/cbmpc/internal/protocol/pve_batch.h | 2350 | `140959a47e0bb81fb502192fc4d3c56a4f69b4aae8cd1b642ca8a5dcd6789575` | 0 |
| include-internal/cbmpc/internal/protocol/schnorr_2p.h | 955 | `26b5a68de67cb25384741b84bf862f3c30ab0f505474cc0b0a5f8fc10b8eb71b` | 0 |
| include-internal/cbmpc/internal/protocol/schnorr_mp.h | 1636 | `25c8b2c1a79f70349ee2098eb56c8bb6f148598fccc91b214af185a17b0b0c1b` | 0 |
| include-internal/cbmpc/internal/protocol/sid.h | 2398 | `a13269fefc215f1f5dbddd924174ee1fed95db295d1cdc909c69c5c014bbd589` | 0 |
| include-internal/cbmpc/internal/protocol/util.h | 2083 | `21d08c60af4b75538821a8ec31f3cd8a50adc6c8753c206837f9f7bb558ea170` | 0 |
| include-internal/cbmpc/internal/zk/fischlin.h | 3695 | `792546bb45cf6ce43db2bd34723b18da117d1f635a97fe518d09ff02c8fb31b6` | 0 |
| include-internal/cbmpc/internal/zk/small_primes.h | 1046 | `2159754496de246e69d96310f1f9dacaec9df1f3c04c16385c4bce995ea2e83e` | 0 |
| include-internal/cbmpc/internal/zk/zk_ec.h | 2816 | `01853d5739fecf852b82e20193aad9faa1a4d38702e4e6dc202d54094b3728e3` | 0 |
| include-internal/cbmpc/internal/zk/zk_elgamal_com.h | 3006 | `90fc7c4c62e170e4fc2bf0dad335cbf556472bb70f30ae1d39ef37dbb55a5135` | 0 |
| include-internal/cbmpc/internal/zk/zk_paillier.h | 7613 | `5ad37919ff30625baf38930da6bea9aefe1fb3cddab2a02e52d9e42a6a0f2253` | 0 |
| include-internal/cbmpc/internal/zk/zk_pedersen.h | 4139 | `899fad68ffd0cc058ea9edabd9505a26a539d2d31e64f3345d976991216bc528` | 0 |
| include-internal/cbmpc/internal/zk/zk_unknown_order.h | 622 | `f632c986fe305b9253cd61b00bf6ca4e91ae2afd4228d910f7ac3219feb9e1ef` | 0 |
| include-internal/cbmpc/internal/zk/zk_util.h | 1721 | `5751b4ae4aa64f5fbe7af8802b7a489737f5f042d05873dcee21ca8fec55a69e` | 0 |
| src/cbmpc/api/access_structure_util.h | 9006 | `ceddfd95a56fef01a49c9f9be5d4d02f9fa6f94dc584bf1e911b0289fc1f4580` | 0 |
| src/cbmpc/api/curve_util.h | 1106 | `2b1ce8031d294bd7721265d8bd13469b0828e5511b10a43ef2ba9cb16f3dd4d6` | 0 |
| src/cbmpc/api/ecdsa2pc.cpp | 13715 | `2bd6f2c9780b68b323f33f000c019d99aa9ece77fc399fd69a4c418a5b247724` | 0 |
| src/cbmpc/api/ecdsa_mp.cpp | 23511 | `e8b790be6ff65035680333e944c16aa409fc39b9f3efde09f3e1a034b66fb069` | 0 |
| src/cbmpc/api/eddsa2pc.cpp | 9662 | `277a7491b190d4e1fbec7aac06aa60e357a4a72d374a5af0d9c8d323344ab2ad` | 0 |
| src/cbmpc/api/eddsa_mp.cpp | 23718 | `fdc84660705d7dd8168aca64fd9620da0a9f5bc0ae584beded77339b79502e0b` | 0 |
| src/cbmpc/api/hd_keyset_ecdsa_2p.cpp | 9399 | `46f38a66df82ed9cd573f6887e08a8dd6f32f96cd4fa3d9e0baaa8efa2c9b34a` | 0 |
| src/cbmpc/api/hd_keyset_eddsa_2p.cpp | 8196 | `db69a2795c6ad2b92dccdb42301e4d58701cfe694787171382580d1f6eac8a5c` | 0 |
| src/cbmpc/api/hd_keyset_util.h | 1102 | `80b15e70053540d811ad516f0a2c9d20577454365379a737793359870c44884e` | 0 |
| src/cbmpc/api/job_util.h | 2963 | `0eaf11ceb45fe2a8c36148f925434e2b9b4e55b053f16fac7c023f751d8928c2` | 0 |
| src/cbmpc/api/mem_util.h | 2091 | `fd6fb01ab217ab64ab6182fe01ee9f656381a6690848ab3f0b11c6506b7063d0` | 0 |
| src/cbmpc/api/pve_base_pke.cpp | 15533 | `5639e943156dbf5e142c178b07da2c4eb0a5d60bcfa0f61af1b18bc22b830937` | 0 |
| src/cbmpc/api/pve_batch_ac.cpp | 19720 | `8b8be49db0d9dabae40d79f31809585672d745b3ac0a66147f6bab96a2f7daa3` | 0 |
| src/cbmpc/api/pve_batch_single_recipient.cpp | 12533 | `c5572970684fdeff67948f2d3e40b6e2777a4fbe0737e70eb334ecaf7cc0e746` | 0 |
| src/cbmpc/api/pve_internal.h | 6257 | `47bce2585e9a7bf7b3a1939dc6f914f9f4a71a8e745a1dd372bc00ebab713754` | 0 |
| src/cbmpc/api/schnorr2pc.cpp | 10080 | `9495eab05f3110eaff559f33a89cea322a17fd6c873139300a9ff54b042eaaad` | 0 |
| src/cbmpc/api/schnorr_mp.cpp | 24257 | `bd909c04140c085cb023ee5fac58ee26b361234b6ce65f395fc0f37defe39bd0` | 0 |
| src/cbmpc/api/tdh2.cpp | 15729 | `a4ff1563e8b6429c4576c0430a6164510211b943d461362ee0ebd3a7186ae1c8` | 0 |
| src/cbmpc/c_api/access_structure_adapter.h | 4841 | `08d2877d3dd792e33afd088e767d5925d177be052c50f2023524c0bbf81ece68` | 0 |
| src/cbmpc/c_api/common.cpp | 1592 | `5280698eda4f9f4e66b6ae8560818f4c8dd2f4f9f7c13ce2957f583ffc70640f` | 0 |
| src/cbmpc/c_api/ecdsa2pc.cpp | 8935 | `350195de0a3b6dec093519c569d2fb7bb50de40ec80f81f750e6fe2e5cef5a77` | 0 |
| src/cbmpc/c_api/ecdsa_mp.cpp | 14657 | `ae5651ed5d7de9eea96f9e9b1c9b8f6ce4779bde23df3c7ad5835c584fe57986` | 0 |
| src/cbmpc/c_api/eddsa2pc.cpp | 7405 | `cac76cf191e1737f82300959bafe1b6d9a73723da0ac752c4fe573764ab576ad` | 0 |
| src/cbmpc/c_api/eddsa_mp.cpp | 14249 | `7393ff3f085a404140f443da26bae530000d8158963983a77a4eebe9402e9849` | 0 |
| src/cbmpc/c_api/pve_base_pke.cpp | 19582 | `c6e5ec7ce741d2c32c9895618ec807b02782e502401b759a79a7cd1030c1ba7e` | 0 |
| src/cbmpc/c_api/pve_batch_ac.cpp | 15057 | `86de96b4539a390203c7c25dd9f452ee31f6d22efe2445135d19fbfb356f9640` | 0 |
| src/cbmpc/c_api/pve_batch_single_recipient.cpp | 9558 | `c1bf050dfe843b0c9491835b2a4a67d5a87bc31e91b20167c76e18fccb15a40b` | 0 |
| src/cbmpc/c_api/pve_internal.h | 3922 | `67717ecc213db88a2ceeefeca34434d6ba44e7606d169118a384f4d0c70ae884` | 0 |
| src/cbmpc/c_api/schnorr2pc.cpp | 8125 | `0ddf4832e2ea31c50a5933a5f0d4b82c7fbbaa50e3de6f4b79f58ec4d8dfe6fc` | 0 |
| src/cbmpc/c_api/schnorr_mp.cpp | 15011 | `f1c40a8f09a77764fe725b393cdc7c0b4e5af68ec1373471d09a0e43b6105cb4` | 0 |
| src/cbmpc/c_api/tdh2.cpp | 12864 | `8a7813233276b5b2322215aff73847238307574f781aa9a331e8e619538f38ee` | 0 |
| src/cbmpc/c_api/transport_adapter.h | 3637 | `b40563601e342dad20c6d714eeb50b71e2a1e17fb3c55ea6e1b06781dd91d199` | 0 |
| src/cbmpc/c_api/util.h | 6137 | `54e197b005d5bf85a970ffd48c13fa55c1748b8e1a53e8b70cd4d2194e73d6a3` | 0 |
| src/cbmpc/core/buf.cpp | 19249 | `4f05b7b7f064a8df4fdbe8f73930690073f9bdf7fe644ad8df2fc95974436711` | 0 |
| src/cbmpc/core/buf128.cpp | 8097 | `ab4b91df60b609f7958c7c9927b1bfac57fef68079ae644be0070555c944d7d6` | 0 |
| src/cbmpc/core/buf256.cpp | 5718 | `bc92ef88c227313eb5c334e8315985ca4ddc23c0cd543e7bcf3778aa9d688878` | 0 |
| src/cbmpc/core/convert.cpp | 5831 | `e058331387e5a1467cbc044ad88e4717644b4893d4d251e1268798a4d8c75f05` | 0 |
| src/cbmpc/core/error.cpp | 5599 | `b32bfc0d066f34f00f5b5e319a04284d35b405ace58c487e0f2105293e024aeb` | 0 |
| src/cbmpc/core/strext.cpp | 3904 | `d760ebfff69eb90c43825f4c67cd57c619e447baa7219ee06a3f1f675b5874bb` | 0 |
| src/cbmpc/crypto/base.cpp | 8596 | `dd2af36fb426bc7b3b618d9972a4215e01577766256eac1ed92966b54e57af93` | 0 |
| src/cbmpc/crypto/base_bn.cpp | 21760 | `fbec856dfe302bc6c8dc4dfdaa52a0f0ee84287ef13634885cf34e1d03ade10e` | 0 |
| src/cbmpc/crypto/base_bn256.cpp | 38165 | `5aab4b8a2ae1328950c40a1589bee877ecb9468101b0fc7baecd773514e5fec3` | 0 |
| src/cbmpc/crypto/base_ec_core.cpp | 2539 | `16280192dd3f73e0969ff983499669d5327b215018dace8f4e37eb161e822c6a` | 0 |
| src/cbmpc/crypto/base_ecc.cpp | 35151 | `dd31645addc8cf00b027fc453868a4aec33a826a95a7acca172dd3af54ca97ec` | 0 |
| src/cbmpc/crypto/base_ecc_secp256k1.cpp | 15422 | `31cabe4ca85327316c07f9865c9efa3a81c98a630bc3276806d3dd96cf400c73` | 0 |
| src/cbmpc/crypto/base_eddsa.cpp | 8170 | `45697966a1eb28d114a3f26c52dbd3d97abef3ed0bd13a6da051f2825f70f99d` | 0 |
| src/cbmpc/crypto/base_hash.cpp | 12718 | `6797b8c75aaaf50070644024ab4df41ade4e6a676dc53cba207929a5e334af86` | 0 |
| src/cbmpc/crypto/base_mod.cpp | 16690 | `8390bd8433403219ac67b744ca8c1f04b919376f75b48e12aaebe1044a551738` | 0 |
| src/cbmpc/crypto/base_paillier.cpp | 11598 | `bc74a8ec5b010ffa69aaeabeb2edb7dd075972229f2997cb48b6bc38106de467` | 0 |
| src/cbmpc/crypto/base_rsa.cpp | 13948 | `ce1f7e2af4ab105d95931ebce00de933dc0718afbb555bea8cac329324b39cf4` | 0 |
| src/cbmpc/crypto/base_rsa_oaep.cpp | 7631 | `488a05f19bfe3be1bb45df021c887b46f88af1930dbe88f4412830a77a70cd19` | 0 |
| src/cbmpc/crypto/drbg.cpp | 2236 | `4e3fbc5382e267539b72d1556890ad8d3ffb15509db8ba4f6d3609f4a75b7708` | 0 |
| src/cbmpc/crypto/ec25519_core.cpp | 32300 | `fcf18843c539fff85668d46a094aa97b4ba6014fdb3005bbf08ce87804fa4d61` | 0 |
| src/cbmpc/crypto/elgamal.cpp | 4096 | `44e90812713ef86a0f2ef69a55d8fd53447a6aee718fe91410a73a3e27b0ab16` | 0 |
| src/cbmpc/crypto/lagrange.cpp | 6291 | `4ed9ad1c1a9f9a3597cd49fc2034d9b6c0986b8d92fb7b1109a87f2dda24772c` | 0 |
| src/cbmpc/crypto/mlkem768.cpp | 3026 | `4078550dd5d763189b297626094dc68bca380049f1f36a8b123a0a0272576792` | 0 |
| src/cbmpc/crypto/ro.cpp | 4612 | `b594d9dff0634336ee222e03972a16e871028b334c15cbd03b74de7bcc74bb41` | 0 |
| src/cbmpc/crypto/secret_sharing.cpp | 18838 | `aea152036abdf368422312bc67b533c9564db6645b423f87bcd7bb4a0fbcce26` | 0 |
| src/cbmpc/crypto/tdh2.cpp | 7393 | `09bb2ea74cb90fce2455dfdfb59a46d2602ec8ec22a88cc65f1006746eaa87db` | 0 |
| src/cbmpc/protocol/agree_random.cpp | 4095 | `fda790e3f41acc7561402f8dc85f21c20e40d9a0228ee0e8596c2135e1476175` | 0 |
| src/cbmpc/protocol/ec_dkg.cpp | 24991 | `3b23c2ec0047bc420818c27c59c8c134214d805ed9f9e835757aa7b5a07a1855` | 0 |
| src/cbmpc/protocol/ecdsa_2p.cpp | 24824 | `676da782f28e8371b19dd2737d91d08ac8fbf805bf4c91b0c4defe0f9116216c` | 0 |
| src/cbmpc/protocol/ecdsa_mp.cpp | 20263 | `6fd98e15fd272931e7ed76418a3833da33c3facd895e60d95453dd3acea59c0b` | 0 |
| src/cbmpc/protocol/eddsa.cpp | 982 | `e534d848e59ef7fad0a8156804d0b545e919aca37cc0995bee5482904f5e985e` | 0 |
| src/cbmpc/protocol/hd_keyset_ecdsa_2p.cpp | 6599 | `dc2f999c8ba5817ac88817a08aa3cdfbfb09d258bf16c2b11719990f9355b075` | 0 |
| src/cbmpc/protocol/hd_keyset_eddsa_2p.cpp | 5751 | `60b1f34c8280d8ca1979f5522553544df9015d0c6c3f8d0f46c9a4f411d1f5b7` | 0 |
| src/cbmpc/protocol/hd_tree_bip32.cpp | 1202 | `b477c98d2d5e834999eab5bc3bdb6d610d01137b3922ce40d2b33f296cfcd939` | 0 |
| src/cbmpc/protocol/int_commitment.cpp | 90896 | `28356c850e19c96fc65a8abb43a8191779f756cf424c07146d4ffde86e64afdd` | 0 |
| src/cbmpc/protocol/mpc_job.cpp | 1207 | `50346b5c5839ece7d5db342babcff1a124f3341a79ee0f4cc9f5da526af5fb09` | 0 |
| src/cbmpc/protocol/ot.cpp | 17534 | `6a1a3e82170609e3e7d4bf15b7d0fcdb22c2887d3f68b851ad9aabe7bb0800db` | 0 |
| src/cbmpc/protocol/pve.cpp | 4987 | `d4c53ffa9710407b9d016673f2de6eb5ce18e3458a6c803b11eb57880905286f` | 0 |
| src/cbmpc/protocol/pve_ac.cpp | 11348 | `de010bed8070f48c7adafbaf606cc0e4bb43243177c9c12448ecb3d9dc2ca536` | 0 |
| src/cbmpc/protocol/pve_base.cpp | 1661 | `4cf97abd43be32195eeb17a2e8ef41aec4bf40d7dac414bee458425764c25df3` | 0 |
| src/cbmpc/protocol/pve_batch.cpp | 7350 | `2bbf74000b73ade87272a6d048a4c894019a5338da4916084e26f510be5dd178` | 0 |
| src/cbmpc/protocol/schnorr_2p.cpp | 5348 | `a998fa463bf108155247586360a6e309dc8ec940ea10916c93a66334c0baab50` | 0 |
| src/cbmpc/protocol/schnorr_mp.cpp | 7312 | `b7aa492e64186b649ce0a19abc70e27afe5f7bcaaffc008bad3a6e0ee7d83af8` | 0 |
| src/cbmpc/zk/fischlin.cpp | 2071 | `b272d3a5cc641eeaab74baaf6d494958a0e56db0e205d28f301b9944b3d66c68` | 0 |
| src/cbmpc/zk/small_primes.cpp | 82305 | `508021bcc27b6bc7efe6481ce1f85407a02501c9a8a6c1628cd022fc59ec4630` | 0 |
| src/cbmpc/zk/zk_ec.cpp | 11090 | `864cc7b1616050ed50842d23b2c8d78c09ca253fcd811d08987091f4bf002614` | 0 |
| src/cbmpc/zk/zk_elgamal_com.cpp | 11105 | `ba7214e14d37fcb23c9334f0502c9ce9fb9627cce992fd676921d82c6f8377ec` | 0 |
| src/cbmpc/zk/zk_paillier.cpp | 23160 | `fd1dc137a7611808815356268521063e54f833048b8fc42e616a59c7188e0ab0` | 0 |
| src/cbmpc/zk/zk_pedersen.cpp | 18743 | `968641640c623fc2cdfe6012b8686db394631006f90478bfc182820228662bc6` | 0 |
| src/cbmpc/zk/zk_unknown_order.cpp | 2674 | `bcde5bc6688e9e3f6bc022f2a4089d98f98a8d3b83f277ed00fbde0e1608fbd7` | 0 |
