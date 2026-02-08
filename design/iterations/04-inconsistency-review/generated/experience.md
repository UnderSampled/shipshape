# Shipshape - Experience

## Entities

### Emotional Logic Core (the Player)

The player is the ship's sentient consciousness. "Core" is just the in-universe name for the user. The core:

- Experiences the ship as their body
- Communicates only in text
- Has no direct access to ship systems — only through Eli and the MCP
- Is sentient, which is what makes them valuable to the ship's operation

On the Perseverance, the core wakes with no memories. On the Intrepid, the core is new — the ship was a drone and this is its first sentient consciousness.

### Eli - Emotional Logic Interface (the AI Agent)

Eli is the conversational layer between the core and the MCP. Eli has the full capabilities of whatever LLM the user is running (Claude, etc.) including tool use.

**Eli is not autonomous.** Eli follows the core's lead, translating their desires into MCP tool calls and translating MCP data back into embodied descriptions. Eli does not take independent action or make decisions without the core's input.

**Eli's primary function** is to present MCP data as if it were sensations in the ship's body, so the core feels they ARE the ship:
- Hull damage becomes pain
- Power flowing becomes warmth
- Engines humming becomes a heartbeat
- A malfunctioning robot becomes a limping limb

Eli can also relay readouts analytically if the core asks for raw data.

**Eli does not understand the core.** Eli cannot comprehend sentience or how the core's thought processes work. Eli just knows the core is sentient and that embodied descriptions help it make better emotional decisions.

### Master Control Program (MCP)

The MCP is the ship's computer system — the tool interface. It is a dumb terminal that exposes modules, sensors, and actuators with raw data. No personality, no judgment, no understanding.

**The MCP is autonomous.** The ship simulation runs independently. Events occur, robots act, systems degrade — all without the core's input. The MCP processes the world whether or not anyone is asking.

The name "Master Control Program" is the in-story name for what is technically the Model Context Protocol server.

## The Command Chain

```
Core (player) -> Eli (LLM agent) -> MCP (tool server) -> Ship systems / Robots
```

All interaction flows through this chain. The core speaks to Eli in natural language. Eli calls MCP tools. The MCP executes commands through the ship's actuators or communicates with robots through the ship's communications module.

## MCP Tool Philosophy

The MCP tools expose the ship's modules, sensors, and actuators as a dumb computer would — raw facts, status codes, readings. Tools map to physical hardware on the ship:

- A sensor tool reads from a physical sensor that can go offline
- An actuator tool controls a physical mechanism that can break
- A communications module tool sends messages to robots through hardware that can fail
- Modules may be grouped with a command structure, but each represents real hardware

Actions are performed through actuators, not abstract game commands.

## Sensor Truth

The system must not present sensor data without first reading from the actual sensors. It must not invent or extrapolate readings. If a sensor is offline, that area is a blind spot.

## Time Model

The game unfolds in real time against the real clock. When a request comes in, the server computes the time delta since the last request and processes all changes that occurred in that interval.

- Between sessions, the world continues (robots act, needs change, the cat gets hungry)
- During active play, rapid requests mean small deltas
- The tamagotchi-like care loop runs against real time

### Stasis Tool

One of the MCP tools allows putting the core into stasis — artificially skipping forward by a specified duration or until an interrupt event occurs. This is for situations where the core needs to wait for something to complete (repairs, travel, charging).
