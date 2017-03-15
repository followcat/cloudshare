'use strict';

module.exports = {
  path: 'upload',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/uploader/upload').default);
    }, 'upload');
  },
  childRoutes: [
    require('./result')
  ]
};