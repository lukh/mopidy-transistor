Recompile the module
install node and yarn

git clone (somewhere, whatever) mopidy.js (https://github.com/mopidy/mopidy.js)
cd mopidy.js

yarn
yarn build

cp mopidy.js/dist/* to ./

search and replace //# sourceMappingURL=/mopidy.js.map to //# sourceMappingURL=mopidy.js.map in .js file