import pytest
from datetime import datetime
from models import UnifiedSession, Memory, Thought, Branch, ArchitectureDecision, PackageInfo, SessionType


class TestUnifiedSession:
    def test_unified_session_creation(self):
        """Test basic UnifiedSession creation and defaults."""
        session = UnifiedSession(
            problem="Test problem",
            success_criteria="Test criteria"
        )

        assert session.problem == "Test problem"
        assert session.success_criteria == "Test criteria"
        assert session.session_type == SessionType.GENERAL
        assert session.constraints == ""
        assert session.codebase_context == ""
        assert session.package_exploration_required is True
        assert isinstance(session.id, str)
        assert len(session.id) > 0
        assert isinstance(session.created_at, datetime)
        assert isinstance(session.updated_at, datetime)
        assert session.thoughts == []
        assert session.memories == []
        assert session.branches == []
        assert session.architecture_decisions == []
        assert session.discovered_packages == []

    def test_unified_session_coding_type(self):
        """Test UnifiedSession creation with coding type."""
        session = UnifiedSession(
            problem="Coding problem",
            success_criteria="Code works",
            session_type=SessionType.CODING
        )

        assert session.session_type == SessionType.CODING
        assert session.package_exploration_required is True

    def test_unified_session_with_context(self):
        """Test UnifiedSession creation with context and constraints."""
        session = UnifiedSession(
            problem="Complex problem",
            success_criteria="Solution meets requirements",
            constraints="No external dependencies",
            codebase_context="Python project with FastAPI",
            package_exploration_required=False
        )

        assert session.constraints == "No external dependencies"
        assert session.codebase_context == "Python project with FastAPI"
        assert session.package_exploration_required is False


class TestMemory:
    def test_memory_creation_defaults(self):
        """Test Memory creation with default values."""
        memory = Memory(content="Test memory content")

        assert memory.content == "Test memory content"
        assert memory.session_id == ""
        assert memory.tags == []
        assert memory.confidence == 0.8
        assert memory.importance == 0.5
        assert memory.dependencies == []
        assert memory.code_snippet == ""
        assert memory.language == ""
        assert isinstance(memory.id, str)
        assert isinstance(memory.created_at, datetime)
        assert isinstance(memory.updated_at, datetime)

    def test_memory_creation_full(self):
        """Test Memory creation with all parameters."""
        memory = Memory(
            session_id="session-123",
            content="Algorithm implementation",
            tags=["algorithm", "python", "optimization"],
            confidence=0.95,
            importance=0.9,
            dependencies=["math", "collections"],
            code_snippet="def quick_sort(arr):",
            language="python"
        )

        assert memory.session_id == "session-123"
        assert memory.content == "Algorithm implementation"
        assert memory.tags == ["algorithm", "python", "optimization"]
        assert memory.confidence == 0.95
        assert memory.importance == 0.9
        assert memory.dependencies == ["math", "collections"]
        assert memory.code_snippet == "def quick_sort(arr):"
        assert memory.language == "python"

    def test_memory_tag_parsing_edge_cases(self):
        """Test Memory with various tag scenarios."""
        # Empty tags
        memory1 = Memory(content="Test", tags="")
        assert memory1.tags == []

        # Single tag
        memory2 = Memory(content="Test", tags="python")
        # Note: tags are expected to be split by commas in the session manager
        assert memory2.tags == ["python"]

        # Multiple tags with comma
        memory3 = Memory(content="Test", tags=["python", "testing", "tdd"])
        assert memory3.tags == ["python", "testing", "tdd"]


class TestThought:
    def test_thought_creation_defaults(self):
        """Test Thought creation with default values."""
        thought = Thought(content="This is a thought")

        assert thought.content == "This is a thought"
        assert thought.session_id == ""
        assert thought.branch_id == ""
        assert thought.confidence == 0.8
        assert thought.dependencies == []
        assert thought.explore_packages is False
        assert thought.suggested_packages == []
        assert isinstance(thought.id, str)
        assert isinstance(thought.created_at, datetime)
        assert isinstance(thought.updated_at, datetime)

    def test_thought_creation_with_packages(self):
        """Test Thought creation with package exploration."""
        thought = Thought(
            session_id="session-456",
            branch_id="branch-789",
            content="Need to implement HTTP client",
            confidence=0.9,
            dependencies=["asyncio", "networking"],
            explore_packages=True,
            suggested_packages=["requests", "httpx", "aiohttp"]
        )

        assert thought.session_id == "session-456"
        assert thought.branch_id == "branch-789"
        assert thought.content == "Need to implement HTTP client"
        assert thought.confidence == 0.9
        assert thought.dependencies == ["asyncio", "networking"]
        assert thought.explore_packages is True
        assert thought.suggested_packages == ["requests", "httpx", "aiohttp"]


class TestBranch:
    def test_branch_creation(self):
        """Test Branch creation."""
        branch = Branch(
            name="Alternative approach",
            purpose="Explore different algorithm",
            session_id="session-123",
            from_thought_id="thought-456"
        )

        assert branch.name == "Alternative approach"
        assert branch.purpose == "Explore different algorithm"
        assert branch.session_id == "session-123"
        assert branch.from_thought_id == "thought-456"
        assert branch.thoughts == []
        assert isinstance(branch.id, str)
        assert isinstance(branch.created_at, datetime)

    def test_branch_with_thoughts(self):
        """Test Branch with pre-existing thoughts."""
        branch = Branch(
            name="Design branch",
            purpose="UI design exploration",
            session_id="session-789",
            from_thought_id="thought-123",
            thoughts=["thought-456", "thought-789"]
        )

        assert len(branch.thoughts) == 2
        assert "thought-456" in branch.thoughts
        assert "thought-789" in branch.thoughts


