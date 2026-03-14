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
│   ├── build-docs.yml    # Build site + deploy to GitHub Pages
│   └── sync-docs-discourse.yml  # Run tests, then sync to Discourse
├── zensical.toml         # Site config, nav tree, theme, extensions
└── site/                 # Build output (gitignored)
```

## License

[MIT](LICENSE)
