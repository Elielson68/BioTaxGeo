function Point_Marker(coord, map, icon, draggable){
    google.maps.Marker.prototype.setIndex = function(index){
        this.index = index
    }
    google.maps.Marker.prototype.getIndex = function(){
        return this.index
    }
    google.maps.Marker.prototype.setLatitude = function(lat){
        this.setPosition(new google.maps.LatLng(lat, this.position["lng"]().toString()))
    }
    google.maps.Marker.prototype.setLongitude = function(lng){
        this.setPosition(new google.maps.LatLng(this.position["lat"]().toString(), lng))
    }
    google.maps.Marker.prototype.getLatitude = function(){
        return this.position["lat"]()
    }
    google.maps.Marker.prototype.getLongitude = function(){
        return this.position["lng"]()
    }
    google.maps.Marker.prototype.getPosition = function(){
        return this.position
    }

    return new google.maps.Marker({ //Pra cada vértice é criado um marker, como se estivesse sendo criado um novo polígono
        title: "Point",
        position: coord,
        map: map,
        icon:  icon===undefined ? "../static/image/green_marker.png" : icon,
        draggable: draggable===undefined ? true : draggable
      });
}