'use strict';

module.exports = {
  path: 'admin',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/management/admin').default);
    }, 'admin');
  }
};