"""Cloudflare Worker entry point for the MCP server."""

from js import Headers, Response

from mcp_server import ToolContext, create_server

# Create the MCP server
server = create_server(name="shipshape-mcp", version="1.0.0")


# Register tools using decorators
@server.tool(
    name="greet",
    description="Greet a user by name",
    input_schema={
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "The name to greet"}
        },
        "required": ["name"],
    },
)
async def greet(args: dict, context: ToolContext) -> str:
    name = args.get("name", "World")
    return f"Hello, {name}!"


@server.tool(
    name="calculate",
    description="Perform basic arithmetic operations",
    input_schema={
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
                "description": "The operation to perform",
            },
            "a": {"type": "number", "description": "First operand"},
            "b": {"type": "number", "description": "Second operand"},
        },
        "required": ["operation", "a", "b"],
    },
)
async def calculate(args: dict, context: ToolContext) -> dict:
    op = args["operation"]
    a = args["a"]
    b = args["b"]

    operations = {
        "add": lambda: a + b,
        "subtract": lambda: a - b,
        "multiply": lambda: a * b,
        "divide": lambda: a / b if b != 0 else "Error: Division by zero",
    }

    result = operations[op]()
    return {"operation": op, "a": a, "b": b, "result": result}


@server.tool(
    name="echo",
    description="Echo back the input with optional transformation",
    input_schema={
        "type": "object",
        "properties": {
            "message": {"type": "string", "description": "The message to echo"},
            "uppercase": {
                "type": "boolean",
                "description": "Convert to uppercase",
                "default": False,
            },
        },
        "required": ["message"],
    },
)
async def echo(args: dict, context: ToolContext) -> dict:
    message = args["message"]
    uppercase = args.get("uppercase", False)
    result = message.upper() if uppercase else message
    return {
        "original": message,
        "result": result,
        "server": context.server_info.name,
    }


@server.resource(
    uri="status://health",
    name="Health Status",
    description="Server health information",
    mime_type="application/json",
)
async def health_status(uri: str) -> dict:
    return {
        "text": '{"status": "healthy", "server": "shipshape-mcp"}',
        "mimeType": "application/json",
    }


@server.prompt(
    name="code_review",
    description="Generate a code review prompt",
    arguments=[
        {"name": "code", "description": "The code to review", "required": True},
        {"name": "language", "description": "Programming language", "required": False},
    ],
)
async def code_review_prompt(args: dict) -> list[dict]:
    code = args.get("code", "")
    language = args.get("language", "")
    return [
        {
            "role": "user",
            "content": f"Please review this {language} code:\n\n```{language}\n{code}\n```",
        }
    ]


async def on_fetch(request, env):
    """Cloudflare Worker fetch handler."""
    method = request.method
    body = None

    if method == "POST":
        body = await request.text()

    status, headers_dict, response_body = await server.handle_http(method, body)

    headers = Headers.new()
    for key, value in headers_dict.items():
        headers.set(key, value)

    return Response.new(response_body, status=status, headers=headers)
