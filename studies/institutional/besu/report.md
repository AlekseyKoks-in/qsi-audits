# Security & Post-Quantum Readiness Audit Report

**Project:** besu @ 1f1ebc2573e1 · Hyperledger Besu — public repository (passive review)
| | |
|---|---|
| Organization | QSI |
| Report date | 2026-11-06 15:36 UTC |
| Report version | 1 |
| Audit run | 9e414b52-3a81-4bd6-96a2-eeef0fccce6f (Document audit) |
| Analyzer engine | qsi-engine 1.3.0 |
| Risk profile | Crypto exchange, custodian or wallet |
| Content SHA-256 | `25c60fc9a59edc6c0ea69ca2871ea1967c583c30f639e09b309380192ecf324d` |
| Signature key (Ed25519, SHA-256 fingerprint; the signature is the separate file report.sig.json) | `5b3cf9c9bd0fa54447e2b5dfa7a6bab569bd0c666fa46949599e5c348d17083e` |
> This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.

## 1. Executive summary

- Critical: **0**
- High: **0**
- Medium: **7**
- Low: **0**
- Info: **0**

- Confirmed technical vulnerability: 0
- Known vulnerable component: 0
- Confirmed configuration error: 0
- Potential cryptographic risk: 0
- Long-term post-quantum risk: 7
- Improvement recommendation: 0
- Insufficient data: 0

Mosca's inequality (x + y > z): x = 10, y = 5, z = 8 → migration would finish too late under this scenario. _z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today._

**Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography.** Next step: Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

## 2. Scope and boundaries

Mode: Document audit

Repository: <https://github.com/besu-eth/besu> @ `1f1ebc2573e187a1339887fbc2a859f095029f21` — evidence links open the lines at this commit.

2927 files, 14494630 bytes in total, 1 redaction(s); the per-file SHA-256 list is in appendix C.

## 3. Methodology

| Area | Status | Count | Examples |
|---|---|---|---|
| source_code | checked | 2927 | .github/scripts/verifyArtifacts.py: 55 lines scanned with 16 rule patterns and 267 registry patterns; app/build.gradle: 121 lines scanned with 16 rule patterns and 267 registry patterns; app/src/main/java/org/hyperledger/besu/Besu.java: 108 lines scanned with 16 rule patterns and 267 registry patterns |
| secrets | checked | 1 | ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/DefaultAuthenticationService.java: 1 redacted value(s) not reported (comments, test modules, fixture declarations, placeholders, values the source annotates as published, or hex values not bound to a secret name) |
| keys | error (not checked) | 1 | ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/JWTAuthOptionsFactory.java line 118: public key could not be parsed (ValueError) |
| certificates_and_keys | checked | 1 | ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/JWTAuthOptionsFactory.java: certificates/keys parsed |
| entropy | checked | 1 | random-number generation: 2867 code files read with 0 macro definitions from the tree; 0 ineffective guard(s), 0 weak random-bytes provider(s), 0 weak key-generation site(s) |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## 4. Assets examined and not examined

- keys — error (not checked): ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/JWTAuthOptionsFactory.java line 118: public key could not be parsed (ValueError)

## 5. Architecture overview

Static review of the source tree besu at 1f1ebc2573e187a1339887fbc2a859f095029f21. 2927 files analysed; of 58293 files, 55251 are test, fuzzing, benchmark or example code and were left out, 115 are not read by any analyzer, 0 exceed the per-file limit and 0 did not fit the total limit. Files no analyzer reads include: .dockerignore, .gitattributes, .github/CODEOWNERS, .github/ISSUE_TEMPLATE/bug-report.md, .github/ISSUE_TEMPLATE/contributor-call.md. 100 files in build-output or dependency-cache directories (.git, .hg, .venv, __pycache__, build, dist, node_modules, target, vendor, venv) were not read. No requests were sent to the owner's systems.

## 6. Overall security posture

- Indicative posture index: **100** / 100 — _Derived from findings in scope (confirmed and potential issues weighted by severity). Indicative only; not comparable across differently scoped audits._
- Quantum-vulnerable share of inventory: 54.5%

## 7. Detailed findings

### QSI-2026-19546 — Quantum-vulnerable ECDH: key wrapping and data encryption at rest (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDH:key_wrapping`
- Data source: ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESHandshaker.java
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:36 UTC
- Priority score: 36.9 / 100
- CVSS v3.1: not applicable

3 reference(s) to ECDH across 1 file(s), e.g. ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESHandshaker.java:174. Role, judged from paths, function names and nearby code: key wrapping and data encryption at rest. Keys or data encrypted to these public keys are stored: anyone who copies them now decrypts them once a CRQC exists (harvest now, decrypt later).

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESHandshaker.java:174 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESHandshaker.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESHandshaker.java#L174) · line 174 · SHA-256 42c03230e34128e44f0465759e8e38e4e0e6189fe6767b4c5274745dce7aba18_

```
  173 |       throw new HandshakeException(
  174 |           "Unable to create ECDH Key agreement due to Crypto engine failure", e);
  175 |     }
```

_file_excerpt · [ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESHandshaker.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESHandshaker.java#L215) · line 215 · SHA-256 98072aee9a15f59c9d5bde25dcc80616f9a1f13c190bafebf3c63f556b0d0ff6_

```
  214 |         throw new HandshakeException(
  215 |             "Unable to create ECDH Key agreement due to Crypto engine failure", e);
  216 |       }
```

_file_excerpt · [ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESHandshaker.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESHandshaker.java#L256) · line 256 · SHA-256 87fc8b8ce160e50ab18034dbec0b6ff5eedcd04929cd0d9ab4d99a025b0f2aac_

```
  255 |       throw new HandshakeException(
  256 |           "Unable to create ECDH Key agreement due to Crypto engine failure", e);
  257 |     }
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19543 — Quantum-vulnerable ECDSA: transaction and message signing (6 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:transaction_signing`
- Data source: crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:36 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

22 reference(s) to ECDSA across 6 file(s), e.g. crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java:18. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java:18 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java#L18) · line 18 · SHA-256 e213dc5290ded225a88c42d82ffacc0652e7434bc1beceffe3bc459e5ddd271c_

```
   17 | import static com.google.common.base.Preconditions.checkArgument;
   18 | import static org.hyperledger.besu.nativelib.secp256k1.LibSecp256k1.SECP256K1_EC_UNCOMPRESSED;
   19 | 
```

_file_excerpt · [crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java#L20) · line 20 · SHA-256 8837eca5a7718c4fe5601891bfaace12b85cb5d85e1e21c29b49956ea9f77a41_

```
   19 | 
   20 | import org.hyperledger.besu.nativelib.secp256k1.LibSecp256k1;
   21 | import org.hyperledger.besu.nativelib.secp256k1.LibSecp256k1.secp256k1_ecdsa_recoverable_signature;
```

_file_excerpt · [crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java#L21) · line 21 · SHA-256 c64cb72b25eb14c8043c23e171b88460dee34713443d789aa5a3ab23d7443700_

```
   20 | import org.hyperledger.besu.nativelib.secp256k1.LibSecp256k1;
   21 | import org.hyperledger.besu.nativelib.secp256k1.LibSecp256k1.secp256k1_ecdsa_recoverable_signature;
   22 | import org.hyperledger.besu.nativelib.secp256k1.LibSecp256k1.secp256k1_ecdsa_signature;
```

_file_excerpt · [ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv5/PeerDiscoveryAgentFactoryV5.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv5/PeerDiscoveryAgentFactoryV5.java#L285) · line 285 · SHA-256 d5ef02c2df4225b5f5b5d7f8d3a2984498a5ea04e71a8bc70eb1ff4c06ad19a8_

```
  284 |           } catch (final RuntimeException e) {
  285 |             LOG.debug("DiscV5: Rejecting peer with missing or malformed secp256k1 key", e);
  286 |             return false;
```

_file_excerpt · [ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/dns/EthereumNodeRecord.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/dns/EthereumNodeRecord.java#L104) · line 104 · SHA-256 425b39f2d8f3eabcc83d1447e01d9bb3446bda6b213ef3423b1046fc665c987a_

```
  103 |     if (!(value instanceof Bytes keyBytes)) {
  104 |       throw new IllegalArgumentException("Missing secp256k1 entry in ENR");
  105 |     }
```

_file_excerpt · [ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/dns/EthereumNodeRecord.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/dns/EthereumNodeRecord.java#L117) · line 117 · SHA-256 51873f0e6a9e6c17a313b4311ebfcdf4ef68634cabaf9860911aa1996c1d4f62_

```
  116 |   static Bytes initPublicKeyBytes(final Map<String, Object> fields) {
  117 |     final Object value = fields.get("secp256k1");
  118 |     if (!(value instanceof Bytes keyBytes)) {
```

_file_excerpt · [ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/dns/EthereumNodeRecord.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/dns/EthereumNodeRecord.java#L119) · line 119 · SHA-256 6ec20acdd3b8c880eb0906cc20cbf86d580ec28cb3e89720726a2e2b6adcece1_

```
  118 |     if (!(value instanceof Bytes keyBytes)) {
  119 |       throw new IllegalArgumentException("Missing secp256k1 entry in ENR");
  120 |     }
```

_file_excerpt · [evm/build.gradle](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/evm/build.gradle#L53) · line 53 · SHA-256 4e3210a305ad5733da441b6266d7167609678aab3aba790db07a29aa2de4893a_

```
   52 |   implementation 'org.hyperledger.besu:gnark'
   53 |   implementation 'org.hyperledger.besu:secp256k1'
   54 |   implementation 'org.hyperledger.besu:boringssl'
```

_file_excerpt · [evm/src/main/java/org/hyperledger/besu/evm/precompile/ECRECPrecompiledContract.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/evm/src/main/java/org/hyperledger/besu/evm/precompile/ECRECPrecompiledContract.java#L24) · line 24 · SHA-256 f8a0dc427ec38cd30650f356f384a4fe1f77c2457d1623533c4642f5ac379f4f_

```
   23 | import org.hyperledger.besu.evm.gascalculator.GasCalculator;
   24 | import org.hyperledger.besu.nativelib.secp256k1.LibSecp256k1JNI;
   25 | 
```

_file_excerpt · [evm/src/main/java/org/hyperledger/besu/evm/precompile/ECRECPrecompiledContract.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/evm/src/main/java/org/hyperledger/besu/evm/precompile/ECRECPrecompiledContract.java#L142) · line 142 · SHA-256 28061cc24efb13d7f06d9c08e7ce7e412019d17e2347fdddd50b12f8f04be022_

```
  141 |     final LibSecp256k1JNI.ECRecoverResult ecres =
  142 |         LibSecp256k1JNI.ecrecover(messageHash.toArrayUnsafe(), sigBytes, recId);
  143 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19544 — Quantum-vulnerable BLS12-381: transaction and message signing (11 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:BLS12-381:transaction_signing`
- Data source: datatypes/src/main/java/org/hyperledger/besu/datatypes/Address.java
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:36 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

19 reference(s) to BLS12-381 across 11 file(s), e.g. datatypes/src/main/java/org/hyperledger/besu/datatypes/Address.java:71. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open datatypes/src/main/java/org/hyperledger/besu/datatypes/Address.java:71 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [datatypes/src/main/java/org/hyperledger/besu/datatypes/Address.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/datatypes/src/main/java/org/hyperledger/besu/datatypes/Address.java#L71) · line 71 · SHA-256 e58e8c52f78004becd67c22f4e246560e4d0b760b0eb186a9e333f5d96a29a5a_

```
   70 |   /** The constant BLS12_G1ADD. */
   71 |   public static final Address BLS12_G1ADD = Address.precompiled(0xB);
   72 | 
```

_file_excerpt · [datatypes/src/main/java/org/hyperledger/besu/datatypes/Address.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/datatypes/src/main/java/org/hyperledger/besu/datatypes/Address.java#L77) · line 77 · SHA-256 0533fcc06d6c9b5458a0667328fcea6949c04afa567906f5509f70f7e8d77a8c_

```
   76 |   /** The constant BLS12_G2ADD. */
   77 |   public static final Address BLS12_G2ADD = Address.precompiled(0xD);
   78 | 
```

_file_excerpt · [datatypes/src/main/java/org/hyperledger/besu/datatypes/Address.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/datatypes/src/main/java/org/hyperledger/besu/datatypes/Address.java#L86) · line 86 · SHA-256 5d84cf57c715bc3eacc6e9a765ee5802f317f40055d927b9f532f288b7f9bf16_

```
   85 |   /** The constant BLS12_MAP_FP_TO_G1. */
   86 |   public static final Address BLS12_MAP_FP_TO_G1 = Address.precompiled(0x10);
   87 | 
```

_file_excerpt · [evm/src/main/java/org/hyperledger/besu/evm/gascalculator/OsakaGasCalculator.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/evm/src/main/java/org/hyperledger/besu/evm/gascalculator/OsakaGasCalculator.java#L17) · line 17 · SHA-256 527f9b389d2b50a4300ebf350ec973bc1f35d9b764639366e39c23f17e04131f_

```
   16 | 
   17 | import static org.hyperledger.besu.datatypes.Address.BLS12_MAP_FP2_TO_G2;
   18 | import static org.hyperledger.besu.datatypes.Address.P256_VERIFY;
```

_file_excerpt · [evm/src/main/java/org/hyperledger/besu/evm/gascalculator/OsakaGasCalculator.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/evm/src/main/java/org/hyperledger/besu/evm/gascalculator/OsakaGasCalculator.java#L47) · line 47 · SHA-256 2b06278ff3568ba213d68885871aa372e52539545dd5f705170eb0ba6001390d_

```
   46 |   public OsakaGasCalculator() {
   47 |     this(BLS12_MAP_FP2_TO_G2.getBytes().getInt(16), P256_VERIFY.getBytes().getInt(16));
   48 |   }
```

_file_excerpt · [evm/src/main/java/org/hyperledger/besu/evm/gascalculator/PragueGasCalculator.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/evm/src/main/java/org/hyperledger/besu/evm/gascalculator/PragueGasCalculator.java#L17) · line 17 · SHA-256 3173f71ac46444ef1b3f69926257ec73fab684a48fd508fb2944cab51905c8f3_

```
   16 | 
   17 | import static org.hyperledger.besu.datatypes.Address.BLS12_MAP_FP2_TO_G2;
   18 | import static org.hyperledger.besu.evm.internal.Words.clampedAdd;
```

_file_excerpt · [evm/src/main/java/org/hyperledger/besu/evm/gascalculator/PragueGasCalculator.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/evm/src/main/java/org/hyperledger/besu/evm/gascalculator/PragueGasCalculator.java#L43) · line 43 · SHA-256 b404f0e946832d4b2d05ba984f1cbd9c4733c2c5f1fbf0cb62bdead35015e20d_

```
   42 |   public PragueGasCalculator() {
   43 |     this(BLS12_MAP_FP2_TO_G2.getBytes().toArrayUnsafe()[19]);
   44 |   }
```

_file_excerpt · [evm/src/main/java/org/hyperledger/besu/evm/precompile/BLS12G1AddPrecompiledContract.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/evm/src/main/java/org/hyperledger/besu/evm/precompile/BLS12G1AddPrecompiledContract.java#L31) · line 31 · SHA-256 f855ee8b03d9894b4d8d428d20f1bcd0a90cb2dec5489ad4fc5426f6982305ba_

```
   30 |   BLS12G1AddPrecompiledContract() {
   31 |     super("BLS12_G1ADD", LibGnarkEIP2537.BLS12_G1ADD_OPERATION_SHIM_VALUE, PARAMETER_LENGTH);
   32 |   }
```

_file_excerpt · [evm/src/main/java/org/hyperledger/besu/evm/precompile/BLS12G1MultiExpPrecompiledContract.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/evm/src/main/java/org/hyperledger/besu/evm/precompile/BLS12G1MultiExpPrecompiledContract.java#L36) · line 36 · SHA-256 970e4da8775ce75f51236165f636317162b750527a9ec0433fc0eed7f5132cb8_

```
   35 |     super(
   36 |         "BLS12_G1MSM",
   37 |         LibGnarkEIP2537.BLS12_G1MULTIEXP_OPERATION_SHIM_VALUE,
```

_file_excerpt · [evm/src/main/java/org/hyperledger/besu/evm/precompile/BLS12G2AddPrecompiledContract.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/evm/src/main/java/org/hyperledger/besu/evm/precompile/BLS12G2AddPrecompiledContract.java#L31) · line 31 · SHA-256 91ac540fb5c1f99f84c28e4b4f1e50adc267e8efe6a715dd52db6980cb38b511_

```
   30 |   BLS12G2AddPrecompiledContract() {
   31 |     super("BLS12_G2ADD", LibGnarkEIP2537.BLS12_G2ADD_OPERATION_SHIM_VALUE, PARAMETER_LENGTH);
   32 |   }
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19545 — Quantum-vulnerable RSA: transaction and message signing (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:RSA:transaction_signing`
- Data source: ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/JWTAuthOptionsFactory.java
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:36 UTC
- Priority score: 35.6 / 100
- CVSS v3.1: not applicable

1 reference(s) to RSA across 1 file(s), e.g. ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/JWTAuthOptionsFactory.java:107. Role, judged from paths, function names and nearby code: transaction and message signing. A CRQC derives the private key from a public key that is already known (on chain after the first spend, in reused addresses): funds and approvals controlled by these keys need a migration path.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/JWTAuthOptionsFactory.java:107 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/JWTAuthOptionsFactory.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/JWTAuthOptionsFactory.java#L107) · line 107 · SHA-256 3813339811f033c67742c58c980cd49ea3fdbe44960bd8359b6776b56f2b17b9_

```
  106 |     try {
  107 |       keyGenerator = KeyPairGenerator.getInstance("RSA");
  108 |       keyGenerator.initialize(2048);
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19540 — Quantum-vulnerable ECDSA: role not determined (11 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDSA:general`
- Data source: app/src/main/java/org/hyperledger/besu/cli/BesuCommand.java
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:36 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

35 reference(s) to ECDSA across 11 file(s), e.g. app/src/main/java/org/hyperledger/besu/cli/BesuCommand.java:1546. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open app/src/main/java/org/hyperledger/besu/cli/BesuCommand.java:1546 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [app/src/main/java/org/hyperledger/besu/cli/BesuCommand.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/app/src/main/java/org/hyperledger/besu/cli/BesuCommand.java#L1546) · line 1546 · SHA-256 c1a058e0fbbf811acdb90166141a355344ca7e57549aff22a17779755cf1bb4d_

```
 1545 |       if (SECP256R1.isNativeAvailable()) {
 1546 |         logger.info("Using the native secp256r1 signature algorithm implementation of p256verify");
 1547 |       } else {
```

_file_excerpt · [app/src/main/java/org/hyperledger/besu/cli/BesuCommand.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/app/src/main/java/org/hyperledger/besu/cli/BesuCommand.java#L1548) · line 1548 · SHA-256 66faed59c80f03f3c3a8ba89766fd23cddee2ae4a70a236c78c2f9a05c413503_

```
 1547 |       } else {
 1548 |         logger.info("Using the Java secp256r1 implementation of p256verify");
 1549 |       }
```

_file_excerpt · [app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java#L45) · line 45 · SHA-256 4807d28c98cbe17b1ef9835c2bd28d88764e756d5b80b783bac6186c679b7b50_

```
   44 |         List<NativeRequirementResult> requirements = new ArrayList<>();
   45 |         var secp256k1 = new SECP256K1();
   46 |         requirements.add(
```

_file_excerpt · [app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java#L48) · line 48 · SHA-256 d6861acb7235ee43cd8c5acca8ee8adc6765cc044b397a03092a001add989f05_

```
   47 |             new NativeRequirementResult(
   48 |                 secp256k1.maybeEnableNative(),
   49 |                 "secp256k1",
```

_file_excerpt · [app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java#L49) · line 49 · SHA-256 649702b112a5e653591ff5be8286dae5cfef33ab117cdc90f44a50488712eb46_

```
   48 |                 secp256k1.maybeEnableNative(),
   49 |                 "secp256k1",
   50 |                 secp256k1.maybeEnableNative()
```

_file_excerpt · [app/src/main/java/org/hyperledger/besu/cli/options/NativeLibraryOptions.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/app/src/main/java/org/hyperledger/besu/cli/options/NativeLibraryOptions.java#L63) · line 63 · SHA-256 591bbfa14e538a691c8bc0c4f4ffe3b70c8c0c47929b6ad71f3f4dc9b5bbb753_

```
   62 |           "Per default a BoringSSL native library is used for p256verify. "
   63 |               + "If the secp256r1 native signature algorithm implementation should be used instead, this option must be set to false",
   64 |       arity = "1")
```

_file_excerpt · [app/src/main/java/org/hyperledger/besu/cli/options/P2PDiscoveryOptions.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/app/src/main/java/org/hyperledger/besu/cli/options/P2PDiscoveryOptions.java#L91) · line 91 · SHA-256 556d2d0b5e6b4e68f886185fa7015b36093c52d8ea4b0551d314456106b1136f_

```
   90 |               + "V4 runs only DiscV4. "
   91 |               + "V5 runs only DiscV5 (requires a secp256k1 node key; falls back to V4 if unsupported). "
   92 |               + "BOTH runs DiscV4 and DiscV5 concurrently on a shared UDP socket.")
```

_file_excerpt · [crypto/algorithms/build.gradle](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/crypto/algorithms/build.gradle#L55) · line 55 · SHA-256 008dc0cd78e0987eaf28597634fafb4339f9dc3e95eec1ef66fa967d732e5d82_

```
   54 |   implementation 'io.consensys.tuweni:tuweni-units'
   55 |   implementation 'org.hyperledger.besu:secp256k1'
   56 |   implementation 'org.hyperledger.besu:secp256r1'
```

_file_excerpt · [crypto/algorithms/build.gradle](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/crypto/algorithms/build.gradle#L56) · line 56 · SHA-256 47a846ad19c2b713f8ee7633f975349487ad7485f33dc07fdfe5ef168a6d2243_

```
   55 |   implementation 'org.hyperledger.besu:secp256k1'
   56 |   implementation 'org.hyperledger.besu:secp256r1'
   57 |   implementation 'org.hyperledger.besu:blake2bf'
```

_file_excerpt · [crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/AbstractSECP256.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/AbstractSECP256.java#L376) · line 376 · SHA-256 2cbd5dc8837b5834b24e17da17658b3236d5286531576085cf57999886fd8405_

```
  375 |   public SECPSignature sign(final Bytes32 dataHash, final KeyPair keyPair) {
  376 |     final ECDSASigner signer = new ECDSASigner(getKCalculator());
  377 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19541 — Quantum-vulnerable BN254 (alt_bn128): role not determined (1 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:BN254 (alt_bn128):general`
- Data source: app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:36 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

2 reference(s) to BN254 (alt_bn128) across 1 file(s), e.g. app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java:66. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java:66 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java#L66) · line 66 · SHA-256 d2ccf80800bec3e2c984dedc51ee8a6836c15cff9ff5d6ecc6ab9f06b7d703b1_

```
   65 |                 AltBN128PairingPrecompiledContract.isNative(),
   66 |                 "alt_bn128",
   67 |                 AltBN128PairingPrecompiledContract.isNative()
```

_file_excerpt · [app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java#L69) · line 69 · SHA-256 cda3b35f9940dda222ad60a0eb8a3e2c41b0cbe983df2202376a8bf020e85923_

```
   68 |                     ? Optional.empty()
   69 |                     : Optional.of("alt_bn128: EC native library failed to load")));
   70 | 
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to a post-quantum algorithm; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.

### QSI-2026-19542 — Quantum-vulnerable ECDH: role not determined (4 file(s))

- Severity: **Medium** · Classification: Long-term post-quantum risk · Confidence: Medium · _preliminary — requires further verification_
- Affected asset: `source-code:ECDH:general`
- Data source: crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/AbstractSECP256.java
- Detection method: Regular-expression matching of crypto API patterns; the role comes from words in paths, enclosing function names and the lines around the matches.
- Analyzer: source_code 1.3.0 · 2026-11-06 15:36 UTC
- Priority score: 34.2 / 100
- CVSS v3.1: not applicable

6 reference(s) to ECDH across 4 file(s), e.g. crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/AbstractSECP256.java:171. Role, judged from paths, function names and nearby code: role not determined. The code does not show what the keys protect; review decides the priority.

**Potential impact.** Long-term risk depends on what the algorithm protects: signatures (authenticity until migration) or key exchange/encryption (retroactive decryption of recorded data).

**Reproduction steps.**

```
Open crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/AbstractSECP256.java:171 and inspect the quoted lines; the evidence lists further files.
```

**Evidence.**

_file_excerpt · [crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/AbstractSECP256.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/AbstractSECP256.java#L171) · line 171 · SHA-256 b2fe4f7b7fe22ad85d656cff1788a5ebe9faf8d5a932f05a196b2a0a878eebff_

```
  170 |     final ECPoint point = cleaned.multiply(privKey.getD()).normalize();
  171 |     checkArgument(!point.isInfinity(), "ECDH key agreement point is at infinity");
  172 |     return point;
```

_file_excerpt · [crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java#L93) · line 93 · SHA-256 f120e93435aec368d24d44798c2501acdf35ff2f76feed086aa0675bd9687174_

```
   92 |         && JNI_UNAVAILABLE_LOGGED.compareAndSet(false, true)) {
   93 |       LOG.info("Native secp256k1 ECDH and ecrecover not available, using the Java implementation");
   94 |     }
```

_file_excerpt · [crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java#L204) · line 204 · SHA-256 87d2ecbf9e1ef3ff4d1d6fa6eee2124d70eac48e9d9bfa4b6858e42434f3f1e4_

```
  203 |       throw new IllegalArgumentException(
  204 |           "Could not calculate ECDH key agreement. Public key or private key is invalid.");
  205 |     }
```

_file_excerpt · [crypto/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/securitymodule/SecurityModule.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/crypto/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/securitymodule/SecurityModule.java#L75) · line 75 · SHA-256 467651ea9fe4cd4be1343a480b1eb7bde3bbb47a8fbd1c0c1c10e880074eed4a_

```
   74 |     throw new SecurityModuleException(
   75 |         "Compressed ECDH key agreement is not supported by this security module");
   76 |   }
```

_file_excerpt · [crypto/services/src/main/java/org/hyperledger/besu/cryptoservices/KeyPairSecurityModule.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/crypto/services/src/main/java/org/hyperledger/besu/cryptoservices/KeyPairSecurityModule.java#L87) · line 87 · SHA-256 6a670c9a6f815a7f928aa779b403fa0167eac48e090538b3dfb541b2114230c6_

```
   86 |     } catch (final Exception e) {
   87 |       throw new SecurityModuleException("Unexpected error while calculating ECDH key agreement", e);
   88 |     }
```

_file_excerpt · [crypto/services/src/main/java/org/hyperledger/besu/cryptoservices/KeyPairSecurityModule.java](https://github.com/besu-eth/besu/blob/1f1ebc2573e187a1339887fbc2a859f095029f21/crypto/services/src/main/java/org/hyperledger/besu/cryptoservices/KeyPairSecurityModule.java#L101) · line 101 · SHA-256 0ee7239aedb2a1418ff01b016f067e4cdb1b5c1eb732bd56272924296232a518_

```
  100 |       throw new SecurityModuleException(
  101 |           "Unexpected error while calculating compressed ECDH key agreement", e);
  102 |     }
```

**Limitations of the check.** This is a forward-looking risk that depends on the arrival of a cryptographically relevant quantum computer (CRQC). No such computer is publicly known to exist today; the timeline is uncertain. It is not a present-day exploitable vulnerability. Heuristic pattern match on source text without data-flow analysis. The usage context (security-relevant or not) must be confirmed manually; treat as preliminary.

**Recommendation.** Classify each usage, record data lifetimes, and plan migration to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH; introduce an abstraction layer for crypto-agility.

**Retest procedure.** Re-run the inventory after refactoring.


## 8. Post-quantum assessment

| | Key establishment (x = how long data must stay confidential; harvest now, decrypt later) | Signatures (x = how long signatures/keys must stay trusted) |
|---|---|---|
| Data/key lifetime x | 10 | 10 |
| Migration time y | 5 | 5 |
| Assumed years to CRQC z | 8 (early) | 8 |
| x + y − z | 7 → migration would finish too late under this scenario | 7 → migration would finish too late under this scenario |
#### Where z comes from

Averaged expert likelihood that a CRQC exists within each horizon, from the annual survey published by the author of this inequality. Likelihood estimates, not predictions of a date.

| Within | Likelihood | The report's wording |
|---|---|---|
| 5 years | ~15% | averaged estimate |
| 10 years | 28-49% | quite possible |
| 15 years | 51-70% | likely |

**Why this scenario (early, z = 8):** Inside the 10-year horizon the survey puts at 28-49% ('quite possible'), and consistent with the BSI estimate of 15 years that 'could shrink to 10 or even less'. Use it for data that must stay confidential for decades, where being wrong is expensive.
_Planning assumptions: x for key establishment, x for signatures, y are the defaults of the risk profile “Crypto exchange, custodian or wallet”, not the client's figures; with the client's actual lifetimes the verdict can change._

### Post-quantum maturity: Level 0 of 4 — no post-quantum cryptography

- Classical only — key wrapping and data encryption at rest: ECDH (1 file(s))

**Next step:** Inventory where classical public-key cryptography protects long-lived data and keys, and choose the first migration: usually a hybrid TLS key exchange and wrapped keys.

_Levels: 0 none; 1 present, not wired; 2 in use outside the critical paths; 3 hybrid in a critical path; 4 post-quantum by default in the critical paths (root of trust, key wrapping, channel key exchange). Judged from code and manifests._

### What the quantum-vulnerable algorithms do

| Role | Algorithms (files) | ID | First step |
|---|---|---|---|
| **key wrapping and data encryption at rest** | ECDH (1) | QSI-2026-19546 | Wrap keys with ML-KEM or a hybrid KEM (X25519 + ML-KEM-768) and re-wrap the stored keys; data that may already have been copied needs its own assessment |
| **transaction and message signing** | BLS12-381 (11), ECDSA (6), RSA (1) | QSI-2026-19543, QSI-2026-19544, QSI-2026-19545 | Follow each chain's post-quantum roadmap, avoid public-key reuse, and keep signers ready to add post-quantum signature schemes as chains adopt them |
| **role not determined** | ECDSA (11), ECDH (4), BN254 (alt_bn128) (1) | QSI-2026-19540, QSI-2026-19541, QSI-2026-19542 | Classify each usage, record data lifetimes, and plan migration to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it; introduce an abstraction layer for crypto-agility |

_Roles are judged from file paths, function names and the code around each match; review confirms them. Root-of-trust keys and wrapped keys come first: they are hard to replace or can be recorded today._
No readiness questionnaire was completed for this project.

### Quantum algorithms relevant to this inventory

| Quantum algorithm | Effect | Attack model | Inventoried algorithms (rows) | What it means for this audit |
|---|---|---|---|---|
| Shor's algorithm — factoring | breaks | Q1 | RSA (2) | Breaks RSA at every key length: a longer modulus only raises the cost polynomially. Plan migration to ML-KEM (or a hybrid) for key establishment and ML-DSA / SLH-DSA for signatures; start with keys protecting data that must stay confidential for years (harvest now, decrypt later) and with long-lived signatures. |
| Shor's algorithm — discrete logarithms in finite fields | breaks | Q1 | BLS12-381 (11), BN254 (alt_bn128) (1) | Breaks finite-field Diffie–Hellman and DSA at every size. Move key establishment to ML-KEM (hybrid with X25519 or ECDH during the transition) and signatures to ML-DSA or SLH-DSA. |
| Shor's algorithm — elliptic-curve discrete logarithms | breaks | Q1 | BLS12-381 (11), BN254 (alt_bn128) (1), ECDH (5), ECDSA (23) | Elliptic-curve keys are expected to fall before RSA keys of comparable classical strength. On blockchains, coins whose public key is already on chain (reused addresses, pay-to-public-key and Taproot outputs) are exposed first; plan the move to post-quantum signatures and avoid key reuse in the meantime. |
| Grover's algorithm — key search and preimages | weakens (larger keys restore the margin) | Q1 | HMAC (1), Keccak-256 (29), SHA-2 (3), bcrypt (1) | Not a break. 256-bit keys (AES-256, ChaCha20) keep a comfortable margin; AES-128 meets NIST category 1, while some authorities ask for 256-bit keys in quantum-resistant contexts (see the AES-128 entry). Prefer 256-bit keys for long-lived data; 256-bit hashes need no change for preimage resistance. |
| Brassard–Høyer–Tapp — collision search | weakens (larger keys restore the margin) | Q1 | Keccak-256 (29), SHA-2 (3) | 256-bit hashes (SHA-256, SHA3-256) remain adequate for collision resistance; 160-bit hashes are already weak classically (SHA-1 collisions are practical). Use 384/512-bit hashes where NIST categories 4–5 are required. |

_Effects: breaks — replace the algorithm; weakens — larger keys or outputs restore the margin; included in standard parameters — no action at standard parameter sets; only with superposition queries — not applicable to ordinary deployments._


## 9. Limitations and assumptions

- This report presents automated and documented analysis results for the stated scope. It is not a legal opinion, a certification or an attestation of compliance with any standard.
- z is a planning assumption chosen per risk profile, not a prediction. A cryptographically relevant quantum computer is not publicly known to exist today.
- keys: ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/JWTAuthOptionsFactory.java line 118: public key could not be parsed (ValueError)

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
| P3 | QSI-2026-19546 | Add ECDH usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19543 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19544 | Add BLS12-381 usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19545 | Add RSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19540 | Add ECDSA usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19541 | Add BN254 (alt_bn128) usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P3 | QSI-2026-19542 | Add ECDH usages at source code to the cryptographic inventory with an owner and a data-lifetime estimate; design for crypto-agility (algorithm identifiers, configurable providers). | short-term risk reduction | Inventory entry with owner, lifetime and target algorithm exists. |
| P4 | QSI-2026-19546 | Plan migration of ECDH to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |
| P4 | QSI-2026-19543 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19544 | Plan migration of BLS12-381 to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-19545 | Plan migration of RSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19540 | Plan migration of ECDSA to ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows ML-DSA (FIPS 204) or SLH-DSA (FIPS 205), in a hybrid/composite form where the ecosystem supports it or a hybrid scheme in use. |
| P4 | QSI-2026-19541 | Plan migration of BN254 (alt_bn128) to  (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows  or a hybrid scheme in use. |
| P4 | QSI-2026-19542 | Plan migration of ECDH to Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH (or a hybrid scheme) once supported by your libraries, protocols and counterparties. | root-cause fix | Re-audit shows Hybrid key establishment with ML-KEM (FIPS 203), e.g. X25519MLKEM768 in TLS 1.3 or mlkem768x25519-sha256 in SSH or a hybrid scheme in use. |

## 11. Tools used

- blockchain 1.0.0
- certificates 1.2.0
- chain_map 1.0.0
- configs 1.1.0
- dependencies 1.3.0
- inventory_document 1.1.0
- solidity 1.3.0
- source_code 1.4.0
- tls_code 1.1.0
- tls_live 1.0.0
- qsi-engine 1.3.0
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
17. M. Ekerå, J. Gärtner — A high-level comparison of state-of-the-art quantum algorithms for breaking asymmetric cryptography (arXiv:2405.14381) — arXiv. <https://arxiv.org/abs/2405.14381> (preprint (2024-05-23): Regev-style algorithms show no overall advantage yet for cryptographic RSA and finite-field sizes)
18. M. Mosca — Cybersecurity in an Era with Quantum Computers: Will We Be Ready? (IEEE Security & Privacy, 2018) — IEEE. <https://doi.org/10.1109/MSP.2018.3761723> (peer-reviewed article; source of the x + y > z migration inequality)
19. M. Roetteler, M. Naehrig, K. Svore, K. Lauter — Quantum resource estimates for computing elliptic curve discrete logarithms (ASIACRYPT 2017) — IACR / arXiv. <https://arxiv.org/abs/1706.06752> (peer-reviewed article: at most 9n + 2⌈log2 n⌉ + 10 qubits and 448 n^3 log2 n + 4090 n^3 Toffoli gates)
20. NIST IR 8547 — Transition to Post-Quantum Cryptography Standards — NIST. <https://csrc.nist.gov/pubs/ir/8547/final> (final (2026-10-27; the initial public draft of November 2024 is obsoleted). Tables 2 and 4: ECDSA, EdDSA and RSA signatures, finite-field and elliptic-curve DH and MQV, and RSA key establishment are deprecated after 2030 and disallowed after 2035 at every key size — the draft deprecated only the 112-bit level. A composite (hybrid) key establishment stays FIPS 140-validatable while one input comes from an approved scheme. Repeats the federal deadlines of OMB M-26-15: post-quantum key establishment by 2030-12-31 and signatures by 2031-12-31 for high value assets and high impact systems)
21. NIST — Post-Quantum Cryptography Standardization: Evaluation Criteria, Security (Call for Proposals, Section 4.A.5) — NIST. <https://csrc.nist.gov/Projects/Post-Quantum-Cryptography/Post-Quantum-Cryptography-Standardization/Evaluation-Criteria/Security-(Evaluation-Criteria)> (security categories: AES-128 key search 2^170/MAXDEPTH quantum gates, AES-192 2^233/MAXDEPTH, AES-256 2^298/MAXDEPTH; MAXDEPTH 2^40–2^96)
22. P. W. Shor — Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer (SIAM J. Comput., 1997) — SIAM. <https://doi.org/10.1137/S0097539795293172> (peer-reviewed article)
23. R. Babbush et al. — Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations (arXiv:2603.28846) — arXiv. <https://arxiv.org/abs/2603.28846> (preprint (2026-03-30, v2 2026-04-15): 256-bit ECDLP with < 1200 logical qubits and < 90 M Toffoli gates (or < 1450 and < 70 M); < 500,000 physical qubits at 10^-3 error, minutes)
24. S. Jaques, M. Naehrig, M. Roetteler, F. Virdia — Implementing Grover oracles for quantum key search on AES and LowMC (EUROCRYPT 2020; arXiv:1910.01700) — Springer / arXiv. <https://arxiv.org/abs/1910.01700> (peer-reviewed article: lower cost estimates for the AES key searches that define the NIST categories)

## Appendices: Cryptographic inventory

By origin: dependency manifests 5 (5 Shor-breakable) · own code 72 (37 Shor-breakable).

| Algorithm | Parameter | Library | Quantum status | Classical status | Count | Locations | Examples |
|---|---|---|---|---|---|---|---|
| HMAC |  |  | reduced margin (Grover), approved | acceptable | 1 | 1 | ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESEncryptionEngine.java:73 |
| bcrypt |  |  | reduced margin (Grover), approved | acceptable | 1 | 1 | app/src/main/java/org/hyperledger/besu/cli/subcommands/PasswordSubCommand.java:95 |
| Keccak-256 | Keccak-256 |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 29 | 29 | crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/Hash.java:94; datatypes/src/main/java/org/hyperledger/besu/datatypes/Address.java:158; datatypes/src/main/java/org/hyperledger/besu/datatypes/Hash.java:80 |
| SHA-2 |  |  | Grover: acceptable to NIST, below ECCG/ANSSI guidance | acceptable | 3 | 3 | crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java:118; ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetBlobsValidator.java:247; ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESEncryptionEngine.java:71 |
| CTR mode |  |  | n/a | acceptable | 1 | 1 | ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESEncryptionEngine.java:75 |
| BLS12-381 |  |  | vulnerable (Shor) | acceptable | 11 | 11 | datatypes/src/main/java/org/hyperledger/besu/datatypes/Address.java:71; evm/src/main/java/org/hyperledger/besu/evm/gascalculator/OsakaGasCalculator.java:17; evm/src/main/java/org/hyperledger/besu/evm/gascalculator/PragueGasCalculator.java:17 |
| BN254 (alt_bn128) |  |  | vulnerable (Shor) | acceptable | 1 | 1 | app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java:66 |
| ECDH |  |  | vulnerable (Shor) | acceptable | 5 | 5 | crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/AbstractSECP256.java:171; crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java:93; crypto/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/securitymodule/SecurityModule.java:75 |
| ECDSA | P-256 |  | vulnerable (Shor) | acceptable | 10 | 10 | app/src/main/java/org/hyperledger/besu/cli/BesuCommand.java:1546; app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java:54; app/src/main/java/org/hyperledger/besu/cli/options/NativeLibraryOptions.java:63 |
| ECDSA | secp256k1 |  | vulnerable (Shor) | acceptable | 10 | 10 | app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java:45; app/src/main/java/org/hyperledger/besu/cli/options/P2PDiscoveryOptions.java:91; crypto/algorithms/build.gradle:55 |
| ECDSA |  |  | vulnerable (Shor) | acceptable | 3 | 3 | crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/AbstractSECP256.java:376; crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java:22; evm/src/main/java/org/hyperledger/besu/evm/precompile/ECRECPrecompiledContract.java:142 |
| RSA |  |  | vulnerable (Shor) | acceptable | 1 | 1 | ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/JWTAuthOptionsFactory.java:107 |
| RSA | 2048-bit |  | vulnerable (Shor) | acceptable | 1 | 1 | ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/JWTAuthOptionsFactory.java:107 |

_Long lists are grouped here; the full per-file list is in the JSON report, signed with the same key._

## Appendices: Input files

| File | Size | SHA-256 | Redactions |
|---|---|---|---|
| .github/scripts/verifyArtifacts.py | 2581 | `991ab7c0b255d2849380885973e8aee25959e5ae50298b19c41743c14a6d5b62` | 0 |
| app/build.gradle | 5158 | `c5f2dc3147409128bab11d0cce1fbe7f353b732476909ba03a5dd484cdd8d3e9` | 0 |
| app/src/main/java/org/hyperledger/besu/Besu.java | 3815 | `ceb2182dfa300285abf753249101b60c2b09b0596547bc2b9fef58a47d60f98a` | 0 |
| app/src/main/java/org/hyperledger/besu/Runner.java | 21960 | `04b1d9fc274e65297309483dbc3ba0ec7f9b7cc055fad35530261bbbefd94f3d` | 0 |
| app/src/main/java/org/hyperledger/besu/RunnerBuilder.java | 62708 | `98b93e67e7b847d66a0a938862c8bb945a095ae215ad2e3293b77468862e7f02` | 0 |
| app/src/main/java/org/hyperledger/besu/chainexport/Era1Accumulator.java | 2179 | `ffefb0f15f48bf648ac7aeee98fadfc6a58a0a1d099a97ebeceececafac65a7d` | 0 |
| app/src/main/java/org/hyperledger/besu/chainexport/Era1AccumulatorFactory.java | 1110 | `6121117902c19c0e99e093c9a536c386a1a65bccedab9fd4e091e45c27eb308c` | 0 |
| app/src/main/java/org/hyperledger/besu/chainexport/Era1BlockExporter.java | 8154 | `0412bed2817c151032055f77f2ef69fe6f3d8f357d3044dc3f5c9d46f30d192e` | 0 |
| app/src/main/java/org/hyperledger/besu/chainexport/Era1BlockIndexConverter.java | 2042 | `de762eb94cf04e2b57321dd6d2216cf7b90518035d052210c140119b090c6749` | 0 |
| app/src/main/java/org/hyperledger/besu/chainexport/Era1FileWriter.java | 3524 | `d1c09c758a19b5663ac334ef8f23ab88e62fe8991d66fbd51778f7b259b4c706` | 0 |
| app/src/main/java/org/hyperledger/besu/chainexport/Era1FileWriterFactory.java | 2011 | `15685d8d61bc37bd98af444a4768a63d68b3917644500d965201851ed33651cd` | 0 |
| app/src/main/java/org/hyperledger/besu/chainexport/RlpBlockExporter.java | 5461 | `1d3f96e2724e84fa77d18ced970f488561c2882a5ecfc07802157f1796f4e402` | 0 |
| app/src/main/java/org/hyperledger/besu/chainimport/BlockHeadersCachePreload.java | 6288 | `f1c84b0186e9c01d5df7ca2e69a0ebdcc120d44264ae4dbdf67054f1d7b20a76` | 0 |
| app/src/main/java/org/hyperledger/besu/chainimport/Era1BlockImporter.java | 7667 | `8e9a38e67505860d328e193fd447ebd89e726370530fe29d95b69b60a2756c14` | 0 |
| app/src/main/java/org/hyperledger/besu/chainimport/JsonBlockImporter.java | 9955 | `45a941383121bcf02bb3bbee5968a9d49752ca46a22426f1b6a5392cb87da26c` | 0 |
| app/src/main/java/org/hyperledger/besu/chainimport/RlpBlockImporter.java | 12200 | `5a4ba8d887f996d40f6877463f7fac608e0218f4aab614faf27165c38e6efcfc` | 0 |
| app/src/main/java/org/hyperledger/besu/chainimport/internal/BlockData.java | 4335 | `fcbd4b7a95414f0a295064b93c50bcabc5760e39330ed2b08554198ec435d3ba` | 0 |
| app/src/main/java/org/hyperledger/besu/chainimport/internal/ChainData.java | 1317 | `d00735e4e0eb618c6ee3289efad546875e690e19509710b55596d147d03d0c13` | 0 |
| app/src/main/java/org/hyperledger/besu/chainimport/internal/TransactionData.java | 3544 | `8d3754da16e461ff6a89256c1a27a0780015cf5c896ff1fcd0ceef3cb0f541ae` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/BesuCommand.java | 140609 | `06425939e14955a5123dbb4a4a367107c020f2182f5d0c33d495489a5d59dc36` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/ConfigurationOverviewBuilder.java | 23058 | `f9d62713ba1f8b28e3b5f044eb985773262329af194fb77252daa14d04f9910d` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/DefaultCommandValues.java | 6748 | `3d93c62073eb982e089d36aebd32c7e8f6333a9a7e1e9ce2a5a38b4ad43418e0` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/NetworkDeprecationMessage.java | 2695 | `726fbf9eb6542775170da3ed8da1b13a372ce2d8007056f4a30d7176275ea4b1` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/UnstableOptionsSubCommand.java | 3292 | `6c6cd3476b1ada93b78ae6f8a1981f29b6a5f3148a3c26f47f52c5c7bbd887c1` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/config/EthNetworkConfig.java | 6486 | `42810e17347646ba738d431a6cf78a0688ffa84610527232b4130efc1621f989` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/config/InternalProfileName.java | 2784 | `9d9066524dc45f4195a337f49c0b87901e30b2de7d4af5fc195a97798596e23b` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/config/NativeRequirement.java | 4300 | `c2c2157be2729a5d3a8c05294677dd19f4cac047c3637aea477fc3e49bfe1ecf` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/config/ProfilesCompletionCandidates.java | 1391 | `17100cbb1ef73192e3150416a3241ec613df32648d9c62fa0db1564ff8b86b42` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/CheckpointConverter.java | 2095 | `8b3ae1576fb2b075d91c0d1876f4037a3290131cfeb672d4bb77d14a76125009` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/DurationMillisConverter.java | 1600 | `5bda3d6a967fa02c2e67c4bb96662c7238250aa0035196f6fbe97f6610b9c7da` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/DurationSecondsConverter.java | 1588 | `1db5432790701f8384a9a04b9c5df5b1b1174bdacd769abeb8fb48ab1a4582b8` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/FractionConverter.java | 1310 | `bf5134a9b55416c74b4ba7972fad36be2fba4ab55a113fa439d1b756d3dd35f1` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/PercentageConverter.java | 1307 | `e4a50646a32235baa32df75e768503de1cc3d98680c1eea7514926c6df126426` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/PluginInfoConverter.java | 1978 | `6d90e17adea50c5133f9ed164d04fff50ed1370fec01a18e564bbc1f80e3941c` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/PositiveNumberConverter.java | 1355 | `e8d0c533184b99f0fcd5a496151256618a2982235b124fca3c49d7288aa25035` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/SubnetCidrConverter.java | 1668 | `b23448feddba2b248318f2c432a094e210fe6ab6662ecc7dde92ccb3c860d75d` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/TypeFormatter.java | 1091 | `bb620ba180fd0761550501b382aedfc7e8cd5a9bcf0ba6c5727d67241ca4796e` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/exception/DurationConversionException.java | 1332 | `600451bb55e9fe551e614920b945c424b48bff02aa6e7f1d79b4f1400ff22916` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/exception/FractionConversionException.java | 1097 | `664efb46636bf1d8ab0e107cd653f35ee3247a821025334b4a432b7b666e4de8` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/exception/PercentageConversionException.java | 1138 | `ec3f1de1ce3800eb143849596e0e2438ef04d8224f251f5a823c9bd7c89fb738` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/exception/PositiveNumberConversionException.java | 1158 | `fdb8cc73aef4b119b43aff074258dc9ca94efad3f84f96f89cfa865307584927` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/converter/exception/RpcApisConversionException.java | 1086 | `6c03dc98c805efdd2901a427058faa82fe8c44ab19d41eb6e3bf3d0e2258719e` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/custom/CorsAllowedOriginsProperty.java | 3107 | `627d8d77968bbc7e452f06f6eca1d3503f16f9f678895365334642189d4bb79f` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/custom/EnodeToURIPropertyConverter.java | 1551 | `15c10fa04a949b4cb96fb47cda03ab18bb9e2028710cf14ed3489d07e099735f` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/custom/JsonRPCAllowlistHostsProperty.java | 2847 | `f57869a417657ea0e810b0f5bff03b52434692d8eb505ceb1c88740e504bb194` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/custom/RpcAuthFileValidator.java | 4526 | `1607fca1aa9823571dfadc2cf2928e461760d51ca2512c9592ddb927ce7e0488` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/error/BesuExecutionExceptionHandler.java | 1482 | `bd254f82d0d7cc7fd909beb7b0c97a5a2ea2cd83c4351204ebdcfad5c98c4773` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/error/BesuParameterExceptionHandler.java | 2176 | `693b04dab48837de0649a280b746776868133fd7cd4028cd81ce551d91fcc023` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/logging/LoggingBootstrapConfigurator.java | 10979 | `13a9bcf14d9a3823ef45dc02b6331d7693b45d0a427382e778a80e70acd61c4a` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/ApiConfigurationOptions.java | 8713 | `0e317c9c126f440508406b98a6a838c8bd3a5f8cbeee69e9f228a8df0693b330` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/BalConfigurationOptions.java | 3415 | `5f817d0eaf3b194eca806b59ebe00d34a1ddf2b3cd8e365759006d1dfd85bfef` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/CLIOptions.java | 1217 | `e2b9e5f8d1fcc1d440f349de6c120280be1aa8b8c2c58bbdb503604f0a4484fe` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/ChainPruningOptions.java | 7251 | `b32c18f5d9767bacca6fa8d297c8d2611b4e2237c494d4cefce46d4aa704da6e` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/DnsOptions.java | 2854 | `e7253db960a951e60545dacb0304292284b444a9406da8f5c7c5d40afa9986b3` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/EngineRPCConfiguration.java | 1509 | `03de393ab3ae6eac344e797930f660f2a540fe680018b8cdf7dc2bda59fd5444` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/EngineRPCOptions.java | 3139 | `f56087bd2a3f8d03a97aca61c1b16bf18833620045d8e6efb2a05dc538a2fa5e` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/EthProtocolOptions.java | 7939 | `6ed3c70ac9cc2256032de616f07a895105e83e0e0c96178c6e4a452a2c3d8856` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/EthstatsOptions.java | 3860 | `a6e869d9e6a0aa18f21a9243d960f7a828b5d2252d51f1ba02cc7ca572c051ba` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/EvmOptions.java | 3255 | `e8e3e87b2d225e6acadd2a5795cce9826c59a8503109fe67c4f7a4c4b5c0cbb2` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/GraphQlOptions.java | 7159 | `b419bdcb204d1098d857cb3e51ca75a9131d9b6901924193483de6fcfd53f00c` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/InProcessRpcOptions.java | 2561 | `575015c4cfda47acf5a8a914e2f91e27559234a809d116bc38f553a8f17722dd` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/IpcOptions.java | 2631 | `03160ce3d3de8b1908aeb9e9e7288c6498eb6bac27394fd11562d73494c218b7` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/JsonRpcHttpOptions.java | 23855 | `9e32c11ae5b5ea02dff9db3aad3329d859784ffea4ecdb443c59d53defc09839` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/LoggingFormat.java | 1567 | `427bf53dc3bd06e0c320bb741e8d8d7352893693819f9fdf5c677fc1a1777ff2` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/LoggingLevelOption.java | 3192 | `4438c07694d3979103e9789cba804f16c7f7e46de0fbcd2afa33bec7059bf6e8` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/MetricsOptions.java | 11552 | `66d0c4426814525cba0b541a21d87b196b89c63819236c76fc7bdaed6537d5aa` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/MiningOptions.java | 15533 | `0c1e19b464965f91d9374bfd6ce3ce94446619c7badea830884f2d352c672bc1` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/NatOptions.java | 1473 | `e8ac422c73ed948a6771b1dc9cb085c2c1b5d9547b6793c1facd9ade6c04c3a8` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/NativeLibraryOptions.java | 4470 | `d2e5c67c149c5f81c166a2a887cbefe35eb37ce5756f52051b4e497c27c1b3bc` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/NetworkingOptions.java | 8470 | `cfc46d0812e500959907e2750984bf926949388c13495435053f4c20ad16afb1` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/NodePrivateKeyFileOption.java | 1625 | `9416da127171e0c1f5742809f32b5b3d2f20b34031d81db9b009752117877c97` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/OptionParser.java | 3932 | `802bd9a66264240c0a27b3b46baaaf7f3a1c7ef0d1d7a7e0c56037378b11e368` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/P2PDiscoveryOptions.java | 19052 | `db10c04e6667a8288b80a78fb7539a070f8f233a9ada0e14d63dc7af95b531a0` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/PermissionsOptions.java | 5860 | `23ae735b058f0fa5254378709e05e2cbd8fb5b415b20d938384fd945626fc8a6` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/PluginsConfigurationOptions.java | 5876 | `ad35f18fc35fb1eda453aa7a1614477e337efb48657929ae970c898c1a496040` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/RPCOptions.java | 3072 | `185a979ce37fb0df51c4d165fabb00e79d66920f16b27e14f986668d5716608f` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/RpcWebsocketOptions.java | 17959 | `903f95264e7cf89db1640611c5cb724199261f78451144e23b5fe3b57a1234a0` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/SynchronizerOptions.java | 34474 | `1c1d78eca7e7a342ab7f8054e6a1c5c2bfee168bd4511e6d9332ec0d7b21cef7` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/TransactionPoolOptions.java | 26143 | `21c5b41367e172912542ef96639b214b1014ef8a3a1a31d6a35fd49d9a18afc5` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/storage/DataStorageOptions.java | 5384 | `bc77300d62cddd9fe37954fe8f6df5769c00c58cf2a1ed08b63a8a695bf545da` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/storage/ExtraStorageOptions.java | 15851 | `ec29da32e13f4abbfb8be822e140166f2cb28a888d1dada817d780d5de56b222` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/unstable/QBFTOptions.java | 1529 | `3f9e14d6da2aa200cfb059383c4d2cdc53b8b6e10ad761ffb1670379a2b4d884` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/options/unstable/UnstableBftOptions.java | 1649 | `282eac2267123b978adbc724f80b6d2ef58e75ebd244131a3fc64959f4d7c33d` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/presynctasks/PreSynchronizationTask.java | 1168 | `75d5b3fc231846d41844c82fa94f2a1523db405b710d9e6d250950ebd1da7c22` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/presynctasks/PreSynchronizationTaskRunner.java | 1351 | `ea64297dac8e927e01e12f0110162a8025b203bac0e1e9b55115e562502de006` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/PasswordSubCommand.java | 3041 | `c7a56dc5c5db92993cdb4833c7b3854cbd3025e8738bf9077880c0d24109112c` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/PublicKeySubCommand.java | 8078 | `4515ae308f5bd27bbaa5acf867ba063e37deb48eacd844c97c5d6b6f665e9503` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/TxParseSubCommand.java | 4871 | `f6a7faa47455c6fb793a04b7482f5770c049c93aae18a179f88417693c7283eb` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/ValidateConfigSubCommand.java | 2860 | `3efef9b8f1453d31c3fa19b400e9891707f0787215e8503b3889285e0698ffc1` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/blocks/BlockExportFormat.java | 829 | `5a7c68c78b34b943065ca4a0767542640720810d370f45b620d7fe3189acca04` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/blocks/BlockImportFormat.java | 873 | `ecd53ad7cf0236dcda953bd7f8996771a260b4df2227270d355ba747f6b32cbb` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/blocks/BlocksSubCommand.java | 20086 | `c35ae9dc34ead1724d73f2fc274bd7df4da175d1ba8edb30df647e2d4c4e3879` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/operator/GenerateBlockchainConfig.java | 13129 | `9f3a63db90c26d48ef8fb62f0e8c79339407d046560724454487452de744e24e` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/operator/GenerateLogBloomCache.java | 3807 | `7fcbb311e411bf58d18e66f5509bd497547a5ef73684dca1e84207f92db059ea` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/operator/OperatorSubCommand.java | 2247 | `4a2686f756abc612dbb89b879a16ae060e766a4de11ba30ecc8d0d78ed1ad64a` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/rlp/IbftExtraDataCLIAdapter.java | 2224 | `cdbe0c400bde86a9fdd0fa90b2ba9cf8bab5b531a1a12ef272db1bca74d54a82` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/rlp/JSONToRLP.java | 1469 | `720904a464d8d534da47f2917b7aa1a34f326b5ca26f6bb1b7024a1d627fa0d1` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/rlp/QbftExtraDataCLIAdapter.java | 2191 | `ede7c4b4b01d5db722d76d7e1bce9776acd22a6008066cb2b76fc1a2387e2547` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/rlp/RLPSubCommand.java | 11667 | `81e5549402ed4b523805404d81063cba35d47c6da85232bb208321207c699885` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/rlp/RLPType.java | 1203 | `a561f08b0ee9453b573f9dab22569c8e521476b027d9e25c81f0b7720d3a2a7a` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/storage/PrunePreMergeBlockDataSubCommand.java | 6107 | `95a4886a56ef74d668e1280400c5f221e793c21a3f2f5983a90eee875efc07cc` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/storage/RevertCodeFormatSubCommand.java | 5019 | `0fcd9511faff7ccdb2b318e6e35e102c2b016a9f424ab01629474167d14522b2` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/storage/RevertMetadataSubCommand.java | 4799 | `0eec5ffcd8b3f5b7e60fe1eb5f9b108787b666961b7bff642eae515104a2520c` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/storage/RocksDbHelper.java | 16802 | `116bfe5e3360b48085d3c3037ecff6f4b6a1326f826b53ed3d65b5e5828a61a4` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/storage/RocksDbSubCommand.java | 5240 | `3defeb83b35c742784986970bd19a2a8cfa7742987c73adbcfb66fbf7a3d21d9` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/storage/SizeUnit.java | 1424 | `234eaba229859e382a77244512104dca29aee708b7d6ee72c8406ab963cffe05` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/storage/StorageSubCommand.java | 6582 | `14d108944da458d11b3c4df6c63db52126ce63393389eebee3c32f56c01bec54` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/storage/TrieLogHelper.java | 17016 | `f6012d87b21e091e7c3ab8b4a38885f93cc316da98e780487c7c194645c9f63a` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/subcommands/storage/TrieLogSubCommand.java | 12371 | `a9b2ca6eaa53d869ee54805c5d309c707c406d06e77383e3b8e2145d8477d9ff` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/util/AbstractConfigurationFinder.java | 4943 | `1f7030bc3ec17602beaa7e587c80f14bcf09460ad3cd884bf943151bff877740` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/util/BesuCommandCustomFactory.java | 1796 | `aa6c347ca93e3b3eb331df3e5bcc6ab24ebabfa55a605c7a7665f74427c44546` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/util/BootnodeResolver.java | 5296 | `591bf54bc5cc2fa1760ede15756bf2b7755662b2e2328130ceead4fc0ea18a97` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/util/CascadingDefaultProvider.java | 1688 | `6ad47ed63cd7fd0e47cf79897267b2f98b9f20d2c29007f4d7a799e08f6a343e` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/util/CommandLineUtils.java | 11949 | `8c58e87e4d13d233052cbf28d72c721fb0ebda3e67924e52bbcd8929ba64cbaa` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/util/ConfigDefaultValueProviderStrategy.java | 3273 | `32626df0dade33b53d0f805101b1b37c41a77f640af8e3e11f2247c50ce82821` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/util/ConfigFileFinder.java | 3624 | `9e20d300bbd477c84d8c855f079d56975c990c047d6883bf904e6c3ae441afad` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/util/EnvironmentVariableDefaultProvider.java | 2202 | `74f96c4d2bcc8c550b21b33dd90d40d12b4eba559a1e4ee6ce680ee36e606723` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/util/ProfileFinder.java | 5447 | `9f5225b690847a31d5b49036eb81322d20d44af8bf8716316c81e84d74f45ec4` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/util/TomlConfigurationDefaultProvider.java | 12279 | `92980148ffae221f2ddaefeb75c8184d8920c4b2918896da9a44007bf6b5a273` | 0 |
| app/src/main/java/org/hyperledger/besu/cli/util/VersionProvider.java | 1806 | `e89b82e3caa6ac6f4650fc810d06cf959828a2b1d099832054a771e79dea9e46` | 0 |
| app/src/main/java/org/hyperledger/besu/components/BesuCommandModule.java | 4063 | `c8f5774aeaf6156345b0bb48c44da5182e98fcd3d97ea3cf9a1965ff92d2196e` | 0 |
| app/src/main/java/org/hyperledger/besu/components/BesuComponent.java | 3025 | `1293f1d701e81e4167dfc00530a250f12aa4da6e3c895d868f9461e09a5d32c8` | 0 |
| app/src/main/java/org/hyperledger/besu/components/BesuPluginContextModule.java | 1147 | `ba7a51bb21ca32cbf5bb74ab526d5e680f9cca7e478435ebe65f46729d5eeaf1` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/BesuController.java | 16116 | `c92764374f86e623739eda094a7af25c94928ff008ee524fb49641010d9e4ef2` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/BesuControllerBuilder.java | 61425 | `a955ceb30b2e57e36ceb5af4da235f321a5486f685b59ff01b938e331ea9c2ee` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/BftQueryPluginServiceFactory.java | 2911 | `a54fee9a316bd475ce1e57801ec7c1ea00c6d90c29dbc025c7862841998b7755` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/CliqueBesuControllerBuilder.java | 4828 | `4485a59db30892e6b7fba4cbd513602004f21aa0029e2afacf0d0fb42e39b294` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/ConsensusScheduleBesuControllerBuilder.java | 19591 | `839039268e91b533f1269017c8d686e089080bdc50b3bae6e55fabf8e8c99020` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/IbftBesuControllerBuilder.java | 16091 | `02244e63e86d8a1ce783f87abd888cc105ddcc361e06783c098e71358a3d133e` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/IbftLegacyBesuControllerBuilder.java | 4439 | `a69d4b20f0b6a3677105139834e6a8bb666c7aecf986ae3cb9132096d327a67d` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/IbftQueryPluginServiceFactory.java | 2635 | `55db77f92500ce0558387c24e646f4a9d933835c5c502f81194edca9c2596209` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/MainnetBesuControllerBuilder.java | 2999 | `445e07dd50d8f19098eb67a59cc0b0b3ff992b41985d24b3996ea25ba7062b30` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/MergeBesuControllerBuilder.java | 11977 | `78c641ccbd6365e148dd396bf010ac5e36271ce4f21a898e1ec9b86b0cabf8c7` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/MiningConfigurationOverrides.java | 1163 | `66a88a2484ef74e2929ee15f657ddb62b61b5d4cd4e92869d39da9bc79d86e11` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/NoopPluginServiceFactory.java | 999 | `a771fe7645b1c9bc2d9d4ed29559e5dd06c695f2c7f6cff866557ce950527a47` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/PluginServiceFactory.java | 1025 | `aacb75a5dcec6fd5d89ac9f50861b13daa86bcee224582c92d22093d2c0c43d3` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/QbftBesuControllerBuilder.java | 25831 | `6006fd936879b2fe08bf566406a81fda426f5ec0287e87344ea1aaafadb9c0b4` | 0 |
| app/src/main/java/org/hyperledger/besu/controller/TransitionBesuControllerBuilder.java | 17560 | `bce56bec6bf018c2080eb25d506a69f2b205cd535a01cc43dd5a01a834563b1c` | 0 |
| app/src/main/java/org/hyperledger/besu/services/BesuConfigurationImpl.java | 5487 | `7e5bfe7c7dd5b225e436e53beea82ef9d04030fb02d25df0b7856ec68b067544` | 0 |
| app/src/main/java/org/hyperledger/besu/services/BesuEventsImpl.java | 8561 | `60014abda8cb8ab6593fce6de6c29526c70f70bf59d9a4fd5b2d51cddb275fe0` | 0 |
| app/src/main/java/org/hyperledger/besu/services/BesuPluginContextImpl.java | 16839 | `12d04e8bfef24f76a1556803e2d6b41390c92964afd188b7e7c7b11dbcb0e8be` | 0 |
| app/src/main/java/org/hyperledger/besu/services/BesuPluginServiceRegistrar.java | 12134 | `c585bf59760839167ff7c6863cc0ae03627d6e5a88ae7269b7c101a4a0fb9a4e` | 0 |
| app/src/main/java/org/hyperledger/besu/services/P2PServiceImpl.java | 5464 | `8d4f3f7036cf839259a6637f0503c9f97aba1e72f93e3c3f551856576f80fa3c` | 0 |
| app/src/main/java/org/hyperledger/besu/services/PicoCLIOptionsImpl.java | 2277 | `0ea727eed2b892d7266041fe2e6609745d443c722c07feddc6fbdecf0676d5c1` | 0 |
| app/src/main/java/org/hyperledger/besu/services/PluginVerifier.java | 19938 | `afc966664646837968019f5133d2768c0a5a54027add6ac04a941170066e8016` | 0 |
| app/src/main/java/org/hyperledger/besu/services/StorageServiceImpl.java | 1907 | `24d4b888ddef5a766d62e54fdbca5e03e5dbb15d031d4193cdb4773a1ea4d714` | 0 |
| app/src/main/java/org/hyperledger/besu/services/SynchronizationServiceImpl.java | 9107 | `282b8d96b6bc1a262f2a6c0102a116c27cb4111d4513cab09049bd1786616b6b` | 0 |
| app/src/main/java/org/hyperledger/besu/util/EphemeryGenesisUpdater.java | 3245 | `702ee2998259ac7edf88cb83aa8850cf1989a7f5279170dcda2925d29e35dbeb` | 0 |
| app/src/main/java/org/hyperledger/besu/util/PermissioningConfigurationValidator.java | 2537 | `e259ef52e2c90e8a8845551f854b032692cefe01c08b24802181cb9e1dbb5ad6` | 0 |
| app/src/main/java/org/hyperledger/besu/util/StringUtils.java | 1620 | `36a0b3749e6f827f37868cf3b9fc67fb66c55c8e525794e66b7c4d448b70c2f1` | 0 |
| build.gradle | 67638 | `100ae6ce07e14170894cb522a21cff5f8763211bdfbb275d03d8eaab87168f5e` | 0 |
| config/build.gradle | 2215 | `e692f9c385c1814c5cd23a6b627d1b00defa731d42de8a74bf0eacdbca58d82f` | 0 |
| config/src/main/java/org/hyperledger/besu/config/BftConfigOptions.java | 2780 | `26b89844e885a777a73306f79f20fcbd8e3ea7d6a94cd9c03ce66a0b44c8ff3d` | 0 |
| config/src/main/java/org/hyperledger/besu/config/BftFork.java | 5912 | `07da82ba322af1e2243936d281deb1af19a51d433b60b98170936d74c7851687` | 0 |
| config/src/main/java/org/hyperledger/besu/config/BlobSchedule.java | 3945 | `e8e56528871d2532c1527dc1bc3733f7fc028e02669ab1178633eca375356a53` | 0 |
| config/src/main/java/org/hyperledger/besu/config/BlobScheduleOptions.java | 4238 | `c65abbbd5d6cce2d159b8bcc70b8ac4e563b8af47f39053b3faa4442aa7cdf8f` | 0 |
| config/src/main/java/org/hyperledger/besu/config/CheckpointConfigOptions.java | 2875 | `5172e226fd4ff72ed6aa2ba8c30d6cbbb7e76dd8aea4e872e832e3c237203132` | 0 |
| config/src/main/java/org/hyperledger/besu/config/CliqueConfigOptions.java | 1327 | `15361d156ee22c60f8b8194fb582c65ad94bb4697cf7108bbd2e6f4e7728daa8` | 0 |
| config/src/main/java/org/hyperledger/besu/config/CliqueFork.java | 2330 | `40c89048b44b30d7d36797e9b5901662502763b3c3a2873f60d82e9fa5de52ce` | 0 |
| config/src/main/java/org/hyperledger/besu/config/DiscoveryOptions.java | 2458 | `acde5a2e711e87b99ef7af472c79a2e91d25291a7f172504824252db8e1791d9` | 0 |
| config/src/main/java/org/hyperledger/besu/config/FixedDifficultyConfigOptions.java | 1816 | `bcb6fdc6b0e7d467bc81cc081c34fc440d1e86e4d98286815559600657c3861a` | 0 |
| config/src/main/java/org/hyperledger/besu/config/Fork.java | 925 | `9208cff602b9fe43878f0c405351a37d08693821b5025fc045f15ac34ed76bce` | 0 |
| config/src/main/java/org/hyperledger/besu/config/GenesisAccount.java | 1476 | `f9daa660c84bc7946f7320032adc86c786c1a592c268134b099ee53916051749` | 0 |
| config/src/main/java/org/hyperledger/besu/config/GenesisConfig.java | 9749 | `ea999e57b68ed679fc30f050df91ee5e735bb39e3e41e4dacf79936a932f257f` | 0 |
| config/src/main/java/org/hyperledger/besu/config/GenesisConfigOptions.java | 9843 | `a650bf7312dbaa6130ebf563a7a9aa583e94d977f5048d7acb175128943fc511` | 0 |
| config/src/main/java/org/hyperledger/besu/config/GenesisReader.java | 8164 | `93a8fd6b6d4b8f731a4e9f5652fcc31bd821379314bb30143cc0822a9d3260c6` | 0 |
| config/src/main/java/org/hyperledger/besu/config/IbftLegacyConfigOptions.java | 2055 | `4a1a10962b6ae7fe680ad78e9509ef3951804d4e4074db3b35d34c5c53ae4dd5` | 0 |
| config/src/main/java/org/hyperledger/besu/config/JsonBftConfigOptions.java | 6830 | `137d0a3626be04dfbe043f017e0f019b3ed5240dc45424354f7914f553b6c5b6` | 0 |
| config/src/main/java/org/hyperledger/besu/config/JsonCliqueConfigOptions.java | 2593 | `aff31fc1a51e4e682bc9145e37aa99c98dbdb9be67bd1343e95f23b734f7acb9` | 0 |
| config/src/main/java/org/hyperledger/besu/config/JsonGenesisConfigOptions.java | 22189 | `3e90ec61cc33e2dff622521e500d26796a0c0e04a8cbe68fd401d83686062d8f` | 0 |
| config/src/main/java/org/hyperledger/besu/config/JsonQbftConfigOptions.java | 2326 | `aad18df8173e72e18b38139b6df69bdb7328615fea9eb24d816f30d631a6c28b` | 0 |
| config/src/main/java/org/hyperledger/besu/config/JsonUtil.java | 21670 | `f729e9c7b6d63b6ab5b381554283ee716eb92a6be63ec8d537e6c617abf9f9e2` | 0 |
| config/src/main/java/org/hyperledger/besu/config/MergeConfiguration.java | 1297 | `2b36d6c176c09c38a753d106a7650c9beaa488b002a353504b6a401c00204cc4` | 0 |
| config/src/main/java/org/hyperledger/besu/config/NetworkDefinition.java | 7745 | `007498ab7b583e95313f5866c74986cc15a8146a4b091ab0f5289ffbdf017b58` | 0 |
| config/src/main/java/org/hyperledger/besu/config/QbftConfigOptions.java | 1294 | `0d4eccdfe4df72ae4a231117b8d12b54a93e0cc6cb04e86babf104e474acba79` | 0 |
| config/src/main/java/org/hyperledger/besu/config/QbftFork.java | 2288 | `b5e783bb720174ca0eb79113f1e268ed5f8aff88c882c39116ce5dd6ef6ef5f5` | 0 |
| config/src/main/java/org/hyperledger/besu/config/StubGenesisConfigOptions.java | 25105 | `4d0a5514ae1d137ea71b2887774bf3289d16db0acc74a9518d9bfb6c5b096ebb` | 0 |
| config/src/main/java/org/hyperledger/besu/config/TransitionsConfigOptions.java | 2778 | `af23135151a56a6483a3616c0c5c1d299db9019f5817abc973cd6fb3f5bf8c5f` | 0 |
| consensus/build.gradle | 646 | `aa191ff708e7b1f228615c5b5cb16cc678f78950515a188dfc87a693e9676ca5` | 0 |
| consensus/clique/build.gradle | 2831 | `2d2d94bb2f617e5dd85b5dc849f41e46b6d6dcb0e3bbd4bb1127f2eaa4a1e265` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/BlockHeaderValidationRulesetFactory.java | 6413 | `f278b0d4067f85724cedd16d2d03091b62efa42be8788e361c87f5dcdb504bbe` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/CliqueBlockHashing.java | 4654 | `f89675db816234079737f24aa71e378f4281f27d980b913e6adc5bb973c1a6c1` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/CliqueBlockHeaderFunctions.java | 1508 | `00be5502736bededbf1626f60f317f384bff0ffc0739d6781e06f2773e00ef41` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/CliqueBlockInterface.java | 4246 | `4f7c0a1ba1356dd8fc1a27b1ef7c20e08db5edab9dad87c30f658ab6ee8b3b00` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/CliqueContext.java | 2315 | `c4bd5df6af0b1538ee06f5caf28f37c6c43a1470f7a4b7d04d97c63274c5e4ee` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/CliqueDifficultyCalculator.java | 1659 | `e752e2ff0221f93e67fb70da8492a8562fb5c91d3d16b595578a93a8bda04185` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/CliqueExtraData.java | 7303 | `3b97303bb7026ffb12412e7dd0db9d0d1aa283a99a4879541abc8be9d19d083f` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/CliqueForksSchedulesFactory.java | 2099 | `02407cb0f59ac370d4087f570a1adead32052194fd9d215649d0907f658043c1` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/CliqueHelpers.java | 6836 | `c258239ee3ddd51344de40ebd0ba708e0dd5be56e72424489b26f4be512ad64c` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/CliqueProposerSelector.java | 2261 | `1a2164236c41964bae4e442faa9ca6b8ab7b71601822a68962d9605d6f4e53c5` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/CliqueProtocolSchedule.java | 6963 | `dfb32552b3a1206a867ab2276cd70f7bb38e4a26ca321d81fd7704ba9977fb5b` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/headervalidationrules/CliqueDifficultyValidationRule.java | 2397 | `212d17b80e130818ffb063e34c48a391e7eaf8271a145a7128dfc6f402525602` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/headervalidationrules/CliqueExtraDataValidationRule.java | 4284 | `b4442e6490aa3dd0c330c729c7d1ac7b7f1aaa55769c6451ab0e7d0707ba6c72` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/headervalidationrules/CliqueNoEmptyBlockValidationRule.java | 2139 | `869a06b1dba59dff10c2a7ee06aa8fc68efba86a9c8dd9e5b306b25b6eed7ff1` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/headervalidationrules/CoinbaseHeaderValidationRule.java | 2166 | `583cf0fc16917da5d73200385662ef3d6f47377896ae44ca185d586b4ebf7586` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/headervalidationrules/SignerRateLimitValidationRule.java | 1986 | `545beaf608b2de0f32dc0735a9fd4a997c8bda60348d3c0dce1e989cfe883ca8` | 0 |
| consensus/clique/src/main/java/org/hyperledger/besu/consensus/clique/headervalidationrules/VoteValidationRule.java | 1930 | `ef2c17448ea6e9973dc3c1d4bf2073c0956bcfa4dbeec99a52b634d4b5363461` | 0 |
| consensus/common/build.gradle | 2856 | `4a0715092d13ab802039703866c1894646660efe3c1845a1c92e51dd5c45fabe` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/BftValidatorOverrides.java | 1492 | `f0819dac2d60db4df213789ca82d71084cc602a42cd2990557e6838e805267d2` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/BlockInterface.java | 1746 | `87e9e6fdaaa5a823e5afe1aeb35581f222465a19e148c9e2f0e8ac55cdc41755` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/CombinedProtocolScheduleFactory.java | 3741 | `13dc3f067979916cf9c527a7c4181575e4f995f3d1f49273b7c187bc02383df0` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/ConsensusHelpers.java | 1249 | `225d3b4ccd12110ec8c3213ea02d5e8a0d34e0242305b898c8734e2d6028d28e` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/EpochManager.java | 2210 | `325c52192f5cd9e19a705d9d8defa8cc40117eed8f328e87f35079e8a4068f88` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/ForksSchedule.java | 2693 | `0610d713601b3b2d9d478a8023ff954baa3a6e15c53c38b9ce053928a1450cc9` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/ForksScheduleFactory.java | 2660 | `f125fbf4c8e96b1d7a912d190242bc334a1f6aa58496d0e1ed7e216e66d85e04` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/MigratingConsensusContext.java | 1544 | `d4e5f43072a1b7e66a307c79f775b50c4df72e7ca5f3a3f36e4e72bfa7c67d09` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/MigratingMiningCoordinator.java | 5723 | `25decced9d0490804f139bb33c568a420ce530d03e8db1faaeb7493790416832` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/MigratingProtocolContext.java | 2770 | `527a26237ca3efbad1f97cba63ff62822a9b7ee3f7d65f84af3cef84eec6664a` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/PoaContext.java | 931 | `410a4fba9d9a83c4e36637a84086f0efcbbc0c14927321b3c05554cc21f27e3c` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/PoaQueryServiceImpl.java | 2227 | `24280fe12c8d127e75f707ea439c1d645c09ab57b86e7bb0eb75643863838ef8` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BaseBftProtocolScheduleBuilder.java | 8596 | `6b681322a212c7dcc99e6e7cfb17468946fb2080dbe0db64f2784445d55fdd12` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BftBlockHashing.java | 5243 | `879edc67a44155d3c9e1ea86a25332ef9a524ecf3f9fb839c68b27e1dfae50b6` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BftBlockHeaderFunctions.java | 2768 | `6c9dd984fcab98d0744acf571c24cd9c4cdbe1dfad1f0a1e731e4d9f1be526b6` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BftBlockInterface.java | 4655 | `29d0207166dfd61c3e943ce31d365abbe8f1757ad465383af7ef63f1fc9315ba` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BftContext.java | 2169 | `9a81084c847a9d1f12bf3a445266fc57a38c5c5830234da1a805c839be31ea0d` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BftEventQueue.java | 3521 | `8ac677c8f5ee248fdbc3d20687e1e347eb7c8a98b4d5c87b38b854c2656d76df` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BftExecutors.java | 5656 | `1965c3d46a864c6354a5964cc65a5d7c22dd4f9e47e358e51b77cefc0b778549` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BftExtraData.java | 2823 | `1206c08ad6a32173cffdc98739bc38b25ac02def98a1fda91881ad7e22b0e568` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BftExtraDataCodec.java | 3166 | `4c63dfd6fe679cd79ce6445d8955a345d5249cd371247d01b417fc969ae79517` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BftHelpers.java | 3895 | `0f7c68629761b544637053e99c270ec9e8c092a1461f6b8805977e9d7decbdd5` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BftProcessor.java | 4994 | `1f0bd5db87172ef26532d976c228c2059119b94ac5eb97cafb36f5c5c9cd6a15` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BftProtocolSchedule.java | 4376 | `e5990903128ad65ce098f8683cd9c5655e2f13aecf423f1461c795a220f4d536` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BftRoundExpiryTimeCalculator.java | 1845 | `c3c1eed7b61fdd260c7a3915669cdd87bb2162112546c1cd1e63bf9658794a67` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/BlockTimer.java | 9298 | `19a6be851338762efa4bb412999234ca43f577f2d61ff5d4ec4ef9fdd87d0b3a` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/ConsensusRoundIdentifier.java | 3446 | `8052c91ba4499eb9b1a43b32f7cadbf319ea00271ff07c2c76664dcc74cc7064` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/EthSynchronizerUpdater.java | 1732 | `cf9f9ca822076d526a6469d45f7121920c1cd2166110beb90c85fb735bc5fa2a` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/EventMultiplexer.java | 2710 | `331c012992054bc9a1bd78f1815539f028f43982dd3e7b8e16df24953e4a4998` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/Gossiper.java | 886 | `86e30cec5e84f853714cf1607f6b9afb5a598266cef2d63685d0d3e5064c7ef3` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/MessageTracker.java | 2053 | `8825cec34c04c4a8bbf824969dc9a46688bf32011b447c83c34970132e946634` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/MutableBftConfigOptions.java | 7340 | `b66c6e16b80f21739f6542d90fe6b610a3319cc7fa9924849bc12623a613f1df` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/RoundExpiryTimeCalculator.java | 1070 | `d66a7556cf9cea8e3c704705c853ce052261708b76ccb84592702d026409ac99` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/RoundTimer.java | 3326 | `26c057a24086c6b7a723fb26bfb4d7a2d6d604d42749bbe0d0ad9f17cb470e5a` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/SizeLimitedMap.java | 1414 | `2d9977e7a1e55c1c951c1822addfd2632fccc554dafd6ce80797e697636fa130` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/SynchronizerUpdater.java | 1062 | `6544bdd77c296a223b63f0b1b4fbf993f184bf959d6e61e0af90ad8bf24dea2f` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/TransactionGasLimitOverrideGasLimitCalculator.java | 2510 | `7004d5d2d6018919ef2bcb1e772e1df15fa662f409f3fb98e03e3c1ef29975dc` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/UniqueMessageMulticaster.java | 2448 | `e4066ffaa02f595af1ec03cce5e486def89d09cbc72418f001b4c70c124262d7` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/Vote.java | 2624 | `1962b3aae964cc8bd4a85a0ad6283b6bf730ce7083fb58788b63f9eb7ef3a46d` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/blockcreation/BftBlockCreator.java | 7795 | `2605632d1dfdd3a810dfaf0f8a86914ff8d2ec0577cac2995c52e5cd47ce27df` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/blockcreation/BftBlockCreatorFactory.java | 7399 | `ab4555aee1afd42c22b8cfd6ff70eda0b77eafe574815fdc4abb59426ccfd31d` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/blockcreation/BftMiningCoordinator.java | 11238 | `1504fd4aba12e9c4635362dfb42619f29567b1881839de82f6a84d88bfa4a619` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/blockcreation/BftProposerSelector.java | 7684 | `62ddb89b20fc5fde9dca3947525df17b4f7fe7fdffcef644c03d3f0d4889e610` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/blockcreation/ProposerSelector.java | 1358 | `53fff0bcd1268f26cc153f989fd59cc59c489fa9aaf811bea46ae02d225fac3e` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/events/BftEvent.java | 890 | `7c108436c03eda694c3cd4f988ce7ba0ffbce2075f6fc3f9d04ba36ebe327cc7` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/events/BftEvents.java | 1381 | `9810811e6eff8dd4847042881a66ecfb72c7ccb503c28fd753e396fabe814db3` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/events/BftReceivedMessageEvent.java | 1273 | `35ec9d69b4c30822ae5b4befaace076254c54a8ec13ec50f94b049a3b59c5992` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/events/BlockTimerExpiry.java | 2066 | `f2e987008dcf50e5dbaba325adfaa8118b37e93a5bf809ddfa8095d01f958444` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/events/NewChainHead.java | 2048 | `2e262d449bfbe884a301213df7dc54009f58d5a35cd99b88f18c06b193e886c9` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/events/RoundExpiry.java | 1879 | `24186153919eaca5d9266d70639dfae4aea98dd2c170510ffec2d41827131f8c` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/headervalidationrules/BftBaseFeeFitsLongValidationRule.java | 2187 | `241012dd78208e9b9ca534bb2fe16d521cdc9a20cfa0af28e0006aa9f52233f5` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/headervalidationrules/BftCoinbaseValidationRule.java | 2198 | `d4dc75b258c27d4d41e78a4c573d1a933d12d9963595892183dd0c4dda39ecbb` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/headervalidationrules/BftCommitSealsValidationRule.java | 5257 | `75fd2a4e0308c22617fa911252c5f65de43135e8366a558b3bd9dda778685ec0` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/headervalidationrules/BftValidatorsValidationRule.java | 3373 | `6d8cefe41f3d93c4dfc05e2b3050ed8ed29e2741df201996fec5dc3a788ce2da` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/headervalidationrules/BftVanityDataValidationRule.java | 2076 | `cb26bbfd5c25a0e9e7e060d5eb49416a8c04c211af98502ffa7bc0a8cb6c26d1` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/messagedata/AbstractBftMessageData.java | 2176 | `61da1d8ff76674a0c866b8809e8595c57755c9332b3bf00465a1e98e3723cd0d` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/messagewrappers/BftMessage.java | 3989 | `e2ac61477c0376d1e548bbb9b035c24ed4a808c66fa0fa20c7b013433060b799` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/network/PeerConnectionTracker.java | 1105 | `fe0352c465fe3fbe0877e9128b0824a3f9ac9cf80e25fa39d377d0282266782d` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/network/ValidatorMulticaster.java | 1181 | `7c0df363308d5d4f85a612145ad77ac9c524af56bd40c22c714a5df2d817fadf` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/network/ValidatorPeers.java | 4418 | `adb8c5f94b34c4e66a0c62126a58433dedd28e0bd0705baffa61d4615e935ea8` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/payload/Authored.java | 873 | `a10be5afe2b3d5eb47fec798b67b603df4f6fd4b86e2c8d5f56e1b2030f5d986` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/payload/Payload.java | 1726 | `28ce4d14bab27be2adc269485d1b1887a127c2b365b06567f7c14992a75931c7` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/payload/RoundSpecific.java | 958 | `80f1f7f690c7ba33027125278db43636d63f0f7fc5ee071c526c601787073a26` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/payload/SignedData.java | 4343 | `b67e888ee69bad986511ed26924a5b3afa8446c0d31cf161db5dec1b720533e2` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/protocol/BftProtocolManager.java | 4518 | `2bdff6fed7b722dc3d4916149800704691c2b9756f25e777dcbeac31bb3e25d4` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/queries/BftQueryServiceImpl.java | 3594 | `8c1f50d5538ca719852d961e9b242661edc228362a54462dfc76d80f31a0389b` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/statemachine/BaseBftController.java | 11367 | `1a0ec9e1e9100c6242d16d66e4242eef6b9717ec49a7afabd956d271766dca9a` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/statemachine/BaseBlockHeightManager.java | 1480 | `cc35dc9bdbcc68a0559d0f8a5dbb73c4dd6b57bb2ba149fdeacd78fa2a93d72d` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/statemachine/BftEventHandler.java | 1697 | `252ea74dc18fdc540271358a325416dfbd9ee019a7360ded57cf292d5ee131c1` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/statemachine/BftFinalState.java | 5393 | `2010955f4281a0f64acda995be677ad31c97f127c0a2b03742d8d2bc9bf9e0ff` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/statemachine/BlockHeightManagerFactory.java | 1149 | `753655478394ce2e85024cebbe7d547ebdfb4535a4fab707a4dd57f467aee20d` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/statemachine/FutureMessageBuffer.java | 9873 | `e3b73213dab634acaa0c6c455f13f0aac7ead660f88d153f844435fd69b79cda` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/bft/validation/ValidationHelpers.java | 1820 | `25e161ca2524989af2bf0345b218d3e58b6691bd6d8ba91f1874b7719da64621` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/jsonrpc/AbstractGetSignerMetricsMethod.java | 6903 | `9398d4b6f2923126e40e77723f7a015990c67fb3cbc7d32ea5b48df493e19e99` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/jsonrpc/AbstractVoteProposerMethod.java | 2529 | `2568d0cefade3553b126a8bc42c88d7240cbee33d972f1d44ecb8327b723f8f9` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/validator/ValidatorProvider.java | 2515 | `2ec6fa80679cab19faf32f61d5a1ace3a82924bd68ff7495a160cd2b44ba2b49` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/validator/ValidatorVote.java | 2576 | `127576b497696ebbf9910e019968f39d7fc077378473070d7fc7ab7a7970938e` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/validator/VoteProvider.java | 1585 | `f32c9e277ad1bf589fb14bbc9b477168ed4217fe80d0b9ad6fb282f020c42aac` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/validator/VoteType.java | 950 | `2263946c81bdaf777e3805be5ab5ad568efbba8543f7d2d59f8e1ba76f6281e9` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/validator/blockbased/BlockValidatorProvider.java | 4222 | `067d0af2e455e02696a56fe963ef7ef2879de988b320991f3c7dbd9a11407419` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/validator/blockbased/BlockVoteProvider.java | 2237 | `8f741203663ddc6d5dcfd806624e7c0c21c9bc13ba06a1a5283fd59bd69293c5` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/validator/blockbased/ForkingVoteTallyCache.java | 1878 | `a819d4f8e85fc459fe26afed27b2b23e42295379dac8172fa78a15bf05c9e2fa` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/validator/blockbased/VoteProposer.java | 4685 | `23cf57ef64195f30c71775cedff79c6d8b9b9f75907a18604ce892767cc0eda9` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/validator/blockbased/VoteTally.java | 4983 | `e1abffa3d8d7004d7c02e4c70e13ced2f6869af3e371f323c8f2eeb408c9bfc7` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/validator/blockbased/VoteTallyCache.java | 4673 | `d5f939df49215e62e09e56cc02fc2d451384f8e9e687553c5821df501de289d1` | 0 |
| consensus/common/src/main/java/org/hyperledger/besu/consensus/common/validator/blockbased/VoteTallyUpdater.java | 3216 | `1ab8e0f1f5cf08fc02a1660d62acda23ec855c18447138e029d5802c306b8505` | 0 |
| consensus/ibft/build.gradle | 3584 | `1c7bf0b067ff313f456e00c02cf9b44a331dd76975e9ed7c72cba96e2794daa4` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/IbftBlockHeaderValidationRulesetFactory.java | 5070 | `78120b62ad32afcbc924e682ca08ea41220275cf1c0199ad1547b677f3481ee5` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/IbftExtraDataCodec.java | 5474 | `c51960694e46a5f3f9d6c04258a2e3e12599f5f8c8ff04bdfbbd619e1c393a78` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/IbftForksSchedulesFactory.java | 2472 | `1a4066e349bdd180c536715f4ba0f2b03d8c811b09b4eb95152bb5e174290c15` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/IbftGossip.java | 3019 | `580494b33a241c55462b9eb75982fa051056223c61fd766b5e0a80d4b81604eb` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/IbftProtocolScheduleBuilder.java | 7501 | `1fb61b909fe47917b8ff3120d8d01a74a48d327f56eefaa7b40bb859d2b2ab21` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/jsonrpc/IbftJsonRpcMethods.java | 4699 | `2c8ffc1934d2719c33aa9feac06fc4ae5385754234d05a33fc2b1eaf34b8fa3c` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/jsonrpc/methods/IbftDiscardValidatorVote.java | 3007 | `ae5a47d1a43d8eb392142ff63509a87bb4c9d9318abe76f630c29937758878b8` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/jsonrpc/methods/IbftGetPendingVotes.java | 1445 | `90e15d2f3cb2049bf0739328c10391b28dcf1d90f01c89ba9db7fcc8d68bf53a` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/jsonrpc/methods/IbftGetSignerMetrics.java | 1819 | `395616ae1fd47ffc2451f7775eadc9d35de3a3626151f3a69bd7438f06e01575` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/jsonrpc/methods/IbftGetValidatorsByBlockHash.java | 3450 | `d63dd22cee999f3a70785c2992c7090de3a892161d369a001bde56df6443ed72` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/jsonrpc/methods/IbftGetValidatorsByBlockNumber.java | 3419 | `57ff70636f405e1a12388cfd3179622596e262a321da8b33b0a3585b1fc70772` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/jsonrpc/methods/IbftProposeValidatorVote.java | 3545 | `3c23d60fbdc2ea6fcb84961805e669b8cd4edf68159015dad1763006a7deee6a` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/messagedata/CommitMessageData.java | 1933 | `38dd7cf920a96b69859d5bc078a47ba2b0a587d1eb15d4f491dcaddfa2e0e30e` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/messagedata/IbftV2.java | 1025 | `41da06037cff66ca774c834fe5add1c6701a38232d68748d895c5ccbc2a47e02` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/messagedata/PrepareMessageData.java | 1953 | `fbce17c4c84696e77d98b1d21a9a96425ac7aad428ee2f611b8827fc8010c112` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/messagedata/ProposalMessageData.java | 2289 | `f23df77738c7c233b0ea4208409d73c6163993a1a81e70057dad03c8c571d66a` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/messagedata/RoundChangeMessageData.java | 2069 | `7b825b0ffb7efc269ef0367f62c56a68cea10b55c69bad043997aa997a144831` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/messagewrappers/Commit.java | 1915 | `6a6e356d3f61af3d4498a417cf9769b6043cf496dec47ee9b45e3b02e3d6087b` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/messagewrappers/Prepare.java | 1726 | `624e3a8783ba0efb70d4b02fc447ad70c158b60501504cc67913c3d168b42e68` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/messagewrappers/Proposal.java | 7230 | `b9543da714e5758c9ece69025e3019a4751d7d2f81f99ba083df75bf80e3b301` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/messagewrappers/RoundChange.java | 6022 | `d6e336250027432cf48dd354f43396c67544f1368d9a74d5e6ac980ca4fe6ed2` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/network/IbftMessageTransmitter.java | 5497 | `240b7d49bb023f846b1f49f50c12ee28a3e542b17b820a5400a630b2d22d8d22` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/payload/CommitPayload.java | 3936 | `648de875a1e4209b374dd5b9a01909a952ff5fcc40fa0ebd73f2e14dd96e3741` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/payload/DecodeBudget.java | 2770 | `ec01bc58fd4f72f8994f84c08b5f0f154e3c8a484c937c5c05e822ffd5d60cb4` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/payload/IbftPayload.java | 1103 | `90914f63adc84bbf53b68e79a350c225f64005fe964ae5475bae9dca2885c845` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/payload/MessageFactory.java | 5876 | `201e16cef8323a2f9383f94fb0050c1cc0d408fc107bc3cfe66e292cf7aaa1ec` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/payload/PayloadDeserializers.java | 5491 | `073ffc02fbaec46dd2318c1cb2f0c1d2f058b4eb0d2581b52debe04ea22696b6` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/payload/PreparePayload.java | 3208 | `4561e4cdc06819f9b1db5fea5f12b8c87ecce8c6c44010f40df583461cc10b81` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/payload/PreparedCertificate.java | 3852 | `ccffd410daa232d77e1aefc7f0e52c2fa1a4091af7ac569a54ad0e82cea31fc1` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/payload/ProposalPayload.java | 3187 | `f01bb2ee4949811b67ead8ffa62fbfc35af4585afedd2d2f3bd503585556c9ef` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/payload/RoundChangeCertificate.java | 4179 | `80d2a7491c09b3d08b33e77567432b0b42d37a1a3a7803d717b0a327f9dde683` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/payload/RoundChangePayload.java | 4178 | `a493b79ea38b2c3e4cba0a7c6977af701524a3a40def96de199e8a5244360afc` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/protocol/IbftSubProtocol.java | 2142 | `5f46c3e881ef26b58e8043a5a1db05da65ab5b03b77e4dce5e8e31367b470d76` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/queries/IbftQueryServiceImpl.java | 2897 | `0fce432277daaf0b5eadd24c6678c77be4a0abd62d878e3094545718776357b0` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/statemachine/BaseIbftBlockHeightManager.java | 1701 | `b55f84d99f956e24437eca34706062fdbcd1bd13e591cb8174f53337061ba511` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/statemachine/IbftBlockHeightManager.java | 14127 | `a7baed3a7bbd8779e7b908246973f3afb0b46e5a53ba920f4501b447d4a81957` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/statemachine/IbftBlockHeightManagerFactory.java | 3519 | `c2a042a3e44d993b11cac4994085b409e1bad3314bcdb89dac6b7f7ed3825242` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/statemachine/IbftController.java | 4871 | `832161e253c8796a6f787c91ecd31d52c1c5a4eacb2edb47da33c1a2a382d3c8` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/statemachine/IbftRound.java | 14667 | `294dac2c52ece4e1e8d2fc050685f7739e0df15f706f34d53c8ef9e0bd78a42f` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/statemachine/IbftRoundFactory.java | 4833 | `544312e159f313e453d422f3613978018873f07e82c3348eeac489e73d5b69db` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/statemachine/NoOpBlockHeightManager.java | 2192 | `631414bc7987d8f08126449184d008594eb5d5d9251b8f4e54aa605cc0b63c8d` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/statemachine/PreparedRoundArtifacts.java | 2183 | `8511f4ff45827d398071f8ff33c40e8ba170552e9ae4caed5bef9252fb6ac9c8` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/statemachine/RoundChangeArtifacts.java | 3802 | `5afd9b769ea2ae2b4c244c41886b8749ecefecf8ba2c4ef2293c42a3c1413c74` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/statemachine/RoundChangeManager.java | 5581 | `e01ea0f6a699b8d459f5269d2d50a3a13b88837867bf5b375585e1a656f7702b` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/statemachine/RoundState.java | 6107 | `d9f6f51710ee2fd6fa545dac9590e0ff5eebab90e42a1bf25ec51a0b42746ae8` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/validation/FutureRoundProposalMessageValidator.java | 2504 | `547bab967c6dd03858d42845060465a70c831f04c056fe16e7e0562eb2e4ff04` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/validation/MessageValidator.java | 7295 | `65dd85273ad83d7d6d38d5cc3f32e293f30df92413f1f9a9180b8e109d1cff9a` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/validation/MessageValidatorFactory.java | 6151 | `b728b334937407381992de0fd7c0d1dc8c88c772f80f368e5040d4fa0e5e41a7` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/validation/ProposalBlockConsistencyValidator.java | 2960 | `7475f139995031ee28d8497d3990288269ab3eae8bee8ea2935f0c8e14255600` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/validation/RoundChangeCertificateValidator.java | 7822 | `e067d5f40ad7e94249fff5a259a7d82b2d61b6a5175a99f3c6577c39aa2068dc` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/validation/RoundChangeMessageValidator.java | 3029 | `f82aa2eb45d13eb991c77070fbbaab76a47254d4828aee219964ddfba4aa8120` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/validation/RoundChangePayloadValidator.java | 6728 | `12a5f0142317f7fa8dd952fd87b433a4e39fdb4b51b87b1e7b421484ba8c8344` | 0 |
| consensus/ibft/src/main/java/org/hyperledger/besu/consensus/ibft/validation/SignedDataValidator.java | 6532 | `46c23df9de6adc6b3260252f218df8f814dc7b710a2e336abb10ed23f680e376` | 0 |
| consensus/ibftlegacy/build.gradle | 2821 | `24de5302ec773e9a01b89865ef0b125b85bd7cd89f012e3e274642b7142043ab` | 0 |
| consensus/ibftlegacy/src/main/java/org/hyperledger/besu/consensus/ibftlegacy/IbftBlockHashing.java | 7587 | `c9d05727e87baa068922e9cf6c4c72b04c545e9cac0a1d13d88f449ee1253332` | 0 |
| consensus/ibftlegacy/src/main/java/org/hyperledger/besu/consensus/ibftlegacy/IbftBlockHeaderValidationRulesetFactory.java | 4619 | `7ef875e92ee9bfa816aace816fc45b650585fde52e58775c4fa982fdf3517c91` | 0 |
| consensus/ibftlegacy/src/main/java/org/hyperledger/besu/consensus/ibftlegacy/IbftExtraDataCodec.java | 4132 | `20ec3dd8ae8e2cbdb6aef9e5851c725e709ed4d5c72c55009a2d77312407468d` | 0 |
| consensus/ibftlegacy/src/main/java/org/hyperledger/besu/consensus/ibftlegacy/IbftHelpers.java | 1307 | `3b3023261640d4d4d4ae178141e5fa1a09b3d4802970a330066c2ecc9e59850f` | 0 |
| consensus/ibftlegacy/src/main/java/org/hyperledger/besu/consensus/ibftlegacy/IbftLegacyBlockInterface.java | 3748 | `a7ed0d581ca71a7f3b48fb2ea5e2c8de81fbf6d89fc20c13a01652fb601fcf67` | 0 |
| consensus/ibftlegacy/src/main/java/org/hyperledger/besu/consensus/ibftlegacy/IbftLegacyExtraData.java | 2196 | `6aae536791d9f1eaeecba859c7853fd8d609039c946277406333c0ed0500ed9c` | 0 |
| consensus/ibftlegacy/src/main/java/org/hyperledger/besu/consensus/ibftlegacy/IbftProtocolSchedule.java | 4244 | `a6ffe0bee44b3d896a9bf6e4b6b4e14cec5c1f31881b7c5dbfc41f8c330a6e79` | 0 |
| consensus/ibftlegacy/src/main/java/org/hyperledger/besu/consensus/ibftlegacy/headervalidationrules/IbftExtraDataValidationRule.java | 5772 | `5cae6604672cf4391f5373d0cd3f6144be9ce03eaa933cb6bf4a850b2e882b60` | 0 |
| consensus/ibftlegacy/src/main/java/org/hyperledger/besu/consensus/ibftlegacy/headervalidationrules/VoteValidationRule.java | 1949 | `6f45b59226fe6c6fd61393791df8e442cd81988f43592f5c9036005bf76b15ed` | 0 |
| consensus/merge/build.gradle | 3263 | `55b1754464a9fcf81a990cf1c5c22cf61a8489e28dd64af9ae7d9dc29cd7115e` | 0 |
| consensus/merge/src/jmh/java/org/hyperledger/besu/consensus/merge/blockcreation/PayloadIdentifierBenchmark.java | 5252 | `0b6fe1b65123f62c90660e81b9a6e2ad4250560501bd6e630701c9996c4ff6c8` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/MergeContext.java | 5159 | `8e207b8cf1480c8cbfaa8471bde0f5a933f843a94895f807c25f5a459dd54751` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/MergeProtocolSchedule.java | 5839 | `a36d3045b5d2f66c13bbedd90acb94e0c7f1f2bc7b854b951875d5e493673ca7` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/MergeValidationRulesetFactory.java | 3700 | `7c21a1c27b2a20d89ce853f083b0154a3bbfccd4dbdf5a541628230f18184670` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/PayloadWrapper.java | 4792 | `08d707ce889b3a19b2e31ead936587998bd29937c52790ffc6806ead98cb9b93` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/PostMergeContext.java | 12120 | `2a72ee3730d76581125ec58b9f3133b31225a4d315fdb7549e79e1d9317c0c58` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/TransitionBackwardSyncContext.java | 3325 | `3ab598b4a89f84c928c6b71903b36b513097025b80733c3408333157362d35a9` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/TransitionBestPeerComparator.java | 2950 | `56b612975896c9851f67057878e611f1c8c5cd9a69293dc5d2d9a747c272a34c` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/TransitionContext.java | 5393 | `bffa7b141709feef1f1193a28a8468c4f8a4a91fa3877205ceae513951644c99` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/TransitionProtocolSchedule.java | 9456 | `0691f57f5dbbaf10847ab750a10ece1858f1f1f51b0d5100fe7ad6cff35eaf18` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/TransitionUtils.java | 5379 | `de981fd5e128a81f3e12b46f09a30a0b1d73bc916be65bfaca526b86f57347d4` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/blockcreation/MergeBlockCreator.java | 4663 | `872e1a387b57f2b92742aa45dbcc7bf2ddee7453032da0324181c650990ec57a` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/blockcreation/MergeCoordinator.java | 46877 | `3f560fdcdb654104f887ff290e0a50a9eb37081af632145d704372384de04e36` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/blockcreation/MergeMiningCoordinator.java | 15277 | `dc493c06ee049d836031d20eaac1c91a48d1faeea6cd65712eca0aef92482601` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/blockcreation/PayloadIdentifier.java | 4807 | `3c6b5a66fec657ce39457bca2b35874feab7b6de48054516979b16c4df8b299a` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/blockcreation/TransitionCoordinator.java | 8052 | `50b77541802b1856d15c668ff88e90da0b23a585538c1f99d61be75a474871bd` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/headervalidationrules/ConstantOmmersHashRule.java | 2418 | `0cbe7975d4f9b4e1185f89c8d2c3dac0927101db6aae47aaaeda4a8f22230469` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/headervalidationrules/IncrementalTimestampRule.java | 2271 | `bb22fc56a731d6914008815cefa1e14f827dd76949ea08df637fdaeb2f48382d` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/headervalidationrules/MergeConsensusRule.java | 2840 | `d3a7fec8204463cd9f3dc2765faf960320240bbeb89926de0179a7990153518b` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/headervalidationrules/NoDifficultyRule.java | 2073 | `94bff51f7ad144d13a6fb2dd22820f8acab3db77a62fd4a0b701a6ef549302f2` | 0 |
| consensus/merge/src/main/java/org/hyperledger/besu/consensus/merge/headervalidationrules/NoNonceRule.java | 2023 | `4401af6441901d87e1f149597299a42548fe47e3dcac0af48b9ce28552b08c2d` | 0 |
| consensus/qbft-core/build.gradle | 4226 | `a9f5fdf6e191e9ebab48bef00265dad3f92e1272a4e06aaa63fa9a0be7e5cac1` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/messagedata/CommitMessageData.java | 1940 | `61451a8bf2992d201d1def80ebbceda41b3205c85515a1e26faed0ff2d563cd4` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/messagedata/PrepareMessageData.java | 1997 | `0eaa60014487c5da7f8d5e3053422718822114afdf6ad39d67a294a5e11671b1` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/messagedata/ProposalMessageData.java | 2534 | `fdd808ca508b4f82b071e3520948b6e512bc6d1bc8f0adc61e8530f633be501c` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/messagedata/QbftV1.java | 1045 | `f2081e2c14e715ed07f2ee4389a0ce353c253753f017556eb7455e51b6e6ab18` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/messagedata/RoundChangeMessageData.java | 2619 | `3056dcfc67aa3fdb56beb52682c227e78167288d1eabe2d20543ae92e2621a9b` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/messagewrappers/Commit.java | 2339 | `261cb5b5bec864f521dc621d494ed14fdd5a52e9185fe839097800d1e5ea1303` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/messagewrappers/Prepare.java | 2160 | `3279b313a63e86ee414b4c8d1d5e455fa0e90cd5de103c6b3bd7e566b3c135f0` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/messagewrappers/Proposal.java | 5109 | `3a897f1e3a5c8d2b8f3da4a30ab64ad5df0773bd935c57240427372f724c3d4e` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/messagewrappers/QbftMessageDecoder.java | 5359 | `a121d9e4799e81acd1d74c23d3ba94fa366950fc3da0c1475b08c6998d3c3235` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/messagewrappers/RoundChange.java | 8467 | `24220d6bd26cbb744f39569fac1c048cce77c5a0ab25f8671ed6da944400709e` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/network/QbftMessageTransmitter.java | 5801 | `b7ebf515091c0f8740503a079983b2d0a77b889bcc7a8c98cb864c5b38facfbc` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/payload/CommitPayload.java | 3927 | `6238d95f5500a1bcbed9dd0a45c7172fdaad2c74656dd0b10d115aff4bf244e5` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/payload/MessageFactory.java | 7424 | `95fea5564973dae1922c8e5d66b79a352b1d3658d6790657f219f6da35d93669` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/payload/PreparePayload.java | 3226 | `99afdfa3ac4ad80a5a25678597a2ee7e0a4bb4965b3383dc69cfa03098bded19` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/payload/PreparedRoundMetadata.java | 3121 | `d986bac99c75eb59e607329f29a3255e603a2438dfb33653d24b9fe198d57da0` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/payload/ProposalPayload.java | 7722 | `e20982c2c64bcd15f617990a29f70be0d2b3491df4eed6c8989359326cdded21` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/payload/QbftPayload.java | 1996 | `392ca08f14d5592ac4f2d5d7634a62a090bf8f2562b1ab2aff3928e2cdcfeff9` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/payload/RoundChangePayload.java | 3994 | `37fa3f39dc0ca621afc091fb3111a9749e38c1ba7113a459d0307a09d88fd65a` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/statemachine/BaseQbftBlockHeightManager.java | 2707 | `5086a0b90db2b01f7f5bda7810906e5011451cc1cba95c11467b9af443c027ee` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/statemachine/NoOpBlockHeightManager.java | 2483 | `261a0ef34a2852873022297060a3b29de0194e3a09d0c2fbcb5822d8d8c119f6` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/statemachine/PreparedCertificate.java | 2704 | `b68de420f3fd1721aa99f32bf26df47e6577933b621a740b2e7dad848e04e322` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/statemachine/QbftBlockHeightManager.java | 23932 | `b478e44bb36cadddb030303037bfb7c800f89c47aa5432384ab3f7960e761ccf` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/statemachine/QbftBlockHeightManagerFactory.java | 5801 | `a16e87d2fc703854f20f1c08802e1a85f9564401ad6ce3f795017287132e0222` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/statemachine/QbftController.java | 13804 | `2386560f866d197f91e794d933d8831024d9ea77b22a2c1b9c74890fbed467ce` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/statemachine/QbftRound.java | 14540 | `254e74eb13bb342ce7b438af46d38555a488286e7fb6b9d0efe40cd77fc020a4` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/statemachine/QbftRoundFactory.java | 4717 | `2bba679686039e68b4a89b7a54a18f252ceb1ef61f89d5f14feedd1dedf04da8` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/statemachine/RoundChangeArtifacts.java | 3480 | `5cce1af245d85244553896692d8d22f4238d3e8f22890eb2e52183debfc2135f` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/statemachine/RoundChangeManager.java | 10943 | `34dfffe18d49764824610ecdff19cd06020e0ec74690c714645a62d0cbd8d0c3` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/statemachine/RoundState.java | 6388 | `b30ed4d5ad461545da94037255964fff810efaedee66756bed726236a925b154` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftBlock.java | 1387 | `d1f955d851e8f3f110f62b7e42affe3cfa5932628b45f9ebbe143a2ffe5d298a` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftBlockCodec.java | 1236 | `16b008c5473b16b8da2e5a533c19e2216bb979c3bd44e272b866f0dd24019a18` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftBlockCreator.java | 1742 | `7990fe2ecf4d03d57aae55277855b9477ad2bbe347ef2fd16096110d9b720faf` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftBlockCreatorFactory.java | 1066 | `73f66d2d560ba05f90ac90dc914dfdbcdedea7e58ab70b1a7e592959293b62b4` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftBlockHeader.java | 1324 | `0423f4763146ce8958905bebaafc80100ec31eda5f97203aa340c7b506b93a48` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftBlockImporter.java | 1158 | `31b635a38c5d7407fc1e0fc8daa353e0216db84a58135a1d62ab4ef5ed1b1ec6` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftBlockInterface.java | 1808 | `cc0214765df2198828cb5e7350aef63c733c970804976b8eb2ce4d5ab437fc4e` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftBlockValidator.java | 1394 | `9b381b813359c5b8e168a4ddbecef87b62301c1415a4d0fa9c7b0be9efd3dd9f` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftBlockchain.java | 1033 | `7bbf43dec1487d6a4f1860b6094720ec66d130fa8c96cfc772ae89d4f895f9db` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftContext.java | 1490 | `b731f5d0b5286ae36e18e2b841ea594a850fe1d6a30e8527add6b5ab5e8e6ec3` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftEventHandler.java | 1558 | `fedae9938192edb3a7ab0b6c489a027e867af7985b3940f9ee0d751bb968adae` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftExtraDataProvider.java | 1063 | `7f9b42895359e6ed2396f81695e7f2978715480ad6672066c6bc4be3d3d82c90` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftFinalState.java | 2613 | `6986fb2a51508d63d89242175f68e6d38c74fc9031c51239b2719c3ce4238ef8` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftGossiper.java | 1060 | `3ec8a8a6d8a40096042c02c985757910f7980efed3a837c310a00d3a1a5c731a` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftMessage.java | 914 | `176a0c5b85006408fd41648e71b300d916f6626b1968b8047b0fc2c30564902b` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftMinedBlockObserver.java | 892 | `255596ed6ac95546ccbb7eac8859ed187f6522932869c947ff0a931d919b3606` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftNewChainHead.java | 1315 | `ec3bf9ff3d884a9331130147da075ad41eb75e2eb039de17cc1353c86255ee5a` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftProtocolSchedule.java | 1324 | `c5c91864e34576bcc0db772c6e4a6f4a3e59d043a7a78f7079867b190cb53b4e` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftReceivedMessageEvent.java | 968 | `93d85376591bcd473b35c2913f8585b1abd9b456ef00715ac679d1f47c55d6d3` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftValidatorModeTransitionLogger.java | 944 | `9530a630a77756543f37007d7ff6f47957752bd2a792b478cefb64041f2d6384` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/types/QbftValidatorProvider.java | 1220 | `c22b4bfa7a7c9027be626804804a1be047ec948ea549671423136683f3ad70de` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/validation/CommitValidator.java | 3704 | `badac8983fcca63dd88e7f61ada809e7405103027e1666085aa7c3ee906d9081` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/validation/FutureRoundProposalMessageValidator.java | 2211 | `e40839ba3e9726592f5bfe27ed06a0a0b610aba7b8c1b121a08926b156847dca` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/validation/MessageValidator.java | 5571 | `41695535b74243dc0bab852d4feebec40da72652fdaf5efc0b258014f663accf` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/validation/MessageValidatorFactory.java | 4623 | `09fd0b1c2f4226a473b0a6eace82d2289a1e9e7249bf7e4487be02dbcccdb99c` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/validation/PrepareValidator.java | 2904 | `83193bdefbb853629c9693c7099c490cf3b70ea61a564b2f6f6bd822c083b8ae` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/validation/ProposalPayloadValidator.java | 4447 | `4e6319d5dccf67aac030a1f9af6315361fd41bbe73adee7819e54a9f4fd112d1` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/validation/ProposalValidator.java | 13565 | `7ae3b5f74411ee3aa6a2f9ded25ceb63a65b9a4c9a8db1a2a3eafcf105832774` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/validation/RoundChangeMessageValidator.java | 6252 | `5d80687a9dc36ec3fad25dfb4a70076b784a557e14f25d92a206257c70ae7dd5` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/validation/RoundChangePayloadValidator.java | 3382 | `829d2b76ec0192c2192ed683f75a6cea44e0495df552a0c1288ce8e695d8b432` | 0 |
| consensus/qbft-core/src/main/java/org/hyperledger/besu/consensus/qbft/core/validation/ValidatorUtil.java | 2848 | `975938bd6950e84ed7836bf176ddca886ff36e40613f760e0f68c440c494c2a5` | 0 |
| consensus/qbft/build.gradle | 3419 | `bd28ba02d2d1bd462d4034ff38ad4c3b6ef757a2914f9990c2a742db3dc396c5` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/BFTPivotSelectorFromPeers.java | 7501 | `e7df2dffaaa4aed4631e426986d4c8a82f45e9ee559e26ffdbd1dd3c7135a59c` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/FutureMessageSynchronizerHandler.java | 1888 | `c79e5772c53f71f3488c2d9cf480d7c308a29c12869b506d5f1a734c738d47ef` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/MutableQbftConfigOptions.java | 2061 | `c0217d026ea85a61b002c54a17d24a7ebacd2b47f28120898ecc5865d9294728` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/QbftBlockHeaderValidationRulesetFactory.java | 4933 | `14c3e42ba6a4ee269febe62900a9d6a022d387e747cd8c273a32a52cab15c5bc` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/QbftExtraDataCodec.java | 6088 | `43263799d4cfa9dedd01121b2393dc64d6fc50f24f0c69ac148c7d9bfc0b10b4` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/QbftForksSchedulesFactory.java | 3737 | `4bf29773f80b78c0902c1423ff0965cef45b754d999de921b968f55e73d5dd98` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/QbftProtocolScheduleBuilder.java | 8126 | `2d43d7dbff0d9802c32824dd55c05e2e0ee491756e6197c322f9078086c4b0b7` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/AdaptorUtil.java | 2474 | `d884971d7933847abdecc0b349c198ff156590f5159788f38bdb7e793ba2b408` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/BftEventHandlerAdaptor.java | 2722 | `1f98e89c9f477c132596b070fe017fed045f79065d17b9c4819243e5c641b6ca` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftBlockAdaptor.java | 4202 | `6509419f851c00464b44027f39751ac9c704044b4a2effdcdd93178082f349e5` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftBlockCodecAdaptor.java | 1955 | `7571351b646ebf8c194871005fe8419ed72ffeed29f331dd24605544fe043356` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftBlockCreatorAdaptor.java | 4683 | `92fe6f9c9aa74660dacd810a1d79205dba97d3bf7d7bf6539244445c98f12eae` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftBlockCreatorFactoryAdaptor.java | 2335 | `4fd79340d9c88d151c97fdac7fae365af1c72595344e228c78896b578d1e0f60` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftBlockHeaderAdaptor.java | 2221 | `3552724d5c7a017ce44f375814dae160c0275eb88399b96bf0ae6c0cc762c27d` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftBlockImporterAdaptor.java | 6197 | `41e1b326ba2c7795412c98d5e17239fa8ed7cb8df37eb3e13d265ff78e217cb8` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftBlockInterfaceAdaptor.java | 2723 | `4e0bf13724992e4d12d40d92b2d82550c542600b04a6e362357406cf5bfdd8d3` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftBlockValidatorAdaptor.java | 4410 | `659655336cde7da2d456abc912a818a77c36af726b9b2d26a8b6652e88ddb3b7` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftBlockchainAdaptor.java | 1643 | `cf20783326d9c958075b20a7e62eb5a0fbfcca37fe0ad42f0a95042bac84eed8` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftFinalStateImpl.java | 5374 | `cb2b653225eba0f939741d5643e1ac0d07d4f7ea83617430eddece5faf4ed88b` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftMessageAdaptor.java | 1660 | `49488eb2f151bd41672aa59be5604c328fa8f5dcc4e7d5b7d89fde85c6cd9cad` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftProtocolScheduleAdaptor.java | 3158 | `8bb88a4a20fba45fb5c6373b65311f5d96dbd97d17cbe953d56888948dbfeb0b` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftReceivedMessageEventAdaptor.java | 1702 | `806f0d2726687d8ef68a85478834fab2fdb74ff581889ca26b0685c8a163d013` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftValidatorModeTransitionLoggerAdaptor.java | 1793 | `ac469ae09e49e4f02d3e9508c894ff0f151cd4a2addba5e065fae5cf6232df3e` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/QbftValidatorProviderAdaptor.java | 1882 | `db6ade46c87067160061830046e6a04f316ed60724cafde653ae24dd3cc710a4` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/adaptor/ValidatedBlockCache.java | 4420 | `23449edebb65d04b6681beafc666c51d202bb711d6a5a2e6ed592b4f4509aeff` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/blockcreation/QbftBlockCreatorFactory.java | 3834 | `9163f16752790a1ff7ed37df8d1e43bb3b61fd810774c17678ac82613c08922c` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/headervalidationrules/QbftValidatorsValidationRule.java | 3622 | `3a02bdcc180db3193a0f0864145e6f61dc24f35deb46a9409849ea4f84a8f508` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/jsonrpc/QbftJsonRpcMethods.java | 4442 | `2538624dff8271af5a951fdd0e3b3bcfbae4de2f50a32c4101c0d4dac4f71924` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/jsonrpc/methods/QbftDiscardValidatorVote.java | 3167 | `a170c8140b1ae8bca8ac3caf439ebd40e9ea784eba62b3dc2bdf64936b251bac` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/jsonrpc/methods/QbftGetPendingVotes.java | 1445 | `f246f2b9790debc79cece09dafd65cf699803d9ed90a3eaa049e6526e5d94fa1` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/jsonrpc/methods/QbftGetRequestTimeoutSeconds.java | 1966 | `86083a23c4a304e4620034f16d9b1f2f95a7d4804b61fcf5011d19fda8c2ca2c` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/jsonrpc/methods/QbftGetSignerMetrics.java | 1819 | `a1bbbfa53895479b68edf43e990cf86a47b17ac68b9d24da1367e6008556c142` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/jsonrpc/methods/QbftGetValidatorsByBlockHash.java | 3577 | `0f2c5efca78777019510105ffa0a27dc0548a9fac4898771020fe858b596f9b0` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/jsonrpc/methods/QbftGetValidatorsByBlockNumber.java | 3945 | `05908f9f4c229cc40788fccdbab22d12df3dd3399365920ca02f651671d2c9fc` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/jsonrpc/methods/QbftProposeValidatorVote.java | 3744 | `3eff8b6bd5d3685c966f16e72bdbaa2dc57d3040e65a15f27a2bf5510d6e75ea` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/network/QbftGossiperImpl.java | 3796 | `118936a4c6f1d18a992a9af46ff44509e5e0514cc65b504dc23983d38b7fd956` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/protocol/Istanbul100SubProtocol.java | 2223 | `5a30ac88138141d6b89f6cdce329d1850bb6a70b633c8087b4f09fd61983b605` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/validator/ForkingValidatorProvider.java | 3896 | `098f1e3544f7ed43ae888fb3e259b2a04d22262664766df33c3757918da7de0f` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/validator/TransactionValidatorProvider.java | 4630 | `c8308c63ae770f749cb328972e4b7ad0b0f2aaaeed223ef3a1400b551fc335db` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/validator/ValidatorContractController.java | 4908 | `eb3bf9aef6128a90cd979f362b737276604a396609ea4ff7d0fc6a21d4052acc` | 0 |
| consensus/qbft/src/main/java/org/hyperledger/besu/consensus/qbft/validator/ValidatorModeTransitionLogger.java | 3511 | `861d78a19254758b884d7040fe111677699dc2bba9dd52ced03c9ba5297b64a9` | 0 |
| crypto/algorithms/build.gradle | 2030 | `942fa3753f0a21213cc26da2e27097a27356d6dce26c187429ea8e9b5ec3dca3` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/AbstractSECP256.java | 18799 | `c82f5714d61029a6ec1ff713b793b5fd0153263b78e0ee04b2807fba812ba9ea` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/BesuProvider.java | 1385 | `b8e90bfcd9e1fdaa9f4de4660bcc3848b8a7d71011f73190344b5be7320d6220` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/Blake2bfMessageDigest.java | 9966 | `a47690715818627a3ec38ba5470e3b428bf744e385ca67257303bdfa78b27596` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/CodeDelegationSignature.java | 2101 | `104922ee4d2911dc97e2930648994f848a63dbde53c0befef650d778b7bad966` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/ECPointUtil.java | 2118 | `76126e7893b9c09cb73061e342ef15f920182cccbfa3765007344e50e586c244` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/Hash.java | 4290 | `a8408f11dc2a484c6748a3e2886409697215b959ee8924aeeaba2f29f17b222c` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/KeyPair.java | 3837 | `53e3e4f3d62d1c53363cf9a599654da1a52bbf09529f953da61720721f6b86ec` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/KeyPairUtil.java | 5635 | `37aa8a1c22e257e7cdb32e9d339e2e015b15ccefd8599caffb5803caa8ed4d1e` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/MessageDigestFactory.java | 2231 | `9bdb8f36b91efbfeaebec5bd3ee7416dbd37a739ec56d274b779805ddc090654` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256K1.java | 11337 | `6c41c6d234240dca030f19ea19af1bd02ca6815bbc1daeff2b9cf36d2c81002e` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECP256R1.java | 6039 | `be00071f55c6dc55195a204e57cc76a251dbacefee521fa9f8c155f09e162844` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECPPrivateKey.java | 2742 | `8d31ca84115d719ab84a4c00977194de4f0a8eb764ada6b81e4f4eddf54444a1` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECPPublicKey.java | 4944 | `ad068d754eb313754621c33d3afec106786a6ffaa60eb20584da5bbc7098779a` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SECPSignature.java | 5417 | `c6afd11f329e13dca855cbec76e502f7fb746ac5452a66bc2acac00d5d881a2b` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SecureRandomProvider.java | 1559 | `b016a68bae46f5a801dfb03e4dfcb707934fa12db179ba47c90219ad15a43845` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SignatureAlgorithm.java | 7600 | `e830a6d01a6db1441840a53ea8f774b502af7c449054e3fc007e943e245c9311` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/SignatureAlgorithmFactory.java | 2592 | `8eb0cd727028fb31c868bb890c4feb56e229e7aa0aa0a842cf81f0fb8e4cca19` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/altbn128/AbstractFieldPoint.java | 4444 | `e1b45c5232037a31850de514cbec1eb9e7a23db899ead549c74f79d92c555ad2` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/altbn128/AbstractFqp.java | 8168 | `0c7977f66ddffc3dfbd13f71c6b073a7692ea8a963a2f13677161cfff64cb69f` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/altbn128/AltBn128Fq12Pairer.java | 3838 | `6f27c0f4e960de782e78bd47fa21a098a367b264262530704d760ae98ef4cd7a` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/altbn128/AltBn128Fq12Point.java | 2723 | `517094e7a296c3596c6164a7f9bdaf3160b916d2a9f88ceb5b92f0dd2be4c077` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/altbn128/AltBn128Fq2Point.java | 3013 | `92e1519f02bcd65431ef7c32142d6412b837c4b182c790a2c7560ab88ea73510` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/altbn128/AltBn128Point.java | 2205 | `3c207d290ad47b85b4d74d6183ad1afa57513714c557c2d06559ebb933dbcc0b` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/altbn128/FieldElement.java | 2090 | `5187a800e674cb3823b1fde5de338a4bf1990f3ddc511139874c21d761015f78` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/altbn128/FieldPoint.java | 1551 | `ebc2da7beb8b462e0695c5f385c2c5b1063bed86cfdcb7a22d2ab9bdf897a992` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/altbn128/Fq.java | 4534 | `e42ed2d3b1c9aca9edc2a3a272cd1123d945976ae03201e793c9a5d0fbdd075a` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/altbn128/Fq12.java | 2816 | `c430438c92af5a2bfab68f6cdbbe8e03a8d42983c156ee05c130ec0d7480e3bb` | 0 |
| crypto/algorithms/src/main/java/org/hyperledger/besu/crypto/altbn128/Fq2.java | 2191 | `3ea0be75fd419746e4988ab3f55cf521676ed5357e56b04ea68cb84ab80a5614` | 0 |
| crypto/build.gradle | 646 | `aa191ff708e7b1f228615c5b5cb16cc678f78950515a188dfc87a693e9676ca5` | 0 |
| crypto/plugin-api/build.gradle | 1855 | `4752a502c49674fd4805265f0358019aaf16217e033bf99394e45bb916f4f357` | 0 |
| crypto/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/SecurityModuleService.java | 1732 | `e32dfeeb8ce28d552bc9c47cd816c06d7c0222b7ac5a8c169ba0d9494d535c42` | 0 |
| crypto/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/securitymodule/SecurityModule.java | 3190 | `08f3aa4d7ff3d866170ff934fe6e3872a58f73190f2ed3280be0f19ce9221f15` | 0 |
| crypto/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/securitymodule/SecurityModuleException.java | 1998 | `a057c83d081a4947f2cbffdcff52a6fda05dbfd909392306e132eb68ecc31871` | 0 |
| crypto/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/securitymodule/data/PublicKey.java | 987 | `5a9c5260cf13c2845282960bcea2d348653465bfb7dc7ac36bf699b33eebde33` | 0 |
| crypto/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/securitymodule/data/Signature.java | 1028 | `9e8ab1a91c9b5c5e5c24caa7af717da4d0084ccda7f5f8d8198796c0b6eaede6` | 0 |
| crypto/services/build.gradle | 1955 | `32d94e5ac57da19d66d31651daa63d08d741fbc9bd22e3df4074ab04f8f9cf99` | 0 |
| crypto/services/src/main/java/org/hyperledger/besu/cryptoservices/KeyPairSecurityModule.java | 4849 | `98d758e2e87dadfdcc29527af197c0fd469ae5d3d245a23a2d68fa93dad1fe0c` | 0 |
| crypto/services/src/main/java/org/hyperledger/besu/cryptoservices/NodeKey.java | 3040 | `3dbd6f44a73344bdb598d13ddd62853b6e398fb7fe91b93b76e9bda8e46507dc` | 0 |
| crypto/services/src/main/java/org/hyperledger/besu/cryptoservices/pluginadapter/SecurityModuleServiceImpl.java | 1645 | `f0d09c3d0ca1734702b5f22a1023c7f22e2686108e377175b51dd66a35e63ff9` | 0 |
| datatypes/build.gradle | 2316 | `ccf614c678100e2662a192c55f3b69466d5975695784f51e5aa554ad218fb352` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/AccessListEntry.java | 2091 | `9b25d32349b5b6f2bcf3cea1b9b10544dcc85b357cccd10054c01a5e28003842` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/AccountValue.java | 1595 | `918038011a4e47cc5a3654b8067cd49d63d980e698a64bb9e688143bb706c1fc` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/Address.java | 8642 | `dbaf4a7ae8f7d0d208dce00a2d243c39bda7be05878e947f4d30eccc08461fc6` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/BLSPublicKey.java | 2690 | `227afc7416ea4ae87cf6e535e6cfd03921c5561401737b7cf0cf200747629771` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/BLSSignature.java | 2666 | `3f8219fe45af697439e1258c27f581f19930f93a6ac745dca55efbc90c2a20fa` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/Blob.java | 972 | `dac03ed606dc8af177bde1328ffd450711400959c34bb385a3f64b9960f35ed0` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/BlobGas.java | 3378 | `6c6cf5d76f3d5766c8bb27c01beade6d52e4e6c9a906e00597d18053370c5fe4` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/BlobType.java | 1969 | `77b8438ccc09ce690c1cffc9d644a8f22c4f229761873233b1ca4961bc3bd2ac` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/BlobsWithCommitments.java | 1615 | `ef7e45651904b4d237d7543f1fc13a40f3e029e53924cc3f7c8d4dc611529bc5` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/BytesHolder.java | 4034 | `5bb62bb8419b7d4a477f2cd991eecbb4e92d37897704c8153b8e303c400de3c7` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/CallParameter.java | 5952 | `9aa6206358cb064c3ef902873d7c3880bfe1fb85b20a7b66172582a441ea4aa5` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/CodeDelegation.java | 1900 | `e61248c9eecf3da71e7c9f60baab65b13b922beac375fdc1cc85783eb9ea120a` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/GWei.java | 3224 | `e9e8d5f236830e0f5c42a5fe399784a0c9d1756a21fa9ac21faa1221376de0b8` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/HardforkId.java | 4287 | `e70476be5a429940ce30216bbd00376f173a4ce207b7a8e0d6f97c0c6801015a` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/Hash.java | 4049 | `485ab6bd1178245d303ce1ea9828c2547a6a04d1dde9b408fd060f090ac7e100` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/KZGCommitment.java | 1049 | `ae22953c8ea0df06d337461a3c63ed61711944090d7852902d416d555cd90c54` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/KZGProof.java | 1024 | `af78f65882f76970301084e35b759bfee1eac832e943f8b909fc3a636bb10af5` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/Log.java | 6782 | `56930850b4aa84a66938d8b211ac77178b10022ed9e79e52fa692abdf69fa8a0` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/LogTopic.java | 2392 | `e6b4b3569ca928299fa660241a6259117d8ac8990fac7cecb7a0113028ecafc9` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/LogsBloomFilter.java | 7667 | `c8376b8cebe0e3e85907b8b6ebe92aada1946bc3217b9ac7fef108af60207f02` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/PendingTransaction.java | 1707 | `e3b1661e9ea18b73e0423eda6bb7c9fdd7b25890781588dcce92b9d609de7345` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/Quantity.java | 1308 | `216f7e264e21738e724804e47ff2f3248aaeed6d14f3d8923f54baad3b3a4067` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/RequestType.java | 2661 | `318d4215165177f1a1d2d7bf9dd790eff2c5f1b9a5f2949cc7a59f0eb3d0429f` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/Sha256Hash.java | 1332 | `ac4e3082214113467e0ab02b29f843d398b2b5e15579d0e3b531969d48058a47` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/StateOverride.java | 6521 | `5324f362326ba9d782b48d01f6e812794e1475c07409b71f727400e6f856a5cb` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/StateOverrideMap.java | 884 | `75ad285d4e1190721ce75b127ce1b1769000e354e68538d37b5c1d8820f8188e` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/StorageSlotKey.java | 3379 | `4c394803f0d02efea426604317029c8d90f4548993249c84b85ea35385938407` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/Transaction.java | 8797 | `05978662b89e8e5013722746a7d2f56d4649e2ea9beb12a8a8297e06168b9c30` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/TransactionType.java | 5861 | `4a57396b31b7587b4c2cba5823cc5e0d5b1118127ccd26ba19c6b9a9fdb158da` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/VersionedHash.java | 3055 | `90fecc0f1ea01e7f7a9db5b735353933f17f2d3476244ab5499e02152764ae9f` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/Wei.java | 5785 | `4a7518ab7df6e58413a1cf2323a441c3bdfe8830fedc5b45846f90deef033788` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/p2p/MessageData.java | 1171 | `8018257b2960c3f5ec2f6cf0f1eac7dad488f4697fb374a3d2c8b75a579a9373` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/parameters/UInt256Parameter.java | 1200 | `ab5aaa572e5fa03e6b1f9ed07b3139020b9b54f6c72409be3a6f042d997e9d55` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/parameters/UnsignedIntParameter.java | 1488 | `f021613f08d26c681a149561495cc7edc8a52b0250a0214858baab2532205e9d` | 0 |
| datatypes/src/main/java/org/hyperledger/besu/datatypes/parameters/UnsignedLongParameter.java | 1685 | `dc9ed8637f834f96df584a09455bcad3f11d602aad8bdd1c5a25f7b50d901f23` | 0 |
| ethereum/api/build.gradle | 6976 | `ba396ac602a9652357b7b962ca4ffd6a48b502548a15dae098ada08e650fee9d` | 0 |
| ethereum/api/plugin-api/build.gradle | 1723 | `f15719aacaedd42444d579755d7e77fc9d6e02c71dee309980beb7e36f618b90` | 0 |
| ethereum/api/plugin-api/src/main/java/org/hyperledger/besu/plugin/rpc/RpcConfiguration.java | 1756 | `d50af81f54fea55162e3a9da8bc6a9f20fd3135fdbb890c49a645b1a69ac9945` | 0 |
| ethereum/api/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/HealthCheckService.java | 5235 | `8319f86933e7964d8df79673a20e2bfd5552fd4b0c0a572b1661739c99f3ae55` | 0 |
| ethereum/api/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/RpcEndpointService.java | 3300 | `cd8931b55ea54e741198d7f8844f0dd6ebca9181c430bba3b11c58cf99a62ca3` | 0 |
| ethereum/api/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/exception/PluginRpcEndpointException.java | 2802 | `dd62a2b5dbac08c363596ae1d9322d5dd2cc3a7da12f1ab298ee2e9d3e1f866c` | 0 |
| ethereum/api/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/rpc/PluginRpcRequest.java | 1086 | `c4501a663d56c1e3ad25177c637b3406522d4c398b9828b8b677b63f63522762` | 0 |
| ethereum/api/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/rpc/PluginRpcResponse.java | 1011 | `bc98c7553f501f7be78a619bad3d219a12b9eb33232dc4318cd38ab0a578b9c8` | 0 |
| ethereum/api/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/rpc/RpcMethodError.java | 1812 | `d06ad8f6a6d8f2e30ab72e11d66f6918c107af7a37d9adc966b5beb5ed887896` | 0 |
| ethereum/api/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/rpc/RpcResponse.java | 896 | `4ad10c3ac312bcdad0f79627b4fcd36315e796fd563c3958d4a936d6f91380ab` | 0 |
| ethereum/api/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/rpc/RpcResponseType.java | 944 | `a6617f02ff5a29692a35ee47b7fe268d210abec9ad34c821c490d7e5455658bf` | 0 |
| ethereum/api/src/jmh/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/CompactHexBenchmark.java | 2951 | `d217687d7843d30fbedd78cfa9939fdc9746db9bf53b43f7e159214d3b703f92` | 0 |
| ethereum/api/src/jmh/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetPayloadBodiesParallelBenchmark.java | 6116 | `117bb81b6db976354ffb2a06ecaa1a2c8f6ae8d2d5b358c91057448e030662f5` | 0 |
| ethereum/api/src/jmh/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/QuantityLongToHexBenchmark.java | 4764 | `20ed0c270101e7974cf931cc5731c42fb8a7db1679d70a36cad7f9fd10384b57` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/ApiConfiguration.java | 7190 | `a502d8e4683a3c2edd5c81e167f0531ab1d6fa57cffbf37d0b527190b11ad9c8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/GraphQLConfiguration.java | 10177 | `8a38057691a13232f7fd478fd681f9180e4fb14ffe5cd7a16590749101dd99ca` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/GraphQLContextType.java | 1421 | `b3980ebd6beb58ca74abb1c72a6b26a00cc6d00e409c65d603744a0e97f7c15e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/GraphQLDataFetcherContext.java | 2297 | `15748b22a54ab2dc71b7ca003d98e7f8742374fc84c35e10154078021f193d0b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/GraphQLDataFetcherContextImpl.java | 4679 | `be24ceef8c1c219fa90a1da26f50a2809f28503c99a1274c8fe69b1257ae834f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/GraphQLDataFetchers.java | 22067 | `049c9085f2e103797833ed4b178eeeedaa91b63c717ffaa6f5a4438919c1711b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/GraphQLException.java | 1738 | `84a0d3e0fb1879fe3a7e5c3f640785e6da1b38e3ceabfecaa0f54e8ff6157132` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/GraphQLHttpService.java | 19086 | `a6f52df78b91aba98b49685cc588a092fd0933a3fe2501798b80810f292380f8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/GraphQLProvider.java | 5332 | `e33e3b1acd5355c5f10f0fe933476dbea96b6def7eb90cb808f1eff6b51b4b0d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/GraphQLServiceException.java | 814 | `dc31980ad1fc41d4dff459fda0d42f250a010ab8b06fc8e2f7e817ea5ca7d4f1` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/Scalars.java | 24803 | `70ab2727a9314848c13553db6ee15e014d8050050fcb13d7bf7bbf1316732b4f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/pojoadapter/AccessListEntryAdapter.java | 2101 | `53cb54d32e9675f49f3450cbec0be11e85c70f1d7cfbaf409363dd302ff48eb1` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/pojoadapter/AccountAdapter.java | 5080 | `def4c3111c8abfa5bda6c598f0c9dc1f48d33766d2d065a4566fa671bbbcbac7` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/pojoadapter/AdapterBase.java | 1086 | `0ac2c563c4ddb38fe107abc1aa617ae4bbb938c6a6e52eba5f096f98403c9c18` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/pojoadapter/BlockAdapterBase.java | 15009 | `969a11d3bc457ab1ef4861b8786de85967bd5e798fde4ceb1ed3adff3054efa8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/pojoadapter/CallResult.java | 2117 | `6c677d14f1643892d2c196426cbe9039b3ce8d10050e8e46ff4c0f7fe9d97fca` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/pojoadapter/EmptyAccountAdapter.java | 2047 | `22227c5addec1a190c295073c224c844af8090104a525cf1fff807d0f50d4bf3` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/pojoadapter/LogAdapter.java | 3763 | `fef6c6977e032d9571a7c160920acabb404f9f5282e39df9a8bc062ea1c68992` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/pojoadapter/NormalBlockAdapter.java | 6643 | `c782b8bb7408df9226831bf89bf31a639ba63020f310f5169200fff94caa3361` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/pojoadapter/PendingStateAdapter.java | 8391 | `c118a51518650bcb1cb52e0ea9636d913b12efdeabc570007a32d98aa0cf531d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/pojoadapter/SyncStateAdapter.java | 2164 | `e9551a519c6796b45645d7c65ab68536c05b6ae2189bdedbafc511cb4e370e13` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/pojoadapter/TransactionAdapter.java | 23926 | `01abe5557cd3782fddb3106836c0369cb2a7281b2d5bcc2d3f2b72b88b2c9529` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/pojoadapter/UncleBlockAdapter.java | 1649 | `9ce1f4b1cf25105dfba8b46d96dfc14edaa43ae4037d4425dd772348e65655a8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/pojoadapter/WithdrawalAdapter.java | 2207 | `539e4380db21d63f0641cc7fd98012d2335b71a3323276ebb01ca9008a2c723f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/response/GraphQLError.java | 6021 | `b142034ce330a07c2c2a20a42940b44d8e2a1915604c838d3cb057488a3b16a7` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/response/GraphQLErrorResponse.java | 1436 | `932044d987009084ff42063c8823445436269b4aab7e1442c81813c9c812e693` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/response/GraphQLJsonRequest.java | 2686 | `b474cb1a11e16d1b8271f015e78d60877259dece0b15fe8296c73262621af000` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/response/GraphQLNoResponse.java | 1263 | `3c7043629ae5fe36cd8168ba30743f7917c093621482a9d85e06e05c7a4be815` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/response/GraphQLResponse.java | 1872 | `bc1b8f994cf2563bfc4993e8a3f4d83f1d2c0e24ce68ce140ff2239314129180` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/response/GraphQLResponseType.java | 1054 | `d06889ebea02f8f996f8f77d3de35daf8a2e52afff5698c5e50101b323a84fbb` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/graphql/internal/response/GraphQLSuccessResponse.java | 1618 | `583d3e851c8ffde380a211ddc10c72eeb02185e0d1c489a7d57cca2b61b9c30c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/handlers/AbstractJsonRpcExecutor.java | 5500 | `54eeab35fabfd245eb825026e7af8aef8132a3c61d425aeb11908ce8896f160b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/handlers/AuthenticationHandler.java | 2594 | `e18b2422af223f9ff92610887f8b4d38996e3d453c1d14c32fb29e3202f0be8d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/handlers/HandlerFactory.java | 2564 | `2eb0c807147b55575f4fb40be78faa32ce95ced1594691e57843abb1c064f246` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/handlers/IsAliveHandler.java | 1632 | `042297da1207d526482cc5401433d69808efa754639bbfa81fcc69520da921b5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/handlers/JsonRpcArrayExecutor.java | 5073 | `7f2c31b10708eb67aa16e06eb2f182b97566088eb292306324e41f37afc9c646` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/handlers/JsonRpcExecutorHandler.java | 7148 | `76b7ed45498333905a6f6bb402b3af9bb97ef420f73b109ca9432d140a3cc338` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/handlers/JsonRpcObjectExecutor.java | 7143 | `aba623a3421a0b9af330844269c8ec6b74afec02a049f675dffee21dddba248c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/handlers/JsonRpcParserHandler.java | 4205 | `1a1e7bfdde217ef8773d54037b31c8bf0f03c568cdbacea8d7c631910cf5460e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/handlers/RpcMethodTimeoutException.java | 815 | `a53d03ff5b7560085bf146d6816ff1cfec39f796b58e6c1c14e7c0cb00fe2ec7` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/handlers/TimeoutHandler.java | 3222 | `73e799bba0224f2f630536a22f98a984353afcf690fb83b0a1b5ff71419bb5ed` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/handlers/TimeoutOptions.java | 1560 | `7caf179d46dd7c113bd83b26b934bafc7d8f885e7036088228b3b230efd4d2d9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/EngineJsonRpcService.java | 29966 | `3d05d12b2607ae1753223601be41e585e0f4b26ffce376ef95a83c3a8dca6931` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/InProcessRpcConfiguration.java | 1182 | `d4d510e4c493cedc21d4ce7a14bd929367a176a297832873af1695005505b2ae` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/JsonResponseStreamer.java | 4082 | `6364f10173bc0d738612f2035eb7a6ad13e5742fcf824e5f06f458f5ee9df226` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/JsonRpcConfiguration.java | 10678 | `3e23a4dfa53af3cc8b06d0a84eddd81cf4fb2dd1db25463cf040618ab8e2f613` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/JsonRpcErrorConverter.java | 3785 | `a2528596a558d9676f2237e36126a3fbb951e83647918ca8cc2d0cd8854360da` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/JsonRpcHttpService.java | 22395 | `ac5b56ae4794294008a3db029a3b2ff42d385ef91595a3cf7436d3c8a3e8a829` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/JsonRpcObjectMapperFactory.java | 4955 | `dff6c1f5aed6d30db14ed722ff19a8c9b4a45e4fff79159fe25e9313058c023c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/JsonRpcServiceException.java | 821 | `7cbe52dd8cd687a67a3f7b852d76918307d753a36732d025bd061ce49d398086` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/LatestNonceProvider.java | 1615 | `c9ea73bf3a1f9045e287391136a03513d864d1c17f7cdcb2bc091f0bd314a64f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/RpcApis.java | 1337 | `924d0595979e0cc578e89a1c6e8a72df2f4cfb63a3aa5c7462caa444baa72a90` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/RpcMethod.java | 9762 | `1fb6e7ee7ee83e3011335e241cb232e6b525f59cce6c231fc351edd7dc7dacf4` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/StreamBackpressure.java | 5205 | `7062bccccf365e6e0e487fc50caecfa898719e0c98d846e89abdf7bd5368a147` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/AuthenticationService.java | 1336 | `b4e2d2ddbfe0dc45b518a7ee69bccd1ec6bfbe2d2b46be54b6b95dc7fc7fdc02` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/AuthenticationUtils.java | 1423 | `1626741aa1eedd7f98a38753d20a9a0107802be78415ec46bcce8bd99bf8b1dd` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/DefaultAuthenticationService.java | 13562 | `bdc36924fe1041eaee8311defa354f3648b9c2ebce6c6465705473815527a9d6` | 1 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/EngineAuthService.java | 8628 | `933163f569f42b7af19eb1ccbc6c8239a68894f2176e1e522556dcb4eb3b7ff6` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/JWTAuthOptionsFactory.java | 5233 | `93d1f1d4de94c4e64291bc5c7f50f1a9d9c9a30e0591945008771f4e28a2a711` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/JwtAlgorithm.java | 1021 | `193da9a400368b7e4cba6f53acf39ef5f37924f34c5def46c43f467bf1faa7da` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/TomlAuth.java | 4397 | `e5bb79a3893ab05018e56f3a9b6bb70e36c2cc483c318c43236dd646025fc684` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/TomlAuthOptions.java | 1231 | `73f423b705c3d44f7f2d0b05d56bd29f6dc3e5b8f43722b0c061bf82edee8465` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/TomlUser.java | 2981 | `ec39b6749c1d4814705f8525ea8b29b5b8cb436b2ae0e7b5237a64307bb47daf` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/authentication/UnsecurableEngineApiException.java | 944 | `b4d5f581722e3d5e0ee50e2bf93a99f6b53cf7fc66dcf59358984d9eba97df89` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/context/ContextKey.java | 1064 | `9d6b7c86b4839f752b6e87821d883c6e48f07b1df496a74fa5dc52daaae83a8c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/execution/AuthenticatedJsonRpcProcessor.java | 3111 | `ecef60eb9948283a25df7cef6c9b4ed6ce4afa405e567758917075e48017f45a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/execution/BaseJsonRpcProcessor.java | 3280 | `07a489d4c84058815edcca84dd1b76b02bf45eab700c72dade7c488a0457a0fd` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/execution/JsonRpcExecutor.java | 7457 | `63c2770a33e8b2faa3e0bfff554897f91652122902d455867f0a1797e8a56765` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/execution/JsonRpcProcessor.java | 1693 | `8def238655478df769af8e7ca910bb063bc3b1f4ffef5c7490dddb12f63d45e3` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/execution/TimedJsonRpcProcessor.java | 2589 | `af7e42810b705191513f0180df55b93e8574ba2c13a1b43ae4349dc8e871bb79` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/execution/TracedJsonRpcProcessor.java | 6978 | `c46344fea4849906b5019287d22d584c6f06be4ae3a3a6b72f0c5f9df296ee86` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/health/HealthService.java | 3193 | `586731d1e5b9485f52c2d55ba2b6fb555ef18584ed328495e2d7fe21c41e9555` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/health/LivenessCheck.java | 1153 | `9f50d7339afac45fc5f78f4ddabab980f0076f174e830ea28cbcd608d7dc724a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/health/ReadinessCheck.java | 5147 | `8cf37ef35959021c71cb0dfb7a3c52446aa7983e6b8780c449242ffba9af5921` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/DebugReplayBlock.java | 4367 | `d2b5f341d620fc0859b627cd0b045867378ac9cff81fb7918427139d500ed047` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/JsonRpcRequest.java | 6440 | `55399c40705f3a66a03a0e74d992efb4f0bb6f033928e5199e516ffd8a1123bc` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/JsonRpcRequestContext.java | 4692 | `8031deed9e0f80787a2a9181f373b1ae3ba1e59eae68687461acd1c3540553b9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/JsonRpcRequestId.java | 2489 | `041943d9d7c36ca32e5b29d0a173874b902469e397280ea9ee885e88ccb361ea` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/QosTimer.java | 2267 | `ef4c39e0ea829bc93454debf9198a385043ed41cadfced50185f90a8eb3130a4` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/exception/InvalidJsonRpcParameters.java | 1336 | `f9127b223befefef051fdbbf82cf3312e1fcf3dc595ccea510d109e25bd6b28f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/exception/InvalidJsonRpcRequestException.java | 1632 | `89d1f08f7e63e894c5071261888849b209b369d903bfe7e00d886a44b86886ec` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/exception/Logging403ErrorHandler.java | 1399 | `c2b8cd9c792d84fa8e3fd179177172236ff65f4adaf48eda982d791ff0cd898d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/filter/BlockFilter.java | 1254 | `eaba697f263438789e0b1ce49adc88e9814a14481539da9a54fa59d375fa7281` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/filter/Filter.java | 1462 | `4c81977e45738a25f86957bfd9bfa1e174f15c335210d33ab1e2a6c4a5272846` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/filter/FilterCountExceededException.java | 1297 | `3804c21d8708de3d1093006714c7746998cb7dc68948459cf95d5b42be70580b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/filter/FilterIdGenerator.java | 1141 | `2bec4390b8c042c516669aaee85f01daaca0fac7c08d6b583b5b69bba293c863` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/filter/FilterManager.java | 10693 | `cb2e6ca9218297489ef921c0d885dbcfaaab3b987fa6d1ea64468b821eeb39ed` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/filter/FilterManagerBuilder.java | 3505 | `3c8ca030a0251465348a875a7ba6d4709d89e0d7187dd37a529ad5351800a220` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/filter/FilterRepository.java | 3127 | `27b571acdf46a6a1d3ac63722b48fb844e81d11e732fcd483151d18d65d0d9ba` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/filter/FilterTimeoutMonitor.java | 1132 | `9a311565e813572920a6e65b63cc6ab22e6f216cc74707c354da4446e402a4d4` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/filter/LogFilter.java | 1879 | `1feec965303fc2df98cf3b54bca6a741644f5f2ad22f01a4789495e33bdcff51` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/filter/PendingTransactionFilter.java | 1347 | `f03cf8facc545b8ba688f2b4503c285b0eb6d05d74df8f0e86aa90d5ff810f0c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AbstractBlockParameterMethod.java | 4462 | `cd300a1006daa2607488c4ca3d237d5fceeb8e88b49a72d184d7c9a9c5be1152` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AbstractBlockParameterOrBlockHashMethod.java | 7768 | `0b41e021e7457b026ee358ea5d1993a3262b9058ed7ceed8de7227573e38bbeb` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AbstractDebugGetModifiedAccounts.java | 6671 | `31b7b2f18780615f5c4bc9b78d2c4025037ab20203858debce69a21f0832f5c4` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AbstractDebugTraceBlock.java | 5846 | `94de33b10e55ca1d3a2b5b149794394198b27e0f50d8ceeb8572ac41c249fb52` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AbstractEstimateGas.java | 15264 | `c44b08fc8dfdaf96fdde78eab5fa0217f7a4f74dede0235351a4797aa4a5a073` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AbstractTraceByBlock.java | 6011 | `f68e192788e29ff3761b9984894e81048f3d6ef3de0580e751662d57dcf1292c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AbstractTraceByHash.java | 5524 | `22aa357ce3f0479844b3f36da43cabb7c4a730d6fd3fb009a9a1c0d35a7ba5b4` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AbstractTraceCall.java | 7641 | `ac9cdb9540aa315227f4270e7fce606bd08939c23d4e2b56b4eff8fb4af61659` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AbstractTxPoolContent.java | 3857 | `1147b9928ab91f367c1d19df47546a846dde707992fa38355a1a699a0ef862e1` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AdminAddPeer.java | 2646 | `ba844b88a3ebd3a7bfe8155ebf33115475b518969fbf4e53c5afc015017b7591` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AdminChangeLogLevel.java | 3579 | `b3d18f5a7f502a6135248b04abfa4c0840a1c5290636aff1553835f5226cca77` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AdminGenerateLogBloomCache.java | 4726 | `0a1dea38c788b697fb110eabe36a73f93d87473a85e3b6e968a879da8f03e5e2` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AdminLogsRemoveCache.java | 5241 | `86ac35f52354f5d8caa56611bf26a868d3f81abc4226e2d2ea4ae8fb4d30004f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AdminLogsRepairCache.java | 3266 | `8acca55f24b5cc69dca795ec62cf008cbd2fa1a99f2811ec3ad9cebd9d2feacf` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AdminModifyPeer.java | 3604 | `166bdcd1942bc051a173f80bd0935a3bb4410d0605600d87ae5bf1ab90289c35` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AdminNodeInfo.java | 7959 | `cc08dd3889276f3394011e2d7b26f8937265083509f2da8c9b071b9edec7ad53` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AdminPeers.java | 2327 | `e7a43c7c7fe54d83ac04cfab891c13af947f51c1eedcf9c426b257b3baff1ee0` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/AdminRemovePeer.java | 2203 | `f0bcf8d8bedaad4bf3b50804d9fe0a70fe70f536c8f078b799fb6b0d4267f334` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/BuildArrayNodeCompleterStep.java | 1249 | `f22468b77b991368f8b827e528ba35080564ce5a96ff3bbd242fe707e8915539` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/CallParameterUtil.java | 5311 | `3ec253f694470468191d204bdbbee92badabaf4f2b23fe92800dad09ed02c120` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugAccountAt.java | 7929 | `5bc68a6579dbc4b5a8e89d1477789b9d625ea4ae77e1d37df04d0f587a65edf3` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugAccountRange.java | 6367 | `1f0e246719f38fd8133b4b8ca0e7aeef7d3c1268338efd0bf469e3f22f100c98` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugBatchSendRawTransaction.java | 5132 | `8441bd12cb75b886bf034965b8fe241b5d25f82a79b4179604b02bf49ac4ba45` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugExecutionWitness.java | 10144 | `ffe1e1bf76854ca1ad1c87ba34efa48e6c49fae006a0f13780dec266e01be1f5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugGetBadBlocks.java | 2564 | `40c079e82075396273966b2f78069b84ffeb757b276266b4552c9831440aaa05` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugGetModifiedAccountsByHash.java | 2232 | `c39cc1b8976e691250025032ed58adb1360693f2c057bae8d68d74a825c5aded` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugGetModifiedAccountsByNumber.java | 2599 | `6880ff29b85d75d6b914f8acdf4e5f75b9a60a62f6582578b62c1dc8fd4f5337` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugGetRawBlock.java | 2566 | `f942b0a99954b1730cc79bd2b99556498573e8d035bccadbcedfc94212616ecf` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugGetRawBlockAccessList.java | 3580 | `7d79145b0ed96037ee74a630cffdc3dd26f78dcb2a46e5bd4e80e71cbea594d0` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugGetRawExecutionRequests.java | 5249 | `9874a214690d46a607a6e5938711209f34cf788dee3ef7240115dbd10ec318ba` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugGetRawHeader.java | 2553 | `4b14bb89d997c356c1d0312483f56896b4386bc87a20cbde6a2a3d7245c22306` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugGetRawReceipts.java | 3576 | `8786fc379ed381a0dd616e942cdab8e1a151a7b843a1af2453ce0e361d6a9178` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugGetRawTransaction.java | 2791 | `c1727443c72484fde6b8f5e040c26b8c855972a947df3fd129912f53c354d642` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugMetrics.java | 3843 | `e6ecb1b80af7889f2362db94cd03f56f840f77b606c9f5c87dab9d91cc7dc99e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugResyncWorldstate.java | 1910 | `e8c579bed167fc3d8c606348d2cb4a3f3ada44fbd73e14c745de052d77639565` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugSetHead.java | 7420 | `18aa319b22c76c9409d039ff5289b5f38cbbea36f8a163b6b41335764ee80817` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugStandardTraceBadBlockToFile.java | 3836 | `8622468cfe16373806f24eba7504dce9994477669bb78c51c78555a8db477449` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugStandardTraceBlockToFile.java | 4754 | `3f1e94188da62f7cc43b5eb3645003818dc62d7880190c45dce86ee167329d91` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugStorageRangeAt.java | 8324 | `2b2b32a35e85d5084c777cf19d47c9624476f0962017342498d538a0b28526ca` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugTraceBlock.java | 7135 | `91043f7e55f9d2ed1b458dd70def81546381bd22904d6d352833a0a7a62cad3d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugTraceBlockByHash.java | 5181 | `b41a35a90769830c67277f739504aa589d63891b0b376ed0bf875424ffcfb4a8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugTraceBlockByNumber.java | 6045 | `15ba6213814a57858b6414e22b093393020325a4c870f87f232659334897c374` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugTraceBlockStreamer.java | 21670 | `97d7281a32beff2532fe343b6759dc4519939e4360680a2f6ca0076aec6ca53f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugTraceCall.java | 6589 | `84e14f6a34094c7927a8f02099b235d06690b4e1d7040c41d00fee8ed8345ea1` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugTraceTransaction.java | 6841 | `7c8b7311a9f066276767cfafa2fd5624f36b18cd2d2aa604c4ef50414c4a32bd` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/DebugTraceTransactionStep.java | 5971 | `c4f38614be998ed5c5925971bd4d6ffc54958e1c3713a4acd01d932854a2e051` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthAccounts.java | 1390 | `1d0a6cd7afc02c12b5ce500465939c2b537ba141fec1956601101df53714bebc` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthBaseFee.java | 1756 | `4ff2b20908774fefe2d9320810a8b36daac4642d87681d5200fa5c39aaf1a7cb` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthBlobBaseFee.java | 2449 | `f05a04c945429cb79f75ea0770ac3a50c2a09122ac42875af3870f5e84db2321` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthBlockNumber.java | 2085 | `32c94b06a18a71e5d0e1b8d690b5835c3275f5dd7d7f2f4e9fc8d12e80c72157` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthCall.java | 8146 | `9bee35fbab58e4c85db03cea2aa6a9cb623cf43807dd9677da7c1501e41898eb` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthCapabilities.java | 3607 | `e92f3c436602ece8b56bfc0dc30f85801c0d089356d35f2c102ef49c16d96d60` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthChainId.java | 1653 | `275252bf7d4a8fc6f0192a9166721f3e61d5c172feabf75e1c9530fe33df9cbb` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthConfig.java | 6352 | `1c9fadcd5e32dcc23e7cf054b499079287299760a83427fea0fe834079b16eeb` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthCreateAccessList.java | 5842 | `7fd961efe1d935570f4c487424def1254b411d00becf447d179dab49d9830288` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthEstimateGas.java | 6382 | `eef61f993bcf9ec1271d1de23652d9abaf031c7f608c8536a3f2a8f51606c7cd` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthFeeHistory.java | 26360 | `23d23838a8800d0d0654664a43723a34dbe3d520e5a25d4e9fab9481bd91903e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGasPrice.java | 2959 | `66acb8ce8883ad42f9111830ccf8a5434a054cd8c7628fefc19e50fc5c56424a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetBalance.java | 2613 | `708796058080eeb8b4b5e775fd1f2f4985feba50b0af33351d3f79102ae4d30e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetBlockAccessList.java | 3435 | `0991a7b565fe1d876710456b9c3f9fc002688c777c6b12d6398213d9a06b3319` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetBlockByHash.java | 3954 | `320843223eeac9ca7f5c7ce28f839b143d54b7e670872ad927f54e80c701b740` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetBlockByNumber.java | 5439 | `5e111079ae2d5e080ed95edc92501084cadfbabd9b5413832660bbb499b7b318` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetBlockReceipts.java | 3952 | `815022b2db8c9f2fb254a90ed36eb4bca27c33523de00d051cbae6665cf2886f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetBlockTransactionCountByHash.java | 2590 | `4659872529683e243e61e73e9d597e239d62f0b2ba48e4d4763c82e60e27631f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetBlockTransactionCountByNumber.java | 2273 | `3d12a0593b3a24361746e1d7fde250729c0f5f2570457b96bd9ff3df541c2ec5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetCode.java | 2520 | `bdfdabc5fe8e4761d2d88391ea636dcff8c32bd085a8bb9c8d951883ebe50622` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetFilterChanges.java | 3368 | `0acf20357a732f6e919873c309f1c2fb9eaad70df5617b7071a43231690502c8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetFilterLogs.java | 2758 | `b6701f984851738d5224004f9cae67affaa60e1bed7e2da72154d7c09408cd77` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetHeaderByHash.java | 2592 | `d45af6f4421b6d82f4ca7aefe550afb1a043b5cc924f0f58ab6bef3d76cdb226` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetHeaderByNumber.java | 3499 | `e756bd1b95b4f5c7f1cc480ca6e90038969f53bc6e1eda0789c6281ad498d48d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetLogs.java | 7168 | `4bbd97104449e3263ab302532f59adbae3fb2b741c357d8a27f83c5fdb34451c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetProof.java | 6789 | `d602ae38718cd90bc2113106bbf72c27ff3b302a19dcf9f16a112b6561d7f270` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetRawTransactionByHash.java | 3789 | `3658a945d296e11d3fc6f6dce70118a0af5e6524c7a04441ae8d65cd576e3e24` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetStorageAt.java | 2826 | `700d162d08a60924cfb5e8266bcbee5624bda36232faa3d06558bf2635ac1552` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetStorageValues.java | 5551 | `501adc0023c710ec59eef0f5d2ae9567a9a17b53fd9beb16dd2c0ae38f8ee20d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetTransactionByBlockHashAndIndex.java | 3196 | `4099f345b198261485115d5b7dd16fee730667ef54e5700747dbe278f86d310b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetTransactionByBlockNumberAndIndex.java | 2938 | `f6a6bbb2b57f4ba573e6da49834001e9137bcf0f390dcc8c7775e06551e5862d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetTransactionByHash.java | 3440 | `2f334dece007a71ad7456397d8cf3e68438ce96cd2e87e28db7cecd66872929f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetTransactionBySenderAndNonce.java | 4112 | `8f403165e69452b5ad088f30489cc700d9861cff3e2c24ea3cb922f19066bdb2` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetTransactionCount.java | 3881 | `e689d71bc00a31031c06e9f31ed69ea06381e43aa70e56a6db185d1dd4c8a6b0` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetTransactionReceipt.java | 3435 | `187c918595b233665283b19d6d8e0050832a2384afe2fbdd2a3f4138209f4eda` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetUncleByBlockHashAndIndex.java | 2979 | `cf044897685c7a3ba732cb8428ab2e76b1b5fb98c6c4cd91f2293daf092576d7` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetUncleByBlockNumberAndIndex.java | 2738 | `1f655588f5509314b62e6878c5aec8979f554c14956579c4ddb54fe45cc080c9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetUncleCountByBlockHash.java | 2387 | `d90338fef30617347a7cfc24f9769cdfa2e1527422c9781401f303073943e83f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthGetUncleCountByBlockNumber.java | 2232 | `6d78792d51e3f13399c37255429dbae63e8cfb8c1a10bcdc4ae5a3349f172299` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthMaxPriorityFeePerGas.java | 1913 | `74935e8c61a0bc331f68b995f54e28785c7e7e86220078ff4cbc8572405c472f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthNewBlockFilter.java | 2094 | `66ea37abd8fec0e5268db3282591986f4493d2927db65bd4e5e1bed408d54723` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthNewFilter.java | 4294 | `ace9420b2da51b0ed51ca3949bc7f415382efe1dcc8b0acbab6446570a4ca168` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthNewPendingTransactionFilter.java | 2147 | `cec85275d1d4024cf4d4cc120298faea9df5df39511d9f705567828293d3342b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthProtocolVersion.java | 2080 | `a4d2af66c71aa48c117d136cb151b72f75f4d95ac2f2f1a45b680d6c617cf107` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthSendRawTransaction.java | 6433 | `de727958ce66b66d5e790a3921597901746830cdb29033c58cba560db70ab16f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthSendTransaction.java | 1471 | `d626dfa62424651fa523cc2dbddd2deeca269af62c47346380f72f76792bf816` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthSimulateV1.java | 8105 | `1d36edf91101dbe2be8e0a6e87180e42fd01878233a8b82410e6e598fc0d0cbf` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthSyncing.java | 1917 | `1af687d9f81fbb065d39f8e0470dbe7478eddf059a63068851b0ebd2c2cf499d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/EthUninstallFilter.java | 2211 | `c94708b20ccaa67936afac9a9c1c2a5a9bc3a3c34883fa277747b5d5e80c9172` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/ExecuteTransactionStep.java | 4889 | `99377116ebcfc17993983a43f2a6bb2baa0cd58fac63baaa273dc28f4cdd0096` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/ExecutionEngineJsonRpcMethod.java | 8603 | `e5f4ac6306d7730f7d8e0c74bae476566f7a7295fbd20a6564d63960bae62ae9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/HexWriter.java | 3588 | `17f772e94de777485db825fb4ab40e30d38aaf1e0a1e350a40754aa0bbe38efe` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/JsonRpcMethod.java | 1853 | `5e1f805d32d6bdb9ef325d485f319d1a85784c0b50704782fd259bf0c202783f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/NetEnode.java | 2493 | `f2ba5837303096f31afa14984436031df421248bfaf50733acd836539d2a5f5b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/NetListening.java | 1560 | `346babf2b70d4d1c642cd90b8b47e5e787aa42531c7c8790c4ed8f8ce56d65dd` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/NetPeerCount.java | 2085 | `6c473f035d82bd42e65a3d02dff673fa5ae8c0ea214b8ba043c934347cc1c37f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/NetServices.java | 4159 | `d9ba8f75f231641e677ad9bb744529c0ae83f5cdc99fd6891521d7147478db03` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/NetVersion.java | 1800 | `39555faaec9d906bd4467b2e69cf43720fdc9b26c49d813c563cb9e897a669b9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/OrderedExecutionJsonRpcMethod.java | 6451 | `022c5682812915a57d5858000008e49e465eeb8cc1107422710bbd0389f9a48a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/PluginJsonRpcMethod.java | 2381 | `2e4deec4285fac6256c2222ce4f731dbcf73624515c6f24c55ad3f93bc4e4d99` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/PluginsReloadConfiguration.java | 5288 | `9570f1ede5232ad9c06baa1c7b1563452e6de8bb07c2d8b27b886d587dda33fc` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/RpcModules.java | 1752 | `2a748803062c04dcb9e9873d92a95c2d8383c88c694a95133d09b258306e6062` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/StreamingJsonRpcMethod.java | 1893 | `0a53ee2f976d894c0dd007686631db163558b4482db9bc90266d2e57949b86de` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TraceBlock.java | 9465 | `da69fc39b62cbb13d4a0127bc4b980ecf3bf5654fbe46e4214c5098937af7f55` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TraceCall.java | 5692 | `8952ebd493fe26da7c7b46b89a73d8c8af98c530539d487338ae33fd8a5d7757` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TraceCallMany.java | 11326 | `1fe9322fe6720127338c7757102b4eba48ed161df0d633d73f4fe2c72bb8f71e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TraceFilter.java | 15178 | `9b1e0b11753cd836d662dc54deca4362bded0bc21f9e2a03a9b806d6fb774d5f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TraceFilterSource.java | 2823 | `6d86abcd8d4e9f026a817b4961ab46ff0644bec9745d3df7e83fd9dfa7248b9b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TraceFlatTransactionStep.java | 3536 | `4fe4c987d78d48c547bd7e77c27a205c2a37405b41e84137e613decad03c1224` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TraceGet.java | 4747 | `bebc06f8cc065ec1ffbfe4cd2e23259b7a2facabf72cd8aa12cf0661b5710f90` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TraceRawTransaction.java | 6802 | `434a15d37bfa8c89549558493e285815b0f43a7a1f90abe58dba6f40a839f146` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TraceReplayBlockTransactions.java | 8906 | `ffb693b58542262b2ac7c2d33ee73a0e47397d7f8f62b21d46e7402ec86d95c4` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TraceReplayTransactionStep.java | 3449 | `6f2c89ac30b25bcb0c625a26a791353a594efb609491e7712c5545af0c6c2bd8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TraceStepLimit.java | 2142 | `e9e017c7b9525950829a7bde2425ab795a1dc6a6f281c23355343f946bb45e6f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TraceTransaction.java | 2871 | `e9331ef48856c83cf1a36031788543f10263c45f29362d2c3873094c4f7ec32b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TransactionSource.java | 1648 | `2a3cba76f068aa0f9bb1cee3f49ccc0c75ee8bba0841763410d6ea3420e02939` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TxPoolBesuPendingTransactions.java | 4238 | `9fd3a5dcb1a42138ebc27b4b6798d37e09dd21fff54d1c6d5b0740511c905bda` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TxPoolBesuStatistics.java | 2299 | `b758f7b83299ce3130a6b800c1655ffe341042a438e7cdc5f903a041c6b3ad65` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TxPoolBesuTransactions.java | 1878 | `8987c523a4d6fc16b5c6dae54bc616c095cd64da6bf3fd5737f7cd3ca72ab7cd` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TxPoolContent.java | 1958 | `ce913081d68120c98f5b8c2f283dacdab8f86d79e42d248a1b989d59e2ad7b47` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TxPoolContentFrom.java | 2837 | `3c9f4ef613191f222fd34bd1e82567fc73bed295a6e78c61105ad9e30bd10f92` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TxPoolInspect.java | 1899 | `df13836976a520ed55f540e11c727233f4e89194a92ca9e4943174d6584fcfab` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/TxPoolStatus.java | 1972 | `f95d944189a2ab6d5221df43740396bc3bb3cdffdc23c1c4f5b8e6cefd90d00a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/Web3ClientVersion.java | 1499 | `d79ce6af9af61abca38470b9e153a4ef6dda25c3bd26302c391b16f5bf1e2909` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/Web3Sha3.java | 2825 | `84499e9caf25fc4bd3d167e96957314563f6eb7f4e891acb83f9299334b44488` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineCallListener.java | 815 | `ce9181326fe863669cd6e7faa8b491e595489e1ce400a620b9b6e2a0a79e9eb9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineExchangeCapabilities.java | 3497 | `b2093c57614ee452eba6e950576466c3d9562ad3d2908a5ec02f96c319c5d98c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineExchangeTransitionConfigurationV1.java | 6851 | `821a807c6a5c747716057def8b11cbab2dd1276f389da2c9221b03ba246db02b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineForkchoiceUpdatedV1.java | 22232 | `0d9cd0967aed5e64895c4c1c854de50ad20e05083698182db8c6708eba5ff1e2` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineForkchoiceUpdatedV2.java | 5195 | `b6b14435c67fb96a70f810455873f57d53f16b46cc66cd1b75916e08f5a4acc1` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineForkchoiceUpdatedV3.java | 3697 | `e102d44148a7d17b5f54a9101d8e0fb353088bdad03dae2268b42e255b206269` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineForkchoiceUpdatedV4.java | 8130 | `bf45d03ac94372bfc19fb7edfc2773cfe0bbdf603ad7c77d0c80b01b140ec3a5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetBlobsV1.java | 8534 | `dcbe087cda633459baab3b2225f2c03f5a36066a09d7f99b906daa9abd47ac7f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetBlobsV2.java | 3354 | `ee342c68777ff87d5ba923699f84289fda8e4fe68802b034130a1a882a1de7c0` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetBlobsV3.java | 2501 | `ba58aeec89ac849988bcf8c4039fc396c8875bbd8bc8f4c8b2e093b47387e1a9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetBlobsV4.java | 9770 | `1d0caadd618d53275b8664fbdad187b2d61fdde781e5e80ff74d4e184cda4c02` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetClientVersionV1.java | 2432 | `b906be65fdd3b38c3a825976990d7cd73859a057e499038409dcb96888393ae6` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetPayloadBodiesByHashV1.java | 4652 | `12c27d22563540076a20135055247e1e3c0ef23e2b41ca30440c79ed84a57dcb` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetPayloadBodiesByHashV2.java | 1968 | `6437482603deefe9bae23744b6d31bee8344b65d0719e9cc5802f7baca12679a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetPayloadBodiesByRangeV1.java | 6112 | `290e257226497b51e43589053d5e55769ae0a609facd7ff8eb40696b1177757f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetPayloadBodiesByRangeV2.java | 1963 | `9578a4944641700ef5b2775788d7683a60326daead81ce67239a4ea0309b8142` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetPayloadV1.java | 6921 | `8894ac8287b56d557747ea4261adef5a94ff9cfd2610d82112200da72b08ac92` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetPayloadV2.java | 4116 | `b7c146a44f3b22bac4bf55fc80eaf0203847eea053b1a516090c390b10b4be75` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetPayloadV3.java | 2661 | `99e18c80228c6cd64724079edc41d3614b3621f1c66344d47c181d8d6935fcc9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetPayloadV4.java | 2194 | `b5a981f0bb1e4b37160b0ed7c00ffb60f4cbe9987dd10aff3637029eb4c38915` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetPayloadV5.java | 2259 | `09dec6446dba0828bb432df59afdcb4e5d788eaeeb6a84a16ff92f370dfcb6d1` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineGetPayloadV6.java | 2803 | `90b28510c6c91b39438db244d39e29f2d0a3d9aecd7d19221e7e8af5d7d9161b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineNewPayloadV1.java | 30691 | `975b11ec5010da00e0a119be5574abf5e68f68d48179a80e94b26ce8918adb09` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineNewPayloadV2.java | 6854 | `214533e8ca1c3812faeca097179289d80728242485b2501488243a702bd0f5f5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineNewPayloadV3.java | 14819 | `44eb518cec6f27a00cb90bc2435488e920bee272a2a3cb5fb1148b97cb6d3622` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineNewPayloadV4.java | 6701 | `a8e8419b10120bdc67a636c44025fc5dd4187ded9d4f3443c5e076fd7308da03` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineNewPayloadV5.java | 5937 | `da2612ea516522ea9fc50a08e15bb0806162da5864d7a4544693ebd397edb5e7` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineNewPayloadWithWitnessV5.java | 6265 | `4ea8e2964c542e94720c4866a1ab5f5ac64748a74f499d8aa66b30559ede56a6` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/EngineQosTimer.java | 2011 | `f6a8701e27cb08b9abb47b52b4c833ac3526eea3a52e5306ed521a6740c36233` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/ForkSupportHelper.java | 3213 | `7587fef44dff8ec4a49fe9a38404586709a8e6e2ddeabb2411d09f0687b1f3ad` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/GetBlobsMetrics.java | 4738 | `a82e8d8686ee5ce47fc699c59c76cc43a078695923acdc6df19f788116af12fc` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/RequestValidatorProvider.java | 1601 | `6397fa5f5c8aa5ecc01bb17b079a00752acb1d2868025410a33b627ccf1ab6f8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/SignatureRecoveryPrecomputation.java | 5272 | `3bb76b02c464e141a7303dd7e6ce5d373eff29a77f102f5e87f4c41059a248d8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/engine/WithdrawalsValidatorProvider.java | 2137 | `18f82d3290c2df0a88f4ad9abbcf55185539d3ccc25f94b34b572d4dc85a9f38` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/miner/MinerChangeTargetGasLimit.java | 2852 | `0e44d94329b69615e380ef1ff6e7d70463f96757080b37ad8f968994854d02bc` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/miner/MinerGetExtraData.java | 1768 | `b0067d2aa345b4f18c2968573b7ede3b23d82a7a9b589a0ee1f67559752be52d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/miner/MinerGetMinGasPrice.java | 1870 | `84bbdf0406a62f954b43751fe3b50117b1b7ad57666c350a938f9e4b3f2fc41d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/miner/MinerGetMinPriorityFee.java | 1877 | `89849a197c5171762d0191e6a0d8837ef8f53a5aa7b4a1e7b28a096c9be6270c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/miner/MinerSetExtraData.java | 3198 | `004999d23c88c1b8a7552eff925175640412c8fb465e6e06b2576e16b2236bb3` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/miner/MinerSetMinGasPrice.java | 3139 | `54f4b6fa75d2ea9f32a93905e42a7c5be736c2619d0327186e71567bf9724246` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/miner/MinerSetMinPriorityFee.java | 2866 | `66b558764caee29d03eecab95d473ce5a1e1348993d292e2480af370691e9d3a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/permissioning/PermAddAccountsToAllowlist.java | 4240 | `e03c0707fe7dcf52d08ae45e668d89a5e335aabf529362e5473361a78df98bac` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/permissioning/PermAddNodesToAllowlist.java | 4980 | `fbbd367f46fc61d7ecce87445eb8d5f3299e5289d5cdf33c54b9ace4f6186dc1` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/permissioning/PermGetAccountsAllowlist.java | 2269 | `4cba282f4dbf349d51f8c8c09ca6e4086513c9fefeb0232563e971603c981ca0` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/permissioning/PermGetNodesAllowlist.java | 2692 | `e84824eb03c8a6cb945cb99c7ce6fbc929979eafd96e7289e9d809adda5b23e1` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/permissioning/PermReloadPermissionsFromFile.java | 2970 | `288cb4d45d277461cb8716f7308628970d6ed0215a5e489e6e74b9ce23c36588` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/permissioning/PermRemoveAccountsFromAllowlist.java | 4260 | `8b27aff29c3c3481573066fbab91554c8880eb35259b9e1d28f828d3a058489d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/methods/permissioning/PermRemoveNodesFromAllowlist.java | 5207 | `e3e416234e5e3a743baf33021dd812443cf4295a7396eb0076a2c1d2c03616f5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/BlockOverridesParameter.java | 4113 | `4db23b9a0b8e9c30c8d403d37928e2c3d54634bf958fcb1e868c26b5171ed814` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/BlockParameter.java | 4770 | `4f0dfdd9242c946cab000fd461e3a305e79381574f948d54543d05c3575881f1` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/BlockParameterOrBlockHash.java | 6469 | `208130e2b9df0c39e2e153d7360d2851a19755be386bd285edd2d3105e7fee9c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/EnginePayloadAttributesParameter.java | 3640 | `dec595314269b0149b6b66e737fa807ea3b3b554c82101394dd5881a583dd83e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/ExecutionPayloadV1.java | 6372 | `a9a9eae6a5b2f7e8586b605c2f82d8f80287b99d92fd1b65289145a2a29b879c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/ExecutionPayloadV2.java | 1967 | `704a1672c1feebcaf2fd185bb5c4a1e509acbbbdbafc9eb24e37e8e585d8a6e4` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/ExecutionPayloadV3.java | 2686 | `a8624b31c347a77311e2de42182c1be882b46cc9ae0ed1fa214510e077885e97` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/ExecutionPayloadV4.java | 2785 | `3b2bfb9962d60216fa8dc5aa2023deb9d391f969b16ea9a13dcfc9aee29ec5ff` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/FilterParameter.java | 9417 | `0a8a5153e993060e28fc02e413082906859c2320582bc7978c785081a8354016` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/ForkchoiceStateV1.java | 1805 | `65d6e40d83417a15d0dccf19ffbd2d0d38c191a819c33504f80c057c8ea07b39` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/ForkchoiceUpdatedRequestParametersV1.java | 1665 | `26eea077dc98f0682f2c8db0a023e12ff9de62f743e6af279e459434efd92f3b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/ForkchoiceUpdatedRequestParametersV2.java | 1289 | `b374669e6f4a48bcb45845dde87481a334f96e028a6159938f26cdbc6cff1d15` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/JsonBlockStateCallParameter.java | 1684 | `e8d1d5b9cfc288c46b8cc7172b04c69325f207f6716544b7cb9198f341b5c395` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/JsonRpcParameter.java | 10991 | `8ccd4954e081807215d2b26a3c8c5c2a192241a9022b6861454500b330819d81` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/NewPayloadRequestParametersV1.java | 1051 | `a729d9163d83fb9141560ce43a79518807bb0133d786bbd753f34bc8bf05725a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/NewPayloadRequestParametersV2.java | 1960 | `9250282d7e60976fafbab1c288c935084902e37f7d8f31b7f8437b3497372cf9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/NewPayloadRequestParametersV3.java | 1281 | `453ff7c81d9a0a56e91cf81d8f9abd56ac290e7c5618027ba11e27c7c147119d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/PayloadAttributesV1.java | 2064 | `b97230e7bc64a1e3ef8440b7a79ef67e763ffd4bd6215a609acbf5fa394b7202` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/PayloadAttributesV2.java | 1522 | `a52a5f564d6a54f193f86d68fc97ffd126f3bfc8688e1e0707d6d591a9478108` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/PayloadAttributesV3.java | 1758 | `815f223d7737c3f821779db85b607ba714a70a35ee1b10c36aeef9bd2e776851` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/PayloadAttributesV4.java | 3024 | `b11df67eed5e1d20044674c885d844f50bc0497dd3fa772c380375067f8a3b54` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/PendingTransactionsParams.java | 5584 | `6c62732c2f0fad528863f6783aa0e53dd8a87e757ec29b5884533e17e9218c31` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/SimulateCallParameterDeserializer.java | 2363 | `f7d4ecff3fd9cef1c18f2ab7a82bb44c466e7a0014d46f8d5ff71e86f9ab02ee` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/SimulateV1Parameter.java | 1735 | `aa0949df1ff5be791496ac933c9e4efd94fa84140c54ab117919adf779608405` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/StorageSlotsRequest.java | 1074 | `f0e75a8d1a9ba8bed032e7d4d63ea6eff7587e7b5ecb17979ce3c775aeb24358` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/StringListParameter.java | 1112 | `d9915e216f731f22cf56ecbec87f5e18a00852a68ec98ed0735dee439fbdaded` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/TopicsDeserializer.java | 2395 | `b6adc0aeaa761e169b49ab9f010d30e1353cff456fa5a12e808480ca69d85c75` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/TraceCallManyParameter.java | 2362 | `1ec928d1254c1385f7ff486d7e6578bda3baf2db42ef443387b3ad4a16ded477` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/TraceCallParameterTuple.java | 1301 | `656b2a10d783422f7a2bf1014dceaf1299432e081145862cd10cc54e22dd4796` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/TraceTypeParameter.java | 2668 | `16f7f37f49429f75073ac656832f9d964bbf5c7ba6d350fa0f07fe7311d987c2` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/TransactionTraceParams.java | 5465 | `7016dd03bb9ec6f6109f325604ce1752b9cc265002d8a3f76c3905355e78177b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/TransitionConfigurationV1.java | 2266 | `d63cc47defb61f9b8fff22ace26187903316f83958c1830a943d688cef5f977f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/parameters/WithdrawalParameter.java | 3633 | `d71f7486dabe8b605ae8b5147d5db6ac3387b328c211e73d86816517ce367a26` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/processor/BlockReplay.java | 8438 | `650dbaebfd4737b13d9a9c4ab9ff706f427d4802036d0900545e203f94102ca0` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/processor/BlockTrace.java | 1018 | `d2fa327f3db5c785776461628c79083e6520da9347cc827440dc8363f956b8ff` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/processor/BlockTracer.java | 3386 | `6fe394a06941cf8c6bedfb2d07e93c6a94f009272f38146c5f2f381f2a3f991c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/processor/Tracer.java | 3683 | `87b7c66d770c8d7d9440552a1b8df8fc81f5a401a9dd38ff9d3c02901f5b5e44` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/processor/TransactionTrace.java | 3050 | `7e962f507dbeaf76af588b23207da79825b97166870aed9405f04717c9e8067b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/processor/TransactionTracer.java | 9893 | `83ad553f1d01ded5e1834f83c6df082a4b943ccfb3d2049310c67eed6cdae7fc` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/response/JsonRpcError.java | 3548 | `02ae6483362f16e96a5efc04c94eff4a1bd237e5c59910e47175af1f66bfe748` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/response/JsonRpcErrorResponse.java | 5900 | `abd2270ac9f199fe768fda604a7ddd19ab6582c18ea2cbaa9ca30373fc3708e2` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/response/JsonRpcNoResponse.java | 906 | `00937bbfcd3beca681eb8e4cfc5113c5ca4877d66b387f5ec03a3bccdd5b1168` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/response/JsonRpcResponse.java | 943 | `f9f62a4b7089a15edcb50adad00d8286297711f545a4e03ffdce85282d6137bf` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/response/JsonRpcSuccessResponse.java | 2066 | `4d547c8f31669ccc9185e5922c06fd569d587528cd219cfd9e1c4f9aff4c830b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/response/JsonRpcUnauthorizedResponse.java | 2531 | `92200a0e19a0caf81b176b9d1e2e5a23207dca1bebed1ceca6fbe97a7cf5ba65` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/response/RpcErrorType.java | 17846 | `e2afa478b517f8b1dba6adf97cb18701c6f5a3e266d182c0be08cc683f30650b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/BadBlockResult.java | 2357 | `1dff861dd6c66ae8b402b1035fcca63d0041de2cc13c03da4d19fe09debaae50` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/BlobAndProofV1.java | 2167 | `2e094ad3af6957e74802010261df0a6f7210230feea8bd0fcdd15fa0b0b4fff0` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/BlobAndProofV2.java | 1802 | `df0baecfbe122d5d4f7896883e3c42ac614e8ce7641ac1c3492f95a68a074087` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/BlobCellsAndProofsV1.java | 1661 | `a03d6b79040b5b69070ade8c10b16e09d69cf7b443c8d74a1e083a2315a591fa` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/BlobsBundleV1.java | 3203 | `ceb1fe1c9e145682d4e17cb5508f036a78fcded6e152b99f42f3dbdbcaa97648` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/BlobsBundleV2.java | 2150 | `ad239aec5cfa2aba90399f40b3d6ca0e38efa0c965610ecddb3721fa8e3cb088` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/BlockAccessListResult.java | 4628 | `2f5a0b800048ba787cb25d6c76c0bd4f42312980cad580cdc0279269456d72b9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/BlockHeaderResult.java | 6622 | `482306e0c71ec77db056f874ec5c2289012d44340c02b87a099aaee8956e5c9e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/BlockReceiptsResult.java | 1173 | `5c318e12fc22849d4a29ecae10d384340a491e9bd5e0b5eb360a114fb1050713` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/BlockResult.java | 8266 | `9c22264d0a384617784032bd1223f1d5797012b7af7570328c7d4c8e07c927a4` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/BlockResultFactory.java | 4201 | `5747affd0f41fb1e07b62a8f2bd7378d038d520fbaf119ad4dec58aed7fa631b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/BlockStateCallResult.java | 7917 | `5bfd25fc6bc0737fe7ecfb2cdd16fc196f05d4feb206c75b775eafacf2b364f9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/CallProcessingResult.java | 2454 | `7b4394702909494b569e13f31d2f0b7ae81d11209ea8a45b7d10f26a67c447c2` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/CallTracerResult.java | 17856 | `bdd7a78c00d224e3b2ee03684335a901cddf87fbc86f4280db813ac3adf6afee` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/CodeDelegationResult.java | 2049 | `b6dcb026abbfaf433dded5fc4b0a2a9faae49422e1436bf1d118c616e7e3e344` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/CreateAccessListResult.java | 1901 | `13bd00b5943d5fce3c49cdfc77b740e36de3dbf856f9eb646abc1f28aaf622e1` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/DebugAccountAtResult.java | 970 | `12116877e9421369f40154b89b09be7f9ef696089e4f1b6d777c18026bee77b9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/DebugAccountRangeAtResult.java | 1279 | `d02474c4f8b700cac69b07875c67c3a8ddc0bbbdd1efd6c4241d121b38742d83` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/DebugStorageRangeAtResult.java | 4064 | `0bc37a3c3abdb278818eb1c8ffb6b1f8e5839d47d345ec7d61178fbdc312654a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/DebugTraceTransactionResult.java | 1814 | `34e235af529acfc81e05618eea34fa3138bb3e4985f2a4ed3574f14e9a0b1582` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/EngineExchangeTransitionConfigurationResult.java | 2287 | `f8454a5b4d4d2ddb603afc73346f8529437977aa592b7ecf7ed0cbe64bdc19c3` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/EngineExecutionWitnessResult.java | 2017 | `cc7d50deee5c16c8ea692b90402b08c91468e5065a08d31bc532ff15c1bda997` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/EngineGetClientVersionResultV1.java | 1500 | `226194b411ddf1319b63dc0f51599d21e811de0dda04c5f45b20e1c9cb6e0949` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/EngineGetPayloadResultV1.java | 1206 | `5645affb95fae708e081edd0c279474f0ff5ac5b9853d6e5a91211a5ee58a97b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/EngineGetPayloadResultV2.java | 1643 | `ca9ba56bd7fae567b084f9abdc6afaac9b778b28b529a38c72a4330b5ee6b64e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/EngineGetPayloadResultV3.java | 1934 | `046e6511a02e55f5b9efdaa0ad98aec0644f8ecaa9a46c54a2ed344d25ece744` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/EngineGetPayloadResultV4.java | 1757 | `6fb2ec60ca96f7fc481752a4a254d920f8a8836b47fd706dddc4879f1849fee5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/EngineGetPayloadResultV5.java | 1490 | `9a8942358dfc92c911a5bb76a5517465a5cc640032ea7ea6d8ae972ecb81eea2` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/EngineGetPayloadResultV6.java | 1643 | `dc7659e8bac966ac9a83c9e1c866d4cd32470caaf3950664b09a065092222ba9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/EnginePayloadWithWitnessResult.java | 2989 | `2a4000bdf1ebc7c0ffc15733cc376efea567f1c2d030eea611d04ac60fc6df14` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/ExecutionPayloadBodiesV1.java | 1601 | `c91801f66e39b051da8dd6bbdf69c000ccc167001e70105740355a1c127fbf98` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/ExecutionPayloadBodiesV2.java | 1824 | `a333ddca21bb131e1be136d67bd00fbd71031f022310eaacf3a53c10da96b620` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/ExecutionWitnessResult.java | 1335 | `ce8911d01efa7329511a6b84fd3af2a4021d479a77363d97798dcec66511d084` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/FeeHistory.java | 2834 | `a46b58db14ec1e10114a59f125b064c77d76f4b197cdae27c62b23e14f1d0dd8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/ForkchoiceUpdatedResultV1.java | 2587 | `697fe470da070267463b621d7c8529501db5c083c1a2833c8eea3521f1a6e639` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/FourByteTracer.java | 2655 | `cf6b94ec5f5140f7a965046b96ee3be2cfeda9ae2161bf35a9a51d7a627dd82b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/FourByteTracerResult.java | 1933 | `80c59c0eaf7761c54cff41715523fcb99a4d9e27f465699e2069e4b7dc899975` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/JsonRpcResult.java | 872 | `9df41677aa964d0a28657f2a6eac554cdeceb86b3eb8cab55f3a2b1a4bd9a2b7` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/LogResult.java | 3403 | `b952a24322d4fcaa20cad26210848f0f206219457e8d3d45e3290e041a8e720b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/LogsResult.java | 1268 | `3cabd3cae4068db054f3520cb43238349c66a1e96cefaae45b1ef31011cfef1e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/NetworkResult.java | 1823 | `17c742274b97a5d37da24982801bed55619674bc897648fece901cbd837f2f44` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/OpCodeLoggerTracerResult.java | 3455 | `814eeaa6e3b447bacfd365c2fa389f93ab3b992bc870ddb9ea8d6410634bd424` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/PayloadPostExecutionValidationResultV1.java | 1702 | `173230ab27a45793600e3354e016a152af52437bd73975edb834be5c5d42ed0d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/PayloadStatusV1.java | 2252 | `7af71ddafe63e913f1e1d65b5fcfb6cd6d1890f7db1068fdffd1d140bbac4546` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/PeerResult.java | 2914 | `810acb4020d6140eec65d89ed97e3c2e7ca11a89075d3f1c51686d26a685cc94` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/PendingTransactionResult.java | 1785 | `b5257dfa7fca2741722c95d007dec1d388e89d693d6f692aa01440b75871c732` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/PendingTransactionsResult.java | 1346 | `84bd37e87ed55b819ecc0ddb53924790785df1c6e4d33e938416434b4219f2b5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/PendingTransactionsStatisticsResult.java | 1336 | `7a2dd59df399869d6c9815b6d411efa1d780ea3f6287007751149169b865bbec` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/ProtocolsResult.java | 1733 | `b6a67a1287ba5d827abfc12d297c6094e6c700e7201cd05e9324c1b28d0f9783` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/Quantity.java | 3769 | `13b89e5ac9f9e7e7fb2132827bd144cbae0f29ed35d032964072062ac2d1cac8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/SignerMetricResult.java | 2620 | `668f3be5635ec1f0f4cec3136bb00016609472e9b4cb4b0d33fd729377da7ce5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/StructLog.java | 8349 | `cb8a8e809dd996e66704caf20f40f7ce76bcb5d260fb11d2902844e95f496b0a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/StructLogWithError.java | 1292 | `6de1a41dddee883fbe2f2eec1ee199c9bdee4262d44dc332e2af3a4b71332056` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/SyncingResult.java | 2771 | `c82c2401670e4696613475ff3270a50201fc36ce62626ee7c88b3f0f7dede75d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/TraceCallResult.java | 2761 | `df59435a303d1b40879200b3c933a70fb58175113e455cdee4da0bfe6370a541` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/TraceReplayResult.java | 3729 | `dc741e0a0713881b38b90e33f21566e0b025429392dc38c568108e23cd18028c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/TransactionBaseResult.java | 8092 | `721d1cd577ae2fd226b861f1ccb2d82bc064b0c5d2c48369902144021f508875` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/TransactionHashResult.java | 982 | `ceb4f7971b5461a4eedec2638c4cf290b8c563dbba24580053481b3e4d979558` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/TransactionPendingResult.java | 1798 | `0537c81c098b32708291bfcb5750b905659b8ccc275004e6ac847155c9efc625` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/TransactionPoolResult.java | 1137 | `0ebb9a8d30d37bd70925feeb89b0da22618d78a40e1d9c2d6d23f6444ac290f1` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/TransactionPoolStatusResult.java | 1202 | `3f472072b2611968ed1a19633515fb7f64cd1e0105ce2101e72449247ce70e9d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/TransactionReceiptLogResult.java | 3419 | `f003b37553a14b1bfc4c4a818014c086597e178d73e241fb9861b2d8352f9727` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/TransactionReceiptResult.java | 6827 | `2813d1d7afda8b07bacfd82bdb66db4552a9b75899871139ce0b55232b1e4cc8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/TransactionReceiptRootResult.java | 1193 | `f5db4eaa0ddd362cfd1ab225fc631a46218d443b304a50be3249535e24a2ee1b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/TransactionReceiptStatusResult.java | 1210 | `fd08f714c36f0637095e78e698335df6fd81e10498540d0087b7302b207b8c37` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/TransactionResult.java | 728 | `cb449bab3a7ca0e5c1b35e29d71d70ffeef2ff591f3ad83f8e103a3b2f793bb0` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/TransactionWithMetadataResult.java | 2121 | `fe1b7fe467d8923afc98b679a047129e9482e26db499340c16ced8075a1970c1` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/UncleBlockResult.java | 1425 | `c57b96474fb16168baf91d544bb164f5da0ab4489eb574f9ad0a13e9e8e1bb49` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/calltrace/CallTracer.java | 23920 | `d567a1e1097c3b0826793c825f6ff95fee8c89f59e45962bbbead40a8a7c1146` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/calltrace/FlatCallTracer.java | 10824 | `dfbfd7b769a78e2d2ad40978b001b5bb6d16a337237772b35339f0f1fdf68088` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/calltrace/FlatCallTracerResult.java | 2355 | `33546e48270797cf80790e0833d3bdac9870b146aa60d20f2e4ce1ebcf12aa26` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/prestate/PrestateTracer.java | 20906 | `35cca78bf0894a9ccbc15eb84e39e9c0d84c4d2e9b00622e2f3ee356cd90e48e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/prestate/PrestateTracerResult.java | 2318 | `18a29c6e69c61dbebf5d64facfd9f2e1b653803c1c617ad6bd7ec2ac7631a825` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/proof/GetProofResult.java | 4827 | `2578b10187428c1e39e73633fe02f792c098e48a66e3d633a81db8ece4837a3f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/proof/StorageEntryProof.java | 1637 | `0a9d73f547dd93693b2e8ab7fb4a628aa98c1f2c8d83819642253cc02e28907e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/Trace.java | 1229 | `6aee7d5c2cbdf4a3a3b64fbc5fe3bf72e4aee17d83752a38e7b2eb7d91a16c13` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/TraceFormatter.java | 1198 | `900440681e1ba05add1c4a76298687625c5d9506f4f959f9ae248d8e8c6111c5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/TraceWriter.java | 779 | `d79e714036e8167c9d496a13a0e56a7fbc29d6c73f0981a3beeaa1bf7afb5162` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/TracingUtils.java | 2162 | `bd44ead53050c3e6111349b66b66fbf5c11923ff8415ddc8f21404ddb37f0b68` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/diff/AccountDiff.java | 1828 | `b90fdbeb139caf6c0f92155f5366c3d6e842312ad7635e9781dd6d1f60536f15` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/diff/DiffNode.java | 2847 | `2bce5c59840d3c6601b6b113927b0507eb77de5ff0aa67c5caf2e228f4ea5eec` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/diff/StateDiffTrace.java | 897 | `a6a9575a9bac27ecf26e2e197d9d5fa7c4ff14acfc0f37788f4e00fb8dbdb3c9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/diff/StateTraceGenerator.java | 7699 | `947d884c089ed7b4fb2142634621b68800f095630986de52882d46f99fc3e554` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/flat/Action.java | 6898 | `aaca23b0f24534c3bcc91019aa4b66a988c7780e7a5f8ee0314b308d7e7cd91f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/flat/FlatTrace.java | 9495 | `66cc468bca9ca1da2a58c2c781ff0d85a2db66961fdb3d6d14c4d34cbb83ca9d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/flat/FlatTraceGenerator.java | 26624 | `c8db3b466bc70cdcaf677eab5401bc0144c852f8a795fd9e175e578ab526bf0a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/flat/MixInIgnoreRevertReason.java | 866 | `32fc5bf5aedd77442c5fb6e383f66a70e9462d53bf03d487e2e35a7303d662a4` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/flat/Result.java | 2947 | `3d7a89b290b8d435605bc8000e289bb190511b5981d13274dd27dfa466773eaa` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/flat/RewardTrace.java | 2731 | `ca652245b46c512d8ad741938990eb5ea30ba36430f3b98b6554ab857dde656f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/flat/RewardTraceGenerator.java | 4110 | `c41979539f0f3f7106e767c9194aa83d4eb3f90b608b9672f4431c86539bf07f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/vm/Mem.java | 971 | `0754782b7fcab75a379096f7fad14562524b110b607f604f11928da43853f2f7` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/vm/Store.java | 969 | `9083fdec55a318d75a1708aa47000a0e0236b6b634805484db0159dabd91e3a8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/vm/VmOperation.java | 2635 | `6bb7038da01409f0f32df82e4e3349d19f42d0fa592bcd842633a7ad5a67032e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/vm/VmOperationExecutionReport.java | 1594 | `648d0ff728c3d684cba8d86d02358bdfacd3813bf0b25ac45092a42c5306a1f0` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/vm/VmTrace.java | 2002 | `80af090de8f9f4ec9843f6e5efad2440d261ada7123128d6eed0dea98b4d0b91` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/tracing/vm/VmTraceGenerator.java | 12428 | `a5857a3a0a4e911a18e1a979c49c6dd2d26f47421d968e27281c37ea9ba6a39f` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/transaction/pool/PendingTransactionFilter.java | 6376 | `363ef5260884acb6824a498150d1d1c24017bfb8bac16de1e1a6fcc968cc73a6` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/internal/results/transaction/pool/Predicate.java | 1595 | `71805c3fe7493d681ca5c269a0b31b0711d26194351068d1c8e620dbff5dda61` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/ipc/JsonRpcIpcConfiguration.java | 1466 | `3a478c88cfbe014a0cfb301223a8dd1ef77e83898b221df6d22b9a5cc84cf9ee` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/ipc/JsonRpcIpcService.java | 10157 | `2fbe07198eb6d1d5e2f440b6c7c00539081ef5c6bb91abc8226a80c2367071c6` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/AdminJsonRpcMethods.java | 4377 | `0a7f8703f0e1206b75df0e5afefa74d3207fa1cb5bc6e157cbdd151df2c2016a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/ApiGroupJsonRpcMethods.java | 1657 | `3496af07e390192021725cdbfc06e113ec7335879d3b88143fd8c397de3f2bde` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/DebugJsonRpcMethods.java | 7619 | `81e5a456432d13341ca281eb323a7a4710ad5876ceb2cb1773b0bda2ab4238cd` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/EthJsonRpcMethods.java | 11963 | `ec75969abcbbe8d00f834b2a9b4f5d9912f4b6c94da71a1071daa659860fca25` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/ExecutionEngineJsonRpcMethods.java | 17398 | `0a64aa4673501a58f932d6324fa48ac7167f009a2c3b18c5445edf174aeda235` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/JsonRpcMethods.java | 923 | `90065d2de1afc2050fdb70b2bc8a7c74f1b44865e447ce63688023ba824b0516` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/JsonRpcMethodsFactory.java | 7507 | `12c0f09f2a68c154bcb531b754fbef8f2c82ef3286d31937bb8407d5a97e6c7c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/MinerJsonRpcMethods.java | 2603 | `3021d6518fceee1ba3a0375568daf1518514dee17ecb63260aaa9d13db88c2d5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/NetJsonRpcMethods.java | 3161 | `ce9f31664697695ec4ae29736069670e5890cb54b7f34d8c865c431189aa9de3` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/PermJsonRpcMethods.java | 3076 | `3820b2e2ecbb0f603eb4ea5bf3844aabcf95983f313a21235deb3fe9f141b0fc` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/PluginsJsonRpcMethods.java | 1448 | `51a3fd96d37122034a7d32618cac1943b2dea47c2314ebf14e373b3c8846ce66` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/TestingJsonRpcMethods.java | 2771 | `924b960429965c825de96ebb3aa896097d7db38251bb21846bff48d496a916b9` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/TraceJsonRpcMethods.java | 4455 | `9da382964d4e8f1d8b3ee4e6eac70aebc0cf7268d48f2a3ddb0c29a7afac73d5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/TxPoolJsonRpcMethods.java | 2271 | `c4c61efa48fbf55c9e14534343acdddb3d403c54f9fbfff560ae82b317622c29` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/methods/Web3JsonRpcMethods.java | 1437 | `f943eeb1109a7ea3a92629c91ca2a2f7eb10803d150006f2142464e6e1a9da55` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/JsonResponseStreamer.java | 3990 | `e149a30046ea6acf54fc2442bfba043402974da5c23802d7f17f949684a30c7e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/WebSocketConfiguration.java | 12461 | `2a7241ed20931d4e08c8ee367648b29799e643a006d53367963f91463e927f91` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/WebSocketMessageHandler.java | 10674 | `cd98d9e9a370445f6fae259fe745a52380e007f034316e67652d88ecff01a343` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/WebSocketService.java | 17120 | `8234846cc95770a3df31d94915ee617c46042c19312d4b6e980bb8d722a00cd3` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/methods/AbstractSubscriptionMethod.java | 1516 | `4bdd6d5db21e9d65b27ebfb9447341a594dae1136827fb577424897a963d1db2` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/methods/EthSubscribe.java | 3779 | `8b58b86439b104aa1345f29c578b8d15299c2d923a395b23326e8d20f9f4b437` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/methods/EthUnsubscribe.java | 2943 | `60b270a9aa6d8814060e5b69845894fd416e1a23ab6077bc3e5522f400405932` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/methods/WebSocketMethodsFactory.java | 2007 | `b5023843fd0df92222e39761f3b88bf31e7a79b2ab21ea7e406731ad7b148a06` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/methods/WebSocketRpcRequest.java | 1649 | `fd5b65e12693b5fbab1a63817955e686982c2c56fdabc3af05345328e7e0a585` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/MaxSubscriptionsExceededException.java | 1362 | `f22b9c60d877ed6652537a3284337311eb50738106a6962749dc6514642f8870` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/Subscription.java | 2580 | `25a8f4674b6815622dbaca7066a16e4c00937e28d84298f805f7a4b73cd33978` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/SubscriptionBuilder.java | 3179 | `9845752f4e644efca66c2f9875a438b10a92f3aafff48f50b88c9075d2ad4e14` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/SubscriptionManager.java | 8528 | `4de7d38364441c9aa7559e8f90243455781fb4d1de872bda3ea68094c9a4598b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/SubscriptionNotFoundException.java | 1065 | `4fddf11cb39f7f4d653ef36c8e2403b079d1e097acf10e08d4dce30c13afbcb8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/blockheaders/NewBlockHeadersSubscription.java | 1371 | `793fe43167d339115111fb6966673ddc3ce15cb041e85fca2a75e7a8b27f2c5a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/blockheaders/NewBlockHeadersSubscriptionService.java | 3963 | `432a220e5bfb5bd19f0dd1b454c32b79df527f4f0ab11fa7ff40d0378673ad0a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/logs/LogsSubscription.java | 1414 | `a11cab82489790a85e1fc1977e3e1d1f211fe1ef0d10791ffce891891c398c2c` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/logs/LogsSubscriptionService.java | 2629 | `27d34d930830c5d5d18ebae04d8ee7716812a71639b860595439359ea779af58` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/pending/PendingTransactionDroppedSubscriptionService.java | 2357 | `28ac9f525f36314b110896c7340b42a81793bd33484bd36387589964f49fc2c5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/pending/PendingTransactionResult.java | 1133 | `e5f86bd09d1d62a1d5755427fcfd87e2fe11efb8ba4beb290a60529854f14526` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/pending/PendingTransactionSubscriptionService.java | 2632 | `c99855e3618028460b6bfa1a67fbaa64b6a1f82111e39f4f78d6114db33cc66b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/request/InvalidRequestException.java | 852 | `4417edb28326459a146d759e60593ca8c06955c1a33f9c4d847bdce62cd7af9b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/request/InvalidSubscriptionRequestException.java | 1067 | `5112b89f2c45f4af3a1a53f127abd266fde35a2bcbf7872a7886ec912068ae00` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/request/SubscribeRequest.java | 3314 | `7e98ff302b1c3ec2152a3e9ecc5404879c96eac88de065714e04138a21230a0a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/request/SubscriptionParam.java | 1117 | `932686b25cd6aa09c5c01aca943750c0e79430b557a79c91441edbabfe1b32f6` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/request/SubscriptionRequestMapper.java | 6552 | `99c58421473c8fb77c678861230c319cbdc00930efa714f686a30064de83fd61` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/request/SubscriptionType.java | 1728 | `512ebd399c21bc7923d4121c7511984457180fbe8b34c8605b3f358789ccd321` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/request/UnsubscribeRequest.java | 1807 | `139eab91528cbde6ce2afc24f98ebda5a769c02b397bd34474fddfc690680417` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/response/SubscriptionResponse.java | 1904 | `44e0025d45795faefefb7243bd3fdc39d1ea25509dc26d867be0d22a188bff00` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/response/SubscriptionResponseResult.java | 1402 | `020584e02e07b3c5f22a41d4828dea0a7fb49a6280e5accc50957733d6794b8e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/syncing/NotSynchronisingResult.java | 1183 | `830b11b03469e07875227558dbf03782a6b4bb4b79b1ca3ab259337ba96e2a9d` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/syncing/SyncingSubscription.java | 1457 | `cb1e73e75ed290b20117dfe0987d8200825d3ffc08a3dee6f1faa4a27e998b58` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/syncing/SyncingSubscriptionService.java | 2211 | `965edc61ecc5289ff44417d130e133a9841a2375897c1ad9504c2271d866be15` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/transactionreceipts/TransactionReceiptsFilterParameter.java | 1648 | `617524f62380433682af9909e86dc3c4af78737c5736907f894ed2a5e4907134` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/transactionreceipts/TransactionReceiptsSubscription.java | 1776 | `7743fc1282de3102b8847e00f3c987114131224be37ca91103d462bca7d441d1` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/jsonrpc/websocket/subscription/transactionreceipts/TransactionReceiptsSubscriptionService.java | 5240 | `9b0ee80dc44c683028ff249ef06567af58f629ca40ca30aba9784b0d2628cee5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/pluginadapter/HealthCheckServiceImpl.java | 1583 | `92f142ac7ee5b5224668f71c59a2977345b193d0955e5aca2854f659429b0951` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/pluginadapter/RpcEndpointServiceImpl.java | 5497 | `00bc2bacf35e1e9e5acce8d57fee57f5eedd010157324afd10a9f604759d81cd` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/pluginadapter/TraceServiceImpl.java | 10954 | `20720b55a18ac804cf4b70afa49b39af9d35be63881f987c72b6425714bfc58b` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/query/BackendQuery.java | 1903 | `8b4e22dac9e5e2d02b03e3f420373c31d100a1560bd7d5be0e545e2b796cb83a` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/query/BlockWithMetadata.java | 2568 | `c625711bcdfcfd976c2407c9e4a1012679d1159c3414679c812f4f022d36b4e5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/query/BlockchainQueries.java | 54079 | `8fd20e0d660cd7dfaeff015f8a6b337e3d79d3ad39c1f1e6e6100fcde22abc76` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/query/LogsQuery.java | 6200 | `f4580b3cac6e0a9bbaa304d9f42e94f6faecef648f6800a54e7133b7c3980d7e` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/query/TransactionReceiptWithMetadata.java | 4976 | `3bf02c2f867cf973c75d81ce9dfc9ca70d3d3bc4ae64f9f2a813b34fbab25533` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/query/TransactionWithMetadata.java | 2408 | `510213dc7c89dbacd81b2bad7f3a18f938743df45c1c48d61a4e62804a64f9c5` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/query/cache/AutoTransactionLogBloomCachingService.java | 4009 | `5973f68a83a9d5807a18e1abc1c15a898933ff46e56d9d9544c3e1fc1ddc83ad` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/query/cache/LogBloomCacheMetadata.java | 2675 | `f989f5098dbe899c6a04e2204feb2273db74627b60ece9f08498738be05b0499` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/query/cache/TransactionLogBloomCacher.java | 16259 | `14eab0d849ef36157ef664aa186691b95f6d06b1822db17b2780e28f5d6e1ba2` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/tls/FileBasedPasswordProvider.java | 1723 | `c5ec056caf94842d458c1a48f8f94edf26341b96824f80a02795682cdc6664a6` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/tls/TlsClientAuthConfiguration.java | 3290 | `4c9d2c36fd876bbbe17f3e51c5fb7e02b090844025fef65054a4735b12fce4bb` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/tls/TlsConfiguration.java | 3952 | `22ced580bad47162dd3b7a48b477175f917f0f427129340b8e7ca9a5133768e8` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/tls/TlsConfigurationException.java | 934 | `0d563c7c7c0005178a0cb8b6249e7489f03cfa09f1f95911fa5820b836c9fb95` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/util/ArrayNodeWrapper.java | 2161 | `946fd71eb7a904f1b545b93aea2214e817fe6615d375fca33cce88855d0d5c82` | 0 |
| ethereum/api/src/main/java/org/hyperledger/besu/ethereum/api/util/DomainObjectDecodeUtils.java | 1844 | `2f3d36c044528375bb97c6fc3225927af9d587b56205b67760716c78ac9bd283` | 0 |
| ethereum/blockcreation/build.gradle | 2166 | `9eccea56108766d2b0326fc526e356667a7e814d9e28f3dfdc1c7fc52945920f` | 0 |
| ethereum/blockcreation/plugin-api/build.gradle | 2146 | `5464522521b3118449bee097b78650f87af66e1ca63ebc836fc01d2288d7240e` | 0 |
| ethereum/blockcreation/plugin-api/src/main/java/org/hyperledger/besu/plugin/data/TransactionSelectionResult.java | 12820 | `a532b485e4c5fd980401764ad9bfa1252ef19dea67b778ee457fb1165aee4a72` | 0 |
| ethereum/blockcreation/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/TransactionSelectionService.java | 2781 | `7c75a9a5a612b9ae68bfec45418eda699a24ec1b468c51bd863048bdc3a81711` | 0 |
| ethereum/blockcreation/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/mining/MiningService.java | 1177 | `36c461c822268f0f40ce938c467f5e06d07c0de2cf0f6dfbcfe00c6341f2afcf` | 0 |
| ethereum/blockcreation/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/txselection/AbstractStatefulPluginTransactionSelector.java | 2539 | `c87b79b2bf28459fdcd64c1a899bdb44b7f440d6ba2bf098f6ba25415632cea7` | 0 |
| ethereum/blockcreation/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/txselection/BlockTransactionSelectionService.java | 2494 | `12ac6ab8c53188a589665bf33d481a7f5565b81cfcd5ba164ac3e3442d1fa6ad` | 0 |
| ethereum/blockcreation/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/txselection/PluginTransactionSelector.java | 3943 | `69dc1ce96604d9cc56c7c9ea382e49e8735662f8f7e039e2dde34e8443365853` | 0 |
| ethereum/blockcreation/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/txselection/PluginTransactionSelectorFactory.java | 2969 | `2e33aa5248b841852d61f37bc8eadf0e5127a8afa6cd898a3151e6d77802a014` | 0 |
| ethereum/blockcreation/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/txselection/SelectorsStateManager.java | 7240 | `1228b296286895ad4cf48fca7b9768731983f327c8fadee2dfb5ec53c16eeac9` | 0 |
| ethereum/blockcreation/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/txselection/TransactionEvaluationContext.java | 2072 | `2226ccade3f5ef5a3320f338dbd6eb999dd1407bc538a4ad50bb2d963a607087` | 0 |
| ethereum/blockcreation/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/txselection/TransactionSelector.java | 851 | `f4ff0dafb81461557a6a3d289a6cfa41d6c8376d73599a7ebbf88a33fa9497d5` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/AbstractBlockCreator.java | 25750 | `8f07509bb1dbae1ed40d2399fe4d69ee2b556304c2ba847720bc816043099a15` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/AsyncBlockCreator.java | 779 | `30252bd325bec2ab81022f88f933b22d1a414a92b3988c6c353770e522f196a6` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/BlockCreationTiming.java | 3121 | `670292b0f90112b0b3adfffb9c51a7d02f361c94f409a83179b399800e62c319` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/BlockCreator.java | 3350 | `81fd44694f3ce357cd3c7a773425104657839192ec0b251216c3be04e35abe27` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/CoinbaseNotSetException.java | 823 | `4b477299b39c8d0e0ba7ce8af5f522e8d1a54ad7c2b6e385e882caa0451e37da` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/GenericBlockCreator.java | 2435 | `f9f71e9437e037853ba514af23388db1957c97d10f30728e9a18232d4c3ad942` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/MiningCoordinator.java | 2467 | `4a322633640feca30f6572fd81120cceadb9a788a9ca2149ef3f0d26af02cf67` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/NoopMiningCoordinator.java | 2327 | `0142101717f1135ea9e90cf1eb2f0395579abe13e50c174bf24a746256683a01` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/pluginadapter/MiningServiceImpl.java | 1876 | `0c3a1ac56476bf2a96835304e1f4c0fc10a0ec1b24124378c465d42975c19c8c` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/pluginadapter/TransactionSelectionServiceImpl.java | 10994 | `d9ea2b70bba564e001cd152d29815eef27e821ce5ef89010a45af29417e186db` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/BlockSelectionContext.java | 2061 | `c3cef9170c0f0225d6edfd43cbf61e06c5bf2e0865b9127ea1004f2f7926b6b4` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/BlockTransactionSelector.java | 50435 | `f577b7e6bbac436207e54b418613bd72c2c17b8a458b1d27dc3b666949d2f817` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/InterruptibleOperationTracer.java | 4234 | `868ac517f6b0d776fa2d0251cf80a86c8d4d2303f247d7d32b515c90633e9122` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/TransactionEvaluationContext.java | 2878 | `71604e0f543a320ae71fb4b3029306d85f3902f4dbb4bf4ae167be96196f7049` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/TransactionSelectionResults.java | 7622 | `7f030b9e4554aab10e30a9368ba5f6591edb0cf4af6b10b25fc4501640ec2272` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/selectors/AbstractStatefulTransactionSelector.java | 2185 | `37baa5d172a83d1a4db37ddbccdc616e5acfae7198e9714a39a12763c356e482` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/selectors/AbstractTransactionSelector.java | 3155 | `1177ce259af8f0b54dd97d1b23dc08e8067521cbc6bf145d95e699fa3b37d788` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/selectors/BlobPriceTransactionSelector.java | 3254 | `1f6ef0f409ac16e395e0721db6734b87bdb646f7b98a766d3943ec8f150fe9ff` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/selectors/BlobSizeTransactionSelector.java | 4371 | `de4515ead6227cf2ea2754ab32f36cd825e5fe64c490fa746783b12ef4889e5a` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/selectors/BlockAccessListItemBudgetTransactionSelector.java | 3512 | `ebf2ff33d3792b373b1ee01e3e9a917aec9ac74bea2a854e50e90c4e6869fd33` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/selectors/BlockRlpSizeTransactionSelector.java | 3868 | `e1f39c78dbceac8199e55d220583742ad68b57ee9d4162bd6b7530735617debe` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/selectors/BlockSizeTransactionSelector.java | 7155 | `c0eb4c3f9b122dc0f9e9af7e94da4ac034f1c461d982c087bec1297374c0f8df` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/selectors/GasState.java | 1553 | `12b7e4f963899f7b1347af1a4483facf7bbe986119a9872b795a228eb13dad66` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/selectors/MinPriorityFeePerGasTransactionSelector.java | 3429 | `b907ea9021cc764217cba38d11e3d8954b661580cffb3940cd2e55aa5967e88d` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/selectors/PriceTransactionSelector.java | 3835 | `5dd24db02c965a8ccc4d8125e46854796687cf6c22351a12f94faf02c5266a58` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/selectors/ProcessingResultTransactionSelector.java | 5221 | `7dbeaf1667e1738a814553aaa8e673f8d553b46c4b9cd5470aeef57bc9396f62` | 0 |
| ethereum/blockcreation/src/main/java/org/hyperledger/besu/ethereum/blockcreation/txselection/selectors/SkipSenderTransactionSelector.java | 4953 | `e83648e5c0b72dc24dd554869686b542162d57a7dfea128dbce5a58bebfe6fb3` | 0 |
| ethereum/build.gradle | 646 | `aa191ff708e7b1f228615c5b5cb16cc678f78950515a188dfc87a693e9676ca5` | 0 |
| ethereum/core/build.gradle | 5746 | `947c72c4a05e5256be9944a5d31412199931b661077c84f65a01e56cdbedb86e` | 0 |
| ethereum/core/plugin-api-chain/build.gradle | 2071 | `477b230c5d52e4f61c30b5e4cddac9fd8e98604f91846333d209394b3dc88464` | 0 |
| ethereum/core/plugin-api-chain/src/main/java/org/hyperledger/besu/plugin/data/AddedBlockContext.java | 2833 | `519bc562e0b5984b0aa9429fba170103290f10d87377410b0faf063ff718533a` | 0 |
| ethereum/core/plugin-api-chain/src/main/java/org/hyperledger/besu/plugin/data/BadBlockCause.java | 1321 | `a71fea2b1475f0b757e19511d852b38690dd8bb47bac3ed456fd859f3c8b6a7f` | 0 |
| ethereum/core/plugin-api-chain/src/main/java/org/hyperledger/besu/plugin/data/BlockContext.java | 1001 | `b976a82f52ae2e2d3e09aa57e5dc24f0521944c7839fe8af2b02b0e0855e982d` | 0 |
| ethereum/core/plugin-api-chain/src/main/java/org/hyperledger/besu/plugin/data/LogWithMetadata.java | 1955 | `43413de0a320995505d767526a025f3c5e5a1ecd677076b46135382809ed23c3` | 0 |
| ethereum/core/plugin-api-chain/src/main/java/org/hyperledger/besu/plugin/data/PropagatedBlockContext.java | 1015 | `ea127848de31fff63bc9a860efb07d21a2ce87b457fdea2c3fbe940b346d37f1` | 0 |
| ethereum/core/plugin-api-chain/src/main/java/org/hyperledger/besu/plugin/services/BlockchainService.java | 8583 | `468b744a7953c5c3114983b63269ed7be43fbf803e9b0ad7a9bdd99999ce62c0` | 0 |
| ethereum/core/plugin-api-chain/src/main/java/org/hyperledger/besu/plugin/services/chain/spi/BadBlockListener.java | 1241 | `fc934fe8e615c08d6adf79dd81b144dac7f23307d391c6744e9c4c0e68101204` | 0 |
| ethereum/core/plugin-api-chain/src/main/java/org/hyperledger/besu/plugin/services/chain/spi/BlockAddedListener.java | 1036 | `415ae2c9c729dc82bec681c298822777b5e5c5b097d026036db22c1ec2d681dd` | 0 |
| ethereum/core/plugin-api-chain/src/main/java/org/hyperledger/besu/plugin/services/chain/spi/BlockPropagatedListener.java | 1302 | `5f5f7a99d7815a9df5456d7bd7d7f4c802eee3058e9ff40200ba2841fca4de22` | 0 |
| ethereum/core/plugin-api-chain/src/main/java/org/hyperledger/besu/plugin/services/chain/spi/BlockReorgListener.java | 1040 | `1ac470ee6a45e65d3fb992932d6c855e65a046507a451316a5310418a2593922` | 0 |
| ethereum/core/plugin-api-chain/src/main/java/org/hyperledger/besu/plugin/services/chain/spi/LogListener.java | 1124 | `9090de48a52f6a1f75a3f46d14da65c7a083f439f4cf335322f1da46b1218674` | 0 |
| ethereum/core/plugin-api-chain/src/main/java/org/hyperledger/besu/plugin/services/rlp/RlpConverterService.java | 2244 | `a7bc87bf9853e0edb4786a7113babe51be9f87941dac95c4b7fd617f37d38e0e` | 0 |
| ethereum/core/plugin-api-execution/build.gradle | 2184 | `fdb68208cbdf9b5bd4da769811dc5903fffa6db9514b70e7ca8c2bbeea300b3d` | 0 |
| ethereum/core/plugin-api-execution/src/main/java/org/hyperledger/besu/plugin/data/BlockOverrides.java | 11681 | `a43f8b61d69a8decdf2e501e0efb784971c39bee2b65b1d97f8d02052ebb921b` | 0 |
| ethereum/core/plugin-api-execution/src/main/java/org/hyperledger/besu/plugin/data/BlockTraceResult.java | 3877 | `1ef58756ba07d30e81090ef830f6cc1afe8f9d55537aa0aadf84f0d379ae1368` | 0 |
| ethereum/core/plugin-api-execution/src/main/java/org/hyperledger/besu/plugin/data/PluginBlockSimulationResult.java | 3568 | `8aa61c005b7a7f5094dae9be723acd852c46ba74efe6ac5ee98aecec08f1d93a` | 0 |
| ethereum/core/plugin-api-execution/src/main/java/org/hyperledger/besu/plugin/data/TransactionSimulationResult.java | 2090 | `26940665aa7e6321ff989edd542dfb54a6c78e03d938e827a4536e4ca017de5d` | 0 |
| ethereum/core/plugin-api-execution/src/main/java/org/hyperledger/besu/plugin/data/TransactionTraceResult.java | 3723 | `42db887661d47385b4c5ec0fe0f36b31cb45e487cfef11125f61865c3a087ed9` | 0 |
| ethereum/core/plugin-api-execution/src/main/java/org/hyperledger/besu/plugin/services/BlockImportTracerProvider.java | 1207 | `9cbe3bf17e06b206a9c6bf42c699486eeb53d7c2b956dc515fac90f31bd9605e` | 0 |
| ethereum/core/plugin-api-execution/src/main/java/org/hyperledger/besu/plugin/services/BlockSimulationService.java | 3137 | `8402d382f670ab8d3ccc5b8b9ee241757458bcdfc5898bc23ccb00b6283db695` | 0 |
| ethereum/core/plugin-api-execution/src/main/java/org/hyperledger/besu/plugin/services/TraceService.java | 2272 | `c68b45c0554635accad21a40487ec91805b800b64266b083ce324fe515c61c68` | 0 |
| ethereum/core/plugin-api-execution/src/main/java/org/hyperledger/besu/plugin/services/TransactionSimulationService.java | 8130 | `30c79b056d37443edd36cc6335224cf2409d101747834051e7a9aedb2cfb6156` | 0 |
| ethereum/core/plugin-api-execution/src/main/java/org/hyperledger/besu/plugin/services/tracer/BlockAwareOperationTracer.java | 3518 | `c729c48bc8357a620f44edc6050e399a76652e3b840da0eca891364058a1b172` | 0 |
| ethereum/core/plugin-api-validation/build.gradle | 1920 | `ffbd991fc12633952fa1906b860e9b9f16bd7608d770c12984488d38f53b53c7` | 0 |
| ethereum/core/plugin-api-validation/src/main/java/org/hyperledger/besu/plugin/services/TransactionValidatorService.java | 1454 | `5d52f0f139a9ed5c893dd9878e38d934c51b39b139167f82e7cb8c48e62e876b` | 0 |
| ethereum/core/plugin-api-validation/src/main/java/org/hyperledger/besu/plugin/services/txvalidator/TransactionValidationRule.java | 1852 | `c73c345fa72f335a7477fd4fde5175816a83cfbfc4d04d3f4e67fc120e022496` | 0 |
| ethereum/core/plugin-api-worldstate-backend/build.gradle | 2439 | `df825b5e4db05d048ef413b6ff503f9ff591c71739c3c5815bb1bb317e124a73` | 0 |
| ethereum/core/plugin-api-worldstate-backend/src/main/java/org/hyperledger/besu/plugin/services/storage/WorldStateKeyValueStorage.java | 1913 | `73c1bc454dfd812b1e6695a96b8b3c8b715e13115a6f4a02b7ad7b1e55e7794e` | 0 |
| ethereum/core/plugin-api-worldstate-backend/src/main/java/org/hyperledger/besu/plugin/services/storage/WorldStatePreimageStorage.java | 2854 | `791e05bdfb76ed06961edba4797b9b89a943dd58de53a9e3c6eca76aa8cd88e4` | 0 |
| ethereum/core/plugin-api-worldstate-backend/src/main/java/org/hyperledger/besu/plugin/services/worldstate/MutableWorldState.java | 2963 | `eaeb550621bb8aa376e7cbd82c80b6851cf15c0c0214f66a1038ea0724e18156` | 0 |
| ethereum/core/plugin-api-worldstate-backend/src/main/java/org/hyperledger/besu/plugin/services/worldstate/StateRootCommitter.java | 2914 | `def3b15c65cadac62f1a9d05116da6ed33717e2afb8414ebd3f7430adbadfcc5` | 0 |
| ethereum/core/plugin-api-worldstate-backend/src/main/java/org/hyperledger/besu/plugin/services/worldstate/StateRootComputation.java | 1255 | `bfc875d1c882b1ad75232fdeb4fffbf2149007ec444ae282c910fe706b8a4404` | 0 |
| ethereum/core/plugin-api-worldstate-backend/src/main/java/org/hyperledger/besu/plugin/services/worldstate/TrieBranchType.java | 965 | `3daab9b6d02c8c1645fe77fa98f107c7ed5cf9aa8ca2336009053afd405cbd04` | 0 |
| ethereum/core/plugin-api-worldstate/build.gradle | 2167 | `cc8acfff9400b5e2a7ed7d0861603fa22880ba20de5d23cf2b45186e5386f468` | 0 |
| ethereum/core/plugin-api-worldstate/src/main/java/org/hyperledger/besu/plugin/services/TrieLogService.java | 1907 | `89475f8aee661d0d3671396fc3bbd5333c08c75ca9d7189265e9ff2bfa52ac39` | 0 |
| ethereum/core/plugin-api-worldstate/src/main/java/org/hyperledger/besu/plugin/services/WorldStateService.java | 1382 | `c70b5fbb3806ae70fcb0fff17b5eb1d33ab122921c75830f05566dabca1e8933` | 0 |
| ethereum/core/plugin-api-worldstate/src/main/java/org/hyperledger/besu/plugin/services/trielogs/TrieLog.java | 6211 | `1fe9ba10ff9d71a63e6d239c5e22707c29cf146fef6223e5bc2d22265f8cb6f0` | 0 |
| ethereum/core/plugin-api-worldstate/src/main/java/org/hyperledger/besu/plugin/services/trielogs/TrieLogAccumulator.java | 1656 | `4aca140966e0dca57f1135455ccf9bc98088d4acd9b00ba43b0cb82bf3cf8b84` | 0 |
| ethereum/core/plugin-api-worldstate/src/main/java/org/hyperledger/besu/plugin/services/trielogs/TrieLogEvent.java | 1284 | `17ddd34ee870a675f85b39e9f8e909ae318a491615c50205836e899a62237946` | 0 |
| ethereum/core/plugin-api-worldstate/src/main/java/org/hyperledger/besu/plugin/services/trielogs/TrieLogFactory.java | 1451 | `eec1a5086c61bb75a947bc4088e19dee0c0ae4de5e85e52e2d7e7a279de12dde` | 0 |
| ethereum/core/plugin-api-worldstate/src/main/java/org/hyperledger/besu/plugin/services/trielogs/TrieLogProvider.java | 3041 | `cce44c2b632e176c8e9269ca4f0ee1cb14f7bec99dddce61681816cd3747c549` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/core/TransactionTypeBenchmark.java | 1923 | `d16c0681b8ff9b849d4dda6fa3dbee7da46a3a1bf04838129fae51f13cc1fbef` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/mainnet/block/access/list/BlockAccessListItemCountBenchmark.java | 4257 | `01299c8bc7fe5437e943086b7408b4593558195a6ccf1cf075fc0bd3ce6c3ed8` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/trie/TrieHashingBenchmark.java | 6976 | `0d27332c13817931d38317f5ee471886b1559f9b90b3a56a50524f0a995f335c` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/EvictedCodeCallBenchmark.java | 8552 | `7c312471a23a780747265c84ef103609b72782806b206d55fb48d3dae647ab81` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/util/AddressStorageSlotKeyHashing.java | 3758 | `10360fac9600ad064a3cb132a72b2b3030fc7c67d942b1f3cd66ab0f81eef4db` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/util/Range.java | 3062 | `3fc519774571be9ce751c00ea4be2bfd6994d305a693777765d1719909d3299f` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/CodeJumpDestAnalysisBenchmark.java | 13077 | `f419ba712f34a567399aa5817659eb576e3637d040386272a7144ee0d7fdedfa` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/AbstractSarOperationBenchmark.java | 5112 | `e6da80b073c504cd7be0755e7174e826106cc39e3f426cfd02cc1599c236fcad` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/AbstractShiftOperationBenchmark.java | 3360 | `cc6f89cfd72b02db802f27c5d54a9fa2cb24f99dee944657efb10c969775ffc5` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/AddModOperationBenchmark.java | 2872 | `ee70fb4ed740ab32acfedc060b78058c5f2f1f8b72304770c4cd1017ec8f4d90` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/AddOperationBenchmark.java | 1614 | `4f89dc23a998f80b1fe2719d6519f1709f2f223516727c479aa1395392f796f5` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/AndOperationBenchmark.java | 1339 | `07100283a4768e752ff40fa24e98cb1f0e093cacd221f594a4213de1a76d4def` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/AndOperationOptimizedBenchmark.java | 1379 | `063c497fce0b9726a9113c13256102290dc937456f796ca0c06fd4d591fbd839` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/BenchmarkHelper.java | 10168 | `75bf6c4798ad598afe8ebec6abd3e3002cfd953b5283b32e08bf5f2c2ac1b91a` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/BinaryArithmeticOperationBenchmark.java | 5495 | `b6556c25e2fd196a7be510dd14c51de75fbab61896eed9dc1182c2b66f7c6789` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/BinaryOperationBaselineBenchmark.java | 1118 | `b3c38b5f54d051e1bd52eb85e2d9f94464a22d5f635af88888008d0e17715bb5` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/BinaryOperationBenchmark.java | 2349 | `e7f2557eac81865f3343a901f59684c023015af4daa6432fca70d1cb296d5e79` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/BinaryOperationNoPushBenchmark.java | 2362 | `87cf2efbb58c8671a894e40d165db017dee34a12fab7c65ce5999ddb98b4883a` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/BlockHashOperationBenchmark.java | 3439 | `ba379ac2c7f85c50e89cd1b432eb48ddfec06d2f6a1413cb0725489686a34d92` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/CallDataCopyOperationBenchmark.java | 3907 | `a2b94e68d338ee6211c223bf6e0db0433dcc0878098cea788389e4513a280b1e` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/CountLeadingZerosOperationBenchmark.java | 4209 | `768971694970b0f8fa6e02393b22deb814d75df09a2f447a3818a082b077d6e9` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/DivOperationBenchmark.java | 2077 | `7c29c93fbe11867a3da9a62370ce24356651a70d07cf6dfe777c639f0983fdb2` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/DupNOperationBenchmark.java | 1785 | `5164b4752c8cb3995caaca7e47165699e102c2d4239cab03cace5fc9d38f9529` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/DupOperationBenchmark.java | 2579 | `0494b50a33893a81772acb8ef5659cc8066f1a1daa00f0445bb82cfc1127bafa` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/EqOperationBenchmark.java | 7014 | `b972c57fd817692663aa9c086c1de68922929b50f3f5bf61e5a57f25c96751e9` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/ExchangeOperationBenchmark.java | 1905 | `6bf7d7d91b183c70ebdb525307d2dac032122c075a1a5f2aadb4ca7a8feb841c` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/ExpOperationBenchmark.java | 1295 | `d5c7d817662634e805f5c99164223fe07684b6f97beb7d901af57aaac7480877` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/GasCostBenchmark.java | 980 | `aa2fcfdf091d8dbc22ec5199553ec73d4ce0e4ab50e80c4b8b67917bed264cc0` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/GasFormulas.java | 1589 | `7c459e5f4ac04f405aeaad7c35f06f80aed0f0712cc73f57335b32406af22aae` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/GasProfiler.java | 7130 | `6c0ed71cb504b1a285573b0e8fb3d69634ca09c94fe5a62152002119959e2eca` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/GtOperationBenchmark.java | 1335 | `0129dc1e196b64329ad95b463c6a5d48a0f33fb88f6f51501a101e8851c9859d` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/ImmediateByteOperationBenchmark.java | 3706 | `66be7b9b3190640cfaadb5e4d5af076e06b69a58cdd8f06ed2f7579c721ac651` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/Keccak256Benchmark.java | 2548 | `d658512db4c8a1d19191a6b3a02a841e1dacc49c87fae453fa56ce60e0dd414a` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/LtOperationBenchmark.java | 1335 | `d8880ab3345f679ee7a7063ae82e4ec8aae83bd31ac728ea0eb7bbe1af1f8037` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/ModOperationBenchmark.java | 1934 | `550c57408d6386894379f4fdb82af0a71b93ed4111025521d40d59d75a3c2561` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/MulModOperationBenchmark.java | 2872 | `e1d6647cba2d99b7472b732b9ff8721f50596d8fb2e750bfc43e816619437d38` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/MulOperationBenchmark.java | 1587 | `c34e0645c3e40dbf274b3c3efbae89d0b29ac16807dc2f386f36d851e6088afe` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/MulOperationOptimizedBenchmark.java | 1623 | `9cc1d4f2ab5b3ec09daf7dc77c791c1030e6e06b720d8caab45983a4d72af91e` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/NotOperationBenchmark.java | 1338 | `1d2eef80f27d39cccd8e200dbb40597c61525d2537734434d73305a47707ffc1` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/NotOperationOptimizedBenchmark.java | 1378 | `c68c3b1376aad8eaba18590b57df69664f7ce516b7b0956d11f98ed3307d537b` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/OperandStackBenchmark.java | 2214 | `679117665970b621d335d6880c68556ac3ead63eb2a072f2e144d05dbaaf7cdb` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/OperationBenchmarkHelper.java | 5915 | `9657f63a5bb7c8729b300f94e08ea9ba8e910b1bb41e82dd0ee1afc9df4ae114` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/OrOperationBenchmark.java | 1335 | `ea162a2cb95d8eda43dc385d602ebf13c01170aa502cf9fcaf7e5a6f4f1cc73d` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/OrOperationOptimizedBenchmark.java | 1375 | `abf5e04169cdc2a56a424db01b9a427b3f327f379b03e0ba922b6872fbc792f2` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/PopOperationBenchmark.java | 2731 | `75f1da408c0127d546dce4501c2782fad8d5d3033ad4fea8f1b448ce92bed1fd` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/Push0OperationBenchmark.java | 1938 | `f21b5cb547f96a8e3acba8fd5f7417130c2fd3cfcc08f30082a0d479600936fb` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/PushOperationBenchmark.java | 2024 | `f820e7ae00f03bbfec410794ffcf1e5bdc3dfc64f094790978a657a02bbe6766` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/PushOperationBenchmarkBase.java | 4741 | `afdf8621a664d4c0171c530384374718323aaf90cd73032ba868fb7e4982ab0e` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/SDivOperationBenchmark.java | 2001 | `d804169acbe0c34ffc07efa01b931a64e5d525c72feb872a98c11e4b7bd3ceca` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/SHA256Benchmark.java | 2430 | `a00ead1a1e6d5d69f7c12628c25283689617ba4934584d2e4c1cc0d62ea2a77e` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/SLtOperationBenchmark.java | 1339 | `d9b5375aa080d17248aa60ba5c75b193300c5abd10e6aac1c19763430fed8f39` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/SModOperationBenchmark.java | 1981 | `27bbb12fdc4db1cff0c21eb7a0166ab76b3f3bcfbcec01515109403ac2dc90c2` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/SarOperationBenchmark.java | 1426 | `132c2c855b7fc639e1b36da08af3803560ed0b7fe016c3202aa2a5da8c16a288` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/SarOperationOptimizedBenchmark.java | 1463 | `678cc1c113be48adcdcb20000d9555c62fd6c79746294517b28e13b8340c2da1` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/SelfBalanceOperationBenchmark.java | 3916 | `2536fd02f90c36df02577828bbad93feb52bde31852c58714acff7d9687e1905` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/ShlOperationBenchmark.java | 1416 | `2de999d1b6a09943f74d2849e2812ba4c5b7edb0b9e6fb5bd5927c5e7417a53a` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/ShlOperationOptimizedBenchmark.java | 1453 | `754b5c853c282227c0aa98245940634276a00b08f4cafd03e93bf0858064f911` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/ShrOperationBenchmark.java | 1425 | `44d78b92fa90f4dcd5e102b4127d4df92b6c1e856b4e5730fd0a97e1e55f1d61` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/ShrOperationOptimizedBenchmark.java | 1462 | `33a8869aa722bf4d629dcbbb6248cb63d98e5f7203c1c2bb6684d4e31ceecb90` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/SignExtendOperationBenchmark.java | 1371 | `2584ca696acfd60e4580c7c4b64b1ebe507c6be3499be62372854691701b7fd6` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/SignedBinaryArithmeticOperationBenchmark.java | 2400 | `b0551677748535b0094259a84064888ba170212a6d6c9e3dc8efdd6a8d79571e` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/SubOperationBenchmark.java | 1587 | `78a85198bf6e2e65483a22279277709d84dce375e1b15556abe6ecd9fa2134f8` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/SubOperationOptimizedBenchmark.java | 1623 | `02d0089a82e0f0a465f42909bfc380bdf6444c9cbb7a0972864e63a26cb924f7` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/SwapNOperationBenchmark.java | 1796 | `648b764ee6660b31a330dd7d1bba6040e5cdf00396a5160ea3b3d4804b0adc1d` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/SwapOperationBenchmark.java | 2561 | `11144c4fb4d1f681d71068d04509c2171d35b8b845147d0caa125d320781bde7` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/TLoadOperationBenchmark.java | 4274 | `a4a615c5cbe65ba45d7ab89edff8d76c6b2ebd5eeb167390715b3933576b6326` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/TStoreOperationBenchmark.java | 5263 | `5bc31b9411558d0572bd39972b881cfbce1c5d06e0814557f3391c40f0d9b7de` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/TernaryArithmeticOperationBenchmark.java | 6025 | `f036afcd9b1f87edbc45eef68d8e95f5bad23bf557cb9594278ebd0191d277ef` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/TernaryOperationBaselineBenchmark.java | 1150 | `861164538d0a0300970ee7573b4e66589e2198acc27609b2b1b932ca1fb930ff` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/TernaryOperationBenchmark.java | 2489 | `b28b960d7632fdc73ada02578c745839797a5c577eb35beba0e6a6c2a8d725c4` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/ToFastHexBenchmark.java | 3710 | `d546ee4f6a92cb3460c3aac374ebe1a9ad0edcc89866fab8f2a7af29d8cc3547` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/UnaryOperationBenchmark.java | 2236 | `740e469f6469274add10eee0978176eb5c9c33adf3e6732def72221b9ea6f8bb` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/XorOperationBenchmark.java | 1339 | `a2d74c200130a34490d354a13598cecdca21f49af0d793f7dfa7051e1c2bb5cc` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/XorOperationOptimizedBenchmark.java | 1379 | `69d67948dc095bb3628c8e3fc4cc0c6ced08e05d54e1dc7d4c0f43489ba279c2` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/AbstractShiftOperationBenchmarkV2.java | 3541 | `54fc404b9d0f19fdcada417ae595366caf3ad16794069bf70b028bff648fc30b` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/AddModOperationBenchmarkV2.java | 2471 | `cff51f55539408281f2399e50a764ef02bb4865154625ec5492fa2f445b449be` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/AddOperationBenchmarkV2.java | 1314 | `c0b147fcfbf83cd4cba0f3d54f65a4c0faf37e53ae9dd6de949dd99c0f20ff12` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/AndOperationBenchmarkV2.java | 1069 | `90022dcc7e268d678403b4ebb26ce5a7dba9ef861fa69f67b860eed036193179` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/BenchmarkHelperV2.java | 6433 | `da8f5edcd1c343f3101e94604eb9ddfa459a8f3a667467a450e0bd01e599d342` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/BinaryArithmeticOperationBenchmarkV2.java | 5872 | `84ead7d7eb2356badb2bf9d7fd5831a0cc02ebcb61dff75f9ddaf53cd7dea6a4` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/BinaryOperationBenchmarkV2.java | 2437 | `67e9d89350d32c87ac996379fd49cd11a0447d7dc4f3daf388b6fa25dc585573` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/BlobHashOperationBenchmarkV1.java | 2696 | `977302f19deb60d16538557dda612914f597559da6d16cd1cd50abd820203d26` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/BlobHashOperationBenchmarkV2.java | 4396 | `0bd8eb6a99dc6fe04c26eda0ddac8ee4d673c03172f9684276bb0f83014eb4d7` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/BlockHashBenchmarkChain.java | 3316 | `4b7038828179243d796af24d4956b923b45d7a17ab77a99a95bd8a5551d28225` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/BlockHashOperationBenchmarkV1.java | 2521 | `5259aec0495d70c33df0013fcb85d5526c613b271bd2486e517980aac37d6f0b` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/BlockHashOperationBenchmarkV2.java | 3826 | `71c6b591b4982768a45b91d431e7dfe600e4c8478eaee429cd8a9eef30f0e322` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/DivOperationBenchmarkV2.java | 1749 | `333d5c9500e20490fe58af36ed6840a35b9fdb9822af2a34e3b71bbd5435d044` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/DupOperationBenchmarkV2.java | 2347 | `f1c8455efbf5f02fcb84fee0452d8a3e8d438fb7d4b0f4fd9357af5bb5099fc4` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/MemoryOperationBenchmarkV2.java | 5351 | `8ecb7fb40a7137e9112bd236484ad632860b60633e9e052f02c63045782cb7ae` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/ModOperationBenchmarkV2.java | 1634 | `a7162f1054c30c37105ca364720f89b1c840afe786d05b734a38f1475abd6dae` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/MulModOperationBenchmarkV2.java | 2466 | `378d26fb54728fa6f115c62383770b59f0c3701cd9cd96baa15b4a7a3638d067` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/MulOperationBenchmarkV2.java | 1314 | `d18a48af08eb7b5510e3008020d0a2b6efa2f8dbe314d93bfda829b427090804` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/NotOperationBenchmarkV2.java | 1068 | `29cdd3a769726d140a07ade14bc2dafe6a4b619154bbb07ed4add7cbca23863d` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/NumberOperationBenchmarkV1.java | 2842 | `9dcc69fd911a04dd918a1e164da310ca742cb18400e58a1898d9141e258c8f8b` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/NumberOperationBenchmarkV2.java | 2998 | `73cfed61490ec3a997d39621591987cd5d2b7fb9877671fe3bb56922dc438ff4` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/OrOperationBenchmarkV2.java | 1066 | `3d003d256df1ebbf8d196d0e6a920b16061ae380fd956754f56dc1deb034440a` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/PopOperationBenchmarkV2.java | 2513 | `32c7fe1667f2e39dfd8908caadbb46cc9f2467e7bf5406627cdb494a49e56f8c` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/PushOperationBenchmarkBaseV2.java | 4835 | `ced28fd998c73d25f4550569e8880386a68c6871dfefa5ac46cb4e1630936aff` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/PushOperationMultiLimbBenchmarkV2.java | 1983 | `66f1bf3f2d81d779049d45ae4a07037efc281f4702441920775b63f70a61d9c4` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/PushOperationSingleByteBenchmarkV2.java | 2172 | `d13528e6e248042d45c8bac08bb09cd8c65b537aa6d1daffbb8c30aa59522992` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/PushOperationSingleLimbBenchmarkV2.java | 1976 | `afabec739d4508be545b73a965d8d0dfb7f687fc13f2d4c0462ac8fe635ac2b9` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/SDivOperationBenchmarkV2.java | 1700 | `e00d2e773175574edfec57593ec0d224d2b43bc06825f34156a17fd7be5d9e9a` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/SModOperationBenchmarkV2.java | 1680 | `12becdde9f2f64c1783fe41a3aa3da46d9df9219da87fc79d181e7fa608dc251` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/SarOperationBenchmarkV2.java | 4775 | `275dd7fc29ad4e6951cf42286565f729b04e1a5b00c1eac4f71fe3efc2f5e8ad` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/SelfBalanceOperationBenchmarkV2.java | 3870 | `1824bf24b31ab8708b4f5cd550fcc42861b5c5e3f1233611b510ce398227fd57` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/ShlOperationBenchmarkV2.java | 1076 | `cb5fa10c88d7bffaf803b29ab2f83917b7b6dbd2e073281cab690ef483890af5` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/ShrOperationBenchmarkV2.java | 1076 | `00ff3edeb7052870fb3a31950483d9b87cb7ce78507599bf94bcf0a297b7d0aa` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/SignedBinaryArithmeticOperationBenchmarkV2.java | 2418 | `202f9a568b4d4b78ab1a929c747f10425fc1c9bbb647958a392c6f59086660a4` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/SubOperationBenchmarkV2.java | 1314 | `7a70e4c9335b85c2371cb3e63e3b0b8166a825e4c2d8bb9cd0e306618a049e19` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/SwapOperationBenchmarkV2.java | 2310 | `ea4b49a4d397b152b5f567c5eaa943f0f37e9319c97f62fd43791c93f0438e27` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/TernaryArithmeticBenchmarkV2.java | 6158 | `e5eee0868f44965111238c84547dd9ccb8fa93f394fd2bf056bbf77ed5d27a6a` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/TernaryOperationBenchmarkV2.java | 2607 | `ad93d5c94f7089509c497bb9ba93b3ee45b2a3c9f4fb0661e5526d69955ff66d` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/TimestampOperationBenchmarkV1.java | 2872 | `e7d6c80dadde6bb9d4a8eab91c9873dd1fb142a38e534f2778e5ca4c53e9a66b` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/TimestampOperationBenchmarkV2.java | 3046 | `38590dbdbbf36735c4727c7f16df11671d27111090258f93e7325cf7eacf1b56` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/UnaryOperationBenchmarkV2.java | 2267 | `a19adaf49674ee307466d4f2450bd3cedf05f7033ea02a7d8968a55aaf7e14c3` | 0 |
| ethereum/core/src/jmh/java/org/hyperledger/besu/ethereum/vm/operations/v2/XorOperationBenchmarkV2.java | 1069 | `cf95abe78b4b1fd5acf304134e8105724c81f00964d824619cf442efb486b836` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/BlockProcessingOutputs.java | 9343 | `27e2a8a6595601fd82fae4f512f41974fda5f2df73a7871fc20c7b9ab45ae160` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/BlockProcessingResult.java | 8062 | `da97c0b70ed64961499b871b502bea022eb3148fd227bc6d44402e2df52a2ff6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/BlockValidationResult.java | 4953 | `32d9aa2acdd6e8b37e3cd1f2fbefe9175bcb5520f9a6aa8e5e9678ac0471ba97` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/BlockValidator.java | 6568 | `cf92415e4f26ed1fdcdbfe50707cd3f93965cf925f45e323dae183e849e7d3c2` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/ConsensusContext.java | 1496 | `7434c6a35a434a5ac709b0aef3ab1c4b5385cc012c436354c006a18c8602ed6a` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/GasLimitCalculator.java | 4163 | `c9f5ac0d71e9c6c6a78aff2251860711ab2474129f3849d1505ea5b3d5e29bf1` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/MainnetBlockValidator.java | 21967 | `13894ba53a42fe8f9bd7edb86de96d3c4d858906107aeba951a0f8294fc3f4b6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/MainnetBlockValidatorBuilder.java | 3040 | `693ce8f1c11f4fa291083a17a44bb41550eca9b63e8634286c48adc12dcb3b51` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/ProtocolContext.java | 7837 | `86950b56cac168135675d591b551fbaa213340f4157c5513cdcbc4db00ec2bf9` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/BadBlockCause.java | 2064 | `e837de409fb970b59f69852a13915b6bb77c8137d005bb4da429bff8cbd223a9` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/BadBlockManager.java | 18781 | `1ee47d9c47640c41446d74845d63e86c84e1fe1099b8f9dd6014189b9b9d87fc` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/BlockAddedEvent.java | 5934 | `64c7750bdf666c0cd5e8d8da2ed0891dbb1b69695f2e92e1fd4ad8514d737f90` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/BlockAddedObserver.java | 808 | `4fc702c0df2b3d81208067f339eb970cdd5d9b8060c8e0d3394af8d4c48c7618` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/Blockchain.java | 14083 | `22aa3112f7e16dd84d3ed5f44945c661c9000d2e24a3c02678381801e25561f8` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/BlockchainStorage.java | 5587 | `b76e8a6416123848e61d27b63892f69aae2ee38eb917b6b7e898f1b5583c8a58` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/ChainDataPruner.java | 15243 | `a4f8c8ffcda6db9238a4fb4981e2627dad6490480844ca4a09f676a42b8d317c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/ChainDataPrunerStorage.java | 4445 | `99b22f703869a85edf65323d8d91385dc72be3cfa7a001906d4d194659e70030` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/ChainHead.java | 1624 | `e8511c974ff147f02ab4fee3051ed638a661f0d60e20f19125c28cb738826dfb` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/ChainPrunerConfiguration.java | 2259 | `4b09f8e27e0c5923c17d70ded4f6101b2b4e7003d2d68a266a22a943b07b09f3` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/ChainReorgObserver.java | 851 | `c08430f15ec0f7a758d70e3af65fc29a5f717f29814d62e7eb9ee88510ef480e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/DefaultBlockchain.java | 57326 | `c84f1c8407c76daae5418e2073614576f1aa8451c6f5196a6ee0394c5ddaa3e5` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/GenesisState.java | 15140 | `56d1b8e5da7121fa79e55ce6e43d7d0f03fea44f5f7645ebc1b018dedde54f00` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/MinedBlockObserver.java | 789 | `50938b895d93c5b3b8d27c4981dd89fe91b2f8357fc084f7e020a125ad82a4db` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/MutableBlockchain.java | 8872 | `0a78f9ffad24fed192c16eb2e0cf6ff4344aa38142dfa61d81edbbd062aacfee` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/TransactionLocation.java | 2288 | `20de48f2b45b1177691f36f5ba7da9582a371f66fafa97d6dd954a91aa61721a` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/VariablesStorage.java | 2574 | `94e06909d326c87e17052252c55a7bd8f7f8127b18a94c3a01a81633767380cb` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/pluginadapter/BlockchainServiceImpl.java | 15467 | `8cf87bcc155b332c363191006ca7bdeaca870668a227c1fc1b94416ca2f8ea20` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/chain/pluginadapter/RlpConverterServiceImpl.java | 3368 | `4b895f3c7c578965f051c892d87c223f0326406cbaa5fec6f4718f92952f3523` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/components/ProtocolScheduleModule.java | 3781 | `2431ca7c73ed03a43db4acb0b692ce964c272f1e76318f3a6a86e412b99bb88c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/components/ProtocolSpecModule.java | 2249 | `6a0d6ce82b6f411a2dd1c6db33b3ad388076a79656d4d997b32d9b0d869e27f7` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/Block.java | 3334 | `8e94bd448dae819b3850cb6686ac4e3c6aaf26c16abacc401ea03dd0d1881e48` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/BlockBody.java | 6029 | `f249f488dfb2d5e40899464451d4ed97fd8c05f9e31bbc75baae21db51187990` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/BlockHeader.java | 19177 | `37611370b1a4531a8802e94df9e04f0d80fc51b4225ebe00b1927dafebe4b97d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/BlockHeaderBuilder.java | 19419 | `af966c7048f7742e5ab9ffb253cf194c8c3c02b3c2a7418620ca5b21c8ba3b69` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/BlockHeaderFunctions.java | 2122 | `81a78249a79c9497d329b55d082df6bf4f60732bba7d6a632ae92341192adeda` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/BlockImporter.java | 4541 | `ffe561e40c1a0eb875ea05d6cc9981d3bae5bfb5e60ed9f0073252bf8784fe09` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/BlockValueCalculator.java | 1644 | `f45501baebb2caee1492c206308c90ff178e7d1b5892c01562f1e6b90a55d9b7` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/BlockWithReceipts.java | 1988 | `ff5b8fa0911457b7801d191483899367ee0b01031f978892b4371b5b4ef3cdd1` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/CodeDelegation.java | 8451 | `33a054efb69c856f2645cb2150e1a6f05f3da22a62d547870c617f615b2b5f8b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/DefaultSyncStatus.java | 2301 | `4b2be36a77ada2086562279dc5a4cf1a89051a33066e1c435cbb46a11f48ee30` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/Difficulty.java | 2621 | `f108cb0eea5aed30d9f1c96573959ed0f4e78a5ebd954cf68b84572e5e5f8c21` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/GasAndAccessedState.java | 1792 | `5fd24e09d41c2e46606b23706a7229ff7a250ca5858adad39828de3a563b014f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/LogWithMetadata.java | 6221 | `d2112767d42d24ef8cb574f31bf4c00ae4b65a3f946c790aefedd9bfbd826c33` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/LogsWrapper.java | 1310 | `65512c32eea0cd422688d4c633767fef6b34020008ab65725097cc0b033fe6f9` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/MiningConfiguration.java | 12715 | `ed718c29807481d659b8befc4fc0acecbc3bccb98e48731bb3a5150d42520a6a` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/MiningParametersMetrics.java | 1626 | `1e8d2ceb80934731101dfd6faf2adeafebead6b8520b5e52549471f737ad2bc9` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/ParsedExtraData.java | 816 | `ee21caec513c10792453667ac0c3a2f3f912affe49091dfe245a0784a795a335` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/Payload.java | 1824 | `46102e3fe736bac6496ecf40e8e12bcd002c01fea2d66976b0845eeb9255c496` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/PermissionTransactionFilter.java | 833 | `c4a0a6c76cf811f47e0cb0f76fb274b6a129cc60b287dd671c93f8cc1779c62b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/ProcessableBlockHeader.java | 6089 | `bbca7cc5b94d76e0bfc4aafb29c306203bba02819a30c930c1faa760e7e08553` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/PropagatedBlockSource.java | 1843 | `6336ea3ec40196f741eb424734b1707ab3a978575be1c73d257d2b490551bf61` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/Request.java | 2607 | `5ffe31e08fa4b646c583ef86158cef152a5dc9139ef987c0114de76243ff4f5e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/SealableBlockHeader.java | 5236 | `7d250831bf02ac83cbf46cc650b426f15223b219474641e1ce357c48f25d17aa` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/SimulationCodeDelegation.java | 3516 | `dc6d35bd479916d9b862be99a7a9bd2c0a9bf43560c6e2b9d80d0ec59006348d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/SyncBlock.java | 1814 | `d34da02e31aa60ff6c1f8e9a10da5bd33084c70d0f364863b165cb416cd22da2` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/SyncBlockAccessList.java | 1477 | `4b6399989caf064455fdcf7c204034cf59261e58e5e8d713453df18f21dd9b2b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/SyncBlockBody.java | 6210 | `a75b8bbdd20be0d72ad495b4eefd3e5167f83cda338a2efb0a59d1dc446188c5` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/SyncBlockWithReceipts.java | 2048 | `53b1e10a3d49d0519378ed84f572a6382f9cbc05b21cb619aace7377390f332a` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/SyncTransactionReceipt.java | 2616 | `9e5b9c64dd8af639519dadd6081c62615ca6ff8c19550d227cab07d24c20ea54` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/Synchronizer.java | 4333 | `1e1904ef504a8b97ee1bcff974c9a210f9b3cb3aa383643cb40b1ee61b734bac` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/Transaction.java | 55488 | `bebfcfc90aca26d269606a8df07dab4b176f2d4c0fe4613251bd43b958c189dd` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/TransactionReceipt.java | 8536 | `d42e16a64991e4218789af8c9e69f94dc8f3b81c7d1e6e9db4b1b60b9f593e59` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/Util.java | 3521 | `841f9581d820ea228f25abbacdfafa5f958f41fc558cad62e97711a964db0b67` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/VersionMetadata.java | 7760 | `602560f8e0ef1e069bfe4ce934f6735c0deabb25286e7d2b67b223941bde6a44` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/Withdrawal.java | 3526 | `144e998263f1ecb949985cffa2f60652e99452ab4704dcf97366ce5c77212329` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/components/CoinbaseModule.java | 998 | `3a3f9dc8700254909f3cd91c33fc446187365674eb41aaf0869df28670eb6cad` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/components/EthereumCoreComponent.java | 1103 | `344bb67c7a42dbf0d19c198f68a83ecf2eea6525d7183ed1029818637ff4f3d7` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/components/MiningParametersModule.java | 2183 | `2cb4ba81cf628b3993eb3e35e5af85b8650d75a0fb4af632b23d5e2f051d21f3` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/AccessListTransactionDecoder.java | 3456 | `7a7b6f18c8f6bf944e8600b953e6e04646af3ea09c86eaaa4ecd18cd82733ed6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/AccessListTransactionEncoder.java | 3950 | `fef50c9beb2994e1c3fe466bf26df4fe566b6115a6293cd2cadfb94d41373fee` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/BlobPooledTransactionDecoder.java | 6220 | `0b29a03c2d5f3e4a70e30bbed73db2e32d7f4ac013c2ed67253f884fdc283a68` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/BlobPooledTransactionEncoder.java | 3526 | `7826c29862ef27fffba501ba06976277ec9ddcc4618c2ca7dfa496ef4d853bdc` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/BlobTransactionDecoder.java | 4261 | `5dce9f581925f4f4d66ff56c25d3c5d9a6b1e88f59673e3513b5b6bdf41e8cdf` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/BlobTransactionEncoder.java | 2320 | `f3da77b72f1b7bb667603baa77daa06895887c3b7c10badf32fd0457a21326db` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/BlockAccessListDecoder.java | 4769 | `69cea09faf49ea07bf30239b2992e9719f4a31d53a1e72e3b14fc41c1103d284` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/BlockAccessListEncoder.java | 2869 | `2d79d3883d8e0fc801403e6fc1684ea8a0d6941c62a2c32102a47aa54313036e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/BlockBodyEncoder.java | 1071 | `5b0b7880f7396068e0c9e720e9735b2606035f62f1dc4ba9296e2efdb47ab877` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/BlockHeaderEncoder.java | 964 | `eee5b01c7ba494afb3f3d9267773c67833b58e6ce5827c4ab3622ba4c4b2cb80` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/CodeDelegationTransactionDecoder.java | 4310 | `fb250f86403a24894351aafb6c9be47da329edd686121614ace6fb30a829a7e8` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/CodeDelegationTransactionEncoder.java | 3617 | `46b1ad2a4d9aa50459e237b53b92b525faa02c542ce6bddf70101f0d779a9315` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/DepositLogDecoder.java | 5561 | `0f5fb1e0fafdf05d8fb19c7d35460b157c9135f3673857f3fdfeecd8afa772b1` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/EIP1559TransactionDecoder.java | 3435 | `8cfd720b544aab82aec338925016e6faeeeecc4e8c8dc6c2e60f963ca3e6ba77` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/EIP1559TransactionEncoder.java | 1918 | `4c45d74077e1e86e4dc02b9058a9ff197f96f054b87660cf91b656ce5a4fd176` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/EncodingContext.java | 4467 | `a785a395d0ca4bd9af4be2368f3e680b7370ac236cb6403a72e299730fa8522b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/FrontierTransactionDecoder.java | 4390 | `b04aaac0bb62e0d87305b6b9c3df7051ad99e1c26b2298976f9acbac10babeb4` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/FrontierTransactionEncoder.java | 1585 | `85059c754621c4b8fdd8e26b4cc6e3dfb0bbcbfb622155f6f154cd44e30de71f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/TransactionDecoder.java | 8775 | `5af4552cf3bf7ee7aa80a690c91edf07c97629ccfb727cb4c6bb6d6c162b5301` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/TransactionEncoder.java | 5932 | `796af1bb3394fe88c855a0a0298b31bbaa682d15929fe9ceb1dc13bcbc371d2f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/WithdrawalDecoder.java | 1628 | `6c9b8248c7209a58a9966377d2d1d92cf10a923df918e4fa239fce957afbb03b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/WithdrawalEncoder.java | 1486 | `611be2ffa7a4495315280ce4951516a9bb77d2adde24734f38779e66880a561c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/receipt/SyncTransactionReceiptDecoder.java | 10905 | `94443926674d811a4ee5a3a895f5e0f3c4defe20df3b82c25bf1f806dbfd2656` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/receipt/SyncTransactionReceiptEncoder.java | 4870 | `63e3b365c5c2f4a671e495207860ad361a2666ab5e2b7e2c3d1330c8ac2ae22b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/receipt/TransactionReceiptDecoder.java | 12262 | `284e09af2ec746db453fe9f20cf1f0e42b07fb9b132dae591dc2f1c329042830` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/receipt/TransactionReceiptEncoder.java | 6091 | `e6fa13167fb73d57d32e5cc665bed9bea081d034a7bab9572d5963c5e520537c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/encoding/receipt/TransactionReceiptEncodingConfiguration.java | 4425 | `79719b390bd7cdda06ac7bf6b398fa6c920edf82a29435ab82465398225a5aab` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/feemarket/CoinbaseFeePriceCalculator.java | 1259 | `4b02fd0053e6959854b1b34fc7876729f06077e0c8e2c2bb64514068d9c4a2e0` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/feemarket/FeeMarketException.java | 1346 | `afbbf87a7e9d07789b29133e0167e673e94f81bc85194c8d6bab401b991366c2` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/feemarket/TransactionPriceCalculator.java | 1704 | `2b8cbaf72a3e902b7869cd509fb28fecf2eb0d5aa6af348397b0ac9a64c80cbe` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/json/BesuJsonModule.java | 2991 | `95fa251abe8f1118c8c1540483cf0b2a52d32384290aead4414e8385c2b09b24` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/json/BlobGasJson.java | 1948 | `22f2c84d496978f61db54458b9199bdbcc0adaaa2c6f06c03a76477fb11c4def` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/json/BlockAccessListJson.java | 2506 | `228c62030d49779920cd037dff1dec1e86f9551b58f59cc5810ad49e5786f2a6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/json/Bytes32Json.java | 2227 | `a3f71182dc1bcc3b06c78fa45ed110164d352a45151d84dede33e789d222f61e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/json/Bytes48Json.java | 2227 | `acc1199dfd03324730e3dad55b013b9ab70f4b21c6345bee9fce2c74f97c572c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/json/BytesJson.java | 2201 | `262860b05286d01b4669a37d8b2fc3004dad9e3dc8623daa627a87ba0892f58b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/json/ChainIdJson.java | 1669 | `651f21f1165c33637f8794becd05aae1a6c4573bcb4fe96388cab157d2c3f8b6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/json/LogsBloomFilterJson.java | 2024 | `d3739e122f47ac2390efb8496d6c721b1909bd4902b3b558b7ac2f861c3dc9ba` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/json/QuantityJson.java | 4136 | `d692fad642a49d190a696a46bf4799993982ba8bc277774dc5f7a7ab5b699224` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/json/TransactionJson.java | 2505 | `1f43843d73dfb1aa7b178caf21fa6c17c241e8b13ad4950bba12fe9d6e8dce08` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/json/UInt64Json.java | 1952 | `c03494e5b6ffa104928f8166470bfbbf618fd7e040d0e5e270fe3dedb227fd55` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/json/WeiJson.java | 1912 | `d99e9810aa3a44a75bfd08b3203d9a18fb74c5682906075341dd2eeb07b121cb` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/json/WithdrawalJson.java | 3093 | `40e3f9ad68c9145a584ce09f36a0be01cc8982636bcf6adbba1e9366a3cdb025` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/kzg/Blob.java | 2125 | `91a84d8f49aeb07dcf4650e179056a68a22d66f442dd4d18b419df20e12b551a` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/kzg/BlobProofBundle.java | 12556 | `f243893f4aa3bb29535f7956132c708e51bd9eb6d1443ec895b81803ca9a1535` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/kzg/BlobsWithCommitments.java | 21437 | `44155387591498f25c07aa1c49e1e3c0fd63af3fa2e6b885d850e9bff653484b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/kzg/CKZG4844Helper.java | 11564 | `afba1a747e11191e0d8c8e9a38a17d5c592554cb7c2e5abf33424fb43a266243` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/kzg/Cell.java | 2757 | `5246cf33231b49fb4aa6e891073fcd180af49bd21f0c339008a20987bd22e3d1` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/kzg/CellMask.java | 8395 | `bbcddbc1963cff17e455e0dc50d1e416bad4e8efd72fb1267e08aa9a9fd6f7af` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/kzg/CellsWithMask.java | 5945 | `9b53b2ded2aa88928f79544983697f059d9591587a4341ccdc967a1f542f1cc4` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/kzg/KZGCommitment.java | 2305 | `86204be0c4d39cfd3a67238f90cfc3cc2623dd676270b73246fa798ed18e4239` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/kzg/KZGProof.java | 2283 | `b2bd860730127187f9fffc05608d3a773d9cbe67269ec23662c760ec9b58cad4` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/plugins/PluginConfiguration.java | 2188 | `a9adaba9906ff14cb1037dc626a037ff7fa6ecdfaa2cb801e0bbb11c11c5cbd5` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/plugins/PluginInfo.java | 1286 | `4223cf7a2c728cf593e1f10153a37b27f9a246350caff830e88e36c1b715143d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/plugins/PluginsVerificationMode.java | 2178 | `5f8875bccea9cdfdc68923ae9a8816ee916cdc072a2036f0a346f701a642871f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/core/plugins/Subscriptions.java | 1521 | `7ac08796b67540acb1bf0fed0e83385a7c0f703ede25a52b9788a686937c27cb` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/debug/TraceOptions.java | 3820 | `fb0dabea7548fbbf972d30f2a71fc2badf6284aab0d6dfefe2a1a42ea68e5403` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/debug/TracerType.java | 3329 | `51fab8a0592292bca8bb2c3ccd4d1fcf9b7aafeadf8dc6e04ecc3b5227e48c18` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/difficulty/fixed/FixedDifficultyCalculators.java | 1569 | `1e4f835c4bc7831e7910595a903f26040a733ec14871793f3eb7f3da8c22536e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/difficulty/fixed/FixedDifficultyProtocolSchedule.java | 2977 | `003031ad7d365cbd458aa759131845ea7a5f9a9e40b811ad3985d41f18956e9f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/forkid/ForkId.java | 3210 | `9f3b47727fb16cf9ee1c2b73453fe6abb82b54c54560f4fd255fbf6de8882ea0` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/forkid/ForkIdManager.java | 8865 | `d546d0f2068f889fba52d70ccd5547b250c35216a9a5e2633ae81b2aed6f9567` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/AbstractBlockProcessor.java | 30318 | `6b4b2c4cd5b002cd456accaa318fd6ff25419a06a393b785ad0b51c1560316b1` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/AbstractGasLimitSpecification.java | 2017 | `d1990a20efa15d4856b046a2d4652a16cd6c7380996a26a8c2d47fda0160f708` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/AmsterdamTargetingGasLimitCalculator.java | 2132 | `0153efee4984cc32d6bb862e37483f805c384eda884af3cdc35015a2c804fc44` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/AttachedBlockHeaderValidationRule.java | 1319 | `d10edcb0dda9a8abce9bf4368d452573152c737ee41b8c0b1b5f84ac6cf2fdc0` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BalConfiguration.java | 2393 | `063280f447322bd14aac8ba63e120908911b745c87785d83dd7546befd522f17` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BaseFeeBlockBodyValidator.java | 2877 | `e4782eb682cc60b96a0596677676afadbe1ad9bdeece272e02b9587d3af6ba33` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BlockAccessListItemSizeCheck.java | 2012 | `3d5707ad5d919d72dbe033dce9324864a571efd10a21aedd5210eae24c972033` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BlockAccessListValidationError.java | 1032 | `37d60bf82c691718b122f53b84823eebba97aa5a99ad48131b6fd0535f846f86` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BlockAccessListValidator.java | 4547 | `67e319a47b6d1ba96c98247fe3625541f7ffb96be3d62d0225636bb522ab710d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BlockAwareJsonTracer.java | 4640 | `8e8906cf3e4fe926235cddbb76c0759cc9199306e13ca7ac773f2277dd9ffeae` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BlockBodyValidator.java | 4180 | `d38addd5c8a95cfa913195d50a203a7d6be9332e9712c6a47ab2f2baed619d7f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BlockExecutionContext.java | 11731 | `45fd26cef78bb205576740ca251a14b8844d7e290185855e82a8708fd6eb4e6f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BlockGasAccountingStrategy.java | 6760 | `233e7741f4beef1fbed451c434bc4b455c540fd1e60e2f8bcd76bba94eb4c637` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BlockGasUsedValidator.java | 3316 | `0b071954316fe63e98ac7575f23362f00a3f2b564beb526005304e128157fb1b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BlockHeaderValidator.java | 6069 | `63ec976ce4f38f10c7107a88683e769a4f6c36fb097ad734a6708fb6b65f58bc` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BlockImportResult.java | 1499 | `8ad11bc24731b3cbdab2684f46b1a385c44f4c9ef28cee72747385df9961c07f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BlockProcessingMetrics.java | 4390 | `1e95a8fb2dcc2d292cb2b25dd556dbbb041b5822fbbff6e6a0543ccad5c3aa74` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BlockProcessor.java | 1754 | `dbc7c08157a441c36973bd73798d8dda0b9df8f20ced354dc0aac697523797e5` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BlockRewardProcessor.java | 4582 | `ba1b85cb272236062a72c8927b5b0bb51730c1a546ffb65409930211d4ea3ee2` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BodyValidation.java | 5737 | `4f58f11e63c4560f108487121961a160c68d9c213bbdd0996a67122c3ffea0ba` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/BodyValidationMode.java | 1102 | `c05557013709cfdac215bb2f59b920fff83e79b2760a352799e6455fc725bef9` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/CancunTargetingGasLimitCalculator.java | 2745 | `71c56ac30b1a3818c6e5d374da383746ce83b404fce2c5e32bbe63af0c4bbb86` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/CodeDelegationProcessor.java | 8736 | `8b6188520be406ec8284171a509f4482eec9e8a98a7a0f4376fb308a5c0b8f3f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/CodeDelegationResult.java | 3301 | `8f93349a1a5cbecb1a9cdf91081d1f178fd5274aca823823107c088f20909763` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/DefaultProtocolSchedule.java | 7469 | `4d4eabd405fc43070ccd754b7e8d2933c2e93b8c15522af76c00a81284126f42` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/DetachedBlockHeaderValidationRule.java | 1180 | `028871c67a62505e6256d635c8848ae8a01c8b0d811fd1f2091dd9681ebfb66b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/DifficultyCalculator.java | 1119 | `1d2216d4bdde5f2bdcfda590fb23e0cc9357082e6dd57d02cd6f410a4436711e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/ExtendableTransactionValidator.java | 2919 | `97eb2bf0214b024be29c66ecdf6c0f67e16909246c9fd23e2155d5c7562f0c3d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/FrontierTargetingGasLimitCalculator.java | 2460 | `9d5dfa1de8192d84e234b502f44eed2d4812d5fafdee6886dfcf046c7305895f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/HeaderValidationMode.java | 1329 | `07f2e3a17043c910c0ad52743e8264ec7e5a424b0c61acd753949cf3ac9faed3` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/LondonTargetingGasLimitCalculator.java | 2338 | `64da311589c1c0b81db2fd3e0d9c76f78b56775e3a9814458e58ce2c04cf49a6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetBlobsValidator.java | 11246 | `aeb76c31869687328996dabd8514fb635b14a30fe1c1ba8dc95c500608f2f2eb` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetBlockAccessListValidator.java | 15050 | `db40b00a39cda9b55417741f8e31bc9082b03a2beaf709e96cd4826e1ee1525d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetBlockBodyValidator.java | 10578 | `4540664132dd4c580b21c60653664a51213fb999a2ea2cf4f44c8f50a433c794` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetBlockHeaderFunctions.java | 1477 | `4b52f2b14de5a6b0ca1131cd0cf1195f89224be835ea48e0f464a0c77b581de2` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetBlockHeaderValidator.java | 7984 | `3bfe34f944e9f73e598440abb8095b08b6d719eeec07e40a5425a086e1b54aa2` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetBlockImporter.java | 4286 | `f166d0da2e331406e6c57eb68dd9aaecd94e6d24b2f0404440c81e35380c9002` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetBlockProcessor.java | 2783 | `d450b2036b699286d0fd0d16eb867d34dac60731de6d45413a686c45ecd37599` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetBlockRewardProcessor.java | 3857 | `910be0c2847f8e6cb68878876ead8e0b069b20f484774b9286c1e2c07eec8098` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetDifficultyCalculators.java | 6202 | `e1e0609927ad475d6577ada10da8f37bdaec14116fe19afa1e3be2550eed5ed7` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetPrecompiledContractRegistries.java | 3820 | `6adb0777a05b1295952b66b7519b4d34d8574e6f3775b780e0244dbaa5b68950` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetProtocolSchedule.java | 7319 | `8f19d4167651c6ce293a66d41b8dcf936b2117538e320b4830f5776ba4bf65df` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetProtocolSpecFactory.java | 12074 | `b9379b7d0548141e223d3fa2798f506a8f803d39da5c41630a1060a9a83c0cb9` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetProtocolSpecs.java | 69045 | `d9979d3aa84ee13fe9d5d7d364b07021a991e3f304bfce728990625b061cdb69` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetTransactionProcessor.java | 47403 | `f829de60a88493e348d9fea446b715144eb8168dbffd9d658c35b2df1d00d4c6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MainnetTransactionValidator.java | 17878 | `ad0a8f454d969e6589fb62dbedcb89aa33681958e0b3c312f7ce6a314a7fb652` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/MiningBeneficiaryCalculator.java | 894 | `7102c2b01e135a34ac5422a69413e25ca8ec12aaaf5f1c4c42973f21aa7daba9` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/NoBlockRewardProcessor.java | 1726 | `bce16d854bf385f57615487e7dadf88c5f37c4f33cac845a476f1776778078e0` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/OsakaTargetingGasLimitCalculator.java | 5396 | `898b6610f3db349c8535030a0fb513033f1ab19f6a218134f5a13fed7fdd3ed9` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/PermissionTransactionValidator.java | 2959 | `f83fc6724b4f227ca78121c155151f8de728fcb4b0a9a5543c965c9967398019` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/PrecompiledContractConfiguration.java | 1132 | `3f5a9da622a53bf64307e9e16724ee45b49a756b393dbcc514d2992207d4b8b8` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/ProtocolSchedule.java | 3200 | `eac31d8be9453457ce3e495822a10396ee2c34408c3ce4bd234356f179ffaebd` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/ProtocolScheduleBuilder.java | 11568 | `bc44b94e5c89bef16ee5dd73c8b3a9379fea53069d5b0650fd2b5a9efa97b070` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/ProtocolSpecAdapters.java | 2000 | `8061b81cfd05899beca6fd6e0d780291d56e150706359946bc84b72fb84fe77d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/ProtocolSpecBuilder.java | 22290 | `5c8c603031cb226267cb2b2c54bc659f94302a2f7006abf3d8f078df42fb0338` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/ScheduleBasedBlockHeaderFunctions.java | 2011 | `9808d1e6cb4311a5bac93cdf58e2aed7f37414ffacdcd641f21d4a9344112167` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/TopLevelTransactionSupport.java | 8694 | `bbf4487551488f9a57abbcb58ebe6df965b827cacfc90d00ad12cd1f561cf931` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/TransactionGasAccounting.java | 4111 | `50219a0ec3e9e90115eb4101a81a50b22ce9760a5a03cf04a2bb530266091ec2` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/TransactionReceiptType.java | 725 | `1fbcd53fef302e3fd95349c79fe13951d3638cd932951d7918667ab956a0d253` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/TransactionValidationParams.java | 9082 | `0bbfdc41b900184e4e51f58f88086f498e2998508d1ce5d98d3018df6041c3e0` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/TransactionValidator.java | 2371 | `f4b64f42248b3696cb8faca42a352e423cb3be16ca7405139dbf0c5011f53dff` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/TransactionValidatorFactory.java | 4687 | `618fa8cd82b3268a94e9433422b985c9e795ae792630eae21fef7fae6cdc8150` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/ValidationResult.java | 2764 | `97283b6d1589bcf3e791441407a945df02ee2adeb80e19befa8a3d2caea54b40` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/WithdrawalsProcessor.java | 2056 | `96e1095a640ed1ef1005e61697087de63577df36a6fa7826761b33e4028e4e58` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/WithdrawalsValidator.java | 5109 | `d097e819de5f4a1111d1c63561eef204b7c6b3d5b0fcf109fdaf35b0a81dc0ce` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/block/access/list/AccessLocationTracker.java | 11867 | `d7289072bd1c8559e8977efa3792c17ac88de61a31445c3e7bdcd38bcd3417df` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/block/access/list/BlockAccessList.java | 18530 | `69f538fb2332e1f2cc7154e6ef46d622dd8f8733f3219eddbd3dbfb255e4df55` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/block/access/list/BlockAccessListAccountLookup.java | 4202 | `3b8520405be0b96281d27f4068bb8314458493ab61b0ec9431627092e767a424` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/block/access/list/BlockAccessListChanges.java | 3123 | `94ae2d5e35b324f5b026050405c4ce9813e8584aaf3f3a6ca4e8431e196b17b1` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/block/access/list/BlockAccessListFactory.java | 1273 | `527ba244390f003b15e89c23ab46769308e254ec569206ca7bf9e53cfdcbacf6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/block/access/list/BlockAccessListOverlay.java | 7426 | `c9feabc4433a4e35f5e21912d3eb406f064617dd1fc649c5f6615ec1d47f2970` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/block/access/list/PartialBlockAccessView.java | 8319 | `27ee3e01762ddd569c648aa084c247794d94d0f699183afdc0377c2fc9605ada` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/blockhash/CancunPreExecutionProcessor.java | 2412 | `7348ea0e2274c8c8b25750fe162b536062a1f69c9713a8e966346b4937817a54` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/blockhash/FrontierPreExecutionProcessor.java | 2147 | `d58bdcfd4cea71b074ab6f117377e456faabdac66c5aed34ed40e12f70fb5480` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/blockhash/PraguePreExecutionProcessor.java | 2871 | `bdcf53674e52fb8909cbeeeae0404383385bb456bcc16880100f02ffdb79e7b1` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/blockhash/PreExecutionProcessor.java | 1840 | `694721ed994e8a50f40e46fedbb23dfb0964d125f04fafdb2f04947d2374aef5` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/feemarket/BaseFeeMarket.java | 1767 | `f2c8bd620ea183e7fbfdfd3d206576a21286647a5d76eadf7c3f0be753bef8c3` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/feemarket/BlobFeeMarket.java | 2711 | `6d685a184ef72bec528b8addecfa41d41446468b4e1d0469379364c9892b275f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/feemarket/ExcessBlobGasCalculator.java | 1769 | `b1d97ada782429e0122ef093096a7f5f53538b313b55503e3d5f66f146c06f4e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/feemarket/FeeMarket.java | 6964 | `d29ae55d1953fa1b5eb03fd8cb6238983a3bb2f784f9fc5918a81838a1c39115` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/feemarket/FixedBaseFeeMarket.java | 1310 | `1624d20f8143a89c8aaa0b1378f14e61f779b41e9665e9203b2f6bb1fb5b0bcb` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/feemarket/LegacyFeeMarket.java | 1240 | `d6baf39aec2822c9914b14e0a945ff690ceb7cedade91cbe693eb0cc1125e8a2` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/feemarket/LondonFeeMarket.java | 4793 | `ecfbf90b94d89d69d793b977a94eb8505f7765d184ee6480731112d7a22d6da0` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/feemarket/ZeroBaseFeeMarket.java | 1031 | `375af1218f12b6ae6959236ad8425d588f14423bebfe5d20fe2ab1ddaf51640c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/feemarket/ZeroBlobFeeMarket.java | 915 | `c5b97a85c35b5d4c6d4f8d6fe68fb8ac5820160ffa223e731e50160c87fd6cde` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/AncestryValidationRule.java | 1880 | `36db7dac5d913d2b795ea507395d3d04218a0c61bae5dfe329d18d5e283e3ea6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/AttachedComposedFromDetachedRule.java | 1723 | `f00f0695a457f447f0d1226d7c7257371e029940fa6039f7aa2c63a7c965bccf` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/BaseFeeMarketBlockHeaderGasPriceValidationRule.java | 3281 | `e5cb4ddf63106dd04dec768a0c989378c032ad6f7e5f37c2bb2716d8ebadee80` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/BlobGasValidationRule.java | 3543 | `0de0a13720f7734ab9468c5c09733475afc20d47e27856558b98e0a55aeaaa62` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/ConstantFieldValidationRule.java | 2011 | `56a1f2daddc3a2826441e6b53adb2cfab59c8ee981237c2949fc77ec37774ff8` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/ConstantOmmersHashRule.java | 1518 | `b164d6f805bb4cca42a27bb92d6f3ae0e5e03013884a76b9852046a8729d5119` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/ExtraDataMaxLengthValidationRule.java | 2000 | `6d8b55afd7ed7ab7f1e658548355551e1a56b2f7770644cda605fef6e8c0d646` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/GasLimitRangeAndDeltaValidationRule.java | 3475 | `407aab7353a3be99544b615636eb2b7d0fa9368682c64038e4ddf20fdd27170f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/GasUsageValidationRule.java | 1662 | `f14eba1605f76abbc6891a6aa6a0f0ffb63dd18ed104c48e5c4e1404a16c6ed2` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/IncrementalTimestampRule.java | 1395 | `759c4a1cdcd1e8425d01ff8bd42549528cb09f039638645cc84e3d1edad622f9` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/NoBlobRule.java | 1269 | `305b0aaadcab87b50b7144c98598d5ccf29ffc8327965f611d1e80ab21adaac6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/NoDifficultyRule.java | 1345 | `6c6db7206562b4a8715b189e0f5028ebb79a7aaa2987f497ceada351902da0cf` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/NoNonceRule.java | 1222 | `587bcc7fb9758b3a3429f1502cc4fef65702a39d5935a4ab79c021c7d8bdc68c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/RequestsHashPresentValidationRule.java | 1938 | `6fe172d1a0b4edbefbda37d55ea8080c58b4c3b32919fe04660edd125c438435` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/SlotNumberPresentValidationRule.java | 1747 | `cb3bfdeda7d29e4c11863fd2891c33ec0005b24a9f14ebecdbfc1411e8e12330` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/TimestampBoundedByFutureParameter.java | 2442 | `81da6867629c7a55f969272cb2cf69acc249a2b2798fc3b07a98e9704a724490` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/headervalidationrules/TimestampMoreRecentThanParent.java | 2584 | `079b9a4f08dfb09a4523cc3e6ab0554e2ea30ef37e1088da569bac39890bd31f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/inclusionlist/InclusionListTransactions.java | 5227 | `ef40f247d063d98de73ff9e14c0027ad26c06049c59fd6774f6ed4040ff6ef2c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/inclusionlist/InclusionListValidationResult.java | 1960 | `1b103ec2ad56a012f8ceaf6c8dbe08aaf48d34fbe0d5d32cf0886910fd231ea4` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/inclusionlist/InclusionListValidator.java | 7177 | `5128b674c4b89437d323b0f684eec7d2870ba6c64676ae210c84fc06bf48d64d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/milestones/MilestoneDefinition.java | 1697 | `84ef55da9b92df9416033221d025f04deef33ca6b08a3f35e251e0c49c6461b1` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/milestones/MilestoneDefinitions.java | 7180 | `2a5b3d558a40a7317b0df16b3db296b169cace9e6477fe137a387438cd260167` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/milestones/MilestoneType.java | 746 | `224c3e4c3f5774f504b13a3d5247ce42885e5b3874be65875f6d4987b68aa657` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/parallelization/BalConcurrentTransactionProcessor.java | 10903 | `7d4ee3aa7fdf0ced701ad4efb940fab25443c8fc1cab70e5921c8b67e3195c21` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/parallelization/BlockProcessingExecutors.java | 6210 | `0c7e273fe09cd1a2b6b410b1957c35b2415478c0bd0980948f54a10ecab9e175` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/parallelization/MainnetParallelBlockProcessor.java | 10936 | `acc98d52ad76b39efc545be464ba107b64f3d996f85ded0b305740e9c791eaef` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/parallelization/OptimisticConcurrentTransactionProcessor.java | 13519 | `7653c480d7dca945b88954afd540b08d5a1970bf80183aaf3191478a55dd39c2` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/parallelization/ParallelBlockTransactionProcessor.java | 4801 | `e1d713fbe63f563a6239e26c290a491c28adc12f62d4a3cd1ca40308d47a1f8a` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/parallelization/ParallelizedTransactionContext.java | 5159 | `925aa7d516772b42bed6d315fd5b226ed502b8f6c265e39632a2d06ec5e3d4a0` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/parallelization/TransactionCollisionDetector.java | 10208 | `00303dd5c6644a57f5e7d483da7dd2eaa9e1181d4caac169093917beeec5b699` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/parallelization/prefetch/BalPrefetcher.java | 10114 | `686431eb3a4e7be995e85384e85510a435381f135728bd898fd9ffb20188a603` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/pluginadapter/TransactionValidatorServiceImpl.java | 1801 | `ee20c8b1984adc18127539cd599e8484f3c3533d4657b54945a8bbd01869cb34` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/requests/DepositRequestProcessor.java | 3190 | `a23edfaec2f3ba2bd16e75759046e07e34915cd4518853309dadd6ec27648c40` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/requests/InvalidDepositLogLayoutException.java | 859 | `e2f58b4059e067e44f87da3108ee13e9a9818faaa9ac544a055fa86109f9268e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/requests/MainnetRequestsProcessor.java | 3174 | `5499f05a41845e563202a5a444a53e8a1c7d154f9717fb79e60fdb3825eaf58f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/requests/MainnetRequestsValidator.java | 2758 | `14b125a237ee3d4735c26f4cc0956f0f53ca3809187f69d6635c5045d5695b83` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/requests/ProhibitedRequestValidator.java | 1278 | `4e3a5f0591cf3077b7eea9a40aa8e46ca5f30e300d1d09ba031be492b648530c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/requests/RequestContractAddresses.java | 5006 | `a076171bab27493c28d05c4f86c8ac0cb263a77f3c5ced484285bca1dcc4e84c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/requests/RequestProcessingContext.java | 1526 | `55f2e4422b9d8a1f114fd6bf0d80e813c624cf801d87ae8e3ae815cf0e88f120` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/requests/RequestProcessor.java | 1164 | `13b87b4a66479397a9d55e6141eb63ba8f29fd4054de7bd30602a14294e87b32` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/requests/RequestProcessorCoordinator.java | 3447 | `38053e9961fddedee377b519da3d3a22fb84109acd88c1e6edbbe06db0e50147` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/requests/RequestsValidator.java | 887 | `2dcf5bad488f0d6bbaf1a890dba91d8ad5e6aae89b2eec4b5f6a336b3424c7d6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/requests/SystemCallRequestProcessor.java | 2534 | `2c4102c8921ca5476d05091b0bceb4843eecfce2a24504c05cd9caa223e46476` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/staterootcommitter/BalStateRootCommitter.java | 17784 | `79293c6fa0814246711ec8cc38bd9a7a8f41d6683ee5c8e10f1c131781dcdaca` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/staterootcommitter/DefaultStateRootCommitter.java | 16086 | `0ad203b5a6764345b0eea50e0c35f456778d751c30413ad609b436aeb7df065d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/staterootcommitter/ForestStateRootCommitter.java | 1558 | `c4b634465037f433177036abdeb3cb11a4235952c7630dea7d2cbf932f84b538` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/staterootcommitter/StateRootCommitterFactory.java | 3434 | `f188a990ecced044fad4d0fe0ede2ee642af3e86d191045d62a8e744b94e3a80` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/staterootcommitter/StateRootComputations.java | 2268 | `0208fdf24feb5e878b0af76770c8c8219d3c4ca1e1c899c1604674efb4b8569e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/staterootcommitter/TrieDisabledStateRootCommitter.java | 7643 | `e38cb85a8cde2b532d3bfbb4503fd6aff36454c6beb736aa538d6d99cce7f494` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/staterootcommitter/WriteSink.java | 5303 | `e99e5d5b5311dc60551231836c3c054e27ae4daffa7f9f047284915df7c36ab4` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/systemcall/BlockContextProcessor.java | 974 | `65a82328e131cf868a3415d1ee2f7b0298d8f402e7bdb412284c77195be6dc94` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/systemcall/BlockProcessingContext.java | 2569 | `6d5fd32262008c7b4fa3b2ed404a74c7e7ca528d683746560cfe46c64e961428` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/systemcall/SystemCallNoCodeAtAddressException.java | 857 | `2f9e25e6b60602aa137b47a6ec303e7ef23679524367b12dac69d4b6685bbc11` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/systemcall/SystemCallProcessor.java | 11339 | `811063cbf4941f757fa8aeb53b3d56751c4c830273b2df71354e09df4346b16e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/transactionpool/OsakaTransactionPoolPreProcessor.java | 3165 | `ebe9c6212cb8c799133bc488875b4132916ee3b73f96f1318edf31abe064abe2` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/mainnet/transactionpool/TransactionPoolPreProcessor.java | 1351 | `9ac28a225d6681a269a413dc74651ec96af1aa709cceee5e9f052b4fe11a1dc7` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/processing/TransactionProcessingResult.java | 17187 | `7243a8884db388d93e7270a6bab8929fe9599135a4d157f8a79e84d9ed7490a4` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/proof/WorldStateProof.java | 2671 | `953737f17e4987e5f5ca40c72ff0b378d76f5f636d14dacd5f4d8a4ecda5cfdd` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/proof/WorldStateProofProvider.java | 10748 | `5a46dc261b36aa987bfbb354756093d3527603fac2907dc9759e80ed78e4b8b4` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/storage/StorageProvider.java | 2189 | `c3f89e3ce7d548111595f382b5ada1ed7ac2efa772d863974c1cdafb0970dd05` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/storage/keyvalue/KeyValueSegmentIdentifier.java | 5902 | `ab67d000350bc67b6d41f7ac6bca48eb4db11379b40da1046fd644a21d9d3449` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/storage/keyvalue/KeyValueStoragePrefixedKeyBlockchainStorage.java | 21843 | `4a5dbe0d48288adc04dba6ab908f25e8c7cbfda54fdae1161d67fd39253c1023` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/storage/keyvalue/KeyValueStorageProvider.java | 5630 | `ea76b7985922d5878050e2f89b0794ee1643d9c03159393916143d4af5c0ae3f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/storage/keyvalue/KeyValueStorageProviderBuilder.java | 2668 | `cd705b34fd6038bd1f917c4964f978f234f7f4bfefd1446946a643af9ac32e5d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/storage/keyvalue/VariablesKeyValueStorage.java | 5417 | `e783bf748ed71b19904a8385b7b5ded11fad8819983cc391d3ef45d9cc50e678` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/storage/keyvalue/WorldStatePreimageKeyValueStorage.java | 2926 | `ea28964b13efa547fe480940a6765fa82598b09fff5e0d12e712e46fefd2c149` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/BlockCallSimulationResult.java | 4021 | `0e90c62c8c2fe74494851e50feb0a83b89a08ffe0d78f02a88a65e6c76457ed1` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/BlockSimulationParameter.java | 8717 | `6595a458e20783af0eda17b9a2ca42e1d81a8834b533ca5435360083d583d0ab` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/BlockSimulationResult.java | 4118 | `628a599fe45203efb19ae09d936b18875b839e431386d961019398a92e3d5e95` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/BlockSimulator.java | 39362 | `6330311353ff947c2eec9d1722ddde406466bf6b444053ea7a66b984548dd093` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/BlockStateCall.java | 1820 | `02f5bd8eaaeb76c7d45af340fdbcc1ff28f7a1ee068c7afb260189b5a789c584` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/BlockStateCallSimulationResult.java | 7726 | `6a395966a6b985b07efc742c31ab4de61281697498d26942077c2e88fd4085c6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/BlockStateCalls.java | 6565 | `821ae551df810b747abd49ffc51722e7eaf8f2def13f4001e0722f79268592b3` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/CallParameter.java | 6466 | `33d2a2090362d3a7a339ef551fd4d1b95c709a6912d131bc14f2a17837dc845d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/CodeDelegationParameterDeserializer.java | 2567 | `b787389eb7b1cc0a196d7a4aa3c9d333951339f3e74ce7c8fa1d7e2f763978e6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/PreCloseStateHandler.java | 2680 | `372f00f82e3332b90ece5b72b4cbbd3f6a1704cf852290ae593be9b8e61dda69` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/SimulationTransactionProcessorFactory.java | 5175 | `24b8a003a13857d0e822d91794520257c4d688f8f0f242976cbc0009b0c09be6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/TransactionInvalidReason.java | 2000 | `f92e4d8d7104814840a57d7c75b4e660fc8a8286f2eae35dcc8ffeacc697abc6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/TransactionSimulator.java | 30981 | `7dc03d95265c75cd769ecd08374fe410509814be55232743540fdab17398d966` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/TransactionSimulatorResult.java | 1567 | `42906a5e552c43ffec578e2faaa795657e3194911da1f6fe791b547b859823d3` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/exceptions/BlockStateCallError.java | 3020 | `c4ac3667508808343f4dc4b201b539e17ab80700de7043f919276ae7069beb0c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/exceptions/BlockStateCallException.java | 3352 | `3e8faa6886a917e1b08218418e8066cf425bce4c52d2767edb1735cbd9930efe` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/pluginadapter/BlockSimulatorServiceImpl.java | 9368 | `72d98d38067bf42c0854e6bf6184ea440986bf30ffe812913bfbe95ac50172e1` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/transaction/pluginadapter/TransactionSimulationServiceImpl.java | 6313 | `a34e49582afc757a4a16cc7dc362f8c0c859b0c1ee7cadeed7e2d6c0327e40cb` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/common/GenesisWorldStateProvider.java | 5036 | `9a7bd34db5befa9d57b1f3586446eb7bc163be6a21509a2f4c2abb3edba29270` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/common/MptStorageRootStrategy.java | 2368 | `d001a8362d18ae801e0e8cf0e42527169c959883c923afe075e40271ea66fd98` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/common/PatriciaTrieAccountValue.java | 4139 | `377d25d5f639a0891dd1c69b0b38047db019f53e1d00f7fd99b926d171cdf60b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/common/StateRootMismatchException.java | 1388 | `03185dcc71509fbf2482161f53abc80868a0cd28b08f504e475039fc2a09f01d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/common/StorageRootStrategy.java | 2269 | `97156bc81ff07eedbb0dc46f8d55bcc8b084d8d15eb32e6e54ab90f5e438e207` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/common/TrieAccountValue.java | 1371 | `7714584993e25960d3c67c7cc5bbbe8cfa043f547ed64bd0546d601d1c9124b4` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/forest/ForestWorldStateArchive.java | 4759 | `d619c341a0679725f03516e057ba6055e32fc16ca45fde91450238ae938d0b6d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/forest/storage/ForestWorldStateKeyValueStorage.java | 5723 | `30ab99902de44720081cb8a2f6d709d7168612f8a9a5d377604cbe599df1c1ab` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/forest/worldview/ForestMutableWorldState.java | 17273 | `d861a2e27b3331c899aea3c604c5eaa83cf8ffc8bbb8b7e88aa017fae6f357c4` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/account/BonsaiAccount.java | 12800 | `6bba551ea758c696f862dd79b0f64504b2225dbbccd9154f8a3d4d0f23dcd5cc` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/BonsaiArchiveContext.java | 1373 | `10dfb607e4528a8f36a7c2acdc2c32095f54a4ee17dda12fe9d9321b202733d9` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/BonsaiArchiveFlatDbStrategy.java | 21043 | `3733858f35d6b22bdaf280367dcff89d4cb87551875d79f2ba383c3a0351175f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/BonsaiArchiveReadFlatDbStrategyProvider.java | 2127 | `5b2d006b0a1805818f7f7c8105e37b785eb1b51fdab49e02f54d64b2ae1c29a4` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/BonsaiArchiveReadWorldStateStorageCoordinator.java | 2073 | `8fe99dc71cf9a9c26c9fb62b689e2dcd8a9efe6c907d1eb5d8f53aa42ded384e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/BonsaiArchiveWorldState.java | 2425 | `ca9859e042acef50a706d3ef865884f9f7a0a277210c130e3ec235826fdaab7d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/BonsaiArchiveWorldStateLayerStorage.java | 4613 | `9061a4ba8939111ab743cc4ff6a3e1f8a7fb054f70561282078836589fac59fa` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/BonsaiArchiveWorldStateProvider.java | 10623 | `11dd878538dc82907284cc38fe767a51bf5088adc8223657285d806335c03581` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/BonsaiFlatDbToArchiveMigrator.java | 15931 | `a2eb681d09c302e6acfe0b7fdcbda182cda22db467940b8d569a07e8ca827d67` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/trienode/ArchiveCoverageTracker.java | 3254 | `5f3d8ad8f497b4fb26d91846e1c76d60c002a07abe03cfdbdfdeacfd0c7c545e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/trienode/ArchiveHistoryReader.java | 5242 | `db623d37a5351904035f10f39cebcd9403166f0793961daaaccdb2793491240c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/trienode/ArchiveNodeHistoryStore.java | 6618 | `35c7388b24da7ed21074fed4d56f8e0af4271ea18b6f1734a23929386c5ac1b8` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/trienode/ArchiveNodeKey.java | 3924 | `57a45814e7685faaa34ab05056987f96c7cf1fae1208d9ffafa70c71a0eb8fd3` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/trienode/ArchiveReadTrieNodeStrategy.java | 2760 | `fa6352495f04bd48e6c222bc7d658b0ac396d626a53577bc473323672328095d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/trienode/ArchiveTrieNodeCodec.java | 5464 | `9752756172fa143dc3b450efddc10772f3d9ca4cab7ddaf7632de45cb1e76447` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/trienode/ArchiveTrieNodeEntry.java | 2917 | `e74e97de0a80f94481558cc4d8406d5a2d0657571295481838c3b21c932e472a` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/trienode/ArchiveTrieNodeStrategy.java | 9543 | `752a5f7eb7f93818c2d1b745571f3d589ad0e9b1f2d77d1355f3eeba0a84ab7e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/trienode/ArchiveTrieNodeWriter.java | 8128 | `e59e6387923b70395867430dad2913f94b6cf46fb0ef73b8034de57393c1620c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/archive/trienode/BinaryDiffCodec.java | 13786 | `4383ae23e3cbca4be812aa52bcd7c658b6e35aeb41717722aced739a7941e790` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/code/BonsaiCodeCache.java | 4178 | `5e5bea25ea93302266e6d8ca00d8a914bdbb0138e0aae19aa7bedfac43162899` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/code/BonsaiCodeCacheModule.java | 1333 | `a818d300fb13fab945d0683758f83e078ce2685e2282d720a4c3a0fea8ba01c7` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/code/CodeMemoryFootprint.java | 1836 | `2934737f94d74ab2bbd7fd6a8c34ab6fa466b11285433f4628969bc2a553a576` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/provider/BonsaiWorldStateProvider.java | 8740 | `95520dc69a68e8fbbeaea4faae6a2d2908649abed17e1d064d1510ed399aba9c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/provider/CodeFetcher.java | 1160 | `a2319e18badafededf668d2f4372e962b4d65c71aafa37b2561e692f15cdf1d6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/provider/PathBasedWorldStateProvider.java | 19937 | `a405f72d44bf3d623a99c4bb1bc9ac45260148a3b6b885b5394b6f4682bfbe53` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/BonsaiExecutionWitnessBuilder.java | 10154 | `a05ee20c38165f05d00d196e9b791724e0f9d24d1f4519c515a245dc7b249b69` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/BonsaiPreImageProxy.java | 2555 | `d4be1c38742a13a2fd58189ea7b87a291b92a0cae1a22679ad4e8dda60fbdcc7` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/BonsaiSnapshotWorldStateKeyValueStorage.java | 8130 | `154f63d0fef25cbf62daadc55eff3408e79f13fd7aa3e9baa92077a34567bc68` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/BonsaiWorldStateKeyValueStorage.java | 32876 | `858e28ecdef466b8282378fbaf105c64fbbedc85591c8a6142b255e1ec8da022` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/BonsaiWorldStateLayerStorage.java | 7266 | `1a9223a13778af8c05580d26f466b6b488bd2ae8151bb73c12c61f18947fe34f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/BonsaiWorldStateWitnessStorage.java | 7595 | `8c0b874d6647181bbcc8ff8ada3f036844473e3f6831465d9be11165af969949` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/StorageSubscriber.java | 938 | `a7341ff1813f3c7d666e81e959f377c40f7b28f3fdb5338fffdf06f5480be83f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/TrieBranchSegments.java | 1375 | `631c8b75f080ff58f5f2097797ce3afca8a5e5484234e6da39fb6da13f950b73` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/cache/FlatDbCacheManager.java | 5000 | `0f34cd22d232687621df3f004cba694ea7b70a11ede4772b5236c11d3df48277` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/cache/VersionedFlatDbCacheManager.java | 20373 | `8cd66b8ff73846a6f8b28193d387f74500c20e7c4cefc2a68c66d3c4463f3a9f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/code/AccountHashCodeStorageStrategy.java | 2188 | `a76970a2d7a022ee4d277009cd246df4a887d52965eed4372fc2eeb0f74b8b02` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/code/CodeHashCodeStorageStrategy.java | 2240 | `4a9b4cdd1a7aada14f545b66293d7f468fa8f035edf03c07641d17707c1e45d9` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/code/CodeStorageMigration.java | 3716 | `30c25192221f15e9d8b7fc06e08f42daefa90110bbc03b915dd9bc5cdb873400` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/code/CodeStorageStrategy.java | 2446 | `1e62d7742c8c747158ab12eee72f0522c53a555528db2a64bd86707af51b09a5` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/code/JumpDestCodeStorageStrategy.java | 6814 | `dda22e263735d886b488012d99ce73a2232cbfb8ac47354854d944fedc447da6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/flat/BonsaiFlatDbStrategy.java | 7537 | `a13ac7ac25bd1371e02f867ad134f8771748ef8d94776bddd5e12f68e55f8311` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/flat/BonsaiFlatDbStrategyProvider.java | 3607 | `d0082801efbc7a3aa2b55dfbd419acfbe10948aa144899d820c703571f4e35df` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/flat/BonsaiFullFlatDbStrategy.java | 5040 | `e68c9d0daf5b871ab564053dd0750b0c8d76243a54faa76b3eb782321ff6dd0c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/flat/BonsaiPartialFlatDbStrategy.java | 6572 | `91eddde5ee818562ce32f4f8762a53fbd5552087f3cbb3f4bcad8f3f3b1ff542` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/flat/FlatDbStrategy.java | 10144 | `57c82af0d0d0e06c8ef59b3d689fbf447786ecc99e520821db2c8d91247b45e0` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/flat/FlatDbStrategyProvider.java | 7941 | `6b4ec6a7f36da411d1992ca6311e9068e4b163783178dcfc37637756bcf9dcf5` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/trienode/BonsaiTrieNodeStrategy.java | 2375 | `d3885b90fe7b59eb2c9d0b4dac88e5ccf5c62e7c2feb488f9462a98c07379d2d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/trienode/TrieNodeKey.java | 2830 | `622fec6f762b0c6fa988c75021d6b8b4ce782f236e87e657f354281c03222a4a` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/storage/trienode/TrieNodeStrategy.java | 1954 | `cc5c9822aee2a7a2b000268c68f6368c10a33a7f73aee6df57d2ec9fb7a01f2c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/trielog/BonsaiTrieLogFactory.java | 9468 | `b39d8659151ddc90242932c2654858cec298ec1cbb680f757e009529e0a01759` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/trielog/NoOpTrieLogManager.java | 1836 | `cd19b6fd01136104f62cf72910839ac5dd896ad54c13cfe667397d12ce516bfb` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/trielog/TrieLogAddedEvent.java | 982 | `4bfbc5b7022bff424770625ded2e428cdd81333c8a7ede628866e07cbd121d7c` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/trielog/TrieLogChanges.java | 2494 | `6f03eb62d48dd4bcae562d2941eb73edaa731f45f5e8339240ce877563499cc6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/trielog/TrieLogLayer.java | 8918 | `61f7f9772bc8d4564f90c00ec833421583aac08815fa9331e96bd5dedecd5c4a` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/trielog/TrieLogManager.java | 10972 | `549c05bf82343a72262a9604d438543e94b7d28733de78dfd975f9ab76cfd6a4` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/trielog/TrieLogPruner.java | 11087 | `be1aded53b22560b2ab9493c754dffc2ed2fcaae083de6ced874774410302443` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/BonsaiWorldState.java | 13488 | `6d46c985c91fd7e3d41e252bbc1ef1424737531e994b6fcce938329dab8c69d8` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/BonsaiWorldView.java | 2623 | `445800efb127c1238f8d434d9f302cd6955807e3a721922c7a1b20041f1a08ff` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/MissingCodeException.java | 1438 | `4a580abf1e23b2c6e101deb36dd8180d456341c397f533ff5e456735662aaee8` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/PathBasedWorldState.java | 17771 | `80f727e3970215fda52c2925f3c40779f65ff6d028d0fb9f8d7671c6baa2ea82` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/WorldStateConfig.java | 4277 | `59610cf945907fd0f14ebd39b116e17a32664725b0b87e3d51b9d943d1a9c5a5` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/accumulator/BonsaiValue.java | 4455 | `bed7eb9b508e6ef361738795486644c4371b8c68794be78cdc64b1937ea8428b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/accumulator/BonsaiWorldStateUpdateAccumulator.java | 6937 | `20f020bb65c15badd3e9a7ed746821b0386363ef80c941759d5bee6e6bc2230b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/accumulator/CommittedTransactionChanges.java | 1110 | `e2cdc8e43872ec7a0e068e8ab28256a471e323b62c168a65767e8c98822d65ca` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/accumulator/CommittedTransactionListener.java | 1109 | `ca65abf1a43de6b7481b509f4b98108c8519529555f8831988a840d204da2c76` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/accumulator/PathBasedWorldStateUpdateAccumulator.java | 44038 | `9a96d24468e2f48356a831a164849a9133d2bcd71fa7a3406dea8b0d6ec37d6d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/accumulator/preload/AccountConsumingMap.java | 3260 | `34831cc4c664d3b2db8ba62ac63320d3e4970b7b1799e1db6ec9686b7a75183d` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/accumulator/preload/BonsaiCachedMerkleTrieLoader.java | 9091 | `d87b819c979572c56225b2e78499a6fe3283028610769ace90fdf6271e850626` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/accumulator/preload/BonsaiCachedMerkleTrieLoaderModule.java | 1175 | `bce138686c58812505ef3d8779cac3bd07ef7012db244e862b61b8b654304eff` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/accumulator/preload/Consumer.java | 862 | `0dab67f4d219e34a5ac90e7b42fc661a73d40da263fd623833d32128bc41a8d4` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/accumulator/preload/NoOpBonsaiCachedMerkleTrieLoader.java | 2485 | `854634c6a5f0ad59d7dddec62472b59649b65d25de2685e5d7a46c2b98205bb7` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/accumulator/preload/StorageConsumingMap.java | 3053 | `e0feb22d0db8ae8bfc604f8ffdd05674c0af9c8c7bc84f270f1531faf3551981` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/bal/BonsaiBalWorldStateUpdateAccumulator.java | 4234 | `aab510b91ffbcb29525c58fc10eff6e4e97983eee16b305b41489da4133966c6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/cache/BonsaiCachedWorldStateView.java | 2935 | `1ded9189e8ab54f0a652ce86a6d730021d3a707c79901755446ff7fe659b5457` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/cache/BonsaiWorldStateCacheManager.java | 3209 | `193345c269e71c4143e5f5a06323b44c5ef9d9b350efb0150363f0a599e93329` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/cache/NoOpBonsaiWorldStateCacheManager.java | 2571 | `b38f15507b7be601529d69db03214e7c0a5d727bb13d9667f2d41b736a935de6` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/cache/PathBasedWorldStateCacheManager.java | 13543 | `532513821b9096f247c0322eec8d20f1bf9e10f831e571733a61d392f9135ce9` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/frontier/CachingFrontierStorageRootTracker.java | 7153 | `c7d06eda80212ae1a0f421128cb31c10b6337ee5b1702c55665a5d3d268b6946` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/frontier/FrontierRootHashTracker.java | 7577 | `c05cf85865e78c718aabaab1148c247b48ac95a75f5cceeb283533839eb7607b` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/trie/pathbased/bonsai/worldview/frontier/FrontierStorageRootTracker.java | 3569 | `74ee1e7b9b9aa908c42013a68a2919f6e669f24e1b84febd79afb6398732a972` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/util/BlockchainUtil.java | 2734 | `d69295c5654c61753411d507a471a198639d05fdb4b7c2255b29589e169fcb1e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/util/ByteArrayUtil.java | 1722 | `c036d76b065c23ea0ded9f991b5c19268abd9253ebab5879e0e8f580d3767446` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/util/NonceProvider.java | 811 | `4ac5fb9516001e7a4abf635d393e860090b49bb12585d0fb6608b04e437ecea8` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/util/RawBlockIterator.java | 3708 | `103572e612b740328ae6e757bc00a9911819fed1363c456d0ebbd042ff0f715a` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/vm/AbstractDebugOperationTracer.java | 6179 | `78365f81a3d8f2e002db7b73112761b649a719d24cd345db6ac0fa7eed3e3fbd` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/vm/BlockchainBasedBlockHashLookup.java | 3830 | `e8689e50a1a16c59ab3c70a26d9b2340bd27e4ed306926081d7f7c602100492f` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/vm/DebugOperationTracer.java | 13873 | `48945ba663d9acfcabf1bb2c7ddd4c24222208e4e3b767408140b774c3e609fd` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/vm/StreamingDebugOperationTracer.java | 4329 | `5c856ab7d1ba537aa7b8b9ad9fb95f0eccf88ab6f5b7379b6aa1dff8fc090cb2` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/worldstate/DataStorageConfiguration.java | 2716 | `d7fbf9d892225140e88806db2bc7ad32966eacc5722498f76fe2c2e512a32836` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/worldstate/ExtraStorageConfiguration.java | 4306 | `ddb99158ab1471982278b452082f6ff799e500afd5677f93ae01da89cfde9bd9` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/worldstate/FlatDbMode.java | 2309 | `1339660aa4a0063a31cc715d5a1a668604ddefb992083a0d9044bb880d03e942` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/worldstate/PeerTrieNodeFinder.java | 1072 | `f4c0f8396d116ec8fd53b7ef992382adce85d9dd7c5db6ee1617c2577e8f5cef` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/worldstate/WorldStateArchive.java | 4471 | `6e955ca89718647c2669c7466e866718094ec4eda950c0bfe47ef3d32d1a85be` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/worldstate/WorldStateQueryParams.java | 8139 | `4d5e38f482792a569cb64c04b018fce49584ef41e288785ac7902842a01a91b3` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/worldstate/WorldStateStorageCoordinator.java | 7904 | `3fd9b06a3e6e3a3f1f1a5d53c0f390ae60899378f1cffe3062528b1b2415114e` | 0 |
| ethereum/core/src/main/java/org/hyperledger/besu/ethereum/worldstate/pluginadapter/WorldStateServiceImpl.java | 2937 | `dbcb1e29e77922d9ea7dcbcb53e83bd804d59f51f3a45315d4dd203c96aa2462` | 0 |
| ethereum/eth/build.gradle | 3996 | `738ee6b2800da72a634518bf5afca3e56ea0afd56999f61f8ad117567a422c60` | 0 |
| ethereum/eth/plugin-api-sync/build.gradle | 1794 | `7e3e0008db62c7622cbf3f699fc16a0c8fa617a74185d06191202596fd7d6451` | 0 |
| ethereum/eth/plugin-api-sync/src/main/java/org/hyperledger/besu/plugin/data/SyncStatus.java | 1847 | `f8d311fdb8e8e4f51b6bc250cf135fecf40fb32d4d4204adf7c5f709924c385b` | 0 |
| ethereum/eth/plugin-api-sync/src/main/java/org/hyperledger/besu/plugin/services/sync/SynchronizationService.java | 3715 | `bf60a138fb433d24e508d0c63d167ba001decbef92ed5e79851753f295909a20` | 0 |
| ethereum/eth/plugin-api-sync/src/main/java/org/hyperledger/besu/plugin/services/sync/spi/InitialSyncCompletionListener.java | 940 | `86a2bafda25960d5b032a07909ded981797782c0bcedaa42243f5c755d7b9bb5` | 0 |
| ethereum/eth/plugin-api-sync/src/main/java/org/hyperledger/besu/plugin/services/sync/spi/SyncStatusListener.java | 1068 | `d474724e2728a56c9785ffbb37f060ea5dbece02a5d2f3a165c88f58e49b67b8` | 0 |
| ethereum/eth/plugin-api-txpool/build.gradle | 1853 | `83ca5ff2583440a9661dfb0c113c3e4c0c90faf7918cc145ac37fa2a9f0c39ac` | 0 |
| ethereum/eth/plugin-api-txpool/src/main/java/org/hyperledger/besu/plugin/services/TransactionPoolValidatorService.java | 1771 | `5865f88f369ac345deb03fa9d8f2b923be331077a8857e51266f3ab32a48dbf7` | 0 |
| ethereum/eth/plugin-api-txpool/src/main/java/org/hyperledger/besu/plugin/services/transactionpool/TransactionPoolService.java | 4085 | `a35a2510dfb6931fa0c23258e90da86097ae3294357d9a93039441fecfc0be45` | 0 |
| ethereum/eth/plugin-api-txpool/src/main/java/org/hyperledger/besu/plugin/services/transactionpool/spi/TransactionAddedListener.java | 1040 | `2929cf55a5418ef0f4e010fd73ad9bad111f60da113cd97bed5b8c9f462b2751` | 0 |
| ethereum/eth/plugin-api-txpool/src/main/java/org/hyperledger/besu/plugin/services/transactionpool/spi/TransactionDroppedListener.java | 1115 | `d17b022b070edf0749f5cfbd37115e48da526f339748a56dcb38cdd147b5de35` | 0 |
| ethereum/eth/plugin-api-txpool/src/main/java/org/hyperledger/besu/plugin/services/txvalidator/PluginTransactionPoolValidator.java | 1683 | `aafcf032fb2cbdf8e77906501c63773df937f8e7684ceae541ac4cd70d66930b` | 0 |
| ethereum/eth/plugin-api-txpool/src/main/java/org/hyperledger/besu/plugin/services/txvalidator/PluginTransactionPoolValidatorFactory.java | 1364 | `a61eb689992c653dd7b82b4a6ae099f9c8027304dfb0a2cdf49ae99e31dbfe42` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/consensus/merge/ForkchoiceEvent.java | 2419 | `69e05c31a79b9620be395c42087458e41815bdd6973dd428ad284cfedf682373` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/consensus/merge/MergeStateHandler.java | 1172 | `e76ea8236deb55fdd33baf8457eadad2028098729f7168682808300c87758917` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/consensus/merge/NewPayloadListener.java | 1245 | `7652431029ba10520480c6679aebaa489d150450d49c072cab87ec44c1c5142a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/consensus/merge/UnverifiedForkchoiceListener.java | 941 | `0a8a8806aba252800ae9e6d02b246549e2297dc64087abb953aeeed9f78869c3` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/EthProtocol.java | 5675 | `23cff9a2b8381b95d0ff7be0e4fe819c45769e3446dbe8f349f04d5ce87b1937` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/EthProtocolConfiguration.java | 3196 | `9f4e0d141d05cd01d40c231a1f02005cb9112577c8fde93f51b0e7f29663e732` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/EthProtocolVersion.java | 6887 | `15164a5ba815c0e9b1c52b5e18132c9e973a422d16bf7ecc395f135b0337b777` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/SnapProtocol.java | 3671 | `2865c4a3d738461dc64d0f4dd57aac7a2012f32c55c50b242535eafe3428481e` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/SnapProtocolVersion.java | 3619 | `51ed32c6d1f57d4d5b5ba9c2555a7cabb231ab23019964616d10305b3f186226` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/encoding/TransactionAnnouncementDecoder.java | 4916 | `86dfefb29cde726298a2f82839dffdc5c832c50776d1513564911dcd7b0d07a3` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/encoding/TransactionAnnouncementEncoder.java | 9136 | `de4a7632770073e1292235711ab172ec88e068d5773d7411fced32596f997769` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/BreachOfProtocolLogger.java | 2060 | `fde64ab28a145e99ce57d6bb9fcaf85d2459d716c4881b1e6ac8eec2584c91c1` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/ChainHeadEstimate.java | 1773 | `446ac925fa3feee526097cf189c5d5bf2e78b670c2bff5bab461a8b691350f59` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/ChainState.java | 6197 | `852e646bc6ce5594bbf44391252abe740685c5a3a56ddc1bf75dce8d1a2a0e7d` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/ChainStateSnapshot.java | 1219 | `02a08345d4a3f3d459bd7e1fcc2bbd6fd4367d7aae980531699e218bf2c20272` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/EthContext.java | 2163 | `d48e99c74eef1a069fb357eecdfce149048455c0b62993a1b87246e4ae986bb8` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/EthMessage.java | 1052 | `fc02dbf7cec467b012891e86548700832b01454e83dbd9dc0a090325a2838c9b` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/EthMessages.java | 3232 | `efef386e042ac01e5784ffa21ef655af4a4091869fcd29351102acca7b55c89e` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/EthPeer.java | 27407 | `05bfc4a7639974bec307572af5a074ecd5347083de3ab7d0fc8a5085dd94aca5` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/EthPeerImmutableAttributes.java | 1748 | `9ddc6490d48ec2fe69baccbb6b07354c426f019ac9cdcf2efc9cdd31433ed2ba` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/EthPeers.java | 39847 | `6f7944ffa26e1b8454763f78c94985a2ac5252b5fccf19b275cb3afc38ad32a5` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/EthProtocolLogger.java | 1072 | `318cf29d44df848f5a9232137478994caeea0abbb08565f455a1c45f4bf940d1` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/EthProtocolManager.java | 20173 | `82e830619dc24fba34d4a7a4e02586c07c553c77cfbbf91f262e7a17c671edc4` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/EthScheduler.java | 15412 | `be1541dd18eb66a00879f4113b17a2809b7ce1f7fdfd17663cb1caa6518b0755` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/EthServer.java | 19080 | `8c1a60f006d67bfab415f334950c8a320e3953f026d1c24f612e95da3d3aa442` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/MergePeerFilter.java | 3958 | `bb7894aa95a6005f8632b28a1b87d2be597ce633988dc8bff6229adc69d19bf4` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/MonitoredExecutors.java | 6290 | `820c3911eaf7e7a509b0ce13c3b05c3e31239fc10df2f32e175005276f1a8847` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/PeerReputation.java | 5089 | `53255649fb505eda8c8baa90d6556660341c5a5c631ab4685a99698b9c86680d` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/PeerRequest.java | 1048 | `4e131a223fe4b8b6e059571171cdbe6130d3a59192a5f8cae33ddad45ba9f576` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/PendingPeerRequest.java | 4614 | `10d0372d63c987c2697691471713edb38e10c5cdc0fbfab6de1405eecb718fbc` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/RequestManager.java | 8096 | `906bfd3af270a7499716bb78fd599f5602034e5179972d062a422589b5829594` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/bounded/BoundedQueue.java | 1657 | `a204729ca03a674de1f462d73ea8ab3ae26b79793bbc00d743385d96ebae79ed` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/exceptions/EthTaskException.java | 1281 | `79d007fb9e733ecb541f42c240d4b3e4b45edfa25e72fbaff0534487721f839a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/exceptions/IncompleteResultsException.java | 962 | `c0c4246bc203bb151e4c4c5e24fc9adb812ca806d8aa966e57a28f7a62315682` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/exceptions/MaxRetriesReachedException.java | 844 | `be25319f21ac377213351485dc4e49cd6ae50add5192f547d7e14026170bdb6d` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/exceptions/NoAvailablePeersException.java | 1399 | `2aedfd86b1d88f1e3b4c52e3c67f7ba874880f98ee3c2223a30fd85a62fcc99c` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/exceptions/PeerBreachedProtocolException.java | 853 | `c4f6d5f61de493340da2a7733f402c6ae85987020ea660dbface61d4460dba8f` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/exceptions/PeerDisconnectedException.java | 1072 | `0c33fe2cbad40e4bc93eece7b58219b4485f70715e6ea0d795f08c5551bd362a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/exceptions/ProtocolViolationException.java | 1288 | `6b91e5ed41c20bbf8a55a7c9190380e733587d8e03f304a6e04a5552bad9204c` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/InvalidPeerTaskResponseException.java | 1015 | `27d073f0af97293f4ed176ee92ea097544c42069c8c32b7a7f1d8364b45ebbbf` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/MalformedRlpFromPeerException.java | 1189 | `9e4b47d05133081f30f71dc2f4c99ffefb8eb585dd186365b7731ce7d8c5e851` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/NoAvailablePeerException.java | 761 | `b73b5165db3a7dfc2280b86b23b11500ba9c7b7ccd4bb3ab805408151fec9a4c` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/PeerSelector.java | 2008 | `a00b4f8c36819b0ee71f9590d70e1c8be05351e94aad98f587024668b9a1a4f9` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/PeerTask.java | 3601 | `d6f2305447f76f64cea7d4ec66cb4921c338fb0eb96f0ebf82ba2a426dd84eea` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/PeerTaskExecutor.java | 11307 | `b3ac080e37fa889355887860dac286dd002c9c0b8963f7f973d7ae51558912d9` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/PeerTaskExecutorResponseCode.java | 855 | `39086e41f6ddf655c24a81171b2aafd8fdc0d683b3c28efbf3f6a6bb7fd6e21c` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/PeerTaskExecutorResult.java | 947 | `83ba994fb69ec9717690959589608e5c66617a7c64e9412ebfcd833d9f2af996` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/PeerTaskRequestSender.java | 2443 | `9a004cfd9c69a2b2e3b45d4672148caa027dda370ee97586c72e1e45d67f4463` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/PeerTaskValidationResponse.java | 1808 | `d6e467126c392133ff35f339743c4e7cb6a0a32bab706a8b53b6cc5e9c5d797c` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/task/AbstractGetBodiesFromPeerTask.java | 3560 | `f06b1cd81e8cc4198f8e3b9c85cd7b578a3affc103ef6a59ba1a60904d803125` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/task/GetBlockAccessListsFromPeerTask.java | 7067 | `9d89e30383f9d9b900e6fcb2d93cfbf9d93975434b1e460dc80d775243192537` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/task/GetBodiesFromPeerTask.java | 3837 | `294979fdecc003b8d0069d0376d84301eef042f18312c173ee64f668525aaf11` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/task/GetHeadersFromPeerTask.java | 10049 | `f37740dfb497fe62b41f998e1285bedf5576c48652907e799889a204f2ece4ac` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/task/GetPooledTransactionsFromPeerTask.java | 6857 | `a7f4e7df3efc0b42fd09e396f9954037f130d7693864c425f5c918caedcb8f54` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/task/GetSyncBlockBodiesFromPeerTask.java | 4200 | `3df43f3705bbf7f1c551f9ce6a26ee0078c24ea212cd3006c0a91fe725aae513` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/peertask/task/GetSyncReceiptsFromPeerTask.java | 13611 | `1ebe85dfb0cc78047a70aac651a84a31b4aef447a74a3e9af9281074ece93ef3` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/snap/GetAccountRangeFromPeerTask.java | 4842 | `2860c1c07fe844fdaf060572fdee99147209ed98da5df6a14bcc64b9ca7984b0` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/snap/GetBytecodeFromPeerTask.java | 5269 | `03e14b6181f260c4a7659da7eabde91456dc660b3ae59e6c373ea0755be705e6` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/snap/GetStorageRangeFromPeerTask.java | 4914 | `d26b879bf9179b9dd80753def433f7c73f9c8bd005f0d1455449c80fe346bd89` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/snap/GetTrieNodeFromPeerTask.java | 5449 | `ff029bfcba4cbb5b567af737a7ce768817491c4dc1f5868f35464d325bf77ca5` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/snap/RetryingGetAccountRangeFromPeerTask.java | 3303 | `f3743067b4e059edd6dcc54f6bbc29e737bf244e7f99464dbcf7056d39e4b08e` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/snap/RetryingGetBytecodeFromPeerTask.java | 2967 | `aac42ea6a03af970c95c3db8c2c730839440980d7d76e4938662014e4cf0d927` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/snap/RetryingGetStorageRangeFromPeerTask.java | 3441 | `686a60ecc730abce52d7603937c0f090e107a147c05caf1c499c8b38ebd921cf` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/snap/RetryingGetTrieNodeFromPeerTask.java | 2918 | `b57b06e96a61af2043977d928c4c61390dbf662e90206ffbad5e4a51440f6c4a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/snap/SnapProtocolManager.java | 13965 | `03b3b3fdb2e678ee953bc180d4213e48ca007ef4eb54fec23d5abbe699cb64d8` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/snap/SnapServer.java | 36607 | `fd6a5516d13ac2f5f952e4cea25382fa5bef37504cc1b653920ab298db703deb` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/AbstractEthTask.java | 6477 | `e3b197cebc85ad33cbaab534447b927fc1fb6662ed5d1612536367c731327a13` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/AbstractGetBodiesFromPeerTask.java | 4479 | `df2eabf62eb10fb374874fb31b44b7e125ea77178ce80f35f9710e44c33df0e8` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/AbstractGetHeadersFromPeerTask.java | 6192 | `d63356fef2786ce0f3fedf1d308676c5d00476c6ae1990f600cbbc225fdea150` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/AbstractPeerRequestTask.java | 6256 | `a0c66ff898b633bb9655aeae52d870f649986aa27f41871901f2cedc2d7f6e0a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/AbstractPeerTask.java | 1789 | `48b6bbb09c4e064126191d9f9453aa80a14a3addfa40b72af499d67493725fdd` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/AbstractRetryingPeerTask.java | 6437 | `9b61f0470b4e90e306d8d1bd15b475a60e692e8b987845184c3a3df1cf59f174` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/AbstractRetryingSwitchingPeerTask.java | 5762 | `4f7cd0a3eda2cee4ce8b89870d64669d95c9ddada57753db713438566b83d4db` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/BodyIdentifier.java | 3767 | `071b693cb83ffc04edcf072bb9b98bd74a5e16bbb93e4820f026fd7222c2031a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/BufferedGetPooledTransactionsFromPeerFetcher.java | 8401 | `25f24b3d026530eb9f3aa45a73ba421d88429cf6fccd9f0200c65b20f1123569` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/EthTask.java | 912 | `f0aa7e373c8caf679d610aaebb003abec5ab0cf8edb77cb8f4f568d69716a5fa` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/GetBodiesFromPeerTask.java | 2451 | `ee007cfb0521ac5340773002063881b1d4cf1d4b4cbc01b09ae5ea4d8ca2f21f` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/GetHeadersFromPeerByHashTask.java | 3235 | `b4dc4be43eaf92e431f75102fdcc8d98f284ecda56723cbaf1aa10fd254546c0` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/GetSyncBlocksFromPeerTask.java | 2617 | `eaa0da6675ae32dbbbed082d6599f13b851af72047aa976634447c5d6ccf6542` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/manager/task/RetryingGetBlocksFromPeersTask.java | 4253 | `4276e07b5ccc699cec6f4ea42434a925c0e18182cefa47ae6a64265f79e3cf55` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/BlockAccessListsMessage.java | 3160 | `3c67794a1e598742dc7ba6395dd773b83ee7fb4d8aa78552ece53297faa42e39` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/BlockAccessListsMessageData.java | 6711 | `e39b2ceb389004c8e07e0c4596a0c9dd72dfed59d7f5fb898579210ee4ec999b` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/BlockBodiesMessage.java | 3176 | `3e518ec9ab2964009bd58a5ddf17fed40d529f3b8d83f284a4dfe0e77acd5915` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/BlockHeadersMessage.java | 3105 | `c8da815a5a5a89780375009a76df0a7f5d8b83506d15adee6f758efe8f7a47d3` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/BlockRangeUpdateMessage.java | 3728 | `fd291381146d1602ed746ecd0405cd701902b7dde1f13a1b1714ffc931d42c2a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/CellsMessage.java | 8016 | `a208a12c00390ed464428f80dd1a04798227a849338f43f38e7865c8c4b783b2` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/EthProtocolMessages.java | 1781 | `042e14206166302a3126de89e1edbb94abb4d68766ff1e8b3eaffa286ccace30` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/GetBlockAccessListsMessage.java | 1968 | `29b2531ba69db9f295d8039df32ed07dd69058948a703bee2c55a716269778d4` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/GetBlockAccessListsMessageData.java | 4702 | `a127fa0892974a0f72889b497b723dad8f5f62cfdb0e035a4a7242a477a87612` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/GetBlockBodiesMessage.java | 2071 | `c85014f7f89d9cacdd197522b4971e87f54928b8ca0bcdf1923e8a72f9ba8303` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/GetBlockHeadersMessage.java | 6727 | `1d778125eb3028b2237019563e48ceda8b88071e6b52baf7965d4c04d8df290a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/GetCellsMessage.java | 5927 | `856b80ad4e19a72579145640288d3cb60df07bd3582f664010301669712a1351` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/GetPaginatedReceiptsMessage.java | 3446 | `98a180d632332b76ac03d17297baf987ac103bb95175fd55c9371adf466b7e4e` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/GetPooledTransactionsMessage.java | 2232 | `37704f432d1cc49ad8ab43f123bbbcbb020f145a6c42a5b646f9ebbd324e58b5` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/GetReceiptsMessage.java | 2932 | `1b7b6f68edef6227ae0a794946af169bec2c5413db59b38ec9b7532f23f1c77a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/LazyHashListDecoder.java | 1827 | `ec9e2fcbdf6404c2fa7f9ec636c5f0d103b66030ec91c7618542d7a5c0e7acdb` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/NewBlockHashesMessage.java | 2976 | `2d6327dc73bc3f8f7b7aaa38b8ddee0384d15f4dcdff4cca5c7c0f6b22b757d5` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/NewBlockMessage.java | 4487 | `b5d84c2f1d0c7e92b2d351339543ab3ab591a166e6a553ad11d7d25bfa3862e9` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/NewPooledTransactionHashesMessage.java | 3402 | `0a1911d406557a1795836550e16ebf34cf08abb70c87280488f203b3eee5ea44` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/PaginatedReceiptsMessage.java | 2213 | `bbb48b9e9dd5ab45df6a7c71caa5f7831af7e414beb7184dc75c083f67d00655` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/PooledTransactionsMessage.java | 3617 | `7bfddc15df4a0286348dca2607f6dacea3b089749b3d9323dad07148c264beb3` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/ReceiptsMessage.java | 3503 | `54efa6e85d9804f1c31fe07ed9d0ac684e0582057f1201fd7c4988ba4a8e94f1` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/StatusMessage.java | 11981 | `01503398f147b07799feae3dcb36c4c015854f6f4244e1da6d6b020437fa1623` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/TransactionsMessage.java | 3953 | `2e27411f6187645eaa89f2c67e0f8cc62e62adb955b10b45733dad574dbc21a7` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/snap/AccountRangeMessage.java | 5325 | `74a681f8098686baa022c9f5eea68ba21dc4b57d51af673d66e01270c9140e0a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/snap/BlockAccessListsMessage.java | 2789 | `f769c55c32a31abff3b6b3ddc6cf8b202b1c1a14dfe2ade2695f6f7f2b5189e6` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/snap/ByteCodesMessage.java | 2654 | `35772fdd22b4dd36086aa03b9d73287b89e070cabd81f290b73a6fe42b3efb0b` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/snap/GetAccountRangeMessage.java | 3614 | `7907d0094cf6d15acd59a0d831c05cae1fc5fcedeeb55edd2f5a34b096c03b55` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/snap/GetBlockAccessListsMessage.java | 2328 | `a80f313a0fecdba92e2db1e095da3323cc437260b7e776e531b92a8f9923f4dd` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/snap/GetByteCodesMessage.java | 4404 | `cf5f166b92318cbda3ce73b7145d50edb71c3b3723e5e184133b6041a16400c9` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/snap/GetStorageRangeMessage.java | 5445 | `a2591c120282f5653b8c5e944ce98343f856971271175b438dd28141d42cdf5b` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/snap/GetTrieNodesMessage.java | 7052 | `616ab3ec99ecc735aefb2c4e8e3bc418a1556216477287d3dcbcd4acc7baa714` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/snap/SnapV1.java | 1417 | `02ff3b431be3f01bc4d8bdcc0171b2627149b85e8ab79efc13626037bccae872` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/snap/SnapV2.java | 1394 | `14b2f517fbc8b8f3028ac87f7ce7faba037154f8dfcdbd4cda18a177e06a65a7` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/snap/StorageRangeMessage.java | 3880 | `f13ad94d0fd641c3ca9576801be6bf64847fed917f581b1cd2ce6383027f26cd` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/messages/snap/TrieNodesMessage.java | 2499 | `9be723e4d50b4bcd351b23b9571f0f495aaf40e0b68344ad170cd9cdd02614c9` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/peervalidation/AbstractPeerBlockValidator.java | 5110 | `d50563c4539142849568d3c3fdbb748fc0ac5e4df9263c79b67548daf1f876c8` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/peervalidation/PeerValidator.java | 2213 | `3c5dba7f614f52e6fedbb09ce4c9c9c89e516e9bf8ea00d665b315868d4169e4` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/peervalidation/PeerValidatorRunner.java | 2559 | `bcee3b2b257253d09948e8b8d6689deb7bc472326c1c9c5e06ff4bf36835f34f` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/peervalidation/RequiredBlocksPeerValidator.java | 2309 | `df45dc2dc68cb0f31bea90ee9b77cce72870b682cf1e57c259a0d714aa2e585a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/AbstractSyncTargetManager.java | 5844 | `cf17d2ce86094afea91ab3c0227dae34ed404192ba8e02a5aaf91c6d44f4c02a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/BlockBroadcaster.java | 3380 | `5b8ca9ea8787d86b3ab378593876336c08125ea6086fe98d08f45f69f0a3ea26` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/BlockPropagationManager.java | 42971 | `db2005dca27a2c175a547a25984fcfe4929ebef3aab10761110066e1bb10b831` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/BlockRangeBroadcaster.java | 7740 | `ac85931721c0e98b556ab8ccca1bd9c69077fe99814f2ca521a69d6f8253e917` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/ChainDownloader.java | 809 | `7b6eb2e73058436e13e2df8c4f0aadf573ad6169a88a552b5b79de02c27eaee0` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/ChainHeadTracker.java | 4612 | `b4ae2aac43d0d2e3a2c6db2411ee62dbfbc6619a0f4a64016d9bb6a508d75fa7` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/DefaultSynchronizer.java | 16197 | `d037ce7ae26acc0eafbb65fe31ab2df4b0bd62a1688a759f99e210fe89e3c5e6` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/DownloadBodiesStep.java | 2062 | `0a84974903200aaa0fc3f51ea039775f17345abc67c9a4ed5df590a5cc4c244a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/DownloadHeadersStep.java | 5768 | `bbceea2b7859be7b43cda867e2f3b399c483d012d94c5529b09bfe2d13b4f658` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/DownloadPipelineFactory.java | 1498 | `38e25d80ed2b9c423dbc88059815ec6540515338a02f5d4285497f9706a247e9` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/DownloadSyncBodiesStep.java | 11764 | `c41a82aab41e67209c4aebaae60585abbab843b22d6404bc29dc9331db05f39a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/MissingCodeFetcher.java | 5021 | `17f4a7acc1d52864223170e12137dc379af452bcbb327b50bd6c28d501eaa265` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/PipelineChainDownloader.java | 7600 | `c37859482df2f0eb3adcfc213e6b032738d910e58635102ea0edcbaf4fcb431c` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/PivotBlockSelector.java | 1119 | `00dc0c846f1b50c5878aa937656e2924e6505dadcac56410ff7997360961b2ce` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/SnapServerChecker.java | 3672 | `4d62a4b66e66d88ce3e7cefd3f886955f0269233828acc4edf1bb57f30c1b49d` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/StorageExceptionManager.java | 2321 | `24ea6e4a75967b5f7bd76455a6a5005ec8d52a8dad8ebdb1e5122d5876f6b27e` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/SyncMode.java | 1236 | `2aec70f0a3702d4a85473d54f638109a02c3b0debd52bd7c2809ac215460b053` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/SynchronizerConfiguration.java | 22199 | `be6f496a455e9cc880344a8887d62e19538339ddcd666833e3d296d3a9651bdc` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/TrailingPeerLimiter.java | 3915 | `08942c0e31295559bac3bde0afaa29b44fb1d20b200efcd1a1631c0e19de8a7d` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/TrailingPeerRequirements.java | 2810 | `d91d2c3a7af91d5e9d9178b4a8734443fbaf18af84b5041449889b4aaed1459d` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/ValidationPolicy.java | 854 | `f25bd780508ce728507936f18b3ea82ee1b5a863b0c71d4d089290e94a6509a2` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/BackwardChain.java | 12713 | `9484f82fecc0ecdfe30cf4ea916d6786202b736e0864b3b43f7d7ab260e1bd47` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/BackwardSyncAlgorithm.java | 8958 | `cb50b780289b0e9dc659ec9a713a993d5f05300919393bbc22cb84c4e262721b` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/BackwardSyncAlgorithmFactory.java | 1228 | `460f9090c88d00c64f5cb4b9c9e3ade00ffc4df56b47e083a1a5f80a1dc0cd50` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/BackwardSyncBalImporter.java | 10322 | `abb46fb99d6b976ba87ba8fc1306f00a433f40b56986d62d24cad0852ead6472` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/BackwardSyncContext.java | 22843 | `b9917b913e6bab41a53f98a96f63f9b26bff812f951df94c068e6f71a27ffca3` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/BackwardSyncException.java | 1325 | `c38e56927cf4cab20e17030506426ffe35ca7d9b3ec720aeb36f6b7d0c533123` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/BackwardSyncStep.java | 6456 | `6d847df4abf31aa341fca325a519750b44e512a8c7941f82a7a96ddc94ef3002` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/BadChainListener.java | 1457 | `c5a98aef9bf1f4eefc323bdcbbd11a30813bbd042c6befe93c71ff59d2c34ec8` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/BlocksConvertor.java | 1646 | `e5e1e4c832b89ad392b01e8a4a8c8ad2e1a08b2f862ef24204198d933305075a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/BlocksHeadersConvertor.java | 1769 | `d711af631d3b2fbff021d789088d8bc4b5eb610e7493e4540f6b784a81f6d0a3` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/FinalBlockConfirmation.java | 2228 | `31a718d310344a762354065447c643c64d438c64e6feb10dbe337430737b569e` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/ForwardSyncStep.java | 5349 | `184f603953bfafe2f17801cfcf462747cd76b4b3bf3bbec3244f073789db256a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/GenericKeyValueStorageFacade.java | 3594 | `561b6bac59284ebc0d32098e1cdb9f15e6d96724a4a22c4bfac0aa429b354a98` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/HashConvertor.java | 1063 | `57b2599a34bfa338cf9273ef44b7c7fe8ccdfeff30aecfcc18a5fc820cfac756` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/KeyConvertor.java | 771 | `8d57128b8bee23a21a56556b4f8a0c7c6768354d6c610e36226d9cdf9aa41c4e` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/ProcessKnownAncestorsStep.java | 3947 | `7acb527282101c4ac639c056aeb0bcb40e81be5ff9e95e05a709f41e42262854` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/SyncStepStep.java | 4209 | `eb81c7daf5973b7681c639a6678ccb0b422400a2232b5b0b895055ddc06e3035` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/backwardsync/ValueConvertor.java | 811 | `900f28171bd24466dabea532679580e97137a45cce2e0dbb64469db36f340ee0` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/BackwardHeaderDriver.java | 13839 | `07afbe8849556a5fc5f6806f9331faa6098cf9121494f5182ba6b1ca3daa01d9` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/BlockHeaderSource.java | 3094 | `47233aaa381f7c71041ecff0e4641cdf2aac2944c1708efa040b117dd58a7feb` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/ChainSyncState.java | 5980 | `3f237f3c9840a415aafff4f5d29d93d49de8a2a870380d84ddb50c7a8e0a18e6` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/ChainSyncStateStorage.java | 5728 | `5e2b467e2589f7fe62b22fd6cded5868154eb54dff7ab820e05a43b44f7e3287` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/DownloadBackwardHeadersStep.java | 15836 | `e6c0bdd6aece378c16042dda1486669c6b71a99ad60404d5d29f4d69fdf931f1` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/DownloadSyncReceiptsStep.java | 11799 | `ad1aa151ccef54f3a47cbe4cd4ae564c380f5b7de25dc8a0bc2e717923811c88` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/ImportSyncBlocksStep.java | 4000 | `cddcce0d0443668ebc2d96e3bec046e409b93d76403f7b98e52361a241ee2ab6` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/NoSyncRequiredException.java | 762 | `968d5b59e3f86b84ab16aed671b3d17abe98cc32ba0f5cabce7e7c8e1c7594be` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/NoSyncRequiredState.java | 840 | `38a6b8faca0dd961925c2a010165952db6176edf2e7519cdb9721c08c527c5d5` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/PivotAtOrBelowCheckpointException.java | 1303 | `c5d2d1c8801b87186299410450175148b0b945bbc20460ca302d2250f52db10a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/PivotBlockConfirmer.java | 8453 | `669f1014413ac961416cf0f67b1b448c8c4b8b6eafaf8e022318ed70c1299ed4` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/PivotBlockRetriever.java | 6323 | `9013bcf3ed465d470eaedf290f2ecc25e8b350a299f683c299455450b78097d8` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/PivotSelectorFromPeers.java | 5771 | `d931c606a264868996b9f9f140a9142fd93525ee307ffb201bd471f55bf9b4a2` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/PivotSelectorFromSafeBlock.java | 10214 | `f8a6f5cb29a03f5978a43d2c039f378914279d90a6d1e98425ed85b3c2a8088b` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/PivotSyncActions.java | 11402 | `0d53d064b7e4cd5e1c65c12d72f0bfb51c85020aaee27ecc031e986f347cb189` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/PivotUpdateListener.java | 1196 | `843563fbed2861addbde760aa7819620a4c372cdabd37065be256d4ec6ddca24` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/SingleBlockHeaderDownloader.java | 3858 | `9d9ba3891e79d90dd6587e9448eddc122d70078dc3dc9d98eb3c4f3c29a81d8e` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/SyncError.java | 775 | `954e010684129db08896f371d7a5897e2dae4cc11a58cf1a6b4f84334e176cc0` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/SyncException.java | 1051 | `d0c3cc13f7ebc111204fa9b4428dccb31dbebd84709c5026edbc35a2ed3c1429` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/SyncTargetManager.java | 9647 | `9b285fdd5db1274f983bfa382765418951f3491305b32e0da97903cc642e2dba` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/WorldStateHealFinishedListener.java | 1253 | `10484caa98ce324dbc9f1f4d249beb2f3826d7cd59d72fb086b7767bd06fdbed` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/WrongChainException.java | 1233 | `ef5b01059ba0ad0da1af8655dcf533e90d1b575e56b2f474b658456f69cf38f6` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/common/checkpoint/Checkpoint.java | 3670 | `d6206bc378cb93bac5aa68681d072ff69d84a5ff7f523459b3eb2959755b3d19` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/BetterSyncTargetEvaluator.java | 2990 | `6d04921817ce0918473df2430198bb8f797c94d8a737606c839ab35a63ab8eae` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/ExtractTxSignaturesStep.java | 1245 | `fdcc8db9113baa9adbc1629d7937fdc2926316adbea29ce10d42a8221d79b2f7` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/FlexibleBlockHashTerminalCondition.java | 1308 | `a7d31ac6f351fcadc3d082649edb64911b919b5ab25457989474aad9f78f4340` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/FullImportBlockStep.java | 3724 | `1c61475bfa533080ee7ca058291a17100b0d6360a1e017e30494a8176b3cd2ab` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/FullSyncChainDownloader.java | 2491 | `19eead1cb82e36e01cb27f7d60edc7d3edd76bbca6410c8ca72a2942ebc2114a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/FullSyncDownloadPipelineFactory.java | 7100 | `97f09298b1f769fc275c0fa71455fb175d1a8e5c687af560d55c340107ad40be` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/FullSyncDownloader.java | 4741 | `12653b78cfa89938d40ed8e28151b0f282f970bb8d5c670d4718a6c0e3d1cfd6` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/FullSyncTargetManager.java | 4829 | `aea9059e21a2c810c9fc715377108d9c677595924eaeebad8cebb8a71b81b58e` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/SyncTerminationCondition.java | 3046 | `cf0affe7d58c75ed579560010e7938f7c6e3226c44ed61df7b1b7b22f59b186a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/era1prepipeline/Era1FileReader.java | 4784 | `40601e103b8a8b36c73654383f9d02d6983406ec2959465ecf6abce98f1d832c` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/era1prepipeline/Era1FileSource.java | 2744 | `617d8031e217a8a0ab5ca114f646901dee622e6629ab96dffc080011ab81a90b` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/era1prepipeline/Era1HttpFileSource.java | 2970 | `f6feab734ace1e88b9966bbd4d8807b0ca47188146d15be900215825453bd45d` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/era1prepipeline/Era1ImportPrepipelineFactory.java | 4945 | `613a8da3cf3df1458bbaeb8260424691dddb980fa8928f75c2e1b2f63a6f2d82` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/era1prepipeline/FileImportChainDownloader.java | 2127 | `5d080e374e7113d91b179f57b81d89730758f01784f631c18203dcde7f7590fd` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/fullsync/era1prepipeline/FileImportPipelineFactory.java | 1240 | `28429cfd28466daa674ea2da5daf8719d529aeb321420a374cb8c8a3b8740557` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/range/RangeHeaders.java | 2093 | `810dce2c895693228910f8cd3bb20bc385054373004119e246529ec631086f9d` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/range/RangeHeadersFetcher.java | 7554 | `5f1a5e023a2b39bd7218bef8ac2c277599339e37096c4c50cf19ca3690e42bf3` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/range/RangeHeadersValidationStep.java | 2669 | `36a14bc6c9c6b048065bd9e3e7f52eed0ff90396d22502e777e5105b69f9399f` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/range/SyncTargetRange.java | 2481 | `c7da7cb589722e71cab8600dba36bc007055d98413798a9f9aa90913e7a94c50` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/range/SyncTargetRangeSource.java | 7202 | `57f1b406e156807112bc8fdb1eb4e397beb70e10e61df676fde7b92927bff032` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/PivotMoves.java | 12218 | `d265f5b2d11e4f40158c99e7d8f007c6b0be5ae99153b2723c0e82454c4dce3a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/ProgressFormat.java | 4645 | `42a2fb15a3d44bb0d846143d5791d0b235fff6a6b2552d63340d1d4dfe2fbf74` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/RestartException.java | 1351 | `b760fe2aaa1f5a9acfeb129c806dc751f579e3f0ce95972eab0843db44a54587` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/Snap2Configuration.java | 2605 | `b1bf94546100aae2495988d8151be70684b8527068721b29ac4416c2525ac661` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/Snap2Metrics.java | 6354 | `090a5191b84e4034e5daf6ae77acda6821df1fdf6b7c50402b530d7da09fbf52` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/Snap2SyncController.java | 14349 | `ebd02742179bf6e58854223ee8cc83945eabff3943f612ad96a86bfb7bd9ba37` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/Snap2SyncFactory.java | 9139 | `53cf70369b47f0832aba06d0bbf609c70780e5a04c4b011655ce256636a9c0d8` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/SyncAttempt.java | 15034 | `8146a143f6298f65a98b1cb821c056e18e5e7083595ce084269babdaf22b7ba7` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/SyncChain.java | 21596 | `e8a96349086cd8c1b599630991bf306d5d5a022da73b1535545d57fd9bfe3511` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/chain/BackfillRanges.java | 2190 | `beaca4fb1e95abf9efa4543136a832346059c90288846d556f1e39bf02e4be53` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/chain/BackgroundBackfill.java | 10686 | `c9be254dd5088bb6616781ac5c71796174e45d4399fef345e57e3c7637fb0514` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/chain/BalFetcher.java | 14388 | `e872940be394078d7dd9a915c98d3bf1d8b254ffb9813ce73a649be551b84862` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/chain/BlockRanges.java | 3436 | `2b69af8c0bef2ffd121b950c8d9d34d0e3b9eee678d1dadf0244b80b0608ac17` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/chain/BodyBackfill.java | 26701 | `86226657ac7b16bad1dbad4124f847b31aa838ae532d4a27ed4d846e1d61f989` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/chain/ChainHeadSource.java | 1167 | `61a145c01a2d46f70854719582efa686f2d89f1422d9bad8672381d744ab5136` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/chain/ForkchoiceHeadTracker.java | 3418 | `2e0e3a835da10b44b62b6b0c473077c30d8cb971a843f21c674605e4fb605d15` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/chain/HeaderBackfill.java | 14628 | `72117426e460dbab35e781aff5bb70dac496e70dbafefd78351c3eba1e82e453` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/chain/HeaderFetcher.java | 6615 | `59fbd6eb7e360a67e1b7613be4d8af2240c6abe7f3c197f5893184092c63e78a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/chain/WriteRetry.java | 2215 | `d1cedf8aa92fdf0d028b2fa5e3752c8dac26fc87aa2bde83371f8610a4405aa8` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/net/PeerTaskRequest.java | 4890 | `6e00fb2c5a9df72a034489a4dd2d5c0c4581a45ea7d0a90e20d3d0d5eba8b4b4` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/net/RequestFailedException.java | 2196 | `f803dc008b272ef4b22dd1640793bccc7bfe5fac3f9d68ae398657c32c8a9514` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/net/RequestScheduler.java | 38444 | `6639590edff427d5e14e6b47175875f5ba2c8ca8320cf6aa5d52d848e8db0567` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/net/RequestSender.java | 2911 | `377452dd367c5f750b33ca8df71a6175a5b5df4e3c9fb52321fd3a7561288293` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/net/SnapMessages.java | 7845 | `62b72dcd3996d304279e395aa6622fed57a2f96b86f2ddfae15a1af003dad47b` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/net/SyncRequest.java | 4106 | `c57e82618f6f8bee6db0a2eacd07d143c8ed7dde13537564c807abfb5be96572` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/AccountRangeRequest.java | 3294 | `2493f78441c8629b1ffebc56fb427f5f7b91522e54087e3b7d72a8a52c032ed0` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/ByteCodesRequest.java | 2753 | `1b005781dc19667038a7a4b692cc51e62a15cb3f1486fb39b7f30709ca60b88a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/CodeQueue.java | 3488 | `4866ea9e6aa2337a2bd6b39f08fb8e9dd028ecf894d525716ffad5c44be32efe` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/EmptyAnswers.java | 1837 | `b7185057293e75737d68e153178e50c7ffa3aa8eb51b585cdabadc92ac94f5a1` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/KeyRangeSet.java | 4395 | `441a5d25a0cb55e0e258fbeed480892008ac867d20cfacb7ee4034631dff9eeb` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/Pivot.java | 1227 | `899a10f76fc4f1e750bc9b6b10a05856736dc04e39e730ba3bdda0ef9eed40d6` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/RangeTask.java | 1101 | `7251d66bd0d6e42ac73d9e93fdc4ce7cc58d6085a7704e656208727abfc1faee` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/StateCoverage.java | 2169 | `3f5349228bd99cb1ba6299305bc783b16460bd45134b66545aad08c3404873fe` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/StateDiff.java | 3665 | `122ef89c577767123568acf2f83d85e12af066827aa27181d5ea61d2353b559c` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/StateDiffApplier.java | 7017 | `98804d849d97a5ee23c81313ae92d3178ed652e85ee0160195732b7711f0733c` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/StateServers.java | 4212 | `9dcf90c4fb8c13e1378bdea1de920000b8d5e3feed111ebe37a3a03ad975aacc` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/StateSync.java | 32918 | `bbd0fb0cb92219e58b1b3309f9403e4fb5d94673b2b7ee4a06eaf14c25e4b8ae` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/StateWriter.java | 13083 | `bf29839e6d172eaac9dc51161820cd7da53067f18e1af4f232b32f2342af759f` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/StorageRangesRequest.java | 5800 | `aa467d1961ecb9eea7a4da91fac1b85dcc430e3e8bcea568c1863a5703546b54` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/state/StorageTask.java | 4372 | `cb4d22a0a0ddba74119b3984d5bc63d83872b4f786410eb57d355ad9d2a24083` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/storage/AbstractSyncStateStorage.java | 9470 | `f7dae683d754366e5e0fdd1516683359fe7d466ac538e1a90cb9dacb09d86a06` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/storage/Accounts.java | 2239 | `1522c3cbea2dc3bae57cecc6c9324098088ae18da3624d26d7858aff596384b5` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/storage/BonsaiSyncStateStorage.java | 6919 | `3f8831805402733a090c8a08c657c0c38cd1f7c321444905f0ca8009f199b12f` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/storage/ForestSyncStateStorage.java | 5506 | `2c265c2e20b96c83f785dc0b39a933158ce06b405707b475e0ffe998996ee779` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/storage/SyncStateStorage.java | 4349 | `c2c4b940fd254aa70eeda1a05e947ea8f5837036b4b2b3f504b799ed66c29bca` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/trie/RangeProof.java | 11202 | `8eb499f643a38657100863f5923e5be30c1deb2f5957000ee1fbc9fb121269e2` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/trie/StorageTrieUpdater.java | 13730 | `071b22fda33760c26964fc0b512192582c6f9b3efa7b3a294fa7dc8194951dbe` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snap2/trie/WorldStateTrieBuilder.java | 12599 | `38698fc4dfe0de4e57ea8687e2f7e1248f61fdbe3fa0f2c50128a878acb74834` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/CompleteTaskStep.java | 2926 | `14fa25eabb422302786ae36fed2ba948d93e10197b24e62ef048b5fa7f241217` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/DynamicPivotBlockSelector.java | 6133 | `afe720172893e22dd2c850fb6f58f2a1cea7fbc8a4032781e74b6cad150de6a2` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/LoadLocalDataStep.java | 4766 | `b3ec6669219df4c47effbe9de07eed625f52dc75711e3c53a7917dc5ec19bb53` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/PersistDataStep.java | 6182 | `cdb13280750326e66c02fcca20e0436011d2918872d0a36c893bfdfd914bc024` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/RequestDataStep.java | 19668 | `8cc13075e57358a7b817fe2a2cb7be9379eabf126d5c8ec40e338063469f5faf` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/RequestType.java | 1290 | `4068f4016f9f5592fb3dc63285cd470d1de7433515129745b1bea008fbfdf50a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/SnapDownloaderFactory.java | 7826 | `a6450ea4a5d367d2059e21757a198d63f74518a0933da9ba1f8c2bc13ccd8aa5` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/SnapSyncChainDownloadPipelineFactory.java | 9257 | `3c17723d0fc860d174e15b526a8511cf47a5ead0ce35e191dd1034df2c5d90d2` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/SnapSyncChainDownloader.java | 39195 | `ec1846c7e85f6acb89d8d87706861cbbd22440c92aeffd5f7e6c4fe4b9ae781a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/SnapSyncConfiguration.java | 5660 | `ed192ecba79d0a489b137c2a5cdcc071d154bb45b574e9a62e37f297032e0d06` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/SnapSyncController.java | 1204 | `9acbd85d357e2f6145047249a0adf13d76bdf27ca65542618f806b80c2925c17` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/SnapSyncDownloader.java | 16054 | `05346153c3aeef445de5a1324f075c261876f605ac4e2ac13265a87529b2384c` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/SnapSyncMetricsManager.java | 9268 | `00015bf2b3058aa94fbe692f7104c1e0fa55539b4c574313acaa7932fb32ba7c` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/SnapSyncProcessState.java | 4972 | `457385c89ccff6e248642bf6182e887e00b6fa3df1a9e40ff73697deeb3da329` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/SnapWorldDownloadState.java | 25699 | `ee3e4eee02c8831cc868d98a87c38665cdb84fbd81bc8d5fbaed184771df3a81` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/SnapWorldStateDownloadProcess.java | 21782 | `4c4d0297737a217f0363211b8bb0503345dd6a2de7ea77720d30572d5df42ec3` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/SnapWorldStateDownloader.java | 12491 | `a874e20cf4fcba0488a76f8545566a3cf139259c99131aa58462b6730a83715e` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/StackTrie.java | 6576 | `f00f4c34498d28699fffd19f6d7516c6b695033a6698125fc6e2bcaf573c83ce` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/context/SnapSyncStatePersistenceManager.java | 6323 | `529ded86a185cf49177edc38b8cd506d1bc55878ae232c9a951fc18e18fac669` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/request/AccountRangeDataRequest.java | 11815 | `582f5d0beb31be2c51c97032fb37dbac2d29522aa444f5ef28511c0dd6bb8a6b` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/request/BytecodeRequest.java | 3756 | `e9375616205d086a186573e6abcc7fa3e2b87cb2b683ccc5da2c6ef2b3be56eb` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/request/SnapDataRequest.java | 7546 | `9599ae681d03e6f5c25397a0e3d8229fb31dc45cc261a17ca040f37d52d7e9d1` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/request/SnapRequestContext.java | 2715 | `96810abe4296a4b2d21dcc4acd437510526ac7dd87c4c4446b8e07d8e9ad8379` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/request/StorageRangeDataRequest.java | 11430 | `4d35aac55bdb93e864025bbff7f99fb9188490f64d200cb2966dc82259664206` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/request/heal/AccountFlatDatabaseHealingRangeRequest.java | 9527 | `b2bc0b9b6c32e143e6aae82ffa57e4efa808320b661a974421812ec16f37027d` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/request/heal/AccountTrieNodeHealingRequest.java | 8400 | `4f0a7007e55d5faebfbd0db39b08ea7e525ccf38384e20648c4df5d3c8a43c2e` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/request/heal/StorageFlatDatabaseHealingRangeRequest.java | 7897 | `a3ff5611be7f85b961fc3b290cdc070e7fa03ef5f2b5caf9a0f539bfdae7671b` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/request/heal/StorageTrieNodeHealingRequest.java | 4176 | `5caf3efbd5c49302605c7fb70cd684e640a0ece33595c5667473cd1f9431d156` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/snapsync/request/heal/TrieNodeHealingRequest.java | 6777 | `f0ad15081208d3908b8d25ca15c6d52f2c8b25f7c27b10f79c2bd0065c8a8da9` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/state/InSyncTracker.java | 4002 | `6d23a08f174fada0b2d11aa1d11cd6fd6cfd0961ed246e1f2d998c6bc912aa7f` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/state/PendingBlocksManager.java | 5722 | `aca7fa761570d0f1b5ea848162c6800395f03d95edb547a622c5fd6da97ca5a4` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/state/SyncState.java | 17432 | `904546842bcd22be153099aad211bb041b66a823e401ab500f4a76c7d16c18d4` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/state/SyncTarget.java | 2495 | `ceb3d6cd819c99d13b14dbee62c16a77488d0a9540f8f38496758cb0c80c6e95` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/state/cache/PendingBlock.java | 894 | `20cf0be4ae6e0a8f6b2e5e294d5a9e6bec31e6b235c823a5cf3d015c1234b7a6` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/state/cache/PendingBlockCache.java | 2832 | `f9e4132c1c6a7d704d69d9794056b4d99e5ec1caaf73a37a93fc47274c72bd94` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/tasks/AbstractCompleteBlocksTask.java | 3953 | `b4fb14ba2e8cb52a8afd03d51acd5ff3918546338ce5fe475ce8994aeab793a6` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/tasks/CompleteBlocksWithPeerTask.java | 5372 | `08f07a6927d583252248435e061ad20258aacb832d15ad12ac490399bc861804` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/tasks/CompleteSyncBlocksTask.java | 3916 | `92fbd4a839355207b21070c54c1a58a6762dd91b81c9616fda758b31dc864e02` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/tasks/DetermineCommonAncestorTask.java | 8402 | `9412a53829c64ec668bd8f1ae505756d26c489ac308da02e7e4b02abeaad93f8` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/tasks/DownloadHeaderSequenceTask.java | 13262 | `26caa16a9f1aaceffb23123f71387f75e38725a4454e07b855b63db2aa103aea` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/tasks/PersistBlockTask.java | 8760 | `866edf76746890297423375b22126481d0721b260e3301603ad346e487c3a287` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/tasks/exceptions/InvalidBlockException.java | 1412 | `63e2130e1e11ae6798e29edea65d7dd20b53a35813d46a919edcfb1c902ce23d` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/worldstate/StalledDownloadException.java | 844 | `c2311b8ebdee35f8f8808a313ff34782794acc8d49b1adcba8a40e74c5445454` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/worldstate/TaskQueueIterator.java | 1617 | `1f1f45eed85986dee6b0c0d43c5c3eeb4b8dbe7eacaf9e816faa674c00e04f6f` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/worldstate/WorldDownloadState.java | 9083 | `5d683280c598f4c4b37b72a6e5b7c125f2c2d48531e79f49f733a210d94cd723` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/worldstate/WorldStateDownloadProcess.java | 924 | `dff85990a7c0c84631ed9854f81e466a7a3edaf556562caaa5515645c520243d` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/worldstate/WorldStateDownloadStatus.java | 828 | `a2d4e9b2ac1d798cc38ad71c158e03b347d6415657ce94ece88c972167b7c6b3` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/worldstate/WorldStateDownloader.java | 1232 | `313facb7646b9161faac0c913608feac3319668c3947840729ff5b0a1c4c25ce` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/sync/worldstate/WorldStateDownloaderException.java | 841 | `ad6cc370d0d4c0bc11bc31ebc6a813d85250cd11193535708a48d638592379a0` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/BlobCache.java | 4623 | `e382b12719c4d3ca2c5afe0f72302af80dda6966b57a0aa67c7ea5f11b54b53b` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/BlobCacheModule.java | 916 | `5ae22266ff02c55e41e37bbcabd7aa52269cc22806b9ed339430399131a70ca4` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/DelegationLimits.java | 21150 | `bc588e350848177c20b3f7ea677429839d0fb0d7c91539997a3bef676995009d` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/DisabledPendingTransactions.java | 3285 | `7bee935c600b2ee2ca1b85ce859ce8aa6b19d4de91bad3c207a3c37dac46adba` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/NewPooledTransactionHashesMessageHandler.java | 4325 | `c612e270995ba2a0621fa302214cb6f25559f114650041ebe3b1f2b7327a9318` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/NewPooledTransactionHashesMessageProcessor.java | 6884 | `aadeed4ed6c8d72d778ed8c6a356ba049e0e47ce6f051a794b9beb48e2341cee` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/NewPooledTransactionHashesMessageSender.java | 4746 | `79b5e6110cfaf6aac6397457b89c4b18e0171d91b1ebd469f64d0cdad87ee1d2` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/PeerTransactionTracker.java | 22115 | `c2da8dbfd25ee38bf8d39d10b95cd7642616c7389e3d5ba877ed230d3253c8d4` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/PendingDelegations.java | 11296 | `a911305ee98aaf759e02ec50427e4d57d42640174d341b0b4790040f91b38798` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/PendingTransaction.java | 15768 | `a13d4694786a113dbfaa9e3d23d7dcddb85dfb3aa36084649f65bbe4bff650ef` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/PendingTransactionAddedListener.java | 861 | `3b7139fb3a273152c8758c25741f19f5c2e125914fc4019f296847d83f9b20db` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/PendingTransactionDroppedListener.java | 893 | `0d0c70a64abbbc1cf1bc78f42ad1df5aa45c40d380984149347dfaf62e27927f` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/PendingTransactions.java | 4240 | `2e74cd6120f5543101fdfd5022fdd76d3a682e27967dbb230114d9c41545f950` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/RemovalReason.java | 1248 | `04264e0780d37d28846b7c1fcd88db379a4f3f9a84d42ea9b4afea6bcb414b5a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/SenderPendingTransactionsData.java | 1712 | `c643637f520da13c031a81da0500e4a680a4f68824bcf7a3fe8cdb7b8b093219` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionAddedResult.java | 4616 | `d6742604bde455fd88a87274cb3509924482b76ef4b7a5a4f074adee0ae9fa01` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionAnnouncement.java | 3451 | `3f36179a77e4713051f77a5a64908d51896d8c274e010d51aade5fd2bf291aa7` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionBroadcaster.java | 7368 | `4d38aa91245312dd3edc95826223abc868979b0cba0c50f87c04c7078f32a20b` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionEventNotifier.java | 9654 | `6014665f4c671f3035725641fece56db01b44c0af5c6a909e8337d55ea90c953` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionPool.java | 54943 | `369c2295859a13fceb0d03ce5dd25c8ef337c1b93bcb0f4bedb9405885c0af4f` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionPoolConfiguration.java | 9298 | `a12ea994e9a18047912a147e54cf27b18e0180d49c722d282d560238ec334da7` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionPoolEvictionService.java | 1771 | `cdb83a1105e70a8b45453e9cd66b91f2f537e47c50862c33e9c42e3db142b9bf` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionPoolFactory.java | 16638 | `3abca8485d0368e45c686ea9d53d1c37b5bee5f139de55072b7e09423ca97a16` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionPoolMetrics.java | 11670 | `3c925d2723096685d3eae6509c364f9a3890a06161938c371e94f210e9bc82a6` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionPoolReplacementHandler.java | 1996 | `cf5a9fbd4c21239157d620e479bb1ac9cf502e6fa8168479f608b21d7ea4cdb1` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionPoolReplacementRule.java | 1121 | `cf741e578acb1763707cf3472632a42ce8de7c764fc35332f465460e22ef8f3d` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionPoolStructuredLogUtils.java | 24685 | `7194b9caee15e1770deb57694ab4d7e2c554d631cf4eaaf920edffeda287c542` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionReplacementByFeeMarketRule.java | 4996 | `b58d2d09d629493ad23e2769e84f9aac02616a94377423731347c9bf1a3f0675` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionReplacementByGasPriceRule.java | 1781 | `3efef18eab737fd2cf60e04d36f0ec0227bed379ddd4bae0ec27d63a43b71f3a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionsMessageHandler.java | 3849 | `5b3d397beea8879283f8b37fa31c195121378789179c9095a098924a6934d2eb` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionsMessageProcessor.java | 4909 | `6c13fdcb9af293c9ee8107035c72116d61f6ef584bdc2b3a638f5409faa71cc7` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/TransactionsMessageSender.java | 4597 | `3aec32eb0698552234fc9cf06cf22a9ecf4dcb9690a3dd204ac457e6ce32e8cc` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/AbstractPrioritizedTransactions.java | 10583 | `4cc09d79cb93105a6f8b8b3db560d82d6edcfa99817060cf3e5e248c81649e5a` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/AbstractSequentialTransactionsLayer.java | 6878 | `8599fb719a2aa98a7af213a08163456d52bdf1ef927d7f23c657d119ea418019` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/AbstractTransactionsLayer.java | 27112 | `08230654f7f7fe360461b4e2f68784b3e6105937af307265a4a9b8d1b779befe` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/AddReason.java | 2127 | `637d40d3dbc5eecaed5ee8577edb261176c80be9ea8b4ecb776ed22ed8255446` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/BaseFeePrioritizedTransactions.java | 9673 | `87956f99823093363a6fe4a7e32621266cace0e44f669811d2f73153875c9006` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/EndLayer.java | 5084 | `57c719d1ffa1dea3fa82d5760338a14845f3d82cc2988e9c0efeebd08085d88e` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/GasPricePrioritizedTransactions.java | 4292 | `4c909b87e10787cc0a639e39a399d90389087a18629c7dfcbd52d7c9382c69a4` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/LayeredPendingTransactions.java | 22170 | `d387b492c612797cabfe9703fc6f5dd69af8c64d7f56d9ba283a886e302711b7` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/LayeredRemovalReason.java | 5780 | `2cd2e4839188727459f0599842d4ab4a5a6eca74d69a510539a00152c5ece799` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/ReadyTransactions.java | 9626 | `a9eb13c6aa381ce0fccb66310a3592d7770208e2b888091ab8ee9777c714516b` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/SenderBalanceChecker.java | 6306 | `693c2fac4c786127f3caba1bd48d3870fe33307fba467e108667e1a18f4a4e3e` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/SparseTransactions.java | 18454 | `54b5f9b3fa14e773bb01c6cba9ae4b328a3ef5a9216fbcb18e7e9ae0cd72b069` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/TransactionsLayer.java | 5671 | `7b32b11c89782837f9abcbf4b56e31b2e7aa8faca3db4fbce7bac7bf99a0321f` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/layered/package-info.java | 5456 | `a1a587719bda4e315f777aa0353fdf1db7bf4e64c2193cff6e847cc7111d5f60` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/pluginadapter/TransactionPoolServiceImpl.java | 2923 | `62c27e0e485dc5477ee254b1bc287be4e449d34fb95a1f95a52579bc045a8c5c` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/pluginadapter/TransactionPoolValidatorServiceImpl.java | 2381 | `d032a1ccf381b134f69be0a38717a9a8012d2287a08beacb69222b6fdc791505` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/sorter/AbstractPendingTransactionsSorter.java | 22365 | `060db10cefdcf420d0cbb1c0f34bc73c14538bf35cf9b02635f7c5d0bd952796` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/sorter/AccountTransactionOrder.java | 2874 | `fd61046c629ab514dc1dda2de9bbe3c661c0fcdce8b81037ec1bb71589d806c7` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/sorter/BaseFeePendingTransactionsSorter.java | 12006 | `c15a3d486c39e4a988dc0a5913448a0e09933a9698c2620194ecf6d89278a919` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/sorter/GasPricePendingTransactionsSorter.java | 3011 | `57bad2f85af9a66fc9563dff7fe313c5e0af7fed5fca4ae4354eee0b29d28b14` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/sorter/PendingTransactionsForSender.java | 5468 | `1b547ddd2c9dfa605411b1e0151cf72a8a8cc028fde7e13be1ce0887ac815099` | 0 |
| ethereum/eth/src/main/java/org/hyperledger/besu/ethereum/eth/transactions/sorter/SequencedRemovalReason.java | 1571 | `937ecdbfd0e439058a62690163beedf0c42f81d1cc28376d49e13fce0afee50f` | 0 |
| ethereum/ethstats/build.gradle | 2933 | `f756307a81f057ecb55254a710617e8a49e896fd985badc62e9eaaed1cc7c3f5` | 0 |
| ethereum/ethstats/src/main/java/org/hyperledger/besu/ethstats/EthStatsService.java | 23358 | `b6d464a8dd35f0b61435ba8cc6af25e6732a89248a73cc0027f0876c302d5661` | 0 |
| ethereum/ethstats/src/main/java/org/hyperledger/besu/ethstats/authentication/AuthenticationData.java | 1724 | `e142347903b2ccdb92fb6a54630c0068e506453af4093e532f4e85f787d5176b` | 0 |
| ethereum/ethstats/src/main/java/org/hyperledger/besu/ethstats/authentication/NodeInfo.java | 2852 | `ccdeb7e7ddc8dee422824efee6ccc9e1340705ec91f0322d9ada21505bfac6a4` | 0 |
| ethereum/ethstats/src/main/java/org/hyperledger/besu/ethstats/report/BlockReport.java | 1584 | `335ce3b069d9611c1a0198cb40ed71c51f4da95bf5be9ab65f2a4935da672f57` | 0 |
| ethereum/ethstats/src/main/java/org/hyperledger/besu/ethstats/report/HistoryReport.java | 1649 | `1b0a3ff09708b00b8c9cfed919f0723983b0a044b8129393cc7ffee7c427d280` | 0 |
| ethereum/ethstats/src/main/java/org/hyperledger/besu/ethstats/report/LatencyReport.java | 1506 | `0275cf8c2e77638cf6abb11a6b8dc2b599853fc1dcafca37e8470dba407de169` | 0 |
| ethereum/ethstats/src/main/java/org/hyperledger/besu/ethstats/report/NodeStatsReport.java | 2931 | `c8930e6df159f0bae38a30b7ef6364f2b2b21a0059177f3324efb6c34a7fac78` | 0 |
| ethereum/ethstats/src/main/java/org/hyperledger/besu/ethstats/report/PendingTransactionsReport.java | 2067 | `f9de44ada26204af726886b0c20af14373845dd23c139f56172bb08050468674` | 0 |
| ethereum/ethstats/src/main/java/org/hyperledger/besu/ethstats/report/PingReport.java | 1501 | `65abac0c065f97e94d4081d787dbf4205e5d1dbdd303b4b105d90bb0c5f7b6a0` | 0 |
| ethereum/ethstats/src/main/java/org/hyperledger/besu/ethstats/request/EthStatsRequest.java | 4460 | `8712312e1e81e2071b4ed49181fc9ba5dcc9ddde2a4ad6c0b94cec0e2c06fdc1` | 0 |
| ethereum/ethstats/src/main/java/org/hyperledger/besu/ethstats/util/EthStatsConnectOptions.java | 4998 | `41e92087911b12f1c6b9aa8fc1281a8dfe7979bfcf354eeb323ca45b478962aa` | 0 |
| ethereum/ethstats/src/main/java/org/hyperledger/besu/ethstats/util/PrimusHeartBeatsHelper.java | 1703 | `0f2b84c9574f868fc51d7aa1c243bb93d5e9b762a748a69383a5adc3c85227be` | 0 |
| ethereum/evmtool/build.gradle | 13999 | `858f5685c20acdae96d078c0eacc0e1421bcd8902e6d67c34674c7af39273422` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/B11rSubCommand.java | 10221 | `0cd55e368eef1aab46ccce5d7316464182d8b1818b8ed9c63bbfcc956f0b6b98` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/BenchmarkSubCommand.java | 8775 | `f78723976af56e69a0c82bfe1019729afb50cb42f49039d8af4617a5e3c2d1b3` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/BlockchainModule.java | 5206 | `cf768cfff4be0b5fdf421e65344b67bea96e6725d424d55ac682385e2564e7cf` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/BlockchainTestSubCommand.java | 31785 | `0634a20317d23bbcb0718cfb12dbf9a1e28a77c5584c3034cc8cf37e531b89f1` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/DataStoreModule.java | 6214 | `b04bb68a0a52fb9bff5097c119e8327d65432410321e94dbb429794a8259bcd0` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/EngineTestExceptionMapper.java | 2380 | `30335d3f9ec96aab99fd1c0a27a0d3742f9524ed45b10956180c5d3d22ed0241` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/EngineTestSubCommand.java | 39457 | `49bdf1de3014d2ee4ca4f059cda03ee30c114faf6a0e1245f7bfc0a75619f824` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/EvmTool.java | 1392 | `c1ad07f3732e1278cf070e6af38e7b8f5190735e2d109972b5e8aacb16d5903d` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/EvmToolCommand.java | 24757 | `c0bf7099faed602d9cf8a3cff8024d259fd9d53bdcd68fa7d4047656a0b32ce7` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/EvmToolCommandOptionsModule.java | 6124 | `5f42e54572be23dee823e0802d4ab4c3f1b5e37c476817b45e9288fd8b41f00e` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/EvmToolComponent.java | 3877 | `9dc9360a07a6b62edb1ee70b65cf9280b64eb32425a12ac591b9125f6281c815` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/EvmToolMergeCoordinator.java | 11519 | `bdd2fbf4adfab61ec043b66fa579df7dee78961a60348b13a058beb2b6405221` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/FixtureRunner.java | 16246 | `69b1f3ce85fbc355a9fc1c025627878febd5fb4a3a3c3975fa54b0ff286d6667` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/GenesisFileModule.java | 5422 | `2c41ae5eb35df885831579b144d1aef04ca9f24f64a1f9805b4c4804b930c62c` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/JsonUtils.java | 2236 | `cdb940295a7f3c09050416239a153589f70a12a05c07583320f9fba69aba22b3` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/MainnetGenesisFileModule.java | 8686 | `9c6802c8267dca5454ff0e3975877eec3201918e724329d9ef38c1522a27221e` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/ProtocolModule.java | 2153 | `f21476db659578f50bb7fbb1eff7ceb95eb3ee69b57409f015d2da86b5d532d3` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/StateTestSubCommand.java | 29459 | `36b266e8f2242ffa93936fb482b139cbe7b2b6b6eae3343fc2efd011d6ede583` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/T8nExecutor.java | 32853 | `4c9768a80e935dec2e023dface8051b310e69335b2afceccae4a177a58dd2a82` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/T8nServerSubCommand.java | 12689 | `b25e1dc8f8b51c1a4fddb029069880dc9962d94e49e2ae299c062acd4bd28c68` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/T8nSubCommand.java | 13492 | `1f11fad03bfac764e03358295752c709ca9ad1bf2f2b1a16b93936d87e4823d2` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/TestNameFilter.java | 6339 | `6030b828a2c1e5f5ee892dd61009135647f0313a01ff6b0ccc18a2a1b57a5627` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/VersionProvider.java | 1790 | `517a8b51fb24ff53bf9e19c6031308acbda862d89b2b502c99a5f8e5a5ef8062` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/exception/UnsupportedForkException.java | 1012 | `75e8890b935fe10548d0d17b21e3a9920aa5f6369a3e2ec64232b317d3ee3729` | 0 |
| ethereum/evmtool/src/main/java/org/hyperledger/besu/evmtool/t8n/T8nBlockchain.java | 8965 | `fe2eaecb0118fa8395fa4307679970969a33650a419a6d53b0f661ac68f84b3a` | 0 |
| ethereum/p2p/build.gradle | 3488 | `26f843385754a35c074bcc22f546fd49e1572ae610b02db1e5d012d9cd0d2911` | 0 |
| ethereum/p2p/plugin-api/build.gradle | 1784 | `464c111c73066341c2ac58cd53e92e15b0bebfe57db53ec581dee771e0642824` | 0 |
| ethereum/p2p/plugin-api/src/main/java/org/hyperledger/besu/plugin/data/p2p/Capability.java | 975 | `5a53a8561d1ece5b978cf6e6bca563096f4dd5fcb754ac6701d81c623a0d6bba` | 0 |
| ethereum/p2p/plugin-api/src/main/java/org/hyperledger/besu/plugin/data/p2p/Message.java | 1148 | `535a288291f5a3db78ec7408eb0dc679b27dc411b1b3e7349319c206631fd7b7` | 0 |
| ethereum/p2p/plugin-api/src/main/java/org/hyperledger/besu/plugin/data/p2p/Peer.java | 1022 | `0ad886429622c23c1c039381efbc05685e7ead981c7490633f35d88665b2e5c6` | 0 |
| ethereum/p2p/plugin-api/src/main/java/org/hyperledger/besu/plugin/data/p2p/PeerConnection.java | 3013 | `f5a938287b1a76757e15b2f029c23e034d862646e9d2054f8ad493dd9bb3ee11` | 0 |
| ethereum/p2p/plugin-api/src/main/java/org/hyperledger/besu/plugin/data/p2p/PeerInfo.java | 1342 | `2ff537dffa7a5f3baf208c60b218792ef93cdef4117564db7dfe74708974ab35` | 0 |
| ethereum/p2p/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/p2p/P2PService.java | 4956 | `4071c0945849b19eaaf9d9b008f7166dd46f2956b0f106db934c5baf8a54c65a` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/config/DiscoveryConfiguration.java | 10042 | `968bb3ae27ed837c57730079197445727a752d6be62f00bad6cb267ca7f6207e` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/config/DiscoveryMode.java | 1169 | `ff6cd93a6ce1ba7145fc27719f1ed484126d16f8f8aeb8ea81f668e1d66db818` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/config/DiscoveryModeResolver.java | 3002 | `ceae812a4833ebeeee7315333abeb52df590d2a6e95d7c863443211b5ce1a1f1` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/config/NetworkingConfiguration.java | 2226 | `1f127462b60dd216a6de1cfcc0c815247de88df6235bf81b3b7a48a55bd8ceaf` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/config/RlpxConfiguration.java | 4329 | `ca0ab2eeaa18356f9d4306dc3b62a4d7c86662828098f85525d63cfb81e8752d` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/config/SubProtocolConfiguration.java | 1437 | `b440ae927ed4197d4b4a7efe19dd061c93a97155de725e2c69df7bbff9385068` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/CompositePeerDiscoveryAgent.java | 8581 | `2d131e7283b305d967e3c1f14d00f20dddcb62c97bd9832a6fff47e157ebb068` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/DefaultPeerDiscoveryAgentFactory.java | 5715 | `11ed27543018b5f052579077a89900f0326cf2c4e94fff0f7ea2c44d411ca5f8` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/DefaultRlpxAgentFactory.java | 5446 | `31fa4cecd5e63b79e50fae50957c332d800b3e94f839868691bb3b72c22be089` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/DiscoveryPeer.java | 2416 | `e0e863bf53a3d629d282dd5cbac792fda811bee86e26fe448379b4c764ef24c6` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/DiscoveryPeerFactory.java | 2770 | `2c932de89cad6d9f8910a1e7c13188332bdee590fa12336bd48c1b380c8f27da` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/HostEndpoint.java | 3062 | `ee2fbe05654f44668c1a093714e8e8b9ec15e34fb2a158b5828919c01cbafa65` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/NodeIdentifier.java | 1730 | `f00235ff855bbabfc7c4f7da28579b41a3c62fbeee8a1bc50531f01d79cb74a5` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/NodeRecordManager.java | 23931 | `81ede5f8a0560147c5f6e8a6cc04a7bc9fb703b31f856cd225252b9a5046aa93` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/P2PDiscoveryConfiguration.java | 1674 | `6b65e486133b615bc21f11292cd657d8a8851227172485461cf3e72c9e1988b6` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/PeerDiscoveryAgent.java | 3735 | `9aba9e661a1b8b1faf7b2c6599e860518b0521109d32c4eeaa9d0c5751b067b2` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/PeerDiscoveryAgentFactory.java | 860 | `e550373f0b0ef37c174ca2283c9b6ecfdf6dc66738d4ac740d9b94f4c56dc7d2` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/PeerDiscoveryPacketDecodingException.java | 1065 | `357a5afbe6c51dfe58a9b67e565e4907a242f2abd298c752c405ee066ff5776a` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/PeerDiscoveryServiceException.java | 935 | `527480aeeab0d1a535a87dadb70a06f628b7a9c0dc169e1ca1f12fc209763a41` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/RlpxAgentFactory.java | 1087 | `bcf724d7cf8a8e98a3bf291f52524ce590c27393c389c59ec33ff3e858bfb689` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/Endpoint.java | 8210 | `9bcee079478b7f2a39d5b4f7739b45ef1cda5a6323ddae6f921b5fcce70a5132` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/NettyPeerDiscoveryAgent.java | 12196 | `39730d46629018767c02f9e40c7352a6177bc11662ddeb8646c562b19f82680d` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/PeerDiscoveryAgentV4.java | 24367 | `a5acc15c85e3a5fca410dea552874cb68e9697f01bff4990b8346146f732ba48` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/Transport.java | 1572 | `f04e85b5e655b88d2e88758d726a4bc28417abf8ae3450ab9ee6cc069cbf408a` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/Bucket.java | 5523 | `7688adcc424c640e7953c4402ac40c786f3b6a14be324379de293ba1c885454d` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/DevP2PException.java | 820 | `4107edebf2c8ad19e7550a8fa92e745d94102199b7abbffbafb2a118b7525f7a` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/DiscoveryPeerV4.java | 4280 | `aa3154f9738c8d481652d17a8df070cce36abd308526229ee2bd5300c446bfc4` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/DiscoveryProtocolLogger.java | 2883 | `25757f577349d407733ad8a16e2d97980379c900add3f32f7261a9476c25d260` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/OutboundMessageHandler.java | 958 | `16c2feafbff0ab3a460baf5b319cb77e59fa58d994cacffbfa61caad67f4bf07` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/PacketType.java | 1570 | `4151970e4caf8a9ef2c3a987e170209a8851632e5614e02d90a7b37940e77469` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/PeerDiscoveryController.java | 47650 | `cdf70ae6a66450cac80fa5a65088715fcfcebd6267e35bd7b42bc3f52ae51a63` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/PeerDiscoveryPermissions.java | 2265 | `80847fb3e74cf7069e6f5bccf9d97d668d547f9d9997a1990ae4a18e602774e3` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/PeerDiscoveryStatus.java | 1444 | `11db2cf7055524f059e9acf86539bf5fe9990d0693cb3a6abefb5eee66efc878` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/PeerDistanceCalculator.java | 1526 | `0546c91916b1f5477c1d981e204d82e684d87f26a9219d33d7f65d6e22b2b8d8` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/PeerRequirement.java | 1153 | `dce239c760fe1ba6cd7a3bc1c9664041e6ed4caa021c1b0ac02259c82746d8a4` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/PeerTable.java | 10295 | `92e73b5ce89c58ceb98e83e3c84abc301923b4b84cdf1a7eda84152e28306e92` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/RecursivePeerRefreshState.java | 13468 | `a734df5f90ae08f816ce610558e6aa10bf143021291a988dfc56ec8328c15a70` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/RetryDelayFunction.java | 1235 | `d17719bcee05907c035140c0f5c00fb78de8eadc48ca966a99df1b649f76c0ff` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/ScheduledExecutorAsyncExecutor.java | 1674 | `204f6987f5965caeb7f1f06bf93964ae3f4b00b2c10971c7d267cd168044b9fb` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/ScheduledExecutorTimerUtil.java | 3705 | `b2a0b23abf050754046439384aa74f8487371527deb737c1a5be4873318d57a2` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/TimerUtil.java | 958 | `a7a2562d163d77c2ac62a28b310af66d22dd9442d7c1b508d1670b6cd215c677` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/Packet.java | 2459 | `760f8477390d0ea1b1ffdfb0cd92dcb63b3cd3c5908f4fe801a21d49f75dfb24` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/PacketData.java | 1057 | `f89943eccfd1c75c65d1c9929b521334cb5a573c699a933a1db56e68dc850457` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/PacketDataDeserializer.java | 851 | `c4de9c1346d8c218ae58f359b2bd47de009e3b71abf88313651bf80723ea12bb` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/PacketDeserializer.java | 4851 | `2c9df63e1728ab8b04f74b4cfbbd7286e14a7602a685f3a30502edf1e8d21ca4` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/PacketFactory.java | 7590 | `d87c3dd4b4e127a3f47efd6a8e7b6148486d79cb1edde625196a899787440585` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/PacketModule.java | 1364 | `d149df43ffeb44d9e7b2ff2741996dab01e32653ea74c7113c5728ea26b999be` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/PacketPackage.java | 1989 | `ac2594fbb7409544c36724cb18a8d335ea03d15a352db29a3c38da8707f985ca` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/PacketSerializer.java | 5655 | `e63c23c59a426a359a9ecd09464989ad512d5a2daddb573a4288c2fef511b3ec` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/PacketSignatureEncoder.java | 1381 | `3e53a8140b10e871def154a201a8c323b4caf5d09e6081f280103565b72a0829` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/enrrequest/EnrRequestPacketData.java | 1193 | `2ddb74981e075d354eb640125082d3e0ce0cba99e0c851b0f8dceb4f7292b04b` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/enrrequest/EnrRequestPacketDataFactory.java | 1715 | `4ba26fe9a0dd0e62e0b56f6e1d5288cb0fd6cc1847cb043717adb667070cec2a` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/enrrequest/EnrRequestPacketDataRlpReader.java | 1538 | `5137e9579d017b42899d5728583517469aa3b0750f5288f9463100000b0e28c0` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/enrrequest/EnrRequestPacketDataRlpWriter.java | 1142 | `04fc19ee8859aa3705985bc06ed218b2d77b3306e296540ceaaed9ea33bafcc9` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/enrresponse/EnrResponsePacketData.java | 1507 | `a43a0b87f4e73d8b231d7c0560e8466709b21379ee38ef1a5b60363a330dc170` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/enrresponse/EnrResponsePacketDataFactory.java | 1763 | `3315d9f2279a7977d45413c79ef0f1b49fc1537dd6e0ad1a01961f579bebc9cb` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/enrresponse/EnrResponsePacketDataRlpReader.java | 2335 | `f17a3fb2fc3a02882987bc3b24d5b5b092fb9bb78e0742828b8984c6d6e3496d` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/enrresponse/EnrResponsePacketDataRlpWriter.java | 1211 | `e94598661e48fa876a626badf9e339e9b2e1f9f3287fc3b0f2b7a4b9a4ce8522` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/findneighbors/FindNeighborsPacketData.java | 1459 | `13d27089f367544f9e2aff01b7db8c5428451fb1ad78d94ab3762c5ab635a103` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/findneighbors/FindNeighborsPacketDataFactory.java | 2151 | `4a5fa6c17a11bd637a7e2729a5e29bf1df6321d1380ce778b7adf29be7a31ed0` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/findneighbors/FindNeighborsPacketDataRlpReader.java | 1666 | `2d93a82c4baf914916c001f6f18efc88b1b75f3557912ed7661d3b4ca0fe01f8` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/findneighbors/FindNeighborsPacketDataRlpWriter.java | 1217 | `eef2721d4e7a2307affd6656d5f9f2b3fa40e76259b7401ac8f49ad6b18887fb` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/neighbors/NeighborsPacketData.java | 1493 | `a638bdd268905d50cab60c0b5d47950084be7dce6d518ecf325deb08382a454b` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/neighbors/NeighborsPacketDataFactory.java | 2289 | `6772d64c52447bb9aa302eb3c6d150c9a22234e57b9aeaa10010a699eb8b81be` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/neighbors/NeighborsPacketDataRlpReader.java | 1720 | `c109d7f45cc175bb78042d052933a142c664751ba2dc990f8353faecd537b430` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/neighbors/NeighborsPacketDataRlpWriter.java | 1297 | `499f9bef635fb45f2602718424d4824bef115ef17e810823eb3fa549d95592bf` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/ping/PingPacketData.java | 2483 | `5eccd28cb9d2e33aa732192e554f5bc74b87af67525cfaa18bfc1eff7ea25758` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/ping/PingPacketDataFactory.java | 3057 | `5e03d0829255ba1e8d24b8472b0d76e72cd902eb80d7a5582d33920165547d6c` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/ping/PingPacketDataRlpReader.java | 3067 | `c473b20837bafa42bf312f4abce770ff9ebaea31976428dde4b06ca7fc0e1959` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/ping/PingPacketDataRlpWriter.java | 1446 | `b9b18d74867c9877c382ba168d6830f816e72078f01bfa0b15b410df521569ab` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/pong/PongPacketData.java | 2034 | `95111f5f520fb03c18de80a98b962e29c272f9852c456749d697140e806f69be` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/pong/PongPacketDataFactory.java | 1994 | `44463ed84c6fdc29e91a4ff33610cd1b7514772ec0e35c02d2de8f16e7be3b89` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/pong/PongPacketDataRlpReader.java | 2323 | `99870d6da7bc5e07ed6904b22db0e5a9f0343542ea35133a5f17b610d4c4a2ea` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/pong/PongPacketDataRlpWriter.java | 1320 | `584754c432476907e6c62b2293b919f8ad7e15af233d17c5cc2ca4299f8ef01f` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/validation/DiscoveryPeersValidator.java | 1178 | `490c4981a7774dcd5ffafdde9c9f19984c18378ce3bda97507ad288350a53156` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/validation/EndpointValidator.java | 1122 | `73d5c19233dfb432a0ea101584b8421a85b1183a892034f88c6982908ede2d46` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/validation/ExpiryValidator.java | 1237 | `70e4608f1658a5a9e057730c66efd07239d14afe5573e3edd85fbf83b16679c9` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/validation/NodeRecordValidator.java | 1119 | `8a24c2b75568411e950c4d87415558bc29777b19fc4d2ba2a532de9bd4c7cb86` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/validation/RequestHashValidator.java | 1101 | `64e7daf449cbe3a09b143a892975598ac9a4753ebf6c7e1e7686f23b4fabe9a7` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/internal/packet/validation/TargetValidator.java | 1272 | `85955062998d8fa1c2a2daa1c576e71435437be69be48e292d2adc67e2d8d442` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv4/transport/NettyTransport.java | 15047 | `591cbbff9116d3fd71074c97e824316d3451078150542ec2e4cc160c096b32b1` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv5/CompositePeerDiscoveryAgentFactory.java | 10680 | `d988e77455985c7395b432f4334768d041023726314dd5c0e584527f27e4d628` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv5/IpV6NewAddressHandler.java | 4881 | `2a88d6eeec646f1c7a39dcb3af6b4bf51c40a43be88a491c446f36e581518f4d` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv5/PeerDiscoveryAgentFactoryV5.java | 16484 | `58f4df6bd8190ad28f67acf96ad940760d7ab16391e08971bea8884af32d12ab` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/discv5/PeerDiscoveryAgentV5.java | 30504 | `d90a52e4646b35657effeaebe8cb2b55399a5f4b29eb144ce7bcec9aa3345fcb` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/dns/DNSDaemon.java | 4010 | `0a3343a62123d26ca80f6ba160a21065203c494be2040d5bdf22759b1f6ab5de` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/dns/DNSDaemonListener.java | 1166 | `eb3867cbcdffe4354262802b126ff2a4e42850294bb78f23dc988a270dd0675f` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/dns/DNSEntry.java | 6930 | `6ee9c5a219bb6566efe06d1ef09a52bfa4dc23d1b90de1ef618d1f9bf40f7c43` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/dns/DNSResolver.java | 12720 | `df3321acb5b1dffc13b31a80e0f3d4b83c36897aab6716830473b94e9b95a1a0` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/dns/DNSVisitor.java | 1139 | `8972a5ead204b4378598b5f08c26b5fd30c3fec1518b0443a7637e365249446e` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/dns/EthereumNodeRecord.java | 8344 | `52af24b0db90b8ede05bf57ac197acfd2802a8cbaa0f8be569078bceb28dff17` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/dns/KVReader.java | 1749 | `ea1cdfe70b7bce30160dac5f721e423905b78e7c9eaf9a8234b7301c22ff1425` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/transport/BesuNettyDiscoveryServer.java | 2827 | `ced64f90b69f6256a601008e08afb77102c1c1e55e70df88cf5dce1a3bb7adf9` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/transport/DemuxCounters.java | 1207 | `76c41ce23d1167114cbc02dbcf7b54e9e3492e1bad545c235563c8f5ad2a417d` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/transport/DemuxProtocol.java | 1009 | `bef66dd03e62391f7191dfb5082f6c4edb9a416cc2521417d964287e88e4e854` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/transport/SharedDiscoveryDemuxHandler.java | 6311 | `1f6ff45302d3c4d615fbf0831623029271fa9e49dde6d1fb70cc44b57c1c8195` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/discovery/transport/SharedDiscoveryTransport.java | 23566 | `b12d6991d6e29e0d981dc4436490ef892432fe9f990c5f28a8c7c25597ff40ce` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/network/DefaultP2PNetwork.java | 27352 | `d12f5039528d8718ba35b9280459307b40ac52d0e160f8b74f8e021364dabd44` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/network/NetworkRunner.java | 9529 | `ea91610a545c92b25bdb321412acf87b339ab6276d052f1ff774e775194c01e0` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/network/NoopP2PNetwork.java | 3266 | `66a3ae3725b93a1ecd62cf9fb3728b2fdfaaa08d9c3c22d477f843c3d29c9580` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/network/P2PNetwork.java | 6459 | `d0633b4140a79ac43f71de8a92d28f7408b96f5696a2389b7a7e8d0186153aac` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/network/PeerDenylistManager.java | 3385 | `fefabde2d74bdabaa969ab4caa8da0070c98b20b2e74e43ffb803be8b5006beb` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/network/ProtocolManager.java | 2630 | `f4e99a484aecd3c58d6eb8f966effbdb2a19bed88a43ed1702315561136295e4` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/network/exceptions/BreachOfProtocolException.java | 836 | `8dab505b270ef1b28172e2404a89559e2ce7dab7eace7d687d17836c24c6b821` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/network/exceptions/IncompatiblePeerException.java | 836 | `dc15f57ddd90d6bf9d22e440e2b51cd2076f22f6cec3effb54a8d41c4f8c7907` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/network/exceptions/P2PDisabledException.java | 825 | `992432e686f91f5992efdca3edc7f5871e64aab6172248745d3848d6a05d8f6c` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/network/exceptions/PeerChannelClosedException.java | 981 | `6289168ac3f199833401835e943016ffb4ce26fb7e49c75be6731da3342697bd` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/network/exceptions/PeerDisconnectedException.java | 987 | `98b9f8084e8bca2a8f479d97869d1fe3a798a2e3b4b347f265c032f73cba0d05` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/network/exceptions/UnexpectedPeerConnectionException.java | 852 | `281d126452a956aa51f0e0da744438b949a142d7cb5fb16e78d3d7be360cc02a` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/peers/DefaultLocalNode.java | 2882 | `1a60727315bd77bea63b1c2c334d5247244748e2884e017ebdfdbde0be287092` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/peers/DefaultPeer.java | 2914 | `144845463f7722c89db2c6b9ce4045ccef7932cb93b268527f679d45fada9bf0` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/peers/DefaultPeerId.java | 1546 | `65204cee63c2efd32c8096cabd7abbad1ca5574f96d70b14b5edf1b289807470` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/peers/DefaultPeerPrivileges.java | 1109 | `800db1ec0c9e028e8591fe569fa46c504d9bca6b80619992c5120f9fc4409188` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/peers/EnodeDnsConfiguration.java | 1036 | `b976acd9e883d24e7d799238c74b0ccbc78a65f69b5a41558d1c06af01fc803c` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/peers/EnodeURLImpl.java | 16776 | `6373c6d53f91d8553f3d06b8fe634db17d786a76cb6bddede0d6ebd15c40be50` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/peers/LocalNode.java | 2417 | `40a55794f4ea4f180f169610b53baa10c9c2ffc0aa828fa2e2cdbfd5fadb7d8a` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/peers/MaintainedPeers.java | 2524 | `94c928c6b335c1ad89b152a6a653ea76674814f00e52b3cd9acf7df8381cd473` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/peers/MutableLocalNode.java | 1253 | `74c9444991e3e87e7e8c511458a2b2a9acb4ac35c7d076d866f61ef9ed8df5fd` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/peers/Peer.java | 2054 | `05d0d364580723484e3ea746585bdd07c07d70249d9747c6e57ef72cccf09bb0` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/peers/PeerId.java | 1237 | `924d5588388d620b623423f4e26897bc1bd4b65cc0fa54d38709be75591044c9` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/peers/PeerPrivileges.java | 1135 | `237c7e8488c01f1a6e669a3f1cb3393b3e2b3eeae275344ce03d92d78ca679ec` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/peers/StaticNodesParser.java | 3460 | `13b502bd0b2783b3de1582b282010efe704296a4e67784fd7a873feb1ee39f73` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/permissions/PeerPermissionSubnet.java | 4166 | `b43628a4131b9870dc2ffa030c890baed87a19181f0060e190b93602593f62ab` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/permissions/PeerPermissions.java | 6918 | `6dfb3dd2e25ebd2bd8a20c97957400679bf57147053529538a266aa6254d22ea` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/permissions/PeerPermissionsDenylist.java | 3082 | `3c64f0fbcff37cbbf19ee42d754c0ad76502625e3fdfb27bae60b64ff01b23b8` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/permissions/PeerPermissionsException.java | 1291 | `a7159f6e333c55e05c40783fbc2082b6f4825c4fc9eeefef7552e85ae64dc0e9` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/permissions/PermissionsUpdateCallback.java | 1577 | `0971b58149f138884652792b79750299eb743deff83f67a5f26725e60c8c61a3` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/plain/MessageHandler.java | 2524 | `5c0cc13492b2271774b0a5802e805aca70b43a26d196716ed70d2ca2f48a9a5c` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/plain/MessageType.java | 1109 | `91829b475bd7e54d536ce516139de6149b881d9bfd60d02ba75afb3a55cec573` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/plain/PlainFramer.java | 2030 | `b40f8f33734d0c65c89eae73b2abaeda7f47037278b7d04b73d4fe6bc6354644` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/plain/PlainHandshaker.java | 5608 | `d40157ecfeb020d3a6f908a589deaae0f35e8f2dff5ac786b5ab131117f4874f` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/plain/PlainMessage.java | 1439 | `a7e02242d052a4f56fe349c9b58d51d1228de3157e64f5a0ff80d4f3639b1bd5` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/ConnectCallback.java | 848 | `4cb780ded439abf5a6a57ecdcd81e7e6d79752bf9e9df79062325424e0f44d4a` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/ConnectSource.java | 1428 | `7649ca2c6b733f008426f2affd1206696443078b2eae864ff34bc710109ae74c` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/DisconnectCallback.java | 1037 | `ef9bc48dfbb00874910bda41f1f90f2d33099881abc1e43709246cf37ae85d7f` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/MessageCallback.java | 922 | `0f0c12c00c059641cc4da04dcd4f6ca16d1371805a51183076868cd9c4f6e0b3` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/RlpxAgent.java | 23848 | `2d11910c62fe9e5e873b4608b115934634da1379c189deaf419cd894fa39e4b9` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/RlpxFrameConstants.java | 874 | `81c89f2c8bb33505c72e88319c9d8971c1058bf7725f17795a7d6e66a325abd6` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/AbstractPeerConnection.java | 9557 | `5638e41822ac983d4089e5be659e483d163685cbde941395eeb008e82b111346` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/ConnectionInitializer.java | 2465 | `0f31bfd375c61a4f5972fd87e631bc4a19875103341e119c4963c71c66d44ca6` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/PeerConnection.java | 4325 | `2e1fd1ace3a4cfaea7291d81f43444757a5c393f8897f8d5e2414c26ce96a6c5` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/PeerConnectionEventDispatcher.java | 1220 | `698d645fe414fd0e62cdcc4e3f3969152aca5afbb7d9b4079cf404bf9a011917` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/PeerConnectionEvents.java | 3228 | `ab5314421f40ee7d435685163ee366062b912a95c4fa95084f4165c747e44e79` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/PeerLookup.java | 1360 | `89dcc81f7ff85aabc5d1abf8858bef9876a0d2c86845b91c20ba1c314ab23a59` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/PeerRlpxPermissions.java | 2650 | `627ee9781a2987e428bc8019a2c85bbc185e54cb30c93a5e2c50ef953b4f4e54` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/netty/AbstractHandshakeHandler.java | 7411 | `58f15a15464b91946b54380038c74a8dae9b2de3f5bfd898023c5548640c1038` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/netty/ApiHandler.java | 5364 | `8991e7ea636a145a6c7c44592f94861f8d85da7c622a14fd679e988997aedb07` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/netty/DeFramer.java | 14383 | `40f5f63a7f7ac137f884fefbac941bf5edcb1116573896f992eeae0dd8012535` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/netty/HandshakeHandlerInbound.java | 2692 | `c1a3424c47aa32ad1ceeefd7b7e2a8eab15c8c96b81b99cc641be5b706e35789` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/netty/HandshakeHandlerOutbound.java | 3580 | `cb4d9c7a24884473aed4821e4cfb622a97eafa666fbc49eff0dd5ce7aa2a6929` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/netty/MessageFramer.java | 1475 | `1042e43fa6975a1ed027e2690a8f17f1cc6dbd2850af5125f03e270731ff7d7e` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/netty/NettyConnectionInitializer.java | 18247 | `6655b13d42225cb9c16dda9965aeb593091ed1f8413e7c445a2291538f74afd0` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/netty/NettyPeerConnection.java | 3069 | `6ddbbd6242015c91237ca2e89ef290a13151c50d3c198c36f215604caa00ef91` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/netty/OutboundMessage.java | 1199 | `ff48a110f6113c5e580041d8c684e845a6a0e92acacf04d35fb02a991a7c2a2b` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/netty/TimeoutHandler.java | 1843 | `359d8a8e543ff8347ee9db75d05aaa9a91eecda60cea262c36be1e74400d8119` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/connections/netty/WireKeepAlive.java | 2624 | `c7384d6b3371ce68c5636031fdd7b09e35ddc94c2e97c31aefede6602cb09b2d` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/framing/Framer.java | 18113 | `202f15757a3b6928627d51ff01b876484e9f4c9d0bd8a5b052e431331caadbc6` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/framing/FramerProvider.java | 865 | `4a333ef48d842b8b4c6890a627eb764744ffedcda163f5e0000a97acea86d4c4` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/framing/FramingException.java | 996 | `1c031a382fa167c28a799101b82f8762362438e4202e3a2244d3643d4422c501` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/framing/SnappyCompressor.java | 1893 | `741e8db24776afffc8de2ff713f98bd55dcaa41cc0ddfe0cd525671dabb7ce81` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/HandshakeException.java | 1004 | `6ca3d3265ad0df935f1c6710aa99dc1e06dbb9f69af771fc73281d292433d98c` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/HandshakeSecrets.java | 6514 | `8f8c5aa5a37b1cb7083cdc034ddda322c26314876159a6058178e094dcc60742` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/Handshaker.java | 7185 | `92bfbd771a9a4d1d70f6f06b9d6a307174b98c03e221e20d8c96ea29bcbee45d` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/HandshakerProvider.java | 778 | `0b2d4e6b44f70b8f614762deb7553e5c9b6a5dccd405a1ea9d7b485b85f91942` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESEncryptionEngine.java | 13477 | `ebaec50da819dc986393d25555295c0fce5a75540121ff186e849812f5992c8b` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ECIESHandshaker.java | 13970 | `1f12826845daa8c859f8c0bb2d7bf40c081ceafc722be0b44dfe3daf0c5200a2` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/EncryptedMessage.java | 4317 | `f94e424c7ec6465ffb934f5bd8578d9098c1559e051cfe64ff182d2bf4a652c8` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/InitiatorHandshakeMessage.java | 999 | `440a60aff2483863195cd4c907121a73805667e576fc5b4f137a3b1f4c81bee5` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/InitiatorHandshakeMessageV4.java | 4141 | `c3273e067c9181ac52238603d558f910f97ef650c6c87db925b845dea18a4016` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ResponderHandshakeMessage.java | 941 | `929465d206489543d73ff93f898522c55f267229f24d589514eadc4f4794fa9d` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/handshake/ecies/ResponderHandshakeMessageV4.java | 2345 | `8a5cc8f16c8bfa2925ed9e090912ccdacea14a6f92d68f75b347d0117cf331eb` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/AbstractMessageData.java | 1551 | `3326f54788f385310746c54e15a024af0059aaaa57c82cf0f55b3c15987e866c` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/AbstractSnapMessageData.java | 3010 | `6b5ea44ff6e7f371cb0a8257ef37d7c1b1dcb8998f630360b7ae52fac67f2dfc` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/Capability.java | 2625 | `840706815e4d181c963107c0faa9c5370ded161a2f0ea6a63c1c2146d2177b3e` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/CapabilityMultiplexer.java | 6345 | `48144a05c07c6a140769c2423f1837b6e6439984d79b34859bdd031e250b8f4f` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/DefaultMessage.java | 1306 | `d798f86d47d25c0c8cacd26e4ea9abbd83e21a1efa9a75649da18e84c0f3b1e1` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/Message.java | 1216 | `cc5f8c3f62d92570410906f5e22ef2dfe8eac0168a422b43e7d89bb5c52e0a54` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/MessageData.java | 3238 | `ea5ab963a4e39d650c0ec69c568fa8e4bd1dd7b4a9069456fec9888ac5a1e4f1` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/PeerClientName.java | 1471 | `0d679770cda7e6bcf140fc4b14aec5cd7a129c1d89cac7b7af87c254065aab3d` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/PeerConnectionGatekeeper.java | 2276 | `9093ef15e64769c843bb0e15b1e6e90754cfa71ff43178081a7d574e29577c1f` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/PeerInfo.java | 5465 | `3a38fa5ec4b3f4d1b80482f66bde6181094d684a2a72cd7b1b13ff2ca04585e4` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/RawMessage.java | 2319 | `34549a52c287bcf6ef2374c8b72467d79b9e077891196c4859e3ace00cd91142` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/SubProtocol.java | 2045 | `1fa73e82e20ad2c79041ac54b323a3fc26ea61bf6d7debf85b44afa86a37cada` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/messages/DisconnectMessage.java | 8497 | `7d8945ab81b6d9250f88e8f2ad1db588b0d24b830727bb069351617566c9f521` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/messages/EmptyMessage.java | 1209 | `74c58d508755d28f8053e72aa85133456d19fe0ad842b4f4500b84cb8939a3c0` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/messages/HelloMessage.java | 1950 | `cd24952e2ee79d4f7882a49d7d8168c621996e0d2f63c591b9c41e78f3faf3c1` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/messages/PingMessage.java | 1053 | `2ab22adc27351f910f560bba380033f5e5250382c1ee76ea32014c83fb9a7cee` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/messages/PongMessage.java | 972 | `3928726feef32af00edb2e108cb9089508874271f425a5358227496e1ecfb099` | 0 |
| ethereum/p2p/src/main/java/org/hyperledger/besu/ethereum/p2p/rlpx/wire/messages/WireMessageCodes.java | 1162 | `ab74172d99fe070fb536255c62b7fbaab11f66742522ac5fd414ffb535395cda` | 0 |
| ethereum/permissioning/build.gradle | 2604 | `d79d61216102ef941ba309f8fadc1ee56ba973a2df6e90271d18d86e16167051` | 0 |
| ethereum/permissioning/plugin-api/build.gradle | 1707 | `af96e384b3b151819396a0a57bf6cfc3fbdc47043e78e7750fe361dddd764b3d` | 0 |
| ethereum/permissioning/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/PermissioningService.java | 2235 | `8d3057678dd6c54e286323935e18a9b1339f2cf1399b2ea09553d3226543b609` | 0 |
| ethereum/permissioning/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/permissioning/NodeConnectionPermissioningProvider.java | 1609 | `2dbe95f474d1ee657d5436688b4fc0b12bdd436f62951b9e211e4b01253b932d` | 0 |
| ethereum/permissioning/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/permissioning/NodeMessagePermissioningProvider.java | 1597 | `a0babb1374de94d20704733c25271abd7ce51c6b3001b8384ed12f940bde3317` | 0 |
| ethereum/permissioning/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/permissioning/TransactionPermissioningProvider.java | 1632 | `46d5d1500faf51b6eea85d35c9a867f471e53f94cff3cf0bb8f60f75069a5286` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/AccountLocalConfigPermissioningController.java | 10906 | `6b1ae727943d9593dc21f21b2de93ee9e82ae8815366b59c570d759d3821e03b` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/AllowlistFileSyncException.java | 736 | `9142230da690089f3bdc3b9e9ca77acb6fee875105bc4dbc6e87f8e86a9e9630` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/AllowlistOperationResult.java | 941 | `956a70ef699370fbb24b873ef0688885678ee8a969304939fbbd0695d9d6559e` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/AllowlistPersistor.java | 5829 | `036fa5f8a6b3fec247d2ab267bf28f9415bc180c12f217f50756e973db397c70` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/LocalPermissioningConfiguration.java | 3209 | `06cc63476c100a50a4a30f76d2d279d4d28ecddf5a8f389eb2d8c105560b821d` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/NodeLocalConfigPermissioningController.java | 13666 | `825aa7df4a90be8eeab58a27e024db67cc04f71ce30d6fbe8ae479c2995d84c7` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/NodePermissioningControllerFactory.java | 2678 | `704012fec4c55774f9e9d15412b98de6aea9498b06df0caa288a6f17fde3160b` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/PermissioningConfiguration.java | 1185 | `b140f5a43d5c165242137a1506ac973fbdfcbbcb116745d791f858741bc6c293` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/PermissioningConfigurationBuilder.java | 6130 | `c25f796ed7671dec1db0d04d2d65a47959c5d7b3f8ac72a46ef7247388a7539d` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/TomlConfigFileParser.java | 2897 | `6cbee9ee0608f18372b2539ca7ce62e289bedb8a03be636928c3fb147d1129d2` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/account/AccountPermissioningController.java | 3158 | `898b3760754a1b6a4f5c77fd43f8cae0d697fa7106bfce02d5593f96d132d1cd` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/account/AccountPermissioningControllerFactory.java | 2947 | `983971c63d5e420dfbed1c95b325bcb0ce02739be592cbc4f76ae0d5fdbf62d1` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/account/TransactionPermissioningProvider.java | 868 | `c789d11c826ae3fd2baa75b4b6d6d1708ee53cebcbd75148fe434c9eccb8fb0d` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/node/ContextualNodePermissioningProvider.java | 1939 | `8dff7368c3ead30288201602bf194929a8850850a8b3e80494e9142cdd9a247e` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/node/InsufficientPeersPermissioningProvider.java | 5420 | `2d85f45c401bcb1816cac6e21a66ef018cb23c731bc3f43fbb665d14ccc3d50a` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/node/NodeAllowlistUpdatedEvent.java | 1861 | `3a40d319ba75a229713b29f971c6435a7d53c71613af2ca0fa13223cbef662b9` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/node/NodePermissioningController.java | 4035 | `56453f8ee4d3ddd7fe2abb48ac003c4c9e2e25ced3fd158533d376b6edf629fa` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/node/PeerPermissionsAdapter.java | 4040 | `a57b308767cc9d6bef958048d89ffb5442a943fe424b7ec061a7ecdbf47573ee` | 0 |
| ethereum/permissioning/src/main/java/org/hyperledger/besu/ethereum/permissioning/pluginadapter/PermissioningServiceImpl.java | 3225 | `6bc212f4f12980880aa43c3583360818639dda7277113b1577d7a504dbe82641` | 0 |
| ethereum/referencetests/build.gradle | 32798 | `ca60a0b12304bbaf4466c30bcf2d0e9d774146950473a98e1fa62c5bfaa80ef8` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/AccountChangesJson.java | 7662 | `16a704024bab07124ce093b19632a59ef2e679a5e890361629136411e8e71c7b` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/BlockAccessListDeserializer.java | 3510 | `76762442d40f34300dbbfd7c4208507f05d38868bb1c7ea97c2d33807de8b46a` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/BlockExceptionMatcher.java | 9123 | `8d4815930fea2c46ec8162be2e053cb5c4b57e973b831570507d33902206dbb5` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/BonsaiReferenceTestUpdateAccumulator.java | 3698 | `5f1c8714b8dd0c3925803904b182d99568bfb3db4c7803da83316c287071a2e5` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/BonsaiReferenceTestWorldState.java | 13472 | `78c05eeea317bef1cdba56f16c61e25fca052e005ff287c636ad8f8f29bcc2b8` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/BonsaiReferenceTestWorldStateStorage.java | 4061 | `2e80c6b941d85a2f4c83e538e398ff5448a852857ae36d584cf0b2a707a2113a` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/EnvironmentInformation.java | 6874 | `10af1ab885a2366f7d9843cf914c87aa25a3e1a525fd8b3d7e3895ef9ccc362f` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/FixtureExecutionWitness.java | 1600 | `8cefad915eb5a1ff7121f3b19ef78bf1e5d28cd92269b8f7f8b9e96d3415a015` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/ForestReferenceTestWorldState.java | 3222 | `d6f569ce84a1325cfc50b4a92705d3ca09095be4923af89d18226d5f1b553e49` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/ReferenceTestBlockchain.java | 8528 | `322cb6fd7190e93fbccbc3416c9aecdfe274d9b659f3dd957d3d79a71be453e9` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/ReferenceTestEnv.java | 11647 | `c66718608b332bddbe96fa5803c1027cc81bd5e97ca7d15d42b6c8776bd17117` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/ReferenceTestProtocolSchedules.java | 18819 | `724f71ed369d9d18cba450e6f957b323f471331d33a71ed662f4c75bea938869` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/ReferenceTestStateRootCommitter.java | 1207 | `e4dcdbd098d782d5f7dc833e52a6e2a46042b770d59441a3771bb12187febe42` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/ReferenceTestWorldState.java | 4024 | `90f6ee1ec29a6e207c0547897b14686864a47a30bad58b60a2392e5a2153da9d` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/StateTestAccessListDeserializer.java | 1750 | `4ac8db0eba8508c18303b21a910fdc77e78503b34c2b8f5fc3cd8408064456a1` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/StateTestVersionedTransaction.java | 12395 | `96bfb1e999d3ff331656fc3be6ad387328d2da821040a6af910c1d770d911168` | 0 |
| ethereum/referencetests/src/main/java/org/hyperledger/besu/ethereum/referencetests/TransactionSequence.java | 927 | `7a4d656b3fdf27a50a261643d04519b56bdcca1fa46eacd3ed7a9946afc8efa6` | 0 |
| ethereum/rlp/build.gradle | 2325 | `944505a3beaaaaa0fe3fe28a8755ee106848e32bd883f1dfc9c489f6f2778505` | 0 |
| ethereum/rlp/src/jmh/java/org/hyperledger/besu/ethereum/rlp/RLPBench.java | 2271 | `5ce76c655d5a25ad4658bc4704cabba39ab77fbe1369ef090c1f5bf001039ad7` | 0 |
| ethereum/rlp/src/main/java/org/hyperledger/besu/ethereum/rlp/BytesValueRLPInput.java | 21866 | `d1d62dc613e658cf89601d3bb8e764ff14115196575abbb997d0ad7db10e714e` | 0 |
| ethereum/rlp/src/main/java/org/hyperledger/besu/ethereum/rlp/BytesValueRLPOutput.java | 8407 | `194df5da81ca9b2c26f03321b42511298adc235acc5248a1eee78f3eae4c650c` | 0 |
| ethereum/rlp/src/main/java/org/hyperledger/besu/ethereum/rlp/CorruptedRLPInputException.java | 892 | `9e47151be7e85f1e146792ea9dac8165ef0390c052db84ae3eea3194837c329c` | 0 |
| ethereum/rlp/src/main/java/org/hyperledger/besu/ethereum/rlp/MalformedRLPInputException.java | 943 | `9e5ccf495aba6329f22b51608b83230459c3d9a335ee8498d4b4510bb16fcbce` | 0 |
| ethereum/rlp/src/main/java/org/hyperledger/besu/ethereum/rlp/RLP.java | 8599 | `67cbadb4c786661adbc5441b902a600263b67b869b2f433c8d1ddbfdeec0dd3c` | 0 |
| ethereum/rlp/src/main/java/org/hyperledger/besu/ethereum/rlp/RLPDecodingHelpers.java | 7122 | `a161349ce99dc3d7bab7fd0859cff673f6702d6f352458ee38f919d22e044d64` | 0 |
| ethereum/rlp/src/main/java/org/hyperledger/besu/ethereum/rlp/RLPEncodingHelpers.java | 3478 | `809d0aa540a888ae9068b4e41ad64621ca0aefe52d010c3da63d638c4af866be` | 0 |
| ethereum/rlp/src/main/java/org/hyperledger/besu/ethereum/rlp/RLPException.java | 950 | `4b93219dcec398fcd1251a9ca772803508dd6317425d8034b3c38bdfd7aec6ac` | 0 |
| ethereum/rlp/src/main/java/org/hyperledger/besu/ethereum/rlp/RLPInput.java | 17641 | `834add0d178476e86ef6bebcfe7d8cb5ee50265b1a7431b6fe11a39f9e26a6ca` | 0 |
| ethereum/rlp/src/main/java/org/hyperledger/besu/ethereum/rlp/RLPOutput.java | 10137 | `7133418347026f15c07b07ad3108f7ceafdec2abe24107dc30dc42dc49245924` | 0 |
| ethereum/rlp/src/main/java/org/hyperledger/besu/ethereum/rlp/SimpleNoCopyRlpEncoder.java | 3778 | `bf252b9bf2afad729d84a12fb70abe0470bae2276bcb011dab83e64185ba867d` | 0 |
| ethereum/rlp/src/main/java/org/hyperledger/besu/ethereum/rlp/package-info.java | 1374 | `0ef135e10ab21f648b2f6c76aeff21a2f02a47d23f0278c01c52be414631c874` | 0 |
| ethereum/stratum/build.gradle | 2080 | `7827e93acd177021565b85381312d3f1f7f71a34080dccbb81798deaa0468a73` | 0 |
| ethereum/trie/build.gradle | 1902 | `01067adc7468f0412207b1f38f2c6ac22b0ca0c0d2646388844efa09dc7f819f` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/AllNodesVisitor.java | 1715 | `30c0a7fc8d137d839392e24db92eea3bd8539f6a4dca554079fa22f2a0cfa7b7` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/CommitVisitor.java | 2398 | `da3aa28558a2a5ba72936c96a9b394e283b2ba72db1f6eb2a5a6c1769b11b8fd` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/CompactEncoding.java | 5472 | `bc426e38f4b1bf459c0fe996127c4177e877ffee1b76d41001e97d3e04c8112a` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/InnerNodeDiscoveryManager.java | 5492 | `e3465afa21982d4108259ee242730b416664d3d371b57ac4f066ff0e4c8566ab` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/KeyValueMerkleStorage.java | 2152 | `e91658754e1cbbb60fbb88b1b103113ffc4e8f132b31244564a9759629363914` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/LocationNodeVisitor.java | 1186 | `e9ec097df310e1aad93dcab8db2d7667097cbc6c2ae2957d96378842b4ae8bed` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/MerkleStorage.java | 1938 | `7a8ee0fdcbffdd3f3f9e39aa41e9c65ffb6e29d1bea2e065cb21c95fd264b636` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/MerkleTrie.java | 5391 | `07b8f516508f015f0bc05eb25d0d18c1045369f51a03a2e26151dfd0a5a02e19` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/MerkleTrieException.java | 1954 | `8ff1a66180f3baee4149867e908c17c91c8dc24a8f787d9d5746d5170277d0b1` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/MissingNode.java | 1441 | `2d8feeefd4ea3eeefa8aef400878e9751f93fd0679925931807efe9249971d8e` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/NoOpMerkleTrie.java | 3169 | `17b8f9afb998040b862163801a454a3b403223b40643ac8b81b15d5da36a0298` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/Node.java | 2328 | `dc40ece33fdfb8833bc1c0bcdfa92b5463b6487a5c8b391244f3a7e001ddda62` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/NodeFactory.java | 1271 | `836494448839772cef62c1692be6ff1ef6287e3d959cc1322ebf6383d49d3d0c` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/NodeLoader.java | 862 | `0e28cfd99c9f2e023e059d1f1ae575b98381292b4657d95f1e6a6f899da20d31` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/NodeUpdater.java | 835 | `80542d1c6bce84c9a196b6f43eed63fd2b9c24d84f3a3eb548c4d8079797a7e1` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/NodeVisitor.java | 1075 | `87a00bb04470bc5cd58c438b31ab89b71a3fa2ed98fd022805f4a4ed23c5671a` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/NullNode.java | 2405 | `40b776582054304a6d180fe6055b03363793bf058b99752143f799aa8bb607d7` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/PathNodeVisitor.java | 1178 | `58faf7f0000cbee0a5e4195ac7cd3177e5c02b19f708acb48b278f7b9ad1f57a` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/PersistVisitor.java | 2630 | `6293b57669f8d1b0f5b389a2c40a553e8fdbd0ca29008a2b47ec39449f6fd013` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/Proof.java | 1160 | `d620577367a53a90d13d430c01bc84b29500d5e60d62be46e951cba076d0f838` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/ProofVisitor.java | 2128 | `fefdf78fe8cab1cf5b10abad037e856e2e077bb3682da4c742ea000d052312f0` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/RangeManager.java | 11371 | `9dc2904104ae6329ce8696b994fdb8d05bfa16fe1189bd60770ab62e666b5de9` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/RangeStorageEntriesCollector.java | 3017 | `7b05182f129149fac9d26ecb321a4bb2c67eeede5f3dc831e438033d31b1b4d5` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/RestoreVisitor.java | 7994 | `1de22e5d5e034a52b4d84313859e524513d20e122ed604116ade811f32bee7fc` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/SimpleMerkleTrie.java | 5460 | `aa15eb34669c226dbe599ef9d79c3a81337d8d6f65b4851b8c2a957a70407271` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/SnapCommitVisitor.java | 5911 | `1e5d2e0077190315c27c1b6f98a59ea1e5840fa1f76c669716fa067eece8558c` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/StorageEntriesCollector.java | 1997 | `792a3451cf3b39879fdeb725f68feffc1da8b2a25870a0b43aaade7c4acbddae` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/StoredMerkleTrie.java | 7089 | `3d6e5eea40e7080e8f79bde4a6d80bcf6d551ca6c0d375dbe5f86450e56a378c` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/StoredNode.java | 3957 | `1cdcca7f13075d833eb4fa2b0bed5866adada7758bba6a4060cec4c4bf1e7fa5` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/TrieBytes.java | 1962 | `470669bda922ca0488e8a4554e3ba82dd25c75a5d245e16b2cb620e3463de1d4` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/TrieIterator.java | 4001 | `6da09de72d40a79c3b41b86493d0b95e162617def386a45bf18e41ddf78618cf` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/AscendingCollapsePatriciaTrie.java | 13805 | `91677258b5ebcf2f4618b04717124b23920f2969eedb072e4fc125f8a51838bb` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/AscendingCollapsePutVisitor.java | 6335 | `da4cb4437f62563b8c0e07f9d7c1a0bb250a2f87c9ccc9e71f77564d66d81fd7` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/BranchNode.java | 8956 | `c5e2723de33920c49efe04e62c1eadc1ab2e9843fbce3e6aeafbe4ca92d066c2` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/DefaultNodeFactory.java | 2680 | `6ff2d5795e208d157100226d29f084ee2f34f949c8d9487e96e3b96986a44ada` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/DeferredPutVisitor.java | 6217 | `fa456864f88d41e0865bc55eae5b404e96686860558812ecbed8e5c778baa33a` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/ExtensionNode.java | 5496 | `a0eb8dba7fac26756254d4cbce2bdaba1a1c77d5c1acaf4367c90888bb9a1188` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/GetVisitor.java | 2418 | `f3b292ef1bc940d17b570b562ebdb30d9da65afadf5287f06f26fc6106ed7688` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/LeafNode.java | 4844 | `9347b7a9ec04c04a7746887162c4322d40e90800de49d57cedf9557fbede6d5e` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/ParallelStoredMerklePatriciaTrie.java | 30109 | `e327c18004c6a50085814f3af2b50c605b22643f2b985eb3e014ea6ed9ddd51e` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/PutVisitor.java | 7108 | `a061b542c1f2c4bb93e3b9ee358749ac5dc7a8c987ebf3d52627b2be410a94b8` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/RemoveVisitor.java | 2817 | `53ead2648bb1ae5c6a95a630e93afcef266c205a060884d97b8a9b7516864f46` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/SimpleMerklePatriciaTrie.java | 1713 | `d0b06f8eda11c4b626aa0c43c700851886d850bbb748d4041340732a592b38d9` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/StoredMerklePatriciaTrie.java | 3086 | `f2bdb67d964bf06a9c4da0e7366e93a229f94dc1d612c1bd25188d7834b20457` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/StoredNodeFactory.java | 9480 | `613ff21b7ed9e6d1f899b6518d542dd050555d99cb7891c94c5f2dbb986c51d0` | 0 |
| ethereum/trie/src/main/java/org/hyperledger/besu/ethereum/trie/patricia/TrieNodeDecoder.java | 6307 | `9763e0a074d30aee1095baccf8c7ab8d8000286826bc01ed97f0ae818b94c424` | 0 |
| evm/build.gradle | 2672 | `f91eaf125c5faf88a010c350021a788c35770ae0f2684c10608bedb74295ed2b` | 0 |
| evm/src/main/java/org/hyperledger/besu/collections/undo/UndoList.java | 7962 | `c92b069bbcaf68f7e03a0d08edb2fe8a3220dd7bfe850b58fe45b8267cca078e` | 0 |
| evm/src/main/java/org/hyperledger/besu/collections/undo/UndoMap.java | 4385 | `5e7aef547de5f292b2bc126008db868cf2cfd1ceefa6836b5f37165f2533f88c` | 0 |
| evm/src/main/java/org/hyperledger/besu/collections/undo/UndoNavigableMap.java | 5150 | `b2941952c996a43b44e5736deaad5b7c1e6bb20f7c6971394f7fad2e282f9b62` | 0 |
| evm/src/main/java/org/hyperledger/besu/collections/undo/UndoScalar.java | 3003 | `94e55cb5d26a066cc7d75caaa738824e0ff4ff3c380421eafd06a6a93e6ab80c` | 0 |
| evm/src/main/java/org/hyperledger/besu/collections/undo/UndoSet.java | 5085 | `b527c2695e0bd44e62def3772ac7c49f1ffe07ea15d755fd0d25018e2d74524c` | 0 |
| evm/src/main/java/org/hyperledger/besu/collections/undo/UndoTable.java | 5943 | `f6961ef3e026660c5394eb69c5e926f08cb2b80e1454aca4164961039587154d` | 0 |
| evm/src/main/java/org/hyperledger/besu/collections/undo/Undoable.java | 2937 | `fae568603e27e6424885f607c4d39a1fa66348aad985f9f283660728117d1922` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/Code.java | 14602 | `ef1226e8595fc4dcdf18aa36ec6e5e007cf143f7ae43aa3db1560bc817c53f7d` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/EVM.java | 31090 | `4b46de2268fc4a15ffc2dc20a2fcc8cc5ba50adc6d3335fe902e73ac7854a0ed` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/EvmSpecVersion.java | 7829 | `7dc31a76f81c60e2e65ea671962e6f31abbc6992f3a212ab3bfc7463ad9bd693` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/MainnetEVMs.java | 51423 | `9d518662cb226406ad258a81f532bca2eb8cdb8d98ca6aef7948bd371053be66` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/ModificationNotAllowedException.java | 937 | `7b3f746cb743a4793689fc8d05ac59697f33142a186ae22dc6fba225364af2e9` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/UInt256.java | 81460 | `bc73380c498e217822da6ac28deb227c50f551e9350af59131c4a3043553d84b` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/account/Account.java | 1627 | `2bd5500fe897348695baa917cae4d6ac412e70efd09cd91ce359ce935664156c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/account/AccountState.java | 5300 | `8ace8d2a756e16ad7dafdaeb8a78a2a5db4b2cde5724298b5ed8a19428c3627f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/account/AccountStorageEntry.java | 3708 | `73659bd1d93c5781decbb1827c2db1412a9e9f814a445529be3fb4448329cbb1` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/account/MutableAccount.java | 3849 | `425178d3be3292292753b3fc9af684740393abb013789aaf136c4aa1b79669e4` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/blockhash/BlockHashLookup.java | 2650 | `e471dc0c8fb5d1c795b6b75043be69df0c416d86bcc53498ead237507bc3774f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/code/OpcodeInfo.java | 14883 | `29b7f177c8ea4c3863683bcf259ab0a2e4d84620b4424b32b5271fb5c0c5aea8` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/code/WorkList.java | 2638 | `21f09922e35026558492797b043e4cd6f8213b072792ea51d608ff9bfde1faf6` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/contractvalidation/ContractValidationRule.java | 1358 | `67aad05d00495d415af056e596e120a16f93188ba5e8daf42de031cfb260d59c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/contractvalidation/MaxCodeSizeRule.java | 3139 | `29779869b757be2ecfee9e2581161a666db0d096b22dda64e8db035cb554a1e3` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/contractvalidation/PrefixCodeRule.java | 1992 | `fcfa6521b32ab7a148765c9f64632ca56877c5467626146126a7621119656e50` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/fluent/EVMExecutor.java | 16028 | `cd59e3a65ca390313efc1d2c24454633abb6c9ff2d66ae9223675a759a5aeaf9` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/fluent/SimpleAccount.java | 5220 | `e3b9ac23dd1139e2d2aba7929a83504cd8f153f59a664358ee866581089c981d` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/fluent/SimpleBlockValues.java | 2918 | `4931b3e8413dd9e644a98786ed9b4066b240bae4adea7d6c417c769d5c5250ef` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/fluent/SimpleWorld.java | 4074 | `f61167af16c34b37a52659b3cd0be1d5033605264653ad4d094fd194f3b19c9d` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/frame/BlockValues.java | 2121 | `3c01e3c66f7c40405722b22d88539ab526b344abd7882ef9730379169a3017a7` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/frame/Eip7928AccessList.java | 1882 | `32163c8bbdca608d055de9b66efc6ea3b015f8fd00f2bc49c19e146d9f7bb5f2` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/frame/ExceptionalHaltReason.java | 4870 | `480c89b4595cb7b3b0bdb244c15bc31973a3f9ccee69c5da24b9065ca45c22e1` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/frame/Memory.java | 17630 | `cdca200dfbc653189a0c9cc81e561c3806b6cbaadea16470520d6426b01c2af2` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/frame/MessageFrame.java | 64023 | `90f9eb3d22f1deeb3c01d544f2f90fbdc71ac9f53fe07365eaa0081c9ae3b0ea` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/frame/SoftFailureReason.java | 1553 | `3c3105249c2c5cef8333db47054aa031d287ae735b08526635590ae9259f7770` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/frame/StacksV2.java | 2396 | `2af20459b0a6b1ee26c933d380c27f50b7b6e76fb08594a6442037b70fecc0a4` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/frame/TxValues.java | 9350 | `c3bd94354a9d3d07da48d784d3142cc0744c771d38c9fbdf9209510fb7c5e914` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/AmsterdamGasCalculator.java | 20007 | `43ddcf79ffbe4585cfdba842fb41406078568677568520e1e606184483b595c3` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/BerlinGasCalculator.java | 9326 | `06724d6651e160b7c12c50cf115a078447fb42ff40a7578d78401d7a4d218924` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/ByzantiumGasCalculator.java | 3545 | `0ce62d378ee22a826cbde6e288f5074d1c6a35a9d5c9fe5bc2a88393755d51f9` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/CancunGasCalculator.java | 2021 | `08d4664783d39dbe1495450d9fbc74af9001e1311f0de8f1d1f2d6fd5ca41bf8` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/ConstantinopleGasCalculator.java | 3734 | `135e7e1d730a9e305aae403458285d396aa9837732f260c92c245af077871ac4` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/DieHardGasCalculator.java | 1013 | `8936591973b66883dd920dd690da769d9d4957c44e56f884713e23bea643a008` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/Eip8037StateGasCostCalculator.java | 3572 | `87238a85a7e761c0d1c392332191a3ded6e962a230d520950b6f612484789c7e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/FrontierGasCalculator.java | 17681 | `bee25117b6c12c166422b1df94b6884688587acfacf198f53093dcc71e386612` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/GasCalculator.java | 25429 | `aa1e340f1b4c05531bb32deb077a9581dea72e314a3ded029272e7d59f2226c4` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/HomesteadGasCalculator.java | 1008 | `e3b0c2224b83919d7c86991fc37457d020d535bc5ed91336e7edbf9bb1816f37` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/IstanbulGasCalculator.java | 4267 | `710f11cb9aef488282abc16154541c927aa2344099715d2fdc43b43343c445b4` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/LondonGasCalculator.java | 3007 | `bda7a775aaf7ae7ec479668dd561415e9cb925bb698ebc9692d1b2e4ef1c9f64` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/OsakaGasCalculator.java | 5224 | `a85b0a36b04df1056a50c25f29d0b2a5de91c2269cb99d7a145b7849e8b095dd` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/PetersburgGasCalculator.java | 2387 | `373193ab6a0b4a38241a06fe6851376d690cda8df98e192fde65fee0cb568323` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/PragueGasCalculator.java | 4705 | `45a687a842ab2bc0b46245ea692c37a9c5ae3fec5220b03c088873a2de9854fb` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/ShanghaiGasCalculator.java | 1486 | `b2cb2892cb2b6c30eae77377a7aa76c86030d59931e8a46b0b7b6fb8c286f309` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/SpuriousDragonGasCalculator.java | 3308 | `ff7d0ca325ee80c3b9b273e4c5ff09ed2cea9068a20a31d8c1dc33ea1da47101` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/StateGasCostCalculator.java | 4966 | `fac76e06b9c77de7090d404238d211b0d9b6dc24712625ed9b7fd0f930e9ab2d` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/StorageTransition.java | 2518 | `7824d7f8e42da37cc8fd10e05787d083e7281f0137396f64a89e59a029315788` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/gascalculator/TangerineWhistleGasCalculator.java | 4939 | `8a002dbc9c4d547b55b92a89f2d216ccf3772aaa93f00742541a99b7c116cf35` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/internal/AddressStorageSlotKey.java | 4514 | `fa1d00eb576ffe1cf613c4a48581bf1ccc4dac653ad73fbe6a3a2af0aba6df47` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/internal/CodeCache.java | 1513 | `28d94f128134955f816dace4c6c0a67b9a9d86e9e82812cf09c29cc6584698d0` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/internal/EvmConfiguration.java | 4829 | `2fbea44e76b3128c3fc3b34b0b90929b108fa162e32c2bfeca73538d35d414c7` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/internal/FixedStack.java | 5661 | `21fba0b70c05515ea514218049dd87db1f1cc4cba05a22223a240c880d84d1eb` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/internal/FlexStack.java | 7981 | `398c8fdd2208f7770fc2b661831d197c0dd24582f14411f826ce10d6fb7d0ce9` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/internal/JumpDestOnlyCodeCache.java | 2505 | `055e2f0e4f072d2317e18c6b3bfb81a8ca4fe0c5850fe721e660432c427f6642` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/internal/MemoryEntry.java | 1284 | `03a8da60520d59563e12baed106c8d914333d1c92bd00ad8b47bed3b2acb09ba` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/internal/OperandStack.java | 975 | `e9fbebce6c5486815d836ca5b8c1ddce80be7d7560f14279c4192949531fe913` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/internal/OverflowException.java | 1427 | `db2ee7133d70977c83adcaba26ba4a6d348960ebb12865e97c7aa5a4a74efb57` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/internal/StorageEntry.java | 1345 | `ecc20b817af0536a200100ffc880dc370406e50807a8ebc1c5aa8ab2a8b41762` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/internal/UnderflowException.java | 1429 | `371e7a3a1b2a23af4e27effff8b01d8ee7a91406c317b051a42fca88f9d77fe5` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/internal/Words.java | 8869 | `b0c5e37f2cf8661e0403d6506d151beefeba221a2196f2302da5824789dcb851` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/log/EIP7708TransferLogEmitter.java | 6164 | `97c04097da839188abd7b6ed2e4d59afb0d5d838ccf380d1955d9f7922d8e07b` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/log/TransferLogEmitter.java | 3146 | `6c9f85d5909c81a73abdfbfb456c73ac9825f43f0c09d614a349b8b42d086258` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/AbstractCallOperation.java | 16882 | `4920a8a41e8e7bb8308c2d9ac2a63457c2be216af965a2f8c245076105a19285` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/AbstractCreateOperation.java | 12428 | `fbcb1e09957d97618831bd07b4656ad9794129f3458c3a9263027d38443f8c94` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/AbstractFixedCostOperation.java | 3249 | `05903b8be61d3b753f15845db1ff127379b1edbcefc7fbc304d0d9b2efc17737` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/AbstractOperation.java | 6087 | `10765f6fab38ddac846bd7cab7555d593d416544344a94e5e7d3509a07deae9d` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/AddModOperation.java | 2533 | `6f13a34e641726ec816b35b4b8042a9d0263206bd5a0f9aff468be45dd573dca` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/AddModOperationOptimized.java | 2127 | `7ee3b21e76acc9ba614a2be8f7a8dc9c5376176b771e0bbb64a83eb5bb73631a` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/AddOperation.java | 2148 | `e95fb8f9c7697f4d108b575591f4c842f37bba660f878dfe577e7093aa47e895` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/AddOperationOptimized.java | 1964 | `35a873c420254c78ad5bf4884b3b26e47540abb1a2d2fee6b276e26b7dfd469c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/AddressOperation.java | 1357 | `5e1102612a1fd504592b42e4b26c2b6e9322b882c147e1af4bdcf84ca7aba3f8` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/AndOperation.java | 1822 | `b323549886e62036eefecfbd19d4707667e8f71accbcb85154b843c4f0527a80` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/AndOperationOptimized.java | 2041 | `ebe4ef3f493fa81ee9ddbeea09c264786718d1c224f6e8dac6a37b7aeabbcd62` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/BalanceOperation.java | 2953 | `3bf12ebd11a1bb984af438a7cd370051f056c19b00132c815d66191b3eaa29e0` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/BaseFeeOperation.java | 1688 | `21d71fe7c35e064f90b430a48f00f58c46783cdf0eb6743fde6b0949913b3e18` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/BlobBaseFeeOperation.java | 1452 | `32fef1729d6a1d309f405af4c4275e8f270c5dc224fc1ccb702ccef927e98e61` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/BlobHashOperation.java | 2619 | `25d3da3a3748020c690090d2fb59e14ea7eda33c8bc3cf5d85fbc154328f1242` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/BlockHashOperation.java | 2969 | `6adce71ce526b0e7288413a81c6ec63a5ca4d5495e6aeafb9029c797b57ad708` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ByteOperation.java | 2335 | `7876bd6f03d4121067394a940c8e76de8f370bd423ad9a636c84559f6f372b62` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/CallCodeOperation.java | 2576 | `75ddf881b8a8f39d9dabd6cf68ab45b9979bdf2b0ecd17e50e1c89b63edce640` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/CallDataCopyOperation.java | 2182 | `55ad4f1dbb62551cbdbf1ae4536499dafa5c2c4c6a364fc6c874ec91251d1441` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/CallDataLoadOperation.java | 2259 | `6f38ca69748b3079b7edc5f34586ed14481807ad8bb86e8d8856f37ec69d3312` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/CallDataSizeOperation.java | 1515 | `d07017f91ed40e8b4f2506fc1791274bc2a4e50c8af198c487a5372ea0dc4266` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/CallOperation.java | 2921 | `30ee1bfc0404266191b13b26787952bf6f7ebe45e7b81fc9276dd4e0d2a25bb2` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/CallValueOperation.java | 1437 | `f92bf7f26ee10a0ce7e28b4736c2fc3b514e1d6275efa90a5ec6166b34c83a58` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/CallerOperation.java | 1349 | `2fa57df8d80dcd845c90863d45e8d260b66c8452bd70f6320aaa25ed22ea557c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ChainIdOperation.java | 1749 | `6e7e5eb24f133f53af0ae75591716ab93a74140c6fdff573d00bb71b8789b35f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/CodeCopyOperation.java | 2000 | `e375e6ecdae7ee56c115af4012126a8b66bb55d651b21e070cc61d88c9e5177d` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/CodeSizeOperation.java | 1481 | `290f916ddc0145958a074a750a2892b93b1d20d48f5448e1e958d3d18871b93e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/CoinbaseOperation.java | 1429 | `beecc69b3f16f1ba93c1aae7ef2528bd2130ef1336bf1db04b164cf051572945` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/CountLeadingZerosOperation.java | 2145 | `5252236fbc15198dab18b162086353cb3dcf2dd25e9e48a1024e6ef6d342c19b` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/Create2Operation.java | 3069 | `5bf5a1c6c9ab3574dff6b5bada20246bae0ff338b709aefa4e6b977ce2dab95f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/CreateOperation.java | 2822 | `2e3761b6c19296d65932cf268133d7be07a8ade81b79f14687706929b82fceaa` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/DelegateCallOperation.java | 2614 | `54aa37ffa122f6ad52e04d07d3eec8aacc9f303bb9903fb1f3878edcbc548f30` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/DifficultyOperation.java | 1376 | `2202b616121a8d1ef219ce7364e3a6050aa5b5610d3ad2667db0440172bd891d` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/DivOperation.java | 2408 | `5f97c8575da5b06050f5934efa5803ced2bf30178cfe5174c5624d77c4ae3260` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/DivOperationOptimized.java | 2080 | `27f9e2e3b8a50164a6ef318d30c8effd9db4e58759a58c500a67b6576cdd3ad1` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/DupNOperation.java | 4040 | `3fccdf53576c6b7cf77263410105b126740ae5a2029184b6774e5051c3031d0b` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/DupOperation.java | 2237 | `eb0abe53de4eb69f7c216c3645266a6cca3f05f816c6475d6746ebd266dd6f5c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/Eip8024Decoder.java | 6392 | `63193d9396e93abfa515df1880dcbc7832077673fd49ebe82f09bda944adb584` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/EqOperation.java | 2320 | `436aae5a734baf765552d6185afac5dd604e839774acfeff851c374ba6fe1d3f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ExchangeOperation.java | 4122 | `7519c2c4341744044d757e88726c8d5089d43fb4d8700fe9786717331da9b889` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ExpOperation.java | 2706 | `a38f8dececbfc6f54133345da1a8df73c64459f8d5d8534057a4f6ce43b7d671` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ExtCodeCopyOperation.java | 3048 | `25b0c003edb348539e2817391fe496379da525bc8fd6248f84d4488a7c891c9e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ExtCodeHashOperation.java | 2926 | `f5bc9b101076217b972ada7fd2a16c775da27529d26050ef9a8c4e4d8299ee7a` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ExtCodeSizeOperation.java | 2909 | `7a4de890b7c1040344f882a79b3726aac646acdc40475c38c5c6903ae2e8d2b0` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/GasLimitOperation.java | 1407 | `cd770b0fbdd3c0a6929e93a6931181d950827c029e4ed303a190829007d683bb` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/GasOperation.java | 1491 | `67af5dc07f3ea76ecfbe83393de4b7a7c5b03b2d85e989a70c8434dcbe211d84` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/GasPriceOperation.java | 1413 | `75b754abb12631c1adb2717b5840167add473cfa8e323a232ae6ad7d4d6a45d8` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/GtOperation.java | 1872 | `86739015b0be0c95c5927a8632b966539a4553286ad4fdbac7bb7a26eb1412f6` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/InvalidOperation.java | 2221 | `d191a7e5377009876cda0b6ad736d5f792a3ed1a052023ad00b0274c289e7ea2` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/IsZeroOperation.java | 1800 | `7c049ddbacfdc7ad3d16cc4c367b9e7ca915527f18ea70c24d19f7a020d355e8` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/JumpDestOperation.java | 1496 | `b3a24fb5c7edf59917366628dc5f448152d18016c4681f58a0549ee2815f30f2` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/JumpOperation.java | 1979 | `5c0e875badf9e52e386c57cd211b8e5b1b5750345d6584eadded7784ae141db0` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/JumpService.java | 2005 | `1d5a862e1b7728f66b852885652c8d9afc09843d6329de0a7c8534fe99a6c269` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/JumpiOperation.java | 2348 | `09c76f7c3e6e0239b4a224d85182989beb2316742a11adc6b529ebf6f5ec22bf` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/Keccak256Operation.java | 1946 | `58858f129416e76cf732bf6bd6b7b93adb060285ac480bb31bc2181e1c2c54aa` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/LogOperation.java | 2701 | `bd0f41a9ac129b66ae7dc9bb4d8173c29a48049e348ab5008094221e4b7d4b69` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/LtOperation.java | 1870 | `3f1e77d6d8ab50cc8dd93148911d1e7d84acf9e841df053b7ef591f7cd6159d4` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/MCopyOperation.java | 1872 | `47148f8781527b340f6cbf0fd3637789d3403b6dfeee2a3c20d5e7d26a472d5c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/MLoadOperation.java | 1808 | `e8d9991bf68c61a59982acb7fc72c9baf98bec7a49136a61c92f283a86a27a06` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/MSizeOperation.java | 1378 | `dcc1691d90dd95d178ff25a03d514cf1ecc40d2a632cb009926ec3ce77d7a12b` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/MStore8Operation.java | 1884 | `4108c1aadd1d6be73160a3ac49c20f2ececa258b729cdb928db48deec146b7fa` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/MStoreOperation.java | 1813 | `13fcd0239bc4ddd3d4887548249f49ea73af14ea3f7b90a6ae6e161a5d0fc374` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ModOperation.java | 2441 | `ef2abbdf320c53a41627443123da83f3890a6005c5c8ecc6645f32ee19cda475` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ModOperationOptimized.java | 1976 | `3cfb5db14705e115eb078796cdb843aa924953fcb6d8b071ca08ebd47e9971de` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/MulModOperation.java | 2547 | `304c0d537d13654fa47b95f2ba787f0ff58782b8921a56a2cab0a218486c81bb` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/MulModOperationOptimized.java | 2118 | `5361fea357e314b28cf45a46ccb2405e4fffb4cd3ee187a9903138a22d9c958a` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/MulOperation.java | 2040 | `d5a44dc11f6bef835b268f3ee5317f9c7230913ac266988cb8fe1e34e1f90326` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/MulOperationOptimized.java | 2010 | `7894ab5fb74fee0f81e8581395495694383e0fd8a3c8a2cba85418395eab2b99` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/NotOperation.java | 1807 | `bc2dc1d05c7bdd128baeab8df07824f2fbe8ef45454fcd0d6a054436eab72b67` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/NotOperationOptimized.java | 1929 | `314aaf2f86c9d6358bd2f16a3b895e7f567910c6bed5927d8636809bfba39886` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/NumberOperation.java | 1425 | `a3192163e457ff8b46bc13bd0e783e3dd8d01c0e53be4968f8704e8a8cef9005` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/Operation.java | 6165 | `46dc60a083df7a9f14ec71f692511ca410cb1e6898dfb5839a151c21ff46a78b` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/OperationRegistry.java | 2018 | `1b0003bb0ad757a847c43c4168702e5cd047393f4f666e9ad0f94d8c34a9e1ca` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/OrOperation.java | 1795 | `16d387adc17738dab669d6bd128cef2a4a2316d316d1038c4c158b81f28602d9` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/OrOperationOptimized.java | 2029 | `5b8417336b31764d742755320eee67cdcfeec26738183634ebc0bb51b0eeca5e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/OriginOperation.java | 1333 | `b202c2f7e29ca7094184a8aea4d129833f578e1fb0e818f3ff4722d57782bbbb` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/PCOperation.java | 1351 | `3e833302a39e91d44506e6192564c6477a8c2166819e1a7939f97f258661c006` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/PayOperation.java | 4276 | `2ff1a6d0b98a1d9237a5479d4dc1052a19b33e3191d01d0f1af3ba36199b9754` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/PopOperation.java | 1614 | `c3a7ddf59aba9402913aa8f667a1332b57f6b14210ff78db3a2ade8eeb855a7a` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/PrevRanDaoOperation.java | 1372 | `800f9b4bec3fb46abd8f58bbb483964fe86d7ef81d36dd76ec6a1827e4a85cc7` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/Push0Operation.java | 1774 | `919f0525b67957243e0866635a3f555430e3a0badfa9b11c78340e865e2991dd` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/PushOperation.java | 2866 | `8465d65ce84d22ba61b7b52618750cab85835cc49cc8a0420198da861a81b23a` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ReturnDataCopyOperation.java | 2704 | `443d580f6636f57d7980c2a4b2090b4ab9c4796597423eacc37ab20109b25832` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ReturnDataSizeOperation.java | 1511 | `258730cca695df92ac3c26ade2456bbbb127314aa34e85b117ce60e4e620fb7e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ReturnOperation.java | 1909 | `161b76b07bef25ecba74d23e7cdbbaf6540241885a6758bac8c6adb374dfa3fc` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/RevertOperation.java | 2010 | `55e4965f7bb3386da072fdaeb2248b02f3d9e2557dec5b1b9d52771e005a242c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SDivOperation.java | 2515 | `606c6d67931840bc96063581b92686cfe85f6f3b24880e615389c4f9bc8646e1` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SDivOperationOptimized.java | 2075 | `39dc20068ec49d27becc6984ac5665b2392560e4c16e1ac14d6742905de57b02` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SGtOperation.java | 2190 | `65feb482eb759c4d4b8b28e9a69273d047a5e7ba6f62bce0ebf31851e639451e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SLoadOperation.java | 2936 | `1aa47963c11d81ebd8ce91e33847f280f8fcbf3cda01c33310c5cbc4c4f3c3f5` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SLtOperation.java | 2190 | `62cbfbb348fdc50038f79452f4595a8e504cf9cc203c9ce7dcfb359ed1e143a7` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SModOperation.java | 2699 | `cc10e08870c254bd5ef6b82d05e1e71e8e7a0ed139b6b46d46087dc4d340efe6` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SModOperationOptimized.java | 1990 | `1d254d2e075b103796d50dd2bc29afd23a006cfc644ca55ded1a8fe9c39c5324` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SStoreOperation.java | 6550 | `8c28e90c901d5c7fcbf75801eb0e81e1e4030925bb398c66f6d55e1483d47130` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SarOperation.java | 2733 | `8f0f3aa463bdd1f6b0ba221c279b144a1ba519b95c6d9c874dc9497aa257872e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SarOperationOptimized.java | 4998 | `d7bf2adda20b39528d94e397d037bd1c1e32c20063a27083a403f689427cf5a2` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SelfBalanceOperation.java | 1634 | `2a4d84071b246128412df8350068b041db680495f495c6ee0d37d6f4b9a1351b` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SelfDestructOperation.java | 7140 | `8a917238e28e7d8643081543e52432765579572788e64b02698da06e311189bd` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/Shift256Operations.java | 3436 | `13beea0904a92c677109dffda00a50fa58d764edb784a638c524c2cbdd13dbca` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ShlOperation.java | 2230 | `ae67c180170947e6c51305c8a4f02309b640e6578a5d7e27e336a981bf01fab3` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ShlOperationOptimized.java | 5064 | `7f61ed8cd0c85466f67ebb606f5ac409d4755220e2518a850ad3c622be679abc` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ShrOperation.java | 2225 | `d78684d8679c79f10661ad08329d3037c93109c3db356614850241eee399a24e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/ShrOperationOptimized.java | 4555 | `8bc70502f1e55dc595d8e774c343e2c1eabff518eb4c470c9fcf1f0c81ffb485` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SignExtendOperation.java | 2624 | `501223ddabdb4c9ad3484f188745855160686d99ecd51cb82887ec2be51ae190` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SlotNumOperation.java | 1473 | `bd2997e04e828cf52d7c6e827436c949f0caf81a16240645c8cfb61ad864b59c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/StaticCallOperation.java | 2616 | `1d2b8e4b42b3647be213a4824cc95a1589343ceddf978a798747852fd649fa02` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/StopOperation.java | 1805 | `cb1853d13c9085df08ec936eeae6cf980751cca6d1415c3c720a69ca70a5afe3` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SubOperation.java | 2309 | `689407a7abe53ddcfd44154ce259b164acb5190de045db3a15dd4dee1107ea36` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SubOperationOptimized.java | 1979 | `73819fb69be13c574212491d9b579abb570d0fcc7f7ebf903b106fd69c56134d` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SwapNOperation.java | 3904 | `b26745c3f781e02ea0df9cc90fe9b49f1010f81cc557a4924eaaa31aabff75bf` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/SwapOperation.java | 2386 | `3e5d964b35e827734037cfef2118dc48477555068ef3271f1727115dce2b6ece` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/TLoadOperation.java | 1996 | `7bbbfd23099ced31195c8585093f95e61c4c5984d314b0b2bb6a642391f686b3` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/TStoreOperation.java | 1998 | `add8b8b7f546f30cdf1e4aa68fb86474d3d4dd601f03ca37435320680e6f2360` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/TimestampOperation.java | 1449 | `7b8c816fdd58c94e44a5dc70a347e0f97aca0e22c91fc84a757567dfff2b5d59` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/VirtualOperation.java | 1722 | `aceced141a3ba2b2d040ffdcea06a22526537e58c87bf15d2a5604d1e1e7930f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/XorOperation.java | 1805 | `74eae2bd610de45c9cfb03e3acf5ee72781e2bb91709f7c0146f0c0894a943ec` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/operation/XorOperationOptimized.java | 2033 | `5f376c657dbe0e91b216a0911305704abdcd420ac8d29427d17ee5d5009e67bd` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/AbstractAltBnPrecompiledContract.java | 4047 | `bbb8beb6eda99f8446f85f3c5359f41079ed759bf6a0f7172d505d680b14b8ff` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/AbstractBLS12PrecompiledContract.java | 9180 | `f8d39f664a4f42b615f5122b406f78febc1ca1a916e4ec2607f6c39c7e22eb2b` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/AbstractPrecompiledContract.java | 4454 | `301cfc6d0bc19e04a6ed190ab380f744a09be190aadeaf55b7392e28781a929e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/AltBN128AddPrecompiledContract.java | 5211 | `c3d767c05a54cd83c8710f97a163932de652885f51acf33fba37f70d927d6af9` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/AltBN128MulPrecompiledContract.java | 5592 | `59564d5be5767ed71c3175b68ee7c2f3f9b96898dff8ce6f097d26debb9bb6a0` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/AltBN128PairingPrecompiledContract.java | 7723 | `9cce5769ed391d64f569559ba8448379fa6b7e7bf61cd710b3bd8d5d43c8a03b` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/BLAKE2BFPrecompileContract.java | 4473 | `d02d2132fcaff74d48b6fbabe5a5dfff520451802a50f89751149124fa2b9dc6` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/BLS12G1AddPrecompiledContract.java | 1530 | `7f8cb84b82b13f509513b1be09a6b72ff9aa00e7431ed3de592b741b9e968a5a` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/BLS12G1MultiExpPrecompiledContract.java | 1847 | `8a6a9324a752881d77f9ffb6035c92e998715ebe63e91c3b48ed87bb66b3cbb2` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/BLS12G2AddPrecompiledContract.java | 1532 | `a8b344cbe115b18a125c398ce0a0b1535c47072f4e25e8c7e655facbd316cca9` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/BLS12G2MultiExpPrecompiledContract.java | 1854 | `9052e3d4dee360aaa8915c00cdb3ebccb3195cfd340307011c283fcd7985f850` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/BLS12MapFp2ToG2PrecompiledContract.java | 1598 | `278c436a51665faa5fa3aae23344c435d5b64e7f0be75fd3e89829944539cf54` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/BLS12MapFpToG1PrecompiledContract.java | 1591 | `0601989717b647f7053a8db0111a69061c0f252fb159de47c108fb4fe3f844bf` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/BLS12PairingPrecompiledContract.java | 1827 | `03d21386f6a4b9603a3ae66697b8dbca605f90db15f8e8775c12a52ecbbdf604` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/BigIntegerModularExponentiationPrecompiledContract.java | 10186 | `cf5eb9f64fc9479819c73863b9ad46425040d33d1605363ae15135ca5dc711a4` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/ECRECPrecompiledContract.java | 7203 | `9e026cf74101eebdf417f83a790f6d7cdfc35958de958174d19c40439a7b5ef3` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/IDPrecompiledContract.java | 1527 | `8d2a3d1287c90f60ca91e1daf44874bd1b1224df9dd92bd47253cfea3b189963` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/KZGPointEvalPrecompiledContract.java | 11671 | `3d2ce089795acf2d7181d0e6b72360ac1e9904cc12b02cdbc6f99f9ad2490a4a` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/MainnetPrecompiledContracts.java | 8694 | `4957191744a5d5bb5d0ca7f188d9056151edcd7a481425c15eedbdd70dc41a23` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/P256VerifyPrecompiledContract.java | 9601 | `c43e6deed13676a09be3175e89a8a1a2cc076ca761b8087c83cdea04a87ce184` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/PrecompileContractRegistry.java | 1801 | `bf164d11e4bedb8fb772cdc1823391d1912351c40628b7a0643481b3f5de75f0` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/PrecompiledContract.java | 4140 | `24cd0b3373e9d050b093347601195590022fddee9ed22fbf638448127fcc830c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/RIPEMD160PrecompiledContract.java | 1677 | `7604c99a584c5f81d398f55648d7afc0d9a6c31fc50ade33ec6d0378d1ef9cc1` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/precompile/SHA256PrecompiledContract.java | 1598 | `8c458477481520be18aced8e434dab03fbaecd1075052120ba4f910b9d75f3ef` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/processor/AbstractMessageProcessor.java | 10191 | `9725c306a3f5ec49561456ca1a5973a7a2a0c687425e45698a17dc7937cea6fd` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/processor/ContractCreationProcessor.java | 10680 | `70d0f570879ff6300ee2e60f81aefb53fee83522f04d6da450459a160e5e7dd4` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/processor/MessageCallProcessor.java | 8527 | `a3c29e9aab2e78d1f6f402b0e1f3dbba721fd420932fef6ed7d2e0842e22d3c3` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/processor/SimulationMessageCallProcessor.java | 1822 | `50683a27a9332994047a0367c824d1405fe074873bb6f26c3024b056d060de4b` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/tracing/AccessListOperationTracer.java | 2295 | `0f50b03fa9195c8bd5f5d6c76c99c545072bb4014657aaeec266b64cf420f8d5` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/tracing/EthTransferLogOperationTracer.java | 4547 | `0ce55d4def25ab603cae767ea313f37ee5db957a9582601490360cc856148696` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/tracing/OpCodeTracerConfigBuilder.java | 6481 | `49a20cb61291611eb1665f9e46ffb399f23582ea7ff4e47f3ab1e1493064ccb0` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/tracing/OperationTracer.java | 6134 | `76b0c851e59fa0d8c392222df0d586183bbde96ce20f4f636b82e71d46ddd4c4` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/tracing/StreamingOperationTracer.java | 8715 | `624d4c687a90a4c045579ba7b1a68b192d1f85c1f0c097d264a3f57e26fc4922` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/tracing/TraceFrame.java | 27814 | `5f7674ee53ccb2d09236585e0ef56405acbd7963af08cb8a34b757c005644b2e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/tracing/TracedStack.java | 1934 | `a1affb90fcf1f60bfccd33630e6157418e9532bb047e007b5de5d5de373563d2` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/AbstractCallOperationV2.java | 16369 | `84019898c7681785e2ac7a51593c9a7a3eae4d7d3bc8e21d456f8183f7f55eb5` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/AbstractCreateOperationV2.java | 10868 | `bc02917dfa0076fd30cf0a1a0c5643afd91a6c73ca670a23cf6f58be07c9b9cf` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/AbstractFixedCostOperationV2.java | 3119 | `6620413dd6299ba93aaff005ad1df7cf8ce73eedc58bfdf8cacdeb34462aff21` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/AbstractOperationV2.java | 7316 | `00951c1b6548ccf28ff82a802ef81fddd27b650c15295a905706e7a8ef7c3a2c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/AddModOperationV2.java | 2489 | `f194bf90bf5b7a2c84f1e6b38f15213a5b10fe7b4c222a48a45ea39836578e10` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/AddOperationV2.java | 2802 | `885baed82b11e5013c4feb41449c2dcc06d22846425e19e9d0422ad7ff1a8f95` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/AddressOperationV2.java | 1585 | `a968765a2b637a33e18896195670d145dc193e09e901cba8d72b9a5777053ac8` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/AndOperationV2.java | 2568 | `9969b9531ad21282d3b96b5031ec3b4d289d9d92214ae0d2cd65b2f9c37a5145` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/BalanceOperationV2.java | 2981 | `7e401182d76eda12035955cad784a18d759907f9b6188bcb28eb120c05a14743` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/BaseFeeOperationV2.java | 1975 | `83dddc38579018f83bb26f3800ca097e039630e22825fc13591b8e474e94b46f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/BlobBaseFeeOperationV2.java | 1597 | `8303050d7ce8a5db6a5bd719a1a8a42ea648740a3c438b826ef97567ade725b2` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/BlobHashOperationV2.java | 2411 | `63052247258b3526cba38e46235a9d39fcc25629bc4c6e32c8d128cc7def83e8` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/BlockHashOperationV2.java | 2895 | `e750014b68627b3d51056fb54b77bd27b5ec08c2d54ec89703a3612028ec8fae` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/ByteOperationV2.java | 2684 | `913bb76554d37a339887063de72fbffb4b041a32de6704082afd50c8e2969d3f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/CallCodeOperationV2.java | 2953 | `55006b01601866dd3b3cb98770c82364a0174c35af1ba65041ddc97345d904ea` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/CallDataCopyOperationV2.java | 2255 | `57e677d96dcc75f2c4dd9ef35a21edd78fe98b4bd91edce59cf7d42de7d1e534` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/CallDataLoadOperationV2.java | 2446 | `6b004cb42095072231702600a181fabae926c909a0c15fc8d7a874c23fbe75ca` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/CallDataSizeOperationV2.java | 1608 | `b281f724a3c1a7e521994297b72ace798ebf454c56eca0b972923976bd22265f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/CallOperationV2.java | 3484 | `bcfbcf732a50e004c60d2eb763997cdd44974654e38a28ba3c04e486e622245c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/CallValueOperationV2.java | 1649 | `c5ab394bba1d895690bb63f015bbc76da3b926ccf34cfb6f4b2f1e52e2a2a635` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/CallerOperationV2.java | 1577 | `f57d7047f7728ee366b840880067f95c66f6114f3a0ca5a00b97abcfdaeb27b5` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/ChainIdOperationV2.java | 2825 | `4c781cc8c77255182095f83926c112a5e65e7ecf2049b0d051a19c8f1c61b19a` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/CodeCopyOperationV2.java | 2162 | `9bf5e848ae05e28a106147fc1c9d3ca3e921313fda0d1cf39c31e71587673b1e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/CodeSizeOperationV2.java | 1584 | `8aa7afee81eace86aed73d4b6b29b72a95b2fd038c8810d8dc491b595c2dd37e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/CoinbaseOperationV2.java | 1654 | `89adeffce2a77647f6ea4cb4f95704912543b82c8969317b47a14612253c9bbb` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/CountLeadingZerosOperationV2.java | 2736 | `6c335c6f5872591a5518f06cc65c087c09554c2e2afbd140e551379636796a43` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/Create2OperationV2.java | 2599 | `8386840a26fcf17d202b49689856fa4d2f1227973d2d298e97576aa42197f272` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/CreateOperationV2.java | 2214 | `ef4435de3a30102c599e1e2ad9902a72e8620d00b539a96498522b67def70d83` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/DelegateCallOperationV2.java | 2722 | `7b0631483488c3110818cfac1f524748cbecb566658754e5892a38459790530f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/DifficultyOperationV2.java | 1612 | `7c632ebef50c470395eaf73bfc82eda76016fdbf09b6c52cc91ab2e1c31c18d6` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/DivOperationV2.java | 2437 | `7dfd666e2745a4d08a629861c10d9ca8a9e221c8ed106cccb9b2112523ba6cd7` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/DupNOperationV2.java | 3275 | `cdf36c3b7e5002e5dde4f59c6c7e03d643984d538c8f9b1b63860888c5a3be1e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/DupOperationV2.java | 2568 | `5ae73d883ea4839b17589e0c7cd86de21b99e695d63fb2a619e46023718081e4` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/EqOperationV2.java | 2405 | `3a69caed792549ddc604b768a68eb04a64b78bfa71d64ea71950e0899cb3ee34` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/ExchangeOperationV2.java | 3292 | `d6d5ef1e759ecc0910f4dd439415480842a0602b9d528d27b99b66d3db94b7f2` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/ExpOperationV2.java | 3998 | `53673d7caf3751a9356a1fd7ab79a66ba7bdf1242d677d4722c77a9dd7222d38` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/ExtCodeCopyOperationV2.java | 3379 | `85c768cbcbeb2d8612eb2b9156dca5b25bcfeb7326e29dae0925c1dbc10be8fb` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/ExtCodeHashOperationV2.java | 2928 | `235e67e17b06377391e73c365a66f63faac316144e0a3fdf307109df4dfeb1fd` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/ExtCodeSizeOperationV2.java | 2786 | `911fe0f50f18f46ed51c96c5d040a72fb812eb684ae7ae211a321752f7c7efdd` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/GasLimitOperationV2.java | 1658 | `c20aca696eac505467b7bb948788c19376f5b2ecb8f01bcea8f6240a98f60d6f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/GasOperationV2.java | 1565 | `cc74a37855a4c1d6a973f67a80b125d96f9d0c02a93389c86d310c13c71b3b19` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/GasPriceOperationV2.java | 1639 | `7ac223c24af0eba3d64d668561e645bbc7e624ccbd485b1d2db81ae9c9c9d6de` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/GtOperationV2.java | 2338 | `43fe1c365923c60663d87e960949dfdad2ae00cea9ffc52aea10bf1737989dee` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/InvalidOperationV2.java | 1799 | `83e7ced022524d70ab7509b9a45356905abcfa044090e64a5a5de3661e582e96` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/IsZeroOperationV2.java | 2223 | `2cbc128ca052d53ee20b600a9e14f0a907d7be2a5d5c6c49b403df141e020658` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/JumpDestOperationV2.java | 1457 | `f462ff3c09d236edcac166917ec82eecce40d98e0645a3b8a4cf8092ccc9e35c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/JumpOperationV2.java | 3330 | `ed36ecc93207fa29801b6f297b9f12ecb510706e43025690c6c7d89cd5e89f68` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/JumpiOperationV2.java | 2720 | `ae4e99969d347660f00aee8feff38a8fb42616cfa2e84cd4424c4ed701e2af83` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/Keccak256OperationV2.java | 2214 | `0bb87ad772b91f406f5c6a3c0652e8d110960eebd1e269ce667d3ec3d31f68ca` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/LogOperationV2.java | 3214 | `69b9bc6adbacf5979bbfcf92da99d31b57c3c7def774a48e57cd0c8af1e0a5b4` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/LtOperationV2.java | 2332 | `ae36051c2b288fa7a7de507646affbc5a03503ae0918dc380e1726a175f92ba3` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/MCopyOperationV2.java | 2100 | `a83f0e2c9643f0aca7e631f88b7bada4d52115ef6f074721e4dd544e66228854` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/MLoadOperationV2.java | 2009 | `484da008a66de8d9b3d05a008e7f0e13ca4da555b0246487eed3ce54c8bdf8ab` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/MSizeOperationV2.java | 1564 | `7f18dfb0d9a8b15d3161f4ffa84b3889fe5ccf0aa581bf232eb2ba7eb06a1ec8` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/MStore8OperationV2.java | 2087 | `01c61670c5b589dfa35a6531151610cb1aa1ed7e856ae82e4d04ea9964a65146` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/MStoreOperationV2.java | 2082 | `a63d6dc05c0f7b21bd32995a5eb741d6ea2d45a733b1e55d4168abffc7944399` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/ModOperationV2.java | 2447 | `368196bb195fe7512c2232a7bf22d168ceeb9537ca8b3de4c35d263ea0d0206c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/MulModOperationV2.java | 2611 | `29404e6e4ea9142c12fa22c5de8c6d784001e9b2ae7de944b344a5a1666b99c4` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/MulOperationV2.java | 2541 | `256c8216076c9add0196bda332efd42646caccfa34a595e62d0371da2fe32dfd` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/NotOperationV2.java | 2310 | `ee2fb269dde64f44f7efea9e9ed2f3bdda56ef4b0ecba8ce94f4fdc1bcc0780c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/NumberOperationV2.java | 1644 | `6b65d8afedbf89edf4ea788637e602a5838f4ee2aa4bcf4a0b4b2fe00d92b7ff` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/OperationsV2.java | 16824 | `fda2aaff9bb43548e05436f5a56ac1b9f4489c7ec76dfbe16fe3e351de7e8139` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/OrOperationV2.java | 2556 | `6c70af3b1e8dfe1c82d4ab2118a46208b3560e8b049898e2ff8a6ddfead5377d` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/OriginOperationV2.java | 1581 | `8e51eba7c9a4745dbd03a886b2418cce48e0e00cee89d0f6f15b7fee83625c24` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/PCOperationV2.java | 1540 | `e37afed89066b8e49be3c60ca0596e7153471a499032993c6e64437674b93fb0` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/PayOperationV2.java | 4318 | `91946e66e19cf775fc9570f6595c44fc008f5e9b66b6d6050ab6afd9802bb4df` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/PopOperationV2.java | 1783 | `7718dc78a2c280456eb30a3bdf2300c8a34f9e37f1d2c581aee6c688fd702168` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/PrevRanDaoOperationV2.java | 1685 | `154fa389fa9aade2bbd61ccd886881382d4056c7df2cd2eb8a9232fbfca069b3` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/PushOperationV2.java | 6802 | `daacca91598ab62def26c4aae227db2fc1556a8fa74b4e6f9c660c41cddb2574` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/ReturnDataCopyOperationV2.java | 2849 | `d67341b5abd0e9a300e8a33a134aa0dae8c50ae1ded496d6c26f38666d9ae523` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/ReturnDataSizeOperationV2.java | 1619 | `a7d3979486f29281713b6b196d0afb3ce64033310478e442e73e4d4d7c009bd4` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/ReturnOperationV2.java | 2166 | `8cdecffd6ae263fa8c1e52ad728b34e84145d538f3af179de332c167c4a905e5` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/RevertOperationV2.java | 2267 | `fdab72bed0b8a0cabd80e79426e588b71f9d1b675aa97462f41420845432178f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SDivOperationV2.java | 2433 | `a1a07a922e76e666801ba4fced6fabbda93d138bb10c43bd4599202b2bbe6d8e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SGtOperationV2.java | 2362 | `a7a23746f3dafbdec0f475752f6e0065bee8d2d74c2f1b6bdddde5be6409497f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SLoadOperationV2.java | 2959 | `248634cee98689c0a00d5dc6dc40186e2fd371a66d2329b991b3d635351aecde` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SLtOperationV2.java | 2356 | `a8e97f9da13f2dfeeab964aff4f7cf61a7f816c6ea78a2c2252ea0fa5fb6c7a8` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SModOperationV2.java | 2455 | `73b7e24d1848e37ebcd564951cfb1e28174dd7765e650f7a1eb61d14b580fad7` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SStoreOperationV2.java | 6052 | `3d1f82cb708ee886a995eafb2ff21199574870e7f1382314a3bbd55c746502be` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SarOperationV2.java | 2594 | `84c16c84255694d6ff7810e1ba8d676385019552347a7628a6d3c5e554a60c3b` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SelfBalanceOperationV2.java | 1913 | `d18883444e2f1c03001f52ab278e0bfd088c8a80b5c70a1d4a66fdd4cc6dba0a` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SelfDestructOperationV2.java | 5790 | `fc6633c4a7282d1d78fe4f5aa07a617cc71434c8857da2712a44343afc8b61b6` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/ShlOperationV2.java | 2614 | `c09dcc00c7b4952dc7a01428133fca4e960ceace0c99bd22dcc785666c82bfbe` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/ShrOperationV2.java | 2608 | `1b84ec39c96564693f63c6162fda9f203c00f16eabb6615fdc743f5c8ca2c69e` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SignExtendOperationV2.java | 3303 | `f992e30b965228d9e099bce2cebd166b4730f967489be7693dccbdddc0114f9f` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SlotNumOperationV2.java | 1620 | `d25b5520a9e6b2dce05e2045bed3726b40918dc41bf2aded5833c8d36e3adefd` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/StackUtil.java | 14662 | `b94d1a03d0f52c45795c7c3ef51cc8b5ff64ccbb04537523425db9e48285de07` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/StaticCallOperationV2.java | 2776 | `620dacc78826f55f8139228dc4f58d42a706d53b2ed424e86119b3c922a29fd3` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/StopOperationV2.java | 1758 | `954d696a239057e4884ca08e6c8c8492f16604c2f886f93278e0d80c5c590d84` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SubOperationV2.java | 2572 | `2101d1d800210219e41e64ba8562f424acc6da167f245d9fab6b28a6be5cf905` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SwapNOperationV2.java | 3115 | `eb146d67ef179eab5ec70f6460a08c59c7b7b912020fad4453f8fcfbb2e7b777` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/SwapOperationV2.java | 2564 | `ae735e31b80edb80a93da4031a4c7f6db477996938ff6b90e9b5dfddd47cf752` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/TLoadOperationV2.java | 2141 | `80881b32a392106931adbea209de0f30472e5447d46354e0180b924b7159d700` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/TStoreOperationV2.java | 2299 | `b7fe93afd33482d30673f4f46cdf72f17def5d1d94639f5ff404c0afc091782c` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/TimestampOperationV2.java | 1662 | `c12d3c1f36d4cefef30e9391e4f33b264a8d987495095455632f4600f06c87d7` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/v2/operation/XorOperationV2.java | 2564 | `0d6af4b3e43d317f763eac5f5076563b5bb9fb3cbd607c84e9131de205f87bc6` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/worldstate/AbstractWorldUpdater.java | 5891 | `747571f8a67d09decdc32f0725529da5deca262d3183fc962132af4f6f324e52` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/worldstate/CodeDelegationHelper.java | 4627 | `048be14821204140ad3ecc7026c4d1d02e4ed6acd817dc43689b8e6ac5540616` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/worldstate/CodeDelegationService.java | 2409 | `1b845403ca5836b43b1f20e75ddddeb741b55ca9a443b1d348ede6e870c53711` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/worldstate/JournaledAccount.java | 11715 | `17d31534934e695d672efc8c10883732d73a63de53f224410f6f306ae5d514d7` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/worldstate/JournaledUpdater.java | 5771 | `88cb06de25d0ea18ce86c01cbe45254f7374fcace8b2dd9f81c732770b0494e7` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/worldstate/MutableWorldView.java | 999 | `e8fecbdc62e9e41664093503b8b46702ff76558e73159d0d31c2757c5f00004a` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/worldstate/StackedUpdater.java | 4666 | `b8cb9a76ee5f5b55e43275af95a090f239b617f58820c0d3ac8fce1cf3c5e4bb` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/worldstate/UpdateTrackingAccount.java | 11162 | `de9eb3735813fcff6991544c0fad5153eb9670c5da175e470a037e95affb6bb6` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/worldstate/WorldState.java | 4015 | `e9c3e306bb010fcba76bc94b8f53483458ff43030cc2eff97d9b8d7b75c43de3` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/worldstate/WorldUpdater.java | 5942 | `51f8cc631e29530010e74a6e797e524fc96eb1dc5fff01e1c00c5a7adaa31feb` | 0 |
| evm/src/main/java/org/hyperledger/besu/evm/worldstate/WorldView.java | 1207 | `9ccaff4ab8782844120a10fd354372916e85f71ebc1f6224e746b7cc5d7992b5` | 0 |
| metrics/build.gradle | 646 | `aa191ff708e7b1f228615c5b5cb16cc678f78950515a188dfc87a693e9676ca5` | 0 |
| metrics/core/build.gradle | 3452 | `11cc0a6d1f588299c2a5bf05c8bb058e92c74f5b801e22c549797037b8f01bcf` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/BesuMetricCategory.java | 3608 | `f3f53b978dbf79b62d1c6c6523ffa9db1a8bc5d03f118ccddab7c8d9ab411652` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/MetricCategoryRegistryImpl.java | 3497 | `7985f71a40588c533f9d7b7513f5f5ed39e1cc95ed3277840d6f9f08f1951870` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/MetricsConfigurationModule.java | 1165 | `f480a488085b512283895f09b10484a6da2728066658d3cb1f4d9e4aa2c13eee` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/MetricsProtocol.java | 1358 | `17d4bc5387b174227b01f6567431e67088bba2d0d5707acc6665bbde737e9c19` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/MetricsService.java | 3086 | `54b9c31f3a32a06aa07356afe3d82e937269f297d90d395863aa929c7514a9f8` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/MetricsSystemFactory.java | 3241 | `64c7e462ce5a11cf79e2c0f6f5187a23b9f111f1feb6254d6b3a00c20dfc9904` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/MetricsSystemModule.java | 1277 | `497a5e8aaa88cf3a4c1bfcde80755671a2dcf7e496e6763c9ef981ed4e16cf9b` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/ObservableMetricsSystem.java | 1377 | `8d8e391f91b2477e494a568e5e3652fef90c934c0d5be359fbeec13c5951cd7e` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/Observation.java | 1020 | `029ef013ba034985d1557da3637bb05e5f8309e735823219aad0137cbb89b2dc` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/ReplaceableDoubleSupplier.java | 1782 | `95402457785818545fba12027b2a651f9e7d60c62be95904bae9fb64a334674b` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/RunnableCounter.java | 2103 | `1894205bc3218ebb46df1d140f9e0009d11ebebb4a9f447d68cc102a97e94da2` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/RunnableTimedCounter.java | 2444 | `cdf4f30f1e2d9964054d55e9daf45ba727ddfed4d34189928af7e2e60b915a82` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/StandardMetricCategory.java | 1244 | `77522c83b95d8682063a7f3b7cf771f057614904eeb70ef93644b115bff0c148` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/SyncDurationMetrics.java | 4453 | `dc45239bc6298825ae18f4c6eeb972d55409ded0bbe121db35a3062f883e3c4b` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/noop/NoOpCounter.java | 857 | `60d96d8b4adb7fc1f5eafbfad598d6db988adcfd401cad69bf6f17faa7e732fa` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/noop/NoOpMetricsSystem.java | 9315 | `60d8ee9c2ab192f16c83c483653769479e8a09248847bb49150d0fba61d42e2d` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/noop/NoOpValueCollector.java | 1511 | `849460b3450b94bbfec3a6fa5b1a276789462621e9968f2c34bf749ec0c7c971` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/opentelemetry/DebugMetricReader.java | 1925 | `83405662f2929d791a600960e3e97ebcdc577d66be3e243da6a25d91f7b6376d` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/opentelemetry/MetricsOtelPushService.java | 1780 | `2d07aef7d3bdc2fa2e16b3d211c401acb3f94c7b2db729195fc944341c89d9d4` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/opentelemetry/OpenTelemetryCounter.java | 2225 | `0dd89d7d665711304a775eee47edf2cd2f713c7f4710449e47259cf4bb569c7a` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/opentelemetry/OpenTelemetryGauge.java | 1598 | `8fc6f98082969dc198535f052c0e1b6a57e1e6d39db5e1747976b0c3346e0b8d` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/opentelemetry/OpenTelemetryLabelledSuppliedMetric.java | 2684 | `9e65102c4765b186a6d6f17dee3224c6eff0499439bbf7bb6f966faedfcdf261` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/opentelemetry/OpenTelemetrySuppliedCounter.java | 1616 | `662ac13687e4f0bb79d12e88379529c1a868be9c44a1b049f0b0c97441fe7a66` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/opentelemetry/OpenTelemetrySystem.java | 17996 | `602053a52156229b54394d4434fdb443afb1701a5e888b3395cb55caedec65d7` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/opentelemetry/OpenTelemetryTimer.java | 2673 | `f7bddc7029e36fa036ee8907d05cec5f0c2962def898a3eec702fdadf60f656e` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/AbstractPrometheusHistogram.java | 4010 | `3d3384009870e96e84ad2080e4dca096156c6b8ec1cc1edd3aabdf6fb28e5546` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/AbstractPrometheusSummary.java | 4657 | `a7fbee5477fb3735a27005fe8f03921c8bba9e0843f58814c1c234b52d5ad9ff` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/AbstractPrometheusSuppliedValueCollector.java | 3542 | `6d2c60a2ecd7a66195ca072a07ff1a48d30235926da2e2ff7b4099ba17f4df72` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/CategorizedPrometheusCollector.java | 1922 | `aee1cc65d743dc38684d06bb83ddf69dca8ca17466f0a8cf74d8f7a0ca25198b` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/MetricsConfiguration.java | 12164 | `5f2c083de06f6c3dce90d3e77a33de9fb8382547f55654281795377d945ca468` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/MetricsHttpService.java | 5879 | `40035eb8d447129e7cee37b64e1990701ea8a5477554cee7c0dbc26336179f3e` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/MetricsPushGatewayService.java | 4489 | `074aa6c4eee24ba2e73d96899203f7f7431558e69c45beb460db2cfee72dcfb1` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/PrometheusCollector.java | 2554 | `bbece7f3e3b44ae94bafbd0cab490da023ab220f1dd7e9cd3143532bb5ae5982` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/PrometheusCounter.java | 3305 | `7da92767ac200ee8f7cd6511209ac05c661551fb5501ed80cd8a639e990fe4f9` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/PrometheusGuavaCache.java | 7040 | `f99c8b85c8899faf0bf515f847dfb96fb28e0c087e8aeef91c344d9150aa4166` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/PrometheusHistogram.java | 1525 | `3e735f153a0cec02fb189a32e50e075b7d19ab2494d4eb48732595ecf5a5e7b6` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/PrometheusMetricsSystem.java | 10892 | `445c9671b73609c6e7bd100098156457ed2440cdbbc179d29f187f8514bfeeed` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/PrometheusSimpleTimer.java | 1618 | `fca7ee88ca0f7d7a1d58ba8f8711ba91956f5eabba5cd1258711a3e837aa25a8` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/PrometheusSuppliedCounter.java | 2600 | `51ad7e6f3712592fe627ccb3e54c3531033d7c71dc75560420ca9571e05d7178` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/PrometheusSuppliedGauge.java | 2699 | `b1d1ec1aa92bda4adf2bbd2b54aa0eeb45d0f4279b1293c66a7d107ae2dc2352` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/PrometheusSuppliedSummary.java | 3316 | `834760593282db16b25ec297036d3399173a56ce193351f8b0c5578d18b0d656` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/prometheus/PrometheusTimer.java | 2001 | `d407685c9712dd0151b9ac825aea58aa0d16f5b75c139037dd3652d17557bc3b` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/vertx/PoolMetricsAdapter.java | 2656 | `e976572419cd13d53208a19df3fb2930ca685443fe6bb486a00b161c55f9bcc6` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/vertx/VertxMetricsAdapter.java | 1391 | `e5840107fb9bc4db12fb7e33b6a7523e362d753fc10d3cc70b7b4aceb887de40` | 0 |
| metrics/core/src/main/java/org/hyperledger/besu/metrics/vertx/VertxMetricsAdapterFactory.java | 1381 | `fee4c404f51a7e00575beaa6c5e9381be370e867e6df2f5804183d8f66e7717a` | 0 |
| metrics/plugin-api/build.gradle | 1741 | `4c3fc0a10dce02492d2909994e32c2125f6bb83e5112bb05b70f24cddf03f425` | 0 |
| metrics/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/MetricsSystem.java | 11723 | `04231bf03c6656427c0457fb30e404b01ba4b6c92321243414e767dd621bb7b6` | 0 |
| metrics/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/metrics/Counter.java | 1074 | `a29c375b96cfc80a2dea18f34473e56b321467c88485d5e2f781509f90eaf794` | 0 |
| metrics/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/metrics/ExternalSummary.java | 1383 | `88829764203e094150f5d5fbbf4e8de528a82c11c9e28a7c4349cb0d62e41262` | 0 |
| metrics/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/metrics/Histogram.java | 1018 | `3827eef4222ec58a0ed529088087039a69ac6f3adfc9b63f5ce81ff615e98df5` | 0 |
| metrics/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/metrics/LabelledMetric.java | 1248 | `a0f457aefb905927b8bb240aae509de748e1ca052890d16d6e7a56db807109b3` | 0 |
| metrics/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/metrics/LabelledSuppliedMetric.java | 1004 | `e8318d71889a03a2a2e33652d084fea59a24aac47555832011592c6bf7038ca1` | 0 |
| metrics/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/metrics/LabelledSuppliedSummary.java | 1027 | `1bd1e53b45296de22fe620ab44a3ff25361419b1998ca2be715efbd5fc17e251` | 0 |
| metrics/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/metrics/MetricCategory.java | 1476 | `41a12431b11d96076078c8a225384a16e25ae768df9cbd07885b140ea8ddc22d` | 0 |
| metrics/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/metrics/MetricCategoryRegistry.java | 1505 | `866dacd59229e801f6c57f34af3890a85b4021b73b3f0442883196136e641c2f` | 0 |
| metrics/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/metrics/OperationTimer.java | 1350 | `477111312dc87056e50f4b1bb69add93af1107d6609a63b1ec1aff826f62ac3a` | 0 |
| metrics/rocksdb/build.gradle | 1596 | `f17a042d6389c15cbadcef531406a0a8c42e31962b9aac2341e274e6c8af06d4` | 0 |
| metrics/rocksdb/src/main/java/org/hyperledger/besu/metrics/rocksdb/RocksDBStats.java | 7209 | `92c1c6e1ef41fe4e920e2ea07a6ce09723ca31b18edbec2cf602b5bb9c166b70` | 0 |
| nat/build.gradle | 2090 | `a26407234ca8155a82fb20980cfa7d7d12543121a3998c728c91c8c3f5569e5d` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/NatMethod.java | 1308 | `97e72a0381a190883c6d6a966a07f4c735a81c3b9d8fb2c29d39a6a66a4a6da9` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/NatService.java | 8429 | `f09436f3d08dad9181a2c99b4e63b89604aa14f5ebbcfe642fcaa647a13870ad` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/core/AbstractNatManager.java | 4895 | `96a8e61ab6cff15a1ac483b41c41690ff547d24d8137ce49c9ca97ce9bf682ef` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/core/IpDetector.java | 967 | `062ce6114e565478b168de7dc4568d0f45e3d950d138839dee233be812e9e157` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/core/NatManager.java | 2879 | `0c2063ea4423e01e30f8232859792ae7e3fd0698b1156cc32a5406e166fb1303` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/core/NatMethodDetector.java | 944 | `78dc4c52826855099d19a6eec36f3c47f03a5e47bab14526df1972e8368f0210` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/core/domain/NatPortMapping.java | 2845 | `59aeb70ba0ff9b7ae8d9ac078e61e4a68d859771f96f3116d9c1e4046929c447` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/core/domain/NatServiceType.java | 2085 | `30aa0ee5dd6556938f5e5fd36f0b11cd7a657d7436b699360379d55e3c4f6414` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/core/domain/NetworkProtocol.java | 958 | `2616eed95c1f0e8f8b87833565d6d48c74500bf399785538d2c82985c24ebb0a` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/core/exception/NatInitializationException.java | 1208 | `b8611886217ee945d7caa0b4e8f7f1d2c561b136c2247dac7b15478b24b04906` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/docker/DockerDetector.java | 1579 | `520f8a74b6240ddf04c7cfbe501afffbebd674e4c3bdbb371f26da3f4fe57c7e` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/docker/DockerNatManager.java | 7122 | `ec7b669ea9780047916ef68c78311503cb5deaa424751df5ebb0ca9ea0a1b5d3` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/docker/HostBasedIpDetector.java | 1293 | `be3a18aa2cd93125aed9fa14e1a8e9d0ea998b38eced593d55d014429ac31487` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/upnp/BesuUpnpRegistryListener.java | 1754 | `9f3a4729437afb0f2c6969bdf6285a981116f19516e8807edeb083eeb66e74b9` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/upnp/BesuUpnpServiceConfiguration.java | 7907 | `6e816657a24bd30a42c957e83d321c9593038e17e7fe474c474b420c979b085d` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/upnp/OkHttpStreamClient.java | 3941 | `e67f6111d74b3147b6bcfaef503d9ddd469adb00022f543fc566d538cfcb5676` | 0 |
| nat/src/main/java/org/hyperledger/besu/nat/upnp/UpnpNatManager.java | 21615 | `0ebf4e33d14f6551a7327b1915b728d73055bc0d1a17773d09d5cfdad70066a8` | 0 |
| platform/build.gradle | 8757 | `1e0963e2db8ff34a2f34b39ec060bf7523406e477c262dca10e85e38e84f6eb9` | 0 |
| plugin-api/build.gradle | 6485 | `0d281108ff80a783a70027df71f75b814fb51c8963dd87d15c830a51321187fb` | 0 |
| plugin-api/core/build.gradle | 1489 | `141eadff003652c349af72e9285c8db7d592a2743e4d91b881e34bf441519e38` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/BesuPlugin.java | 4322 | `335404bcb678e20926a5ac667a872cac488ee27b2f13dbe1ed5bd1860b92c99f` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/CoreConfiguration.java | 1467 | `73b05b5c420a2fa62107a882f09f57321e5a48adc880338a275a6e8d4cdce651` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/ServiceManager.java | 3010 | `04c33d5db7cfc24cb4de429478424c77e74c403f9c3a4dda2a8112584ef18786` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/Unstable.java | 1232 | `22eb11cb7342d9b1098f2869f0748d535616785d659f96d3693f40c4db13bcb7` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/data/BlockBody.java | 1630 | `b41acbf099cf9cd92418b3653de50777c69d1d2a77ae23e5a4b7fa8a78c4deda` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/data/BlockHeader.java | 5515 | `9b39ca93a2f496f0f8c3c8bb8b50f6e52824e99a028355c8345c8f46cc7f7ffc` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/data/EnodeURL.java | 2036 | `6ff277661414cbb311a72f8522b90f5a13c0616f26375ae43a6934307978ab38` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/data/Log.java | 1321 | `ef44b1ce779d0ed4c9384425b44dc13c96e3afccb6d97e71b5c11a96ccfebda9` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/data/ProcessableBlockHeader.java | 3565 | `19b4e814246019663e94fae8f51eb36bd6caecf759d5479f35cd3569011ef31b` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/data/TransactionProcessingResult.java | 2829 | `5d74870dc1548b21c50a78f79dcf1669842503fe2bf9fe6ef21a81226cb29bbf` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/data/TransactionReceipt.java | 1961 | `75501f4cb7a8b0aefbe7bb37b23d8c82ce6efa607e1186668510fc0d083a18f3` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/data/Withdrawal.java | 1638 | `956b2c95ec8274a680befe25c4ef68be43c285769c161dd19506ea44629fb992` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/services/BesuService.java | 880 | `1cb4403d13b2e7addd93cc201f95e5149a08097116e51624aa2d7393bbcf802c` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/services/PicoCLIOptions.java | 1634 | `2084efa50a683bb0a3f2eeffd58707190440c72221c240ef21f82a9950e5bd89` | 0 |
| plugin-api/core/src/main/java/org/hyperledger/besu/plugin/services/Subscription.java | 1406 | `a0b6b7b0d8290a4d3e4e6539bdc3ee8b1ec95818f4cda182905dd3bd3569d3bb` | 0 |
| plugin-api/src/main/java/org/hyperledger/besu/plugin/data/Request.java | 1435 | `302cb45f9be48d604f843b9fbbb3c255c1c9d71ac2ec37044ddb47c955c9be69` | 0 |
| plugin-api/src/main/java/org/hyperledger/besu/plugin/data/Restriction.java | 1527 | `5ea933e1c6d229277f7ffc6d26e015c98571d6258fcb586191b00aef7650c4f6` | 0 |
| plugin-api/src/main/java/org/hyperledger/besu/plugin/data/Signature.java | 1172 | `eaa42dbb0bd6927f25e677dfd28a2ff1c55fcf05449639bc61876c7430481c5e` | 0 |
| plugin-api/src/main/java/org/hyperledger/besu/plugin/data/UnsignedPrivateMarkerTransaction.java | 1891 | `d64fbf37381bc889b81fc9246f188473d6c1a81a4b82726c99e63c3aa48aab69` | 0 |
| plugin-api/src/main/java/org/hyperledger/besu/plugin/services/BesuEvents.java | 13345 | `835abbdc4bf127d83b3aec85ff1967027e4b9cf3d1375b90b44585628f1ee09f` | 0 |
| plugin-api/src/main/java/org/hyperledger/besu/plugin/services/PluginVersionsProvider.java | 1142 | `693be602a4cd26bf7bc17aba5559b83a2d258c7c4909b7c6d097fe4b4620b9c5` | 0 |
| plugin-api/src/main/java/org/hyperledger/besu/plugin/services/query/BftQueryService.java | 1836 | `81c37c4d02861b2b1b59ef7ef37dbea9850d630e88483a87f648e1540dfea026` | 0 |
| plugin-api/src/main/java/org/hyperledger/besu/plugin/services/query/PoaQueryService.java | 1844 | `c68cb202b9e6be73f089dd8b0d07b7fb1e95f0a19128d395e07ef31fc2201049` | 0 |
| plugins/build.gradle | 609 | `a728d984b294c9eafee51f1c7b8052c0c40500f6738cd040b3ac139c2dc4e0ba` | 0 |
| plugins/health/build.gradle | 1283 | `a9ebcedbf7a50bb54c600571f06efd65ccf1ced266319e4093d983f53978f51f` | 0 |
| plugins/health/src/main/java/org/hyperledger/besu/plugin/services/health/LivenessCheckPlugin.java | 1606 | `600b7944c0a21dd668709e0a5990e7d616fddc67ae729614ce453a87324d7a5b` | 0 |
| plugins/health/src/main/java/org/hyperledger/besu/plugin/services/health/ReadinessCheckPlugin.java | 8543 | `0a96fdc82d8423d375edc7592828348e1fc5a910f2adc5ca3408a5a1254a2f4e` | 0 |
| plugins/rocksdb/build.gradle | 2372 | `348c4b9cde17ef16495826c80def596d809d3de9f040aefea23f903e7c4c4d94` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/RocksDBKeyValueStorageFactory.java | 20766 | `09ba80dc4a3aa0ac232d0699e8329ef727a758b99330797e3e5dca2742a34ab0` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/RocksDBMetrics.java | 2892 | `e10966378580f62cfbf91420ce05ed35a0e187665252b5392bf7db07dfed0c9c` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/RocksDBMetricsFactory.java | 5901 | `b238ec0df0280a228e9c7b0e4d19af1afaa1659ec3108ec0179000876c091f77` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/RocksDBPlugin.java | 5363 | `89c973cde37ac5e47265742e5ddce64652558a26c01871daf3fc18a5b83baf9d` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/RocksDBTransaction.java | 4347 | `feea88ccb3e2e657867b98e6bf4a63e89434acddb8ad1334db86019b1703af9a` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/RocksDBWriteBatchTransaction.java | 3668 | `3d1040feb802359b35594b6efcf6a49cb33f94c874977d02c1b8925fc25bfbad` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/RocksDbIterator.java | 4532 | `c94bd43ed64967be7b84f353d52a8fbcbfec7af1f909790746e52bfcd907f00c` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/RocksDbSegmentIdentifier.java | 2699 | `5057b16d3baa87ca8c7046a8007b4b8216e0555434855f31cc0924ca91a52512` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/RocksDbUtil.java | 1480 | `ebee4bf6639df5a6ffa9917c4448d92945d61a86367366c534f43f012a066d40` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/configuration/BaseVersionedStorageFormat.java | 4499 | `07eae6398dcedd266ff2819910db642970e41946d021cd7ac2fd3ac95fa4955e` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/configuration/DatabaseMetadata.java | 7234 | `4f974f57eda1debefd2c4fa5e4dde3f2098c3a80c9cfba0c03a2e0fdbf558555` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/configuration/RocksDBCLIOptions.java | 11724 | `65b8174bba6fe8407ba9176f38a38c37a8f9b0ce9506327326ea9a160f9c9970` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/configuration/RocksDBConfiguration.java | 4664 | `b434d2b8d959d820476b0ed6136bf03d9ea3cd46f5acdef414f00c563e8946b4` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/configuration/RocksDBConfigurationBuilder.java | 7033 | `113eab56bf3bbc9a232b7c36776c57f018bd630d149ffca2636963fb92acf01b` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/configuration/RocksDBFactoryConfiguration.java | 4212 | `9cad65e4e54d1b6fda05dc0bfe38b966fa45816ea7226e2ef9dba2b93974c67a` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/configuration/VersionedStorageFormat.java | 1153 | `598acda8ec21280f3345f1bc0416e088b56805b73e5889be1154a2b0a3ec380b` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/segmented/OptimisticRocksDBColumnarKeyValueStorage.java | 4562 | `0eac58807933be2056961dbb8eb87d2d2aea5f6fae9f2c3b6e963e955c082491` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/segmented/RocksDBColumnarKeyValueSnapshot.java | 9811 | `6dbb38843acfe58cf066e4c84746e2bf20b3fa6cf61a0ee399fb905e60ac57c6` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/segmented/RocksDBColumnarKeyValueStorage.java | 29860 | `debc3252d73f3c618a3ed1dde03d9f396cb7d142635aa4aa72053bb3660367e8` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/segmented/RocksDBOpener.java | 6749 | `22451116ca5456c72b5676182fcc02faf811cc03b96c391a8b182b65da94e41c` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/segmented/RocksDBSegmentRewrite.java | 25428 | `1735821d615dd3bd18efb42142ee85ab2775eb3e8de91237fe14afda4e05262a` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/segmented/RocksDBSnapshot.java | 2006 | `67374b1a03dec8c35b48e76bd9702315abd9c294a793957b30d143d659e1ddbd` | 0 |
| plugins/rocksdb/src/main/java/org/hyperledger/besu/plugin/services/storage/rocksdb/segmented/TransactionDBRocksDBColumnarKeyValueStorage.java | 4106 | `d94d74ca8c2a6132d77bf8e0d3e32dc56eaa979d69fa3da756d055847c4444bf` | 0 |
| services/build.gradle | 646 | `aa191ff708e7b1f228615c5b5cb16cc678f78950515a188dfc87a693e9676ca5` | 0 |
| services/kvstore/build.gradle | 1688 | `d6265369fafe728006f4b30e72cd24b89b0a0b2a1943bee32146e0a553ef61fe` | 0 |
| services/kvstore/plugin-api/build.gradle | 2096 | `fa2d88b4d6b48f39a7acfd87ecdf0058fd5218afe62668fb2429142e6064302f` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/BesuConfiguration.java | 2399 | `4cc713fce68c69af30f5108cb7c548d286eeda70fdeefd5ff4455693cdeb3c08` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/StorageService.java | 1878 | `fb69fb057588b92f555c7fa03491177a7fc960ac364352258b1d94531f28bbb5` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/exception/StorageException.java | 1884 | `35585f92046318d517a9bf0f5b280479835456bb2874b2c6a90139dade4eab0d` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/storage/DataStorageConfiguration.java | 1855 | `266e453d8ee86d1135ac6f2c066e56f58f68983319002334284a2c4de4c7ab5e` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/storage/DataStorageFormat.java | 1231 | `cb4f3a798f6a945566c33c0802f38ee19ceeb44d9ae953f97e569a95abdf638d` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/storage/KeyValueStorage.java | 6202 | `52fd3ba0c036c78278740b8ff40e224e181c2c4ffaa21e96573db7aeacf6225a` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/storage/KeyValueStorageFactory.java | 4143 | `96281506b88a09061eaa95458ae30db6073c1d314c0d32d1830f8ca01785d088` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/storage/KeyValueStorageTransaction.java | 1860 | `c16768d53368c7850a782fcc71aa00fb55aa84563bd1a371f408a0cebc3ec2ef` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/storage/SegmentIdentifier.java | 2841 | `18f62403b6201543c7a9dfa3ff5940e2b7c7fabb73551efd4be19d849570e028` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/storage/SegmentedKeyValueStorage.java | 12236 | `bb260439ab915d34b3a1834c1043f52abfbc883de103d81e4eff5f934c437a44` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/storage/SegmentedKeyValueStorageTransaction.java | 2063 | `586f8d9ed1317dc06073fa6b903bc7b78926c68e4162acffd03ce4ed41c0e018` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/storage/SnappableKeyValueStorage.java | 947 | `394b4e8d69bb21974d6a38aae27f67cd47ccddf5843b3c0676fdc1f7f02e4734` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/services/storage/SnappedKeyValueStorage.java | 973 | `55a540b19ffaaea59e27256bfc45426661ba709c578fee2a06e23c0211832ba8` | 0 |
| services/kvstore/plugin-api/src/main/java/org/hyperledger/besu/plugin/storage/StorageConfiguration.java | 1812 | `c945fa0230b9b714a473be8594f419d219ab4b425e19f1e3bf81aca7cb220f1b` | 0 |
| services/kvstore/src/main/java/org/hyperledger/besu/services/kvstore/InMemoryKeyValueStorage.java | 3388 | `4f930e6176e76e8ae4edce2c77f14cb75db5f3e45740d5e6b0ec6bbc68da4b39` | 0 |
| services/kvstore/src/main/java/org/hyperledger/besu/services/kvstore/InMemoryStoragePlugin.java | 4709 | `318a9a90cba66cf31176f1476a9effe2ffebc6633b60a6195b29fd303791494b` | 0 |
| services/kvstore/src/main/java/org/hyperledger/besu/services/kvstore/KeyComparator.java | 2448 | `ff4bf0bab58d11efb0a275d7931e2ca1da9e5aef89fc0ae2dde6279be29bc4ea` | 0 |
| services/kvstore/src/main/java/org/hyperledger/besu/services/kvstore/KeyValueStorageTransactionValidatorDecorator.java | 2897 | `19e00414909445063e20c7372bdd46588ececb1632d8d9444f9c0fdc7816d580` | 0 |
| services/kvstore/src/main/java/org/hyperledger/besu/services/kvstore/LayeredKeyValueStorage.java | 17591 | `23176e6947f45bb5a35ec94e57a20b85117b62fb6558d58b08791daacf3e6336` | 0 |
| services/kvstore/src/main/java/org/hyperledger/besu/services/kvstore/LimitedInMemoryKeyValueStorage.java | 6279 | `30c12091583d631b104b1a89866954f9fee5c38d30412ed126788cc745f100a8` | 0 |
| services/kvstore/src/main/java/org/hyperledger/besu/services/kvstore/SegmentedInMemoryKeyValueStorage.java | 16597 | `77fe2e27476011e7923123c1a489e0ba383a576cd115377dab508d48625c6ed4` | 0 |
| services/kvstore/src/main/java/org/hyperledger/besu/services/kvstore/SegmentedKeyValueStorageAdapter.java | 6479 | `637e197faf6fd5085fbe604d5f478bc9f4744dc7c906f384c005adee29f9a28c` | 0 |
| services/kvstore/src/main/java/org/hyperledger/besu/services/kvstore/SegmentedKeyValueStorageTransactionValidatorDecorator.java | 3138 | `f9a30cc1ee17cc238b54d00bd1ae728a6a40de4326e5773ca6aef9401aa461ba` | 0 |
| services/pipeline/build.gradle | 1936 | `e611dcfb2b3ae68a9a2c1e37308d1c93b8afd03f0cf657d7a543795b04a787c8` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/AggregatingReadPipe.java | 3173 | `51e6da43b2b4747a1f186c5a2cad2035be1f1b919df07933d2a2aae2b36598f5` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/AsyncOperationProcessor.java | 4957 | `a52cac87d34f9b400ff6144d393815e3b1a45bc8092279092decf0a7e4037b6d` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/BatchingReadPipe.java | 4022 | `c488096235623b9e764890109a67ebb1477975ce5f8f9304f3f6a9ea071f93b9` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/CompleterStage.java | 1485 | `50371e264d43675f0b47bede9ab4f11c3f4d39e9ca17f85b6f285217f8f291ab` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/FlatMapProcessor.java | 1173 | `676cd1ae6a97c180f97d852c728e33fba950a2ba021bc17d2650e97d298b1c10` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/IteratorSourceStage.java | 1277 | `e5e2712ef22757d61dfb3be627da15601ab17542a902549bf9e7bfd5bdcae6c8` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/MapProcessor.java | 1123 | `f71c13e1f60d6e96dbb0242852e6348af1ef6a4336428dd5b5c2722ea1dbebdd` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/Pipe.java | 4938 | `ab5aae237e953b735df4b08259eeb5fa86ebec4e344ba6559754da5b371bb92c` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/Pipeline.java | 8354 | `c9a2dffc6b343a99c80b294005e5c2bacb217e08a3064f91e36e11067fda5f39` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/PipelineBuilder.java | 18693 | `ae0895661d42b1ee8ca848e95d9160f6cb2846edfa28dc0e7161ed4c11367226` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/ProcessingStage.java | 1595 | `dba8ec1ec00fbe18b9af4ebe6b7913df28d7c1e114a50d0c76ea1f9b801ad4ee` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/Processor.java | 905 | `892d25758a2b413858a9242155f620713d8ea73a61348ef97b1a0e7b9f523b97` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/ReadPipe.java | 2387 | `d63f7e3efebf547642392a478d20b392d2897e38abf75a7185543b916d0096b6` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/SharedWritePipe.java | 2092 | `7ad295779580b5442440cb6e1429e14b6d240d1b845bdacf133e9b5bafbc9a75` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/Stage.java | 817 | `dc27356071015b45a59d218663f202bb9a4db4f211892e28d425198276f6b947` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/WritePipe.java | 1779 | `02a94c18715bcdc0caffada9ddde2c2a14709dbba03b5eccc97fe508f9691949` | 0 |
| services/pipeline/src/main/java/org/hyperledger/besu/services/pipeline/exception/AsyncOperationException.java | 1144 | `9909da79e1adb51f7350245d593528c9458979cb20d321e99cda494a8951b6be` | 0 |
| services/tasks/build.gradle | 1863 | `4640395c2173bc6e59fd9a60b7555f2ffbbf74e21bf2067ab3fcc45ab4613ca9` | 0 |
| services/tasks/src/main/java/org/hyperledger/besu/services/tasks/CachingTaskCollection.java | 4681 | `35eed3b5bbc4d26718621e3e0dbd1b2ea97f5ff2b2eaf4c831f0f02a6f30bc61` | 0 |
| services/tasks/src/main/java/org/hyperledger/besu/services/tasks/InMemoryTaskQueue.java | 3796 | `3ad393681ed819b1e294e080b74da80e798ca698db6202b34be08c80e7450e7b` | 0 |
| services/tasks/src/main/java/org/hyperledger/besu/services/tasks/InMemoryTasksPriorityQueues.java | 5329 | `7feba81b6c5bd351538360ce12b57bb2d812afde1242225755ebe527619c0ddf` | 0 |
| services/tasks/src/main/java/org/hyperledger/besu/services/tasks/Task.java | 965 | `7e021df30d7b82fe9dd714bc98690ef0651486de4b7f3284a239bc71c17458c2` | 0 |
| services/tasks/src/main/java/org/hyperledger/besu/services/tasks/TaskCollection.java | 1796 | `a98e352504e99471b88928d0d257b881c0965b15920d3ab2f537433fea7aaf91` | 0 |
| services/tasks/src/main/java/org/hyperledger/besu/services/tasks/TasksPriorityProvider.java | 937 | `dea56b4a3becd93c5aab8a15aac05d4bfd52aff410781a3eb171102f6b655929` | 0 |
| settings.gradle | 2750 | `1196118fe1f500c212c84b9c0b4804c30b53b1bc894bb1ca1f061f5792b03dc0` | 0 |
| testfuzz/build.gradle | 4612 | `dba0f69651eaba69845893f0a8fb6d587739f0d835b077065c0dff2e3326e4f3` | 0 |
| testfuzz/src/main/java/org/hyperledger/besu/testfuzz/BesuFuzz.java | 1295 | `02cc29370a2ff1f013c69dfd0430f9c650b892eaf35d771a74f6996e5e0b4e79` | 0 |
| testfuzz/src/main/java/org/hyperledger/besu/testfuzz/BesuFuzzCommand.java | 2424 | `437d7693796ba1a48b108a66eae4513cda76c4433fd01bcd041e5013eeb5290c` | 0 |
| testfuzz/src/main/java/org/hyperledger/besu/testfuzz/FuzzingClient.java | 771 | `37e9241dbbe6a291e7e2c52ee72ac5a97504d67898b8ee0e556011d8bbcdf4c8` | 0 |
| testfuzz/src/main/java/org/hyperledger/besu/testfuzz/InternalClient.java | 1529 | `7f33a8aa7a2fe07782b3523a23e6d106f8155c4f5e96853ff4e13ba3e4ec43c5` | 0 |
| testfuzz/src/main/java/org/hyperledger/besu/testfuzz/P256VerifyCorpusGenerator.java | 10775 | `4c60601fa145b119bba82dd37ca493e0b61afd1100ec10cbde9d26f7851837d0` | 0 |
| testfuzz/src/main/java/org/hyperledger/besu/testfuzz/P256VerifyFuzzTarget.java | 36050 | `ce4623a7ed165138861a3b8ec168ed5fb10994e4f962be52ee00e9e10240a704` | 0 |
| testfuzz/src/main/java/org/hyperledger/besu/testfuzz/P256VerifySubCommand.java | 6480 | `3e501bf0a07ba71a61bad69dc4f73f4d98dc37c88918212438b6abda1ac83728` | 0 |
| testfuzz/src/main/java/org/hyperledger/besu/testfuzz/SingleQueryClient.java | 2913 | `e873c4fc585e5dc6bb6436263840d0a1d3465bcbc2faa82c74b3aa73da4dd8e5` | 0 |
| testfuzz/src/main/java/org/hyperledger/besu/testfuzz/StreamingClient.java | 1675 | `160091b60b25d4efa35a80af690a8239dbf6e7563db346e6839365d87d04528d` | 0 |
| testfuzz/src/main/java/org/hyperledger/besu/testfuzz/VersionProvider.java | 1657 | `021ccb0fdd14ad2fbdcc5a354864faea36fd9911c07dd7e6b5d71dfcf633757c` | 0 |
| testfuzz/src/main/java/org/hyperledger/besu/testfuzz/javafuzz/Corpus.java | 13728 | `2bb1458c2c3809d4b6bba747ef43cf9c672951cabd214f640a7e6f91289808b2` | 0 |
| testfuzz/src/main/java/org/hyperledger/besu/testfuzz/javafuzz/FuzzTarget.java | 1028 | `8d953f25eb32c105dc2f4ca3ae13cada5e2bc9370626b573cf024d59e84661dd` | 0 |
| testfuzz/src/main/java/org/hyperledger/besu/testfuzz/javafuzz/Fuzzer.java | 10058 | `4a84697b2487f2567532a9c05ae88a9add587a5fc25d473ebe1ee9ca3776b40f` | 0 |
| util/build.gradle | 2717 | `d5d8c539e34da4fab9dc0954caff93aa0e3c1d2cb97fdbaa56c7a8ce5e9179ab` | 0 |
| util/src/main/java/org/hyperledger/besu/util/BesuVersionUtils.java | 4638 | `04da9b1f6166c77e590add595008928cf0f4840ee1f78b92317a4547b275014a` | 0 |
| util/src/main/java/org/hyperledger/besu/util/EndianUtils.java | 1545 | `629fd01cdf73c232be4c5681ef1e8706f0ca0559f2376b96717896beed631db0` | 0 |
| util/src/main/java/org/hyperledger/besu/util/ExceptionUtils.java | 1201 | `6b88b5995a7e4c8963afd83f88630aa8e7a2894bae453f0ddd79c95e4a964e17` | 0 |
| util/src/main/java/org/hyperledger/besu/util/FutureUtils.java | 4986 | `46689afec8d9772f4b8fef780d3a658762fa3c9b84523e5e6190a73b8c7ee4f0` | 0 |
| util/src/main/java/org/hyperledger/besu/util/HexUtils.java | 1739 | `1590b55c2212342ad51bae90e109d150b0fcddda9f8b49e4c66f0c809ba3f147` | 0 |
| util/src/main/java/org/hyperledger/besu/util/IllegalPortException.java | 931 | `3974abd589e4de660ab9fb3bcfc27e14808612cb36a72e0bc89bfd68d83ae942` | 0 |
| util/src/main/java/org/hyperledger/besu/util/InvalidConfigurationException.java | 974 | `8e9e1c227661298e8dcbffe7e0b22d51d6d4919646a4fa425db25b18b612d5f2` | 0 |
| util/src/main/java/org/hyperledger/besu/util/LimitedSet.java | 2106 | `fce7cd718c4bd72b62781817c79fc46591bf17c86ec0ee9dc273f00b7b26630f` | 0 |
| util/src/main/java/org/hyperledger/besu/util/Log4j2ConfiguratorUtil.java | 4399 | `d6768e117d98c0143fd0bf9dd8267e21e8b4f0e66cd1931d9f090b819a5f1511` | 0 |
| util/src/main/java/org/hyperledger/besu/util/LogConfigurator.java | 2011 | `91e3bf326dfffc1075ddad99d373e2eea2599037d1abc6b77f47af67ee8099df` | 0 |
| util/src/main/java/org/hyperledger/besu/util/NetworkUtility.java | 8174 | `35c6119f25d88a99facd6f73496ca1f844b75bd088c60f5d5c2db62759c65acd` | 0 |
| util/src/main/java/org/hyperledger/besu/util/OrderStatistics.java | 4737 | `d856fbd51c33b772917d05add91629fd5e28475c7e8ee7076c78c0797f22d2dd` | 0 |
| util/src/main/java/org/hyperledger/besu/util/Preconditions.java | 1360 | `dd3bd5f7ac97face8ecb75b5aaba11ab88ca8894de06e8fb96855259ee7b7364` | 0 |
| util/src/main/java/org/hyperledger/besu/util/Subscribers.java | 5405 | `67cfc3f5398a728d7c9a2091f39ba2172ea35e9d129f2a7833ef332d2fcb4f16` | 0 |
| util/src/main/java/org/hyperledger/besu/util/cache/BiToIntFunction.java | 1295 | `ab947c85da8dc18c96db137c7b793687c2804d434986f0712870f42d36649990` | 0 |
| util/src/main/java/org/hyperledger/besu/util/cache/MemoryBoundCache.java | 3247 | `00b8f5814ce7a31321571816649ff00687e4cb3e18f0b1e4de3df3e2425a6e2c` | 0 |
| util/src/main/java/org/hyperledger/besu/util/era1/Era1Accumulator.java | 863 | `621e16bdb5dafa4d4bb96a010ed98d687c9c0bc33b09e3c6ebf4908647c72342` | 0 |
| util/src/main/java/org/hyperledger/besu/util/era1/Era1BlockIndex.java | 983 | `d29285029bca0f09a9c555014ef7a577b5557008631453587b3375d66770180a` | 0 |
| util/src/main/java/org/hyperledger/besu/util/era1/Era1ExecutionBlockBody.java | 884 | `b087b34fbcd932600d407e33d4630edb6ca932e3f54f28e58bf05ed29cca43b3` | 0 |
| util/src/main/java/org/hyperledger/besu/util/era1/Era1ExecutionBlockHeader.java | 897 | `c32adaa599c6a3178095d8346ea004d9c14990688954e31cba2aab72404f0403` | 0 |
| util/src/main/java/org/hyperledger/besu/util/era1/Era1ExecutionBlockReceipts.java | 935 | `6297348f248f8543adef38d9f7225503342c5706b62951c34cdb698c8673e360` | 0 |
| util/src/main/java/org/hyperledger/besu/util/era1/Era1Reader.java | 6262 | `46ada598d3abe08fb1c9df844e6551d6fde03d7f84a3bba20056a4f0adad5794` | 0 |
| util/src/main/java/org/hyperledger/besu/util/era1/Era1ReaderListener.java | 1992 | `83cf293e3c62ad48e89d0b2a608bf90b918ac6cea9590407cc7d5b61700fc9cf` | 0 |
| util/src/main/java/org/hyperledger/besu/util/era1/Era1TotalDifficulty.java | 908 | `92f3d3a81503b0828f53eaabdfc984b739a6aeb2649590493fd1bb051f08d527` | 0 |
| util/src/main/java/org/hyperledger/besu/util/era1/Era1Type.java | 2603 | `b2fe0d2d9b1a7bd21ded1eb892b8e265266c83e00c53bfd144465a7d667d2078` | 0 |
| util/src/main/java/org/hyperledger/besu/util/io/InputStreamFactory.java | 1279 | `2a9fb9a1a6bf4d67a5b4509a770f1c5fe414bb3eafa71a6f5fda63f0308711eb` | 0 |
| util/src/main/java/org/hyperledger/besu/util/io/OutputStreamFactory.java | 1318 | `68e147c9ab7d5f6b29a11dc0006014b9b18feb3d91732b8e2110d109ca6f24ea` | 0 |
| util/src/main/java/org/hyperledger/besu/util/io/RollingFileReader.java | 3747 | `960153c9060035abf9eec2c3e9609cc2e8651e65def6edb950876c6743c0ecbc` | 0 |
| util/src/main/java/org/hyperledger/besu/util/io/RollingFileWriter.java | 3511 | `9949bbcc3cabd9127cd25e47214ffcfbcf96fd8ddb1bf2c03067e780c51d6168` | 0 |
| util/src/main/java/org/hyperledger/besu/util/log/FramedLogMessage.java | 2568 | `9d3dfb2eb5c5ca6e1d7caaac8eed5257828bb37104c39aff0f957917c979d65a` | 0 |
| util/src/main/java/org/hyperledger/besu/util/log/LogUtil.java | 4132 | `b160cf8606de71866a07b80567c1c0550a1545160975a6e10238da19eaaa16a3` | 0 |
| util/src/main/java/org/hyperledger/besu/util/log4j/plugin/BesuLogMessageConverter.java | 2618 | `92fea8eedb1dc86bb771543b2e9dfd4efb802fb6bd462878b66dc531852ca6c2` | 0 |
| util/src/main/java/org/hyperledger/besu/util/log4j/plugin/StackTraceMatchFilter.java | 4403 | `83a9d2d299a63fdf7a8cd638b25bc160ab287cbeebb314783b01a7f0939a521f` | 0 |
| util/src/main/java/org/hyperledger/besu/util/number/ByteUnits.java | 1031 | `608f32205eded6fc038bdc27d0666b01f49bcbc12e7aba8b2bbe089fd799f8ab` | 0 |
| util/src/main/java/org/hyperledger/besu/util/number/Fraction.java | 2779 | `2537f2b02c29965c32dc793bedb46bd1c3f50eecab4e01240be289b7358f59a9` | 0 |
| util/src/main/java/org/hyperledger/besu/util/number/Percentage.java | 2350 | `60add940340edc722065fec936bc05ac921a4670770a7d6300ae1c3b97fa81b9` | 0 |
| util/src/main/java/org/hyperledger/besu/util/number/PositiveNumber.java | 2275 | `a5a2bc3ef00eeec71fb1f6ae092145cd36bef2b770a5060672d314fc2675fddb` | 0 |
| util/src/main/java/org/hyperledger/besu/util/platform/PlatformDetector.java | 9396 | `a4c1dc6f7fdf318efe81bc38a21d4814bf4af79a812802249b42bdd3040f37c3` | 0 |
| util/src/main/java/org/hyperledger/besu/util/snappy/SnappyFactory.java | 2067 | `707008f62a8f57e8d46cf59b590b61d8d15c0f1caf0a815e3edccea0d4bc80e7` | 0 |
| util/src/main/java/org/hyperledger/besu/util/ssz/Merkleizer.java | 3826 | `e846de3b675909919ea91bf41ed162b99abcfc305b444ab16da246a50bf7a0eb` | 0 |
