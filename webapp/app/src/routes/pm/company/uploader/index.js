'use strict';

module.exports = {
  path: 'uploader',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/pm/company/uploader').default);
    }, 'company-uploader');
  }
};