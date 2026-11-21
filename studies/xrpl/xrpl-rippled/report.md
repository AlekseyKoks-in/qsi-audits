# Security & Post-Quantum Readiness Audit Report

**Project:** xrpl-rippled @ 82217fbd0ac4 · XRPL Foundation — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-21 10:18 UTC |
| Report version | 1 |
| Audit run | fe3a3564-14d5-49cb-a8cd-9be73435fd0a (Document audit) |
| Analyzer engine | qsi-engine 1.8.1 |
| Risk profile | Web3 project |
| Content SHA-256 | `9136ce16707b8ab4fe7a8b9f0015d3ef2cabb5b9408358727cb35ced33b70963` |
| Signature key (Ed25519 SHA-256 fingerprint, then the ML-DSA-65 one where it co-signs; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e · ML-DSA-65 dbd4e297b3213d1d7577a565e76de14cc5ad0e409f1dc68291c67266fc95066a` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **5**
- Low: **2**
- Info: **0**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 0
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 7
- Improvement recommendation: 0
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 5, y = 5, z = 12 → tight margin. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/XRPLF/rippled> @ `82217fbd0ac4234c3a97fedcf94f35e5796aa9f2` — evidence links open the lines at this commit.

1246 files, 9330952 bytes in total, 4 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 1232 | .github/scripts/check-pr-description.py: 85 lines scanned with 16 rule patterns and 313 registry patterns; .github/scripts/format-inline-bash.py: 403 lines scanned with 16 rule patterns and 313 registry patterns; .github/scripts/levelization/generate.py: 335 lines scanned with 16 rule patterns and 313 registry patterns |
| certificates | error (not checked) | 1 | bin/check-distrusted-roots.sh line 36: certificate could not be parsed (ValueError) |
| certificates_and_keys | checked | 1 | bin/check-distrusted-roots.sh: certificates/keys parsed |
| dependencies | checked | 4 | cmake/scripts/codegen/requirements.txt: 4 dependencies parsed (0 pinned); crates/Cargo.lock: 33 dependencies parsed (33 pinned); crates/Cargo.toml: 1 dependencies parsed (0 pinned) |
| secrets | checked | 2 | include/xrpl/config/Constants.h: 3 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name); src/xrpld/rpc/handlers/transaction/Simulate.cpp: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| entropy | checked | 1 | random-number generation: 1232 code files read with 12 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |
| crediting | checked | 1 | payment crediting: 2 file(s) read incoming transfers on TON, the XRP Ledger, Tron or an EVM chain, 0 credit from a Tron or EVM node; 0 lead(s). A wait for confirmations or finality is recognised by its words, not traced; reorganisations and duplicate crediting are not checked |
| osv_advisories | checked | 1 | 33 pinned packages queried at OSV.dev; 0 affected |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- certificates — error (not checked): bin/check-distrusted-roots.sh line 36: certificate could not be parsed (ValueError)

## 5. Architecture overview

Static review of the source tree xrpl-rippled at 82217fbd0ac4234c3a97fedcf94f35e5796aa9f2. 1246 files analysed; of 2189 files, 685 are test, fuzzing, benchmark or example code and were left out, 258 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .clang-format, .clang-tidy, .codecov.yml, .cspell.config.yaml, .envrc. 37 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **100** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 97.3%

## 7. Detailed findings

### QSI-2026-34889 — Quantum-vulnerable ECDSA: transaction and message signing (5 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: include/xrpl/protocol/detail/secp256k1.h
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:18 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

36 reference(s) to ECDSA across 5 file(s), e.g. include/xrpl/protocol/detail/secp256k1.h:3. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open include/xrpl/protocol/detail/secp256k1.h:3 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [include/xrpl/protocol/detail/secp256k1.h](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/include/xrpl/protocol/detail/secp256k1.h#L3) · line 3 · SHA-256 6c16d6709c6f777da57ac7e1740c83332f4b103b3ed1772e64f46a1a1aec50be_

```
    2 | 
    3 | #include <secp256k1.h>
    4 | 
```

_file_excerpt · [src/libxrpl/protocol/PublicKey.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/PublicKey.cpp#L10) · line 10 · SHA-256 f727dca3b6f535ac3a2684df1383c54ca63987ae83051f26f64909ac57bc55a9_

```
    9 | #include <xrpl/protocol/UintTypes.h>
   10 | #include <xrpl/protocol/detail/secp256k1.h>
   11 | #include <xrpl/protocol/digest.h>
```

_file_excerpt · [src/libxrpl/protocol/PublicKey.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/PublicKey.cpp#L17) · line 17 · SHA-256 38584098da024c99ad081756c86658f000704c2f0eb395e73fc0a059a2a60ee6_

```
   16 | #include <ed25519.h>
   17 | #include <secp256k1.h>
   18 | 
```

_file_excerpt · [src/libxrpl/protocol/PublicKey.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/PublicKey.cpp#L217) · line 217 · SHA-256 ba26a105fe9791a3e3eb229abb60497b82b63d4e9907842fa0eba3f00a311ffc_

```
  216 |         if (slice[0] == kEcCompressedPrefixEvenY || slice[0] == kEcCompressedPrefixOddY)
  217 |             return KeyType::Secp256k1;
  218 |     }
```

_file_excerpt · [src/libxrpl/protocol/SecretKey.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/SecretKey.cpp#L14) · line 14 · SHA-256 38e5325ec4258b984ac91eed5c93f4e9e3440ebaee85bc56728f914649281d64_

```
   13 | #include <xrpl/protocol/Seed.h>
   14 | #include <xrpl/protocol/detail/secp256k1.h>
   15 | #include <xrpl/protocol/digest.h>
```

_file_excerpt · [src/libxrpl/protocol/SecretKey.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/SecretKey.cpp#L21) · line 21 · SHA-256 840a5f6d8fe49549a0785d05dda7accffb38254693cbffad59f99b78fb9b1c1e_

```
   20 | #include <ed25519.h>
   21 | #include <secp256k1.h>
   22 | 
```

_file_excerpt · [src/libxrpl/protocol/SecretKey.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/SecretKey.cpp#L201) · line 201 · SHA-256 cba1430f01340d81f4d8c4fd3d128772b495146aab735d5634b65d9d6d6c482e_

```
  200 | 
  201 |         return {derivePublicKey(KeyType::Secp256k1, gsk), gsk};
  202 |     }
```

_file_excerpt · [src/libxrpl/server/Wallet.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/server/Wallet.cpp#L167) · line 167 · SHA-256 381d1f5fc567cfaf9a439fe4fbfab001d90ca37e7826fffffab6161a930bf97d_

```
  166 |             // Only use if the public and secret keys are a pair
  167 |             if (sk && pk && (*pk == derivePublicKey(KeyType::Secp256k1, *sk)))
  168 |                 return {*pk, *sk};
```

_file_excerpt · [src/libxrpl/server/Wallet.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/server/Wallet.cpp#L173) · line 173 · SHA-256 f3e90e4ed2e8ed4fc594065641c51539ac18e39cc64d4e649e37a098c7d12414_

```
  172 |     // If a valid identity wasn't found, we randomly generate a new one:
  173 |     auto [newpublicKey, newsecretKey] = randomKeyPair(KeyType::Secp256k1);
  174 | 
```

_file_excerpt · [src/xrpld/rpc/handlers/admin/keygen/WalletPropose.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/xrpld/rpc/handlers/admin/keygen/WalletPropose.cpp#L125) · line 125 · SHA-256 fc9152883a4a2deac1b906c58de8656cabf0cc5370a84539b883c8a6b4056151_

```
  124 |     if (!keyType)
  125 |         keyType = KeyType::Secp256k1;
  126 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-34891 — Quantum-vulnerable Ed25519: transaction and message signing (3 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:transaction_signing`
- Data source: src/libxrpl/protocol/PublicKey.cpp
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:18 UTC
- Priority score: 33.0 / 100
- CVSS v3.1: not applicable

11 reference(s) to Ed25519 across 3 file(s), e.g. src/libxrpl/protocol/PublicKey.cpp:214. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/libxrpl/protocol/PublicKey.cpp:214 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/libxrpl/protocol/PublicKey.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/PublicKey.cpp#L214) · line 214 · SHA-256 24bbd8c1b991a3ae0933fdc66c33535414986777343af43d8300262f80bd0cf7_

```
  213 |         if (slice[0] == 0xED)
  214 |             return KeyType::Ed25519;
  215 | 
```

_file_excerpt · [src/libxrpl/protocol/PublicKey.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/PublicKey.cpp#L280) · line 280 · SHA-256 e0071f88d3334f0d64589a828741b0c7e3ca9ce45b319a2772de67091ebacddd_

```
  279 |         }
  280 |         if (*type == KeyType::Ed25519)
  281 |         {
```

_file_excerpt · [src/libxrpl/protocol/PublicKey.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/PublicKey.cpp#L289) · line 289 · SHA-256 c8344a31c692a0e31b00571e81b72bc52a70015906fc518eab4332ff4d072d5a_

```
  288 |             // first strip that prefix.
  289 |             return ed25519_sign_open(m.data(), m.size(), publicKey.data() + 1, sig.data()) == 0;
  290 |         }
