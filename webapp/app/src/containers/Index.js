'use strict';
import React, { Component } from 'react';
import 'whatwg-fetch';

import { message } from 'antd';

import Header from '../components/index/Header';
import Login from '../components/index/Login';

import StorageUtil from '../utils/storage';

import './index.less';

export default class Index extends Component {
  constructor() {
    super();
  }

  handleOnSignIn(user) {
    fetch(`/api/session`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: user.account,
        password: user.password,
      }),
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        StorageUtil.setAll({
          _pj: user.project,
          token: json.token,
          user: json.user
        });
        location.href = json.redirect_url;
      } else {
        message.error(json.message);
      }
    });
  }

  render() {
    return (
      <div>
        <div id="viewport">
          <Header />
          <div className="cs-layout-container">
            <Login onSignIn={this.handleOnSignIn}/>
          </div>
        </div>
      </div>
    );
  }
}
