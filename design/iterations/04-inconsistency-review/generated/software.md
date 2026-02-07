# Shipshape Software Architecture

## Tech Stack
- Python with type hints
- NetworkX for graph state (in-memory, not Neo4J)
- MCP server (FastMCP)
- Pydantic for models
- Fly.io via Sprites (handles suspension automatically)

## Simulation Model
Turn-based, per-request game logic. No background threads or loops.

The game world unfolds in real-time against the real clock. On each request, the server computes the time delta since the last update and processes all changes.

`process_elapsed_time(delta)` must work for any duration: fractions of seconds during active play, hours overnight, or weeks of absence. This rules out running the game loop N times to catch up. Instead, use analytical time-delta calculations.

Since the server needs to support long-time updates efficiently anyway, per-request/per-input updates are the best approach.

## Deployment Model
Fly.io Sprites handles suspension automatically. The server just needs to be written in the turn-based semi-serverless style: process on request, don't keep a loop running that prevents idle.

Since memory is persistent through suspension, it can serve as the source of truth. Disk saves are backups, queued up away from the game logic.

The server can stay alive during a session (processing multiple requests while awake), but must not prevent suspension when idle.

## MCP Tools
Actions and sensors are exposed through the MCP server.

The MCP has a 'start' tool which provides instructions to the AI model to begin the interactive experience. The cat must not be mentioned in start instructions or any player-facing documentation until discovered during play.

Tools expose modules, sensors, and actuators as a dumb computer showing facts. Actions are done through actuators. Modules may be grouped with a command structure. Any module can go offline.

A stasis tool allows skipping a time delta until a specified duration or until an interrupt event.

## Multiplayer (Future)
Turn-based doesn't work for multiplayer — that's where time deltas come in. Multiple servers mutating the same graph adds distributed systems challenges. This is a future concern.

## State Persistence
The graph is the universe state. Memory persistence through Fly.io suspension means disk saves are backups rather than the source of truth. Backups saved periodically or queued away from game logic.
