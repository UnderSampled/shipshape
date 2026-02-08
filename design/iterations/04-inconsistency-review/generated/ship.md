# Shipshape - Ship Design

## Ship Variants

Three ships with different features and layouts:

| Ship | Systems | Layout | Character |
|------|---------|--------|-----------|
| **Intrepid** | All online | Drone ship, no human quarters | Clean, functional |
| **Perseverance** | Most offline | Full ship with dormant human areas | Damaged, recoverable |
| **Phoenix** | Antagonistic | Full ship, locked/hostile sections | Threatening, mysterious |

## Ship Systems

Systems adapted for a robot crew (FTL-style):

| System | Function |
|--------|----------|
| Reactor | Power generation |
| Shields | Damage absorption |
| Engines | FTL jump charging, evasion |
| Weapons | Defense against threats |
| Sensors | Detection range, accuracy |
| Doors | Room access control |
| Repair Bay | Robot repairs |
| Charging Stations | Robot power |
| Coolant System | Thermal management |
| Data Core | Robot memory/processing |
| Drone Control | External drones |

Each system has: power_level, health, efficiency, manned_by, online status. Most start offline on the Perseverance.

## Dormant Human Systems

These exist but are offline and unused. They serve as reminders of the absent crew, world-building, and resources for cat care.

- Crew Quarters (empty bunks, personal effects)
- Mess Hall (emergency rations, cat food stored here)
- Bridge (dusty command consoles)
- Medical Bay (could help the cat)
- Recreation Area (the cat's favorite spots)
- Observation Deck (viewports)

## Modules and Hardpoints

Modules attach to hardpoints on ships, stations, and drones, limited by their size. This enables:

- Salvage: find modules at derelicts and depots
- Upgrades: swap modules for better ones
- Customization: configure the ship for the journey ahead
- Damage: individual modules can be damaged or destroyed

Hardpoints have size constraints. A station module won't fit a drone hardpoint.

## Sensors and Actuators

The ship has built-in sensors and actuators that are part of it — things like bulkheads, life support systems, fire suppression systems, mechanical arms. These feel like pieces of the ship's body (from Eli's perspective — the MCP reports them as raw data).

**Sensors**: Fuel levels, long-range detection, hull integrity (strain gauges), proximity sensors, life-signs detectors, environmental monitors, cameras, motion detectors, radiation detectors.

**Actuators**: Bulkhead doors, airlock controls, life support regulators, fire suppression, gravity plating, mechanical cargo arms, docking clamps, emergency shutters.

Sensors are limited in scope by their relationships to other objects in the graph. A sensor can only report what it can physically detect.
