from .graph import Node, Edge, KnowledgeGraph

kg = KnowledgeGraph() \
    .add_node(node_knowledge := Node(("knowledge", 0))) \
    .add_node(node_graph := Node((1, "graph"))) \
    .add_relation("represents") \
    .add_edge(Edge(node_knowledge, "represents", node_graph))

# TEST: serialization / deserialization
s = kg.to_json()
print(s)
assert kg == KnowledgeGraph.from_json(s)

# TEST: the nodes are what we think they are
a = kg.all()
assert a == {node_knowledge, node_graph}

# TEST: editing kg.all() does not affect the knowledge graph
a.remove(node_graph)
assert kg.all() == {node_knowledge, node_graph}

# TEST: targets and sources
ns = kg.one(("knowledge", 0))
assert kg.targets(ns) == kg.one((1, "graph"))
assert kg.targets(ns, relations="not a relation") == set()
assert kg.sources(ns) == set()
