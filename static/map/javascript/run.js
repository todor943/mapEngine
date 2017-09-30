var distance = 1000; // 2km
var eventTimeout = 10 * 1000; // 10s
var persistTimeout = 1000;

var options = {
  enableHighAccuracy: true,
  maximumAge: 5000
};
var eventMarkerList = {};
var player = false;
var playerRadius = false;
var playerPosition = false;
var eventFetcher = null;
var locationFetcher = null;
var locationFetcher = null;

var map;
var mapOptions = {
  disableDefaultUI: true,
  center: {lat: 0, lng: 0},
  zoom: 14,

};
// var recentering = true;
var userOptions = null;

window.onload = initMap;

function playerPositionToMarker(position) {
    var googleLocation = {lat : position.coords.latitude, lng: position.coords.longitude}
    var marker = new google.maps.Marker({
        position: googleLocation,
        map: map,
        title: 'PLAYER_LOCATION'
    });
    return marker;
}

function addSliderControl(map) {
    var controlDiv = document.createElement('div');
    controlDiv.id = 'slider';
    map.controls[google.maps.ControlPosition.RIGHT_CENTER].push(controlDiv);
    noUiSlider.create(controlDiv, {
        start: [ 200 ],
        range: {
            'min': [  50 ],
            'max': [ 3000 ]
        },
        connect: 'lower',
        orientation: 'vertical',
        direction : 'ltr'
    });
    controlDiv.noUiSlider.on('change', updatePlayerRadius);
    controlDiv.noUiSlider.on('update', updatePlayerRadius);
}

function initMap() {
    map = new google.maps.Map(
      document.getElementById('map'),
      mapOptions);
    playerRadius = new google.maps.Circle({
        strokeColor: '#0000FF',
        strokeOpacity: 0.8,
        strokeWeight: 1,
        fillColor: '#0000FF',
        fillOpacity: 0.15,
        map: map,
        radius: distance
    });

    addSliderControl(map);

    map.addListener('zoom_changed', captureMapState);
    map.addListener('center_changed', captureMapState);

    var eventFetcher = setInterval(fetchEvents, eventTimeout);
    var persister = setInterval(persistMapState, persistTimeout)
    var locationFetcher = navigator.geolocation.getCurrentPosition(handlePosition, handleError);
    var locationFetcher = navigator.geolocation.watchPosition(handlePosition, handleError, options);
}

function captureMapState() {
    userOptions = {
        zoom : map.getZoom(),
        center : {
            lat : map.getCenter().lat(),
            lng : map.getCenter().lng()
        }
    };
}

function persistMapState() {
    if(typeof(Storage) !== "undefined") {
        sessionStorage.setItem("userOptions", JSON.stringify(userOptions));
    } else {
        console.log("// Sorry! No Web Storage support..");
    }
    // console.log(sessionStorage.getItem("key"));
    // console.log(JSON.parse(sessionStorage.getItem("userOptions")));
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

// Convert Degress to Radians
function deg2rad( deg ) {
  return deg * Math.PI / 180;
}

// main
function handlePosition(position) {
    if(player == false) {
        updatePlayer(position);
        fetchEvents();
    }
    else {
        updatePlayer(position);
    }
    // recenterMap(position);
    updatePlayerCircle();
    // if(recentering) {
        recenterMap(position);
    // }
    captureMapState();
}

function updatePlayer(position) {
    if(player != false) {
        player.setMap(null);
    }
    player = playerPositionToMarker(position);
    playerPosition = position;
}

function recenterMap(position) {
    map.setCenter({lat : position.coords.latitude, lng: position.coords.longitude})
}

function updatePlayerRadius(values, handle, unencoded, tap, positions) {

    distance = parseFloat(values[0]);
    console.log(distance);
    // updatePlayerCircle();
    playerRadius.setRadius(distance);
}

function updatePlayerCircle() {
    if(playerRadius != false){
        playerRadius.bindTo('center', player, 'position');

    }
}

function handleError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            console.log("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            console.log("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            console.log("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            console.log("An unknown error occurred.");
            break;
    }
}


function clearFarEvents() {

}

function fetchEvents() {
    var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
          handleResult(xhttp.responseText)
        }
      }

    xhttp.open("POST", document.eventApiLocation, true);
    // xhttp.open("POST", "http://127.0.0.1:8000" + document.eventApiLocation, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send("jsonData=" + JSON.stringify(
        {
            position : {
                lat : playerPosition.coords.latitude,
                lng : playerPosition.coords.longitude
            },
            mapOptions : userOptions,
            radius : distance
        }));
}

function handleResult(result) {
    var data = JSON.parse(result);
    if(data.features && data.features.length > 0) {
        for (var i = 0; i < data.features.length; i++) {
            addEventToMap(data.features[i]);
        }
    }
}


function addEventToMap(feature) {
        var marker = eventToMarker(feature);
        eventMarkerList[feature.properties.uuid] = marker;
}

function eventToMarker(eventData) {
    var googleLocation = {lat : eventData.geometry.coordinates[1], lng: eventData.geometry.coordinates[0]}
    var marker = new google.maps.Marker({
        position: googleLocation,
        map: map,
        title: eventData.properties.entityName,
    });
    // var infowindow = new google.maps.InfoWindow({
    //     content: '<p>' + eventData.properties.entityDescription + '</p>'
    // });
    // marker.addListener('click', function() {
    //     infowindow.open(map, marker);
    // });
    marker.eventUuid = eventData.properties.uuid
    return marker;
}

function detectBrowser() {
  var useragent = navigator.userAgent;
  var mapdiv = document.getElementById("map");

  if (useragent.indexOf('iPhone') != -1 || useragent.indexOf('Android') != -1 ) {
    mapdiv.style.width = '100%';
    mapdiv.style.height = '100%';
  } else {
    // mapdiv.style.width = '600px';
    mapdiv.style.height = '100%';
  }
}
