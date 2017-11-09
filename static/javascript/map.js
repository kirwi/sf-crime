var accessToken ="pk.eyJ1Ijoia2lyd2kiLCJhIjoiY2luanhuajFhMHh5enVrbTNnNWxiNmFuYiJ9._OXf5ly8GcEla3_8vGwcEg"
mapboxgl.accessToken = accessToken;

var map = new mapboxgl.Map({
    container: "map",
    style: "mapbox://styles/mapbox/light-v9",
    center: [-122.431297, 37.773972],
    zoom: 11.5
});

map.on("load", function (e) {

    map.addSource("crimes", {
        type: "geojson",
        data: "ROBBERY/2003",
        cluster: true,
        clusterRadius: 50,
        clusterMaxZoom: 13,
    });

    map.addLayer({
        id: "clusters",
        type: "circle",
        source: "crimes",
        filter: ["has", "point_count"],
        paint: {
            "circle-color": {
                property: "point_count",
                type: "interval",
                stops: [
                    [0, "#67a9cf"],
                    [100, "#ef8a62"],
                    [750, "#b2182b"]
                ]
            },
            "circle-radius": {
                property: "point_count",
                type: "interval",
                stops: [
                    [0, 20],
                    [100, 30],
                    [750, 40]
                ]
            },
            "circle-opacity": 0.6,
            "circle-stroke-width": 2,
            "circle-stroke-color": "#535353"
        }
    });

    map.addLayer({
        id: "cluster-count",
        type: "symbol",
        source: "crimes",
        filter: ["has", "point_count"],
        layout: {
            "text-field": "{point_count_abbreviated}",
            "text-size": 12
        }
    });

    map.addLayer({
        id: "unclustered-point",
        type: "circle",
        source: "crimes",
        filter: ["!has", "point_count"],
        paint: {
            "circle-color": "#2166ac",
            "circle-radius": 4,
            "circle-stroke-width": 2,
            "circle-stroke-color": "#535353"
        }
    });
});

var pieSvg = d3.select("#piechart"),
    lineSvg = d3.select("#linechart"),
    margin = {top: 0, right: 0, bottom: 20, left: 25},
    container = document.querySelector(".chart-container"),
    containerWidth = +container.offsetWidth,
    containerHeight = +container.offsetHeight,
    width = containerWidth - margin.left - margin.right,
    height = containerHeight - margin.top - margin.bottom,
    parseTime = d3.timeParse("%a, %d %b %Y %H:%M:%S GMT"),
    formatMonth = d3.timeFormat("%b");

var lines = lineSvg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
var wedges = pieSvg.append("g")
    .attr("transform", "translate(" + containerWidth / 2 + "," +
        containerHeight / 2 + ")");

var linesX = d3.scaleTime().rangeRound([0, width]),
    linesY = d3.scaleLinear().rangeRound([height, 0]),
    radius = Math.min(containerWidth, containerHeight) / 2,
    color = d3.scaleOrdinal(["#98abc5", "#8a89a6", "#7b6888", "#6b486b",
        "#a05d56", "#d0743c", "#ff8c00"]);

var line = d3.line()
    .x(function(d) { return linesX(new Date(d.date)); })
    .y(function(d) { return linesY(d.occurrences); });

var pie = d3.pie()
    .sort(null)
    .value(function(d) { return d.occurrences; });

drawLineChart("ROBBERY", 2003);
drawPieChart("ROBBERY", 2003);

function drawPieChart(crime, year) {
    d3.json("/agg/day/" + crime + "/" + year, function(data){

        var path = d3.arc()
            .outerRadius(radius)
            .innerRadius(0);

        var label = d3.arc()
            .outerRadius(radius - 40)
            .innerRadius(radius - 40);

        var arc = wedges.selectAll(".arc")
            .data(pie(data.aggregates))
            .enter().append("g")
            .attr("class", "arc");

        arc.append("path")
            .attr("d", path)
            .attr("fill", function(d) { return color(d.data.occurrences); });

        arc.append("text")
            .attr("transform", function(d) {
                return "translate(" + label.centroid(d) + ")";
            })
            .attr("dy", "0.35em")
            .text(function(d) { return d.data.day; });

    });
}

function drawLineChart(crime, year) {
    d3.json("/agg/month/" + crime + "/" + year, function(data) {

        linesX.domain(d3.extent(data.aggregates,
            function(d) { return new Date(d.date); }));
        linesY.domain(d3.extent(data.aggregates,
            function(d) { return d.occurrences; }));

        lines.append("g")
            .attr("transform", "translate(0," + height + ")")
            .call(d3.axisBottom(linesX).tickFormat(formatMonth).ticks(4));

        lines.append("g")
            .call(d3.axisLeft(linesY).ticks(5))
            .append("text")
            .attr("fill", "#000")
            .attr("transform", "rotate(-90)")
            // .attr("y", 0)
            .attr("text-anchor", "end");

        lines.append("path")
            .datum(data.aggregates)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-linejoin", "round")
            .attr("stroke-linecap", "round")
            .attr("stroke-width", 3.0)
            .attr("class", "line")
            .attr("d", line);
    });
}

d3.select("#slider").on("change", function() {
    var year = this.value;
    var crime = document.getElementById("crime").textContent;
    var dataString = "/" + crime + "/" + year;
    map.getSource("crimes").setData(dataString);
    document.getElementById("year").textContent = year;
    d3.json("/agg/month/" + crime + "/" + year, function(data) {
        linesX.domain(d3.extent(data.aggregates,
            function(d) { return new Date(d.date); }));
        linesY.domain(d3.extent(data.aggregates,
            function(d) { return d.occurrences; }));
        d3.select(".line").transition().duration(400)
          .attr("d", line(data.aggregates));
    });

});

var menu = document.getElementById("menu")
menu.addEventListener("click", function(e) {
    var crime = e.target.innerHTML;
    console.log(e);
    console.log(crime);
    document.getElementById("crime").textContent = crime;
    document.getElementById("slider").value = 2003;
    document.getElementById("year").textContent = 2003;
    var dataString = "/" + crime + "/" + 2003;
    map.getSource("crimes").setData(dataString);
});
