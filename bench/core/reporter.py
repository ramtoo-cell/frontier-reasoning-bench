"""
Benchmark Reporter
Generates console summary reports and GitHub markdown leaderboards.
"""

from typing import List, Dict
from bench.core.taxonomy import VerificationResult, OutcomeType

class BenchmarkReporter:
    @staticmethod
    def generate_markdown_summary(results: List[VerificationResult]) -> str:
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        avg_score = sum(r.score for r in results) / total if total > 0 else 0.0

        stem_res = [r for r in results if r.track == "STEM"]
        conc_res = [r for r in results if r.track == "CONCEPTUAL"]

        stem_pass = sum(1 for r in stem_res if r.passed)
        conc_pass = sum(1 for r in conc_res if r.passed)

        lines = [
            "# Frontier Reasoning Benchmark — Evaluation Report",
            "",
            f"**Overall Accuracy:** {passed}/{total} ({passed/total*100:.1f}%) | **Mean Composite Score:** {avg_score:.2f} / 1.00",
            "",
            "## Track Performance",
            "",
            "| Track | Evaluated Domains | Pass Rate | Mean Score | Status |",
            "| :--- | :--- | :--- | :--- | :--- |",
            f"| **STEM Track** | Ring-LWE Lattice Crypto, Optical Interconnect Physics | {stem_pass}/{len(stem_res)} ({stem_pass/len(stem_res)*100 if stem_res else 0:.1f}%) | {sum(r.score for r in stem_res)/len(stem_res) if stem_res else 0:.2f} | Verified |",
            f"| **Conceptual Reasoning** | Mechanism Design (Auctions), Deontic Modal Logic | {conc_pass}/{len(conc_res)} ({conc_pass/len(conc_res)*100 if conc_res else 0:.1f}%) | {sum(r.score for r in conc_res)/len(conc_res) if conc_res else 0:.2f} | Verified |",
            "",
            "## Detailed Problem Outcomes",
            "",
            "| Problem ID | Track | Subdomain | Result | Score | Failure Taxonomy / Explanation |",
            "| :--- | :--- | :--- | :---: | :---: | :--- |"
        ]

        for r in results:
            icon = "✅ PASS" if r.passed else "❌ FAIL"
            lines.append(f"| `{r.problem_id}` | {r.track} | {r.subdomain} | {icon} | {r.score:.2f} | {r.outcome} — {r.explanation} |")

        return "\n".join(lines)
