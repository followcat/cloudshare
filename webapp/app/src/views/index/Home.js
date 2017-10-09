'use strict';
import React, { Component } from 'react';

import SignIn from 'components/signin';
import Header from 'components/header';
import Feature from 'components/feature';
import CreateAccount from 'components/create-account';

import { message, Tabs } from 'antd';

import { getFeature } from 'request/feature';
import { createAccount } from 'request/account';
import { signIn } from 'request/sign';

import StorageUtil from 'utils/storage';

const TabPane = Tabs.TabPane;

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

  handleCreateAccountSubmit(feildValue) {
    createAccount({
      name: feildValue.name,
      password: feildValue.password,
      email: feildValue.email,
      phone: feildValue.phone,
      smscode: feildValue.smscode,
    }, (json) => {
      if (json.code === 200) {
        message.success('注册成功',1,function(){
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
            <div className="cs-container-center-info">
              <h1>最智能速配简历平台</h1>
              <p>职位智能深度分析<br />可视化数据对比<br />云招聘共享管理</p>
            </div>
            <div className="cs-container-center-flow">
              <Tabs defaultActiveKey="1" animated={false} tabBarStyle={{borderBottom: '0px solid',marginBottom: '10px'}}>
                <TabPane tab="登入" key="1">
                  <SignIn
                    title="登入"
                    btnText="登入"
                    projects={this.state.projects}
                    wrapperCol={{ span: 14, offset: 9 }}
                    onSubmit={this.handleSignInSubmit}
                  />
                </TabPane>
                <TabPane tab="注册" key="2">
                  <CreateAccount
                    title="注册"
                    btnText="注册"
                    projects={this.state.projects}
                    wrapperCol={{ span: 14, offset: 9 }}
                    onSubmit={this.handleCreateAccountSubmit}
                  />
                </TabPane>
              </Tabs>
              </div>
          </div>
        </div>
        <div className="copyright">
            <p>Copyright©2015 广州汇人达计算机科技有限公司 粤ICP15006654号-1 </p>  
        </div>
      </div>
    );
  }
}

export default Home;
