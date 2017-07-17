'use strict';

module.exports = {
  path: 'cvsdocmining',
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/cvsdoc-mining').default);
      }, 'cvsdoc-mining');
    }
  }
};
