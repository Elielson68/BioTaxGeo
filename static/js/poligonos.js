identificador_input = 0;
    var num_vertices = document.getElementById("numero_de_vertices");
    var input_vertices = document.getElementById("input_vertices");
    var focado;
    var poligono_criado = {};
    var poligonos_salvos = [];
    var editando = false
    var poligono_selecionado = 0
    var map;
    var contador = 99;
    var Poligono;
    var markers = [];
    var criar_vertices_button = document.getElementById("button-addon2");
    var numero_poligonos_criados = document.getElementById("numero_poligonos_criados")
    var infoWindow = [];
    numero_poligonos_criados.innerHTML = poligonos_salvos.length
    //Função que inicia o mapa
    function setCriarVertice(lat, lng){
      identificador_input += 1;
      var div_pai = document.createElement('div');
      var div_filha = document.createElement('div');
      var span = document.createElement('span');
      var texto_span  = document.createTextNode(identificador_input.toString()+"ª. "+"Vértice");
      var input_1 = document.createElement('input');
      var input_2 = document.createElement('input');
      var div_button_filha = document.createElement('div');
      var button_excluir = document.createElement('button');
      var texto_button =  document.createTextNode("Excluir");  
      
      div_pai.className = "input-group";
      div_pai.id = "input_vertice"+identificador_input.toString();
      
      div_filha.className = "input-group-prepend";
      div_pai.appendChild(div_filha);

      
      span.className = "input-group-text";
      span.id = "span"+identificador_input;
      div_filha.appendChild(span);

      
      span.appendChild(texto_span);

      
      input_1.type = "text";
      input_1.className = "form-control";
      input_1.placeholder = "Latitude";
      input_1.id = "Lat"+identificador_input.toString();
      div_pai.appendChild(input_1);
      input_1.value = lat;
      input_1.setAttribute("onfocus",`Mudando_valores_poligono(${identificador_input})`);

      
      input_2.type = "text";
      input_2.className = "form-control";
      input_2.placeholder = "Longitude";
      input_2.id = "Lng"+identificador_input.toString();        
      div_pai.appendChild(input_2);
      input_2.value = lng;
      input_2.setAttribute("onfocus",`Mudando_valores_poligono(${identificador_input})`);

      
      div_button_filha.className = "input-group-append";
      div_pai.appendChild(div_button_filha);

      
      
      button_excluir.className = "btn btn-danger";
      button_excluir.id = "Excluir"+identificador_input.toString();
      
      button_excluir.appendChild(texto_button);
      div_button_filha.appendChild(button_excluir);

      div_pai.style = "margin-bottom: 10px;"
      input_vertices.appendChild(div_pai);
    }    
    function Mudando_valores_poligono(index){
      focado = index;
    }
    function addLatLng(event){
        if(contador>0){
          contador -= 1;
          document.getElementById("contador").innerHTML = "Vértices disponíveis: "+contador;
          marker = new google.maps.Marker({
            title: "Vértice: "+(identificador_input+1),
            position: event.latLng,
            map: map,
            icon: "../static/green_marker.png",
            draggable: true
          });
          markers.push(marker);
          markers[markers.length-1].setMap(map);
          marker_latitude = markers[markers.length-1].position["lat"]().toString()
          marker_longitude = markers[markers.length-1].position["lng"]().toString()
          setCriarVertice(marker_latitude,marker_longitude);//Cria um ponto de vértice no mapa a partir do ponto de referência de onde o marker foi clicado

          input_latitude = parseFloat(document.getElementById("Lat"+identificador_input).value)
          input_longitude = parseFloat(document.getElementById("Lng"+identificador_input).value)
          var coordenada_map = new google.maps.LatLng(input_latitude, input_longitude)//Cria um objeto de coordenada do google, que pode ser usado para inserir uma coordeanda de latitude e longitude nos objetos da API
          //coordenadas.push(coordenada_map)//Guardo o valor dos objetos de coordenadas nese vetor
          Poligono_atual = poligonos_salvos[poligono_selecionado]//Pego a referência do poligono que desejo inserir a vértice
          Poligono_atual.getPath().push(coordenada_map);//Aqui eu atribuo uma nova vértice criada pelo click do mouse
          document.getElementById("Lat"+identificador_input).addEventListener('change', Modificando_vertice_input);//Adiciono o evento pro input criado poder alterar essa vértice em específico
          document.getElementById("Lng"+identificador_input).addEventListener('change', Modificando_vertice_input);
          document.getElementById("Excluir"+identificador_input).addEventListener('click', ExcluirVertice);
          marker.addListener('position_changed', Modificando_vertice_marker);
          poligono_criado["poligono"+(poligono_selecionado+1)].push(coordenada_map);
        }
        else{
          alert("Limite de vértices atingido!")
        }
      }
    function Modificando_vertice_input(){
        var input_latitude = parseFloat(document.getElementById("Lat"+focado).value);
        var input_longitude = parseFloat(document.getElementById("Lng"+focado).value);
        var nova_coordenada_map = new google.maps.LatLng(input_latitude, input_longitude);
        var Poligono_atual = poligonos_salvos[poligono_selecionado];
        Poligono_atual.getPath().setAt(focado-1, nova_coordenada_map); //Altero o valor da vértice do poligono atual
        poligono_criado["poligono"+(poligono_selecionado+1)][focado-1] = nova_coordenada_map;
        markers[focado-1].setMap(null);//desabilita o marker da posição atual
        marker = new google.maps.Marker({
          title: "Vértice: "+focado.toString(),
          position: nova_coordenada_map,
          map: map,
          icon: "../static/green_marker.png",
          draggable: true
        });
        marker.addListener('position_changed', Modificando_vertice_marker);//Pra cada objeto marker criado é adicionado o evento que possibilita ele de alterar o vértice por quem ele é responsável
        markers[focado-1] = marker;
        markers[focado-1].setMap(map);//habilita a nova posição dele
    }
    function Modificando_vertice_marker(event){
        var indice = this.title.replace("Vértice: ","");
        var latitude_input = document.getElementById("Lat"+indice);
        var longitude_input = document.getElementById("Lng"+indice);

        latitude_input.value = this.position["lat"]().toString();
        longitude_input.value = this.position["lng"]().toString();

        var nova_coordenada_map = new google.maps.LatLng(parseFloat(latitude_input.value),parseFloat(longitude_input.value));
        poligonos_salvos[poligono_selecionado].getPath().setAt((indice-1), nova_coordenada_map);
        poligono_criado["poligono"+(poligono_selecionado+1)][indice-1] = nova_coordenada_map;
    }
    function CriarVerticesButton(){
        if(contador>0){
          contador -= 1
          document.getElementById("contador").innerHTML = "Vértices disponíveis: "+contador;
          var latitude_input = document.getElementById("Latitude")
          var longitude_input = document.getElementById("Longitude")
          if(latitude_input.value && longitude_input.value != null){
            setCriarVertice(latitude_input.value,longitude_input.value) 
            var nova_coordenada_map = new google.maps.LatLng(parseFloat(latitude_input.value),parseFloat(longitude_input.value));
            console.log(nova_coordenada_map)
            poligonos_salvos[poligono_selecionado].getPath().push(nova_coordenada_map)
            var marker = new google.maps.Marker({
              title: "Vértice: "+identificador_input,
              position: nova_coordenada_map,
              map: map,
              icon: "../static/green_marker.png",
              draggable: true
            });
            markers.push(marker);
            markers[markers.length-1].setMap(map);
            markers[markers.length-1].addListener('position_changed', Modificando_vertice_marker);
            document.getElementById("Lat"+identificador_input).addEventListener('change', Modificando_vertice_input);
            document.getElementById("Lng"+identificador_input).addEventListener('change', Modificando_vertice_input);
            document.getElementById("Excluir"+identificador_input).addEventListener('click', ExcluirVertice);
            poligono_criado["poligono"+(poligono_selecionado+1)].push(nova_coordenada_map)
          }
          else{
            alert("Insira um valor válido de latitude e longitude.")
          }
        }
        else{
          alert("Limite de vértices atingido!")
        }
    }
    function ExcluirVertice(){
        var indice = this.id.replace("Excluir","")
        var Input_para_excluir = document.getElementById("input_vertice"+indice)
        var Input_pai = document.getElementById("input_vertices")
        var Poligono_atual = poligonos_salvos[poligono_selecionado]
        contador += 1;
        identificador_input -= 1;
        document.getElementById("contador").innerHTML = "Vértices disponíveis: "+contador;

        Input_pai.removeChild(Input_para_excluir);
        indice = parseInt(indice)
        markers[indice-1].setMap(null);
        markers.splice(indice-1,1);
        Poligono_atual.getPath().removeAt(indice-1);
        for (x=0;x<(markers.length);x++){
          //renomeando título de todos os markers
          markers[x].setMap(null)
          markers[x].title = "Vértice: "+(x+1).toString()
          markers[x].setMap(map)

          //renomeando id de todos os inputs e spans
          if((x+1)>=indice){
            var span_formatado = document.getElementById("span"+(x+2).toString())
            var input_lat = document.getElementById("Lat"+(x+2).toString())
            var input_lng = document.getElementById("Lng"+(x+2).toString())
            var div_inputs = document.getElementById("input_vertice"+(x+2).toString())
            var button_id = document.getElementById("Excluir"+(x+2).toString())

            span_formatado.innerHTML = (x+1).toString()+"ª. "+"Vértice"
            span_formatado.id = "span"+(x+1).toString()
            input_lat.id = "Lat"+(x+1).toString()
            input_lng.id = "Lng"+(x+1).toString()
            input_lat.setAttribute("onfocus",`Mudando_valores_poligono(${x+1})`);
            input_lng.setAttribute("onfocus",`Mudando_valores_poligono(${x+1})`);
            div_inputs.id = "input_vertice"+(x+1).toString()   
            button_id.id = "Excluir"+(x+1)
          }
        }
        poligono_criado["poligono"+(poligono_selecionado+1)].splice(indice-1,1);
    }
    function Plotar_novo_poligono(){
        if(poligono_criado["poligono"+(poligono_selecionado+1)].length > 2){
          if(numero_poligonos_criados.innerHTML == poligonos_salvos.length){
            for(botoes=0; botoes<poligonos_salvos.length; botoes++){
                document.getElementById("Poligono "+(botoes+1)).className = "dropdown-item";
            }
          }
          var Input_pai = document.getElementById("input_vertices")
          var div_buttons_poligonos = document.getElementById("div_buttons_poligonos")
          for (var excluir=1;excluir<=identificador_input; excluir++){
            var Input_para_excluir = document.getElementById("input_vertice"+excluir)
            Input_pai.removeChild(Input_para_excluir);
          }
          if(numero_poligonos_criados.innerHTML < poligonos_salvos.length){
            CriarBotaoRefPoligono()
            for(botoes=0; botoes<poligonos_salvos.length; botoes++){
                document.getElementById("Poligono "+(botoes+1)).className = "dropdown-item";
            }
          }
          contador = 99
          identificador_input = 0
          markers = []
          poligono_selecionado = (poligonos_salvos.length-1)
          poligono_selecionado += 1;
          editando = false
          initMap(); 
        }
        else{
          alert("Seu polígono deve ter ao menos 3 vértices para criar um novo.")
        }
    }
    function selecionar_poligono(){
        
        var Input_pai = document.getElementById("input_vertices")
        var div_buttons_poligonos = document.getElementById("div_buttons_poligonos")
        for (var excluir=1;excluir<=identificador_input; excluir++){
          var Input_para_excluir = document.getElementById("input_vertice"+excluir)
          Input_pai.removeChild(Input_para_excluir);
        }
        if(numero_poligonos_criados.innerHTML < poligonos_salvos.length){
          CriarBotaoRefPoligono()
        }
        contador = 99
        identificador_input = 0
        editando = true
        poligono_selecionado = parseInt(this.id.replace("Poligono ",""))-1
        markers = []
        initMap()
        
    }
    function CriarBotaoRefPoligono(){
        function QuandoEstaSobre(){
          if(this.className != "dropdown-item active"){
            this.className = "dropdown-item bg-primary"
          }
   
        }
        function QuandoSai(){
          if(this.className != "dropdown-item active"){
            this.className = "dropdown-item"
          }     
        }
        function QuandoClicado(){
          for(botoes=0; botoes<poligonos_salvos.length; botoes++){
            document.getElementById("Poligono "+(botoes+1)).className = "dropdown-item";
          }
          if(this.className != "dropdown-item active"){
            this.className = "dropdown-item active"
          }
          
        }
        numero_poligonos_criados.innerHTML = poligonos_salvos.length
        var botao_poligono = document.createElement("button")
        var texto_button = document.createTextNode("Poligono "+poligonos_salvos.length)
        botao_poligono.appendChild(texto_button)
        botao_poligono.className = "dropdown-item active"
        botao_poligono.id = "Poligono "+poligonos_salvos.length
        botao_poligono.addEventListener('click',selecionar_poligono)
        botao_poligono.addEventListener('mouseover', QuandoEstaSobre) 
        botao_poligono.addEventListener("mouseout", QuandoSai);   
        botao_poligono.addEventListener('click', QuandoClicado)
        div_buttons_poligonos.appendChild(botao_poligono)  
     
        document.getElementById("contador").innerHTML = "Vértices disponíveis: "+contador;
    }
    function Poligono_Escolhido(){
        var poligono_editando = poligono_criado["poligono"+(poligono_selecionado+1)]
        poligonos_salvos[plotar_poligono].fillColor = "#FF0000";
        poligonos_salvos[plotar_poligono].setMap(map)
        for(var indice=0; indice<poligono_editando.length; indice++){ //Aqui ele vai pegar o objeto do polígono que ele tá editando, nesse objeto é salvo todas as coordenadas de todas as vértices.
          contador -= 1
          document.getElementById("contador").innerHTML = "Vértices disponíveis: "+contador;
          var marker = new google.maps.Marker({ //Pra cada vértice é criado um marker, como se estivesse sendo criado um novo polígono
            title: "Vértice: "+(indice+1),
            position:  poligono_editando[indice],
            map: map,
            icon: "../static/green_marker.png",
            draggable: true
          });
          //E tudo isso aqui embaixo é atribuição de eventos para os markers de cada vértice e pra cada input criado novamente.
          markers.push(marker);
          var marker_latitude = marker.position["lat"]().toString()
          var marker_longitude = marker.position["lng"]().toString()
          setCriarVertice(marker_latitude,marker_longitude)
          document.getElementById("Excluir"+(indice+1)).addEventListener('click', ExcluirVertice);
          document.getElementById("Lat"+(indice+1)).addEventListener('change', Modificando_vertice_input);//Adiciono o evento pro input criado poder alterar essa vértice em específico
          document.getElementById("Lng"+(indice+1)).addEventListener('change', Modificando_vertice_input);
          markers[markers.length-1].addListener('position_changed', Modificando_vertice_marker)
          markers[markers.length-1].setMap(map)
        }
    }
    function SalvarVertices(){
      var enviando_formatado = "{"
      var valores = []
      var contador = 0
      for(var soldado in poligono_criado){
        contador++
        enviando_formatado += `'${soldado}': [`
        for(var bala of poligono_criado[soldado]){

          valores.push(`{'lat': ${bala["lat"]().toString()}, 'lng': ${bala["lng"]().toString()}}`)
        }
        if(contador == Object.keys(poligono_criado).length){
          enviando_formatado += valores+"]"
        }
        else{
          enviando_formatado += valores+"],"
        }
        valores = []
      }
      enviando_formatado += "}"
      document.getElementById("vert").value =  enviando_formatado
      console.log(enviando_formatado)
      if(numero_poligonos_criados.innerHTML < poligonos_salvos.length){
        CriarBotaoRefPoligono()
      }
      alert("Coordenadas salvas")
  }
