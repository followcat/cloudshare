'use strict';

const StorageUtil = {
  get: (name) => {
    let reg = /^\[.+\]$/g,
        value = localStorage.getItem(name) || sessionStorage.getItem(name);
    return reg.test(value) ? JSON.parse(value) : value;
  },

  set: (name, value) => {
    let storageValue = value instanceof Object ? JSON.stringify(value) : value;
    localStorage.setItem(name, storageValue);
  },

  setAll: (object) => {
    for (let key in object) {
      let value = object[key] instanceof Object ? JSON.stringify(object[key]) : object[key];
      localStorage.setItem(key, object[key]);
    }
  },

  unset: (name) => {
    localStorage.removeItem(name);
  },

  unsetAll: (nameList) => {
    for (let name of nameList) {
      localStorage.removeItem(name);
    }
  },
};

module.exports = StorageUtil;
