'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'result',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/prouploader/result').default);
    }, 'upload-result');
  },
  onEnter: checkStatus
};