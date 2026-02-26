var w = window.innerWidth;

// coordonnées du Consulat général de Belgique à Lubumbashi
var consulatLat = -11.66523;
var consulatLng = 27.47886;

if (w < 768) {
    var center_qud = new google.maps.LatLng(consulatLat, consulatLng); // mobile
} else {
    var center_qud = new google.maps.LatLng(consulatLat, consulatLng);
}

function initialize() {
    var myOptions = {
        zoom: 15,
        center: center_qud,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        scrollwheel: false,
        mapTypeControl: false,
        zoomControl: false,
        streetViewControl: false,
        styles: [ /* tes styles existants */ ]
    };

    var img_icon = 'img/map-marker.png';
    var map = new google.maps.Map(document.getElementById("map-canvas"), myOptions);

    var marker = new google.maps.Marker({
        map: map,
        icon: img_icon,
        position: new google.maps.LatLng(consulatLat, consulatLng)
    });

    // si tu veux une info‑window avec texte
    var infowindow = new google.maps.InfoWindow({
        content: '<strong>Institut National de Statistique</strong><br>Avenue Lufira 990, Lubumbashi'
    });

    google.maps.event.addListener(marker, "click", function() {
        infowindow.open(map, marker);
    });
}

google.maps.event.addDomListener(window, 'load', initialize);