# Development

This repository contains the initial Python skeleton for the Vercosa AI Framework.

## Scope

The current package is intentionally minimal. It provides:

- project metadata in `pyproject.toml`;
- a provider-agnostic Python package under `src/`;
- a basic CLI with version and diagnostic output;
- core domain primitives for future Clean Architecture layers;
- minimal pytest coverage for the CLI.

It does not implement adapters for OpenCode, OpenAI, PostgreSQL, vector stores, model providers, or runtimes.

## Local Checks

Run syntax compilation:

```bash
python -m compileall src
```

Run tests:

```bash
pytest
```

## Architecture Direction

Core modules should remain independent from external providers and infrastructure. Future integrations should be added as adapters around the core instead of being imported directly by domain models or policies.
