'use strict';
// import { Member } from 'views/ProjectManagement';

module.exports = {
  path: 'member',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/pm/member').default);
    }, 'member');
  }
};