$(
    function(){
      $(".thead_poligono").click(function(){
        var id = this.id.replace("thead","tbody")
        $("#"+id).show()
      });
    }
);