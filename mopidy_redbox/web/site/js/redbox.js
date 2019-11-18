var mopidy = new Mopidy();
var event_source = new EventSource('/transistor/events');

// Utilities
function el(id) {
   return document.getElementById(id);
 }
 
 function hide(selector) {
   document.querySelectorAll(selector).forEach(e => {
     e.hidden = true;
   });
 }
 
 function show(selector) {
   document.querySelectorAll(selector).forEach(e => {
     e.hidden = false;
   });
 }


/* Toggle between adding and removing the "responsive" class to topnav when the user clicks on the icon */
function toggleMenu() {
  var x = el("menu");
  if (x.className === "sidebar") {
    x.className += " responsive";
  } else {
    x.className = "sidebar";
  }
}

function toggleFooter() {
  var x = el("footer_id");
  var toggle = el("toggle-footer");
  if (x.className === "footer") {
    x.className += " responsive";
    toggle.className = "fas fa-minus-circle";
  } else {
    x.className = "footer";
    toggle.className = "fas fa-plus-circle";
  }
}


// Events Hook - Mopidy
mopidy.on("state:online", function () {
   mopidy.playback.getState().then(updatePlaybackState);
   mopidy.playback.getCurrentTrack().then(updateCurrentTrack);
 
   el("play").onclick = () => mopidy.playback.play();
   el("pause").onclick = () => mopidy.playback.pause();
   el("previous").onclick = () => mopidy.playback.previous();
   el("next").onclick = () => mopidy.playback.next();
 
   el("repeat").onclick = () =>
     mopidy.tracklist
       .getRepeat()
       .then(state => mopidy.tracklist.setRepeat([!state]));
   el("random").onclick = () =>
     mopidy.tracklist
       .getRandom()
       .then(state => mopidy.tracklist.setRandom([!state]));
   el("single").onclick = () =>
     mopidy.tracklist
       .getSingle()
       .then(state => mopidy.tracklist.setSingle([!state]));
   el("consume").onclick = () =>
     mopidy.tracklist
       .getConsume()
       .then(state => mopidy.tracklist.setConsume([!state]));

    var volumeElement = el("volume")
    volumeElement.onchange = () => {
        var vol = parseInt(volumeElement.value);
        mopidy.mixer.setVolume([vol]);
    }
    mopidy.mixer.getVolume().then((vol) => {
      volumeElement.value = vol;
    });
});

mopidy.on("state:offline", () => {
  hide(".online-only");
  show(".offline-only");
});

mopidy.on("event:playbackStateChanged", ({ new_state }) => {
  updatePlaybackState(new_state);
});

mopidy.on("event:trackPlaybackStarted", ({ tl_track }) => {
  updateCurrentTrack(tl_track.track);
});

mopidy.on("event:trackPlaybackStopped", () => {
  updatePlaybackState("stopped");
});

mopidy.on("event:trackPlaybackPaused", ({ time_position }) => {
  updatePlaybackState("paused", time_position);
});

mopidy.on("event:trackPlaybackResumed", () => {});

mopidy.on("event:streamTitleChanged", ( title ) => {
   el("current-track").innerText = title.title;   
});

mopidy.on('event:volumeChanged', function(event) {
  el("volume").value = event.volume;
});



// Tools
// function updateCover(trackUri, images) {
//    const [image] = images[trackUri];
//    el("cover").setAttribute("src", image.uri);
//    el("cover").setAttribute("height", image.height);
//    el("cover").setAttribute("width", image.width);
//  }
 

 function updateCurrentTrack(track=null) {
   if(track != null){
      const artists = track.artists.map(a => a.name).join(", ");
      let albumName = track.album.name;
      if (track.album.date) {
         albumName = `${albumName} (${track.album.date})`;
      }

      el("current-artist").innerText = artists;
      el("current-album").innerText = albumName;
      el("current-track").innerText = track.name;

      // mopidy.library
      //    .getImages([[track.uri]])
      //    .then(result => updateCover(track.uri, result));
   }
 }


 function updatePlaybackState(state, timePosition) {
  if (timePosition) {
    el("playback-state").innerText = `${state} at ${timePosition / 1000}s`;
  } else {
    el("playback-state").innerText = state;
  }

  switch (state) {
    case "playing":
      el("play").hidden = true;
      el("pause").hidden = false;
      break;
    case "paused":
    case "stopped":
      el("play").hidden = false;
      el("pause").hidden = true;
      break;
    default:
  }
}


event_source.onmessage = function(message) {
  data = JSON.parse(message.data);

  // tuner position
  if(data.hasOwnProperty('tuner_position')){
    tuner_position = el("tuner-position");
    tuner_position.value = data.tuner_position;
  }

  // tuner labels
  if(data.hasOwnProperty('tuner_labels')){
    tuner_labels = el("tuner-labels");
    tuner_labels.innerHTML = '';

    for (var label_position in data.tuner_labels){
      var label_name = data.tuner_labels[label_position];

      var label = document.createElement('span');
      label.innerText = label_name;
      label.className = "tuner-label";
      label.style.left = label_position.toString(10) + '%';

      tuner_labels.appendChild(label);
    }
  }

  if(data.hasOwnProperty('time')){
    time_label = el("time");
    time_label.innerText = data.time;
  }

  if(data.hasOwnProperty('date')){
    date_label = el("date");
    date_label.innerText = data.date;
  }

  if(data.hasOwnProperty('battery_soc')){
    bat_gauge = el("battery_level");
    bat_gauge.style.width = data.battery_soc.toString() + "%";
  }
};