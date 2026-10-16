"""
Benchmark Reporter
Generates console summary reports and GitHub markdown leaderboards across the 5 Conceptual Reasoning disciplines.
"""

from typing import List
from bench.core.taxonomy import VerificationResult

class BenchmarkReporter:
    @staticmethod
    def generate_markdown_summary(results: List[VerificationResult]) -> str:
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        avg_score = sum(r.score for r in results) / total if total > 0 else 0.0

        lines = [
            "# Frontier Reasoning Benchmark — Conceptual Reasoning Evaluation Report",
            "",
            f"**Overall Accuracy:** {passed}/{total} ({passed/total*100:.1f}%) | **Mean Invariant Score:** {avg_score:.2f} / 1.00",
            "",
            "## Discipline Breakdown",
            "",
            "| Discipline | Subdomain | Pass Rate | Mean Score | Status |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ]

        subdomains = [
            ("Economics", "Mechanism_Design"),
            ("Philosophy", "Deontic_Modal_Logic"),
            ("Cognitive Science", "Cognitive_Science"),
            ("Policy & Governance", "Policy_Governance"),
            ("Law & Jurisprudence", "Law_Jurisprudence"),
        ]

        for label, sub in subdomains:
            sub_res = [r for r in results if r.subdomain == sub]
            sub_pass = sum(1 for r in sub_res if r.passed)
            sub_avg = sum(r.score for r in sub_res) / len(sub_res) if sub_res else 0.0
            lines.append(
                f"| **{label}** | `{sub}` | {sub_pass}/{len(sub_res)} ({sub_pass/len(sub_res)*100 if sub_res else 0:.1f}%) | {sub_avg:.2f} | Verified |"
            )

        lines.extend([
            "",
            "## Detailed Case Outcomes",
            "",
            "| Problem ID | Subdomain | Result | Score | Invariant Verification Explanation |",
            "| :--- | :--- | :---: | :---: | :--- |"
        ])

        for r in results:
            icon = "✅ PASS" if r.passed else "❌ FAIL"
            lines.append(f"| `{r.problem_id}` | `{r.subdomain}` | {icon} | {r.score:.2f} | {r.outcome.value} — {r.explanation} |")

        return "\n".join(lines)
