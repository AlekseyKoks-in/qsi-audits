# Zcash has already shipped quantum recoverability. Here is what the code still contains.

**13 codebases, 3 495 parsed files, 793 inventory rows, 267 breakable by
Shor's algorithm, 3 post-quantum.** Each audited at a pinned commit on 2026-10-29, each bundle signed and
verifiable offline without contacting me: https://github.com/AlekseyKoks-in/qsi-audits

## The thing most people have not noticed

Zcash deployed a consensus change for quantum recoverability **three months ago**. ZIP 258, status **Final**, set
`ACTIVATION_HEIGHT (NU6.3)` on Mainnet to **3 428 143** with `CONSENSUS_BRANCH_ID 0x37A5165B`; that
block was mined at **2026-07-28 14:07:23 UTC**, about 93 days ago. NU6.3 introduced the **Ironwood pool** and
deployed ZIP 229 (version 6 transaction format), **ZIP 2005 (Ironwood Quantum Recoverability)** and ZIP 2006
(Restricting Transfers into the Orchard Pool).

Compare the state of the same question on Bitcoin, where BIP-360 (Pay-to-Merkle-Root) is a Draft that explicitly
defers post-quantum signatures to a separate unwritten proposal, and BIP-361's legacy-signature sunset is a Draft
that "follows the implementation of any post-quantum output type" — an output type that does not exist. On that
comparison Zcash is not behind. It is the furthest ahead of any major chain, and it got there without a
post-quantum primitive, by making funds *recoverable* after a break instead of trying to prevent one.

## What ZIP 2005 actually says, in its own words

> An adversary able to compute discrete logarithms (in fact, a single discrete logarithm is sufficient) could
> cause arbitrary inflation or steal users' funds.

> Critically, the note commitment algorithms used by the Sapling and Orchard shielded protocols are not
> post-quantum binding. This means that even if the proof system were upgraded to one that is believed to be
> secure against quantum computers, and even if the note commitment tree were to be reconstructed (from public
> information) to use a suitable hash function, it would still be possible for a quantum or
> discrete-logarithm-breaking adversary to forge and spend notes that are not actually in the commitment tree —
> thus breaking the Balance property.

> Recovery would not be possible for funds still in the Sprout, Sapling, or Orchard pools; all such funds would
> be inaccessible after their respective protocols are disabled.

Three consequences, each of which cuts against the usual framing of quantum risk to a privacy coin.

**The failure mode is the money supply, not the privacy.** Addressing quantum attacks on privacy is an explicit
*non-requirement* of ZIP 2005. An amount committed with a Pedersen commitment stays hidden against any adversary
with any computer, because hiding is information-theoretic; it is *binding* that rests on the discrete logarithm.
The realistic quantum failure is therefore undetectable inflation of a shielded pool, not the retroactive
unmasking of past payments.

**Replacing the proof system would not have been enough.** The commitments had to change too. That is why ZIP 2005
alters note derivation now, years ahead of any decision about a post-quantum proof system, and why it needed a new
pool rather than a patch to Orchard.

**Recoverability is not security.** ZIP 2005 says so itself: the feature "does not make the Orchard protocol
secure against quantum attacks". It buys an orderly evacuation, not immunity.

## The deadline that is actually a week away is not a quantum one

NU7 is next: ZIP 259, status Proposed, `ACTIVATION_HEIGHT` Mainnet **3 543 405**,
`CONSENSUS_BRANCH_ID 0x77190AD9`. At height 3 535 207, reached 2026-10-29 22:57 UTC, that is **8 198
blocks** away — about 7.1 days at the current 75-second target spacing.

NU7 carries **no post-quantum content**: it deploys ZIPs 200, 207 Rev 2, 214 Rev 3, 218, 235, 237, 2003 and 2008 —
faster blocks, the Network Sustainability Mechanism, action limits, and the end of version 4 transactions. But that
last item matters here, because Sprout transfers can only be represented in version 4 transactions, so **funds
remaining in the Sprout pool become unspendable** at NU7.

That is the mechanism ZIP 2005 is written about, happening on schedule to a different pool. Zcash does close pools.

## Is the ecosystem following?

Yes — and this is the part I expected to find missing and did not. Counting source files that reference Ironwood in
a fresh clone of each repository:

