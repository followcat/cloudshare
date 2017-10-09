'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'readmessage',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/notice/readmessage').default);
    });
  },
  onEnter: checkStatus,
};