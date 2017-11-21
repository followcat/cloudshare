'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'becomemember',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/layout/Layout').default);
    }, 'common-layout');
  },
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/become-member').default);
      }, 'become-member');
    }
  },
  onEnter: checkStatus,
};