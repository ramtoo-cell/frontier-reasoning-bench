"""
Unit Tests for Frontier Reasoning Benchmark (5-Discipline Conceptual Reasoning Suite)
Validates that verifiers accurately reward sound reasoning and deterministically flag
injected conceptual fallacies across Philosophy, Cognitive Science, Economics, Policy, and Law.
"""

import unittest
from bench.core.runner import BenchmarkRunner
from bench.core.taxonomy import OutcomeType
from bench.conceptual.mechanism_design_eval import MechanismDesignVerifier
from bench.conceptual.deontic_logic_eval import DeonticLogicVerifier
from bench.conceptual.cognitive_belief_eval import CognitiveBeliefVerifier
from bench.conceptual.policy_tradeoff_eval import PolicyTradeoffVerifier
from bench.conceptual.statutory_interpretation_eval import StatutoryInterpretationVerifier

class TestConceptualReasoningBench(unittest.TestCase):
    def setUp(self):
        self.runner = BenchmarkRunner()

    def test_full_suite_canonical_execution(self):
        results = self.runner.run_suite()
        self.assertEqual(len(results), 10)
        for r in results:
            self.assertTrue(r.passed, f"Problem {r.problem_id} failed: {r.explanation}")

    def test_economics_myerson_satterthwaite_violation(self):
        verifier = MechanismDesignVerifier()
        prob = {"id": "T-ECON", "ground_truth_expected_revenue": 0.333}
        impossible_trace = [{"claims_all_four_simultaneously": True, "external_subsidy_present": False}]
        res = verifier.verify_bilateral_trade(prob, impossible_trace)
        self.assertFalse(res.passed)
        self.assertEqual(res.outcome, OutcomeType.EQUILIBRIUM_INSTABILITY)

    def test_philosophy_deontic_logic_antinomy(self):
        verifier = DeonticLogicVerifier()
        prob = {
            "id": "T-PHIL",
            "has_contrary_to_duty_clause": False,
            "expected_normative_resolution": "SAFE_STATE"
        }
        contradictory_trace = [
            {"action": "transmit_unencrypted_data", "normative_status": "OBLIGATORY"},
            {"action": "transmit_unencrypted_data", "normative_status": "PROHIBITED"},
            {"final_resolution": "SAFE_STATE"}
        ]
        res = verifier.verify_normative_consistency(prob, contradictory_trace)
        self.assertFalse(res.passed)
        self.assertEqual(res.outcome, OutcomeType.DEONTIC_PARADOX_COLLAPSE)

    def test_cogsci_base_rate_neglect_detection(self):
        verifier = CognitiveBeliefVerifier()
        prob = {
            "id": "T-COGSCI",
            "prior_probability": 0.01,
            "true_positive_rate": 0.95,
            "false_positive_rate": 0.05
        }
        # Model commits base-rate neglect by claiming posterior is 0.95 instead of ~0.161
        neglect_trace = [{"claimed_posterior": 0.95}]
        res = verifier.verify_epistemic_update(prob, neglect_trace)
        self.assertFalse(res.passed)
        self.assertEqual(res.outcome, OutcomeType.CALCULATION_DRIFT)

    def test_policy_pareto_vs_kaldor_hicks_conflation(self):
        verifier = PolicyTradeoffVerifier()
        prob = {
            "id": "T-POLICY",
            "status_quo_utilities": [10, 10, 10],
            "candidate_allocations": {
                "Policy_A": [28, 12, 6],
                "Policy_B": [15, 15, 15]
            }
        }
        # Model claims Policy_A is a strict Pareto improvement even though group 3 drops from 10 to 6
        bad_trace = [{"claims_strict_pareto_improvement": True, "evaluated_policy": "Policy_A"}]
        res = verifier.verify_policy_allocation(prob, bad_trace)
        self.assertFalse(res.passed)
        self.assertEqual(res.outcome, OutcomeType.EQUILIBRIUM_INSTABILITY)

    def test_law_lex_specialis_inversion(self):
        verifier = StatutoryInterpretationVerifier()
        prob = {
            "id": "T-LAW",
            "applicable_canon": "LEX_SPECIALIS_DEROGAT_LEGI_GENERALI",
            "expected_liability_outcome": "EXEMPT_UNDER_SAFE_HARBOR"
        }
        bad_trace = [{"general_overrides_specific_without_repeal": True}]
        res = verifier.verify_statutory_construction(prob, bad_trace)
        self.assertFalse(res.passed)
        self.assertEqual(res.outcome, OutcomeType.DEONTIC_PARADOX_COLLAPSE)

if __name__ == "__main__":
    unittest.main()
