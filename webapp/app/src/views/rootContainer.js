'use strict';
import React, { Component } from 'react';
import { Router, browserHistory } from 'react-router';

import StorageUtil from 'utils/storage';

import 'components/global.less';

import { isMember } from 'request/member';

const promise = new Promise((resolve, reject) => {
      isMember((json) => {
        if (json.result === true) {
          global.ismember = true
        }else{
          global.ismember = false
        }
        resolve(global.ismember);
      });
  });

const rootRoute = {
  path: '/',
  // indexRoute: {
  //   path: 'hp',
  //   getComponent(nextState, callback) {
  //     require.ensure([], (require) => {
  //       callback(null, require('views/home').default);
  //     }, 'home');
  //   }
  // },
  getComponent(nextState, callback) {
    require.ensure([], (require) => {
      callback(null, require('views/App').default);
    }, 'app');
  },
  onEnter(nextState, replace) {
    let pathname = nextState.location.pathname,
        user = StorageUtil.get('user'),
        token = StorageUtil.get('token');
    if (user && token) {
      if(pathname === '/')
        promise.then((data) => {
          if(global.ismember){
            browserHistory.replace("/search");
            replace({ pathname: 'search' });
          }else{
            browserHistory.replace("/prouploader");
            replace({ pathname: 'prouploader' });
           }
        })
    } else if (pathname == '/') replace({ pathname: 'index' });
  },
  childRoutes: [
    require('routes/index'),
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
    require('routes/add-position'),
  ]
};

class rootContainer extends Component {

  componentWillUnmount() {
    console.log(global.ismember);
  }

  render() {
    return (
      <Router history={browserHistory} routes={rootRoute} {...global.ismember}/>
    );
  }
}

export default rootContainer;
