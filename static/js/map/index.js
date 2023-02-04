'use strict';



(function(w,d,$){
    $(d).ready(function(){
      $(".spinner-border").hide();
        let infoWindow = new google.maps.InfoWindow();
        let markers = [];
        let bounds = new google.maps.LatLngBounds();
        let mcOptions = {maxZoom: 15};
          let mapOptions = {
          center: new google.maps.LatLng(37.950902,23.641103),
          zoom: 12,
          mapTypeId: google.maps.MapTypeId.ROADMAP
    
        };
        let map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
        
        function clearFeaturesData(){
            if(map.data){
              map.data.forEach(function (feature) {
                map.data.remove(feature);
              });
            }
        }
        function processPoints(geometry, callback, thisArg) {
            if (geometry instanceof google.maps.LatLng) {
              callback.call(thisArg, geometry);
            } else if (geometry instanceof google.maps.Data.Point) {
              callback.call(thisArg, geometry.get());
            } else {
              geometry.getArray().forEach(function(g) {
                processPoints(g, callback, thisArg);
              });
            }
          }
          map.data.addListener('addfeature', function(e) {
            var bounds = new google.maps.LatLngBounds();
            processPoints(e.feature.getGeometry(), bounds.extend, bounds);
            map.fitBounds(bounds);
          });

          let height = $(".content").height();
          $('#map-canvas').height(height);



        $("body").on("click", '.point', function(e){
            e.preventDefault();
            let id = $(this).data("id");
            $.when($.ajax({
                url: $(this).data("url"),
                method: 'GET',
                datatype: 'json',
                data: { id: id },
                beforeSend: function(){
                   $(".spinner-border").show();
                 },
                 complete: function(){
                   $(".spinner-border").hide();
                 },
              })).then(function( resp, textStatus, jqXHR ) {
                clearFeaturesData();
                let data = JSON.parse(resp);
                console.info(data);
                map.data.addGeoJson(data);
                let distance = $('.container').offset().top - 80;
                $('html,body').animate({scrollTop:distance},100);

              });
            return false


        })



    }) /* document ready */



})(window,document,jQuery)