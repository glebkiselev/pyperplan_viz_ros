        // Set up the plot window.
        var margin = 30;
        var w = 700 - 2 * margin, h = 500 - 2 * margin;
        var svg = d3.select("#plot").append("svg")
                        .attr("width", w + 2 * margin)
                        .attr("height", h + 2 * margin)
                    .append("svg:g")
                        .attr("transform", "translate(" + margin + ", " + margin + ")");


        // Axes scaling functions.
        var xscale = d3.scale.linear().range([0, w]);
        var yscale = d3.scale.linear().range([h, 0]);

        // The axes objects themselves.
        var xaxis = d3.svg.axis().scale(xscale).ticks(8);
        var yaxis = d3.svg.axis().scale(yscale).ticks(8).orient("left");

        svg.append("svg:g").attr("class", "x axis")
                           .attr("transform", "translate(0, " + h + ")");
        svg.append("svg:g").attr("class", "y axis");

        // Load the data.
        var callback = function (data) {


            // Insert the data points.
            fill = d3.scale.category20();

          var force = d3.layout.force()
                      .charge(-120)
                      .linkDistance(30)
                      .nodes(data.nodes)
                      .links(data.links)
                      .size([w, h])
                      .start();


          var link = svg.selectAll("line.link")
              .data(data.links)
            .enter().append("svg:line")
              .attr("class", "link")
              .style("stroke-width", function(d) { return Math.sqrt(d.value); })
              .attr("x1", function(d) { return d.source.x; })
              .attr("y1", function(d) { return d.source.y; })
              .attr("x2", function(d) { return d.target.x; })
              .attr("y2", function(d) { return d.target.y; });

          var node = svg.selectAll("circle.node")
              .data(data.nodes)
            .enter().append("svg:circle")
              .attr("class", "node")
              .attr("cx", function(d) { return d.x; })
              .attr("cy", function(d) { return d.y; })
              .attr("r", 5)
              .style("fill", function(d) { return fill(d.group); })
              .call(force.drag);

          node.append("svg:title")
              .text(function(d) { return d.name; });

            svg.style("opacity", 1e-6)
                .transition()
                  .duration(1000)
                  .style("opacity", 1);


          force.on("tick", function() {
            link.attr("x1", function(d) { return d.source.x; })
                .attr("y1", function(d) { return d.source.y; })
                .attr("x2", function(d) { return d.target.x; })
                .attr("y2", function(d) { return d.target.y; });

            node.attr("cx", function(d) { return d.x; })
                .attr("cy", function(d) { return d.y; });
  });

        };

            d3.json("/data", callback);

