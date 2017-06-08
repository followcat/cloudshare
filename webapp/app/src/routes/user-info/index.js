'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'userInfo',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/user-info').default);
    });
  },
  onEnter: checkStatus,
  childRoutes: [
    require('./history'),
    require('./bookmark'),
    require('./setting')
  ]
};