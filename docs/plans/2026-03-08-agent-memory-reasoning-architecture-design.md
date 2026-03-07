# Agent Memory And Reasoning Architecture Design

**Date:** 2026-03-08
**Status:** Approved for planning
**Scope:** Local-first fallback, cloud-assisted primary operation for long-running LLM coding agents on large codebases

---

## Goal

Design a practical memory and reasoning architecture for LLM coding agents that:

- preserves durable project knowledge across long-running work
- keeps active context small enough to remain reliable
- separates human-authored truth from machine retrieval artifacts
- supports cloud-assisted operation with local fallback
- exposes stable capabilities through MCP rather than coupling agents to storage internals

---

## Core Principles

1. Markdown is canonical human truth.
2. Semantic recall augments canonical docs; it does not replace them.
3. Raw scratch reasoning is ephemeral by default.
4. Only promoted conclusions become durable machine memory.
5. Retrieval is on demand, scoped, and policy-driven.
6. Token thresholds are engineering defaults, not universal facts.
7. Cloud memory is optional overlay, never source of truth.

---

## Recommended Layered Architecture

### L0 Working Memory

Short-lived task context for the current agent session:

- active files
- current subtask summary
- recent tool outputs
- unresolved questions
- bounded scratchpad

This layer is disposable and should be aggressively compacted.

### L1 Episodic Memory

Session artifacts that describe what happened:

- task summaries
- bug investigation outcomes
- handoff bundles
- subtask checkpoints

This layer supports recovery and collaboration, but it is not automatically canonical.

### L2 Semantic Project Memory

Durable machine-retrievable knowledge about the codebase:

- promoted memories
- architecture decisions
- investigation summaries
- module cards
- stable code summaries
- recurring debugging heuristics

This is the main semantic recall layer for agents.

### L3 Canonical Documentation

Human-readable project truth stored as markdown and related documents:

- ADRs
- design docs
- module maps
- runbooks
- onboarding notes
- maintenance summaries

This is the source of truth for humans and the preferred location for stable, reviewable project knowledge.

### L4 Cloud Overlay

Optional sync layer for:

- roaming continuity
- user preferences
- cross-machine convenience
- selected mirrored summaries

This layer improves continuity when online, but core operation must still work locally.

---

## System Boundaries

### Markdown

Official human-maintained truth.

### qmd

Search engine for canonical docs and document collections only.

Owns:

- markdown knowledge bases
- design docs
- ADRs
- runbooks
- notes and transcripts that are intentionally treated as documents

Does not own live session artifact retrieval.

### Zvec

Semantic recall engine for promoted memory and non-doc retrievable artifacts.

Owns:

- promoted memories
- decisions
- investigation summaries
- module cards
- stable code summaries
- handoff bundles

It should not index only "memories"; it should index the full set of non-doc artifacts needed for agent recall.

### Structured Metadata Store

Explicit lifecycle and provenance layer.

Stores:

- scope
- source type
- confidence
- evidence level
- promotion status
- stale flags
- recency
- sync state
- re-embedding status

Zvec supports schemas and typed fields, but lifecycle metadata should still be explicit and simple rather than implicit in vector records alone.

### FastMCP

Integration layer only.

Owns:

- agent-facing tools
- resources
- workflow prompts
- composition of retrieval, promotion, summarization, and handoff services

It is plumbing, not memory.

---

## Recommended Components

### Zvec as Local Semantic Store

Recommended role:

- local persistent semantic index
- filtered retrieval over promoted artifacts
- live updates during active sessions
- local fallback when cloud providers are unavailable

Why use it:

- embedded vector database
- supports dense, sparse, and hybrid retrieval
- supports schema-based collections and typed fields
- supports insert, upsert, update, and filtered query operations

Decision:

- use Zvec to augment markdown-based memory
- do not replace canonical file storage with Zvec

### FastMCP as MCP Tool Layer

Recommended role:

- local MCP server exposing stable workflows to agents
- abstraction boundary between LLM clients and storage/retrieval internals
- capability surface for search, summarization, promotion, handoff, and codebase mapping

Recommended tools:

- `retrieve_context`
- `search_docs`
- `search_memory`
- `promote_memory`
- `summarize_session`
- `generate_handoff`
- `map_changed_modules`
- `refresh_memory_artifact`

Avoid exposing tiny low-level storage operations directly unless needed for maintenance.

