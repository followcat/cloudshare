'use strict';
import React, { Component, PropTypes } from 'react';
import ButtonWithModal from '../../../components/button-with-modal';
import { Form, Input, Select } from 'antd';

import websiteText from '../../../config/website-text';

const language = websiteText.zhCN;
const FormItem = Form.Item,
      SelectOption = Select.Option;

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
          { getFieldProps } = props.form;

    const companyNameProps = getFieldProps('co_id', {
      rules: [{ required: true, message: language.COMPANY_NAME_VALIDATE_MSG }]
    });

    const jobDescriptionNameProps = getFieldProps('jd_name', {
      rules: [{ required: true, message: language.JOB_DESCRIPTION_NAME_VALIDATE_MSG }]
    });

    const jobDescriptionContentProps = getFieldProps('jd_description', {
      rules: [{ required: true, message: language.JOB_DESCRIPTION_CONTENT_VALIDATE_MSG }]
    });

    return (
      <ButtonWithModal
        {...props}
        onModalOk={this.handleModalOk}
      >
        <Form horizontal>
          <FormItem
            label={language.COMPANY_NAME}
          >
            <Select {...companyNameProps}>
              {props.companyList.map(item => {
                return (
                  <SelectOption
                    key={item.id}
                    value={item.id}
                  >
                    {item.name}
                  </SelectOption>
                );
              })}
            </Select>
          </FormItem>
          <FormItem
            label={language.JOB_DESCRIPTION_NAME}
          >
            <Input {...jobDescriptionNameProps}/>
          </FormItem>
          <FormItem
            label={language.JOB_DESCRIPTION_CONTENT}
          >
            <Input
              {...jobDescriptionContentProps}
              type="textarea"
              rows="4"
            />
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
  companyList: PropTypes.array,
  onCreate: PropTypes.func,
};

export default CreateNewJobDescription = Form.create({})(CreateNewJobDescription);
