'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'result',
  getComponent(location, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/job-search/result').default);
    }, 'search-result');
  },
  onEnter: checkStatus
};