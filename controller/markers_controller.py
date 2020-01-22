from flask import render_template, redirect, url_for, request, Blueprint
from controller import home_controller
import requests
from arcgis.gis import GIS
import googlemaps
from arcgis.geocoding import reverse_geocode
gis = GIS()
gmaps = googlemaps.Client(key='AIzaSyCNEzVQus5NRrbNeVKppxbEy7nKre_0Djc')
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
        here_request = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key=AIzaSyCNEzVQus5NRrbNeVKppxbEy7nKre_0Djc"
        states = []
        Localitys = {}
        for x in range(len(coord_lat)):
            reverse_geocode_result = gmaps.reverse_geocode((coord_lat[x], coord_lng[x]), language="pt-BR")
            states.append(reverse_geocode_result)
        Localitys = {"Locais": states}
        return Localitys #render_template("form/markers_form.html", latitude=coord_lat, longitude=coord_lng)

'''
REQUESTS PARA BUSCAR LOCALIZAÇÃO UTILIZANDO REVERSE GEOCODING
UTILIZANDO API DO BIGDATACLOUD (https://www.bigdatacloud.com/geocoding-apis/free-reverse-geocode-to-city-api?gclid=EAIaIQobChMIspzcrZSV5wIVUeWGCh2XjAxKEAAYAiAAEgJgaPD_BwE)
OBS: ELES PROIBEM O USO DESSA API NO LADO DO SERVIDOR, PARA USAR NO SERVIDOR É NECESSÁRIO COMPRAR A LICENÇA DELES
    states = []
    for x in range(len(coord_lat)):
        states.append(requests.get("https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={}&longitude={}&localityLanguage=pt".format(coord_lat[x], coord_lng[x])).json()['principalSubdivision'])
    print(states)
    
TEMPO DE RESPOSTA: 1:36:70 (min/seg/mil)
______________________________________________________________________________________________________________________
UTILIZANDO API DO HERE (https://developer.here.com/documentation/examples/rest/geocoder/reverse-geocode)
O HERE DEMORA BEM MAIS QUE O BIGDATACLOUD PRA FAZER REQUESTS
    here_request = "https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?prox={},{},1150&apiKey=OIQTA4RdTMXLYB7gS-IYkII9M3uwUg12VMGXOBX2uzw&language=pt&mode=retrieveAreas"
    states = []
    for x in range(len(coord_lat)):
        states.append(requests.get(here_request.format(coord_lat[x], coord_lng[x])).json()['Response']['View'][0]['Result'][0]['Location']['Address']['State'])
    print(states)
    
TEMPO DE RESPOSTA: 4:14:14 (min/seg/mil)
_______________________________________________________________________________________________________________________
UTILIZANDO API DO ARCGIS (https://developers.arcgis.com/python/guide/reverse-geocoding/)
    locais = []
    for x in range(len(coord_lat)):
        location = [coord_lng[x], coord_lat[x]]
        results = reverse_geocode(location)
        locais.append((results['address']['City']))
    print(locais)
    print(len(locais))
    
TEMPO DE RESPOSTA: 3:14:17 (min/seg/mil)
'''