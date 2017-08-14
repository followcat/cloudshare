'use strict';

module.exports = {
  path: 'createaccount',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/create-account').default);
    });
  },
};