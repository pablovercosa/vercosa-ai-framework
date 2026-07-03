# Persistence Module

Links principais: [README principal](../../../README.md) | [Índice de módulos](../../../docs/architecture/module-index.md) | [Spec 0013](../../../specs/framework/0013-persistence-layer.md)

## Objetivo

Fornecer contratos e adapter filesystem inicial para persistir registros do framework sem fixar banco ou storage.

## O Que Este Módulo Faz

- Define referências de entidade, registros persistidos, resultados e filtros.
- Define contrato genérico `Repository`.
- Implementa `FilesystemRepository` com JSON determinístico e hash de conteúdo.
- Redige campos sensíveis básicos antes de gravação.

## O Que Este Módulo Não Faz

- Não implementa SQLite, PostgreSQL ou pgvector.
- Não define schema físico final.
- Não substitui stores de domínio especializados.
- Não executa migrations.
- Não armazena segredos em claro por decisão arquitetural.

## Principais Arquivos

| Arquivo | Responsabilidade |
| --- | --- |
| `types.py` | Tipos de persistência, records e filtros. |
| `repository.py` | Contrato abstrato `Repository`. |
| `filesystem.py` | Adapter `FilesystemRepository`. |
| `__init__.py` | Exportações públicas do módulo. |

## Principais Tipos, Classes E Funções

- `EntityRef`: referência a entidade de domínio.
- `PersistedRecord`: envelope persistível determinístico.
- `PersistenceResult`: resultado de operação.
- `QueryFilter`: filtros simples.
- `Repository`: porta abstrata.
- `FilesystemRepository`: adapter local em filesystem.

## Entradas E Saídas

Entradas:

- `PersistedRecord` com payload serializável.
- `QueryFilter` para listagem ou busca simples.

Saídas:

- Arquivos JSON determinísticos no adapter filesystem.
- `PersistenceResult` e `PersistedRecord` carregado.

## Dependências Internas

- Não deve depender de módulos de domínio concretos.

## Módulos Relacionados

- Acima: [missions](../missions/README.md), [workflows](../workflows/README.md), [tasks](../tasks/README.md), [knowledge](../knowledge/README.md), [canonicalizer](../canonicalizer/README.md).
- Abaixo: filesystem local, SQLite, PostgreSQL e pgvector como adapters futuros.
- Transversal: [guardian](../guardian/README.md), [model_selection](../model_selection/README.md).

## Specs Correspondentes

- [Spec 0013: Persistence Layer](../../../specs/framework/0013-persistence-layer.md)

## Docs Relacionadas

- [Persistence Layer](../../../docs/persistence-layer.md)
- [Architecture Map](../../../docs/alignment/architecture-map.md)
- [Open Questions](../../../docs/alignment/open-questions.md)

## Exemplo Mínimo

```python
from pathlib import Path
from vercosa_ai_framework.persistence import EntityRef, FilesystemRepository, PersistedRecord

repo = FilesystemRepository(Path(".vaf/state"))
record = PersistedRecord(
    record_type="example",
    entity_ref=EntityRef(entity_type="example", entity_id="1"),
    payload={"ok": True},
)
repo.save(record)
```

## Status Atual

Status: `MVP`.

O módulo oferece porta e adapter filesystem inicial, mas schemas por domínio, migrations e adapters de banco ainda são futuros.

## Próximos Passos

- Definir stores por domínio e audit log.
- Decidir ordem de adapters futuros: filesystem, SQLite, PostgreSQL e pgvector.
