'use strict';
import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRoute, hashHistory } from 'react-router';
import enUS from 'antd/lib/locale-provider/en_US';
import { LocaleProvider } from 'antd';
import UserInfo from '../views/UserInfo';
import BrowsingHistory from '../components/user-info/BrowsingHistory';
import Bookmark from '../components/user-info/Bookmark';
import Setting from '../components/user-info/Setting';
import 'babel-polyfill';

ReactDOM.render(
  <LocaleProvider locale={enUS}>
    <Router history={hashHistory}>
      <Route path="/" component={UserInfo}>
        <IndexRoute
          name="history"
          component={BrowsingHistory}
        />
        <Route 
          path="/history"
          name="history"
          title="Browsing History"
          component={BrowsingHistory}
        />
        <Route
          path="/bookmark"
          name="bookmark"
          title="Bookmark"
          component={Bookmark}
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
