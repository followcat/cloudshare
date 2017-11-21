'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'fastmatching',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/layout/Layout').default);
    }, 'common-layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/fast-matching').default);
      }, 'fast-matching');
    }
  },
  onEnter: checkStatus
};