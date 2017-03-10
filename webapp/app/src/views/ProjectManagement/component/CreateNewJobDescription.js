'use strict';
import React, { Component, PropTypes } from 'react';

import ButtonWithModal from 'components/button-with-modal';

import { Form, Input, Select } from 'antd';

import websiteText from 'config/website-text';

const language = websiteText.zhCN;
const FormItem = Form.Item,
      Option = Select.Option;

class CreateNewJobDescription extends Component {
  constructor() {
    super();
    this.handleModalOk = this.handleModalOk.bind(this);
  }

  handleModalOk() {
    this.props.form.validateFields((errors, values) => {
      if (!!errors) {
        return;
      } else {
        this.props.onCreate(values);
        this.props.form.resetFields();
      }
    });
  }

  render() {
    const props = this.props,
          { getFieldDecorator } = props.form;

    return (
      <ButtonWithModal
        {...props}
        onModalOk={this.handleModalOk}
      >
        <Form layout="horizontal">
          <FormItem label={language.COMPANY_NAME}>
            {getFieldDecorator('co_id', {
              rules: [{ required: true, message: language.COMPANY_NAME_VALIDATE_MSG }]
            })(
              <Select>
                {props.companyList.map(item => {
                  return (
                    <Option key={item.id} value={item.id}>
                      {item.name}
                    </Option>
                  );
                })}
              </Select>
            )}
          </FormItem>
          <FormItem label={language.JOB_DESCRIPTION_NAME}>
            {getFieldDecorator('jd_name')(<Input />)}
          </FormItem>
          <FormItem label={language.JOB_DESCRIPTION_CONTENT}>
            {getFieldDecorator('jd_description')(
              <Input type="textarea" rows="4" />
            )}
          </FormItem>
        </Form>
      </ButtonWithModal>
    );
  }
}

CreateNewJobDescription.defaultProps = {
  companyList: [],
  onCreate() {},
};

CreateNewJobDescription.propTypes = {
  form: PropTypes.object,
  companyList: PropTypes.array,
  onCreate: PropTypes.func,
};

export default CreateNewJobDescription = Form.create({})(CreateNewJobDescription);
