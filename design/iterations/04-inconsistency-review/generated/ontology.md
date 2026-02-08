# Shipshape - Ontology

## The Graph

All game state is stored in a single directed multigraph. Entities are nodes with typed attributes. Relationships are labeled edges.

## Entity Types

Listed roughly by scale, largest to smallest:

### Environments

Top-level spatial containers in the procedurally generated universe.

- **Star systems** - Generated from seed. Contain gravitational bodies, jump paths.
- **Gravitational bodies** - Planets, moons, stars. Orbits and gravity wells.
- **Asteroid fields** - Navigation hazards, mining opportunities.
- **Nebulae** - Sensor interference zones, shield-boosting regions.
- **Dead space** - Empty void between points of interest.

### Stations

Fixed structures in space. AI-operated, no humans.

- **Trading depots** - Buy/sell items and modules
- **Refueling stations** - Fuel and consumable resupply
- **Repair docks** - Automated repair services
- **Beacons** - Information about nearby space
- **The destination** - Scripted endpoint of the journey

### Ships

Vessels that move through space. The player's ship is one of these.

- Have hardpoints for modules
- Have rooms connected by doors
- Contain robots, items, systems
- Can be derelicts (salvage targets)

### Drones

Small mobile units deployed from ships or stations.

- Operate externally (repair, scouting, combat)
- May have hardpoints (small)
- Controlled through drone control system
- Range limited by control module

### Modules

Attach to hardpoints on ships, stations, and drones. Limited by hardpoint size.

- **Weapons** - Auto-cannons, missiles, beams
- **Sensors** - Various types and ranges
- **Cargo** - Storage containers
- **Utility** - Repair arms, tractor beams, mining gear
- **Defense** - Shield projectors, armor, countermeasures
- **Propulsion** - Engines, thrusters

### Items

Objects that can be stored, moved, used, and traded.

- **Quest items** - Non-fungible, tied to discovery/story
- **Rare artifacts** - Unique finds with special properties
- **Trade goods** - Fungible, for exchange (value varies by location)
- **Consumable resources** - Fuel, spare parts, raw materials, food

### Robots

Mobile autonomous entities aboard ships. See robots.md for full detail.

### Creatures

Biological entities. The cat. Possibly aliens encountered in space (non-sentient).

## Relationships

Edges in the graph describe spatial and logical relationships:

### Spatial

- `in` - "The robot is **in** the engine room"
- `on` - "The wrench is **on** the workbench"
- `connected_to` - "The engine room is **connected to** the corridor"
- `orbits` - "The moon **orbits** the planet"
- `docked_at` - "The ship is **docked at** the station"

### Functional

- `attached_to` - "The sensor module is **attached to** hardpoint 3"
- `powered_by` - "The door is **powered by** the reactor"
- `assigned_to` - "ENG-3 is **assigned to** the reactor room"
- `contains` - "The cargo bay **contains** spare parts"

### Logical

- `jump_path` - "Sol **connects to** Alpha Centauri by jump path"
- `belongs_to` - "The collar **belongs to** the cat"

## Containment Rules

Entities are generally contained by larger entities:
- Items fit in modules or rooms
- Modules fit on hardpoints (size-limited)
- Robots fit in rooms
- Drones fit in drone bays (or small drones in larger drone modules)
- Rooms are parts of ships/stations
- Ships/stations are in environments

A ship cannot be in a drone. A drone might be in a ship's module, but only a very small drone in another drone's module.

## Memoized Generation

Procedurally generated entities (from seed) are memoized: generated on first access, mutable after discovery. This means:
- The universe is deterministic from the seed
- But once the player interacts with something, it can change
- Unvisited areas don't consume memory
