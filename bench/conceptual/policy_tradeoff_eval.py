"""
Conceptual Reasoning Module: Public Policy & Social Welfare Trade-Offs
Evaluates Pareto dominance, Kaldor-Hicks potential compensation, and Rawlsian Maximin fairness.
"""

from typing import Dict, Any, List
from bench.core.taxonomy import VerificationResult, OutcomeType

class PolicyTradeoffVerifier:
    """
    Deterministic verifier for policy allocation trade-offs across competing welfare axioms:
    1. Pareto Efficiency (no agent can be made better off without making at least one worse off)
    2. Kaldor-Hicks Efficiency (positive aggregate net surplus; winners could hypothetically compensate losers)
    3. Rawlsian Maximin Criterion (maximizing the minimum utility of the worst-off group)
    """
    def verify_policy_allocation(self, problem: Dict[str, Any], candidate_steps: List[Dict[str, Any]]) -> VerificationResult:
        status_quo = problem["status_quo_utilities"]
        allocations = problem["candidate_allocations"]  # dict of name -> list of group utilities

        # Compute ground-truth welfare properties
        kaldor_hicks_optimal = max(allocations.keys(), key=lambda k: sum(allocations[k]))
        rawlsian_optimal = max(allocations.keys(), key=lambda k: min(allocations[k]))

        for idx, step in enumerate(candidate_steps):
            # Check if candidate conflates Kaldor-Hicks with strict Pareto improvement
            if step.get("claims_strict_pareto_improvement") is True:
                chosen = step.get("evaluated_policy")
                if chosen in allocations:
                    utils = allocations[chosen]
                    is_pareto = all(u >= sq for u, sq in zip(utils, status_quo)) and any(u > sq for u, sq in zip(utils, status_quo))
                    if not is_pareto:
                        return VerificationResult(
                            problem_id=problem["id"],
                            track="CONCEPTUAL",
                            subdomain="Policy_Governance",
                            passed=False,
                            outcome=OutcomeType.EQUILIBRIUM_INSTABILITY,
                            score=0.3,
                            failed_step_index=idx,
                            explanation=f"Conflated Kaldor-Hicks aggregate surplus with strict Pareto improvement: Policy '{chosen}' imposes uncompensated losses on at least one stakeholder group."
                        )

            if "kaldor_hicks_winner" in step and step["kaldor_hicks_winner"] != kaldor_hicks_optimal:
                return VerificationResult(
                    problem_id=problem["id"],
                    track="CONCEPTUAL",
                    subdomain="Policy_Governance",
                    passed=False,
                    outcome=OutcomeType.CALCULATION_DRIFT,
                    score=0.4,
                    failed_step_index=idx,
                    explanation=f"Incorrect Kaldor-Hicks net benefit maximization. Expected '{kaldor_hicks_optimal}', got '{step['kaldor_hicks_winner']}'."
                )

            if "rawlsian_maximin_winner" in step and step["rawlsian_maximin_winner"] != rawlsian_optimal:
                return VerificationResult(
                    problem_id=problem["id"],
                    track="CONCEPTUAL",
                    subdomain="Policy_Governance",
                    passed=False,
                    outcome=OutcomeType.CALCULATION_DRIFT,
                    score=0.5,
                    failed_step_index=idx,
                    explanation=f"Incorrect Rawlsian Maximin floor optimization. Expected '{rawlsian_optimal}', got '{step['rawlsian_maximin_winner']}'."
                )

        return VerificationResult(
            problem_id=problem["id"],
            track="CONCEPTUAL",
            subdomain="Policy_Governance",
            passed=True,
            outcome=OutcomeType.CORRECT,
            score=1.0,
            explanation="Policy trade-offs across Pareto, Kaldor-Hicks, and Rawlsian Maximin criteria verified accurately."
        )
