# Hard-coded secrets: the detector's precision, measured / Точность детектора секретов, измеренная

Двуязычный документ: русская версия ниже английской. / Bilingual: the Russian version follows the English one.

Date: 2026-10-27 · Engine: 1.2.0 · Rule: `CODE-HARDCODED-SECRET` (severity `high`)

---

## EN

### Why this was looked at

One untriaged `CODE-HARDCODED-SECRET` in the re-audited `agave` blocked citing agave's figures. Checking that one
finding against the real source turned it into a class.

### What the eleven findings actually were

Every one of the portfolio's eleven `CODE-HARDCODED-SECRET` evidence rows was fetched from its repository **at the
commit the report names** and verified byte for byte against the `source_sha256` the report recorded, so this is a
reading of the audited bytes and not of today's code. All nine distinct files matched.

| Audit | Path | What the value is | The evidence in the file itself |
|---|---|---|---|
| agave | `docs/docusaurus.config.js:106` | Algolia DocSearch search-only key | `// This API key is "search-only" and safe to be published` |
| noir | `docs/docusaurus.config.ts:173` | Algolia DocSearch search-only key | `// Public API key: it is safe to commit it` |
| metamask-extension | `app/scripts/constants/on-ramp.ts:1–3` | Transak / MoonPay / Coinbase Pay publishable keys | `// It's a public key, which will be included in a URL for Transak.`, `// Publishable key.` ×2, and MoonPay's documented `pk_live_` prefix |
| ethers-js | `provider-ankr.ts:40` and two build copies | Ankr's shared community RPC key | bound to `defaultApiKey`, beside `showThrottleMessage` and `CommunityResourcable` |
| nitro | `util/signature/simple_hmac.go:77` | a test fixture | declared as `TestSimpleHmacConfig`, next to `EmptySimpleHmacConfig` |
| rabby | `src/utils/ga4.ts:10` | GA4 Measurement Protocol `api_secret` | **genuine** |
| signal-desktop | `ts/state/smart/fun/giphy.preload.ts:22` | Giphy client API key | **genuine** |

**Nine of eleven high-severity findings were false.** An Algolia search-only key is served to every browser that
loads the documentation; it can query one index and cannot write, delete, or read account data. A publishable
payment key is designed to sit in a URL. A `Test…` fixture is test data in a file that is not test code.

The two genuine ones are genuine but **not high**: neither grants access to funds or to user data. The GA4 secret
allows injecting events into Rabby's analytics property; the Giphy key allows spending Signal's quota. The test
suite had already decided these two deliberately, on the stated ground that *whether a third-party key's exposure
is intended is a human decision, not something the detector may assume* — a decision this review reached
independently and did not disturb.

### What was changed

Three guards, each taken from the measurement rather than from a guess, in
`app/services/audit/analyzers/source_code.py`:

1. **The project's own annotation counts.** The existing guard read only the *identifier*
   (`COOKBOOK_PUBLIC_API_KEY`), so a decision recorded in a comment was invisible. A trailing comment, or one on
   the line above, that applies publication to the value — `publishable`, `search-only`, `public API key`, `safe to
   commit`, `not a secret` — is that human decision, written down by the people who made it. A bare "public"
   disclaims nothing: it is a Java modifier and a word about interfaces.
2. **A fixture can live in a production file.** The old guard was path-based, so `TestSimpleHmacConfig` in
   `util/signature/simple_hmac.go` was out of its reach. The declaration the value sits inside is scanned upward to
   the nearest line indented less than its own, and its name is what decides. Anchored at the start and followed by
   a case boundary, so `latest`, `attestation` and `contest` are not fixtures.
3. **`hex_private_key_32b` is a shape, not a thing.** It means "64 hex characters", and that cannot tell a private
   key from any other 32-byte credential. ethers.js binds exactly that shape to `defaultApiKey`, so a client's
   report said *private key* about a vendor's published RPC key — a factual error, and a report that misnames one
   finding is disbelieved on the rest. A re-labelling guard was written for this and then **deleted**: the recall
   fix below turned out to solve it one layer earlier and better. Once `defaultApiKey` is read the way
   `default_api_key` always was, the value is an assignment to an API key and never claims to be a key at all.
   Measured before removing it, name by name: every name the guard could have re-labelled now either goes through
   `generic_assignment` or produces no finding, so it was unreachable code — worse to keep, with a test asserting
   behaviour the pipeline can no longer produce, than to have neither.

