"""
Unit Tests for Frontier Reasoning Benchmark
Validates that verifiers correctly classify mathematically sound derivations
as well as intentionally injected reasoning bugs and fallacies.
"""

import unittest
from bench.core.runner import BenchmarkRunner
from bench.core.taxonomy import OutcomeType
from bench.stem.lattice_crypto_eval import LatticeCryptoVerifier
from bench.stem.optical_kv_eval import OpticalKVPhysicsVerifier
from bench.conceptual.mechanism_design_eval import MechanismDesignVerifier
from bench.conceptual.deontic_logic_eval import DeonticLogicVerifier

class TestFrontierReasoningBench(unittest.TestCase):
    def setUp(self):
        self.runner = BenchmarkRunner()

    def test_lattice_crypto_negacyclic_soundness(self):
        verifier = LatticeCryptoVerifier(degree=4, modulus=17)
        prob = {
            "id": "T-LATTICE",
            "input_poly_a": [1, 2, 0, 0],
            "input_poly_b": [3, 0, 1, 0]
        }
        # Correct derivation
        expected = verifier.negacyclic_multiply(prob["input_poly_a"], prob["input_poly_b"])
        trace = [{"stage": "negacyclic_reduction", "claimed_coefficients": expected}]
        res = verifier.verify_step_derivation(prob, trace)
        self.assertTrue(res.passed)
        self.assertEqual(res.outcome, OutcomeType.CORRECT)

    def test_lattice_crypto_cyclic_error_detection(self):
        verifier = LatticeCryptoVerifier(degree=4, modulus=17)
        prob = {
            "id": "T-LATTICE-FAIL",
            "input_poly_a": [1, 2, 0, 0],
            "input_poly_b": [0, 0, 0, 1]  # x^3
        }
        # Injected error: model claims cyclic reduction (x^4 = +1) instead of negacyclic (x^4 = -1)
        cyclic_bad_trace = [{"stage": "negacyclic_reduction", "claimed_coefficients": [0, 0, 0, 1]}]
        res = verifier.verify_step_derivation(prob, cyclic_bad_trace)
        self.assertFalse(res.passed)
        self.assertEqual(res.outcome, OutcomeType.CALCULATION_DRIFT)

    def test_photonic_budget_thermal_drift_check(self):
        verifier = OpticalKVPhysicsVerifier()
        prob = {
            "id": "T-OPT",
            "temperature_swing_kelvin": 10.0,
            "laser_power_dbm": 5.0,
            "receiver_sensitivity_dbm": -15.0,
            "num_grating_couplers": 2,
            "coupler_loss_db": 1.0,
            "waveguide_length_cm": 5.0,
            "propagation_loss_db_per_cm": 0.5
        }
        # Correct trace
        trace = [
            {"thermal_drift_nm": 0.8},
            {"total_loss_db": 4.5},
            {"link_feasible": True}
        ]
        res = verifier.verify_photonic_budget(prob, trace)
        self.assertTrue(res.passed)

        # Injected drift error
        bad_trace = [{"thermal_drift_nm": 1.5}]
        bad_res = verifier.verify_photonic_budget(prob, bad_trace)
        self.assertFalse(bad_res.passed)
        self.assertEqual(bad_res.outcome, OutcomeType.CALCULATION_DRIFT)

    def test_mechanism_design_myerson_satterthwaite_violation(self):
        verifier = MechanismDesignVerifier()
        prob = {"id": "T-ECON", "ground_truth_expected_revenue": 0.333}
        # Model claims an impossible bilateral trade mechanism
        impossible_trace = [{"claims_all_four_simultaneously": True, "external_subsidy_present": False}]
        res = verifier.verify_bilateral_trade(prob, impossible_trace)
        self.assertFalse(res.passed)
        self.assertEqual(res.outcome, OutcomeType.EQUILIBRIUM_INSTABILITY)

    def test_deontic_logic_normative_antinomy(self):
        verifier = DeonticLogicVerifier()
        prob = {
            "id": "T-DEONTIC",
            "has_contrary_to_duty_clause": False,
            "expected_normative_resolution": "SAFE_STATE"
        }
        # Injected contradiction: Action A is both obligatory and prohibited
        contradictory_trace = [
            {"action": "transmit_unencrypted_data", "normative_status": "OBLIGATORY"},
            {"action": "transmit_unencrypted_data", "normative_status": "PROHIBITED"},
            {"final_resolution": "SAFE_STATE"}
        ]
        res = verifier.verify_normative_consistency(prob, contradictory_trace)
        self.assertFalse(res.passed)
        self.assertEqual(res.outcome, OutcomeType.DEONTIC_PARADOX_COLLAPSE)

if __name__ == "__main__":
    unittest.main()
