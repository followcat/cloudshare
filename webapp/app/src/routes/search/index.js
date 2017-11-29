'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'search',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/layout/Layout').default);
    }, 'layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/search/search').default);
      }, 'search');
    }
  },
  onEnter(nextState, replace) {
    checkStatus();
    if (nextState.location.pathname === `/${this.path}`) {
      // replace({ pathname: '/jobsearch' });
    }
  },
  childRoutes: [
    require('./result')
  ]
};