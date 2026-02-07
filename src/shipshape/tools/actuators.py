"""Actuator MCP tools for controlling the ship."""

import json
from typing import TYPE_CHECKING

from mcp.server import Server
from mcp.types import Tool, TextContent

if TYPE_CHECKING:
    from ..state.game import GameState
    from ..simulation.engine import SimulationEngine


def register_actuator_tools(server: Server, state: "GameState", engine: "SimulationEngine"):
    """Register actuator tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="set_power",
                description="Allocate power to a system (0-100). System must be online.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "system_id": {
                            "type": "string",
                            "description": "The ID of the system"
                        },
                        "power_level": {
                            "type": "number",
                            "description": "Power level to set (0-100)"
                        }
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
                        "system_id": {
                            "type": "string",
                            "description": "The ID of the system to bring online"
                        }
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
                        "system_id": {
                            "type": "string",
                            "description": "The ID of the system to take offline"
                        }
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
                        "robot_id": {
                            "type": "string",
                            "description": "The ID of the robot"
                        },
                        "task_type": {
                            "type": "string",
                            "enum": [
                                "operate_system", "repair_system", "repair_robot",
                                "move_to", "charge", "fight_fire",
                                "feed_cat", "water_cat", "patrol"
                            ],
                            "description": "Type of task to assign"
                        },
                        "target": {
                            "type": "string",
                            "description": "Target for the task (system_id, robot_id, or room_id depending on task)"
                        },
                        "priority": {
                            "type": "integer",
                            "description": "Task priority (1=highest, 10=lowest, default: 5)"
                        },
                        "immediate": {
                            "type": "boolean",
                            "description": "If true, interrupt current task (default: false)"
                        }
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
                        "robot_id": {
                            "type": "string",
                            "description": "The ID of the robot"
                        }
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
                        "room_a": {
                            "type": "string",
                            "description": "First room ID"
                        },
                        "room_b": {
                            "type": "string",
                            "description": "Second room ID"
                        },
                        "state": {
                            "type": "string",
                            "enum": ["open", "closed", "locked"],
                            "description": "Door state to set"
                        }
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
                        "target_node": {
                            "type": "string",
                            "description": "ID of the node to jump to"
                        }
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
                        "power_level": {
                            "type": "number",
                            "description": "Shield power level (0-100)"
                        }
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
                        "target": {
                            "type": "string",
                            "description": "Target to aim at"
                        },
                        "weapon_system": {
                            "type": "string",
                            "enum": ["weapons_laser", "weapons_missile"],
                            "description": "Weapon system to use"
                        }
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
                        "weapon_system": {
                            "type": "string",
                            "enum": ["weapons_laser", "weapons_missile"],
                            "description": "Weapon system to fire"
                        }
                    },
                    "required": ["weapon_system"]
                }
            ),
            Tool(
                name="ship_broadcast",
                description="Broadcast a message to all robots (affects morale/coordination).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Message to broadcast"
                        }
                    },
                    "required": ["message"]
                }
            ),
            Tool(
                name="set_room_temperature",
                description="Adjust temperature in a room (requires life support online).",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "room_id": {
                            "type": "string",
                            "description": "Room to adjust"
                        },
                        "temperature": {
                            "type": "number",
                            "description": "Target temperature in Celsius"
                        }
                    },
                    "required": ["room_id", "temperature"]
                }
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "set_power":
            return await _set_power(state, arguments)
        elif name == "bring_online":
            return await _bring_online(state, arguments)
        elif name == "take_offline":
            return await _take_offline(state, arguments)
        elif name == "order_robot":
            return await _order_robot(state, arguments)
        elif name == "cancel_task":
            return await _cancel_task(state, arguments)
        elif name == "set_door":
            return await _set_door(state, arguments)
        elif name == "initiate_jump":
            return await _initiate_jump(state, engine, arguments)
        elif name == "activate_shields":
            return await _activate_shields(state, arguments)
        elif name == "target_weapons":
            return await _target_weapons(state, arguments)
        elif name == "fire_weapons":
            return await _fire_weapons(state, arguments)
        elif name == "ship_broadcast":
            return await _ship_broadcast(state, arguments)
        elif name == "set_room_temperature":
            return await _set_room_temperature(state, arguments)

        return None


async def _set_power(state: "GameState", arguments: dict):
    """Set power level for a system."""
    system_id = arguments.get("system_id")
    power_level = arguments.get("power_level", 0)

    with state.lock():
        system = state.systems.get(system_id)
        if not system:
            return [TextContent(type="text", text=f"System '{system_id}' not found.")]

        if not system.online:
            return [TextContent(type="text", text=f"System '{system.name}' is offline. Bring it online first.")]

        # Clamp power level
        power_level = max(0, min(100, power_level))

        # Check available power
        current_power = system.power_level
        delta = power_level - current_power
        if delta > 0 and not state.can_allocate_power(delta):
            available = state.total_power - state.power_allocated + current_power
            return [TextContent(
                type="text",
                text=f"Insufficient power. Available: {available:.1f}, Requested: {power_level:.1f}"
            )]

        system.power_level = power_level
        state.log_event(
            "power_change",
            f"{system.name} power set to {power_level:.1f}",
            severity="info",
            system=system_id,
            power=power_level
        )

    return [TextContent(type="text", text=json.dumps({
        "success": True,
        "system": system.name,
        "power_level": power_level,
        "efficiency": f"{system.efficiency * 100:.1f}%"
    }, indent=2))]


async def _bring_online(state: "GameState", arguments: dict):
    """Bring a system online."""
    system_id = arguments.get("system_id")

    with state.lock():
        system = state.systems.get(system_id)
        if not system:
            return [TextContent(type="text", text=f"System '{system_id}' not found.")]

        if system.online:
            return [TextContent(type="text", text=f"System '{system.name}' is already online.")]

        # Check phase requirement
        from ..state.game import GamePhase
        phases = list(GamePhase)
        required_phase = GamePhase(system.required_phase)
        current_phase = state.phase

        if phases.index(current_phase) < phases.index(required_phase):
            return [TextContent(
                type="text",
                text=f"System '{system.name}' requires phase '{required_phase.value}'. Current phase: '{current_phase.value}'"
            )]

        # Check health
        if system.health < 10:
            return [TextContent(
                type="text",
                text=f"System '{system.name}' is too damaged to come online. Health: {system.health:.1f}%"
            )]

        # Check power availability
        min_power = 20  # Minimum power to start
        if not state.can_allocate_power(min_power):
            return [TextContent(
                type="text",
                text=f"Insufficient power to bring '{system.name}' online. Need at least {min_power}."
            )]

        system.online = True
        system.power_level = min_power
        state.log_event(
            "system_online",
            f"{system.name} brought online",
            severity="info",
            system=system_id
        )

    return [TextContent(type="text", text=json.dumps({
        "success": True,
        "system": system.name,
        "status": "online",
        "power_level": min_power
    }, indent=2))]


async def _take_offline(state: "GameState", arguments: dict):
    """Take a system offline."""
    system_id = arguments.get("system_id")

    with state.lock():
        system = state.systems.get(system_id)
        if not system:
            return [TextContent(type="text", text=f"System '{system_id}' not found.")]

        if not system.online:
            return [TextContent(type="text", text=f"System '{system.name}' is already offline.")]

        # Critical systems can't be taken offline
        critical = ["reactor", "data_core_system"]
        if system_id in critical:
            return [TextContent(
                type="text",
                text=f"System '{system.name}' is critical and cannot be taken offline."
            )]

        # Remove any robots manning the system
        system.manned_by.clear()

        system.online = False
        system.power_level = 0
        state.log_event(
            "system_offline",
            f"{system.name} taken offline",
            severity="info",
            system=system_id
        )

    return [TextContent(type="text", text=json.dumps({
        "success": True,
        "system": system.name,
        "status": "offline"
    }, indent=2))]


async def _order_robot(state: "GameState", arguments: dict):
    """Assign a task to a robot."""
    from ..simulation.robots import Task, TaskType

    robot_id = arguments.get("robot_id")
    task_type_str = arguments.get("task_type")
    target = arguments.get("target")
    priority = arguments.get("priority", 5)
    immediate = arguments.get("immediate", False)

    with state.lock():
        robot = state.robots.get(robot_id)
        if not robot:
            return [TextContent(type="text", text=f"Robot '{robot_id}' not found.")]

        if not robot.is_functional:
            return [TextContent(
                type="text",
                text=f"Robot '{robot.designation}' is not functional. Status: {robot.status_summary}"
            )]

        # Map task type string to enum
        task_type_map = {
            "operate_system": TaskType.OPERATE_SYSTEM,
            "repair_system": TaskType.REPAIR_SYSTEM,
            "repair_robot": TaskType.REPAIR_ROBOT,
            "move_to": TaskType.MOVE_TO,
            "charge": TaskType.CHARGE,
            "fight_fire": TaskType.FIGHT_FIRE,
            "feed_cat": TaskType.FEED_CAT,
            "water_cat": TaskType.WATER_CAT,
            "patrol": TaskType.PATROL,
        }

        task_type = task_type_map.get(task_type_str)
        if not task_type:
            return [TextContent(type="text", text=f"Unknown task type: {task_type_str}")]

        # Validate target based on task type
        if task_type in [TaskType.OPERATE_SYSTEM, TaskType.REPAIR_SYSTEM, TaskType.FIGHT_FIRE]:
            if target and target not in state.systems:
                return [TextContent(type="text", text=f"System '{target}' not found.")]

        elif task_type == TaskType.REPAIR_ROBOT:
            if target and target not in state.robots:
                return [TextContent(type="text", text=f"Robot '{target}' not found.")]

        elif task_type == TaskType.MOVE_TO:
            if target and not state.graph.get_entity(target):
                return [TextContent(type="text", text=f"Location '{target}' not found.")]

        # Create and assign task
        task = Task(
            task_type=task_type,
            target=target,
            priority=priority
        )

        robot.assign_task(task, immediate=immediate)
        state.log_event(
            "task_assigned",
            f"Task '{task_type.value}' assigned to {robot.designation}",
            severity="info",
            robot=robot_id,
            task=task_type.value,
            target=target
        )

    return [TextContent(type="text", text=json.dumps({
        "success": True,
        "robot": robot.designation,
        "task": task_type.value,
        "target": target,
        "priority": priority,
        "immediate": immediate
    }, indent=2))]


async def _cancel_task(state: "GameState", arguments: dict):
    """Cancel a robot's current task."""
    robot_id = arguments.get("robot_id")

    with state.lock():
        robot = state.robots.get(robot_id)
        if not robot:
            return [TextContent(type="text", text=f"Robot '{robot_id}' not found.")]

        if not robot.current_task:
            return [TextContent(type="text", text=f"Robot '{robot.designation}' has no current task.")]

        # Clean up if was operating a system
        if robot.current_task.task_type.value == "operate_system":
            system = state.systems.get(robot.current_task.target)
            if system and robot_id in system.manned_by:
                system.manned_by.remove(robot_id)

        task_type = robot.current_task.task_type.value
        robot.current_task = None
        robot.status = robot.status.__class__.IDLE

        state.log_event(
            "task_cancelled",
            f"Task cancelled for {robot.designation}",
            severity="info",
            robot=robot_id
        )

    return [TextContent(type="text", text=json.dumps({
        "success": True,
        "robot": robot.designation,
        "cancelled_task": task_type
    }, indent=2))]


