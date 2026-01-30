"""Type definitions for the MCP server."""

from dataclasses import dataclass, field
from typing import Any, Callable, Awaitable, TypeVar, Generic
from enum import Enum


class ContentType(Enum):
    TEXT = "text"
    IMAGE = "image"
    RESOURCE = "resource"


@dataclass
class TextContent:
    type: str = "text"
    text: str = ""


@dataclass
class ImageContent:
    type: str = "image"
    data: str = ""
    mimeType: str = "image/png"


@dataclass
class ToolResult:
    content: list[TextContent | ImageContent]
    isError: bool = False


@dataclass
class Tool:
    name: str
    description: str
    inputSchema: dict[str, Any]
    handler: Callable[..., Awaitable[Any]]


@dataclass
class Resource:
    uri: str
    name: str
    description: str | None = None
    mimeType: str | None = None


@dataclass
class Prompt:
    name: str
    description: str | None = None
    arguments: list[dict[str, Any]] | None = None


@dataclass
class ServerInfo:
    name: str
    version: str


@dataclass
class ServerCapabilities:
    tools: dict[str, bool] = field(default_factory=lambda: {"listChanged": False})
    resources: dict[str, bool] = field(
        default_factory=lambda: {"subscribe": False, "listChanged": False}
    )
    prompts: dict[str, bool] = field(default_factory=lambda: {"listChanged": False})


@dataclass
class JsonRpcRequest:
    jsonrpc: str
    method: str
    id: str | int | None = None
    params: dict[str, Any] | None = None


@dataclass
class JsonRpcError:
    code: int
    message: str
    data: Any = None


@dataclass
class JsonRpcResponse:
    jsonrpc: str = "2.0"
    id: str | int | None = None
    result: Any = None
    error: JsonRpcError | None = None


@dataclass
class ToolContext:
    request_id: str | int | None
    server_info: ServerInfo
