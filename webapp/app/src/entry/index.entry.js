'use strict';
import React from 'react';
import ReactDOM from 'react-dom';
import {
  Router, 
  Route,
  browserHistory
} from 'react-router';

import { Home } from 'views/Index/index';

import 'babel-polyfill';

ReactDOM.render(
  <Router history={browserHistory}>
    <Route path="index" component={Home} />
  </Router>,
  document.getElementById('app')
);