'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'notice',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/notice').default);
    });
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/notice/invitemessage').default);
      }, 'invitemessage');
    }
  },
  onEnter: checkStatus,
  childRoutes: [
    require('./invitemessage'),
  ]
};