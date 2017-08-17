'use strict';
import React, { Component } from 'react';

import CreateAccount from 'components/create-account';
import Header from 'components/header';
import Feature from 'components/feature';

import { message } from 'antd';

import { getFeature } from 'request/feature';

import StorageUtil from 'utils/storage';
import { createAccount } from 'request/account';


class Register extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      dataSource: '',
      projects: [],
    };
    this.handleFeatureClick = this.handleFeatureClick.bind(this);
    this.handleFeatureClose = this.handleFeatureClose.bind(this);
    this.handleCreateAccountSubmit = this.handleCreateAccountSubmit.bind(this);
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

  handleCreateAccountSubmit(feildValue) {
    createAccount({
      name: feildValue.name,
      password: feildValue.password,
      email: feildValue.email,
      phone: feildValue.phone,
    }, (json) => {
      if (json.code === 200) {
        message.success('注册成功',3,function(){
          window.location.href = json.redirect_url;
        });
      } else {
        message.error('注册信息有误！');
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
            <CreateAccount
              title="注册"
              btnText="注册"
              projects={this.state.projects}
              wrapperCol={{ span: 14, offset: 9 }}
              onSubmit={this.handleCreateAccountSubmit}
            />
          </div>
        </div>
      </div>
    );
  }
}

export default Register;