# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** ethers-js @ 3ea4c226dd0b · ethers.js project — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-28 18:21 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 0ef970f7-1de5-4aaa-965a-3c8635f1d23b (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `59ba9aa8e8627d919a00be18246ec709d497ff78833c5c217a3bb0541b676a29` |
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

Проверка аналитика: подтверждено — 0, не применимо — 0, отклонено как ложные срабатывания — 12.

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/ethers-io/ethers.js> @ `3ea4c226dd0b3a074abf90748de9d11192027f4f` — ссылки в доказательствах открывают строки на этом коммите.

759 файлов, всего 3988480 байт, редактирований: 12; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 753 | docs.wrm/config.mjs: 90 lines scanned with 16 rule patterns and 122 registry patterns; lib.commonjs/_version.d.ts: 5 lines scanned with 16 rule patterns and 122 registry patterns; lib.commonjs/_version.js: 9 lines scanned with 16 rule patterns and 122 registry patterns |
| dependencies | проверено | 6 | lib.commonjs/package.json: 0 dependencies parsed (0 pinned); lib.esm/package.json: 0 dependencies parsed (0 pinned); misc/basedirs/lib.commonjs/package.json: 0 dependencies parsed (0 pinned) |
| osv_advisories | проверено | 1 | 162 pinned packages queried at OSV.dev; 6 affected (6 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree ethers-js at 3ea4c226dd0b3a074abf90748de9d11192027f4f. 759 files analysed; of 1764 files, 343 are test, fuzzing, benchmark or example code and were left out, 662 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **100** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 29.0%

## 7. Подробное описание находок

### QSI-2026-05818 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (26 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: lib.commonjs/crypto/signing-key.js
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:21 UTC
- Балл приоритета: 35.6 / 100
- CVSS v3.1: неприменимо

60 упоминаний ECDSA в 26 файл(ах), например lib.commonjs/crypto/signing-key.js:9. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте lib.commonjs/crypto/signing-key.js:9 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [lib.commonjs/crypto/signing-key.js](https://github.com/ethers-io/ethers.js/blob/3ea4c226dd0b3a074abf90748de9d11192027f4f/lib.commonjs/crypto/signing-key.js#L9) · line 9 · SHA-256 7ef35a38316b94e728ea05e5c31e334715e5e3602e9caebea9a982631c239309_

```
    8 | exports.SigningKey = void 0;
    9 | const secp256k1_1 = require("@noble/curves/secp256k1");
   10 | const index_js_1 = require("../utils/index.js");
```

_file_excerpt · [lib.commonjs/crypto/signing-key.js](https://github.com/ethers-io/ethers.js/blob/3ea4c226dd0b3a074abf90748de9d11192027f4f/lib.commonjs/crypto/signing-key.js#L49) · line 49 · SHA-256 6853aea5cfae93e258a69831a228d49230d842c5424728f5bfb82e16261c0a2f_

```
   48 |         (0, index_js_1.assertArgument)((0, index_js_1.dataLength)(digest) === 32, "invalid digest length", "digest", digest);
   49 |         const sig = secp256k1_1.secp256k1.sign((0, index_js_1.getBytesCopy)(digest), (0, index_js_1.getBytesCopy)(this.#privateKey), {
   50 |             lowS: true
```

_file_excerpt · [lib.commonjs/crypto/signing-key.js](https://github.com/ethers-io/ethers.js/blob/3ea4c226dd0b3a074abf90748de9d11192027f4f/lib.commonjs/crypto/signing-key.js#L82) · line 82 · SHA-256 064ed30b908a9a5154447af71529ee389c56267c804c950fe9e535d168f17b7f_

```
   81 |         const pubKey = SigningKey.computePublicKey(other);
   82 |         return (0, index_js_1.hexlify)(secp256k1_1.secp256k1.getSharedSecret((0, index_js_1.getBytesCopy)(this.#privateKey), (0, index_js_1.getBytes)(pubKey), false));
   83 |     }
```

_file_excerpt · [lib.commonjs/providers/abstract-signer.d.ts](https://github.com/ethers-io/ethers.js/blob/3ea4c226dd0b3a074abf90748de9d11192027f4f/lib.commonjs/providers/abstract-signer.d.ts#L42) · line 42 · SHA-256 2e10073276976a3b9236ff22acdfe75ed04096d960a55398e0469d92c8ad6819_

```
   41 |     abstract signMessage(message: string | Uint8Array): Promise<string>;
   42 |     abstract signTypedData(domain: TypedDataDomain, types: Record<string, Array<TypedDataField>>, value: Record<string, any>): Promise<string>;
   43 | }
```

_file_excerpt · [lib.commonjs/providers/abstract-signer.d.ts](https://github.com/ethers-io/ethers.js/blob/3ea4c226dd0b3a074abf90748de9d11192027f4f/lib.commonjs/providers/abstract-signer.d.ts#L67) · line 67 · SHA-256 2495c89bdab8fe1d1e67cc521129af53017e34e1d7663e370a4bf74d87925e52_

```
   66 |     signMessage(message: string | Uint8Array): Promise<string>;
   67 |     signTypedData(domain: TypedDataDomain, types: Record<string, Array<TypedDataField>>, value: Record<string, any>): Promise<string>;
   68 | }
```

_file_excerpt · [lib.commonjs/providers/abstract-signer.js](https://github.com/ethers-io/ethers.js/blob/3ea4c226dd0b3a074abf90748de9d11192027f4f/lib.commonjs/providers/abstract-signer.js#L244) · line 244 · SHA-256 d6d090327c45a224befa454f63b2686590c2ec6b5131716e45d32744300882fb_

```
  243 |     }
  244 |     async signTypedData(domain, types, value) {
  245 |         this.#throwUnsupported("typed-data", "signTypedData");
```

_file_excerpt · [lib.commonjs/providers/abstract-signer.js](https://github.com/ethers-io/ethers.js/blob/3ea4c226dd0b3a074abf90748de9d11192027f4f/lib.commonjs/providers/abstract-signer.js#L245) · line 245 · SHA-256 af6365aec67977c0ca5264e667a5cfe2baafa68e9a6ad43b7a113f428db7fb5e_

```
  244 |     async signTypedData(domain, types, value) {
  245 |         this.#throwUnsupported("typed-data", "signTypedData");
  246 |     }
```

_file_excerpt · [lib.commonjs/providers/provider-jsonrpc.d.ts](https://github.com/ethers-io/ethers.js/blob/3ea4c226dd0b3a074abf90748de9d11192027f4f/lib.commonjs/providers/provider-jsonrpc.d.ts#L208) · line 208 · SHA-256 ec731f4fe5e8838a247980357dd17cf47fcbc7cc4fcf945b4d32728cfb3c9469_

```
  207 |     signMessage(_message: string | Uint8Array): Promise<string>;
  208 |     signTypedData(domain: TypedDataDomain, types: Record<string, Array<TypedDataField>>, _value: Record<string, any>): Promise<string>;
  209 |     unlock(password: [REDACTED] Promise<boolean>;
```

_file_excerpt · [lib.commonjs/providers/provider-jsonrpc.js](https://github.com/ethers-io/ethers.js/blob/3ea4c226dd0b3a074abf90748de9d11192027f4f/lib.commonjs/providers/provider-jsonrpc.js#L205) · line 205 · SHA-256 5ae0c3df321d5d79915ac18b8b566dd14ef2f0d82f2e1635eb64a23097406f44_

```
  204 |     }
  205 |     async signTypedData(domain, types, _value) {
  206 |         const value = deepCopy(_value);
```

_file_excerpt · [lib.commonjs/providers/provider-jsonrpc.js](https://github.com/ethers-io/ethers.js/blob/3ea4c226dd0b3a074abf90748de9d11192027f4f/lib.commonjs/providers/provider-jsonrpc.js#L706) · line 706 · SHA-256 ae316bffc48c74621fc8348ceb3d5ee1a9fcca0d937fd7c8e0c4ffb1ae8a29b3_

```
  705 |                 personal_sign: "signMessage",
  706 |                 eth_signTypedData_v4: "signTypedData",
  707 |                 eth_signTransaction: "signTransaction",
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05823 — Квантово-уязвимый ECDSA: роль не определена (3 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: lib.commonjs/utils/errors.d.ts
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-28 18:21 UTC
- Балл приоритета: 34.2 / 100
- CVSS v3.1: неприменимо

3 упоминаний ECDSA в 3 файл(ах), например lib.commonjs/utils/errors.d.ts:433. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте lib.commonjs/utils/errors.d.ts:433 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [lib.commonjs/utils/errors.d.ts](https://github.com/ethers-io/ethers.js/blob/3ea4c226dd0b3a074abf90748de9d11192027f4f/lib.commonjs/utils/errors.d.ts#L433) · line 433 · SHA-256 a84563e1f30cb77a5f593227c00bb10d9f74bd03e2ffe46a12e78e71291e47da_

```
  432 |      */
  433 |     action: "requestAccess" | "sendTransaction" | "signMessage" | "signTransaction" | "signTypedData" | "unknown";
  434 |     /**
```

_file_excerpt · [lib.esm/utils/errors.d.ts](https://github.com/ethers-io/ethers.js/blob/3ea4c226dd0b3a074abf90748de9d11192027f4f/lib.esm/utils/errors.d.ts#L433) · line 433 · SHA-256 a84563e1f30cb77a5f593227c00bb10d9f74bd03e2ffe46a12e78e71291e47da_

```
  432 |      */
  433 |     action: "requestAccess" | "sendTransaction" | "signMessage" | "signTransaction" | "signTypedData" | "unknown";
  434 |     /**
```

_file_excerpt · [src.ts/utils/errors.ts](https://github.com/ethers-io/ethers.js/blob/3ea4c226dd0b3a074abf90748de9d11192027f4f/src.ts/utils/errors.ts#L569) · line 569 · SHA-256 c0f3b204ae084503587b8682861b9225330ad4a436e3eadb0624c06b44ae2095_

```
  568 |      */
  569 |     action: "requestAccess" | "sendTransaction" | "signMessage" | "signTransaction" | "signTypedData" | "unknown",
  570 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-05833 — 21 бюллетеней в 6 пакет(ах) npm, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies:npm:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:21 UTC
- Балл приоритета: 15.5 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 21 бюллетеней (12 с оценкой high или critical) для 6 пакет(ов) npm, которые подтягивают только инструменты разработки или сборки (package-lock.json): например, brace-expansion@1.1.13 [dev]: GHSA-3jxr-9vmj-r5cp, GHSA-6j4f-fj2g-mc7p, GHSA-mh99-v99m-4gvg, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895; brace-expansion@2.0.3 [dev]: GHSA-3jxr-9vmj-r5cp, GHSA-6j4f-fj2g-mc7p, GHSA-mh99-v99m-4gvg, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895; deepmerge@4.3.1 [dev]: GHSA-gcqx-w48m-w2h4; diff@7.0.0 [dev]: GHSA-73rr-hh4g-fpgx; js-yaml@4.1.1 [dev]: GHSA-2883-xcg3-v3hh, GHSA-52cp-r559-cp3m, GHSA-5p4m-2wfm-xmqj, GHSA-h67p-54hq-rp68. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в package-lock.json.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (npm)](https://osv.dev/) · package-lock.json · SHA-256 53cda0dec77a756f58bd280981cf6772e5faea8c2833526bdd685c6e623379c1_

```
brace-expansion@1.1.13 [dev]: GHSA-3jxr-9vmj-r5cp, GHSA-6j4f-fj2g-mc7p, GHSA-mh99-v99m-4gvg, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895
brace-expansion@2.0.3 [dev]: GHSA-3jxr-9vmj-r5cp, GHSA-6j4f-fj2g-mc7p, GHSA-mh99-v99m-4gvg, GHSA-q2hr-2g5m-vwhr, GHSA-qhr7-859c-m2p7, GHSA-rgw5-rvv9-x895
deepmerge@4.3.1 [dev]: GHSA-gcqx-w48m-w2h4
diff@7.0.0 [dev]: GHSA-73rr-hh4g-fpgx
js-yaml@4.1.1 [dev]: GHSA-2883-xcg3-v3hh, GHSA-52cp-r559-cp3m, GHSA-5p4m-2wfm-xmqj, GHSA-h67p-54hq-rp68
serialize-javascript@6.0.2 [dev]: GHSA-5c6j-r48x-rmvq, GHSA-m5mm-p8h7-m29v, GHSA-qj8w-gfj5-8c6v
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-05832 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя · _предварительно — требует дополнительной проверки_
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-28 18:21 UTC
- Балл приоритета: 13.3 / 100
- CVSS v3.1: неприменимо

В 6 манифестах зависимостей QSI нашёл криптобиблиотеки (@noble/curves, @noble/hashes), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · lib.commonjs/package.json, lib.esm/package.json, misc/basedirs/lib.commonjs/package.json, misc/basedirs/lib.esm/package.json, package-lock.json, package.json · SHA-256 078fb8046cd4bccf27a6ed674faeb8de9ef662abe519b61003925a76d1f6b779_

```
Crypto libraries: @noble/curves, @noble/hashes
```

**Ограничения проверки.** Отсутствие доказательств не является доказательством отсутствия: системные библиотеки и транзитивные зависимости могут не указываться.

**Рекомендация.** Определите источник поддержки PQC (TLS-терминатор, KMS/HSM, обновление библиотек).

**Повторная проверка.** Повторите сканирование после обновлений.

### Отклонено после проверки

_Эти находки аналитик отклонил как ложные срабатывания; в подсчётах отчёта они не учитываются._

| ID | Подробное описание находок | Проверка аналитика |
|---|---|---|
| QSI-2026-05819 | Возможный секрет в коде lib.commonjs/providers/provider-alchemy.js | Community default endpoint keys that ethers.js publishes on purpose, one per provider, in src.ts and in the committed lib.commonjs and lib.esm builds: defaultApiKey in provider-ankr, provider-alchemy and provider-blockscout, and defaultToken in provider-quicknode. Each is the fallback the constructor uses when the caller supplies no key — `if (apiKey == null) { apiKey = defaultApiKey; }` — so the library works unconfigured; each provider implements CommunityResourcable and calls showThrottleMessage, which is the library telling the user they are on a shared, rate-limited credential. Public by design, not leaked. Note that the first three were invisible to the detector until it learned to read a camelCase credential name on 2026-10-27, and only the Ankr one was ever reported, by the accident of being 64 hex characters long. |
| QSI-2026-05820 | Возможный секрет в коде lib.commonjs/providers/provider-ankr.js | Community default endpoint keys that ethers.js publishes on purpose, one per provider, in src.ts and in the committed lib.commonjs and lib.esm builds: defaultApiKey in provider-ankr, provider-alchemy and provider-blockscout, and defaultToken in provider-quicknode. Each is the fallback the constructor uses when the caller supplies no key — `if (apiKey == null) { apiKey = defaultApiKey; }` — so the library works unconfigured; each provider implements CommunityResourcable and calls showThrottleMessage, which is the library telling the user they are on a shared, rate-limited credential. Public by design, not leaked. Note that the first three were invisible to the detector until it learned to read a camelCase credential name on 2026-10-27, and only the Ankr one was ever reported, by the accident of being 64 hex characters long. |
| QSI-2026-05821 | Возможный секрет в коде lib.commonjs/providers/provider-blockscout.js | Community default endpoint keys that ethers.js publishes on purpose, one per provider, in src.ts and in the committed lib.commonjs and lib.esm builds: defaultApiKey in provider-ankr, provider-alchemy and provider-blockscout, and defaultToken in provider-quicknode. Each is the fallback the constructor uses when the caller supplies no key — `if (apiKey == null) { apiKey = defaultApiKey; }` — so the library works unconfigured; each provider implements CommunityResourcable and calls showThrottleMessage, which is the library telling the user they are on a shared, rate-limited credential. Public by design, not leaked. Note that the first three were invisible to the detector until it learned to read a camelCase credential name on 2026-10-27, and only the Ankr one was ever reported, by the accident of being 64 hex characters long. |
| QSI-2026-05822 | Возможный секрет в коде lib.commonjs/providers/provider-quicknode.js | Community default endpoint keys that ethers.js publishes on purpose, one per provider, in src.ts and in the committed lib.commonjs and lib.esm builds: defaultApiKey in provider-ankr, provider-alchemy and provider-blockscout, and defaultToken in provider-quicknode. Each is the fallback the constructor uses when the caller supplies no key — `if (apiKey == null) { apiKey = defaultApiKey; }` — so the library works unconfigured; each provider implements CommunityResourcable and calls showThrottleMessage, which is the library telling the user they are on a shared, rate-limited credential. Public by design, not leaked. Note that the first three were invisible to the detector until it learned to read a camelCase credential name on 2026-10-27, and only the Ankr one was ever reported, by the accident of being 64 hex characters long. |
| QSI-2026-05824 | Возможный секрет в коде lib.esm/providers/provider-alchemy.js | Community default endpoint keys that ethers.js publishes on purpose, one per provider, in src.ts and in the committed lib.commonjs and lib.esm builds: defaultApiKey in provider-ankr, provider-alchemy and provider-blockscout, and defaultToken in provider-quicknode. Each is the fallback the constructor uses when the caller supplies no key — `if (apiKey == null) { apiKey = defaultApiKey; }` — so the library works unconfigured; each provider implements CommunityResourcable and calls showThrottleMessage, which is the library telling the user they are on a shared, rate-limited credential. Public by design, not leaked. Note that the first three were invisible to the detector until it learned to read a camelCase credential name on 2026-10-27, and only the Ankr one was ever reported, by the accident of being 64 hex characters long. |
| QSI-2026-05825 | Возможный секрет в коде lib.esm/providers/provider-ankr.js | Community default endpoint keys that ethers.js publishes on purpose, one per provider, in src.ts and in the committed lib.commonjs and lib.esm builds: defaultApiKey in provider-ankr, provider-alchemy and provider-blockscout, and defaultToken in provider-quicknode. Each is the fallback the constructor uses when the caller supplies no key — `if (apiKey == null) { apiKey = defaultApiKey; }` — so the library works unconfigured; each provider implements CommunityResourcable and calls showThrottleMessage, which is the library telling the user they are on a shared, rate-limited credential. Public by design, not leaked. Note that the first three were invisible to the detector until it learned to read a camelCase credential name on 2026-10-27, and only the Ankr one was ever reported, by the accident of being 64 hex characters long. |
| QSI-2026-05826 | Возможный секрет в коде lib.esm/providers/provider-blockscout.js | Community default endpoint keys that ethers.js publishes on purpose, one per provider, in src.ts and in the committed lib.commonjs and lib.esm builds: defaultApiKey in provider-ankr, provider-alchemy and provider-blockscout, and defaultToken in provider-quicknode. Each is the fallback the constructor uses when the caller supplies no key — `if (apiKey == null) { apiKey = defaultApiKey; }` — so the library works unconfigured; each provider implements CommunityResourcable and calls showThrottleMessage, which is the library telling the user they are on a shared, rate-limited credential. Public by design, not leaked. Note that the first three were invisible to the detector until it learned to read a camelCase credential name on 2026-10-27, and only the Ankr one was ever reported, by the accident of being 64 hex characters long. |
| QSI-2026-05827 | Возможный секрет в коде lib.esm/providers/provider-quicknode.js | Community default endpoint keys that ethers.js publishes on purpose, one per provider, in src.ts and in the committed lib.commonjs and lib.esm builds: defaultApiKey in provider-ankr, provider-alchemy and provider-blockscout, and defaultToken in provider-quicknode. Each is the fallback the constructor uses when the caller supplies no key — `if (apiKey == null) { apiKey = defaultApiKey; }` — so the library works unconfigured; each provider implements CommunityResourcable and calls showThrottleMessage, which is the library telling the user they are on a shared, rate-limited credential. Public by design, not leaked. Note that the first three were invisible to the detector until it learned to read a camelCase credential name on 2026-10-27, and only the Ankr one was ever reported, by the accident of being 64 hex characters long. |
| QSI-2026-05828 | Возможный секрет в коде src.ts/providers/provider-alchemy.ts | Community default endpoint keys that ethers.js publishes on purpose, one per provider, in src.ts and in the committed lib.commonjs and lib.esm builds: defaultApiKey in provider-ankr, provider-alchemy and provider-blockscout, and defaultToken in provider-quicknode. Each is the fallback the constructor uses when the caller supplies no key — `if (apiKey == null) { apiKey = defaultApiKey; }` — so the library works unconfigured; each provider implements CommunityResourcable and calls showThrottleMessage, which is the library telling the user they are on a shared, rate-limited credential. Public by design, not leaked. Note that the first three were invisible to the detector until it learned to read a camelCase credential name on 2026-10-27, and only the Ankr one was ever reported, by the accident of being 64 hex characters long. |
| QSI-2026-05829 | Возможный секрет в коде src.ts/providers/provider-ankr.ts | Community default endpoint keys that ethers.js publishes on purpose, one per provider, in src.ts and in the committed lib.commonjs and lib.esm builds: defaultApiKey in provider-ankr, provider-alchemy and provider-blockscout, and defaultToken in provider-quicknode. Each is the fallback the constructor uses when the caller supplies no key — `if (apiKey == null) { apiKey = defaultApiKey; }` — so the library works unconfigured; each provider implements CommunityResourcable and calls showThrottleMessage, which is the library telling the user they are on a shared, rate-limited credential. Public by design, not leaked. Note that the first three were invisible to the detector until it learned to read a camelCase credential name on 2026-10-27, and only the Ankr one was ever reported, by the accident of being 64 hex characters long. |
| QSI-2026-05830 | Возможный секрет в коде src.ts/providers/provider-blockscout.ts | Community default endpoint keys that ethers.js publishes on purpose, one per provider, in src.ts and in the committed lib.commonjs and lib.esm builds: defaultApiKey in provider-ankr, provider-alchemy and provider-blockscout, and defaultToken in provider-quicknode. Each is the fallback the constructor uses when the caller supplies no key — `if (apiKey == null) { apiKey = defaultApiKey; }` — so the library works unconfigured; each provider implements CommunityResourcable and calls showThrottleMessage, which is the library telling the user they are on a shared, rate-limited credential. Public by design, not leaked. Note that the first three were invisible to the detector until it learned to read a camelCase credential name on 2026-10-27, and only the Ankr one was ever reported, by the accident of being 64 hex characters long. |
| QSI-2026-05831 | Возможный секрет в коде src.ts/providers/provider-quicknode.ts | Community default endpoint keys that ethers.js publishes on purpose, one per provider, in src.ts and in the committed lib.commonjs and lib.esm builds: defaultApiKey in provider-ankr, provider-alchemy and provider-blockscout, and defaultToken in provider-quicknode. Each is the fallback the constructor uses when the caller supplies no key — `if (apiKey == null) { apiKey = defaultApiKey; }` — so the library works unconfigured; each provider implements CommunityResourcable and calls showThrottleMessage, which is the library telling the user they are on a shared, rate-limited credential. Public by design, not leaked. Note that the first three were invisible to the detector until it learned to read a camelCase credential name on 2026-10-27, and only the Ankr one was ever reported, by the accident of being 64 hex characters long. |

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
| **подпись транзакций и сообщений** | ECDSA (26) | QSI-2026-05818 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |
| **роль не определена** | ECDSA (3) | QSI-2026-05823 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | ECDSA (29) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | AES-128 (3), HMAC (10), Keccak-256 (27), PBKDF2 (10), RIPEMD-160 (5), SHA-2 (7), scrypt (5) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | Keccak-256 (27), RIPEMD-160 (5), SHA-2 (7) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

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
| P3 | QSI-2026-05818 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-05823 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-05818 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05823 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-05833 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |

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
19. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
20. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
21. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
22. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| RIPEMD-160 | RIPEMD-160 |  | слаб классически | устаревающий | 5 | 5 | lib.commonjs/crypto/ripemd160.d.ts; lib.commonjs/crypto/ripemd160.js; lib.esm/crypto/ripemd160.d.ts |
| HMAC |  |  | сниженный запас (Гровер), одобрен | допустимо | 10 | 10 | lib.commonjs/crypto/crypto-browser.d.ts:12; lib.commonjs/crypto/crypto-browser.js:33; lib.commonjs/crypto/hmac.d.ts |
| PBKDF2 |  |  | сниженный запас (Гровер), одобрен | допустимо | 10 | 10 | lib.commonjs/crypto/crypto-browser.d.ts:13; lib.commonjs/crypto/crypto-browser.js:39; lib.commonjs/crypto/pbkdf2.d.ts |
| SHA-2 | SHA-512 |  | сниженный запас (Гровер), одобрен | допустимо | 2 | 2 | lib.esm/crypto/sha2.js:7; src.ts/crypto/sha2.ts:13 |
| scrypt |  |  | сниженный запас (Гровер), одобрен | допустимо | 5 | 5 | lib.commonjs/crypto/scrypt.d.ts; lib.commonjs/crypto/scrypt.js; lib.esm/crypto/scrypt.d.ts |
| AES-128 | AES-128 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 3 | 3 | lib.commonjs/wallet/json-keystore.js:39; lib.esm/wallet/json-keystore.js:35; src.ts/wallet/json-keystore.ts:75 |
| Keccak-256 | Keccak-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 27 | 27 | lib.commonjs/crypto/keccak.d.ts:29; lib.commonjs/crypto/keccak.js:13; lib.esm/abi/interface.js:874 |
| SHA-2 |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 3 | 3 | lib.commonjs/crypto/sha2.d.ts; lib.commonjs/crypto/sha2.js; lib.esm/crypto/sha2.d.ts |
| SHA-2 | SHA-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 2 | 2 | lib.esm/crypto/sha2.js:4; src.ts/crypto/sha2.ts:9 |
| Crypto library | 1.2.0 | @noble/curves (noble-curves) | н/п | допустимо | 2 | 2 | package-lock.json; package.json |
| Crypto library | 1.3.2 | @noble/hashes (noble-hashes) | н/п | допустимо | 2 | 2 | package-lock.json; package.json |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 3 | 3 | lib.commonjs/crypto/signing-key.js:9; lib.esm/crypto/signing-key.js:6; src.ts/crypto/signing-key.ts:7 |
| ECDSA |  |  | уязвим (Шор) | допустимо | 26 | 26 | lib.commonjs/providers/abstract-signer.d.ts:42; lib.commonjs/providers/abstract-signer.js:244; lib.commonjs/providers/provider-jsonrpc.d.ts:208 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| docs.wrm/config.mjs | 2751 | `dc82b3e90910f435d884067d5e9c10bfeff69c0c5b15d6a83ed4da22212d9a84` | 0 |
| lib.commonjs/_version.d.ts | 119 | `31e313c0dba34e94e0135fe3b19bc3ee155a3958a96a6c60f9242612b6be23c6` | 0 |
| lib.commonjs/_version.js | 278 | `f0e5c3b54fe8023dc46d47b63c568fb396864b5928e5ee6e0a94b1e2f97d860a` | 0 |
| lib.commonjs/abi/abi-coder.d.ts | 2377 | `3ab09cdc78b5e435e38c90d4d6845abaa6b60adb4c28d1df89b4e957d4107cc9` | 0 |
| lib.commonjs/abi/abi-coder.js | 8609 | `13a2eecdf8f2bcb3b0c65e888f4b37ff791828d9aa6ab346a96da8f59e97fabd` | 0 |
| lib.commonjs/abi/bytes32.d.ts | 423 | `033d848b02f3948d2fb4feb7fba98e9cc3cba797b417210f30454491b2d9170c` | 0 |
| lib.commonjs/abi/bytes32.js | 1454 | `3ad6af4d1b7ca767bfab298b579585e7eebc56023c365f349507b3b3ef23657e` | 0 |
| lib.commonjs/abi/coders/abstract-coder.d.ts | 3881 | `67dbef5497f47d7f39dfd36d503a2fcd7235296f976ccd7be93bd2ec45945b3c` | 0 |
| lib.commonjs/abi/coders/abstract-coder.js | 16655 | `fb0661a9ab8bfc713b5c6230a240737a506c8129a100ef34714f5b1ea0571df2` | 0 |
| lib.commonjs/abi/coders/address.d.ts | 408 | `d432f5b818c23b022f0be4ac1b93583aac03a5dbbc2f23d2cfdc6acbd8116703` | 0 |
| lib.commonjs/abi/coders/address.js | 1081 | `8e7123a934a277af1c259b1569d25750676af41364d5d780022eedcada8b3ec6` | 0 |
| lib.commonjs/abi/coders/anonymous.d.ts | 452 | `7cec3e1a96117900f40511797aed1d1e68c3d7bd35d6b2a467f837bbe493e8ad` | 0 |
| lib.commonjs/abi/coders/anonymous.js | 756 | `8dad034d4aaaf1ab8bc0ac0831bc62b8e54555bd583053fa0d278ac93db4dece` | 0 |
| lib.commonjs/abi/coders/array.d.ts | 769 | `3124340589a03e45a24b79dd64cb60304a057bbec9776ea16f8d55f783a2b531` | 0 |
| lib.commonjs/abi/coders/array.js | 6372 | `37809d12e3c6498a447b64e81d1f6d8626765991578eb9174252f91e90f52a6c` | 0 |
| lib.commonjs/abi/coders/boolean.d.ts | 410 | `7129a090917912a223915b29cb712d00163521c75981fa8092115f335dc61b9f` | 0 |
| lib.commonjs/abi/coders/boolean.js | 710 | `0818096a027ddf2eadeb1eb45709d504338caf533828a08af43306d741a45195` | 0 |
| lib.commonjs/abi/coders/bytes.d.ts | 528 | `f85aa84e63c8d17429cd8161cca7125725a547e623623a6364d476587b89dcfe` | 0 |
| lib.commonjs/abi/coders/bytes.js | 1096 | `23fb072f86b863f15213beeb0f23a952cdce3ed4faf284d1370d808b6a3c2d29` | 0 |
| lib.commonjs/abi/coders/fixed-bytes.d.ts | 514 | `02c8003a0835f0db719b1c7e8d85548dc9c67a495debf53f91d40504c748336d` | 0 |
| lib.commonjs/abi/coders/fixed-bytes.js | 1175 | `0f191b350d75279a5e9b4ff6235fb0a83cdc63843dc8e1bde57e3e72f9db8d53` | 0 |
| lib.commonjs/abi/coders/null.d.ts | 351 | `2cf283bda00af2894f54d7afceca9e1c856c9c78110140da6ae23213ecebbd61` | 0 |
| lib.commonjs/abi/coders/null.js | 705 | `f4bbbb587ca6a367cd000876b5477b33b75ec547a75b006d39debcadda99e6ce` | 0 |
| lib.commonjs/abi/coders/number.d.ts | 558 | `7cfd40df82c249f56f5c37daeaf886941f11ab56595d657d7592d5de0fc17580` | 0 |
| lib.commonjs/abi/coders/number.js | 1944 | `f16f33da7e0599a3ca4ce3446428e5edd2221ee40fa391cbc03e8820b6e53d58` | 0 |
| lib.commonjs/abi/coders/string.d.ts | 421 | `cdd503d7c427abce5a90fef98ce394db81c0e24be8b01d049f7dc5077322ef1c` | 0 |
| lib.commonjs/abi/coders/string.js | 749 | `320975dd997b3cdd8f89afc261f849967d9cd1898f8f82c14196d2d7c6bc9c3c` | 0 |
| lib.commonjs/abi/coders/tuple.d.ts | 509 | `f89c44293da3f402e380d1893792088285af9b1f6782f02adc0410b4de1f5860` | 0 |
| lib.commonjs/abi/coders/tuple.js | 2182 | `b0a8a65b9932a5e4b4e56454365062ded028b6c0c06d155afa9d025372cd2509` | 0 |
| lib.commonjs/abi/fragments.d.ts | 14007 | `09c6791e3421ad7b5feff77120adcb3aca2f45b0caa48fa0eb5bbde333075257` | 0 |
| lib.commonjs/abi/fragments.js | 47525 | `dcaebe93b0a7c634a91bfeb57e16cd5653169eaa8f7caec75e5737cd6efe7684` | 0 |
| lib.commonjs/abi/index.d.ts | 1023 | `f09ab98499647d29d8f3a5e0a5c1194b5d24fa9e1b2f94e195d1555ca8ba4098` | 0 |
| lib.commonjs/abi/index.js | 3767 | `7a24b12137f26db188ff54e18380125f17dd32f9380440278f5f592ee4bbe429` | 0 |
| lib.commonjs/abi/interface.d.ts | 13957 | `2a54c89cbd1baefaed665291d05b9d28ac7356536c3f681f9401d642b2b0c0cd` | 0 |
| lib.commonjs/abi/interface.js | 42771 | `bc8afe177045695f66582bfeb40838968c73061e9425e134d7056a9ea6818851` | 0 |
| lib.commonjs/abi/typed.d.ts | 15351 | `74f763ea382866434fec07cd11967ac0fa2d94d3f9f98e4a908435ec98b2e0d5` | 0 |
| lib.commonjs/abi/typed.js | 16578 | `8bb3c0686c5ef2eec79cc452ea6a7df674ab536bbc82116f6c9cadde1595669c` | 0 |
| lib.commonjs/address/address.d.ts | 2129 | `53cfce94cd12e7e0bd9a5d635dd4929f5883c18135e86290775dea5b920545f8` | 0 |
| lib.commonjs/address/address.js | 6132 | `6b3aa63e2c8b2367ba06e4428827a87341c1db657b3b5cfa852e8616189becc9` | 0 |
| lib.commonjs/address/checks.d.ts | 2538 | `9df9be9776aae375c562e7115e32fd0f2c2a0598b26ab23c3b0f1408751efecb` | 0 |
| lib.commonjs/address/checks.js | 4019 | `bfae8d9fdcc50248e5c2795dfe690ab08d4502e379922a270ac02ee4b52e1a87` | 0 |
| lib.commonjs/address/contract-address.d.ts | 1624 | `2d868771bfc205cf27c0b36626e2c3925a55a4fcdb6e4f30f563b0ba98e583c4` | 0 |
| lib.commonjs/address/contract-address.js | 2992 | `9fa1e108e397adb593ab5aa1e86dc22b3ec89cda72194b44030755d625143199` | 0 |
| lib.commonjs/address/index.d.ts | 1720 | `3ebf9d4673a4a8bf80186f47be2697c48fd85b2dbbbfb3718744b9a94ae9bec7` | 0 |
| lib.commonjs/address/index.js | 1903 | `af61e8c4aaaf6568209b95c3d7a70bdf645c8c6ca381631d8d6dcde7c7ee3aa1` | 0 |
| lib.commonjs/constants/addresses.d.ts | 193 | `42a070375b9fa9e09573b391dc15e9751113151288937f6d622373d8705e478a` | 0 |
| lib.commonjs/constants/addresses.js | 324 | `5d3ad42a13ab2351bac8ab8547ff427b71ae38d55f4b9da94080c877e627031c` | 0 |
| lib.commonjs/constants/hashes.d.ts | 208 | `77c1edc2eb2c2ef64cc6d45f846dac52c1a1cf0357c28d72a903da58b9fbf56f` | 0 |
| lib.commonjs/constants/hashes.js | 360 | `0019dc68da49851784f99e57f4592fe0477c24f8b5991f781931926e2982968f` | 0 |
| lib.commonjs/constants/index.d.ts | 378 | `8bc016c287b028ceb9ca0438967afc8bd3ec4b0db901f5cc058ebfbe7abd7aab` | 0 |
| lib.commonjs/constants/index.js | 1680 | `bd8a606ece8f8fa3ec7df4d7c918f855d5d6ec102872470ad94bc3d2a2bb6999` | 0 |
| lib.commonjs/constants/numbers.d.ts | 954 | `f3ccf447160ee55c440b3cdc68bbafd8393c658fb257d557745b861781ecf1d4` | 0 |
| lib.commonjs/constants/numbers.js | 1388 | `4dd785d7cc711f099a548e7a8629f3ab1638a0195fc790fdaf10aa2af22d17fb` | 0 |
| lib.commonjs/constants/strings.d.ts | 354 | `34ac47d3fc6b5707ceaf7f0b580ee1805fa393ea045142f659b679e0332c6240` | 0 |
| lib.commonjs/constants/strings.js | 553 | `c6a9fb3a300667ade30855c300af5824f09eb07b30bbfb0ce02f1b4d479095dd` | 0 |
| lib.commonjs/contract/contract.d.ts | 6791 | `8418c6ff163da8295c03be007fba44281ce6c56af61c197defd0f8a11d512fed` | 0 |
| lib.commonjs/contract/contract.js | 36247 | `d2c308a2336f0b89f9e8e91bb72aec79c914c9a9a84bd45c7bcb225945cfa96e` | 0 |
| lib.commonjs/contract/factory.d.ts | 2606 | `7334b41305fbb99b9efe411cddcae9ef17fa6d89ab081d26435f0f9a72f065bf` | 0 |
| lib.commonjs/contract/factory.js | 4459 | `78fd09abe501222a9a84553d8013da0893a5afc026e87f4f1e81c42327674b4c` | 0 |
| lib.commonjs/contract/index.d.ts | 974 | `352d3bb36b12c1799dc302e90f3a9b47385a249fb5df3ce0e4df3cfd726bd746` | 0 |
| lib.commonjs/contract/index.js | 2124 | `5362ede26f9c65db10c64e06e42814c9a6307e846f3ee9315d256f21ac2e7d9a` | 0 |
| lib.commonjs/contract/types.d.ts | 6857 | `d0ed250ca7915611e8b150505c4b524a4ecfb1d121ef046b369976bd314698b8` | 0 |
| lib.commonjs/contract/types.js | 116 | `4a93e6ea16f28c11c6c7ce5341818af506d05fb9afd9128270535e80ea5fbec3` | 0 |
| lib.commonjs/contract/wrappers.d.ts | 4313 | `14a09b10bcd25f3178c39d53b4160977293bc6bf045e52ee3c08896fdf8f3274` | 0 |
| lib.commonjs/contract/wrappers.js | 5644 | `0c640d904fad10cbd8496687df519ff6d7e072567e7f6b5160e1725264400866` | 0 |
| lib.commonjs/crypto/crypto-browser.d.ts | 609 | `64e38476609a864082366bfc84e50718a596e191505fbd1b68c52d0afe741608` | 0 |
| lib.commonjs/crypto/crypto-browser.js | 2267 | `8a51ccffb74b25948386aa04e8bd2dd2e3f7a0ad0ee947cc4a7c07302f2f7865` | 0 |
| lib.commonjs/crypto/crypto.d.ts | 110 | `0cd11cb899a92aa3f998b339a31e7111bfa01ff00e5470ba2c450b99b67c4e9f` | 0 |
| lib.commonjs/crypto/crypto.js | 712 | `0291e2a48dcfbfa996ac688f366daf129541e4d376057983df9bc0d1ef86e39d` | 0 |
| lib.commonjs/crypto/hmac.d.ts | 907 | `afd9ebfe2b8ced603e34db1c54c7764c7db7bb9d67c69dd90beaeb4d99e11603` | 0 |
| lib.commonjs/crypto/hmac.js | 1562 | `2e941a9caffed641f0ebdcac89eff405784638e82a45168483c82ecac42d2374` | 0 |
| lib.commonjs/crypto/index.d.ts | 997 | `02d0e3d40ac1e761e16a96c882ae1b75a327d0f20731bbc690c15eba0f6c15bd` | 0 |
| lib.commonjs/crypto/index.js | 2794 | `ee1887611b9b2266751699f3a11ce0405541443ba1ad3f4ed29f1fde71574e4f` | 0 |
| lib.commonjs/crypto/keccak.d.ts | 995 | `c2189948d258e7bffb176ec0f982ff136c15f7cb43711a6457ae93d6d1a44575` | 0 |
| lib.commonjs/crypto/keccak.js | 1451 | `ca68418d92aca22a795dec5856f0823040b077f05eb9c077baf9449c7159475a` | 0 |
| lib.commonjs/crypto/pbkdf2.d.ts | 1485 | `7d0b3df72dc921d9f438c43ba6cb82683fa79a2ae1566946075ebbd08d830840` | 0 |
| lib.commonjs/crypto/pbkdf2.js | 1862 | `23408cee7967d0b3ccdc3649e5df04ab376b0a4e8990ab93dc023390276f19a5` | 0 |
| lib.commonjs/crypto/random.d.ts | 409 | `0e2eeffb8a065abf94202469089ca0def7db7d071fffb85c2d20b2a4611a8619` | 0 |
| lib.commonjs/crypto/random.js | 1158 | `b671b6118c253366f295ccbeeab5cbe14c2f9838808e307b1b9e34183dfecda5` | 0 |
| lib.commonjs/crypto/ripemd160.d.ts | 639 | `a6fe037550736f4a33d23650cb86ae83e981e3547e143073fd9e6294f5eabb81` | 0 |
| lib.commonjs/crypto/ripemd160.js | 1109 | `272dccf92bbec09798c68864b4b8758d83940556e529958f927dc60ddcbae993` | 0 |
| lib.commonjs/crypto/scrypt.d.ts | 3748 | `edf4bbbd2c49e1a3ca16db235375e35fdc78c01336526b4ded61b83a1a27be5e` | 0 |
| lib.commonjs/crypto/scrypt.js | 4131 | `c46dd7a68f2905a7a9d23aaf55f28acbda8753642e637e83d827fc457a7f8713` | 0 |
| lib.commonjs/crypto/sha2.d.ts | 1145 | `a91270b389959d4c658eb232bc98ac0d6625a2f5d815922f04184c067cf45ab9` | 0 |
| lib.commonjs/crypto/sha2.js | 1919 | `173177e9a1e68da13a347cfdb3e27df1f24305da4a95a1b0f15bc4d865f2325a` | 0 |
| lib.commonjs/crypto/signature.d.ts | 5058 | `13c4194f23f76b20ef3bd4dd15f6da80806c08eaaff8d8b655a74ee67af2e41b` | 0 |
| lib.commonjs/crypto/signature.js | 11911 | `1b35127577b43c8ee084e2407ec536a0f07059c7f4b904d85f0775156b786734` | 0 |
| lib.commonjs/crypto/signing-key.d.ts | 4140 | `52683c193bf516deb3897278f759d14325baca083deefd36e693e5c09ba436b4` | 0 |
| lib.commonjs/crypto/signing-key.js | 6769 | `4447821501cfe073247cfd730ad745bd19be3736c73cc770f982aa461d1a8b75` | 0 |
| lib.commonjs/ethers.d.ts | 5965 | `190bfb8a3040387428311c6da0dfb6250ca70fd45fe19b066e3d20fe042b4be3` | 0 |
| lib.commonjs/ethers.js | 29692 | `47f99d7956adc92545bc9475cd1962b9bde40b403c63a4870341d8868f98182a` | 0 |
| lib.commonjs/hash/authorization.d.ts | 721 | `891790a0c6238d37c521c6e37e733a7b9f3e2bcbca4b040e98dcb4fc5f31297a` | 0 |
| lib.commonjs/hash/authorization.js | 1317 | `d700cb76449297102c89e8af56013a84d7d8b7d19241e9c01816ec8cc542a28d` | 0 |
| lib.commonjs/hash/id.d.ts | 344 | `3266a03c5946baa44bb5413f01560c1d70b41cc975cccba45d6d257e8ad6e9b6` | 0 |
| lib.commonjs/hash/id.js | 602 | `ab4a5bbcc97e24fa10d2e44611a5790087b25d33853f183a81d08c0c46ec7d43` | 0 |
| lib.commonjs/hash/index.d.ts | 764 | `a061f40fd57f34ae7bf038f9ee41c2fa83145f054adbda9be5cbf8a93b607209` | 0 |
| lib.commonjs/hash/index.js | 2749 | `f24fce8369f3b66ae9854889062f658e6850d145fa68a5b1a480452627cbd1cd` | 0 |
| lib.commonjs/hash/message.d.ts | 1212 | `2b00099841c56a96fa1b9c0444e95503e4467528f331685665ef74397b95c656` | 0 |
| lib.commonjs/hash/message.js | 1879 | `06e6e0e3e5284eef5422ae5a5f495b580f3ebf88ee3f5ac0a6a3f1d512657dca` | 0 |
| lib.commonjs/hash/namehash.d.ts | 611 | `5ba98fa53903226fa84855af5757147f3926e84cdceb8c9653c217aef3d54362` | 0 |
| lib.commonjs/hash/namehash.js | 3247 | `5a4cbcb7aee982353229c705d620a6c46f2d88181d77a37f6b5d44239eb8d4c1` | 0 |
| lib.commonjs/hash/solidity.d.ts | 1216 | `8ac191cee94b0b802d9295377456de2ded468f8212c7c147eed21f69d78b1c2e` | 0 |
| lib.commonjs/hash/solidity.js | 4518 | `a36b79a99cb7894af4b5fc73b7cb88e231027c8d1534944c044f2c8976626102` | 0 |
| lib.commonjs/hash/typed-data.d.ts | 5377 | `057980116843d7c307b7b9df0df6272fbb12b48e3a4b386fa4960cb39f40c085` | 0 |
| lib.commonjs/hash/typed-data.js | 20748 | `e7e176b766d887594510706e45c0d1aa7312bd55d8f017d382fd6df3305b7a39` | 0 |
| lib.commonjs/index.d.ts | 352 | `e981c8c1e332df4f83dd27eeb3b0557a8afd36ffc5110b09e60d0a1a5b8c682a` | 0 |
| lib.commonjs/index.js | 540 | `17771082edebd848a7e261149bbbbe3221e58825517dc79255a4b9376f21ad82` | 0 |
| lib.commonjs/package.json | 440 | `9177de1f0725735d11b559b89a246932e5640531f046d63feaff45de1bf2fe08` | 0 |
| lib.commonjs/providers/abstract-provider.d.ts | 16097 | `e8b5ea1f3bc2c2397a8a793970a1c3b4b7664254104d55bd3520958f840d3b9e` | 0 |
| lib.commonjs/providers/abstract-provider.js | 53285 | `35d3c2a1811529cdaabb5f8f907b75691e5879cbdf0d124b3cfb15a54d2a3beb` | 0 |
| lib.commonjs/providers/abstract-signer.d.ts | 3145 | `afee3d5f2fd0092e4e9e2a03bde1729b599e0521e763dd145a7489a8ba97e63b` | 0 |
| lib.commonjs/providers/abstract-signer.js | 10420 | `5e89ed4eb0004e387d981f8ef8c30e05b18289903b665115f5c315d6885dae42` | 0 |
| lib.commonjs/providers/community.d.ts | 974 | `82af483335b93a35000fca8ed01c5f8c7aa23bee91896d6daafac88e4bf263bf` | 0 |
| lib.commonjs/providers/community.js | 1704 | `4916ae23218cfa2c53c425ecec53217ad41301562612c927d91079e553b29851` | 0 |
| lib.commonjs/providers/contracts.d.ts | 1252 | `dc0f45854448366e46ed513f5d198379da258376d466f11e6d651dfbb968a3d5` | 0 |
| lib.commonjs/providers/contracts.js | 114 | `f14a59805eb63819f5ec8cb76d6b0887426c550f981ff517e74790eb3f1d8746` | 0 |
| lib.commonjs/providers/default-provider.d.ts | 1893 | `209a4f359634064b7e07b300eb87f46909411586015a75d771337301285baf6e` | 0 |
| lib.commonjs/providers/default-provider.js | 7788 | `df8ee8bdcbe06877db953f72ba556ca833323516378beabf0b01e86ffcf8ed51` | 0 |
| lib.commonjs/providers/ens-resolver.d.ts | 5310 | `c845638f8e301087c49190b9f7c259aa90a79755e23625585e276fe84b3991c3` | 0 |
| lib.commonjs/providers/ens-resolver.js | 25292 | `3facaf7187a4f91b0578421df86eb38d5bee96f746eb69fb83e27401c680b1c9` | 0 |
| lib.commonjs/providers/format.d.ts | 1087 | `b31b025f01a686d46771b54ae03b966af7fd9fd0a5480003ab7e390c43752e2e` | 0 |
| lib.commonjs/providers/format.js | 10977 | `9a394f4ea8df2d0c8b00925794b789f33c8e5d228bc74e2224ecb961e3ba1d58` | 0 |
| lib.commonjs/providers/formatting.d.ts | 8681 | `05c620cb5382f37a46eef76e57b2769109eff2190c439893d7c40fdd04eb5148` | 0 |
| lib.commonjs/providers/formatting.js | 235 | `ecd2615e6c5599e952a6d64bb317625b7f6c4e2eb062205f82994d41dbede262` | 0 |
| lib.commonjs/providers/index.d.ts | 3552 | `90e04e44bf25f8b6071d3695296abdcba54bc1803064e48b2e739d273f9eace7` | 0 |
| lib.commonjs/providers/index.js | 9476 | `fcffabbf768b7a6ad96c429eb3051d212cfedb8251f50ff7c0c7caa6c31c196d` | 0 |
| lib.commonjs/providers/network.d.ts | 3376 | `87180277f45dbc2a384fa331b8db3174ae42f5445955469d1554840b245a76d5` | 0 |
| lib.commonjs/providers/network.js | 13922 | `9992ca65052c69f63beb661400eb77ff227aedbf0479e8f2ef9d42ec69ee02db` | 0 |
| lib.commonjs/providers/pagination.d.ts | 192 | `b000559850c7766aeb0a13a56f5451e6402feacf34018971e68919362884be0c` | 0 |
| lib.commonjs/providers/pagination.js | 115 | `8e97dc66b25390bdad98b2a6a5bf6f69079fb93aea9b26bb7def4217f7bbfab7` | 0 |
| lib.commonjs/providers/plugin-fallback.d.ts | 695 | `435fb4fb1fd9f596628a47bf8f0b38575d6b3863ce57a3fd85ad0fe0d6294573` | 0 |
| lib.commonjs/providers/plugin-fallback.js | 1201 | `49996bb25ced6ea34446649093563c61062fdde73a86e4d89285d1894ad85216` | 0 |
| lib.commonjs/providers/plugins-network.d.ts | 5569 | `f52c9a59a36b2b80e82108132883624e1ca5889b8161c96685d5b7abf1221d3b` | 0 |
| lib.commonjs/providers/plugins-network.js | 7970 | `6b973a3935160c7c799d7ebd3a2b6b5df272491dd0d67a157ac520a7d88d4af5` | 0 |
| lib.commonjs/providers/provider-alchemy.d.ts | 2001 | `7d03d9adda53f51aba7375d78b50c82a478afa5d601ccadd5c8ef2721c19390d` | 0 |
| lib.commonjs/providers/provider-alchemy.js | 5635 | `64e3508787dc9f936922d6465f154dfc64e2d4b4814c3c7a796ee7d4c3ba44db` | 1 |
| lib.commonjs/providers/provider-ankr.d.ts | 2311 | `9459ddcf024cf57584f329bac738c8a26a8a76bb85b6f97ebaf755d270f1eb45` | 0 |
| lib.commonjs/providers/provider-ankr.js | 4968 | `7f8215a09a3dc3fb9e3b9c1404ef8131263c02c7dadf9cec37f095f9ba6f2515` | 1 |
| lib.commonjs/providers/provider-blockscout.d.ts | 2149 | `098d93d036a4f80dbd002010a940753570dfa293af4ed6e2180e2dec8aa893b5` | 0 |
| lib.commonjs/providers/provider-blockscout.js | 5512 | `85165db11123edb71375bb4e5fcf10221577e7ef828d57e3334539277e5d91ac` | 1 |
| lib.commonjs/providers/provider-browser.d.ts | 3643 | `314359daf8d71a2883cbc054dbf16c4161f1b66c1bc01e0e737262cc0dfaf2ec` | 0 |
| lib.commonjs/providers/provider-browser.js | 8110 | `e4addd3e3b9e2607a6c9a7581bc71570e7b1b95a6ca84b194761567ecad1471b` | 0 |
| lib.commonjs/providers/provider-chainstack.d.ts | 1686 | `3890ab6996506722cd1fecd0b5b838a5af654836abe484c99696f82dc4147f32` | 0 |
| lib.commonjs/providers/provider-chainstack.js | 3616 | `da4e9b617572950cb3c1a2904d436f9a879a94747ede35c2579eadcdd90d683a` | 0 |
| lib.commonjs/providers/provider-cloudflare.d.ts | 404 | `825b9b3691d29482cc2034a8e6292d4800222601c2a883ad3e777182bad6fa04` | 0 |
| lib.commonjs/providers/provider-cloudflare.js | 953 | `4585d9b4e02ef8c9ce88ff94a2157596c0035a82e6de110fa9ac319e96134e40` | 0 |
| lib.commonjs/providers/provider-etherscan.d.ts | 4985 | `ce51923912e666f0440bf60da367fa5bb59a33816f093de780d5e350cb02c220` | 0 |
| lib.commonjs/providers/provider-etherscan.js | 24945 | `3dbf08bcf32656baa8c1e0e7cdc1f60891f5b4f68608bfff81446bad851be9e3` | 0 |
| lib.commonjs/providers/provider-fallback.d.ts | 3501 | `167488303ef27a82d6bf439a7e09901c88ce520b2ca70398698713cf29f7599d` | 0 |
| lib.commonjs/providers/provider-fallback.js | 23731 | `ca932f54eb323d810f736d94b59e208c829d177374744a92b748d907579d5c07` | 0 |
| lib.commonjs/providers/provider-infura.d.ts | 3755 | `3e6548ae5c61384f7faf2f75793628fe5ef06c56060bffe86bda3cbcc7d94524` | 0 |
| lib.commonjs/providers/provider-infura.js | 7420 | `b4598207d96155eec218d5f97438410b50edab3211514fab22daac1b876722eb` | 0 |
| lib.commonjs/providers/provider-ipcsocket-browser.d.ts | 130 | `94daf1df14a61f222bcf90b95f9b4eade5cdf1143bf139769a37ff5671f16eb0` | 0 |
| lib.commonjs/providers/provider-ipcsocket-browser.js | 251 | `d28b9df37ed976b7b02c5ac26d670a71304d4ef277082234e0b0f108eeaf3d6e` | 0 |
| lib.commonjs/providers/provider-ipcsocket.d.ts | 783 | `2a444ea55b9bc6f78215d2462dfdd008a9d2d5f2119ac541ae57b83847e9786a` | 0 |
| lib.commonjs/providers/provider-ipcsocket.js | 2319 | `dc4745b6762a43a7130bbb7fe43bf889170a6d774354a12eb618f67305832851` | 0 |
| lib.commonjs/providers/provider-jsonrpc.d.ts | 12449 | `25fca633b8863ffd82f264d27c3f3bc70535bf66d484191bf3920bfd8cf7d764` | 0 |
| lib.commonjs/providers/provider-jsonrpc.js | 40445 | `56841720d3618689c4de8adbf845e672d59941f8ef8e92b0de6d2e7ebcb95ec2` | 0 |
| lib.commonjs/providers/provider-pocket.d.ts | 1979 | `2b4630bc489a8585742ced3952f491fe741d8f38bdd6d205d1a938baccddbda3` | 0 |
| lib.commonjs/providers/provider-pocket.js | 3838 | `551433b630953806e1c7eba81c010a1734d7e6ad3ea3cc51cecd3b563421e53f` | 0 |
| lib.commonjs/providers/provider-quicknode.d.ts | 2178 | `3bba9d77cfa07f2c6d174f804317e14d2573ed8234ec14152e51b207c90d1c47` | 0 |
| lib.commonjs/providers/provider-quicknode.js | 5852 | `e59396733a902dd0184de8e9cf4a6cc09665d037086a208b8f083b9e548c66ea` | 1 |
| lib.commonjs/providers/provider-socket.d.ts | 3802 | `55e749e97482f1e8867594715bf2e12cd38a9ff3d5dd4775f8a038b66573608e` | 0 |
| lib.commonjs/providers/provider-socket.js | 10770 | `0bf0aba5de79c5f8fcf6238c62ca9b74bfcb72b9e87ee5a583753b91548ba058` | 0 |
| lib.commonjs/providers/provider-websocket.d.ts | 1464 | `c33f0b0ce44cc14942c7fdb26da13b6a2b2f048c9b344f015a3789a7a12604ba` | 0 |
| lib.commonjs/providers/provider-websocket.js | 2801 | `6c48ce3329492f46269763c86c5f7376f2f4321b200fe3e1a6af0af2cb213db4` | 0 |
| lib.commonjs/providers/provider.d.ts | 41089 | `b199e3fe2e42e49f54a6679ea0194bc72236c0d12058f588a0fe379eb1e5a52a` | 0 |
| lib.commonjs/providers/provider.js | 44364 | `fc0a34ad2916446126b62fcd6f1b5e0cec509ec01fe329a7626e0b7317c77dac` | 0 |
| lib.commonjs/providers/signer-noncemanager.d.ts | 1532 | `97a67bba2c8123cd1fc6412042fb38ceee1477e6d844b5ec2dafea21f7f3e6f7` | 0 |
| lib.commonjs/providers/signer-noncemanager.js | 2471 | `9ecf421c9498333c40487976be42a6a3ea7ffcef5b4a27ccd681cd0af14e299e` | 0 |
| lib.commonjs/providers/signer.d.ts | 6220 | `fedb24ddffb67350cee62144c15d470251a1d0637b5ba37da4c836083165ce47` | 0 |
| lib.commonjs/providers/signer.js | 111 | `a4d069dcb02131b9ae46ddaf381594e7b58ed61d693fc9e6702e1c4d7e14ae65` | 0 |
| lib.commonjs/providers/subscriber-connection.d.ts | 709 | `6636880b988746258ec8f03fba033683a5c1b8e2cb28eb3a5984db35b221f456` | 0 |
| lib.commonjs/providers/subscriber-connection.js | 1573 | `b2d0b3af6b91244cf79c8993ab46517ebf4eac13f17cf37cba0d25c8844ea49c` | 0 |
| lib.commonjs/providers/subscriber-filterid.d.ts | 2450 | `a72c8a6b4ea88c20c4b0e0aab6fd8b352ee36d870c4806a91526c8bc764b1b20` | 0 |
| lib.commonjs/providers/subscriber-filterid.js | 5830 | `3fb5855164cb42a85639d4c32263eaf32d80e4561e8b2eadcdf67106d0ab675e` | 0 |
| lib.commonjs/providers/subscriber-polling.d.ts | 3232 | `8192008e5b481302fa03ad48b4a6b0c266ef6b53cbb9a9589c3feb94a3515b5d` | 0 |
| lib.commonjs/providers/subscriber-polling.js | 9251 | `37251d6d6fe068a6f24a83a01fc72ea47a22c86b5129708e8c3e36cf1faaea58` | 0 |
| lib.commonjs/providers/ws-browser.d.ts | 107 | `529d9b7f4bae95357c2a078c62ea0de073a42a2a2178481fa3c3cf7b523375b7` | 0 |
| lib.commonjs/providers/ws-browser.js | 505 | `6041d6d1ebc8faed70a5f3edd46a097f3fb14373d815fdebcd80c13c80805a8a` | 0 |
| lib.commonjs/providers/ws.d.ts | 64 | `2b550ff58b50e3d9715b4790748c82ebbbf74f4c41824600aa3416b690d54dda` | 0 |
| lib.commonjs/providers/ws.js | 273 | `9e06431925686f3be1ba93a5d6ee96c9628c42081b4471e1f63010b455b616b1` | 0 |
| lib.commonjs/transaction/accesslist.d.ts | 260 | `0df6ff347a9d41713af680b29476a430d0f0eaa30465efe3ef149cfbc7b63a3b` | 0 |
| lib.commonjs/transaction/accesslist.js | 1770 | `d182799dda06e5af478dd0fc83be279debb7c19e33b84c28bf1ac61031ba12ff` | 0 |
| lib.commonjs/transaction/address.d.ts | 614 | `d95862256da7116eae8b69d1fef8b1ffe47e221787fb7541b90295336731274c` | 0 |
| lib.commonjs/transaction/address.js | 1056 | `f22ac0ac700ef45e33d0e16b551608ee67c0bc10003a7c195eb0b1eaa2ae340d` | 0 |
| lib.commonjs/transaction/authorization.d.ts | 193 | `12a68e03b6c646f7eff6dee0bfad0669aa3f0bf84a62c0fe69c637fd2a4cfb46` | 0 |
| lib.commonjs/transaction/authorization.js | 692 | `31a9a5bc6cfc9a7d662d25afa016fbe1cacfe98a1fb5d43ea44f676e492e6257` | 0 |
| lib.commonjs/transaction/index.d.ts | 1323 | `32d70e138cd4199ae0516401cbade1343c27baa0b8d451da6d8cf753d5546668` | 0 |
| lib.commonjs/transaction/index.js | 1254 | `13c635ec15486b4f247c7229a13f1d2fcdbb99a9d00715598d9356d980595efd` | 0 |
| lib.commonjs/transaction/transaction.d.ts | 13059 | `039cee8feda0a8da4d6a873792b5f935a7eb5ef276bef33f3918b10e96292fd8` | 0 |
| lib.commonjs/transaction/transaction.js | 48444 | `5d1ab70f968b852ae4aa168fea8413d694c22723b2182880358fe98f9fefad8f` | 0 |
| lib.commonjs/utils/base58.d.ts | 873 | `c1d45ad150211313b9f4965a7f984993dc07313a8e81255f3d6d1c2d2b7a8fd9` | 0 |
| lib.commonjs/utils/base58.js | 2174 | `bc6901a54f4a72187783c5594fc4c6e21a2f27f94c43c200b107092b09db4566` | 0 |
| lib.commonjs/utils/base64-browser.d.ts | 220 | `143c50cf9d69e670767b881cc31f710ca3f96491dd4de645105c706a1606bf51` | 0 |
| lib.commonjs/utils/base64-browser.js | 798 | `e40e46136b268a513a38d1faa05f7f27c11141719ce8845f46ff4eb64140d586` | 0 |
| lib.commonjs/utils/base64.d.ts | 1057 | `3099c6d6ca03d5f2098837cac45e7793786c54e06dfa882ff4a854bddeb3f97b` | 0 |
| lib.commonjs/utils/base64.js | 1675 | `1159bf9ded677750169ff7d5b3390742413d2e5c4b24247d1420d8730c2fe973` | 0 |
| lib.commonjs/utils/data.d.ts | 3180 | `f0b25ecfcc4cad84f95951dbdc13686433c5a7c54deebe9a43b1b4ddee1bb5be` | 0 |
| lib.commonjs/utils/data.js | 5701 | `94218fa9bce8cc557e54dea061144fc60b1448439ca3f15a069cddeaf3adf2e8` | 0 |
| lib.commonjs/utils/errors.d.ts | 16678 | `fe0c1e2efe12fcc7e0409e799a31b02e3aa3007e516af720106da72e8c22157a` | 0 |
| lib.commonjs/utils/errors.js | 8173 | `96e0d6db74d5d8e42c5b3c3b158a28bb36538a3f1dd3b091ca1eb4983b7c6557` | 0 |
| lib.commonjs/utils/events.d.ts | 2302 | `7a8ead38ea10e5187f72c8ff01938f91ee8341bfdf33c467b26d049cf2719530` | 0 |
| lib.commonjs/utils/events.js | 1288 | `f9c1b9366193e67e2333679b20a11c53af79a3165501ef9c30cf5dba8ad1eb46` | 0 |
| lib.commonjs/utils/fetch.d.ts | 12331 | `c8a94ee463980a023d5b0591edbd32c6c729cb217aa3901b23473295030f4354` | 0 |
| lib.commonjs/utils/fetch.js | 29315 | `b4c1b3a53270b05ed298f28f9a020f9a280ea9d221ea14b5ded28131254d8543` | 0 |
| lib.commonjs/utils/fixednumber.d.ts | 9160 | `9a721310a62782bf36638b10fb31aebb3ff34e2857a3fa25f0c243a67b39bff2` | 0 |
| lib.commonjs/utils/fixednumber.js | 19962 | `0f7684f9e65d66346b41d75f1cc2f0772a1f1ec4b4954c485f8c6c1be8dd0975` | 0 |
| lib.commonjs/utils/geturl-browser.d.ts | 335 | `b3ea4f3cb1a74cc33b05a53306ead10e86ecba946597d395f3bb89be319938e7` | 0 |
| lib.commonjs/utils/geturl-browser.js | 2540 | `b8bbdb16813c67bbdb393209bc1f114b998de19dc09a88540e62fbc83e768875` | 0 |
| lib.commonjs/utils/geturl.d.ts | 370 | `32853e5f765babab7f3de559d9ecbe68049dd064e231c2da7e31ec32e0caf28d` | 0 |
| lib.commonjs/utils/geturl.js | 5114 | `bec24b7f9c274a4d456244475b12928dd2cca07e723604d1e3b8ec86300d3730` | 0 |
| lib.commonjs/utils/index.d.ts | 2430 | `aa546b567b477fcd690218295cbd9eb877d3e25bdfc049b40973702712d00788` | 0 |
| lib.commonjs/utils/index.js | 8439 | `9f2ac07d9b9dd29e51e5ac81a18a72da78e739d831ab948bc66bfba20eae69bb` | 0 |
| lib.commonjs/utils/maths.d.ts | 2478 | `ca1b7949fa09108f8890ddefa6ed3d2c3461bb283cd8a09c0d5037ebf032ec71` | 0 |
| lib.commonjs/utils/maths.js | 8480 | `103a48c11e5305a5f7ff76d7d9cae08b24d82281e46e4bc1466e0b191e66888c` | 0 |
| lib.commonjs/utils/properties.d.ts | 624 | `1cdd7ea3d40571e6ed8cd91a1ef9f390c6d845d7adbdde29a61ca1af4036e7c8` | 0 |
| lib.commonjs/utils/properties.js | 1821 | `8a4fd276aaca99e42e848b608d6dfd38dea93f96a026f32999f1986c18ac6413` | 0 |
| lib.commonjs/utils/rlp-decode.d.ts | 245 | `8b49bd9c17fce53462e3c2094d961cb5bca26b3166cdc3e8c6952c00963b6a59` | 0 |
| lib.commonjs/utils/rlp-decode.js | 3379 | `58b756eaf8c85e6169cdb52153090880c33e23f40f76f437ea6601da42e50766` | 0 |
| lib.commonjs/utils/rlp-encode.d.ts | 235 | `d07f8e8c858239ee0fa66e25cc9e7034d8fe7b0876be61d3d2d22c06fdc6944d` | 0 |
| lib.commonjs/utils/rlp-encode.js | 1577 | `ac3bd1e71e0cc0151ebce3f571164c6b82f53aaa37e092328d08a2a195310ea6` | 0 |
| lib.commonjs/utils/rlp.d.ts | 571 | `e29069b75d8b588f0cd62242dc120178d0518aeddf9757a440cd35c2606de2d6` | 0 |
| lib.commonjs/utils/rlp.js | 696 | `67256006fb73548108eabbc5868956f52caebad88daa8bba59226f13d5f4135c` | 0 |
| lib.commonjs/utils/units.d.ts | 1006 | `fa2f8c5eedd3ed40be37deb32999191e1334f03fd402bad36c4b5a6da92470a6` | 0 |
| lib.commonjs/utils/units.js | 3260 | `b4dab8b090da1b16fa86cc4dcae7ad83d692b218cbbb4631271df297b6174a3a` | 0 |
| lib.commonjs/utils/utf8.d.ts | 3945 | `2d28f80386b506e00285b9cbd0dc1a695c810cb3bc61e0b2b081aac304ee3bc4` | 0 |
| lib.commonjs/utils/utf8.js | 8129 | `f665552162a67b547b1be04b2d1c559349eb0f489f31edb845a2171e192710f8` | 0 |
| lib.commonjs/utils/uuid.d.ts | 280 | `00f74835b3aaf3690d7480f1ad08fe02593113e38e7a26d7ad27d327f5b9af8f` | 0 |
| lib.commonjs/utils/uuid.js | 1037 | `442a0e3f717a51c58b1dd5b01ae31ebdb5d4d87e95d3cd3a93d5aa5703703370` | 0 |
| lib.commonjs/wallet/base-wallet.d.ts | 2128 | `abef0d03eb94032878417c5594b32bb25a44c14002933fe5b188ce7eb72ee140` | 0 |
| lib.commonjs/wallet/base-wallet.js | 5126 | `fd16b9463eeb67d5e3e4f63de5bc84c33b6ac9f2d579c4ef3178cb83167d757f` | 0 |
| lib.commonjs/wallet/hdwallet.d.ts | 8335 | `7f1ddcce6f5aa325fbe874137ed533a4e23e557050dfb15747a9e19e2d6b463f` | 0 |
| lib.commonjs/wallet/hdwallet.js | 19978 | `4996fee2da550e04de5c6b1f331232eea3f53553d92fec636085071fc36d13d1` | 0 |
| lib.commonjs/wallet/index.d.ts | 1341 | `deef751ee7953fca04f567770514f93f9d2fa1254e5cdcb7da5229757c65ea39` | 0 |
| lib.commonjs/wallet/index.js | 3563 | `30737258f198ead78d9518cc7ce184db0b876cc6f92eb1007b84d197091b2905` | 0 |
| lib.commonjs/wallet/json-crowdsale.d.ts | 929 | `a10dc770ceb0a20ecde6e0cc37ed95d1c5390f34eb7d7930407fa700354db3b5` | 0 |
| lib.commonjs/wallet/json-crowdsale.js | 2487 | `758f02b090693b153bc8cad9f8ddb7f1176bbc78c9763bdcd493e53388899ec6` | 0 |
| lib.commonjs/wallet/json-keystore.d.ts | 3211 | `0e41bc8a6621ff6901a89fb0cca175731835723a4d9bd6ba3974cd0df809be89` | 0 |
| lib.commonjs/wallet/json-keystore.js | 14479 | `5cbfaedd50de30f945d520642523061ae9236234160bc9e6b76c4af5e51e3f03` | 0 |
| lib.commonjs/wallet/mnemonic.d.ts | 2319 | `4af291a429ee3d5516e506b507453e6fbc80fcea52bd62ce18190702acb5c807` | 0 |
| lib.commonjs/wallet/mnemonic.js | 6626 | `575e1e397944e8e77a165d58cfa6d4c5caff139d4a9b2eef34b7687cc3402b61` | 0 |
| lib.commonjs/wallet/utils.d.ts | 351 | `b424554c62c1b741ac0da65e79b5cddf8b1e228b30d1a73ba8aecedddb78ebde` | 0 |
| lib.commonjs/wallet/utils.js | 4441 | `2e64a4fc0f75f869f93e5a0b92e1d6ea9fc90d023b1f81e7f0ca06a2e8e970b6` | 0 |
| lib.commonjs/wallet/wallet.d.ts | 2940 | `aae5435e7c8b476b2b4fd960fb4ca413c9ed6dc8675d8db29a895ff7389e638f` | 0 |
| lib.commonjs/wallet/wallet.js | 5997 | `ea20742e0d885b84d7938b9f7ba12b31b1a0f5a8a8984cf525c8cb65a39a12a3` | 0 |
| lib.commonjs/wordlists/bit-reader.d.ts | 141 | `03487c22bbf8b0fa0ff0b7b865b5339b81a826a3233884102d4ccba8796ec29d` | 0 |
| lib.commonjs/wordlists/bit-reader.js | 1145 | `d67f2bceaa62f1cc4f710e8dde6f818810ec2f8c2b97f68c691dfe71f162249b` | 0 |
| lib.commonjs/wordlists/decode-owl.d.ts | 221 | `8c42c85090f1bcbd0523cee41536d0500100e73af5983fe6c7f6aa5bb9089c40` | 0 |
| lib.commonjs/wordlists/decode-owl.js | 1834 | `a867ed8baf11030b1e5fbe00fdd271edc4d5b95eeec707a2c3ebbe8faa51232f` | 0 |
| lib.commonjs/wordlists/decode-owla.d.ts | 144 | `5983ead9b6aad7a3512864366014f72032b6a423bd1d661bf814a2a2c83ce083` | 0 |
| lib.commonjs/wordlists/decode-owla.js | 1255 | `df490d6b582f6d2713e954661d4504aab0ac7b19d11e70e107a594d27119b59d` | 0 |
| lib.commonjs/wordlists/generation/encode-latin.d.ts | 644 | `9fd984d4e94660bda8d5ce949b32dcdd08220635a7db00bb022f2b41734e83bb` | 0 |
| lib.commonjs/wordlists/generation/encode-latin.js | 12230 | `4de40576fb51b1af27a30204bac26e4a55365ef5cc2b15670693c3406404e1ef` | 0 |
| lib.commonjs/wordlists/index.d.ts | 1043 | `43881022601c5fc87ff751cd869103981215489384643c71d5c8e58619f7bc96` | 0 |
| lib.commonjs/wordlists/index.js | 1866 | `85b04d9293fa2a6da31fb2a83b7dff469a28056d100531514d1ab5ffb4103c3a` | 0 |
| lib.commonjs/wordlists/lang-cz.d.ts | 639 | `0154e7bbdf0ddb952e11a7a5f7e43b1862d67a567985437fdddd681f4c9e4075` | 0 |
| lib.commonjs/wordlists/lang-cz.js | 8159 | `703b812d7fee2dcb9af26a0d1e2375975c439094154e6880a60f680ce9934fa9` | 0 |
| lib.commonjs/wordlists/lang-en.d.ts | 636 | `3fa498ce08b62f4148452e553d138429a5d928f8c39395683ef941856d9d8942` | 0 |
| lib.commonjs/wordlists/lang-en.js | 7038 | `0110f9f3a909a1d6c45d41bf838f1607e55b6dc8c705e4c0f42bd15c6a76fb87` | 0 |
| lib.commonjs/wordlists/lang-es.d.ts | 639 | `206c91c5c29bb0e66b1783262e5b6b0f1504ab033a81024977cc9a4484e36e8f` | 0 |
| lib.commonjs/wordlists/lang-es.js | 7303 | `b2828c28c66ca858b73bb9f4d25bcab33804ec09511b8b04ec54c2b9a9570835` | 0 |
| lib.commonjs/wordlists/lang-fr.d.ts | 638 | `b5e820752d23030fdab51a822e31662a46e09c188d301c31483965b30baeed94` | 0 |
| lib.commonjs/wordlists/lang-fr.js | 9054 | `a2bbf8a91e1a13a99126e8bffdddf443ab8eaf6436d0b8a1e77becb1a2d9aaad` | 0 |
| lib.commonjs/wordlists/lang-it.d.ts | 636 | `f909868bbe43d44156945d8c3d1f9f4489e6c7ae42141cfb57a8189428086b0c` | 0 |
| lib.commonjs/wordlists/lang-it.js | 8689 | `69ea10327285cdb9e454364724c87678f1f088026178c59f2f61618c96f70d87` | 0 |
| lib.commonjs/wordlists/lang-ja.d.ts | 785 | `fc8df545bc58bb69aa4b930f8f6e205e13cbefe6a1fa85b1217f4281f56c503b` | 0 |
| lib.commonjs/wordlists/lang-ja.js | 13007 | `3b72625736551b9226f515fefede8d1d9859dded84d9889fb7c4c3150320dd85` | 0 |
| lib.commonjs/wordlists/lang-ko.d.ts | 701 | `12336beed48c3f0ce3bac5b71841539f62ddd1b0288e108ca1ce7ce951cf6129` | 0 |
| lib.commonjs/wordlists/lang-ko.js | 14535 | `a2cdde69b4ea1ebef4576d46a6892fd00c5d23d50532113edfc5f300627749d0` | 0 |
| lib.commonjs/wordlists/lang-pt.d.ts | 639 | `1cecf5360f1fffa45f72c287f51be1ea3e12e7a92d5047750993f0b7101c7557` | 0 |
| lib.commonjs/wordlists/lang-pt.js | 8528 | `e4848e099e22480ce7a84374a4711b9faa747b2489203c7c7a5a860132c949ab` | 0 |
| lib.commonjs/wordlists/lang-zh.d.ts | 1059 | `997e3cd9dc0b53fc3270eb75935d99479ed3b2a087544a2499737689b11e2a1e` | 0 |
| lib.commonjs/wordlists/lang-zh.js | 11008 | `312781a7dc4224e764ec6bf62ef666cb39ee677ca77a9ae5bf9952e3dcbe1522` | 0 |
| lib.commonjs/wordlists/wordlist-owl.d.ts | 1044 | `b908d48bfaf9a491303e5970101a2b9895cc6f8f4c6abfabd6bb93ca425a22d0` | 0 |
| lib.commonjs/wordlists/wordlist-owl.js | 2371 | `112be914bd4791076e9282341e87531bcfe8568a0b14e5222204ce63e6e7f1b3` | 0 |
| lib.commonjs/wordlists/wordlist-owla.d.ts | 982 | `96d22cd33030a9b7bab47064406ef0fbf7502fd2b2779af845bb63c27e8ca92e` | 0 |
| lib.commonjs/wordlists/wordlist-owla.js | 1316 | `cfb3feba246d0279368c3141d4f035ce3420b033092167a1731a9efc8c19bc01` | 0 |
| lib.commonjs/wordlists/wordlist.d.ts | 1650 | `486a4acd1ddabb05055e75770bd51ffa166b1ac3940ec4019761f06c3c3b1d6c` | 0 |
| lib.commonjs/wordlists/wordlist.js | 1564 | `198d248815ef4c374ce92929886455e17a9627e39f72fd5827089efcdc58869a` | 0 |
| lib.commonjs/wordlists/wordlists-browser.d.ts | 152 | `821c80cd6b923d8e3f842d05bb92e69fea2989afa27db821720e68c2220cd38a` | 0 |
| lib.commonjs/wordlists/wordlists-browser.js | 261 | `db5d570168a00a649916f4b1828101ea31435b66891125a6d2db5f9fdc406186` | 0 |
| lib.commonjs/wordlists/wordlists-extra.d.ts | 357 | `0a9d1c6c00ab47eadbe8d21dc420603b1cc4d7f400663d0d9c10d2831e01e9d9` | 0 |
| lib.commonjs/wordlists/wordlists-extra.js | 1528 | `7bf9b7cdb87075f577cba7dc6aa94680f008eb70a0249691bc594dc89fb9d674` | 0 |
| lib.commonjs/wordlists/wordlists.d.ts | 658 | `cd564236c3689e0237b1b16c779deba4bf0905949b2cd1332b867a255a1fca61` | 0 |
| lib.commonjs/wordlists/wordlists.js | 1509 | `23a03f7f67ccf145d5df5152709dda4a813828d6cc6e34dc495a4a3fd2ae5241` | 0 |
| lib.esm/_admin/create-release.d.ts | 55 | `276a27d28bf39e01603e2f5651d1bc1a1b16a1300550b4da6dd55f1ab1067388` | 0 |
| lib.esm/_admin/create-release.js | 1454 | `16919a16ef4bbca26c74e223351c5dcf19accb3f1706b67fbd6f25c7cb2ce894` | 0 |
| lib.esm/_admin/generate-diffs.d.ts | 55 | `9c127b393111c62a7fb0705836c8b56ccb0cd79d9f355f24c0eea9aeaca4c086` | 0 |
| lib.esm/_admin/generate-diffs.js | 1160 | `96fb2797f3da78ae7486740e5dccc37ff56d9eafb0f36b0d4674725c695034ac` | 0 |
| lib.esm/_admin/test-browser.d.ts | 909 | `8ca4416c518448d8cd9ba5f8258cdb53c166c99445348469deff5791e2e626de` | 0 |
| lib.esm/_admin/test-browser.js | 14135 | `7a9df74a696e16f806af1f3e42df0d5dbc48a59a1d0fdc8d9ca111f14cfb023a` | 0 |
| lib.esm/_admin/update-changelog.d.ts | 57 | `710729651cb92b9bd86e2f6244ba00cd3297eeb7f38936dfc25a8ba7d8ddc5bb` | 0 |
| lib.esm/_admin/update-changelog.js | 5839 | `41dc35c833b3411240806da2eae843fad712fb25c2b8423534358b86aa01f75e` | 0 |
| lib.esm/_admin/update-version.d.ts | 55 | `631c4c6a9812a4064aece42ebb1663f18ad2adc044e417915032a2ea185202c1` | 0 |
| lib.esm/_admin/update-version.js | 3858 | `a2e276b4efad0d56c49e544656cbac28f1e8a6953fa61a908bc1c7d7c2856238` | 0 |
| lib.esm/_admin/utils/changelog.d.ts | 197 | `9fd6c1375a90699d84e1dcc7c320e77d4320003715ae9d0ecba60c325eb6fcc9` | 0 |
| lib.esm/_admin/utils/changelog.js | 708 | `fb3f96f340b74bf755ef6a95c61eb4d6c43f331148cf38698ca7a3879234133c` | 0 |
| lib.esm/_admin/utils/date.d.ts | 91 | `6f3d30887830b5c672adb7bb6fe1665d358247c18dc8cbd5f1537fa8295d7b78` | 0 |
| lib.esm/_admin/utils/date.js | 695 | `5552a80016a6b8e0977a21b7b578387afb64a5305f86d24eb1f95bb646481a60` | 0 |
| lib.esm/_admin/utils/fs.d.ts | 117 | `9809c47683cd91847bb7119669cab18d6f2f3a5e0c57b0ac599e08a8f700b025` | 0 |
| lib.esm/_admin/utils/fs.js | 237 | `66ea184f0f5e2f22c4098eac56e7455ff9394c3785adf7617a593a1e0bec8d2d` | 0 |
| lib.esm/_admin/utils/git.d.ts | 618 | `33f91288bb7250b1f3e0add878bc9a59f501eabae33dd72a0f25138a34530a86` | 0 |
| lib.esm/_admin/utils/git.js | 3022 | `0a6e370a27f5713de9ad3d21d41ba55d95fca3eff29bea484450e0deeab529fb` | 0 |
| lib.esm/_admin/utils/json.d.ts | 255 | `6d78e5cc92d50eebb8f39e21045ed48527a1f9a4460186a209fdeaebaeb8ebc4` | 0 |
| lib.esm/_admin/utils/json.js | 1045 | `84f46be0e70bcd6496f2d4c0daa527ed1d01c96b819452b7f0489ba058f50083` | 0 |
| lib.esm/_admin/utils/npm.d.ts | 264 | `1b3869727301ac957e5fc10c72c942bbdfab5187b66cf611991b7e0456f2ebaa` | 0 |
| lib.esm/_admin/utils/npm.js | 3049 | `0a10a49a6a797541bccb4da8b441660d5dd1d2f98dd17d99f7c6645850ba68fc` | 0 |
| lib.esm/_admin/utils/path.d.ts | 134 | `5d0e29eabfb9f599570a4c8778754aaf4304ae64ed84dcabbc5e5b118b4f624a` | 0 |
| lib.esm/_admin/utils/path.js | 391 | `f8edb700eef410e58de7afcd82fda0162c77555cdbe1f8649b3b64585b6caed1` | 0 |
| lib.esm/_admin/utils/run.d.ts | 635 | `e4a33c84af9555cf15a0e5ef6fb7cf1aec573b653d9c0ffae7fe07e2aaffa954` | 0 |
| lib.esm/_admin/utils/run.js | 1437 | `4286eb313daaf6cccd000f7092de1c91bc9ae5ff34f386f71afb7f6f11d98de2` | 0 |
| lib.esm/_version.d.ts | 119 | `31e313c0dba34e94e0135fe3b19bc3ee155a3958a96a6c60f9242612b6be23c6` | 0 |
| lib.esm/_version.js | 180 | `9f1010be12f1a336e30d98736d014bbc489ca99283ea35b6a53190f4b442e806` | 0 |
| lib.esm/abi/abi-coder.d.ts | 2377 | `3ab09cdc78b5e435e38c90d4d6845abaa6b60adb4c28d1df89b4e957d4107cc9` | 0 |
| lib.esm/abi/abi-coder.js | 8081 | `c9f607051d4d742691addac8aee1e847377d1e13650a904d55621fa4cbffe842` | 0 |
| lib.esm/abi/bytes32.d.ts | 423 | `033d848b02f3948d2fb4feb7fba98e9cc3cba797b417210f30454491b2d9170c` | 0 |
| lib.esm/abi/bytes32.js | 1195 | `b98ff37ea9e1ec7e6b574c9bb8e2803adac128a2ca1ca5a9c26fc57edb8be6cf` | 0 |
| lib.esm/abi/coders/abstract-coder.d.ts | 3881 | `67dbef5497f47d7f39dfd36d503a2fcd7235296f976ccd7be93bd2ec45945b3c` | 0 |
| lib.esm/abi/coders/abstract-coder.js | 16028 | `0942faf6b3b328ffe5ba427ec04a9382b0695aab0618ccf9ba2efacd307f4242` | 0 |
| lib.esm/abi/coders/address.d.ts | 408 | `d432f5b818c23b022f0be4ac1b93583aac03a5dbbc2f23d2cfdc6acbd8116703` | 0 |
| lib.esm/abi/coders/address.js | 838 | `2686db1e32d9e2fe65f2d65191d58cccdbe0d59b6f625be154cb44a50ca0600d` | 0 |
| lib.esm/abi/coders/anonymous.d.ts | 452 | `7cec3e1a96117900f40511797aed1d1e68c3d7bd35d6b2a467f837bbe493e8ad` | 0 |
| lib.esm/abi/coders/anonymous.js | 577 | `7e5d64424b8a3fe73252d94f8fa2430837ce634e80285e31db56f9ca795a5f84` | 0 |
| lib.esm/abi/coders/array.d.ts | 769 | `3124340589a03e45a24b79dd64cb60304a057bbec9776ea16f8d55f783a2b531` | 0 |
| lib.esm/abi/coders/array.js | 5949 | `6135fe17fe2d94bb1dbf4df0f4822bcc242945b71946685bef271ad21721b8b8` | 0 |
| lib.esm/abi/coders/boolean.d.ts | 410 | `7129a090917912a223915b29cb712d00163521c75981fa8092115f335dc61b9f` | 0 |
| lib.esm/abi/coders/boolean.js | 520 | `5cd44b4e193672d17dbb29d991f3a0383ac9a1543df72ae1b120c51923ae6046` | 0 |
| lib.esm/abi/coders/bytes.d.ts | 528 | `f85aa84e63c8d17429cd8161cca7125725a547e623623a6364d476587b89dcfe` | 0 |
| lib.esm/abi/coders/bytes.js | 839 | `e8d2ef8828e11c52fc79e6ccca2111220af60ae1ec58ee5a342cd62dd7259614` | 0 |
| lib.esm/abi/coders/fixed-bytes.d.ts | 514 | `02c8003a0835f0db719b1c7e8d85548dc9c67a495debf53f91d40504c748336d` | 0 |
| lib.esm/abi/coders/fixed-bytes.js | 956 | `79891f6d1167980eef43c5cecc4023a60b4d3b6be30bc88ece8dc06feb5f2855` | 0 |
| lib.esm/abi/coders/null.d.ts | 351 | `2cf283bda00af2894f54d7afceca9e1c856c9c78110140da6ae23213ecebbd61` | 0 |
| lib.esm/abi/coders/null.js | 541 | `c952925f628b8695f884fdc2404d2f066ffeb857b901843fb5aac2f14c3f3263` | 0 |
| lib.esm/abi/coders/number.d.ts | 558 | `7cfd40df82c249f56f5c37daeaf886941f11ab56595d657d7592d5de0fc17580` | 0 |
| lib.esm/abi/coders/number.js | 1639 | `e3dd3faeb0029d46f42ac084197c3a1fb3ea2e5ba487fd10714999d16a07c3dd` | 0 |
| lib.esm/abi/coders/string.d.ts | 421 | `cdd503d7c427abce5a90fef98ce394db81c0e24be8b01d049f7dc5077322ef1c` | 0 |
| lib.esm/abi/coders/string.js | 577 | `f4d3601ee44a7a9d66ea0d78124e35039c93bdbab4d455c329c4e5d0bdffd4bb` | 0 |
| lib.esm/abi/coders/tuple.d.ts | 509 | `f89c44293da3f402e380d1893792088285af9b1f6782f02adc0410b4de1f5860` | 0 |
| lib.esm/abi/coders/tuple.js | 1946 | `0642b1548d9a9a0635b23e5ab3e5cff59a28a493adba0f82fae811a506df8591` | 0 |
| lib.esm/abi/fragments.d.ts | 14007 | `09c6791e3421ad7b5feff77120adcb3aca2f45b0caa48fa0eb5bbde333075257` | 0 |
| lib.esm/abi/fragments.js | 46421 | `e6afebdc2fd739899dd27f2ba7ed0944bad72706893a29bc1cb9bb99147ac636` | 0 |
| lib.esm/abi/index.d.ts | 1023 | `f09ab98499647d29d8f3a5e0a5c1194b5d24fa9e1b2f94e195d1555ca8ba4098` | 0 |
| lib.esm/abi/index.js | 836 | `55582f8e8bb4b4623b03b290e5ca5c566a42d4bc42a2bd0355bebd80c16b3078` | 0 |
| lib.esm/abi/interface.d.ts | 13957 | `2a54c89cbd1baefaed665291d05b9d28ac7356536c3f681f9401d642b2b0c0cd` | 0 |
| lib.esm/abi/interface.js | 41082 | `000167889c4ff9660119e0a64f23fbe39074d1f19b5ed99b3edb9cf195eb58bc` | 0 |
| lib.esm/abi/typed.d.ts | 15351 | `74f763ea382866434fec07cd11967ac0fa2d94d3f9f98e4a908435ec98b2e0d5` | 0 |
| lib.esm/abi/typed.js | 16449 | `c9517b9980f400b0849a61de736e0b58f34ab7b6c642cd31d948128e35e9c327` | 0 |
| lib.esm/address/address.d.ts | 2129 | `53cfce94cd12e7e0bd9a5d635dd4929f5883c18135e86290775dea5b920545f8` | 0 |
| lib.esm/address/address.js | 5856 | `7a98077a0803a7c95fb5f94c4bf9e1e6bf24757e0a0813d89f121851ca1cb5bd` | 0 |
| lib.esm/address/checks.d.ts | 2538 | `9df9be9776aae375c562e7115e32fd0f2c2a0598b26ab23c3b0f1408751efecb` | 0 |
| lib.esm/address/checks.js | 3665 | `d7638bb0c5898dfd767cf0334321ea4652231ebf5b2df494a4b16c0ec99ae3e2` | 0 |
| lib.esm/address/contract-address.d.ts | 1624 | `2d868771bfc205cf27c0b36626e2c3925a55a4fcdb6e4f30f563b0ba98e583c4` | 0 |
| lib.esm/address/contract-address.js | 2575 | `b8b0a667a65843a134ca22819d906e154c5eaf24e2d7f132badd15a134988d40` | 0 |
| lib.esm/address/index.d.ts | 1720 | `3ebf9d4673a4a8bf80186f47be2697c48fd85b2dbbbfb3718744b9a94ae9bec7` | 0 |
| lib.esm/address/index.js | 793 | `9fc86d21b1924360ad50fd196fff1b6d0c23af5f0651fc5d13cbd4dab98f3b5e` | 0 |
| lib.esm/constants/addresses.d.ts | 193 | `42a070375b9fa9e09573b391dc15e9751113151288937f6d622373d8705e478a` | 0 |
| lib.esm/constants/addresses.js | 222 | `83f56033efe31568796ffd09aae24370777ff5237fc4ef6ad2cf325060b14d1b` | 0 |
| lib.esm/constants/hashes.d.ts | 208 | `77c1edc2eb2c2ef64cc6d45f846dac52c1a1cf0357c28d72a903da58b9fbf56f` | 0 |
| lib.esm/constants/hashes.js | 261 | `4751e9c2e65ee78cb8e5bc569d8746d20dc92c93647a7957d46c70742f84b7ea` | 0 |
| lib.esm/constants/index.d.ts | 378 | `8bc016c287b028ceb9ca0438967afc8bd3ec4b0db901f5cc058ebfbe7abd7aab` | 0 |
| lib.esm/constants/index.js | 376 | `e1bb0f3242683ccc9eefb81260e24863b7e929625ca9790e5f99b6e2492e602e` | 0 |
| lib.esm/constants/numbers.d.ts | 954 | `f3ccf447160ee55c440b3cdc68bbafd8393c658fb257d557745b861781ecf1d4` | 0 |
| lib.esm/constants/numbers.js | 1233 | `70e5abfd7b83a6484c59b2eb73cb1372f9aaa29bb68f53891ba836071b8f99c2` | 0 |
| lib.esm/constants/strings.d.ts | 354 | `34ac47d3fc6b5707ceaf7f0b580ee1805fa393ea045142f659b679e0332c6240` | 0 |
| lib.esm/constants/strings.js | 432 | `f14874782cf44e9171a59404bf01812fb77f91927aa9c08ec5f7d0df34099a3b` | 0 |
| lib.esm/contract/contract.d.ts | 6791 | `8418c6ff163da8295c03be007fba44281ce6c56af61c197defd0f8a11d512fed` | 0 |
| lib.esm/contract/contract.js | 35241 | `cab6926329c0df29570d9cfdf28dfd224c955a27e18eb97fc5a303227878d591` | 0 |
| lib.esm/contract/factory.d.ts | 2606 | `7334b41305fbb99b9efe411cddcae9ef17fa6d89ab081d26435f0f9a72f065bf` | 0 |
| lib.esm/contract/factory.js | 4176 | `ef64ecd778244c804c393de74e41441a912f6fdaa9d553672bcf524d5c29bafe` | 0 |
| lib.esm/contract/index.d.ts | 974 | `352d3bb36b12c1799dc302e90f3a9b47385a249fb5df3ce0e4df3cfd726bd746` | 0 |
| lib.esm/contract/index.js | 671 | `7981dd126eb08e21ee0171c09a4ac5a5e6394f709cd1bf8f6e468529246e69b1` | 0 |
| lib.esm/contract/types.d.ts | 6857 | `d0ed250ca7915611e8b150505c4b524a4ecfb1d121ef046b369976bd314698b8` | 0 |
| lib.esm/contract/types.js | 50 | `73aebe556ca95bb7a42f2e5e1a2225deb5b99798a422ed32c5cc8fac52ba77b6` | 0 |
| lib.esm/contract/wrappers.d.ts | 4313 | `14a09b10bcd25f3178c39d53b4160977293bc6bf045e52ee3c08896fdf8f3274` | 0 |
| lib.esm/contract/wrappers.js | 5000 | `03449896a0cdc15f22f2efb3369470e2263e43f1e846d055ec819e90b74bee1f` | 0 |
| lib.esm/crypto/crypto-browser.d.ts | 609 | `64e38476609a864082366bfc84e50718a596e191505fbd1b68c52d0afe741608` | 0 |
| lib.esm/crypto/crypto-browser.js | 1803 | `852a5c2a8dabc17292c4d70a77fd1f58c176128cd5e930d69d0257b396eff348` | 0 |
| lib.esm/crypto/crypto.d.ts | 110 | `0cd11cb899a92aa3f998b339a31e7111bfa01ff00e5470ba2c450b99b67c4e9f` | 0 |
| lib.esm/crypto/crypto.js | 108 | `9bda04c9ae161c70845bbf638f0c4337763252899cf1106bd808669aaa0b6f85` | 0 |
| lib.esm/crypto/hmac.d.ts | 907 | `afd9ebfe2b8ced603e34db1c54c7764c7db7bb9d67c69dd90beaeb4d99e11603` | 0 |
| lib.esm/crypto/hmac.js | 1366 | `25ae819f85ec77b008b9d64080d3e8335ea4f929eea78ed82ce13caae70b5690` | 0 |
| lib.esm/crypto/index.d.ts | 997 | `02d0e3d40ac1e761e16a96c882ae1b75a327d0f20731bbc690c15eba0f6c15bd` | 0 |
| lib.esm/crypto/index.js | 1146 | `0c3d5863e62cfd2a78f916a760dd8844a444507bc11a14a47e7369c70f200600` | 0 |
| lib.esm/crypto/keccak.d.ts | 995 | `c2189948d258e7bffb176ec0f982ff136c15f7cb43711a6457ae93d6d1a44575` | 0 |
| lib.esm/crypto/keccak.js | 1287 | `1cfaac25ce63f98e3e8433d5600fd20dc7272bb6aeba3ffa0fca8ee134b6b942` | 0 |
| lib.esm/crypto/pbkdf2.d.ts | 1485 | `7d0b3df72dc921d9f438c43ba6cb82683fa79a2ae1566946075ebbd08d830840` | 0 |
| lib.esm/crypto/pbkdf2.js | 1681 | `1f347fcd2a4d200ded8edbbb67d8b7a3278e4442476f5b10123f04c8a62b918f` | 0 |
| lib.esm/crypto/random.d.ts | 409 | `0e2eeffb8a065abf94202469089ca0def7db7d071fffb85c2d20b2a4611a8619` | 0 |
| lib.esm/crypto/random.js | 1024 | `45799cc6f169ab89c3cfea83f1168e762205a03e556940f53e13579804b022dc` | 0 |
| lib.esm/crypto/ripemd160.d.ts | 639 | `a6fe037550736f4a33d23650cb86ae83e981e3547e143073fd9e6294f5eabb81` | 0 |
| lib.esm/crypto/ripemd160.js | 959 | `b924076297b89c0f97999c453cb58ec93047fd78986415a343b2717a0de5847b` | 0 |
| lib.esm/crypto/scrypt.d.ts | 3748 | `edf4bbbd2c49e1a3ca16db235375e35fdc78c01336526b4ded61b83a1a27be5e` | 0 |
| lib.esm/crypto/scrypt.js | 3882 | `c284dc987b53e2c1fb421905ff3f97970dccc697f1a9c42fe6abc886b12f62e8` | 0 |
| lib.esm/crypto/sha2.d.ts | 1145 | `a91270b389959d4c658eb232bc98ac0d6625a2f5d815922f04184c067cf45ab9` | 0 |
| lib.esm/crypto/sha2.js | 1670 | `714fad2ddcba6933a6660219cced4173e6fa0fd2ee6d13db40a9f26d2ef60d15` | 0 |
| lib.esm/crypto/signature.d.ts | 5058 | `13c4194f23f76b20ef3bd4dd15f6da80806c08eaaff8d8b655a74ee67af2e41b` | 0 |
| lib.esm/crypto/signature.js | 11314 | `59f40dfb2969c897d5c2985f824523231a7ad3f1891347b571416e3d55286598` | 0 |
| lib.esm/crypto/signing-key.d.ts | 4140 | `52683c193bf516deb3897278f759d14325baca083deefd36e693e5c09ba436b4` | 0 |
| lib.esm/crypto/signing-key.js | 6243 | `4da3d51e128b5a6483337a06b3ac726c7552fa504ebf285dba8680bad458905d` | 0 |
| lib.esm/ethers.d.ts | 5965 | `190bfb8a3040387428311c6da0dfb6250ca70fd45fe19b066e3d20fe042b4be3` | 0 |
| lib.esm/ethers.js | 3429 | `525a528bd289c9b4d62698c2f25fb7a91b79c437e6580cc60119e13e5df311a3` | 0 |
| lib.esm/hash/authorization.d.ts | 721 | `891790a0c6238d37c521c6e37e733a7b9f3e2bcbca4b040e98dcb4fc5f31297a` | 0 |
| lib.esm/hash/authorization.js | 995 | `ced5131c482564642ff2e89ecca58e4ae300ea6ebec39d886b8748ecaa2fb009` | 0 |
| lib.esm/hash/id.d.ts | 344 | `3266a03c5946baa44bb5413f01560c1d70b41cc975cccba45d6d257e8ad6e9b6` | 0 |
| lib.esm/hash/id.js | 460 | `7a28acc94288ef163644ce8865923751d0b91123550ebae9929c2331b4d9d04b` | 0 |
| lib.esm/hash/index.d.ts | 764 | `a061f40fd57f34ae7bf038f9ee41c2fa83145f054adbda9be5cbf8a93b607209` | 0 |
| lib.esm/hash/index.js | 626 | `74bbc0bacebe045a58b084f5025296bc69a9b56cadea31aa0114e3288cf904e9` | 0 |
| lib.esm/hash/message.d.ts | 1212 | `2b00099841c56a96fa1b9c0444e95503e4467528f331685665ef74397b95c656` | 0 |
| lib.esm/hash/message.js | 1592 | `3112146f1efad6cb62d32acb6582303cc51720bd8854f39e9822713b6e18c140` | 0 |
| lib.esm/hash/namehash.d.ts | 611 | `5ba98fa53903226fa84855af5757147f3926e84cdceb8c9653c217aef3d54362` | 0 |
| lib.esm/hash/namehash.js | 2757 | `7dac6f5befc952c85b3664567150874f5b954a31762096bd139dca496362916f` | 0 |
| lib.esm/hash/solidity.d.ts | 1216 | `8ac191cee94b0b802d9295377456de2ded468f8212c7c147eed21f69d78b1c2e` | 0 |
| lib.esm/hash/solidity.js | 3897 | `68861bf3779de30d93227ea49c888adb6129d9345f6bc452d506ee1c648ab2ba` | 0 |
| lib.esm/hash/typed-data.d.ts | 5377 | `057980116843d7c307b7b9df0df6272fbb12b48e3a4b386fa4960cb39f40c085` | 0 |
| lib.esm/hash/typed-data.js | 19734 | `507dacd1218da8dc2a7a08395900c9d6b095aa2f429f62de1f5c0d06dae8fcfb` | 0 |
| lib.esm/index.d.ts | 352 | `e981c8c1e332df4f83dd27eeb3b0557a8afd36ffc5110b09e60d0a1a5b8c682a` | 0 |
| lib.esm/index.js | 350 | `586bc08ce4c6bdb64f2972f9284f9eca568b7211f33c387d5b83f63887ffc468` | 0 |
| lib.esm/package.json | 438 | `71a3a95826a9a4955ac66b62e7880e817658723e678114457e2e5d1aab27a3a0` | 0 |
| lib.esm/providers/abstract-provider.d.ts | 16097 | `e8b5ea1f3bc2c2397a8a793970a1c3b4b7664254104d55bd3520958f840d3b9e` | 0 |
| lib.esm/providers/abstract-provider.js | 51772 | `82859a8d79a59d230a9d99b385e6fd8871e0af408644b467f9d2f19048cca0a6` | 0 |
| lib.esm/providers/abstract-signer.d.ts | 3145 | `afee3d5f2fd0092e4e9e2a03bde1729b599e0521e763dd145a7489a8ba97e63b` | 0 |
| lib.esm/providers/abstract-signer.js | 9986 | `b2be508623922d8555e56f06730777fd35f362d34766a8248e35c2d7f1e3efd5` | 0 |
| lib.esm/providers/community.d.ts | 974 | `82af483335b93a35000fca8ed01c5f8c7aa23bee91896d6daafac88e4bf263bf` | 0 |
| lib.esm/providers/community.js | 1545 | `787664bfd59ff9cd78e2258403658adf4bdcfb070b27c1ccbf0fe6df0e977312` | 0 |
| lib.esm/providers/contracts.d.ts | 1252 | `dc0f45854448366e46ed513f5d198379da258376d466f11e6d651dfbb968a3d5` | 0 |
| lib.esm/providers/contracts.js | 48 | `427a6852d1b4fbc59c12b396120836e73895fb11bee3ec3841f58f9c9f32499d` | 0 |
| lib.esm/providers/default-provider.d.ts | 1893 | `209a4f359634064b7e07b300eb87f46909411586015a75d771337301285baf6e` | 0 |
| lib.esm/providers/default-provider.js | 7249 | `6769d5785ac205e0e9ef9d4ca7c23d23ced021130ec8fda3e5f0d5ad12b0925d` | 0 |
| lib.esm/providers/ens-resolver.d.ts | 5310 | `c845638f8e301087c49190b9f7c259aa90a79755e23625585e276fe84b3991c3` | 0 |
| lib.esm/providers/ens-resolver.js | 24536 | `8607e03b326a3d6adf957adb8f8b17a2e8ec8ebf9b5aaa4d7878729f5e2582c2` | 0 |
| lib.esm/providers/format.d.ts | 1087 | `b31b025f01a686d46771b54ae03b966af7fd9fd0a5480003ab7e390c43752e2e` | 0 |
| lib.esm/providers/format.js | 9547 | `4d692c5c5b4ff22bfb96eb721ac6bc0f542ba2c1f32f5633f1ef0e306991c2d7` | 0 |
| lib.esm/providers/formatting.d.ts | 8681 | `05c620cb5382f37a46eef76e57b2769109eff2190c439893d7c40fdd04eb5148` | 0 |
| lib.esm/providers/formatting.js | 169 | `c080f7e38b8b2f39d43e56b010e3075f033bd2a4d5e046470c87b8089ac518e4` | 0 |
| lib.esm/providers/index.d.ts | 3552 | `90e04e44bf25f8b6071d3695296abdcba54bc1803064e48b2e739d273f9eace7` | 0 |
| lib.esm/providers/index.js | 2338 | `42c8cd3e814001cc3655bd34c0320f782ec62df4b2fa1773498d52de2ee3eda2` | 0 |
| lib.esm/providers/network.d.ts | 3376 | `87180277f45dbc2a384fa331b8db3174ae42f5445955469d1554840b245a76d5` | 0 |
| lib.esm/providers/network.js | 13575 | `8650e61e9b29fce7753c46e9df831d85557a55b0e58806217d572a1e9664e600` | 0 |
| lib.esm/providers/pagination.d.ts | 192 | `b000559850c7766aeb0a13a56f5451e6402feacf34018971e68919362884be0c` | 0 |
| lib.esm/providers/pagination.js | 49 | `442d5a85099066b9f94020a5199bca7ebfcb45dd4f9d0ba7b0dc595afa55893d` | 0 |
| lib.esm/providers/plugin-fallback.d.ts | 695 | `435fb4fb1fd9f596628a47bf8f0b38575d6b3863ce57a3fd85ad0fe0d6294573` | 0 |
| lib.esm/providers/plugin-fallback.js | 880 | `569eda7e1593efc7c49618b7da9a4d61b2267e5febd9b20057477de2c87ac83b` | 0 |
| lib.esm/providers/plugins-network.d.ts | 5569 | `f52c9a59a36b2b80e82108132883624e1ca5889b8161c96685d5b7abf1221d3b` | 0 |
| lib.esm/providers/plugins-network.js | 7475 | `9d7192075d35e5ff7fed7bd7776eda54b10b29a1267d1d0122be4a2d24e879a3` | 0 |
| lib.esm/providers/provider-alchemy.d.ts | 2001 | `7d03d9adda53f51aba7375d78b50c82a478afa5d601ccadd5c8ef2721c19390d` | 0 |
| lib.esm/providers/provider-alchemy.js | 5395 | `f1d065d704fb8749536fc555b0a659aef25ed65b9ddf55d493092e2f66cdcb29` | 1 |
| lib.esm/providers/provider-ankr.d.ts | 2311 | `9459ddcf024cf57584f329bac738c8a26a8a76bb85b6f97ebaf755d270f1eb45` | 0 |
| lib.esm/providers/provider-ankr.js | 4758 | `030c4a10efebf3a3697455745f1b7c6b0a6f3a6c7553355a3ea1ba8e4efa231c` | 1 |
| lib.esm/providers/provider-blockscout.d.ts | 2149 | `098d93d036a4f80dbd002010a940753570dfa293af4ed6e2180e2dec8aa893b5` | 0 |
| lib.esm/providers/provider-blockscout.js | 5297 | `48e9c5a141e95e303c5460cffa8d9625248e4fe044221f85f5f50deca18bee79` | 1 |
| lib.esm/providers/provider-browser.d.ts | 3643 | `314359daf8d71a2883cbc054dbf16c4161f1b66c1bc01e0e737262cc0dfaf2ec` | 0 |
| lib.esm/providers/provider-browser.js | 7910 | `1be5ee01fb6d23cc496c5e7fc06db9c78a2143198f427ded3f729191f79066b2` | 0 |
| lib.esm/providers/provider-chainstack.d.ts | 1686 | `3890ab6996506722cd1fecd0b5b838a5af654836abe484c99696f82dc4147f32` | 0 |
| lib.esm/providers/provider-chainstack.js | 3372 | `93f509da5bde5d93ba78b6eb99372dcf68730e36df22461abb8adfc4ff3d0f45` | 0 |
| lib.esm/providers/provider-cloudflare.d.ts | 404 | `825b9b3691d29482cc2034a8e6292d4800222601c2a883ad3e777182bad6fa04` | 0 |
| lib.esm/providers/provider-cloudflare.js | 736 | `5186c4ccb61eb3b7e3f199a8d8b2e62fcd5fb25bfeab141c8d49f1815532e42d` | 0 |
| lib.esm/providers/provider-etherscan.d.ts | 4985 | `ce51923912e666f0440bf60da367fa5bb59a33816f093de780d5e350cb02c220` | 0 |
| lib.esm/providers/provider-etherscan.js | 24371 | `bdbb350334aed80ee16344940a0e07dfae1eb87f958fdd5e710783a63bfe718c` | 0 |
| lib.esm/providers/provider-fallback.d.ts | 3501 | `167488303ef27a82d6bf439a7e09901c88ce520b2ca70398698713cf29f7599d` | 0 |
| lib.esm/providers/provider-fallback.js | 23359 | `448caf257ac70f1d0546cc4f1c6f59227e8e44baa239c7d0126345cb85817a73` | 0 |
| lib.esm/providers/provider-infura.d.ts | 3755 | `3e6548ae5c61384f7faf2f75793628fe5ef06c56060bffe86bda3cbcc7d94524` | 0 |
| lib.esm/providers/provider-infura.js | 7063 | `a660b7a1d453639be72d0d12571d01d0a10c16842232672fe49fd575e34efb4a` | 0 |
| lib.esm/providers/provider-ipcsocket-browser.d.ts | 130 | `94daf1df14a61f222bcf90b95f9b4eade5cdf1143bf139769a37ff5671f16eb0` | 0 |
| lib.esm/providers/provider-ipcsocket-browser.js | 121 | `43a8be3998f5cb33bb42f7608e1e988d916f75c99998cb7c8e5642b4c7b1fdc8` | 0 |
| lib.esm/providers/provider-ipcsocket.d.ts | 783 | `2a444ea55b9bc6f78215d2462dfdd008a9d2d5f2119ac541ae57b83847e9786a` | 0 |
| lib.esm/providers/provider-ipcsocket.js | 2128 | `e181aae417ea056d707a10493ffaf57210aae84c3331b5a525897d32619a38fa` | 0 |
| lib.esm/providers/provider-jsonrpc.d.ts | 12449 | `25fca633b8863ffd82f264d27c3f3bc70535bf66d484191bf3920bfd8cf7d764` | 0 |
| lib.esm/providers/provider-jsonrpc.js | 39192 | `6a6a0bf4db927e18f61c4b565514b4255ec3659156bf586caff21ce852ea0942` | 0 |
| lib.esm/providers/provider-pocket.d.ts | 1979 | `2b4630bc489a8585742ced3952f491fe741d8f38bdd6d205d1a938baccddbda3` | 0 |
| lib.esm/providers/provider-pocket.js | 3622 | `1f94874c1174d5e5b04a32f9294333c014bea76550e2b358399a72a65d6f1641` | 0 |
| lib.esm/providers/provider-quicknode.d.ts | 2178 | `3bba9d77cfa07f2c6d174f804317e14d2573ed8234ec14152e51b207c90d1c47` | 0 |
| lib.esm/providers/provider-quicknode.js | 5627 | `07783d3b60afb7566a683a43f51cd63508dc38269a2944fa8c1a73e7ec84f81b` | 1 |
| lib.esm/providers/provider-socket.d.ts | 3802 | `55e749e97482f1e8867594715bf2e12cd38a9ff3d5dd4775f8a038b66573608e` | 0 |
| lib.esm/providers/provider-socket.js | 10181 | `992b28fcb1fdba4e7f6781d8e5d9bd5fcf2bd7973403767087687a5c42f57f63` | 0 |
| lib.esm/providers/provider-websocket.d.ts | 1464 | `c33f0b0ce44cc14942c7fdb26da13b6a2b2f048c9b344f015a3789a7a12604ba` | 0 |
| lib.esm/providers/provider-websocket.js | 2628 | `910f31287518f3ab0bea8c94ee9a3a9820a796d4b52118dbaa733edc28c84ffe` | 0 |
| lib.esm/providers/provider.d.ts | 41089 | `b199e3fe2e42e49f54a6679ea0194bc72236c0d12058f588a0fe379eb1e5a52a` | 0 |
| lib.esm/providers/provider.js | 43686 | `a92a54a180d13444929d9afa48c28fff9b9a0addeacff28c93d00cf34cda08af` | 0 |
| lib.esm/providers/signer-noncemanager.d.ts | 1532 | `97a67bba2c8123cd1fc6412042fb38ceee1477e6d844b5ec2dafea21f7f3e6f7` | 0 |
| lib.esm/providers/signer-noncemanager.js | 2294 | `87e6543d44dab83c9d4598b425927423b510f8f4fca542f7e97b4df17acaf329` | 0 |
| lib.esm/providers/signer.d.ts | 6220 | `fedb24ddffb67350cee62144c15d470251a1d0637b5ba37da4c836083165ce47` | 0 |
| lib.esm/providers/signer.js | 45 | `28ca9eb477ad3f2fbb659e28f41cd1e0bc0efd8679da751986a17d17342b7ae9` | 0 |
| lib.esm/providers/subscriber-connection.d.ts | 709 | `6636880b988746258ec8f03fba033683a5c1b8e2cb28eb3a5984db35b221f456` | 0 |
| lib.esm/providers/subscriber-connection.js | 1378 | `6bc5239cc078e816891f8b23daa0d70503945d8bac1b05b461c378b0f5a288bc` | 0 |
| lib.esm/providers/subscriber-filterid.d.ts | 2450 | `a72c8a6b4ea88c20c4b0e0aab6fd8b352ee36d870c4806a91526c8bc764b1b20` | 0 |
| lib.esm/providers/subscriber-filterid.js | 5450 | `ea742cde1e757624f71bbdad26d376d5cf924685a57be72a1be50942d3981f0a` | 0 |
| lib.esm/providers/subscriber-polling.d.ts | 3232 | `8192008e5b481302fa03ad48b4a6b0c266ef6b53cbb9a9589c3feb94a3515b5d` | 0 |
| lib.esm/providers/subscriber-polling.js | 8552 | `5a51b23bcc553333e4e62bc2afa520fa82b22787ac8c0b75d51781f15a4352be` | 0 |
| lib.esm/providers/ws-browser.d.ts | 107 | `529d9b7f4bae95357c2a078c62ea0de073a42a2a2178481fa3c3cf7b523375b7` | 0 |
| lib.esm/providers/ws-browser.js | 404 | `bc09b548e2eec4f696b7a60c9ea9f34f42d0543f2ff341f4ca6ae77fe9d93f60` | 0 |
| lib.esm/providers/ws.d.ts | 64 | `2b550ff58b50e3d9715b4790748c82ebbbf74f4c41824600aa3416b690d54dda` | 0 |
| lib.esm/providers/ws.js | 62 | `caefece82d27b0cb70f44639e1a76837ebb17b142addd5e200f70843f3dea1dd` | 0 |
| lib.esm/transaction/accesslist.d.ts | 260 | `0df6ff347a9d41713af680b29476a430d0f0eaa30465efe3ef149cfbc7b63a3b` | 0 |
| lib.esm/transaction/accesslist.js | 1548 | `7dcfa9df4861fa918bf1437f0efc6d42ac778d1ab3269152a785ae74f30f750c` | 0 |
| lib.esm/transaction/address.d.ts | 614 | `d95862256da7116eae8b69d1fef8b1ffe47e221787fb7541b90295336731274c` | 0 |
| lib.esm/transaction/address.js | 808 | `6caca4ca24eb2cd2b8b420ca978fb787d82476507c211fd4547f0a8ac1d27a68` | 0 |
| lib.esm/transaction/authorization.d.ts | 193 | `12a68e03b6c646f7eff6dee0bfad0669aa3f0bf84a62c0fe69c637fd2a4cfb46` | 0 |
| lib.esm/transaction/authorization.js | 478 | `5a201be0e8f1bb96a7141ceecb8d9f2ff831406c2966871eb1cbdfe4fdcdc3c5` | 0 |
| lib.esm/transaction/index.d.ts | 1323 | `32d70e138cd4199ae0516401cbade1343c27baa0b8d451da6d8cf753d5546668` | 0 |
| lib.esm/transaction/index.js | 400 | `76cd01c430c30800cfa358d2a0303f64bf579e4fc6fcab1435a9ef94d89cc8e1` | 0 |
| lib.esm/transaction/transaction.d.ts | 13059 | `039cee8feda0a8da4d6a873792b5f935a7eb5ef276bef33f3918b10e96292fd8` | 0 |
| lib.esm/transaction/transaction.js | 45854 | `213cf05fd98e84217afd2e865a1d24bc16c44a76048afe9014ebcd260eafed65` | 0 |
| lib.esm/utils/base58.d.ts | 873 | `c1d45ad150211313b9f4965a7f984993dc07313a8e81255f3d6d1c2d2b7a8fd9` | 0 |
| lib.esm/utils/base58.js | 1932 | `38fb0bf3962b8e24cbe8c9280a8de7972095c0da612ab32c0c70057e5ec5686d` | 0 |
| lib.esm/utils/base64-browser.d.ts | 220 | `143c50cf9d69e670767b881cc31f710ca3f96491dd4de645105c706a1606bf51` | 0 |
| lib.esm/utils/base64-browser.js | 575 | `89cf03c8953a0a2a40df380743bf396874af63e33ac304e8602296491e13e015` | 0 |
| lib.esm/utils/base64.d.ts | 1057 | `3099c6d6ca03d5f2098837cac45e7793786c54e06dfa882ff4a854bddeb3f97b` | 0 |
| lib.esm/utils/base64.js | 1466 | `ee069843b833a821f5f8a51bbc17c100cc8e8c89d44198fbe5aa62e465f331ce` | 0 |
| lib.esm/utils/data.d.ts | 3180 | `f0b25ecfcc4cad84f95951dbdc13686433c5a7c54deebe9a43b1b4ddee1bb5be` | 0 |
| lib.esm/utils/data.js | 5052 | `30a7f033963d91c9edb2b94586b5e022c3919075d0cb402bc184f3a2d7d9fafc` | 0 |
| lib.esm/utils/errors.d.ts | 16678 | `fe0c1e2efe12fcc7e0409e799a31b02e3aa3007e516af720106da72e8c22157a` | 0 |
| lib.esm/utils/errors.js | 7595 | `86b90fc247ae3a11abd50fa00f34a557eb11d94a4343dd92fd2833c1ddf5bd98` | 0 |
| lib.esm/utils/events.d.ts | 2302 | `7a8ead38ea10e5187f72c8ff01938f91ee8341bfdf33c467b26d049cf2719530` | 0 |
| lib.esm/utils/events.js | 1129 | `c0d74c2f2224697ac730ad3aab98df620dd343ef297d7f522167cdab5f47c83b` | 0 |
| lib.esm/utils/fetch.d.ts | 12331 | `c8a94ee463980a023d5b0591edbd32c6c729cb217aa3901b23473295030f4354` | 0 |
| lib.esm/utils/fetch.js | 28676 | `a161fd9671c87aeece477816e1888e27bf8f9b79bdc331f0a41f02ec340afb6f` | 0 |
| lib.esm/utils/fixednumber.d.ts | 9160 | `9a721310a62782bf36638b10fb31aebb3ff34e2857a3fa25f0c243a67b39bff2` | 0 |
| lib.esm/utils/fixednumber.js | 19466 | `b2c6566a0ba02d1961d1ffbc55b0d23a9fb4374cb331c058993baeb7eed0ee35` | 0 |
| lib.esm/utils/geturl-browser.d.ts | 335 | `b3ea4f3cb1a74cc33b05a53306ead10e86ecba946597d395f3bb89be319938e7` | 0 |
| lib.esm/utils/geturl-browser.js | 2287 | `6904c603247f68b07b5c516796d8f5e16a123915f620d64cde448af6450d691b` | 0 |
| lib.esm/utils/geturl.d.ts | 370 | `32853e5f765babab7f3de559d9ecbe68049dd064e231c2da7e31ec32e0caf28d` | 0 |
| lib.esm/utils/geturl.js | 4700 | `8d782107378084930c3f14ee5556c6dc81bc3a29dd64c059d86893724b0098b1` | 0 |
| lib.esm/utils/index.d.ts | 2430 | `aa546b567b477fcd690218295cbd9eb877d3e25bdfc049b40973702712d00788` | 0 |
| lib.esm/utils/index.js | 1361 | `87f9f65d29d5686dbae0d032fd7a3d19d0ed6062ba63641648c5dfc7bc56aa3e` | 0 |
| lib.esm/utils/maths.d.ts | 2478 | `ca1b7949fa09108f8890ddefa6ed3d2c3461bb283cd8a09c0d5037ebf032ec71` | 0 |
| lib.esm/utils/maths.js | 7688 | `ad3bcf8a31ac229e317848a97b5ab3cb976679747c78518a2754fefaaa48e2aa` | 0 |
| lib.esm/utils/properties.d.ts | 624 | `1cdd7ea3d40571e6ed8cd91a1ef9f390c6d845d7adbdde29a61ca1af4036e7c8` | 0 |
| lib.esm/utils/properties.js | 1603 | `8767551fbaf6563360089fd1061348ab1751006cbeec366dc7b2ab5013b1c879` | 0 |
| lib.esm/utils/rlp-decode.d.ts | 245 | `8b49bd9c17fce53462e3c2094d961cb5bca26b3166cdc3e8c6952c00963b6a59` | 0 |
| lib.esm/utils/rlp-decode.js | 3142 | `3a981835374690162a61f0d72dc1080d066d75be6827de3d99481f78b4442f82` | 0 |
| lib.esm/utils/rlp-encode.d.ts | 235 | `d07f8e8c858239ee0fa66e25cc9e7034d8fe7b0876be61d3d2d22c06fdc6944d` | 0 |
| lib.esm/utils/rlp-encode.js | 1431 | `c6d92abf28f6589d2a814f57b64600125504d3527f1a0e43b1a09015fb86f033` | 0 |
| lib.esm/utils/rlp.d.ts | 571 | `e29069b75d8b588f0cd62242dc120178d0518aeddf9757a440cd35c2606de2d6` | 0 |
| lib.esm/utils/rlp.js | 315 | `2b6e38f618deedacbd421cf5cd4782ea1d1d27f4c562e7e9c063c17920ccb5a0` | 0 |
| lib.esm/utils/units.d.ts | 1006 | `fa2f8c5eedd3ed40be37deb32999191e1334f03fd402bad36c4b5a6da92470a6` | 0 |
| lib.esm/utils/units.js | 2858 | `32fb2d99a3ce9ad249b75a0a4c09c8fdee7814eec9419d4d0c228114f726ec18` | 0 |
| lib.esm/utils/utf8.d.ts | 3945 | `2d28f80386b506e00285b9cbd0dc1a695c810cb3bc61e0b2b081aac304ee3bc4` | 0 |
| lib.esm/utils/utf8.js | 7765 | `d6cde7314bea1ea5f17756110b64dc60eafdc03d01a8c6261da53097873bd8a0` | 0 |
| lib.esm/utils/uuid.d.ts | 280 | `00f74835b3aaf3690d7480f1ad08fe02593113e38e7a26d7ad27d327f5b9af8f` | 0 |
| lib.esm/utils/uuid.js | 894 | `0db82b8953b305fa4ec797e2fc2b8b1971d107f8d8eb218c99caa014b2cf6430` | 0 |
| lib.esm/wallet/base-wallet.d.ts | 2128 | `abef0d03eb94032878417c5594b32bb25a44c14002933fe5b188ce7eb72ee140` | 0 |
| lib.esm/wallet/base-wallet.js | 4805 | `9bfb412471e5fb83f3fd4d015c0707c6248bc276a4bcb010686cd59a3125eec6` | 0 |
| lib.esm/wallet/hdwallet.d.ts | 8335 | `7f1ddcce6f5aa325fbe874137ed533a4e23e557050dfb15747a9e19e2d6b463f` | 0 |
| lib.esm/wallet/hdwallet.js | 18581 | `bbcf201f4df3e6ad55d631246ac91fa7e801c418f6923147a1841629882c4ca9` | 0 |
| lib.esm/wallet/index.d.ts | 1341 | `deef751ee7953fca04f567770514f93f9d2fa1254e5cdcb7da5229757c65ea39` | 0 |
| lib.esm/wallet/index.js | 1203 | `d8d575295146c3e058055934bf27d1a190319356ae4ba28080301c4dcc58529b` | 0 |
| lib.esm/wallet/json-crowdsale.d.ts | 929 | `a10dc770ceb0a20ecde6e0cc37ed95d1c5390f34eb7d7930407fa700354db3b5` | 0 |
| lib.esm/wallet/json-crowdsale.js | 2108 | `0bd0dad72e021e502a305e3c7ccf4b3fabb5f40d26977b29950efdd3299936a4` | 0 |
| lib.esm/wallet/json-keystore.d.ts | 3211 | `0e41bc8a6621ff6901a89fb0cca175731835723a4d9bd6ba3974cd0df809be89` | 0 |
| lib.esm/wallet/json-keystore.js | 12774 | `725510a247d7078e24e194bbb87f73235d4c3945691c85f7dbf6a2e063b6a857` | 0 |
| lib.esm/wallet/mnemonic.d.ts | 2319 | `4af291a429ee3d5516e506b507453e6fbc80fcea52bd62ce18190702acb5c807` | 0 |
| lib.esm/wallet/mnemonic.js | 6254 | `8125b28441295ae3d3400ec79447a539f29c5bb0cac689a673fd994e40c739f2` | 0 |
| lib.esm/wallet/utils.d.ts | 351 | `b424554c62c1b741ac0da65e79b5cddf8b1e228b30d1a73ba8aecedddb78ebde` | 0 |
| lib.esm/wallet/utils.js | 4117 | `56a5438c1739f0cddb4a150c01b4931ea882a22215f6f0c4b029cfe9ce1e1830` | 0 |
| lib.esm/wallet/wallet.d.ts | 2940 | `aae5435e7c8b476b2b4fd960fb4ca413c9ed6dc8675d8db29a895ff7389e638f` | 0 |
| lib.esm/wallet/wallet.js | 5592 | `71b7b77c35c0320ba53b57875b1df137c89209b6160dec13e793d92564659455` | 0 |
| lib.esm/wordlists/bit-reader.d.ts | 141 | `03487c22bbf8b0fa0ff0b7b865b5339b81a826a3233884102d4ccba8796ec29d` | 0 |
| lib.esm/wordlists/bit-reader.js | 1013 | `b062579e25800a07beb0669647df207e80925727370a8151d283535397150178` | 0 |
| lib.esm/wordlists/decode-owl.d.ts | 221 | `8c42c85090f1bcbd0523cee41536d0500100e73af5983fe6c7f6aa5bb9089c40` | 0 |
| lib.esm/wordlists/decode-owl.js | 1657 | `98e00c4948789fe34b8c1aeef91ad816298b17fb8e6015a3d11a81c55b7e371d` | 0 |
| lib.esm/wordlists/decode-owla.d.ts | 144 | `5983ead9b6aad7a3512864366014f72032b6a423bd1d661bf814a2a2c83ce083` | 0 |
| lib.esm/wordlists/decode-owla.js | 1055 | `a8b8163884a338c50ea82d0b673cd36052f2fc532644a6466617f86e1d79ab9a` | 0 |
| lib.esm/wordlists/generation/encode-latin.d.ts | 644 | `9fd984d4e94660bda8d5ce949b32dcdd08220635a7db00bb022f2b41734e83bb` | 0 |
| lib.esm/wordlists/generation/encode-latin.js | 11833 | `0bf4a437d5cc14e2ab00eb63b43a990409208304d3c01f78b296e56aee76970c` | 0 |
| lib.esm/wordlists/index.d.ts | 1043 | `43881022601c5fc87ff751cd869103981215489384643c71d5c8e58619f7bc96` | 0 |
| lib.esm/wordlists/index.js | 1041 | `5e28c87aa299bb472f161463387720ad1f6403ed3e4d85c629099f881f42a5dd` | 0 |
| lib.esm/wordlists/lang-cz.d.ts | 639 | `0154e7bbdf0ddb952e11a7a5f7e43b1862d67a567985437fdddd681f4c9e4075` | 0 |
| lib.esm/wordlists/lang-cz.js | 8014 | `ad53ea06594c7ac9f3e3c6ccf1aa9d002f58181a8bb3de942f641f96e3c5d795` | 0 |
| lib.esm/wordlists/lang-en.d.ts | 636 | `3fa498ce08b62f4148452e553d138429a5d928f8c39395683ef941856d9d8942` | 0 |
| lib.esm/wordlists/lang-en.js | 6893 | `55c72f9f81abd618eb892d5c3669d427adb31a40ba5d25d5946e68b67eae4472` | 0 |
| lib.esm/wordlists/lang-es.d.ts | 639 | `206c91c5c29bb0e66b1783262e5b6b0f1504ab033a81024977cc9a4484e36e8f` | 0 |
| lib.esm/wordlists/lang-es.js | 7157 | `aa5c51a354223ae1e46ee9ccdd917d13e9230adc727d762cc100cd17ae00e35d` | 0 |
| lib.esm/wordlists/lang-fr.d.ts | 638 | `b5e820752d23030fdab51a822e31662a46e09c188d301c31483965b30baeed94` | 0 |
| lib.esm/wordlists/lang-fr.js | 8908 | `e1540d1c79ee22a57458b774930e8f42a6b57283a60d8e76fbfcdfad82491586` | 0 |
| lib.esm/wordlists/lang-it.d.ts | 636 | `f909868bbe43d44156945d8c3d1f9f4489e6c7ae42141cfb57a8189428086b0c` | 0 |
| lib.esm/wordlists/lang-it.js | 8544 | `e2f379ac83c795df663bf9790fd38bb1414d079e0cf70cb67b868441463755a4` | 0 |
| lib.esm/wordlists/lang-ja.d.ts | 785 | `fc8df545bc58bb69aa4b930f8f6e205e13cbefe6a1fa85b1217f4281f56c503b` | 0 |
| lib.esm/wordlists/lang-ja.js | 12817 | `86525412225add037ade271c8fdeafbab0064d31bc4e241f1eefd026450a39d4` | 0 |
| lib.esm/wordlists/lang-ko.d.ts | 701 | `12336beed48c3f0ce3bac5b71841539f62ddd1b0288e108ca1ce7ce951cf6129` | 0 |
| lib.esm/wordlists/lang-ko.js | 14355 | `edc044bce4ebfe89c6cb41b550be41db045409cd7e15711aa8452628f7b66248` | 0 |
| lib.esm/wordlists/lang-pt.d.ts | 639 | `1cecf5360f1fffa45f72c287f51be1ea3e12e7a92d5047750993f0b7101c7557` | 0 |
| lib.esm/wordlists/lang-pt.js | 8383 | `3eef98979c0463189eea8798c373cc690f450debe21b89264b5cea3190fdb8a5` | 0 |
| lib.esm/wordlists/lang-zh.d.ts | 1059 | `997e3cd9dc0b53fc3270eb75935d99479ed3b2a087544a2499737689b11e2a1e` | 0 |
| lib.esm/wordlists/lang-zh.js | 10828 | `839289565df3701ce1f5675d2063577ab372d70eba1fbed51f84269a156d96b3` | 0 |
| lib.esm/wordlists/wordlist-owl.d.ts | 1044 | `b908d48bfaf9a491303e5970101a2b9895cc6f8f4c6abfabd6bb93ca425a22d0` | 0 |
| lib.esm/wordlists/wordlist-owl.js | 2150 | `350ffe433e9e7a05737b90df71f724b45f5f80649b11b9a24cf4265675adb370` | 0 |
| lib.esm/wordlists/wordlist-owla.d.ts | 982 | `96d22cd33030a9b7bab47064406ef0fbf7502fd2b2779af845bb63c27e8ca92e` | 0 |
| lib.esm/wordlists/wordlist-owla.js | 1124 | `8e1d34c678586c252f8d2138c619d9b8413143f010189c1867e4d1534b19e800` | 0 |
| lib.esm/wordlists/wordlist.d.ts | 1650 | `486a4acd1ddabb05055e75770bd51ffa166b1ac3940ec4019761f06c3c3b1d6c` | 0 |
| lib.esm/wordlists/wordlist.js | 1427 | `77918b03eb000c5f2b1e25ae0983787fdcc6176e6b7cb4b830aca2fb8dc9a665` | 0 |
| lib.esm/wordlists/wordlists-browser.d.ts | 152 | `821c80cd6b923d8e3f842d05bb92e69fea2989afa27db821720e68c2220cd38a` | 0 |
| lib.esm/wordlists/wordlists-browser.js | 141 | `2e55be9da951806b9e11aee6dab72ca9c80c78ab2312d129b58e4bccbe9246a4` | 0 |
| lib.esm/wordlists/wordlists-extra.d.ts | 357 | `0a9d1c6c00ab47eadbe8d21dc420603b1cc4d7f400663d0d9c10d2831e01e9d9` | 0 |
| lib.esm/wordlists/wordlists-extra.js | 355 | `44c92af92f836b4efd1a098cce14238148d216d46a61a8252304cffc35a53274` | 0 |
| lib.esm/wordlists/wordlists.d.ts | 658 | `cd564236c3689e0237b1b16c779deba4bf0905949b2cd1332b867a255a1fca61` | 0 |
| lib.esm/wordlists/wordlists.js | 1216 | `92957d7026a6e6e95d9666b393079f619ef7b18caaf74387f1f2f9f2ed996853` | 0 |
| misc/basedirs/lib.commonjs/package.json | 440 | `9177de1f0725735d11b559b89a246932e5640531f046d63feaff45de1bf2fe08` | 0 |
| misc/basedirs/lib.esm/package.json | 438 | `71a3a95826a9a4955ac66b62e7880e817658723e678114457e2e5d1aab27a3a0` | 0 |
| package-lock.json | 76577 | `b8ed4724b0acc4446ac2b0fc85b0727102cbdb7c3f887953d28b50548d4a4e05` | 0 |
| package.json | 4945 | `d644d7df228197962e4ca19824b06e8d50dce0b5ee2aced63dcfc2a11ec7b90f` | 0 |
| reporter.cjs | 6783 | `0dfdb4180cab16dbd2c831e2b8e4707de188578069ca4772c17de1bb607b4431` | 0 |
| rollup.config.mjs | 1422 | `bca5b9181135d843d40c16e6cd45121f3f5f30c6f6e9cf55c548d1c208fd6715` | 0 |
| src.ts/_admin/create-release.ts | 1398 | `d462aaff325f7abba647ad0675aabb7e86a92436a6f68ba943adfaf25e981be4` | 0 |
| src.ts/_admin/generate-diffs.ts | 1112 | `5a3ef793d0a7f9a08e15d823ec50224f7c5c15f045bec669a0a24d08c05d5a82` | 0 |
| src.ts/_admin/test-browser.ts | 14509 | `c627fb35fface44d959a85cc481c10d65471aa6ed3492860035acf9576c4c9ae` | 0 |
| src.ts/_admin/update-changelog.ts | 6157 | `8ed0923347ddd09a2f117d9c72dcd8b84f96215dd591d707a2f426714e088739` | 0 |
| src.ts/_admin/update-version.ts | 3680 | `5a8f5ae29ff0b94f1a1ee41a345eda17b83f11a8f9e2f4bf567b36056899cab8` | 0 |
| src.ts/_admin/utils/changelog.ts | 812 | `7f1585a45d73e1f60e25474443403cefc33cf45930599c00e42556c559cc16ef` | 0 |
| src.ts/_admin/utils/date.ts | 708 | `e3db149d84746f0c54abe26251e6be3688ae2c9e846060c367db7a77649c8646` | 0 |
| src.ts/_admin/utils/fs.ts | 244 | `58416b832d1bfc761b5f5310052c79d34346cb96a68f92df571c4fd8575ca396` | 0 |
| src.ts/_admin/utils/git.ts | 3217 | `f72061bc5735c1a1056244654a81f29ed986b5b8e85b3c96edcc992cb7803a01` | 0 |
| src.ts/_admin/utils/json.ts | 1289 | `fdfa0d5aaa87b81c5504fb74ee64ed813ec2f7ad1284808e046a595821eb81c0` | 0 |
| src.ts/_admin/utils/npm.ts | 3186 | `317096a8b7fd9a18f088536bbdbc3bd8fa40f27c5c16ef42f6146773589ee21a` | 0 |
| src.ts/_admin/utils/path.ts | 385 | `6f56ce32aebbe1f7895c2a27ef98cf55c10cfef5b492cbb282d407eb02cbf938` | 0 |
| src.ts/_admin/utils/run.ts | 1728 | `897640aee188628ec77a10b8adfdb678cf6cec00bf200859d505b86bbb8f0360` | 0 |
| src.ts/_version.ts | 153 | `b9eaaa6b5d62304b40d1b6bd38a70f8b2e341bd1c00fd6c3e9155b9fcc946106` | 0 |
| src.ts/abi/abi-coder.ts | 8813 | `2391fc9f81dab3b26c8bf5c21ca2da98acc17da99108101994c4bc0f3625859e` | 0 |
| src.ts/abi/bytes32.ts | 1214 | `b8f2e8ba724ec671dcc235bc8a9b30edee637de29e9ec42481d1360681048c6c` | 0 |
| src.ts/abi/coders/abstract-coder.ts | 17682 | `907ea38bbb756881c27614af12d31259e84e9a917c6dc6bc107607a7a51d9e73` | 0 |
| src.ts/abi/coders/address.ts | 928 | `6aa0a05bdda4ee48513e4479577764af9ab098036cd2f6def862bb8ded7d820e` | 0 |
| src.ts/abi/coders/anonymous.ts | 666 | `76739e3a49a3a263bc68457711a68a397da21d1200885b5612e1ed9b9f531b52` | 0 |
| src.ts/abi/coders/array.ts | 6397 | `a6d2dc265563e058365fc36791ab0a229921d27b42ab97e84994df212311798d` | 0 |
| src.ts/abi/coders/boolean.ts | 612 | `66fee9dbbfa354600870c304d982a23d3867510d3ea954b153b47e5343f5cabd` | 0 |
| src.ts/abi/coders/bytes.ts | 952 | `80f8624b98fdc5f1904ab6a14aaf7f5935915282e240b6dc4fdc1203329514ea` | 0 |
| src.ts/abi/coders/fixed-bytes.ts | 1128 | `0d0c6bf899e6fdc6c406e1eaab4f50bcea30ab4ae8d695703f0c84a5830fd16f` | 0 |
| src.ts/abi/coders/null.ts | 603 | `9acc7cbde1fd87a10fdaccefb5de82b59eed96363e641053b5bd2f9278720322` | 0 |
| src.ts/abi/coders/number.ts | 1867 | `92f16840d05221f67ee2b0d0b8c74dbd94d19b01a8404943b729f0b99cf16af6` | 0 |
| src.ts/abi/coders/string.ts | 671 | `f9850e8c709746834c4262fceab261a3605ff5644aa7f4e9a2c952de903755dd` | 0 |
| src.ts/abi/coders/tuple.ts | 2055 | `828d9ed3a1f3b0995d846ea2212dc64a247b7f90d59e2871b06909e75b8bb826` | 0 |
| src.ts/abi/fragments.ts | 52736 | `7b9ff1d7a5c298cb3af35deacd8ce1fbd7ea56e22344d5282da2a5999a12f169` | 0 |
| src.ts/abi/index.ts | 1044 | `d1964ee0a7e0c371fcca67d52b882c241dad9a0b097d552d18f17560514f7f86` | 0 |
| src.ts/abi/interface.ts | 45084 | `37671349325ca097215f854b0d0e6c72c9b9b1452a6654f0e02649693a996166` | 0 |
| src.ts/abi/typed.ts | 20503 | `ed7666beef4d18710e700cd95eb90db58bd695e7c05f277a0bbe371073367a6c` | 0 |
| src.ts/address/address.ts | 5911 | `b42cd79b915501f4099aab27714980f8ee4d571a93747ac371f30aef9fbadfe0` | 0 |
| src.ts/address/checks.ts | 3850 | `f6ed6ce79b150ffe5a286cca7981ad09730aec8beb5a6395e71459f1c55e63b5` | 0 |
| src.ts/address/contract-address.ts | 2692 | `45e0e704fd4a9a351d84c9ab9316729e00a32d02e0cd3bbdfc66b7f985a7b4a4` | 0 |
| src.ts/address/index.ts | 1699 | `f61b18f35d3da7dfb6d4abaca2f891cc91809c1a9bfdf0941eb7de4de5eadd19` | 0 |
| src.ts/constants/addresses.ts | 195 | `7a9adb525a213fb4b7b3881fefa39d998578312af6365f4041f6a8278309dc50` | 0 |
| src.ts/constants/hashes.ts | 236 | `15d680ea1fe166943d0df1c5c49a8ab3344fce06cf0b4a4fcfcbf6ce5df7fbc0` | 0 |
| src.ts/constants/index.ts | 364 | `b13174181943f1f5ca3b1fe61739e7e7101dd653010f2f02e2c6b2ebe0267eb2` | 0 |
| src.ts/constants/numbers.ts | 1243 | `41c6e5cf05fb0673df835c84884691c27d910b70155abb50a21c26b7665d88e2` | 0 |
| src.ts/constants/strings.ts | 417 | `e92417288d44a8233856a69e9e60fe8c1d1d749e5e76a18c232de22660bee0b6` | 0 |
| src.ts/contract/contract.ts | 40283 | `7f086d346cd53f8eb65a7a775e08dc161677d5bf482db8803341f4c6e6b7de05` | 0 |
| src.ts/contract/factory.ts | 5172 | `71e6615896d97271102c5fa35fe1fed5cb4d0e29e9b8895bedce4c423d319eec` | 0 |
| src.ts/contract/index.ts | 990 | `b54974f79515d7dd0ab06a4265c2e26f252f8a72d93acf3ffd5669a68ba2a88b` | 0 |
| src.ts/contract/types.ts | 7146 | `304d4c7e82fb6356cb967f4eadf8143d5b369f7630ad42c186c8c19cd3dac044` | 0 |
| src.ts/contract/wrappers.ts | 6235 | `688aa5b29d084c436a4dd1fc2ede924c91b669b52b6c304814162ed61abe866f` | 0 |
| src.ts/crypto/crypto-browser.ts | 2085 | `d49c260c571595f4ed90defabc465f1a0379afe512c78c5bb2fc743d38b94a19` | 0 |
| src.ts/crypto/crypto.ts | 79 | `4ac38b67ac5423044f99de2792dc8d3643fc8ba55acf1f28688ae3f29b59c8e5` | 0 |
| src.ts/crypto/hmac.ts | 1564 | `813536b3e56d953812a0d4bcae23f7534d8d9ddebdc6c8e2af90025f9de59695` | 0 |
| src.ts/crypto/index.ts | 1303 | `aa1587f72f7c3e9cb301ba6f56aa1177e8d6eccd5d6c54978d5a1ae6af1236a0` | 0 |
| src.ts/crypto/keccak.ts | 1410 | `c59000f10364fed26aa3841ce1952118fae01c2d43921c2421d20b6bee6a834e` | 0 |
| src.ts/crypto/pbkdf2.ts | 1952 | `03f3a04582808c232afb61e300bbb10ef24be1af6fbbbf60b11d8c9a81798454` | 0 |
| src.ts/crypto/random.ts | 1055 | `8371570d71a111b70a06a2e8dccaf567a4a44cfe910076424014c099724fdf71` | 0 |
| src.ts/crypto/ripemd160.ts | 1079 | `f082a045a1b5770f4be430bd99f938ce87287feae1aff7619b3415df00df32de` | 0 |
| src.ts/crypto/scrypt.ts | 4927 | `2906af8a25f39f52b12b4a1bd2306471c5f6ccf570b7ece88499257e6809dce2` | 0 |
| src.ts/crypto/sha2.ts | 1907 | `2fb491cac36ab4df24d24c5a3ff6a3803497c74c50c20bcbda2cacb339670095` | 0 |
| src.ts/crypto/signature.ts | 12147 | `c8f22c2c54fb60b7cca1f68d6451a3d87dfaf6e12c27199ccbc95f6b1ee466b6` | 0 |
| src.ts/crypto/signing-key.ts | 6526 | `d83ef2ab9b1a46b0559c9499189e3778f70c5e9a5dc984e3e65b640a8e66e08d` | 0 |
| src.ts/ethers.ts | 6612 | `e620f25db763d512d41cd966ccfe1d76725963f16d159071c6cec376ca2108fd` | 0 |
| src.ts/hash/authorization.ts | 1337 | `eb2f57d4819cc92eb43b3b19a4242abf9c37a96446d119344d4f13115a067c8d` | 0 |
| src.ts/hash/id.ts | 447 | `c2970f4342486b09f407ee4a5b4fa7fadf402d0b5eef28cee298f0c5f0a92a71` | 0 |
| src.ts/hash/index.ts | 734 | `094e558f61108bf658914b2fef3645d632ba39acc1267011c78ca0462857db9d` | 0 |
| src.ts/hash/message.ts | 1676 | `9c98390efb5e621634fa12830a9087c7f5c3b4b0ffa8b5b15b297158c3910a58` | 0 |
| src.ts/hash/namehash.ts | 2902 | `24f487715733398295b022ddee22f89867afdcd1a7d2481d55d5f56c3669fa14` | 0 |
| src.ts/hash/solidity.ts | 4002 | `9b310f4d710e2b302ddab00f5b39b2be022cb481f6c1912bcea9e91789346c45` | 0 |
| src.ts/hash/typed-data.ts | 22963 | `03e28366d8a2e950bff5ad07ee42d72de2148270b9105cca3782e49b956fae48` | 0 |
| src.ts/index.ts | 319 | `704747bf1f7f0e9db3d240c701101e53194321d7139ce4d477d525f072bff1f3` | 0 |
| src.ts/providers/abstract-provider.ts | 60790 | `de899863a1e4c1f72024b6b0515e9c5d71532d36658e4694ee0fe1c63a60435d` | 0 |
| src.ts/providers/abstract-signer.ts | 11686 | `b1e571c47aafc687011a98916422f327ab141dc0eacd5e98f84e6290bbe26885` | 0 |
| src.ts/providers/community.ts | 1873 | `274c294244a60ce347620a36d7a6929232fc1ffbf9c9acd678e122d882ddeca9` | 0 |
| src.ts/providers/contracts.ts | 1222 | `ad14ba10b15b6283b93692e46dde07e8672d42443c66d55b7f0c967d07730616` | 0 |
| src.ts/providers/default-provider.ts | 7319 | `01500d3ba7ad5d41d84ec08adbf0706b536d584de73e02eff8a657065c8064ee` | 0 |
| src.ts/providers/ens-resolver.ts | 26559 | `4951b990a917ca7dbb56d57d45040df41bc44c67976d1b5870f2324dd71ba64a` | 0 |
| src.ts/providers/format.ts | 9982 | `5e59ccb0bd6ac4fc82e9a4313cd098d5703044ab8f3f04f01fcc8b064d220702` | 0 |
| src.ts/providers/formatting.ts | 9151 | `025a6b212277a5e5e91b559cd1e08a35a1e77b2b4bbbb9d017a65364b7a9aa9f` | 0 |
| src.ts/providers/index.ts | 3837 | `da36e9a08fadc6ebcb9a51b2b186ce38b95f7dd110db444b3eb61cc7d7ea8c57` | 0 |
| src.ts/providers/network.ts | 14875 | `bf3895603cbe7a538c9fc721960bf3d42081c328235c42e1e465e0a47a355920` | 0 |
| src.ts/providers/pagination.ts | 218 | `52493d1265c4bd004c088664ba45e07cbb7333920fdf6002de12bfe4492fba69` | 0 |
| src.ts/providers/plugin-fallback.ts | 1163 | `6025353b441a0097cea309496f2781cd7136e869782410174a4f11c84a4aeeec` | 0 |
| src.ts/providers/plugins-network.ts | 9577 | `6da2913640be78a63655cb02bdbb8fe6c68bf479a9a1ef22c114f682ecd84562` | 0 |
| src.ts/providers/provider-alchemy.ts | 5709 | `63566373b00ad2a6db77ec535d17213c0a54171b5803a4953a8bae5dceeba306` | 1 |
| src.ts/providers/provider-ankr.ts | 5141 | `086d3de0dc4b23e7ba9965b5bf7b6eaf2716436c72d383eb80bb969ef0fdfc3b` | 1 |
| src.ts/providers/provider-blockscout.ts | 5792 | `2579502cf883ec8420ca94ba4ed7fcf213afa3a10eff085d3da2be5949c378a7` | 1 |
| src.ts/providers/provider-browser.ts | 10932 | `f2f734a9080fd4ae91c280f8778d9dde1ed9aea24bb12300ad593bed7cb6e17f` | 0 |
| src.ts/providers/provider-chainstack.ts | 3658 | `aba251e2c319cd1d3b33530f5a72b696d2c0fcda32dd2dc1ec330abe96c77c06` | 0 |
| src.ts/providers/provider-cloudflare.ts | 734 | `a69ade671bbf5fc9e630db8ac324eeb99f6f713ccddc7656c625cbb7da462abf` | 0 |
| src.ts/providers/provider-etherscan.ts | 24922 | `c711ae1cff89bdc13077cf7fc2166ad70f2a6b001f338ab8f9850138e10b53b8` | 0 |
| src.ts/providers/provider-fallback.ts | 27199 | `61abbc69cf32cf0f4c01250ff3f0d3e6392bad3a04b06460a17ff47ff4264c47` | 0 |
| src.ts/providers/provider-infura.ts | 7530 | `526a978f8b0050cb1e0db62aac435fe3714d3521b9d55bfb2cf1a8bfb92bc6d7` | 0 |
| src.ts/providers/provider-ipcsocket-browser.ts | 68 | `6e5e7833b1c829bece2dde95504b19c0a4925746494bb09a6b656498d6e65419` | 0 |
| src.ts/providers/provider-ipcsocket.ts | 2369 | `2f88a93fe01b9feac5cb8f2163cb671e1ec5dcabd4e0eac4269728a49afadd12` | 0 |
| src.ts/providers/provider-jsonrpc.ts | 46740 | `d212e68c7fbfcde7218f542127bbab771462e33f222fced521bd9c19228dd931` | 0 |
| src.ts/providers/provider-pocket.ts | 3930 | `d4f7c344ecc56c2cb8ab5a8257fcc30a55d6d7a8a19c0cdf52285a91239f2d78` | 0 |
| src.ts/providers/provider-quicknode.ts | 5901 | `709cbf715653033db398e50a1b781d55410e13fcd51e71939f20f95a7c4c0289` | 1 |
| src.ts/providers/provider-socket.ts | 11481 | `8803394d6d91051b9dbf3054346f58f7cd0641004401e8b04547a614ead99785` | 0 |
| src.ts/providers/provider-websocket.ts | 3250 | `24d8d28f813d04defbca4528a79d49cff50c00a2527dd338c192882588b57055` | 0 |
| src.ts/providers/provider.ts | 66080 | `ac6c318e0f889ec4593e9183483115fc48e23846830d4d3596a274fe7f04d2b3` | 0 |
| src.ts/providers/signer-noncemanager.ts | 2855 | `a4e7a06e2684880522114018f8bd299404b5f55214008b4624dfb9c75e75b965` | 0 |
| src.ts/providers/signer.ts | 6378 | `7a5c4c210046d34becfb9d9682938916661028d22dd6c4e8826a32e2d8d7460e` | 0 |
| src.ts/providers/subscriber-connection.ts | 1853 | `463fbfc32639bb8bdaf1a5979059a2c91dc415b9670b9a1dacd4915190aad14e` | 0 |
| src.ts/providers/subscriber-filterid.ts | 6098 | `ba63a74456f21dace16311533c69739ce52cf182197b5365d891c12fb2569291` | 0 |
| src.ts/providers/subscriber-polling.ts | 9206 | `f4df8149b409745fc546afc2a5af43e8dd0eb351e7642ebf1763c6eeff5cb0da` | 0 |
| src.ts/providers/ws-browser.ts | 329 | `359bed16e83cf5a4d6c706e4fe8817a5c52d7897f52582bee65c414365cb2a68` | 0 |
| src.ts/providers/ws.ts | 34 | `0a1e622075c44130e2ddde94c9271c9dbbd6ccad09c96caae91635d3223fa890` | 0 |
| src.ts/thirdparty.d.ts | 390 | `35165dc7529896dc2589f7d5c7ab5d6ff98171a3c8caee792d24b50381adf486` | 0 |
| src.ts/transaction/accesslist.ts | 1860 | `852517a563118e5d2f573662e80473b1d9dce33de433213828aab85eb5029852` | 0 |
| src.ts/transaction/address.ts | 951 | `4b911e5ed13e1f66c9d97e2b75170f5db051f8ab10a146e780d77c0592450795` | 0 |
| src.ts/transaction/authorization.ts | 538 | `e23328725974007028b941444224c4382fd47a4708cc93436ab9897d6d5aaa0f` | 0 |
| src.ts/transaction/index.ts | 1369 | `fd825471f40fd8000c5711f3ef327814daedfecd3147c0d2a5e3b9111bfbeb8c` | 0 |
| src.ts/transaction/transaction.ts | 52912 | `189c18d4e6a3138b47e516ee9ed4f381308094a9b3380a64d55cfcc50d182cdd` | 0 |
| src.ts/utils/base58.ts | 2018 | `2507f70a51362e95e3d68291dd1cbd784158dea97b95a744b153add0be136c90` | 0 |
| src.ts/utils/base64-browser.ts | 622 | `cfb1596219badc045128cd7df314d5674cb917cf5c77d1e3398a77a46613156d` | 0 |
| src.ts/utils/base64.ts | 1518 | `c8878c88bc64f86c9efcc9aa7cc96ba5c34aebc7e140137aa39ac653b30bbc91` | 0 |
| src.ts/utils/data.ts | 5860 | `670842b1821e80b278c40b6b09f79a23ca9385713827c159cc77200486dc5700` | 0 |
| src.ts/utils/errors.ts | 21924 | `61abb0c70c36cb264ce5ddd05f4f2cd74f2d5f4dbb5d54f73da121ada6dc7b75` | 0 |
| src.ts/utils/events.ts | 2810 | `d0d011ffb708b87e3880568bdcaa59adfe55aad1bc9633c8c5cfb56b69656a28` | 0 |
| src.ts/utils/fetch.ts | 32054 | `057cbc0dc970d831ba0f1fc2ecb04dcb4bbb8af7535d87868872b7a81a163e29` | 0 |
| src.ts/utils/fixednumber.ts | 22062 | `fe0f8223fd3652d227ebf0991c86a97c36eea3d4a2188ef27f942f56f40244de` | 0 |
| src.ts/utils/geturl-browser.ts | 2584 | `17f602abed5701f875917a5bb943f33643d40ab532f2219a64de128267e67568` | 0 |
| src.ts/utils/geturl.ts | 4909 | `57e30a6e1bd61b825adf76b64d70a45a319e529b9f353358507917c6bfdacd7e` | 0 |
| src.ts/utils/index.ts | 2667 | `57d49126aa35a4e26dd7816fc95e2788420cbebddd93c597e7f2ad81b9ff0dfc` | 0 |
| src.ts/utils/maths.ts | 8114 | `517c55ea8b79c8b660fca276445bda8a7ffeb86ee09f481ffa5bdb0214fcb193` | 0 |
| src.ts/utils/properties.ts | 1728 | `1497204c844dfad7da24759e2048b72c1307c3b4edace4a840dfb55e8d9446cf` | 0 |
| src.ts/utils/rlp-decode.ts | 3427 | `a4eea776f78605af1e838e898fad99b33e66ea6048fd59a2a22540962f45aab2` | 0 |
| src.ts/utils/rlp-encode.ts | 1604 | `e149702062da002c41dec6a0a29380af66fda1077152840c122d2754646059f8` | 0 |
| src.ts/utils/rlp.ts | 542 | `23074e61f02eeeb4e74b4dec3741d86adceecf77000973328413270ab0aada1b` | 0 |
| src.ts/utils/units.ts | 3002 | `c101ad4e110137a74a821764ca3d5883868b786b98a49d990881de90a8edbb93` | 0 |
| src.ts/utils/utf8.ts | 10752 | `2b9b5b4265b1d8bad4327ba700bf76eb2b0fcb3a3a7d89cd27961e9b2c9ca6e1` | 0 |
| src.ts/utils/uuid.ts | 927 | `91e14f985e603fa0c1b4d94cf1fc19b9823d4daf556820506a1b4bb5a0bad6b7` | 0 |
| src.ts/wallet/base-wallet.ts | 5564 | `f1ca6a6ea4d82c31a74ef44270b717585a71e4056b70c4464bc5efb0ee9589a0` | 0 |
| src.ts/wallet/hdwallet.ts | 20267 | `16d2f0edfca9540fd9e3793ebccae8628bfd422478f2c8f21ce444f8b6cdfb71` | 0 |
| src.ts/wallet/index.ts | 1347 | `6fa58fe87a39349ea2085afca3a0b00be28baaf6e5e6fd1dea568d9e7f884896` | 0 |
| src.ts/wallet/json-crowdsale.ts | 2283 | `cddf9bfbe1aeb75e394d3023bd14529e7c63860d24ecc3ba0ebb31ac0e78683f` | 0 |
| src.ts/wallet/json-keystore.ts | 14389 | `14fb4c34519fadb8e00c0f24cd860a65175226c071add73f2819af60a8caffad` | 0 |
| src.ts/wallet/mnemonic.ts | 6805 | `acbccb31d9d9678edec623909ae9226c27a0602293167f4e0196eb9aacafdcac` | 0 |
| src.ts/wallet/utils.ts | 4108 | `6e0a058598687f9710408df72040da5f089b37ebf88bd12eeacd1b02cf7ffce2` | 0 |
| src.ts/wallet/wallet.ts | 6209 | `64c4bd6eabc23912d2a59bb72e312f1e4279a1d81993fc6ba4d4e36d6e2650fe` | 0 |
| src.ts/wordlists/bit-reader.ts | 1015 | `de0adf8f17f08566bef6551c1151c31f08a8cc021941762b8233c348a88ea216` | 0 |
| src.ts/wordlists/decode-owl.ts | 1706 | `1d4dfa818e8321eca0e5318093b45011ed72d3b733f47e5e6c9a0d1fb01afd54` | 0 |
| src.ts/wordlists/decode-owla.ts | 1055 | `06795a8c2592cc27b3cca59a463c2673708ef428ac658779f3ea258ed4536b92` | 0 |
| src.ts/wordlists/generation/encode-latin.ts | 12237 | `ae10babeaa9a236add6ad89d29b6ab37adcda8fe6a1a8e951155d5987313a51a` | 0 |
| src.ts/wordlists/index.ts | 1010 | `731b3f2b3bbae5179ba1c6658d2c3440118c44ec23120c9be626a678a9c75367` | 0 |
| src.ts/wordlists/lang-cz.ts | 7987 | `38d0fc970f3e7742efbbc61b055cded7d69b8fde022b6b4d006381a50cff51d3` | 0 |
| src.ts/wordlists/lang-en.ts | 6866 | `403a827870a4cdef07a0b566f62e772a4d7a937562e64698d0ff7259f6565f28` | 0 |
| src.ts/wordlists/lang-es.ts | 7131 | `5c230c2ad033b54a4d41da8e56cc7c19a344ec76c258e329a5a1473ba33ddab0` | 0 |
| src.ts/wordlists/lang-fr.ts | 8881 | `aafd0c979acf9b5256c7c75ab09235896b8fc3a40915a101bf07256786fe366d` | 0 |
| src.ts/wordlists/lang-it.ts | 8517 | `30a3c9afa7b2a97b286ae49c71be56bc6052719a4d71a62ca91602c4ed123a8e` | 0 |
| src.ts/wordlists/lang-ja.ts | 12986 | `a081149423349cb436ff06a23f7e0702681522ee85a16f4fcff2c44ce61e4128` | 0 |
| src.ts/wordlists/lang-ko.ts | 14440 | `35fbec9fcdfe15145eaa0980c868b960f3c568ed198d4028cbc113ec24e8d8e4` | 0 |
| src.ts/wordlists/lang-pt.ts | 8357 | `21cf14378300655859f18e09f5f19e164a456ba1c369602ce4d0116ead05abcf` | 0 |
| src.ts/wordlists/lang-zh.ts | 11036 | `30149426ae5818ebcca73b0000d1c76574c2767a5a2a7711e8fc10cf06d357c2` | 0 |
| src.ts/wordlists/wordlist-owl.ts | 2258 | `69b84f312e683d6442a96b8be084e4812bda6111586914e631cfd71dcd95ac46` | 0 |
| src.ts/wordlists/wordlist-owla.ts | 1152 | `be1fccfea53691911c9474d7e1ac15f0360355bd8e8095c9cceb5043b5f19481` | 0 |
| src.ts/wordlists/wordlist.ts | 1822 | `1fcf00ef5f2fcaa024b345ea2bbe5af7e4446d4a76aa4cd74a3299f1123e42c2` | 0 |
| src.ts/wordlists/wordlists-browser.ts | 170 | `ffe5b850ba12b2bff7d00da5891570e6f42d0f9bce7435351bae69977e4b40cc` | 0 |
| src.ts/wordlists/wordlists-extra.ts | 313 | `6d8e823f74a835555d379b401cafcf8857cc204b246d71cc96324a1d008ea186` | 0 |
| src.ts/wordlists/wordlists.ts | 1235 | `4772d7e3d1b652826b94121e0bd65ebb8b5776dc8e48cceb8675fddfb306731c` | 0 |
