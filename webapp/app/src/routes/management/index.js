'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'management',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/management').default);
    });
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/management/list-menber').default);
      }, 'management');
    }
  },
  onEnter: checkStatus,
  childRoutes: [
    require('./project-list'),
    require('./list-menber'),
    require('./admin'),
  ]
};