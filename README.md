# ShipShape MCP Server

[![CI](https://github.com/UnderSampled/shipshape/actions/workflows/ci.yml/badge.svg)](https://github.com/UnderSampled/shipshape/actions/workflows/ci.yml)

A serverless Model Context Protocol (MCP) server for Cloudflare Workers, written in Python.

## Features

- Full MCP protocol support (tools, resources, prompts)
- Runs on Cloudflare Workers with Python
- Zero cold start overhead
- Simple decorator-based API

## Quick Start

### Prerequisites

- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/install-and-update/)
- Cloudflare account

### Development

```bash
# Run locally
wrangler dev

# Deploy
wrangler deploy
```

### Usage

The server exposes a JSON-RPC endpoint. Send POST requests with MCP protocol messages:

```bash
# Initialize
curl -X POST https://your-worker.workers.dev \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}'

# List tools
curl -X POST https://your-worker.workers.dev \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}'

# Call a tool
curl -X POST https://your-worker.workers.dev \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "greet", "arguments": {"name": "World"}}}'
```

## Included Tools

- **greet** - Greet a user by name
- **calculate** - Basic arithmetic (add, subtract, multiply, divide)
- **echo** - Echo input with optional uppercase transformation

## Adding Custom Tools

```python
from mcp_server import create_server, ToolContext

server = create_server(name="my-server", version="1.0.0")

@server.tool(
    name="my_tool",
    description="Description of what the tool does",
    input_schema={
        "type": "object",
        "properties": {
            "param": {"type": "string", "description": "Parameter description"}
        },
        "required": ["param"]
    }
)
async def my_tool(args: dict, context: ToolContext) -> str:
    return f"Result: {args['param']}"
```

## Project Structure

```
shipshape/
├── .github/workflows/
│   └── ci.yml           # CI workflow (lint, type check, test)
├── src/
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   ├── server.py    # Core MCP server
│   │   └── types.py     # Type definitions
│   └── worker.py        # Cloudflare Worker entry point
├── tests/
│   └── test_server.py   # Test suite
├── wrangler.toml        # Cloudflare config
├── pyproject.toml       # Python project config
└── README.md
```

## CI/CD

- **CI**: GitHub Actions runs linting (ruff), type checking (mypy), and tests on all pushes and PRs
- **Deployment**: Handled automatically by Cloudflare Workers GitHub integration on pushes to main

## License

MIT
