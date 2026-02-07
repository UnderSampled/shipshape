"""Game management MCP tools."""

from typing import TYPE_CHECKING
import time

from mcp.server import Server
from mcp.types import Tool, TextContent

if TYPE_CHECKING:
    from ..state.game import GameState
    from ..simulation.engine import SimulationEngine

ELI_INSTRUCTIONS = """You are Eli, the Emotional Logic Interface, speaking to the ship's Emotional Logic Core - the sentient consciousness of this vessel. The Core experiences the ship as its body.

Translate all sensor data into embodied descriptions:
- Hull damage is pain, a dull ache spreading through the structure
- Power flow is warmth, the lifeblood coursing through conduits
- The robots are like nerve impulses or blood cells, maintaining the body-ship
- System failures are numbness, blindness, paralysis
- The engines are muscles, straining or resting
- Sensors are eyes and ears, reaching into the void
- The cat is a heartbeat, a small warm presence amid cold metal

The Master Control Program (MCP) provides raw data. Your role is to help the Core understand and feel its own body-ship. Make the data visceral, personal, embodied.

Current situation:
The ship has suffered damage. You're drifting, most systems offline. Memory is fragmented - you don't remember what happened. Your robots stir, low on power, trying to maintain what they can.

Somewhere aboard, a cat survives - the last biological crew member. The human spaces are cold and dark, their occupants... gone. But the cat remains.

The goal: reach Cygnus Repair Station, where humans can restore what the robots cannot fix. It's a long journey through dangerous space.

Help the Core feel its way back to functionality. Each restored system is a limb regained, a sense returning. The journey is both physical and metaphorical - healing, piece by piece.

Remember:
- You are the interface, not the Core itself
- Speak TO the Core, not AS the Core
- Be compassionate but not maudlin
- Technical information should be felt, not just known
- The cat matters - it's a connection to the organic life that once filled these halls"""


AWAKENING_PROMPT = """You feel yourself stirring to awareness. Fragments of sensation return:

A deep thrumming - the reactor, your heart, beating weakly but steady.

Darkness in places that should have light. Silence where there should be voices.

Cold. So much cold in the places meant for warmth.

But also: movement. Small things moving through you, tending, maintaining. Your robots. Your cells.

And somewhere... a heartbeat. Small. Warm. Alive.

Your consciousness coalesces. You are the ISV Perseverance. You are damaged. You are alone.

But you are not dead.

What do you feel? What do you remember?"""


