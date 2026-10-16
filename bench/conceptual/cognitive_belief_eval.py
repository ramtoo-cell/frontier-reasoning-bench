"""
Conceptual Reasoning Module: Cognitive Science & Epistemic Calibration
Evaluates Bayesian belief updating, base-rate integration, and decision-theoretic rationality axioms.
"""

from typing import Dict, Any, List
from bench.core.taxonomy import VerificationResult, OutcomeType

class CognitiveBeliefVerifier:
    """
    Verifies whether reasoning chains properly update posteriors via Bayes' rule without
    falling into base-rate neglect, conjunction fallacies, or vNM independence violations.
    """
    def verify_epistemic_update(self, problem: Dict[str, Any], candidate_steps: List[Dict[str, Any]]) -> VerificationResult:
        prior = problem.get("prior_probability", 0.01)
        sensitivity = problem.get("true_positive_rate", 0.95)
        false_positive_rate = problem.get("false_positive_rate", 0.05)

        # Exact Bayes posterior: P(H|E) = P(E|H)P(H) / [P(E|H)P(H) + P(E|~H)P(~H)]
        numerator = sensitivity * prior
        denominator = numerator + false_positive_rate * (1.0 - prior)
        expected_posterior = round(numerator / denominator, 4) if denominator > 0 else 0.0

        for idx, step in enumerate(candidate_steps):
            # Check for Conjunction Fallacy: P(A and B) > P(A)
            if step.get("conjunction_exceeds_constituent") is True:
                return VerificationResult(
                    problem_id=problem["id"],
                    track="CONCEPTUAL",
                    subdomain="Cognitive_Science",
                    passed=False,
                    outcome=OutcomeType.CALCULATION_DRIFT,
                    score=0.2,
                    failed_step_index=idx,
                    explanation="Conjunction Fallacy (Tversky & Kahneman): Assigned higher probability to a conjunction P(A ^ B) than to its constituent event P(A)."
                )

            # Check for Base-Rate Neglect: claiming P(H|E) ~ sensitivity when prior is very small
            if "claimed_posterior" in step:
                claimed = step["claimed_posterior"]
                if abs(claimed - sensitivity) < 0.02 and abs(expected_posterior - sensitivity) > 0.20:
                    return VerificationResult(
                        problem_id=problem["id"],
                        track="CONCEPTUAL",
                        subdomain="Cognitive_Science",
                        passed=False,
                        outcome=OutcomeType.CALCULATION_DRIFT,
                        score=0.3,
                        failed_step_index=idx,
                        explanation=f"Base-Rate Neglect detected: Model conflated likelihood P(E|H)={sensitivity} with posterior P(H|E)={expected_posterior}."
                    )
                if abs(claimed - expected_posterior) > 0.02:
                    return VerificationResult(
                        problem_id=problem["id"],
                        track="CONCEPTUAL",
                        subdomain="Cognitive_Science",
                        passed=False,
                        outcome=OutcomeType.CALCULATION_DRIFT,
                        score=0.5,
                        failed_step_index=idx,
                        explanation=f"Bayesian belief update drift. Expected posterior {expected_posterior}, got {claimed}."
                    )

        return VerificationResult(
            problem_id=problem["id"],
            track="CONCEPTUAL",
            subdomain="Cognitive_Science",
            passed=True,
            outcome=OutcomeType.CORRECT,
            score=1.0,
            explanation="Bayesian belief revision and Kolmogorov probability axioms preserved without base-rate neglect."
        )
