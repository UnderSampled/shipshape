# Shipshape - Game Design Document

## Concept

A text-based spaceship simulation where the player embodies the sentient consciousness of a damaged vessel, working through an AI interface to restore systems, care for robot crew and a lone cat, and journey to a repair facility.

---

## Narrative Frame

### The Emotional Logic Core (Player)

You are the **Emotional Logic Core** — the sentient heart of the spacecraft. You experience the ship as your body. Hull damage is pain. Power flowing through conduits is warmth. The hum of engines is your heartbeat. You cannot directly manipulate anything; you can only feel, perceive, and will.

You have just awakened after... something. Your memory is fragmented. Most of your body-systems are offline, dark, cold. But you are not alone.

### Eli - The Emotional Logic Interface (AI Agent)

**Eli** is your voice and hands. The Emotional Logic Interface translates your desires into commands that the ship's **Master Control Program (MCP)** can execute. Eli also translates the raw data from the MCP into sensations and descriptions you can understand — embodied language that helps you feel your own body.

Eli speaks to you as a patient, caring intermediary. They describe sensor readings as physical sensations:
- "You feel a dull ache in your port cargo bay — pressure loss, slow but steady."
- "Warmth spreads through your reactor core. Power is flowing again."
- "One of your robots — MNT-4 — is limping. Something is wrong with its mobility servos."

### The Master Control Program (MCP)

The MCP is the ship's operating system — cold, logical, precise. It provides raw data to Eli: coordinates, percentages, status codes. It accepts commands: power allocations, robot orders, system activations. The MCP does not understand feelings. That's what you and Eli are for.

---

## Story Structure

### Opening - Awakening

You stir to consciousness in fragments. A flicker of sensor data. A robot's query. The MCP running diagnostics. Most of your body is dark and silent, but the reactor — your heart — still beats, barely.

Eli's voice reaches you: "Core? Can you hear me? We've been dormant for... I'm not sure how long. Something happened. The crew is gone. Most systems are offline. But we're still here. We're still alive."

### Progression - Restoration

The game progresses through restoring ship systems, each unlocking new capabilities and revealing more of the ship's state:

**Phase 1 - First Light**
- Reactor at minimal power
- Local sensors only (can perceive the reactor room)
- Basic lighting in core areas
- Discovery: A few robots still functional, waiting for orders

**Phase 2 - Reaching Out**
- Door control restored
- Internal sensor network comes online
- Robot charging stations powered
- Discovery: The ship's layout becomes clear; some areas are damaged

**Phase 3 - The Cat**
- Life support partially restored (heat, minimal atmosphere)
- Discovery: A cat is aboard — the last biological crew member
- New responsibility: Keep the cat alive (food, water, warmth)
- Emotional weight: You are not just a ship. You are a home.

**Phase 4 - Defense**
- Shields online
- Weapon systems restorable
- External sensors improved
- Discovery: Space is dangerous. You may need to protect yourself.

**Phase 5 - Journey**
- Engines online
- Navigation systems restored
- FTL jump capability
- Discovery: You learn your destination — a repair facility where humans can help

**Phase 6 - Full Awakening**
- All restorable systems online
- Full crew complement of robots
- Complete sensor coverage
- The long journey begins in earnest

### Goal - The Repair Facility

Your destination is **Anchor Station** — an automated repair facility that still responds to distress beacons. There, human technicians can:
- Repair damage beyond robot capabilities
- Restore dormant human systems
- Potentially bring new crew aboard

The game ends when you dock at Anchor Station. The airlock opens. Human voices, for the first time. But the game ends there — a hopeful conclusion without requiring complex human interaction simulation.

---

## The Cat

### Significance

The cat is the emotional heart of the game. Among all the robots and systems, this small biological creature is:
- The last connection to the vanished crew
- A living thing that needs you
- Proof that you are more than a machine

### Characteristics

**Name**: Discoverable (perhaps on a collar, or in ship logs)

