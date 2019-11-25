var ws = new WebSocket("ws://localhost:6680/transistor/updatesocket");

ws.onmessage = function (evt) {
   el("update_informations").innerText = el("update_informations").innerText + '\n' + evt.data;
};

function update_system() {
   ws.send("update_system");
}

function update_mopidy() {
    ws.send("update_mopidy");
}
