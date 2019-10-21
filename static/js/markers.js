function Detectar_Marks(latitude, longitude, markers, poligono){
  for(var lat in latitude){
    var coordenadas = new google.maps.LatLng(latitude[lat], longitude[lat])
    var marker = new google.maps.Marker({
      position: coordenadas,
      map: null,
      icon: "",
    });
    markers.push(marker);
  }
  for(var marker in markers){
    for(var poli in poligono){
      var isWithinPolygon = google.maps.geometry.poly.containsLocation(markers[marker].position,poligono[poli])
      if(isWithinPolygon){
        markers[marker].icon = "../static/blue_marker2.png"
        markers[marker].setMap(map)
        Criar_TBody(markers[marker].position["lat"](), markers[marker].position["lng"](), (parseInt(poli)+1))
        break;
      }
      else{
        markers[marker].icon = "../static/red_marker2.png"
        markers[marker].setMap(map)
      }
    }
  }
}
function Criar_TBody(latitude, longitude, indice){
  var elemento_pai = document.getElementById("tbody_poligono"+indice)
  var linha = document.createElement("tr")
  var indice_coluna = document.createElement("th")
  var nome_coluna = document.createElement("td")
  var latitude_coluna = document.createElement("td")
  var longitude_coluna = document.createElement("td")
  linha.appendChild(indice_coluna)
  linha.appendChild(nome_coluna)
  linha.appendChild(latitude_coluna)
  linha.appendChild(longitude_coluna)
  elemento_pai.appendChild(linha)
  latitude_coluna.innerHTML = latitude
  longitude_coluna.innerHTML = longitude
}
function Criar_THead(indice){
  var tabela = document.getElementById("tabela")
  var thead = document.createElement("thead")
  
  var tr_titulo_tabela = document.createElement("tr")
  var th_titulo = document.createElement("th")
  th_titulo.style = "text-align: center"
  th_titulo.setAttribute("colspan",4)
  th_titulo.id = "thead_poligono"+indice
  th_titulo.className = "thead_poligono"
  var texto_th_titulo = document.createTextNode("Lista de Markers dentro do Poligono "+indice)
  th_titulo.appendChild(texto_th_titulo)
  tr_titulo_tabela.appendChild(th_titulo)
  thead.appendChild(tr_titulo_tabela)

  var tr_titulos = document.createElement("tr")
  var th_indice = document.createElement("th")
  th_indice.setAttribute("scope","col")
  th_indice.innerHTML = "#"
  var th_nome = document.createElement("th")
  th_nome.setAttribute("scope","col")
  th_nome.innerHTML = "Nome Científico"
  var th_latitude = document.createElement("th")
  th_latitude.setAttribute("scope","col")
  th_latitude.innerHTML = "Latitude"
  var th_longitude = document.createElement("th")
  th_longitude.setAttribute("scope","col")
  th_longitude.innerHTML = "Longitude"

  tr_titulos.appendChild(th_indice)
  tr_titulos.appendChild(th_nome)
  tr_titulos.appendChild(th_latitude)
  tr_titulos.appendChild(th_longitude)

  thead.append(tr_titulos)

  var tbody = document.createElement("tbody")
  tbody.id = "tbody_poligono"+indice+"none"
  tbody.style = "display: none"

  tabela.appendChild(thead)
  tabela.appendChild(tbody)
}