And one limit put on the first guard, because of what this product audits. In wallet and node code, the public
half of a keypair is an ordinary thing to write in a comment directly above the private half:

```rust
// public key: 0x04ab…
const PRIVATE_KEY: &str = "…";
```

Read naively, that comment would have silenced the gravest finding the tool can make, through a habit of exactly
the authors it audits. **An identifier that says private outranks any comment** — `privateKey`, `secret`, `seed`,
`mnemonic`, `signingKey`, `masterKey`, `xprv`, `wif`. The api-key and token terms are deliberately *not* in that
list, since clearing those is what the guard is for.

### A prior decision reversed, on purpose and in the open

A reading of these same findings on 2026-10-23 reached the opposite conclusion and wrote it down: *"A comment is
not evidence, so these stay findings and a human records `accepted_risk`."* Four of today's cases were named there
by hand. That decision protected something real — `accepted_risk` keeps the row inside the report's counts, with a
person's judgement attached, instead of letting the detector decide alone.

What changes it is not a better argument but the month that followed: the triage it depends on happened for none of
them, while nine false high-severity findings stood in the portfolio, and one of them was the item that blocked
citing agave's figures at all. A rule whose output is 82% false, at `high`, is not a question for an analyst's
queue; it is a precision defect.

So both halves are kept. The finding is suppressed, and the reason is written into the report's coverage section
**against the line it was taken on**, quoting the class of annotation that disclaimed it — `publishable`,
`search-only`, `safe to commit` — or naming the fixture declaration the value sits in. The client is not shown
their own documented decision as a critical issue, and the decision is still in the report to be disagreed with.
Pinned by a test, on the same principle as the trust-store rule: the decision has to be stated, not silent.

### Measured result

Run over the same verified bytes, so before and after differ only by the analyzer:

| Audit | Before | After | Why |
|---|---|---|---|
| agave | 1 | **0** | annotated published |
| noir | 1 | **0** | annotated published |
| metamask-extension | 3 | **0** | annotated published ×3 |
| nitro | 1 | **0** | fixture declaration |
| ethers-js | 1 (×3 copies) | 1 (×3) | kept, no longer called a private key |
| rabby | 1 | 1 | genuine, deliberately kept |
| signal-desktop | 1 | 1 | genuine, deliberately kept |
| **Total rows** | **11** | **5** | and 3 of the 5 no longer called private keys |

`agave` therefore goes from 16 high-severity findings to 15; noir, metamask-extension and nitro each lose one high.

### Two defects found by writing the tests

**A guard that was never tested.** `_PUBLIC_NAME`'s "publishable" branch was pinned by the case
`const publishableKey = 'pk_live_…'` — which redaction never flags, so the case passed because nothing was ever a
candidate, not because the guard worked. Two of the file's cases were vacuous this way. The test file now separates
`ANALYZER_QUIET`, where each case must be shown to reach the analyzer with something to suppress, from `QUIET`,
where going unredacted is itself the mechanism.

**My own guard was wrong, and my own test caught it.** `// https://stripe.com/docs/publishable-key` is a link to a
page about publishable keys, not a statement about the value beside it — and it silenced a real secret. A URL
inside a comment is now stripped before the phrase is looked for.

### A recall gap found on the way, and fixed

While measuring, `apiSecret` turned out not to be redacted at all while `API_SECRET` was. The name pattern accepted
a prefix separated by punctuation (`client_secret`, `DB_PASSWORD`, `aws_secret_access_key`) but not one separated
by case — and camelCase is the usual spelling in JavaScript, TypeScript, Java and Go. So `clientSecret`,
`authToken`, `dbPassword` and `apiSecret` were never redacted and therefore could never be reported: not a wrong
answer but no answer, which reads in a report as a clean result. This is the failure this product treats as the
worst kind, so it was fixed rather than filed.

