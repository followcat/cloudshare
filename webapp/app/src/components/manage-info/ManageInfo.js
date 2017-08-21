'use strict';
import React, { Component, PropTypes } from 'react';
import StorageUtil from '../../utils/storage';
import { getAccount } from 'request/account';

import {
  Form,
  Input,
  Button,
  message,
} from 'antd';

const FormItem = Form.Item;

class ManageInfo extends Component {
  constructor() {
    super();
    this.handleReset = this.handleReset.bind(this);
    this.handleClick = this.handleClick.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
  }

  state = {
    name: StorageUtil.get('user'),
    email: '',
    phone: '',
    btnstatus: false,
  }
    //重置表单方法
  handleReset(e) {
    this.setState({
      btnstatus : false,
    })
    e.preventDefault();
    this.props.form.resetFields();
  }

  handleClick(e) {
     this.props.form.validateFields((errors, values) => {
      if (!errors) {
        this.props.onSubmit(values);
      }
    });
  }

  handleChange(e) {
    e.preventDefault();
    this.setState({
      btnstatus : true,
    })
  }

  handleKeyPress(e) {
    if (e.key === 'Enter') {
      this.handleClick();
    }
  }

  componentDidMount() {
    getAccount({
      name: this.state.name,
    },(json) => {
      if (json.code === 200) {
        this.setState({
          email: json.result.email,
          phone: json.result.phone,
        })
      } else {
        message.error('系统繁忙，刷新重试！');
      }
    });
}

  render() {
    const { wrapperCol, btnText,resetText } = this.props,
          { getFieldDecorator } = this.props.form;

    return (
      <Form layout="horizontal" onKeyPress={this.handleKeyPress} 
        onChange={this.handleChange}>
        <FormItem
          label="用户名"
          hasFeedback
        >
        <label>{this.state.name}</label>
        </FormItem>
        <FormItem
          label="电子邮箱"
          hasFeedback
        >
          {getFieldDecorator('email', {
            initialValue: this.state.email,
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
            initialValue: this.state.phone,
            rules: [{
              required: true, message: '手机号码是地址必填项',}
            ],
          })(
            <Input />
          )}
        </FormItem>
        <FormItem>
        { this.state.btnstatus ?
          <Button type="primary" onClick={this.handleClick}>
          {btnText}
          </Button>
          :
          <Button type="primary" onClick={this.handleClick} disabled>
            {btnText}
          </Button>
        }
          <Button type="ghost" onClick={this.handleReset} >
          {resetText}
          </Button>
        </FormItem>
      </Form>
    );
  }
}

ManageInfo.defaultProps = {
  prefixCls: 'cs-manageinfo',
  btnText: '更新',
  resetText: '重置',
  wrapperCol: {},
  onSubmit() {},
};

ManageInfo.propTypes = {
  prefixCls: PropTypes.string,
  btnText: PropTypes.string,
  resetText: PropTypes.string,
  wrapperCol: PropTypes.object,
  form: PropTypes.object,
  onSubmit: PropTypes.func,
};

export default ManageInfo = Form.create({})(ManageInfo);
