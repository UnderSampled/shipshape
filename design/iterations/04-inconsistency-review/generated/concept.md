# Shipshape - Concept

## High Concept

A text-based spaceship simulation exposed through an MCP server. The player is the ship's sentient consciousness, working through an AI interface to manage systems, crew, and journey. The MCP server is the player's only interaction with the virtual spaceship.

## Inspirations

- **Dwarf Fortress** - Emergent behavior from simple autonomous agents with needs and traits. Procedural terrain/world generation.
- **FTL** - Ship systems management, roguelike journey through sectors, events and encounters.
- **MUD** - Graph-based prepositional relationships for locations, containment, and spatial reasoning.
- **Tamagotchi** - A pet to come back for and take care of, with a real-time (slow time) component. Emotional attachment.
- **D&D / Dungeon Mastering** - A world with actors, motivations, and triggers for scripted encounters. Procedural dungeon modules.
- **Elite / Frontier** - Rolling from tables to generate solar systems, economies. Procedural outer space as backdrop.
- **Alien** - The ship in Alien, but if Ripley and the Xenomorph both died and the cat was the only survivor — and then the ship wakes up.
- **Roguelike (Rogue)** - World updates only on input turns. Seeded procedural generation. Permadeath implied.
- **Metroidvania** - Come back to areas after discovering information, fixing things up, unlocking doors.
- **Star Citizen** - An engine to build stories in; single-player story layered onto a complex simulation.

## Design Principles

### Engine First, Story Later

The Dwarf-Fortress + FTL style survival game makes the spaceship complex enough to be interesting when it comes time to explore it for the story. The engine is built first. The narrative is layered on top.

### The Honesty Principle

The game respects what AI can and cannot authentically do:

- An LLM-powered AI (like Eli, or like a smart robot) can have dialogue it generates, and any problems with its generation can honestly be attributed in-game to the peculiarities of the robot's tech — not pretending to be smarter or more sentient than it is.
- There should be no scripted dialogue, apart from dumb robots using scripted dialogue that is also scripted in-universe.
- Creatures (the cat, aliens) are an accepted part of the fiction. They won't talk, so it's less of an issue.
- The player's sentience is real. The AI's lack of sentience is honest.

### Complementary Layers

- **StarGraph** is the engine philosophy — a simulation rich enough to build stories in.
- **Shipshape** is the game engine layer — robots, journey, cat, system restoration.
- **The Derelict** is the narrative layer — mystery, twist, to be woven in later.

## Three Ships / Three Modes

| Ship | Difficulty | Mode | Starting State | Crew |
|------|-----------|------|----------------|------|
| **Intrepid** | Easy | Exploration sandbox | All systems online | A drone ship never meant to have people aboard |
| **Perseverance** | Normal | Survival adventure | Systems offline | Crew missing |
| **Phoenix** | Hard | Horror/mystery | Antagonistic systems and communications issues | Crew dead |

The first two are the initial build targets. The Phoenix incorporates the full Derelict story.
