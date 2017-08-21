'use strict';
import React, { Component, PropTypes } from 'react';
import { checkAccount } from 'request/account';

import {
  Form,
  Input,
  Button,
  message,
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
    result: false,
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

  handleNameFocus = (e) => {
    this.setState({result: false})
  }

  handleNameBlur = (e) => {
    const form = this.props.form;
    const value = e.target.value;
    if (value){
    checkAccount({
      name: form.getFieldValue('name'),
    },(json) => {
      if (json.code === 200) {
          this.setState({result: true})
          form.validateFields(['name'], { force: true });
      } else {
        message.error('系统繁忙，稍后再试！');
      }
    });
    }
  }

  checkName = (rule, value, callback) => {
    const form = this.props.form;
    if (value && this.state.result) {
      callback('用户名已存在，请重新输入!');
    } else {
      callback();
    }
  }

  checkPassword = (rule, value, callback) => {
    const form = this.props.form;
    if (value && value !== form.getFieldValue('password')) {
      callback('您输入的两个密码不一致!');
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
          hasFeedback
        >
          {getFieldDecorator('name', {
            rules: [{ required: true, message: '用户名是必填项',whitespace: true },
            {
              validator: this.checkName,
            }]
          })(<Input onBlur={this.handleNameBlur}  onFocus={this.handleNameFocus} placeholder="请输入用户名" />)}
        </FormItem>
                <FormItem
          label="密码"
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
          label="确认密码"
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
          label="电子邮箱"
          hasFeedback
        >
          {getFieldDecorator('email', {
            rules: [{
              type: 'email', message: '请输入正确邮箱地址'
            },{
              required: true, message: '邮箱地址是必填项'}
            ],
          })(
            <Input />
          )}
        </FormItem>
        <FormItem label="联系电话"  hasFeedback>
          {getFieldDecorator('phone',{
            rules: [{
              required: true, message: '手机号码是地址必填项',}
            ],
          })(
            <Input />
          )}
        </FormItem>
        <FormItem>
          <Button type="primary" onClick={this.handleClick}>
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
