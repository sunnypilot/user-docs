# sunnypilot docs

Source of truth for all [sunnypilot](https://github.com/sunnypilot/sunnypilot) user-facing documentation. Markdown files in `docs/` are built into a static site and synced one-way to the [sunnypilot Community Forum](https://community.sunnypilot.ai).

| Location        | Link                                                              |
|-----------------|-------------------------------------------------------------------|
| **Forum**       | [community.sunnypilot.ai](https://community.sunnypilot.ai)        |
| **Source repo** | [sunnypilot/sunnypilot](https://github.com/sunnypilot/sunnypilot) |

## Quick start

```bash
pip install zensical          # static site generator
zensical build                # build site to site/
```

## Repository structure

```
user-docs/
├── docs/                 # Markdown source files (features, settings, guides, safety)
├── tools/                # Python pipeline for Discourse sync
│   ├── nav_parser.py     # Parse zensical.toml nav tree into flat entries
│   ├── content_cache.py  # SHA-256 hashing to skip unchanged docs
│   ├── converter.py      # MkDocs Material markdown -> Discourse markdown
│   ├── discourse_client.py  # Discourse REST API client (stdlib only)
│   ├── sync_to_discourse.py # Sync orchestrator (entry point)
│   └── test_*.py         # Unit tests for each module
├── .github/workflows/
│   ├── ci.yml            # Lint and test on PR/push to tools/
│   ├── build-docs.yml    # Build site + deploy to GitHub Pages
│   └── sync-docs-discourse.yml  # Run tests, then sync to Discourse
├── zensical.toml         # Site config, nav tree, theme, extensions
└── site/                 # Build output (gitignored)
```

## Testing

Run tests locally before pushing:

```bash
pip install uv zensical ruff

# Lint
ruff check tools/

# Run all tests
python3 tools/test_nav_parser.py
python3 tools/test_content_cache.py
python3 tools/test_converter.py
python3 tools/test_discourse_client.py
python3 tools/test_sync_to_discourse.py

# Or run individual test file
python3 tools/test_converter.py
```

CI runs these on every PR and push to `master` (see `.github/workflows/ci.yml`).

## License

[MIT](LICENSE)
