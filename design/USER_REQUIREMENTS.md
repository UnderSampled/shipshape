# User Requirements - Verbatim

## Initial Request

> Make an MCP server that exposes an interface to a virtual spaceship's computer control system, while a separate thread simulates the spaceship in real-time, with dwarf-fortress emergent interactions (use simple robots as the characters, instead of sentient creatures), FTL style systems, events, and challenges, and MUD style prepositional relationships (store state, including locations, in a graph structure). The MCP server will be the player's only interraction with this virtual spaceship.

## Clarifications

### On robot needs (when asked about life support/medbay)

> The droids don't have a need for life support, or a medbay, but there should be equivalent things to need to keep running for their sake. Since the goal is complex emergent interraction, a full suite is good.

### On narrative framing (when asked about MCP interface structure and events)

> The frame story will be that the user is the ship's "Emotional Logic Core" — the sentient part of the ship. the AI agent using the MCP is the "Emoti9nal Logic Interface", or "Eli". Eli will translate the user's requests into calls read from sensors and use actuators. In order for the core to make the best decisions, Eli translates the sensor readings into descriotions such that the core feels like the ship is it's body. This would all be explained to the LLM through MCP commands to start or resume the game.

*[Note: "Emoti9nal" appears to be a typo for "Emotional"]*

### On events and embodiment (answering multiple choice questions)

> A Full variety, but never meeting another sentient being, to be true to life.

*[Context: When asked what kind of events/challenges should occur]*

> Roguelike journey

*[Context: When asked about game mode - sandbox vs mission-based vs roguelike]*

> Eli should be instructed to do the translation — the MCP would just supply the computer-like data readouts.

*[Context: When asked how detailed the embodied descriptions should be - clarifying that MCP gives raw data, Eli translates]*

### Additional story and gameplay notes (after seeing the initial plan)

> Two more notes: The MCP tools and server (normally 'model control protocol') is known to Eli in the story as the 'Master Control Program'. The game starfs with most of the systems offline, and restoring them is a story progression/goal, while also being a tutorial sequence (amd allowing the systems themselves to be more complex to learn how to manage.) The eventual goal would be to dock at a repairbfacility where humans can actually fix yoir deeper issues and get people back on board (but the game ebds before any interraction with actual people). Perhaps human-centered systems can also be found in the ship, lying dormant/unused. Maybe there's a cat to keep alive.

*[Note: Contains typos - "starfs" = "starts", "amd" = "and", "repairbfacility" = "repair facility", "yoir" = "your", "ebds" = "ends"]*

### Technology choices (from multiple choice answers)

> Python (Recommended)

*[Context: When asked what programming language to use]*

> Full needs system

*[Context: When asked about robot AI complexity - chose "Robots have power levels, maintenance needs, task priorities, morale-like metrics"]*
