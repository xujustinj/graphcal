import json

from core import Node, Edge, KnowledgeGraph
from visualization import visualize

t2g = KnowledgeGraph()

class Paper(Node):
    def __init__(self, title):
        super().__init__(("!!paper", title))

class Model(Node):
    def __init__(self, name):
        super().__init__(("!!model", name))

t2g.add_relation(PROPOSES := "proposes")
t2g.add_relation(USES_BASELINE := "uses_baseline")
t2g.add_relation(HAS_VARIANT := "has_variant")

t2g.add_node(paper__GT_BT := Paper("An Unsupervised Joint System for Text Generation from Knowledge Graphs and Semantic Parsing"))

t2g \
    .add_node(model__GT_BT_rule_based_baseline := Model("GT-BT's rule-based baseline")) \
    .add_edge(Edge(paper__GT_BT, PROPOSES, model__GT_BT_rule_based_baseline))

t2g \
    .add_node(model__GT_BT := Model("GT-BT")) \
    .add_edge(Edge(paper__GT_BT, PROPOSES, model__GT_BT))

t2g \
    .add_node(model__GT_BT_sampled_noise := Model("GT-BT, sampled noise")) \
    .add_edge(Edge(model__GT_BT, HAS_VARIANT, model__GT_BT_sampled_noise))

t2g \
    .add_node(model__GT_BT_composed_noise := Model("GT-BT, composed noise")) \
    .add_edge(Edge(paper__GT_BT, PROPOSES, model__GT_BT_composed_noise))

t2g \
    .add_node(paper__CycleGT := Paper("CycleGT: Unsupervised Graph-to-Text and Text-to-Graph Generation via Cycle Training")) \
    .add_edge(Edge(paper__CycleGT, USES_BASELINE, model__GT_BT_rule_based_baseline)) \
    .add_edge(Edge(paper__CycleGT, USES_BASELINE, model__GT_BT_sampled_noise))

t2g \
    .add_node(model__CycleGT := Model("CycleGT")) \
    .add_edge(Edge(paper__CycleGT, PROPOSES, model__CycleGT))

t2g \
    .add_node(model__CycleGT_supervised := Model("CycleGT, supervised")) \
    .add_edge(Edge(model__CycleGT, HAS_VARIANT, model__CycleGT_supervised))

t2g \
    .add_node(model__CycleGT_unsupervised := Model("CycleGT, unsupervised")) \
    .add_edge(Edge(model__CycleGT, HAS_VARIANT, model__CycleGT_unsupervised))

with open("./examples/t2g/t2g.json", "w") as f:
    json.dump(json.loads(t2g.to_json()), f, indent=2)

with open("./examples/t2g/t2g.html", "w") as f:
    f.write(visualize(t2g))