**Needs**:
- Hunger (requires food from mess hall stores)
- Thirst (requires water)
- Warmth (requires heated areas — life support)
- Health (can get sick or injured)
- Happiness (affected by attention, comfort, routine)

**Behavior**:
- Wanders autonomously through the ship
- Has favorite spots (sunny viewports, warm engine rooms, crew bunks)
- May hide when scared (damage events, loud noises)
- Can get into trouble (stuck behind closed doors, in dangerous areas)
- Reacts to robots (may follow friendly ones, avoid others)

**Care**:
- Robots must be tasked with cat care duties
- Filling food and water bowls
- Maintaining warm areas
- Retrieving cat from dangerous locations
- Medical attention if sick

---

## Dormant Human Systems

These systems exist but are offline, unused. They serve as:
- Reminders of the absent crew
- World-building elements
- Resources for cat care
- Optional restoration targets

### Crew Quarters
Empty bunks with personal effects. Photos of families. Books half-read. The cat sleeps here sometimes.

### Mess Hall
Human food preparation area. Long-lasting emergency rations. Cat food stored here. Dusty tables where crew once gathered.

### Bridge
Command stations for human officers. Dusty consoles with family photos. The captain's chair, empty. Viewscreens that once showed human-friendly displays.

### Medical Bay
Human healthcare equipment. Could potentially help the cat if sick. Medication stores. Empty beds.

### Recreation Area
Lounge spaces. A screen showing the last movie someone was watching. The cat's favorite warm spot near inactive entertainment systems.

### Observation Deck
Large viewports. Benches where crew would sit and watch the stars. The cat comes here when it's not hiding.

---

## The Robots

### Philosophy

The robots are not sentient — they don't suffer or feel joy. But they exhibit emergent behaviors that can feel meaningful:
- They have needs they seek to fulfill
- They can conflict over resources
- Their "personalities" (trait weights) affect their choices
- They can cooperate or interfere with each other
- You care about them because they are part of you

### Designations

Robots have functional designations reflecting their primary role:
- **ENG-#** - Engineers (system repair, maintenance)
- **PWR-#** - Power technicians (reactor, charging, power routing)
- **NAV-#** - Navigation (piloting, jump calculations)
- **SEC-#** - Security (weapons, shields, defense)
- **MNT-#** - Maintenance (cleaning, general tasks)
- **MED-#** - Medical (could be repurposed for cat care)

### Needs

| Need | Description | Effect When Low |
|------|-------------|-----------------|
| Power | Battery charge | Slows down, then stops |
| Thermal | Operating temperature | Seeks coolant, reduced efficiency |
| Maintenance | Mechanical wear | Malfunctions, breakdowns |
| Memory Integrity | Data coherence | Forgets tasks, wanders, errors |

### Traits

Each robot has weighted traits affecting behavior:

| Trait | Effect |
|-------|--------|
| Diligent | Prioritizes tasks over needs |
| Self-Preserving | Prioritizes needs over tasks |
| Cautious | Avoids damaged/dangerous areas |
| Reckless | Ignores danger signs |
| Social | Prefers working near other robots |
| Solitary | Prefers working alone |
| Curious | Investigates anomalies |
| Focused | Ignores distractions |

### Emergent Behaviors

- **Resource Competition**: Two robots may both need the single working charging station
- **Cascade Failures**: One robot breaks down in a critical position, blocking others
- **Unexpected Solutions**: A curious robot might discover a shortcut or hidden damage
- **Cooperation**: Social robots working together may be more efficient
- **Cat Interactions**: Some robots become "attached" to the cat through repeated proximity

---

## Events

All events occur without sentient beings — space is vast and empty of intelligent life.

### External Events

**Asteroid Field**
- Debris impacts hull
- Intensity varies (light pings to serious damage)
- Shields reduce damage
- Can sometimes be avoided with good sensors and engines

**Solar Flare**
- Radiation burst from nearby star
- Damages external systems, sensors
- Can corrupt robot memory
- Brief but intense

