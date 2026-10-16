"""
Frontier Reasoning Benchmark CLI
Command-line interface to execute deterministic verification across STEM and Conceptual Reasoning.
"""

import argparse
import sys
import os

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bench.core.runner import BenchmarkRunner
from bench.core.reporter import BenchmarkReporter

def main():
    parser = argparse.ArgumentParser(description="Frontier Reasoning Benchmark (Anthropic Fellowship Focus)")
    parser.add_argument("--track", choices=["ALL", "STEM", "CONCEPTUAL"], default="ALL", help="Reasoning track to evaluate")
    parser.add_argument("--output", choices=["console", "markdown", "json"], default="console", help="Output format")
    args = parser.parse_args()

    runner = BenchmarkRunner()
    results = runner.run_suite(track=args.track)

    if args.output == "markdown":
        print(BenchmarkReporter.generate_markdown_summary(results))
    else:
        print("\n" + "=" * 78)
        print("          FRONTIER REASONING BENCHMARK — EVALUATION EXECUTION")
        print("=" * 78)
        for r in results:
            status = "[PASS]" if r.passed else "[FAIL]"
            print(f"{status} {r.problem_id:<15} [{r.track:<10}] {r.subdomain:<25} Score: {r.score:.2f}")
            if not r.passed:
                print(f"       -> Failure Mode: {r.outcome.value}")
                print(f"       -> Reason: {r.explanation}")
        
        passed = sum(1 for r in results if r.passed)
        print("=" * 78)
        print(f"Total: {passed}/{len(results)} Passed ({passed/len(results)*100:.1f}%) | Mean Score: {sum(r.score for r in results)/len(results):.2f}/1.00")
        print("=" * 78 + "\n")

if __name__ == "__main__":
    main()
