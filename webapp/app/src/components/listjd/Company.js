 'use strict';
import React, { Component, PropTypes } from 'react';

import { Table, Button, Modal, Form, Input } from 'antd';

class Company extends Component {
  constructor(props) {
    super(props);
    this.state = {
      visible: false,
      confirmLoading: false,
    };

    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
    this.handleOk = this.handleOk.bind(this);
  }

  handleClick() {
    this.setState({
      visible: true,
    });
  }

  handleCancel() {
    this.setState({
      visible: false,
    });
  }

  handleOk() {
    this.setState({
      confirmLoading: true,
    });

    const _this = this;

    this.props.form.validateFields((error, value) => {
      if (!!error) {
        return;
      } else {
        this.props.onCreateNewCompany(value, function() {
          _this.setState({
            confirmLoading: false,
            visible: false,
          });
          _this.props.form.resetFields();
        })
      }
    })
  }


  render() {
    const columns = [
      {
        title: 'Company Name',
        dataIndex: 'name',
        key: 'name',
        width: 280,
      },
      {
        title: 'Introduction',
        dataIndex: 'introduction',
        key: 'introduction',
      },
    ];

    const pagination = {
      total: this.props.companyData.length,
      showSizeChanger: true,
    };

    const { getFieldProps } = this.props.form;

    return (
      <div>
        <div style={{ paddingTop: 10, paddingBottom: 10 }}>
          <Button
            type="primary"
            onClick={this.handleClick}
          >
          Create new company
          </Button>
          <Modal
            title="Create New Company"
            okText="Submit"
            visible={this.state.visible}
            onCancel={this.handleCancel}
            onOk={this.handleOk}
          >
            <Form horizontal style={{ width: '88%', margin: '0 auto' }}>
              <Form.Item
                label="Company Name"
              >
                <Input
                  {...getFieldProps('companyName', { rules: [{ required: true }]})}
                  placeholder="Please input the company name"
                />
              </Form.Item>
              <Form.Item
                label="Introduction"
              >
                <Input
                  {...getFieldProps('introduction')}
                  type="textarea"
                  rows="4"
                />
              </Form.Item>
            </Form>
          </Modal>
        </div>
        <Table
          columns={columns}
          pagination={pagination}
          dataSource={this.props.companyData}
          scroll={{ y: this.props.height }}
        />
      </div>
    );
  }
}

Company.propTypes = {

};

export default Company = Form.create({})(Company);
