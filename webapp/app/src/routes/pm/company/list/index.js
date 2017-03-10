'use strict';
// import { CompanyList } from 'views/ProjectManagement';

module.exports = {
  path: 'list',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/ProjectManagement/component/CompanyList').default);
    }, 'company-list');
  }
};