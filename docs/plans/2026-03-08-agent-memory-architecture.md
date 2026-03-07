# Agent Memory Architecture Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Refactor the project from flat markdown session storage into a layered memory architecture with explicit artifact types, promotion policy, bounded reasoning state, and documented operational boundaries.

**Architecture:** Keep markdown as canonical human truth, add a structured metadata layer plus semantic artifact retrieval, and expose stable workflows through MCP. Introduce the new system incrementally so the current server remains functional while memory promotion, checkpointing, and retrieval capabilities are added behind tests.

**Tech Stack:** Python, pytest, markdown files, local metadata store, Zvec adapter, qmd adapter, FastMCP-compatible MCP surface

---

### Task 1: Align Documentation And Agent Guidance

**Files:**
- Modify: `README.md`
- Modify: `CLAUDE.md`
- Reference: `docs/plans/2026-03-08-agent-memory-reasoning-architecture-design.md`

**Step 1: Write the failing doc expectations**

```python
def test_readme_mentions_layered_memory_architecture():
    content = Path("README.md").read_text()
    assert "Markdown as canonical truth" in content
    assert "qmd" in content
    assert "Zvec" in content
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_docs_expectations.py::test_readme_mentions_layered_memory_architecture -v`
Expected: FAIL because the repository does not yet document the new architecture.

**Step 3: Update repository docs**

```markdown
## Architecture Direction

- Markdown as canonical truth
- qmd for canonical document retrieval
- Zvec for promoted memory artifacts
- Structured metadata for lifecycle state
- MCP for stable agent workflows
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_docs_expectations.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add README.md CLAUDE.md tests/test_docs_expectations.py
git commit -m "docs: align repository guidance with memory architecture"
```

### Task 2: Add Artifact And Metadata Models

**Files:**
- Modify: `models.py`
- Modify: `errors.py`
- Test: `tests/test_models.py`

**Step 1: Write the failing tests**

```python
def test_memory_artifact_defaults():
    artifact = MemoryArtifact(
        artifact_type=ArtifactType.HANDOFF,
        title="Task handoff",
        content="Condensed summary"
    )
    assert artifact.promotion_status == PromotionStatus.CANDIDATE
    assert artifact.evidence_refs == []
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_models.py::test_memory_artifact_defaults -v`
Expected: FAIL with `NameError` or missing attribute errors.

**Step 3: Add minimal implementation**

```python
class ArtifactType(Enum):
    MEMORY = "memory"
    DECISION = "decision"
    MODULE_CARD = "module_card"
    HANDOFF = "handoff"

@dataclass
class MemoryArtifact:
    artifact_type: ArtifactType
    title: str
    content: str
    promotion_status: PromotionStatus = PromotionStatus.CANDIDATE
    evidence_refs: List[str] = field(default_factory=list)
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_models.py -v`
Expected: PASS for the new model coverage with no regressions.

**Step 5: Commit**

```bash
git add models.py errors.py tests/test_models.py
git commit -m "feat: add artifact and promotion metadata models"
```

### Task 3: Introduce Structured Metadata Persistence

**Files:**
- Create: `metadata_store.py`
- Modify: `session_manager.py`
- Test: `tests/test_metadata_store.py`
- Test: `tests/test_session_manager.py`

**Step 1: Write the failing tests**

```python
def test_metadata_store_round_trip(tmp_path):
    store = MetadataStore(tmp_path / "memory-bank")
    artifact_id = store.upsert({
        "artifact_id": "a1",
        "scope": "session",
        "confidence": 0.9,
        "promotion_status": "promoted",
    })
    loaded = store.get(artifact_id)
    assert loaded["promotion_status"] == "promoted"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_metadata_store.py::test_metadata_store_round_trip -v`
Expected: FAIL because `MetadataStore` does not exist.

**Step 3: Write minimal implementation**

```python
class MetadataStore:
    def __init__(self, memory_bank_path: Path):
        self.metadata_file = memory_bank_path / "metadata.json"

    def upsert(self, record: dict) -> str:
        ...

    def get(self, artifact_id: str) -> dict:
        ...
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_metadata_store.py tests/test_session_manager.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add metadata_store.py session_manager.py tests/test_metadata_store.py tests/test_session_manager.py
git commit -m "feat: add metadata persistence for memory artifacts"
```

### Task 4: Implement Promotion And Checkpoint Policies

**Files:**
- Modify: `session_manager.py`
- Modify: `mcp_tools.py`
- Test: `tests/test_session_manager.py`
- Test: `tests/test_mcp_tools.py`

**Step 1: Write the failing tests**

```python
def test_promote_memory_requires_confidence_and_evidence(session_manager):
    session_manager.start_session("Problem", "Criteria")
    thought_id = session_manager.add_thought("Maybe the root cause is import order")
    with pytest.raises(ValidationError):
        session_manager.promote_artifact(
            source_id=thought_id,
            artifact_type="decision",
            confidence=0.4,
            evidence_refs=[]
        )
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_session_manager.py::test_promote_memory_requires_confidence_and_evidence -v`
Expected: FAIL because promotion APIs do not exist yet.

**Step 3: Write minimal implementation**

```python
def promote_artifact(self, source_id, artifact_type, confidence, evidence_refs):
    if confidence < 0.7 or not evidence_refs:
        raise ValidationError("Promotion requires evidence and sufficient confidence")
    ...
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_session_manager.py tests/test_mcp_tools.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add session_manager.py mcp_tools.py tests/test_session_manager.py tests/test_mcp_tools.py
git commit -m "feat: add promotion and checkpoint policy enforcement"
```

### Task 5: Add Retrieval Adapters For qmd And Zvec

