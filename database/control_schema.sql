-- ============================================================================
-- Control Database Schema (control.sqlite)
-- Autonomous Data-to-Decision Application Framework (Skills 01-37)
-- Database Engine: SQLite 3
-- ============================================================================

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;

-- 1. AUTHENTICATION & MULTI-TENANCY (Skill 31)
CREATE TABLE IF NOT EXISTS tenants (
    tenant_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK(status IN ('active', 'suspended', 'archived')) DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'analyst', 'approver', 'viewer')) NOT NULL,
    status TEXT CHECK(status IN ('active', 'inactive')) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    jwt_token_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 2. JOB QUEUE & ASYNCHRONOUS TASKS (Skill 35)
CREATE TABLE IF NOT EXISTS job_queue (
    job_id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    job_type TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    status TEXT CHECK(status IN ('queued', 'processing', 'completed', 'failed', 'cancelled')) DEFAULT 'queued',
    priority INTEGER DEFAULT 5,
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_job_queue_status_priority ON job_queue(status, priority, created_at);

-- 3. HUMAN-IN-THE-LOOP (HITL) APPROVALS (Skill 34)
CREATE TABLE IF NOT EXISTS candidate_actions (
    action_id TEXT PRIMARY KEY,
    tenant_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    net_recovery_amount REAL NOT NULL,
    feasibility_score REAL CHECK(feasibility_score BETWEEN 0 AND 1),
    time_to_value_days INTEGER,
    status TEXT CHECK(status IN ('draft', 'pending_approval', 'approved', 'rejected', 'executed')) DEFAULT 'pending_approval',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS action_approvals (
    approval_id TEXT PRIMARY KEY,
    action_id TEXT NOT NULL,
    tenant_id TEXT NOT NULL,
    reviewer_user_id TEXT NOT NULL,
    decision TEXT CHECK(decision IN ('approved', 'rejected', 'override_approved')) NOT NULL,
    notes TEXT,
    override_amount REAL,
    approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (action_id) REFERENCES candidate_actions(action_id) ON DELETE CASCADE,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_user_id) REFERENCES users(user_id)
);

-- 4. GEMINI API GOVERNANCE & TOKEN LOGS (Skill 36)
CREATE TABLE IF NOT EXISTS gemini_api_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id TEXT NOT NULL,
    user_id TEXT,
    model_name TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    prompt_tokens INTEGER NOT NULL,
    completion_tokens INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,
    estimated_cost_usd REAL NOT NULL,
    latency_ms INTEGER NOT NULL,
    status_code INTEGER DEFAULT 200,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS gemini_quota_tracking (
    tenant_id TEXT PRIMARY KEY,
    daily_token_limit INTEGER DEFAULT 1000000,
    daily_tokens_used INTEGER DEFAULT 0,
    monthly_budget_usd REAL DEFAULT 100.0,
    monthly_spend_usd REAL DEFAULT 0.0,
    last_reset_date TEXT DEFAULT (DATE('now')),
    FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id) ON DELETE CASCADE
);

-- 5. OBSERVABILITY & AUDIT LOGS (Skill 37)
CREATE TABLE IF NOT EXISTS system_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id TEXT,
    trace_id TEXT NOT NULL,
    level TEXT CHECK(level IN ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')) NOT NULL,
    component TEXT NOT NULL,
    message TEXT NOT NULL,
    context_json TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_system_logs_trace_id ON system_logs(trace_id);
CREATE INDEX IF NOT EXISTS idx_system_logs_timestamp ON system_logs(timestamp);

-- Seed Initial System Data
INSERT OR IGNORE INTO tenants (tenant_id, name, status) VALUES ('tenant_demo', 'Acme Corporation (Demo)', 'active');
INSERT OR IGNORE INTO users (user_id, tenant_id, email, password_hash, full_name, role) VALUES ('user_admin', 'tenant_demo', 'admin@acme.com', '$2b$12$eImiTXuWVxfM37uY4JANjOqE2g4i9N9.0zZ92f2N90g9.0zZ92f2N', 'Executive Director', 'admin');
INSERT OR IGNORE INTO gemini_quota_tracking (tenant_id) VALUES ('tenant_demo');