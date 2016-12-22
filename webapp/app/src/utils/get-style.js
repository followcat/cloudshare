'use strict';

const getStyle = (el, prop) => {
  return el.currentStyle ?
      el.currentStyle[prop] :
      window.getComputedStyle(el, null)[prop];
};

module.exports = getStyle;
