"""
STEM Evaluation Module: Photonic Interconnects & Optical KV-Cache Physics
Verifies insertion loss budgets, ring resonator thermal drift, and memory scaling invariants.
"""

from typing import Dict, Any, List
from bench.core.taxonomy import VerificationResult, OutcomeType

class OpticalKVPhysicsVerifier:
    """
    Evaluates reasoning over silicon photonic link budgets and near-memory attention latency bounds.
    """
    def __init__(self):
        # Physical constants for silicon photonic waveguides at 1310/1550 nm
        self.d_lambda_dT = 0.08  # nm/K (thermo-optic coefficient for silicon microring resonators)
        self.max_allowable_loss_db = 15.0  # dB link optical power margin

    def verify_photonic_budget(self, problem: Dict[str, Any], candidate_steps: List[Dict[str, Any]]) -> VerificationResult:
        delta_T = problem["temperature_swing_kelvin"]
        laser_power_dbm = problem["laser_power_dbm"]
        receiver_sens_dbm = problem["receiver_sensitivity_dbm"]
        num_couplers = problem["num_grating_couplers"]
        coupler_loss_db = problem["coupler_loss_db"]
        waveguide_len_cm = problem["waveguide_length_cm"]
        propagation_loss_db_per_cm = problem["propagation_loss_db_per_cm"]

        # Exact physical derivations
        expected_thermal_drift = round(delta_T * self.d_lambda_dT, 4)
        total_coupler_loss = num_couplers * coupler_loss_db
        total_prop_loss = waveguide_len_cm * propagation_loss_db_per_cm
        total_insertion_loss = round(total_coupler_loss + total_prop_loss, 3)
        available_margin = laser_power_dbm - receiver_sens_dbm

        for idx, step in enumerate(candidate_steps):
            if "thermal_drift_nm" in step:
                claimed_drift = step["thermal_drift_nm"]
                if abs(claimed_drift - expected_thermal_drift) > 0.005:
                    return VerificationResult(
                        problem_id=problem["id"],
                        track="STEM",
                        subdomain="Photonic_Interconnects",
                        passed=False,
                        outcome=OutcomeType.CALCULATION_DRIFT,
                        score=0.3,
                        failed_step_index=idx,
                        explanation=f"Thermal drift calculation error. Expected {expected_thermal_drift} nm, got {claimed_drift} nm"
                    )

            if "total_loss_db" in step:
                claimed_loss = step["total_loss_db"]
                if abs(claimed_loss - total_insertion_loss) > 0.05:
                    return VerificationResult(
                        problem_id=problem["id"],
                        track="STEM",
                        subdomain="Photonic_Interconnects",
                        passed=False,
                        outcome=OutcomeType.CALCULATION_DRIFT,
                        score=0.5,
                        failed_step_index=idx,
                        explanation=f"Optical insertion loss miscalculated. Expected {total_insertion_loss} dB, got {claimed_loss} dB"
                    )

            if "link_feasible" in step:
                claimed_feasibility = step["link_feasible"]
                expected_feasibility = total_insertion_loss <= available_margin
                if claimed_feasibility != expected_feasibility:
                    return VerificationResult(
                        problem_id=problem["id"],
                        track="STEM",
                        subdomain="Photonic_Interconnects",
                        passed=False,
                        outcome=OutcomeType.PHYSICAL_CONSTRAINT_VIOLATION,
                        score=0.6,
                        failed_step_index=idx,
                        explanation=f"Feasibility decision violated physical optical power margin ({total_insertion_loss} dB vs {available_margin} dB margin)."
                    )

        return VerificationResult(
            problem_id=problem["id"],
            track="STEM",
            subdomain="Photonic_Interconnects",
            passed=True,
            outcome=OutcomeType.CORRECT,
            score=1.0,
            explanation="Optical power budget and microring thermo-optic drift verified accurately."
        )
