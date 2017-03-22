'use strict';

module.exports = {
  path: 'setting',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/user-info/setting').default);
    });
  }
};