'use strict';
import React, { Component, PropTypes } from 'react';

import ButtonWithModal from 'components/button-with-modal';

import { Form, Input } from 'antd';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

class CreateNewCompany extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
    };
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.handleModalOk = this.handleModalOk.bind(this);
    this.handleModalCancel = this.handleModalCancel.bind(this);
  }

  handleButtonClick() {
    this.setState({
      visible: true,
    });
  }

  handleModalOk() {
    this.props.form.validateFields((errors, values) => {
      if (!errors) {
        this.setState({
          visible: false
        });
        this.props.onSubmit(values);
        return;
      }
    });
  }

  handleModalCancel() {
    this.props.form.resetFields();
    this.setState({
      visible: false,
    });
  }

  render() {
    const { getFieldDecorator } = this.props.form;

    const formItemLayout = {
      labelCol: { span: 5 },
      wrapperCol: { span: 17 },
    };

    return (
      <ButtonWithModal
        buttonType="primary"
        buttonText={language.CREATION}
        modalTitle={language.CREATION}
        modalOkText={language.SUBMIT}
        modalCancelText={language.CANCEL}
        visible={this.state.visible}
        confirmLoading={this.props.confirmLoading}
        onButtonClick={this.handleButtonClick}
        onModalOk={this.handleModalOk}
        onModalCancel={this.handleModalCancel}
        buttonStyle={{ marginLeft: 8 }}
        modalStyle={{ top: 20 }}
      >
        <Form layout="horizontal">
          <Form.Item
            label={language.COMPANY_NAME}
            {...formItemLayout}
          >
            {getFieldDecorator('name', {
              rules: [{ required: true, message: '公司名称是必填项', whitespace:true}]
            })(
              <Input placeholder={`${language.INPUT_PLACEHOLDER}${language.COMPANY_NAME}`} />
            )}
          </Form.Item>
          <Form.Item
            label={language.COMPANY_INTRODUCTION}
            {...formItemLayout}
          >
            {getFieldDecorator('introduction')(
              <Input
                type="textarea"
                rows="2"
                placeholder={`${language.INPUT_PLACEHOLDER}${language.COMPANY_INTRODUCTION}`}
              />
            )}
          </Form.Item>
          <Form.Item
            label={language.DISTRICT}
            {...formItemLayout}
          >
            {getFieldDecorator('district')(
              <Input placeholder={`${language.INPUT_PLACEHOLDER}${language.DISTRICT}`} />
            )}
          </Form.Item>
          <Form.Item
            label={language.PRODUCT}
            {...formItemLayout}
          >
            {getFieldDecorator('product')(
              <Input placeholder={`${language.INPUT_PLACEHOLDER}${language.PRODUCT}`} />
            )}
          </Form.Item>
          <Form.Item
            label={language.TELLPHONE}
            {...formItemLayout}
          >
            {getFieldDecorator('conumber')(
              <Input placeholder={`${language.INPUT_PLACEHOLDER}${language.TELLPHONE}`} />
            )}
          </Form.Item>
          <Form.Item
            label={language.ADDRESS}
            {...formItemLayout}
          >
            {getFieldDecorator('address')(
              <Input placeholder={`${language.INPUT_PLACEHOLDER}${language.ADDRESS}`} />
            )}
          </Form.Item>
          <Form.Item
            label={language.EMAIL}
            {...formItemLayout}
          >
            {getFieldDecorator('email', {
              rules: [{ type: 'email', message: language.EMAIL_VALIDATE_TIP }]
            })(
              <Input placeholder={`${language.INPUT_PLACEHOLDER}${language.EMAIL}`} />
            )}
          </Form.Item>
          <Form.Item
            label={language.WEBSITE}
            {...formItemLayout}
          >
            {getFieldDecorator('website')(
              <Input placeholder={`${language.INPUT_PLACEHOLDER}${language.WEBSITE}`} />
            )}
          </Form.Item>
        </Form>
      </ButtonWithModal>
    );
  }
}

CreateNewCompany.propTypes = {
  confirmLoading: PropTypes.bool,
  onSubmit: PropTypes.func,
  form: PropTypes.shape({
    getFieldDecorator: PropTypes.func,
    resetFields: PropTypes.func,
    validateFields: PropTypes.func,
  }),
};

export default CreateNewCompany = Form.create({})(CreateNewCompany);