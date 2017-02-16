'use strict';
import React from 'react';
import ReactDOM from 'react-dom';

import {
  Router,
  Route,
  IndexRoute,
  browserHistory
} from 'react-router';

import Layout from 'views/common/Layout';
import { Uploader, UploaderResult } from 'views/Uploader/index';

import 'babel-polyfill';

ReactDOM.render(
  <Router history={browserHistory}>
    <Route path="/" component={Layout}>
      <IndexRoute name="uploader" component={Uploader} />
      <Route path="uploader" component={Uploader}>
        <Route path="result" component={UploaderResult} />
      </Route>
    </Route>
  </Router>,
  document.getElementById('app')
);