### qmd as Canonical Doc Retrieval Layer

Recommended role:

- hybrid retrieval over canonical markdown and document collections
- controlled indexing for human-authored knowledge assets
- document-focused retrieval with reranking

Important operational rule:

qmd indexing must remain a controlled workflow. Its own repo guidance warns against automatically running indexing/update commands in some contexts and warns against direct DB modification. Treat indexing as queued or operator-controlled jobs, not a chatty automatic hook on every small change.

### Cloud Overlay

Recommended role:

- optional sync of selected summaries and profile-style memory
- cloud-assisted convenience when online
- no dependence for core local retrieval or canonical truth

Provider policy:

- embeddings: cloud first using `VOYAGE_API_KEY`, local embedding fallback when needed
- summarization/compression/judging: cloud first using `OPENROUTER_API_KEY`, local model fallback when needed
- retrieval: always local against indexed local artifacts once data is ingested

---

## Memory Promotion Policy

Promotion must be policy-driven, not transcript-driven.

A candidate artifact should be promoted only if most of these are true:

- evidence is present
- confidence is above threshold
- it is stable beyond the current task
- it is likely to be useful again
- it is specific enough to retrieve later
- it is not already represented canonically elsewhere

What to promote:

- decisions
- module summaries
- debugging lessons with evidence
- integration quirks
- handoff bundles
- investigation summaries
- stable codebase maps

What not to promote by default:

- raw chain-of-thought
- verbose exploratory notes
- duplicate summaries
- low-confidence speculation
- tool chatter
- temporary failures without durable lessons

---

## Reasoning Architecture

### Scratch Reasoning

Ephemeral notes for the current step. Never durable by default.

### Checkpoint Summaries

Compact recovery points written:

- at subtask boundaries
- before context compaction
- before handoff
- before provider/backend switches when useful

### Promoted Conclusions

Durable outputs extracted from the reasoning process and stored as semantic artifacts or canonical docs.

### Handoff Packages

Compact re-entry bundles for future agents containing:

- completed work
- changed modules
- current state
- unresolved risks
- next suggested action

Agents should receive handoff bundles and retrieved artifacts, never full transcripts by default.

---

## Token Management Policy Defaults

These values are policy defaults, not universal truths:

- target active context ceiling: `64K`
- compaction trigger example: `45K`

The operating principle matters more than the exact numbers:

- keep active context bounded
- retrieve on demand
- compact at checkpoints
- pass summaries, not transcripts

### Context Budget Shape

Illustrative default allocation:

- system and agent rules: `~2K`
- compiled task skill/tooling summary: `~3K-8K`
- retrieved semantic memory seed: `~4K-8K`
- active task window: `~20K-30K`
- working scratchpad: `~10K`
- headroom: `~8K`

### Budget Watch Workflow

When policy threshold is crossed:

1. summarize completed work
2. preserve active subtask state
3. strip low-value raw history
4. inject compressed checkpoint summary
5. continue with refreshed effective context

### Partitioning Strategy

Large codebases should be split into logical scopes:

- package
- service
- feature area
- infra slice
- test surface

Each scope should have a compact `module card` containing:

- purpose
- inputs/outputs
- invariants
- dependencies
- recent changes
- known risks

### Remember vs Discard

Remember:

- reusable conclusions
- validated decisions
- cross-task lessons
- stable summaries
- handoff bundles

Discard:

- stale scratch reasoning
- duplicate low-value summaries
- irrelevant neighboring code
- old raw history once checkpointed

---

## Example Pipelines

### Memory Pipeline

```text
Store
  raw event or result
  -> classify artifact type
  -> summarize to compact form
  -> evaluate promotion policy
  -> write markdown if canonical
  -> write metadata row
  -> embed non-doc artifact into Zvec
  -> optionally mirror summary to cloud

Retrieve
  task starts
  -> detect scope
  -> query qmd for canonical docs
  -> query Zvec for promoted artifacts
  -> merge and rerank using metadata filters
  -> inject compact context only

Update
  task ends or checkpoint fires
  -> compress session
  -> promote durable conclusions
  -> mark stale items
  -> refresh embeddings for changed artifacts
  -> emit handoff bundle
```

### Reasoning Pipeline

