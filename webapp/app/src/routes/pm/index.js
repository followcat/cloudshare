'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'pm',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/pm/Layout').default);
    }, 'layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/pm/job-description').default);
      }, 'job-description');
    }
  },
  onEnter: checkStatus,
  childRoutes: [
    require('./job-description'),
    require('./customer'),
    require('./company'),
    require('./project-list')
  ]
};