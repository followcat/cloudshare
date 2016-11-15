'use strict';
import React from 'react';
import ReactDOM from 'react-dom';

import 'babel-polyfill';

import enUS from 'antd/lib/locale-provider/en_US';
import { LocaleProvider } from 'antd';

import SearchResult from '../containers/SearchResult';

ReactDOM.render(
  <LocaleProvider local={enUS}>
    <SearchResult />
  </LocaleProvider>,
  document.getElementById('app')
);