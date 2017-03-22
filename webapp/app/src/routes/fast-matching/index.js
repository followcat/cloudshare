'use strict';

module.exports = {
  path: 'fastmatching',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/common/Layout').default);
    }, 'common-layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/fast-matching').default);
      }, 'fast-matching');
    }
  }
};