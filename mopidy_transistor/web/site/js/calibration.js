var loc = window.location, ws_uri;
ws_uri = "ws:";
ws_uri += "//" + loc.host;
ws_uri += "/transistor/calibsocket";

var ws = new WebSocket(ws_uri);
// ws.onopen = function() {
//};

ws.onmessage = function (evt) {
   //  alert(evt.data);
   el("calib_information").innerHTML = el("calib_information").innerHTML + '<br>' + evt.data;
};

function calibration_step() {
   ws.send("next_step");
}