import uuid
from typing import List
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field


class SessionType(Enum):
    GENERAL = "general"
    CODING = "coding"


@dataclass
class UnifiedSession:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    problem: str = ""
    success_criteria: str = ""
    constraints: str = ""
    session_type: SessionType = SessionType.GENERAL
    codebase_context: str = ""
    package_exploration_required: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    memories: List["Memory"] = field(default_factory=list)
    thoughts: List["Thought"] = field(default_factory=list)
    branches: List["Branch"] = field(default_factory=list)
    architecture_decisions: List["ArchitectureDecision"] = field(default_factory=list)
    discovered_packages: List["PackageInfo"] = field(default_factory=list)


@dataclass
class Memory:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    content: str = ""
    tags: List[str] = field(default_factory=list)
    confidence: float = 0.8
    importance: float = 0.5
    dependencies: List[str] = field(default_factory=list)

    code_snippet: str = ""
    language: str = ""
    # pattern_type field removed as it's currently unused

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)




@dataclass
class Thought:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    branch_id: str = ""
    content: str = ""
    confidence: float = 0.8
    dependencies: List[str] = field(default_factory=list)
    explore_packages: bool = False
    suggested_packages: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Branch:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    purpose: str = ""
    session_id: str = ""
    from_thought_id: str = ""
    thoughts: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class ArchitectureDecision:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    decision_title: str = ""
    context: str = ""
    options_considered: str = ""
    chosen_option: str = ""
    rationale: str = ""
    consequences: str = ""
    package_dependencies: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class PackageInfo:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    version: str = ""
    description: str = ""
    api_signatures: List[str] = field(default_factory=list)
    relevance_score: float = 0.0
    installation_status: str = ""
    session_id: str = ""
    discovered_at: datetime = field(default_factory=datetime.now)


