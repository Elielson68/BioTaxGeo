from flask import Flask, jsonify, render_template, redirect, url_for, make_response
import requests
app = Flask(__name__)

#animal = "Anodorhynchus hyacinthinus"
#Latitude = "-1.45502"
#Longitude =  "-48.5024"
#Pais = "Brazil"
dados = {
    'occurrenceId': "teste",
}
pesquisar = dados

def Buscar_ocorrencia(quantidade):
    pesquisar = []
    for criar in range(1,int(quantidade)+1):
        pais = input("Digite o país: ")
        Nome_cientifico = input("Digite o nome cientifico: ")
        try:
            latitude = float(str(input("Digite a latitude: ")))

        except:
            latitude = ""
        try:
            longitude = float(str(input("Digite a longitude: ")))
        except:
            longitude = ""
        print("\n")
        dados = {
                 'occurrenceId':              criar,
                 'decimalLatitude':        latitude,
                 'decimalLongitude':      longitude,
                 'countryCode':                pais,
                 'scientificName':  Nome_cientifico,
                }
        pesquisar.append(dados)
    pesquisar = str(pesquisar)
    return pesquisar.replace("'", '\"')

@app.route("/")
def json_api():
    quantidade = int(input("Quantas ocorrências? "))
    resultado = requests.post("http://api-geospatial.vertnet-portal.appspot.com/geospatial", Buscar_ocorrencia(quantidade))
    print(resultado.json())
    return jsonify(resultado.json())
app.run()





