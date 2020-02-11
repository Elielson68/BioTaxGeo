function initMap() {
    var belem = {lat:-1.44502, lng: -48.4650};
    var map = new google.maps.Map(document.getElementById('plot_map'), {zoom: 4, center: belem});
    //var mapi = new google.maps.Map(document.getElementById("mapi"), {zoom: 4, center: belem});
    var checkbox_group_markers = document.getElementById("checkbox")
    var Geo = new google.maps.Geocoder
    var coordinate_conversor = new Coordinate();
    var input_radio = new ComponentHTML()
    var modal = document.getElementById("modal_body")
    var Cancel_Buttom = document.getElementById("Cancel_Buttom")
    var Confirm_Buttom = document.getElementById("Confirm_Buttom")
    var data = document.getElementById("data")
    var row_modify = null
    var send_server = {}
    var modify_column = {}
    var column_modify = ""
    var column_changed = null
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
        selected_polygon.setTitle("polygon"+list_poly.length)
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
                
                list_componentsHTML[p].createBodyTable(name, country[i], state[i], county[i], locality[i], list_marker[i].getLatitude(), list_marker[i].getLongitude(), row_coord_lat[i], i, list_poly[p].getTitle())


                if(list_checked_regions[i]['country']['score']<60 && list_checked_regions[i]['country']['name2'] != "null"){
                    list_componentsHTML[p].setWrongRow(list_componentsHTML[p].getRowCountry(), list_checked_regions[i]['country']['name1'], ActiveModal)
                    list_componentsHTML[p].setWrongRow(list_componentsHTML[p].getRowLatitude(),  list_marker[i].getLatitude(), ActiveModal)
                    list_componentsHTML[p].setWrongRow(list_componentsHTML[p].getRowLongitude(), list_marker[i].getLongitude(), ActiveModal)
                }
                else if (list_checked_regions[i]['country']['score']>=60 && list_checked_regions[i]['country']['score']<100){
                    list_componentsHTML[p].setIncorrectRow(list_componentsHTML[p].getRowCountry(), list_checked_regions[i]['country']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['state']['score']<60 && list_checked_regions[i]['state']['name2'] != "null"){

                    list_componentsHTML[p].setWrongRow(list_componentsHTML[p].getRowState(), list_checked_regions[i]['state']['name1'], ActiveModal)
                    list_componentsHTML[p].setWrongRow(list_componentsHTML[p].getRowLatitude(),  list_marker[i].getLatitude(), ActiveModal)
                    list_componentsHTML[p].setWrongRow(list_componentsHTML[p].getRowLongitude(), list_marker[i].getLongitude(), ActiveModal)
                }
                else if(list_checked_regions[i]['state']['score']>=60 && list_checked_regions[i]['state']['score']<100){
                    list_componentsHTML[p].setIncorrectRow(list_componentsHTML[p].getRowState(), list_checked_regions[i]['state']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['county']['score']<60 && list_checked_regions[i]['county']['name2'] != "null"){
                    list_componentsHTML[p].setWrongRow(list_componentsHTML[p].getRowCounty(),  list_checked_regions[i]['county']['name1'], ActiveModal)
                    list_componentsHTML[p].setWrongRow(list_componentsHTML[p].getRowLatitude(),  list_marker[i].getLatitude(), ActiveModal)
                    list_componentsHTML[p].setWrongRow(list_componentsHTML[p].getRowLongitude(), list_marker[i].getLongitude(), ActiveModal)
                }
                else if(list_checked_regions[i]['county']['score']>=60 && list_checked_regions[i]['county']['score']<100){
                    list_componentsHTML[p].setIncorrectRow(list_componentsHTML[p].getRowCounty(),  list_checked_regions[i]['county']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['locality']['score']<60 && list_checked_regions[i]['locality']['name2'] != "null"){
                    list_componentsHTML[p].setWrongRow( list_componentsHTML[p].getRowLocality(),  list_checked_regions[i]['locality']['name1'], ActiveModal)
                    list_componentsHTML[p].setWrongRow(list_componentsHTML[p].getRowLatitude(),  list_marker[i].getLatitude(), ActiveModal)
                    list_componentsHTML[p].setWrongRow(list_componentsHTML[p].getRowLongitude(), list_marker[i].getLongitude(), ActiveModal)
                }
                else if (list_checked_regions[i]['locality']['score']>=60 && list_checked_regions[i]['locality']['score']<100){
                    list_componentsHTML[p].setIncorrectRow( list_componentsHTML[p].getRowLocality(),  list_checked_regions[i]['locality']['name1'], ActiveModal)
                }
                
            }
        }
    }
    MarkersOutPolygon = new ComponentHTML()
    MarkersOutPolygon.createHeaderTable("Lista de Markers fora de Polígonos", "Without", "red")
    MarkersOutPolygon.createTitleTable()
    for(i=0;i<list_marker.length;i++){
            if(!list_marker[i].isInsidePolygon()){
                name = genus[i]+" "+specie[i]
                list_marker[i].setTitle(`\tInfo. da Planilha\nPaís: ${country[i]}\nEstado: ${state[i]}\nMunicípio: ${county[i]}\nLatitude: ${latitudes[i]}\nLongitude: ${longitudes[i]}`)
                MarkersOutPolygon.createBodyTable(name, country[i], state[i], county[i], locality[i], list_marker[i].getLatitude(), list_marker[i].getLongitude(), row_coord_lat[i], i, "without")
                if(list_checked_regions[i]['country']['score']<60 && list_checked_regions[i]['country']['name2'] != "null"){
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowCountry(), list_checked_regions[i]['country']['name1'], ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLatitude(),  list_marker[i].getLatitude(), ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLongitude(), list_marker[i].getLongitude(), ActiveModal)
                }
                else if (list_checked_regions[i]['country']['score']>=60 && list_checked_regions[i]['country']['score']<100){
                    MarkersOutPolygon.setIncorrectRow(MarkersOutPolygon.getRowCountry(), list_checked_regions[i]['country']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['state']['score']<60 && list_checked_regions[i]['state']['name2'] != "null"){

                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowState(), list_checked_regions[i]['state']['name1'], ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLatitude(),  list_marker[i].getLatitude(), ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLongitude(), list_marker[i].getLongitude(), ActiveModal)
                }
                else if(list_checked_regions[i]['state']['score']>=60 && list_checked_regions[i]['state']['score']<100){
                    MarkersOutPolygon.setIncorrectRow(MarkersOutPolygon.getRowState(), list_checked_regions[i]['state']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['county']['score']<60 && list_checked_regions[i]['county']['name2'] != "null"){
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowCounty(),  list_checked_regions[i]['county']['name1'], ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLatitude(),  list_marker[i].getLatitude(), ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLongitude(), list_marker[i].getLongitude(), ActiveModal)
                }
                else if(list_checked_regions[i]['county']['score']>=60 && list_checked_regions[i]['county']['score']<100){
                    MarkersOutPolygon.setIncorrectRow(MarkersOutPolygon.getRowCounty(),  list_checked_regions[i]['county']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['locality']['score']<60 && list_checked_regions[i]['locality']['name2'] != "null"){
                    MarkersOutPolygon.setWrongRow( MarkersOutPolygon.getRowLocality(),  list_checked_regions[i]['locality']['name1'], ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLatitude(),  list_marker[i].getLatitude(), ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLongitude(), list_marker[i].getLongitude(), ActiveModal)
                }
                else if (list_checked_regions[i]['locality']['score']>=60 && list_checked_regions[i]['locality']['score']<100){
                    MarkersOutPolygon.setIncorrectRow( MarkersOutPolygon.getRowLocality(),  list_checked_regions[i]['locality']['name1'], ActiveModal)
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
        var column = this.className
        var text = document.getElementById("modal_text")
        var index = this.id.replace(this.name, "")
        row_modify = row_coord_lat[index]
        column_changed = this.id
        column_modify = spreadsheet_titles[column]
        if(send_server[row_modify] != undefined){
            modify_column = send_server[row_modify]
        }
        else{
            modify_column = {}
        }
        if(region.indexOf(column) > -1){
            if(column == "country"){
                text.innerHTML = `Verificamos que seu PAÍS está incorreto.<br>Observamos que em sua planilha sua coluna referente ao País consta o valor: ${country[index]}<br>Enquanto sua coordenada representa o local: ${list_region[index][column]}`
                modify_column[column_modify] = list_region[index][column]
            }
            else if(column == "state"){
                text.innerHTML = `Verificamos que seu ESTADO está incorreto.<br>Observamos que em sua planilha sua coluna referente ao Estado consta o valor: ${state[index]}<br>Enquanto sua coordenada representa o local: ${list_region[index][column]}`
                modify_column[column_modify] = list_region[index][column]
            }
            else if(column == "county"){
                text.innerHTML = `Verificamos que seu MUNICÍPIO está incorreto.<br>Observamos que em sua planilha sua coluna referente ao Município consta o valor: ${county[index]}<br>Enquanto sua coordenada representa o local: ${list_region[index][column]}`
                modify_column[column_modify] = list_region[index][column]
            }
            else if(column == "locality"){
                text.innerHTML = `Verificamos que sua LOCALIDADE está incorreta.<br>Observamos que em sua planilha sua coluna referente a Localidade consta o valor: ${locality[index]}<br>Enquanto sua coordenada representa o local: ${list_region[index][column]}`
                modify_column[column_modify] = list_region[index][column]
            }
        }
        else if(coordinates.indexOf(column) > -1){
            CompRest = {
                        componentRestrictions: { 
                                                country: country[index],
                                                administrativeArea: state[index],
                                                administrativeArea: county[index],
                                                route: locality[index]
                                               }
                        }
            Geo.geocode(CompRest, function (a, b){
                coordinate = {"latitude": {"decimal": null, "MMDDSS": null, "MMDD": null}, "longitude":{"decimal": null, "MMDDSS": null, "MMDD": null}}               
                latitude = a[0]['geometry']['location']['lat']()
                longitude = a[0]['geometry']['location']['lng']()
                lat_lng = column == "latitude"? "lat":"lng"
                coordinate[column]['decimal'] = lat_lng == "lat"? latitude:longitude
                coord_decimal = coordinate[column]['decimal']
                coordinate[column]['DDMMSS'] = coordinate_conversor.toDDMMSS(coord_decimal, lat_lng)
                coordinate[column]['DDMM'] = coordinate_conversor.toDDMM(coord_decimal, lat_lng)
                text.innerHTML = `Verificamos que sua coordenada está incorreta.<br>A região informada em sua planilha é: ${country[index]}, ${state[index]}, ${county[index]}, ${locality[index]}<br><br>Enquanto que suas coordenadas apontam para: ${list_region[index]['country']}, ${list_region[index]['state']}, ${list_region[index]['county']}, ${list_region[index]['locality']}<br><br>As coordenadas corretas para este local são:<br><br>`
                
                decimal = coordinate[column]['decimal']
                DDMMSS = coordinate[column]['DDMMSS']
                DDMM = coordinate[column]['DDMM']
                input_radio.createRadioInput(modal, `Decimal ${column}: ${decimal}<br><br>`, decimal, SelectedRadio, column)
                input_radio.createRadioInput(modal, `MMDDSS ${column}: ${DDMMSS}<br><br>`, DDMMSS, SelectedRadio, column)
                input_radio.createRadioInput(modal, `MMDD ${column}: ${DDMM}<br><br>`, DDMM, SelectedRadio, column)
            })
        }
    }

    function RemoveRadioModal(){
        input_radio.removeRadioInput(modal)
    }
    function SelectedRadio(){
        column_modify = spreadsheet_titles[this.id]
        modify_column[column_modify] = this.value
    }
    function SaveChange(){
        coord = ["latitude", "longitude"]
        region = ["country", "state", "county", "locality"]
        component = new ComponentHTML()
        changed = document.getElementById(column_changed)
        component.removeStatusWrongRow(changed, modify_column[column_modify], ActiveModal)
        send_server[row_modify] = modify_column
        data.value = JSON.stringify(send_server)

        if(region.indexOf(changed.className) > -1){
            lat_id = changed.id.replace(changed.className, "latitude")
            lng_id = changed.id.replace(changed.className, "longitude")
            lat = document.getElementById(lat_id)
            lng = document.getElementById(lng_id)
            component.removeStatusWrongRow(lat, lat.innerHTML, ActiveModal)
            component.removeStatusWrongRow(lng , lng.innerHTML, ActiveModal)
        }
        if(coord.indexOf(changed.className) > -1){
            country_id = changed.id.replace(changed.className, "country")
            state_id = changed.id.replace(changed.className, "state")
            county_id = changed.id.replace(changed.className, "county")
            locality_id = changed.id.replace(changed.className, "locality")
            country = document.getElementById(country_id)
            state = document.getElementById(state_id)
            county = document.getElementById(county_id)
            locality = document.getElementById(locality_id)
            component.removeStatusWrongRow(country, country.innerHTML, ActiveModal)
            component.removeStatusWrongRow(state , state.innerHTML, ActiveModal)
            component.removeStatusWrongRow(county , county.innerHTML, ActiveModal)
            component.removeStatusWrongRow(locality , locality.innerHTML, ActiveModal)
        }
    }
    Cancel_Buttom.addEventListener("click", RemoveRadioModal)
    Confirm_Buttom.addEventListener("click", RemoveRadioModal)
    Confirm_Buttom.addEventListener("click", SaveChange)
    checkbox_group_markers.addEventListener('change', ActiveMarkerCluster)
}