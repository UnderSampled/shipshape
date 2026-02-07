"""Main simulation loop running in a separate thread."""

import time
import random
import threading
from typing import TYPE_CHECKING

from .events import EventGenerator
from .journey import JourneyManager
from .robots import Task, TaskType, RobotStatus

if TYPE_CHECKING:
    from ..state.game import GameState


class SimulationEngine:
    """
    Main simulation engine running in a separate thread.

    Updates all game state at a fixed tick rate.
    """

    def __init__(self, state: "GameState", tick_rate: float = 1.0):
        """
        Initialize the simulation engine.

        Args:
            state: The shared game state
            tick_rate: Ticks per second (default 1.0)
        """
        self.state = state
        self.tick_rate = tick_rate
        self.tick_interval = 1.0 / tick_rate

        self._thread: threading.Thread | None = None
        self._running = False
        self._paused = False

        self.event_generator = EventGenerator(state)
        self.journey_manager = JourneyManager(state)

    def start(self) -> None:
        """Start the simulation thread."""
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop the simulation thread."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
            self._thread = None

    def pause(self) -> None:
        """Pause the simulation."""
        self._paused = True

    def resume(self) -> None:
        """Resume the simulation."""
        self._paused = False

    @property
    def is_running(self) -> bool:
        return self._running and not self._paused

    def _run_loop(self) -> None:
        """Main simulation loop."""
        last_tick = time.time()

        while self._running:
            current_time = time.time()
            elapsed = current_time - last_tick

            if elapsed >= self.tick_interval and not self._paused:
                self._tick()
                last_tick = current_time

            # Sleep a bit to not burn CPU
            time.sleep(0.05)

    def _tick(self) -> None:
        """Process one simulation tick."""
        with self.state.lock():
            self.state.current_tick += 1

            # Get event modifiers
            modifiers = self.event_generator.get_active_modifiers()

            # Update systems
            self._update_systems(modifiers)

            # Update robots
            self._update_robots(modifiers)

            # Update cat
            self._update_cat()

            # Update journey
            self.journey_manager.tick()

            # Apply ongoing damage from events
            if modifiers["hull_damage_per_tick"] > 0:
                shields = self.state.systems.get("shields")
                damage = modifiers["hull_damage_per_tick"]

                # Shields absorb some damage
                if shields and shields.online:
                    absorbed = damage * shields.efficiency
                    damage -= absorbed

                if damage > 0:
                    self.state.hull_integrity = max(0, self.state.hull_integrity - damage)

            # Generate new events
            self.event_generator.tick()

            # Update power calculations
            self.state.total_power = self.state.calculate_total_power()
            self.state.power_allocated = self.state.calculate_power_allocated()

    def _update_systems(self, modifiers: dict) -> None:
        """Update all ship systems."""
        coolant = self.state.systems.get("coolant_system")
        coolant_eff = coolant.efficiency if coolant and coolant.online else 0.0

        # Apply coolant leak penalty
        coolant_eff = max(0, coolant_eff - modifiers.get("coolant_penalty", 0))

        for system in self.state.systems.values():
            if system.online:
                events = system.tick(coolant_eff)
                for event_msg in events:
                    self.state.log_event("system", event_msg, severity="warning")

    def _update_robots(self, modifiers: dict) -> None:
        """Update all robots."""
        coolant = self.state.systems.get("coolant_system")
        coolant_available = coolant and coolant.online and coolant.efficiency > 0.3

        for robot in self.state.robots.values():
            # Apply radiation damage to memory
            memory_damage = modifiers.get("memory_damage", 0)
            if memory_damage > 0:
                robot.degrade_memory(memory_damage)

            # Run robot tick
            events = robot.tick(
                ambient_temp=20.0,
                coolant_available=coolant_available
            )
            for event_msg in events:
                self.state.log_event("robot", event_msg, severity="warning")

            # Process robot tasks and AI
            if robot.is_functional:
                self._process_robot_ai(robot)

    def _process_robot_ai(self, robot) -> None:
        """Process robot AI decision making."""
        # Check for urgent needs that override tasks
        urgent_need = robot.most_urgent_need
        if urgent_need and urgent_need.endswith("_critical"):
            self._handle_urgent_need(robot, urgent_need)
            return

        # If currently moving, continue movement
        if robot.status == RobotStatus.MOVING:
            self._process_movement(robot)
            return

        # If charging, continue charging
        if robot.status == RobotStatus.CHARGING:
            self._process_charging(robot)
            return

        # If working on a task, continue task
        if robot.current_task and robot.status == RobotStatus.WORKING:
            self._process_task(robot)
            return

        # If idle with no task, handle needs or pick up queued task
        if robot.status == RobotStatus.IDLE:
            if urgent_need:
                self._handle_need(robot, urgent_need)
            elif robot.task_queue:
                robot.current_task = robot.task_queue.pop(0)
                robot.status = RobotStatus.WORKING

    def _handle_urgent_need(self, robot, need: str) -> None:
        """Handle critical robot needs."""
        if need == "power_critical":
            # Must charge immediately
            if robot.location == "charging_station":
                robot.status = RobotStatus.CHARGING
            else:
                # Move to charging station
                robot.move_target = "charging_station"
                robot.move_progress = 0
                robot.status = RobotStatus.MOVING

        elif need == "cooling_critical":
            # Find coolest room (coolant room)
            if robot.location != "coolant_room":
                robot.move_target = "coolant_room"
                robot.move_progress = 0
                robot.status = RobotStatus.MOVING

    def _handle_need(self, robot, need: str) -> None:
        """Handle non-critical robot needs."""
        if need == "charge" and robot.location != "charging_station":
            robot.move_target = "charging_station"
            robot.move_progress = 0
            robot.status = RobotStatus.MOVING

        elif need == "charge" and robot.location == "charging_station":
            robot.status = RobotStatus.CHARGING

        elif need == "cooling" and robot.location != "coolant_room":
            robot.move_target = "coolant_room"
            robot.move_progress = 0
            robot.status = RobotStatus.MOVING

        elif need == "maintenance" and robot.location != "repair_bay":
            robot.move_target = "repair_bay"
            robot.move_progress = 0
            robot.status = RobotStatus.MOVING

        elif need == "sync":
            # Sync can happen anywhere if data core is online
            data_core = self.state.systems.get("data_core_system")
            if data_core and data_core.online:
                robot.sync_memory(5.0 * data_core.efficiency)

    def _process_movement(self, robot) -> None:
        """Process robot movement between rooms."""
        if not robot.move_target:
            robot.status = RobotStatus.IDLE
            return

        # Movement takes ~5 ticks per room
        robot.move_progress += 20
        robot.consume_power(0.5)  # Movement costs power

        if robot.move_progress >= 100:
            # Arrived at destination
            old_location = robot.location
            robot.location = robot.move_target
            robot.move_target = None
            robot.move_progress = 0
            robot.status = RobotStatus.IDLE

            # Update graph
            self.state.graph.remove_relations(robot.id, "in")
            self.state.graph.add_relation(robot.id, "in", robot.location)

    def _process_charging(self, robot) -> None:
        """Process robot charging."""
        charging_system = self.state.systems.get("charging_system")
        if not charging_system or not charging_system.online:
            # Can't charge, return to idle
            robot.status = RobotStatus.IDLE
            return

        # Charge based on system efficiency
        charge_rate = 5.0 * charging_system.efficiency
        robot.charge(charge_rate)

        # Stop charging when full or if urgent task
        if robot.power_level >= 95 or (robot.current_task and robot.current_task.priority <= 2):
            robot.status = RobotStatus.IDLE

    def _process_task(self, robot) -> None:
        """Process robot task execution."""
        task = robot.current_task
        if not task:
            robot.status = RobotStatus.IDLE
            return

        # Check if at correct location for task
        target_location = self._get_task_location(task)
        if target_location and robot.location != target_location:
            robot.move_target = target_location
            robot.move_progress = 0
            robot.status = RobotStatus.MOVING
            return

        # Execute task
        progress_rate = 10.0 + (robot.efficiency / 10.0)  # Base + efficiency bonus
        robot.consume_power(0.3)
        robot.heat_up(0.2)

        if task.task_type == TaskType.REPAIR_SYSTEM:
            system = self.state.systems.get(task.target)
            if system:
                repair_amount = (robot.repair_skill / 100.0) * 2.0
                system.repair(repair_amount)
                task.progress += progress_rate
                if system.health >= 100:
                    task.progress = 100

        elif task.task_type == TaskType.OPERATE_SYSTEM:
            system = self.state.systems.get(task.target)
            if system and robot.id not in system.manned_by:
                system.manned_by.append(robot.id)
            # Operating is ongoing, slow progress
            task.progress += 1

        elif task.task_type == TaskType.FIGHT_FIRE:
            system = self.state.systems.get(task.target)
            if system and system.on_fire:
                # 20% chance per tick to extinguish
                if random.random() < 0.2:
                    system.on_fire = False
                    task.progress = 100
                else:
                    task.progress += progress_rate

        elif task.task_type == TaskType.FEED_CAT:
            bowl = self.state.graph.get_entity("cat_food_bowl")
            if bowl:
                self.state.graph.update_entity("cat_food_bowl", filled=True, contents=100.0)
                task.progress = 100

        elif task.task_type == TaskType.WATER_CAT:
            bowl = self.state.graph.get_entity("cat_water_bowl")
            if bowl:
                self.state.graph.update_entity("cat_water_bowl", filled=True, contents=100.0)
                task.progress = 100

        elif task.task_type == TaskType.REPAIR_ROBOT:
            target_robot = self.state.robots.get(task.target)
            if target_robot:
                repair_amount = (robot.repair_skill / 100.0) * 3.0
                target_robot.repair(repair_amount)
                task.progress += progress_rate
                if target_robot.maintenance >= 100:
                    task.progress = 100

        else:
            # Generic task progress
            task.progress += progress_rate

        # Check if task complete
        if task.is_complete:
            # Clean up
            if task.task_type == TaskType.OPERATE_SYSTEM:
                system = self.state.systems.get(task.target)
                if system and robot.id in system.manned_by:
                    system.manned_by.remove(robot.id)

            self.state.log_event(
                "task_complete",
                f"{robot.designation} completed: {task.task_type.value}",
                severity="info",
                robot=robot.id,
                task=task.task_type.value
            )
            robot.complete_current_task()

    def _get_task_location(self, task: Task) -> str | None:
        """Get the location where a task should be performed."""
        if task.task_type == TaskType.REPAIR_SYSTEM:
            system = self.state.systems.get(task.target)
            return system.location if system else None

        elif task.task_type == TaskType.OPERATE_SYSTEM:
            system = self.state.systems.get(task.target)
            return system.location if system else None

        elif task.task_type == TaskType.FIGHT_FIRE:
            system = self.state.systems.get(task.target)
            return system.location if system else None

        elif task.task_type == TaskType.CHARGE:
            return "charging_station"

        elif task.task_type == TaskType.REPAIR_ROBOT:
            return "repair_bay"

        elif task.task_type == TaskType.FEED_CAT:
            return "mess_hall"

        elif task.task_type == TaskType.WATER_CAT:
            return "mess_hall"

        elif task.task_type == TaskType.MOVE_TO:
            return task.target

        return task.data.get("location")

    def _update_cat(self) -> None:
        """Update the cat's state."""
        cat = self.state.cat

        # Increase needs over time
        cat.hunger = min(100, cat.hunger + 0.05)
        cat.thirst = min(100, cat.thirst + 0.08)

        # Get room temperature
        room_data = self.state.graph.get_entity(cat.location)
        if room_data:
            room_temp = room_data.get("temperature", 15)
            # Warmth based on room temp (comfort zone 20-25)
            if room_temp < 18:
                cat.warmth = max(0, cat.warmth - 0.5)
            elif room_temp > 25:
                cat.warmth = min(100, cat.warmth + 0.2)
            else:
                # Comfort zone, warmth trends to 70
                if cat.warmth < 70:
                    cat.warmth = min(70, cat.warmth + 0.3)
                elif cat.warmth > 70:
                    cat.warmth = max(70, cat.warmth - 0.1)

        # Check food bowl
        food_bowl = self.state.graph.get_entity("cat_food_bowl")
        if food_bowl and food_bowl.get("filled") and cat.location == "mess_hall":
            if cat.hunger > 30 and random.random() < 0.1:
                # Cat eats
                cat.hunger = max(0, cat.hunger - 30)
                new_contents = max(0, food_bowl.get("contents", 0) - 20)
                self.state.graph.update_entity(
                    "cat_food_bowl",
                    contents=new_contents,
                    filled=new_contents > 0
                )
                cat.status = cat.status  # Will be updated below

        # Check water bowl
        water_bowl = self.state.graph.get_entity("cat_water_bowl")
        if water_bowl and water_bowl.get("filled") and cat.location == "mess_hall":
            if cat.thirst > 30 and random.random() < 0.15:
                # Cat drinks
                cat.thirst = max(0, cat.thirst - 25)
                new_contents = max(0, water_bowl.get("contents", 0) - 15)
                self.state.graph.update_entity(
                    "cat_water_bowl",
                    contents=new_contents,
                    filled=new_contents > 0
                )

        # Update cat health based on needs
        if cat.hunger > 90 or cat.thirst > 90 or cat.warmth < 20:
            cat.health = max(0, cat.health - 0.1)
        elif cat.hunger < 30 and cat.thirst < 30 and cat.warmth > 40:
            cat.health = min(100, cat.health + 0.02)

        # Update happiness
        happiness_factors = [
            100 - cat.hunger,
            100 - cat.thirst,
            cat.warmth,
            cat.health
        ]
        cat.happiness = sum(happiness_factors) / len(happiness_factors)

        # Update cat status based on state
        if cat.health < 30:
            cat.status = cat.status.__class__.DISTRESSED
        elif cat.hunger > 80 or cat.thirst > 80:
            cat.status = cat.status.__class__.DISTRESSED
        elif cat.warmth < 30:
            cat.status = cat.status.__class__.HIDING
        elif random.random() < 0.01:
            # Random status changes
            cat.status = random.choice([
                cat.status.__class__.SLEEPING,
                cat.status.__class__.WANDERING,
                cat.status.__class__.PLAYING
            ])

        # Cat wandering behavior
        if cat.status == cat.status.__class__.WANDERING and random.random() < 0.02:
            # Move to adjacent room
            connected = self.state.graph.get_connected_rooms(cat.location)
            if connected:
                new_room, _ = random.choice(connected)
                # Prefer certain rooms
                preferred = ["recreation_room", "observation_deck", "mess_hall"]
                for room in preferred:
                    if any(r == room for r, _ in connected):
                        if random.random() < 0.3:
                            new_room = room
                            break

                self.state.graph.remove_relations(cat.id if hasattr(cat, 'id') else "cat", "in")
                cat.location = new_room
                self.state.graph.add_relation("cat", "in", new_room)
