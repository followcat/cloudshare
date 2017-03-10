'use strict';
// import { Company } from 'views/ProjectManagement';

module.exports = {
  path: 'company',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/ProjectManagement/component/Company').default);
    }, 'company');
  },
  childRoutes: [
    require('./list'),
    require('./uploader')
  ]
};