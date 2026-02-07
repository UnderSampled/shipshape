"""Robot entities with Dwarf Fortress-style needs and behaviors."""

from enum import Enum
from typing import Any
import random

from pydantic import BaseModel, Field


class RobotRole(str, Enum):
    """Robot specializations."""
    ENGINEER = "engineer"     # System repair and maintenance
    GUNNER = "gunner"         # Weapons operation
    PILOT = "pilot"           # Navigation and engines
    REPAIR = "repair"         # Robot repair specialist
    GENERAL = "general"       # Jack of all trades
    CARETAKER = "caretaker"   # Cat care specialist


class RobotStatus(str, Enum):
    """Current robot state."""
    IDLE = "idle"
    WORKING = "working"
    MOVING = "moving"
    CHARGING = "charging"
    REPAIRING = "repairing"      # Being repaired
    DISABLED = "disabled"
    MALFUNCTIONING = "malfunctioning"


class TaskType(str, Enum):
    """Types of tasks robots can perform."""
    OPERATE_SYSTEM = "operate_system"   # Man a station
    REPAIR_SYSTEM = "repair_system"     # Fix a system
    REPAIR_ROBOT = "repair_robot"       # Fix another robot
    MOVE_TO = "move_to"                 # Go to location
    CHARGE = "charge"                   # Charge at station
    FIGHT_FIRE = "fight_fire"           # Extinguish fire
    FEED_CAT = "feed_cat"               # Fill cat food bowl
    WATER_CAT = "water_cat"             # Fill cat water bowl
    PATROL = "patrol"                   # Move between rooms
    CUSTOM = "custom"                   # User-defined task


class Trait(str, Enum):
    """Robot personality traits affecting behavior."""
    DILIGENT = "diligent"       # Prioritizes tasks over needs
    CAUTIOUS = "cautious"       # Avoids hazardous areas
    RECKLESS = "reckless"       # Ignores danger
    SOCIAL = "social"           # Prefers being near other robots
    SOLITARY = "solitary"       # Prefers being alone
    EFFICIENT = "efficient"     # Better at power management
    LOYAL = "loyal"             # Follows orders precisely
    INDEPENDENT = "independent" # May interpret orders creatively


class Task(BaseModel):
    """A task assigned to a robot."""
    task_type: TaskType
    target: str | None = None  # Target entity/location
    priority: int = Field(default=5, ge=1, le=10)  # 1=highest
    progress: float = Field(default=0.0, ge=0.0, le=100.0)
    data: dict[str, Any] = Field(default_factory=dict)

    @property
    def is_complete(self) -> bool:
        return self.progress >= 100.0


