'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'unreadmessage',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/notice/unreadmessage').default);
    });
  },
  onEnter: checkStatus,
};