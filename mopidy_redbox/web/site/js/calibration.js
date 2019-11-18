var ws = new WebSocket("ws://localhost:6680/redbox/calibsocket");
// ws.onopen = function() {
//};

ws.onmessage = function (evt) {
   //  alert(evt.data);
   document.getElementById("calib_information").innerText = evt.data;
};

function calibration_step() {
   ws.send("next_step");
}