class ForceCanvas {
	constructor() {
		this.nodes = [];
		this.graphcanvas = d3.select("#ForceCanvas");
		this.graphcontainer = d3.select("#ForceContainer");
		this.nodes = [];
	}

	/**
	 * A function which toggles all of the visible elements to show
	 */
	show() {
		this.graphcontainer.style("display", "block");
	};

	/**
	 * A function which toggles all of the visible elements to hide
	 */
	hide() {
		this.graphcontainer.style("display", "none");
	};

	/** A callback function to handle start dragging on a node */
	dragstarted(d) {
		if (!d3.event.active) this.simulation.alphaTarget(0.3).restart();
		d.fx = d.x;
		d.fy = d.y;
	}

	/** A callback function to handle dragging on a node */
	dragged(d) {
		d.fx = d3.event.x;
		d.fy = d3.event.y;
	}

	/** A callback function to handle drag release on a node */
	dragended(d) {
		if (!d3.event.active) this.simulation.alphaTarget(0);
		d.fx = null;
		d.fy = null;
	}

	/** A callback function to handle the animation */
	ticked() {
		this.links
			.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
	
		this.nodes
			.attr("cx", function(d) { return d.x; })
			.attr("cy", function(d) { return d.y; });
	};

	/** A callback function to handle zooming/panning */
	zoomed() {
		this.nodes.attr("transform", d3.event.transform);
		this.links.attr("transform", d3.event.transform);
	};

	/**
	 * A function which pans the audio to a time corresponding to
	 * a double clicked node
	 * @param {object} d: A handle to the node that's been clicked 
	 */
	visitLink(d) {
		window.open(d.url);
	};


	/**
	 * Update the graph with information from a new song
	 * @param {*} params: A dictionary of parameters for a newly loaded song,
	 * including a graph object with all of the nodes, edges, and weights 
	 */
	updateParams(params) {
		// With heavy inspiration from https://bl.ocks.org/mbostock/4062045
		const width = params.width;
		const height = params.height;

		this.simulation = d3.forceSimulation()
							.force("link", d3.forceLink().id(function(d) { return d.id; }))
							.force("charge", d3.forceManyBody())
							.force("center", d3.forceCenter(width / 2, height / 2));
		
		let graph = params.graph;
		// Step 1: Identify unique sites and make a node for each one
		let url2id = {};
		graph.nodes = [];
		let N = 0;
		for (let i = 0; i < graph.edges.length; i++) {
			for (let k = 0; k < 2; k++) {
				let u = graph.edges[i][k];
				if (url2id[u] === undefined) {
					url2id[u] = N;
					graph.nodes.push({"id":N, "url":u});
					N++;
				}
			}
		}
		// Step 2: Add the edges
		for (let i = 0; i < graph.edges.length; i++) {
			for (let k = 0; k < 2; k++) {
				let u = graph.edges[i][k];
				if (!(u in url2id)) {
					url2id[u] = graph.nodes.length;
					graph.nodes.push({"id":i, "url":u});
				}
			}
		}
		graph.links = graph.edges.map(e => {
			return {"source":url2id[e[0]], "target":url2id[e[1]]};
		});
		
		// Clear all graph elements if any exist
		this.graphcanvas.selectAll("*").remove();
		this.graphcanvas.attr('width', width).attr('height', height);
		
		this.links = this.graphcanvas.append("g")
			.attr("class", "links")
			.selectAll("line")
			.data(graph.links)
			.enter().append("line");
		this.links.style("stroke", "#aaa");
		
		const URLDisplay = document.getElementById("url");
		this.nodes = this.graphcanvas.append("g")
			.attr("class", "nodes")
			.selectAll("circle")
			.data(graph.nodes)
			.enter().append("circle")
			.attr("r", 5)
			.attr("fill", () => d3.rgb(0, 0, 0))
			.on("mouseover", d=>{
				let urlName = d.url.replace(graph.base_url, "");
				URLDisplay.innerHTML = "<a href = \"" + d.url+ "\" target=\"_blank\">" + urlName + "</a>";
			});

		this.nodes.call(d3.drag()
			.on("start", this.dragstarted.bind(this))
			.on("drag", this.dragged.bind(this))
			.on("end", this.dragended.bind(this)));
		
		this.nodes.on("dblclick", this.visitLink.bind(this));

		this.simulation
			.nodes(graph.nodes)
			.on("tick", this.ticked.bind(this));
		
		this.simulation.force("link")
			.links(graph.links);
		
		this.graphcanvas.call(d3.zoom()
			.scaleExtent([1/4, 8])
			.on("zoom", this.zoomed.bind(this))
			.filter(function () {
				return d3.event.ctrlKey;
			}));
		
	}

	search(pattern) {
		pattern = pattern.toLowerCase();
		this.nodes.attr("fill", (d) => {
			let ret = d3.rgb(0, 0, 0);
			let s = d.url.toLowerCase();
			if (s.indexOf(pattern) != -1) {
				ret = d3.rgb(255, 103, 1);
			}
			return ret;
		});
	}

}
