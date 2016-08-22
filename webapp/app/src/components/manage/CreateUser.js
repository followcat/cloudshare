import React, { Component } from 'react';

import { Button, Modal, Form, Input } from 'antd';

class CreateUser extends Component {
  constructor(props) {
    super(props);
    this.userExists = this.userExists.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  userExists(rule, value, callback) {
    if (!value) {
      callback();
    } else {
      this.props.userList.forEach((item) => {
        if (value === item.name) {
          callback(['This name is existed.']);
        }
      });
      callback();
    }
  }

  handleSubmit() {
    this.props.onSubmitCreation(this.props.form.getFieldsValue(['name', 'password']));
    this.props.form.resetFields();
  }

  render() {
    const { getFieldProps, getFieldError, isFieldValidating } = this.props.form;
    
    //name表单验证规则
    const nameProps = getFieldProps('name', {
      rules: [
        { required: true, message: 'Name is required.' },
        { validator: this.userExists },
      ],
    });

    //password表单验证规则
    const pwdProps = getFieldProps('password', {
      rules: [
        { required: true, message: 'Password is required.'},
        { min: 6, max: 12, message: 'Invalid Password. (At least 6-12 characters)' },
      ]
    });

    return (
      <div>
        <Button type="primary" onClick={this.props.onModalOpen}>Create User</Button>
        <Modal
          title="Create User"
          okText="Create"
          visible={this.props.visible}
          confirmLoading={this.props.confirmLoading}
          onOk={this.handleSubmit}
          onCancel={this.props.onModalClose}
        >
          <Form horizontal>
            <Form.Item
              id="name"
              label="Name"
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 14 }}
              hasFeedback
              help={isFieldValidating('name') ? "It's checking name..." : getFieldError('name')}
            >
              <Input {...nameProps} id="name" placeholder="Please input username..."/>
            </Form.Item>
            <Form.Item
              id="password"
              label="Password"
              labelCol={{ span: 6 }}
              wrapperCol={{ span: 14 }}
            >
              <Input {...pwdProps} type="password" id="password" placeholder="Please input password..."/>
            </Form.Item>
          </Form>
        </Modal>
      </div>
    );
  }
}

export default CreateUser = Form.create({})(CreateUser);