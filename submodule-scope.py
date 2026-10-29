#!/usr/bin/env python3
"""Do the submodules your project pins actually reach the tools you believe are reading them?

    python3 submodule-scope.py                      # are the pinned submodules even populated?
    python3 submodule-scope.py --repo /path/to/repo
    python3 submodule-scope.py --against results.sarif
    python3 submodule-scope.py --against parsed-files.txt --scope src include
    python3 submodule-scope.py --json

No dependencies, no network. Exit status 0 when nothing is wrong, 1 when something is, so it can go straight
into CI. It reads `.gitmodules` with a small parser of its own and never shells out to git, so it also works on
an exported tree with no `.git` directory.

Why this exists
---------------
Two defects, both found the hard way, both silent, both of which make a security tool report a clean result for
code it never opened.

1. **A shallow clone leaves submodules empty.** `git clone --depth 1` without `--recurse-submodules` leaves every
   pinned submodule as an empty directory, and a scanner walking the tree finds nothing there and says nothing
   about it. Blockstream Jade measured 7 cryptographic inventory rows and no secp256k1 at all this way; read with
   its submodules materialised it is 93 rows, 66 of them breakable by Shor's algorithm. CI is where this happens,
   because CI is where shallow clones live.

2. **A skip list can silently override a declared scope.** A scanner whose directory-skip list contains `vendor`
   will skip `vendor/embit` even when the audit scope explicitly named it — and if it skips before counting, the
   report never mentions the files it declined. A Bitcoin hardware wallet measured 13 inventory rows and a single
   ECDSA row that way; read correctly it is 98 rows and 64 Shor-breakable.

Mode 1 catches the first and needs nothing but the checkout. Mode 2 catches the second: give it the list of files
your tool says it parsed and it will tell you which pinned, in-scope submodules are missing from that list.

Nothing here is specific to any one scanner. `--against` accepts a SARIF file, a JSON array of paths, a JSON
object with a "files" or "inputs" list, or a plain text file with one path per line.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys


def parse_gitmodules(text: str) -> list[dict]:
    """Minimal .gitmodules reader: INI-ish sections, `path` and `url` keys. No git required."""
    mods: list[dict] = []
    cur: dict | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if line.startswith("[") and line.endswith("]"):
            if cur and cur.get("path"):
                mods.append(cur)
            inner = line[1:-1].strip()
            cur = {"name": inner.split('"')[1] if '"' in inner else inner} if inner.lower().startswith("submodule") else None
            continue
        if cur is None or "=" not in line:
            continue
        k, _, v = line.partition("=")
        k, v = k.strip().lower(), v.strip()
        if k in ("path", "url", "branch"):
            cur[k] = v
    if cur and cur.get("path"):
        mods.append(cur)
    return mods


def load_parsed_paths(path: pathlib.Path) -> set[str]:
    """Paths a tool says it read, from SARIF, a JSON list/object, or one path per line."""
    text = path.read_text(errors="replace")
    try:
        doc = json.loads(text)
    except json.JSONDecodeError:
        return {l.strip().lstrip("./") for l in text.splitlines() if l.strip()}

    out: set[str] = set()

    def add(p):
        if isinstance(p, str) and p.strip():
            out.add(p.strip().lstrip("./").removeprefix("file://"))

    if isinstance(doc, list):
        for item in doc:
            add(item if isinstance(item, str) else (item or {}).get("path") or (item or {}).get("name"))
        return out
    if not isinstance(doc, dict):
        return out
    # SARIF: results[].locations[].physicalLocation.artifactLocation.uri, plus artifacts[].location.uri
    for run in doc.get("runs") or []:
        for art in run.get("artifacts") or []:
            add(((art or {}).get("location") or {}).get("uri"))
        for res in run.get("results") or []:
            for loc in res.get("locations") or []:
                add((((loc or {}).get("physicalLocation") or {}).get("artifactLocation") or {}).get("uri"))
    for key in ("files", "inputs", "paths", "parsed"):
        for item in doc.get(key) or []:
            add(item if isinstance(item, str) else (item or {}).get("name") or (item or {}).get("path"))
    return out


def in_scope(sub: str, scope: list[str]) -> bool:
    """A submodule is in scope when no scope was declared, or when it overlaps a declared path either way."""
    if not scope:
        return True
    for s in scope:
        s = s.strip().strip("/")
        if not s:
            continue
        if sub == s or sub.startswith(s + "/") or s.startswith(sub + "/"):
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="check that pinned submodules are populated and actually read",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=".", help="the checkout to inspect (default: .)")
    ap.add_argument("--against", metavar="FILE",
                    help="list of files a tool says it parsed: SARIF, JSON, or one path per line")
    ap.add_argument("--scope", nargs="*", default=[], metavar="PATH",
                    help="the paths the tool was told to read; a submodule outside them is expected to be absent")
    ap.add_argument("--exclude", nargs="*", default=[], metavar="PATH",
                    help="submodule paths that are deliberately not read, e.g. pinned test vectors")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    a = ap.parse_args(argv)

    repo = pathlib.Path(a.repo).resolve()
    gm = repo / ".gitmodules"
    if not gm.exists():
        msg = f"no .gitmodules in {repo} — nothing to check"
        print(json.dumps({"ok": True, "reason": msg}) if a.json else f"ok: {msg}")
        return 0

    mods = parse_gitmodules(gm.read_text(errors="replace"))
    excluded = {e.strip().strip("/") for e in a.exclude}
    parsed = load_parsed_paths(pathlib.Path(a.against)) if a.against else None

    empty, unread, fine, out_of_scope, skipped = [], [], [], [], []
    for m in mods:
        path = m["path"].strip().strip("/")
        d = repo / path
        if path in excluded:
            skipped.append(path)
            continue
        if not in_scope(path, a.scope):
            out_of_scope.append(path)
            continue
        if not d.is_dir() or not any(d.iterdir()):
            empty.append(path)
            continue
        if parsed is not None:
            if any(p == path or p.startswith(path + "/") for p in parsed):
                fine.append(path)
            else:
                unread.append(path)
        else:
            fine.append(path)

    problems = len(empty) + len(unread)
    if a.json:
        print(json.dumps({"ok": problems == 0, "declared": len(mods), "empty": empty, "unread": unread,
                          "populated_and_read" if parsed is not None else "populated": fine,
                          "out_of_scope": out_of_scope, "excluded": skipped}, indent=2))
        return 1 if problems else 0

    print(f"{len(mods)} submodule(s) declared in .gitmodules")
    for p in fine:
        print(f"  ok       {p}" + ("  (populated and read)" if parsed is not None else "  (populated)"))
    for p in out_of_scope:
        print(f"  skipped  {p}  (outside the declared scope, so expected to be absent)")
    for p in skipped:
        print(f"  excluded {p}  (excluded by request)")
    for p in empty:
        print(f"  EMPTY    {p}  <- pinned but the directory has nothing in it")
    for p in unread:
        print(f"  UNREAD   {p}  <- populated, in scope, and absent from what the tool says it parsed")

    if not problems:
        print("\nnothing wrong." + ("" if parsed is not None else
              "  Re-run with --against to also check that your tool actually read them."))
        return 0

    print()
    if empty:
        print(f"{len(empty)} pinned submodule(s) are EMPTY. A tool walking this tree will report a clean result")
        print("for code it never opened. In CI this is usually a shallow clone:")
        print("    git clone --recurse-submodules ...        # or, in an existing checkout:")
        print("    git submodule update --init --recursive")
        print("  GitHub Actions: actions/checkout with `submodules: recursive`.")
    if unread:
        print(f"{len(unread)} populated, in-scope submodule(s) are missing from what the tool parsed.")
        print("Either the tool's skip list is overriding the scope it was given, or the scope is wrong.")
        print("Whichever it is, the result understates the tree — check before trusting it.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
