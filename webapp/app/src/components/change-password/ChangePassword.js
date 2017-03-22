'use strict';
import React, { Component, PropTypes } from 'react';
import { Button, Form, Input, Row, Col } from 'antd';
import classNames from 'classnames';

const FormItem = Form.Item;

function noop() {
  return false;
}

class ChangePassword extends Component {
  constructor() {
    super();
    this.state = {
      newPasswordBarShow: false,
      reNewPasswordBarShow: false,
      newPasswrodStrength: 'L',
      reNewPasswordStrength: 'L',
    };
    this.handleReset = this.handleReset.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.getPasswordStrenth = this.getPasswordStrenth.bind(this);
    this.checkPassword = this.checkPassword.bind(this);
    this.checkRePassword = this.checkRePassword.bind(this);
  }

  //重置表单方法
  handleReset(e) {
    e.preventDefault();
    this.props.form.resetFields();
  }

  //提交表单方法
  handleSubmit(e) {
    e.preventDefault();
    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        return;
      } else {
        this.props.onSubmit(values);
        this.props.form.resetFields();
      }
    });
  }

  //获取密码长度方法
  getPasswordStrenth(value, type) {
    if (value) {
      let strength;
      // 密码强度的校验规则自定义
      if (value.match(/^\d+$/g)) {
        strength = 'L';
      } else if (value.length <= 9) {
        strength = 'M';
      } else {
        strength = 'H';
      }
      if (type === 'newPassword') {
        this.setState({ 
          newPasswordBarShow: true,
          newPasswrodStrength: strength,
        });
      } else {
        this.setState({
          reNewPasswordBarShow: true,
          reNewPasswordStrength: strength,
        });
      }
    } else {
      if (type === 'newPassword') {
        this.setState({
          newPasswordBarShow: false,
        });
      } else {
        this.setState({
          reNewPasswordBarShow: false,
        });
      }
    }
  }

  //新密码表单验证方法
  checkPassword(rule, value, callback) {
    const { validateFields } = this.props.form;
    this.getPasswordStrenth(value, 'newPassword');

    if (value) {
      validateFields(['reNewPassword'], { force: true });
    }
    callback(); 
  }

  //确认新密码表单验证方法
  checkRePassword(rule, value, callback) {
    const { getFieldValue } = this.props.form;
    this.getPasswordStrenth(value, 'reNewPassword');

    if (value && value !== getFieldValue('newPassword')) {
      callback('两次输入的密码不一致');
    } else {
      callback();
    }
  }

  //渲染密码强度验证条UI
  renderPasswordStrengthBar(type) {
    const strength = type === 'newPassword' ? this.state.newPasswrodStrength : this.state.reNewPasswordStrength;
    const classSet = classNames({
      'ant-pwd-strength': true,
      'ant-pwd-strength-low': strength === 'L',
      'ant-pwd-strength-medium': strength === 'M',
      'ant-pwd-strength-high': strength === 'H',
    });

    const level = {
      L: 'Low',
      M: 'Middle',
      H: 'High',
    };

    return (
      <div>
        <ul className={classSet}>
          <li className="ant-pwd-strength-item ant-pwd-strength-item-1"></li>
          <li className="ant-pwd-strength-item ant-pwd-strength-item-2"></li>
          <li className="ant-pwd-strength-item ant-pwd-strength-item-3"></li>
          <span className="ant-form-text">
            {level[strength]}
          </span>
        </ul>
      </div>
    );
  }

  render() {
    const formInputLayout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };

    const props = this.props,
          { getFieldDecorator } = props.form;

    const rules = [
      { required: true, message: '必填项' },
      { min: 6, max: 18, message: '无效密码, 必须有6-12个字符组成' },
    ];

    return (
      <Form layout="horizontal">
        <Row>
          <Col span={16}>
            <FormItem
              {...formInputLayout}
              label="旧密码"
            >
              {getFieldDecorator('oldPassword', {
                rules: rules
              })(
                <Input
                  type="password"
                  id="oldPassword"
                  autoComplete="off"
                  onContextMenu={noop}
                  onPaste={noop}
                  onCopy={noop}
                  onCut={noop}
                />
              )}
            </FormItem>
          </Col>
        </Row>
        <Row>
          <Col span={16}>
            <FormItem
              {...formInputLayout}
              label="新密码"
            >
              {getFieldDecorator('newPassword', {
                rules: [
                  ...rules,
                  { validator: this.checkPassword }
                ]
              })(
                <Input
                  type="password"
                  id="newPassword"
                  autoComplete="off"
                  onContextMenu={noop}
                  onPaste={noop}
                  onCopy={noop}
                  onCut={noop}
                />
              )}
            </FormItem>
          </Col>
          <Col span={8}>
            {this.state.newPasswordBarShow ? this.renderPasswordStrengthBar('newPassword') : null}
          </Col>
        </Row>
        <Row>
          <Col span={16}>
            <FormItem
              {...formInputLayout}
              label="确认新密码"
            >
              {getFieldDecorator('reNewPassword', {
                rules: [
                  ...rules,
                  { validator: this.checkRePassword }
                ]
              })(
                <Input
                  type="password"
                  id="reNewPassword"
                  autoComplete="off"
                  onContextMenu={noop}
                  onPaste={noop}
                  onCopy={noop}
                  onCut={noop}
                />
              )}
            </FormItem>
          </Col>
          <Col span={8}>
            {this.state.reNewPasswordBarShow ? this.renderPasswordStrengthBar('reNewPassword') : null}
          </Col>
        </Row>
        <Row>
          <Col
            span="16"
            offset="8"
          >
            <Button
              type="ghost"
              onClick={this.handleReset}
            >
              {props.resetText}
            </Button>
            &nbsp;&nbsp;&nbsp;
            <Button
              type="primary"
              onClick={this.handleSubmit}
            >
              {props.submitText}
            </Button>
          </Col>
        </Row>
      </Form>
    );
  }
}

ChangePassword.defaultProps = {
  resetText: '重置',
  submitText: '提交',
  onSubmit() {},
};

ChangePassword.propTypes = {
  form: PropTypes.object,
  resetText: PropTypes.string,
  submitText: PropTypes.string,
  onSubmit: PropTypes.func,
};

export default ChangePassword = Form.create({})(ChangePassword);
