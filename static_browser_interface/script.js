// force-directed layout: http://bl.ocks.org/mbostock/4062045
// ***this is the one we started from *** force-directed with labels: https://bl.ocks.org/heybignick/3faf257bbbbc7743bb72310d03b86ee8
// modified force-directed layout: http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/
// slider: http://bl.ocks.org/mbostock/6452972
var svg
var color
var simulation
var link
var node
var circles
var labels


svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

color = d3.scaleOrdinal(d3.schemeCategory10);

simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));

function loadGraph(graph) {

    svg.selectAll("g").remove();
    svg.selectAll("line").remove();

  link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return Math.sqrt(d.value); })
      .style("marker-end",  "url(#suit)");

  node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter().append("g")

  circles = node.append("circle")
      .attr("r", 6)
      .attr("fill", function(d) { return color(d.group); })
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

  labels = node.append("text")
      .text(function(d) {
        return d.id;
      })
      .attr('x', 6)
      .attr('y', 3);

  node.append("title")
      .text(function(d) { return d.id; });

    svg.append("defs").selectAll("marker")
        .data(["suit", "licensing", "resolved"])
      .enter().append("marker")
        .attr("id", function(d) { return d; })
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 25)
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
      .append("path")
        .attr("d", "M0,-5L10,0L0,5 L10,0 L0, -5")
        .style("stroke", "#4679BD")
        .style("opacity", "0.6");

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);
      
}

function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
        })
}

function displayData(d) {
// needs to be prettified, but it should do for now.

    d3.select('textTitle')
      .text(d.title)
    d3.select('citeKey')
      .text(d.id)
    
}

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  displayData(d)
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

function fetch_JSON_data(json_api_address){
    fetch(json_api_address)
      .then(function(response) {
        if (response.status !== 200) {
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(function(data) {
            var newLinks = [];
            for (var i=0; i < data.links.length ; i++){
                var new_link = "yes";
                // presume link is new until we find otherwise
                // check by comparison of sources and targets with each link in totalData
                for (var j=0; j < totalData.links.length; j++){
                    if (data.links[i].source == totalData.links[j].source.id){
                        if (data.links[i].target == totalData.links[j].target.id){new_link = "no"}
                    }
                }
            if (new_link != "no"){newLinks.push(i)}
            }
            for (var i = 0; i < newLinks.length; i++){totalData.links.push(data.links[newLinks[i]])}

            var newNodes = [];
            for (var i=0; i < data.nodes.length ; i++){
                // presume node is new until we find otherwise
                var new_node = "yes";
                // check if data is new_input by comparison of ids with each node in totalData
                for (var j=0; j < totalData.nodes.length; j++){
                    if (data.nodes[i].id == totalData.nodes[j].id){new_node = "no"}
                }
                if (new_node != "no"){newNodes.push(i)}
            }
            for (var i = 0; i <newNodes.length; i++){
                totalData.nodes.push(data.nodes[newNodes[i]])
            }
            console.log(totalData)
            loadGraph(totalData)
        });
      })
      .catch(function(error) {
        console.log("Fetch error: " + error);
    });



}



totalData = {"nodes":[{"id":"A Book"},{"id":"Another Book"}, {"id":"Yet Another Book"}],
    "links":[{"target":"A Book","source":"Yet Another Book","value":"3"},{"target":"Another Book","source":"Yet Another Book","value":"5"},{"target":"Another Book","source":"A Book","value":"1"}]}


function clickButton(){
    console.log('Clicked Button')
    fetch_JSON_data('http://127.0.0.1:5000/api/RWebberBurrows2018')
}

loadGraph(totalData)

//~
