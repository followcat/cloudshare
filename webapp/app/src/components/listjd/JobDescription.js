'use strict';
import React, { Component, PropTypes } from 'react';

import { Table } from 'antd';

export default class JobDescription extends Component {

  constructor(props){
    super(props);
  }

  render() {
    const columns = [
      {
        title: 'Company Name',
        dataIndex: 'company',
        key: 'company',
        width: 160,
      },  
      {
        title: 'Position',
        dataIndex: 'name',
        key: 'position',
        width: 240,
      },
      {
        title: 'Creator',
        dataIndex: 'committer',
        key: 'creator',
        width: 80,
      },
      {
        title: 'Status',
        dataIndex: 'status',
        key: 'status',
        width: 80,
        render: (text) => <span style={text === 'Opening' ? { color: 'green' } : { color: 'red' }}>{text}</span>,
        filterMultiple: true,
        filters: [
          { text: 'Opening', value: 'Opening' },
          { text: 'Closed', value: 'Closed' },
        ],
      },
      {
        title: 'Operation',
        key: 'operation',
        render: (record) => (
          <a href="#">CV Fast Matching</a>
        )
      }
    ];

    const pagination = {
      total: this.props.jobDescriptionData.length,
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
          pagination={pagination}
          dataSource={this.props.jobDescriptionData}
          expandedRowRender={record => <p>{record.description.split('\n').map((item) => {
            return (
              <span>
                {item}
                <br />
              </span>
            )
          })}</p>}
          scroll={{ y: this.props.height }}
        />
      </div>
    );
  }
}

JobDescription.propTypes = {
  jobDescriptionData: PropTypes.array,
  height: PropTypes.number,
};