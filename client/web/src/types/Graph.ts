export interface Node extends d3.SimulationNodeDatum {
    id: number;
    label?: string;
}

export interface Link extends d3.SimulationLinkDatum<Node> {
    id: number;
    label?: string;
    source: Node;
    target: Node;
}

export interface Graph {
    nodes: Array<Node>;
    links: Array<Link>;
}