| Codebase | Source files referencing Ironwood | Source files | Share |
|---|---:|---:|---:|
| `librustzcash` | 117 | 359 | 33% |
| `orchard` | 12 | 59 | 20% |
| `zebra` | 91 | 745 | 12% |
| `lightwalletd` | 12 | 47 | 26% |
| `zcash-android-wallet-sdk` | 52 | 497 | 10% |
| `zcash-swift-wallet-sdk` | 63 | 325 | 19% |
| `zodl-android` | 87 | 1 993 | 4% |
| `zingolib` | 85 | 237 | 36% |

Every one of the eight has it. `orchard` ships `IronwoodVersion`, `IronwoodDomain` and `IronwoodNoteEncryption` with
the lead-byte `0x03` note plaintext ZIP 2005 specifies; `librustzcash` carries a dedicated `zcash_pool_migration`
crate and PCZT roles with `create_ironwood_proof` and `sign_ironwood`. The migration is being built broadly, not by
one team.

One observation, scoped carefully. ZIP 326 "NU6.3 Consequences for Wallets" — the document that tells wallets how
to handle the upgrade — is still a **Draft**, three months after the consensus change it describes went live. The
`use_qsk` key distinction it names, which decides whether an account's notes are recoverable at all, does not
appear under that identifier anywhere in the code I read. That is consistent with the ZIP still being a Draft and
is not by itself a defect in any implementation. It is the kind of gap between a shipped consensus rule and
settled wallet guidance that an inventory is for, and it is worth someone's attention before it becomes one.

## What the code contains

| Codebase | Commit | Files | Rows | Shor-breakable | Post-quantum | Before the fix |
|---|---|---:|---:|---:|---:|---:|
| `zcash/orchard` | `616a669d` | 49 | 69 | **41** | 0 | 1/0 |
| `zcash/sapling-crypto` | `88a7946b` | 37 | 57 | **36** | 0 | 16/15 |
| `ZcashFoundation/reddsa` | `04e973bc` | 15 | 12 | **4** | 0 | 1/1 |
| `zcash/halo2` | `3442dd33` | 100 | 73 | **45** | 0 | 2/2 |
| `zcash/librustzcash` | `8672a4b2` | 333 | 156 | **23** | 0 | 46/19† |
| `ZcashFoundation/zebra` | `147a6a8b` | 439 | 148 | **65** | 0 | 27/14† |
| `zcash/lightwalletd` | `4abfe9cd` | 34 | 8 | **3** | 0 | 8/3† |
| `zcash/zcash-android-wallet-sdk` | `a95780ac` | 350 | 46 | **2** | 0 | 14/2† |
| `zcash/zcash-swift-wallet-sdk` | `4895ee05` | 205 | 45 | **2** | 0 | 12/2† |
| `zodl-inc/zodl-android` | `229dd3bf` | 1 609 | 5 | **0** | 0 | 5/0† |
| `ZcashFoundation/frost` | `0966bd15` | 61 | 59 | **33** | 0 | 57/33 |
| `zingolabs/zingolib` | `81d79977` | 205 | 86 | **3** | 3 | — |
| `tachyon-zcash/tachyon` | `6cdaebcc` | 58 | 29 | **10** | 0 | — |

† Figures published before today, in the Zcash grant application thread, and corrected here. Rows
without a dagger are codebases audited for the first time today; their "before" is the same commit measured with
the old registry a few hours earlier, and was never published.

Each row is an algorithm found at a line of source, or a crypto-bearing dependency named in a manifest, and the
report distinguishes the two. **5 of the 793 rows are something else again**: OpenPGP primary keys and
subkeys committed to the repositories — maintainers' release-signing keys, in `zebra` and both wallet SDKs. They are
real cryptography and they do have to migrate, since a CRQC forges release signatures as readily as transaction
ones, but they are not cryptography these projects implement, and I am naming them rather than letting them sit
inside a headline. Each carries `usage: OpenPGP primary key` or `OpenPGP subkey` in the report, so anyone can split
them out. `frost` is here because ZIP 2005 requires its scheme to remain compatible with FROST
threshold multisignatures.

The inventory now maps onto the attack list ZIP 2005 writes out for itself — forged Groth16 or Halo 2 proofs,
forged value-commitment openings or binding signatures, forged RedJubjub or RedPallas spend authorizations, forged
ECDSA-over-secp256k1 for the transparent pool — and it says, per repository and per line, where each of those
primitives actually is. ZIP 2005 also notes that one discrete logarithm on BLS12-381 suffices against Sprout and
Sapling, and one on Pallas/Vesta against Orchard and Ironwood.

