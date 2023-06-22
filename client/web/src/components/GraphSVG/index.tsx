import * as d3 from "d3";
import React, {useEffect, useRef} from "react";

interface GraphProps extends Pick<React.SVGAttributes<SVGSVGElement>, "width" | "height"> {
    onRender: (container: d3.Selection<SVGSVGElement, unknown, null, undefined>) => void;
}

const GraphSVG: React.FC<GraphProps> = ({width, height, onRender}) => {
    const svgRef = useRef<SVGSVGElement>();
    useEffect(() => {
        if (svgRef.current !== null) {
            onRender(d3.select(svgRef.current));
        }
    }, [onRender]);

    return <svg ref={svgRef} width={width} height={height}></svg>;
};

export default GraphSVG;