async def _set_door(state: "GameState", arguments: dict):
    """Set door state between two rooms."""
    room_a = arguments.get("room_a")
    room_b = arguments.get("room_b")
    door_state = arguments.get("state")

    with state.lock():
        # Check if door control is online
        doors = state.systems.get("doors")
        if not doors or not doors.online:
            return [TextContent(
                type="text",
                text="Door control system is offline. Cannot operate doors."
            )]

        # Find the connection
        connections = state.graph.query(subject=room_a, predicate="connected_to", obj=room_b)
        if not connections:
            return [TextContent(
                type="text",
                text=f"No door found between '{room_a}' and '{room_b}'."
            )]

        # Update door state in both directions
        door_id = connections[0][3].get("door_id")

        # Update room_a -> room_b
        state.graph.remove_relation(room_a, "connected_to", room_b)
        state.graph.add_relation(
            room_a, "connected_to", room_b,
            direction=connections[0][3].get("direction"),
            door_id=door_id,
            door_state=door_state,
            door_locked=(door_state == "locked")
        )

        # Update room_b -> room_a
        reverse_conn = state.graph.query(subject=room_b, predicate="connected_to", obj=room_a)
        if reverse_conn:
            state.graph.remove_relation(room_b, "connected_to", room_a)
            state.graph.add_relation(
                room_b, "connected_to", room_a,
                direction=reverse_conn[0][3].get("direction"),
                door_id=door_id,
                door_state=door_state,
                door_locked=(door_state == "locked")
            )

        state.log_event(
            "door_change",
            f"Door {door_id} set to {door_state}",
            severity="info",
            door=door_id,
            state=door_state
        )

    return [TextContent(type="text", text=json.dumps({
        "success": True,
        "door": door_id,
        "state": door_state
    }, indent=2))]


