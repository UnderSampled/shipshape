"""Game state container for the spaceship simulation."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from threading import RLock
from typing import TYPE_CHECKING

from pydantic import BaseModel

from .graph import GraphState

if TYPE_CHECKING:
    from ..simulation.robots import Robot
    from ..simulation.systems import ShipSystem


class GamePhase(str, Enum):
    """Tutorial/progression phases."""
    AWAKENING = "awakening"      # Phase 1: Basic systems only
    MOBILITY = "mobility"        # Phase 2: Doors, charging
    DISCOVERY = "discovery"      # Phase 3: Find cat, life support
    DEFENSE = "defense"          # Phase 4: Shields, weapons
    JOURNEY = "journey"          # Phase 5: Engines, navigation
    FULL_CAPABILITY = "full"     # Phase 6: All systems


class CatStatus(str, Enum):
    """Cat behavior states."""
    SLEEPING = "sleeping"
    WANDERING = "wandering"
    EATING = "eating"
    DRINKING = "drinking"
    HIDING = "hiding"
    DISTRESSED = "distressed"
    PLAYING = "playing"


class Cat(BaseModel):
    """The ship's cat - the last biological crew member."""
    name: str = "Unknown"  # Discoverable from collar
    location: str = "recreation_room"
    hunger: float = 50.0      # 0-100, higher = more hungry
    thirst: float = 50.0      # 0-100, higher = more thirsty
    warmth: float = 70.0      # 0-100, higher = warmer
    health: float = 100.0     # 0-100
    happiness: float = 50.0   # 0-100
    status: CatStatus = CatStatus.SLEEPING
    discovered: bool = False  # Has the Core found the cat?
    last_fed_tick: int = 0
    last_watered_tick: int = 0


@dataclass
class EventLogEntry:
    """A logged event."""
    tick: int
    timestamp: float
    event_type: str
    message: str
    severity: str = "info"  # info, warning, critical
    data: dict = field(default_factory=dict)


