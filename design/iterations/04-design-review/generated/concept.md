# Shipshape - Concept

## Elevator Pitch

A text-based spaceship simulation played through an MCP server. The player is the ship's sentient consciousness. An AI agent (Eli) translates between the player's emotions and the ship's computer systems. The ship's simulation runs autonomously — robots act, systems degrade, events occur — and the player experiences it all as sensations in their own body.

## Inspirations

- **Dwarf Fortress** - Emergent behavior from simple needs-driven actors. Procedural terrain/world generation. Complex systems creating unscripted stories.
- **FTL: Faster Than Light** - Ship systems management, power allocation, roguelike sector progression, events and encounters.
- **MUD (Multi-User Dungeon)** - Graph-based prepositional relationships for spatial state. "The wrench is on the workbench in the engine room."
- **Tamagotchi** - Real-time (slow) care loop. The cat needs you even when you're away. Emotional attachment to a simple creature.
- **D&D / Dungeon Mastering** - Scripted encounters with actors and motivations, set within a procedurally generated world. Tables and rolls for variety.
- **Elite / Frontier** - Procedural generation of solar systems, economies, and trade from tables and seeds. The vastness of space as backdrop.
- **Alien (1979)** - A ship with a cat. Everyone else is dead. The ship wakes up.
- **Roguelike (genre)** - Seeded world generation, permadeath tension, turn-based input advancing the world, journey through increasingly dangerous territory.
- **Return of the Obra Dinn** - Investigating what happened aboard a ship through evidence and inference. Piecing together identities and events.

## Design Pillars

### The Honesty Principle

The game respects what AI can and cannot do:

- **No faked sentience.** Eli and the MCP are explicitly non-sentient. Their capabilities match what AI systems actually do.
- **Honest dialogue.** LLM-powered entities (Eli, smart robots) generate their own dialogue. Any quirks in their speech are honestly attributable to their in-universe technology. No scripted dialogue, except for dumb robots using canned responses that are also canned in-universe.
- **Player consciousness is real.** The player genuinely experiences the role. We never interfere with their thoughts.
- **Creatures are fiction.** Cats, aliens, and other non-talking creatures are accepted as part of the simulation fiction.

### Embodiment

The ship is the player's body. Eli's job is to translate raw MCP data into visceral, sensory language so the player feels they ARE the ship. The MCP itself is a dumb computer showing facts.

### Emergent Complexity

The ship simulation should be complex enough that unscripted events emerge from the interaction of simple systems — robots competing for resources, cascading failures, unexpected discoveries.

## Difficulty Modes / Ships

Three ships, each with a different difficulty, story, and character:

| Ship | Difficulty | Mode | Starting State | Passengers |
|------|-----------|------|----------------|------------|
| **Intrepid** | Easy | Exploration sandbox | All systems online | None (drone ship, never meant for people) |
| **Perseverance** | Normal | Survival adventure | Systems offline | Missing (discover what happened) |
| **Phoenix** | Hard | Horror/mystery | Antagonistic systems, communication issues | Dead (full Derelict story) |

The Intrepid and Perseverance are the initial build targets. The Phoenix incorporates the full Derelict narrative and is deferred.