class TestArchitectureDecision:
    def test_architecture_decision_creation_minimal(self):
        """Test ArchitectureDecision creation with minimal required fields."""
        decision = ArchitectureDecision(
            session_id="session-123",
            decision_title="Database choice",
            context="Need data persistence",
            options_considered="SQLite, PostgreSQL, MongoDB",
            chosen_option="PostgreSQL",
            rationale="ACID compliance needed",
            consequences="More complex setup, better data integrity"
        )

        assert decision.session_id == "session-123"
        assert decision.decision_title == "Database choice"
        assert decision.context == "Need data persistence"
        assert decision.options_considered == "SQLite, PostgreSQL, MongoDB"
        assert decision.chosen_option == "PostgreSQL"
        assert decision.rationale == "ACID compliance needed"
        assert decision.consequences == "More complex setup, better data integrity"
        assert decision.package_dependencies == []
        assert isinstance(decision.id, str)
        assert isinstance(decision.created_at, datetime)

    def test_architecture_decision_with_dependencies(self):
        """Test ArchitectureDecision with package dependencies."""
        decision = ArchitectureDecision(
            session_id="session-456",
            decision_title="HTTP framework",
            context="Building REST API",
            options_considered="Flask, Django, FastAPI",
            chosen_option="FastAPI",
            rationale="Automatic OpenAPI generation, async support",
            consequences="Learning curve for async patterns",
            package_dependencies=["fastapi", "uvicorn", "pydantic"]
        )

        assert decision.package_dependencies == ["fastapi", "uvicorn", "pydantic"]


class TestPackageInfo:
    def test_package_info_creation(self):
        """Test PackageInfo creation."""
        package = PackageInfo(
            name="requests",
            version="2.28.1",
            description="HTTP library for Python",
            api_signatures=["requests.get()", "requests.post()", "requests.Session()"],
            relevance_score=0.85,
            installation_status="installed",
            session_id="session-123"
        )

        assert package.name == "requests"
        assert package.version == "2.28.1"
        assert package.description == "HTTP library for Python"
        assert len(package.api_signatures) == 3
        assert "requests.get()" in package.api_signatures
        assert package.relevance_score == 0.85
        assert package.installation_status == "installed"
        assert package.session_id == "session-123"
        assert isinstance(package.id, str)
        assert isinstance(package.discovered_at, datetime)

    def test_package_info_minimal(self):
        """Test PackageInfo creation with minimal data."""
        package = PackageInfo(
            name="pytest",
            version="7.1.2"
        )

        assert package.name == "pytest"
        assert package.version == "7.1.2"
        assert package.description == ""
        assert package.api_signatures == []
        assert package.relevance_score == 0.0
        assert package.installation_status == ""
        assert package.session_id == ""


class TestSessionType:
    def test_session_type_values(self):
        """Test SessionType enum values."""
        assert SessionType.GENERAL.value == "general"
        assert SessionType.CODING.value == "coding"

    def test_session_type_comparison(self):
        """Test SessionType comparisons."""
        assert SessionType.GENERAL == SessionType.GENERAL
        assert SessionType.GENERAL != SessionType.CODING
        assert SessionType.CODING == SessionType.CODING


class TestDataIntegrity:
    def test_unique_ids_across_models(self):
        """Test that different model instances get unique IDs."""
        session1 = UnifiedSession(problem="Test 1")
        session2 = UnifiedSession(problem="Test 2")
        memory1 = Memory(content="Memory 1")
        memory2 = Memory(content="Memory 2")
        thought1 = Thought(content="Thought 1")
        thought2 = Thought(content="Thought 2")
        branch1 = Branch(name="Branch 1", purpose="Test", session_id="s1", from_thought_id="t1")
        branch2 = Branch(name="Branch 2", purpose="Test", session_id="s2", from_thought_id="t2")
        decision1 = ArchitectureDecision(
            session_id="s1", decision_title="D1", context="c",
            options_considered="o", chosen_option="c", rationale="r", consequences="c"
        )
        decision2 = ArchitectureDecision(
            session_id="s2", decision_title="D2", context="c",
            options_considered="o", chosen_option="c", rationale="r", consequences="c"
        )
        package1 = PackageInfo(name="pkg1", version="1.0")
        package2 = PackageInfo(name="pkg2", version="2.0")

        # Collect all IDs
        all_ids = [
            session1.id, session2.id,
            memory1.id, memory2.id,
            thought1.id, thought2.id,
            branch1.id, branch2.id,
            decision1.id, decision2.id,
            package1.id, package2.id
        ]

        # Check all IDs are unique
        assert len(all_ids) == len(set(all_ids)), "All IDs should be unique"

        # Check all IDs are valid UUIDs (basic format check)
        for id_val in all_ids:
            assert isinstance(id_val, str)
            assert len(id_val) > 20  # UUIDs are typically 36 chars with hyphens