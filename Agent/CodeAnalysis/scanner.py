"""Incremental static scanner for the NaukriGulf iOS repo.

Walks Swift / XIB / storyboard / plist files, stores symbols, API endpoints and feature mapping
in SQLite. Unchanged files (same SHA-1) are skipped on later runs.
Usage: python3 Agent/CodeAnalysis/scanner.py [--full]
"""
import datetime
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Core.db import AGENT_ROOT, connect  # noqa: E402

CONFIG = json.load(open(os.path.join(AGENT_ROOT, "Configuration", "agent.json")))
REPO = CONFIG["app_repo"]
EXTS = {".swift": "swift", ".xib": "xib", ".storyboard": "storyboard", ".plist": "plist", ".strings": "strings"}

DECL_RE = re.compile(
    r"^\s*(?:@\w+\s+)*(?:(?:final|public|private|fileprivate|internal|open)\s+)*"
    r"(class|struct|enum|protocol)\s+(\w+)\s*(?::\s*([\w\.]+))?")
CASE_RE = re.compile(r"^\s*case\s+(.+?):\s*(?://.*)?$")
RETURN_PATH_RE = re.compile(r'return\s+"(/[^"]*)"')
RETURN_METHOD_RE = re.compile(r"return\s+\.(get|post|put|delete|patch)\b", re.I)
CUSTOM_CLASS_RE = re.compile(r'customClass="(\w+)"')
AX_ID_RE = re.compile(r'<accessibility key="accessibilityConfiguration"[^>]*\bidentifier="[^"]+"')
SWIFT_AX_RE = re.compile(r'\.accessibilityIdentifier\s*=')


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def iter_files():
    for root_name in CONFIG["scan_roots"]:
        base = os.path.join(REPO, root_name)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in CONFIG["ignore_dirs"] and not d.endswith(".xcassets")]
            for fn in filenames:
                ext = os.path.splitext(fn)[1]
                if ext not in EXTS or fn in CONFIG["ignore_files"] or fn.endswith(".orig"):
                    continue
                if ext == ".strings" and "Localizable" not in fn:
                    continue
                full = os.path.join(dirpath, fn)
                yield os.path.relpath(full, REPO), EXTS[ext]


def feature_for(rel):
    root = CONFIG["feature_root"].rstrip("/") + "/"
    if rel.startswith(root):
        return rel[len(root):].split("/")[0]
    parts = rel.split("/")
    if len(parts) >= 3 and parts[1] == "Classes":
        return "Shared/" + parts[2]
    return "Shared/" + (parts[1] if len(parts) > 2 else parts[0])


def symbol_kind(name, superclass):
    sup = superclass or ""
    if name.endswith(("VC", "ViewController", "Controller")) or "ViewController" in sup:
        return "view_controller"
    if name.endswith(("VM", "ViewModel")):
        return "view_model"
    if name.endswith("Cell") or sup.endswith("Cell"):
        return "cell"
    if "EndPoint" in sup or name.endswith(("EndPoint", "EndPoints")):
        return "endpoint_enum"
    if name.endswith(("Model", "Models")) or sup == "Mappable":
        return "model"
    return "type"


def parse_endpoints(lines):
    """Map enum cases to URL path + HTTP method from `var path` / `var httpMethod` switches."""
    enum_name, block, current = None, None, []
    paths, methods = {}, {}
    for ln in lines:
        m = DECL_RE.match(ln)
        if m and m.group(1) == "enum" and enum_name is None:
            enum_name = m.group(2)
        s = ln.strip()
        if s.startswith("var path"):
            block, current = "path", []
            continue
        if s.startswith("var httpMethod"):
            block, current = "method", []
            continue
        if s.startswith("var ") or s.startswith("func "):
            block = None
        if block is None:
            continue
        if s.startswith("default:"):
            current = ["__default__"]
            continue
        cm = CASE_RE.match(ln)
        if cm:
            current = [c.strip().lstrip(".").split("(")[0] for c in cm.group(1).split(",") if c.strip().startswith(".")]
            continue
        if block == "path":
            pm = RETURN_PATH_RE.search(ln)
            if pm:
                for c in current:  # last return wins (non-docker path follows docker branch)
                    paths[c] = pm.group(1)
        else:
            mm = RETURN_METHOD_RE.search(ln)
            if mm:
                for c in current:
                    methods.setdefault(c, mm.group(1).upper())
    fallback = methods.get("__default__", "")
    paths.pop("__default__", None)
    return enum_name, [(c, p, methods.get(c, fallback)) for c, p in sorted(paths.items())]


