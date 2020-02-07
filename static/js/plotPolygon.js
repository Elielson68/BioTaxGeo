function initMap() {
    var belem = {lat:-1.44502, lng: -48.4650};
    var map = new google.maps.Map(document.getElementById('plot_map'), {zoom: 4, center: belem});
    var checkbox_group_markers = document.getElementById("checkbox")
    var Geo = new google.maps.Geocoder
    var coordinate_conversor = new Coordinate();
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
            list_marker.push(marker)
        }

    }
    for(i=0;i<list_marker.length;i++){
        for(p=0; p<list_poly.length; p++){
            if(list_poly[p].haveMarker(list_marker[i].getPosition())){
                list_marker[i].setIcon("../static/image/blue_marker2.png")
                list_marker[i].setInsidePolygon(true)
                list_marker[i].setTitle(`\tInfo. da Planilha\nPaís: ${country[i]}\nEstado: ${state[i]}\nMunicípio: ${county[i]}\nLatitude: ${latitudes[i]}\nLongitude: ${longitudes[i]}`)
                name = genus[i]+" "+specie[i]
                list_componentsHTML[p].createBodyTable(name, country[i], state[i], county[i], locality[i], list_marker[i].getLatitude(), list_marker[i].getLongitude(), row_coord_lat[i], i)

                
            }
        }
    }
    MarkersOutPolygon = new ComponentHTML()
    MarkersOutPolygon.createHeaderTable("Lista de Markers fora de Polígonos", "Without", "red")
    MarkersOutPolygon.createTitleTable()
    console.log(list_checked_regions)
    console.log(locality)
    for(i=0;i<list_marker.length;i++){
            if(!list_marker[i].isInsidePolygon()){
                name = genus[i]+" "+specie[i]
                list_marker[i].setTitle(`\tInfo. da Planilha\nPaís: ${country[i]}\nEstado: ${state[i]}\nMunicípio: ${county[i]}\nLatitude: ${latitudes[i]}\nLongitude: ${longitudes[i]}`)
                MarkersOutPolygon.createBodyTable(name, country[i], state[i], county[i], locality[i], list_marker[i].getLatitude(), list_marker[i].getLongitude(), row_coord_lat[i], i)
                if(list_checked_regions[i]['country']['score']<60 && list_checked_regions[i]['country']['name2'] != "null"){
                    MarkersOutPolygon.getRowCountry().innerHTML = list_checked_regions[i]['country']['name1']
                    MarkersOutPolygon.getRowCountry().setAttribute("data-target","#exampleModal") 
                    MarkersOutPolygon.getRowCountry().setAttribute("data-toggle","modal")
                    MarkersOutPolygon.getRowCountry().style = "color: red" 
                    MarkersOutPolygon.getRowCountry().addEventListener("click", ActiveModal)

                    MarkersOutPolygon.getRowLatitude().setAttribute("data-target","#exampleModal")
                    MarkersOutPolygon.getRowLatitude().setAttribute("data-toggle","modal")
                    MarkersOutPolygon.getRowLatitude().style = "color: red" 
                    MarkersOutPolygon.getRowLatitude().addEventListener("click", ActiveModal)

                    MarkersOutPolygon.getRowLongitude().setAttribute("data-target","#exampleModal")
                    MarkersOutPolygon.getRowLongitude().setAttribute("data-toggle","modal")
                    MarkersOutPolygon.getRowLongitude().style = "color: red" 
                    MarkersOutPolygon.getRowLongitude().addEventListener("click", ActiveModal)
                }
                if(list_checked_regions[i]['state']['score']<60 && list_checked_regions[i]['state']['name2'] != "null"){
                    MarkersOutPolygon.getRowState().innerHTML = list_checked_regions[i]['state']['name1']
                    MarkersOutPolygon.getRowState().setAttribute("data-target","#exampleModal") 
                    MarkersOutPolygon.getRowState().setAttribute("data-toggle","modal")
                    MarkersOutPolygon.getRowState().style = "color: red" 
                    MarkersOutPolygon.getRowState().addEventListener("click", ActiveModal)

                    MarkersOutPolygon.getRowLatitude().setAttribute("data-target","#exampleModal")
                    MarkersOutPolygon.getRowLatitude().setAttribute("data-toggle","modal")
                    MarkersOutPolygon.getRowLatitude().style = "color: red" 
                    MarkersOutPolygon.getRowLatitude().addEventListener("click", ActiveModal)

                    MarkersOutPolygon.getRowLongitude().setAttribute("data-target","#exampleModal")
                    MarkersOutPolygon.getRowLongitude().setAttribute("data-toggle","modal")
                    MarkersOutPolygon.getRowLongitude().style = "color: red" 
                    MarkersOutPolygon.getRowLongitude().addEventListener("click", ActiveModal)
                }
                if(list_checked_regions[i]['county']['score']<60 && list_checked_regions[i]['county']['name2'] != "null"){
                    MarkersOutPolygon.getRowCounty().innerHTML = list_checked_regions[i]['county']['name1']
                    MarkersOutPolygon.getRowCounty().setAttribute("data-target","#exampleModal") 
                    MarkersOutPolygon.getRowCounty().setAttribute("data-toggle","modal")
                    MarkersOutPolygon.getRowCounty().style = "color: red" 
                    MarkersOutPolygon.getRowCounty().addEventListener("click", ActiveModal)

                    MarkersOutPolygon.getRowLatitude().setAttribute("data-target","#exampleModal")
                    MarkersOutPolygon.getRowLatitude().setAttribute("data-toggle","modal")
                    MarkersOutPolygon.getRowLatitude().style = "color: red" 
                    MarkersOutPolygon.getRowLatitude().addEventListener("click", ActiveModal)

                    MarkersOutPolygon.getRowLongitude().setAttribute("data-target","#exampleModal")
                    MarkersOutPolygon.getRowLongitude().setAttribute("data-toggle","modal")
                    MarkersOutPolygon.getRowLongitude().style = "color: red" 
                    MarkersOutPolygon.getRowLongitude().addEventListener("click", ActiveModal)
                }
                if(list_checked_regions[i]['locality']['score']<60 && list_checked_regions[i]['locality']['name2'] != "null"){
                    MarkersOutPolygon.getRowLocality().innerHTML = list_checked_regions[i]['locality']['name1']
                    MarkersOutPolygon.getRowLocality().setAttribute("data-target","#exampleModal") 
                    MarkersOutPolygon.getRowLocality().setAttribute("data-toggle","modal")
                    MarkersOutPolygon.getRowLocality().style = "color: red" 
                    MarkersOutPolygon.getRowLocality().addEventListener("click", ActiveModal)

                    MarkersOutPolygon.getRowLatitude().setAttribute("data-target","#exampleModal")
                    MarkersOutPolygon.getRowLatitude().setAttribute("data-toggle","modal")
                    MarkersOutPolygon.getRowLatitude().style = "color: red" 
                    MarkersOutPolygon.getRowLatitude().addEventListener("click", ActiveModal)

                    MarkersOutPolygon.getRowLongitude().setAttribute("data-target","#exampleModal")
                    MarkersOutPolygon.getRowLongitude().setAttribute("data-toggle","modal")
                    MarkersOutPolygon.getRowLongitude().style = "color: red" 
                    MarkersOutPolygon.getRowLongitude().addEventListener("click", ActiveModal)
                }
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
    function ActiveModal(){
        var region = ["country", "state", "county", "locality"]
        var coordinates = ["latitude", "longitude"]
        var text = document.getElementById("modal_text")
        var index = this.id.replace(this.className, "")
        if(region.indexOf(this.className) > -1){
            if(this.className == "country"){
                text.innerHTML = `Verificamos que seu PAÍS está incorreto.<br>Observamos que em sua planilha sua coluna referente ao País consta o valor: ${country[index]}<br>Enquanto sua coordenada representa o local: ${list_region[index][this.className]}`
            }
            else if(this.className == "state"){
                text.innerHTML = `Verificamos que seu ESTADO está incorreto.<br>Observamos que em sua planilha sua coluna referente ao Estado consta o valor: ${state[index]}<br>Enquanto sua coordenada representa o local: ${list_region[index][this.className]}`
            }
            else if(this.className == "county"){
                text.innerHTML = `Verificamos que seu MUNICÍPIO está incorreto.<br>Observamos que em sua planilha sua coluna referente ao Município consta o valor: ${county[index]}<br>Enquanto sua coordenada representa o local: ${list_region[index][this.className]}`
            }
            else if(this.className == "locality"){
                text.innerHTML = `Verificamos que sua LOCALIDADE está incorreta.<br>Observamos que em sua planilha sua coluna referente a Localidade consta o valor: ${county[index]}<br>Enquanto sua coordenada representa o local: ${list_region[index][this.className]}`
            }
        }
        else if(coordinates.indexOf(this.className) > -1){
            Geo.geocode({'address': `${country[index]}, ${state[index]}, ${county[index]}, ${locality[index]}`}, function (a, b){
                latitude = a[0]['geometry']['location']['lat']()
                longitude = a[0]['geometry']['location']['lng']()
                format_MMDDSS_Lat = coordinate_conversor.toDDMMSS(latitude, "lat")
                format_MMDDSS_Lng = coordinate_conversor.toDDMMSS(longitude, "lng")
                format_MMDD_Lat = coordinate_conversor.toDDMM(latitude, "lat")
                format_MMDD_Lng = coordinate_conversor.toDDMM(longitude, "lng")
                text.innerHTML = `Verificamos que sua coordenada está incorreta.<br>A região informada em sua planilha é: ${country[index]}, ${state[index]}, ${county[index]}<br><br>Enquanto que suas coordenadas apontam para: ${list_region[index]['country']}, ${list_region[index]['state']}, ${list_region[index]['county']}<br><br>As coordenadas corretas para este local são:<br><br>Formato Decimal:<br>Latitude: ${latitude}<br>Longitude: ${longitude}<br><br>Formato MMDDSS:<br>Latitude: ${format_MMDDSS_Lat}<br>Longitude: ${format_MMDDSS_Lng}<br><br>Formato MMDD:<br>Latitude: ${format_MMDD_Lat}<br>Longitude: ${format_MMDD_Lng}`
                console.log(b)
            })

            
        }
    }
    checkbox_group_markers.addEventListener('change', ActiveMarkerCluster)
}