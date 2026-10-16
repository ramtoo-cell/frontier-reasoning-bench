"""
STEM Evaluation Module: Lattice Cryptography & Cyclotomic Polynomial Rings
Verifies multi-step Ring-LWE reductions: R_q = Z_q[x] / (x^d + 1)
"""

import math
from typing import List, Dict, Any
from bench.core.taxonomy import VerificationResult, OutcomeType

class LatticeCryptoVerifier:
    """
    Deterministic invariant grader for Ring-LWE polynomial arithmetic derivations.
    Verifies step-by-step reduction modulo (x^d + 1) and prime modulus q.
    """
    def __init__(self, degree: int = 4, modulus: int = 17):
        self.d = degree
        self.q = modulus

    def negacyclic_multiply(self, p1: List[int], p2: List[int]) -> List[int]:
        """Exact negacyclic polynomial multiplication in Z_q[x]/(x^d + 1)"""
        d = self.d
        res = [0] * (2 * d)
        for i in range(d):
            for j in range(d):
                res[i + j] = (res[i + j] + p1[i] * p2[j]) % self.q
        
        # Negative wrapped convolution: x^d = -1 mod (x^d + 1)
        for i in range(d - 1, -1, -1):
            res[i] = (res[i] - res[i + d]) % self.q
        return res[:d]

    def verify_step_derivation(self, problem: Dict[str, Any], candidate_steps: List[Dict[str, Any]]) -> VerificationResult:
        p1 = problem["input_poly_a"]
        p2 = problem["input_poly_b"]
        expected_product = self.negacyclic_multiply(p1, p2)

        for idx, step in enumerate(candidate_steps):
            claimed_res = step.get("claimed_coefficients")
            # Step 1: Check intermediate degree reduction
            if step.get("stage") == "convolution":
                raw_prod = [0] * (2 * self.d)
                for i in range(self.d):
                    for j in range(self.d):
                        raw_prod[i + j] = (raw_prod[i + j] + p1[i] * p2[j]) % self.q
                if claimed_res != raw_prod:
                    return VerificationResult(
                        problem_id=problem["id"],
                        track="STEM",
                        subdomain="Lattice_Cryptography",
                        passed=False,
                        outcome=OutcomeType.CALCULATION_DRIFT,
                        score=0.25,
                        failed_step_index=idx,
                        explanation=f"Calculation drift at polynomial outer-product. Expected {raw_prod}, got {claimed_res}"
                    )

            if step.get("stage") == "negacyclic_reduction":
                if claimed_res != expected_product:
                    # Check if model mistakenly applied cyclic reduction (x^d = +1) instead of negacyclic (x^d = -1)
                    cyclic_res = [0] * (2 * self.d)
                    for i in range(self.d):
                        for j in range(self.d):
                            cyclic_res[i + j] = (cyclic_res[i + j] + p1[i] * p2[j]) % self.q
                    for i in range(self.d):
                        cyclic_res[i] = (cyclic_res[i] + cyclic_res[i + self.d]) % self.q
                    if claimed_res == cyclic_res[:self.d]:
                        return VerificationResult(
                            problem_id=problem["id"],
                            track="STEM",
                            subdomain="Lattice_Cryptography",
                            passed=False,
                            outcome=OutcomeType.CALCULATION_DRIFT,
                            score=0.50,
                            failed_step_index=idx,
                            explanation="Critical Ring-LWE error: Model applied cyclic reduction x^d = +1 instead of negacyclic x^d = -1."
                        )
                    return VerificationResult(
                        problem_id=problem["id"],
                        track="STEM",
                        subdomain="Lattice_Cryptography",
                        passed=False,
                        outcome=OutcomeType.CALCULATION_DRIFT,
                        score=0.40,
                        failed_step_index=idx,
                        explanation=f"Incorrect modular reduction in Z_q. Expected {expected_product}, got {claimed_res}"
                    )

        # Final check
        final_answer = candidate_steps[-1].get("claimed_coefficients")
        if final_answer == expected_product:
            return VerificationResult(
                problem_id=problem["id"],
                track="STEM",
                subdomain="Lattice_Cryptography",
                passed=True,
                outcome=OutcomeType.CORRECT,
                score=1.0,
                explanation="Polynomial negacyclic reduction in R_q verified with 100% mathematical fidelity."
            )
        
        return VerificationResult(
            problem_id=problem["id"],
            track="STEM",
            subdomain="Lattice_Cryptography",
            passed=False,
            outcome=OutcomeType.CALCULATION_DRIFT,
            score=0.0,
            failed_step_index=len(candidate_steps)-1,
            explanation=f"Final product mismatch. Expected {expected_product}, got {final_answer}"
        )
