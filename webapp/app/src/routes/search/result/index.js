'use strict';
module.exports = {
  path: 'result',
  getComponent(location, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/Search/component/SearchResult').default);
    }, 'search-result');
  }
};