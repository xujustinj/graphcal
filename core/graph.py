"""
Loosely follows the definition of a Knowledge Graph given in
  Representation Learning for Dynamic (Knowledge) Graphs: A Survey
  Seyed Mehran Kazemi, Rishab Goel, Kshitij Jain, Ivan Kobyzev, Akshay Sethi, Peter Forsyth and Pascal Poupart
  Journal of Machine Learning Research (JMLR), 21(70):1-73, 2020.

This may be subject to change in the future.
"""

from dataclasses import dataclass, field
import json
import re
from typing import Optional

from dataclasses_json import dataclass_json

Token = None | bool | int | float | str
Name = tuple[Token, ...]
Relation = str

@dataclass_json
@dataclass(frozen=True)
class Node:
    name: Name

    def __lt__(self, other: "Node") -> bool:
        assert isinstance(other, Node)
        return str(self.name) < str(other.name)

NodeSet = set[Node]

@dataclass_json
@dataclass(frozen=True)
class Edge:
    source: Node
    relation: Relation
    target: Node

    def __lt__(self, other: "Edge") -> bool:
        assert isinstance(other, Edge)
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

    # Add operations

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

    # Remove operations

    def remove_node(self, v: Node, strict=False) -> "KnowledgeGraph":
        assert isinstance(v, Node)
        for edge in self.edges:
            assert edge.source != v and edge.target != v
        if strict:
            assert v in self.nodes
            self.nodes.remove(v)
        elif v in self.nodes:
            self.nodes.remove(v)
        return self

    def remove_edge(self, e: Edge, strict=False) -> "KnowledgeGraph":
        assert isinstance(e, Edge)
        assert e.source in self.nodes
        assert e.relation in self.relations
        assert e.target in self.nodes
        if strict:
            assert e not in self.edges
            self.edges.remove(e)
        elif e in self.edges:
            self.edges.remove(e)
        return self

    def remove_relation(self, r: Relation, strict=False) -> "KnowledgeGraph":
        assert isinstance(r, Relation)
        for edge in self.edges:
            assert edge.relation != r
        if strict:
            assert r in self.relations
            self.relations.remove(r)
        elif r in self.relations:
            self.relations.remove(r)
        return self

    # Copy

    def copy(self) -> "KnowledgeGraph":
        return KnowledgeGraph(
            nodes=set(self.nodes),
            edges=set(self.edges),
            relations=set(self.relations),
        )

    # Query operations

    def all(self) -> NodeSet:
        return set(self.nodes)

    def one(self, name: Name) -> NodeSet:
        node = Node(name)
        assert node in self.nodes
        return {node}

    def targets(
        self,
        sources: NodeSet,
        relations: Optional[str | re.Pattern] = None
    ) -> NodeSet:
        if isinstance(relations, str):
            relations = re.compile(relations)
        return {
            edge.target
            for edge in self.edges
            if edge.source in sources
            and (relations is None or relations.match(edge.relation))
        }

    def sources(
        self,
        targets: NodeSet,
        relations: Optional[str | re.Pattern] = None
    ) -> NodeSet:
        if isinstance(relations, str):
            relations = re.compile(relations)
        return {
            edge.source
            for edge in self.edges
            if edge.target in targets
            and (relations is None or relations.match(edge.relation))
        }

    # JSON serialization

    def to_dict(self) -> dict[str, list]:
        return {
            "nodes": [node.to_dict() for node in sorted(self.nodes)],
            "edges": [edge.to_dict() for edge in sorted(self.edges)],
            "relations": sorted(self.relations),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    # JSON deserialization

    @classmethod
    def from_dict(cls, d: dict) -> "KnowledgeGraph":
        kg = cls()
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
