'use strict';

module.exports = {
  path: 'docminingcv/:resumeId',
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/doc-mining-cv').default);
      }, 'doc-mining-cv');
    }
  }
};