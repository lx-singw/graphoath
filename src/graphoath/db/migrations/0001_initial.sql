-- GraphOath Initial Schema DDL Migration

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(64) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'operator',
    organization_id VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
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
