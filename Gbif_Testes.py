'''
import pygbif
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from planilha import Planilha

occ = pygbif
app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def mapa_teste():
    if request.method == 'GET':
        return render_template("mapa_teste.html")
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        planilha_atual = Planilha(secure_filename(f.filename))
        planilha_atual.get_Total_de_colunas()
        planilha_atual.get_Total_de_linhas()
        planilha_atual.get_Valor_na_celula(6, 2)
        planilha_atual.get_Valores_na_coluna(6)
        planilha_atual.get_Valores_na_coluna(2)
        return render_template("mapa_teste.html")

#'POLYGON(([longitude ->]-60.2910 [latitude ->]-14.4626,-52.6142 -14.4626, -53.5810 -22.2995,  -60.1591 -22.2995, -60.2910 -14.4626))'

app.run(debug=True, port=8080)
'''
from planilha import Planilha
planilha_atual = Planilha()
planilha_atual.set_Diretorio("teste_leitura_latitude_longitude_leitura_autonoma.xls")
planilha_atual.set_Latitude_values("Latitude")
planilha_atual.set_Longitude_values("Longitude")
print(planilha_atual.get_Latitude_values())
