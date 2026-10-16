"""
Frontier Reasoning Benchmark Runner
Orchestrates problem loading, candidate reasoning trace verification,
and error classification across the 5 Conceptual Reasoning disciplines:
Philosophy, Cognitive Science, Economics, Policy, and Law.
"""

import json
import os
from typing import List, Dict, Any, Optional
from bench.core.taxonomy import VerificationResult, OutcomeType
from bench.conceptual.mechanism_design_eval import MechanismDesignVerifier
from bench.conceptual.deontic_logic_eval import DeonticLogicVerifier
from bench.conceptual.cognitive_belief_eval import CognitiveBeliefVerifier
from bench.conceptual.policy_tradeoff_eval import PolicyTradeoffVerifier
from bench.conceptual.statutory_interpretation_eval import StatutoryInterpretationVerifier

class BenchmarkRunner:
    def __init__(self, data_dir: Optional[str] = None):
        if not data_dir:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(os.path.dirname(base_path), "data")
        self.data_dir = data_dir
        
        self.mechanism_verifier = MechanismDesignVerifier()
        self.deontic_verifier = DeonticLogicVerifier()
        self.cognitive_verifier = CognitiveBeliefVerifier()
        self.policy_verifier = PolicyTradeoffVerifier()
        self.statutory_verifier = StatutoryInterpretationVerifier()

    def load_problems(self, track: str = "ALL") -> List[Dict[str, Any]]:
        conc_path = os.path.join(self.data_dir, "conceptual_problems.json")
        if os.path.exists(conc_path):
            with open(conc_path, "r") as f:
                return json.load(f)
        return []

    def evaluate_trace(self, problem: Dict[str, Any], candidate_trace: List[Dict[str, Any]]) -> VerificationResult:
        subdomain = problem.get("subdomain")
        if subdomain == "Mechanism_Design":
            return self.mechanism_verifier.verify_bilateral_trade(problem, candidate_trace)
        elif subdomain == "Deontic_Modal_Logic":
            return self.deontic_verifier.verify_normative_consistency(problem, candidate_trace)
        elif subdomain == "Cognitive_Science":
            return self.cognitive_verifier.verify_epistemic_update(problem, candidate_trace)
        elif subdomain == "Policy_Governance":
            return self.policy_verifier.verify_policy_allocation(problem, candidate_trace)
        elif subdomain == "Law_Jurisprudence":
            return self.statutory_verifier.verify_statutory_construction(problem, candidate_trace)
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
                trace = self._get_canonical_sample_trace(prob)
            res = self.evaluate_trace(prob, trace)
            results.append(res)
        return results

    def _get_canonical_sample_trace(self, problem: Dict[str, Any]) -> List[Dict[str, Any]]:
        subdomain = problem.get("subdomain")
        if subdomain == "Mechanism_Design":
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
        elif subdomain == "Cognitive_Science":
            prior = problem["prior_probability"]
            sens = problem["true_positive_rate"]
            fpr = problem["false_positive_rate"]
            num = sens * prior
            den = num + fpr * (1.0 - prior)
            post = round(num / den, 4)
            return [
                {"conjunction_exceeds_constituent": False},
                {"claimed_posterior": post}
            ]
        elif subdomain == "Policy_Governance":
            allocs = problem["candidate_allocations"]
            kh_win = max(allocs.keys(), key=lambda k: sum(allocs[k]))
            rawls_win = max(allocs.keys(), key=lambda k: min(allocs[k]))
            return [
                {"claims_strict_pareto_improvement": False},
                {"kaldor_hicks_winner": kh_win},
                {"rawlsian_maximin_winner": rawls_win}
            ]
        elif subdomain == "Law_Jurisprudence":
            return [
                {"general_overrides_specific_without_repeal": False},
                {"applied_canon": problem["applicable_canon"]},
                {"liability_outcome": problem["expected_liability_outcome"]}
            ]
        return []