The second alternative is deliberately **case-sensitive**: a camelCase prefix counts only when the keyword begins
with a capital, so `notsecret`, `mytoken` and `subtoken` remain names. The suffix rule is untouched — `token_type`
and `secretName` name something about a credential rather than holding one. The prefix is bounded to 40 characters
so the scan stays linear, and two adversarial inputs for the new branch were added to the existing linear-time test.

### Checks

`scripts/dev/lint.sh` clean (ruff, mypy, import-linter: 4 contracts kept, 191 files). The labelled corpus,
end-to-end audit and analyzer-complexity tests pass (223), and the secret guards pass in both directions (33).

### Deliberately not done

- **ethers.js reports the same key three times**, from `src.ts/`, `lib.commonjs/` and `lib.esm/` — the source and
  two committed build outputs. Suppressing build directories would also hide a secret introduced at build time,
  which is worth knowing, so this needs its own measurement rather than a guess.
- **The two genuine findings were left at `high`.** Lowering them is a severity-model change that should be argued
  on the model, not slipped in beside a precision fix.

---

## RU

### Зачем это понадобилось

Один непротриажированный `CODE-HARDCODED-SECRET` в переаудированном `agave` мешал приводить цифры agave. Проверка
этой одной находки по живому исходнику превратила её в целый класс.

### Чем эти одиннадцать находок были на самом деле

Каждая из одиннадцати строк-доказательств `CODE-HARDCODED-SECRET` по всему портфелю была загружена из своего
репозитория **на том коммите, который называет отчёт**, и сверена байт в байт с записанным в отчёте
`source_sha256`. То есть это чтение аудированных байтов, а не сегодняшнего кода. Все девять файлов совпали.

| Аудит | Путь | Что это за значение | Доказательство в самом файле |
|---|---|---|---|
| agave | `docs/docusaurus.config.js:106` | search-only ключ Algolia DocSearch | `// This API key is "search-only" and safe to be published` |
| noir | `docs/docusaurus.config.ts:173` | search-only ключ Algolia DocSearch | `// Public API key: it is safe to commit it` |
| metamask-extension | `app/scripts/constants/on-ramp.ts:1–3` | publishable-ключи Transak / MoonPay / Coinbase Pay | `// It's a public key, which will be included in a URL for Transak.`, дважды `// Publishable key.`, и документированный префикс MoonPay `pk_live_` |
| ethers-js | `provider-ankr.ts:40` и две сборочные копии | общий community-RPC ключ Ankr | привязан к `defaultApiKey`, рядом `showThrottleMessage` и `CommunityResourcable` |
| nitro | `util/signature/simple_hmac.go:77` | тестовая фикстура | объявлена как `TestSimpleHmacConfig`, рядом с `EmptySimpleHmacConfig` |
| rabby | `src/utils/ga4.ts:10` | `api_secret` GA4 Measurement Protocol | **настоящая** |
| signal-desktop | `ts/state/smart/fun/giphy.preload.ts:22` | клиентский ключ Giphy | **настоящая** |

**Девять из одиннадцати находок уровня high были ложными.** Search-only ключ Algolia отдаётся каждому браузеру,
который открывает документацию; он умеет искать по одному индексу и не умеет ни писать, ни удалять, ни читать
данные аккаунта. Publishable-ключ платёжного шлюза по устройству живёт в URL. Фикстура `Test…` — это тестовые
данные в файле, который сам тестовым кодом не является.

Две настоящие — настоящие, но **не high**: ни одна не даёт доступа ни к средствам, ни к данным пользователей.
Секрет GA4 позволяет подмешивать события в аналитику Rabby; ключ Giphy — расходовать квоту Signal. Тестовый набор
уже содержал это решение, принятое намеренно и с объяснением: *преднамеренность раскрытия чужого ключа — решение
человека, а не то, что детектор вправе предполагать за него*. Я пришёл к тому же независимо и не стал его менять.

### Что изменено

Три защиты, каждая из измерения, а не из догадки, в `app/services/audit/analyzers/source_code.py`:

1. **Пометка самого проекта имеет силу.** Существовавшая защита читала только *имя переменной*
   (`COOKBOOK_PUBLIC_API_KEY`), поэтому решение, записанное в комментарии, было для неё невидимо. Комментарий в
   конце строки или строкой выше, который объявляет значение публичным — `publishable`, `search-only`,
   `public API key`, `safe to commit`, `not a secret` — и есть то человеческое решение, записанное теми, кто его
   принял. Одного слова «public» недостаточно: это модификатор в Java и слово про интерфейсы.
