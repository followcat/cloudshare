import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, IndexRoute, hashHistory } from 'react-router';

import enUS from 'antd/lib/locale-provider/en_US';
import { LocaleProvider } from 'antd';

import Manage from '../containers/Manage';
import UserList from '../components/manage/UserList';
import Setting from '../components/manage/Setting';

ReactDOM.render(
  <LocaleProvider locale={enUS}>
    <Router history={hashHistory}>
      <Route path="/" component={Manage}>
        <IndexRoute component={UserList} />
        <Route path="/userlist" component={UserList} />
        <Route path="/setting" component={Setting} />
      </Route>
    </Router>
  </LocaleProvider>,
  document.getElementById('app')
);