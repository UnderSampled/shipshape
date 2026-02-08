# Shipshape - Project Context

## Design History

This project has gone through three separate design iterations of the same core concept. Each was written independently, not as evolutions of one another, though later iterations remembered concepts from earlier ones.

All design materials live under `design/iterations/`, ordered chronologically:

1. **01-stargraph** - Hand-written (no Claude conversation). A data-only galaxy/universe space simulator. Graph-based state in Neo4J, procedural generation with deterministic seeds, full ontology of space objects. Designed as the simulation engine.

2. **02-derelict** - Claude conversation. A narrative investigation game aboard a single damaged ship. 3-act mystery structure with a midpoint twist (the previous Emotional Logic Core malfunctioned, a crew member sacrificed themselves to replace it). The ship "Phoenix" has secret orders to destroy a colony world. Metroidvania progression, communication degradation mechanic, single ending. This captures the full story ambition.

3. **03-shipshape** - Claude conversation. The implementation-first version. FTL-style roguelike journey, Dwarf Fortress-style robots, a cat, MCP server architecture. Written with the intent to build the simple system first and layer in story later. The full story may or may not be used, but was captured to include in the design process.

4. **04-design-review** - Claude conversation. Review of all design files for inconsistencies, followed by design decisions resolving them and generation of unified design documents.

The iterations are **complementary layers**, not competing designs:
- **StarGraph** is the engine philosophy — a simulation rich enough to build stories in.
- **Shipshape** is the game engine layer — DF robots, FTL journey, cat, system restoration make the ship complex and interesting.
- **The Derelict** is the narrative layer — mystery, twist, communication degradation, to be woven into the engine later.

The plan is to build the Shipshape engine first, then add the Derelict story on top. Surface-level inconsistencies between the earlier docs (documented in `design/iterations/04-design-review/`) reflect this layered intent, not conflicting visions. The iteration 04 generated docs represent the current unified design.

## Convention: Save Conversation Notes

At the end of each Claude conversation that involves design decisions or user statements about the project, save the user's statements (verbatim, with context headers) into the next numbered iteration folder under `design/iterations/`. Each iteration folder contains:
- `notes.md` (or `notes_*.md`) - User's verbatim statements with context
- `generated/` (optional) - Any documents Claude produced during the session

This preserves design intent across sessions so future conversations have access to the creator's actual words and reasoning.

### Notes format

Each user statement is captured as a blockquote under a descriptive heading. Below each quote, a `*[Context: ...]*` line briefly notes **what Claude said that the user was responding to** — just enough to understand the prompt. Do NOT summarize, analyze, or restate the user's words in the context line.

## Tech Stack

- Python with type hints
- NetworkX for graph state (in-memory, not Neo4J)
- MCP server (FastMCP)
- Turn-based simulation with time deltas (not real-time threads)
- Fly.io via Sprites (handles suspension automatically)
- Pydantic for models
- Per-request game logic (no background threads/loops)
