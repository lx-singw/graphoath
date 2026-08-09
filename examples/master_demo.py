"""
GraphOath Master Hackathon Interactive Evaluation Suite.

Provides judges with an interactive CLI menu to run individual or all demo scripts.
"""

import sys
import os
import subprocess

DEMOS = [
    ("1", "Real-World Multi-Platform Pipeline Triage Demo (Snowflake -> dbt -> Looker)", "examples/realworld_pipeline_triage_demo.py"),
    ("2", "End-to-End Citation Gate & Live Tamper Detection Demo", "examples/mock_mcp_citation_demo.py"),
    ("3", "LangChain / LangGraph Agent Integration Demo", "examples/langchain_agent_example.py"),
    ("4", "Financial Cost of Hallucination ROI Model Calculator", "examples/cost_calculator_demo.py"),
    ("5", "OpenTelemetry (OTel) Semantic Telemetry Trace Emitter", "examples/otel_tracing_demo.py"),
    ("6", "Automated Custody Ledger Tamper Detection Pytest Suite", "tests/test_ledger_tamper.py"),
    ("7", "1-Liner Decorator Self-Test Demo", "examples/decorator.py"),
    ("8", "Graph Traversal Circuit Breaker & Resilience Self-Test", "tests/test_resilience.py")
]

def run_script(script_path: str):
    print(f"\n>>> EXECUTING: {script_path}\n" + "-"*70)
    if script_path.endswith(".py") and "tests/" in script_path:
        cmd = [sys.executable, "-m", "pytest", script_path]
    else:
        cmd = [sys.executable, script_path]
    subprocess.run(cmd)

def main():
    print("========================================================================")
    print("  GraphOath — Master Hackathon Interactive Evaluation Suite")
    print("========================================================================")
    for num, name, path in DEMOS:
        print(f"  [{num}] {name}")
    print("  [A] RUN ALL DEMOS SEQUENTIALLY")
    print("  [Q] Quit")
    print("========================================================================")
    
    choice = input("Select an option [1-8, A, Q] (default 'A'): ").strip().upper() or "A"
    
    if choice == "Q":
        print("Exiting evaluation suite. Thank you!")
        return
    elif choice == "A":
        for num, name, path in DEMOS:
            run_script(path)
        print("\n========================================================================")
        print("[OK] All Demos Completed Successfully!")
        print("========================================================================")
    else:
        selected = next((path for num, name, path in DEMOS if num == choice), None)
        if selected:
            run_script(selected)
        else:
            print(f"Invalid option '{choice}'.")

if __name__ == "__main__":
    main()
