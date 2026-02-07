"""MCP server entry point for the Shipshape spaceship simulation."""

import asyncio
import logging
from contextlib import asynccontextmanager

from mcp.server import Server
from mcp.server.stdio import stdio_server

from .state.game import GameState
from .simulation.engine import SimulationEngine
from .tools.game import register_game_tools
from .tools.sensors import register_sensor_tools
from .tools.actuators import register_actuator_tools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("shipshape")


class ShipshapeServer:
    """Main MCP server for the spaceship simulation."""

    def __init__(self):
        self.server = Server("shipshape")
        self.state = GameState()
        self.engine = SimulationEngine(self.state, tick_rate=1.0)

        # Register all tools
        self._register_tools()

    def _register_tools(self):
        """Register all MCP tools with the server."""
        # We need to combine the tool handlers since MCP only allows one handler per decorator
        # Create combined handlers

        # Store individual tool handlers
        game_tools = []
        sensor_tools = []
        actuator_tools = []

        # Collect tool definitions
        @self.server.list_tools()
        async def list_all_tools():
            """List all available tools."""
            tools = []

            # Game management tools
            from mcp.types import Tool
            tools.extend([
                Tool(
                    name="start_game",
                    description="Start a new game. Returns Eli's instructions for the AI and the initial ship state.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "ship_name": {
                                "type": "string",
                                "description": "Optional custom name for the ship (default: ISV Perseverance)"
                            }
                        }
                    }
                ),
                Tool(
                    name="resume_game",
                    description="Resume a saved game. Returns Eli's instructions and current ship state.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "save_slot": {
                                "type": "string",
                                "description": "Save slot to load (default: autosave)"
                            }
                        }
                    }
                ),
                Tool(
                    name="save_game",
                    description="Save the current game state.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "save_slot": {
                                "type": "string",
                                "description": "Save slot name (default: autosave)"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_game_status",
                    description="Get the current game status (running, paused, etc.)",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="pause_game",
                    description="Pause the simulation.",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="resume_simulation",
                    description="Resume a paused simulation.",
                    inputSchema={"type": "object", "properties": {}}
                ),
            ])

            # Sensor tools
            tools.extend([
                Tool(
                    name="scan_ship",
                    description="Get an overview of all ship systems, power, and hull integrity.",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="scan_room",
                    description="Get the contents and state of a specific room.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "room_id": {"type": "string", "description": "The ID of the room to scan"}
                        },
                        "required": ["room_id"]
                    }
                ),
                Tool(
                    name="scan_robots",
                    description="Get status of all robots (location, task, needs).",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="scan_robot",
                    description="Get detailed status of one robot.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "robot_id": {"type": "string", "description": "The ID of the robot to scan"}
                        },
                        "required": ["robot_id"]
                    }
                ),
                Tool(
                    name="scan_cat",
                    description="Get the cat's location, needs, and status (only available after cat is discovered).",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="scan_system",
                    description="Get detailed status of one ship system.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "system_id": {"type": "string", "description": "The ID of the system to scan"}
                        },
                        "required": ["system_id"]
                    }
                ),
                Tool(
                    name="scan_exterior",
                    description="Get information about what's outside the ship (current location, nearby objects).",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="scan_journey",
                    description="Get sector progress, jump status, and map information.",
                    inputSchema={"type": "object", "properties": {}}
                ),
                Tool(
                    name="read_log",
                    description="Get recent events and alerts.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "count": {"type": "integer", "description": "Number of recent events (default: 20)"}
                        }
                    }
                ),
                Tool(
                    name="list_rooms",
                    description="Get a list of all rooms on the ship.",
                    inputSchema={"type": "object", "properties": {}}
                ),
            ])

            # Actuator tools
            tools.extend([
                Tool(
                    name="set_power",
                    description="Allocate power to a system (0-100). System must be online.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "system_id": {"type": "string", "description": "The ID of the system"},
                            "power_level": {"type": "number", "description": "Power level to set (0-100)"}
                        },
                        "required": ["system_id", "power_level"]
                    }
                ),
                Tool(
                    name="bring_online",
                    description="Attempt to bring an offline system online.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "system_id": {"type": "string", "description": "The ID of the system to bring online"}
                        },
                        "required": ["system_id"]
                    }
                ),
                Tool(
                    name="take_offline",
                    description="Take a system offline.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "system_id": {"type": "string", "description": "The ID of the system to take offline"}
                        },
                        "required": ["system_id"]
                    }
                ),
                Tool(
                    name="order_robot",
                    description="Assign a task to a robot.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "robot_id": {"type": "string", "description": "The ID of the robot"},
                            "task_type": {
                                "type": "string",
                                "enum": ["operate_system", "repair_system", "repair_robot", "move_to", "charge", "fight_fire", "feed_cat", "water_cat", "patrol"],
                                "description": "Type of task to assign"
                            },
                            "target": {"type": "string", "description": "Target for the task"},
                            "priority": {"type": "integer", "description": "Task priority (1=highest, 10=lowest)"},
                            "immediate": {"type": "boolean", "description": "Interrupt current task if true"}
                        },
                        "required": ["robot_id", "task_type"]
                    }
                ),
                Tool(
                    name="cancel_task",
                    description="Cancel a robot's current task.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "robot_id": {"type": "string", "description": "The ID of the robot"}
                        },
                        "required": ["robot_id"]
                    }
                ),
                Tool(
                    name="set_door",
                    description="Open, close, or lock a door between two rooms.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "room_a": {"type": "string", "description": "First room ID"},
                            "room_b": {"type": "string", "description": "Second room ID"},
                            "state": {"type": "string", "enum": ["open", "closed", "locked"], "description": "Door state"}
                        },
                        "required": ["room_a", "room_b", "state"]
                    }
                ),
                Tool(
                    name="initiate_jump",
                    description="Begin FTL jump to a connected sector node.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "target_node": {"type": "string", "description": "ID of the node to jump to"}
                        },
                        "required": ["target_node"]
                    }
                ),
                Tool(
                    name="activate_shields",
                    description="Configure shield settings.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "power_level": {"type": "number", "description": "Shield power level (0-100)"}
                        },
                        "required": ["power_level"]
                    }
                ),
                Tool(
                    name="target_weapons",
                    description="Aim weapons at a target.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "target": {"type": "string", "description": "Target to aim at"},
                            "weapon_system": {"type": "string", "enum": ["weapons_laser", "weapons_missile"]}
                        },
                        "required": ["target", "weapon_system"]
                    }
                ),
                Tool(
                    name="fire_weapons",
                    description="Fire the targeted weapon system.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "weapon_system": {"type": "string", "enum": ["weapons_laser", "weapons_missile"]}
                        },
                        "required": ["weapon_system"]
                    }
                ),
                Tool(
                    name="ship_broadcast",
                    description="Broadcast a message to all robots.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "message": {"type": "string", "description": "Message to broadcast"}
                        },
                        "required": ["message"]
                    }
                ),
                Tool(
                    name="set_room_temperature",
                    description="Adjust temperature in a room (requires life support).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "room_id": {"type": "string", "description": "Room to adjust"},
                            "temperature": {"type": "number", "description": "Target temperature in Celsius"}
                        },
                        "required": ["room_id", "temperature"]
                    }
                ),
            ])

            return tools

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            """Route tool calls to appropriate handlers."""
            import json
            from mcp.types import TextContent

            # Game management tools
            if name == "start_game":
                from .tools.game import _start_game
                return await _start_game(self.state, self.engine, arguments)
            elif name == "resume_game":
                from .tools.game import _resume_game
                return await _resume_game(self.state, self.engine, arguments)
            elif name == "save_game":
                from .tools.game import _save_game
                return await _save_game(self.state, arguments)
            elif name == "get_game_status":
                from .tools.game import _get_game_status
                return await _get_game_status(self.state, self.engine)
            elif name == "pause_game":
                self.engine.pause()
                return [TextContent(type="text", text="Simulation paused.")]
            elif name == "resume_simulation":
                self.engine.resume()
                return [TextContent(type="text", text="Simulation resumed.")]

            # Sensor tools
            elif name == "scan_ship":
                from .tools.sensors import _scan_ship
                return await _scan_ship(self.state)
            elif name == "scan_room":
                from .tools.sensors import _scan_room
                return await _scan_room(self.state, arguments.get("room_id"))
            elif name == "scan_robots":
                from .tools.sensors import _scan_robots
                return await _scan_robots(self.state)
            elif name == "scan_robot":
                from .tools.sensors import _scan_robot
                return await _scan_robot(self.state, arguments.get("robot_id"))
            elif name == "scan_cat":
                from .tools.sensors import _scan_cat
                return await _scan_cat(self.state)
            elif name == "scan_system":
                from .tools.sensors import _scan_system
                return await _scan_system(self.state, arguments.get("system_id"))
            elif name == "scan_exterior":
                from .tools.sensors import _scan_exterior
                return await _scan_exterior(self.state)
            elif name == "scan_journey":
                from .tools.sensors import _scan_journey
                return await _scan_journey(self.state)
            elif name == "read_log":
                from .tools.sensors import _read_log
                return await _read_log(self.state, arguments.get("count", 20))
            elif name == "list_rooms":
                from .tools.sensors import _list_rooms
                return await _list_rooms(self.state)

            # Actuator tools
            elif name == "set_power":
                from .tools.actuators import _set_power
                return await _set_power(self.state, arguments)
            elif name == "bring_online":
                from .tools.actuators import _bring_online
                return await _bring_online(self.state, arguments)
            elif name == "take_offline":
                from .tools.actuators import _take_offline
                return await _take_offline(self.state, arguments)
            elif name == "order_robot":
                from .tools.actuators import _order_robot
                return await _order_robot(self.state, arguments)
            elif name == "cancel_task":
                from .tools.actuators import _cancel_task
                return await _cancel_task(self.state, arguments)
            elif name == "set_door":
                from .tools.actuators import _set_door
                return await _set_door(self.state, arguments)
            elif name == "initiate_jump":
                from .tools.actuators import _initiate_jump
                return await _initiate_jump(self.state, self.engine, arguments)
            elif name == "activate_shields":
                from .tools.actuators import _activate_shields
                return await _activate_shields(self.state, arguments)
            elif name == "target_weapons":
                from .tools.actuators import _target_weapons
                return await _target_weapons(self.state, arguments)
            elif name == "fire_weapons":
                from .tools.actuators import _fire_weapons
                return await _fire_weapons(self.state, arguments)
            elif name == "ship_broadcast":
                from .tools.actuators import _ship_broadcast
                return await _ship_broadcast(self.state, arguments)
            elif name == "set_room_temperature":
                from .tools.actuators import _set_room_temperature
                return await _set_room_temperature(self.state, arguments)

            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]

    async def run(self):
        """Run the MCP server."""
        logger.info("Starting Shipshape MCP server...")

        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )

    def shutdown(self):
        """Shutdown the server and simulation."""
        logger.info("Shutting down...")
        self.engine.stop()


def main():
    """Main entry point."""
    server = ShipshapeServer()
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()
