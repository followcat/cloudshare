'use strict';

const stringToKeyValue = (str, obj) => {
  let kv = str.split('=');
  obj[kv[0]] = decodeURIComponent(kv[1]);
};

const queryString = (str) => {
  let cutStr = str.indexOf('?') > 0 ? str.slice(str.indexOf('?') + 1) : str,
      arr = [],
      obj = {};

  if (cutStr.indexOf('&') > 0) {
    arr = cutStr.split('&');
    arr.map((item) => {
      stringToKeyValue(item, obj);
    });
  } else {
    stringToKeyValue(cutStr, obj);
  }

  return obj;
};

module.exports = queryString;

