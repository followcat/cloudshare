'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'users',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/manage/users').default);
    });
  },
  onEnter: checkStatus
};