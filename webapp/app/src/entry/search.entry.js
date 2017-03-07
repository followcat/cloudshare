'use strict';
import React from 'react';
import ReacDOM from 'react-dom';
import {
  Router, 
  Route,
  IndexRoute,
  browserHistory
} from 'react-router';

import Layout from 'views/common/Layout';
import { Search, SearchResult } from 'views/Search/index';

import 'babel-polyfill';

ReacDOM.render(
  <Router history={browserHistory}>
    <Route path="/" component={Layout}>
      <IndexRoute name="search" component={Search} />
      <Route path="search" component={Search} />
      <Route path="result" component={SearchResult}/>
    </Route>
  </Router>,
  document.getElementById('app')
);
