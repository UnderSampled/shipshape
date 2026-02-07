"""Ship system definitions and behaviors."""

from enum import Enum
from pydantic import BaseModel, Field


class SystemType(str, Enum):
    """Types of ship systems."""
    REACTOR = "reactor"
    SHIELDS = "shields"
    ENGINES = "engines"
    WEAPONS = "weapons"
    SENSORS = "sensors"
    DOORS = "doors"
    REPAIR_BAY = "repair_bay"
    CHARGING = "charging"
    COOLANT = "coolant"
    DATA_CORE = "data_core"
    DRONE_CONTROL = "drone_control"
    LIFE_SUPPORT = "life_support"
    GRAVITY = "gravity"
    LIGHTING = "lighting"
    NAVIGATION = "navigation"
    COMMUNICATIONS = "communications"
    UTILITY = "utility"


class ShipSystem(BaseModel):
    """A ship system with FTL-style mechanics."""

    id: str
    name: str
    description: str
    system_type: SystemType
    location: str  # Room where system is located

    # State
    online: bool = False
    power_level: float = Field(default=0.0, ge=0.0, le=100.0)  # Allocated power
    health: float = Field(default=100.0, ge=0.0, le=100.0)
    temperature: float = Field(default=20.0)  # Celsius

    # Configuration
    required_phase: str = "awakening"  # Game phase required to bring online
    base_power_draw: float = 10.0  # Power needed at 100%
    max_operators: int = 2  # Max robots that can operate it

    # Manning
    manned_by: list[str] = Field(default_factory=list)  # Robot IDs

    # Damage effects
    damaged_ticks: int = 0  # Ticks spent in critical damage
    on_fire: bool = False
    breached: bool = False  # Hull breach in this location

    @property
    def efficiency(self) -> float:
        """
        Calculate system efficiency (0.0 - 1.0).

        Based on power level, health, and manning.
        """
        if not self.online:
            return 0.0

        # Base efficiency from power (normalized to 0-1)
        power_factor = self.power_level / 100.0

        # Health reduces efficiency
        health_factor = self.health / 100.0

        # Manning bonus (up to 20% boost)
        manning_bonus = min(len(self.manned_by) / max(self.max_operators, 1), 1.0) * 0.2

        # Temperature penalty if overheating
        temp_factor = 1.0
        if self.temperature > 80:
            temp_factor = max(0.0, 1.0 - (self.temperature - 80) / 40)

        return min(1.0, power_factor * health_factor * temp_factor + manning_bonus)

    @property
    def actual_power_draw(self) -> float:
        """Calculate actual power being consumed."""
        if not self.online:
            return 0.0
        return self.base_power_draw * (self.power_level / 100.0)

    @property
    def is_critical(self) -> bool:
        """Check if system is in critical state."""
        return self.health < 25 or self.on_fire or self.breached

    @property
    def status_summary(self) -> str:
        """Get a brief status description."""
        if not self.online:
            return "OFFLINE"
        if self.on_fire:
            return "FIRE"
        if self.breached:
            return "BREACHED"
        if self.health < 25:
            return "CRITICAL"
        if self.health < 50:
            return "DAMAGED"
        if self.efficiency < 0.3:
            return "LOW POWER"
        return "OPERATIONAL"

    def take_damage(self, amount: float) -> None:
        """Apply damage to the system."""
        self.health = max(0.0, self.health - amount)
        if self.health == 0:
            self.online = False

    def repair(self, amount: float) -> None:
        """Repair the system."""
        self.health = min(100.0, self.health + amount)

    def update_temperature(self, coolant_efficiency: float, ambient: float = 20.0) -> None:
        """Update system temperature based on load and cooling."""
        if not self.online:
            # Cool down when offline
            self.temperature = max(ambient, self.temperature - 1.0)
            return

        # Heat generation based on power usage
        heat_generated = self.actual_power_draw * 0.5

        # Cooling based on coolant system efficiency
        cooling = coolant_efficiency * 10.0

        # Net temperature change
        delta = heat_generated - cooling
        self.temperature = max(ambient, min(120.0, self.temperature + delta * 0.1))

        # Fire risk if too hot
        if self.temperature > 100 and not self.on_fire:
            # 5% chance per tick when overheating
            import random
            if random.random() < 0.05:
                self.on_fire = True

    def tick(self, coolant_efficiency: float) -> list[str]:
        """
        Process one simulation tick.

        Returns list of events that occurred.
        """
        events = []

        # Update temperature
        self.update_temperature(coolant_efficiency)

        # Track time in critical state
        if self.is_critical:
            self.damaged_ticks += 1
            if self.damaged_ticks > 30:  # 30 seconds of critical damage
                events.append(f"{self.name} has suffered catastrophic damage")
        else:
            self.damaged_ticks = 0

        # Fire damage
        if self.on_fire:
            self.take_damage(2.0)
            events.append(f"{self.name} is taking fire damage")

        return events
