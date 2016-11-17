'use strict';
import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRoute, hashHistory } from 'react-router';

import 'babel-polyfill';

import enUS from 'antd/lib/locale-provider/en_US';
import { LocaleProvider } from 'antd';

import Manage from '../views/Manage';
import UserList from '../components/manage/UserList';
import Setting from '../components/manage/Setting';

ReactDOM.render(
  <LocaleProvider locale={enUS}>
    <Router history={hashHistory}>
      <Route 
        path="/" 
        component={Manage}
      >
        <IndexRoute 
          name="userlist"
          component={UserList}
        />
        <Route
          path="/userlist"
          name="userlist"
          title="User List"
          component={UserList}
        />
        <Route
          path="/setting"
          name="setting"
          title="Setting"
          component={Setting}
        />
      </Route>
    </Router>
  </LocaleProvider>,
  document.getElementById('app')
);