async def _initiate_jump(state: "GameState", engine: "SimulationEngine", arguments: dict):
    """Initiate FTL jump."""
    target_node = arguments.get("target_node")

    from ..simulation.journey import JourneyManager
    journey = JourneyManager(state)

    with state.lock():
        success, message = journey.initiate_jump(target_node)

    return [TextContent(type="text", text=json.dumps({
        "success": success,
        "message": message
    }, indent=2))]


async def _activate_shields(state: "GameState", arguments: dict):
    """Configure shields."""
    power_level = arguments.get("power_level", 0)

    with state.lock():
        shields = state.systems.get("shields")
        if not shields:
            return [TextContent(type="text", text="Shield system not found.")]

        if not shields.online:
            return [TextContent(type="text", text="Shields are offline. Bring them online first.")]

        # Set power level
        power_level = max(0, min(100, power_level))

        current_power = shields.power_level
        delta = power_level - current_power
        if delta > 0 and not state.can_allocate_power(delta):
            available = state.total_power - state.power_allocated + current_power
            return [TextContent(
                type="text",
                text=f"Insufficient power. Available: {available:.1f}"
            )]

        shields.power_level = power_level
        state.log_event(
            "shields_adjusted",
            f"Shields set to {power_level:.1f}% power",
            severity="info"
        )

    return [TextContent(type="text", text=json.dumps({
        "success": True,
        "power_level": power_level,
        "efficiency": f"{shields.efficiency * 100:.1f}%"
    }, indent=2))]


