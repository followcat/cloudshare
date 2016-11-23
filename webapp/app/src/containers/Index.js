'use strict';
import React, { Component } from 'react';
import { message } from 'antd';
import Home from '../components/index/Home';
import HomeMain from '../components/index/HomeMain';
import SignIn from '../components/signin';
import Header from '../components/index/Header';
import Feature from '../components/feature';
import StorageUtil from '../utils/storage';
import 'whatwg-fetch';

export default class Index extends Component {
  constructor() {
    super();

    this.state = {
      visible: false,
      dataSource: '',
      projects: [],
    };

    this.handleFeatureClick = this.handleFeatureClick.bind(this);
    this.handleFeatureClose = this.handleFeatureClose.bind(this);
    this.handleSignInSubmit = this.handleSignInSubmit.bind(this);
    this.getFeatureData = this.getFeatureData.bind(this);
    this.getProjectData = this.getProjectData.bind(this);
  }

  componentDidMount() {
    this.getProjectData();
  }

  handleFeatureClick() {
    this.setState({
      visible: true,
    });
    this.getFeatureData();
  }

  handleFeatureClose() {
    this.setState({
      visible: false,
    });
  }

  handleSignInSubmit(feildValue) {
    fetch(`/api/session`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: feildValue.account,
        password: feildValue.password,
      }),
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        StorageUtil.setAll({
          _pj: feildValue.project,
          token: json.token,
          user: json.user
        });
        location.href = json.redirect_url;
      } else {
        message.error(json.message);
      }
    });
  }

  getFeatureData() {
    fetch(`/api/feature`, {
      method: 'GET',
    })
    .then(response => response.json())
    .then(json => {
      if (json.code === 200) {
        this.setState({
          dataSource: json.data,
        });
      }
    })
  }

  getProjectData() {
    fetch(`/api/projectnames`, {
      method: 'GET',
    })
    .then(response => response.json())
    .then(json => {
      if (json.code === 200) {
        this.setState({
          projects: json.data,
        });
      }
    })
  }

  render() {
    return (
      <Home>
        <Header>
          <Feature
            visible={this.state.visible}
            dataSource={this.state.dataSource}
            onClick={this.handleFeatureClick}
            onOk={this.handleFeatureClose}
            onCancel={this.handleFeatureClose}
            wrapClassName="vertical-center-modal"
          />
        </Header>
        <HomeMain>
          <SignIn 
            projects={this.state.projects}
            wrapperCol={{ span: 14, offset: 9 }}
            onSubmit={this.handleSignInSubmit}
          />
        </HomeMain>
      </Home>
    );
  }
}
