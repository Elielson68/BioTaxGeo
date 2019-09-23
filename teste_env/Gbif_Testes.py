import pygbif
from flask import Flask
occ = pygbif
app = Flask(__name__)


@app.route("/")
def teste():
    return "EAE"


app.run(debug=True, port=8080)

pesquisa = occ.search(geometry='POLYGON((-60.2910 -14.4626,-52.6142 -14.4626, -53.5810 -22.2995,  -60.1591 -22.2995, -60.2910 -14.4626))', scientificName="Anodorhynchus hyacinthinus")
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
    else:
        Resultado += " | Latitude: NULO"

    if 'decimalLongitude' in x:
        Resultado += " | Longitude: "+str(x['decimalLongitude'])
    else:
        Resultado += " | Longitude: NULO"
    print(Resultado+"\n")
