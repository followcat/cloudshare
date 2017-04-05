'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'history',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/user-info/history').default);
    });
  },
  onEnter: checkStatus
};