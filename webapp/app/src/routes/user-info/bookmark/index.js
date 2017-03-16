'use strict';

module.exports = {
  path: 'bookmark',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/user-info/bookmark').default);
    });
  }
};