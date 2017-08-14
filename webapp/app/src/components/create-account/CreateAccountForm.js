'use strict';
import React, { Component, PropTypes } from 'react';

import {
  Form,
  Input,
  Button
} from 'antd';

const FormItem = Form.Item;

class CreateAccountForm extends Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
  }

  state = {
    confirmDirty: false,
    autoCompleteResult: [],
  };

  handleClick(e) {
    // e.preventDefault();

    this.props.form.validateFields((errors, values) => {
      if (!errors) {
        this.props.onSubmit(values);
      }
    });
  }

  handleKeyPress(e) {
    if (e.key === 'Enter') {
      this.handleClick();
    }
  }

    handleConfirmBlur = (e) => {
    const value = e.target.value;
    this.setState({ confirmDirty: this.state.confirmDirty || !!value });
  }
  checkPassword = (rule, value, callback) => {
    const form = this.props.form;
    if (value && value !== form.getFieldValue('password')) {
      callback('Two passwords that you enter is inconsistent!');
    } else {
      callback();
    }
  }
  checkConfirm = (rule, value, callback) => {
    const form = this.props.form;
    if (value && this.state.confirmDirty) {
      form.validateFields(['confirm'], { force: true });
    }
    callback();
  }

  render() {
    const { wrapperCol, btnText } = this.props,
          { getFieldDecorator } = this.props.form;

    return (
      <Form layout="horizontal" onKeyPress={this.handleKeyPress}>
        <FormItem
          label="用户名"
          id="account"
        >
          {getFieldDecorator('name', {
            rules: [{ required: true, message: '用户名是必填项' }]
          })(<Input placeholder="请输入用户名" />)}
        </FormItem>
                <FormItem
          label="Password"
          hasFeedback
        >
          {getFieldDecorator('password', {
            rules: [{
              required: true, message: '密码是必填项',
            },{min : 6,max : 18 ,message: '密码长度必须介于6到18'}, {
              validator: this.checkConfirm,
            }],
          })(
            <Input type="password" />
          )}
        </FormItem>
        <FormItem
          label="Confirm Password"
          hasFeedback
        >
          {getFieldDecorator('confirm', {
            rules: [{
              required: true, message: '请再次确认密码',
            },{
              validator: this.checkPassword,
            }],
          })(
            <Input type="password" onBlur={this.handleConfirmBlur} />
          )}
        </FormItem>
        <FormItem
          label="E-mail"
          hasFeedback
        >
          {getFieldDecorator('email', {
            rules: [{
              type: 'email', message: '请输入正确邮箱地址',
            },{
              required: true, message: '邮箱是地址必填项',}
            ],
          })(
            <Input />
          )}
        </FormItem>
        <FormItem
          label="Phone Number"
        >
          {getFieldDecorator('phone')(
            <Input />
          )}
        </FormItem>
        <FormItem wrapperCol={wrapperCol}>
          <Button
            type="primary"
            onClick={this.handleClick}
          >
            {btnText}
          </Button>
        </FormItem>
      </Form>
    );
  }
}

CreateAccountForm.defaultProps = {
  projects: [],
  btnText: '注册',
  wrapperCol: {},
  onSubmit() {},
};

CreateAccountForm.propTypes = {
  projects: PropTypes.array,
  btnText: PropTypes.string,
  wrapperCol: PropTypes.object,
  form: PropTypes.object,
  onSubmit: PropTypes.func,
};

export default CreateAccountForm = Form.create({})(CreateAccountForm);
