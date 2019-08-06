var mopidy = new Mopidy();

mopidy.on("state", console.log);
mopidy.on("event", console.log);