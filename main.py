import asyncio
import json
from typing import Any, Dict, List
from mcp.server import Server
from mcp.types import Tool
from mcp.server.stdio import stdio_server
from mcp.types import TextContent
from session_manager import UnifiedSessionManager
from mcp_tools import MCPToolsHandler


server = Server("sequential-thinking-mcp-v2")
session_manager = UnifiedSessionManager()
tools_handler = MCPToolsHandler(session_manager)


@server.list_tools()
async def list_tools() -> List[Tool]:
    return [
        Tool(
            name="start_thinking_session",
            description="Start a new thinking session with problem and success criteria",
            inputSchema={
                "type": "object",
                "properties": {
                    "problem": {"type": "string"},
                    "success_criteria": {"type": "string"},
                    "constraints": {"type": "string", "default": ""}
                },
                "required": ["problem", "success_criteria"]
            }
        ),
        Tool(
            name="start_coding_session",
            description="Start a new coding session with enhanced package discovery",
            inputSchema={
                "type": "object",
                "properties": {
                    "problem": {"type": "string"},
                    "success_criteria": {"type": "string"},
                    "constraints": {"type": "string", "default": ""},
                    "codebase_context": {"type": "string", "default": ""},
                    "package_exploration_required": {"type": "boolean", "default": True}
                },
                "required": ["problem", "success_criteria"]
            }
        ),
        Tool(
            name="create_memory_session",
            description="Create a new memory session (backward compatible)",
            inputSchema={
                "type": "object",
                "properties": {
                    "problem": {"type": "string"},
                    "success_criteria": {"type": "string"},
                    "constraints": {"type": "string", "default": ""},
                    "session_type": {"type": "string", "default": "general"}
                },
                "required": ["problem", "success_criteria"]
            }
        ),
        Tool(
            name="add_thought",
            description="Add a new thought to the current session",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "branch_id": {"type": "string", "default": ""},
                    "confidence": {"type": "number", "default": 0.8},
                    "dependencies": {"type": "string", "default": ""}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="add_coding_thought",
            description="Add a coding-specific thought with package exploration",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "branch_id": {"type": "string", "default": ""},
                    "confidence": {"type": "number", "default": 0.8},
                    "dependencies": {"type": "string", "default": ""},
                    "explore_packages": {"type": "boolean", "default": True}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="revise_thought",
            description="Revise an existing thought",
            inputSchema={
                "type": "object",
                "properties": {
                    "thought_id": {"type": "string"},
                    "new_content": {"type": "string"},
                    "confidence": {"type": "number", "default": 0.8}
                },
                "required": ["thought_id", "new_content"]
            }
        ),
        Tool(
            name="create_branch",
            description="Create a new branch for alternative reasoning",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "from_thought": {"type": "string"},
                    "purpose": {"type": "string"}
                },
                "required": ["name", "from_thought", "purpose"]
            }
        ),
        Tool(
            name="merge_branch",
            description="Merge a branch back into main reasoning",
            inputSchema={
                "type": "object",
                "properties": {
                    "branch_id": {"type": "string"},
                    "target_thought": {"type": "string", "default": ""}
                },
                "required": ["branch_id"]
            }
        ),
        Tool(
            name="store_memory",
            description="Store a memory with enhanced coding support",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "collection_id": {"type": "string", "default": ""},
                    "confidence": {"type": "number", "default": 0.8},
                    "dependencies": {"type": "string", "default": ""},
                    "code_snippet": {"type": "string", "default": ""},
                    "language": {"type": "string", "default": ""},
                    "pattern_type": {"type": "string", "default": ""}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="revise_memory",
            description="Revise an existing memory",
            inputSchema={
                "type": "object",
                "properties": {
                    "memory_id": {"type": "string"},
                    "new_content": {"type": "string"},
                    "confidence": {"type": "number", "default": 0.8}
                },
                "required": ["memory_id", "new_content"]
            }
        ),
        Tool(
            name="create_collection",
            description="Create a collection of related memories",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "from_memory": {"type": "string"},
                    "purpose": {"type": "string"}
                },
                "required": ["name", "from_memory", "purpose"]
            }
        ),
        Tool(
            name="merge_collection",
            description="Merge a collection with memories",
            inputSchema={
                "type": "object",
                "properties": {
                    "collection_id": {"type": "string"},
                    "target_memory": {"type": "string", "default": ""}
                },
                "required": ["collection_id"]
            }
        ),
        Tool(
            name="explore_packages",
            description="Explore packages for given task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_description": {"type": "string"},
                    "language": {"type": "string", "default": "python"}
                },
                "required": ["task_description"]
            }
        ),
        Tool(
            name="record_architecture_decision",
            description="Record an architecture decision with context",
            inputSchema={
                "type": "object",
                "properties": {
                    "decision_title": {"type": "string"},
                    "context": {"type": "string"},
                    "options_considered": {"type": "string"},
                    "chosen_option": {"type": "string"},
                    "rationale": {"type": "string"},
                    "consequences": {"type": "string"},
                    "package_dependencies": {"type": "string", "default": ""},
                    "thinking_session_id": {"type": "string", "default": ""}
                },
                "required": ["decision_title", "context", "options_considered", "chosen_option", "rationale", "consequences"]
            }
        ),
        Tool(
            name="detect_code_reinvention",
            description="Detect potential code reinvention",
            inputSchema={
                "type": "object",
                "properties": {
                    "proposed_code": {"type": "string"},
                    "existing_packages_checked": {"type": "string", "default": ""},
                    "confidence_threshold": {"type": "number", "default": 0.8}
                },
                "required": ["proposed_code"]
            }
        ),
        Tool(
            name="query_architecture_decisions",
            description="Query previous architecture decisions",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "default": ""},
                    "technology": {"type": "string", "default": ""},
                    "package": {"type": "string", "default": ""},
                    "similarity_threshold": {"type": "number", "default": 0.7}
                }
            }
        ),
        Tool(
            name="get_cross_system_context",
            description="Get cross-system context for session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "default": ""}
                }
            }
        ),
        Tool(
            name="set_external_context",
            description="Set external context for cross-system integration",
            inputSchema={
                "type": "object",
                "properties": {
                    "external_context": {"type": "string"},
                    "session_id": {"type": "string", "default": ""}
                },
                "required": ["external_context"]
            }
        ),
        Tool(
            name="analyze_thinking",
            description="Analyze current thinking session",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="analyze_memories",
            description="Analyze current memory session",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="export_session_to_file",
            description="Export session to file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "format": {"type": "string", "default": "markdown"}
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="export_memories_to_file",
            description="Export memories to file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "tags": {"type": "string", "default": ""}
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="create_project_structure",
            description="Create project structure for memory bank",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string"}
                },
                "required": ["project_name"]
            }
        ),
        Tool(
            name="load_project_context",
            description="Load project context from existing structure",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "default": "memory-bank"}
                }
            }
        ),
        Tool(
            name="update_project_index",
            description="Update project knowledge index",
            inputSchema={
                "type": "object",
                "properties": {
                    "section": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["section", "content"]
            }
        ),
        Tool(
            name="discover_packages",
            description="Discover available packages",
            inputSchema={
                "type": "object",
                "properties": {
                    "scan_imports": {"type": "boolean", "default": True}
                }
            }
        ),
        Tool(
            name="validate_package_usage",
            description="Validate code against existing packages",
            inputSchema={
                "type": "object",
                "properties": {
                    "code_snippet": {"type": "string"}
                },
                "required": ["code_snippet"]
            }
        ),
        Tool(
            name="explore_existing_apis",
            description="Explore existing APIs for functionality",
            inputSchema={
                "type": "object",
                "properties": {
                    "functionality": {"type": "string"}
                },
                "required": ["functionality"]
            }
        ),
        Tool(
            name="store_codebase_pattern",
            description="Store a codebase pattern for reuse",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern_type": {"type": "string"},
                    "code_snippet": {"type": "string"},
                    "description": {"type": "string", "default": ""},
                    "file_path": {"type": "string", "default": ""},
                    "language": {"type": "string", "default": ""},
                    "tags": {"type": "string", "default": ""}
                },
                "required": ["pattern_type", "code_snippet"]
            }
        ),
        Tool(
            name="load_codebase_context",
            description="Load codebase context into memory",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {"type": "string", "default": ""}
                }
            }
        ),
        Tool(
            name="prevent_reinvention_check",
            description="Check if functionality might already exist",
            inputSchema={
                "type": "object",
                "properties": {
                    "functionality_description": {"type": "string"}
                },
                "required": ["functionality_description"]
            }
        ),
        Tool(
            name="execute_auto_cycle",
            description="Execute configurable auto-cycle workflow with optional step control",
            inputSchema={
                "type": "object",
                "properties": {
                    "enable_automation": {"type": "boolean", "default": True},
                    "skip_steps": {"type": "string", "default": ""},
                    "custom_thoughts": {"type": "boolean", "default": False}
                }
            }
        ),
        Tool(
            name="optimize_context_window",
            description="Optimize context window for large sessions using priority-based chunking",
            inputSchema={
                "type": "object",
                "properties": {
                    "required_types": {"type": "string", "default": ""}
                }
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        if hasattr(tools_handler, name):
            result = getattr(tools_handler, name)(**arguments)
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        else:
            return [TextContent(type="text", text=json.dumps({"error": f"Tool {name} not found"}))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
