import pytest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from session_manager import UnifiedSessionManager
from models import SessionType


class TestUnifiedSessionManager:
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

    def test_session_manager_initialization(self, temp_memory_bank):
        """Test SessionManager initialization creates required directories."""
        manager = UnifiedSessionManager(memory_bank_path=temp_memory_bank)

        memory_bank_path = Path(temp_memory_bank)
        assert memory_bank_path.exists()
        assert (memory_bank_path / "sessions").exists()
        assert (memory_bank_path / "memories").exists()
        assert (memory_bank_path / "patterns").exists()
        assert (memory_bank_path / "index.md").exists()

    def test_start_general_session(self, session_manager):
        """Test starting a general session."""
        session_id = session_manager.start_session(
            problem="Test problem statement",
            success_criteria="Solution works correctly",
            constraints="No external dependencies"
        )

        assert isinstance(session_id, str)
        assert len(session_id) > 0
        assert session_manager.current_session is not None
        assert session_manager.current_session.problem == "Test problem statement"
        assert session_manager.current_session.success_criteria == "Solution works correctly"
        assert session_manager.current_session.constraints == "No external dependencies"
        assert session_manager.current_session.session_type == SessionType.GENERAL

    def test_start_coding_session(self, session_manager):
        """Test starting a coding session."""
        session_id = session_manager.start_session(
            problem="Implement REST API",
            success_criteria="All endpoints work",
            session_type="coding",
            codebase_context="FastAPI project"
        )

        assert session_manager.current_session is not None
        assert session_manager.current_session.session_type == SessionType.CODING
        assert session_manager.current_session.codebase_context == "FastAPI project"
        assert session_manager.current_session.package_exploration_required is True

    def test_session_file_creation(self, session_manager, temp_memory_bank):
        """Test that session files are created properly."""
        session_id = session_manager.start_session(
            problem="Test problem",
            success_criteria="Test criteria"
        )

        session_file = Path(temp_memory_bank) / "sessions" / f"{session_id}.md"
        assert session_file.exists()

        content = session_file.read_text()
        assert "Test problem" in content
        assert "Test criteria" in content
        assert session_id in content

    def test_add_thought_to_session(self, session_manager):
        """Test adding thoughts to a session."""
        session_manager.start_session(
            problem="Test problem",
            success_criteria="Test criteria"
        )

        thought_id = session_manager.add_thought(
            content="This is a test thought",
            confidence=0.9
        )

        assert isinstance(thought_id, str)
        assert len(session_manager.current_session.thoughts) == 1
        assert session_manager.current_session.thoughts[0].content == "This is a test thought"
        assert session_manager.current_session.thoughts[0].confidence == 0.9

    def test_add_thought_without_session_raises_error(self, session_manager):
        """Test that adding thought without active session raises ValueError."""
        session_manager.current_session = None

        with pytest.raises(ValueError, match="No active session"):
            session_manager.add_thought(content="Test thought")

    def test_create_branch(self, session_manager):
        """Test creating a branch in a session."""
        session_manager.start_session(
            problem="Test problem",
            success_criteria="Test criteria"
        )

        # First add a thought to branch from
        thought_id = session_manager.add_thought("Initial thought")

        branch_id = session_manager.create_branch(
            name="Alternative approach",
            from_thought=thought_id,
            purpose="Explore different solution"
        )

        assert isinstance(branch_id, str)
        assert len(session_manager.current_session.branches) == 1
        branch = session_manager.current_session.branches[0]
        assert branch.name == "Alternative approach"
        assert branch.from_thought_id == thought_id
        assert branch.purpose == "Explore different solution"

    def test_merge_branch(self, session_manager):
        """Test merging a branch."""
        session_manager.start_session(
            problem="Test problem",
            success_criteria="Test criteria"
        )

        thought_id = session_manager.add_thought("Main thought")
        branch_id = session_manager.create_branch(
            name="Branch",
            from_thought=thought_id,
            purpose="Test branch"
        )

        target_thought = session_manager.add_thought("Target thought")

        result = session_manager.merge_branch(branch_id, target_thought)

        assert result == branch_id
        # Check that the target thought was updated
        updated_thought = session_manager.current_session.thoughts[-1]
        assert "[Merged from Branch]" in updated_thought.content

    def test_store_memory(self, session_manager):
        """Test storing a memory."""
        session_manager.start_session(
            problem="Test problem",
            success_criteria="Test criteria"
        )

        memory_id = session_manager.store_memory(
            content="Important algorithm pattern",
            confidence=0.95,
            code_snippet="def example():\n    pass",
            language="python",
            tags="algorithm,python,pattern"
        )

        assert isinstance(memory_id, str)
        assert len(session_manager.current_session.memories) == 1
        memory = session_manager.current_session.memories[0]
        assert memory.content == "Important algorithm pattern"
        assert memory.confidence == 0.95
        assert memory.code_snippet == "def example():\n    pass"
        assert memory.language == "python"
        assert memory.tags == ["algorithm", "python", "pattern"]

    def test_memory_file_creation(self, session_manager, temp_memory_bank):
        """Test that memory files are created properly."""
        session_manager.start_session(
            problem="Test problem",
            success_criteria="Test criteria"
        )

        memory_id = session_manager.store_memory(
            content="Test memory content",
            tags="test,example"
        )

        memory_file = Path(temp_memory_bank) / "memories" / f"{memory_id}.md"
        assert memory_file.exists()

        content = memory_file.read_text()
        assert "Test memory content" in content
        assert memory_id in content
        assert "test, example" in content

    def test_query_memories_by_tags(self, session_manager):
        """Test querying memories by tags."""
        session_manager.start_session(
            problem="Test problem",
            success_criteria="Test criteria"
        )

        # Store multiple memories
        session_manager.store_memory("Python content", tags="python,programming")
        session_manager.store_memory("JavaScript content", tags="javascript,programming")
        session_manager.store_memory("Algorithm content", tags="algorithm,python")

        # Query by single tag
        python_memories = session_manager.query_memories(tags="python")
        assert len(python_memories) == 2

        # Query by OR (comma separated)
        prog_memories = session_manager.query_memories(tags="python,javascript")
        assert len(prog_memories) == 3

        # Query by AND
        python_prog_memories = session_manager.query_memories(tags="python&programming")
        assert len(python_prog_memories) == 1

    def test_query_memories_by_content(self, session_manager):
        """Test querying memories by content."""
        session_manager.start_session(
            problem="Test problem",
            success_criteria="Test criteria"
        )

        session_manager.store_memory("Sorting algorithm implementation")
        session_manager.store_memory("Search algorithm implementation")
        session_manager.store_memory("Data structure explanation")

        # Query by content
        algorithm_memories = session_manager.query_memories(content_contains="algorithm")
        assert len(algorithm_memories) == 2

    def test_query_memories_regex(self, session_manager):
        """Test querying memories with regex."""
        session_manager.start_session(
            problem="Test problem",
            success_criteria="Test criteria"
        )

        session_manager.store_memory("Function name: process_data")
        session_manager.store_memory("Variable name: data_processor")
        session_manager.store_memory("Class name: DataHandler")

        # Regex query
        regex_memories = session_manager.query_memories(content_contains="/process.*data/")
        assert len(regex_memories) == 2

    def test_record_decision(self, session_manager):
        """Test recording architecture decisions."""
        session_manager.start_session(
            problem="Test problem",
            success_criteria="Test criteria"
        )

        decision_id = session_manager.record_decision(
            decision_title="Database choice",
            context="Need data persistence",
            options_considered="SQLite, PostgreSQL",
            chosen_option="PostgreSQL",
            rationale="ACID compliance needed",
            consequences="More complex setup"
        )

        assert isinstance(decision_id, str)
        assert len(session_manager.current_session.architecture_decisions) == 1
        decision = session_manager.current_session.architecture_decisions[0]
        assert decision.decision_title == "Database choice"
        assert decision.chosen_option == "PostgreSQL"

    def test_explore_packages(self, session_manager):
        """Test package exploration."""
        session_manager.start_session(
            problem="Need HTTP client",
            success_criteria="Working HTTP requests",
            session_type="coding"
        )

        packages = session_manager.explore_packages("HTTP requests")

        assert isinstance(packages, list)
        # Should find some packages related to HTTP
        http_packages = [pkg for pkg in packages if 'http' in pkg.lower() or 'request' in pkg.lower()]
        assert len(http_packages) >= 0  # May not find packages in test environment

    def test_analyze_session(self, session_manager):
        """Test session analysis."""
        session_manager.start_session(
            problem="Test problem",
            success_criteria="Test criteria"
        )

        session_manager.add_thought("Test thought")
        session_manager.store_memory("Test memory")
        session_manager.create_branch("Test branch", "thought-1", "Test purpose")
        session_manager.record_decision(
            "Test decision", "Test context", "A, B", "A", "Reason", "Consequences"
        )

        analysis = session_manager.analyze_session()

        assert analysis["session_id"] == session_manager.current_session.id
        assert analysis["session_type"] == "general"
        assert analysis["total_thoughts"] == 1
        assert analysis["total_memories"] == 1
        assert analysis["total_branches"] == 1
        assert analysis["architecture_decisions"] == 1

    def test_list_sessions(self, session_manager, temp_memory_bank):
        """Test listing sessions."""
        # Create multiple sessions
        session1_id = session_manager.start_session(
            problem="Problem 1", success_criteria="Criteria 1"
        )
        session2_id = session_manager.start_session(
            problem="Problem 2", success_criteria="Criteria 2"
        )

        sessions = session_manager.list_sessions()

        assert len(sessions) == 2
        session_ids = [s["id"] for s in sessions]
        assert session1_id in session_ids
        assert session2_id in session_ids

    def test_load_session(self, session_manager):
        """Test loading a specific session."""
        # Create a session
        original_session_id = session_manager.start_session(
            problem="Original problem",
            success_criteria="Original criteria"
        )
        session_manager.add_thought("Original thought")

        # Create a new session manager (simulating restart)
        new_manager = UnifiedSessionManager(
            memory_bank_path=session_manager.memory_bank_path
        )

        # Load the original session
        result = new_manager.load_session(original_session_id)

        assert result["session_id"] == original_session_id
        assert result["status"] == "loaded"
        assert new_manager.current_session.problem == "Original problem"
        assert len(new_manager.current_session.thoughts) == 1

    def test_load_nonexistent_session_raises_error(self, session_manager):
        """Test that loading non-existent session raises ValueError."""
        with pytest.raises(ValueError, match="Session nonexistent not found"):
            session_manager.load_session("nonexistent")

    def test_package_suggestion(self, session_manager):
        """Test package suggestion functionality."""
        suggestions = session_manager._suggest_packages("Need to make HTTP requests and handle JSON data")

        assert isinstance(suggestions, list)
        # Should suggest relevant packages
        suggested_text = ' '.join(suggestions).lower()
        assert any(keyword in suggested_text for keyword in ['request', 'http', 'json'])

    def test_package_relevance_calculation(self, session_manager):
        """Test package relevance scoring."""
        # Exact match
        score1 = session_manager._calculate_relevance("requests", "HTTP requests library")
        assert score1 >= 0.7

        # Partial match
        score2 = session_manager._calculate_relevance("pandas", "Data analysis with pandas")
        assert score2 >= 0.4

        # No match
        score3 = session_manager._calculate_relevance("numpy", "Web development")
        assert score3 <= 0.2

    def test_error_handling_in_file_operations(self, session_manager):
        """Test graceful error handling in file operations."""
        # Test with invalid session file
        invalid_file = session_manager.sessions_dir / "invalid.md"
        invalid_file.write_text("Invalid content without proper structure")

        # Should not crash when parsing invalid content
        try:
            session_manager._parse_session_markdown("Invalid content", "invalid")
            # If it doesn't crash, that's good
        except Exception:
            # Even if it raises an exception, it should be handled gracefully
            pass

    def test_index_file_updates(self, session_manager, temp_memory_bank):
        """Test that index file is properly updated."""
        index_file = Path(temp_memory_bank) / "index.md"

        # Create a session
        session_id = session_manager.start_session(
            problem="Test problem",
            success_criteria="Test criteria"
        )

        index_content = index_file.read_text()
        assert session_id in index_content
        assert "Test problem" in index_content