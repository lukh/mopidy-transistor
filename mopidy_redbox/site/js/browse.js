
// By clearing tracklist, a random one will be added and played
function browse_directory() {
    console.log("COUCOUC")
 };


function browseTracks() {
    const printTracks = tracks => {
        var tableRef = document.getElementById('browse').getElementsByTagName('tbody')[0];
        for (t_id in tracks){
            track = tracks[t_id];
            console.log(track);


            // Insert a row in the table at the last row
            var newRow   = tableRef.insertRow();
            
            var cellType  = newRow.insertCell(0);
            var typeDiv = document.createElement("div");
            if(track.type == "directory"){
                typeDiv.innerHTML = '<i class="browse-directory far fa-folder" onclick="browse_directory()></i>';
            }
            else if(track.type == "track"){
                typeDiv.innerHTML = '<i class="browse-track fas fa-play-circle"></i>';
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
  
    mopidy.library.browse(["redbox:radios:AM"]).then(printTracks, failureHandler);
  }

mopidy.on("state:online", function () {
    console.log("Hellow You, in the Browse");

    browseTracks();
});


