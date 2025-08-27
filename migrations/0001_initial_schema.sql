-- Initial schema for Enhanced MCP Memory on Cloudflare D1
-- Based on the original SQLite schema, adapted for D1

-- Projects table - tracks different coding projects
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    path TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT  -- JSON metadata
);

-- Memories table - stores contextual information and learning
CREATE TABLE IF NOT EXISTS memories (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    type TEXT NOT NULL,  -- 'code', 'conversation', 'decision', 'pattern', 'error', 'thinking_chain', 'thinking_step'
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding_vector TEXT,  -- JSON array for semantic search
    content_hash TEXT,  -- Hash for duplicate detection
    file_path TEXT,  -- Associated file path
    importance_score REAL DEFAULT 0.5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accessed_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP,
    tags TEXT,  -- JSON array of tags
    metadata TEXT,  -- JSON metadata
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Tasks table - tracks development tasks and TODOs
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending',  -- 'pending', 'in_progress', 'completed', 'cancelled'
    priority TEXT DEFAULT 'medium',  -- 'low', 'medium', 'high', 'critical'
    category TEXT,  -- 'bug', 'feature', 'refactor', 'docs', 'test'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP,
    estimated_hours REAL,
    actual_hours REAL,
    tags TEXT,  -- JSON array
    metadata TEXT,  -- JSON metadata
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Knowledge Graph - relationships between memories, tasks, and concepts
CREATE TABLE IF NOT EXISTS knowledge_relationships (
    id TEXT PRIMARY KEY,
    from_type TEXT NOT NULL,  -- 'memory', 'task', 'project', 'concept'
    from_id TEXT NOT NULL,
    to_type TEXT NOT NULL,
    to_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,  -- 'depends_on', 'relates_to', 'conflicts_with', 'implements', 'references'
    strength REAL DEFAULT 1.0,  -- relationship strength (0.0 to 1.0)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT  -- JSON metadata
);

-- Sessions table - tracks AI interaction sessions
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    interaction_count INTEGER DEFAULT 0,
    context_summary TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Thinking chains table - for sequential thinking
CREATE TABLE IF NOT EXISTS thinking_chains (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    objective TEXT NOT NULL,
    status TEXT DEFAULT 'active',  -- 'active', 'completed', 'abandoned'
    current_stage TEXT DEFAULT 'analysis',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    metadata TEXT,  -- JSON metadata including steps
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Project conventions - learned patterns and conventions
CREATE TABLE IF NOT EXISTS project_conventions (
    id TEXT PRIMARY KEY,
    project_id TEXT,
    pattern_type TEXT NOT NULL,  -- 'command', 'tool', 'environment', 'dependency'
    pattern_name TEXT NOT NULL,
    pattern_content TEXT NOT NULL,
    importance REAL DEFAULT 0.5,
    confidence REAL DEFAULT 0.5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    metadata TEXT,  -- JSON metadata
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_memories_project_id ON memories(project_id);
CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(type);
CREATE INDEX IF NOT EXISTS idx_memories_created_at ON memories(created_at);
CREATE INDEX IF NOT EXISTS idx_memories_importance ON memories(importance_score);

CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);

CREATE INDEX IF NOT EXISTS idx_knowledge_relationships_from ON knowledge_relationships(from_type, from_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_relationships_to ON knowledge_relationships(to_type, to_id);

CREATE INDEX IF NOT EXISTS idx_sessions_project_id ON sessions(project_id);
CREATE INDEX IF NOT EXISTS idx_sessions_started_at ON sessions(started_at);

CREATE INDEX IF NOT EXISTS idx_thinking_chains_project_id ON thinking_chains(project_id);
CREATE INDEX IF NOT EXISTS idx_thinking_chains_status ON thinking_chains(status);

CREATE INDEX IF NOT EXISTS idx_project_conventions_project_id ON project_conventions(project_id);
CREATE INDEX IF NOT EXISTS idx_project_conventions_type ON project_conventions(pattern_type);
CREATE INDEX IF NOT EXISTS idx_project_conventions_importance ON project_conventions(importance);