'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'uploader',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/layout/Layout').default);
    }, 'layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/uploader/upload').default);
      }, 'upload');
    }
  },
  onEnter: checkStatus,
  childRoutes: [
    require('./upload')
  ]
};