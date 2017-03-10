'use strict';
// import { Layout, JobDescription } from 'views/ProjectManagement';

module.exports = {
  path: 'pm',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/ProjectManagement/component/Layout').default);
    }, 'layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/ProjectManagement/component/JobDescription').default);
      }, 'job-description');
    }
  },
  childRoutes: [
    require('./job-description'),
    require('./customer'),
    require('./company')
  ]
};