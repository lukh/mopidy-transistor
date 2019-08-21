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

  