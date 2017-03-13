'use strict';
import React from 'react';
import ReactDOM from 'react-dom';
import {
  Router,
  Route,
  browserHistory
} from 'react-router';

import Layout from 'views/common/Layout';
import { FastMatching } from 'views/FastMatching/index';

import 'babel-polyfill';

ReactDOM.render(
  <Router history={browserHistory}>
    <Route path="/" component={Layout} >
    <Route path="fastmatching" component={FastMatching} />
    </Route>
  </Router>,
  document.getElementById('app')
);