from core import KnowledgeGraph

from .visualize import visualize

with open("./graphfs/mount/graphfs.json") as f:
    kg = KnowledgeGraph.from_json(f.read())

with open("./graphfs/mount/graphfs.html", "w") as f:
    f.write(visualize(kg))
