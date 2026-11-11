#!/usr/bin/env python3
"""
Master E2E Verification Harness for BF2 Slovenia (Golovec / SE Ljubljana) AAA Level Package.

Usage:
    python3 tests/verify_bf2_level.py [options]

Options:
    --tier {1,2,3,4,all}   Run specific test tier (default: all)
    --level-dir PATH       Path to level directory (default: /home/ator/BF2/levels/slovenia_golovec)
    --verbose, -v          Show detailed test progress
    --report PATH          Save JSON summary report to path
"""

import os
import sys
import argparse
import unittest
import json
import time

# Ensure tests directory is on path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from test_tier1_feature_coverage import TestTier1FeatureCoverage
from test_tier2_boundary_corner import TestTier2BoundaryCorner
from test_tier3_cross_feature import TestTier3CrossFeature
from test_tier4_real_world_gameplay import TestTier4RealWorldGameplay


TIER_MAP = {
    "1": [TestTier1FeatureCoverage],
    "2": [TestTier2BoundaryCorner],
    "3": [TestTier3CrossFeature],
    "4": [TestTier4RealWorldGameplay],
}


class DiagnosticTestResult(unittest.TextTestResult):
    """Custom test result tracking detailed pass/fail diagnostics per test case."""

    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.successes = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes.append(test)


def run_tests(tier: str = "all", level_dir: str = None, verbose: bool = False) -> dict:
    if level_dir:
        os.environ["BF2_LEVEL_DIR"] = os.path.abspath(level_dir)
    else:
        level_dir = os.environ.get("BF2_LEVEL_DIR", "/home/ator/BF2/levels/slovenia_golovec")

    print("=" * 80)
    print("BATTLEFIELD 2 E2E LEVEL VERIFICATION HARNESS")
    print(f"Target Level: {level_dir}")
    print(f"Tier Selection: {tier.upper()}")
    print("=" * 80)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    selected_tiers = ["1", "2", "3", "4"] if tier == "all" else [tier]
    tier_stats = {}

    start_time = time.time()

    total_runs = 0
    total_failures = 0
    total_errors = 0
    total_passed = 0

    failure_details = []

    for t in selected_tiers:
        test_classes = TIER_MAP[t]
        tier_suite = unittest.TestSuite()
        for cls in test_classes:
            tier_suite.addTests(loader.loadTestsFromTestCase(cls))

        runner = unittest.TextTestRunner(
            verbosity=2 if verbose else 1,
            resultclass=DiagnosticTestResult
        )
        print(f"\n--- Running Tier {t} Suite ({tier_suite.countTestCases()} test cases) ---")
        result = runner.run(tier_suite)

        passed = len(result.successes)
        failed = len(result.failures)
        errors = len(result.errors)
        run_count = result.testsRun

        tier_stats[f"Tier {t}"] = {
            "total": run_count,
            "passed": passed,
            "failed": failed,
            "errors": errors
        }

        total_runs += run_count
        total_failures += failed
        total_errors += errors
        total_passed += passed

        for test, trace in result.failures:
            failure_details.append({
                "tier": f"Tier {t}",
                "test": test.id(),
                "type": "FAILURE",
                "message": trace.strip().splitlines()[-1]
            })

        for test, trace in result.errors:
            failure_details.append({
                "tier": f"Tier {t}",
                "test": test.id(),
                "type": "ERROR",
                "message": trace.strip().splitlines()[-1]
            })

    elapsed = time.time() - start_time

    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80)
    print(f"{'Tier':<12} | {'Total':<8} | {'Passed':<8} | {'Failed':<8} | {'Errors':<8} | {'Pass Rate':<10}")
    print("-" * 65)
    for t_name, s in tier_stats.items():
        rate = (s["passed"] / s["total"] * 100.0) if s["total"] > 0 else 0.0
        print(f"{t_name:<12} | {s['total']:<8} | {s['passed']:<8} | {s['failed']:<8} | {s['errors']:<8} | {rate:6.1f}%")
    print("-" * 65)
    overall_rate = (total_passed / total_runs * 100.0) if total_runs > 0 else 0.0
    print(f"{'OVERALL':<12} | {total_runs:<8} | {total_passed:<8} | {total_failures:<8} | {total_errors:<8} | {overall_rate:6.1f}%")
    print(f"Elapsed Time: {elapsed:.2f}s")
    print("=" * 80)

    if failure_details and verbose:
        print("\nDiagnostic Failures:")
        for idx, item in enumerate(failure_details, 1):
            print(f"[{idx}] {item['tier']} - {item['test']}")
            print(f"    {item['type']}: {item['message']}")

    return {
        "level_dir": level_dir,
        "elapsed": elapsed,
        "total_runs": total_runs,
        "total_passed": total_passed,
        "total_failures": total_failures,
        "total_errors": total_errors,
        "tier_stats": tier_stats,
        "failures": failure_details
    }


def main():
    parser = argparse.ArgumentParser(description="Battlefield 2 Level Package E2E Verification Harness")
    parser.add_argument("--tier", choices=["1", "2", "3", "4", "all"], default="all", help="Target test tier")
    parser.add_argument("--level-dir", default=None, help="Path to level directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose test diagnostics")
    parser.add_argument("--report", default=None, help="Path to export JSON summary report")

    args = parser.parse_args()

    results = run_tests(tier=args.tier, level_dir=args.level_dir, verbose=args.verbose)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"\nReport written to: {args.report}")

    if results["total_failures"] > 0 or results["total_errors"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
