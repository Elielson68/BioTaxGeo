import pygbif

nome_especie = ""
pais = ""
gbif = pygbif
latitude = []
longitude = []
if(nome_especie != ""):
    animal = gbif.search(scientificName=nome_especie,country=pais)
    impressao = '' #variável que vai ser usada pra imprimir as informações
    for x in animal['results']:#dentro da variável que referência os dados buscados pelo gbif, ele busca os dados correspondentes a chave results
        if('stateProvince' in x):#Cada if pega como referência uma chave, caso exista ele soma na variável que ficará pra impressão, caso não ele pula pro else
            impressao += 'Estado: ' + x["stateProvince"]+" | "
        else:# se não existir a variável, então ele retorna que a key não existe no determinado dado
            impressao += "Estado: SEM ESTADO | "
        if('locality' in x):
            impressao += 'Local: '+x['locality']+" | "
        else:
            impressao += 'Local: SEM LOCAL | '
        if('decimalLatitude' in x):
            impressao += 'Latitude: '+str(x['decimalLatitude'])+" | "
            latitude.append(x['decimalLatitude'])
        else:
            impressao += 'Local: SEM LATITUDE | '
        if('decimalLongitude' in x):
            impressao += 'Longitude: '+str(x['decimalLongitude'])+" | "
            longitude.append(x['decimalLongitude'])
        else:
            impressao += 'Local: SEM LONGITUDE | '
            impressao += "\n"
            print(impressao)
            impressao = ''

#x['decimalLongitude']
#x['locality']
#x['stateProvince']
#x['decimalLatitude']
#+' Latitude: '+x['decimalLatitude']+' Longitude: '+x['decimalLongitude']
