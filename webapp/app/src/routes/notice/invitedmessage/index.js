'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'invitedmessage',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/notice/invitedmessage').default);
    });
  },
  onEnter: checkStatus,
};