# Shipshape - Software Architecture

## Tech Stack

- Python with type hints
- NetworkX for graph state (in-memory)
- MCP server (FastMCP)
- Pydantic for models
- Fly.io via Sprites (handles suspension automatically)

## Per-Request Game Logic

The server uses a turn-based, semi-serverless style. No background threads or game loops. On each MCP request, the server:

1. Computes elapsed real time since last request
2. Processes the time delta through the simulation
3. Handles the request (sensor read or actuator command)
4. Returns the result

`process_elapsed_time(delta)` must work for:
- 0.1 seconds (rapid requests during active play)
- 8 hours (overnight idle)
- 1 week (extended absence)

This means:
- Continuous effects: multiply rate by time (`power -= drain_rate * hours`)
- Discrete events: priority queue sorted by trigger time
- Bounded catch-up: cap simulation for very long gaps, summarize instead

This is more roguelike than real-time — Rogue would update the world only on input turns. But things also unfold against the real clock between requests.

## Persistence

Fly.io Sprites handles suspension automatically. In-memory state is the source of truth. Disk saves are backups — saved periodically, or queued up away from the game logic.

Since memory is persistent through suspension, saves become a backup rather than the primary persistence mechanism.

## Graph State (NetworkX)

MUD-style prepositional relationships. Entities are nodes, relationships are edges with types:

- Node types: room, robot, cat, system, module, item, sector, etc.
- Edge types: "in", "on", "connected_to", "attached_to", "contains", etc.

The raw state of the graph is not read directly by the player. They interact through sensors, which are limited in scope by their relationships to other objects.

## MCP Tools

Tools expose modules, sensors, and actuators as a dumb computer showing facts. All actions go through actuators. Modules can go offline, affecting tool availability.

Some modules might be grouped up with a command structure. For instance, a physical communications module to interact with the robots — it would have a tool to use it, and it could go offline.

### Categories

- **Game management**: start_game, resume_game, save_game, stasis
- **Sensors**: Read state from ship systems, rooms, robots, exterior, journey
- **Actuators**: Power allocation, robot commands, doors, weapons, shields, jumps, drones
- **Databanks**: Logs, records, ship documentation

The start_game tool returns Eli's instructions — the LLM prompt that frames the experience.

## File Structure

Existing source is in `src/shipshape/`. It was generated for a real-time threaded model and needs modification for per-request logic.