```

_file_excerpt · [src/libxrpl/protocol/SecretKey.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/SecretKey.cpp#L240) · line 240 · SHA-256 3c24fcf15e268889f6d1e314392aa126fa3a68fa1b159771a9dae5afc1791456_

```
  239 |     {
  240 |         case KeyType::Ed25519: {
  241 |             Buffer b(64);
```

_file_excerpt · [src/libxrpl/protocol/SecretKey.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/SecretKey.cpp#L242) · line 242 · SHA-256 3c7c8a245e1c4b5ec959accfb61f516c08a228f59dc8936dcfdedd1887ed765a_

```
  241 |             Buffer b(64);
  242 |             ed25519_sign(m.data(), m.size(), sk.data(), pk.data() + 1, b.data());
  243 |             return b;
```

_file_excerpt · [src/libxrpl/protocol/SecretKey.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/SecretKey.cpp#L286) · line 286 · SHA-256 c7f6b8062f06a9588d7c69ff30f351b0f90ede10bb93a2fc325983f003f77201_

```
  285 | {
  286 |     if (type == KeyType::Ed25519)
  287 |     {
```

_file_excerpt · [src/xrpld/rpc/handlers/admin/keygen/WalletPropose.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/xrpld/rpc/handlers/admin/keygen/WalletPropose.cpp#L99) · line 99 · SHA-256 1f299e753f425f4ac9ca5151b45ef562d304cf4afed710850f5d2edcece86f26_

```
   98 |             // Ed25519 we return an error.
   99 |             if (keyType.value_or(KeyType::Ed25519) != KeyType::Ed25519)
  100 |                 return rpcError(RpcBadSeed);
```

_file_excerpt · [src/xrpld/rpc/handlers/admin/keygen/WalletPropose.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/xrpld/rpc/handlers/admin/keygen/WalletPropose.cpp#L102) · line 102 · SHA-256 6b122be9cb05ae09dc5452b23504d1a479534b4fdb9254b4c02687cf8ed47d08_

```
  101 | 
  102 |             keyType = KeyType::Ed25519;
  103 |         }
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-34886 — Quantum-vulnerable ECDSA: role not determined (15 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: conanfile.py
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:18 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

31 reference(s) to ECDSA across 15 file(s), e.g. conanfile.py:102. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open conanfile.py:102 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [conanfile.py](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/conanfile.py#L102) · line 102 · SHA-256 775460b37c8975103fa15121bc84b156e4cf36027d484d1c6c34d23b7db30a9d_

```
  101 |         "rocksdb/*:with_snappy": True,
  102 |         "secp256k1/*:shared": False,
  103 |         "snappy/*:shared": False,
```

_file_excerpt · [conanfile.py](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/conanfile.py#L136) · line 136 · SHA-256 5cf505cce5c92ca55c4e753b7924f68ac48b41a1f512a9a33043a071914d8cc2_

```
  135 |             self.requires("rocksdb/10.5.1")
  136 |         self.requires("secp256k1/0.7.1", transitive_headers=True)
  137 |         self.requires("sqlite3/3.53.0", force=True)
```

_file_excerpt · [conanfile.py](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/conanfile.py#L225) · line 225 · SHA-256 3fc59cee850354680b97a4999d4b2ae897ee4f1f9db19b2a3592236167f5ee8f_

```
  224 |             "soci::soci",
  225 |             "secp256k1::secp256k1",
  226 |             "sqlite3::sqlite",
```

_file_excerpt · [include/xrpl/protocol/ConfidentialTransfer.h](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/include/xrpl/protocol/ConfidentialTransfer.h#L13) · line 13 · SHA-256 c366d5bf79d2ffaa396837ffdd35eaa762f1ebf455e04dc229d094716288fdfe_

```
   12 | #include <xrpl/protocol/UintTypes.h>
   13 | #include <xrpl/protocol/detail/secp256k1.h>
   14 | 
```

_file_excerpt · [include/xrpl/protocol/ConfidentialTransfer.h](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/include/xrpl/protocol/ConfidentialTransfer.h#L15) · line 15 · SHA-256 1183fef450a5669f88636dd00c656a9db1687dcca9cd2bea4b10018839326258_

```
   14 | 
   15 | #include <secp256k1.h>
   16 | 
```

_file_excerpt · [include/xrpl/protocol/KeyType.h](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/include/xrpl/protocol/KeyType.h#L16) · line 16 · SHA-256 88a5525ec38ffea82bfbcec7d9c930d51e37b4d91c7bedaef301235935c8d391_

```
   15 | {
   16 |     if (s == "secp256k1")
   17 |         return KeyType::Secp256k1;
```

_file_excerpt · [include/xrpl/protocol/KeyType.h](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/include/xrpl/protocol/KeyType.h#L17) · line 17 · SHA-256 13c8ae1808dab55f50025ba24e71573bb9373ca52c527f9d624ac339eb02a8ad_

```
   16 |     if (s == "secp256k1")
   17 |         return KeyType::Secp256k1;
   18 | 
```

_file_excerpt · [include/xrpl/protocol/KeyType.h](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/include/xrpl/protocol/KeyType.h#L28) · line 28 · SHA-256 190a78a3c249829b0eba660c990119ad4e86c310ed8d8ed82bd3a78df4657bcf_

```
   27 | {
   28 |     if (type == KeyType::Secp256k1)
   29 |         return "secp256k1";
```

_file_excerpt · [include/xrpl/protocol/STValidation.h](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/include/xrpl/protocol/STValidation.h#L194) · line 194 · SHA-256 1d3cc4bdde996ae4da1cbea6ce43b2fe04e1594d426d8ad9383994cf9e2eab15_

```
  193 | 
  194 |         if (publicKeyType(makeSlice(spk)) != KeyType::Secp256k1)
  195 |             Throw<std::runtime_error>("Invalid public key in validation");
```

_file_excerpt · [include/xrpl/protocol/STValidation.h](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/include/xrpl/protocol/STValidation.h#L238) · line 238 · SHA-256 d20295b008470f5df5193e2f04e4360e59b59c5be3b4fba8ce5294fa6573cd8d_

```
  237 |     // First, set our own public key:
  238 |     if (publicKeyType(pk) != KeyType::Secp256k1)
  239 |         logicError("We can only use secp256k1 keys for signing validations");
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-34887 — Quantum-vulnerable Ed25519: role not determined (3 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:Ed25519:general`
- Data source: conanfile.py
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:18 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

6 reference(s) to Ed25519 across 3 file(s), e.g. conanfile.py:216. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open conanfile.py:216 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [conanfile.py](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/conanfile.py#L216) · line 216 · SHA-256 d3de261a0ebfd888c2ad8cf259c96fb8ba8d5ee9011d85aa86eb314934995e05_

```
  215 |             "date::date",
  216 |             "ed25519::ed25519",
  217 |             "fast_float::fast_float",
```

_file_excerpt · [include/xrpl/protocol/KeyType.h](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/include/xrpl/protocol/KeyType.h#L20) · line 20 · SHA-256 214e02ba06d5031ed7a3608cdd3a92a0ee55348e73abda9a0f283ce1d96155ba_

```
   19 |     if (s == "ed25519")
   20 |         return KeyType::Ed25519;
   21 | 
```

_file_excerpt · [include/xrpl/protocol/KeyType.h](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/include/xrpl/protocol/KeyType.h#L31) · line 31 · SHA-256 aa0a86dc057d5b475eb45ce13282d2311e830d863ad1e532743419a686d957c8_

```
   30 | 
   31 |     if (type == KeyType::Ed25519)
   32 |         return "ed25519";
```

_file_excerpt · [src/xrpld/rpc/detail/RPCHelpers.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/xrpld/rpc/detail/RPCHelpers.cpp#L367) · line 367 · SHA-256 6130b800795fa4d38f2b699cc262a2614925ca37f76f04a44dd2c93a97333211_

```
  366 |             // requested another key type, return an error.
  367 |             if (keyType.value_or(KeyType::Ed25519) != KeyType::Ed25519)
  368 |             {
```

_file_excerpt · [src/xrpld/rpc/detail/RPCHelpers.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/xrpld/rpc/detail/RPCHelpers.cpp#L373) · line 373 · SHA-256 4779ef1e059b7680b3ff7ae710d193b0ff75c697a423fd36003fd68df949f3ef_

```
  372 | 
  373 |             keyType = KeyType::Ed25519;
  374 |         }
```

_file_excerpt · [src/xrpld/rpc/detail/RPCHelpers.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/xrpld/rpc/detail/RPCHelpers.cpp#L408) · line 408 · SHA-256 4e0804d2ed7c4d70f9e507bb9f5f7c52abdd394c7563aff14307ce7c6a20dcc5_

```
  407 | 
  408 |     if (keyType != KeyType::Secp256k1 && keyType != KeyType::Ed25519)
  409 |         logicError("keypairForSignature: invalid key type");
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-34892 — Quantum-vulnerable ECDSA: authentication and identity (certificates, tokens, device attestation) (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:authentication`
- Data source: src/xrpld/app/main/NodeIdentity.cpp
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:18 UTC
- Priority score: 31.7 / 100
- CVSS v3.1: not applicable

2 reference(s) to ECDSA across 1 file(s), e.g. src/xrpld/app/main/NodeIdentity.cpp:48. Role, judged from paths, function names and nearby code: authentication and identity (certificates, tokens, device attestation). Short-lived authentication stays safe until a CRQC exists; long-lived identities (device attestation, CA and SSH keys) need a plan earlier.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/xrpld/app/main/NodeIdentity.cpp:48 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/xrpld/app/main/NodeIdentity.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/xrpld/app/main/NodeIdentity.cpp#L48) · line 48 · SHA-256 6bbb971c7a8e5d69722cf65d66fc31e6be8680564b2ade9980b81d01bdddf809_

```
   47 |     {
   48 |         auto const secretKey = [REDACTED] *seed);
   49 |         auto const publicKey = derivePublicKey(KeyType::Secp256k1, secretKey);
```

_file_excerpt · [src/xrpld/app/main/NodeIdentity.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/xrpld/app/main/NodeIdentity.cpp#L49) · line 49 · SHA-256 126e0ee85341021f97ff8c121e7f82ea7c3a7f0cd33f40aa3c8ae290067a9d7e_

```
   48 |         auto const secretKey = [REDACTED] *seed);
   49 |         auto const publicKey = derivePublicKey(KeyType::Secp256k1, secretKey);
   50 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-34888 — Quantum-vulnerable EC-ElGamal: role not determined (2 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:EC-ElGamal:general`
- Data source: include/xrpl/protocol/Protocol.h
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:18 UTC
- Priority score: 25.2 / 100
- CVSS v3.1: not applicable

5 reference(s) to EC-ElGamal across 2 file(s), e.g. include/xrpl/protocol/Protocol.h:10. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open include/xrpl/protocol/Protocol.h:10 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [include/xrpl/protocol/Protocol.h](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/include/xrpl/protocol/Protocol.h#L10) · line 10 · SHA-256 bc51b5ff22b1fc724b515092053780f6f982993a2a11361ca4654e6e9965654a_

```
    9 | #include <mpt_protocol.h>
   10 | #include <secp256k1_mpt.h>
   11 | 
```

_file_excerpt · [src/libxrpl/protocol/ConfidentialTransfer.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/ConfidentialTransfer.cpp#L23) · line 23 · SHA-256 0a5bb4cf53dfb7ed48b3a433616e0d73b278ae8fc9449c89973b2be7dda743ca_

```
   22 | #include <secp256k1.h>
   23 | #include <secp256k1_mpt.h>
   24 | 
```

_file_excerpt · [src/libxrpl/protocol/ConfidentialTransfer.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/ConfidentialTransfer.cpp#L205) · line 205 · SHA-256 4ee166148e0d245fab21c6db030f0e9a6f6e9043211b65e18451ed927d124450_

```
  204 |     EcPair sum{};
  205 |     if (auto const res = secp256k1_elgamal_add(
  206 |             secp256k1Context(), &sum.c1, &sum.c2, &pairA->c1, &pairA->c2, &pairB->c1, &pairB->c2);
```

_file_excerpt · [src/libxrpl/protocol/ConfidentialTransfer.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/protocol/ConfidentialTransfer.cpp#L228) · line 228 · SHA-256 b7044493e58c3f69b8b0ef1f54ce56df8571bfb7bbd5d4af3c84010dc024cc30_

```
  227 |     EcPair diff{};
  228 |     if (auto const res = secp256k1_elgamal_subtract(
  229 |             secp256k1Context(), &diff.c1, &diff.c2, &pairA->c1, &pairA->c2, &pairB->c1, &pairB->c2);
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-34890 — Quantum-vulnerable RSA: role not determined (1 file(s))

- Severity: **Low** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:RSA:general`
- Data source: src/libxrpl/basics/make_SSLContext.cpp
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.8.1 · 2026-11-21 10:18 UTC
- Priority score: 25.2 / 100
- CVSS v3.1: not applicable

2 reference(s) to RSA across 1 file(s), e.g. src/libxrpl/basics/make_SSLContext.cpp:106. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open src/libxrpl/basics/make_SSLContext.cpp:106 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [src/libxrpl/basics/make_SSLContext.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/basics/make_SSLContext.cpp#L106) · line 106 · SHA-256 488016f7bb481bc190519056867710fb869582ceb86673b09338269dc00061a1_

```
  105 | 
  106 |         if (RSA_generate_key_ex(rsa, gDefaultRsaKeyBits, bn, nullptr) != 1)
  107 |             logicError("RSA_generate_key_ex failure");
```

_file_excerpt · [src/libxrpl/basics/make_SSLContext.cpp](https://github.com/XRPLF/rippled/blob/82217fbd0ac4234c3a97fedcf94f35e5796aa9f2/src/libxrpl/basics/make_SSLContext.cpp#L107) · line 107 · SHA-256 406e921d4e3417572ddb9e9257aa7426b7eb82b6959bf35a52d01be94ba04337_

```
  106 |         if (RSA_generate_key_ex(rsa, gDefaultRsaKeyBits, bn, nullptr) != 1)
  107 |             logicError("RSA_generate_key_ex failure");
  108 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.


## 8. Post-quantum assessment

| | Key establishment (x = how long data must stay confidential; harvest now, decrypt later) | Signatures (x = how long signatures/keys must stay trusted) |
|---|---|---|
| Data/key lifetime x | 5 | 10 |
| Migration time y | 5 | 5 |
| Assumed years to CRQC z | 12 (central) | 12 |
| x + y − z | -2 → tight margin | 3 → migration would finish too late under this scenario |
#### Where z comes from

Averaged expert likelihood that a CRQC exists within each horizon, from the annual survey published by the author of this inequality. Likelihood estimates, not predictions of a date.

| Within | Likelihood | The report's wording |
|---|---|---|
| 5 years | ~15% | averaged estimate |
| 10 years | 28-49% | quite possible |
| 15 years | 51-70% | likely |

**Why this scenario (central, z = 12):** Between the 10-year band (28-49%) and the 15-year band (51-70%): roughly where the experts' averaged likelihood crosses one half. More than half of the respondents (13 of 26) already put the likelihood at 50% or more for some horizon.
_Planning assumptions: x for key establishment, x for signatures, y are the defaults of the risk profile “Web3 project”, not the client's figures; with the client's actual lifetimes the verdict can change._

### Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography


**Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **transaction and message signing** | ECDSA (5), Ed25519 (3) | QSI-2026-34889, QSI-2026-34891 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **authentication and identity (certificates, tokens, device attestation)** | ECDSA (1) | QSI-2026-34892 | Keep credentials short-lived and plan ML-DSA certificates, tokens and keys as the ecosystem supports them |
| **role not determined** | ECDSA (15), Ed25519 (3), EC-ElGamal (2), RSA (1) | QSI-2026-34886, QSI-2026-34887, QSI-2026-34888, QSI-2026-34890 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — factoring | breaks | Q1 | RSA (1) | Breaks RSA at every key length: a longer modulus only raises the cost polynomially. Plan migration to ML-KEM (or a hybrid) for key establishment and ML-DSA / SLH-DSA for signatures; start with keys protecting data that must stay confidential for years (harvest now, decrypt later) and with long-lived signatures. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | EC-ElGamal (2), ECDSA (25), Ed25519 (8) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | SHA-2 (1) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | SHA-2 (1) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- certificates: bin/check-distrusted-roots.sh line 36: certificate could not be parsed (ValueError)

## 10. Remediation plan / Priorities for 30, 60 and 90 days

### 30 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
### 60 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
### 90 days

| Priority | ID | Action | Type | Closure criteria |
|---|---|---|---|---|
| P3 | QSI-2026-34889 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-34891 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-34886 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-34887 | Add Ed25519 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-34892 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-34888 | Add EC-ElGamal usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-34890 | Add RSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-34889 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-34891 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-34886 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-34887 | Plan migration of Ed25519 to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-34892 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-34888 | Plan migration of EC-ElGamal to NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows NIST's post-quantum standards cover key encapsulation and signatures; none covers additively homomorphic encryption. Treat amounts encrypted this way as eventually public, and limit what a design must store on-ledger; lattice-based homomorphic schemes are the research direction or a hybrid scheme in use. |
| P4 | QSI-2026-34890 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |

## 11. Tools used

- blockchain 1.0.0
- certificates 1.2.0
- chain_map 1.0.0
- configs 1.1.0
- crediting 1.1.0
- dependencies 1.4.3
- hndl 1.0.0
- inventory_document 1.1.0
- mpc 1.0.0
- solidity 1.5.2
- source_code 1.7.1
- tls_code 1.1.0
- tls_live 1.0.0
- ton_contracts 1.0.0
- validator_keys 1.2.0
- wallet_login 1.0.0
- qsi-engine 1.8.1
- OSV.dev API v1

## 12. Sources and normative documents

1. A. Chailloux, M. Naya-Plasencia, A. Schrottenloher — An Efficient Quantum Collision Search Algorithm and Implications on Symmetric Cryptography (ASIACRYPT 2017; IACR ePrint 2017/847) — IACR ePrint. <https://eprint.iacr.org/2017/847> (peer-reviewed article: Õ(2^{2n/5}) time, O(n) qubits, Õ(2^{n/5}) classical memory)
2. C. Chevignard, P.-A. Fouque, A. Schrottenloher — Reducing the Number of Qubits in Quantum Discrete Logarithms on Elliptic Curves (IACR ePrint 2026/280) — IACR ePrint. <https://eprint.iacr.org/2026/280> (revision of a EUROCRYPT 2026 paper: 3.12n + o(n) qubits; for n = 256, 1193 qubits and 22 runs of 2^38.98 Toffoli gates)
3. C. Gidney — How to factor 2048 bit RSA integers with less than a million noisy qubits (arXiv:2505.15917) — arXiv. <https://arxiv.org/abs/2505.15917> (preprint (2025-05-21): < 1 million noisy qubits, < 1 week, 0.1% gate error, 1 µs surface-code cycle)
4. C. Gidney, M. Ekerå — How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits (Quantum 5, 433) — Quantum. <https://doi.org/10.22331/q-2021-04-15-433> (peer-reviewed article (2021): 10^-3 gate error, 1 µs cycle, 10 µs reaction time)
5. C. Zalka — Grover's quantum searching algorithm is optimal (Phys. Rev. A 60, 2746, 1999; arXiv:quant-ph/9711070) — APS. <https://doi.org/10.1103/PhysRevA.60.2746> (peer-reviewed article: optimal for any success probability; parallel search gains no more than splitting the space)
6. Common Vulnerability Scoring System v3.1: Specification Document — FIRST. <https://www.first.org/cvss/v3.1/specification-document> (final)
7. D. J. Bernstein — Cost analysis of hash collisions: Will quantum computers make SHARCS obsolete? (2009) — cr.yp.to. <https://cr.yp.to/hash/collisioncost-20090823.pdf> (paper dated 2009-08-23)
8. D. Litinski — How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates (arXiv:2306.08585) — arXiv. <https://arxiv.org/abs/2306.08585> (preprint (2023-06-14): 6000 modules × 1152 physical qubits, one key per 10 minutes under its architecture assumptions)
9. FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — NIST. <https://csrc.nist.gov/pubs/fips/203/final> (final (August 2024))
10. FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/204/final> (final (August 2024))
11. FIPS 205 — Stateless Hash-Based Digital Signature Standard (SLH-DSA) — NIST. <https://csrc.nist.gov/pubs/fips/205/final> (final (August 2024))
12. G. Brassard, P. Høyer, A. Tapp — Quantum Algorithm for the Collision Problem (LATIN '98; arXiv:quant-ph/9705002) — Springer / arXiv. <https://arxiv.org/abs/quant-ph/9705002> (peer-reviewed article: collisions of r-to-one functions in O((N/r)^{1/3}) expected evaluations)
13. J. Proos, C. Zalka — Shor's discrete logarithm quantum algorithm for elliptic curves (Quantum Inf. Comput. 3(4), 2003; arXiv:quant-ph/0301141) — Quantum Information & Computation. <https://doi.org/10.26421/QIC3.4-3> (peer-reviewed article)
14. L. K. Grover — A fast quantum mechanical algorithm for database search (STOC 1996) — ACM. <https://doi.org/10.1145/237814.237866> (peer-reviewed article)
15. M. Amy et al. — Estimating the cost of generic quantum pre-image attacks on SHA-2 and SHA-3 (SAC 2016; arXiv:1603.09383) — Springer / arXiv. <https://arxiv.org/abs/1603.09383> (peer-reviewed article: SHA-256 about 2^153.8 surface-code cycles on 2^12.6 logical qubits; SHA3-256 about 2^146.5 cycles on 2^20)
16. M. Cain et al. — Shor's algorithm is possible with as few as 10,000 reconfigurable atomic qubits (arXiv:2603.28627) — arXiv. <https://arxiv.org/abs/2603.28627> (preprint (2026-03-30): P-256 in a few days with 26,000 physical neutral-atom qubits; RSA-2048 one to two orders of magnitude longer)
17. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
18. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
19. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
20. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
21. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
22. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
23. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: dependency manifests 2 (2 Shor-breakable) · own code 35 (34 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| SHA-2 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 1 | 1 | src/libxrpl/basics/make_SSLContext.cpp:213 |
| EC-ElGamal |  |  | vulnerable (Shor) | acceptable | 2 | 2 | include/xrpl/protocol/Protocol.h:10; src/libxrpl/protocol/ConfidentialTransfer.cpp:23 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 19 | 19 | conanfile.py:102; include/xrpl/protocol/ConfidentialTransfer.h:13; include/xrpl/protocol/KeyType.h:16 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 6 | 6 | include/xrpl/protocol/STValidation.h:249; include/xrpl/protocol/SecretKey.h:160; src/libxrpl/protocol/PublicKey.cpp:246 |
| Ed25519 | Ed25519 |  | vulnerable (Shor) | acceptable | 8 | 8 | conanfile.py:216; include/xrpl/protocol/KeyType.h:20; src/libxrpl/protocol/PublicKey.cpp:214 |
| RSA |  |  | vulnerable (Shor) | acceptable | 1 | 1 | src/libxrpl/basics/make_SSLContext.cpp:106 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| .github/scripts/check-pr-description.py | 2524 | `1eb040604b4330b16ace0ef7f7ea581c0c38280a08be82d403f34350cdb36328` | 0 |
| .github/scripts/format-inline-bash.py | 13114 | `4ef6facaf4b95fa85319e17c62dba3a626796d1bf21f1fd16a5e769343fd4e7d` | 0 |
| .github/scripts/levelization/generate.py | 12347 | `9ed9694c197a0d462897c3a1e1afc6b34835f6d33f812634ad07f0fec3546c62` | 0 |
| .github/scripts/strategy-matrix/generate.py | 14102 | `92e95eb081710b2471333247e0acd6e9591ca9fc3a649d0422962fabdfe7223a` | 0 |
| bin/check-distrusted-roots.sh | 2044 | `5f1bbc720b859dff8885c67e2c7ea82ff520537f49ff3edcc00c23b0c2bca5ec` | 0 |
| bin/filter-clang-tidy.py | 3414 | `9bc6d35e6a21e6eeac585b6543f63b3c6e701ae0bc30ca79f32c9d8cedc2e446` | 0 |
| bin/pre-commit/check_doxygen_style.py | 17747 | `45a03639cb62fda0a5d65b33c8d4000d46accdc3686c220ad62dbbfe1fb9dbd9` | 0 |
| bin/pre-commit/check_rust_coverage_attrs.py | 5407 | `b8ebf9dde5521bc96018ece6155afb3fa32a48b7bec44ab40ec2cf0f1b546ae4` | 0 |
| bin/pre-commit/clang_tidy_check.py | 3540 | `b991df083f5fd5ed418665ae41d9ab5f1bef523a6ba681fcadc4801e10b813f8` | 0 |
| bin/pre-commit/fix_gtest_names.py | 5317 | `e2dfb5df1306d0fb6a311a1eea649b725d751342fa5d409908aaa41008a8e883` | 0 |
| bin/pre-commit/fix_include_style.py | 816 | `a315fcde2f921fde86097fc8e09002494a38e31bc5ef7597dbf2d7b6bdf240a4` | 0 |
| bin/pre-commit/fix_pragma_once.py | 703 | `ad0ec13c5609c661fb15b22a692d973c8877f72d5402610af51843853413a848` | 0 |
| cmake/scripts/codegen/generate_ledger_classes.py | 6779 | `e9f4f027b1f6c9d1593b182effd1971c013554fba292524bba7aed3614f665ba` | 0 |
| cmake/scripts/codegen/generate_tx_classes.py | 9420 | `e33e95dfebaddb5c9d2d9e367645e3874f7c21dd96fb95258636094b93409ed8` | 0 |
| cmake/scripts/codegen/macro_parser_common.py | 10246 | `01cc8994e276ec477becfaf3b8aa9c3322a27624b0cce3adf7b5507a4e236393` | 0 |
| cmake/scripts/codegen/requirements.txt | 8383 | `28b31103616e8e27d91961c27ddff60327bcbd0803f0c8b65df2930e64482bf9` | 0 |
| conanfile.py | 7439 | `e7391d14f374b20b0145712c7d9e3a3ebeab0d49bcfce692f78182d96f882016` | 0 |
| crates/.cargo/config.toml | 276 | `ebf2265f68f1cea59a5cfe1d9c58e3d20ae70d12ec890a40e97810978cf99b4b` | 0 |
| crates/Cargo.lock | 7741 | `975d736978fca74bd4e2a6a14106d445e4f56f7dd8f4860d4444cf86877e77ba` | 0 |
| crates/Cargo.toml | 368 | `7d8c232d2cb6cd5f9fc280e1c5f4892f07dcf19da4867876ac5fc08bd051e8b8` | 0 |
| crates/hello_world/Cargo.toml | 174 | `a04b45096c58f8a2f976fc3037077489a49ac439bff257f57ad969b6550c64e9` | 0 |
| crates/hello_world/src/lib.rs | 449 | `671f40ddd03fabc7126e7b01915b76bf54fe465eb08ec127885aad5a337d5a75` | 0 |
| external/antithesis-sdk/antithesis_instrumentation.h | 3543 | `22020ab853956ad449e4d1e15e49d0720ac3cc0a70fd45d3478e2a2f4ad1d6e1` | 0 |
| external/antithesis-sdk/antithesis_sdk.h | 44526 | `81454c3bc0d1bd0d2284102f1cd84c30d2e6554ffdc2ca66861285842371f78c` | 0 |
| include/xrpl/basics/Blob.h | 229 | `9f045cd6d85f71f83b1f0049d035a184a598e362fecdd165f73be6cfe08f420f` | 0 |
| include/xrpl/basics/Buffer.h | 4886 | `22367df8c0b2f26dc8076a492732abd2cd5192e729518a92b6279da8c409cbea` | 0 |
| include/xrpl/basics/ByteUtilities.h | 380 | `883d9b9363fe6bdd3005a4fa4b02f01d8d96bcdfe90688ec6226047e0b4f0a8d` | 0 |
| include/xrpl/basics/CompressionAlgorithms.h | 4302 | `488f67c6296ba4964795c9397d0ee6810621dce096762564da08c9bfb0df5402` | 0 |
| include/xrpl/basics/CountedObject.h | 2716 | `7e9c641d07719509668df7169e114874866246779676230822fa7ce38049dcc4` | 0 |
| include/xrpl/basics/DecayingSample.h | 3038 | `1a4e6a88b4fdac972d4ca7dc9cddfb504b6465c0455fdc412bcbc0efa0159be0` | 0 |
| include/xrpl/basics/FileUtilities.h | 1664 | `39202a281180d8051e593e67590a2b9b65f478d303b664a994e4ad61b40226aa` | 0 |
| include/xrpl/basics/IntrusivePointer.h | 14993 | `a2b2db1931510f1344d4d30d0d336e0928cfc3e320f524b358edea7bf3d356c7` | 0 |
| include/xrpl/basics/IntrusiveRefCounts.h | 17699 | `f02df248b84097b76fd5b19b2288d79cbeab604bfb0426b9ed9a02c15eac0d4f` | 0 |
| include/xrpl/basics/KeyCache.h | 177 | `76d12b6631e77eb3311d16448dab434459e0df8cf962eb8abf081df1c7200e9b` | 0 |
| include/xrpl/basics/LocalValue.h | 2132 | `16e1526c54f38191215aa8ca0228bf4e51574cd5a2fffb93875c42b2517ba187` | 0 |
| include/xrpl/basics/Log.h | 6134 | `648b6c5ef1fb1f05bbcac3f9968e448fcd8dccbe52b57dea823381284eface4b` | 0 |
| include/xrpl/basics/MallocTrim.h | 2775 | `a3018252d28f98b3c39b5caeaca2a862b1a6f7ff7f06e91127e1e61246d757ac` | 0 |
| include/xrpl/basics/MathUtilities.h | 7321 | `5e5ce5e05b9faca40f4f6b54299aa37dc27c4503e1464a1ec865f74a685078f2` | 0 |
| include/xrpl/basics/Mutex.hpp | 3631 | `7ae37dd2649ad8ac61aadbbcd443b4af333fa98ce52079740fc57d9bef26eae7` | 0 |
| include/xrpl/basics/Number.h | 29657 | `75313cc14dd41c346b04ea0c40bfe0c7c310b2d03ba661c467e726215027176d` | 0 |
| include/xrpl/basics/RangeSet.h | 5063 | `f57296393d55485989e7e25c87cbf827e1fc9a52762e55151e6f7c11e5759d79` | 0 |
| include/xrpl/basics/Resolver.h | 1024 | `bfbc8fdf2c18e273c97f349acc24fbc4dfc976352236ac3e4e810267dd618bcb` | 0 |
| include/xrpl/basics/ResolverAsio.h | 369 | `884ae1883816e7462fd1c15aa03f2c422c2cfa2e0ddae247a49a0b6d378cdcfe` | 0 |
| include/xrpl/basics/SHAMapHash.h | 1658 | `df1ba9b8cead20ba2a50c770184ac0a63a9861906ca947658e0812614a3754cd` | 0 |
| include/xrpl/basics/SharedWeakCachePointer.h | 3211 | `f8e4b359081f7a882e0ce367afacf006c3541122636c5ddf330fa11933906918` | 0 |
| include/xrpl/basics/SlabAllocator.h | 12173 | `854afcb75e39b58201fcc2a35c13207a243ba3cc265589d9bb2751083b381841` | 0 |
| include/xrpl/basics/Slice.h | 5417 | `0b8b2af39e6fab2ef8773934a2e5c8569937cefb0ee806cc1fdd454270fa3b76` | 0 |
| include/xrpl/basics/StringUtilities.h | 6416 | `44ab93a89d52996b2c71d4c7e18faba2d60916e862f01763737e1d02d56c659a` | 0 |
| include/xrpl/basics/TaggedCache.h | 14549 | `a731ddd5dc3d47f602928cd8d357a91f456324a15d7e817f97d36285fc502892` | 0 |
| include/xrpl/basics/ToString.h | 901 | `60e0826569279d2b64dd8963264dd20c01fd3e637f73006b8fdd56c6fba1211e` | 0 |
| include/xrpl/basics/UnorderedContainers.h | 3052 | `4004e270f76bda8b308fc35d04065203736d6dadb8417279fd09978cc554743c` | 0 |
| include/xrpl/basics/UptimeClock.h | 1069 | `6ebfbddba552bc5d92fb7cce6772df8431e4fb4cf25fd5558c31c9c756fdbcfc` | 0 |
| include/xrpl/basics/algorithm.h | 3220 | `beab007bb00eb411dd4c305aa3ccdc3b1c6b92a99c852b24ee883b658c6e0135` | 0 |
| include/xrpl/basics/base64.h | 2294 | `d946038151200614b9dae80d7caf3a54df49d7d5e1659fbc38268965fbf85a85` | 0 |
| include/xrpl/basics/base_uint.h | 18475 | `f0ca5725df46e15859e036db136ac06777db35170071d638b8ffc4814afd2d93` | 0 |
| include/xrpl/basics/chrono.h | 2644 | `d81531bafbcb8b0bfcae52b447c38b4c09c9e8cb1b3c8fc241f2c916e4481eef` | 0 |
| include/xrpl/basics/contract.h | 1670 | `c4ad5ea043db94cedf19caf03ff46584d414d01e7ac5b57a71517ae6eaac1ecb` | 0 |
| include/xrpl/basics/hardened_hash.h | 2050 | `1732bdf0e87c2898bf025e6cd5f8c537c579b47c37142fc08cb8c938811813a0` | 0 |
| include/xrpl/basics/join.h | 1975 | `355c6e0542cf33b9fe1b83a547ab8c1c773252a81edeb002fb042a2532a8bf7e` | 0 |
| include/xrpl/basics/make_SSLContext.h | 577 | `217ecc7cceeb1118b51886de00692b697f6edcba94a4841f2e518ad89df6009b` | 0 |
| include/xrpl/basics/mulDiv.h | 566 | `15bca85930ebb4df083dcc472804e0cebce4b356ab538844e157a33f7d4a831a` | 0 |
| include/xrpl/basics/partitioned_unordered_map.h | 7865 | `ca5f91510b9989725aef9222d50579e6fa074f8b31127372bf462036dcf316b1` | 0 |
| include/xrpl/basics/random.h | 5277 | `48e265f464eaf85c643c39768028b47bd7cb3af099907998543b6d3c089198f9` | 0 |
| include/xrpl/basics/safe_cast.h | 3396 | `85869c686a814e042e39dd3866de2e3a7e04f930aaf646f4aac3c39e8ad7bf3d` | 0 |
| include/xrpl/basics/sanitizers.h | 465 | `f43af1ae67b36529b9e140060a71f233a1036918336ad466e2e0076115547396` | 0 |
| include/xrpl/basics/scope.h | 5771 | `6fee846a13db60c7d431108700f4a3c7075b66e84ed9b6dfcee2e84b9075f939` | 0 |
| include/xrpl/basics/spinlock.h | 6421 | `2ca224a961fa4bf6fe475a337358949a4960f9a89bcc9b9ac166cabbf765431d` | 0 |
| include/xrpl/basics/strHex.h | 751 | `83d76c176960c437133f79d919c51484386ab4732b3df84f25b1bd4b069bfd12` | 0 |
| include/xrpl/basics/tagged_integer.h | 4574 | `532501d02dae23845bb33e75ca6d1e3b1dd94f5831fdd352886ec907fddded78` | 0 |
| include/xrpl/beast/asio/io_latency_probe.h | 6063 | `a2cca90253b52cbc81124580b683bbbda4bb6e6fb28e416c0e526672137efe9d` | 0 |
| include/xrpl/beast/clock/abstract_clock.h | 2254 | `65e4b0bc4090d5791691e80099ac1155d4ff91b84e5e5146930b2dd61b5d47d6` | 0 |
| include/xrpl/beast/clock/basic_seconds_clock.h | 859 | `8ab86d0573cdf96e5512ee05c6692df8d245b578a031cddab0a52e6e290e9e07` | 0 |
| include/xrpl/beast/clock/manual_clock.h | 2014 | `9bcd8ac2cdfddd824e97eae9ef41ee4afde32464104ebbd879cf66f98f034d68` | 0 |
| include/xrpl/beast/container/aged_container.h | 187 | `052d80964eb84a09fe5816e19dd12ce984e78b4b6d21b2aabb81cd6b02dcd1e4` | 0 |
| include/xrpl/beast/container/aged_container_utility.h | 655 | `660a6fb05298dbedaa9e0b358aba714b243ce52fcd7ce73039500990fe2b5c07` | 0 |
| include/xrpl/beast/container/aged_map.h | 476 | `1252ec97751300d6ccb227153c7a20b732c9654f8c9078b6b565ea46ef6469ae` | 0 |
| include/xrpl/beast/container/aged_multimap.h | 480 | `e4f8a2de61639e5470d78f2de861d2c036f996c30e6c6e39a492b08f93b8828b` | 0 |
| include/xrpl/beast/container/aged_multiset.h | 436 | `3f2c475a8bbb7d725bc7e64cbb01dbd02d765a225105f15b4d00195262f1a300` | 0 |
| include/xrpl/beast/container/aged_set.h | 428 | `108af6de9740b3a0a131b6f99b677d2aa81dd10f296a6d7033d4817a006f16ce` | 0 |
| include/xrpl/beast/container/aged_unordered_map.h | 538 | `48b7817ea5fcb86aaf9868cedb73e272184f10eb571c4fdfdfeb46907dac6569` | 0 |
| include/xrpl/beast/container/aged_unordered_multimap.h | 542 | `3134d78b3abd388ffd2ffbaeacba938d5f22311cfbd4586e1f22f3306af495b4` | 0 |
| include/xrpl/beast/container/aged_unordered_multiset.h | 494 | `994e3e0103e1c5bbb6d187a3864d52a1f6bf9d9ace89b8ebac23a4e855004d7b` | 0 |
| include/xrpl/beast/container/aged_unordered_set.h | 490 | `13fac6dc515727a56598f17f20ee9ab475026bd01577605866b7383d5fc25273` | 0 |
| include/xrpl/beast/container/detail/aged_associative_container.h | 678 | `ccb8fa3d29d2002032ece6e76b33cfe42af407aa0d970319dad77c69c03f4720` | 0 |
| include/xrpl/beast/container/detail/aged_container_iterator.h | 3551 | `27a048951e94670f9486c3ee57b1c5b2211770fe14de02befa82030d2272ab13` | 0 |
| include/xrpl/beast/container/detail/aged_ordered_container.h | 55473 | `a0857cc1a4e78daeef6a96335709a1445d683aa09675ae44e0d23a91e6b286ef` | 0 |
| include/xrpl/beast/container/detail/aged_unordered_container.h | 73131 | `8f5a6ea200e42e7173a9e059517b6f3a2946f576842c835ebbbaee3a5b5f4700` | 0 |
| include/xrpl/beast/container/detail/empty_base_optimization.h | 2174 | `1f67fd50dbce7b06e42477d97f1a0a95b546e0e98d532e89c282ae7a22857ec0` | 0 |
| include/xrpl/beast/core/CurrentThreadName.h | 1641 | `69ccefa0ab7c8d93a87a9bdfd9e3bad08308e72c6a4163bd4fac066abbf592b8` | 0 |
| include/xrpl/beast/core/LexicalCast.h | 5370 | `0d8ee49f70c3edd65f9d93c71052027147f24372e04b65f99958465003a63ac5` | 0 |
| include/xrpl/beast/core/List.h | 14359 | `4bd8060a76537b4bf1f064cbf3a0d957dac6083da4f3c40df8e2de04e586aebc` | 0 |
| include/xrpl/beast/core/LockFreeStack.h | 6749 | `813d94ce4a73eb59b358d2f63f29dbef91f192246631ce3451db54558c4b02ba` | 0 |
| include/xrpl/beast/core/SemanticVersion.h | 2035 | `744fdc9f5c0db58145f90886af2867a28be274321f23a642140f1deccda57dda` | 0 |
| include/xrpl/beast/hash/hash_append.h | 12351 | `0929a2affdff1f5b7b25d373b6631f2c1b6d011443bc556280dbc25f76d53d2a` | 0 |
| include/xrpl/beast/hash/uhash.h | 468 | `f574f39ef110f889f8ac890b2a9fdc42979c2e8de56358709bce198bcb87e142` | 0 |
| include/xrpl/beast/hash/xxhasher.h | 3389 | `535a59f5e755dc17fe3aec8b735fd3706cc8d440cb832f773d8d8abff2fac1be` | 0 |
| include/xrpl/beast/insight/Collector.h | 3000 | `42b392970aa6e67948c702ff614935f52aac1f54d4e9a844c9021fbb0285e7e7` | 0 |
| include/xrpl/beast/insight/Counter.h | 1896 | `dd3d66005ba6220883ce66ad3aca142f9f56df42880db7cca4ec328fb9cafd90` | 0 |
| include/xrpl/beast/insight/CounterImpl.h | 335 | `0aca2b4301306c316de452e75d17bd854ee7ef0f8b45bfb8e6a98846e608a34f` | 0 |
| include/xrpl/beast/insight/Event.h | 1523 | `32fb7c541a3b0635b171fc84aaa50c903fe41f94460aa3ef6bd6bb8257fa41da` | 0 |
| include/xrpl/beast/insight/EventImpl.h | 342 | `33d2f93d5570bd09090f4b8b460c1b9c38907321f1d499c5cf7a42587989ac8d` | 0 |
| include/xrpl/beast/insight/Gauge.h | 2962 | `079dd6e8ac8b3ebeeedbb7394e8db1b0566cbb38352f95c1a402b604c04c0613` | 0 |
| include/xrpl/beast/insight/GaugeImpl.h | 423 | `20c8adafc1f9c5eeacf7e872781f85f43c1f5cfcad07485a18917dd3a1681410` | 0 |
| include/xrpl/beast/insight/Group.h | 444 | `668d693744d41b49cbf60b8f4a3fceeb1556916a633a2afa2e841876c2b9c990` | 0 |
| include/xrpl/beast/insight/Groups.h | 717 | `f75a46334dc52df88d2d5945c70ec83920d73385ab4a9693715a5b69eda7816a` | 0 |
| include/xrpl/beast/insight/Hook.h | 834 | `f2661823c002cc1c3045d4ef09f36a2c62e0d3e42be861af911cf3d83f4d8511` | 0 |
| include/xrpl/beast/insight/HookImpl.h | 268 | `af8a76b4b897bbe76500be0f53ad24dac44e244a7e4d0b7b0a3618040436e99f` | 0 |
| include/xrpl/beast/insight/Meter.h | 1596 | `fbc25f41766a43e5d365f570a16837cf3d0e5580fa6ea16adac6273c675436b2` | 0 |
| include/xrpl/beast/insight/MeterImpl.h | 328 | `1b31508a66c59eb81e64366a425ac24d301b44fc23c139245dcbae45c1c08309` | 0 |
| include/xrpl/beast/insight/NullCollector.h | 334 | `f2d400627d5eb6674362a1a9f3f4af3f6441afd98650b0bf93e778ecb1c715ef` | 0 |
| include/xrpl/beast/insight/StatsDCollector.h | 813 | `2695573a23ab377daf817e35665865cb251013ff253ea9e39e42cd7c317828a8` | 0 |
| include/xrpl/beast/net/IPAddress.h | 2251 | `4b4c534aa3ebc32d8dfeea5703d2ff2000672cdd66136eabc9bf5ecf925d8e63` | 0 |
| include/xrpl/beast/net/IPAddressConversion.h | 1288 | `47a26beb2362cd6e93d81e8b59e10f9fd8d4d63d170a61f12cc2a02a6fdb1dd9` | 0 |
| include/xrpl/beast/net/IPAddressV4.h | 541 | `6511cb7fe239e096ece5eea498adfa1a8a876dcfed4d753986a943f8681bc1be` | 0 |
| include/xrpl/beast/net/IPAddressV6.h | 376 | `27b027e4e1cfd5c3837c9f06e8ebade10cfbd77f1b02abc46c763991bf75aa48` | 0 |
| include/xrpl/beast/net/IPEndpoint.h | 4948 | `f299c6fd9e2f54f74600303438542e01ef6208523d306a6c61448ab655252b24` | 0 |
| include/xrpl/beast/rfc2616.h | 8396 | `22f9930cd98fe4a7afaaf3d21aaa0ce038f1e5be0b03f0c4f3986d079670f87b` | 0 |
| include/xrpl/beast/type_name.h | 813 | `77b5be70d7a289e611e180c08b5b429fd577b31a165b387ea360c8d86182f4ab` | 0 |
| include/xrpl/beast/utility/Journal.h | 11313 | `2ff4b305e6ecde4ec229617466527dd989cc790367e3943f24c59792b7e15b13` | 0 |
| include/xrpl/beast/utility/PropertyStream.h | 9656 | `ea5a8da357d48f93f4411eddf79421f193aa7086ebf5c8dd2fa26817298e9595` | 0 |
| include/xrpl/beast/utility/WrappedSink.h | 1801 | `ff7311123471b5800bdc3540306cb237cdc8a0ff2057e6b6cac49161dfd2d8ba` | 0 |
| include/xrpl/beast/utility/Zero.h | 2717 | `2661708b3f85d12f12b0a5472daeaf22a4820ae270437541db460cf39659b3cb` | 0 |
| include/xrpl/beast/utility/instrumentation.h | 3243 | `0a1eb337e2327441c342b4e30979235defb9d0d4beceb197f32fe9d112717288` | 0 |
| include/xrpl/beast/utility/maybe_const.h | 480 | `4dffed86008e1f1b9594f674383a3940a0f80baef1e1199bbbb4ef70750a20bd` | 0 |
| include/xrpl/beast/utility/rngfill.h | 1303 | `da3fe4ae79ff459a13b6b18616b4f94ef462ce84cf1b725cc42f34a0e0d95682` | 0 |
| include/xrpl/beast/xor_shift_engine.h | 1861 | `61edf233c14998a5a066aafae6f201802a30b311e3003ef43a08e459957c3c76` | 0 |
| include/xrpl/conditions/Condition.h | 2273 | `dd5fc1e19b9bdfefccec54d609656afe1ff5e03d63f104dba5c661c5339033d9` | 0 |
| include/xrpl/conditions/Fulfillment.h | 3569 | `c48b8cd933c8f09dbe00f007f3315fce3387caee9a09613f4b0e5a23f9f2b3e9` | 0 |
| include/xrpl/conditions/detail/PreimageSha256.h | 3152 | `f6c2a11b9a596ccc9d812cd266a9c5b2764060a2e49adc2ad0462e16b964fb7f` | 0 |
| include/xrpl/conditions/detail/error.h | 750 | `af2dc39e109dbff82ffd7e61f5253844d4dc5a70e77a8923e670e79d3beeb557` | 0 |
| include/xrpl/conditions/detail/utils.h | 4011 | `ee793753b0e5a17bf81db7f709d586b151aa710bb3c10cf0ca97d7334db45c7c` | 0 |
| include/xrpl/config/BasicConfig.h | 9638 | `61a8d0b7e99341d8a58ec69e8ce075f32ecdc903feb9ba46f5c2c8dca244b9f3` | 0 |
| include/xrpl/config/Constants.h | 10382 | `0c62d954e64474794107fef102f5b906df0e47a56e8d95c77195e4f3b3a740ba` | 3 |
| include/xrpl/consensus/CensorshipDetector.h | 3557 | `68f0957825da9a9375f5b217f7685abcdbd3d5e52ee72e5e40343aae16ebe539` | 0 |
| include/xrpl/consensus/Consensus.h | 65721 | `4684058cb3639651ce2f52e52d21fa661bb3760f9f39d7dc4f4f06132cb4fc6d` | 0 |
| include/xrpl/consensus/ConsensusParms.h | 7765 | `8ed966c4354da053b4c820d2c43395e95ad7163011327ec429db9324f2c5e1ad` | 0 |
| include/xrpl/consensus/ConsensusProposal.h | 7755 | `4053aef6fb7448fc89901e378c6ae870bf4478e79df1a86a348223867db076db` | 0 |
| include/xrpl/consensus/ConsensusTypes.h | 9033 | `55f898ad17863915f42cbf65862ab47eec18928ca32678e8e1b6e31804614205` | 0 |
| include/xrpl/consensus/DisputedTx.h | 10615 | `32183c81856f63753c8c4abb374b55aea5f541c3690b87da5e9b04091858faa1` | 0 |
| include/xrpl/consensus/LedgerTrie.h | 26815 | `04146e9bcacf6f4f82ce7c344506e4a4f8de608ca0b6db26b5f878cf9ecdeeb6` | 0 |
| include/xrpl/consensus/Validations.h | 38702 | `b56a2b26f9a16d120d3001c286b83712cad42f73127b84f2898cf0f383c265c7` | 0 |
| include/xrpl/core/ClosureCounter.h | 6626 | `0c6707f69a5379fd6d18fbc371810a420ce8c263d9a126252aa2c04fcec90bab` | 0 |
| include/xrpl/core/HashRouter.h | 8398 | `79810a5efb1d9aa08495d32a7f8c9389fa9e230a4fffffd7e83df38f7b72e0a0` | 0 |
| include/xrpl/core/Job.h | 4744 | `1aea5df2daba62f1fe69c916514a13caaffbee7095dfe5cbfaa517bf2d1fc787` | 0 |
| include/xrpl/core/JobQueue.h | 13974 | `2fa1f493152648f4720745ebeff71d0fc92778bc86027748faae5efd2284c2d2` | 0 |
| include/xrpl/core/JobTypeData.h | 1783 | `da52292ba9821a68b0b9ca663f1b2b7feddc207f7f28a892440ea8464196e05f` | 0 |
| include/xrpl/core/JobTypeInfo.h | 1670 | `8c8f332df66eb48fec5f2e5d55794ecdb25e43f0debc068062e736def1859851` | 0 |
| include/xrpl/core/JobTypes.h | 6752 | `1de98fa8420f4bd37d59cc79f374bd1c4b8acc5f21799e4ae2fc91eb6c069249` | 0 |
| include/xrpl/core/LoadEvent.h | 1607 | `50ed1902c2df432bb5aae7cc29fce8484c546a81d4ca816d541619cf5ff7d7de` | 0 |
| include/xrpl/core/LoadMonitor.h | 1429 | `cd3214b2f5b4bb168a73b4751b3479d088c980e3b1b3ab21529199f98c2ef5a2` | 0 |
| include/xrpl/core/NetworkIDService.h | 786 | `5ea34339acb8c0017a48a780b9d604cd3ae0b03486bbbeed9f1f3068fa1a7a9d` | 0 |
| include/xrpl/core/PeerReservationTable.h | 2485 | `0b905260c1342fa4db69d4b32db2f0d21dc8c3cf171ef9a0c112c9ef30b86887` | 0 |
| include/xrpl/core/PerfLog.h | 5074 | `2deb651a37b25c70110140844aab52b548f63326a284d57b57154ce8b5fb38b4` | 0 |
| include/xrpl/core/ServiceRegistry.h | 5374 | `ea1fc676bfab71803fabd6a0c1708bd7cd6254029d0ac700e656e0c1e7ee8517` | 0 |
| include/xrpl/core/StartUpType.h | 325 | `69f5829eb08e96111bf53b63527615f034242868d6cd05118bf5566589de9fc7` | 0 |
| include/xrpl/core/detail/Workers.h | 7286 | `b6e540f9f918baf0e813508143a1a6d979ea97ac8ea7f514cc0d965c22d748b9` | 0 |
| include/xrpl/core/detail/semaphore.h | 2248 | `9575ba7fd085d295ddc2ec469995d2d2a4eca92d33c4db8be7e03dfb8cd917af` | 0 |
| include/xrpl/crypto/RFC1751.h | 1209 | `ca9563cd386c3a541a4f19b79040200f5c3ea03a15f851a1211edee028b597b8` | 0 |
| include/xrpl/crypto/csprng.h | 1721 | `b5462fcc0e88baf9d3b1e296e8f088a35b158d79ceb5f59f1311ec064b3a4a49` | 0 |
| include/xrpl/crypto/secure_erase.h | 713 | `e4fbb0aa8f9ab163683a56fe8b681e3199cc788e5cac8c4394e2a083514ff4dd` | 0 |
| include/xrpl/git/Git.h | 157 | `4e62085f2edcf42c032a8508ccb45cc88a99798623db54011779736f80976076` | 0 |
| include/xrpl/json/JsonPropertyStream.h | 1653 | `1495ea8b1596565bb2d0a9274401a1d5da461a492a1cf414bcd4a02cc85385f4` | 0 |
| include/xrpl/json/Output.h | 290 | `6c16fe33e7d93fb8dcb8bcbde6030208dd471b009593e833f508f80738f5e9ec` | 0 |
| include/xrpl/json/detail/json_assert.h | 157 | `18e8a724f6bb87b7e03ee60bfeea5d12e73ecb706d1aaaf35143d7dc0d099564` | 0 |
| include/xrpl/json/json_errors.h | 160 | `3b7a68d20b10d5c6ac07741718d8ab4d4c4292c36c67e2e79c5296151aaedb87` | 0 |
| include/xrpl/json/json_forwards.h | 214 | `75fb649e6479a6c82ecd3033e676ac44b4ec9fa599ce0387c3787ec7d5fc1e50` | 0 |
| include/xrpl/json/json_reader.h | 5703 | `23690e3fd1311dbcf2299cb5ec8c91f7f4d0bea1b127ec770e49883704e3f3b5` | 0 |
| include/xrpl/json/json_value.h | 18847 | `1ee20e6b8110bffae1c4bc562e2ba39f47892557beb45072cdb5acce0a8817ff` | 0 |
| include/xrpl/json/json_writer.h | 8483 | `dc15a1ebedecf857e162d32494f69639b5943148e5d064d19903fcd113601729` | 0 |
| include/xrpl/json/to_string.h | 283 | `0a869070a8faa63003bcf4954342614cf960c96d2d1d18196a13fb295f8c98a1` | 0 |
| include/xrpl/ledger/AcceptedLedgerTx.h | 2167 | `a32450db06fda52e071e79e87f792e82aa2183787b89a37d563c6c0c7bae48ba` | 0 |
| include/xrpl/ledger/AmendmentTable.h | 6585 | `c2c527819e7b618af14552cf9047b0bbde013176b69051cbd8c84467b2bf7c80` | 0 |
| include/xrpl/ledger/ApplyView.h | 15700 | `743c406464b490703ce61aefec2f826b4ca406eb7ec4179c5879484227ae3e98` | 0 |
| include/xrpl/ledger/ApplyViewImpl.h | 2189 | `bc932c25deeafbdd5edad8b72d1447ea85392bc374e1665ff032416a4103b5d4` | 0 |
| include/xrpl/ledger/CachedSLEs.h | 218 | `0004f82ce28bfd9be5e06e88297d30cade21990ffd61847df3084f18d62688c9` | 0 |
| include/xrpl/ledger/CachedView.h | 3501 | `4b3884f5a587f1730603b934a3a0200dea9b6915c07b049f7aabb861ffdae1fd` | 0 |
| include/xrpl/ledger/CanonicalTXSet.h | 3410 | `9e9f6f5b740aeb2ce5d26b71a313b9042992afa55b4bc75049831a061e22b336` | 0 |
| include/xrpl/ledger/Ledger.h | 12319 | `d8b79229e9e8710519a402babcb390eff4aa7c5fa1b2c054a59a844125513c1d` | 0 |
| include/xrpl/ledger/LedgerTiming.h | 5437 | `e15efa79e8a82de4ebcaf388e0ddb4b9ec34875157cb83deb6fb6f253ed4fa46` | 0 |
| include/xrpl/ledger/OpenView.h | 6722 | `260fe43f79befb010151419a9e948c21affe329c56bbda741fd54687f586fc6a` | 0 |
| include/xrpl/ledger/OrderBookDB.h | 3552 | `3e57fc01d0bcc675fd550bf64fb6f7e88c593ff36ca03c2b705ae08dee37d1d9` | 0 |
| include/xrpl/ledger/OwnerCounts.h | 2097 | `adde131eff8baddb5eaaa569202ad0cdfff189734bd2fb7fb2bb8829b064cf2f` | 0 |
| include/xrpl/ledger/PaymentSandbox.h | 7738 | `52a2ac06fad289e14ac4b2aeb2a9aa499968663d27f2dd31799370f0cf11847d` | 0 |
| include/xrpl/ledger/PendingSaves.h | 3004 | `205b66b0a67469b506845708101d39641ee5641335060e7e51749cb163f05ee9` | 0 |
| include/xrpl/ledger/RawView.h | 2111 | `606d80f54710a452336b78f0bd2d094e87531f33dcbd3bdb6b1375c15977331e` | 0 |
| include/xrpl/ledger/ReadView.h | 8740 | `862344706754c2bd40091531277d3608d0f2c072e9089306b6fd10c27314992d` | 0 |
| include/xrpl/ledger/Sandbox.h | 851 | `526c71520fb3dcee0f45b6d24669b786c57132ee4ef37afb89462f25b865637b` | 0 |
| include/xrpl/ledger/View.h | 11195 | `a0ba8a40019e8ed0c20bef3f4f9aebc82f16c5f72d691aaf1159580d7b29b5af` | 0 |
| include/xrpl/ledger/detail/ApplyStateTable.h | 3211 | `4092cbaad6af11d1a37ba0dd89ee857b754dc9f730d9791e1cc30fb19e7f0b8c` | 0 |
| include/xrpl/ledger/detail/ApplyViewBase.h | 2619 | `ac3bba5f4573551925a2d8b9ae2d24eebe5fca4a56b54b3444cb598b112684db` | 0 |
| include/xrpl/ledger/detail/RawStateTable.h | 3411 | `4f44a693e08e4fe8c4bd3cb5a7a7da35db2ebefc3a5b97620ed6c1f82bc9e74a` | 0 |
| include/xrpl/ledger/detail/ReadViewFwdRange.h | 2752 | `2861608bfe27cdee440cd5092c2eb852b20e99dda5c5c1d22595fb5946128fde` | 0 |
| include/xrpl/ledger/entries/AMMEntry.h | 1155 | `67ca072aca59bffca13f427e4da38ecb532662ebfea81bebaa0921fda9327804` | 0 |
| include/xrpl/ledger/entries/AccountRootEntry.h | 937 | `f8a4a6243644138ef7831dbcdc28335dfe9faf99fd896b1fcd9a1a65c4082dc7` | 0 |
| include/xrpl/ledger/entries/AmendmentsEntry.h | 2284 | `53d7235b537e404211909f21606b1633e701aa33917b557f06caf8a57bc29e4e` | 0 |
| include/xrpl/ledger/entries/CheckEntry.h | 1214 | `2db2ada4008881c779cbc33831670f982e0b9d4255c91ee484b929bb95d89d3a` | 0 |
| include/xrpl/ledger/entries/CredentialEntry.h | 1332 | `88c828fd3cbc96ba6e2839126a2f1d9b237130373c5d2d173c78193cd2f464f7` | 0 |
| include/xrpl/ledger/entries/DIDEntry.h | 877 | `37c8b0020ca4312b6c8a7f623bc02f6bfda97517b339d55ebf4f2afe4f6b05ad` | 0 |
| include/xrpl/ledger/entries/DelegateEntry.h | 985 | `12c883bf5a43bb1dc9220a75cd9adafc76364ea732b8839fd62c7ddcd0bc6d2e` | 0 |
| include/xrpl/ledger/entries/DepositPreauthEntry.h | 1691 | `0c4d9d151e702fed207264c47aefe5d382f6423de9e7455c39fa6e22d27b699d` | 0 |
| include/xrpl/ledger/entries/DirectoryNodeEntry.h | 1341 | `9146a09023c31ec34965d908f814b2f33b9c759d1b0ae33d35958230bb0fbbfb` | 0 |
| include/xrpl/ledger/entries/EscrowEntry.h | 966 | `4364944a4d73db31f552f3ed44e69fb6842adaaca194dd4fcf92de88f38a0e98` | 0 |
| include/xrpl/ledger/entries/FeeSettingsEntry.h | 873 | `e26798bdc688a57bd56ee647accf4f4adabf1c42713223daefe0a6e8717db083` | 0 |
| include/xrpl/ledger/entries/LedgerHashesEntry.h | 1996 | `2b7b9103b3a74300b10fea3e315668d7cc8b5a37e2b4b4aee9a3da83bf7447d4` | 0 |
| include/xrpl/ledger/entries/LoanBrokerEntry.h | 1287 | `f64834364276dfd5d4e8acc7062f76aeb4981bc8667361f5f751fea4fa723150` | 0 |
| include/xrpl/ledger/entries/LoanEntry.h | 1190 | `ac24d0733dec1f8cc9159ed4712bda51e2b34bf829dea90898c12feab12b19ac` | 0 |
| include/xrpl/ledger/entries/MPTokenEntry.h | 1539 | `32c69af9ba872888c866a13c51f2ca644c2b7ac0b026887f836c1a8c751318d8` | 0 |
| include/xrpl/ledger/entries/MPTokenIssuanceEntry.h | 1620 | `fa5a1d176b44c209806750018197900280b7e339287df5052be8400b164aef53` | 0 |
| include/xrpl/ledger/entries/NFTokenOfferEntry.h | 1299 | `e2ab0c3694963f2247dfaf8ac4df3cfcffe2d8a9297c41386d93a9808de32cf0` | 0 |
| include/xrpl/ledger/entries/NFTokenPageEntry.h | 1011 | `92653f553dd35b0347f353d7318e0cdb70ef36e938b4a678662a52792f97c3ed` | 0 |
| include/xrpl/ledger/entries/NegativeUNLEntry.h | 873 | `87084328325dd8e60b7c31215f9df45f80f699aec91bc4e36a353aa7fb521c39` | 0 |
| include/xrpl/ledger/entries/OfferEntry.h | 1214 | `0379f5334237f6a8526d696ca951e04111f975eae3b23f600dc33763b5ceee21` | 0 |
| include/xrpl/ledger/entries/OracleEntry.h | 970 | `9defda2a5255468999480435231f8ce368506141685ce2af5f6f2073ff506317` | 0 |
| include/xrpl/ledger/entries/PayChannelEntry.h | 1031 | `af8b26d26f1eb6d4da846b038927a656775b632469efc3845aa06c1206c62b4d` | 0 |
| include/xrpl/ledger/entries/PermissionedDomainEntry.h | 1371 | `b978cca20f4394d6ed26a584d274dc64c99695b2075862f2647fd59ad8225ba8` | 0 |
| include/xrpl/ledger/entries/RippleStateEntry.h | 1351 | `cf326907514b6c599cdd89765e30dc34e2d8210ff09d6fc4b85546f749b6c4e0` | 0 |
| include/xrpl/ledger/entries/SLEBase.h | 16648 | `7307a18e59f784aee9a2c555ca945407a90711987a1e670df847510cef3d2813` | 0 |
| include/xrpl/ledger/entries/SignerListEntry.h | 942 | `ba3f67509e1ce636f7a972cf66eaf0bb744369d0a869361067f56939094c6e05` | 0 |
| include/xrpl/ledger/entries/SponsorshipEntry.h | 992 | `1f94b67ab808e22eef154fa3f38b62447f41716dcea02f6ab8d477115d3c8d29` | 0 |
| include/xrpl/ledger/entries/TicketEntry.h | 1239 | `fb5f5315f5e153c3a3b5185988aae0caed237741160cd4a026306aef110f1e8d` | 0 |
| include/xrpl/ledger/entries/TransactionProposalEntry.h | 1086 | `4662e26cb3a09c31aa87741a894eba0af5085d7947d5683599443e89ef68232a` | 0 |
| include/xrpl/ledger/entries/VaultEntry.h | 1220 | `d7e286a6d71eca3fe703f9e181a76f777d69d4ba9da52222074da64f9b10fae8` | 0 |
| include/xrpl/ledger/helpers/AMMHelpers.h | 28278 | `aeed41445285de9ade3144b3a1cb7a04a53a8f6af1bc3bd7fed0506ed78adb32` | 0 |
| include/xrpl/ledger/helpers/AccountRootHelpers.h | 13084 | `ea5098edb5a8370e76dae898820272f5d10d84765192f3bd040fb56dfc77eecb` | 0 |
| include/xrpl/ledger/helpers/CredentialHelpers.h | 3952 | `78ffa62185d62436ac0bf77efabfa9678059bc87004851caebe80aeed5fde58c` | 0 |
| include/xrpl/ledger/helpers/DelegateHelpers.h | 1065 | `a83d1f6781987ffe63af132e946e73a170068074d17981d03f3ad786938eeb2d` | 0 |
| include/xrpl/ledger/helpers/DirectoryHelpers.h | 5675 | `5239659c72b38b018a79b94af40399acac298b9b8f55b4b8ce1ded046890d8cd` | 0 |
| include/xrpl/ledger/helpers/EscrowHelpers.h | 20312 | `280d8c83b2f013dbb9911489e882d6a9aad879d01a72da6299002347cbf1e030` | 0 |
| include/xrpl/ledger/helpers/LendingHelpers.h | 26861 | `51a983b5e77abba13799aa23bb854804fd4ab8529fdc287a77410ba103fec5ec` | 0 |
| include/xrpl/ledger/helpers/MPTokenHelpers.h | 13084 | `ba625da8f0341b5d3e5777f04659dd7275142d0efec2e7f024e7127cf5cb109d` | 0 |
| include/xrpl/ledger/helpers/NFTokenHelpers.h | 4210 | `4f9116ee9eeb3922020fa58fc5f29814ac261ac4ba60b3a8ea25cf825bbd0af5` | 0 |
| include/xrpl/ledger/helpers/OfferHelpers.h | 656 | `bf0c34657403f83b590b8de6ff7a6a7bfb07cc346cfc292f173b1ac785d4aa95` | 0 |
| include/xrpl/ledger/helpers/OracleHelpers.h | 866 | `348b7b5389c515c75572db145b2ea94c73f128ea1788bdd2c61f146ac4817910` | 0 |
| include/xrpl/ledger/helpers/PaymentChannelHelpers.h | 1915 | `dd8367a57740b3207da42ffe42173016d1a72e712e6dd40fb1edac37e580ce22` | 0 |
| include/xrpl/ledger/helpers/PermissionedDEXHelpers.h | 624 | `dc14a6685d650381c8ab30e83c7ebe4b4c5e66a39bcb6f2b9303ad4625e6db92` | 0 |
| include/xrpl/ledger/helpers/ProposalHelpers.h | 7154 | `22fd175e8cd0331957d38d0259d04f6df0b89c24de56a9a1fd8b1e93aa4af24c` | 0 |
| include/xrpl/ledger/helpers/RippleStateHelpers.h | 8684 | `7f937613c96cf9d0b279f7f7666fd3d4bc4127af8f7e13a4ccd9e46af91aa39e` | 0 |
| include/xrpl/ledger/helpers/SponsorHelpers.h | 7157 | `2cc9953456fcb31183e67d7e1cf81d25e7452d673aabc0051e11ba8e201af3b4` | 0 |
| include/xrpl/ledger/helpers/TokenHelpers.h | 14864 | `ed541612ac4f59f4ca7b6379edd949b0890087b27653055132aebc35a16a025f` | 0 |
| include/xrpl/ledger/helpers/VaultHelpers.h | 24082 | `4a043cc8a2662bfcf5c778fb3645a48adf17d278be80d82724b1d11e9915f5cd` | 0 |
| include/xrpl/net/AutoSocket.h | 8758 | `9259d43e56c31c1e4d30807df0c7826df521466157000b6efca83c12d339dc17` | 0 |
| include/xrpl/net/HTTPClient.h | 2674 | `3ecdbde1ebf868d830f45c68fb3030dcb46d8115579ea8c08b7fc1dd6a32eff5` | 0 |
| include/xrpl/net/HTTPClientSSLContext.h | 4680 | `b7bc9829e5600206a89e9654fecb8ee72b8db0c21247c94d0a182b3699d5d2fd` | 0 |
| include/xrpl/net/RegisterSSLCerts.h | 525 | `8900eec0c592234d27d7c1b913822f4bdc84c2a87907ee9d5915bb147fa0db2e` | 0 |
| include/xrpl/nodestore/Backend.h | 4376 | `549c400de93ab7fb14f193b4f4a94238e976500acc239d33b0a3ae5e5b23de0a` | 0 |
| include/xrpl/nodestore/Database.h | 8966 | `82ff8835b67407712199c074735d779c069e62f3355dbe20959a1370d2ff2e14` | 0 |
| include/xrpl/nodestore/DatabaseRotating.h | 1746 | `3cd2b26a87408a06b7e5a778a127ecaca6c38183b6813b587850e4e024838120` | 0 |
| include/xrpl/nodestore/DummyScheduler.h | 533 | `8c4d94420464eaf9b9919c08d65f7ace7c1ff91aaa5e0683c5de80a3889dba10` | 0 |
| include/xrpl/nodestore/Factory.h | 1830 | `e2c67d08df897f7a9663cf4e34d9a43ea84e9730727a6e86109f441382470a2a` | 0 |
| include/xrpl/nodestore/Manager.h | 2762 | `837a2baaaa3eb8473e3630a78964c1f166d24531fb1778d5899c01687f9ba0ca` | 0 |
| include/xrpl/nodestore/NodeObject.h | 2461 | `495740ae1de3578ef24525d8d63ff1c51b9b9bb19bdf1b4ff4eb687d50b47954` | 0 |
| include/xrpl/nodestore/Scheduler.h | 1602 | `388a4246c68c58c9769c581dd53391dd503320a8a54027730cde44257fa08559` | 0 |
| include/xrpl/nodestore/Task.h | 322 | `4df277e5ea57e57baba018ed557b6ee374d825292a69d4756df5f39674ba3e93` | 0 |
| include/xrpl/nodestore/Types.h | 832 | `3a05a301d286a7c385c9cb6253578a4f3220ee299a0585062a753cc3b2070dc1` | 0 |
| include/xrpl/nodestore/detail/BatchWriter.h | 1928 | `009d7840626f5394f744a32d60103e1852cad9d694c27b14c9a92103bc419030` | 0 |
| include/xrpl/nodestore/detail/DatabaseNodeImp.h | 3600 | `8215036eaddd5cc7fbd502db992effdda2533893967cb6ca788bce558510bd23` | 0 |
| include/xrpl/nodestore/detail/DatabaseRotatingImp.h | 2557 | `c0c4154ed3293e26682071e592facd7c1ae9d0a2cff1640db68c3238d98f896f` | 0 |
| include/xrpl/nodestore/detail/DecodedBlob.h | 1212 | `fd84faed151ed642d4d9e06598f3183604afa22ad4c9c3271f129b2dab392e0a` | 0 |
| include/xrpl/nodestore/detail/EncodedBlob.h | 3416 | `fa4c9a5cc7b0bce7c8abaa7776dd1a58f2bf71c801c6cdbd8f3af351d1d0d2dd` | 0 |
| include/xrpl/nodestore/detail/ManagerImp.h | 1190 | `fae241554183c579114a84b33fae1be6be142ef2166615d053e842aa4136c159` | 0 |
| include/xrpl/nodestore/detail/Varint.h | 2497 | `774374004c084d7216d2a53283dab58453067695b8d767fa50d89e6c3c9ae55a` | 0 |
| include/xrpl/nodestore/detail/codec.h | 10487 | `180b3a7b78749c347a3a69338567fde0294afcb38f09f9165752a7bfebedccdb` | 0 |
| include/xrpl/peerfinder/Config.h | 4208 | `9e61d667f3703d37654b8e8e045dc7944e24018ac347913eb53be1a2aee7614a` | 0 |
| include/xrpl/peerfinder/PeerfinderManager.h | 5178 | `698497a5de11d485d49d9e92d7ed2c8b26e0fc0143b80b22aa44b5dc6ba02a3c` | 0 |
| include/xrpl/peerfinder/Slot.h | 1806 | `3c6b33db23ec2cfe88126dce111fb333e79f771c977586d176226d7692ecb17d` | 0 |
| include/xrpl/peerfinder/Types.h | 952 | `4f6a2af97946588e663a60e02f785ca0f5b204ff51fd0ca86e4b46f14904e2f6` | 0 |
| include/xrpl/peerfinder/detail/Bootcache.h | 4483 | `349e7f858acb73f087e59a7385e0bfce518b47c17cf6b03b37de255dd02f7360` | 0 |
| include/xrpl/peerfinder/detail/Checker.h | 5010 | `d33c999621eb763e85ed660cb8a10ea92974b23f3be3dc1b567eefe5920a3bb9` | 0 |
| include/xrpl/peerfinder/detail/Counts.h | 9523 | `319ef6a573a6d9bd4eedb7241e3062ce2592c369d353882df2caae07504344d5` | 0 |
| include/xrpl/peerfinder/detail/Fixed.h | 1144 | `b3e1fa0f3b08284475c4f7ebd21c202553b7da7e028c8432beeafd1a477a33f3` | 0 |
| include/xrpl/peerfinder/detail/Handouts.h | 7842 | `cea37166f309ae904e837baa107c9fa8799075a9dce407ac44f188f915d41026` | 0 |
| include/xrpl/peerfinder/detail/Livecache.h | 14791 | `9fd5cb8f35e4e38052b2fb546c9178aa65d74bda327567ad3dfb1ba6adfe1e6a` | 0 |
| include/xrpl/peerfinder/detail/Logic.h | 40339 | `be76d83e7194a8c2cc1f10646509410b1502a536d1ea31f5babc2abf6ded3820` | 0 |
| include/xrpl/peerfinder/detail/SlotImp.h | 4425 | `9faad5388e0e76b8f84fc1d355d5c4fc0bf8b042903e92abfb8e40ffa6b7e342` | 0 |
| include/xrpl/peerfinder/detail/Source.h | 1192 | `d7aaf612a3c51f850b4fdd04b2c0edfe859542f0f40ddd502db5eb27b1d95fbd` | 0 |
| include/xrpl/peerfinder/detail/SourceStrings.h | 470 | `09d2fda58f9f051bc147a50b3f83c964cac5e70e29b4b1960d4ce47a30d08174` | 0 |
| include/xrpl/peerfinder/detail/Store.h | 678 | `9debc24d5022ebaf59177c87658e6e00c83cfeced89cecf96c52c4393dee8609` | 0 |
| include/xrpl/peerfinder/detail/Tuning.h | 3440 | `3e9cc70105218e963eef0dbe9a5804e4e4a355c54680d2a749c712dab05ce552` | 0 |
| include/xrpl/peerfinder/make_Manager.h | 1146 | `181b139f372ce841c579c410b3dbf06ff85718dd6785943b6b4d8d8d825e9743` | 0 |
| include/xrpl/proto/org/xrpl/rpc/v1/get_ledger.proto | 2393 | `61dbd75b6123f300159464222f3684ab7c8bd090fd008770306724df8345f011` | 0 |
| include/xrpl/proto/org/xrpl/rpc/v1/get_ledger_data.proto | 1677 | `3cae1bb3595562c5b8eb3cd992f8ea10447be606e0af06ff6244d24da03caeab` | 0 |
| include/xrpl/proto/org/xrpl/rpc/v1/get_ledger_diff.proto | 810 | `c9e9afd250e8429fe9b3023bc3debc6956047a79ce04ae875ef5b3637bbebd9f` | 0 |
| include/xrpl/proto/org/xrpl/rpc/v1/get_ledger_entry.proto | 719 | `8c3e29f44b4b3cad53dc688c5dc82dde362858a450e7d6e31c983e5b4d6f3a83` | 0 |
| include/xrpl/proto/org/xrpl/rpc/v1/ledger.proto | 1499 | `35f3bc749ded16dda6f7771bbad270b724eaee3e6a7f2dd2462fa6b905229020` | 0 |
| include/xrpl/proto/org/xrpl/rpc/v1/xrp_ledger.proto | 1281 | `04d1d21e8198cbd7a0100dfbe529a631c795d9ebf49d6f7ae8c2765fd0fc8158` | 0 |
| include/xrpl/proto/xrpl.proto | 9089 | `4d28515ea1ae503137b0d6e883a0cc8e0c21f43af99865ac92d7070cbc6f5435` | 0 |
| include/xrpl/protocol/AMMCore.h | 2982 | `021a65d3efda2fe0e2a9e7ac45d3ea4d89d46761f7a7e3135ea741bf2e47653c` | 0 |
| include/xrpl/protocol/AccountID.h | 3364 | `7aa793eb7d511189c38a591807355c529878250b8f6d18abc17c5625c81ccb8f` | 0 |
| include/xrpl/protocol/AmountConversions.h | 6954 | `f18cfe54538e303765730e5703facafc370ba26fcdb231997b8c1fd0dbed4cfc` | 0 |
| include/xrpl/protocol/ApiVersion.h | 6176 | `c1fc14534b75debbfb059e275245c20736af49853c2a6a27b7b45bd89bb9e660` | 0 |
| include/xrpl/protocol/Asset.h | 8541 | `01d9586da2e977e63127b1f69087934479dc276d232dfac8f88cc2f188a66638` | 0 |
| include/xrpl/protocol/Batch.h | 666 | `970a38e4e1ba5f6a7e1ff45daf22108c78e08032d15b26c8f36f7f5b2b1ddec2` | 0 |
| include/xrpl/protocol/Book.h | 5843 | `ef2b92da43a361a138e2ecb3dc5782c8f907590c08d3fd67dccc86d2c6c54ebc` | 0 |
| include/xrpl/protocol/BuildInfo.h | 2318 | `a6d3f729b05f1cfffbfc86a379184d25aeb0cae1bafe744896dc2d6145b9be5b` | 0 |
| include/xrpl/protocol/Concepts.h | 2923 | `0336b5ab6f2bebe644b88d1af0ed3c2d6d1b7010790b83ea075fe356dab42051` | 0 |
| include/xrpl/protocol/ConfidentialTransfer.h | 20118 | `03b875149e8aa0716dddb2ae6285f435e4aab8497bda3ad6bc9b21f98b4efa27` | 0 |
| include/xrpl/protocol/ErrorCodes.h | 8284 | `bc1184b7cbec9ac71ae49b36fa498797ff770497b04b6a60028103a399516edc` | 0 |
| include/xrpl/protocol/Feature.h | 12352 | `7973ffdbe96b64d9e1e47298b11328d14d4a776fb2c70d0f4531054aa76f4303` | 0 |
| include/xrpl/protocol/Fees.h | 3114 | `6052df99ca896cfb151b21408b4919c472f502d57224f049490ac48d5a159810` | 0 |
| include/xrpl/protocol/HashPrefix.h | 2978 | `d43eecad05fc5a8af1eb2cc4dcb443c458d8249f06addb8661a343348ee8c8a3` | 0 |
| include/xrpl/protocol/IOUAmount.h | 4038 | `741de0f39b3068ba6d132619723522c09701b044e5b21d933283769ab168866b` | 0 |
| include/xrpl/protocol/Indexes.h | 8863 | `bce9a9465c611a9b54e0bc09bb94efa0307c2fc7bc33c5ef81bb94a17e2413eb` | 0 |
| include/xrpl/protocol/InnerObjectFormats.h | 612 | `3206f420866e61efb8eedd5d26ce9af2edab3e73c493020b0cc1aa2c8238ac76` | 0 |
| include/xrpl/protocol/Issue.h | 2361 | `2f9ca987af52f6cabd23de114ccb37bfd469bce471c9549a1789cffb76f4b040` | 0 |
| include/xrpl/protocol/JsonRpc.h | 457 | `4d683d05418e7a50d44d26904447e49259582209ba82285030402516e38f17f7` | 0 |
| include/xrpl/protocol/KeyType.h | 672 | `a86fe068106298ab0f561df3ab335779c7ad1e6d27312489a68308c45e499b13` | 0 |
| include/xrpl/protocol/Keylet.h | 671 | `0493747ed62de51c12914c46a7ec94468110f4873435cdde301f1c71d0c1031f` | 0 |
| include/xrpl/protocol/KnownFormats.h | 5084 | `81b01c776252737811eab0bb14168789b9831ce827e96045156450acf90f0993` | 0 |
| include/xrpl/protocol/LedgerFormats.h | 19704 | `adfef6c0e45870f08e06ab0c1773affa1ef011d9f297b403cb10e1dff4528b7a` | 0 |
| include/xrpl/protocol/LedgerHeader.h | 2115 | `1fb7936ab578d4a03bb7c34db08014a111a9a5f3890ee6e8ad6467a0a90e2d07` | 0 |
| include/xrpl/protocol/MPTAmount.h | 4069 | `23438f4e1b901d8c008205b4e5d5686b6a0cb7a4fc6ba9c52b770b8170fe921e` | 0 |
| include/xrpl/protocol/MPTIssue.h | 2987 | `3ed960415ee74783156a660cb414c19bf4dab1a859b97b3a30c6507352427b5c` | 0 |
| include/xrpl/protocol/MultiApiJson.h | 6852 | `d67c86d855391bb0133c434376a48f28e6dbe4747ecb6a74cea81565b9df7279` | 0 |
| include/xrpl/protocol/NFTokenID.h | 926 | `9c5a86f7070b1608de4d03ccb9dbfaebb93e8c944bef8328da694b163c4bbff2` | 0 |
| include/xrpl/protocol/NFTokenOfferID.h | 808 | `b534ce5acaa6a8370456ea20ca1ec214958373867c9311310a1837be32a4fd39` | 0 |
| include/xrpl/protocol/PathAsset.h | 4014 | `80069907aff8480a912ee9771bdb6aeabc80cd500c5016f984d3fbefc4a8fb85` | 0 |
| include/xrpl/protocol/PayChan.h | 411 | `3d2727a2284f14895fa3cd96764fd2c4f1ff0c47bf010d8cfdb279d01f7c6c2f` | 0 |
| include/xrpl/protocol/Permissions.h | 4125 | `e1e7e4ee02c67721e9a7e6da0b73ce3dd25713e41fe4353198d1ca2f7b043a3e` | 0 |
| include/xrpl/protocol/Protocol.h | 17151 | `cdb33e26a66bcea985504762988a650fa5e382d4d4bf50c53d31a30ecfb81471` | 0 |
| include/xrpl/protocol/PublicKey.h | 7124 | `8b0bb1340ab6b0607044413ce1117c8f08a507758d35b95eb9a3233b3cb3dd1d` | 0 |
| include/xrpl/protocol/Quality.h | 11249 | `637739086e598ea595417eadb673b240ad9f66499a843df3f776d05b1ee07561` | 0 |
| include/xrpl/protocol/QualityFunction.h | 2697 | `b71b060b934cec285374a8366bdb02da30b05b7a8f5cade7a08e06e369cd5169` | 0 |
| include/xrpl/protocol/RPCErr.h | 243 | `c9ccb98bf4295037edf11c375d9821db50d9e046232e69412bb64d4ecb8be171` | 0 |
| include/xrpl/protocol/Rate.h | 1586 | `a88b2a59143b5335be94db93adf3d56484d7c13a319a2c0a4c2914fcb2c18371` | 0 |
| include/xrpl/protocol/RippleLedgerHash.h | 118 | `ec3e0b66510c09022c79adef608b60a5542a70b78eae956bd3c19ef5c6b210e0` | 0 |
| include/xrpl/protocol/Rules.h | 3310 | `ce989301028a4c1632d33f39d9cda00a7f21a70a4a35434034ec5613ca426703` | 0 |
| include/xrpl/protocol/SField.h | 11282 | `c521d036879fe0ab6e63837e4003748a0e41d002f6eb31f16c57b0fb2faea6d1` | 0 |
| include/xrpl/protocol/SOTemplate.h | 4535 | `d86970103bd95f8fe79c453bcb57553d52140e04c850d28b2ce65eedcdcbc25c` | 0 |
| include/xrpl/protocol/STAccount.h | 2430 | `4833de73998b363a3a33a948a068e7914e17184a17e54c103db922ab7bb5b64d` | 0 |
| include/xrpl/protocol/STAmount.h | 21843 | `2547d0a51cec07ece5b3f8a43e916677b8d7f31d3a8c94c7c8d90184ea4f880f` | 0 |
| include/xrpl/protocol/STArray.h | 5518 | `4271bf4bad59259c62cf08016f18a303c91753566b9b1af942d7d42a7b789604` | 0 |
| include/xrpl/protocol/STBase.h | 5550 | `1404d69f5428a4ee6f74f59c6de0eab34a3fd1049907f59a0017f80ca3f243b2` | 0 |
| include/xrpl/protocol/STBitString.h | 3996 | `334d87fc570b55bad4e33bf9c9ae957104d5453b0daa9c7187b4480387b16cc0` | 0 |
| include/xrpl/protocol/STBlob.h | 2424 | `4db1075654f8e9f626dd8a90511caba6ada0e6768b1d7b78251c64107707187c` | 0 |
| include/xrpl/protocol/STCurrency.h | 2191 | `09c03305863b99791c912f2fb08aaa0226863af8cab9b43479add94d1fd0868a` | 0 |
| include/xrpl/protocol/STExchange.h | 3517 | `5a893dcdbed0450ae4021dfd42961260974843a91d815c011a95d763892bd842` | 0 |
| include/xrpl/protocol/STInteger.h | 3173 | `910d1dbcd625c62b3809ecfcc82ac5dcd943253fed9f11d7fa149397ac2af3bd` | 0 |
| include/xrpl/protocol/STIssue.h | 3461 | `8c84fe7adc2ed03e8b2d2804783a51c48a9beefa584f7b612ccf1f4c08047196` | 0 |
| include/xrpl/protocol/STLedgerEntry.h | 3212 | `d8d45b191e793e7dfc77f073ee04ab498056e7d154d9f2ef2651ac6fba982317` | 0 |
| include/xrpl/protocol/STNumber.h | 2770 | `f48db352c2e1ae7befa4fdf934678e2ec4aa914f280f30c932587e94b0aa3344` | 0 |
| include/xrpl/protocol/STObject.h | 32345 | `fe5fd4c8dc086ffbff3e07999e877f6a237adb11abbbaf644721d6e688b4c418` | 0 |
| include/xrpl/protocol/STParsedJSON.h | 1465 | `031869150938d18f11daf98b893556c813c926d6fba606f9d40405d747a29bd3` | 0 |
| include/xrpl/protocol/STPathSet.h | 16655 | `06582385f1bcfeb50659493bfbb585836d17e750f2d3abf401df87e12e90f635` | 0 |
| include/xrpl/protocol/STTakesAsset.h | 1834 | `cc4911fbff6dc25ff831a3265a021c5a08d991513d7b7f79c4678792f5ac7839` | 0 |
| include/xrpl/protocol/STTx.h | 7019 | `8bb5dca4c04326c6693851b03a56827a1b1fbf8964ff061be4d54c180809f1e7` | 0 |
| include/xrpl/protocol/STValidation.h | 8675 | `c2f17aea40fd4c40820b669a8abfea3815443e9038e97accc9ff0d70de9c59d3` | 0 |
| include/xrpl/protocol/STVector256.h | 4546 | `25031958bfed455cc35934a9dd229f5f4eab2ca59c0b58c259d134c65fbda4c0` | 0 |
| include/xrpl/protocol/SecretKey.h | 3862 | `74109ffeab9eb15e6c44c4ed25923e533afa35ff63dd3274868bee8b32248694` | 0 |
| include/xrpl/protocol/Seed.h | 2565 | `a48df5ede108d83543d4c72d181b89777ec63c41cf790075956edbb851d2afa1` | 0 |
| include/xrpl/protocol/SeqProxy.h | 4673 | `54f1314f7509a683543593df4651d39ceb7cec3bfb2f8a9fac03f80fa48ecd04` | 0 |
| include/xrpl/protocol/Serializer.h | 16416 | `97c56f3b8f171200bf69f5698bdd7637197d5164caf29ffac86b09d14cbb6670` | 0 |
| include/xrpl/protocol/Sign.h | 3850 | `0a27796de6ff5c4f6c5d29c9046f7c13cf4e05667e4895d26bdf4063949af05a` | 0 |
| include/xrpl/protocol/SystemParameters.h | 1975 | `d848c11aa78f3cd68e80a733146edcd5d74f04d29d603a8a0e49fdf5540e54cc` | 0 |
| include/xrpl/protocol/TER.h | 20127 | `ba315856555ddec5c1b42d623af3c4b6ac18ac168fd446fec5142f2a074e1879` | 0 |
| include/xrpl/protocol/TxFlags.h | 38277 | `567a139a145e6ac0d0296aa01cab60e7af78ff6b6171934345673b99a69a4f1a` | 0 |
| include/xrpl/protocol/TxFormats.h | 5133 | `a4ed8a45cd8c5a5653b384c20a944264a7863d8c0151588b92e486cb0f2207e7` | 0 |
| include/xrpl/protocol/TxMeta.h | 3026 | `43a396219daf1720cd557ee8f63fc8af1c0779ff7d10405cc9df19bc4801eb5f` | 0 |
| include/xrpl/protocol/TxSearched.h | 100 | `f132deff5f3bd6cd6b4621a83fb923f191b75043d1bb5fa6a50788a8aae548ff` | 0 |
| include/xrpl/protocol/TxSettings.h | 4092 | `a2820a43381c79a1c128db246e43d8c6106c961604a624aac3a3161876c4cc8f` | 0 |
| include/xrpl/protocol/UintTypes.h | 2859 | `3610b406e86d73947b0370a7d95c387e4dbc56229e88d8eba7cddaa2d538d05e` | 0 |
| include/xrpl/protocol/Units.h | 14333 | `7aa8aa0d7d2771760f80376e8b327dbf99f9637598193cfd21a7b58790da758f` | 0 |
| include/xrpl/protocol/XRPAmount.h | 6633 | `d63a0be2583b45edeade3e3bbe711dac4b8e580a0c8e662c92a35260e5552f4f` | 0 |
| include/xrpl/protocol/detail/STVar.h | 3309 | `ac7ac06d5d81fd004d0a09e5f076512f5a8ba944f911ed8ab1fcd5c8fd530b0c` | 0 |
| include/xrpl/protocol/detail/b58_utils.h | 5323 | `85d6c3eb000c8cbb349d9e77d3de9534eac39201454c97c241668cf92ebf8a8a` | 0 |
| include/xrpl/protocol/detail/secp256k1.h | 648 | `635e92ec9cfed8bee398d82d7032f84207c6ce5ca21ac14b3cabadfba52dec46` | 0 |
| include/xrpl/protocol/detail/token_errors.h | 2105 | `645bc3a8fb1ff82f4200237428e4e7823dee02a9916bda9b1b94b28ae498b3a2` | 0 |
| include/xrpl/protocol/digest.h | 5276 | `da213d4aba4170ce753a09075576ca86266bf414de3f725a86102ae683a00bc5` | 0 |
| include/xrpl/protocol/json_get_or_throw.h | 3975 | `96cef392ce9d9f00f20003fa36c400bd3531c3fe01241f48b2f1c20c88306bb7` | 0 |
| include/xrpl/protocol/jss.h | 40859 | `c87f75c9b80ba003f6d694189f43d1e8c7ddc6b2914652689044a365412d6ded` | 0 |
| include/xrpl/protocol/nft.h | 2894 | `6792dd5552f41f7281ed7a62b961d7749816810381edd3e3440aaae906d1affb` | 0 |
| include/xrpl/protocol/nftPageMask.h | 398 | `f79c6e09a689d7c8849bd58bc5501e8ec712e158ca2e059881f1716aab8f7d64` | 0 |
| include/xrpl/protocol/serialize.h | 514 | `3f6758ec7c953572633b7e94156958468f985f4d295ba5984c6e383d149f433b` | 0 |
| include/xrpl/protocol/tokens.h | 2943 | `6c1775fc3ce80082f3542b0df40c2fdcd124c4b59f6da8afe601ed4cadd3b89e` | 0 |
| include/xrpl/protocol_autogen/LedgerEntryBase.h | 4379 | `b45c34ba4a4766b0cf7c99f9798c4e8975921f2ce95dcba1bb61df014e6af4f8` | 0 |
| include/xrpl/protocol_autogen/LedgerEntryBuilderBase.h | 2474 | `36e1118176022b53c3362085a7a705315a2b56944068ac53ebe36c8e3ab6f52e` | 0 |
| include/xrpl/protocol_autogen/STObjectValidation.h | 1212 | `b894445c41449737b8e14ee1d614b356e6deab67f32f91436cf9b511d527e52c` | 0 |
| include/xrpl/protocol_autogen/TransactionBase.h | 12096 | `3ec4025d151a08fe2183f43082cddd121d9075e492e19ded809e3733181b10ec` | 0 |
| include/xrpl/protocol_autogen/TransactionBuilderBase.h | 7503 | `f8fdec772a78a14e06d6a77ce870d1d092ea27356450ee1b0882e48f05e61612` | 0 |
| include/xrpl/protocol_autogen/Utils.h | 310 | `034156f7716e917d92716eb41f5275d24592d16411095761759aecb3f8c2a020` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/AMM.h | 10525 | `64e1c98a52d8cffd234bb2a3530d9fe26678837445e03a9e4736b4a81a20d400` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/AccountRoot.h | 25390 | `5bba404a8032902b8e400b70fdb2d48bcda01a4eae2c9ded656e7f4212c2d72a` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/Amendments.h | 6465 | `fd81e6b70d9df2752b5ec6004b12745ed0d6eec45c1b49d00631e8ba2227f91c` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/Check.h | 11744 | `5918314471029beb941c35eefaa7c470433c661c9d549ff48efc176e92f9cebd` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/Credential.h | 9543 | `02f805b03c615960f547897d3a95e8cf5c08dbdf6bf14055ca4456234a5b46ba` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/DID.h | 7870 | `ad0365438b29aa9d0988d900898d1b8a0fddef3b569e4622d04a3daf0fff7aa7` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/Delegate.h | 7772 | `0e16caed408cf259282e87435d141c759b3787e60ada322a9c08ad8d60b9a9fe` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/DepositPreauth.h | 7599 | `6268233c3ccc79c47b69081ab64969317ffda093795ff370bd0f0d271ad96adf` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/DirectoryNode.h | 17116 | `40823daa3ff32fef523b1ea4abf1a7e70893f68d9e823376ef84be6df3300496` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/Escrow.h | 16609 | `c2b46033a5483b58e08d9444962cf284475fb77750bc829d298f8b0c6a2e3064` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/FeeSettings.h | 13977 | `1941d3937a5d69db93b04fef3f69c058de228b670635d4305202523cb004ed26` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/LedgerHashes.h | 5378 | `a27980626946a924ea1bdeefd73f3261bc695ecd77b79072e0d7ce41101b28f6` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/Loan.h | 25978 | `f5b76e01de412e3de34ffe4d6e04914bd72ed1902eda1fef118f39c237e18b7c` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/LoanBroker.h | 17162 | `eb7a805629a93b3db98db18925d87bb6b275520d8bba8a8d3a1f08646ee69457` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/MPToken.h | 18116 | `fedb2bf2343d928c4da2b8514f33db78a862a827890d48f65aaf35713c7e3c56` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/MPTokenIssuance.h | 20567 | `54b4fd1dd94661551966a66ebb075b86043cc1598fdbb4acf3259a535c58bab6` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/NFTokenOffer.h | 9468 | `e2f01cc4600393bd5c19fe419ffdca0e6f67cfc6f917dc5feb4b11c4445d461a` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/NFTokenPage.h | 6728 | `de3c70424d82095210e6181fc822d598935f614780b6e50b5159040c286cab94` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/NegativeUNL.h | 7620 | `f4e9ada9e739d9c395b7a6e49ad0b024f94d9a9c11211ac678b2c28f272f0e36` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/Offer.h | 11550 | `f67bd53d0e5d15092fb31b03d6292b7d5386a6283d98b6bc7141e3526ac7680d` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/Oracle.h | 9937 | `09742e07a0b9e496670f0ad234e0d41e64f47c18b2ec9aceec548f70f3b89738` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/PayChannel.h | 14367 | `5842e62ca613c0ebd4588a436f5c538bdb141ad73f0ca1263da565df47b4594e` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/PermissionedDomain.h | 7180 | `4d196ce0b9006aef9ada2810bacde90f204bd55e1c7281bb5cfbfbaf1bf2a151` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/RippleState.h | 13519 | `d4604e926ca88cbca4a3bed2fd3e6fad0552c51a283e80273bb01ba6c7e65c81` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/SignerList.h | 7845 | `f1eaee47ff23105fb02c4d9df4a14e5225871c20548818792129a1cbaa8d519f` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/Sponsorship.h | 9639 | `261fdf7b7479b7a933f3740927c5fa97a348f238f3d90e04f93ecd8e83db3f52` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/Ticket.h | 6145 | `f01d40e571f7b9aa8eeab1701d6541becf778004d2d6720063c3856fb9b2c57b` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/TransactionProposal.h | 7230 | `1000fea89b20dcca9fcc92ed122d82695c578475545e8dbaacd2294bd187d362` | 0 |
| include/xrpl/protocol_autogen/ledger_entries/Vault.h | 19670 | `e78d731ee08abd24b9c4095dc02c822fb55fc8789fc11ad42b4c0c1864ada3ba` | 0 |
| include/xrpl/protocol_autogen/transactions/AMMBid.h | 7501 | `96d51407be91d86bd22f7a69b1be652306c0f3aaf00f95308b9f31f345b095a6` | 0 |
| include/xrpl/protocol_autogen/transactions/AMMClawback.h | 6679 | `f910f8f232edc1b9e5a9162a6c7f99597ee5bb04232f633b5dd7a8bd5a12b83f` | 0 |
| include/xrpl/protocol_autogen/transactions/AMMCreate.h | 5606 | `48dc9804ca6d1254f6e1e995e62235f4b18454db48451fde091f13c9bd164425` | 0 |
| include/xrpl/protocol_autogen/transactions/AMMDelete.h | 4905 | `2d8b359e3c71a5121d8ff8a7ee5accf084738031fa89ec6492fdc9873e06c25c` | 0 |
| include/xrpl/protocol_autogen/transactions/AMMDeposit.h | 9653 | `7ae271a041d8e984e6a0346e866eb089772d7d24b827183446a392aa8d7e9a0b` | 0 |
| include/xrpl/protocol_autogen/transactions/AMMVote.h | 5527 | `c96db4f7b03f6f74cff194b56f0d121c628dc8ef4a176a2aa631e1a91de1b3ce` | 0 |
| include/xrpl/protocol_autogen/transactions/AMMWithdraw.h | 8789 | `447df859d8f40045056209d998be73765119e54cb654bb832a4fed805ca104fb` | 0 |
| include/xrpl/protocol_autogen/transactions/AccountDelete.h | 6000 | `ec37d2584efe45d6449611d8ed7aa6a1735f5552769c0d2e8bb3a40074c2f2f0` | 0 |
| include/xrpl/protocol_autogen/transactions/AccountSet.h | 12424 | `fa5a102c15b7ba39032f356fc079b538324832765e3aef858312a0766c48648b` | 0 |
| include/xrpl/protocol_autogen/transactions/Batch.h | 4841 | `1d76775daea855ab3e761cf64fbdcd0f3f7b2d07cb5520fd53fd844ced3cb462` | 0 |
| include/xrpl/protocol_autogen/transactions/CheckCancel.h | 3977 | `62572ef2df2128341d127acd78d948ec619144f14d408756f7174a1e4dc25cdc` | 0 |
| include/xrpl/protocol_autogen/transactions/CheckCash.h | 6003 | `60f45751ebda2a704ea0402de7095e53a1d2863d92f058a685f3b3e98f989d46` | 0 |
| include/xrpl/protocol_autogen/transactions/CheckCreate.h | 7626 | `dc8f508c5f761d1cd543c95fb9b378faec1db9830279117e72a31ff230fb01f3` | 0 |
| include/xrpl/protocol_autogen/transactions/Clawback.h | 4902 | `90653fd50d5b094fecce0e7caac23faa3da9a470ed595c73ea55cd363fea7de3` | 0 |
| include/xrpl/protocol_autogen/transactions/ConfidentialMPTClawback.h | 6466 | `ada5efb02783e279c3a4980ec7c360c1ded70221216bb81cf01f884f7f1d8c4c` | 0 |
| include/xrpl/protocol_autogen/transactions/ConfidentialMPTConvert.h | 10463 | `5d2455cd3fe5df8a3c1db3053c10967ef406a3a90f6891976c6229ffe02d3340` | 0 |
| include/xrpl/protocol_autogen/transactions/ConfidentialMPTConvertBack.h | 10144 | `ff5ed10038cb34791bbc62e6776d71058047c24e3a5e1e6e08c23d33cace5032` | 0 |
| include/xrpl/protocol_autogen/transactions/ConfidentialMPTHolderKeyUpdate.h | 8676 | `b5bb0bd4b0562a70f0856606a79cff22a7a61f7bfe30a0b3d8083018ca35eb77` | 0 |
| include/xrpl/protocol_autogen/transactions/ConfidentialMPTMergeInbox.h | 4449 | `c5e006af7226270dfb40425ac0186cf6b17efa331306e7b6ca7434ca93f60b68` | 0 |
| include/xrpl/protocol_autogen/transactions/ConfidentialMPTMirrorUpdate.h | 8168 | `29424e47408502450eaf137da188a63f976c0300c29b74da6a6ff44f967bbe07` | 0 |
| include/xrpl/protocol_autogen/transactions/ConfidentialMPTSend.h | 12769 | `d6de41777b6da2f566a1fb97715e09248aaf134e6412be4aff056223aa103dc5` | 0 |
| include/xrpl/protocol_autogen/transactions/CredentialAccept.h | 4842 | `7cea419b9e2397874ebf98a6374413073830c8f2f63617c703ef550ade4378c4` | 0 |
| include/xrpl/protocol_autogen/transactions/CredentialCreate.h | 6625 | `34ca1b6321a3b7b5c10c62504a792f5b9675c5c16e5b663ea9c948a3eaa51a50` | 0 |
| include/xrpl/protocol_autogen/transactions/CredentialDelete.h | 5952 | `c663497a39137d5f1e23e2ac6a888144f2d99a738216cf1c746df72b17d9082e` | 0 |
| include/xrpl/protocol_autogen/transactions/DIDDelete.h | 3252 | `02b420bd54f775535ec5d7fc6fb469cee354b572251dfa18a9e6c25c7c0c0faa` | 0 |
| include/xrpl/protocol_autogen/transactions/DIDSet.h | 5784 | `787b7b44a773f763eaa1f3ca63d6f3f9916c3d91b511a330ddf38543e26afd33` | 0 |
| include/xrpl/protocol_autogen/transactions/DelegateSet.h | 4708 | `9bdd9e1424e3191c2bafdf4547bf959b20b81902d126c3fec473fba0fbd5a729` | 0 |
| include/xrpl/protocol_autogen/transactions/DepositPreauth.h | 7322 | `7ecd820fb8341c04824e7ddd517c2bafd1438d7a2bf6bc32dec402b78222d01a` | 0 |
| include/xrpl/protocol_autogen/transactions/EnableAmendment.h | 4829 | `a1de069805a69eb8348d82dab305e4a0ff18470ea0e8f0d0296670081d39f548` | 0 |
| include/xrpl/protocol_autogen/transactions/EscrowCancel.h | 4722 | `fb9b242bdf8955a74c5768b700801602fbd1ad37c3fe471b00ed8ba8263c19e7` | 0 |
| include/xrpl/protocol_autogen/transactions/EscrowCreate.h | 10319 | `e4be5bbc2e9da341b3f19c1ebc0b76406930704267c5ab9d9ee57e9bae449edd` | 0 |
| include/xrpl/protocol_autogen/transactions/EscrowFinish.h | 8356 | `979167f8df76f0568254585937ec299ca2a9eb023b80e7cd810df0a73b96b8fe` | 0 |
| include/xrpl/protocol_autogen/transactions/LedgerStateFix.h | 5956 | `b7ac9150996a260a82f4c798d5b8e15445643488e1eba11f36aafefbd88d74a9` | 0 |
| include/xrpl/protocol_autogen/transactions/LoanBrokerCoverClawback.h | 5579 | `92660d873f2257847f7f1da97656b051df9cb0090c27d1f047871b4f7627458e` | 0 |
| include/xrpl/protocol_autogen/transactions/LoanBrokerCoverDeposit.h | 5133 | `f9a1b5a00a3f871880eeaab51008e5b18845d8a30a333ad44378c2aa329f7272` | 0 |
| include/xrpl/protocol_autogen/transactions/LoanBrokerCoverWithdraw.h | 8051 | `4d84e233ce45d7490621cc6fc6ce0c49bc5f94e8181c4e8ebab7f611208ccfc6` | 0 |
| include/xrpl/protocol_autogen/transactions/LoanBrokerDelete.h | 4209 | `be748759ce8e327b88e1f4050d7201f3878a6a9dac09c98075e0d637c27f6e69` | 0 |
| include/xrpl/protocol_autogen/transactions/LoanBrokerSet.h | 10714 | `f5f91cbc5ecf2ab88896bfb387f6dfbda7941bb2e9e1902900db1099fe0dcfcd` | 0 |
| include/xrpl/protocol_autogen/transactions/LoanDelete.h | 3958 | `bc8b45b45a9c0ba8ff3b91ee9c046a5c01c67f17dee1d1d1528a7c74b2c1e3d3` | 0 |
| include/xrpl/protocol_autogen/transactions/LoanManage.h | 3966 | `c9d6b11475524b5e6925e463236a8f98780f7495e0c061433d41ba1aa1d756c4` | 0 |
| include/xrpl/protocol_autogen/transactions/LoanPay.h | 4722 | `72ecba6ce2db487908d20a487bb367665036332bb30391c0b9a1d4fe743f98fa` | 0 |
| include/xrpl/protocol_autogen/transactions/LoanSet.h | 19192 | `cf64b28cdac04e202a69c4667583d178e42446a4632c2c34b74093c8de85a90e` | 0 |
| include/xrpl/protocol_autogen/transactions/MPTokenAuthorize.h | 5112 | `edc77aaef6828a05e70d8fa52bd9d759da803de01d3f23e2c8b51e463d759f4b` | 0 |
| include/xrpl/protocol_autogen/transactions/MPTokenIssuanceCreate.h | 9232 | `d393f4ca66d523fbb287b393c36537ba485bbf03e97491e4ba1a277669d0bca5` | 0 |
| include/xrpl/protocol_autogen/transactions/MPTokenIssuanceDestroy.h | 4375 | `b9e71c4f7ac7d61835786c39483b218faaba9679aeaa769e008cfa63a4ab4199` | 0 |
| include/xrpl/protocol_autogen/transactions/MPTokenIssuanceSet.h | 10966 | `ce095ccd84488f1f75e977178943a16734a8eec3021be60e0afa9fab93dc471c` | 0 |
| include/xrpl/protocol_autogen/transactions/NFTokenAcceptOffer.h | 6417 | `da7ac72aaa702dffc60fa31058c64d984462fa082239a77c4db3e3e6886c37af` | 0 |
| include/xrpl/protocol_autogen/transactions/NFTokenBurn.h | 4880 | `c92e1c46fcf389ef860558ba12f87a2b4b3fed653596279e6b261bdf7e4f02ec` | 0 |
| include/xrpl/protocol_autogen/transactions/NFTokenCancelOffer.h | 4221 | `af2cf5251ae14fe6ec56ddeecab92216280879f72810b0ac1a0a95d6b146b39b` | 0 |
| include/xrpl/protocol_autogen/transactions/NFTokenCreateOffer.h | 7589 | `7e8adb144f4c922df343adc567fb1ce3d5c34d19797624c491c403cf7f716fe7` | 0 |
| include/xrpl/protocol_autogen/transactions/NFTokenMint.h | 9424 | `318ad295dad68b21b2eead926b4ed3edab215caa47b0a83c3f12afb929fd69c2` | 0 |
| include/xrpl/protocol_autogen/transactions/NFTokenModify.h | 5773 | `79937af135ee9c22abe13bba29edca5a01669030690639195a3e18ed559fc5f8` | 0 |
| include/xrpl/protocol_autogen/transactions/OfferCancel.h | 4039 | `b6f1e907561fd5be222b40010641199e01dd6a8d87c6a68bb601169aac53d3d0` | 0 |
| include/xrpl/protocol_autogen/transactions/OfferCreate.h | 7744 | `d5f76fec0d2baba9249df0f3ee7a4414483ff5bc363cd84b66c5f96d525cad24` | 0 |
| include/xrpl/protocol_autogen/transactions/OracleDelete.h | 4106 | `e6f40de2a52ea10de4833927740ff584953fa4839d307783d2fa0d6c8730b371` | 0 |
| include/xrpl/protocol_autogen/transactions/OracleSet.h | 8152 | `7510663aa80c7c2da75b92b5719321560db8644899c17f7cb412d998c2ad602a` | 0 |
| include/xrpl/protocol_autogen/transactions/Payment.h | 11428 | `e4109ddfb127322cb3a464a588a9f92a2fda6be3b9ef65279f78842c78f17539` | 0 |
| include/xrpl/protocol_autogen/transactions/PaymentChannelClaim.h | 8711 | `80027c4d114e54974b15a0938a03e734855c6a87648b337fe24885d585693aa5` | 0 |
| include/xrpl/protocol_autogen/transactions/PaymentChannelCreate.h | 8218 | `c5998ba76add5ddfebef1d99add597b0b4aec5f284373ac1ab3f5c048547195e` | 0 |
| include/xrpl/protocol_autogen/transactions/PaymentChannelFund.h | 5717 | `c239456967ba0a44fe6f851ac1d9788dd55eb7761c510fc7e1d038db35411b56` | 0 |
| include/xrpl/protocol_autogen/transactions/PermissionedDomainDelete.h | 4321 | `84d0fdd4f96a03a8aed7f2ff29cad067a4667f2439bc416e0cd814bb463503b3` | 0 |
| include/xrpl/protocol_autogen/transactions/PermissionedDomainSet.h | 5242 | `d61d8984385d012d218a8ba8caa93e81d81a8fb794170a1e40cbdab8d34be197` | 0 |
| include/xrpl/protocol_autogen/transactions/SetFee.h | 13605 | `e69cafdca333b997977614eb09bca3a85765b256e60447a4681e8b9095f088b7` | 0 |
| include/xrpl/protocol_autogen/transactions/SetRegularKey.h | 4273 | `c46865d66417be9d71dafad6fc13e8695588d1eac1dbfcaba609e12b06167529` | 0 |
| include/xrpl/protocol_autogen/transactions/SignerListSet.h | 5056 | `9ceb1add1229586a8294a509a1db068ea9656b71be108fb83593a9c9d4973256` | 0 |
| include/xrpl/protocol_autogen/transactions/SponsorshipSet.h | 8188 | `d2083671852280d1a8f95cd433d9b0394d98b39dde9678747db402227213fc1d` | 0 |
| include/xrpl/protocol_autogen/transactions/SponsorshipTransfer.h | 5299 | `f3de25088adbca60f48dd567c9459d329e8f7eff9f09727f7996ffeb30d0a08a` | 0 |
| include/xrpl/protocol_autogen/transactions/TicketCreate.h | 4042 | `c6fa0c87e48f8793fa3014bdc614cc956a9d98be8f88c0a27eb460c03d1133b0` | 0 |
| include/xrpl/protocol_autogen/transactions/TransactionProposalCancel.h | 4357 | `b41babb9422ce29475b969ea22a8748708460a26e60dc9b928f482ba6f07d453` | 0 |
| include/xrpl/protocol_autogen/transactions/TransactionProposalCreate.h | 5138 | `cdc862ef972bf2ad5f2b422eb41c3b156b7f8a065c31fff448e608d4065c076c` | 0 |
| include/xrpl/protocol_autogen/transactions/TrustSet.h | 5979 | `2936ba28452e553c97ad516bb7d7fd9ae3ced585a7742a82d6168894df63f4ab` | 0 |
| include/xrpl/protocol_autogen/transactions/UNLModify.h | 5584 | `8931323c16b4d3e86cbb70e631309cd8d5a3c84bbcd55d19f98c92d636d64c7d` | 0 |
| include/xrpl/protocol_autogen/transactions/VaultClawback.h | 5766 | `47cf8aa08e465a9681ea41d6a84baf4a4dd389324a88ed14ad40a717d1afca17` | 0 |
| include/xrpl/protocol_autogen/transactions/VaultCreate.h | 12550 | `bac6942b41b0d8bac0f0431d9157683910b6f02d1b272c8a1c07d5dd815138ca` | 0 |
| include/xrpl/protocol_autogen/transactions/VaultDelete.h | 4955 | `7bbd1ffd43123dc5c20e81e439a2807a305167e2fe9ad3efef6a1a3a4c3334d4` | 0 |
| include/xrpl/protocol_autogen/transactions/VaultDeposit.h | 4859 | `749c5353313adf0d419b0ebfd9b5276655c9b5616df74bbd8a2075902a0800d1` | 0 |
| include/xrpl/protocol_autogen/transactions/VaultSet.h | 6626 | `281846a9b15ce35055b8522ae46331792f326e5efc0b9de65e3cb1dacddb6960` | 0 |
| include/xrpl/protocol_autogen/transactions/VaultWithdraw.h | 7764 | `d2d9318de43e9e97e73fed34171d675c8c67289423369a6bc867df2f13d18f12` | 0 |
| include/xrpl/rdb/DBInit.h | 5313 | `09f6778966ecd21910517e4a5f4949cdf2452a3f36cbeeb9b946324d5ff74a14` | 0 |
| include/xrpl/rdb/DatabaseCon.h | 6815 | `bbe2273b2ae6239ee4c87f319793b39616f9405859a7348c6e295389beb723fa` | 0 |
| include/xrpl/rdb/RelationalDatabase.h | 18542 | `dd4d0b3e208071975198c31181ffc33ed8517a40133ffc06f9bede806dfa97c8` | 0 |
| include/xrpl/rdb/SociDB.h | 3047 | `0bf30b79600e46b8a9015384fbed4524578f7263d0c0ddfb38e10effad4fb2ff` | 0 |
| include/xrpl/resource/Charge.h | 1190 | `8a86cfe31ea0dbdeaca62e558e0c11718280ad116c51ec78e661607405d1181a` | 0 |
| include/xrpl/resource/Consumer.h | 2028 | `deba469b0206e2a36ed7c4671b5bbecb85b63b4e55550bb5ae5a665408995824` | 0 |
| include/xrpl/resource/Disposition.h | 410 | `28211b098606987012501f73fb8e07ac7bad85211f2d8f4701bfd2217a88d489` | 0 |
| include/xrpl/resource/Fees.h | 1530 | `9459ba6cabbcab4460c661a222b660f7249c8856d9250974fe1737764d4b2913` | 0 |
| include/xrpl/resource/Gossip.h | 469 | `6c2818952d899c7cb67c3e6205f00cb63b1565eb9095ed5cc11a7567526ba914` | 0 |
| include/xrpl/resource/ResourceManager.h | 2014 | `1acc15b6bc97c26680bdf2ac9914c90c079256c5eb50e700db0b71c8c103c373` | 0 |
| include/xrpl/resource/detail/Entry.h | 2324 | `9a7780f56a6e45ec720947c44cdb614bf9144745d6d16f12bacde4acf1b2687a` | 0 |
| include/xrpl/resource/detail/Import.h | 598 | `c3673e1085ca56aef141d460b84ef97ba28ecdc723a9c486d32bbca4fdd64944` | 0 |
| include/xrpl/resource/detail/Key.h | 863 | `e58c5b003d948c4a1f5d26a9242ea7a9e419f3fcc48864c1dd2c6aaa4c212480` | 0 |
| include/xrpl/resource/detail/Kind.h | 429 | `94e5c4508f11abda3c608e18e14ddc98ab38048202edcd86ca26a5475180aaad` | 0 |
| include/xrpl/resource/detail/Logic.h | 17208 | `bceb222a6f168462f52e332f2cfbe22aadc2b546478f06df1fc6a98922d092f0` | 0 |
| include/xrpl/resource/detail/Tuning.h | 772 | `bb3d628fc1fd71bce6fdee12b6b4e0309410bc5e2d146b7c7b25b61a7f62a778` | 0 |
| include/xrpl/server/Handoff.h | 868 | `0d8a82fea79c1d7deb2f01c20bb65fe47b06bcf09e31be3f83d35eeb481fb668` | 0 |
| include/xrpl/server/InfoSub.h | 17898 | `ca6cf0a6fdb8a89c95ce2d10b6dfd71f16482a65926527af1092d54434aa98e3` | 0 |
| include/xrpl/server/LoadFeeTrack.h | 3502 | `e8ca6447fc79dff8dce7c110f3d0e5da680c622f91d9bb585ab1de111cd056b1` | 0 |
| include/xrpl/server/Manifest.h | 21157 | `bc9c1bd77169bff389bc6a51c5c96eb9843ce03008d1b874dcce1335891619ee` | 0 |
| include/xrpl/server/NetworkOPs.h | 8483 | `b6f3ba4a414e92388a988f5e4b9299ad3f359e928f027c15cc86bdcbcdcd2f86` | 0 |
| include/xrpl/server/Port.h | 2952 | `dc0188efd6fbe207e34a5794b904c3d50c4c1c7e7d931d1a5ddb0d51a3806059` | 0 |
| include/xrpl/server/Server.h | 479 | `9a1e82bf2110b98c9fc5381e9b9aa9faaf28b1903741b8ceb1757d309a76dff1` | 0 |
| include/xrpl/server/Session.h | 3254 | `a43edf9a17e37cb13fc4b6f97b9399c1f39f8b62ac3809634386855cbba5cdfc` | 0 |
| include/xrpl/server/SimpleWriter.h | 1279 | `f695f02b4a326f0e15224c500a6cec69af41b84f7b6cc09971ee09bafbbf3f6d` | 0 |
| include/xrpl/server/State.h | 2029 | `a5fd28514dc4bf6debe8d38f20f85c84c320c5508c052002809012927c342d54` | 0 |
| include/xrpl/server/Vacuum.h | 434 | `f74e9c56b313011a9cbdb89c48b2dd3d9379a9dc7cfa9c1cd26b96bd994ea6e1` | 0 |
| include/xrpl/server/WSSession.h | 3148 | `8add20c86e79b986f784b07163d344dd85c1d8996f44363920111ed87c2819c3` | 0 |
| include/xrpl/server/Wallet.h | 5492 | `a1d66f0adc01b8e8c3649b3793f6a7053e191ac0fc72866682ba613044373154` | 0 |
| include/xrpl/server/Writer.h | 946 | `22b25bcbf8c240cc35a716a25cf51908b2998f9e8347499623af99a6c4b530fc` | 0 |
| include/xrpl/server/detail/BaseHTTPPeer.h | 12214 | `ff22afc52415cda66dfa43a25c395747692680f1f800da858c8641f83d778220` | 0 |
| include/xrpl/server/detail/BasePeer.h | 2306 | `f074b3d0f4057dd321032c32f2233ac89b51587966bae4afa5f4acd93e237af2` | 0 |
| include/xrpl/server/detail/BaseWSPeer.h | 12896 | `77348faf08842ee2276ecac0aff5fdfd5e0e89363fd5dfb6e6f41f3a77645092` | 0 |
| include/xrpl/server/detail/Door.h | 12572 | `4c18bc4f0d9e09e712c89f9da9a976e883ce62d8424b5aac1dcab3fa17a58a1a` | 0 |
| include/xrpl/server/detail/JSONRPCUtil.h | 239 | `ffe32b3a2cb0ffcafe8d4ab819bf0d3fa5599d488f8acf5cf68f6367e4c4f4aa` | 0 |
| include/xrpl/server/detail/LowestLayer.h | 215 | `50c7475a8741c66592c25dfc07e42ec4b8491c70b7fb9768cc74aacea5bcfe3d` | 0 |
| include/xrpl/server/detail/PlainHTTPPeer.h | 4059 | `98b258e3d7ee715210279d55f532b3e8a000fd14ef7ee6c62d4ed595905ece5b` | 0 |
| include/xrpl/server/detail/PlainWSPeer.h | 1786 | `6e6c50bae784f6b34a8b944b3a52dd7341cbc38934ff6af4c95ccdaf7a9c1d53` | 0 |
| include/xrpl/server/detail/SSLHTTPPeer.h | 5243 | `7401bc79858460c8b06485149c19fff1d4815efefa4b88d15d29b1f1752ebb10` | 0 |
| include/xrpl/server/detail/SSLWSPeer.h | 2236 | `8607fccd21b44d5ab9e783b9945895d41f36fdbb2b6b9c23e8d0e8256540f269` | 0 |
| include/xrpl/server/detail/ServerImpl.h | 4431 | `b919ed8de41f1799fd6794d3349878eb9e358d5120dede5537bf93938206627c` | 0 |
| include/xrpl/server/detail/Spawn.h | 2219 | `fc07b4f78b339717c11b010a3064f2f0783ec6b2a56917e46888ef840a893b74` | 0 |
| include/xrpl/server/detail/io_list.h | 5130 | `b0d99cd9899d723eae0c8facb8f31e65efad3c16089f38a092632e656e77c52f` | 0 |
| include/xrpl/shamap/Family.h | 1667 | `70a8671d602eec88080489c93e401e69da223cce6b86803f71ed0834d6eeaec3` | 0 |
| include/xrpl/shamap/FullBelowCache.h | 3070 | `560fcd453e2f8b149079fead71cb133ec198b78a045581d4c20402926bb572e0` | 0 |
| include/xrpl/shamap/SHAMap.h | 34233 | `f85b2b6098539b58231e5c5f2b823960b0a893ed6be6e728d78c9266fc2fcc0a` | 0 |
| include/xrpl/shamap/SHAMapAccountStateLeafNode.h | 1812 | `47910633656e83cd3a0d0839110f87bf383df89f71c0691a20b0e4d50578b2c4` | 0 |
| include/xrpl/shamap/SHAMapAddNode.h | 4557 | `c976cc2f210e61c8e2a15b81ee06b0aeebcc475c512f5b903b6100efa462d62a` | 0 |
| include/xrpl/shamap/SHAMapInnerNode.h | 5923 | `0d050ce4865ddded62aef19a9785e2b1afaf3306a0c40204cdfa17e94cf3d025` | 0 |
| include/xrpl/shamap/SHAMapItem.h | 5291 | `db366a03ccf7a20ea5c3be02d5bba0e8b61e6c43e3865508b319e30bed95da01` | 0 |
| include/xrpl/shamap/SHAMapLeafNode.h | 1826 | `25d8be8524eee2427e3df6c0c61464fdfb2fd4840644574d15ca85f3eab9b030` | 0 |
| include/xrpl/shamap/SHAMapMissingNode.h | 1166 | `8b7d37f8214c3f0942d85726b7e10a8757ac44db10aef22d53bdc21a2e4b0775` | 0 |
| include/xrpl/shamap/SHAMapNodeID.h | 3989 | `0b0a6cae12d15ff34fbc1831f8a1f4c0c07c6f4ee02f3d0257763ba7df5d5cbb` | 0 |
| include/xrpl/shamap/SHAMapSyncFilter.h | 841 | `01147912ab94ba0d7b3a33ff3afc27314a35a190080640f27a5dbff87b27febd` | 0 |
| include/xrpl/shamap/SHAMapTreeNode.h | 5273 | `1c9ffeee745af2e9dd2514252bde8d62aab7714dc5cbaae46070a174e223cded` | 0 |
| include/xrpl/shamap/SHAMapTxLeafNode.h | 1665 | `d3922b4c8fd73a3ad03613b620b7356887108355417096d1ba6d2f6f53d74e7c` | 0 |
| include/xrpl/shamap/SHAMapTxPlusMetaLeafNode.h | 1837 | `e5534e0efa2e70744bb04e9c66a9b944d920e417ec6d5b3fd4169e6605bcba03` | 0 |
| include/xrpl/shamap/TreeNodeCache.h | 376 | `e300cc5a5c35dd1e172d35b2d665ff618611cf76ebba80f03aff6508bdaf736b` | 0 |
| include/xrpl/shamap/detail/TaggedPointer.h | 8433 | `6ce984caa7ec25f6bfc03c606d741d96ec42815974b038b1c8eb80b52c24ec99` | 0 |
| include/xrpl/tx/ApplyContext.h | 4033 | `462f96851aa96f3dae5f4c123ebf19b3de7110635a6a77f33a4de303d81f8635` | 0 |
| include/xrpl/tx/SignerEntries.h | 1971 | `c5129aa559d01ddd70c0e7f40f654ef0036096be36ecd4abfdcc01db834f7c80` | 0 |
| include/xrpl/tx/Transactor.h | 23675 | `cf3846e04417b9bc41d3eab9cd29b343c99221613aec35472ad984b73ed398eb` | 0 |
| include/xrpl/tx/apply.h | 3895 | `97efd547420c038629ceb04b3e8a5a8882745babf32c411228df1fd05eb5bbb7` | 0 |
| include/xrpl/tx/applySteps.h | 11814 | `564b61ee9e692dedf12ef5105a387c4c36141f3e50d705e0428064d21ff18043` | 0 |
| include/xrpl/tx/invariants/AMMInvariant.h | 1864 | `16ed1dc4d17e42e3b10f379cc469e7795e09a52097c5f21f626ef141d0f42868` | 0 |
| include/xrpl/tx/invariants/CosignerInvariant.h | 1630 | `6b27cf5a94d5aad64caebbf429cfec3d136c8ae1b11adbf15ef42312158ee7d8` | 0 |
| include/xrpl/tx/invariants/DirectoryInvariant.h | 685 | `f3bd99ae8e7b8706f87c7d8dbd5f4c3750b21a0c12137cab50df176c3572473b` | 0 |
| include/xrpl/tx/invariants/FreezeInvariant.h | 2344 | `22e11911fb24debe8c70de0fbd4ca25dea0dd637ece501fe88fe84df9d714ce8` | 0 |
| include/xrpl/tx/invariants/InvariantCheck.h | 15546 | `78a7c13e14543d5fc950450ce9f52df6984ab5760bc10700e51789f0e30f2d01` | 0 |
| include/xrpl/tx/invariants/InvariantCheckPrivilege.h | 1174 | `3071db1a4c273b66b320216460d3c7b8a01eb88cea891e002af3e7971fda0f9b` | 0 |
| include/xrpl/tx/invariants/InvariantRunner.h | 5858 | `c7ec79ae6b4d1af1ae906949cc360034e25e4bc08e175bec57c39439623628b7` | 0 |
| include/xrpl/tx/invariants/LoanBrokerInvariant.h | 2882 | `a7dc0f41eb2f978ff9a014ffda6bbf05dda6f0803987d1c20105af8fb11f2218` | 0 |
| include/xrpl/tx/invariants/LoanInvariant.h | 2838 | `dd0c6dd1041e33f5e93a43eb487ec5ebbdb5064af7a2734e4b9c1af403428062` | 0 |
| include/xrpl/tx/invariants/MPTInvariant.h | 10317 | `2e2447b530e25d4a8a4712e3674ddc86e687655e9ec7b77f19075154ac08fc81` | 0 |
| include/xrpl/tx/invariants/NFTInvariant.h | 2279 | `29fabd3c1d89e21690cbb6dd5e2f510a07aee6b407af4498e2ee8b3b8e184b17` | 0 |
| include/xrpl/tx/invariants/PermissionedDEXInvariant.h | 1096 | `bec0619a23ba1df68522b7a25e1eadf15bd0273eb60dffa0ec2e41681c4be352` | 0 |
| include/xrpl/tx/invariants/PermissionedDomainInvariant.h | 1067 | `a2464e1bbba3ce419207a20f0f9d9fa2e3684544d122860e421d01f585133327` | 0 |
| include/xrpl/tx/invariants/SponsorshipInvariant.h | 1935 | `8858b46b14276a6d1f26d4298364977b892e0687152c4b75246c92d8cb61b4b0` | 0 |
| include/xrpl/tx/invariants/VaultInvariant.h | 11394 | `e8caf787a79b330fffb9cf71b4c3ff0645f9a5a7021742add016be9c8a199f1d` | 0 |
| include/xrpl/tx/paths/AMMLiquidity.h | 3893 | `7851e5b95bec15a5f7ece9a47fda4d20e02b4d329573099236033884be84545f` | 0 |
| include/xrpl/tx/paths/AMMOffer.h | 4130 | `e2e204c1e40dfc676a96748f4cb3ef349e5ff37f280770758039c919cf74b495` | 0 |
| include/xrpl/tx/paths/BookTip.h | 1374 | `1f1a795b24254ec5ced8ec3743f9a198e454b736321394fcf2dad8172d31465b` | 0 |
| include/xrpl/tx/paths/Flow.h | 1738 | `49c09d6c02098bf948540ecc9b36c9411f1b884592894d96d05a497426026fb1` | 0 |
| include/xrpl/tx/paths/Offer.h | 7359 | `65d5427c80da74d56a0338109caedb97d6ffdd907dfadeea8afbeb9c2c5a9e3f` | 0 |
| include/xrpl/tx/paths/OfferStream.h | 4203 | `a1a552e6d84c9ef1c0ad9fce021d30b71f442546736d2bb305ec0b95d48db6b8` | 0 |
| include/xrpl/tx/paths/RippleCalc.h | 3127 | `440cf8bbbcd562eada3be5de408b3a46dcbd608e2a203337fd36bfe388f05c18` | 0 |
| include/xrpl/tx/paths/detail/EitherAmount.h | 1242 | `3921a543ad40a0bb7bd211c709ebe9df18b9555b80c03594a4f54e77daab2aad` | 0 |
| include/xrpl/tx/paths/detail/FlatSets.h | 678 | `6d0282d96ca64298a78d85468d466e463d950a132c1c6dc4f86bd8dd630d146b` | 0 |
| include/xrpl/tx/paths/detail/StepChecks.h | 2732 | `3498f5807a44767402494c9bdbbfd91c9e474883f6a67fd94902574508bb3ca1` | 0 |
| include/xrpl/tx/paths/detail/Steps.h | 23001 | `c5645f45ebda07b3c4a206846639c50782a820a0e4e6cf3f904704272dc592ba` | 0 |
| include/xrpl/tx/paths/detail/StrandFlow.h | 30189 | `4d5ac709eade2154d01dcda036c52e88dab1e75fe7e86f07c80b619acd842f0e` | 0 |
| include/xrpl/tx/transactors/account/AccountDelete.h | 1143 | `ff22ca4fb215f830303c2fe6edea293a7838bd4b0813acf42065858830e4eb7c` | 0 |
| include/xrpl/tx/transactors/account/AccountSet.h | 1157 | `1cd643b01c4c69b72e14eb04b46fa919479eb513294bc847cc19805d35ecf2f5` | 0 |
| include/xrpl/tx/transactors/account/SetRegularKey.h | 1015 | `d94830a621cb47b85e091ef091e326d89c3496b5093866d858c35a35b0379e22` | 0 |
| include/xrpl/tx/transactors/account/SignerListSet.h | 2362 | `f9a30ead148f9b4043e734af90c556b64985efed862ea8d96468faa77f473353` | 0 |
| include/xrpl/tx/transactors/check/CheckCancel.h | 986 | `2c99f58d771c55e606c6e70f735aa47e5bef56fce096016cf9d0656a100713cf` | 0 |
| include/xrpl/tx/transactors/check/CheckCash.h | 1052 | `6c092a760e23f8a2db48aaa14a3e359f4ccecaa7a942b2924d7022803493edaf` | 0 |
| include/xrpl/tx/transactors/check/CheckCreate.h | 1062 | `d24634e607bccb06f3d66b222cec878d77c9c01a685edb4590c8b82f413c8764` | 0 |
| include/xrpl/tx/transactors/credentials/CredentialAccept.h | 1089 | `df6514e65a2d7ff0e30d7dd12b74d17f9660b4931a1e84539f1e2546a40dbb73` | 0 |
| include/xrpl/tx/transactors/credentials/CredentialCreate.h | 1089 | `f24622a44d47ac50e2d6391d2a512c5bc24cbcafca62ea24190d45a4bf12ff02` | 0 |
| include/xrpl/tx/transactors/credentials/CredentialDelete.h | 1089 | `7782ac8b50675aef7f4f97c465c22bc6c944df162ec64c6c6a7eedf59c713def` | 0 |
| include/xrpl/tx/transactors/delegate/DelegateSet.h | 1145 | `723054ed473441e454cd7358b4e31f4451edf1a2e038c14ff1d53f286a507449` | 0 |
| include/xrpl/tx/transactors/dex/AMMBid.h | 3184 | `01ae894803c6bf52a2f4357205fd465da92eaac508446398bce0a40c6c37272a` | 0 |
| include/xrpl/tx/transactors/dex/AMMClawback.h | 2238 | `7034695a60b98e0c8cb334d036aca7a21ef21b61439fc80d315c69e8767f8bd4` | 0 |
| include/xrpl/tx/transactors/dex/AMMContext.h | 2092 | `6fd34d89538da3037eed1a519884f7624a540e7ba2d002ad01426f4b828921ac` | 0 |
| include/xrpl/tx/transactors/dex/AMMCreate.h | 3151 | `09227729755764b86c7a2c7b99ebedf2d24f5e619beea15ac3f657dc64c24b28` | 0 |
| include/xrpl/tx/transactors/dex/AMMDelete.h | 1384 | `6b7dc9eecd6d096ca15d93350bf8f73c1593379d839e1d5990273f9c4b174202` | 0 |
| include/xrpl/tx/transactors/dex/AMMDeposit.h | 9338 | `bd095bdb138ec73c79735f60334ce4b02ffca8c604f1ef4fe1105da54421da5f` | 0 |
| include/xrpl/tx/transactors/dex/AMMVote.h | 2348 | `345607f1f75443604a2c73660049805f1eb088b857e1ea7a42a9bddf9f044236` | 0 |
| include/xrpl/tx/transactors/dex/AMMWithdraw.h | 12889 | `702c8f1073b1fadb54c9ffbe64ac5236ca3ee9882603154e7c771e426e93ab35` | 0 |
| include/xrpl/tx/transactors/dex/OfferCancel.h | 986 | `958eaf024811d0e67c5e4454f6ec498a28f37ff10f67f6ced03e133e51962f3e` | 0 |
| include/xrpl/tx/transactors/dex/OfferCreate.h | 3030 | `fb58d9b153eb964ce38ae71d050271369f841e75bfbe779ad0ae5b8f204fbeae` | 0 |
| include/xrpl/tx/transactors/did/DIDDelete.h | 1228 | `814e2d3574b64f022ba5da096d78181ddb754af33ab5590d34d53fba1c61db22` | 0 |
| include/xrpl/tx/transactors/did/DIDSet.h | 918 | `7546d36d09735760526631ab0a7f99a12d9ed771d04362e34a398fc055dedfdb` | 0 |
| include/xrpl/tx/transactors/escrow/EscrowCancel.h | 988 | `ae7c1993fd31c332303196c779610402733c0b774e0318086a8b025b6e7cbae3` | 0 |
| include/xrpl/tx/transactors/escrow/EscrowCreate.h | 1220 | `cc2222d7cb8c0ade4b42c2709438b96ebcd0f960f1cf9edee8f25ea3ab358e0d` | 0 |
| include/xrpl/tx/transactors/escrow/EscrowFinish.h | 1215 | `841fb0367d031654feaa3c8ebf9e4b66fa2ca57ca9a77f6739fb03596975a534` | 0 |
| include/xrpl/tx/transactors/lending/LoanBrokerCoverClawback.h | 1162 | `b0474a0fe4fcd969436e2124a8c05b92b849cc7939117193336312c6f9098fbb` | 0 |
| include/xrpl/tx/transactors/lending/LoanBrokerCoverDeposit.h | 1160 | `38db109d02c588e880d2b5c0eceaf915adea97685896735548e3bdbba262dfe5` | 0 |
| include/xrpl/tx/transactors/lending/LoanBrokerCoverWithdraw.h | 1162 | `9de5a2551bdde6bf37a3d88fb74c96b36520ac8c03ca1c250b52cd090483002e` | 0 |
| include/xrpl/tx/transactors/lending/LoanBrokerDelete.h | 1148 | `9fc5bc6297701689c30f7c1edcc413e5ea9e1c3626719574768cdd7563600cba` | 0 |
| include/xrpl/tx/transactors/lending/LoanBrokerSet.h | 1367 | `4e24e92fac7edaa0f1d95ad139b17d439ed0dec66a672fb67ee05bf5a3fa93fa` | 0 |
| include/xrpl/tx/transactors/lending/LoanDelete.h | 1136 | `c3fba7ae24932813f8ab34fe032fd7fa58b3b9e7466f0c6f920fa4f49b6514db` | 0 |
| include/xrpl/tx/transactors/lending/LoanManage.h | 3336 | `566995601a5be98ca35c0b939c335fa5c4213724df93be4dc38df02ed2e8eb05` | 0 |
| include/xrpl/tx/transactors/lending/LoanPay.h | 1305 | `736bd1592ef9d2143eca5b964a26b683b04d9ecaae1f2606d67c441347cd870a` | 0 |
| include/xrpl/tx/transactors/lending/LoanSet.h | 2042 | `cbcacbe360a865a8ff2887cf15de91678733861c19628ea75a1b6e79d06891f8` | 0 |
| include/xrpl/tx/transactors/nft/NFTokenAcceptOffer.h | 1406 | `d40adf1ca147e8f52dc18b334ea2e0018b81713ea3a5edfaa0b5c047fa2491df` | 0 |
| include/xrpl/tx/transactors/nft/NFTokenBurn.h | 986 | `93b89c6a15ac7f90e52121d77db70dc1a40f3bf9811e8ee95c1f6c92e4772714` | 0 |
| include/xrpl/tx/transactors/nft/NFTokenCancelOffer.h | 1000 | `733f3bab020da79046276fab595a6bdafcfb3c4e70a7b204abc32a03a35925e7` | 0 |
| include/xrpl/tx/transactors/nft/NFTokenCreateOffer.h | 1093 | `c313815a40fcaccffc774a4a61b503d4fb30c74c2436adc2bc9afce20f189bd0` | 0 |
| include/xrpl/tx/transactors/nft/NFTokenMint.h | 1478 | `20a8d49efa787049c7b239afbf94cffb78f6253197abb12e423d1b46fd46fac5` | 0 |
| include/xrpl/tx/transactors/nft/NFTokenModify.h | 990 | `a0fe500464c59194725b19050ab552cfde123579ef7fe2f827871771e08fcedd` | 0 |
| include/xrpl/tx/transactors/oracle/OracleDelete.h | 1530 | `c20f3863199e3297e7140b31a72a04d64dc98481edb65f3ebbd2d1ab12dd281a` | 0 |
| include/xrpl/tx/transactors/oracle/OracleSet.h | 1345 | `99cf0b5d3b847b520363643410a4637c94999bfce8a5182be7142fc9e73b4315` | 0 |
| include/xrpl/tx/transactors/payment/DepositPreauth.h | 1269 | `349a062ad5f4b7a94bec7e2d7ee92264d449152841b1e28b933613b6289d077a` | 0 |
| include/xrpl/tx/transactors/payment/Payment.h | 1670 | `cea3710de31464d1d924f7a278a71135cc012c56f3e633eb97cbb88dee6ee540` | 0 |
| include/xrpl/tx/transactors/payment_channel/PaymentChannelClaim.h | 1165 | `ef7dafe8c686acb405677e0f584c47f61b0d51b745a915fb9a44918210deff3b` | 0 |
| include/xrpl/tx/transactors/payment_channel/PaymentChannelCreate.h | 1084 | `8aaab2855eacb605651c44ea6111cb7376fb744f40c19b78c737ba99680fb7ae` | 0 |
| include/xrpl/tx/transactors/payment_channel/PaymentChannelFund.h | 1022 | `804974c064a1661b0f2537dfeb47e588930191657910ff1d325bfd4881162bb7` | 0 |
| include/xrpl/tx/transactors/permissioned_domain/PermissionedDomainDelete.h | 1078 | `990c1882cca9a480d0c758d511d876c8a4dfb3d233a8e92651fe6ef42aaedef8` | 0 |
| include/xrpl/tx/transactors/permissioned_domain/PermissionedDomainSet.h | 1142 | `16fc8d03c0555404301fbded9c4e1032951017cf4202bf18d89962e376615580` | 0 |
| include/xrpl/tx/transactors/proposal/TransactionProposalCancel.h | 1016 | `0c1e50b9199c87df8b2e503333dcbdf7ce5f77cb7d87a1e9e321e9c1f71d920a` | 0 |
| include/xrpl/tx/transactors/proposal/TransactionProposalCreate.h | 1014 | `1b6f3beec340c3343f5e9d2ed819157a4971bc979a2a0062488872ca3d6ccf22` | 0 |
| include/xrpl/tx/transactors/sponsor/SponsorshipSet.h | 1464 | `7e8703f9c41db47be508eb327f2311e64436195224fa72acb00c6a04967958aa` | 0 |
| include/xrpl/tx/transactors/sponsor/SponsorshipTransfer.h | 1097 | `1f071e85472a20312dc105ee5e980741e4588804fe44b1fa6ae543d6316429c0` | 0 |
| include/xrpl/tx/transactors/system/Batch.h | 2449 | `745d5360c6dc40fdddc680282c5074556b154d8cac81f14cf4f8223907fc5695` | 0 |
| include/xrpl/tx/transactors/system/Change.h | 1415 | `0aff895532b791021c4f0c055bee22e5d9f100d5b4773f6fde378ff1bb46e972` | 0 |
| include/xrpl/tx/transactors/system/LedgerStateFix.h | 1202 | `aa916265c393d22d8bc60ad63539220102d08ac265baa072126c07274ce023e8` | 0 |
| include/xrpl/tx/transactors/system/TicketCreate.h | 2824 | `09d5d7f2305f50e7bf5659cd7da1b142e6a54e225e721215d990120c917bec4a` | 0 |
| include/xrpl/tx/transactors/token/Clawback.h | 980 | `ae69b063b46b03a8280b310822a6d266252a44b3ac21d6bfe76bba83ded0b906` | 0 |
| include/xrpl/tx/transactors/token/ConfidentialMPTClawback.h | 1881 | `f8b7f38410d8543a4988c78c10b18edcd26d935f0278aec0dda23b57e3813d52` | 0 |
| include/xrpl/tx/transactors/token/ConfidentialMPTConvert.h | 2008 | `ce8604439a5d1416775610d88fe18349bd32c9245ed73c515d4ab93f5740598b` | 0 |
| include/xrpl/tx/transactors/token/ConfidentialMPTConvertBack.h | 2061 | `82aee139cb281ab1192ce3e19cc0c2a99b1ab5120557b190f374fe40b2d00c51` | 0 |
| include/xrpl/tx/transactors/token/ConfidentialMPTHolderKeyUpdate.h | 2718 | `ad046a09efc1d966c93d53562ea1e346ad6a97d74c2420b82e5f7af64c7b2f07` | 0 |
| include/xrpl/tx/transactors/token/ConfidentialMPTMergeInbox.h | 2169 | `6c1f29bab362d8da7a5a61d1c1387ff4dc30f53bd063ae32200aceedb6da77f7` | 0 |
| include/xrpl/tx/transactors/token/ConfidentialMPTMirrorUpdate.h | 3885 | `09ca1a52f03ae3933657ad8c753903141bac8f9238c93958ac6f6b8eed8c1f6f` | 0 |
| include/xrpl/tx/transactors/token/ConfidentialMPTSend.h | 2558 | `55ff8e20f11e85c444092cb96802e4ed9dd99d17c2833875c3a78029da958204` | 0 |
| include/xrpl/tx/transactors/token/MPTokenAuthorize.h | 1376 | `ba74c4e61cf90d591b746ebb53cef0615bc58970848b534e80f206b4c0fbba4b` | 0 |
| include/xrpl/tx/transactors/token/MPTokenIssuanceCreate.h | 2516 | `f2da6edf66ff0e9658b392d16a8d9c10c6095c4b88f79d6ecd8d6c8f91c83b89` | 0 |
| include/xrpl/tx/transactors/token/MPTokenIssuanceDestroy.h | 1008 | `126e89733b0842af3f86d54b221f4ee82a000a3f036f8838b28db8d592e3c488` | 0 |
| include/xrpl/tx/transactors/token/MPTokenIssuanceSet.h | 2962 | `3582168dcbff593760622e0ce261371aeed2e4db95e1d086977edef5d936c722` | 0 |
| include/xrpl/tx/transactors/token/TrustSet.h | 1322 | `41c0866792df0a3dfa10563cc2841b5f6dd41d725b2243759dbab7a3b0dc7c97` | 0 |
| include/xrpl/tx/transactors/vault/VaultClawback.h | 1327 | `5e7ac4d4cb43d36e32f4143b1b2daf91828e845a42c961c9fe36dbfd128b55ab` | 0 |
| include/xrpl/tx/transactors/vault/VaultCreate.h | 1149 | `181b555bc9123c57021273d23c7ece4c97a179642d1caac1742d1ae664ee168e` | 0 |
| include/xrpl/tx/transactors/vault/VaultDelete.h | 986 | `2b1e9a64724ecf8a056f89c3d26a58584bbe51e4ef02f752f775258d4fa841da` | 0 |
| include/xrpl/tx/transactors/vault/VaultDeposit.h | 988 | `93e37f71a2f2b2f9cc0e0b926db62fb092fd9cfa8e2e4b33d11fa1545350898c` | 0 |
| include/xrpl/tx/transactors/vault/VaultSet.h | 1050 | `813b34e586b81738812225a98cfe2badce54a9b2dcb8128ef55aab83ce001d41` | 0 |
| include/xrpl/tx/transactors/vault/VaultWithdraw.h | 1060 | `132abeb30da4c476c71ca075527d8a64e112a6a67b2a2d0b626623bfb875c64f` | 0 |
| package/build_pkg.py | 13296 | `065728476480344b4707eb7302870323a743fb017de8b18401c72c43ba9727b1` | 0 |
| package/images/packaging/publish_pkg.py | 6204 | `61a6a3028bb280c0aeb0e8335d9ffc5fe49f7ed0da5b3a13e08abd43605f371e` | 0 |
| package/sign_rpm.py | 4492 | `5cecdb236fc90da1f855ea4e091a9d9eff81e40e2031300ca28417b090d2bdad` | 0 |
| rust-toolchain.toml | 137 | `788bfd24261793dd57b7ad6530cb558b51d65ddae52699701d26156bc3c2f0e7` | 0 |
| src/libxrpl/basics/CountedObject.cpp | 799 | `0fc7865ed6d7b8217a096f001ffccaae22a6e260a929d73f5fca3e8778387e8e` | 0 |
| src/libxrpl/basics/FileUtilities.cpp | 3155 | `392ee341429e1da67d5ee43f5cee9e695ba2421108af8e5b89eeeef5403a51e3` | 0 |
| src/libxrpl/basics/Log.cpp | 8987 | `d6989e288e1da18af86fdbe76f998972a6b6b5d3cc76f1427c911925bc909a57` | 0 |
| src/libxrpl/basics/MallocTrim.cpp | 4520 | `0bd608be4f20b2b103f6d3a4bb7e982bf6ea7bf8dcc829c491eb6c75526a4507` | 0 |
| src/libxrpl/basics/Number.cpp | 56569 | `f7c4a9174da5a036008293c8587cbdea9ab9f87a1b22aa7ba013e34c0ce26f38` | 0 |
| src/libxrpl/basics/ResolverAsio.cpp | 11414 | `6e6e8b033e93ff99e5e95e1afbc21bbf14154e8ca394636d8392a6de472aa8cd` | 0 |
| src/libxrpl/basics/StringUtilities.cpp | 4775 | `56661066d66945483116f3273972d326a861fc707de6e9af63a00082f8023c3d` | 0 |
| src/libxrpl/basics/UptimeClock.cpp | 1385 | `33bae9e266754acab6413af764bf2ca9338422f4c3852fb1df80a8e64a4e2ada` | 0 |
| src/libxrpl/basics/base64.cpp | 6506 | `9dc2da69681a536ee0ea2e6883f1d761624a7b7f2034313ee8309c1cc43f9283` | 0 |
| src/libxrpl/basics/contract.cpp | 862 | `76b59e1df8637760e7f85e074da5bc9939f8ea5a23fd5ffcae30e8412f52463e` | 0 |
| src/libxrpl/basics/make_SSLContext.cpp | 11997 | `be21cdd60bdf5a8c56080235991fd98f8850b5b17c39a8a2489da51543fc76a9` | 0 |
| src/libxrpl/basics/mulDiv.cpp | 500 | `2ddea8853bd783cf589c8df9fd18626bdc3d550afee7be43f54499e17551aa3d` | 0 |
| src/libxrpl/beast/clock/basic_seconds_clock.cpp | 1841 | `b0a55e9e423675ac1d11382c7929cae5b47967b527e17a155b01a0a4773cf054` | 0 |
| src/libxrpl/beast/core/CurrentThreadName.cpp | 2807 | `87f0640a8fba7848546ccbed90682268f7bafaf29f777ade2b4812f2c7917fa7` | 0 |
| src/libxrpl/beast/core/SemanticVersion.cpp | 7723 | `02ae49aaafdecbd5c8ae36b426f4e67492f4675858c886ff3f0c4c3304529236` | 0 |
| src/libxrpl/beast/insight/Collector.cpp | 137 | `7396a2eb395ea79d573d15861b6d0f98c09070e3ef4a70d88db36c4832ff28c1` | 0 |
| src/libxrpl/beast/insight/Groups.cpp | 2741 | `f972e03b6fd502381a0c3ac6aa516e20c5ba027d10cee4fd9c8d816fdd23d556` | 0 |
| src/libxrpl/beast/insight/Hook.cpp | 172 | `4bf263afdb0fdebf0d3e60531c365bdbe1e33455fa36018b0026abd0a0311599` | 0 |
| src/libxrpl/beast/insight/Metric.cpp | 377 | `f5d9d73242a4f96ab39e6c1aa5c81453d1458ea293e23baf7e2b516558643108` | 0 |
| src/libxrpl/beast/insight/NullCollector.cpp | 3140 | `389897a329bb27cb755ffae335247cce0878349b0c833f7358d7058b632db1d1` | 0 |
| src/libxrpl/beast/insight/StatsDCollector.cpp | 17555 | `9924c2d5ba0febd895f48d3ba42c9afe1c72d28dbd82060ee1efe11bbea1b50d` | 0 |
| src/libxrpl/beast/net/IPAddressConversion.cpp | 690 | `223fa9c5a993b175993b17625534f32231680c579fb080f91e0be01235ee48a4` | 0 |
| src/libxrpl/beast/net/IPAddressV4.cpp | 1995 | `0857951f5730970793cc9a16c113b07948430a0b4ae7b813470beceef65063c4` | 0 |
| src/libxrpl/beast/net/IPAddressV6.cpp | 1860 | `b3b4d732ee62a37427672ff2f53dee82d6d02b4b5c38741bde93210d55a32798` | 0 |
| src/libxrpl/beast/net/IPEndpoint.cpp | 4293 | `c6815df82ea686f12a9280245d570cedbec4d5864de351ba4d950d854f320995` | 0 |
| src/libxrpl/beast/utility/beast_Journal.cpp | 2749 | `8b5f6d72b4903f592d297eb6f6c08ad5fef910fed3040c803d73f81ec2d3dd82` | 0 |
| src/libxrpl/beast/utility/beast_PropertyStream.cpp | 10689 | `d12f2d3efdbdefb8f3e8f698ba480d4fda49bab937ca93b7ac42c8fd732feea2` | 0 |
| src/libxrpl/conditions/Condition.cpp | 4922 | `fd45cc09a4eb7c654299d7cf6ab49209e3379f1e9cec8bbe29bd85beb6b29d38` | 0 |
| src/libxrpl/conditions/Fulfillment.cpp | 2920 | `b506d1e22f5422d57533c8a6d14ed9bb4e5e7b931c4c3e13ab592dd4d818ec71` | 0 |
| src/libxrpl/conditions/error.cpp | 3262 | `00d9c7326d34a5b552cbdee0ff60347ab3e1e544cbcfa822cea09abc5fe8e15f` | 0 |
| src/libxrpl/config/BasicConfig.cpp | 4710 | `8cb7249503274e5e695ccf435c2baa8413e1844bf127530e543700411c2312f5` | 0 |
| src/libxrpl/consensus/Consensus.cpp | 9077 | `c36cf3c3891abd706d414c65619efee63cf940fdc44beead918ec8ebf3fc8c55` | 0 |
| src/libxrpl/core/HashRouter.cpp | 3384 | `a9026d54cc18da8515069a095be0e40a22129a5f4c103bdc2cc0394a58e0ea27` | 0 |
| src/libxrpl/core/detail/Job.cpp | 1804 | `c5babd8d8ce4b7f961c1be7cbc15e5318d10f110aadcff587ebe7c57406cdc25` | 0 |
| src/libxrpl/core/detail/JobQueue.cpp | 11452 | `c024b6f0f2892fad8ff4af8db8ac05ef736f8c1a4ee0c65bf783026d8b6f3e2a` | 0 |
| src/libxrpl/core/detail/LoadEvent.cpp | 1413 | `9aad10c4d3a8e9b3553496b79fa6f639c9455681eb711fa32efb07d9cbceb796` | 0 |
| src/libxrpl/core/detail/LoadMonitor.cpp | 4283 | `4148019671ebf1b826c4bc4bbf964ee0bd260abb40005818995be186ab9615e5` | 0 |
| src/libxrpl/core/detail/Workers.cpp | 6993 | `4bbec279fe40b5946c84a6775ce3efbe5b6dd4f41ab615582885c19f2877acf0` | 0 |
| src/libxrpl/crypto/RFC1751.cpp | 24198 | `970772ca78ee3c30c8785b5a2cca514724ce9e9e5156f813dd7bd249465ab0ed` | 0 |
| src/libxrpl/crypto/csprng.cpp | 2092 | `027a2ff0fa10b220f97254c683b93cc91eba801529ffd36ee1e0d85d514e5e6f` | 0 |
| src/libxrpl/crypto/secure_erase.cpp | 214 | `f921a0415156c59e5e9b86290e8f6eb6f8e18fd053f3f8b39c34e0c9faaae67f` | 0 |
| src/libxrpl/git/Git.cpp | 589 | `cbd512cce907f6a3a0beffbeabe0bd6706588fbc9a9266b5e35f7f85278cf8c5` | 0 |
| src/libxrpl/json/JsonPropertyStream.cpp | 2670 | `c1af34127b07c42f903af2fb8c3da110338288341896d06ae2de0fae114bb8ee` | 0 |
| src/libxrpl/json/json_reader.cpp | 21285 | `3abb0d523bdcb2203bf3db9df3f9e461bffa1327a1d06d03c70055fc0423e5cb` | 0 |
| src/libxrpl/json/json_value.cpp | 30639 | `d869014a12318e0f9c5c53389ef9e407a8fd0f2a2423bab4f1e8c26bbc541b9d` | 0 |
| src/libxrpl/json/json_valueiterator.cpp | 4351 | `a75719668d21037cc8d82f3dbe3410c5229e614c94d1a5a74d5cb078d0bcda9b` | 0 |
| src/libxrpl/json/json_writer.cpp | 17489 | `54e814f187ba628f246c70074ba050732afb84e6f7b646fab41f3e573c895564` | 0 |
| src/libxrpl/json/to_string.cpp | 297 | `d5bb9af2b721a4f0857965b807812101369cc3611d77f442c8b41b716f374aec` | 0 |
| src/libxrpl/ledger/AcceptedLedgerTx.cpp | 2485 | `ce27c79a5fde743d964f0a2bd526305a973d8b4872c3c1cd2b74409055813fd7` | 0 |
| src/libxrpl/ledger/ApplyStateTable.cpp | 20333 | `c17e3ddb18178644eaf600919aa857f0e8e364b8af9a73f475cba7ca4f1ce7b6` | 0 |
| src/libxrpl/ledger/ApplyView.cpp | 12601 | `033a39858b19025e73564d18ed6ed49361238f216686edc847bc966159316b56` | 0 |
| src/libxrpl/ledger/ApplyViewBase.cpp | 2738 | `bfb5fbdf9ff56a9aa2b085b64a3b638b902cefd07d3d5476d151abbc6edff372` | 0 |
| src/libxrpl/ledger/ApplyViewImpl.cpp | 1141 | `0a7f2577f05040271cd4d77af254c600503eb3af0f135722681c9a60d3ec9ccd` | 0 |
| src/libxrpl/ledger/CachedView.cpp | 2020 | `6762e1055d6ccc3148b44da45358534f24dbbe0898252e9dc61d746688344946` | 0 |
| src/libxrpl/ledger/CanonicalTXSet.cpp | 2311 | `26278c4f7cc774974dc0fecf20707e63ab45df19a7e00f15752061dbbf6da5d9` | 0 |
| src/libxrpl/ledger/Ledger.cpp | 27622 | `1adc75be8f7bacacf514015365435e18d5be6d5ecb38fb18eab50f1f0e181e9f` | 0 |
| src/libxrpl/ledger/OpenView.cpp | 6148 | `0e5cc4f3e4e6d897aba4c90280a247e6f4ad9a841e612d6e66218d424802d369` | 0 |
| src/libxrpl/ledger/PaymentSandbox.cpp | 13130 | `9d9a8e0efd195299cdf0ce10f594ce69a0155a1cd657d4bf2250a95a148ebdfe` | 0 |
| src/libxrpl/ledger/RawStateTable.cpp | 8821 | `cba82982b82675f6657f22d3fbad9634e683445040fc7057b9cc4e85ad7ae80a` | 0 |
| src/libxrpl/ledger/ReadView.cpp | 1773 | `ca6b73cdee5f5d0e94a92624e0cefc8fd1311ea91cc414ec1be62ae21c70776d` | 0 |
| src/libxrpl/ledger/View.cpp | 21880 | `29489665fdbd54dc7ef9f42cce8badcb4747107d99ce78a252319fcb7c39dfeb` | 0 |
| src/libxrpl/ledger/helpers/AMMHelpers.cpp | 32786 | `0f90fd188e43c73268a548d465f32fdda210553ba105285a4cbad4c751aa24da` | 0 |
| src/libxrpl/ledger/helpers/AccountRootHelpers.cpp | 22356 | `ef89398aceb734e9759b32785d772732f2c6423f8981b574b83a277281569857` | 0 |
| src/libxrpl/ledger/helpers/CredentialHelpers.cpp | 13424 | `08c80675d80851b1e87b38e06888cc0eb61d09ea6f4f12af7d880bbd34c0c7b6` | 0 |
| src/libxrpl/ledger/helpers/DirectoryHelpers.cpp | 4840 | `3952662fad6bd31ed3dc539badd19e025f525c90347c8d7af1c213d71b8e7f29` | 0 |
| src/libxrpl/ledger/helpers/LendingHelpers.cpp | 98047 | `c51446edfc7d51a0b8d3212ca8951bce4a60a0fdd8b9d5d848f492b8b5480537` | 0 |
| src/libxrpl/ledger/helpers/MPTokenHelpers.cpp | 38487 | `b25f7611a984390ccd964f387f5e70dcd37ef34be848d79cce711e47cee2d387` | 0 |
| src/libxrpl/ledger/helpers/NFTokenHelpers.cpp | 35747 | `ee0be1fabd232000cf1b7bb39cff2707e0264fcb213ad65b3b4b44e4b7fa4939` | 0 |
| src/libxrpl/ledger/helpers/OfferHelpers.cpp | 1982 | `a117d964f60ee7bcb135d3eeb1cfba9e3b99cb1c62d2c943b0f5c742dffbcd4c` | 0 |
| src/libxrpl/ledger/helpers/PaymentChannelHelpers.cpp | 2893 | `11040c638458dd62a0bfe3dbc25f01b6909480595a34da0796e38f82279a8570` | 0 |
| src/libxrpl/ledger/helpers/PermissionedDEXHelpers.cpp | 3539 | `ce6968b0193d31c0e167dc6671e6dcbd14f48178f2d044b03d58345dc35c4677` | 0 |
| src/libxrpl/ledger/helpers/ProposalHelpers.cpp | 6462 | `8118255b3940b05ff7d065412f7b9e9a7b84c379e2026296999521cd977ca045` | 0 |
| src/libxrpl/ledger/helpers/RippleStateHelpers.cpp | 27790 | `89106546cd821965ac8d1a39b4aefbc6c29e58e5d403043fba7d3d52d1df8e50` | 0 |
| src/libxrpl/ledger/helpers/SponsorHelpers.cpp | 12033 | `21cbdd7334d31a12d6b2e88a7d077b18c1a38e03b10e9a5f67aa7143d8492d74` | 0 |
| src/libxrpl/ledger/helpers/TokenHelpers.cpp | 54821 | `e80d315297b791a2374b110beeea5c8b1b6ed6e767f67388793ad4bbf963f913` | 0 |
| src/libxrpl/ledger/helpers/VaultHelpers.cpp | 31709 | `b727a5e902db734dc1be8475b0c735af25600f66aca8a90a11c710eb7b71d759` | 0 |
| src/libxrpl/net/HTTPClient.cpp | 17920 | `b38d126014404303a693e390501bb884419a73e2349efa4f533d56394e974f9d` | 0 |
| src/libxrpl/net/RegisterSSLCerts.cpp | 2848 | `41cf1c2c2abc9f1089385801a779c0530f134fbfd128a6112a64f9188ce69df5` | 0 |
| src/libxrpl/nodestore/BatchWriter.cpp | 2468 | `32861b4d70cbd8168ec43364da52a2d706ea7675c962fc5bb67cda4a74e31a3a` | 0 |
| src/libxrpl/nodestore/Database.cpp | 9747 | `719d99d14c20c034c2bedf71dd4348983103eb809a524a6ea439c3d0fb2ba60c` | 0 |
| src/libxrpl/nodestore/DatabaseNodeImp.cpp | 3671 | `b3ff03952e276726fd612c1861100039ddf83304d586ab9eb761d02da6eb126a` | 0 |
| src/libxrpl/nodestore/DatabaseRotatingImp.cpp | 6688 | `fa4d3861c2b51fd530417fa7f294601e881d74672de90988651e38a2f88d3046` | 0 |
| src/libxrpl/nodestore/DecodedBlob.cpp | 1754 | `369052d57183a88218574555680d2f8254e2ea789faa89cf09c831666b4f1a43` | 0 |
| src/libxrpl/nodestore/DummyScheduler.cpp | 433 | `3133ff735b96ddeab6401ae1b2748e5387dc1d3a4f38a8d1adc89d8a13584bef` | 0 |
| src/libxrpl/nodestore/ManagerImp.cpp | 3450 | `d918f4ff6174a8da5b1ab4e81cd7baa40c8d3b40efb67524fd827e60a20bd6ce` | 0 |
| src/libxrpl/nodestore/NodeObject.cpp | 813 | `e40b94176299c4792bf50a5a05467d9c39514b5cb9505d2327ea72aa62ed836e` | 0 |
| src/libxrpl/nodestore/backend/MemoryFactory.cpp | 4918 | `50f2c53600a48648f92f3ca41d8cd6b5cbfc99d65b72f7e17bca91214c8b5c79` | 0 |
| src/libxrpl/nodestore/backend/NuDBFactory.cpp | 12813 | `036f0ca86f60dbd52886ae70d00acb0e5f17ff61d2168f5f96a698ad8733d728` | 0 |
| src/libxrpl/nodestore/backend/NullFactory.cpp | 2202 | `5544b75b40089fad1c784e28f10b3de9b6afa712f2c4ef48ff975fac7a4acbd9` | 0 |
| src/libxrpl/nodestore/backend/RocksDBFactory.cpp | 13164 | `7f707c863c6bbd0c70c22cd6f3aacc629d549e880cb4a3888d35cc83ef8609a8` | 0 |
| src/libxrpl/peerfinder/Bootcache.cpp | 6917 | `ab9dc7b22eb07920797ac644cc4b2c51460611cee4ea75399c752e417ee91d56` | 0 |
| src/libxrpl/peerfinder/Config.cpp | 4354 | `b51727c2d2cf06a7a3ab1a9c06da7a270301f91193314050cdc34a59b5c368bc` | 0 |
| src/libxrpl/peerfinder/Endpoint.cpp | 341 | `13469d4ab9316d6f08b6bfc94ea61495ba4aad3e8a752d0050169c7c1a43f66a` | 0 |
| src/libxrpl/peerfinder/PeerfinderManager.cpp | 7346 | `53be111a933ccfc149b44be5490fd4e0bf1d0541e5d4443a3aef778812899df8` | 0 |
| src/libxrpl/peerfinder/SlotImp.cpp | 3728 | `6845dcc81f9a15253c18db636b5a55761a782d4b5637ba871ff82b3f61cb3cf4` | 0 |
| src/libxrpl/peerfinder/SourceStrings.cpp | 1392 | `d32b9d12207a7d581580333de7b6c3b4f36072ad5aa45a8a74713b0c7b81392e` | 0 |
| src/libxrpl/protocol/AMMCore.cpp | 3981 | `be858023d8a56f81d1ef8b814edf342147f5e22c522c21046dde37613576f052` | 0 |
| src/libxrpl/protocol/AccountID.cpp | 4994 | `72a4d64746eeecb78a33f30cae3e7a5587bea2fdeb00346fc8cfc724b37605c9` | 0 |
| src/libxrpl/protocol/Asset.cpp | 1760 | `aeb008d99ec6c9c06d45de2475383ad6677d50ee27ae51319b2a33176f26097f` | 0 |
| src/libxrpl/protocol/Book.cpp | 561 | `1b9f8b2437ca5dda5519ff2d0be2455d7076040ffadb4bcf6964f35e158d145d` | 0 |
| src/libxrpl/protocol/BuildInfo.cpp | 4500 | `65e6dabcb846184096fcb16590db809fa32b3f4e0e5a656be8760958d4232768` | 0 |
| src/libxrpl/protocol/ConfidentialTransfer.cpp | 19386 | `f181c37ad0e458929525541f9d718102e745f1206d0d70d6a683573ef70163c1` | 0 |
| src/libxrpl/protocol/ErrorCodes.cpp | 10677 | `0132b1dd3d2afd1e4dd4e4f1eba64c4c519878cf4cfa5a4277904c8b0ee73534` | 0 |
| src/libxrpl/protocol/Feature.cpp | 14021 | `b721b6a5c0a9f3b91352163a61f31ee6ca228a45a11da7006932142fe3c1497b` | 0 |
| src/libxrpl/protocol/IOUAmount.cpp | 6320 | `2ae9b3af56136a15f3d57744fe966376d75deea1c72afc40c712f1ec5257809e` | 0 |
| src/libxrpl/protocol/Indexes.cpp | 18054 | `3a08568998743ba3eabad58a97e7ba457c4882368f256bc99c566fb313ebebab` | 0 |
| src/libxrpl/protocol/InnerObjectFormats.cpp | 3587 | `c0ebacd0a3c1df4a42d612a1bad7fd283f82d06ce12644cb806c83325ff5324b` | 0 |
| src/libxrpl/protocol/Issue.cpp | 2855 | `78f4b4eab9ec377fe25f48ed4b931cf4ad559cf2f4faccea59ccaee842658b59` | 0 |
| src/libxrpl/protocol/Keylet.cpp | 559 | `71e4f0b73f7d4138d150e9919edbde2488159550f8b072ef6a50e971b5015ceb` | 0 |
| src/libxrpl/protocol/LedgerFormats.cpp | 1089 | `6775a368d73f659e81ddef30b742489d7f7bcac96089296e747aaab34b983b28` | 0 |
| src/libxrpl/protocol/LedgerHeader.cpp | 2076 | `b90409089f5ecea143a085e924cb8f2353f8ee1214b7ec39c705481a67a110d0` | 0 |
| src/libxrpl/protocol/MPTAmount.cpp | 1405 | `1c888d9a80b9f9bb4c7362388e0333a801e411996ce6a1cc990f20019396b0c6` | 0 |
| src/libxrpl/protocol/MPTIssue.cpp | 2196 | `6feab49157ae215cb02feddf572d46db70581ea3680c529d2469be3207629cdd` | 0 |
| src/libxrpl/protocol/NFTokenID.cpp | 6098 | `d2dc1ad7d5d3ef60787845593e78769318774366f119e61f6c606dafd4e8225b` | 0 |
| src/libxrpl/protocol/NFTokenOfferID.cpp | 1752 | `a26c9561f33655d9c4d62f72cf71a5c87c28b15eed4591bd0d0cd5e2f3bf5a98` | 0 |
| src/libxrpl/protocol/PathAsset.cpp | 383 | `e5c33046c04d48cb1a9c1beed12461acb12a81d233ea467ffd4694ee4504055e` | 0 |
| src/libxrpl/protocol/Permissions.cpp | 9589 | `9d31a58d21eb3e3cc6759a7d61ac21010e5846be9036d9285af4dc15e0b72221` | 0 |
| src/libxrpl/protocol/Protocol.cpp | 242 | `6b569f79c2873c4f2eb1186b41d4ac923af7e0dd29a6fdf738ac41ef7e0f1bf7` | 0 |
| src/libxrpl/protocol/PublicKey.cpp | 8580 | `767817e23a365a20bac17e99cce51bb5d3e2281b71ee0f80ff94ec11c92537c1` | 0 |
| src/libxrpl/protocol/Quality.cpp | 5840 | `50084253886010b09e65fdb992707d95d89329e9ce7c9a019af04f4010c706d1` | 0 |
| src/libxrpl/protocol/QualityFunction.cpp | 1810 | `197b52af1764ce74010ab8118c076e72af99a11693f180e6ca2a2d99ecd89329` | 0 |
| src/libxrpl/protocol/RPCErr.cpp | 529 | `29c51376bd8538db547e12d86d3874d699e837227f48ec80156d7393d752c865` | 0 |
| src/libxrpl/protocol/Rate2.cpp | 2321 | `8afbb3a0b637cfc6e52d7cd03a15693ea5fd6b9904673d669acb31d438538af5` | 0 |
| src/libxrpl/protocol/Rules.cpp | 6386 | `53d447666d9ed2126ccfeb862ce47052ba524ea5e244f8bd334f0dd647eb2546` | 0 |
| src/libxrpl/protocol/SField.cpp | 4149 | `1ece4a9bee30878a7eace7385df32d608df8565969d2667f726d8ac209a72197` | 0 |
| src/libxrpl/protocol/SOTemplate.cpp | 1808 | `0cf9aae9d39b1ef6a267e8c638388488ea2938f661ed9cd30253a14034c4a78d` | 0 |
| src/libxrpl/protocol/STAccount.cpp | 2594 | `9a701f0e88883e3eba2ae57ddc7851b04ade2d8749db779fe2709ed65c78034a` | 0 |
| src/libxrpl/protocol/STAmount.cpp | 54196 | `cacae816b92a36f51c63f80a5ccded482bd2538a50c1d39f6e47b98ba3a814b6` | 0 |
| src/libxrpl/protocol/STArray.cpp | 3461 | `1a606dd8468f980a6f9015d01f5963986adff9a03057fc3ccee7064d2a7e0591` | 0 |
| src/libxrpl/protocol/STBase.cpp | 2416 | `39aff027633336224dd38a15855a235d4006ed2d5447352df78c22f8dfda4e1e` | 0 |
| src/libxrpl/protocol/STBlob.cpp | 1276 | `f0629ffdb053916b9785bfa9821ecddb90413fdc55517d74a0181c9b43f31030` | 0 |
| src/libxrpl/protocol/STCurrency.cpp | 2024 | `1a48d90078989c1fad9386f7a2969e62d8dab257d49ff364d5f3562d289eb637` | 0 |
| src/libxrpl/protocol/STInteger.cpp | 5451 | `e3fda666fb98eb976878d465e5291cc193f89afd1ef177427cd97c67f70b7e70` | 0 |
| src/libxrpl/protocol/STIssue.cpp | 3924 | `97d179ace07d97d72aed8e483a544b7deab1c8fafd36389dafc109fe3205f70d` | 0 |
| src/libxrpl/protocol/STLedgerEntry.cpp | 4521 | `d083cca15ff361e442be1f588f1df21cc2008af14176b1113b090ddaed4b4a24` | 0 |
| src/libxrpl/protocol/STNumber.cpp | 8522 | `32ef0d1ee3a8f397bab088117480c4367de6da02c673e5f7ab829aa8b6cd80e2` | 0 |
| src/libxrpl/protocol/STObject.cpp | 21877 | `0e0a445455524b7e5b53723f7e403c15a72c7b8bfe2091871ed122d2a0c7baef` | 0 |
| src/libxrpl/protocol/STParsedJSON.cpp | 37122 | `f06459f32e35b391353e63ceddf56dd0c09f1841fae14271b04f974a17d7381d` | 0 |
| src/libxrpl/protocol/STPathSet.cpp | 9232 | `79c2d765ac16b70c2db387b6cea990e156a9a8c4c9ed4bb9d8b7a31dfd83c972` | 0 |
| src/libxrpl/protocol/STTakesAsset.cpp | 1770 | `1608601e8c0e756bfc5b8ba96e8b439a868f50732373e3cc0bb5fbe003610f89` | 0 |
| src/libxrpl/protocol/STTx.cpp | 27795 | `4a755b9aa7432b4e8fb9c73a15f27711cdcbc7b551e9dba7fc39119ca4f0d89a` | 0 |
| src/libxrpl/protocol/STValidation.cpp | 4544 | `00fac888640247f81d2db31f2a248a4ab1596dccb35e50127a7f0efb566f5b4f` | 0 |
| src/libxrpl/protocol/STVar.cpp | 5848 | `6fbf3b11ae0b4093f4e7214f9c68c7d211265bf2334604ef3138d9a1330a0d04` | 0 |
| src/libxrpl/protocol/STVector256.cpp | 1967 | `660901e78903805f0bde7a4203f5975d1edbcef530ebc2136e151087d59d3763` | 0 |
| src/libxrpl/protocol/SecretKey.cpp | 11259 | `e2ad569a109ca9c25fd32e983740ba5b38421a89263805f1c4f83141837c4353` | 0 |
| src/libxrpl/protocol/Seed.cpp | 3043 | `a9209f402382a5f82e5473e7d5518d567ccae072f4bdc48c6226c9d6bc829ab9` | 0 |
| src/libxrpl/protocol/Serializer.cpp | 13901 | `f115ea79a9bb1c74f7b08abb465179fa49888da4f16f5cf2806b8874ad2a776d` | 0 |
| src/libxrpl/protocol/Sign.cpp | 5201 | `193a7b0c15d8eff1fa39fad75534ef0826ba47cadcd6a8711c21f56e598748c8` | 0 |
| src/libxrpl/protocol/TER.cpp | 21211 | `564414c67817b0335f1895fc90c931be9799453411494cc4427b782d4d23a0f3` | 0 |
| src/libxrpl/protocol/TxFormats.cpp | 1751 | `fc9eff792853e07214933d6bf0ca6a9a4bf8402e22f682e2636eb78b71112afb` | 0 |
| src/libxrpl/protocol/TxMeta.cpp | 8659 | `66e2e43a31041ee1ebdb252b1361c77daebb6b6729be41fbc7c4359680d79a20` | 0 |
| src/libxrpl/protocol/UintTypes.cpp | 2732 | `15d25733a863637b400bf8a666c316e4ec0d48c6ab986fd280ab877892f3e31b` | 0 |
| src/libxrpl/protocol/XRPAmount.cpp | 1291 | `7939c6c27edfde15a877957875ab6d7a9b4448564af85441eb0830706a9d0373` | 0 |
| src/libxrpl/protocol/digest.cpp | 2127 | `b0b1b8e0ace1c821e9a4cd275df39f6211c8cda54e9370cfa3e942d73e883a8d` | 0 |
| src/libxrpl/protocol/tokens.cpp | 23228 | `1434dedc41762c26f1a60898d47d53c2a7f91f5ed0bc35814d2eb2e2d70359b7` | 0 |
| src/libxrpl/protocol_autogen/placeholder.cpp | 82 | `17ea10c5faea38363cdcc0d0c8d1689ca70629839c8195809246908c976ecf8e` | 0 |
| src/libxrpl/rdb/DatabaseCon.cpp | 2755 | `9b4fb76d52d343cfc7fa2713642370c3fba079c3cd358f63b3aae77120642f6e` | 0 |
| src/libxrpl/rdb/SociDB.cpp | 9086 | `0350d420a4b81068de11f4c0cec6d6d72fd97b4f9bde1483ce029d86f3b2d5e8` | 0 |
| src/libxrpl/resource/Charge.cpp | 917 | `9bc4b8673cffd0e6e5503c88499c788e3bc1865fe805416872e435d216e19693` | 0 |
| src/libxrpl/resource/Consumer.cpp | 2933 | `203563f8f669bd70a057f4049fd662f32152790fed9bfca859d9bf222d792012` | 0 |
| src/libxrpl/resource/Fees.cpp | 1082 | `b6e409ad69cbef9e9b02452e776a2a031853266feefd4ca41aa75e39822e7ab8` | 0 |
| src/libxrpl/resource/ResourceManager.cpp | 4275 | `bf506e1bbc6612f9ce9de07668fbdde3f720cfcb37985c17bdb236be989ca0de` | 0 |
| src/libxrpl/server/InfoSub.cpp | 10035 | `2ec248ce5860d3d8fd0268d33d1011e15a9785ba95e440b0c7e4f8754d57b88a` | 0 |
| src/libxrpl/server/JSONRPCUtil.cpp | 4040 | `7556ce189a05736cd46ad2f984195af62d20224997b5dd90571c014689fba9d3` | 0 |
| src/libxrpl/server/LoadFeeTrack.cpp | 2305 | `f9ffab1ef414b770851fe14825d1a76dcbd5722867b2f1858427b0601d8e35c8` | 0 |
| src/libxrpl/server/Manifest.cpp | 21394 | `6ecba1ae5cb811d4ee1d4768eca9348d13d8cf907fac74d9eaa90e1c867c868d` | 0 |
| src/libxrpl/server/Port.cpp | 9983 | `cffcc172480c20ff9bc3d7811ae28a9099334e5eefd9b77e8cf473066cb3908c` | 0 |
| src/libxrpl/server/State.cpp | 3301 | `de7af1239c38628597fa73cb78afdd11bc76dc8ec900d5d8924dbb66bfb9feb9` | 0 |
| src/libxrpl/server/Vacuum.cpp | 1893 | `03da5e52c136fc52cdebabb015e7890a1df07fbeea2ae4cc4e60617f399e90cf` | 0 |
| src/libxrpl/server/Wallet.cpp | 10160 | `5d39def3bdb0773cacc46ad59921baf3d0ba5910ad52d0b05e31c4da703c8a06` | 0 |
| src/libxrpl/shamap/SHAMap.cpp | 35202 | `9f754600c81d67762434159dec2e2162f35c4880c37aa62440482b3c2a43e658` | 0 |
| src/libxrpl/shamap/SHAMapDelta.cpp | 13373 | `763a441e00bd5baf47f5a17eb82f138849e99f6630bbafea55fa3552f37ef04f` | 0 |
| src/libxrpl/shamap/SHAMapInnerNode.cpp | 14138 | `4a6cf403b62c181d84e32a2245ce98f62865b11c8bedab555d5db112f089ea3e` | 0 |
| src/libxrpl/shamap/SHAMapLeafNode.cpp | 2438 | `be5f4d19695c7607bdbb5c49f1139a549c75f24e45270708e84beb68ce9b0cea` | 0 |
| src/libxrpl/shamap/SHAMapNodeID.cpp | 6144 | `c37d447ad8ab875648a6c1190f1bf645c6c6814e47408c38797c96c0eb49ff88` | 0 |
| src/libxrpl/shamap/SHAMapSync.cpp | 32039 | `cb9d04345df197b19190e5d6c4af397d0eaa7d45ddf4ea71b243141c5437371b` | 0 |
| src/libxrpl/shamap/SHAMapTreeNode.cpp | 5832 | `3e392cec122187ff76ac71058f988471174887d84c307e2abd9cb97e411bd9ba` | 0 |
| src/libxrpl/tx/ApplyContext.cpp | 1860 | `62772b01a6663eb35fc93887a9c42c2d2cf59618a8503c613ad65b8b564bca87` | 0 |
| src/libxrpl/tx/SignerEntries.cpp | 1643 | `bf874e5ee3744030ab431e2126b42307985c7e81abe5e1c4877bdeaafefa7ccc` | 0 |
| src/libxrpl/tx/Transactor.cpp | 58904 | `f5ef9829e27747bc11b5ded20023aea5b13f438286952840715640b01b9f7c40` | 0 |
| src/libxrpl/tx/apply.cpp | 11789 | `656182354ab102ca5e775d9bd7effbe40132ca4a5e9fcc05aaab076b0d67f717` | 0 |
| src/libxrpl/tx/applySteps.cpp | 16626 | `2bc2fc54aea69dbce37c3a24325e3529df079afc7d63d6e57e0b96a70288c504` | 0 |
| src/libxrpl/tx/invariants/AMMInvariant.cpp | 12045 | `1f11d15e95189187b2cdb7bff2170f1e9d0371c9196387971649ac23d0b05bf9` | 0 |
| src/libxrpl/tx/invariants/CosignerInvariant.cpp | 7187 | `ad0d71d934d5328cb620326ee351a9965da2ab57da4b554046e73609beef1412` | 0 |
| src/libxrpl/tx/invariants/DirectoryInvariant.cpp | 3203 | `6ba5e39f4fc6727d1475e40e4c4d312f765579c0652a09143789bf5000be9e0e` | 0 |
| src/libxrpl/tx/invariants/FreezeInvariant.cpp | 12410 | `fe72bee412b64f5856780ec10c677de9f3d081b98796f03c75bbecffb57fd3ee` | 0 |
| src/libxrpl/tx/invariants/InvariantCheck.cpp | 49469 | `24d77056919d08e8088a3cdf5c538e906b2c32c7f7bc265d7d55a27c2af19e63` | 0 |
| src/libxrpl/tx/invariants/InvariantRunner.cpp | 3539 | `fab192f80cedd5b67959063c959bef29b5623255524fa47534a5cda970ef4d8f` | 0 |
| src/libxrpl/tx/invariants/LoanBrokerInvariant.cpp | 11732 | `8e384dfc900988f2f68dc0f7534bb539ca056c0df110592287175fa8ce356dfe` | 0 |
| src/libxrpl/tx/invariants/LoanInvariant.cpp | 13602 | `130513374f33d134f77aa02defcfb62af9534c3b78118b4842abc9807a544afd` | 0 |
| src/libxrpl/tx/invariants/MPTInvariant.cpp | 45795 | `eb1adc7b2aa29acddff5446f94acba2157a897217be144510bb93a1158432be7` | 0 |
| src/libxrpl/tx/invariants/NFTInvariant.cpp | 8712 | `cbba6dd8192bcb58182b6651e552f95c92981c9209c799cf2bdda8c7bb6afb6b` | 0 |
| src/libxrpl/tx/invariants/PermissionedDEXInvariant.cpp | 4000 | `e470236a0bc0a2b15c36323eb5ef1affe59f093468bb8a69d5f99aee857bd933` | 0 |
| src/libxrpl/tx/invariants/PermissionedDomainInvariant.cpp | 5773 | `f0408b2ed17761d49a7eb41bd0768466c3d6a7025b47a15ac1fcfb31aaef4697` | 0 |
| src/libxrpl/tx/invariants/SponsorshipInvariant.cpp | 5429 | `f99ee415eeba2ccbe7e60b9a8dca88bd5d85bd4c3116dc5f6074868c67be9bee` | 0 |
| src/libxrpl/tx/invariants/VaultInvariant.cpp | 64631 | `f4d6b4ac9505ddf841904f6d3cc09bd34062d8bc888b4d4eb230c598f5ca6f39` | 0 |
| src/libxrpl/tx/paths/AMMLiquidity.cpp | 8315 | `1ca13acb67697bddc473d74c7e756a785118d806906fcad66fd5397c89cf9afa` | 0 |
| src/libxrpl/tx/paths/AMMOffer.cpp | 6017 | `2bef8e30e6acaf822a8e408e899c09845993a4b080d972e100c4294aea5faa2a` | 0 |
| src/libxrpl/tx/paths/BookStep.cpp | 67408 | `4006cf5a99e90ad5774017b1de9f1f7d7d654bdee19cc1f2136bcd12bc39c651` | 0 |
| src/libxrpl/tx/paths/BookTip.cpp | 1667 | `c4d2879faece714d75e284dcb94659593a6c5f049dc04b6f4a84b4ad015bea32` | 0 |
| src/libxrpl/tx/paths/DirectStep.cpp | 31024 | `fb3e4de667837a7f46ff4a67594565ab93684075e09d4a720da5b449669c14ca` | 0 |
| src/libxrpl/tx/paths/Flow.cpp | 4297 | `e42394c97a98f6ca52e69369b174df2e9c7afacf794b998408365994c55c2cf1` | 0 |
| src/libxrpl/tx/paths/MPTEndpointStep.cpp | 33254 | `38e0abec7fd913ae5b949b4b76b024783472115fa294878e6e4c64f66809f608` | 0 |
| src/libxrpl/tx/paths/OfferStream.cpp | 14990 | `16ee449c43277c1c4e299374546dfbe4eba57a66e4d01c5c5a025ebba7c1654b` | 0 |
| src/libxrpl/tx/paths/PaySteps.cpp | 25965 | `36e31f5020cd437178d95bfb5493184cc13012043e2572e4ffa9b6d66b49e07a` | 0 |
| src/libxrpl/tx/paths/RippleCalc.cpp | 3476 | `60a059bd6f92952328fbee24edc58fee88f35ec583648e279a6a0dd5e97a0258` | 0 |
| src/libxrpl/tx/paths/XRPEndpointStep.cpp | 11996 | `b72c16096699eb929e69eeb54e9c69b2526d5bba25acf3a257921d47cf57e026` | 0 |
| src/libxrpl/tx/transactors/account/AccountDelete.cpp | 14975 | `1bbd20aa9c0dc2d571d2149f4015b0ceca22a1391172daa8993112efb128d963` | 0 |
| src/libxrpl/tx/transactors/account/AccountSet.cpp | 16861 | `16b43ee17e593dc005096f6cfdcecdfbae3a537bf349ffe467d3968fdc0425d9` | 0 |
| src/libxrpl/tx/transactors/account/SetRegularKey.cpp | 2493 | `9cdf6af492bcfdccedeafdff48a7e5fbf53ca7f704a0a8b56ce2dace95a34acf` | 0 |
| src/libxrpl/tx/transactors/account/SignerListSet.cpp | 14007 | `2935421fba9e246c74b5c6c5f61ae7e9b1391eddcb8d4e633808e4abbc8d18e4` | 0 |
| src/libxrpl/tx/transactors/check/CheckCancel.cpp | 3748 | `edca4e5ed46fe0b8c9b34445393261ec027b4c738e38182bb9a08b98821005a9` | 0 |
| src/libxrpl/tx/transactors/check/CheckCash.cpp | 26626 | `95819a1e2031e1aca6ab58da3e6798e324c0399ca4fd7d7a8e9b98e6c8c51e70` | 0 |
| src/libxrpl/tx/transactors/check/CheckCreate.cpp | 10051 | `cc2b3973c8736f732b76fff32626012e0af2172194997bdf18a44f95b3386ea6` | 0 |
| src/libxrpl/tx/transactors/credentials/CredentialAccept.cpp | 4803 | `c532895d1f73c98ffcd67656a46e62cf6fc098cd5ccf9724faf5f89950774293` | 0 |
| src/libxrpl/tx/transactors/credentials/CredentialCreate.cpp | 6201 | `bf460f2dcc43de47b308ef0386671cef126e4bf45e3f0a007a0ca9d7c44ca093` | 0 |
| src/libxrpl/tx/transactors/credentials/CredentialDelete.cpp | 3262 | `7dc34f84a5e60e6de94f002fef0c2b8e7f79665c0aca5fac8a0ea5aa24bd1d79` | 0 |
| src/libxrpl/tx/transactors/delegate/DelegateSet.cpp | 5859 | `ec70ae84d278d8be29bd33c4cd31d811a7164febfee706e9bdb95d941d1b5df7` | 0 |
| src/libxrpl/tx/transactors/delegate/DelegateUtils.cpp | 1611 | `99f0055034e85bdbe0a77d444801bf8b336d5562b29e1082a336b3494a6bb489` | 0 |
| src/libxrpl/tx/transactors/dex/AMMBid.cpp | 12934 | `c2a8e584e014d729eb6470264f457755f3302d6f0bef03b8f77755120819706f` | 0 |
| src/libxrpl/tx/transactors/dex/AMMClawback.cpp | 13776 | `04c3d136e5a36b4e12f786ebdc14893c18575149d99dfd00731110eaba228ff7` | 0 |
| src/libxrpl/tx/transactors/dex/AMMCreate.cpp | 14848 | `f3d7b680c0a9b62100b9f33d2dbc6adc892e0eabfb30cdb2adcb754300398d49` | 0 |
| src/libxrpl/tx/transactors/dex/AMMDelete.cpp | 1989 | `cfb9df7ab58c1c785f842940e08e2582e5063c3900434471346e64fb28193741` | 0 |
| src/libxrpl/tx/transactors/dex/AMMDeposit.cpp | 38537 | `f653c4a57d48c7b33c3e75125f9343d36398751431ce6acaaa6e34d50f392557` | 0 |
| src/libxrpl/tx/transactors/dex/AMMVote.cpp | 8661 | `aec536399bb2a45e0901fd8aeaabb9d16f65ae08923fcee62341a1c3d5db9a19` | 0 |
| src/libxrpl/tx/transactors/dex/AMMWithdraw.cpp | 45937 | `fc4114714f27dc307538b437753b0b90bc9fc1f241bf39b9d1d43ec31a3716ed` | 0 |
| src/libxrpl/tx/transactors/dex/OfferCancel.cpp | 2316 | `e3f400b0b9efb578569a0475163df0d58ed6226f931794aaa982801e622b9a01` | 0 |
| src/libxrpl/tx/transactors/dex/OfferCreate.cpp | 42149 | `564b1fe96a112e8db5c1d399324c00d79ec6f848bab155d96c895b5dd993c560` | 0 |
| src/libxrpl/tx/transactors/did/DIDDelete.cpp | 2042 | `b1885c7e22a5ac6ef8104e0257db60a242b2567046d8259bcdfabf248fd80cb1` | 0 |
| src/libxrpl/tx/transactors/did/DIDSet.cpp | 4972 | `6c40c82d2425533cccd8c95f2047ab91e2f6bd042100938d62f435dfc2138253` | 0 |
| src/libxrpl/tx/transactors/escrow/EscrowCancel.cpp | 6077 | `23b30a7e8cfeddc752fb3077c7e994dd15b81cf92bb35a08eace77f6f2af1002` | 0 |
| src/libxrpl/tx/transactors/escrow/EscrowCreate.cpp | 15964 | `89ea90062311bb92325232338e7532af15c55135cefcc27e1c9cf97f6ddde815` | 0 |
| src/libxrpl/tx/transactors/escrow/EscrowFinish.cpp | 16056 | `bffc3a0042c2ff37a28677ccc5ce4f6d9b15fe496d95b9991291409209ab7a68` | 0 |
| src/libxrpl/tx/transactors/lending/LoanBrokerCoverClawback.cpp | 13915 | `f9c1ad0a4157ba19bedf039892d1be2bf3266f458d7267b2e07387ccbc3e290c` | 0 |
| src/libxrpl/tx/transactors/lending/LoanBrokerCoverDeposit.cpp | 7541 | `36afa280163792b2c18ef424e2af14c460d9d4d3f590c4156b3e1d85c2793a9d` | 0 |
| src/libxrpl/tx/transactors/lending/LoanBrokerCoverWithdraw.cpp | 9920 | `3c8dbe8d6b5c63745faacbe8d1bfbd6fa07104a2b1c1d17ef4cac0053b9b3715` | 0 |
| src/libxrpl/tx/transactors/lending/LoanBrokerDelete.cpp | 8675 | `64decc3d0abf2a22ceca75ac63c2ff645e9dbf27280d902d7bca5e50b23bf32e` | 0 |
| src/libxrpl/tx/transactors/lending/LoanBrokerSet.cpp | 13038 | `9c3f968629518bebc4e2c5243b7759a6f60e6f5c23ffe291517b40b8f430279d` | 0 |
| src/libxrpl/tx/transactors/lending/LoanDelete.cpp | 4818 | `8b9aeac0ff17146810bf9c37ee12bbaf709150a58bb67f02a91447c98c71cee0` | 0 |
| src/libxrpl/tx/transactors/lending/LoanManage.cpp | 22817 | `cbfee0f767973c854fc5cc8b95df4ddc38787a4cde975e81ab54baf4c67cf86a` | 0 |
| src/libxrpl/tx/transactors/lending/LoanPay.cpp | 38562 | `f7abd9f049ee281d3729a7e93a88ca07bca17178034b9e405ecb8e7e26406d32` | 0 |
| src/libxrpl/tx/transactors/lending/LoanSet.cpp | 31043 | `856158bf6deed151c169a5ef40f5f9cc54e69cac0283918c11a6cbb763656df8` | 0 |
| src/libxrpl/tx/transactors/nft/NFTokenAcceptOffer.cpp | 21030 | `1954038f6e116fe13037ccb2b90300fb2bcd309f9b7c51ab791c71002935f380` | 0 |
| src/libxrpl/tx/transactors/nft/NFTokenBurn.cpp | 3257 | `0243e3ad569f5c3b7eaad6c41474ce5d5e8ebb58e8233c315b2a850b131a3a29` | 0 |
| src/libxrpl/tx/transactors/nft/NFTokenCancelOffer.cpp | 3426 | `2cb9176cd9795cb326822c816ecc5385f46c4cd6c2755fcefc3eb70b0dc9004c` | 0 |
| src/libxrpl/tx/transactors/nft/NFTokenCreateOffer.cpp | 2821 | `d4ec990e9fd58a8d59dfb0680d2ac5b732c2c3c3b441f909fb07a3b62cbc3c32` | 0 |
| src/libxrpl/tx/transactors/nft/NFTokenMint.cpp | 12802 | `b1c569b763c9f71f1d67821d06dc4f080ea2584273caabf5c4cc6b4a4a74912f` | 0 |
| src/libxrpl/tx/transactors/nft/NFTokenModify.cpp | 2353 | `a5c0b86fdba6deb9164e47574401c2c21bbeafe7ae884da928011bb8277c6654` | 0 |
| src/libxrpl/tx/transactors/oracle/OracleDelete.cpp | 2758 | `17ee239787eb66c3b47f866f66ca6c5d76fd3201ee03efe06bdf40c0be996843` | 0 |
| src/libxrpl/tx/transactors/oracle/OracleSet.cpp | 12159 | `192f76e8b04ef7f589290f428432eda37737e7e2087370c0834ee2b3f4f32c5b` | 0 |
| src/libxrpl/tx/transactors/payment/DepositPreauth.cpp | 11592 | `9ec39ee381c708739ebb74a0de68b8a2f372417dedffd3256ca138f2c393382b` | 0 |
| src/libxrpl/tx/transactors/payment/Payment.cpp | 34817 | `55e49f8467f26ae61770cf497820679f00d9abb44a654dd5ab1e74280ea4aa3b` | 0 |
| src/libxrpl/tx/transactors/payment_channel/PaymentChannelClaim.cpp | 6771 | `28c5b655c32a7bff6c6e6251a78d5c6e809a466a44aabcae25cfe927f15189b4` | 0 |
| src/libxrpl/tx/transactors/payment_channel/PaymentChannelCreate.cpp | 8814 | `d92e337a583e554a0b1633a3c82b37b0e2f7d07aaf0a650fef1176e6bbbcb32c` | 0 |
| src/libxrpl/tx/transactors/payment_channel/PaymentChannelFund.cpp | 4421 | `fa0b7472f29e65653966eef13ca8b199aeb4bb83e38fcc00d5a47a402077b384` | 0 |
| src/libxrpl/tx/transactors/permissioned_domain/PermissionedDomainDelete.cpp | 2668 | `1d4e2cacf0323d11af9147e7654ba2bed0c9c6dfbe386fed2f4ac00c8b43ba25` | 0 |
| src/libxrpl/tx/transactors/permissioned_domain/PermissionedDomainSet.cpp | 5029 | `cbf03d47a59153a8b1e84aa76b4b74c632c8db54d1cddf911535c8075b0affbd` | 0 |
| src/libxrpl/tx/transactors/proposal/TransactionProposalCancel.cpp | 4136 | `b4beba762013bdfe72bea93ad10081b4729c3042a4348b1be0aaeb29a0acdda1` | 0 |
| src/libxrpl/tx/transactors/proposal/TransactionProposalCreate.cpp | 15513 | `25538c7b040dea71c337cdae983a57f2516ffb7cbae37ac8f72e3f46c693e9d8` | 0 |
| src/libxrpl/tx/transactors/sponsor/SponsorshipSet.cpp | 17136 | `fe8fa111ea2efa37059563e9cb0640fa92edaad5bcdcc89624f5ef98da35121b` | 0 |
| src/libxrpl/tx/transactors/sponsor/SponsorshipTransfer.cpp | 21538 | `ea5c633b58aecc3397b71a6303943baca9bbf81b1e05ff374a3d6c76d60c8e6f` | 0 |
| src/libxrpl/tx/transactors/system/Batch.cpp | 23774 | `66f014cbedada42e3c890c5d4ae779fd3e4982cb1533a320238ece4260a3597e` | 0 |
| src/libxrpl/tx/transactors/system/Change.cpp | 13008 | `64e369f6585d12a4432792c6344485a2730821d3c056d1b02d009ac02f7069eb` | 0 |
| src/libxrpl/tx/transactors/system/LedgerStateFix.cpp | 4813 | `c6b421501c6db8801401318b55e89e1a1188479daaf507243fb00d36dcfd2128` | 0 |
| src/libxrpl/tx/transactors/system/TicketCreate.cpp | 5311 | `817e0cce26f1a8448c77005a779a0575af2e7b0fc6197bb356bd0fee9a42fff9` | 0 |
| src/libxrpl/tx/transactors/token/Clawback.cpp | 8187 | `cf384df74e565318cee8cf14428784a30a2f6a194d3bc4ca7131fc44087b826e` | 0 |
| src/libxrpl/tx/transactors/token/ConfidentialMPTClawback.cpp | 8592 | `5137fad7fe2a8406549126ac517ccc661666821fa35a5609eb1c03b0e9867bdc` | 0 |
| src/libxrpl/tx/transactors/token/ConfidentialMPTConvert.cpp | 13783 | `de93d6547406566d6197fdef914a7befe107181944cee3b578faf28885ae3181` | 0 |
| src/libxrpl/tx/transactors/token/ConfidentialMPTConvertBack.cpp | 11622 | `fc883d9d2b91c1eeca77049d9bddbd44eb8443553e32292af65bc88f0278d4b9` | 0 |
| src/libxrpl/tx/transactors/token/ConfidentialMPTHolderKeyUpdate.cpp | 7560 | `dc350cdbb57b0f3e3ccb108192924b7356fe12576b5f901db366b5fb1ac4dde7` | 0 |
| src/libxrpl/tx/transactors/token/ConfidentialMPTMergeInbox.cpp | 5274 | `1f5997f54f28ef0d7fac1a21ac7a077fdc11e0a32ce6732ba6be58891e028426` | 0 |
| src/libxrpl/tx/transactors/token/ConfidentialMPTMirrorUpdate.cpp | 10329 | `12f80ffa31cb7a8ae8f23e2b76ee44516ff83af41af4c49cd3232148b3561e71` | 0 |
| src/libxrpl/tx/transactors/token/ConfidentialMPTSend.cpp | 17237 | `192e32c5bf2561788d8c9fec5c89a3a89d8c453642c849dae3c81e948d6d1137` | 0 |
| src/libxrpl/tx/transactors/token/MPTokenAuthorize.cpp | 5966 | `e8ab08619ea5cbbbdd713d680e05681bd884d511fc15121be5f000bf57c8832b` | 0 |
| src/libxrpl/tx/transactors/token/MPTokenIssuanceCreate.cpp | 8239 | `cb4546b8ede122842503f7e9699248aa4e7799c45486a17fb410dbac8ee0269a` | 0 |
| src/libxrpl/tx/transactors/token/MPTokenIssuanceDestroy.cpp | 1997 | `e0f0730ba5541a426f131619e91ca180de078b3958cea9b5f324986f9a282b83` | 0 |
| src/libxrpl/tx/transactors/token/MPTokenIssuanceSet.cpp | 19305 | `cb5399afb255fa0eeac4c78fbf9c07b2b5fe17534dfd0ce38d41f9fc0729948e` | 0 |
| src/libxrpl/tx/transactors/token/TrustSet.cpp | 26117 | `189918c14e4b7290d9da75306728afc566c3f89b60bbd7704c634c5e89d5efb6` | 0 |
| src/libxrpl/tx/transactors/vault/VaultClawback.cpp | 21052 | `d69121a3469bac7797ac94efa4e1555e2f0ee1a0897c4a602a2cdaba03d704dd` | 0 |
| src/libxrpl/tx/transactors/vault/VaultCreate.cpp | 12817 | `3acebb3b575b534aaea489fd0da6abe751b481406f0f0eedd6fbbdcbbbcb4fba` | 0 |
| src/libxrpl/tx/transactors/vault/VaultDelete.cpp | 7510 | `7f9296f8ce7f6bac5ed251ce68a933ed4d4b9cf38fda4acc2adaf60505474e53` | 0 |
| src/libxrpl/tx/transactors/vault/VaultDeposit.cpp | 15915 | `d6dc878213d63a137217e77d15ac349553a8576e81988c97fe5c47379a39d8b6` | 0 |
| src/libxrpl/tx/transactors/vault/VaultSet.cpp | 7053 | `357a62f93e32d4e8b2ed8e483dccf361688bdd62c819e5584a8d5b665349c95a` | 0 |
| src/libxrpl/tx/transactors/vault/VaultWithdraw.cpp | 27264 | `0a33e1730b2990a6a9e5865cdcfbbcee29dbb3c237763efaad72a7553a09ac25` | 0 |
| src/xrpld/app/consensus/RCLConsensus.cpp | 35990 | `784ba13ecfba4b423efee94025cb90198d247fbd58ff869c8b34ee7290c853e4` | 0 |
| src/xrpld/app/consensus/RCLConsensus.h | 18171 | `b9f1c75d134985f33bc405d7b15369721c931502407751824b5a0550aa7c69b6` | 0 |
| src/xrpld/app/consensus/RCLCxLedger.h | 2753 | `f5ea43dcb2dafe14eb09ca8643f571b926cd45b143ac768f5a9378ca3b233aa6` | 0 |
| src/xrpld/app/consensus/RCLCxPeerPos.cpp | 1949 | `cf1aaa0b72e9802c4d4fa568bff65b00d103b0d7233fc8ee597b338a142ef913` | 0 |
| src/xrpld/app/consensus/RCLCxPeerPos.h | 3745 | `0ed22ea8eb0204a922605ebc3dac1e00b3d63ab22fd093c9fab93cc4fda47528` | 0 |
| src/xrpld/app/consensus/RCLCxTx.h | 4899 | `2144c4d929d6caffa9fbb948c74766528bdeccb2e39ef74db15efdb576e05498` | 0 |
| src/xrpld/app/consensus/RCLValidations.cpp | 7502 | `90dd18ada46e079d238dec9f7f7a326179a191d63b612d6d4bf30b16cc2ad067` | 0 |
| src/xrpld/app/consensus/RCLValidations.h | 6235 | `f243f6b44456b198cfe5030ac48b3fd665febd958e6dcd38512db1343aad5d94` | 0 |
| src/xrpld/app/ledger/AbstractFetchPackContainer.h | 697 | `c533f24de29ad59fbdd5533f7d7ed9d9cc8a3950a959de45f589b7cbffeac992` | 0 |
| src/xrpld/app/ledger/AcceptedLedger.cpp | 660 | `e6818c49546ec694534492ccaa5ed3a83843475bf8bb3adecfec225e5b6853ab` | 0 |
| src/xrpld/app/ledger/AcceptedLedger.h | 1788 | `9461bdd7c6a687944366ee012bb2af90bdc107fa7ef7980acd996ad142c5dee6` | 0 |
| src/xrpld/app/ledger/AccountStateSF.cpp | 675 | `c959924d0ed062b3ba48adb4939b3e93406af4e9eab019bc295e0b2c290e7aad` | 0 |
| src/xrpld/app/ledger/AccountStateSF.h | 970 | `ecbcb400dbc9f1f297724b71fc14c066ff1714e6deeb773209ecfaadd79eb290` | 0 |
| src/xrpld/app/ledger/BuildLedger.h | 1848 | `2a09dc9a1e346fa2b8ccf964dd27d08a84ad70719fb905d4419290506564a75b` | 0 |
| src/xrpld/app/ledger/ConsensusTransSetSF.cpp | 3043 | `513c2caec44b57a3d2632c2863ee64ffcdd67c0a05ad512a46a0ca36bdfaea86` | 0 |
| src/xrpld/app/ledger/ConsensusTransSetSF.h | 1629 | `d8e4eb65d7c0b499673da5ef9a843ad427d44653bb963b57ec93253c0f965378` | 0 |
| src/xrpld/app/ledger/InboundLedger.h | 6424 | `a014a52fe370310f9c20627586b529c58c1bb2cb5ded72215af0463ded9a31be` | 0 |
| src/xrpld/app/ledger/InboundLedgers.h | 2448 | `76363334f9342aff4987edf71269c4d3e382133082b095c57f85a3ca86594d74` | 0 |
| src/xrpld/app/ledger/InboundTransactions.h | 2403 | `884defc1f01a4dc3689dd33c2f13f9a7f5b3a3a35e513a4a4f1991a067d8e1c8` | 0 |
| src/xrpld/app/ledger/LedgerCleaner.h | 1170 | `877966183c48262a13ddffbc4ed963c5960444ba31b0c3e923b33d255cdd0ad4` | 0 |
| src/xrpld/app/ledger/LedgerHistory.cpp | 20964 | `94cc366a365b1b512938a65b81ab29cc36747dc774082002f63836dcf8db262c` | 0 |
| src/xrpld/app/ledger/LedgerHistory.h | 5427 | `6201d46637964c9fa9b1f4127ec7107e4d84f9a86df2d449a5a98e6d3a51bdf5` | 0 |
| src/xrpld/app/ledger/LedgerHolder.h | 1366 | `fa44cae28dea8f7401a61ecaffdb53544f4bc0747271e2a0d4766035922ebca6` | 0 |
| src/xrpld/app/ledger/LedgerMaster.h | 37917 | `46cadbcb8e9dac7761fd1673204de4438bc3cb55c7080ed3c18889d033e16b6c` | 0 |
| src/xrpld/app/ledger/LedgerNodeHelpers.h | 1975 | `3884903aee06c1e9813caf6bb9aae5927740e54f8da0648f80676ff4877c84cd` | 0 |
| src/xrpld/app/ledger/LedgerPersistence.h | 3000 | `7aec1fcd755d597d471dc1956830bf555908b27cf177e67a3816de4d6db7736e` | 0 |
| src/xrpld/app/ledger/LedgerReplay.h | 1248 | `5231791af44c70558c2dfed50886b920f8d6ff02ec54b0bf83ab6f5c36e7a5bb` | 0 |
| src/xrpld/app/ledger/LedgerReplayTask.h | 4763 | `e72cbd9141b04e6f25ee34a50bb45c52d1ac88941eaa2e58229778288090dc4d` | 0 |
| src/xrpld/app/ledger/LedgerReplayer.h | 4294 | `80eea64e38a1fa962115148adea8a652a9833aa896f2922f9a4aa950c7c31db9` | 0 |
| src/xrpld/app/ledger/LedgerToJson.h | 1423 | `1bbd1ab7661ceb87291b0804a48b7a76fc79ebdfdfbc4bae5877516c9911754f` | 0 |
| src/xrpld/app/ledger/LocalTxs.h | 1128 | `26551d715b0976429397a507a0f18187a714eec082b19a0ad81e02cdc5da2ba5` | 0 |
| src/xrpld/app/ledger/OpenLedger.h | 7821 | `52ae69fd818e15ac904c9c522d7f7282b37c64a783a6b6377c4062d0fcf659a2` | 0 |
| src/xrpld/app/ledger/OrderBookDBImpl.cpp | 10412 | `8ae8213b3b45f799f09bcb53f7574bdb50fe5778c8ef522d042cdaf7a9ba6495` | 0 |
| src/xrpld/app/ledger/OrderBookDBImpl.h | 2289 | `7d88e3ca873f7bfa70d7e0c420a61361fa23f488e33ee726d150fc5552fb76c4` | 0 |
| src/xrpld/app/ledger/TransactionMaster.h | 2159 | `ee0c82b4d4f1d79eacebeee42203f61b196cfc1321007ea4d6593b6cd6807c7a` | 0 |
| src/xrpld/app/ledger/TransactionStateSF.cpp | 872 | `1e8fbeeac70a930a674b9b06fd500daa738f8f02aacf00d3382503c7232b9b70` | 0 |
| src/xrpld/app/ledger/TransactionStateSF.h | 976 | `13aff3a47c6e877271a9bb9dcedcc14126ad1ab13413a26aa810f5c078908b8a` | 0 |
| src/xrpld/app/ledger/detail/BuildLedger.cpp | 8825 | `2a4ad5301406c5eddb2e8cd9e61e1c9ec2c0a471ca5db7460908ef6ee99efc2b` | 0 |
| src/xrpld/app/ledger/detail/InboundLedger.cpp | 43134 | `d1e6d1cfbf5baf57e52f961d3d4e051aeba87f4a5f2deb5f66af0d236770daa0` | 0 |
| src/xrpld/app/ledger/detail/InboundLedgers.cpp | 13110 | `8b1cfe3ea6aa2807c7ef06838bf97f76a5a12cf1729d2832c60c26657c00aa33` | 0 |
| src/xrpld/app/ledger/detail/InboundTransactions.cpp | 7639 | `bb6c054ec9bf400125d0f403ef6f37aced346bead9de626c2a4ed93cd7f9fbea` | 0 |
| src/xrpld/app/ledger/detail/LedgerCleaner.cpp | 14883 | `09733ca14126d86660da76115442b1c90622c5995f3619fb718b46b2c094b03d` | 0 |
| src/xrpld/app/ledger/detail/LedgerDeltaAcquire.cpp | 7876 | `a7712fc4d2c7152c887877aab008743ce7e22a01644fc2b267300f44dc241f59` | 0 |
| src/xrpld/app/ledger/detail/LedgerDeltaAcquire.h | 4802 | `84142aa78c96edc05eae7de7c93b9d6f8c25eea31da0adcbcf600b2574a823be` | 0 |
| src/xrpld/app/ledger/detail/LedgerMaster.cpp | 71582 | `633cf8414779e08897d360fce9668e173fb543862d2859c91ae9d62a65e59ba1` | 0 |
| src/xrpld/app/ledger/detail/LedgerNodeHelpers.cpp | 2464 | `501813c54f6e2d51f038ec9f144873881553219e797223b32d96e24e4981683e` | 0 |
| src/xrpld/app/ledger/detail/LedgerPersistence.cpp | 7521 | `b0760ae804ee7df1e839013a9907631a811be159cc812ecd30127ad15efa1784` | 0 |
| src/xrpld/app/ledger/detail/LedgerReplay.cpp | 958 | `a0af56ad57efdab83023913872a31205d8be3b198e551bc5d0519d1889e30159` | 0 |
| src/xrpld/app/ledger/detail/LedgerReplayMsgHandler.cpp | 11139 | `3507067ba9671dd69b92021cc82ae90f79e230ca5e9e4c564013c2f27cb4c323` | 0 |
| src/xrpld/app/ledger/detail/LedgerReplayMsgHandler.h | 1869 | `b28fbeb2935a6f585a6c59a00193c29b38dd60ba8b05036899fc61385f8cbada` | 0 |
| src/xrpld/app/ledger/detail/LedgerReplayTask.cpp | 8385 | `5818214b7f8acf236f4405b90f838d5dae33ede911df6160a2cc8dcce322139d` | 0 |
| src/xrpld/app/ledger/detail/LedgerReplayer.cpp | 8599 | `81dbee75670979a7887f457dc97dbdb08e5096f5c4661107aa24fea860867255` | 0 |
| src/xrpld/app/ledger/detail/LedgerToJson.cpp | 11547 | `29e8b5f53b01febffb2650e90c6b39d4c3359344a2af4fcbaba56b3212c6f090` | 0 |
| src/xrpld/app/ledger/detail/LocalTxs.cpp | 5163 | `06e048cc8dad8be6182aea3f2c3034382579d0122b24a54d6dda7131a0713249` | 0 |
| src/xrpld/app/ledger/detail/OpenLedger.cpp | 6406 | `308ec87ecd5595356acb744010d2d7a11339d40837168957e1bba00deff4ca27` | 0 |
| src/xrpld/app/ledger/detail/SkipListAcquire.cpp | 6500 | `b51f2106af8aa3c6edb6647960df3335ba91e1168f2be3ef0f7a38d8de369918` | 0 |
| src/xrpld/app/ledger/detail/SkipListAcquire.h | 4313 | `c7a0e6a2b55474b892e9d5f79e52fa9e488059b946bc8c3271763cec5e7fef70` | 0 |
| src/xrpld/app/ledger/detail/TimeoutCounter.cpp | 2685 | `a7af80e3eaf186d29786e912faa8857a3013d8d5ad0f3178712b75164fa3386e` | 0 |
| src/xrpld/app/ledger/detail/TimeoutCounter.h | 4538 | `294479c59dd1de4f9ba5cdc62adbbf43912eb35c561a2a14a9935f2cb34fe265` | 0 |
| src/xrpld/app/ledger/detail/TransactionAcquire.cpp | 7664 | `f84afb469aced70c5d60ff2cc444609542fb5e352be6390834253d4490faaf06` | 0 |
| src/xrpld/app/ledger/detail/TransactionAcquire.h | 2497 | `db6fab2d37d3bd50af764c6f834203217515ce7445b3f83fa2d18705a7549607` | 0 |
| src/xrpld/app/ledger/detail/TransactionMaster.cpp | 4205 | `8efc0dd3164f031ba1670b5c2288b80269d4963b4b4f1a9e72b21603d6394b8a` | 0 |
| src/xrpld/app/main/Application.cpp | 70696 | `97a6eb13b268d5014c11015a3e0058e26ea233472975a078a5f94aeafec41b6d` | 0 |
| src/xrpld/app/main/Application.h | 3813 | `c0a62a18e51577232cac4a9c7045c06d8c873cab237bfb1c507da4a0f33a1cd1` | 0 |
| src/xrpld/app/main/BasicApp.cpp | 647 | `40bcc3568182c8df7680937d8322a190304bea3709721dbc47167178fe9ffa13` | 0 |
| src/xrpld/app/main/BasicApp.h | 656 | `9da261008442725b2bd57b211c334095fe22a26d39c9badfb553cf2a66d67322` | 0 |
| src/xrpld/app/main/CollectorManager.cpp | 1982 | `992b1417de7af728847536162727c14c4215d6ba6445e8e89eb70e063fbfb816` | 0 |
| src/xrpld/app/main/CollectorManager.h | 650 | `6b5e2f945f9af36e18d694e56e4f277e53f171457fa301ed68893cc3a239beef` | 0 |
| src/xrpld/app/main/GRPCServer.cpp | 27726 | `ad48f324141782a00fa0f6d06c1ac90a4d58c4ed43e6477ebdefe041779f4ac7` | 0 |
| src/xrpld/app/main/GRPCServer.h | 10005 | `73538d9a067e9cb436b9a3c95a0602503d7398ba8745201f643f486485f9a5c0` | 0 |
| src/xrpld/app/main/LoadManager.cpp | 5333 | `6db1e0e2ea0babab6b833342ab6679c1b18f8403e92f5c721f2cc0e13cf9c2b0` | 0 |
| src/xrpld/app/main/LoadManager.h | 2437 | `cd536ed1c3dff87551bd2c012ca7068105db1e15c8027e76e794b61107dbc1f8` | 0 |
| src/xrpld/app/main/Main.cpp | 28551 | `b014b05b17a53d7a84bb305f5e5ca4a83019aad74e832aafa62d61ef96b33efc` | 0 |
| src/xrpld/app/main/NodeIdentity.cpp | 1588 | `0121cca9e785f9ae238c75a98fde942c2d0b5400226bf1c7c93b33534fd1d42c` | 0 |
| src/xrpld/app/main/NodeIdentity.h | 539 | `f3dae695f7467454a87151170e6eeca5b9afeffc86d71a1e1d14778e6da7d6ee` | 0 |
| src/xrpld/app/main/NodeStoreScheduler.cpp | 1170 | `ec9ac7f360059c2738f3816a0047bc5306709cd11a324314a6574d829276031b` | 0 |
| src/xrpld/app/main/NodeStoreScheduler.h | 586 | `47c0d3342fb426ff57f692c20468b929759652ae9ba50d58db021b7a17c71488` | 0 |
| src/xrpld/app/main/Tuning.h | 277 | `3d82b640010275f722630af07ede0db5d8df84669b256cf5a7d22d11a1bdb7c3` | 0 |
| src/xrpld/app/misc/DeliverMax.h | 548 | `654502219006d01d8144594399e36bec1c3c21d1f6149c053b39177f627a52aa` | 0 |
| src/xrpld/app/misc/FeeVote.h | 1227 | `eb1d3c8c0611321086719a101ce9a6de81b010f1d6146aa30396ac2ecea1e969` | 0 |
| src/xrpld/app/misc/FeeVoteImpl.cpp | 10615 | `d9e153d4f3ed906a78fd284b9efd9acd285ffc4403cd408f4dd6185c3184d283` | 0 |
| src/xrpld/app/misc/NegativeUNLVote.cpp | 11975 | `80fff2fcccc288d6e567f10671e95f28884486e6fb55d3256a5973e1f90698fe` | 0 |
| src/xrpld/app/misc/NegativeUNLVote.h | 6426 | `b6f5d42babe24e93654b9dc7c1cdfee861d946f6e8b524451d66e2aca13ec2db` | 0 |
| src/xrpld/app/misc/NetworkOPs.cpp | 187760 | `9e0ce6415c5c1399ee163f49b3c1f6eb222911485180e921a385d13fe265d412` | 0 |
| src/xrpld/app/misc/SHAMapStore.h | 2885 | `08ddd464144bd2afd68b5670fd027042fcb3cc4d6a25eccabeb2c302ba42102f` | 0 |
| src/xrpld/app/misc/SHAMapStoreImp.cpp | 31835 | `e510d40054234c896ab0f9beab47a40e54e6ffb138bf0fdbc96b9e6375a0417c` | 0 |
| src/xrpld/app/misc/SHAMapStoreImp.h | 7770 | `3a357076326cb39c38b2283136b06593011b52262d2976f7800943858bd10cb6` | 0 |
| src/xrpld/app/misc/Transaction.h | 11514 | `91221b344c0f5fe9d404c159142ba008de0a1cf8b856ad4035957f62f38e57fc` | 0 |
| src/xrpld/app/misc/TxQ.h | 34502 | `2ffbd0676348a824f298df608abbc354fb5514c60c8bf7c457b29d8e24ac330d` | 0 |
| src/xrpld/app/misc/ValidatorKeys.h | 1511 | `40a5c53dc0c9760536e80bb3a74144a5d580b375715164db2a90ac64aad76bc0` | 0 |
| src/xrpld/app/misc/ValidatorList.h | 29381 | `cb20d28a01c11e3583aab9fcf22568862b36800a3d3b1a371205d0d1cfc8aec9` | 0 |
| src/xrpld/app/misc/ValidatorSite.h | 7135 | `86003d2dca1dcc19ad71daac5b3f3c48d567d4be0cec2fd7d7018bdb5b0f3d30` | 0 |
| src/xrpld/app/misc/detail/AccountTxPaging.cpp | 1759 | `cfb3b91ca14890ec92da10878267408867a9f43426c327ddd13f6c3b75fd1148` | 0 |
| src/xrpld/app/misc/detail/AccountTxPaging.h | 540 | `4e41ed835aaf15376679ab93cdab73db1823a0580cc34b2f8c733c4d2e3c18fc` | 0 |
| src/xrpld/app/misc/detail/AmendmentTable.cpp | 33679 | `faefc4cd3f7183a358bef15579bbeb6ccc41c1f6e3ceb3883459b2affb0a6784` | 0 |
| src/xrpld/app/misc/detail/DeliverMax.cpp | 492 | `55092b36d1abfe09ab42b5fd8e1aed4f4ea1f560693621808075e40d3ea4baec` | 0 |
| src/xrpld/app/misc/detail/Transaction.cpp | 5388 | `7ff3593c349ceb3963763f8687925314eafa3f034db43bdc1e31341535b5620b` | 0 |
| src/xrpld/app/misc/detail/TxQ.cpp | 85108 | `9fb90e0ec69344576693053f6ce9076a5f6447d0859f074d83deb89b5275977a` | 0 |
| src/xrpld/app/misc/detail/ValidatorKeys.cpp | 2546 | `0411ffba7d73cf4cf6d19617f2e2bca0367ae6ac7a0f9f3cec846c7d50bd7c9f` | 0 |
| src/xrpld/app/misc/detail/ValidatorList.cpp | 68562 | `54be3cc2203d65aa5981192bff2844b5e2f637d06ba2861df91befc6c7383cfe` | 0 |
| src/xrpld/app/misc/detail/ValidatorSite.cpp | 23386 | `1f7c88c2bf4b39f9c28bcc0742b6777963c8bf51ba3500ce8c9a2bb0c8a7d304` | 0 |
| src/xrpld/app/misc/detail/Work.h | 364 | `7bcfddb4f0e628e8749c3f1e2ccda42b320a3d2ef9f06c53dd6a4c61198cce3f` | 0 |
| src/xrpld/app/misc/detail/WorkBase.h | 6314 | `ee765830c5b8a3ee207180cf5e920e3c2332d8c519555b013067990c29e2aae9` | 0 |
| src/xrpld/app/misc/detail/WorkFile.h | 2083 | `8fe829d5cdaf951ffbf54c513e85a48b411120cbb414be2542e45c4d9351eb07` | 0 |
| src/xrpld/app/misc/detail/WorkPlain.h | 1238 | `8e88ec178cb0eb1581c7f7e98ad0ecff6ef935681c1319387aa87118c9ba6746` | 0 |
| src/xrpld/app/misc/detail/WorkSSL.cpp | 1706 | `6e582e704fa1ff58b353bb0931c642a5b2ee35e4d9941c91dae3efe91056f509` | 0 |
| src/xrpld/app/misc/detail/WorkSSL.h | 1087 | `3962910831497edde0fc729c86d8bde055dd72f42d6b7d1d5d382c2c62bc6bdd` | 0 |
| src/xrpld/app/misc/detail/setup_HashRouter.cpp | 1338 | `16b386fe704988608923ed3d17f9655c7e0be5f8633d6ceb342673d29e691c70` | 0 |
| src/xrpld/app/misc/make_NetworkOPs.h | 746 | `f12a15279b40775afd49bc5bb438696cbea368bdebdc90a2797c99b54717b30e` | 0 |
| src/xrpld/app/misc/setup_HashRouter.h | 238 | `f427fab9794638bb8c60e863a64fdda9c8e7bf5f876b405c9e8ca1e74fd5c9fc` | 0 |
| src/xrpld/app/rdb/PeerFinder.h | 1531 | `cbf8bc409f97e48e6b528afc3f94640b0f466f3206b69b3997748274ad6849ee` | 0 |
| src/xrpld/app/rdb/backend/SQLiteDatabase.h | 18414 | `90725bd3f4c1bc472b06f398f9c58b0dafd76cb538cae554f467a4bacb31fd85` | 0 |
| src/xrpld/app/rdb/backend/detail/Node.cpp | 50499 | `28f5234c3fa3b983cbab6fc7868f0aadd871ca689733e43c3f3c5dd756d183df` | 0 |
| src/xrpld/app/rdb/backend/detail/Node.h | 17132 | `92596ed2ead532a666d9f7cb4f4afe452d1a2cc85fdd5a9c93e6a030a5485c32` | 0 |
| src/xrpld/app/rdb/backend/detail/SQLiteDatabase.cpp | 15877 | `21ae081571bb8d9821843f6b801c01c13877c3dc92cb57ce9df63ab3d1666186` | 0 |
| src/xrpld/app/rdb/detail/PeerFinder.cpp | 7550 | `d73bb6a29716dc562c755e069a44cf989385aa5f509823bf40b5a0b7d577c564` | 0 |
| src/xrpld/core/Config.h | 14501 | `8d42dad85f3dbccc62b696bc4e3749106fd911e5b273d00de12a5e0541c28e94` | 0 |
| src/xrpld/core/NetworkIDServiceImpl.h | 684 | `dc2cf854a675c90138bce5ba9102fbf8d18ee66d3f98985c975a100395a51c54` | 0 |
| src/xrpld/core/TimeKeeper.h | 3154 | `cbfa4e5626eed58a349aa740feb1c0339094fadd2ee95bc5b5deacee6cd75e3d` | 0 |
| src/xrpld/core/detail/Config.cpp | 49488 | `85e2e2669a130de0964fe86d49a6fb9512dd6b8341963bba67ee038c90eb2219` | 0 |
| src/xrpld/core/detail/NetworkIDServiceImpl.cpp | 296 | `a58d9e40798bcf4a467379dd089b8231b917ea177c9f7fd7abd4280411413d6b` | 0 |
| src/xrpld/overlay/Cluster.h | 3114 | `aa483979c06ec84da1fa70f82dec56133717454e683715f1d9d3a520aead212b` | 0 |
| src/xrpld/overlay/ClusterNode.h | 1029 | `27878a93482b8aa300358cfe5ac7652f1174669da2f1e3269bded965013e9291` | 0 |
| src/xrpld/overlay/Compression.h | 2814 | `81cc7afc916f4bd623a92480c9ff7dfeaf3bedf06ea03a634c8d10b3c334f660` | 0 |
| src/xrpld/overlay/Message.h | 5448 | `9c8567edd88ba88afa10da7478411a25a2eb58ea95cb484cb9dfd66dc6b0448b` | 0 |
| src/xrpld/overlay/Overlay.h | 7282 | `521d90669673b41a26d43238f8403979d8e1faaf823eccca4c37f1e6c6dd48f5` | 0 |
| src/xrpld/overlay/Peer.h | 2989 | `522fbfbaed6d931b260cbde2b8e75607f574fdfc1ca557dcd20ba601677a2390` | 0 |
| src/xrpld/overlay/PeerSet.h | 2209 | `7d061f0c37cde0ba1b59c1eb99fc58e49b04d0523b9776fb7b412d4c7acf7622` | 0 |
| src/xrpld/overlay/ReduceRelayCommon.h | 1845 | `9fa0d8314c8ce0b182829b71c3e690d78b90a3819964798edefb3991dba95235` | 0 |
| src/xrpld/overlay/Slot.h | 26101 | `329b566a79c4df01092d34bbd9d6a741623cce1c66ac3cca4256ac30f4d0041d` | 0 |
| src/xrpld/overlay/Squelch.h | 2554 | `1450e8e857b88ec195eb0c0547677268315866f1e3195966e4524656f0e22e55` | 0 |
| src/xrpld/overlay/detail/Cluster.cpp | 3096 | `316c7a084e57b9b175f37d44287b18b620fb76dff40df0d2ec8996865ffb5ec0` | 0 |
| src/xrpld/overlay/detail/ConnectAttempt.cpp | 12013 | `96e517641c6c447ba71aea3fcc3a2533952d118764628102edb5c28dac93de6d` | 0 |
| src/xrpld/overlay/detail/ConnectAttempt.h | 3145 | `1f7a0832fefeeafea5101c47a8de9653dc9f4cfeb8f678d7e8fae529fb8b2905` | 0 |
| src/xrpld/overlay/detail/Handshake.cpp | 13589 | `225fcd028d327f56d85ba7869a3787d0211abd77be37c209563acd42fcb818a1` | 0 |
| src/xrpld/overlay/detail/Handshake.h | 7771 | `33c8efada38683bd559ad6e3a22782dba0d0c406878ae6ce02c13172d9e3448a` | 0 |
| src/xrpld/overlay/detail/Message.cpp | 6701 | `dfee3eaa19f3d118ae8ce692d4ec32509aeed1a94176374ca2f2c7cab0fb3804` | 0 |
| src/xrpld/overlay/detail/OverlayImpl.cpp | 53521 | `d9c7e186bed67a76168b7c613facbb1e64cf4cfd342410ad4fd05e973570ecd5` | 0 |
| src/xrpld/overlay/detail/OverlayImpl.h | 18095 | `fb010eca65b6fc5e12a569c4ab23444eb52874f686856f1c37b2a023ecf7eb0c` | 0 |
| src/xrpld/overlay/detail/PeerImp.cpp | 125236 | `002a80869bb72709296a163ba1e0748e7e3a230828d9980a5e90d29e4deeeaa6` | 0 |
| src/xrpld/overlay/detail/PeerImp.h | 25073 | `990b77a928fca8df26d427a54ffe5c2245b4f052b4f0d8c9d82637f67067e577` | 0 |
| src/xrpld/overlay/detail/PeerReservationTable.cpp | 3396 | `0ddfb310bf2beb93f1fef171beacb0c132914f2664940da54a8a41c3973b20d7` | 0 |
| src/xrpld/overlay/detail/PeerSet.cpp | 4322 | `b932d1da1fd68c62af6280098fd9793d1a062c520c372ec8a4a81b50bb530bf6` | 0 |
| src/xrpld/overlay/detail/ProtocolMessage.h | 14966 | `078a9325ee399c07a957b3903a078c976e154c87a5c4f1d90f58b1e92b6cfe6b` | 0 |
| src/xrpld/overlay/detail/ProtocolVersion.cpp | 4880 | `27a520996fb57bcec371847abccd7ca86f1585df16f2fe6c2e98fdffcf5799fe` | 0 |
| src/xrpld/overlay/detail/ProtocolVersion.h | 2037 | `7a33eeea556fa2dfdc7a6f43246c941530e1bdd636adab3bf30653ae0c0d7e50` | 0 |
| src/xrpld/overlay/detail/TrafficCount.cpp | 6098 | `e70e57e492c71846a517d619eeb2fab6359cf3797d220a7e8626bbb085cf9caf` | 0 |
| src/xrpld/overlay/detail/TrafficCount.h | 14624 | `6ae1592866f9c4fc14789ee96d092bab8a4b61be0cb8eb20d4d727d09ba458f1` | 0 |
| src/xrpld/overlay/detail/Tuning.h | 5654 | `2f6a214654ab6d703c7afb4696fdb52b3ed8145e778d91f3464e4517e1c9d7d8` | 0 |
| src/xrpld/overlay/detail/TxMetrics.cpp | 3580 | `a871457383de79310ceaabaceac42aa5ec89a4b25f22e1e62f077162f103faaa` | 0 |
| src/xrpld/overlay/detail/TxMetrics.h | 3623 | `fc931640d900de878626d4ecabc215dec678d93821a715b06b443d26d9668efa` | 0 |
| src/xrpld/overlay/detail/ZeroCopyStream.h | 4728 | `4bb18db9a0aedc0f08bc1f1b637bec63b9749fda6b98482a4ddf9ace92814184` | 0 |
| src/xrpld/overlay/make_Overlay.h | 862 | `d46213b715d0608bbf408e2e895666ded74ba3f5a7b8bbc8b520934f9c3e7b5b` | 0 |
| src/xrpld/overlay/predicates.h | 3246 | `ca9e2063e830efba0ba7554cb9419dc21c675e00e633b2d13ee5a6a8bd54b742` | 0 |
| src/xrpld/peerfinder/PeerfinderManager.h | 318 | `7ca8143d0aead775d59ae7852c165fbf4ea15ffb956655b4972a324dcf01ff46` | 0 |
| src/xrpld/peerfinder/detail/PeerfinderConfig.cpp | 781 | `6b940fa66c1f4eba93cb3e8f7505159507487c5d5fb8199336baaa0ea80c8beb` | 0 |
| src/xrpld/peerfinder/detail/StoreSqdb.h | 2051 | `9fbb48761fbd0efcc665621ce87843ae7b03833bc3badfe9b749d1c7ae7953bc` | 0 |
| src/xrpld/perflog/detail/PerfLogImp.cpp | 16009 | `55c3594503e43694ea19b6621297caa2a10085d2d5013bdbb5fc9196a31f6a6a` | 0 |
| src/xrpld/perflog/detail/PerfLogImp.h | 5800 | `f4bf05639d5d248da735a62d6ba26c3f1d982dbfa1531c36b7fdc65046eb706d` | 0 |
| src/xrpld/rpc/BookChanges.h | 10049 | `51cd2849448adb2ba18a182e890ee171f5bf5ea64d4ec9fb8d025a10a3f193f3` | 0 |
| src/xrpld/rpc/CTID.h | 3557 | `70e37b25fc4a6eb3b8edfb2e6ef18e47086a895e8ac91fcf0f305daabcc1a619` | 0 |
| src/xrpld/rpc/Context.h | 1144 | `a614babb1dd141ed7feb17a7da75f9dd9c325573bfd1b6b5213d8539b145a644` | 0 |
| src/xrpld/rpc/DeliveredAmount.h | 1387 | `1c0b8a326b695fedd463f9045dd1788977282bf6d2228df93f8e0f67f30693fe` | 0 |
| src/xrpld/rpc/GRPCHandlers.h | 1320 | `16ce4a28a6ab07a05b233be9b19ff033b20cdb7886c1a639fb87c890a6bda81f` | 0 |
| src/xrpld/rpc/MPTokenIssuanceID.h | 865 | `aa7d06f70d9ff5b850c5a20cefc5e3d194098c13a808d9ea65044426b3a45823` | 0 |
| src/xrpld/rpc/MethodNames.h | 5389 | `2e2964a6cd0c5b627d6151022548bff8a0af8072e3b80a78279ed0e68a924821` | 0 |
| src/xrpld/rpc/RPCCall.h | 2088 | `4f673125d745ea5e600ad63d5ff8ce0cb6802918bcf9da3042183a5e6ac50f85` | 0 |
| src/xrpld/rpc/RPCHandler.h | 452 | `cd3bfea6b80b466bbdff9a3331705fdde6d563141ade698c01501272ebcad090` | 0 |
| src/xrpld/rpc/RPCSub.h | 824 | `83cac9c4d853252c977ca8e237869034338459ff06576af625b76e50391bf5e5` | 0 |
| src/xrpld/rpc/Role.h | 2144 | `0c735bf2392e9cc90462efa287ab77034d340303c951db0b259e425a263d3d56` | 0 |
| src/xrpld/rpc/ServerHandler.h | 5450 | `e8bb03e8841b5665841b33c6b2c4a7be994b6109c32ed451531c5d60edf7004c` | 0 |
| src/xrpld/rpc/detail/AccountAssets.cpp | 2587 | `c974892da281a5a2318ebb8589cb35ad4aca18d683d2408030db41e669e1b98f` | 0 |
| src/xrpld/rpc/detail/AccountAssets.h | 513 | `4628bfab86aa11fb12888fcad8ed4d0859c037af9848027adb6da4c091d8c429` | 0 |
| src/xrpld/rpc/detail/AssetCache.cpp | 6317 | `8314fc72daf1b9f8b304ae8d9c5dc8fcd3570a0e828df335cca1bca911080fd4` | 0 |
| src/xrpld/rpc/detail/AssetCache.h | 3339 | `45639dd50e7086e549b24f6fa21fe7a1137f57381b78529d3e4917df9ab89442` | 0 |
| src/xrpld/rpc/detail/DeliveredAmount.cpp | 5713 | `b5acaabeb28d718d65661aee9eb31f37823042153c0daa13cf36205b33949007` | 0 |
| src/xrpld/rpc/detail/Handler.cpp | 20903 | `41dbbfd67d0b0c71a32b17425ac4c05ca85e7a8eb4bce2d0889c6f583505afe3` | 0 |
| src/xrpld/rpc/detail/Handler.h | 5950 | `1cd0b296c1efcad86dd237dbdd946c72d01d1dc53d5af781e0677ea3ce8b3923` | 0 |
| src/xrpld/rpc/detail/JsonFieldView.hpp | 7984 | `2a18c1aa3543149251705f16c947abfef5127908867a603a38daab2cb6e1880e` | 0 |
| src/xrpld/rpc/detail/JsonObjectView.hpp | 1965 | `ce1de778ccd4744c08271d245ead4eb239250f38cbea98fad5c219a4c4a691e2` | 0 |
| src/xrpld/rpc/detail/LegacyPathFind.cpp | 1100 | `c8c9ba21e733226f99d3dabd316f4aa2e548804874fe1885ccaa4cb453bc5121` | 0 |
| src/xrpld/rpc/detail/LegacyPathFind.h | 388 | `42d605396db0c4ba9957d211533b1555c344b97053345693fe25ef8cb39cd469` | 0 |
| src/xrpld/rpc/detail/MPT.h | 1111 | `3ed6d47b05b2a6f25c0ae3f13e0e88eb989112cb031c3e4afd1ef11279a9c04f` | 0 |
| src/xrpld/rpc/detail/MPTokenIssuanceID.cpp | 1882 | `92eea032834c27ef807943b35ca74598ee4ceada09ee2dc054013509e75149ff` | 0 |
| src/xrpld/rpc/detail/PathRequest.cpp | 26415 | `579a606be668c9aa4acc1b17b4666cf5572bb457c9517378e0eb2686d253b65e` | 0 |
| src/xrpld/rpc/detail/PathRequest.h | 4396 | `b8296890fe73073343dde199b9c587feca8724fe0abd5cb42241b392c0de5e1e` | 0 |
| src/xrpld/rpc/detail/PathRequestManager.cpp | 10082 | `ded0834f0db2d5ce1ee56a3595c7411cf5ed1f38cf40f312ad3774f882acf62f` | 0 |
| src/xrpld/rpc/detail/PathRequestManager.h | 2801 | `79a106480c5166014e8fd32875ea14d38424b43e1564aac6d2caefc839555802` | 0 |
| src/xrpld/rpc/detail/Pathfinder.cpp | 51325 | `0fffd15d3ef9d1fd13fa58db7df6fd7c698483a260856906cc252a8c6d078720` | 0 |
| src/xrpld/rpc/detail/Pathfinder.h | 6934 | `d26373584443c79249a23987b869eb89dca329a07c9f817c77c4f161a824caaa` | 0 |
| src/xrpld/rpc/detail/PathfinderUtils.h | 841 | `066a8981a7a23a74eba6397e4686cf60262343c6458d90bdafcb2e2a360cf3f9` | 0 |
| src/xrpld/rpc/detail/RPCCall.cpp | 68441 | `21e320d5933f32ff5e49499701b8b5c02516167ff899d32a09443d450b85ccff` | 0 |
| src/xrpld/rpc/detail/RPCHandler.cpp | 6983 | `9219f58cc04dcbd2911c24275e6013763104b773ee3db89cff4c062b3afd706b` | 0 |
| src/xrpld/rpc/detail/RPCHelpers.cpp | 15659 | `0262ded1c8095e729671b3173a5bee7e3b3be5f12fef6465fcdb58e6954d02f6` | 0 |
| src/xrpld/rpc/detail/RPCHelpers.h | 7672 | `422a8cb64927765e9f2f72d25127ea9960e683747ab4d56598b0f36f5e0e3647` | 0 |
| src/xrpld/rpc/detail/RPCLedgerHelpers.cpp | 18314 | `cb6b32c083866f862e0626e60780e6ff8dedf27e325a58d9cf79b50c2bd8242a` | 0 |
| src/xrpld/rpc/detail/RPCLedgerHelpers.h | 7760 | `64ddb8627136dca756a12f540af951bebf571349a9b90fbba8137a18fe63bf50` | 0 |
| src/xrpld/rpc/detail/RPCSub.cpp | 5660 | `f1c3e718f812c9d3634c8612f676faed460b7ea70da446273c2e406534663623` | 0 |
| src/xrpld/rpc/detail/Role.cpp | 9959 | `59edfcca3500a23aeeb811655926780afa6d1b8a4f421e7424ab5dc327f0da1f` | 0 |
| src/xrpld/rpc/detail/ServerHandler.cpp | 40449 | `bf7684fffbcaaeb0c23b2c6c0edb47821fdc8277018682940d24c8370516b1ab` | 0 |
| src/xrpld/rpc/detail/SpecBridge.hpp | 2146 | `43e6d5fe22e3a92edd75c8ce7030d97de1be0b378a4ffcd2bb48298833ba028f` | 0 |
| src/xrpld/rpc/detail/SyntheticFields.cpp | 1213 | `d4d93e60513d14c348beecb51da01b54b276eb4a71dde33a1885a0614979f3f4` | 0 |
| src/xrpld/rpc/detail/SyntheticFields.h | 706 | `b3852f91d620e86e4e31fb626cfc10eb1a8bfdac4b59bf67939029b5c764798e` | 0 |
| src/xrpld/rpc/detail/TransactionSign.cpp | 47157 | `1090f8d37ec44587c0e8f727f3fa9b54c65324a10427188b95fd55383b7a4a50` | 0 |
| src/xrpld/rpc/detail/TransactionSign.h | 4232 | `83d43efe47127559c7bec8533065e010262fa43a8b2fbc8ca1945684b1bf364e` | 0 |
| src/xrpld/rpc/detail/TrustLine.cpp | 2912 | `bf3d6b4c5129a562555059113ca5bf48a77da020bcf7af9de09039d288f7ad53` | 0 |
| src/xrpld/rpc/detail/TrustLine.h | 5999 | `67b88f4a999a8c3d5db2aa9b6a51b2abe968e153d4b31fc5f867a2047b3cda5a` | 0 |
| src/xrpld/rpc/detail/Tuning.h | 2603 | `a2ae8c60afce6ba6cc95190e4f358d655bfef36a5342bf95fcb4300ea78d069f` | 0 |
| src/xrpld/rpc/detail/WSInfoSub.h | 1650 | `688b19f5d1e7e8718b2f8e30e374fe95aa6930c6e291d9750d7bcf1228519b74` | 0 |
| src/xrpld/rpc/handlers/ChannelVerify.cpp | 2563 | `01973d8854ebecad926b092f80bb226b16810886aef05356aa10b65d4c21286c` | 0 |
| src/xrpld/rpc/handlers/Handlers.h | 2971 | `2f0a3b5dc962dc036b9dd5b91072c28d35b77da3e81ca917b7e737c4060e6dc2` | 0 |
| src/xrpld/rpc/handlers/VaultInfo.cpp | 3794 | `d693331da64434afa6693060ecbe4952f848557acdb638df5be629a81d6d52f5` | 0 |
| src/xrpld/rpc/handlers/account/AccountChannels.cpp | 6355 | `426cced3cc4558db766874fbc42d225c7c7c2415cd2189282422967fcfd85134` | 0 |
| src/xrpld/rpc/handlers/account/AccountChannels.h | 2277 | `fb3369a91df5d4dadada9e6a67b4211d8928f959912914f115291d2c3f7976ae` | 0 |
| src/xrpld/rpc/handlers/account/AccountCurrencies.cpp | 2268 | `86fb9692d8230173878588693fbfd105658ee9ec1148504489fad56a2d16d597` | 0 |
| src/xrpld/rpc/handlers/account/AccountCurrencies.h | 2031 | `0e7eebbf8adadaf88dfb091f2b20829915b9e467830936a4825995d85706957a` | 0 |
| src/xrpld/rpc/handlers/account/AccountInfo.cpp | 11908 | `4ec1e8f97217b58f234978a6d221d308bfdad4e4719d753e0354700817b84cf5` | 0 |
| src/xrpld/rpc/handlers/account/AccountInfo.h | 2291 | `72e6ce70f0f856e77d6a705553c0b91f8e0473c87adb03299a001c9639c72c69` | 0 |
| src/xrpld/rpc/handlers/account/AccountLines.cpp | 7712 | `05f0afb741316253d0ad11d66b31b45aede58a4e5fd1ea8fc7bf82d9871b062d` | 0 |
| src/xrpld/rpc/handlers/account/AccountLines.h | 2384 | `c0d87655cb3ffd598ba5160ab7c48f8ce1ab05c03c5bf4eec689cdb96fe1eb3d` | 0 |
| src/xrpld/rpc/handlers/account/AccountNFTs.cpp | 5590 | `8687572ecc0708c6d690421df18e1ff5e085a981e08911d1ec5a96e1d3f120e1` | 0 |
| src/xrpld/rpc/handlers/account/AccountNFTs.h | 2144 | `66b20c27f9c8f56123f08161473a1c0f2e5690703b706a50f9573037daebd939` | 0 |
| src/xrpld/rpc/handlers/account/AccountObjects.cpp | 13232 | `d04d6f256cd76b12fc79b83ebbdeb0be3e172b151c375e3738696b9c3c0e907d` | 0 |
| src/xrpld/rpc/handlers/account/AccountOffers.cpp | 5861 | `4ac5099135b1683d1e6f0e143fa1ff860f33ddd83838929c5e72a4b76de53294` | 0 |
| src/xrpld/rpc/handlers/account/AccountOffers.h | 2382 | `ce200f39c06ed7d6ecc744236cc9fdb788d9809194e8e29f98f20a3bc3dc85fe` | 0 |
| src/xrpld/rpc/handlers/account/AccountTx.cpp | 20202 | `1548461fe21ef294b69ffa4e226bb4b7d01fcd1263c56a82fea87b18c4b72c70` | 0 |
| src/xrpld/rpc/handlers/account/GatewayBalances.cpp | 9793 | `ad26646bdb50dd08cd025a96f8068a3a8ec8ec8b7ad2706858a488ed72c30f50` | 0 |
| src/xrpld/rpc/handlers/account/NoRippleCheck.cpp | 6773 | `27b596d3fad447bf627ccdafbbd0e0c9acd09e1dfdc67552253dbb7602aeb28c` | 0 |
| src/xrpld/rpc/handlers/account/OwnerInfo.cpp | 1374 | `a14d4d607714db60a6ecd662e099259a8531ea1520ce635a6bdfabe4d73fe56b` | 0 |
| src/xrpld/rpc/handlers/admin/BlackList.cpp | 479 | `bd3f42ef6e39e604cb7451dd717542e9625d2cff465732d590f2e04a0b7e692d` | 0 |
| src/xrpld/rpc/handlers/admin/UnlList.cpp | 788 | `01bd336ba8e552560d9b228785a7796b7b9f5de472fb2d9168aff03eed3b63b2` | 0 |
| src/xrpld/rpc/handlers/admin/data/CanDelete.cpp | 2485 | `2e6ff45fc3de29f8f2095164ce84fb3ed26c824e7272d8fa35cc44e1008a632c` | 0 |
| src/xrpld/rpc/handlers/admin/data/LedgerCleaner.cpp | 402 | `ca482475302e458f16c97a2359f46fa032513a199e8f043ec4a84e0e99e4b8f8` | 0 |
| src/xrpld/rpc/handlers/admin/data/LedgerRequest.cpp | 739 | `de9eb8008d1f927e91b350ac3dcb464441039d7b9a74cc298ded386a45eecc9c` | 0 |
| src/xrpld/rpc/handlers/admin/keygen/ValidationCreate.cpp | 1392 | `ee18c1542c156be6251ede33355936b1775594e997bb9a3430c4a8e21d08484f` | 0 |
| src/xrpld/rpc/handlers/admin/keygen/WalletPropose.cpp | 4872 | `66a3ccf740c5e263e5598bb972c17e9b8ae9dc9674b102c3651675df64c63b76` | 0 |
| src/xrpld/rpc/handlers/admin/keygen/WalletPropose.h | 143 | `2ea9fe9b384e2e08e38de0aab70d9f1281d8a6c60eeed6b487061cfe28a90e7b` | 0 |
| src/xrpld/rpc/handlers/admin/log/LogLevel.cpp | 2092 | `de091ecd65d396ced783d142176133e4079f0e4044512a0c0ca19b81d1ed8b9c` | 0 |
| src/xrpld/rpc/handlers/admin/log/LogRotate.cpp | 404 | `aee93cecd96239d46b1d11e3671a812fe0fc0a081fefe7d3c4669aa9de6bdd19` | 0 |
| src/xrpld/rpc/handlers/admin/peer/Connect.cpp | 1487 | `0a169bca81324d2164bef0728c9d6308c962ec02f0d6c747d9be7b6b8f994bdb` | 0 |
| src/xrpld/rpc/handlers/admin/peer/PeerReservationsAdd.cpp | 2499 | `7277e03cfcedba1ae2e7927d9ca2c67074df0888ef60fb65636fbf5cb38ebf6f` | 0 |
| src/xrpld/rpc/handlers/admin/peer/PeerReservationsDel.cpp | 1239 | `717c6aaf1195f4bc447fd2e1fa960a4b11ad038036e8d8dc88ce3ef216b62b67` | 0 |
| src/xrpld/rpc/handlers/admin/peer/PeerReservationsList.cpp | 726 | `01094442bfa0753d440fbdb8ca9c55be796c21b83b8766c7d801edc4ef2cf79f` | 0 |
| src/xrpld/rpc/handlers/admin/peer/Peers.cpp | 2097 | `466d747711708fe892bc2fdf6e69a0ecfea27d71c7037160bf7f8b27e210a807` | 0 |
| src/xrpld/rpc/handlers/admin/server_control/LedgerAccept.cpp | 736 | `a9b596f66b6f4f7f166d15e91af1fd0de5f8ef92c3c255c59ea8b087c4fe8ae1` | 0 |
| src/xrpld/rpc/handlers/admin/server_control/Stop.cpp | 408 | `ad0f0f8b7837a174e7bdcdf2ad1af509ab58a326daf95d3a1697647d83face64` | 0 |
| src/xrpld/rpc/handlers/admin/signing/ChannelAuthorize.cpp | 3090 | `8d3de2b3d73d5134d882b0d97b592641e93c08b89f24079765fc711227928047` | 0 |
| src/xrpld/rpc/handlers/admin/signing/Sign.cpp | 1237 | `154f0b870dc2864ce01ac760657c050721fa52aaea57f39b2fd90eef00862ae5` | 0 |
| src/xrpld/rpc/handlers/admin/signing/SignFor.cpp | 1261 | `33bffeb381534c9182c5188026051c46a1bb7f72da9a03a746ff3cb1f052d514` | 0 |
| src/xrpld/rpc/handlers/admin/status/ConsensusInfo.cpp | 353 | `570206839ca623ee44b7224bc0d6c94d8b0436d30a2943080804ca48a27d2d2e` | 0 |
| src/xrpld/rpc/handlers/admin/status/FetchInfo.cpp | 523 | `3c129dd13cdec2cba5256cb8f11f8c0434e0aed45ed428a829394b8cf87df642` | 0 |
| src/xrpld/rpc/handlers/admin/status/GetCounts.cpp | 3215 | `d109b0de495c4f18b32536d1d96bfca635cadcba3f374d9ea1f24d5fa41ffaa7` | 0 |
| src/xrpld/rpc/handlers/admin/status/GetCounts.h | 195 | `fbdfab3581c10039e4f9c7d4f55f854cb4f2f6cfd3d6fdef8b8283e68cabdfe0` | 0 |
| src/xrpld/rpc/handlers/admin/status/Print.cpp | 605 | `6d9cd9f664d9e76ad2e7a13f81357784d8a019d10f9cced98e3d9b4eaa5eaf52` | 0 |
| src/xrpld/rpc/handlers/admin/status/ValidatorInfo.cpp | 1456 | `f0c71439e4d315696b24dd6d7b1591237e6494625cbd73217ea79c549606b833` | 0 |
| src/xrpld/rpc/handlers/admin/status/ValidatorListSites.cpp | 307 | `008efb149d55783560a56505d5d272632398c7f1432593e017235956b38fa81f` | 0 |
| src/xrpld/rpc/handlers/admin/status/Validators.cpp | 295 | `dbae34b232f6be5bbc57237e41b263290b274e6ce09a9e5651f5d81a0b982b4a` | 0 |
| src/xrpld/rpc/handlers/ledger/Ledger.cpp | 12779 | `f5fa11f7b4ab596eac986fdde91cbb4514731a03c8a79e6185c8508c1d240a87` | 0 |
| src/xrpld/rpc/handlers/ledger/Ledger.h | 2054 | `55f18615213034af10a2597be2ddc3b70bfe7e21e0a478af4d417e87f852f365` | 0 |
| src/xrpld/rpc/handlers/ledger/LedgerClosed.cpp | 668 | `a8705f8779f6110edb5200b8d490fcd2100b1db17adc5846dbbad30139c549d0` | 0 |
| src/xrpld/rpc/handlers/ledger/LedgerCurrent.cpp | 411 | `7c3a3998405e6e18da36033c03ad2064fe966fd1a2703445ee282e68b7fec5d6` | 0 |
| src/xrpld/rpc/handlers/ledger/LedgerData.cpp | 6404 | `c03123cf5a6ddbdb70f79fc4875a5c361db35006bf28fe578374cf2cec9acb98` | 0 |
| src/xrpld/rpc/handlers/ledger/LedgerDiff.cpp | 3006 | `a8e9216a27caccb2f716051db19cab1a2596541c493a1eaa10db0f4f3d2c6900` | 0 |
| src/xrpld/rpc/handlers/ledger/LedgerEntry.cpp | 32463 | `14e33e6e1854b7657640772f51ac121e78422f303b90ce86f8202a5030bd072c` | 0 |
| src/xrpld/rpc/handlers/ledger/LedgerEntryHelpers.h | 5860 | `a9791c11c5bd1c4f2be7b622bdf75df168a5d10dc568f11963f1cf356b3ecbba` | 0 |
| src/xrpld/rpc/handlers/ledger/LedgerHeader.cpp | 911 | `2e13b080b46208681f56df160b0f9597c4e7256ca3a7f4efec8a10452b232419` | 0 |
| src/xrpld/rpc/handlers/orderbook/AMMInfo.cpp | 9056 | `ed0bb24da7afa0fc126ba652e6252bde2085698794b6d00b36f77804d8d7192c` | 0 |
| src/xrpld/rpc/handlers/orderbook/BookChanges.cpp | 896 | `bc7eb065cf40df6561539a0c54e8de86e60a06fbf1d36b6d7e30ef7973467e14` | 0 |
| src/xrpld/rpc/handlers/orderbook/BookChanges.h | 1607 | `792d07b7924d8e2ddc64df1d958cdb7d8835c31de63dbf9de6c5da5658c67ef2` | 0 |
| src/xrpld/rpc/handlers/orderbook/BookOffers.cpp | 7793 | `413b5849178580f20382a121f00eb2e0b2893c38718bf43de4c0ca98d67ef8d2` | 0 |
| src/xrpld/rpc/handlers/orderbook/DepositAuthorized.cpp | 4602 | `5c84c61e8244bf79ea24fdeb6b76ae99e34b1b0b4bb9a910c2381fea204993e3` | 0 |
| src/xrpld/rpc/handlers/orderbook/DepositAuthorized.h | 1849 | `bdbade60c6de382fdae2a0dd0807369232844c39b987d25bbe6552f5f9ce6771` | 0 |
| src/xrpld/rpc/handlers/orderbook/GetAggregatePrice.cpp | 13755 | `51c1ad1ddb60a4a3a6e4529bccbf2f61e49cdb66f1b52d07d28f23d32084b9c6` | 0 |
| src/xrpld/rpc/handlers/orderbook/NFTBuyOffers.cpp | 566 | `e74ace3aa60eb39a4260eda1ec54d1620d9b440b67a63e1dce3ff159884a09d4` | 0 |
| src/xrpld/rpc/handlers/orderbook/NFTBuyOffers.h | 892 | `3124a20189cbe3de8312fe2e39a34036fc52311e45dd1b752685188b4a332681` | 0 |
| src/xrpld/rpc/handlers/orderbook/NFTOffersCommon.cpp | 5126 | `3c00004f7a407b4fae1674f0a764c2b34fd661d9c5eb00afae2e45584177172d` | 0 |
| src/xrpld/rpc/handlers/orderbook/NFTOffersCommon.h | 2255 | `0de05635f532468fb3f62db345b8cf29a7250f448702074be288478964d9dd3b` | 0 |
| src/xrpld/rpc/handlers/orderbook/NFTSellOffers.cpp | 572 | `6bb918c2926cf8214a6e8e2da3887f2b27212e3eb3fbc0b814e25efe88a92f69` | 0 |
| src/xrpld/rpc/handlers/orderbook/NFTSellOffers.h | 895 | `0558fbc7e7720a529c5dd08d48e82294e711d20ab9e0096d3e82e5b810b81dff` | 0 |
| src/xrpld/rpc/handlers/orderbook/PathFind.cpp | 1790 | `bd62a153a663b47d149668b86540010fe895c7d064e2315e040119a0ef61483b` | 0 |
| src/xrpld/rpc/handlers/orderbook/RipplePathFind.cpp | 6915 | `652da2b550a3722d7f776be7beb8b45e1356781ec86dbf67566bd5869e17e2ec` | 0 |
| src/xrpld/rpc/handlers/server_info/Feature.cpp | 2498 | `d6c5911c7a49ca0b3069bc3ec2bd6e609acf1657a73a0d509e02cfeaa1d9bab1` | 0 |
| src/xrpld/rpc/handlers/server_info/Fee.cpp | 623 | `5ca4983bd88212fc69fe10422c467a93ce66ec27bbaceb097705f613c3450157` | 0 |
| src/xrpld/rpc/handlers/server_info/Manifest.cpp | 1845 | `99f52a84131f6eb7173b2c7d3a35fb6fef2557350e68dbe6db01d7b5aac0a0d5` | 0 |
| src/xrpld/rpc/handlers/server_info/ServerDefinitions.cpp | 12358 | `c596d46e37bce9d42a272e8e780cbdc44f5f58f76fd7f8a16cb884ecdf631fab` | 0 |
| src/xrpld/rpc/handlers/server_info/ServerDefinitions.h | 136 | `7d5ca96f72455c82bb293a11c707dc070583158e6df6e27004da6a9c6e60dc84` | 0 |
| src/xrpld/rpc/handlers/server_info/ServerInfo.cpp | 550 | `b2cc0d7bf22a346378ad82b156c3cc3e01758631f871610448b78d44c132dcc3` | 0 |
| src/xrpld/rpc/handlers/server_info/ServerState.cpp | 518 | `5222dfbcbd01f4b8d8a3cacc98fd2653f996a1fe8de5f1f11c7ef3ce86d23542` | 0 |
| src/xrpld/rpc/handlers/server_info/Version.h | 1676 | `89a828adef7017e75a603ac26e76ef948298b3106ce1d267b49f7d0657f1caf2` | 0 |
| src/xrpld/rpc/handlers/subscribe/Subscribe.cpp | 15447 | `af81606bd1efefb1d196dd273c361aca901c6f94ce758ed14bda63a9d329d9cd` | 0 |
| src/xrpld/rpc/handlers/subscribe/Unsubscribe.cpp | 7545 | `69420a41d9b54824cfcfdf0d7727ccbe482a5f1388116e82342d9852be794b12` | 0 |
| src/xrpld/rpc/handlers/transaction/Simulate.cpp | 12215 | `aa4c21fb11c1ff17824fd856e946757112753f660e133c712981ba9fe31f7027` | 1 |
| src/xrpld/rpc/handlers/transaction/Submit.cpp | 5888 | `c3247aab1330b5b3d7dd3b6602fc0c6aca6b8e14e789d7003058a7453c58326a` | 0 |
| src/xrpld/rpc/handlers/transaction/SubmitMultiSigned.cpp | 827 | `ec62395fc64f5c0b16ab9ad4de686d3a57d9f730712664de213fd633d2e321b8` | 0 |
| src/xrpld/rpc/handlers/transaction/TransactionEntry.cpp | 3207 | `ffcc7f6f5ff4d5e3ad36f9dc2d55a0d47688ecc972cc5ff915954bba259718fb` | 0 |
| src/xrpld/rpc/handlers/transaction/TransactionEntry.h | 2017 | `15cd054a260996bf70df74ebc685549df36486453487a7df13ed036de5556095` | 0 |
| src/xrpld/rpc/handlers/transaction/Tx.cpp | 10083 | `3fa67f9c890a846bebefbb25d4c6d4bfea2d54bd3a773ed88e3f0e0d94a61b02` | 0 |
| src/xrpld/rpc/handlers/transaction/TxHistory.cpp | 1323 | `bcb5e6cb99203fc4b0748e55da5bf25241a050cca61ea1f043963493edb3253a` | 0 |
| src/xrpld/rpc/handlers/transaction/TxReduceRelay.cpp | 290 | `7646ece030db660a5e28802a54cb789c4a6f26f3fae7bf4e299966e7709e7981` | 0 |
| src/xrpld/rpc/handlers/utility/Ping.cpp | 1168 | `09ec6ae8dfe59a37f82e4de22f5995b181a48341aa1cb0ae3c9be5475f745297` | 0 |
| src/xrpld/rpc/handlers/utility/Random.cpp | 882 | `5dd8080e7e783a8a1c407c67608c095cab3cbb7082858c5834e15188a6b13a62` | 0 |
| src/xrpld/rpc/json_body.h | 2848 | `f9b6cb065441a6f29be856f0660854994e3a7b49f9a85b3866b4a82d0dbe031c` | 0 |
| src/xrpld/shamap/NodeFamily.cpp | 2560 | `987b2d7679d0402cc0dd077ca3fc0a7ddd941e0a282318377836fa26b8d2dbfb` | 0 |
| src/xrpld/shamap/NodeFamily.h | 1850 | `b7f6140ca29a6e6182aaff26ba88c0963a78bb8822f0497d013a3361abc99623` | 0 |
