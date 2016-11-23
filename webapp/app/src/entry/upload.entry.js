'use strict';
import React from 'react';
import ReactDOM from 'react-dom';

import 'babel-polyfill';

import enUS from 'antd/lib/locale-provider/en_US';
import { LocaleProvider } from 'antd';

import Upload from '../containers/Upload';

ReactDOM.render(
  <LocaleProvider local={enUS}>
    <Upload />
  </LocaleProvider>,
  document.getElementById('app')
);