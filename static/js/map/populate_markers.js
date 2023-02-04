'use strict';
function populateMarkers(url,type,data,datatype, map, markerClusterer,bounds, markers,infowindow){
  /*
  url : the url link for ajax Call
  type: method post or get
  data: a dict {},
  datatype: xml or json,
  markerCluster instance,
  bounds: Googlemaps instance,
  markers: array,
  infowindow: google maps InfoWindow
  */
  $(".spinner-border").show();
  return $.ajax({
      url: url,
      type: type,
      data: data,
      datatype: datatype,
      success: function(data)
      {
        $('.spinner-border').hide();
        if(data.features.length <1){
          $( ".spinner-border" ).hide();
          $( "#res" ).show();
        }
        else{
          $('.spinner-border').hide();
          $('#res').hide();
        }
        markerClusterer.minimumClusterSize = data.features.length;
        for (let i = 0; i < data.features.length; i++){
          let marker = new google.maps.Marker({
              position: new google.maps.LatLng(data.features[i].geometry.coordinates[1],data.features[i].geometry.coordinates[0]),
              map: map

            });
           let latlng = new google.maps.LatLng(data.features[i].geometry.coordinates[1],data.features[i].geometry.coordinates[0])
           bounds.extend(latlng);
           markers.push(marker);
           google.maps.event.addListener(marker, 'click', (function(marker, i) {
             return function() {
               infowindow.setContent("Name:"+data.features[i].properties.name+"</br>"+"Category :"+data.features[i].properties.category+ '</br><a href="/p/' + data.features[i].properties.pk + "/" + data.features[i].properties.name.replace(" ", "-") + ".html" +'">Detail</a></div>');
               infowindow.open(map, marker);
             }
           })(marker, i));
         }
         map.fitBounds(bounds);
         markerClusterer.addMarkers(markers);
         markerClusterer.fitMapToMarkers();
      }
  });
}
