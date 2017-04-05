'use strict';
import React from 'react';
import ReactDOM from 'react-dom';
import { Router, browserHistory } from 'react-router';

import 'components/global.less';

import 'babel-polyfill';

import StorageUtil from 'utils/storage';

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
  onEnter(nextState, replace) {
    let pathname = nextState.location.pathname,
        user = StorageUtil.get('user'),
        token = StorageUtil.get('token');

    if (pathname === '/' && user && token) {
      replace({ pathname: 'search' });
    }
  },
  childRoutes: [
    require('./routes/search'),
    require('./routes/uploader'),
    require('./routes/pm'),
    require('./routes/fast-matching'),
    require('./routes/user-info'),
    require('./routes/resume'),
    require('./routes/upload-preview'),
    require('./routes/go-to-signin')
  ]
};

ReactDOM.render(
  <Router history={browserHistory} routes={rootRoute} />,
  document.getElementById('root')
);
