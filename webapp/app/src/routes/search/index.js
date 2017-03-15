'use strict';

module.exports = {
  path: 'search',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/common/Layout').default);
    }, 'layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/search/search').default);
      }, 'search');
    }
  },
  childRoutes: [
    require('./result')
  ]
};