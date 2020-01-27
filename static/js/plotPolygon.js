function initMap() {
    var belem = {lat:-1.44502, lng: -48.4650};
    var map = new google.maps.Map(document.getElementById('plot_map'), {zoom: 4, center: belem});
    var checkbox_group_markers = document.getElementById("checkbox")
    checkbox_group_markers.checked = true
    list_poly = []
    list_componentsHTML = []
    list_marker = []
    for (poly in polygons){
        selected_polygon = new Polygon(map)
        selected_polygon.setActive(false)
        selected_polygon.setPath(polygons[poly])
        list_poly.push(selected_polygon)

        header_table = new ComponentHTML()
        header_table.createHeaderTable("Lista de Markers dentro do Polígono "+list_poly.length, list_poly.length)
        header_table.createTitleTable()
        list_componentsHTML.push(header_table)
    }
    for(i=0;i<latitudes.length;i++){
        if (latitudes[i]!=""){
            coord = new google.maps.LatLng(latitudes[i], longitudes[i])
            marker = new Point_Marker(coord, map, "../static/image/red_marker2.png" , false)
            marker.setTitle(`Latitude: ${latitudes[i]}\nLongitude: ${longitudes[i]}`)
            list_marker.push(marker)
        }

    }
    for(i=0;i<list_marker.length;i++){
        for(p=0; p<list_poly.length; p++){
            if(list_poly[p].haveMarker(list_marker[i].getPosition())){
                list_marker[i].setIcon("../static/image/blue_marker2.png")
                list_marker[i].setInsidePolygon(true)
                name = genus[i]+" "+specie[i]
                list_componentsHTML[p].createBodyTable(name, country[i], state[i], county[i], list_marker[i].getLatitude(), list_marker[i].getLongitude(), row_coord_lat[i])
            }
        }
    }
    MarkersOutPolygon = new ComponentHTML()
    MarkersOutPolygon.createHeaderTable("Lista de Markers fora de Polígonos", "Without", "red")
    MarkersOutPolygon.createTitleTable()
    for(i=0;i<list_marker.length;i++){
            if(!list_marker[i].isInsidePolygon()){
                name = genus[i]+" "+specie[i]
                MarkersOutPolygon.createBodyTable(name, country[i], state[i], county[i], list_marker[i].getLatitude(), list_marker[i].getLongitude(), row_coord_lat[i])
            }
    }
    opt_options = {imagePath:'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m', gridSize: 60, maxZoom: 14, minimumClusterSize: 2}
    var markerCluster = new MarkerClusterer(map, list_marker, opt_options);
    function ActiveMarkerCluster(){
        if(this.checked){
            opt_options = {imagePath:'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m', gridSize: 60, maxZoom: 14, minimumClusterSize: 2}
            markerCluster.setOptions(opt_options)
            markerCluster.repaint()
        }
        else{
            opt_options = {imagePath:'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m', gridSize: 1, maxZoom: 1, minimumClusterSize: 1}
            markerCluster.setOptions(opt_options)
            markerCluster.repaint()
        }
    }
    checkbox_group_markers.addEventListener('change', ActiveMarkerCluster)
    selected_polygon.vertices.addListener('click', addVerticesPolygonClick);
    map.addListener('click', addVerticesPolygonClick);
}