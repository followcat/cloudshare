'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'resume/:resumeId',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/resume').default);
    });
  },
  onEnter: checkStatus
};
