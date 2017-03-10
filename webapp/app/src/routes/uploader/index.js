'use strict';

module.exports = {
  path: 'uploader',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/common/Layout').default);
    }, 'common-layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/Uploader/component/Uploader').default);
      }, 'uploader');
    }
  },
  childRoutes: [
    require('./result')
  ]
};