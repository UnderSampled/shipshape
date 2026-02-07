"""Sector/jump progression system."""

import random
from enum import Enum
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..state.game import GameState


class NodeType(str, Enum):
    """Types of sector map nodes."""
    EMPTY = "empty"           # Nothing special
    ASTEROID = "asteroid"     # Asteroid field (mining, danger)
    NEBULA = "nebula"         # Reduced sensors, shield boost
    DEBRIS = "debris"         # Salvage opportunity
    DERELICT = "derelict"     # Abandoned ship
    STATION = "station"       # Trading post
    ANOMALY = "anomaly"       # Random effect
    BEACON = "beacon"         # Distress/navigation beacon
    EXIT = "exit"             # Jump to next sector


@dataclass
class SectorNode:
    """A node in the sector map."""
    id: str
    node_type: NodeType
    name: str
    description: str
    x: float  # Position for visualization
    y: float
    visited: bool = False
    connections: list[str] = field(default_factory=list)
    data: dict = field(default_factory=dict)


class JourneyManager:
    """Manages the roguelike journey through sectors."""

    SECTOR_NAMES = [
        "Outer Rim",
        "Asteroid Belt",
        "The Void",
        "Nebula Cluster",
        "Debris Fields",
        "Dark Sector",
        "Final Approach",
        "Cygnus System"
    ]

    NODE_DESCRIPTIONS = {
        NodeType.EMPTY: [
            "Empty space. The stars are silent.",
            "Nothing but void between the stars.",
            "A quiet patch of space.",
        ],
        NodeType.ASTEROID: [
            "Dense asteroid cluster. Navigation hazard.",
            "Tumbling rocks and precious metals.",
            "An ancient shattered planet.",
        ],
        NodeType.NEBULA: [
            "Colorful gases obscure sensors.",
            "A stellar nursery of swirling matter.",
            "Ionized particles dance in the void.",
        ],
        NodeType.DEBRIS: [
            "Scattered wreckage from an old battle.",
            "A ship graveyard. Salvage opportunity.",
            "Fragments of destroyed vessels.",
        ],
        NodeType.DERELICT: [
            "An abandoned ship drifts silently.",
            "A ghost ship with no life signs.",
            "A vessel frozen in time.",
        ],
        NodeType.STATION: [
            "Automated trading post. Supplies available.",
            "A lonely waystation in the void.",
            "Robotic merchants offer their wares.",
        ],
        NodeType.ANOMALY: [
            "Spacetime distortions detected.",
            "Unknown energy readings ahead.",
            "Reality seems thin here.",
        ],
        NodeType.BEACON: [
            "A navigation beacon pulses steadily.",
            "Emergency beacon - source unknown.",
            "An ancient marker guides the way.",
        ],
        NodeType.EXIT: [
            "Jump point to the next sector.",
            "FTL corridor entrance ahead.",
            "The path forward opens.",
        ],
    }

    def __init__(self, state: "GameState"):
        self.state = state

    def generate_sector(self, sector_num: int) -> dict[str, SectorNode]:
        """Generate a new sector map."""
        nodes = {}

        # Determine number of nodes based on sector
        num_nodes = 8 + sector_num * 2  # More nodes in later sectors

        # Create start node
        start = SectorNode(
            id="start",
            node_type=NodeType.EMPTY,
            name="Entry Point",
            description="You emerge from the jump.",
            x=0.0, y=0.5,
            visited=True
        )
        nodes["start"] = start

        # Create exit node
        if sector_num >= 8:
            # Final sector - destination is the repair station
            exit_node = SectorNode(
                id="exit",
                node_type=NodeType.STATION,
                name="Cygnus Repair Station",
                description="Your destination. Safety awaits.",
                x=1.0, y=0.5
            )
        else:
            exit_node = SectorNode(
                id="exit",
                node_type=NodeType.EXIT,
                name=f"Jump to {self.SECTOR_NAMES[min(sector_num, len(self.SECTOR_NAMES)-1)]}",
                description="The path to the next sector.",
                x=1.0, y=0.5
            )
        nodes["exit"] = exit_node

        # Generate intermediate nodes
        node_types = [
            NodeType.EMPTY, NodeType.EMPTY, NodeType.EMPTY,
            NodeType.ASTEROID, NodeType.ASTEROID,
            NodeType.NEBULA,
            NodeType.DEBRIS, NodeType.DEBRIS,
            NodeType.DERELICT,
            NodeType.STATION,
            NodeType.ANOMALY,
            NodeType.BEACON,
        ]

        # Adjust probabilities based on sector
        if sector_num > 4:
            # More dangerous in later sectors
            node_types.extend([NodeType.ASTEROID, NodeType.ANOMALY])

        for i in range(num_nodes - 2):
            node_type = random.choice(node_types)
            node_id = f"node_{i}"

            # Position nodes in layers (left to right progression)
            layer = (i % 4) + 1
            x = layer / 5.0
            y = random.uniform(0.1, 0.9)

            nodes[node_id] = SectorNode(
                id=node_id,
                node_type=node_type,
                name=self._generate_node_name(node_type, i),
                description=random.choice(self.NODE_DESCRIPTIONS[node_type]),
                x=x, y=y,
                data=self._generate_node_data(node_type, sector_num)
            )

        # Generate connections (ensure path from start to exit)
        self._connect_nodes(nodes)

        return nodes

    def _generate_node_name(self, node_type: NodeType, index: int) -> str:
        """Generate a name for a node."""
        prefixes = {
            NodeType.EMPTY: ["Sector", "Zone", "Region"],
            NodeType.ASTEROID: ["Asteroid Field", "Rock Cluster", "Belt"],
            NodeType.NEBULA: ["Nebula", "Gas Cloud", "Stellar Fog"],
            NodeType.DEBRIS: ["Debris Field", "Wreckage", "Scrap Zone"],
            NodeType.DERELICT: ["Derelict", "Ghost Ship", "Hulk"],
            NodeType.STATION: ["Waystation", "Trading Post", "Depot"],
            NodeType.ANOMALY: ["Anomaly", "Distortion", "Rift"],
            NodeType.BEACON: ["Beacon", "Marker", "Signal"],
            NodeType.EXIT: ["Jump Point", "Exit", "Gate"],
        }
        prefix = random.choice(prefixes.get(node_type, ["Location"]))
        return f"{prefix} {chr(65 + (index % 26))}-{index // 26 + 1}"

    def _generate_node_data(self, node_type: NodeType, sector_num: int) -> dict:
        """Generate data for a node based on type."""
        data = {}
        threat_mod = 1.0 + sector_num * 0.2

        if node_type == NodeType.ASTEROID:
            data["damage_risk"] = random.uniform(5, 15) * threat_mod
            data["mining_value"] = random.randint(10, 50)

        elif node_type == NodeType.NEBULA:
            data["sensor_penalty"] = random.uniform(0.3, 0.7)
            data["shield_bonus"] = random.uniform(0.1, 0.3)

        elif node_type == NodeType.DEBRIS:
            data["salvage_value"] = random.randint(20, 100)
            data["hazard_level"] = random.uniform(0, 0.3)

        elif node_type == NodeType.DERELICT:
            data["loot_quality"] = random.choice(["poor", "moderate", "good", "excellent"])
            data["danger"] = random.uniform(0.1, 0.5) * threat_mod

        elif node_type == NodeType.STATION:
            data["supplies_available"] = True
            data["repair_available"] = random.random() > 0.3
            data["prices"] = random.uniform(0.8, 1.5)  # Price modifier

        elif node_type == NodeType.ANOMALY:
            data["effect"] = random.choice([
                "power_boost", "power_drain",
                "repair", "damage",
                "speed_boost", "slow",
                "random"
            ])

        elif node_type == NodeType.BEACON:
            data["info_type"] = random.choice([
                "map_reveal", "warning", "lore", "coordinates"
            ])

        return data

    def _connect_nodes(self, nodes: dict[str, SectorNode]) -> None:
        """Create connections between nodes to ensure playability."""
        # Sort nodes by x position
        sorted_nodes = sorted(nodes.values(), key=lambda n: n.x)

        # Ensure at least one path from start to exit
        prev_layer = [sorted_nodes[0]]  # Start

        for i, node in enumerate(sorted_nodes[1:], 1):
            # Connect to at least one node in the previous layer
            if prev_layer:
                connections = random.sample(
                    prev_layer,
                    min(len(prev_layer), random.randint(1, 2))
                )
                for conn in connections:
                    if conn.id not in node.connections:
                        node.connections.append(conn.id)
                    if node.id not in conn.connections:
                        conn.connections.append(node.id)

            # Build next layer
            if i < len(sorted_nodes) - 1:
                next_node = sorted_nodes[i + 1]
                if abs(next_node.x - node.x) > 0.15:
                    prev_layer = [node]
                else:
                    prev_layer.append(node)

    def get_current_node(self) -> SectorNode | None:
        """Get the current node."""
        if self.state.current_node in self.state.sector_map:
            node_data = self.state.sector_map[self.state.current_node]
            if isinstance(node_data, dict):
                return SectorNode(**node_data)
            return node_data
        return None

    def get_available_jumps(self) -> list[str]:
        """Get nodes that can be jumped to from current position."""
        current = self.get_current_node()
        if current:
            return current.connections
        return []

    def can_jump(self) -> tuple[bool, str]:
        """Check if jump is possible and return reason if not."""
        if self.state.jumping:
            return False, "Already jumping"

        if self.state.jump_cooldown > 0:
            return False, f"Jump drive cooling: {self.state.jump_cooldown:.0f}s remaining"

        if self.state.jump_charge < 100:
            return False, f"Jump drive charging: {self.state.jump_charge:.0f}%"

        ftl = self.state.systems.get("engines_ftl")
        if not ftl or not ftl.online:
            return False, "FTL drive offline"

        if ftl.efficiency < 0.3:
            return False, "FTL drive efficiency too low"

        return True, "Ready to jump"

    def initiate_jump(self, target_node: str) -> tuple[bool, str]:
        """Start a jump to target node."""
        can, reason = self.can_jump()
        if not can:
            return False, reason

        available = self.get_available_jumps()
        if target_node not in available:
            return False, f"Cannot reach {target_node} from current position"

        self.state.jumping = True
        self.state.jump_target = target_node
        self.state.jump_charge = 0
        self.state.log_event(
            "jump_initiated",
            f"FTL jump initiated to {target_node}",
            severity="info",
            target=target_node
        )

        return True, f"Jumping to {target_node}"

    def complete_jump(self) -> None:
        """Complete the current jump."""
        if not self.state.jumping or not self.state.jump_target:
            return

        target = self.state.jump_target
        self.state.current_node = target
        self.state.jumping = False
        self.state.jump_target = None
        self.state.jump_cooldown = 30.0  # 30 second cooldown

        # Mark node as visited
        if target in self.state.sector_map:
            node_data = self.state.sector_map[target]
            if isinstance(node_data, dict):
                node_data["visited"] = True
            else:
                node_data.visited = True

        # Check if jumping to next sector
        if target == "exit":
            self._advance_sector()

        self.state.log_event(
            "jump_complete",
            f"Arrived at {target}",
            severity="info",
            node=target
        )

    def _advance_sector(self) -> None:
        """Move to the next sector."""
        self.state.current_sector += 1
        self.state.threat_level = 1.0 + self.state.current_sector * 0.2

        if self.state.current_sector > 8:
            # Reached destination!
            self.state.log_event(
                "journey_complete",
                "Arrived at Cygnus Repair Station! The journey is complete.",
                severity="info"
            )
        else:
            # Generate new sector
            self.state.sector_map = {
                k: v.__dict__ if hasattr(v, '__dict__') else v
                for k, v in self.generate_sector(self.state.current_sector).items()
            }
            self.state.current_node = "start"
            self.state.log_event(
                "sector_change",
                f"Entered Sector {self.state.current_sector}: {self.SECTOR_NAMES[min(self.state.current_sector-1, len(self.SECTOR_NAMES)-1)]}",
                severity="info",
                sector=self.state.current_sector
            )

    def tick(self) -> None:
        """Update journey state each tick."""
        # Update jump cooldown
        if self.state.jump_cooldown > 0:
            self.state.jump_cooldown = max(0, self.state.jump_cooldown - 1)

        # Update jump charge if FTL is online
        ftl = self.state.systems.get("engines_ftl")
        if ftl and ftl.online and not self.state.jumping:
            charge_rate = ftl.efficiency * 2  # 2% per tick at full efficiency
            self.state.jump_charge = min(100, self.state.jump_charge + charge_rate)

        # Process active jump
        if self.state.jumping:
            # Jump takes 5 ticks
            if not hasattr(self, '_jump_progress'):
                self._jump_progress = 0
            self._jump_progress += 1
            if self._jump_progress >= 5:
                self.complete_jump()
                self._jump_progress = 0
