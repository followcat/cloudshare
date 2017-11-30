'use strict';

module.exports = {
  path: 'index',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/index').default);
    }, 'index');
  },
};