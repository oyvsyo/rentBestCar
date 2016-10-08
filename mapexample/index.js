var map;


function initMap(id) {
    map = L.map(id);
    L.tileLayer('https://api.mapbox.com/styles/v1/stassavchuk93/ciolhd2bi003n22nirqv95n09/tiles/{z}/{x}/{y}?access_token=pk.eyJ1Ijoic3Rhc3NhdmNodWs5MyIsImEiOiJjaW9saDdvd3QwMDF3dmxseTkyZzVlN295In0.espQjLLdlsjhvPIkNspGPw', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,

        id: 'ciolhd2bi003n22nirqv95n09',
        accessToken: 'pk.eyJ1Ijoic3Rhc3NhdmNodWs5MyIsImEiOiJjaW9saDdvd3QwMDF3dmxseTkyZzVlN295In0.espQjLLdlsjhvPIkNspGPw'
    }).addTo(map);

    map.setView([51.5, 0.1], 12);

}

$(document).ready(function() {
    initMap('mapid');
});