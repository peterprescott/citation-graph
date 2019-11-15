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

	svg.selectAll("*").remove();

  var link = svg.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

  var node = svg.append("g")
      .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter().append("g")
    
  var circles = node.append("circle")
      .attr("r", 5)
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
            

            
        
			// add unique values from data.nodes to totalData.nodes
			
			// for each value in data.nodes
			for (var i=0; i < data.nodes.length ; i++){
			
				// presume node is new_input until we find otherwise
				var new_input = "true"
				
				// check if data is new_input by comparison of ids with each node in totalData
				for (var j=0; j < totalData.nodes.length; j++){
					if (data.nodes[i].id == totalData.nodes[j].id){
						new_input = "false"
					}					
				}
				
				if (new_input === "true") {	
					totalData.nodes.push(data.nodes[i])	}
			}

			// for each value in data.links
			for (var i=0; i < data.links.length ; i++){
			
				// presume node is new_input until we find otherwise
				var new_input = "true"
				
				// check if data is new_input by comparison of ids with each node in totalData
				for (var j=0; j < totalData.links.length; j++){
					
					if ((data.links[i].source.id == totalData.links[j].source.id) 
							&& (data.links[i].target.id == totalData.links[j].target.id)){
						
						//~ new_input = "false"
					}					
				}
				
				if (new_input === "true") {	
					totalData.links.push(data.links[i])	}
			}
            

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
