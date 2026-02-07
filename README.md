# Shipshape - Virtual Spaceship MCP Server

A Python MCP server exposing a virtual spaceship's computer system with:
- **Dwarf Fortress-style** emergent robot interactions
- **FTL-style** ship systems and roguelike journey
- **MUD-style** graph-based location/relationship storage

## Installation

```bash
pip install -e .
```

## Running the Server

```bash
python -m shipshape.server
```

Or use the installed command:

```bash
shipshape
```

## Connecting with Claude

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "shipshape": {
      "command": "python",
      "args": ["-m", "shipshape.server"]
    }
  }
}
```

## Game Concept

### Narrative Frame
- **User** = "Emotional Logic Core" (ship's sentient consciousness)
- **AI Agent (Eli)** = "Emotional Logic Interface" (translates between Core and ship systems)
- **MCP** = "Master Control Program" (in-story name for the tool interface)

### Story
The ship has suffered damage and most systems are offline. A cat survives somewhere aboard - the last biological crew member. Your goal: reach a repair facility where humans can restore what the robots cannot fix.

## MCP Tools

### Game Management
- `start_game` - Begin a new game, returns Eli's instructions
- `resume_game` - Load a saved game
- `save_game` - Save current game state

### Sensors (Read-only)
- `scan_ship` - Overview of all systems
- `scan_room` - Contents of a specific room
- `scan_robots` - Status of all robots
- `scan_robot` - Detailed status of one robot
- `scan_cat` - Cat's location and needs
- `scan_system` - Detailed system status
- `scan_exterior` - External environment
- `scan_journey` - Sector progress and map
- `read_log` - Recent events

### Actuators (Actions)
- `set_power` - Allocate power to systems
- `order_robot` - Assign tasks to robots
- `set_doors` - Control door states
- `target_weapons` - Aim weapons
- `fire_weapons` - Attack threats
- `activate_shields` - Configure shields
- `initiate_jump` - Begin FTL jump
- `launch_drone` - Deploy drones
- `ship_broadcast` - Announce to robots
