'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'addposition',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/layout/Layout').default);
    }, 'layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/add-position').default);
      }, 'addposition');
    }
  },
  onEnter: checkStatus,
  childRoutes: [
    require('./upload')
  ]
};