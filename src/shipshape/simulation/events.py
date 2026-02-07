"""Event generation and processing for the simulation."""

import random
from enum import Enum
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from ..state.game import GameState


class EventType(str, Enum):
    """Types of events that can occur."""
    # External events
    ASTEROID_FIELD = "asteroid_field"
    SOLAR_FLARE = "solar_flare"
    DEBRIS_FIELD = "debris_field"
    DISTRESS_BEACON = "distress_beacon"
    NEBULA = "nebula"
    GRAVITY_WELL = "gravity_well"
    RADIATION_STORM = "radiation_storm"

    # Internal events
    SYSTEM_MALFUNCTION = "system_malfunction"
    POWER_SURGE = "power_surge"
    POWER_SHORTAGE = "power_shortage"
    ROBOT_CONFLICT = "robot_conflict"
    FIRE = "fire"
    ELECTRICAL_HAZARD = "electrical_hazard"
    HULL_BREACH = "hull_breach"
    COOLANT_LEAK = "coolant_leak"

    # Journey events
    BEACON_DISCOVERY = "beacon_discovery"
    DERELICT_SHIP = "derelict_ship"
    SPACE_STATION = "space_station"
    JUMP_ANOMALY = "jump_anomaly"

    # Cat events
    CAT_HUNGRY = "cat_hungry"
    CAT_THIRSTY = "cat_thirsty"
    CAT_COLD = "cat_cold"
    CAT_STUCK = "cat_stuck"
    CAT_FOUND = "cat_found"


@dataclass
class Event:
    """An event in the simulation."""
    event_type: EventType
    severity: str  # info, warning, critical
    message: str
    duration: int = 0  # Ticks the event lasts (0 = instant)
    data: dict = None

    def __post_init__(self):
        if self.data is None:
            self.data = {}


