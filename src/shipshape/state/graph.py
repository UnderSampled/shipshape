"""Graph-based state store using NetworkX for MUD-style relationships."""

from typing import Any
import networkx as nx


class GraphState:
    """
    MUD-style prepositional relationship graph.

    Node types: room, robot, item, system, cat
    Edge types with prepositions: "in", "on", "connected_to", "north_of", etc.
    """

    def __init__(self):
        self.graph = nx.MultiDiGraph()

    def add_entity(self, entity_id: str, entity_type: str, **attributes) -> None:
        """Add an entity (node) to the graph."""
        self.graph.add_node(entity_id, entity_type=entity_type, **attributes)

    def update_entity(self, entity_id: str, **attributes) -> None:
        """Update attributes of an existing entity."""
        if entity_id in self.graph:
            self.graph.nodes[entity_id].update(attributes)

    def get_entity(self, entity_id: str) -> dict[str, Any] | None:
        """Get an entity's attributes."""
        if entity_id in self.graph:
            return dict(self.graph.nodes[entity_id])
        return None

    def remove_entity(self, entity_id: str) -> None:
        """Remove an entity and all its relations."""
        if entity_id in self.graph:
            self.graph.remove_node(entity_id)

    def add_relation(self, subject: str, predicate: str, obj: str, **attributes) -> None:
        """
        Add a relationship between entities.

        Example: add_relation("robot_1", "in", "engine_room")
        """
        self.graph.add_edge(subject, obj, predicate=predicate, **attributes)

    def remove_relation(self, subject: str, predicate: str, obj: str) -> None:
        """Remove a specific relationship."""
        edges_to_remove = []
        for key in self.graph[subject].get(obj, {}):
            if self.graph[subject][obj][key].get("predicate") == predicate:
                edges_to_remove.append(key)
        for key in edges_to_remove:
            self.graph.remove_edge(subject, obj, key)

    def remove_relations(self, subject: str, predicate: str) -> None:
        """Remove all relations of a type from a subject."""
        edges_to_remove = []
        for _, target, key, data in self.graph.out_edges(subject, keys=True, data=True):
            if data.get("predicate") == predicate:
                edges_to_remove.append((subject, target, key))
        for edge in edges_to_remove:
            self.graph.remove_edge(*edge)

    def query(
        self,
        subject: str | None = None,
        predicate: str | None = None,
        obj: str | None = None
    ) -> list[tuple[str, str, str, dict]]:
        """
        Query relationships matching the given pattern.

        Returns list of (subject, predicate, object, attributes) tuples.
        """
        results = []

        if subject is not None:
            # Query from specific subject
            if subject not in self.graph:
                return results
            for _, target, data in self.graph.out_edges(subject, data=True):
                if predicate is not None and data.get("predicate") != predicate:
                    continue
                if obj is not None and target != obj:
                    continue
                results.append((subject, data.get("predicate", ""), target, data))
        elif obj is not None:
            # Query to specific object
            if obj not in self.graph:
                return results
            for source, _, data in self.graph.in_edges(obj, data=True):
                if predicate is not None and data.get("predicate") != predicate:
                    continue
                results.append((source, data.get("predicate", ""), obj, data))
        else:
            # Query all edges
            for source, target, data in self.graph.edges(data=True):
                if predicate is not None and data.get("predicate") != predicate:
                    continue
                results.append((source, data.get("predicate", ""), target, data))

        return results

    def get_contents(self, location_id: str) -> list[str]:
        """Get all entities that are 'in' a location."""
        results = []
        for source, _, data in self.graph.in_edges(location_id, data=True):
            if data.get("predicate") == "in":
                results.append(source)
        return results

    def get_location(self, entity_id: str) -> str | None:
        """Get the location of an entity (where it is 'in')."""
        for _, target, data in self.graph.out_edges(entity_id, data=True):
            if data.get("predicate") == "in":
                return target
        return None

    def get_entities_by_type(self, entity_type: str) -> list[str]:
        """Get all entity IDs of a specific type."""
        return [
            node for node, data in self.graph.nodes(data=True)
            if data.get("entity_type") == entity_type
        ]

    def get_connected_rooms(self, room_id: str) -> list[tuple[str, str]]:
        """Get rooms connected to this room with their direction."""
        results = []
        for _, target, data in self.graph.out_edges(room_id, data=True):
            if data.get("predicate") == "connected_to":
                direction = data.get("direction", "")
                results.append((target, direction))
        return results

    def to_dict(self) -> dict:
        """Serialize graph to dictionary for saving."""
        return {
            "nodes": [
                {"id": node, **data}
                for node, data in self.graph.nodes(data=True)
            ],
            "edges": [
                {"source": u, "target": v, **data}
                for u, v, data in self.graph.edges(data=True)
            ]
        }

    def from_dict(self, data: dict) -> None:
        """Load graph from dictionary."""
        self.graph.clear()
        for node_data in data.get("nodes", []):
            node_id = node_data.pop("id")
            self.graph.add_node(node_id, **node_data)
        for edge_data in data.get("edges", []):
            source = edge_data.pop("source")
            target = edge_data.pop("target")
            self.graph.add_edge(source, target, **edge_data)
