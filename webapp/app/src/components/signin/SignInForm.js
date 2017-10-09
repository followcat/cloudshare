'use strict';
import React, { Component, PropTypes } from 'react';

import {
  Form,
  Input,
  Icon,
  Button
} from 'antd';

const FormItem = Form.Item;

class SignInForm extends Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
    this.handleRegisterClick = this.handleRegisterClick.bind(this);
  }

  handleRegisterClick(){
    window.location.href = '/createaccount';
  }
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

  render() {
    const { wrapperCol, btnText } = this.props,
          { getFieldDecorator } = this.props.form;

    return (
      <Form layout="horizontal" onKeyPress={this.handleKeyPress}>
        <FormItem  id="account">
          {getFieldDecorator('account', {
            rules: [{ required: true, message: '用户名是必填项' }]
          })(<Input prefix={<Icon type="user" style={{ fontSize: 13 }} />} placeholder="用户名" />
          )}
        </FormItem>
        <FormItem  id="password">
          {getFieldDecorator('password', {
            rules: [
              { required: true, message: '密码是必填项' },
              { min: 6, max: 18, message: '无效密码，密码长度为6-18位' }
            ]
          })(<Input prefix={<Icon type="lock" style={{ fontSize: 13 }} />} type="password" placeholder="密码" />
          )}
        </FormItem>
        <FormItem >
          <Button style={{width : '100%'}} type="primary" onClick={this.handleClick}>
          {btnText}
          </Button>
          </FormItem>
          Or <a href="/createaccount">创建用户!</a>
      </Form>
    );
  }
}

SignInForm.defaultProps = {
  projects: [],
  btnText: '登入',
  wrapperCol: {},
  onSubmit() {},
};

SignInForm.propTypes = {
  projects: PropTypes.array,
  btnText: PropTypes.string,
  wrapperCol: PropTypes.object,
  form: PropTypes.object,
  onSubmit: PropTypes.func,
};

export default SignInForm = Form.create({})(SignInForm);
