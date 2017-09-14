'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'notice',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/notice').default);
    });
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/notice/unreadmessage').default);
      }, 'unreadmessage');
    }
  },
  onEnter: checkStatus,
  childRoutes: [
    require('./readmessage'),
    require('./sentmessage'),
    require('./unreadmessage'),
    require('./invitedmessage'),
    require('./invitermessage'),
    require('./processedmessage'),
  ]
};