'use strict';

module.exports = {
  path: 'projectlist',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/pm/project-list').default);
    }, 'project-list');
  }
};