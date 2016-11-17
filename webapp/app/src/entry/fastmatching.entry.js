'use strict';
import React from 'react';
import ReactDOM from 'react-dom';

import 'babel-polyfill';

import enUS from 'antd/lib/locale-provider/en_US';
import { LocaleProvider } from 'antd';

import FastMatching from '../views/FastMatching';

ReactDOM.render(
  <LocaleProvider locale={enUS}>
    <FastMatching />
  </LocaleProvider>,
  document.getElementById('app')
);