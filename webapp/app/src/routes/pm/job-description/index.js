'use strict';
// import { JobDescription } from 'views/ProjectManagement';

module.exports = {
  path: 'jobdescription',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/ProjectManagement/component/JobDescription').default);
    }, 'job-description');
  }
};