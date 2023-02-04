'use strict';
(function(w,d,$){
  $(d).ready(function(){
    $(".spinner-border").hide();
    let mapOptions = {
      center: new google.maps.LatLng(37.950902,23.641103),
      zoom: 12,
      mapTypeId: google.maps.MapTypeId.ROADMAP

    };
    let vertices = null;
    let map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
    let infoWindow = new google.maps.InfoWindow();
    let markers = [];
    let bounds = new google.maps.LatLngBounds();
    let mcOptions = {maxZoom: 15};
    let markerClusterer = new MarkerClusterer(map, markers, mcOptions);
    $('#loading, #res').hide();
    $('#error').hide();
    $('#result').hide();
    let shape_coordinates = [];
    let Ar = [];
    let options = {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0
    };
    let loadForm = function() {
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        data: data,
        dataType: 'json',
        beforeSend: function () {
          $("#category-modal").modal("show");
        },
        success: function (data) {
          $("#category-modal .modal-content").html(data.html_form);
        }
      });
    };
    let saveForm = function() {
      let form = $(this);
      if (markers.length > 0){
        markers.length = 0;
      }
      if(map.data){
    		map.data.forEach(function (feature) {
    			map.data.remove(feature);
    		});
    	}
      if (markerClusterer) {
        markerClusterer.clearMarkers();
      }
      $("#category-modal").modal("hide");
      shape.setOptions({ editable: false });
      google.maps.event.clearListeners(map, 'click');
      map.fitBounds(bounds);
      let m = populateMarkers('/world/get_polygon','GET',{polygon: Ar, category: $('#id_category').val()},'json', map, markerClusterer,bounds, markers,infoWindow);
      return false;
    };
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
       navigator.geolocation.getCurrentPosition(function(position) {
       let pos = {
           lat: position.coords.latitude,
           lng: position.coords.longitude
       };
       infoWindow.setPosition(pos);
       infoWindow.setContent('Location found.');
       map.setCenter(pos);
       }, function() {
           handleLocationError(true, infoWindow, map.getCenter());
           },options);
       } else {
           // Browser doesn't support Geolocation
           handleLocationError(false, infoWindow, map.getCenter());
       }
       function handleLocationError(browserHasGeolocation, infoWindow, pos) {
         infoWindow.setPosition(pos);
         infoWindow.setContent(browserHasGeolocation ?
                               'Error: The Geolocation service failed.' :
                               'Error: Your browser doesn\'t support geolocation.');
         infoWindow.open(map);
      }
    function addPoint(e) {
        shape.setMap(map);
        vertices= shape.getPath();
        vertices.push(e.latLng);
        shape_coordinates.push(e.latLng);
      }
    let shape = new google.maps.Polygon({
          editable: true,
          // strokeColor: '#F0F0F0',
          strokeOpacity: 0.8,
          strokeWeight: 1,
          // fillColor: '#F0F0F0',
          fillOpacity: 0.4
      });
    google.maps.event.addListener(map,'click',addPoint);
    $('#edit').click(function(){
        shape.setOptions({ editable: true });
        shape_coordinates.length = 0;
        vertices.length = 0;
        markers.length = 0;
        Ar.length = 0
        markerClusterer.clearMarkers();
        google.maps.event.addListener(map,'click',addPoint);
        if(map.data){
    			map.data.forEach(function (feature) {
    				map.data.remove(feature);
    			});
    		}
        if (markers.length > 0){
          markers.length = 0;
        }
        if(map.data){
          map.data.forEach(function (feature) {
            map.data.remove(feature);
          });
        }
        if (markerClusterer) {
          markerClusterer.clearMarkers();
        }
    })
    $("#polygon").click(function(e){
        $('#result').hide();
        if (markers.length > 0){
          markers.length = 0;
        }
        if(map.data){
      		map.data.forEach(function (feature) {
      			map.data.remove(feature);
      		});
      	}
        if (markerClusterer) {
          markerClusterer.clearMarkers();
        }
        let a=JSON.stringify(shape_coordinates);
        let c=JSON.parse(a);
        if (typeof vertices === "undefined"){
          alert("create a polygon to the map");
        }
        else{
          vertices.forEach(function(xy, i) {
            Ar.push(xy.lng()+" "+xy.lat());
            // point = new google.maps.LatLng(xy.lat(),xy.lng());
            // bounds.extend(point);
          });
          $.ajax({
              url: '/world/polygon_create/',
              type: 'get',
              data: {'x':Ar},
              dataType: 'json',
              beforeSend: function () {
                $("#category-modal").modal("show");
              },
              success: function (data) {
                $("#category-modal .modal-content").html(data.html_form);
              }
            });

        }

    })
    $("#category-modal").on("submit", ".js-category-create-form", saveForm);
  })
})(window,document,jQuery)
