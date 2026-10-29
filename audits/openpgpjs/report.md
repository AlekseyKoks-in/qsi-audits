# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** openpgpjs @ 8bc35df48879 · OpenPGP.js project — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-28 12:44 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 2b3ed4b7-2e32-4adb-8ed5-25a8c413c766 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Разработчик ПО безопасности |
| SHA-256 содержимого | `b2ce41a779ab83da67c60c3d95217832c3b36f0255aef76330dcb58b2cfe65da` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **0**
- Средняя: **7**
- Низкая: **1**
- Информационная: **1**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 0
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 2
- Долгосрочный постквантовый риск: 6
- Рекомендация по улучшению: 1
- Недостаточность данных: 0

Неравенство Моски (x + y > z): x = 10, y = 3, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

**Постквантовая зрелость: Уровень 2 из 4 — постквантовое используется вне критичных путей.** Следующий шаг: Распространите постквантовую защиту на критичные роли, которые остаются классическими, начиная с того, что можно записать уже сегодня (обёрнутые ключи, обмен ключами в канале).

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/openpgpjs/openpgpjs> @ `8bc35df4887933a3b2661e3741b33ba5f347b935` — ссылки в доказательствах открывают строки на этом коммите.

108 файлов, всего 1427412 байт, редактирований: 15; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 103 | .jsdocrc.cjs: 28 lines scanned with 16 rule patterns and 122 registry patterns; docs/scripts/linenumber.js: 25 lines scanned with 16 rule patterns and 122 registry patterns; docs/scripts/prettify/lang-css.js: 3 lines scanned with 16 rule patterns and 122 registry patterns |
| keys | проверено | 15 | README.md: the marker at line 238 is a PEM header without key material (a literal in code that parses or writes PEM, or a documentation placeholder); README.md: the marker at line 288 is a PEM header without key material (a literal in code that parses or writes PEM, or a documentation placeholder); README.md: the marker at line 318 is a PEM header without key material (a literal in code that parses or writes PEM, or a documentation placeholder) |
| certificates_and_keys | проверено | 3 | README.md: certificates/keys parsed; docs/index.html: certificates/keys parsed; src/encoding/armor.js: certificates/keys parsed |
| dependencies | проверено | 3 | lightweight/package.json: 0 dependencies parsed (0 pinned); package-lock.json: 1021 dependencies parsed (1021 pinned); package.json: 50 dependencies parsed (0 pinned) |
| osv_advisories | проверено | 1 | 929 pinned packages queried at OSV.dev; 23 affected (23 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree openpgpjs at 8bc35df4887933a3b2661e3741b33ba5f347b935. 108 files analysed; of 241 files, 61 are test, fuzzing, benchmark or example code and were left out, 72 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **94** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 53.8%

## 7. Подробное описание находок

### QSI-2026-04759 — Квантово-уязвимый X25519: обёртка ключей и шифрование хранимых данных (5 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:X25519:key_wrapping`
- Источник данных: src/crypto/crypto.js
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:44 UTC
- Балл приоритета: 38.0 / 100
- CVSS v3.1: неприменимо

41 упоминаний X25519 в 5 файл(ах), например src/crypto/crypto.js:67. Роль по путям, именам функций и соседнему коду: обёртка ключей и шифрование хранимых данных. Ключи или данные, зашифрованные на эти открытые ключи, хранятся: кто скопирует их сейчас, расшифрует, когда появится CRQC («собери сейчас — расшифруй потом»).

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/crypto/crypto.js:67 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/crypto/crypto.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/crypto.js#L67) · line 67 · SHA-256 6caf77681182d2e5587208f4f2f3e2adfbe5716ca5c74635b3d4338ab32c9a72_

```
   66 |     }
   67 |     case enums.publicKey.x25519:
   68 |     case enums.publicKey.x448: {
```

_file_excerpt · [src/crypto/crypto.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/crypto.js#L126) · line 126 · SHA-256 97ebcbb54d2758fefc29cac032c9f08d18ded0816dc1c0a8867b60c82312d138_

```
  125 |     }
  126 |     case enums.publicKey.x25519:
  127 |     case enums.publicKey.x448: {
```

_file_excerpt · [src/crypto/crypto.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/crypto.js#L202) · line 202 · SHA-256 7ce8a6903b93123062ab7128a6e668e6d2cf40ebae581e2048e2f844cd2bc378_

```
  201 |     case enums.publicKey.ed448:
  202 |     case enums.publicKey.x25519:
  203 |     case enums.publicKey.x448: {
```

_file_excerpt · [src/crypto/public_key/elliptic/ecdh_x.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/ecdh_x.js#L16) · line 16 · SHA-256 6a8eddf288a9c2a77149db1f401d401b0b95e3d4a1215b63173ffa115a3c1d3f_

```
   15 | const HKDF_INFO = {
   16 |   x25519: util.encodeUTF8('OpenPGP X25519'),
   17 |   x448: util.encodeUTF8('OpenPGP X448')
```

_file_excerpt · [src/crypto/public_key/elliptic/ecdh_x.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/ecdh_x.js#L27) · line 27 · SHA-256 922ea9b93ea793bd820ba0ef05d8cf6ea9bda82b3587e2f71a243d89d2cb9d94_

```
   26 |   switch (algo) {
   27 |     case enums.publicKey.x25519:
   28 |       try {
```

_file_excerpt · [src/crypto/public_key/elliptic/ecdh_x.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/ecdh_x.js#L57) · line 57 · SHA-256 371ae1787aa309a61d2ab90e6f937a3c82ffb06df08f86b0074baa8b7940524e_

```
   56 |         }
   57 |         const { default: x25519 } = await import('@openpgp/tweetnacl');
   58 |         // k stays in little-endian, unlike legacy ECDH over curve25519
```

_file_excerpt · [src/key/helper.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/key/helper.js#L425) · line 425 · SHA-256 59adffecad14d86080d43ea51a008d5eed02ea566984f5458a383bd909e5ad53_

```
  424 |       break;
  425 |     case 'ecc': // NB: this case also handles legacy eddsa and x25519 keys, based on `options.curve`
  426 |       try {
```

_file_excerpt · [src/key/helper.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/key/helper.js#L442) · line 442 · SHA-256 0cee2e279a6b5fe687f969526552efa361b0132a03e1b834689ac210cb80a418_

```
  441 |     case 'curve25519':
  442 |       options.algorithm = options.sign ? enums.publicKey.ed25519 : enums.publicKey.x25519;
  443 |       break;
```

_file_excerpt · [src/key/helper.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/key/helper.js#L482) · line 482 · SHA-256 e5505ee4ae066a442ec272a51ad1f32a27704ddf9d13d5f4ce1205af1d8d11cf_

```
  481 |     case enums.publicKey.ecdh:
  482 |     case enums.publicKey.x25519:
  483 |     case enums.publicKey.x448:
```

_file_excerpt · [src/message.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/message.js#L367) · line 367 · SHA-256 16b37e58a27065ccebe12db67a707b30d29ed30a225cd9e99bcd10e2b1af24ac_

```
  366 |       .then(maybeKey => {
  367 |         if (maybeKey && (maybeKey.keyPacket.algorithm === enums.publicKey.x25519 || maybeKey.keyPacket.algorithm === enums.publicKey.x448) &&
  368 |           !aeadAlgoName && !util.isAES(symmetricAlgo)) { // if AEAD is defined, then PKESK v6 are used, and the algo info is encrypted
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Оборачивайте ключи ML-KEM или гибридным KEM (X25519 + ML-KEM-768) и переоберните хранимые ключи; для данных, которые уже могли скопировать, нужна отдельная оценка.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-04764 — Квантово-уязвимый ECDH: обёртка ключей и шифрование хранимых данных (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDH:key_wrapping`
- Источник данных: src/crypto/public_key/elliptic/ecdh_x.js
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:44 UTC
- Балл приоритета: 38.0 / 100
- CVSS v3.1: неприменимо

8 упоминаний ECDH в 1 файл(ах), например src/crypto/public_key/elliptic/ecdh_x.js:69. Роль по путям, именам функций и соседнему коду: обёртка ключей и шифрование хранимых данных. Ключи или данные, зашифрованные на эти открытые ключи, хранятся: кто скопирует их сейчас, расшифрует, когда появится CRQC («собери сейчас — расшифруй потом»).

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/crypto/public_key/elliptic/ecdh_x.js:69 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/crypto/public_key/elliptic/ecdh_x.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/ecdh_x.js#L69) · line 69 · SHA-256 30222de3219cc99164d9b95fb8c95d2b149f5e65081439fc8f66d5ab949cf0cf_

```
   68 |     default:
   69 |       throw new Error('Unsupported ECDH algorithm');
   70 |   }
```

_file_excerpt · [src/crypto/public_key/elliptic/ecdh_x.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/ecdh_x.js#L147) · line 147 · SHA-256 4fc585ad8fd85e138aac18c158c73931dd6b712783d58a4bd4167814da997bd9_

```
  146 |     default:
  147 |       throw new Error('Unsupported ECDH algorithm');
  148 |   }
```

_file_excerpt · [src/crypto/public_key/elliptic/ecdh_x.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/ecdh_x.js#L183) · line 183 · SHA-256 d1b356d9bc94caa86cfccaa12996dbfd31b0813f90221d6728549b30f14f789f_

```
  182 |     default:
  183 |       throw new Error('Unsupported ECDH algorithm');
  184 |   }
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Оборачивайте ключи ML-KEM или гибридным KEM (X25519 + ML-KEM-768) и переоберните хранимые ключи; для данных, которые уже могли скопировать, нужна отдельная оценка.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-04762 — Квантово-уязвимый ECDH: роль не определена (2 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDH:general`
- Источник данных: src/crypto/public_key/elliptic/ecdh.js
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:44 UTC
- Балл приоритета: 35.3 / 100
- CVSS v3.1: неприменимо

9 упоминаний ECDH в 2 файл(ах), например src/crypto/public_key/elliptic/ecdh.js:249. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/crypto/public_key/elliptic/ecdh.js:249 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/crypto/public_key/elliptic/ecdh.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/ecdh.js#L249) · line 249 · SHA-256 3454cba51223c0daf016a91dac4294f475ec4f66b4f481c989050ea86ad3ee90_

```
  248 |     {
  249 |       name: 'ECDH',
  250 |       namedCurve: curve.web
```

_file_excerpt · [src/crypto/public_key/elliptic/ecdh.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/ecdh.js#L260) · line 260 · SHA-256 3e270aa8dd1322e70e5a4ce00d678ee9e1891c5a88f54924881a592cdfcee43e_

```
  259 |     {
  260 |       name: 'ECDH',
  261 |       namedCurve: curve.web
```

_file_excerpt · [src/crypto/public_key/elliptic/ecdh.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/ecdh.js#L269) · line 269 · SHA-256 a4b9152c04c73f78c219aef1b6c7e22425768c871b4ec13008e117d0efd76c1d_

```
  268 |     {
  269 |       name: 'ECDH',
  270 |       namedCurve: curve.web,
```

_file_excerpt · [src/crypto/public_key/elliptic/oid_curves.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/oid_curves.js#L324) · line 324 · SHA-256 dbae0069b965a134528d3224723dbe1cd05dd4c423c0cd22d845e0b96c3a9996_

```
  323 |   // Note: ECDSA and ECDH key generation is structurally equivalent
  324 |   const ecdh = nodeCrypto.createECDH(nodeCurves[name]);
  325 |   ecdh.generateKeys();
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-04763 — Квантово-уязвимый X25519: роль не определена (5 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:X25519:general`
- Источник данных: src/crypto/public_key/elliptic/ecdh.js
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:44 UTC
- Балл приоритета: 35.3 / 100
- CVSS v3.1: неприменимо

11 упоминаний X25519 в 5 файл(ах), например src/crypto/public_key/elliptic/ecdh.js:92. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/crypto/public_key/elliptic/ecdh.js:92 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/crypto/public_key/elliptic/ecdh.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/ecdh.js#L92) · line 92 · SHA-256 33754afed28e070c6fe889d3028e51b53ef1b222bbaf8f8fb6756bf243d4c20e_

```
   91 |     case 'curve25519Legacy': {
   92 |       const { sharedSecret: [REDACTED] ephemeralPublicKey } = await ecdhXGenerateEphemeralEncryptionMaterial(enums.publicKey.x25519, Q.subarray(1));
   93 |       const publicKey = util.concatUint8Array([new Uint8Array([curve.wireFormatLeadingByte]), ephemeralPublicKey]);
```

_file_excerpt · [src/crypto/public_key/elliptic/ecdh.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/ecdh.js#L158) · line 158 · SHA-256 294a3fb06da976751217f842b6f6103deff0a00f190f61bc434ea854ef0e4cb5_

```
  157 |       const secretKey = [REDACTED]
  158 |       const sharedKey = await ecdhXRecomputeSharedSecret(enums.publicKey.x25519, V.subarray(1), Q.subarray(1), secretKey);
  159 |       return { secretKey, sharedKey }; // Note: sharedKey is little-endian here, unlike below
```

_file_excerpt · [src/crypto/public_key/elliptic/oid_curves.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/oid_curves.js#L189) · line 189 · SHA-256 085af22a63073285f9b41c8fd1580f25e34eee786fc9c93549f81de299b1dc3a_

```
  188 |         // the private key must be stored in big endian and already clamped: https://www.ietf.org/archive/id/draft-ietf-openpgp-crypto-refresh-13.html#section-5.5.5.6.1.1-3
  189 |         const { k, A } = await ecdhXGenerate(enums.publicKey.x25519);
  190 |         const privateKey = [REDACTED]
```

_file_excerpt · [src/crypto/public_key/elliptic/oid_curves.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/oid_curves.js#L263) · line 263 · SHA-256 06a2e4b692ec06cd2f2668c4defc241cabf6aa423908d36123d1b82fa220a96e_

```
  262 |     }
  263 |     return ecdhXValidateParams(enums.publicKey.x25519, Q.subarray(1), dLittleEndian);
  264 |   }
```

_file_excerpt · [src/crypto/public_key/post_quantum/kem/ecc_kem.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/post_quantum/kem/ecc_kem.js#L9) · line 9 · SHA-256 61f4944eac6993ac9bc705985a4ca6e817fe3e097fc73a0729ec47f9df0acc31_

```
    8 |     case enums.publicKey.mlkem768X25519: {
    9 |       const { A, k } = await ecdhX.generate(enums.publicKey.x25519);
   10 |       return {
```

_file_excerpt · [src/crypto/public_key/post_quantum/kem/ecc_kem.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/post_quantum/kem/ecc_kem.js#L23) · line 23 · SHA-256 a072232312f37979fc0f350cae28c9be08729c30e6d4b0a81c003d5a2f924fd0_

```
   22 |     case enums.publicKey.mlkem768X25519: {
   23 |       const { ephemeralPublicKey: eccCipherText, sharedSecret: [REDACTED] } = await ecdhX.generateEphemeralEncryptionMaterial(enums.publicKey.x25519, eccRecipientPublicKey);
   24 | 
```

_file_excerpt · [src/crypto/public_key/post_quantum/kem/ecc_kem.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/post_quantum/kem/ecc_kem.js#L38) · line 38 · SHA-256 e24fdf348a018c86e5ac263481e36f6c24c92db544237676c517d1bc0d7c8122_

```
   37 |     case enums.publicKey.mlkem768X25519: {
   38 |       const eccKeyShare = await ecdhX.recomputeSharedSecret(enums.publicKey.x25519, eccCipherText, eccPublicKey, eccSecretKey);
   39 |       return eccKeyShare;
```

_file_excerpt · [src/enums.d.ts](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/enums.d.ts#L77) · line 77 · SHA-256 51bcc65cc5abe5fd7bb19e52368c5e477cac45493cdb751d3a8e4abe399ccdb6_

```
   76 | 
   77 |   export type publicKeyNames = 'rsaEncryptSign' | 'rsaEncrypt' | 'rsaSign' | 'elgamal' | 'dsa' | 'ecdh' | 'ecdsa' | 'eddsaLegacy' | 'aedh' | 'aedsa' | 'ed25519' | 'x25519' | 'ed448' | 'x448' | 'mlkem768X25519' | 'mldsa65Ed25519';
   78 |   export enum publicKey {
```

_file_excerpt · [src/enums.d.ts](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/enums.d.ts#L89) · line 89 · SHA-256 3e0f0dc265cee6d852a925e4e23941bd5bae8987249ecfe7607016fe88d0fb48_

```
   88 |     aedsa = 24,
   89 |     x25519 = 25,
   90 |     x448 = 26,
```

_file_excerpt · [src/enums.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/enums.js#L93) · line 93 · SHA-256 2abe536f7602f2ea77e7707a22b274dd3d1d46f3120d3844e4c048920a94af2e_

```
   92 |     /** X25519 (Encrypt only) */
   93 |     x25519: 25,
   94 |     /** X448 (Encrypt only) */
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-04765 — Квантово-уязвимый RSA: роль не определена (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:RSA:general`
- Источник данных: src/crypto/public_key/rsa.js
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:44 UTC
- Балл приоритета: 35.3 / 100
- CVSS v3.1: неприменимо

4 упоминаний RSA в 1 файл(ах), например src/crypto/public_key/rsa.js:162. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/crypto/public_key/rsa.js:162 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/crypto/public_key/rsa.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/rsa.js#L162) · line 162 · SHA-256 b0cbb193503eeb88bf6bc5592bf1fd5c47d7ad63d3c813b6cd2e4f794ff32445_

```
  161 |     const keyGenOpt = {
  162 |       name: 'RSASSA-PKCS1-v1_5',
  163 |       modulusLength: bits, // the specified keysize in bits
```

_file_excerpt · [src/crypto/public_key/rsa.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/rsa.js#L184) · line 184 · SHA-256 d75d3961fa30018d8b20a2bec1167b41ed845cbe35528febd5214c22eda40a26_

```
  183 |     const jwk = await new Promise((resolve, reject) => {
  184 |       nodeCrypto.generateKeyPair('rsa', opts, (err, _, jwkPrivateKey) => {
  185 |         if (err) {
```

_file_excerpt · [src/crypto/public_key/rsa.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/rsa.js#L264) · line 264 · SHA-256 53874c8c2c39e251bb82434c3249acca1da7f567fd83b00687a98795e3b3caab_

```
  263 |   const algo = {
  264 |     name: 'RSASSA-PKCS1-v1_5',
  265 |     hash: { name: hashName }
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-04760 — Использование MD5 в src/crypto/hash/index.js

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `file:src/crypto/hash/index.js`
- Источник данных: src/crypto/hash/index.js
- Метод обнаружения: Сопоставление регулярных выражений с API конкретного языка.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:44 UTC
- Балл приоритета: 34.3 / 100
- CVSS v3.1: неприменимо

1 мест(а) использования MD5 (первое — строка 78).

**Возможные последствия.** При использовании для подписей, хранения паролей, защиты целостности или генерации токенов возможна эксплуатация коллизий. Для несекретных контрольных сумм допустимо.

**Шаги воспроизведения.**

```
Откройте строка 78 в предоставленном файле src/crypto/hash/index.js и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/crypto/hash/index.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/hash/index.js#L78) · line 78 · SHA-256 37bf736791dde606da49f3d3749ab6d97bbb3b0c6fc06aa5255a6610d4392a66_

```
   76 |   switch (algo) {
   77 |     case enums.hash.md5:
   78 |       return md5(data);
   79 |     case enums.hash.sha1:
   80 |       return sha1(data);
```

**Ограничения проверки.** Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Замените на SHA-256/SHA-3 (Argon2/bcrypt для паролей) там, где это влияет на безопасность.

**Повторная проверка.** Повторно просканируйте код и проверьте места вызова из доказательства.

### QSI-2026-04761 — Использование SHA-1 в src/crypto/hash/index.js

- Серьёзность: **Средняя** · Классификация: Потенциальный криптографический риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `file:src/crypto/hash/index.js`
- Источник данных: src/crypto/hash/index.js
- Метод обнаружения: Сопоставление регулярных выражений с API конкретного языка.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:44 UTC
- Балл приоритета: 34.3 / 100
- CVSS v3.1: неприменимо

1 мест(а) использования SHA-1 (первое — строка 80).

**Возможные последствия.** При использовании для подписей, хранения паролей, защиты целостности или генерации токенов возможна эксплуатация коллизий. Для несекретных контрольных сумм допустимо.

**Шаги воспроизведения.**

```
Откройте строка 80 в предоставленном файле src/crypto/hash/index.js и изучите приведённые строки (см. доказательство).
```

**Подтверждающие доказательства.**

_file_excerpt · [src/crypto/hash/index.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/hash/index.js#L80) · line 80 · SHA-256 2bb3e32df818e85ca86b80b83efa65ddd49c199bade96c413185312ccd710b0e_

```
   78 |       return md5(data);
   79 |     case enums.hash.sha1:
   80 |       return sha1(data);
   81 |     case enums.hash.ripemd:
   82 |       return ripemd(data);
```

**Ограничения проверки.** Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Замените на SHA-256/SHA-3 (Argon2/bcrypt для паролей) там, где это влияет на безопасность.

**Повторная проверка.** Повторно просканируйте код и проверьте места вызова из доказательства.

### QSI-2026-04758 — Квантово-уязвимый ECDSA: роль не определена (7 файл(ов))

- Серьёзность: **Низкая** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: src/config.ts
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 12:44 UTC
- Балл приоритета: 28.3 / 100
- CVSS v3.1: неприменимо

13 упоминаний ECDSA в 7 файл(ах), например src/config.ts:369. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/config.ts:369 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/config.ts](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/config.ts#L369) · line 369 · SHA-256 c5db59fdcbe6ed4bb21e923d3d013f8150ee82531432e8c501ba83aea57a06c1_

```
  368 |    */
  369 |   rejectCurves: new Set([enums.curve.secp256k1])
  370 | };
```

_file_excerpt · [src/crypto/public_key/elliptic/noble_curves.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/noble_curves.js#L10) · line 10 · SHA-256 d339484c3d24ee7f0a65f3f6c881ae00e7f2e5c3ea93ab621e7ffa1749003a2d_

```
    9 | import { x448, ed448 } from '@noble/curves/ed448.js';
   10 | import { secp256k1 } from '@noble/curves/secp256k1.js';
   11 | import { brainpoolP256r1, brainpoolP384r1, brainpoolP512r1 } from '@noble/curves/misc.js';
```

_file_excerpt · [src/crypto/public_key/elliptic/noble_curves.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/noble_curves.js#L20) · line 20 · SHA-256 256a4ebbf585ae607de0248487d875bff7cbc60abef68e287c9d2b026e0088b4_

```
   19 |   brainpoolP512r1,
   20 |   secp256k1,
   21 |   x448,
```

_file_excerpt · [src/crypto/public_key/elliptic/oid_curves.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/oid_curves.js#L41) · line 41 · SHA-256 efbb3e14bd355823baff05fd7e74cb47297988aab466ed4e15e01f82d5bd7032_

```
   40 | const nodeCurves = nodeCrypto ? {
   41 |   [enums.curve.secp256k1]: knownCurves.includes('secp256k1') ? 'secp256k1' : undefined,
   42 |   [enums.curve.nistP256]: knownCurves.includes('prime256v1') ? 'prime256v1' : undefined,
```

_file_excerpt · [src/crypto/public_key/elliptic/oid_curves.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/oid_curves.js#L42) · line 42 · SHA-256 49f43e42cd4df4962d3fb7ea9ad262602f69f27be96debf7a2e0c5850b5200f3_

```
   41 |   [enums.curve.secp256k1]: knownCurves.includes('secp256k1') ? 'secp256k1' : undefined,
   42 |   [enums.curve.nistP256]: knownCurves.includes('prime256v1') ? 'prime256v1' : undefined,
   43 |   [enums.curve.nistP384]: knownCurves.includes('secp384r1') ? 'secp384r1' : undefined,
```

_file_excerpt · [src/crypto/public_key/elliptic/oid_curves.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/crypto/public_key/elliptic/oid_curves.js#L86) · line 86 · SHA-256 aeaa982bd5f9fbf62cac44e5be94c099de8292755a9abb1a8b08f36492fd3dde_

```
   85 |   },
   86 |   [enums.curve.secp256k1]: {
   87 |     oid: [0x06, 0x05, 0x2B, 0x81, 0x04, 0x00, 0x0A],
```

_file_excerpt · [src/enums.d.ts](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/enums.d.ts#L113) · line 113 · SHA-256 1e886ad8295c1de43a7adecc20929a406bcb5b7c9bf8d8152755b414a8565342_

```
  112 |     curve25519Legacy = 'curve25519Legacy',
  113 |     secp256k1 = 'secp256k1',
  114 |     brainpoolP256r1 = 'brainpoolP256r1',
```

_file_excerpt · [src/enums.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/enums.js#L32) · line 32 · SHA-256 45efce41a21d89e8da3215093aeb57cf9c1ab6d75d7ce992e3b0ca5296eaa95b_

```
   31 |     /** SECG SECP256k1 Curve */
   32 |     'secp256k1':              'secp256k1',
   33 | 
```

_file_excerpt · [src/index.d.ts](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/index.d.ts#L677) · line 677 · SHA-256 79115c16a34a64e10cbf419c921b1f950b76ee4ba788294e1fbe7bc747446279_

```
  676 | 
  677 | export type EllipticCurveName = 'ed25519Legacy' | 'curve25519Legacy' | 'nistP256' | 'nistP384' | 'nistP521' | 'secp256k1' | 'brainpoolP256r1' | 'brainpoolP384r1' | 'brainpoolP512r1';
  678 | 
```

_file_excerpt · [src/type/oid.js](https://github.com/openpgpjs/openpgpjs/blob/8bc35df4887933a3b2661e3741b33ba5f347b935/src/type/oid.js#L43) · line 43 · SHA-256 c3397494df5c3355f392a24b9cc3572a1eed7ea01393c68d2999992c77a5d4b2_

```
   42 |   '2b81040023': enums.curve.nistP521,
   43 |   '2b8104000a': enums.curve.secp256k1,
   44 |   '2b06010401da470f01': enums.curve.ed25519Legacy,
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-04766 — 71 бюллетеней в 23 пакет(ах) npm, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:npm:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-28 12:44 UTC
- Балл приоритета: 15.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 71 бюллетеней (30 с оценкой high или critical) для 23 пакет(ов) npm, которые подтягивают только инструменты разработки или сборки (package-lock.json): например, @humanfs/node@0.16.7 [dev]: GHSA-p498-v437-472g; basic-ftp@5.3.1 [dev]: GHSA-c475-qrg2-pj4r; brace-expansion@1.1.18 [dev]: GHSA-6j4f-fj2g-mc7p, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7; brace-expansion@2.1.4 [dev]: GHSA-6j4f-fj2g-mc7p, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7; brace-expansion@5.0.6 [dev]: GHSA-3jxr-9vmj-r5cp, GHSA-6j4f-fj2g-mc7p, GHSA-mh99-v99m-4gvg, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в package-lock.json.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · package-lock.json · SHA-256 04859aea607eeb6e0eee59480e26ef786e776b704c2aa89bf4a9cb23ebcb0c63_

```
@humanfs/node@0.16.7 [dev]: GHSA-p498-v437-472g
basic-ftp@5.3.1 [dev]: GHSA-c475-qrg2-pj4r
brace-expansion@1.1.18 [dev]: GHSA-6j4f-fj2g-mc7p, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7
brace-expansion@2.1.4 [dev]: GHSA-6j4f-fj2g-mc7p, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7
brace-expansion@5.0.6 [dev]: GHSA-3jxr-9vmj-r5cp, GHSA-6j4f-fj2g-mc7p, GHSA-mh99-v99m-4gvg, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895
brace-expansion@5.0.9 [dev]: GHSA-6j4f-fj2g-mc7p, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7
deepmerge@4.3.1 [dev]: GHSA-gcqx-w48m-w2h4
deepmerge-ts@7.1.6 [dev]: GHSA-ggr8-5vv4-36mx
diff@7.0.0 [dev]: GHSA-73rr-hh4g-fpgx
extract-zip@2.0.1 [dev]: GHSA-7pqw-9j4j-h8q3, GHSA-jmr9-qjv8-65gv
ip-address@10.5.0 [dev]: GHSA-2vr4-cq9g-pvrc, GHSA-h3mg-xc3c-68pw, GHSA-j6r3-76f7-8jcv, GHSA-rpw4-54j3-4h4q, GHSA-rxp7-6hxx-x8q5
js-yaml@4.3.1 [dev]: GHSA-2883-xcg3-v3hh
markdown-it@14.3.0 [dev]: GHSA-253c-mchw-3w2r, GHSA-gfr2-rv44-r23c, GHSA-r7fv-28h4-cvq7, GHSA-vfgh-jcmw-g37q
pug@2.0.4 [dev]: GHSA-3965-hpx2-q597, GHSA-p493-635q-r6gr
pug-code-gen@2.0.3 [dev]: GHSA-3965-hpx2-q597
qs@6.15.3 [dev]: GHSA-4mjr-xmp4-gh2g, GHSA-6pq8-jhm2-2vcw, GHSA-x5fp-wj9c-mxmx
serialize-javascript@6.0.2 [dev]: GHSA-5c6j-r48x-rmvq, GHSA-m5mm-p8h7-m29v, GHSA-qj8w-gfj5-8c6v
serialize-javascript@7.0.5 [dev]: GHSA-m5mm-p8h7-m29v
source-map-js@1.2.1 [dev]: GHSA-68fv-2mgg-jv7q
undici@6.28.0 [dev]: GHSA-2m5v-pch6-74hx, GHSA-3wwx-pv8p-q78v, GHSA-4qv8-2p9j-2685, GHSA-9fm3-97px-rjf6, GHSA-qrxm-fqhp-jwvm, GHSA-r53p-7pc4-xj5r, GHSA-rfgv-xxqx-mfg5, GHSA-xjj6-f33q-929c
undici@7.29.0 [dev]: GHSA-2gqq-gqf2-x968, GHSA-2jfj-6hjv-fm6j, GHSA-2m5v-pch6-74hx, GHSA-3wwx-pv8p-q78v, GHSA-3xpg-4rpp-hhhm, GHSA-4qv8-2p9j-2685, GHSA-4w7w-5xrc-9h26, GHSA-55wc-3pg8-jfw6, GHSA-8436-99hf-9mmv, GHSA-9fm3-97px-rjf6, GHSA-f72v-6w45-q472, GHSA-pmjh-fq2x-6v4x, GHSA-qrxm-fqhp-jwvm, GHSA-r53p-7pc4-xj5r, GHSA-rfgv-xxqx-mfg5, GHSA-rx4f-c7p8-82vq, GHSA-w293-vg96-wgc3, GHSA-xjj6-f33q-929c
vue-template-compiler@2.7.16 [dev]: GHSA-g3ch-rx76-35fx
zod@3.25.76 [dev]: GHSA-mrhx-c7xc-m3w5
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.


## 8. Постквантовая оценка

| | Обмен ключами (x — сколько данные должны оставаться конфиденциальными; «собери сейчас, расшифруй потом») | Подписи (x — сколько подписи и ключи должны оставаться доверенными) |
|---|---|---|
| Срок жизни данных/ключей x | 10 | 5 |
| Время миграции y | 3 | 3 |
| Принятое число лет до CRQC z | 8 (early) | 8 |
| x + y − z | 5 → при этом сценарии миграция завершится слишком поздно | 0 → запас минимален |
#### Откуда взято z

Усреднённая оценка экспертов, что CRQC появится в пределах горизонта, из ежегодного опроса, который публикует автор этого неравенства. Это оценки вероятности, а не предсказание даты.

| В пределах | Вероятность | Формулировка отчёта |
|---|---|---|
| 5 лет | ~15% | усреднённая оценка |
| 10 лет | 28-49% | вполне возможно |
| 15 лет | 51-70% | вероятно |

**Почему выбран этот сценарий (early, z = 8):** Внутри 10-летнего горизонта, которому опрос даёт 28-49% («вполне возможно»), и согласуется с оценкой BSI в 15 лет, которая «может сократиться до 10 или меньше». Для данных с десятилетиями конфиденциальности, где ошибка дорога.
_Допущения планирования: x для обмена ключами, x для подписей, y — значения по умолчанию профиля риска «Разработчик ПО безопасности», а не данные клиента; с фактическими сроками клиента вывод может измениться._

### Постквантовая зрелость: Уровень 2 из 4 — постквантовое используется вне критичных путей

- Используется: ML-DSA, ML-KEM — src/crypto/public_key/post_quantum/noble_post_quantum.ts
- Есть, но не подключено: ML-KEM — src/crypto/public_key/post_quantum/kem/ml_kem.js
- Есть, но не подключено: ML-DSA — src/crypto/public_key/post_quantum/signature/ml_dsa.js
- Постквантовая библиотека объявлена в зависимостях
- Только классика — обёртка ключей и шифрование хранимых данных: ECDH, X25519 (5 файл(ов))

**Следующий шаг:** Распространите постквантовую защиту на критичные роли, которые остаются классическими, начиная с того, что можно записать уже сегодня (обёрнутые ключи, обмен ключами в канале).

_Уровни: 0 — нет; 1 — есть, но не подключено; 2 — используется вне критичных путей; 3 — гибрид в критичном пути; 4 — постквантовое по умолчанию в критичных путях (корень доверия, обёртка ключей, обмен ключами в канале). Оценка по коду и манифестам._

### Что делают квантово-уязвимые алгоритмы

| Роль | Алгоритмы (файлы) | ID | Первый шаг |
|---|---|---|---|
| **обёртка ключей и шифрование хранимых данных** | X25519 (5), ECDH (1) | QSI-2026-04759, QSI-2026-04764 | Оборачивайте ключи ML-KEM или гибридным KEM (X25519 + ML-KEM-768) и переоберните хранимые ключи; для данных, которые уже могли скопировать, нужна отдельная оценка |
| **роль не определена** | ECDSA (7), X25519 (5), ECDH (2), RSA (1) | QSI-2026-04758, QSI-2026-04762, QSI-2026-04763, QSI-2026-04765 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — факторизация | взламывает | Q1 | RSA (2) | Взламывает RSA при любой длине ключа: более длинный модуль лишь полиномиально повышает стоимость. Планируйте переход на ML-KEM (или гибрид) для установления ключей и ML-DSA / SLH-DSA для подписей; начинайте с ключей, защищающих данные, которые должны оставаться конфиденциальными годами («собери сейчас — расшифруй потом»), и с долгоживущих подписей. |
| Алгоритм Шора — дискретный логарифм в конечных полях | взламывает | Q1 | DSA (3), ElGamal (1) | Взламывает Диффи–Хеллмана в конечных полях и DSA при любом размере. Переводите установление ключей на ML-KEM (на переходный период — гибрид с X25519 или ECDH), подписи — на ML-DSA или SLH-DSA. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | ECDH (5), ECDSA (12), Ed25519 (2), X25519 (10) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | 3DES (2), Argon2 (1), Blowfish (2), CAST5 (4), CMAC (1), DES (1), HKDF (1), HMAC (1), IDEA (1) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Алгоритм Саймона — суперпозиционные атаки на симметричные конструкции | только при суперпозиционных запросах | Q2 | GCM mode (1) | Для обычного применения AES-GCM или CBC-MAC действий не требуется — модель атаки неприменима. Зафиксируйте это как допущение модели; для конструкций типа Even–Mansour см. офлайн-вариант. |
| Квантовое решетчатое просеивание | учтено в стандартных параметрах | Q1 | ML-DSA (3), ML-KEM (3) | Для ML-KEM и ML-DSA в стандартных наборах параметров ничего менять не нужно. Заявление 2024 года о полиномиальном квантовом алгоритме для LWE отозвано после обнаружения ошибки (см. заявления). |

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
| P3 | QSI-2026-04760 | Проверьте каждое использование MD5 в src/crypto/hash/index.js; замените влияющие на безопасность на SHA-256 или функцию хеширования паролей. | устранение первопричины | Не осталось использований MD5, влияющих на безопасность. |
| P3 | QSI-2026-04761 | Проверьте каждое использование SHA-1 в src/crypto/hash/index.js; замените влияющие на безопасность на SHA-256 или функцию хеширования паролей. | устранение первопричины | Не осталось использований SHA-1, влияющих на безопасность. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-04759 | Внесите использования X25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-04764 | Внесите использования ECDH в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-04762 | Внесите использования ECDH в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-04763 | Внесите использования X25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-04765 | Внесите использования RSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-04758 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-04759 | Запланируйте миграцию X25519 на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-04764 | Запланируйте миграцию ECDH на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-04762 | Запланируйте миграцию ECDH на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-04763 | Запланируйте миграцию X25519 на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-04765 | Запланируйте миграцию RSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-04758 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-04766 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |

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
3. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
4. C. Gidney — How to factor 2048 bit RSA integers with less than a million noisy qubits (arXiv:2505.15917) — arXiv. <https://arxiv.org/abs/2505.15917> (preprint (2025-05-21): < 1 million noisy qubits, < 1 week, 0.1% gate error, 1 µs surface-code cycle)
5. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
6. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
7. CRYSTALS-Kyber — Algorithm Specifications and Supporting Documentation (round 3, 2021-08-04) — CRYSTALS team. <https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf> (NIST round-3 submission: core-SVP cost 2^{0.292β} classical, 2^{0.265β} quantum; Kyber768 166 quantum bits)
8. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
9. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
10. D. R. Simon — On the Power of Quantum Computation (SIAM J. Comput. 26, 1997) — SIAM. <https://doi.org/10.1137/S0097539796298637> (peer-reviewed article)
11. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
12. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
13. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
14. H. Kuwakado, M. Morii — Quantum distinguisher between the 3-round Feistel cipher and the random permutation (IEEE ISIT 2010) — IEEE. <https://ieeexplore.ieee.org/document/5513654> (peer-reviewed conference paper)
15. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
16. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
17. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
18. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
19. M. Ekerå, J. Gärtner — A high-level comparison of state-of-the-art quantum algorithms for breaking asymmetric cryptography (arXiv:2405.14381) — arXiv. <https://arxiv.org/abs/2405.14381> (preprint (2024-05-23): Regev-style algorithms show no overall advantage yet for cryptographic RSA and finite-field sizes)
20. M. Kaplan, G. Leurent, A. Leverrier, M. Naya-Plasencia — Breaking Symmetric Cryptosystems using Quantum Period Finding (CRYPTO 2016; arXiv:1602.05973) — Springer / arXiv. <https://arxiv.org/abs/1602.05973> (peer-reviewed article: superposition-query forgeries on CBC-MAC, PMAC, GMAC, GCM, OCB)
21. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
22. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
23. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/ipd> (initial public draft (November 2024); proposes deprecating quantum-vulnerable public-key algorithms after 2030 and disallowing them after 2035 — dates may change in the final version)
24. NIST SP 800-131A Rev. 2 — Transitioning the Use of Cryptographic Algorithms and Key Lengths — NIST. <https://csrc.nist.gov/pubs/sp/800/131/a/r2/final> (final (2019))
25. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
26. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
27. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
28. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
29. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| 3DES |  |  | слаб классически | устаревший | 2 | 2 | src/crypto/cipher/index.js:16; src/message.js:217 |
| Blowfish |  |  | слаб классически | устаревающий | 2 | 2 | src/crypto/cipher/blowfish.js; src/crypto/cipher/index.js:14 |
| CAST5 |  |  | слаб классически | устаревающий | 4 | 4 | src/crypto/cipher/cast5.js:600; src/crypto/cipher/index.js:13; src/crypto/cipherMode/cfb.js:40 |
| DES | DES |  | слаб классически | взломан | 1 | 1 | src/crypto/cipher/des.js |
| IDEA |  |  | слаб классически | устаревающий | 1 | 1 | src/crypto/cipherMode/cfb.js:38 |
| Argon2 |  |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/type/s2k/argon2.js |
| CMAC |  |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/crypto/cmac.js |
| HKDF |  |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/crypto/hkdf.js:15 |
| HMAC |  |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/crypto/aes_kw.js:47 |
| CBC mode |  |  | н/п | допустимо | 2 | 2 | src/crypto/cipherMode/cfb.js:170; src/crypto/cmac.js:87 |
| Crypto library | 2.4.0 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | 2.4.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | package-lock.json |
| Crypto library | ^2.4.0 | @noble/curves (noble-curves) | н/п | допустимо | 1 | 1 | package.json |
| Crypto library | ^2.4.0 | @noble/hashes (noble-hashes) | н/п | допустимо | 1 | 1 | package.json |
| GCM mode |  |  | н/п | допустимо | 1 | 1 | src/crypto/cipherMode/gcm.js:36 |
| OpenPGP |  |  | н/п | допустимо | 1 | 1 | src/openpgp.js |
| ML-DSA |  |  | постквантовый | допустимо | 1 | 1 | src/crypto/public_key/post_quantum/noble_post_quantum.ts:10 |
| ML-DSA | ML-DSA-65 |  | постквантовый | допустимо | 2 | 2 | src/crypto/public_key/post_quantum/noble_post_quantum.ts:10; src/crypto/public_key/post_quantum/signature/ml_dsa.js:30 |
| ML-KEM | ML-KEM-768 |  | постквантовый | допустимо | 2 | 2 | src/crypto/public_key/post_quantum/kem/ml_kem.js:30; src/crypto/public_key/post_quantum/noble_post_quantum.ts:9 |
| ML-KEM |  |  | постквантовый | допустимо | 1 | 1 | src/crypto/public_key/post_quantum/noble_post_quantum.ts:9 |
| PQC library | 0.7.1 | @noble/post-quantum (noble post-quantum) | постквантовый | допустимо | 1 | 1 | package-lock.json |
| PQC library | ^0.7.1 | @noble/post-quantum (noble post-quantum) | постквантовый | допустимо | 1 | 1 | package.json |
| DSA |  |  | уязвим (Шор) | устаревший | 3 | 3 | src/crypto/public_key/dsa.js; src/crypto/public_key/post_quantum/signature/ecc_dsa.js; src/crypto/public_key/post_quantum/signature/ml_dsa.js |
| ECDH |  |  | уязвим (Шор) | допустимо | 5 | 5 | src/crypto/public_key/elliptic/ecdh.js:249; src/crypto/public_key/elliptic/ecdh_x.js:69; src/crypto/public_key/elliptic/oid_curves.js:324 |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 7 | 7 | src/config.ts:369; src/crypto/public_key/elliptic/noble_curves.js:10; src/crypto/public_key/elliptic/oid_curves.js:41 |
| ECDSA |  |  | уязвим (Шор) | допустимо | 4 | 4 | src/crypto/public_key/elliptic/ecdsa.js; src/crypto/public_key/elliptic/oid_curves.js:311; src/crypto/public_key/post_quantum/kem/ecc_kem.js |
| ECDSA | P-256 |  | уязвим (Шор) | допустимо | 1 | 1 | src/crypto/public_key/elliptic/oid_curves.js:42 |
| Ed25519 |  |  | уязвим (Шор) | допустимо | 2 | 2 | src/crypto/public_key/elliptic/eddsa.js; src/crypto/public_key/elliptic/eddsa_legacy.js |
| ElGamal |  |  | уязвим (Шор) | устаревший | 1 | 1 | src/crypto/public_key/elgamal.js |
| RSA |  |  | уязвим (Шор) | допустимо | 2 | 2 | src/crypto/pkcs1.js; src/crypto/public_key/rsa.js:162 |
| X25519 | X25519 |  | уязвим (Шор) | допустимо | 10 | 10 | src/crypto/crypto.js:67; src/crypto/public_key/elliptic/ecdh.js:92; src/crypto/public_key/elliptic/ecdh_x.js:16 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| .jsdocrc.cjs | 649 | `8c230a656dc05c32569eb7c00de11413b9f13bf3f17a919f2bd5bed7632866ec` | 0 |
| README.md | 30090 | `176ee00dcebb1a4e32568659ef992f2f8ccbb9c553224c18f424b25a296ae3c6` | 7 |
| docs/index.html | 39869 | `ce6de6bfc583de901f2e9877affe7fc43a503548da25f6fbed1e781b60f0a190` | 7 |
| docs/scripts/linenumber.js | 671 | `823284680b49a0137de2d1474c93bf40c5a6da264dec349763f1001ab1f3c77d` | 0 |
| docs/scripts/prettify/lang-css.js | 861 | `9b6ac483033b02572714eb4d37ee199185c41008eb2b3f46a00ab0ebce6a20c5` | 0 |
| docs/scripts/prettify/prettify.js | 13632 | `e2e576e3bc607cd179ff511947010f645d3441a35313aec0dbd06c4437f83b77` | 0 |
| eslint.config.js | 6916 | `bb1983b1ff488d5ddb39e09685ff81eaff321237d6e58006a6a4c1d1d15961bb` | 0 |
| lightweight/package.json | 118 | `65f93c27dd99d120a293ef70f0c32760b0095cd17fafc890e4fc6297fbace460` | 0 |
| package-lock.json | 482592 | `04d6fd791775a89735de451d26f979a6b4b8b3b62b93857a5745933e3a43f0a8` | 0 |
| package.json | 5106 | `ad236c803bb9bdbc88e6797de35a8a3b29a8d1c6cfb2a003b2da413ce27df4c3` | 0 |
| rollup.config.js | 7506 | `215449d44802aec637abb5da4e22d558adbc9c96c717f95f8e0b6679c427e4d3` | 0 |
| src/cleartext.js | 9763 | `f1f6a4912d3b60159ca9cc6403ccfb113ac296f7a432193e106432b3837c935f` | 0 |
| src/config.ts | 18214 | `8b9ef728da3fffbd26b2a40ad002ae283638675d799febcf23c3d1521dc8da18` | 0 |
| src/crypto/aes_kw.js | 4007 | `802131a5d4bdcf5291f695c2ba274860a2a7160538bc4530c9110f190de8fca0` | 0 |
| src/crypto/biginteger.ts | 5524 | `a72713070d76783ccfb3f863f5df69073941c7996b66b39c2589cc7144642a36` | 0 |
| src/crypto/cipher/blowfish.js | 18036 | `fd05045fee2d948ff70a3909a819947bb2a63ef2e9bd9776d89f951a1766118c` | 0 |
| src/crypto/cipher/cast5.js | 35281 | `9bffb7fe602dc713b10b39f3283da5554df083fc7ccb10ba526f6f2adc0f05e5` | 0 |
| src/crypto/cipher/des.js | 19423 | `26c896c9f7554148d1359744ea1ca98902dd1732bdee42a0f781f800161c7e56` | 0 |
| src/crypto/cipher/index.js | 2058 | `7c91f1d6c91eaefd459d9d1c558403cdc0d5e2942507475abb83bce87213b2d7` | 0 |
| src/crypto/cipher/legacy_ciphers.js | 558 | `33b99f86d26646b2d4a40bcdcec87ff896b0c938b42c8ba1e656a72b120c51d7` | 0 |
| src/crypto/cipher/twofish.js | 9674 | `69132c33b96b583a8438542e4cb89ac84dcd98b474058c56ca0e4772a1bf7b1a` | 0 |
| src/crypto/cipherMode/cfb.js | 13365 | `f2df89a3f6fe9245ab7f85281ef933def0984b3d133adfee05b5d7012c6ea3d4` | 0 |
| src/crypto/cipherMode/eax.js | 6033 | `f8b26857331f1eb665e8eef9d7a2af5fcb4eb1d9b7c1aa8865acbc09a46eb12c` | 0 |
| src/crypto/cipherMode/gcm.js | 5058 | `13ddbb873c55acbe1942ed3b72e2ca21e83fe549f4d2230fa423082e2d514636` | 0 |
| src/crypto/cipherMode/index.js | 1011 | `3e5ccc8fc5b484e912d96cb070b70f5ed610db663e56a12208a87fc9a3c11388` | 0 |
| src/crypto/cipherMode/ocb.js | 9154 | `a7345e4507a97df867f576713c507e5b157cc80f38e4b318faefbe1621b61b94` | 0 |
| src/crypto/cmac.js | 3594 | `a501a3c39ebf2f29d30ae4dbd1a33b6976e6251ac687f890a6c15ff8b04b1223` | 0 |
| src/crypto/crypto.js | 24748 | `703c5ba10d7a165bbe449b6b3ca778dd0e7711788d21d01576612ab5592609bd` | 0 |
| src/crypto/hash/index.js | 4117 | `8d6b12940eb7cb6f7fbac8015b85edbef49ae21ec3f6ad0357777da6a72d8f06` | 0 |
| src/crypto/hash/noble_hashes.js | 551 | `7eae04d848e75d500e4dc1ce475e13478b39cdc10cc9a48f354e39e1ee48c24f` | 0 |
| src/crypto/hkdf.js | 695 | `4733faf0e6cc10941b02e1fe3215ad0a74bad6ea2a3d0110a92a689a54093f60` | 0 |
| src/crypto/index.js | 620 | `b2579dba894325e11e36773a746861b40f8b052fa7e763463f0e7b83a7001f7b` | 0 |
| src/crypto/pkcs1.js | 6703 | `04255de021496e704813ce5ed566afb2fc7ac7f28a42cbbf9a3b81b08bd9eadf` | 0 |
| src/crypto/pkcs5.js | 1880 | `ab120664b4e4ba1e2c3eec28bc47a0c3f434f7e60fec79982e1705e524240a68` | 0 |
| src/crypto/public_key/dsa.js | 6095 | `b0b8c388f086e4c2de58a994f99fb3633668b541410929156c3ee094d566af01` | 0 |
| src/crypto/public_key/elgamal.js | 4800 | `477414bd1cfaaf81351629726deecee091c4762306d8be0d965583a396fa9381` | 0 |
| src/crypto/public_key/elliptic/ecdh.js | 13028 | `a47c4f75e3480010db08a67c8f6c24843f725d43d0f54b5d03e5b488112cdc86` | 0 |
| src/crypto/public_key/elliptic/ecdh_x.js | 12266 | `75d82a69c31dde8ebcfe2718bbb1536d8cde0503581a40fa910a6fe5d972a801` | 0 |
| src/crypto/public_key/elliptic/ecdsa.js | 9927 | `39b45979cc019ea9532ebd0a268687144f25600790efd856cf421d5566973002` | 0 |
| src/crypto/public_key/elliptic/eddsa.js | 9111 | `8d2826d98c570bebb8a582a924592e9bfb8ef3d0b20471ea7ecd49701b8c6c99` | 0 |
| src/crypto/public_key/elliptic/eddsa_legacy.js | 3858 | `cc3a8b0debac9a2b1a7d4d581bad35c3847a1919bc687161bb55e76f5417c6f2` | 0 |
| src/crypto/public_key/elliptic/index.js | 1537 | `15265d4196c23c44d6b88cd4c213978b64f0c2565f822dcd8ecc9e42eed23db1` | 0 |
| src/crypto/public_key/elliptic/noble_curves.js | 682 | `2a1bfa8fe6029dbb5717478a4b87eed625a1c0a133f46172f67e5b0be794012c` | 0 |
| src/crypto/public_key/elliptic/oid_curves.js | 13764 | `a509143ad8b8e7b725cf5be5a976a1472ab7fc083ba1aae7f300deb0f3c99d7a` | 0 |
| src/crypto/public_key/index.js | 320 | `8c13b8b05bc07b38b219d5058e4b963c1b194caf8b10ec774afad6c8acd50b44` | 0 |
| src/crypto/public_key/post_quantum/index.js | 146 | `d6095c8c994762e3b63763737f9de2041a2f96e8ce3a14228e19cf5e969f49f4` | 0 |
| src/crypto/public_key/post_quantum/kem/ecc_kem.js | 1555 | `b71fb6b416bd690e166ffe0d1a2c174db710c090cf91093232a83ad73a80e04e` | 0 |
| src/crypto/public_key/post_quantum/kem/index.js | 168 | `f0e8179bb4b1ce0407f13ebb16769d03d2b25cbef8556a2f205b12765d0bcd60` | 0 |
| src/crypto/public_key/post_quantum/kem/kem.js | 2469 | `68afe7ee8655c755f4bad6a5e03036f1515bea6d033d95c7f152b73b828b0e5b` | 0 |
| src/crypto/public_key/post_quantum/kem/ml_kem.js | 2484 | `d67432c208c990bcd0f729282e63e13ab21f8a986129383b94096237b7c28ad5` | 0 |
| src/crypto/public_key/post_quantum/noble_post_quantum.ts | 418 | `246b031915f9f89fa8ee90543ee711a098bc555f78fb503c58ff3d5b65f2f08f` | 0 |
| src/crypto/public_key/post_quantum/signature/ecc_dsa.js | 1580 | `d33e5e033d65c6070a5e719d890da65c4678fa795c0c570eb73907476cf353eb` | 0 |
| src/crypto/public_key/post_quantum/signature/index.js | 192 | `1a96adc4ca627c7d1c3c0a27097813654b6032b71d116622eb485b42dd8a6f67` | 0 |
| src/crypto/public_key/post_quantum/signature/ml_dsa.js | 2375 | `b6e08589e5207dbc47ada3cd13d58405b223166304aaff1238c2bb45a23a16ce` | 0 |
| src/crypto/public_key/post_quantum/signature/signature.js | 2525 | `33918216a395320c0daa0d0f45c7969ad2c00181c76f860050a98739c30b0e23` | 0 |
| src/crypto/public_key/prime.ts | 8520 | `8acea275e5d6bd5f32f40cf6cb4e617dbe8c301a8428943fcb39bc40eda406de` | 0 |
| src/crypto/public_key/rsa.js | 14729 | `9558590f47e04e083ac6c292710d903d8acc039b7650a359cbbea25579775133` | 0 |
| src/crypto/random.js | 2445 | `97df8098201352705b53d453b7b0da3d6c0ddeb5a283421777cd573bc8c346dd` | 0 |
| src/crypto/signature.js | 11492 | `44a9d1f67306aada76336d5ba29abac1b2f8b2fe4951367e05ec282abc795024` | 0 |
| src/encoding/armor.js | 14928 | `389cffa77b54f3e8e84d5779776fd7da62ee7984424988ef9f748802499fe68c` | 1 |
| src/encoding/base64.js | 3990 | `44684bd982f778463348271de62ef7f2b4eed8bd2b8c4d6b877a45dc2f9ad919` | 0 |
| src/enums.d.ts | 5756 | `0f55028f6afa996e52c82dfb543b37dc2de7d3f35ce15e976aca1ba099542313` | 0 |
| src/enums.js | 15129 | `ef596e9696993aaec65875ccd0374f47c6c1177d2d072a0d79c257ef3b5cdd8e` | 0 |
| src/index.d.ts | 35799 | `4bdc54675e0aa0916483fd28c05bfc13e02e4c47580a01bff057a26691491bee` | 0 |
| src/index.js | 859 | `9e33556836285817a5ec857fd92e419a4409b6dbf655c5186217d17da84fd025` | 0 |
| src/key/factory.js | 20344 | `030141c22d59ba2c519c91a68132cb3cc517c33b5a27251d2f8ccc17db34b181` | 0 |
| src/key/helper.js | 25115 | `ad6b24fa9a009ce5e8dc3435ebc92514a60b72f151a08d6d3e262be0e02f1c61` | 0 |
| src/key/index.js | 635 | `128d97a529dda65a49cdb51ec1cebea1a8f54f683f9b7d6b74df11076d80e61b` | 0 |
| src/key/key.js | 32376 | `b91ea74bc92d3153948e7ac0db3188a8c44fa6124700e1f489d6d5714aa67540` | 0 |
| src/key/private_key.js | 11329 | `b3b3e766bc88bc9cf49e06fe41f83116ab05e115d25e2e9c9bbe90e20dc8dfdd` | 0 |
| src/key/public_key.js | 2297 | `5a47c4ccfaaec14a423a8c7fd77448949eb4bb7c647d7cafdd7265f1a8b508d6` | 0 |
| src/key/subkey.js | 8378 | `6be788c445b9decaa5163d473c1e9733c46a15a4ec3e435b4568ba96a1661e8f` | 0 |
| src/key/user.js | 10961 | `f6cae0a64a5238faf128f08d6d7cab96dd1da1b3362a934fc8ea61b5eebdbeb4` | 0 |
| src/message.js | 45894 | `52f89b40657bef5227e9f0016e8f5ac31ee1fb0913ac31ff8b733e3d81004507` | 0 |
| src/openpgp.js | 41155 | `8eeb09ac4b65bbbe129e6d178eafd707aa3520c735749b818a8dc58235677faa` | 0 |
| src/packet/aead_encrypted_data.js | 5150 | `02009ca2a904e326440365d30ade6dd121ba9237e9d352510532bc8b80643840` | 0 |
| src/packet/all_packets.js | 1418 | `377fc3e05dc1bfcd3298aaf6b5cc57d0a8ff85b73495f0e7dad362ab23e36ea1` | 0 |
| src/packet/compressed_data.js | 10985 | `fc034cb055a92bf21a5f4fcfe1be68b28a605c8a67cb633ab1b308095cd98e42` | 0 |
| src/packet/grammar.ts | 6135 | `b77ab2fd8b223b18d5c98760b620c5564a3de7afeff76d1cdecd94c0f31acaf5` | 0 |
| src/packet/index.js | 230 | `5c9892f01d0e6be45cd6794e5cc6a3b13d771d02d1fed5174349c112b58dbb2e` | 0 |
| src/packet/literal_data.js | 5531 | `0fbd61955639f7b79efaf3eaf3f763bba48b8ffdf6e9efd47f7fb15649c28b72` | 0 |
| src/packet/marker.js | 2193 | `cdfe2f58ffe727925be3be132c985554f2aa5f978c7143c548b1693134fa7a5d` | 0 |
| src/packet/one_pass_signature.js | 8362 | `b4688e15a30c78cd1efb0f30c45a96fbe1c5488ce6800dec1edb799fb47c3935` | 0 |
| src/packet/packet.js | 10161 | `1860fee73f00729284191ce06277ed37b71f66c7fa8f1d74a1d86059ec42593f` | 0 |
| src/packet/packetlist.js | 13132 | `25440a0a4e9ca74f6b4be0a46165f5ad859ee0b54d4d74645b1eeb464f3459a4` | 0 |
| src/packet/padding.js | 2045 | `46db53004f16807ea4f4a30cdd8b120587ddac5c8d4986a44153ad4ac0b0e411` | 0 |
| src/packet/public_key.js | 9961 | `2ee99e44145016ea51b84ff354fa8bb0b1beca0b0eb85f7f6ded1e17bf5aeb33` | 0 |
| src/packet/public_key_encrypted_session_key.js | 12293 | `0962a8a0baca0a841dde5efe6a19fcc76b30f0f2eff7f5d03bc60e8c624aa627` | 0 |
| src/packet/public_subkey.js | 2278 | `affdecf700fd1c69bfcf32be74a9414d57ca31417e1771831ab910652d682528` | 0 |
| src/packet/secret_key.js | 22519 | `6a812e7fe488b380230aca527e02d773b3d41495fc20c29e506b79fa540dc395` | 0 |
| src/packet/secret_subkey.js | 1516 | `23e8a3f41c0ba5cf0eaf4a0c0dea077cec6d0f89222c8024ffd285d09992ccd6` | 0 |
| src/packet/signature.js | 34790 | `cab4afbdb7668dad2d07c43977119f1385ec082eec522b69489f65df01ab1edc` | 0 |
| src/packet/sym_encrypted_integrity_protected_data.js | 16234 | `b70ceee3b93eaef8665111bae2e224a5822532361e51b30e2339f836e7a9d2d8` | 0 |
| src/packet/sym_encrypted_session_key.js | 8910 | `201c7f83ba77e5debd727e1622c867e4a0af9867767a6d5d36bcd8a1f398d790` | 0 |
| src/packet/symmetrically_encrypted_data.js | 5086 | `42811aa930e6cee3537efcbc771db78b6b170925cf21cd3ae30f7df7ba27d2ad` | 0 |
| src/packet/trust.js | 1168 | `036f6038f0878324d3080bd44cf1764d62335ce34577d7d8562c531d044631ec` | 0 |
| src/packet/user_attribute.js | 3203 | `650c793c9afe48a609cf6fc460315a677989fcb604005143003b3a47deb68397` | 0 |
| src/packet/userid.js | 4844 | `c2252ac0b90f9ca7b2f8ab818f686b7e07c8cf84d1f031bb81924a296a00ef55` | 0 |
| src/signature.js | 4025 | `e9708dc7d10b26d0db876b84f8ccea3cdeaca384bdc509ab86188053a6a28a22` | 0 |
| src/type/ecdh_symkey.js | 1811 | `fcaaacde27d43882671a101586c69a019efe0a455596160ffe2d3364577a40ef` | 0 |
| src/type/ecdh_x_symkey.js | 1387 | `21c465dbcd71a7ee0d5c1baee645d4df1224d3801d6f228e0f80b9f978d4c4e2` | 0 |
| src/type/kdf_params.js | 2245 | `fd03d0651bfe99aa97682fe3ed25433ceed502fa4a17bb2e46a0170653e6e970` | 0 |
| src/type/keyid.js | 2869 | `991daaa2d2f574b31c4f7ddd6e48927a803db8c851562e55143da9e91af7278c` | 0 |
| src/type/oid.js | 3859 | `abeff52445230bffea6cc45ae2b3c1ac7bd2a99391391ad9f8fa607bcc93b8ff` | 0 |
| src/type/s2k/argon2.js | 4963 | `40ec86165ab3455069ffc18bc0b0f9d7022c09d6aeb80e06deaf3f4f0f4c19ba` | 0 |
| src/type/s2k/generic.js | 6189 | `db69b9d4cd0adb20bb912c34ff5a748eb1863de588425997bc4178c91aa24ed1` | 0 |
| src/type/s2k/index.js | 1433 | `0bd9c89caee022bd4194e57d6b2e04bb2b32ebe4816645431aa4ae8cde4fb43e` | 0 |
| src/util.js | 20979 | `bf139af9304ecf67f18e706c7e3f198752389cba4f2f28c08c7a3b035ee13f36` | 0 |
