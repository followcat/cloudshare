'use strict';
import React from 'react';
import ReactDOM from 'react-dom';
import enUS from 'antd/lib/locale-provider/en_US';
import { LocaleProvider } from 'antd';
import UploadPreview from '../views/UploadPreview';
import 'babel-polyfill';

ReactDOM.render(
  <LocaleProvider locale={enUS}>
    <UploadPreview />
  </LocaleProvider>,
  document.getElementById('app')
);