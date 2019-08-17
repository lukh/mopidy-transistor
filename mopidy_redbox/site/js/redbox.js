var mopidy = new Mopidy();

mopidy.on("state", console.log);
mopidy.on("event", console.log);


mopidy.on("state:online", function () {
    console.log("Hellow You, in the Main")
    // // Set buttons depending on state playing or paused/stopped
    // mopidy.playback.getState().done(function(state) {
    //    toggleButtons(state);
    // });
 
    // // Update track information
    // mopidy.playback.getCurrentTrack().done(function(track) {
    //    if (track) {
    //       updateCurrentTrack(track);
    //    }
    // });
 
    //  // Update track position
    //  mopidy.playback.getTimePosition().done(function(timePosition) {
    //      setTrackPosition(timePosition);
    //  });
 
    // // Update volume position
    // mopidy.playback.getVolume().done(function(volume) {
    //    setVolumeUi(volume);
    // });
 });


 function el(id) {
    return document.getElementById(id);
  }