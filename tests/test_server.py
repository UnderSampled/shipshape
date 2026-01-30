"""Tests for the MCP server."""

import pytest

from mcp_server import ToolContext, create_server


@pytest.fixture
def server():
    """Create a test server."""
    return create_server(name="test-server", version="1.0.0")


class TestServerCreation:
    def test_creates_server_with_name_and_version(self, server):
        assert server.name == "test-server"
        assert server.version == "1.0.0"

    def test_server_info_property(self, server):
        info = server.server_info
        assert info.name == "test-server"
        assert info.version == "1.0.0"


class TestToolRegistration:
    @pytest.mark.asyncio
    async def test_registers_tool(self, server):
        @server.tool(
            name="test_tool",
            description="A test tool",
            input_schema={"type": "object", "properties": {}},
        )
        async def test_tool(args: dict, context: ToolContext) -> str:
            return "test result"

        assert "test_tool" in server._tools
        assert server._tools["test_tool"].description == "A test tool"


class TestJsonRpcHandling:
    @pytest.mark.asyncio
    async def test_handles_initialize(self, server):
        from mcp_server.types import JsonRpcRequest

        request = JsonRpcRequest(jsonrpc="2.0", id=1, method="initialize", params={})
        response = await server.handle_request(request)

        assert response.id == 1
        assert response.result is not None
        assert response.result["serverInfo"]["name"] == "test-server"

    @pytest.mark.asyncio
    async def test_handles_tools_list(self, server):
        from mcp_server.types import JsonRpcRequest

        @server.tool(name="greet", description="Greet someone")
        async def greet(args: dict, context: ToolContext) -> str:
            return f"Hello, {args.get('name', 'World')}!"

        request = JsonRpcRequest(jsonrpc="2.0", id=2, method="tools/list")
        response = await server.handle_request(request)

        assert len(response.result["tools"]) == 1
        assert response.result["tools"][0]["name"] == "greet"

    @pytest.mark.asyncio
    async def test_handles_tools_call(self, server):
        from mcp_server.types import JsonRpcRequest

        @server.tool(name="echo", description="Echo input")
        async def echo(args: dict, context: ToolContext) -> str:
            return args.get("message", "")

        request = JsonRpcRequest(
            jsonrpc="2.0",
            id=3,
            method="tools/call",
            params={"name": "echo", "arguments": {"message": "hello"}},
        )
        response = await server.handle_request(request)

        assert response.result["content"][0]["text"] == "hello"

    @pytest.mark.asyncio
    async def test_handles_unknown_method(self, server):
        from mcp_server.types import JsonRpcRequest

        request = JsonRpcRequest(jsonrpc="2.0", id=4, method="unknown/method")
        response = await server.handle_request(request)

        assert response.error is not None
        assert response.error.code == -32601

    @pytest.mark.asyncio
    async def test_handles_unknown_tool(self, server):
        from mcp_server.types import JsonRpcRequest

        request = JsonRpcRequest(
            jsonrpc="2.0",
            id=5,
            method="tools/call",
            params={"name": "nonexistent", "arguments": {}},
        )
        response = await server.handle_request(request)

        assert response.error is not None
        assert response.error.code == -32602

    @pytest.mark.asyncio
    async def test_handles_ping(self, server):
        from mcp_server.types import JsonRpcRequest

        request = JsonRpcRequest(jsonrpc="2.0", id=6, method="ping")
        response = await server.handle_request(request)

        assert response.result == {}


class TestHttpHandling:
    @pytest.mark.asyncio
    async def test_handles_options_request(self, server):
        status, headers, body = await server.handle_http("OPTIONS", None)

        assert status == 204
        assert headers["Access-Control-Allow-Origin"] == "*"

    @pytest.mark.asyncio
    async def test_rejects_get_request(self, server):
        status, headers, body = await server.handle_http("GET", None)

        assert status == 405

    @pytest.mark.asyncio
    async def test_handles_valid_post(self, server):
        import json

        payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "ping"})
        status, headers, body = await server.handle_http("POST", payload)

        assert status == 200
        result = json.loads(body)
        assert result["result"] == {}

    @pytest.mark.asyncio
    async def test_handles_invalid_json(self, server):
        import json

        status, headers, body = await server.handle_http("POST", "invalid json")

        assert status == 400
        result = json.loads(body)
        assert result["error"]["code"] == -32700


class TestResourceHandling:
    @pytest.mark.asyncio
    async def test_registers_and_lists_resources(self, server):
        from mcp_server.types import JsonRpcRequest

        @server.resource(uri="test://resource", name="Test Resource")
        async def test_resource(uri: str) -> dict:
            return {"text": "test content"}

        request = JsonRpcRequest(jsonrpc="2.0", id=1, method="resources/list")
        response = await server.handle_request(request)

        assert len(response.result["resources"]) == 1
        assert response.result["resources"][0]["uri"] == "test://resource"

    @pytest.mark.asyncio
    async def test_reads_resource(self, server):
        from mcp_server.types import JsonRpcRequest

        @server.resource(uri="test://resource", name="Test Resource")
        async def test_resource(uri: str) -> dict:
            return {"text": "test content"}

        request = JsonRpcRequest(
            jsonrpc="2.0",
            id=1,
            method="resources/read",
            params={"uri": "test://resource"},
        )
        response = await server.handle_request(request)

        assert response.result["contents"][0]["text"] == "test content"


class TestPromptHandling:
    @pytest.mark.asyncio
    async def test_registers_and_lists_prompts(self, server):
        from mcp_server.types import JsonRpcRequest

        @server.prompt(name="test_prompt", description="A test prompt")
        async def test_prompt(args: dict) -> list[dict]:
            return [{"role": "user", "content": "test"}]

        request = JsonRpcRequest(jsonrpc="2.0", id=1, method="prompts/list")
        response = await server.handle_request(request)

        assert len(response.result["prompts"]) == 1
        assert response.result["prompts"][0]["name"] == "test_prompt"

    @pytest.mark.asyncio
    async def test_gets_prompt(self, server):
        from mcp_server.types import JsonRpcRequest

        @server.prompt(name="greet_prompt", description="Greeting prompt")
        async def greet_prompt(args: dict) -> list[dict]:
            return [{"role": "user", "content": f"Hello {args.get('name', 'there')}"}]

        request = JsonRpcRequest(
            jsonrpc="2.0",
            id=1,
            method="prompts/get",
            params={"name": "greet_prompt", "arguments": {"name": "World"}},
        )
        response = await server.handle_request(request)

        assert response.result["messages"][0]["content"] == "Hello World"
