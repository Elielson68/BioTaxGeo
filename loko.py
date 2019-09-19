from flask import Flask, jsonify, render_template, redirect, url_for, request
from werkzeug import secure_filename
import pygbif
app = Flask(__name__)
latitude = []
longitude = []
nome_especie = ""
pais = ""
escrito = []
def Pesquisar(nome, pais):
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
            latitude.append(x['decimalLatitude'])
        else:
            impressao += 'Latitude: SEM LATITUDE | '
        if ('decimalLongitude' in x):
            impressao += 'Longitude: ' + str(x['decimalLongitude']) + " | "
            longitude.append(x['decimalLongitude'])
        else:
            impressao += 'Longitude: SEM LONGITUDE | '
            impressao += "\n"
        print(impressao)
        impressao = ''



@app.route("/", methods=["GET", "POST"])
def teste():
    if request.method == 'POST':
        nome_especie = request.form['NomeC']
        pais = request.form['pais']
        Pesquisar(nome_especie, pais)
        return redirect(url_for('mapa'))
    else:
        return render_template("index.html")


@app.route("/mapa", methods=["GET", "POST"])
def mapa():
    return render_template("map.html", latitude=latitude, longitude=longitude)
@app.route("/ler",methods=["GET","POST"])
def ler():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        arquivo = open(f.filename,'r')
        for linha in arquivo:
            escrito.append(linha)

        arquivo.close()
        print(escrito)
        return render_template("leitura.html", escrito=escrito)

@app.route("/gbif")
def gbif():
    from req_gbif import animal
    return animal

app.run(debug=True)
