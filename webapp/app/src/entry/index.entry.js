'use strict';
import React from 'react';
import ReactDOM from 'react-dom';

import 'babel-polyfill';

import enUS from 'antd/lib/locale-provider/en_US';
import { LocaleProvider } from 'antd';

import Index from '../views/Index';

ReactDOM.render(
  <LocaleProvider locale={enUS}>
    <Index />
  </LocaleProvider>,
  document.getElementById('app')
);