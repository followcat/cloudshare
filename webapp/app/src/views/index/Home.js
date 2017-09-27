'use strict';
import React, { Component } from 'react';

import SignIn from 'components/signin';
import Header from 'components/header';
import Feature from 'components/feature';

import { message } from 'antd';

import { getFeature } from 'request/feature';

import StorageUtil from 'utils/storage';
import { signIn } from 'request/sign';


class Home extends Component {
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
    signIn({
      username: feildValue.account,
      password: feildValue.password,
    }, (json) => {
      if (json.code === 200) {
        StorageUtil.setAll({
          token: json.token,
          user: json.user
        });
        window.location.href = json.redirect_url;
      } else {
        message.error('用户名或密码错误！');
      }
    });
  }

  getFeatureData() {
    getFeature((json) => {
      if (json.code === 200) {
        this.setState({
          dataSource: json.data,
        });
      }
    });
  }


  render() {
    return (
      <div className="viewport">
        <Header logoMode="center">
          <Feature
            style={{ position: 'absolute', right: 0, top: 0 }}
            text="更新日志"
            title="更新日志"
            visible={this.state.visible}
            dataSource={this.state.dataSource}
            onClick={this.handleFeatureClick}
            onCancel={this.handleFeatureClose}
            footer={null}
            wrapClassName="vertical-center-modal"
          />
        </Header>
        <div className="cs-container">
          <div className="cs-container-center">
            <div className="cs-container-center-info">
              <h1>最智能速配简历平台</h1>
              <p>职位智能深度分析<br />可视化数据对比<br />云招聘共享管理</p>
            </div>
            <SignIn
              title="登入"
              btnText="登入"
              projects={this.state.projects}
              wrapperCol={{ span: 14, offset: 9 }}
              onSubmit={this.handleSignInSubmit}
            />
          </div>
        </div>
      </div>
    );
  }
}

export default Home;
