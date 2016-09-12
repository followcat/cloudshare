import React from 'react';

import { Button, Form, Input, Row, Col } from 'antd';

import './changepassword.less';

import classNames from 'classnames';

function noop() {
  return false;
}

class ChangePassword extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      newPwdBarShow: false,
      rePwdBarShow: false,
      newPwdStrength: 'L',
      rePwdStrength: 'L',
    };
    this.handleReset = this.handleReset.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.getPassStrenth = this.getPassStrenth.bind(this);
    this.renderPassStrengthBar = this.renderPassStrengthBar.bind(this);
    this.checkPassword = this.checkPassword.bind(this);
    this.checkRePassword = this.checkRePassword.bind(this);
  }

  handleReset(e) {
    e.preventDefault();
    this.props.form.resetFields();
  }

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

  getPassStrenth(value, type) {
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
      if (type === 'newPwd') {
        this.setState({ newPwdBarShow: true, newPwdStrength: strength });
      } else {
        this.setState({ rePwdBarShow: true, rePwdStrength: strength });
      }
    } else {
      if (type === 'newPwd') {
        this.setState({ newPwdBarShow: false });
      } else {
        this.setState({ rePwdBarShow: false });
      }
    }
  }

  renderPassStrengthBar(type) {
    const strength = type === 'newPwd' ? this.state.newPwdStrength : this.state.rePwdStrength;
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

  checkPassword(rule, value, callback) {
    const { validateFields } = this.props.form;
    this.getPassStrenth(value, 'newPwd');

    if (value) {
      validateFields(['reNewPwd'], { force: true });
    }
    callback(); 
  }

  checkRePassword(rule, value, callback) {
    const { getFieldValue } = this.props.form;
    this.getPassStrenth(value, 'reNewPwd');

    if (value && value !== getFieldValue('newPwd')) {
      callback('Twice password input value are inconsistent.');
    } else {
      callback();
    }
  }

  render() {
    const formInputLayout = {
      labelCol: { span: 8 },
      wrapperCol: { span: 16 },
    };

    const { getFieldProps } = this.props.form;

    //旧密码表单验证
    const oldPwdProps = getFieldProps('oldPwd', {
      rules: [
        { required: true, message: 'Password is required.' },
        { min: 6, max: 18, message: 'Invalid Password. (At least 6-12 characters)' },
      ]
    });

    //新密码表单验证
    const newPwdProps = getFieldProps('newPwd', {
      rules: [
        { required: true, message: 'Password is required.'},
        { min: 6, max: 18, message: 'Invalid Password. (At least 6-12 characters)' },
        { validator: this.checkPassword }
      ]
    });


    const reNewPwdProps = getFieldProps('reNewPwd', {
      rules: [
        { required: true, message: 'Password is required.'},
        { min: 6, max: 18, message: 'Invalid Password. (At least 6-12 characters)' },
        { validator: this.checkRePassword }
      ]
    });

    return (
      <div>
        <Form horizontal>
          <Row>
            <Col span="18">
              <Form.Item
                {...formInputLayout}
                label="Old Password"
              >
                <Input
                  {...oldPwdProps}
                  type="password"
                  id="oldPwd"
                  autoComplete="off"
                  onContextMenu={noop}
                  onPaste={noop}
                  onCopy={noop}
                  onCut={noop}
                />
              </Form.Item>
            </Col>
            <Col span="6">
              {this.state.oldPwdBarShow ? this.renderPassStrengthBar('oldPwd') : null}
            </Col>
          </Row>

          <Row>
            <Col span="18">
              <Form.Item
                {...formInputLayout}
                label="New Password"
              >
                <Input
                  {...newPwdProps}
                  type="password"
                  id="newPwd"
                  autoComplete="off"
                  onContextMenu={noop}
                  onPaste={noop}
                  onCopy={noop}
                  onCut={noop}
                />
              </Form.Item>
            </Col>
            <Col span="6">
              {this.state.newPwdBarShow ? this.renderPassStrengthBar('newPwd') : null}
            </Col>
          </Row>
          
          <Row>
            <Col span="18">
              <Form.Item
                {...formInputLayout}
                label="Password Confirmation"
              >
                <Input
                  {...reNewPwdProps}
                  type="password"
                  id="reNewPwd"
                  autoComplete="off"
                  onContextMenu={noop}
                  onPaste={noop}
                  onCopy={noop}
                  onCut={noop}
                />
              </Form.Item>
            </Col>
            <Col span="6">
              {this.state.rePwdBarShow ? this.renderPassStrengthBar('reNewPwd') : null}
            </Col>
          </Row>
          <Row>
            <Col span="16" offset="8">
              <Button type="ghost" onClick={this.handleReset}>Reset</Button>
              &nbsp;&nbsp;&nbsp;
              <Button type="primary" onClick={this.handleSubmit}>Submit</Button>
            </Col>
          </Row>
        </Form>
      </div>
    );
  }
}

export default ChangePassword = Form.create({})(ChangePassword);