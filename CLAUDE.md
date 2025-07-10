# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a unified Model Context Protocol (MCP) server that combines Sequential Thinking MCP and Memory Bank MCP functionality. It provides structured reasoning, persistent memory, and package discovery capabilities for AI-assisted development workflows.

## Key Architecture

### Core Components
- **main.py**: MCP server entry point with 34 tool definitions
- **session_manager.py**: `UnifiedSessionManager` - main orchestration class
- **models.py**: Data models using dataclasses (`UnifiedSession`, `Memory`, `Thought`, `Branch`, etc.)
- **database.py**: SQLite persistence layer (`UnifiedDatabase`)
- **mcp_tools.py**: `MCPToolsHandler` - business logic for all MCP tools
- **workflow_manager.py**: Enterprise workflow orchestration
- **auto_cycle.py**: `AutoCycleWorkflow` - automated 5-step problem-solving workflow
- **context_chunker.py**: `ContextChunker` - manages large session contexts (>25k tokens)

### Session Types
- **General**: Basic thinking sessions for problem analysis
- **Coding**: Development sessions with automatic package discovery
- **Architecture**: Technical decision making and documentation
- **Debugging**: Multi-branch investigation workflows

## Common Development Commands

### Running the MCP Server
```bash
# Start the server (uses stdio transport)
uv run main.py

# Install dependencies
uv sync

# The server uses SQLite database 'memory.db' for persistence
```

### Testing
```bash
# No specific test commands found - check if tests exist
find . -name "*test*" -type f
```

## Development Workflow

### Session Management Pattern
1. Start session with `start_thinking_session()` or `start_coding_session()`
2. Add structured reasoning with `add_thought()` or `add_coding_thought()`
3. Store insights with `store_memory()` for persistence
4. Document decisions with `record_architecture_decision()`

### Package Discovery Integration
- `explore_packages()` automatically scans installed packages
- `detect_code_reinvention()` prevents unnecessary custom implementations
- `validate_package_usage()` suggests better alternatives
- Package suggestions integrated into coding thoughts

### Context Management
- Sessions auto-chunk when exceeding 25k tokens (context_chunker.py:41)
- `optimize_context_window()` for large sessions
- Cross-system context sharing via `set_external_context()`

## Key Features

### Auto-Cycle Workflow
Five-step automated problem solving:
1. Package discovery
2. Thought generation  
3. Memory storage
4. Architecture decisions
5. Validation analysis

Enable with `auto_validation=True` in session creation.

### Enterprise Integration
- Materials directory structure for team collaboration
- Shared pattern storage in `materials/shared/patterns/`
- Enterprise PRP (Problem-Requirement-Plan) generation
- Cross-team context sharing

### Memory Bank Integration
- Persistent storage across sessions
- Collections for grouping related memories
- Code pattern storage with reusable snippets
- Validation gates to prevent code reinvention

## Database Schema

SQLite tables managed by `UnifiedDatabase`:
- `sessions` - Unified session information
- `thoughts` - Sequential reasoning chains  
- `memories` - Persistent memory storage
- `collections` - Grouped memories
- `branches` - Alternative reasoning paths
- `architecture_decisions` - Technical decisions with context
- `packages` - Discovered package information
- `code_patterns` - Reusable code templates
- `cross_system_context` - Integration with other systems

## Claude Desktop Integration

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "sequential-thinking-unified": {
      "command": "uv",
      "args": ["run", "/path/to/sequential-thinking-mcp-v2/main.py"]
    }
  }
}
```

## Important Implementation Details

### Token Management
- Sessions auto-detect token count via `_estimate_tokens()` (session_manager.py:19)
- Context chunking activates at 25k tokens using priority-based selection
- Chunking preserves high-confidence thoughts and critical memories

### Package Discovery
- Scans `importlib.metadata.distributions()` for installed packages
- Relevance scoring based on task description keywords
- Automatic suggestions for common patterns (HTTP, web, data, testing)

### Cross-System Context
- Enables integration with other MCP systems
- Shared package information and decision history
- External context injection for enterprise workflows

## Development Tips

### Adding New Tools
1. Define tool schema in `main.py` list_tools()
2. Add method to `MCPToolsHandler` class
3. Implement business logic using `UnifiedSessionManager`
4. Update database schema if needed

### Session Branching
- Use `create_branch()` for parallel investigation paths
- Each branch maintains independent thought chains
- `merge_branch()` combines insights back to main flow

### Memory Collections
- Group related memories with `create_collection()`
- Collections persist across sessions
- Use for building reusable knowledge bases

### Architecture Decisions
- Document all technical choices with `record_architecture_decision()`
- Include package dependencies and consequences
- Query previous decisions to maintain consistency