'use strict';

module.exports = {
  path: 'listcustomer',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/pm/list-member').default);
    }, 'list-member');
  }
};