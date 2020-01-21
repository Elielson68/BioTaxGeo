from flask import render_template, redirect, url_for, request, Blueprint
from controller import home_controller
import requests
from arcgis.geocoding import reverse_geocode
used_sheet = home_controller.used_sheet
markers_blueprint = Blueprint('markers', __name__, template_folder='templates')

@markers_blueprint .route("/markers_validation", methods=["GET", "POST"])
def markers_validation():
    if request.method == "POST":
        coord = request.form["selection"]
        coord = eval(coord)
        used_sheet.coordinate.set_Latitude_Column_values(coord["latitude"])
        used_sheet.coordinate.set_Longitude_Column_values(coord["longitude"])
        return redirect(url_for("markers.markers_list"))

@markers_blueprint .route("/markers_list",methods=["GET","POST"])
def markers_list():
    if request.method == "POST":
        polygons = request.form['vertices']
        polygons = eval(polygons)
        coord_lat = used_sheet.coordinate.get_Latitude_Column_values()
        coord_lng = used_sheet.coordinate.get_Longitude_Column_values()
        coord_lat = used_sheet.coordinate.Convert_Lat_Decimal(coord_lat)
        coord_lng = used_sheet.coordinate.Convert_Lng_Decimal(coord_lng)
        row_coord_lat = used_sheet.coordinate.get_Index_Row_Lat()
        row_coord_lng = used_sheet.coordinate.get_Index_Row_Lng()
        return render_template("list/markers_list.html", polygons=polygons, latitude=coord_lat, longitude=coord_lng, row_coord_lat=row_coord_lat, row_coord_lng=row_coord_lng)
    else:
        coord_lat = used_sheet.coordinate.get_Latitude_Column_values()
        coord_lng = used_sheet.coordinate.get_Longitude_Column_values()
        coord_lat = used_sheet.coordinate.Convert_Lat_Decimal(coord_lat)
        coord_lng = used_sheet.coordinate.Convert_Lng_Decimal(coord_lng)
        locais = []
        for x in range(len(coord_lat)):
            location = [coord_lat[x], coord_lng[x]]
            results = reverse_geocode(location)
            locais.append((results))
        print(locais)
        return render_template("form/markers_form.html", latitude=coord_lat, longitude=coord_lng)

'''
REQUESTS PARA BUSCAR LOCALIZAÇÃO UTILIZANDO REVERSE GEOCODING
UTILIZANDO API DO BIGDATACLOUD
OBS: ELES PROIBEM O USO DESSA API NO LADO DO SERVIDOR, PARA USAR NO SERVIDOR É NECESSÁRIO COMPRAR A LICENÇA DELES
    states = []
    for x in range(len(coord_lat)):
        states.append(requests.get("https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={}&longitude={}&localityLanguage=pt".format(coord_lat[x], coord_lng[x])).json()['principalSubdivision'])
    print(states)
______________________________________________________________________________________________________________________
UTILIZANDO API DO developer.here.com
O HERE DEMORA BEM MAIS QUE O BIGDATACLOUD PRA FAZER REQUESTS
    here_request = "https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?prox={},{},1150&apiKey=OIQTA4RdTMXLYB7gS-IYkII9M3uwUg12VMGXOBX2uzw&language=pt&mode=retrieveAreas"
    states = []
    for x in range(len(coord_lat)):
        states.append(requests.get(here_request.format(coord_lat[x], coord_lng[x])).json()['View'][0]['Result'][0]['Location']['Address']['State'])
    print(states)
    
'''