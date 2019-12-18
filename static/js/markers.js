function Detectar_Marks(latitude, longitude, markers, poligono){
  //Cria os markers e os insere no vetor
  
  for(var lat in latitude){
    var coordenadas = new google.maps.LatLng(latitude[lat], longitude[lat])
    var marker = new google.maps.Marker({
      title: "Lat: "+latitude[lat]+"\nLng: "+longitude[lat],
      position: coordenadas,
      map: null,
      icon: "",
    });
    markers.push(marker);
  }
  //Identifica cada marker em cada um dos poligonos, ele pega 1 marker de cada vez pra verificar em todos os poligonos
  
  for(var poli in poligono){
    contador = 0
    vazio = true//Verifica se o poligono está vazio, ele começa com true pra facilitar a identificação.
    for(var marker in markers){
      var isWithinPolygon = google.maps.geometry.poly.containsLocation(markers[marker].position,poligono[poli])
      if(isWithinPolygon){
        vazio = false //Caso ele encontre alguma marca dentro ele já se torna falso e não cria problemas.
        contador++
        //Caso ele esteja dentro de algum poligono então ele se torna azul e o looping para e vai pro próximo marker
        markers[marker].icon = "../static/image/blue_marker2.png"
        markers[marker].setMap(map)
        Criar_TBody(markers[marker].position["lat"](), markers[marker].position["lng"](), (parseInt(poli)+1), contador, isWithinPolygon)
      }
      else if(markers[marker].icon != "../static/image/blue_marker2.png"){
        //Se não ele continua verificando e inserindo o marker vermelho
        markers[marker].icon = "../static/image/red_marker2.png"
        markers[marker].setMap(map)
      }
    }
    if(vazio){
      Criar_TBody_Vazio((parseInt(poli)+1));
    }
  }
}
//Cria o corpo de cada tabela referente aos poligonos.
function Criar_TBody(latitude, longitude, indice, contador){
  //Criando os dados de cada tabela referente aos poligonos

  if(contador==1){
      var tr_titulos = document.createElement("tr")
      var th_indice = document.createElement("th")
      var th_nome = document.createElement("th")
      var th_latitude = document.createElement("th")
      var th_longitude = document.createElement("th")
      var thead = document.getElementById("thead_poligono"+indice)
  
      //Títulos de cada coluna
      th_indice.setAttribute("scope","col")
      th_indice.innerHTML = "#"
      th_nome.setAttribute("scope","col")
      th_nome.innerHTML = "Nome Científico"
      th_latitude.setAttribute("scope","col")
      th_latitude.innerHTML = "Latitude"
      th_longitude.setAttribute("scope","col")
      th_longitude.innerHTML = "Longitude"
      //Anexando todos eles a coluna principal
      tr_titulos.appendChild(th_indice)
      tr_titulos.appendChild(th_nome)
      tr_titulos.appendChild(th_latitude)
      tr_titulos.appendChild(th_longitude)
      tr_titulos.id = "tr_poligono"+indice
      tr_titulos.setAttribute("class","collapse "+"tab_poligono"+indice)
      //anexando ao cabeçário da tabela
      thead.append(tr_titulos)
    }

    var elemento_pai = document.getElementById("tbody_poligono"+indice)
    var linha = document.createElement("tr")
    var indice_coluna = document.createElement("th")
    indice_coluna.innerHTML = contador
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
//Criar o cabeçario
function Criar_THead(indice){
  //Pegando o ID da tabela
  var tabela = document.getElementById("tabela")
  //Criando o cabeçario da tabela
  var thead = document.createElement("thead")
  var tr_titulo_tabela = document.createElement("tr")
  var th_titulo = document.createElement("th")
  var texto_th_titulo;
  //Criando o corpo da tabela
  var tbody = document.createElement("tbody")
  //Define a cor de fundo do título
  thead.className = "thead-light";

  //Título principal
  th_titulo.style = "text-align: center"
  th_titulo.setAttribute("colspan",4)
  th_titulo.className = "thead"
  texto_th_titulo = document.createElement("button")
  texto_th_titulo.innerHTML = "Lista de Markers dentro do Poligono "+indice
  texto_th_titulo.setAttribute("class","btn btn-link")
  th_titulo.appendChild(texto_th_titulo)
  th_titulo.setAttribute("data-toggle","collapse")
  th_titulo.setAttribute("data-target",".tab_poligono"+indice)
  th_titulo.setAttribute("aria-expanded","false")
  th_titulo.setAttribute("aria-controls","tbody_poligono"+indice)
  tr_titulo_tabela.appendChild(th_titulo)
  thead.appendChild(tr_titulo_tabela)

  //Identificando o body para inserir os dados de cada poligono individualmente
  tbody.id = "tbody_poligono"+indice
  thead.id = "thead_poligono"+indice
  tbody.setAttribute("class","collapse "+"tab_poligono"+indice)

  //Anexado o cabeçario e o corpo na tabela
  tabela.appendChild(thead)
  tabela.appendChild(tbody)
}
//Caso o polígono não contenha nenhum marker ele chama essa função. Ele cria uma linha que indica que não há markers dentro do poligono.
function Criar_TBody_Vazio(indice){
  var tbody = document.getElementById("tbody_poligono"+indice);
  var tr_titulo = document.createElement("tr");
  tr_titulo.id = "tr_poligono"+indice
  tr_titulo.setAttribute("class","collapse "+"tab_poligono"+indice)
  
  var th_vazio = document.createElement("th");

  th_vazio.setAttribute("scope","col");
  th_vazio.innerHTML = "Está vazio.";
  
  th_vazio.setAttribute("colspan",4);
  tr_titulo.style = "text-align: center";
  tr_titulo.appendChild(th_vazio);
  tbody.appendChild(tr_titulo);
}
