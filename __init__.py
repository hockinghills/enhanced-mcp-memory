# Copyright 2025 Chris Bunting.
"""
Enhanced MCP Memory Server Package

Enterprise-grade MCP server with sequential thinking, project convention learning, 
and intelligent memory management capabilities.
"""

__version__ = "2.0.0"
__author__ = "Chris Bunting"
__email__ = "cbunting99@users.noreply.github.com"

# Import main components for easier access
from .mcp_server_enhanced import main
from .memory_manager import MemoryManager
from .database import DatabaseManager
from .sequential_thinking import SequentialThinkingEngine, ThinkingStage
from .project_conventions import ProjectConventionLearner

__all__ = [
    'main',
    'MemoryManager', 
    'DatabaseManager',
    'SequentialThinkingEngine',
    'ThinkingStage',
    'ProjectConventionLearner'
]
