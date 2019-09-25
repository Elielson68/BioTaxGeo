import pygbif
from flask import Flask, render_template, request

occ = pygbif
app = Flask(__name__)
latitude = []
longitude = []

@app.route("/", methods=["GET", "POST"])
def teste():
    if request.method == 'GET':
        criar_poligono = False
        return render_template("mapa2.html",latitude=latitude,longitude=longitude,criar_poligono=criar_poligono)
    if request.method == 'POST':
        criar_poligono = True
        poligono = request.form['poligono']
        macaco = "eaeuyi"
        vertices = request.form['vertices']
        Pesquisar_Poli(poligono,latitude,longitude)
        return render_template("mapa2.html",latitude=latitude, longitude=longitude,criar_poligono=criar_poligono,vertices=vertices)


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


