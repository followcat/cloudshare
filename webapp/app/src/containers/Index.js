'use strict';
import React, { Component } from 'react';
import 'whatwg-fetch';

import { message } from 'antd';

import Header from '../components/index/Header';
import Login from '../components/index/Login';

import './index.less';

import config from '../../config';

export default class Index extends Component {
  constructor() {
    super();
  }

  handleOnSignIn(user) {
    fetch(`${config.host}/login/check`, {
      method: 'POST',
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
        localStorage.token = json.token;
        localStorage.user = json.user;
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
