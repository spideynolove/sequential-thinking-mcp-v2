from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from models import UnifiedSession, Memory, Thought, ArchitectureDecision, PackageInfo, CodePattern
import json


@dataclass
class ContextChunk:
    id: str
    content: str
    token_count: int
    priority: float
    chunk_type: str
    session_id: str
    dependencies: List[str]


@dataclass
class ContextWindow:
    chunks: List[ContextChunk]
    total_tokens: int
    max_tokens: int
    priority_threshold: float


class ContextChunker:
    def __init__(self, max_tokens: int = 32000, chunk_size: int = 2000):
        self.max_tokens = max_tokens
        self.chunk_size = chunk_size
        self.priority_weights = {
            "session_core": 1.0,
            "high_confidence_thoughts": 0.9,
            "architecture_decisions": 0.85,
            "code_patterns": 0.8,
            "memories": 0.75,
            "package_info": 0.6,
            "low_confidence_thoughts": 0.4
        }
    
    def chunk_session(self, session: UnifiedSession) -> ContextWindow:
        chunks = []
        
        chunks.extend(self._chunk_session_core(session))
        chunks.extend(self._chunk_thoughts(session.thoughts))
        chunks.extend(self._chunk_memories(session.memories))
        chunks.extend(self._chunk_architecture_decisions(session.architecture_decisions))
        chunks.extend(self._chunk_code_patterns(session.code_patterns))
        chunks.extend(self._chunk_packages(session.discovered_packages))
        
        sorted_chunks = sorted(chunks, key=lambda c: c.priority, reverse=True)
        
        window = self._build_context_window(sorted_chunks)
        return window
    
    def _chunk_session_core(self, session: UnifiedSession) -> List[ContextChunk]:
        core_content = {
            "session_id": session.id,
            "problem": session.problem,
            "success_criteria": session.success_criteria,
            "constraints": session.constraints,
            "session_type": session.session_type.value,
            "codebase_context": session.codebase_context,
            "auto_validation": session.auto_validation
        }
        
        content_str = json.dumps(core_content, indent=2)
        token_count = self._estimate_tokens(content_str)
        
        return [ContextChunk(
            id=f"{session.id}_core",
            content=content_str,
            token_count=token_count,
            priority=self.priority_weights["session_core"],
            chunk_type="session_core",
            session_id=session.id,
            dependencies=[]
        )]
    
    def _chunk_thoughts(self, thoughts: List[Thought]) -> List[ContextChunk]:
        chunks = []
        
        high_confidence = [t for t in thoughts if t.confidence >= 0.8]
        low_confidence = [t for t in thoughts if t.confidence < 0.8]
        
        for thought_group, group_type in [(high_confidence, "high_confidence_thoughts"), 
                                         (low_confidence, "low_confidence_thoughts")]:
            
            current_chunk_thoughts = []
            current_token_count = 0
            
            for thought in thought_group:
                thought_content = {
                    "id": thought.id,
                    "content": thought.content,
                    "confidence": thought.confidence,
                    "status": thought.status.value,
                    "dependencies": thought.dependencies,
                    "explore_packages": thought.explore_packages,
                    "suggested_packages": thought.suggested_packages
                }
                
                thought_str = json.dumps(thought_content)
                thought_tokens = self._estimate_tokens(thought_str)
                
                if current_token_count + thought_tokens > self.chunk_size and current_chunk_thoughts:
                    chunk = self._create_thoughts_chunk(
                        current_chunk_thoughts, group_type, current_token_count
                    )
                    chunks.append(chunk)
                    current_chunk_thoughts = []
                    current_token_count = 0
                
                current_chunk_thoughts.append(thought_content)
                current_token_count += thought_tokens
            
            if current_chunk_thoughts:
                chunk = self._create_thoughts_chunk(
                    current_chunk_thoughts, group_type, current_token_count
                )
                chunks.append(chunk)
        
        return chunks
    
    def _chunk_memories(self, memories: List[Memory]) -> List[ContextChunk]:
        chunks = []
        
        high_importance = [m for m in memories if m.importance >= 0.7]
        medium_importance = [m for m in memories if 0.4 <= m.importance < 0.7]
        low_importance = [m for m in memories if m.importance < 0.4]
        
        for memory_group in [high_importance, medium_importance, low_importance]:
            if not memory_group:
                continue
                
            current_chunk_memories = []
            current_token_count = 0
            
            for memory in memory_group:
                memory_content = {
                    "id": memory.id,
                    "content": memory.content,
                    "tags": memory.tags,
                    "confidence": memory.confidence,
                    "importance": memory.importance,
                    "code_snippet": memory.code_snippet,
                    "language": memory.language,
                    "pattern_type": memory.pattern_type
                }
                
                memory_str = json.dumps(memory_content)
                memory_tokens = self._estimate_tokens(memory_str)
                
                if current_token_count + memory_tokens > self.chunk_size and current_chunk_memories:
                    chunk = self._create_memories_chunk(current_chunk_memories, current_token_count)
                    chunks.append(chunk)
                    current_chunk_memories = []
                    current_token_count = 0
                
                current_chunk_memories.append(memory_content)
                current_token_count += memory_tokens
            
            if current_chunk_memories:
                chunk = self._create_memories_chunk(current_chunk_memories, current_token_count)
                chunks.append(chunk)
        
        return chunks
    
    def _chunk_architecture_decisions(self, decisions: List[ArchitectureDecision]) -> List[ContextChunk]:
        chunks = []
        
        current_chunk_decisions = []
        current_token_count = 0
        
        for decision in decisions:
            decision_content = {
                "id": decision.id,
                "decision_title": decision.decision_title,
                "context": decision.context,
                "options_considered": decision.options_considered,
                "chosen_option": decision.chosen_option,
                "rationale": decision.rationale,
                "consequences": decision.consequences,
                "package_dependencies": decision.package_dependencies
            }
            
            decision_str = json.dumps(decision_content)
            decision_tokens = self._estimate_tokens(decision_str)
            
            if current_token_count + decision_tokens > self.chunk_size and current_chunk_decisions:
                chunk = self._create_decisions_chunk(current_chunk_decisions, current_token_count)
                chunks.append(chunk)
                current_chunk_decisions = []
                current_token_count = 0
            
            current_chunk_decisions.append(decision_content)
            current_token_count += decision_tokens
        
        if current_chunk_decisions:
            chunk = self._create_decisions_chunk(current_chunk_decisions, current_token_count)
            chunks.append(chunk)
        
        return chunks
    
    def _chunk_code_patterns(self, patterns: List[CodePattern]) -> List[ContextChunk]:
        chunks = []
        
        current_chunk_patterns = []
        current_token_count = 0
        
        for pattern in patterns:
            pattern_content = {
                "id": pattern.id,
                "pattern_type": pattern.pattern_type,
                "code_snippet": pattern.code_snippet,
                "description": pattern.description,
                "language": pattern.language,
                "file_path": pattern.file_path,
                "tags": pattern.tags
            }
            
            pattern_str = json.dumps(pattern_content)
            pattern_tokens = self._estimate_tokens(pattern_str)
            
            if current_token_count + pattern_tokens > self.chunk_size and current_chunk_patterns:
                chunk = self._create_patterns_chunk(current_chunk_patterns, current_token_count)
                chunks.append(chunk)
                current_chunk_patterns = []
                current_token_count = 0
            
            current_chunk_patterns.append(pattern_content)
            current_token_count += pattern_tokens
        
        if current_chunk_patterns:
            chunk = self._create_patterns_chunk(current_chunk_patterns, current_token_count)
            chunks.append(chunk)
        
        return chunks
    
    def _chunk_packages(self, packages: List[PackageInfo]) -> List[ContextChunk]:
        chunks = []
        
        high_relevance = [p for p in packages if p.relevance_score >= 0.7]
        medium_relevance = [p for p in packages if 0.4 <= p.relevance_score < 0.7]
        low_relevance = [p for p in packages if p.relevance_score < 0.4]
        
        for package_group in [high_relevance, medium_relevance, low_relevance]:
            if not package_group:
                continue
                
            current_chunk_packages = []
            current_token_count = 0
            
            for package in package_group:
                package_content = {
                    "id": package.id,
                    "name": package.name,
                    "version": package.version,
                    "description": package.description,
                    "api_signatures": package.api_signatures,
                    "relevance_score": package.relevance_score,
                    "installation_status": package.installation_status
                }
                
                package_str = json.dumps(package_content)
                package_tokens = self._estimate_tokens(package_str)
                
                if current_token_count + package_tokens > self.chunk_size and current_chunk_packages:
                    chunk = self._create_packages_chunk(current_chunk_packages, current_token_count)
                    chunks.append(chunk)
                    current_chunk_packages = []
                    current_token_count = 0
                
                current_chunk_packages.append(package_content)
                current_token_count += package_tokens
            
            if current_chunk_packages:
                chunk = self._create_packages_chunk(current_chunk_packages, current_token_count)
                chunks.append(chunk)
        
        return chunks
    
    def _create_thoughts_chunk(self, thoughts: List[Dict], chunk_type: str, token_count: int) -> ContextChunk:
        chunk_id = f"thoughts_{chunk_type}_{len(thoughts)}"
        content = json.dumps({"thoughts": thoughts}, indent=2)
        
        dependencies = []
        for thought in thoughts:
            dependencies.extend(thought.get("dependencies", []))
        
        return ContextChunk(
            id=chunk_id,
            content=content,
            token_count=token_count,
            priority=self.priority_weights[chunk_type],
            chunk_type=chunk_type,
            session_id=thoughts[0].get("session_id", "") if thoughts else "",
            dependencies=list(set(dependencies))
        )
    
    def _create_memories_chunk(self, memories: List[Dict], token_count: int) -> ContextChunk:
        chunk_id = f"memories_{len(memories)}"
        content = json.dumps({"memories": memories}, indent=2)
        
        return ContextChunk(
            id=chunk_id,
            content=content,
            token_count=token_count,
            priority=self.priority_weights["memories"],
            chunk_type="memories",
            session_id=memories[0].get("session_id", "") if memories else "",
            dependencies=[]
        )
    
    def _create_decisions_chunk(self, decisions: List[Dict], token_count: int) -> ContextChunk:
        chunk_id = f"architecture_decisions_{len(decisions)}"
        content = json.dumps({"architecture_decisions": decisions}, indent=2)
        
        return ContextChunk(
            id=chunk_id,
            content=content,
            token_count=token_count,
            priority=self.priority_weights["architecture_decisions"],
            chunk_type="architecture_decisions",
            session_id=decisions[0].get("session_id", "") if decisions else "",
            dependencies=[]
        )
    
    def _create_patterns_chunk(self, patterns: List[Dict], token_count: int) -> ContextChunk:
        chunk_id = f"code_patterns_{len(patterns)}"
        content = json.dumps({"code_patterns": patterns}, indent=2)
        
        return ContextChunk(
            id=chunk_id,
            content=content,
            token_count=token_count,
            priority=self.priority_weights["code_patterns"],
            chunk_type="code_patterns",
            session_id=patterns[0].get("session_id", "") if patterns else "",
            dependencies=[]
        )
    
    def _create_packages_chunk(self, packages: List[Dict], token_count: int) -> ContextChunk:
        chunk_id = f"package_info_{len(packages)}"
        content = json.dumps({"packages": packages}, indent=2)
        
        return ContextChunk(
            id=chunk_id,
            content=content,
            token_count=token_count,
            priority=self.priority_weights["package_info"],
            chunk_type="package_info",
            session_id=packages[0].get("session_id", "") if packages else "",
            dependencies=[]
        )
    
    def _build_context_window(self, sorted_chunks: List[ContextChunk]) -> ContextWindow:
        selected_chunks = []
        current_tokens = 0
        
        for chunk in sorted_chunks:
            if current_tokens + chunk.token_count <= self.max_tokens:
                selected_chunks.append(chunk)
                current_tokens += chunk.token_count
            else:
                break
        
        priority_threshold = selected_chunks[-1].priority if selected_chunks else 0.0
        
        return ContextWindow(
            chunks=selected_chunks,
            total_tokens=current_tokens,
            max_tokens=self.max_tokens,
            priority_threshold=priority_threshold
        )
    
    def _estimate_tokens(self, text: str) -> int:
        return int(len(text) / 3.5)
    
    def get_context_summary(self, window: ContextWindow) -> Dict[str, Any]:
        chunk_types = {}
        for chunk in window.chunks:
            chunk_types[chunk.chunk_type] = chunk_types.get(chunk.chunk_type, 0) + 1
        
        return {
            "total_chunks": len(window.chunks),
            "total_tokens": window.total_tokens,
            "max_tokens": window.max_tokens,
            "utilization": window.total_tokens / window.max_tokens,
            "priority_threshold": window.priority_threshold,
            "chunk_distribution": chunk_types,
            "truncated_chunks": len([c for c in window.chunks if c.priority < window.priority_threshold])
        }
    
    def optimize_context_window(self, window: ContextWindow, required_chunk_types: List[str]) -> ContextWindow:
        required_chunks = [c for c in window.chunks if c.chunk_type in required_chunk_types]
        optional_chunks = [c for c in window.chunks if c.chunk_type not in required_chunk_types]
        
        required_tokens = sum(c.token_count for c in required_chunks)
        remaining_tokens = self.max_tokens - required_tokens
        
        optimized_chunks = required_chunks.copy()
        current_tokens = required_tokens
        
        for chunk in sorted(optional_chunks, key=lambda c: c.priority, reverse=True):
            if current_tokens + chunk.token_count <= self.max_tokens:
                optimized_chunks.append(chunk)
                current_tokens += chunk.token_count
        
        return ContextWindow(
            chunks=optimized_chunks,
            total_tokens=current_tokens,
            max_tokens=self.max_tokens,
            priority_threshold=optimized_chunks[-1].priority if optimized_chunks else 0.0
        )