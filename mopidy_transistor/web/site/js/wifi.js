function deleteSSID(ssid){
    entry = el("delete-"+ssid);
    entry.style.width = "100px";
    var form = document.createElement("form");
    form.setAttribute('method',"post");
    form.setAttribute('action',"wifi");

    var i = document.createElement("button"); //input element, text
    i.setAttribute('type',"submit");
    i.setAttribute('name',"del_ssid");
    i.setAttribute('value', ssid);
    i.innerText = "Delete";
    form.appendChild(i);

    entry.appendChild(form);
}