**3 post-quantum rows across the whole stack, and all of them are in one wallet's transport layer.**
Not one of these 13 codebases ships a post-quantum signature, note commitment or proof system. That is
not a criticism, and after reading ZIP 2005 it is not even a surprise: recoverability was deliberately designed to
need no post-quantum primitive, so that it could ship before one was chosen. It is the baseline the eventual
migration will be measured against.

## Tachyon, measured rather than described

`tachyon-zcash/tachyon` is the successor shielded protocol. Its own tracking issue lists **eleven ZIPs, none of
them checked off**, and the 2026-10-26 milestone is "ZIP drafts ready for audit". So this is a measurement of a
protocol still being written, and it should be read that way.

What is in it today: **29 inventory rows from 58 parsed files, 10 of them Shor-breakable and
0 post-quantum.** The composition is the interesting part — 14 Poseidon rows, 9 RedDSA, and a
Pedersen commitment. Poseidon is the one primitive here whose hardness is not group hardness, so a protocol built
on it leans in the right direction; but spend authorization is still RedDSA and the value commitment is still
Pedersen, both of which rest on the discrete logarithm. A protocol often described as quantum-resistant does not
yet contain a single post-quantum primitive. That is not a criticism of unfinished work — it is the baseline, and
it is the number that should be re-measured when those eleven ZIPs land.

Of the live stack, `zingolib` is the only codebase here with any post-quantum material at all: 3 rows,
`X25519MLKEM768` among them, which arrives through its transport stack rather than through the Zcash protocol.
A wallet reaches post-quantum TLS years before it reaches a post-quantum note.

## A defect in my own tool, published with the finding

Before 2026-10-29 this inventory could not see Zcash's cryptography at all. Auditing `zcash/orchard` produced
**1 inventory row** — AES-256 — and **0 Shor-breakable rows**, for the protocol whose
Balance property rests entirely on discrete logarithms in the Pallas group. The cause was not a parsing failure.
The algorithm registry had no entry for Sinsemilla, RedDSA, Halo 2 or Poseidon, so the scanner opened every file
and recognised nothing in it.

Four registry entries were added, with detection patterns written against the real source rather than from memory,
and a positive and a negative test case each; the Pedersen pattern was extended to the `ValueCommit*` spelling that
§ 5.4.8.3 of the protocol specification defines as a homomorphic Pedersen commitment. Poseidon is recorded as
`grover_reduced`, not Shor-breakable, because its hardness is not group hardness — getting that distinction wrong
in either direction would misstate the risk.

Across the stack the new entries produced: Halo 2 (IPA) (72), Pedersen commitment (52), RedDSA (27), Sinsemilla (24), Poseidon (21). **9 of the 11 re-measured codebases
gained rows, and the totals went from 189 rows / 91 Shor-breakable to 793 / 267.** The
before-state is archived and every re-audit is pinned to the same commit as the original, so the difference is
attributable to the registry and to nothing else.

I am publishing the defect with the measurement because a reader who can verify the second deserves to know the
first. **Every figure I published for a Zcash codebase that implements shielded cryptography understated it.**

Two did not move, and they are exactly the two that should not have. `lightwalletd` is unchanged at 8 rows —
it relays shielded data rather than implementing the protocol. `zodl-android` is unchanged at 5 rows — it is a
Kotlin wallet whose cryptography lives in the Rust SDK it depends on, which is why the SDKs moved and the app did
not. Neither contains Sinsemilla, RedDSA or Halo 2 to find. Those two are the control that tells me the new
patterns are reading the code rather than firing on everything.

## Method

Each audit runs offline against a pinned commit with submodules materialised — a shallow clone leaves submodules
empty, and a scanner then reports a clean result for code it never opened. Each bundle carries `report.json`, a
CycloneDX CBOM, SARIF, and an Ed25519 signature over a canonical form of the report; `verify.py` in the repository
checks all of them with no network access. Where an analyst corrected a finding, the decision is signed into the
report and replayed on re-audit instead of being discarded.

Limits, stated plainly: `.cairo`, `.move` and `.vy` have no analyzer. A file-name signal is weaker evidence than a
call site and is recorded as such. The byte budget is 50 MB per audit, and when it binds the report names what
did not fit. The Ironwood counts above are a reference count, not a conformance test: they show that a codebase
knows the pool exists, not that it handles it correctly.

---

*Aleksey Koksin — Quantum Security Intelligence. Bundles, signatures and verification: https://github.com/AlekseyKoks-in/qsi-audits*
