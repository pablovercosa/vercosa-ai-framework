# Persistence Layer MVP

This MVP implements a local filesystem adapter for the Persistence Layer defined by Spec 0013.

## Adapter

`FilesystemRepository` stores one `PersistedRecord` per deterministic JSON file.

Layout:

```text
<root_dir>/<namespace>/<collection>/<record_id>.json
```

The caller configures `root_dir`, `namespace`, and `collection`. Path components are validated to avoid path traversal. The adapter does not use a database, network, external APIs, `sudo`, or global configuration.

## Operations

Supported operations:

- `save(record)` writes or replaces a JSON record.
- `get(ref)` retrieves by `record_id`, or by `entity_type` and `entity_id` when no `record_id` is provided.
- `list(query_filter)` returns records in deterministic order and supports the existing `QueryFilter` fields.
- `delete(ref)` removes a record by ID or entity reference.

## Determinism

JSON is serialized with sorted keys, stable indentation, ASCII escaping, and a trailing newline. A `content_hash` is calculated from the canonical JSON representation excluding the `content_hash` field itself.

## Secret Warning

When `record.metadata["secret_warning"]` is truthy, the adapter redacts the payload before writing it to disk and records `secret_warning_payload_redaction` in `redactions_applied`. This MVP chooses fail-safe redaction over secret inference to avoid persisting marked secrets in cleartext.

## Testability

The adapter is designed for `tmp_path` tests and local-first execution. It is not a final production storage contract and does not provide locks, migrations, backup, encryption, or database semantics.
