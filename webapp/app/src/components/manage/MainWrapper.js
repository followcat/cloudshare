'use strict';
import React, { Component } from 'react';
import { Menu, Table, Button } from 'antd';

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
      <a href="#">删除</a>
    )
  }
];

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
    
    const datas = [
      {
        key: 1,
        name: 'CJK',
      },
      {
        key: 2,
        name: 'Test'
      }
    ];

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
              <Button type="primary">Create User</Button>
            </div>
            <Table columns={columns} dataSource={datas} />
          </div>
        </div>
      </div>
    );
  }
}