function openSection(pageName, elmnt){
    // Hide all elements with class="tabcontent" by default */
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("settings-tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].className = "settings-tabcontent";
    }
    content = el(pageName).className = "settings-tabcontent active";


    // Remove the background color of all tablinks/buttons
    tablinks = document.getElementsByClassName("settings-tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = "settings-tablink";
    }
    // Add the specific color to the button used to open the tab content
    elmnt.className = "settings-tablink active";
}

function onUploadBackup(){
    // el('file_backup_upload').removeEventListener("change")
    el('file_backup_upload').addEventListener('change', submitForm);
    function submitForm() {
        el('form_upload_backup').submit();
    }

    el('file_backup_upload').click();
}


