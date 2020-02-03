function ComponentHTML(){

}
ComponentHTML.prototype.createInputGroup = function(lat, lng, index, append, eventInput, eventButton){
    this.super_div = document.createElement('div');
    this.children_div = document.createElement('div');
    this.span = document.createElement('span');
    this.text_span  = document.createTextNode((index+1)+"ª. "+"Vértice");
    this.input_1 = document.createElement('input');
    this.input_2 = document.createElement('input');
    this.div_button_children = document.createElement('div');
    this.button_delete = document.createElement('button');
    this.text_button =  document.createTextNode("Excluir");  
    
    this.super_div.className = "input-group";
    this.super_div.id = "input_vertex"+index;
    
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
    this.button_delete.id = "Delete"+index;
    
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
ComponentHTML.prototype.setValueInputLat = function(lat){
    this.input_1.value = lat
}
ComponentHTML.prototype.setValueInputLng = function(lng){
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
ComponentHTML.prototype.createHeaderTable = function (title, index, color){
    this.count = 0
    this.index = index
    this.table = document.getElementById("table")
    //Criando o cabeçario da table
    this.thead = document.createElement("thead")
    this.tr_title_table = document.createElement("tr")
    this.th_title = document.createElement("th")
    this.texto_th_title;
    //Criando o corpo da table
    this.tbody = document.createElement("tbody")
    //Define a cor de fundo do título
    this.thead.className = "thead-light";
  
    //Título principal
    this.th_title.style = "text-align: center"
    this.th_title.setAttribute("colspan", 8)
    this.th_title.className = "thead"
    this.texto_th_title = document.createElement("button")
    this.texto_th_title.innerHTML = title
    color===undefined ? null : this.texto_th_title.style = `color: ${color};`
    this.texto_th_title.setAttribute("class","btn btn-link")
    this.th_title.appendChild(this.texto_th_title)
    this.th_title.setAttribute("data-toggle","collapse")
    this.th_title.setAttribute("data-target",".tab_polygon"+index)
    this.th_title.setAttribute("aria-expanded","false")
    this.th_title.setAttribute("aria-controls","tbody_polygon"+index)
    this.tr_title_table.appendChild(this.th_title)
    this.thead.appendChild(this.tr_title_table)
  
    //Identificando o body para inserir os dados de cada polygon individualmente
    this.tbody.id = "tbody_polygon"+index
    this.thead.id = "thead_polygon"+index
    this.tbody.setAttribute("class","collapse tab_polygon"+index)
  
    //Anexado o cabeçario e o corpo na table
    this.table.appendChild(this.thead)
    this.table.appendChild(this.tbody)
}
ComponentHTML.prototype.createBodyTable = function (name, country, state, county, latitude, longitude, index, wrong, func){
    this.count++
    this.row = document.createElement("tr")
    this.column_index = document.createElement("th")
    this.column_name = document.createElement("td")
    this.column_country = document.createElement("td")
    this.column_state = document.createElement("td")
    this.column_county = document.createElement("td")
    this.column_latitude = document.createElement("td")
    this.column_longitude = document.createElement("td")
    this.column_index_row = document.createElement("td")

    this.row.appendChild(this.column_index)
    this.row.appendChild(this.column_name)
    this.row.appendChild(this.column_country)
    this.row.appendChild(this.column_state)
    this.row.appendChild(this.column_county)
    this.row.appendChild(this.column_latitude)
    this.row.appendChild(this.column_longitude)
    this.row.appendChild(this.column_index_row)
    this.tbody.appendChild(this.row)

    this.column_index.innerHTML = this.count
    this.column_name.innerHTML = name
    this.column_country.innerHTML = country
    this.column_state.innerHTML = state
    this.column_county.innerHTML = county
    this.column_latitude.innerHTML = latitude
    this.column_longitude.innerHTML = longitude
    this.column_index_row.innerHTML = index

    this.column_country.className = "country"
    this.column_state.className = "state"
    this.column_county.className = "county"
    this.column_latitude.className = "latitude"
    this.column_longitude.className = "longitude"

    this.column_country.id = "country"+this.count
    this.column_state.id = "state"+this.count
    this.column_county.id = "county"+this.count
    this.column_latitude.id = "latitude"+this.count
    this.column_longitude.id = "longitude"+this.count
    if(wrong===true){

        this.column_country.setAttribute("data-target","#exampleModal")
        this.column_country.setAttribute("data-toggle","modal")
        this.column_country.style = "color: red" 
        this.column_country.addEventListener("click", func)

        this.column_state.setAttribute("data-target","#exampleModal")
        this.column_state.setAttribute("data-toggle","modal")
        this.column_state.style = "color: red" 
        this.column_state.addEventListener("click", func)
        
        this.column_county.setAttribute("data-target","#exampleModal")
        this.column_county.setAttribute("data-toggle","modal")
        this.column_county.style = "color: red" 
        this.column_county.addEventListener("click", func)

        this.column_latitude.setAttribute("data-target","#exampleModal")
        this.column_latitude.setAttribute("data-toggle","modal")
        this.column_latitude.style = "color: red" 
        this.column_latitude.addEventListener("click", func)

        this.column_longitude.setAttribute("data-target","#exampleModal")
        this.column_longitude.setAttribute("data-toggle","modal")
        this.column_longitude.style = "color: red" 
        this.column_longitude.addEventListener("click", func)

    }

}
ComponentHTML.prototype.createTitleTable = function (){
    //Criando os dados de cada table referente aos polygons
    this.tr_titles = document.createElement("tr")
    this.th_index = document.createElement("th")
    this.th_name = document.createElement("th")
    this.th_country = document.createElement("th")
    this.th_state = document.createElement("th")
    this.th_county = document.createElement("th")
    this.th_latitude = document.createElement("th")
    this.th_longitude = document.createElement("th")
    this.th_index_row = document.createElement("th")

    //Títulos de cada coluna
    this.th_index.setAttribute("scope","col")
    this.th_index.innerHTML = "#"
    this.th_name.setAttribute("scope","col")
    this.th_name.innerHTML = "Nome Científico"
    this.th_country.setAttribute("scope","col")
    this.th_country.innerHTML = "País"
    this.th_state.setAttribute("scope","col")
    this.th_state.innerHTML = "Estado"
    this.th_county.setAttribute("scope","col")
    this.th_county.innerHTML = "Município"
    this.th_latitude.setAttribute("scope","col")
    this.th_latitude.innerHTML = "Latitude"
    this.th_longitude.setAttribute("scope","col")
    this.th_longitude.innerHTML = "Longitude"
    this.th_index_row.setAttribute("scope","col")
    this.th_index_row.innerHTML = "Linha"

    //Anexando todos eles a coluna principal
    this.tr_titles.appendChild(this.th_index)
    this.tr_titles.appendChild(this.th_name)
    this.tr_titles.appendChild(this.th_country)
    this.tr_titles.appendChild(this.th_state)
    this.tr_titles.appendChild(this.th_county)
    this.tr_titles.appendChild(this.th_latitude)
    this.tr_titles.appendChild(this.th_longitude)
    this.tr_titles.appendChild(this.th_index_row)
    this.tr_titles.id = "tr_polygon"+this.index
    this.tr_titles.setAttribute("class","collapse tab_polygon"+this.index)
    //anexando ao cabeçário da table
    this.thead.append(this.tr_titles)
  }