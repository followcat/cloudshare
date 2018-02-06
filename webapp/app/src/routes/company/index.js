'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'company/:companyId',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/company').default);
    });
  },
  onEnter: checkStatus
};
