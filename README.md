# DemoShop Web UI Test Automation (Selenium + Python + pytest)

Automated UI tests for a small simulated web application ("DemoShop"). The suite covers six
critical user workflows with 26 test cases and uses the Page Object Model for maintainability.

## Tech stack
| Item | Choice |
|---|---|
| Language | Python 3.9+ |
| Automation | Selenium WebDriver 4 |
| Runner / assertions | pytest |
| Reporting | pytest-html (`reports/report.html`) |
| Browser | Chrome (default) or Firefox |

## Simulated environment
The `mock_app/` folder contains a tiny static web app so the tests are runnable end-to-end.
`run_mock_server.py` serves it at `http://localhost:8000` (started/stopped automatically by pytest).
To test a different app, set `BASE_URL` and `START_MOCK_SERVER=false`.

**Valid credentials:** `testuser` / `Password123!`

### URL structure
| Page | Path | Auth required |
|---|---|---|
| Login | `/login.html` | No |
| Dashboard | `/dashboard.html` | Yes |
| Products | `/products.html` | Yes |
| Contact | `/contact.html` | Yes |
| Unknown URL | any other path | returns HTTP 404 page |

### Element locators assumed
| Page | Element | Locator |
|---|---|---|
| Login | Username / Password / Button / Error | `#username` / `#password` / `#login-button` / `#login-error` |
| Dashboard | Welcome text / Nav links / Logout | `#welcome-message` / `#nav-dashboard`, `#nav-products`, `#nav-contact` / `#logout-button` |
| Products | Search box / button / cards / empty msg | `#search-input` / `#search-button` / `.product-card` / `#no-results` |
| Contact | Fields / Submit | `#name`, `#email`, `#message` / `#submit-button` |
| Contact | Messages | `#success-message`, `#name-error`, `#email-error`, `#message-error` |
| 404 page | Heading | `#error-title` |

### Application rules assumed
* Login: both fields required; only `testuser` / `Password123!` succeeds; otherwise an error shows and the user stays on `/login.html`.
* Contact form: name required; email must look like `x@y.z`; message at least 10 characters.
* Search: case-insensitive "contains" filter; "No products found" when nothing matches.
* Protected pages redirect anonymous users to `/login.html`; logout clears the session.

## Workflows and test files
| # | Workflow | File | Tests |
|---|---|---|---|
| 1 | Login (valid / invalid) | `tests/test_login.py` | 5 |
| 2 | Form submission | `tests/test_form_submission.py` | 6 |
| 3 | Navigation | `tests/test_navigation.py` | 4 |
| 4 | Product search | `tests/test_search.py` | 5 |
| 5 | Logout and session protection | `tests/test_session_and_errors.py` | 6 (incl. 404) |
| 6 | Error handling (404 page) | `tests/test_session_and_errors.py` | (included above) |

## Project structure
```
config/settings.py        URLs, timeouts, browser, test data (env-overridable)
pages/                    Page Objects (locators + actions, no assertions)
tests/conftest.py         Fixtures: server, driver, logged-in session, failure screenshots
tests/test_*.py           Test cases (assertions only)
mock_app/                 Simulated web application
run_mock_server.py        Local server for the mock app
```

## How to run
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest                           # all tests, headless Chrome
pytest -m smoke                  # only smoke tests
pytest -m negative               # only error-handling tests
pytest tests/test_login.py       # a single file
HEADLESS=false pytest            # watch the browser (Windows: set HEADLESS=false)
BROWSER=firefox pytest           # use Firefox
```
Requires Google Chrome (or Firefox) installed; Selenium Manager downloads the driver automatically.

Outputs: `reports/report.html` (HTML report) and `screenshots/` (one PNG per failed test).

## Best practices applied
* Page Object Model - locators live in one place; tests read like user stories.
* Explicit waits only (no `time.sleep`).
* Setup/teardown via pytest fixtures; browser always closed, even on failure.
* Independent tests with a fresh browser each (no ordering dependency).
* Data-driven tests with `parametrize`; test data separated from test logic.
* Failure handling: automatic screenshot on failure; screenshot errors never mask the real failure.
* Markers (`smoke`, `negative`) for selective runs.
