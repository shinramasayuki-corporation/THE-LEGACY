PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS members (
    id TEXT PRIMARY KEY,
    discord_id TEXT UNIQUE,
    username TEXT NOT NULL,
    preferred_language TEXT NOT NULL DEFAULT 'fr',
    account_status TEXT NOT NULL DEFAULT 'active'
        CHECK (account_status IN ('active', 'suspended', 'deleted')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_key TEXT NOT NULL UNIQUE,
    label TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS member_roles (
    member_id TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    assigned_at TEXT NOT NULL,
    PRIMARY KEY (member_id, role_id),
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS consent_records (
    id TEXT PRIMARY KEY,
    member_id TEXT NOT NULL,
    category TEXT NOT NULL,
    policy_version TEXT NOT NULL,
    granted_at TEXT NOT NULL,
    revoked_at TEXT,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    actor_member_id TEXT,
    action TEXT NOT NULL,
    target_type TEXT NOT NULL,
    target_id TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (actor_member_id) REFERENCES members(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_members_status
ON members(account_status);

CREATE INDEX IF NOT EXISTS idx_member_roles_member
ON member_roles(member_id);

CREATE INDEX IF NOT EXISTS idx_consent_member
ON consent_records(member_id);

CREATE INDEX IF NOT EXISTS idx_audit_created
ON audit_logs(created_at);
