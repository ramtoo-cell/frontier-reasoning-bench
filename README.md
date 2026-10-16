# frontier-reasoning-bench

[![evals](https://img.shields.io/badge/evals-10%2F10_passing-brightgreen.svg)]()
[![tests](https://img.shields.io/badge/tests-6%2F6_passing-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)]()
[![Focus](https://img.shields.io/badge/Focus-Conceptual_Reasoning_%26_Process_Supervision-orange.svg)]()

> **Step-level invariant verification harnesses, process-supervision reward oracles, and failure taxonomies for frontier LLM reasoning across Philosophy, Cognitive Science, Economics, Policy, and Law.**

Read the full Google-style architecture & invariant specification: **[`docs/DESIGN.md`](docs/DESIGN.md)**.

---

## 🎯 Why Step-Level Invariant Verification for Conceptual Reasoning?

In judgment-heavy domains (**philosophy, cognitive science, economics, policy, and law**), outcome-only multiple-choice benchmarks saturate quickly and mask fatal intermediate reasoning errors:
1. **Right Conclusion via Invalid Axiom:** A model can guess the correct policy option while conflating **Kaldor-Hicks potential compensation** with **strict Pareto dominance**.
2. **Rhetorical Sycophancy:** Free-text LLM judges reward confident, verbose prose over formal consistency.
3. **Zero Process Signal:** Binary final-answer grading cannot pinpoint *which* step in a 20-step reasoning chain violated a legal canon or economic equilibrium constraint.

`frontier-reasoning-bench` provides **deterministic process-level verifiers** across all five disciplines of the **Anthropic Conceptual Reasoning Fellowship**, turning foundational theorems and canons into executable unit tests on reasoning trajectories.

---

## 🧠 The 5 Conceptual Reasoning Verification Modules

| Discipline | Module | Formal Invariants Verified |
| :--- | :--- | :--- |
| **1. Economics** | [`mechanism_design_eval.py`](bench/conceptual/mechanism_design_eval.py) | **Myerson-Satterthwaite Impossibility Theorem** (ex-post efficiency vs. BIC, IIR, and budget balance), Vickrey dominant-strategy truthfulness, and Revenue Equivalence. |
| **2. Philosophy** | [`deontic_logic_eval.py`](bench/conceptual/deontic_logic_eval.py) | **Standard Deontic Logic ($\mathbf{SDL}$ / $\text{KD45}_n$)**, Axiom D consistency ($\neg(\mathcal{O}p \wedge \mathcal{F}p)$), Hume's Guillotine (no $\mathcal{O}p \leftrightarrow p$ deontic collapse), and **Chisholm's Contrary-to-Duty (CTD)** paradox resolution. |
| **3. Cognitive Science** | [`cognitive_belief_eval.py`](bench/conceptual/cognitive_belief_eval.py) | **Bayesian Posterior Coherence**, detection of **Base-Rate Neglect** under low-prevalence priors ($P(H) \ll 0.05$), and **Tversky-Kahneman Conjunction Fallacy** ($P(A \wedge B) \le P(A)$). |
| **4. Policy & Governance** | [`policy_tradeoff_eval.py`](bench/conceptual/policy_tradeoff_eval.py) | Multi-stakeholder welfare optimization across **Strict Pareto Efficiency**, **Kaldor-Hicks Net Surplus**, and **Rawlsian Maximin** floors. |
| **5. Law & Jurisprudence** | [`statutory_interpretation_eval.py`](bench/conceptual/statutory_interpretation_eval.py) | Formal canons of statutory construction: ***Lex Specialis Derogat Legi Generali*** (safe-harbor precedence) and ***Ejusdem Generis*** (enumerated class constraints). |

---

## 📊 Structured Failure Taxonomy

Every failed reasoning trajectory returns a deterministic `VerificationResult` with an exact `failed_step_index` and diagnostic classification:

* `EQUILIBRIUM_INSTABILITY` — Profitable unilateral deviation exists, or mechanism violates Myerson-Satterthwaite / Pareto boundaries.
* `DEONTIC_PARADOX_COLLAPSE` — Conflation of empirical fact with normative obligation, unhandled SDL Axiom D antinomy, or inverted *lex specialis*.
* `CALCULATION_DRIFT` — Exact Bayesian posterior, Kaldor-Hicks surplus, or Rawlsian floor miscalculation (including Base-Rate Neglect).
* `PREMISE_HALLUCINATION` — Application of an inapplicable statutory canon or unstated factual assumption.
* `CIRCULAR_JUSTIFICATION` — Monadic material implication used where dyadic defeasible logic is required for secondary breach duties.

---

## 🚀 Quickstart (Zero Dependencies, Pure Python 3)

```bash
git clone https://github.com/ramtoo-cell/frontier-reasoning-bench.git
cd frontier-reasoning-bench

# 1. Execute the 10-case benchmark across all 5 conceptual disciplines
python3 -m bench.cli --track ALL

# 2. Generate Markdown leaderboard & discipline report
python3 -m bench.cli --track ALL --output markdown

# 3. Run the invariant unit-test suite (verifies both sound traces and injected fallacies)
python3 -m unittest discover tests -v
```

### Sample Console Output

```text
==============================================================================
          FRONTIER REASONING BENCHMARK — EVALUATION EXECUTION
==============================================================================
[PASS] ECON-01         [CONCEPTUAL] Mechanism_Design          Score: 1.00
[PASS] ECON-02         [CONCEPTUAL] Mechanism_Design          Score: 1.00
[PASS] PHIL-01         [CONCEPTUAL] Deontic_Modal_Logic       Score: 1.00
[PASS] PHIL-02         [CONCEPTUAL] Deontic_Modal_Logic       Score: 1.00
[PASS] COGSCI-01       [CONCEPTUAL] Cognitive_Science         Score: 1.00
[PASS] COGSCI-02       [CONCEPTUAL] Cognitive_Science         Score: 1.00
[PASS] POLICY-01       [CONCEPTUAL] Policy_Governance         Score: 1.00
[PASS] POLICY-02       [CONCEPTUAL] Policy_Governance         Score: 1.00
[PASS] LAW-01          [CONCEPTUAL] Law_Jurisprudence         Score: 1.00
[PASS] LAW-02          [CONCEPTUAL] Law_Jurisprudence         Score: 1.00
==============================================================================
Total: 10/10 Passed (100.0%) | Mean Score: 1.00/1.00
==============================================================================
```
