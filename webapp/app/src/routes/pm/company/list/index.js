'use strict';

module.exports = {
  path: 'list',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/pm/company/list').default);
    }, 'company-list');
  }
};