Here’s a rough guideline of what we expect when it comes to contributing **safely and responsibly**:

* **Clear purpose:** What’s the PR trying to solve? It should be focused and easy to understand.

* **Minimal scope:** Every line changed should directly support that purpose.

* **Validation:** How did you test it? “Feels great after 100 hours” doesn’t cut it. Show **logs**, **plots**, **comparisons** - proof matters.
  > [!info] **sunnypilot** (*like **openpilot***) is essentially a *data science project* - everything must be data-driven as much as possible.

* **Justification:** If it’s tuning, show before/after graphs. If it’s an optimization, show benchmarks.

* **CI:** PR must pass all tests and include test coverage where applicable. sunnypilot includes scripts that automate most test runs locally or with CI.
