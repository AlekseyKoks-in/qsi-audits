# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** embit @ 2b375a33bd89 · embit (SeedSigner, Krux) — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-29 21:10 UTC |
| Версия отчёта | 1 |
| Запуск аудита | d450d12b-59fc-47df-8956-1fafe44953b0 (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `e9746bf4b6b267bdcfac6f8386056330806949cdbd324b7328f3887daf254733` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **0**
- Средняя: **4**
- Низкая: **0**
- Информационная: **1**

- Подтверждённая техническая уязвимость: 0
- Известная уязвимая версия компонента: 0
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 4
- Рекомендация по улучшению: 1
- Недостаточность данных: 0

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

Проверка аналитика: подтверждено — 4, не применимо — 1, отклонено как ложные срабатывания — 1.

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/diybitcoinhardware/embit> @ `2b375a33bd8926caec7e53d7cfd41b165d196566` — ссылки в доказательствах открывают строки на этом коммите.

142 файлов, всего 1402338 байт, редактирований: 0; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| tls_key_exchange_groups | Недостаточность данных | 56 | poetry.lock line 9: not in the algorithm registry, not assessed: ["main"]; poetry.lock line 25: not in the algorithm registry, not assessed: ["main"]; poetry.lock line 46: not in the algorithm registry, not assessed: ["main"] |
| tls_configuration | проверено | 2 | poetry.lock: openssl TLS directives parsed; src/embit/slip39.py: openssl TLS directives parsed |
| dependencies | проверено | 2 | poetry.lock: 55 dependencies parsed (55 pinned); pyproject.toml: 0 dependencies parsed (0 pinned) |
| source_code | проверено | 140 | secp256k1/config/libsecp256k1-config.h: 44 lines scanned with 16 rule patterns and 123 registry patterns; setup.py: 3 lines scanned with 16 rule patterns and 123 registry patterns; src/embit/__init__.py: 0 lines scanned with 16 rule patterns and 123 registry patterns |
| osv_advisories | проверено | 1 | 55 pinned packages queried at OSV.dev; 8 affected (8 of them only in development or build dependencies) |
| osv_advisories | Недостаточность данных | 1 | PyPI/virtualenv@21.2.0: 23 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- tls_key_exchange_groups — Недостаточность данных: 56 (примеры: poetry.lock line 9: not in the algorithm registry, not assessed: ["main"]; poetry.lock line 25: not in the algorithm registry, not assessed: ["main"]; poetry.lock line 46: not in the algorithm registry, not assessed: ["main"])
- osv_advisories — Недостаточность данных: 1 (примеры: PyPI/virtualenv@21.2.0: 23 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest)

## 5. Краткое описание архитектуры

Static review of the source tree embit at 2b375a33bd8926caec7e53d7cfd41b165d196566. 142 files analysed; of 302 files, 71 are test, fuzzing, benchmark or example code and were left out, 89 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .github/CODEOWNERS, .github/codeql/codeql-config.yml, .github/dependency-review-reviewed-purls.txt, .github/scripts/require-reviewed-dependencies.sh, .github/workflows/ci.yml. 63 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. 85 files come from directories a .gitmodules pins and are read as shipped source rather than skipped as a dependency cache: secp256k1/secp256k1-zkp (85). No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **100** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 71.4%

## 7. Подробное описание находок

### QSI-2026-06939 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (31 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-29): подтверждено аналитиком.** Verified against source at 2b375a33bd89. src/embit/ec.py wraps the implementation directly: line 18 serialises with secp256k1.ecdsa_signature_serialize_der and line 24 parses with ecdsa_signature_parse_der, over the pinned secp256k1/secp256k1-zkp submodule. This is the signing path two hardware wallets actually reach: SeedSigner through embit==0.8.0, pinned with a sha256 hash lock in its requirements.txt, and Krux through the vendor/embit submodule. A CRQC recovers the private key from a public key already on chain, so the exposure is retroactive for any reused or already-spent address. One correction to the finding's own exemplar: contrib/lax_der_parsing.c:11 is a permissive DER parsing helper, not the signing core, and a reader checking that line first will underrate the finding. src/embit/ec.py:18 and :24 are the lines to read.
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: src/embit/bip32.py
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:10 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

277 упоминаний ECDSA в 31 файл(ах), например src/embit/bip32.py:3. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/embit/bip32.py:3 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/embit/bip32.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/bip32.py#L3) · line 3 · SHA-256 a8b42d09eb77c177154252c5f274438dfbbcfc53100766c04a7cd71d251931dc_

```
    2 | from .base import EmbitKey, EmbitError
    3 | from .misc import copy, const, secp256k1
    4 | from .networks import NETWORKS
```

_file_excerpt · [src/embit/bip32.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/bip32.py#L206) · line 206 · SHA-256 bfbf28b2b5b8980de70b75cc83b4a01fcdc39deb07a1381f571ed93b9cb7ba69_

```
  205 |         if self.is_private:
  206 |             secret = [REDACTED] self.key.serialize())
  207 |             key = ec.PrivateKey(secret)
```

_file_excerpt · [src/embit/bip32.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/bip32.py#L211) · line 211 · SHA-256 f257453c600d4d5996d932210ea616c21fbe2a6f6c7605004e30af206c8413ea_

```
  210 |             point = copy(self.key._point)
  211 |             point = secp256k1.ec_pubkey_add(point, secret)
  212 |             key = ec.PublicKey(point)
```

_file_excerpt · [src/embit/liquid/descriptor.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/liquid/descriptor.py#L10) · line 10 · SHA-256 9e6fc96fc45bcab56439aca852a15109ab99d8319277e462ed8941438d9c9242_

```
    9 | from ..hashes import tagged_hash, sha256
   10 | from ..misc import secp256k1
   11 | 
```

_file_excerpt · [src/embit/liquid/descriptor.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/liquid/descriptor.py#L134) · line 134 · SHA-256 b98ba9d78c484f41b83d4bdec5e96cd09c6832dbf69f419e1d7f94c5892b0103_

```
  133 |         if self.key.is_private:
  134 |             secret = [REDACTED] tweak)
  135 |             # negate if it's odd
```

_file_excerpt · [src/embit/liquid/descriptor.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/liquid/descriptor.py#L137) · line 137 · SHA-256 e58f68c5cca5a26f8189e094ced217234b3a26e975e5a15362f18573d4ef26fb_

```
  136 |             if ec.PrivateKey(secret).sec()[0] == 0x03:
  137 |                 secp256k1.ec_privkey_negate(secret)
  138 |             return ec.PrivateKey(secret)
```

_file_excerpt · [src/embit/liquid/pset.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/liquid/pset.py#L4) · line 4 · SHA-256 be76bf3231c4ad587fec64719a03d297d6dc8dfc1361fc6c31881889e1935519_

```
    3 | if sys.implementation.name == "micropython":
    4 |     import secp256k1
    5 | else:
```

_file_excerpt · [src/embit/liquid/pset.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/liquid/pset.py#L6) · line 6 · SHA-256 5409347930b60473b6df5803ef84dc9f039c5518a2506f2ee17591ca15c03c12_

```
    5 | else:
    6 |     from ..util import secp256k1
    7 | 
```

_file_excerpt · [src/embit/liquid/pset.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/liquid/pset.py#L98) · line 98 · SHA-256 e5f7879369e8a16d51d09dc01e03454623a0fbcda076eb350c1723ffbbed1e6a_

```
   97 |         # verify
   98 |         gen = secp256k1.generator_generate_blinded(asset, in_abf)
   99 |         if gen != secp256k1.generator_parse(self.utxo.asset):
```

_file_excerpt · [src/embit/liquid/transaction.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/liquid/transaction.py#L11) · line 11 · SHA-256 94c58e8f3830aad313664c73e1bd27aaad1d5dbfa17da0fb6df8cad31b4ebb5e_

```
   10 | if sys.implementation.name == "micropython":
   11 |     import secp256k1
   12 | else:
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06941 — Квантово-уязвимый Pedersen commitment: пороговая подпись и протоколы MPC (4 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-29): подтверждено аналитиком.** The primitive is present and quantum-relevant, but both the role and the stated consequence are wrong and are corrected here. src/embit/liquid/pset.py:101 and :300 call secp256k1.pedersen_commit over value blinding factors: this is Liquid confidential transactions, not threshold signing and not MPC. And the consequence is the opposite way round from the finding's text: a Pedersen commitment's HIDING property is information-theoretic, so a CRQC does not retroactively reveal blinded amounts, while its BINDING property rests on the discrete logarithm, so a CRQC can open a commitment to a different value. The risk here is forged amounts, that is inflation of a confidential asset, not loss of confidentiality. Priority should be read accordingly.
- Затронутый актив: `source-code:Pedersen commitment:threshold_mpc`
- Источник данных: src/embit/liquid/pset.py
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:10 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

15 упоминаний Pedersen commitment в 4 файл(ах), например src/embit/liquid/pset.py:101. Роль по путям, именам функций и соседнему коду: пороговая подпись и протоколы MPC. Paillier, обязательства Педерсена и доказательства на дискретном логарифме внутри пороговых ECDSA и EdDSA ломаются алгоритмом Шора; постквантовая пороговая схема — это смена протокола, а не параметра.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/embit/liquid/pset.py:101 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/embit/liquid/pset.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/liquid/pset.py#L101) · line 101 · SHA-256 b66b1e583d90306b059a9fd44ead20cf204eaa731e5f490ea219c83b49b2b806_

```
  100 |             raise PSBTError("Invalid asset commitment")
  101 |         cmt = secp256k1.pedersen_commit(vbf, value, gen)
  102 |         if cmt != secp256k1.pedersen_commitment_parse(self.utxo.value):
```

_file_excerpt · [src/embit/liquid/pset.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/liquid/pset.py#L102) · line 102 · SHA-256 06f441e13a3c4ee80a5e7bc1c367c410548b47089185765cf11a4af021382bbc_

```
  101 |         cmt = secp256k1.pedersen_commit(vbf, value, gen)
  102 |         if cmt != secp256k1.pedersen_commitment_parse(self.utxo.value):
  103 |             raise PSBTError("Invalid value commitment")
```

_file_excerpt · [src/embit/liquid/pset.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/liquid/pset.py#L300) · line 300 · SHA-256 e13d6f4ff6fe3bd7adcceae1d254128bfd231d1754548bed4173819fd6551f55_

```
  299 |             if self.value_blinding_factor:
  300 |                 value_commitment = secp256k1.pedersen_commit(
  301 |                     self.value_blinding_factor, self.value, gen
```

_file_excerpt · [src/embit/liquid/transaction.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/liquid/transaction.py#L90) · line 90 · SHA-256 ffe62aaa23ace0fd2936ab3f4a57b541efac76f5ce1fdc493f53d8712547af75_

```
   89 | 
   90 |     commit = secp256k1.pedersen_commitment_parse(value_commitment)
   91 |     gen = secp256k1.generator_parse(asset_commitment)
```

_file_excerpt · [src/embit/util/ctypes_secp256k1.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/ctypes_secp256k1.py#L949) · line 949 · SHA-256 b7bf98d515fa733b6fa50b40868407081e5d056aea4aa1f8521535f39f60d5b6_

```
  948 | @locked
  949 | def pedersen_commitment_parse(inp, context=_secp.ctx):
  950 |     if len(inp) != 33:
```

_file_excerpt · [src/embit/util/ctypes_secp256k1.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/ctypes_secp256k1.py#L960) · line 960 · SHA-256 ae7600847f2badfdc520dc9b43caa54fe5c140fbc3f2618b08e27f37897e4ee4_

```
  959 | @locked
  960 | def pedersen_commitment_serialize(commit, context=_secp.ctx):
  961 |     if len(commit) != 64:
```

_file_excerpt · [src/embit/util/ctypes_secp256k1.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/ctypes_secp256k1.py#L971) · line 971 · SHA-256 d061be5d1ea86ffb8675c67e3f0d729a08048a4c9b7bd6c3790b187b4d3ede29_

```
  970 | @locked
  971 | def pedersen_commit(vbf, value, gen, context=_secp.ctx):
  972 |     if len(gen) != 64:
```

_file_excerpt · [src/embit/util/secp256k1.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/secp256k1.py#L51) · line 51 · SHA-256 4485c26fa3e644b515ed1a6abf59b2d50f2bc77722ad56b84c581a20e445d203_

```
   50 |             "generator_serialize": "secp256k1_generator_serialize",
   51 |             "pedersen_commitment_parse": "secp256k1_pedersen_commitment_parse",
   52 |             "pedersen_commitment_serialize": "secp256k1_pedersen_commitment_serialize",
```

_file_excerpt · [src/embit/util/secp256k1.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/secp256k1.py#L52) · line 52 · SHA-256 9ee2ecc76d93cb9f14a224de7eee8a4eb5a1dab003a01063faae76fc6b3515e0_

```
   51 |             "pedersen_commitment_parse": "secp256k1_pedersen_commitment_parse",
   52 |             "pedersen_commitment_serialize": "secp256k1_pedersen_commitment_serialize",
   53 |             "pedersen_commit": "secp256k1_pedersen_commit",
```

_file_excerpt · [src/embit/util/secp256k1.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/secp256k1.py#L53) · line 53 · SHA-256 b419e6b04ad1f224679bd93af0189ee4ac479a9d15402a9c1c3e8a73e7604079_

```
   52 |             "pedersen_commitment_serialize": "secp256k1_pedersen_commitment_serialize",
   53 |             "pedersen_commit": "secp256k1_pedersen_commit",
   54 |             "pedersen_blind_generator_blind_sum": (
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06943 — Квантово-уязвимый Schnorr (BIP-340): подпись транзакций и сообщений (6 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-29): подтверждено аналитиком.** Verified. include/secp256k1_schnorrsig.h:82 is secp256k1_schnorrsig_sign and :100 is secp256k1_schnorrsig_verify, so taproot signing is present and reachable from embit. BIP-340 rests on the same discrete-log hardness as ECDSA: it fixed malleability and enabled aggregation, not quantum resistance, so these rows are exposed exactly as the ECDSA ones are. Counted with a caveat recorded against the scanner rather than against the project: one of the cited files, src/bench_schnorrsig.c, is a benchmark, and benchmark files inside a pinned submodule were not excluded by the test-and-example filter even though the report claims they were. 12 of this audit's 89 inventory rows come from bench_*.c files in secp256k1-zkp. That is an over-count on my side, the mirror image of the submodule under-reads this project has already fixed, and it is being fixed in the runner rather than papered over here.
- Затронутый актив: `source-code:Schnorr (BIP-340):transaction_signing`
- Источник данных: src/embit/util/ctypes_secp256k1.py
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:10 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

19 упоминаний Schnorr (BIP-340) в 6 файл(ах), например src/embit/util/ctypes_secp256k1.py:287. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/embit/util/ctypes_secp256k1.py:287 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/embit/util/ctypes_secp256k1.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/ctypes_secp256k1.py#L287) · line 287 · SHA-256 57e08893e8b0d02ff62160e83bf0ee2a5297829ebdd67694ce5df8eac407d88d_

```
  286 | 
  287 |         secp256k1.secp256k1_schnorrsig_verify.argtypes = [
  288 |             c_void_p,  # ctx
```

_file_excerpt · [src/embit/util/ctypes_secp256k1.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/ctypes_secp256k1.py#L293) · line 293 · SHA-256 081fdf562b7a5fc864bee913ad182153c51fe01d652d42c0ccaec47ab8249e94_

```
  292 |         ]
  293 |         secp256k1.secp256k1_schnorrsig_verify.restype = c_int
  294 | 
```

_file_excerpt · [src/embit/util/ctypes_secp256k1.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/ctypes_secp256k1.py#L295) · line 295 · SHA-256 ca6ef88f4a54753ab4313ab865dab0bd59f732d4276c85eb8d3f4d7a3600a616_

```
  294 | 
  295 |         secp256k1.secp256k1_schnorrsig_sign.argtypes = [
  296 |             c_void_p,  # ctx
```

_file_excerpt · [src/embit/util/secp256k1.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/secp256k1.py#L33) · line 33 · SHA-256 adb579a45705e6d888d7888b09c5050db942d38a241b5a2a87bb7a936d646be3_

```
   32 |             "xonly_pubkey_from_pubkey": "secp256k1_xonly_pubkey_from_pubkey",
   33 |             "schnorrsig_verify": "secp256k1_schnorrsig_verify",
   34 |             "schnorrsig_sign": "secp256k1_schnorrsig_sign",
```

_file_excerpt · [src/embit/util/secp256k1.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/secp256k1.py#L34) · line 34 · SHA-256 c80e8c18be40947686a82eb0ecc11060bb83dcc69e53c236ddf22e0459b702a5_

```
   33 |             "schnorrsig_verify": "secp256k1_schnorrsig_verify",
   34 |             "schnorrsig_sign": "secp256k1_schnorrsig_sign",
   35 |             "keypair_create": "secp256k1_keypair_create",
```

_file_excerpt · [secp256k1/secp256k1-zkp/include/secp256k1_schnorrsig.h](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/secp256k1/secp256k1-zkp/include/secp256k1_schnorrsig.h#L82) · line 82 · SHA-256 44a2365db81547948644f36130e817fe690091caa187560ab468f34585def2d5_

```
   81 |  */
   82 | SECP256K1_API int secp256k1_schnorrsig_sign(
   83 |     const secp256k1_context* ctx,
```

_file_excerpt · [secp256k1/secp256k1-zkp/include/secp256k1_schnorrsig.h](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/secp256k1/secp256k1-zkp/include/secp256k1_schnorrsig.h#L100) · line 100 · SHA-256 72dc7958413515e7228437fe19dec8a24a240083981c855296f98cdf0e8262f2_

```
   99 |  */
  100 | SECP256K1_API SECP256K1_WARN_UNUSED_RESULT int secp256k1_schnorrsig_verify(
  101 |     const secp256k1_context* ctx,
```

_file_excerpt · [secp256k1/secp256k1-zkp/src/modules/musig/example.c](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/secp256k1/secp256k1-zkp/src/modules/musig/example.c#L160) · line 160 · SHA-256 e6ab7181c8dbb6504611247b2678ae83985acb1cf70e10429645f5d869e047bd_

```
  159 |     printf("Verifying signature.....");
  160 |     if (!secp256k1_schnorrsig_verify(ctx, sig, msg, &combined_pk)) {
  161 |         printf("FAILED\n");
```

_file_excerpt · [secp256k1/secp256k1-zkp/src/modules/musig/main_impl.h](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/secp256k1/secp256k1-zkp/src/modules/musig/main_impl.h#L460) · line 460 · SHA-256 8347c1cd3e521a8ba5e1c0b465436477efc94e0749e2b6314e1928dcfbe9a321_

```
  459 | 
  460 |     secp256k1_schnorrsig_sha256_tagged(&sha);
  461 |     secp256k1_xonly_pubkey_load(ctx, &rp, &session->combined_nonce);
```

_file_excerpt · [secp256k1/secp256k1-zkp/src/modules/schnorrsig/main_impl.h](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/secp256k1/secp256k1-zkp/src/modules/schnorrsig/main_impl.h#L98) · line 98 · SHA-256 e73ca8d800b70a374cf5e3972e2d153290a93d2d12334ada5196282ceec4cede_

```
   97 |  * SHA256 to SHA256("BIP0340/challenge")||SHA256("BIP0340/challenge"). */
   98 | static void secp256k1_schnorrsig_sha256_tagged(secp256k1_sha256 *sha) {
   99 |     secp256k1_sha256_initialize(sha);
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06940 — Квантово-уязвимый ECDSA: роль не определена (4 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-29): подтверждено аналитиком.** Confirmed, with the role corrected. The finding reports "role not determined" for src/embit/ec.py, but the role is determinable from the file itself: ec.py is embit's signature and public-key class, and lines 18 and 24 serialise and parse DER ECDSA signatures for transactions. This is the same transaction-signing role as the other ECDSA finding in this audit, not an undetermined one, and the two should be read together rather than as separate exposures.
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: src/embit/ec.py
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 21:10 UTC
- Балл приоритета: 40.2 / 100
- CVSS v3.1: неприменимо

31 упоминаний ECDSA в 4 файл(ах), например src/embit/ec.py:3. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте src/embit/ec.py:3 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [src/embit/ec.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/ec.py#L3) · line 3 · SHA-256 2da5ac4f0aac6b95a77ebbf62d29881b49cb5b77b6b6b0e545c568d12aeab1d0_

```
    2 | from . import hashes
    3 | from .misc import secp256k1
    4 | from .networks import NETWORKS
```

_file_excerpt · [src/embit/ec.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/ec.py#L18) · line 18 · SHA-256 22af8149d1de86bdaa2f37e9a1ee21d18db2b64fbb9fcd55610a17ea2df854d2_

```
   17 |     def write_to(self, stream) -> int:
   18 |         return stream.write(secp256k1.ecdsa_signature_serialize_der(self._sig))
   19 | 
```

_file_excerpt · [src/embit/ec.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/ec.py#L24) · line 24 · SHA-256 91eebf765cedecb0508205d819b8bdf939b5d9534e0cb94aab17156c7e3b5641_

```
   23 |         der += stream.read(der[1])
   24 |         return cls(secp256k1.ecdsa_signature_parse_der(der))
   25 | 
```

_file_excerpt · [src/embit/misc.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/misc.py#L7) · line 7 · SHA-256 05b74d409d6158636eb6487a7526851bab9bc6f71ec1c6983c7c03cd2cc94eec_

```
    6 |     from micropython import const
    7 |     import secp256k1
    8 | else:
```

_file_excerpt · [src/embit/misc.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/misc.py#L9) · line 9 · SHA-256 ff45e726cacf161b9a430429e3241edb8cf6b0a3b38b7970dee8086c42c5c030_

```
    8 | else:
    9 |     from .util import secp256k1
   10 | 
```

_file_excerpt · [src/embit/util/__init__.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/__init__.py#L1) · line 1 · SHA-256 00860f29eecbf17fef97f8df024ac6a0e1c1e9cbbe9369e049e938eacbea33e9_

```
    1 | from . import secp256k1
    2 | 
```

_file_excerpt · [src/embit/util/key.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/key.py#L3) · line 3 · SHA-256 fb27cc95d202f1f9be5c94d5caf6544118c775bffd007789a844330fdfa96171_

```
    2 | Copy-paste from key.py in bitcoin test_framework.
    3 | This is a fallback option if the library can't do ctypes bindings to secp256k1 library.
    4 | """
```

_file_excerpt · [src/embit/util/key.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/key.py#L72) · line 72 · SHA-256 f4860ef5ca982601d75e3762c06772c2ab7ccf9a8ffdaa2358d967ebabd52c20_

```
   71 | 
   72 |     secp256k1's is defined over field of size 2**256 - 2**32 - 977, which is 3 mod 4.
   73 |     """
```

_file_excerpt · [src/embit/util/key.py](https://github.com/diybitcoinhardware/embit/blob/2b375a33bd8926caec7e53d7cfd41b165d196566/src/embit/util/key.py#L261) · line 261 · SHA-256 1471d3953d248e8889d6d17cab1582a88926e37c21d530e7fd12090d810e15b7_

```
  260 | class ECPubKey:
  261 |     """A secp256k1 public key"""
  262 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06944 — 40 бюллетеней в 8 пакет(ах) PyPI, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-29): не применимо к этому коду.** All eight packages are reached only through development and build groups in poetry.lock - black, certifi, filelock and similar - and none is imported by src/embit, which is the code that ships to SeedSigner as a wheel and to Krux as a submodule. The advisories are real for those packages and irrelevant to anyone running the library, so they are recorded and kept out of any risk figure. The dev-versus-runtime split is doing its job here.
- Затронутый актив: `dependencies:PyPI:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-29 21:10 UTC
- Балл приоритета: 18.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 40 бюллетеней (17 с оценкой high или critical) для 8 пакет(ов) PyPI, которые подтягивают только инструменты разработки или сборки (poetry.lock): например, black@26.3.1 [dev]: GHSA-cg8m-r9f2-5wm2; certifi@2026.2.25 [dev]: GHSA-6q48-6c7w-9gw2; filelock@3.25.2 [dev]: GHSA-567q-5qvw-pf92, GHSA-69hj-f68j-2879, GHSA-8mx5-7m5m-r77g, GHSA-9vhv-jxww-xfm5, GHSA-cwqr-hh33-gh44, GHSA-fq56-3cx3-fjxp, GHSA-j8f7-rjxc-mr56, GHSA-rfpc-qcw5-3pc4, GHSA-v4x8-3wr5-3wq8; idna@3.11 [dev]: GHSA-65pc-fj4g-8rjx; mkdocs-material@9.7.6 [dev]: GHSA-xvg9-69gf-fjrf. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в poetry.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (PyPI)](https://osv.dev/) · poetry.lock · SHA-256 47704e2f28f1e9b2997e7f58043e0a0637c52977b48edc36f9c64c07f445ea48_

```
black@26.3.1 [dev]: GHSA-cg8m-r9f2-5wm2
certifi@2026.2.25 [dev]: GHSA-6q48-6c7w-9gw2
filelock@3.25.2 [dev]: GHSA-567q-5qvw-pf92, GHSA-69hj-f68j-2879, GHSA-8mx5-7m5m-r77g, GHSA-9vhv-jxww-xfm5, GHSA-cwqr-hh33-gh44, GHSA-fq56-3cx3-fjxp, GHSA-j8f7-rjxc-mr56, GHSA-rfpc-qcw5-3pc4, GHSA-v4x8-3wr5-3wq8
idna@3.11 [dev]: GHSA-65pc-fj4g-8rjx
mkdocs-material@9.7.6 [dev]: GHSA-xvg9-69gf-fjrf
pymdown-extensions@10.21 [dev]: GHSA-62q4-447f-wv8h, GHSA-9xwg-3r6f-jcx2, GHSA-gm37-52c6-37mw
urllib3@2.6.3 [dev]: GHSA-8988-9cw3-xx77, GHSA-gh4c-6fx4-qh6g, GHSA-mf9v-mfxr-j63j, GHSA-qccp-gfcp-xxvc, GHSA-vxq7-64xx-v4gw
virtualenv@21.2.0 [dev]: GHSA-394h-qwmc-48pf, GHSA-43mp-35q3-x3fq, GHSA-494p-63j8-28p3, GHSA-558c-9hv2-4prj, GHSA-5vjq-rrrf-7h2q, GHSA-6w3r-xr62-4xcp, GHSA-8rjx-v5ww-45pp, GHSA-94p9-xgh2-xp45, GHSA-9h9j-4vrj-gf7g, GHSA-c947-3pg5-gm8q, GHSA-c978-59m8-c77v, GHSA-cw65-gx24-rc82, GHSA-cx28-75q4-x26q, GHSA-fc2g-4w5p-6whm, GHSA-hhxq-47xx-j5xx, GHSA-p58f-9548-mpm2, GHSA-qmx5-4p3x-wvqf, GHSA-vxj4-q4g9-crj7, GHSA-x78j-v8h9-3j2q
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### Отклонено после проверки

_Эти находки аналитик отклонил как ложные срабатывания; в подсчётах отчёта они не учитываются._

| ID | Подробное описание находок | Проверка аналитика |
|---|---|---|
| QSI-2026-06942 | Малое число итераций PBKDF2 (2500) в src/embit/slip39.py | Read the source: src/embit/slip39.py runs hashlib.pbkdf2_hmac("sha256", i + passphrase, salt + right, 2500 << exponent, half) inside a loop over four round indices. SLIP-39 specifies a base iteration count of 10000 divided across its four Feistel rounds, which is 2500 per round, scaled by two to the power of the share's exponent field. The number is mandated by the standard the file implements, not a configuration the project chose, and the effective total at exponent 0 is 10000. Flagging it would mean flagging SLIP-39 itself, which is a different argument and does not belong in this finding. |

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
| **пороговая подпись и протоколы MPC** | Pedersen commitment (4) | QSI-2026-06941 | Отслеживайте постквантовые пороговые подписи (NIST IR 8214C) и держите слой протоколов готовым к замене схемы подписи; зафиксируйте, сколько должны жить ключи и доли |
| **подпись транзакций и сообщений** | ECDSA (31), Schnorr (BIP-340) (6) | QSI-2026-06939, QSI-2026-06943 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |
| **роль не определена** | ECDSA (4) | QSI-2026-06940 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | ECDH (1), ECDSA (44), Pedersen commitment (4), Schnorr (BIP-340) (6) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | HMAC (6), PBKDF2 (3), RIPEMD-160 (3), SHA-2 (10) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | RIPEMD-160 (3), SHA-2 (10) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.
- tls_key_exchange_groups: 56 (примеры: poetry.lock line 9: not in the algorithm registry, not assessed: ["main"]; poetry.lock line 25: not in the algorithm registry, not assessed: ["main"]; poetry.lock line 46: not in the algorithm registry, not assessed: ["main"])
- osv_advisories: 1 (примеры: PyPI/virtualenv@21.2.0: 23 advisories at OSV.dev, the first 20 are listed as findings; see OSV.dev for the rest)

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
| P3 | QSI-2026-06939 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06941 | Внесите использования Pedersen commitment в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06943 | Внесите использования Schnorr (BIP-340) в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06940 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-06939 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06941 | Запланируйте миграцию Pedersen commitment на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-06943 | Запланируйте миграцию Schnorr (BIP-340) на  (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование  или гибридной схемы. |
| P4 | QSI-2026-06940 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06944 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |

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
| RIPEMD-160 | RIPEMD-160 |  | слаб классически | устаревающий | 3 | 3 | src/embit/descriptor/miniscript.py:245; src/embit/hashes.py:6; src/embit/util/py_ripemd160.py |
| HMAC |  |  | сниженный запас (Гровер), одобрен | допустимо | 6 | 6 | src/embit/bip32.py:53; src/embit/bip85.py:26; src/embit/liquid/blip32.py:11 |
| PBKDF2 |  |  | сниженный запас (Гровер), одобрен | допустимо | 2 | 2 | src/embit/bip39.py:81; src/embit/slip39.py:51 |
| PBKDF2 | 2500 iterations |  | сниженный запас (Гровер), одобрен | устаревающий | 1 | 1 | src/embit/slip39.py:51 |
| SHA-2 | SHA-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 10 | 10 | secp256k1/secp256k1-zkp/src/modules/rangeproof/main_impl.h:24; src/embit/bip39.py:57; src/embit/hashes.py:18 |
| ECDH |  |  | уязвим (Шор) | допустимо | 1 | 1 | secp256k1/secp256k1-zkp/include/secp256k1_ecdh.h |
| ECDSA |  |  | уязвим (Шор) | допустимо | 14 | 14 | secp256k1/secp256k1-zkp/contrib/lax_der_parsing.c:11; secp256k1/secp256k1-zkp/contrib/lax_der_parsing.h:88; secp256k1/secp256k1-zkp/include/secp256k1.h:85 |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 30 | 30 | secp256k1/secp256k1-zkp/contrib/lax_der_parsing.h:57; secp256k1/secp256k1-zkp/contrib/lax_der_privatekey_parsing.h:34; secp256k1/secp256k1-zkp/include/secp256k1_ecdh.h:4 |
| Pedersen commitment |  |  | уязвим (Шор) | допустимо | 4 | 4 | src/embit/liquid/pset.py:101; src/embit/liquid/transaction.py:90; src/embit/util/ctypes_secp256k1.py:949 |
| Schnorr (BIP-340) |  |  | уязвим (Шор) | допустимо | 6 | 6 | secp256k1/secp256k1-zkp/include/secp256k1_schnorrsig.h:82; secp256k1/secp256k1-zkp/src/modules/musig/example.c:160; secp256k1/secp256k1-zkp/src/modules/musig/main_impl.h:460 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| poetry.lock | 141384 | `2cb04f5c9e548a06fd72f23071379937898e90680cf8323c9ad76b732067b4c9` | 0 |
| pyproject.toml | 2272 | `13dbd4a607f5ab89d185fd59084e095ec07f61aff41ae796593140fe510f0e86` | 0 |
| secp256k1/config/libsecp256k1-config.h | 1049 | `b89383e0d2b44a0ee82a1047507425812039ba509d5ef6c670b48bac2bfc5ddc` | 0 |
| setup.py | 63 | `cac35ae0415825d9140c994aac5cf0e4178f180bf32cbc86d8be4913a00937b4` | 0 |
| src/embit/__init__.py | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| src/embit/base.py | 3472 | `7c0b75fa140abce6663fc879f811c69bc231099b962f968ed362ac1bfbe10461` | 0 |
| src/embit/base58.py | 1978 | `9166fd6cec484bf1c14a4ca1dabc05a9cff1613a35598737945da0b5dec81d5f` | 0 |
| src/embit/bech32.py | 5165 | `9ad80ea66ef64f7e2c8906175fdd5bc3ba19952fea6a356edd15cf693736ba3f` | 0 |
| src/embit/bip32.py | 10157 | `44cbc51b66db1ee9651545d899da381b11da778c5c8f63f03de03bc1075726bf` | 0 |
| src/embit/bip39.py | 4140 | `630534f8fb4a6559eb8492c124f581a8530dae40137cd53ec74047e192a83429` | 0 |
| src/embit/bip85.py | 1910 | `9ebb91c3a22f5f10de08456d83927fea9be2191bee833782c63d90c91d91310b` | 0 |
| src/embit/compact.py | 1255 | `596ccb412342104001f7779c6c2deb441674e32347d2f8c43b31bd8705d50c1c` | 0 |
| src/embit/descriptor/__init__.py | 87 | `4aa84fc0a3ed296e6dc2da33d5363444b1a5999883a0a8724caaf4acc16abe29` | 0 |
| src/embit/descriptor/arguments.py | 16154 | `c6bfb0a18831955fc2718e0657ac9cef966572abf37fc588e4d977268b73ca99` | 0 |
| src/embit/descriptor/base.py | 606 | `28f0a4f67943598e5cec7e108bb173c09dbc549828cfc4f5b448aaf5fbc9b8a1` | 0 |
| src/embit/descriptor/checksum.py | 1424 | `ce2f12172291964693395525bcff945ca2c13703e19343dc5a102765c75f8ef3` | 0 |
| src/embit/descriptor/descriptor.py | 12227 | `e5083d56f2c6aa5158b6491df835bcc706b08c911ce5e978007b6eb420246f53` | 0 |
| src/embit/descriptor/errors.py | 218 | `b168765207c4248fbe3abfca5c1117871f988452255b2d7d01db3fd73d84e589` | 0 |
| src/embit/descriptor/miniscript.py | 27644 | `7ed80636da6dc861b1ec703fbbaca4bf58acaa2f5a71b012b2881018e56cfe77` | 0 |
| src/embit/descriptor/taptree.py | 4775 | `1a5dc80eedaaf07d3de85417e320de529cf9283aadc752f8b7d5874b38dea826` | 0 |
| src/embit/ec.py | 8332 | `1c2b11a8e397a903473962ff0baa2b3de02e81c211b6df300fe828f1249a533b` | 0 |
| src/embit/finalizer.py | 3339 | `0a1b2be13e3c9e41ca7aa78ab7c5b67dc81f6571fe8e849252d25be261853520` | 0 |
| src/embit/hashes.py | 1222 | `a0fbfa6dfd9c2db718a706e20b09bbf29d0ff120d8381f2db0477f8f169b9505` | 0 |
| src/embit/liquid/__init__.py | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| src/embit/liquid/addresses.py | 3182 | `7560dad8a486ba99ef94507ce0b2598ffdcce7e3ac94f76dda7b227f18d946fa` | 0 |
| src/embit/liquid/blech32.py | 4555 | `f86db4a16f3aae7b21bccd084f228dc3b8964aecbcf314195a4aca61cc0591d6` | 0 |
| src/embit/liquid/blip32.py | 481 | `62d971910564b0174001a5bd0669733d5c8ef8459ce1b8cbe959ff0bce454437` | 0 |
| src/embit/liquid/descriptor.py | 8775 | `faeaf423b09b7889ce4e47e93cd3563358f7cfa39230af015ea4ef7a1b47bafd` | 0 |
| src/embit/liquid/finalizer.py | 2009 | `8977b650b2cfcba3222ddc8b01a1279faf5b398064168c733f5d03ac9d9c7d9f` | 0 |
| src/embit/liquid/networks.py | 2145 | `ffb9ded28c4dd810cffa57fde65f742d0c6deb5dba9ff757d92e0156aa5e814a` | 0 |
| src/embit/liquid/pset.py | 25766 | `b9bd8b713c6395282122052daeb4e95540d556abcaf40e055cb9c597d618738b` | 0 |
| src/embit/liquid/psetview.py | 9461 | `fbf0a066084aa00ef241fc42cbae11e4f698dde9d725803bd3de2a7c428656e4` | 0 |
| src/embit/liquid/slip77.py | 453 | `0e797e76b309e09b7323ee71e86e490bbbbad3695318c732308cd27561b44aeb` | 0 |
| src/embit/liquid/transaction.py | 18550 | `601e672e0ae53c08780b307a0b231215d31c8325b0fe18b97bb45a3e2892cb16` | 0 |
| src/embit/misc.py | 1820 | `fc544d7dcb476386b4a2c1b47ea6c6da553e3471d916e8b2c24ea6328769ef9d` | 0 |
| src/embit/networks.py | 2256 | `d1ba1531c9bb5fb67e838b092a2f30153a8a3b135c61c4819ab20ea1339bd94b` | 0 |
| src/embit/psbt.py | 43779 | `6fa64dd99a4486c02800d11dd95175169462a7b6c3b860069fa411029810aeff` | 0 |
| src/embit/psbtview.py | 37684 | `aa891a9294d08e2dd96ee79927f8609477a265be315c161a02895dc74145b0b5` | 0 |
| src/embit/script.py | 6460 | `5ed7e72166fc98383dd2c0f7114819b2606f46ec9381d736605e81b3c8e0bc0a` | 0 |
| src/embit/slip39.py | 13751 | `363e0dbd9282b7d6bd0e6aecaf04b58a3d86dd69df05eaaa1cf7df82870add79` | 0 |
| src/embit/transaction.py | 14648 | `a9396f1d6a8afade20a85b3ee982850d980468d7a83613c3be623f7455b00f8a` | 0 |
| src/embit/util/__init__.py | 96 | `23cccc8f03e645102b5d2722758ac955edda2a2b14b7d24eec17a28b71595c79` | 0 |
| src/embit/util/ctypes_secp256k1.py | 39495 | `76695a82303a769942a1d9edab23aaa9380af577ebae6ddf2eae04acc6b5d43b` | 0 |
| src/embit/util/key.py | 20166 | `0850b1637dafc13c7c2e0d1e4afbbcbc655890dc142da543c340ac8e494a5dd9` | 0 |
| src/embit/util/py_ripemd160.py | 5397 | `44d730f6ced0ee5d4ffaa9662420779f8797bf5ba3a1927dd11b6af2639a08d3` | 0 |
| src/embit/util/py_secp256k1.py | 13341 | `cd71a7d933635ba82eea52e9af59854ab03392e9eb866ff1072f581c3de716ba` | 0 |
| src/embit/util/secp256k1.py | 3751 | `3f0dfccabac80a6c83c0d2318582d296d0fa9cf88ab347418ba7e27af5e333c6` | 0 |
| src/embit/wordlists/__init__.py | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 0 |
| src/embit/wordlists/base.py | 897 | `c4e144c64cbc7e46e8c9e66ad625cc4e2a04f3a13d71ae2c197413973e79ace1` | 0 |
| src/embit/wordlists/bip39.py | 27467 | `c7398e797b743901822741e5a2c6010cb1ac09f7ea1bc562d6da0d8bf4d164e2` | 0 |
| src/embit/wordlists/slip39.py | 14418 | `9141a27eb0a1c62be940660318966ae9965358a5a517317ac67b75ef47e1f502` | 0 |
| src/embit/wordlists/ubip39.py | 124 | `5bb74513560d9643773b3e4c6016094414c2c6bbc7bfe97944e66dfbf27300be` | 0 |
| src/embit/wordlists/uslip39.py | 129 | `368d0994125fd8124c26b6009042dbdb153b9da011cbc6bd509df7b6cb9e4241` | 0 |
| tools/generate_release_sbom.py | 5351 | `abe044b870fa5b5b86be6eeff07e9ff1abffc969644cf9093ddc4c9f2b7f0ee9` | 0 |
| tools/package_inspect.py | 856 | `30e1e125db2ab21d39b6b93bc2f216c28eb948472aaec61f69443c33748d60fd` | 0 |
| tools/verify_github_actions_pins.py | 6600 | `79f0b6469a0c964f7699b477939a8abfc6831fa545f9d149b0b17e769c234eed` | 0 |
| tools/verify_package_artifacts.py | 12821 | `f57fa3c5279910e6d63944a55b6b40f80d12869ed85d0e4931ccb87ded2d17d6` | 0 |
| secp256k1/secp256k1-zkp/contrib/lax_der_parsing.c | 3575 | `14225148538be5587db2304dcb6ba6340b2f195352ada8de78da53ba9ca7eec1` | 0 |
| secp256k1/secp256k1-zkp/contrib/lax_der_parsing.h | 4234 | `79c479a9e6f51a5ad1e83b9efcde9df4e3431c2a3e894d37de8e9c9bc4538fb2` | 0 |
| secp256k1/secp256k1-zkp/contrib/lax_der_privatekey_parsing.c | 5096 | `53acbaf3ab72f97855a87d936bfb32e288745de9d2311da8750e9ff842f905ee` | 0 |
| secp256k1/secp256k1-zkp/contrib/lax_der_privatekey_parsing.h | 4048 | `3dcaf6d98270a20ef1455f67479191ff31747af1e66cec979b01a2be41a968f2` | 0 |
| secp256k1/secp256k1-zkp/include/secp256k1.h | 36956 | `524e48b39a62c9f54f203dca9b8a5a69946028fe7adeadeb60a81e590eb5c78a` | 0 |
| secp256k1/secp256k1-zkp/include/secp256k1_ecdh.h | 2508 | `7950343b5eea7112a491850ad20fd0862ae965f84ae0e8e74ea404cf83e6d12a` | 0 |
| secp256k1/secp256k1-zkp/include/secp256k1_ecdsa_adaptor.h | 7473 | `e2961621b8bd190b7c4426d10203876d33c2ab0c6a16adcb5f016da47fa36c70` | 0 |
| secp256k1/secp256k1-zkp/include/secp256k1_ecdsa_s2c.h | 12308 | `981e83c3d35e25dcb292b0e9d7d07fa4093173a431d87c3efb5e587a9f75c449` | 0 |
| secp256k1/secp256k1-zkp/include/secp256k1_extrakeys.h | 12104 | `d134316cf706bdbce101a8225d24c07c4d1774d4d64815fd6a8e743e0c2bba60` | 0 |
| secp256k1/secp256k1-zkp/include/secp256k1_generator.h | 3430 | `05d5b4b7b8ff0954a3bfe50025093bbf9fd1aad6ecd0886b2042c9a671efd934` | 0 |
| secp256k1/secp256k1-zkp/include/secp256k1_musig.h | 24450 | `b492db382be02ae4423f796c6f3a051d355009ea6dcc1948d50359232a30bdd5` | 0 |
| secp256k1/secp256k1-zkp/include/secp256k1_preallocated.h | 5689 | `a398cf3eeb4d8041825e8798770447efcd3118771f4f58c1477877e01555ed0d` | 0 |
| secp256k1/secp256k1-zkp/include/secp256k1_rangeproof.h | 15139 | `2a1e6b3ae4c44f3f453b1d53c996e617a4af1f38acd3b5e7635d4eb369aa0041` | 0 |
| secp256k1/secp256k1-zkp/include/secp256k1_recovery.h | 4742 | `92b8b66ad249ca92a4dd41fed8ee56cfaf34bf29f1ac12398324f87157baf1e5` | 0 |
| secp256k1/secp256k1-zkp/include/secp256k1_schnorrsig.h | 4941 | `4c06e835211e9426c0a1af5a6e7ba8a9b7a0849eb6c60adb9f9309902266b9b4` | 0 |
| secp256k1/secp256k1-zkp/include/secp256k1_surjectionproof.h | 12419 | `a7003623b033602fff8abd1dbd8084a6c0e3c0f30a3fa3e2604d36a8b9945d1b` | 0 |
| secp256k1/secp256k1-zkp/include/secp256k1_whitelist.h | 6507 | `2cb891357e7113721542c6cf61f7c32796f70a68589ef1103b691223b3f5231d` | 0 |
| secp256k1/secp256k1-zkp/src/assumptions.h | 4366 | `1a7f40ea5b62146fa1809da4799e3315743195950b494b12ce2d0c81e8c76024` | 0 |
| secp256k1/secp256k1-zkp/src/basic-config.h | 590 | `5af274e93a0de7a51f1111f356d249262b1934976d0e537c072ddbbbec2ae7b6` | 0 |
| secp256k1/secp256k1-zkp/src/eccommit.h | 2162 | `b9336fd346fcde5886597c7c8b34e0fa9769519774c093695341e1d60a7d4431` | 0 |
| secp256k1/secp256k1-zkp/src/eccommit_impl.h | 3117 | `7cb79dcac87f70f59664dd0599e6f79f1f5f5b779e1ca3e4c599d1eb16309dad` | 0 |
| secp256k1/secp256k1-zkp/src/ecdsa.h | 1201 | `812552ffa5a48b516a7dea910a15278739cf1376dbcc650ccb3d4dc29269d824` | 0 |
| secp256k1/secp256k1-zkp/src/ecdsa_impl.h | 10686 | `475d3dd3d6d4338201468465b88c08f8cf8cc7ff6c610d7cd3a03721bc01c9f7` | 0 |
| secp256k1/secp256k1-zkp/src/eckey.h | 1237 | `4638e4e797460ede9b9dd78b1306cfa17a8a9ba5828433325773722acc80ccaa` | 0 |
| secp256k1/secp256k1-zkp/src/eckey_impl.h | 3464 | `2a6e70bc9b74cd0c10236a17c1dc35a72f0dddbc33906ad945aae4a9fe364627` | 0 |
| secp256k1/secp256k1-zkp/src/ecmult.h | 2487 | `7fe6bd0b0752025015e54982125d655893c465b4e93a1f8eeaee169f3dd6756d` | 0 |
| secp256k1/secp256k1-zkp/src/ecmult_const.h | 853 | `2d4839089f63eb4993987262b9bf9455f6c2b660789ce1fadf37867bd283bfcb` | 0 |
| secp256k1/secp256k1-zkp/src/ecmult_const_impl.h | 10274 | `e9b3796ea1fdd731a9b1d80f5d9ae9d9e8784560f705ea13ad7ce47eb737f77a` | 0 |
| secp256k1/secp256k1-zkp/src/ecmult_gen.h | 2708 | `a7c4ae33d19fe563377c5eace565555fd8bb9b183c52e39072f84f6f5cabe831` | 0 |
| secp256k1/secp256k1-zkp/src/ecmult_gen_impl.h | 8857 | `e7e3d7fb0881bd5f511eea4ba90ccc8ad54c357505dedadd2100a1ab428841dc` | 0 |
| secp256k1/secp256k1-zkp/src/ecmult_impl.h | 44043 | `f4dc1435edb6dad53ab4f0f5706855db45e45a6baafd48cffef3e17952f219e7` | 0 |
| secp256k1/secp256k1-zkp/src/field.h | 6213 | `d499ca2108b4271a81896140d1490df9b825291311eeb2e99d103ced939189c6` | 0 |
| secp256k1/secp256k1-zkp/src/field_10x26.h | 1987 | `ef897ddfc9b1c3e15eb08700808222b4cfdb5c6596c7e954df1fb24fb6ebe33f` | 0 |
| secp256k1/secp256k1-zkp/src/field_10x26_impl.h | 50619 | `3cf50cb54d0f4b4db0cbeb4266a3d9333f5219203aa18449e9f9276088688930` | 0 |
| secp256k1/secp256k1-zkp/src/field_5x52.h | 2030 | `4c016d20cc779b03d46413ecfdadb4cab06bba412aa365648e48c8c4b57737c3` | 0 |
| secp256k1/secp256k1-zkp/src/field_5x52_asm_impl.h | 13167 | `c1e68e895926261022aeb7bc08eb4794231149b50a0cc79b37033cbc77cd1174` | 0 |
| secp256k1/secp256k1-zkp/src/field_5x52_impl.h | 19115 | `7cb7c821d7f63658c2310e0366e38b9f078a88220704b75a713d6103fbdedc27` | 0 |
| secp256k1/secp256k1-zkp/src/field_5x52_int128_impl.h | 9349 | `0d7f1365e76aec0af251f8e6a99cf59cc81b02e0b565a35e73ce8a4097e668ca` | 0 |
| secp256k1/secp256k1-zkp/src/field_impl.h | 4176 | `98391a3485187a4ca2af56661412f1329bc764cd131985a177cb8b6801009e4e` | 0 |
| secp256k1/secp256k1-zkp/src/gen_context.c | 3515 | `475071487ef772208fd3bee8cdce40ca536fb34c90b093f091285d87d27d88bb` | 0 |
| secp256k1/secp256k1-zkp/src/group.h | 8502 | `3c12f857092bf57c103479a5c49b4b59eedbc3bc61682bbd526d9722dd82dfff` | 0 |
| secp256k1/secp256k1-zkp/src/group_impl.h | 27300 | `cc9fdd12aa8cffb17cf96d2ac0faa1213b1a746c69afa42239bb6b46bba6834a` | 0 |
| secp256k1/secp256k1-zkp/src/hash.h | 1714 | `038dcdfcc50e4a99ecf9aabde34494f218a4e791405c233c59119bdd5b7ce756` | 0 |
| secp256k1/secp256k1-zkp/src/hash_impl.h | 13381 | `dcaccfbbf8001e28f728237e09cf2064518e66d3de848ee7697d834d5ef98251` | 0 |
| secp256k1/secp256k1-zkp/src/modinv32.h | 1590 | `547dc92e3d8d5d66748d2de4b1dc1559d33c3ce8de62ed4be5b6dbaad29c43d4` | 0 |
| secp256k1/secp256k1-zkp/src/modinv32_impl.h | 26705 | `0a74faf781c312e93b58d7f00f2b2a8a76882794b029609f52b1d1eb8d2bb095` | 0 |
| secp256k1/secp256k1-zkp/src/modinv64.h | 1694 | `d5fb8ac55ef964df7cd9d03c48b07e39bf25d6c5be01f2aefe7e5bbdb893607c` | 0 |
| secp256k1/secp256k1-zkp/src/modinv64_impl.h | 27997 | `4cd24aa3b4a59b96fe5a2be212b4ec9ac511b6bf49af7532aec529f79593ceb2` | 0 |
| secp256k1/secp256k1-zkp/src/modules/ecdh/main_impl.h | 2361 | `b88931b1b2f71adb0ef917064910601240f5a380b45defc0759b75e8e878279d` | 0 |
| secp256k1/secp256k1-zkp/src/modules/ecdsa_adaptor/dleq_impl.h | 5642 | `7d5652b63ec268bf08486b01ef0ce3de6ada5629937da1b4bfa7213b76064671` | 0 |
| secp256k1/secp256k1-zkp/src/modules/ecdsa_adaptor/main_impl.h | 14327 | `177349a8e2d98112868ebb4eb0d9a5c883a4ce09d8ef4866e78f4059bddaeec6` | 0 |
| secp256k1/secp256k1-zkp/src/modules/ecdsa_s2c/main_impl.h | 8616 | `723bdad7d125439572a67341d0bde2275ecd94f23f7bbf8c543274956ae5f22d` | 0 |
| secp256k1/secp256k1-zkp/src/modules/extrakeys/main_impl.h | 10189 | `0c88a343e58e38a909be3a62f0a7023b4231e24071d8df50ee0cd2dde2d930cd` | 0 |
| secp256k1/secp256k1-zkp/src/modules/generator/main_impl.h | 8233 | `0ad192c8973c4da4c9980a573c415c78ea54404c3fa8200839cd20e43f03f50c` | 0 |
| secp256k1/secp256k1-zkp/src/modules/musig/example.c | 6918 | `7568f0ec3778da013a98fd5e3133c2a640e3eb3f3cff59290cee43de7cdf856a` | 0 |
| secp256k1/secp256k1-zkp/src/modules/musig/main_impl.h | 26302 | `f5b1e1cb467ee05a70006c55efe00cbc54962adf5a5446f74438f0b282aa1d75` | 0 |
| secp256k1/secp256k1-zkp/src/modules/rangeproof/borromean.h | 1143 | `668ad333886c5a7db3f518cdc9acf88fc78eaad04e6d280fcb0ee58a571b94ee` | 0 |
| secp256k1/secp256k1-zkp/src/modules/rangeproof/borromean_impl.h | 7996 | `970fe56254e3e90c7bc14aff93c181ea96c35b22465a1ae15b8bc389d5174cf5` | 0 |
| secp256k1/secp256k1-zkp/src/modules/rangeproof/main_impl.h | 12799 | `6c46c3678bdc43b3f85275e27b7e05dad3c757069443068e8d56080d3f9fd8c4` | 0 |
| secp256k1/secp256k1-zkp/src/modules/rangeproof/pedersen.h | 890 | `ba1740c13e0e28450fdc7c2222b4dcb535979a632ca418ab3b7499c459f827e0` | 0 |
| secp256k1/secp256k1-zkp/src/modules/rangeproof/pedersen_impl.h | 1677 | `241097c4cd4bf909821b34e6d0da590f3409f0703f061734ea19fdfdbc67c6ae` | 0 |
| secp256k1/secp256k1-zkp/src/modules/rangeproof/rangeproof.h | 981 | `f136150e8e7347ff0bfac863581d9d0506bf1d4f528bf29750a7db4d2d4a8b54` | 0 |
| secp256k1/secp256k1-zkp/src/modules/rangeproof/rangeproof_impl.h | 25672 | `02ac85491617607e7f38e073d1f4769ddbcfd74603b460fc1598d61aff2feb51` | 0 |
| secp256k1/secp256k1-zkp/src/modules/recovery/main_impl.h | 6227 | `d130fb409ac92c96a2ec3d368998cc6de277bbdb7e11e5ab1234d8aaca17834e` | 0 |
| secp256k1/secp256k1-zkp/src/modules/schnorrsig/main_impl.h | 8187 | `eb51e55a0617e6145afed8ccdd2be86d3fc640a0a996f421a1caa5eb3f34e935` | 0 |
| secp256k1/secp256k1-zkp/src/modules/surjection/main_impl.h | 15987 | `44294734be933d3236040e7f690de0a28783ba7747a729ba4b9d3c88c141aeca` | 0 |
| secp256k1/secp256k1-zkp/src/modules/surjection/surjection.h | 1058 | `33eb9735803f1dbcb20ad42370f011f3d876e49e5d0d5998013fd644ec466fc0` | 0 |
| secp256k1/secp256k1-zkp/src/modules/surjection/surjection_impl.h | 3448 | `fa0a740afca1ef6a9bfd5776166692a885b67272bcdc46bb3b46f9555de7d574` | 0 |
| secp256k1/secp256k1-zkp/src/modules/whitelist/main_impl.h | 6489 | `7c4ddad42f296606dd12d2ae683345f300e9a3c846dfe60265ab9c0661332e69` | 0 |
| secp256k1/secp256k1-zkp/src/modules/whitelist/whitelist_impl.h | 4527 | `3a673bb954f54cf5c0a511efc6628e4e5512047b7d2580efd58e31d81df7ed62` | 0 |
| secp256k1/secp256k1-zkp/src/scalar.h | 5430 | `41f80a5baf85ef8ad70fced31d3001b6c82ccd6400835c352de8277db2eb21e1` | 0 |
| secp256k1/secp256k1-zkp/src/scalar_4x64.h | 801 | `42aed583b28bda7982c54a6f63e50c0ae5f9c27d5f66d92ec6bf6c90e765735a` | 0 |
| secp256k1/secp256k1-zkp/src/scalar_4x64_impl.h | 31469 | `0ab498d00f7f0cb2b7d5afb350e1d571425c5be56e6c124144084bfe4d41a5ac` | 0 |
| secp256k1/secp256k1-zkp/src/scalar_8x32.h | 725 | `0614cea113aea88a47ef3b2ba8167722e850d7b2a696a4f16b03ec9a320ef1d6` | 0 |
| secp256k1/secp256k1-zkp/src/scalar_8x32_impl.h | 30373 | `9cc6e80eaeb189290f07ea2aa115426b5337e8cfa96bb9d5157acc842691a328` | 0 |
| secp256k1/secp256k1-zkp/src/scalar_impl.h | 11302 | `f930431bd0739551cb40949e4816cde21880cf33c4d7c0d2e68466b00ddb9010` | 0 |
| secp256k1/secp256k1-zkp/src/scalar_low.h | 658 | `f0427de1e87d0f4e06f5dc1d23d036056afab26e809cfdec5b16e45d946be477` | 0 |
| secp256k1/secp256k1-zkp/src/scalar_low_impl.h | 5047 | `344191609736ed83d118b6343c881c94e8883fa340f6b9d9270cce4ab34e84eb` | 0 |
| secp256k1/secp256k1-zkp/src/scratch.h | 2152 | `0301e4ae76f1090462b1e798bc0b4f25359c0ee38dd3e10f06f2fd491e2ffb9e` | 0 |
| secp256k1/secp256k1-zkp/src/scratch_impl.h | 3677 | `b7ef71c35713908ea32aab65ed5a42a2be13bc7b5a0fc2115d891dce7fef9125` | 0 |
| secp256k1/secp256k1-zkp/src/secp256k1.c | 31640 | `c206ee81472c00de7c947edbb1178e22bb3bdcbff71439a0440f3d8072b6e9f1` | 0 |
| secp256k1/secp256k1-zkp/src/selftest.h | 1264 | `4deb00dd293926cc8a52aab5f59351c6fd25d72dd26c448dcc3ec6d16d370a55` | 0 |
| secp256k1/secp256k1-zkp/src/testrand.h | 2030 | `e1aab215d46d5168a2e411663cfc1f00bcdd15419d115baf8457608886957440` | 0 |
| secp256k1/secp256k1-zkp/src/testrand_impl.h | 6500 | `6fc1e8956367d5d7fbf86cf5fe4d30ba28cee9ed0fb93939f9c7c30f9b252907` | 0 |
| secp256k1/secp256k1-zkp/src/util.h | 13326 | `c987ae9066b447e16c102767b8cd58b2555b5db4a0cd966e9bf4a58ac4c983d1` | 0 |
