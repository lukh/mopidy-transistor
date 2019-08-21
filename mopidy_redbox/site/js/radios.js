function openPage(pageName, elmnt, color) {
    // Hide all elements with class="tabcontent" by default */
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("radios-tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].className = "radios-tabcontent";
    }
    document.getElementById(pageName).className = "radios-tabcontent active";


    // Remove the background color of all tablinks/buttons
    tablinks = document.getElementsByClassName("radios-tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = "radios-tablink";
    }
    // Add the specific color to the button used to open the tab content
    elmnt.className = "radios-tablink active";
}

function addBank() {
    var bankList = document.getElementById("radios-banks");
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

  