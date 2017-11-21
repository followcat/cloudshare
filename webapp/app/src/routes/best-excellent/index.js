'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'excellent',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/layout/Layout').default);
    }, 'common-layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/best-excellent').default);
      }, 'best-excellent');
    }
  },
  onEnter: checkStatus
};