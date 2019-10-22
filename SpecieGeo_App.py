import os
import pygbif
import xlrd
from flask import Flask, jsonify, render_template, redirect, url_for, request
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
latitude = []
longitude = []
nome_especie = ""
pais = ""
escrito = []
occ = pygbif



@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/ler_planilha", methods=["GET", "POST"])
def ler_planilha():
    if request.method == 'POST':
        latitude.clear()
        longitude.clear()
        f = request.files['file']
        f.save(secure_filename(f.filename))
        Ler_Arquivo(secure_filename(f.filename),latitude,longitude)
        return redirect(url_for('mapa_desenhar'))

@app.route("/mapa_desenhar",methods=["GET","POST"])
def mapa_desenhar():
    if request.method == "POST":
        poligonos = request.form['vertices']
        poligonos = eval(poligonos)
        return render_template("plotar_poligono_no_mapa.html", poligonos=poligonos, latitude=latitude, longitude=longitude)
    else:
        return render_template("criar_poligono_no_mapa.html")

#Criar um arquivo onde vai ser a classe de pesquisa, qualquer coisa referente a pesquisa deve ser criado lá
def Pesquisar(nome, pais, Latitude, Longitude):
    gbif = pygbif
    animal = gbif.search(scientificName=nome, country=pais)
    print("\n\n\nAnimal pesquisado: {}".format(nome)+".\nNo país: {}".format(pais)+"\n\n\n")
    impressao = ''  # variável que vai ser usada pra imprimir as informações
    for x in animal['results']:  # dentro da variável que referência os dados buscados pelo gbif, ele busca os dados correspondentes a chave results
        if ('stateProvince' in x):  # Cada if pega como referência uma chave, caso exista ele soma na variável que ficará pra impressão, caso não ele pula pro else
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
            Longitude.append(x['dec19imalLongitude'])
        else:
            impressao += 'Longitude: SEM LONGITUDE | '
            impressao += "\n"
        print(impressao)
        impressao = ''
#Criar classe a leitura de arquivo, qualquer coisa referente a leitura de arquivo deve ser feito lá
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

def Pesquisar_Poli(Poligono, lat, long):
    #'POLYGON((-60.2910 -14.4626,-52.6142 -14.4626, -53.5810 -22.2995,  -60.1591 -22.2995, -60.2910 -14.4626))'
    pesquisa = occ.search(geometry=Poligono)
    Resultado_total = ""
    for x in pesquisa['results']:
        Resultado = ""
        if 'countryCode' in x:
            Resultado += "Nome científico: "+x['scientificName']
        else:
            Resultado += "Nome científico: NULO"

        if 'countryCode' in x:
            Resultado += " | Código do País: "+x['countryCode']
        else:
            Resultado += " | Código do País: NULO"

        if 'country' in x:
            Resultado += " | País: "+x['country']
        else:
            Resultado += " | País: NULO"

        if 'stateProvince' in x:
            Resultado += " | Estado: "+x['stateProvince']
        else:
            Resultado += " | Estado: NULO"

        if 'decimalLatitude' in x:
            Resultado += " | Latitude: "+str(x['decimalLatitude'])
            lat.append(x['decimalLatitude'])
        else:
            Resultado += " | Latitude: NULO"

        if 'decimalLongitude' in x:
            Resultado += " | Longitude: "+str(x['decimalLongitude'])
            long.append(x['decimalLongitude'])
        else:
            Resultado += " | Longitude: NULO"
        Resultado_total += Resultado+"\n"
    return print(Resultado_total)
app.run(debug=True, port=8080)