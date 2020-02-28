'''
from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for, current_app, send_from_directory
from werkzeug.utils import secure_filename
from planilha import Planilha
import json
app = Flask(__name__)
Planilha_atual = Planilha()
coord_lat = []
coord_lng = []
@app.route("/", methods=["GET", "POST"])
def mapa_teste():
    if request.method == 'GET':
        #planilha_atual.tratamento_de_dados.AlterandoDadosPlanilha()
        return render_template("mapa_teste.html")
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        Planilha_atual.set_Diretorio(secure_filename(f.filename))        
        return render_template("markers_form.html", titulos=Planilha_atual.get_Cabecario_Planilha())

@app.route("/verificacao_planilha", methods=["GET", "POST"])
def verificacao():
    if request.method == "POST":
        coord = request.form["selecao"]
        coord = eval(coord)
        Planilha_atual.coordenadas.set_Latitude_Column_values(coord["latitude"])
        Planilha_atual.coordenadas.set_Longitude_Column_values(coord["longitude"])
        return redirect(url_for("mapa_desenhar"))

@app.route("/mapa_desenhar",methods=["GET","POST"])
def mapa_desenhar():
    if request.method == "POST":
        poligonos = request.form['vertices']
        poligonos = eval(poligonos)
        coord_lat = Planilha_atual.coordenadas.get_Latitude_Column_values()
        coord_lng = Planilha_atual.coordenadas.get_Longitude_Column_values()
        coord_lat = Planilha_atual.coordenadas.Converter_Lat_Decimal(coord_lat)
        coord_lng = Planilha_atual.coordenadas.Converter_Lng_Decimal(coord_lng)
        return render_template("markers_list.html", poligonos=poligonos, latitude=coord_lat, longitude=coord_lng)
    else:
        return render_template("markers_form_map.html")

#'POLYGON(([longitude ->]-60.2910 [latitude ->]-14.4626,-52.6142 -14.4626, -53.5810 -22.2995,  -60.1591 -22.2995, -60.2910 -14.4626)
app.run(debug=True, port=8080)

'''
from model.sheet_treatment import Sheet
Planilha_atual = Sheet()
Planilha_atual.set_Path("Planilha_Formatada.xls")
Coordenadas = Planilha_atual.coordinate
#Planilha_atual.coordenadas.set_Latitude("03° 20' 16.44\" S")
#print(Coordenadas.get_Latitude())
#Planilha_atual.coordenadas.set_Longitude("e 42 41.546 58.648")
#Coordenadas.Adicionar_Coordenada("s 1° 23.546' 85.648\"", "e 42 41.546 58.648")
#Coordenadas.Adicionar_Coordenada("n 2° 53.896' 35.648\"", "e 32 61.546")
#Coordenadas.set_Latitude_Column_values("Latitude1")
#Coordenadas.set_Longitude_Column_values("Longitude1")
#coord_lat = Coordenadas.get_Latitude_Column_values()
#coord_lng = Coordenadas.get_Longitude_Column_values()
latitudes = ["1° 44' 53,94\" S", "-1° 44' 53,94\"", "S 1° 44' 53,94\"", "1° 44' 53,94\" N", "1° 44.899' S", "1 44.899' S", "1° 44.899 S", "1 44.899 S"]
print(Coordenadas.Convert_Lat_Decimal(latitudes))
