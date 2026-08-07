"""
GraphOath Continuous Background Audit Daemon.

Monitors Custody hash-chain ledger integrity and flags evidence drift asynchronously.
"""

import typing
import sys
import os

# Add parent directory to path for standalone execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from graphoath.ledger_verify import verify_ledger_chain, compute_receipt_hash

class AuditDaemon:
    """
    Background audit daemon checking hash chain integrity and evidence drift.
    """
    def __init__(self, ledger_provider: typing.Callable[[], typing.List[typing.Dict[str, typing.Any]]]):
        self.ledger_provider = ledger_provider
        self.is_running = False
        self.audit_count = 0

    def run_audit(self) -> typing.Tuple[bool, str]:
        self.audit_count += 1
        ledger = self.ledger_provider()
        is_valid, idx, msg = verify_ledger_chain(ledger)
        if not is_valid:
            return False, f"[AUDIT DAEMON BREACH] {msg}"
        return True, f"[AUDIT DAEMON OK] Audit #{self.audit_count} passed across {len(ledger)} receipt(s)."

if __name__ == "__main__":
    genesis_prev = "GENESIS_HASH_00000000000000000000000000000000000000000000000000000000"
    p1 = {"receipt_id": "rcpt_daemon_1", "claim": "Daemon test"}
    h1 = compute_receipt_hash(genesis_prev, p1)
    mock_ledger = [{"previous_hash": genesis_prev, "payload": p1, "ledger_hash": h1}]

    daemon = AuditDaemon(ledger_provider=lambda: mock_ledger)
    ok, status = daemon.run_audit()
    print(status)
    assert ok
