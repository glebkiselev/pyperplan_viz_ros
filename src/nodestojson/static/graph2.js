    // Set up the plot window.
    var margin = 30;
    var w = 700 - 2 * margin, h = 500 - 2 * margin;
    var svg = d3.select("#plot").append("svg")
                    .attr("width", w + 2 * margin)
                    .attr("height", h + 2 * margin)


/* Build the directional arrows for the links/edges */
    svg.append("svg:defs")
                .selectAll("marker")
                .data(["end"])
                .enter().append("svg:marker")
                .attr("id", String)
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 15)
                .attr("refY", -1.5)
                .attr("markerWidth", 6)
                .attr("markerHeight", 6)
                .attr("orient", "auto")
                .append("svg:path")
                .attr("d", "M0,-5L10,0L0,5");


    function callback(data) {
        /* Draw the node labels first */
       var texts = svg.selectAll("text")
                        .data(data.nodes)
                        .enter()
                        .append("text")
                        .attr("fill", "black")
                        .attr("font-family", "sans-serif")
                        .attr("font-size", "10px")
                        .text(function(d) { return d.name; });
        /* Establish the dynamic force behavor of the nodes */
        var force = d3.layout.force()
                        .nodes(data.nodes)
                        .links(data.links)
                        .size([w,h])
                        .linkDistance([250])
                        .charge([-1500])
                        .gravity(0.3)
                        .start();
        /* Draw the edges/links between the nodes */
        var link = svg.selectAll("line.link")
                        .data(data.links)
                        .enter()
                        .append("svg:line")
                        .attr("class", "link")
                        .style("stroke", "#ccc")
                        .style("stroke-width", 1)
                        .attr("marker-end", "url(#end)");
        /* Draw the nodes themselves */
        var nodes = svg.selectAll("circle.node")
                        .data(data.nodes)
                        .enter()
                        .append("svg:circle")
                        .attr("r", 20)
                        .attr("opacity", 0.5)
                        .style("fill", function(d,i) { return color(i); })
                        .call(force.drag);
        /* Run the Force effect */
        force.on("tick", function() {
                   link.attr("x1", function(d) { return d.source.x; })
                        .attr("y1", function(d) { return d.source.y; })
                        .attr("x2", function(d) { return d.target.x; })
                        .attr("y2", function(d) { return d.target.y; });
                   nodes.attr("cx", function(d) { return d.x; })
                        .attr("cy", function(d) { return d.y; })
                   texts.attr("transform", function(d) {
                            return "translate(" + d.x + "," + d.y + ")";
                            });
                   }); // End tick func
    }; // End makeDiag worker func

    /* Load the json data */
            d3.json("/data", callback);