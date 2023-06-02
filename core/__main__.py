from .graph import Node, Edge, KnowledgeGraph

kg = KnowledgeGraph()

# TEST: adding
kg \
    .add_node(node_knowledge := Node(("knowledge", 0))) \
    .add_node(node_graph := Node((1, "graph"))) \
    .add_relation("represents") \
    .add_edge(edge := Edge(node_graph, "represents", node_knowledge))

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

# TEST: querying by name
set_knowledge = kg.one(("knowledge", 0))
set_graph = kg.one((1, "graph"))
assert set_knowledge == {node_knowledge}
assert set_graph == {node_graph}

# TEST: targets
assert kg.targets(set_knowledge) == set()
assert kg.targets(set_graph) == set_knowledge
assert kg.targets(set_graph, relations="^represents$") == set_knowledge
assert kg.targets(set_graph, relations="^Represents$") == set()

# TEST: sources
assert kg.sources(set_knowledge) == set_graph
assert kg.sources(set_knowledge, relations="^represents$") == set_graph
assert kg.sources(set_knowledge, relations="^Represents$") == set()
assert kg.sources(set_graph) == set()

# TEST: copying
cp = kg.copy()
assert cp == kg

# TEST: removing
cp \
    .remove_edge(edge) \
    .remove_relation("represents") \
    .remove_node(node_knowledge) \
    .remove_node(node_graph)
assert cp != kg
assert cp == KnowledgeGraph()
