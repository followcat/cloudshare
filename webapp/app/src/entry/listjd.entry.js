'use strict';
import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRoute, hashHistory } from 'react-router';
import enUS from 'antd/lib/locale-provider/en_US';
import { LocaleProvider } from 'antd';
import ListJD from '../views/ListJD';
import JobDescription from '../components/list-jd/JobDescription';
import Company from '../components/list-jd/Company';
import 'babel-polyfill';

ReactDOM.render(
  <LocaleProvider locale={enUS}>
    <Router history={hashHistory}>
      <Route
        path="/"
        component={ListJD}
      >
        <IndexRoute
          name="jobdescription"
          component={JobDescription}
        />
        <Route
          path="/jobdescription"
          name="jobdescription"
          title="Job Description"
          component={JobDescription}
        />
        <Route
          path="/company"
          name="company"
          title="Company"
          component={Company}
        />
      </Route>
    </Router>
  </LocaleProvider>,
  document.getElementById('app')
);
