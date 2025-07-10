from typing import Dict, Any, List
from datetime import datetime
from session_manager import UnifiedSessionManager
from models import ThoughtStatus, SessionType
from workflow_manager import WorkflowManager


class AutoCycleWorkflow:
    def __init__(self, session_manager: UnifiedSessionManager):
        self.session_manager = session_manager
        self.workflow_manager = WorkflowManager(session_manager, session_manager.db, self)
    
    def execute_auto_cycle(
        self, 
        enable_automation: bool = True,
        skip_steps: str = "",
        custom_thoughts: bool = False
    ) -> Dict[str, Any]:
        session = self.session_manager.current_session
        if not session:
            return {"error": "No active session"}
        
        if not enable_automation:
            return {"message": "Auto-cycle disabled by user choice"}
        
        inputs = {
            "session_id": session.id,
            "skip_steps": skip_steps,
            "custom_thoughts": custom_thoughts
        }
        
        execution_id = self.workflow_manager.execute_workflow("auto_cycle", session.id, inputs)
        return self.workflow_manager.get_execution_status(execution_id)
    
    def _step_1_package_discovery(self) -> Dict[str, Any]:
        session = self.session_manager.current_session
        if not session:
            return {"step": 1, "name": "Package Discovery", "status": "failed", "error": "No session"}
        
        if session.session_type == SessionType.CODING and session.package_exploration_required:
            discovered = self.session_manager.explore_packages(session.problem)
            return {
                "step": 1,
                "name": "Package Discovery",
                "status": "completed",
                "packages_found": len(discovered),
                "packages": discovered[:10]
            }
        
        return {"step": 1, "name": "Package Discovery", "status": "skipped", "reason": "Not a coding session"}
    
    def _step_2_thought_generation(self, custom_thoughts: bool = False) -> Dict[str, Any]:
        session = self.session_manager.current_session
        if not session:
            return {"step": 2, "name": "Thought Generation", "status": "failed", "error": "No session"}
        
        if custom_thoughts:
            return {
                "step": 2,
                "name": "Thought Generation",
                "status": "skipped",
                "reason": "Custom thoughts mode - use manual add_thought() calls"
            }
        
        auto_thoughts = self._generate_auto_thoughts(session.problem, session.success_criteria)
        thought_ids = []
        
        for thought_content in auto_thoughts:
            thought_id = self.session_manager.add_thought(
                content=thought_content,
                confidence=0.7,
                explore_packages=True
            )
            thought_ids.append(thought_id)
        
        return {
            "step": 2,
            "name": "Thought Generation",
            "status": "completed",
            "thoughts_generated": len(thought_ids),
            "thought_ids": thought_ids
        }
    
    def _step_3_memory_storage(self) -> Dict[str, Any]:
        session = self.session_manager.current_session
        if not session:
            return {"step": 3, "name": "Memory Storage", "status": "failed", "error": "No session"}
        
        memory_ids = []
        
        for thought in session.thoughts:
            if thought.status == ThoughtStatus.ACTIVE:
                memory_id = self.session_manager.store_memory(
                    content=f"Thought: {thought.content}",
                    confidence=thought.confidence,
                    pattern_type="auto_generated"
                )
                memory_ids.append(memory_id)
        
        return {
            "step": 3,
            "name": "Memory Storage",
            "status": "completed",
            "memories_stored": len(memory_ids),
            "memory_ids": memory_ids
        }
    
    def _step_4_architecture_decisions(self) -> Dict[str, Any]:
        session = self.session_manager.current_session
        if not session:
            return {"step": 4, "name": "Architecture Decisions", "status": "failed", "error": "No session"}
        
        if session.session_type != SessionType.CODING:
            return {"step": 4, "name": "Architecture Decisions", "status": "skipped", "reason": "Not a coding session"}
        
        decision_id = self.session_manager.record_architecture_decision(
            decision_title="Auto-cycle Decision Framework",
            context=f"Problem: {session.problem}",
            options_considered="Auto-generated options based on discovered packages",
            chosen_option="Systematic approach with package integration",
            rationale="Automated decision making for consistency",
            consequences="Standardized approach, may need human review"
        )
        
        return {
            "step": 4,
            "name": "Architecture Decisions",
            "status": "completed",
            "decision_id": decision_id
        }
    
    def _step_5_validation_analysis(self) -> Dict[str, Any]:
        session = self.session_manager.current_session
        if not session:
            return {"step": 5, "name": "Validation Analysis", "status": "failed", "error": "No session"}
        
        analysis = self.session_manager.analyze_thinking()
        
        validation_results = {
            "completeness_score": self._calculate_completeness(session),
            "consistency_score": self._calculate_consistency(session),
            "package_integration_score": self._calculate_package_integration(session),
            "overall_score": 0.0
        }
        
        validation_results["overall_score"] = (
            validation_results["completeness_score"] + 
            validation_results["consistency_score"] + 
            validation_results["package_integration_score"]
        ) / 3
        
        return {
            "step": 5,
            "name": "Validation Analysis",
            "status": "completed",
            "analysis": analysis,
            "validation": validation_results
        }
    
    def _generate_auto_thoughts(self, problem: str, success_criteria: str) -> List[str]:
        base_thoughts = [
            f"Problem analysis: {problem}",
            f"Success criteria: {success_criteria}",
            "First principles: What are the core requirements?",
            "Constraints: What limitations do we have?",
            "Implementation approach: How should we proceed?"
        ]
        
        session = self.session_manager.current_session
        if session and session.session_type == SessionType.CODING:
            coding_thoughts = [
                "Package discovery: What existing libraries can help?",
                "Architecture considerations: How should components interact?",
                "Testing strategy: How will we validate the solution?",
                "Deployment considerations: How will this be deployed?"
            ]
            base_thoughts.extend(coding_thoughts)
        
        return base_thoughts
    
    def _calculate_completeness(self, session) -> float:
        min_thoughts = 5
        min_memories = 3
        
        thought_score = min(len(session.thoughts) / min_thoughts, 1.0)
        memory_score = min(len(session.memories) / min_memories, 1.0)
        
        return (thought_score + memory_score) / 2
    
    def _calculate_consistency(self, session) -> float:
        if not session.thoughts:
            return 0.0
        
        consistency_score = 0.0
        for thought in session.thoughts:
            if thought.confidence > 0.7:
                consistency_score += 0.1
        
        return min(consistency_score, 1.0)
    
    def _calculate_package_integration(self, session) -> float:
        if session.session_type != SessionType.CODING:
            return 1.0
        
        if not session.discovered_packages:
            return 0.0
        
        integration_score = 0.0
        for package in session.discovered_packages:
            if package.relevance_score > 0.5:
                integration_score += 0.2
        
        return min(integration_score, 1.0)
    
    def run_validation_gate(self, proposed_code: str) -> Dict[str, Any]:
        session = self.session_manager.current_session
        if not session:
            return {"error": "No active session"}
        
        validation_results = {
            "timestamp": datetime.now(),
            "session_id": session.id,
            "code_length": len(proposed_code),
            "checks": []
        }
        
        reinvention_check = self.session_manager.detect_code_reinvention(proposed_code)
        validation_results["checks"].append({
            "name": "Code Reinvention Check",
            "status": "warning" if reinvention_check["reinvention_detected"] else "passed",
            "details": reinvention_check
        })
        
        package_suggestions = self.session_manager._suggest_packages(proposed_code)
        validation_results["checks"].append({
            "name": "Package Suggestion Check",
            "status": "info",
            "suggestions": package_suggestions
        })
        
        validation_results["overall_status"] = "warning" if any(
            check["status"] == "warning" for check in validation_results["checks"]
        ) else "passed"
        
        return validation_results