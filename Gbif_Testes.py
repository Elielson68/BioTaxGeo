#'''
import pygbif
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from planilha import Planilha
import requests

occ = pygbif
app = Flask(__name__)
planilha_atual = Planilha()


@app.route("/", methods=["GET", "POST"])
def mapa_teste():
    if request.method == 'GET':
        return render_template("mapa_teste.html")
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        planilha_atual.set_Diretorio(secure_filename(f.filename))
        planilha_atual.set_ColG_ColNC("Genus1","Species1")
        return redirect (url_for("species"))

@app.route("/species", methods=["GET", "POST"])
def species():
    if request.method == 'GET':
        return planilha_atual.get_NC_Tratado()
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