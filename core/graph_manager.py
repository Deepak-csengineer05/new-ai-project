import networkx as nx
import json
from typing import List, Dict, Set

class SkillGraph:
    """
    Manages the Directed Acyclic Graph (DAG) of skills using NetworkX.
    """
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_skill(self, skill_name: str, description: str = "", resources: List[str] = None):
        """Adds a skill node to the graph."""
        if resources is None:
            resources = []
        self.graph.add_node(skill_name, description=description, resources=resources, status="pending")

    def add_dependency(self, from_skill: str, to_skill: str, reason: str = ""):
        """
        Adds a dependency edge: from_skill -> to_skill.
        'from_skill' is a prerequisite for 'to_skill'.
        """
        self.graph.add_edge(from_skill, to_skill, reason=reason)

    def build_from_json(self, data: Dict):
        """
        Populates the graph from a JSON dictionary containing 'nodes' and 'edges'.
        Expected format:
        {
            "nodes": [{"id": "Skill A", "desc": "..."}],
            "edges": [{"source": "Skill A", "target": "Skill B", "reason": "..."}]
        }
        """
        self.graph.clear()
        for node in data.get("nodes", []):
            self.add_skill(node["id"], node.get("desc", ""), node.get("resources", []))
        
        for edge in data.get("edges", []):
            self.add_dependency(edge["source"], edge["target"], edge.get("reason", ""))

    def get_critical_path(self) -> List[str]:
        """Returns the longest path in the DAG (Critical Path)."""
        try:
            return nx.dag_longest_path(self.graph)
        except nx.NetworkXError:
            return [] # Graph might be empty or cyclic (though we aim for DAG)

    def get_prerequisites(self, skill: str) -> List[str]:
        """Returns immediate predecessors of a skill."""
        if skill in self.graph:
            return list(self.graph.predecessors(skill))
        return []

    def get_all_ancestors(self, skill: str) -> Set[str]:
        """Returns all recursive prerequisites."""
        if skill in self.graph:
            return nx.ancestors(self.graph, skill)
        return set()

    def get_blockers(self, skill: str) -> List[str]:
        """
        Returns uncompleted prerequisites for a skill.
        Assumes nodes have a 'status' attribute ('completed' or 'pending').
        """
        blockers = []
        for pred in self.get_prerequisites(skill):
            if self.graph.nodes[pred].get("status") != "completed":
                blockers.append(pred)
        return blockers

    def mark_completed(self, skill: str):
        """Marks a skill as completed."""
        if skill in self.graph:
            self.graph.nodes[skill]["status"] = "completed"

    def to_dict(self) -> Dict:
        """Serializes graph to dictionary for frontend or storage."""
        return nx.node_link_data(self.graph)

    def from_dict(self, data: Dict):
        """Loads graph from dictionary."""
        self.graph = nx.node_link_graph(data)
