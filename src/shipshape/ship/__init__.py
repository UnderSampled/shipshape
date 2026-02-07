"""Ship structure and system definitions."""

from .layout import SHIP_ROOMS, ROOM_CONNECTIONS, initialize_ship_layout
from .systems import SYSTEM_DEFINITIONS, initialize_ship_systems

__all__ = [
    "SHIP_ROOMS",
    "ROOM_CONNECTIONS",
    "initialize_ship_layout",
    "SYSTEM_DEFINITIONS",
    "initialize_ship_systems",
]
