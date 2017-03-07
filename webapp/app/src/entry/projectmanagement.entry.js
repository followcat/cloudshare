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
  Customer,
  Company,
  CompanyList,
  CompanyUploader
} from 'views/ProjectManagement/index';

import 'babel-polyfill';

ReactDOM.render(
  <Router history={hashHistory}>
    <Route path="/" component={Layout}>
      <IndexRoute name="jobdescription" component={JobDescription} />
      <Route path="jobdescription" component={JobDescription} />
      <Route path="customer" component={Customer} />
      <Route path="company" component={Company}>
        <Route path="list" component={CompanyList} />
        <Route path="uploader" component={CompanyUploader} />
      </Route>
    </Route>
  </Router>,
  document.getElementById('app')
);