function initMap() {
    var belem = {lat:-1.44502, lng: -48.4650};
    map = new google.maps.Map(document.getElementById('mapa_criar'), {zoom: 4, center: belem});
    //Primeiro verifico se existe algum poligono salvo no vetor, caso não exista ele atribui alguns eventos a uns botões
    //Esses eventos só podem ser atribuídos 1 vez, pois se não eles vão se acumulando dentro dos componentes e vão gerando bugs
    if(poligonos_salvos.length != 0){
      if(editando == false){ //Verifica se a variável editando é verdadeira ou falso, se for false significa que a pessoa só adicionou mais 1 poligono
        for(plotar_poligono of poligonos_salvos){
          plotar_poligono.fillColor = "#2F4F4F";
          plotar_poligono.setMap(map)
        }
      }
      else{ //Se for verdadeira significa que ela clicou em um poligono para editar
        for(plotar_poligono=0;plotar_poligono<poligonos_salvos.length;plotar_poligono++){ //Aqui ele verifica todos os poligonos criados até o momento
          if(plotar_poligono != poligono_selecionado){ //Se o índice que o for estiver percorrendo for diferente ele plota o polígono salvo no mapa normalmente, só que com uma cor diferente.
            poligonos_salvos[plotar_poligono].fillColor = "#2F4F4F";
            poligonos_salvos[plotar_poligono].setMap(map)
          }
          else{ //Se for igual ele vem pra cá e faz essas alteraçções, muda a cor pra vermelha que é a cor de edição padrão, ele resgata o objeto do vetor e plota ele no mapa
            Poligono_Escolhido(plotar_poligono)
          }
        }
      }
    }
    else{
      botao_salvar_vertices = document.getElementById("button_salvar")
      botao_salvar_vertices.addEventListener('click',SalvarVertices)
      botao_criar_novo_poligono = document.getElementById("botao_criar_novo_poligono")
      botao_criar_novo_poligono.addEventListener('click',Plotar_novo_poligono)
      criar_vertices_button.addEventListener('click', CriarVerticesButton);
    }
    if(editando == false){ //Se for verdadeiro ele não irá criar um novo polígono ao iniciar a função initMap novamente.
      var Poligono = new google.maps.Polygon({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
      })
      poligonos_salvos.push(Poligono)
      poligonos_salvos[poligonos_salvos.length-1].title = "Poligono "+poligonos_salvos.length
      infoWindow.push(new google.maps.InfoWindow)
      contentString = `<b>Poligono ${poligonos_salvos.length}</b><br>`
      infoWindow[infoWindow.length-1].setContent(contentString);
      poligonos_salvos[poligonos_salvos.length-1].addListener("click",function(event){
        infoWindow[(this.title.replace("Poligono ",""))-1].setPosition(event.latLng);
        infoWindow[(this.title.replace("Poligono ",""))-1].open(map);
      })
      poligono_criado["poligono"+(poligonos_salvos.length)] = []
      poligonos_salvos[poligono_selecionado].setMap(map);
    }
    map.addListener('click', addLatLng);  
}