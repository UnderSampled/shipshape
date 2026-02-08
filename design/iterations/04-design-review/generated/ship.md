# Shipshape - Ship Design

## Ship as Body

The ship is the core's body. Every system, sensor, and actuator is a part of that body. When systems are offline, those areas are numb — the core can't feel them. When sensors come online, it's like gaining sight. When actuators respond, it's like moving a limb. Eli translates all of this into embodied language; the MCP just reports facts.

## Ship Variants

Each difficulty mode has its own ship with potentially different layouts and features:

- **Intrepid** - Drone ship. Compact, efficient, no human-oriented spaces. All systems online.
- **Perseverance** - Personnel ship. Full layout with passenger areas (dormant). Most systems offline at start.
- **Phoenix** - Same as Perseverance but with additional locked/antagonistic systems. Deferred.

## Rooms and Layout

The ship is a graph of rooms connected by doors/corridors. Each room is a node with attributes (atmosphere, temperature, lighting, power state). Connections are edges with properties (door state, structural integrity).

### Core Areas (all ships)

- **Reactor Room** - Heart of the ship. Power generation.
- **Engineering** - System repair and maintenance. Repair bay.
- **Sensor Array** - Central sensor processing.
- **Weapons Bay** - Weapons systems and targeting.
- **Shield Generator** - Shield systems.
- **Engine Room** - Sublight and FTL engines.
- **Navigation** - Star charts, jump calculations.
- **Data Core** - Central computing, robot memory sync.
- **Charging Bay** - Robot charging stations.
- **Coolant Processing** - Thermal management.
- **Drone Bay** - External drone launch and storage.
- **Cargo Hold** - Item storage, trade goods.
- **Communications Hub** - Robot command interface, external comms.

### Passenger Areas (Perseverance / Phoenix only)

- **Passenger Quarters** - Empty bunks, personal effects.
- **Mess Hall** - Food preparation, cat food storage.
- **Bridge** - Officer command stations, captain's chair.
- **Medical Bay** - Healthcare equipment, medication.
- **Recreation Area** - Lounge, entertainment systems.
- **Observation Deck** - Viewports, benches.
- **Life Support** - Atmosphere, temperature for biologicals.

## Systems

Each system is a node in the graph with attributes:

```
power_level:  0-100  (allocated power)
health:       0-100  (damage state)
efficiency:   computed from power, health, manning
manned_by:    [robot_ids]
online:       bool
```

Systems consume power from the reactor. Total allocation cannot exceed reactor output. Damaged systems have reduced efficiency even at full power.

## Modules and Hardpoints

Ships have hardpoints — physical mounting points of specific sizes. Modules attach to hardpoints.

### Hardpoint Sizes

- **Small** - Utility modules, minor sensors, point defense
- **Medium** - Standard weapons, sensor arrays, cargo pods
- **Large** - Heavy weapons, main engines, large cargo

### Module Types

- **Weapons** - Auto-cannons, missile launchers, beam weapons
- **Sensors** - Short/long range, specialized (life signs, radiation, etc.)
- **Cargo** - Storage containers of varying size
- **Utility** - Repair arms, tractor beams, mining equipment
- **Defense** - Shield projectors, armor plating, countermeasures

Modules can be:
- Salvaged from derelicts
- Traded at automated depots
- Damaged or destroyed in combat/events
- Swapped between compatible hardpoints

## Sensors (Perception)

Sensors are physical hardware that can go offline. Each sensor has a type, range, and condition. The MCP can only report what functioning sensors detect.

- **Internal cameras** - Visual monitoring of rooms
- **Environmental monitors** - Temperature, pressure, atmosphere composition
- **Structural integrity sensors** - Hull stress, breach detection
- **Motion detectors** - Movement within rooms
- **Radiation detectors** - Radiation levels
- **Fuel level sensors** - Tank readings
- **External sensors** - Long-range detection, short-range scanning (module-based)
- **Life signs detector** - Biological presence detection
- **Proximity sensors** - Near-hull object detection

## Actuators (Action)

Actuators are physical mechanisms that can break. The MCP sends commands; actuators execute them.

- **Bulkhead doors** - Open, close, lock
- **Airlock controls** - Cycling, emergency seal
- **Life support regulators** - Atmosphere mix, temperature
- **Fire suppression systems** - Foam, venting
- **Gravity plating controls** - Per-room gravity
- **Mechanical cargo arms** - Loading, moving heavy objects
- **Docking clamps** - Station attachment
- **Emergency shutters** - Blast protection, breach isolation

## Power Distribution

The reactor generates a total power budget. The player allocates power to systems. Trade-offs are constant:
- More power to shields means less for engines
- Charging robots draws from the same pool
- Damaged reactor = reduced total budget
- Some systems have minimum power thresholds to function at all
