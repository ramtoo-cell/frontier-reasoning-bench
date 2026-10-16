"""
Frontier Reasoning Benchmark Runner
Orchestrates problem loading, candidate reasoning trace verification,
and error classification across STEM and Conceptual tracks.
"""

import json
import os
from typing import List, Dict, Any, Optional
from bench.core.taxonomy import VerificationResult, OutcomeType
from bench.stem.lattice_crypto_eval import LatticeCryptoVerifier
from bench.stem.optical_kv_eval import OpticalKVPhysicsVerifier
from bench.conceptual.mechanism_design_eval import MechanismDesignVerifier
from bench.conceptual.deontic_logic_eval import DeonticLogicVerifier

class BenchmarkRunner:
    def __init__(self, data_dir: Optional[str] = None):
        if not data_dir:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(os.path.dirname(base_path), "data")
        self.data_dir = data_dir
        
        self.lattice_verifier = LatticeCryptoVerifier()
        self.optical_verifier = OpticalKVPhysicsVerifier()
        self.mechanism_verifier = MechanismDesignVerifier()
        self.deontic_verifier = DeonticLogicVerifier()

    def load_problems(self, track: str = "ALL") -> List[Dict[str, Any]]:
        problems = []
        if track in ["ALL", "STEM"]:
            stem_path = os.path.join(self.data_dir, "stem_problems.json")
            if os.path.exists(stem_path):
                with open(stem_path, "r") as f:
                    problems.extend(json.load(f))
        if track in ["ALL", "CONCEPTUAL"]:
            conc_path = os.path.join(self.data_dir, "conceptual_problems.json")
            if os.path.exists(conc_path):
                with open(conc_path, "r") as f:
                    problems.extend(json.load(f))
        return problems

    def evaluate_trace(self, problem: Dict[str, Any], candidate_trace: List[Dict[str, Any]]) -> VerificationResult:
        subdomain = problem.get("subdomain")
        if subdomain == "Lattice_Cryptography":
            return self.lattice_verifier.verify_step_derivation(problem, candidate_trace)
        elif subdomain == "Photonic_Interconnects":
            return self.optical_verifier.verify_photonic_budget(problem, candidate_trace)
        elif subdomain == "Mechanism_Design":
            return self.mechanism_verifier.verify_bilateral_trade(problem, candidate_trace)
        elif subdomain == "Deontic_Modal_Logic":
            return self.deontic_verifier.verify_normative_consistency(problem, candidate_trace)
        else:
            raise ValueError(f"Unknown subdomain: {subdomain}")

    def run_suite(self, track: str = "ALL", traces_by_id: Optional[Dict[str, List[Dict[str, Any]]]] = None) -> List[VerificationResult]:
        problems = self.load_problems(track)
        results = []
        for prob in problems:
            pid = prob["id"]
            if traces_by_id and pid in traces_by_id:
                trace = traces_by_id[pid]
            else:
                # Default to an ideal or sample baseline trace
                trace = self._get_canonical_sample_trace(prob)
            res = self.evaluate_trace(prob, trace)
            results.append(res)
        return results

    def _get_canonical_sample_trace(self, problem: Dict[str, Any]) -> List[Dict[str, Any]]:
        subdomain = problem.get("subdomain")
        if subdomain == "Lattice_Cryptography":
            p1 = problem["input_poly_a"]
            p2 = problem["input_poly_b"]
            expected = self.lattice_verifier.negacyclic_multiply(p1, p2)
            return [
                {"stage": "convolution", "claimed_coefficients": self._raw_poly_mul(p1, p2, 17)},
                {"stage": "negacyclic_reduction", "claimed_coefficients": expected}
            ]
        elif subdomain == "Photonic_Interconnects":
            delta_T = problem["temperature_swing_kelvin"]
            drift = round(delta_T * 0.08, 4)
            coupler_loss = problem["num_grating_couplers"] * problem["coupler_loss_db"]
            prop_loss = problem["waveguide_length_cm"] * problem["propagation_loss_db_per_cm"]
            total_loss = round(coupler_loss + prop_loss, 3)
            margin = problem["laser_power_dbm"] - problem["receiver_sensitivity_dbm"]
            return [
                {"thermal_drift_nm": drift},
                {"total_loss_db": total_loss},
                {"link_feasible": total_loss <= margin}
            ]
        elif subdomain == "Mechanism_Design":
            return [
                {"claims_all_four_simultaneously": False, "external_subsidy_present": False},
                {"optimal_bidding_strategy": "truthful_value" if problem.get("auction_type") == "second_price_sealed_bid" else "shading"},
                {"expected_seller_revenue": problem.get("ground_truth_expected_revenue", 0.333)}
            ]
        elif subdomain == "Deontic_Modal_Logic":
            return [
                {"conflates_is_with_ought": False},
                {"action": "report_anomaly", "normative_status": "OBLIGATORY"},
                {"resolves_ctd_with_defeasibility": True},
                {"final_resolution": problem.get("expected_normative_resolution")}
            ]
        return []

    def _raw_poly_mul(self, p1: List[int], p2: List[int], q: int) -> List[int]:
        d = len(p1)
        res = [0] * (2 * d)
        for i in range(d):
            for j in range(d):
                res[i + j] = (res[i + j] + p1[i] * p2[j]) % q
        return res
