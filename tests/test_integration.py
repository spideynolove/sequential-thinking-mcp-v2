import pytest
import tempfile
import shutil
import json
from pathlib import Path
from session_manager import UnifiedSessionManager
from mcp_tools import MCPToolsHandler


class TestIntegration:
    """Integration tests for the complete Sequential Thinking MCP workflow."""

    @pytest.fixture
    def temp_memory_bank(self):
        """Create a temporary memory bank for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def full_setup(self, temp_memory_bank):
        """Set up complete environment with session manager and tools handler."""
        session_manager = UnifiedSessionManager(memory_bank_path=temp_memory_bank)
        tools_handler = MCPToolsHandler(session_manager)
        return session_manager, tools_handler

    def test_complete_workflow_coding_session(self, full_setup):
        """Test complete workflow for a coding session."""
        session_manager, tools_handler = full_setup

        # 1. Start coding session
        session_result = tools_handler.start_session(
            problem="Build a REST API for user management",
            success_criteria="All CRUD operations work, proper error handling, documentation",
            session_type="coding",
            codebase_context="FastAPI project with PostgreSQL",
            package_exploration_required=True
        )

        session_id = session_result["session_id"]
        assert session_manager.current_session.session_type.value == "coding"

        # 2. Explore relevant packages
        packages_result = tools_handler.explore_packages(
            task_description="REST API with database and authentication",
            language="python"
        )

        # Should suggest relevant packages
        assert isinstance(packages_result["packages"], list)

        # 3. Add thoughts about implementation
        thought1 = tools_handler.add_thought(
            content="Start with User model using SQLAlchemy for database ORM",
            confidence=0.9,
            explore_packages=True
        )

        thought2 = tools_handler.add_thought(
            content="Use FastAPI's automatic OpenAPI generation for documentation",
            confidence=0.85
        )

        # 4. Create alternative approach branch
        branch = tools_handler.create_branch(
            name="NoSQL approach",
            from_thought=thought1["thought_id"],
            purpose="Explore MongoDB instead of PostgreSQL"
        )

        # 5. Add thought to branch
        tools_handler.add_thought(
            content="Consider MongoDB for flexible schema and easier scaling",
            branch_id=branch["branch_id"],
            confidence=0.7
        )

        # 6. Store implementation memories
        memory1 = tools_handler.store_memory(
            content="FastAPI dependency injection pattern for database sessions",
            code_snippet="""
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
            """,
            language="python",
            tags="fastapi,dependency-injection,database"
        )

        memory2 = tools_handler.store_memory(
            content="Pydantic model for request/response validation",
            code_snippet="""
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    created_at: datetime

    class Config:
        from_attributes = True
            """,
            language="python",
            tags="pydantic,validation,model"
        )

        # 7. Record architecture decisions
        decision1 = tools_handler.record_decision(
            decision_title="Database choice",
            context="Need persistent storage for user data with relationships",
            options_considered="PostgreSQL, MongoDB, SQLite",
            chosen_option="PostgreSQL",
            rationale="ACID compliance needed for user data, complex queries expected",
            consequences="More complex setup, requires migrations, but better data integrity",
            package_dependencies="sqlalchemy,asyncpg,alembic"
        )

        decision2 = tools_handler.record_decision(
            decision_title="Authentication method",
            context="Need secure user authentication",
            options_considered="JWT, OAuth2, Session-based",
            chosen_option="JWT",
            rationale="Stateless, works well with APIs, standard approach",
            consequences="Need token refresh mechanism, careful with secret management",
            package_dependencies="python-jose,cryptography,passlib"
        )

        # 8. Merge the alternative branch back
        tools_handler.merge_branch(branch["branch_id"], thought2["thought_id"])

        # 9. Analyze session completeness
        analysis = tools_handler.analyze_session()

        # Verify session state
        assert analysis["total_thoughts"] >= 2
        assert analysis["total_memories"] == 2
        assert analysis["total_branches"] == 1
        assert analysis["architecture_decisions"] == 2
        assert analysis["discovered_packages"] >= 0

        # 10. Export session for documentation
        export_result = tools_handler.export_session(
            filename="user_api_implementation.md",
            format="markdown",
            export_type="session"
        )

        # Verify export file
        export_file = Path(export_result["filename"])
        assert export_file.exists()
        content = export_file.read_text()
        assert "User management" in content
        assert "PostgreSQL" in content
        assert "JWT" in content

        # 11. Export memories as reference
        memories_export = tools_handler.export_session(
            filename="implementation_patterns.md",
            format="markdown",
            export_type="memories",
            tags="fastapi,pydantic"
        )

        memories_file = Path(memories_export["filename"])
        assert memories_file.exists()

    def test_research_and_knowledge_building_workflow(self, full_setup):
        """Test workflow for research and knowledge building."""
        session_manager, tools_handler = full_setup

        # 1. Start memory-focused session
        tools_handler.start_session(
            problem="Research best practices for microservices architecture",
            success_criteria="Comprehensive understanding of patterns, trade-offs, and implementation strategies",
            session_type="memory",
            constraints="Focus on practical, real-world applications"
        )

        # 2. Add research thoughts
        research_thoughts = [
            "Microservices should be organized around business capabilities (Domain-Driven Design)",
            "Each service should own its own data to avoid tight coupling",
            "API Gateway pattern helps with routing, authentication, and rate limiting",
            "Service discovery is crucial for dynamic environments (Kubernetes)",
            "Circuit breaker pattern prevents cascade failures",
            "Event-driven architecture enables loose coupling between services"
        ]

        thought_ids = []
        for thought in research_thoughts:
            result = tools_handler.add_thought(
                content=thought,
                confidence=0.8 + (thought_ids.index(thought) * 0.02)  # Varying confidence
            )
            thought_ids.append(result["thought_id"])

        # 3. Create branches for different aspects
        patterns_branch = tools_handler.create_branch(
            name="Design Patterns",
            from_thought=thought_ids[0],
            purpose="Explore specific microservices design patterns"
        )

        challenges_branch = tools_handler.create_branch(
            name="Implementation Challenges",
            from_thought=thought_ids[1],
            purpose="Document common pitfalls and solutions"
        )

        # 4. Add detailed memories for each area
        patterns_memories = [
            {
                "content": "API Gateway Pattern: Single entry point for all clients, handles cross-cutting concerns",
                "code": "# API Gateway routing example\n@app.route('/api/users/*')\ndef user_routes():\n    return proxy_to_user_service()",
                "tags": "api-gateway,pattern,routing"
            },
            {
                "content": "Circuit Breaker Pattern: Prevents cascading failures by detecting failures and opening circuit",
                "code": "# Hystrix circuit breaker\n@hystrix_command(fallback_method='get_user_fallback')\ndef get_user(user_id):\n    return user_service.get(user_id)",
                "tags": "circuit-breaker,resilience,fallback"
            },
            {
                "content": "Service Discovery Pattern: Services automatically register and discover each other",
                "code": "# Consul service registration\nconsul.agent.service.register(\n    name='user-service',\n    service_id=f'user-service-{instance_id}',\n    port=8080,\n    health_check='http://localhost:8080/health'\n)",
                "tags": "service-discovery,consul,registration"
            }
        ]

        for memory_data in patterns_memories:
            tools_handler.store_memory(
                content=memory_data["content"],
                code_snippet=memory_data["code"],
                language="python",
                tags=memory_data["tags"]
            )

        # 5. Add thoughts to branches
        tools_handler.add_thought(
            content="Saga pattern for distributed transactions: Each service has local transaction, compensated by undo actions",
            branch_id=patterns_branch["branch_id"],
            confidence=0.9
        )

        tools_handler.add_thought(
            content="Distributed tracing is essential for debugging requests across multiple services",
            branch_id=challenges_branch["branch_id"],
            confidence=0.85
        )

        # 6. Record key architectural decisions
        tools_handler.record_decision(
            decision_title="Service Communication",
            context="Choosing between synchronous and asynchronous communication",
            options_considered="REST API calls, Message Queues, gRPC, GraphQL",
            chosen_option="Message Queues (RabbitMQ/Kafka)",
            rationale="Better resilience, supports event-driven architecture, easier scaling",
            consequences="Added complexity, eventual consistency, learning curve",
            package_dependencies="celery,kafka-python,pika"
        )

        # 7. Query and verify memories can be found
        api_patterns = tools_handler.query_memories(tags="api-gateway")
        assert len(api_patterns["memories"]) >= 1

        resilience_patterns = tools_handler.query_memories(tags="circuit-breaker,resilience")
        assert len(resilience_patterns["memories"]) >= 1

        all_patterns = tools_handler.query_memories(tags="pattern")
        assert len(all_patterns["memories"]) >= 3

        # 8. Export research findings
        research_export = tools_handler.export_session(
            filename="microservices_research.md",
            format="markdown",
            export_type="session"
        )

        patterns_export = tools_handler.export_session(
            filename="microservices_patterns.md",
            format="markdown",
            export_type="memories",
            tags="pattern"
        )

        # Verify exports
        for export_file in [research_export["filename"], patterns_export["filename"]]:
            file_path = Path(export_file)
            assert file_path.exists()
            content = file_path.read_text()
            assert len(content) > 100  # Should have substantial content

    def test_session_persistence_and_recovery(self, full_setup):
        """Test that sessions persist and can be recovered after restart."""
        session_manager, tools_handler = full_setup

        # 1. Create comprehensive session
        tools_handler.start_session(
            problem="Data processing pipeline design",
            success_criteria="Efficient ETL process with proper error handling",
            session_type="coding"
        )

        # Add various data
        thought_id = tools_handler.add_thought("Use Apache Spark for large-scale data processing")
        memory_id = tools_handler.store_memory(
            content="Spark transformation pattern",
            code_snippet="df = spark.read.json('input.json')\ndf_clean = df.filter(col('value').isNotNull())",
            tags="spark,etl,transformation"
        )
        tools_handler.record_decision(
            decision_title="Processing Framework",
            context="Need to process large datasets efficiently",
            options_considered="Apache Spark, Pandas, Dask",
            chosen_option="Apache Spark",
            rationale="Distributed processing, mature ecosystem",
            consequences="Complex setup, requires cluster management"
        )

        original_session_id = session_manager.current_session.id

        # 2. Simulate server restart by creating new managers
        new_session_manager = UnifiedSessionManager(
            memory_bank_path=session_manager.memory_bank_path
        )
        new_tools_handler = MCPToolsHandler(new_session_manager)

        # 3. Load the previous session
        load_result = new_tools_handler.load_session(original_session_id)

        assert load_result["session_id"] == original_session_id
        assert load_result["status"] == "loaded"
        assert new_session_manager.current_session.problem == "Data processing pipeline design"

        # 4. Verify data integrity
        analysis = new_tools_handler.analyze_session()
        assert analysis["total_thoughts"] >= 1
        assert analysis["total_memories"] >= 1
        assert analysis["architecture_decisions"] >= 1

        # 5. Continue working with restored session
        new_thought = new_tools_handler.add_thought(
            "Implement data validation at source to prevent garbage in/garbage out"
        )
        assert new_thought["thought_id"] is not None

        # 6. Query memories in restored session
        memories = new_tools_handler.query_memories(tags="spark")
        assert len(memories["memories"]) >= 1
        assert "Spark" in memories["memories"][0]["content"]

    def test_error_handling_and_recovery(self, full_setup):
        """Test error handling in various failure scenarios."""
        session_manager, tools_handler = full_setup

        # 1. Test operations without session
        assert "error" in tools_handler.add_thought("Test")
        assert "error" in tools_handler.store_memory("Test")
        assert "error" in tools_handler.create_branch("Test", "test", "test")

        # 2. Start session and test invalid operations
        tools_handler.start_session("Test", "Test")

        # Test invalid branch merge
        result = tools_handler.merge_branch("nonexistent_branch")
        assert "error" in result

        # Test loading non-existent session
        result = tools_handler.load_session("nonexistent_session")
        assert "error" in result

        # 3. Test malformed exports
        # Export without active session (clear current session)
        session_manager.current_session = None
        result = tools_handler.export_session("test.md")
        assert "error" in result

    def test_json_export_functionality(self, full_setup):
        """Test JSON export functionality and data integrity."""
        session_manager, tools_handler = full_setup

        # Create session with rich data
        tools_handler.start_session(
            problem="JSON export test",
            success_criteria="All data properly serialized",
            session_type="coding"
        )

        tools_handler.add_thought("Complex thought with special chars: !@#$%^&*()", confidence=0.95)
        tools_handler.store_memory(
            content="Memory with Unicode: 🚀 Python test",
            code_snippet="print('Hello, 世界!')",
            tags="unicode,python,test",
            confidence=0.9
        )
        tools_handler.record_decision(
            decision_title="JSON Decision",
            context="Testing JSON serialization",
            options_considered="Option A, Option B",
            chosen_option="Option A",
            rationale="Test rationale",
            consequences="Test consequences"
        )

        # Export as JSON
        json_export = tools_handler.export_session(
            filename="test_export.json",
            format="json",
            export_type="session"
        )

        # Verify JSON is valid and contains expected data
        json_file = Path(json_export["filename"])
        assert json_file.exists()

        with open(json_file, 'r') as f:
            data = json.load(f)

        assert data["problem"] == "JSON export test"
        assert len(data["thoughts"]) >= 1
        assert len(data["memories"]) >= 1
        assert "🚀" in data["memories"][0]["content"]

    def test_concurrent_session_management(self, full_setup):
        """Test managing multiple sessions and switching between them."""
        session_manager, tools_handler = full_setup

        # Create first session
        session1_result = tools_handler.start_session(
            problem="Session 1: Frontend development",
            success_criteria="Responsive UI works"
        )
        session1_id = session1_result["session_id"]
        tools_handler.add_thought("Use React for component-based architecture")

        # Create second session
        session2_result = tools_handler.start_session(
            problem="Session 2: Backend API",
            success_criteria="RESTful endpoints functional"
        )
        session2_id = session2_result["session_id"]
        tools_handler.add_thought("Implement Express.js with middleware")

        # Verify we're in session 2
        current_analysis = tools_handler.analyze_session()
        assert current_analysis["session_id"] == session2_id
        assert "Backend API" in session_manager.current_session.problem

        # Switch back to session 1
        load_result = tools_handler.load_session(session1_id)
        assert load_result["session_id"] == session1_id

        # Verify we're back in session 1
        current_analysis = tools_handler.analyze_session()
        assert current_analysis["session_id"] == session1_id
        assert "Frontend development" in session_manager.current_session.problem

        # List all sessions and verify both exist
        sessions = tools_handler.list_sessions()
        session_ids = [s["id"] for s in sessions["sessions"]]
        assert session1_id in session_ids
        assert session2_id in session_ids