```text
PreTask
  -> retrieve docs from qmd
  -> retrieve artifacts from Zvec
  -> assemble compact working context

Active Task
  -> bounded scratch reasoning
  -> targeted tool use via MCP
  -> checkpoint at subtask boundaries

BudgetWatch
  -> summarize completed work
  -> preserve active state
  -> discard low-value history

PostTask
  -> extract outputs and lessons
  -> gate promotion by evidence and confidence
  -> persist canonical docs and semantic artifacts
  -> generate handoff bundle
```

---

## MCP Surface

Recommended MCP exposure model:

- tools for meaningful workflows
- resources for static or semi-static knowledge assets
- prompts for repeatable procedures only

Example resources:

- architecture map
- current module cards
- latest handoff bundle
- active decision register
- canonical design index

Example prompts:

- investigate bug
- compress context
- prepare handoff
- promote findings

---

## Third-Party Memory System Evaluation

### Summary Judgment

- `claude-mem`: use as a pattern source
- `supermemory`: use only as optional cloud overlay
- neither should define the core architecture

### Comparison Table

| System | Primary Role | Backend Style | Strengths | Limitations | Recommendation |
|---|---|---|---|---|---|
| `claude-mem` | Local persistent memory for Claude workflows | SQLite/FTS style local memory with optional vector-style patterns depending on setup | Good capture patterns, hook-based workflow ideas, progressive disclosure, local orientation | Too tied to Claude-specific workflow shape to be core architecture for a general MCP memory platform | Borrow patterns, do not adopt as core |
| `claude-supermemory` / `supermemory` | Cloud-backed cross-session memory overlay | Hosted/cloud memory and API-driven integration | Strong continuity across sessions and machines, convenient cloud-assisted recall, ready-made integration path | Vendor dependence, canonical truth should not live here, weaker fit as authoritative project memory | Use only as selective sync overlay |

---

## Final Architecture Diagram

```text
                        Cloud Overlay (optional)
                 supermemory / remote sync / roaming profile
                                   ^
                                   |
                                   | selective sync only
                                   |
+-------------------+      +-------+--------+      +------------------+
|   LLM Client      | <--> |   FastMCP      | <--> | Reasoning Engine |
| Claude/Codex/etc. | MCP  | local server   |      | policy + budget  |
+-------------------+      +-------+--------+      +---------+--------+
                                   |                         |
                                   | tools/resources         |
                    +--------------+-------------+           |
                    |                            |           |
                    v                            v           v
             +-------------+              +-------------+  +----------------+
             | qmd         |              | Zvec        |  | Metadata Store |
             | canonical   |              | semantic    |  | lifecycle      |
             | doc search  |              | memory      |  | provenance      |
             +------+------+              +------+------+  +--------+-------+
                    |                            |                   |
                    v                            v                   v
         Markdown canon/docs             promoted artifacts     state, scope,
         ADRs, runbooks, maps,           summaries, module      confidence,
         design notes, handoffs          cards, decisions       stale/sync flags
```

---

## Implementation Implications For This Repository

The current repository already has a basic session manager and markdown persistence, but it lacks:

- a clear distinction between scratch notes and promoted memory
- explicit lifecycle metadata
- semantic recall beyond flat search
- controlled compaction
- proper handoff artifacts
- explicit boundaries between canonical docs and machine memory

The next implementation phase should therefore focus on:

1. defining artifact types and metadata schema
2. adding memory promotion and checkpoint compaction
3. introducing a semantic retrieval layer
4. separating canonical doc search from memory recall
5. exposing the system through a stable MCP interface

---

## Sources

- Zvec docs: https://zvec.org/en/docs/
- Zvec data operations: https://zvec.org/en/docs/data-operations/
- FastMCP docs: https://gofastmcp.com/
- FastMCP transforms overview: https://gofastmcp.com/servers/transforms/transforms
- FastMCP tool search: https://gofastmcp.com/servers/transforms/tool-search
- MCP introduction: https://modelcontextprotocol.io/introduction
- MCP server concepts: https://modelcontextprotocol.io/docs/concepts/servers
- qmd README: https://github.com/tobi/qmd
- qmd CLAUDE.md: https://github.com/tobi/qmd/blob/main/CLAUDE.md
- claude-mem architecture overview: https://docs.claude-mem.ai/architecture/overview
- supermemory Claude Code integration: https://supermemory.ai/docs/integrations/claude-code
- supermemory MCP repo: https://github.com/supermemoryai/supermemory-mcp
