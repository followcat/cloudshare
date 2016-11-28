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
      callback('Twice password input value are inconsistent.');
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
          { getFieldProps } = props.form;

    //旧密码表单验证
    const oldPasswordProps = getFieldProps('oldPassword', {
      rules: [
        { required: true, message: 'Password is required.' },
        { min: 6, max: 18, message: 'Invalid Password. (At least 6-12 characters)' },
      ]
    });

    //新密码表单验证
    const newPasswordProps = getFieldProps('newPassword', {
      rules: [
        { required: true, message: 'Password is required.'},
        { min: 6, max: 12, message: 'Invalid Password. (At least 6-12 characters)' },
        { validator: this.checkPassword }
      ]
    });
    const reNewPasswordProps = getFieldProps('reNewPassword', {
      rules: [
        { required: true, message: 'Password is required.'},
        { min: 6, max: 12, message: 'Invalid Password. (At least 6-12 characters)' },
        { validator: this.checkRePassword }
      ]
    });

    return (
      <Form horizontal>
        {/*old password*/}
        <Row>
          <Col span={16}>
            <FormItem
              {...formInputLayout}
              label="Old password"
            >
              <Input
                {...oldPasswordProps}
                type="password"
                id="oldPassword"
                autoComplete="off"
                onContextMenu={noop}
                onPaste={noop}
                onCopy={noop}
                onCut={noop}
              />
            </FormItem>
          </Col>
        </Row>
        {/*old password end*/}
        {/*new password*/}
        <Row>
          <Col span={16}>
            <FormItem
              {...formInputLayout}
              label="New password"
            >
              <Input
                {...newPasswordProps}
                type="password"
                id="newPassword"
                autoComplete="off"
                onContextMenu={noop}
                onPaste={noop}
                onCopy={noop}
                onCut={noop}
              />
            </FormItem>
          </Col>
          <Col span={8}>
            {this.state.newPasswordBarShow ? this.renderPasswordStrengthBar('newPassword') : null}
          </Col>
        </Row>
        {/*new password end*/}
        {/*new password confirmation*/}
        <Row>
          <Col span={16}>
            <FormItem
              {...formInputLayout}
              label="Password confirmation"
            >
              <Input
                {...reNewPasswordProps}
                type="password"
                id="reNewPassword"
                autoComplete="off"
                onContextMenu={noop}
                onPaste={noop}
                onCopy={noop}
                onCut={noop}
              />
            </FormItem>
          </Col>
          <Col span={8}>
            {this.state.reNewPasswordBarShow ? this.renderPasswordStrengthBar('reNewPassword') : null}
          </Col>
        </Row>
        {/*new password confirmation end*/}
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
  resetText: 'Reset',
  submitText: 'Submit',
  onSubmit() {},
};

ChangePassword.propTypes = {
  resetText: PropTypes.string,
  submitText: PropTypes.string,
  onSubmit: PropTypes.func,
};

export default ChangePassword = Form.create({})(ChangePassword);
