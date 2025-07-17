# Enhanced MCP Memory - Installation Guide

## Quick Start with uvx (Recommended)

The easiest way to install and run Enhanced MCP Memory is using `uvx`:

```bash
# Install and run directly
uvx enhanced-mcp-memory
```

This will automatically:
- Download and install the package
- Install all dependencies
- Start the MCP server

## MCP Client Configuration

Add this to your MCP client configuration file:

### For uvx installation:
```json
{
  "mcpServers": {
    "memory-manager": {
      "command": "uvx",
      "args": ["enhanced-mcp-memory"],
      "env": {
        "LOG_LEVEL": "INFO",
        "MAX_MEMORY_ITEMS": "1000",
        "ENABLE_AUTO_CLEANUP": "true"
      }
    }
  }
}
```

### For local development:
```json
{
  "mcpServers": {
    "memory-manager": {
      "command": "python",
      "args": ["mcp_server_enhanced.py"],
      "cwd": "/path/to/enhanced-mcp-memory",
      "env": {
        "LOG_LEVEL": "INFO",
        "MAX_MEMORY_ITEMS": "1000",
        "ENABLE_AUTO_CLEANUP": "true"
      }
    }
  }
}
```

## Alternative Installation Methods

### Method 1: pip install from PyPI (when published)
```bash
pip install enhanced-mcp-memory
enhanced-mcp-memory
```

### Method 2: pip install from source
```bash
pip install git+https://github.com/cbunting99/enhanced-mcp-memory.git
enhanced-mcp-memory
```

### Method 3: Development installation
```bash
git clone https://github.com/cbunting99/enhanced-mcp-memory.git
cd enhanced-mcp-memory
pip install -e .
enhanced-mcp-memory
```

### Method 4: Run directly from source
```bash
git clone https://github.com/cbunting99/enhanced-mcp-memory.git
cd enhanced-mcp-memory
pip install -r requirements.txt
python mcp_server_enhanced.py
```

## Environment Variables

Configure the server behavior using these environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `MAX_MEMORY_ITEMS` | `1000` | Maximum memories per project |
| `CLEANUP_INTERVAL_HOURS` | `24` | Auto-cleanup interval |
| `ENABLE_AUTO_CLEANUP` | `true` | Enable automatic cleanup |
| `MAX_CONCURRENT_REQUESTS` | `5` | Max concurrent requests |
| `REQUEST_TIMEOUT` | `30` | Request timeout in seconds |

## First Run

On first startup, the server will:
1. Create a `data/` directory for the SQLite database
2. Create a `logs/` directory for log files
3. Download the sentence-transformers model (~90MB) for semantic search
4. Initialize the database schema

## Verification

Test that the installation works:

```bash
# Test import
python -c "import mcp_server_enhanced; print('✅ Installation successful')"

# Run tests (if installed from source)
python run_tests.py
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed
   ```bash
   pip install -r requirements.txt
   ```

2. **Permission errors**: The server needs write access to create `data/` and `logs/` directories

3. **Model download fails**: Ensure internet connection for downloading the AI model on first run

4. **Unicode errors on Windows**: The server handles this automatically, but ensure your terminal supports UTF-8

### Getting Help

- Check the logs in `logs/mcp_memory_YYYYMMDD.log`
- Use the `health_check()` tool to verify server status
- Run `get_performance_stats()` to check performance metrics

## Next Steps

Once installed, you can:
1. Use `get_memory_context()` to retrieve relevant memories
2. Use `create_task()` to add new tasks
3. Use `health_check()` to monitor server health
4. Explore all available tools in your MCP client

For more information, see the main [README.md](README.md) file.