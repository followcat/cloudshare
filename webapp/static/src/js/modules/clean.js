(function() {
  'use strict';
  var timestamp = '2016-11-18 00:00:00';

  function removeHistoryStorage() {
    var storage = localStorage.getItem('history') && JSON.parse(localStorage.getItem('history'));
    if (storage) {
      var length = storage.length;
      var lastItem = storage[length - 1];
      if (new Date(timestamp) > new Date(lastItem.time)) {
        localStorage.removeItem('history');
      }
    }
  }

  removeHistoryStorage();
}());