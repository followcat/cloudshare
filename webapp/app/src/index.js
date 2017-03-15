'use strict';
import React from 'react';
import ReactDOM from 'react-dom';
import { Router, browserHistory } from 'react-router';

import 'babel-polyfill';

const rootRoute = {
  path: '/',
  indexRoute: {
    getComponent(nextState, callback) {
      require.ensure([], (require) => {
        callback(null, require('views/index').default);
      }, 'index');
    }
  },
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/App').default);
    }, 'app');
  },
  childRoutes: [
    require('./routes/search'),
    require('./routes/uploader'),
    require('./routes/pm'),
    require('./routes/fast-matching')
  ]
};

ReactDOM.render(
  <Router history={browserHistory} routes={rootRoute} />,
  document.getElementById('root')
);
