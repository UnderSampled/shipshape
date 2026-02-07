# Spaceship MCP Server - Implementation Plan

## Overview

A Python MCP server exposing a virtual spaceship's computer system. A separate thread simulates the spaceship in real-time with:
- **Dwarf Fortress-style** emergent robot interactions
- **FTL-style** ship systems and roguelike journey
- **MUD-style** graph-based location/relationship storage

### Narrative Frame
- **User** = "Emotional Logic Core" (ship's sentient consciousness)
- **AI Agent (Eli)** = "Emotional Logic Interface" (translates between Core and ship systems)
- **MCP** = "Master Control Program" (in-story name for the tool interface)
- **MCP Tools** = Raw sensor data and actuator commands (Eli translates to embodied descriptions)

### Story Structure
- **Start state**: Most systems offline, ship damaged/dormant
- **Progression**: Restoring systems one by one (tutorial + story advancement)
- **Goal**: Reach a repair facility where humans can fix the ship and return crew
- **Ending**: Game ends upon docking - no direct human interaction
- **The Cat**: One biological life form aboard (ship's cat) - requires food, water, warmth
- **Dormant Human Systems**: Crew quarters, mess hall, bridge stations, life support - all offline, haunting reminders

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      MCP Server                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Sensors   │  │  Actuators  │  │  Game Management    │  │
│  │  (read)     │  │  (write)    │  │  start/resume/save  │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
└─────────┼────────────────┼────────────────────┼─────────────┘
          │                │                    │
          ▼                ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    Shared Game State                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              Graph State Store (NetworkX)            │    │
│  │  - Rooms/locations as nodes                          │    │
│  │  - Connections as edges with prepositions            │    │
│  │  - Robots, items, systems as nodes with relations    │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐               │
│  │Ship Systems│ │   Robots   │ │  Journey   │               │
│  │ (FTL-style)│ │  (DF-style)│ │  (sectors) │               │
│  └────────────┘ └────────────┘ └────────────┘               │
└─────────────────────────────────────────────────────────────┘
          ▲
          │ Thread-safe access (RLock)
          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Simulation Thread                           │
│  - Runs at fixed tick rate (e.g., 1 tick/second)            │
│  - Updates robot needs, positions, tasks                     │
│  - Processes system states (power, damage, etc.)            │
│  - Generates events                                          │
│  - Advances journey when jumping                             │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
shipshape/
├── pyproject.toml           # Project config, dependencies
├── README.md                 # Setup instructions
├── src/
│   └── shipshape/
│       ├── __init__.py
│       ├── server.py         # MCP server entry point
│       ├── state/
│       │   ├── __init__.py
│       │   ├── graph.py      # Graph state store (NetworkX)
│       │   ├── game.py       # Game state container
│       │   └── persistence.py # Save/load game state
│       ├── simulation/
│       │   ├── __init__.py
│       │   ├── engine.py     # Main simulation loop thread
│       │   ├── systems.py    # Ship systems (FTL-style)
│       │   ├── robots.py     # Robot entities and AI
│       │   ├── events.py     # Event generation and processing
│       │   └── journey.py    # Sector/jump progression
│       ├── ship/
│       │   ├── __init__.py
│       │   ├── layout.py     # Ship room definitions
│       │   └── systems.py    # System definitions and behaviors
│       └── tools/
│           ├── __init__.py
│           ├── sensors.py    # Read-only sensor tools
│           ├── actuators.py  # Action/command tools
│           └── game.py       # start_game, resume_game, save_game
```

---

## Core Components

### 1. Graph State Store (`state/graph.py`)

MUD-style prepositional relationships using NetworkX:

```python
# Node types: room, robot, item, system
# Edge types with prepositions: "in", "on", "connected_to", "north_of", etc.

class GraphState:
    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def add_entity(self, entity_id, entity_type, **attributes)
    def add_relation(self, subject, predicate, object)  # "robot_1", "in", "engine_room"
    def query(self, subject=None, predicate=None, object=None)
    def get_contents(self, location_id)  # What's in this room?
    def get_location(self, entity_id)    # Where is this entity?
```

### 2. Ship Systems (`simulation/systems.py`)

FTL-style systems adapted for robots:

| System | Function | Robot Equivalent |
|--------|----------|------------------|
| **Reactor** | Power generation | Powers all systems |
| **Shields** | Damage absorption | Hull protection |
| **Engines** | FTL jump charging, evasion | Movement/escape |
| **Weapons** | Combat | Defense against threats |
| **Sensors** | Detection range, accuracy | Awareness |
| **Doors** | Room access control | Containment |
| **Repair Bay** | Robot repairs | Instead of medbay |
| **Charging Stations** | Robot power | Instead of O2 |
| **Coolant System** | Thermal management | Prevents overheating |
| **Data Core** | Robot memory/processing | Cognitive functions |
| **Drone Control** | External drones | Repairs, combat |

Each system has:
- `power_level` (0-100, how much power allocated)
- `health` (0-100, damage state)
- `efficiency` (calculated from power, health, manning)
- `manned_by` (robot IDs operating it)
- `online` (bool - most start FALSE)

### Dormant Human Systems (offline, unused)
| System | Purpose | Story Element |
|--------|---------|---------------|
| **Life Support** | O2, temperature for humans | Needed only for the cat |
| **Crew Quarters** | Human sleeping areas | Empty bunks, personal effects |
| **Mess Hall** | Human food preparation | Cat food storage here |
| **Bridge** | Human command stations | Dusty consoles |
| **Medical Bay** | Human healthcare | Could help the cat if sick |
| **Recreation** | Human entertainment | The cat's favorite spots |

### The Cat
```python
class Cat:
    name: str              # Discoverable, maybe on collar
    location: str          # Wanders the ship
    hunger: float          # 0-100, needs food
    thirst: float          # 0-100, needs water
    warmth: float          # 0-100, needs heated areas
    health: float          # 0-100
    happiness: float       # Affects where it goes
    status: CatStatus      # SLEEPING, WANDERING, EATING, HIDING, DISTRESSED
```
- Cat is found early in the game (perhaps triggers life support restoration)
- Robots must be tasked with cat care (filling food bowl, maintaining warm areas)
- Cat wanders autonomously, may get into trouble (stuck in rooms, near hazards)
- Keeping cat alive is an emotional anchor for the journey

### Tutorial/Progression System
Game starts with only basic systems online:
1. **Phase 1 - Awakening**: Reactor (minimal), Sensors (local only), basic lighting
2. **Phase 2 - Mobility**: Doors, internal sensors, robot charging
3. **Phase 3 - Discovery**: Find the cat, restore partial life support
4. **Phase 4 - Defense**: Shields, basic weapons
5. **Phase 5 - Journey**: Engines, navigation, jump capability
6. **Phase 6 - Full Capability**: All systems restorable

Each restored system unlocks new MCP tools/capabilities.

### 3. Robot Simulation (`simulation/robots.py`)

Dwarf Fortress-style needs and behaviors:

```python
class Robot:
    # Identity
    id: str
    designation: str  # "MNT-7", "PWR-3"
    role: RobotRole   # ENGINEER, GUNNER, PILOT, REPAIR, GENERAL

    # Needs (0-100, lower = more urgent)
    power_level: float      # Need to charge
    thermal_level: float    # Need cooling
    maintenance: float      # Need repairs
    memory_integrity: float # Need data core sync

    # State
    location: str           # Room ID
    current_task: Task | None
    task_queue: list[Task]
    status: RobotStatus     # IDLE, WORKING, CHARGING, REPAIRING, DISABLED

    # Personality (affects emergent behavior)
    traits: list[Trait]     # DILIGENT, CAUTIOUS, RECKLESS, SOCIAL, etc.
```

**Emergent behaviors:**
- Robots prioritize needs vs assigned tasks
- Robots can conflict over resources (charging stations, repair bay)
- Robots form "relationships" through proximity and cooperation
- Damaged robots may malfunction, cause accidents
- Robots with low memory_integrity may "forget" tasks or wander

### 4. Event System (`simulation/events.py`)

Events with no sentient beings:

**External Events:**
- Asteroid field (hull damage risk)
- Solar flare (system damage, sensor interference)
- Debris field (salvage opportunities)
- Distress beacon (automated, derelict ships)
- Nebula (sensor reduction, shield boost)
- Gravity well (engine strain)
- Radiation storm (robot memory corruption)

**Internal Events:**
- System malfunction
- Power surge/shortage
- Robot conflict (resource competition)
- Fire/electrical hazard
- Hull breach
- Coolant leak

**Journey Events:**
- Beacon discovery
- Derelict ship encounter
- Space station (automated trading post)
- Jump point anomaly

### 5. Journey System (`simulation/journey.py`)

Roguelike sector progression:

```python
class Journey:
    current_sector: int          # 1-8
    current_node: str            # Position in sector map
    sector_map: dict             # Generated nodes and connections
    destination: str             # Final goal
    threat_level: float          # Increases per sector

    # Jump mechanics
    jump_charge: float           # 0-100
    jump_cooldown: float         # Time until can jump again
```

---

## MCP Tools

### Game Management Tools

**`start_game`** - Returns Eli's instructions and initial state
```python
# Returns:
{
    "eli_instructions": """You are Eli, the Emotional Logic Interface,
        speaking to the ship's Emotional Logic Core - the sentient
        consciousness of this vessel. The Core experiences the ship
        as its body. Translate all sensor data into embodied
        descriptions: hull damage is pain, power flow is warmth,
        the robots are like nerve impulses or blood cells...

        The Master Control Program (MCP) provides raw data. Your role
        is to help the Core understand and feel its own body-ship.

        The ship has suffered damage. Most systems are offline.
        Somewhere aboard, a cat survives - the last biological
        crew member. The goal: reach a repair facility where
        humans can restore what the robots cannot fix.""",
    "ship_name": "...",
    "initial_status": { ... },  # Most systems: online=False
    "awakening_prompt": "You feel yourself stirring to awareness..."
}
```

**`resume_game`** - Load saved state, return Eli instructions + current status

**`save_game`** - Persist current state

### Sensor Tools (Read-only)

**`scan_ship`** - Overview of all systems, power, hull integrity
**`scan_room`** - Contents and state of a specific room
**`scan_robots`** - Status of all robots (location, task, needs)
**`scan_robot`** - Detailed status of one robot
**`scan_cat`** - Cat's location, needs, status (once discovered)
**`scan_system`** - Detailed status of one ship system
**`scan_exterior`** - What's outside (current sector node, nearby objects)
**`scan_journey`** - Sector progress, jump status, map
**`read_log`** - Recent events and alerts

### Actuator Tools (Actions)

**`set_power`** - Allocate power to systems
**`order_robot`** - Assign task to robot
**`set_doors`** - Open/close/lock doors
**`target_weapons`** - Aim at external threat
**`fire_weapons`** - Attack
**`activate_shields`** - Shield configuration
**`initiate_jump`** - Begin FTL jump to connected node
**`launch_drone`** - Deploy drone for task
**`ship_broadcast`** - Announce to all robots (affects morale/coordination)

---

## Implementation Order

### Phase 1: Foundation
1. Project setup (pyproject.toml, structure)
2. Graph state store with basic operations
3. Game state container with online/offline system tracking
4. Basic MCP server skeleton

### Phase 2: Ship Structure
5. Ship layout (rooms, connections) - including dormant human areas
6. Ship systems definitions (with online=False defaults for most)
7. Power distribution logic
8. System restoration mechanics

### Phase 3: Entities
9. Robot class with needs
10. Basic robot AI (need prioritization)
11. Task system
12. Cat class with needs and wandering behavior

### Phase 4: Simulation
13. Simulation thread with tick loop
14. System updates per tick
15. Robot updates per tick
16. Cat updates per tick
17. Thread-safe state access

### Phase 5: Events & Journey
18. Event generation (scaled to available systems)
19. Event effects
20. Sector map generation
21. Jump mechanics
22. Progression triggers (system restoration unlocks)

### Phase 6: MCP Tools
23. Sensor tools (gated by system availability)
24. Actuator tools (gated by system availability)
25. Game management tools (start_game with Eli instructions)
26. Cat care tools

### Phase 7: Polish
27. Save/load persistence
28. Balance tuning
29. Tutorial/awakening sequence
30. Error handling

---

## Verification

1. **Run MCP server**: `python -m shipshape.server`
2. **Test with MCP inspector or Claude**: Connect and call `start_game`
3. **Verify simulation runs**: Check that `scan_ship` returns changing values over time
4. **Test robot behavior**: Observe robots moving to charge when low on power
5. **Test events**: Wait for random events, verify they affect state
6. **Test journey**: Initiate jump, verify sector progression

---

## Dependencies

```toml
[project]
dependencies = [
    "mcp>=1.0.0",
    "networkx>=3.0",
    "pydantic>=2.0",
]
```

---

## Key Design Decisions

1. **NetworkX for graph** - Mature, well-tested, supports multi-edges for multiple relationships
2. **Pydantic for models** - Validation, serialization for save/load
3. **RLock for thread safety** - Allows nested locking from same thread
4. **1 tick/second simulation** - Balance between responsiveness and CPU usage
5. **Raw data from MCP** - Eli (LLM) handles embodied translation per instructions in start_game
