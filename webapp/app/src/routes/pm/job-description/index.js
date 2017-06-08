'use strict';

module.exports = {
  path: 'jobdescription',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/pm/job-description').default);
    }, 'job-description');
  }
};