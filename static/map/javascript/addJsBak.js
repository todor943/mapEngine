// console.log(csrftoken);
var mapX;
var mapY;
var mapCenter;

var distance = 1000; // 2km
var eventTimeout = 10 * 1000; // 10s
var initTimeout = 1000; // 1s
var running = false;
var options = {
  enableHighAccuracy: true,
  maximumAge: 5000
};
var eventMarkerList = {};

var playerRadius = false;
var playerPosition = false;
var eventFetcher = null;
var locationFetcher = null;
var locationFetcher = null;
var mapOptions = {
  disableDefaultUI: true,
  center: {lat: 50.7880386, lng: 1.074141},
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

var map;
var player = false;

window.onload = initMap;

function playerPositionToMarker(position) {
    var googleLocation = {lat : position.coords.latitude, lng: position.coords.longitude}
    var marker = new google.maps.Marker({
        position: googleLocation,
        map: map,
        title: 'Click to zoom'
    });
    return marker;
}

function eventToMarker(eventData) {
    var googleLocation = {lat : eventData.locLat, lng: eventData.locLong}
    var marker = new google.maps.Marker({
        position: googleLocation,
        map: map,
        title: 'Click to zoom'
    });
    marker.eventUuid = eventData.uuid
    // console.log(marker);
    return marker;
}

function initMap() {
    map = new google.maps.Map(
      document.getElementById('map'),
      mapOptions
    );


    // var eventFetcher = setInterval(fetchEvents, eventTimeout);
    var locationFetcher = navigator.geolocation.getCurrentPosition(handlePosition, handleError);
    var locationFetcher = navigator.geolocation.watchPosition(handlePosition, handleError, options);
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
    recenterMap(position);
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


function fetchEvents() {
    var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
          handleResult(xhttp.responseText)
        }
      }

    xhttp.open("POST", "http://127.0.0.1:8000" + document.eventApiLocation, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send("jsonData=" + JSON.stringify({
        position : {
            lat : playerPosition.coords.latitude,
            lng : playerPosition.coords.longitude,
            acc : playerPosition.coords.accuracy,
            heading : playerPosition.coords.heading
        },
        time : playerPosition.timestamp,
        radius : distance
    }));
}

function handleResult(result) {
    var data = JSON.parse(result);
    console.log(data.features);
    // if(defined(data.features)) {
    //     console.log('defined');
    // }
    // else {
    //
    // }
    // if(data.success == true) {
        // for (var i = 0; i < data.length; i++) {
        //
        //     data[i].fields.uuid = data[i].pk;
        //     addEventToMap(data[i].fields);
        //     console.log(data[i].fields);
        // }
    // console.log(data);
    // }
}


function addEventToMap(eventData) {
    if (eventData.uuid in eventMarkerList) {

    }
    else {
        var marker = eventToMarker(eventData);
        eventMarkerList[eventData.uuid] = marker;
        console.log(marker);
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
