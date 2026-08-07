"""
GraphOath Standalone Verification & Demo Execution Runner.

Executes test suites and verification scripts across the project and reports objective execution status.
"""

import sys
import os
import subprocess

def run_step(step_name: str, cmd: list) -> bool:
    print(f"\n[EXECUTING VERIFICATION STEP] {step_name}...")
    res = subprocess.run(cmd)
    if res.returncode == 0:
        print(f"  --> [PASS] {step_name}")
        return True
    else:
        print(f"  --> [FAIL] {step_name}")
        return False

def main():
    print("========================================================================")
    print("  GraphOath — Standalone Verification & Evaluation Runner")
    print("========================================================================")
    
    steps = [
        ("Custody Ledger Tamper Pytest Suite", [sys.executable, "-m", "unittest", "tests/test_ledger_tamper.py"]),
        ("Agent Key Signature Verification", [sys.executable, "graphoath/identity.py"]),
        ("Continuous Audit Daemon Verification", [sys.executable, "graphoath/audit_daemon.py"]),
        ("Circuit Breaker & Resilience Verification", [sys.executable, "graphoath/resilience.py"]),
        ("Financial Impact Model Estimator", [sys.executable, "examples/cost_calculator_demo.py"]),
        ("OpenTelemetry Semantic Telemetry Trace Emitter", [sys.executable, "examples/otel_tracing_demo.py"]),
        ("Real-World Multi-Platform Pipeline Triage Simulation", [sys.executable, "examples/realworld_pipeline_triage_demo.py"]),
        ("Documentation Link Integrity Verifier", [sys.executable, "scripts/verify_docs_integrity.py"])
    ]
    
    passed_count = 0
    for name, cmd in steps:
        if run_step(name, cmd):
            passed_count += 1
            
    print("\n========================================================================")
    print(f"  VERIFICATION SUMMARY: {passed_count}/{len(steps)} Steps Completed Successfully")
    print("========================================================================")

if __name__ == "__main__":
    main()
