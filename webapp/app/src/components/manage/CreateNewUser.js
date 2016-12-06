'use strict';
import React, { Component, PropTypes } from 'react';
import ButtonWithModal from '../button-with-modal';
import { Form, Input } from 'antd';
const FormItem = Form.Item;

class CreateNewUser extends Component {
  constructor() {
    super();
    this.handleModalOk = this.handleModalOk.bind(this);
    this.checkUserExisted = this.checkUserExisted.bind(this);
  }

  handleModalOk() {
    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        return;
      } else {
        this.props.onCreate(values);
        this.props.form.resetFields();
      }
    });
  }

  checkUserExisted(rule, value, callback) {
    if (!value) {
      callback();
    } else {
      this.props.dataSource.forEach((item) => {
        if (value === item.name) {
          callback(['This name is existed!']);
        }
      });
      callback();
    }
  }

  render() {
    const props = this.props,
          { getFieldProps, getFieldError, isFieldValidating } = this.props.form;

    //name表单验证规则
    const nameProps = getFieldProps('name', {
      rules: [
        { required: true, message: 'Name is required.' },
        { validator: this.checkUserExisted },
      ],
    });

    //password表单验证规则
    const passwordProps = getFieldProps('password', {
      rules: [
        { required: true, message: 'Password is required.'},
        { min: 6, max: 12, message: 'Invalid Password. (At least 6-12 characters)' },
      ],
    });

    return (
      <ButtonWithModal
        {...props}
        onModalOk={this.handleModalOk}
      >
        <Form horizontal>
          <FormItem
            id="name"
            label="Name"
            labelCol={{ span: 6 }}
            wrapperCol={{ span: 14 }}
            hasFeedback
            help={isFieldValidating('name') ? "It's checking name..." : getFieldError('name')}
          >
            <Input
              {...nameProps}
              id="name"
              placeholder="Please input username"
            />
          </FormItem>
          <FormItem
            id="password"
            label="Password"
            labelCol={{ span: 6 }}
            wrapperCol={{ span: 14 }}
          >
            <Input
              {...passwordProps}
              type="password"
              id="password"
              placeholder="Please input password"
            />
          </FormItem>
        </Form>
      </ButtonWithModal>
    );
  }
}

CreateNewUser.defaultProps = {
  onCreate() {},
};

CreateNewUser.propTypes = {
  onCreate: PropTypes.func,
};

export default CreateNewUser = Form.create({})(CreateNewUser);
