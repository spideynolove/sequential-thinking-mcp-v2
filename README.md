# Sequential Thinking MCP v2

`sequential-thinking-mcp-v2` is a local MCP server for structured reasoning, session persistence, and project memory. The current codebase is the older markdown-only implementation; the repository now also contains an approved design and implementation plan for a layered memory architecture better suited to long-running coding-agent work.

## Architecture Direction

The approved direction is:

- Markdown as canonical human truth
- `qmd` for canonical document retrieval
- `Zvec` for promoted memory artifacts and other non-doc semantic artifacts
- a structured metadata store for lifecycle state
- MCP as the stable tool interface
- cloud-assisted operation first, with local-first fallback when network access fails

Design and plan documents:

- `docs/plans/2026-03-08-agent-memory-reasoning-architecture-design.md`
- `docs/plans/2026-03-08-agent-memory-architecture.md`

## Why This Changes

The current implementation stores sessions and memories as markdown snapshots. That is simple and inspectable, but it is weak for:

- semantic recall across long-running work
- distinguishing scratch reasoning from durable conclusions
- checkpointing and compaction
- large-codebase context management
- reliable handoff between agents or sessions

The target architecture keeps the human-readable markdown layer and adds explicit retrieval, promotion, and metadata boundaries.

## Memory Model

### Canonical Truth

Markdown remains the official human-maintained truth:

- design docs
- ADRs
- runbooks
- module maps
- handoff docs

### Semantic Recall

`Zvec` is intended to index more than just "memories". It should cover promoted non-doc artifacts such as:

- promoted memories
- investigation summaries
- module cards
- stable code summaries
- architecture decisions
- handoff bundles

### Retrieval Ownership Split

- `qmd`: canonical docs and document collections
- `Zvec`: promoted memory objects and other non-doc artifacts
- metadata store: confidence, evidence, provenance, scope, staleness, promotion status, and sync state

This split is intentional. It prevents overlapping retrieval systems from fighting over the same job.

## Reasoning Model

The target reasoning lifecycle is:

- scratch reasoning: local, bounded, disposable
- checkpoint summaries: compact recovery points
- promoted conclusions: reusable machine memory
- canonical docs: durable human truth

Hard rule:

- raw chain-of-thought is not long-term memory by default
- only promoted conclusions should become durable memory

Promotion should be gated by:

- evidence
- confidence
- stability beyond the current task
- likely future reuse

## Token Management

The project should treat token limits as a first-class design problem.

Policy defaults:

- target active context ceiling: `64K`
- compaction trigger example: `45K`

These are engineering defaults, not universal facts. The core idea is:

- retrieve on demand
- checkpoint at subtask boundaries
- compress old context
- pass summaries and handoff bundles instead of raw transcripts

## MCP Integration

MCP is the stable interface layer between the agent and the memory system.

Recommended MCP surface:

- `retrieve_context`
- `search_docs`
- `search_memory`
- `promote_memory`
- `summarize_session`
- `generate_handoff`
- `map_changed_modules`

The current implementation still exposes the original 12 tools. The architecture work in `docs/plans/` describes how that surface should evolve.

## qmd Indexing Policy

`qmd` indexing should remain a controlled workflow. Do not treat it like a chatty automatic hook that re-indexes on every tiny change, and do not modify qmd's DB directly. Batch or queue indexing work instead.

## Cloud-Assisted, Local-First Fallback

Provider policy for the target system:

- embeddings: cloud-assisted first, local fallback
- summarization/compression: cloud-assisted first, local fallback
- retrieval: local against indexed artifacts whenever possible

This repository is being designed to work even when internet access fails.

## Current Repository Layout

```text
.
├── CLAUDE.md
├── README.md
├── docs/plans/
├── main.py
├── mcp_tools.py
├── models.py
├── session_manager.py
├── errors.py
├── memory-bank/
└── tests/
```

## Current Server Components

- `main.py`: MCP entry point and tool registration
- `mcp_tools.py`: current business logic for exposed tools
- `session_manager.py`: session persistence and memory-bank file operations
- `models.py`: current dataclasses and enums
- `errors.py`: exception hierarchy

## Historical Setup Note

Older docs referenced:

```bash
uv sync
uv run main.py
```

Use those commands only if the dependency manifest is present in your checkout. The current repository snapshot may not include `pyproject.toml`.

## License

MIT License
