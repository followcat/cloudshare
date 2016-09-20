'use strict';
import React, { Component, PropTypes } from 'react';

import { Table, Button, Modal, Form, Input, Select } from 'antd';

import ToolBar from './ToolBar';

class JobDescription extends Component {

  constructor(props){
    super(props);
    this.state = {
      visible: false,
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
  }

  handleClick(record) {
    this.props.form.setFieldsValue({
      companyName: record.company,
      jdId: record.id,
      jdContent: record.description,
      statusSelect: record.status,
    });
    this.setState({
      visible: true,
    });
  }

  handleCancel() {
    this.setState({
      visible: false,
    });
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
          <div>
            <Button type="primary" size="small">CV Fast Matching</Button>
            <Button type="ghost" size="small" onClick={() => this.handleClick(record)}>Edit Job Description</Button>
          </div>
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

    const { getFieldProps } = this.props.form;
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
        <Modal
          title="Edit Job Description"
          okText="Submit"
          wrapClassName="vertical-center-modal"
          visible={this.state.visible}
          onCancel={this.handleCancel}
        >
          <Form horizontal style={{ width: '88%', margin: '0 auto' }}>
            <Form.Item
              label="Company Name"
            >
              <Input
                {...getFieldProps('companyName')}
                disabled={true}
              />
            </Form.Item>
            <Form.Item
              label="Job Description ID"
            >
              <Input
                {...getFieldProps('jdId')}
              />
            </Form.Item>
            <Form.Item
              label="Job Description Content"
            >
              <Input
                {...getFieldProps('jdContent')}
                type="textarea"
                rows="4"
              />
            </Form.Item>
            <Form.Item
              label="Status"
            >
              <Select
                {...getFieldProps('statusSelect')}
              >
                <Select.Option key={0} value="Opening">Opening</Select.Option>
                <Select.Option key={0} value="Closed">Closed</Select.Option>
              </Select>
            </Form.Item>
          </Form>
        </Modal>
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

export default JobDescription = Form.create({})(JobDescription);