"""Serverless MCP Server implementation."""

import json
from collections.abc import Awaitable, Callable
from dataclasses import asdict, dataclass, field
from typing import Any

from .types import (
    JsonRpcError,
    JsonRpcRequest,
    JsonRpcResponse,
    Prompt,
    Resource,
    ServerCapabilities,
    ServerInfo,
    Tool,
    ToolContext,
)


class McpError(Exception):
    """Custom error for MCP protocol errors."""

    def __init__(self, code: int, message: str, data: Any = None):
        super().__init__(message)
        self.code = code
        self.data = data


@dataclass
class McpServer:
    """
    Serverless MCP Server.

    A Model Context Protocol server designed for serverless environments.
    Handles JSON-RPC requests over HTTP without requiring persistent connections.
    """

    name: str
    version: str
    capabilities: ServerCapabilities = field(default_factory=ServerCapabilities)
    _tools: dict[str, Tool] = field(default_factory=dict)
    _resources: dict[str, Resource] = field(default_factory=dict)
    _resource_handlers: dict[str, Callable[[str], Awaitable[dict[str, Any]]]] = field(
        default_factory=dict
    )
    _prompts: dict[str, Prompt] = field(default_factory=dict)
    _prompt_handlers: dict[
        str, Callable[[dict[str, str]], Awaitable[list[dict[str, str]]]]
    ] = field(default_factory=dict)

    @property
    def server_info(self) -> ServerInfo:
        return ServerInfo(name=self.name, version=self.version)

    def tool(
        self,
        name: str,
        description: str,
        input_schema: dict[str, Any] | None = None,
    ) -> Callable[[Callable[..., Awaitable[Any]]], Callable[..., Awaitable[Any]]]:
        """Decorator to register a tool."""

        def decorator(
            func: Callable[..., Awaitable[Any]],
        ) -> Callable[..., Awaitable[Any]]:
            schema = input_schema or {"type": "object", "properties": {}}
            self._tools[name] = Tool(
                name=name,
                description=description,
                inputSchema=schema,
                handler=func,
            )
            return func

        return decorator

    def resource(
        self,
        uri: str,
        name: str,
        description: str | None = None,
        mime_type: str | None = None,
    ) -> Callable[
        [Callable[[str], Awaitable[dict[str, Any]]]],
        Callable[[str], Awaitable[dict[str, Any]]],
    ]:
        """Decorator to register a resource."""

        def decorator(
            func: Callable[[str], Awaitable[dict[str, Any]]],
        ) -> Callable[[str], Awaitable[dict[str, Any]]]:
            self._resources[uri] = Resource(
                uri=uri,
                name=name,
                description=description,
                mimeType=mime_type,
            )
            self._resource_handlers[uri] = func
            return func

        return decorator

    def prompt(
        self,
        name: str,
        description: str | None = None,
        arguments: list[dict[str, Any]] | None = None,
    ) -> Callable[
        [Callable[[dict[str, str]], Awaitable[list[dict[str, str]]]]],
        Callable[[dict[str, str]], Awaitable[list[dict[str, str]]]]
    ]:
        """Decorator to register a prompt."""

        def decorator(
            func: Callable[[dict[str, str]], Awaitable[list[dict[str, str]]]],
        ) -> Callable[[dict[str, str]], Awaitable[list[dict[str, str]]]]:
            self._prompts[name] = Prompt(
                name=name,
                description=description,
                arguments=arguments,
            )
            self._prompt_handlers[name] = func
            return func

        return decorator

    async def handle_request(self, request: JsonRpcRequest) -> JsonRpcResponse:
        """Handle a JSON-RPC request."""
        context = ToolContext(
            request_id=request.id,
            server_info=self.server_info,
        )

        try:
            result = await self._route_method(
                request.method, request.params or {}, context
            )
            return JsonRpcResponse(id=request.id, result=result)
        except McpError as e:
            return JsonRpcResponse(
                id=request.id,
                error=JsonRpcError(code=e.code, message=str(e), data=e.data),
            )
        except Exception as e:
            return JsonRpcResponse(
                id=request.id,
                error=JsonRpcError(code=-32603, message=str(e)),
            )

    async def handle_http(
        self, method: str, body: str | None
    ) -> tuple[int, dict[str, str], str]:
        """
        Handle an HTTP request.

        Returns: (status_code, headers, body)
        """
        cors_headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }

        if method == "OPTIONS":
            return 204, cors_headers, ""

        if method != "POST":
            return (
                405,
                {**cors_headers, "Content-Type": "application/json"},
                json.dumps({"error": "Method not allowed"}),
            )

        try:
            data = json.loads(body or "{}")
            request = JsonRpcRequest(
                jsonrpc=data.get("jsonrpc", ""),
                method=data.get("method", ""),
                id=data.get("id"),
                params=data.get("params"),
            )

            if request.jsonrpc != "2.0" or not request.method:
                return (
                    400,
                    {**cors_headers, "Content-Type": "application/json"},
                    json.dumps(
                        {
                            "jsonrpc": "2.0",
                            "id": request.id,
                            "error": {"code": -32600, "message": "Invalid Request"},
                        }
                    ),
                )

            response = await self.handle_request(request)
            return (
                200,
                {**cors_headers, "Content-Type": "application/json"},
                json.dumps(self._response_to_dict(response)),
            )

        except json.JSONDecodeError:
            return (
                400,
                {**cors_headers, "Content-Type": "application/json"},
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {"code": -32700, "message": "Parse error"},
                    }
                ),
            )

    def _response_to_dict(self, response: JsonRpcResponse) -> dict[str, Any]:
        """Convert a response to a JSON-serializable dict."""
        result: dict[str, Any] = {"jsonrpc": response.jsonrpc, "id": response.id}
        if response.error:
            result["error"] = {
                "code": response.error.code,
                "message": response.error.message,
            }
            if response.error.data is not None:
                result["error"]["data"] = response.error.data
        else:
            result["result"] = response.result
        return result

    async def _route_method(
        self, method: str, params: dict[str, Any], context: ToolContext
    ) -> Any:
        """Route a method to its handler."""
        handlers = {
            "initialize": self._handle_initialize,
            "tools/list": self._handle_tools_list,
            "tools/call": lambda p, c: self._handle_tools_call(p, c),
            "resources/list": self._handle_resources_list,
            "resources/read": self._handle_resources_read,
            "prompts/list": self._handle_prompts_list,
            "prompts/get": self._handle_prompts_get,
            "ping": self._handle_ping,
        }

        handler = handlers.get(method)
        if not handler:
            raise McpError(-32601, f"Method not found: {method}")

        return await handler(params, context)

    async def _handle_initialize(
        self, params: dict[str, Any], context: ToolContext
    ) -> dict[str, Any]:
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": asdict(self.capabilities),
            "serverInfo": asdict(self.server_info),
        }

    async def _handle_tools_list(
        self, params: dict[str, Any], context: ToolContext
    ) -> dict[str, Any]:
        tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.inputSchema,
            }
            for tool in self._tools.values()
        ]
        return {"tools": tools}

    async def _handle_tools_call(
        self, params: dict[str, Any], context: ToolContext
    ) -> dict[str, Any]:
        name = params.get("name", "")
        arguments = params.get("arguments", {})

        tool = self._tools.get(name)
        if not tool:
            raise McpError(-32602, f"Unknown tool: {name}")

        try:
            result = await tool.handler(arguments, context)

            if isinstance(result, str):
                return {"content": [{"type": "text", "text": result}]}

            if isinstance(result, dict) and "content" in result:
                return result

            return {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}

        except Exception as e:
            return {
                "content": [{"type": "text", "text": f"Error: {e}"}],
                "isError": True,
            }

    async def _handle_resources_list(
        self, params: dict[str, Any], context: ToolContext
    ) -> dict[str, Any]:
        resources = [
            {
                "uri": r.uri,
                "name": r.name,
                "description": r.description,
                "mimeType": r.mimeType,
            }
            for r in self._resources.values()
        ]
        return {"resources": resources}

    async def _handle_resources_read(
        self, params: dict[str, Any], context: ToolContext
    ) -> dict[str, Any]:
        uri = params.get("uri", "")
        handler = self._resource_handlers.get(uri)

        if not handler:
            raise McpError(-32602, f"Unknown resource: {uri}")

        content = await handler(uri)
        return {"contents": [{"uri": uri, **content}]}

    async def _handle_prompts_list(
        self, params: dict[str, Any], context: ToolContext
    ) -> dict[str, Any]:
        prompts = [
            {
                "name": p.name,
                "description": p.description,
                "arguments": p.arguments,
            }
            for p in self._prompts.values()
        ]
        return {"prompts": prompts}

    async def _handle_prompts_get(
        self, params: dict[str, Any], context: ToolContext
    ) -> dict[str, Any]:
        name = params.get("name", "")
        arguments = params.get("arguments", {})

        prompt = self._prompts.get(name)
        handler = self._prompt_handlers.get(name)

        if not prompt or not handler:
            raise McpError(-32602, f"Unknown prompt: {name}")

        messages = await handler(arguments)
        return {"description": prompt.description, "messages": messages}

    async def _handle_ping(
        self, params: dict[str, Any], context: ToolContext
    ) -> dict[str, Any]:
        return {}


def create_server(name: str, version: str) -> McpServer:
    """Create a new MCP server instance."""
    return McpServer(name=name, version=version)
