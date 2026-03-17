# Handoff — 2026-03-17

## Current task
No active task — repo is clean and stable; last work added session documentation for codebase components and relationships.

## Next steps
- [ ] Begin implementing the target memory architecture per `docs/plans/2026-03-08-agent-memory-architecture.md` — start with artifact metadata models and promotion gating (`models.py`)
- [ ] Add structured metadata store for lifecycle state (confidence, evidence, promotion status, staleness, scope, sync state) — new module alongside `session_manager.py`
- [ ] Expand tests for: artifact metadata validation, promotion gating, handoff generation, retrieval composition, fallback behavior (per CLAUDE.md testing focus)

## Decisions made
- Markdown remains canonical human truth; `qmd` owns retrieval for canonical docs, `Zvec` owns retrieval for promoted machine memory artifacts — do not collapse these layers
- Raw chain-of-thought is ephemeral; only promoted conclusions are durable machine memory — do not store scratch reasoning long-term
- Target architecture is documented in `docs/plans/` — codebase is transitional, treat design docs as authoritative when they conflict with current code
- qmd indexing is a controlled workflow — do not auto-index on every change
