'use strict';
import React, { Component, PropTypes } from 'react';

import { Modal, Form, Input, Select } from 'antd';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;
const FormItem = Form.Item,
      Option = Select.Option;

class EditJobDescriptionForm extends Component {
  constructor() {
    super();
    this.handleModalOK = this.handleModalOK.bind(this);
  }

  handleModalOK() {
    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        return;
      } else {
        this.props.onSubmit(values);
      }
    });
  }

  render() {
    const props = this.props,
          { getFieldProps } = props.form;
    
    const formItemLayout = {
      labelCol: { span: 6 },
      wrapperCol: { span: 16 },
    };

    const status = [{
      value: 'Opening',
      text: language.OPENING
    }, {
      value: 'Closed',
      text: language.CLOSED
    }];

    return (
      <Modal
        title={language.EDIT_JOB_DESCRIPTION}
        okText={language.SUBMIT}
        visible={props.visible}
        confirmLoading={props.confirmLoading}
        onOk={this.handleModalOK}
        onCancel={props.onCancel}
      >
        <Form horizontal>
          <FormItem
            {...formItemLayout}
            label={language.JOB_DESCRIPTION_ID}
          >
            <Input 
              {...getFieldProps('id', { initialValue: props.record.id })}
              readOnly
            />
          </FormItem>
          <FormItem
            {...formItemLayout}
            label={language.COMPANY_NAME}
          >
            <Select
              {...getFieldProps('company', { initialValue: props.record.company })}
              disabled={true}
            >
              {props.customerDataSource.map(v => {
                return (
                  <Option
                    key={v.id}
                    value={v.id}
                  >
                    {v.name}
                  </Option>
                );
              })}
            </Select>
          </FormItem>
          <FormItem
            {...formItemLayout}
            label={language.JOB_DESCRIPTION_CONTENT}
          >
            <Input
              {...getFieldProps('description', {
                initialValue: props.record.description,
                rules: [{ required: true }]
              })}
              type="textarea"
              rows="6"
              disabled={props.record.committer !== localStorage.user}
            />
          </FormItem>
          <FormItem
            {...formItemLayout}
            label={language.COMMENTARY}
          >
            <Input
              {...getFieldProps('commentary', {
                initialValue: props.record.commentary,
              })}
              type="textarea"
              rows="2"
            />
          </FormItem>
          <FormItem
            {...formItemLayout}
            label={language.CURRENT_STATUS}
          >
            <Select {...getFieldProps('status', { initialValue: props.record.status })}>
              {status.map(item => {
                return (
                  <Option
                    key={item.value}
                    value={item.value}
                  >
                    {item.text}
                  </Option>
                );
              })}
            </Select>
          </FormItem>
        </Form>
      </Modal>
    );
  }
}

EditJobDescriptionForm.propTypes = {
  form: PropTypes.shape({
    getFieldProps: PropTypes.func,
    validateFields: PropTypes.func
  }),
  onSubmit: PropTypes.func
};

export default EditJobDescriptionForm = Form.create({})(EditJobDescriptionForm);
