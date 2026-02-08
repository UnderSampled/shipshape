# Shipshape - Ontology

## The Graph

The universe state is a graph describing objects, their types, their individual states, and their relationships. The raw state of the graph is not read directly by actors — they interact through sensors, which are limited in scope.

## Entity Types

Listed generally by scale. Containment follows size: items fit in modules, modules attach to ships, ships exist in environments.

### Environments
- Star systems
- Gravitational bodies (planets, moons)
- Asteroid fields
- Nebulae
- Dead space

### Stations
- Automated trading depots
- Refueling stations
- Repair facilities (including the destination)
- Derelict stations (procedural dungeon modules)

### Ships
- The player's ship (Intrepid, Perseverance, or Phoenix)
- Derelict ships (salvage encounters)
- Automated vessels

### Drones
- External repair drones
- Combat drones
- Scout drones

### Modules
- Attach to hardpoints on ships, stations, and drones
- Limited by hardpoint size
- Can be salvaged, swapped, damaged, repaired

### Robots
- Ship crew at various intelligence tiers
- Exist within the ship's rooms
- Have needs, traits, tasks

### Items
- Non-fungible quest items
- Rare artifacts
- Fungible trade-goods
- Consumable resources (fuel, repair materials, cat food)

### Creatures
- The cat
- Potential alien fauna (non-sentient)

## Relationships

Relationships are edges in the graph with typed predicates:

- **Spatial**: "in", "on", "connected_to", "orbits", "docked_at"
- **Containment**: "contains", "stored_in", "attached_to"
- **Navigation**: "jump_path" (between star systems), "route_to"
- **State**: "is_burning_since", "has_fuel_level", "has_power_level"
- **Social**: "assigned_to", "commanded_by", "near"

## State Examples

- "Sol" is a star system
- The Sol system connects to Alpha Centauri by a jump path
- The X1 fighter is in hangar 535424; hangar 535424 is in starship 234
- The X1 fighter's fuel tank is 55% full
- The thruster is burning; it has been burning since `<timestamp>`

## Events and Effects

Mutations to the universe state occur through events at specific points in time.

**Effects** are triggered events according to conditional rules. Results can be deterministic or probability-driven, with probabilities altered by object states:
- When a fuel tank is empty, thrusters stop burning
- When landing without gear deployed: 35% hull damage, 5% rupture
- When docked at a depot, the ship can trade

**Actions** are events caused by an actor through actuators:
- Fire an auto-cannon at a target
- Set a long-range sensor to scan mode
- Dispatch a repair robot

## Procedural Generation

The outer world is procedurally generated from a fixed seed (Elite/Frontier style). Solar systems, economies, and encounters are rolled from tables. Scripted locations (the destination, key encounters) are placed into the generated map.

In-game randomness (robot personality on construction, event outcomes) is not seeded — it happens chaotically during play.

Procedurally generated objects are memoized: generated on-demand from the seed, but mutable after discovery.
