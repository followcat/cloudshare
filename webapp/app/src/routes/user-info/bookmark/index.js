'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'bookmark',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/user-info/bookmark').default);
    });
  },
  onEnter: checkStatus
};