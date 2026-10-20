# Repository helpers

`repo.py` dispatches small standard-library modules under `repo_support/`. Python 3.11+ is required; your application can use any language. Tests are isolated in `tools/tests/`, not mixed with application tests.

See the [README command reference](../README.md#command-reference). Default commands are inspection-only except explicitly named metadata/scaffolding/cache writes. `verify run` needs `--execute`; `adopt` needs `--apply`. No tool starts a model session, installs a provider, fetches/pushes Git, changes home settings, deploys or enables MCP.

```bash
python tools/repo.py check --tests
python tools/repo.py --help
```

The helpers are not a sandbox, full Markdown renderer, semantic authority validator, security scanner or application CI framework. Keep native app commands native and register only reviewed local checks.
