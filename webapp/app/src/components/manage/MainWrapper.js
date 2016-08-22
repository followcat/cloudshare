'use strict';
import React, { Component } from 'react';
import { Menu, Table, Button, Modal, Form, Input } from 'antd';

import CreateUser from './CreateUser';

import './mainwrapper.less';

const columns = [
  {
    title: 'Name',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'Operation',
    key: 'operation',
    render: () => (
      <a href="#" onClick={showConfirm}>Delete</a>
    )
  }
];

function showConfirm() {
  Modal.confirm({
    title: "Delete User",
    content: "Are you sure to delete this user item?",
    onOk() {
      return new Promise((resolve) => {
        setTimeout(resolve, 2000);
      });
    },
    onCancel() {},
  });
}

export default class MainWrapper extends Component {
  constructor(props) {
    super(props);

    this.state = {
      current: 'user',
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
      <div className="cs-layout-bottom">
        <div className="cs-layout-wrapper">
          <div className="cs-layout-sider">
            <Menu
              mode="inline"
              selectedKeys={[this.state.current]}
              onClick={this.handleClick}
            >
              <Menu.Item key="user">User List</Menu.Item>
              <Menu.Item key="setting">Setting</Menu.Item>
            </Menu>
          </div>
          <div className="cs-layout-content">
            <div className="toolbar">
              <CreateUser {...this.props} />
            </div>
            <Table columns={columns} dataSource={this.props.userList} />
          </div>
        </div>
      </div>
    );
  }
}

React.propTypes = {
  datas: React.PropTypes.array.isRequired,
  visible: React.PropTypes.bool,
};