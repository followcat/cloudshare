'use strict';
import React from 'react';
import ReactDOM from 'react-dom';

import enUS from 'antd/lib/locale-provider/en_US';
import { LocaleProvider } from 'antd';

import Resume from '../containers/Resume';

ReactDOM.render(
  <LocaleProvider local={enUS}>
    <Resume />
  </LocaleProvider>,
  document.getElementById('app')
);