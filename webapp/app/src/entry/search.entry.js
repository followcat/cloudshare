'use strict';
import React, { Component } from 'react';
import ReacDOM from 'react-dom';

import 'babel-polyfill';

import enUS from 'antd/lib/locale-provider/en_US';
import { LocaleProvider } from 'antd';

import Search from '../containers/Search';

ReacDOM.render(
  <LocaleProvider local={enUS}>
    <Search />
  </LocaleProvider>,
  document.getElementById('app')
);