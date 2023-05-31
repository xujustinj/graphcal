"""
Loosely follows the definition of a Knowledge Graph given in
  Representation Learning for Dynamic (Knowledge) Graphs: A Survey
  Seyed Mehran Kazemi, Rishab Goel, Kshitij Jain, Ivan Kobyzev, Akshay Sethi, Peter Forsyth and Pascal Poupart
  Journal of Machine Learning Research (JMLR), 21(70):1-73, 2020.

This may be subject to change in the future.
"""

from dataclasses import dataclass, field
import json

from dataclasses_json import dataclass_json

Token = bool | int | float | str
Name = tuple[Token, ...]
Relation = str

@dataclass_json
@dataclass(frozen=True)
class Node:
    name: Name

    def __lt__(self, other: "Node") -> bool:
        assert isinstance(other, Node)
        return str(self.name) < str(other.name)

@dataclass_json
@dataclass(frozen=True)
class Edge:
    source: Node
    relation: Relation
    target: Node

    def __lt__(self, other: "Node") -> bool:
        assert isinstance(other, Node)
        return (
            str(self.relation) < str(other.relation)
            or self.source < other.source
            or self.target < other.target
        )

@dataclass
class KnowledgeGraph:
    nodes: set[Node] = field(default_factory=set)
    edges: set[Edge] = field(default_factory=set)
    relations: set[Relation] = field(default_factory=set)

    def add_node(self, v: Node, strict=False) -> "KnowledgeGraph":
        assert isinstance(v, Node)
        if strict:
            assert v not in self.nodes
        self.nodes.add(v)
        return self

    def add_edge(self, e: Edge, strict=False) -> "KnowledgeGraph":
        assert isinstance(e, Edge)
        assert e.source in self.nodes
        assert e.relation in self.relations
        assert e.target in self.nodes
        if strict:
            assert e not in self.edges
        self.edges.add(e)
        return self

    def add_relation(self, r: Relation, strict=False) -> "KnowledgeGraph":
        assert isinstance(r, Relation)
        if strict:
            assert r not in self.relations
        self.relations.add(r)
        return self

    def to_dict(self) -> dict[str, list]:
        return {
            "nodes": [node.to_dict() for node in sorted(self.nodes)],
            "edges": [edge.to_dict() for edge in sorted(self.edges)],
            "relations": sorted(self.relations),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, d: dict) -> "KnowledgeGraph":
        kg = KnowledgeGraph()
        for node in d["nodes"]:
            kg.add_node(node, strict=True)
        for relation in d["relations"]:
            kg.add_relation(relation, strict=True)
        for edge in d["edges"]:
            kg.add_edge(edge, strict=True)
        return kg

    @classmethod
    def from_json(cls, s: str) -> "KnowledgeGraph":
        d = json.loads(s)
        assert "nodes" in d
        assert "edges" in d
        assert "relations" in d
        assert len(d) == 3

        d["nodes"] = [Node.from_dict(node) for node in d["nodes"]]
        d["edges"] = [Edge.from_dict(edge) for edge in d["edges"]]
        return cls.from_dict(d)
