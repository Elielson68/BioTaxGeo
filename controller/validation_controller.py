from flask import Flask, jsonify, render_template, redirect, url_for, request, Blueprint
from controller import home_controller
import json

Planilha_atual = home_controller.Planilha_atual
validation_blueprint = Blueprint('validation', __name__, template_folder='templates')

@validation_blueprint.route("/taxon_list", methods=["GET", "POST"])
def taxon_list():
    if request.method == "POST":
        titulos = request.form["selecao"]
        if("null" in titulos):
            titulos = titulos.replace("null","None")
        titulos = eval(titulos)
        Planilha_atual.set_Colunas_para_verificar(titulos)
        Planilha_atual.tratamento_de_dados.set_Hierarquia_verificada(Planilha_atual.get_Colunas_para_verificar())
        verificacao = json.dumps(Planilha_atual.tratamento_de_dados.get_Hierarquia_verificada())
        return render_template("list/taxon_list.html", verificacao=verificacao, total_linhas = Planilha_atual.get_Total_de_linhas())

@validation_blueprint.route("/taxon_validation", methods=["GET", "POST"])
def taxon_validation():
    if request.method == "POST":
        dados = request.form["dados"]
        dados = eval(dados)
        Planilha_atual.AlterandoDadosPlanilha(dados)
        Planilha_atual.SalvarPlanilhaFormatada()
        return redirect(url_for("home.home"))

@validation_blueprint.route("/markers_validation", methods=["GET", "POST"])
def markers_validation():
    if request.method == "POST":
        coord = request.form["selecao"]
        coord = eval(coord)
        Planilha_atual.coordenadas.set_Latitude_Column_values(coord["latitude"])
        Planilha_atual.coordenadas.set_Longitude_Column_values(coord["longitude"])
        return redirect(url_for("validation.markers_list"))

@validation_blueprint.route("/markers_list",methods=["GET","POST"])
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
