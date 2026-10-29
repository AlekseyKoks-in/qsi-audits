# Отчёт об аудите безопасности и постквантовой готовности

**Проект:** trustwallet-wallet-core @ adf80f8bac98 · Trust Wallet — публичный репозиторий (пассивная проверка)
| | |
|---|---|
| Организация | QSI |
| Дата отчёта | 2026-10-29 05:59 UTC |
| Версия отчёта | 1 |
| Запуск аудита | 53ee9f40-bf9b-4cc7-8301-73d775703f3d (Документальный аудит) |
| Версия анализатора | qsi-engine 1.2.0 |
| Профиль риска | Криптобиржа, кастодиан или кошелёк |
| SHA-256 содержимого | `4704b49e843bb279b44c96a91beee1357d25d6854946a2e9dd09694609f0f746` |
| Ключ подписи (Ed25519, отпечаток SHA-256; подпись — отдельный файл report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.

## 1. Резюме для руководства

- Критическая: **0**
- Высокая: **0**
- Средняя: **9**
- Низкая: **0**
- Информационная: **15**

- Подтверждённая техническая уязвимость: 1
- Известная уязвимая версия компонента: 7
- Подтверждённая ошибка конфигурации: 0
- Потенциальный криптографический риск: 0
- Долгосрочный постквантовый риск: 8
- Рекомендация по улучшению: 7
- Недостаточность данных: 1

Неравенство Моски (x + y > z): x = 10, y = 5, z = 8 → при этом сценарии миграция завершится слишком поздно. _z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует._

Проверка аналитика: подтверждено — 11, не применимо — 13, отклонено как ложные срабатывания — 0.

**Постквантовая зрелость: Уровень 0 из 4 — постквантовой криптографии нет.** Следующий шаг: Проведите инвентаризацию: где классическая криптография с открытым ключом защищает долгоживущие данные и ключи, и выберите первую миграцию — обычно гибридный обмен ключами TLS и обёрнутые ключи.

## 2. Область и границы проверки

Режим: Документальный аудит

Репозиторий: <https://github.com/trustwallet/wallet-core> @ `adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9` — ссылки в доказательствах открывают строки на этом коммите.

1695 файлов, всего 5785435 байт, редактирований: 32; список SHA-256 по файлам — в приложении C.

## 3. Методология

| Область | Статус | Количество | Примеры |
|---|---|---|---|
| source_code | проверено | 1556 | include/TrustWalletCore/TWAES.h: 57 lines scanned with 16 rule patterns and 123 registry patterns; include/TrustWalletCore/TWAESPaddingMode.h: 18 lines scanned with 16 rule patterns and 123 registry patterns; include/TrustWalletCore/TWAccount.h: 77 lines scanned with 16 rule patterns and 123 registry patterns |
| dependencies | проверено | 47 | rust/Cargo.lock: 246 dependencies parsed (246 pinned); rust/Cargo.toml: 0 dependencies parsed (0 pinned); rust/chains/tw_aptos/Cargo.toml: 4 dependencies parsed (0 pinned) |
| secrets | проверено | 19 | rust/chains/tw_pactus/src/transaction/mod.rs: 2 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); rust/chains/tw_pactus/src/types/address.rs: value(s) at line(s) 334 (test_address_from_private_key) are declared inside a fixture and treated as test data, although the file itself is not test code; rust/chains/tw_pactus/src/types/address.rs: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| chain_map | проверено | 59 | rust/tw_cosmos_sdk/Protobuf/authz_tx.proto: Cosmos SDK chains; rust/tw_cosmos_sdk/Protobuf/bank_tx.proto: Cosmos SDK chains; rust/tw_cosmos_sdk/Protobuf/coin.proto: Cosmos SDK chains |
| osv_advisories | проверено | 1 | 246 pinned packages queried at OSV.dev; 15 affected (2 of them only in development or build dependencies) |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## 4. Проверенные и непроверенные активы

- Нет

## 5. Краткое описание архитектуры

Static review of the source tree trustwallet-wallet-core at adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9. 1695 files analysed; of 2105 files, 373 are test, fuzzing, benchmark or example code and were left out, 36 are not read by any analyzer, 1 exceed the per-file limit and 0 did not fit the total limit. No requests were sent to the owner's systems.

## 6. Общая оценка состояния безопасности

- Ориентировочный индекс состояния: **95** / 100 — _Рассчитан по находкам в области проверки (подтверждённые и потенциальные проблемы, взвешенные по серьёзности). Ориентировочный; не сравним между аудитами с разной областью._
- Доля квантово-уязвимых элементов инвентаризации: 71.5%

## 7. Подробное описание находок

### QSI-2026-06464 — Подпись транзакций для сетей (43) основана на подписях на эллиптических кривых

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Высокая
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** True by construction and the headline row for this repository: the protobuf definitions cover 43 chains, every one of which authorizes transactions with ECDSA, Ed25519 or Schnorr. A wallet library cannot migrate any of them unilaterally — consensus decides — so the deliverable is a per-chain readiness map, and its ordering is the actual product. Nothing here is a defect in wallet-core.
- Затронутый актив: `chain-map`
- Источник данных: rust/tw_cosmos_sdk/Protobuf/authz_tx.proto
- Метод обнаружения: Определения сообщений (.proto) сопоставлены с таблицей схем подписи сетей QSI.
- Анализатор: chain_map 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 56.8 / 100
- CVSS v3.1: неприменимо

Определения сообщений кошелька охватывают сети: Aion, Algorand, Aptos, BNB Beacon Chain, BNB Greenfield, Bitcoin, Cardano, Cosmos SDK chains, Decred, EOS, Ethereum and EVM chains, Everscale, FIO, Filecoin, Harmony, Hedera, ICON, IOST, Internet Computer, IoTeX, MultiversX, NEAR, NULS, Nano, Nebulas, Neo, Nervos CKB, Nimiq, Oasis, Ontology, Polkadot and Substrate chains, Polymesh, Solana, Stellar, Sui, TON, Tezos, Theta, Tron, VeChain, XRP Ledger, Zcash (transparent), æternity. Эти сети авторизуют транзакции подписями BLS12-381, ECDSA, Ed25519, Schnorr (BIP-340), sr25519, которые алгоритм Шора взламывает на криптографически значимом квантовом компьютере. Кошелёк не может сам перевести сеть на постквантовые подписи: сначала схему должна принять сеть.

**Возможные последствия.** Когда появится CRQC, атакующий, увидевший открытый ключ аккаунта, сможет вычислить закрытый ключ и вывести средства; когда ключи раскрываются, зависит от сети (повторное использование адресов, модель аккаунтов).

**Шаги воспроизведения.**

```
Откройте файлы .proto, указанные в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [rust/tw_cosmos_sdk/Protobuf/authz_tx.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_cosmos_sdk/Protobuf/authz_tx.proto#L3) · line 3 · SHA-256 7ee1228daba53fb5617b888cc0403d0a751138449db3950c5a74f5f884574d5d_

```
package cosmos.authz.v1beta1;
```

_file_excerpt · [rust/tw_cosmos_sdk/Protobuf/bank_tx.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_cosmos_sdk/Protobuf/bank_tx.proto#L2) · line 2 · SHA-256 f6546a890c481e81c5b75d98264b93a6fcb85e9445c54ba5806db9937b6be5ac_

```
package cosmos.bank.v1beta1;
```

_file_excerpt · [rust/tw_cosmos_sdk/Protobuf/coin.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_cosmos_sdk/Protobuf/coin.proto#L2) · line 2 · SHA-256 db8c63b0b95be7e7aa4044ee20c0a182bfe2106eb5b9915c533b89ff4f87d847_

```
package cosmos.base.v1beta1;
```

_file_excerpt · [rust/tw_cosmos_sdk/Protobuf/crypto_multisig.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_cosmos_sdk/Protobuf/crypto_multisig.proto#L2) · line 2 · SHA-256 f101bd4459a23618679f8acbfacb2423d1562f82bcfa5881be9feefc5e3f04f2_

```
package cosmos.multisig.v1beta1;
```

_file_excerpt · [rust/tw_cosmos_sdk/Protobuf/crypto_secp256k1_keys.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_cosmos_sdk/Protobuf/crypto_secp256k1_keys.proto#L2) · line 2 · SHA-256 1accaa627d0a2e4488e3695402654fb0eb422b4f3979c9fa0482338d241c0cf2_

```
package cosmos.crypto.secp256k1;
```

_file_excerpt · [rust/tw_cosmos_sdk/Protobuf/distribution_tx.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_cosmos_sdk/Protobuf/distribution_tx.proto#L2) · line 2 · SHA-256 dafd633ea087f93183fed900419ed3e79fae8f3b5d47fe88344a6a9de4e6f351_

```
package cosmos.distribution.v1beta1;
```

_file_excerpt · [rust/tw_cosmos_sdk/Protobuf/gov_tx.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_cosmos_sdk/Protobuf/gov_tx.proto#L3) · line 3 · SHA-256 ba0c9e2ffb4bb2a322e5016428f1bce66760857ed1561c97b0d44b9bd486cb09_

```
package cosmos.gov.v1beta1;
```

_file_excerpt · [rust/tw_cosmos_sdk/Protobuf/greenfield_ethsecp256k1.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_cosmos_sdk/Protobuf/greenfield_ethsecp256k1.proto#L2) · line 2 · SHA-256 1237ec9411d39cc3799dcd390f322ce07f05ccad9825620c825904cf31a22a24_

```
package cosmos.crypto.eth.ethsecp256k1;
```

_file_excerpt · [rust/tw_cosmos_sdk/Protobuf/greenfield_tx.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_cosmos_sdk/Protobuf/greenfield_tx.proto#L2) · line 2 · SHA-256 9352fcea9c50dbb0a78bc8d1d84b5c6f7062e40f3d8950be9adf3d046fec961b_

```
package greenfield.bridge;
```

_file_excerpt · [rust/tw_cosmos_sdk/Protobuf/staking_tx.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_cosmos_sdk/Protobuf/staking_tx.proto#L2) · line 2 · SHA-256 8a188a9f34eeb14df30b980390fa4f5834a7cc864e32a8053a7f8162b7810ff5_

```
package cosmos.staking.v1beta1;
```

_file_excerpt · [rust/tw_cosmos_sdk/Protobuf/tx.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_cosmos_sdk/Protobuf/tx.proto#L2) · line 2 · SHA-256 316e69a8e877e3ec72d20d2ce558b58e30a2fa2d0978803fac8fbd5c61207758_

```
package cosmos.tx.v1beta1;
```

_file_excerpt · [rust/tw_cosmos_sdk/Protobuf/tx_signing.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_cosmos_sdk/Protobuf/tx_signing.proto#L2) · line 2 · SHA-256 9de8d719853a1cd08824252f18406868134274e1cdcc13332338944e4ec6ee96_

```
package cosmos.signing.v1beta1;
```

_file_excerpt · [src/proto/Aeternity.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/proto/Aeternity.proto#L3) · line 3 · SHA-256 b32f557fe4f4e25313f57f6e57ced3b6bf6a64c497895b40a41bef25e50c1fd7_

```
package TW.Aeternity.Proto;
```

_file_excerpt · [src/proto/Aion.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/proto/Aion.proto#L3) · line 3 · SHA-256 2cf1ac7b573d07215d5268452762a72dfe4d941b9b33dcd58609f7beb91f0fa1_

```
package TW.Aion.Proto;
```

_file_excerpt · [src/proto/Algorand.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/proto/Algorand.proto#L3) · line 3 · SHA-256 3119a1d10cc445858e7dd50b2022654ad4d2102c3d2d3209a4bead909619b975_

```
package TW.Algorand.Proto;
```

_file_excerpt · [src/proto/Aptos.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/proto/Aptos.proto#L7) · line 7 · SHA-256 c5260f6a863e2a58db9012177aa7d6e5d2ef37019b1e7e11ac98d9b9d91f9904_

```
package TW.Aptos.Proto;
```

_file_excerpt · [src/proto/Binance.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/proto/Binance.proto#L3) · line 3 · SHA-256 b8e4866aabb8ab92e8e3fccb0f5ff5413e4473f433331f27b1d074cf8de803b0_

```
package TW.Binance.Proto;
```

_file_excerpt · [src/proto/Bitcoin.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/proto/Bitcoin.proto#L3) · line 3 · SHA-256 9b4140920cfccf896347d3b4cf899c480baeeafa8bfc00c1da01bcfe8283ed0c_

```
package TW.Bitcoin.Proto;
```

_file_excerpt · [src/proto/BitcoinV2.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/proto/BitcoinV2.proto#L3) · line 3 · SHA-256 24b9bbc3a287f3f2f14e3d1b1ec588fa35908a05babbef1bd208afe1cbdadcc7_

```
package TW.BitcoinV2.Proto;
```

_file_excerpt · [src/proto/Cardano.proto](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/proto/Cardano.proto#L3) · line 3 · SHA-256 8792838f34bf778627eb59b463b2cea7c3360b797c39f59a27a35f67563e1943_

```
package TW.Cardano.Proto;
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Сети распознаются по именам определений сообщений (файлы .proto и пакеты); схемы — документированные подписи аккаунтов сетей, а не анализ кода подписи кошелька.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями. Сохраняйте криптогибкость слоя подписи по каждой сети (идентификаторы алгоритмов в сообщениях и хранилище, место под более длинные ключи и подписи) и отслеживайте постквантовые предложения сетей, чтобы добавить новую схему, когда сеть её активирует.

**Повторная проверка.** Повторить, когда сеть активирует постквантовую схему подписи или кошелёк добавит её поддержку.

### QSI-2026-06456 — Квантово-уязвимый ECDSA: подпись транзакций и сообщений (84 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** The remaining rows carry roles the engine determined and review agrees with. ECDSA across 84 files (211 references), anchored at include/TrustWalletCore/TWCurve.h:14 and running through every chain's signer, and Ed25519 across 33 files, are transaction and message signing: a CRQC derives the private key from a public key that is already on chain after the first spend. ECDSA at tw_internet_computer/src/protocol/identity.rs:6 is authentication and identity, a shorter-lived exposure. This repository is the largest single row count in the portfolio (355 inventory rows, 254 Shor-breakable) because it supports the most chains, not because it is the weakest code.
- Затронутый актив: `source-code:ECDSA:transaction_signing`
- Источник данных: include/TrustWalletCore/TWCurve.h
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

211 упоминаний ECDSA в 84 файл(ах), например include/TrustWalletCore/TWCurve.h:14. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте include/TrustWalletCore/TWCurve.h:14 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [include/TrustWalletCore/TWCurve.h](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/include/TrustWalletCore/TWCurve.h#L14) · line 14 · SHA-256 0e788cd2a9821aba60f5f665d317d31258ffce2e9ed4467f0f4701d6dc630ead_

```
   13 | enum TWCurve {
   14 |     TWCurveSECP256k1              /* "secp256k1" */,
   15 |     TWCurveED25519                /* "ed25519" */,
```

_file_excerpt · [rust/chains/tw_binance/src/compiler.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_binance/src/compiler.rs#L17) · line 17 · SHA-256 ffde304f79d96fb736ca768ba785b3a537e97d341fba33e7bf8d7a8f3d213069_

```
   16 | use tw_cosmos_sdk::modules::serializer::json_serializer::JsonSerializer;
   17 | use tw_cosmos_sdk::public_key::secp256k1::Secp256PublicKey;
   18 | use tw_cosmos_sdk::public_key::CosmosPublicKey;
```

_file_excerpt · [rust/chains/tw_binance/src/context.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_binance/src/context.rs#L7) · line 7 · SHA-256 57daf48e843eac1036710508adfdb069531738db7b8a6c985e235e9a29164d13_

```
    6 | use tw_cosmos_sdk::context::CosmosContext;
    7 | use tw_cosmos_sdk::private_key::secp256k1::Secp256PrivateKey;
    8 | use tw_cosmos_sdk::public_key::secp256k1::Secp256PublicKey;
```

_file_excerpt · [rust/chains/tw_binance/src/context.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_binance/src/context.rs#L8) · line 8 · SHA-256 90fbbea1bf282b0c9642e5404940d571f5a33e921d5c8bf1dbb508449b5c69b2_

```
    7 | use tw_cosmos_sdk::private_key::secp256k1::Secp256PrivateKey;
    8 | use tw_cosmos_sdk::public_key::secp256k1::Secp256PublicKey;
    9 | use tw_cosmos_sdk::signature::secp256k1::Secp256k1Signature;
```

_file_excerpt · [rust/chains/tw_binance/src/context.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_binance/src/context.rs#L9) · line 9 · SHA-256 1ba4ee90c18bcd14a4fd470e22a584822ca80eebcdaadb4a390c87ee4332ba6e_

```
    8 | use tw_cosmos_sdk::public_key::secp256k1::Secp256PublicKey;
    9 | use tw_cosmos_sdk::signature::secp256k1::Secp256k1Signature;
   10 | use tw_hash::hasher::Hasher;
```

_file_excerpt · [rust/chains/tw_binance/src/signer.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_binance/src/signer.rs#L15) · line 15 · SHA-256 9132820941960c2f1639ca83de3b097d8f463301dcdc513fbd05ca9aea2fa2e8_

```
   14 | use tw_cosmos_sdk::modules::serializer::json_serializer::JsonSerializer;
   15 | use tw_cosmos_sdk::public_key::secp256k1::Secp256PublicKey;
   16 | use tw_keypair::ecdsa::secp256k1;
```

_file_excerpt · [rust/chains/tw_binance/src/signer.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_binance/src/signer.rs#L16) · line 16 · SHA-256 60fcc90f8462cd9fc10e15f8deb2de6e7315336dd0ce729dcf7f7c3502de9821_

```
   15 | use tw_cosmos_sdk::public_key::secp256k1::Secp256PublicKey;
   16 | use tw_keypair::ecdsa::secp256k1;
   17 | use tw_keypair::traits::{KeyPairTrait, SigningKeyTrait};
```

_file_excerpt · [rust/chains/tw_binance/src/signer.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_binance/src/signer.rs#L39) · line 39 · SHA-256 b4554e8b0de95bf7ebbc083e6e4c2ac39467f7bcc8847aab86b5a0f929545e5d_

```
   38 | 
   39 |         let key_pair = secp256k1::KeyPair::try_from(input.private_key.as_ref())?;
   40 | 
```

_file_excerpt · [rust/chains/tw_binance/src/transaction/mod.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_binance/src/transaction/mod.rs#L8) · line 8 · SHA-256 e6e3da14e69186208299f0a23326a2c20975fe7460746ae6192ec9b51070336b_

```
    7 | use serde::{Deserialize, Serialize};
    8 | use tw_cosmos_sdk::public_key::secp256k1::Secp256PublicKey;
    9 | use tw_memory::Data;
```

_file_excerpt · [rust/chains/tw_bitcoin/src/babylon/spending_info.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_bitcoin/src/babylon/spending_info.rs#L55) · line 55 · SHA-256 301cbb746c8184116fa67e7806cea110be8daa7db05cc5d797a74e816fff52c9_

```
   54 |             .expect("Leaf added at a valid depth")
   55 |             .finalize(secp256k1::SECP256K1, *UNSPENDABLE_KEY_PATH_XONLY)
   56 |             .expect("Expected a valid Taproot tree");
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06457 — Квантово-уязвимый Ed25519: подпись транзакций и сообщений (33 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** The remaining rows carry roles the engine determined and review agrees with. ECDSA across 84 files (211 references), anchored at include/TrustWalletCore/TWCurve.h:14 and running through every chain's signer, and Ed25519 across 33 files, are transaction and message signing: a CRQC derives the private key from a public key that is already on chain after the first spend. ECDSA at tw_internet_computer/src/protocol/identity.rs:6 is authentication and identity, a shorter-lived exposure. This repository is the largest single row count in the portfolio (355 inventory rows, 254 Shor-breakable) because it supports the most chains, not because it is the weakest code.
- Затронутый актив: `source-code:Ed25519:transaction_signing`
- Источник данных: rust/chains/tw_aptos/src/address.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 41.8 / 100
- CVSS v3.1: неприменимо

69 упоминаний Ed25519 в 33 файл(ах), например rust/chains/tw_aptos/src/address.rs:40. Роль по путям, именам функций и соседнему коду: подпись транзакций и сообщений. CRQC восстанавливает закрытый ключ по уже известному открытому (в блокчейне после первой траты, при повторном использовании адреса): средствам и подтверждениям под этими ключами нужен путь миграции.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте rust/chains/tw_aptos/src/address.rs:40 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [rust/chains/tw_aptos/src/address.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_aptos/src/address.rs#L40) · line 40 · SHA-256 8f7b78a463449acce69b658c699c439f39c2c59a2c239cfa988fb170c509db36_

```
   39 |     pub fn with_ed25519_pubkey(
   40 |         pubkey: &ed25519::sha512::PublicKey,
   41 |     ) -> Result<Address, AddressError> {
```

_file_excerpt · [rust/chains/tw_aptos/src/signer.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_aptos/src/signer.rs#L25) · line 25 · SHA-256 2845f180f614099134d28cb8d46d648121f8ec3028a4f3c7a50275bd738b3bd4_

```
   24 |     ) -> SigningResult<Proto::SigningOutput<'static>> {
   25 |         let key_pair = ed25519::sha512::KeyPair::try_from(input.private_key.as_ref())?;
   26 |         let builder = transaction_builder::TransactionFactory::new_from_protobuf(input.clone())?;
```

_file_excerpt · [rust/chains/tw_aptos/src/transaction.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_aptos/src/transaction.rs#L14) · line 14 · SHA-256 009b3511b7752e430efb26276e5d2d731f3c5089c80e7419e938afad6309a9c3_

```
   13 | use tw_encoding::{bcs, EncodingResult};
   14 | use tw_keypair::ed25519::sha512::KeyPair;
   15 | use tw_keypair::traits::{KeyPairTrait, SigningKeyTrait};
```

_file_excerpt · [rust/chains/tw_aptos/src/transaction.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_aptos/src/transaction.rs#L64) · line 64 · SHA-256 d348225535878491ed1e52a540d0e935c82c0c703679b7720844bd59abfb1a39_

```
   63 |                        "signature": encode(signature, true),
   64 |                        "type": "ed25519_signature"})
   65 |             },
```

_file_excerpt · [rust/chains/tw_pactus/src/signer.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_pactus/src/signer.rs#L30) · line 30 · SHA-256 afa2a5fcda89821934b2767fb5451c5fc96c627693fae6888689db48621a9784_

```
   29 |         let mut trx = TxBuilder::from_proto(&input)?;
   30 |         let key_pair = ed25519::sha512::KeyPair::try_from(input.private_key.as_ref())?;
   31 |         let signature = trx.sign(key_pair.private())?;
```

_file_excerpt · [rust/chains/tw_pactus/src/transaction/mod.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_pactus/src/transaction/mod.rs#L8) · line 8 · SHA-256 22dd2a0a30b89479c0648462ceaa06516f217f7dd887bd984cc1e5ae4e82847c_

```
    7 | use tw_hash::blake2::blake2_b;
    8 | use tw_keypair::ed25519::sha512::{PrivateKey, PublicKey};
    9 | use tw_keypair::ed25519::Signature;
```

_file_excerpt · [rust/chains/tw_pactus/src/transaction/mod.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_pactus/src/transaction/mod.rs#L9) · line 9 · SHA-256 096dee44db3159681c89fc885d808d8ffe050db941e19d111bdc681de5d3d174_

```
    8 | use tw_keypair::ed25519::sha512::{PrivateKey, PublicKey};
    9 | use tw_keypair::ed25519::Signature;
   10 | use tw_keypair::traits::SigningKeyTrait;
```

_file_excerpt · [rust/chains/tw_pactus/src/types/address.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_pactus/src/types/address.rs#L14) · line 14 · SHA-256 f04c6e347241cb5a0469c694101bd6091289a57e360bfb06e6fc9c510d1ec316_

```
   13 | use tw_hash::H160;
   14 | use tw_keypair::ed25519::sha512::PublicKey;
   15 | use tw_memory::Data;
```

_file_excerpt · [rust/chains/tw_polkadot/src/entry.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_polkadot/src/entry.rs#L9) · line 9 · SHA-256 0a65a90f33a5f367bd7938737d2dd24c8d3d91a30fef69a8cf1931951b81a3ab_

```
    8 | use tw_coin_entry::signing_output_error;
    9 | use tw_keypair::ed25519::sha512::{KeyPair, PublicKey};
   10 | use tw_number::U256;
```

_file_excerpt · [rust/chains/tw_polymesh/src/entry.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_polymesh/src/entry.rs#L9) · line 9 · SHA-256 0a65a90f33a5f367bd7938737d2dd24c8d3d91a30fef69a8cf1931951b81a3ab_

```
    8 | use tw_coin_entry::signing_output_error;
    9 | use tw_keypair::ed25519::sha512::{KeyPair, PublicKey};
   10 | use tw_number::U256;
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06458 — Квантово-уязвимый ECDSA: роль не определена (18 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Role resolved: the anchors are the keypair implementation itself — rust/tw_keypair/src/ecdsa/{mod.rs,nist256p1/private.rs,nist256p1/public.rs} and schnorr/public.rs — plus per-chain signature types (tw_binance/src/signature.rs, tw_internet_computer/src/protocol/principal.rs). This is the secp256k1 and NIST P-256 ECDSA that every chain crate signs through, so it is the same exposure as the transaction-signing rows reached one layer lower. Count it once: it is where the migration work lands, not an extra surface.
- Затронутый актив: `source-code:ECDSA:general`
- Источник данных: rust/chains/tw_binance/src/signature.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 40.2 / 100
- CVSS v3.1: неприменимо

50 упоминаний ECDSA в 18 файл(ах), например rust/chains/tw_binance/src/signature.rs:5. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте rust/chains/tw_binance/src/signature.rs:5 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [rust/chains/tw_binance/src/signature.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_binance/src/signature.rs#L5) · line 5 · SHA-256 88ba8fc39193afb25224b7d690a405837d75e758a4d7d498c0d59607409e5933_

```
    4 | 
    5 | use tw_keypair::ecdsa::secp256k1;
    6 | 
```

_file_excerpt · [rust/chains/tw_binance/src/signature.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_binance/src/signature.rs#L7) · line 7 · SHA-256 17c1ce48f1f586fb612fd04175b17ec4162dbd8e4add73d3541282890a5ffb0f_

```
    6 | 
    7 | pub type BinanceSignature = secp256k1::VerifySignature;
```

_file_excerpt · [rust/chains/tw_internet_computer/src/protocol/principal.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_internet_computer/src/protocol/principal.rs#L9) · line 9 · SHA-256 7eb78104add388b603c7624548372dcc5f817f90de66dfd02f7a38ab2f425330_

```
    8 | use tw_hash::{crc32::crc32, sha2::sha224};
    9 | use tw_keypair::ecdsa::secp256k1::PublicKey;
   10 | 
```

_file_excerpt · [rust/tw_keypair/src/ecdsa/mod.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_keypair/src/ecdsa/mod.rs#L14) · line 14 · SHA-256 551cceb26a98e6c740913f4820d69f98b4d46d8fc1d4660bc34e6b3f7012cae4_

```
   13 | pub mod nist256p1;
   14 | pub mod secp256k1;
   15 | pub mod signature;
```

_file_excerpt · [rust/tw_keypair/src/ecdsa/nist256p1/private.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_keypair/src/ecdsa/nist256p1/private.rs#L9) · line 9 · SHA-256 b9bfa9a067be5bf54001c7312b95a9ecfd74221c9bf249a8ca48da5937adec61_

```
    8 | use crate::{KeyPairError, KeyPairResult};
    9 | use p256::ecdsa::SigningKey;
   10 | use tw_encoding::hex;
```

_file_excerpt · [rust/tw_keypair/src/ecdsa/nist256p1/public.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_keypair/src/ecdsa/nist256p1/public.rs#L8) · line 8 · SHA-256 9d3fa16b6656d7e432a225cfe9307da71abc9d3e7cdb08bfadec4c56e3b01f3d_

```
    7 | use crate::{KeyPairError, KeyPairResult};
    8 | use p256::ecdsa::signature::hazmat::PrehashVerifier;
    9 | use p256::ecdsa::VerifyingKey;
```

_file_excerpt · [rust/tw_keypair/src/ecdsa/nist256p1/public.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_keypair/src/ecdsa/nist256p1/public.rs#L9) · line 9 · SHA-256 46bd6d49e210591f9efe04e328813099de8acff0054374ed79c09efb4831213e_

```
    8 | use p256::ecdsa::signature::hazmat::PrehashVerifier;
    9 | use p256::ecdsa::VerifyingKey;
   10 | use tw_encoding::hex;
```

_file_excerpt · [rust/tw_keypair/src/schnorr/public.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_keypair/src/schnorr/public.rs#L5) · line 5 · SHA-256 31e7bb6ba6db1a2423fedc84efb4d16e0416b965e4c241ba20cae4e35525ed9a_

```
    4 | use bitcoin::key::TapTweak;
    5 | use secp256k1::SECP256K1;
    6 | use tw_hash::{H256, H264};
```

_file_excerpt · [rust/tw_keypair/src/schnorr/public.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_keypair/src/schnorr/public.rs#L11) · line 11 · SHA-256 3c43a8dda1886ab2514afeea5b80d126f2f1a687bb7ce964928f1331ba350e62_

```
   10 | pub struct PublicKey {
   11 |     pub(crate) public: secp256k1::PublicKey,
   12 | }
```

_file_excerpt · [rust/tw_keypair/src/schnorr/public.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_keypair/src/schnorr/public.rs#L26) · line 26 · SHA-256 29068813b09ac765ac6466e087c701a7bf74bf40674baf429d7b06911bcb9ca4_

```
   25 |         PublicKey {
   26 |             public: secp256k1::PublicKey::from_x_only_public_key(
   27 |                 tweaked_pubkey.to_inner(),
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06459 — Квантово-уязвимый ECDSA: аутентификация и идентификация (сертификаты, токены, аттестация устройств) (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** The remaining rows carry roles the engine determined and review agrees with. ECDSA across 84 files (211 references), anchored at include/TrustWalletCore/TWCurve.h:14 and running through every chain's signer, and Ed25519 across 33 files, are transaction and message signing: a CRQC derives the private key from a public key that is already on chain after the first spend. ECDSA at tw_internet_computer/src/protocol/identity.rs:6 is authentication and identity, a shorter-lived exposure. This repository is the largest single row count in the portfolio (355 inventory rows, 254 Shor-breakable) because it supports the most chains, not because it is the weakest code.
- Затронутый актив: `source-code:ECDSA:authentication`
- Источник данных: rust/chains/tw_internet_computer/src/protocol/identity.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 40.2 / 100
- CVSS v3.1: неприменимо

1 упоминаний ECDSA в 1 файл(ах), например rust/chains/tw_internet_computer/src/protocol/identity.rs:6. Роль по путям, именам функций и соседнему коду: аутентификация и идентификация (сертификаты, токены, аттестация устройств). Краткоживущая аутентификация безопасна до появления CRQC; долгоживущим идентификаторам (аттестация устройств, ключи УЦ и SSH) план нужен раньше.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте rust/chains/tw_internet_computer/src/protocol/identity.rs:6 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [rust/chains/tw_internet_computer/src/protocol/identity.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_internet_computer/src/protocol/identity.rs#L6) · line 6 · SHA-256 232561ad0151094c6a9a805ec32107beaed65850f27225dc823c7332736dfd35_

```
    5 | use tw_hash::H256;
    6 | use tw_keypair::{ecdsa::secp256k1::PrivateKey, traits::SigningKeyTrait, KeyPairError};
    7 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06460 — Квантово-уязвимый Ed25519: роль не определена (14 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Role resolved: rust/tw_keypair/src/tw/{private,public}.rs are the type-erased keypair wrappers, and the remaining anchors are per-chain compilers and request builders (tw_pactus, tw_ton). Transaction signing, reached through the generic keypair layer rather than named at the call site — which is exactly why the role came back undetermined.
- Затронутый актив: `source-code:Ed25519:general`
- Источник данных: rust/chains/tw_pactus/src/compiler.rs
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 40.2 / 100
- CVSS v3.1: неприменимо

52 упоминаний Ed25519 в 14 файл(ах), например rust/chains/tw_pactus/src/compiler.rs:67. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте rust/chains/tw_pactus/src/compiler.rs:67 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [rust/chains/tw_pactus/src/compiler.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_pactus/src/compiler.rs#L67) · line 67 · SHA-256 ddbcc7e415e77ca7a22e0980904e952f4f702f4059125c69491820041f01eb19_

```
   66 | 
   67 |         let public_key = ed25519::sha512::PublicKey::try_from(public_key_bytes.as_slice())?;
   68 |         let signature = ed25519::Signature::try_from(signature_bytes.as_slice())?;
```

_file_excerpt · [rust/chains/tw_pactus/src/compiler.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_pactus/src/compiler.rs#L68) · line 68 · SHA-256 75ce9c3904ec65495ed5f71ac2ea06f5649d9ed0733e5bdfa4324f95c49e296d_

```
   67 |         let public_key = ed25519::sha512::PublicKey::try_from(public_key_bytes.as_slice())?;
   68 |         let signature = ed25519::Signature::try_from(signature_bytes.as_slice())?;
   69 | 
```

_file_excerpt · [rust/chains/tw_ton/src/compiler.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_ton/src/compiler.rs#L12) · line 12 · SHA-256 de275ff17bcc16ee5ec6118d607c522acc41c401c166447679a4f18b1a3a10bb_

```
   11 | use tw_coin_entry::signing_output_error;
   12 | use tw_keypair::ed25519::Signature;
   13 | use tw_proto::TheOpenNetwork::Proto;
```

_file_excerpt · [rust/chains/tw_ton/src/signing_request/builder.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/chains/tw_ton/src/signing_request/builder.rs#L12) · line 12 · SHA-256 0dc79cc64dd34a07b5d67c444ffadf7d1d1a964db7573cb94d461dc0ef8f7279_

```
   11 | use tw_coin_entry::error::prelude::*;
   12 | use tw_keypair::ed25519::sha512::{KeyPair, PublicKey};
   13 | use tw_number::U256;
```

_file_excerpt · [rust/tw_keypair/src/tw/private.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_keypair/src/tw/private.rs#L79) · line 79 · SHA-256 fd6251750d927ce0fd61d43423cb4135dbfab48054fb525530d29da975162716_

```
   78 |             Curve::Ed25519 => {
   79 |                 ed25519::sha512::PrivateKey::try_from(&bytes[Self::KEY_RANGE]).is_ok()
   80 |             },
```

_file_excerpt · [rust/tw_keypair/src/tw/private.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_keypair/src/tw/private.rs#L181) · line 181 · SHA-256 53dc5b5da3e2596a05817299f3f253ad99d18eb1a02d7cee9f501d152ac6ca29_

```
  180 |     /// Tries to convert [`PrivateKey::key`] to [`ed25519::sha512::PrivateKey`].
  181 |     fn to_ed25519(&self) -> KeyPairResult<ed25519::sha512::PrivateKey> {
  182 |         ed25519::sha512::PrivateKey::try_from(self.key().as_slice())
```

_file_excerpt · [rust/tw_keypair/src/tw/private.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_keypair/src/tw/private.rs#L182) · line 182 · SHA-256 85914753ff8ccd15280f13641c2b04236278ac0b8c2b308afff8d71bcc80cfc2_

```
  181 |     fn to_ed25519(&self) -> KeyPairResult<ed25519::sha512::PrivateKey> {
  182 |         ed25519::sha512::PrivateKey::try_from(self.key().as_slice())
  183 |     }
```

_file_excerpt · [rust/tw_keypair/src/tw/public.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_keypair/src/tw/public.rs#L21) · line 21 · SHA-256 0c091ed9d5203b044423b589e6b4ef4f3af29b7f447be8d0f9f1eb857a58dacc_

```
   20 |     Nist256p1Extended(nist256p1::PublicKey),
   21 |     Ed25519(ed25519::sha512::PublicKey),
   22 |     Ed25519Blake2b(ed25519::blake2b::PublicKey),
```

_file_excerpt · [rust/tw_keypair/src/tw/public.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_keypair/src/tw/public.rs#L53) · line 53 · SHA-256 692dbf1f35d75f1081b2bfc2dcd3227394e1df95358f0d1fbf84ac3b67ff4448_

```
   52 |             },
   53 |             PublicKeyType::Ed25519 if ed25519::sha512::PublicKey::LEN == bytes.len() => {
   54 |                 let pubkey = ed25519::sha512::PublicKey::try_from(bytes.as_slice())?;
```

_file_excerpt · [rust/tw_keypair/src/tw/public.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_keypair/src/tw/public.rs#L54) · line 54 · SHA-256 904b0eda9991a4f7da9c914e4c8c3b66095da392fc2ac0de8e1634aeca836eea_

```
   53 |             PublicKeyType::Ed25519 if ed25519::sha512::PublicKey::LEN == bytes.len() => {
   54 |                 let pubkey = ed25519::sha512::PublicKey::try_from(bytes.as_slice())?;
   55 |                 Ok(PublicKey::Ed25519(pubkey))
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06462 — Квантово-уязвимый ECDH: роль не определена (1 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Role resolved: trezor-crypto/crypto/bip32.c:710 is the vendored copy of trezor-crypto's hdnode_get_shared_key, the same ECDH-over-a-BIP-32-node function reviewed in trezor-firmware.yml. Session keys for identity and encryption features, so harvest-now-decrypt-later applies; one row, not a signing exposure.
- Затронутый актив: `source-code:ECDH:general`
- Источник данных: trezor-crypto/crypto/bip32.c
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 40.2 / 100
- CVSS v3.1: неприменимо

1 упоминаний ECDH в 1 файл(ах), например trezor-crypto/crypto/bip32.c:710. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте trezor-crypto/crypto/bip32.c:710 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [trezor-crypto/crypto/bip32.c](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/trezor-crypto/crypto/bip32.c#L710) · line 710 · SHA-256 fc0f67b75badada1d9f60f67987b2b65b192f28758f4f422ee5a308ea5c751ed_

```
  709 |     *result_size = 0;
  710 |     return 1;  // ECDH is not supported
  711 |   }
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06463 — Квантово-уязвимый X25519: роль не определена (3 файл(ов))

- Серьёзность: **Средняя** · Классификация: Долгосрочный постквантовый риск · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Role resolved: all three anchors are the vendored trezor-crypto C library (trezor-crypto/crypto/bip32.c:504, crypto/ed25519-donna/ed25519.c, include/TrezorCrypto/ed25519.h) — the curve25519 public-key derivation layer underneath the Ed25519 signing rows, not an independent use. In the inventory because the derivation changes in any post-quantum scheme; not additional exposure on top of the signing rows.
- Затронутый актив: `source-code:X25519:general`
- Источник данных: trezor-crypto/crypto/bip32.c
- Метод обнаружения: Сопоставление регулярных выражений с криптографическими API; роль определяется по словам в путях, именам охватывающих функций и строкам рядом с совпадениями.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 40.2 / 100
- CVSS v3.1: неприменимо

6 упоминаний X25519 в 3 файл(ах), например trezor-crypto/crypto/bip32.c:504. Роль по путям, именам функций и соседнему коду: роль не определена. По коду не видно, что защищают ключи; приоритет определит проверка.

**Возможные последствия.** Долгосрочный риск зависит от назначения: подписи (подлинность до миграции) или обмен ключами/шифрование (ретроспективная расшифровка записанных данных).

**Шаги воспроизведения.**

```
Откройте trezor-crypto/crypto/bip32.c:504 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [trezor-crypto/crypto/bip32.c](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/trezor-crypto/crypto/bip32.c#L504) · line 504 · SHA-256 47d113caf7018eed16f9b117c4871eced54640a9c8bb72d92452967b09489236_

```
  503 |     } else if (node->curve == &curve25519_info) {
  504 |       curve25519_scalarmult_basepoint(node->public_key + 1, node->private_key);
  505 | #if USE_CARDANO
```

_file_excerpt · [trezor-crypto/crypto/bip32.c](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/trezor-crypto/crypto/bip32.c#L704) · line 704 · SHA-256 83f6544d5aa3abd1751b645ed1b6a2ebb0b589a1f46a0b596b1d2a85b2d20e5e_

```
  703 |     }
  704 |     curve25519_scalarmult(session_key + 1, node->private_key,
  705 |                           peer_public_key + 1);
```

_file_excerpt · [trezor-crypto/crypto/ed25519-donna/ed25519.c](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/trezor-crypto/crypto/ed25519-donna/ed25519.c#L256) · line 256 · SHA-256 9e656227d679e36314943547e7e588b91a3cddd726836f3245a74e5368df0d91_

```
  255 | void
  256 | curve25519_scalarmult_basepoint(curve25519_key pk, const curve25519_key e) {
  257 | 	curve25519_key ec = {0};
```

_file_excerpt · [trezor-crypto/crypto/ed25519-donna/ed25519.c](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/trezor-crypto/crypto/ed25519-donna/ed25519.c#L285) · line 285 · SHA-256 b328e900320ab22dad57147cdc9a054b232cb920970e43c140b16d0c52ef74f5_

```
  284 | void
  285 | curve25519_scalarmult(curve25519_key mypublic, const curve25519_key secret, const curve25519_key basepoint) {
  286 | 	curve25519_key e = {0};
```

_file_excerpt · [trezor-crypto/include/TrezorCrypto/ed25519.h](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/trezor-crypto/include/TrezorCrypto/ed25519.h#L27) · line 27 · SHA-256 878f8ae17d33525d5f47067318d7914607990b2f56694aabef79f0d138018961_

```
   26 | 
   27 | void curve25519_scalarmult(curve25519_key mypublic, const curve25519_key secret, const curve25519_key basepoint);
   28 | void curve25519_scalarmult_basepoint(curve25519_key mypublic, const curve25519_key secret);
```

_file_excerpt · [trezor-crypto/include/TrezorCrypto/ed25519.h](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/trezor-crypto/include/TrezorCrypto/ed25519.h#L28) · line 28 · SHA-256 5da1505233e10f4163e9aa512844147d4956f3002e08c01dc77ded1dfa97c442_

```
   27 | void curve25519_scalarmult(curve25519_key mypublic, const curve25519_key secret, const curve25519_key basepoint);
   28 | void curve25519_scalarmult_basepoint(curve25519_key mypublic, const curve25519_key secret);
   29 | 
```

**Ограничения проверки.** Это прогнозный риск, зависящий от появления криптографически значимого квантового компьютера (CRQC). Публично известных CRQC сегодня нет; сроки неопределённы. Это не уязвимость, эксплуатируемая сегодня. Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH; введите уровень абстракции для криптогибкости.

**Повторная проверка.** Повторите инвентаризацию после рефакторинга.

### QSI-2026-06470 — crypto-bigint 0.5.1 затронут RUSTSEC-2026-0387 (без оценки серьёзности)

- Серьёзность: **Средняя** · Классификация: Подтверждённая техническая уязвимость · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** crypto-bigint 0.5.1 (multiple timing variability issues in operations intended to be constant-time) is a hard, non-optional dependency of the signing path, so unlike in the BitBox02 firmware there is no feature flag to hide behind. rust/tw_keypair/Cargo.toml declares k256 0.13.0 with features ["ecdh", "ecdsa", "pkcs8", "schnorr", "std"] and p256 0.13.0 with ["ecdsa", "std"], both of which depend on elliptic-curve, which depends on crypto-bigint; starknet-crypto and starknet-ff reach it directly as well. Traced in rust/Cargo.lock: the workspace roots tw_tests and wallet_core_bin both reach it, by way of tw_keypair and therefore of every chain crate that signs. This is a library that signs on behalf of wallets on a host operating system, so timing variability in operations documented as constant-time is in scope rather than academic. No exploit is demonstrated and the attacker needs local measurement; medium, not high. Fixed in crypto-bigint 0.7.6, which is a breaking upgrade through elliptic-curve and will need k256/p256 to move first. _автоматическая серьёзность: Низкая._
- Затронутый актив: `dependency:crates.io/crypto-bigint@0.5.1`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 27.7 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает RUSTSEC-2026-0387 для пакета crates.io crypto-bigint версии 0.5.1: Multiple timing variability issues in operations intended to be constant-time. У бюллетеня нет ни вектора CVSS, ни оценки базы данных, поэтому QSI ставит низкую серьёзность и пометку «предварительно» до разбора. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-06476 — serde_with 3.16.0 затронут GHSA-7gcf-g7xr-8hxj

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** wallet-core uses serde_with only in tw_zcash (PCZT transparent bundle) as serde_as(as = "BTreeMap<[_; 33], _>"); KeyValueMap, the type whose serialization panics, is not referenced anywhere in the tree. _автоматическая серьёзность: Средняя._
- Затронутый актив: `dependency:crates.io/serde_with@3.16.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 35.2 / 100
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

### QSI-2026-06468 — block-buffer 0.9.0 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** Both affected versions are present (block-buffer 0.9.0 and 0.10.3) and both reach almost the whole tree through digest and blake-hash, so the dependency claim is right. The advisory needs a panic to be caught and the corrupted buffer then reused, and that cannot happen here: a code search for catch_unwind across trustwallet/wallet-core returns zero hits, and the C FFI boundary propagates rather than catches. The same advisory recurs in bitbox02-firmware, zcash's librustzcash, lightwalletd, zebra and the Android SDK, and monero-project/monero — which is the recurrence argument for a consolidated inventory, and is why it is worth recording a reasoned decision once rather than six times. _автоматическая серьёзность: Средняя._
- Затронутый актив: `dependency:crates.io/block-buffer@0.9.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-qwgh-2vcv-g2f7 для пакета crates.io block-buffer версии 0.9.0: block_buffer: panic corrupts inline buffer position. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-06469 — block-buffer 0.10.3 затронут GHSA-qwgh-2vcv-g2f7

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** Both affected versions are present (block-buffer 0.9.0 and 0.10.3) and both reach almost the whole tree through digest and blake-hash, so the dependency claim is right. The advisory needs a panic to be caught and the corrupted buffer then reused, and that cannot happen here: a code search for catch_unwind across trustwallet/wallet-core returns zero hits, and the C FFI boundary propagates rather than catches. The same advisory recurs in bitbox02-firmware, zcash's librustzcash, lightwalletd, zebra and the Android SDK, and monero-project/monero — which is the recurrence argument for a consolidated inventory, and is why it is worth recording a reasoned decision once rather than six times. _автоматическая серьёзность: Средняя._
- Затронутый актив: `dependency:crates.io/block-buffer@0.10.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-qwgh-2vcv-g2f7 для пакета crates.io block-buffer версии 0.10.3: block_buffer: panic corrupts inline buffer position. Бюллетень не называет затронутых функций, поэтому достижимость не определена.

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

### QSI-2026-06472 — keccak 0.1.3 затронут GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** keccak 0.1.3's unsoundness is in the opt-in ARMv8 assembly backend behind the asm Cargo feature, which is off by default and which no manifest in the audited tree enables; the advisory's own CVSS vector (AV:L/AC:H/AT:P, exploit maturity unproven) reflects that. keccak arrives through sha3 and tw_hash, both using the portable implementation. Upgrading to 0.1.6 is routine maintenance. _автоматическая серьёзность: Низкая._
- Затронутый актив: `dependency:crates.io/keccak@0.1.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012) для пакета crates.io keccak версии 0.1.3: Unsoundness in opt-in ARMv8 assembly backend for `keccak`. Затронутый код находится за флагом Cargo `asm`, выключенным по умолчанию; ни один проверенный манифест его не включает — бюллетень не применим, если флаг не включает другая зависимость.

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

### QSI-2026-06475 — rand 0.8.5 затронут GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** rand 0.8.5 is unsound only when a custom global logger calls rand::rng() reentrantly. wallet-core installs no global logger; rand reaches the tree through secp256k1, ark-std, fixed-hash and move-core-types, none of which log from inside the generator. The affected functions rand::rng and rand::thread_rng are not named in the audited code. _автоматическая серьёзность: Низкая._
- Затронутый актив: `dependency:crates.io/rand@0.8.5`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097) для пакета crates.io rand версии 0.8.5: Rand is unsound with a custom logger using rand::rng(). Проверенный код не упоминает затронутые функции (rand::rng, rand::thread_rng); rand приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-cq8v-f236-94qc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-cq8v-f236-94qc](https://osv.dev/vulnerability/GHSA-cq8v-f236-94qc) · manifest · SHA-256 84f328baa4aa1681eba22618a21d380d6b69ff39e6bef138ef912679c6d4245d_

```
{"id": "GHSA-cq8v-f236-94qc", "aliases": ["RUSTSEC-2026-0097"], "modified": "2026-09-10T03:50:43.958966498Z", "summary": "Rand is unsound with a custom logger using rand::rng()", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.10.1, 0.8.6, 0.9.3).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06477 — time 0.3.44 затронут GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** time 0.3.44 is pulled in only by serde_with (Cargo.lock), which wallet-core uses only for the BTreeMap adapter above; the affected RFC 2822 parsing functions are not reached. _автоматическая серьёзность: Средняя._
- Затронутый актив: `dependency:crates.io/time@0.3.44`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 26.4 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009) для пакета crates.io time версии 0.3.44: time vulnerable to stack exhaustion Denial of Service attack. Проверенный код не упоминает затронутые функции (time::Date::parse, time::OffsetDateTime::parse, time::PrimitiveDateTime::parse, time::Time::parse, time::UtcDateTime::parse, time::UtcOffset::parse …); time приходит через другие зависимости, которые могут их вызывать.

**Возможные последствия.** Зависит от достижимости уязвимого кода в вашем приложении.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/GHSA-r6v5-fh4h-64xc
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev GHSA-r6v5-fh4h-64xc](https://osv.dev/vulnerability/GHSA-r6v5-fh4h-64xc) · manifest · SHA-256 47bed44226c6f8f5c94bfd27c3dd67ade62aa708c5d61bcca37c2b8bbe9b577d_

```
{"id": "GHSA-r6v5-fh4h-64xc", "aliases": ["CVE-2026-25727", "RUSTSEC-2026-0009"], "modified": "2026-09-10T03:50:35.583241382Z", "summary": "time vulnerable to stack exhaustion Denial of Service attack", "severity": [{"type": "CVSS_V4", "score": "CVSS:4.0/AV:N/AC:H/AT:N/PR:L/UI:A/VC:N/VI:N/VA:H/SC:N/SI:N/SA:H"}], "declared_in_manifest": false}
```

**Ограничения проверки.** Данные об уязвимости получены от OSV.dev в зафиксированное время. Достижимость оценивается по именам, а не по графу вызовов: затронутые функции из бюллетеня — по идентификаторам проверенного кода продукта, флаг Cargo, выключенный по умолчанию, — по проверенным манифестам, платформы — по объявленным целям сборки Rust. Косвенные вызовы (через трейты, макросы, другие зависимости) не прослеживаются.

**Рекомендация.** Обновите до исправленной версии (0.3.47).

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06466 — anyhow 1.0.75 затронут RUSTSEC-2026-0190 (без оценки серьёзности)

- Серьёзность: **Информационная** · Классификация: Известная уязвимая версия компонента · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** anyhow 1.0.75 (unsoundness in Error::downcast_mut) arrives through move-core-types, so only the Aptos and Sui crates depend on it, and no audited file calls downcast_mut. Upgrading to 1.0.103 is routine maintenance rather than a fix for an exposure here. _автоматическая серьёзность: Низкая._
- Затронутый актив: `dependency:crates.io/anyhow@1.0.75`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 20.9 / 100
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

### QSI-2026-06467 — bincode 1.3.3: информационный бюллетень RUSTSEC-2025-0141 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Высокая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** Five unmaintained-crate notices (bincode 1.3.3, derivative 2.2.0, paste 1.0.11, proc-macro-error 1.0.4, unsafe-libyaml 0.2.11). None reports a defect and none carries cryptography, so none bears on post-quantum readiness; recording the decision to keep them, which is what an informational advisory asks for.
- Затронутый актив: `dependency:crates.io/bincode@1.3.3`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
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

### QSI-2026-06479 — 3 бюллетеней в 2 пакет(ах) crates.io, нужных только для разработки или сборки

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** Three advisories in two build-only crates (ansi_term 0.12.1 RUSTSEC-2021-0139; atty 0.2.14 GHSA-g98v-hv3f-hcfr and RUSTSEC-2024-0375), neither of which ships in a built artefact. They are worth updating during routine maintenance, and worth watching only insofar as they run in CI with credentials.
- Затронутый актив: `dependencies:crates.io:non-runtime`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch по точным версиям; область применения — из devDependencies, флагов dev в package-lock.json, разделов importers в pnpm, графа Cargo.lock от таблиц Cargo.toml и — для yarn.lock, который область не записывает вовсе — графа файла блокировки, пройденного от package.json. Если рабочее требование в файле блокировки разрешить не удалось, файл остаётся без классификации, чтобы пакет не был отложен в сторону по ошибке.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 18.3 / 100
- CVSS v3.1: неприменимо

OSV.dev сообщает 3 бюллетеней (0 с оценкой high или critical) для 2 пакет(ов) crates.io, которые подтягивают только инструменты разработки или сборки (rust/Cargo.lock): например, ansi_term@0.12.1 [build]: RUSTSEC-2021-0139; atty@0.2.14 [build]: GHSA-g98v-hv3f-hcfr, RUSTSEC-2024-0375. Манифесты помечают их так (devDependencies, "dev": true в package-lock.json, [dev-dependencies]/[build-dependencies] через граф Cargo.lock), поэтому в поставляемый продукт они не входят.

**Возможные последствия.** Пользователей продукта они не затрагивают. Они могут влиять на машины разработчиков и CI (цепочка поставки): скомпрометированный или уязвимый инструмент способен изменить сборку.

**Шаги воспроизведения.**

```
Найдите пакеты из доказательства на https://osv.dev и проверьте их область применения в rust/Cargo.lock.
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev (crates.io)](https://osv.dev/) · rust/Cargo.lock · SHA-256 d512f877bef1ab54a9ad6c9b72d65a548bdb13d69a354016a31df65cc1a19445_

```
ansi_term@0.12.1 [build]: RUSTSEC-2021-0139
atty@0.2.14 [build]: GHSA-g98v-hv3f-hcfr, RUSTSEC-2024-0375
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время. Области применения взяты из манифестов; собственные build-зависимости крейтов реестра в Cargo.lock не различимы, поэтому множество runtime может оказаться больше реального, но не меньше.

**Рекомендация.** Обновите инструменты в рамках планового обслуживания; в первую очередь пакеты, которые выполняются в CI с секретами или создают релизные артефакты.

**Повторная проверка.** Повторите сканирование зависимостей после обновления.

### QSI-2026-06461 — SHA-1 предоставляется функциями API (5 файл(ов))

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Accurate as stated, and the reason it cannot simply be removed is worth recording. rust/tw_hash/src/sha1.rs defines sha1() and rust/tw_hash/src/ffi.rs:128 exports it over the C FFI; it is published through the library's public surface as TWHash (include/TrustWalletCore/TWHash.h, src/interface/TWHash.cpp, src/Hash.h, src/Hash.cpp). No in-tree security decision depends on it, which is exactly what the rule says. But src/Bitcoin/OpCodes.h references SHA-1 because Bitcoin Script defines OP_SHA1, so a wallet library that evaluates or builds scripts has to be able to compute it: this is a consensus-level requirement, not a choice the library can revisit. Correct disposition is therefore to keep it, document it as script-compatibility only, and ensure no new caller uses it for integrity — not to delete it.
- Затронутый актив: `source-code:SHA-1:api`
- Источник данных: rust/tw_hash/src/ffi.rs
- Метод обнаружения: Сопоставление регулярных выражений с API конкретного языка; совпадение в определении, объявлении или внутри функции с именем алгоритма считается предоставлением.
- Анализатор: source_code 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 16.3 / 100
- CVSS v3.1: неприменимо

9 определений, объявлений или тонких обёрток SHA-1 в 5 файл(ах), например rust/tw_hash/src/ffi.rs:128. Эти файлы предоставляют алгоритм (библиотека хеширования, экспорт FFI); использования в решениях безопасности в них не найдено.

**Возможные последствия.** Само по себе — нет: риск зависит от вызывающего кода. Вызов, полагающийся на стойкость к коллизиям (подписи, сертификаты, дедупликация недоверенных данных), был бы слабым.

**Шаги воспроизведения.**

```
Откройте rust/tw_hash/src/ffi.rs:128 и проверьте приведённые строки; остальные файлы перечислены в доказательствах.
```

**Подтверждающие доказательства.**

_file_excerpt · [rust/tw_hash/src/ffi.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_hash/src/ffi.rs#L128) · line 128 · SHA-256 9ed1f22d34e422bf072bb686e56d03365d3ef92f492782a9d13a0b4920f1f6bd_

```
  127 | #[no_mangle]
  128 | pub unsafe extern "C" fn sha1(input: *const u8, input_len: usize) -> CByteArray {
  129 |     let input = std::slice::from_raw_parts(input, input_len);
```

_file_excerpt · [rust/tw_hash/src/ffi.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_hash/src/ffi.rs#L130) · line 130 · SHA-256 63735fc84ccd3fd503c83e7b94ec825cb7478638e63499fe7d0ccab8bfac9e64_

```
  129 |     let input = std::slice::from_raw_parts(input, input_len);
  130 |     sha1::sha1(input).into()
  131 | }
```

_file_excerpt · [rust/tw_hash/src/sha1.rs](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/rust/tw_hash/src/sha1.rs#L8) · line 8 · SHA-256 755b3868066df3e578dc9d0090494943ab96b936b04c84a0cd5280854eb45ffc_

```
    7 | 
    8 | pub fn sha1(input: &[u8]) -> Vec<u8> {
    9 |     hasher::<sha1::Sha1>(input)
```

_file_excerpt · [src/Hash.cpp](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/Hash.cpp#L56) · line 56 · SHA-256 6be2e5160d3be8988d8645bde3d67cb750e030332a63178280c2737684697249_

```
   55 | 
   56 | Data Hash::sha1(const byte* data, size_t size) {
   57 |     return Rust::CByteArrayWrapper(Rust::sha1(data, size)).data;
```

_file_excerpt · [src/Hash.cpp](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/Hash.cpp#L57) · line 57 · SHA-256 f7dcd9904ebfe1fef61c75143aa30b1f335e3acae32160b69481bc95fdebea0c_

```
   56 | Data Hash::sha1(const byte* data, size_t size) {
   57 |     return Rust::CByteArrayWrapper(Rust::sha1(data, size)).data;
   58 | }
```

_file_excerpt · [src/Hash.h](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/Hash.h#L55) · line 55 · SHA-256 ea5191b0b622d1414abe459334e606a115d7e1d79abbc302f598b8ebd39190c6_

```
   54 | /// Computes the SHA1 hash.
   55 | Data sha1(const byte* data, size_t size);
   56 | 
```

_file_excerpt · [src/Hash.h](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/Hash.h#L112) · line 112 · SHA-256 304180984a1b9593e033d769b20ae2ad6c4f5d3f0093d1f00fc5cd33288cc59e_

```
  111 | template <typename T>
  112 | Data sha1(const T& data) {
  113 |     return sha1(reinterpret_cast<const byte*>(data.data()), data.size());
```

_file_excerpt · [src/Hash.h](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/Hash.h#L113) · line 113 · SHA-256 b9acc9a98d4b9b288895b49c91e4e202243d7bcf143246699f182a631208ebb4_

```
  112 | Data sha1(const T& data) {
  113 |     return sha1(reinterpret_cast<const byte*>(data.data()), data.size());
  114 | }
```

_file_excerpt · [src/interface/TWHash.cpp](https://github.com/trustwallet/wallet-core/blob/adf80f8bac989e18a4ef1922e2b9eaeb4bf804a9/src/interface/TWHash.cpp#L20) · line 20 · SHA-256 5bd5abbb2909be2243b3e0e4e07e150eeb7e349157fff249c9e71122927dc2ed_

```
   19 | TWData* _Nonnull TWHashSHA1(TWData* _Nonnull data) {
   20 |     const auto result = Hash::sha1(reinterpret_cast<const byte*>(TWDataBytes(data)), TWDataSize(data));
   21 |     return TWDataCreateWithData(&result);
```

**Ограничения проверки.** Эвристическое сопоставление шаблонов в исходном тексте без анализа потоков данных. Контекст использования (влияет ли на безопасность) требует ручного подтверждения; находка предварительная.

**Рекомендация.** Зафиксируйте, зачем предоставляется SHA-1 (протокол или устаревший формат, которому он нужен), проверьте вызывающий код и выведите алгоритм из API там, где он не нужен.

**Повторная проверка.** Повторно просканируйте код после проверки.

### QSI-2026-06465 — Не обнаружено криптобиблиотек с поддержкой PQC

- Серьёзность: **Информационная** · Классификация: Недостаточность данных · Уверенность: Средняя
> **Проверка аналитика (QSI review, 2026-10-28): подтверждено аналитиком.** Accurate: across 47 dependency manifests the declared cryptography is curve25519-dalek, ecdsa, k256, p256 and secp256k1, with nothing PQC-capable. For a library that signs for 43 chains this is not a dependency that can usefully be added yet — each chain's signature scheme is set by its own consensus, so until a chain defines a post-quantum scheme there is nothing for the wallet to implement against. The actionable part is the opposite direction: the library should be ready to carry two schemes per chain during a transition, which is an architectural question about tw_keypair rather than a missing crate.
- Затронутый актив: `dependencies`
- Источник данных: dependency manifests
- Метод обнаружения: Сопоставление названий зависимостей.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 15.0 / 100
- CVSS v3.1: неприменимо

В 47 манифестах зависимостей QSI нашёл криптобиблиотеки (curve25519-dalek, ecdsa, k256, p256, secp256k1), но ни одной из списка поддерживающих PQC.

**Возможные последствия.** Только индикатор готовности: поддержка PQC может обеспечиваться платформой (OpenSSL, ОС, облачный KMS), а не зависимостями приложения.

**Шаги воспроизведения.**

```
Изучите перечисленные в доказательстве манифесты.
```

**Подтверждающие доказательства.**

_dependency · rust/Cargo.lock, rust/Cargo.toml, rust/chains/tw_aptos/Cargo.toml, rust/chains/tw_binance/Cargo.toml, rust/chains/tw_bitcoin/Cargo.toml, rust/chains/tw_bitcoincash/Cargo.toml, rust/chains/tw_cosmos/Cargo.toml, rust/chains/tw_decred/Cargo.toml, rust/chains/tw_ethereum/Cargo.toml, rust/chains/tw_greenfield/Cargo.toml, rust/chains/tw_groestlcoin/Cargo.toml, rust/chains/tw_internet_computer/Cargo.toml, rust/chains/tw_komodo/Cargo.toml, rust/chains/tw_native_evmos/Cargo.toml, rust/chains/tw_native_in · SHA-256 a5f70b6ce7042da5b0b824636b38dcb7070949ac7f84d558eb8842d79c68c310_

```
Crypto libraries: curve25519-dalek, ecdsa, k256, p256, secp256k1
```

**Ограничения проверки.** Отсутствие доказательств не является доказательством отсутствия: системные библиотеки и транзитивные зависимости могут не указываться.

**Рекомендация.** Определите источник поддержки PQC (TLS-терминатор, KMS/HSM, обновление библиотек).

**Повторная проверка.** Повторите сканирование после обновлений.

### QSI-2026-06471 — derivative 2.2.0: информационный бюллетень RUSTSEC-2024-0388 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** Five unmaintained-crate notices (bincode 1.3.3, derivative 2.2.0, paste 1.0.11, proc-macro-error 1.0.4, unsafe-libyaml 0.2.11). None reports a defect and none carries cryptography, so none bears on post-quantum readiness; recording the decision to keep them, which is what an informational advisory asks for.
- Затронутый актив: `dependency:crates.io/derivative@2.2.0`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2024-0388 для пакета crates.io derivative версии 2.2.0 как информационный (unmaintained): `derivative` is unmaintained; consider using an alternative. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0388
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2024-0388](https://osv.dev/vulnerability/RUSTSEC-2024-0388) · manifest · SHA-256 3438f6c3cab3309fb6388762a19097619076b18baff08e3e9ab34fa969478d55_

```
{"id": "RUSTSEC-2024-0388", "aliases": [], "modified": "2024-11-10T13:34:40Z", "summary": "`derivative` is unmaintained; consider using an alternative", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-06473 — paste 1.0.11: информационный бюллетень RUSTSEC-2024-0436 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** Five unmaintained-crate notices (bincode 1.3.3, derivative 2.2.0, paste 1.0.11, proc-macro-error 1.0.4, unsafe-libyaml 0.2.11). None reports a defect and none carries cryptography, so none bears on post-quantum readiness; recording the decision to keep them, which is what an informational advisory asks for.
- Затронутый актив: `dependency:crates.io/paste@1.0.11`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2024-0436 для пакета crates.io paste версии 1.0.11 как информационный (unmaintained): paste - no longer maintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

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

### QSI-2026-06474 — proc-macro-error 1.0.4: информационный бюллетень RUSTSEC-2024-0370 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** Five unmaintained-crate notices (bincode 1.3.3, derivative 2.2.0, paste 1.0.11, proc-macro-error 1.0.4, unsafe-libyaml 0.2.11). None reports a defect and none carries cryptography, so none bears on post-quantum readiness; recording the decision to keep them, which is what an informational advisory asks for.
- Затронутый актив: `dependency:crates.io/proc-macro-error@1.0.4`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2024-0370 для пакета crates.io proc-macro-error версии 1.0.4 как информационный (unmaintained): proc-macro-error is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0370
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2024-0370](https://osv.dev/vulnerability/RUSTSEC-2024-0370) · manifest · SHA-256 31fe0830d6149ef7bd8a557f7bdf7451b97b71aa4e25f7a96204c4fc47ba193f_

```
{"id": "RUSTSEC-2024-0370", "aliases": [], "modified": "2026-06-07T20:00:03.923932350Z", "summary": "proc-macro-error is unmaintained", "severity": null, "declared_in_manifest": false}
```

**Ограничения проверки.** Данные получены от OSV.dev в зафиксированное время.

**Рекомендация.** Запланируйте переход на поддерживаемую альтернативу или зафиксируйте решение оставить пакет.

**Повторная проверка.** Повторите сканирование зависимостей после изменения.

### QSI-2026-06478 — unsafe-libyaml 0.2.11: информационный бюллетень RUSTSEC-2024-0449 (unmaintained)

- Серьёзность: **Информационная** · Классификация: Рекомендация по улучшению · Уверенность: Низкая
> **Проверка аналитика (QSI review, 2026-10-28): не применимо к этому коду.** Five unmaintained-crate notices (bincode 1.3.3, derivative 2.2.0, paste 1.0.11, proc-macro-error 1.0.4, unsafe-libyaml 0.2.11). None reports a defect and none carries cryptography, so none bears on post-quantum readiness; recording the decision to keep them, which is what an informational advisory asks for.
- Затронутый актив: `dependency:crates.io/unsafe-libyaml@0.2.11`
- Источник данных: OSV.dev
- Метод обнаружения: Запрос OSV.dev querybatch для точной объявленной версии.
- Анализатор: dependencies 1.2.0 · 2026-10-29 05:59 UTC
- Балл приоритета: 11.8 / 100
- CVSS v3.1: неприменимо

OSV.dev отмечает RUSTSEC-2024-0449 для пакета crates.io unsafe-libyaml версии 0.2.11 как информационный (unmaintained): unsafe-libyaml is unmaintained. Уязвимости в нём нет; неподдерживаемый пакет не получит исправлений будущих уязвимостей.

**Возможные последствия.** Известной уязвимости нет. Исправления безопасности в будущем могут не выйти.

**Шаги воспроизведения.**

```
curl -s https://api.osv.dev/v1/vulns/RUSTSEC-2024-0449
```

**Подтверждающие доказательства.**

_tool_output · [OSV.dev RUSTSEC-2024-0449](https://osv.dev/vulnerability/RUSTSEC-2024-0449) · manifest · SHA-256 26d102e813573cb2577fa623e28e26359b004df953372bdda3fd7cf447bb3d4b_

```
{"id": "RUSTSEC-2024-0449", "aliases": [], "modified": "2026-10-12T11:45:02.518189315Z", "summary": "unsafe-libyaml is unmaintained", "severity": null, "declared_in_manifest": false}
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
| **подпись транзакций и сообщений** | ECDSA (143), Ed25519 (92), BLS12-381 (59), Schnorr (BIP-340) (59), sr25519 (59) | QSI-2026-06456, QSI-2026-06457, QSI-2026-06464 | Следите за постквантовыми планами каждой сети, не используйте открытые ключи повторно и держите подписание готовым к постквантовым схемам по мере их принятия сетями |
| **аутентификация и идентификация (сертификаты, токены, аттестация устройств)** | ECDSA (1) | QSI-2026-06459 | Делайте учётные данные краткоживущими и планируйте сертификаты, токены и ключи ML-DSA по мере поддержки в экосистеме |
| **роль не определена** | ECDSA (18), Ed25519 (14), X25519 (3), ECDH (1) | QSI-2026-06458, QSI-2026-06460, QSI-2026-06462, QSI-2026-06463 | Классифицируйте каждое использование, зафиксируйте сроки жизни данных и запланируйте миграцию на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема; введите уровень абстракции для криптогибкости |

_Роль определяется по путям файлов, именам функций и коду вокруг совпадений; проверка её подтверждает. Сначала — ключи корня доверия и обёрнутые ключи: их трудно заменить или можно записать уже сегодня._
Анкета готовности для проекта не заполнялась.

### Квантовые алгоритмы, значимые для этой инвентаризации

| Квантовый алгоритм | Действие | Модель атаки | Алгоритмы из инвентаризации (строк) | Что это значит для аудита |
|---|---|---|---|---|
| Алгоритм Шора — дискретный логарифм в конечных полях | взламывает | Q1 | BLS12-381 (1) | Взламывает Диффи–Хеллмана в конечных полях и DSA при любом размере. Переводите установление ключей на ML-KEM (на переходный период — гибрид с X25519 или ECDH), подписи — на ML-DSA или SLH-DSA. |
| Алгоритм Шора — дискретный логарифм на эллиптических кривых | взламывает | Q1 | BLS12-381 (1), ECDH (1), ECDSA (151), Ed25519 (88), Schnorr (BIP-340) (2), X25519 (9), sr25519 (2) | Ключи на эллиптических кривых, по оценкам, падут раньше ключей RSA сопоставимой классической стойкости. В блокчейнах первыми под угрозой монеты, чей открытый ключ уже опубликован (повторно используемые адреса, выходы pay-to-public-key и Taproot); планируйте переход на постквантовые подписи и до этого избегайте повторного использования ключей. |
| Алгоритм Гровера — поиск ключа и прообразов | ослабляет (более длинные ключи восстанавливают запас) | Q1 | AES-128 (1), AES-192 (1), AES-256 (1), BLAKE2 (9), ChaCha20-Poly1305 (2), HMAC (8), Keccak-256 (38), PBKDF2 (2), Poly1305 (3), RC4 (2), RIPEMD-160 (3), SHA-1 (1), SHA-2 (9), SHA-3 (7), scrypt (2) | Не взлом. Ключи 256 бит (AES-256, ChaCha20) сохраняют хороший запас; AES-128 соответствует категории 1 NIST, но некоторые регуляторы требуют 256-битных ключей в квантово-устойчивых системах (см. запись AES-128). Для долгоживущих данных предпочитайте 256-битные ключи; 256-битные хеши для стойкости к прообразам менять не нужно. |
| Брассар–Хойер–Тапп — поиск коллизий | ослабляет (более длинные ключи восстанавливают запас) | Q1 | BLAKE2 (9), Keccak-256 (38), RIPEMD-160 (3), SHA-1 (1), SHA-2 (9), SHA-3 (7) | 256-битные хеши (SHA-256, SHA3-256) остаются достаточными по стойкости к коллизиям; 160-битные хеши слабы уже классически (коллизии SHA-1 практичны). Где нужны категории NIST 4–5, используйте хеши на 384/512 бит. |

_Действие: взламывает — алгоритм нужно заменить; ослабляет — более длинные ключи или выходы восстанавливают запас; учтено в стандартных параметрах — при стандартных наборах действий не требуется; только при суперпозиционных запросах — к обычному применению неприменимо._


## 9. Ограничения и допущения

- Отчёт содержит результаты автоматизированного и документального анализа в указанных границах. Он не является юридическим заключением, сертификацией или подтверждением соответствия какому-либо стандарту.
- z — плановое допущение профиля риска, а не прогноз. Публично известного криптографически значимого квантового компьютера сегодня не существует.

## 10. План устранения проблем / Приоритеты на 30, 60 и 90 дней

### 30 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P2 | QSI-2026-06476 | Обновите serde_with до исправленной версии (3.21.0). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-7gcf-g7xr-8hxj. |
| P2 | QSI-2026-06468 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-06469 | Обновите block-buffer до исправленной версии (пока не выпущена; меры смягчения — в бюллетене). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-qwgh-2vcv-g2f7. |
| P2 | QSI-2026-06472 | Обновите keccak до исправленной версии (0.1.6). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-3288-p39f-rqpv (RUSTSEC-2026-0012). |
| P2 | QSI-2026-06475 | Обновите rand до исправленной версии (0.10.1, 0.8.6, 0.9.3). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-cq8v-f236-94qc (RUSTSEC-2026-0097). |
| P2 | QSI-2026-06477 | Обновите time до исправленной версии (0.3.47). | устранение первопричины | Сканирование зависимостей больше не сообщает GHSA-r6v5-fh4h-64xc (CVE-2026-25727, RUSTSEC-2026-0009). |
### 60 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-06470 | Разберите RUSTSEC-2026-0387; при необходимости обновите crypto-bigint до исправленной версии (0.7.6). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0387 или результат разбора записан. |
| P3 | QSI-2026-06466 | Разберите RUSTSEC-2026-0190; при необходимости обновите anyhow до исправленной версии (1.0.103). | устранение первопричины | Сканирование больше не сообщает RUSTSEC-2026-0190 или результат разбора записан. |
### 90 дн.

| Приоритет | ID | Действие | Тип | Условие закрытия |
|---|---|---|---|---|
| P3 | QSI-2026-06464 | Внесите использования BLS12-381, ECDSA, Ed25519, Schnorr (BIP-340), sr25519 в the wallet's transaction signing в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06456 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06457 | Внесите использования Ed25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06458 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06459 | Внесите использования ECDSA в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06460 | Внесите использования Ed25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06462 | Внесите использования ECDH в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P3 | QSI-2026-06463 | Внесите использования X25519 в source code в криптографическую инвентаризацию с владельцем и оценкой срока жизни данных; обеспечьте криптографическую гибкость (идентификаторы алгоритмов, конфигурируемые провайдеры). | краткосрочное снижение риска | Существует запись инвентаризации с владельцем, сроком жизни и целевым алгоритмом. |
| P4 | QSI-2026-06464 | Запланируйте миграцию BLS12-381, ECDSA, Ed25519, Schnorr (BIP-340), sr25519 на ? (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ? или гибридной схемы. |
| P4 | QSI-2026-06456 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06457 | Запланируйте миграцию Ed25519 на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06458 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06459 | Запланируйте миграцию ECDSA на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06460 | Запланируйте миграцию Ed25519 на ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование ML-DSA (FIPS 204) или SLH-DSA (FIPS 205), в гибридной/композитной форме, где это поддерживает экосистема или гибридной схемы. |
| P4 | QSI-2026-06462 | Запланируйте миграцию ECDH на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-06463 | Запланируйте миграцию X25519 на Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH (или гибридную схему) после появления поддержки в библиотеках, протоколах и у контрагентов. | устранение первопричины | Повторный аудит показывает использование Гибридное установление ключей с ML-KEM (FIPS 203), например X25519MLKEM768 в TLS 1.3 или mlkem768x25519-sha256 в SSH или гибридной схемы. |
| P4 | QSI-2026-06467 | Замените bincode поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | bincode заменён или решение зафиксировано. |
| P4 | QSI-2026-06479 | Обновите зависимости разработки и сборки из доказательства. | устранение первопричины | Сканирование не сообщает бюллетеней для пакетов инструментов, либо оставшиеся зафиксированы. |
| P4 | QSI-2026-06461 | Задокументируйте, зачем предоставляется SHA-1, и проверьте вызывающий код. | устранение первопричины | Вызывающий код проверен; SHA-1 оставлен только там, где его требует протокол. |
| P4 | QSI-2026-06471 | Замените derivative поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | derivative заменён или решение зафиксировано. |
| P4 | QSI-2026-06473 | Замените paste поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | paste заменён или решение зафиксировано. |
| P4 | QSI-2026-06474 | Замените proc-macro-error поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | proc-macro-error заменён или решение зафиксировано. |
| P4 | QSI-2026-06478 | Замените unsafe-libyaml поддерживаемой альтернативой или зафиксируйте, почему он остаётся. | устранение первопричины | unsafe-libyaml заменён или решение зафиксировано. |

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
20. NIST SP 800-131A Rev. 2 — Transitioning the Use of Cryptographic Algorithms and Key Lengths — NIST. <https://csrc.nist.gov/pubs/sp/800/131/a/r2/final> (final (2019))
21. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
22. OSV advisory GHSA-3288-p39f-rqpv — OSV.dev. <https://osv.dev/vulnerability/GHSA-3288-p39f-rqpv> (modified 2026-09-10T03:50:59.332505686Z)
23. OSV advisory GHSA-7gcf-g7xr-8hxj — OSV.dev. <https://osv.dev/vulnerability/GHSA-7gcf-g7xr-8hxj> (modified 2026-09-10T03:51:10.897685062Z)
24. OSV advisory GHSA-cq8v-f236-94qc — OSV.dev. <https://osv.dev/vulnerability/GHSA-cq8v-f236-94qc> (modified 2026-09-10T03:50:43.958966498Z)
25. OSV advisory GHSA-qwgh-2vcv-g2f7 — OSV.dev. <https://osv.dev/vulnerability/GHSA-qwgh-2vcv-g2f7> (modified 2026-08-19T19:30:06.686866977Z)
26. OSV advisory GHSA-r6v5-fh4h-64xc — OSV.dev. <https://osv.dev/vulnerability/GHSA-r6v5-fh4h-64xc> (modified 2026-09-10T03:50:35.583241382Z)
27. OSV advisory RUSTSEC-2024-0370 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0370> (modified 2026-06-07T20:00:03.923932350Z)
28. OSV advisory RUSTSEC-2024-0388 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0388> (modified 2024-11-10T13:34:40Z)
29. OSV advisory RUSTSEC-2024-0436 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0436> (modified 2026-01-27T22:03:15.694766Z)
30. OSV advisory RUSTSEC-2024-0449 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2024-0449> (modified 2026-10-12T11:45:02.518189315Z)
31. OSV advisory RUSTSEC-2025-0141 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2025-0141> (modified 2026-01-16T11:07:28.867553Z)
32. OSV advisory RUSTSEC-2026-0190 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0190> (modified 2026-06-29T14:15:03.650725453Z)
33. OSV advisory RUSTSEC-2026-0387 — OSV.dev. <https://osv.dev/vulnerability/RUSTSEC-2026-0387> (modified 2026-10-24T03:45:02.365137418Z)
34. OSV.dev — open-source vulnerability database and API — Open Source Security Foundation. <https://osv.dev/> (the database QSI queries for each exactly pinned version; every advisory id in a finding resolves at https://osv.dev/vulnerability/<id>)
35. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
36. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
37. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Приложения: Криптографическая инвентаризация

| Алгоритм | Параметр | Библиотека | Квантовый статус | Классический статус | Количество | Мест | Примеры |
|---|---|---|---|---|---|---|---|
| RC4 |  |  | слаб классически | взломан | 2 | 2 | trezor-crypto/crypto/rc4.c; trezor-crypto/include/TrezorCrypto/rc4.h |
| RIPEMD-160 | RIPEMD-160 |  | слаб классически | устаревающий | 3 | 3 | rust/tw_hash/src/ripemd.rs:12; trezor-crypto/crypto/ripemd160.c; trezor-crypto/include/TrezorCrypto/ripemd160.h |
| SHA-1 | SHA-1 |  | слаб классически | устаревший | 1 | 1 | rust/tw_hash/src/sha1.rs |
| AES-192 | AES-192 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/Keystore/AESParameters.h:23 |
| AES-256 | AES-256 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | src/Keystore/AESParameters.h:24 |
| ChaCha20-Poly1305 | ChaCha20-Poly1305 |  | сниженный запас (Гровер), одобрен | допустимо | 2 | 2 | trezor-crypto/crypto/chacha20poly1305/chacha20poly1305.c:13; trezor-crypto/include/TrezorCrypto/chacha20poly1305/chacha20poly1305.h:13 |
| HMAC |  |  | сниженный запас (Гровер), одобрен | допустимо | 7 | 7 | rust/tw_hash/src/ffi.rs:110; rust/tw_hash/src/hmac.rs:5; rust/tw_keypair/src/ecdsa/canonical.rs:25 |
| HMAC | HMAC-SHA-256 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | rust/tw_hash/src/hmac.rs:8 |
| PBKDF2 |  |  | сниженный запас (Гровер), одобрен | допустимо | 2 | 2 | trezor-crypto/crypto/pbkdf2.c; trezor-crypto/include/TrezorCrypto/pbkdf2.h |
| Poly1305 |  |  | сниженный запас (Гровер), одобрен | допустимо | 3 | 3 | trezor-crypto/crypto/chacha20poly1305/poly1305-donna.c; trezor-crypto/include/TrezorCrypto/chacha20poly1305/poly1305-donna-32.h; trezor-crypto/include/TrezorCrypto/chacha20poly1305/poly1305-donna.h |
| SHA-2 | SHA-512 |  | сниженный запас (Гровер), одобрен | допустимо | 4 | 4 | rust/tw_hash/src/sha2.rs:18; rust/tw_keypair/src/ed25519/mod.rs:20; rust/tw_keypair/src/ed25519/modifications/cardano/mod.rs:5 |
| SHA-3 | SHA3-512 |  | сниженный запас (Гровер), одобрен | допустимо | 1 | 1 | rust/tw_hash/src/sha3.rs:21 |
| scrypt |  |  | сниженный запас (Гровер), одобрен | допустимо | 2 | 2 | trezor-crypto/crypto/scrypt.c; trezor-crypto/include/TrezorCrypto/scrypt.h |
| AES-128 | AES-128 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 1 | 1 | src/Keystore/AESParameters.h:22 |
| BLAKE2 |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 9 | 9 | rust/tw_hash/src/blake2.rs; trezor-crypto/crypto/blake2b.c; trezor-crypto/crypto/blake2s.c |
| Keccak-256 | Keccak-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 38 | 38 | rust/chains/tw_greenfield/src/context.rs:22; rust/chains/tw_native_evmos/src/context.rs:21; rust/chains/tw_native_injective/src/context.rs:21 |
| SHA-2 | SHA-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 2 | 2 | rust/tw_hash/src/hmac.rs:6; rust/tw_hash/src/sha2.rs:14 |
| SHA-2 | SHA-224 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | устаревающий | 1 | 1 | rust/tw_hash/src/sha2.rs:10 |
| SHA-2 |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 2 | 2 | trezor-crypto/crypto/sha2.c; trezor-crypto/include/TrezorCrypto/sha2.h |
| SHA-3 | SHA3-256 |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 1 | 1 | rust/tw_hash/src/sha3.rs:17 |
| SHA-3 |  |  | Гровер: допустимо по NIST, ниже рекомендаций ECCG/ANSSI | допустимо | 5 | 5 | trezor-crypto/crypto/ed25519-donna/ed25519-sha3.c; trezor-crypto/crypto/sha3.c; trezor-crypto/include/TrezorCrypto/ed25519-donna/ed25519-hash-custom-sha3.h |
| Crypto library | 0.13.1 | k256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | rust/Cargo.lock |
| Crypto library | 0.13.2 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | rust/Cargo.lock |
| Crypto library | 0.16.6 | ecdsa (python-ecdsa) | н/п | допустимо | 2 | 2 | rust/Cargo.lock; rust/tw_keypair/Cargo.toml |
| Crypto library | 0.27.0 | secp256k1 (secp256k1 bindings) | н/п | допустимо | 4 | 4 | rust/Cargo.lock; rust/chains/tw_bitcoin/Cargo.toml; rust/frameworks/tw_utxo/Cargo.toml |
| Crypto library | 4.1.3 | curve25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | rust/Cargo.lock |
| Crypto library | 0.13.0 | p256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | rust/tw_keypair/Cargo.toml |
| Crypto library | 0.13.0 | k256 (RustCrypto elliptic curves) | н/п | допустимо | 1 | 1 | rust/tw_keypair/Cargo.toml |
| Crypto library | 4.1 | curve25519-dalek (ed25519-dalek) | н/п | допустимо | 1 | 1 | rust/tw_keypair/Cargo.toml |
| BLS12-381 | BLS signatures |  | уязвим (Шор) | допустимо | 1 | 1 | src/proto/Filecoin.proto:3 |
| ECDH |  |  | уязвим (Шор) | допустимо | 1 | 1 | trezor-crypto/crypto/bip32.c:710 |
| ECDSA | secp256k1 |  | уязвим (Шор) | допустимо | 135 | 135 | include/TrustWalletCore/TWCurve.h:14; rust/chains/tw_binance/src/compiler.rs:17; rust/chains/tw_binance/src/context.rs:7 |
| ECDSA | P-256 |  | уязвим (Шор) | допустимо | 4 | 4 | rust/tw_keypair/src/ecdsa/nist256p1/private.rs:9; rust/tw_keypair/src/ecdsa/nist256p1/public.rs:8; src/proto/NEO.proto:3 |
| ECDSA |  |  | уязвим (Шор) | допустимо | 8 | 8 | src/Ethereum/MessageSigner.cpp:91; src/Ethereum/MessageSigner.h:36; src/PrivateKey.cpp:262 |
| ECDSA | secp256k1, P-256 |  | уязвим (Шор) | допустимо | 3 | 3 | src/proto/EOS.proto:3; src/proto/Sui.proto:7; src/proto/Tezos.proto:3 |
| ECDSA | secp256k1, transparent addresses |  | уязвим (Шор) | допустимо | 1 | 1 | src/proto/Zcash.proto:3 |
| Ed25519 | Ed25519 |  | уязвим (Шор) | допустимо | 67 | 67 | rust/chains/tw_aptos/src/address.rs:40; rust/chains/tw_aptos/src/signer.rs:25; rust/chains/tw_aptos/src/transaction.rs:14 |
| Ed25519 |  |  | уязвим (Шор) | допустимо | 19 | 19 | src/proto/Aeternity.proto:3; src/proto/Aion.proto:3; src/proto/Algorand.proto:3 |
| Ed25519 | BIP32-Ed25519 |  | уязвим (Шор) | допустимо | 1 | 1 | src/proto/Cardano.proto:3 |
| Ed25519 | BLAKE2b variant |  | уязвим (Шор) | допустимо | 1 | 1 | src/proto/Nano.proto:3 |
| Schnorr (BIP-340) | secp256k1, Taproot |  | уязвим (Шор) | допустимо | 2 | 2 | src/proto/Bitcoin.proto:3; src/proto/BitcoinV2.proto:3 |
| X25519 | X25519 |  | уязвим (Шор) | допустимо | 3 | 3 | trezor-crypto/crypto/bip32.c:504; trezor-crypto/crypto/ed25519-donna/ed25519.c:256; trezor-crypto/include/TrezorCrypto/ed25519.h:27 |
| X25519 |  |  | уязвим (Шор) | допустимо | 6 | 6 | trezor-crypto/crypto/ed25519-donna/curve25519-donna-32bit.c; trezor-crypto/crypto/ed25519-donna/curve25519-donna-helpers.c; trezor-crypto/crypto/ed25519-donna/curve25519-donna-scalarmult-base.c |
| sr25519 |  |  | уязвим (Шор) | допустимо | 2 | 2 | src/proto/Polkadot.proto:3; src/proto/Polymesh.proto:7 |

_Длинные списки здесь сгруппированы; полный список по файлам — в JSON-версии отчёта, подписанной тем же ключом._

## Приложения: Входные файлы

| Файл | Размер | SHA-256 | Маскирования |
|---|---|---|---|
| include/TrustWalletCore/TWAES.h | 1929 | `6634415205b11d3e43be88c4fdf6c64a9c48c4e6a125ad2e92c619ec3729d430` | 0 |
| include/TrustWalletCore/TWAESPaddingMode.h | 413 | `1053eef67a8680b5e6c95e543ed73034a776ca83b865b0987bfb8e3a07077124` | 0 |
| include/TrustWalletCore/TWAccount.h | 2748 | `1d03ca17815f16bbc4c6754e979f45b251aae42330a37263e5209ea777fd4b58` | 0 |
| include/TrustWalletCore/TWAnyAddress.h | 6664 | `e2ee9b081d9faaddc65f04911ba6a4f6e6ae0ef7b096649b9dbc7e77983ce214` | 0 |
| include/TrustWalletCore/TWAnySigner.h | 1887 | `ccc575e1da55a7e5461330feee3741b338d906fed79671f43855a374559407a8` | 0 |
| include/TrustWalletCore/TWAsnParser.h | 560 | `c352b5bd2710a3771469acb2ff0cc06fcc5721ca2d1f24f0b53fbce49ed93e79` | 0 |
| include/TrustWalletCore/TWBase.h | 1910 | `5a13bc85971cf75e6ba1b7f4b78bc560f5cf564f08849a1883f7b3d4d6318ef1` | 0 |
| include/TrustWalletCore/TWBase32.h | 1734 | `7d44911d14e1977cabee8f5aba679a8b8f0c22beef0bca4e40ab8c5cd60ac7c6` | 0 |
| include/TrustWalletCore/TWBase58.h | 1443 | `2ba4e447e29dd54c8f6eb804e9fbe700a3f9c3733bee097dded965455abb70be` | 0 |
| include/TrustWalletCore/TWBase64.h | 1339 | `90a8fc7abe2ae896d91c0d7dd2017add3a780760f1b7d3aa8d6bd1587072ee27` | 0 |
| include/TrustWalletCore/TWBech32.h | 1492 | `1303a795170973bb5d1a6c8e63e6282fc610d53fb13ab9f0942fafbc487c4ed7` | 0 |
| include/TrustWalletCore/TWBitcoinAddress.h | 2990 | `09532e54416cc5167d828b98f39769587c91b58c26ae0ee698b4bdc96f5c8f63` | 0 |
| include/TrustWalletCore/TWBitcoinMessageSigner.h | 1613 | `80f4127d742d55c5d190a2a54e43f57b2195a5e42b19a7188ffd5c42ffa2f01e` | 0 |
| include/TrustWalletCore/TWBitcoinScript.h | 8008 | `dd2b468b5b64923e1d551049c0d8eb4337f9d1885ae980c894820c579904cf5d` | 0 |
| include/TrustWalletCore/TWBitcoinSigHashType.h | 924 | `c3a64d582e4c5b23aa2158dbc187342e752054f012c17dd7b80a96544c978fbc` | 0 |
| include/TrustWalletCore/TWBlockchain.h | 2111 | `bab1ed4b6ede82231496096c2ed1242434f2c5f3477d51bebeabc1abd3e04f3d` | 0 |
| include/TrustWalletCore/TWCardano.h | 2082 | `599eecb92952fcb180657f87a17576839b1e1a7cb21974f3c4e7c9b8133c41bc` | 0 |
| include/TrustWalletCore/TWCoinType.h | 10805 | `f853075b58c31ba3c7973d8d746ef43da6883f7780f93e9bf626792eef9d8222` | 0 |
| include/TrustWalletCore/TWCoinTypeConfiguration.h | 2243 | `d11fff9709e978a6494bd2f54ed31eff4012f3526a60da7514122d95d20d9be1` | 0 |
| include/TrustWalletCore/TWCryptoBox.h | 1621 | `7bcb6717aa3da2cc74040f2fd53e998e1e4d6ab80d65c690b01925bc16591ca4` | 0 |
| include/TrustWalletCore/TWCurve.h | 610 | `212236e77a6b379beb9c0c9dd149d1ae9574f6a0cd986fa4931b5d03a38fc664` | 0 |
| include/TrustWalletCore/TWData.h | 4962 | `28e07eca5e013a4ad1c953eb25be0709d88bbf8d5df45d905ed95f9ee2b3df01` | 0 |
| include/TrustWalletCore/TWDataVector.h | 1814 | `43c71b6cdaafd7bc897711b960b64d4a426e64244dd922c2dc597762276a9321` | 0 |
| include/TrustWalletCore/TWDerivation.h | 1070 | `5faceb271bebca8b1a86f92f2a6ef135b008cdf1018fc88b43e0578da40767ed` | 0 |
| include/TrustWalletCore/TWDerivationPath.h | 3495 | `743f895526d05a6cc9078a4536c920757340450e078e0e7dc4f7c3f51826f0a2` | 0 |
| include/TrustWalletCore/TWDerivationPathIndex.h | 1540 | `bcbe7d8300a9bc2ee346ee07bff5284abd9c0c990c5c415f9449c0c3a9b17ec5` | 0 |
| include/TrustWalletCore/TWEthereumAbi.h | 4847 | `df0cd4cf8bf43047f910697db0e0d47b44954300710d900ee7a77539acf7328f` | 0 |
| include/TrustWalletCore/TWEthereumAbiFunction.h | 19832 | `9b4c65cb131ad8362e732ab626bd88751d71188b13be2de7f9efb87e33e71f9f` | 0 |
| include/TrustWalletCore/TWEthereumAbiValue.h | 3850 | `17ad5438cde2093199b4ffe45693c1acc830710fe367fc5d7d0920ec4aeb917c` | 0 |
| include/TrustWalletCore/TWEthereumMessageSigner.h | 3518 | `256598effe95266ab9373bea571f49c41154c3168b8894d8f3448e9ff461ff93` | 0 |
| include/TrustWalletCore/TWEthereumRlp.h | 608 | `05f197ccd895ded8b0278d3c2be507973915a0a22df4c1dcb3855cb5d3ff5d2a` | 0 |
| include/TrustWalletCore/TWFIOAccount.h | 940 | `7511fdae6106c1cf5e8e3affc82537dfe00ac7b340cc7c7dc637673435d41eea` | 0 |
| include/TrustWalletCore/TWFilecoinAddressConverter.h | 972 | `31c1c99a213200ed2c1d465b24730a29f1489b1eb9b47841770a998348cc2b38` | 0 |
| include/TrustWalletCore/TWFilecoinAddressType.h | 322 | `170e71cddc47e559dd01dfeb33ae55d1f92e5836b7b89a039acf8114e4ee102a` | 0 |
| include/TrustWalletCore/TWFiroAddressType.h | 305 | `6666eed5f90f01a88c7641205aed9ff472fb990d416b2845413b6677d80d6af2` | 0 |
| include/TrustWalletCore/TWGroestlcoinAddress.h | 2112 | `50b9f73912b01c3b34ee7462c5e5e5ffca8b77f4b270172fd8f6deaa06a22d4c` | 0 |
| include/TrustWalletCore/TWHDVersion.h | 1488 | `37e6b39d7969d280a025df31da35bbdac699692ce0a2cf3f18d82d0628513a1a` | 0 |
| include/TrustWalletCore/TWHDWallet.h | 12217 | `4f1fff90e5ff901faa73d9f8737da1b7b039faa77e1afe8e387268dd99a64dc8` | 0 |
| include/TrustWalletCore/TWHash.h | 4681 | `b106f47bc687c8dd6ae621e882485c20e6b4c38ccb18f135b22e33669d72964e` | 0 |
| include/TrustWalletCore/TWLiquidStaking.h | 521 | `5a189b9a88237e676a81ece03b0273ef9e78ea6795a326968c15968ab19bf451` | 0 |
| include/TrustWalletCore/TWMnemonic.h | 1172 | `19a40124bccf0fda6e9ab64689bfffc1d994f8013abdb1bb25adc33842835c29` | 0 |
| include/TrustWalletCore/TWNEARAccount.h | 976 | `5e262aeb025e226d32faeae2cbfdb9286b2dae3a2dff24259351c05a9fe4e81a` | 0 |
| include/TrustWalletCore/TWNervosAddress.h | 2090 | `5648119d8c516f7488b5d9f652364847a13bab55467bc3cbb4e3d19aa9bed1c8` | 0 |
| include/TrustWalletCore/TWPBKDF2.h | 1300 | `a5fd8f8663d63b49a6fae22a015f4ae608e7ca78acfb3baeca8bae0fd04a242f` | 0 |
| include/TrustWalletCore/TWPrivateKey.h | 5657 | `eb8ceb2b7fa40cd808f6a970809596a41d16edb1a0183c0028ff83960bb9ba76` | 0 |
| include/TrustWalletCore/TWPrivateKeyType.h | 433 | `cbb17afdfd199a905b85708ca280650241c29f39eb83635437d9733e0e1e5c59` | 0 |
| include/TrustWalletCore/TWPublicKey.h | 5175 | `90bd105679ee07427ca1b73befc535556a9574f8b186cc8c134bfc50de823449` | 0 |
| include/TrustWalletCore/TWPublicKeyType.h | 550 | `fd81f37d4780be6ae07e5141fe44b4df21d552bd6bf1dfbdbb7f192ac47f816a` | 0 |
| include/TrustWalletCore/TWPurpose.h | 719 | `6a54ecba472ad88b62a51dc73063a6b8f966f9860f79df92ac7e3ceb933449ce` | 0 |
| include/TrustWalletCore/TWSegwitAddress.h | 3142 | `da4eb76967e536aa400c169be20220ce79f71f3cad709a92d280f362729bed99` | 0 |
| include/TrustWalletCore/TWSolanaAddress.h | 1951 | `7c19746a3b26ce897057f30240b839db7ca843b8397ea01fd9226cae8090eb0d` | 0 |
| include/TrustWalletCore/TWStarkExMessageSigner.h | 1454 | `7522f076785b9faeefeedfa62f3b34f350234126aaab3d87ee2eed7a8fcbbbc0` | 0 |
| include/TrustWalletCore/TWStarkWare.h | 802 | `18b49d9ece1c98388b9bae6f805f80b9222f9123c09bcc045f64ccb6edf4d9fe` | 0 |
| include/TrustWalletCore/TWStellarMemoType.h | 380 | `d19b00c08c8b3e33d1864c4a0bec8aa1d236f6efc5ead048e45f53cc8cb144d8` | 0 |
| include/TrustWalletCore/TWStellarPassphrase.h | 592 | `59764b0f01d6eb1c34bcb0d90b614f04e98489cc4abdf54227452bfb68205dbd` | 0 |
| include/TrustWalletCore/TWStellarVersionByte.h | 435 | `b00c077ce510dd7fc411938b5e8dd8040dccbd1332d6000b2fd0c71953f7d1e0` | 0 |
| include/TrustWalletCore/TWStoredKey.h | 20671 | `0077685c504088b0b8a54db5f5dbff492e4b18c8cbedd12f7f0e3dad27fff565` | 0 |
| include/TrustWalletCore/TWStoredKeyEncryption.h | 353 | `b8841456c891b361d235d7b1c114d0b74f5b9ed09b245674945a2e9a245022f7` | 0 |
| include/TrustWalletCore/TWStoredKeyEncryptionLevel.h | 722 | `1c6e48a113d25767108e75f7ef365d52f3c92fbc0dccafc098af7443df5266c4` | 0 |
| include/TrustWalletCore/TWString.h | 2246 | `57e9839fa734c64b046c075b9a0461941fdb90a037d24f3158117d70dcf97931` | 0 |
| include/TrustWalletCore/TWTHORChainSwap.h | 500 | `3c5b67006fd687d021e150bbe23812d06c6cc0142c1de89b8763a4ea10d15557` | 0 |
| include/TrustWalletCore/TWTezosMessageSigner.h | 2090 | `46d56cdaa1920a3a1b6e91aea72c664d7a73bf9e92ce12e3d777ef77d861645f` | 0 |
| include/TrustWalletCore/TWTransactionCompiler.h | 2215 | `715ec3e8dadb56af0c995f8b833eb49d19b9da36b95685b88d5c28a7ce25ae33` | 0 |
| include/TrustWalletCore/TWTransactionDecoder.h | 588 | `29f860ac7b86efe9b9114ebc558bc9f64e8b5afa9b61bbc843aabd1cf32d789e` | 0 |
| include/TrustWalletCore/TWTransactionUtil.h | 601 | `b22061b6ae0c940cac436f5a4ebe5721882b2ba1b2def478fe1387ca91aef4c8` | 0 |
| include/TrustWalletCore/TWTronMessageSigner.h | 1453 | `14c33557e9c1e47d5429741562187465a1f47db824671ceb35a8c4a43e91e3ac` | 0 |
| include/TrustWalletCore/TWWebAuthn.h | 1358 | `d2c9ae4eccb8ef0dd04fb80495947a4645484cda331e6d4a400490ade7eeefd5` | 0 |
| rust/Cargo.lock | 68307 | `2e0a91cecf4cc5305e000af96b3dd9c4baefe0171cf736bf06e59f016e5fd337` | 0 |
| rust/Cargo.toml | 1415 | `7c3b882a782ae660e8bf837806688a68ec9650d9b3475f3c68f6300d6e1649b6` | 0 |
| rust/chains/tw_aptos/Cargo.toml | 818 | `4d5e91bd5fe9ea94aff23cea85468343a0ebdb43b1cd7759a2b3b3df81f8ce4a` | 0 |
| rust/chains/tw_aptos/src/address.rs | 4647 | `06c7819770d2fa99fe53ea4913e9f52531ab549fac9f775d8f8d1bfda6e809cb` | 0 |
| rust/chains/tw_aptos/src/aptos_move_packages.rs | 7004 | `f487d19c265ec4626e6c613996cb8b81fcf3851d82ecba33df6be8934f5a0543` | 0 |
| rust/chains/tw_aptos/src/aptos_move_types.rs | 6096 | `5d3967d7fde72e6558ed409c78078c87c3263bda0666461e8e8c427d34f672b9` | 0 |
| rust/chains/tw_aptos/src/compiler.rs | 2810 | `36940166b8909b10d3a8344caa2f72cbd894764af46b6775e6cc279af6d84f07` | 0 |
| rust/chains/tw_aptos/src/constants.rs | 392 | `72785d4e6b8d704e1444e27a43fdaa8ad2c4ea1ef05b0eba286370915c16454d` | 0 |
| rust/chains/tw_aptos/src/entry.rs | 3237 | `60a7ccc5dc198987b0e7c628b2da968f0d764cb2fc70f4d583193c67727896fd` | 0 |
| rust/chains/tw_aptos/src/lib.rs | 371 | `a7247090a93224a099e6c3541d8fd0176f36500cc823d5cfb29dcf87a64e24b5` | 0 |
| rust/chains/tw_aptos/src/liquid_staking.rs | 5199 | `def51be3ecd3177b39a297bd580323df15e23f92ad4bc37e4389d018a2500a1f` | 0 |
| rust/chains/tw_aptos/src/modules/mod.rs | 104 | `3e38c1b77a2e2f40e7b92d1fe60fd0937e20d810c98f0ae4d70c00fab11bc88c` | 0 |
| rust/chains/tw_aptos/src/modules/transaction_util.rs | 1384 | `52ba6eaa71eadd5eaf46bc9d9682ed17e241861d299ab49d06d363f907b58bf1` | 0 |
| rust/chains/tw_aptos/src/nft.rs | 5687 | `fe6c35dfad875d9924aa9a0f3adf72f19b9d254e490a7ee482968a4239948bd0` | 0 |
| rust/chains/tw_aptos/src/serde_helper/mod.rs | 165 | `9601ff00a1ce7a3a970b2afc8dda5a4e2e8c73ed51a86020930a07ce3c308535` | 0 |
| rust/chains/tw_aptos/src/serde_helper/vec_bytes.rs | 786 | `c449aef3d45e27f1cfa16d7cdd4a1c3521e592486917d6e40290e444d19f19c4` | 0 |
| rust/chains/tw_aptos/src/signer.rs | 1514 | `49d8bc158ea418df728cff339e42900e856016f1286b8b904a6e3f2a26236898` | 0 |
| rust/chains/tw_aptos/src/transaction.rs | 6650 | `67ef9ba663df36909bef7694c062145eb60233ad64ff5982548d600b12a40afe` | 0 |
| rust/chains/tw_aptos/src/transaction_builder.rs | 10507 | `ee0758e56d1a6cb95b87c28b62ef97cdca4f5fbc37af5b0a55fea4e6af2951af` | 0 |
| rust/chains/tw_aptos/src/transaction_payload.rs | 24596 | `209ab3584df30e7b5aaf9188422b1cb6fa6a56ceebaebca658325f4dea96f028` | 0 |
| rust/chains/tw_binance/Cargo.toml | 671 | `fc8d81d4b4c4bf0d11a27856ee099b86209869b26d86a13488637ab3a5d50566` | 0 |
| rust/chains/tw_binance/src/address.rs | 2744 | `80bf15bc8141b7a31ab939e9274232f7ddc20b3826cbc053d276d7486dcc58a3` | 0 |
| rust/chains/tw_binance/src/amino.rs | 5029 | `076d9583a6e3fe807337e9d32d38011b4049198af1bfb04b3bc8b96968cadd8e` | 0 |
| rust/chains/tw_binance/src/compiler.rs | 3728 | `90c4a829199bea64862007a15194716a45683b75238c2b322c4ba94cc8a30af5` | 0 |
| rust/chains/tw_binance/src/context.rs | 714 | `1a2f4c49353c96fcead85ac7ee54fd513a3f33d23d40538e5e2c0aff6ca8f518` | 0 |
| rust/chains/tw_binance/src/entry.rs | 3131 | `6af25885fd7e5e9fbebc938767af4dd963a50dbc5e84e4293731ca930e24e86b` | 0 |
| rust/chains/tw_binance/src/lib.rs | 233 | `fbca6492fc7ee2fa4ab028120d802ad40653bcc8e956d10e7add8880851e9272` | 0 |
| rust/chains/tw_binance/src/modules/mod.rs | 161 | `485c9a078cc930be1b5a7c06f5ba85dcf82dcd26829e6d5fe318fcb21e3a5476` | 0 |
| rust/chains/tw_binance/src/modules/preimager.rs | 770 | `d8e14e126888dd32fe09073b53c4caa96cccb8b0eff63b43b3ffbbdd33877ba4` | 0 |
| rust/chains/tw_binance/src/modules/serializer.rs | 2264 | `87378bb1ddc65fe34703af62c8b9aa637ae7e23ad9c49d7b19d8ce91b58cdca4` | 0 |
| rust/chains/tw_binance/src/modules/tx_builder.rs | 1758 | `c773d6b1cfec5e3596272966ef41223fd9172254d31ef3574dbf3f20e86602d6` | 0 |
| rust/chains/tw_binance/src/modules/wallet_connect/connector.rs | 2114 | `249227f2a6d1837e6bc855e929a57f250bff7e1f58cc2c6c8f81b943ebe1bdce` | 0 |
| rust/chains/tw_binance/src/modules/wallet_connect/mod.rs | 112 | `7e3163633e9b4ee9852344753187983ce30564247aaf142a24b19d6d0ad75d73` | 0 |
| rust/chains/tw_binance/src/modules/wallet_connect/types.rs | 275 | `5a7b2392fe9f1e216befcd6bdd7f0a4b90b54fb5acdc8e35ef70a1da397ee870` | 0 |
| rust/chains/tw_binance/src/signature.rs | 169 | `f4fc6f2f8d370db49df6ccd6d9fce4bfb45887d7a42dbeb42926125c37f33a2a` | 0 |
| rust/chains/tw_binance/src/signer.rs | 2436 | `fa137311ec0c2bb272584a66b345be718a6f9e9f8543bb649c05d5b1e13c8c73` | 0 |
| rust/chains/tw_binance/src/transaction/message/htlt_order.rs | 6296 | `695bd6940a3d850e5d3211e3716dcba4485a05804ef4ea2cdc4dd767fdc07913` | 0 |
| rust/chains/tw_binance/src/transaction/message/mod.rs | 9526 | `930ad213d715147e12c2c494d870e691ec589d7ccdb59dfeacd22b309630fafe` | 0 |
| rust/chains/tw_binance/src/transaction/message/send_order.rs | 2904 | `8c252a24f9369f0ae799cf354273863b75e6249e3288993938bbd6836fed40b8` | 0 |
| rust/chains/tw_binance/src/transaction/message/side_chain_delegate.rs | 9786 | `49c57fcadd5746c40971dcb6c5fae14ee5ed65ae101d36af4dd9691632011381` | 0 |
| rust/chains/tw_binance/src/transaction/message/time_lock_order.rs | 4588 | `90afb05194526b37d7d849e2496bee854db8bae453ef2faa9524e6dd63e51dd8` | 0 |
| rust/chains/tw_binance/src/transaction/message/trade_order.rs | 4237 | `5c93bd940ee4dd9bdbfd453f1feeba533c98cb9b3feec8f7dc0b84ce60b78341` | 0 |
| rust/chains/tw_binance/src/transaction/message/transfer_out_order.rs | 2055 | `a60e304a5144c9ad6eb232541979044769aea8243092cb3c4651ac19ba5fe3da` | 0 |
| rust/chains/tw_binance/src/transaction/mod.rs | 1092 | `64c6c8b729b3304338292fb741ee17199613db975a74247ed80ce5764d80d359` | 0 |
| rust/chains/tw_bitcoin/Cargo.toml | 819 | `9cc07a925abf6e8563ecc7ac13318f955af066779661ba219f63cc7203876e8d` | 0 |
| rust/chains/tw_bitcoin/src/babylon/conditions.rs | 5177 | `01f12061f661c4ee1849a6df69869c2418e517c8651eba3b4ce889f787638d1f` | 0 |
| rust/chains/tw_bitcoin/src/babylon/mod.rs | 214 | `9beabceb32b2776d88773932a1ce547e52268d0511c467eeda62f727dfdf2033` | 0 |
| rust/chains/tw_bitcoin/src/babylon/multi_sig_ordered.rs | 4689 | `2a413914b8fa3eaef6a5c830be6d9729d285efba927fc20ca57b903022bbc8a5` | 0 |
| rust/chains/tw_bitcoin/src/babylon/proto_builder/mod.rs | 2784 | `a48c956227e747782de18332f79119786ac7472c2d144f73639e5ad7e30342d6` | 0 |
| rust/chains/tw_bitcoin/src/babylon/proto_builder/output_protobuf.rs | 2587 | `4c4bb19c554362727c29177a766680b9e80991ca7162cee2df95730f4e5c1021` | 0 |
| rust/chains/tw_bitcoin/src/babylon/proto_builder/utxo_protobuf.rs | 3418 | `dad68a741dfe07e9f7d502af7667fa19bfd2840cd4d97bf67c28117395ae0a15` | 0 |
| rust/chains/tw_bitcoin/src/babylon/spending_data.rs | 1917 | `157482f44455299c5a667087dd7a9be02214b9183066123ccea53e832ab96d60` | 0 |
| rust/chains/tw_bitcoin/src/babylon/spending_info.rs | 6031 | `50eecf25f72d0a93ccfd0cf2b8778c724c4522135c03325720ffcbfcc3374fd7` | 0 |
| rust/chains/tw_bitcoin/src/babylon/tx_builder/mod.rs | 548 | `9e6cce6ce17c21b2abdb8c5e0a824c58d3cb4e1ce6626e790d6c63a54029e4d7` | 0 |
| rust/chains/tw_bitcoin/src/babylon/tx_builder/output.rs | 3024 | `e72128225ffe2bc1b5c8a166814c39652b7d8f725f1d09b34484a4e4c464ca43` | 0 |
| rust/chains/tw_bitcoin/src/babylon/tx_builder/utxo.rs | 4988 | `2275c9b64d8817adfe1c6f83f89942ce79d2b1534e5795dcfd694ad44f16f431` | 0 |
| rust/chains/tw_bitcoin/src/context.rs | 2322 | `d44b5fc6437750d62ce9012690ce544954c40aef88023ae6258725365c48aabb` | 0 |
| rust/chains/tw_bitcoin/src/entry.rs | 3314 | `f1ce9b38618a05e025e71991e4ed17f8987e6427841e9085f6af2e5958df9009` | 0 |
| rust/chains/tw_bitcoin/src/lib.rs | 144 | `9be99fd9238720e466bea62e2406561987d4ec8177c121081537f3baa1fce1ec` | 0 |
| rust/chains/tw_bitcoin/src/modules/compiler.rs | 7231 | `8db08529b67c8d92d11ddf3d549c3cfb11cf5fe158067cfb399f3407db87cf88` | 0 |
| rust/chains/tw_bitcoin/src/modules/mod.rs | 248 | `5f6c8a9428c75cc2c110f2861b341f20970b7326af0977cceabe5819a4a19c37` | 0 |
| rust/chains/tw_bitcoin/src/modules/planner/mod.rs | 4678 | `6c093395770027328ed6b2868dcca3cff3d3f4004c971703ae3c255c708b4a87` | 0 |
| rust/chains/tw_bitcoin/src/modules/planner/psbt_planner.rs | 4381 | `7dcb657f2488be23dfa5a5a68c06549bbc1820bd5dda603e0eb21c824cf2baf7` | 0 |
| rust/chains/tw_bitcoin/src/modules/protobuf_builder/mod.rs | 378 | `075681c04f3010a09d0a261f4e06dc68b7d6ee959ed5a7dbd1b05d850341eba2` | 0 |
| rust/chains/tw_bitcoin/src/modules/protobuf_builder/standard_protobuf_builder.rs | 2315 | `e3f5523ca4ee88b7a6d9ba3f89f22e053ba2a0c80bd52b3cdb9e39d1fcdb4e33` | 0 |
| rust/chains/tw_bitcoin/src/modules/psbt_request/mod.rs | 4216 | `a33ba76d589b730652bd4076e50dae7156fdc2b9a66765e53807b01b8817e8cc` | 0 |
| rust/chains/tw_bitcoin/src/modules/psbt_request/output_psbt.rs | 922 | `77647b9dd6be1d227533709db24b23fd094158891085ac6e0ab365bebf5cec27` | 0 |
| rust/chains/tw_bitcoin/src/modules/psbt_request/standard_psbt_request_handler.rs | 3708 | `3cb581f59a6a95c18209482149ca997ba4cc0b16b77cf2653e0b7c2df6218f1c` | 0 |
| rust/chains/tw_bitcoin/src/modules/psbt_request/utxo_psbt.rs | 7057 | `84732e6e1a406a8d72e222adf5b2d7d9cb3a92bd2da2713aaf5a064004eef06a` | 0 |
| rust/chains/tw_bitcoin/src/modules/signer.rs | 6021 | `82ce70c07fdeaf01d2bc78186aaa70215112b276a86f0270f19c49a14f9da377` | 0 |
| rust/chains/tw_bitcoin/src/modules/signing_request/mod.rs | 556 | `d124c085679570a3b88706973548b52b583c5cb7bd6179d8e809a5956041bc58` | 0 |
| rust/chains/tw_bitcoin/src/modules/signing_request/standard_signing_request.rs | 8696 | `79ea7a6f25584ea491d146b085444c9cff305bdb600e4dc48bb69616f4f02285` | 0 |
| rust/chains/tw_bitcoin/src/modules/transaction_util.rs | 1105 | `2975cdd56c5b82261e3ed8ba1115d660796c0e93cf2a6681f6af54c58cb6811d` | 0 |
| rust/chains/tw_bitcoin/src/modules/tx_builder/mod.rs | 611 | `0a6d444b51f74b9fff63ef419cfb07bb27ff72e6a24af61004a81ce5cc64c486` | 0 |
| rust/chains/tw_bitcoin/src/modules/tx_builder/output_protobuf.rs | 10140 | `f28697caefed7f9dc64ad12a49a7cfd602a3c0f1d347e77cd8cd1b9b8ce9000d` | 0 |
| rust/chains/tw_bitcoin/src/modules/tx_builder/public_keys.rs | 2415 | `6140c23d0455727f038c63821f66569b0d1eb4a40d4ec75bb16357b072ac87d1` | 0 |
| rust/chains/tw_bitcoin/src/modules/tx_builder/script_parser.rs | 4701 | `deab40ff5effc1d4671eb1077dda141b9ee3fd57c4dde56468bc39667eb705d0` | 0 |
| rust/chains/tw_bitcoin/src/modules/tx_builder/utxo_protobuf.rs | 10884 | `d010723f1f2794d803643a2cd7bd0059bc4fe2dc6ce2a8da0cdc02e84591a2ef` | 0 |
| rust/chains/tw_bitcoincash/Cargo.toml | 464 | `a38e9d154b838ac66194ef442ba9f1e2952dfacc2c9e6abec808df935aabcebd` | 0 |
| rust/chains/tw_bitcoincash/src/address.rs | 2883 | `6c12b75cc83b735aa229289c63d661cbea8abe13cc8514e24eae24ae31ea342b` | 0 |
| rust/chains/tw_bitcoincash/src/cash_address/cash_base32.rs | 2704 | `9737d5a623592b99e2c6a1b4834a1cf3dc93fd734756e42536d371f86daf04a8` | 0 |
| rust/chains/tw_bitcoincash/src/cash_address/checksum.rs | 2129 | `796b1b243e2b0c553aff813810ddcb29b398b73d4cb6308e74b6edd4ca084cb3` | 0 |
| rust/chains/tw_bitcoincash/src/cash_address/mod.rs | 8370 | `4b99161bfa30257f5f71dbd358fc5ab33620dabbeb7adb582dcb65d5b2c445fb` | 0 |
| rust/chains/tw_bitcoincash/src/cash_address/unchecked.rs | 4957 | `09114e9046ab9e8bdf32512b2a340311d9e5ee3244de2dcbbec0436c476552b9` | 0 |
| rust/chains/tw_bitcoincash/src/context.rs | 1774 | `64ddbc3b10557abf6586d10caa20e54a6e14f8a2e52363080e2e92b1bcc95908` | 0 |
| rust/chains/tw_bitcoincash/src/entry.rs | 3542 | `16b6420d749baa298f59a9d60dd73b45d6a44316d7c63d919727506c0b73da7d` | 0 |
| rust/chains/tw_bitcoincash/src/lib.rs | 149 | `d86ee2e316073e8f6826730cc374cc161013f61849ac59ef0773a72b87ac5bcf` | 0 |
| rust/chains/tw_cosmos/Cargo.toml | 356 | `9699fbe177354b353791c8b483fa738f7accbdff6e0b5fec8c4414fbf91a6728` | 0 |
| rust/chains/tw_cosmos/src/entry.rs | 3364 | `faa0f18cef073dde95d305e2c7a09ba4f83548f64a7d4535420b0ead3b2e1e9c` | 0 |
| rust/chains/tw_cosmos/src/lib.rs | 93 | `d3d5683fa38f0a50cbdcc090cc47860a6d407c71661b88a883b9830edd675c37` | 0 |
| rust/chains/tw_decred/Cargo.toml | 489 | `a536a6c3be0d32ada19107e732ae80686f775c4634d1b9cde5ae9b745e05c569` | 0 |
| rust/chains/tw_decred/src/address/mod.rs | 358 | `269f6674d0beacf6898c88c1338dcfa5baf778f0e9c371b02832ef89c6960322` | 0 |
| rust/chains/tw_decred/src/context.rs | 1391 | `7f84b2f72fdc99b2bf5728431f269fe921b51324d8cd2946d60cc015194a6479` | 0 |
| rust/chains/tw_decred/src/entry.rs | 3227 | `26f2ef8fc98e5e6a270bc4cdf5268f6036f898c525039380d8d176022561fae6` | 0 |
| rust/chains/tw_decred/src/lib.rs | 4643 | `5612d6370d78bc381fddc48e9b2ce3f1f37cc500f651774ace5b7b6dbb196ee5` | 0 |
| rust/chains/tw_decred/src/modules/decred_sighash.rs | 2432 | `7c4914f9fdc28e815f6561f5f3aaad8fc088ced2658623c279e323d89d8bb492` | 0 |
| rust/chains/tw_decred/src/modules/mod.rs | 182 | `07f0cdaf3735fe946ff8482bfdcbf768c4b210e03ccce0ffac0eb9f479f3a5cf` | 0 |
| rust/chains/tw_decred/src/modules/protobuf_builder.rs | 2302 | `255d1f5fa6247d52263ddce45b4c2a7c8bbf68dad6565988f3066f697bec8786` | 0 |
| rust/chains/tw_decred/src/modules/signing_request.rs | 6021 | `ff4fa3cdf9358a404cbb18f3bd9bd8b7c8f59b07be5302b4620474c36ada8874` | 0 |
| rust/chains/tw_decred/src/modules/transaction_builder/mod.rs | 2963 | `9aaf1fee863318332cac67a298ff375d4ec54cd6c41b52d16a4c7ce49e41ca3e` | 0 |
| rust/chains/tw_decred/src/modules/transaction_builder/output.rs | 746 | `dcf7ddc643fc7ff30de4281f2ff78d02dcf3dc1cedea63bc008d525176d60ff1` | 0 |
| rust/chains/tw_decred/src/modules/transaction_builder/utxo.rs | 1929 | `ce7697ba4235e4612a473c48a6f5814277991a47e4972aafb5e29fe2eeab0a57` | 0 |
| rust/chains/tw_decred/src/transaction.rs | 10059 | `a387d0f161fee719e79da6c5192bf501e924cc3e27e9e5ced57a12ad43751977` | 0 |
| rust/chains/tw_ethereum/Cargo.toml | 454 | `a62bc463013aa9676f9aedd6ea604d6c11fbf17a2c2ed7c7078b8f8ee069154c` | 0 |
| rust/chains/tw_ethereum/src/entry.rs | 3427 | `83716a2ffc0a6914e1d29248bf08f0433945ef01ead497d94bd21f43862e013a` | 0 |
| rust/chains/tw_ethereum/src/lib.rs | 93 | `d3d5683fa38f0a50cbdcc090cc47860a6d407c71661b88a883b9830edd675c37` | 0 |
| rust/chains/tw_greenfield/Cargo.toml | 730 | `f21ec51ad4425a86deaf043b212c1fb1e09a2e113a5c4f930c2ac9b132631ce7` | 0 |
| rust/chains/tw_greenfield/src/address.rs | 1195 | `345d7f5cfc5d566b5978c7a8c392408178141f998b0aab0f290e0f1af976cadb` | 0 |
| rust/chains/tw_greenfield/src/compiler.rs | 4689 | `66f6e7a22327358cf89f722caeac206d28f830d7e48da55e78e3922b48a2c363` | 0 |
| rust/chains/tw_greenfield/src/context.rs | 753 | `c531c858f7e81fa0a3f7418660e43c68a25d749990d140e3b9b5c801c8bd8aa0` | 0 |
| rust/chains/tw_greenfield/src/eip712_types.rs | 8828 | `d606311867fca887ff488e59365883c56b0a2b14209aa6266db7b2453405c03f` | 0 |
| rust/chains/tw_greenfield/src/entry.rs | 3077 | `ee65212681673591766531809aa92624f69c5d18e110f12bb8006bbc2dd61bcd` | 0 |
| rust/chains/tw_greenfield/src/lib.rs | 260 | `5fbb210961774fc8c3c2fa0f3e7a0136d343e1872723ae3d6429cb5db2bb205c` | 0 |
| rust/chains/tw_greenfield/src/modules/eip712_signer.rs | 3338 | `c4e57f87d69f558c8e18380e814b8c193843fe5853de34a1b3d61ae0f4e1c515` | 0 |
| rust/chains/tw_greenfield/src/modules/mod.rs | 121 | `97dca7c34e90df66d94ee600ef705c431ba9aa9efacbb49c201263dfbfab78ec` | 0 |
| rust/chains/tw_greenfield/src/modules/tx_builder.rs | 6520 | `a4023f092edab1f6704834dc581de30cc0c4c60b8d7de33aa1813045d05fa969` | 0 |
| rust/chains/tw_greenfield/src/public_key.rs | 1772 | `d06a40a8a59f2ec0d249531ddb6199619bc2d6df6fc8852f0435228f4f583e12` | 0 |
| rust/chains/tw_greenfield/src/signature.rs | 1290 | `2bc5452b7ad82dd4c4fff97b7be60fe8fb65450db65411dbe280d03c0241f0b2` | 0 |
| rust/chains/tw_greenfield/src/signer.rs | 1797 | `fe3a8cf4a4c2be1ee93c69fe13153ec2d6b56f91d55d208cab9061cfcf6c3b7a` | 0 |
| rust/chains/tw_greenfield/src/transaction/message/mod.rs | 690 | `313e1e8ba5b71263a1ec9e50014b46e8f4cd815d581879599225000556fa02bb` | 0 |
| rust/chains/tw_greenfield/src/transaction/message/send_order.rs | 3120 | `9f63a63c0f1502b75c9162330c8a5c8e3bf83cb08b4b1cc37061401bff28d404` | 0 |
| rust/chains/tw_greenfield/src/transaction/message/transfer_out.rs | 3155 | `4f8277a318cf66e4d5419f803fdeedb58728edfb52dbdc714f468e7fcaf3810e` | 0 |
| rust/chains/tw_greenfield/src/transaction/message/type_msg_amount.rs | 802 | `29297e0dca814342419ee4ac615c625e37acabcb6692cc153a8354ab34f98dc8` | 0 |
| rust/chains/tw_greenfield/src/transaction/mod.rs | 2352 | `2ff7007c5a5287656bf90fa776188147c616e12074c3dbd86940a07d30d82a10` | 0 |
| rust/chains/tw_groestlcoin/Cargo.toml | 494 | `bcc8a4fc89ef5acd8ccf3531cf125450300f06e3d2d423624863f5c5ba2a41c0` | 0 |
| rust/chains/tw_groestlcoin/src/address/groestlcoin_legacy.rs | 292 | `1c4ed93648d7bebf9458aca5577ef1a6219d1122cfd3227f4d93495e4e8ba118` | 0 |
| rust/chains/tw_groestlcoin/src/address/mod.rs | 4726 | `cc71f94c91c6fe05660c5743d5bf3a318788a89232af2c59292271d6a66cfc3b` | 0 |
| rust/chains/tw_groestlcoin/src/context.rs | 1734 | `c6fd9052b810f35c0a147583ec415bc6ffb527f6f83057ddd9be93aa2c51d6dd` | 0 |
| rust/chains/tw_groestlcoin/src/entry.rs | 3224 | `678453bffc207ce6477b325e3abb1482ee24d0308201aa6dbe9ac588ee752c19` | 0 |
| rust/chains/tw_groestlcoin/src/lib.rs | 4890 | `c809c826e993cea859db1fd994066e52227fbaa62b0b54b9465f496d95d538ed` | 0 |
| rust/chains/tw_internet_computer/Cargo.toml | 460 | `c32505739ead7f386dae46bbd8902cce90c50938ca5b7396c7d883cd6d754e4b` | 0 |
| rust/chains/tw_internet_computer/build.rs | 1794 | `2611f0d26957cf064f40755d615f8458ef5d82a08c9ff8760b0b75ac48ae76be` | 0 |
| rust/chains/tw_internet_computer/src/address.rs | 5806 | `e5f2e4b2273ea90846b7b74229de04784ebf48324e97e6c308d1404e3767d1eb` | 0 |
| rust/chains/tw_internet_computer/src/context.rs | 2261 | `68b4b16bca1586a8202010d136d1fa88dd5b349371302719f26dacb71906bc53` | 0 |
| rust/chains/tw_internet_computer/src/entry.rs | 3327 | `34cd8fffab043afbbf3b4482a67cbcb39be51584e08831fe4a26e4f25f50dd7b` | 0 |
| rust/chains/tw_internet_computer/src/lib.rs | 183 | `8ca7b72babb874d7ae99762a8deccdff90d965a35e39c9ea15bf8f8529f077f8` | 0 |
| rust/chains/tw_internet_computer/src/protocol/envelope.rs | 7081 | `4480af9b5d576902c9781357e3ae3b4dbc1b32e129f0ebea57a0895546cd8686` | 0 |
| rust/chains/tw_internet_computer/src/protocol/identity.rs | 3622 | `37271d8170fb6572647ee60dc7a30689401078eac0e375bdde37bd03f4136afe` | 0 |
| rust/chains/tw_internet_computer/src/protocol/mod.rs | 1296 | `0f687e7346c2ee91af2390b7ef8c31296e28a4aada20026c6ab8f746ea4f2788` | 0 |
| rust/chains/tw_internet_computer/src/protocol/principal.rs | 7670 | `d29be11d9d73156485e0b0d1f3791321ff5fe04467af0a4f3b340b2ee260b53e` | 0 |
| rust/chains/tw_internet_computer/src/protocol/request_id.rs | 3898 | `d6266aab25b014e0b5ccda2afc5038b00b6c6402f45e8cadab4d6298e504d6fa` | 0 |
| rust/chains/tw_internet_computer/src/protocol/rosetta.rs | 1619 | `3b6b883f0846e9f6abf2491cffcc83979a94cc57e8bb9b3a4e4eeedd623adf2c` | 0 |
| rust/chains/tw_internet_computer/src/signer.rs | 2729 | `1fe4d290693f9ad7ce58dc7dfc7f11cdf6cbcfaa354682de3e3ec08d7922db0e` | 0 |
| rust/chains/tw_internet_computer/src/transactions/mod.rs | 1485 | `88cfe20ef98dfe7f5e8370a3bc52b5df3565826f0792ab8f09d488974956790f` | 0 |
| rust/chains/tw_internet_computer/src/transactions/proto/ledger.proto | 6601 | `fd4e4eec05e85a3a28e1cd4d227b2e25a1fbbd52269e3924ae5564ea2d653128` | 0 |
| rust/chains/tw_internet_computer/src/transactions/proto/types.proto | 491 | `e6afd1f1fec32ef2029fa6667350bc69c5d9b874c0b18900dc2295a166359938` | 0 |
| rust/chains/tw_internet_computer/src/transactions/transfer.rs | 10551 | `43b0b7cab7438aa24607e1bc80065afa24140fcb6e1797690bb844965a60253e` | 0 |
| rust/chains/tw_komodo/Cargo.toml | 355 | `7f31613ebe8ac037acf38bfbdb75da9c25b8d786cc99f6e3c11d1cc48a6ec76a` | 0 |
| rust/chains/tw_komodo/src/context.rs | 1337 | `3c3e3889f7d7b33c7354ad190d226c76b3506c397aeb96e105f8a9b27e94aac5` | 0 |
| rust/chains/tw_komodo/src/entry.rs | 3192 | `9b5e6f8e89ec15c723a854df93e9e4fdb0d011ef1ebdabd1d4a4e171026d187a` | 0 |
| rust/chains/tw_komodo/src/lib.rs | 110 | `8781bc3ac220e7c2b770cbf112ec1f9a5d2f975329858c533e5f114ec59d2d80` | 0 |
| rust/chains/tw_native_evmos/Cargo.toml | 440 | `6bc7eb5b918dae010f129390e9cad0e2661b6e5daf8243e4d574160f634a3964` | 0 |
| rust/chains/tw_native_evmos/src/context.rs | 685 | `e2ff5919ea1d6665b6550e7050d2a5533848ef13257fba7ca1df935c35b3c514` | 0 |
| rust/chains/tw_native_evmos/src/entry.rs | 3105 | `f0867c6cfe871ca62b960d9d0597f9a82061e2f8b9fbe93a63b8f0ad4b2fd269` | 0 |
| rust/chains/tw_native_evmos/src/ethermint_public_key.rs | 2029 | `0b3e003bc46fd35e3337076af18887b7770758b1c1c52d68db995630e8dd1f61` | 0 |
| rust/chains/tw_native_evmos/src/lib.rs | 140 | `5e3a0a3a92028e3069d053c6f6658b0953f5ebd56443ac867056caafbe8d798f` | 0 |
| rust/chains/tw_native_injective/Cargo.toml | 444 | `f004923b7219473dd0f7e3e6187f9a7f2e61436a69b8858f060d6a091ade07be` | 0 |
| rust/chains/tw_native_injective/src/context.rs | 693 | `15d1b6c5e1fa2616c0580d4e885ad1111366ae95271c621ba34a699243e6493f` | 0 |
| rust/chains/tw_native_injective/src/entry.rs | 3188 | `89e0b9789afac8772de4899da7fcc774296102f68969647978744f5ee5265056` | 0 |
| rust/chains/tw_native_injective/src/injective_public_key.rs | 2134 | `f53d6779a1330b4bf574967bacd0db92788e45699553aee9a4635b8009bfb1b1` | 0 |
| rust/chains/tw_native_injective/src/lib.rs | 140 | `e85ce0d11fe4d42d85e903060719d25d87a1878b8c82096e5a185e5f304f49f1` | 0 |
| rust/chains/tw_pactus/Cargo.toml | 435 | `4d59f095cf0860b1a5f82ce11c4a8f4e7b929d2a31adacebddaedab9ac0b05b8` | 0 |
| rust/chains/tw_pactus/src/compiler.rs | 2772 | `a28ea539ec24b8ce3347acc3a92013b4b4b5f40439f1fcceeea15075bd7b3026` | 0 |
| rust/chains/tw_pactus/src/encoder/decode.rs | 3960 | `55099c3561f7fda71938b54f93cd11314dcf9c18acc71bcff09bdae7bec2588f` | 0 |
| rust/chains/tw_pactus/src/encoder/encode.rs | 4244 | `6ebfdc4be27e6a58d1b8f6ce2d73db9e6d7f5c44fde4fefbbca06bde29a42034` | 0 |
| rust/chains/tw_pactus/src/encoder/error.rs | 448 | `1c2a6ff57a2793f29efb235527676981e89355f935d0c85332864ef25e480c41` | 0 |
| rust/chains/tw_pactus/src/encoder/mod.rs | 1029 | `e49386d124273571db5d5a69ab8b9ce351b9d9e69ac7e3e5e34d81cc9d340404` | 0 |
| rust/chains/tw_pactus/src/encoder/var_int.rs | 6271 | `d7999260fcb312d0533c22bcfd9d06bdedd2b374e2ff01727014a9833cc5412c` | 0 |
| rust/chains/tw_pactus/src/entry.rs | 3380 | `95f33c2c5886f1183d5c57650b13989877d1427631fdab6db05b99a72931ffdc` | 0 |
| rust/chains/tw_pactus/src/lib.rs | 197 | `755d55b8e3575eb17e9a8bb6df730838aaf6f9c250b83747170bf13e20316dbe` | 0 |
| rust/chains/tw_pactus/src/modules/mod.rs | 124 | `46d0e0392fdf1ee762708f78cd9709ebf402005f6f014ae0bd2655f75c812a96` | 0 |
| rust/chains/tw_pactus/src/modules/transaction_util.rs | 891 | `94083962b65e968dfde979a5d966f581d39cb150a520eac5a75017a0cffc8b30` | 0 |
| rust/chains/tw_pactus/src/modules/tx_builder.rs | 2212 | `a79fb9eb1011bcc95adc82f6645c2f17fcacbd57f872e5fd0285b728dc3bdff9` | 0 |
| rust/chains/tw_pactus/src/signer.rs | 1307 | `9106167b615f1b86b19daa1d7b0c8fa06754c3d7467ce6562461c9800ea099ad` | 0 |
| rust/chains/tw_pactus/src/transaction/mod.rs | 8754 | `92a5e83aafd15fa8e46cc5cd5c4f545c30cfb9333ac7278338eeb9101013f1d9` | 2 |
| rust/chains/tw_pactus/src/transaction/payload/bond.rs | 2430 | `6ae11f1726735370791a607bd298462bb8731900e9dde1ab3a6bdd6f866b563e` | 0 |
| rust/chains/tw_pactus/src/transaction/payload/mod.rs | 1374 | `93edf5211694435181cd94a303675c13e978f81a5e87027f21f5179adb851d6a` | 0 |
| rust/chains/tw_pactus/src/transaction/payload/transfer.rs | 1463 | `34c827486d6230bc8e414b719fb73ad98d8f29571f139446bc25cd5502f41dcf` | 0 |
| rust/chains/tw_pactus/src/types/address.rs | 10748 | `82e37136c9f373cf542f1d4213a9d9226aa8218dac55257b1cc5d914cfeb9c0e` | 1 |
| rust/chains/tw_pactus/src/types/amount.rs | 816 | `eae93aec8f2267263a9d355b5659e1c89a7a1933c6b3f7fc358524692bb337f8` | 0 |
| rust/chains/tw_pactus/src/types/mod.rs | 181 | `8bd2a50b4d021bb203951a8db18cb313db2a41977c8d6289d4ebc96076241c84` | 0 |
| rust/chains/tw_pactus/src/types/network.rs | 2458 | `9dccd4e8817c4480846e41fc73c4dabf7639e3c6c4577620229fef577cc0e12b` | 0 |
| rust/chains/tw_pactus/src/types/validator_public_key.rs | 4397 | `84bdc4210f891414f697cb86110ee3ee5d73f2ea7d967c01de0fd630a6ae8725` | 0 |
| rust/chains/tw_polkadot/Cargo.toml | 527 | `acdbdb5f5ef24f23dae558a834dc7869be07c33013c8640516a6ea35c987e287` | 0 |
| rust/chains/tw_polkadot/src/call_encoder/generic.rs | 8120 | `a4ec986aa757951c1e84da130ac29421fc552003e9d60859235f96db816f0e46` | 0 |
| rust/chains/tw_polkadot/src/call_encoder/mod.rs | 7879 | `acc783161f153223d87307e89c921ddb6a67d976ca6e56a1c622420de3fd60e8` | 0 |
| rust/chains/tw_polkadot/src/call_encoder/polkadot.rs | 2786 | `e641722300b87ec105d12cc83372ce1ab32a0ad77dff71f0e7a2a1e495031332` | 0 |
| rust/chains/tw_polkadot/src/entry.rs | 5021 | `0e1dd537c1d2e183e4d6dfef8822cae602665c5895241205940cc09473629560` | 0 |
| rust/chains/tw_polkadot/src/lib.rs | 2490 | `a402c636cfb888a5255d0789965c5281d23c2785892ce4c61b0a32d413367a31` | 0 |
| rust/chains/tw_polymesh/Cargo.toml | 527 | `9601faa1e39deae2afb31ba1e5b4c5fd516c55a2c265bf3aa39cf015e6f10ad6` | 0 |
| rust/chains/tw_polymesh/src/call_encoder.rs | 12913 | `26c7008feb4d3a8d942a84b2386245097deea465fb68d607ba9131841bf853c0` | 0 |
| rust/chains/tw_polymesh/src/entry.rs | 4931 | `6913e0f77c7ec1e16ec7d86cb5438836e86b0541de3e504fef5cb5644f86bc2c` | 0 |
| rust/chains/tw_polymesh/src/lib.rs | 795 | `1c13ae526fb1fab9ec0df180d6e209414faaf0ea35d11d001da4c1bfe15c8494` | 0 |
| rust/chains/tw_polymesh/src/types.rs | 8433 | `7339e3a07d259d2fad443614a037b87c628ef4c61cf50af1d85f964e651479e0` | 0 |
| rust/chains/tw_ripple/Cargo.toml | 566 | `4479a06f79ef9b81fa562f613e88a2ea2176e4a09fba21686074250cc88d9e42` | 0 |
| rust/chains/tw_ripple/src/address/classic_address.rs | 3001 | `6a2585749c74923ad88c89fd2de32a28294cd0f75fd210dc31bed9394276298e` | 0 |
| rust/chains/tw_ripple/src/address/mod.rs | 1589 | `c6fc7282e905ee67a6ab6889101687d96b77ef95f85870009878c098bf335096` | 0 |
| rust/chains/tw_ripple/src/address/x_address.rs | 3370 | `3f98381c6d1bbb526e7c47c48977d906067f38bf15eba13c9a1579c0c3f5fd28` | 0 |
| rust/chains/tw_ripple/src/compiler.rs | 2982 | `a33ee3055c53b72f4d17711fee0ba08940933fec9cbcc71402540f4964c64fab` | 0 |
| rust/chains/tw_ripple/src/definitions.rs | 1579 | `a05932bf5ab26778b8e403122a3b400c80b5b3f900d607d22ad3b7cd4d6f3c2e` | 0 |
| rust/chains/tw_ripple/src/encode/encoder.rs | 4208 | `7a80dd3c6efcc88de0627cac2d1876934430ae271896fafd742de0945daadd3e` | 0 |
| rust/chains/tw_ripple/src/encode/field_instance.rs | 3361 | `89f7d8d70bbc19ba98034abf5575b1c69c252d17f85ba91c94ff3c6c13709255` | 0 |
| rust/chains/tw_ripple/src/encode/impls.rs | 746 | `47fb7b48a9fc6b0f98f1e5c5dffc753864fda0b0cc13e32c574b355768a4232c` | 0 |
| rust/chains/tw_ripple/src/encode/mod.rs | 1256 | `1249d0af73db902785bc0aae33aed48e721ffda1dda6aa963c37389b821e9bb3` | 0 |
| rust/chains/tw_ripple/src/encode/st_array.rs | 1290 | `2b623bbf85755b4a4f47b4e09fd6bac219325ec572bff40981fba884034c00b0` | 0 |
| rust/chains/tw_ripple/src/encode/st_object.rs | 8885 | `f00d6a1d2248226c0927d612e546ecea79f87c20da67d6907bdbde67dbe65e42` | 0 |
| rust/chains/tw_ripple/src/encode/xrpl_types.rs | 5282 | `8d14764d37177353a6cf869e0fd2d16b4e8598bd80aa3d6d8dadc84ddce9eb9a` | 0 |
| rust/chains/tw_ripple/src/entry.rs | 3097 | `4f6b04e43d969da7887aae07d27de61ff33c52483f813eb5bda966f2c806358b` | 0 |
| rust/chains/tw_ripple/src/lib.rs | 4921 | `b40f934212273cdf9dd0a132c3a31f030d25fbecf1e4a48edb06ae858b548a5d` | 0 |
| rust/chains/tw_ripple/src/modules/mod.rs | 132 | `f0dd6ebaa1075de7f4ea022ab5e64102f21693dc1426746a95a9cdddb56f5de9` | 0 |
| rust/chains/tw_ripple/src/modules/protobuf_builder.rs | 17938 | `f31cde667ebf0ad86584f293066e9c98669ef9e91312b14bdd2bf97e92bf4f24` | 0 |
| rust/chains/tw_ripple/src/modules/transaction_signer.rs | 5468 | `bb0141ef3406018c7e9db16450f69a9859993cec6f21985f1be99bcceff14188` | 0 |
| rust/chains/tw_ripple/src/signer.rs | 1378 | `97250676fc46fbc5306e0a723d8197c54481071ed4952e90b62ed43e10748c93` | 0 |
| rust/chains/tw_ripple/src/transaction/common_fields.rs | 3298 | `08230160f0384a7cf04bc3e26e46ef11d9fc24f7de1cce912407198703428c92` | 0 |
| rust/chains/tw_ripple/src/transaction/json_transaction.rs | 1037 | `d83fad92fb8d08aa9424e331f14955a4d22671c78a4329a8e3905d2805cc694c` | 0 |
| rust/chains/tw_ripple/src/transaction/mod.rs | 925 | `c92670e2a22c315f35bab034dea45cb51e5c789d7ffb6022a6201281d448ed38` | 0 |
| rust/chains/tw_ripple/src/transaction/transaction_builder.rs | 6987 | `05ea84455f0308397530df6589bbc57668956554c27ca4ef1df33e6c34e90b27` | 0 |
| rust/chains/tw_ripple/src/transaction/transaction_type.rs | 3158 | `164f30c7dc79ac5a417289c4f430575faf5a0b2d5c8e77ade01595229e5df033` | 0 |
| rust/chains/tw_ripple/src/transaction/transactions/escrow_cancel.rs | 988 | `4cff2de738ad46016bb5abc76b10f0cf2ac0b7f34f8592cc2cde4ce7b6afdf8d` | 0 |
| rust/chains/tw_ripple/src/transaction/transactions/escrow_create.rs | 2460 | `306a5b8f5d790ca384d8db02ef682d580f4e134d7c88958c54c0df8f7d68faf6` | 0 |
| rust/chains/tw_ripple/src/transaction/transactions/escrow_finish.rs | 1579 | `8f918eb4277e26bc43b98512a8ffebc02f9f2b15663a32df3976057d8d4ab451` | 0 |
| rust/chains/tw_ripple/src/transaction/transactions/mod.rs | 295 | `37b24b954e016bf7327616604e3986ffc4c8682425379aac1d5e1bd1951f2692` | 0 |
| rust/chains/tw_ripple/src/transaction/transactions/nftoken_accept_offer.rs | 1306 | `4a9219f2833eca48ee47eac686192f21ba6a20121a3a94c1c9fb3b434b5f73a6` | 0 |
| rust/chains/tw_ripple/src/transaction/transactions/nftoken_burn.rs | 1485 | `73e3a6f39894f26fbf100d9a1a4190591de5c47340961f96681080112d751b05` | 0 |
| rust/chains/tw_ripple/src/transaction/transactions/nftoken_cancel_offer.rs | 1098 | `d7dea371eb6a0268798d159fc5a618faf1bef8ee82c15ba4cf8c177df505a4c4` | 0 |
| rust/chains/tw_ripple/src/transaction/transactions/nftoken_create_offer.rs | 2637 | `09dbe0c076892ac834d9b02c879065efd1cad8fe476ba1c48bbf94ff436b215d` | 0 |
| rust/chains/tw_ripple/src/transaction/transactions/payment.rs | 1925 | `a5547a5ec4042aee0610baddf082660a05777641fc535ba78d64ed4b9cf0d975` | 0 |
| rust/chains/tw_ripple/src/transaction/transactions/trust_set.rs | 989 | `02358b3440a57304f98970c21921b7b378ab9c692ae2f6a1aed3a50e67a77fae` | 0 |
| rust/chains/tw_ripple/src/types/account_id.rs | 1459 | `65664450f6e19130b8c8ac44563c8968df41ba487468286b0625023994ff55ff` | 0 |
| rust/chains/tw_ripple/src/types/amount/issued_currency.rs | 9505 | `37aba4993ea7593fe6096ca4bfb44d460df6d0d93f1089d494f30252c41a4184` | 0 |
| rust/chains/tw_ripple/src/types/amount/mod.rs | 1338 | `e5e5c0f2297f202e3d576c0eca3ad9236317d514ce63e9cf8b9f30b788836494` | 0 |
| rust/chains/tw_ripple/src/types/amount/native_amount.rs | 2710 | `0afacde10938669f5173419ec2a9374f22a278d318a0af21902fd7c73641ad4f` | 0 |
| rust/chains/tw_ripple/src/types/blob.rs | 699 | `82997b8f6314502a2e4a76f1c8a59f193fde76d5f1dcbb83e9ce0217b2d6ca2d` | 0 |
| rust/chains/tw_ripple/src/types/currency.rs | 2931 | `ba43e1321d0984d88a86097396a5bdb54aff36e32296fa60d2b5d1654f004679` | 0 |
| rust/chains/tw_ripple/src/types/mod.rs | 165 | `feac93c135a3ff19d2aa109d14f639e1a8b8051cb0512d5f9ba227ba014748f5` | 0 |
| rust/chains/tw_ripple/src/types/vector256.rs | 787 | `e70635d38a91f30f50cc664e08932f81d7d09333dffaf40db31c0660a3588ecc` | 0 |
| rust/chains/tw_ronin/Cargo.toml | 492 | `f718f5ddd31dfb653ed2503228c1ed6c742e9a2722b41e73fec2bd05ab5bb731` | 0 |
| rust/chains/tw_ronin/src/address.rs | 1676 | `fb390787b3f7d9e2955dd8e7e4fb86f2443e56c3f9aeb39eb9b1bc16f10796aa` | 0 |
| rust/chains/tw_ronin/src/entry.rs | 3259 | `fc0832647501d52bb689cdc6966d1c9183c49e03d248b93bb7b9740fe00d4bb8` | 0 |
| rust/chains/tw_ronin/src/lib.rs | 133 | `8c84e0eeafec35158be4c997510f9de3059c8f6a0ac1e911b7989c54feb99f5b` | 0 |
| rust/chains/tw_ronin/src/ronin_context.rs | 255 | `ae23517eab9a4a583f2bc970e2f20a71ab1b8a91876bf110a1e420df34fe7fe9` | 0 |
| rust/chains/tw_solana/Cargo.toml | 575 | `35969766101831bc3398bd9b708ae1b7876fd97658790c1c8c49a0fa7e716889` | 0 |
| rust/chains/tw_solana/src/address.rs | 6695 | `c06545d1008b28b798eaf8a96dfe524011652f78112a390b326d1125f51ffb5e` | 0 |
| rust/chains/tw_solana/src/blockhash.rs | 1028 | `a0475b206262c77f5f1bd9141d01c8bf87f16176d3f8e12cb57325eb935f47cf` | 0 |
| rust/chains/tw_solana/src/compiler.rs | 4481 | `723213ffb42cc4d25f7af99ff6b4c8fe52dcb8c27d1e80e707bdaa1126b4ff14` | 0 |
| rust/chains/tw_solana/src/defined_addresses.rs | 1394 | `918e230e6ab5030d59f582b89a61ca89fde3931f84b29c4842e96c3b2199e89d` | 0 |
| rust/chains/tw_solana/src/entry.rs | 3340 | `c914b1bc2ce7c70b7114e7dc08176019131c6147d55b2fcc6db7a00978862fc8` | 0 |
| rust/chains/tw_solana/src/instruction.rs | 3448 | `1a56257034e4247894456e5e332c72dc246ffa68aab7a3e53de856a10d9ac2cb` | 0 |
| rust/chains/tw_solana/src/lib.rs | 379 | `d83349d93c0e0db73f27c3f00ea2cf589fbb04bb3250efd548aad49dce518a51` | 0 |
| rust/chains/tw_solana/src/modules/compiled_instructions.rs | 3073 | `9995f2571e4b7cef526c8ebe52044f88fc8eb3246568eb180d2d759cea483829` | 0 |
| rust/chains/tw_solana/src/modules/compiled_keys.rs | 4362 | `bbb20285b8022531289dc85c1159e3f3a63d729ac582faf565bb9c4dde7d4b8d` | 0 |
| rust/chains/tw_solana/src/modules/insert_instruction.rs | 17304 | `0f3dd96ac14ccbcce4961b8e07d8d5836525a8cd2fc24353cdcb727be371505a` | 0 |
| rust/chains/tw_solana/src/modules/instruction_builder/compute_budget_instruction.rs | 1575 | `ae3c843556a6ac898fba54302aca13a7b249cd284ac0cf1f4a3f331db6fb4cbc` | 0 |
| rust/chains/tw_solana/src/modules/instruction_builder/mod.rs | 2614 | `e7ffa2d88bbe06519af2f06c34ac557557e1750ac708fef597b4731eecb384a6` | 0 |
| rust/chains/tw_solana/src/modules/instruction_builder/stake_instruction.rs | 15355 | `28651c64c303e736492a33359bba2e6a6329de338bbf3c9ec512d568a234397e` | 0 |
| rust/chains/tw_solana/src/modules/instruction_builder/system_instruction.rs | 10686 | `e4db4513fd6b85d93cde88be300164093728d3398b782de1cc186be9cae8c748` | 0 |
| rust/chains/tw_solana/src/modules/instruction_builder/token_instruction.rs | 4455 | `6256c84a7519b1a2d5c3cd02ce1d9e174f007158fe7931f00392b3adc91eebbf` | 0 |
| rust/chains/tw_solana/src/modules/message_builder.rs | 33788 | `0217224c3115b6f06378f36804b507fc12d503e240fc6218056e0ee060c1b1c5` | 0 |
| rust/chains/tw_solana/src/modules/message_decompiler.rs | 2123 | `610638ccbb8a3c5fe39e99073e8c83df9553a4751a5b9c76fab9c1292a419cf5` | 0 |
| rust/chains/tw_solana/src/modules/message_signer.rs | 11649 | `4995e166cd75558931d803f70a6ce9356648684aacdf80706681d8a2536cf358` | 0 |
| rust/chains/tw_solana/src/modules/mod.rs | 623 | `ae9d95ad854b7e690cbd88a7dc6765c69bd9681480ad249c7996e8145e7d6812` | 0 |
| rust/chains/tw_solana/src/modules/offchain_message.rs | 8745 | `03a8d782662529cf06b97395bee24af3aebb594e93af81d180f31c5afa06193e` | 0 |
| rust/chains/tw_solana/src/modules/proto_builder.rs | 3469 | `6c7d677cc339e1178cde748d3f6e475068d6ee61096684171b61248e12208330` | 0 |
| rust/chains/tw_solana/src/modules/structured_message.rs | 4422 | `81b47fd9d56725ad24c20b6a199bd97e9e4a9d1cc358fc116eca17168961e2a8` | 0 |
| rust/chains/tw_solana/src/modules/transaction_decoder.rs | 1424 | `2dca0389950eb27fc0add74cc756693aee6f9248768c17102994a10e27726a0f` | 0 |
| rust/chains/tw_solana/src/modules/transaction_util.rs | 1495 | `f4d2493fbf374e383e74c7b0be0267c8994e4f28cc6b4a4b5842ace981cc415b` | 0 |
| rust/chains/tw_solana/src/modules/tx_signer.rs | 2728 | `db30c89b9daafd183425f3e782e32192a084107533c1adba21f80a0092431e54` | 0 |
| rust/chains/tw_solana/src/modules/utils.rs | 12389 | `27216933523c824a1d6533e61db274f41bb37c3bd126673837a71d91a36c7fd5` | 0 |
| rust/chains/tw_solana/src/modules/wallet_connect/connector.rs | 2524 | `f71455ecb40dce2e3e9b2a72506c40e3053766ed28372b5aa4e9c1f77d80277b` | 0 |
| rust/chains/tw_solana/src/modules/wallet_connect/mod.rs | 114 | `1998b3e7d8d2a6fc1223da74977d814576ba3577fa1cd3e33df1debac0bdcd17` | 0 |
| rust/chains/tw_solana/src/modules/wallet_connect/request.rs | 435 | `a6d47d7a4dea8ed1e2d87c98b9f474a5571fe1720ac1ea76a42fc9eb731ece39` | 0 |
| rust/chains/tw_solana/src/program/mod.rs | 101 | `4b2c8dbc5dba3567a28376bbf669fc9fb570c73c5299d808c5698017b763494f` | 0 |
| rust/chains/tw_solana/src/program/stake_program.rs | 1754 | `142b7b74478438742fd03a20e638664fa7787ad501298190de19773b3eb1ebcf` | 0 |
| rust/chains/tw_solana/src/signer.rs | 2238 | `adb34d35f6ab9c248838cad09cc3aa69f6e4da930dd0136f5c903c03878538ce` | 0 |
| rust/chains/tw_solana/src/transaction/legacy.rs | 2376 | `cf01db51e77521031c2504a770b501e9b6c2c03801b9b072fa80d4e4d855d895` | 0 |
| rust/chains/tw_solana/src/transaction/mod.rs | 9876 | `a3194cd0fea04d9cdfa49925bf0f27b88b00a689c328e505c509afd84b608329` | 0 |
| rust/chains/tw_solana/src/transaction/short_vec.rs | 12079 | `cf195473f18c9d355fbd627456177c43c28521556f2e5d2110948682522acfb8` | 0 |
| rust/chains/tw_solana/src/transaction/v0.rs | 2848 | `e2cf3507904aa68cc428787511dafafc610ef2a1830d34c09e9593e6c160d3b2` | 0 |
| rust/chains/tw_solana/src/transaction/versioned.rs | 11646 | `21c591d3c0852d37b39e9989d0834272f9fd2171a320c5c1a265bf0bb7668923` | 0 |
| rust/chains/tw_sui/Cargo.toml | 640 | `c26e3b08a5242713b202498fddfc980dfa57116b00fb288e9469a5e97bcb8e65` | 0 |
| rust/chains/tw_sui/src/address.rs | 2820 | `4f6cdc27962de261b85f5d583a89cfc2506e483508738f57229684fc88d0c832` | 0 |
| rust/chains/tw_sui/src/compiler.rs | 3557 | `27f0387e39e55582c6661bdfdca888f8e96079973bf4b087c9e1a3506cf38b9c` | 0 |
| rust/chains/tw_sui/src/constants.rs | 1343 | `1982486fba0873f50506913471ba0dab358894ccc5a654eafee13405e917d7dd` | 0 |
| rust/chains/tw_sui/src/entry.rs | 3208 | `ef77e22dd98b1f5d31e44c78a8d0c3e03f7ba6e14609de4e8246a9ed26816212` | 0 |
| rust/chains/tw_sui/src/lib.rs | 220 | `582e36e077ee05d33ea2b132ab0ad42935e224db254e1e0c804fa630a834e93b` | 0 |
| rust/chains/tw_sui/src/modules/intent.rs | 3050 | `ef87ca703292a75bfe5256951582f1b6159bcdfbaf3a6ea671e182418b43d3db` | 0 |
| rust/chains/tw_sui/src/modules/message_signer.rs | 4265 | `509428543f39888cb1c46bd2d1ef8d51ff81a5668d80bd53fee5de091b0999d6` | 0 |
| rust/chains/tw_sui/src/modules/mod.rs | 183 | `45dc728f347b48e9d29438856dfbea02c32bf9f53991c683a5054f9800bcfcb6` | 0 |
| rust/chains/tw_sui/src/modules/transaction_util.rs | 1458 | `65d524cd759e3965cf14e82ffa8e74e2532845b2dc223794c154a098e986df16` | 0 |
| rust/chains/tw_sui/src/modules/tx_builder.rs | 8333 | `19b4f787941268855494dc45ed3637dc5aa649fdf5feefeef3b9818ec19608e1` | 0 |
| rust/chains/tw_sui/src/modules/tx_signer.rs | 3073 | `ac6f5636f40cd437158c177b503f5ea27233da63c42253e5a0d2592968edb776` | 0 |
| rust/chains/tw_sui/src/signature.rs | 2236 | `936c0e4e6150ecca8fc82cdb291787718f654133aa89cea7ea421747d398d994` | 0 |
| rust/chains/tw_sui/src/signer.rs | 1525 | `4f1956818f4d82b8d6250640d890d173d00122ed175d67b8bc8e67c12f0bf78d` | 0 |
| rust/chains/tw_sui/src/transaction/command.rs | 3782 | `5c8600fe3a0692a027f1252d2c33dbe07b7ec88337cd20d749d4df113013aa1a` | 0 |
| rust/chains/tw_sui/src/transaction/mod.rs | 222 | `6425f9b5d4736781bff1048ef42d52acd611621e391091b5b6add17aac42cb0d` | 0 |
| rust/chains/tw_sui/src/transaction/programmable_transaction.rs | 9176 | `38e34cb8635cc18104f1c9590c7e5fce9dd4d1f8b435d9aae7c85222d1d041ea` | 0 |
| rust/chains/tw_sui/src/transaction/raw_types.rs | 9999 | `eab7c968a14c092bd61e04972233ccc27fd07082dedaf2539c2dafede0f3a58c` | 0 |
| rust/chains/tw_sui/src/transaction/sui_types.rs | 3479 | `269359be7e7996c57bc026d7548a8305669966e6fc822475e85d12d063e63516` | 0 |
| rust/chains/tw_sui/src/transaction/transaction_builder.rs | 8629 | `a4ca2c4f40e3bf5873d3a61fb4885e084fedc3b8ae33456cc0a267a87a6a0d3b` | 0 |
| rust/chains/tw_sui/src/transaction/transaction_data.rs | 6309 | `6cb062a53ddd682bd86e19c10c9230e37637e7cd47af8ac40592f0c24d055928` | 0 |
| rust/chains/tw_thorchain/Cargo.toml | 400 | `d57bd39f4941cc57a0054c0a287f9f0f9749935277a3cabdd62b44b17747279f` | 0 |
| rust/chains/tw_thorchain/src/compiler.rs | 1268 | `e2e204fb0886e8ca7cc92053ee45c7657d07bc72b760bb2c226d153db5f40679` | 0 |
| rust/chains/tw_thorchain/src/entry.rs | 2939 | `1daea19e69f0c63cdcd6337fa90ebd99889274137c4b55e449236145e1554b7a` | 0 |
| rust/chains/tw_thorchain/src/lib.rs | 150 | `b8991cea77ed9788cc1a252ee3c19e0447ba4dcec6b523fca0d3776411638b97` | 0 |
| rust/chains/tw_thorchain/src/signer.rs | 632 | `1a738ab7683b55889b5b349c0a2f17b1f0ec54043d12d1a8fe7e891ec1c7c823` | 0 |
| rust/chains/tw_thorchain/src/signing_input.rs | 656 | `52efecbad7229b3083bfae487bb477b0e21bdf660fca498cccfb269554e45808` | 0 |
| rust/chains/tw_ton/Cargo.toml | 485 | `045db1517dbbdc7d19fb4b918e81f66c4a2ac71ac0c83fde88bdf057b86aa8ec` | 0 |
| rust/chains/tw_ton/src/address.rs | 4017 | `aa4cc564ff1909ade1902abe40101afc6966a898fe5c06ee79dad7e7f8804370` | 0 |
| rust/chains/tw_ton/src/compiler.rs | 3775 | `f63acac84e8cce0f04c80dc78ff372a4e33727405f7fa60bd12a54bda25c6543` | 0 |
| rust/chains/tw_ton/src/entry.rs | 3595 | `1886eb19b76b77dc4c1995363dd67e7e6b75246bd5ab4c0df3185e45c21d0af7` | 0 |
| rust/chains/tw_ton/src/lib.rs | 259 | `5cb24f5144ef5394e2171de1fa3488ad6b1ffb8bb8626320ba9720f0947a97b3` | 0 |
| rust/chains/tw_ton/src/message/external_message/mod.rs | 116 | `13f7683b744815eb1fccc3ce80a04bd93a59280f78356a1b80b9a55e17721f5c` | 0 |
| rust/chains/tw_ton/src/message/external_message/wallet_v4.rs | 942 | `7e384ad841527f5b922e7eedfaa0f65b5a9a7ea0299befde88feafc478e691a6` | 0 |
| rust/chains/tw_ton/src/message/external_message/wallet_v5.rs | 2811 | `d1e7e09b3ed39aefbf8fdca073490fe8f1b34a57afd7f2821da3c1b9de8c1f21` | 0 |
| rust/chains/tw_ton/src/message/internal_message/mod.rs | 476 | `17dcc8416b26a962cc8027836591c8a3c0c7c8c750a7d5e390979a6d1b0f4590` | 0 |
| rust/chains/tw_ton/src/message/internal_message/transfer.rs | 2789 | `7955b1cdd533628a4d53768f802e2568343cc8ef48b73f279c989c0ae9e51676` | 0 |
| rust/chains/tw_ton/src/message/mod.rs | 111 | `6b580a8274cd4ee197651b2a7ded7fd7b479638976f30d32bc6c98ec1f6b611b` | 0 |
| rust/chains/tw_ton/src/message/out_list/mod.rs | 708 | `007129d8d01b3ee2b707f61978fafb5d6a31279db0876cbe0adbc458226d30ae` | 0 |
| rust/chains/tw_ton/src/message/out_list/out_action.rs | 1177 | `1126aa16c48f7d7b29e3124b5143dc7a8a9f2f430764c947baa97ed4f6329ee7` | 0 |
| rust/chains/tw_ton/src/message/payload/comment.rs | 604 | `e480ab29472a04446dd033038f57f75de69dce9c54edc70c2fbb1fad83ac86f7` | 0 |
| rust/chains/tw_ton/src/message/payload/empty.rs | 357 | `edb9cfeb398da6d0d2c48c469952d2fd8dd2e3ef115c5f7a026763763569cadd` | 0 |
| rust/chains/tw_ton/src/message/payload/jetton_transfer.rs | 3789 | `5e36bc527d5ae5d0ec9e8b0ab76243560aec6c57fe75811f28497170bb61e887` | 0 |
| rust/chains/tw_ton/src/message/payload/mod.rs | 135 | `cfcfb0074bdd17eeee71de8feb770d34bf5eee2e2fe1991982b3594fdb1acd00` | 0 |
| rust/chains/tw_ton/src/message/signed_message/mod.rs | 132 | `d3de472b1ebd82cb8bd77005011df53bcf8b98a4163c1b1ba4adc887d014c86e` | 0 |
| rust/chains/tw_ton/src/message/signed_message/signed_message_v4.rs | 662 | `f3cffd4b42dc346ff94e4e6c2b2e005523d5e4c81414a6cfc9cf0197fd36238b` | 0 |
| rust/chains/tw_ton/src/message/signed_message/signed_message_v5.rs | 661 | `5ae760e7197e008a60b79376821f3cf48159fffe4206ed5d11155b6d607b1fa4` | 0 |
| rust/chains/tw_ton/src/modules/address_converter.rs | 2797 | `a3c8b59586f290b07656238825f3899741b3b8798d82f082c1a7c74952cf2bdc` | 0 |
| rust/chains/tw_ton/src/modules/mod.rs | 189 | `98107041b9ecbde5f81827e467e53e3a658dbb3b236bd9d1273cea6b29c78807` | 0 |
| rust/chains/tw_ton/src/modules/personal_message_signer.rs | 2084 | `49865d69cd9ac823cc18439fc9cfb37d65d349148b6003f961023ef89193fafe` | 0 |
| rust/chains/tw_ton/src/modules/transaction_util.rs | 1416 | `4ecb22a47fcc89f3a610d9d22d2e6965e1cc2f100a6835f68af68d9a1543f90b` | 0 |
| rust/chains/tw_ton/src/modules/wallet_provider.rs | 1275 | `fb43c7eecf23aa490347be8f8756b93591ef0f714a0334b480b0ef677821e098` | 0 |
| rust/chains/tw_ton/src/resources.rs | 1111 | `c9b604e605dd5b2bd5e71e4579a8e8576e76f231047ad6d8f66a87dbd2f83eaa` | 0 |
| rust/chains/tw_ton/src/signer.rs | 2093 | `b56924090b76e07a34b13bb54589625e0828672e3ba00cd6ac3a51fe11ed6e5f` | 0 |
| rust/chains/tw_ton/src/signing_request/builder.rs | 6115 | `e55af96d7acad703457b2bf40255d8c577f2b84f4e89c919fe1679b5327fd897` | 0 |
| rust/chains/tw_ton/src/signing_request/cell_creator.rs | 5426 | `f02cf52f81a1d976cf8987d720b2ddda9eaeff3bf411f59d6e96bc13989c7071` | 0 |
| rust/chains/tw_ton/src/signing_request/mod.rs | 2195 | `d89bf9652ba8c1cfb905eeea81247352ed4379523efc57914ba7875b81f6f169` | 0 |
| rust/chains/tw_ton/src/transaction.rs | 1620 | `0c21f35f7a2278f09343afada19b71592ce0505f44041bbdd8290986ccc86075` | 0 |
| rust/chains/tw_ton/src/wallet/mod.rs | 4169 | `f6f547c2ece2684a6d6a8cfb9e7e6dd1a67fb3a887d2b4bfe78d83ee5742e574` | 0 |
| rust/chains/tw_ton/src/wallet/wallet_v4.rs | 3863 | `0ae77de629bd6c51802d8bd39588fb5aa110e0f4fff6247a47552811e425c15b` | 0 |
| rust/chains/tw_ton/src/wallet/wallet_v5.rs | 4413 | `f35a4f5e582c2f04463e225b6b3db055d1010cb4d1809207fb2a02ad9b3bd1cb` | 0 |
| rust/chains/tw_zcash/Cargo.toml | 714 | `0a85a7d240260d2195649e0d8d798bddb79d893a70c36c0169d32f421cdc45d8` | 0 |
| rust/chains/tw_zcash/src/address.rs | 3447 | `07834dc5de4d6c6853b89a3814d0d18c7d52e7773aece4f3b1efce5440e20b4f` | 0 |
| rust/chains/tw_zcash/src/context.rs | 1393 | `9c445ae9b4d7bc06735f32ecf638205d843754d28af2053987f4ac97438e4368` | 0 |
| rust/chains/tw_zcash/src/entry.rs | 3354 | `8c03fa8cb4f684553cdbe81f2e33dc7776ec6d6f14cf08fdf4c5cef8e1a1157c` | 0 |
| rust/chains/tw_zcash/src/lib.rs | 5248 | `f45296e8ea38622eb275a89ff9d3622e916928197d9e78b72fb5f115373854ab` | 0 |
| rust/chains/tw_zcash/src/modules/mod.rs | 246 | `11ca961f38eeb9039def4818bf97166a7c55ec6af2183239d298612c684084aa` | 0 |
| rust/chains/tw_zcash/src/modules/pczt/common.rs | 5463 | `9d571df59af04e9af13af679f6cad5685729ff1f5b54bbd00eaf29f0d458497b` | 0 |
| rust/chains/tw_zcash/src/modules/pczt/mod.rs | 3129 | `61013668b387a2ee0d293ff51edfb058a85e975f3b4e01664717076f4679d8a9` | 0 |
| rust/chains/tw_zcash/src/modules/pczt/orchard.rs | 1651 | `d0751481e4a2556bb161752b1f7f9a45db5ef52479953a3aee4fba873984585d` | 0 |
| rust/chains/tw_zcash/src/modules/pczt/sapling.rs | 1112 | `037d9d277c064e3a9ce773f1399de223c6ea273a88a99a27082d6e2c6d620fe3` | 0 |
| rust/chains/tw_zcash/src/modules/pczt/transparent.rs | 6199 | `774dd7bece00a39804b9fe61a6be85b5472cb212217f24df84ba3ac881db912c` | 0 |
| rust/chains/tw_zcash/src/modules/pczt_request/mod.rs | 154 | `5c57aed90701ad5358cbd330060c6f002dc9f3399919624b90254c5d2d702641` | 0 |
| rust/chains/tw_zcash/src/modules/pczt_request/output_pczt.rs | 1034 | `9454524b0c3ba3afd7d4a67344551718f1180499724d4600d037a9d78f9f6500` | 0 |
| rust/chains/tw_zcash/src/modules/pczt_request/utxo_pczt.rs | 3839 | `fa46dd1c62559acee6a1033de9a66ae746d651f24081157eca289f2f2b65c789` | 0 |
| rust/chains/tw_zcash/src/modules/pczt_request/zcash_pczt_request_handler.rs | 4470 | `9f41737effef7961f501fee83c79ef59192bb4985342972dd8ba47fa14cd4e2d` | 0 |
| rust/chains/tw_zcash/src/modules/protobuf_builder.rs | 1395 | `2f5d8e9e6f49f065276f59a28bd47fd7849036b628c77e5bcf7c1abd5add9e7a` | 0 |
| rust/chains/tw_zcash/src/modules/signing_request.rs | 6596 | `9c6d3caa0f49b5a1fd404292a86e2856c583eb62964d714c8e9f290b371243a7` | 0 |
| rust/chains/tw_zcash/src/modules/transaction_builder.rs | 2743 | `3b5ba0767251aebae471249a91cfbe285ec9628085dc094fa55e92abf98eb774` | 0 |
| rust/chains/tw_zcash/src/modules/zcash_fee_estimator.rs | 1283 | `3126c28cf8b723d81716ccf53c796ff47a92816e7b0d83f6755931cd71966bc4` | 0 |
| rust/chains/tw_zcash/src/modules/zcash_sighash.rs | 5029 | `04e7c1a248399933358e85aeecadd7d2717dea84fc07cc1aab10260c77f27098` | 0 |
| rust/chains/tw_zcash/src/t_address.rs | 502 | `04a1827ce3fb39cb757c9b5f878595394158692fa4926a5eeb613b3a4700c56e` | 0 |
| rust/chains/tw_zcash/src/tex_address.rs | 4017 | `4e5261e2aafae9ef5bcd74dd748a39ef6ba4f76baf2004ee006a4201552267f2` | 0 |
| rust/chains/tw_zcash/src/transaction/mod.rs | 6079 | `d4fb7276fa75345f654061ebc0b6009ebbd5c34f429d3356d76ef176d9a5c1a0` | 0 |
| rust/frameworks/tw_substrate/Cargo.toml | 470 | `52515fa2b96d81ed0cfcae71c38676fcf977ff9c49791db6629ad3de426da288` | 0 |
| rust/frameworks/tw_substrate/src/address.rs | 2809 | `3fa969f6a67288093f269c71b4536551515081f6a9005f895c1cdc37b66163b5` | 0 |
| rust/frameworks/tw_substrate/src/entry.rs | 5476 | `37090fb30389b1056f307024ebd6be767b0fbe59df910e81ad58f9b86e2ea69f` | 0 |
| rust/frameworks/tw_substrate/src/extensions.rs | 8065 | `959dc98912392d72e30fe054bac08c0ab395765f43d525318047898eea37ddd1` | 0 |
| rust/frameworks/tw_substrate/src/extrinsic.rs | 8262 | `37432567d457b5d17cfa87f72cd8a6836a78dce47eb293083d0ff0ae919fefe7` | 0 |
| rust/frameworks/tw_substrate/src/lib.rs | 1819 | `df08bd16d796c83dd9a02f32e0a91ee4a15d49b7eabeb3c946f97aac1affa322` | 0 |
| rust/frameworks/tw_substrate/src/modules/mod.rs | 104 | `3e38c1b77a2e2f40e7b92d1fe60fd0937e20d810c98f0ae4d70c00fab11bc88c` | 0 |
| rust/frameworks/tw_substrate/src/modules/transaction_util.rs | 893 | `6d8e8deaf5fbf61560cbd2cca7fa39f880300ec999c1a001dfff97cd7a357cc2` | 0 |
| rust/frameworks/tw_substrate/src/substrate_coin_entry.rs | 6355 | `cce96d9b2f79a420a67d618b9d1a8282397714df9d7ab32b4eaf286ce14ea9f7` | 0 |
| rust/frameworks/tw_ton_sdk/Cargo.toml | 521 | `58e2cb43b18dc0f22b8e32c4fd99934d5cade62bba5f666cf1ebe3fcf60e8b1f` | 0 |
| rust/frameworks/tw_ton_sdk/src/address/address_data.rs | 713 | `5c5b1d5a95f82d1b248599998febe640cc9a9a87e5fe936c4b98f614ce0263bc` | 0 |
| rust/frameworks/tw_ton_sdk/src/address/mod.rs | 152 | `d3ee1f4eac47f6308a434b2eacc8810ac2b71c32c2e4ac09d2971a045c2e1081` | 0 |
| rust/frameworks/tw_ton_sdk/src/address/raw_address.rs | 1808 | `6f5e0686ac5cecff9dd5cb032c34c157cb711728ba88dd83ead608c479615157` | 0 |
| rust/frameworks/tw_ton_sdk/src/address/user_friendly_address.rs | 4765 | `4e4b8537c5529c8b52b365977b7ac67edc8a76e1f226d5eee0f307d496d2e946` | 0 |
| rust/frameworks/tw_ton_sdk/src/boc/binary_reader.rs | 1806 | `d8c2a58f97ede7bc2dab31f43f20126a42a24e1990642c76607f9eea154ce291` | 0 |
| rust/frameworks/tw_ton_sdk/src/boc/binary_writer.rs | 2874 | `f353a9a0de67c0f4db471783d6ec70612475177d0ae58f56440c148e4e802d1e` | 0 |
| rust/frameworks/tw_ton_sdk/src/boc/boc_to_raw_boc.rs | 5402 | `d7992c0c4e7169889970eebbc76204b0fccadf5f3b22e8c7ab81213e352d7a50` | 0 |
| rust/frameworks/tw_ton_sdk/src/boc/mod.rs | 3742 | `90e4c0e08613de77d78dbe755f15510638d3ee6bc5e33e4bcb2cc27423abebb6` | 0 |
| rust/frameworks/tw_ton_sdk/src/boc/raw.rs | 9511 | `00b22a156b0db1612736ba65fb83a7e015540ad18e942f30854b45cc1d0cdb93` | 0 |
| rust/frameworks/tw_ton_sdk/src/cell/cell_builder.rs | 7386 | `bcbbf521a43da8480841225f24fba1f5081aa2ce89aef6695619487e8678b324` | 0 |
| rust/frameworks/tw_ton_sdk/src/cell/cell_parser.rs | 5241 | `f7be44707aa9284c4680c97c5bbf0076851c5a521674e031c7fb7b2cc7b1981d` | 0 |
| rust/frameworks/tw_ton_sdk/src/cell/cell_type.rs | 6918 | `10ace55b854d0f415a11cbf25fd4b52ee5fc530be7f8f911afb4c7ebd7ec249e` | 0 |
| rust/frameworks/tw_ton_sdk/src/cell/level_mask.rs | 1209 | `e5753244efd8588064711ff4e9f1ac5eb1738f0f9ea3c952aeb1456ce7d9c396` | 0 |
| rust/frameworks/tw_ton_sdk/src/cell/mod.rs | 9976 | `ee5009614c6fecd6c3d0a7c68296856278c9118e07d9683ef092999aba60e19c` | 0 |
| rust/frameworks/tw_ton_sdk/src/crc.rs | 304 | `6c283b283dbba44ce2de04571fb72182c582bcffa9661f83ad7f66ac3b1d670d` | 0 |
| rust/frameworks/tw_ton_sdk/src/error.rs | 1103 | `def616c2585c39cda0f49f849c58affb8f6ccde65a80c08cbde9cfc56bc34172` | 0 |
| rust/frameworks/tw_ton_sdk/src/lib.rs | 167 | `42b82c143e84a7cb7032367c4a83b2d9088efed79a566de0535b49ecd05b4a6b` | 0 |
| rust/frameworks/tw_ton_sdk/src/message/mod.rs | 98 | `1342a7b3b71afe1f2b028441d7ca8fc78f9806e055bf0ca74c4fa80094dfbfde` | 0 |
| rust/frameworks/tw_ton_sdk/src/message/state_init.rs | 1269 | `04b29a343449c2162a7f8ce83d4c4261bd25c9921b3540d59e68101b66f26ca3` | 0 |
| rust/frameworks/tw_utxo/Cargo.toml | 775 | `db3f28ca06d20768c5d7a61c0f8446e84a5db140c98c3864035c22dc677704eb` | 0 |
| rust/frameworks/tw_utxo/src/address/derivation.rs | 2807 | `10a4ee690a57df8084a78353d9dce0fef3ebbaac104ddf11d5210c390df771ed` | 0 |
| rust/frameworks/tw_utxo/src/address/legacy.rs | 272 | `d5420b2200558f60822fcbbd5e851a5d3ad830567d4af49b4a0fead41797bc6c` | 0 |
| rust/frameworks/tw_utxo/src/address/mod.rs | 440 | `e40478c2720fb30e7844571a34e41c0028f3952951fe55cf15397bd8a51f07f2` | 0 |
| rust/frameworks/tw_utxo/src/address/prefixed_b58_address.rs | 6238 | `75e540741cbb6d29416410a8971a8b722cbd51a6bac07d7d02a26ed3dd57417f` | 0 |
| rust/frameworks/tw_utxo/src/address/segwit.rs | 8034 | `55d2057f511d98cc8d984fd8f27f2a42de9af8ec6f2ebca50767d142fbbe50c5` | 0 |
| rust/frameworks/tw_utxo/src/address/standard_bitcoin.rs | 6965 | `26f524131f06a69863cb39d0d10ceac09a2d3230009794c727d5a24784540c0f` | 0 |
| rust/frameworks/tw_utxo/src/address/statically_prefixed_base58_address.rs | 5800 | `cac543a785f3b7bcc865b5ae5aae626ca2d60bdb98926f6e8820aa1aae25a30e` | 0 |
| rust/frameworks/tw_utxo/src/address/taproot.rs | 9297 | `acf3638e3c054fbecfd400d34c4aef8ea3509bc3f696c6401daa725720fb109c` | 0 |
| rust/frameworks/tw_utxo/src/address/witness_program.rs | 4345 | `5e5d238a0fb1d45f31cd6467e95ecc454420ef809034e491f95452202ee4b613` | 0 |
| rust/frameworks/tw_utxo/src/constants.rs | 1503 | `9cf6d210fd298278970c29726270ab20ebce7470386aec9dc5ffd15b252a4952` | 0 |
| rust/frameworks/tw_utxo/src/context.rs | 1246 | `1c20584b45732fdfaf4beb6168f523ebc78046924b115e031f019e2036901a33` | 0 |
| rust/frameworks/tw_utxo/src/dust/dust_filter.rs | 1904 | `91933102c3870b9b3bd49456739c93e2a37345616cc33c674e5667366a25d064` | 0 |
| rust/frameworks/tw_utxo/src/dust/mod.rs | 513 | `6bbdea76b2f00fdbfece33d822b254aabacec6409a304208eccd4292cf14c5e8` | 0 |
| rust/frameworks/tw_utxo/src/encode/compact_integer.rs | 2649 | `cec6496da87ff5c579c2ee8a57f64a2f5e3478fa187d109e68d65a4be70e5778` | 0 |
| rust/frameworks/tw_utxo/src/encode/impls.rs | 2541 | `0be0ff1371c1c938b7bd5e379478e1bcd1936a962c26e55cd1a1b8e2e5d1d1eb` | 0 |
| rust/frameworks/tw_utxo/src/encode/mod.rs | 690 | `99d2b13b1949532a78659192077855fdefa87938188df635be345041a486ba61` | 0 |
| rust/frameworks/tw_utxo/src/encode/stream.rs | 1516 | `e4d3d77e27e9a5521b1f7d4e02adb0a59c42c6b275a5c7a49bed95cf7ed9d86a` | 0 |
| rust/frameworks/tw_utxo/src/fee/fee_estimator.rs | 1315 | `28c9da95c0bbc45c1aa83e452a7b37295c9d53a8336bd08bfd4feb87669bcf5a` | 0 |
| rust/frameworks/tw_utxo/src/fee/mod.rs | 399 | `7fc166549a22dca7b87177c78f18681a280b78ab720d19090debf2b91b6861b4` | 0 |
| rust/frameworks/tw_utxo/src/lib.rs | 309 | `172294bde843ff9f24bec7aa1f538fab394197aab73126646fe659f1c6280a1a` | 0 |
| rust/frameworks/tw_utxo/src/modules/keys_manager.rs | 2861 | `b4cd0276f0d568459f4badf4e83b3d1017728f7b840056bce7e954adf1e62c0c` | 0 |
| rust/frameworks/tw_utxo/src/modules/mod.rs | 235 | `9bee3264ae3a765adf6bdf4773bcbb9a989ba7cf9dc3ab30966239308b077852` | 0 |
| rust/frameworks/tw_utxo/src/modules/sighash_computer.rs | 4968 | `9871a6e9be78e47b1212d94d384ff4594f1d2f06022382cfd49ade95bf097d81` | 0 |
| rust/frameworks/tw_utxo/src/modules/sighash_verifier.rs | 5019 | `a9f6af71d7a26cb6f34032215d4cb481f1c631071c27c216239f4e7adaf7a3b8` | 0 |
| rust/frameworks/tw_utxo/src/modules/tx_compiler.rs | 4600 | `f3d192a86752c6276d61baeb36d395173cc5fc3f8f5841c08b89cf3f64b0b197` | 0 |
| rust/frameworks/tw_utxo/src/modules/tx_planner.rs | 3252 | `90391768fbf2b80e2251bd29c1e031ca6cac46fc8d95d26a1e2840432ac685a5` | 0 |
| rust/frameworks/tw_utxo/src/modules/tx_signer.rs | 3140 | `00d68755b0954b4b2319639931936933147ff32f264728de952b72acea869f09` | 0 |
| rust/frameworks/tw_utxo/src/modules/utxo_selector/exact_selector.rs | 6301 | `7166f5fe860a6b3cf1b33bc884063ef19e8baa8ab1558a6e38a423afb3a7a2c4` | 0 |
| rust/frameworks/tw_utxo/src/modules/utxo_selector/max_selector.rs | 4737 | `2d04f5e677b55e64ddbc062ca032ae0e160f47e8beb7e0f1d2001269bbde89ac` | 0 |
| rust/frameworks/tw_utxo/src/modules/utxo_selector/mod.rs | 1655 | `c575072664c8c721635dca2a1509a0a340bd79294d8f5173b81bf7bc8f1ec5b5` | 0 |
| rust/frameworks/tw_utxo/src/script/mod.rs | 8391 | `c3aa226787bf0fc8f9721e51a8836d5b3b1bbb14c367f264b9116e35b0a20a5d` | 0 |
| rust/frameworks/tw_utxo/src/script/standard_script/claims.rs | 3025 | `6d8d6ec089ff0f1e02453a51920ccddce564c9a78c3768165d0878dd60deba1e` | 0 |
| rust/frameworks/tw_utxo/src/script/standard_script/conditions.rs | 6110 | `5dcc7c5df69902328650bfc8d8b09acaec8ef9dff9fe441de4e686fc8f02bae3` | 0 |
| rust/frameworks/tw_utxo/src/script/standard_script/mod.rs | 104 | `780fb64988ba669677926c88cadd21574a2be314ee75444e2e438d0648681b9e` | 0 |
| rust/frameworks/tw_utxo/src/script/standard_script/opcodes.rs | 9379 | `10976e7c812b29771f07858a4a023b88ee30820ccc41fe2c77d3111a2cc42fbc` | 0 |
| rust/frameworks/tw_utxo/src/sighash.rs | 3466 | `d3b0a367dafdf4688bdf9845cf29ab97abea3b721236c966cc88673d8e4387e7` | 0 |
| rust/frameworks/tw_utxo/src/signature.rs | 6208 | `9d50c1fd6d9213220c319357a73246f1d169f74ebb931cf42b3d0652c2038e9b` | 0 |
| rust/frameworks/tw_utxo/src/signing_mode.rs | 308 | `15522b3eed96838f0f7b36f68330eb7cbb6283cc44d7de3c0db31a9d76034cf6` | 0 |
| rust/frameworks/tw_utxo/src/spending_data/mod.rs | 1382 | `f69db81f7d59cbe71e7b6a324a6c0cce196286679da4498bd03792cb577732d4` | 0 |
| rust/frameworks/tw_utxo/src/spending_data/standard_constructor.rs | 2208 | `b3f6ed2a372cf3d9b9b519e285d5b5d9e4927d9f466bd7872bdfba3340b29b19` | 0 |
| rust/frameworks/tw_utxo/src/transaction/asset/brc20.rs | 2217 | `eed1e952cc2d31ffa6e6ab43379ee9a518c0912936ffc6d13bd9c0176c00d77b` | 0 |
| rust/frameworks/tw_utxo/src/transaction/asset/mod.rs | 32 | `c77d737bd8b2d8708690d0eac6648e4265ad034611bc8676991a67f2f959d988` | 0 |
| rust/frameworks/tw_utxo/src/transaction/asset/ordinal.rs | 5075 | `28cbda0939655705d51f405329ceaa8a7c788605d79878b8295e234032a83f88` | 0 |
| rust/frameworks/tw_utxo/src/transaction/mod.rs | 2905 | `8eeb1bffe65f7e43137e7c1b42ee3e0c0f3f1fe3a12a6f9b150abd7867eb6fe0` | 0 |
| rust/frameworks/tw_utxo/src/transaction/standard_transaction/builder/mod.rs | 2275 | `3cf2480b99652fa13e0afbf5c24fcd79b18d21af0e2e5cac4a834f7241d5adce` | 0 |
| rust/frameworks/tw_utxo/src/transaction/standard_transaction/builder/output.rs | 5404 | `a91e154f18b4fd4320f81eab75785b17958cd09681dee8d65c6ab7bb6110a46a` | 0 |
| rust/frameworks/tw_utxo/src/transaction/standard_transaction/builder/utxo.rs | 18326 | `c6299351702db16143b2f72c3c71cf5e211c5332686470d52fe642a4dbd3786e` | 0 |
| rust/frameworks/tw_utxo/src/transaction/standard_transaction/mod.rs | 10140 | `95013f861910dfe94b5f810a023597503ee692081a19e0f1342aa45ea1a628bf` | 0 |
| rust/frameworks/tw_utxo/src/transaction/transaction_hashing.rs | 4024 | `543d77685b7ad3e416e7652fb37beb3f0bbf67feec2499e384b5c35887663015` | 0 |
| rust/frameworks/tw_utxo/src/transaction/transaction_interface.rs | 2103 | `d59bc2f4eb72aee30bbc9f02caa150c57b4f3fd098098af8a61f9611f717e23c` | 0 |
| rust/frameworks/tw_utxo/src/transaction/transaction_parts.rs | 727 | `14f7e7a8e1fbb04fd912051a7c4a19b3b5e1a9b8171850f904d8be878bf8b80a` | 0 |
| rust/frameworks/tw_utxo/src/transaction/transaction_sighash/fork_id_sighash.rs | 840 | `1f42a5bef95827f455eec7647392d116b868f45a3f56f3c3021087d065dcc57f` | 0 |
| rust/frameworks/tw_utxo/src/transaction/transaction_sighash/legacy_sighash.rs | 4206 | `384720f00cc8e8ba1d8d3d453ddee87c5ea47e2a095070d2da9767c0ac482d94` | 0 |
| rust/frameworks/tw_utxo/src/transaction/transaction_sighash/mod.rs | 179 | `32b754da7391be1f50aff1719ba6d9e51bdcd74d696836374959cdbc8b5bb257` | 0 |
| rust/frameworks/tw_utxo/src/transaction/transaction_sighash/taproot1_sighash.rs | 3468 | `8cadd27a02ba01889b240b454e1a11441cff8bd32c4a11a3a7374370a549435e` | 0 |
| rust/frameworks/tw_utxo/src/transaction/transaction_sighash/witness0_sighash.rs | 2443 | `090a601c50a640088e7ba194078d97072d47e38ce591fed92331fa822ae53d94` | 0 |
| rust/frameworks/tw_utxo/src/transaction/unsigned_transaction.rs | 5523 | `d86453e28f4a5e44d9e53dfa778cef8826d344d8ca428e893fc16125b3245d54` | 0 |
| rust/tw_any_coin/Cargo.toml | 586 | `ed783eeabb1220a29d562dab88411ef3ed9bd2855896b408635d5b6c465aebf3` | 0 |
| rust/tw_any_coin/src/any_address.rs | 2730 | `79d292036e709f735edf20d4fd7d57f0c99c57ca3ef3a6d3049ee582607ed41e` | 0 |
| rust/tw_any_coin/src/any_signer.rs | 937 | `5e50e13861c392ac4c9892a420edeb177cae826e33bd6b620dfa45c6666a08f3` | 0 |
| rust/tw_any_coin/src/ffi/mod.rs | 281 | `d5aac3d035a30495eb1daab1ccb43d3cb5c26f258e4a8081304240d409e538c2` | 0 |
| rust/tw_any_coin/src/ffi/tw_any_address.rs | 10842 | `a0b8f5cdb955db08baab6dedcac4d48d24411e653bedaa336ad0a30540fbed4f` | 0 |
| rust/tw_any_coin/src/ffi/tw_any_signer.rs | 1705 | `6366e616f4fccb79f78d6080be1ac3d82eec4a5c1aec14b70ca25f6c9f733bc0` | 0 |
| rust/tw_any_coin/src/ffi/tw_message_signer.rs | 2792 | `0971cbbbd0f1017c4e9380029bb031e53a0b9665f24b2179f1e53b977f5c4d75` | 0 |
| rust/tw_any_coin/src/ffi/tw_transaction_compiler.rs | 2792 | `36105ccfb12bfdc4f7c2166a481b978f6648d6cc205a3d3e0562b67839995f7e` | 0 |
| rust/tw_any_coin/src/ffi/tw_transaction_decoder.rs | 954 | `cc5b79aa62d9ca26cf8354d71097058889b2a1d797302055b71e4b5cfb52ef5e` | 0 |
| rust/tw_any_coin/src/ffi/tw_transaction_util.rs | 1092 | `ea571c849dc21a6eb87a1fe13b1cbce1e0e6ee651bd038fe6d7c02d059342e66` | 0 |
| rust/tw_any_coin/src/ffi/tw_wallet_connect_request.rs | 1260 | `99a931fb35d29e5a025ee5f616f373ad57507d68f0fc01bc21e8554a13203328` | 0 |
| rust/tw_any_coin/src/lib.rs | 356 | `9a198b0e940c04f81cf6175e2f3f2ec49d8fa9f9b6cc990d2b3eb3ac5077e9a4` | 0 |
| rust/tw_any_coin/src/message_signer.rs | 1089 | `15e67cfe7066bdcc5d9d5021176184015a163dacc132987cb2ac2a3722ed68f0` | 0 |
| rust/tw_any_coin/src/transaction_compiler.rs | 1205 | `75d46b17c2b41dd4986e6846f0edc4fb36c192ec189ff821170944a3b9ca76bc` | 0 |
| rust/tw_any_coin/src/transaction_decoder.rs | 548 | `b55376a9ed5c12fdd800776193d401341b22105779de66f5eb8a58f07a9082a8` | 0 |
| rust/tw_any_coin/src/transaction_util.rs | 514 | `ec733aca203cd89cf310455c4309b2fdb4876636969bf07bca015dcb7303c15f` | 0 |
| rust/tw_any_coin/src/wallet_connect_request.rs | 724 | `b07b871cd8aa9743459a53b08345a13fb21dc586b7ef37aa9cf04670a7f9a132` | 0 |
| rust/tw_base58_address/Cargo.toml | 359 | `19672e4a44774f1bdb593e655cd41822339c73975348bf605f4e0881c61f1505` | 0 |
| rust/tw_base58_address/src/lib.rs | 3598 | `c82fdde3e3743bb60e26b8dd354e9d2160d681ecb6408b2e83bac328476b1db1` | 0 |
| rust/tw_bech32_address/Cargo.toml | 339 | `3aeafd9bad1c3a71b0420607b25542881e4df1ab4be8c1075014358bce54f00a` | 0 |
| rust/tw_bech32_address/src/bech32_prefix.rs | 525 | `b2cd714e2b178ccc2c0cfe29597bcab9fae241509a771cd66ca7950302fa3325` | 0 |
| rust/tw_bech32_address/src/lib.rs | 15376 | `bbab50bd2a8ce3c2b125fcd150ceafcf7023eac1a111c3e9f9e0188930a77dd8` | 11 |
| rust/tw_coin_entry/Cargo.toml | 419 | `e7b407fd3547f03ca7e113751e45e64b51ced45e2c7e68caced312fe8fb1556e` | 0 |
| rust/tw_coin_entry/src/coin_context.rs | 881 | `1f9548a81cffd4963a35cd804cf380d60b1e879f75de8f9b6b785507eed30a4f` | 0 |
| rust/tw_coin_entry/src/coin_entry.rs | 6435 | `1f1473a952fe6fb53228d1009ac29583344e2018ec0c6bfcd5c043b45bb67185` | 0 |
| rust/tw_coin_entry/src/coin_entry_ext.rs | 10327 | `2b5502db3ef835a65370a3eb633305334b08d58aab10dfbd6c9eb587c9e1ca5f` | 0 |
| rust/tw_coin_entry/src/common/compile_input.rs | 1796 | `455e7f6f7a016201eb6b9e08b0c36c762a641ddb7b40ca224a5d07ed63cf666a` | 0 |
| rust/tw_coin_entry/src/common/mod.rs | 101 | `97ef69c11da49b82306f9d68a389351c4f3fe69123a5d90ce24722f60c3611ce` | 0 |
| rust/tw_coin_entry/src/derivation.rs | 950 | `9456260d349744c75b0ad64ab45d93dd3b77298da10573276aa55e434e27b1e2` | 0 |
| rust/tw_coin_entry/src/error/address_error.rs | 735 | `55fce66285cc7deb30497c4b9da85af780b10b573591aef1e18d24253fac2886` | 0 |
| rust/tw_coin_entry/src/error/impl_from.rs | 1835 | `7dff49e8dc507e19d6953ed265a9b3d891a9c3dcdeed0270758fa8ebe4eaf4bb` | 0 |
| rust/tw_coin_entry/src/error/mod.rs | 2263 | `3c1391710e168e70154027121f270fa2fca4fdd3e2f24979830e6d92df55e012` | 0 |
| rust/tw_coin_entry/src/error/tw_error.rs | 2233 | `4def034658d1941696746b94d76f5ce17e28e43cc3f5cd400f27b9153d14ec15` | 0 |
| rust/tw_coin_entry/src/error/tw_result.rs | 1968 | `3d781b018f15041eba6ab7828bef3cc114ee141f8bb746401682b431a45419a7` | 0 |
| rust/tw_coin_entry/src/lib.rs | 280 | `7d9a1ad302e6d05ede9fbcbd395dd6f8d26e59d6f60044d7e63732c42b150984` | 0 |
| rust/tw_coin_entry/src/modules/json_signer.rs | 773 | `e7182b69ed21ba88c62b7173e26aac7df09f1288bf35bea14555d93eff5b2d94` | 0 |
| rust/tw_coin_entry/src/modules/message_signer.rs | 2016 | `3cf84339d8d7c35e8b82af29f71120dd188aec252b152334ce46514d682207dd` | 0 |
| rust/tw_coin_entry/src/modules/mod.rs | 314 | `5f41ece236a33f8521b9a44d106d25cc83f29bb666291296b8fed3acb238209e` | 0 |
| rust/tw_coin_entry/src/modules/plan_builder.rs | 895 | `3e48008da4cc1ece8a1d769461328cad27725cf625e3de955d2237a40c4739a9` | 0 |
| rust/tw_coin_entry/src/modules/transaction_decoder.rs | 742 | `9070e484a079d295934384d439b0f6c769057fa55c1879d51c720345998a030a` | 0 |
| rust/tw_coin_entry/src/modules/transaction_util.rs | 653 | `6a2dd8ec2c746ca306ee76cc6e3c409d9f4dbd306faa1e87c8eead2cf082e4a2` | 0 |
| rust/tw_coin_entry/src/modules/wallet_connector.rs | 828 | `a9b5bcc06dedc09306b7119cfbf171ac6f22928b1fc4e259268c91e72953ef4c` | 0 |
| rust/tw_coin_entry/src/prefix.rs | 1532 | `04315c8afa8dc375d8c346e14777797a22281be9954196849e35d54c3611089e` | 0 |
| rust/tw_coin_registry/Cargo.toml | 1774 | `96f59f2c732ee9adddff1bbf9f6f3334449d1a756a4639b7db938722b169ac73` | 0 |
| rust/tw_coin_registry/build.rs | 3044 | `abd9f0308d5ccc09db76f097888a9bdcdec428ea37f8b20887232bc4e314c07f` | 0 |
| rust/tw_coin_registry/src/blockchain_type.rs | 882 | `cfc2dd871c4961af23fc205f6031d6f4b2c39c3fcee76455b8b48f783462db18` | 0 |
| rust/tw_coin_registry/src/coin_context.rs | 1225 | `8d56b0b5f59003e61dc32a6c8d6658cbb8f91bdf9eab000b4049fa327dc6449f` | 0 |
| rust/tw_coin_registry/src/dispatcher.rs | 4889 | `70d7b25ba6fde271265d9a8c36ab5ff8fc5ee74fe30ac939698abf898ea203d1` | 0 |
| rust/tw_coin_registry/src/error.rs | 749 | `6e86a3afa75d5ffe50505aa6863373a80e4a99076217c7ed4d1c271204d152e6` | 0 |
| rust/tw_coin_registry/src/lib.rs | 281 | `e48552de496f89c2fc5613a914d7abf7429b86e3b32f77779e1af87cc0bddd22` | 0 |
| rust/tw_coin_registry/src/registry.rs | 2024 | `2e81ea44df02aea8a1c1c0f777ae9c79b02c1f29f5c17cc5e94c908245fef98f` | 0 |
| rust/tw_coin_registry/src/tw_derivation.rs | 1437 | `f3461f3f61a979a6cf0713891c4c028bd023e6e2f15a3eedbdb18f301cc40a8a` | 0 |
| rust/tw_cosmos_sdk/Cargo.toml | 821 | `d47019faef664197e32d6fbad133c3338f00af3d476f73921ab16e447eaaffe8` | 0 |
| rust/tw_cosmos_sdk/Protobuf/authz_tx.proto | 1017 | `4c10694b10e5f63ad75d3af4481535612c0ae5649808d770080c211a42f63fd4` | 0 |
| rust/tw_cosmos_sdk/Protobuf/bank_tx.proto | 388 | `4dfda13fe3ac27914604569114e61a975be54595ca73eac7eb2635f5becc79be` | 0 |
| rust/tw_cosmos_sdk/Protobuf/coin.proto | 364 | `8bcf217ecffb0013ba4a644c3abad4048dc9b083e75f23325db771541f37c392` | 0 |
| rust/tw_cosmos_sdk/Protobuf/cosmwasm_wasm_v1_tx.proto | 879 | `4f469388ae68337775c36216b73403702dc44664eb58640c07ce59620bb913bd` | 0 |
| rust/tw_cosmos_sdk/Protobuf/crypto_multisig.proto | 539 | `8d568b6305b4ce8163330814a85804988fe8a77d40d8d83dff471ca754550b3a` | 0 |
| rust/tw_cosmos_sdk/Protobuf/crypto_secp256k1_keys.proto | 527 | `b776c777b8c69a3da3bfa368e9b38835e3684e9935ce17d684c838c60db78cc3` | 0 |
| rust/tw_cosmos_sdk/Protobuf/distribution_tx.proto | 567 | `2dfe2c0da7c0efaca729fd366d8f5692f22617f77dbd05230712222a71436851` | 0 |
| rust/tw_cosmos_sdk/Protobuf/ethermint_keys.proto | 261 | `4a10d473420eed652d75a4abd5da3d8c40db457df8669b4320a06a5a81976cd5` | 0 |
| rust/tw_cosmos_sdk/Protobuf/gov_tx.proto | 741 | `a0300ee7a4548eb60b689fe8089b9394d694ca0072d5529111183087cd014b3b` | 0 |
| rust/tw_cosmos_sdk/Protobuf/greenfield_ethsecp256k1.proto | 385 | `f172c0d944d187061e2fe559dddac659278703e1f8983551211c1dd88fd152fe` | 0 |
| rust/tw_cosmos_sdk/Protobuf/greenfield_tx.proto | 430 | `209cb51e5de2006121f239e373f3b8e4f9ef6cb41a8ae18b9661ea5509eafe1a` | 0 |
| rust/tw_cosmos_sdk/Protobuf/ibc_applications_transfer_tx.proto | 1135 | `930b18a49e78312d02ba7e511c35cffe88b9b928285af9a34c7f0f3d5cbaf2b0` | 0 |
| rust/tw_cosmos_sdk/Protobuf/ibc_core_client.proto | 467 | `87e4786b86a81d3ea440038ce264537b6171d495e0d7fa0a78278814be577f37` | 0 |
| rust/tw_cosmos_sdk/Protobuf/injective_keys.proto | 103 | `61a0ed885cea98b4ea8a8714f0deadfe961979c7d07886e8add8c617127439a1` | 0 |
| rust/tw_cosmos_sdk/Protobuf/staking_tx.proto | 1087 | `810a00a0dfb0c0b53a614420e265874c4f6ebcf40030e9653a95496887d8fdaf` | 0 |
| rust/tw_cosmos_sdk/Protobuf/stride_liquid_staking.proto | 258 | `cbaac7b453d2140e67cc4c091fa9424a93f67186dd826676320483b0ee3aabda` | 0 |
| rust/tw_cosmos_sdk/Protobuf/terra_wasm_v1beta1_tx.proto | 825 | `22cb1e0e125af0d3d636486d299a7b228992fa0ee61dae181879e45e8e0ddee3` | 0 |
| rust/tw_cosmos_sdk/Protobuf/thorchain_bank_tx.proto | 1343 | `95b5e795c3a5d018957e0558c370783eacc5aa5f4837a293fe4d908978de852a` | 0 |
| rust/tw_cosmos_sdk/Protobuf/tx.proto | 7930 | `763944e800554924201a83f2ad1693656129fa0ba819b0ee25866723d3c802d4` | 0 |
| rust/tw_cosmos_sdk/Protobuf/tx_signing.proto | 3380 | `a294af44f352db7d25090d319f8cc8616b341b970200955a78b0613d68f36e57` | 0 |
| rust/tw_cosmos_sdk/build.rs | 2125 | `b9ff3fd5d08621e6d99cd26bc231e7a820de0c0b93ed1a0e87943a978a2a46ad` | 0 |
| rust/tw_cosmos_sdk/src/address.rs | 402 | `996ecf6d886956864aec489c56cf89fab5e3f1bd897c98ac8692c4dc65dc9e48` | 0 |
| rust/tw_cosmos_sdk/src/context.rs | 969 | `6643dd4f178ddd48d3481da32be75b88ff8173c8761a4acd43f60103c45c1805` | 0 |
| rust/tw_cosmos_sdk/src/lib.rs | 407 | `33d190667eca4a433d5d5706ba630c93b98bafaadce9367e580b8a27a776a0cf` | 0 |
| rust/tw_cosmos_sdk/src/modules/broadcast_msg.rs | 1827 | `f8ed15341880b52342e4f0d2172df98a8d6cd3be40cabda32a0becc434bffbd4` | 0 |
| rust/tw_cosmos_sdk/src/modules/compiler/json_preimager.rs | 1217 | `fcbc0b85d9d53d1deb517753797c8c8e947c318cacfd00089cebae3fe0c2cae4` | 0 |
| rust/tw_cosmos_sdk/src/modules/compiler/mod.rs | 151 | `973b39bf3c9bd02c6d9b66e797c05676c51ad32aa310e4c7ec063aeef49caab4` | 0 |
| rust/tw_cosmos_sdk/src/modules/compiler/protobuf_preimager.rs | 1470 | `047438b08150ce72dd8bc251182a0c1c290d2a9d613b10e180e3c0c61931697b` | 0 |
| rust/tw_cosmos_sdk/src/modules/compiler/tw_compiler.rs | 8959 | `45c266b677160ac97ce70a06e5f19a4ad47d48e521eaab2b8f1f668a31b4f7e1` | 0 |
| rust/tw_cosmos_sdk/src/modules/mod.rs | 201 | `a8d62f6d787775ce417130b52c14e3472a547f049bc9e94556d1f1f73741e67a` | 0 |
| rust/tw_cosmos_sdk/src/modules/serializer/json_serializer.rs | 4096 | `49bf18655341e73fda73c020360e1f9094ce8246a63043eef6b35832783910d1` | 0 |
| rust/tw_cosmos_sdk/src/modules/serializer/mod.rs | 132 | `ea59a7c84357bf45a957aac9ab5c1a7f02be01bcc063a2cab62885011306456e` | 0 |
| rust/tw_cosmos_sdk/src/modules/serializer/protobuf_serializer.rs | 5860 | `73e328ad14173c09bb52f82a20143b126efb36645499a7022fd2ae5f7046bc39` | 0 |
| rust/tw_cosmos_sdk/src/modules/signer/mod.rs | 97 | `d1a4d7d3d73798ce52eddc5945b64b1d9271daea578f54110e7c9f2506cd1c78` | 0 |
| rust/tw_cosmos_sdk/src/modules/signer/tw_signer.rs | 1837 | `dce39fdf245e4afdee56816fc0bd3ec6bdbd0fd83b2b03768f942a5105e071fd` | 0 |
| rust/tw_cosmos_sdk/src/modules/transaction_util.rs | 1259 | `cbcfa09dfa8197659ae3bdfb49985464d23bd9acf6337c22d6fbd4f010631c71` | 0 |
| rust/tw_cosmos_sdk/src/modules/tx_builder.rs | 32239 | `342626f1a0fa1f961d179a7b504bc0e8a4432928eff5cb44353fe5492bf78960` | 0 |
| rust/tw_cosmos_sdk/src/private_key/mod.rs | 419 | `d9d6f3f8765fcec0d92fdef9d63aac3a2e6b285726cf849eb52f573876f95d28` | 0 |
| rust/tw_cosmos_sdk/src/private_key/secp256k1.rs | 862 | `e99bf1bfe1fd568b47d238a38712eddabb1b05607baeccd9b6039212eda1da19` | 0 |
| rust/tw_cosmos_sdk/src/public_key/mod.rs | 1362 | `750b4a6dcc7e2adf6cb7f24273571a4be72c5fb3cce061f65dff4bac21053c68` | 0 |
| rust/tw_cosmos_sdk/src/public_key/secp256k1.rs | 2884 | `d0525c5fe1e2848aa6fc48f91dc9e2bd80769d9554e0e3625ebad1c26cf8b53a` | 0 |
| rust/tw_cosmos_sdk/src/signature/mod.rs | 250 | `673734013abdb3b323421e5003a9bedf5d68f43f1bcefe04ff0f1892921ebc35` | 0 |
| rust/tw_cosmos_sdk/src/signature/secp256k1.rs | 258 | `604373f51b7d33749bf77d0850110bdee6f072891a94ccbeaa8a4df4d0963e21` | 0 |
| rust/tw_cosmos_sdk/src/transaction/message/cosmos_auth_message.rs | 1798 | `7c6cfe271bab98f2f6368245d016b0040d9877da3861c04dac3e243e2e345a1d` | 0 |
| rust/tw_cosmos_sdk/src/transaction/message/cosmos_bank_message.rs | 1386 | `11bd8d2e89df91d889e26eaa3c343595c282f52bdfe0c228924541af1a036326` | 0 |
| rust/tw_cosmos_sdk/src/transaction/message/cosmos_generic_message.rs | 575 | `c88a5f6b2fc32dc0c49551661b53eaada609f7f613fbe9d75209a88fd0aedbcb` | 0 |
| rust/tw_cosmos_sdk/src/transaction/message/cosmos_gov_message.rs | 1315 | `f78a147dbed888a11406b0de71afe5f5975dcc27b5e166f662b66ba8c408deaf` | 0 |
| rust/tw_cosmos_sdk/src/transaction/message/cosmos_staking_message.rs | 5706 | `03aa765c3db8f0b5d795a10497abafc1ac5673374639e09d74e0258a7b6b28f9` | 0 |
| rust/tw_cosmos_sdk/src/transaction/message/ibc_message.rs | 2039 | `a332a459414c584593afdfe290931ede88f34b6d09afa0abb4971e7968fb692a` | 0 |
| rust/tw_cosmos_sdk/src/transaction/message/mod.rs | 1886 | `df2a4dde5896d4f7f12862c8d07f7a166d3cbd9eb031d312652bebabee15dc44` | 0 |
| rust/tw_cosmos_sdk/src/transaction/message/stride_message.rs | 1412 | `f767074ed35969d17157e1f9e4773e7aa7ceb3a0241fb8cc60eec8e8c7f29895` | 0 |
| rust/tw_cosmos_sdk/src/transaction/message/terra_wasm_message.rs | 1958 | `a2eda9e39662b8ff99f3764b4e75947cafa10e9d8d058cd22ca25b61e9090f99` | 0 |
| rust/tw_cosmos_sdk/src/transaction/message/thorchain_message.rs | 2227 | `bfd34ddf14130eeca5204fc8a6a7d9c49bb1eabbc4966ccbbe3b610363736d28` | 0 |
| rust/tw_cosmos_sdk/src/transaction/message/wasm_message.rs | 3294 | `be79879bd060662860c584aa2a1a4c73d82de2188cc38c2fc25e80118b3ee055` | 0 |
| rust/tw_cosmos_sdk/src/transaction/message/wasm_message_instantiate_contract.rs | 3657 | `32dd1695fed6eae35894853110b71ad1088d8b640bdeb070f7487f2c38b26eb2` | 0 |
| rust/tw_cosmos_sdk/src/transaction/mod.rs | 1677 | `7682155b78ace72609398b362783210ef1c29814201ff0719abbf8313f630a45` | 0 |
| rust/tw_encoding/Cargo.toml | 387 | `e1181753576f11fb65862f9f0201fde87e387f34c748e4d7f7f7fd237aa882fe` | 0 |
| rust/tw_encoding/src/base32.rs | 4635 | `bfa173478a118ce2c6cbac60b2bc2fb782f57a1ffa1d4a1e728b58fdc558ec85` | 0 |
| rust/tw_encoding/src/base58.rs | 2369 | `bb0442dec54438c39d8ff8c84abfca45284475bbbe64e21d8f2b016814c8f98b` | 0 |
| rust/tw_encoding/src/base64.rs | 1921 | `d6a6b58a7882d04b90c1bbdfa84011c69e5f04fe54162301ae4d4150ee481a1a` | 0 |
| rust/tw_encoding/src/bcs.rs | 510 | `403c5784e4d6ffc32a6df5d666c548922483b18bee968f9d7c520ddfa8e9d7e9` | 0 |
| rust/tw_encoding/src/bech32.rs | 751 | `ba1cef60a2f23bdc5dd1da568c449248fb6b410df3e5f1fc5f3dc01da28a0f88` | 0 |
| rust/tw_encoding/src/cbor.rs | 1992 | `082a079ed25e2304911aba72e9740490ce21d7efd0d505eb7547b2f9fea11380` | 0 |
| rust/tw_encoding/src/ffi.rs | 7574 | `a5e1b421ae80d25e5cb9c8651bc8bb8856ced0669f3f93464855af8d5e45da50` | 0 |
| rust/tw_encoding/src/hex.rs | 6695 | `3b0fa36bf27acecbbbff302db9d21510c0591a2aaa89dffc2b9ba24b4c9ef9c5` | 0 |
| rust/tw_encoding/src/lib.rs | 360 | `aa0e2cfb5f7d0c8014fd9374da1e3e74130f716cb5d4b997d75c8babbfbbc31e` | 0 |
| rust/tw_evm/Cargo.toml | 798 | `15feffae154a21eb0c49790e67d0c2b3c9f00a225f0a7c36eb8aab8f19970dc2` | 0 |
| rust/tw_evm/src/abi/contract.rs | 1909 | `2b69f31fc48577d2ab9671b9c5a08f774367f8a6fff5be49b29322843c708ab7` | 0 |
| rust/tw_evm/src/abi/decode.rs | 37017 | `473f21ca1df0f1589bf72bde128f275809a029641e78c3ea1c8ee2a66c33aea8` | 0 |
| rust/tw_evm/src/abi/encode.rs | 46064 | `c9ea33b19aa17f91779779f47158a954728650de4ad0befb4f79449ac4f92677` | 0 |
| rust/tw_evm/src/abi/function.rs | 2499 | `15f02a39fdb4cb2a20e812f115a2452cbec755cd011063d1012d76a859d5729f` | 0 |
| rust/tw_evm/src/abi/mod.rs | 1997 | `e954c71d7c2b89f72bc8c98753ae44764b1df67c88a4d5ea8c98c0b67f69da08` | 0 |
| rust/tw_evm/src/abi/non_empty_array.rs | 1868 | `fd1775767413d13cca48540d98e2c48e4b136585acbc180516fc3db9a0b0946e` | 0 |
| rust/tw_evm/src/abi/param.rs | 3617 | `2265e17d7fd7eede74ad9cdb79a15fb40c65d9e762c1df5e420048e51f8ac55a` | 0 |
| rust/tw_evm/src/abi/param_token.rs | 1730 | `1d10b9f4d7ad2ca19bd2dfdc6c546847e11f4a4cf40a29ca03e5561f59147b45` | 0 |
| rust/tw_evm/src/abi/param_type/constructor.rs | 2599 | `d98fe33139865c5a1a805970849141a662fa655008b7a65af882fdccb662c39b` | 0 |
| rust/tw_evm/src/abi/param_type/mod.rs | 3957 | `0fa3b11b6932b5076f93479d64bdfb36707c92b8309a0f299b0b4e77bfe80c8a` | 0 |
| rust/tw_evm/src/abi/param_type/reader.rs | 5164 | `211160a635aeb98660e2ab143a6a470780346e5e0892ec34a886515f1c120d0d` | 0 |
| rust/tw_evm/src/abi/param_type/writer.rs | 4205 | `5530b472ed021dc9e3ff8c4fd611c20c96fcb14971a367d2d86acbaacbfaaef8` | 0 |
| rust/tw_evm/src/abi/prebuild/biz.rs | 4713 | `99be4be66c424025d6df2e19371eccbce698e23a9efe5eb00adc2f5f91fa137a` | 0 |
| rust/tw_evm/src/abi/prebuild/biz_passkey_session.rs | 3164 | `944b43eb24ccd447a496249bb980fc33057d5c8b7ac832d2fd936e43b686d0bd` | 0 |
| rust/tw_evm/src/abi/prebuild/erc1155.rs | 1084 | `08b12e8ff0e99a2243bae8dfad0c35d69e23761e5fa52823a6ef3e67bd61e920` | 0 |
| rust/tw_evm/src/abi/prebuild/erc1967.rs | 6437 | `4a0f3a73167145558af861ad087482bc5b6e30d82c593762f89ebd75e9ed8a31` | 0 |
| rust/tw_evm/src/abi/prebuild/erc20.rs | 1022 | `0a717677ef4bf9995eb249f5a4d10cab90e1f5a5193fac636cd750a625469d25` | 0 |
| rust/tw_evm/src/abi/prebuild/erc4337.rs | 1955 | `c6e3a3026c22612d1c1edb478a4f98636489e073d89fdcd569d1fb4d4a79af50` | 0 |
| rust/tw_evm/src/abi/prebuild/erc721.rs | 930 | `78dcd79885a05d16cdc3ef4c8bf81342c87a4c712a5799499a39873eeaf2ec28` | 0 |
| rust/tw_evm/src/abi/prebuild/mod.rs | 381 | `e290f1ed2fb41ad527450d65059d9f9681063e7d806ca19ae64149078b50ac36` | 0 |
| rust/tw_evm/src/abi/signature.rs | 1023 | `aebe7bc67a915e18af7867b3d295410945b5786a678f620a25d7dfe62c53d8b9` | 0 |
| rust/tw_evm/src/abi/token.rs | 7301 | `910403efea19848331019050afda77f1c335538fe0df5a984e77332710521710` | 0 |
| rust/tw_evm/src/abi/uint.rs | 1315 | `6de8510e7ed8c18bcffb210d4383a306b4e749f316c3b6a633033496feddbbf8` | 0 |
| rust/tw_evm/src/address.rs | 29285 | `7203da23146eaaad77852d662eb45071d3a27b0606ca98d0efe0aff0422308e2` | 0 |
| rust/tw_evm/src/evm_context.rs | 335 | `805ad243e918f670d9fd70d05e9f016b47e890d87205714eeebc484bd10dcc6c` | 0 |
| rust/tw_evm/src/evm_entry.rs | 5072 | `057761dc8d0c133abc388500c22ac8df50abe2978c788929621c0de47fb7f8ac` | 0 |
| rust/tw_evm/src/ffi/barz.rs | 6348 | `83c2f0c0a05674fc4d97d84df4baca346990f683682ffd3dc663fbb90c1b910d` | 0 |
| rust/tw_evm/src/ffi/biz.rs | 4881 | `c2d00f1ff8d8dd5d544ab9c3baab1d72f1aec285a64b4553a135bb2ab6451965` | 0 |
| rust/tw_evm/src/ffi/biz_passkey_session.rs | 5090 | `9dff436f81c62908315dc355af7366480646aa8683419bf663443e5cb4a53a67` | 0 |
| rust/tw_evm/src/ffi/eip7702.rs | 3117 | `6a97d5f32e61ae2f937e7c4c49bbb312c36b41f5aaaa1b94586197e664d43273` | 0 |
| rust/tw_evm/src/ffi/ethereum_address.rs | 4475 | `d74eda42ae769b78ecf4d97a732656bf59cf419ad516cab8f767aeee3bff5969` | 0 |
| rust/tw_evm/src/ffi/mod.rs | 204 | `5da84c24e4224881ad6202ff5292f22281a2bc4d65fb1f6ba8f943c3112919eb` | 0 |
| rust/tw_evm/src/ffi/webauthn_solidity.rs | 3014 | `51411aa4e43cf62b02176ef480b94bf42952f0bb223195e4f981418ca8f4eee5` | 0 |
| rust/tw_evm/src/lib.rs | 248 | `a410937cb2611a4f59e84a03969206701f223552238813b31f28e3c21a4047e5` | 0 |
| rust/tw_evm/src/message/eip191.rs | 1488 | `afa199fe4b6847ff48732028652c2f69a725c18f653f600de855855490fb874b` | 0 |
| rust/tw_evm/src/message/eip712/eip712_message.rs | 16411 | `b081d12581096e13a8842446fcb3e63daa7802408b547119b8ffdc655e0515bc` | 0 |
| rust/tw_evm/src/message/eip712/message_types.rs | 1462 | `55f06fb4648c246bed835afbc4dbd50ee945dc94fbd3880c644dad56d8748f67` | 0 |
| rust/tw_evm/src/message/eip712/mod.rs | 143 | `71deab6c8877b2ec635ccf5ac2c5e633ae5be4082a3c4408e646a9741562d8ed` | 0 |
| rust/tw_evm/src/message/eip712/property.rs | 5697 | `597e121c0f5c75ee1bae657e1748090950796ab136a309360b3dfc875db05041` | 0 |
| rust/tw_evm/src/message/eip7702_authorization.rs | 2692 | `2e0c9fdeb1955275a217578351f242d224169f2faa710eaf54ab8bdfb94b36ff` | 0 |
| rust/tw_evm/src/message/mod.rs | 1303 | `7cbe63fef5967b2e2b6d1569f8b7e95b7f5aa2e9ffd51c185608249e04b15798` | 0 |
| rust/tw_evm/src/message/signature.rs | 2711 | `3742d7313a0eb7fe52ed00e414443d86ba51086966f21c26be1e9de625f40147` | 0 |
| rust/tw_evm/src/modules/abi_encoder.rs | 23608 | `572806ba2fd003da1a3c6737b3eedabaaa5281450d7229c2a8485ce8f7e5c0e9` | 0 |
| rust/tw_evm/src/modules/barz/core.rs | 11412 | `38080fc66c77f69b4752d1d8fffbcd6f145cd523d7a4149c66ee532953e23f56` | 0 |
| rust/tw_evm/src/modules/barz/error.rs | 1569 | `c9c2861ee97b85c414bbb69efe1885987dbb8dd66361dc652dea9be8b28c2f0f` | 0 |
| rust/tw_evm/src/modules/barz/mod.rs | 107 | `2233ab6cb98a21a87f6a46063c8067a5422f532f96ffec3f8dbcb61b9fb9a05d` | 0 |
| rust/tw_evm/src/modules/biz.rs | 5876 | `9209074405b9c3814f4c9710b78e000bf6bf8a5985751e6972fd32e1cdfcb4cd` | 0 |
| rust/tw_evm/src/modules/biz_passkey_session.rs | 6357 | `61f13d88ef9ed1a691b891f3fa7bfdb447801ddf4b4317552158d5865e798c4e` | 0 |
| rust/tw_evm/src/modules/compiler.rs | 3183 | `083772fc8a3d1e434328f4d327fd36d14d3c2175b08198c4510fe0e99e0bc532` | 0 |
| rust/tw_evm/src/modules/eip7702.rs | 1574 | `1e1c60846672961d670ef07740b93befd1a36b026c58c4aade97ea7c65678fbb` | 0 |
| rust/tw_evm/src/modules/message_signer.rs | 6559 | `7a4ee271378db9ae9ad9aa63cfcd5ab89da591dff007c26144b96ddd2b9009af` | 0 |
| rust/tw_evm/src/modules/mod.rs | 315 | `598b1f735e680213a3bc20e5232d2f93ecf404fe55d8fd9d29fdc9b0aeff8768` | 0 |
| rust/tw_evm/src/modules/rlp_encoder.rs | 3573 | `6bfeaa4acaee44ba9df2bb971b689770674f7dda36a024fde4ee05b2ad591fdf` | 0 |
| rust/tw_evm/src/modules/signer.rs | 1973 | `e76ee2989f5c1299c9011b7c487347d83d1a373cefabe7a24ce582814d25d9a0` | 0 |
| rust/tw_evm/src/modules/transaction_util.rs | 787 | `29984f1d95eb0c2d68398bb7a551ca45c96458a185381bfed604e40ffa5b00fb` | 0 |
| rust/tw_evm/src/modules/tx_builder.rs | 28465 | `55962f416e568679a3033e74a7fe3c166a222c9a893cf46077c428377e867b09` | 0 |
| rust/tw_evm/src/modules/webauthn.rs | 6282 | `640ccd5038d203990428f800fff62c189019058e4561df26e62e6cc2d7c4a46f` | 0 |
| rust/tw_evm/src/rlp/buffer.rs | 1681 | `09195a31b6ebe2bd15588901c08f6596c168197e0e601222c1b89a7147ad908c` | 0 |
| rust/tw_evm/src/rlp/impls.rs | 1256 | `f06ab03d633a23d20e7ded955276c320a1d64f17a59f3123172a4db93b50bf4f` | 0 |
| rust/tw_evm/src/rlp/list.rs | 1444 | `b841c982335e80f129ebb035a96c7308881635287fea318b904648034ff3ef0a` | 0 |
| rust/tw_evm/src/rlp/mod.rs | 313 | `aa1a07e1339ac0ebe56cdcef2db2e03b1ae1ffb0f632a04fb1b901410f175caa` | 0 |
| rust/tw_evm/src/signature.rs | 1508 | `87b1573fe3b2c12c44fac246e8c6453c5169efe2ea08349540b7e502d85fc2ee` | 0 |
| rust/tw_evm/src/transaction/access_list.rs | 1571 | `0d4e5f58e744dc4468c39fb96b6ca83e4fd1c4a4b3833a75e73ae8c6cb5eaea2` | 0 |
| rust/tw_evm/src/transaction/authorization_list.rs | 3347 | `f26230d27d9f97de39d44e34a0268066cac1a984d610bed1e9a2676c6dfc87b4` | 0 |
| rust/tw_evm/src/transaction/mod.rs | 2988 | `847b756b22ad1ac3a420342dcf75fd38ff616d344d8a43823c5abb58da38d6f0` | 0 |
| rust/tw_evm/src/transaction/signature.rs | 5486 | `91312d7774ea4c9a7cda252d39298b1dae77d1a6b68f1f31d01d702450104853` | 0 |
| rust/tw_evm/src/transaction/transaction_eip1559.rs | 6256 | `6a54bee133cb6623f922d80efd0c149c264524ea72ed286ded15d079538a7808` | 7 |
| rust/tw_evm/src/transaction/transaction_eip7702.rs | 5296 | `a3db9a71630999f1ddad82541d8a2d6fab6218cc85c7fdecff429ec741cd53a7` | 0 |
| rust/tw_evm/src/transaction/transaction_non_typed.rs | 4765 | `18c5b78c885135de7cc92750f55aaa6b738b1523bd7de90e2441c4e7f76c43de` | 0 |
| rust/tw_evm/src/transaction/user_operation.rs | 7469 | `52d4c20a83312ace644691e23cda863184310d65dc25c29ac0462e5bd7bdc7a5` | 0 |
| rust/tw_evm/src/transaction/user_operation_v0_7.rs | 16932 | `3ba84527c825451d6f5852700348465bd2279111bbfe8e0b3dde0e8dffaecf23` | 0 |
| rust/tw_hash/Cargo.toml | 546 | `14271784747f211a6b0efa45cb2694ccd37b3849bbfcd27faa799b5b130a60b7` | 0 |
| rust/tw_hash/src/blake.rs | 615 | `d2a441e14d3f9dd5934e3757f6692e5931c127eb05ffd228e6b33fd084454488` | 0 |
| rust/tw_hash/src/blake2.rs | 2812 | `0e3074c506b50c9c93e794e24da8566d7e04d6eed93e2e3605de5fb6dd50fd48` | 0 |
| rust/tw_hash/src/crc32.rs | 3771 | `336357e874c776107267d47dad9d8029dc86456d7d0c9394543ff1305d67fd5f` | 0 |
| rust/tw_hash/src/ffi.rs | 7116 | `a675c549766ede5c61d8b42fd0d31e2fdb9bb7c48f2a999d47e2c2568e155420` | 0 |
| rust/tw_hash/src/groestl.rs | 564 | `9bee12532026b1a070f519cb2c9402c7313072f1d83fb428d189f7b011d94b50` | 0 |
| rust/tw_hash/src/hash_array.rs | 11627 | `c18fc412b60886eed22184a0f0ebbdb345cce2bd9f411d6e905c5458c7444640` | 0 |
| rust/tw_hash/src/hash_wrapper.rs | 271 | `5c2d7a8e9ed1b1881a5a94bb44266330d3d80361aecd917ea81db7a5a52397b0` | 0 |
| rust/tw_hash/src/hasher.rs | 3794 | `7b5c2899cdca7878ba0a26637e74931d3ceefe2190c99d0ef14b1b2f5ac2346c` | 0 |
| rust/tw_hash/src/hmac.rs | 389 | `cdf1926f3eb7c9edee2edf673c0255f90058b630d8f0159da2d205da949502f1` | 0 |
| rust/tw_hash/src/lib.rs | 619 | `b5f25c1c637d81886b6ab658c7c600a510beb4c59314377e544215dba0ecf4cf` | 0 |
| rust/tw_hash/src/ripemd.rs | 966 | `3a08b7ebd729bdf87feda792a3283193bd243bf9567201d33564c3914fb47bdd` | 0 |
| rust/tw_hash/src/sha1.rs | 310 | `4780008adfebd168daa9a025d4c6a963fbbefaed0904074e8adb906a0e15422c` | 0 |
| rust/tw_hash/src/sha2.rs | 1103 | `d50987df8a1a230da745c868e4303b73f69a65bf28fe24dc0f5aee8046154bc7` | 0 |
| rust/tw_hash/src/sha3.rs | 904 | `0610dc6bf60933a43ac58833d76ac187713617aa6a218794f5ce658f7a81058e` | 0 |
| rust/tw_keypair/Cargo.toml | 1365 | `4b8f85a7631b91b3196924b1bf4602d447a3b5eb727e9fcc3a6b9529d2455924` | 0 |
| rust/tw_keypair/src/ecdsa/canonical.rs | 4756 | `b8d3c928f6e9ec85f9975a25a362f898fd0036708191e776f4cb05fde80b76eb` | 0 |
| rust/tw_keypair/src/ecdsa/der.rs | 8959 | `d7e702e506528f220c0fe81c188f5c3464ba988274906f2b42bc42dd6344d15a` | 0 |
| rust/tw_keypair/src/ecdsa/mod.rs | 629 | `a7fdf2d7533d15d57a1f03b3f6c9f519fd1ead5f81c61a7d3a47befa524aff0f` | 0 |
| rust/tw_keypair/src/ecdsa/nist256p1/keypair.rs | 1910 | `58cb7c0162a81f27442b0472c61418700df904b030bbf9aa991c5dfda2df7ae8` | 0 |
| rust/tw_keypair/src/ecdsa/nist256p1/mod.rs | 4310 | `3022e6b03c9425963dd9ef5b53ef2eb536fa540e2dc3ae94dfe538432d9eebc3` | 1 |
| rust/tw_keypair/src/ecdsa/nist256p1/private.rs | 1901 | `b5c4f93f39dd97a405d315be664a54f1b47ebc1c5c6ac0c24de9557989084416` | 0 |
| rust/tw_keypair/src/ecdsa/nist256p1/public.rs | 3037 | `56de85d3239a0f9ae8b3e350e94d8da862b9aa4ddd84de20f5df8c41c0412837` | 0 |
| rust/tw_keypair/src/ecdsa/secp256k1/keypair.rs | 1899 | `f1a50151dcff419b57dda39869ede8269fe4e2bcf93563322608e6cd1747cc5d` | 0 |
| rust/tw_keypair/src/ecdsa/secp256k1/mod.rs | 7032 | `7afd7578611b43d80cf70f0fc39cdcf0310a7924828740465cb4cb18391f8105` | 3 |
| rust/tw_keypair/src/ecdsa/secp256k1/private.rs | 3308 | `3945746da4805e9936451057e16b50fa298e15ac3c2421edb8ccef12181b4693` | 0 |
| rust/tw_keypair/src/ecdsa/secp256k1/public.rs | 4189 | `473872fd3b1bbe7f24e02e787fe788b835131372b6813c28d8b53b451502ec8e` | 0 |
| rust/tw_keypair/src/ecdsa/signature.rs | 7179 | `5e8ab6ed86cc3b968dae83870b33939a477fef6dc154874582bf9a1e9fe06912` | 0 |
| rust/tw_keypair/src/ed25519/keypair.rs | 1868 | `aebc17c9505a36a0f7e792cbc9c91b2375f9f51becb4e49a3da68d5e106143da` | 0 |
| rust/tw_keypair/src/ed25519/mangle.rs | 456 | `ed53c2b77e5092f3801d4d3eb6c4cd847ca50f8d8c49a166bd8a8c7269f6c246` | 0 |
| rust/tw_keypair/src/ed25519/mod.rs | 10676 | `be4d3ab91e65005c79ced863948808759610dbed4e1b0e4fcdba22b8f846623f` | 1 |
| rust/tw_keypair/src/ed25519/modifications/cardano/extended_keypair.rs | 2073 | `26f6d55dc32a2423ef3ae786e33317375af2bfa1199364f5e9a8379c61ca91dc` | 0 |
| rust/tw_keypair/src/ed25519/modifications/cardano/extended_private.rs | 5098 | `db1cb0acae3ee25a87290c17eda5f952987b914105cd15d66ca8ba2cc32c8cfa` | 0 |
| rust/tw_keypair/src/ed25519/modifications/cardano/extended_public.rs | 4022 | `3e430cfb4eb8b535715fcaec85d0add7eb271bc7255e1167f5eaf3f5d176d91e` | 0 |
| rust/tw_keypair/src/ed25519/modifications/cardano/mod.rs | 382 | `56a1463012fb6f97c8da1709f731841c715fbcd9aa7b976ead443584aeb49766` | 0 |
| rust/tw_keypair/src/ed25519/modifications/mod.rs | 110 | `8f01fb4e8cb418a482205b3171f716641588ebe77d16c3e013d1e84730174c2d` | 0 |
| rust/tw_keypair/src/ed25519/modifications/waves/keypair.rs | 1988 | `5d234eec1dd28f38c63e166dc898ec23b87a94e0c23556724e7bf50cb8444f8e` | 0 |
| rust/tw_keypair/src/ed25519/modifications/waves/mod.rs | 326 | `487447f37f65ec026c511907493ee380ffe31c195927ff6e6cef7c0029e89236` | 0 |
| rust/tw_keypair/src/ed25519/modifications/waves/private.rs | 1950 | `0d4519737088139c4be8fe0eba78df5dd6381251e7ed08e341f95b299df5a7cb` | 0 |
| rust/tw_keypair/src/ed25519/modifications/waves/public.rs | 2952 | `af2c09cc69a04845a96883a1c972ce2ff986f568ac023c4a1bc781018643db16` | 0 |
| rust/tw_keypair/src/ed25519/modifications/waves/signature.rs | 2440 | `2f60493e5fead95ed0d1c9d85c50062766d3ba6be057f8d9792ad14598bcfaef` | 0 |
| rust/tw_keypair/src/ed25519/private.rs | 2121 | `250a5720abdc0b6ed8af0c84b8dc1249d6985f11cd5f57b0ecc33d9c9f1f619c` | 0 |
| rust/tw_keypair/src/ed25519/public.rs | 5598 | `fb1a0ee5d9659226ab13fdc794bc24609e51f8a9f264be8eee7095e0fbaba746` | 0 |
| rust/tw_keypair/src/ed25519/secret.rs | 5694 | `0414c2c33fadcd5cd3fe63dd22628200f4e0afcd36795d4bfc49f35f1d86b632` | 1 |
| rust/tw_keypair/src/ed25519/signature.rs | 3535 | `ab3e43a29e362ba36376e10428b661d4d9ca9becfafd1166dc604a8fc554b5a6` | 0 |
| rust/tw_keypair/src/ffi/asn.rs | 1120 | `c09ac24000ccfc1b52604c6f804500267f8f0f03f1f4bc28d6af576fa93e0d4e` | 0 |
| rust/tw_keypair/src/ffi/crypto_box/mod.rs | 2807 | `8cd83bd9be9e542d0bfdcf14d5a153503c4c706ac92b465ce905255c4a0f162a` | 0 |
| rust/tw_keypair/src/ffi/crypto_box/public_key.rs | 2671 | `ed03737fdc59633578a8299b9ecdb20620713bc0b27f73db43643043b4cad087` | 0 |
| rust/tw_keypair/src/ffi/crypto_box/secret_key.rs | 3760 | `1a7c5a5fbc173e367cac7c55aa35918a01334c1327457e2b5c143fcfad45c90e` | 0 |
| rust/tw_keypair/src/ffi/mod.rs | 144 | `5ad31a7157673c75c8e955c34fe6686589d7e0845ce042ff1561ea6943e43555` | 0 |
| rust/tw_keypair/src/ffi/privkey.rs | 5287 | `e436335d30fc3bd2467809575fb40c41d08b1f3d7e6d16bcbcfbd368134a9ee9` | 0 |
| rust/tw_keypair/src/ffi/pubkey.rs | 3384 | `1e30d1780d766c580beab158e9188be11ab3f437b59237372f6853f7cd5411e8` | 0 |
| rust/tw_keypair/src/lib.rs | 2187 | `4cfe143bf009ba34f3aac81f6bf61e555dbb147fbd8da138b702583c20585c12` | 0 |
| rust/tw_keypair/src/nacl_crypto_box/mod.rs | 5235 | `64dae71968914a0dd4e9141ae5235e66997aaa557deecad58cd7d978e9c98aae` | 0 |
| rust/tw_keypair/src/nacl_crypto_box/public_key.rs | 1779 | `8bcac2acd89523d149214de72131cdb57cd1267df953b9547966f7c17dfaba10` | 0 |
| rust/tw_keypair/src/nacl_crypto_box/secret_key.rs | 1410 | `821d9db2bfbc4cc0ea9771254378eced198db96a1aba6d677c7b68abcb25153f` | 0 |
| rust/tw_keypair/src/rand.rs | 138 | `d770e8dd92191e8db4541671da5fa7b5879ccf7139de0775697de79ada4ef984` | 0 |
| rust/tw_keypair/src/schnorr/keypair.rs | 1904 | `07ba9df966abd65250eabdd9d8574e8bbdd1f38fa5c004698352524b0d99b317` | 0 |
| rust/tw_keypair/src/schnorr/mod.rs | 4278 | `f473a633ec1016cd1a66e2719752deb48e8354b1a5c7389f08352970134ba481` | 1 |
| rust/tw_keypair/src/schnorr/private.rs | 3149 | `e841c138492453253c0117ab5b33bc9767de2402957e5353567775965c2cd69c` | 0 |
| rust/tw_keypair/src/schnorr/public.rs | 3061 | `aa29aa38b286f8f02e4dca01f9642b219d371dd253291c7a3c60b438168d91d5` | 0 |
| rust/tw_keypair/src/schnorr/signature.rs | 1075 | `bb941c181b5c85484326ccdeadea7fec7a69391b336f3cacb2e37d30b74168b6` | 0 |
| rust/tw_keypair/src/starkex/keypair.rs | 1806 | `d08f3f80652e947c5d85b02aa5905d13a64eee1c5e80ce22b5dd3fb7d6eaef94` | 0 |
| rust/tw_keypair/src/starkex/mod.rs | 4314 | `48b260d92938db8d4b253d73991e4e17c41a2f164d52c8de1966d0baec866f38` | 2 |
| rust/tw_keypair/src/starkex/private.rs | 4089 | `175b7158e2dcf8a24bf511a0747ff6c090ae1ca2c38251cae1131bc2535c87ae` | 0 |
| rust/tw_keypair/src/starkex/public.rs | 1919 | `3c814f311529b144ff07a23a186f3ee432ad379e8a0449400659642353954454` | 0 |
| rust/tw_keypair/src/starkex/signature.rs | 2413 | `60d502052086915cc93ec66c1e44df1b3e5c0e8d3c706618bd5f49a3fa4485db` | 0 |
| rust/tw_keypair/src/traits.rs | 1027 | `650018c38f960ae97817236cbc2ad55f9a39a464dacdc2ff48013e0dadfdfc8d` | 0 |
| rust/tw_keypair/src/tw/mod.rs | 4160 | `ecff410985222437b3ee125fa2f6c17d1b829b2e75a3ffd4404394eec32966d3` | 0 |
| rust/tw_keypair/src/tw/private.rs | 8770 | `cf220e0853c15c3abbe23df891ec67cab8b3403e7bb25fbdcd4276326b30ccf8` | 0 |
| rust/tw_keypair/src/tw/public.rs | 8090 | `3db5af0c4e5027693e88c457892c285606344f466e20535c38a0c49f9dc60cdd` | 0 |
| rust/tw_macros/Cargo.toml | 295 | `31cec8f3f400ef10fd8db5274c5e300b4d307bbf61bfd73389f1c5b527a2184f` | 0 |
| rust/tw_macros/src/code_gen.rs | 656 | `5a7d12ae0fddb7454c8fe24fba1b3608e4526a5a1f9d8593b196b0f50dbb2180` | 0 |
| rust/tw_macros/src/lib.rs | 302 | `5b09ce412ad1fdd16d84ce5555a7437158d4557d4d840113776019ff2c850d77` | 0 |
| rust/tw_macros/src/tw_ffi.rs | 7739 | `e6a20d7869b7de8d5d583f0bc3a40961c5604929697946f5f670066fee3d2e26` | 0 |
| rust/tw_macros/src/utils.rs | 181 | `40a27c422ef223dea5e87187933696865ae9a5578f1b6b7097a8d660c2a3ee21` | 0 |
| rust/tw_memory/Cargo.toml | 108 | `2388b019723322f650fd609407b6b1e4eefbc5b8908e9eb1707d7c343c5b927d` | 0 |
| rust/tw_memory/src/ffi/c_byte_array.rs | 2991 | `dbdc533b0d63d0f57158e3a121f579be412bd8471ee4ffffdc97f134d14e4e32` | 0 |
| rust/tw_memory/src/ffi/c_byte_array_ref.rs | 1041 | `0aaefc368bbef345a799e270afed50d4df27a89abac421f1cfe68dc1505db884` | 0 |
| rust/tw_memory/src/ffi/c_result.rs | 2888 | `805a1f02ac0f26fd31cfe6f919953202ee2b6229a25269ad81188b4377347549` | 0 |
| rust/tw_memory/src/ffi/mod.rs | 1500 | `5b5a9d7a916df0afbfc1b85fb4b2b414f431b6158e4fee00b4e1fec69e83e03d` | 0 |
| rust/tw_memory/src/ffi/tw_data.rs | 2717 | `5a938084fe28b04847a8fee147c2797dc821c8f622a21927d35a350880272b72` | 0 |
| rust/tw_memory/src/ffi/tw_data_vector.rs | 1951 | `55f698716f9d91a98e35c799a7c5b32725a7d9734f4f592e89fdbdb558d021e5` | 0 |
| rust/tw_memory/src/ffi/tw_string.rs | 2980 | `b1500c7813de4c03c448fdac0e93d4a86b9f38b9e94f1932d520a97b60758ac8` | 0 |
| rust/tw_memory/src/lib.rs | 389 | `ea8197f40290cc2771c7a7a55c6e1eca7883218955ee8a53f404d2a8fb904165` | 0 |
| rust/tw_misc/Cargo.toml | 263 | `57990c84dc8dc670d265f9079d58fe71e1d45a370d1431f6fe4a578990e92f8a` | 0 |
| rust/tw_misc/src/lib.rs | 202 | `a3c6724dd611f3c6f1c98e65ddde590550034a7a47ce5a598bd581e51fa35303` | 0 |
| rust/tw_misc/src/macros.rs | 522 | `9dc6d62091e6685b230a896cc9390d99979629c31860cfe2eef5d20be9775aff` | 0 |
| rust/tw_misc/src/serde.rs | 4117 | `653a181b0e23f9d62573e7bae75010e35884823566d0106744b6142e5f954907` | 0 |
| rust/tw_misc/src/traits.rs | 1730 | `aa399f5b3e6fa6d20b6817e6e2e095284808c75cfbb1a506856af6e6b804047b` | 0 |
| rust/tw_number/Cargo.toml | 558 | `a3c202bec9fd2d7191bf0e6796aa5e96f351123efe71f3fbb5024ce01e52d62d` | 0 |
| rust/tw_number/src/i256.rs | 14041 | `cbb0cce6fc85361b1621b14e6437c6cdfa4ec5053e0de6090cf49eb5f8ee3189` | 0 |
| rust/tw_number/src/lib.rs | 1708 | `8c4eb2b1dabe9c5e845d7feda3899acf725d2649eb55260dd1da698b0f693e1d` | 0 |
| rust/tw_number/src/serde.rs | 322 | `2b661b0433a11b954b12494085cff69b7edbe1db6b7c9a4ae1f67d1ec986ca71` | 0 |
| rust/tw_number/src/sign.rs | 911 | `c0cfa9ca90d25375256c6128839c7fe7d8860e517702a5383747a193ea96a2d7` | 0 |
| rust/tw_number/src/u256.rs | 8745 | `1e76adfc09c12dcdb95d736ad38efb77d89a9d96d826f1892cdb65670f72b773` | 0 |
| rust/tw_proto/Cargo.toml | 275 | `cdbf697cb4b43617bd28bc8cf36b2fbdd6042e0a35b8b492bd7cfede76d3ed44` | 0 |
| rust/tw_proto/build.rs | 3967 | `53a19b6136349c32e18fa2de304942ee0a34273025d1f4600f873b963292263c` | 0 |
| rust/tw_proto/src/common/google/mod.rs | 96 | `ee57b7f70ee243047ab0f17ac5017648c6aa1beb422809355a14d17ed5df6085` | 0 |
| rust/tw_proto/src/common/google/protobuf/any.proto | 6610 | `759e80afc302d7d653357ad6af3711799b19c5fd96757e3241d4741ada4b8d6e` | 0 |
| rust/tw_proto/src/common/google/protobuf/any.rs | 1788 | `3a7cc7fe735bdcf3a5ef47c91d4303b0570aa0a730775844e00f61caffc64148` | 0 |
| rust/tw_proto/src/common/google/protobuf/mod.rs | 141 | `f41609daa9000ee41c4c6b39e87949801ff188318ff31a61719b4382225875c1` | 0 |
| rust/tw_proto/src/common/google/protobuf/timestamp.proto | 6865 | `8830cea869c8ed60b47c4ac71065cf4d0caf7b1601fe33e2204519da7f1563aa` | 0 |
| rust/tw_proto/src/common/google/protobuf/timestamp.rs | 1689 | `a2319c1fb118d838d11ade0ce6895d3c9d7d618b3176a1d07aa918c27eccfc7f` | 0 |
| rust/tw_proto/src/common/mod.rs | 94 | `0948618c885272d31c68f3254120f4c7280c788251306ac5729f2fbc42e0d8d0` | 0 |
| rust/tw_proto/src/impls.rs | 3909 | `255196f3b7269f7dd29d5fc3f8f8b133ead1e9af5331c96deef12994aa020480` | 0 |
| rust/tw_proto/src/lib.rs | 2665 | `45b3d243ddc6c5071b6fa13edba5e674c8506b0449e16f59295fa45c761c95bd` | 0 |
| rust/tw_scale/Cargo.toml | 151 | `1aa31660143c7e9d3a20e0716d2d3f54a33793d7bfada9e6c1f91c69e63a3ad0` | 0 |
| rust/tw_scale/src/lib.rs | 15712 | `1e0a84ec23ac603f9e0d5450cddbe269774d83ef2198ba624954a51953298fcd` | 0 |
| rust/tw_scale/src/macros.rs | 5442 | `22134c00ba5dd6db04fc961327d23cbd4fe941d825976f0831423c221288c3bb` | 0 |
| rust/tw_ss58_address/Cargo.toml | 373 | `102f3b0fa728233032391c6bd2691135849ae6544cad66efe42c186539f174cb` | 0 |
| rust/tw_ss58_address/src/lib.rs | 14980 | `9ec9f7e3d360f0901f804e91d00fe8bb12edcff4c1597ce9d65a0ba3bd057eee` | 1 |
| rust/wallet_core_bin/Cargo.toml | 171 | `7ce1e77576a692244721f38d7a46ee6396e4eb20f4c56f67a7ec4074781d456f` | 0 |
| rust/wallet_core_bin/src/main.rs | 816 | `8554c5a7ba01e59511dc4a65961f4f4384da9cdfc664db6e86e27b23064cc8ba` | 0 |
| rust/wallet_core_bin/src/registry_stats.rs | 2311 | `667ed3a56b9817a1f4c49de723a8a4c84d89242d50a5a2c2a550b9527e2c9fd5` | 0 |
| rust/wallet_core_rs/Cargo.toml | 1527 | `3286e5164f4947a6b99ea1b72332f15b179e9cb616804a512e22b3a2e27a6e8a` | 0 |
| rust/wallet_core_rs/src/ffi/bitcoin/mod.rs | 77 | `ba85c55afc25ade8f5e54d06d6a020a2419ff1d5b778e2d4ea76ffd7c2d671d0` | 0 |
| rust/wallet_core_rs/src/ffi/ethereum/abi.rs | 5584 | `4df62e3e258592b325d76c0350fdafc61691c5b4a65bbd16630dfec974fba5ea` | 0 |
| rust/wallet_core_rs/src/ffi/ethereum/mod.rs | 104 | `b9215bb25d1844d7946bf42378a4f8ad242f014052119b35e736b29fde86f42c` | 0 |
| rust/wallet_core_rs/src/ffi/ethereum/rlp.rs | 1072 | `994c0d1763212d5e6e95354b924e5db6cac70b12a02b8424b4c28ac2c04db71a` | 0 |
| rust/wallet_core_rs/src/ffi/mod.rs | 291 | `7187709997e8d3f06e2e7538125f98af51ffcbabcb766121169c0881ab1e57c4` | 0 |
| rust/wallet_core_rs/src/ffi/solana/address.rs | 2629 | `56b2499083b4904c1bc6d5e3f63b877fb15305bbd98594e2875c550e509a0f8a` | 0 |
| rust/wallet_core_rs/src/ffi/solana/mod.rs | 116 | `e0a728bd6704d754beb536ed42a2e89178a2437e83113edce9d92dc06cbcf1d7` | 0 |
| rust/wallet_core_rs/src/ffi/solana/transaction.rs | 10728 | `cdac4233f98e8f7bddb38f1e9ace7180898e085ff4a04a09b62e3a89544b3761` | 0 |
| rust/wallet_core_rs/src/ffi/ton/address_converter.rs | 3385 | `f9c08ce057d0cfbcce4cc82fe5ed5d150aa17b157d0ac5f4a6f1567ede4f81a1` | 0 |
| rust/wallet_core_rs/src/ffi/ton/message_signer.rs | 1799 | `3119bea6377b3344c1403484ce159706cb3ad604ddbdd17079b1b02fe93e5c5a` | 0 |
| rust/wallet_core_rs/src/ffi/ton/mod.rs | 145 | `0568c0b12d2ab7bb2796e77d428bcbafcf75a55eafb327ef7c4e21a89400fb2c` | 0 |
| rust/wallet_core_rs/src/ffi/ton/wallet.rs | 2535 | `e8d44ecfb5bdee2943525e829f9a6793b5362daa2f374f4f19b7c7ad945585b3` | 0 |
| rust/wallet_core_rs/src/ffi/utils/bit_reader_ffi.rs | 5191 | `7b95ceeaff35a4616e18abfdd8ab3096005f8e6ed625c0c4bc52088f4113de63` | 0 |
| rust/wallet_core_rs/src/ffi/utils/mod.rs | 120 | `11ecec896ec34a072bf269fa093442eb3f1d833d370ce1a0b8fbaec4c890f1e8` | 0 |
| rust/wallet_core_rs/src/ffi/utils/uuid_ffi.rs | 455 | `f3c9ecbf90c7af03f3c97b4da435bc628f007f03e3cb223acd84acd0bd587086` | 0 |
| rust/wallet_core_rs/src/lib.rs | 476 | `435b602ce91ae01b493cd2c7e3b1541629847ef6251dadbd3e795af5130b1450` | 0 |
| src/Aeternity/Address.cpp | 1604 | `801289cb9210c6cc59c0782f30d430ec854b0a9f7f939a62be6f9f20f76e6fb6` | 0 |
| src/Aeternity/Address.h | 817 | `12a66896336723dccc18ae4b83119bf32401667912879c9f5af9fe4b7169e681` | 0 |
| src/Aeternity/Entry.cpp | 935 | `111bfa5d0752a0fd766c1c87d07afe479c18e742eef241ed74c3aa622ea97b31` | 0 |
| src/Aeternity/Entry.h | 730 | `fc9343378a96e4cd7cb16c8a18ca7fcaee702cbe403f73c4961d17f82d953ef0` | 0 |
| src/Aeternity/Identifiers.h | 1034 | `7eab5f8f8a037249aa78b48bae8eb3d30f0abdd6fce28ac6a109fcbabd87a4d7` | 0 |
| src/Aeternity/Signer.cpp | 2993 | `d49e76f1c19162ab87113c2e23418e4c1d7b37144e5576240e7e5768c77c6f8e` | 0 |
| src/Aeternity/Signer.h | 964 | `a5bf59d17c3957b8b88b408fbde201d5fd1ab0ab08d3c949ec65e71c4cacfdf9` | 0 |
| src/Aeternity/Transaction.cpp | 2036 | `15fee1225cf78a04b1d3681c12108f71221d3457804dec0e033f6a08d8c0e779` | 0 |
| src/Aeternity/Transaction.h | 1141 | `a92e452f26e02f5189124eb4773644fa966134f54f4554203518000704f722db` | 0 |
| src/Aion/Address.cpp | 1077 | `640ce27061eac91959f9d5cab6b658aff8e14277fc7fdb31845ec4444e4202de` | 0 |
| src/Aion/Address.h | 1113 | `d5e645ea6fb3c17a4bb7cd175dcf2396893531c5689c73adde21df8398621961` | 0 |
| src/Aion/Entry.cpp | 2460 | `04ae76a29d069873a4b3468a9e5f7d59c0e687e3b96d05d5d4a82709e7e96373` | 0 |
| src/Aion/Entry.h | 953 | `a6eb358f4932c7b36129d90d5cb5588fe582d63ae478664d378d6d662b7ee02a` | 0 |
| src/Aion/RLP.h | 934 | `80b33209dbcc25cf0d4e3278eaa529d167d8eab82958929bb96b10ba28585125` | 0 |
| src/Aion/Signer.cpp | 2636 | `af20c013f3cda84f878ec05ec085c32b70e8d804849afa734ad666e67dcff057` | 0 |
| src/Aion/Signer.h | 1067 | `80aab4120c2648a520f297a66680adebb0098dc74f8bde85619b9e35db7bc79a` | 0 |
| src/Aion/Transaction.cpp | 1300 | `4f94c3d408e4a932c4b16d25a42ade838cadb4d9c1e3148a59ae7365b1538408` | 0 |
| src/Aion/Transaction.h | 969 | `521d6569ce34840036aec98e82545949587050a88c821bf96534c71c255ffa33` | 0 |
| src/Algorand/Address.cpp | 1889 | `ee0c9af616aa4725c0f72de4f30b8866b35419db93ff059191efa8b2c8ab4b23` | 0 |
| src/Algorand/Address.h | 934 | `bc008fb722eeac40d8abf13f0fc2e6c37ecb1dcf9d62b80cdf22a3b280ed398d` | 0 |
| src/Algorand/AssetTransfer.cpp | 1289 | `1901c1415b786c1f9c87721a1a95c5bf53bc751f0506e286fbdf832c19371945` | 0 |
| src/Algorand/AssetTransfer.h | 1069 | `6fd4a76ab2ea5d60dc58a6248c1b84a3208202ac8ca7d0a118890b7adfc5863e` | 0 |
| src/Algorand/BaseTransaction.h | 862 | `17c8b8e951ee34163b82e2735d02693e8f7ac4b10d8116fab669a4200e270820` | 0 |
| src/Algorand/BinaryCoding.h | 2687 | `a21a6e54ce09d68834e0be1a2f17c0b96eb275458b0014e24e0da90c6643a138` | 0 |
| src/Algorand/Entry.cpp | 2489 | `f89014acd1ab222d8ba75799337e7eaa131386126608b0cefb0aea6b7d825875` | 0 |
| src/Algorand/Entry.h | 1106 | `62a722c9178f4aa64669acc054fa1cfd3403ab5f93437328417869ff86b052c5` | 0 |
| src/Algorand/OptInAssetTransaction.cpp | 1255 | `7da88ca8e858a28b3ce0e0e5449af47e538fede17085d47cf8006ad27aaed309` | 0 |
| src/Algorand/OptInAssetTransaction.h | 1022 | `95aa52d727c212a31f1a377851b6cf944d1800b2727b442ef42125200411466f` | 0 |
| src/Algorand/Signer.cpp | 5773 | `dd17bf2cfca0668ef8851c37f64330d1100c98eb3f8a659bcde0da85af8418d9` | 0 |
| src/Algorand/Signer.h | 1284 | `35cc2fa6953d423005c34de371c56285cf919935a565df1bd39f6a5ca59dfaa3` | 0 |
| src/Algorand/Transfer.cpp | 1602 | `c779835ce9a668ab57e59a68470e3b2910f4a04c3b50cf583c70dd42f95d77e3` | 0 |
| src/Algorand/Transfer.h | 1011 | `a6a407871d8f3d9ba76155ddc13070a9e10ed58852702f37d8ba621e5cc674bc` | 0 |
| src/AnyAddress.cpp | 1023 | `a1a35a791fabcdaf8bb65626834d2a23672d6c61a21e60a1c57dc43078655906` | 0 |
| src/AnyAddress.h | 1204 | `663c8539ca1c19fa8716e87575160043d767c7b8a0fa8c33b5998b9d294a9247` | 0 |
| src/Aptos/Entry.h | 397 | `57803892b1e2f7de635a0275c1163f59330b3c2ca6f66aeb7b09bda35d746a7f` | 0 |
| src/AsnParser.h | 560 | `2e54aeb4a84a2ca6bb2a41e907b01864e1700b3cab755d3fc272bac36a73811b` | 0 |
| src/Base32.h | 1283 | `479ec4d263191f15bb660502a64973394a15241ff76728eec0c7c6d87bfb2b32` | 0 |
| src/Base58.h | 2329 | `9badc6078c14d4bd7bcdf2ffb324688f5a8de2c9ce670c4431f8243a6cfaa1a3` | 0 |
| src/Base58Address.h | 2902 | `0bded19f183f268662826fd44928edbf7a8d68bac4bd940f2c180968ca490bda` | 0 |
| src/Base64.cpp | 1915 | `53a910a00a280c7a39b53f84dba6c417928444e76026a8b2fb75b937bd6c7b22` | 0 |
| src/Base64.h | 745 | `548649a19198d69e81b59af023515bab6373e64debbb24f7c97a754e8602698a` | 0 |
| src/Bech32.cpp | 5315 | `3cdb3daeb06963218b9b2285e302c2287f15b8c40f04ed2290300f1d7dea0354` | 0 |
| src/Bech32.h | 1527 | `8f680b9e50f6f26d449a49a2bee66fec095d6c828c3bba81749e6eea6e5b8bc9` | 0 |
| src/Bech32Address.cpp | 2248 | `a96c3ea20211a835b40b0e9f8e38df2ba2608fb6d880aaac54d1297abf856e5c` | 0 |
| src/Bech32Address.h | 2235 | `4f634260e7596de87331a3ac5ec4923267f4cee3531750259ae901dc986c99ea` | 0 |
| src/Binance/Address.cpp | 1342 | `6a612174a41c61698617912cf34c2a33431a4f11c214a6f0a8bd0852a8ed0b34` | 0 |
| src/Binance/Address.h | 1601 | `b4e3751dea906d61cdd9ce661835eb0ec30368157f68487a5236a80a56023af6` | 0 |
| src/Binance/Entry.cpp | 501 | `cc8df7421c7d0d5964fcc38e7190ff661bff60ebe6eb1c326ef96b2c67fa27d6` | 0 |
| src/Binance/Entry.h | 564 | `ef46665250941717a17f3e2b6af5b72e40045677947e1945d309f95355febf55` | 0 |
| src/BinaryCoding.cpp | 4892 | `d83e6fdd0e5fc6fa7b7dc8620505918ba03086100eca7ce9b7138d45bfaa3f5a` | 0 |
| src/BinaryCoding.h | 4189 | `d5db449f99b0a491ea1622239589ccdab9d6ecc9c8cc5675d1e9c81452cc79ed` | 0 |
| src/Bitcoin/Address.h | 928 | `1aa82b62b4a81e1053b5789f5b36f6dc6b626fbf47e7228fd9f20cd0fb606803` | 0 |
| src/Bitcoin/Amount.h | 327 | `f564f62bde79fdd88c2aef0d88c37fd8120f60ee1b5ed154387c3c8d76461815` | 0 |
| src/Bitcoin/CashAddress.cpp | 3724 | `2523d2d4eebfaea093e65900d076fb8a5bc9c47c594f14346e3c078e43a7c296` | 0 |
| src/Bitcoin/CashAddress.h | 2553 | `7619b55e9168287273506f7f41aeb7e3b0f4768a47d2e22bdd72605d719ad2be` | 0 |
| src/Bitcoin/DustCalculator.cpp | 1070 | `31b55319a7f49e2a493ac21abfd1cf465acb7bf1b15223d292bd93d72bdaee9f` | 0 |
| src/Bitcoin/DustCalculator.h | 1365 | `b040fa872fe2464beb80e27ae0d045f45813b6d4a793445d2f62bfeb10bc0f25` | 0 |
| src/Bitcoin/Entry.cpp | 6327 | `6430f31d9930cbfabcd698c3acb7217722373e018ba3f3d3f4ba1659529e2b44` | 0 |
| src/Bitcoin/Entry.h | 1551 | `54e0bea20a4b7efe0acab86eee8dfc41fade70e83888ce08b42bd0475d349ebb` | 0 |
| src/Bitcoin/ExchangeAddress.h | 1274 | `05961c9aaf31076a6a3c411c99b6e157ff60f266b15081728d5f710927b9f247` | 0 |
| src/Bitcoin/FeeCalculator.cpp | 3354 | `21b0f78b3e0f07e6f2193575c444bf117a66e99e0c6e454639225376c18e43f9` | 0 |
| src/Bitcoin/FeeCalculator.h | 3998 | `ab4f8700fc88851a98bf1f8869115e26c32f423b3769aad746724d67b27c8327` | 0 |
| src/Bitcoin/InputSelector.cpp | 7996 | `865929affcc9bdbbd4ec3ce79d4b067b058e1eb2acba6746a734655330589656` | 0 |
| src/Bitcoin/InputSelector.h | 3225 | `47e82dfdee0b9ae0b992fa7a826b2fe5b3b192471c5f8050ac55ce90c8d20dc8` | 0 |
| src/Bitcoin/MessageSigner.cpp | 3999 | `7333ae7c1a13661cc43a00b8818201d8833776130d0b9884b407cefa80272cb4` | 0 |
| src/Bitcoin/MessageSigner.h | 2525 | `b646658fbd55603b50cbd225e4f961a1c57b4cd7d01c3dd2ae96422bf60edccd` | 0 |
| src/Bitcoin/OpCodes.h | 4767 | `5836a32008492aaaf200795e07def7d2e40223742fba60808a2172a3c11ad08c` | 0 |
| src/Bitcoin/OutPoint.cpp | 418 | `4e2796bf41261a49f6e24329663c9272f6082353dcfff9b9ec79d3dbdcd4972c` | 0 |
| src/Bitcoin/OutPoint.h | 1721 | `7c5952d30385bc1a84ebe444f7ce5619a5b933206efb0a3f8333282c1487e253` | 0 |
| src/Bitcoin/Script.cpp | 19270 | `70f268a7c4d008f3fb557d08d593cc3ae844f768169fc2b4eada4c5096af1193` | 0 |
| src/Bitcoin/Script.h | 6493 | `50ea0585d7341cfd53b9748d872be549e9c397ff31efee8d21163d5b471a8ad6` | 0 |
| src/Bitcoin/SegwitAddress.cpp | 3203 | `88333cd34bf344e1d3a842686a4fb866e7fb5c31dfcfcb6f09d4cbc42e5c3d9a` | 0 |
| src/Bitcoin/SegwitAddress.h | 2567 | `5f2c1eeee2dec38f5336b7612e21bc1de63bf3d5640e3197d41c14222ef65543` | 0 |
| src/Bitcoin/SigHashType.h | 1298 | `938aa365dea08985e1ada7adef88cbfb9dd737e1edd29bc1c859c99cdb52d2a3` | 0 |
| src/Bitcoin/SignatureBuilder.cpp | 14754 | `8d4d4a854bf501a96879055e4066573eab5df71eac61b947651b918ba98f3581` | 0 |
| src/Bitcoin/SignatureBuilder.h | 3253 | `560f04fbc77cdd90fb21fc3234a918d8e6cab5464d1f5c76b943cdc94af6cc08` | 0 |
| src/Bitcoin/SignatureVersion.h | 195 | `db082fd74bfdac57d1ec2ae292093fb61fc3b3cfa2828cc655a2428a5c2a8b73` | 0 |
| src/Bitcoin/Signer.cpp | 7458 | `bcf3fe9c3af3fe39a3b894ae1ac94ac5928351e45d96239c4b9d055bc9d23400` | 0 |
| src/Bitcoin/Signer.h | 1950 | `ecd9e07155e132ac7a7ed53487602b42cb1f582261d7e338ef49762d0312d573` | 0 |
| src/Bitcoin/SigningInput.cpp | 1666 | `90c439e9ba557326d3dfbde4b1db4b8be01804fdacd982ed9c6734343e6307ff` | 0 |
| src/Bitcoin/SigningInput.h | 2389 | `113d090ff9ad2aa3e7ad256eb3d846d196869db1f96b3389ed36f8f862c1dab9` | 0 |
| src/Bitcoin/Transaction.cpp | 8304 | `fda9e19f9431ca03332f9d8a077758e27d7b7640f31008558f3f6b2b218561fc` | 0 |
| src/Bitcoin/Transaction.h | 3903 | `4d31f1558fc82518a76b19ed7a54c56b04aecfcdc1582f13eab8b5af035c015b` | 0 |
| src/Bitcoin/TransactionBuilder.cpp | 9993 | `bdf26baab18a8b85bbe4a9d778bf407e7c9396fc3d09b7df5dae807a40074ba5` | 0 |
| src/Bitcoin/TransactionBuilder.h | 3373 | `8e2d5b351831f533188f56410a1c0936eeba3f4369cab514b29c7b528be4c177` | 0 |
| src/Bitcoin/TransactionInput.cpp | 684 | `7a936eab42f2152b7653c4943ea91c79b9f465ae9d2d249f8c40d8e95cc62d79` | 0 |
| src/Bitcoin/TransactionInput.h | 1218 | `b45e54cc067a67d17cc8d03712d8b1104fcfaa5cc690a1738d5e96e0a8304994` | 0 |
| src/Bitcoin/TransactionOutput.cpp | 300 | `62e35a155b4db1cb6ec01ca75459a05e7087cab9158bb98d643fff12683f802e` | 0 |
| src/Bitcoin/TransactionOutput.h | 825 | `5998f596f9db5d1debc3d4230cd26bfe12097b3fe1e1ed55539c2fab6520079f` | 0 |
| src/Bitcoin/TransactionPlan.h | 2711 | `a120edf75e485a4f55f80c6a34fc70d7ddf5d4842dff48e432703fe1bbb66e70` | 0 |
| src/Bitcoin/TransactionSigner.cpp | 3434 | `b3b01f2046dbea00dd6f583e4e06149887e7e7a3bf0befa425416ebf7349610b` | 0 |
| src/Bitcoin/TransactionSigner.h | 1099 | `ad209dcff63e4bbe65636f5c2c11d4e57b71ca220bbeca1e373fbdfecf38800b` | 0 |
| src/Bitcoin/UTXO.h | 1167 | `bde80dad55cf8cb5ca27296885fec2b8b6f53b4851b7c13dda7f6d18bf798747` | 0 |
| src/BitcoinCash/Entry.h | 618 | `c12e50c9e501857a49884a989fd4665b71d3c9a2994acb8a7380c52f37f23a62` | 0 |
| src/BitcoinDiamond/Entry.cpp | 3763 | `aab9d48ee3ba037a23184c11e15e9cc7d414b99bd2c11f3d566f26b69a60bcaa` | 0 |
| src/BitcoinDiamond/Entry.h | 1189 | `eb5b592f870c72ed2a4d78fddfb1ce21d60ec92ab1c335a9aa26b80920dcb74c` | 0 |
| src/BitcoinDiamond/Signer.cpp | 2106 | `e56a90f9e6cb08743ab3bf4c953e53591ba50787eb67758de0d1c4d74dea8794` | 0 |
| src/BitcoinDiamond/Signer.h | 1048 | `804b3d219d5145dfd04ff699475818b09f67eaf0505853d4d5f5ea62a64fc365` | 0 |
| src/BitcoinDiamond/Transaction.cpp | 7344 | `e5e9f18cdc3c588e7dfeca662a0a694e2734bd433e55364e84048067e6be1991` | 0 |
| src/BitcoinDiamond/Transaction.h | 2146 | `d874bd6d164f72512500cdb6b703372f6553832d05e78532d0f270b267aaae3a` | 0 |
| src/BitcoinDiamond/TransactionBuilder.h | 1357 | `7a994006b6e4ef193f1fd8dc14f46b24ede87e96acc45119e363bfa1283982c5` | 0 |
| src/Cardano/AddressV2.cpp | 3740 | `f5db535e2bcd558437be7f6e6277dc26f78ff6635f36b592100167ad2e348922` | 0 |
| src/Cardano/AddressV2.h | 3123 | `13bdcb3d8a1c1c5adf81878d2c29cfd8048a6126455a7bdf75a7bfadb592996c` | 0 |
| src/Cardano/AddressV3.cpp | 7383 | `80a901aff8764a46ce1d81792655ec84e82cb712c39ffc37cb7a8e25852b76b3` | 0 |
| src/Cardano/AddressV3.h | 4242 | `f212f522cab89cf5fe07c96ca5671ddc1db58c0a4adf4d3bb7b2bfe6da138f3a` | 0 |
| src/Cardano/Entry.cpp | 2682 | `f3f8322eb202c4c1766ee8166779a9bc20559935e35c7d6b9624d3aea9d60b7d` | 0 |
| src/Cardano/Entry.h | 1106 | `f185172fb638ab324b105fb00098d3b972ef87eb63a0534872a49d212c1755df` | 0 |
| src/Cardano/Signer.cpp | 27018 | `3dfce78f285ec1f8bf84759a12d9ddf3018bb7cf741ff9e343ef4d189ceba48f` | 0 |
| src/Cardano/Signer.h | 2343 | `be5cc978dd35fdbd778e9f8ac76bfcbb3056c99c8a1323b2cdaa6073713c2dcd` | 0 |
| src/Cardano/Transaction.cpp | 14606 | `c5a77a01a1ee16926b85c6b77e0879740754b5a8a3af312937be04a046760df2` | 0 |
| src/Cardano/Transaction.h | 5955 | `77a900024c25c69c32c74a1af5bf3a085f24ca0fc342a7dc18bdfa0b21b5d283` | 0 |
| src/Cbor.cpp | 15929 | `25baac5b934dfc23cc5235686f73454c36d97fcbc308d4f8cabf7660acfa6319` | 0 |
| src/Cbor.h | 5398 | `f0de70eb2f27d325d805e3629a388fa921be10ccefadf7632f30bf3f1ff1b0ac` | 0 |
| src/Coin.cpp | 16004 | `374e7e62dc1a86899eeb3922f6457aa9de96c330496c2c6544c982bbb5deb89b` | 0 |
| src/Coin.h | 5891 | `ab2e8134de77767e8abc0700bb1fe212ffc9218177e8601f5c7b61b721ac87ca` | 0 |
| src/CoinEntry.cpp | 1157 | `564ec6a6ec70e8b75926af3db87fddf098bd7d69b43def707dc8c9007aa474f1` | 0 |
| src/CoinEntry.h | 8081 | `9c76abc1b8940b1fe1ea7a920442c959cddc9db90c578ec130858ff8604899bb` | 0 |
| src/Cosmos/Address.h | 1891 | `51e486c5ffb32bb2fd5af6b174e6926d044ea0a626894a2505165f8da31786d8` | 0 |
| src/Cosmos/Entry.cpp | 611 | `41be91c8aff90999c6815e3245c318387a447c84d509d9e20b3882f23fe0a377` | 0 |
| src/Cosmos/Entry.h | 604 | `bc8473c00da20b55f516d6c7386610d82a2d8fbc05057c5e0143986215065870` | 0 |
| src/Crc.cpp | 1501 | `a0efda0b9200347b8af41885f39e76c0751826fcc78f1c8d7bec9c3dd1d33333` | 0 |
| src/Crc.h | 6447 | `817758731e72220e0d86141bcadd8bca0bbcc747f86378ba8835d9c9c61544eb` | 0 |
| src/CryptoBox.cpp | 2640 | `584b75ed18f6c628f4a76fe4c72d618de62050f187d887cefdf2a3898fd0799e` | 0 |
| src/CryptoBox.h | 2195 | `2b0577e3440f4d67b2c298cbef7041ac131e96404b7ebac7631a9c3a468dd94d` | 0 |
| src/Data.cpp | 1143 | `2ff9733bd3f953ec0c9eeacc65863f0244b87c0b93ddffb51c74abed9bdac471` | 0 |
| src/Data.h | 2591 | `a4aad9bae051e000500f1fce5c81b19190267ca073d825d0a8cb7c9d39e77950` | 0 |
| src/DataVector.h | 650 | `1dfb8ebcd0d58423f816698bc72f06fafdbec9a8eecf6e70b16b54f9e91e1f6d` | 0 |
| src/Decred/Address.cpp | 1644 | `04cd3db1a3a9d3b4c8b8087e79afd9bdad4fc163cd27485f051d27c25ebacfa0` | 0 |
| src/Decred/Address.h | 850 | `ed9174dc40045323d4f51468b6377f3cde02034335c4a7ead0cf1decb6bb5a74` | 0 |
| src/Decred/Entry.cpp | 2718 | `c665da52b79b03377a6b02f84d56f8d9b1b653a100b5e634626e96b5263b6c80` | 0 |
| src/Decred/Entry.h | 1081 | `663ff05ccf76e20fb22069ad5228f496bfd893201f91eddd3ba9f413f98ed4a8` | 0 |
| src/Decred/OutPoint.cpp | 375 | `ed830fac1efd360c873dd517d14bb502602482ba3d84065c7f51bd8c040dd0e4` | 0 |
| src/Decred/OutPoint.h | 2170 | `0e13527374e853d4685845e89e3f5ca1b11151d79a6d1314c86ea8cdb535d3c0` | 0 |
| src/Decred/Signer.cpp | 12063 | `8819f8e0af09b8f4937cf9450e6b089fc2a7636d5b2ffd451cd8e8ec5257bcab` | 0 |
| src/Decred/Signer.h | 3671 | `8700814e6053d5ea07067b7f6e1121ad6b7a33f54ec93ddf829684a03ec212a0` | 0 |
| src/Decred/Transaction.cpp | 8215 | `7f25379559034363ad078996e4e293d6a0798f1f1572c1920c9f367280bb3db0` | 0 |
| src/Decred/Transaction.h | 2318 | `e357fc982d7d6ba02369e34d6a794611af6bc90c44863a867ee2d19360d749bd` | 0 |
| src/Decred/TransactionBuilder.h | 2073 | `301d7c43b5dfe55738b43b50858bf30b7b6b1bf4fc180a46def5f00a753f576f` | 0 |
| src/Decred/TransactionInput.cpp | 492 | `bca8d52a632209df21c4e198221c520ff9ff5b2bdc93e0910d2ecea7fcd6ed89` | 0 |
| src/Decred/TransactionInput.h | 1413 | `5ac419742f31d3128fa38ee18203c322367868aa24305aeec255b879db08f8dd` | 0 |
| src/Decred/TransactionOutput.cpp | 328 | `c7dd3c4e11f2d276704f140b2144800523e3847045083fcc918455202879a4bd` | 0 |
| src/Decred/TransactionOutput.h | 900 | `bd565e4251b5517457b637ead9ab4147a8e70d668425031810ceb9bfa6db9de9` | 0 |
| src/Defer.h | 463 | `643773b047332f6bd9545bec71d430fd2a293ae261906dacd77e42895ed0485a` | 0 |
| src/DerivationPath.cpp | 1494 | `87858b263cbf7ce13b60a0b7416dcdf31656b5719053ae7fbcf5f75c42f9591d` | 0 |
| src/DerivationPath.h | 4126 | `dae898b88ae04daa879aa64df7e259e8d20993d8f641919492edbe61dd0c62e9` | 0 |
| src/EOS/Action.cpp | 1696 | `8315d0e7012c5fa382191d46fc207dce01a200da1dbc6cacb3478efe61d170c6` | 0 |
| src/EOS/Action.h | 1078 | `b0d866c047763edb68b73fad7a7181b629f27193008786ae4f3da2ea23c87f6d` | 0 |
| src/EOS/Address.cpp | 4304 | `8dd91a4967e9e1a7949c6aaace106a6e59bd7789f310599c8064d618fbbabeac` | 0 |
| src/EOS/Address.h | 1610 | `347daaa917deb07242dca860a4574f48f41d76d1b4d82b9f4ecd1296df5b965c` | 0 |
| src/EOS/Asset.cpp | 3810 | `1740de12d37c19c501b968ee0a96732967cb565d3d782749245825bc857d25b7` | 0 |
| src/EOS/Asset.h | 1128 | `5b47821c2472fa7b58c68c3d5e6d7036df5b78376f8c6d2ea254e64e6653c88d` | 0 |
| src/EOS/Entry.cpp | 2462 | `32126d58371d57c27bc9fdc8293aaf5b28092a19b36e956c23e402808a9e4e9e` | 0 |
| src/EOS/Entry.h | 946 | `9d5ea30874a966cadc52dbdc1f24d84ee450c26f93e4d40e077d769b6a641424` | 0 |
| src/EOS/KeyType.h | 226 | `aaece3634e1c477e409aa9b1d062d61ef576ce89f31d7b6598de4cb3a354bdcc` | 0 |
| src/EOS/Name.cpp | 1235 | `65a4f7fd41de399e5ec07955ecdd89b78945925d7cfece71068e89525c31afbc` | 0 |
| src/EOS/Name.h | 398 | `3aa0ca336d83b80a75de2734b36ba6711395990615235b7e78e031fa20a43e94` | 0 |
| src/EOS/PackedTransaction.cpp | 1275 | `549e2a1c547dd74214152dfbedb284b0c8112fbdfdc4bfd4f66341b383db5b3e` | 0 |
| src/EOS/PackedTransaction.h | 640 | `cefadc0c8f4f780378f3c3ce8c7c7e388b73ece2e50a3c8b77b36188e36f31fd` | 0 |
| src/EOS/Prefixes.h | 1532 | `00cdb7cf2743b4313604bef6785a2d89a31a269dbfbcec1b8ceda13e1f3a04fb` | 0 |
| src/EOS/Serialization.h | 1993 | `58448d7df729b7fa488f5c6123565f8583386b33419cbe8e1499ac85e848e039` | 0 |
| src/EOS/Signer.cpp | 4388 | `737c34ae7a54857a346389925edb8b6d5822d71e7347026da14aea38fb5b3312` | 0 |
| src/EOS/Signer.h | 1263 | `a113a5fdd3adf42bf3a19e858de6bcbbec89bbbbb48e8345f0b37242f1b8712e` | 0 |
| src/EOS/Transaction.cpp | 4035 | `005aaccc821f6b5af991dead8b0f90fcf6d4b63a615816f097793245cb323d84` | 0 |
| src/EOS/Transaction.h | 1657 | `00e682c2401fba1990ffc8431d6791e199919ba3a7ee3ca5f5978dfde89cd75a` | 0 |
| src/Encrypt.cpp | 4108 | `ce7ad26f4190330364f2e8070daa8ba1e5a46a45028442f7a980da3483cfadfb` | 0 |
| src/Encrypt.h | 1917 | `178c3151f1543ea91aa97773960e1ae10d2ecd3b482c4e238f45d900bf455630` | 0 |
| src/Ethereum/ABI/Function.cpp | 6569 | `3a3344a3548279079bc6244de4a22254ecc2d99e4a215a3edbe01488dec87e6a` | 0 |
| src/Ethereum/ABI/Function.h | 3561 | `93c9331fe4932409b94577b9bdf815ae1715957041b94220ba8e6f2f1388fab9` | 0 |
| src/Ethereum/ABI/ProtoParam.h | 3000 | `0d0f9503526dacb6205ae26862119aa538e4ae5097ba02c9ea3c7f6f22b4adcf` | 0 |
| src/Ethereum/ABI/ValueDecoder.cpp | 1197 | `b822433056dfcaf03af94ee2980c2c9e6cf1a16197b5d7f870b99f37a9b7ee3f` | 0 |
| src/Ethereum/ABI/ValueDecoder.h | 466 | `cd8f3f9756ab16b962cab444fed827e6788402c8f177d25939023ed87d42b2af` | 0 |
| src/Ethereum/ABI/ValueEncoder.cpp | 2773 | `ce2a389c06ebdee03cf6561836c94b99948196aa510459b028bfcebcbb9a0b40` | 0 |
| src/Ethereum/ABI/ValueEncoder.h | 1818 | `d1d26ee8fda976ed986ea78e8d6a5380f7bfde0440c18568f7ad86fa946166d8` | 0 |
| src/Ethereum/Address.cpp | 1296 | `90ed5b61fae0ce1b71e20c4f9b12e9890d92e594f87eb275faf361cfb6c1756e` | 0 |
| src/Ethereum/Address.h | 1263 | `417a84c4fe7a1d852fbce98d9687356b43cd6a5d953fb28bccdca23d889f15a2` | 0 |
| src/Ethereum/AddressChecksum.cpp | 871 | `081809303b708ed007bebd1be068ec2b86db84305ad7321ac79c8b1dfd6d4d4e` | 0 |
| src/Ethereum/AddressChecksum.h | 235 | `2914877ef8000fb7ca84fc58c7865a1d230000afa5cd5029e5f39975aaded2fb` | 0 |
| src/Ethereum/ContractCall.cpp | 1101 | `bec0096af64f1d78deb851d2905d490076bd1b22afdef7ff6835907648663e10` | 0 |
| src/Ethereum/ContractCall.h | 326 | `fd8446fe2b68bb34932a15e45f15d00deb65ed37a73e0bf67782b873b99ed309` | 0 |
| src/Ethereum/Entry.cpp | 525 | `f496e516b8c4bdb4915fa27d933b36c69aa20ef59531dc415e5d8b2403f65698` | 0 |
| src/Ethereum/Entry.h | 578 | `3e12a6b5659b78e5a1ef7f703f3d446f3835f2beb2a53fd66ed8e9e57caf3bec` | 0 |
| src/Ethereum/MessageSigner.cpp | 4138 | `4fd5d771ae97f393c883294cb9a8af9d1ed84d397e1d65e2bb4a39d55a53632f` | 0 |
| src/Ethereum/MessageSigner.h | 2081 | `921a001e4acc575f23f02ed88b89b586f28d9392e352375a37b6fc2befd6a4ec` | 0 |
| src/Ethereum/RLP.cpp | 1170 | `bba81d916206f33fab2637ce2087d615adc2b41fbd3251df5ebd1a55033d9efd` | 0 |
| src/Ethereum/RLP.h | 577 | `0597dae15e8023dc757c47f00cafd41ec975cc29cd2e7edfbd8c645bb86bcd70` | 0 |
| src/Everscale/Address.cpp | 846 | `5ef3c685267d985ea539515d618c6f1f41e8ecdc1c93270eb85e509519d71718` | 0 |
| src/Everscale/Address.h | 1389 | `515e8e55f1d90386151f88d96ff6f161aa0f8da6112ddf426fd0a4a4e58b9665` | 0 |
| src/Everscale/CommonTON/BitReader.cpp | 1134 | `382bbeb1642786346478718c01a40e9c6d4f1fa264cd1f34f0a32b67be588e14` | 0 |
| src/Everscale/CommonTON/BitReader.h | 851 | `4520ab5df8ff7d5cb1dae86b88cd249514f18c6ad9aa572bc5a382fe6ece8175` | 0 |
| src/Everscale/CommonTON/Cell.cpp | 12851 | `21d162d86b54a3ace56703d8c3a8eddc052b695df0c2051345795506cf8c4234` | 0 |
| src/Everscale/CommonTON/Cell.h | 1819 | `1bb1c03bb0c48b15d8d315846decc139ada12baedf9383ce102c7a0a9f168d34` | 0 |
| src/Everscale/CommonTON/CellBuilder.cpp | 7595 | `9827f4f73da468359092c68f839ebe5cc6034189ef2f3471b539667e5cfaceb8` | 0 |
| src/Everscale/CommonTON/CellBuilder.h | 1501 | `8babbf69f0408f8fb199d9a259e480701849fdb70a93735f25116522c82c0244` | 0 |
| src/Everscale/CommonTON/CellSlice.cpp | 1363 | `5d815faa4d447cb58d06d0c5a42418df5c86d6650357121413f312f1b4d78315` | 0 |
| src/Everscale/CommonTON/CellSlice.h | 510 | `488834a25e5cff632f9bd413db715a3adc9f7b177458a10bf1d9e5c76c1f1d2e` | 0 |
| src/Everscale/CommonTON/Messages.cpp | 1713 | `b46ae9b3891c0d8851c4db5c012461de25c09387a8236a8a567c7a1fd0a9c521` | 0 |
| src/Everscale/CommonTON/Messages.h | 1618 | `cdebc47e3c396f350886bedfa87e7ad5203a1fe32c1bda924b9a8b84328d5706` | 0 |
| src/Everscale/CommonTON/RawAddress.cpp | 2832 | `414cea84fe55fa97fac66f5ec4cc0907385fae8a3f34aefb60248b9cb6667850` | 0 |
| src/Everscale/CommonTON/RawAddress.h | 949 | `fb29c514376d7105ff59c7dc7de74e7ca85333109ed1a348d396ada599aa31a7` | 0 |
| src/Everscale/CommonTON/WorkchainType.h | 214 | `9578feea18f059649020e09343ea45dba2ca3dfd5815aa6991aefe0e0776f04c` | 0 |
| src/Everscale/Entry.cpp | 1151 | `4468a8fe663703fd64ed9a4f5110053a845fa13b90764c50397934a0c807573d` | 0 |
| src/Everscale/Entry.h | 818 | `983e45a3b2a578502aceff082aa830c3ec5164425efbc710bec11374fd9be4e3` | 0 |
| src/Everscale/Messages.cpp | 2389 | `e7833eaec9f84950920a0da85dc9676c7042436d6c311dd11eaa82aeaa8c9803` | 0 |
| src/Everscale/Messages.h | 659 | `2502f4c51a3cd0cfe6ac01378c340fecaf0c20839e7b5b0df175dc869d9be471` | 0 |
| src/Everscale/Signer.cpp | 1759 | `f79d931be6df2b144d03ffab7ca035ba0c162ff52bdafcd6934b674725677328` | 0 |
| src/Everscale/Signer.h | 495 | `8987bbc5c4bbe2d8945f0f570421bc26794d094d9f40a729a4571dfdbf598c45` | 0 |
| src/Everscale/Wallet.cpp | 1931 | `f6d3a907fe1ded629a7b3969307f02007c9f0331bb78f136139ad49819443822` | 0 |
| src/Everscale/Wallet.h | 1937 | `c761ad7ad9294fd5d9eab360f64456cde5a1d3030805193cbf35fdbea6b27084` | 0 |
| src/Everscale/WorkchainType.h | 237 | `041f876cc759af4705ad10c708c13c9c23c861db33b95de80b10bfcb6c171eeb` | 0 |
| src/FIO/Action.cpp | 2592 | `e93f95d21179320e73c23e0946e79fceef6446c1f3a4962d8fa8442ec28fdd8d` | 0 |
| src/FIO/Action.h | 5935 | `346108e3149036bb9ceed2ec31b8bb2cb41b89955ca48abc500fc04d89a18b6c` | 0 |
| src/FIO/Actor.cpp | 1567 | `4b8d8ed5f20f4cd1278214bd385ec4d90fcc09912aa2dc4ab1878dde95f706f7` | 0 |
| src/FIO/Actor.h | 708 | `26d845374dbb00429246e6084f82f38a7adc717a7713b2b0df718ee2a201ad62` | 0 |
| src/FIO/Address.cpp | 2816 | `0e39466f5e5b644395717f5ee826b6ffafaa636720807dfe34a80727721093d9` | 0 |
| src/FIO/Address.h | 1466 | `e62d9bdaba302627b9014e12885ea433c3f0e5d8387d7e8fae24b3148ab96712` | 0 |
| src/FIO/Encryption.cpp | 5161 | `67a152af731dbbb7cb657552896e066366fd75799677ab8f1fa2b87498562dfb` | 0 |
| src/FIO/Encryption.h | 2210 | `e69043cd9e90a455a7e9b06ef331b4812d32a7b92350c7b1caebce5b6e87409e` | 0 |
| src/FIO/Entry.cpp | 2226 | `549c9790017f8b4c8c1d0a7f0b2bbcb5b9c52d49bef2dbb60278b5f6b89e072c` | 0 |
| src/FIO/Entry.h | 946 | `0ef6050063ccb88af8a257e19d712b75cc23d1a44919bb0fe85515598a2d9af1` | 0 |
| src/FIO/NewFundsRequest.cpp | 1774 | `4303f8945db10b14cc2d16f7c5ba1fb6497c8b935ffe57d01cc99eff2ad5c127` | 0 |
| src/FIO/NewFundsRequest.h | 1011 | `199adfe6cf254fc542fab7a599c89c4e07effe137b8df6eeb6459156a2f479f7` | 0 |
| src/FIO/Signer.cpp | 2162 | `81820fa4fa16b59fa7a08d479397a9e0c9f069b8e3eb7d08743e960c77ba44df` | 0 |
| src/FIO/Signer.h | 1316 | `fa869b2c71d3ebfca005770ca8d60e40418c6b407d9e664b4003c6d2ccc137de` | 0 |
| src/FIO/Transaction.cpp | 791 | `f25143a69c09a84842f4c1e207e1a6542734e393b47a364a83b1a34e7c252400` | 0 |
| src/FIO/Transaction.h | 622 | `8ad2ecd5dff50fffca527095f733d630e651fab938de9bfef6f8825c352ec76c` | 0 |
| src/FIO/TransactionBuilder.cpp | 20915 | `21a5ff3bf0b854026b132afac1fd63809477d34bbc8c285332ec7ed0785e1fc3` | 0 |
| src/FIO/TransactionBuilder.h | 13995 | `86d2d7aa73e00ae5bb0e95e14830228e8857e0cff451cc0e562d944ca1577f80` | 0 |
| src/Filecoin/Address.cpp | 9473 | `ee345a00e8c56a46a6900a79a440a988726c642a42fb8d7c54a8a939fdfe063c` | 0 |
| src/Filecoin/Address.h | 4325 | `dab9d9d6d9aedf8ed6cc0fd05108fb11a1083461a01d610e9f6541b2129f8704` | 0 |
| src/Filecoin/AddressConverter.cpp | 2301 | `6d2c545eb939cb79c34b57019f28e8ce62d355da8f64b312752106d43b101b8f` | 0 |
| src/Filecoin/AddressConverter.h | 891 | `c4cb66f7f332c8661f0ff73c8b8274c8b48bea3357ecbdce57ed09d385f21f95` | 0 |
| src/Filecoin/Entry.cpp | 2711 | `69a93e44ec846a3589c79a03465b6f974bbea39ea614373ca17fbbca7ca4217b` | 0 |
| src/Filecoin/Entry.h | 1110 | `11747817d2a8efa792522c7df84844e9a80e6bfa45f6fc452bbb862a11593019` | 0 |
| src/Filecoin/Signer.cpp | 7414 | `def0ec03967d68cdf858d6c3e31d616f993c1b1599858312d0d24c8300837a20` | 0 |
| src/Filecoin/Signer.h | 1468 | `a20d5635e8ffe425a3ea2126b22890d1857b8c91616ca82308fbff8f244e3411` | 0 |
| src/Filecoin/Transaction.cpp | 2780 | `692863979813a18b22e03938281f5211ef9eba823a6dc225b3c6d7ca18109e17` | 0 |
| src/Filecoin/Transaction.h | 1849 | `9b4f50f8c9da99e82a39ea14129f4632747cb30d1625dfc2ace35614c5e3a3e1` | 0 |
| src/FullSS58Address.h | 4725 | `a6a7afe90f31923d2a5faab5ef750621d834d373104d7cbdf54cc309b9098723` | 0 |
| src/Greenfield/Entry.h | 413 | `78af9d87c7ffb6850fa521d53b93098fdc3819c7922f82cb70963b66ba32708d` | 0 |
| src/Groestlcoin/Address.cpp | 1924 | `69544714b5096aa3b1f0aa76c5eac84ce1ec31f711edb8ef81d07d458584e642` | 0 |
| src/Groestlcoin/Address.h | 1595 | `8574229fb08b0c4cd9223c038e7dac52a0b3aff36d6dc5efe8e55acc124ec926` | 0 |
| src/Groestlcoin/Entry.cpp | 3525 | `a931562cb3312307efdf41aa91c2eb38470af6074c7afc5311f5c108a12c911d` | 0 |
| src/Groestlcoin/Entry.h | 1096 | `824fb007f2919b81c0340d7987de457f3f77e42a9ae431bfd1a2272b63dca2a5` | 0 |
| src/Groestlcoin/Signer.cpp | 2419 | `90262fe8c63915b8a65725fbedb98c8eee43e514d8c06646f2c2359806281a91` | 0 |
| src/Groestlcoin/Signer.h | 943 | `555a23d7c833506f4caa9e7da49cb0bf004b5e6da13e22a274c08c716b83ec0a` | 0 |
| src/Groestlcoin/Transaction.h | 443 | `f29e1bc59a54c4273295f4edb39850a29a3ecc268f1d961dbdbd38c8462d37d5` | 0 |
| src/HDWallet.cpp | 16132 | `a1a30c0bfc850c5baaf3b83fbc4beacc7d767842b5ce23c7e91b1ec98eb86e29` | 0 |
| src/HDWallet.h | 6276 | `5c08f4b860f54edc5c4b00b7162d5514bbbc8f0058592e6300e2d8d76c225d33` | 0 |
| src/Harmony/Address.cpp | 246 | `610553d2c00dc50f023a84b113c109dc57fd754b99306853c9746cbce6f44c05` | 0 |
| src/Harmony/Address.h | 1282 | `23288e75687f158122b7deb893e8f4a5a49861fbb6b475e60777ab528450f074` | 0 |
| src/Harmony/Entry.cpp | 2533 | `d8ad3c5f0315831529fbaaf24b94be547312cec2d14f1111708d73787356dfb2` | 0 |
| src/Harmony/Entry.h | 1178 | `5dc8b1f7873b05928f4785a8626973ce9d59936ef45c2e0967b7779f1e2edbc3` | 0 |
| src/Harmony/Signer.cpp | 27527 | `d2aa623c88ec200c6e9377c744cf1807a3fa605f5bc674413f4a0bcb4243b0a9` | 0 |
| src/Harmony/Signer.h | 4925 | `2e4690ed765dcea59b103c54c768f8a63c723413d4756242b74a4f045e5f745a` | 0 |
| src/Harmony/Staking.cpp | 77 | `ba85c55afc25ade8f5e54d06d6a020a2419ff1d5b778e2d4ea76ffd7c2d671d0` | 0 |
| src/Harmony/Staking.h | 5497 | `c1cb4cf5afdc39e15fd9238406f778c4973649b23e4501b8ae931382e9f338a9` | 0 |
| src/Harmony/Transaction.h | 1115 | `ca3cd5a698b52b02074a6ebb2af677e8ca2947e3f77021935502358bd2748688` | 0 |
| src/Hash.cpp | 3995 | `563854369bf41d42cbbb440f6ebb502d0a11511a9feaa5f90ee41d8b9bedcb5f` | 0 |
| src/Hash.h | 6520 | `994ce834f53fb95c86687fa90e85f3f151282a55a59296da4a9e9affdd4db465` | 0 |
| src/Hedera/Address.cpp | 4472 | `e7c3f053d661f0675bd1cf5c71487c29a8aa89592607c38b6223b7b744d718f6` | 0 |
| src/Hedera/Address.h | 1368 | `345f079486a1cc82f47fe5777cf13c4e3208eb62729d2700ddf1e224cee3945c` | 0 |
| src/Hedera/DER.cpp | 634 | `778ea6b086e0606b30f5c5456cb6b415c73485c999457699d5776602f8136f88` | 0 |
| src/Hedera/DER.h | 717 | `771381a095ead264d08413f537f9396df7176167ea9847199fb9861908c0d001` | 0 |
| src/Hedera/Entry.cpp | 814 | `bed2ab64c208462a5c2289f09a8c4901780e5d26c45e96aeaf00f81e920bc922` | 0 |
| src/Hedera/Entry.h | 745 | `dfdf95459e21eb26484a87b4920367c843999894b4ebacec2dd79df92cb48418` | 0 |
| src/Hedera/Protobuf/basic_types.proto | 40897 | `b913a2a6f1431d3eb2180caf947e40e2e7a6f3ea7ceea2f5025657032b7d961a` | 0 |
| src/Hedera/Protobuf/crypto_transfer.proto | 2252 | `7a88bb4e98e68eb04a58b96e0016df3a241b2d5e82f95f5221016debd3037b15` | 0 |
| src/Hedera/Protobuf/duration.proto | 1013 | `6bd1fd9f0eea239a4360b01441fc9e4faa9a494767d5f406ff61745753e65f1e` | 0 |
| src/Hedera/Protobuf/timestamp.proto | 1519 | `74c7922098e04098bbcd1ae6ba332b8df0f9a253306bd9a50bc98f919cc6108d` | 0 |
| src/Hedera/Protobuf/transaction_body.proto | 2170 | `a3543edb4a8da88977ebf6cd51031008f1330fc70d75fc73f47e6188834ea201` | 0 |
| src/Hedera/Protobuf/transaction_contents.proto | 1177 | `ffe72515039fde018c33eee3896c67743ce695c221a8c46091619cc0353dddbc` | 0 |
| src/Hedera/Signer.cpp | 4992 | `4bab649f4a0a8ef12de17f55831be1fbaeb5561095498bd8ffce993bd6dd3917` | 0 |
| src/Hedera/Signer.h | 483 | `aee0480244869946985c68e85f316590dc6c47a2a5e974d1f06b3fe30d0c0629` | 0 |
| src/HexCoding.h | 4726 | `7157e91f5c5e3e769ecf3f0abef34d88d2f69b3a339cc1ef87101e33384e678c` | 0 |
| src/IOST/Account.cpp | 1880 | `37cbb87f9c5450ab9f8c13c1e13f486c1cf971e34089c9437ed4fdf55689e4df` | 0 |
| src/IOST/Account.h | 1024 | `593ac28e1a9876126e19b9b63de4ccf770a05f4cc56f1818d707206bb94034ab` | 0 |
| src/IOST/Entry.cpp | 2179 | `c0ed0916a092e729c90a35c53b9614381b182a3e7ec82a8e5946606cf280fd97` | 0 |
| src/IOST/Entry.h | 1136 | `b8cda50764b81f31ecfe89d7947b444bf9c6a7109dfb41a05a1b8cf52c413a38` | 0 |
| src/IOST/Signer.cpp | 5566 | `900090e09497343bf999abea85152b664f959a48a26de03b6052ef8ccdf6bb1e` | 0 |
| src/IOST/Signer.h | 650 | `959014d6698cd8055aadab493667608de3f938e52fedaf16be6cefd683e8b5a8` | 0 |
| src/Icon/Address.cpp | 1748 | `1ed32878655094a74bd0a104e23049a977ddba7191acc74fdb3c814af5625a29` | 0 |
| src/Icon/Address.h | 1261 | `60682514228e4f5f0d258b373f513e5d631c5f4693167b69a20c7a6224873476` | 0 |
| src/Icon/AddressType.h | 241 | `135f6988e980f3894269a1cb54f35f9583a1fdc541d9d25f2be63893825d5483` | 0 |
| src/Icon/Entry.cpp | 2511 | `1ec109b1f7140bdd37307bfa52768e4011f7175639778fcfab17889ef3f9690f` | 0 |
| src/Icon/Entry.h | 953 | `ecb54dcee7a0b5e65246c5608fc44d4ce4e4105d11585ccdc1814a0e7446edb9` | 0 |
| src/Icon/Signer.cpp | 2652 | `f6909e2b527d2878833c3bd7766d1da07c643dec7a4020146f48310c2c86930c` | 0 |
| src/Icon/Signer.h | 869 | `c386b4547f326d3c492911a11e8140ccf937d7cc2144e613028806097a12cbf3` | 0 |
| src/ImmutableX/Constants.h | 877 | `8ac069a7e93de87bb51b05b100edc07bc82ee991d17418002b9b6e27a2170e1b` | 0 |
| src/ImmutableX/StarkKey.cpp | 1636 | `0c88d54fcbfa45d054c1070964bd74d5fb31a9a987e00af3fcdc9cf3d5f8cad6` | 0 |
| src/ImmutableX/StarkKey.h | 612 | `7eee4641b971acdc332541f0c0cb731c60145733e552f54fe613904da09e659a` | 0 |
| src/InternetComputer/Entry.h | 430 | `813663757e66568d21a8f80b7e84c6cb4db8d948b4424aa4b6d3afb08f8764d3` | 0 |
| src/IoTeX/Address.cpp | 206 | `66805849a1ea1731f526fe275adad6ce31e0fc5ddb3e78f4a9a42474f2de9ed0` | 0 |
| src/IoTeX/Address.h | 1272 | `2f3bddc2c20bd2633774233bd1cd8bc167b6ab1967cc3a1d7145f567f276f91d` | 0 |
| src/IoTeX/Entry.cpp | 2001 | `713f45cac096d8bc75b53ae49152006a12b62d3886ecb110d0fecefd1f18d05d` | 0 |
| src/IoTeX/Entry.h | 952 | `6110c992e1b93d96b85466b7c7a1c8a73afe62b2e53ed5fafe8af495dc8ba27f` | 0 |
| src/IoTeX/Signer.cpp | 2138 | `b499b687853535e8e2fff034417340207ed65f47d98ba48ea735612769bac16c` | 0 |
| src/IoTeX/Signer.h | 1295 | `fd6ca724e1fa4d5ff0fa3243653e51f2c90ea33d76501bb9411acd72d23458d7` | 0 |
| src/IoTeX/Staking.cpp | 4178 | `17f8b5c35f0c96f023aff3fa85e3129e51c253cd790afce781a58f7b004c3551` | 0 |
| src/IoTeX/Staking.h | 1541 | `19d7333cb854cae52f12acd604caaf76fe54c532d0cb605f3e35f302194dc73a` | 0 |
| src/KeyPair.h | 240 | `f745308b3d6378af978dfe23b32017023e6684df80a19b115074532d2bdb7585` | 0 |
| src/Keystore/AESParameters.cpp | 3178 | `8b62c4cffb3c340ff0c8cb2062a6d00c70f54cdee699255bb12f4d6df04e1e5f` | 0 |
| src/Keystore/AESParameters.h | 1609 | `16f8471ac323ee1ec1c1e0b3e4a7d87388d241f952917235c30d98cc7c8993d8` | 0 |
| src/Keystore/Account.cpp | 2754 | `80a5c5fde3eea5488ac666166f7081988725cbbe040a4ed1b07560ef373c48af` | 0 |
| src/Keystore/Account.h | 1530 | `217e681133068cb23ef29f4a3cd0313df86a7a27deb3cd81af353a4b7c78abfe` | 0 |
| src/Keystore/EncryptionParameters.cpp | 12180 | `7ceefc3db4202b71824bf4f0fcf5b7802689287ef6c9b1e157e8842e475f957e` | 0 |
| src/Keystore/EncryptionParameters.h | 3850 | `d9a12ec11ba7a86ff7a02da9f977c7f0939deeb4ed21e73a926e7c5f02f81d6b` | 0 |
| src/Keystore/JsonParsing.h | 1929 | `bf9343cda51ab1d29ec782ae5ad225c43360e9ddc5c973060567d4f46845a715` | 0 |
| src/Keystore/PBKDF2Parameters.cpp | 1693 | `6322d69e4977357004368e2fcfcc3c55bb3b9d991a7ff458a2bec0193ff6b734` | 0 |
| src/Keystore/PBKDF2Parameters.h | 1291 | `16e69590985189820d08e6eb8ecfca0074f3e1b87899fe3dfc0f05af31f238ee` | 0 |
| src/Keystore/ScryptParameters.cpp | 6155 | `ad1371b1ce6a274957bb1e1f14ad77a6a2ba8ae398a15acdeac8ae914d64522d` | 0 |
| src/Keystore/ScryptParameters.h | 4536 | `8ce8e061b9baa7d15cb32b6ee28020e572e4e0ef51fe337d7496b86c50eba7b3` | 0 |
| src/Keystore/StoredKey.cpp | 20510 | `f78a159f8ce0401fc06b28c243e88d5a53f58c3c2a676fce67013c100fcf9644` | 1 |
| src/Keystore/StoredKey.h | 10668 | `9f3bf57ce96353638c8a72da354c5e8c38a7630d94c195c90d5a66e3bd43691e` | 0 |
| src/Komodo/Entry.h | 364 | `a85ed08ab123348e1ed1d6e29e89644dc373d82634f95c3a652d68d66a5c2803` | 0 |
| src/Kusama/Entry.h | 414 | `071fe470358c2bbd674dd7f531fd34135ff809bdc95c44f87feeae069c768873` | 0 |
| src/LiquidStaking/LiquidStaking.cpp | 15154 | `b71a4246cf943ffd09611f1595d23640e4f62a69818871f33ce32541d40e2b5b` | 0 |
| src/LiquidStaking/LiquidStaking.h | 3438 | `6a00293dfa43b9fd36a813123cbe5b72e0518603c4c783bc770e9e9dc4a5c016` | 0 |
| src/LiquidStaking/TWLiquidStaking.cpp | 967 | `528f609a2f593cc437074a9f6183673ed10bce0bf0e0e85421e5503dbf989581` | 0 |
| src/Mnemonic.cpp | 2166 | `4599c6d3a7208ea0ec267d728931685ff48655ddf8037d53e357bbbc3425b56c` | 0 |
| src/Mnemonic.h | 1677 | `beff711494b0c4711c7620f524fbbc4c0e7d13f3cafad9143b7050a6d6a8c8d8` | 0 |
| src/Move/Address.h | 3886 | `11430818733eb3443ba1f6ed0bf10d5736ae4b8f0bbfa89b9a5a235a8b794030` | 0 |
| src/MultiversX/Address.cpp | 342 | `a1f7b3b2257aebd0fa6e4d9c368dbbb4870238da539e46dc47542e06834a9298` | 0 |
| src/MultiversX/Address.h | 969 | `343a6d0b3274cf795e1af3a806615d0c335f74ae3df9eee37be26bcf2f59bf84` | 0 |
| src/MultiversX/Codec.cpp | 1125 | `6baae6f7243a4779da6c8219586bc23c2aa15cf108f942a8543279949d02e5a2` | 0 |
| src/MultiversX/Codec.h | 899 | `1939af66c94bbf451cb3935dc11fe840bc057fb8dd5eb562164f658fb4419d98` | 0 |
| src/MultiversX/Entry.cpp | 2384 | `d2264d09c0899ec439e83ac5fcb831f98432d4a425e18fb868a278b518a99b0b` | 0 |
| src/MultiversX/Entry.h | 1187 | `a3cad3bc549e4f996d7f624c1d45e64f70c857d435778e00e161c8ed2a3f629c` | 0 |
| src/MultiversX/Serialization.cpp | 2577 | `bd33ead4d437d2e548968df34ef40ab461d59d628ed379dbe9b1cc021d533798` | 0 |
| src/MultiversX/Serialization.h | 435 | `c71ebb2f51cc0440b3e16fa1a306fc12f50f1172983bdee1be1a38b4145ec2c0` | 0 |
| src/MultiversX/Signer.cpp | 1697 | `80e280af67de3277e88a45b6d282f2b4c5546f3eaac42b7e4a885d954aa5dbf1` | 0 |
| src/MultiversX/Signer.h | 819 | `0b535a70ef44ca6c93e294248efce7ebe28e6135594ff2fe9345498fe04df240` | 0 |
| src/MultiversX/Transaction.cpp | 559 | `d37ec8efcc962d75fc49b9401123206d21c6c6cb50fa1070e930e8b91ed1cace` | 0 |
| src/MultiversX/Transaction.h | 1018 | `4155f362c271592bb5ed5c725f5eb2a3ae9ee543060c7531d7f8636999c79aa8` | 0 |
| src/MultiversX/TransactionFactory.cpp | 8006 | `a27d5920fefd99db7b4edb3bb76ee680e377adfeab6d423bfb74031e776f503d` | 0 |
| src/MultiversX/TransactionFactory.h | 2612 | `2ab2dddb7409fabc023cfc20ab10103cc9d5ffec709a9d1e27beecd47bf85050` | 0 |
| src/MultiversX/TransactionFactoryConfig.cpp | 3597 | `41947e0bf3a54aa630024927e26e192a6c3650f0007dee381b336306e9cb8114` | 0 |
| src/MultiversX/TransactionFactoryConfig.h | 3037 | `77a06270273ddb39dd87afac6b07a04296570de74ff824e995f96067a3958990` | 0 |
| src/NEAR/Account.cpp | 534 | `b75a20331ecdf9f3d307de720b8a72e6269d48607dee05ca16caabcdee65efb2` | 0 |
| src/NEAR/Account.h | 305 | `5dce5f8b0ba951973396db4c9186d96a17a022e037e5ae893dbf0a1469ca3335` | 0 |
| src/NEAR/Address.cpp | 1925 | `915f63043de6f85173650f0f636a5ff973ab5eb7911bcc7eab90d51c936bff60` | 0 |
| src/NEAR/Address.h | 1258 | `24cdcbba8e2248f0bbd9c759dfe8c95d87f3502f61f001090b50f2bcef45e890` | 0 |
| src/NEAR/Entry.cpp | 2728 | `8d16932ec65eac85e92770d725e49253d080d0eca602f564afdab809aa861b60` | 0 |
| src/NEAR/Entry.h | 1143 | `6c460fd1a68d97881abdd9edf2caafbdab27ef50090087eaa9e2105b71be34ff` | 0 |
| src/NEAR/Serialization.cpp | 8002 | `a83a3e518121706bc532f4d76398dd513774652ccd4a7bdc6d363e2a625d7c42` | 0 |
| src/NEAR/Serialization.h | 493 | `869edde4cdbe95fd9072d4338c781cb28f58c968bf0f3a874c12be9f7d9450db` | 0 |
| src/NEAR/Signer.cpp | 2350 | `f07b3bc8e13b5e166343fdd85d3702c19e8283eaf4e7333610738fcabe682124` | 0 |
| src/NEAR/Signer.h | 766 | `04f675a30ae473ecde05631337d418e848a4ae7b06c6259a6cf669ebd24b58a2` | 0 |
| src/NEO/Address.cpp | 1505 | `c0adfe6eb3771d859ed84227867c5672fd3c90d30aee334a2319ce97e3b325c2` | 0 |
| src/NEO/Address.h | 1313 | `5fc8da782e5ba6f3617c6146929c2450a5a22a38d274e11c31da60bbc41d7b52` | 0 |
| src/NEO/BinaryCoding.h | 1325 | `dd7684d5d2f556f7f67b32225b066b3af61b2f6f985d3027e8c5ad8eda52a3dc` | 0 |
| src/NEO/CoinReference.h | 1340 | `1635168acc3a1525c814106a03ce813ad7db61d2d09b95479892d4f201a7c931` | 0 |
| src/NEO/Constants.h | 294 | `ed92f6b835caf3caf6dbf480b0431fc6ba47f688460e5fb9e62ecac9f18f3f87` | 0 |
| src/NEO/Entry.cpp | 2539 | `95b086f26e4c579f4cb890b799c9536f431dc65dfa43171af1a60db32e5af472` | 0 |
| src/NEO/Entry.h | 1138 | `b92725183f5f4283770a8d07e16175da1c6ed2c30c275750c2aa0adbed991370` | 0 |
| src/NEO/ISerializable.h | 429 | `50c0bd9d94db2cc84bde4c6a0152f1c5f0de2dfea5e7dcf15447f8cf356b5501` | 0 |
| src/NEO/InvocationTransaction.h | 1214 | `7f9696d00c58b9fd1bfaef11c6e5cb9eba5c47e4fd0d10f00f116fc1c88b1b9f` | 0 |
| src/NEO/MinerTransaction.h | 728 | `c26c774b08913c1d3d90a455b4a94def20702512a80008d90aac382f4228a60f` | 0 |
| src/NEO/OpCode.h | 777 | `d0bd6728dd418c3a191d21b98f60529749aad2d2beeeb6c6475e3f459cb5fe48` | 0 |
| src/NEO/ReadData.cpp | 1808 | `56862a95ca4ee497e01792f3efc6ea9a39f6e924fef1b5c2cbbeb5d6333860be` | 0 |
| src/NEO/ReadData.h | 931 | `c90001176b9aa5326c0f98db8459cca801adcfc183ed4f302824542faa08eb2a` | 0 |
| src/NEO/Script.cpp | 1671 | `a1f7f3a8b0024e4d368569c64125248a130ed71415cf04c5dc4c9f66b9b07a23` | 0 |
| src/NEO/Script.h | 551 | `c51bf4032f1842eade76e1044ffc3ee41243b97c311230c306d6f0d14c1c1f42` | 0 |
| src/NEO/Serializable.h | 1674 | `07de8d03e14743f5fa01f1b6713300c6d71951cb4f3d3b3356521e34347b920e` | 0 |
| src/NEO/Signer.cpp | 12980 | `fa1719342d060c05daa9ef8c75f817c9317bc4281041811c3e8af260c2838d25` | 0 |
| src/NEO/Signer.h | 1238 | `001227b5cf431ac0a2304b79597509e11ba291cf47378c93da05a3400506f1d3` | 0 |
| src/NEO/Transaction.cpp | 2852 | `42cee7d4f416ae02137097214808da5a7c53d27152d0682d4e677ebb42874f57` | 0 |
| src/NEO/Transaction.h | 1318 | `90cd5b015994a45fdc1752667cac60ddc1646342a1f6216bac5f4ca4d6745003` | 0 |
| src/NEO/TransactionAttribute.h | 3876 | `fa72c9ae0f2b2d5ebf57b0f0e7f8ee3d9c7dc772e7d335d58db18d4c0f33bab3` | 0 |
| src/NEO/TransactionAttributeUsage.h | 1060 | `a5e6331e55e228a598f251116a47f84e51389eb5821a39e23481d450ed55cb5d` | 0 |
| src/NEO/TransactionOutput.h | 1443 | `05ce88baf4b795438cd8a6768a9d75791afd90df83e80867619bac5601a37e46` | 0 |
| src/NEO/TransactionType.h | 464 | `a48b55eb9c0d53428d465e0e0f52c787a9244097ceb1230b6b087cd3c981d06d` | 0 |
| src/NEO/Witness.h | 1192 | `cd624235b15fe7623428ae4826801c8b778383c7a1bca1cdda4d6dc4556905eb` | 0 |
| src/NULS/Address.cpp | 2620 | `eaaee2aadedf69f8faaf00ed540a9ad93146f628829dcd972f6606c9553e9a1c` | 0 |
| src/NULS/Address.h | 1306 | `9a347fd92732ce7f6ed1f68d728df3cf6f2ee31aa8e40520031aab275c582691` | 0 |
| src/NULS/BinaryCoding.h | 4335 | `e84df57f6cddde6725a3332597a58490957659cc0006b4c2b91513757185748e` | 0 |
| src/NULS/Entry.cpp | 3304 | `bffbd6a0347892601ba13a8900c3bd1b7198d877bc60c985e983ad8b112fe037` | 0 |
| src/NULS/Entry.h | 1069 | `d10ef487b03b8e38dbf4d48b8f05e026b113d4996a9da3f994982569e7b2f3f9` | 0 |
| src/NULS/Signer.cpp | 8690 | `97676e76cb0f9d5d7d472c2c4b61b4228da6c7728c6f3aaa51411daf4f61f192` | 0 |
| src/NULS/Signer.h | 1726 | `0ad4acaac0293ce54fa9e7ab557a994e5952424be1cf5152ba0ea417c7724865` | 0 |
| src/Nano/Address.cpp | 1891 | `976e7f0a5a9c69e2ed088e101eab1285f82d4695de04082a7ce79e04bc65d26e` | 0 |
| src/Nano/Address.h | 903 | `d2eee2f31efc3bfc8a2d21a0435ec717f79df0f9873653b3bb631815567c5847` | 0 |
| src/Nano/Entry.cpp | 2288 | `4f626343952ac5b0eeae12a05ad028c17f89f4af6e861534998a43b267881fd1` | 0 |
| src/Nano/Entry.h | 1169 | `0a50cd1cbeb21240f148f0061b356bdc944de81192452a29e78ebfc899a15969` | 0 |
| src/Nano/Signer.cpp | 7443 | `1cbe555db46bf7762f350eb3dd61e10386d9599970546a73d673a2e8fe43eb07` | 0 |
| src/Nano/Signer.h | 1263 | `6751ea552645f164156e45bd1cd418706f2e40293741c1f4f1a5b806c39e320d` | 0 |
| src/NativeEvmos/Entry.h | 403 | `437f0ec266d924852f52c35040b186869fff0714d5dbc2f85ad934fdbdc97b11` | 0 |
| src/NativeInjective/Entry.h | 411 | `7ebee274b7db4f3d88586753f0d06f62e09f9e061f7aa532ac683909b2f881ea` | 0 |
| src/Nebulas/Address.cpp | 1852 | `60b06d8af96b74a745a8da0d38a49d47420c58acd5b223409775448b1e7ed1a3` | 0 |
| src/Nebulas/Address.h | 1099 | `a165dc967e0c0d309318564614d320dee6e205cf14dcfc6a9c2b601e655e4bb6` | 0 |
| src/Nebulas/Entry.cpp | 936 | `68418d24a1b12f298c918e3ba5ba551a248e5246fdf2309ebf2572b496ab5bd4` | 0 |
| src/Nebulas/Entry.h | 726 | `34de4433968f85549a4235446d8f13dd317a31545af9a363dd6f230b667f4dfa` | 0 |
| src/Nebulas/Signer.cpp | 2477 | `06ab357385b6d294dd3a93b3261dc43082d882f36b52726184356cd2432cbe71` | 0 |
| src/Nebulas/Signer.h | 1123 | `7931761f2ae1fd47bbc7b5d298cfb18a3cdef7f1194dae6954b66b038aa0225e` | 0 |
| src/Nebulas/Transaction.cpp | 3027 | `b94087e69a79cd20a8d67ad5c19c7817b84302c45e8eafc216547bfecdd5e2e4` | 0 |
| src/Nebulas/Transaction.h | 1306 | `e999c0d729605427f312a9cfe15fae88aef3d9e42e7289853b8c1a0fcf3aafa7` | 0 |
| src/Nervos/Address.cpp | 5685 | `65b53732b158aacd817372bb912cc47244e3e8c5d708dac8036539698aaa0133` | 0 |
| src/Nervos/Address.h | 2759 | `b2823498e2cac010b4a453e42b4a82004890be3ddf943dadf8df74f093999cab` | 0 |
| src/Nervos/Cell.h | 3207 | `a8605374e4b080e2a1bbc666e55f00fbb4f520694f8b397c7692d76bc08e9e44` | 0 |
| src/Nervos/CellDep.cpp | 948 | `179d66aa163da7da52074903cc0edbaef50731b0fc8304c95c107412f3dfc790` | 0 |
| src/Nervos/CellDep.h | 870 | `43ad9adc5af7674749ff33b00dddc285cf4ba03891bf894e4fc711e0f6e8b5d4` | 0 |
| src/Nervos/CellInput.cpp | 474 | `42c873d38ad2a5dfb8c2d7ca9636481fe6d1fea0bf4adf2d062afd6e9dfe820c` | 0 |
| src/Nervos/CellInput.h | 862 | `a681ce957f564440a9a9346f4ceb45a7bbf1450a68513893d3e9e77c434d866f` | 0 |
| src/Nervos/CellOutput.cpp | 699 | `d8f9980a8d8ccc412f19c886a35c42ad9bd06735e2bdbd9c55cca1f5481b320f` | 0 |
| src/Nervos/CellOutput.h | 1355 | `0a5cc7a22f12ce9e9646aff8976a9664525be2b63355413e63404f0404e6f466` | 0 |
| src/Nervos/Constants.h | 1736 | `12558f56529f4968fdfa3397e31ef0fb528db8b848385db254cd030aac23d1d4` | 0 |
| src/Nervos/Entry.cpp | 1138 | `dd9e304e0c30a6316954694cc7c3e98d5b94f932bd52164b0d232cdff7bc7f66` | 0 |
| src/Nervos/Entry.h | 819 | `0876fe68c900c1b5331877aa728315113b203778277f4dbcba51406905b3ab42` | 0 |
| src/Nervos/HeaderDep.h | 273 | `348d731d557ae022a5b27c4bd02ef2ef15affa5315390169c370af0fb7ec6354` | 0 |
| src/Nervos/OutPoint.cpp | 495 | `0a33cd099b795efa86d23d1b254c476ca6fea602d52b20844197ce8f82d558f5` | 0 |
| src/Nervos/OutPoint.h | 1417 | `44e32d0287d1e6bf82ddcaf65d85784571b03cb743e1bd08bdd6c8fe200a4594` | 0 |
| src/Nervos/Script.cpp | 1212 | `780512201d97e6fd4c87ae17a53ab5410d2441ee7ad18da0e0246c4e67f9b3b7` | 0 |
| src/Nervos/Script.h | 2924 | `9b8f8145b66345316118292a49e1d844c12109eb1e6bfc4d8bd4b32d5f3f4ba6` | 0 |
| src/Nervos/Serialization.h | 1939 | `189e01865ac2881341ce4e2932723fb1742136f47b8078827affbc780f7efd39` | 0 |
| src/Nervos/Signer.cpp | 1413 | `154cc30b9ea109cd1737831dcdac76de0903f798690e1441f73ce1cba20073ad` | 0 |
| src/Nervos/Signer.h | 554 | `8e778e8ad0e31f7c02b236b95815e11b745541527d82a611f66082177d8973a4` | 0 |
| src/Nervos/Transaction.cpp | 7165 | `f3e1012dd6463315bc310c2b1928c28b477dfcfa779d99536f8050f21b36d262` | 0 |
| src/Nervos/Transaction.h | 1756 | `683907f9caf4821784fed44eb3f1b7f6493b410adefad93d1b5c2658152701ab` | 0 |
| src/Nervos/TransactionPlan.cpp | 12911 | `cf9487815ecb8a85c2ca2a9841a432a2ad9c9f020d61a8bef1d42f9535591b4a` | 0 |
| src/Nervos/TransactionPlan.h | 3684 | `58beb8e7a50b5f1e79a774cb633ba584de873dfc61e64fc36aa4753b03984401` | 0 |
| src/Nervos/Witness.cpp | 731 | `e62cb8ea9b2467181cd6b610ee270517c26a6713cbfdefc16827f821a23bd36d` | 0 |
| src/Nervos/Witness.h | 653 | `34a8cb7b8fc4a12f2fc6cde6b699ae92a40d9a75ba7610472d9df3ccec9a6b1e` | 0 |
| src/Nimiq/Address.cpp | 3875 | `c4672c09ba3c3a7b9a8f0ec03d0ba576811b7f1fd17d061a22579478c7be6741` | 0 |
| src/Nimiq/Address.h | 1312 | `296083b12146c4572fac0edfdaa2a31be501442f7abca55b5f245f8de05c5b2e` | 0 |
| src/Nimiq/Entry.cpp | 912 | `f84de371f969ff63c99a6b69d3e2934c9e4b68739ddc7b08907d88cb54dcd457` | 0 |
| src/Nimiq/Entry.h | 720 | `66c47e9b3c576cf2ece5f099252b223acb95f74b3555e0bbce042c180f3bfa00` | 0 |
| src/Nimiq/Signer.cpp | 1316 | `275259d29d3d5f1eab334826d46ef97798a89102b9d72e66ad8f9588eb3947e1` | 0 |
| src/Nimiq/Signer.h | 980 | `de233ca7a52bbd063d635d9e9414c0c511af0eb63b3eb7a153fb0a1298ba3681` | 0 |
| src/Nimiq/Transaction.cpp | 2538 | `7b324a0e334e9666c53faa9ddbc50a954f7c99af2dc97feaa0ce575a942304b2` | 0 |
| src/Nimiq/Transaction.h | 1060 | `f13b5e6181c1e436b941a35d30d0571fd81abda8cebdbfbc61d2f825e8116a27` | 0 |
| src/Numeric.h | 560 | `a0d237b1458fd3711b84dc5e2979c904a23e1a67a23d6b191b60004b5c370e5f` | 0 |
| src/NumericLiteral.h | 287 | `7cd27b4cd89690f500ee9d9d362571c05b17c5701b007cdbce59624cc8b97ee7` | 0 |
| src/Oasis/Address.cpp | 1432 | `3a1aa5bcad83c27444e20df7207170715e09fcff9bf15dc96f9ff67c884ffc6e` | 0 |
| src/Oasis/Address.h | 1174 | `9f14ad0a4733953c4e3d01aeafe957d46830b40289c68b650f2e151aa72d3c64` | 0 |
| src/Oasis/Entry.cpp | 2079 | `97ee2426906a75398bda2c86ac2eed73279fd199ccc0185eb3cf9afdc521181d` | 0 |
| src/Oasis/Entry.h | 986 | `b8fc621680083ee6ee95814861bb382e3a354bebb77bb1e596f5a8a745beee99` | 0 |
| src/Oasis/Signer.cpp | 6140 | `d41bff117268c9003d923e39284c58a324b75f15799e042c7325e7f52552dd1c` | 0 |
| src/Oasis/Signer.h | 1280 | `a944c2285e5a4879a8bc6279a4646f8fd4e0d4ac9e10f0b3c569675d29414fb8` | 0 |
| src/Oasis/Transaction.cpp | 4897 | `64baef396c16e3afaf7afe513af3f8e73536bbe8cf0262c73d4f50b6843d13ee` | 0 |
| src/Oasis/Transaction.h | 3545 | `39360f3077f28cadbe4e9d9383b42e466ef781c9ca044c6d0228d3a085d11614` | 0 |
| src/Ontology/Address.cpp | 2265 | `224655730153e1af82d1b03dec7a3c18e614a39bdfd37f67a171a4a9aa52f6c7` | 0 |
| src/Ontology/Address.h | 1177 | `84bd1fab04966b9550348d4ab6043e8ecafd9ec0aedbd57e5936d7ba6507b0f8` | 0 |
| src/Ontology/Asset.h | 1099 | `20c5113841930729a6e406227cb4b393edc5b754ac9ccce4e149402a0cd66feb` | 0 |
| src/Ontology/Entry.cpp | 3176 | `5f59f9260e3eb809f833eb605d33f83005ae1de55deb37fb465d468b493450d1` | 0 |
| src/Ontology/Entry.h | 961 | `ee695c228aa385a1ce4214a51e89b571badc2ec5252a3fdd611ca5ed519e8786` | 0 |
| src/Ontology/Oep4.cpp | 2737 | `94f4d026f0147b72f7a1706d013b2bedec1f11707118c662264ea42eba77c419` | 0 |
| src/Ontology/Oep4.h | 1359 | `e29fc79b99388e0323f9fa9540902e024a9aaed1cecacca75eac9effd2f609a8` | 0 |
| src/Ontology/Oep4TxBuilder.cpp | 2595 | `d42002f6c3bffeda2f5d7157e77d5a11a05d134795daed9eda45304c9c5c1f4d` | 0 |
| src/Ontology/Oep4TxBuilder.h | 639 | `33fe9008e0b02b9b69a45575d8fac95c8ccbe154e8c7a3f3c3ede738a8a25855` | 0 |
| src/Ontology/Ong.cpp | 2878 | `e37e25bfe9bbfb7b7eef96dcb7f6ef2402a0df71025b465a743383ad81803253` | 0 |
| src/Ontology/Ong.h | 1268 | `8a1fc286e000c35aa7ee4f18ad8936668155648e2e63580ae48357743e5a2286` | 0 |
| src/Ontology/OngTxBuilder.cpp | 2655 | `05788ebb3cabbb79c33f9098b94bdef9bfb0226481f3ec76cc63608b96b9d2f1` | 0 |
| src/Ontology/OngTxBuilder.h | 718 | `9b799547250e32305ed5b79e8642ac415be01dcc13bfad6adb742d2393a37b08` | 0 |
| src/Ontology/Ont.cpp | 2245 | `d7b7f64ecc6a8c7b6ef6021011b064436870e0c38b448a07040f4e3bdcebbf82` | 0 |
| src/Ontology/Ont.h | 1109 | `913437ab34867549a4d1c7387334fd784bd7df7cb5cc6cc3feb6c91103e79ee8` | 0 |
| src/Ontology/OntTxBuilder.cpp | 2051 | `374a9df7e3a8f5b31d34519c56bf6eb277567037b24dcfbb31ab75fb6e7a2dc4` | 0 |
| src/Ontology/OntTxBuilder.h | 647 | `36881d41b340d161d57c154f2dc00469c15480c9c3474c360ff23c41f37dee5a` | 0 |
| src/Ontology/OpCode.h | 787 | `2d1af1999e9e78f29323b58c45995a2dca2453cc946e4a1be2929f481bcc3d72` | 0 |
| src/Ontology/ParamsBuilder.cpp | 7970 | `214e43e42fb3662d19a0b57aff3acb8d1b52534ebc6a66a47bd0f6e09b53f809` | 0 |
| src/Ontology/ParamsBuilder.h | 2642 | `a85d499f25c022ee3b0ae11d2c4369b4670c9a1b2029b803ab860699d1908840` | 0 |
| src/Ontology/SigData.cpp | 708 | `5136da53444aa566667784f390b3fbe84a75cd3d907d6e27285a344a8afbeec1` | 0 |
| src/Ontology/SigData.h | 470 | `5022b8fdcc22e916ef9d754833bee5bdea258e6cad83b51298905ffb23dec44c` | 0 |
| src/Ontology/Signer.cpp | 3090 | `44e53ec8e1426967eab895c3c6c7faace24986a8157994738f497a8fd459c4ba` | 0 |
| src/Ontology/Signer.h | 929 | `bed3fe94e65712e28412b86a172210ab7b37184267b5bb002eeb3da4fe82c376` | 0 |
| src/Ontology/Transaction.cpp | 1563 | `6e2defcd606adf4a45faabe70c470ffaee632ed0670eb55ccd457695642a656c` | 0 |
| src/Ontology/Transaction.h | 1278 | `d9e5df9cba9413702008a38e18422400060943ad6606405adf18703ed9e6b2f0` | 0 |
| src/Pactus/Entry.h | 377 | `28517a4e61a30b645093fdf01880adc3397162aeeeb0af07dba4ff6283f08f6b` | 0 |
| src/Polkadot/Entry.h | 400 | `bb2a5317f97f4f341bc5b90efb12359e579c1c77749441cc9868b8c677f6a1ae` | 0 |
| src/Polymesh/Entry.h | 383 | `b049fed56503613261171ba8068d74316cad2de11322115f31605a066c8e719b` | 0 |
| src/PrivateKey.cpp | 12830 | `0c07c44035da0df7578bf4908529cff150b93713d8a77aaa9465996bf4bb64e0` | 0 |
| src/PrivateKey.h | 6367 | `1485aef0e84b5a240b2426277bf2a345b7600ec277ff5d5c3cacb363ab6d333b` | 0 |
| src/PublicKey.cpp | 11519 | `be1d99f2de6e665cd3e0f0b8e842ac28a5e2207d96dd50b56d95fa2cd6956375` | 0 |
| src/PublicKey.h | 4740 | `68273cecf1be9c91b3d4c3a440f17d945c4197fb0ae8e004915ad72f38ec1d93` | 0 |
| src/Result.h | 4658 | `0cf897798f73b74ff7264fee8811c2e27398d564d9883ab4c51b3a44b3fc6aaa` | 0 |
| src/Ronin/Entry.h | 261 | `e7976e5f1e43c48350ae8ea4a060a8b9276aad6032f13b31a09317736ef7f5a9` | 0 |
| src/Solana/Address.cpp | 1259 | `9279b88a0cb2fa8a4ce519023269ab51360b68258c0bd1c8a13fb6532f3e2833` | 0 |
| src/Solana/Address.h | 1230 | `805b82994e61e3a56d3b8b8a47b2d3cd781b654d33006b26455b2ebc58af3f2a` | 0 |
| src/Solana/Entry.cpp | 1356 | `5fde572aa6b7bfc92a07e964d727e64eac8404d8cff3c8d590242cb86dfcecb6` | 0 |
| src/Solana/Entry.h | 702 | `69e361941a134ffb48c83aa1c8663fd25a5bc59653c86a3e016bee989834cf51` | 0 |
| src/StarkEx/MessageSigner.cpp | 681 | `bdcadfb6d9fd40b2a0a7fdc412f3ad2be5589cd30f67ca545887e613c32f98b8` | 0 |
| src/StarkEx/MessageSigner.h | 900 | `fc925d1a171f5007746f429be1affa5a4176f0bc6b3053e5c104b9165eba46ca` | 0 |
| src/Stellar/Address.cpp | 2332 | `ba1160618085289692c7f873be1e7726490356eab33cb648942738c4ced6fdb0` | 0 |
| src/Stellar/Address.h | 1123 | `486685e9e338bee871fbf7cb76b1119967cf830f6c24601db8cc0e5fea9804a6` | 0 |
| src/Stellar/Entry.cpp | 4134 | `185fe6c79a104b6c677760eba9e3d6bf97f39f2d871345b4c51b4e552fb8c218` | 0 |
| src/Stellar/Entry.h | 1108 | `da7739668b0375dbca72ff766af89e838adfb609e7e1548f53cee9a69d3a92df` | 0 |
| src/Stellar/Signer.cpp | 10034 | `b479bac6ea8fd7742b4d9ff749fd4d5ab25f8f3d4fc936514f3a645ff02eafab` | 0 |
| src/Stellar/Signer.h | 1158 | `cfe3afae0fcedee4a3dba9f74d1b0433a16579e72e3d52c0c488be5e76845fc1` | 0 |
| src/Sui/Entry.h | 222 | `9467bd27ba80602a63d87cc287df2860d3026aabfb55a92ba03c38f1c0c6cf5b` | 0 |
| src/THORChain/Entry.h | 426 | `05913a2a6277afa8d176cff78559e2cdc28610265dcfa37e79993b27e0080fdd` | 0 |
| src/THORChain/Swap.cpp | 14605 | `0a56614fe2d7c4fc260a9a399baa46c9185cbfda248b875c7bbdc7d09e09ace2` | 0 |
| src/THORChain/Swap.h | 4675 | `fb80163eb8d041ca5f794f6d4712ac464675d7b95121bab70c516125fa747757` | 0 |
| src/THORChain/TWSwap.cpp | 6251 | `038339206bb5ff19448ded01e700a1a5f4c6d281dd177c97e989a7d7d318c7ec` | 0 |
| src/Tezos/Address.cpp | 3653 | `5d8443c59ff76a7df431861aed5be7fdcfc902c4066b538f684082198809bc11` | 0 |
| src/Tezos/Address.h | 1094 | `0a06e770ca929f9a847e0902c24e54ca7925256539c175919ef96d53e0f7b38a` | 0 |
| src/Tezos/BinaryCoding.cpp | 2147 | `a37b37843d95814a53c25b28ba0acc86f0d1b3aa9d314de09cc686675fe28257` | 0 |
| src/Tezos/BinaryCoding.h | 418 | `5f781f8a368ca734a14715206cf9775cd55637284e7eee810a79c9017c17167f` | 0 |
| src/Tezos/Entry.cpp | 3092 | `98fecc16f642b57742e0ea5765dbed545ce9c7c898db70c478935115ca07e571` | 0 |
| src/Tezos/Entry.h | 1160 | `ad5f49ad60bd168c7b30ab02ddfe92c58452da33b1a03b7c78b590de51eab228` | 0 |
| src/Tezos/Forging.cpp | 12389 | `9367e377d9707a887b886d8c2a381e83c325428333f8b27297cec8d392579e4d` | 0 |
| src/Tezos/Forging.h | 1005 | `eeb7e2018996089bd32a717fc77d249a343df95f5885909aa6a532eef9a69cdb` | 0 |
| src/Tezos/MessageSigner.cpp | 2121 | `63f3d7beefbd4ac6ca2a2aa47f1fdbb2cc56986116aa0277fe92881ca48c804e` | 0 |
| src/Tezos/MessageSigner.h | 1708 | `c4436f4df0766bbf08a836058943d860ae746dde8c85fa682512f3331f44a1fd` | 0 |
| src/Tezos/Michelson.cpp | 1566 | `3f8250911c32c13088571c202884005a5055e4bce34ad64209b23b16fcd138ec` | 0 |
| src/Tezos/Michelson.h | 1068 | `d0625227e8c806b048547cb509258e90c8e568d7a0cc4b09ab44de212035557d` | 0 |
| src/Tezos/OperationList.cpp | 1841 | `8f7af14a1c46bc5abcff850a556da6983de171a7ac71782affd857cc3fb2d901` | 0 |
| src/Tezos/OperationList.h | 633 | `4a31249a60485a41a7b4add9db2999e8ab42e18973669d7be6c0a956b1ea9bd9` | 0 |
| src/Tezos/Signer.cpp | 2335 | `0b448a59987fad2f025065a76dbd495c612796a3e1da5a4bf69efe9af9339fc7` | 0 |
| src/Tezos/Signer.h | 950 | `e839e7616b92280a6264c67abc93e4550fa641386715148672c04ef9b350affd` | 0 |
| src/TheOpenNetwork/Entry.h | 244 | `3bdd4e11a099c51b545ad7c02fb263c3c173722dafee83a839cc517ac8488529` | 0 |
| src/Theta/Coins.h | 389 | `a182944204699841fb82afe916d2d4955064cbfc3c5519292bb352f50612aacd` | 0 |
| src/Theta/Entry.cpp | 2395 | `4b4fd785a015747edf1261902b80efa8c9459a2a4b7d6a7c7f43d845b9f09246` | 0 |
| src/Theta/Entry.h | 1148 | `ab95e7c1dc30b511f2a6f07ef2265a087f257d18d789d3ea8ba9fa57b12a2031` | 0 |
| src/Theta/Signer.cpp | 3879 | `64d25348a040d1eb18e992037fe656d3a504987cf437e9218862309ee084da3c` | 0 |
| src/Theta/Signer.h | 1200 | `d537fb770808e42f0f6c0b65e83adbb0b9d20b686c06c8ac260c25b34a24ac53` | 0 |
| src/Theta/Transaction.cpp | 3609 | `5e4252a226e46ddf3ef31694d4fe1d5a50f5b338ffde8ac009d57af420c8f56e` | 0 |
| src/Theta/Transaction.h | 1828 | `6f6d4dd9ed382d5d9fcb2f5dd8a2aedabd3e99ff2df6a70dc28b570946ce02a9` | 0 |
| src/TransactionCompiler.cpp | 1522 | `9ac79a7f2f7402d0a7814326527b9ad504ea8f045cb04c52b60c11fd666df946` | 0 |
| src/TransactionCompiler.h | 1302 | `9a130d9ed7ba4ad169347f3048db571a2ee835c10ddd94e19b2c0270a33956a5` | 0 |
| src/Tron/Address.cpp | 902 | `b7b31b9cf936bd36faa0a7ddbb3f0993b35cdbdd7f34bb13873302c184542f95` | 0 |
| src/Tron/Address.h | 874 | `52b66b60f9ecfcb2d1830b72cbe08927d255e1bf8277d26561c227048ecfc601` | 0 |
| src/Tron/Constants.h | 3212 | `b38712ddc1d2a072462e509c152ca36a881980f720a2560d77ebbfb4ed2ae105` | 0 |
| src/Tron/Deserialization.cpp | 21719 | `4c7af79a315ae9b3db2193e1f08873641df6527f08f2d5c7fc0a7040b9c39277` | 0 |
| src/Tron/Deserialization.h | 1249 | `0e4a52b4ae07c685ace4b09b360a3bed1277831dfb0fa30bf6f5b108efa4853c` | 0 |
| src/Tron/Entry.cpp | 2108 | `ebe49a6b5a4e9d135939511b6d28f3ed7dbfb8d71d75012de3ef405c3f3220c3` | 0 |
| src/Tron/Entry.h | 984 | `debbe8183bc9721a732fedf021e0682768c2d78adb2baedd3600c90202b615e6` | 0 |
| src/Tron/MessageSigner.cpp | 1156 | `043ec5c1151dcff4494b3374ee8750d685e0579e3dc59b742c836915b724c3ed` | 0 |
| src/Tron/MessageSigner.h | 1138 | `66cc25524305692a6528128245c22429fd32641f087b0a6662b490b891ef15ab` | 0 |
| src/Tron/Protobuf/TronInternal.proto | 3779 | `cd3ca02d0a871ec3a12202a00cb025cfb7cd680164f3cd917bc5395315cb9150` | 0 |
| src/Tron/Serialization.cpp | 11268 | `73b2837fce35d74c698b2a9f8d7f0728409083a79ecaa9d1ca28baeabfa31217` | 0 |
| src/Tron/Serialization.h | 396 | `a2fa4ff2f57bb1d577bf3f26e5168391eca606b06ba5ae163f80aaa6f59282da` | 0 |
| src/Tron/Signer.cpp | 27459 | `2ea580fcedd2af9e82315a984f180d83e66aac3800922f8fdb058f7df5cc3665` | 0 |
| src/Tron/Signer.h | 1989 | `4f0551124689b5125031c6d38a0bc22dd11301f2fc81f5e585a98cc720c0ac5b` | 0 |
| src/VeChain/Clause.h | 719 | `d9ae0caca349d92a4247a813af669a3d92aa7395a3c9bfffa816650d081b08a3` | 0 |
| src/VeChain/Entry.cpp | 2654 | `b39156cb5f5030bc19c71132ddf8043749549952ccde9e421152b52636dc132f` | 0 |
| src/VeChain/Entry.h | 1154 | `0caf42f50902da52dc38ac569b33597320f9bcf06cfa32408efc9930c98c62c0` | 0 |
| src/VeChain/Signer.cpp | 2812 | `985e9ddf18da3ead83f7f382718a536e69e0bc3c941f8a5c30e959de3e9df250` | 0 |
| src/VeChain/Signer.h | 816 | `58ea7aeeebb663fcbed47f36323d5e615cf1f1a7ef88fb11f2ceb061906dee1f` | 0 |
| src/VeChain/Transaction.cpp | 1796 | `9c3643edda70ed0db75ddeceba08b7b003a698555ee878b5ed7d0cea750b90be` | 0 |
| src/VeChain/Transaction.h | 1539 | `40727c2effeac42da97f9d6376bbebc3cd5b7386b988d26da9c63ed35dbb0692` | 0 |
| src/Verge/Entry.cpp | 3755 | `5b8f697683b1fd143d52dbb082f2b6e2b4e28a2cc554d2f2a05108576dcba5ea` | 0 |
| src/Verge/Entry.h | 1162 | `0255a7dfa6648c2589254f8fc5e3862ab49de1b38fdcf073104938e752d2e119` | 0 |
| src/Verge/Signer.cpp | 2001 | `5b0c66f0f943256b0c2567f1ba313b4444d6d3c8498d6a80f9388006c5083d68` | 0 |
| src/Verge/Signer.h | 1024 | `6fa7da9a2cc65835739c1df8131ed1ccfcfaca82aeed6cc437ba9d60e6d49029` | 0 |
| src/Verge/Transaction.cpp | 5861 | `6a8f0665daa50b8e438ef4ed82dfd6fe6af31ae0f59f773ff8663ab2987c94b5` | 0 |
| src/Verge/Transaction.h | 1987 | `35e633fc10811e851571b33f00239ac0a6541b30b2a66beac76520c258fe5fc5` | 0 |
| src/Verge/TransactionBuilder.h | 1388 | `e65d47ad3619e18d5ee4d2e4aa39b625e772ceb62fba810d9eb4fa0e9fb08439` | 0 |
| src/Wasm.h | 314 | `882a321a6b656d593fc9b3100e7b654b70c756456216f7455d00fe070ad1e86f` | 0 |
| src/Waves/Address.cpp | 2202 | `44aae14853ee6d3a48cc494a27140ab17238dd3ea6d19076b34590651295abf8` | 0 |
| src/Waves/Address.h | 1276 | `bac6582a62e4f5d74caf83dc37fe2f0ac676dbd819799e2a1c8153e08d21a19a` | 0 |
| src/Waves/BinaryCoding.h | 708 | `53e0bc61727266c323e693b2e9d522afe3f84b8ddf52984acc934e4fc9c78f4e` | 0 |
| src/Waves/Entry.cpp | 933 | `bd2f23401b221931753a5a0782ac71cd6454d5c9e27c7a24383162a9abd670e7` | 0 |
| src/Waves/Entry.h | 720 | `cf398bf75045916e216f1e66f58e240d95dcacee10461ba87cc4d95f1e8fe814` | 0 |
| src/Waves/Signer.cpp | 1041 | `f07489f7e48a6976d1012b715bf79dacc6dcb091996273f9a133611e35381604` | 0 |
| src/Waves/Signer.h | 665 | `f35a0fa513858d8004b46bd291168223f76598f711eed9f6423627ca14cc18b2` | 0 |
| src/Waves/Transaction.cpp | 6700 | `8ee4a3e11517ffd1be38d7d9851c902ef1c7e6b776e321faa4ba79b0f323332a` | 0 |
| src/Waves/Transaction.h | 914 | `511a5b09b259aa3095f1c557a5197fc3bb2ab486c79f646a3a2a4cf837673494` | 0 |
| src/WebAuthn.cpp | 6295 | `c2f3255822733dc1c1df7b0a9d05d2bc86266ec50425eb99bc1c3526cec5ae59` | 0 |
| src/WebAuthn.h | 343 | `7e6ac2e91bfe4f9ba42196696cef69e7257da5eba38bb0682069202781d74716` | 0 |
| src/XRP/Entry.h | 412 | `324d935490df2473274acc53dd81e743377176a30446f0a407d216beca0d6505` | 0 |
| src/Zcash/Entry.cpp | 3504 | `ceb217d57319304f72a066c08f23864ac865c5fc99282d2d1e1bece144de0f91` | 0 |
| src/Zcash/Entry.h | 1114 | `f042fbdc3649bff0670364d94b5ceafee6255cffc6c02702fbc543edba1fccec` | 0 |
| src/Zcash/Signer.cpp | 2260 | `89d197eee53d7d1af15928e5332d12dfadf7a221e6ff09afc1accc591eb5f5e3` | 0 |
| src/Zcash/Signer.h | 895 | `ab56f2dbda2844d05ce7107ff8bbb18a53f5a004e2398e43ffce2c07f4c2b1dc` | 0 |
| src/Zcash/TAddress.h | 1532 | `73ed3c069e84406a2f3874bc9a20932919c7b5767f0cfa5c2bb77f1bc2dfdb1f` | 0 |
| src/Zcash/TexAddress.cpp | 1076 | `e3ccab608788bd446c97fb0c34d39234e2069687701f1b51f6f1dbbc90e0313a` | 0 |
| src/Zcash/TexAddress.h | 995 | `eb563fd55b48138b43583b621e6918a0ba4cbe03843d90397e125c655f189323` | 0 |
| src/Zcash/Transaction.cpp | 7763 | `b5ef1fe4b71aeef2d14bdad4bc9d657a9c8ce6ced1e8e04700cad30630de971d` | 0 |
| src/Zcash/Transaction.h | 2455 | `dc9c4bd15032030b690c9c609bae60ba58dc244a2e033ff09dc6d9c35f621d7b` | 0 |
| src/Zcash/TransactionBuilder.h | 1524 | `51b474d350863ffc60e9e205b2abe7798bd03c61730f7199f2d023287b8b6b28` | 0 |
| src/Zen/Address.h | 1588 | `6da7665a5d31615336044a67c675299d2ce59df5586b0023012337288d515541` | 0 |
| src/Zen/Entry.cpp | 2838 | `e527d2cca915871969d5c1b3e7de83271221aed069545afa2118965990fdb29f` | 0 |
| src/Zen/Entry.h | 1158 | `5213f886d66cd77ff6152c19ebcf83c3b2ea0547daff58dad0383a9493495d79` | 0 |
| src/Zen/Signer.cpp | 1995 | `f654c4aeaef8d9803bdefb6ef80e60083cddadbb90c570e85abd85e8c8c30d4a` | 0 |
| src/Zen/Signer.h | 981 | `324d29e65a474fc04f895da21b1e6e255315a925d26f9436f3017d08c9d9c6e5` | 0 |
| src/Zen/TransactionBuilder.h | 3902 | `1876f74a19de4c9afc89d852a712ebca4d3479e9a8412f86892b634a701c3aab` | 0 |
| src/Zilliqa/Address.cpp | 235 | `1bb4b3ab46a1fdf1b2ed65db1ba0fc19295553fa75a07232ccf43c15dc7d3851` | 0 |
| src/Zilliqa/Address.h | 1008 | `86081bed71ee81755e6e56611a7bd2ed538b2ffb9908c3bb31ecd44601cb65d4` | 0 |
| src/Zilliqa/AddressChecksum.cpp | 1031 | `0bf643cbb0870609c954db7b88772609e270b91ba2aebcc086fba379a7394df8` | 0 |
| src/Zilliqa/AddressChecksum.h | 225 | `e922b6ade3202e66e6d69eec41fd7fcc01c17241e983c0a7bf0acb103cfedb4c` | 0 |
| src/Zilliqa/Entry.cpp | 1351 | `bd55078979ba63ed5573f731490cccbf4de9e17135334ea3d20ad4f57a694053` | 0 |
| src/Zilliqa/Entry.h | 949 | `be2b8ca61c96e038fe1fe6346c674337c3611dfcf660b546dcd62b3f3b48cd77` | 0 |
| src/Zilliqa/Protobuf/ZilliqaMessage.proto | 1098 | `fa73152ef4073b90af251a0fb9978b5708c0ca65b6719722a1d5d6695894405a` | 0 |
| src/Zilliqa/Signer.cpp | 4503 | `056ff9794857e0b38c524ab0adfe60bfff150b2d32189abc73045cb66723166e` | 0 |
| src/Zilliqa/Signer.h | 747 | `1578901cd40b4cc8d7c3bca811b7dc62eea8a64cca103b8644f419da5bdcb517` | 0 |
| src/algorithm/erase.h | 965 | `afe608355f02c1cb364cea24526cc9d7bde7bdc74eb098393bdc84cd99e0e1e8` | 0 |
| src/algorithm/sort_copy.h | 589 | `c42a85a9bd05c4b9b09378238630683c66315580f0066bed418635a426669414` | 0 |
| src/algorithm/string.hpp | 1215 | `ddf5e65d206aeae04976f90176a065a663399b5b9e414767eb177ac9b3eddb9d` | 0 |
| src/algorithm/to_array.h | 397 | `1652640ed0d904fe78f387166f9265959b05fd0374415dfddc0bf285d828ed37` | 0 |
| src/concepts/tw_concepts.h | 292 | `00ad55da44a1e64b59b3de1defd1f43f5b48f20cd70b71f59d4b4665f3ecb908` | 0 |
| src/interface/TWAES.cpp | 1466 | `957b2f4abb096d97c2904da3d7f8bb0df1bd985259d66758f05e42b4bbc020a9` | 0 |
| src/interface/TWAccount.cpp | 2185 | `8e199c968728ec62946335ef6be691413e38028f79a412b0701365c461158186` | 0 |
| src/interface/TWAnyAddress.cpp | 5043 | `ad3c0969ba6dc24c5bae6dd92a667fb76e905e8bbf8e3ea112c4ce9ab77713d9` | 0 |
| src/interface/TWAnySigner.cpp | 1194 | `02fabb20b2d936da8f284229fe29f718c687fd9cd429da23f44b1f0e4e9457aa` | 0 |
| src/interface/TWAsnParser.cpp | 603 | `dd9dec0c7032265fb919e80aefb80a9024b0331504afb1f9fa71e6a8639f405f` | 0 |
| src/interface/TWBase32.cpp | 1265 | `2ffe4e86489576f4653058e64584462121d9289b14173430eb6cd5bf4c372479` | 0 |
| src/interface/TWBase58.cpp | 1220 | `6af7b19a0af469d8587844330b51b5f95c559ea68c5d3dcec495555549da11e2` | 0 |
| src/interface/TWBase64.cpp | 1096 | `586aebeaea4ce0ef82f6dedeaf31d6391d739d19f28bf285d4c39a919b2c704c` | 0 |
| src/interface/TWBech32.cpp | 1901 | `93a9958484e5ddebbec8afdfed5ada052879224df805755295cf6d5fdb91584a` | 0 |
| src/interface/TWBitcoinAddress.cpp | 2114 | `289794b8dbfdb4e164f529bd15ebc27fa8430f16424f6b706c06bb8cb2ffad38` | 0 |
| src/interface/TWBitcoinMessageSigner.cpp | 899 | `45af3b69e373817e8b94f00250acdcc12bde3ba7bae8b60a2a4c8e9ff4bb801a` | 0 |
| src/interface/TWBitcoinScript.cpp | 6106 | `f2230bf6170da7b0e6663c25097c7fb436239dfbece835c780e4146ad6eb0484` | 0 |
| src/interface/TWBitcoinSigHashType.cpp | 398 | `23cab3c1d4045064586c7c982e3f1673ddb9bd05999a4301a7d1df6cd97416c1` | 0 |
| src/interface/TWCardano.cpp | 3483 | `64910d4c3e6acdce30b2e655591dd24968487d68908b6b569b8534924aae2d97` | 0 |
| src/interface/TWCoinType.cpp | 2826 | `b6f4f9667b206fd3068d478d39e98120e41088ecf1ec97fc0963252b7c1b9388` | 0 |
| src/interface/TWCryptoBox.cpp | 1026 | `919cf11bebe4389fabbbd89cf2cba6ae0d4aa7cb91d6e5fa31b5dc4599aa9027` | 0 |
| src/interface/TWData.cpp | 3826 | `2ebc470532e3edc9e5b115314f09e6851750f9c5a36d3cda0a8d51f40db80113` | 0 |
| src/interface/TWDataVector.cpp | 1256 | `12e72f5e0ca5b87cdaaf4b007a169f69851a126a56308146ee1c1a1684073293` | 0 |
| src/interface/TWDerivationPath.cpp | 1993 | `4c3d808ba374db011eb2f0a8bdc818705107bf606d11c41d13c0e5ccd2e104fd` | 0 |
| src/interface/TWDerivationPathIndex.cpp | 910 | `69dc1d96d6bac36bcde633c8dce9497270f4cc2e9e5f79992846a493d8b27a4e` | 0 |
| src/interface/TWEthereumAbi.cpp | 3586 | `4aa636ac440e234198fc6f5909a7ce622c4fd34945ff783974c0fc3635bafd4a` | 0 |
| src/interface/TWEthereumAbiFunction.cpp | 15759 | `895cf4c991dea1a88c5414dbe8db02980a834b67e8102d3e34cd6b6c932ad365` | 0 |
| src/interface/TWEthereumAbiValue.cpp | 3315 | `90cd1fc383c9075864a09b853d94d571a7907f9a1a6af45738857a7c4a7555a2` | 0 |
| src/interface/TWEthereumMessageSigner.cpp | 2946 | `ee5f05e8f7392762e5762c2002d892b1c0e12b5a07932e680c7f2cd826eeb9cf` | 0 |
| src/interface/TWEthereumRlp.cpp | 620 | `edf84a476b4a98d73f67c1b00afc6b8c2699d86bb6195332ea2c8d4c84afd071` | 0 |
| src/interface/TWFIOAccount.cpp | 938 | `ebc06a7bdf389b6fcd7e09a8d30c4ab27179433a54a8e5b1a4f70e0fdf0c12ae` | 0 |
| src/interface/TWFilecoinAddressConverter.cpp | 1154 | `d3212310f89f94cf78d7c4f7cd2ced7bc8971beee7e74b61b660c93e9ace3d7a` | 0 |
| src/interface/TWGroestlcoinAddress.cpp | 1422 | `2fabc9fb41e853e8f70a8450d2b767304f7990458e854e20520f1742244ae20e` | 0 |
| src/interface/TWHDVersion.cpp | 923 | `ffa450508aeb2c89cb01e3bd7387fcff4bb2d55bd14117694936696395e795ea` | 0 |
| src/interface/TWHDWallet.cpp | 7164 | `d48e24459a169828b755f1f3af189ef53158a2e0f80ddeb262419676800c1086` | 0 |
| src/interface/TWHash.cpp | 5083 | `6af31309a6c25d0bb974320d53dbeaf85a807239216e17c80a8a415ee7c8f540` | 0 |
| src/interface/TWMnemonic.cpp | 599 | `0e69a61efa218dcc537d5f9c669d56ae6651477621ae6682ead739c90a6597c5` | 0 |
| src/interface/TWNEARAccount.cpp | 981 | `7313ec5b0172b8913226faaca4d1ad7880d43cc1c4baca56fc9e9c9d50326c16` | 0 |
| src/interface/TWNervosAddress.cpp | 1613 | `a1aa53e28065eb6a699b9ea7874b93f224e3bbe2ef67860d7f4debb6614efe21` | 0 |
| src/interface/TWPBKDF2.cpp | 1264 | `c67de2e59283e739d7f22becbcd1702da84e81bc518d372ee6714550a68395a2` | 0 |
| src/interface/TWPrivateKey.cpp | 4538 | `fa9e78fa9bc321a5c1090855e5de9ef869d723b6a84b7335d3524fb3a2b734e9` | 0 |
| src/interface/TWPublicKey.cpp | 2829 | `858b70aa947aa1a8bdf76566e15e2386dbfa813fa35d6bba8b0643810c0fb02c` | 0 |
| src/interface/TWSegwitAddress.cpp | 1986 | `beb17a71943f73fc9573fb98e59772bce8102e4403ee74c3f3f4cba44dbbc0cb` | 0 |
| src/interface/TWSolanaAddress.cpp | 2110 | `15cd7c970f9fbd7c3e1b7b214c580c30f6c44f7b8f841536d3f536bc9a0807ea` | 0 |
| src/interface/TWStarkExMessageSigner.cpp | 844 | `00d84c2829eac8626ef98b3ea4aa61d828b438a9d4ad388580b526a2e66493c5` | 0 |
| src/interface/TWStarkWare.cpp | 646 | `0db03062aa51249f1cff7b1662d51a502b550d11c4d718b802d4f73da67e915d` | 0 |
| src/interface/TWStoredKey.cpp | 14521 | `41063e160ac67219ecde6d2b50e096dabc990751ee767eb7be5775f9231b70ee` | 0 |
| src/interface/TWString+Hex.cpp | 1038 | `d80ed8213ee952a3bc932f2ff8f4f201c8c1e5b99316c69b495f8b319c66f876` | 0 |
| src/interface/TWString.cpp | 1508 | `665b372df5964dea7c7369a145eb4bf719ee73b22d9f0f5071b24b916363f1a5` | 0 |
| src/interface/TWTezosMessageSigner.cpp | 1344 | `2b64aed7dc694d3f3b9fa144121508571da018729f053d0c81cecec48b2832a5` | 0 |
| src/interface/TWTransactionCompiler.cpp | 2359 | `5e6d4da825f6e1b9e85e8a40c68e0b16feb187d90286e30d21169551bccc13e8` | 0 |
| src/interface/TWTransactionDecoder.cpp | 665 | `1a439675c9b251abf55aaa1522031703d17aef8bb658d8a5e9cfffba3db26ad2` | 0 |
| src/interface/TWTransactionUtil.cpp | 786 | `07317261d82cc8e02372b78a4809bb53deb4c40611bdd48380962c6654301438` | 0 |
| src/interface/TWTronMessageSigner.cpp | 825 | `7d2120d6f23ad31f9542045cf8b40b28ae711a4d1812440a1d77feff72ef63f3` | 0 |
| src/interface/TWWebAuthn.cpp | 1506 | `f6aceab3084ce58d15a31ef6f14dfb20556f30301ab27b381b4d13e427dc00da` | 0 |
| src/memory/memzero_wrapper.h | 1564 | `ea18e8594e846c35a0070a9ebd30a63e527a91da1cfc1d388d66b4e2791a667c` | 0 |
| src/operators/equality_comparable.h | 419 | `382b90c46d7e0f0fcad658fa8efd951924b08acb8e0f5422a48c2f78c809c7e8` | 0 |
| src/proto/Aeternity.proto | 1196 | `2839833e2201c83b59e048d54a67d13e1c250c2e51e6cb30bd3e547cb11bd4ea` | 0 |
| src/proto/Aion.proto | 1095 | `66da606479d0d8e3ca88091844b5bc0717ff1b7da9309718b7b9e9d80408df7a` | 0 |
| src/proto/Algorand.proto | 1703 | `27406f5e5e0de829ca66dbe0dda715490ff7e0171c5b14d8adc3fdb4593929b6` | 0 |
| src/proto/Aptos.proto | 5481 | `5f6d07467d4ff67d09e593ab9cbf672c35e37f3e6629dbe27e68b6fa58b2dabd` | 0 |
| src/proto/BabylonStaking.proto | 4056 | `8e0549befd47eb9e57ad6fc680d2ca58421fc47f44a77244a521db71e23531f3` | 0 |
| src/proto/Barz.proto | 1553 | `ef6317bd87641180e6a7f63e347d8510d829057f861c5a98b079b4c8ed70ef5b` | 0 |
| src/proto/Binance.proto | 7925 | `e7e0a3a13013f1fed244493a2f4230a21dc8bca99a9383d6d5aa5858dc8d3302` | 0 |
| src/proto/Bitcoin.proto | 8062 | `2d8cd45caf021cc741bbfcd5c49856fcc809cdefbdb13101268ca23899e625d5` | 0 |
| src/proto/BitcoinV2.proto | 15539 | `f1ee501d01dceba94f8ebeb5baf4b2a61163b3cd065955609320a528ee9fbe38` | 0 |
| src/proto/Biz.proto | 1380 | `7e944a240260a3e0b0c8543d224b1dae127efefa5e67e1cd2df1fb130b6db3f8` | 0 |
| src/proto/BizPasskeySession.proto | 1946 | `8774aaf16a8ee4994de18aa4bbb04e4d5943cc0d6fb0de035801d2240e1db31e` | 0 |
| src/proto/Cardano.proto | 7135 | `5d4ff0c87a937f1ce19289b82da5a427d53757a6f1bc6570aac54409acac9556` | 0 |
| src/proto/Common.proto | 2957 | `b2392248c6c90d48df3145ae0eda6f4a81670a090ab1c53639f4eec7b99c0965` | 0 |
| src/proto/Cosmos.proto | 14064 | `0a2f644fda2dc3951e2c43b6ece14ac02263b34072652748760ab086da77d163` | 0 |
| src/proto/Decred.proto | 2252 | `d610081ceb743d37d199d946f652fb0922c372f5090583978f810d3c998004e3` | 0 |
| src/proto/DecredV2.proto | 2132 | `164853ce404179981620365de40c294b4a2b9a26c3db73727510cb41a5b76140` | 0 |
| src/proto/EOS.proto | 1559 | `fe1653a10419a03b7e3e44136a1db3c58d4fcfcc1d3839ce62e9f6b719519df5` | 0 |
| src/proto/Ethereum.proto | 11289 | `e0527b81b749a733283d310381192afbfaac79de37dfcd946896d77ed4f9f863` | 0 |
| src/proto/EthereumAbi.proto | 7874 | `93385e5757e510cf8b14c829755eb05997e6ae896d99c318f434dc942b5fc86e` | 0 |
| src/proto/EthereumRlp.proto | 1120 | `0b6b59a28073610cc169196761e5d100f2c31b5a99507fdb024bfb9112d98a9e` | 0 |
| src/proto/Everscale.proto | 1538 | `a52636629ffe830636252d3386202d58d81529c7db325690c79554c7cc4c9fd6` | 0 |
| src/proto/FIO.proto | 7044 | `99987204936014ee100e23d6e67bdf04c1bcbfea3d8390117c6e301f18b8f48a` | 0 |
| src/proto/Filecoin.proto | 1464 | `2a70c629b0b4037d239df67a8f10f4f688ed8d0abf984950131e7a6424f399ef` | 0 |
| src/proto/Greenfield.proto | 3025 | `9b14f27c6271f61abf0e7eb270b6c75e93450e7eba1073b7f13d0c3208588a46` | 0 |
| src/proto/Harmony.proto | 4161 | `d28f7bd54165c860b9b56a7107c59e0094b7a2fadb1677fac71834a0f4c206a7` | 0 |
| src/proto/Hedera.proto | 4474 | `1f18cfd1212f2079ed29e775273db74103c7f532b0d6fde18f53decc6604d35c` | 0 |
| src/proto/IOST.proto | 2267 | `4f7dc74f5fec400ef019297a9ba036d311fda67fe6a7241b7b511ab408c4a68c` | 0 |
| src/proto/Icon.proto | 1076 | `3900e68d1714148dce07f5d51d6f29034830cc287756cad8864976f0b330f744` | 0 |
| src/proto/InternetComputer.proto | 1067 | `f911c004c6906186d9a883d13bd7fcce249065888432d8fd9df2ef17aeb423a7` | 0 |
| src/proto/IoTeX.proto | 5584 | `0107538d8741681ea81483437eeafc0f57d44d939577cc442ddccf52d2a66418` | 0 |
| src/proto/LiquidStaking.proto | 3143 | `eb363d06f7da035b139baa312442ac3bf33d34083c81ff6643110505d9ccbf87` | 0 |
| src/proto/MultiversX.proto | 3070 | `ffa62f70eaccfa1fb0e40da0308934baad2bd7d24ef3b7a72f9d3a30503aebe5` | 0 |
| src/proto/NEAR.proto | 3334 | `3d7724f2a9444e0947a435763b25c4279f2ce5c6fce9885a026ed23b0ef39d37` | 0 |
| src/proto/NEO.proto | 3395 | `1c5fb4b273cdf3ee485839ece69494ecf5b6c7187670a0b1fd8f55a76ad8a4e1` | 0 |
| src/proto/NULS.proto | 3241 | `8aa666690f2ddedf443613ff11a844dc52519bb819f165470f03c7f235a8ea64` | 0 |
| src/proto/Nano.proto | 1228 | `c79859853d3f4a34e08b4139aa5d8bedf6866a7cf9c8a0384fdc8b845406d9e0` | 0 |
| src/proto/Nebulas.proto | 2142 | `50b6a82fce9373b64a7d3cd62a1e951dbaa5429e8c5678cca7ead0356a66d5c9` | 0 |
| src/proto/Nervos.proto | 4320 | `bf0ef87e38d116cf8f4b3a13cd14dddb935175ad37d494d0a503aa373cf2af92` | 0 |
| src/proto/Nimiq.proto | 1041 | `be9f478cda49a16dc44b6187b4758fcf6ecb08ea1cb8bde93849c57dc2604c58` | 0 |
| src/proto/Oasis.proto | 1736 | `29fb9419580b270194ee7dd58081b5676f964185e91e52a8957ad507e9ebc1b5` | 0 |
| src/proto/Ontology.proto | 1370 | `dc10209a9d6da0197a081da9b24abe6f22b948175220d0eb1c0bff467930c234` | 0 |
| src/proto/Pactus.proto | 1721 | `f523663e2dee57e9c9417e17e6636ae80acb5fa387082c93cec94f3650c4f422` | 0 |
| src/proto/Polkadot.proto | 6960 | `6a4110490f76ad158b6fdf93433e47ddd7a7d98f8e05fdbf0c07a842baa134f8` | 0 |
| src/proto/Polymesh.proto | 8054 | `ddddb898ee6deabaa4783ed0994fe64f40e25319a786976a1062ee5a3938a6e1` | 0 |
| src/proto/Ripple.proto | 4550 | `e93e780d4185ccbf016b8dd816e316f296de9e60cfd5c4de16a205868c68b24c` | 0 |
| src/proto/Solana.proto | 18146 | `083b460f746392e623b01aa070487a36c003032506925f2716876c8d0041d8a4` | 0 |
| src/proto/Stellar.proto | 3279 | `04cedb816782407b285bac3183f16d4844248f2561e75e8e112b2ad16c7efad0` | 0 |
| src/proto/Sui.proto | 5797 | `808269ec34c902eadc43c3472afa020b237c9985466ea717e6e13f66dbb993a3` | 0 |
| src/proto/THORChainSwap.proto | 3818 | `da714fd77aa965d5e504b15b842a40019edf07db86d21e51bd70331782ff4273` | 0 |
| src/proto/Tezos.proto | 2760 | `232252df17f6dcf61d7f7806b9e42d2bcd68d4a1e2898b525aa64ee256484489` | 0 |
| src/proto/TheOpenNetwork.proto | 3529 | `6a62d9ea472346cf15829d67e7ed413d173d096de66dba5f6efd1adecd61c3ca` | 0 |
| src/proto/Theta.proto | 1237 | `f29dcb38ed5141bd8b2acce44f20b01d827e52ac16706045d6e4390af4d2ada6` | 0 |
| src/proto/TransactionCompiler.proto | 483 | `e7da2263f2941d6d4f24a80f8aede9ec4e057e678d58b790b07e956d40e97eb3` | 0 |
| src/proto/Tron.proto | 8160 | `37f8c60b7cc0ea713f17cb110c3a5ad99a9a807dc7624db8fee510fc33cfda57` | 0 |
| src/proto/Utxo.proto | 1418 | `3ccd535813f400a2b9cc9e0a38c91060fc13a16a5b20f624d86e135c34d491ab` | 0 |
| src/proto/VeChain.proto | 1816 | `0b62caa38b1e183bc8d16b4a1c4b9e2246b4dd043583aeaf4c5879d9ecf0bb9e` | 0 |
| src/proto/WalletConnect.proto | 1166 | `2016640bdc7653b18084a1b9ce495fc9b56fd5406b672c0f80bfe482ebde6070` | 0 |
| src/proto/Waves.proto | 1619 | `58d4d5a7eee86f4cddcb718f2d417ec938ab8bdf6903a494fd9d28cc7cffec35` | 0 |
| src/proto/Zcash.proto | 1414 | `82b9076281a73f5d2baec676df6f15a48643da429841d03aeb4d25e375bce047` | 0 |
| src/proto/Zilliqa.proto | 1625 | `05324da8d3f8c542f2cf7d94b36443dc62b1deaed4cdfe231b2aaa78dca3e290` | 0 |
| src/rust/RustCoinEntry.cpp | 6092 | `e5e9182fde247a61d6cd7c08e23f6f1ad19ca79a45b75cb5550dd74621b998cb` | 0 |
| src/rust/RustCoinEntry.h | 2481 | `450a3775719800691b93de8907277fef98b166e7696f795577317dd6beda0d78` | 0 |
| src/rust/Wrapper.h | 6190 | `6fee2dca447f0497f0ff93e3e7fa76f5392eeb2e8136af45333892c3c3b53eb3` | 0 |
| src/uint256.h | 2363 | `6c23ac93527e55aa3cda8161a395f611af9a6330597cbe866c4f2650f86fdd39` | 0 |
| trezor-crypto/crypto/address.c | 3377 | `a473c33bb0c83710a442d7a029264a364f3ea0d3cce8f56ecbc10447a4a7f294` | 0 |
| trezor-crypto/crypto/aes/aes_modes.c | 30925 | `9adeb4a5305d287333b11b3ca8a6dc0cc0a031153718c267f2c46b2d14605c35` | 0 |
| trezor-crypto/crypto/aes/aescrypt.c | 10384 | `6cdbc2a8185330a6f1572423ef60b7f4cd5a08373ed349184731c42bb81b3a67` | 0 |
| trezor-crypto/crypto/aes/aeskey.c | 16160 | `19bd8db1ae31d5716dd347478c2e9f32515bdc8fd9979d4af0c111925881a321` | 0 |
| trezor-crypto/crypto/aes/aestab.c | 15890 | `17d1481c3a141c2bd16ea2b1cc04f780f84961345a70709730d2d8a4f296a2a1` | 0 |
| trezor-crypto/crypto/base32.c | 6227 | `36e592c0b5c09ecdb25f82e4e4ddb11391687b8f3cc470196d8676c423584969` | 0 |
| trezor-crypto/crypto/base58.c | 8469 | `730871edf6387e304bf0bdee75a999809975fb7f350ed32a7dbc0c96a72589e2` | 0 |
| trezor-crypto/crypto/bignum.c | 61925 | `0cdd6765aab4b9ff73a295c807d814a4fb3972982a81ddc2b830dbc186862223` | 0 |
| trezor-crypto/crypto/bip32.c | 25407 | `d3086fd5790d113fc036ef929e8940e1af58503847a1a4b7d50982f583ade651` | 0 |
| trezor-crypto/crypto/bip39.c | 8758 | `bd3900318aec14386da390e030f50e311036ddda8ce764b744fa70676af35e33` | 0 |
| trezor-crypto/crypto/blake256.c | 6546 | `cf9e87cfcac8fc7d6d70b271576d18552cbf4939cd84f8e095836c0ac461eb7f` | 0 |
| trezor-crypto/crypto/blake2b.c | 9901 | `d0986ad731996072d5f84c94168eee083fc3c3fe2a43845a4abe495214966c04` | 0 |
| trezor-crypto/crypto/blake2s.c | 9210 | `ee281cc32bf9a0c53d1baf002f7842421794f15fe00bcc9aae004c1f24a43d86` | 0 |
| trezor-crypto/crypto/cardano.c | 10227 | `e87dc3b9b33ffdfca2b5f80950e18775f84f9242d9000434d1a7d5ab307e43bd` | 0 |
| trezor-crypto/crypto/cash_addr.c | 6764 | `f7f0ddec0d153172c28e3d5c9c473ff6a03264ba09d258f209b32328125a1744` | 0 |
| trezor-crypto/crypto/chacha20poly1305/chacha20poly1305.c | 2565 | `d1dc36dad4d0dc41b4302e0b723d2788bd00438e51ee5c58c159948665a32708` | 0 |
| trezor-crypto/crypto/chacha20poly1305/chacha_merged.c | 6611 | `73f396e4cdca110b2f86202bee3d953a3ff67e28ba629fbf4084cca282778b33` | 0 |
| trezor-crypto/crypto/chacha20poly1305/poly1305-donna.c | 5192 | `dce73413b7d71acbd3f33cf75007ce88c7476fe7304792d6fdc837e963cd91de` | 0 |
| trezor-crypto/crypto/chacha20poly1305/rfc7539.c | 1830 | `cc93857dac0e332fbda7438a8e1af96b5f7d83dd1dbecbde370ecc218feba252` | 0 |
| trezor-crypto/crypto/chacha_drbg.c | 4576 | `782e8792984afcf2bf306eec37de89efe8e0085b36b18b9469d2c5a8b12f8f2a` | 0 |
| trezor-crypto/crypto/curves.c | 1870 | `054eeeb872d1a4eac3e0fc40dbc249fd9af097f0bb86aefe72e8bb8a9ecf01ec` | 0 |
| trezor-crypto/crypto/ecdsa.c | 36867 | `2a3de289c028fcd6fe7f58036652786a48156e0831b01ef3bae6d111664562a8` | 0 |
| trezor-crypto/crypto/ed25519-donna/curve25519-donna-32bit.c | 26940 | `a29255666da0c616b20d910670ea0aed7b5dbe74481f21a0d70ee1e8f4602883` | 0 |
| trezor-crypto/crypto/ed25519-donna/curve25519-donna-helpers.c | 2408 | `231a48697950ed965ce66fb5010dbf6af6dd2c9a1b6cbfd82fb9a06bee1f153d` | 0 |
| trezor-crypto/crypto/ed25519-donna/curve25519-donna-scalarmult-base.c | 2241 | `48ad7c177150104afe346e196229589253c24687ebb162236d83e03620a2fbf7` | 0 |
| trezor-crypto/crypto/ed25519-donna/ed25519-blake2b.c | 200 | `6986254701da5eb69fecd77e8eb80da464aa19afd3ae2cfb07a365c79ed8062d` | 0 |
| trezor-crypto/crypto/ed25519-donna/ed25519-donna-32bit-tables.c | 12022 | `99d4efe8b2ca369f2c7680a47b3076d661007f6e8d6031b8d9fa3e83ce961774` | 0 |
| trezor-crypto/crypto/ed25519-donna/ed25519-donna-basepoint-table.c | 124096 | `eef7a3fb828209233dcfcd0f7c4163021df7c3e2b1e2eb0d7a9f78e7078ad1cd` | 0 |
| trezor-crypto/crypto/ed25519-donna/ed25519-donna-impl-base.c | 21931 | `e5585bbc23c86499ca5bfa93a9ef3996293de88835b9dc82f69bfdb128074cb3` | 0 |
| trezor-crypto/crypto/ed25519-donna/ed25519-keccak.c | 197 | `b139deaacb9c11775b66443258fa6eea5be93ecca40eda033df9d6370ff56cae` | 0 |
| trezor-crypto/crypto/ed25519-donna/ed25519-sha3.c | 191 | `ab364c9b78306aeef462c821db1eaade1300cf11d288124ba881626f29e47921` | 0 |
| trezor-crypto/crypto/ed25519-donna/ed25519.c | 7660 | `35855684b64fdfc5847723d1541293dbe0411719b0bc0d9397edd514f526a2e7` | 0 |
| trezor-crypto/crypto/ed25519-donna/modm-donna-32bit.c | 23074 | `696529b66740c3c17368d490b6ebe20a97b9296740fdd6fcdd12109ef920582b` | 0 |
| trezor-crypto/crypto/groestl.c | 34054 | `9bfae457f05a241478930323aad9758c34b82d70bed089a92c8bd566cab76041` | 0 |
| trezor-crypto/crypto/hasher.c | 4632 | `e981abc16e258dfee2a789ecc6cabeb6f05af50b2aa794481ded59c14c9479ee` | 0 |
| trezor-crypto/crypto/hmac.c | 6386 | `97ddd64b6100a34d7c380b31c964d671916752d19d958b150173bcfc35cc00b8` | 0 |
| trezor-crypto/crypto/hmac_drbg.c | 4747 | `d8e842ea3e9203633a19dad1979c03e5d9fc4226128b54b58f3bdbef276bc9e4` | 0 |
| trezor-crypto/crypto/memzero.c | 1886 | `1d5534da0a5686f84d867bfb11ae750a5396ffb615f12381b7cd22c25e8104ac` | 0 |
| trezor-crypto/crypto/monero/base58.c | 7455 | `7a92d4eed522ebc7d99a756468cc4092bb57eed60ab26593b3047d35824d8f4f` | 0 |
| trezor-crypto/crypto/monero/base58.h | 2202 | `02366a0ff2110b11b8447cd2a486fc70651d57316e279ca693f6404ca7cdb51a` | 0 |
| trezor-crypto/crypto/monero/int-util.h | 3153 | `d9991aea12fa61d3bdc939e63e7c57c0a6520bec380bd1a95705f46ae28edbfc` | 0 |
| trezor-crypto/crypto/monero/monero.h | 367 | `8caaec1bb7963b82c99652c8944a6a77e7820c9dc39a892ac45d5af58923303f` | 0 |
| trezor-crypto/crypto/monero/range_proof.c | 3249 | `2ea355976d592f782d0be061472cee4361d553978f8edfc4cd53ee3946c88715` | 0 |
| trezor-crypto/crypto/monero/range_proof.h | 826 | `38337b07b112e9c0ee7ddd66c416cca1f99486c55fe0be4c12182530138a1541` | 0 |
| trezor-crypto/crypto/monero/serialize.c | 1071 | `31aab284f1c3c4cee2920beda7b065b6fa758d878122feb78135699f2cc1bc30` | 0 |
| trezor-crypto/crypto/monero/serialize.h | 361 | `f2a4135173f708918ed8bf802d8fbb2e10c6b3548cfe18d11d705925027350f5` | 0 |
| trezor-crypto/crypto/monero/xmr.c | 4708 | `84289f5a015163f96fcce4393496ee4ee0c6ef4adcbf16fd5677c619a6bfffa4` | 0 |
| trezor-crypto/crypto/monero/xmr.h | 2551 | `8cf6ea0a386017e7a163b4b2ec057c64c9344a49e671c7a0d3b0174f642cbd6a` | 0 |
| trezor-crypto/crypto/nano.c | 4773 | `05a86780742aa1d7fa27252754f7526e6a85e22a9ea6a387e342292661160499` | 0 |
| trezor-crypto/crypto/nem.c | 17485 | `6a69e7b46a2d52e44dcd96425daae3685b35a9e5ec76535ec8d48c5f35a2f1d3` | 0 |
| trezor-crypto/crypto/nist256p1.c | 2638 | `a00a4118335430cfdb9e30f860b69097527ec652c8b8d6c39d4e3c446e86310d` | 0 |
| trezor-crypto/crypto/pbkdf2.c | 6814 | `3cc55736b36a4ebee9be551504f22e196c426a98c919884f70dcda2c13724755` | 0 |
| trezor-crypto/crypto/rand.c | 2151 | `cf432ca318af6d9896eb1ba96db11c7e5de13088c156a4c4aedb6ae4495d5875` | 0 |
| trezor-crypto/crypto/rc4.c | 1857 | `fc3ccc0e09440eaa5ee2c9447b81b244b3168dc2dcf5b6644858e6d319455486` | 0 |
| trezor-crypto/crypto/rfc6979.c | 2416 | `72cfc46127d392a559eb372b63405d5a70b3e3c32c6466f364402ee7c9273e97` | 0 |
| trezor-crypto/crypto/ripemd160.c | 10314 | `8fce455a559928ccb69d1d6c9de700bce32bfa036217e7ac209bc7e255ad2110` | 0 |
| trezor-crypto/crypto/script.c | 2401 | `2891beb249908a8b5e9c5ec68d292c07296d10d5594f026b60367c0c84d34b2d` | 0 |
| trezor-crypto/crypto/scrypt.c | 9096 | `7e427a630604536117f69fc7f06ee57e744f8cbb2132ecc40bcd5bc4bf3d024e` | 0 |
| trezor-crypto/crypto/secp256k1.c | 3270 | `2ab0a901298dce1984bf8352002462174cae4aeb19fd1c67dd13b25ebb631fa6` | 0 |
| trezor-crypto/crypto/setup.py | 828 | `7d35389b6dd2553ff3f32e2c567d4c79fb86f59d058377a96a8854a054c91d59` | 0 |
| trezor-crypto/crypto/sha2.c | 39400 | `49d1c1efd653f6434a4ea64972a24711abea227d9766e633f13403a2b1a6ee53` | 0 |
| trezor-crypto/crypto/sha3.c | 11058 | `27100b4a56ac7afbb9e54236797dc67b04bcda04f4a6f5072f4c44d4734b8189` | 0 |
| trezor-crypto/crypto/shamir.c | 9963 | `b63ef0d055174301a7f5c458bcbcdf7c257b257c7b6d6179dd2c0936e2805877` | 0 |
| trezor-crypto/crypto/slip39.c | 4164 | `2f0fa9786033b408ccbada0598f5c63f3992f67eca11ac313b7983c010daefed` | 0 |
| trezor-crypto/crypto/sodium/keypair.c | 1867 | `6c4af6b74a8afed210f2b031b4a53e04c05fd06333be867cfd6a99ae7678b210` | 0 |
| trezor-crypto/crypto/sodium/private/ed25519_ref10.c | 13796 | `3bb936d5c7997eb80302e02f8a2d6064c12f9f1b2b786259207e90128229768c` | 0 |
| trezor-crypto/crypto/sodium/private/ed25519_ref10_fe_25_5.c | 26174 | `9052e607bb3016a8557cd6a762244bfcf5f848f45adb0cd028ead9e0a8c01ca1` | 0 |
| trezor-crypto/crypto/sodium/private/fe_25_5/fe.c | 6212 | `1cdba47a600041d9f52e05851bfcd0fca98fb97c9846199ce259a86fa0ad054a` | 0 |
| trezor-crypto/crypto/tools/bip39bruteforce.c | 2722 | `a6c9ec3573b2fe2c84717f5a6fb496e006013f3ecc35d940de77b2d030d2ef1c` | 0 |
| trezor-crypto/crypto/tools/mktable.c | 1894 | `54c8ce2618f82a552ce767b5f6bf3ab609f8e31b8ef1ed59441d8dfa2a05f9c0` | 0 |
| trezor-crypto/crypto/tools/nem_test_vectors.rb | 2644 | `99184a81184c8f4e522bbc5edf3d9fb25a83e4a8e7f2e193476b36e568f9c1d0` | 0 |
| trezor-crypto/crypto/tools/xpubaddrgen.c | 1290 | `7f5354bb6605cad3e42a8c649750025e33eba26140949bc8c08d518b4241c549` | 0 |
| trezor-crypto/crypto/zilliqa.c | 5868 | `e6ed95be380f99948f18f62cd03c6afc7b256023a3f400a31a792da19b303188` | 0 |
| trezor-crypto/include/TrezorCrypto/TrezorCrypto.h | 878 | `99aa538c1910ce7ec818bc3d0015c9421b11a791b38ce9695965db09f306da09` | 0 |
| trezor-crypto/include/TrezorCrypto/address.h | 1743 | `cb36f6876e066644a6fb62770ebfff9a68372faa7e0c2a24691351badb72cb51` | 0 |
| trezor-crypto/include/TrezorCrypto/aes/aesopt.h | 27855 | `d8ae0ede0c172b2c08af3fb92ab246ee744068d8da4b860d858c3aae086d8b06` | 0 |
| trezor-crypto/include/TrezorCrypto/aes/aestab.h | 5162 | `54a0b84dfb358c0b1577f777c85cf9d90abea3c6f4ec5d587b7d230f123154d5` | 0 |
| trezor-crypto/include/TrezorCrypto/aes.h | 7998 | `39fac3fa0a70c65c5c5b837ce6ff7476b055538afb8b862c7562a6d3d52764af` | 0 |
| trezor-crypto/include/TrezorCrypto/base32.h | 1901 | `2957e4a01ba1fb4a038f2097cc923a8b48e6459ade3b76865a981e74913e1394` | 0 |
| trezor-crypto/include/TrezorCrypto/base58.h | 2264 | `8b38ac1a2f8c2532852f3ca3adc189f53db487cd74f41ecba2e25d454211b63f` | 0 |
| trezor-crypto/include/TrezorCrypto/bignum.h | 6941 | `9521b1a0eb106c646648345bb7e749dac2c573aa01687097080ce24ebe46a1ff` | 0 |
| trezor-crypto/include/TrezorCrypto/bip32.h | 6068 | `d9b6c80ad6c89a91cf4c47d9ebfa324f64853765d37c9c8cc7d57d843226de4a` | 0 |
| trezor-crypto/include/TrezorCrypto/bip39.h | 2464 | `890159ffa7a3aa6bc428728cc15c090e57db00bc6a96bc3a9658f8b15c92233a` | 0 |
| trezor-crypto/include/TrezorCrypto/bip39_english.h | 26250 | `a360e08b684ef0a6e3de4929f2edcf6d036d9e4299bcf37bc4247e6c5d24b353` | 0 |
| trezor-crypto/include/TrezorCrypto/blake256.h | 2263 | `2271f04c0e4ea010f6d787d77477f672365c934f3292c1b9f02ddbdeba1296e5` | 0 |
| trezor-crypto/include/TrezorCrypto/blake2_common.h | 675 | `226587236acd714b8901c1f000adbfe6ab491eb414eef00ad5fc27dfe213a635` | 0 |
| trezor-crypto/include/TrezorCrypto/blake2b.h | 1481 | `e317ee2389625075efdfcae31068d46ba240d840d0807f91a7f8a858d283891a` | 0 |
| trezor-crypto/include/TrezorCrypto/blake2s.h | 1308 | `bfdd8c653b4bef47b66c0fcb10cd1abaca3948e315a466f4bae558cb31d9c751` | 0 |
| trezor-crypto/include/TrezorCrypto/cardano.h | 2275 | `e565147f9e767f32f1cf9a0a3abbf15619199c33646fbef58aa7c4d68402af75` | 0 |
| trezor-crypto/include/TrezorCrypto/cash_addr.h | 3748 | `becbae036070ba5e27db0fd27c432878d859ff0143e8b3f566480d756f47cbaf` | 0 |
| trezor-crypto/include/TrezorCrypto/chacha20poly1305/chacha20poly1305.h | 787 | `a3e82ff4817b4e960740c96182b5c5696df898bc373bdf328ad2afe44954277a` | 0 |
| trezor-crypto/include/TrezorCrypto/chacha20poly1305/ecrypt-config.h | 5804 | `7ed8cab12d40e1f86fe2511d0c3c0332594bbb56eea0e9592e7d9c825c1876a9` | 0 |
| trezor-crypto/include/TrezorCrypto/chacha20poly1305/ecrypt-machine.h | 1182 | `70dd1a45d677c3cfa62955fd1d3e125a31002f44f550e85a25364ae6cac159b9` | 0 |
| trezor-crypto/include/TrezorCrypto/chacha20poly1305/ecrypt-portable.h | 6780 | `8a1f73bb364d19382983d2bc1a8ca568c4a5f7cc9dafa696ace5ebe954dbbcce` | 0 |
| trezor-crypto/include/TrezorCrypto/chacha20poly1305/ecrypt-sync.h | 7851 | `2684a9c88e80749f88e94caea40b8ba57ddea17c5cfc06dc6c479d48d2b15c0f` | 0 |
| trezor-crypto/include/TrezorCrypto/chacha20poly1305/ecrypt-types.h | 1175 | `7d0b98aad7734e79ad1a897d7c568d60547ece3d3f03e639fc274e8c9bcc1639` | 0 |
| trezor-crypto/include/TrezorCrypto/chacha20poly1305/poly1305-donna-32.h | 6515 | `85bc63c1a468fe31a896c242be1cb7afe0cc9a262e5042911abc2cc5dbd1bcb6` | 0 |
| trezor-crypto/include/TrezorCrypto/chacha20poly1305/poly1305-donna.h | 658 | `db2194945f4aeb914e13efee982d365cd32cc16009febb6f68b51b6aaf17514e` | 0 |
| trezor-crypto/include/TrezorCrypto/chacha20poly1305/rfc7539.h | 381 | `62118527120d554d8bdff62575650f402a296fcd4294503d51817b2f79b7213e` | 0 |
| trezor-crypto/include/TrezorCrypto/chacha_drbg.h | 2344 | `741f0e90c79f25454ced81af887b47af4021534531166ce59b4b564e0b28514b` | 0 |
| trezor-crypto/include/TrezorCrypto/check_mem.h | 1092 | `023c6cd6d69941985f6c3058810fceb4b36367930e381bd7d17b5e84b680283d` | 0 |
| trezor-crypto/include/TrezorCrypto/curves.h | 1814 | `7872ceaaa172965980289a6660b83b92ce9544224722965b350f78e3cac8e8c9` | 0 |
| trezor-crypto/include/TrezorCrypto/ecdsa.h | 6305 | `d3cfc9df6649c541e1d33b50305e4e5f48977badd68bb015f798b580bf4ab4a2` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/curve25519-donna-32bit.h | 2727 | `02ffafcb224974385ac9a3a2633a412656cd3f0a7a54b72d59b0bb489929bd83` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/curve25519-donna-helpers.h | 565 | `59d05f92ce256c3a80e7e413ffc07589d85e7adf3f4c8a2a313ab4df84557a15` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/curve25519-donna-scalarmult-base.h | 372 | `6b09a09393ce4a4d6cb0fde19db63785b5097d6521c6375fc664c3be8a5c6984` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/ed25519-blake2b.h | 638 | `767b0480445133853bff8720f4086d717bc81765efaeba7f8cf167ecb46cd6e0` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/ed25519-donna-32bit-tables.h | 391 | `2ce588764e1e6e5cac2a8d34922f0055544c60f9819195005ba60a4c15a874e6` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/ed25519-donna-basepoint-table.h | 225 | `02d37cc9f8f96035139ce92e8cced95ab76ad9ac7089c4d064bfa64178289b56` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/ed25519-donna-impl-base.h | 3029 | `3fb67f8a42c938d64be6d6aafd497d9e4680dd004f2606e7fb7fbb9806eb49d7` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/ed25519-donna-portable.h | 666 | `687f07886b276d3cf86d170fd03f1b47d1d5f43b9ee5ebe90abe86e26cebb4e5` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/ed25519-donna.h | 1493 | `106b5df7e3352a7b9ab0e163fbfbf7b1e368aa404eae3b9c7a2868e03ad03354` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/ed25519-hash-custom-blake2b.h | 824 | `7d845fa97a898ba01076c9b739eb9aab8c5fb2dc5520da9a750bc9484da93404` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/ed25519-hash-custom-keccak.h | 798 | `abb4b77f87101b5529531fd853e6f5aa7daff8d34ffbf2dc6a802549753030dd` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/ed25519-hash-custom-sha3.h | 790 | `250af4d831aa18aad6a217e82eb6fb86f84da39af9b0ddd8314941199847bd1d` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/ed25519-hash-custom.h | 796 | `05fff7ecab569a93f3a1ed6054319a0000bf560b495da7ca460351793a6fb557` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/ed25519-keccak.h | 631 | `d8c19b3cdf47bff102c30cbb42f6ca4cc2da4239b1a248311c7471b14a0e27d3` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/ed25519-sha3.h | 617 | `2ea505ebb9af50e1c04d83aedb0ef21fbb0ff48ab5a8659e348bb22059391722` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519-donna/modm-donna-32bit.h | 2788 | `85831826b0ce14642ab1d668ba32cc6fb3d130c96e0d5eef0577f3745df9f9cb` | 0 |
| trezor-crypto/include/TrezorCrypto/ed25519.h | 1780 | `68ca8e3df0ea2622e903a9e786cccebe56584a65f65f84d691e4dd87eb866bc6` | 0 |
| trezor-crypto/include/TrezorCrypto/endian.h | 3619 | `4e43b6f152a448d3d0ce7ad4084ad714fd2c4cdf481bc0912a75560eb7439805` | 0 |
| trezor-crypto/include/TrezorCrypto/groestl.h | 3520 | `720be4c30f81dad3cb96bc2e85c86bb156db77bd74ca564edcb01a158193b837` | 0 |
| trezor-crypto/include/TrezorCrypto/groestl_internal.h | 14878 | `a9f30253028a90b290d1a5273b24decc6a4318500808b07854448af10fb556b0` | 0 |
| trezor-crypto/include/TrezorCrypto/hasher.h | 2538 | `acd0f2ba428282193ff4f814b81f011b79524f1d44ae92c7da38ea47ea1d5367` | 0 |
| trezor-crypto/include/TrezorCrypto/hmac.h | 2714 | `c01a3d1619c320ab9effd01f2b4d8b6ec2fd787f1f83674dc1443b58b577a467` | 0 |
| trezor-crypto/include/TrezorCrypto/hmac_drbg.h | 1856 | `e0a98a2028fb86bc994ca097bbd6984d8a42f51f77f79261bdb3a2fad3a26892` | 0 |
| trezor-crypto/include/TrezorCrypto/memzero.h | 209 | `ba27fd063030d194d2d20212a86179740a67cdd718b688e7a98ae2c08445cbcd` | 0 |
| trezor-crypto/include/TrezorCrypto/monero/xmr.h | 2329 | `44c1849f91f9388a98b66c14ed5555882fabc8c4dee30da1bf62ebf42b35235a` | 0 |
| trezor-crypto/include/TrezorCrypto/nano.h | 1722 | `a235cefd69079f87bc4bd59c62e61d1f1cf9e674041d36c51ef33cd181a1a574` | 0 |
| trezor-crypto/include/TrezorCrypto/nem.h | 6950 | `506eea429ade61b6db3d6292e451d6c233d0b8f302be560e3a9cdae787c6174d` | 0 |
| trezor-crypto/include/TrezorCrypto/nist256p1.h | 1360 | `1a8be02d270c3267eb5dc07465d305105c50c06498b19e7cd7a90b38e4776f67` | 0 |
| trezor-crypto/include/TrezorCrypto/options.h | 2739 | `999ccc1f4e5267ece7fe369c70353bd6729b73a06c7643411e146194c2fa0ad4` | 0 |
| trezor-crypto/include/TrezorCrypto/pbkdf2.h | 3133 | `f91b7dc1c902c01d0a4ed0c5a63a9186cc8f898fc82fd514a29427688b23a637` | 0 |
| trezor-crypto/include/TrezorCrypto/rand.h | 1498 | `f62b32bdc6e2a2562a4e8eac6f2c373e37a74e4c468b648e378bdfb94fb9f2d8` | 0 |
| trezor-crypto/include/TrezorCrypto/rc4.h | 1397 | `183634a8819215c6f1c0828ae37d91cb4672b0689c3bd6436a6b8b4168a099e6` | 0 |
| trezor-crypto/include/TrezorCrypto/rfc6979.h | 1680 | `876cd568de73effbfdf8b33b441d9fa4ea38456a4dd42b6312e44aca56a70c15` | 0 |
| trezor-crypto/include/TrezorCrypto/ripemd160.h | 848 | `99cc621a82df1b1bedcb5bf7c51f49a73b07557e39744d51274d3e71a011a261` | 0 |
| trezor-crypto/include/TrezorCrypto/script.h | 1314 | `ca110b2927e37ad9970e8a5a5a769ad9972c0fd5f4ca6399092e5e18c631c10d` | 0 |
| trezor-crypto/include/TrezorCrypto/scrypt.h | 2548 | `1dc71a0741faf70a6c23b2c3168fdae32c45bf902e4e1ca0880d794008f1a22c` | 0 |
| trezor-crypto/include/TrezorCrypto/secp256k1.h | 1587 | `28a18b33c1fdad59fc46f727d85561ce4837d447bfab896f0aa807c59238bc8b` | 0 |
| trezor-crypto/include/TrezorCrypto/sha2.h | 4873 | `fb8860a26db3b7447df9f4ec02cf0c3989563dfb679c3e45bb4d3df6b67ba88a` | 0 |
| trezor-crypto/include/TrezorCrypto/sha3.h | 2994 | `583558d0423d8f65c83dd5f2195e8eb8833b83212a5665d7f6b28cbe446a149b` | 0 |
| trezor-crypto/include/TrezorCrypto/shamir.h | 3246 | `8d8a1286ab5cd315e0210862c2a61c354854c81ec412908b265d3a4e8f0a190c` | 0 |
| trezor-crypto/include/TrezorCrypto/slip39.h | 1581 | `364ad4b4f9e4f7e76bf693859150ba11dfe73375253385aaf7d8caa54d13c722` | 0 |
| trezor-crypto/include/TrezorCrypto/slip39_wordlist.h | 44174 | `4ef5a0ce5b616ecf50e64ea8fae3d623704d46b3dbd5a03cd3aec51566009e92` | 0 |
| trezor-crypto/include/TrezorCrypto/sodium/keypair.h | 382 | `d1737d226a7cd2e5d70b085fc2f1527b791f0c5d03a3f8566625ff6aedd4d76c` | 0 |
| trezor-crypto/include/TrezorCrypto/sodium/private/ed25519_ref10.h | 1829 | `b6ceccb03053e0e7b2e403461fdccd28278327dfcd780a15c313bfdad7c12ccc` | 0 |
| trezor-crypto/include/TrezorCrypto/sodium/private/ed25519_ref10_fe_25_5.h | 906 | `d7b65fad745b5d7dfa11d5e330fb289e100c1d831af151b340a3eeed9463fa47` | 0 |
| trezor-crypto/include/TrezorCrypto/sodium/private/fe_25_5/constants.h | 883 | `c3fb4cfc5e49b7c3af195c1e0011bdbcb29bad063f49d761d5903c340cdac87f` | 0 |
| trezor-crypto/include/TrezorCrypto/sodium/private/fe_25_5/fe.h | 363 | `5e66af42805b19b058141dcc24375c6568295bc1c0ec8c33e257d4db1bf47e9c` | 0 |
| trezor-crypto/include/TrezorCrypto/zilliqa.h | 2187 | `53adde566c60c6c35e59becc8955464a91a73e1ded6584f8d6ce42faa3d7fa01` | 0 |
