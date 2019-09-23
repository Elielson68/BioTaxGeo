import os

import pygbif
import xlrd
from flask import Flask, render_template, redirect, url_for, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
latitude = []
longitude = []
nome_especie = ""
pais = ""
escrito = []
pygbif.registry.dataset_metrics(uuid='3f8a1297-3259-4700-91fc-acc4170b27ce')
occ = pygbif



@app.route("/", methods=["GET", "POST"])
def teste():
    return render_template("index.html")


@app.route("/mapa", methods=["GET", "POST"])
def mapa():
    if request.method == 'POST':
        return render_template("map.html", latitude=latitude, longitude=longitude)
    else:
        return render_template("map.html", latitude=latitude, longitude=longitude)


@app.route("/ler", methods=["GET", "POST"])
def ler():
    if request.method == 'POST':
        latitude.clear()
        longitude.clear()
        f = request.files['file']
        f.save(secure_filename(f.filename))
        Ler_Arquivo(secure_filename(f.filename),latitude,longitude)
        return redirect(url_for('mapa'))


@app.route("/pesquisar", methods=["GET", "POST"])
def pesquisar():
    if request.method == 'POST':
        latitude.clear()
        longitude.clear()
        nome_especie = request.form['nome']
        pais = request.form['pais']
        Pesquisar(nome_especie, pais, latitude, longitude)
        return redirect(url_for('mapa'))

def Pesquisar(nome, pais, Latitude, Longitude):
    gbif = pygbif
    animal = gbif.search(scientificName=nome, country=pais)
    print("\n\n\nAnimal pesquisado: {}".format(nome)+".\nNo país: {}".format(pais)+"\n\n\n")
    impressao = ''  # variável que vai ser usada pra imprimir as informações
    for x in animal['results']:  # dentro da variável que referência os dados buscados pelo gbif, ele busca os dados correspondentes a chave results
        if (
                'stateProvince' in x):  # Cada if pega como referência uma chave, caso exista ele soma na variável que ficará pra impressão, caso não ele pula pro else
            impressao += 'Estado: ' + x["stateProvince"] + " | "
        else:  # se não existir a variável, então ele retorna que a key não existe no determinado dado
            impressao += "Estado: SEM ESTADO | "
        if ('locality' in x):
            impressao += 'Local: ' + x['locality'] + " | "
        else:
            impressao += 'Local: SEM LOCAL | '
        if ('decimalLatitude' in x):
            impressao += 'Latitude: ' + str(x['decimalLatitude']) + " | "
            Latitude.append(x['decimalLatitude'])
        else:
            impressao += 'Latitude: SEM LATITUDE | '
        if ('decimalLongitude' in x):
            impressao += 'Longitude: ' + str(x['decimalLongitude']) + " | "
            Longitude.append(x['decimalLongitude'])
        else:
            impressao += 'Longitude: SEM LONGITUDE | '
            impressao += "\n"
        print(impressao)
        impressao = ''

def Ler_Arquivo(arquivo,Latitude,Longitude):
    path = str(os.getcwd()) + "/"+arquivo
    wb = xlrd.open_workbook(path)
    sheets = wb.sheet_names()
    sheet = wb.sheet_by_name(sheets[0])
    linhas = sheet.nrows
    colunas = sheet.ncols
    coluna_lng = ""
    coluna_lat = ""
    armazenar = False

    for coluna in range(colunas):
        for linha in range(linhas):

            if (armazenar and coluna_lat == coluna):
                Latitude.append(sheet.cell(linha, coluna).value)
            if (sheet.cell(linha, coluna).value == "Latitude"):
                armazenar = True
                coluna_lat = coluna

            if (armazenar and coluna_lng == coluna):
                Longitude.append(sheet.cell(linha, coluna).value)
            if (sheet.cell(linha, coluna).value == "Longitude"):
                armazenar = True
                coluna_lng = coluna

app.run(debug=True)