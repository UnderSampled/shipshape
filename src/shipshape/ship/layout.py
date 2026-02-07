"""Ship room definitions and layout."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..state.game import GameState

# Room definitions: id -> (name, description, is_human_area)
SHIP_ROOMS = {
    # Core ship areas (robot-focused)
    "reactor_room": (
        "Reactor Chamber",
        "The heart of the ship. The fusion reactor hums with contained power, its status displays flickering.",
        False
    ),
    "engine_room": (
        "Engine Bay",
        "Massive FTL drives dominate this space, currently cold and dormant. Conduits snake across every surface.",
        False
    ),
    "sensor_array": (
        "Sensor Array Hub",
        "Banks of sensors and processing units line the walls. Displays show static where data should flow.",
        False
    ),
    "weapons_bay": (
        "Weapons Control",
        "Targeting systems and weapon mounts. Emergency lights cast red shadows across idle consoles.",
        False
    ),
    "shield_generator": (
        "Shield Generator Room",
        "The shield emitter cores sit silent, their protective fields offline.",
        False
    ),
    "repair_bay": (
        "Repair Bay",
        "Robot maintenance and repair station. Diagnostic equipment and spare parts fill the shelves.",
        False
    ),
    "charging_station": (
        "Charging Station",
        "Multiple charging ports line the walls. Status lights blink in standby mode.",
        False
    ),
    "coolant_room": (
        "Coolant Processing",
        "Pipes and heat exchangers manage thermal loads. A low gurgle indicates partial operation.",
        False
    ),
    "data_core": (
        "Data Core",
        "The ship's computational heart. Server racks and memory banks store robot consciousness backups.",
        False
    ),
    "drone_bay": (
        "Drone Bay",
        "External drone launch and recovery. Several repair drones sit in their cradles.",
        False
    ),
    "cargo_hold": (
        "Cargo Hold",
        "A cavernous space filled with supplies, spare parts, and equipment containers.",
        False
    ),
    "corridor_main": (
        "Main Corridor",
        "The ship's primary thoroughfare, connecting major sections. Emergency lighting casts long shadows.",
        False
    ),
    "corridor_engineering": (
        "Engineering Corridor",
        "Access passage to engineering systems. Pipes and conduits line the ceiling.",
        False
    ),
    "corridor_crew": (
        "Crew Section Corridor",
        "The passage to human living areas. Dust motes drift in the dim emergency lights.",
        False
    ),
    "airlock": (
        "Main Airlock",
        "The primary entry/exit point. Heavy doors seal against the void.",
        False
    ),

    # Human areas (dormant, haunting)
    "bridge": (
        "Bridge",
        "The command center. Empty chairs face dark consoles. A captain's mug sits forgotten.",
        True
    ),
    "crew_quarters": (
        "Crew Quarters",
        "Bunks line the walls, personal effects still in place. Photos of families, trinkets from ports.",
        True
    ),
    "mess_hall": (
        "Mess Hall",
        "Tables and chairs for meals never eaten. The galley contains preserved food stores.",
        True
    ),
    "medical_bay": (
        "Medical Bay",
        "Human healthcare facility. Beds with restraints, diagnostic equipment, medicine cabinets.",
        True
    ),
    "recreation_room": (
        "Recreation Room",
        "Entertainment space with screens, games, and comfortable seating. A cat bed sits in a sunny corner.",
        True
    ),
    "life_support": (
        "Life Support Center",
        "Oxygen recyclers and temperature controls. Critical for organic life.",
        True
    ),
    "observation_deck": (
        "Observation Deck",
        "Reinforced windows look out into the void. The stars wheel slowly past.",
        True
    ),
}

# Room connections: (room_a, room_b, direction_from_a_to_b, direction_from_b_to_a)
ROOM_CONNECTIONS = [
    # Main corridor hub
    ("corridor_main", "reactor_room", "aft", "fore"),
    ("corridor_main", "bridge", "fore", "aft"),
    ("corridor_main", "corridor_engineering", "port", "starboard"),
    ("corridor_main", "corridor_crew", "starboard", "port"),
    ("corridor_main", "cargo_hold", "below", "above"),
    ("corridor_main", "airlock", "port-fore", "starboard-aft"),

    # Engineering section
    ("corridor_engineering", "engine_room", "aft", "fore"),
    ("corridor_engineering", "repair_bay", "port", "starboard"),
    ("corridor_engineering", "coolant_room", "starboard", "port"),
    ("corridor_engineering", "charging_station", "below", "above"),

    # Reactor connects to critical systems
    ("reactor_room", "shield_generator", "port", "starboard"),
    ("reactor_room", "data_core", "starboard", "port"),

    # Sensor and weapons
    ("bridge", "sensor_array", "port", "starboard"),
    ("bridge", "weapons_bay", "starboard", "port"),

    # Drone bay off cargo
    ("cargo_hold", "drone_bay", "aft", "fore"),

    # Crew section
    ("corridor_crew", "crew_quarters", "fore", "aft"),
    ("corridor_crew", "mess_hall", "starboard", "port"),
    ("corridor_crew", "medical_bay", "port", "starboard"),
    ("corridor_crew", "recreation_room", "fore-starboard", "aft-port"),
    ("corridor_crew", "life_support", "below", "above"),

    # Observation deck off recreation
    ("recreation_room", "observation_deck", "above", "below"),
]


def initialize_ship_layout(state: "GameState") -> None:
    """Set up the ship's room structure in the graph."""
    graph = state.graph

    # Add all rooms
    for room_id, (name, description, is_human_area) in SHIP_ROOMS.items():
        graph.add_entity(
            room_id,
            entity_type="room",
            name=name,
            description=description,
            is_human_area=is_human_area,
            temperature=15.0 if is_human_area else 20.0,  # Human areas are cold
            lighting=0.2 if is_human_area else 0.5,  # Dim emergency lighting
            atmosphere=True,  # Ship is pressurized
            hazards=[],
        )

    # Add connections
    for room_a, room_b, dir_a_to_b, dir_b_to_a in ROOM_CONNECTIONS:
        graph.add_relation(
            room_a, "connected_to", room_b,
            direction=dir_a_to_b,
            door_id=f"door_{room_a}_{room_b}",
            door_state="closed",  # Doors start closed
            door_locked=False
        )
        graph.add_relation(
            room_b, "connected_to", room_a,
            direction=dir_b_to_a,
            door_id=f"door_{room_a}_{room_b}",
            door_state="closed",
            door_locked=False
        )

    # Place special items
    # Cat food and water bowl in mess hall
    graph.add_entity(
        "cat_food_bowl",
        entity_type="item",
        name="Cat Food Bowl",
        description="A small bowl for cat food. Currently empty.",
        filled=False,
        capacity=100.0,
        contents=0.0
    )
    graph.add_relation("cat_food_bowl", "in", "mess_hall")

    graph.add_entity(
        "cat_water_bowl",
        entity_type="item",
        name="Cat Water Bowl",
        description="A small bowl for water. Currently empty.",
        filled=False,
        capacity=100.0,
        contents=0.0
    )
    graph.add_relation("cat_water_bowl", "in", "mess_hall")

    # Cat bed in recreation room
    graph.add_entity(
        "cat_bed",
        entity_type="item",
        name="Cat Bed",
        description="A cozy heated cat bed in a sunny corner. The heating element is off.",
        heated=False,
        temperature=15.0
    )
    graph.add_relation("cat_bed", "in", "recreation_room")

    # Log the initialization
    state.log_event(
        "initialization",
        f"Ship layout initialized: {len(SHIP_ROOMS)} rooms",
        severity="info"
    )
