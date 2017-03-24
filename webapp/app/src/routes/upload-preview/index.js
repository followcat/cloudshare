'use strict';

module.exports = {
  path: 'preview',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/common/Layout').default);
    });
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/upload-preview').default);
      });
    }
  }
};
