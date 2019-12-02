var ws = new WebSocket("ws://localhost:6680/transistor/updatesocket");

ws.onmessage = function (evt) {
   el("update_informations").innerText = el("update_informations").innerText + evt.data;
};

function update_mopidy() {
   ws.send("update_mopidy");
   el("update_mopidy").style.backgroundColor = "grey";
   el("update_system").style.backgroundColor = "grey";
}

function update_system() {
   ws.send("update_system");
   el("update_system").style.backgroundColor = "grey";
   el("update_mopidy").style.backgroundColor = "grey";
}
