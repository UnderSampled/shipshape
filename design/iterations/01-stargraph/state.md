# Stargraph space sim

Stargraph is a data-only galaxy/universe space simulator. The intention is to make a complex enough universe to explore, such that emergent behaviors will allow rich interactions for text-based adventures.

## The Graph
"The Graph", also called the universe state, is a graph describing objects, their types, their individual states, and their relationships.

### State
Here are some examples of state and relationships that are stored in the Graph:
  - "Sol" is a star system
  - The Sol system connects to the Alpha Centauri system by a "jump path"
  - Luna orbits Sol
  - "The X1 fighter is in hanger 535424; hanger 535424 is in starship 234
  - The X1 fighter's fuel tank is 55% full
  - The thruster is burning; it has been burning since <timestamp>

## Events
The mutations to the universe state occur through events, which occur at specific points in time.

### Effects
Effects are triggered events, which occur according to conditional rules.
The results of triggering an effect can be simple cause-and-effect, or the effects might be random, driven by probability tables. Probabilities can altered according to the states of the relevant objects. For example:
  - When a fighter's fuel tank is empty, its thrusters stop burning
  - When fighter lands without landing gear deployed, there is a 35% chance of damaging the hull, and a 5% chance of rupturing it
  - When docked at a space-port, a ship can trade
  - When entering the DMZ for a space-port, the likeliness that the space-port will use its comms to tell the ship to leave depends on their report with the space-port's faction

### Actions
Actions are events caused by an actor. For instance, if a ship is controlled by an actor, and it has actuators, that actor can use those actuators to enact actions. For example:
  - An auto-cannon can be fired at a target hostile ship
  - A long-range sensor can be set to scan mode
  - A repair droid can be dispatched

## Sensors
Sensors are how actors perceive the Graph. The raw state of the graph is not read directly by actors. Instead, they must interact with it through sensors, which are limited in scope by their relationships to other objects. For example:
  - Fuel levels can be monitored by reading a fuel level sensor
  - The presense of a hostile fighter in orbit around a different gravitational locus can be monitored by reading a long-range sensor
  - The hull integrity can be read through strain gauages and other realistic data-sources
  - Detecting (or "feeling", from the point of view of the ship) the presense of an intruder resting on the surface of the hull might require a functioning proximity sensor, life-signs detector, etc.