'use strict';

module.exports = {
  path: 'docmining',
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/doc-mining').default);
      }, 'doc-mining');
    }
  }
};
