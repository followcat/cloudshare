'use strict';
import React, { Component, PropTypes } from 'react';

import { Button, Modal, Form, Input, Select } from 'antd';

class CreateJobDescription extends Component {

  constructor(props) {
    super(props);

    this.handleOk = this.handleOk.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
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
    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        return;
      } else {
        this.props.onCreateNewJobDescription(values);
        this.props.form.resetFields();
      }
    });
  }

  render() {
    const style = {
      width: 200,
      display: 'inline-block',
    };
    const { getFieldProps } = this.props.form;

    const selectProps = getFieldProps('companySelection', {
      rules: [
        { required: true, message: 'Please select a company name.' }
      ],
    });

    const jdNameProps = getFieldProps('jdName', {
      rules: [
        { required: true, message: 'Please input job description project name.' }
      ],
    });

    const jdContentProps = getFieldProps('jdContent', {
      rules: [
        { required: true, message: 'Please input job description content.' }
      ],
    });

    return (
      <div style={style}>
        <Button
          type="primary"
          onClick={this.props.onModalOpen}
        >
        Create job description
        </Button>
        <Modal
          title="Create A Job Description"
          visible={this.props.visible}
          confirmLoading={this.props.confirmLoading}
          onCancel={this.props.onModalCancel}
          onOk={this.handleOk}
        >
          <Form horizontal style={{ width: '88%', margin: '0 auto' }}>
            <Form.Item
              id="cName"
              label="Company Name"
            >
              <Select
                {...selectProps}
              >
                {this.props.companyData.map((item, index) => {
                  return (
                    <Select.Option key={index} value={item.name}>{item.name}</Select.Option>
                  )
                })}
              </Select>
            </Form.Item>
            <Form.Item
              id="jdName"
              label="Job Description Project Name"
            >
              <Input {...jdNameProps} />
            </Form.Item>
            <Form.Item
              id="jdContent"
              label="Job Description Content"
            >
              <Input {...jdContentProps} type="textarea" rows="4" />
            </Form.Item>
          </Form>
        </Modal>
      </div>
    );
  }
}

CreateJobDescription.propTypes = {
  visible: PropTypes.bool,
  confirmLoading: PropTypes.bool,
  companyData: PropTypes.array,
};

export default CreateJobDescription = Form.create({})(CreateJobDescription);