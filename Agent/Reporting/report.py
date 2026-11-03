"""Generate HTML + JSON reports for a run from the SQLite history.
Usage: python3 Agent/Reporting/report.py [RUN_ID]   (default: latest run)
"""
import html
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Core.db import AGENT_ROOT, connect  # noqa: E402

CONFIG = json.load(open(os.path.join(AGENT_ROOT, "Configuration", "agent.json")))
STATUS_ORDER = ["FAILED", "BLOCKED", "NEEDS_REVIEW", "PASSED", "SKIPPED", "NOT_EXECUTED"]


def changed_files():
    try:
        out = subprocess.check_output(["git", "-C", CONFIG["app_repo"], "status", "--porcelain"]).decode()
        return [ln[3:] for ln in out.splitlines() if ln.strip()]
    except subprocess.CalledProcessError:
        return []


def build(run_id=None):
    conn = connect()
    run = conn.execute("SELECT * FROM runs WHERE run_id=?" if run_id else
                       "SELECT * FROM runs ORDER BY started_at DESC LIMIT 1", (run_id,) if run_id else ()).fetchone()
    if not run:
        sys.exit("No runs found.")
    run = dict(run)
    rows = [dict(r) for r in conn.execute(
        "SELECT e.*, t.feature, t.title, t.expected, t.priority, t.severity, t.jira_ref, t.requirement_ref, "
        "t.review_flag, t.review_note, t.automation_status, t.approval_status, t.source_files, t.steps "
        "FROM executions e JOIN test_cases t ON t.test_id=e.test_id WHERE e.run_id=? ORDER BY e.test_id",
        (run["run_id"],))]
    for r in rows:
        r["attachments"] = json.loads(r["attachments"] or "[]")
        r["source_files"] = json.loads(r["source_files"] or "[]")
        r["steps"] = json.loads(r["steps"] or "[]")
    summary = json.loads(run["summary"] or "{}")
    data = {
        "run": run, "summary": summary, "changed_files_uncommitted": changed_files(),
        "affected_features": sorted({r["feature"] for r in rows}),
        "jira_references": sorted({r["jira_ref"] for r in rows if r["jira_ref"]}),
        "total_duration_s": round(sum(r["duration_s"] or 0 for r in rows), 1),
        "candidates_pending_approval": sum(1 for r in rows if r["approval_status"] == "CANDIDATE"),
        "needs_review": [{"test_id": r["test_id"], "note": r["review_note"], "observed": r["actual"]}
                         for r in rows if r["review_flag"] or r["status"] == "NEEDS_REVIEW"],
        "failures": [r for r in rows if r["status"] in ("FAILED", "BLOCKED")],
        "results": rows,
    }
    out_dir = os.path.join(AGENT_ROOT, "Reports", "runs", run["run_id"])
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "report.json"), "w") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    with open(os.path.join(out_dir, "report.html"), "w") as fh:
        fh.write(render_html(data))
    with open(os.path.join(AGENT_ROOT, "Reports", "latest.html"), "w") as fh:
        fh.write(render_html(data, rel_prefix="runs/%s/" % run["run_id"]))
    return os.path.join(out_dir, "report.html")


def esc(v):
    return html.escape(str(v if v is not None else ""))


