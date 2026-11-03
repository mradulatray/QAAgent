"""Persistent SQLite store for the QA agent (knowledge base + test repository + history)."""
import json
import os
import sqlite3

AGENT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(AGENT_ROOT, "TestRepository", "qa_agent.sqlite")

SCHEMA = """
CREATE TABLE IF NOT EXISTS source_files (
    path TEXT PRIMARY KEY, kind TEXT, sha1 TEXT, feature TEXT, scanned_at TEXT
);
CREATE TABLE IF NOT EXISTS symbols (
    id INTEGER PRIMARY KEY, path TEXT, name TEXT, kind TEXT, superclass TEXT, line INTEGER
);
CREATE INDEX IF NOT EXISTS idx_symbols_path ON symbols(path);
CREATE TABLE IF NOT EXISTS endpoints (
    id INTEGER PRIMARY KEY, path TEXT, enum_name TEXT, case_name TEXT, url_path TEXT, http_method TEXT
);
CREATE INDEX IF NOT EXISTS idx_endpoints_path ON endpoints(path);
CREATE TABLE IF NOT EXISTS features (
    name TEXT PRIMARY KEY, folder TEXT, file_count INTEGER, view_controllers INTEGER, view_models INTEGER
);
CREATE TABLE IF NOT EXISTS requirements (
    id TEXT PRIMARY KEY, source TEXT, title TEXT, body TEXT, status TEXT, updated_at TEXT
);
CREATE TABLE IF NOT EXISTS test_cases (
    test_id TEXT PRIMARY KEY, feature TEXT, title TEXT, scenario_type TEXT,
    jira_ref TEXT, requirement_ref TEXT, preconditions TEXT, steps TEXT, test_data TEXT,
    expected TEXT, priority TEXT, severity TEXT, automation_status TEXT, automation_ref TEXT,
    approval_status TEXT, review_flag TEXT, review_note TEXT, source_files TEXT,
    fingerprint TEXT UNIQUE, version INTEGER DEFAULT 1, created_at TEXT, updated_at TEXT
);
CREATE TABLE IF NOT EXISTS test_case_versions (
    test_id TEXT, version INTEGER, snapshot TEXT, changed_at TEXT, reason TEXT,
    PRIMARY KEY (test_id, version)
);
CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY, started_at TEXT, finished_at TEXT, kind TEXT, git_branch TEXT,
    commit_sha TEXT, app_build TEXT, device TEXT, environment TEXT, result_bundle TEXT, summary TEXT
);
CREATE TABLE IF NOT EXISTS executions (
    id INTEGER PRIMARY KEY, run_id TEXT, test_id TEXT, status TEXT, duration_s REAL,
    actual TEXT, error TEXT, failure_class TEXT, attachments TEXT
);
"""


def connect():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def dumps(value):
    return json.dumps(value, ensure_ascii=False)
