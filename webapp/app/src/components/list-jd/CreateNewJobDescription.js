'use strict';
import React, { Component, PropTypes } from 'react';
import ButtonWithModal from '../button-with-modal';
import { Form, Input, Select } from 'antd';
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

    const companyProps = getFieldProps('companyName', {
      rules: [
        { required: true, message: 'Please choose a company name.' },
      ],
    });
    const jdNameProps = getFieldProps('jobDescriptionName', {
      rules: [
        { required: true, message: 'Please input job description project name.' },
      ],
    });
    const jdContentProps = getFieldProps('jobDescriptionContent', {
      rules: [
        { required: true, message: 'Please input job description content.' },
      ],
    });

    return (
      <ButtonWithModal
        {...props}
        onModalOk={this.handleModalOk}
      >
        <Form horizontal>
          <FormItem
            id="companyName"
            label="Company Name"
          >
            <Select {...companyProps}>
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
            id="jobDescriptionName"
            label="Job Description Project Name"
          >
            <Input {...jdNameProps}/>
          </FormItem>
          <FormItem
            id="jobDescriptionContent"
            label="Job Description Content"
          >
            <Input
              {...jdContentProps}
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
