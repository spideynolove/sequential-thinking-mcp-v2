# Sequential Thinking MCP v2

A focused Model Context Protocol (MCP) server providing structured reasoning, persistent memory, and package discovery with markdown-based storage.

## Architecture

**Simple & Clean Design:**
- **12 essential tools** (down from 39)
- **Markdown storage** in memory-bank/ (no SQLite)
- **4 core files:** main.py, session_manager.py, models.py, mcp_tools.py
- **File-based sessions** with automatic directory structure

## Quick Start

```bash
git clone https://github.com/spideynolove/sequential-thinking-mcp-v2.git
cd sequential-thinking-mcp-v2
uv sync
uv run main.py
```

**Claude Desktop Integration:**
```json
{
  "mcpServers": {
    "sequential-thinking": {
      "command": "uv",
      "args": ["run", "/path/to/sequential-thinking-mcp-v2/main.py"]
    }
  }
}
```

## Core Tools (12)

### Session Management
- **`start_session`** - Create thinking/coding/memory sessions
- **`list_sessions`** - List all saved sessions  
- **`load_session`** - Resume specific session
- **`analyze_session`** - Analyze session completeness

### Thinking & Memory
- **`add_thought`** - Add structured reasoning with optional package exploration
- **`create_branch`** - Alternative reasoning paths
- **`merge_branch`** - Combine insights from branches
- **`store_memory`** - Persist insights with code snippets
- **`query_memories`** - Search by tags or content

### Development
- **`record_decision`** - Architecture decisions with context
- **`explore_packages`** - Discover relevant libraries  
- **`export_session`** - Export to markdown/JSON

## Usage Examples

### Basic Session
```python
# Start session
start_session(
    problem="Build user authentication system",
    success_criteria="Secure JWT-based auth with refresh tokens",
    session_type="coding"
)

# Add structured thinking
add_thought(
    content="Research existing auth libraries before custom implementation", 
    explore_packages=True
)

# Store reusable knowledge
store_memory(
    content="Use fastapi-users for production auth systems",
    code_snippet="from fastapi_users import FastAPIUsers",
    language="python",
    tags="authentication,fastapi"
)
```

### Memory & Decision Workflow
```python
# Query existing knowledge
query_memories(tags="authentication,security")

# Document architecture decision
record_decision(
    decision_title="Authentication Library Selection",
    context="Need production-ready JWT auth for FastAPI",
    options_considered="Custom JWT, FastAPI-Users, Authlib",
    chosen_option="FastAPI-Users with custom user model",
    rationale="Battle-tested, handles edge cases, good documentation"
)

# Export session
export_session(filename="auth_research.md", format="markdown")
```

### Package Discovery
```python
# Discover relevant packages
explore_packages("HTTP client library", language="python")

# Branch reasoning for comparison
create_branch(
    name="http_client_comparison",
    from_thought="base_requirement_thought",
    purpose="Compare requests vs httpx vs aiohttp"
)
```

## File Structure

```
/
├── main.py              # MCP server with 12 tools
├── session_manager.py   # File-based session operations  
├── models.py            # Essential data structures
├── mcp_tools.py         # Business logic for 12 tools
├── memory-bank/         # Markdown storage
│   ├── sessions/        # Session files
│   ├── memories/        # Individual memories  
│   ├── patterns/        # Code patterns
│   └── index.md         # Session registry
├── pyproject.toml       # Dependencies (no SQLite)
└── README.md            # This file
```

## Session Types

- **General:** Problem analysis and structured thinking
- **Coding:** Development with automatic package discovery
- **Memory:** Knowledge building and documentation focus

## Memory Bank

All data stored in human-readable markdown files:
- **Sessions:** `memory-bank/sessions/{session-id}.md`
- **Memories:** `memory-bank/memories/{memory-id}.md`  
- **Index:** `memory-bank/index.md` tracks all sessions

## Development Workflow

1. **Research Phase:** `start_session` → `explore_packages` → `add_thought`
2. **Decision Phase:** `record_decision` with context and rationale
3. **Memory Phase:** `store_memory` for reusable insights
4. **Export Phase:** `export_session` for documentation

## Key Features

- **No Database:** Pure markdown files for simplicity
- **Package Discovery:** Automatic library suggestions
- **Structured Reasoning:** Dependencies between thoughts
- **Branch Exploration:** Multiple approaches to problems
- **Decision Documentation:** Architecture decisions with context
- **Memory Persistence:** Searchable knowledge base

## Tool Consolidation

**Simplified from 39 → 12 tools:**
- Removed complex enterprise workflows
- Eliminated SQLite database dependency
- Focused on core thinking and memory features
- Clean separation of concerns

## Best Practices

- **Start with exploration:** Use `explore_packages` before coding
- **Document decisions:** Always `record_decision` for important choices  
- **Build knowledge:** `store_memory` for reusable insights
- **Branch when unsure:** Use `create_branch` for alternatives
- **Query before storing:** Check `query_memories` to avoid duplication

## License

MIT License