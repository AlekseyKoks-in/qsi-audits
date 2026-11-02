# A federal mandate now describes this work. Here is the portfolio measured against it.

*First published 30 October 2026; updated 2 November 2026 with NIST's final transition schedule
(section 3) and the order's number.*

On 24 June 2026 the Office of Management and Budget issued **M-26-15, Execution of the Migration to
Post-Quantum Cryptography** ([primary source](https://www.whitehouse.gov/wp-content/uploads/2026/06/M-26-15-Execution-of-the-Migration-to-Post-Quantum-Cryptography.pdf)), implementing the Executive Order *Securing the Nation
Against Advanced Cryptographic Attacks* of 22 June 2026. The memorandum names that order by its title and
not by a number, and when this report was first published the number in secondary coverage could not be
confirmed from it. It is now: the Federal Register lists the order as **Executive Order 14412**
([91 FR 38483](https://www.federalregister.gov/documents/2026/06/25/2026-12909/securing-the-nation-against-advanced-cryptographic-attacks)), and NIST's final IR 8547 cites it by that number.

Two things in it matter to anyone doing cryptographic inventory work, and both are quoted rather than paraphrased.

## 1. The memorandum describes the method, not just the goal

> **Automated Cryptographic Inventory:** The foundation of the migration plan is a dynamic, continuously updated
> inventory of all cryptographic assets. This inventory should be created and maintained through automated tools
> wherever possible, including by use of Software Composition Analysis (SCA) to analyze Software Bills of
> Materials (SBOMs), Static/Dynamic Application Security Testing (SAST/DAST) to find cryptographic functions in
> code, and network scanners to detect protocols and cipher suites. This data should populate a central
> Cryptographic Bill of Materials (CBOM) to provide a real-time view of the agency's cryptographic posture.

Three discovery methods. **These bundles use two of them and declare the third rather than quietly omitting it.**
Across the 53 codebases here, the reports record 804 coverage entries for dependency
manifests (the SCA path) and 28 813 for source code (the SAST path), plus
115 for certificate and key material and
111 for TLS settings read out of code and configuration. Live
network probing is the third method, and it is **declared not performed**:
170 `tls_key_exchange_groups` entries sit in each report's `not_checked`
list, because every audit here runs offline and sends no request to the owner's systems. The scanner exists in the
product; these bundles deliberately do not use it, and say so.

Every bundle carries a CycloneDX `cbom.cdx.json`. Note that the **minimum elements of a CBOM are not defined
yet**: the order directs CISA and NIST to publish them within 270 days, which falls around
**19 March 2027**. Until then nobody can claim conformance to them, and a vendor who does is selling
something that does not exist.

## 2. The algorithm table has seven names and a catch-all, and the catch-all is where the real exposure is

M-26-15 tabulates the quantum-vulnerable algorithms: ECDH, MQV, ECDSA, Diffie-Hellman and variants, RSA
signatures, RSA key establishment, DSA — and then **"Other non-PQC Asymmetric Algorithms: Remaining asymmetric
algorithms not enumerated in the list above."**

That last row is doing most of the work. Of the **1 729 Shor-breakable rows** in this portfolio:

| Algorithm, as M-26-15 names it | Shor-breakable rows found |
|---|---:|
| ECDSA | 778 |
| RSA signatures and key establishment | 190 |
| ECDH key exchange | 100 |
| DH key exchange and variants | 3 |
| DSA | 4 |
| MQV key exchange | 0 |
| **Other non-PQC Asymmetric Algorithms** (the catch-all) | **654** |

**62% fall under one of the seven named algorithms, and 38% fall only under the catch-all** —
16 distinct algorithms that a checklist built from the seven would never look for:

| In the catch-all | rows |
|---|---:|
| Ed25519 | 201 |
| Pedersen commitment | 103 |
| Halo 2 (IPA) | 72 |
| Paillier | 59 |
| FROST | 42 |
| Schnorr (BIP-340) | 38 |
| RedDSA | 38 |
| BLS12-381 | 32 |
| Sinsemilla | 24 |
| BN254 (alt_bn128) | 18 |
| ElGamal | 10 |
| Bulletproofs | 6 |

The largest single thing the named list misses is **Ed25519, with 201 rows**. It is in SSH, in
Signal, in a dozen blockchains, and the memorandum does not name EdDSA anywhere. Everything below it is the
cryptography that modern systems are actually built from: Pedersen commitments and Halo 2 in shielded pools,
Paillier and FROST in threshold-signing libraries, BLS12-381 in consensus layers, Sinsemilla and RedDSA in Zcash.

The practical consequence is worth stating plainly, because it cuts against how compliance tooling usually gets
built. **A tool that implements the memorandum's seven named algorithms is not a quantum-readiness tool.** It is
a tool for finding RSA and ECDSA, which are the easy two thirds. The catch-all is not an afterthought in the
memorandum; it is the clause that makes the requirement correct, and it can only be satisfied by a vocabulary
that was not derived from the list.

## 3. NIST's final transition schedule covers every key size

On 27 October 2026 — three days before this report was first published, which missed it — NIST issued
**IR 8547, Transition to Post-Quantum Cryptography Standards, in final form** ([primary source](https://csrc.nist.gov/pubs/ir/8547/final)).
Its tables of quantum-vulnerable algorithms now carry one schedule for every key size: ECDSA, EdDSA and RSA
signatures, finite-field and elliptic-curve Diffie-Hellman and MQV, and RSA key establishment are all
**"Deprecated after 2030, Disallowed after 2035"**. The November 2024 draft deprecated only the 112-bit level, so
128-bit-and-up keys — P-256, Ed25519, RSA-3072 — had no milestone before 2035. NIST gives the reason in the text:

> These guidelines had projected that NIST would disallow public-key schemes that provide 112 bits of security on
> January 1, 2031. However, based on the need to migrate to quantum-resistant algorithms during this time frame,
> NIST will instead deprecate all quantum-vulnerable digital signature algorithms after 2030 and disallow their
> use under NIST standards and guidelines after 2035.

NIST's schedule governs approved parameter sets, and much of this portfolio is not on them, so the
1 729 Shor-breakable rows are split by the parameter each inventory row records:

| Shor-breakable rows | rows | Draft, Nov 2024 | Final, Oct 2026 |
|---|---:|---|---|
| Approved, 128-bit and up: Ed25519, P-256, P-384, RSA-3072 and RSA-4096 | 281 | disallowed after 2035, no earlier milestone | **deprecated after 2030**, disallowed after 2035 |
| Approved, 112-bit: RSA-2048 | 60 | deprecated after 2030 | deprecated after 2030 |
| Tabulated family, key size or curve not recorded | 380 | depended on the key size | deprecated after 2030 at any size, if on approved parameters |
| secp256k1, which is not a NIST-approved curve | 470 | not approved | not approved |
| X25519, NIST approval for key establishment not confirmed here | 68 | not confirmed | not confirmed |
| EdDSA variants outside FIPS 186-5, mixed secp256k1/P-256, RSA-1024 | 13 | — | — |
| Families no NIST standard approves | 457 | — | — |

Two results. **The final puts a 2030 milestone on 281 rows that the draft left alone until
2035** — standard Ed25519, P-256, P-384, RSA-3072 and up — against 60 RSA-2048 rows that had
one already. And **for 380 rows whose key size the inventory could not recover, the final makes
the size irrelevant**: under the draft the date depended on it, under the final it does not. An inventory that
cannot read a key length can now still state the NIST date. EdDSA — the largest item in M-26-15's catch-all, which
the memorandum never names — is in the final's Table 2; 148 of its 201 rows here are standard
Ed25519 and carry the new milestone.

The largest single block, **470 secp256k1 rows** — the curve of Bitcoin and Ethereum — was never
on a NIST-approved curve, so neither version of the schedule governs it. With the 457 rows in
families no NIST standard approves — Pedersen commitments, Halo 2, Paillier, FROST, BLS12-381, BIP-340 Schnorr and
the rest, plus DSA, which FIPS 186-5 no longer allows for signature generation and the final tables do not list —
that is **927 of 1 729 rows (54%) about which NIST's transition dates say nothing**. For a
blockchain codebase, the deadline is whatever its own protocol decides.

For federal high-value assets and high-impact systems the earlier deadlines still govern, and IR 8547 repeats
them: post-quantum key establishment by 31 December 2030, post-quantum signatures by 31 December 2031, and TLS 1.3
support by 2 January 2030. Hybrid key establishment remains allowed — the final says a composite scheme can be
FIPS 140-validated "as long as at least one of the inputs ... comes from an approved key-establishment scheme".

## What this exercise changed in the tool

Checking the registry against the memorandum's table found **one genuine gap: MQV**. Six of the seven named
algorithms had entries; MQV had none, because it is rarely deployed — TLS never adopted it and Bouncy Castle is
the usual implementation — so nothing in the portfolio ever reported it missing. That is precisely how a gap
against a normative list survives.

An entry now exists, with its OIDs read from Bouncy Castle's `SECObjectIdentifiers` and `X9ObjectIdentifiers`
rather than from memory (SECG `1.3.132.1.3`–`.6`, `.13`; X9.42 `1.2.840.10046.3.7`–`.8`), detection patterns taken
from the real classes (`ECMQVBasicAgreement`, `MQVParameterSpec`, the `KeyAgreement.ECMQVWITHSHA*KDF` names), and
a positive and a negative test case. **No published figure changes**: the pattern matches nothing in twelve
cloned repositories and no bundle names MQV — which for a scheme TLS never adopted is the expected result, and is
stated as the measured effect rather than left implied.

## What this is not

This is not a federal compliance artefact and it is not offered as one. The memorandum applies to federal
agencies and, through OMB's contractor provisions, to their suppliers; it explicitly **does not apply to national
security systems**. The minimum CBOM elements are unpublished. These are audits of public open-source code,
performed offline, signed, and verifiable — a demonstration that the method the memorandum describes produces
something checkable, measured on 30 802 parsed files across 53 codebases.

Every figure above is computed from the 61 bundles in this repository and can be recomputed from them.
`verify.py` checks all of them with no network access and no trust in me.