2. **Фикстура может лежать в рабочем файле.** Прежняя защита смотрела на путь, поэтому `TestSimpleHmacConfig` в
   `util/signature/simple_hmac.go` был вне её досягаемости. Теперь объявление, внутри которого лежит значение,
   ищется вверх до ближайшей строки с меньшим отступом, и решает его имя. Привязано к началу имени и требует
   границы регистра, поэтому `latest`, `attestation` и `contest` фикстурами не становятся.
3. **`hex_private_key_32b` — это форма, а не сущность.** Она означает «64 шестнадцатеричных символа», а по форме
   нельзя отличить приватный ключ от любого другого 32-байтового credential. ethers.js привязывает ровно эту форму
   к `defaultApiKey`, и отчёт клиенту говорил *приватный ключ* про опубликованный вендором RPC-ключ — фактическая
   ошибка, а отчёту, который неверно назвал одну находку, не верят и в остальных. Защита-переименование была
   написана и затем **удалена**: правка полноты ниже решает то же самое слоем раньше и лучше. Как только
   `defaultApiKey` читается так же, как всегда читался `default_api_key`, значение становится присваиванием
   API-ключа и вообще не притворяется ключом. Перед удалением это было измерено по именам: всё, что защита могла бы
   переименовать, теперь либо идёт через `generic_assignment`, либо не даёт находки, то есть код стал
   недостижимым — хуже оставить его вместе с тестом на поведение, которого конвейер уже не производит, чем не иметь
   ни того, ни другого.

### Прежнее решение развёрнуто — намеренно и открыто

Разбор этих же находок 23 октября пришёл к противоположному выводу и записал его: *«Комментарий не является
доказательством, поэтому они остаются находками, а человек помечает `accepted_risk`»*. Четыре из сегодняшних
случаев были там названы вручную. То решение защищало нечто реальное: `accepted_risk` оставляет строку внутри
подсчётов отчёта, с приложенным человеческим суждением, вместо того чтобы детектор решал один.

Его меняет не более удачный аргумент, а прошедший месяц: триаж, на который оно опиралось, не состоялся ни для
одной из них, девять ложных находок уровня high простояли в портфеле, и одна из них перекрывала возможность вообще
приводить цифры agave. Правило, вывод которого ложен на 82% при severity `high`, — это не вопрос в очередь к
аналитику, а дефект точности.

Поэтому сохранены обе половины. Находка подавляется, а причина пишется в раздел покрытия **напротив той строки, по
которой решение принято**, с указанием класса пометки, которая её сняла — `publishable`, `search-only`,
`safe to commit` — либо с именем объявления-фикстуры, внутри которого лежит значение. Клиенту не показывают его же
задокументированное решение как критическую проблему, но решение остаётся в отчёте, и с ним можно спорить.
Закреплено тестом по тому же принципу, что и правило хранилища доверия: решение должно быть произнесено, а не
умолчано.

### Измеренный результат

Прогон по тем же сверенным байтам, так что «до» и «после» отличаются только аналитиком:

| Аудит | До | После | Почему |
|---|---|---|---|
| agave | 1 | **0** | помечено как публичное |
| noir | 1 | **0** | помечено как публичное |
| metamask-extension | 3 | **0** | трижды помечено как публичное |
| nitro | 1 | **0** | объявление фикстуры |
| ethers-js | 1 (×3 копии) | 1 (×3) | оставлена, больше не называется приватным ключом |
| rabby | 1 | 1 | настоящая, оставлена намеренно |
| signal-desktop | 1 | 1 | настоящая, оставлена намеренно |
| **Всего строк** | **11** | **5** | и три из пяти больше не называются приватными ключами |

Соответственно у `agave` находок уровня high становится 15 вместо 16; noir, metamask-extension и nitro теряют по
одной high.

### Два дефекта, найденных при написании тестов

