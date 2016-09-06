'use strict';
import React, { Component } from 'react';

import { Table, Popconfirm, message } from 'antd';

export default class Bookmark extends Component {
  constructor(props) {
    super(props);
    this.handleConfirm = this.handleConfirm.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }

  handleConfirm(id) {
    this.props.onDeleteBookmark(id);
  }

  handleCancel() {

  }

  render() {
    const columns = [{
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <a href={`/show/${record.id}.md`}>
          {text !== '' ? text : record.id}
        </a>
      )
    }, {
      title: 'Gender',
      dataIndex: 'gender',
      key: 'gender',
    }, {
      title: 'Age',
      dataIndex: 'age',
      key: 'age',
    }, {
      title: 'Position',
      dataIndex: 'position',
      key: 'position',
    }, {
      title: 'Operation',
      key: 'operation',
      render: (text, record) => (
        <Popconfirm
          title="Are you sure to delete this bookmark?"
          placement="left"
          onConfirm={() => this.handleConfirm(record.id)}
          onCancel={this.handleCancel}
        >
          <a href="#">Delete</a>
        </Popconfirm>
      ),
    }];

    const pagination = {
      total: this.props.bookmarkList.length,
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
        <Table
          columns={columns}
          dataSource={this.props.bookmarkList}
          scroll={{ y: this.props.bookmarkHeight }}
          pagination={pagination}
        />
      </div>
    );
  }
}