function openPage(pageName, elmnt, color) {
    // Hide all elements with class="tabcontent" by default */
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("radios-tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].className = "radios-tabcontent";
    }
    el(pageName).className = "radios-tabcontent active";


    // Remove the background color of all tablinks/buttons
    tablinks = document.getElementsByClassName("radios-tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = "radios-tablink";
    }
    // Add the specific color to the button used to open the tab content
    elmnt.className = "radios-tablink active";

    // update value of add radio button
    el("radios-addradio-button").setAttribute("value", pageName); 

    //hide add radio form
    el("radios-addradio").style.display = "none";
}

function addBank() {
    var bankList = el("radios-banks");
    newBankDiv = document.createElement("div");

    var form = document.createElement("form");
    form.setAttribute('method',"post");
    form.setAttribute('action',"radios");

    var i = document.createElement("input"); //input element, text
    i.setAttribute('type',"text");
    i.setAttribute('name',"new_bank");
    form.appendChild(i);

    newBankDiv.appendChild(form);

    newBankDiv.className = "radios-new-bank";
    bankList.appendChild(newBankDiv);
}

function deleteBank(bank) {
    minus = el("radio-tab-del-"+bank);
    minus.style.display = "none";

    tab = el("radios-tab-" + bank);
    var form = document.createElement("form");
    form.setAttribute('method',"post");
    form.setAttribute('action',"radios");

    var i = document.createElement("button"); //input element, text
    i.setAttribute('type',"submit");
    i.setAttribute('name',"del_bank");
    i.setAttribute('value', bank);
    i.innerText = "Delete";
    form.appendChild(i);

    tab.appendChild(form);
}

function addRadio() {
    form = el("radios-addradio");
    button = el("radios-addradio-show");
    if(form.style.display != "block"){
        form.style.display = "block";
        button.className = "fas fa-minus-circle";
    }
    else{
        form.style.display = "none";
        button.className = "fas fa-plus-circle";
    }
}

function deleteRadio(bank, radio_index) {
    entry = el("delete-"+bank+"-"+radio_index);
    entry.style.width = "100px";
    var form = document.createElement("form");
    form.setAttribute('method',"post");
    form.setAttribute('action',"radios");

    var i = document.createElement("input"); //input element, text
    i.setAttribute('type',"text");
    i.setAttribute('name',"del_radio_bank");
    i.setAttribute('value', bank);
    i.innerText = "";
    i.style.display = "none";
    form.appendChild(i);

    var i = document.createElement("button"); //input element, text
    i.setAttribute('type',"submit");
    i.setAttribute('name',"del_radio_radio");
    i.setAttribute('value', radio_index);
    i.innerText = "Delete";
    form.appendChild(i);

    entry.appendChild(form);

}

function updateRadio(bank, id, radio, position, url) {
    form = el("radios-modifyradio");
    form.style.display = "block";

    form.elements["id"].value = id;
    form.elements["position"].value = position;
    form.elements["name"].value = radio;
    form.elements["url"].value = url;
    form.elements["modify_radio_bank"].value = bank;
}
    