'use strict';
import React, { Component } from 'react';

import Header from '../components/index/Header';
import Login from '../components/index/Login';

import './index.less';

export default class Index extends Component {
  render() {
    return (
      <div>
        <div id="viewport">
          <Header />
          <div className="cs-layout-container">
            <Login />
          </div>
        </div>
      </div>
    );
  }
}