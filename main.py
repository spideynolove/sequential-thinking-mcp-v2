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
            name="start_session",
            description="Start a new session (thinking, coding, or memory-focused)",
            inputSchema={
                "type": "object",
                "properties": {
                    "problem": {"type": "string"},
                    "success_criteria": {"type": "string"},
                    "constraints": {"type": "string", "default": ""},
                    "session_type": {"type": "string", "default": "general", "enum": ["general", "coding", "memory"]},
                    "codebase_context": {"type": "string", "default": ""},
                    "package_exploration_required": {"type": "boolean", "default": True}
                },
                "required": ["problem", "success_criteria"]
            }
        ),
        Tool(
            name="add_thought",
            description="Add a new thought to the current session with optional package exploration",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "branch_id": {"type": "string", "default": ""},
                    "confidence": {"type": "number", "default": 0.8},
                    "dependencies": {"type": "string", "default": ""},
                    "explore_packages": {"type": "boolean", "default": False}
                },
                "required": ["content"]
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
            description="Store a memory with code snippets and patterns",
            inputSchema={
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "confidence": {"type": "number", "default": 0.8},
                    "code_snippet": {"type": "string", "default": ""},
                    "language": {"type": "string", "default": ""},
                    "pattern_type": {"type": "string", "default": ""},
                    "tags": {"type": "string", "default": ""}
                },
                "required": ["content"]
            }
        ),
        Tool(
            name="query_memories",
            description="Search memories by tags or content",
            inputSchema={
                "type": "object",
                "properties": {
                    "tags": {"type": "string", "default": ""},
                    "content_contains": {"type": "string", "default": ""}
                }
            }
        ),
        Tool(
            name="record_decision",
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
                    "package_dependencies": {"type": "string", "default": ""}
                },
                "required": ["decision_title", "context", "options_considered", "chosen_option", "rationale", "consequences"]
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
            name="export_session",
            description="Export session or memories to file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "format": {"type": "string", "default": "markdown", "enum": ["markdown", "json"]},
                    "export_type": {"type": "string", "default": "session", "enum": ["session", "memories"]},
                    "tags": {"type": "string", "default": ""}
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="list_sessions",
            description="List all saved sessions",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="load_session",
            description="Resume a specific session",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_id": {"type": "string"}
                },
                "required": ["session_id"]
            }
        ),
        Tool(
            name="analyze_session",
            description="Analyze current session completeness and insights",
            inputSchema={
                "type": "object",
                "properties": {}
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
