'use strict';
import React, { Component } from 'react';
import 'whatwg-fetch';

import { Table, message, Modal } from 'antd';

import CreateUser from './CreateUser';

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
    };
    this.handleModalOpen = this.handleModalOpen.bind(this);
    this.handleModalClose = this.handleModalClose.bind(this);
    this.handleSubmitCreation = this.handleSubmitCreation.bind(this);
    this.showConfirm = this.showConfirm.bind(this);
  }

  loadUserList() {
    fetch(`/api/accounts`, {
      headers: {
        'Authorization': `Basic ${localStorage.token}`
      }
    })
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
    fetch(`/api/accounts`, {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${localStorage.token}`,
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
        fetch(`/api/accounts/${name}`, {
          method: "DELETE",
          headers: {
            'Authorization': `Basic ${localStorage.token}`,
          }
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
    const pagination = {
      total: this.state.datas.length,
      showSizeChanger: true,
      onShowSizeChange(current, pageSize) {
        console.log('Current: ', current, '; PageSize: ', pageSize);
      },
      onChange(current) {
        console.log('Current: ', current);
      },
    };
    return (
      <div>
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
        <Table
          rowSelection={rowSelection}
          columns={columns}
          dataSource={this.state.datas}
          scroll={{ y: this.props.wrapperHeigth }}
          pagination={pagination}
        />
      </div>
    );
  }
}