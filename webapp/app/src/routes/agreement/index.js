'use strict';

module.exports = {
  path: 'agreement',
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/agreement').default);
    }, 'agreement');
  },
};