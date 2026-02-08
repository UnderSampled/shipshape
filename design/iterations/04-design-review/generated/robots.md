# Shipshape - Robots

## Philosophy

Robots are the ship's crew. They are not sentient — they don't suffer or feel joy. But they exhibit emergent behaviors from simple needs and traits that can feel meaningful. The player cares about them because they are part of the ship's body.

Robots exist at multiple intelligence tiers, from dumb actuators to LLM-powered agents. The honesty principle applies: each tier's dialogue and behavior honestly reflects its actual capability.

## Intelligence Tiers

### Tier 0: Simple Actuators

Direct execution of specific commands. No autonomy, no dialogue. Mechanical arms, welding torches, basic repair tools.

- Controlled entirely through MCP actuator commands
- No decision-making capability
- Example: "Cut this panel," "Weld this seam"

### Tier 1: Scripted Units

Pre-programmed routines. Canned responses. Can complete defined tasks but cannot adapt.

- Follow programmed sequences
- Use scripted dialogue that is also scripted in-universe ("TASK COMPLETE," "ERROR: OBSTRUCTION DETECTED")
- No emergent behavior
- Example: A cleaning bot that follows a fixed route

### Tier 2: Autonomous Robots (DF-style)

The core crew. Needs-driven, trait-weighted decision-making. This is where Dwarf Fortress-style emergent behavior happens.

- Have needs they seek to fulfill
- Have personality traits that weight their decisions
- Can conflict over resources, cooperate, form proximity-based affinities
- Communicate through the ship's communications module
- Their dialogue is simple, functional, generated from templates with variation
- Example: ENG-3 prioritizes repairing the reactor over charging because it has the Diligent trait

### Tier 3: LLM-Powered Agents

The most intelligent robots. Use an LLM to generate dialogue and make complex decisions. Their speech is honest — an AI talking like an AI, with any quirks attributable to their technology.

- Can problem-solve within defined parameters
- Generate natural dialogue through an LLM
- Can be conversed with through the communications module
- Any oddities in their responses are honestly their robot's AI being imperfect
- Example: A sophisticated engineering unit that can explain what it's doing and why, discuss repair strategies, and adapt to unexpected situations

## Designations

Robots have functional designations reflecting their primary role:

| Prefix | Role | Typical Tier |
|--------|------|-------------|
| ENG-# | Engineers (system repair, maintenance) | 2-3 |
| PWR-# | Power technicians (reactor, charging, routing) | 2 |
| NAV-# | Navigation (piloting, jump calculations) | 2-3 |
| SEC-# | Security (weapons, shields, defense) | 2 |
| MNT-# | Maintenance (cleaning, general tasks) | 1-2 |
| MED-# | Medical (repurposed for cat care) | 2 |
| DRN-# | Drones (external operations) | 1-2 |

## Needs (Tier 2+)

Needs range from 0-100. Lower values are more urgent.

| Need | Description | Effect When Low |
|------|-------------|-----------------|
| Power | Battery charge | Slows down, then stops. Seeks charging station. |
| Thermal | Operating temperature | Reduced efficiency. Seeks coolant. |
| Maintenance | Mechanical wear | Malfunctions, breakdowns. Seeks repair bay. |
| Memory Integrity | Data coherence | Forgets tasks, wanders, errors. Seeks data core sync. |

## Traits (Tier 2+)

Each robot has weighted traits that affect behavior priorities:

| Trait | Opposite | Effect |
|-------|----------|--------|
| Diligent | Self-Preserving | Prioritizes tasks over own needs |
| Cautious | Reckless | Avoids damaged/dangerous areas |
| Social | Solitary | Prefers working near other robots |
| Curious | Focused | Investigates anomalies vs. ignores distractions |

Traits are weighted, not binary. A robot can be somewhat cautious and very diligent.

Constructed robots receive random trait weights — this is runtime randomness, not seeded.

## Emergent Behaviors

These are not scripted — they emerge from the needs/traits simulation:

- **Resource Competition** - Two robots both need the single working charging station
- **Cascade Failures** - A robot breaks down in a doorway, blocking others
- **Unexpected Solutions** - A curious robot investigates an anomaly and discovers hidden damage
- **Cooperation** - Social robots near each other work more efficiently
- **Cat Affinities** - Robots with repeated cat proximity develop behavioral patterns around it
- **Priority Conflicts** - A diligent robot ignores low power to finish a critical repair, then shuts down in a bad location

## Communication

Robots are communicated with through the ship's communications module — a physical piece of hardware that can go offline. Commands flow through the chain:

```
Core -> Eli -> MCP -> Communications Module -> Robot
```

If the communications module is offline or damaged, robots cannot receive new orders (though autonomous robots continue acting on their current priorities).

## Robot Construction

If materials and facilities are available, new robots can be constructed. Constructed robots:
- Have a random personality (traits)
- Start at a base intelligence tier determined by available technology
- Must be given a designation and role
