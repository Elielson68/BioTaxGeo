from flask import render_template, redirect, url_for, request, Blueprint
from controller import home_controller


Planilha_atual = home_controller.Planilha_atual
markers_blueprint = Blueprint('markers', __name__, template_folder='templates')

@markers_blueprint .route("/markers_validation", methods=["GET", "POST"])
def markers_validation():
    if request.method == "POST":
        coord = request.form["selecao"]
        coord = eval(coord)
        Planilha_atual.coordenadas.set_Latitude_Column_values(coord["latitude"])
        Planilha_atual.coordenadas.set_Longitude_Column_values(coord["longitude"])
        return redirect(url_for("markers.markers_list"))

@markers_blueprint .route("/markers_list",methods=["GET","POST"])
def markers_list():
    if request.method == "POST":
        poligonos = request.form['vertices']
        poligonos = eval(poligonos)
        coord_lat = Planilha_atual.coordenadas.get_Latitude_Column_values()
        coord_lng = Planilha_atual.coordenadas.get_Longitude_Column_values()
        coord_lat = Planilha_atual.coordenadas.Converter_Lat_Decimal(coord_lat)
        coord_lng = Planilha_atual.coordenadas.Converter_Lng_Decimal(coord_lng)
        return render_template("list/markers_list.html", poligonos=poligonos, latitude=coord_lat, longitude=coord_lng)
    else:
        return render_template("form/markers_form.html")
