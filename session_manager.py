from typing import Optional, List, Dict, Any
from datetime import datetime
import importlib.metadata
from models import (
    UnifiedSession, Memory, Collection, Thought, Branch, 
    ArchitectureDecision, PackageInfo, CrossSystemContext,
    SessionType
)
from database import UnifiedDatabase
from context_chunker import ContextChunker


class UnifiedSessionManager:
    def __init__(self, db_path: str = "memory.db"):
        self.db = UnifiedDatabase(db_path)
        self.current_session: Optional[UnifiedSession] = None
        self.context_chunker = ContextChunker()
    
    def _estimate_tokens(self) -> int:
        if not self.current_session:
            return 0
        
        total_content = []
        total_content.append(self.current_session.problem)
        total_content.append(self.current_session.success_criteria)
        total_content.append(self.current_session.constraints)
        
        for thought in self.current_session.thoughts:
            total_content.append(thought.content)
        
        for memory in self.current_session.memories:
            total_content.append(memory.content)
            total_content.append(memory.code_snippet)
        
        full_text = " ".join(total_content)
        return int(len(full_text) / 3.5)
    
    def _check_context_size(self) -> Dict[str, Any]:
        token_count = self._estimate_tokens()
        if token_count > 25000:
            window = self.context_chunker.chunk_session(self.current_session)
            return {
                "needs_chunking": True,
                "current_tokens": token_count,
                "chunked_tokens": window.total_tokens,
                "chunks_created": len(window.chunks),
                "priority_threshold": window.priority_threshold
            }
        return {
            "needs_chunking": False,
            "current_tokens": token_count,
            "max_tokens": 25000
        }
    
    def start_thinking_session(
        self, 
        problem: str, 
        success_criteria: str, 
        constraints: str = ""
    ) -> str:
        session = UnifiedSession(
            problem=problem,
            success_criteria=success_criteria,
            constraints=constraints,
            session_type=SessionType.GENERAL
        )
        session_id = self.db.save_session(session)
        self.current_session = session
        return session_id
    
    def start_coding_session(
        self,
        problem: str,
        success_criteria: str,
        constraints: str = "",
        codebase_context: str = "",
        package_exploration_required: bool = True
    ) -> str:
        session = UnifiedSession(
            problem=problem,
            success_criteria=success_criteria,
            constraints=constraints,
            session_type=SessionType.CODING,
            codebase_context=codebase_context,
            package_exploration_required=package_exploration_required
        )
        session_id = self.db.save_session(session)
        self.current_session = session
        
        if package_exploration_required:
            self.explore_packages(problem)
        
        return session_id
    
    def create_memory_session(
        self,
        problem: str,
        success_criteria: str,
        constraints: str = "",
        session_type: str = "general"
    ) -> str:
        session = UnifiedSession(
            problem=problem,
            success_criteria=success_criteria,
            constraints=constraints,
            session_type=SessionType(session_type)
        )
        session_id = self.db.save_session(session)
        self.current_session = session
        return session_id
    
    def add_thought(
        self, 
        content: str, 
        branch_id: str = "", 
        confidence: float = 0.8,
        dependencies: str = "",
        explore_packages: bool = True
    ) -> str:
        if not self.current_session:
            raise ValueError("No active session")
        
        thought = Thought(
            session_id=self.current_session.id,
            branch_id=branch_id,
            content=content,
            confidence=confidence,
            dependencies=dependencies.split(",") if dependencies else [],
            explore_packages=explore_packages
        )
        
        if explore_packages and self.current_session.session_type == SessionType.CODING:
            thought.suggested_packages = self._suggest_packages(content)
        
        thought_id = self.db.save_thought(thought)
        self.current_session.thoughts.append(thought)
        return thought_id
    
    def add_coding_thought(
        self,
        content: str,
        branch_id: str = "",
        confidence: float = 0.8,
        dependencies: str = "",
        explore_packages: bool = True
    ) -> str:
        return self.add_thought(content, branch_id, confidence, dependencies, explore_packages)
    
    def revise_thought(self, thought_id: str, new_content: str, confidence: float = 0.8) -> str:
        if not self.current_session:
            raise ValueError("No active session")
        
        for thought in self.current_session.thoughts:
            if thought.id == thought_id:
                thought.content = new_content
                thought.confidence = confidence
                thought.updated_at = datetime.now()
                self.db.save_thought(thought)
                return thought_id
        
        raise ValueError(f"Thought {thought_id} not found")
    
    def create_branch(self, name: str, from_thought: str, purpose: str) -> str:
        if not self.current_session:
            raise ValueError("No active session")
        
        branch = Branch(
            name=name,
            purpose=purpose,
            session_id=self.current_session.id,
            from_thought_id=from_thought
        )
        
        branch_id = self.db.save_branch(branch)
        self.current_session.branches.append(branch)
        return branch_id
    
    def merge_branch(self, branch_id: str, target_thought: str = "") -> str:
        if not self.current_session:
            raise ValueError("No active session")
        
        for branch in self.current_session.branches:
            if branch.id == branch_id:
                if target_thought:
                    for thought in self.current_session.thoughts:
                        if thought.id == target_thought:
                            thought.content += f"\n[Merged from {branch.name}]"
                            self.db.save_thought(thought)
                            break
                return branch_id
        
        raise ValueError(f"Branch {branch_id} not found")
    
    def store_memory(
        self,
        content: str,
        collection_id: str = "",
        confidence: float = 0.8,
        dependencies: str = "",
        code_snippet: str = "",
        language: str = "",
        pattern_type: str = ""
    ) -> str:
        if not self.current_session:
            raise ValueError("No active session")
        
        memory = Memory(
            session_id=self.current_session.id,
            content=content,
            confidence=confidence,
            dependencies=dependencies.split(",") if dependencies else [],
            code_snippet=code_snippet,
            language=language,
            pattern_type=pattern_type
        )
        
        memory_id = self.db.save_memory(memory)
        self.current_session.memories.append(memory)
        return memory_id
    
    def revise_memory(self, memory_id: str, new_content: str, confidence: float = 0.8) -> str:
        if not self.current_session:
            raise ValueError("No active session")
        
        for memory in self.current_session.memories:
            if memory.id == memory_id:
                memory.content = new_content
                memory.confidence = confidence
                memory.updated_at = datetime.now()
                self.db.save_memory(memory)
                return memory_id
        
        raise ValueError(f"Memory {memory_id} not found")
    
    def create_collection(self, name: str, from_memory: str, purpose: str) -> str:
        if not self.current_session:
            raise ValueError("No active session")
        
        collection = Collection(
            name=name,
            purpose=purpose,
            session_id=self.current_session.id,
            memory_ids=[from_memory]
        )
        
        collection_id = self.db.save_collection(collection)
        self.current_session.collections.append(collection)
        return collection_id
    
    def merge_collection(self, collection_id: str, target_memory: str = "") -> str:
        if not self.current_session:
            raise ValueError("No active session")
        
        for collection in self.current_session.collections:
            if collection.id == collection_id:
                if target_memory and target_memory not in collection.memory_ids:
                    collection.memory_ids.append(target_memory)
                    self.db.save_collection(collection)
                return collection_id
        
        raise ValueError(f"Collection {collection_id} not found")
    
    def explore_packages(self, task_description: str, language: str = "python") -> List[str]:
        if not self.current_session:
            raise ValueError("No active session")
        
        installed_packages = []
        try:
            for dist in importlib.metadata.distributions():
                package = PackageInfo(
                    name=dist.metadata['name'],
                    version=dist.version,
                    description=f"Installed package: {dist.metadata['name']}",
                    relevance_score=self._calculate_relevance(dist.metadata['name'], task_description),
                    installation_status="installed",
                    session_id=self.current_session.id
                )
                
                if package.relevance_score > 0.3:
                    package_id = self.db.save_package_info(package)
                    self.current_session.discovered_packages.append(package)
                    installed_packages.append(package.name)
        except Exception:
            pass
        
        return installed_packages
    
    def record_architecture_decision(
        self,
        decision_title: str,
        context: str,
        options_considered: str,
        chosen_option: str,
        rationale: str,
        consequences: str,
        package_dependencies: str = "",
        thinking_session_id: str = ""
    ) -> str:
        if not self.current_session:
            raise ValueError("No active session")
        
        decision = ArchitectureDecision(
            session_id=self.current_session.id,
            decision_title=decision_title,
            context=context,
            options_considered=options_considered,
            chosen_option=chosen_option,
            rationale=rationale,
            consequences=consequences,
            package_dependencies=package_dependencies.split(",") if package_dependencies else []
        )
        
        decision_id = self.db.save_architecture_decision(decision)
        self.current_session.architecture_decisions.append(decision)
        return decision_id
    
    def detect_code_reinvention(
        self,
        proposed_code: str,
        existing_packages_checked: str = "",
        confidence_threshold: float = 0.8
    ) -> Dict[str, Any]:
        reinvention_score = 0.0
        suggestions = []
        
        for package in self.current_session.discovered_packages:
            if any(keyword in proposed_code.lower() for keyword in package.name.lower().split()):
                reinvention_score += 0.3
                suggestions.append(f"Consider using {package.name} instead")
        
        return {
            "reinvention_detected": reinvention_score > confidence_threshold,
            "confidence": reinvention_score,
            "suggestions": suggestions,
            "existing_packages": existing_packages_checked.split(",") if existing_packages_checked else []
        }
    
    def query_architecture_decisions(
        self,
        pattern: str = "",
        technology: str = "",
        package: str = "",
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        if not self.current_session:
            return []
        
        matching_decisions = []
        for decision in self.current_session.architecture_decisions:
            match_score = 0.0
            
            if pattern and pattern.lower() in decision.decision_title.lower():
                match_score += 0.4
            if technology and technology.lower() in decision.context.lower():
                match_score += 0.3
            if package and package in decision.package_dependencies:
                match_score += 0.3
            
            if match_score >= similarity_threshold:
                matching_decisions.append({
                    "decision": decision,
                    "match_score": match_score
                })
        
        return sorted(matching_decisions, key=lambda x: x["match_score"], reverse=True)
    
    def get_cross_system_context(self, session_id: str = "") -> Optional[CrossSystemContext]:
        target_session = session_id or (self.current_session.id if self.current_session else "")
        if not target_session:
            return None
        
        return self.db.get_cross_system_context(target_session)
    
    def set_external_context(self, external_context: str, session_id: str = "") -> str:
        target_session = session_id or (self.current_session.id if self.current_session else "")
        if not target_session:
            raise ValueError("No session specified")
        
        context = CrossSystemContext(
            session_id=target_session,
            external_context=external_context
        )
        
        return self.db.save_cross_system_context(context)
    
    def analyze_thinking(self) -> Dict[str, Any]:
        if not self.current_session:
            return {"error": "No active session"}
        
        return {
            "session_id": self.current_session.id,
            "total_thoughts": len(self.current_session.thoughts),
            "total_memories": len(self.current_session.memories),
            "total_branches": len(self.current_session.branches),
            "architecture_decisions": len(self.current_session.architecture_decisions),
            "discovered_packages": len(self.current_session.discovered_packages),
            "code_patterns": len(self.current_session.code_patterns),
            "session_type": self.current_session.session_type.value,
            "auto_validation": self.current_session.auto_validation
        }
    
    def analyze_memories(self) -> Dict[str, Any]:
        return self.analyze_thinking()
    
    def _suggest_packages(self, content: str) -> List[str]:
        suggestions = []
        keywords = {
            "http": ["requests", "httpx", "urllib3"],
            "web": ["flask", "django", "fastapi"],
            "data": ["pandas", "numpy", "sqlite3"],
            "test": ["pytest", "unittest", "mock"],
            "json": ["json", "jsonschema", "pydantic"],
            "async": ["asyncio", "aiohttp", "tornado"]
        }
        
        content_lower = content.lower()
        for keyword, packages in keywords.items():
            if keyword in content_lower:
                suggestions.extend(packages)
        
        return list(set(suggestions))
    
    def _calculate_relevance(self, package_name: str, task_description: str) -> float:
        task_lower = task_description.lower()
        package_lower = package_name.lower()
        
        if package_lower in task_lower:
            return 0.8
        
        common_words = set(task_lower.split()) & set(package_lower.split())
        if common_words:
            return 0.5
        
        return 0.1