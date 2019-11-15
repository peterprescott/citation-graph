// force-directed layout: http://bl.ocks.org/mbostock/4062045
// ***this is the one we started from *** force-directed with labels: https://bl.ocks.org/heybignick/3faf257bbbbc7743bb72310d03b86ee8
// modified force-directed layout: http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/
// slider: http://bl.ocks.org/mbostock/6452972



var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");

var color = d3.scaleOrdinal(d3.schemeCategory10);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));

function loadGraph(graph) {

    svg.selectAll("g").remove();
    svg.selectAll("line").remove();

  var link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return Math.sqrt(d.value); })
      .style("marker-end",  "url(#suit)");

  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter().append("g")

  var circles = node.append("circle")
      .attr("r", 6)
      .attr("fill", function(d) { return color(d.group); })
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

  var labels = node.append("text")
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
  }}


function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
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
            console.log(data)
            
            var newLinks = [];
            for (var i=0; i < data.links.length ; i++){
                console.log('i ='+i);
                var new_link = "yes";
                // presume node is new_input until we find otherwise
                // check if data is new_input by comparison of sources and targets with each node in totalData
                for (var j=0; j < totalData.links.length; j++){
                    console.log('j ='+j);
                    console.log(data.links[i].source)
                    console.log(totalData.links[j].source.id)
                    if (data.links[i].source == totalData.links[j].source.id){
                        //why do we never get in here??
                        console.log('sources equal', data.links[i].target, totalData.links[j].target)
                        
                        if (data.links[i].target == totalData.links[j].target.id){
                            console.log('targets equal at i:'+i+',j:'+j);
                            new_link = "no"

                        }
                    }
                }
                if (new_link != "no"){
                    
                    newLinks.push(i);
                    
                    console.log(i+' is a new link')}
                    else{console.log(i+' is not a new link')}

            }

            console.log('newLinks = '+newLinks)
            for (var i = 0; i < newLinks.length; i++){
                totalData.links.push(data.links[newLinks[i]])   }


            // add unique values from data.nodes to totalData.nodes
            var newNodes = [];
            // for each value in data.nodes
            for (var i=0; i < data.nodes.length ; i++){
                
                // presume node is new_input until we find otherwise

                var new_node = "yes";

                // check if data is new_input by comparison of ids with each node in totalData
                for (var j=0; j < totalData.nodes.length; j++){
                
                    if (data.nodes[i].id == totalData.nodes[j].id){
                        new_node = "no"
                        console.log('here')
                    }
                }
                
                if (new_node != "no"){
                    newNodes.push(i)
                    console.log(i)}

            }
            console.log('newNodes = '+newNodes)
            for (var i = 0; i <newNodes.length; i++){
                totalData.nodes.push(data.nodes[newNodes[i]])
            }




            


            


            console.log(totalData.links)
            loadGraph(totalData)

        });
      })
      .catch(function(error) {
        console.log("Fetch error: " + error);
    });



}

totalData = {"nodes":[{"id":"Example"}],"links":[]}


function clickButton(){
    console.log('Clicked Button')
    fetch_JSON_data('http://127.0.0.1:5000/api/RWebberBurrows2018')
}

loadGraph(totalData)

//~
