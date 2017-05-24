'use strict';
import checkStatus from 'utils/check-status';

module.exports = {
  path: 'setting',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/manage/setting').default);
    });
  },
  onEnter: checkStatus
};
