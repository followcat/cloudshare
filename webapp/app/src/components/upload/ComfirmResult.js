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
        render: (record) => <a href={`/resume/${record.id}`} target="_blank" disabled={record.status !== 'success' ? true : false}>Check</a>
      }
    ];

    const dataSource = this.props.comfirmResult.concat(this.props.errorResult);

    return (
      <div style={{ width: 720, margin: '0 auto' }}>
        <Table
          columns={columns}
          dataSource={dataSource}
          pagination={false}
          bordered={true}
        />
      </div>
    );
  }
}

ComfirmResult.defaultProps = {
  comfirmResult: [],
  errorResult: [],
};

ComfirmResult.propTypes = {
  comfirmResult: PropTypes.arrayOf(PropTypes.object),
  errorResult: PropTypes.arrayOf(PropTypes.object),
};