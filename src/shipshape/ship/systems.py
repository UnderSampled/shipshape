"""Ship system definitions and behaviors."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..state.game import GameState
    from ..simulation.systems import ShipSystem

# System definitions: id -> (name, description, location, starts_online, required_phase, power_draw)
SYSTEM_DEFINITIONS = {
    # Core systems (robot-focused)
    "reactor": (
        "Fusion Reactor",
        "Primary power generation. Without it, the ship is dead.",
        "reactor_room",
        True,  # Starts online (minimal)
        "awakening",
        0  # Generates power, doesn't consume
    ),
    "sensors_internal": (
        "Internal Sensors",
        "Monitors conditions throughout the ship. Limited range when damaged.",
        "sensor_array",
        True,  # Starts online (limited)
        "awakening",
        5
    ),
    "sensors_external": (
        "External Sensors",
        "Long-range detection of objects, ships, and phenomena.",
        "sensor_array",
        False,
        "journey",
        15
    ),
    "shields": (
        "Shield Generator",
        "Protective energy barrier against impacts and radiation.",
        "shield_generator",
        False,
        "defense",
        25
    ),
    "engines_sublight": (
        "Sublight Engines",
        "Conventional thrust for maneuvering and evasion.",
        "engine_room",
        False,
        "journey",
        20
    ),
    "engines_ftl": (
        "FTL Drive",
        "Faster-than-light jump capability. Requires charge time.",
        "engine_room",
        False,
        "journey",
        30
    ),
    "weapons_laser": (
        "Laser Array",
        "Primary defensive weapon system.",
        "weapons_bay",
        False,
        "defense",
        20
    ),
    "weapons_missile": (
        "Missile Launcher",
        "Heavy ordnance for serious threats.",
        "weapons_bay",
        False,
        "defense",
        15
    ),
    "doors": (
        "Door Control System",
        "Automated door operation throughout the ship.",
        "data_core",
        False,
        "mobility",
        5
    ),
    "repair_system": (
        "Repair Bay Systems",
        "Robot maintenance and repair equipment.",
        "repair_bay",
        False,
        "mobility",
        10
    ),
    "charging_system": (
        "Charging Network",
        "Power distribution for robot recharging.",
        "charging_station",
        True,  # Minimal charging available
        "awakening",
        10
    ),
    "coolant_system": (
        "Coolant Circulation",
        "Thermal management for ship systems and robots.",
        "coolant_room",
        True,  # Basic cooling online
        "awakening",
        8
    ),
    "data_core_system": (
        "Data Core",
        "Central processing and robot memory synchronization.",
        "data_core",
        True,  # Core consciousness requires this
        "awakening",
        12
    ),
    "drone_control": (
        "Drone Control",
        "Management of external repair and combat drones.",
        "drone_bay",
        False,
        "full",
        10
    ),
    "navigation": (
        "Navigation Computer",
        "Star charts and jump calculations.",
        "bridge",
        False,
        "journey",
        8
    ),
    "communications": (
        "Communications Array",
        "Long-range transmission and reception.",
        "bridge",
        False,
        "full",
        10
    ),

    # Human-focused systems (dormant)
    "life_support": (
        "Life Support",
        "Oxygen recycling, temperature control for organic life.",
        "life_support",
        False,
        "discovery",
        20
    ),
    "gravity": (
        "Artificial Gravity",
        "Maintains comfortable gravity throughout the ship.",
        "life_support",
        False,
        "discovery",
        15
    ),
    "lighting": (
        "Primary Lighting",
        "Full illumination beyond emergency lights.",
        "data_core",
        False,
        "mobility",
        5
    ),
}


def initialize_ship_systems(state: "GameState") -> None:
    """Set up ship systems in the game state."""
    from ..simulation.systems import ShipSystem, SystemType

    # Map system IDs to types
    type_mapping = {
        "reactor": SystemType.REACTOR,
        "sensors_internal": SystemType.SENSORS,
        "sensors_external": SystemType.SENSORS,
        "shields": SystemType.SHIELDS,
        "engines_sublight": SystemType.ENGINES,
        "engines_ftl": SystemType.ENGINES,
        "weapons_laser": SystemType.WEAPONS,
        "weapons_missile": SystemType.WEAPONS,
        "doors": SystemType.DOORS,
        "repair_system": SystemType.REPAIR_BAY,
        "charging_system": SystemType.CHARGING,
        "coolant_system": SystemType.COOLANT,
        "data_core_system": SystemType.DATA_CORE,
        "drone_control": SystemType.DRONE_CONTROL,
        "navigation": SystemType.NAVIGATION,
        "communications": SystemType.COMMUNICATIONS,
        "life_support": SystemType.LIFE_SUPPORT,
        "gravity": SystemType.GRAVITY,
        "lighting": SystemType.LIGHTING,
    }

    for system_id, (name, description, location, starts_online, required_phase, power_draw) in SYSTEM_DEFINITIONS.items():
        system = ShipSystem(
            id=system_id,
            name=name,
            description=description,
            system_type=type_mapping.get(system_id, SystemType.UTILITY),
            location=location,
            online=starts_online,
            required_phase=required_phase,
            base_power_draw=power_draw,
            power_level=20.0 if starts_online else 0.0,
            health=70.0 if starts_online else 50.0,  # Online systems less damaged
        )
        state.systems[system_id] = system

        # Add system as entity in graph
        state.graph.add_entity(
            system_id,
            entity_type="system",
            name=name,
            online=starts_online
        )
        state.graph.add_relation(system_id, "in", location)

    state.log_event(
        "initialization",
        f"Ship systems initialized: {len(state.systems)} systems",
        severity="info"
    )
