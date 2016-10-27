'use strict';
import React, { Component, PropTypes } from 'react';

import { Table } from 'antd';

export default class ComfirmResult extends Component {
  render() {
    const columns = [
      {
        title: 'File Name',
        dataIndex: 'filename',
        key: 'filename',
      }, {
        title: 'Status',
        dataIndex: 'status',
        key: 'status',
        render: (text) => text === 'success' ? <span style={{ color: 'green' }}>{text}</span> : <span style={{ color: 'red' }}>{text}</span>
      }, {
        title: 'Message',
        dataIndex: 'message',
        key: 'message',
        render: (text) => <span>{text}</span>
      }, {
        title: 'Operation',
        key: 'operation',
        render: (record) => <a href={`/show/${record.id}.md`} target="_blank" disabled={record.status !== 'success' ? true : false}>Check</a>
      }
    ];
    return (
      <div style={{ width: 720, margin: '0 auto' }}>
        <Table
          columns={columns}
          dataSource={this.props.comfirmResult}
          pagination={false}
          bordered={true}
        />
      </div>
    );
  }
}

ComfirmResult.propTypes = {
  comfirmResult: PropTypes.arrayOf(PropTypes.object),
};