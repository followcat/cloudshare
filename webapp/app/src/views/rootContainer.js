'use strict';
import React, { Component } from 'react';
import { Router, browserHistory } from 'react-router';

import StorageUtil from 'utils/storage';

import 'components/global.less';

import { isMember } from 'request/member';

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
      if(global.ismember){
        replace({ pathname: 'search' });
      }else{
        replace({ pathname: 'jobsearch' });
      }
    }
  },
  childRoutes: [
    require('routes/search'),
    require('routes/uploader'),
    require('routes/prouploader'),
    require('routes/become-member'),
    require('routes/pm'),
    require('routes/fast-matching'),
    require('routes/doc-mining'),
    require('routes/cvdoc-mining'),
    require('routes/cvsdoc-mining'),
    require('routes/doc-mining-cv'),
    require('routes/user-info'),
    require('routes/notice'),
    require('routes/management'),
    require('routes/resume'),
    require('routes/upload-preview'),
    require('routes/go-to-signin'),
    require('routes/agreement'),
    require('routes/job-search'),
    require('routes/best-excellent'),
    require('routes/company'),
  ]
};

class rootContainer extends Component {

  render() {
    return (
      <Router history={browserHistory} routes={rootRoute} />
    );
  }
}

export default rootContainer;
