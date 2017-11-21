'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'invitermessage',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/notice/invitermessage').default);
    });
  },
  onEnter: checkStatus,
};