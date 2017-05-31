'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'manage',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/manage').default);
    });
  },
  onEnter(nextState, replace) {
    checkStatus();
    if (nextState.location.pathname === `/${this.path}`) {
      replace({ pathname: '/manage/users' });
    }
  },
  childRoutes: [
    require('./users'),
    require('./setting')
  ]
};