'use strict';

const callbackFunction = (callback, json) => {
  if (callback && typeof callback === 'function') {
    callback(json);
  }
};

export { callbackFunction };
