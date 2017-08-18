'use strict';
import React, { Component, PropTypes } from 'react';
import StorageUtil from '../../utils/storage';

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
    this.handleClick = this.handleClick.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
  }

  state = {
    name: StorageUtil.get('user'),
  };

  handleClick(e) {
     e.preventDefault();

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
            更新
          </Button>
        </FormItem>
      </Form>
    );
  }
}

ManageInfo.defaultProps = {
  prefixCls: 'cs-manageinfo',
  projects: [],
  btnText: '',
  wrapperCol: {},
  onSubmit() {},
};

ManageInfo.propTypes = {
  projects: PropTypes.array,
  btnText: PropTypes.string,
  wrapperCol: PropTypes.object,
  form: PropTypes.object,
  onSubmit: PropTypes.func,
};

export default ManageInfo = Form.create({})(ManageInfo);
