# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Current State

This repository is still the older markdown-only implementation of `sequential-thinking-mcp-v2`. The approved direction is now documented in:

- `docs/plans/2026-03-08-agent-memory-reasoning-architecture-design.md`
- `docs/plans/2026-03-08-agent-memory-architecture.md`

When repository behavior and these design docs disagree, treat the design docs as the target architecture and the codebase as transitional.

## Development Notes

Historical docs reference:

```bash
uv sync
uv run main.py
```

Use those commands only if the dependency manifest exists in the checkout you are working from. Do not assume `pyproject.toml` is present.

## Target Architecture Boundaries

### Memory Layers

- Markdown is canonical human truth.
- `qmd` owns retrieval for canonical docs and document collections.
- `Zvec` owns retrieval for promoted memory artifacts and non-doc semantic artifacts.
- A small structured metadata store owns lifecycle state such as confidence, evidence, promotion status, staleness, scope, and sync state.
- Cloud memory is an optional overlay for continuity, never the source of truth.

### Reasoning Rules

- Scratch reasoning is ephemeral and bounded.
- Checkpoint summaries are recovery artifacts.
- Promoted conclusions are the only durable machine memory.
- Raw chain-of-thought should not be stored as long-term memory by default.
- Promotion requires evidence, sufficient confidence, and likely reuse value.

### Retrieval Rules

- Retrieval is on demand and scoped to the active task.
- Do not preload the whole codebase into context.
- Pass handoff bundles and summaries between agents, not raw transcripts.
- Token ceilings like `64K` active context and `45K` compaction triggers are policy defaults, not universal facts.

### qmd Indexing Policy

Treat qmd indexing as a controlled workflow. Do not automatically spam indexing/update commands on every small change, and do not modify qmd's database directly. Queue or batch indexing work instead.

## Existing Code Map

### Core Files

- `main.py`: current MCP server entry point and tool registration
- `mcp_tools.py`: current tool handlers
- `session_manager.py`: current markdown persistence and session orchestration
- `models.py`: current dataclasses for sessions, thoughts, memories, branches, and package info
- `errors.py`: current exception types

### Current Storage Layout

- `memory-bank/sessions/`: session markdown files
- `memory-bank/memories/`: standalone memory markdown files
- `memory-bank/patterns/`: reserved pattern storage
- `memory-bank/index.md`: session registry

## Implementation Guidance

When changing this repository:

- preserve the distinction between canonical docs and retrievable machine memory
- add explicit artifact and metadata models before adding more retrieval complexity
- prefer stable MCP workflows like `retrieve_context` or `generate_handoff` over low-level storage tools
- keep local-first fallback viable even when cloud providers are configured
- treat documentation updates as part of the architecture, not an afterthought

## Testing Focus

When implementing the target architecture, expand tests around:

- artifact metadata validation
- promotion gating
- handoff generation
- retrieval composition
- fallback behavior between cloud-assisted and local modes
- MCP tool contracts for context retrieval and memory promotion