async def _target_weapons(state: "GameState", arguments: dict):
    """Target weapons at something."""
    target = arguments.get("target")
    weapon_system = arguments.get("weapon_system")

    with state.lock():
        weapon = state.systems.get(weapon_system)
        if not weapon:
            return [TextContent(type="text", text=f"Weapon system '{weapon_system}' not found.")]

        if not weapon.online:
            return [TextContent(type="text", text=f"{weapon.name} is offline.")]

        # Store target (simplified - in full implementation would track actual targets)
        state.graph.update_entity(weapon_system, current_target=target)

        state.log_event(
            "weapons_targeted",
            f"{weapon.name} targeting: {target}",
            severity="info"
        )

    return [TextContent(type="text", text=json.dumps({
        "success": True,
        "weapon": weapon.name,
        "target": target
    }, indent=2))]


async def _fire_weapons(state: "GameState", arguments: dict):
    """Fire weapons."""
    weapon_system = arguments.get("weapon_system")

    with state.lock():
        weapon = state.systems.get(weapon_system)
        if not weapon:
            return [TextContent(type="text", text=f"Weapon system '{weapon_system}' not found.")]

        if not weapon.online:
            return [TextContent(type="text", text=f"{weapon.name} is offline.")]

        if weapon.efficiency < 0.3:
            return [TextContent(type="text", text=f"{weapon.name} efficiency too low to fire.")]

        # Check for target
        weapon_data = state.graph.get_entity(weapon_system)
        target = weapon_data.get("current_target") if weapon_data else None

        if not target:
            return [TextContent(type="text", text=f"{weapon.name} has no target. Use target_weapons first.")]

        # Fire (simplified - damage calculation would be more complex)
        damage = weapon.efficiency * 50  # Base damage modified by efficiency

        state.log_event(
            "weapons_fired",
            f"{weapon.name} fired at {target}. Estimated damage: {damage:.1f}",
            severity="info",
            weapon=weapon_system,
            target=target,
            damage=damage
        )

    return [TextContent(type="text", text=json.dumps({
        "success": True,
        "weapon": weapon.name,
        "target": target,
        "damage": damage
    }, indent=2))]


async def _ship_broadcast(state: "GameState", arguments: dict):
    """Broadcast message to all robots."""
    message = arguments.get("message", "")

    with state.lock():
        state.log_event(
            "broadcast",
            f"Ship broadcast: {message}",
            severity="info"
        )

        # Boost robot efficiency/morale slightly (simplified effect)
        for robot in state.robots.values():
            if robot.is_functional:
                robot.efficiency = min(100, robot.efficiency + 2)

    return [TextContent(type="text", text=json.dumps({
        "success": True,
        "message": message,
        "recipients": len(state.robots)
    }, indent=2))]


async def _set_room_temperature(state: "GameState", arguments: dict):
    """Set room temperature."""
    room_id = arguments.get("room_id")
    temperature = arguments.get("temperature", 20)

    with state.lock():
        # Check life support
        life_support = state.systems.get("life_support")
        if not life_support or not life_support.online:
            return [TextContent(
                type="text",
                text="Life support is offline. Cannot adjust temperature."
            )]

        room = state.graph.get_entity(room_id)
        if not room:
            return [TextContent(type="text", text=f"Room '{room_id}' not found.")]

        # Clamp temperature to reasonable range
        temperature = max(10, min(35, temperature))

        state.graph.update_entity(room_id, temperature=temperature)
        state.log_event(
            "temperature_adjusted",
            f"Temperature in {room.get('name', room_id)} set to {temperature}°C",
            severity="info"
        )

    return [TextContent(type="text", text=json.dumps({
        "success": True,
        "room": room_id,
        "temperature": temperature
    }, indent=2))]
