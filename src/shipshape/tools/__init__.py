"""MCP tools for interacting with the spaceship."""

from .sensors import register_sensor_tools
from .actuators import register_actuator_tools
from .game import register_game_tools

__all__ = [
    "register_sensor_tools",
    "register_actuator_tools",
    "register_game_tools",
]