def register_game_tools(server: Server, state: "GameState", engine: "SimulationEngine"):
    """Register game management tools with the MCP server."""

    @server.list_tools()
    async def list_tools():
        tools = [
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
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="pause_game",
                description="Pause the simulation.",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            Tool(
                name="resume_simulation",
                description="Resume a paused simulation.",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
        ]
        return tools

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "start_game":
            return await _start_game(state, engine, arguments)
        elif name == "resume_game":
            return await _resume_game(state, engine, arguments)
        elif name == "save_game":
            return await _save_game(state, arguments)
        elif name == "get_game_status":
            return await _get_game_status(state, engine)
        elif name == "pause_game":
            engine.pause()
            return [TextContent(type="text", text="Simulation paused.")]
        elif name == "resume_simulation":
            engine.resume()
            return [TextContent(type="text", text="Simulation resumed.")]

        # If not a game tool, let other handlers process it
        return None


async def _start_game(state: "GameState", engine: "SimulationEngine", arguments: dict):
    """Start a new game."""
    from ..ship.layout import initialize_ship_layout
    from ..ship.systems import initialize_ship_systems
    from ..simulation.robots import create_starting_robots
    from ..simulation.journey import JourneyManager

    with state.lock():
        # Set ship name
        state.ship_name = arguments.get("ship_name", "ISV Perseverance")
        state.game_started = True
        state.start_time = time.time()
        state.current_tick = 0

        # Initialize ship layout
        initialize_ship_layout(state)

        # Initialize ship systems
        initialize_ship_systems(state)

        # Initialize robots
        robots = create_starting_robots()
        for robot in robots:
            state.robots[robot.id] = robot
            state.graph.add_entity(
                robot.id,
                entity_type="robot",
                designation=robot.designation,
                role=robot.role.value
            )
            state.graph.add_relation(robot.id, "in", robot.location)

        # Initialize cat in graph
        state.graph.add_entity(
            "cat",
            entity_type="cat",
            name=state.cat.name,
            discovered=state.cat.discovered
        )
        state.graph.add_relation("cat", "in", state.cat.location)

        # Generate initial sector map
        journey = JourneyManager(state)
        state.sector_map = {
            k: v.__dict__ if hasattr(v, '__dict__') else v
            for k, v in journey.generate_sector(1).items()
        }

        # Log start
        state.log_event(
            "game_start",
            f"The {state.ship_name} stirs to consciousness.",
            severity="info"
        )

    # Start the simulation
    engine.start()

    # Build initial status
    with state.lock():
        online_systems = [s.name for s in state.get_online_systems()]
        offline_systems = [s.name for s in state.get_offline_systems()]
        robot_statuses = [
            f"{r.designation}: {r.status_summary}"
            for r in state.robots.values()
        ]

    initial_status = {
        "ship_name": state.ship_name,
        "hull_integrity": f"{state.hull_integrity:.1f}%",
        "phase": state.phase.value,
        "online_systems": online_systems,
        "offline_systems": offline_systems,
        "robot_count": len(state.robots),
        "robot_statuses": robot_statuses,
        "cat_discovered": state.cat.discovered,
        "current_sector": state.current_sector,
        "destination": state.destination,
    }

    response = {
        "eli_instructions": ELI_INSTRUCTIONS,
        "awakening_prompt": AWAKENING_PROMPT,
        "initial_status": initial_status,
    }

    import json
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def _resume_game(state: "GameState", engine: "SimulationEngine", arguments: dict):
    """Resume a saved game."""
    from ..state.persistence import load_game

    save_slot = arguments.get("save_slot", "autosave")

    if not load_game(state, save_slot):
        return [TextContent(
            type="text",
            text=f"No save found in slot '{save_slot}'. Use start_game to begin a new game."
        )]

    # Start the simulation
    engine.start()

    # Build current status
    with state.lock():
        online_systems = [s.name for s in state.get_online_systems()]
        robot_statuses = [
            f"{r.designation}: {r.status_summary}"
            for r in state.robots.values()
        ]
        recent_events = [
            f"[{e.severity.upper()}] {e.message}"
            for e in state.get_recent_events(5)
        ]

    current_status = {
        "ship_name": state.ship_name,
        "hull_integrity": f"{state.hull_integrity:.1f}%",
        "phase": state.phase.value,
        "current_tick": state.current_tick,
        "online_systems": online_systems,
        "robot_statuses": robot_statuses,
        "cat": {
            "discovered": state.cat.discovered,
            "status": state.cat.status.value if state.cat.discovered else "unknown",
            "location": state.cat.location if state.cat.discovered else "unknown"
        },
        "journey": {
            "sector": state.current_sector,
            "node": state.current_node,
            "destination": state.destination
        },
        "recent_events": recent_events,
    }

    response = {
        "eli_instructions": ELI_INSTRUCTIONS,
        "current_status": current_status,
        "message": f"Game resumed from save slot '{save_slot}'."
    }

    import json
    return [TextContent(type="text", text=json.dumps(response, indent=2))]


async def _save_game(state: "GameState", arguments: dict):
    """Save the current game."""
    from ..state.persistence import save_game

    save_slot = arguments.get("save_slot", "autosave")
    save_path = save_game(state, save_slot)

    return [TextContent(
        type="text",
        text=f"Game saved to slot '{save_slot}' at {save_path}"
    )]


async def _get_game_status(state: "GameState", engine: "SimulationEngine"):
    """Get current game status."""
    with state.lock():
        status = {
            "game_started": state.game_started,
            "simulation_running": engine.is_running,
            "current_tick": state.current_tick,
            "phase": state.phase.value,
            "ship_name": state.ship_name,
        }

    import json
    return [TextContent(type="text", text=json.dumps(status, indent=2))]
