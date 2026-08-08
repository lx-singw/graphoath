-- GraphOath Initial Schema DDL Migration & Security Immutability Triggers

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(64) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'operator',
    organization_id VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS custody_receipts (
    id BIGSERIAL PRIMARY KEY,
    receipt_id VARCHAR(64) UNIQUE NOT NULL,
    sequence_number BIGINT UNIQUE NOT NULL,
    previous_hash VARCHAR(64) NOT NULL,
    current_hash VARCHAR(64) NOT NULL,
    agent_id VARCHAR(255) NOT NULL,
    spiffe_id VARCHAR(255) NOT NULL DEFAULT 'spiffe://graphoath.io/agent/deposition-v1',
    svid_serial VARCHAR(128) DEFAULT 'svid-serial-0001',
    action_type VARCHAR(128) NOT NULL,
    target_urn VARCHAR(512) NOT NULL,
    evidence_payload JSONB NOT NULL DEFAULT '[]'::jsonb,
    claims_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    gate_decision VARCHAR(32) NOT NULL DEFAULT 'APPROVED',
    confidence_score DOUBLE PRECISION NOT NULL DEFAULT 1.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_custody_target_urn ON custody_receipts(target_urn);
CREATE INDEX IF NOT EXISTS idx_custody_spiffe_id ON custody_receipts(spiffe_id);
CREATE INDEX IF NOT EXISTS idx_custody_created_at ON custody_receipts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_custody_current_hash ON custody_receipts(current_hash);

-- Immutability Trigger: Block UPDATE or DELETE on custody_receipts
CREATE OR REPLACE FUNCTION prevent_receipt_mutation()
RETURNS TRIGGER AS $$
BEGIN
    RAISE EXCEPTION 'GRAPH-OATH SECURITY VIOLATION: Custody receipts are immutable and cannot be updated or deleted.';
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS enforce_receipt_immutability ON custody_receipts;
CREATE TRIGGER enforce_receipt_immutability
BEFORE UPDATE OR DELETE ON custody_receipts
FOR EACH ROW EXECUTE FUNCTION prevent_receipt_mutation();

CREATE TABLE IF NOT EXISTS ledger_audit_log (
    id BIGSERIAL PRIMARY KEY,
    verification_id VARCHAR(64) UNIQUE NOT NULL,
    status VARCHAR(32) NOT NULL, -- 'PASSED', 'TAMPERED', 'HEALTHY', 'CORRUPTED'
    total_records_checked BIGINT NOT NULL,
    tampered_receipt_id VARCHAR(64),
    execution_time_ms DOUBLE PRECISION NOT NULL,
    verified_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS hitl_approvals (
    id BIGSERIAL PRIMARY KEY,
    approval_id VARCHAR(64) UNIQUE NOT NULL,
    receipt_id VARCHAR(64) REFERENCES custody_receipts(receipt_id),
    status VARCHAR(32) NOT NULL DEFAULT 'PENDING',
    requested_by_spiffe_id VARCHAR(255) NOT NULL,
    approved_by_user VARCHAR(255),
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS receipts (
    receipt_id VARCHAR(128) PRIMARY KEY,
    module VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    trigger_info JSONB NOT NULL,
    claim TEXT NOT NULL,
    evidence JSONB NOT NULL,
    confidence VARCHAR(20) NOT NULL DEFAULT 'high',
    action_taken JSONB NOT NULL,
    hash VARCHAR(64) NOT NULL,
    prev_hash VARCHAR(64) NOT NULL,
    prior_receipts JSONB DEFAULT '[]'::jsonb,
    memory_note TEXT
);

CREATE INDEX IF NOT EXISTS idx_receipts_created_at ON receipts (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_receipts_hash ON receipts (hash);

CREATE TABLE IF NOT EXISTS approval_actions (
    action_id VARCHAR(64) PRIMARY KEY,
    receipt_id VARCHAR(128) REFERENCES receipts(receipt_id),
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    requires_role VARCHAR(50) NOT NULL DEFAULT 'operator',
    approver_note TEXT,
    approved_by VARCHAR(64),
    approved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
