'use strict';
import React, { Component, PropTypes } from 'react';

import { Table } from 'antd';

import ToolBar from './ToolBar';

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
      total: this.props.searchData.length > 0 ? this.props.searchData.length : this.props.jobDescriptionData.length,
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
        <ToolBar
          onSearch={this.props.onSearch}
          companyData={this.props.companyData}
          confirmLoading={this.props.confirmLoading}
          visible={this.props.visible}
          onModalOpen={this.props.onModalOpen}
          onModalCancel={this.props.onModalCancel}
          onCreateNewJobDescription={this.props.onCreateNewJobDescription}
        />
        <Table
          columns={columns}
          pagination={pagination}
          dataSource={this.props.searchData.length > 0 ? this.props.searchData : this.props.jobDescriptionData}
          expandedRowRender={record => <p>{record.description.split('\n').map((item, index) => {
            return (
              <span key={index}>
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
  searchData: PropTypes.array,
  height: PropTypes.number,
  onSearch: PropTypes.func,
};