"""
Frontier Reasoning Benchmark - Error Taxonomy
Defines granular classification for reasoning trajectory failures in LLMs.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any

class OutcomeType(str, Enum):
    CORRECT = "CORRECT"
    CALCULATION_DRIFT = "CALCULATION_DRIFT"
    PREMISE_HALLUCINATION = "PREMISE_HALLUCINATION"
    PHYSICAL_CONSTRAINT_VIOLATION = "PHYSICAL_CONSTRAINT_VIOLATION"
    EQUILIBRIUM_INSTABILITY = "EQUILIBRIUM_INSTABILITY"
    DEONTIC_PARADOX_COLLAPSE = "DEONTIC_PARADOX_COLLAPSE"
    CIRCULAR_JUSTIFICATION = "CIRCULAR_JUSTIFICATION"

@dataclass
class VerificationResult:
    problem_id: str
    track: str  # "STEM" or "CONCEPTUAL"
    subdomain: str
    passed: bool
    outcome: OutcomeType
    score: float  # 0.0 to 1.0
    failed_step_index: Optional[int] = None
    explanation: str = ""
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "problem_id": self.problem_id,
            "track": self.track,
            "subdomain": self.subdomain,
            "passed": self.passed,
            "outcome": self.outcome.value,
            "score": round(self.score, 3),
            "failed_step_index": self.failed_step_index,
            "explanation": self.explanation,
            "metadata": self.metadata or {}
        }
