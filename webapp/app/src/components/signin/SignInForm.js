'use strict';
import React, { Component, PropTypes } from 'react';

import {
  Form,
  Input,
  Button,
  Select
} from 'antd';

const FormItem = Form.Item,
      SelectOption = Select.Option;

class SignInForm extends Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(e) {
    e.preventDefault();

    this.props.form.validateFields((errors, values) => {
      if (!errors) {
        this.props.onSubmit(values);
      }
    });
  }

  render() {
    const { wrapperCol, btnText } = this.props,
          { getFieldDecorator } = this.props.form;

    return (
      <Form layout="horizontal">
        <FormItem
          label="用户名"
          id="account"
        >
          {getFieldDecorator('account', {
            rules: [{ required: true, message: '用户名是必填项' }]
          })(<Input placeholder="请输入用户名" />)}
        </FormItem>
        <FormItem
          label="密码"
          id="password"
        >
          {getFieldDecorator('password', {
            rules: [
              { required: true, message: '密码是必填项' },
              { min: 6, max: 18, message: '无效密码，密码长度为6-18位' }
            ]
          })(<Input type="password" placeholder="请输入密码" />)}
        </FormItem>
        <FormItem
          label="项目"
          id="project"
        >
          {getFieldDecorator('project', {
            rules: [
              { required: true, message: '项目是必填项' }
            ],
          })(<Select>
              {this.props.projects.map((item, index) => {
                return (
                  <SelectOption
                    key={index}
                    value={item}
                  >
                    {item}
                  </SelectOption>
                );
              })}
            </Select>)}
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
