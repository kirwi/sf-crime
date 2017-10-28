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

document.getElementById("slider").addEventListener("input", function (e) {
    var year = parseInt(e.target.value);
    var dataString = "ROBBERY/" + year;
    map.getSource("crimes").setData(dataString);
    document.getElementById("year").innerText = year;
});
