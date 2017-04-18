'use strict';
import React, { Component, PropTypes } from 'react';

import ButtonWithModal from 'components/button-with-modal';

import { Form, Input, message } from 'antd';

import { createAccount } from 'request/account';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class CreateNewUser extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
      confirmLoading: false
    };
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.handleModalOk = this.handleModalOk.bind(this);
    this.handleModalCancel = this.handleModalCancel.bind(this);
    this.checkUserExisted = this.checkUserExisted.bind(this);
    this.onCreate = this.onCreate.bind(this);
  }

  handleButtonClick() {
    this.setState({
      visible: true
    });
  }

  handleModalOk() {
    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        return;
      } else {
        this.onCreate(values);
        this.props.form.resetFields();
      }
    });
  }

  handleModalCancel() {
    this.setState({
      visible: false
    });
  }

  checkUserExisted(rule, value, callback) {
    if (!value) {
      callback();
    } else {
      this.props.dataSource.forEach((item) => {
        if (value === item.name) {
          callback(['该用户名已存在']);
        }
      });
      callback();
    }
  }

  onCreate(fieldValue) {
    this.setState({
      confirmLoading: true
    });

    createAccount(fieldValue, (json) => {
      this.setState({
        confirmLoading: false,
        visible: false,
      });

      if (json.code === 200) {
        message.success(language.ADD_SUCCESS_MSG);
        this.props.getUserList();
      } else {
        message.error(language.ADD_FAIL_MSG);
      }
    });
  }

  render() {
    const { getFieldDecorator, getFieldError, isFieldValidating } = this.props.form;
    const { visible, confirmLoading } = this.state;

    const itemWrap = {
      labelCol: { span: 6 },
      wrapperCol: { span: 14 }
    };

    return (
      <ButtonWithModal
        visible={visible}
        confirmLoading={confirmLoading}
        buttonType="primary"
        buttonText="新建用户"
        modalTitle="创建新用户"
        modalOkText="新建"
        modalCancelText="关闭"
        onButtonClick={this.handleButtonClick}
        onModalOk={this.handleModalOk}
        onModalCancel={this.handleModalCancel}
      >
        <Form layout="horizontal">
          <Form.Item
            {...itemWrap}
            id="name"
            label="用户名"
            hasFeedback
            help={isFieldValidating('name') ? '正在验证该用户名...' : getFieldError('name')}
          >
            {getFieldDecorator('name', {
              rules: [
                { required: true, message: '必填项' },
                { validator: this.checkUserExisted },
              ]
            })(
              <Input placeholder="请输入用户名" />
            )}
          </Form.Item>
          <Form.Item
            {...itemWrap}
            id="password"
            label="密码"
          >
            {getFieldDecorator('password', {
              rules: [
                { required: true, message: '必填项'},
                { min: 6, max: 12, message: '无效密码, 必须有6-12个字符组成' },
              ]
            })(
              <Input type="password" placeholder="请输入密码" />
            )}
          </Form.Item>
        </Form>
      </ButtonWithModal>
    );
  }
}

CreateNewUser.defaultProps = {
  dataSource: [],
  onCreate() {},
};

CreateNewUser.propTypes = {
  dataSource: PropTypes.array,
  form: PropTypes.object,
  getUserList: PropTypes.func,
  onCreate: PropTypes.func
};

export default CreateNewUser = Form.create({})(CreateNewUser);
