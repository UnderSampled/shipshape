"""Sensor MCP tools for reading ship state."""

import json
from typing import TYPE_CHECKING

from mcp.server import Server
from mcp.types import Tool, TextContent

if TYPE_CHECKING:
    from ..state.game import GameState


def register_sensor_tools(server: Server, state: "GameState"):
    """Register sensor tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
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
                        "room_id": {
                            "type": "string",
                            "description": "The ID of the room to scan"
                        }
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
                        "robot_id": {
                            "type": "string",
                            "description": "The ID of the robot to scan"
                        }
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
                        "system_id": {
                            "type": "string",
                            "description": "The ID of the system to scan"
                        }
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
                        "count": {
                            "type": "integer",
                            "description": "Number of recent events to retrieve (default: 20)"
                        }
                    }
                }
            ),
            Tool(
                name="list_rooms",
                description="Get a list of all rooms on the ship.",
                inputSchema={"type": "object", "properties": {}}
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "scan_ship":
            return await _scan_ship(state)
        elif name == "scan_room":
            return await _scan_room(state, arguments.get("room_id"))
        elif name == "scan_robots":
            return await _scan_robots(state)
        elif name == "scan_robot":
            return await _scan_robot(state, arguments.get("robot_id"))
        elif name == "scan_cat":
            return await _scan_cat(state)
        elif name == "scan_system":
            return await _scan_system(state, arguments.get("system_id"))
        elif name == "scan_exterior":
            return await _scan_exterior(state)
        elif name == "scan_journey":
            return await _scan_journey(state)
        elif name == "read_log":
            return await _read_log(state, arguments.get("count", 20))
        elif name == "list_rooms":
            return await _list_rooms(state)

        return None


async def _scan_ship(state: "GameState"):
    """Scan the entire ship."""
    with state.lock():
        systems_data = []
        for sys in state.systems.values():
            systems_data.append({
                "id": sys.id,
                "name": sys.name,
                "status": sys.status_summary,
                "online": sys.online,
                "health": f"{sys.health:.1f}%",
                "efficiency": f"{sys.efficiency * 100:.1f}%",
                "power": f"{sys.power_level:.1f}",
                "temperature": f"{sys.temperature:.1f}°C",
            })

        result = {
            "ship_name": state.ship_name,
            "hull_integrity": f"{state.hull_integrity:.1f}%",
            "phase": state.phase.value,
            "total_power": f"{state.total_power:.1f}",
            "power_allocated": f"{state.power_allocated:.1f}",
            "power_available": f"{state.total_power - state.power_allocated:.1f}",
            "systems": systems_data,
            "robot_count": len(state.robots),
            "active_robots": len([r for r in state.robots.values() if r.is_functional]),
        }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _scan_room(state: "GameState", room_id: str):
    """Scan a specific room."""
    with state.lock():
        room_data = state.graph.get_entity(room_id)
        if not room_data:
            return [TextContent(type="text", text=f"Room '{room_id}' not found.")]

        # Get contents
        contents = state.graph.get_contents(room_id)
        items = []
        robots_in_room = []
        systems_in_room = []

        for entity_id in contents:
            entity = state.graph.get_entity(entity_id)
            if entity:
                etype = entity.get("entity_type")
                if etype == "robot":
                    robot = state.robots.get(entity_id)
                    if robot:
                        robots_in_room.append({
                            "id": robot.id,
                            "designation": robot.designation,
                            "status": robot.status_summary
                        })
                elif etype == "system":
                    sys = state.systems.get(entity_id)
                    if sys:
                        systems_in_room.append({
                            "id": sys.id,
                            "name": sys.name,
                            "status": sys.status_summary
                        })
                elif etype == "item":
                    items.append({
                        "id": entity_id,
                        "name": entity.get("name", entity_id),
                        "description": entity.get("description", "")
                    })
                elif etype == "cat" and state.cat.discovered:
                    items.append({
                        "id": "cat",
                        "name": state.cat.name,
                        "description": f"The ship's cat. Status: {state.cat.status.value}"
                    })

        # Get connections
        connections = state.graph.get_connected_rooms(room_id)

        result = {
            "id": room_id,
            "name": room_data.get("name", room_id),
            "description": room_data.get("description", ""),
            "is_human_area": room_data.get("is_human_area", False),
            "temperature": f"{room_data.get('temperature', 20):.1f}°C",
            "lighting": f"{room_data.get('lighting', 0.5) * 100:.0f}%",
            "hazards": room_data.get("hazards", []),
            "robots": robots_in_room,
            "systems": systems_in_room,
            "items": items,
            "connections": [
                {"room": room, "direction": direction}
                for room, direction in connections
            ]
        }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _scan_robots(state: "GameState"):
    """Scan all robots."""
    with state.lock():
        robots = []
        for robot in state.robots.values():
            robots.append({
                "id": robot.id,
                "designation": robot.designation,
                "role": robot.role.value,
                "location": robot.location,
                "status": robot.status_summary,
                "power": f"{robot.power_level:.1f}%",
                "maintenance": f"{robot.maintenance:.1f}%",
                "current_task": robot.current_task.task_type.value if robot.current_task else None,
                "queued_tasks": len(robot.task_queue),
                "urgent_need": robot.most_urgent_need,
            })

    return [TextContent(type="text", text=json.dumps({"robots": robots}, indent=2))]


async def _scan_robot(state: "GameState", robot_id: str):
    """Scan a specific robot."""
    with state.lock():
        robot = state.robots.get(robot_id)
        if not robot:
            return [TextContent(type="text", text=f"Robot '{robot_id}' not found.")]

        result = {
            "id": robot.id,
            "designation": robot.designation,
            "role": robot.role.value,
            "location": robot.location,
            "status": robot.status.value,
            "status_summary": robot.status_summary,
            "needs": {
                "power_level": f"{robot.power_level:.1f}%",
                "thermal_level": f"{robot.thermal_level:.1f}",
                "maintenance": f"{robot.maintenance:.1f}%",
                "memory_integrity": f"{robot.memory_integrity:.1f}%",
            },
            "needs_charge": robot.needs_charge,
            "needs_repair": robot.needs_repair,
            "needs_cooling": robot.needs_cooling,
            "needs_sync": robot.needs_sync,
            "most_urgent_need": robot.most_urgent_need,
            "skills": {
                "repair": f"{robot.repair_skill:.1f}",
                "combat": f"{robot.combat_skill:.1f}",
                "efficiency": f"{robot.efficiency:.1f}",
            },
            "traits": [t.value for t in robot.traits],
            "current_task": {
                "type": robot.current_task.task_type.value,
                "target": robot.current_task.target,
                "progress": f"{robot.current_task.progress:.1f}%",
                "priority": robot.current_task.priority,
            } if robot.current_task else None,
            "task_queue": [
                {"type": t.task_type.value, "target": t.target, "priority": t.priority}
                for t in robot.task_queue
            ],
            "relationships": robot.relationships,
        }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _scan_cat(state: "GameState"):
    """Scan the cat."""
    with state.lock():
        if not state.cat.discovered:
            # Check if internal sensors are online
            sensors = state.systems.get("sensors_internal")
            if sensors and sensors.online:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "not_found",
                        "hint": "Sensors detect faint life signs somewhere aboard. Location unclear."
                    }, indent=2)
                )]
            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "sensors_offline",
                    "message": "Internal sensors offline. Cannot scan for life forms."
                }, indent=2)
            )]

        cat = state.cat
        result = {
            "name": cat.name,
            "location": cat.location,
            "status": cat.status.value,
            "needs": {
                "hunger": f"{cat.hunger:.1f}%",
                "thirst": f"{cat.thirst:.1f}%",
                "warmth": f"{cat.warmth:.1f}%",
            },
            "health": f"{cat.health:.1f}%",
            "happiness": f"{cat.happiness:.1f}%",
            "warnings": []
        }

        # Add warnings
        if cat.hunger > 70:
            result["warnings"].append("Cat is hungry")
        if cat.thirst > 70:
            result["warnings"].append("Cat is thirsty")
        if cat.warmth < 40:
            result["warnings"].append("Cat is cold")
        if cat.health < 50:
            result["warnings"].append("Cat health is concerning")

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _scan_system(state: "GameState", system_id: str):
    """Scan a specific system."""
    with state.lock():
        system = state.systems.get(system_id)
        if not system:
            return [TextContent(type="text", text=f"System '{system_id}' not found.")]

        result = {
            "id": system.id,
            "name": system.name,
            "description": system.description,
            "type": system.system_type.value,
            "location": system.location,
            "status": system.status_summary,
            "online": system.online,
            "health": f"{system.health:.1f}%",
            "power_level": f"{system.power_level:.1f}",
            "power_draw": f"{system.actual_power_draw:.1f}",
            "efficiency": f"{system.efficiency * 100:.1f}%",
            "temperature": f"{system.temperature:.1f}°C",
            "on_fire": system.on_fire,
            "breached": system.breached,
            "required_phase": system.required_phase,
            "manned_by": system.manned_by,
            "max_operators": system.max_operators,
        }

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _scan_exterior(state: "GameState"):
    """Scan the exterior environment."""
    with state.lock():
        # Check if external sensors are online
        ext_sensors = state.systems.get("sensors_external")
        sensor_quality = "full"
        if not ext_sensors or not ext_sensors.online:
            # Fall back to internal sensors (limited)
            int_sensors = state.systems.get("sensors_internal")
            if not int_sensors or not int_sensors.online:
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "status": "sensors_offline",
                        "message": "No sensors available. Cannot scan exterior."
                    }, indent=2)
                )]
            sensor_quality = "limited"

        current_node = state.sector_map.get(state.current_node, {})

        result = {
            "sensor_quality": sensor_quality,
            "current_location": {
                "id": state.current_node,
                "name": current_node.get("name", state.current_node),
                "type": current_node.get("node_type", "unknown"),
                "description": current_node.get("description", ""),
            },
            "sector": state.current_sector,
            "threat_level": f"{state.threat_level:.1f}",
        }

        # Add nearby objects if sensors are good
        if sensor_quality == "full":
            available_jumps = []
            connections = current_node.get("connections", [])
            for conn_id in connections:
                conn_node = state.sector_map.get(conn_id, {})
                available_jumps.append({
                    "id": conn_id,
                    "name": conn_node.get("name", conn_id),
                    "type": conn_node.get("node_type", "unknown"),
                    "visited": conn_node.get("visited", False),
                })
            result["available_jumps"] = available_jumps

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _scan_journey(state: "GameState"):
    """Scan journey progress."""
    with state.lock():
        ftl = state.systems.get("engines_ftl")
        ftl_status = "offline"
        if ftl and ftl.online:
            ftl_status = "ready" if state.jump_charge >= 100 else "charging"

        result = {
            "current_sector": state.current_sector,
            "total_sectors": 8,
            "destination": state.destination,
            "current_node": state.current_node,
            "threat_level": f"{state.threat_level:.1f}",
            "ftl_status": ftl_status,
            "jump_charge": f"{state.jump_charge:.1f}%",
            "jump_cooldown": f"{state.jump_cooldown:.1f}s",
            "is_jumping": state.jumping,
            "jump_target": state.jump_target,
        }

        # Add sector map if navigation is online
        nav = state.systems.get("navigation")
        if nav and nav.online:
            map_data = []
            for node_id, node in state.sector_map.items():
                if isinstance(node, dict):
                    map_data.append({
                        "id": node_id,
                        "name": node.get("name", node_id),
                        "type": node.get("node_type", "unknown"),
                        "visited": node.get("visited", False),
                        "connections": node.get("connections", []),
                    })
            result["sector_map"] = map_data

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _read_log(state: "GameState", count: int):
    """Read recent events."""
    with state.lock():
        events = state.get_recent_events(count)
        log_entries = [
            {
                "tick": e.tick,
                "type": e.event_type,
                "severity": e.severity,
                "message": e.message,
            }
            for e in events
        ]

    return [TextContent(type="text", text=json.dumps({"events": log_entries}, indent=2))]


async def _list_rooms(state: "GameState"):
    """List all rooms on the ship."""
    from ..ship.layout import SHIP_ROOMS

    rooms = []
    for room_id, (name, description, is_human_area) in SHIP_ROOMS.items():
        rooms.append({
            "id": room_id,
            "name": name,
            "is_human_area": is_human_area,
        })

    return [TextContent(type="text", text=json.dumps({"rooms": rooms}, indent=2))]