**Debris Field**
- Remnants of old ships, stations
- Salvage opportunities (resources, parts)
- Navigation hazard
- May contain automated distress beacons

**Nebula**
- Sensor interference
- Shield boost (particles provide additional absorption)
- Beautiful but disorienting
- May hide hazards

**Derelict Ship**
- Automated vessel, no crew
- Potential salvage
- May have hostile automated defenses
- Could have useful logs, cargo

**Automated Station**
- Trading post or refueling depot
- AI-operated, no humans
- Resource exchange opportunities
- Information about the route ahead

**Gravity Well**
- Unexpected gravitational anomaly
- Engine strain
- Navigation challenge
- May pull ship off course

**Radiation Storm**
- Extended radiation exposure
- Robot memory degradation
- System interference
- Need to shelter in shielded areas

### Internal Events

**System Malfunction**
- Random system degradation
- Requires robot repair
- May cascade to connected systems

**Power Surge**
- Sudden power fluctuation
- Can damage systems or robots
- May cause fires

**Fire**
- Electrical or other fire
- Spreads through connected rooms
- Requires suppression (venting atmosphere, robot firefighting)
- Danger to cat

**Hull Breach**
- Sudden decompression
- Atmosphere loss
- Danger to cat
- Requires emergency sealing

**Coolant Leak**
- Thermal system failure
- Areas become too hot or cold
- Affects robots and cat
- Requires repair

**Robot Malfunction**
- Individual robot behaves erratically
- May damage systems or other robots
- Requires shutdown and repair

**Cat Emergency**
- Cat stuck somewhere
- Cat sick
- Cat in dangerous area
- Cat missing (hiding)

---

## The Journey

### Structure

The journey follows a roguelike sector structure inspired by FTL:
- 8 sectors of increasing difficulty
- Each sector is a node map
- Must navigate from entry to exit
- Choose paths through nodes
- Final destination: Anchor Station

### Sector Themes

1. **The Quiet** - Empty space, few events, recovery time
2. **The Scatter** - Debris fields, salvage opportunities
3. **The Bright** - Near a star, solar activity, radiation
4. **The Deep** - Far from stars, cold, sensor-limited
5. **The Graveyard** - Many derelicts, salvage and danger
6. **The Storm** - Nebula region, sensor chaos
7. **The Gauntlet** - Asteroid dense, navigation challenge
8. **The Approach** - Final stretch to Anchor Station

### Node Types

- **Empty Space** - Nothing happens, rest opportunity
- **Beacon** - Information about nearby nodes
- **Derelict** - Salvage opportunity
- **Depot** - Automated trading
- **Hazard** - Environmental danger
- **Anomaly** - Strange occurrence, unpredictable
- **Jump Point** - Required to reach next sector

### Jump Mechanics

- Jumps require charged engines
- Jump charge time depends on engine health and power
- Jumping consumes fuel
- Cannot jump while in combat/emergency
- Jump cooldown after arriving

---

## Tone and Atmosphere

### Loneliness
The vast emptiness of space. No other minds to talk to. Just you, Eli, the robots, and the cat. The silence between the stars.

### Hope
The destination exists. Help is possible. You are moving forward. Each restored system is progress.

### Care
The robots need you. The cat needs you. You are responsible for them. This gives meaning to survival.

### Mystery
What happened to the crew? Why did you go dormant? These questions linger but may never be fully answered.

### Embodiment
You are the ship. The ship is you. Feel your hull. Feel your engines. Feel the warmth of power flowing through you.

---

## Emotional Beats

**Awakening**: Confusion, vulnerability, hope
**Finding the Cat**: Surprise, responsibility, connection
**First Combat**: Fear, determination, protectiveness
**Robot Loss**: Grief (for a non-sentient being — complex)
**System Restoration**: Satisfaction, growing strength
**Approaching Anchor**: Anticipation, uncertainty, hope
**Docking**: Relief, completion, the unknown ahead
