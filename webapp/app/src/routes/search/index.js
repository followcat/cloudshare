'use strict';
// import Layout from 'views/common/Layout';
// import { Search } from 'views/Search';

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
        callback(null, require('views/Search/component/Search').default);
      }, 'search');
    }
  },
  childRoutes: [
    require('./result')
  ]
};