class Robot(BaseModel):
    """A robot crew member with needs and behaviors."""

    # Identity
    id: str
    designation: str  # Human-readable name like "MNT-7"
    role: RobotRole

    # Needs (0-100, lower = more urgent need)
    power_level: float = Field(default=80.0, ge=0.0, le=100.0)
    thermal_level: float = Field(default=50.0, ge=0.0, le=100.0)  # 50 = optimal
    maintenance: float = Field(default=90.0, ge=0.0, le=100.0)
    memory_integrity: float = Field(default=95.0, ge=0.0, le=100.0)

    # State
    location: str
    current_task: Task | None = None
    task_queue: list[Task] = Field(default_factory=list)
    status: RobotStatus = RobotStatus.IDLE

    # Movement
    move_progress: float = 0.0  # Progress moving between rooms
    move_target: str | None = None

    # Personality
    traits: list[Trait] = Field(default_factory=list)

    # Stats
    repair_skill: float = Field(default=50.0, ge=0.0, le=100.0)
    combat_skill: float = Field(default=50.0, ge=0.0, le=100.0)
    efficiency: float = Field(default=50.0, ge=0.0, le=100.0)

    # Relationships (robot_id -> affinity -100 to 100)
    relationships: dict[str, int] = Field(default_factory=dict)

    @property
    def is_functional(self) -> bool:
        """Check if robot can operate."""
        return (
            self.status != RobotStatus.DISABLED and
            self.power_level > 5 and
            self.maintenance > 10
        )

    @property
    def needs_charge(self) -> bool:
        """Check if robot needs to charge."""
        threshold = 30 if Trait.DILIGENT in self.traits else 40
        return self.power_level < threshold

    @property
    def needs_repair(self) -> bool:
        """Check if robot needs maintenance."""
        return self.maintenance < 40

    @property
    def needs_cooling(self) -> bool:
        """Check if robot is overheating."""
        return self.thermal_level > 80

    @property
    def needs_sync(self) -> bool:
        """Check if robot needs data core sync."""
        return self.memory_integrity < 50

    @property
    def most_urgent_need(self) -> str | None:
        """Get the most urgent need, if any."""
        if self.power_level < 10:
            return "power_critical"
        if self.thermal_level > 90:
            return "cooling_critical"
        if self.maintenance < 20:
            return "maintenance_critical"
        if self.needs_charge:
            return "charge"
        if self.needs_cooling:
            return "cooling"
        if self.needs_repair:
            return "maintenance"
        if self.needs_sync:
            return "sync"
        return None

    @property
    def status_summary(self) -> str:
        """Get a brief status description."""
        if self.status == RobotStatus.DISABLED:
            return "DISABLED"
        if self.power_level < 10:
            return "POWER CRITICAL"
        if self.thermal_level > 90:
            return "OVERHEATING"
        if self.maintenance < 20:
            return "DAMAGED"
        if self.status == RobotStatus.MALFUNCTIONING:
            return "MALFUNCTION"
        if self.status == RobotStatus.CHARGING:
            return "CHARGING"
        if self.status == RobotStatus.WORKING:
            return f"WORKING: {self.current_task.task_type.value if self.current_task else 'unknown'}"
        if self.status == RobotStatus.MOVING:
            return f"MOVING TO: {self.move_target}"
        return "IDLE"

    def assign_task(self, task: Task, immediate: bool = False) -> None:
        """Assign a task to this robot."""
        if immediate:
            if self.current_task:
                self.task_queue.insert(0, self.current_task)
            self.current_task = task
            self.status = RobotStatus.WORKING
        else:
            self.task_queue.append(task)

    def complete_current_task(self) -> Task | None:
        """Mark current task complete and get next task."""
        completed = self.current_task
        self.current_task = None

        if self.task_queue:
            self.current_task = self.task_queue.pop(0)
            self.status = RobotStatus.WORKING
        else:
            self.status = RobotStatus.IDLE

        return completed

    def consume_power(self, amount: float) -> None:
        """Consume power for an action."""
        modifier = 0.8 if Trait.EFFICIENT in self.traits else 1.0
        self.power_level = max(0.0, self.power_level - amount * modifier)
        if self.power_level <= 0:
            self.status = RobotStatus.DISABLED

    def charge(self, amount: float) -> None:
        """Charge the robot's power cells."""
        self.power_level = min(100.0, self.power_level + amount)

    def heat_up(self, amount: float) -> None:
        """Increase thermal level from work."""
        self.thermal_level = min(100.0, self.thermal_level + amount)

    def cool_down(self, amount: float) -> None:
        """Decrease thermal level."""
        self.thermal_level = max(0.0, self.thermal_level - amount)

    def take_damage(self, amount: float) -> None:
        """Take maintenance damage."""
        self.maintenance = max(0.0, self.maintenance - amount)
        if self.maintenance <= 0:
            self.status = RobotStatus.DISABLED

    def repair(self, amount: float) -> None:
        """Repair maintenance damage."""
        self.maintenance = min(100.0, self.maintenance + amount)
        if self.status == RobotStatus.DISABLED and self.maintenance > 10:
            self.status = RobotStatus.IDLE

    def degrade_memory(self, amount: float) -> None:
        """Degrade memory integrity."""
        self.memory_integrity = max(0.0, self.memory_integrity - amount)
        if self.memory_integrity < 30:
            # Risk of malfunction
            if random.random() < 0.1:
                self.status = RobotStatus.MALFUNCTIONING

    def sync_memory(self, amount: float) -> None:
        """Sync with data core to restore memory integrity."""
        self.memory_integrity = min(100.0, self.memory_integrity + amount)
        if self.status == RobotStatus.MALFUNCTIONING and self.memory_integrity > 50:
            self.status = RobotStatus.IDLE

    def update_relationship(self, other_id: str, delta: int) -> None:
        """Update relationship with another robot."""
        current = self.relationships.get(other_id, 0)
        self.relationships[other_id] = max(-100, min(100, current + delta))

    def tick(self, ambient_temp: float, coolant_available: bool) -> list[str]:
        """
        Process one simulation tick.

        Returns list of events.
        """
        events = []

        # Skip if disabled
        if self.status == RobotStatus.DISABLED:
            return events

        # Passive power drain
        self.consume_power(0.1)

        # Passive memory degradation
        self.degrade_memory(0.05)

        # Temperature adjustment
        if coolant_available:
            # Cool toward 50 (optimal)
            if self.thermal_level > 50:
                self.cool_down(2.0)
            elif self.thermal_level < 50:
                self.heat_up(1.0)
        else:
            # Slow passive heating
            self.heat_up(0.5)

        # Check for critical states
        if self.power_level <= 0:
            self.status = RobotStatus.DISABLED
            events.append(f"{self.designation} has shut down: power depleted")
        elif self.thermal_level >= 100:
            self.status = RobotStatus.DISABLED
            events.append(f"{self.designation} has shut down: thermal overload")
        elif self.maintenance <= 0:
            self.status = RobotStatus.DISABLED
            events.append(f"{self.designation} has shut down: critical damage")

        return events


