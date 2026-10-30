# A federal mandate now describes this work. Here is the portfolio measured against it.

On 24 June 2026 the Office of Management and Budget issued **M-26-15, Execution of the Migration to
Post-Quantum Cryptography** ([primary source](https://www.whitehouse.gov/wp-content/uploads/2026/06/M-26-15-Execution-of-the-Migration-to-Post-Quantum-Cryptography.pdf)), implementing the Executive Order *Securing the Nation
Against Advanced Cryptographic Attacks* of 22 June 2026. The memorandum names that order by its title and
not by a number, so the "EO 14412" of secondary coverage is not something this document can confirm.

Two things in it matter to anyone doing cryptographic inventory work, and both are quoted rather than paraphrased.

## 1. The memorandum describes the method, not just the goal

> **Automated Cryptographic Inventory:** The foundation of the migration plan is a dynamic, continuously updated
> inventory of all cryptographic assets. This inventory should be created and maintained through automated tools
> wherever possible, including by use of Software Composition Analysis (SCA) to analyze Software Bills of
> Materials (SBOMs), Static/Dynamic Application Security Testing (SAST/DAST) to find cryptographic functions in
> code, and network scanners to detect protocols and cipher suites. This data should populate a central
> Cryptographic Bill of Materials (CBOM) to provide a real-time view of the agency's cryptographic posture.

Three discovery methods. **These bundles use two of them and declare the third rather than quietly omitting it.**
Across the 52 codebases here, the reports record 801 coverage entries for dependency
manifests (the SCA path) and 28 786 for source code (the SAST path), plus
115 for certificate and key material and
110 for TLS settings read out of code and configuration. Live
network probing is the third method, and it is **declared not performed**:
169 `tls_key_exchange_groups` entries sit in each report's `not_checked`
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

That last row is doing most of the work. Of the **1 708 Shor-breakable rows** in this portfolio:

| Algorithm, as M-26-15 names it | Shor-breakable rows found |
|---|---:|
| ECDSA | 778 |
| RSA signatures and key establishment | 190 |
| ECDH key exchange | 100 |
| DH key exchange and variants | 3 |
| DSA | 4 |
| MQV key exchange | 0 |
| **Other non-PQC Asymmetric Algorithms** (the catch-all) | **633** |

**63% fall under one of the seven named algorithms, and 37% fall only under the catch-all** —
15 distinct algorithms that a checklist built from the seven would never look for:

| In the catch-all | rows |
|---|---:|
| Ed25519 | 201 |
| Pedersen commitment | 99 |
| Halo 2 (IPA) | 72 |
| Paillier | 59 |
| FROST | 42 |
| Schnorr (BIP-340) | 38 |
| BLS12-381 | 32 |
| RedDSA | 27 |
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
something checkable, measured on 30 771 parsed files across 52 codebases.

Every figure above is computed from the 60 bundles in this repository and can be recomputed from them.
`verify.py` checks all of them with no network access and no trust in me.
