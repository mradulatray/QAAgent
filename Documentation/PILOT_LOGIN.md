# Login pilot — findings (RUN_20261102_221949)

Flow verified at runtime: Jobs home → Login → email-first screen (`NGSmartLoginRRVC`) →
`GET /ngprofile/user/emailValidation` → 200 = Registration, 400 = password screen (`NGLoginViewController`).

## Results: 12 automated executed — 10 PASSED, 2 NEEDS_REVIEW; 15 NOT_EXECUTED (need staging/accounts/mocks/manual)

## Needs product decision
| ID | Observation |
|---|---|
| LOGIN_004 | Empty email + Continue: nothing happens, no message ("Please specify your Email ID" never shown) |
| LOGIN_007 | Valid long-TLD email (`.museum`) rejected — regex allows 2–4 letter TLD only |
| LOGIN_011 | Leading space dropped, trailing space → "Please enter a valid email ID" (no trimming) |
| LOGIN_022 | emailValidation 5xx/timeout: code shows no feedback (code review, not executed) |
| LOGIN_027 | Password screen: empty password is not validated before calling login API (code review, not executed) |
| LOGIN_030 | Password max 20 chars — may block longer existing passwords (code review) |

## App issues found (outside login)
- Info.plist `UIAppFonts` lists 6 fonts missing from the bundle: HelveticaNeue.ttc, Lato-Bold.ttf, Lato-Regular.ttf,
  Satoshi-Regular.otf, Satoshi-Medium.otf, TimesNewRoman.ttf. Causes UI-test crashes under Rosetta (worked around).

## Automation lessons applied
- Tapping a static label does not end editing → use keyboard toolbar "Done".
- Email domain suggestion list covers "Continue with email" → end editing before tapping it.
- First run's LOGIN_003 failure was a simulator accessibility-service crash (ENVIRONMENT), passed on re-run.
