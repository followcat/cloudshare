'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'prouploader',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/layout/Layout').default);
    }, 'layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/prouploader/upload').default);
      }, 'upload');
    }
  },
  onEnter: checkStatus,
  childRoutes: [
    require('./upload')
  ]
};