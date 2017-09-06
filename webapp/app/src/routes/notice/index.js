'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'notice',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/notice').default);
    });
  },
  onEnter: checkStatus,
    childRoutes: [
    require('./invitemessage'),
  ]
};