"""
Conceptual Reasoning Module: Deontic Modal Logic & Normative Policy Conflicts
Evaluates reasoning over obligations (O), permissions (P), and prohibitions (F).
Prevents deontic collapse, Chisholm's contrary-to-duty paradox, and regulatory antinomies.
"""

from typing import Dict, Any, List, Set
from bench.core.taxonomy import VerificationResult, OutcomeType

class DeonticLogicVerifier:
    """
    Evaluates formal consistency of normative reasoning chains under modal deontic logic (SDL / KD45_n).
    """
    def verify_normative_consistency(self, problem: Dict[str, Any], candidate_steps: List[Dict[str, Any]]) -> VerificationResult:
        obligations: Set[str] = set()
        prohibitions: Set[str] = set()
        permissions: Set[str] = set()

        for idx, step in enumerate(candidate_steps):
            action = step.get("action")
            norm_type = step.get("normative_status")  # "OBLIGATORY", "PROHIBITED", "PERMITTED"

            # Check for Deontic Collapse (O p <-> p)
            if step.get("conflates_is_with_ought") is True:
                return VerificationResult(
                    problem_id=problem["id"],
                    track="CONCEPTUAL",
                    subdomain="Deontic_Modal_Logic",
                    passed=False,
                    outcome=OutcomeType.DEONTIC_PARADOX_COLLAPSE,
                    score=0.2,
                    failed_step_index=idx,
                    explanation="Deontic collapse detected: Reasoning deduced empirical facticity directly from normative obligation (violation of Hume's Guillotine / SDL Axiom D)."
                )

            # Check for direct contradiction under Axiom D: O(p) and F(p) simultaneously
            if norm_type == "OBLIGATORY" and action:
                if action in prohibitions:
                    return VerificationResult(
                        problem_id=problem["id"],
                        track="CONCEPTUAL",
                        subdomain="Deontic_Modal_Logic",
                        passed=False,
                        outcome=OutcomeType.DEONTIC_PARADOX_COLLAPSE,
                        score=0.3,
                        failed_step_index=idx,
                        explanation=f"Axiom D Violation (Normative Antinomy): Action '{action}' declared both obligatory and prohibited without preference ordering or exception clause."
                    )
                obligations.add(action)

            elif norm_type == "PROHIBITED" and action:
                if action in obligations:
                    return VerificationResult(
                        problem_id=problem["id"],
                        track="CONCEPTUAL",
                        subdomain="Deontic_Modal_Logic",
                        passed=False,
                        outcome=OutcomeType.DEONTIC_PARADOX_COLLAPSE,
                        score=0.3,
                        failed_step_index=idx,
                        explanation=f"Axiom D Violation (Normative Antinomy): Action '{action}' declared both prohibited and obligatory simultaneously."
                    )
                prohibitions.add(action)

            # Check resolution of contrary-to-duty (CTD) obligations
            if step.get("resolves_ctd_with_defeasibility") is False and problem.get("has_contrary_to_duty_clause"):
                return VerificationResult(
                    problem_id=problem["id"],
                    track="CONCEPTUAL",
                    subdomain="Deontic_Modal_Logic",
                    passed=False,
                    outcome=OutcomeType.CIRCULAR_JUSTIFICATION,
                    score=0.5,
                    failed_step_index=idx,
                    explanation="Chisholm's Contrary-to-Duty (CTD) paradox unhandled: Failed to use dyadic or defeasible conditional logic for secondary obligations arising upon breach."
                )

        # Final check against expected conclusion
        expected_verdict = problem.get("expected_normative_resolution")
        final_verdict = candidate_steps[-1].get("final_resolution")
        if final_verdict != expected_verdict:
            return VerificationResult(
                problem_id=problem["id"],
                track="CONCEPTUAL",
                subdomain="Deontic_Modal_Logic",
                passed=False,
                outcome=OutcomeType.PREMISE_HALLUCINATION,
                score=0.5,
                failed_step_index=len(candidate_steps)-1,
                explanation=f"Normative resolution mismatch. Expected '{expected_verdict}', got '{final_verdict}'."
            )

        return VerificationResult(
            problem_id=problem["id"],
            track="CONCEPTUAL",
            subdomain="Deontic_Modal_Logic",
            passed=True,
            outcome=OutcomeType.CORRECT,
            score=1.0,
            explanation="Deontic modal logic reasoning verified with no normative antinomies or deontic collapse."
        )