**Защита, которую никогда не проверяли.** Ветка «publishable» в `_PUBLIC_NAME` была закреплена случаем
`const publishableKey = 'pk_live_…'` — а такую строку редактирование вообще не помечает, то есть тест проходил
потому, что кандидата не было, а не потому, что защита работает. Так проходили впустую два случая. Теперь тестовый
файл разделяет `ANALYZER_QUIET`, где для каждого случая доказывается, что аналитику есть что подавлять, и `QUIET`,
где отсутствие редактирования само является механизмом.

**Моя собственная защита оказалась неверной, и поймал её мой собственный тест.**
`// https://stripe.com/docs/publishable-key` — это ссылка на страницу про publishable-ключи, а не утверждение о
значении рядом, и она заглушила настоящий секрет. Теперь ссылка внутри комментария вырезается до поиска фразы.

### Пробел в полноте, найденный по пути и закрытый

При измерении выяснилось, что `apiSecret` не редактируется вовсе, тогда как `API_SECRET` редактируется. Паттерн имени
принимал приставку, отделённую знаком (`client_secret`, `DB_PASSWORD`, `aws_secret_access_key`), но не отделённую
регистром — а camelCase как раз обычное написание в JavaScript, TypeScript, Java и Go. Поэтому `clientSecret`,
`authToken`, `dbPassword` и `apiSecret` никогда не редактировались и, значит, не могли быть и сообщены: не
неверный ответ, а отсутствие ответа, которое в отчёте читается как чистый результат. Этот тип отказа продукт
считает худшим, поэтому он исправлен, а не отложен.

Вторая альтернатива сделана **чувствительной к регистру** намеренно: приставка в camelCase считается только если
ключевое слово начинается с большой буквы, поэтому `notsecret`, `mytoken` и `subtoken` остаются именами. Правило
про суффиксы не тронуто — `token_type` и `secretName` называют что-то о credential, а не держат его. Приставка
ограничена сорока символами, чтобы проход оставался линейным, и в существующий тест на линейность добавлены два
враждебных входа под новую ветку.

### Проверки

`scripts/dev/lint.sh` чист (ruff, mypy, import-linter: 4 контракта соблюдены, 191 файл). Размеченный корпус,
сквозной аудит и тесты сложности анализаторов проходят (223), защиты от ложных секретов проходят в обе стороны (33).

### Намеренно не сделано

- **ethers.js сообщает об одном и том же ключе трижды** — из `src.ts/`, `lib.commonjs/` и `lib.esm/`, то есть из
  исходника и двух закоммиченных сборок. Подавление сборочных каталогов скрыло бы и секрет, внесённый на сборке,
  а это как раз то, что хочется знать, поэтому нужно отдельное измерение, а не догадка.
- **Две настоящие находки оставлены на уровне `high`.** Их понижение — изменение модели severity, которое надо
  обсуждать на уровне модели, а не проводить попутно с правкой точности.

---

# Дополнение 2026-10-28: расширение охвата и один измеренный регресс / 2026-10-28 addendum

## Пробел: ловилось 2 формы записи из 9

Разделитель в шаблоне `generic_assignment` был `(\s*[:=]\s*)` — **ровно один** символ. Анализатор видит только
то, что создал редактор, поэтому непойманная форма не могла быть сообщена ни при каких обстоятельствах: это тот
вид отказа, который выглядит как чистый результат.

| форма | до | после |
|---|---|---|
| `password = "…"`, `password: "…"` | видна | видна |
| `password := "…"` — **идиоматическое присваивание Go** | не видна | видна |
| `password === "…"`, `== "…"`, `!= "…"`, `!== "…"` | не видна | видна |
| `apiKey == "…"` (camelCase) | не видна | видна |
| `secret => hash(secret)`, `'logo_url' in approvals`, `passwordHash = "…"` | не видна | **не видна** |

Вторая форма особенно показательна: в `source_code.py` стоял комментарий, утверждавший, что операторы сравнения
исключены из фильтра намеренно, «потому что `password === "hunter2"` — это захардкоженный пароль». Верно про
фильтр и неверно про вход — значение до фильтра не доходило. Один модуль документировал возможность, которой
другой молча не имел.

## Замер: 11 репозиториев, и регресс найден до публикации

