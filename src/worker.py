"""
Enhanced MCP Memory Server for Cloudflare Workers
Main entry point and Durable Object implementation
"""

import os
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Import Cloudflare Workers runtime
from js import Request, Response, console
from pyodide.ffi import create_proxy

try:
    from fastmcp import FastMCP, Context
except ImportError as e:
    console.error("FastMCP not available - this is expected in Cloudflare Workers environment")
    # We'll implement a lightweight MCP protocol handler instead

# Import our adapted modules (will need to be created/adapted)
from .database_d1 import D1DatabaseManager
from .memory_manager_cf import CloudflareMemoryManager
from .sequential_thinking_cf import CloudflareSequentialThinking
from .embeddings_cf import CloudflareEmbeddings

class MemoryManagerMCP:
    """
    Durable Object class for the Enhanced MCP Memory Server
    Handles persistent WebSocket connections and MCP protocol
    """
    
    def __init__(self, ctx, env):
        """Initialize the Durable Object with Cloudflare bindings"""
        self.ctx = ctx
        self.env = env
        self.state = ctx.state
        
        # Initialize Cloudflare service connections
        self.db = env.DB  # D1 database
        self.kv = env.KV_CACHE  # KV namespace
        self.ai = env.AI  # Workers AI
        self.r2 = env.R2_STORAGE  # R2 bucket
        
        # Initialize our adapted components
        self.db_manager = D1DatabaseManager(self.db)
        self.embeddings = CloudflareEmbeddings(self.ai)
        self.memory_manager = CloudflareMemoryManager(
            self.db_manager, 
            self.embeddings,
            self.kv
        )
        self.thinking_engine = CloudflareSequentialThinking(
            self.db_manager, 
            self.memory_manager,
            self.embeddings
        )
        
        # MCP tools registry
        self.tools = self._register_tools()
        
        # Performance tracking
        self.start_time = datetime.now()
        self.call_counts = {}
        
    def _register_tools(self) -> Dict[str, Any]:
        """Register all MCP tools"""
        tools = {}
        
        # Core Memory Tools
        tools['health_check'] = self.health_check
        tools['get_memory_context'] = self.get_memory_context
        tools['create_task'] = self.create_task
        tools['get_tasks'] = self.get_tasks
        tools['update_task_status'] = self.update_task_status
        tools['get_project_summary'] = self.get_project_summary
        
        # Sequential Thinking Tools  
        tools['start_thinking_chain'] = self.start_thinking_chain
        tools['add_thinking_step'] = self.add_thinking_step
        tools['get_thinking_chain'] = self.get_thinking_chain
        tools['list_thinking_chains'] = self.list_thinking_chains
        
        # Context Management Tools
        tools['create_context_summary'] = self.create_context_summary
        tools['start_new_chat_session'] = self.start_new_chat_session
        tools['consolidate_current_session'] = self.consolidate_current_session
        tools['get_optimized_context'] = self.get_optimized_context
        tools['estimate_token_usage'] = self.estimate_token_usage
        
        # Auto-Processing Tools
        tools['auto_process_conversation'] = self.auto_process_conversation
        tools['decompose_task'] = self.decompose_task
        
        # Project Convention Tools
        tools['auto_learn_project_conventions'] = self.auto_learn_project_conventions
        tools['get_project_conventions'] = self.get_project_conventions
        tools['suggest_correct_command'] = self.suggest_correct_command
        tools['remember_project_pattern'] = self.remember_project_pattern
        tools['update_memory_context'] = self.update_memory_context
        
        # System Management Tools
        tools['get_performance_stats'] = self.get_performance_stats
        tools['cleanup_old_data'] = self.cleanup_old_data
        tools['optimize_memories'] = self.optimize_memories
        tools['get_database_stats'] = self.get_database_stats
        
        return tools
    
    async def fetch(self, request):
        """Handle HTTP requests - main entry point for MCP communication"""
        try:
            url = request.url
            method = request.method
            
            # Handle CORS preflight
            if method == 'OPTIONS':
                return self._cors_response()
            
            # Parse request path
            if '/mcp' in url:
                return await self._handle_mcp_request(request)
            elif '/health' in url:
                return await self._handle_health_check(request)
            else:
                return self._json_response({
                    'error': 'Not found',
                    'available_endpoints': ['/mcp', '/health']
                }, 404)
                
        except Exception as e:
            console.error(f"Error handling request: {e}")
            return self._json_response({'error': str(e)}, 500)
    
    async def _handle_mcp_request(self, request):
        """Handle MCP protocol requests"""
        try:
            # Parse request body
            body = await request.json() if request.method == 'POST' else {}
            
            # Extract MCP method and parameters
            method = body.get('method')
            params = body.get('params', {})
            request_id = body.get('id')
            
            # Handle different MCP methods
            if method == 'initialize':
                return self._mcp_response({
                    'protocolVersion': '2024-11-05',
                    'capabilities': {
                        'tools': {},
                        'resources': {},
                        'prompts': {}
                    },
                    'serverInfo': {
                        'name': 'enhanced-mcp-memory-cf',
                        'version': '2.0.8-cloudflare'
                    }
                }, request_id)
            
            elif method == 'tools/list':
                return self._mcp_response({
                    'tools': [
                        {
                            'name': name,
                            'description': getattr(tool, '__doc__', f'Tool: {name}')
                        }
                        for name, tool in self.tools.items()
                    ]
                }, request_id)
            
            elif method == 'tools/call':
                tool_name = params.get('name')
                tool_params = params.get('arguments', {})
                
                if tool_name in self.tools:
                    # Track call count
                    self.call_counts[tool_name] = self.call_counts.get(tool_name, 0) + 1
                    
                    # Execute tool
                    result = await self._execute_tool(tool_name, tool_params)
                    return self._mcp_response({
                        'content': [{
                            'type': 'text',
                            'text': result
                        }]
                    }, request_id)
                else:
                    return self._mcp_error(f'Unknown tool: {tool_name}', request_id)
            
            else:
                return self._mcp_error(f'Unknown method: {method}', request_id)
                
        except Exception as e:
            console.error(f"MCP request error: {e}")
            return self._mcp_error(str(e), body.get('id'))
    
    async def _execute_tool(self, tool_name: str, params: Dict[str, Any]) -> str:
        """Execute a registered tool"""
        try:
            tool_func = self.tools[tool_name]
            
            # Call the tool function with parameters
            if hasattr(tool_func, '__code__') and tool_func.__code__.co_argcount > 1:
                # Function takes parameters
                result = await tool_func(**params)
            else:
                # Function takes no parameters
                result = await tool_func()
            
            return result if isinstance(result, str) else json.dumps(result, indent=2)
            
        except Exception as e:
            console.error(f"Tool execution error for {tool_name}: {e}")
            return json.dumps({'error': f'Tool execution failed: {str(e)}'})
    
    # ==================== MCP TOOL IMPLEMENTATIONS ====================
    
    async def health_check(self) -> str:
        """Check server health and database connectivity"""
        try:
            # Test D1 database
            await self.db_manager.test_connection()
            
            # Get basic stats
            stats = await self.db_manager.get_database_stats()
            
            health_info = {
                "status": "healthy",
                "database": "connected",
                "active_sessions": 1,
                "total_memories": stats.get('memories_count', 0),
                "total_tasks": stats.get('tasks_count', 0),
                "uptime_minutes": int((datetime.now() - self.start_time).total_seconds() / 60),
                "call_counts": self.call_counts,
                "timestamp": datetime.now().isoformat()
            }
            
            return json.dumps(health_info, indent=2)
        except Exception as e:
            return json.dumps({
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            })
    
    async def get_memory_context(self, query: str = "") -> str:
        """Get current memory context and task reminders for the AI"""
        try:
            context = await self.memory_manager.get_memory_context(query)
            return context if context else "No context available"
        except Exception as e:
            console.error(f"Error getting memory context: {e}")
            return f"Error retrieving context: {str(e)}"
    
    async def create_task(self, title: str, description: str = "", priority: str = "medium", category: str = "feature") -> str:
        """Create a new task for the current project"""
        try:
            task_id = await self.memory_manager.create_task(
                title=title,
                description=description,
                priority=priority,
                category=category
            )
            return f"✅ Task created: '{title}' (ID: {task_id[:8]}...)"
        except Exception as e:
            console.error(f"Error creating task: {e}")
            return f"⚠️ Error creating task: {str(e)}"
    
    # Add placeholder implementations for other tools
    async def get_tasks(self, status: str = None, limit: int = 20) -> str:
        """Get tasks for the current project"""
        return json.dumps({"placeholder": "get_tasks implementation needed"})
    
    async def update_task_status(self, task_id: str, status: str) -> str:
        """Update task status"""
        return json.dumps({"placeholder": "update_task_status implementation needed"})
    
    async def get_project_summary(self) -> str:
        """Get comprehensive project overview"""
        return json.dumps({"placeholder": "get_project_summary implementation needed"})
    
    async def start_thinking_chain(self, objective: str) -> str:
        """Begin structured reasoning process"""
        return json.dumps({"placeholder": "start_thinking_chain implementation needed"})
    
    async def add_thinking_step(self, chain_id: str, stage: str, title: str, content: str, reasoning: str = "") -> str:
        """Add reasoning steps"""
        return json.dumps({"placeholder": "add_thinking_step implementation needed"})
    
    async def get_thinking_chain(self, chain_id: str) -> str:
        """Retrieve complete thinking chain"""  
        return json.dumps({"placeholder": "get_thinking_chain implementation needed"})
    
    async def list_thinking_chains(self, limit: int = 10) -> str:
        """List recent thinking chains"""
        return json.dumps({"placeholder": "list_thinking_chains implementation needed"})
    
    async def create_context_summary(self, content: str, key_points: str = "", decisions: str = "", actions: str = "") -> str:
        """Compress context for token optimization"""
        return json.dumps({"placeholder": "create_context_summary implementation needed"})
    
    async def start_new_chat_session(self, title: str, objective: str = "", continue_from: str = "") -> str:
        """Begin new conversation with optional continuation"""
        return json.dumps({"placeholder": "start_new_chat_session implementation needed"})
    
    async def consolidate_current_session(self) -> str:
        """Compress current session for handoff"""
        return json.dumps({"placeholder": "consolidate_current_session implementation needed"})
    
    async def get_optimized_context(self, max_tokens: int = 4000) -> str:
        """Get token-optimized context"""
        return json.dumps({"placeholder": "get_optimized_context implementation needed"})
    
    async def estimate_token_usage(self, text: str) -> str:
        """Estimate token count for planning"""
        return json.dumps({"placeholder": "estimate_token_usage implementation needed"})
    
    async def auto_process_conversation(self, content: str, interaction_type: str = "conversation") -> str:
        """Extract memories and tasks automatically"""
        return json.dumps({"placeholder": "auto_process_conversation implementation needed"})
    
    async def decompose_task(self, prompt: str) -> str:
        """Break complex tasks into subtasks"""
        return json.dumps({"placeholder": "decompose_task implementation needed"})
    
    async def auto_learn_project_conventions(self) -> str:
        """Automatically detect and learn project patterns"""
        return json.dumps({"placeholder": "auto_learn_project_conventions implementation needed"})
    
    async def get_project_conventions(self) -> str:
        """Get formatted summary of learned conventions"""
        return json.dumps({"placeholder": "get_project_conventions implementation needed"})
    
    async def suggest_correct_command(self, user_command: str) -> str:
        """Suggest project-appropriate command corrections"""
        return json.dumps({"placeholder": "suggest_correct_command implementation needed"})
    
    async def remember_project_pattern(self, pattern_type: str, pattern_name: str, pattern_content: str, importance: float = 0.8) -> str:
        """Manually store project patterns"""
        return json.dumps({"placeholder": "remember_project_pattern implementation needed"})
    
    async def update_memory_context(self, query: str = "") -> str:
        """Refresh memory context with latest project conventions"""
        return json.dumps({"placeholder": "update_memory_context implementation needed"})
    
    async def get_performance_stats(self) -> str:
        """Get server performance statistics"""
        uptime_seconds = (datetime.now() - self.start_time).total_seconds()
        stats = {
            "uptime_hours": round(uptime_seconds / 3600, 2),
            "call_counts": self.call_counts,
            "total_calls": sum(self.call_counts.values())
        }
        return json.dumps(stats, indent=2)
    
    async def cleanup_old_data(self, days_old: int = 30) -> str:
        """Clean up old memories and tasks"""
        return json.dumps({"placeholder": "cleanup_old_data implementation needed"})
    
    async def optimize_memories(self) -> str:
        """Remove duplicates and optimize storage"""
        return json.dumps({"placeholder": "optimize_memories implementation needed"})
    
    async def get_database_stats(self) -> str:
        """Get comprehensive database statistics"""
        try:
            stats = await self.db_manager.get_database_stats()
            return json.dumps(stats, indent=2)
        except Exception as e:
            return json.dumps({"error": f"Failed to get database stats: {str(e)}"})
    
    # ==================== UTILITY METHODS ====================
    
    async def _handle_health_check(self, request):
        """Simple health check endpoint"""
        return self._json_response({'status': 'ok', 'timestamp': datetime.now().isoformat()})
    
    def _cors_response(self):
        """Return CORS preflight response"""
        return Response(None, {
            'status': 204,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            }
        })
    
    def _json_response(self, data: Dict[str, Any], status: int = 200):
        """Return JSON response with CORS headers"""
        return Response(
            json.dumps(data),
            {
                'status': status,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                }
            }
        )
    
    def _mcp_response(self, result: Any, request_id: Optional[str] = None):
        """Format MCP protocol response"""
        response = {
            'jsonrpc': '2.0',
            'result': result
        }
        if request_id is not None:
            response['id'] = request_id
        return self._json_response(response)
    
    def _mcp_error(self, message: str, request_id: Optional[str] = None):
        """Format MCP protocol error response"""
        response = {
            'jsonrpc': '2.0',
            'error': {
                'code': -1,
                'message': message
            }
        }
        if request_id is not None:
            response['id'] = request_id
        return self._json_response(response, 400)


# Entry point for Cloudflare Workers
async def on_fetch(request, env):
    """Main entry point for HTTP requests to the Worker"""
    try:
        # Create Durable Object instance
        id = env.MEMORY_MCP.idFromName("memory-mcp-singleton")
        stub = env.MEMORY_MCP.get(id)
        
        # Forward request to Durable Object
        return await stub.fetch(request)
        
    except Exception as e:
        console.error(f"Worker error: {e}")
        return Response(
            json.dumps({'error': 'Internal server error'}),
            {
                'status': 500,
                'headers': {'Content-Type': 'application/json'}
            }
        )

# Export the handler
fetch = create_proxy(on_fetch)