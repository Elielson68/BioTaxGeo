import requests
animal = "Anodorhynchus hyacinthinus"
#r_especie = requests.get('http://api.vertnet-portal.appspot.com/api/search?q={"q":"'+animal+'"}')
#print(r_especie.text)
Latitude = "-1.45502"
Longitude =  "-48.5024"
Pais = "Brazil"
Nome_cientifico = "Puma concolor"
r_geo = requests.get("http://api-geospatial.vertnet-portal.appspot.com/geospatial?decimalLongitude=1.2324&decimalLatitude=3.2314&scientificName="+Nome_cientifico+"&countryCode="+Pais)

print(r_geo.text)