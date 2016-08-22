import React from 'react';
import ReactDOM from 'react-dom';
import enUS from 'antd/lib/locale-provider/en_US';
import { LocaleProvider } from 'antd';
import Manage from '../containers/Manage';

ReactDOM.render(
  <LocaleProvider locale={enUS}>
    <Manage />
  </LocaleProvider>,
  document.getElementById('app')
);