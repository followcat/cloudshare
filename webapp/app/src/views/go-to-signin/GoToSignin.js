'use strict';
import React, { Component } from 'react';
import { browserHistory, Link } from 'react-router';

import Header from 'components/header';

import loginFail from 'image/loginfail.png';

class GoToSignin extends Component {
  constructor() {
    super();
    this.state = {
      second: 5
    };
    this.tick = this.tick.bind(this);
  }

  componentDidMount() {
    this.timer = setInterval(() => {
      if (this.state.second !== 0) {
        this.tick();
      } else {
        clearInterval(this.timer);
        browserHistory.push('/');
      }
    }, 1000);
  }

  componentWillUnmount() {
    clearInterval(this.timer);
  }

  tick() {
    this.setState((prevState) => ({
      second: prevState.second - 1
    }));
  }

  render() {
    const { second } = this.state;

    return (
      <div className="viewport">
        <Header logoMode="center" />
        <div className="signinfail-wrap">
          <div className="info-box">
            <img src={loginFail} alt="signinfail" />
            <p>账号未登陆， <span id="time">{second}</span> 秒后返回登陆页</p>
            <Link to="/">点击立即跳转</Link>
          </div>
        </div>
      </div>
    );
  }
}

export default GoToSignin;
