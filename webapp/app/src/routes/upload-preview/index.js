'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'preview',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/layout/Layout').default);
    });
  },
  onEnter: checkStatus,
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/upload-preview').default);
      });
    }
  }
};
