'use strict';
// import { UploaderResult } from 'views/Uploader';

module.exports = {
  path: 'result',
  getComponent(location, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/Uploader/component/UploaderResult').default);
    }, 'uploader-result');
  }
};