**Files:**
- Create: `retrieval.py`
- Modify: `session_manager.py`
- Modify: `mcp_tools.py`
- Test: `tests/test_retrieval.py`

**Step 1: Write the failing tests**

```python
def test_retrieve_context_merges_doc_and_memory_results():
    retriever = ContextRetriever(
        docs_backend=FakeDocsBackend(["ADR: use module cards"]),
        memory_backend=FakeMemoryBackend(["Past incident summary"]),
    )
    result = retriever.retrieve("module handoff")
    assert "docs" in result
    assert "memory" in result
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_retrieval.py::test_retrieve_context_merges_doc_and_memory_results -v`
Expected: FAIL because retrieval composition does not exist.

**Step 3: Write minimal implementation**

```python
class ContextRetriever:
    def __init__(self, docs_backend, memory_backend):
        self.docs_backend = docs_backend
        self.memory_backend = memory_backend

    def retrieve(self, query: str) -> dict:
        return {
            "docs": self.docs_backend.search(query),
            "memory": self.memory_backend.search(query),
        }
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_retrieval.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add retrieval.py session_manager.py mcp_tools.py tests/test_retrieval.py
git commit -m "feat: add retrieval adapters for docs and memory"
```

### Task 6: Expand The MCP Surface To Stable Workflows

**Files:**
- Modify: `main.py`
- Modify: `mcp_tools.py`
- Test: `tests/test_mcp_tools.py`
- Test: `tests/test_integration.py`

**Step 1: Write the failing tests**

```python
def test_retrieve_context_tool_returns_docs_and_memory(tools_handler):
    result = tools_handler.retrieve_context("handoff for auth module")
    assert "docs" in result
    assert "memory" in result
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_mcp_tools.py::test_retrieve_context_tool_returns_docs_and_memory -v`
Expected: FAIL because the tool is not registered.

**Step 3: Write minimal implementation**

```python
Tool(
    name="retrieve_context",
    description="Retrieve scoped context from canonical docs and promoted memory",
    inputSchema={"type": "object", "properties": {"query": {"type": "string"}}},
)
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_mcp_tools.py tests/test_integration.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add main.py mcp_tools.py tests/test_mcp_tools.py tests/test_integration.py
git commit -m "feat: expose memory workflows through MCP tools"
```

### Task 7: Add Compaction And Handoff Generation

**Files:**
- Modify: `session_manager.py`
- Modify: `mcp_tools.py`
- Test: `tests/test_session_manager.py`
- Test: `tests/test_integration.py`

**Step 1: Write the failing tests**

```python
def test_generate_handoff_compacts_raw_history(session_manager):
    session_manager.start_session("Large task", "Stay within budget")
    session_manager.add_thought("Raw exploratory note one")
    session_manager.add_thought("Raw exploratory note two")
    handoff = session_manager.generate_handoff()
    assert "next_action" in handoff
    assert "summary" in handoff
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_session_manager.py::test_generate_handoff_compacts_raw_history -v`
Expected: FAIL because handoff generation does not exist.

**Step 3: Write minimal implementation**

```python
def generate_handoff(self) -> dict:
    return {
        "summary": self._summarize_session(),
        "next_action": "Resume from promoted conclusions only",
    }
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_session_manager.py tests/test_integration.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add session_manager.py mcp_tools.py tests/test_session_manager.py tests/test_integration.py
git commit -m "feat: add checkpoint compaction and handoff generation"
```

### Task 8: Wire Configuration For Cloud-Assist And Local Fallback

**Files:**
- Create: `config.py`
- Modify: `session_manager.py`
- Modify: `README.md`
- Test: `tests/test_config.py`

**Step 1: Write the failing tests**

```python
def test_provider_config_prefers_cloud_then_local_fallback(monkeypatch):
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key")
    cfg = ProviderConfig.from_env()
    assert cfg.embedding_provider == "voyage"
    assert cfg.local_fallback_enabled is True
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_config.py::test_provider_config_prefers_cloud_then_local_fallback -v`
Expected: FAIL because provider config does not exist.

**Step 3: Write minimal implementation**

```python
@dataclass
class ProviderConfig:
    embedding_provider: str
    local_fallback_enabled: bool = True

    @classmethod
    def from_env(cls):
        if os.getenv("VOYAGE_API_KEY"):
            return cls(embedding_provider="voyage")
        return cls(embedding_provider="local")
```

**Step 4: Run tests to verify they pass**

Run: `pytest tests/test_config.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add config.py session_manager.py README.md tests/test_config.py
git commit -m "feat: add provider configuration for hybrid memory operation"
```

### Task 9: Run Full Verification

**Files:**
- Test: `tests/test_models.py`
- Test: `tests/test_session_manager.py`
- Test: `tests/test_mcp_tools.py`
- Test: `tests/test_integration.py`
- Test: `tests/test_metadata_store.py`
- Test: `tests/test_retrieval.py`
- Test: `tests/test_config.py`

**Step 1: Run targeted verification**

Run: `pytest tests/test_models.py tests/test_metadata_store.py tests/test_retrieval.py -v`
Expected: PASS

**Step 2: Run workflow verification**

Run: `pytest tests/test_session_manager.py tests/test_mcp_tools.py tests/test_integration.py -v`
Expected: PASS

**Step 3: Run full suite**

Run: `pytest -v`
Expected: PASS with all new and existing tests green.

**Step 4: Inspect working tree**

Run: `git status --short`
Expected: only intentional implementation files are modified.

**Step 5: Commit final integration checkpoint**

```bash
git add .
git commit -m "feat: add layered memory architecture foundation"
```