class EventGenerator:
    """Generates random events based on game state."""

    # Base chances per tick (will be modified by conditions)
    BASE_CHANCES = {
        # External (only when moving/at certain nodes)
        EventType.ASTEROID_FIELD: 0.002,
        EventType.SOLAR_FLARE: 0.001,
        EventType.DEBRIS_FIELD: 0.003,
        EventType.RADIATION_STORM: 0.001,

        # Internal (always possible)
        EventType.SYSTEM_MALFUNCTION: 0.005,
        EventType.POWER_SURGE: 0.003,
        EventType.FIRE: 0.002,
        EventType.COOLANT_LEAK: 0.002,

        # Cat (when cat discovered)
        EventType.CAT_HUNGRY: 0.01,
        EventType.CAT_THIRSTY: 0.01,
        EventType.CAT_COLD: 0.008,
    }

    def __init__(self, state: "GameState"):
        self.state = state
        self.active_events: list[Event] = []

    def tick(self) -> list[Event]:
        """
        Generate events for this tick.

        Returns list of new events.
        """
        new_events = []

        # Update active events (decrease duration)
        remaining = []
        for event in self.active_events:
            if event.duration > 0:
                event.duration -= 1
                remaining.append(event)
            else:
                # Event ended
                self._end_event(event)
        self.active_events = remaining

        # Roll for new events
        new_events.extend(self._check_external_events())
        new_events.extend(self._check_internal_events())
        new_events.extend(self._check_cat_events())

        # Add new events to active list
        for event in new_events:
            if event.duration > 0:
                self.active_events.append(event)
            self._apply_event(event)

        return new_events

    def _check_external_events(self) -> list[Event]:
        """Check for external space events."""
        events = []

        # Only external events when not docked
        if self.state.current_node == "station":
            return events

        # Modify chances based on sector
        threat_mod = self.state.threat_level

        # Asteroid field
        if random.random() < self.BASE_CHANCES[EventType.ASTEROID_FIELD] * threat_mod:
            damage = random.uniform(5, 15) * threat_mod
            events.append(Event(
                EventType.ASTEROID_FIELD,
                "warning",
                f"Asteroid field impact! Hull taking damage.",
                duration=random.randint(3, 8),
                data={"damage_per_tick": damage}
            ))

        # Solar flare
        if random.random() < self.BASE_CHANCES[EventType.SOLAR_FLARE] * threat_mod:
            events.append(Event(
                EventType.SOLAR_FLARE,
                "warning",
                "Solar flare detected! Sensor interference and potential system damage.",
                duration=random.randint(5, 15),
                data={"sensor_penalty": 0.5, "damage_chance": 0.1}
            ))

        # Radiation storm
        if random.random() < self.BASE_CHANCES[EventType.RADIATION_STORM] * threat_mod:
            events.append(Event(
                EventType.RADIATION_STORM,
                "critical",
                "Radiation storm! Robot memory systems at risk.",
                duration=random.randint(10, 20),
                data={"memory_damage": 2.0}
            ))

        return events

    def _check_internal_events(self) -> list[Event]:
        """Check for internal ship events."""
        events = []

        # System malfunction (more likely if systems are damaged)
        damaged_systems = [
            s for s in self.state.systems.values()
            if s.online and s.health < 50
        ]
        malfunction_chance = (
            self.BASE_CHANCES[EventType.SYSTEM_MALFUNCTION] *
            (1 + len(damaged_systems) * 0.5)
        )
        if damaged_systems and random.random() < malfunction_chance:
            system = random.choice(damaged_systems)
            events.append(Event(
                EventType.SYSTEM_MALFUNCTION,
                "warning",
                f"{system.name} is malfunctioning!",
                data={"system_id": system.id, "efficiency_penalty": 0.3}
            ))

        # Power surge (if reactor is damaged)
        reactor = self.state.systems.get("reactor")
        if reactor and reactor.online and reactor.health < 70:
            if random.random() < self.BASE_CHANCES[EventType.POWER_SURGE]:
                events.append(Event(
                    EventType.POWER_SURGE,
                    "warning",
                    "Power surge from reactor! Systems may take damage.",
                    data={"damage": random.uniform(5, 15)}
                ))

        # Fire (if any system is overheating)
        hot_systems = [
            s for s in self.state.systems.values()
            if s.online and s.temperature > 80
        ]
        if hot_systems and random.random() < self.BASE_CHANCES[EventType.FIRE]:
            system = random.choice(hot_systems)
            if not system.on_fire:
                system.on_fire = True
                events.append(Event(
                    EventType.FIRE,
                    "critical",
                    f"Fire in {system.location}! {system.name} is burning!",
                    data={"system_id": system.id, "location": system.location}
                ))

        # Coolant leak
        coolant = self.state.systems.get("coolant_system")
        if coolant and coolant.online and coolant.health < 60:
            if random.random() < self.BASE_CHANCES[EventType.COOLANT_LEAK]:
                events.append(Event(
                    EventType.COOLANT_LEAK,
                    "warning",
                    "Coolant leak detected! Cooling efficiency reduced.",
                    duration=random.randint(10, 30),
                    data={"efficiency_penalty": 0.4}
                ))

        return events

    def _check_cat_events(self) -> list[Event]:
        """Check for cat-related events."""
        events = []
        cat = self.state.cat

        # Skip if cat not discovered
        if not cat.discovered:
            # Random chance to discover cat
            if random.random() < 0.001:
                cat.discovered = True
                events.append(Event(
                    EventType.CAT_FOUND,
                    "info",
                    f"Life form detected in {cat.location}! It appears to be a cat.",
                    data={"location": cat.location}
                ))
            return events

        # Cat hunger
        if cat.hunger > 70 and random.random() < self.BASE_CHANCES[EventType.CAT_HUNGRY]:
            events.append(Event(
                EventType.CAT_HUNGRY,
                "warning" if cat.hunger > 85 else "info",
                f"The cat is hungry. Hunger level: {cat.hunger:.0f}%",
                data={"hunger": cat.hunger}
            ))

        # Cat thirst
        if cat.thirst > 70 and random.random() < self.BASE_CHANCES[EventType.CAT_THIRSTY]:
            events.append(Event(
                EventType.CAT_THIRSTY,
                "warning" if cat.thirst > 85 else "info",
                f"The cat is thirsty. Thirst level: {cat.thirst:.0f}%",
                data={"thirst": cat.thirst}
            ))

        # Cat cold
        room_data = self.state.graph.get_entity(cat.location)
        if room_data:
            room_temp = room_data.get("temperature", 20)
            if room_temp < 18 and random.random() < self.BASE_CHANCES[EventType.CAT_COLD]:
                events.append(Event(
                    EventType.CAT_COLD,
                    "warning" if cat.warmth < 30 else "info",
                    f"The cat is cold. Room temperature: {room_temp:.1f}°C",
                    data={"temperature": room_temp, "warmth": cat.warmth}
                ))

        return events

    def _apply_event(self, event: Event) -> None:
        """Apply an event's immediate effects."""
        state = self.state

        if event.event_type == EventType.POWER_SURGE:
            # Damage random online systems
            damage = event.data.get("damage", 10)
            online_systems = [s for s in state.systems.values() if s.online]
            if online_systems:
                target = random.choice(online_systems)
                target.take_damage(damage)

        elif event.event_type == EventType.SYSTEM_MALFUNCTION:
            system = state.systems.get(event.data.get("system_id"))
            if system:
                system.take_damage(5)

        # Log the event
        state.log_event(
            event.event_type.value,
            event.message,
            severity=event.severity,
            **event.data
        )

    def _end_event(self, event: Event) -> None:
        """Handle event ending."""
        state = self.state

        if event.event_type == EventType.ASTEROID_FIELD:
            state.log_event(
                "event_end",
                "Cleared the asteroid field.",
                severity="info"
            )

        elif event.event_type == EventType.SOLAR_FLARE:
            state.log_event(
                "event_end",
                "Solar flare has subsided.",
                severity="info"
            )

        elif event.event_type == EventType.RADIATION_STORM:
            state.log_event(
                "event_end",
                "Radiation storm has passed.",
                severity="info"
            )

    def get_active_modifiers(self) -> dict:
        """Get combined modifiers from all active events."""
        modifiers = {
            "hull_damage_per_tick": 0.0,
            "sensor_penalty": 0.0,
            "memory_damage": 0.0,
            "coolant_penalty": 0.0,
        }

        for event in self.active_events:
            if event.event_type == EventType.ASTEROID_FIELD:
                modifiers["hull_damage_per_tick"] += event.data.get("damage_per_tick", 0)

            elif event.event_type == EventType.SOLAR_FLARE:
                modifiers["sensor_penalty"] += event.data.get("sensor_penalty", 0)

            elif event.event_type == EventType.RADIATION_STORM:
                modifiers["memory_damage"] += event.data.get("memory_damage", 0)

            elif event.event_type == EventType.COOLANT_LEAK:
                modifiers["coolant_penalty"] += event.data.get("efficiency_penalty", 0)

        return modifiers
