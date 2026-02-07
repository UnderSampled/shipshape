# Shipshape Ship Design

## Ship Modes

| Ship | Difficulty | Mode | State | Crew |
|------|-----------|------|-------|------|
| **Intrepid** | Easy | Exploration sandbox | All systems online | Drone ship, never meant for people |
| **Perseverance** | Normal | Survival adventure | Systems offline | Crew missing |
| **Phoenix** | Hard | Horror/mystery | Antagonistic systems, communications issues | Crew dead |

Start with the first two.

## Modules and Hardpoints
Modules attach to hardpoints on ships, stations, and drones, limited by their size.

The MCP tools expose modules, sensors, and actuators directly. Modules may be grouped with a command structure. Any module can go offline.

## Sensors
Sensors are how actors perceive the graph. The raw state is not read directly. Actors interact through sensors, which are limited in scope by their relationships to other objects. Examples:
- Fuel levels via a fuel level sensor
- Hostile fighters via a long-range sensor
- Hull integrity via strain gauges
- Intruders via proximity sensor, life-signs detector

## Actuators
Actions are done through actuators. There are actuators and sensors built into the ship that are part of it and feel like pieces of its body: bulkheads, life support systems, fire suppression systems, mechanical arms, etc.

## Dormant Human Systems
Human-centered systems can be found in the ship, lying dormant/unused.
