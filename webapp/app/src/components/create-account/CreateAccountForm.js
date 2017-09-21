'use strict';
import React, { Component, PropTypes } from 'react';
import { checkAccount } from 'request/account';
import { getCaptcha, getSmscode } from 'request/captchaverify';

import {
  Form,
  Input,
  Button,
  message,
  Modal,
} from 'antd';

const FormItem = Form.Item;

class CreateAccountForm extends Component {
  constructor() {
    super();
    this.handleClick = this.handleClick.bind(this);
    this.handlePhoneClick = this.handlePhoneClick.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
    this.getCaptchaPng = this.getCaptchaPng.bind(this);
  }

  state = {
    confirmDirty: false,
    result: false,
    image: null,
    smscode: '',
    visible:false,
  };

  handleCancel = (e) => {
    this.setState({
      visible: false,
    });
  }

  handlePhoneClick(e) {
     e.preventDefault();
  this.props.form.validateFields(
    ['phone'],(errors, values) => {
      if (!errors) {
        this.setState({
          visible : true,
        })
      }
    });
  }

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
      if (json.result === true) {
          this.setState({result: true})
          form.validateFields(['name'], { force: true });
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

  checkCaptcha = (rule, value, callback) => {
    const form = this.props.form;
    if(value && value.length === 4) {   
      getSmscode({
       captcha: value,
       phone: form.getFieldValue('phone')
      },(json) => {
       if (json.result === true) {
          callback();
          this.setState({
          visible : false,
          });
       } else {
          this.getCaptchaPng();
          callback('验证码错误，请重新输入!');
       }
     });
    } else {callback('验证码长度必须4位')}
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

  getCaptchaPng (){
    getCaptcha((blob) => {
      if (blob){
        this.setState({
          image : URL.createObjectURL(blob),
        });
      }
    });
  }

  componentWillMount() {
    this.getCaptchaPng();
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
              required: true, message: '手机号码是地址必填项',},
              {len: 11,message: '手机长度为11位'}
            ],
          })(
            <Input />
          )}
        </FormItem>
        <FormItem label="短信验证码">
          {getFieldDecorator('smscode',{
            rules: [{
              required: true, message: '短信验证码是地址必填项',}
            ],
          })(
            <Input />
          )}
          <Button type="primary" onClick={this.handlePhoneClick}>
            {"获取验证码"}
          </Button>
        </FormItem>
        <Modal
          visible={this.state.visible}
          onCancel={this.handleCancel}
          title={'发送手机验证码'}
          width={'350px'}
          footer={null}
        >
        <FormItem label="验证码" >
        {getFieldDecorator('captcha', {
            rules: [{
              required: true, message: '验证码是必填项'},{
            },
            {
              validator: this.checkCaptcha,
            }]
          })(<Input />)}
        <img src={this.state.image} onClick={this.getCaptchaPng}>
        </img>
        </FormItem>
        </Modal>
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
