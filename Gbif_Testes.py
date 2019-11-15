#'''
from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for, current_app, send_from_directory
from werkzeug.utils import secure_filename
from planilha import Planilha
import json
app = Flask(__name__)
planilha_atual = Planilha()


@app.route("/", methods=["GET", "POST"])
def mapa_teste():
    if request.method == 'GET':
        #planilha_atual.tratamento_de_dados.AlterandoDadosPlanilha()
        return render_template("mapa_teste.html")
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        planilha_atual.set_Diretorio(secure_filename(f.filename))        
        return render_template("requerimentos_para_leitura_de_planilha.html", titulos=planilha_atual.get_Cabecario_Planilha())

@app.route("/verificacao", methods=["GET", "POST"])
def verificacao():
    if request.method == "POST":
        titulos = request.form["selecao"]
        titulos = eval(titulos)
        planilha_atual.set_Colunas_para_verificar(titulos)
        return planilha_atual.get_Colunas_para_verificar()

#'POLYGON(([longitude ->]-60.2910 [latitude ->]-14.4626,-52.6142 -14.4626, -53.5810 -22.2995,  -60.1591 -22.2995, -60.2910 -14.4626))'

app.run(debug=True, port=8080)
#'''

'''
import requests
from planilha import Planilha
planilha_atual = Planilha()
planilha_atual.set_Diretorio("teste_leitura_latitude_longitude_leitura_autonoma.xls")
print(planilha_atual.__dict__)
'''