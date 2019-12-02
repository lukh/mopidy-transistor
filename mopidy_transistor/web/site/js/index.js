
function updateTrackList(){
    const printTracks = tracks => {
        var tableRef = el('tracklist').getElementsByTagName('tbody')[0];
        while ( tableRef.rows.length > 0 ) { tableRef.deleteRow(0); }

        // list
        for (t_id in tracks){
            track = tracks[t_id];

            var newRow = tableRef.insertRow();

            var cellName  = newRow.insertCell(0);
            var nameText  = document.createTextNode(track.name);
            cellName.appendChild(nameText);
        }

    }
    const failureHandler = () => {
        console.warn("Something went wrong");
    }

    mopidy.tracklist.getTracks().then(printTracks, failureHandler);
}

mopidy.on("state:online", function () {
    updateTrackList();
});

mopidy.on("event:tracklistChanged", function () {
    updateTrackList();
});