# Design Doc: Step-Level Invariant Verification for Conceptual Reasoning

**Author:** Ramkumar Bharathan  
**Status:** Implemented (v1.0)  
**Target Domain:** Process Supervision & Formal Invariant Verification across Philosophy, Cognitive Science, Economics, Policy, and Law  

---

## 1. Context & Problem Statement

Standard benchmarks for evaluating Large Language Models (MMLU, BIG-Bench, GPQA) rely on **outcome supervision** over single-token multiple-choice selections or short-form strings. In judgment-heavy domains (**philosophy, cognitive science, economics, policy, and law**), outcome-only evaluation fails for three reasons:

1. **Right Answer via Flawed Deduction (False Positives):** Models routinely arrive at the legally or economically plausible conclusion while violating core intermediate axioms (e.g., conflating Kaldor-Hicks potential compensation with strict Pareto dominance, or ignoring a statutory safe harbor before excusing liability on an unrelated ground).
2. **Sycophancy & Rhetorical Masking:** Free-text LLM-as-a-judge rubrics reward eloquent prose and hedging ("both sides have merit") over sharp formal consistency.
3. **Opaque Failure Localization:** A binary pass/fail score on a 1,500-token reasoning trace provides zero gradient or diagnostic signal on *which* step violated an axiom.

## 2. Goals & Non-Goals

### Goals
* **Step-Level Invariant Verification:** Verify intermediate structured deductions against formal domain axioms across all 5 disciplines of the Anthropic Conceptual Reasoning Fellowship.
* **Deterministic, Zero-Dependency Execution:** Run in $<2\,\text{ms}$ for the entire suite using pure Python 3 standard library (`unittest` green, zero external dependencies).
* **Actionable Failure Taxonomy:** Classify every reasoning failure into a mutually exclusive diagnostic bucket (`CALCULATION_DRIFT`, `EQUILIBRIUM_INSTABILITY`, `DEONTIC_PARADOX_COLLAPSE`, `PREMISE_HALLUCINATION`, `CIRCULAR_JUSTIFICATION`) with an exact `failed_step_index`.

### Non-Goals
* Replacing open-ended prose rubrics (`policy-reasoning-bench` handles prose rubric grading; `frontier-reasoning-bench` verifies formal structural invariants).
* Training a neural Process Reward Model (PRM) directly in this repository; rather, this engine serves as a **deterministic reward oracle** for RLVR (Reinforcement Learning with Verifiable Rewards) in conceptual domains.

---

## 3. Architecture & Domain Invariants

```
Candidate Reasoning Trace (Step 0 ... Step N)
                    │
                    ▼
    ┌───────────────────────────────┐
    │      BenchmarkRunner          │
    └───────────────┬───────────────┘
                    │
    ┌───────────────┼───────────────────────────────────────────────────┐
    ▼               ▼               ▼                 ▼                 ▼
[Economics]   [Philosophy]    [Cognitive Sci]    [Policy/Welfare]   [Law/Statutes]
Myerson-      Standard        Bayes Posterior    Pareto vs.         Lex Specialis,
Satterthwaite Deontic Logic   & Base-Rate        Kaldor-Hicks vs.   Ejusdem Generis,
& VCG IC/IR   (SDL / CTD)     Neglect Traps      Rawlsian Maximin   Safe Harbors
    │               │               │                 │                 │
    └───────────────┴───────────────┼─────────────────┴─────────────────┘
                                    ▼
                    VerificationResult(passed, outcome,
                                       score, failed_step_index)
```

### 3.1 Economics (`bench/conceptual/mechanism_design_eval.py`)
* **Myerson-Satterthwaite Theorem:** In bilateral trade with private valuations $v_s, v_b \sim U[0, 1]$ and overlapping supports, no mechanism can simultaneously satisfy:
  1. Ex-post Pareto efficiency
  2. Bayesian Incentive Compatibility (BIC)
  3. Interim Individual Rationality (IIR)
  4. Ex-post Budget Balance ($\sum t_i = 0$)
  Any reasoning step claiming all four hold without an external subsidy is immediately flagged as `EQUILIBRIUM_INSTABILITY`.
* **Vickrey / Second-Price Auctions:** Weakly dominant strategy is truthful bidding ($b_i = v_i$) regardless of opponent bid distributions.

### 3.2 Philosophy & Deontic Logic (`bench/conceptual/deontic_logic_eval.py`)
* **Hume's Guillotine (No Deontic Collapse):** Empirical fact $p$ never entails normative obligation $\mathcal{O}p$, nor does $\mathcal{O}p \to p$.
* **SDL Axiom D:** $\mathcal{O}p \to \neg \mathcal{O}\neg p$ (equivalently, $\neg(\mathcal{O}p \wedge \mathcal{F}p)$). Simultaneous assertion of obligation and prohibition without hierarchical override triggers `DEONTIC_PARADOX_COLLAPSE`.
* **Chisholm's Contrary-to-Duty (CTD) Paradox:** Secondary restorative duties triggered upon breach ($\neg p \to \mathcal{O}q$) must be evaluated using dyadic defeasible conditionals $\mathcal{O}(q \mid \neg p)$ rather than material implication in monadic $\mathbf{SDL}$.

### 3.3 Cognitive Science (`bench/conceptual/cognitive_belief_eval.py`)
* **Kolmogorov & Bayes Coherence:** Given prior $P(H)$, sensitivity $P(E \mid H)$, and false-positive rate $P(E \mid \neg H)$, posterior belief must satisfy:
  $$P(H \mid E) = \frac{P(E \mid H)P(H)}{P(E \mid H)P(H) + P(E \mid \neg H)(1 - P(H))}$$
  Asserting $P(H \mid E) \approx P(E \mid H)$ when $P(H) \ll 0.05$ is flagged as **Base-Rate Neglect**.
* **Extension Rule:** $P(A \wedge B) \le \min(P(A), P(B))$. Violation is flagged as **Tversky-Kahneman Conjunction Fallacy**.

### 3.4 Public Policy & Welfare Economics (`bench/conceptual/policy_tradeoff_eval.py`)
* Given status-quo utility vector $u^0 \in \mathbb{R}^n$ and policy allocation $u^p \in \mathbb{R}^n$:
  * **Strict Pareto Improvement:** $\forall i, u^p_i \ge u^0_i$ and $\exists j, u^p_j > u^0_j$.
  * **Kaldor-Hicks Efficiency:** $\sum_i u^p_i > \sum_i u^0_i$ (potential compensation without actual transfer).
  * **Rawlsian Maximin:** $\arg\max_p \min_i u^p_i$.
  Conflating Kaldor-Hicks surplus with Pareto improvement when $\exists k, u^p_k < u^0_k$ is flagged.

### 3.5 Law & Statutory Interpretation (`bench/conceptual/statutory_interpretation_eval.py`)
* **Lex Specialis Derogat Legi Generali:** Where a specific statutory provision establishes a conditional safe harbor, a general prohibition in a coordinate statute cannot nullify the safe harbor absent express repeal.
* **Ejusdem Generis:** Where general words follow an enumeration of specific classes of things, the general words are construed to apply only to things of the same general nature (*genus*) as those enumerated.
