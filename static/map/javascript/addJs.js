var mapOptions = {
  disableDefaultUI: true,
  center: {lat: 0, lng: 0},
  zoom: 14,
  zoomControl: false,
  mapTypeControl: false,
  scrollwheel: false, disableDoubleClickZoom: true,
  scaleControl: false,
  streetViewControl: false,
  navigationControl: false,
  rotateControl: false,
  fullscreenControl: false,
  draggable : false
};
var userOptions = null;
if(typeof(preloadedMap)!== "undefined") {
    mapOptions.center = preloadedMap.center;
    mapOptions.zoom = preloadedMap.zoom;
}


var map;
var pin = false;

window.onload = initMap;

function initMap() {

    loadUserOptions();
    map = new google.maps.Map(
      document.getElementById('map'),
      mapOptions
    );

    pin = new google.maps.Marker({
        position: map.getCenter(),
        map: map,
        draggable:true,
        title:"Place me!"
    });

    var $formLat = $('input#id_locLat');
    var $formLng = $('input#id_locLong');

    // initial setting of the coodrdinates
    pinP = pin.getPosition();
    $formLng.val(pinP.lng());
    $formLat.val(pinP.lat());

    google.maps.event.addListener(pin, 'dragend', function(evt) {
        $formLng.val(evt.latLng.lng());
        $formLat.val(evt.latLng.lat());
    });
    google.maps.event.addListener(pin, 'drag', function(evt) {
        $formLat.val(evt.latLng.lat());
        $formLng.val(evt.latLng.lng());
    });
}

function loadUserOptions() {
    if(typeof(Storage) !== "undefined") {
        userOptions = sessionStorage.getItem("userOptions");

        if(userOptions !== null) {
            userOptions = JSON.parse(userOptions);

            mapOptions.center = userOptions.center;
            mapOptions.zoom = userOptions.zoom;
            // console.log(mapOptions);
            return true;
        }
        return false;
    }
}

function detectBrowser() {
  var useragent = navigator.userAgent;
  var mapdiv = document.getElementById("map");

  if (useragent.indexOf('iPhone') != -1 || useragent.indexOf('Android') != -1 ) {
    mapdiv.style.width = '100%';
    mapdiv.style.height = '100%';
  } else {
    mapdiv.style.height = '100%';
  }
}
