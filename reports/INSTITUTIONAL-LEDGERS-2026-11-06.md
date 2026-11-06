# Post-quantum readiness of institutional ledgers and bank-facing platforms (2026-11-06)

Seven open-source platforms that banks, market infrastructures and stablecoin issuers build on, audited at a pinned
commit with QSI. Each line below was checked against the source, not only against the scanner's output. The signed
bundles (report, CycloneDX CBOM, SARIF) are in `studies/institutional/<name>/` (kept apart from the portfolio totals in the README), verifiable offline with `python3 verify.py studies/institutional/*`.

This is not a vulnerability report: nothing here is exploitable today. It answers the question a supervisor or a
bank's CISO now asks (PCI DSS v4.0 req. 12.3.3, the EU coordinated PQC roadmap's inventory by end-2026, the US
Treasury's focus on banks' software suppliers): *where does public-key cryptography protect what, and what has
already moved?*

## Summary

| Platform | Commit | Own-code rows | Shor-breakable | Post-quantum present | The exposure that matters first |
|---|---|---:|---:|---|---|
| Canton (Digital Asset) | `4eab7a0` | 74 | 35 | **ML-DSA-65 signing** (experimental flag) | View **encryption** is ECIES-P256 or RSA-OAEP only — no ML-KEM |
| Arc (Circle) | `6e76402` | 37 | 12 | **SLH-DSA precompile** | Consensus votes and proposals signed with Ed25519 |
| Hyperledger Fabric + fabric-lib-go | `13ef9e5` / `f8b4f4a` | 39 + 37 | 15 + 24 | **Hybrid TLS by Go default** (X25519MLKEM768) | Endorsements, orderer signatures and MSP identities: ECDSA/Ed25519/RSA |
| Hyperledger Besu | `1f1ebc2` | 72 | 37 | none | RLPx peer encryption is ECIES on secp256k1; transactions ECDSA |
| Corda (R3) | `8003358` | 23 | 16 | none | Default identity Ed25519, TLS ECDSA P-256 |
| Open Bank Project (TESOBE) | `6a4a13e` | 32 | 10 | none | Gateway tokens with core-banking session data encrypted with JWE RSA-OAEP-256 |

## Two different problems: signatures and encryption

**Encryption is the urgent one.** Anything encrypted with ECDH, ECIES or RSA today can be recorded now and decrypted
once a cryptographically relevant quantum computer exists ("harvest now, decrypt later"). Transaction data in these
systems has a long confidentiality life, so it is exposed today.

- **Canton.** Views are encrypted end-to-end to participants' keys and pass through sequencers, which may be run by
  other organisations and retain what they relay. The supported schemes are `EciesHkdfHmacSha256Aes128Cbc` (P-256;
  `community/base/.../crypto/Encryption.scala:380`, JCE "ECIESwithSHA256andAES-CBC" in `JcePureCrypto.scala`) and
  `RsaOaepSha256` for KMS providers (`config/CryptoProvider.scala:153`). Digital Asset's public position (forum, August
  2026) expects post-quantum TLS to "block many store-and-decrypt style attacks". TLS protects the link, not the
  payload a sequencer stores. Only an ML-KEM (or hybrid) `EncryptionAlgorithmSpec` closes that.
- **Besu.** The devp2p RLPx handshake is ECIES on secp256k1 (`ethereum/p2p/.../rlpx/handshake/ecies/ECIESHandshaker.java:174`).
  For a private, permissioned network, which is how banks deploy Besu, the recorded peer traffic is the asset.
- **Open Bank Project.** `CertificateUtil.scala:232` encrypts gateway-login JWTs with RSA-OAEP-256. They carry
  `cbs_token`, `cbs_id` and `session_id` (`GatewayLogin.scala:105`, `dauth.scala:94`).
- **Fabric is the exception.** Its `go.mod` requires Go 1.27.3, and no production `tls.Config` sets
  `CurvePreferences` (`internal/pkg/comm/config.go:227`, `creds.go:43`, `common/fabhttp/tls.go:44`). So TLS 1.3
  between Fabric components already negotiates X25519MLKEM768. One configuration change, such as pinning curves for a
  FIPS profile, would silently remove it.

**Signatures have a longer runway but a slower migration.** A forged signature needs the quantum computer to exist,
but ledgers keep signatures forever, and identities, certificates and HSM key slots take years to rotate.

- Canton has done the hard architectural part: `SigningKeySpec.MlDsa65` (`Signing.scala:1019`, BouncyCastle).
- Arc ships an SLH-DSA verification precompile (`crates/pq-precompile/src/lib.rs:22`). Its consensus types still
  sign with Ed25519 (`crates/types/src/signing.rs:21`, `ssz/v1/vote.rs:21`, `proposal_part.rs:26`), which Circle's
  published roadmap schedules for a later phase.
- Corda's `CryptoService` takes the scheme as a parameter, but `Crypto.kt` lists no post-quantum scheme.
- Fabric's BCCSP is a pluggable provider with ECDSA, Ed25519 and RSA only (`bccsp/sw/*`, `bccsp/pkcs11/*`).
- Besu signs transactions with ECDSA secp256k1, a protocol rule it shares with Ethereum. Its BLS12-381 rows are the
  EIP-2537 precompiles.

## Method and limits

Static review of the source tree at the commit shown, with test, fuzzing, benchmark and example code excluded.
Vendored and third-party code is reported separately from the project's own code. Counts are inventory rows (one per
algorithm per location), not call sites. The Fabric hybrid rows are inferred from the Go toolchain default and are
marked low confidence. A build that sets `GODEBUG=tlsmlkem=0` would not have them. Private submodules and closed
components (for example Canton's enterprise modules, Circle's custody stack) were not available and are not covered.

*QSI — quantum-readiness inventory of cryptography. Contact: alekseykoksin@gmail.com.*
