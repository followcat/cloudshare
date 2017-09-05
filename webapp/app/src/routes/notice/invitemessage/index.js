'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'invitemessage',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/notice/invitemessage').default);
    });
  },
  onEnter: checkStatus,
};