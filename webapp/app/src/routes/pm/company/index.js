'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'company',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/pm/company').default);
    }, 'company');
  },
  childRoutes: [
    require('./list'),
    require('./uploader')
  ],
  onEnter: checkStatus
};