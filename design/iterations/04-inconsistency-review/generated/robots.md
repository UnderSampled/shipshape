# Shipshape - Robots

## Intelligence Tiers

The robots have varying levels of AI. The DF-style robots are just one of the more intelligent tiers. They are indeed the crew. The different levels must be represented:

| Tier | Description | Dialogue | Example |
|------|-------------|----------|---------|
| **Dumb actuators** | Direct execution of specific commands | Scripted in-universe responses only | Cut this panel, weld this seam |
| **Basic autonomous** | Complete simple tasks with general instructions | Simple status reports, scripted | Clear debris from corridor C |
| **DF-style crew** | Needs, traits, emergent behavior, task prioritization | Generated but honest — attributed to the robot's tech | ENG-3, MNT-7, PWR-2 |
| **LLM-powered** | Full conversational AI, complex problem-solving | LLM-generated, explicitly non-sentient | Sophisticated subagents |

Communication with robots goes through a physical communications module (which can go offline), via the Eli → MCP → actuators chain.

## Needs (DF-style and above)

| Need | Description | Effect When Low |
|------|-------------|-----------------|
| Power | Battery charge | Slows down, then stops |
| Thermal | Operating temperature | Seeks coolant, reduced efficiency |
| Maintenance | Mechanical wear | Malfunctions, breakdowns |
| Memory Integrity | Data coherence | Forgets tasks, wanders, errors |

## Traits (DF-style and above)

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

If we construct a robot during play, it might have a random personality. This is not generated from the world seed — it happens chaotically during the game.

## Designations

Robots have functional designations reflecting their primary role:

- **ENG-#** - Engineers (system repair, maintenance)
- **PWR-#** - Power technicians (reactor, charging, power routing)
- **NAV-#** - Navigation (piloting, jump calculations)
- **SEC-#** - Security (weapons, shields, defense)
- **MNT-#** - Maintenance (cleaning, general tasks)
- **MED-#** - Medical (repurposed for cat care)

## Emergent Behaviors

- Resource competition (two robots need the single working charging station)
- Cascade failures (one breaks down in a critical position, blocking others)
- Unexpected solutions (a curious robot discovers a shortcut or hidden damage)
- Cooperation (social robots working together are more efficient)
- Cat interactions (some robots become "attached" through repeated proximity)

## The Honesty Principle for Robots

Robots are not sentient — they don't suffer or feel joy. But they exhibit emergent behaviors that can feel meaningful. Any dialogue a robot generates is honest: an LLM-powered AI can have dialogue, and any problems with its generation can honestly be attributed in-game to the peculiarities of the robot's tech. No robot pretends to be smarter or more sentient than it is.
