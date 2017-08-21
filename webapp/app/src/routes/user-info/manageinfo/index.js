'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'manageinfo',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/user-info/manage-info').default);
    });
  },
  onEnter: checkStatus
};