def scan(full=False):
    conn = connect()
    known = {r["path"]: r["sha1"] for r in conn.execute("SELECT path, sha1 FROM source_files")}
    seen, changed = set(), 0
    for rel, kind in iter_files():
        seen.add(rel)
        data = open(os.path.join(REPO, rel), "rb").read()
        sha = hashlib.sha1(data).hexdigest()
        if not full and known.get(rel) == sha:
            continue
        changed += 1
        text = data.decode("utf-8", errors="ignore")
        lines = text.splitlines()
        conn.execute("DELETE FROM symbols WHERE path=?", (rel,))
        conn.execute("DELETE FROM endpoints WHERE path=?", (rel,))
        if kind == "swift":
            for i, ln in enumerate(lines, 1):
                m = DECL_RE.match(ln)
                if m:
                    conn.execute("INSERT INTO symbols(path,name,kind,superclass,line) VALUES(?,?,?,?,?)",
                                 (rel, m.group(2), symbol_kind(m.group(2), m.group(3)), m.group(3), i))
            ax = len(SWIFT_AX_RE.findall(text))
            if ax:
                conn.execute("INSERT INTO symbols(path,name,kind,superclass,line) VALUES(?,?,?,?,?)",
                             (rel, "accessibilityIdentifiers=%d" % ax, "ax_ids", None, 0))
            if "/EndPoints/" in rel or "EndPointType" in text:
                enum_name, eps = parse_endpoints(lines)
                for case, path, method in eps:
                    conn.execute("INSERT INTO endpoints(path,enum_name,case_name,url_path,http_method) VALUES(?,?,?,?,?)",
                                 (rel, enum_name, case, path, method))
        elif kind in ("xib", "storyboard"):
            for cls in sorted(set(CUSTOM_CLASS_RE.findall(text))):
                conn.execute("INSERT INTO symbols(path,name,kind,superclass,line) VALUES(?,?,?,?,?)",
                             (rel, cls, "ib_reference", None, 0))
            ax = len(AX_ID_RE.findall(text))
            if ax:
                conn.execute("INSERT INTO symbols(path,name,kind,superclass,line) VALUES(?,?,?,?,?)",
                             (rel, "accessibilityIdentifiers=%d" % ax, "ax_ids", None, 0))
        conn.execute("INSERT OR REPLACE INTO source_files(path,kind,sha1,feature,scanned_at) VALUES(?,?,?,?,?)",
                     (rel, kind, sha, feature_for(rel), now()))
    removed = [p for p in known if p not in seen]
    for p in removed:
        for t in ("source_files", "symbols", "endpoints"):
            conn.execute("DELETE FROM %s WHERE path=?" % t, (p,))
    rebuild_features(conn)
    conn.commit()
    return {"files_total": len(seen), "files_rescanned": changed, "files_removed": len(removed)}


def rebuild_features(conn):
    conn.execute("DELETE FROM features")
    conn.execute("""
        INSERT INTO features(name, folder, file_count, view_controllers, view_models)
        SELECT f.feature, f.feature, COUNT(DISTINCT f.path),
               (SELECT COUNT(*) FROM symbols s JOIN source_files g ON g.path=s.path
                 WHERE g.feature=f.feature AND s.kind='view_controller'),
               (SELECT COUNT(*) FROM symbols s JOIN source_files g ON g.path=s.path
                 WHERE g.feature=f.feature AND s.kind='view_model')
        FROM source_files f GROUP BY f.feature""")


def export_knowledge_base():
    conn = connect()
    kb = {
        "generated_at": now(),
        "repo": REPO,
        "counts": {r["kind"]: r["n"] for r in conn.execute("SELECT kind, COUNT(*) n FROM source_files GROUP BY kind")},
        "symbol_counts": {r["kind"]: r["n"] for r in conn.execute("SELECT kind, COUNT(*) n FROM symbols GROUP BY kind")},
        "features": [dict(r) for r in conn.execute("SELECT * FROM features ORDER BY file_count DESC")],
        "endpoints": [dict(r) for r in conn.execute(
            "SELECT enum_name, case_name, http_method, url_path, path AS file FROM endpoints ORDER BY enum_name, case_name")],
        "view_controllers": [dict(r) for r in conn.execute(
            "SELECT s.name, s.path, f.feature FROM symbols s JOIN source_files f ON f.path=s.path "
            "WHERE s.kind='view_controller' ORDER BY f.feature, s.name")],
        "files_with_accessibility_ids": [r["path"] for r in conn.execute(
            "SELECT DISTINCT path FROM symbols WHERE kind='ax_ids'")],
    }
    out_dir = os.path.join(AGENT_ROOT, "Reports", "scan")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "knowledge_base.json"), "w") as fh:
        json.dump(kb, fh, indent=2)

    md = ["# NaukriGulf iOS — Knowledge Base", "", "Generated: %s" % kb["generated_at"], "",
          "## File counts", "", "| Kind | Files |", "|---|---|"]
    md += ["| %s | %d |" % (k, v) for k, v in sorted(kb["counts"].items())]
    md += ["", "## Features (by folder under `%s`)" % CONFIG["feature_root"], "",
           "| Feature | Files | ViewControllers | ViewModels |", "|---|---|---|---|"]
    md += ["| %s | %d | %d | %d |" % (f["name"], f["file_count"], f["view_controllers"], f["view_models"])
           for f in kb["features"]]
    md += ["", "## API endpoints (%d)" % len(kb["endpoints"]), "", "| Enum | Case | Method | Path |", "|---|---|---|---|"]
    md += ["| %s | %s | %s | `%s` |" % (e["enum_name"], e["case_name"], e["http_method"] or "?", e["url_path"])
           for e in kb["endpoints"]]
    with open(os.path.join(AGENT_ROOT, "Documentation", "KNOWLEDGE_BASE.md"), "w") as fh:
        fh.write("\n".join(md) + "\n")
    return kb


if __name__ == "__main__":
    stats = scan(full="--full" in sys.argv)
    kb = export_knowledge_base()
    print(json.dumps({**stats, "features": len(kb["features"]), "endpoints": len(kb["endpoints"]),
                      "view_controllers": len(kb["view_controllers"]),
                      "files_with_accessibility_ids": len(kb["files_with_accessibility_ids"])}, indent=2))
