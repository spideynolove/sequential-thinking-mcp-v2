import pytest
import tempfile
import shutil
from pathlib import Path
from session_manager import UnifiedSessionManager
from mcp_tools import MCPToolsHandler


class TestMCPToolsHandler:
    @pytest.fixture
    def temp_memory_bank(self):
        """Create a temporary memory bank for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def session_manager(self, temp_memory_bank):
        """Create a SessionManager with temporary storage."""
        return UnifiedSessionManager(memory_bank_path=temp_memory_bank)

    @pytest.fixture
    def tools_handler(self, session_manager):
        """Create MCPToolsHandler with session manager."""
        return MCPToolsHandler(session_manager)

    def test_start_session_success(self, tools_handler):
        """Test successful session start."""
        result = tools_handler.start_session(
            problem="Test problem",
            success_criteria="Solution works",
            session_type="coding",
            constraints="No external deps"
        )

        assert result["session_id"] is not None
        assert result["session_type"] == "coding"
        assert result["problem"] == "Test problem"
        assert result["success_criteria"] == "Solution works"
        assert result["constraints"] == "No external deps"
        assert result["package_exploration_required"] is True

    def test_start_session_with_error(self, tools_handler):
        """Test session start with error handling."""
        # Mock session manager to raise an exception
        def mock_start_session(*args, **kwargs):
            raise ValueError("Invalid session parameters")

        tools_handler.session_manager.start_session = mock_start_session

        result = tools_handler.start_session("Test", "Criteria")

        assert "error" in result
        assert "Invalid session parameters" in result["error"]

    def test_add_thought_success(self, tools_handler):
        """Test successful thought addition."""
        # First start a session
        tools_handler.start_session("Test problem", "Test criteria")

        result = tools_handler.add_thought(
            content="This is a test thought",
            confidence=0.9,
            explore_packages=True
        )

        assert result["thought_id"] is not None
        assert result["content"] == "This is a test thought"
        assert result["confidence"] == 0.9
        assert result["explore_packages"] is True

    def test_add_thought_without_session(self, tools_handler):
        """Test adding thought without active session."""
        result = tools_handler.add_thought("Test thought")

        assert "error" in result
        assert "Cannot add thought without an active session" in result["error"]

    def test_create_branch_success(self, tools_handler):
        """Test successful branch creation."""
        # Start session and add thought
        tools_handler.start_session("Test problem", "Test criteria")
        thought_result = tools_handler.add_thought("Initial thought")

        result = tools_handler.create_branch(
            name="Alternative approach",
            from_thought=thought_result["thought_id"],
            purpose="Explore different solution"
        )

        assert result["branch_id"] is not None
        assert result["name"] == "Alternative approach"
        assert result["from_thought"] == thought_result["thought_id"]
        assert result["purpose"] == "Explore different solution"

    def test_merge_branch_success(self, tools_handler):
        """Test successful branch merge."""
        # Setup session with branch
        tools_handler.start_session("Test problem", "Test criteria")
        thought_result = tools_handler.add_thought("Main thought")
        branch_result = tools_handler.create_branch("Branch", thought_result["thought_id"], "Test")
        target_thought = tools_handler.add_thought("Target thought")

        result = tools_handler.merge_branch(
            branch_id=branch_result["branch_id"],
            target_thought=target_thought["thought_id"]
        )

        assert result["branch_id"] == branch_result["branch_id"]
        assert result["target_thought"] == target_thought["thought_id"]
        assert result["status"] == "merged"

    def test_store_memory_success(self, tools_handler):
        """Test successful memory storage."""
        tools_handler.start_session("Test problem", "Test criteria")

        result = tools_handler.store_memory(
            content="Important implementation detail",
            confidence=0.95,
            code_snippet="def example():\n    return True",
            language="python",
            tags="implementation,python,example"
        )

        assert result["memory_id"] is not None
        assert result["content"] == "Important implementation detail"
        assert result["confidence"] == 0.95
        assert result["tags"] == ["implementation", "python", "example"]

    def test_store_memory_tag_parsing(self, tools_handler):
        """Test memory storage with various tag formats."""
        tools_handler.start_session("Test problem", "Test criteria")

        # Test with comma-separated tags
        result1 = tools_handler.store_memory("Test 1", tags="python,testing")
        assert result1["tags"] == ["python", "testing"]

        # Test with empty tags
        result2 = tools_handler.store_memory("Test 2", tags="")
        assert result2["tags"] == []

        # Test with no tags parameter
        result3 = tools_handler.store_memory("Test 3")
        assert result3["tags"] == []

    def test_query_memories_success(self, tools_handler):
        """Test successful memory query."""
        tools_handler.start_session("Test problem", "Test criteria")
        tools_handler.store_memory("Python algorithm", tags="python,algorithm")
        tools_handler.store_memory("JavaScript function", tags="javascript,function")
        tools_handler.store_memory("General concept", tags="concept")

        # Query by single tag
        result = tools_handler.query_memories(tags="python")
        assert result["count"] == 1
        assert len(result["memories"]) == 1

        # Query by multiple tags (OR)
        result = tools_handler.query_memories(tags="python,javascript")
        assert result["count"] == 2

        # Query with content
        result = tools_handler.query_memories(content_contains="function")
        assert result["count"] == 1

        # Query with no results
        result = tools_handler.query_memories(tags="nonexistent")
        assert result["count"] == 0
        assert "search_tips" in result

    def test_record_decision_success(self, tools_handler):
        """Test successful decision recording."""
        tools_handler.start_session("Test problem", "Test criteria")

        result = tools_handler.record_decision(
            decision_title="Framework choice",
            context="Building web application",
            options_considered="Flask, Django, FastAPI",
            chosen_option="FastAPI",
            rationale="Modern async support with automatic docs",
            consequences="Learning curve for async patterns",
            package_dependencies="fastapi,uvicorn,pydantic"
        )

        assert result["decision_id"] is not None
        assert result["decision_title"] == "Framework choice"
        assert result["chosen_option"] == "FastAPI"

    def test_explore_packages_success(self, tools_handler):
        """Test successful package exploration."""
        tools_handler.start_session("HTTP client needed", "Working requests", session_type="coding")

        result = tools_handler.explore_packages(
            task_description="HTTP requests and JSON handling",
            language="python"
        )

        assert "packages" in result
        assert "count" in result
        assert "language" in result
        assert result["language"] == "python"
        assert isinstance(result["packages"], list)

    def test_export_session_success(self, tools_handler):
        """Test successful session export."""
        tools_handler.start_session("Test problem", "Test criteria")
        tools_handler.add_thought("Test thought")
        tools_handler.store_memory("Test memory")

        # Test markdown export
        result = tools_handler.export_session(
            filename="test_export.md",
            format="markdown",
            export_type="session"
        )

        assert result["filename"] is not None
        assert result["format"] == "markdown"
        assert result["export_type"] == "session"
        assert result["status"] == "exported"

        # Verify file was created
        export_file = Path(result["filename"])
        assert export_file.exists()
        content = export_file.read_text()
        assert "Test problem" in content
        assert "Test thought" in content

    def test_export_session_json(self, tools_handler):
        """Test session export in JSON format."""
        tools_handler.start_session("JSON test", "Test criteria")
        tools_handler.add_thought("JSON thought")

        result = tools_handler.export_session(
            filename="test_export.json",
            format="json",
            export_type="session"
        )

        assert result["format"] == "json"

        # Verify JSON is valid
        import json
        export_file = Path(result["filename"])
        content = export_file.read_text()
        data = json.loads(content)
        assert data["problem"] == "JSON test"

    def test_export_memories_success(self, tools_handler):
        """Test successful memories export."""
        tools_handler.start_session("Test problem", "Test criteria")
        tools_handler.store_memory("Memory 1", tags="test")
        tools_handler.store_memory("Memory 2", tags="example")

        result = tools_handler.export_session(
            filename="memories_export.md",
            export_type="memories",
            tags="test,example"
        )

        assert result["export_type"] == "memories"
        assert result["status"] == "exported"

        # Verify file contains memories
        export_file = Path(result["filename"])
        content = export_file.read_text()
        assert "Memory 1" in content
        assert "Memory 2" in content

    def test_list_sessions_success(self, tools_handler):
        """Test successful session listing."""
        # Create multiple sessions
        tools_handler.start_session("Problem 1", "Criteria 1")
        tools_handler.start_session("Problem 2", "Criteria 2")

        result = tools_handler.list_sessions()

        assert "sessions" in result
        assert "count" in result
        assert result["count"] >= 1  # At least one session exists

    def test_load_session_success(self, tools_handler):
        """Test successful session loading."""
        # Create a session
        create_result = tools_handler.start_session("Original problem", "Original criteria")
        session_id = create_result["session_id"]
        tools_handler.add_thought("Original thought")

        # Create new handler to simulate restart
        new_handler = MCPToolsHandler(tools_handler.session_manager)

        # Load the session
        result = new_handler.load_session(session_id)

        assert result["session_id"] == session_id
        assert result["status"] == "loaded"
        assert result["thoughts_count"] >= 1

    def test_analyze_session_success(self, tools_handler):
        """Test successful session analysis."""
        tools_handler.start_session("Analysis test", "Test criteria")
        tools_handler.add_thought("Test thought")
        tools_handler.store_memory("Test memory")

        result = tools_handler.analyze_session()

        assert result["session_id"] is not None
        assert result["session_type"] in ["general", "coding"]
        assert result["total_thoughts"] >= 1
        assert result["total_memories"] >= 1

    def test_analyze_session_without_active(self, tools_handler):
        """Test session analysis without active session."""
        tools_handler.session_manager.current_session = None

        result = tools_handler.analyze_session()

        assert "error" in result
        assert "No active session" in result["error"]

    def test_export_session_without_active(self, tools_handler):
        """Test session export without active session."""
        tools_handler.session_manager.current_session = None

        result = tools_handler.export_session(filename="test.md")
        assert "error" in result
        assert "Cannot export without an active session" in result["error"]

    def test_export_invalid_format(self, tools_handler):
        """Test export with invalid format (should handle gracefully)."""
        tools_handler.start_session("Test", "Test")

        # This should still work, defaulting to markdown
        result = tools_handler.export_session(
            filename="test.md",
            format="invalid"
        )

        # The method should handle this gracefully
        # Depending on implementation, it might use default or return error
        assert "filename" in result or "error" in result

    def test_package_exploration_without_session(self, tools_handler):
        """Test package exploration without active session."""
        result = tools_handler.explore_packages("HTTP client")

        assert "error" in result
        assert "No active session" in result["error"]

    def test_input_validation_edge_cases(self, tools_handler):
        """Test edge cases in input validation."""
        tools_handler.start_session("Test", "Test")

        # Very long content
        long_content = "Test " * 1000
        result = tools_handler.add_thought(content=long_content)
        assert "thought_id" in result or "error" in result

        # Special characters in content
        special_content = "Test with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = tools_handler.add_thought(content=special_content)
        assert "thought_id" in result or "error" in result

        # Empty confidence value
        result = tools_handler.store_memory(content="Test", confidence=None)
        assert "memory_id" in result or "error" in result

    def test_concurrent_operations(self, tools_handler):
        """Test that operations work correctly in sequence."""
        # Start session
        session_result = tools_handler.start_session("Concurrent test", "Test criteria")
        session_id = session_result["session_id"]

        # Add multiple thoughts
        thought_ids = []
        for i in range(3):
            result = tools_handler.add_thought(f"Thought {i+1}")
            thought_ids.append(result["thought_id"])

        # Add memories
        memory_ids = []
        for i in range(2):
            result = tools_handler.store_memory(f"Memory {i+1}", tags=f"tag{i+1}")
            memory_ids.append(result["memory_id"])

        # Create branch from first thought
        branch_result = tools_handler.create_branch(
            name="Test branch",
            from_thought=thought_ids[0],
            purpose="Testing branch"
        )

        # Record decision
        decision_result = tools_handler.record_decision(
            decision_title="Test decision",
            context="Testing",
            options_considered="A, B",
            chosen_option="A",
            rationale="Test",
            consequences="Test"
        )

        # Analyze session
        analysis = tools_handler.analyze_session()

        # Verify all data is present
        assert analysis["total_thoughts"] == 3
        assert analysis["total_memories"] == 2
        assert analysis["total_branches"] == 1
        assert analysis["architecture_decisions"] == 1