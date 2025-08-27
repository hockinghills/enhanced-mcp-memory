"""
Cloudflare Memory Manager
Adapted for Cloudflare Workers environment with D1, KV, and Workers AI
"""

import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any

class CloudflareMemoryManager:
    """Memory manager adapted for Cloudflare Workers"""
    
    def __init__(self, db_manager, embeddings, kv_cache):
        """Initialize with Cloudflare service bindings"""
        self.db_manager = db_manager
        self.embeddings = embeddings
        self.kv = kv_cache
        
        # Current session info
        self.current_project_id = None
        self.session_id = None
        
    async def get_memory_context(self, query: str = "") -> str:
        """Get current memory context and task reminders"""
        try:
            # Ensure we have a current project
            if not self.current_project_id:
                await self.start_session()
            
            context_parts = []
            
            # Add project info
            context_parts.append(f"## Current Project: {self.current_project_id[:8]}...")
            context_parts.append("Description: Auto-detected project")
            
            # Get relevant memories if query provided
            if query:
                memories = await self._search_memories(query, limit=5)
                if memories:
                    context_parts.append("## 🧠 Relevant Memories")
                    for memory in memories[:3]:  # Top 3 most relevant
                        context_parts.append(f"### {memory.get('type', 'memory').title()}: {memory.get('title', 'Untitled')}")
                        context_parts.append(memory.get('content', '')[:200] + "..." if len(memory.get('content', '')) > 200 else memory.get('content', ''))
            
            # Get pending tasks
            tasks = await self.get_pending_tasks(limit=5)
            if tasks:
                context_parts.append("## Pending Tasks:")
                for task in tasks:
                    priority = task.get('priority', 'medium')
                    context_parts.append(f"- [{priority}] {task.get('title', 'Untitled')}")
            
            # Add task reminder
            context_parts.append("## Task Reminder:")
            context_parts.append("Remember to create or update tasks for the current project as needed.")
            
            return "\\n\\n".join(context_parts) if context_parts else "No context available"
            
        except Exception as e:
            console.error(f"Error getting memory context: {e}")
            return f"Error retrieving context: {str(e)}"
    
    async def start_session(self):
        """Start a new session"""
        self.session_id = str(uuid.uuid4())
        self.current_project_id = await self._get_or_create_default_project()
    
    async def _get_or_create_default_project(self) -> str:
        """Get or create a default project"""
        try:
            # For now, create a simple project ID
            project_id = f"project_{datetime.now().strftime('%Y%m%d')}"
            
            # TODO: Implement proper project creation in D1
            # For now, just return the ID
            return project_id
            
        except Exception as e:
            console.error(f"Error creating project: {e}")
            return "default_project"
    
    async def create_task(self, title: str, description: str = "", priority: str = "medium", category: str = "feature") -> str:
        """Create a new task"""
        try:
            if not self.current_project_id:
                await self.start_session()
            
            task_id = await self.db_manager.add_task(
                project_id=self.current_project_id,
                title=title,
                description=description,
                priority=priority,
                category=category,
                metadata={'source': 'manual', 'created_by': 'ai_tool'}
            )
            
            return task_id
            
        except Exception as e:
            console.error(f"Error creating task: {e}")
            raise e
    
    async def get_pending_tasks(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get pending tasks for the current project"""
        try:
            if not self.current_project_id:
                return []
            
            tasks = await self.db_manager.get_tasks(
                self.current_project_id, 
                status='pending', 
                limit=limit
            )
            
            return tasks
            
        except Exception as e:
            console.error(f"Error getting pending tasks: {e}")
            return []
    
    async def _search_memories(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search memories using semantic similarity"""
        try:
            # TODO: Implement proper semantic search with embeddings
            # For now, return empty list
            memories = await self.db_manager.get_memories(
                project_id=self.current_project_id,
                limit=limit
            )
            
            # If we have embeddings available, do semantic search
            if memories and self.embeddings:
                # This would use the embeddings for similarity search
                # For now, just return the memories as-is
                pass
            
            return memories
            
        except Exception as e:
            console.error(f"Error searching memories: {e}")
            return []
    
    async def add_memory(self, memory_type: str, title: str, content: str, **kwargs) -> str:
        """Add a new memory"""
        try:
            if not self.current_project_id:
                await self.start_session()
            
            # Generate embedding for content
            embedding = await self.embeddings.generate_embedding(content)
            
            memory_id = await self.db_manager.add_memory(
                project_id=self.current_project_id,
                memory_type=memory_type,
                title=title,
                content=content,
                embedding=embedding,
                **kwargs
            )
            
            return memory_id
            
        except Exception as e:
            console.error(f"Error adding memory: {e}")
            raise e