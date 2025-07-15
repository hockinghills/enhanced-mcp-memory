# Repository Setup Guide

## 📁 Directory Structure Changes

To properly set up your GitHub repository, you'll need to rename your current directory and create the repository with the correct name.

### Current Setup
- **Current directory**: `C:\mcpservers\kiro`
- **Should be**: `C:\mcpservers\kiro-mcp-memory`

### Recommended Steps

1. **Rename the directory** (optional but recommended):
   ```bash
   # Navigate to parent directory
   cd C:\mcpservers
   
   # Rename the directory
   mv kiro kiro-mcp-memory
   cd kiro-mcp-memory
   ```

2. **Initialize Git repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Kiro MCP Memory server v1.2.0"
   ```

3. **Create GitHub repository**:
   - Go to GitHub and create a new repository named `kiro-mcp-memory`
   - **Repository URL**: `https://github.com/cbunting99/kiro-mcp-memory`

4. **Connect local repository to GitHub**:
   ```bash
   git remote add origin https://github.com/cbunting99/kiro-mcp-memory.git
   git branch -M main
   git push -u origin main
   ```

## 📦 Package Configuration

The package has been updated with the correct repository information:

### ✅ Updated Files
- `pyproject.toml` - Author and repository URLs updated
- `setup.py` - Author and project URLs updated  
- `README.md` - All GitHub URLs updated
- `INSTALLATION.md` - Installation commands updated

### 🔗 Repository URLs
All references now point to:
- **Repository**: `https://github.com/cbunting99/kiro-mcp-memory`
- **Issues**: `https://github.com/cbunting99/kiro-mcp-memory/issues`
- **Documentation**: `https://github.com/cbunting99/kiro-mcp-memory#readme`

## 🚀 uvx Installation

Once the repository is set up, users can install your package with:

```bash
# From GitHub (after repository is created)
uvx --from git+https://github.com/cbunting99/kiro-mcp-memory.git kiro-mcp-memory

# Or if published to PyPI
uvx kiro-mcp-memory
```

## 📋 MCP Configuration

Users should configure their MCP client with:

```json
{
  "mcpServers": {
    "memory-manager": {
      "command": "uvx",
      "args": ["kiro-mcp-memory"],
      "env": {
        "LOG_LEVEL": "INFO",
        "MAX_MEMORY_ITEMS": "1000",
        "ENABLE_AUTO_CLEANUP": "true"
      }
    }
  }
}
```

## 🎯 Next Steps

1. **Create the GitHub repository** with the name `kiro-mcp-memory`
2. **Push your code** to the new repository
3. **Test the installation** from GitHub:
   ```bash
   pip install git+https://github.com/cbunting99/kiro-mcp-memory.git
   ```
4. **Consider publishing to PyPI** for easier uvx installation

## 📝 Repository Description

For your GitHub repository, use this description:
> Enhanced MCP server for intelligent memory and task management with semantic search, automatic task extraction, and knowledge graphs. Compatible with uvx for easy installation.

## 🏷️ Repository Topics

Add these topics to your GitHub repository:
- `mcp`
- `memory-management`
- `task-management`
- `ai`
- `semantic-search`
- `knowledge-graph`
- `python`
- `uvx`
- `fastmcp`

Your package is now properly configured for the correct repository structure!