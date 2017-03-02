'use strict';
import React, { Component, PropTypes } from 'react';

import ButtonWithModal from 'components/button-with-modal';

import { Form, Input } from 'antd';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;

const FormItem = Form.Item;

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
    this.setState({
      visible: false
    });
    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        return;
      }
      this.props.onSubmit(values);
    });
  }

  handleModalCancel() {
    this.props.form.resetFields();
    this.setState({
      visible: false,
    });
  }

  render() {
    const { getFieldProps } = this.props.form;

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
        <Form horizontal>
          <FormItem
            label={language.COMPANY_NAME}
            {...formItemLayout}
          >
            <Input
              {...getFieldProps('name', { rules: [{ required: true }] })}
              placeholder={`${language.INPUT_PLACEHOLDER}${language.COMPANY_NAME}`}
            />
          </FormItem>
          <FormItem
            label={language.RESPONSIBLE}
            {...formItemLayout}
          >
            <Input
              {...getFieldProps('priority', { rules: [{ required: true }] })}
              placeholder={`${language.INPUT_PLACEHOLDER}${language.RESPONSIBLE}`}
            />
          </FormItem>
          <FormItem
            label={language.COMPANY_INTRODUCTION}
            {...formItemLayout}
          >
            <Input
              {...getFieldProps('introduction')}
              type="textarea"
              rows="2"
              placeholder={`${language.INPUT_PLACEHOLDER}${language.COMPANY_INTRODUCTION}`}
            />
          </FormItem>
          <FormItem
            label={language.DISTRICT}
            {...formItemLayout}
          >
            <Input
              {...getFieldProps('district')}
              placeholder={`${language.INPUT_PLACEHOLDER}${language.DISTRICT}`}
            />
          </FormItem>
          <FormItem
            label={language.PRODUCT}
            {...formItemLayout}
          >
            <Input
              {...getFieldProps('product')}
              placeholder={`${language.INPUT_PLACEHOLDER}${language.PRODUCT}`}
            />
          </FormItem>
          <FormItem
            label={language.TELLPHONE}
            {...formItemLayout}
          >
            <Input
              {...getFieldProps('conumber')}
              placeholder={`${language.INPUT_PLACEHOLDER}${language.TELLPHONE}`}
            />
          </FormItem>
          <FormItem
            label={language.ADDRESS}
            {...formItemLayout}
          >
            <Input
              {...getFieldProps('address')}
              placeholder={`${language.INPUT_PLACEHOLDER}${language.ADDRESS}`}
            />
          </FormItem>
          <FormItem
            label={language.EMAIL}
            {...formItemLayout}
          >
            <Input
              {...getFieldProps('email', { rules: [{ type: 'email', message: language.EMAIL_VALIDATE_TIP }] })}
              placeholder={`${language.INPUT_PLACEHOLDER}${language.EMAIL}`}
            />
          </FormItem>
          <FormItem
            label={language.WEBSITE}
            {...formItemLayout}
          >
            <Input
              {...getFieldProps('website')}
              placeholder={`${language.INPUT_PLACEHOLDER}${language.WEBSITE}`}
            />
          </FormItem>
        </Form>
      </ButtonWithModal>
    );
  }
}

CreateNewCompany.propTypes = {
  confirmLoading: PropTypes.bool,
  onSubmit: PropTypes.func,
  form: PropTypes.shape({
    getFieldProps: PropTypes.func,
    resetFields: PropTypes.func,
    validateFields: PropTypes.func,
  }),
};

export default CreateNewCompany = Form.create({})(CreateNewCompany);
