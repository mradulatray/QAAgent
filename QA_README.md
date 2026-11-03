# qaAgent — NaukriGulf iOS QA Testing Agent

Self-contained: all code, config, tests, data and reports live in this folder.
Only exception: generated XCUITests are written into the app repo's `NaukriGulfUITests/Generated/` (synchronized folder).

## Status (2026-11-02)
| Component | State |
|---|---|
| Code scanner + knowledge base (SQLite, incremental) | ✅ working — `Documentation/KNOWLEDGE_BASE.md` |
| Test repository (candidates / approved, dedup, versions, approved-test protection) | ✅ working |
| XCUITest target `NaukriGulfUITests` + Login pilot (12 automated) | ✅ executed: 10 passed, 2 needs review |
| Runner (xcodebuild → xcresult → history, failure classification) | ✅ working |
| HTML/JSON reports | ✅ `Reports/latest.html` |
| Jira integration, file/git monitoring, impact analysis, API tests, CI | ⏳ not built yet |

## Commands
| Command | What it does |
|---|---|
| `./Scripts/scan.sh [--full]` | Scan app code (only changed files) |
| `./Scripts/import-test-plan.sh TestPlans/login_pilot.json` | Load test cases into the repository |
| `./Scripts/run-tests.sh --feature Login` | Run tests for a feature + report |
| `./Scripts/run-tests.sh --tests LOGIN_001,LOGIN_005` | Run specific tests + report |
| `./Scripts/approve-test.sh LOGIN_001 ...` | Promote candidates to the approved regression suite |
| `./Scripts/run-full-regression.sh` | Run all APPROVED tests + report |
| `./Scripts/generate-report.sh [RUN_ID]` | Rebuild a report |

## Layout
| Folder | Contents |
|---|---|
| `Agent/Core` | SQLite schema (`db.py`), test repository (`repository.py`) |
| `Agent/CodeAnalysis` | `scanner.py` — Swift/XIB/storyboard/endpoint scanner |
| `Agent/TestGeneration` | `import_plan.py` |
| `Agent/Execution` | `runner.py` |
| `Agent/Reporting` | `report.py` |
| `TestPlans/` | Source test plans (`login_pilot.json`) |
| `TestRepository/` | `qa_agent.sqlite` + JSON mirrors per approval state |
| `Reports/`, `Screenshots/`, `Logs/` | Run output |
| `Configuration/agent.json` | Paths, simulator, environment |

## Known limitations
- Debug build talks to **production**; network-dependent tests stay NOT_EXECUTED until staging + test accounts exist.
- App runs as x86_64 under Rosetta; UI tests set `OS_ACTIVITY_MODE=disable` to avoid an XCTest crash caused by 6 missing fonts in Info.plist.
- Element lookup uses visible labels (only 1 app file sets accessibility identifiers) — English UI only for now.
- 30 of 121 endpoints have no detected HTTP method (non-standard switch form).
