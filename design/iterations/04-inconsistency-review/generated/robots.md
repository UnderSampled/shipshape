# Shipshape Robot Design

## Intelligence Tiers
The DF-style robots are one of the more intelligent tiers. They are the crew. Different levels must be represented:

- **Dumb actuators** - Direct execution of specific commands. May use scripted dialogue that is also scripted in-universe.
- **DF-style robots** - Needs, traits, emergent behavior. The crew. Full needs system: power levels, maintenance needs, task priorities, morale-like metrics. Equivalent systems to life support/medbay to keep them running. Since the goal is complex emergent interaction, a full suite.
- **LLM-powered robots** - An even more intelligent tier that actually uses an LLM. Generated dialogue attributed honestly to the robot's tech level.

## Communication
Robots communicate through a physical communications module (an actuator), which can go offline. The core communicates with them through the Eli -> MCP -> actuators chain.

## Honesty
LLM-powered AI can have dialogue it generates. Any problems with generation can honestly be attributed in-game to the peculiarities of the robot's tech — not pretending to be smarter or more sentient than it is. Dumb robots use scripted dialogue that is also scripted in-universe.
