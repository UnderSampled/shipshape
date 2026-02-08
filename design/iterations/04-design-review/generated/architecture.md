# Shipshape - Software Architecture

## Tech Stack

- **Python** with type hints
- **NetworkX** for in-memory graph state
- **FastMCP** for the MCP server
- **Pydantic** for models and serialization
- **Fly.io via Sprites** for hosting (automatic suspension)

## Simulation Model: Per-Request Time Deltas

No background threads or game loops. The world advances when a request arrives.

```
Request arrives
  -> Compute delta_t since last request
  -> Process all changes for that interval
  -> Handle the request
  -> Return response
  -> Record timestamp
```

### Time Delta Processing

`process_elapsed_time(delta)` must handle:
- **Milliseconds** (rapid requests during active play)
- **Hours** (overnight, between sessions)
- **Days/weeks** (extended absence)

Processing strategies:
- **Continuous effects**: Multiply rate by time (`power -= drain_rate * delta`)
- **Discrete events**: Priority queue sorted by trigger time, process all events with timestamps <= now
- **Bounded catch-up**: For very long gaps, cap simulation depth and summarize

This is NOT running the game loop N times to catch up. It is computing the result of elapsed time directly.

### Real-Clock Time

The game unfolds against the real wall clock. The cat gets hungry while you're away. Robots continue their tasks. Systems degrade. This enables the tamagotchi-like care loop.

### Stasis Tool

An MCP tool allows skipping time forward by a specified duration or until an interrupt event. Internally, this is just a large time delta processed at once.

## Graph State (NetworkX)

All game state is stored in a directed multigraph. Entities are nodes, relationships are edges with labels.

```python
# Entity as node with attributes
graph.add_node("reactor_room", type="room", atmosphere=0.95, temperature=22)

# Relationship as labeled edge
graph.add_edge("robot_ENG_1", "reactor_room", relation="in")
graph.add_edge("wrench", "workbench", relation="on")
graph.add_edge("workbench", "reactor_room", relation="in")
```

The graph is the single source of truth. MCP tools read from and write to the graph.

## Persistence

### Memory as Primary State

On Fly.io/Sprites, the VM suspends with memory intact. The in-memory graph IS the persistent state. Resume is fast (~100-500ms).

### Disk as Backup

Periodic JSON backup of the full graph state. Also triggered on SIGTERM (before suspension). This is a safety net, not the primary persistence mechanism.

### Save/Load

- `save_game` - Serialize graph + metadata to JSON on disk
- `resume_game` - Deserialize from disk (used after cold boot, not after suspend)
- `start_game` - Initialize a new graph from ship definition + seed

## MCP Server Structure

```
MCP Server
  |
  +-- Game Management Tools (start, resume, save, stasis)
  |
  +-- Sensor Tools (read from graph, gated by sensor hardware status)
  |
  +-- Actuator Tools (write to graph, gated by actuator hardware status)
  |
  +-- Module Tools (grouped by physical module, can go offline)
```

Tools map to physical hardware. If a sensor module is offline, its tools return errors or nothing. If an actuator is damaged, its tools may fail or produce unexpected results.

## Procedural Generation

World generation uses a fixed seed for deterministic results:
- Sector maps, node placement, connections
- Star systems, environments (Elite-style table rolls)
- Encounter contents (what's in a derelict, what a station sells)

Seeded generation is memoized — objects are generated on first access and become mutable after discovery.

Runtime randomness (robot personality on construction, event rolls during play) uses the game's running RNG, not the seed.

## File Structure

```
shipshape/
  pyproject.toml
  README.md
  CLAUDE.md
  design/
  src/
    shipshape/
      __init__.py
      server.py          # MCP server entry point
      state/
        __init__.py
        graph.py          # NetworkX graph state
        game.py           # Game state container, time tracking
        persistence.py    # Save/load
      simulation/
        __init__.py
        engine.py         # Time delta processing
        systems.py        # Ship system simulation
        robots.py         # Robot behavior simulation
        events.py         # Event generation and processing
        journey.py        # Sector/jump progression
        cat.py            # Cat behavior simulation
      ship/
        __init__.py
        layout.py         # Ship room/module definitions per ship type
        systems.py        # System definitions
      tools/
        __init__.py
        sensors.py        # Sensor MCP tools
        actuators.py      # Actuator MCP tools
        game.py           # Game management MCP tools
```

## Dependencies

```toml
[project]
dependencies = [
    "mcp>=1.0.0",
    "networkx>=3.0",
    "pydantic>=2.0",
]
```
