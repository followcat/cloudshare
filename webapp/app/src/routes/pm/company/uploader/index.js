'use strict';
// import { CompanyUploader } from 'views/ProjectManagement';

module.exports = {
  path: 'uploader',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/ProjectManagement/component/CompanyUploader').default);
    }, 'company-uploader');
  }
};