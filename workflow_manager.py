from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
import copy
from enum import Enum
from models import UnifiedSession


class WorkflowState(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class StepStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class WorkflowCheckpoint:
    step_id: str
    session_state: Dict[str, Any]
    database_state: Dict[str, Any]
    timestamp: datetime
    step_outputs: Dict[str, Any]


@dataclass
class WorkflowStep:
    id: str
    name: str
    description: str
    function: Callable
    validation_function: Optional[Callable]
    rollback_function: Optional[Callable]
    required_inputs: List[str]
    outputs: List[str]
    status: StepStatus = StepStatus.PENDING
    error_message: str = ""
    execution_time: float = 0.0
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class WorkflowExecution:
    id: str
    session_id: str
    workflow_type: str
    state: WorkflowState
    steps: List[WorkflowStep]
    checkpoints: List[WorkflowCheckpoint] = field(default_factory=list)
    current_step_index: int = 0
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    total_execution_time: float = 0.0
    error_details: Dict[str, Any] = field(default_factory=dict)


class WorkflowManager:
    def __init__(self, session_manager, database, auto_cycle_workflow):
        self.session_manager = session_manager
        self.database = database
        self.auto_cycle = auto_cycle_workflow
        self.active_executions: Dict[str, WorkflowExecution] = {}
        self.workflow_definitions: Dict[str, List[WorkflowStep]] = {}
        self._setup_auto_cycle_workflow()
    
    def _setup_auto_cycle_workflow(self):
        auto_cycle_steps = [
            WorkflowStep(
                id="step_1_package_discovery",
                name="Package Discovery",
                description="Discover relevant packages for the session",
                function=self._execute_package_discovery,
                validation_function=self._validate_package_discovery,
                rollback_function=self._rollback_package_discovery,
                required_inputs=["session_id"],
                outputs=["discovered_packages"]
            ),
            WorkflowStep(
                id="step_2_thought_generation",
                name="Thought Generation",
                description="Generate structured thoughts for the problem",
                function=self._execute_thought_generation,
                validation_function=self._validate_thought_generation,
                rollback_function=self._rollback_thought_generation,
                required_inputs=["session_id"],
                outputs=["generated_thoughts"]
            ),
            WorkflowStep(
                id="step_3_memory_storage",
                name="Memory Storage",
                description="Store insights as persistent memories",
                function=self._execute_memory_storage,
                validation_function=self._validate_memory_storage,
                rollback_function=self._rollback_memory_storage,
                required_inputs=["session_id", "generated_thoughts"],
                outputs=["stored_memories"]
            ),
            WorkflowStep(
                id="step_4_architecture_decisions",
                name="Architecture Decisions",
                description="Record architecture decisions with context",
                function=self._execute_architecture_decisions,
                validation_function=self._validate_architecture_decisions,
                rollback_function=self._rollback_architecture_decisions,
                required_inputs=["session_id"],
                outputs=["architecture_decisions"]
            ),
            WorkflowStep(
                id="step_5_validation_analysis",
                name="Validation Analysis",
                description="Analyze session completeness and consistency",
                function=self._execute_validation_analysis,
                validation_function=self._validate_validation_analysis,
                rollback_function=None,
                required_inputs=["session_id"],
                outputs=["validation_results"]
            )
        ]
        
        self.workflow_definitions["auto_cycle"] = auto_cycle_steps
    
    def execute_workflow(self, workflow_type: str, session_id: str, inputs: Dict[str, Any]) -> str:
        if workflow_type not in self.workflow_definitions:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        
        execution_id = f"{workflow_type}_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        steps = copy.deepcopy(self.workflow_definitions[workflow_type])
        
        execution = WorkflowExecution(
            id=execution_id,
            session_id=session_id,
            workflow_type=workflow_type,
            state=WorkflowState.PENDING,
            steps=steps
        )
        
        self.active_executions[execution_id] = execution
        
        try:
            return self._run_workflow(execution, inputs)
        except Exception as e:
            execution.state = WorkflowState.FAILED
            execution.error_details = {"error": str(e), "step": execution.current_step_index}
            return execution_id
    
    def _run_workflow(self, execution: WorkflowExecution, inputs: Dict[str, Any]) -> str:
        execution.state = WorkflowState.RUNNING
        execution.start_time = datetime.now()
        
        step_outputs = inputs.copy()
        
        for i, step in enumerate(execution.steps):
            execution.current_step_index = i
            
            try:
                checkpoint = self._create_checkpoint(execution, step.id, step_outputs)
                execution.checkpoints.append(checkpoint)
                
                step_result = self._execute_step(step, step_outputs)
                
                if step.validation_function:
                    validation_result = step.validation_function(step_result)
                    if not validation_result.get("valid", False):
                        raise Exception(f"Validation failed: {validation_result.get('error', 'Unknown error')}")
                
                step.status = StepStatus.COMPLETED
                step_outputs.update(step_result)
                
            except Exception as e:
                step.status = StepStatus.FAILED
                step.error_message = str(e)
                execution.error_details = {
                    "step_id": step.id,
                    "step_name": step.name,
                    "error": str(e),
                    "step_index": i
                }
                
                if step.retry_count < step.max_retries:
                    step.retry_count += 1
                    step.status = StepStatus.PENDING
                    i -= 1
                    continue
                else:
                    rollback_result = self._rollback_workflow(execution, i)
                    execution.state = WorkflowState.ROLLED_BACK
                    execution.error_details["rollback_result"] = rollback_result
                    break
        
        if all(step.status == StepStatus.COMPLETED for step in execution.steps):
            execution.state = WorkflowState.COMPLETED
        
        execution.end_time = datetime.now()
        execution.total_execution_time = (execution.end_time - execution.start_time).total_seconds()
        
        return execution.id
    
    def _execute_step(self, step: WorkflowStep, inputs: Dict[str, Any]) -> Dict[str, Any]:
        step.status = StepStatus.RUNNING
        start_time = datetime.now()
        
        try:
            result = step.function(inputs)
            end_time = datetime.now()
            step.execution_time = (end_time - start_time).total_seconds()
            return result
        except Exception as e:
            end_time = datetime.now()
            step.execution_time = (end_time - start_time).total_seconds()
            raise e
    
    def _create_checkpoint(self, execution: WorkflowExecution, step_id: str, step_outputs: Dict[str, Any]) -> WorkflowCheckpoint:
        session = self.session_manager.current_session
        session_state = {
            "session_id": session.id if session else None,
            "thoughts_count": len(session.thoughts) if session else 0,
            "memories_count": len(session.memories) if session else 0,
            "decisions_count": len(session.architecture_decisions) if session else 0,
            "packages_count": len(session.discovered_packages) if session else 0
        }
        
        database_state = self._capture_database_state(execution.session_id)
        
        return WorkflowCheckpoint(
            step_id=step_id,
            session_state=session_state,
            database_state=database_state,
            timestamp=datetime.now(),
            step_outputs=step_outputs.copy()
        )
    
    def _capture_database_state(self, session_id: str) -> Dict[str, Any]:
        try:
            with self.database.db_path as db_path:
                import sqlite3
                with sqlite3.connect(db_path) as conn:
                    state = {}
                    
                    tables = ["sessions", "thoughts", "memories", "collections", 
                             "architecture_decisions", "packages", "code_patterns"]
                    
                    for table in tables:
                        try:
                            cursor = conn.execute(f"SELECT COUNT(*) FROM {table} WHERE session_id = ?", (session_id,))
                            count = cursor.fetchone()[0]
                            state[f"{table}_count"] = count
                        except Exception:
                            state[f"{table}_count"] = 0
                    
                    return state
        except Exception:
            return {}
    
    def _rollback_workflow(self, execution: WorkflowExecution, failed_step_index: int) -> Dict[str, Any]:
        rollback_result = {
            "rollback_steps": [],
            "errors": [],
            "success": False
        }
        
        for i in range(failed_step_index, -1, -1):
            step = execution.steps[i]
            
            if step.status == StepStatus.COMPLETED and step.rollback_function:
                try:
                    checkpoint = self._find_checkpoint_for_step(execution, step.id)
                    if checkpoint:
                        rollback_data = {
                            "step_outputs": checkpoint.step_outputs,
                            "session_state": checkpoint.session_state,
                            "database_state": checkpoint.database_state
                        }
                        
                        step.rollback_function(rollback_data)
                        rollback_result["rollback_steps"].append(step.id)
                        step.status = StepStatus.PENDING
                except Exception as e:
                    rollback_result["errors"].append(f"Rollback failed for {step.id}: {str(e)}")
        
        if not rollback_result["errors"]:
            rollback_result["success"] = True
        
        return rollback_result
    
    def _find_checkpoint_for_step(self, execution: WorkflowExecution, step_id: str) -> Optional[WorkflowCheckpoint]:
        for checkpoint in reversed(execution.checkpoints):
            if checkpoint.step_id == step_id:
                return checkpoint
        return None
    
    def _execute_package_discovery(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        session_id = inputs["session_id"]
        session = self.database.get_session(session_id)
        
        if not session:
            raise Exception(f"Session {session_id} not found")
        
        discovered_packages = self.session_manager.explore_packages(session.problem)
        
        return {
            "discovered_packages": discovered_packages,
            "package_count": len(discovered_packages)
        }
    
    def _validate_package_discovery(self, result: Dict[str, Any]) -> Dict[str, Any]:
        packages = result.get("discovered_packages", [])
        return {
            "valid": len(packages) >= 0,
            "package_count": len(packages)
        }
    
    def _rollback_package_discovery(self, rollback_data: Dict[str, Any]):
        pass
    
    def _execute_thought_generation(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        session_id = inputs["session_id"]
        session = self.database.get_session(session_id)
        
        if not session:
            raise Exception(f"Session {session_id} not found")
        
        auto_thoughts = self.auto_cycle._generate_auto_thoughts(session.problem, session.success_criteria)
        thought_ids = []
        
        for thought_content in auto_thoughts:
            thought_id = self.session_manager.add_thought(
                content=thought_content,
                confidence=0.7,
                explore_packages=True
            )
            thought_ids.append(thought_id)
        
        return {
            "generated_thoughts": thought_ids,
            "thought_count": len(thought_ids)
        }
    
    def _validate_thought_generation(self, result: Dict[str, Any]) -> Dict[str, Any]:
        thoughts = result.get("generated_thoughts", [])
        return {
            "valid": len(thoughts) > 0,
            "thought_count": len(thoughts)
        }
    
    def _rollback_thought_generation(self, rollback_data: Dict[str, Any]):
        generated_thoughts = rollback_data["step_outputs"].get("generated_thoughts", [])
        
        for thought_id in generated_thoughts:
            try:
                with self.database.db_path as db_path:
                    import sqlite3
                    with sqlite3.connect(db_path) as conn:
                        conn.execute("DELETE FROM thoughts WHERE id = ?", (thought_id,))
            except Exception:
                pass
    
    def _execute_memory_storage(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        session_id = inputs["session_id"]
        generated_thoughts = inputs.get("generated_thoughts", [])
        
        memory_ids = []
        
        for thought_id in generated_thoughts:
            try:
                memory_id = self.session_manager.store_memory(
                    content=f"Auto-generated memory from thought {thought_id}",
                    confidence=0.7,
                    pattern_type="auto_generated"
                )
                memory_ids.append(memory_id)
            except Exception as e:
                raise Exception(f"Memory storage failed for thought {thought_id}: {str(e)}")
        
        return {
            "stored_memories": memory_ids,
            "memory_count": len(memory_ids)
        }
    
    def _validate_memory_storage(self, result: Dict[str, Any]) -> Dict[str, Any]:
        memories = result.get("stored_memories", [])
        return {
            "valid": len(memories) >= 0,
            "memory_count": len(memories)
        }
    
    def _rollback_memory_storage(self, rollback_data: Dict[str, Any]):
        stored_memories = rollback_data["step_outputs"].get("stored_memories", [])
        
        for memory_id in stored_memories:
            try:
                with self.database.db_path as db_path:
                    import sqlite3
                    with sqlite3.connect(db_path) as conn:
                        conn.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            except Exception:
                pass
    
    def _execute_architecture_decisions(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        session_id = inputs["session_id"]
        session = self.database.get_session(session_id)
        
        if not session:
            raise Exception(f"Session {session_id} not found")
        
        decision_id = self.session_manager.record_architecture_decision(
            decision_title="Auto-cycle Decision Framework",
            context=f"Problem: {session.problem}",
            options_considered="Auto-generated options based on discovered packages",
            chosen_option="Systematic approach with package integration",
            rationale="Automated decision making for consistency",
            consequences="Standardized approach, may need human review"
        )
        
        return {
            "architecture_decisions": [decision_id],
            "decision_count": 1
        }
    
    def _validate_architecture_decisions(self, result: Dict[str, Any]) -> Dict[str, Any]:
        decisions = result.get("architecture_decisions", [])
        return {
            "valid": len(decisions) > 0,
            "decision_count": len(decisions)
        }
    
    def _rollback_architecture_decisions(self, rollback_data: Dict[str, Any]):
        decisions = rollback_data["step_outputs"].get("architecture_decisions", [])
        
        for decision_id in decisions:
            try:
                with self.database.db_path as db_path:
                    import sqlite3
                    with sqlite3.connect(db_path) as conn:
                        conn.execute("DELETE FROM architecture_decisions WHERE id = ?", (decision_id,))
            except Exception:
                pass
    
    def _execute_validation_analysis(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        session_id = inputs["session_id"]
        analysis = self.session_manager.analyze_thinking()
        
        return {
            "validation_results": analysis,
            "overall_score": analysis.get("overall_score", 0.0)
        }
    
    def _validate_validation_analysis(self, result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "valid": True,
            "analysis_completed": True
        }
    
    def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        if execution_id not in self.active_executions:
            return None
        
        execution = self.active_executions[execution_id]
        
        return {
            "execution_id": execution.id,
            "session_id": execution.session_id,
            "workflow_type": execution.workflow_type,
            "state": execution.state.value,
            "current_step": execution.current_step_index,
            "total_steps": len(execution.steps),
            "steps": [
                {
                    "id": step.id,
                    "name": step.name,
                    "status": step.status.value,
                    "error_message": step.error_message,
                    "execution_time": step.execution_time,
                    "retry_count": step.retry_count
                } for step in execution.steps
            ],
            "checkpoints": len(execution.checkpoints),
            "total_execution_time": execution.total_execution_time,
            "error_details": execution.error_details
        }
    
    def cancel_execution(self, execution_id: str) -> Dict[str, Any]:
        if execution_id not in self.active_executions:
            return {"error": "Execution not found"}
        
        execution = self.active_executions[execution_id]
        
        if execution.state == WorkflowState.RUNNING:
            rollback_result = self._rollback_workflow(execution, execution.current_step_index)
            execution.state = WorkflowState.ROLLED_BACK
            execution.end_time = datetime.now()
            
            return {
                "execution_id": execution_id,
                "cancelled": True,
                "rollback_result": rollback_result
            }
        
        return {
            "execution_id": execution_id,
            "cancelled": False,
            "reason": f"Cannot cancel execution in state: {execution.state.value}"
        }