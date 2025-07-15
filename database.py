import sqlite3
import json
from typing import List, Optional
from models import (
    UnifiedSession, Memory, Collection, Thought, Branch, 
    ArchitectureDecision, PackageInfo, CodePattern, CrossSystemContext,
    SessionType, ThoughtStatus
)


class UnifiedDatabase:
    def __init__(self, db_path: str = "memory.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    problem TEXT,
                    success_criteria TEXT,
                    constraints TEXT,
                    session_type TEXT,
                    codebase_context TEXT,
                    package_exploration_required BOOLEAN,
                    auto_validation BOOLEAN,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    content TEXT,
                    tags TEXT,
                    confidence REAL,
                    importance REAL,
                    dependencies TEXT,
                    code_snippet TEXT,
                    language TEXT,
                    pattern_type TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS collections (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    purpose TEXT,
                    memory_ids TEXT,
                    session_id TEXT,
                    created_at TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS thoughts (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    branch_id TEXT,
                    content TEXT,
                    confidence REAL,
                    dependencies TEXT,
                    status TEXT,
                    explore_packages BOOLEAN,
                    suggested_packages TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS branches (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    purpose TEXT,
                    session_id TEXT,
                    from_thought_id TEXT,
                    thoughts TEXT,
                    created_at TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS architecture_decisions (
                    id TEXT PRIMARY KEY,
                    session_id TEXT,
                    decision_title TEXT,
                    context TEXT,
                    options_considered TEXT,
                    chosen_option TEXT,
                    rationale TEXT,
                    consequences TEXT,
                    package_dependencies TEXT,
                    created_at TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS packages (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    version TEXT,
                    description TEXT,
                    api_signatures TEXT,
                    relevance_score REAL,
                    installation_status TEXT,
                    session_id TEXT,
                    discovered_at TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS code_patterns (
                    id TEXT PRIMARY KEY,
                    pattern_type TEXT,
                    code_snippet TEXT,
                    description TEXT,
                    language TEXT,
                    file_path TEXT,
                    tags TEXT,
                    session_id TEXT,
                    created_at TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cross_system_context (
                    session_id TEXT PRIMARY KEY,
                    external_context TEXT,
                    shared_packages TEXT,
                    sync_timestamp TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                )
            ''')
    
    def save_session(self, session: UnifiedSession) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO sessions (
                    id, problem, success_criteria, constraints, session_type,
                    codebase_context, package_exploration_required, auto_validation,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                session.id, session.problem, session.success_criteria,
                session.constraints, session.session_type.value,
                session.codebase_context, session.package_exploration_required,
                session.auto_validation, session.created_at, session.updated_at
            ))
        return session.id
    
    def get_session(self, session_id: str) -> Optional[UnifiedSession]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM sessions WHERE id = ?', (session_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            
            from datetime import datetime
            session = UnifiedSession(
                id=row[0], problem=row[1], success_criteria=row[2],
                constraints=row[3], session_type=SessionType(row[4]),
                codebase_context=row[5], package_exploration_required=row[6],
                auto_validation=row[7], 
                created_at=datetime.fromisoformat(row[8]) if isinstance(row[8], str) else row[8],
                updated_at=datetime.fromisoformat(row[9]) if isinstance(row[9], str) else row[9]
            )
            
            session.memories = self.get_memories_by_session(session_id)
            session.collections = self.get_collections_by_session(session_id)
            session.thoughts = self.get_thoughts_by_session(session_id)
            session.branches = self.get_branches_by_session(session_id)
            session.architecture_decisions = self.get_decisions_by_session(session_id)
            session.discovered_packages = self.get_packages_by_session(session_id)
            session.code_patterns = self.get_patterns_by_session(session_id)
            
            return session
    
    def save_memory(self, memory: Memory) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO memories (
                    id, session_id, content, tags, confidence, importance,
                    dependencies, code_snippet, language, pattern_type,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                memory.id, memory.session_id, memory.content,
                json.dumps(memory.tags), memory.confidence, memory.importance,
                json.dumps(memory.dependencies), memory.code_snippet,
                memory.language, memory.pattern_type,
                memory.created_at, memory.updated_at
            ))
        return memory.id
    
    def get_memories_by_session(self, session_id: str) -> List[Memory]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM memories WHERE session_id = ?', (session_id,)
            )
            memories = []
            for row in cursor.fetchall():
                memories.append(Memory(
                    id=row[0], session_id=row[1], content=row[2],
                    tags=json.loads(row[3]), confidence=row[4],
                    importance=row[5], dependencies=json.loads(row[6]),
                    code_snippet=row[7], language=row[8], pattern_type=row[9],
                    created_at=row[10], updated_at=row[11]
                ))
            return memories
    
    def save_thought(self, thought: Thought) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO thoughts (
                    id, session_id, branch_id, content, confidence,
                    dependencies, status, explore_packages, suggested_packages,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                thought.id, thought.session_id, thought.branch_id,
                thought.content, thought.confidence,
                json.dumps(thought.dependencies), thought.status.value,
                thought.explore_packages, json.dumps(thought.suggested_packages),
                thought.created_at, thought.updated_at
            ))
        return thought.id
    
    def get_thoughts_by_session(self, session_id: str) -> List[Thought]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM thoughts WHERE session_id = ?', (session_id,)
            )
            thoughts = []
            for row in cursor.fetchall():
                thoughts.append(Thought(
                    id=row[0], session_id=row[1], branch_id=row[2],
                    content=row[3], confidence=row[4],
                    dependencies=json.loads(row[5]),
                    status=ThoughtStatus(row[6]), explore_packages=row[7],
                    suggested_packages=json.loads(row[8]),
                    created_at=row[9], updated_at=row[10]
                ))
            return thoughts
    
    def save_collection(self, collection: Collection) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO collections (
                    id, name, purpose, memory_ids, session_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                collection.id, collection.name, collection.purpose,
                json.dumps(collection.memory_ids), collection.session_id,
                collection.created_at
            ))
        return collection.id
    
    def get_collections_by_session(self, session_id: str) -> List[Collection]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM collections WHERE session_id = ?', (session_id,)
            )
            collections = []
            for row in cursor.fetchall():
                collections.append(Collection(
                    id=row[0], name=row[1], purpose=row[2],
                    memory_ids=json.loads(row[3]), session_id=row[4],
                    created_at=row[5]
                ))
            return collections
    
    def save_branch(self, branch: Branch) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO branches (
                    id, name, purpose, session_id, from_thought_id, thoughts, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                branch.id, branch.name, branch.purpose, branch.session_id,
                branch.from_thought_id, json.dumps(branch.thoughts), branch.created_at
            ))
        return branch.id
    
    def get_branches_by_session(self, session_id: str) -> List[Branch]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM branches WHERE session_id = ?', (session_id,)
            )
            branches = []
            for row in cursor.fetchall():
                branches.append(Branch(
                    id=row[0], name=row[1], purpose=row[2],
                    session_id=row[3], from_thought_id=row[4],
                    thoughts=json.loads(row[5]), created_at=row[6]
                ))
            return branches
    
    def save_architecture_decision(self, decision: ArchitectureDecision) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO architecture_decisions (
                    id, session_id, decision_title, context, options_considered,
                    chosen_option, rationale, consequences, package_dependencies, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                decision.id, decision.session_id, decision.decision_title,
                decision.context, decision.options_considered, decision.chosen_option,
                decision.rationale, decision.consequences,
                json.dumps(decision.package_dependencies), decision.created_at
            ))
        return decision.id
    
    def get_decisions_by_session(self, session_id: str) -> List[ArchitectureDecision]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM architecture_decisions WHERE session_id = ?', (session_id,)
            )
            decisions = []
            for row in cursor.fetchall():
                decisions.append(ArchitectureDecision(
                    id=row[0], session_id=row[1], decision_title=row[2],
                    context=row[3], options_considered=row[4], chosen_option=row[5],
                    rationale=row[6], consequences=row[7],
                    package_dependencies=json.loads(row[8]), created_at=row[9]
                ))
            return decisions
    
    def save_package_info(self, package: PackageInfo) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO packages (
                    id, name, version, description, api_signatures,
                    relevance_score, installation_status, session_id, discovered_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                package.id, package.name, package.version, package.description,
                json.dumps(package.api_signatures), package.relevance_score,
                package.installation_status, package.session_id, package.discovered_at
            ))
        return package.id
    
    def get_packages_by_session(self, session_id: str) -> List[PackageInfo]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM packages WHERE session_id = ?', (session_id,)
            )
            packages = []
            for row in cursor.fetchall():
                packages.append(PackageInfo(
                    id=row[0], name=row[1], version=row[2], description=row[3],
                    api_signatures=json.loads(row[4]), relevance_score=row[5],
                    installation_status=row[6], session_id=row[7], discovered_at=row[8]
                ))
            return packages
    
    def save_code_pattern(self, pattern: CodePattern) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO code_patterns (
                    id, pattern_type, code_snippet, description, language,
                    file_path, tags, session_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                pattern.id, pattern.pattern_type, pattern.code_snippet,
                pattern.description, pattern.language, pattern.file_path,
                json.dumps(pattern.tags), pattern.session_id, pattern.created_at
            ))
        return pattern.id
    
    def get_patterns_by_session(self, session_id: str) -> List[CodePattern]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM code_patterns WHERE session_id = ?', (session_id,)
            )
            patterns = []
            for row in cursor.fetchall():
                patterns.append(CodePattern(
                    id=row[0], pattern_type=row[1], code_snippet=row[2],
                    description=row[3], language=row[4], file_path=row[5],
                    tags=json.loads(row[6]), session_id=row[7], created_at=row[8]
                ))
            return patterns
    
    def save_cross_system_context(self, context: CrossSystemContext) -> str:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO cross_system_context (
                    session_id, external_context, shared_packages, sync_timestamp
                ) VALUES (?, ?, ?, ?)
            ''', (
                context.session_id, context.external_context,
                json.dumps(context.shared_packages), context.sync_timestamp
            ))
        return context.session_id
    
    def get_cross_system_context(self, session_id: str) -> Optional[CrossSystemContext]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT * FROM cross_system_context WHERE session_id = ?', (session_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            
            return CrossSystemContext(
                session_id=row[0], external_context=row[1],
                shared_packages=json.loads(row[2]), sync_timestamp=row[3]
            )