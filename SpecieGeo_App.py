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


@app.route("/requerimento_planilha", methods=["GET", "POST"])
def ler_planilha():
    if request.method == 'GET':
        return render_template("requerimentos_para_leitura_de_planilha.html", titulos=Planilha_atual.get_Cabecario_Planilha())


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
        return render_template("plotar_poligono_no_mapa.html", poligonos=poligonos, latitude=Planilha_atual.get_Latitude(), longitude=Planilha_atual.get_Longitude())
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

app.run(debug=True, port=8080)