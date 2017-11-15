'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'upload',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/prouploader/upload').default);
    }, 'upload');
  },
  onEnter: checkStatus,
  childRoutes: [
    require('./result')
  ]
};