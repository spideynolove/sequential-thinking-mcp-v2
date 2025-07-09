import sqlite3
import json
import shutil
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from models import SessionType, ThoughtStatus


class SchemaMigration:
    def __init__(self, db_path: str = "memory.db"):
        self.db_path = db_path
        self.backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def validate_memory_bank_schema(self) -> Dict[str, Any]:
        validation_result = {
            "valid": False,
            "tables_found": [],
            "missing_tables": [],
            "schema_conflicts": [],
            "data_integrity": True
        }
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
                existing_tables = [row[0] for row in cursor.fetchall()]
                validation_result["tables_found"] = existing_tables
                
                memory_bank_tables = ["sessions", "memories", "collections"]
                for table in memory_bank_tables:
                    if table not in existing_tables:
                        validation_result["missing_tables"].append(table)
                
                if "memories" in existing_tables:
                    cursor = conn.execute("PRAGMA table_info(memories)")
                    columns = {row[1]: row[2] for row in cursor.fetchall()}
                    
                    if "tags" in columns and columns["tags"] == "TEXT":
                        validation_result["schema_conflicts"].append({
                            "table": "memories",
                            "column": "tags", 
                            "current_type": "TEXT",
                            "required_type": "JSON_ARRAY"
                        })
                
                validation_result["valid"] = (
                    len(validation_result["missing_tables"]) == 0 and
                    len(validation_result["schema_conflicts"]) == 0
                )
                
        except Exception as e:
            validation_result["error"] = str(e)
            validation_result["data_integrity"] = False
        
        return validation_result
    
    def create_backup(self) -> bool:
        try:
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, self.backup_path)
                return True
            return False
        except Exception:
            return False
    
    def migrate_memory_bank_to_unified(self) -> Dict[str, Any]:
        migration_result = {
            "success": False,
            "backup_created": False,
            "tables_migrated": [],
            "data_transformed": [],
            "errors": []
        }
        
        migration_result["backup_created"] = self.create_backup()
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                self._migrate_sessions_table(conn, migration_result)
                self._migrate_memories_table(conn, migration_result)
                self._migrate_collections_table(conn, migration_result)
                self._add_unified_tables(conn, migration_result)
                
                migration_result["success"] = len(migration_result["errors"]) == 0
                
        except Exception as e:
            migration_result["errors"].append(f"Migration failed: {str(e)}")
            if migration_result["backup_created"]:
                self.rollback_from_backup()
        
        return migration_result
    
    def _migrate_sessions_table(self, conn: sqlite3.Connection, result: Dict[str, Any]):
        try:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sessions'")
            if cursor.fetchone():
                cursor = conn.execute("PRAGMA table_info(sessions)")
                existing_columns = {row[1] for row in cursor.fetchall()}
                
                required_columns = {
                    "session_type", "codebase_context", "package_exploration_required", 
                    "auto_validation"
                }
                missing_columns = required_columns - existing_columns
                
                for column in missing_columns:
                    if column == "session_type":
                        conn.execute("ALTER TABLE sessions ADD COLUMN session_type TEXT DEFAULT 'general'")
                    elif column == "codebase_context":
                        conn.execute("ALTER TABLE sessions ADD COLUMN codebase_context TEXT DEFAULT ''")
                    elif column == "package_exploration_required":
                        conn.execute("ALTER TABLE sessions ADD COLUMN package_exploration_required BOOLEAN DEFAULT 1")
                    elif column == "auto_validation":
                        conn.execute("ALTER TABLE sessions ADD COLUMN auto_validation BOOLEAN DEFAULT 0")
                
                conn.execute("UPDATE sessions SET session_type = 'general' WHERE session_type IS NULL")
                
                result["tables_migrated"].append("sessions")
            
        except Exception as e:
            result["errors"].append(f"Sessions table migration failed: {str(e)}")
    
    def _migrate_memories_table(self, conn: sqlite3.Connection, result: Dict[str, Any]):
        try:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='memories'")
            if cursor.fetchone():
                cursor = conn.execute("PRAGMA table_info(memories)")
                existing_columns = {row[1] for row in cursor.fetchall()}
                
                required_columns = {
                    "code_snippet", "language", "pattern_type", "importance"
                }
                missing_columns = required_columns - existing_columns
                
                for column in missing_columns:
                    if column == "code_snippet":
                        conn.execute("ALTER TABLE memories ADD COLUMN code_snippet TEXT DEFAULT ''")
                    elif column == "language":
                        conn.execute("ALTER TABLE memories ADD COLUMN language TEXT DEFAULT ''")
                    elif column == "pattern_type":
                        conn.execute("ALTER TABLE memories ADD COLUMN pattern_type TEXT DEFAULT ''")
                    elif column == "importance":
                        conn.execute("ALTER TABLE memories ADD COLUMN importance REAL DEFAULT 0.5")
                
                cursor = conn.execute("SELECT id, tags FROM memories WHERE tags IS NOT NULL")
                rows = cursor.fetchall()
                
                for memory_id, tags_str in rows:
                    try:
                        if isinstance(tags_str, str) and tags_str.strip():
                            if tags_str.startswith('[') and tags_str.endswith(']'):
                                tags_list = json.loads(tags_str)
                            else:
                                tags_list = [tag.strip() for tag in tags_str.split(',')]
                            
                            conn.execute(
                                "UPDATE memories SET tags = ? WHERE id = ?",
                                (json.dumps(tags_list), memory_id)
                            )
                    except (json.JSONDecodeError, TypeError):
                        conn.execute(
                            "UPDATE memories SET tags = ? WHERE id = ?",
                            (json.dumps([]), memory_id)
                        )
                
                result["data_transformed"].append("memories.tags")
                result["tables_migrated"].append("memories")
            
        except Exception as e:
            result["errors"].append(f"Memories table migration failed: {str(e)}")
    
    def _migrate_collections_table(self, conn: sqlite3.Connection, result: Dict[str, Any]):
        try:
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='collections'")
            if cursor.fetchone():
                cursor = conn.execute("SELECT id, memory_ids FROM collections WHERE memory_ids IS NOT NULL")
                rows = cursor.fetchall()
                
                for collection_id, memory_ids_str in rows:
                    try:
                        if isinstance(memory_ids_str, str):
                            if memory_ids_str.startswith('[') and memory_ids_str.endswith(']'):
                                memory_ids_list = json.loads(memory_ids_str)
                            else:
                                memory_ids_list = [mid.strip() for mid in memory_ids_str.split(',')]
                            
                            conn.execute(
                                "UPDATE collections SET memory_ids = ? WHERE id = ?",
                                (json.dumps(memory_ids_list), collection_id)
                            )
                    except (json.JSONDecodeError, TypeError):
                        conn.execute(
                            "UPDATE collections SET memory_ids = ? WHERE id = ?",
                            (json.dumps([]), collection_id)
                        )
                
                result["data_transformed"].append("collections.memory_ids")
                result["tables_migrated"].append("collections")
            
        except Exception as e:
            result["errors"].append(f"Collections table migration failed: {str(e)}")
    
    def _add_unified_tables(self, conn: sqlite3.Connection, result: Dict[str, Any]):
        try:
            unified_tables = {
                "thoughts": '''
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
                ''',
                "branches": '''
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
                ''',
                "architecture_decisions": '''
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
                ''',
                "packages": '''
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
                ''',
                "code_patterns": '''
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
                ''',
                "cross_system_context": '''
                    CREATE TABLE IF NOT EXISTS cross_system_context (
                        session_id TEXT PRIMARY KEY,
                        external_context TEXT,
                        shared_packages TEXT,
                        sync_timestamp TIMESTAMP,
                        FOREIGN KEY (session_id) REFERENCES sessions (id)
                    )
                '''
            }
            
            for table_name, create_sql in unified_tables.items():
                conn.execute(create_sql)
                result["tables_migrated"].append(table_name)
            
        except Exception as e:
            result["errors"].append(f"Unified tables creation failed: {str(e)}")
    
    def validate_data_integrity(self) -> Dict[str, Any]:
        integrity_result = {
            "valid": True,
            "checks": [],
            "errors": []
        }
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                checks = [
                    ("sessions_count", "SELECT COUNT(*) FROM sessions"),
                    ("memories_count", "SELECT COUNT(*) FROM memories"),
                    ("collections_count", "SELECT COUNT(*) FROM collections"),
                    ("thoughts_count", "SELECT COUNT(*) FROM thoughts"),
                    ("foreign_key_violations", "PRAGMA foreign_key_check")
                ]
                
                for check_name, sql in checks:
                    try:
                        cursor = conn.execute(sql)
                        if check_name == "foreign_key_violations":
                            violations = cursor.fetchall()
                            if violations:
                                integrity_result["errors"].append(f"Foreign key violations: {violations}")
                                integrity_result["valid"] = False
                            else:
                                integrity_result["checks"].append(f"{check_name}: none")
                        else:
                            count = cursor.fetchone()[0]
                            integrity_result["checks"].append(f"{check_name}: {count}")
                    except Exception as e:
                        integrity_result["errors"].append(f"{check_name} failed: {str(e)}")
                        integrity_result["valid"] = False
                
        except Exception as e:
            integrity_result["errors"].append(f"Integrity validation failed: {str(e)}")
            integrity_result["valid"] = False
        
        return integrity_result
    
    def rollback_from_backup(self) -> bool:
        try:
            if os.path.exists(self.backup_path):
                shutil.copy2(self.backup_path, self.db_path)
                return True
            return False
        except Exception:
            return False
    
    def cleanup_backup(self) -> bool:
        try:
            if os.path.exists(self.backup_path):
                os.remove(self.backup_path)
                return True
            return False
        except Exception:
            return False