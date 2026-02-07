# Shipshape Game Design

## Inspirations
- **Dwarf Fortress** - Emergent interactions, procedural terrain generation
- **FTL** - Ship systems, roguelike journey
- **MUD** - Graph-based prepositional relationships for state/locations
- **Tamagotchi** - Cat care, real-time slow-time component, emotional attachment
- **D&D** - Dungeon master approach to world design: actors, motivations, scripted encounter triggers
- **Elite/Frontier** - Procedural generation of solar systems, economies, space as backdrop
- **Alien** - Cat on a ship (if Ripley and the Xenomorph both died and the cat was the only survivor, and then the ship wakes up)
- **Rogue** - World updates on input turns
- **Metroidvania** - Non-graphical: come back to areas after discovering information, fix things, unlock doors

## The Graph
State is stored in a graph describing objects, their types, their individual states, and their relationships (MUD-style prepositional relationships).

Examples:
- "Sol" is a star system
- The Sol system connects to Alpha Centauri by a "jump path"
- The X1 fighter is in hangar 535424; hangar 535424 is in starship 234
- The X1 fighter's fuel tank is 55% full
- The thruster is burning; it has been burning since \<timestamp\>

## Ontology
Listed generally by size. Items might be stored in modules, a station might be in an asteroid field, but it's unlikely for a ship to be in a drone.

- **Environments** - gravitational bodies (planets), asteroid fields, dead space
- **Stations**
- **Ships**
- **Drones**
- **Modules** - attach to hardpoints on ships, stations, and drones, limited by their size
- **Items**
  - Non-fungible quest items
  - Rare artifacts
  - Fungible trade-goods and consumable resources

## Events and Effects
Mutations to the universe state occur through events at specific points in time.

**Effects** are triggered events, occurring according to conditional rules. Results can be simple cause-and-effect, or random driven by probability tables. Probabilities can be altered by object states. Examples:
- When a fighter's fuel tank is empty, its thrusters stop burning
- When a fighter lands without landing gear deployed, there is a 35% chance of damaging the hull
- When docked at a space-port, a ship can trade

**Actions** are events caused by an actor through actuators. Examples:
- An auto-cannon can be fired at a target
- A long-range sensor can be set to scan mode
- A repair droid can be dispatched

## The Cat
Not discovered up front. Not mentioned in any diagnostics or documentation until discovered during play. The core should be learning what it means to be a ship before meeting the cat.

The cat provides something to come back for and take care of, with a real-time (slow time) component. Emotional attachment. Tamagotchi-style ongoing care.

## Progression
The game starts with most systems offline. Restoring them is story progression/goal, while also being a tutorial sequence, allowing the systems themselves to be more complex to learn how to manage.

Non-graphical Metroidvania: come back to areas after discovering information, fix things up, unlock doors.

## World Design
Approach like a D&D dungeon master: set up a world with actors, motivations, and triggers for scripted encounters.

- Some parts procedurally generated like dungeon modules (derelict space station, robot mining colony, alien hive, etc.)
- Some parts procedurally generated like Elite: rolling from tables for solar systems, economies
- Random elements during gameplay (e.g., constructed robot gets random personality) not necessarily from the seed
- World seed is fixed for procedural generation

The outer space is a backdrop for what's going on inside the ship, and a source for supplies and an end goal. Elite gives a good blueprint. Scripted locations (like the destination) are built into the generated map.

Keep it roguelike. Full variety of events, but never meeting another sentient being.

## Ending
Docking is a reward, a denouement. Being repaired enough to dock is a requirement to get the good ending. This applies whether the story is active or it's just survival/repairs.
