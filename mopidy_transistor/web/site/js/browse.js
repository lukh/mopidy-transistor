
var browseStack = [];

function browseTracks(uri_base=null) {
    const printTracks = tracks => {
        // // header
        var headerRef = el("browse-header");

        // Table
        var tableRef = el('browse').getElementsByTagName('tbody')[0];
        while ( tableRef.rows.length > 0 ) { tableRef.deleteRow(0); }
        // Back function
        if(browseStack.length > 0){
            var newRow = tableRef.insertRow();
            newRow.id = browseStack.length > 1 ? browseStack[browseStack.length - 1] : null;

            var cellType  = newRow.insertCell(0);
            var typeDiv = document.createElement("div");
            typeDiv.innerHTML = '<i class="fas fa-arrow-circle-up"></i>';
            newRow.onclick = function(newRow){
                return function() {
                    browseStack.pop();

                    var hrefs = headerRef.getElementsByClassName("browse-header-entry")
                    headerRef.removeChild(hrefs[hrefs.length - 1]);

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
            if(track.type == "directory" || track.type == "album"){
                newRow.id = track.uri;
                newRow.onclick = function(newRow){
                    return function() { 
                        browseStack.push(uri_base);

                        href = document.createElement("i");
                        href.className = "browse-header-entry fas fa-chevron-right";
                        href.innerHTML = newRow.cells[1].innerText;
                        headerRef.appendChild(href);

                        browseTracks(newRow.id);
                    };
                }(newRow);
            }
            // cell 0
            var cellType  = newRow.insertCell(0);
            var typeDiv = document.createElement("div");
            if(track.type == "directory" || track.type == "album"){
                typeDiv.innerHTML = track.type == "directory" ? '<i class="fas fa-folder"></i>' : '<i class="fas fa-compact-disc"></i>';
            }
            else if(track.type == "track"){
                typeDiv.innerHTML = '<i class="fas fa-play-circle"></i>';
                typeDiv.id = track.uri;
                typeDiv.onclick = function(typeDiv){
                    return function() {
                        mopidy.tracklist.clear();
                        mopidy.tracklist.add({uris:[typeDiv.id]});
                        mopidy.playback.play();
                    };
                }(typeDiv);
            }
            cellType.appendChild(typeDiv);

            // cell 1
            var cellName  = newRow.insertCell(1);
            var nameText  = document.createTextNode(track.name);
            cellName.appendChild(nameText);

            // cell 2
            if(track.type == "track"){
                var cellAdd  = newRow.insertCell(2);
                var addDiv = document.createElement("div");
                addDiv.innerHTML = '<i class="fas fa-plus-circle"></i>';
                addDiv.id = track.uri;
                addDiv.onclick = function(addDiv){
                    return function() {
                        mopidy.tracklist.add({uris:[addDiv.id]});
                    };
                }(typeDiv);
                cellAdd.appendChild(addDiv);
            }

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



