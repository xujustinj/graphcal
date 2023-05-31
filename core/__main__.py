from core.graph import Node, Edge, KnowledgeGraph

kg = KnowledgeGraph() \
    .add_node(node_knowledge := Node(("knowledge", 0))) \
    .add_node(node_graph := Node((1, "graph"))) \
    .add_relation("represents") \
    .add_edge(Edge(node_knowledge, "represents", node_graph))
s = kg.to_json()
assert kg == KnowledgeGraph.from_json(s)
