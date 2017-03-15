'use strict';

module.exports = {
  path: 'uploader',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/common/Layout').default);
    }, 'layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/uploader/upload').default);
      }, 'upload');
    }
  },
  childRoutes: [
    require('./upload')
  ]
};