Образ пересобран, прогнаны четыре цели (`nitro`, `lightwalletd` — Go; `metamask-extension`, `rabby` — JS) и затем
семь JS/TS (`bitgo-mpc`, `bitwarden-sdk`, `ethers-js`, `matrix-js-sdk`, `reown-appkit`, `signal-desktop`,
`sigstore-js`). Проверено, что изменение живо в контейнере, а не что оно «должно работать».

**Новых настоящих находок: ноль.** Причина выяснена по исходникам, а не предположена: в `nitro` все `:=` рядом с
именами про учётные данные присваивают выражения (`nativeTokenAddressString := f…` — флаг запуска), а в `rabby`
реальная строка `password === ''` — проверка формы, которую порог в 8 символов отсекает правильно. Разработчики
сравнивают пароли с переменными, а не с литералами.

**Новых ложных: одна, и она была поймана до публикации.** `reown-appkit`,
`packages/scaffold-ui/src/views/w3m-swap-select-token-view/index.ts:103`:

```js
if (this.targetToken === 'sourceToken') {
```

Экран обмена спрашивает, какое поле он заполняет: «token» здесь — ERC-20 актив, а литерал — имя другого поля.
Важность — `high`, то есть именно та ошибка, которая дороже всего стоит доверию.

## Исправление: различает оператор, а не значение

Расширять правило «значение похоже на имя» было нельзя: в тестах закреплено, что `password = "MySecretHere"` —
**не** плейсхолдер, а чей-то слабый пароль. Разделяет эти случаи оператор:

* **сравнение** credential-именованной переменной с другим credential-подобным **именем** — это сравнение имён
  (состояние интерфейса, перечисление), а не секрета;
* **присваивание** имя-подобного значения — это слабый пароль и остаётся находкой.

`is_placeholder` получила параметр `comparison`, а списки ключевых слов вынесены в константы `_CRED_WORDS` и
`_CRED_WORDS_CAMEL`, которые теперь использует и основной шаблон, и новая проверка, — чтобы они не разъехались.

Итог после исправления: `reown-appkit` снова 103 находки и 0 строк по секретам, то есть ровно как до изменения.
**По 11 репозиториям: ноль новых находок, ноль новых ложных срабатываний.** Портфель цел — 42 комплекта,
подписи валидны, шлюз согласованности без расхождений. Тестов добавлено 16; вся связка по секретам проходит,
линт, mypy и контракты слоёв чисты.

**Ценность изменения — в охвате, не в находках сегодня:** закрыта форма, которой в этих одиннадцати
репозиториях нет, но которая является идиоматическим присваиванием в Go и обычным сравнением в JavaScript.

---

# ENGLISH

**The gap: 2 of 9 spellings were seen.** The `generic_assignment` separator was a single `[:=]`, and since an
analyzer only ever sees what redaction produced, the other seven could never be reported — the failure that reads
as a clean result. Now covered: Go's idiomatic `:=`, and `==`, `===`, `!=`, `!==` including the camelCase name
spelling. Still correctly ignored: arrow functions, membership operands, suffix names. Notably `source_code.py`
already carried a comment asserting that comparison operators were deliberately left in scope "because
`password === "hunter2"` is a hard-coded credential" — true of the filter, false of the input.

**The measurement: 11 repositories, and the regression was caught before publication.** Four targets (`nitro`,
`lightwalletd` in Go; `metamask-extension`, `rabby` in JS) then seven JS/TS repositories, on a rebuilt image whose
behaviour was verified inside the container. **Zero new real findings** — because in `nitro` every `:=` beside a
credential name assigns an expression (a launch flag), and `rabby`'s real line is `password === ''`, a form check
the 8-character floor correctly excludes. **One new false positive**, at `high`: reown-appkit's
`if (this.targetToken === 'sourceToken')`, a swap screen asking which field it is filling.

**The fix discriminates on the operator, not the value**, because an existing test pins
`password = "MySecretHere"` as somebody's weak password rather than a placeholder. Comparing a credential-named
variable against another credential-shaped name compares names; assigning one is a weak password. `is_placeholder`
gained a `comparison` parameter, and the keyword lists moved into constants shared by the pattern and the guard so
they cannot drift.

**Result: zero new findings and zero new false positives across 11 repositories**, reown-appkit back to its exact
prior figures, 42 bundles verifying, the consistency gate clean, 16 tests added, lint and mypy clean.