class GameState:
    """
    Central container for all game state.

    Thread-safe access via RLock for simulation thread.
    """

    def __init__(self):
        self._lock = RLock()

        # Graph-based state
        self.graph = GraphState()

        # Game metadata
        self.ship_name = "ISV Perseverance"
        self.game_started = False
        self.current_tick = 0
        self.start_time = 0.0
        self.phase = GamePhase.AWAKENING

        # Ship systems (populated by ship module)
        self.systems: dict[str, ShipSystem] = {}

        # Robots (populated by simulation)
        self.robots: dict[str, Robot] = {}

        # The cat
        self.cat = Cat()

        # Journey state
        self.current_sector = 1
        self.current_node = "start"
        self.sector_map: dict = {}
        self.destination = "Cygnus Repair Station"
        self.threat_level = 1.0
        self.jump_charge = 0.0
        self.jump_cooldown = 0.0
        self.jumping = False
        self.jump_target: str | None = None

        # Event log (circular buffer)
        self.event_log: list[EventLogEntry] = []
        self.max_log_entries = 100

        # Total power available (from reactor)
        self.total_power = 0.0
        self.power_allocated = 0.0

        # Hull integrity
        self.hull_integrity = 65.0  # Start damaged

    def lock(self) -> RLock:
        """Get the state lock for thread-safe access."""
        return self._lock

    def log_event(
        self,
        event_type: str,
        message: str,
        severity: str = "info",
        **data
    ) -> None:
        """Add an event to the log."""
        entry = EventLogEntry(
            tick=self.current_tick,
            timestamp=time.time(),
            event_type=event_type,
            message=message,
            severity=severity,
            data=data
        )
        self.event_log.append(entry)
        if len(self.event_log) > self.max_log_entries:
            self.event_log.pop(0)

    def get_recent_events(self, count: int = 20) -> list[EventLogEntry]:
        """Get the most recent events."""
        return self.event_log[-count:]

    def get_system(self, system_id: str) -> ShipSystem | None:
        """Get a ship system by ID."""
        return self.systems.get(system_id)

    def get_robot(self, robot_id: str) -> Robot | None:
        """Get a robot by ID."""
        return self.robots.get(robot_id)

    def get_online_systems(self) -> list[ShipSystem]:
        """Get all online systems."""
        return [s for s in self.systems.values() if s.online]

    def get_offline_systems(self) -> list[ShipSystem]:
        """Get all offline systems."""
        return [s for s in self.systems.values() if not s.online]

    def calculate_total_power(self) -> float:
        """Calculate available power from reactor."""
        reactor = self.systems.get("reactor")
        if reactor and reactor.online:
            return reactor.efficiency * 100  # Max 100 power at full efficiency
        return 0.0

    def calculate_power_allocated(self) -> float:
        """Calculate total power currently allocated."""
        return sum(s.power_level for s in self.systems.values() if s.online)

    def can_allocate_power(self, amount: float) -> bool:
        """Check if there's enough power available."""
        available = self.calculate_total_power() - self.calculate_power_allocated()
        return available >= amount

    def advance_phase(self) -> bool:
        """Try to advance to the next game phase."""
        phases = list(GamePhase)
        current_idx = phases.index(self.phase)
        if current_idx < len(phases) - 1:
            self.phase = phases[current_idx + 1]
            self.log_event(
                "phase_change",
                f"Ship capabilities expanded: {self.phase.value}",
                severity="info"
            )
            return True
        return False

    def to_dict(self) -> dict:
        """Serialize game state for saving."""
        return {
            "ship_name": self.ship_name,
            "current_tick": self.current_tick,
            "phase": self.phase.value,
            "graph": self.graph.to_dict(),
            "systems": {sid: s.model_dump() for sid, s in self.systems.items()},
            "robots": {rid: r.model_dump() for rid, r in self.robots.items()},
            "cat": self.cat.model_dump(),
            "journey": {
                "current_sector": self.current_sector,
                "current_node": self.current_node,
                "sector_map": self.sector_map,
                "destination": self.destination,
                "threat_level": self.threat_level,
                "jump_charge": self.jump_charge,
                "jump_cooldown": self.jump_cooldown,
            },
            "hull_integrity": self.hull_integrity,
            "event_log": [
                {
                    "tick": e.tick,
                    "timestamp": e.timestamp,
                    "event_type": e.event_type,
                    "message": e.message,
                    "severity": e.severity,
                    "data": e.data
                }
                for e in self.event_log
            ]
        }

    def from_dict(self, data: dict, system_class, robot_class) -> None:
        """Load game state from dictionary."""
        self.ship_name = data.get("ship_name", self.ship_name)
        self.current_tick = data.get("current_tick", 0)
        self.phase = GamePhase(data.get("phase", "awakening"))

        if "graph" in data:
            self.graph.from_dict(data["graph"])

        if "systems" in data:
            self.systems = {
                sid: system_class.model_validate(sdata)
                for sid, sdata in data["systems"].items()
            }

        if "robots" in data:
            self.robots = {
                rid: robot_class.model_validate(rdata)
                for rid, rdata in data["robots"].items()
            }

        if "cat" in data:
            self.cat = Cat.model_validate(data["cat"])

        if "journey" in data:
            j = data["journey"]
            self.current_sector = j.get("current_sector", 1)
            self.current_node = j.get("current_node", "start")
            self.sector_map = j.get("sector_map", {})
            self.destination = j.get("destination", self.destination)
            self.threat_level = j.get("threat_level", 1.0)
            self.jump_charge = j.get("jump_charge", 0.0)
            self.jump_cooldown = j.get("jump_cooldown", 0.0)

        self.hull_integrity = data.get("hull_integrity", 65.0)

        if "event_log" in data:
            self.event_log = [
                EventLogEntry(**e) for e in data["event_log"]
            ]
