function ComponentHTML(){

}
ComponentHTML.prototype.createInputGroup = function(lat, lng, index, append, eventInput, eventButton){
    this.super_div = document.createElement('div');
    this.children_div = document.createElement('div');
    this.span = document.createElement('span');
    this.text_span  = document.createTextNode(index+"ª. "+"Vértice");
    this.input_1 = document.createElement('input');
    this.input_2 = document.createElement('input');
    this.div_button_children = document.createElement('div');
    this.button_delete = document.createElement('button');
    this.text_button =  document.createTextNode("Excluir");  
    
    this.super_div.className = "input-group";
    this.super_div.id = "input_vertice"+index;
    
    this.children_div.className = "input-group-prepend";
    this.super_div.appendChild(this.children_div);
  
    
    this.span.className = "input-group-text";
    this.span.id = "span"+index;
    this.children_div.appendChild(this.span);
  
    
    this.span.appendChild(this.text_span);
  
    
    this.input_1.type = "text";
    this.input_1.className = "form-control";
    this.input_1.placeholder = "Latitude";
    this.input_1.id = "Lat"+index;
    this.super_div.appendChild(this.input_1);
    this.input_1.value = lat;
    this.input_1.addEventListener("change", eventInput);
  
    
    this.input_2.type = "text";
    this.input_2.className = "form-control";
    this.input_2.placeholder = "Longitude";
    this.input_2.id = "Lng"+index;        
    this.super_div.appendChild(this.input_2);
    this.input_2.value = lng;
    this.input_2.addEventListener("change", eventInput);
  
    
    this.div_button_children.className = "input-group-append";
    this.super_div.appendChild(this.div_button_children);
  
    
    this.button_delete.addEventListener("click", eventButton);
    this.button_delete.className = "btn btn-danger";
    this.button_delete.id = "Excluir"+index;
    
    this.button_delete.appendChild(this.text_button);
    this.div_button_children.appendChild(this.button_delete);
  
    this.super_div.style = "margin-bottom: 10px;"
    append.appendChild(this.super_div);
}
ComponentHTML.prototype.createOption = function(value, text, select){
    new_option = document.createElement("option");
    new_option.value = value
    new_option.innerHTML = text
    select.appendChild(new_option);
}
ComponentHTML.prototype.getSuperDiv = function(){
    return this.super_div
}
ComponentHTML.prototype.getInputLat = function(){
    return this.input_1
}
ComponentHTML.prototype.getInputLng = function(){
    return this.input_2
}
ComponentHTML.prototype.getDeleteButton = function(){
    return this.button_delete
}
ComponentHTML.prototype.getSpan = function(){
    return this.span
}
ComponentHTML.prototype.setInputLat = function(lat){
    this.input_1.value = lat
}
ComponentHTML.prototype.setInputLng = function(lng){
    this.input_2.value = lng
}
ComponentHTML.prototype.setIDSuperDiv = function(id){
    this.super_div.id = id
}
ComponentHTML.prototype.setIDInputLat = function(id){
    this.input_1.id = id
}
ComponentHTML.prototype.setIDInputLng = function(id){
    this.input_2.id = id
}
ComponentHTML.prototype.setIDButton = function(id){
    this.button_delete.id = id
}
ComponentHTML.prototype.setIDSpan = function(id){
    this.span.id = id
}
ComponentHTML.prototype.setTextSpan = function(text){
    this.span.removeChild(this.text_span)
    this.text_span = document.createTextNode(text);
    this.span.appendChild(this.text_span)
}
ComponentHTML.prototype.createHeaderTable = function (indice){
    this.indice = indice
    this.tabela = document.getElementById("tabela")
    //Criando o cabeçario da tabela
    this.thead = document.createElement("thead")
    this.tr_titulo_tabela = document.createElement("tr")
    this.th_titulo = document.createElement("th")
    this.texto_th_titulo;
    //Criando o corpo da tabela
    this.tbody = document.createElement("tbody")
    //Define a cor de fundo do título
    this.thead.className = "thead-light";
  
    //Título principal
    this.th_titulo.style = "text-align: center"
    this.th_titulo.setAttribute("colspan",4)
    this.th_titulo.className = "thead"
    this.texto_th_titulo = document.createElement("button")
    this.texto_th_titulo.innerHTML = "Lista de Markers dentro do Poligono "+indice
    this.texto_th_titulo.setAttribute("class","btn btn-link")
    this.th_titulo.appendChild(this.texto_th_titulo)
    this.th_titulo.setAttribute("data-toggle","collapse")
    this.th_titulo.setAttribute("data-target",".tab_poligono"+indice)
    this.th_titulo.setAttribute("aria-expanded","false")
    this.th_titulo.setAttribute("aria-controls","tbody_poligono"+indice)
    this.tr_titulo_tabela.appendChild(this.th_titulo)
    this.thead.appendChild(this.tr_titulo_tabela)
  
    //Identificando o body para inserir os dados de cada poligono individualmente
    this.tbody.id = "tbody_poligono"+indice
    this.thead.id = "thead_poligono"+indice
    this.tbody.setAttribute("class","collapse tab_poligono"+indice)
  
    //Anexado o cabeçario e o corpo na tabela
    this.tabela.appendChild(this.thead)
    this.tabela.appendChild(this.tbody)
}
ComponentHTML.prototype.createBodyTable = function (latitude, longitude, indice, contador){
    //Criando os dados de cada tabela referente aos poligonos
  
    if(contador==1){
        this.tr_titulos = document.createElement("tr")
        this.th_indice = document.createElement("th")
        this.th_nome = document.createElement("th")
        this.th_latitude = document.createElement("th")
        this.th_longitude = document.createElement("th")
    
        //Títulos de cada coluna
        this.th_indice.setAttribute("scope","col")
        this.th_indice.innerHTML = "#"
        this.th_nome.setAttribute("scope","col")
        this.th_nome.innerHTML = "Nome Científico"
        this.th_latitude.setAttribute("scope","col")
        this.th_latitude.innerHTML = "Latitude"
        this.th_longitude.setAttribute("scope","col")
        this.th_longitude.innerHTML = "Longitude"
        //Anexando todos eles a coluna principal
        this.tr_titulos.appendChild(this.th_indice)
        this.tr_titulos.appendChild(th_nome)
        this.tr_titulos.appendChild(this.th_latitude)
        this.tr_titulos.appendChild(this.th_longitude)
        this.tr_titulos.id = "tr_poligono"+indice
        this.tr_titulos.setAttribute("class","collapse tab_poligono"+indice)
        //anexando ao cabeçário da tabela
        this.thead.append(this.tr_titulos)
      }
      this.linha = document.createElement("tr")
      this.indice_coluna = document.createElement("th")
      indice_coluna.innerHTML = contador
      this.nome_coluna = document.createElement("td")
      this.latitude_coluna = document.createElement("td")
      this.longitude_coluna = document.createElement("td")
      linha.appendChild(indice_coluna)
      linha.appendChild(nome_coluna)
      linha.appendChild(latitude_coluna)
      linha.appendChild(longitude_coluna)
      this.tbody.appendChild(linha)
      latitude_coluna.innerHTML = latitude
      longitude_coluna.innerHTML = longitude
  }