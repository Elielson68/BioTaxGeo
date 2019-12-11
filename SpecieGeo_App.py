import os

import xlrd
from flask import Flask, jsonify, render_template, redirect, url_for, request
import json
from werkzeug.utils import secure_filename
from planilha import Planilha, Coordenadas, Tratamento_de_Dados


app = Flask(__name__)

Planilha_atual = Planilha()


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        if(Planilha_atual.get_Diretorio() == None):
            return render_template("index.html")
        else:
            return  render_template("Selecionar_Rota.html")
    if request.method == "POST":
        f = request.files['file']
        f.save(secure_filename(f.filename))
        Planilha_atual.set_Diretorio(secure_filename(f.filename))        
        return render_template("Selecionar_Rota.html")


@app.route("/requerimento_planilha_tax", methods=["GET", "POST"])
def ler_planilha():
    if request.method == 'GET':
        return render_template("requerimentos_para_leitura_de_planilha.html", titulos=Planilha_atual.get_Cabecario_Planilha())

@app.route("/requerimento_planilha_map", methods=["GET", "POST"])
def ler_planilha2():
    if request.method == 'GET':
        return render_template("requerimento_selecao_coordenadas.html", titulos=Planilha_atual.get_Cabecario_Planilha())

@app.route("/verificacao_planilha", methods=["GET", "POST"])
def verificacao():
    if request.method == "POST":
        titulos = request.form["selecao"]
        if("null" in titulos):
            titulos = titulos.replace("null","None")
        titulos = eval(titulos)
        Planilha_atual.set_Colunas_para_verificar(titulos)
        Planilha_atual.tratamento_de_dados.set_Hierarquia_verificada(Planilha_atual.get_Colunas_para_verificar())
        verificacao = json.dumps(Planilha_atual.tratamento_de_dados.get_Hierarquia_verificada())
        return render_template("planilha.html", verificacao=verificacao, total_linhas = Planilha_atual.get_Total_de_linhas())

@app.route("/verificacao_planilha_mapa", methods=["GET", "POST"])
def verificacao2():
    if request.method == "POST":
        coord = request.form["selecao"]
        coord = eval(coord)
        Planilha_atual.coordenadas.set_Latitude_Column_values(coord["latitude"])
        Planilha_atual.coordenadas.set_Longitude_Column_values(coord["longitude"])
        return redirect(url_for("mapa_desenhar"))

@app.route("/salvar", methods=["GET", "POST"])
def salvar():
    if request.method == "POST":
        dados = request.form["dados"]
        dados = eval(dados)
        Planilha_atual.AlterandoDadosPlanilha(dados)
        Planilha_atual.SalvarPlanilhaFormatada()
        return redirect(url_for("home"))


@app.route("/mapa_desenhar",methods=["GET","POST"])
def mapa_desenhar():
    if request.method == "POST":
        poligonos = request.form['vertices']
        poligonos = eval(poligonos)
        coord_lat = Planilha_atual.coordenadas.get_Latitude_Column_values()
        coord_lng = Planilha_atual.coordenadas.get_Longitude_Column_values()
        coord_lat = Planilha_atual.coordenadas.Converter_Lat_Decimal(coord_lat)
        coord_lng = Planilha_atual.coordenadas.Converter_Lng_Decimal(coord_lng)
        return render_template("plotar_poligono_no_mapa.html", poligonos=poligonos, latitude=coord_lat, longitude=coord_lng)
    else:
        return render_template("criar_poligono_no_mapa.html")

app.run(debug=True, port=8080)