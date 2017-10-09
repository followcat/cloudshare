'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'processedmessage',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/notice/processedmessage').default);
    });
  },
  onEnter: checkStatus,
};