// much of this has been borrowed from these three variants on a force-directed network graph:
// force-directed layout: http://bl.ocks.org/mbostock/4062045
// force-directed with labels: https://bl.ocks.org/heybignick/3faf257bbbbc7743bb72310d03b86ee8
// modified force-directed layout: http://www.coppelia.io/2014/07/an-a-to-z-of-extra-features-for-the-d3-force-layout/

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



function loadGraph(graph) {

simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));


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
          
  var checkBox = document.getElementById("myCheck");
  if (checkBox.checked == true){   
          hidden = null }
    else { hidden = true}

  labels = node.append("text")
      .text(function(d) {
        return d.id;
      })
      .attr('x', 6)
      .attr('y', 3)
      .attr('hidden', hidden);

  //~ node.append("title")
      //~ .text(function(d) { return d.id; });

    //~ svg.append("defs").selectAll("marker")
        //~ .data(["suit", "licensing", "resolved"])
      //~ .enter().append("marker")
        //~ .attr("id", function(d) { return d; })
        //~ .attr("viewBox", "0 -5 10 10")
        //~ .attr("refX", 25)
        //~ .attr("refY", 0)
        //~ .attr("markerWidth", 6)
        //~ .attr("markerHeight", 6)
        //~ .attr("orient", "auto")
      //~ .append("path")
        //~ .attr("d", "M0,-5L10,0L0,5 L10,0 L0, -5")
        //~ .style("stroke", "#4679BD")
        //~ .style("opacity", "0.6");

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

    d3.select('textTitle')
      .html("<a href='https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q="+d.title+"'>" + d.title + "</a>")
    d3.select('authors')
      .text(d.authors)
    d3.select('publicationDate')
      .text("(" + d.year + ")")
    d3.select('citationKey')
      .text(d.id)
    citationKey = d.id

}

function showKeys() {
      // Get the checkbox
  var checkBox = document.getElementById("myCheck");

    

  if (checkBox.checked == true){      
    d3.selectAll('text')
      .attr('hidden', null);
  }
  else {
    d3.selectAll('text')
      .attr('hidden', true);
  }
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
                // check if node is added more than once in new data
                for (var j=0; j<newNodes.length; j++){
                    if (data.nodes[i].id == data.nodes[newNodes[j]].id){new_node = "no"}
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



initialData = {"nodes":[  {"id":"RWebberBurrows2018",
                        "authors":["Webber", "Burrows"],
                        "title":"The Predictive Postcode-- The Geodemographic Classification of British Society",
                        "type": "book",
                        "year": "2018",
                        "group":0},
                        
                        {"id": "EShevkyBell1955",
                        "authors": ["Shevky", "Bell"],
                        "title": "Social Area Analysis: Theory, Illustrative Application, and Computational Procedures",
                        "type": "book",
                        "year": "1955",
                        "group": -1},
                        
                        {"id": "DTimms1971",
                        "authors": ["Timms"],
                        "title": "The urban mosaic: towards a theory of residential differentiation",
                        "type":"book",
                        "year":"1971",
                        "group": -1},],
                                
        "links":[   {"target":"EShevkyBell1955","source":"RWebberBurrows2018","value":"1"},
                    {"target":"EShevkyBell1955","source":"DTimms1971","value":"1"},
                    {"target":"DTimms1971","source":"RWebberBurrows2018","value":"1"}],
                
                }


totalData=initialData

citationKey = 'RWebberBurrows2018'
radius =1

function increase() { 
    radius++
    if (radius >3){radius = 3}
    d3.select('radius')
      .text(radius) 
      }

function decrease() {
    radius--;
    if (radius<0){radius = 0}
    d3.select('radius')
      .text(radius)
      }

function clickButton(){
    totalData = {"nodes":[], "links":[]}
    console.log('Clicked Button')
    console.log(document.getElementById('radius'))
    fetch_JSON_data('http://127.0.0.1:5000/api/' + citationKey + '/' + radius)
}

loadGraph(totalData)

//~
