'use strict';
import React from 'react';
import { Link } from 'react-router';

import { Menu } from 'antd';

import Header from '../components/manage/Header';

import './manage.less';

export default class Manage extends React.Component {
  constructor() {
    super();
    this.state = {
      current: 'userList',
    };
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    this.setState({
      current: e.key,
    });
  }

  render() {
    return (
      <div>
        <div id="viewport">
          <Header />
          <div className="cs-layout-bottom">
            <div className="cs-layout-wrapper">
              <div className="cs-layout-sider">
                <Menu
                  mode="inline"
                  selectedKeys={[this.state.current]}
                  onClick={this.handleClick}
                >
                  <Menu.Item key="userList"><Link to="/userlist">User List</Link></Menu.Item>
                  <Menu.Item key="setting"><Link to="/setting">Setting</Link></Menu.Item>
                </Menu>
              </div>
              {this.props.children}
            </div>
          </div>
        </div>
      </div>
    );
  }
}