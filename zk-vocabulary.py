#!/usr/bin/env python3
"""Does your scanner have a word for the cryptography in this tree?

    python3 zk-vocabulary.py                          # what zero-knowledge primitives are in .
    python3 zk-vocabulary.py --repo /path/to/checkout
    python3 zk-vocabulary.py --against results.sarif  # ...and which of them your tool failed to report
    python3 zk-vocabulary.py --json
    python3 zk-vocabulary.py --self-test              # check the patterns before you trust their silence

No dependencies, no network, no git. Exit status 0 when nothing is wrong, 1 when something is, so it can go
straight into CI.

Why this exists
---------------
A cryptographic inventory can fail in a way that looks exactly like a clean result. Not a crash, not a parse
error: the scanner opens every file, recognises nothing, and reports that the code contains no quantum-vulnerable
cryptography.

That happened to this author's own tool, on the worst possible target. Auditing `zcash/orchard` — the protocol
whose Balance property rests entirely on discrete logarithms in the Pallas group — produced **one inventory row
(AES-256) and zero Shor-breakable rows** from 49 parsed files. The cause was not detection logic. The algorithm
registry had no entry for Sinsemilla, RedDSA, Halo 2 or Poseidon, so there was no word in the vocabulary for any
of it. With four entries added, the same commit measures 69 rows and 41 Shor-breakable.

A vocabulary gap is invisible from the outside, because its output is indistinguishable from good news. This tool
is the generalisable half: it carries the vocabulary, and `--against` tells you whether your own tool shares it.

Two things it is careful about, which are the reason it is worth running rather than grepping
---------------------------------------------------------------------------------------------
**It says what a quantum adversary breaks, not merely that something is breakable.** For a commitment the answer
is *binding*, not hiding — a Pedersen commitment hides amounts information-theoretically, so committed values stay
secret against any computer, while a quantum adversary can open a commitment to a different value. The failure is
forged supply, not lost privacy. For a proof system the answer is *soundness*: accepted proofs of false
statements. Getting this backwards, in either direction, is how a report ends up recommending the wrong work.

**Poseidon is not Shor-breakable and is reported that way.** Its hardness is not group hardness. Filing it under
Shor would overstate the risk exactly as badly as missing Sinsemilla understated it.

A library that implements a primitive does not call it
-----------------------------------------------------
`ZcashFoundation/reddsa` names RedDSA, RedPallas and RedJubjub **27 times in doc comments and zero times in
code**: the code says `SpendAuth`, `Binding` and `SigType`. A call-shaped pattern finds every caller and misses
the implementation, so the crate that *is* RedDSA reported no RedDSA. The patterns below therefore include
declaration-shaped ones. If you write your own, test them against the library and not only against its consumers.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# Generated from the registry the published audits were produced with, so these are the patterns that did the
# measuring rather than a retyped approximation of them.
PRIMITIVES = {
    "sinsemilla": {
        "name": "Sinsemilla",
        "status": "vulnerable_shor",
        "attack": "shor",
        "basis": "elliptic_curve_dlog",
        "breaks": "binding",
        "consequence": "Forge a note that is not in the commitment tree, and spend it. Breaks Balance — the supply — not privacy. ZIP 2005 says the Sapling and Orchard note commitments are 'not post-quantum binding', so replacing the proof system does not fix this.",
        "patterns": [
            "\\b[Ss]insemilla\\w*"
        ],
        "sources": [
            "ZCASHSPEC",
            "ZIP2005",
            "SHOR1997"
        ]
    },
    "reddsa": {
        "name": "RedDSA",
        "status": "vulnerable_shor",
        "attack": "shor",
        "basis": "elliptic_curve_dlog",
        "breaks": "forgery",
        "consequence": "Recover the signing key and forge spend authorization. Re-randomizable keys give unlinkability, not quantum resistance.",
        "patterns": [
            "\\b(RedDSA|RedPallas|RedJubjub)\\b|\\breddsa::|\\b(SpendAuthSig|BindingSig)\\b",
            "\\bpub (?:trait|enum) SpendAuth\\b|\\bimpl(?:<[^>]*>)? SigType for\\b|\\bpub type Randomizer\\b"
        ],
        "sources": [
            "ZCASHSPEC",
            "ZIP2005",
            "SHOR1997"
        ]
    },
    "halo2-ipa": {
        "name": "Halo 2 (IPA)",
        "status": "vulnerable_shor",
        "attack": "shor",
        "basis": "elliptic_curve_dlog",
        "breaks": "soundness",
        "consequence": "Produce an accepted proof of a false statement. Zero knowledge is statistical and is not lost retroactively, so the exposure is forged value, not disclosed value.",
        "patterns": [
            "\\bhalo2(_proofs|_gadgets|_backend)?::|\\bHalo2\\w*|\\bParamsIPA\\b|\\b(Prover|Verifier)IPA\\b|\\bIPACommitmentScheme\\b"
        ],
        "sources": [
            "HALO2",
            "ZCASHSPEC",
            "ZIP2005",
            "SHOR1997"
        ]
    },
    "pedersen-commitment": {
        "name": "Pedersen commitment",
        "status": "vulnerable_shor",
        "attack": "shor",
        "basis": "elliptic_curve_dlog",
        "breaks": "binding",
        "consequence": "Open a commitment to a different value: forged amounts, hidden inflation. Hiding is information-theoretic, so amounts already committed stay hidden against any adversary. The risk is the supply, not the secret.",
        "patterns": [
            "\\bPedersenGens\\b|\\bPedersenCommitment\\b|\\bpedersen_commit\\w*|\\bValueCommit\\w*|\\b[Pp]edersen_?[Hh]ash\\w*"
        ],
        "sources": [
            "PEDERSEN1991",
            "ZCASHSPEC",
            "SHOR1997"
        ]
    },
    "poseidon": {
        "name": "Poseidon",
        "status": "grover_reduced",
        "attack": "grover",
        "basis": "hash",
        "breaks": "preimage/collision only",
        "consequence": "No Shor-type break: the hardness is not group hardness. Generic quantum search sets the margin, so the field size and sponge parameters decide it, not the algebra.",
        "patterns": [
            "(?:\\b|_)[Pp]oseidon\\w*"
        ],
        "sources": [
            "POSEIDON2019",
            "ZCASHSPEC",
            "SHOR1997"
        ]
    },
    "groth16": {
        "name": "Groth16",
        "status": "vulnerable_shor",
        "attack": "shor",
        "basis": "pairing",
        "breaks": "soundness",
        "consequence": "Produce an accepted proof of a false statement; pairing-based, and the trusted setup is a separate concern from this one.",
        "patterns": [
            "\\bverifyProof\\s*\\(\\s*(uint|\\[)|\\bGroth16Verifier\\b|\\bgroth16\\.(verify|fullProve|prove)\\b|\\bVerifyingKey\\b[^\\n]{0,80}\\bgamma2\\b"
        ],
        "sources": [
            "GROTH16",
            "EIP-197",
            "SHOR1997"
        ]
    },
    "bls12-381": {
        "name": "BLS12-381",
        "status": "vulnerable_shor",
        "attack": "shor",
        "basis": "pairing",
        "breaks": "forgery",
        "consequence": "Pairing and discrete-logarithm break: signatures forgeable, and any proof system over this curve loses soundness with it.",
        "patterns": [
            "\\bbls12_381\\b|\\bBLS12_381\\b|@noble/curves/bls12-381|\\bblst_\\w+|\\bBLS12_(G1ADD|G1MSM|G2ADD|G2MSM|PAIRING_CHECK|MAP_FP_TO_G1|MAP_FP2_TO_G2)\\b",
            "address\\(\\s*0x0*(b|c|d|e|f|10|11)\\s*\\)|staticcall\\(\\s*gas\\(\\)\\s*,\\s*(0x0*(b|c|d|e|f|10|11)|1[1-7])\\s*,"
        ],
        "sources": [
            "EIP-2537",
            "SHOR1997"
        ]
    },
    "bulletproofs": {
        "name": "Bulletproofs",
        "status": "vulnerable_shor",
        "attack": "shor",
        "basis": "elliptic_curve_dlog",
        "breaks": "soundness",
        "consequence": "Forge range or circuit proofs, e.g. negative amounts in a confidential transaction. No trusted setup, soundness on discrete logarithms alone.",
        "patterns": [
            "\\bbulletproofs::|\\bBulletproofGens\\b|\\bRangeProof::prove_(single|multiple)\\b"
        ],
        "sources": [
            "BULLETPROOFS2018",
            "SHOR1997"
        ]
    },
    "stark-fri": {
        "name": "STARK (FRI)",
        "status": "grover_reduced",
        "attack": "grover",
        "basis": "hash",
        "breaks": "preimage/collision only",
        "consequence": "Hash-based and transparent: no Shor-type break, and the proof parameters decide the margin.",
        "patterns": [
            "\\bwinterfell::|\\bStarkProof\\b|\\bFriProver\\b|\\bverify_stark_proof\\b"
        ],
        "sources": [
            "STARK2018"
        ]
    }
}

SELF_TEST = {
    "sinsemilla": [
        [
            "let domain = sinsemilla::CommitDomain::new(b\"z.cash:Orchard-NoteCommit\");",
            "        SinsemillaChip::<_, _, _>::configure(meta, advices, witness_pieces)"
        ],
        [
            "semilla = \"seed\"",
            "let sin_cos = (x.sin(), x.cos());"
        ]
    ],
    "reddsa": [
        [
            "use reddsa::orchard::SpendAuth;",
            "pub trait SpendAuth: SigType {}",
            "pub enum SpendAuth {}",
            "impl SigType for SpendAuth {}",
            "impl SigType for Binding {}",
            "pub type Randomizer<S> = <S as private::Sealed<S>>::Scalar;"
        ],
        [
            "let binding = value.clone();",
            "pub enum Binding { Early, Late }",
            "pub trait SpendAuthorization { fn check(&self); }",
            "impl SigTypeRegistry for Foo {}",
            "let randomizer = rng.gen();"
        ]
    ],
    "halo2-ipa": [
        [
            "use halo2_proofs::plonk::Circuit;",
            "use halo2_gadgets::ecc::chip::EccChip;"
        ],
        [
            "let halo_radius = 2.0;",
            "let halo2_version = \"0.4\";"
        ]
    ],
    "pedersen-commitment": [
        [
            "let pc_gens = PedersenGens::default();",
            "let cv = ValueCommitment::derive(value, rcv);",
            "let rho = pedersen_hash(Personalization::NoteCommitment, bits);"
        ],
        [
            "pedersen = \"author\"",
            "let commitment = \"we commit to this\";"
        ]
    ],
    "poseidon": [
        [
            "let nf = poseidon_hash(nk, rho);",
            "use halo2_poseidon::primitives::P128Pow5T3;"
        ],
        [
            "let positions = vec![0u8; 32];",
            "let position = 3;"
        ]
    ],
    "groth16": [
        [
            "function verifyProof(uint[2] calldata a, uint[2][2] calldata b) public view returns (bool)"
        ],
        [
            "function verify(bytes calldata data)"
        ]
    ],
    "bls12-381": [
        [
            "use bls12_381::{G1Affine, Scalar};"
        ],
        [
            "let bls = 12;"
        ]
    ],
    "bulletproofs": [
        [
            "let bp_gens = BulletproofGens::new(64, 1);"
        ],
        [
            "bullet = \"point\""
        ]
    ],
    "stark-fri": [
        [
            "let proof: StarkProof = prover.prove(trace)?;"
        ],
        [
            "stark = \"industries\""
        ]
    ]
}

SOURCE_EXT = {".rs", ".go", ".py", ".kt", ".swift", ".c", ".h", ".cc", ".cpp", ".cxx", ".hpp", ".js", ".mjs",
              ".cjs", ".ts", ".tsx", ".java", ".sol", ".cairo", ".move", ".zig", ".cs", ".rb", ".php", ".ex",
              ".exs", ".scala", ".hs", ".ml", ".nim", ".dart"}
SKIP_DIR = {".git", ".hg", ".svn", "node_modules", "target", "build", "dist", "vendor", "venv", ".venv",
            "__pycache__", ".tox", ".mypy_cache", ".pytest_cache"}
# Comments are excluded: a doc comment naming an algorithm is weaker evidence than a line of code using it, and
# reddsa shows the two can disagree completely. Line comments only — a crude rule, and stated rather than hidden.
COMMENT = re.compile(r"^\s*(//|#|\*|/\*|--|;)")


def scan(root: pathlib.Path, max_bytes: int = 2_000_000) -> dict:
    found: dict[str, list[tuple[str, int, str]]] = {}
    files = 0
    compiled = {k: [re.compile(p) for p in v["patterns"]] for k, v in PRIMITIVES.items()}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SOURCE_EXT:
            continue
        if any(part in SKIP_DIR for part in path.parts):
            continue
        try:
            if path.stat().st_size > max_bytes:
                continue
            text = path.read_text(errors="replace")
        except OSError:
            continue
        files += 1
        lines = text.splitlines()
        for pid, rxs in compiled.items():
            for rx in rxs:
                for m in rx.finditer(text):
                    ln = text.count("\n", 0, m.start()) + 1
                    if ln - 1 < len(lines) and COMMENT.match(lines[ln - 1]):
                        continue
                    rel = str(path.relative_to(root))
                    found.setdefault(pid, []).append((rel, ln, m.group(0)[:60]))
                    break
                else:
                    continue
                break
    return {"files": files, "found": found}


def reported_names(path: pathlib.Path) -> set[str]:
    """Algorithm names your tool says it found: SARIF, a JSON list or object, or one name per line."""
    text = path.read_text(errors="replace")
    out: set[str] = set()

    def add(v):
        if isinstance(v, str) and v.strip():
            out.add(v.strip().lower())

    try:
        doc = json.loads(text)
    except json.JSONDecodeError:
        for line in text.splitlines():
            add(line)
        return out
    stack = [doc]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            for k, v in node.items():
                if k in ("algorithm", "name", "ruleId", "message", "text", "title") and isinstance(v, str):
                    add(v)
                else:
                    stack.append(v)
        elif isinstance(node, list):
            stack.extend(node)
        elif isinstance(node, str):
            add(node)
    return out


def names_of(pid: str) -> list[str]:
    row = PRIMITIVES[pid]
    base = [row["name"], pid, pid.replace("-", " "), pid.replace("-", "_")]
    return [b.lower() for b in base]


def self_test() -> int:
    bad = 0
    for pid, (pos, neg) in SELF_TEST.items():
        rxs = [re.compile(p) for p in PRIMITIVES[pid]["patterns"]]
        for line in pos:
            if not any(r.search(line) for r in rxs):
                print(f"  FAIL  {pid}: missed  {line}")
                bad += 1
        for line in neg:
            if any(r.search(line) for r in rxs):
                print(f"  FAIL  {pid}: fired on near miss  {line}")
                bad += 1
    # Cross-check: no primitive may claim another's near miss.
    for pid, row in PRIMITIVES.items():
        rxs = [re.compile(p) for p in row["patterns"]]
        for other, (_, neg) in SELF_TEST.items():
            for line in neg:
                if any(r.search(line) for r in rxs):
                    print(f"  FAIL  {pid} fires on {other}'s near miss  {line}")
                    bad += 1
    n = sum(len(p) + len(q) for p, q in SELF_TEST.values())
    print(f"\n{n} cases over {len(PRIMITIVES)} primitives: " + ("all pass" if not bad else f"{bad} FAILED"))
    return 1 if bad else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="find zero-knowledge and shielded-pool primitives, and check that "
                                             "your own tool reports them")
    ap.add_argument("--repo", default=".", help="the checkout to scan (default: .)")
    ap.add_argument("--against", metavar="FILE",
                    help="algorithm names your tool reported: SARIF, JSON, or one per line")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--self-test", action="store_true", help="check the patterns, then exit")
    a = ap.parse_args(argv)

    if a.self_test:
        return self_test()

    root = pathlib.Path(a.repo).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2
    res = scan(root)
    found = res["found"]
    reported = reported_names(pathlib.Path(a.against)) if a.against else None

    missed = []
    if reported is not None:
        for pid in found:
            if not any(n in r or r in n for n in names_of(pid) for r in reported):
                missed.append(pid)

    if a.json:
        print(json.dumps({
            "ok": not missed,
            "files_scanned": res["files"],
            "primitives": {pid: {"name": PRIMITIVES[pid]["name"], "quantum_status": PRIMITIVES[pid]["status"],
                                 "breaks": PRIMITIVES[pid]["breaks"], "occurrences": len(hits),
                                 "first": {"file": hits[0][0], "line": hits[0][1]}}
                           for pid, hits in sorted(found.items())},
            "not_reported_by_your_tool": missed,
        }, indent=2))
        return 1 if missed else 0

    print(f"{res['files']} source file(s) scanned under {root}")
    if not found:
        print("\nNo zero-knowledge or shielded-pool primitive found. If this is a zk codebase, that is the"
              "\nresult this tool exists to distrust: check the vocabulary before believing the silence.")
        return 0
    print()
    for pid, hits in sorted(found.items(), key=lambda kv: -len(kv[1])):
        row = PRIMITIVES[pid]
        flag = "SHOR" if row["status"] == "vulnerable_shor" else row["status"]
        print(f"  {row['name']}  [{flag}]  breaks: {row['breaks']}")
        print(f"      {len(hits)} occurrence(s), first at {hits[0][0]}:{hits[0][1]}")
        print(f"      {row['consequence']}")
        print(f"      sources: {', '.join(row['sources'])}")
        print()
    if reported is not None:
        if missed:
            print("Present in the tree and NOT reported by your tool:")
            for pid in missed:
                print(f"  {PRIMITIVES[pid]['name']}  ({len(found[pid])} occurrence(s), "
                      f"first at {found[pid][0][0]}:{found[pid][0][1]})")
            print("\nEither its vocabulary has no entry for these, or they were filtered after detection."
                  "\nUntil you know which, its silence about them is not evidence of their absence.")
            return 1
        print("Every primitive found here also appears in what your tool reported.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
