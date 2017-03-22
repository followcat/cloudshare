'use strict';

module.exports = {
  path: 'userInfo',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/user-info').default);
    });
  },
  childRoutes: [
    require('./history'),
    require('./bookmark'),
    require('./setting')
  ]
};