def create_starting_robots() -> list[Robot]:
    """Create the initial robot crew."""
    robots = [
        Robot(
            id="robot_eng_1",
            designation="ENG-1",
            role=RobotRole.ENGINEER,
            location="reactor_room",
            traits=[Trait.DILIGENT, Trait.CAUTIOUS],
            repair_skill=80.0,
            efficiency=70.0,
            power_level=60.0,
            maintenance=75.0,
        ),
        Robot(
            id="robot_eng_2",
            designation="ENG-2",
            role=RobotRole.ENGINEER,
            location="engine_room",
            traits=[Trait.EFFICIENT, Trait.SOLITARY],
            repair_skill=75.0,
            efficiency=85.0,
            power_level=55.0,
            maintenance=70.0,
        ),
        Robot(
            id="robot_gun_1",
            designation="GUN-1",
            role=RobotRole.GUNNER,
            location="weapons_bay",
            traits=[Trait.LOYAL, Trait.RECKLESS],
            combat_skill=90.0,
            power_level=50.0,
            maintenance=65.0,
        ),
        Robot(
            id="robot_plt_1",
            designation="PLT-1",
            role=RobotRole.PILOT,
            location="bridge",
            traits=[Trait.CAUTIOUS, Trait.EFFICIENT],
            efficiency=80.0,
            power_level=70.0,
            maintenance=80.0,
        ),
        Robot(
            id="robot_rpr_1",
            designation="RPR-1",
            role=RobotRole.REPAIR,
            location="repair_bay",
            traits=[Trait.DILIGENT, Trait.SOCIAL],
            repair_skill=95.0,
            power_level=65.0,
            maintenance=85.0,
        ),
        Robot(
            id="robot_gen_1",
            designation="GEN-1",
            role=RobotRole.GENERAL,
            location="cargo_hold",
            traits=[Trait.INDEPENDENT],
            power_level=45.0,
            maintenance=60.0,
        ),
        Robot(
            id="robot_care_1",
            designation="CARE-1",
            role=RobotRole.CARETAKER,
            location="mess_hall",
            traits=[Trait.DILIGENT, Trait.SOCIAL],
            efficiency=70.0,
            power_level=55.0,
            maintenance=75.0,
        ),
    ]

    return robots
