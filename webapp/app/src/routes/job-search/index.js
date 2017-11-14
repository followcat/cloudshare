'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'jobsearch',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/layout/Layout').default);
    }, 'layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/job-search/search').default);
      }, 'search');
    }
  },
  onEnter: checkStatus,
  childRoutes: [
    require('./result')
  ]
};