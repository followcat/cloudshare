'use strict';

module.exports = {
  path: 'goto',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/go-to-signin').default);
    }, 'go-to-signin');
  },
};