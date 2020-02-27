function plotPolygon() {
    //var mapi = new google.maps.Map(document.getElementById("mapi"), {zoom: 4, center: belem});

    //__________________________________VARIÁVEIS GLOBAIS___________________________________________________________________
    var belem/*.......................*/= {lat:-1.44502, lng: -48.4650};
    var map/*.........................*/= new google.maps.Map(document.getElementById('second_map'), {zoom: 4, center: belem});
    var CHECKBOX_ACTIVE_MARKERCLUSTER/*......*/= document.getElementById("checkbox");
        CHECKBOX_ACTIVE_MARKERCLUSTER.checked  = true;
    var modal/*.......................*/= document.getElementById("modal_body");
    var BUTTOM_CANCEL/*...............*/= document.getElementById("Cancel_Buttom");
    var BUTTOM_CONFIRM/*..............*/= document.getElementById("Confirm_Buttom");
    var BUTTOM_CLOSE/*..............*/= document.getElementById("close_x");
    var DATA/*........................*/= document.getElementById("data");
    var Geo/*.........................*/= new google.maps.Geocoder;
    var COORDINATE_CONVERSOR/*........*/= new Coordinate();
    var INPUT_RADIO/*.................*/= new ComponentHTML();
    var SEND_VALUES_SERVER/*.................*/= {};
    var VALUES_TO_SEND/*...............*/= {};
    var COLUMN_MODIFY/*...............*/= "";
    var COLUMN_CHANGED/*..............*/= null;
    var ROW_MODIFY/*..................*/= null;
    var LIST_POLY/*..................*/ = [];
    var LIST_COMPONENTS_HTML/*........*/ = [];
    var LIST_MARKER/*................*/ = [];
    //_____________________________________________________________________________________________________________________

    for (poly in polygons){
        let selected_polygon = new Polygon(map)
        let header_table = new ComponentHTML()
        selected_polygon.setActive(false)
        selected_polygon.setPath(polygons[poly])
        LIST_POLY.push(selected_polygon)
        header_table.createHeaderTable("Lista de Markers dentro do Polígono "+LIST_POLY.length, LIST_POLY.length)
        header_table.createTitleTable()
        selected_polygon.setTitle("polygon"+LIST_POLY.length)
        LIST_COMPONENTS_HTML.push(header_table)
    }
    for(i=0;i<latitudes.length;i++){
        if (latitudes[i]!=""){
            let coord = new google.maps.LatLng(latitudes[i], longitudes[i])
            let marker = new Point_Marker(coord, map, "../static/image/red_marker2.png" , false)
            LIST_MARKER.push(marker)
        }
    }
    for(i=0;i<LIST_MARKER.length;i++){
        for(p=0; p<LIST_POLY.length; p++){
            if(LIST_POLY[p].haveMarker(LIST_MARKER[i].getPosition())){
                LIST_MARKER[i].setIcon("../static/image/blue_marker2.png")
                LIST_MARKER[i].setInsidePolygon(true)
                LIST_MARKER[i].setTitle(`\tInfo. da Planilha\nPaís: ${country[i]}\nEstado: ${state[i]}\nMunicípio: ${county[i]}\nLatitude: ${latitudes[i]}\nLongitude: ${longitudes[i]}`)
                name = genus[i]+" "+specie[i]
                
                LIST_COMPONENTS_HTML[p].createBodyTable(name, country[i], state[i], county[i], locality[i], LIST_MARKER[i].getLatitude(), LIST_MARKER[i].getLongitude(), row_coord_lat[i], i, LIST_POLY[p].getTitle())


                if(list_checked_regions[i]['country']['score']<60 && list_checked_regions[i]['country']['name2'] != "null"){
                    LIST_COMPONENTS_HTML[p].setWrongRow(LIST_COMPONENTS_HTML[p].getRowCountry(), list_checked_regions[i]['country']['name1'], ActiveModal)
                    LIST_COMPONENTS_HTML[p].setWrongRow(LIST_COMPONENTS_HTML[p].getRowLatitude(),  LIST_MARKER[i].getLatitude(), ActiveModal)
                    LIST_COMPONENTS_HTML[p].setWrongRow(LIST_COMPONENTS_HTML[p].getRowLongitude(), LIST_MARKER[i].getLongitude(), ActiveModal)
                }
                else if (list_checked_regions[i]['country']['score']>=60 && list_checked_regions[i]['country']['score']<100){
                    LIST_COMPONENTS_HTML[p].setIncorrectRow(LIST_COMPONENTS_HTML[p].getRowCountry(), list_checked_regions[i]['country']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['state']['score']<60 && list_checked_regions[i]['state']['name2'] != "null"){

                    LIST_COMPONENTS_HTML[p].setWrongRow(LIST_COMPONENTS_HTML[p].getRowState(), list_checked_regions[i]['state']['name1'], ActiveModal)
                    LIST_COMPONENTS_HTML[p].setWrongRow(LIST_COMPONENTS_HTML[p].getRowLatitude(),  LIST_MARKER[i].getLatitude(), ActiveModal)
                    LIST_COMPONENTS_HTML[p].setWrongRow(LIST_COMPONENTS_HTML[p].getRowLongitude(), LIST_MARKER[i].getLongitude(), ActiveModal)
                }
                else if(list_checked_regions[i]['state']['score']>=60 && list_checked_regions[i]['state']['score']<100){
                    LIST_COMPONENTS_HTML[p].setIncorrectRow(LIST_COMPONENTS_HTML[p].getRowState(), list_checked_regions[i]['state']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['county']['score']<60 && list_checked_regions[i]['county']['name2'] != "null"){
                    LIST_COMPONENTS_HTML[p].setWrongRow(LIST_COMPONENTS_HTML[p].getRowCounty(),  list_checked_regions[i]['county']['name1'], ActiveModal)
                    LIST_COMPONENTS_HTML[p].setWrongRow(LIST_COMPONENTS_HTML[p].getRowLatitude(),  LIST_MARKER[i].getLatitude(), ActiveModal)
                    LIST_COMPONENTS_HTML[p].setWrongRow(LIST_COMPONENTS_HTML[p].getRowLongitude(), LIST_MARKER[i].getLongitude(), ActiveModal)
                }
                else if(list_checked_regions[i]['county']['score']>=60 && list_checked_regions[i]['county']['score']<100){
                    LIST_COMPONENTS_HTML[p].setIncorrectRow(LIST_COMPONENTS_HTML[p].getRowCounty(),  list_checked_regions[i]['county']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['locality']['score']<60 && list_checked_regions[i]['locality']['name2'] != "null"){
                    LIST_COMPONENTS_HTML[p].setWrongRow( LIST_COMPONENTS_HTML[p].getRowLocality(),  list_checked_regions[i]['locality']['name1'], ActiveModal)
                    LIST_COMPONENTS_HTML[p].setWrongRow(LIST_COMPONENTS_HTML[p].getRowLatitude(),  LIST_MARKER[i].getLatitude(), ActiveModal)
                    LIST_COMPONENTS_HTML[p].setWrongRow(LIST_COMPONENTS_HTML[p].getRowLongitude(), LIST_MARKER[i].getLongitude(), ActiveModal)
                }
                else if (list_checked_regions[i]['locality']['score']>=60 && list_checked_regions[i]['locality']['score']<100){
                    LIST_COMPONENTS_HTML[p].setIncorrectRow( LIST_COMPONENTS_HTML[p].getRowLocality(),  list_checked_regions[i]['locality']['name1'], ActiveModal)
                }
                
            }
        }
    }
    MarkersOutPolygon = new ComponentHTML()
    MarkersOutPolygon.createHeaderTable("Lista de Markers fora de Polígonos", "Without", "red")
    MarkersOutPolygon.createTitleTable()
    for(i=0;i<LIST_MARKER.length;i++){
            if(!LIST_MARKER[i].isInsidePolygon()){
                name = genus[i]+" "+specie[i]
                LIST_MARKER[i].setTitle(`\tInfo. da Planilha\nPaís: ${country[i]}\nEstado: ${state[i]}\nMunicípio: ${county[i]}\nLatitude: ${latitudes[i]}\nLongitude: ${longitudes[i]}`)
                MarkersOutPolygon.createBodyTable(name, country[i], state[i], county[i], locality[i], LIST_MARKER[i].getLatitude(), LIST_MARKER[i].getLongitude(), row_coord_lat[i], i, "without")
                if(list_checked_regions[i]['country']['score']<60 && list_checked_regions[i]['country']['name2'] != "null"){
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowCountry(), list_checked_regions[i]['country']['name1'], ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLatitude(),  LIST_MARKER[i].getLatitude(), ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLongitude(), LIST_MARKER[i].getLongitude(), ActiveModal)
                }
                else if (list_checked_regions[i]['country']['score']>=60 && list_checked_regions[i]['country']['score']<100){
                    MarkersOutPolygon.setIncorrectRow(MarkersOutPolygon.getRowCountry(), list_checked_regions[i]['country']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['state']['score']<60 && list_checked_regions[i]['state']['name2'] != "null"){

                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowState(), list_checked_regions[i]['state']['name1'], ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLatitude(),  LIST_MARKER[i].getLatitude(), ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLongitude(), LIST_MARKER[i].getLongitude(), ActiveModal)
                }
                else if(list_checked_regions[i]['state']['score']>=60 && list_checked_regions[i]['state']['score']<100){
                    MarkersOutPolygon.setIncorrectRow(MarkersOutPolygon.getRowState(), list_checked_regions[i]['state']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['county']['score']<60 && list_checked_regions[i]['county']['name2'] != "null"){
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowCounty(),  list_checked_regions[i]['county']['name1'], ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLatitude(),  LIST_MARKER[i].getLatitude(), ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLongitude(), LIST_MARKER[i].getLongitude(), ActiveModal)
                }
                else if(list_checked_regions[i]['county']['score']>=60 && list_checked_regions[i]['county']['score']<100){
                    MarkersOutPolygon.setIncorrectRow(MarkersOutPolygon.getRowCounty(),  list_checked_regions[i]['county']['name1'], ActiveModal)
                }
                if(list_checked_regions[i]['locality']['score']<60 && list_checked_regions[i]['locality']['name2'] != "null"){
                    MarkersOutPolygon.setWrongRow( MarkersOutPolygon.getRowLocality(),  list_checked_regions[i]['locality']['name1'], ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLatitude(),  LIST_MARKER[i].getLatitude(), ActiveModal)
                    MarkersOutPolygon.setWrongRow(MarkersOutPolygon.getRowLongitude(), LIST_MARKER[i].getLongitude(), ActiveModal)
                }
                else if (list_checked_regions[i]['locality']['score']>=60 && list_checked_regions[i]['locality']['score']<100){
                    MarkersOutPolygon.setIncorrectRow( MarkersOutPolygon.getRowLocality(),  list_checked_regions[i]['locality']['name1'], ActiveModal)
                }
            }
    }
    var opt_options = {imagePath:'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m', gridSize: 60, maxZoom: 14, minimumClusterSize: 2}
    var markerCluster = new MarkerClusterer(map, LIST_MARKER, opt_options);
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
        let region = ["country", "state", "county", "locality"]
        let coordinates = ["latitude", "longitude"]
        let column = this.className
        let text = document.getElementById("modal_text")
        let index = this.id.replace(this.name, "")
        ROW_MODIFY = row_coord_lat[index]
        COLUMN_CHANGED = this.id
        COLUMN_MODIFY = spreadsheet_titles[column]
        if(SEND_VALUES_SERVER[ROW_MODIFY] != undefined){
            VALUES_TO_SEND = SEND_VALUES_SERVER[ROW_MODIFY]
        }
        else{
            VALUES_TO_SEND = {}
        }
        if(region.indexOf(column) > -1){
            if(column == "country"){
                text.innerHTML = `Verificamos que seu PAÍS está incorreto.<br>Observamos que em sua planilha sua coluna referente ao País consta o valor: <b style='color: red;'>${country[index]}</b><br>Enquanto sua coordenada representa o local: <b style='color: green;'>${list_region[index][column]}<b>`
                VALUES_TO_SEND[COLUMN_MODIFY] = list_region[index][column]
            }
            else if(column == "state"){
                text.innerHTML = `Verificamos que seu ESTADO está incorreto.<br>Observamos que em sua planilha sua coluna referente ao Estado consta o valor: <b style='color: red;'>${state[index]}</b><br>Enquanto sua coordenada representa o local: <b style='color: green;'>${list_region[index][column]}<b>`
                VALUES_TO_SEND[COLUMN_MODIFY] = list_region[index][column]
            }
            else if(column == "county"){
                text.innerHTML = `Verificamos que seu MUNICÍPIO está incorreto.<br>Observamos que em sua planilha sua coluna referente ao Município consta o valor: <b style='color: red;'>${county[index]}</b><br>Enquanto sua coordenada representa o local: <b style='color: green;'>${list_region[index][column]}<b>`
                VALUES_TO_SEND[COLUMN_MODIFY] = list_region[index][column]
            }
            else if(column == "locality"){
                text.innerHTML = `Verificamos que sua LOCALIDADE está incorreta.<br>Observamos que em sua planilha sua coluna referente a Localidade consta o valor: <b style='color: red;'>${locality[index]}</b><br>Enquanto sua coordenada representa o local: <b style='color: green;'>${list_region[index][column]}<b>`
                VALUES_TO_SEND[COLUMN_MODIFY] = list_region[index][column]
            }
        }
        else if(coordinates.indexOf(column) > -1){
            let CompRest = {
                        componentRestrictions: { 
                                                country: country[index],                                                
                                                administrativeArea: `${state[index]}, ${county[index]}`,
                                                locality: locality[index]                                                
                                               }
                } 
            Geo.geocode(CompRest, function (a){
                for(x of a){
                    console.log(x['address_components'])
                }
                coordinate = {"latitude": {"decimal": null, "MMDDSS": null, "MMDD": null}, "longitude":{"decimal": null, "MMDDSS": null, "MMDD": null}}               
                latitude = a[0]['geometry']['location']['lat']()
                longitude = a[0]['geometry']['location']['lng']()
                lat_lng = column == "latitude" ? "lat":"lng"
                coordinate[column]['decimal'] = lat_lng == "lat"? latitude:longitude
                coord_decimal = coordinate[column]['decimal']
                coordinate[column]['DDMMSS'] = COORDINATE_CONVERSOR.toDDMMSS(coord_decimal, lat_lng)
                coordinate[column]['DDMM'] = COORDINATE_CONVERSOR.toDDMM(coord_decimal, lat_lng)
                text.innerHTML = `Verificamos que sua coordenada está incorreta.<br>A região informada em sua planilha é: ${country[index]}, ${state[index]}, ${county[index]}, ${locality[index]}<br><br>Enquanto que suas coordenadas apontam para: ${list_region[index]['country']}, ${list_region[index]['state']}, ${list_region[index]['county']}, ${list_region[index]['locality']}<br><br>As coordenadas corretas para este local são:<br><br>`
                
                decimal = coordinate[column]['decimal']
                DDMMSS = coordinate[column]['DDMMSS']
                DDMM = coordinate[column]['DDMM']
                INPUT_RADIO.createRadioInput(modal, `Decimal ${column}: ${decimal}<br><br>`, decimal, SelectedRadio, column)
                INPUT_RADIO.createRadioInput(modal, `MMDDSS ${column}: ${DDMMSS}<br><br>`, DDMMSS, SelectedRadio, column)
                INPUT_RADIO.createRadioInput(modal, `MMDD ${column}: ${DDMM}<br><br>`, DDMM, SelectedRadio, column)
            })
        }
    }

    function RemoveRadioModal(){
        INPUT_RADIO.removeRadioInput(modal)
    }
    function SelectedRadio(){
        COLUMN_MODIFY = spreadsheet_titles[this.id]
        VALUES_TO_SEND[COLUMN_MODIFY] = this.value
    }
    function SaveChange(){
        var coord = ["latitude", "longitude"]
        var region = ["country", "state", "county", "locality"]
        var component = new ComponentHTML()
        var changed = document.getElementById(COLUMN_CHANGED)
        component.removeStatusWrongRow(changed, VALUES_TO_SEND[COLUMN_MODIFY], ActiveModal)
        SEND_VALUES_SERVER[ROW_MODIFY] = VALUES_TO_SEND
        DATA.value = JSON.stringify(SEND_VALUES_SERVER)

        if(region.indexOf(changed.className) > -1){
            var lat_id = changed.id.replace(changed.className, "latitude")
            var lng_id = changed.id.replace(changed.className, "longitude")
            var lat = document.getElementById(lat_id)
            var lng = document.getElementById(lng_id)
            component.removeStatusWrongRow(lat, lat.innerHTML, ActiveModal)
            component.removeStatusWrongRow(lng , lng.innerHTML, ActiveModal)
        }
        if(coord.indexOf(changed.className) > -1){
            var country_id = changed.id.replace(changed.className, "country")
            var state_id = changed.id.replace(changed.className, "state")
            var county_id = changed.id.replace(changed.className, "county")
            var locality_id = changed.id.replace(changed.className, "locality")
            
            var country = document.getElementById(country_id)
            var state = document.getElementById(state_id)
            var county = document.getElementById(county_id)
            var locality = document.getElementById(locality_id)
            component.removeStatusWrongRow(country, country.innerHTML, ActiveModal)
            component.removeStatusWrongRow(state , state.innerHTML, ActiveModal)
            component.removeStatusWrongRow(county , county.innerHTML, ActiveModal)
            component.removeStatusWrongRow(locality , locality.innerHTML, ActiveModal)
        }
    }
    BUTTOM_CANCEL.addEventListener("click", RemoveRadioModal)
    BUTTOM_CONFIRM.addEventListener("click", RemoveRadioModal)
    BUTTOM_CLOSE.addEventListener("click", RemoveRadioModal)
    BUTTOM_CONFIRM.addEventListener("click", SaveChange)
    CHECKBOX_ACTIVE_MARKERCLUSTER.addEventListener('change', ActiveMarkerCluster)
}