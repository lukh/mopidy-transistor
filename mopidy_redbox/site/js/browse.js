
var browseStack = [];

function browseTracks(uri_base=null) {
    const printTracks = tracks => {
        var tableRef = document.getElementById('browse').getElementsByTagName('tbody')[0];
        while ( tableRef.rows.length > 0 ) { tableRef.deleteRow(0); }

        // Insert a row in the table at the last row
        if(browseStack.length > 0){
            var newRow = tableRef.insertRow();
            newRow.id = browseStack.length > 1 ? browseStack[browseStack.length - 1] : null;

            var cellType  = newRow.insertCell(0);
            var typeDiv = document.createElement("div");
            typeDiv.innerHTML = '...';
            newRow.onclick = function(newRow){
                return function() {
                    browseStack.pop();
                    console.log(newRow.id, "list", browseStack);
                    browseTracks(newRow.id == 'null' ? null : newRow.id);
                };
            }(newRow);
            cellType.appendChild(typeDiv);

            var cellName  = newRow.insertCell(1);
            var nameText  = document.createTextNode("Back");
            cellName.appendChild(nameText);
        }

        // list
        for (t_id in tracks){
            track = tracks[t_id];

            // Insert a row in the table at the last row
            var newRow = tableRef.insertRow();
            newRow.id = track.uri;

            var cellType  = newRow.insertCell(0);
            var typeDiv = document.createElement("div");
            if(track.type == "directory" || track.type == "album"){
                typeDiv.innerHTML = track.type == "directory" ? '<i class="far fa-folder"></i>' : '<i class="fas fa-compact-disc"></i>';
                newRow.onclick = function(newRow){
                    return function() { 
                        browseStack.push(uri_base);
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
    browseTracks();
});



