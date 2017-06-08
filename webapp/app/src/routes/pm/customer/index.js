'use strict';
// import { Customer } from 'views/ProjectManagement';

module.exports = {
  path: 'customer',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/pm/customer').default);
    }, 'customer');
  }
};