'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'sentmessage',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/notice/sentmessage').default);
    });
  },
  onEnter: checkStatus,
};