'use strict';
import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRoute, hashHistory } from 'react-router';

import enUS from 'antd/lib/locale-provider/en_US';
import { LocaleProvider } from 'antd';

import ListJD from '../containers/ListJD';
import JobDescription from '../components/listjd/JobDescription';
import Company from '../components/listjd/Company';

ReactDOM.render(
  <LocaleProvider locale={enUS}>
    <Router history={hashHistory}>
      <Route path="/" component={ListJD}>
        <IndexRoute component={JobDescription} />
        <Route path="/jobdescription" component={JobDescription} />
        <Route path="/company" component={Company} />
      </Route>
    </Router>
  </LocaleProvider>,
  document.getElementById('app')
);
