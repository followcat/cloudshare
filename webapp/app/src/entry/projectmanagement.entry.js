'use strict';
import React from 'react';
import ReactDOM from 'react-dom';
import {
  Router, 
  Route,
  IndexRoute,
  hashHistory
} from 'react-router';

import {
  Layout,
  JobDescription,
  OwnCustomer,
  DevelopmentalCustomer
} from '../views/ProjectManagement/index';

import 'babel-polyfill';

ReactDOM.render(
  <Router history={hashHistory}>
    <Route
      path="/"
      component={Layout}
    >
      <IndexRoute
        name="jobdescription"
        component={JobDescription}
      />
      <Route 
        path="/jobdescription"
        component={JobDescription}
      />
      <Route 
        path="/owncustomer"
        component={OwnCustomer}
      />
      <Route
        path="/developcustomer"
        component={DevelopmentalCustomer}
      />
    </Route>
  </Router>,
  document.getElementById('app')
);