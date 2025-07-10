# Sequential Thinking MCP v2 - Unified with Memory Bank

A unified Model Context Protocol (MCP) server that combines Sequential Thinking MCP and Memory Bank MCP into a single system with 39 tools providing auto-cycle workflow, persistent memory, session management, and cross-session continuity.

## Features

### Core Unified Capabilities
- **Unified Sessions**: Single session model combining thinking and memory capabilities
- **Auto-cycle Workflow**: Optional 5-step automation for systematic problem solving
- **Persistent Memory**: All thinking sessions automatically stored in SQLite database
- **Cross-system Context**: Built-in integration with other MCP systems
- **Package Discovery**: Automatic exploration of existing libraries before coding

### Sequential Thinking Features
- **Structured Reasoning**: Build logical chains of thought with dependencies
- **Branch Management**: Explore alternative approaches and merge insights
- **Coding Integration**: Enhanced workflow for development tasks
- **Architecture Decisions**: Track and query technical decisions with context

### Memory Bank Features
- **Persistent Storage**: Store and retrieve memories across sessions
- **Collections**: Group related memories with clear purposes
- **Code Patterns**: Store reusable code templates and examples
- **Validation Gates**: Prevent code reinvention with existing library checks

### Auto-cycle Workflow
The system provides automated workflow capabilities through the `execute_auto_cycle()` tool:
1. **Package Discovery**: Scan for relevant existing libraries
2. **Thought Generation**: Create structured reasoning chains
3. **Memory Storage**: Persist insights for future reference
4. **Architecture Decisions**: Record technical choices with context
5. **Validation Analysis**: Score completeness and consistency

## Installation

```bash
git clone https://github.com/spideynolove/sequential-thinking-mcp-v2.git
cd sequential-thinking-mcp-v2
uv sync
```

## Usage

### Basic Unified Session

```python
# Start a unified session (combines thinking + memory)
start_thinking_session(
    problem="Build a recommendation system",
    success_criteria="Scalable system with <100ms response time",
    constraints="Limited to open source tools, $1000 budget"
)

# Add thoughts that automatically suggest packages
add_thought(
    content="Need collaborative filtering for user-user similarity",
    confidence=0.9,
    explore_packages=True
)

# Store memories with code integration
store_memory(
    content="Use scikit-learn for similarity calculations",
    code_snippet="from sklearn.metrics.pairwise import cosine_similarity",
    language="python",
    pattern_type="ml_algorithm"
)
```

### Enhanced Coding Session

```python
# Start coding session with auto package discovery
start_coding_session(
    problem="Build REST API for user management",
    success_criteria="Secure, scalable endpoints with automatic documentation",
    constraints="Must integrate with existing Django app",
    codebase_context="Django 4.2 project with PostgreSQL",
    package_exploration_required=True
)

# Resume previous work
list_sessions()  # See all saved sessions
load_session("session-id-here")  # Resume specific session

# Add coding thoughts with package suggestions
add_coding_thought(
    content="Need async web framework for high performance API",
    explore_packages=True  # Automatically suggests FastAPI, Django, Flask
)

# Check for code reinvention
detect_code_reinvention(
    proposed_code="def custom_http_client(): # custom HTTP implementation",
    existing_packages_checked="requests, httpx"
)
```

### Auto-cycle Workflow

```python
# Use auto-cycle for systematic problem solving
start_coding_session(
    problem="Implement user authentication system",
    success_criteria="Secure, maintainable, following best practices"
)

# Execute automated workflow
execute_auto_cycle(
    enable_automation=True,
    skip_steps="",
    custom_thoughts=False
)

# System automatically:
# 1. Discovers packages (finds: django-auth, flask-login, etc.)
# 2. Generates structured thoughts
# 3. Stores memories for future reference
# 4. Records architecture decisions
# 5. Validates completeness and consistency
```

### Memory Bank Integration

```python
# Backward compatible memory session
create_memory_session(
    problem="Implement user auth",
    success_criteria="Secure + scalable",
    session_type="coding_session"
)

# Query historical memories
query_memories(tags="authentication,security")
query_memories(content_contains="JWT token")

# Store code patterns for reuse
store_codebase_pattern(
    pattern_type="authentication",
    code_snippet="@login_required\ndef protected_view(request):",
    description="Django authentication decorator pattern",
    language="python"
)

# Prevent reinvention with existing APIs
prevent_reinvention_check("HTTP client for REST APIs")
# Returns: Found existing APIs: requests.get(), urllib3.request(), etc.
```

## Tool Reference

### Session Management
- `start_thinking_session()` - Start general thinking session
- `start_coding_session()` - Start coding session with package discovery
- `create_memory_session()` - Backward compatible memory session
- `list_sessions()` - List all saved sessions
- `load_session()` - Resume a specific session
- `get_active_session()` - Get current active session info
- `switch_session()` - Change active session
- `delete_session()` - Delete a session and all related data

### Thinking Tools
- `add_thought()` - Add structured reasoning step
- `add_coding_thought()` - Add coding-specific thought with package suggestions
- `revise_thought()` - Update existing thought
- `create_branch()` - Explore alternative approaches
- `merge_branch()` - Combine insights from branches

### Memory Tools
- `store_memory()` - Store insights with code integration
- `revise_memory()` - Update stored memories
- `create_collection()` - Group related memories
- `merge_collection()` - Combine memory collections
- `query_memories()` - Search memories by tags or content

### Coding Integration
- `explore_packages()` - Discover relevant libraries
- `detect_code_reinvention()` - Check for unnecessary reimplementation
- `record_architecture_decision()` - Document technical choices
- `query_architecture_decisions()` - Find similar past decisions
- `validate_package_usage()` - Check code against existing libraries

### Export & Analysis
- `analyze_thinking()` - Analyze session completeness
- `export_session_to_file()` - Export to markdown/JSON
- `create_project_structure()` - Create project folders
- `load_project_context()` - Resume previous work
- `execute_auto_cycle()` - Run automated 5-step workflow
- `optimize_context_window()` - Manage large session contexts

## Database Schema

The unified system uses a single SQLite database with tables for:
- **sessions** - Unified session information
- **thoughts** - Sequential reasoning chains
- **memories** - Persistent memory storage
- **collections** - Grouped memories
- **branches** - Alternative reasoning paths
- **architecture_decisions** - Technical decisions with context
- **packages** - Discovered package information
- **code_patterns** - Reusable code templates
- **cross_system_context** - Integration with other systems

## Claude Desktop Integration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sequential-thinking-unified": {
      "command": "uv",
      "args": [
        "run",
        "/path/to/sequential-thinking-mcp-v2/main.py"
      ]
    }
  }
}
```

## Backward Compatibility

The unified system maintains full backward compatibility:
- All original `start_thinking_session()` calls work unchanged
- All original `create_memory_session()` calls work unchanged
- Tool signatures preserved for existing integrations
- Database migrations handle existing data

## Advanced Features

### Cross-System Context
```python
# Share context with other MCP systems
set_external_context(
    external_context="Package context from memory-bank-mcp",
    session_id="current-session"
)

# Retrieve shared context
get_cross_system_context()
```

### Package Discovery
```python
# Automatic package exploration
discover_packages(scan_imports=True)

# Explore existing APIs for functionality
explore_existing_apis("HTTP client library")
```

### Validation Gates
```python
# Validate code before implementation
validate_package_usage("""
def make_request(url):
    import urllib.request
    return urllib.request.urlopen(url).read()
""")
# Returns: Warning - Consider using requests library
```

## License

MIT License - see LICENSE file for details.