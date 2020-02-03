from flask import render_template, redirect, url_for, request, Blueprint
from controller import home_controller
from model.hierarchy_taxon import Hierarchy_Taxon
import googlemaps

hrch_taxon = Hierarchy_Taxon()
gmaps = googlemaps.Client(key='AIzaSyDJ47tWCXOUSPql_E5MRnw5iFKo9uaaWp8')
used_sheet = home_controller.used_sheet
markers_blueprint = Blueprint('markers', __name__, template_folder='templates')

@markers_blueprint .route("/markers_validation", methods=["GET", "POST"])
def markers_validation():
    if request.method == "POST":
        coord = request.form["selection_coordinate"]
        coord = eval(coord)
        region = request.form["selection_region"]
        region = eval(region)
        region = request.form["selection_region"]
        region = eval(region)
        taxon = request.form["selection_taxon"]
        taxon = eval(taxon)

        used_sheet.coordinate.set_Latitude_Column_values(coord["latitude"])
        used_sheet.coordinate.set_Longitude_Column_values(coord["longitude"])
        used_sheet.locality.set_Country_Column_values(region["country"])
        used_sheet.locality.set_State_Column_values(region["state"])
        used_sheet.locality.set_County_Column_values(region["county"])


        hrch_taxon.set_Genus(used_sheet.Value_in_Column(taxon['genus']))
        hrch_taxon.set_Specie(used_sheet.Value_in_Column(taxon['specie']))

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

        spreadsheet_country = used_sheet.locality.get_Country_Column_values()
        spreadsheet_state = used_sheet.locality.get_State_Column_values()
        spreadsheet_county = used_sheet.locality.get_County_Column_values()

        genus=hrch_taxon.get_Genus()
        specie=hrch_taxon.get_Specie()

        list_empty_values = [i for i, item in enumerate(coord_lat) if item == '']
        count=0
        list_region = []
        list_treatment_region = []
        for x in list_empty_values:
            delete = x-count
            del(coord_lat[delete])
            del(coord_lng[delete])
            del(spreadsheet_country[delete])
            del(spreadsheet_state[delete])
            del(spreadsheet_county[delete])
            del(genus[delete])
            del(specie[delete])
            count+=1
        if len(coord_lat)<=1000:
            
            for x in range(len(coord_lat)):
                region = {"country": None, "state": None, "county": None}
                reverse_geocode_result = gmaps.reverse_geocode((coord_lat[x], coord_lng[x]), language="pt-BR")
                try:
                    region['country'] = reverse_geocode_result[0]['address_components'][2]['long_name']
                except:
                    region['country'] = "null"
                try:
                    region['state'] = reverse_geocode_result[0]['address_components'][1]['long_name']
                except:
                    region['state'] = "null"
                try:
                    region['county'] = reverse_geocode_result[0]['address_components'][0]['long_name']
                except:
                    region['county'] = "null"
                list_region.append(region)
            for x in range(len(list_region)):
                checked_region = {"country": None, "state": None, "county" : None}
                checked_region['country'] = used_sheet.data_treatment.Compare_String(spreadsheet_country[x], list_region[x]['country'])
                checked_region['state'] = used_sheet.data_treatment.Compare_String(spreadsheet_state[x],list_region[x]['state'])
                checked_region['county'] = used_sheet.data_treatment.Compare_String(spreadsheet_county[x],list_region[x]['county'])
                list_treatment_region.append(checked_region)
        else:
            list_region = "null"
            list_treatment_region = "null"
        row_coord_lat = used_sheet.coordinate.get_Index_Row_Lat()
        row_coord_lng = used_sheet.coordinate.get_Index_Row_Lng()
        return render_template("list/markers_list.html", polygons=polygons, latitude=coord_lat, longitude=coord_lng, row_coord_lat=row_coord_lat, row_coord_lng=row_coord_lng, list_region=list_region, country=spreadsheet_country, state=spreadsheet_state, county=spreadsheet_county, genus=genus, specie=specie, list_checked_regions=list_treatment_region)
    else:
        return render_template("form/markers_form.html" )

'''
REQUESTS PARA BUSCAR LOCALIZAÇÃO UTILIZANDO REVERSE GEOCODING
UTILIZANDO API REST DO BIGDATACLOUD (https://www.bigdatacloud.com/geocoding-apis/free-reverse-geocode-to-city-api?gclid=EAIaIQobChMIspzcrZSV5wIVUeWGCh2XjAxKEAAYAiAAEgJgaPD_BwE)
OBS: ELES PROIBEM O USO DESSA API NO LADO DO SERVIDOR, PARA USAR NO SERVIDOR É NECESSÁRIO COMPRAR A LICENÇA DELES
    states = []
    for x in range(len(coord_lat)):
        states.append(requests.get("https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={}&longitude={}&localityLanguage=pt".format(coord_lat[x], coord_lng[x])).json()['principalSubdivision'])
    print(states)
    
TEMPO DE RESPOSTA: 1:36:70 (min/seg/mil)
______________________________________________________________________________________________________________________
UTILIZANDO API REST DO HERE (https://developer.here.com/documentation/examples/rest/geocoder/reverse-geocode)
O HERE DEMORA BEM MAIS QUE O BIGDATACLOUD PRA FAZER REQUESTS
    here_request = "https://reverse.geocoder.ls.hereapi.com/6.2/reversegeocode.json?prox={},{},1150&apiKey=OIQTA4RdTMXLYB7gS-IYkII9M3uwUg12VMGXOBX2uzw&language=pt&mode=retrieveAreas"
    states = []
    for x in range(len(coord_lat)):
        states.append(requests.get(here_request.format(coord_lat[x], coord_lng[x])).json()['Response']['View'][0]['Result'][0]['Location']['Address']['State'])
    print(states)
    
TEMPO DE RESPOSTA: 4:14:14 (min/seg/mil)
_______________________________________________________________________________________________________________________
UTILIZANDO API REST DO ARCGIS (https://developers.arcgis.com/python/guide/reverse-geocoding/)
    locais = []
    for x in range(len(coord_lat)):
        location = [coord_lng[x], coord_lat[x]]
        results = reverse_geocode(location)
        locais.append((results['address']['City']))
    print(locais)
    print(len(locais))
    
TEMPO DE RESPOSTA: 3:14:17 (min/seg/mil)

_______________________________________________________________________________________________________________________
UTILIZANDO API REST DO GOOGLEMAPS 
'''