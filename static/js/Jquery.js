$(
    function(){
      $(".thead").mousemove(function(){
        $(".thead").click(function(){
          var id = this.id.replace("thead","tbody");
          var id2 = this.id.replace("thead","tr");
          this.className = "thead_visivel"
          $("#"+id+":hidden").show("fast")
          $("#"+id2).show();
        });
        $(".thead_visivel").click(function(){
          this.className = "thead"
          var id = this.id.replace("thead","tbody");
          var id2 = this.id.replace("thead","tr");
          $("#"+id+":visible").hide("fast")
          $("#"+id2).hide();
        });
      })

    }
);