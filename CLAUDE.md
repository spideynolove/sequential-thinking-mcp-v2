# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running and Development

**Start the MCP server:**
```bash
uv run main.py
```

**Install dependencies:**
```bash
uv sync
```

**Testing tools:**
The MCP server provides 12 tools for session management, thinking workflows, and memory storage. Test by connecting Claude Desktop or other MCP clients to the server.

## Architecture Overview

This is a Model Context Protocol (MCP) server that provides structured reasoning and memory persistence through a simple 4-file architecture:

### Core Components

**main.py** - MCP server entry point with 12 tools registration:
- `start_session`, `add_thought`, `create_branch`, `merge_branch`
- `store_memory`, `query_memories`, `record_decision`, `explore_packages`
- `export_session`, `list_sessions`, `load_session`, `analyze_session`

**session_manager.py** - File-based persistence layer:
- Manages markdown storage in `memory-bank/` directory
- Handles session state, memory storage, and file I/O
- Auto-loads last active session on startup
- No database dependency - pure markdown files

**models.py** - Data structures:
- `UnifiedSession` - Main session container with thoughts, memories, branches
- `Thought`, `Memory`, `Branch`, `ArchitectureDecision`, `PackageInfo`
- Uses dataclasses with UUID generation and timestamps

**mcp_tools.py** - Business logic for all 12 tools:
- Implements the actual functionality behind each MCP tool
- Handles validation, package discovery, and session operations
- Manages memory queries and export functionality

### Storage Architecture

**Markdown-based persistence:**
- `memory-bank/sessions/` - Individual session files
- `memory-bank/memories/` - Standalone memory entries
- `memory-bank/patterns/` - Code patterns (forward compatibility)
- `memory-bank/index.md` - Session registry and metadata

All data is human-readable markdown with JSON frontmatter for structured data.

### Session Types

- **General** - Problem analysis and structured thinking
- **Coding** - Development with automatic package discovery
- **Memory** - Knowledge building and documentation focus

## Key Workflows

**Research Phase:** `start_session` → `explore_packages` → `add_thought`
**Decision Phase:** `record_decision` with context and rationale
**Memory Phase:** `store_memory` for reusable insights
**Export Phase:** `export_session` for documentation

## Package Discovery

The server automatically suggests relevant Python packages using `importlib.metadata.distributions()`. Package exploration is integrated into thinking workflows for coding sessions.

## Important Design Decisions

- **No SQLite:** Simplified from v1, uses pure markdown files
- **Tool consolidation:** Reduced from 39 → 12 tools for focus
- **File-based sessions:** Each session is a separate markdown file
- **Auto-session loading:** Restores last active session on restart
- **Branch exploration:** Supports alternative reasoning paths within sessions