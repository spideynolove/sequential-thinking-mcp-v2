import json
from typing import Dict, Any
from session_manager import UnifiedSessionManager
from auto_cycle import AutoCycleWorkflow
from models import CodePattern


class MCPToolsHandler:
    def __init__(self, session_manager: UnifiedSessionManager):
        self.session_manager = session_manager
        self.auto_cycle = AutoCycleWorkflow(session_manager)
    
    def start_thinking_session(self, problem: str, success_criteria: str, constraints: str = "") -> Dict[str, Any]:
        try:
            session_id = self.session_manager.start_thinking_session(problem, success_criteria, constraints)
            return {
                "session_id": session_id,
                "session_type": "thinking",
                "problem": problem,
                "success_criteria": success_criteria,
                "constraints": constraints
            }
        except Exception as e:
            return {"error": str(e)}
    
    def start_coding_session(
        self, 
        problem: str, 
        success_criteria: str, 
        constraints: str = "",
        codebase_context: str = "",
        package_exploration_required: bool = True
    ) -> Dict[str, Any]:
        try:
            session_id = self.session_manager.start_coding_session(
                problem, success_criteria, constraints, codebase_context, package_exploration_required
            )
            return {
                "session_id": session_id,
                "session_type": "coding",
                "problem": problem,
                "success_criteria": success_criteria,
                "constraints": constraints,
                "codebase_context": codebase_context,
                "package_exploration_required": package_exploration_required
            }
        except Exception as e:
            return {"error": str(e)}
    
    def create_memory_session(
        self, 
        problem: str, 
        success_criteria: str, 
        constraints: str = "",
        session_type: str = "general"
    ) -> Dict[str, Any]:
        try:
            session_id = self.session_manager.create_memory_session(
                problem, success_criteria, constraints, session_type
            )
            return {
                "session_id": session_id,
                "session_type": session_type,
                "problem": problem,
                "success_criteria": success_criteria,
                "constraints": constraints
            }
        except Exception as e:
            return {"error": str(e)}
    
    def add_thought(
        self, 
        content: str, 
        branch_id: str = "", 
        confidence: float = 0.8,
        dependencies: str = ""
    ) -> Dict[str, Any]:
        try:
            thought_id = self.session_manager.add_thought(content, branch_id, confidence, dependencies)
            return {
                "thought_id": thought_id,
                "content": content,
                "confidence": confidence,
                "branch_id": branch_id
            }
        except Exception as e:
            return {"error": str(e)}
    
    def add_coding_thought(
        self,
        content: str,
        branch_id: str = "",
        confidence: float = 0.8,
        dependencies: str = "",
        explore_packages: bool = True
    ) -> Dict[str, Any]:
        try:
            thought_id = self.session_manager.add_coding_thought(
                content, branch_id, confidence, dependencies, explore_packages
            )
            return {
                "thought_id": thought_id,
                "content": content,
                "confidence": confidence,
                "branch_id": branch_id,
                "explore_packages": explore_packages
            }
        except Exception as e:
            return {"error": str(e)}
    
    def revise_thought(self, thought_id: str, new_content: str, confidence: float = 0.8) -> Dict[str, Any]:
        try:
            self.session_manager.revise_thought(thought_id, new_content, confidence)
            return {
                "thought_id": thought_id,
                "new_content": new_content,
                "confidence": confidence
            }
        except Exception as e:
            return {"error": str(e)}
    
    def create_branch(self, name: str, from_thought: str, purpose: str) -> Dict[str, Any]:
        try:
            branch_id = self.session_manager.create_branch(name, from_thought, purpose)
            return {
                "branch_id": branch_id,
                "name": name,
                "from_thought": from_thought,
                "purpose": purpose
            }
        except Exception as e:
            return {"error": str(e)}
    
    def merge_branch(self, branch_id: str, target_thought: str = "") -> Dict[str, Any]:
        try:
            self.session_manager.merge_branch(branch_id, target_thought)
            return {
                "branch_id": branch_id,
                "target_thought": target_thought,
                "status": "merged"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def store_memory(
        self,
        content: str,
        collection_id: str = "",
        confidence: float = 0.8,
        dependencies: str = "",
        code_snippet: str = "",
        language: str = "",
        pattern_type: str = ""
    ) -> Dict[str, Any]:
        try:
            memory_id = self.session_manager.store_memory(
                content, collection_id, confidence, dependencies, 
                code_snippet, language, pattern_type
            )
            return {
                "memory_id": memory_id,
                "content": content,
                "confidence": confidence,
                "code_snippet": code_snippet,
                "language": language,
                "pattern_type": pattern_type
            }
        except Exception as e:
            return {"error": str(e)}
    
    def revise_memory(self, memory_id: str, new_content: str, confidence: float = 0.8) -> Dict[str, Any]:
        try:
            self.session_manager.revise_memory(memory_id, new_content, confidence)
            return {
                "memory_id": memory_id,
                "new_content": new_content,
                "confidence": confidence
            }
        except Exception as e:
            return {"error": str(e)}
    
    def create_collection(self, name: str, from_memory: str, purpose: str) -> Dict[str, Any]:
        try:
            collection_id = self.session_manager.create_collection(name, from_memory, purpose)
            return {
                "collection_id": collection_id,
                "name": name,
                "from_memory": from_memory,
                "purpose": purpose
            }
        except Exception as e:
            return {"error": str(e)}
    
    def merge_collection(self, collection_id: str, target_memory: str = "") -> Dict[str, Any]:
        try:
            self.session_manager.merge_collection(collection_id, target_memory)
            return {
                "collection_id": collection_id,
                "target_memory": target_memory,
                "status": "merged"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def explore_packages(self, task_description: str, language: str = "python") -> Dict[str, Any]:
        try:
            packages = self.session_manager.explore_packages(task_description, language)
            return {
                "task_description": task_description,
                "language": language,
                "packages_found": len(packages),
                "packages": packages
            }
        except Exception as e:
            return {"error": str(e)}
    
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
    ) -> Dict[str, Any]:
        try:
            decision_id = self.session_manager.record_architecture_decision(
                decision_title, context, options_considered, chosen_option,
                rationale, consequences, package_dependencies, thinking_session_id
            )
            return {
                "decision_id": decision_id,
                "decision_title": decision_title,
                "chosen_option": chosen_option,
                "package_dependencies": package_dependencies.split(",") if package_dependencies else []
            }
        except Exception as e:
            return {"error": str(e)}
    
    def detect_code_reinvention(
        self,
        proposed_code: str,
        existing_packages_checked: str = "",
        confidence_threshold: float = 0.8
    ) -> Dict[str, Any]:
        try:
            result = self.session_manager.detect_code_reinvention(
                proposed_code, existing_packages_checked, confidence_threshold
            )
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def query_architecture_decisions(
        self,
        pattern: str = "",
        technology: str = "",
        package: str = "",
        similarity_threshold: float = 0.7
    ) -> Dict[str, Any]:
        try:
            decisions = self.session_manager.query_architecture_decisions(
                pattern, technology, package, similarity_threshold
            )
            return {
                "pattern": pattern,
                "technology": technology,
                "package": package,
                "decisions_found": len(decisions),
                "decisions": decisions
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_cross_system_context(self, session_id: str = "") -> Dict[str, Any]:
        try:
            context = self.session_manager.get_cross_system_context(session_id)
            if context:
                return {
                    "session_id": context.session_id,
                    "external_context": context.external_context,
                    "shared_packages": context.shared_packages,
                    "sync_timestamp": context.sync_timestamp.isoformat()
                }
            return {"context": None}
        except Exception as e:
            return {"error": str(e)}
    
    def set_external_context(self, external_context: str, session_id: str = "") -> Dict[str, Any]:
        try:
            result = self.session_manager.set_external_context(external_context, session_id)
            return {
                "session_id": result,
                "external_context": external_context,
                "status": "set"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_thinking(self) -> Dict[str, Any]:
        try:
            analysis = self.session_manager.analyze_thinking()
            return analysis
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_memories(self) -> Dict[str, Any]:
        try:
            analysis = self.session_manager.analyze_memories()
            return analysis
        except Exception as e:
            return {"error": str(e)}
    
    def export_session_to_file(self, filename: str, format: str = "markdown") -> Dict[str, Any]:
        try:
            if not self.session_manager.current_session:
                return {"error": "No active session"}
            
            session = self.session_manager.current_session
            
            if format == "markdown":
                content = self._generate_markdown_export(session)
            elif format == "json":
                content = self._generate_json_export(session)
            else:
                return {"error": f"Unsupported format: {format}"}
            
            with open(filename, 'w') as f:
                f.write(content)
            
            return {
                "filename": filename,
                "format": format,
                "session_id": session.id,
                "status": "exported"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def export_memories_to_file(self, filename: str, tags: str = "") -> Dict[str, Any]:
        try:
            if not self.session_manager.current_session:
                return {"error": "No active session"}
            
            session = self.session_manager.current_session
            memories = session.memories
            
            if tags:
                tag_list = [tag.strip() for tag in tags.split(",")]
                memories = [m for m in memories if any(tag in m.tags for tag in tag_list)]
            
            content = self._generate_memories_export(memories)
            
            with open(filename, 'w') as f:
                f.write(content)
            
            return {
                "filename": filename,
                "memories_exported": len(memories),
                "tags": tags,
                "status": "exported"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def create_project_structure(self, project_name: str) -> Dict[str, Any]:
        try:
            import os
            
            base_path = f"{project_name}-memory-bank"
            os.makedirs(base_path, exist_ok=True)
            os.makedirs(f"{base_path}/sessions", exist_ok=True)
            os.makedirs(f"{base_path}/exports", exist_ok=True)
            os.makedirs(f"{base_path}/patterns", exist_ok=True)
            
            with open(f"{base_path}/project_knowledge_index.md", 'w') as f:
                f.write(f"# {project_name} Knowledge Index\n\n")
                f.write("## Sessions\n\n")
                f.write("## Architecture Decisions\n\n")
                f.write("## Code Patterns\n\n")
                f.write("## Package Dependencies\n\n")
            
            return {
                "project_name": project_name,
                "base_path": base_path,
                "status": "created"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def load_project_context(self, project_path: str = "memory-bank") -> Dict[str, Any]:
        try:
            import os
            
            if not os.path.exists(project_path):
                return {"error": f"Project path {project_path} does not exist"}
            
            context_loaded = {
                "project_path": project_path,
                "sessions_found": 0,
                "patterns_found": 0,
                "status": "loaded"
            }
            
            sessions_path = f"{project_path}/sessions"
            if os.path.exists(sessions_path):
                context_loaded["sessions_found"] = len(os.listdir(sessions_path))
            
            patterns_path = f"{project_path}/patterns"
            if os.path.exists(patterns_path):
                context_loaded["patterns_found"] = len(os.listdir(patterns_path))
            
            return context_loaded
        except Exception as e:
            return {"error": str(e)}
    
    def update_project_index(self, section: str, content: str) -> Dict[str, Any]:
        try:
            filename = "project_knowledge_index.md"
            
            if not os.path.exists(filename):
                return {"error": f"Project index file {filename} does not exist"}
            
            with open(filename, 'r') as f:
                current_content = f.read()
            
            section_header = f"## {section}"
            if section_header in current_content:
                lines = current_content.split('\n')
                new_lines = []
                in_section = False
                
                for line in lines:
                    if line.strip() == section_header:
                        in_section = True
                        new_lines.append(line)
                        new_lines.append("")
                        new_lines.append(content)
                    elif line.startswith("## ") and in_section:
                        in_section = False
                        new_lines.append("")
                        new_lines.append(line)
                    elif not in_section:
                        new_lines.append(line)
                
                with open(filename, 'w') as f:
                    f.write('\n'.join(new_lines))
            
            return {
                "section": section,
                "filename": filename,
                "status": "updated"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def discover_packages(self, scan_imports: bool = True) -> Dict[str, Any]:
        try:
            packages = self.session_manager.explore_packages("general package discovery")
            return {
                "packages_discovered": len(packages),
                "packages": packages,
                "scan_imports": scan_imports
            }
        except Exception as e:
            return {"error": str(e)}
    
    def validate_package_usage(self, code_snippet: str) -> Dict[str, Any]:
        try:
            validation = self.auto_cycle.run_validation_gate(code_snippet)
            return validation
        except Exception as e:
            return {"error": str(e)}
    
    def execute_auto_cycle(
        self,
        enable_automation: bool = True,
        skip_steps: str = "",
        custom_thoughts: bool = False
    ) -> Dict[str, Any]:
        try:
            result = self.auto_cycle.execute_auto_cycle(enable_automation, skip_steps, custom_thoughts)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def explore_existing_apis(self, functionality: str) -> Dict[str, Any]:
        try:
            packages = self.session_manager.explore_packages(functionality)
            suggestions = self.session_manager._suggest_packages(functionality)
            
            return {
                "functionality": functionality,
                "discovered_packages": packages,
                "suggestions": suggestions,
                "total_found": len(packages) + len(suggestions)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def store_codebase_pattern(
        self,
        pattern_type: str,
        code_snippet: str,
        description: str = "",
        file_path: str = "",
        language: str = "",
        tags: str = ""
    ) -> Dict[str, Any]:
        try:
            if not self.session_manager.current_session:
                return {"error": "No active session"}
            
            
            pattern = CodePattern(
                pattern_type=pattern_type,
                code_snippet=code_snippet,
                description=description,
                file_path=file_path,
                language=language,
                tags=tags.split(",") if tags else [],
                session_id=self.session_manager.current_session.id
            )
            
            pattern_id = self.session_manager.db.save_code_pattern(pattern)
            self.session_manager.current_session.code_patterns.append(pattern)
            
            return {
                "pattern_id": pattern_id,
                "pattern_type": pattern_type,
                "language": language,
                "status": "stored"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def load_codebase_context(self, project_path: str = "") -> Dict[str, Any]:
        return self.load_project_context(project_path)
    
    def prevent_reinvention_check(self, functionality_description: str) -> Dict[str, Any]:
        try:
            packages = self.session_manager.explore_packages(functionality_description)
            reinvention_check = self.session_manager.detect_code_reinvention(functionality_description)
            
            return {
                "functionality_description": functionality_description,
                "existing_packages": packages,
                "reinvention_risk": reinvention_check,
                "recommendation": "Use existing packages" if packages else "Custom implementation may be needed"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def optimize_context_window(self, required_types: str = "") -> Dict[str, Any]:
        try:
            context_check = self.session_manager._check_context_size()
            
            if context_check["needs_chunking"]:
                required_list = [t.strip() for t in required_types.split(",") if t.strip()]
                window = self.session_manager.context_chunker.chunk_session(self.session_manager.current_session)
                
                if required_list:
                    optimized_window = self.session_manager.context_chunker.optimize_context_window(window, required_list)
                    return {
                        "optimization_applied": True,
                        "original_tokens": context_check["current_tokens"],
                        "optimized_tokens": optimized_window.total_tokens,
                        "chunks_preserved": len(optimized_window.chunks),
                        "required_types": required_list,
                        "priority_threshold": optimized_window.priority_threshold
                    }
                else:
                    return {
                        "optimization_available": True,
                        "current_tokens": context_check["current_tokens"],
                        "chunked_tokens": context_check["chunked_tokens"],
                        "chunks_available": context_check["chunks_created"],
                        "recommendation": "Specify required_types for targeted optimization"
                    }
            
            return {
                "optimization_needed": False,
                "current_tokens": context_check["current_tokens"],
                "max_tokens": context_check["max_tokens"]
            }
        except Exception as e:
            return {"error": str(e)}
    
    def _generate_markdown_export(self, session) -> str:
        content = f"# Session Export: {session.problem}\n\n"
        content += f"**Success Criteria:** {session.success_criteria}\n\n"
        content += f"**Constraints:** {session.constraints}\n\n"
        content += f"**Session Type:** {session.session_type.value}\n\n"
        
        if session.thoughts:
            content += "## Thoughts\n\n"
            for thought in session.thoughts:
                content += f"- {thought.content} (Confidence: {thought.confidence})\n"
        
        if session.memories:
            content += "\n## Memories\n\n"
            for memory in session.memories:
                content += f"- {memory.content} (Confidence: {memory.confidence})\n"
        
        if session.architecture_decisions:
            content += "\n## Architecture Decisions\n\n"
            for decision in session.architecture_decisions:
                content += f"### {decision.decision_title}\n"
                content += f"**Context:** {decision.context}\n"
                content += f"**Chosen Option:** {decision.chosen_option}\n"
                content += f"**Rationale:** {decision.rationale}\n\n"
        
        return content
    
    def _generate_json_export(self, session) -> str:
        export_data = {
            "session_id": session.id,
            "problem": session.problem,
            "success_criteria": session.success_criteria,
            "constraints": session.constraints,
            "session_type": session.session_type.value,
            "thoughts": [
                {
                    "id": t.id,
                    "content": t.content,
                    "confidence": t.confidence,
                    "status": t.status.value
                } for t in session.thoughts
            ],
            "memories": [
                {
                    "id": m.id,
                    "content": m.content,
                    "confidence": m.confidence,
                    "tags": m.tags
                } for m in session.memories
            ],
            "architecture_decisions": [
                {
                    "id": d.id,
                    "title": d.decision_title,
                    "context": d.context,
                    "chosen_option": d.chosen_option,
                    "rationale": d.rationale
                } for d in session.architecture_decisions
            ]
        }
        
        return json.dumps(export_data, indent=2, default=str)
    
    def _generate_memories_export(self, memories) -> str:
        content = "# Memories Export\n\n"
        
        for memory in memories:
            content += f"## {memory.id}\n\n"
            content += f"**Content:** {memory.content}\n\n"
            content += f"**Tags:** {', '.join(memory.tags)}\n\n"
            content += f"**Confidence:** {memory.confidence}\n\n"
            
            if memory.code_snippet:
                content += f"**Code Snippet:**\n```{memory.language}\n{memory.code_snippet}\n```\n\n"
            
            content += "---\n\n"
        
        return content
    
    def list_sessions(self) -> Dict[str, Any]:
        try:
            sessions = self.session_manager.list_sessions()
            return {
                "sessions": sessions,
                "count": len(sessions)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def load_session(self, session_id: str) -> Dict[str, Any]:
        try:
            result = self.session_manager.load_session(session_id)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def query_memories(self, tags: str = "", content_contains: str = "") -> Dict[str, Any]:
        try:
            memories = self.session_manager.query_memories(tags, content_contains)
            return {
                "memories": memories,
                "count": len(memories),
                "tags": tags,
                "content_contains": content_contains
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_active_session(self) -> Dict[str, Any]:
        try:
            session = self.session_manager.get_active_session()
            return {"active_session": session}
        except Exception as e:
            return {"error": str(e)}
    
    def switch_session(self, session_id: str) -> Dict[str, Any]:
        try:
            result = self.session_manager.switch_session(session_id)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def delete_session(self, session_id: str) -> Dict[str, Any]:
        try:
            result = self.session_manager.delete_session(session_id)
            return result
        except Exception as e:
            return {"error": str(e)}