
function plotMap() {
    let text = document.getElementById("latlon");
    let coords = JSON.parse(text.value);
    console.log(coords)

    var data = [{
    type: 'scattergeo',
    lat: coords.map(x => x[1]),
    lon: coords.map(x => x[0]),   
    mode: 'markers+lines',
    line:{
        width: 2,
        color: 'blue'
    }
    }];
    
    
    var layout = {
    title: 'Routing Path',
    showlegend: false,
    geo: {
        resolution: 50,
        showland: true,
        showlakes: true,
        landcolor: 'rgb(204, 204, 204)',
        countrycolor: 'rgb(204, 204, 204)',
        lakecolor: 'rgb(255, 255, 255)',
        projection: {
        type: 'equirectangular'
        },
        coastlinewidth: 2
    }
    
    };
    
    
    Plotly.newPlot('mapArea', data, layout);
}
