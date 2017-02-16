'use strict';
const path = require('path'),
      fs = require('fs'),
      folderPath = require('./folder-path');


const getEntryFile = function() {

  let entryPath = path.resolve(folderPath.PATHS.SRC_PATH, 'entry'),
      dirs = fs.readdirSync(entryPath),
      matchs = [], files = {};

  dirs.forEach(function(item) {
    matchs = item.match(/(.+)\.entry\.js$/);
    if (matchs) {
      files[matchs[1]] = path.resolve(folderPath.PATHS.SRC_PATH, 'entry', item);
    }
  });

  return files;
};

module.exports = getEntryFile;
