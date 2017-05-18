'use strict';

module.exports = {
  path: 'cvdocmining',
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/cvdoc-mining').default);
      }, 'cvdoc-mining');
    }
  }
};
