from pyvis.network import Network

from core import Node, KnowledgeGraph

def node_id(node: Node) -> str:
    return "/".join(str(token) for token in node.name)

def visualize(kg: KnowledgeGraph) -> str:
    net = Network(notebook=False)
    for node in kg.nodes:
        id = node_id(node)
        if isinstance(node.name, tuple):
            label = str(node.name[-1])
        else:
            label = str(node.name)
        net.add_node(id, label=label)

    for edge in kg.edges:
        source_id = node_id(edge.source)
        target_id = node_id(edge.target)
        id = f"{source_id}>{edge.relation}>{target_id}"
        label = edge.relation
        net.add_edge(source_id, target_id, id=id, label=label)

    return net.generate_html()
