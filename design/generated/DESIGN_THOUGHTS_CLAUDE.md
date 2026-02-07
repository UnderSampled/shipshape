# Claude's Design Analysis

## Platform Assessment

### Why Fly.io Works Well

Fly.io is a strong fit for Shipshape because it resolves the tension between:
- Wanting Python (mature, familiar, NetworkX)
- Wanting serverless-like cost model (don't pay when idle)
- Wanting graph operations without SQL contortions

Cloudflare Workers would require TypeScript (or beta Python), SQLite-only storage, and manual graph query implementation via recursive CTEs. The research showed no viable pure-JS Cypher interpreter exists, and SQLite extensions (graphqlite, sqlite-graph) can't load on Cloudflare.

Fly.io sidesteps all of this: run Python, use NetworkX, suspend when idle.

### The Suspend Model

Fly.io's suspend is underappreciated for game servers:
- Full VM snapshot (memory + CPU state)
- ~100-500ms resume (vs seconds for cold boot)
- Storage-only cost when suspended
- SIGTERM signal allows clean save before suspend

This means the game state in memory IS the persistent state, with disk as backup. It's conceptually similar to Cloudflare Durable Objects but with full VM flexibility.

## Simulation Architecture

### Turn-Based as Default

The roguelike parallel is apt. Key insight: the world doesn't need to run continuously if:
1. All state changes can be computed from time deltas
2. The player (via AI) is the only one requesting state

This simplifies everything:
- No background threads/loops
- No race conditions
- Deterministic: same inputs + same Δt = same outputs
- Testable: can simulate any time period

### Time Delta Design

The critical realization is that `process_elapsed_time(delta)` must work for:
- 0.1 seconds (rapid requests during active play)
- 8 hours (overnight idle)
- 1 week (extended absence)

This rules out naive approaches like "run the game loop N times to catch up." Instead:
- Continuous effects: multiply rate by time (`power -= drain_rate * hours`)
- Discrete events: priority queue sorted by trigger time
- Bounded catch-up: cap simulation for very long gaps, summarize instead

### The Hybrid Option

The user's insight about hybrid operation is valid:
- While actively playing, short background ticks could provide responsiveness
- The same Δt-based logic handles both cases
- The distinction is UX (smoother active play) not architecture

But pure turn-based may be simpler and sufficient for an MCP-based game where the AI mediates all interaction anyway.

## Multiplayer Implications

### The Core Problem

Turn-based assumes: "world waits for player input."
Multiplayer breaks this: "multiple players, world can't freeze for all."

Time-delta simulation helps but doesn't solve coordination:
- Player A fires at Player B
- Player B fires at Player A
- Both requests arrive at "the same time"
- Who wins?

### Sector Authority Model

The cleanest solution is spatial partitioning:
- Each sector/region has one authoritative server
- Ships in that sector send actions to that server
- Server resolves conflicts locally (ordering, physics, etc.)
- Cross-sector = async messaging, not shared state

This avoids distributed graph mutations by ensuring each subgraph has one writer.

### Graph Partitioning

For NetworkX, this could mean:
- Each sector server has its own `nx.DiGraph()` for local entities
- Ships moving between sectors = serialize ship subgraph, transfer, deserialize
- Shared universe data (star map, faction standings) = read-only replicated

The graph isn't truly distributed; it's partitioned with clear ownership.

## Recommendations

### Phase 1: Single-Player MVP
- Fly.io + Python + NetworkX
- Turn-based simulation with time deltas
- MCP server via FastMCP
- JSON backup on SIGTERM + periodic
- Single machine, suspend when idle

### Phase 2: Polish
- Background ticks during active sessions (optional)
- Better event queue for scheduled happenings
- Save versioning for compatibility

### Phase 3: Multiplayer (if pursued)
- Sector-based architecture
- Each sector = separate Fly machine
- Players connect to their current sector's server
- Design ship handoff protocol for sector transitions
- Event sourcing for audit trail / replay

### Open Questions

1. **MCP transport**: Streamable HTTP vs SSE for Fly.io deployment?
2. **Session management**: How does MCP client reconnect after suspend/resume?
3. **Save format**: JSON sufficient or need something more structured?
4. **Multiplayer identity**: How are players authenticated across sectors?

These can be deferred until the single-player foundation is solid.
