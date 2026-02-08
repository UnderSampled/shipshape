# Shipshape - Game Design

## Core Loop

Restore systems, manage robots, care for the cat, survive events, journey toward the destination.

On the Perseverance: Explore → Restore → Discover → Survive → Progress.

## Progression (Perseverance)

The game starts with most systems offline. Restoring them is story progression/goal, while also being a tutorial sequence — allowing the systems themselves to be more complex to learn how to manage.

**Phase 1 - Awakening**: Reactor at minimal power, local sensors only, basic lighting. A few robots still functional.

**Phase 2 - Reaching Out**: Door control, internal sensor network, robot charging stations.

**Phase 3 - Discovery**: Partial life support restored. The cat is discovered. (The cat is not mentioned in diagnostics or documentation before this point.)

**Phase 4 - Defense**: Shields, weapon systems, improved external sensors.

**Phase 5 - Journey**: Engines, navigation, FTL jump capability. The destination becomes known.

**Phase 6 - Full Awakening**: All restorable systems online.

## The Roguelike Journey

The outer space is procedurally generated from a fixed seed — Elite gives a good blueprint. It is ultimately a backdrop for what's going on inside the ship, and a source for supplies and an end goal. Scripted locations (like the destination) are built into the generated map.

### Sectors

8 sectors of increasing difficulty, each a node map. Navigate from entry to exit, choosing paths through nodes.

### Node Types

- Empty space (rest opportunity)
- Beacon (information about nearby nodes)
- Derelict (salvage opportunity)
- Depot (automated trading)
- Hazard (environmental danger)
- Anomaly (unpredictable)
- Jump point (reach next sector)

### Procedural Encounter Modules

Some encounters are procedurally generated dungeon modules — a derelict space station, robot mining colony, alien hive, etc. Each is a game system of its own.

### Jump Mechanics

Jumps require charged engines, consume fuel, cannot happen during emergencies. Cooldown after arriving.

## Events

All events occur without sentient beings — a full variety, but never meeting another sentient being, to be true to life. Automated stations, derelict ships, aliens (non-sentient creatures), but no people.

### External Events

Asteroid fields, solar flares, debris fields, nebulae, derelict ships, automated stations, gravity wells, radiation storms.

### Internal Events

System malfunctions, power surges, fires, hull breaches, coolant leaks, robot malfunctions, cat emergencies.

## Time Model

Things unfold in real time against the real clock. The simulation processes elapsed time via time deltas on each request — this must work for 0.1 seconds (rapid play) and 8 hours (overnight).

A stasis tool lets the core skip time forward until a duration or an interrupt event.

In-game random events (like constructing a robot with a random personality) are not seeded — they happen chaotically during play.

## The Ending

Being repaired enough to dock is a requirement to get the good ending. Docking is a reward — a denouement. The airlock opens. Human voices, for the first time. The game ends there.
