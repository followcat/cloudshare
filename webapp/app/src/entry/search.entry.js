'use strict';
import React from 'react';
import ReacDOM from 'react-dom';
import {
  Router, 
  Route,
  IndexRoute,
  hashHistory
} from 'react-router';

import {
  Layout,
  Search,
  SearchResult
} from 'views/Search/index';

import 'babel-polyfill';

ReacDOM.render(
  <Router history={hashHistory}>
    <Route path="/" component={Layout}>
      <IndexRoute name="search" component={Search} />
      <Route path="search" component={Search} />
      <Route path="result" component={SearchResult}/>
    </Route>
  </Router>,
  document.getElementById('app')
);
