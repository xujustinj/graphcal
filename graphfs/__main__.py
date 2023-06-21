import json
import os

from core import Edge, KnowledgeGraph

from .open import graphfs_open

graphfs = KnowledgeGraph()

MOUNT_PATH = "./graphfs/mount"

graphfs = KnowledgeGraph()
for file in graphfs_open(MOUNT_PATH):
    file_node = file.to_node()
    graphfs.add_node(file.to_node())
    for property, value in file.properties.items():
        relation = f"file_property:{property}"
        graphfs.add_relation(relation)
        graphfs.add_node(value)
        graphfs.add_edge(Edge(file_node, relation, value))

with open(os.path.join(MOUNT_PATH, "graphfs.json"), "w") as f:
    json.dump(json.loads(graphfs.to_json()), f, indent=2)
