# Shipshape - Game Mechanics

## Core Loop

Manage ship systems, care for your robot crew and cat, and navigate a roguelike journey through increasingly dangerous space to reach your destination.

```
Restore/Manage Systems -> Handle Events -> Care for Crew/Cat -> Navigate -> Repeat
```

## Progression

The game starts with most systems offline (on the Perseverance). Restoring them serves as both tutorial and story progression.

### Phases (Perseverance)

1. **Awakening** - Reactor at minimal power, local sensors only, basic lighting. A few robots waiting for orders.
2. **Mobility** - Door control, internal sensor network, robot charging stations.
3. **Discovery** - Life support partially restored. The cat is discovered (not mentioned before this point).
4. **Defense** - Shields, weapons, improved external sensors.
5. **Journey** - Engines, navigation, FTL jump capability. Destination revealed.
6. **Full Capability** - All restorable systems online. The long journey begins.

Each restored system unlocks new MCP tools and capabilities.

### Intrepid

All systems are online from the start. Progression comes from exploration, upgrades, and the journey itself.

## Ship Systems

FTL-style systems, each with:
- **Power level** (0-100) - How much power is allocated
- **Health** (0-100) - Damage state
- **Efficiency** - Calculated from power, health, and manning
- **Manned by** - Robot IDs operating the system
- **Online** - Whether the system is functional (most start FALSE on Perseverance)

### Active Systems

| System | Function |
|--------|----------|
| Reactor | Power generation |
| Shields | Damage absorption |
| Engines | FTL jump charging, sublight movement |
| Weapons | Combat / defense |
| Sensors | Detection range, accuracy |
| Doors | Room access control, containment |
| Repair Bay | Robot repairs |
| Charging Stations | Robot power |
| Coolant System | Thermal management |
| Data Core | Robot memory, processing |
| Drone Control | External drone deployment |
| Communications | Robot command interface |

### Dormant Passenger Systems

Offline, unused. Reminders of the absent passengers. Resources for cat care.

| System | Story Element |
|--------|---------------|
| Life Support | Needed for the cat |
| Passenger Quarters | Empty bunks, personal effects |
| Mess Hall | Cat food storage |
| Bridge | Dusty consoles |
| Medical Bay | Could help the cat |
| Recreation | Cat's favorite spots |
| Observation Deck | Viewports, benches |

## Power Distribution

Total power is limited by reactor output and health. The player allocates power across systems. Over-allocation is not possible — enabling one system may require reducing another.

## Modules and Hardpoints

Ships, stations, and drones have hardpoints where modules attach, limited by size. Modules can be:
- Found through salvage
- Traded at automated depots
- Swapped between hardpoints
- Damaged or destroyed

This provides the upgrade loop for the roguelike journey.

## Items

### Types
- **Quest items** - Non-fungible, tied to story/discovery
- **Rare artifacts** - Unique finds with special properties
- **Trade goods** - Fungible, for exchange at automated depots
- **Consumable resources** - Fuel, spare parts, raw materials

Items are stored in modules (cargo bays, storage lockers). Trading occurs at automated stations — no sentient merchants.

## Events

All events occur without sentient beings.

### External Events

| Event | Effect |
|-------|--------|
| Asteroid field | Hull damage, shields reduce impact |
| Solar flare | System/sensor damage, robot memory corruption |
| Debris field | Salvage opportunity, navigation hazard |
| Nebula | Sensor interference, shield boost |
| Derelict ship | Salvage, possible automated defenses |
| Automated station | Trading, refueling, information |
| Gravity well | Engine strain, course deviation |
| Radiation storm | Extended exposure, robot memory degradation |

### Internal Events

| Event | Effect |
|-------|--------|
| System malfunction | Degradation, cascading failures |
| Power surge | Damage to systems/robots, possible fires |
| Fire | Spreads through rooms, danger to cat |
| Hull breach | Decompression, atmosphere loss |
| Coolant leak | Thermal failure, area temperature changes |
| Robot malfunction | Erratic behavior, potential damage |
| Cat emergency | Cat stuck, sick, in danger, or hiding |

## Ending

Being repaired enough to dock at the destination is a requirement. Docking is the reward — a denouement. The game ends when you dock. What comes after is implied, not played.

## Difficulty Modes

| | Intrepid | Perseverance | Phoenix |
|---|---------|-------------|---------|
| Systems | All online | Mostly offline | Offline + antagonistic |
| Story | Sandbox exploration | Passengers missing mystery | Full horror/mystery |
| Cat | Present from start | Discovered mid-game | Discovered mid-game |
| Events | Standard | Standard | Escalating + story-driven |
| Communications | Normal | Normal | Degrading |