def render_html(d, rel_prefix=""):
    up = "../../../" if not rel_prefix else "../"
    run, s = d["run"], d["summary"]
    chips = "".join('<div class="chip s-%s"><b>%d</b><span>%s</span></div>' % (k, s.get(k, 0), k.replace("_", " "))
                    for k in STATUS_ORDER)
    meta = [("Run ID", run["run_id"]), ("Started", run["started_at"]), ("Finished", run["finished_at"]),
            ("Kind", run["kind"]), ("Git branch", run["git_branch"]), ("Commit", (run["commit_sha"] or "")[:12]),
            ("App build", run["app_build"]), ("Device", run["device"]), ("Backend", run["environment"]),
            ("Features", ", ".join(d["affected_features"])), ("Jira", ", ".join(d["jira_references"]) or "— (not linked yet)"),
            ("Executed duration", "%ss" % d["total_duration_s"]),
            ("Candidates awaiting approval", d["candidates_pending_approval"])]
    meta_html = "".join("<tr><th>%s</th><td>%s</td></tr>" % (esc(k), esc(v)) for k, v in meta)

    def row(r):
        shots = "".join('<a href="%s%s"><img src="%s%s" loading="lazy"></a>' % (up, esc(a), up, esc(a))
                        for a in r["attachments"][:1])
        review = '<div class="rv">NEEDS_REVIEW: %s</div>' % esc(r["review_note"]) if r["review_flag"] else ""
        return ("<tr><td class='mono'>%s</td><td>%s%s</td><td><span class='st s-%s'>%s</span></td>"
                "<td>%s</td><td>%s</td><td>%s</td><td>%s</td><td class='shot'>%s</td></tr>") % (
            esc(r["test_id"]), esc(r["title"]), review, esc(r["status"]), esc(r["status"].replace("_", " ")),
            esc(r["priority"]), esc(r["expected"]), esc(r["actual"]),
            esc(round(r["duration_s"] or 0, 1)) if r["duration_s"] else "—", shots)

    fails = "".join(
        "<div class='card'><h3>%s — %s</h3><p><b>Classification:</b> %s</p><p><b>Expected:</b> %s</p>"
        "<p><b>Error:</b> <span class='mono'>%s</span></p><p><b>Steps:</b> %s</p><p><b>Source:</b> %s</p></div>" % (
            esc(f["test_id"]), esc(f["title"]), esc(f["failure_class"]), esc(f["expected"]), esc(f["error"]),
            esc(" → ".join(f["steps"])), esc(", ".join(f["source_files"][:3])))
        for f in d["failures"]) or "<p class='muted'>No failures in this run.</p>"
    changed = "".join("<li class='mono'>%s</li>" % esc(c) for c in d["changed_files_uncommitted"]) or "<li>None</li>"
    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>QA Run Report</title>
<style>
:root{--bg:#f6f7f9;--fg:#1b1f24;--muted:#5f6b7a;--card:#fff;--line:#e3e6ea;--pass:#1a7f37;--fail:#cf222e;--warn:#9a6700;--block:#8250df;--na:#6e7781}
@media (prefers-color-scheme:dark){:root{--bg:#0f1216;--fg:#e6edf3;--muted:#9aa5b1;--card:#161b22;--line:#2b323b}}
body{margin:0;font:14px/1.5 -apple-system,system-ui,sans-serif;background:var(--bg);color:var(--fg)}
main{max-width:1200px;margin:0 auto;padding:24px 16px}h1{margin:0 0 4px}h2{margin-top:32px}
.muted{color:var(--muted)}.mono{font-family:ui-monospace,Menlo,monospace;font-size:12px}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}.chip{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:96px}
.chip b{display:block;font-size:22px}.chip span{font-size:12px;color:var(--muted)}
table{width:100%%;border-collapse:collapse;background:var(--card);border:1px solid var(--line);border-radius:8px;overflow:hidden}
th,td{text-align:left;vertical-align:top;padding:8px 10px;border-bottom:1px solid var(--line)}th{font-weight:600}
.meta th{width:220px;color:var(--muted);font-weight:500}.wrap{overflow-x:auto}
.st{font-weight:600;font-size:12px;white-space:nowrap}.s-PASSED{color:var(--pass)}.s-FAILED{color:var(--fail)}
.s-NEEDS_REVIEW{color:var(--warn)}.s-BLOCKED{color:var(--block)}.s-NOT_EXECUTED,.s-SKIPPED{color:var(--na)}
.chip.s-PASSED b{color:var(--pass)}.chip.s-FAILED b{color:var(--fail)}.chip.s-NEEDS_REVIEW b{color:var(--warn)}.chip.s-BLOCKED b{color:var(--block)}
.rv{color:var(--warn);font-size:12px;margin-top:4px}.shot img{width:72px;border-radius:6px;border:1px solid var(--line)}
.card{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--fail);border-radius:8px;padding:12px 16px;margin:10px 0}
</style></head><body><main>
<h1>QA Run Report</h1><div class="muted">NaukriGulf iOS · qaAgent · %s</div>
<div class="chips">%s</div>
<table class="meta">%s</table>
<h2>Failures</h2>%s
<h2>All tests</h2><div class="wrap"><table><tr><th>ID</th><th>Test</th><th>Status</th><th>Pri</th><th>Expected</th><th>Actual / observation</th><th>Sec</th><th>Shot</th></tr>%s</table></div>
<h2>Uncommitted changes in app repo</h2><ul>%s</ul>
<p class="muted">PASSED is only reported for tests that actually executed. NOT EXECUTED = needs staging/test accounts/mocks or manual. NEEDS REVIEW = expected behaviour undefined; observation recorded.</p>
</main></body></html>""" % (esc(run["run_id"]), chips, meta_html, fails, "".join(row(r) for r in d["results"]), changed)


if __name__ == "__main__":
    print(build(sys.argv[1] if len(sys.argv) > 1 else None))
