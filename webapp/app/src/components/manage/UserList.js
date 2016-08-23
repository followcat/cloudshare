'use strict';
import React, { Component } from 'react';
import 'whatwg-fetch';

import { Table, message, Modal } from 'antd';

import CreateUser from './CreateUser';
import config from '../../../config';

message.config({
  top: 66,
  duration: 3,
});

export default class UserList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      datas: [],
      visible: false,
      confirmLoading: false,
      tableHeight: 0,
    };
    this.handleModalOpen = this.handleModalOpen.bind(this);
    this.handleModalClose = this.handleModalClose.bind(this);
    this.handleSubmitCreation = this.handleSubmitCreation.bind(this);
    this.showConfirm = this.showConfirm.bind(this);
  }

  loadUserList() {
    fetch(`${config.host}/api/accounts`)
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        let datas = json.data.map((value, index) => {
          return { key: index, name: value };
        });
        this.setState({ datas: datas });
      }
    })
  }

  handleModalOpen() {
    this.setState({
      visible: true,
    });
  }

  handleModalClose() {
    this.setState({
      visible: false,
    });
  }

  handleSubmitCreation(user) {
    this.setState({
      confirmLoading: true,
    });
    fetch(`${config.host}/api/accounts`,{
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-type': 'application/json',
      },
      body: JSON.stringify({
        name: user.name,
        password: user.password,
      })
    })
    .then((response) => {
      return response.json();
    })
    .then((json) => {
      if (json.code === 200) {
        let datas = this.state.datas,
            len = datas.length;
        datas.push({ key: len, name: user.name });
        this.setState({
          datas: datas,
          confirmLoading: false,
          visible: false,
        });
        message.success(json.message);
      } else {
        this.setState({
          confirmLoading: false,
          visible: false,
        });
        message.error(json.message);
      }
    });
  }

  showConfirm(name) {
    const _this = this;
    Modal.confirm({
      title: "Delete User",
      content: "Are you sure to delete this user item?",
      okText: 'Yes',
      cancelText: 'No',
      onOk() {
        fetch(`${config.host}/api/accounts/${name}`, {
          method: "DELETE",
        })
        .then((response) => {
          return response.json();
        })
        .then((json) => {
          if (json.code === 200) {
            _this.loadUserList();
            message.success(json.message);
          } else {
            message.error(json.message);
          }
        });
      },
      onCancel() {},
    });
  }

  componentDidMount() {
    this.loadUserList();

    let height = parseInt(this.refs.contentDiv.offsetHeight - this.refs.toolbarDiv.offsetHeight) - 90;
    this.setState({
      tableHeight: height,
    });
  }

  render() {
    const columns = [
      {
        title: 'Name',
        dataIndex: 'name',
        key: 'name',
        width: 300,
      },
      {
        title: 'Operation',
        key: 'operation',
        render: (record) => (
          <a href="#" onClick={() => {this.showConfirm(record.name)}}>Delete</a>
        )
      }
    ];
    const rowSelection = {};
    return (
      <div>
        <div className="cs-layout-content" ref="contentDiv">
          <div className="toolbar" ref="toolbarDiv">
            <CreateUser             
              userList={this.state.datas}
              visible={this.state.visible}
              confirmLoading={this.state.confirmLoading}
              onSubmitCreation={this.handleSubmitCreation}
              onModalOpen={this.handleModalOpen}
              onModalClose={this.handleModalClose}
            />
          </div>
          <Table rowSelection={rowSelection} columns={columns} dataSource={this.state.datas} scroll={{ y: this.state.tableHeight }} />
        </div>
      </div>
    );
  }
}