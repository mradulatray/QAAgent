"""Test-case repository: dedup by fingerprint, version history, approved tests protected."""
import datetime
import hashlib
import json
import os

from Core.db import AGENT_ROOT, connect, dumps

AUTOMATION_STATUS = {"automated": "AUTOMATED", "observation": "OBSERVATION", "blocked": "BLOCKED",
                     "manual": "MANUAL"}


def _now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def fingerprint(feature, title, steps, data):
    raw = json.dumps([feature.lower(), title.strip().lower(), steps, data], sort_keys=True)
    return hashlib.sha1(raw.encode()).hexdigest()


def import_plan(plan_path):
    """Load a TestPlans/*.json file into the repository as candidates. Returns stats."""
    plan = json.load(open(plan_path))
    conn = connect()
    stats = {"inserted": 0, "updated": 0, "unchanged": 0, "protected_approved": 0, "duplicates": 0}
    for c in plan["cases"]:
        fp = fingerprint(plan["feature"], c["title"], c["steps"], c.get("data", {}))
        row = conn.execute("SELECT * FROM test_cases WHERE test_id=?", (c["id"],)).fetchone()
        dup = conn.execute("SELECT test_id FROM test_cases WHERE fingerprint=? AND test_id<>?", (fp, c["id"])).fetchone()
        if dup:
            stats["duplicates"] += 1
            continue
        values = dict(
            test_id=c["id"], feature=plan["feature"], title=c["title"], scenario_type=c["type"],
            jira_ref=c.get("jira", plan.get("jira_ref", "")), requirement_ref=c.get("req", ""),
            preconditions=c.get("pre", ""), steps=dumps(c["steps"]), test_data=dumps(c.get("data", {})),
            expected=c["expected"], priority=c["priority"], severity=c["severity"],
            automation_status=AUTOMATION_STATUS[c["automation"]], automation_ref=c.get("ref", ""),
            review_flag="NEEDS_REVIEW" if c.get("review") or "NEEDS_REVIEW" in c["expected"] else "",
            review_note=c.get("review", c.get("blocker", "")), source_files=dumps(plan["source_files"]),
            fingerprint=fp)
        if row is None:
            values.update(approval_status="CANDIDATE", version=1, created_at=_now(), updated_at=_now())
            cols = ",".join(values)
            conn.execute("INSERT INTO test_cases(%s) VALUES(%s)" % (cols, ",".join("?" * len(values))),
                         list(values.values()))
            _snapshot(conn, c["id"], 1, values, "created")
            stats["inserted"] += 1
        elif all(str(row[k] if row[k] is not None else "") == str(v) for k, v in values.items()):
            stats["unchanged"] += 1
        elif row["approval_status"] == "APPROVED":
            # Never silently change an approved test: record proposal only.
            _snapshot(conn, c["id"], row["version"] + 1, values, "PROPOSED change to approved test (not applied)")
            stats["protected_approved"] += 1
        else:
            values.update(version=row["version"] + 1, updated_at=_now())
            sets = ",".join("%s=?" % k for k in values)
            conn.execute("UPDATE test_cases SET %s WHERE test_id=?" % sets, list(values.values()) + [c["id"]])
            _snapshot(conn, c["id"], values["version"], values, "candidate updated")
            stats["updated"] += 1
    conn.commit()
    export_files(conn)
    return stats


def _snapshot(conn, test_id, version, values, reason):
    conn.execute("INSERT OR REPLACE INTO test_case_versions(test_id,version,snapshot,changed_at,reason) VALUES(?,?,?,?,?)",
                 (test_id, version, dumps(values), _now(), reason))


def set_approval(test_id, status):
    assert status in ("APPROVED", "CANDIDATE", "EXPLORATORY", "DEPRECATED")
    conn = connect()
    conn.execute("UPDATE test_cases SET approval_status=?, updated_at=? WHERE test_id=?", (status, _now(), test_id))
    conn.commit()
    export_files(conn)


def export_files(conn):
    """Mirror DB into TestRepository/<Approved|Candidates|Exploratory>/<feature>.json for easy review."""
    folders = {"APPROVED": "Approved", "CANDIDATE": "Candidates", "EXPLORATORY": "Exploratory"}
    grouped = {}
    for r in conn.execute("SELECT * FROM test_cases ORDER BY test_id"):
        d = dict(r)
        for k in ("steps", "test_data", "source_files"):
            d[k] = json.loads(d[k] or "null")
        grouped.setdefault((folders.get(d["approval_status"], "Candidates"), d["feature"]), []).append(d)
    for (folder, feature), cases in grouped.items():
        path = os.path.join(AGENT_ROOT, "TestRepository", folder, "%s.json" % feature.lower())
        with open(path, "w") as fh:
            json.dump(cases, fh, indent=2, ensure_ascii=False)
