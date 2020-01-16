function SearchLocalitys (coordinate, array_localitys){
    Geo = new google.maps.Geocoder()
    Geo.geocode({'location': coordinate}, 
    function(a){
        a.forEach(function(element, index, array){
            var country = null
            var state = null
            var county = null
            var locality = null
            element.address_components.forEach(function(element, index, array){
                if (element["types"][0] == "country"){
                    country = element["long_name"]
                }
                if (element["types"][0] == "administrative_area_level_1"){
                    state = element["long_name"]
                }
                if (element["types"][0] == "administrative_area_level_2"){
                    county = element["long_name"]
                }
                if (element["types"][0] == "route"){
                    locality = element["long_name"]
                }
            })
            var new_locality = new Localitys(country, state, county, locality)
            array_localitys.push(new_locality)
        })
    })
}