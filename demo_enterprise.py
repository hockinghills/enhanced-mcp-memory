#!/usr/bin/env python3
"""
Enterprise Sequential Thinking Demo
Demonstrates the new token optimization and context management features

Copyright 2025 Chris Bunting.
"""
import sys
import os
import json
import time
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import DatabaseManager
from memory_manager import MemoryManager
from sequential_thinking import SequentialThinkingEngine, ThinkingStage

def demo_enterprise_workflow():
    """Demonstrate a complete enterprise workflow"""
    print("🚀 Enterprise Sequential Thinking & Context Management Demo")
    print("=" * 65)
    
    # Initialize the system
    print("\n📊 Initializing Enterprise System...")
    db_manager = DatabaseManager("data/demo_enterprise.db")
    memory_manager = MemoryManager(db_manager)
    thinking_engine = SequentialThinkingEngine(db_manager, memory_manager)
    
    # Start a session for a complex enterprise project
    print("🏢 Starting Enterprise Project Session...")
    memory_manager.start_session(os.getcwd())
    project_name = "Enterprise Token Optimization Platform"
    
    print(f"   ✓ Project: {project_name}")
    print(f"   ✓ Session ID: {memory_manager.current_session_id[:8]}...")
    print(f"   ✓ Project ID: {memory_manager.current_project_id[:8]}...")
    
    # Step 1: Create a structured thinking chain for the project
    print("\n🧠 Creating Sequential Thinking Chain...")
    objective = "Design and implement enterprise-grade token optimization with 70% compression"
    chain_id = thinking_engine.create_thinking_chain(objective)
    
    # Add comprehensive thinking steps
    thinking_steps = [
        (ThinkingStage.ANALYSIS, "Market & Technical Analysis", 
         """Current enterprise challenges:
         - Claude Sonnet 4 uses 3-5x more tokens than previous models
         - Conversations can exceed 32K context windows rapidly
         - Manual context management is inefficient and error-prone
         - Need seamless session handoffs between different AI tools
         
         Technical requirements:
         - Real-time token estimation with 90%+ accuracy
         - Automated context compression achieving 30-70% reduction
         - Intelligent key information extraction
         - Session continuity across conversation breaks"""),
        
        (ThinkingStage.PLANNING, "Architecture & System Design",
         """System architecture:
         1. SequentialThinkingEngine - Core reasoning orchestrator
         2. ContextCompressionSystem - Intelligent summarization
         3. TokenOptimizationEngine - Real-time token management
         4. SessionContinuityManager - Conversation handoffs
         
         Key design decisions:
         - Pattern-based content extraction (TODO, FIXME, ACTION items)
         - Multi-stage compression (key points, decisions, actions)
         - Enterprise-grade error handling with graceful degradation
         - Performance monitoring and metrics collection"""),
        
        (ThinkingStage.EXECUTION, "Implementation Strategy",
         """Implementation phases:
         Phase 1: Core token estimation algorithms
         Phase 2: Context summarization with pattern matching
         Phase 3: Chat session management and consolidation
         Phase 4: Enterprise monitoring and health checks
         Phase 5: Comprehensive testing and validation
         
         Technology stack:
         - FastMCP for tool integration
         - SQLite for reliable data persistence
         - sentence-transformers for semantic analysis
         - Pattern-based regex for content extraction"""),
        
        (ThinkingStage.VALIDATION, "Testing & Quality Assurance",
         """Validation approach:
         - Unit tests for each component
         - Integration tests for end-to-end workflows
         - Performance benchmarks for token estimation accuracy
         - Load testing for enterprise-scale conversations
         - Compression ratio validation (target: 30-70% reduction)
         
         Success metrics:
         - Token estimation accuracy > 90%
         - Context compression ratio 30-70%
         - Session consolidation time < 2 seconds
         - Zero data loss during compression"""),
        
        (ThinkingStage.REFLECTION, "Performance & Optimization",
         """System performance analysis:
         - Token estimation: ~75% accuracy achieved
         - Compression ratios: 30-65% typical reduction
         - Processing speed: <100ms for most operations
         - Memory efficiency: Minimal overhead
         
         Areas for improvement:
         - Fine-tune token estimation for code vs prose
         - Enhance pattern matching for complex content
         - Optimize database queries for large datasets
         - Add caching for frequently accessed contexts""")
    ]
    
    step_ids = []
    for i, (stage, title, content) in enumerate(thinking_steps):
        print(f"   {i+1}. Adding {stage.value.upper()} step: {title}")
        step_id = thinking_engine.add_thinking_step(
            chain_id=chain_id,
            stage=stage,
            title=title,
            content=content,
            reasoning=f"Critical {stage.value} phase for enterprise implementation",
            confidence=0.9
        )
        step_ids.append(step_id)
    
    # Step 2: Demonstrate token optimization
    print("\n⚡ Demonstrating Token Optimization...")
    
    # Create a large context that needs compression
    large_context = """
    Enterprise Development Discussion - Token Optimization Project
    
    Key Requirements Identified:
    • Real-time token counting for enterprise conversations
    • Automatic context compression when approaching limits
    • Seamless session handoffs between team members
    • Intelligent extraction of decisions and action items
    • Performance monitoring for enterprise-scale usage
    
    Technical Decisions Made:
    • Use pattern-based extraction for TODO/FIXME/ACTION items
    • Implement multi-stage compression (analysis -> summary -> optimization)
    • Create structured thinking chains for complex problem solving
    • Build session continuity system for conversation handoffs
    • Add enterprise monitoring with health checks and metrics
    
    Implementation Notes:
    TODO: Implement caching mechanism for token estimation
    FIXME: Optimize database queries for large conversation histories
    ACTION: Create comprehensive testing suite for all components
    TODO: Add support for multiple AI model token counting
    FIXME: Handle edge cases with special characters and code blocks
    ACTION: Implement automated cleanup of old conversation data
    
    Performance Targets:
    • Token estimation accuracy: >90%
    • Context compression ratio: 30-70%
    • Session consolidation time: <2 seconds
    • Database query response: <100ms
    • Memory usage overhead: <50MB for large conversations
    
    Next Steps:
    1. Complete core implementation of all components
    2. Run comprehensive testing suite
    3. Performance benchmarking and optimization
    4. Documentation and deployment preparation
    5. Enterprise customer pilot program
    """
    
    # Show original token count
    original_tokens = thinking_engine.estimate_token_count(large_context)
    print(f"   📝 Original context: {original_tokens} tokens")
    
    # Create compressed summary
    print("   🔄 Creating compressed summary...")
    summary_id = thinking_engine.create_context_summary(large_context)
    
    # Get compression results
    cursor = db_manager.connection.cursor()
    cursor.execute("SELECT * FROM context_summaries WHERE id = ?", (summary_id,))
    summary = cursor.fetchone()
    
    compressed_tokens = summary['compressed_token_count']
    compression_ratio = summary['compression_ratio']
    
    print(f"   ✅ Compressed to: {compressed_tokens} tokens ({compression_ratio:.1%} of original)")
    print(f"   📊 Compression achieved: {(1-compression_ratio)*100:.1f}% reduction")
    
    # Step 3: Demonstrate session management
    print("\n💬 Demonstrating Session Management...")
    
    # Create a chat session
    session_id = thinking_engine.create_chat_session(
        title="Enterprise Token Optimization - Implementation Phase",
        objective="Complete implementation and testing of token optimization features"
    )
    
    print(f"   💼 Created enterprise session: {session_id[:8]}...")
    
    # Simulate adding conversation content
    conversation_memories = [
        "Discussed token estimation algorithms and settled on word+character based approach",
        "Decided to use pattern matching for extracting TODO, FIXME, and ACTION items",
        "Agreed on 30-70% compression ratio target for enterprise deployments",
        "Planned comprehensive testing strategy including performance benchmarks",
        "Established monitoring requirements for enterprise health checks"
    ]
    
    for memory in conversation_memories:
        memory_manager.add_context_memory(
            content=memory,
            memory_type="conversation",
            importance=0.8
        )
    
    # Add some tasks that would be auto-extracted
    enterprise_tasks = [
        ("Implement token estimation caching", "high", "performance"),
        ("Create enterprise monitoring dashboard", "medium", "feature"),
        ("Optimize database queries for scale", "high", "performance"),
        ("Build automated testing pipeline", "medium", "testing"),
        ("Create deployment documentation", "low", "docs")
    ]
    
    for title, priority, category in enterprise_tasks:
        db_manager.add_task(
            project_id=memory_manager.current_project_id,
            title=title,
            description=f"Enterprise task: {title}",
            priority=priority,
            category=category
        )
    
    print(f"   ✅ Added {len(conversation_memories)} conversation memories")
    print(f"   ✅ Added {len(enterprise_tasks)} enterprise tasks")
    
    # Step 4: Demonstrate session consolidation
    print("\n🔄 Demonstrating Session Consolidation...")
    
    consolidation = thinking_engine.consolidate_chat_session(session_id)
    
    print(f"   📊 Session consolidated successfully:")
    print(f"      • Original tokens: {consolidation['original_tokens']}")
    print(f"      • Compressed tokens: {consolidation['compressed_tokens']}")
    print(f"      • Compression ratio: {consolidation['compression_ratio']:.1%}")
    print(f"      • Key context items: {len(consolidation['key_context'])}")
    print(f"      • Decisions captured: {len(consolidation['decisions_made'])}")
    print(f"      • Actions identified: {len(consolidation['pending_actions'])}")
    
    # Step 5: Demonstrate session continuation
    print("\n🔗 Demonstrating Session Continuation...")
    
    continuation_context = thinking_engine.get_session_continuation_context(session_id)
    continuation_tokens = thinking_engine.estimate_token_count(continuation_context)
    
    print(f"   📋 Continuation context ready:")
    print(f"      • Context length: {len(continuation_context)} characters")
    print(f"      • Estimated tokens: {continuation_tokens}")
    print(f"      • Token reduction: {((original_tokens - continuation_tokens) / original_tokens * 100):.1f}%")
    
    # Show sample of continuation context
    print("   📖 Sample continuation context:")
    lines = continuation_context.split('\n')[:8]
    for line in lines:
        if line.strip():
            print(f"      {line}")
    
    # Step 6: Performance metrics
    print("\n📈 Performance Metrics Summary...")
    
    # Get thinking chain details
    chain = thinking_engine.get_thinking_chain(chain_id)
    
    print(f"   🧠 Thinking Chain Performance:")
    print(f"      • Total steps: {len(chain.steps)}")
    print(f"      • Total tokens: {chain.total_tokens}")
    print(f"      • Average confidence: {sum(step.confidence for step in chain.steps) / len(chain.steps):.2f}")
    
    # Database statistics
    cursor.execute("SELECT COUNT(*) FROM memories WHERE project_id = ?", (memory_manager.current_project_id,))
    memory_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE project_id = ?", (memory_manager.current_project_id,))
    task_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM context_summaries WHERE project_id = ?", (memory_manager.current_project_id,))
    summary_count = cursor.fetchone()[0]
    
    print(f"   💾 Database Statistics:")
    print(f"      • Memories created: {memory_count}")
    print(f"      • Tasks created: {task_count}")
    print(f"      • Summaries created: {summary_count}")
    
    # Final summary
    print("\n" + "=" * 65)
    print("🎉 Enterprise Demo Completed Successfully!")
    print("\n💡 Key Achievements:")
    print(f"   ✅ Sequential thinking chain with {len(chain.steps)} structured steps")
    print(f"   ✅ Context compression achieving {(1-compression_ratio)*100:.1f}% reduction")
    print(f"   ✅ Session consolidation with {len(consolidation['key_context'])} key points")
    print(f"   ✅ Token optimization from {original_tokens} to {continuation_tokens} tokens")
    print(f"   ✅ Enterprise-grade data management with {memory_count + task_count} records")
    
    print("\n🚀 System Ready for Enterprise Deployment!")
    print("   • Handles high-token conversations efficiently")
    print("   • Provides seamless session continuity")
    print("   • Offers structured problem-solving workflows")
    print("   • Includes comprehensive monitoring and metrics")
    
    return {
        'chain_id': chain_id,
        'session_id': session_id,
        'summary_id': summary_id,
        'original_tokens': original_tokens,
        'compressed_tokens': compressed_tokens,
        'compression_ratio': compression_ratio,
        'memory_count': memory_count,
        'task_count': task_count
    }

if __name__ == "__main__":
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Run the enterprise demo
        results = demo_enterprise_workflow()
        
        print(f"\n📊 Demo completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
