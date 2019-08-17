function browseTracks(uri_base=null) {
    const printTracks = tracks => {
        var tableRef = document.getElementById('browse').getElementsByTagName('tbody')[0];
        while ( tableRef.rows.length > 0 )
        {
            tableRef.deleteRow(0);
        }

        // list
        for (t_id in tracks){
            track = tracks[t_id];

            // Insert a row in the table at the last row
            var newRow   = tableRef.insertRow();
            newRow.id = track.uri;


            var cellType  = newRow.insertCell(0);
            var typeDiv = document.createElement("div");
            if(track.type == "directory"){
                typeDiv.innerHTML = '<i class="far fa-folder"></i>';
                newRow.onclick = function(newRow){
                    return function() { 
                        browseTracks(newRow.id);
                    };
                }(newRow);
            }
            else if(track.type == "track"){
                typeDiv.innerHTML = '<i class="fas fa-play-circle"></i>';
            }
            cellType.appendChild(typeDiv);

            var cellName  = newRow.insertCell(1);
            var nameText  = document.createTextNode(track.name);
            cellName.appendChild(nameText);

        }
    };
  
    const failureHandler = () => {
      console.warn("Something went wrong");
    };
  
    mopidy.library.browse([uri_base]).then(printTracks, failureHandler);
  }

mopidy.on("state:online", function () {
    console.log("Hellow You, in the Browse");

    browseTracks();
});



