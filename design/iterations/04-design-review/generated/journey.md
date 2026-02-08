# Shipshape - The Journey

## Structure

The journey follows a roguelike sector structure inspired by FTL. The outer space is procedurally generated (Elite-style) and serves as a backdrop for what's happening inside the ship and a source for supplies.

Scripted locations (like the destination) are built into the generated map.

## Sectors

8 sectors of increasing difficulty. Each sector is a node map generated from the seed. The player navigates from entry to exit, choosing paths through nodes.

### Sector Themes

1. **The Quiet** - Empty space, few events. Recovery time after awakening.
2. **The Scatter** - Debris fields. Salvage opportunities, navigation hazards.
3. **The Bright** - Near a star. Solar activity, radiation events.
4. **The Deep** - Far from stars. Cold, sensor-limited, resource-scarce.
5. **The Graveyard** - Dense with derelicts. Rich salvage but dangerous.
6. **The Storm** - Nebula region. Sensor chaos, shield boosts, hidden hazards.
7. **The Gauntlet** - Asteroid-dense. Intense navigation challenge.
8. **The Approach** - Final stretch to the destination.

## Node Types

Each node in a sector map has a type determining what happens there:

- **Empty Space** - Nothing notable. Rest and repair opportunity.
- **Beacon** - Information about nearby nodes and routes.
- **Derelict** - Abandoned ship or structure. Salvage modules, items, resources. May have automated defenses.
- **Depot** - Automated trading post. Buy/sell items and modules. Refuel.
- **Hazard** - Environmental danger (asteroid cluster, radiation pocket, gravity anomaly).
- **Anomaly** - Strange occurrence. Unpredictable outcome.
- **Jump Point** - Required to reach the next sector.

## Procedural Generation

### From Seed (Deterministic)

The universe layout is generated from a fixed seed:
- Sector maps (node count, connections, layout)
- Node contents (what type, what's there)
- Star systems and environments (Elite-style table rolls)
- Derelict contents (modules, items, condition)
- Station inventories and prices
- Encounter parameters

### Memoized

Nodes are generated on first access. Until visited, they exist only as a seed + position. Once generated, they become mutable — the player can change them (salvage depleted, station inventory reduced, etc.).

### Dungeon Modules

Some encounters expand into explorable sub-areas with their own internal structure:
- Derelict space stations (rooms, hazards, loot)
- Robot mining colonies
- Alien hives
- Abandoned research facilities

These are each their own game system — procedurally generated interiors with encounters, hazards, and rewards.

## Jump Mechanics

- Jumps require charged engines
- Charge time depends on engine health and power allocation
- Jumping consumes fuel
- Cannot jump during combat or emergency
- Jump cooldown after arriving at a new node
- Each jump moves to a connected node in the sector map

## Encounters at Nodes

Encounters are generated according to the DM model: actors with motivations and triggers. Even in procedural space, encounters have internal logic:

- An automated defense system protects a derelict because it was programmed to
- A trading depot has specific inventory based on its location and the seed
- A hazard has specific parameters (intensity, duration, type)

No sentient beings are encountered. Stations are AI-operated. Ships are derelicts or automated. The universe is vast and empty of intelligent life.

## Resources and Trade

The journey creates resource pressure:
- **Fuel** - Consumed by jumps and engines. Must be found or traded for.
- **Spare parts** - Needed for repairs. Salvaged or purchased.
- **Raw materials** - For robot construction and system fabrication.
- **Food/supplies** - For the cat. Found in derelicts or traded.

Trade occurs at automated depots. Prices vary by location (seed-determined). The player trades items and resources.

## The Destination

The final node in sector 8 is the destination — a repair facility where the ship can dock. This is a scripted location built into every generated map. Reaching it and being repaired enough to dock is the win condition.
