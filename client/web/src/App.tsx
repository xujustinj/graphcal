import * as d3 from "d3";
import {useCallback, useEffect, useRef, useState} from "react";
import HelloWorld from "components/HelloWorld";
import GraphSVG from "components/GraphSVG";
import {Node, Link, Graph} from "./types/Graph";

const App: React.FC = () => {
  const onRender = useCallback(
    (container: d3.Selection<SVGSVGElement, unknown, null, undefined>) => {
      console.log("onRender");
      gRef.current = container.append("g");
      container.call(d3.zoom().on("zoom", (e) => gRef.current.attr("transform", e.transform)));
    },
    []
  );

  const [graph, setGraph] = useState<Graph>({
    nodes: [{id: 0}],
    links: []
  });

  const gRef = useRef<d3.Selection<SVGElement, unknown, null, undefined>>();

  useEffect(() => {
    const g = gRef.current;
    if (g === null) {
      return;
    }

    // render links first so they end up in the background
    const links = g
      .selectAll(".link")
      .data(graph.links, (d: Link) => d.id)
      .join("line")
      .attr("class", "link")
      .style("stroke", "black");

    const nodes = g
      .selectAll(".node")
      .data(graph.nodes, (d: Node) => d.id)
      .join("circle")
      .attr("class", "node")
      .attr("cx", 300)
      .attr("cy", 300)
      .attr("r", 16)
      .call(
        d3
          .drag<Element, Node>()
          .on("start", (e, d) => {
            simulation.alphaTarget(0.03).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on("drag", (e, d) => {
            d.fx = e.x;
            d.fy = e.y;
          })
          .on("end", (e, d) => {
            simulation.alphaTarget(0.03).restart();
            d.fx = null;
            d.fy = null;
          })
      );
    nodes.exit().remove();

    const simulation = d3
      .forceSimulation(graph.nodes)
      .force(
        "link",
        d3
          .forceLink<Node, Link>()
          .id((node) => node.id)
          .links(graph.links)
      )
      .force("charge", d3.forceManyBody().strength(-1000))
      .force("collide", d3.forceCollide().radius(24))
      .force("center", d3.forceCenter(300, 300))
      .on("tick", () => {
        links
          .attr("x1", (d) => d.source.x)
          .attr("y1", (d) => d.source.y)
          .attr("x2", (d) => d.target.x)
          .attr("y2", (d) => d.target.y);
        nodes.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
      });
    simulation.restart();
  }, [graph]);

  return (
    <>
      <HelloWorld />
      <GraphSVG width={600} height={600} onRender={onRender} />
      <button
        onClick={() => {
          const source = graph.nodes[Math.floor(Math.random() * graph.nodes.length)];
          const newNode = {id: graph.nodes.length};
          const newLink = {id: graph.links.length, source, target: newNode};
          setGraph({
            nodes: [...graph.nodes, newNode],
            links: [...graph.links, newLink]
          });
        }}
      >
        Add Node
      </button>
    </>
  );
};

export default App;
