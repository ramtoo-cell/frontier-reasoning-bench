# frontier-reasoning-bench

[![CI](https://img.shields.io/badge/evals-passing-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)]()
[![Anthropic: Fellowship Focus](https://img.shields.io/badge/Anthropic_Fellowship-STEM_%26_Conceptual-orange.svg)]()

> **Automated verification harnesses, error taxonomies, and formal stress-tests for frontier LLM reasoning across STEM (Lattice Cryptography, Photonic Interconnects) and Conceptual domains (Mechanism Design, Deontic Modal Logic).**

Developed to support research evaluating long-horizon scientific and conceptual reasoning in frontier models such as Claude.

---

## 🎯 Motivation: Beyond Multiple-Choice Evals

Standard LLM benchmarks (MMLU, GSM8K, standard QA) suffer from two fundamental limitations when assessing frontier reasoning models:
1. **Benchmark Saturation & Memorization:** Multiple-choice formats reward shallow pattern matching rather than genuine deductive proof search.
2. **Invisible Intermediate Drift:** A model can arrive at a correct final token through flawed intermediate steps, or conversely, execute 15 valid reasoning steps only to suffer an unflagged arithmetic sign-flip at step 16.

`frontier-reasoning-bench` introduces **Step-Level Invariant Verification**: instead of simply grading final answers, our verifiers test whether every intermediate deduction satisfies domain invariants—physical, mathematical, economic, and normative.

```
       Frontier LLM Reasoning Chain (CoT)
       ┌─────────────────────────────────────────────────────────────┐
       │ Step 1: Formulate Cyclotomic Ring R_q = Z_q[x]/(x^d + 1)    │
       │ Step 2: Compute Negacyclic Convolution (x^d = -1 mod q)     │
       │ Step 3: Inject Discrete Gaussian Noise Vector χ_σ           │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                         Automated Verification Engine
                                      ▼
       ┌─────────────────────────────────────────────────────────────┐
       │ Invariant 1: Degree Boundary [deg(p) < d]                   │
       │ Invariant 2: Modular Equivalence [Z_q reduction verified]   │
       │ Invariant 3: Negacyclic vs Cyclic Check [x^d = -1 != +1]   │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                              Taxonomy Classifier
                                      ▼
             [PASS] or [CALCULATION_DRIFT / DEONTIC_COLLAPSE]
```

---

## 🔬 Benchmark Tracks

### Track A: STEM (Science & Engineering)
* **Lattice Cryptography (`bench/stem/lattice_crypto_eval.py`):**
  * Evaluates multi-step reductions in quotient rings $R_q = \mathbb{Z}_q[x]/(x^d + 1)$.
  * Verifies that reasoning chains distinguish between negacyclic convolution ($x^d \equiv -1 \pmod{x^d+1}$) and standard cyclic convolution ($x^d \equiv 1$).
  * Validates noise bounds in Ring-LWE Key Encapsulation Mechanisms (Kyber / ML-KEM).
* **Photonic Interconnect Physics (`bench/stem/optical_kv_eval.py`):**
  * Verifies insertion loss budgets ($\sum \alpha_i \le \alpha_{\text{margin}}$) across high-throughput optical KV-cache memory fabrics.
  * Models silicon microring resonator thermal tuning shifts ($\Delta \lambda = \frac{d\lambda}{dT}\Delta T$) under 20–40 K thermal gradients.
  * Evaluates physical feasibility constraints without hallucinatory optical power margins.

### Track B: Conceptual Reasoning (Philosophy, Economics, Law)
* **Game-Theoretic Mechanism Design (`bench/conceptual/mechanism_design_eval.py`):**
  * Stress-tests economic reasoning against the **Myerson-Satterthwaite Impossibility Theorem**: verifies that the model recognizes that no bilateral trade mechanism can simultaneously achieve ex-post efficiency, Bayesian incentive compatibility (BIC), interim individual rationality (IIR), and ex-post budget balance without external subsidies.
  * Verifies dominant-strategy incentive compatibility in second-price sealed-bid auctions.
* **Deontic Modal Logic & Regulatory Antinomies (`bench/conceptual/deontic_logic_eval.py`):**
  * Evaluates formal normative reasoning under $\text{KD45}_n$ and Standard Deontic Logic ($\mathbf{SDL}$).
  * Invariant checks prevent **Deontic Collapse** ($\mathcal{O}p \leftrightarrow p$, conflating fact with obligation) and resolve **Contrary-to-Duty (CTD)** obligations without Chisholm's paradox.
  * Detects unhandled normative contradictions under SDL Axiom D: $\mathcal{O}p \wedge \mathcal{F}p \to \bot$.

---

## 📊 Error Taxonomy Classification

Every failing reasoning trace is classified into an explicit structural failure mode:

| Error Type | Description |
| :--- | :--- |
| `CALCULATION_DRIFT` | Exact algebraic or arithmetic invariant failure in intermediate derivations. |
| `PHYSICAL_CONSTRAINT_VIOLATION` | Physical violation (e.g., optical power margin exceeded, negative entropy). |
| `EQUILIBRIUM_INSTABILITY` | Profitable deviations exist; mechanism fails Incentive Compatibility or IR. |
| `DEONTIC_PARADOX_COLLAPSE` | Conflation of factual truth with normative obligation, or unresolved normative antinomy. |
| `PREMISE_HALLUCINATION` | Introduction of unstated constraints or unwarranted background assumptions. |
| `CIRCULAR_JUSTIFICATION` | Conclusion assumed as a premise in multi-step deductive arguments. |

---

## 🚀 Quickstart

### 1. Installation

```bash
git clone https://github.com/ramtoo-cell/frontier-reasoning-bench.git
cd frontier-reasoning-bench
```

Zero external dependencies required—runs directly on pure Python standard library:

### 2. Run All Benchmarks

```bash
python3 -m bench.cli --track ALL
```

### 3. Generate Markdown Leaderboard / Summary

```bash
python3 -m bench.cli --track ALL --output markdown
```

### 4. Run Unit Tests

```bash
python3 -m unittest discover tests
```

---

## 📂 Project Structure

```
frontier-reasoning-bench/
├── README.md                           # Documentation & theoretical framing
├── bench/
│   ├── cli.py                          # CLI runner entrypoint
│   ├── core/
│   │   ├── runner.py                   # Benchmark orchestration engine
│   │   ├── reporter.py                 # Markdown & summary report generator
│   │   └── taxonomy.py                 # Error taxonomy enum & data models
│   ├── stem/
│   │   ├── lattice_crypto_eval.py      # Ring-LWE & cyclotomic ring verifiers
│   │   └── optical_kv_eval.py          # Photonic link budget & thermal drift verifiers
│   └── conceptual/
│       ├── mechanism_design_eval.py    # Game theory & auction equilibria verifiers
│       └── deontic_logic_eval.py       # Deontic modal logic & norm conflict verifiers
├── data/
│   ├── stem_problems.json              # Curated STEM benchmark problems
│   └── conceptual_problems.json        # Curated Conceptual Reasoning problems
└── tests/
    └── test_bench.py                   # Invariant test suite
```

---

## 🎓 Fellowships Context

Authored by **Ramkumar Bharathan** (Chicago Booth MBA Honors, Purdue MS AI in progress) as a dedicated technical artifact demonstrating evaluation frameworks for the **Anthropic STEM & Conceptual Reasoning Fellowships** (January 2027 cohort).
