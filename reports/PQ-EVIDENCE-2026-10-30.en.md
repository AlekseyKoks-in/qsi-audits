# Who has begun the post-quantum migration — graded by the strength of the evidence

53 codebases, measured 2026-10-30. The predecessor of this report answered the question with one criterion:
does the codebase contain a `pqc` or `hybrid` inventory row. That treats a dependency declaration, a file name and
a line of source as the same fact. They are not, and two of that report's claims rested on the weakest of the
three. So here the same question is answered in four states, each named after **what the evidence actually is**.

| State | Codebases | What it means |
|---|---:|---|
| **Implemented** | 6 | a post-quantum primitive appears at a line of source code |
| **Named only** | 1 | the evidence is a file's *name*; the reports mark this `confidence: low` |
| **Declared only** | 4 | a manifest or the toolchain's default makes the capability available (Go 1.24+ crypto/tls); nothing in the project chose it |
| **Absent** | 42 | no post-quantum row at all |

**11 of 53 have started on the loosest reading, and 6 on the only reading that means
code.** Not one of the four states is a statement about a vendor: an absent row means absent *in the audited
scope at a pinned commit*, and work may sit in another branch, repository or closed source.

## Implemented — a post-quantum primitive at a line of source

| Codebase | PQ rows | Shor-breakable | What, and where the strongest row sits |
|---|---:|---:|---|
| `rustls` | 9 | 29 | X25519MLKEM768 ×6, SecP256r1MLKEM768 ×2, SecP384r1MLKEM1024 — `rustls-aws-lc-rs/src/kx.rs:59` |
| `openpgpjs` | 8 | 32 | ML-DSA ×3, ML-KEM ×3, PQC library ×2 — `src/crypto/public_key/post_quantum/noble_post_quantum.ts:10` |
| `trezor-firmware` | 7 | 74 | ML-DSA ×6, SLH-DSA — `core/embed/sec/mcu_attestation/inc/sec/mcu_attestation.h:24` |
| `bitwarden-sdk` | 5 | 13 | ML-DSA ×3, PQC library ×2 — `crates/bitwarden-crypto/src/signing/cose.rs:7` |
| `zingolib` | 3 | 3 | X25519MLKEM768 ×2, PQC library — `zingo-netutils/src/crypto.rs:25` |
| `coinbase-cb-mpc` | 2 | 93 | ML-KEM ×2 — `src/cbmpc/crypto/mlkem768.cpp:8` |

`trezor-firmware` is the one with the strongest claim of all: ML-DSA in MCU attestation and **SLH-DSA at
`core/embed/sec/image/boot_header.c:30`, in the root of trust**, beside Ed25519 at line 81 of the same file — a
migration visibly in progress rather than announced. `coinbase-cb-mpc` is the opposite shape: ML-KEM-768 is
implemented in `mlkem768.h` and `mlkem768.cpp` and included only by its own translation unit, its CMake file and
its unit test, so the key-share backup path that would need it does not reach it. Built, not wired.

## Named only — the evidence is a file name

| Codebase | PQ rows | Shor-breakable | What, and where the strongest row sits |
|---|---:|---:|---|
| `signal-desktop` | 2 | 0 | ML-KEM ×2 — `ts/sql/migrations/1470-kyber-triple.std.ts` |

Both rows come from the names of SQL migrations. A migration called `85-add-kyber-keys.std.ts` says this
application's *schema stores* Kyber keys; it does not say this codebase implements ML-KEM, and the cryptography it
leans on lives in native libraries outside the audited TypeScript tree. The file-name signal exists for a good
reason — `trezor-firmware/crypto/pbkdf2.c` defines PBKDF2 rather than calling it, so no call-site pattern reaches
it — and the reports mark it `confidence: low`. Counting it as "has started" is where the predecessor report went
furthest beyond its data.

## Declared only — a manifest, and nothing more

| Codebase | PQ rows | Shor-breakable | What, and where the strongest row sits |
|---|---:|---:|---|
| `rage` | 3 | 13 | PQC library ×3 — `Cargo.lock` |
| `foundry` | 1 | 17 | X25519MLKEM768 — `Cargo.toml:494` |
| `lightwalletd` | 1 | 3 | X25519MLKEM768 — `frontend/rawrequest.go:60` |
| `scroll` | 1 | 7 | X25519MLKEM768 — `bridge-history-api/cmd/api/app/app.go:67` |

## A correction to the predecessor report, and the defect behind it

That report said X25519MLKEM768 "appears in `rustls` and in `foundry` (through the same TLS library)". For
`foundry` that is a dependency inference and was stated as one. For `rustls` it is circular: `rustls` *is* the TLS
library, and the only row the audit had for it was that same inference, recorded against
`bogo/Cargo.toml` — a **test-harness manifest**.

The claim happens to be true. `rustls` declares the group in its own source, at `src/crypto/kx/mod.rs`, beside
`MLKEM512`, `MLKEM768`, `MLKEM1024` and `secp256r1MLKEM768`. But my audit did not establish it, and a claim that
is true by luck rather than by measurement is one I would rather retract than keep.

**The cause was a hole in the registry, and it was systematic.** Every hybrid KEM entry — X25519MLKEM768,
SecP256r1MLKEM768, SecP384r1MLKEM1024, X25519Kyber768Draft00, and the two SSH hybrids `mlkem768x25519-sha256` and
`sntrup761x25519-sha512` — carried a TLS or SSH group *name* and **no code pattern at all**. A library that
declares the group in source was invisible to the one evidence class that matters most. This is the third
instance of the same class in this repository: HKDF named 75 times inside `rustls` and reached by no call-shaped
pattern, RedDSA named 27 times in `reddsa`'s doc comments and never in its code, and now the hybrids.

Patterns were written from the real spellings, which include `config_x25519mlkem768`, `SeparateX25519Mlkem768`
and `SSL_GROUP_X25519_MLKEM768` — so they carry no leading word boundary, because in each of those the preceding
character is itself a word character. Six entries, six positive and six negative test cases, and a prediction
written down before the measurement: on re-audit `rustls` should move out of *Declared only*.

**It did.** Re-audited at the same commit, `rustls` went from **1 post-quantum row to 9** — including
`rustls/src/crypto/kx/mod.rs:563`, the declaration the audit had previously missed, and **SecP256r1MLKEM768 and
SecP384r1MLKEM1024, two groups the registry had never detected anywhere**. Its parsed-file count and its Shor
count did not move, so the whole change is the new detection and none of it is a false positive. It now sits in
*Implemented*, which is where it belonged; `foundry` and `zingolib` did not move, which is also right, since their
rows really are a manifest and a single provider line.

## Absent — the largest exposures with nothing post-quantum

| Codebase | Shor-breakable rows |
|---|---:|
| `trustwallet-wallet-core` | 294 |
| `bitbox02-firmware` | 113 |
| `agave` | 111 |
| `jade` | 107 |
| `monero` | 99 |
| `fireblocks-mpc-lib` | 88 |
| `libwally-core` | 81 |
| `bitgo-mpc` | 68 |

Across all 53 codebases, 1 942 inventory rows fall to Shor's algorithm. The point of grading the other
column is that "has started" and "is protected" are different questions, and only the first one is measurable
from source at all.

---

*Every figure recomputable from the bundles in this repository; `verify.py` checks them with no network access.*
