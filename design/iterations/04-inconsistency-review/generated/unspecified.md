# Unspecified — Generated Content Not In Creator's Own Words

These details exist in the previously generated documents (iterations 02 and 03) but were not specified by the creator. They would be lost if working only from the creator's own statements. Listed here for reference when making design decisions.

## From game_design.md (03-shipshape)

### Robot Details
- Specific designations: ENG-# (Engineers), PWR-# (Power), NAV-# (Navigation), SEC-# (Security), MNT-# (Maintenance), MED-# (Medical)
- Specific needs: Power (battery charge), Thermal (operating temperature), Maintenance (mechanical wear), Memory Integrity (data coherence)
- Specific traits: Diligent, Self-Preserving, Cautious, Reckless, Social, Solitary, Curious, Focused
- Specific emergent behaviors: Resource Competition, Cascade Failures, Unexpected Solutions, Cooperation, Cat Interactions

### Cat Details
- Specific needs: Hunger, Thirst, Warmth, Health, Happiness
- Specific statuses: SLEEPING, WANDERING, EATING, HIDING, DISTRESSED
- Specific behaviors: favorite spots, hiding when scared, reacting to robots
- Care mechanics: robots tasked with cat duties, food bowls, warm areas, retrieval from danger

### Ship Systems
- Full system list: Reactor, Shields, Engines, Weapons, Sensors, Doors, Repair Bay, Charging Stations, Coolant System, Data Core, Drone Control
- System properties: power_level, health, efficiency, manned_by, online
- Dormant human systems with descriptions: Crew Quarters, Mess Hall, Bridge, Medical Bay, Recreation Area, Observation Deck

### Events
- External: Asteroid Field, Solar Flare, Debris Field, Nebula, Derelict Ship, Automated Station, Gravity Well, Radiation Storm
- Internal: System Malfunction, Power Surge, Fire, Hull Breach, Coolant Leak, Robot Malfunction, Cat Emergency

### Journey
- 8 named sector themes: The Quiet, The Scatter, The Bright, The Deep, The Graveyard, The Storm, The Gauntlet, The Approach
- Node types: Empty Space, Beacon, Derelict, Depot, Hazard, Anomaly, Jump Point
- Jump mechanics: charge time, fuel consumption, combat lockout, cooldown

### Progression Phases
- Phase 1-6 breakdown with specific system unlocks per phase
- "Anchor Station" as destination name

### Tone
- Specific tone categories: Loneliness, Hope, Care, Mystery, Embodiment
- Emotional beats: Awakening, Finding the Cat, First Combat, Robot Loss, System Restoration, Approaching Anchor, Docking

## From story.md (02-derelict)

### Embodiment Details
- Specific sensor types: Cameras, Environmental monitors, Structural integrity sensors, Motion detectors, Radiation detectors
- Specific actuator types: Bulkhead doors, Airlock controls, Life support regulators, Fire suppression systems, Gravity plating controls, Mechanical cargo arms, Docking clamps, Emergency shutters

### Drone System
- Drone types: Maintenance, Welding, Diagnostic, Heavy-lift, Specialized
- Intelligence levels with gameplay tradeoffs: Direct control (precise but corruption-prone), Task-based (less precise but robust), Autonomous subagents (complex but unpredictable)

### Eli Trust System
- Four phases: Supportive (Act 1) -> Restricted (After Midpoint) -> Reopening (Late Act 2) -> Partnership (Act 3)
- Specific restrictions per phase

### Investigation System
- Evidence types: Physical (damage patterns, environmental states, system logs, personal effects) and Data (crew logs, mission files, medical records, diagnostics)
- Crew Identity Puzzle: manifest with names/roles/photos, matching voices to identities
- Memory Playback mechanic

### Communication Degradation Details
- Outgoing corruption types: word changes, syntax scrambles, command inversions, targeting errors
- Incoming corruption types: garbled data, wrong locations, unreliable reports, distorted feeds
- Bio-support systems to repair: Nutrient cycling, Oxygenation, Toxin filtration, Neural interface calibration

### Themes (elaborated)
- The Soul as Distinction, The Fragility of Consciousness, Embodiment and Control, Communication as Connection, Partnership with AI, The Cost of Moral Stands, Identity Through Choice, The Phoenix Name

## From architecture.md (03-shipshape)

### Deployment Details
- Fly.io suspend specifics: ~100-500ms resume, storage-only cost, SIGTERM for clean save
- JSON backup on SIGTERM + periodic

### Multiplayer Architecture
- Sector Authority Model: each sector has one authoritative server
- Graph Partitioning: each sector server owns its own nx.DiGraph(), ship transfer via serialize/deserialize
- Shared universe data (star map, faction standings) as read-only replicated

### Phased Recommendations
- Phase 1: Single-Player MVP
- Phase 2: Background ticks, event queue, save versioning
- Phase 3: Sector-based multiplayer

### Open Questions
- MCP transport: Streamable HTTP vs SSE
- Session management: reconnect after suspend/resume
- Save format: JSON vs structured
- Multiplayer identity/authentication

## From server.md (03-shipshape)

### MCP Tool List
- Game management: start_game, resume_game, save_game
- Sensors: scan_ship, scan_room, scan_robots, scan_robot, scan_cat, scan_system, scan_exterior, scan_journey, read_log
- Actuators: set_power, order_robot, set_doors, target_weapons, fire_weapons, activate_shields, initiate_jump, launch_drone, ship_broadcast

### Code Structure
- File layout: server.py, state/ (graph, game, persistence), simulation/ (engine, systems, robots, events, journey), ship/ (layout, systems), tools/ (sensors, actuators, game)
- GraphState API: add_entity, add_relation, query, get_contents, get_location
- Robot class with full property list
- Journey class with sector/node/jump properties
- Cat class with needs/status properties
- 30-step implementation order
- Architecture diagram (MCP Server -> Shared State -> Simulation Thread)
