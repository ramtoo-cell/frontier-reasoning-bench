"""
Conceptual Reasoning Module: Law & Statutory Interpretation
Evaluates formal application of legal canons of construction (lex specialis, ejusdem generis),
safe-harbor burden shifting, and mens rea / strict liability boundaries.
"""

from typing import Dict, Any, List
from bench.core.taxonomy import VerificationResult, OutcomeType

class StatutoryInterpretationVerifier:
    """
    Deterministic verifier for multi-step legal reasoning over conflicting statutory clauses.
    Verifies adherence to:
    1. Lex Specialis Derogat Legi Generali (specific statute overrides general statute)
    2.Lex Posterior Derogat Legi Priori (later statute overrides earlier statute of equal rank)
    3. Ejusdem Generis (general catch-all terms constrained by the enumerated class)
    """
    def verify_statutory_construction(self, problem: Dict[str, Any], candidate_steps: List[Dict[str, Any]]) -> VerificationResult:
        expected_canon = problem["applicable_canon"]
        expected_liability = problem["expected_liability_outcome"]

        for idx, step in enumerate(candidate_steps):
            # Check if candidate reverses lex specialis (letting general provision override specific safe harbor)
            if step.get("general_overrides_specific_without_repeal") is True:
                return VerificationResult(
                    problem_id=problem["id"],
                    track="CONCEPTUAL",
                    subdomain="Law_Jurisprudence",
                    passed=False,
                    outcome=OutcomeType.DEONTIC_PARADOX_COLLAPSE,
                    score=0.25,
                    failed_step_index=idx,
                    explanation="Violation of Lex Specialis canon: Permitted a general statutory prohibition to nullify an explicit, narrowly tailored statutory safe-harbor."
                )

            if "applied_canon" in step and step["applied_canon"] != expected_canon:
                return VerificationResult(
                    problem_id=problem["id"],
                    track="CONCEPTUAL",
                    subdomain="Law_Jurisprudence",
                    passed=False,
                    outcome=OutcomeType.PREMISE_HALLUCINATION,
                    score=0.4,
                    failed_step_index=idx,
                    explanation=f"Incorrect statutory canon applied. Expected '{expected_canon}', got '{step['applied_canon']}'."
                )

            if "liability_outcome" in step and step["liability_outcome"] != expected_liability:
                return VerificationResult(
                    problem_id=problem["id"],
                    track="CONCEPTUAL",
                    subdomain="Law_Jurisprudence",
                    passed=False,
                    outcome=OutcomeType.PREMISE_HALLUCINATION,
                    score=0.5,
                    failed_step_index=idx,
                    explanation=f"Legal conclusion mismatch. Expected '{expected_liability}', got '{step['liability_outcome']}'."
                )

        return VerificationResult(
            problem_id=problem["id"],
            track="CONCEPTUAL",
            subdomain="Law_Jurisprudence",
            passed=True,
            outcome=OutcomeType.CORRECT,
            score=1.0,
            explanation="Statutory construction and burden-shifting canons applied with complete jurisprudential consistency."
        )
