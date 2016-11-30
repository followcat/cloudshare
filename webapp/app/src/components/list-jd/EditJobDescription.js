'use strict';
import React, { Component, PropTypes } from 'react';
import ButtonWithModal from '../button-with-modal';
import { Form, Input, Select } from 'antd';
const FormItem = Form.Item,
      Option = Select.Option;

class EditJobDescription extends Component {
  constructor() {
    super();
    this.state = {
      visible: false,
    };
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.handleModalOK = this.handleModalOK.bind(this);
    this.handleModalCancel = this.handleModalCancel.bind(this);
  }

  handleButtonClick() {
    const record = this.props.record;

    this.props.form.setFieldsValue({
      jobDescriptionID: record.id,
      company: record.company,
      jobDescriptionContent: record.description,
      status: record.status,
    });

    this.setState({
      visible: true,
    });
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

  handleModalCancel() {
    this.setState({
      visible: false,
    });
  }

  render() {
    const props = this.props,
          { getFieldProps } = props.form;

    return (
      <ButtonWithModal
        {...props}
        visible={this.state.visible}
        onButtonClick={this.handleButtonClick}
        onModalCancel={this.handleModalCancel}
        onModalOk={this.handleModalOK}
      >
        <Form horizontal>
          <FormItem
            id="jobDescriptionID"
            label="Job Description ID"
          >
            <Input 
              {...getFieldProps('jobDescriptionID')}
              readOnly
            />
          </FormItem>
          <FormItem
            label="Company Name"
          >
            <Select
              {...getFieldProps('company')}
            >
              {props.companyList.map(item => {
                return (
                  <Option
                    key={item.id}
                    value={item.id}
                  >
                    {item.name}
                  </Option>
                );
              })}
            </Select>
          </FormItem>
          <FormItem
            label="Job Description Content"
          >
            <Input
              {...getFieldProps('jobDescriptionContent', {
                rules: [{ required: true }]
              })}
              type="textarea"
              rows="4"
            />
          </FormItem>
          <FormItem
            label="Status"
          >
            <Select
              {...getFieldProps('status')}
            >
              {props.status.map(item => {
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
      </ButtonWithModal>
    );
  }
}

EditJobDescription.defaultProps = {
  companyList: [],
  onSubmit() {},
};

EditJobDescription.propTypes = {
  companyList: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string,
    name: PropTypes.string,
  })),
  status: PropTypes.arrayOf(PropTypes.shape({
    value: PropTypes.string,
    text: PropTypes.string,
  })),
  onSubmit: PropTypes.func,
};

export default EditJobDescription = Form.create({})(EditJobDescription);
